"""tools/week0 (M1): the pass / branch / fail logic of spec §6's M1 table, applied to synthetic numbers; the
week0.md record and summary; the approval refusals. No device, model, network or Claude call is used."""
import dataclasses

import pytest

from engine.config import operator as op
from engine.config.innate import ENTRIES
from tools.week0 import measure, memory, record, sandbox_check, claude_checks
from tools.week0 import thresholds as T


def o(v):
    return v.outcome


# ------------------------------------------------------------------------------------------------ thresholds
def test_thresholds_come_from_innate():
    assert T.TH is ENTRIES["m1_thresholds"].value
    assert ENTRIES["m1_thresholds"].category == "generic" and ENTRIES["m1_thresholds"].subtype == "engineering"


def test_tracker():
    assert o(T.tracker(20.0)) == "pass"
    assert o(T.tracker(25.0)) == "branch" and "5 Hz" in T.tracker(25.0).selects
    assert o(T.tracker(35.0)) == "remeasure"
    assert o(T.tracker(35.0, 30.0)) == "branch"
    assert o(T.tracker(35.0, 30.1)) == "fail"


def test_pipeline():
    assert [o(T.pipeline(x)) for x in (90.0, 90.1, 400.0, 400.1)] == ["pass", "branch", "branch", "fail"]


def test_clock():
    assert o(T.clock(True)) == "pass"
    assert o(T.clock(False)) == "remeasure"
    assert o(T.clock(False, 10.0)) == "branch"
    assert o(T.clock(False, 20.0)) == "branch"         # 10-33 ms: pass with the SD stated (spec owner, 2026-11-27)
    assert o(T.clock(False, 33.0)) == "branch"
    assert o(T.clock(False, 33.1)) == "fail"


def test_stream_asr():
    assert o(T.stream_asr("en", 0.9, 0.15, 0.49)) == "pass"
    v = T.stream_asr("fr", 1.2, 0.10, 0.3)
    assert o(v) == "branch" and "longer partial echo" in v.selects
    for bad in (T.stream_asr("en", 1.6, 0.1, 0.3), T.stream_asr("en", 0.5, 0.16, 0.3),
                T.stream_asr("en", 0.5, 0.1, 0.5), T.stream_asr("de", 0.5, 0.1, 0.3), T.stream_asr(None, 0.5, 0.1, 0.3)):
        assert o(bad) == "branch" and bad.selects.startswith("fallback")


def test_utterance_asr():
    assert o(T.utterance_asr(0.29, 0.12)) == "pass"
    assert o(T.utterance_asr(0.30, 0.12)) == "branch"
    assert o(T.utterance_asr(0.49, 0.10)) == "branch"
    assert o(T.utterance_asr(0.50, 0.10)) == "fail"
    assert o(T.utterance_asr(0.10, 0.21)) == "fail"
    assert o(T.utterance_asr(0.10, 0.15)) == "branch"


def test_asr_plan_fails_only_when_both_fail():
    fall = T.stream_asr("de", 0.5, 0.1, 0.3)
    assert o(T.asr_plan(fall, T.utterance_asr(0.6, 0.1))) == "fail"
    assert o(T.asr_plan(fall, T.utterance_asr(0.2, 0.1))) == "branch"
    assert o(T.asr_plan(T.stream_asr("en", 0.5, 0.1, 0.3), T.utterance_asr(0.6, 0.1))) == "pass"


def test_breath():
    good_silent = [0.5] * 8 + [1.5] * 2                  # 80 % within 1 /min
    good_talk = [1.5] * 6 + [3.0] * 4                    # 60 % within 2 /min
    assert o(T.breath(good_silent, 9, 10, 0.7, good_talk)) == "pass"
    v = T.breath(good_silent, 9, 10, 0.7, [3.0] * 10)
    assert o(v) == "branch" and "mutual silence" in v.selects
    assert o(T.breath([0.5] * 7 + [1.5] * 3, 10, 10, 0.9, good_talk)) == "fail"
    assert o(T.breath(good_silent, 8, 10, 0.9, good_talk)) == "fail"
    assert o(T.breath(good_silent, 10, 10, 0.69, good_talk)) == "fail"
    assert T.breath(good_silent, 8, 10, 0.9, good_talk).selects == "breathing off"
    assert o(T.breath([-0.9] * 10, 10, 10, 0.9, [-1.9] * 10)) == "pass"   # errors count by magnitude


def test_ticks_and_memory():
    assert [o(T.fast_tick(x)) for x in (5.0, 5.1)] == ["pass", "remeasure"]
    assert [o(T.fast_tick(x, "B")) for x in (5.0, 5.1)] == ["branch", "fail"]
    assert [o(T.slow_tick(x)) for x in (50.0, 50.1, 200.0, 200.1)] == ["pass", "branch", "branch", "fail"]
    assert o(T.memory(6.0)) == "pass"
    assert o(T.memory(6.1)) == "remeasure" and "kyutai_4bit" in T.memory(6.1).selects
    assert o(T.memory(5.9, "kyutai_4bit")) == "branch"
    assert "pool_2" in T.memory(6.1, "kyutai_4bit").selects and "pool_1" in T.memory(6.1, "pool_2").selects
    assert o(T.memory(6.1, "pool_1")) == "fail"


def test_sandbox_and_env():
    assert o(T.sandbox(0)) == "pass" and o(T.sandbox(1)) == "fail" and o(T.sandbox(0, False)) == "fail"
    gb = 10 ** 9
    assert o(T.env("darwin", (3, 13, 1), True, True, 30 * gb, 100 * gb)) == "pass"
    assert o(T.env("darwin", (3, 13, 1), True, True, 10.5 * gb, 100 * gb)) == "fail"       # 0.5 GB above the floor
    assert o(T.env("darwin", (3, 13, 1), True, True, 13 * gb, 100 * gb, "models")) == "fail"
    v = T.env("linux", (3, 14, 0), False, False, 50 * gb, 100 * gb)
    assert o(v) == "fail" and all(w in v.selects for w in ("macOS", "Python", "uv", "Xcode"))
    assert o(T.downloads(5, 5, 1.0)) == "pass" and o(T.downloads(4, 5, 1.0)) == "fail"


def test_claude_rows():
    assert o(T.claude_resume(20, 20)) == "pass" and o(T.claude_resume(19, 20)) == "branch"
    assert o(T.claude_resume(10, 10)) == "remeasure"
    assert o(T.claude_thinking(0, 20)) == "pass" and o(T.claude_thinking(1, 20, 12.0)) == "branch"
    assert [o(T.claude_latency(x)) for x in (1.5, 1.6, 3.0, 3.1)] == ["pass", "branch", "branch", "fail"]
    assert o(T.claude_compaction(True, True)) == "pass"
    assert o(T.claude_compaction(False, False)) == "branch"
    assert o(T.claude_compaction(True, False)) == "remeasure"
    assert [o(T.claude_tokens(x)) for x in (4500, 4501)] == ["pass", "branch"]


def test_percentile_and_wer():
    assert T.percentile(range(101), 99) == 99.0 and T.percentile([1.0, 2.0], 50) == 1.5
    assert T.wer("the cat sat on the mat", "the cat sat on mat") == pytest.approx(1 / 6)
    assert T.wer("A, b. c!", "a b c") == 0.0


# ------------------------------------------------------------------------------------------------ measurement helpers
def test_realtime_queue_and_delivery_latency():
    assert measure.realtime_finish([0.01, 0.2, 0.01], 0.08) == pytest.approx([0.09, 0.36, 0.37])
    finish = measure.realtime_finish([0.01] * 50, 0.08)
    stream = [("one", 10), ("two", 20), ("extra", 25), ("three", 30)]
    ref = [("One", 0.0, 0.5), ("two,", 0.9, 1.2), ("three", 2.0, 2.1)]
    lat = measure.delivery_latencies(stream, finish, ref)
    assert lat == pytest.approx([finish[10] - 0.5, finish[20] - 1.2, finish[30] - 2.1])


def test_rig_onsets():
    fps = 240.0
    flash = [0.0] * 2400
    screen = [0.0] * 2400
    for k in range(5):
        a = 100 + 400 * k
        for i in range(a, a + 20):
            flash[i] = 1.0
        for i in range(a + 12, a + 32):                  # 12 frames = 50 ms later
            screen[i] = 1.0
    lags = measure.pair_onsets(measure.rising_crossings(flash, fps), measure.rising_crossings(screen, fps))
    assert len(lags) == 5 and lags == pytest.approx([12 / fps] * 5)


def test_pearson_memory_and_lsof_parsing():
    assert measure.pearson([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
    rows = [(1, 0, 100), (2, 1, 50), (3, 2, 25), (4, 0, 1000)]
    assert memory.tree_sum(rows, [1]) == 175
    out = ("COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n"
           "python 9 u 3u IPv4 0x1 0t0 TCP 127.0.0.1:5000->127.0.0.1:6000 (ESTABLISHED)\n"
           "python 9 u 4u IPv4 0x2 0t0 TCP 10.0.0.2:5001->1.1.1.1:443 (SYN_SENT)\n"
           "python 9 u 5u IPv4 0x3 0t0 TCP 127.0.0.1:7000 (LISTEN)\n")
    assert sandbox_check.non_local(out) == {"1.1.1.1:443"}


def test_compaction_switch_detection():
    assert claude_checks.compaction_switch("", {"autoCompactEnabled": False}) == (True, True)
    assert claude_checks.compaction_switch("", {"autoCompactEnabled": True}) == (True, False)
    assert claude_checks.compaction_switch("--autocompact <auto|tokens>", {}) == (False, False)


# ------------------------------------------------------------------------------------------------ week0.md
def test_record_append_parse_and_summary(tmp_path):
    path = tmp_path / "week0.md"
    record.append(T.tracker(25.0), path, load="core", when="2026-12-01T10:00:00Z")
    record.append(T.tracker(19.0), path, load="core", when="2026-12-01T10:05:00Z")
    record.append(T.stream_asr("de", 0.5, 0.1, 0.3), path, when="2026-12-01T10:10:00Z")
    record.append(T.utterance_asr(0.6, 0.1), path, when="2026-12-01T10:20:00Z")
    rows = record.parse(path)
    assert [r["check"] for r in rows] == ["tracker", "tracker", "asr_stream", "asr_utterance"]
    assert rows[1]["measured"] == {"p99_ms": 19.0}
    s = record.write_summary(path)
    assert s["latest"]["tracker"]["outcome"] == "pass"
    assert s["asr_plan"].outcome == "fail" and s["status"] == "stopped" and "asr_plan" in s["failed"]
    record.append(T.utterance_asr(0.2, 0.1), path, when="2026-12-01T10:30:00Z")   # rows go above the summary
    s = record.write_summary(path)
    text = path.read_text()
    assert text.count(record.SUMMARY_MARK) == 1 and text.index("10:30:00") < text.index(record.SUMMARY_MARK)
    assert s["status"] == "open" and "clock" in s["missing"] and s["asr_plan"].outcome == "branch"


def test_record_complete_status(tmp_path):
    path = tmp_path / "week0.md"
    passing = {"env_check": T.env("darwin", (3, 13, 0), True, True, 50e9, 100e9), "download_models": T.downloads(5, 5, 1),
               "tracker": T.tracker(10), "echo_rig": T.pipeline(50), "clock": T.clock(True),
               "asr_stream": T.stream_asr("en", 0.5, 0.1, 0.3), "asr_utterance": T.utterance_asr(0.2, 0.1),
               "breath": T.breath([0.0] * 10, 10, 10, 0.9, [0.0] * 10), "fast_tick": T.fast_tick(2),
               "slow_tick": T.slow_tick(20), "memory": T.memory(4), "sandbox": T.sandbox(0),
               "claude_resume": T.claude_resume(20, 20), "claude_thinking": T.claude_thinking(0, 20),
               "claude_latency": T.claude_latency(1.0), "claude_compaction": T.claude_compaction(False, False),
               "claude_tokens": T.claude_tokens(3000)}
    assert set(passing) == set(record.REQUIRED)
    for v in passing.values():
        record.append(v, path, when="2026-12-01T10:00:00Z")
    assert record.summary(record.parse(path))["status"] == "complete"
    record.append(T.clock(False, 20.0), path, when="2026-12-01T11:00:00Z")   # 10-33 ms is now a branch
    assert record.summary(record.parse(path))["status"] == "complete"
    record.append(T.clock(False, None), path, when="2026-12-01T12:00:00Z")   # remeasure keeps it open
    s = record.summary(record.parse(path))
    assert s["status"] == "open" and s["open"] == ["clock"]


# ------------------------------------------------------------------------------------------------ approvals
def _unanswered(monkeypatch, *names):
    for n in names:
        monkeypatch.setitem(op.SWITCHES, n, dataclasses.replace(op.SWITCHES[n], answered=False,
                                                                usable_before_answer=False))


@pytest.mark.parametrize("module, argv, switch", [
    ("claude_checks", ["latency"], "claude_test_calls_m1"),
    ("asr_stream", [], "downloads_approved"),
    ("asr_utterance", [], "conversation_language"),
    ("tracker", [], "downloads_approved"),
    ("clock", [], "conversation_language"),
    ("download_models", [], "downloads_approved"),
    ("breath", [], "conversation_language"),
    ("echo_rig", [], "conversation_language"),
    ("sandbox_check", [], "hub_offline_after_download"),
])
def test_checks_refuse_before_the_operators_answer(monkeypatch, tmp_path, module, argv, switch):
    import importlib
    from tools.week0 import common
    monkeypatch.setattr(common, "WEEK0_MD", tmp_path / "week0.md")
    _unanswered(monkeypatch, "claude_test_calls_m1", "downloads_approved", "conversation_language",
                "hub_offline_after_download")
    mod = importlib.import_module(f"tools.week0.{module}")
    with pytest.raises(SystemExit) as e:
        mod.main(argv)
    assert e.value.code == 2 and switch in e.value.msg
    assert not (tmp_path / "week0.md").exists()


def test_m1_test_call_switch_is_answered_in_the_repository():
    """Q34 item 1 answered 2026-11-28 (D97): a few week-0 test calls through his login are allowed."""
    assert op.SWITCHES["claude_test_calls_m1"].answered is True
    assert op.require("claude_test_calls_m1")["claude_test_calls_m1"] is True
