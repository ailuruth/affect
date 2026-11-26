"""Type tags of the latent state (spec §1.3; r5 §2.2).

T: his words, turn order, session boundaries, identity, per-session latched values, the agent's own body clock,
   and anything computed only from these.
F: anything computed within a session from his face, voice or derived features.
O: the agent's own realised words, draft choice, retrieval, own turn events (the design's Omega).
K: the world model and the concept layer.
latched: rule-6 session values (b_id, b_read, sigma_id), readable by T only as rule 6 allows.

FIELD_TYPES is the declaration the T1 AST rule (engine/invariants/t1_rule.py) and, at M4, the type trace read.
The objects TranscriptText, Marker, Snippet and OwnHeard come at M4/M6.
"""
from __future__ import annotations

TYPES = frozenset({"T", "F", "O", "K", "latched"})

FIELD_TYPES = {
    "E": "T",
    "A_F": "F",
    "A_L": "T",
    "V_F": "F",
    "h_word": "T",
    "K": "T",
    "P_play": "T",
    "I_lp": "T",
    "N_L": "T",
    "Dp_face": "F",
    "Dp_word": "T",
    "mu_T": "T",
    "mu_F": "F",
    "slots_T": "T",
    "slots_F": "F",
    "xi": "F",
    "xi_A": "F",
    "D_tau": "F",
    "q_trace": "T",
    "omega": "T",
    "b_id": "latched",
    "b_read": "latched",
    "sigma_id": "latched",
    "env_drop": "T",
    "env_rise": "T",
    "M_state": "K",
    "concepts": "K",
}

assert set(FIELD_TYPES.values()) <= TYPES


def fields_of(tag: str) -> frozenset:
    return frozenset(k for k, v in FIELD_TYPES.items() if v == tag)
