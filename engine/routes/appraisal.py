"""The appraisal display (spec §1.5.2; r5 §2.6, design §2.5-2.7). Zero-DC within and across sessions.

  xi_A = h_20s * x - h_90s * x        band-pass of x = [u; f_loud; f_glare; f_laugh] (36), both low-passes starting
                                      at b_id at session start (so xi_A starts at 0), stepped at the frame clock;
  alpha = A(xi_A, z_T, b, omega)      learned network (36 + 64 + 7 + 4) -> 64 -> 12 (UNTRAINED STUB: alpha = 0);
  Gamma(alpha) = sum_r softmax(W alpha)_r Gamma^(r),  W 12 -> 5 (UNTRAINED STUB: W = 0, so the five bases are
                                      weighted 1/5 each);
  y_A = Gamma(alpha) xi_A             computed at 2 Hz and linearly interpolated to the frame clock (from the
                                      previous tick's value to the current one over the next 0.5 s; causal).
Bases: Gamma^(0) = 0; Gamma^(1) basis_return_LP_CR, diagonal s_A c_k omega_smile_laugh on LP, CR, BU_L, RHY, BRE
(innate, S44); Gamma^(2) basis_orient, HG <- f_loud +0.10 by the reflection rule and EN <- f_loud -0.10 (innate, S44);
Gamma^(3), Gamma^(4) learned (UNTRAINED STUB: zeros), trained nightly by L_A (M8) and projected onto the set:
|Gamma_kk| <= s_A c_k |omega_g|; cross entries in the away orthant only, each <= 0.15, row <= 0.25; the dyad sign
prior on face pairs; the own-display mask (no weight on the BL, LT, LPR, NW, DIM rows); on zero-ceiling rows only
away entries (A3 (ii)). A7 checks every basis; its fail-safe sets Gamma^(3,4) (and Delta) to 0.

Reference: bp(x) = lp(x, 20) - lp(x, 90) and the return diagonal s_A c_k of research/foundations/sims/design-g5/
checks.py H9, regression-tested in tests/test_appraisal.py.
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.invariants.typetrace import TypedState
from engine.routes.cone import (CODES, DERIVED, GROUP_OF, N, N_IN, is_face_pair, is_reflected, pair_sign)

LO_S, HI_S = ENTRIES["appraisal_band_s"].value
CROSS = ENTRIES["appraisal_cross_max"].value
SHAPE = ENTRIES["appraisal_net_shape"].value
N_BASES = SHAPE["bases"]
MASK_ZERO = tuple(CODES.index(c) for c in ENTRIES["own_display_mask"].value["zero"])
RETURN = tuple(CODES.index(c) for c in ENTRIES["appraisal_return_channels"].value)
_OR = ENTRIES["appraisal_orient_basis"].value


class AppraisalNet:
    """alpha = A(xi_A[36], z_T[64], b[7], omega[4]) -> 64 -> 12; selection W 12 -> 5 (UNTRAINED STUB: zeros)."""

    def __init__(self):
        n_in = sum(SHAPE["inputs"])
        self.W1 = np.zeros((n_in, SHAPE["hidden"]))
        self.b1 = np.zeros(SHAPE["hidden"])
        self.W2 = np.zeros((SHAPE["hidden"], SHAPE["out"]))
        self.Wsel = np.zeros((N_BASES, SHAPE["out"]))
        self.learned_bases = np.zeros((2, N, N_IN))
        self.trained = False

    def alpha(self, xi_A, z_T, b, omega):
        x = np.concatenate([np.reshape(xi_A, -1), np.reshape(z_T, -1), np.reshape(b, -1), np.reshape(omega, -1)])
        return np.tanh(x @ self.W1 + self.b1) @ self.W2

    def select(self, alpha):
        z = self.Wsel @ alpha
        z = z - np.max(z)
        e = np.exp(z)
        return e / np.sum(e)


def innate_bases(omega) -> np.ndarray:
    """(3, 33, 36): neutral, basis_return_LP_CR, basis_orient."""
    om = np.asarray(omega, dtype=np.float64)
    B = np.zeros((3, N, N_IN))
    sA, c = TABLE.array("s_A"), TABLE.array("c")
    for k in RETURN:
        B[1, k, k] = sA[k] * c[k] * om[GROUP_OF[k]]
    jl = N + DERIVED.index("f_loud")
    B[2, CODES.index("HG"), jl] = _OR["HG_from_f_loud"]
    B[2, CODES.index("EN"), jl] = _OR["EN_from_f_loud"]
    return B


def is_away(k: int, j: int, v: float, S: np.ndarray) -> bool:
    if is_reflected(k, j):
        return True
    s = S[k, j]
    return s != 0 and np.sign(v) == -s


def violations(B: np.ndarray, omega, S: np.ndarray, learned: bool) -> list:
    """Every way one basis (33, 36) leaves the appraisal set; `learned` adds the own-display mask."""
    out = []
    sA, c = TABLE.array("s_A"), TABLE.array("c")
    om = np.asarray(omega, dtype=np.float64)
    for k in range(N):
        cap = sA[k] * c[k] * (abs(om[GROUP_OF[k]]) if GROUP_OF[k] >= 0 else 0.0)
        if abs(B[k, k]) > cap + 1e-12:
            out.append((k, k, "diagonal above s_A c_k |omega|"))
        row = 0.0
        for j in range(N_IN):
            v = B[k, j]
            if j == k or v == 0.0:
                continue
            if not is_away(k, j, v, S):
                out.append((k, j, "cross entry not in the away orthant"))
            if abs(v) > CROSS["entry"] + 1e-12:
                out.append((k, j, "cross entry above 0.15"))
            row += abs(v)
        if row > CROSS["row"] + 1e-12:
            out.append((k, -1, "cross row above 0.25"))
        if learned and k in MASK_ZERO and np.any(B[k] != 0):
            out.append((k, -1, "own-display mask row"))
    return out


def project_basis(B: np.ndarray, omega, S: np.ndarray) -> np.ndarray:
    """Projection of a learned basis onto its set (after every replay step)."""
    P = np.array(B, dtype=np.float64)
    sA, c = TABLE.array("s_A"), TABLE.array("c")
    om = np.asarray(omega, dtype=np.float64)
    for k in range(N):
        cap = sA[k] * c[k] * (abs(om[GROUP_OF[k]]) if GROUP_OF[k] >= 0 else 0.0)
        P[k, k] = np.clip(P[k, k], -cap, cap)
        off = [j for j in range(N_IN) if j != k]
        for j in off:
            P[k, j] = np.clip(P[k, j], -CROSS["entry"], CROSS["entry"]) if is_away(k, j, P[k, j], S) else 0.0
        rs = sum(abs(P[k, j]) for j in off)
        if rs > CROSS["row"]:
            for j in off:
                P[k, j] *= CROSS["row"] / rs
        if k in MASK_ZERO:
            P[k] = 0.0
    return P


class Appraisal(TypedState):
    def __init__(self, fs: float, net: AppraisalNet, dyad_prior=None, slow_dt: float = 0.5):
        self.fs, self.slow_dt = float(fs), slow_dt
        self.aL, self.aH = 1 - np.exp(-1 / (LO_S * self.fs)), 1 - np.exp(-1 / (HI_S * self.fs))
        self.net = net
        self.S = pair_sign(np.zeros((N, N)) if dyad_prior is None else dyad_prior)
        self.refl = np.zeros((N, N_IN))
        for k in range(N):
            for j in range(N_IN):
                if is_reflected(k, j):
                    self.refl[k, j] = 1.0
        self.xi_A_lo = None
        self.xi_A_hi = None
        self.xi_A = None
        self.y_A_tick = np.zeros(N)
        self.y_A_prev_tick = np.zeros(N)
        self.t_tick = -np.inf
        self.learned_off = False

    def latch(self, omega, b_id) -> None:
        self.omega = np.asarray(omega, dtype=np.float64)
        self.b_id = b_id
        self.bases = np.concatenate([innate_bases(self.omega), self.net.learned_bases * (0.0 if self.learned_off else 1.0)])
        self.xi_A_lo = np.zeros(N_IN) + 0.0 * b_id
        self.xi_A_hi = np.zeros(N_IN) + 0.0 * b_id
        self.xi_A = self.xi_A_lo - self.xi_A_hi

    def disable_learned(self) -> None:
        """A7 fail-safe: learned bases 0 (innate bases only)."""
        self.learned_off = True
        self.bases[3:] = 0.0

    def step(self, t: float, x):
        """Frame at time t: advance the band-pass of x [36]; return the interpolated y_A [33] at this frame."""
        dev = x - self.b_id
        self.xi_A_lo = self.aL * dev + (1 - self.aL) * self.xi_A_lo
        self.xi_A_hi = self.aH * dev + (1 - self.aH) * self.xi_A_hi
        self.xi_A = self.xi_A_lo - self.xi_A_hi
        frac = float(np.clip((t - self.t_tick) / self.slow_dt, 0.0, 1.0)) if np.isfinite(self.t_tick) else 1.0
        return self.y_A_prev_tick + frac * (self.y_A_tick - self.y_A_prev_tick)

    def display(self, w, lateral_trace):
        """Gamma(alpha) xi_A; lateral rows from a non-lateral input opposite his own 20-s lateral trace."""
        Gam = np.tensordot(w, self.bases, axes=1)
        direct = (Gam * (1.0 - self.refl)) @ self.xi_A
        side = -np.sign(lateral_trace)
        return direct + side * ((Gam * self.refl) @ self.xi_A)

    def tick(self, t: float, z_T, b7, lateral_trace, omega=None):
        """2-Hz tick: alpha, the basis weights, and the display value the next 0.5 s interpolate toward."""
        om = self.omega if omega is None else omega
        a = self.net.alpha(self.xi_A, z_T, b7, om)
        w = self.net.select(a)
        self.y_A_prev_tick = self.y_A_tick
        self.y_A_tick = self.display(w, lateral_trace)
        self.t_tick = t
        return w
