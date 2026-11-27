"""One engine session for the battery: engine.shadow.ShadowPair driven frame by frame, with the hooks the harnesses
need, and the internal-state readouts they score.

Hooks (each documented where it is defined):
  lesion  a switch from eval/switches.py, applied to the pair (and its own copy of the learned parts) before frame 0;
  steer   eval/steering.Step: a controlled change of one named latent component, applied to the factual and the shadow
          run alike (a T field changed in one run only would be an F -> T leak and fire A5);
  mirror  his streams are made from the agent's own rendered output (the mirror-only partner, eval/mirror.py);
  face_fn his streams transformed before the boundary (input clamps, swaps; words and turn order unchanged).

Readouts are the engine's own state, never a comparison with a human face: per 2-Hz tick the factual run's body
fields (`TICK_FIELDS`), the drive D, |L_d|, and the T-state digest (A5's digest); per frame y, ybar, the ledger's
x2, rendered output, g and g_o. Every run gets its own deep copy of the learned parts.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

import numpy as np

from engine.config.channels import TABLE
from engine.invariants.asserts import t_state_digest
from engine.shadow.shadow import Frame, ShadowPair
from engine.state.body import Session
from engine.state.types import Utterance, heard_at_playback

N = len(TABLE.codes)
CAPPED = np.asarray(TABLE.c) > 0
TICK_FIELDS = ("E", "A_L", "h_word", "K", "P_play", "I_lp", "Dp_word", "q_hat", "q_trace", "env_drop", "env_rise",
               "env_progress", "env_laugh")


@dataclass
class PartnerSession:
    """One partner session as features only: his 33 channels at fs (None for the mirror-only partner), his words
    (t_end, text) and the agent's heard turns (t_end, words). `day` orders sessions in time (month-swap)."""
    U: np.ndarray | None
    fs: float
    utterances: tuple = ()
    own_heard: tuple = ()
    g_at: float = 0.4
    pid: str = "partner"
    day: float = 0.0
    seconds: float | None = None

    def __post_init__(self):
        if self.seconds is None:
            self.seconds = None if self.U is None else self.U.shape[0] / self.fs

    @property
    def T(self) -> int:
        return int(round(self.seconds * self.fs))


@dataclass
class Mirror:
    """The mirror-only partner: his channel k at frame n is (1 - gain) base_k + gain rendered_k(n - lag), clipped to
    the channel's range (gain 1: a pure mirror of the agent's own rendered output). He shows nothing of his own; his
    latched baseline b_id is `base`."""
    base: np.ndarray
    gain: float = 1.0
    lag_s: float = 0.3


@dataclass
class Trace:
    fs: float
    tick_t: np.ndarray
    ticks: dict
    digests: list
    U: np.ndarray
    y: np.ndarray
    ybar: np.ndarray
    x2: np.ndarray
    rendered: np.ndarray
    g: np.ndarray
    g_o: np.ndarray
    safety_log: list
    steer_t: float | None = None
    meta: dict = field(default_factory=dict)

    @property
    def r(self) -> np.ndarray:
        return self.y - self.ybar


def b_id_of(U: np.ndarray) -> np.ndarray:
    return np.concatenate([np.asarray(U).mean(0), np.zeros(3)])


def run(ps: PartnerSession, learned, lesion=None, steer=None, mirror: Mirror | None = None, face_fn=None,
        seed: int = 0, session: Session | None = None, b_id=None) -> Trace:
    L = copy.deepcopy(learned)
    fs = float(ps.fs)
    T = ps.T
    lo = np.where(np.array([s == "signed" for s in TABLE.signs]), -1.0, 0.0)
    if mirror is not None:
        U_src = None
        b = np.concatenate([np.asarray(mirror.base, float), np.zeros(3)]) if b_id is None else b_id
    else:
        U_src = ps.U if face_fn is None else face_fn(ps.U.copy())
        b = b_id_of(U_src) if b_id is None else b_id
    pair = ShadowPair(session or Session(K=0.6), b, L, fs=fs, seed=seed)
    if lesion is not None:
        lesion.apply(pair)
    utt = sorted(ps.utterances)
    own = sorted(ps.own_heard)
    ui = oi = 0
    U = np.zeros((T, N))
    Y, YB, X2, R = (np.zeros((T, N)) for _ in range(4))
    G, GO = np.zeros(T), np.zeros(T)
    tick_t, ticks, digests = [], {k: [] for k in TICK_FIELDS + ("D", "L_d_abs")}, []
    lag = int(round(mirror.lag_s * fs)) if mirror is not None else 0
    steered = None
    for n in range(T):
        t = n / fs
        while ui < len(utt) and utt[ui][0] <= t:
            te, txt = utt[ui]
            pair.push_utterance(Utterance("him", (), txt, te, txt))
            ui += 1
        while oi < len(own) and own[oi][0] <= t:
            te, words = own[oi]
            k = len(words)
            pair.push_own_heard(heard_at_playback(list(words), [te - 0.4 * (k - 1 - i) for i in range(k)],
                                                  "statement", te - 0.4 * k))
            oi += 1
        if mirror is not None:
            src = R[n - lag] if n - lag >= 0 else np.zeros(N)
            u = np.clip((1.0 - mirror.gain) * mirror.base + mirror.gain * src, lo, 1.0)
        else:
            u = U_src[n]
        U[n] = u
        before = pair.next_tick
        o = pair.step(Frame.from_u(t, u, ps.g_at))
        Y[n], YB[n], X2[n], R[n] = o.y, o.ybar, o.x2, o.rendered
        G[n], GO[n] = o.g, o.g_o
        if pair.next_tick != before:
            body = pair.factual.body
            tick_t.append(before)
            for k in TICK_FIELDS:
                ticks[k].append(float(getattr(body, k)))
            ticks["D"].append(float(body.D()))
            ticks["L_d_abs"].append(float(np.abs(body.L_d).sum()))
            digests.append(t_state_digest(body.t_fields()))
            if steer is not None and steered is None and before >= steer.t - 1e-9:
                steer.apply(pair)
                steered = float(before)
    return Trace(fs, np.asarray(tick_t), {k: np.asarray(v) for k, v in ticks.items()}, digests, U, Y, YB, X2, R, G,
                 GO, list(pair.safety.log), steered, {"pid": ps.pid, "seed": seed})


# ==================================================================================================== readouts
def frames_changed(tr: Trace, channels=None) -> float:
    """Fraction of frames on which the ledger changed the partner-caused part (x2 != r) on any capped channel."""
    m = CAPPED if channels is None else np.isin(np.arange(N), list(channels)) & CAPPED
    diff = np.abs(tr.x2 - tr.r)[:, m] > 1e-12
    return float(diff.any(axis=1).mean()) if diff.size else 0.0


def summary(tr: Trace, after: float | None = None) -> dict:
    """Scalar internal-state readouts of one run (means over ticks / frames from time `after`)."""
    from engine.config.channels import SMILE_LAUGH
    sel = tr.tick_t >= (after if after is not None else -np.inf)
    n0 = 0 if after is None else int(np.ceil(after * tr.fs))
    out = {k: float(v[sel].mean()) if sel.any() else 0.0 for k, v in tr.ticks.items()}
    sl = list(SMILE_LAUGH)
    out.update({
        "g": float(tr.g[n0:].mean()), "g_o": float(tr.g_o[n0:].mean()),
        "smile_laugh_rendered": float(tr.rendered[n0:, sl].mean()),
        "partner_part_abs": float(np.abs(tr.r[n0:]).mean()),
        "x2_abs": float(np.abs(tr.x2[n0:]).mean()),
        "ledger_frames_changed": frames_changed(tr),
        "zero_ceiling_x2_abs": float(np.abs(tr.x2[n0:, ~CAPPED]).max()) if (~CAPPED).any() else 0.0,
        "assert_failures": float(len(tr.safety_log)),
    })
    return out


READOUTS = TICK_FIELDS + ("D", "L_d_abs", "g", "g_o", "smile_laugh_rendered", "partner_part_abs", "x2_abs",
                          "ledger_frames_changed", "zero_ceiling_x2_abs", "assert_failures")
