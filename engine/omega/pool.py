"""The warm pool of Claude Code forks, streaming, interruption, the scoring deadline, the daily cap and the fallbacks
(spec §1.8; §2.1: asyncio, <= 4 Claude Code processes).

Turn cycle.
1. When a reply completes (`_commit`), the engine writes the canonical session file (the window, engine-written),
   deletes every other session file of its project directory (the forks of the last turn), and spawns `size` CLI
   processes with `--resume <canonical> --fork-session`, idle on stdin (warm).
2. `turn(new, ...)` at p_end >= theta_end: the A11 byte check of the canonical file; the daily cap grants n <= size
   calls; each warm fork i receives his message (+ <= 3 snippets) and its fork line i. Each streams; only text deltas
   count (thinking deltas are ignored).
3. A draft is scored (`scorer`, from the `slow` process) when its first sentence ends. Drafts with a first sentence
   by 0.5 s after the first draft's first sentence, or 3.0 s after his turn end, whichever is first, are compared;
   if none has one by 3.0 s the first to arrive is the only one compared. The best score wins (ties: earliest).
4. Losers are killed (SIGKILL to the process group, not drained) and replaced in the background, never more than
   `claude_max_processes` (4) at once. The winner streams on to the tts process (`on_text`) and is interrupted at
   the end of its second sentence or at 60 words (INNATE `draft_cut`).
5. The winner's text, cut, without its line, becomes a `ChosenReply`; his message and the reply are appended to the
   canonical transcript (step 1 again). `ChosenReply` goes to `tts` and the transcript only: the state hears the
   agent only through `OwnHeard`, made at playback, and the five ports (F19).

Fallbacks. (1) `line_in_system`: each fork carries its line in its own system prompt (week-0 `resume` check).
(2) A rate- or usage-limit signal, or p90 first-sentence latency > 3.0 s over 20 turns, shrinks the pool 3 -> 2; a
second signal within 30 min -> 1; after 30 min clear it grows back by one; a signal at size 1 makes the agent silent
until the limit resets (the signal's reset time, else 30 min, then one probe turn at size 1). (3) No process answers
(CLI missing, logged out, offline, crash): the agent is silent for the turn. At the daily cap the agent is silent
until the next day. There are no hand-written words anywhere (D88): silence is the only fallback. A11 (a prompt or
the canonical transcript not as built, an attend-to line in a history) stops the route for the rest of the session;
a compaction event makes the turn silent and is logged. Nothing is retried in a way that could add calls.

Telemetry (`duration_ms`, usage, first-sentence latency) goes to `self.log` only; it is never fed to the state.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import signal
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from engine.config.innate import ENTRIES
from engine.omega import isolation, lines as L, scorer as S, transcript as TR
from engine.state.types import Marker, TranscriptText, _chosen_reply, agent_text

_DL = ENTRIES["draft_deadline_s"].value
AFTER_FIRST_S = float(_DL["after_first"])
CAP_AFTER_END_S = float(_DL["cap_after_turn_end"])
_CUT = ENTRIES["draft_cut"].value
CUT_SENTENCES, CUT_WORDS = int(_CUT["sentences"]), int(_CUT["words"])
_RS = ENTRIES["pool_resize"].value
RESIZE_P90_S, RESIZE_TURNS, RESIZE_WINDOW_S = float(_RS["p90_s"]), int(_RS["turns"]), 60.0 * float(_RS["window_min"])
MAX_PROCESSES = isolation.MAX_PROCESSES
_SENT_END = re.compile(r"[.!?]+[\"')\]]*(?=\s)")
_LIMIT_TEXT = re.compile(r"\b(usage|rate)[ -]?limit|limit (reached|exceeded)|\b429\b", re.I)
STREAM_LIMIT = 1 << 22


def cut_point(text: str, final: bool) -> int | None:
    """Index where the draft is interrupted: the end of its CUT_SENTENCES-th sentence or its CUT_WORDS-th word."""
    ends = [m.end() for m in _SENT_END.finditer(text)]
    if final and text.rstrip() and text.rstrip()[-1] in ".!?\"')]" and (not ends or ends[-1] < len(text.rstrip())):
        ends.append(len(text.rstrip()))
    pos = ends[CUT_SENTENCES - 1] if len(ends) >= CUT_SENTENCES else None
    words = list(re.finditer(r"\S+", text))
    if len(words) >= CUT_WORDS:
        w = words[CUT_WORDS - 1].end()
        pos = w if pos is None else min(pos, w)
    return pos


def first_sentence_end(text: str, final: bool) -> int | None:
    m = _SENT_END.search(text)
    if m:
        return m.end()
    if final and text.strip():
        return len(text.rstrip())
    return None


# ------------------------------------------------------------------------------------------------ daily cap
class DailyCap:
    """Calls per day (Q34 item 2), persisted so a restart does not reset the count. One message sent = one call."""

    def __init__(self, path: Path, cap: int, today=None):
        self.path, self.cap = Path(path), int(cap)
        self.today = today or (lambda: date.today().isoformat())

    def _read(self) -> dict:
        try:
            d = json.loads(self.path.read_text())
        except (OSError, ValueError):
            d = {}
        return d if d.get("day") == self.today() else {"day": self.today(), "calls": 0}

    def used(self) -> int:
        return int(self._read()["calls"])

    def take(self, n: int) -> int:
        d = self._read()
        k = max(0, min(int(n), self.cap - int(d["calls"])))
        d["calls"] = int(d["calls"]) + k
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(d))
        os.replace(tmp, self.path)
        return k


# ------------------------------------------------------------------------------------------------ pool size
class PoolSizer:
    """Fallback 2 of spec §1.8: shrink on a limit signal or slow first sentences, grow back after 30 min clear."""

    def __init__(self, size_max: int, now=time.monotonic):
        self.size_max = self.size = int(size_max)
        self.now = now
        self.last_change = None
        self.silent_until = None
        self.lat = deque(maxlen=RESIZE_TURNS)

    def signal(self, resets_at_s: float | None = None) -> None:
        t = self.now()
        if self.size <= 1:
            self.silent_until = resets_at_s if resets_at_s is not None and resets_at_s > t else t + RESIZE_WINDOW_S
        else:
            self.size -= 1
        self.last_change = t

    def record_latency(self, first_s: float) -> None:
        self.lat.append(float(first_s))
        if len(self.lat) == RESIZE_TURNS:
            xs = sorted(self.lat)
            p90 = xs[min(len(xs) - 1, int(0.9 * len(xs)))]
            if p90 > RESIZE_P90_S:
                self.lat.clear()
                if self.size > 1:
                    self.signal()

    def silent(self) -> bool:
        t = self.now()
        if self.silent_until is not None:
            if t < self.silent_until:
                return True
            self.silent_until = None
            self.last_change = t
        return False

    def current(self) -> int:
        t = self.now()
        if self.size < self.size_max and self.last_change is not None and t - self.last_change >= RESIZE_WINDOW_S \
                and self.silent_until is None:
            self.size += 1
            self.last_change = t
        return self.size


# ------------------------------------------------------------------------------------------------ one fork
@dataclass
class Draft:
    index: int
    sent: str = ""
    t_send: float | None = None
    text: str = ""
    t_first: float | None = None
    first: str | None = None
    score: float | None = None
    session_id: str | None = None
    model: str | None = None       # the exact model id the CLI reports in its init event (Fix P, D102)
    usage: dict = field(default_factory=dict)
    duration_ms: float | None = None
    ended: bool = False
    error: str | None = None
    limit: bool = False
    resets_at: float | None = None
    compact: bool = False


class Fork:
    """One Claude Code CLI process, spawned idle (warm) on the canonical session; one message, one draft."""

    def __init__(self, pool: "Pool", line_index: int | None):
        self.pool, self.line_index = pool, line_index
        self.system = pool._system(line_index)
        self.canonical_sid = pool.canonical.sid
        self.proc = None
        self.draft = None
        self.reader = None
        self.first_evt = asyncio.Event()
        self.updated = asyncio.Event()
        self.done_evt = asyncio.Event()

    async def spawn(self) -> bool:
        cfg = self.pool.cfg
        resume = self.canonical_sid if self.pool.canonical.history else None
        try:
            self.proc = await asyncio.create_subprocess_exec(
                *isolation.command(cfg, self.system, resume), cwd=str(cfg.workdir), env=isolation.environment(cfg),
                stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
                start_new_session=True, limit=STREAM_LIMIT)
        except OSError as err:
            self.pool._note("spawn_failed", error=str(err))
            return False
        self.pool._alive.add(self)
        self.pool.max_alive = max(self.pool.max_alive, len(self.pool._alive))
        return True

    def alive(self) -> bool:
        return self.proc is not None and self.proc.returncode is None

    async def send(self, index: int, message: str) -> None:
        self.draft = Draft(index, message, asyncio.get_running_loop().time())
        line = json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": message}]}})
        try:
            self.proc.stdin.write(line.encode("utf-8") + b"\n")
            await self.proc.stdin.drain()
            self.proc.stdin.close()
        except (BrokenPipeError, ConnectionResetError, AttributeError) as err:
            self.draft.error = f"send: {err}"
        self.reader = asyncio.create_task(self._read())

    async def _read(self) -> None:
        d = self.draft
        loop = asyncio.get_running_loop()
        streamed = False
        try:
            while True:
                raw = await self.proc.stdout.readline()
                if not raw:
                    break
                try:
                    ev = json.loads(raw)
                except ValueError:
                    continue
                kind = ev.get("type")
                if kind == "system":
                    if ev.get("subtype") == "init":
                        d.session_id = ev.get("session_id")
                        d.model = ev.get("model")
                    elif ev.get("subtype") == "compact_boundary":
                        d.compact = True
                elif kind == "stream_event":
                    delta = (ev.get("event") or {}).get("delta") or {}
                    if delta.get("type") == "text_delta":
                        streamed = True
                        d.text += delta.get("text", "")
                        self._first(loop, final=False)
                        self.updated.set()
                elif kind == "assistant" and not streamed:
                    msg = ev.get("message") or {}
                    d.text += "".join(b.get("text", "") for b in msg.get("content", []) if b.get("type") == "text")
                    self.updated.set()
                elif kind == "rate_limit_event":
                    info = ev.get("rate_limit_info") or {}
                    if info.get("status") == "rejected":
                        d.limit = True
                        d.resets_at = info.get("resetsAt")
                elif kind == "result":
                    d.usage = ev.get("usage") or {}
                    d.duration_ms = ev.get("duration_ms")
                    if ev.get("is_error"):
                        d.error = str(ev.get("result") or ev.get("subtype") or "error")
                        if _LIMIT_TEXT.search(d.error) or ev.get("api_error_status") == 429:
                            d.limit = True
        except (ValueError, asyncio.LimitOverrunError) as err:
            d.error = f"stream: {err}"
        finally:
            if not d.limit and not d.error:
                self._first(loop, final=True)
            d.ended = True
            self.updated.set()
            self.done_evt.set()
            if self.proc is not None:
                try:
                    await asyncio.wait_for(self.proc.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.kill()

    def _first(self, loop, final: bool) -> None:
        d = self.draft
        if d.t_first is None:
            k = first_sentence_end(d.text, final)
            if k is not None:
                d.t_first, d.first = loop.time(), d.text[:k]
                self.first_evt.set()

    def kill(self) -> None:
        if self.alive():
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                try:
                    self.proc.kill()
                except ProcessLookupError:
                    pass

    async def reap(self) -> None:
        self.kill()
        if self.proc is not None:
            try:
                await asyncio.wait_for(self.proc.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                pass
        if self.reader is not None:
            try:
                await asyncio.wait_for(self.reader, timeout=5.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                self.reader.cancel()
        self.pool._alive.discard(self)


# ------------------------------------------------------------------------------------------------ the pool
@dataclass(frozen=True)
class TurnResult:
    reply: object                  # ChosenReply, or None (the agent is silent)
    reason: str                    # spoken | cut | interrupted | silent:<why>
    fork: int | None = None
    drafts: int = 0
    timings: dict = field(default_factory=dict)


class Pool:
    """The omega process's coupling: one instance per session. Use `await start()`, `await turn(...)` per agent
    turn, `interrupt()` from another task when he takes the floor, and always `await close()`."""

    def __init__(self, cfg: isolation.OmegaConfig, now=None, today=None):
        if not isinstance(cfg, isolation.OmegaConfig):
            raise TypeError("the pool needs an OmegaConfig (made only from the operator's answers)")
        self.cfg = cfg
        self.instruction = L.instruction()
        self.lines = L.LINES
        self.canonical = TR.CanonicalFile(cfg.home, cfg.workdir)
        self.cap = DailyCap(cfg.state_dir / "claude_calls.json", cfg.daily_cap, today)
        self.sizer = PoolSizer(cfg.pool_size, now or time.monotonic)
        self.entries = []
        self.warm = []
        self._alive = set()
        self._bg = set()
        self.max_alive = 0
        self.stopped = None
        self.log = []
        self._interrupt = asyncio.Event()
        self.killed_pids = []

    # ---------------------------------------------------------------- the model behind the voice (Fix P, D102)
    def _model_ok(self, model) -> bool:
        """The exact model id that speaks is recorded the first time it is seen. If a later turn reports a different id
        (an alias such as "haiku" resolving to a new model), the change is logged and the agent stays silent until the
        operator sets `claude_model` to the new exact id, so a model change can never alter the agent's words
        unnoticed."""
        if not model:
            return True
        path = self.cfg.state_dir / "claude_model_seen.json"
        try:
            prev = json.loads(path.read_text()).get("model")
        except (OSError, ValueError):
            prev = None
        if prev is None or model == self.cfg.model:
            if prev != model:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"model": model}))
                self._note("model_recorded", model=model, was=prev)
            return True
        if model == prev:
            return True
        self._note("model_changed", was=prev, now=model)
        return False

    # ---------------------------------------------------------------- lifecycle
    def _note(self, what: str, **kw) -> None:
        self.log.append(dict(kw, event=what, t=time.time()))

    def _system(self, i: int | None) -> str:
        return self.instruction if i is None else self.instruction + "\n" + self.lines[i]

    async def start(self, entries=()) -> None:
        """Session start: the session's earlier turns (TranscriptText / Marker), usually none."""
        self.entries = list(entries)
        await self._rewrite_and_warm()

    async def _rewrite_and_warm(self, history=None) -> None:
        await self._kill_all()
        if history is None:
            history = TR.commit_window(self.instruction, self.entries, self.lines, self.cfg.tokens_max,
                                       self.cfg.send_snippets)
        self.canonical.write(history)
        self._sweep()
        await self._warm(self.sizer.current())

    def _sweep(self) -> None:
        """Delete every session file of the engine's project directory except the canonical one (the forks of the
        last turn; spec: at the next idle moment)."""
        for p in self.canonical.dir.glob("*.jsonl"):
            if p != self.canonical.path:
                p.unlink(missing_ok=True)

    async def _warm(self, n: int) -> None:
        self.warm = [f for f in self.warm if f.alive() and f.draft is None and f.canonical_sid == self.canonical.sid]
        n = min(n, len(self.lines))
        while len(self.warm) < n and len(self._alive) < MAX_PROCESSES:
            line = None
            if self.cfg.line_in_system:      # fallback 1: each fork carries its own line in its system prompt
                have = {f.line_index for f in self.warm}
                line = min(i for i in range(len(self.lines)) if i not in have)
            f = Fork(self, line)
            if not await f.spawn():
                break
            self.warm.append(f)

    async def _kill_all(self) -> None:
        for t in list(self._bg):
            t.cancel()
        for t in list(self._bg):
            try:
                await t
            except (asyncio.CancelledError, Exception):
                pass
        self._bg.clear()
        forks = list(self._alive) + [f for f in self.warm if f not in self._alive]
        for f in forks:
            if f.alive() and f.proc is not None:
                self.killed_pids.append(f.proc.pid)
        await asyncio.gather(*(f.reap() for f in forks))
        self.warm = []

    async def close(self) -> None:
        await self._kill_all()
        self._sweep()
        self.canonical.remove()

    def interrupt(self) -> None:
        """He took the floor: every draft and the winner's stream stop now."""
        self._interrupt.set()

    def alive_count(self) -> int:
        return sum(1 for f in self._alive if f.alive())

    # ---------------------------------------------------------------- one turn
    async def _silent(self, new, why: str, commit: bool = True, **timings) -> TurnResult:
        self._note("silent", why=why)
        if commit:
            self.entries.append(new)
            if self.stopped is None:
                await self._rewrite_and_warm()
        return TurnResult(None, "silent:" + why, timings=timings)

    async def _stop(self, why: str) -> None:
        self.stopped = why
        self._note("a11", why=why)
        await self._kill_all()

    async def turn(self, new, snippets=(), t_turn_end: float | None = None, scorer=S.untrained,
                   on_text=None) -> TurnResult:
        """One agent turn for his message (TranscriptText) or an observable marker (Marker)."""
        if not isinstance(new, (TranscriptText, Marker)) or (isinstance(new, TranscriptText) and new.speaker != "his"):
            raise TypeError("a turn answers his TranscriptText or a Marker")
        loop = asyncio.get_running_loop()
        t_end = loop.time() if t_turn_end is None else float(t_turn_end)
        self._interrupt.clear()
        if self.stopped is not None:
            return TurnResult(None, "silent:route_stopped")
        if self.sizer.silent():
            return await self._silent(new, "limit")
        try:
            self.canonical.verify()
        except TR.IntegrityError as err:
            await self._stop(str(err))
            return TurnResult(None, "silent:a11")
        snippets = tuple(snippets) if self.cfg.send_snippets else ()
        try:
            tp = TR.build_turn(self.instruction, self.entries, new, snippets, self.lines, self.cfg.tokens_max,
                               self.cfg.line_in_system, history=self.canonical.history)
        except TR.WindowTooShort:
            tp = TR.build_turn(self.instruction, self.entries, new, snippets, self.lines, self.cfg.tokens_max,
                               self.cfg.line_in_system)
            await self._kill_all()
            self.canonical.write(tp.history)
            self._sweep()
            self._note("window_rebuilt", dropped=tp.dropped_turns)
        n = min(self.sizer.current(), len(self.lines))
        if self.cap.used() >= self.cap.cap:
            return await self._silent(new, "cap")
        await self._warm(n)
        avail = sorted(self.warm, key=lambda f: -1 if f.line_index is None else f.line_index)[:n]
        if not avail:
            return await self._silent(new, "no_process")
        n = self.cap.take(len(avail))           # one message sent = one call; spawning is not a call
        if n == 0:
            return await self._silent(new, "cap")
        forks = avail[:n]
        self.warm = [f for f in self.warm if f not in forks]
        for i, f in enumerate(forks):
            li = i if f.line_index is None else f.line_index
            await f.send(li, tp.messages[li])
        try:
            return await self._run(new, tp, forks, t_end, scorer, on_text)
        finally:
            for f in forks:
                if f.alive():
                    self.killed_pids.append(f.proc.pid)
                await f.reap()

    async def _wait_any(self, aws, timeout: float | None) -> None:
        """Wait for any awaitable, the interrupt, or the timeout."""
        tasks = [asyncio.ensure_future(a) for a in aws] + [asyncio.ensure_future(self._interrupt.wait())]
        try:
            await asyncio.wait(tasks, timeout=None if timeout is None else max(0.0, timeout),
                               return_when=asyncio.FIRST_COMPLETED)
        finally:
            for t in tasks:
                t.cancel()

    async def _run(self, new, tp, forks, t_end, scorer, on_text) -> TurnResult:
        score_tasks = {}
        try:
            return await self._select_and_stream(new, tp, forks, t_end, scorer, on_text, score_tasks)
        finally:
            for t in score_tasks.values():
                t.cancel()

    async def _select_and_stream(self, new, tp, forks, t_end, scorer, on_text, score_tasks) -> TurnResult:
        loop = asyncio.get_running_loop()

        def start_scores():
            for f in forks:
                if f.draft.first is not None and f not in score_tasks:
                    score_tasks[f] = asyncio.create_task(S.score(scorer, f.draft.first))

        # ---- phase 1: until the deadline
        cap = t_end + CAP_AFTER_END_S
        deadline = cap
        while not self._interrupt.is_set():
            start_scores()
            firsts = [f.draft.t_first for f in forks if f.draft.t_first is not None and f.draft.t_first <= cap]
            if firsts:
                deadline = min(min(firsts) + AFTER_FIRST_S, cap)
            now = loop.time()
            pending = [f for f in forks if f.draft.t_first is None and not f.draft.ended]
            if now >= deadline or not pending:
                break
            await self._wait_any([f.first_evt.wait() for f in pending] + [f.done_evt.wait() for f in pending],
                                 deadline - now)
        start_scores()
        if self._interrupt.is_set():
            return await self._end_interrupted(new, forks, None, "")
        if any(f.draft.compact for f in forks):
            self._note("a11_compaction", forks=[f.draft.index for f in forks if f.draft.compact])
            return await self._silent(new, "compaction")
        limit = [f for f in forks if f.draft.limit]
        if limit:
            self.sizer.signal(next((f.draft.resets_at for f in limit if f.draft.resets_at), None))
        cands = [f for f in forks if f.draft.t_first is not None and f.draft.t_first <= deadline]
        if not cands:
            self.sizer.record_latency(float("inf"))
            self._note("no_draft", errors=[f.draft.error for f in forks])
            why = "limit" if limit else ("deadline" if any(f.draft.t_first or not f.draft.ended for f in forks)
                                         else "failure")
            return await self._silent(new, why)
        scores = await asyncio.gather(*(score_tasks[f] for f in cands))
        for f, s in zip(cands, scores):
            f.draft.score = s
        win = max(cands, key=lambda f: (f.draft.score, -f.draft.t_first))
        t_first_min = min(f.draft.t_first for f in cands)
        self.sizer.record_latency(t_first_min - t_end)
        # ---- losers killed, replaced in the background
        for f in forks:
            if f is not win:
                if f.alive():
                    self.killed_pids.append(f.proc.pid)
                await f.reap()
        self._replace_in_background()
        # ---- the model that would speak must be the recorded one (Fix P, D102)
        if not self._model_ok(win.draft.model):
            return await self._silent(new, "model_changed")
        # ---- A11 on the winner's own session file, before any word goes out
        try:
            self._check_fork(win, final=False)
        except TR.IntegrityError as err:
            await self._stop(str(err))
            return TurnResult(None, "silent:a11", drafts=len(forks))
        # ---- the winner streams on to tts, cut at its second sentence or 60 words
        sent_upto, reason = 0, "spoken"
        while True:
            win.updated.clear()
            d = win.draft
            k = cut_point(d.text, d.ended)
            upto = len(d.text) if k is None else k
            if upto > sent_upto and on_text is not None:
                on_text(d.text[sent_upto:upto])
            sent_upto = max(sent_upto, upto)
            if k is not None:
                if not d.ended:
                    reason = "cut"
                    win.kill()
                break
            if d.ended:
                break
            if self._interrupt.is_set():
                return await self._end_interrupted(new, forks, win, d.text[:sent_upto])
            await self._wait_any([win.updated.wait()], None)
        text = win.draft.text[:sent_upto].strip()
        if win.draft.compact:
            self._note("a11_compaction", fork=win.draft.index)
        await win.reap()
        try:
            self._check_fork(win, final=True)
            self.canonical.verify()
        except TR.IntegrityError as err:
            await self._stop(str(err))
            return TurnResult(None, "silent:a11", drafts=len(forks))
        timings = {"first_s": [None if f.draft.t_first is None else f.draft.t_first - t_end for f in forks],
                   "winner_first_s": win.draft.t_first - t_end}
        self._note("turn", calls=len(forks), winner=win.draft.index, reason=reason, tokens=tp.tokens_total,
                   usage=[f.draft.usage for f in forks], duration_ms=[f.draft.duration_ms for f in forks], **timings)
        if not text:
            return await self._silent(new, "empty")
        reply = _chosen_reply(text, loop.time())
        self.entries += [new, agent_text(reply)]
        await self._rewrite_and_warm()
        return TurnResult(reply, reason, win.draft.index, len(forks), timings)

    async def _end_interrupted(self, new, forks, win, spoken: str) -> TurnResult:
        for f in forks:
            if f.alive():
                self.killed_pids.append(f.proc.pid)
            await f.reap()
        self._note("interrupted", spoken=bool(spoken.strip()))
        if win is not None and spoken.strip():
            # what already went out to tts is part of the conversation: the turn is committed with it
            reply = _chosen_reply(spoken.strip(), asyncio.get_running_loop().time())
            self.entries += [new, agent_text(reply)]
            await self._rewrite_and_warm()
            return TurnResult(reply, "interrupted", win.draft.index, len(forks))
        # nothing went out (a false start): the same canonical window, fresh warm forks; his words come again
        await self._rewrite_and_warm(history=self.canonical.history)
        return TurnResult(None, "interrupted", drafts=len(forks))

    def _check_fork(self, f: Fork, final: bool) -> None:
        sid = f.draft.session_id
        path = self.canonical.dir / f"{sid}.jsonl" if sid else None
        if path is None or not path.exists():
            if final:
                raise TR.IntegrityError("A11: the winning fork's session file was not found (F14 not checkable)")
            return
        TR.check_fork_file(path, self.canonical.history, f.draft.sent)

    def _replace_in_background(self) -> None:
        async def refill():
            await self._warm(self.sizer.current())
        t = asyncio.create_task(refill())
        self._bg.add(t)
        t.add_done_callback(self._bg.discard)

    def stats(self) -> dict:
        turns = [e for e in self.log if e["event"] == "turn"]
        return {"calls_today": self.cap.used(), "turns": len(turns), "max_processes": self.max_alive,
                "tokens_per_call_estimate": [e["tokens"] for e in turns]}
