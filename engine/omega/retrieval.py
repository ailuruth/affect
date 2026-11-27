"""Retrieval of <= 3 raw transcript snippets of earlier sessions (spec §1.8, §1.9; ALiBi slope 1/(7 days)).

The relevance of each stored candidate is computed by the `slow` process (need-conditioned retrieval, §1.9) and
reaches this function as a number; the number never reaches Claude. What reaches Claude is only the raw stored text of
the chosen snippets (`Snippet`, made from stored `TranscriptText`), and only if the operator's `send_snippets` is on
(Q34 item 1). The state's influence is the choice (about 6 bits), not any text.
"""
from __future__ import annotations

from engine.config.innate import ENTRIES
from engine.state.types import Snippet

SLOPE_PER_DAY = float(ENTRIES["alibi_slope_per_day"].value)
K = int(ENTRIES["context_window"].value["snippets"])
DAY_S = 86400.0


def retrieve(candidates, now_s: float, send_snippets: bool, k: int = K) -> tuple:
    """`candidates`: (Snippet, relevance) pairs. Score = relevance - slope x age in days; the best k, best first."""
    if not send_snippets:
        return ()
    scored = []
    for s, rel in candidates:
        if not isinstance(s, Snippet):
            raise TypeError("retrieval returns only Snippet objects")
        age_days = max(0.0, (float(now_s) - s.t) / DAY_S)
        scored.append((float(rel) - SLOPE_PER_DAY * age_days, -s.t, s))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return tuple(s for _, _, s in scored[:min(k, K)])
