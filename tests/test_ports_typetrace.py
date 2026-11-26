"""OwnHeard, the five ports P1-P5 and the type trace (spec §1.3.1, §4.4; F19 by construction).

The trace runs a synthetic session; the tests check that it passes on the engine, that it refuses an Ω read outside
a port, an F -> T leak and a gate reading a channel it may not read, and that the committed downstream(Pi) equals a
fresh trace. The F19-style checks diff every T field bit for bit. Synthetic only; not evidence about behaviour."""
import dataclasses

import numpy as np
import pytest

from engine.invariants import typetrace
from engine.invariants.tagged import TagViolation, Tagged
from engine.routes.learned_t import Learned, randomise_for_trace
from engine.shadow.shadow import Run
from engine.state import ports
from engine.state.body import Body, Session, SlowInputs
from engine.state.types import OwnHeard, Utterance, heard_at_playback


# ------------------------------------------------------------------------------------------------- OwnHeard
def test_own_heard_only_at_playback_and_truncated_at_interruption():
    with pytest.raises(TypeError):
        OwnHeard(("x",), (1.0,), "statement", 0.0, 1.0, False)
    oh = heard_at_playback(["one", "two", "three"], [1.0, 1.5, 2.0], "question", 0.5, t_played_until=1.6)
    assert oh.words == ("one", "two") and oh.interrupted and oh.t_end == 1.5
    full = heard_at_playback(["one"], [1.0], "statement", 0.5)
    assert not full.interrupted and full.t_end == 1.0


def test_ports_outputs_and_bounds():
    L = randomise_for_trace(Learned(), 1)
    L.pname.b[:] = 1.0                                      # saturate: P4 stays <= 0.05
    oh = heard_at_playback(["are", "you", "there"], [1.0, 1.2, 1.4], "question", 0.6)
    assert ports.p_name(oh, L.enc, L.pname).max() <= 0.05
    assert float(ports.turn_question_bit(oh, True)) == 1.0 and float(ports.turn_question_bit(oh, False)) == 0.0
    ts, te, ev = ports.own_turn_events(oh)
    assert (float(ts), float(te)) == (0.6, 1.4) and [e.kind for e in ev] == ["agent_utterance_start", "agent_utterance_end"]
    np.testing.assert_array_equal(np.asarray(ports.lambda_own(oh, L.enc, L.lam)),
                                  np.asarray(ports.qhat_agent_turn(oh, L.enc, L.lam))[0])
    with pytest.raises(TypeError):
        ports.lambda_own("not heard", L.enc, L.lam)


# ------------------------------------------------------------------------------------------------- the trace
@pytest.fixture(scope="module")
def record():
    return typetrace.run_trace(60.0)


def test_trace_passes_and_every_display_term_checked(record):
    assert {"display:" + n for n in ("y_f", "y_C", "y_A", "y_o", "g", "g_o")} <= set(record)
    assert not any(t.startswith("F:") for t in record["display:y_o"])
    assert not any(t.startswith(("F:", "O:")) for t in record["display:g_o"])
    assert not {"F:u.LP", "F:u.CR", "F:u.BU_L", "F:u.RHY", "F:u.BRE"} & record["display:g"]
    assert "T:port.P1" in record["display:g"] and "T:port.P1" in record["display:g_o"]
    for f, tg in record.items():
        if typetrace.FIELD_TYPES.get(f) == "T":
            assert not any(t.startswith(("F:", "O:", "own:")) for t in tg), f


def test_committed_downstream_equals_a_fresh_trace(record):
    assert typetrace.downstream(record) == typetrace.load_downstream()
    ds = typetrace.load_downstream()
    assert ds["P1"] == ["lam_own"] and ds["P4"] == ["p_name"]
    assert {"q_hat", "e_agent_turn"} <= set(ds["P2"]) and {"t_agent_start", "t_agent_end", "last_speaker"} <= set(ds["P5"])


def _factory(patch):
    def make(L, session, b_id, fs):
        run = Run(L, session, b_id, fs)
        patch(run)
        return run
    return make


def test_trace_refuses_an_omega_read_outside_the_ports():
    def patch(run):
        orig = run.body._own_heard

        def rogue(oh):
            orig(oh)
            run.body.t_his_spoke = oh.t_end * 1.0            # a T field read straight from OwnHeard
        run.body._own_heard = rogue
    with pytest.raises(TagViolation, match="O:own_heard"):
        typetrace.run_trace(30.0, engine_factory=_factory(patch))


def test_trace_refuses_an_f_to_t_leak():
    def patch(run):
        orig = run.slow_tick

        def leaky(inp, u_read):
            orig(inp, u_read)
            run.body.h_word = np.maximum(run.body.h_word, 0.01 * run.V_F)
        run.slow_tick = leaky
    with pytest.raises(TagViolation, match="h_word"):
        typetrace.run_trace(30.0, engine_factory=_factory(patch))


def test_trace_refuses_a_gate_reading_his_smile():
    def patch(run):
        orig = run.fast_step

        def peek(fr):
            tm = orig(fr)
            tm.g = tm.g * (1.0 + 0.0 * fr.u[0])             # g now depends on his LP
            return tm
        run.fast_step = peek
    with pytest.raises(TagViolation, match="display term g received 'F:u.BRE'"):
        typetrace.run_trace(10.0, engine_factory=_factory(patch))


def test_trace_refuses_g_o_reading_any_channel_of_his():
    def patch(run):
        orig = run.fast_step

        def peek(fr):
            tm = orig(fr)
            tm.g_o = tm.g_o * (1.0 + 0.0 * fr.u_read[3])
            return tm
        run.fast_step = peek
    with pytest.raises(TagViolation, match="display term g_o"):
        typetrace.run_trace(10.0, engine_factory=_factory(patch))


# ------------------------------------------------------------------------------------------------- F19 checks
def _session(reply_words, starts, hold_ports=None, seed=0):
    """A body-only session: the same utterances; the agent's replies with the given words and times. Returns the T
    fields after every tick."""
    L = randomise_for_trace(Learned(), seed)
    b = Body(Session(K=0.5), L)
    if hold_ports is not None:
        for name in hold_ports:
            fn = getattr(ports, ports.PORT_NAMES[name])
            setattr(ports, ports.PORT_NAMES[name], hold_ports[name](fn))
    out = []
    try:
        for n in range(240):
            t = 0.5 * n
            us = (Utterance("him", (), "his words %d" % n, t, "his words %d" % n),) if n % 13 == 5 else ()
            oh = ()
            for (ts, w) in zip(starts, reply_words):
                if abs(t - (ts + 1.0)) < 1e-9:
                    oh = (heard_at_playback(w, [ts + 0.5, ts + 1.0], "statement", ts),)
            b.tick(SlowInputs(t, us, oh, True, (), 0.0, 0.9))
            out.append({k: np.array(v, dtype=object) if isinstance(v, tuple) else np.asarray(v).copy()
                        for k, v in b.t_fields().items()})
    finally:
        if hold_ports is not None:
            import importlib
            importlib.reload(ports)
    return out


def _changed(a, b):
    from engine.invariants.asserts import t_state_digest
    return {k for x, y in zip(a, b) for k in x if t_state_digest({k: x[k].tolist()}) != t_state_digest({k: y[k].tolist()})}


STARTS = (10.0, 40.0, 75.0)


def test_f19_reply_text_swap_changes_only_downstream_of_the_ports():
    a = _session([["yes", "indeed"]] * 3, STARTS)
    b = _session([["no", "way"], ["maybe", "so"], ["never", "mind"]], STARTS)
    ds = typetrace.load_downstream()
    allowed = set(ds["P1"]) | set(ds["P2"]) | set(ds["P3"]) | set(ds["P4"])
    ch = _changed(a, b)
    assert ch and ch <= allowed, ch - allowed


def test_f19_all_ports_held_gives_bit_identical_t_state():
    held = {}

    def hold(fn):
        cache = {}

        def held_fn(oh, *args):
            key = (round(float(oh.t_start), 6),)
            if key not in cache:
                cache[key] = fn(heard_at_playback(["yes", "indeed"], oh.t_word_end, oh.template, oh.t_start), *args)
            return cache[key]
        return held_fn
    for p in ("P1", "P2", "P4"):
        held[p] = hold
    a = _session([["yes", "indeed"]] * 3, STARTS, hold_ports=held)
    b = _session([["no", "way"], ["maybe", "so"], ["never", "mind"]], STARTS, hold_ports=held)
    assert _changed(a, b) == set()


def test_f19_duration_change_reaches_only_downstream_of_p5_in_addition():
    a = _session([["yes", "indeed"]] * 3, STARTS)
    b = _session([["yes", "indeed"]] * 3, (10.0, 41.5, 75.0))
    ds = typetrace.load_downstream()
    allowed = set().union(*map(set, ds.values()))
    ch = _changed(a, b)
    assert ch and ch <= allowed and ch & set(ds["P5"]), ch
