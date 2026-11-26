"""The held cone (spec §1.5.1, A3 (ii), A6): regression against the cone diagonal of sims/design-g5 (H9), centring,
the sets, G0, the reflection rule and the fail-safe. Synthetic arrays only."""
import numpy as np
import pytest

import refsims
from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants.asserts import check_a3_static, check_a6
from engine.routes import cone as C

LP, BI, HG, BL = (TABLE.index(c) for c in ("LP", "BI", "HG", "BL"))
JG = C.N + C.DERIVED.index("f_glare")


@pytest.fixture(scope="module")
def partner():
    return refsims.g9_partners()["u"][:18000]


def _x(u_lp, n_in=C.N_IN):
    X = np.zeros((u_lp.size, n_in))
    X[:, LP] = u_lp
    return X


def test_constants_are_the_references():
    g5 = refsims.g5(10.0)
    assert np.array_equal(C.TAU_M, g5["TAU_M"]) and np.array_equal(C.F_M, g5["F_M"]) and np.array_equal(C.F_BI, g5["F_BI"])


def test_diagonal_matches_reference_h9(partner):
    """y_C,LP = sum_m F_m s_C c lp(u - mean, tau_m) (design-g5 H9) with b_id = his mean and omega = 1."""
    g5 = refsims.g5(10.0)
    uu = partner
    sc, ck = TABLE.s_C[LP], TABLE.c[LP]
    y_ref = sum(g5["F_M"][m] * sc * ck * g5["lp"](uu - uu.mean(), g5["TAU_M"][m], 10.0) for m in range(4))
    cone = C.Cone(10.0)
    b = np.zeros(C.N_IN)
    b[LP] = uu.mean()
    cone.latch(np.ones(4), b)
    X = _x(uu)
    y = np.array([cone.step(X[n])[LP] for n in range(uu.size)])
    np.testing.assert_allclose(y, y_ref, rtol=0, atol=1e-15)


def test_centred_at_b_id_and_latched():
    cone = C.Cone(30.0)
    b = np.random.default_rng(0).uniform(0, 0.5, C.N_IN)
    cone.latch([0.5, 0.3, 0.2, 0.5], b)
    for _ in range(300):
        y = cone.step(b)
    assert np.all(y == 0.0)                     # his own baseline gives nothing: Lemma S* centring


def test_latch_in_its_sets_and_g0_entries():
    cone = C.Cone(30.0)
    G = cone.latch([1.0, -1.0, 0.5, 0.2], np.zeros(C.N_IN))
    assert check_a6(G, cone.omega, cone.S, cone.G0) == []
    assert G[1, LP, JG] == -0.012 and G[2, LP, JG] == -0.0035
    assert G[0, BI, JG] == G[1, BI, JG] == 0.006
    assert G[0, HG, JG] == 0.25 and G[1, HG, JG] == 0.05
    S = C.pair_sign(np.zeros((33, 33)))
    for m in range(4):
        check_a3_static(ZERO_CEILING, G[m], S, "cone")


def test_projection_keeps_learned_entries_in_the_sets():
    r = np.random.default_rng(1)
    prior = np.sign(r.normal(size=(33, 33))) * (r.uniform(size=(33, 33)) < 0.5)
    cone = C.Cone(30.0, dyad_prior=prior)
    cone.learned = 0.2 * r.normal(size=cone.learned.shape)
    G = cone.latch(np.ones(4), np.zeros(C.N_IN))
    assert check_a6(G, cone.omega, cone.S, cone.G0) == []
    for m in range(4):
        check_a3_static(ZERO_CEILING, G[m], cone.S, "cone")
        for k in range(C.N):
            for j in range(C.N_IN):
                if C.is_face_pair(k, j) and G[m, k, j] != 0 and cone.G0[m, k, j] == 0:
                    assert np.sign(G[m, k, j]) == cone.S[k, j]       # face pairs carry the dyad prior's sign


def test_a6_fires_and_falls_back():
    cone = C.Cone(30.0)
    G = cone.latch(np.ones(4), np.zeros(C.N_IN))
    cone.last_valid = G.copy()
    bad = G.copy()
    bad[1, LP, LP] *= 2                          # diagonal not omega F s_C c
    bad[1, BL, LP] = 0.05                        # toward entry on a zero-ceiling row
    assert check_a6(bad, cone.omega, cone.S, cone.G0)
    assert check_a6(G, [1.5, 0, 0, 0], cone.S, cone.G0)            # omega outside [-1, 1]
    cone.G = bad
    cone.fallback()
    assert np.array_equal(cone.G, G)
    cone.last_valid = None
    cone.fallback()
    assert check_a6(cone.G, cone.omega, cone.S, cone.G0) == []


def test_reflection_rule_renders_away_from_his_lateral_trace():
    cone = C.Cone(30.0)
    cone.latch(np.zeros(4), np.zeros(C.N_IN))    # omega 0: only G0
    x = np.zeros(C.N_IN)
    x[JG] = 0.5                                  # a glare
    for side in (+0.2, -0.2):
        cone.latch(np.zeros(4), np.zeros(C.N_IN))
        x[HG] = side
        for _ in range(300):
            y = cone.step(x)
        assert np.sign(y[HG]) == -np.sign(side)  # gaze away, opposite his own horizontal gaze


def test_synergy_signs_within_synergy_only():
    S = C.SYN_SIGN
    assert S[LP, TABLE.index("CR")] == 1 and S[BI, TABLE.index("LD")] == 1
    assert S[BI, TABLE.index("HP")] == -1
    assert S[LP, BI] == 0                        # cross-synergy pair: unsigned (rule J removed, M8)


@pytest.mark.parametrize("prior", [-1.0, 0.0, 1.0])
def test_g0_inside_its_budgets_under_every_prior(prior):
    """review-m4 Part 2: every non-reflected G0 cross entry is charged at weight 1 whatever the dyad prior, so G0
    alone fits its budgets under priors -1, 0 and +1 on every G0 pair, and A6 never fires on G0."""
    dp = np.full((33, 33), prior)
    cone = C.Cone(30.0, dyad_prior=dp)
    G = cone.latch(np.ones(4), np.zeros(C.N_IN))
    assert check_a6(G, cone.omega, cone.S, cone.G0) == []
    for m in range(4):
        ch0, aw0, bad0 = C.g0_usage(cone.G0[m], m)
        budget, _, rcap = C.budgets(m)
        assert bad0 == [] and np.all(ch0 <= budget + 1e-12) and np.all(aw0 <= rcap + 1e-12)
    ch1, _, _ = C.g0_usage(cone.G0[1], 1)
    assert ch1[LP] == 0.012                     # charged at weight 1, not 0 (unsigned face pair) or 0.3


@pytest.mark.parametrize("prior", [-1.0, 0.0, 1.0])
def test_learned_entries_get_only_what_g0_leaves(prior):
    """Learned cross entries on LP (face pairs and non-face pairs) are projected into F_m s_X c_LP minus G0's
    weight-1 use, whatever the prior."""
    dp = np.full((33, 33), prior)
    cone = C.Cone(30.0, dyad_prior=dp)
    r = np.random.default_rng(7)
    cone.learned = np.abs(r.normal(size=cone.learned.shape)) * np.sign(cone.S)[None] * 0.5   # toward signs, large
    cone.learned[:, LP, :] = 0.3 * np.sign(cone.S[LP]) + 0.3 * (cone.S[LP] == 0)
    G = cone.latch(np.ones(4), np.zeros(C.N_IN))
    assert check_a6(G, cone.omega, cone.S, cone.G0) == []
    for m in range(4):
        budget, _, _ = C.budgets(m)
        ch0, _, _ = C.g0_usage(cone.G0[m], m)
        chL, _, bad = C.usage(cone.learned[m], m, cone.S)
        assert bad == []
        assert np.all(chL <= np.maximum(0.0, budget - ch0) + 1e-12)
        assert chL[LP] + ch0[LP] <= budget[LP] + 1e-12


def test_old_g0_size_would_fire_a6():
    """The r5 size (-0.035 on trace 1) is over LP's budget once charged at weight 1: A6 catches it."""
    cone = C.Cone(30.0)
    G = cone.latch(np.ones(4), np.zeros(C.N_IN))
    G0 = cone.G0.copy()
    G0[1, LP, JG] = -0.035
    G = G.copy()
    G[1, LP, JG] = -0.035
    assert any(b[2] == "charged cross budget exceeded" for b in check_a6(G, cone.omega, cone.S, G0) if len(b) == 3)
