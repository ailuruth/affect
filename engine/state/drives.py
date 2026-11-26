"""The drive D(b) and the partner-load drive D_p(N) (spec §1.3 "Drive"; r5 §2.1). Pure functions of the state.

Every term is satiable (Principle 6): D = 0 inside the dead-band box. The drive dynamics themselves (E's waking
decay, A's lexical term, ...) are built at M4; M0 has the forms, the declared update terms that A14 accounts
for, and nothing else.
"""
from __future__ import annotations

from engine.config.innate import ENTRIES

DRIVES = ("E", "A", "V", "K", "P", "I")
_TERMS = ENTRIES["drive_terms"].value
_PSI_POW = ENTRIES["drive_psi_power"].value
_DP = ENTRIES["Dp_terms"].value

# The declared update terms of each drive within a session (A14), with the sign each may take:
# +1 raises the drive only, -1 lowers it only, 0 either way.
DECLARED_TERMS = {
    "E": {"waking_decay": -1},
    "A": {"lexical_rise": +1, "lexical_decay": -1, "face_voice_load": 0},
    "V": {"reflex_load": 0, "h_word_latch": +1, "h_word_decay": -1},
    "K": {"in_session_contact": -1},
    "P": {"growth": +1, "qhat_term": -1},
    "I": {"growth": +1, "progress_term": -1},
}


def psi(x: float) -> float:
    return x ** _PSI_POW


def drive(b: dict, f_id: float = 1.0) -> float:
    """D(b) = sum_i w_i psi(|b_i - b_i*| - delta_i)+ ; K's weight is 0.6 f_id."""
    total = 0.0
    for name in DRIVES:
        setp, band, w = _TERMS[name]
        if name == "K":
            w = w * f_id
        total += w * psi(max(0.0, abs(b[name] - setp) - band))
    return total


def drive_partner(V: float, A: float, T: float) -> float:
    """D_p(N) = 0.8 [psi(V - 0.05)+ + 0.7 psi(A - 0.15)+ + 0.5 psi(T - 0.20)+]."""
    s = 0.0
    for name, x in (("V", V), ("A", A), ("T", T)):
        thr, w = _DP[name]
        s += w * psi(max(0.0, x - thr))
    return _DP["scale"] * s
