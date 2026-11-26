"""The appraisal display (spec §1.5.2, A3 (ii), A7): regression of the band-pass against sims/design-g5 bp, zero DC,
the design's step and sup figures, 2-Hz evaluation with interpolation, the sets and the fail-safe. Synthetic only."""
import numpy as np
import pytest

import refsims
from engine.config.channels import APPRAISAL_SUP, TABLE, ZERO_CEILING
from engine.invariants.asserts import check_a3_static, check_a7
from engine.routes import appraisal as AP
from engine.routes.cone import N, N_IN

LP, HG, EN, BL = (TABLE.index(c) for c in ("LP", "HG", "EN", "BL"))


def _run_bp(x, fs, b=0.0):
    a = AP.Appraisal(fs, AP.AppraisalNet())
    bid = np.zeros(N_IN)
    bid[LP] = b
    a.latch(np.ones(4), bid)
    X = np.zeros(N_IN)
    out = np.zeros(x.size)
    for n in range(x.size):
        X[LP] = x[n]
        a.step(n / fs, X)
        out[n] = a.xi_A[LP]
    return out


def test_band_pass_matches_reference_bp():
    uu = refsims.g9_partners()["u2"][:12000]
    g5 = refsims.g5(10.0)
    ref = g5["bp"](uu - uu.mean())
    np.testing.assert_allclose(_run_bp(uu, 10.0, uu.mean()), ref, rtol=0, atol=1e-15)


def test_zero_dc_and_the_design_step_response():
    """xi_A has no DC: a held step returns to 0; its peak is 0.505 at about 39 s (r5 §2.6)."""
    fs = 10.0
    y = _run_bp(np.ones(int(600 * fs)), fs)
    assert abs(y.max() - 0.505) < 0.002 and abs(np.argmax(y) / fs - 39.0) < 1.5
    assert abs(y[-1]) < 0.01


def test_sup_gain_is_0636():
    w = np.logspace(-4, 1, 20000)
    H = 1 / (1 + 1j * w * 20.0) - 1 / (1 + 1j * w * 90.0)
    assert abs(np.abs(H).max() - APPRAISAL_SUP) < 5e-4


def test_innate_bases_in_their_sets_and_zero_ceiling_rows_away_only():
    om = [1.0, 0.3, 0.2, 0.5]
    B = AP.innate_bases(om)
    S = AP.pair_sign(np.zeros((33, 33)))
    assert check_a7(B, om, S) == []
    assert B[1, LP, LP] == TABLE.s_A[LP] * TABLE.c[LP] * 1.0
    assert B[2, EN, N] == -0.10 and B[2, HG, N] == 0.10
    for r in range(3):
        check_a3_static(ZERO_CEILING, B[r], S, "appraisal")


def test_learned_basis_projection_and_a7():
    r = np.random.default_rng(2)
    om = np.ones(4)
    S = AP.pair_sign(np.sign(r.normal(size=(33, 33))))
    raw = 0.3 * r.normal(size=(N, N_IN))
    bases = np.concatenate([AP.innate_bases(om), raw[None], np.zeros((1, N, N_IN))])
    assert check_a7(bases, om, S)                                    # raw: outside the set, mask rows written
    bases[3] = AP.project_basis(raw, om, S)
    assert check_a7(bases, om, S) == []
    assert np.all(bases[3][list(AP.MASK_ZERO)] == 0)
    check_a3_static(ZERO_CEILING, bases[3], S, "appraisal")


def test_two_hz_display_and_interpolation():
    fs = 30.0
    net = AP.AppraisalNet()
    a = AP.Appraisal(fs, net)
    a.latch(np.ones(4), np.zeros(N_IN))
    X = np.zeros(N_IN)
    vals, ticks = [], []
    for n in range(int(60 * fs)):
        t = n / fs
        X[LP] = 0.3 if t > 5 else 0.0
        if n % 15 == 0:
            w = a.tick(t, np.zeros(64), np.zeros(7), np.zeros(N))
            assert np.allclose(w, 0.2)                                # untrained selection: uniform over 5 bases
            ticks.append((t, a.y_A_tick[LP], a.xi_A[LP]))
        vals.append(a.step(t, X)[LP])
    # at a tick the frame shows the previous tick's value, reaching the current one 0.5 s later (causal)
    assert vals[15 * 40] == pytest.approx(ticks[39][1], abs=1e-12)
    gain = 0.2 * TABLE.s_A[LP] * TABLE.c[LP]                        # weight 1/5 on basis_return_LP_CR, omega 1
    for _, y_tick, xi in ticks[1:]:
        assert y_tick == pytest.approx(gain * xi, abs=1e-15)
    assert max(abs(v) for v in vals) <= 0.636 * TABLE.s_A[LP] * TABLE.c[LP] * 0.3 + 1e-9


def test_disable_learned_is_the_a7_failsafe():
    a = AP.Appraisal(30.0, AP.AppraisalNet())
    a.net.learned_bases[:] = 0.01
    a.latch(np.ones(4), np.zeros(N_IN))
    assert np.any(a.bases[3:] != 0)
    a.disable_learned()
    assert np.all(a.bases[3:] == 0)
