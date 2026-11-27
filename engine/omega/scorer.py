"""Draft scoring interface (spec §1.8): score = -E[sum D(b) + D_p(N)] over a 30-s rollout of the world model at 2 Hz
(60 steps, INNATE `draft_rollout`), computed by the `slow` process on a copy of its state.

The omega process holds no state value: it sends a draft's first sentence and receives one number back, which is
used only to choose the winner (<= log2 3 bits per turn). The rollout writes nothing to the state, so a draft's text
cannot change any T, F or K field (F19); only the chosen reply, heard at playback (`OwnHeard`), reaches the state.
The world model is not built yet (M8): `untrained` scores every draft 0, so the earliest first sentence wins.
"""
from __future__ import annotations

import asyncio
import inspect


def untrained(first_sentence: str) -> float:
    return 0.0


async def score(scorer, first_sentence: str) -> float:
    """Call a sync or async scorer; any failure scores -inf (the draft cannot win on an error)."""
    try:
        r = scorer(first_sentence)
        if inspect.isawaitable(r):
            r = await r
        return float(r)
    except asyncio.CancelledError:
        raise
    except Exception:
        return float("-inf")
