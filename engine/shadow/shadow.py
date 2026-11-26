"""The engine run, its shadow, the ledger and the fail-safes (spec §1.6, §4.3; design §2.13, r6 §2.13).

`Run` is one instance of the engine: body and T state (engine/state/body.py), fast gear, cone, appraisal, gates and
free display (engine/routes/). `ShadowPair` runs two of them in lockstep, the factual run on his streams and the
shadow on his latched baseline b_id in place of his expressive stream (u, f_der, his masked read), with the same
learned weights and the same code. Held (copied) in the shadow, and only these: every Ω value (the same OwnHeard
objects reach P1-P5 in both), the rule-6 latches (b_id; b_read and sigma_id enter only the readers), the agent's own
noise draws, g and D_tau (rule 10). Computed in the shadow from its own inputs: its whole T state (body, drives,
loads, q_trace, envelopes, events, L_d, qhat), its F state, g_o and its outputs ybar. His words, turn events,
identity and session are the same objects in both runs, so the shadow's T state equals the factual one exactly when
no F value leaks into T: A5 compares them (digest of every T field at 2 Hz; the T-only free display y_o at 30 Hz)
and checks the held copies.

Per frame: y = assemble(factual), ybar = assemble(shadow), r = y - ybar, x2 = ledger(u, r), rendered = ybar + x2,
then the muscle filter on the face channels. Fail-safes (spec §4.3), for the rest of the session:
  A1, A3, A4  channel k renders ybar_k;          A2  the failing gate -> its context-free constant (reads nothing);
  A5          the whole output -> ybar, the factual T state overwritten by the shadow's, learning off, build failed;
  A6          cone -> last valid latch, else G0 and the diagonal;   A7  learned appraisal bases and Delta -> 0;
  A8          L_d -> 0;    A9  laugh synth gated to 0, neutral prosody;    A14  body frozen, learning off (in Body).
The fast loop never stops; Claude is not told.

`traced_session` drives one run in trace mode for the type trace (engine/invariants/typetrace.py).
"""
from __future__ import annotations

import copy
import dataclasses
from dataclasses import dataclass, field

import numpy as np

from engine.boundary.derived import derived, tag_sets, threat_reflex
from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants import asserts as A
from engine.invariants import typetrace
from engine.invariants.tagged import Tagged
from engine.routes.appraisal import Appraisal
from engine.routes.cone import Cone
from engine.routes.fast_gear import FastGear
from engine.routes.free_display import FreeDisplay
from engine.routes.gates import GateInputs, g_vector, go_vector
from engine.routes.learned_t import OWN_READ_IDX, READ_IDX, Learned
from engine.shadow.assemble import MuscleFilter, assemble, laugh_synth_input
from engine.shadow.ledger import Ledger
from engine.state.body import Body, Session, SlowInputs

N = len(TABLE.codes)
BUS_READ = READ_IDX.index(TABLE.index("BU_S"))
SLOW_DT = 0.5


@dataclass
class Frame:
    """One 30-Hz frame of his streams (F) as the boundary emits them, plus the agent's own observed face."""
    t: float
    u: np.ndarray
    f_der: np.ndarray
    u_read: np.ndarray
    own_face: np.ndarray | None = None

    @classmethod
    def from_u(cls, t: float, u, g_at: float = 0.0, own_face=None) -> "Frame":
        u = np.asarray(u, dtype=np.float64)
        return cls(t, u, derived(u, g_at), u[list(READ_IDX)], own_face)


@dataclass
class Terms:
    y_f: object
    y_C: object
    y_A: object
    y_o: object
    g: object
    g_o: object


class Run:
    """One engine instance (factual or shadow)."""

    def __init__(self, learned: Learned, session: Session, b_id, fs: float = 30.0, dyad_prior=None):
        self.L, self.fs = learned, float(fs)
        self.body = Body(session, learned, SLOW_DT)
        self.fast = FastGear(self.fs)
        self.cone = Cone(self.fs, dyad_prior)
        self.cone.latch(session.omega, b_id)
        self.appr = Appraisal(self.fs, learned.appraisal, dyad_prior, SLOW_DT)
        self.appr.latch(session.omega, b_id)
        self.free = FreeDisplay(learned.delta)
        self.gi = GateInputs(len(READ_IDX), len(OWN_READ_IDX), self.fs, SLOW_DT)
        self.held_g = None
        self.held_D_tau = None
        self.V_F = np.float64(0.0)
        self.last_terms = None

    def fast_step(self, fr: Frame) -> Terms:
        L, b, t = self.L, self.body, fr.t
        y_f = self.fast.step(t, fr.u)
        x = np.concatenate([fr.u, fr.f_der[0:1], fr.f_der[2:4]])
        y_C = self.cone.step(x)
        y_A = self.appr.step(t, x)
        self.V_F = threat_reflex(fr.f_der)
        own = np.zeros(N) if fr.own_face is None else fr.own_face
        self.gi.fast(fr.u_read, own[list(OWN_READ_IDX)])
        if self.held_D_tau is not None:
            self.gi.D_tau = self.held_D_tau
        g = self.held_g if self.held_g is not None else L.gates.g(g_vector(self.gi, b.Dp_word, b.lam_delivered,
                                                                             b.lam_own, b.q_trace))
        g_o = L.gates.g_o(go_vector(self.gi, b.Dp_word, b.lam_delivered, b.lam_own, b.q_trace))
        y_o, _ = self.free.step(b, t)
        self.last_terms = Terms(y_f, y_C, y_A, y_o, g, g_o)
        return self.last_terms

    def slow_tick(self, inp: SlowInputs, u_read) -> None:
        self.body.tick(dataclasses.replace(inp, V_F=float(self.V_F)))
        self.gi.slow(self.L.reader_his, self.L.reader_own, u_read, BUS_READ)
        if self.held_D_tau is not None:
            self.gi.D_tau = self.held_D_tau
        b = self.body
        z_T = np.zeros(64) + 0.0 * b.E                      # mu_T / slots / concepts: not built at M4 (M untrained)
        b7 = np.stack([b.E * 1.0, b.A_L * 1.0, self.V_F + b.h_word, b.K * 1.0, b.P_play * 1.0, b.I_lp * 1.0,
                       b.Dp_word * 1.0])
        self.appr.tick(inp.t, z_T, b7, self.cone.xi[0][:N])


@dataclass
class Safety:
    """The fail-safe state of a session and its failure log (t, assertion, detail)."""
    channel_ybar: np.ndarray = field(default_factory=lambda: np.zeros(N, dtype=bool))
    whole_ybar: bool = False
    laugh_synth_on: bool = True
    neutral_prosody: bool = False
    learning_off: bool = False
    build_failed: bool = False
    log: list = field(default_factory=list)

    def fail(self, t, aid, detail):
        self.log.append((float(t), aid, detail))


@dataclass
class Output:
    rendered: np.ndarray
    face: np.ndarray
    y: np.ndarray
    ybar: np.ndarray
    x2: np.ndarray
    g: float
    g_o: float
    laugh_synth: dict


class ShadowPair:
    def __init__(self, session: Session, b_id, learned: Learned | None = None, fs: float = 30.0, dyad_prior=None,
                 seed: int = 0, b_read=None, sigma_id=None):
        self.L = Learned() if learned is None else learned
        self.fs = float(fs)
        self.b_id = np.asarray(b_id, dtype=np.float64)
        assert self.b_id.shape == (N + 3,)
        self.b_read, self.sigma_id = b_read, sigma_id          # rule-6 latches: readers only (M8 calibration)
        self.session = session
        self.factual = Run(self.L, session, self.b_id, self.fs, dyad_prior)
        self.shadow = Run(self.L, session, self.b_id, self.fs, dyad_prior)
        self.ledger = Ledger(TABLE.c, self.fs)
        self.muscle = MuscleFilter(self.fs)
        self.rng = np.random.default_rng(seed)
        self.safety = Safety()
        self.next_tick = float(session.t0)
        self.pending_utt, self.pending_own, self.delivered, self.present = [], [], (), True
        self.prev_rendered = np.zeros(N)
        self.prev_ybar = np.zeros(N)
        self.t = None
        self._load_checks()

    # ------------------------------------------------------------------------------------------ T inputs
    def push_utterance(self, u) -> None:
        self.pending_utt.append(u)
        self.delivered = ()

    def push_own_heard(self, oh) -> None:
        self.pending_own.append(oh)

    def deliver(self, words) -> None:
        self.delivered = tuple(words)

    def set_present(self, present: bool) -> None:
        self.present = bool(present)

    # ------------------------------------------------------------------------------------------ checks at load
    def _load_checks(self) -> None:
        t = self.session.t0
        for run in (self.factual, self.shadow):
            if A.check_a6(run.cone.G, run.cone.omega, run.cone.S, run.cone.G0):
                self.safety.fail(t, "A6", "cone latch outside its sets")
                run.cone.fallback()
            else:
                run.cone.last_valid = run.cone.G.copy()
        if A.check_a7(self.factual.appr.bases, self.factual.appr.omega, self.factual.appr.S, self.L.delta):
            self.safety.fail(t, "A7", "appraisal basis or Delta outside its set")
            for run in (self.factual, self.shadow):
                run.appr.disable_learned()
            self.L.delta.disabled = True
        if not np.all(np.isfinite(self.L.ld.W)):
            self.safety.fail(t, "A8", "L_d weights")
            self.L.ld.disabled = True

    def baseline_frame(self, t: float, own_face=None) -> Frame:
        b = self.b_id
        u = b[:N]
        f_der = np.stack([b[N], 0.0 * b[N], b[N + 1], b[N + 2], np.sqrt(np.maximum(u[0] * u[1], 0.0))])
        return Frame(t, u, f_der, u[list(READ_IDX)], own_face)

    # ------------------------------------------------------------------------------------------ the 2-Hz tick
    def _slow(self, t: float, fr: Frame) -> None:
        noise = float(self.rng.uniform())
        inp = SlowInputs(t, tuple(self.pending_utt), tuple(self.pending_own), self.present, self.delivered, 0.0, noise)
        self.factual.slow_tick(inp, fr.u_read)
        self.shadow.held_D_tau = copy.deepcopy(self.factual.gi.D_tau)
        self.shadow.slow_tick(inp, self.baseline_frame(t).u_read)
        self.pending_utt, self.pending_own = [], []
        fb, sb = self.factual.body, self.shadow.body
        bad = A.check_a5(fb.t_fields(), sb.t_fields(), {"D_tau": (self.factual.gi.D_tau, self.shadow.gi.D_tau)})
        if bad and not self.safety.whole_ybar:
            self._a5(t, bad)
        for aid, body in (("A14", fb),):
            if body.failures and not self.safety.learning_off:
                self.safety.fail(t, aid, body.failures[-1][2])
                self.safety.learning_off = True
        if not self.L.ld.disabled:
            v = A.check_a8(fb.L_d, self.L.ld.W)
            if v:
                self.safety.fail(t, "A8", v)
                self.L.ld.disabled = True

    def _a5(self, t: float, bad) -> None:
        self.safety.fail(t, "A5", bad)
        self.safety.whole_ybar = True
        self.safety.learning_off = True
        self.safety.build_failed = True
        for k, v in self.shadow.body.t_fields().items():
            object.__setattr__(self.factual.body, k, copy.deepcopy(v))

    # ------------------------------------------------------------------------------------------ the frame
    def step(self, fr: Frame) -> Output:
        t = fr.t
        while t >= self.next_tick - 1e-9:
            self._slow(self.next_tick, fr)
            self.next_tick += SLOW_DT
        S = self.safety
        if fr.own_face is None:
            fr = dataclasses.replace(fr, own_face=self.prev_rendered)
        Tf = self.factual.fast_step(fr)
        self.shadow.held_g = Tf.g
        Ts = self.shadow.fast_step(self.baseline_frame(t, self.prev_ybar))
        y = assemble(Tf.y_f, Tf.y_C, Tf.y_A, Tf.y_o, Tf.g, Tf.g_o)
        ybar = assemble(Ts.y_f, Ts.y_C, Ts.y_A, Ts.y_o, Ts.g, Ts.g_o)

        a1 = A.check_a1(Tf.y_f, self.factual.fast.last_xd, self.factual.fast.last_E, self.factual.fast.G,
                        self.factual.fast.one_sided)
        if a1.any():
            S.fail(t, "A1", [TABLE.codes[k] for k in np.nonzero(a1 & ~S.channel_ybar)[0]])
            S.channel_ybar |= a1
        for name in A.check_a2(Tf.g, Tf.g_o):
            S.fail(t, "A2", name)
            getattr(self.L.gates, name).disabled = True
        if not S.whole_ybar and (A.t_state_digest({"y_o": Tf.y_o}) != A.t_state_digest({"y_o": Ts.y_o})
                                 or A.t_state_digest({"g": Ts.g}) != A.t_state_digest({"g": Tf.g})):
            self._a5(t, ["fast-loop T inputs (y_o)" if not np.array_equal(Tf.y_o, Ts.y_o) else "held:g"])

        r = y - ybar
        x2 = self.ledger.step(fr.u, r)
        led = self.ledger
        a3 = A.check_a3_frame(ZERO_CEILING, x2, led.S, led.last_active)
        a4 = A.check_a4_frame(r, x2, led.S, led.E, led.bound, led.last_active, led.last_hold)
        for aid, m in (("A3", a3), ("A4", a4)):
            if m.any():
                S.fail(t, aid, [TABLE.codes[k] for k in np.nonzero(m & ~S.channel_ybar)[0]])
                S.channel_ybar |= m
        rendered = ybar + x2
        rendered = np.where(S.channel_ybar, ybar, rendered)
        if S.whole_ybar:
            rendered = ybar.copy()
        synth = laugh_synth_input(rendered)
        a9 = A.check_a9(self.factual.body.env_laugh, rendered, synth)
        if a9 and S.laugh_synth_on:
            S.fail(t, "A9", a9)
            S.laugh_synth_on = False
            S.neutral_prosody = True
        if not S.laugh_synth_on:
            synth = {k: 0.0 for k in synth}
        face = self.muscle.step(rendered)
        self.prev_rendered, self.prev_ybar, self.t = rendered, ybar, t
        return Output(rendered, face, y, ybar, x2, float(Tf.g), float(Tf.g_o), synth)


# ==================================================================================================== trace driver
def _synthetic_u(T: int, fs: float, rng) -> np.ndarray:
    t = np.arange(T) / fs
    U = np.zeros((T, N))
    for k in range(N):
        f1, f2 = rng.uniform(0.01, 0.05), rng.uniform(0.2, 0.8)
        base = 0.3 + 0.2 * np.sin(2 * np.pi * f1 * t + rng.uniform(0, 6)) + 0.1 * np.sin(2 * np.pi * f2 * t)
        U[:, k] = base - (0.3 if TABLE.signs[k] == "signed" else 0.0)
    return np.clip(U, -1, 1)


def traced_session(seconds: float = 60.0, seed: int = 0, engine_factory=None, fs: float = 30.0) -> Run:
    """One run in trace mode on a synthetic session: his streams wrapped with their channel tags at the boundary,
    his utterances "T:utterance", OwnHeard "O:own_heard", b_id "latched:b_id", the agent's own face "own:face". Every
    declared field assignment is checked (typetrace.TypedState); the display terms are checked here (rule 4, 11',
    13'). Returns the run. engine_factory(learned, session, b_id, fs) may build a modified run (tests)."""
    from engine.state.readers import TText
    from engine.state.types import Utterance, heard_at_playback
    rng = np.random.default_rng(seed)
    T = int(seconds * fs)
    U = _synthetic_u(T, fs, rng)
    b = np.concatenate([U.mean(0), np.zeros(3)])
    b_id = Tagged.wrap(b, {"latched:b_id"})
    from engine.routes.learned_t import randomise_for_trace
    L = randomise_for_trace(Learned(), seed)
    session = Session(t0=0.0, K=0.6)
    run = (engine_factory or Run)(L, session, b_id, fs)
    u_tags = frozenset("F:u." + c for c in TABLE.codes)
    read_tags = frozenset("F:u." + TABLE.codes[i] for i in READ_IDX)
    der_tags = frozenset().union(*tag_sets().values())
    own_prev = np.zeros(N)
    next_tick = 0.0
    utt_times = np.arange(5.0, seconds, 7.0)
    own_times = np.arange(8.5, seconds, 9.0)
    pend_u, pend_o = [], []
    for n in range(T):
        t = n / fs
        if utt_times.size and t >= utt_times[0]:
            te, utt_times = float(utt_times[0]), utt_times[1:]
            txt = TText.wrap("words %d of the synthetic partner" % n, {"T:utterance"})
            pend_u.append(Utterance("him", (), txt, te, txt))
        if own_times.size and t >= own_times[0]:
            te, own_times = float(own_times[0]), own_times[1:]
            oh = heard_at_playback(["reply", "number", str(n)], [te - 1.0, te - 0.5, te], "question", te - 1.5)
            tg = {"O:own_heard"}
            oh = dataclasses.replace(oh, words=tuple(TText.wrap(w, tg) for w in oh.words),
                                     t_start=Tagged.wrap(np.float64(oh.t_start), tg),
                                     t_end=Tagged.wrap(np.float64(oh.t_end), tg))
            pend_o.append(oh)
        u_plain = U[n]
        fr = Frame(t, Tagged.wrap(u_plain, u_tags), Tagged.wrap(derived(u_plain, 0.5), der_tags),
                   Tagged.wrap(u_plain[list(READ_IDX)], read_tags), Tagged.wrap(own_prev, {"own:face"}))
        if t >= next_tick - 1e-9:
            run.slow_tick(SlowInputs(next_tick, tuple(pend_u), tuple(pend_o), True, (), 0.0,
                                     float(rng.uniform())), fr.u_read)
            pend_u, pend_o = [], []
            next_tick += SLOW_DT
        tm = run.fast_step(fr)
        for name in ("y_f", "y_C", "y_A", "y_o", "g", "g_o"):
            typetrace.check_display(name, getattr(tm, name))
        own_prev = np.asarray(assemble(tm.y_f, tm.y_C, tm.y_A, tm.y_o, tm.g, tm.g_o)).view(np.ndarray).copy()
    return run
