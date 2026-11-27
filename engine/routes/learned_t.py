"""Learned T parts (spec §1.5.5, §1.5.6, §1.9): the listener display L_d, the listener-laugh reader qhat, the turn
model (p_end, hazard, theta_end) and omega. Frozen after the offline fit; **T inputs only** (rule 14).

UNTRAINED STUBS with their fixed shapes (`trained = False`); M3 (dyad fit) and M8 (replay, omega) write the weights:
  - ListenerDisplay: ridge W (outputs x 140), the outputs BI, BO, LD, LP, CR, RT plus the rows each approved dyad
    stream unlocks (D95; innate `listener_display_stream_rows`: head_pose -> HP, TILT; gaze -> VG; voice_features ->
    FR, EN), never a row of the own-display mask; features (1, V, A, T, Lambda(3)) of his last utterance times a
    one-hot 2-s time-since bin over 0-20 s, for each of the turn events his_utterance_end and session_start
    (2 x 10 x 7 = 140). A row whose stream is not in `dyad_streams` is never written (held at 0; A8).
    Untrained: W = 0, so L_d = 0 (its disabled state).
  - QHat: monotone additive logistic model (the gate form) on (Lambda_V of his last two turns, Lambda_V of the agent's
    last turn through port P2, turn order, surprisal). Untrained: its base rate, here 0 (no own laugh).
  - TurnModel: logistic p_end and hazard (50 to 64 inputs each, plus a bias); inputs from innate `turn_model_form`: the
    base inputs, both people's 23 AU columns, and both people's head (HP, YAW, TILT), gaze (VG, HG) and pitch (F0, FR)
    channels when head_pose, gaze, voice_features are in `dyad_streams` (D95). theta_end = 0.5 until the val fit.
    Untrained: weights 0.
  - Omega: per-group omega in [-1, 1]; prior of a new person; the one omega_rule (S37), applied per session
    in replay (M8) from inputs replay computes (rho_rel, h_bar).
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.config.operator import require
from engine.routes.gates import MonotoneAdditive

_LDF = ENTRIES["listener_display_form"].value
_STREAM_ROWS = ENTRIES["listener_display_stream_rows"].value
_MASK = ENTRIES["own_display_mask"].value
_MASKED = frozenset(_MASK["zero"]) | frozenset(_MASK["own_rise_only"])
LD_MAX = ENTRIES["listener_display_max"].value
N_FEAT, N_BINS, BIN_S = _LDF["features"], _LDF["bins"], _LDF["bin_s"]
N_EVENTS = len(_LDF["turn_events"])
TABLE_N = len(TABLE.codes)


def dyad_streams() -> frozenset:
    """The approved dyad streams (operator switch `dyad_streams`, Q30; D70 widened by D95)."""
    return frozenset(require("dyad_streams")["dyad_streams"])


def listener_display_rows(streams=None) -> tuple:
    """(output rows, zero rows) of L_d as channel indices. Outputs: the fixed outputs of `listener_display_form`, then
    the rows the approved streams unlock, in channel order, none on the own-display mask. Zero rows: every
    stream-unlocked row whose stream is not approved (A8)."""
    s = dyad_streams() if streams is None else frozenset(streams)
    gated = {c for rows in _STREAM_ROWS.values() for c in rows}
    unlocked = {c for st, rows in _STREAM_ROWS.items() if st in s for c in rows}
    codes = list(_LDF["outputs"]) + [c for c in TABLE.codes if c in unlocked and c not in _LDF["outputs"]]
    out = tuple(TABLE.index(c) for c in codes if c not in _MASKED)
    zero = tuple(TABLE.index(c) for c in TABLE.codes if c in gated - unlocked)
    assert not set(out) & set(zero)
    return out, zero


LD_OUT, LD_ZERO_ROWS = listener_display_rows()


class ListenerDisplay:
    def __init__(self, streams=None):
        self.out, self.zero_rows = listener_display_rows(streams)
        self.W = np.zeros((len(self.out), N_EVENTS * N_BINS * N_FEAT))
        self._place = np.zeros((TABLE_N, len(self.out)))
        for i, k in enumerate(self.out):
            self._place[k, i] = 1.0
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
        """L_d in R^33: the outputs at their channels, |L_d,k| <= 0.45, every other row 0."""
        if self.disabled:
            return np.zeros(TABLE_N)
        return self._place @ np.clip(self.W @ phi, -LD_MAX, LD_MAX)


QHAT_INPUTS = tuple(ENTRIES["qhat_form"].value["inputs"])


class QHat(MonotoneAdditive):
    def __init__(self):
        super().__init__(QHAT_INPUTS, "logistic", 0.0)


_TMF = ENTRIES["turn_model_form"].value


def turn_model_inputs(streams=None) -> tuple:
    """Names of the turn model's inputs: the base inputs, both people's AU columns, then both people's channels of
    each approved stream (head_pose, gaze, voice_features: head, gaze and pitch; D95), in the innate order."""
    s = dyad_streams() if streams is None else frozenset(streams)
    names = list(_TMF["base"])
    people = [f"p{i}" for i in range(_TMF["people"])]
    names += [f"{p}_au{j}" for p in people for j in range(_TMF["au_columns"])]
    for st, chans in _TMF["stream_inputs"].items():
        if st in s:
            names += [f"{p}_{c}" for p in people for c in chans]
    return tuple(names)


class TurnModel:
    """p_end and hazard h(t): logistic models (inputs: silence length, syntactic completion, the question bit of the
    last turn and whose, both people's AU channels, and both people's head, gaze and pitch channels when those
    streams are approved; D95). theta_end default before the val fit."""

    def __init__(self, streams=None):
        self.inputs = turn_model_inputs(streams)
        self.N_IN = len(self.inputs)
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
        from engine.memory.retrieval_index import RetrievalQuery
        self.head_id = {}                                   # identity -> R.HeadId (nightly, M8)
        self.adapter = {}                                   # identity -> R.Adapter (nightly, M8)
        self.retrieval_query = RetrievalQuery()

    def encode_his(self, u):
        return self.enc.encode(u.text_norm)

    def encode_words(self, words):
        return self.enc.encode([getattr(w, "text", w) for w in words])

    def untrained(self) -> list:
        parts = ("enc", "lam", "pop", "word_v", "surprisal", "progress", "pname", "reader_his", "reader_own", "qhat",
                 "ld", "turns", "appraisal", "delta", "retrieval_query")
        out = [p for p in parts if not getattr(self, p).trained]
        out += [f"gates.{n}" for n in ("g", "g_o") if not getattr(self.gates, n).trained]
        return out


_UNREAD = set(ENTRIES["echo_gate_unread"].value)
READ_IDX = tuple(i for i, c in enumerate(TABLE.codes) if c not in _UNREAD)
OWN_READ_IDX = tuple(i for i, c in enumerate(TABLE.codes) if c not in ("LP", "CR"))


def randomise_for_trace(L: Learned, seed: int = 0, scale: float = 0.05) -> Learned:
    """Small random weights on every stub, for the type trace only: provenance does not depend on the weights'
    values, but a zero weight can leave a branch untaken (an event of amplitude 0 is not recorded), so the trace runs
    the dataflow with generic nonzero weights. Never used to render."""
    r = np.random.default_rng(seed)
    for part in (L.lam, L.word_v, L.pname, L.reader_his, L.reader_own):
        part.W = scale * r.standard_normal(part.W.shape)
        part.b = np.abs(scale * r.standard_normal(part.b.shape))
    L.pop.W1 = scale * r.standard_normal(L.pop.W1.shape)
    L.pop.W2 = scale * r.standard_normal(L.pop.W2.shape)
    L.pop.b2 = np.full(3, 0.3)
    L.surprisal = lambda e: np.abs(e[0]) * 0.0 + 0.5 + 0.0 * e[1]
    L.progress = lambda e: np.abs(e[1]) + 0.05
    for gm in (L.gates.g, L.gates.g_o, L.qhat):
        gm.beta = scale * r.standard_normal(gm.beta.shape)
        gm.b0 = 0.0 if gm.link == "logistic" else -0.1
    L.ld.W = scale * r.standard_normal(L.ld.W.shape)
    L.appraisal.W1 = scale * r.standard_normal(L.appraisal.W1.shape)
    L.appraisal.W2 = scale * r.standard_normal(L.appraisal.W2.shape)
    L.appraisal.Wsel = r.standard_normal(L.appraisal.Wsel.shape)
    return L
