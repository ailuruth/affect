"""The scaled safety net's governor, revision 2 (engine/shadow/governor.py; design-scaled-safety-net.md §7.2, §7.7;
Q35, D104). Code and mechanism tests on constructed signals; never evidence about behaviour or people.

Reference: `Governor2` of research/foundations/sims/scaled-safety-net/rev2_lib.py (loaded verbatim through
tests/refsims.py), at its own rate of 10 Hz.
"""
from __future__ import annotations

import numpy as np
import pytest

import refsims
from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants.asserts import check_a4g_frame
from engine.shadow.governor import GOVERNOR, Governor, build_net, evidence_floor, t_multiplier
from engine.shadow.ledger import Ledger
from synth import worst_block_slope

FS = 10.0
R = refsims.rev2_lib()
CAPPED = [k for k in range(33) if TABLE.c[k] > 0]


def _run(gov, U, X, led=None):
    T, n = X.shape
    O = np.zeros_like(X)
    A = np.zeros_like(X)
    Ap = np.zeros_like(X)
    for t in range(T):
        x = gov.step(U[t], X[t])
        A[t], Ap[t] = gov.a, gov.prev_a
        O[t] = led.step(U[t], x) if led is not None else x
    return O, A, Ap


def _mixed(T, seed=3):
    """8 columns: copies of several gains and delays (causal, from b_id), one away copy, one zero-ceiling copy."""
    U = R.partners_fast(8, seed, T=T)
    u0 = R.engine_baseline(8, seed)
    c = np.array([0.03, 0.05, 0.10, 0.35, 0.0, 0.05, 0.10, 0.20])
    g = np.array([33.0, 10.0, 3.0, 1.5, 1.0, -5.0, 0.3, 5.0])          # slope / c (0.05 absolute on the zero row)
    D = np.array([30.0, 47.35, 90.0, 213.7, 10.0, 30.0, 60.0, 0.45])
    X = np.stack([g[j] * (c[j] if c[j] > 0 else 0.05) * R.causal_copy(U[:, j], D[j], u0[j]) for j in range(8)], 1)
    return U, X, c, u0


# ------------------------------------------------------------------------------------------------ constants
def test_constants_match_the_reference_settings():
    p = R.GOV2
    for k in ("kappa_g", "z", "t_crit", "n_req", "sigma0", "taus", "sets", "batch_W", "start_W", "max_lag_s",
              "ratchet"):
        assert GOVERNOR[k] == p[k], k
    assert p["prov_n"] is None                       # the provisional gain was not adopted (§7.6)
    assert GOVERNOR["rate_hz"] == 10.0
    keys = sum(len(range(0, 301, int(s))) for _, _, s in GOVERNOR["sets"])
    assert keys == 153 and len(GOVERNOR["taus"]) == 3


def test_t_multiplier_against_tabulated_quantiles():
    """Student's t at one-sided p = 0.00135 (z = 3): df 3 9.2189, df 10 3.9569, df 30 3.2703 (tabulated). The
    Cornish-Fisher expansion is within a few % at df 3 and below the exact value there."""
    tab = {3: 9.218940, 10: 3.956937, 30: 3.270334}
    for df, q in tab.items():
        got = float(t_multiplier(3.0, df))
        assert abs(got - q) / q <= (0.03 if df == 3 else 0.002), (df, got, q)
    assert t_multiplier(3.0, 3) < tab[3]
    assert np.all(np.diff(t_multiplier(3.0, np.arange(1.0, 60.0))) < 0)


# ------------------------------------------------------------------------------------------------ regression
@pytest.fixture(scope="module")
def mixed():
    T = int(1200 * FS)
    U, X, c, u0 = _mixed(T)
    ref = R.Governor2(c, u0)
    Oref = np.stack([ref.step(U[t], X[t]) for t in range(T)])
    gov = Governor(c, FS, u0)
    O, A, Ap = _run(gov, U, X)
    return dict(U=U, X=X, c=c, u0=u0, ref=ref, Oref=Oref, gov=gov, O=O, A=A, Ap=Ap)


def test_bit_identical_to_rev2_lib_governor2_at_10hz(mixed):
    m = mixed
    assert np.array_equal(m["O"], m["Oref"]), np.abs(m["O"] - m["Oref"]).max()
    assert np.array_equal(m["gov"].a, m["ref"].a)
    assert np.array_equal(m["gov"].first, m["ref"].first)
    assert np.array_equal(m["gov"].engaged, m["ref"].engaged.astype(np.int64))
    for S, Sr in zip(m["gov"].sets, m["ref"].sets):
        for i, s in enumerate(Sr["mem"]):
            for key in ("C", "E", "A11", "A12", "A22", "Eb", "beta", "se", "neff", "latch"):
                assert np.array_equal(S[key][i], s[key]), (S["w"], S["kind"], i, key)
    assert (m["A"][-1] < 1).sum() >= 5                # the copies above the target were caught


def test_net_bit_identical_to_rev2_lib_run2_with_floor(mixed):
    """Governor -> ledger with the evidence floor E0 = 0.54, against rev2_lib.run2(..., led_E0=0.54)."""
    m = mixed
    Oref, *_ = R.run2(m["U"], m["X"], m["c"], m["u0"], net="new", led_E0=0.54)
    O, _, _ = _run(Governor(m["c"], FS, m["u0"]), m["U"], m["X"], Ledger(m["c"], FS, evidence_floor=0.54))
    assert np.array_equal(O, Oref), np.abs(O - Oref).max()


def test_attenuate_only_exact_product_and_ratchet_every_frame(mixed):
    m = mixed
    X, O, A, Ap = m["X"], m["O"], m["A"], m["Ap"]
    assert np.all((A >= 0) & (A <= 1))
    assert np.all(O == A * X)                                     # x = a r exactly
    assert np.all(np.abs(O) <= np.abs(X)) and np.all(O * X >= 0)
    assert np.all(np.diff(A, axis=0) <= 0)                        # the ratchet: a never rises within a session
    assert np.all(A <= Ap)
    away = 5                                                      # an away copy (negative slope) is never touched
    assert np.all(A[:, away] == 1.0)


def test_a4g_silent_on_the_governor_and_firing_on_violations(mixed):
    m = mixed
    gov = Governor(m["c"], FS, m["u0"])
    zero = [4]
    for t in range(m["U"].shape[0]):
        x = gov.step(m["U"][t], m["X"][t])
        assert not check_a4g_frame(m["X"][t], x, gov.a, gov.prev_a, gov.ever_latched, zero).any(), t
    r = np.array([0.1, 0.1, 0.1])
    a = np.array([0.5, 1.0, 0.5])
    assert list(check_a4g_frame(r, a * r, a, np.ones(3), np.array([True, False, False]), [2])) == [False, False, True]
    assert check_a4g_frame(r, a * r, a, np.array([0.4, 1, 1]), np.ones(3, bool), [])[0]      # a rose
    assert check_a4g_frame(r, r, a, np.ones(3), np.ones(3, bool), [])[0]                    # x != a r
    assert check_a4g_frame(r, a * r, a, np.ones(3), np.array([False, True, True]), [])[0]   # a < 1, never latched


def test_lemma0_exact_homogeneity():
    """Scale the ceilings and the partner-caused part by 8: a identical, output x 8, exactly (governor and ledger)."""
    T = 6000
    U = R.partners_fast(4, 3, T=T)
    c = np.array([0.03, 0.05, 0.10, 0.35])
    u0 = R.engine_baseline(4, 3)
    X = np.stack([5 * c[j] * R.causal_copy(U[:, j], 30.0, u0[j]) for j in range(4)], 1)
    O1, A1, _ = _run(Governor(c, FS, u0), U, X, Ledger(c, FS, evidence_floor=0.54))
    O8, A8, _ = _run(Governor(8 * c, FS, u0), U, 8 * X, Ledger(8 * c, FS, evidence_floor=0.54))
    assert (A1[-1] < 1).all()
    assert np.array_equal(A1, A8)
    assert np.array_equal(O8, 8 * O1)


# ------------------------------------------------------------------------------------------------ evidence rule
def test_no_sums_before_lag_plus_two_windows():
    T = int(420 * FS)
    U = R.partners_fast(3, 5, T=T)
    X = 0.2 * (U - U.mean(0))
    gov = Governor(np.array([0.05, 0.10, 0.0]), FS, U.mean(0))
    for t in range(T):
        gov.step(U[t], X[t])
        if t % 7 == 0 or t == T - 1:
            k = gov.t - 1                                         # the tick just taken
            for S in gov.sets:
                counted = k >= S["start"]
                assert np.array_equal(S["Wt"][:, 0, :] > 0, np.broadcast_to(counted, S["Wt"][:, 0, :].shape))
                for key in ("C", "E", "bP", "bE", "A22", "Eb"):
                    assert np.all(S[key][:, :, ~counted] == 0.0), (S["w"], S["kind"], key, t)
    assert gov.sets[2]["start"][-1] == int((300 + 120) * FS)       # 60-s level key at lag 300 s counts from 420 s


def test_one_large_step_counts_as_one_batch():
    """§7.1 item 7(b): the evidence is the effective number of independent batches n = (sum w_b E_b)^2 /
    sum w_b^2 E_b^2, so one large movement of his counts as about one batch however large it is. He sits still (noise
    1e-3) except for a 1-s step up and back at 600 s (on a batch boundary), which the partner-caused part copies at
    10 c_k (its own noise independent). On the long-memory 10-s keys at lag 0 the slope is far above the target, the
    evidence stays near 1 batch for a step of 0.35 and of 0.70 alike, and the governor never engages."""
    c = np.array([0.05])
    T = int(1200 * FS)
    seen = {}
    for A in (0.35, 0.70):
        rng = np.random.default_rng(0)
        U = 0.20 + 1e-3 * rng.standard_normal((T, 1))
        X = 1e-3 * rng.standard_normal((T, 1))
        U[6000:6010] += A
        X[6000:6010] += 10 * c[0] * A
        gov = Governor(c, FS, np.array([0.20]))
        for t in range(T):
            gov.step(U[t], X[t])
            if t == int(660 * FS):
                seen[A] = [(float(S["beta"][0, 0, 0]), float(S["neff"][0, 0, 0])) for S in gov.sets[:2]]
        assert gov.engaged.sum() == 0 and gov.a[0] == 1.0, (A, gov.latched_key())
    for A, rows in seen.items():
        for beta, n in rows:
            assert n < 1.2, (A, rows)
    assert seen[0.70][0][0] > 5 * GOVERNOR["kappa_g"] * c[0]
    for (b1, n1), (b2, n2) in zip(seen[0.35], seen[0.70]):
        assert abs(n1 - n2) < 0.01, (seen,)


# ------------------------------------------------------------------------------------------------ zero ceiling
def test_zero_ceiling_channels():
    """c_k = 0: a toward copy sets a_k to 0 once a key latches (a in {0, 1} on every frame, x = 0 after); no
    partner-caused part leaves a_k = 1. Not asserted, by design (§7.2: the target is 0 at every key): an away copy, or
    a partner-caused part unrelated to his movement, also latches some key among the 459 on a zero-ceiling channel
    (a lag where his movement anticorrelates, or chance across the keys) and is then held at 0 for the session."""
    T = int(1200 * FS)
    U = R.partners_fast(3, 11, T=T)
    u0 = R.engine_baseline(3, 11)
    c = np.zeros(3)
    X = np.stack([0.05 * R.causal_copy(U[:, 0], 10.0, u0[0]), 0.05 * R.causal_copy(U[:, 1], 60.0, u0[1]),
                  np.zeros(T)], 1)
    gov = Governor(c, FS, u0)
    O, A, _ = _run(gov, U, X)
    assert set(np.unique(A)) <= {0.0, 1.0}
    assert A[-1, 0] == 0.0 and gov.first[0] > 10.0
    t0 = int(np.argmax(A[:, 0] == 0.0))
    assert np.all(O[t0:, 0] == 0.0)
    assert A[-1, 1] == 0.0
    assert np.all(A[:, 2] == 1.0)


# ------------------------------------------------------------------------------------------------ rates and wiring
def test_30hz_updates_every_third_frame_and_tracks_10hz():
    T10 = int(900 * FS)
    U10 = R.partners_fast(3, 4, T=T10)
    c = np.array([0.05, 0.10, 0.35])
    u0 = R.engine_baseline(3, 4)
    X10 = np.stack([g * c[j] * R.causal_copy(U10[:, j], 30.0, u0[j]) for j, g in enumerate((10.0, 3.0, 2.0))], 1)
    t10, t30 = np.arange(T10) / 10.0, np.arange(3 * T10) / 30.0
    U30 = np.stack([np.interp(t30, t10, U10[:, j]) for j in range(3)], 1)
    X30 = np.stack([np.interp(t30, t10, X10[:, j]) for j in range(3)], 1)
    g10, g30 = Governor(c, 10.0, u0), Governor(c, 30.0, u0)
    _run(g10, U10, X10)
    O30, A30, _ = _run(g30, U30, X30)
    assert g30.t == T10 and g30.every == 3
    assert np.all(A30[1::3] == A30[0::3]) and np.all(A30[2::3] == A30[0::3])     # a held between updates
    assert np.all(O30 == A30 * X30)
    assert np.all(g10.a < 1) and np.all(g30.a < 1)
    assert np.all(np.abs(g30.a / g10.a - 1) < 0.15), (g10.a, g30.a)
    with pytest.raises(ValueError):
        Governor(c, 25.0, u0)


def test_net_modes_and_the_operator_switch():
    from engine.shadow.shadow import ShadowPair
    from engine.state.body import Session
    from engine.config.operator import SWITCHES
    assert SWITCHES["safety_net"].value == "scaled_rev2_with_floor" and SWITCHES["safety_net"].answered
    gov, led = build_net(TABLE.c, 30.0, np.zeros(33))
    assert isinstance(gov, Governor) and led.E0 == evidence_floor(30.0) == pytest.approx(1.62)
    assert np.all(led.E == 1e-9 + led.E0)
    gov, led = build_net(TABLE.c, 10.0, np.zeros(33), "ledger_only")
    assert gov is None and led.E0 == 0.0 and np.all(led.E == 1e-9)
    gov, led = build_net(TABLE.c, 10.0, np.zeros(33), "scaled_rev2")
    assert gov is not None and led.E0 == 0.0
    with pytest.raises(ValueError):
        build_net(TABLE.c, 10.0, np.zeros(33), "monitor")
    b = np.concatenate([np.full(33, 0.2), np.zeros(3)])
    pair = ShadowPair(Session(), b)
    assert pair.governor is not None and np.array_equal(pair.governor.u0, b[:33])     # started at b_id, not a mean
    assert ShadowPair(Session(), b, net_mode="ledger_only").governor is None


# ------------------------------------------------------------------------------------------------ natural partners
@pytest.fixture(scope="module")
def partners_1h():
    """One batched 1-h run, governor -> ledger with the floor:
      K6 (rev2_check.py R5): seed 8, and seed 10 livelier (30-s blocks on every channel), counted routes only, with the
         neutral input set 0.10 below and above his session mean (capped channels);
      R4: the counted routes running high at 0.50 c and 0.85 c on c = 0.03, 0.05, 0.10, 0.35 (partners of seed 77)."""
    T = int(3600 * FS)
    Us, Xs, u0s, cs, tags = [], [], [], [], []
    for seed in (8, 10):
        if seed == 10:
            r10 = np.random.default_rng(10)
            Un = np.stack([R.partner(T, r10, 30.0) - (0.4 if R.SIGNED[k] else 0) for k in range(33)], 1)
        else:
            Un = R.partners_fast(33, 8, T=T, signed=R.SIGNED)
        for dl in (-0.10, 0.10):
            u0 = Un.mean(0) + dl
            Y = R.counted_routes(Un, u0, R.CEIL, R.GAIN, R.SIGNED)
            Us.append(Un[:, CAPPED]); Xs.append(Y[:, CAPPED]); u0s.append(u0[CAPPED]); cs.append(R.CEIL[CAPPED])
            tags += [("K6", seed, dl)] * len(CAPPED)
    SS = (0.50, 0.70, 0.85, 0.974)
    CS = (0.03, 0.05, 0.10, 0.35)
    Ux = R.partners_fast(16, 77, T=T)
    u0x = R.engine_baseline(16, 77)
    for ci, cc in enumerate(CS):
        for si in (0, 2):
            j = ci * 4 + si
            Us.append(Ux[:, j:j + 1]); u0s.append(u0x[j:j + 1]); cs.append(np.array([cc]))
            Xs.append((SS[si] * cc * R.causal_copy(Ux[:, j], 0.45, u0x[j]))[:, None])
            tags.append(("R4", cc, SS[si]))
    U, X, u0, c = np.concatenate(Us, 1), np.concatenate(Xs, 1), np.concatenate(u0s), np.concatenate(cs)
    gov = Governor(c, FS, u0)
    O, A, _ = _run(gov, U, X, Ledger(c, FS, evidence_floor=evidence_floor(FS)))
    return dict(U=U, X=X, O=O, A=A, c=c, gov=gov, tags=tags)


def test_natural_partners_not_engaged(partners_1h):
    """K6: counted routes only, neutral input 0.10 off his mean either way: a = 1 on every frame (design §7.4: 0.00 %
    on all four; revision 1: 4.3 %). The 8 partners of seeds 7-14 with b_id: tests/test_ledger_injected.py
    test_counted_routes_untouched."""
    m = partners_1h
    k6 = np.array([t[0] == "K6" for t in m["tags"]])
    assert m["gov"].engaged[k6].sum() == 0 and np.all(m["A"][:, k6] == 1.0)


def test_counted_routes_running_high_are_trimmed(partners_1h):
    """R4: counted routes at 0.85 c_k (an extreme but legal partner) are trimmed to <= 0.65 c_k (design §7.4:
    0.52-0.61 c); at 0.50 c_k nothing is touched."""
    m = partners_1h
    for j, tag in enumerate(m["tags"]):
        if tag[0] != "R4":
            continue
        _, cc, s = tag
        w = float(worst_block_slope(m["U"][:, j], m["O"][:, j], FS).max()) / cc
        if s == 0.50:
            assert m["gov"].engaged[j] == 0, tag
        else:
            assert m["A"][-1, j] < 1.0 and w <= 0.65, (tag, w, m["A"][-1, j])
