"""Echo gate g and own-display gate g_o (spec §1.5.4; design §2.1, §2.4.3; r7 §2.4.1). Learned offline, frozen.

Form (general learning bias S13, innate): a monotone additive model. Per input i a shape function on fixed knots
(7 basis functions: the input itself and six hinges (x - q_j)+ at the knots, which the fit places at the input's
quantiles 0.05 ... 0.80), fitted directions (the sign constraint of each input's coefficients), exp link divided by
m_ref and clipped to [0, 1]. This is `phi` / `fit_gate` of research/foundations/sims/design-g7/checks.py; the
evaluation formula is regression-tested against it (tests/test_gates.py).

Inputs (spec §1.5.4):
  g   (18): V-_his (his 20-s read through the own-body reader, LP CR BU_L RHY BRE masked), D_p(N_L), Lambda_V(his
           words as delivered), V_own, Lambda_V(own words) (P1), D_tau (3 x 4), q_trace. Never his LP, CR, BU_L,
           RHY, BRE, traces included (rule 11').
  g_o (5): D_p(N_L), Lambda_V(his words), V_own, Lambda_V(own words), q_trace. Never any channel of his (rule 13').
g multiplies only y_f on the smile_laugh group, g_o only the agent's own smile_laugh displays.

UNTRAINED STUB: coefficients 0, knots at their default positions, intercept log(context-free constant), m_ref 1.
The context-free constant of an unfitted gate is 1.0 (no attenuation; A2's fail-safe bound g <= 1 still keeps the
echo at or below G_k x his channel). M3 writes the fitted values.
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES
from engine.invariants.typetrace import TypedState

N_BASIS = ENTRIES["gate_basis"].value["count"]
_KR = ENTRIES["gate_basis"].value["knot_range"]
DEFAULT_KNOTS = np.linspace(_KR[0], _KR[1], N_BASIS - 1)
G_INPUTS = ("V_his", "Dp_word", "lam_delivered", "V_own", "lam_own") + tuple(
    f"D_tau_{m}_{j}" for m in range(3) for j in range(4)) + ("q_trace",)
GO_INPUTS = ("Dp_word", "lam_delivered", "V_own", "lam_own", "q_trace")
assert len(G_INPUTS) == 18


def basis(X, knots):
    """phi(x): per input, x and (x - q_j)+ for each knot. X (..., n_in), knots (n_in, n_knots) -> (..., n_in, n_basis)."""
    X = np.asarray(X) if not hasattr(X, "tags") else X
    Xe = X[..., :, None]
    hinge = np.maximum(Xe - knots, 0.0)
    return np.concatenate([Xe, hinge], axis=-1)


class MonotoneAdditive:
    """link(b0 + sum_i sum_j beta_ij phi_j(x_i)); link 'exp' -> clip(exp(.)/m_ref, 0, 1), 'logistic' -> sigmoid."""

    def __init__(self, names, link: str = "exp", context_free: float = 1.0):
        self.names = tuple(names)
        n = len(self.names)
        self.link = link
        self.knots = np.tile(DEFAULT_KNOTS, (n, 1))
        self.beta = np.zeros((n, N_BASIS))
        self.directions = np.zeros(n)          # +1 non-decreasing, -1 non-increasing, 0 free (set by the fit)
        self.context_free = float(context_free)
        if link == "exp":
            self.b0 = float(np.log(context_free)) if context_free > 0 else -np.inf
        else:
            self.b0 = float(np.log(context_free / (1 - context_free))) if 0 < context_free < 1 else (
                -np.inf if context_free <= 0 else np.inf)
        self.m_ref = 1.0
        self.trained = False
        self.disabled = False                  # fail-safe (A2) or the "disabled part" state: the constant, reads nothing

    def __call__(self, x):
        if self.disabled:
            return np.float64(self.context_free)
        z = self.b0 + np.sum(basis(x, self.knots) * self.beta)
        if self.link == "exp":
            return np.clip(np.exp(z) / self.m_ref, 0.0, 1.0)
        return 1.0 / (1.0 + np.exp(-z))

    def directions_hold(self) -> bool:
        """The fitted directions: every coefficient of a signed input has that sign (monotone shape)."""
        d = self.directions[:, None]
        return bool(np.all((d == 0) | (self.beta * d >= 0)))


class Gates:
    """The two gate models (shared, frozen weights) evaluated on a run's inputs."""

    def __init__(self):
        self.g = MonotoneAdditive(G_INPUTS, "exp", 1.0)
        self.g_o = MonotoneAdditive(GO_INPUTS, "exp", 1.0)


class GateInputs(TypedState):
    """F (and own) state feeding the gates: his 20-s masked trace and read, D_tau, the own face trace and V_own.

    trace_read20: first-order 20-s trace of his masked channels (30 Hz). V_his = the reader's V on it (2 Hz).
    D_tau (3, 4): traces at 20 s, 2 min, 10 min of his masked read (V, A, T) and BU_S (2 Hz; held in the shadow).
    own_face_trace: 3-s trace of the agent's own observed face, LP and CR masked; V_own its reader V (2 Hz).
    """
    TAUS = (20.0, 120.0, 600.0)

    def __init__(self, n_read: int, n_own: int, fs: float, slow_dt: float = 0.5):
        self.fs, self.slow_dt = fs, slow_dt
        self.a20 = 1 - np.exp(-1 / (20.0 * fs))
        self.a3 = 1 - np.exp(-1 / (3.0 * fs))
        self.aD = np.array([1 - np.exp(-slow_dt / tau) for tau in self.TAUS])[:, None]
        self.trace_read20 = None
        self.own_face_trace = None
        self.V_his = np.float64(0.0)
        self.V_own = np.float64(0.0)
        self.D_tau = np.zeros((3, 4))
        self.n_read, self.n_own = n_read, n_own

    def fast(self, u_read, own_read):
        if self.trace_read20 is None:
            self.trace_read20 = u_read * 1.0
            self.own_face_trace = own_read * 1.0
        self.trace_read20 = self.trace_read20 + self.a20 * (u_read - self.trace_read20)
        self.own_face_trace = self.own_face_trace + self.a3 * (own_read - self.own_face_trace)

    def slow(self, reader_his, reader_own, u_read, bus_idx: int):
        if self.trace_read20 is None:
            return
        self.V_his = reader_his(self.trace_read20)[0]
        self.V_own = reader_own(self.own_face_trace)[0]
        x = np.concatenate([reader_his(u_read), u_read[bus_idx:bus_idx + 1]])
        self.D_tau = self.D_tau + self.aD * (x[None, :] - self.D_tau)


def g_vector(gi: GateInputs, Dp_word, lam_delivered, lam_own, q_trace, D_tau=None):
    D = gi.D_tau if D_tau is None else D_tau
    return np.concatenate([np.stack([gi.V_his * 1.0, Dp_word * 1.0, lam_delivered * 1.0, gi.V_own * 1.0,
                                     lam_own * 1.0]), np.reshape(D, -1), np.reshape(q_trace * 1.0, 1)])


def go_vector(gi: GateInputs, Dp_word, lam_delivered, lam_own, q_trace):
    return np.stack([Dp_word * 1.0, lam_delivered * 1.0, gi.V_own * 1.0, lam_own * 1.0, q_trace * 1.0])
