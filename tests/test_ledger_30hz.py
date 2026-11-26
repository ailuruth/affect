"""The 30-Hz ledger against its 10-Hz figures (spec §5.1 note; M4 done-check): the sims partners resampled to 30 Hz,
stated tolerance: worst block-mean slopes within +-0.02 c of the 10-Hz figures, frames changed of the counted routes
<= 0.1 %, grow and flip exactly 0. The counted routes are the engine's own fast gear (0.45 s, interpolated at 30 Hz)
and a held 2-min route at 0.22 c (as sims/design-g9 N2). Code regression only; not evidence about behaviour.

Default: the first 30 min of each partner. `pytest -m slow`: the full 2 h at the delays 10, 150, 240, 300 s."""
import numpy as np
import pytest

import refsims
from engine.routes.fast_gear import FastGear
from engine.shadow import ledger as L
from synth import worst_block_slope

C_LP = 0.35


@pytest.fixture(scope="module")
def parts():
    return refsims.g9_partners()


def _to30(u10):
    t10 = np.arange(u10.size) / 10.0
    t30 = np.arange(u10.size * 3) / 30.0
    return np.interp(t30, t10, u10)


def _delay(x, n):
    n = int(n)
    return x.copy() if n <= 0 else np.concatenate([np.full(n, x[0]), x[:-n]])


def _worst(u, y, fs):
    return float(worst_block_slope(u, y, fs, max_lag_s=300.0, lag_step_s=1.0).max()) / C_LP


def _copy_case(u10, lag):
    u30 = _to30(u10)
    out10, h10, g10, f10 = L.run(u10, _delay(u10, lag * 10) - u10.mean(), [C_LP], 10.0)
    out30, h30, g30, f30 = L.run(u30, _delay(u30, lag * 30) - u30.mean(), [C_LP], 30.0)
    assert g10 == f10 == g30 == f30 == 0.0
    w10, w30 = _worst(u10, out10, 10.0), _worst(u30, out30, 30.0)
    assert abs(w30 - w10) <= 0.02, (lag, w10, w30)
    return w10, w30


def _counted(u10):
    u30 = _to30(u10)
    fg = FastGear(30.0, G=[0.224], signs=["one_sided"])
    y_fast = np.array([fg.step(n / 30.0, u30[n:n + 1])[0] for n in range(u30.size)])
    y = y_fast + 0.22 * C_LP * refsims.g9(30.0)["lp"](u30 - u30.mean(), 120.0)
    _, h, g, f = L.run(u30, y, [C_LP], 30.0)
    assert g == f == 0.0
    assert h <= 0.001, h


@pytest.mark.parametrize("name", ["u", "u2"])
def test_counted_routes_at_30hz_30min(parts, name):
    _counted(parts[name][:18000])


@pytest.mark.parametrize("lag", [60, 240])
def test_delayed_copy_30hz_within_002c_of_10hz_30min(parts, lag):
    _copy_case(parts["u"][:18000], lag)


@pytest.mark.slow
@pytest.mark.parametrize("name", ["u", "u2"])
def test_full_2h_counted_routes_at_30hz(parts, name):
    _counted(parts[name])


@pytest.mark.slow
@pytest.mark.parametrize("name,lag", [("u", 10), ("u", 150), ("u", 240), ("u", 300), ("u2", 240)])
def test_full_2h_delayed_copy_30hz_within_002c(parts, name, lag):
    _copy_case(parts[name], lag)
