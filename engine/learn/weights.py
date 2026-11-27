"""The general learning biases of replay (spec §1.10; D85 source 3; design audit S38-S40, S48; r6 §2.1). These are
the only innate parts of learning; none names a situation, an expression or a label.

  sample weight      w = 1 + 3 min(1, D_p(N-hat)/0.05) on every replayed moment (S48, kappa_replay = 4: moments of
                     the agent's own partner-need drive are consolidated more, McGaugh-type; one scalar
                     of the agent's own model, the same for every topic and person)
  learning rate      lr x exp(-0.5 r_bar), r_bar the night's mean amplitude of the agent's own drop events
                     (Joffily-type: a night of many own drops consolidates more slowly)
  gradient           clipped to norm 1 per parameter group; pull 0.1 to the initial weights theta_0
  calibration        from low-need moments, slow toward aversive readings (S38; engine/learn/nightly.py)
  credit             the adapter learns only from separated, partner-initiated reports (S40)

**What the weights may read** (`ALLOWED_WEIGHT_SIGNALS`): the agent's own D_p column of the body snapshot and its own
drop-event amplitudes. Nothing reads his smiles, his attention (gaze, presence) or his time (session length, time
of day, how long he stayed) as a reward or a target (brief Principle 6): his face enters learning only as an input
(the appraisal's band-passed input, his calibrated face for H_id and the calibration statistics), never as a weight,
a learning-rate factor or the target of any objective (`TARGET_SOURCES`, tested in tests/test_replay.py).
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES

_RW = ENTRIES["replay_need_weight"].value
LR_COEFF = float(ENTRIES["lr_gate_coeff"].value)
CLIP = float(ENTRIES["grad_clip"].value)
PULL = float(ENTRIES["theta0_pull"].value)

ALLOWED_WEIGHT_SIGNALS = frozenset({"body.Dp", "events.drop_event.amp"})

# The stored streams each objective's target is computed from (and nothing else). None of them is his face, his
# gaze, his presence or a duration.
TARGET_SOURCES = {
    "pi_tilde": frozenset({"own_loads"}),                 # the agent's own loads, from its own face
    "calibration": frozenset(),                           # statistics of his face, no target
    "head_id": frozenset({"transcript.his"}),             # the population reader's decoding of his words
    "adapter": frozenset({"transcript.his", "events.report"}),
    "word_v": frozenset({"body.V_F"}),                    # the threat reflex (teacher)
    "appraisal": frozenset({"drivers"}),                  # the agent's own innate display 2 s ahead
    "delta": frozenset({"own_loads"}),                    # the agent's own legibility
    "omega": frozenset({"events.drop_event", "body.D", "body.h_word"}),   # omega_rule on its own T events
}
FORBIDDEN_TARGET_SOURCES = frozenset({"u", "f_der", "breath", "voice_phrase", "presence", "session_length",
                                      "time_of_day", "gaze"})


def sample_weight(Dp) -> np.ndarray:
    """1 + 3 min(1, D_p/0.05) per moment (S48). Reads only the agent's own D_p(N-hat)."""
    d = np.maximum(np.asarray(Dp, dtype=np.float64), 0.0)
    return 1.0 + _RW["gain"] * np.minimum(1.0, d / _RW["scale"])


def lr_scale(drop_amps) -> float:
    """exp(-0.5 r_bar), r_bar = mean amplitude of the night's own drop events (0 without any)."""
    a = np.asarray(list(drop_amps), dtype=np.float64)
    r_bar = float(np.mean(a)) if a.size else 0.0
    return float(np.exp(-LR_COEFF * r_bar))


def clip_grad(g: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(g))
    return g * (CLIP / n) if n > CLIP else g


def biased_step(theta: np.ndarray, grad: np.ndarray, theta0: np.ndarray, lr: float) -> np.ndarray:
    """theta <- theta - lr (clip(grad) + 0.1 (theta - theta_0))."""
    return theta - lr * (clip_grad(grad) + PULL * (theta - theta0))
