"""Shared runner of checks 7 and 8: the engine's own factual-and-shadow step (engine/shadow/shadow.py ShadowPair:
fast gear, cone, appraisal, free display, gates, assembly, ledger, A1-A9) in real time at 30 Hz on a scripted
synthetic partner, under the load session. Each frame's time is split into its 2-Hz part (`_slow`, the slow tick)
and the rest (the fast tick). numpy only: no approval is needed.

Until the process split (engine/procs/, M2) the two parts run in one process here; the fast number therefore
excludes the slow part exactly, but shares the interpreter with it (stated in week0.md's note)."""
from __future__ import annotations

import time


def run(seconds: float, fs: float = 30.0):
    """Returns (fast_ms per frame, slow_ms per 2-Hz tick)."""
    import numpy as np
    from engine.routes.learned_t import Learned, randomise_for_trace
    from engine.shadow.shadow import Frame, ShadowPair
    from engine.state.body import Session
    from engine.state.types import Utterance

    class Timed(ShadowPair):
        slow_ms: list = []

        def _slow(self, t, fr):
            t0 = time.perf_counter()
            super()._slow(t, fr)
            self.slow_ms.append(1000.0 * (time.perf_counter() - t0))

    N = 33
    r = np.random.default_rng(3)
    pair = Timed(Session(K=0.6), np.full(N + 3, 0.1), randomise_for_trace(Learned(), 5), fs=fs)
    pair.slow_ms = []
    fast_ms = []
    t_start = time.perf_counter()
    n = 0
    while n / fs < seconds:
        t = n / fs
        u = np.clip(0.1 + 0.05 * np.sin(2 * np.pi * 0.03 * t + np.arange(N)) + 0.02 * r.standard_normal(N), -1, 1)
        if n % int(7 * fs) == int(3 * fs):
            pair.push_utterance(Utterance("him", (), "scripted words for the tick", t, "scripted words for the tick"))
        k = len(pair.slow_ms)
        t0 = time.perf_counter()
        pair.step(Frame.from_u(t, u))
        dt = 1000.0 * (time.perf_counter() - t0)
        fast_ms.append(dt - (pair.slow_ms[-1] if len(pair.slow_ms) > k else 0.0))
        n += 1
        wait = t_start + n / fs - time.perf_counter()
        if wait > 0:
            time.sleep(wait)
    return fast_ms, list(pair.slow_ms)
