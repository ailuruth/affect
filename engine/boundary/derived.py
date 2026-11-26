"""Derived partner features (spec §1.2.5; r5 §2.1): innate, F-typed, computed by the boundary from u.

  f_loud = (EN - 0.7)+ / 0.3;  g_at = his gaze at the agent's face in [0, 1] (from the tracker, M2);
  f_glare = BL LT g_at;  f_laugh = sqrt(BU_L RHY);  f_duch = sqrt(LP CR).
And the threat reflex V_F = g_at max(f_glare, f_loud (1 - 2 f_pos)+), f_pos = max(f_laugh, f_duch) (S41).
In trace mode each derived feature carries the provenance tags of the channels it is computed from.
"""
from __future__ import annotations

import numpy as np

from engine.config.channels import TABLE
from engine.config.innate import ENTRIES

F_DER = ("f_loud", "g_at", "f_glare", "f_laugh", "f_duch")
_LOUD = ENTRIES["loud_threshold"].value
_POS = ENTRIES["reflex_glare_loud_pos_gain"].value
_I = {c: TABLE.index(c) for c in ("EN", "BL", "LT", "BU_L", "RHY", "LP", "CR")}


def derived(u, g_at):
    """f_der [5] in the order of F_DER."""
    f_loud = np.maximum(u[_I["EN"]] - _LOUD["EN"], 0.0) / _LOUD["span"]
    f_glare = u[_I["BL"]] * u[_I["LT"]] * g_at
    f_laugh = np.sqrt(np.maximum(u[_I["BU_L"]] * u[_I["RHY"]], 0.0))
    f_duch = np.sqrt(np.maximum(u[_I["LP"]] * u[_I["CR"]], 0.0))
    return np.stack([f_loud, g_at * 1.0, f_glare, f_laugh, f_duch])


def threat_reflex(f_der):
    f_loud, g_at, f_glare, f_laugh, f_duch = (f_der[i] for i in range(5))
    f_pos = np.maximum(f_laugh, f_duch)
    return g_at * np.maximum(f_glare, f_loud * np.maximum(1.0 - _POS * f_pos, 0.0))


def tag_sets() -> dict:
    """Provenance of each derived feature (for the trace's boundary wrapper)."""
    u = lambda *cs: {"F:u." + c for c in cs}
    return {"f_loud": u("EN"), "g_at": {"F:gaze_at"}, "f_glare": u("BL", "LT") | {"F:gaze_at"},
            "f_laugh": u("BU_L", "RHY"), "f_duch": u("LP", "CR")}
