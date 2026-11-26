"""T1 as an AST rule (spec §4.4, A15): no counter, accumulator or event rate is a T field.

Checked in engine/state/ and engine/routes/, on every assignment whose target is a field declared T
(engine/state/types.py), by bare name or attribute name:
  1. no augmented assignment whose right side is an integer constant or len(...);
  2. no call to len, .count, collections.Counter / Counter, np.count_nonzero, np.sum or np.mean on an argument
     named as an event list, event-time array or turn list;
  3. no division of a count by an elapsed time.
Also no T field is declared with a counter-like name. Values of the last utterances and time-since-event are
allowed (rule 14). Exceptions only by name on the reviewed list T1_EXCEPTIONS (currently none).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from engine.state.types import fields_of

T1_EXCEPTIONS: tuple = ()          # reviewed list of (path, field) pairs; adding one is a reviewed change

_COUNT_FUNCS = {"len", "Counter", "count_nonzero", "sum", "mean"}
_COUNT_METHODS = {"count"}
_EVENTISH = {"event", "events", "turns", "onsets", "utterances"}
_TIMEISH = {"elapsed", "duration", "dt", "since", "time", "seconds", "t"}
_COUNTISH = {"count", "counts", "counter", "num", "n", "total"}
_NAME_FORBIDDEN = {"count", "counter", "counts", "rate", "accum", "accumulator", "tally"}


def tokens(name: str) -> list:
    out = []
    for part in re.split(r"[^0-9A-Za-z]+", name):
        out += [t.lower() for t in re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", part)]
    return out


def _ident(node) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Subscript):
        return _ident(node.value)
    return ""


def _eventish(node) -> bool:
    name = _ident(node)
    tk = set(tokens(name))
    return bool(tk & _EVENTISH) or name.endswith("_times") or (("turn" in tk) and bool(tk & {"list", "times"}))


def _is_count_call(node) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if isinstance(f, ast.Name) and f.id in _COUNT_FUNCS:
        return True
    if isinstance(f, ast.Attribute) and (f.attr in _COUNT_FUNCS or f.attr in _COUNT_METHODS):
        return True
    return False


def _counting_on_events(expr) -> ast.AST | None:
    for n in ast.walk(expr):
        if _is_count_call(n):
            f = n.func
            args = list(n.args)
            if isinstance(f, ast.Attribute) and f.attr in _COUNT_METHODS:
                args.append(f.value)
            if any(_eventish(a) for a in args):
                return n
    return None


def _count_over_time(expr) -> ast.AST | None:
    for n in ast.walk(expr):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Div, ast.FloorDiv)):
            num_count = any(_is_count_call(m) or (isinstance(m, (ast.Name, ast.Attribute))
                                                  and set(tokens(_ident(m))) & _COUNTISH)
                            for m in ast.walk(n.left))
            den_time = any(isinstance(m, (ast.Name, ast.Attribute)) and set(tokens(_ident(m))) & _TIMEISH
                           for m in ast.walk(n.right))
            if num_count and den_time:
                return n
    return None


def check_source(src: str, path: str = "<src>", t_fields: frozenset | None = None) -> list:
    """Return a list of (path, line, field, rule) violations in one Python source."""
    t_fields = fields_of("T") if t_fields is None else t_fields
    out = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.AugAssign):
            targets, value = [node.target], node.value
        elif isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for tg in targets:
            field = _ident(tg)
            if field not in t_fields or (path, field) in T1_EXCEPTIONS:
                continue
            if isinstance(node, ast.AugAssign):
                v = node.value
                if (isinstance(v, ast.Constant) and isinstance(v.value, int) and not isinstance(v.value, bool)) or \
                        (isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "len"):
                    out.append((path, node.lineno, field, "augmented assignment of an integer or len()"))
            if _counting_on_events(value) is not None:
                out.append((path, node.lineno, field, "count over an event or turn list"))
            if _count_over_time(value) is not None:
                out.append((path, node.lineno, field, "count divided by elapsed time"))
    return out


def check_declarations(t_fields: frozenset | None = None) -> list:
    t_fields = fields_of("T") if t_fields is None else t_fields
    return [(f, "counter-like T field name") for f in sorted(t_fields) if set(tokens(f)) & _NAME_FORBIDDEN]


def check_tree(root: Path) -> list:
    out = []
    for sub in ("engine/state", "engine/routes"):
        for p in sorted((root / sub).rglob("*.py")):
            out += check_source(p.read_text(encoding="utf-8"), str(p.relative_to(root)))
    return out
