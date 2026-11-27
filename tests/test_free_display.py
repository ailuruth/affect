"""The free display, L_d, qhat, omega and the derived features (spec §1.5.3, §1.5.5, §1.2.5; A8). Synthetic only."""
import numpy as np
import pytest

from engine.boundary.derived import derived, threat_reflex
from engine.config.channels import TABLE
from engine.invariants.asserts import check_a8
from engine.routes import free_display as FD
from engine.routes import learned_t as LT
from engine.routes.learned_t import Learned, randomise_for_trace
from engine.shadow.shadow import Frame, ShadowPair
from engine.state.body import Body, Session, SlowInputs
from engine.state.types import Utterance

C = {c: TABLE.index(c) for c in TABLE.codes}


def test_pi0_rows_and_the_q33_switch():
    P = FD.pi0_matrix(True)
    rise = FD.DRIVERS.index("rise")
    assert P[C["BI"], rise] == 0.45 and P[C["LD"], rise] == 0.35 and P[C["FR"], rise] == -0.20
    assert FD.pi0_matrix(False)[C["BI"], rise] == 0.0
    laugh = FD.DRIVERS.index("laugh")
    assert P[C["BU_L"], laugh] == 0.40 and P[C["RHY"], laugh] == 0.35
    assert not P[list(FD.MASK_ZERO)].any()                       # Pi_0 never writes the masked channels


def test_rise_envelope_drives_the_brow_and_the_own_laugh_is_bounded():
    L = Learned()
    L.word_v.b[:] = 0.5
    L.qhat.b0 = 50.0                                             # qhat -> 1: own laugh amplitude 0.40
    b = Body(Session(), L)
    fd = FD.FreeDisplay(L.delta)
    b.tick(SlowInputs(0.5, (Utterance("him", (), "x", 0.4, "x"),), (), True))
    y, d = fd.step(b, 0.4 + 1.0)
    S = (0.5 - 0.05) ** 2                                         # the h part of D_V rises by psi(0.5 - 0.05)
    a_d = S / (S + 0.02)
    assert d[FD.DRIVERS.index("rise")] == pytest.approx(a_d)      # on the envelope's apex 0.9 s after the tick
    assert y[C["BI"]] == pytest.approx(0.45 * a_d + 0.25 * 0.5 / 0.65)   # rise row + word-latch row h/(h + 0.15)
    assert d[FD.DRIVERS.index("laugh")] <= 0.40 + 1e-12
    for _ in range(4):
        b.tick(SlowInputs(b.t_his_end + 0.6, (Utterance("him", (), "x", float(b.t_his_end) + 0.5, "x"),), (), True))
    assert FD.FreeDisplay(L.delta).drivers(b, float(b.t_his_end) + 1.0)[FD.DRIVERS.index("laugh")] <= 0.40


def test_inhale_sigh_and_p_name():
    L = Learned()
    b = Body(Session(), L)
    fd = FD.FreeDisplay(L.delta)
    b.pre_speech_inhale(np.float64(2.0))
    assert fd.step(b, 2.1)[0][FD.BRE] == pytest.approx(0.15) and fd.step(b, 2.4)[0][FD.BRE] == 0.0
    b.sigh_t = np.float64(5.0)
    assert fd.step(b, 5.9)[0][FD.BRE] == pytest.approx(0.15)
    b.p_name = np.full(33, 0.05)
    assert fd.step(b, 5.9)[0][FD.BRE] == pytest.approx(0.15 * 0.95)


def test_delta_respects_the_own_display_mask():
    dl = FD.DisplayDelta()
    r = np.random.default_rng(0)
    dl.W1, dl.W2, dl.syn = (r.normal(size=a.shape) for a in (dl.W1, dl.W2, dl.syn))
    y = dl(r.normal(size=161), 0.0)
    assert np.all(y[list(FD.MASK_ZERO)] == 0) and np.all(y[list(FD.MASK_RISE_ONLY)] == 0)
    assert np.all(np.abs(y) <= 0.3 * np.abs(dl.syn).sum(0) + 1e-12)
    assert dl.mask_violations()                                   # the raw synergy matrix itself writes them: A7


FACE_ONLY = {"FAUValue", "is_valid", "transcript"}
ALL_STREAMS = FACE_ONLY | {"head_pose", "gaze", "voice_features"}


def test_listener_display_form_bound_and_zero_rows():
    """D95: every stream approved, so L_d has 11 output rows (BI, BO, LD, LP, CR, RT, HP, VG, TILT, FR, EN)."""
    ld = LT.ListenerDisplay()
    assert ld.W.shape == (11, 140) and LT.LD_ZERO_ROWS == ()
    assert [TABLE.codes[k] for k in ld.out] == ["BI", "BO", "LD", "LP", "CR", "RT", "HP", "VG", "TILT", "FR", "EN"]
    assert np.all(ld(ld.features(np.array([0.5, 0.2, 0.1]), np.zeros(3), 3.1, 30.0)) == 0)    # untrained: L_d = 0
    ld.W = 5.0 * np.random.default_rng(1).normal(size=ld.W.shape)
    phi = ld.features(np.array([0.5, 0.2, 0.1]), np.array([0.3, 0.0, 0.1]), 3.1, 30.0)
    assert phi.shape == (140,) and phi.sum() > 0
    v = ld(phi)
    assert np.abs(v).max() <= 0.45 and check_a8(v, ld.W) == []
    assert np.all(v[[C[c] for c in ("TILT", "HP", "VG", "FR", "EN")]] != 0)
    others = [k for k in range(33) if k not in ld.out]
    assert np.all(v[others] == 0)
    assert np.all(ld(ld.features(np.zeros(3), np.zeros(3), None, 25.0)) == 0)    # no event in the last 20 s
    assert check_a8(np.full(33, 0.5))


@pytest.mark.parametrize("removed, zero", [
    ({"head_pose", "gaze", "voice_features"}, ["HP", "VG", "TILT", "FR", "EN"]),
    ({"head_pose"}, ["HP", "TILT"]),
    ({"gaze"}, ["VG"]),
    ({"voice_features"}, ["FR", "EN"]),
    (set(), []),
])
def test_listener_display_zero_rows_follow_dyad_streams(removed, zero):
    streams = ALL_STREAMS - removed
    out, zr = LT.listener_display_rows(streams)
    assert [TABLE.codes[k] for k in zr] == zero
    assert not set(out) & set(zr) and len(out) == 11 - len(zero)
    ld = LT.ListenerDisplay(streams)
    assert ld.W.shape == (11 - len(zero), 140)
    ld.W = 5.0 * np.random.default_rng(2).normal(size=ld.W.shape)
    v = ld(ld.features(np.array([0.5, 0.2, 0.1]), np.array([0.3, 0.0, 0.1]), 3.1, 30.0))
    assert np.all(v[list(zr)] == 0) and check_a8(v, ld.W, streams) == []
    for c in zero:                                                  # a written row without its stream: A8
        bad = v.copy()
        bad[C[c]] = 0.01
        assert (c, "row without an approved dyad stream is not 0") in check_a8(bad, streams=streams)
    if zero:                                                        # weights fitted for a wider scope: A8
        assert ("W", "rows do not match the approved dyad streams") in check_a8(v, LT.ListenerDisplay().W, streams)


def test_listener_display_never_writes_the_own_display_mask():
    mask = FD._MASK["zero"] + FD._MASK["own_rise_only"]
    for streams in (FACE_ONLY, ALL_STREAMS):
        out, _ = LT.listener_display_rows(streams)
        assert not {TABLE.codes[k] for k in out} & set(mask)


@pytest.mark.parametrize("streams, n_in", [
    (FACE_ONLY, 4 + 2 * 23),
    (FACE_ONLY | {"head_pose"}, 4 + 2 * 23 + 2 * 3),
    (FACE_ONLY | {"gaze"}, 4 + 2 * 23 + 2 * 2),
    (FACE_ONLY | {"voice_features"}, 4 + 2 * 23 + 2 * 2),
    (ALL_STREAMS, 4 + 2 * 23 + 2 * 7),
])
def test_turn_model_input_shape(streams, n_in):
    tm = LT.TurnModel(streams)
    assert tm.N_IN == n_in == len(tm.inputs) == len(set(tm.inputs))
    assert tm.w_end.shape == tm.w_haz.shape == (n_in + 1,)
    assert np.all(tm.w_end == 0) and np.all(tm.w_haz == 0) and not tm.trained
    assert tm.p_end(np.ones(n_in)) == 0.5                          # untrained: weights 0
    assert tm.hazard(np.ones(n_in)) == LT.ENTRIES["hazard_without_fit_per_s"].value
    if "head_pose" in streams:
        assert {"p0_HP", "p1_YAW", "p1_TILT"} <= set(tm.inputs)
    if "voice_features" in streams:
        assert {"p0_F0", "p1_FR"} <= set(tm.inputs)
    assert LT.TurnModel().N_IN == 4 + 2 * 23 + 2 * 7               # the operator's current scope (D95)


def test_omega_rule():
    assert LT.omega_target(0.6, 0.0) == pytest.approx(1.0)
    assert LT.omega_target(0.0, 0.10) == pytest.approx(-1.0)
    om = LT.omega_update(LT.OMEGA_PRIOR, 1.0)
    np.testing.assert_allclose(om, LT.OMEGA_PRIOR + (1.0 - LT.OMEGA_PRIOR) / 60.0)


def test_derived_features_and_threat_reflex():
    u = np.zeros(33)
    u[[C["BL"], C["LT"]]] = 0.8
    f = derived(u, 1.0)
    assert f[2] == pytest.approx(0.64) and threat_reflex(f) == pytest.approx(0.64)
    u[[C["LP"], C["CR"]]] = 0.6                                  # a Duchenne smile: loud praise is not a threat
    u[C["EN"]] = 1.0
    u[[C["BL"], C["LT"]]] = 0.0
    assert threat_reflex(derived(u, 1.0)) == 0.0


def test_t_routes_do_not_move_with_his_face():
    """F5 as a mechanism check: scaling his LP and CR (words and turns fixed) changes no T field and not y_o."""
    from engine.invariants.asserts import t_state_digest
    r = np.random.default_rng(2)
    U = r.uniform(0, 0.6, (900, 33))
    digests = []
    for scale in (0.0, 0.5, 2.0):
        V = U.copy()
        V[:, [C["LP"], C["CR"]]] *= scale
        pair = ShadowPair(Session(K=0.5), np.concatenate([U.mean(0), np.zeros(3)]), randomise_for_trace(Learned(), 7))
        y_o = []
        for n in range(900):
            if n % 200 == 50:
                pair.push_utterance(Utterance("him", (), "w %d" % n, n / 30, "w %d" % n))
            o = pair.step(Frame.from_u(n / 30, np.clip(V[n], 0, 1), 0.3))
            y_o.append(pair.factual.last_terms.y_o)
        digests.append((t_state_digest(pair.factual.body.t_fields()), t_state_digest({"y_o": y_o})))
    assert digests[0] == digests[1] == digests[2]
