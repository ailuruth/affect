"""Provenance wrapper for the type trace (spec §4.4, minimal API).

`Tagged` is an ndarray subclass with `tags: frozenset[str]` naming its source streams, e.g. "F:u.LP",
"T:utterance", "O:own_heard", "latched:b_id". Created with `Tagged.wrap(array, tags)` at the boundary's outputs
and at the ports. Every ufunc and every numpy function returns the union of its inputs' tags (Python and numpy
scalars carry none); a reduction that would return a numpy scalar returns a 0-d Tagged array so the tags survive;
indexing keeps the tags of the whole array (conservative). Live mode uses plain arrays; only the trace wraps.
"""
from __future__ import annotations

import numpy as np


def _tags_of(objs) -> frozenset:
    out = frozenset()
    stack = list(objs)
    while stack:
        o = stack.pop()
        if isinstance(o, Tagged):
            out |= o.tags
        elif isinstance(o, (list, tuple)):
            stack.extend(o)
        elif isinstance(o, dict):
            stack.extend(o.values())
    return out


def _plain(o):
    if isinstance(o, Tagged):
        return o.view(np.ndarray)
    if isinstance(o, list):
        return [_plain(x) for x in o]
    if isinstance(o, tuple):
        return tuple(_plain(x) for x in o)
    return o


def _retag(result, tags: frozenset):
    if isinstance(result, Tagged):
        result.tags = tags
        return result
    if isinstance(result, np.ndarray):
        r = result.view(Tagged)
        r.tags = tags
        return r
    if isinstance(result, np.generic) and result.dtype.kind in "biufc":
        r = np.asarray(result).view(Tagged)
        r.tags = tags
        return r
    if isinstance(result, tuple):
        return tuple(_retag(x, tags) for x in result)
    if isinstance(result, list):
        return [_retag(x, tags) for x in result]
    return result


class Tagged(np.ndarray):
    tags: frozenset

    @classmethod
    def wrap(cls, array, tags) -> "Tagged":
        obj = np.asarray(array).view(cls)
        obj.tags = frozenset(tags)
        return obj

    def __array_finalize__(self, obj):
        self.tags = getattr(obj, "tags", frozenset())

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        outs = kwargs.get("out", ())
        tags = _tags_of(inputs) | _tags_of(outs)
        args = [_plain(x) for x in inputs]
        if outs:
            kwargs["out"] = tuple(_plain(x) for x in outs)
        result = getattr(ufunc, method)(*args, **kwargs)
        for o in outs:                       # in-place: the written arrays now carry the union
            if isinstance(o, Tagged):
                o.tags = tags
        if outs and len(outs) == 1 and isinstance(outs[0], Tagged) and method == "__call__":
            return outs[0]
        return _retag(result, tags)

    def __array_function__(self, func, types, args, kwargs):
        tags = _tags_of(args) | _tags_of(kwargs)
        result = func(*_plain(list(args)), **{k: _plain(v) for k, v in kwargs.items()})
        return _retag(result, tags)

    def __getitem__(self, key):
        r = super().__getitem__(key)
        return _retag(r, self.tags)

    def __setitem__(self, key, value):
        """Writing into a Tagged array (ring buffers, traces in place) adds the written value's tags (M4)."""
        super().__setitem__(key, _plain(value))
        self.tags = self.tags | _tags_of([value])

    def __repr__(self):
        return f"Tagged({np.asarray(self).__repr__()}, tags={sorted(self.tags)})"


def tags_of(x) -> frozenset:
    """The provenance of a value: its tags if Tagged, else none."""
    return x.tags if isinstance(x, Tagged) else frozenset()


class TagViolation(TypeError):
    pass


def check_sources(field: str, value, allowed_prefixes: frozenset) -> None:
    """Raise if any tag of `value` lies outside the field's allowed source prefixes ("T:", "latched:", ...)."""
    bad = sorted(t for t in tags_of(value) if not any(t.startswith(p) for p in allowed_prefixes))
    if bad:
        raise TagViolation(f"field {field!r} received {bad[0]!r} (allowed: {sorted(allowed_prefixes)})")
