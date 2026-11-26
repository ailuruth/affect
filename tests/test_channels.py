"""Channel table and A0 (spec §1.1, §4.3)."""
import dataclasses

import numpy as np
import pytest

from engine.config import channels as ch
from engine.invariants.asserts import InvariantError, check_a0


def test_shape_and_sums():
    t = ch.TABLE
    assert len(t.codes) == 33 == len(set(t.codes))
    assert abs(sum(t.c) - 2.44) < 1e-12
    assert len(ch.ZERO_CEILING) == 13
    assert [t.codes[i] for i in ch.SMILE_LAUGH] == ["LP", "CR", "BU_L", "RHY", "BRE"]


def test_a0_passes_and_totals():
    check_a0(ch.TABLE, ch.POOLED_MAX, ch.N_CHANNELS)
    tot = ch.TABLE.pooled_total()
    assert max(tot) <= 0.974
    assert abs(tot[0] - 0.9737) < 1e-9          # LP is the tightest row


def test_onset_lobe_matches_listed_values():
    t = ch.TABLE
    for code, listed in ch.LISTED_R.items():
        # r6 J2 defines r_k = 0.949 G_k/c_k; the printed table rounds LP's 0.60736 up to 0.608 (0.95 G/c)
        assert abs(t.r[t.index(code)] - listed) <= 0.001
    for k, s in enumerate(t.signs):
        if s != "one_sided":
            assert t.r[k] == 0.0


def test_fast_gains():
    t = ch.TABLE
    for k in range(9, 20):                       # head-gaze and voice: G = 0.80 c
        assert abs(t.G[k] - 0.8 * t.c[k]) < 1e-12
    for k in ch.ZERO_CEILING:
        assert t.G[k] == 0 and t.c[k] == 0


@pytest.mark.parametrize("field,k,val", [("s_C", 0, 0.30), ("G", 20, 0.01), ("s_X", 25, 0.05), ("c", 3, -0.1)])
def test_a0_refuses_broken_tables(field, k, val):
    vals = list(getattr(ch.TABLE, field))
    vals[k] = val
    bad = dataclasses.replace(ch.TABLE, **{field: tuple(vals)})
    with pytest.raises(InvariantError):
        check_a0(bad, ch.POOLED_MAX, ch.N_CHANNELS)


def test_arrays_read_only():
    a = ch.TABLE.array("c")
    with pytest.raises(ValueError):
        a[0] = 1.0
    assert np.array_equal(a, np.array(ch.TABLE.c))
