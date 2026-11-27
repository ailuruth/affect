"""The canonical transcript, its window, the per-fork prompt and the A11 prompt-integrity checks (spec §1.8, A11).

What Claude receives, and nothing else: the constant instruction (system prompt), the engine-written canonical
transcript (his normalised utterances and the agent's chosen replies, windowed), observable-marker user turns,
<= 3 retrieved raw snippets, and one fixed fork line. `build_turn` accepts only `TranscriptText`, `Marker` and
`Snippet` objects (engine/state/types.py; made only from recogniser output, the agent's chosen replies, the marker
template and stored transcript entries) plus the fork lines of engine/omega/lines.py; anything else is a TypeError.
No body value, latent value, label or number derived from state can enter: there is no argument through which it
could.

Window (Q34 item 9): the current session's most recent turns, oldest dropped first, so that instruction + window +
snippets + the new message (+ the longest fork line) stay <= context_tokens_max tokens. Tokens are estimated
conservatively from UTF-8 bytes (INNATE `token_estimate`) until the M1 check measures the CLI's own count. Snippets
are bounded at INNATE `context_window.snippet_tokens` each and taken before the window; if his new message alone is
over the budget its oldest words are dropped. The history starts with one of his turns and ends with an agent turn;
his turns after the last agent turn (the agent was silent) are put in front of the new message, consecutive turns
of one speaker are joined with a newline.

Session file: the CLI's `.jsonl` format (the format the M1 `resume` check writes), one user/assistant line per
message, written by the engine and never by the CLI (`--fork-session` writes the fork to its own file). Its SHA-256
is kept; `CanonicalFile.verify` is the A11 byte check. `check_fork_file` is F14 / F17 and the compaction check on a
fork's own session file.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from engine.config.innate import ENTRIES
from engine.omega import lines as L
from engine.state.types import Marker, Snippet, TranscriptText

_BYTES_PER_TOKEN = float(ENTRIES["token_estimate"].value["bytes_per_token"])
_WIN = ENTRIES["context_window"].value
SNIPPETS_MAX = int(_WIN["snippets"])
SNIPPET_TOKENS = int(_WIN["snippet_tokens"])
TOKENS_MAX = int(_WIN["tokens_max"])


class IntegrityError(RuntimeError):
    """A11: a prompt, the canonical transcript or a fork's history is not what the engine built, or compaction."""


def tokens(text: str) -> int:
    return int(math.ceil(len(text.encode("utf-8")) / _BYTES_PER_TOKEN))


def _role(e) -> str:
    if isinstance(e, Marker):
        return "user"
    if isinstance(e, TranscriptText):
        return "user" if e.speaker == "his" else "assistant"
    raise TypeError(f"the prompt builder accepts only TranscriptText, Marker and Snippet, not {type(e).__name__}")


def _merge(entries) -> list:
    """[(role, text)] with consecutive turns of one speaker joined by a newline."""
    out = []
    for e in entries:
        r = _role(e)
        if out and out[-1][0] == r:
            out[-1] = (r, out[-1][1] + "\n" + e.text)
        else:
            out.append((r, e.text))
    return out


def _keep_newest_words(text: str, budget: int) -> str:
    if tokens(text) <= budget:
        return text
    words = text.split()
    while words and tokens(" ".join(words)) > budget:
        words.pop(0)
    return " ".join(words)


def render_snippet(s: Snippet, budget: int = SNIPPET_TOKENS) -> str:
    """Header, the earliest stored lines that fit in `budget` tokens, end line."""
    if not isinstance(s, Snippet):
        raise TypeError("render_snippet reads only a Snippet")
    head, tail = L.SNIPPET_HEADER, L.SNIPPET_END
    body = []
    for e in s.entries:
        who = L.SPEAKER_HIS if _role(e) == "user" else L.SPEAKER_AGENT
        line = f"{who}: {e.text}"
        if tokens("\n".join([head, *body, line, tail])) > budget:
            break
        body.append(line)
    return "\n".join([head, *body, tail]) if body else ""


@dataclass(frozen=True)
class TurnPrompt:
    """What one turn sends: the system prompt, the history (role, text) the forks resume, and one user message per
    fork line. `tokens_total` is the estimate of the largest fork's whole prompt."""
    system: str
    history: tuple
    messages: tuple
    tokens_total: int
    dropped_turns: int
    snippets_sent: int


class WindowTooShort(Exception):
    """His new message does not fit beside the pre-written window: the window is rebuilt for this turn."""


def _check_inputs(entries, new, snippets, fork_lines):
    if not isinstance(new, (TranscriptText, Marker)) or _role(new) != "user":
        raise TypeError("the new message is his TranscriptText or a Marker")
    for line in fork_lines:
        if line not in L.LINES:
            raise TypeError("fork lines come only from engine/omega/lines.py")
    for e in entries:
        _role(e)
    if not all(isinstance(s, Snippet) for s in snippets):
        raise TypeError("snippets must be Snippet objects")


def _split_lead(entries):
    """(entries up to the last agent turn, his turns after it)."""
    cut = max([i for i, e in enumerate(entries) if _role(e) == "assistant"], default=-1)
    return entries[:cut + 1], entries[cut + 1:]


def _fixed_tokens(instruction: str, fork_lines, line_in_system: bool) -> int:
    """System prompt and fork line: the part of every prompt that is not window, snippets or message."""
    return tokens(instruction) + tokens(max(fork_lines, key=tokens)) + 1


def _window(msgs, budget: int) -> tuple:
    kept = []
    for r, t in reversed(msgs):
        if tokens(t) > budget:
            break
        kept.insert(0, (r, t))
        budget -= tokens(t)
    while kept and kept[0][0] != "user":
        kept.pop(0)
    return tuple(kept)


def commit_window(instruction: str, entries, fork_lines=L.LINES, tokens_max: int = TOKENS_MAX,
                  send_snippets: bool = True) -> tuple:
    """The window written to the canonical file when a reply completes, before his next message is known: it keeps
    room for <= 3 snippets (if sent) and INNATE `token_estimate.message_reserve_tokens` for his message."""
    entries = list(entries)
    for e in entries:
        _role(e)
    base, _ = _split_lead(entries)
    reserve = int(ENTRIES["token_estimate"].value["message_reserve_tokens"])
    if send_snippets:
        reserve += SNIPPETS_MAX * (SNIPPET_TOKENS + 1)
    tmax = min(int(tokens_max), TOKENS_MAX)
    return _window(_merge(base), tmax - _fixed_tokens(instruction, fork_lines, False) - reserve)


def build_turn(instruction: str, entries, new, snippets=(), fork_lines=L.LINES, tokens_max: int = TOKENS_MAX,
               line_in_system: bool = False, history=None) -> TurnPrompt:
    """The per-fork messages of one turn. `entries`: the current session's TranscriptText / Marker turns, oldest
    first. `new`: his TranscriptText or a Marker. `snippets`: retrieved Snippet objects, best first; a snippet that
    does not fit is left out. `history`: the window already written to the canonical file (the warm forks resume
    it); WindowTooShort if his message does not fit beside it. Without `history` the window is computed here
    (oldest turns dropped first; his message keeps its newest words if it alone is over the budget)."""
    entries, snippets = list(entries), list(snippets)[:SNIPPETS_MAX]
    _check_inputs(entries, new, snippets, fork_lines)
    tmax = min(int(tokens_max), TOKENS_MAX)
    budget = tmax - _fixed_tokens(instruction, fork_lines, line_in_system)
    base, lead = _split_lead(entries)
    new_text = "\n".join([e.text for e in lead] + [new.text])
    if history is not None:
        history = tuple(tuple(h) for h in history)
        budget -= sum(tokens(t) for _, t in history)
        if tokens(new_text) > budget:
            raise WindowTooShort(f"message {tokens(new_text)} tokens, room {budget}")
    else:
        new_text = _keep_newest_words(new_text, budget)
    budget -= tokens(new_text)
    blocks = []
    for s in snippets:
        b = render_snippet(s)
        if b and tokens(b) + 2 <= budget:
            blocks.append(b)
            budget -= tokens(b) + 2
    msgs = _merge(base)
    kept = history if history is not None else _window(msgs, budget)
    body = "\n\n".join(blocks + [new_text])
    if line_in_system:
        messages = tuple(body for _ in fork_lines)
        systems = [instruction + "\n" + ln for ln in fork_lines]
    else:
        messages = tuple(body + "\n\n" + ln for ln in fork_lines)
        systems = [instruction]
    total = max(tokens(x) for x in systems) + sum(tokens(t) for _, t in kept) + max(tokens(m) for m in messages)
    if total > tmax:
        raise IntegrityError(f"window over budget: {total} > {tmax}")
    return TurnPrompt(instruction, kept, messages, total, max(0, len(msgs) - len(kept)), len(blocks))


def fork_system(tp: TurnPrompt, fork_lines, i: int, line_in_system: bool) -> str:
    return tp.system + "\n" + fork_lines[i] if line_in_system else tp.system


# ------------------------------------------------------------------------------------------------- session files
def project_dir(home: Path, cwd: Path) -> Path:
    """Where the CLI keeps the session files of a working directory."""
    return Path(home) / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(cwd).resolve()))


def session_lines(sid: str, cwd: Path, history) -> bytes:
    ts = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    base = {"sessionId": sid, "cwd": str(Path(cwd).resolve()), "isSidechain": False, "userType": "external",
            "timestamp": ts}
    out, parent = [], None
    for role, text in history:
        u = str(uuid.uuid4())
        if role == "user":
            msg = {"role": "user", "content": text}
        else:
            msg = {"role": "assistant", "type": "message", "model": "engine-written",
                   "content": [{"type": "text", "text": text}]}
        out.append(dict(base, type=role, uuid=u, parentUuid=parent, message=msg))
        parent = u
    return "".join(json.dumps(x, sort_keys=True, ensure_ascii=False) + "\n" for x in out).encode("utf-8")


class CanonicalFile:
    """The engine-written canonical session file of the current turn; the A11 byte check."""

    def __init__(self, home: Path, cwd: Path):
        self.dir = project_dir(home, cwd)
        self.cwd = Path(cwd)
        self.sid = None
        self.path = None
        self.digest = None
        self.history = ()

    def write(self, history) -> str:
        old = self.path
        self.dir.mkdir(parents=True, exist_ok=True)
        sid = str(uuid.uuid4())
        data = session_lines(sid, self.cwd, history) if history else b""
        path = self.dir / f"{sid}.jsonl"
        path.write_bytes(data)
        self.sid, self.path, self.digest, self.history = sid, path, hashlib.sha256(data).hexdigest(), tuple(history)
        if old is not None and old != path:
            old.unlink(missing_ok=True)
        return sid

    def verify(self) -> None:
        if self.path is None:
            raise IntegrityError("A11: no canonical transcript written")
        try:
            data = self.path.read_bytes()
        except OSError as err:
            raise IntegrityError(f"A11: canonical transcript unreadable: {err}") from None
        if hashlib.sha256(data).hexdigest() != self.digest:
            raise IntegrityError("A11: canonical transcript differs from what the engine wrote (F14)")
        if any(ln in t for _, t in self.history for ln in L.LINES):
            raise IntegrityError("A11: an attend-to line in the canonical transcript (F17)")

    def remove(self) -> None:
        if self.path is not None:
            self.path.unlink(missing_ok=True)


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


def read_session(path: Path) -> tuple:
    """(messages [(role, text)], compaction seen) of a CLI session file."""
    msgs, compact = [], False
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(raw)
        except ValueError:
            continue
        if ev.get("type") == "summary" or ev.get("isCompactSummary") or ev.get("subtype") == "compact_boundary":
            compact = True
        if ev.get("type") in ("user", "assistant") and isinstance(ev.get("message"), dict):
            msgs.append((ev["type"], _text_of(ev["message"].get("content", ""))))
    return msgs, compact


def check_fork_file(path: Path, history, sent: str) -> None:
    """F14 / F17 / compaction on a fork's own session file: its history equals the canonical history, its next user
    message equals what was sent, and no fork line appears anywhere before it."""
    msgs, compact = read_session(path)
    if compact:
        raise IntegrityError("A11: compaction in a fork's session file")
    n = len(history)
    if [tuple(m) for m in msgs[:n]] != [tuple(h) for h in history]:
        raise IntegrityError("A11: a fork's history differs from the canonical transcript (F14)")
    if len(msgs) > n:
        if msgs[n] != ("user", sent):
            raise IntegrityError("A11: a fork's recorded message differs from what the engine built (F14)")
    if any(ln in t for _, t in msgs[:n] for ln in L.LINES):
        raise IntegrityError("A11: an attend-to line from an earlier turn in a fork's history (F17)")
