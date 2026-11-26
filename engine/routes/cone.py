"""The held cone (spec §1.5.1; r5 §2.5, r6 §2.5, design §2.5): ungated within a session, centred across sessions.

  y_C(t) = sum_m G_m^(id) (xi_m(t) - b_id),   xi_m = h_m * x,   x = [u (33); f_loud; f_glare; f_laugh] (36),
h_m first-order low-passes with tau_m = 20 s, 2 min, 20 min, 3 h (unit DC), reset to b_id at session start. The
state `xi` holds the centred traces xi_m - b_id (so a trace starts at 0), at the frame clock. G_m is latched at
session start and is not a function of any within-session context.

G_m, row by row (r5 §2.5 as changed by design §2.5 (9.1) and spec §1.5.1):
  - diagonal omega_g F_m s_C c_k, F_m = (0, 0.7, 0.2, 0.1), inner brow (0.5, 0.5, 0, 0); omega_g of the row's group;
  - G0 keeps only the threat reflex's entries: HG <- f_glare +0.25 (m 0), +0.05 (m 1), by the reflection rule;
    LP <- f_glare -0.012 (m 1), -0.0035 (m 2) (= F_m s_X c_LP; resized from r5's -0.035, -0.01, which r6's cut of
    s_X(LP) left over budget: review-m4 Part 2); BI <- f_glare +0.006 (m 0, m 1). Every non-reflected G0 cross
    entry is charged at weight 1 whatever the dyad prior says (the worst case over priors, `g0_usage`), so G0 fits
    its sets before and after M3 and the learned entries get only what G0 leaves;
  - learned cross entries (UNTRAINED STUB, zeros until replay writes them), projected after every write onto:
      face pairs (both channels facial action units): the dyad sign prior's sign or 0 (prior: an M3 statistic; the
      stub prior is 0 everywhere, so learned face-pair entries are 0); other pairs: the agent's own within-synergy
      sign (cross-synergy pairs unsigned); charged entries (toward orthant of a signed pair, weight 1; unsigned pair,
      weight 0.3) within sum_j lambda_kj |G_m,kj| <= F_m s_X c_k; away entries |G| <= a_m, row <= r_m;
      lateral rows (YAW, HG) from a non-lateral input are rendered on the side opposite his own 20-s lateral trace
      (away by construction, under the away caps);
  - zero-ceiling rows: no charged entry, diagonal <= 0.
A derived input carries its constituent's sign and face-ness (f_loud as EN, f_glare as BL, f_laugh as BU_L).
A6 (engine/invariants/asserts.py, check_a6) checks the latched G against these sets; on failure the cone falls back
to its last valid latch, or to G0 and the diagonal (learned entries 0).

Reference: the cone diagonal of research/foundations/sims/design-g5/checks.py H9, sum_m F_m s_C c_k lp(u - mean, tau_m),
regression-tested in tests/test_cone.py.
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.invariants.typetrace import TypedState

N = len(TABLE.codes)
N_IN = N + 3
CODES = TABLE.codes
TAU_M = np.array(ENTRIES["cone_trace_tau_s"].value)
F_M = np.array(ENTRIES["cone_trace_shares"].value)
F_BI = np.array(ENTRIES["cone_trace_shares_BI"].value)
AWAY = ENTRIES["cone_away_caps"].value
A_M, R_M = np.array(AWAY["entry"]), np.array(AWAY["row"])
LAMBDA = ENTRIES["cone_cross_budget_weights"].value
LATERAL = tuple(CODES.index(c) for c in ENTRIES["cone_lateral_rows"].value)
LATERAL_ALL = tuple(CODES.index(c) for c in ("YAW", "TILT", "HG"))
FACE = frozenset(CODES.index(c) for c in ENTRIES["face_channels"].value)
_DER = ENTRIES["derived_feature_sign_as"].value
DERIVED = ("f_loud", "f_glare", "f_laugh")
EFF = tuple(range(N)) + tuple(CODES.index(_DER[d]) for d in DERIVED)        # input column -> constituent channel
GROUPS = ("smile_laugh", "brow", "head_gaze", "voice")
GROUP_OF = np.array([GROUPS.index(g) if g in GROUPS else -1 for g in TABLE.groups])


def synergy_sign_table() -> np.ndarray:
    """S_kj from the agent's own signed synergies: s_k s_j when k and j share a synergy and every shared synergy
    agrees; 0 otherwise (cross-synergy pairs unsigned; M8 removed rule J). Diagonal +1."""
    syn = ENTRIES["own_synergies"].value
    S = np.zeros((N, N))
    for k in range(N):
        for j in range(N):
            if k == j:
                S[k, j] = 1.0
                continue
            prods = {m[CODES[k]] * m[CODES[j]] for m in syn.values() if CODES[k] in m and CODES[j] in m}
            S[k, j] = prods.pop() if len(prods) == 1 else 0.0
    return S


SYN_SIGN = synergy_sign_table()


def pair_sign(dyad_prior: np.ndarray) -> np.ndarray:
    """Toward sign of every (row k, input column j) pair, shape (33, 36): the dyad prior on face pairs, the own
    synergy sign elsewhere. dyad_prior is (33, 33) on channels (the M3 sign table; 0 = no sign)."""
    S = np.zeros((N, N_IN))
    for k in range(N):
        for j in range(N_IN):
            je = EFF[j]
            if k == je:
                S[k, j] = 1.0
            elif k in FACE and je in FACE:
                S[k, j] = dyad_prior[k, je]
            else:
                S[k, j] = SYN_SIGN[k, je]
    return S


def is_face_pair(k: int, j: int) -> bool:
    return k in FACE and EFF[j] in FACE and k != EFF[j]


def is_reflected(k: int, j: int) -> bool:
    return k in LATERAL and EFF[j] not in LATERAL_ALL


def shares(m: int) -> np.ndarray:
    F = np.full(N, F_M[m])
    F[CODES.index("BI")] = F_BI[m]
    return F


def diagonal(omega) -> np.ndarray:
    """(4, 33): omega_g F_m s_C c_k."""
    om = np.asarray(omega, dtype=np.float64)
    w = np.where(GROUP_OF >= 0, om[np.maximum(GROUP_OF, 0)], 0.0)
    sC, c = TABLE.array("s_C"), TABLE.array("c")
    return np.stack([w * shares(m) * sC * c for m in range(4)])


def g0_entries() -> np.ndarray:
    """(4, 33, 36): the innate threat-reflex entries (G0), on the f_glare column."""
    G0 = np.zeros((4, N, N_IN))
    jg = N + DERIVED.index("f_glare")
    tr = ENTRIES["g0_glare_traces"].value
    vals = {"LP": ENTRIES["g0_glare_to_LP"].value, "HG": ENTRIES["g0_glare_to_HG"].value,
            "BI": [ENTRIES["g0_glare_to_BI"].value] * 2}
    for code, ms in tr.items():
        for m, v in zip(ms, vals[code]):
            G0[m, CODES.index(code), jg] = v
    return G0


def classify(k: int, j: int, v: float, S: np.ndarray):
    """('diag'|'away'|'charged'|'forbidden', lambda) for an entry of value v at (k, j)."""
    if j == k:
        return "diag", 0.0
    if v == 0.0:
        return "zero", 0.0
    if is_reflected(k, j):
        return "away", 0.0
    s = S[k, j]
    if is_face_pair(k, j):
        return ("charged", LAMBDA["signed_pair"]) if (s != 0 and np.sign(v) == s) else ("forbidden", 0.0)
    if s == 0:
        return "charged", LAMBDA["unmasked_pair"]
    return ("charged", LAMBDA["signed_pair"]) if np.sign(v) == s else ("away", 0.0)


def budgets(m: int):
    """Per row: charged budget F_m s_X c_k, away entry cap a_m, away row cap r_m."""
    return shares(m) * TABLE.array("s_X") * TABLE.array("c"), A_M[m], R_M[m]


def usage(Gm: np.ndarray, m: int, S: np.ndarray):
    """(charged, away) totals per row of one trace's off-diagonal entries, and the forbidden entries."""
    ch, aw, bad = np.zeros(N), np.zeros(N), []
    for k, j in zip(*np.nonzero(Gm)):
        kind, lam = classify(k, j, Gm[k, j], S)
        if kind == "charged":
            ch[k] += lam * abs(Gm[k, j])
        elif kind == "away":
            aw[k] += abs(Gm[k, j])
            if abs(Gm[k, j]) > A_M[m] + 1e-12:
                bad.append((m, k, j, "away entry above a_m"))
        elif kind == "forbidden":
            bad.append((m, k, j, "face pair against the dyad sign prior"))
    return ch, aw, bad


def g0_usage(G0m: np.ndarray, m: int):
    """(charged, away) totals per row of G0's off-diagonal entries: reflected entries are away; every other entry is
    charged at weight 1 (lambda of a signed pair), independently of the dyad prior's sign (exempt from the prior's
    sign, never from the budgets). Returns (charged, away, violations of the away entry cap)."""
    ch, aw, bad = np.zeros(N), np.zeros(N), []
    w = LAMBDA["signed_pair"]
    for k, j in zip(*np.nonzero(G0m)):
        if j == k:
            continue
        if is_reflected(k, j):
            aw[k] += abs(G0m[k, j])
            if abs(G0m[k, j]) > A_M[m] + 1e-12:
                bad.append((m, k, j, "away entry above a_m"))
        else:
            ch[k] += w * abs(G0m[k, j])
    return ch, aw, bad


def project_learned(Lm: np.ndarray, m: int, S: np.ndarray, G0m: np.ndarray) -> np.ndarray:
    """Project one trace's learned cross entries onto the set left after G0's use of the budgets."""
    L = np.array(Lm, dtype=np.float64)
    np.fill_diagonal(L[:, :N], 0.0)
    for k in range(N):
        for j in range(N_IN):
            kind, _ = classify(k, j, L[k, j], S)
            if kind == "forbidden" or (kind == "charged" and TABLE.c[k] == 0.0):
                L[k, j] = 0.0
            elif kind == "away":
                L[k, j] = np.clip(L[k, j], -A_M[m], A_M[m])
    budget, _, rcap = budgets(m)
    ch0, aw0, _ = g0_usage(G0m, m)
    chL, awL, _ = usage(L, m, S)
    for k in range(N):
        left = max(0.0, budget[k] - ch0[k])
        if chL[k] > left:
            for j in range(N_IN):
                if classify(k, j, L[k, j], S)[0] == "charged":
                    L[k, j] *= left / chL[k]
        aleft = max(0.0, rcap - aw0[k])
        if awL[k] > aleft:
            for j in range(N_IN):
                if classify(k, j, L[k, j], S)[0] == "away":
                    L[k, j] *= aleft / awL[k]
    return L


class Cone(TypedState):
    def __init__(self, fs: float, dyad_prior=None):
        self.fs = float(fs)
        self.a = 1 - np.exp(-1 / (TAU_M * self.fs))          # (4,)
        self.one_minus_a = 1 - self.a
        self.dyad_prior = np.zeros((N, N)) if dyad_prior is None else np.asarray(dyad_prior, dtype=np.float64)
        self.S = pair_sign(self.dyad_prior)
        self.learned = np.zeros((4, N, N_IN))               # UNTRAINED STUB: replay writes, then project
        self.G0 = g0_entries()
        self.last_valid = None
        self.xi = None
        self.G = None
        self.b_id = None

    def latch(self, omega, b_id) -> np.ndarray:
        """Session start: G_m from omega, G0 and the projected learned entries; traces reset to b_id."""
        om = np.clip(np.asarray(omega, dtype=np.float64), -1.0, 1.0)
        self.learned = np.stack([project_learned(self.learned[m], m, self.S, self.G0[m]) for m in range(4)])
        G = self.G0 + self.learned
        D = diagonal(om)
        for m in range(4):
            G[m, np.arange(N), np.arange(N)] += D[m]
        self.G = G
        self.omega = om
        self.b_id = b_id
        self.xi = np.zeros((4, N_IN)) + 0.0 * b_id
        self.refl = np.zeros((4, N, N_IN))
        for k in range(N):
            for j in range(N_IN):
                if is_reflected(k, j):
                    self.refl[:, k, j] = 1.0
        return G

    def fallback(self) -> None:
        """A6 fail-safe: the last valid latch, else G0 and the diagonal only (learned entries 0)."""
        if self.last_valid is not None:
            self.G = self.last_valid.copy()
        else:
            self.learned = np.zeros_like(self.learned)
            G = self.G0.copy()
            D = diagonal(self.omega)
            for m in range(4):
                G[m, np.arange(N), np.arange(N)] += D[m]
            self.G = G

    def step(self, x):
        """One frame: x [36] = [u; f_loud; f_glare; f_laugh]. Returns y_C [33]."""
        dev = x - self.b_id
        self.xi = self.a[:, None] * dev[None, :] + self.one_minus_a[:, None] * self.xi
        direct = self.G * (1.0 - self.refl)
        y = np.zeros(N) + 0.0 * self.xi[0, 0]
        for m in range(4):
            y = y + direct[m] @ self.xi[m]
        side = -np.sign(self.xi[0, :N])                     # opposite his own 20-s lateral trace
        r = np.zeros(N)
        for m in range(4):
            r = r + (self.G[m] * self.refl[m]) @ self.xi[m]
        return y + side * r
