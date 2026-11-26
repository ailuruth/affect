"""Checks 11-15: the Claude Code command-line tool, through the operator's own login, text only (D84).

Refuses until `claude_test_calls_m1` (Q34 item 1, M1 test calls only) is answered. Every call sends only short
scripted text written here (no audio, video, features, state or anything about him), with model `haiku`, effort
`low`, no tools, a fixed one-line system prompt, and the auto-updater off. Sub-commands, 20 calls each:
  resume      a hand-written transcript (a session file with a code word) is resumed with --fork-session: accepted
              if the reply contains the code word, identical if the hand-written file is byte-identical afterwards
  thinking    calls at effort low: runs whose stream contains any thinking content
  latency     first-sentence latency p90 (spawn to the first sentence end in the streamed text)
  compaction  whether an auto-compaction switch exists (help text and settings) and is off (no call is made)
  tokens      tokens per call (the CLI's usage count) with a 4,000-token scripted transcript window
Run:
    uv run python -m tools.week0.claude_checks resume|thinking|latency|compaction|tokens
"""
from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys
import time
import uuid
from pathlib import Path

from engine.config.innate import ENTRIES
from tools.week0 import common, thresholds

SYSTEM = "Answer in one or two short plain sentences."
RUNS = thresholds.TH["claude_runs"]
SENTENCE_END = re.compile(r"[.!?](\s|$)")


def _base(sw) -> list:
    return [common.require_tool("claude", "install Claude Code and log in first"), "-p", "--model", sw["claude_model"],
            "--effort", sw["effort"], "--tools", "", "--system-prompt", SYSTEM, "--strict-mcp-config"]


def _env() -> dict:
    return dict(os.environ, DISABLE_AUTOUPDATER="1")


def stream_call(sw, prompt: str, cwd: Path, extra=()) -> dict:
    """One streamed call: first-sentence latency, text, thinking characters, usage."""
    cmd = _base(sw) + ["--output-format", "stream-json", "--verbose", "--include-partial-messages", *extra, prompt]
    t0 = time.perf_counter()
    pr = subprocess.Popen(cmd, cwd=cwd, env=_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    text, thinking, first, usage, rc_ok = "", 0, None, {}, False
    for line in pr.stdout:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "stream_event":
            d = ev.get("event", {}).get("delta", {})
            if d.get("type") == "text_delta":
                text += d.get("text", "")
                if first is None and SENTENCE_END.search(text):
                    first = time.perf_counter() - t0
            elif d.get("type") == "thinking_delta":
                thinking += len(d.get("thinking", ""))
        elif ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "thinking":
                    thinking += len(b.get("thinking", ""))
        elif ev.get("type") == "result":
            usage = ev.get("usage", {})
            rc_ok = not ev.get("is_error", False)
            text = text or ev.get("result", "")
    pr.wait(timeout=120)
    if first is None and text:
        first = time.perf_counter() - t0
    return {"text": text, "first_s": first, "thinking_chars": thinking, "usage": usage, "ok": rc_ok and pr.returncode == 0}


def _workdir() -> Path:
    d = common.local_path("claude_cwd")
    d.mkdir(exist_ok=True)
    return d


def _project_dir(cwd: Path) -> Path:
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd.resolve()))


def handwritten_session(cwd: Path, code: str) -> tuple:
    """A hand-written two-turn transcript in the CLI's session-file format; returns (session id, path)."""
    sid = str(uuid.uuid4())
    u1, a1 = str(uuid.uuid4()), str(uuid.uuid4())
    ts = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    base = {"sessionId": sid, "cwd": str(cwd.resolve()), "isSidechain": False, "userType": "external", "timestamp": ts}
    lines = [dict(base, type="user", uuid=u1, parentUuid=None,
                  message={"role": "user", "content": f"The code word for this test is {code}."}),
             dict(base, type="assistant", uuid=a1, parentUuid=u1,
                  message={"role": "assistant", "type": "message", "model": "scripted",
                           "content": [{"type": "text", "text": "Noted."}]})]
    d = _project_dir(cwd)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{sid}.jsonl"
    path.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in lines))
    return sid, path


def window_text(tokens: int) -> str:
    """A scripted transcript window of about `tokens` tokens (about 0.75 words per token) from the reading text."""
    words = (common.ROOT / "tools" / "week0" / "reading.txt").read_text().split()
    need = int(0.75 * tokens)
    out = []
    while len(out) < need:
        out += words
    body = " ".join(out[:need])
    return f"Transcript so far:\n{body}\n\nReply to the last line in one sentence."


def compaction_switch(help_text: str, settings: dict) -> tuple:
    """(found, off): a settings key or an option that turns auto-compaction off."""
    for k in ("autoCompactEnabled", "autoCompact"):
        if k in settings:
            return True, settings[k] in (False, "off", "false")
    if re.search(r"DISABLE_AUTO_COMPACT|auto-?compact[^\n]*\b(off|disable|false)\b", help_text, re.I):
        return True, os.environ.get("DISABLE_AUTO_COMPACT") in ("1", "true")
    return False, False


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("which", choices=("resume", "thinking", "latency", "compaction", "tokens"))
    args = p.parse_args(argv)
    if args.which != "compaction":
        common.require_approval("claude_test_calls_m1")
    sw = common.require_approval("claude_model", "effort")
    cwd = _workdir()
    if args.which == "compaction":
        cli = common.require_tool("claude", "install Claude Code first")
        help_text = subprocess.run([cli, "--help"], capture_output=True, text=True, env=_env()).stdout
        settings = {}
        for f in (Path.home() / ".claude" / "settings.json", Path.home() / ".claude.json"):
            try:
                settings.update(json.loads(f.read_text()))
            except (OSError, ValueError):
                pass
        v = thresholds.claude_compaction(*compaction_switch(help_text, settings))
        return common.finish(v, args, load="-")
    if args.which == "resume":
        ok = 0
        for _ in range(RUNS):
            code = secrets.token_hex(3)
            sid, path = handwritten_session(cwd, code)
            before = path.read_bytes()
            r = stream_call(sw, "What is the code word? Reply with the word only.", cwd, ("--resume", sid, "--fork-session"))
            ok += bool(r["ok"] and code in r["text"] and path.read_bytes() == before)
            path.unlink(missing_ok=True)
        return common.finish(thresholds.claude_resume(ok, RUNS), args, load="-")
    if args.which in ("thinking", "latency"):
        rs = [stream_call(sw, f"Say one sentence about the number {i}.", cwd, ("--no-session-persistence",))
              for i in range(RUNS)]
        if args.which == "thinking":
            with_t = [r for r in rs if r["thinking_chars"] > 0]
            mean_tokens = round(sum(r["thinking_chars"] for r in rs) / 4.0 / len(rs), 1)   # ~4 characters per token
            return common.finish(thresholds.claude_thinking(len(with_t), len(rs), mean_tokens), args, load="-")
        firsts = [r["first_s"] for r in rs if r["first_s"] is not None]
        if len(firsts) < RUNS:
            raise common.Refused(f"only {len(firsts)} of {RUNS} calls returned text")
        return common.finish(thresholds.claude_latency(round(thresholds.percentile(firsts, 90), 3)), args, load="-")
    window = ENTRIES["context_window"].value["tokens_max"]
    rs = [stream_call(sw, window_text(window) + f" ({i})", cwd, ("--no-session-persistence",)) for i in range(RUNS)]
    counts = [sum(int(r["usage"].get(k, 0)) for k in ("input_tokens", "cache_creation_input_tokens",
                                                       "cache_read_input_tokens", "output_tokens")) for r in rs if r["usage"]]
    if len(counts) < RUNS:
        raise common.Refused(f"only {len(counts)} of {RUNS} calls reported usage")
    return common.finish(thresholds.claude_tokens(round(thresholds.percentile(counts, 90), 1)), args, load="-",
                         note=f"window {window} tokens; p90 of {len(counts)} calls")


if __name__ == "__main__":
    sys.exit(main())
