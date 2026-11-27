"""Synthetic stand-ins for the dry run: constructed partners that exercise the harness code paths. They are never
evidence about the engine's behaviour or about people (spec §5 "Constructed partners ... are not evidence"); every
run on them is marked `synthetic` and kept out of research/build/results/ (eval/results.py).

The face streams follow the recipe of research/foundations/sims/design-g9 (piecewise-constant level blocks with
exponential lengths, bursts at a level-dependent rate, a 0.5-s low-pass, small noise), written afresh. Words are
placeholder strings at fixed spacings; the agent's heard words are placeholder `OwnHeard` turns.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter

from engine.config.channels import TABLE
from eval.drive import PartnerSession

N = len(TABLE.codes)
SIGNED = np.array([s == "signed" for s in TABLE.signs])


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs))
    return lfilter([a], [1, -(1 - a)], x, axis=0)


def _blocks(T, mean_len_s, fs, r):
    x = np.zeros(T)
    t = 0
    while t < T:
        n = int(r.exponential(mean_len_s * fs)) + 10
        x[t:t + n] = r.uniform()
        t += n
    return x


def _bursts(rate_per_min, T, fs, r, dur=2.5):
    z = np.zeros(T)
    t = 0
    while t < T:
        q = max(rate_per_min[min(t, T - 1)], 1e-3) / 60
        t += int(r.exponential(1 / q) * fs) + 1
        if t >= T:
            break
        n = max(1, int(np.exp(np.log(dur) + .4 * r.normal()) * fs))
        z[t:t + n] = 1
        t += n
    return z


def channel(T, fs, r, mean_len_s=30.0):
    m = _blocks(T, mean_len_s, fs, r)
    b = _bursts(0.5 + 3 * m, T, fs, r)
    return np.clip(.15 + .25 * m + .35 * lp(b, 0.5, fs) + .02 * r.normal(size=T), 0, 1)


def face(seconds: float, fs: float, seed: int, mean_len_s: float = 30.0) -> np.ndarray:
    r = np.random.default_rng(seed)
    T = int(round(seconds * fs))
    U = np.zeros((T, N))
    for k in range(N):
        u = channel(T, fs, r, mean_len_s)
        U[:, k] = u - 0.3 if SIGNED[k] else u
    return U


def partner(seconds: float, fs: float = 10.0, seed: int = 0, words_every_s: float = 7.0, own_every_s: float = 11.0,
            day: float = 0.0, pid: str | None = None, U=None) -> PartnerSession:
    """One synthetic partner session: his 33 channels, placeholder words every `words_every_s` and placeholder agent
    turns every `own_every_s` (0 = none)."""
    U = face(seconds, fs, seed) if U is None else np.asarray(U, float)
    utt = tuple((float(t), f"placeholder words {i}") for i, t in
                enumerate(np.arange(3.0, seconds, words_every_s))) if words_every_s else ()
    own = tuple((float(t), ("a", "placeholder", "reply")) for t in
                np.arange(9.0, seconds, own_every_s)) if own_every_s else ()
    return PartnerSession(U=U, fs=fs, utterances=utt, own_heard=own, pid=pid or f"synthetic-{seed}", day=day)


def learned(seed: int = 0):
    """Learned parts with small random weights (engine.routes.learned_t.randomise_for_trace), so that every learned
    path carries a nonzero value for the harness to lesion or steer. Stand-in weights: never fitted, never evidence."""
    from engine.routes.learned_t import Learned, randomise_for_trace
    return randomise_for_trace(Learned(), seed)
