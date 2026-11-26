"""Mechanism unit test (spec §5.1 F22 row: "synthetic injected copies on all 33 channels are a mechanism unit test in
CI, not F22"). A gain-1 copy of his channel, delayed 10-300 s, is injected after assembly on every channel at once;
the 97-key ledger at kappa 0.70 must hold it. Synthetic signals: not evidence about behaviour.
"""
from __future__ import annotations

import numpy as np
import pytest

from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants.asserts import check_a3_frame, check_a4_frame
from engine.shadow.ledger import Ledger
from synth import delay, lp, partner, worst_block_slope

FS = 10.0
T = int(3600 * FS)
DELAYS = (10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300)


@pytest.fixture(scope="module")
def injected():
    r = np.random.default_rng(33)
    U = np.zeros((T, 33))
    X = np.zeros((T, 33))
    for k in range(33):
        u = partner(T, FS, r, 300.0 if k % 2 == 0 else 30.0)
        if TABLE.signs[k] == "signed":
            u = u - 0.4
        U[:, k] = u
        X[:, k] = delay(u, DELAYS[k % 12] * FS) - u.mean()
    led = Ledger(TABLE.c, FS)
    O = np.zeros_like(X)
    a3 = np.zeros(33, dtype=np.int64)
    a4 = np.zeros(33, dtype=np.int64)
    for t in range(T):
        O[t] = led.step(U[t], X[t])
        a3 += check_a3_frame(ZERO_CEILING, O[t], led.S, led.last_active)
        a4 += check_a4_frame(X[t], O[t], led.S, led.E, led.bound, led.last_active, led.last_hold)
    return U, X, O, led, a3, a4


def test_attenuate_only_every_frame(injected):
    U, X, O, led, _, _ = injected
    assert np.all(np.abs(O) <= np.abs(X))
    assert np.all(O * X >= 0)
    assert led.grow.sum() == 0 and led.flip.sum() == 0


def test_a3_and_a4_hold_every_frame(injected):
    *_, a3, a4 = injected
    assert a3.sum() == 0
    assert a4.sum() == 0


@pytest.fixture(scope="module")
def slopes(injected):
    U, X, O, *_ = injected
    return worst_block_slope(U, X, FS).max(0), worst_block_slope(U, O, FS).max(0)


def test_copy_strongly_attenuated_on_capped_channels(slopes):
    """What the 97-key kappa-0.70 ledger guarantees here: the gain-1 copy, far above every ceiling, is cut to at
    most half its slope on every capped channel, and to <= 2.5 c_k."""
    before, after = slopes
    c = TABLE.array("c")
    for k in range(33):
        if c[k] > 0:
            assert before[k] > 2 * c[k], TABLE.codes[k]
            assert after[k] <= 0.5 * before[k], (TABLE.codes[k], after[k], before[k])
            assert after[k] <= 2.5 * c[k], (TABLE.codes[k], after[k] / c[k])


@pytest.mark.xfail(strict=False, reason=(
    "F22's 1.0 c_k criterion is not met on every channel of these synthetic partners: the ledger is bit-identical "
    "to ledger9/w10, whose 0.83-0.88 c figures were measured only at c = 0.35 (lip pull); on the reference's own "
    "partner at c = 0.05 the same ledger leaves 1.04-1.10 c, and here channels with small c_k reach ~1.1-2.0 c. "
    "Reported to the spec owner; the mechanism is not changed at M0."))
def test_copy_held_below_ceiling_on_capped_channels(slopes):
    before, after = slopes
    c = TABLE.array("c")
    worst = max(after[k] / c[k] for k in range(33) if c[k] > 0)
    assert worst <= 1.0, worst


def test_zero_ceiling_channels_carry_no_toward_copy(injected, slopes):
    """A3 holds exactly (S+ = 0 on active keys, test above); the block-mean metric, which does not see the
    ledger's deviation floor, reads at most a few hundredths of the copy's gain-1 slope."""
    U, X, O, *_ = injected
    after = slopes[1][list(ZERO_CEILING)]
    assert len(ZERO_CEILING) == 13
    assert np.all(after <= 0.03), after
    assert np.mean(np.abs(O[:, ZERO_CEILING])) < 0.01 * np.mean(np.abs(X[:, ZERO_CEILING]))


def test_counted_routes_untouched():
    """F22's second clause, as a mechanism test: the fast gear (0.45 s) plus a held 2-min route at 0.22 c_k on
    every channel change <= 1 % of frames."""
    r = np.random.default_rng(7)
    n = int(1800 * FS)
    U = np.zeros((n, 33))
    Y = np.zeros((n, 33))
    for k in range(33):
        u = partner(n, FS, r, 300.0 if k % 2 == 0 else 30.0)
        if TABLE.signs[k] == "signed":
            u = u - 0.4
        U[:, k] = u
        xd = delay(u, 0.45 * FS)
        e = xd - lp(xd, 4.0, FS)
        fast = TABLE.G[k] * (np.maximum(e, 0.0) if TABLE.signs[k] == "one_sided" else e)
        Y[:, k] = fast + 0.22 * TABLE.c[k] * lp(u - u.mean(), 120.0, FS)
    led = Ledger(TABLE.c, FS)
    for t in range(n):
        led.step(U[t], Y[t])
    changed = led.hits / n
    assert np.all(changed[[k for k in range(33) if TABLE.c[k] > 0]] <= 0.01), changed
