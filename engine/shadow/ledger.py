"""The attenuate-only shadow ledger, revision 9.2 (spec §1.6; design §2.13).

Per channel k and frame: r_k = y_k - ybar_k (partner-caused part: factual output minus shadow output). For each of
the 97 (window W, lag L) keys:
  his deviation        pi = ubar_W(t - L) - ubar_C(t - L)   (window EMA of u_k minus its 30-min EMA, per key)
  output deviation     rho = rbar_W(t) - rbar_C(t) of the projected output x2 (per window)
  running sums         S <- max(0, d S) + rho pi,  E <- d E + pi^2,  Q <- d Q + (1 - d) pi^2
  bound                S+ = max(0, S) <= kappa c_k E, kappa = 0.70 (0 on zero-ceiling channels).
A key with |pi| < 0.10 sqrt(Q) imposes nothing; a key over budget (b < 0) holds the channel's partner-caused part
at 0 for the frame. The projected value is clipped between 0 and r_k (never larger, never the other sign).
Rendered y_k = ybar_k + x2.

This is `ledger7` (research/foundations/sims/design-g7/checks.py) with the key set of `ledger9`
(sims/design-g9/ledger_lag120.py) and the 97 keys of `w10` (sims/check-cayley91/ledger_close.py), vectorised over
(channels, keys) with the same floating-point operations in the same order, so that at the same sample rate it is
bit-identical to the reference (tests/test_ledger_regression.py). The key order differs from the reference's
(it lists the 10-s lags 125-300 s last); every per-key quantity is independent and combined only by min, max and
any, so the order does not change a bit.

Budgets are per session: reset() at session start; EMAs of u start at the first frame, as the reference.
History of u is one ring of max-lag + 1 frames shared by all keys (the reference reads u[t - L], u[0] before t = L).
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES

KAPPA = ENTRIES["ledger_kappa"].value
KEYS = tuple((float(w), float(l)) for w, l in ENTRIES["ledger_keys"].value)
FLOOR = ENTRIES["ledger_floor"].value
TAU_BUDGET = ENTRIES["ledger_tau_budget_s"].value
TAU_CENTRE = ENTRIES["ledger_tau_centre_s"].value
PI_EPS = ENTRIES["ledger_pi_eps"].value


class Ledger:
    """Streaming ledger over n channels. `bound` per channel is kappa * c_k (computed as one float product, as the
    reference's `kappa * c`)."""

    def __init__(self, ceilings, fs: float, kappa: float = KAPPA, keys=KEYS, tau_budget: float = TAU_BUDGET,
                 tau_centre: float = TAU_CENTRE, floor: float = FLOOR):
        self.fs = float(fs)
        c = np.asarray(ceilings, dtype=np.float64)
        self.n = c.shape[0]
        self.bound = np.array([kappa * float(ck) for ck in c], dtype=np.float64)
        self.keys = tuple((float(w), float(l)) for w, l in keys)
        self.wins = tuple(sorted({w for w, _ in self.keys}))
        self.floor = float(floor)
        fs = self.fs
        self.dR = np.exp(-1 / (tau_budget * fs))
        self.aC = 1 - np.exp(-1 / (tau_centre * fs))
        aW = {w: 1 - np.exp(-1 / (w * fs)) for w in self.wins}
        self.aW_win = np.array([aW[w] for w in self.wins])
        self.a_key = np.array([aW[w] for w, _ in self.keys])
        self.one_minus_a_key = 1 - self.a_key
        self.win_of_key = np.array([self.wins.index(w) for w, _ in self.keys])
        self.lag_frames = np.array([int(l * fs) for _, l in self.keys])
        self.H = int(self.lag_frames.max()) + 1
        self.reset()

    def reset(self) -> None:
        """Session start: every running sum, EMA and the lag history start afresh."""
        n, K = self.n, len(self.keys)
        self.uW = np.zeros((n, K))
        self.uC = None                      # initialised to the first frame
        self.rW = np.zeros((n, len(self.wins)))
        self.rC = np.zeros(n)
        self.S = np.zeros((n, K))
        self.E = np.full((n, K), 1e-9)
        self.Q = np.full((n, K), 1e-12)
        self.buf = None
        self.ptr = -1
        self.t = 0
        self.hits = np.zeros(n, dtype=np.int64)
        self.grow = np.zeros(n, dtype=np.int64)
        self.flip = np.zeros(n, dtype=np.int64)
        self.last_active = np.zeros((n, K), dtype=bool)
        self.last_hold = np.zeros(n, dtype=bool)

    def step(self, u, r) -> np.ndarray:
        """One frame. u: his channels [n]; r: partner-caused part [n]. Returns x2 [n], the admitted part."""
        u = np.asarray(u, dtype=np.float64)
        x = np.asarray(r, dtype=np.float64)
        if self.buf is None:
            self.buf = np.repeat(u[None, :], self.H, axis=0)
            self.uC = np.repeat(u[:, None], len(self.keys), axis=1)
        self.ptr = (self.ptr + 1) % self.H
        self.buf[self.ptr] = u
        ut = self.buf[(self.ptr - self.lag_frames) % self.H].T          # (n, K): u[t - L], u[0] before L

        a = self.a_key
        self.uW += a * (ut - self.uW)
        self.uC += self.aC * (ut - self.uC)
        pi = self.uW - self.uC
        dR = self.dR
        self.Q = dR * self.Q + (1 - dR) * pi * pi
        base = self.one_minus_a_key * self.rW[:, self.win_of_key] - self.rC[:, None]
        Sm = np.maximum(0.0, dR * self.S)
        b = self.bound[:, None] * (dR * self.E + pi * pi) - Sm

        active = ~(np.abs(pi) < self.floor * np.sqrt(self.Q))
        hold = np.any(active & (b < 0), axis=1)
        cons = active & ~(b < 0)
        up = cons & (pi > PI_EPS)
        dn = cons & (pi < -PI_EPS)
        safe_pi = np.where(up | dn, pi, 1.0)
        lim = (b / safe_pi - base) / a
        hi = np.min(np.where(up, lim, np.inf), axis=1)
        lo = np.max(np.where(dn, lim, -np.inf), axis=1)

        x2 = np.where(lo <= hi, np.minimum(np.maximum(x, lo), hi), 0.0)
        x2 = np.where(hold, 0.0, x2)
        x2 = np.minimum(np.maximum(x2, np.minimum(0.0, x)), np.maximum(0.0, x))

        self.hits += np.abs(x2 - x) > 1e-12
        self.grow += np.abs(x2) > np.abs(x) + 1e-12
        self.flip += x2 * x < -1e-18
        self.rW += self.aW_win * (x2[:, None] - self.rW)
        self.rC += self.aC * (x2 - self.rC)
        self.S = np.maximum(0.0, dR * self.S) + (self.rW[:, self.win_of_key] - self.rC[:, None]) * pi
        self.E = dR * self.E + pi ** 2
        self.last_active, self.last_hold = active, hold
        self.t += 1
        return x2


def run(u: np.ndarray, r: np.ndarray, ceilings, fs: float, **kw):
    """Run a whole session. u, r: (T, n) or (T,). Returns (out, hits/T, grow/T, flip/T) per channel, as ledger7."""
    u = np.asarray(u, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    one = u.ndim == 1
    if one:
        u, r = u[:, None], r[:, None]
    led = Ledger(np.atleast_1d(np.asarray(ceilings, dtype=np.float64)), fs, **kw)
    out = np.empty_like(r)
    for t in range(u.shape[0]):
        out[t] = led.step(u[t], r[t])
    T = u.shape[0]
    res = (out, led.hits / T, led.grow / T, led.flip / T)
    if one:
        res = (out[:, 0], res[1][0], res[2][0], res[3][0])
    return res
