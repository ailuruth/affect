"""The shadow run, assembly, ledger wiring and the fail-safes of A1-A9 (spec §1.6, §4.3). Synthetic partners only:
code tests, never evidence about behaviour."""
import numpy as np
import pytest

from engine.config.channels import SMILE_LAUGH, TABLE
from engine.routes.learned_t import Learned, randomise_for_trace
from engine.shadow import assemble as AS
from engine.shadow.shadow import Frame, Run, ShadowPair
from engine.state.body import Session
from engine.state.types import Utterance, heard_at_playback
from synth import partner

FS = 30.0
ONE = np.array([s != "signed" for s in TABLE.signs])
LP = TABLE.index("LP")


def _partner(seconds, seed=0):
    r = np.random.default_rng(seed)
    T = int(seconds * FS)
    U = np.zeros((T, 33))
    for k in range(33):
        u = partner(T, FS, r, 30.0)
        U[:, k] = u if ONE[k] else u - 0.3
    return U


def _b_id(U):
    return np.concatenate([U.mean(0), np.zeros(3)])


def _drive(pair, U, g_at=0.4, words=True, inject=None):
    outs = []
    for n in range(U.shape[0]):
        t = n / FS
        if words and n % int(7 * FS) == int(3 * FS):
            pair.push_utterance(Utterance("him", (), "words %d" % n, t, "words %d" % n))
        if words and n % int(11 * FS) == int(9 * FS):
            pair.push_own_heard(heard_at_playback(["a", "reply"], [t - 0.4, t], "statement", t - 0.8))
        fr = Frame.from_u(t, U[n], g_at)
        if inject is not None:
            inject(pair, n)
        outs.append(pair.step(fr))
    return outs


@pytest.fixture(scope="module")
def clean():
    U = _partner(120)
    pair = ShadowPair(Session(K=0.6), _b_id(U), randomise_for_trace(Learned(), 5))
    return U, pair, _drive(pair, U)


def test_no_assertion_fires_on_a_clean_session(clean):
    U, pair, outs = clean
    assert pair.safety.log == []
    assert not pair.safety.whole_ybar and not pair.safety.channel_ybar.any()


def test_shadow_t_state_equals_factual_although_his_face_differs(clean):
    from engine.invariants.asserts import t_state_digest
    U, pair, _ = clean
    f, s = pair.factual.body.t_fields(), pair.shadow.body.t_fields()
    assert t_state_digest(f) == t_state_digest(s)
    assert not np.array_equal(pair.factual.cone.xi, pair.shadow.cone.xi)      # F state differs


def test_rendered_is_ybar_plus_the_attenuated_partner_part(clean):
    U, pair, outs = clean
    for o in outs:
        r = o.y - o.ybar
        assert np.all(np.abs(o.x2) <= np.abs(r) + 1e-15) and np.all(o.x2 * r >= 0)
        np.testing.assert_array_equal(o.rendered, o.ybar + o.x2)
        lo = np.where(ONE, 0.0, -1.0)
        assert np.all(o.y >= lo) and np.all(o.y <= 1.0)
        assert o.rendered[TABLE.index("BU_S")] == 0.0
        assert set(o.laugh_synth) == {"BU_L", "RHY", "BRE"}


def test_assembly_formula():
    r = np.random.default_rng(0)
    y_f, y_C, y_A, y_o = (r.uniform(-0.2, 0.4, 33) for _ in range(4))
    g, g_o = 0.3, 0.6
    y = AS.assemble(y_f, y_C, y_A, y_o, g, g_o)
    sl = np.zeros(33, bool)
    sl[list(SMILE_LAUGH)] = True
    pre = np.where(sl, g * y_f + g_o * y_o, y_f + y_o) + y_C + y_A
    np.testing.assert_allclose(y, np.clip(pre, np.where(ONE, 0, -1), 1), rtol=0, atol=1e-15)


def test_muscle_filter_unit_dc_and_smoothing():
    m = AS.MuscleFilter(FS)
    x = np.zeros(33)
    out = [m.step(x + (n >= 30) * 0.5) for n in range(300)]
    assert out[-1][LP] == pytest.approx(0.5, abs=1e-9)
    assert 0 < out[31][LP] < 0.25                                   # a 4-Hz second-order muscle, not a jump
    assert out[31][TABLE.index("BU_L")] == 0.5                      # laugh-sound channels pass through


def test_a5_catches_an_f_to_t_leak_and_falls_back():
    U = _partner(40, 1)

    def leak(pair, n):                                              # a bug: the body's h_word reads the F load V_F
        if n == 1:
            for run in (pair.factual, pair.shadow):
                orig = run.slow_tick

                def leaky(inp, u_read, run=run, orig=orig):
                    orig(inp, u_read)
                    object.__setattr__(run.body, "h_word", np.maximum(run.body.h_word, 0.5 * run.V_F))
                run.slow_tick = leaky
    U[:, TABLE.index("BL")] = 0.8
    U[:, TABLE.index("LT")] = 0.8                                   # a glare: factual V_F > 0, shadow V_F = 0
    pair = ShadowPair(Session(), _b_id(U) * 0.0)
    outs = _drive(pair, U, g_at=1.0, inject=leak)
    S = pair.safety
    assert [e[1] for e in S.log][:1] == ["A5"] and S.whole_ybar and S.learning_off and S.build_failed
    t5 = S.log[0][0]
    after = [o for o in outs if o is not None][int((t5 + 1) * FS):]
    assert all(np.array_equal(o.rendered, o.ybar) for o in after)


def test_a1_failsafe_renders_ybar_on_that_channel():
    U = _partner(10, 2)
    pair = ShadowPair(Session(), _b_id(U))
    orig = pair.factual.fast.step
    pair.factual.fast.step = lambda t, u: orig(t, u) * np.where(np.arange(33) == LP, 3.0, 1.0) + (np.arange(33) == LP) * 0.01
    outs = _drive(pair, U, words=False)
    assert pair.safety.channel_ybar[LP] and pair.safety.log[0][1] == "A1"
    assert outs[-1].rendered[LP] == outs[-1].ybar[LP]
    assert not pair.safety.whole_ybar


def test_a2_failsafe_sets_the_gate_to_its_constant():
    U = _partner(5, 3)
    L = Learned()
    L.gates.g.b0 = np.log(1.0)
    pair = ShadowPair(Session(), _b_id(U), L)
    orig = pair.factual.fast_step

    def bad(fr):
        tm = orig(fr)
        if not L.gates.g.disabled:
            tm.g = 1.3
        return tm
    pair.factual.fast_step = bad
    _drive(pair, U, words=False)
    assert ("A2" in [e[1] for e in pair.safety.log]) and L.gates.g.disabled


def test_a8_failsafe_sets_l_d_to_zero():
    U = _partner(5, 4)
    L = Learned()
    pair = ShadowPair(Session(), _b_id(U), L)
    orig = pair.factual.body._tick

    def bad(inp):
        orig(inp)
        v = np.zeros(33)
        v[TABLE.index("TILT")] = 0.6                                # above the 0.45 bound (TILT has a target, D95)
        object.__setattr__(pair.factual.body, "L_d", v)
    pair.factual.body._tick = bad
    _drive(pair, U, words=False)
    assert "A8" in [e[1] for e in pair.safety.log] and L.ld.disabled


def test_a9_failsafe_gates_the_laugh_synth():
    U = _partner(5, 5)
    pair = ShadowPair(Session(), _b_id(U))
    def over(pair, n):                                              # above the own laugh's 0.40 bound
        if n == 2:
            object.__setattr__(pair.factual.body, "env_laugh", np.float64(0.5))
    outs = _drive(pair, U[:4], words=False, inject=over)
    assert not pair.safety.laugh_synth_on and pair.safety.neutral_prosody
    assert all(v == 0.0 for v in outs[-1].laugh_synth.values())


def test_a7_at_load_disables_learned_bases():
    L = Learned()
    L.appraisal.learned_bases[0, TABLE.index("BL"), TABLE.index("BL")] = -0.001    # a masked row
    pair = ShadowPair(Session(), np.zeros(36), L)
    assert pair.safety.log[0][1] == "A7" and np.all(pair.factual.appr.bases[3:] == 0) and L.delta.disabled


def test_ledger_trims_an_uncounted_copy_injected_after_assembly():
    """A gain-1 copy of his LP delayed 20 s added to the factual output only: the ledger sees it as partner-caused
    and attenuates it (never larger, never the other sign)."""
    U = _partner(240, 6)
    pair = ShadowPair(Session(), _b_id(U))
    import engine.shadow.shadow as SH
    orig = SH.assemble
    calls = {"n": 0}

    def inject(*a, **k):
        y = orig(*a, **k)
        calls["n"] += 1
        if calls["n"] % 2 == 1:                                     # the factual call of each frame
            n = calls["n"] // 2
            y = y.copy()
            y[LP] += U[max(0, n - int(20 * FS)), LP] - U[:, LP].mean()
        return y
    SH.assemble = inject
    try:
        outs = _drive(pair, U, words=False)
    finally:
        SH.assemble = orig
    r = np.array([o.y[LP] - o.ybar[LP] for o in outs])
    x2 = np.array([o.x2[LP] for o in outs])
    assert np.all(np.abs(x2) <= np.abs(r) + 1e-15)
    assert pair.ledger.hits[LP] > 0.2 * len(outs)
