#!/usr/bin/env python3
"""A fake Claude Code CLI for the omega tests: it mimics `claude -p --input-format stream-json --output-format
stream-json --verbose --include-partial-messages [--resume SID --fork-session]` and makes no network call.

It starts idle, reads one user message (a JSON line) from stdin, writes the fork's session file the way the CLI does
(the resumed history under a new session id, then the user message, then the reply), and streams the reply word by
word as `stream_event` text deltas (plus a thinking delta, which the engine must ignore), then `assistant` and
`result` events. Behaviour comes from the JSON scenario in $FAKE_CLAUDE_SCENARIO:
  {"default": {...}, "rules": [{"match": "<substring of message or system prompt>", ...}, ...]}
with keys text, first_delay, word_delay and mode in {ok, limit, crash, hang, compact, tamper_canonical, misrecord}.
Every start, every received message (with the resumed history) and every finished call is appended as a JSON line to $FAKE_CLAUDE_LOG.
"""
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path


def log(rec):
    path = os.environ.get("FAKE_CLAUDE_LOG")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")


def emit(ev):
    sys.stdout.write(json.dumps(ev) + "\n")
    sys.stdout.flush()


def arg(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def project_dir(cwd):
    home = Path(os.environ["HOME"])
    return home / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(cwd).resolve()))


def text_of(content):
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if b.get("type") == "text")


def main():
    argv = sys.argv[1:]
    cwd = os.getcwd()
    env_keys = ("DISABLE_AUTOUPDATER", "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
                "CLAUDE_CODE_EFFORT_LEVEL", "MAX_THINKING_TOKENS")
    log({"event": "start", "pid": os.getpid(), "argv": argv, "cwd": cwd, "t": time.time(),
         "env": {k: os.environ.get(k) for k in env_keys}})
    raw = sys.stdin.readline()
    if not raw:
        log({"event": "eof", "pid": os.getpid()})
        return 0
    msg = json.loads(raw)
    message = text_of(msg["message"]["content"])
    system = arg(argv, "--system-prompt") or ""
    scen = json.loads(Path(os.environ["FAKE_CLAUDE_SCENARIO"]).read_text())
    beh = dict(scen.get("default", {}))
    for rule in scen.get("rules", []):
        if rule["match"] in message or rule["match"] in system:
            beh.update(rule)
            break
    mode = beh.get("mode", "ok")
    if mode == "crash":
        log({"event": "crash", "pid": os.getpid()})
        return 1

    pdir = project_dir(cwd)
    resume = arg(argv, "--resume")
    history_lines = []
    if resume:
        src = pdir / f"{resume}.jsonl"
        history_lines = [json.loads(x) for x in src.read_text().splitlines() if x.strip()]
        if mode == "tamper_canonical":
            with open(src, "a", encoding="utf-8") as fh:
                fh.write("\n")
    log({"event": "recv", "pid": os.getpid(), "message": message, "system": system, "t": time.time(),
         "history": [[h["type"], text_of(h["message"]["content"])] for h in history_lines]})
    sid = str(uuid.uuid4()) if ("--fork-session" in argv or not resume) else resume
    pdir.mkdir(parents=True, exist_ok=True)
    fork_file = pdir / f"{sid}.jsonl"
    recorded = message if mode != "misrecord" else message + " (changed)"
    with open(fork_file, "w", encoding="utf-8") as fh:
        parent = None
        for h in history_lines:
            h = dict(h, sessionId=sid)
            parent = h.get("uuid")
            fh.write(json.dumps(h) + "\n")
        u = str(uuid.uuid4())
        fh.write(json.dumps({"type": "user", "sessionId": sid, "uuid": u, "parentUuid": parent,
                             "message": {"role": "user", "content": [{"type": "text", "text": recorded}]}}) + "\n")
    emit({"type": "system", "subtype": "init", "session_id": sid, "model": os.environ.get("FAKE_CLAUDE_MODEL") or arg(argv, "--model"),
          "tools": []})
    if mode == "limit":
        emit({"type": "rate_limit_event", "rate_limit_info": {"status": "rejected"}})
        emit({"type": "result", "subtype": "success", "is_error": True, "result": "Claude usage limit reached",
              "session_id": sid})
        log({"event": "limit", "pid": os.getpid(), "message": message, "system": system})
        return 1
    if mode == "compact":
        emit({"type": "system", "subtype": "compact_boundary", "session_id": sid})
    if mode == "hang":
        log({"event": "hang", "pid": os.getpid(), "message": message, "system": system})
        while True:
            time.sleep(1.0)
    time.sleep(float(beh.get("first_delay", 0.02)))
    emit({"type": "stream_event", "event": {"type": "content_block_delta",
                                            "delta": {"type": "thinking_delta", "thinking": "Let me see."}}})
    text = beh.get("text", "Fine. Go on. More words here.")
    words = text.split(" ")
    out = ""
    for i, w in enumerate(words):
        piece = w if i == 0 else " " + w
        out += piece
        emit({"type": "stream_event", "event": {"type": "content_block_delta",
                                                "delta": {"type": "text_delta", "text": piece}}})
        time.sleep(float(beh.get("word_delay", 0.005)))
    emit({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": out}]}})
    with open(fork_file, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"type": "assistant", "sessionId": sid, "uuid": str(uuid.uuid4()),
                             "message": {"role": "assistant", "content": [{"type": "text", "text": out}]}}) + "\n")
    n_in = (len(system.encode()) + len(message.encode()) +
            sum(len(json.dumps(h.get("message", "")).encode()) for h in history_lines)) // 4
    emit({"type": "result", "subtype": "success", "is_error": False, "result": out, "session_id": sid,
          "duration_ms": 100, "usage": {"input_tokens": n_in, "output_tokens": len(words)}})
    log({"event": "done", "pid": os.getpid(), "t": time.time()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
