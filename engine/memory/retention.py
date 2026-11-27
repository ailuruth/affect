"""The retention job (spec §1.9; Q34 item 6; M2). Runs nightly, before replay.

Window: the operator switch `feature_retention_days` (recommended 30; options 7, or None = until he deletes them).
After the window a session's feature arrays, state snapshots, Ω records **and its transcripts** are deleted. What
remains is only what replay consolidated (learned weights, per-person latches) and, if `keep_slot_snippets` is on, the
transcript lines that episode slots reference as their retrieval snippets (<= 3 lines per slot: INNATE
`store_limits.slot_lines_max`), the only raw text kept past the window.

Before he answers (either switch unanswered) the job **deletes nothing and keeps nothing on his behalf**: it is the
safe choice when the answer is unknown, because a deletion cannot be undone and a keep can be. It reports every
session older than the default window, so the operator sees what waits for his answer; the engine runs no live
session until then (`Store.open_session` refuses), so nothing new accumulates.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from engine.config.innate import ENTRIES
from engine.config.operator import SWITCHES
from engine.memory.store import Store

DAY_S = 86400.0
SLOT_LINES = int(ENTRIES["store_limits"].value["slot_lines_max"])


@dataclass
class RetentionReport:
    answered: bool
    window_days: float | None
    beyond_window: list = field(default_factory=list)      # sessions older than the window (or the default)
    deleted: list = field(default_factory=list)
    deleted_before_replay: list = field(default_factory=list)
    kept_snippet_lines: int = 0
    dropped_snippet_lines: int = 0
    message: str = ""


def reference_snippets(store: Store, slot: str, refs) -> None:
    """Record which transcript lines an episode slot keeps as its retrieval snippet: [(session id, line index)],
    at most 3 per slot (replay writes these when it consolidates a slot)."""
    refs = [[str(s), int(i)] for s, i in refs]
    if len(refs) > SLOT_LINES:
        raise ValueError(f"a slot keeps at most {SLOT_LINES} lines")
    allrefs = store.read_json("slot_refs.json", {})
    allrefs[str(slot)] = refs
    store.write_json("slot_refs.json", allrefs)


def run_retention(store: Store, now_s: float, switches: dict | None = None) -> RetentionReport:
    sw = SWITCHES if switches is None else switches
    days_sw, keep_sw = sw["feature_retention_days"], sw["keep_slot_snippets"]
    answered = days_sw.answered and keep_sw.answered
    days = days_sw.value if answered else SWITCHES["feature_retention_days"].value
    closed = [s for s in store.sessions() if s.manifest.get("t_end") is not None]
    rep = RetentionReport(answered, days if answered else None)
    if days is None:                                        # "until he deletes them"
        rep.message = "retention: kept until the operator deletes them"
        store.append_log("retention_log.jsonl", {"t": float(now_s), "message": rep.message})
        return rep
    cutoff = float(now_s) - float(days) * DAY_S
    old = [s for s in closed if float(s.manifest["t_end"]) < cutoff]
    rep.beyond_window = [s.sid for s in old]
    if not answered:
        rep.message = (f"retention: waiting for the operator (Q34 item 6); nothing deleted; {len(old)} session(s) "
                       f"older than the default {days} days kept: {', '.join(rep.beyond_window) or 'none'}")
        store.append_log("retention_log.jsonl", {"t": float(now_s), "message": rep.message,
                                                 "waiting": rep.beyond_window})
        return rep
    keep_snippets = bool(keep_sw.value)
    refs = store.read_json("slot_refs.json", {})
    kept = store.read_lines("snippets.jsonl")
    old_ids = {s.sid for s in old}
    for s in old:
        if keep_snippets:
            lines = s.transcript()
            for slot, rr in refs.items():
                for sid, i in rr:
                    if sid == s.sid and 0 <= i < len(lines):
                        entry, words = lines[i]
                        kept.append({"slot": slot, "speaker": entry.speaker, "text": entry.text, "t": entry.t,
                                     "identity": s.manifest["identity"]})
                        rep.kept_snippet_lines += 1
        if not s.manifest.get("replayed"):
            rep.deleted_before_replay.append(s.sid)
        store.delete_session(s.sid)
        rep.deleted.append(s.sid)
    if not keep_snippets:
        rep.dropped_snippet_lines = len(kept)
        kept = []
    for slot in list(refs):
        refs[slot] = [r for r in refs[slot] if r[0] not in old_ids]
        if not refs[slot]:
            del refs[slot]
    store.write_lines("snippets.jsonl", kept)
    store.write_json("slot_refs.json", refs)
    rep.message = (f"retention: {days} days; deleted {len(rep.deleted)} session(s); "
                   f"{rep.kept_snippet_lines} slot snippet line(s) kept")
    store.append_log("retention_log.jsonl", {"t": float(now_s), "message": rep.message, "deleted": rep.deleted})
    return rep
