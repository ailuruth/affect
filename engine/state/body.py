"""The innate body and the T state it keeps (spec §1.3; r5 §2.1, §2.8; design §2.1, §2.8). Stepped at 2 Hz.

Loads (named by function; r5 §2.8): E energy; A activation = A_F (F) + A_L (T); V aversive = V_F (F, the threat
reflex) + h_word (T); K contact deficit of the present person; P play deficit; I learning-progress deficit. The drive
D(b) and D_p(N) are engine/state/drives.py; every change of a drive is recorded against one of its declared update
terms and checked by A14 (engine/invariants/asserts.py, DriveAccount) at every tick; on an A14 failure the body is
frozen at its last valid state and learning for the session is off (spec §4.3).

Dynamics (each from the cited row of the spec's state table):
  E      -0.04 %/min awake (restored only in nightly replay, not here).
  A_L    A_L <- max(A_L, 0.5 s_lex^2) at his utterance end; decays with tau 3 min (M6).
  h_word h <- max(h, v_w) at his (addressed) utterance; tau 10 min; no halving (S20).
  K      in session dK/dt = -K f_id e(t)/30 s, e = 1 while his face is present and he spoke in the last 60 s, 0.5
         while present only (S26); 0 for a person never missed (f_id below contact_known_min); between sessions
         rises (1 - K)/36 h (`between_sessions`).
  P      rises (1 - P)/5.05 h; P <- P (1 - 0.15 qhat) at each of his turns (S21).
  I      rises (1 - I)/1 h awake; I <- max(0, I - 0.5 pi_topic) at a partner-initiated utterance (r4 §2.1).
  N_L    per topic slot (V, A, T) from the population word reader; tau 30 min; evidence only raises it (S39; see the
         README for the one simplification).
Events (E1, T parts only): R = drops of D_p(N_L), D_K, D_P, D_I; S = rises of D_p(N_L) and of the h part of D_V;
R' = max(0, R - 3 S) (M5); amplitudes R'/(R' + 0.02), S/(S + 0.02); envelopes (rise 0.4 s, apex to 1.5 s, decay tau
3 s) summed over the recent events and capped at 1. The own laugh: amplitude 0.40 qhat at each of his turns through
the laugh pattern (g_o multiplies it at assembly with the rest of the smile_laugh displays). The sigh: spontaneous
rate 1/3 min x (1 + 2 max(0, 0.5 - E)/0.3), drawn from the agent's own noise (held in the shadow).

Every assignment uses numpy operations so that provenance tags survive in trace mode (engine/invariants/typetrace.py).
"""
from __future__ import annotations

import copy
from dataclasses import dataclass

import numpy as np

from engine.config.innate import ENTRIES
from engine.invariants.asserts import DriveAccount, InvariantError
from engine.invariants.typetrace import TypedState
from engine.routes.learned_t import OMEGA_PRIOR
from engine.state import ports
from engine.state.readers import TOPIC_DIM, topic_code
from engine.state.types import OwnHeard, Utterance

_TERMS = ENTRIES["drive_terms"].value
_DP = ENTRIES["Dp_terms"].value
E_DECAY_PER_S = ENTRIES["energy_decay_per_min"].value / 60.0
AL_GAIN = ENTRIES["activation_lexical_gain"].value
AL_TAU = ENTRIES["activation_lexical_tau_s"].value
H_TAU = ENTRIES["h_word_tau_s"].value
K_TAU_S = ENTRIES["contact_in_session_tau_s"].value
K_RISE_H = ENTRIES["contact_rise_tau_h"].value
K_E = ENTRIES["contact_presence_factor"].value
K_SPOKE_S = ENTRIES["contact_spoke_window_s"].value
K_KNOWN = ENTRIES["contact_known_min"].value
P_TAU_H = ENTRIES["play_rise_tau_h"].value
P_QGAIN = ENTRIES["play_qhat_gain"].value
I_TAU_H = ENTRIES["learn_progress_rise_tau_h"].value
I_GAIN = ENTRIES["learn_progress_gain"].value
NL_TAU = ENTRIES["word_need_tau_s"].value
EV_HALF = ENTRIES["event_amplitude_half"].value
MASK3 = ENTRIES["opponent_mask_factor"].value
ENV = ENTRIES["envelope_shape_s"].value
LAUGH_GAIN = ENTRIES["laugh_drive_gain"].value
LAUGH_MAX = ENTRIES["own_laugh_max"].value
Q_TAU = ENTRIES["q_trace_tau_s"].value
SIGH = ENTRIES["sigh_rate"].value
EVENT_KEEP_S = 40.0          # an envelope is below 1e-4 of its apex after 29 s: older events are dropped (engineering)


def envelope(tau):
    """env(tau): 0 before the event, linear rise over 0.4 s, apex to 1.5 s, then exp(-(tau - 1.5)/3)."""
    tau = np.asarray(tau, dtype=np.float64) if not hasattr(tau, "tags") else tau
    rise = np.clip(tau / ENV["rise"], 0.0, 1.0)
    decay = np.exp(-np.maximum(tau - ENV["apex_end"], 0.0) / ENV["decay_tau"])
    return np.where(tau < 0.0, 0.0, np.where(tau < ENV["rise"], rise, decay))


def envelope_sum(events, t, cap=1.0):
    """Sum of a env(t - t_n) over (t_n, a) records, capped (weights of the latch sequence sum to <= 1 after the cap)."""
    total = np.float64(0.0)
    for tn, a in events:
        total = total + a * envelope(t - tn)
    return np.minimum(cap, total)


def psi(x):
    return x * x


def dp_partner(N):
    """D_p(N) = 0.8 [psi(V - 0.05)+ + 0.7 psi(A - 0.15)+ + 0.5 psi(T - 0.20)+] (numpy form of drives.drive_partner)."""
    s = np.float64(0.0)
    for i, name in enumerate(("V", "A", "T")):
        thr, w = _DP[name]
        s = s + w * psi(np.maximum(0.0, N[i] - thr))
    return _DP["scale"] * s


def d_term(name, x, f_id=1.0):
    setp, band, w = _TERMS[name]
    if name == "K":
        w = w * f_id
    return w * psi(np.maximum(0.0, np.abs(x - setp) - band))


@dataclass
class Session:
    """What a session starts from (T, latched per session): identity familiarity, the body's carried levels, omega."""
    f_id: float = 1.0
    E: float = 0.8
    K: float = 0.0
    P: float = 0.3
    I: float = 0.3
    omega: tuple = tuple(OMEGA_PRIOR)
    t0: float = 0.0


@dataclass
class SlowInputs:
    """T inputs of one 2-Hz tick (the same objects in the factual and the shadow run), plus the F loads sampled from
    the fast loop (V_F) and the agent's own noise draw (held)."""
    t: float
    utterances: tuple = ()          # his Utterance objects ended since the last tick
    own_heard: tuple = ()           # OwnHeard objects (Ω) completed since the last tick
    present: bool = True            # his face present (identity token, T)
    delivered: tuple = ()           # his words delivered so far in the current utterance (T)
    V_F: float = 0.0                # threat-reflex load (F), from the fast loop
    noise: float = 1.0              # the agent's own uniform draw for the sigh (held in the shadow)


class Body(TypedState):
    def __init__(self, session: Session, learned, dt: float = 0.5):
        self.L = learned
        self.dt = dt
        self.f_id = float(session.f_id)
        self.known = self.f_id >= K_KNOWN
        self.E = np.float64(session.E)
        self.A_L = np.float64(0.0)
        self.A_F = np.float64(0.0)      # the spec gives no formula for A_F (r5: "slow loudness and motion"): held at 0
        self.V_F = np.float64(0.0)
        self.h_word = np.float64(0.0)
        self.K = np.float64(session.K if self.known else 0.0)
        self.P_play = np.float64(session.P)
        self.I_lp = np.float64(session.I)
        self.N_L = np.zeros((TOPIC_DIM, 3))
        self.Dp_word = np.float64(0.0)
        self.Dp_face = np.float64(0.0)
        self.q_hat = np.float64(0.0)
        self.q_trace = np.float64(0.0)
        self.omega = np.array(session.omega, dtype=np.float64)
        self.reader_his = np.zeros(3)
        self.e_his_last = np.zeros(self.L.enc_dim)
        self.e_his_prev = np.zeros(self.L.enc_dim)
        self.lam_his_last = np.zeros(3)
        self.lam_his_prev = np.zeros(3)
        self.lam_delivered = np.float64(0.0)
        self.surprisal_last = np.float64(0.0)
        self.lam_own = np.float64(0.0)
        self.e_agent_turn = np.zeros(3)
        self.q_bit_agent = np.float64(0.0)
        self.p_name = np.zeros(33)
        self.t_agent_start = np.float64(-np.inf)
        self.t_agent_end = np.float64(-np.inf)
        self.t_his_end = np.float64(-np.inf)
        self.t_his_spoke = np.float64(-np.inf)
        self.t_session_start = np.float64(session.t0)
        self.present = np.float64(1.0)
        self.last_speaker = np.float64(-1.0)        # 1 agent, 0 him, -1 nobody yet
        self.sigh_t = np.float64(-np.inf)
        self.inhale_t = np.float64(-np.inf)
        self.drop_events = ()
        self.rise_events = ()
        self.progress_events = ()
        self.laugh_events = ()
        self.env_drop = np.float64(0.0)
        self.env_rise = np.float64(0.0)
        self.env_progress = np.float64(0.0)
        self.env_laugh = np.float64(0.0)
        self.L_d = np.zeros(33)
        self.D_T_prev = self._t_terms()
        self.last_own = None
        self.frozen = False
        self.learning_off = False
        self.failures = []
        self.account = DriveAccount(self.b(), self.f_id)

    # ------------------------------------------------------------------------------------------ drives
    def b(self) -> dict:
        return {"E": float(self.E), "A": float(min(1.0, self.A_F + self.A_L)), "V": float(min(1.0, self.V_F + self.h_word)),
                "K": float(self.K), "P": float(self.P_play), "I": float(self.I_lp)}

    def D(self) -> float:
        from engine.state.drives import drive
        return drive(self.b(), self.f_id)

    def _t_terms(self):
        """The T drive terms whose drops and rises are the E1 events: D_p(N_L), D_K, D_P, D_I, and the h part of D_V."""
        return np.stack([self.Dp_word * 1.0, d_term("K", self.K, self.f_id), d_term("P", self.P_play),
                         d_term("I", self.I_lp), d_term("V", self.h_word)])

    def _set(self, name: str, drive: str, term: str, new) -> None:
        """Assign a load and record the change of its drive against the declared term (A14)."""
        before = self.b()[drive]
        setattr(self, name, new)
        self.account.record(drive, term, self.b()[drive] - before)

    def between_sessions(self, hours: float) -> None:
        """K rises (1 - K)/36 h between sessions (only for a known person)."""
        if self.known:
            self.K = 1.0 - (1.0 - self.K) * np.exp(-hours / K_RISE_H)

    # ------------------------------------------------------------------------------------------ his turns
    def _his_utterance(self, u: Utterance) -> None:
        L = self.L
        e = L.encode_his(u)
        slot = L.enc.topic(u.text_norm)
        tc = topic_code(slot, like=e)
        r = L.pop(e, tc)
        self.reader_his = r
        self.e_his_prev, self.e_his_last = self.e_his_last, e
        self.lam_his_prev, self.lam_his_last = self.lam_his_last, L.lam(e)
        s_lex = L.surprisal(e)
        self.surprisal_last = s_lex
        self._set("A_L", "A", "lexical_rise", np.maximum(self.A_L, AL_GAIN * s_lex ** 2))
        self._set("h_word", "V", "h_word_latch", np.maximum(self.h_word, L.word_v(e, tc)))
        onehot = (np.arange(TOPIC_DIM) == slot)[:, None]
        self.N_L = np.where(onehot, np.maximum(self.N_L, r[None, :]), self.N_L)   # (no item writes: tags survive)
        agent_before = self.last_speaker * 0.0 + (self.last_speaker == 1.0)
        x = np.stack([self.lam_his_last[0], self.lam_his_prev[0], self.e_agent_turn[0], agent_before * 1.0, s_lex])
        self.q_hat = L.qhat(x)
        self._set("P_play", "P", "qhat_term", self.P_play * (1.0 - P_QGAIN * self.q_hat))
        self.laugh_events = self.laugh_events + ((np.float64(u.t_end), LAUGH_GAIN * self.q_hat),)
        initiated = 1.0 - agent_before                     # partner-initiated: not a reply to an agent turn
        lowered = np.maximum(0.0, self.I_lp - I_GAIN * L.progress(e))
        self._set("I_lp", "I", "progress_term", self.I_lp + initiated * (lowered - self.I_lp))   # data flow, no branch
        self.t_his_end = np.float64(u.t_end) + 0.0 * e[0]
        self.t_his_spoke = self.t_his_end
        self.q_bit_agent = ports.turn_question_bit(self.last_own, False)
        self.last_speaker = 0.0 * e[0]

    def _own_heard(self, oh: OwnHeard) -> None:
        L = self.L
        self.lam_own = ports.lambda_own(oh, L.enc, L.lam)
        self.e_agent_turn = ports.qhat_agent_turn(oh, L.enc, L.lam)
        self.p_name = ports.p_name(oh, L.enc, L.pname)
        ts, te, _ = ports.own_turn_events(oh)
        self.t_agent_start, self.t_agent_end = ts, te
        self.last_speaker = te * 0.0 + 1.0
        self.last_own = oh
        self.q_bit_agent = ports.turn_question_bit(oh, True)

    def pre_speech_inhale(self, t_event) -> None:
        """The pre-speech inhale (BRE 0.15 for 0.3 s) at a decision to speak; the turn model (M6/M7) calls it with
        the port-P5 time of the agent's own turn event."""
        self.inhale_t = t_event

    # ------------------------------------------------------------------------------------------ the tick
    def tick(self, inp: SlowInputs) -> None:
        if self.frozen:
            return
        snap = self._snapshot()
        try:
            self._tick(inp)
            self.account.check(self.b(), self.D())
        except InvariantError as err:              # A14 fail-safe: body frozen at its last valid state
            self._restore(snap)
            self.frozen = True
            self.learning_off = True
            self.failures.append((inp.t, "A14", str(err)))

    def _tick(self, inp: SlowInputs) -> None:
        L, dt, t = self.L, self.dt, inp.t
        # continuous terms first, then the events of this tick in time order
        self._set("E", "E", "waking_decay", np.maximum(0.0, self.E - E_DECAY_PER_S * dt))
        self._set("A_L", "A", "lexical_decay", self.A_L * np.exp(-dt / AL_TAU))
        self._set("h_word", "V", "h_word_decay", self.h_word * np.exp(-dt / H_TAU))
        self._set("V_F", "V", "reflex_load", np.float64(inp.V_F) * 1.0)
        self.present = np.float64(1.0 if inp.present else 0.0)
        if self.known:
            spoke = (t - self.t_his_spoke) <= K_SPOKE_S
            e = np.where(self.present > 0, np.where(spoke, K_E["face_and_spoke_60s"], K_E["face_only"]), 0.0)
            self._set("K", "K", "in_session_contact", self.K * np.exp(-self.f_id * e * dt / K_TAU_S))
        self._set("P_play", "P", "growth", 1.0 - (1.0 - self.P_play) * np.exp(-dt / (P_TAU_H * 3600.0)))
        self._set("I_lp", "I", "growth", 1.0 - (1.0 - self.I_lp) * np.exp(-dt / (I_TAU_H * 3600.0)))
        self.N_L = self.N_L * np.exp(-dt / NL_TAU)
        items = sorted([(float(u.t_end), 0, u) for u in inp.utterances] + [(float(o.t_end), 1, o) for o in inp.own_heard],
                       key=lambda z: (z[0], z[1]))
        for _, kind, obj in items:
            if kind == 0:
                self._his_utterance(obj)
            else:
                self._own_heard(obj)
        if inp.delivered:
            self.lam_delivered = L.lam(L.encode_words(inp.delivered))[0]
        elif inp.utterances:
            self.lam_delivered = self.lam_his_last[0]
        self.Dp_word = dp_partner(np.max(self.N_L, axis=0))
        # E1 events from the T terms only
        now = self._t_terms()
        drops = np.maximum(0.0, self.D_T_prev - now)
        rises = np.maximum(0.0, now - self.D_T_prev)
        R = drops[0] + drops[1] + drops[2] + drops[3]
        S = rises[0] + rises[4]
        Rm = np.maximum(0.0, R - MASK3 * S)
        a_r = Rm / (Rm + EV_HALF)
        a_d = S / (S + EV_HALF)
        RI = np.maximum(0.0, drops[3] - MASK3 * S)
        a_p = RI / (RI + EV_HALF)
        tt = np.float64(t)
        keep = lambda evs: tuple(ev for ev in evs if t - float(ev[0]) < EVENT_KEEP_S)
        if a_r > 0:
            self.drop_events = self.drop_events + ((tt, a_r),)
        if a_d > 0:
            self.rise_events = self.rise_events + ((tt, a_d),)
        if a_p > 0:
            self.progress_events = self.progress_events + ((tt, a_p),)
        self.drop_events = keep(self.drop_events)
        self.rise_events = keep(self.rise_events)
        self.progress_events = keep(self.progress_events)
        self.laugh_events = keep(self.laugh_events)
        self.D_T_prev = now
        self.env_drop = envelope_sum(self.drop_events, t)
        self.env_rise = envelope_sum(self.rise_events, t)
        self.env_progress = envelope_sum(self.progress_events, t)
        self.env_laugh = envelope_sum(self.laugh_events, t, LAUGH_MAX)
        d = np.exp(-dt / Q_TAU)
        self.q_trace = self.q_trace * d + (1.0 - d) * self.q_hat
        rate = SIGH["per_s"] * (1.0 + SIGH["gain"] * np.maximum(0.0, SIGH["E_ref"] - self.E) / SIGH["E_span"])
        if inp.noise < rate * dt:
            self.sigh_t = tt + 0.0 * self.E
        self.L_d = L.ld(L.ld.features(self.reader_his, self.lam_his_last,
                                      None if not np.isfinite(float(self.t_his_end)) else t - self.t_his_end,
                                      t - self.t_session_start))

    # ------------------------------------------------------------------------------------------ snapshots, A5
    _SKIP = {"L", "account", "failures", "last_own"}

    def _snapshot(self) -> dict:
        return {k: copy.deepcopy(v) for k, v in self.__dict__.items() if k not in self._SKIP}

    def _restore(self, snap: dict) -> None:
        for k, v in snap.items():
            object.__setattr__(self, k, v)

    def t_fields(self) -> dict:
        from engine.state.types import FIELD_TYPES
        return {k: v for k, v in self.__dict__.items() if FIELD_TYPES.get(k) == "T"}
