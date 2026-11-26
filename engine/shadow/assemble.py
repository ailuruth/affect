"""Output assembly (spec §1.6; design §2.3), 30 Hz:

  y = sat(g y_f|smile_laugh + y_f|others + y_C + y_A + g_o y_o|smile_laugh + y_o|others) + visemes,

then the attenuate-only ledger (engine/shadow/ledger.py, in engine/shadow/shadow.py), then the muscle filter M (4 Hz,
zeta 0.8; second-order, bilinear transform, numpy only) on the face and head channels: M * (y + blink reflex).
sat clips each channel to its nominal range: one-sided and zero-ceiling channels [0, 1], signed channels [-1, 1].
Visemes and the blink reflex come with the rig at M5 (zero here). The laugh synthesizer reads only y_BU_L, y_RHY,
y_BRE (`laugh_synth_input`); there is no sob source (y_BU_S = 0; A9).
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import SMILE_LAUGH, TABLE
from engine.config.innate import ENTRIES

N = len(TABLE.codes)
SL = np.zeros(N, dtype=bool)
SL[list(SMILE_LAUGH)] = True
LO = np.array([-1.0 if s == "signed" else 0.0 for s in TABLE.signs])
HI = np.ones(N)
_FACE = set(ENTRIES["face_channels"].value) | {c for c, g in zip(TABLE.codes, TABLE.groups) if g == "head_gaze"}
FACE_RENDER = np.array([c in _FACE for c in TABLE.codes])
_MF = ENTRIES["muscle_filter"].value


def assemble(y_f, y_C, y_A, y_o, g, g_o, visemes=None):
    pre = np.where(SL, g * y_f, y_f) + y_C + y_A + np.where(SL, g_o * y_o, y_o)
    y = np.clip(pre, LO, HI)
    return y if visemes is None else y + visemes


def laugh_synth_input(y) -> dict:
    return {c: y[TABLE.index(c)] for c in ("BU_L", "RHY", "BRE")}


class MuscleFilter:
    """H(s) = w^2 / (s^2 + 2 zeta w s + w^2), w = 2 pi 4 Hz, discretised by the bilinear transform at fs; per channel,
    direct form II transposed, applied to the face and head channels only (others pass through)."""

    def __init__(self, fs: float, freq_hz: float = _MF["freq_hz"], zeta: float = _MF["zeta"]):
        w = 2 * np.pi * freq_hz
        K = 2.0 * fs
        a0 = K * K + 2 * zeta * w * K + w * w
        self.b = np.array([w * w, 2 * w * w, w * w]) / a0
        self.a = np.array([1.0, (2 * w * w - 2 * K * K) / a0, (K * K - 2 * zeta * w * K + w * w) / a0])
        self.z = None

    def step(self, y):
        y = np.asarray(y, dtype=np.float64)
        if self.z is None:                                  # start at rest on the first frame's value
            self.z = np.stack([y * (1 - self.b[0]), y * (self.b[2] - self.a[2])])
        out = self.b[0] * y + self.z[0]
        self.z = np.stack([self.b[1] * y - self.a[1] * out + self.z[1], self.b[2] * y - self.a[2] * out])
        return np.where(FACE_RENDER, out, y)
