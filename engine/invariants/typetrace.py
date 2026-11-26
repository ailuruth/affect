"""The type trace (spec §4.4): rules 1-14 checked dynamically on provenance-carrying arrays.

In trace mode every input stream is a `Tagged` array (engine/invariants/tagged.py) and every assignment of a field
declared in engine/state/types.py goes through `TypedState.__setattr__`, which calls `check_field`: the value's tags
must lie inside the allowed prefixes of the field's type (T reads only T, latched values and the port outputs
"T:port.Pi"; F never reads Ω). The display terms are checked at assembly by `check_display` against rule 4 and the
gate rules (11', 13'): y_f only his channels; y_o only T; g none of his LP, CR, BU_L, RHY, BRE; g_o no channel of his.

`run_trace` (below) drives one engine run in trace mode on a synthetic session (CI) or on recorded features (the
Mac, at every start) and returns the record of which port tags reached which T field: `downstream(Pi)`, compared in
CI with the committed engine/state/ports_downstream.json (F19). Live mode uses plain arrays and checks nothing here.

Limits (stated): the wrapper follows data flow, not control flow (a branch on an F value that selects between two T
values is not seen); Python float() and built-in max/min drop tags, so engine code on traced paths uses numpy
operations only, which the trace's own tests exercise.
"""
from __future__ import annotations

import json
import traceback
from pathlib import Path

from engine.invariants.tagged import TagViolation, _tags_of
from engine.state.types import ALLOWED_SOURCES, FIELD_TYPES

_STATE = {"on": False, "record": None}

DOWNSTREAM_PATH = Path(__file__).resolve().parents[1] / "state" / "ports_downstream.json"
PORTS = ("P1", "P2", "P3", "P4", "P5")

# rule 4 and the gate rules: allowed prefixes, and exact tags refused (the echo gate's unread channels)
DISPLAY_SOURCES = {
    "y_f": (frozenset({"F:u."}), frozenset()),
    "y_C": (frozenset({"F:", "latched:", "T:"}), frozenset()),
    "y_A": (frozenset({"F:", "latched:", "T:"}), frozenset()),
    "y_o": (frozenset({"T:", "noise:"}), frozenset()),
    "g": (frozenset({"T:", "F:", "own:", "latched:"}), None),     # forbidden set filled from INNATE (rule 11')
    "g_o": (frozenset({"T:", "own:"}), frozenset()),
}


def _unread_tags() -> frozenset:
    from engine.config.innate import ENTRIES
    return frozenset("F:u." + c for c in ENTRIES["echo_gate_unread"].value)


def active() -> bool:
    return _STATE["on"]


def start() -> dict:
    _STATE["on"] = True
    _STATE["record"] = {}
    return _STATE["record"]


def stop() -> dict:
    _STATE["on"] = False
    rec, _STATE["record"] = _STATE["record"], None
    return rec or {}


def check_field(name: str, value, owner: str = "") -> None:
    ftype = FIELD_TYPES[name]
    tg = _tags_of([value])
    bad = sorted(t for t in tg if not any(t.startswith(p) for p in ALLOWED_SOURCES[ftype]))
    if bad:
        stack = "".join(traceback.format_stack(limit=6)[:-2])
        raise TagViolation(f"type trace: {owner}.{name} ({ftype}) received {bad[0]!r}\n{stack}")
    rec = _STATE["record"]
    if rec is not None:
        rec.setdefault(name, set()).update(tg)


def check_display(name: str, value) -> None:
    allowed, forbidden = DISPLAY_SOURCES[name]
    if forbidden is None:
        forbidden = _unread_tags()
    tg = _tags_of([value])
    bad = sorted(t for t in tg if t in forbidden or not any(t.startswith(p) for p in allowed))
    if bad:
        raise TagViolation(f"type trace: display term {name} received {bad[0]!r}")
    rec = _STATE["record"]
    if rec is not None:
        rec.setdefault("display:" + name, set()).update(tg)


class TypedState:
    """Base of every state container: in trace mode each assignment of a declared field is type-checked."""

    def __setattr__(self, name, value):
        if _STATE["on"] and name in FIELD_TYPES:
            check_field(name, value, type(self).__name__)
        object.__setattr__(self, name, value)


def downstream(record: dict) -> dict:
    """ports.downstream(Pi): the T fields whose values carried the port's output tag during the trace."""
    out = {}
    for p in PORTS:
        tag = "T:port." + p
        out[p] = sorted(f for f, tg in record.items()
                        if not f.startswith("display:") and FIELD_TYPES.get(f) == "T" and tag in tg)
    return out


def load_downstream(path: Path = DOWNSTREAM_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_downstream(ds: dict, path: Path = DOWNSTREAM_PATH) -> None:
    Path(path).write_text(json.dumps(ds, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def run_trace(seconds: float = 60.0, seed: int = 0, engine_factory=None) -> dict:
    """Run one engine run in trace mode on a synthetic session (or a recorded one through engine_factory) and return
    the field record. Raises TagViolation on the first violation. See engine/shadow/shadow.py for the driver."""
    from engine.shadow.shadow import traced_session
    start()
    try:
        traced_session(seconds=seconds, seed=seed, engine_factory=engine_factory)
    finally:
        rec = stop()
    return rec
