"""Small synthetic signals for mechanism tests. Constructed signals; never evidence about behaviour or people.

The generator follows the recipe of research/foundations/sims/design-g9 (piecewise-constant level blocks with
exponential lengths, bursts at a level-dependent rate, a 0.5-s low-pass and small noise), written afresh here.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import lfilter


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs))
    return lfilter([a], [1, -(1 - a)], x, axis=0)


def delay(x, n):
    n = int(n)
    return x.copy() if n <= 0 else np.concatenate([np.full(n, x[0]), x[:-n]])


def level_blocks(T, mean_len_s, fs, r):
    x = np.zeros(T)
    t = 0
    while t < T:
        n = int(r.exponential(mean_len_s * fs)) + 10
        x[t:t + n] = r.uniform()
        t += n
    return x


def bursts(rate_per_min, T, fs, r, dur=2.5):
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


def partner(T, fs, r, mean_len_s=300.0):
    m = level_blocks(T, mean_len_s, fs, r)
    b = bursts(0.5 + 3 * m, T, fs, r)
    return np.clip(.15 + .25 * m + .35 * lp(b, 0.5, fs) + .02 * r.normal(size=T), 0, 1)


def worst_block_slope(u, y, fs, max_lag_s=300.0, lag_step_s=1.0, windows=(2.0, 10.0, 60.0)):
    """The block-mean copy metric of the sims (worst over 6 block phases and lags 0..max_lag of the slope of y's
    block means on u's), for (T, n) arrays at once. Returns (len(windows), n)."""
    u = np.asarray(u, float)
    y = np.asarray(y, float)
    if u.ndim == 1:
        u, y = u[:, None], y[:, None]
    T, n = u.shape
    cu = np.vstack([np.zeros((1, n)), np.cumsum(u, 0)])
    cy = np.vstack([np.zeros((1, n)), np.cumsum(y, 0)])
    out = np.full((len(windows), n), -9.0)
    lags = range(0, int(max_lag_s * fs) + 1, max(1, int(round(lag_step_s * fs))))
    for wi, W in enumerate(windows):
        nb = int(W * fs)
        for lg in lags:
            for ph in range(0, nb, max(1, nb // 6)):
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
                out[wi] = np.maximum(out[wi], sl)
    return out
