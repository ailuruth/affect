"""Learned T parts (spec §1.5.5, §1.5.6, §1.9): the listener display L_d, the listener-laugh reader qhat, the turn
model (p_end, hazard, theta_end) and omega. Frozen after the offline fit; **T inputs only** (rule 14).

UNTRAINED STUBS with their fixed shapes (`trained = False`); M3 (dyad fit) and M8 (replay, omega) write the weights:
  - ListenerDisplay: ridge W (6 outputs x 140), the outputs BI, BO, LD, LP, CR, RT; features (1, V, A, T, Lambda(3)) of
    his last utterance times a one-hot 2-s time-since bin over 0-20 s, for each of the turn events his_utterance_end
    and session_start (2 x 10 x 7 = 140). TILT, HP, VG, FR, EN rows are never written (no target under D70; A8).
    Untrained: W = 0, so L_d = 0 (its disabled state).
  - QHat: monotone additive logistic model (the gate form) on (Lambda_V of his last two turns, Lambda_V of the agent's
    last turn through port P2, turn order, surprisal). Untrained: its base rate, here 0 (no own laugh).
  - TurnModel: logistic p_end and hazard (~100 weights each); theta_end = 0.5 until the val fit. Untrained: weights 0.
  - Omega: per-group omega in [-1, 1]; prior of a new person; the one person-valence rule (S37), applied per session
    in replay (M8) from inputs replay computes (rho_rel, h_bar).
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.routes.gates import MonotoneAdditive

_LDF = ENTRIES["listener_display_form"].value
LD_OUT = tuple(TABLE.index(c) for c in _LDF["outputs"])
LD_ZERO_ROWS = tuple(TABLE.index(c) for c in ENTRIES["listener_display_zero_rows"].value)
LD_MAX = ENTRIES["listener_display_max"].value
N_FEAT, N_BINS, BIN_S = _LDF["features"], _LDF["bins"], _LDF["bin_s"]
N_EVENTS = len(_LDF["turn_events"])


class ListenerDisplay:
    def __init__(self):
        self.W = np.zeros((len(LD_OUT), N_EVENTS * N_BINS * N_FEAT))
        self.trained = False
        self.disabled = False

    def features(self, reader_vat, lam3, since_his, since_start):
        """phi = concat over turn events of onehot(bin(time since)) (x) (1, V, A, T, Lambda(3))."""
        f = np.concatenate([np.ones(1), np.reshape(reader_vat, 3), np.reshape(lam3, 3)])
        blocks = []
        for since in (since_his, since_start):
            oh = np.zeros(N_BINS)
            if since is not None and 0.0 <= since < N_BINS * BIN_S:
                oh[int(since // BIN_S)] = 1.0
            blocks.append(np.reshape(oh[:, None] * f[None, :], -1))
        return np.concatenate(blocks)

    def __call__(self, phi):
        """L_d in R^33: the 6 outputs at their channels, |L_d,k| <= 0.45, every other row 0."""
        if self.disabled:
            return np.zeros(TABLE_N)
        return _PLACE @ np.clip(self.W @ phi, -LD_MAX, LD_MAX)


TABLE_N = len(TABLE.codes)
_PLACE = np.zeros((TABLE_N, len(LD_OUT)))
for _i, _k in enumerate(LD_OUT):
    _PLACE[_k, _i] = 1.0
assert not set(LD_OUT) & set(LD_ZERO_ROWS)
QHAT_INPUTS = tuple(ENTRIES["qhat_form"].value["inputs"])


class QHat(MonotoneAdditive):
    def __init__(self):
        super().__init__(QHAT_INPUTS, "logistic", 0.0)


class TurnModel:
    """p_end and hazard h(t): logistic models (inputs: silence length, syntactic completion, the question bit of the
    last turn and whose, both people's AU channels). theta_end default before the val fit."""

    N_IN = 4 + 2 * 23

    def __init__(self):
        self.w_end = np.zeros(self.N_IN + 1)
        self.w_haz = np.zeros(self.N_IN + 1)
        self.theta_end = ENTRIES["theta_end_default"].value
        self.trained = False

    def p_end(self, x):
        return 1.0 / (1.0 + np.exp(-(self.w_end[0] + np.asarray(x) @ self.w_end[1:])))

    def hazard(self, x):
        if not self.trained:
            return ENTRIES["hazard_without_fit_per_s"].value
        return 1.0 / (1.0 + np.exp(-(self.w_haz[0] + np.asarray(x) @ self.w_haz[1:])))


OMEGA_PRIOR = np.array(ENTRIES["omega_prior"].value)
_OR = ENTRIES["omega_rule"].value
OMEGA_TAU = ENTRIES["omega_tau_sessions"].value


def omega_target(rho_rel: float, h_bar: float) -> float:
    """s = clip(0.3 + 0.7 min(1, rho_rel/0.6) - 1.3 min(1, h_bar/0.10), -1, 1) (S37)."""
    s = _OR["offset"] + _OR["rel_gain"] * min(1.0, rho_rel / _OR["rel_scale"]) - _OR["h_gain"] * min(1.0, h_bar / _OR["h_scale"])
    return float(np.clip(s, -1.0, 1.0))


def omega_update(omega, s: float):
    """omega_g <- omega_g + (s - omega_g)/60, every group the same target; stays in [-1, 1]."""
    om = np.asarray(omega, dtype=np.float64)
    return np.clip(om + (s - om) / OMEGA_TAU, -1.0, 1.0)


class Learned:
    """Every learned part one engine run reads, frozen within a session; the factual and the shadow run share the
    same object (same weights, spec §1.6). All untrained stubs until M3 / M8 write them."""

    def __init__(self):
        from engine.routes.appraisal import AppraisalNet
        from engine.routes.free_display import DisplayDelta
        from engine.routes.gates import Gates
        from engine.state import readers as R
        n_read = len(READ_IDX)
        self.enc = R.Encoder()
        self.enc_dim = R.E_DIM
        self.lam = R.Lambda()
        self.pop = R.PopReader()
        self.word_v = R.WordToV()
        self.surprisal = R.Surprisal()
        self.progress = R.Progress()
        self.pname = R.PNameMap()
        self.reader_his = R.PiTilde0(n_read)
        self.reader_own = R.PiTilde0(len(OWN_READ_IDX))
        self.gates = Gates()
        self.qhat = QHat()
        self.ld = ListenerDisplay()
        self.turns = TurnModel()
        self.appraisal = AppraisalNet()
        self.delta = DisplayDelta()

    def encode_his(self, u):
        return self.enc.encode(u.text_norm)

    def encode_words(self, words):
        return self.enc.encode([getattr(w, "text", w) for w in words])

    def untrained(self) -> list:
        parts = ("enc", "lam", "pop", "word_v", "surprisal", "progress", "pname", "reader_his", "reader_own", "qhat",
                 "ld", "turns", "appraisal", "delta")
        out = [p for p in parts if not getattr(self, p).trained]
        out += [f"gates.{n}" for n in ("g", "g_o") if not getattr(self.gates, n).trained]
        return out


_UNREAD = set(ENTRIES["echo_gate_unread"].value)
READ_IDX = tuple(i for i, c in enumerate(TABLE.codes) if c not in _UNREAD)
OWN_READ_IDX = tuple(i for i, c in enumerate(TABLE.codes) if c not in ("LP", "CR"))
