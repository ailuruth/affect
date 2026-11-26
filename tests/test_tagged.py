"""Provenance wrapper (spec §4.4)."""
import numpy as np
import pytest

from engine.invariants.tagged import Tagged, TagViolation, check_sources, tags_of


def test_wrap_and_union():
    a = Tagged.wrap(np.ones(3), {"F:u.LP"})
    b = Tagged.wrap(np.arange(3.0), {"T:utterance"})
    c = a * b + 2.0
    assert isinstance(c, Tagged) and c.tags == {"F:u.LP", "T:utterance"}
    assert (a + 1).tags == {"F:u.LP"}


def test_functions_reductions_and_indexing():
    a = Tagged.wrap(np.arange(6.0).reshape(2, 3), {"F:u.CR"})
    b = Tagged.wrap(np.ones(3), {"latched:b_id"})
    assert np.sum(a).tags == {"F:u.CR"}
    assert a.mean().tags == {"F:u.CR"}
    assert np.concatenate([a[0], b]).tags == {"F:u.CR", "latched:b_id"}
    assert a[1, 2].tags == {"F:u.CR"}
    assert np.maximum(a[0], b).tags == {"F:u.CR", "latched:b_id"}
    assert np.where(a[0] > 1, a[0], b).tags == {"F:u.CR", "latched:b_id"}


def test_in_place_and_plain_inputs():
    a = Tagged.wrap(np.zeros(3), {"T:turn"})
    a += Tagged.wrap(np.ones(3), {"O:own_heard"})
    assert a.tags == {"T:turn", "O:own_heard"}
    assert tags_of(np.ones(2)) == frozenset()
    assert (np.ones(3) * 2).__class__ is np.ndarray


def test_check_sources():
    v = Tagged.wrap(np.ones(2), {"T:utterance", "latched:b_id"})
    check_sources("q_trace", v, frozenset({"T:", "latched:"}))
    with pytest.raises(TagViolation, match="F:u.LP"):
        check_sources("q_trace", v + Tagged.wrap(1.0, {"F:u.LP"}), frozenset({"T:", "latched:"}))
