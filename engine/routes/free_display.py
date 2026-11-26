"""The free display y_o (spec §1.5.3; r5 §2.7; design §2.5-2.7): Pi_o = Pi_0 + Delta + L_d, **T inputs only**.

Drivers (all T; evaluated at the frame clock from the body's event records, so the 2-Hz events give smooth
envelopes): env_drop (drop events, E1); env_rise (own rise events; Q33 switch own_rise_brow); h_d = h/(h + 0.15);
a_A = A_L/(A_L + 0.2); e = (0.5 - E)+/0.3; env_progress (learning-progress drops); env_laugh (own laugh amplitude
0.40 qhat at his turns, <= 0.40). Pi_0 newborn rows (S45; INNATE.lock pi0_*): drop -> LP, CR, brighter voice; own
rise -> BI +0.45, LD +0.35, lower voice; h_word -> brow, depressor, gaze aversion; activation -> raised lids and outer
brow; low energy; progress drop -> interest face; the laugh motor pattern (BU_L 0.40, RHY 0.35, CR 0.20, LP 0.15 per
unit); the pre-speech inhale (BRE 0.15 for 0.3 s) and the physiological sigh (BRE 0.15 for 1 s).
Delta (UNTRAINED STUB): 161 -> 128 -> 18 open synergies, tanh, each in [-0.3, 0.3], with zero weight on the BL, LT,
LPR, NW, DIM rows and LS, CHR only times the agent's own rise envelope (own-display mask, Q31). L_d (engine/routes/
learned_t.py) is added with the same mask. P_name (port P4) attenuates each named channel by <= 0.05.

g_o is applied at assembly to the whole smile_laugh part of y_o (spec §1.6), the own laugh included; the own laugh's
amplitude here is 0.40 qhat (T), so g_o multiplies it once (see engine/README.md: the spec's a_laugh = 0.40 qhat g_o).
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES
from engine.config.operator import require
from engine.state.body import envelope_sum

N = len(TABLE.codes)
CODES = TABLE.codes
_DS = ENTRIES["pi0_driver_shape"].value
DRIVERS = ("drop", "rise", "word_latch", "activation", "low_energy", "progress_drop", "laugh")
_MASK = ENTRIES["own_display_mask"].value
MASK_ZERO = tuple(CODES.index(c) for c in _MASK["zero"])
MASK_RISE_ONLY = tuple(CODES.index(c) for c in _MASK["own_rise_only"])
INHALE = ENTRIES["inhale_pattern"].value
SIGH = ENTRIES["sigh_pattern"].value
BRE = CODES.index("BRE")
DSHAPE = ENTRIES["display_delta_shape"].value
LAUGH_MAX = ENTRIES["own_laugh_max"].value


def pi0_matrix(own_rise_brow: bool = True) -> np.ndarray:
    """(33, 7): one column per driver of DRIVERS."""
    rows = {"drop": ENTRIES["pi0_drop_row"].value,
            "rise": {**ENTRIES["pi0_rise_row"].value, **ENTRIES["pi0_rise_voice"].value},
            "word_latch": ENTRIES["pi0_word_latch_row"].value, "activation": ENTRIES["pi0_activation_row"].value,
            "low_energy": ENTRIES["pi0_low_energy_row"].value, "progress_drop": ENTRIES["pi0_progress_drop_row"].value,
            "laugh": ENTRIES["laugh_pattern"].value}
    P = np.zeros((N, len(DRIVERS)))
    for i, d in enumerate(DRIVERS):
        for code, v in rows[d].items():
            if d == "rise" and code in ("BI", "LD") and not own_rise_brow:
                continue
            P[CODES.index(code), i] = v
    return P


class DisplayDelta:
    """Delta: T inputs (161) -> 128 -> 18 open synergies (tanh x bound) -> channels (synergy matrix 18 x 33)."""

    def __init__(self):
        self.W1 = np.zeros((DSHAPE["inputs"], DSHAPE["hidden"]))
        self.W2 = np.zeros((DSHAPE["hidden"], DSHAPE["out"]))
        self.syn = np.zeros((DSHAPE["out"], N))
        self.trained = False
        self.disabled = False

    def __call__(self, z_T, env_rise):
        if self.disabled:
            return np.zeros(N)
        s = DSHAPE["bound"] * np.tanh(np.tanh(z_T @ self.W1) @ self.W2)
        y = s @ self.syn
        mask = np.ones(N)
        mask[list(MASK_ZERO)] = 0.0
        y = y * mask
        rise_only = np.zeros(N)
        rise_only[list(MASK_RISE_ONLY)] = 1.0
        return y * (1.0 - rise_only) + y * rise_only * env_rise

    def mask_violations(self) -> list:
        """A7 on Delta: no weight on the masked rows (the synergy matrix columns of BL, LT, LPR, NW, DIM)."""
        return [CODES[k] for k in MASK_ZERO if np.any(self.syn[:, k] != 0)]


class FreeDisplay:
    def __init__(self, delta: DisplayDelta):
        self.delta = delta
        self.P0 = pi0_matrix(require("own_rise_brow")["own_rise_brow"])
        m = np.ones(N)
        m[list(MASK_ZERO)] = 0.0
        self.mask = m

    def drivers(self, body, t: float):
        h = body.h_word
        e_low = np.maximum(0.0, _DS["low_energy_ref"] - body.E) / _DS["low_energy_span"]
        return np.stack([envelope_sum(body.drop_events, t), envelope_sum(body.rise_events, t),
                         h / (h + _DS["h_word_half"]), body.A_L / (body.A_L + _DS["activation_half"]), e_low,
                         envelope_sum(body.progress_events, t), envelope_sum(body.laugh_events, t, LAUGH_MAX)])

    def step(self, body, t: float, z_T=None):
        """y_o [33] at frame time t from the body's T values."""
        d = self.drivers(body, t)
        y = self.P0 @ d
        pulse = np.zeros(N)
        if 0.0 <= t - float(body.inhale_t) < INHALE["duration_s"]:
            pulse[BRE] += INHALE["BRE"]
        if 0.0 <= t - float(body.sigh_t) < SIGH["duration_s"]:
            pulse[BRE] += SIGH["BRE"]
        z = np.zeros(DSHAPE["inputs"]) + 0.0 * body.E if z_T is None else z_T
        y = y + pulse + self.delta(z, d[1]) + body.L_d * self.mask
        return y * (1.0 - body.p_name), d
