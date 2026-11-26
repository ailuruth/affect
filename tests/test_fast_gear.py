"""The frozen fast gear (spec §1.4, A1): regression against the reference `fast` of sims/design-g9, the pointwise
lemma and per-channel independence. Synthetic arrays only; not evidence about behaviour."""
import numpy as np
import pytest
from scipy.signal import lfilter

import refsims
from engine.config.channels import TABLE
from engine.invariants.asserts import check_a1
from engine.routes.fast_gear import FastGear

N30 = 30 * 60 * 10           # 30 min at 10 Hz


@pytest.fixture(scope="module")
def partners():
    return refsims.g9_partners()


def _run(fg, U, fs, t0=0.0):
    out = np.zeros_like(U)
    for n in range(U.shape[0]):
        out[n] = fg.step(t0 + n / fs, U[n])
    return out


@pytest.mark.parametrize("name", ["u", "u2"])
def test_bit_identical_to_reference_fast_at_10hz(partners, name):
    """At 10 Hz the reference reads x_d with an integer delay int(0.45 fs) = 4 frames; the engine with that delay
    (0.4 s, a whole number of frames) is bit for bit the reference on the lip-pull channel (G 0.224)."""
    ref = refsims.g9(10.0)
    uu = partners[name][:N30]
    y_ref = ref["fast"](uu, 0.224, 0.45)
    fg = FastGear(10.0, G=[0.224], signs=["one_sided"], delay_s=0.4)
    y = _run(fg, uu[:, None], 10.0)[:, 0]
    assert np.array_equal(y, y_ref)


def test_bit_identical_at_20hz_where_045s_is_whole_frames(partners):
    """At 20 Hz 0.45 s is 9 frames: the engine's 0.45-s capture-time read equals the reference's delay exactly."""
    ref = refsims.g9(20.0)
    uu = np.repeat(partners["u"][:6000], 2)
    y_ref = ref["fast"](uu, 0.224, 0.45)
    fg = FastGear(20.0, G=[0.224], signs=["one_sided"])
    assert np.array_equal(_run(fg, uu[:, None], 20.0)[:, 0], y_ref)


def test_30hz_interpolated_delay_matches_the_formula(partners):
    """At 30 Hz 0.45 s is 13.5 frames: x_d is the linear interpolation by capture time (spec §2.2)."""
    fs = 30.0
    uu = np.repeat(partners["u2"][:3000], 3)
    t = np.arange(uu.size) / fs
    xd = np.interp(t - 0.45, t, uu, left=uu[0])
    a = 1 - np.exp(-1 / (4.0 * fs))
    e = xd - lfilter([a], [1, -(1 - a)], xd)
    y_ref = 0.224 * np.maximum(e, 0.0)
    fg = FastGear(fs, G=[0.224], signs=["one_sided"])
    y = _run(fg, uu[:, None], fs)[:, 0]
    np.testing.assert_allclose(y, y_ref, rtol=0, atol=1e-12)


def test_pointwise_lemma_and_a1_on_all_33_channels_irregular_frames():
    r = np.random.default_rng(3)
    fg = FastGear(30.0)
    t = 0.0
    for n in range(3000):
        t += 1 / 30 + r.uniform(-0.004, 0.004)                     # capture-time jitter
        u = r.uniform(0, 1, 33) * (r.uniform() < 0.3)
        u = np.where(np.array(TABLE.signs) == "signed", u - 0.5, u)
        y = fg.step(t, u)
        assert not check_a1(y, fg.last_xd, fg.last_E, fg.G, fg.one_sided).any()
        one = fg.one_sided & (TABLE.array("c") > 0)
        assert np.all(y[one] >= 0) and np.all(y[one] <= fg.G[one] * fg.last_xd[one] + 1e-12)
        assert np.all(y[list(range(20, 33))] == 0.0)                # zero ceiling: G_k = 0


def test_a1_fires_on_a_fast_gear_bug():
    fg = FastGear(30.0)
    for n in range(60):
        y = fg.step(n / 30, np.full(33, 0.4) if n > 30 else np.zeros(33))
    assert check_a1(2.5 * y + 0.01, fg.last_xd, fg.last_E, fg.G, fg.one_sided).any()


def test_each_channel_reads_only_its_own_input():
    r = np.random.default_rng(4)
    U = r.uniform(0, 1, (400, 33))
    base = _run(FastGear(30.0), U, 30.0)
    for j in (0, 5, 9, 14):
        V = U.copy()
        V[:, j] += r.uniform(0, 0.3, 400)
        out = _run(FastGear(30.0), V, 30.0)
        changed = np.nonzero(np.any(out != base, axis=0))[0]
        assert set(changed) <= {j}
