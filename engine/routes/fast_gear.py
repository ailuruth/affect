"""The frozen per-channel fast gear (spec §1.4; r6 §2.4; S43). Innate reflex and ceiling: nothing is learned here.

Per channel k, at the frame clock:
  x_d,k(t) = u_k(t - 0.45 s)          read from a 0.6-s ring buffer by capture time, linearly interpolated
  E_k      = x_d,k - lp4(x_d,k)        first-order 4-s low-pass (a = 1 - exp(-1/(4 f_s)), state starting at 0)
  y_f,k    = G_k max(E_k, 0)           one-sided channels;   y_f,k = G_k E_k on signed channels;   G_k = 0 on
                                       zero-ceiling channels.
Before the ring holds 0.45 s of history the first sample is read (as the reference's delay pads with x[0]).
No other partner channel, no context and no exogenous input enters (r6 §2.4): dy_f,k/du_j = 0 for j != k.
The echo gate g multiplies the smile_laugh part at assembly; the muscle filter follows at assembly; on the voice
channels the prosody stage (M5) renders y_f only as a zero-mean within-phrase contour (rule 7).

Reference: `fast` in research/foundations/sims/design-g9/ledger_lag120.py (G max(x_d - lp(x_d, 4), 0) with lfilter
and an integer-frame delay); tests/test_fast_gear.py checks the engine against it bit for bit where the delay is a
whole number of frames, and the pointwise lemma 0 <= y_f <= G_k x_d (A1).
"""
from __future__ import annotations

import math

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.invariants.tagged import Tagged, tags_of
from engine.invariants.typetrace import TypedState

DELAY_S = ENTRIES["fast_gear_delay_s"].value
ONSET_TAU_S = ENTRIES["fast_gear_onset_tau_s"].value
RING_S = ENTRIES["ring_buffer_s"].value
_SNAP = 1e-6                      # interpolation weight snapped to 0 or 1 within 1e-6 of a frame (clock rounding)


class FastGear(TypedState):
    def __init__(self, fs: float, G=None, signs=None, delay_s: float = DELAY_S, tau_s: float = ONSET_TAU_S):
        self.fs = float(fs)
        self.G = np.asarray(TABLE.G if G is None else G, dtype=np.float64)
        signs = TABLE.signs if signs is None else signs
        self.one_sided = np.array([s != "signed" for s in signs])
        self.n = self.G.shape[0]
        self.delay_s = float(delay_s)
        self.a = 1 - np.exp(-1 / (tau_s * self.fs))
        self.cap = int(math.ceil(max(RING_S, delay_s) * self.fs)) + 3
        self.reset()

    def reset(self) -> None:
        self.ring_u = None
        self.times = np.full(self.cap, -np.inf)
        self.head = -1
        self.filled = 0
        self.lp4 = np.zeros(self.n)
        self.last_xd = np.zeros(self.n)
        self.last_E = np.zeros(self.n)

    def _push(self, t: float, u) -> None:
        if self.ring_u is None:
            z = np.zeros((self.cap, self.n))
            self.ring_u = Tagged.wrap(z, tags_of(u)) if tags_of(u) else z
        self.head = (self.head + 1) % self.cap
        self.times[self.head] = t
        self.ring_u[self.head] = u
        self.filled = min(self.filled + 1, self.cap)

    def _read(self, tr: float):
        order = [(self.head - i) % self.cap for i in range(self.filled)][::-1]      # oldest .. newest
        times = self.times[order]
        if tr <= times[0]:
            return self.ring_u[order[0]]
        j = int(np.searchsorted(times, tr, side="right")) - 1
        if j >= len(order) - 1:
            return self.ring_u[order[-1]]
        ta, tb = times[j], times[j + 1]
        w = (tr - ta) / (tb - ta)
        if w < _SNAP:
            return self.ring_u[order[j]]
        if w > 1 - _SNAP:
            return self.ring_u[order[j + 1]]
        ua, ub = self.ring_u[order[j]], self.ring_u[order[j + 1]]
        return ua + w * (ub - ua)

    def step(self, t: float, u):
        """One frame at capture time t with his channels u [n]. Returns y_f [n]."""
        self._push(t, u)
        xd = self._read(t - self.delay_s)
        self.lp4 = self.a * xd + (1 - self.a) * self.lp4
        E = xd - self.lp4
        self.last_xd, self.last_E = xd, E
        return np.where(self.one_sided, self.G * np.maximum(E, 0.0), self.G * E)
