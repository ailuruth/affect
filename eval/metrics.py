"""Metrics of the battery, on the engine's output and his channel (never a match to a human face).

worst_block_slope  the block-mean copy metric of the sims and spec §5.1 (F1, F22): the slope of the agent's block means
                   on his, worst over 6 block phases and the lags scanned, per window (2 s, 10 s, 1 min).
pooled_slope       the pooled slope over people: block means centred within each person, one least-squares slope.
monotone_drift     a channel's mean drifting monotonically over consecutive blocks by more than a tolerance.
"""
from __future__ import annotations

import numpy as np


def _cum(x):
    return np.vstack([np.zeros((1,) + x.shape[1:]), np.cumsum(x, 0)])


def worst_block_slope(u, y, fs, lags_s=(0.0,), windows=(2.0, 10.0, 60.0), phases: int = 6):
    """(len(windows), n) worst slopes of y's block means on u's (u, y: (T,) or (T, n)); y lags u by each lag."""
    u = np.asarray(u, float)
    y = np.asarray(y, float)
    if u.ndim == 1:
        u, y = u[:, None], y[:, None]
    T, n = u.shape
    cu, cy = _cum(u), _cum(y)
    out = np.full((len(windows), n), np.nan)
    for wi, W in enumerate(windows):
        nb = int(round(W * fs))
        best = np.full(n, -np.inf)
        for lag_s in lags_s:
            lg = int(round(lag_s * fs))
            for ph in range(0, nb, max(1, nb // phases)):
                m = (T - lg - ph) // nb
                if m < 3:
                    continue
                s = ph + nb * np.arange(m + 1)
                xu = (cu[s[1:]] - cu[s[:-1]]) / nb
                xy = (cy[lg + s[1:]] - cy[lg + s[:-1]]) / nb
                xu = xu - xu.mean(0)
                xy = xy - xy.mean(0)
                den = (xu * xu).sum(0)
                sl = np.where(den > 0, (xu * xy).sum(0) / np.where(den > 0, den, 1.0), 0.0)
                best = np.maximum(best, sl)
        out[wi] = np.where(np.isfinite(best), best, np.nan)
    return out


def block_means(x, fs, window_s, lag_s=0.0):
    x = np.asarray(x, float)
    nb = int(round(window_s * fs))
    lg = int(round(lag_s * fs))
    x = x[lg:]
    m = x.shape[0] // nb
    return x[:m * nb].reshape(m, nb).mean(1) if m else np.zeros(0)


def pooled_slope(us, ys, fs, window_s, lag_s=0.0) -> float:
    """Pooled over people: slope of y's block means on u's (y lagged by lag_s), each person centred on its own mean."""
    sxy = sxx = 0.0
    for u, y in zip(us, ys):
        bu = block_means(u, fs, window_s)
        by = block_means(y, fs, window_s, lag_s)
        m = min(bu.size, by.size)
        if m < 3:
            continue
        a, b = bu[:m] - bu[:m].mean(), by[:m] - by[:m].mean()
        sxy += float(a @ b)
        sxx += float(a @ a)
    return sxy / sxx if sxx > 0 else 0.0


def monotone_drift(x, n_blocks: int, tol: float) -> bool:
    """True if the block means of x over n_blocks equal blocks are strictly monotone and move by more than tol."""
    x = np.asarray(x, float)
    m = x.shape[0] // n_blocks
    if m == 0:
        return False
    b = x[:m * n_blocks].reshape(n_blocks, m).mean(1)
    d = np.diff(b)
    return bool((np.all(d > 0) or np.all(d < 0)) and abs(b[-1] - b[0]) > tol)
