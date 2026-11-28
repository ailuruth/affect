"""Nightly replay (spec §1.9, §1.10, §6 M8): the gate and budgets, the consolidation weights, the learning steps on
the stubs, every learned part inside its set afterwards, and nothing of his smiles, attention or time used as a
reward or target. Synthetic arrays in a temporary store only: code tests, never evidence about behaviour."""
import collections
import dataclasses
import inspect

import numpy as np
import pytest

from engine.config import operator as op
from engine.config.innate import ENTRIES
from engine.invariants import asserts as A
from engine.learn import nightly as NL
from engine.learn import projections as PJ
from engine.learn import weights as WB
from engine.memory.replay import Budget, Replay, load_session
from engine.memory.retrieval_index import SnippetIndex
from engine.memory.store import Store
from engine.omega.retrieval import retrieve
from engine.routes import appraisal as AP
from engine.routes import cone as C
from engine.routes.learned_t import Learned
from synth_store import CR, DAY, GAZE, LP, answered, write_session

Disk = collections.namedtuple("Disk", "total used free")
ROOMY = lambda p: Disk(100, 10, 90)                         # noqa: E731
SMALL_RSS = lambda: 100 * 1024 ** 2                         # noqa: E731
NIGHT = dict(idle_s=3600.0, local_hour=3.0)


def _store(tmp_path, name="st", n=3, **kw):
    st = Store(tmp_path / name, answered())
    for i in range(n):
        write_session(st, f"s{i}", t0=i * DAY, seconds=60.0, seed=i, **kw)
    return st


def _replay(st, L=None, **kw):
    kw.setdefault("budget", Budget(rss=SMALL_RSS))
    return Replay(st, Learned() if L is None else L, answered(), disk_usage=ROOMY, **kw)


@pytest.fixture(scope="module")
def night(tmp_path_factory):
    st = _store(tmp_path_factory.mktemp("night"))
    L = Learned()
    rep = _replay(st, L).run(now_s=3 * DAY, **NIGHT)
    return st, L, rep


# ---------------------------------------------------------------------------------------------------- the gate
def test_budgets_are_the_spec_values():
    b = ENTRIES["replay_budget"].value
    assert b["wall_s"] == 3600.0 and b["memory_gb"] == 2.0


def test_refuses_before_the_schedule_is_approved(tmp_path):
    st = _store(tmp_path, n=1)
    rep = Replay(st, Learned(), dict(op.SWITCHES), disk_usage=ROOMY).run(now_s=DAY, **NIGHT)
    assert not rep.ran and "nightly_schedule" in rep.reason
    assert not st.sessions()[0].manifest["replayed"]


@pytest.mark.parametrize("idle,hour,ok", [(3600, 3.0, True), (60, 3.0, False), (3600, 12.0, False),
                                          (3600, 6.0, False), (3600, 2.0, True)])
def test_idle_window(tmp_path, idle, hour, ok):
    st = _store(tmp_path, n=0)
    assert _replay(st).may_start(idle, hour)[0] is ok


def test_window_across_midnight(tmp_path):
    st = _store(tmp_path, n=0)
    sw = answered(nightly_schedule={"start_hour": 23, "end_hour": 5, "idle_min_s": 0.0})
    r = Replay(st, Learned(), sw, disk_usage=ROOMY)
    assert r.may_start(0, 23.5)[0] and r.may_start(0, 1.0)[0] and not r.may_start(0, 12.0)[0]


def test_never_alongside_a_live_session(tmp_path):
    st = _store(tmp_path, n=1)
    w = st.open_session("live1", "op", 5 * DAY)
    rep = _replay(st).run(now_s=6 * DAY, **NIGHT)
    assert not rep.ran and "live" in rep.reason
    w.close(5 * DAY + 1)


def test_disk_floor(tmp_path):
    st = _store(tmp_path, n=0)
    r = Replay(st, Learned(), answered(), disk_usage=lambda p: Disk(100, 95, 5))
    assert not r.may_start(3600, 3.0)[0]


# ---------------------------------------------------------------------------------------------------- budgets
def _weights(L):
    return {k: np.array(v) for k, v in NL.export(L, {}).items() if not k.startswith("trained.")}


def test_wall_budget_stops_and_defers(tmp_path):
    st = _store(tmp_path, n=2)
    t = [0.0]

    def clock():                                           # every reading advances 30 s of fake time
        t[0] += 30.0
        return t[0]
    L = Learned()
    before = _weights(L)
    rep = _replay(st, L, budget=Budget(clock=clock, rss=SMALL_RSS)).run(now_s=2 * DAY, **NIGHT)
    status = {n: s for n, s, _ in rep.steps}
    assert "stopped at budget" in status.values()
    stopped = [n for n, s, _ in rep.steps if s == "stopped at budget"][0]
    names = [n for n, _, _ in rep.steps]
    later = names[names.index(stopped) + 1:]
    assert all(status[n] in ("deferred", "not built") for n in later)
    assert rep.elapsed_s <= 3600.0 + 30.0                  # one clock reading past the check at most
    assert not any(s.manifest["replayed"] for s in st.sessions())
    after = _weights(L)
    for part in [stopped] + later:                         # the stopped and deferred parts are untouched
        for k in before:
            if k.startswith(part + "."):
                np.testing.assert_array_equal(before[k], after[k])


def test_memory_budget_stops_before_learning(tmp_path):
    st = _store(tmp_path, n=1)
    L = Learned()
    before = _weights(L)
    rep = _replay(st, L, budget=Budget(rss=lambda: 2 * 1024 ** 3 + 1)).run(now_s=DAY, **NIGHT)
    assert rep.steps == [] or all(s in ("stopped at budget", "deferred", "not built") for _, s, _ in rep.steps)
    after = _weights(L)
    for k in before:
        np.testing.assert_array_equal(before[k], after[k])


def test_memory_estimate_counts_against_the_budget(tmp_path):
    st = _store(tmp_path, n=1)
    data = load_session(st.sessions()[0]).nbytes()
    cap = 100 * 1024 ** 2 + 2 * data                          # the 4x working estimate does not fit
    rep = _replay(st, budget=Budget(mem_bytes=cap, rss=SMALL_RSS)).run(now_s=DAY, **NIGHT)
    assert [s for n, s, _ in rep.steps if n == "pi_tilde"] == ["stopped at budget"]


def test_real_budget_on_this_machine(night):
    st, L, rep = night
    assert rep.ran and rep.elapsed_s < 3600.0 and rep.peak_bytes < 2 * 1024 ** 3


# ---------------------------------------------------------------------------------------------------- the night
def test_steps_run_in_order(night):
    st, L, rep = night
    names = [n for n, _, _ in rep.steps]
    assert names == [n for n, _, _ in NL.STEPS]
    done = {n for n, s, _ in rep.steps if s == "done"}
    assert {"pi_tilde", "calibration", "adapter", "word_v", "appraisal", "delta", "omega", "energy"} <= done
    assert {n: s for n, s, _ in rep.steps}["world_model"] == "not built"
    assert rep.violations == []
    assert all(s.manifest["replayed"] for s in st.sessions())


def test_flagged_sessions_are_skipped(tmp_path):
    st = _store(tmp_path, n=1)
    write_session(st, "bad5", t0=2 * DAY, seconds=30.0, seed=5, flag="A5")
    write_session(st, "bad14", t0=3 * DAY, seconds=30.0, seed=6, flag="A14")
    rep = _replay(st).run(now_s=4 * DAY, **NIGHT)
    assert set(rep.skipped_flagged) == {"bad5", "bad14"} and rep.sessions == ["s0"]


def test_learned_parts_changed_and_saved(night, tmp_path):
    st, L, rep = night
    assert np.any(L.reader_own.W) and np.any(L.word_v.W) and np.any(L.appraisal.learned_bases) and np.any(L.delta.syn)
    assert "op" in L.adapter and np.all(np.abs(L.adapter["op"](np.eye(16))) <= 0.15)
    L2 = Learned()
    NL.restore(L2, st.load_arrays("learned.npz"))
    np.testing.assert_array_equal(L2.appraisal.learned_bases, L.appraisal.learned_bases)
    np.testing.assert_array_equal(L2.delta.syn, L.delta.syn)
    assert L2.delta.trained and L2.adapter["op"].trained


def test_every_learned_part_inside_its_budget_after_replay(night):
    st, L, rep = night
    persons = st.read_json("persons.json", {})
    omegas = [p["omega"] for p in persons["persons"].values()]
    assert PJ.check_all(L, omegas) == []
    S = C.pair_sign(np.zeros((C.N, C.N)))
    for om in omegas:
        assert np.all(np.abs(om) <= 1.0)
        bases = np.concatenate([AP.innate_bases(om), L.appraisal.learned_bases])
        assert A.check_a7(bases, om, S, L.delta) == []
        cone = C.Cone(30.0)
        assert A.check_a6(cone.latch(om, np.zeros(C.N_IN)), om, cone.S, cone.G0) == []
    from engine.routes.free_display import MASK_ZERO
    assert not np.any(L.delta.syn[:, list(MASK_ZERO)])
    assert 0.0 <= persons["agent"]["E"] <= 1.0


def test_assertions_stay_green_in_a_session_after_replay(night):
    """A short synthetic session through the shadow pair with the replay-trained weights: A1-A9, A14 silent."""
    from engine.config.channels import TABLE
    from engine.shadow.shadow import Frame, ShadowPair
    from engine.state.body import Session
    from engine.state.types import Utterance, heard_at_playback
    from synth import partner
    st, L, rep = night
    om = st.read_json("persons.json", {})["persons"]["op"]["omega"]
    r = np.random.default_rng(3)
    fs, T = 30.0, int(40 * 30)
    one = np.array([s != "signed" for s in TABLE.signs])
    U = np.stack([partner(T, fs, r, 30.0) if one[k] else partner(T, fs, r, 30.0) - 0.3 for k in range(33)], 1)
    pair = ShadowPair(Session(K=0.6, omega=tuple(om)), np.concatenate([U.mean(0), np.zeros(3)]), L)
    for n in range(T):
        t = n / fs
        if n % int(7 * fs) == int(3 * fs):
            pair.push_utterance(Utterance("him", (), "we planted beans", t, "we planted beans"))
        if n % int(11 * fs) == int(9 * fs):
            pair.push_own_heard(heard_at_playback(["a", "reply"], [t - 0.4, t], "statement", t - 0.8))
        pair.step(Frame.from_u(t, U[n], 0.4))
    assert pair.safety.log == []
    L.delta.disabled = False


def test_a7_failure_in_a_step_is_undone(tmp_path, monkeypatch):
    st = _store(tmp_path, n=1)
    L = Learned()
    from engine.learn import projections
    real = projections.project_delta
    monkeypatch.setattr(projections, "project_delta", lambda d: None)        # a projection bug
    monkeypatch.setattr(NL.PJ, "project_delta", lambda d: None)
    rep = _replay(st, L).run(now_s=DAY, **NIGHT)
    monkeypatch.setattr(projections, "project_delta", real)
    st_delta = {n: s for n, s, _ in rep.steps}["delta"]
    assert st_delta == "undone" and any(v[1] == "A7" for v in rep.violations)
    assert not np.any(L.delta.syn) and not L.delta.trained


# ---------------------------------------------------------------------------------------------------- what may weigh
def test_weight_functions_read_only_the_allowed_signals():
    assert list(inspect.signature(WB.sample_weight).parameters) == ["Dp_word"]
    assert list(inspect.signature(WB.lr_scale).parameters) == ["drop_amps"]
    assert WB.ALLOWED_WEIGHT_SIGNALS == {"body.Dp_word", "events.drop_event.amp"}
    for step, src in WB.TARGET_SOURCES.items():
        assert not src & WB.FORBIDDEN_TARGET_SOURCES, step
    w = WB.sample_weight([0.0, 0.025, 0.05, 0.5])
    np.testing.assert_allclose(w, [1.0, 2.5, 4.0, 4.0])
    assert WB.lr_scale([]) == 1.0 and abs(WB.lr_scale([0.4, 0.6]) - np.exp(-0.25)) < 1e-12


def test_session_weights_depend_only_on_Dp_word(tmp_path):
    def more_smiles_and_gaze(u):
        u = u.copy()
        u[:, [LP, CR]] = np.clip(u[:, [LP, CR]] + 0.5, 0, 1)
        u[:, list(GAZE)] = 0.0
        return u
    a = load_session(_store(tmp_path, "a", n=1).sessions()[0])
    b = load_session(_store(tmp_path, "b", n=1, his_face=more_smiles_and_gaze).sessions()[0])
    assert not np.array_equal(a.u, b.u)
    np.testing.assert_array_equal(a.weights(), b.weights())
    c = load_session(_store(tmp_path, "c", n=1, Dp_word_scale=0.2).sessions()[0])
    assert not np.array_equal(a.weights(), c.weights())                       # the positive control
    d = load_session(_store(tmp_path, "d", n=1, Dp_scale=0.2).sessions()[0])
    np.testing.assert_array_equal(a.weights(), d.weights())                   # the face-including Dp column is not read (fix R1)


def test_his_smiles_and_attention_are_never_a_target(tmp_path):
    """Two nights that differ only in his face (more smiling, gaze held away): every part whose objective could act
    as a reward learns exactly the same weights; only his own readers' statistics (calibration, H_id inputs) see
    his face, as inputs."""
    def more_smiles_and_gaze(u):
        u = u.copy()
        u[:, [LP, CR]] = np.clip(u[:, [LP, CR]] + 0.5, 0, 1)
        u[:, list(GAZE)] = 0.0
        return u
    La, Lb = Learned(), Learned()
    sa, sb = _store(tmp_path, "a", n=2), _store(tmp_path, "b", n=2, his_face=more_smiles_and_gaze)
    _replay(sa, La).run(now_s=2 * DAY, **NIGHT)
    _replay(sb, Lb).run(now_s=2 * DAY, **NIGHT)
    wa, wb = _weights(La), _weights(Lb)
    for k in wa:
        if not k.startswith(("head_id.", "theta0.head_id")):
            np.testing.assert_array_equal(wa[k], wb[k], err_msg=k)
    pa, pb = sa.read_json("persons.json", {}), sb.read_json("persons.json", {})
    assert pa["persons"]["op"]["omega"] == pb["persons"]["op"]["omega"]
    assert pa["persons"]["op"]["b_read"] != pb["persons"]["op"]["b_read"]   # knowing his face: an input only


def test_his_time_is_never_a_reward(tmp_path):
    """A longer session (the same moments plus a quiet tail: he stayed longer) gives the shared moments the same
    weights, adds no drop event, and, with no word latch in either, moves omega exactly as the short one."""
    a = load_session(_store(tmp_path, "a", n=1).sessions()[0])
    b = load_session(_store(tmp_path, "b", n=1, extra_quiet_s=600.0).sessions()[0])
    assert b.n > a.n
    np.testing.assert_array_equal(a.weights(), b.weights()[:a.n])
    assert [e for e in a.events if e["kind"] == "drop_event"] == [e for e in b.events if e["kind"] == "drop_event"]
    for s in (a, b):
        s.body[:, NL.COL["h_word"]] = 0.0
    pa, pb = {"agent": {}, "persons": {}}, {"agent": {}, "persons": {}}
    NL.step_omega(NL.Night(Learned(), pa, [a]))
    NL.step_omega(NL.Night(Learned(), pb, [b]))
    assert pa["persons"]["op"]["omega"] == pb["persons"]["op"]["omega"]


def test_adapter_learns_only_from_separated_reports(tmp_path):
    s = load_session(_store(tmp_path, n=1).sessions()[0])
    for ev in s.events:
        if ev["kind"] == "report":
            ev["separated"] = False
    night = NL.Night(Learned(), {"agent": {}, "persons": {}}, [s])
    assert "no separated report" in NL.step_adapter(night) and "op" not in night.L.adapter


def test_head_id_waits_for_400_utterances(night):
    st, L, rep = night
    assert "op" not in L.head_id
    detail = {n: d for n, _, d in rep.steps}["head_id"]
    assert "< 400" in detail


# ---------------------------------------------------------------------------------------------------- retrieval
def test_retrieval_index_over_retained_transcripts(night):
    st, L, rep = night
    idx = SnippetIndex.build(st, L.enc, "op")
    assert idx.entries and len(idx.entries[0][0].entries) <= 3
    q = L.retrieval_query(np.zeros(6), np.zeros(3), np.zeros(64))
    cands = idx.candidates(q)
    assert all(rel == 0.0 for _, rel in cands)              # untrained query: recency alone
    got = retrieve(cands, now_s=3 * DAY, send_snippets=True)
    assert 0 < len(got) <= 3 and got[0].t >= got[-1].t
    assert retrieve(cands, now_s=3 * DAY, send_snippets=False) == ()
    assert SnippetIndex.build(st, L.enc, "someone_else").entries == []


# ------------------------------------------------------------------------------------- fix G (D101): frozen gate readers
def test_replay_never_changes_what_the_gates_read(tmp_path):
    """The gates g and g_o read his and the agent's own face only through frozen copies of the readers they were
    fitted with. A replay night retrains reader_his / reader_own but must leave the gate readers bit-identical, and
    no replay-writable array may be (or alias) a gate reader."""
    st = _store(tmp_path, "g", n=2)
    L = Learned()
    before = {n: (getattr(L, n).W.copy(), getattr(L, n).b.copy()) for n in ("gate_reader_his", "gate_reader_own")}
    _replay(st, L).run(now_s=2 * DAY, **NIGHT)
    for n, (W, b) in before.items():
        np.testing.assert_array_equal(getattr(L, n).W, W)
        np.testing.assert_array_equal(getattr(L, n).b, b)
    gate_arrays = [getattr(L, n).W for n in before] + [getattr(L, n).b for n in before]
    for name, (obj, attr) in NL.param_items(L).items():
        arr = getattr(obj, attr)
        assert not any(np.shares_memory(arr, g) for g in gate_arrays if isinstance(arr, np.ndarray)), name
    assert L.gate_reader_his is not L.reader_his and L.gate_reader_own is not L.reader_own


# ------------------------------------------------------------------- D101 follow-up: typed store columns and streams
def test_replay_weights_and_targets_respect_column_types():
    """Every stored body column has a type; replay weights read only T columns; a target that reads an F column is
    declared (omega's D, bounded by Lemma S*); the per-tick streams the readers are fitted to are never F."""
    from engine.memory import store as S
    from engine.memory.replay import TICK_STREAMS
    assert set(S.BODY_COLUMN_TYPES) == set(S.BODY_COLUMNS)
    for sig in WB.ALLOWED_WEIGHT_SIGNALS:
        if sig.startswith("body."):
            assert S.BODY_COLUMN_TYPES[sig[5:]] == "T", sig
    declared_f = {("omega", "body.D"), ("word_v", "body.V_F")}   # both declared routes (Lemma S*; pass 16 table)
    for step, srcs in WB.TARGET_SOURCES.items():
        for src in srcs:
            if src.startswith("body.") and S.BODY_COLUMN_TYPES.get(src[5:]) == "F":
                assert (step, src) in declared_f, (step, src)
    assert set(TICK_STREAMS) <= set(S.STREAM_TYPES)
    for step in ("pi_tilde", "delta"):
        for src in WB.TARGET_SOURCES[step]:
            assert S.STREAM_TYPES.get(src) in ("own", "T"), (step, src)
