"""The 33 counterpart channels (spec §1.1; r6 §2.1, unchanged by revisions 7-9.2). Innate; frozen.

Order is the index used by every array of shape [33]. Groups are muscle and signal groups.
Columns: ceiling c_k, frozen fast gain G_k, pooled shares (s_C, s_X, s_A) as fractions of c_k, and the
onset-lobe allowance r_k as a fraction of c_k (r6 J2: r_k = 0.949 G_k / c_k on one-sided channels, 0 on
signed channels; the spec table lists it rounded to three decimals, which `LISTED_R` keeps and a test
compares). A0 runs at import: a table that breaks it cannot be imported, so the engine refuses to start.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

N_CHANNELS = 33
RHO = 0.091                 # cone seam factor rho (r6 J3)
APPRAISAL_SUP = 0.636       # sup |H| of the 20-90 s band-pass (r5 §2.1)
POOLED_MAX = 0.974          # pooled counted total per channel, fraction of c_k (r6 J3)
ONSET_LOBE_FACTOR = 0.949   # r_k = 0.949 G_k / c_k on one-sided channels (r6 J2)

# idx: (code, group, sign, c_k, G_k, (s_C, s_X, s_A))
_ROWS = (
    ("LP", "smile_laugh", "one_sided", 0.35, 0.224, (0.22, 0.05, 0.12)),
    ("CR", "smile_laugh", "one_sided", 0.25, 0.150, (0.24, 0.05, 0.12)),
    ("BU_L", "smile_laugh", "one_sided", 0.35, 0.280, (0.10, 0.02, 0.10)),
    ("RHY", "smile_laugh", "one_sided", 0.30, 0.240, (0.10, 0.02, 0.10)),
    ("BRE", "smile_laugh", "one_sided", 0.15, 0.120, (0.10, 0.02, 0.10)),
    ("BI", "brow", "one_sided", 0.20, 0.020, (0.68, 0.10, 0.05)),
    ("BO", "brow", "one_sided", 0.10, 0.024, (0.44, 0.12, 0.20)),
    ("LD", "brow", "one_sided", 0.05, 0.012, (0.44, 0.12, 0.20)),
    ("JO", "brow", "one_sided", 0.10, 0.024, (0.44, 0.12, 0.20)),
    ("HP", "head_gaze", "signed", 0.10, 0.080, (0.50, 0.20, 0.35)),
    ("VG", "head_gaze", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
    ("YAW", "head_gaze", "signed", 0.03, 0.024, (0.50, 0.20, 0.35)),
    ("TILT", "head_gaze", "signed", 0.03, 0.024, (0.50, 0.20, 0.35)),
    ("HG", "head_gaze", "signed", 0.03, 0.024, (0.50, 0.20, 0.35)),
    # voice (phrase level): G_k = 0.80 c_k, within-phrase contour only (rule 7)
    ("F0", "voice", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
    ("FR", "voice", "signed", 0.10, 0.080, (0.50, 0.20, 0.35)),
    ("EN", "voice", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
    ("RT", "voice", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
    ("PAU", "voice", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
    ("LAT", "voice", "signed", 0.05, 0.040, (0.50, 0.20, 0.35)),
) + tuple(
    (code, "zero_ceiling", "none", 0.0, 0.0, (0.0, 0.0, 0.0))
    for code in ("BL", "UL", "LT", "NW", "LS", "CHR", "LPR", "DIM", "FUN", "PUK", "MCL", "LRO", "BU_S")
)

# r_k as printed in the spec table (three decimals), for the comparison test only.
LISTED_R = {"LP": 0.608, "CR": 0.569, "BU_L": 0.759, "RHY": 0.759, "BRE": 0.759, "BI": 0.095,
            "BO": 0.228, "LD": 0.228, "JO": 0.228}


@dataclass(frozen=True)
class ChannelTable:
    codes: tuple
    groups: tuple
    signs: tuple
    c: tuple
    G: tuple
    s_C: tuple
    s_X: tuple
    s_A: tuple
    r: tuple

    def index(self, code: str) -> int:
        return self.codes.index(code)

    def array(self, field: str) -> np.ndarray:
        """A read-only float64 copy of one numeric column (innate tables are never written)."""
        a = np.array(getattr(self, field), dtype=np.float64)
        a.flags.writeable = False
        return a

    def pooled_total(self) -> tuple:
        """s_C(1 + rho) + s_X + 0.636 s_A + r_k per channel, as a fraction of c_k."""
        return tuple(sc * (1 + RHO) + sx + APPRAISAL_SUP * sa + rk
                     for sc, sx, sa, rk in zip(self.s_C, self.s_X, self.s_A, self.r))

    def zero_ceiling(self) -> tuple:
        return tuple(i for i, ck in enumerate(self.c) if ck == 0.0)


def _onset_lobe(sign: str, c: float, G: float) -> float:
    return ONSET_LOBE_FACTOR * G / c if (sign == "one_sided" and c > 0) else 0.0


TABLE = ChannelTable(
    codes=tuple(r[0] for r in _ROWS),
    groups=tuple(r[1] for r in _ROWS),
    signs=tuple(r[2] for r in _ROWS),
    c=tuple(r[3] for r in _ROWS),
    G=tuple(r[4] for r in _ROWS),
    s_C=tuple(r[5][0] for r in _ROWS),
    s_X=tuple(r[5][1] for r in _ROWS),
    s_A=tuple(r[5][2] for r in _ROWS),
    r=tuple(_onset_lobe(r[2], r[3], r[4]) for r in _ROWS),
)

SMILE_LAUGH = tuple(i for i, g in enumerate(TABLE.groups) if g == "smile_laugh")
ZERO_CEILING = TABLE.zero_ceiling()

from engine.invariants.asserts import check_a0  # noqa: E402  (A0 at import; asserts imports nothing from here)

check_a0(TABLE, POOLED_MAX, N_CHANNELS)
