"""The closed list of Ω -> T ports (spec §1.3.1; F19 by construction).

A T computation may read an Ω value (`OwnHeard`) only inside one of these five functions. Each returns a T value
tagged "T:port.Pi" in trace mode (the only place where an "O:" provenance tag is replaced), so the type trace
(engine/invariants/typetrace.py) refuses any other Ω read by a T, F or display field, and records which T fields lie
downstream of each port (`downstream`, committed in engine/state/ports_downstream.json and compared in CI).

| Port | Reads | Feeds |
| P1 lambda_own        | OwnHeard.words through the encoder and Lambda | Lambda_V(own) in g and g_o |
| P2 qhat_agent_turn   | the same Lambda encoding of the agent's last OwnHeard | qhat's agent-turn input |
| P3 turn_question_bit | OwnHeard.template of the agent's last turn, if it spoke last | the turn model's question bit |
| P4 p_name            | OwnHeard.words | P_name, attenuate-only <= 0.05 on a named display |
| P5 own_turn_events   | OwnHeard.t_start, t_end | turn events agent_utterance_start / end |
"""
from __future__ import annotations

import numpy as np

from engine.invariants import typetrace
from engine.invariants.tagged import Tagged, tags_of
from engine.state.types import OwnHeard, TurnEvent

PORT_NAMES = {"P1": "lambda_own", "P2": "qhat_agent_turn", "P3": "turn_question_bit", "P4": "p_name",
              "P5": "own_turn_events"}


def _out(value, port: str):
    v = np.asarray(value.view(np.ndarray) if isinstance(value, Tagged) else value, dtype=np.float64)
    if typetrace.active() or isinstance(value, Tagged) or tags_of(value):
        return Tagged.wrap(v.copy(), {"T:port." + port})
    return v.copy()


def _check(oh) -> None:
    if not isinstance(oh, OwnHeard):
        raise TypeError("ports read only OwnHeard (made at playback)")


def lambda_own(oh: OwnHeard, encoder, lam):
    """P1: Lambda_V of the agent's own heard words (scalar)."""
    _check(oh)
    return _out(lam(encoder.encode(oh.words))[0], "P1")


def qhat_agent_turn(oh: OwnHeard, encoder, lam):
    """P2: the Lambda encoding (V, A, T) of the agent's last OwnHeard; no other text feature of it."""
    _check(oh)
    return _out(lam(encoder.encode(oh.words)), "P2")


def turn_question_bit(oh: OwnHeard | None, agent_spoke_last: bool):
    """P3: 1 if the agent spoke last and its last turn used the question template, else 0."""
    if oh is None or not agent_spoke_last:
        return _out(0.0, "P3")
    _check(oh)
    return _out(1.0 if oh.template == "question" else 0.0, "P3")


def p_name(oh: OwnHeard, encoder, pmap):
    """P4: attenuation [33] in [0, 0.05] of the displays the agent's own words name."""
    _check(oh)
    return _out(pmap(encoder.encode(oh.words)), "P4")


def own_turn_events(oh: OwnHeard):
    """P5: (agent_utterance_start, agent_utterance_end) times, and the turn events."""
    _check(oh)
    ts, te = _out(oh.t_start, "P5"), _out(oh.t_end, "P5")
    return ts, te, (TurnEvent("agent_utterance_start", float(oh.t_start)), TurnEvent("agent_utterance_end", float(oh.t_end)))


def downstream(port: str) -> list:
    """The committed downstream(Pi): T fields reachable from the port's output in the static dataflow graph."""
    return typetrace.load_downstream()[port]
