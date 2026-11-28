"""M6 offline: the Claude coupling (engine/omega/) against a fake Claude Code CLI (tests/fake_claude.py).

Nothing here calls the real `claude` or the network: every Pool gets the fake's argv explicitly, and the fake writes
its session files under a temporary HOME. Covers: refusal before the operator's answers, isolation flags and
environment, no state or labels in any prompt (40 scripted turns: A11 / F14 / F17), the window bound, the daily cap
and silence at the limit, the scoring deadline and the fallbacks, interruption and the cut, the pool lifecycle (losers
killed, <= 4 processes, session files swept), compaction and integrity failures, and F19's omega side (the reply text
reaches the state only as OwnHeard at playback)."""
import ast
import asyncio
import dataclasses
import json
import os
import re
import sys
from pathlib import Path

import pytest

from engine.config import operator as op
from engine.config.innate import ENTRIES
from engine.omega import isolation, lines as L, pool as P, retrieval, transcript as TR
from engine.state import ports
from engine.state.types import (FIELD_TYPES, ChosenReply, Marker, Snippet, TranscriptText, Utterance, agent_text,
                                his_text, marker, snippet, _chosen_reply)
from tools.lint_labels import hits_in

ROOT = Path(__file__).resolve().parents[1]
FAKE = (sys.executable, str(ROOT / "tests" / "fake_claude.py"))
A, B, C = L.LINES


def answered(**over):
    sw = dict(op.SWITCHES)
    vals = {"send_text_to_anthropic": True, "send_snippets": True, "claude_daily_cap": 450,
            "nonessential_traffic_off": True, "account_training_use_checked": "checked by the operator",
            "overage_confirmed_off": True, "context_tokens_max": 4000, "claude_text_approved": L.text_digest()}
    vals.update(over)
    for k, v in vals.items():
        sw[k] = dataclasses.replace(sw[k], value=v, answered=True)
    return sw


class Env:
    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.home, self.work, self.state = tmp / "home", tmp / "work" / "cwd", tmp / "state"
        self.home.mkdir()
        self.scenario, self.logp = tmp / "scenario.json", tmp / "fake.log"
        self.set()

    def set(self, default=None, rules=()):
        self.scenario.write_text(json.dumps({"default": default or {}, "rules": list(rules)}))

    def cfg(self, cli=FAKE, line_in_system=False, base_env=None, **over):
        return isolation.OmegaConfig.from_operator(
            cli, self.work, self.state, self.home, switches=answered(**over), line_in_system=line_in_system,
            extra_env={"HOME": str(self.home), "FAKE_CLAUDE_SCENARIO": str(self.scenario),
                       "FAKE_CLAUDE_LOG": str(self.logp), **(base_env or {})})

    def log(self, event=None):
        if not self.logp.exists():
            return []
        recs = [json.loads(x) for x in self.logp.read_text().splitlines() if x.strip()]
        return [r for r in recs if event is None or r["event"] == event]


@pytest.fixture
def env(tmp_path):
    return Env(tmp_path)


def his(text, t=1.0):
    return his_text(Utterance("him", (), text, t, text))


def run(coro):
    return asyncio.run(coro)


def pid_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


async def session(cfg, turns, **kw):
    """Run turns [(new, snippets)] in one pool; returns (results, pool)."""
    pool = P.Pool(cfg, **kw)
    out = []
    try:
        await pool.start()
        for new, sn in turns:
            out.append(await pool.turn(new, sn))
    finally:
        await pool.close()
    return out, pool


# ------------------------------------------------------------------------------------------------ refusal
def test_refuses_until_the_operator_answers(env):
    with pytest.raises(op.Unanswered) as err:
        isolation.OmegaConfig.from_operator(FAKE, env.work, env.state, env.home,
                                            switches={n: dataclasses.replace(v, answered=False, usable_before_answer=False)
                                                      for n, v in op.SWITCHES.items()})
    for name in ("send_text_to_anthropic", "send_snippets", "claude_daily_cap", "nonessential_traffic_off",
                 "account_training_use_checked", "overage_confirmed_off", "context_tokens_max",
                 "claude_text_approved"):
        assert name in str(err.value)
    for over, msg in (({"claude_daily_cap": None}, "claude_daily_cap"), ({"claude_daily_cap": 0}, "claude_daily_cap"),
                      ({"claude_daily_cap": True}, "claude_daily_cap"),
                      ({"send_text_to_anthropic": False}, "send_text"), ({"overage_confirmed_off": False}, "overage"),
                      ({"account_training_use_checked": None}, "account"),
                      ({"context_tokens_max": 9000}, "context_tokens_max"),
                      ({"claude_text_approved": "0" * 64}, "approved")):
        with pytest.raises(ValueError, match=msg):
            env.cfg(**over)
    with pytest.raises(TypeError):
        P.Pool(object())
    assert env.log() == []                         # no process was ever started
    with pytest.raises(op.Unanswered):              # the live switches stay unanswered in the repository
        op.require(*isolation.SWITCHES_NEEDED)


def test_working_directory_must_be_empty_and_without_memory_files(env, tmp_path):
    (tmp_path / "work" / "CLAUDE.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "work" / "CLAUDE.md").write_text("x")
    with pytest.raises(ValueError, match="CLAUDE.md"):
        env.cfg()
    (tmp_path / "work" / "CLAUDE.md").unlink()
    (env.work / "stray.txt").write_text("x")
    with pytest.raises(ValueError, match="empty"):
        env.cfg()


# ------------------------------------------------------------------------------------------------ isolation
@pytest.mark.parametrize("traffic_off", [True, False])
def test_isolation_flags_and_environment(env, traffic_off):
    base = {"CLAUDE_CODE_MAX_OUTPUT_TOKENS": "50", "CLAUDE_CODE_EFFORT_LEVEL": "max", "MAX_THINKING_TOKENS": "9"}
    cfg = env.cfg(nonessential_traffic_off=traffic_off, base_env=base)
    run(session(cfg, [(his("Hello there, how was the walk."), ()), (his("It rained a bit."), ())]))
    starts = env.log("start")
    assert starts
    for s in starts:
        a = s["argv"]
        assert a[a.index("--setting-sources") + 1] == ""
        assert a[a.index("--tools") + 1] == ""
        assert "--strict-mcp-config" in a and json.loads(a[a.index("--mcp-config") + 1]) == {"mcpServers": {}}
        assert a[a.index("--permission-mode") + 1] == "default"
        assert a[a.index("--model") + 1] == "haiku" and a[a.index("--effort") + 1] == "low"
        assert a[a.index("--output-format") + 1] == "stream-json" and "--include-partial-messages" in a
        assert a[a.index("--input-format") + 1] == "stream-json"
        assert a[a.index("--system-prompt") + 1] == L.instruction()
        assert "--bare" not in a and not any("max-output" in x or "budget" in x for x in a)
        assert Path(s["cwd"]).resolve() == env.work.resolve()
        assert s["env"]["DISABLE_AUTOUPDATER"] == "1"
        assert s["env"]["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == ("1" if traffic_off else None)
        assert s["env"]["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] is None and s["env"]["CLAUDE_CODE_EFFORT_LEVEL"] is None
        assert s["env"]["MAX_THINKING_TOKENS"] is None
    resumed = [s for s in starts if "--resume" in s["argv"]]
    assert resumed and all("--fork-session" in s["argv"] for s in resumed)


# ------------------------------------------------------------------------------------------------ prompts
SAYINGS = ["I went to the market this morning.", "The bus was late again.", "My sister phoned at lunch.",
           "We talked about the garden.", "The tomatoes are finally red.", "I might paint the fence.",
           "Do you think blue would work?", "The neighbour has a new dog.", "It barks at the postman.",
           "I made soup for dinner."]


def _state_names():
    from engine.config.innate import ENTRIES as E
    return {n for n in list(FIELD_TYPES) + list(E) if "_" in n}


def test_forty_scripted_turns_carry_no_state_or_labels(env):
    """A11 / F14 / F17 on 40 scripted turns, with markers and snippets: every prompt is made only of the instruction,
    his words, the agent's replies, markers, snippets and the one fork line; no label stem, no state name, no
    number except a marker's silence; no fork line in any history."""
    env.set({"text": "That sounds like a full day. Tell me more about it. I am listening."})
    old = snippet([his("We planted beans last spring.", 0.0),
                   agent_text(_chosen_reply("Beans grow fast in warm weather.", 1.0))])
    turns = []
    for i in range(40):
        new = marker(23 + i, 100.0 + i) if i % 7 == 6 else his(SAYINGS[i % len(SAYINGS)], 100.0 + i)
        turns.append((new, (old,) if i % 5 == 0 else ()))
    results, pool = run(session(env.cfg(), turns))
    assert all(r.reply is not None for r in results), [r.reason for r in results]
    done = env.log("recv")
    assert len(done) == 40 * 3
    allowed = {L.instruction(), *SAYINGS}
    names = _state_names()
    for rec in done:
        msg, system, hist = rec["message"], rec["system"], rec["history"]
        assert system == L.instruction()
        assert sum(msg.endswith("\n\n" + ln) for ln in L.LINES) == 1           # exactly one fork line, at the end
        for role, text in hist:                                                  # F17
            assert not any(ln in text for ln in L.LINES)
        for text in [msg, system] + [t for _, t in hist]:
            assert hits_in(text) == [], text
            toks = set(re.findall(r"[A-Za-z_]+", text))
            assert not (toks & names), toks & names
            for num in re.findall(r"\d+", text):
                assert re.search(r"\[no reply from him for %s s\]" % num, text), text
        body = msg.rsplit("\n\n", 1)[0]
        parts = [p for p in body.split("\n\n")]
        for p in parts:
            assert (p in allowed or p.startswith(L.SNIPPET_HEADER) or re.fullmatch(r"\[no reply from him for \d+ s\]", p)
                    or all(x in allowed for x in p.split("\n"))), p
    # each turn: the three forks got the same body and the three different lines
    for k in range(40):
        msgs = sorted(r["message"] for r in done[3 * k:3 * k + 3])
        assert len({m.rsplit("\n\n", 1)[0] for m in msgs}) == 1
    # the builder accepts nothing but the prompt objects
    for bad in ("raw text", 0.42, {"E": 0.3}, Utterance("him", (), "x", 0.0, "x")):
        with pytest.raises(TypeError):
            TR.build_turn(L.instruction(), [], bad)
        with pytest.raises(TypeError):
            TR.build_turn(L.instruction(), [bad], his("x"))
    with pytest.raises(TypeError):
        TR.build_turn(L.instruction(), [], his("x"), fork_lines=("Your inner state is 0.7.",))
    for make in (lambda: TranscriptText("his", "x", 0.0), lambda: Marker("x", 0.0), lambda: Snippet((), 0.0),
                 lambda: ChosenReply("x", 0.0)):
        with pytest.raises(TypeError):
            make()


def test_constant_instruction_and_lines_are_clean():
    text = L.instruction()
    assert hits_in(text) == [] and not re.search(r"\d", text)
    assert all(hits_in(ln) == [] and not re.search(r"\d", ln) for ln in L.LINES)
    assert not (set(re.findall(r"[A-Za-z_]+", text)) & _state_names())
    assert L.instruction_bytes() == (ROOT / "engine" / "omega" / "instruction.txt").read_bytes()


def test_window_length_bound(env):
    long = " ".join(["word%s" % chr(97 + i % 26) for i in range(70)])         # about 450 bytes, no digits
    env.set({"text": "Yes. I see what you mean. Go on."})
    tmax = 1500
    turns = [(his(long + " turn " + chr(97 + i % 26) * 3, float(i)), ()) for i in range(12)]
    results, pool = run(session(env.cfg(context_tokens_max=tmax, send_snippets=False), turns))
    assert all(r.reply is not None for r in results)
    done = env.log("recv")
    for rec in done:
        total = TR.tokens(rec["system"]) + sum(TR.tokens(t) for _, t in rec["history"]) + TR.tokens(rec["message"])
        assert total <= tmax, total
        assert not rec["history"] or rec["history"][0][0] == "user"
    last = done[-1]["history"]
    assert len(last) >= 2 and len(last) < 2 * 11                                                  # oldest turns were dropped
    assert turns[0][0].text not in " ".join(t for _, t in last)
    # a message alone over the budget keeps its newest words
    huge = his(" ".join("w%s" % chr(97 + i % 26) for i in range(3000)))
    tp = TR.build_turn(L.instruction(), [], huge, tokens_max=500)
    assert tp.tokens_total <= 500 and tp.messages[0].split("\n\n")[0].endswith(huge.text.split()[-1])
    w = TR.commit_window(L.instruction(), [his(long), agent_text(_chosen_reply("ok", 0))] * 30, tokens_max=tmax,
                         send_snippets=False)
    assert w and w[0][0] == "user" and w[-1][0] == "assistant" and len(w) < 60


# ------------------------------------------------------------------------------------------------ cap and limit
def test_daily_cap_and_silence_at_the_cap(env):
    env.set({"text": "Sure. That works. Fine."})
    spoken = []
    results, pool = run(session(env.cfg(claude_daily_cap=4), [(his("one"), ()), (his("two"), ()), (his("three"), ())]))
    assert [r.drafts for r in results[:2]] == [3, 1]
    assert results[2].reply is None and results[2].reason == "silent:cap"
    assert len(env.log("recv")) == 4
    cap = P.DailyCap(env.state / "claude_calls.json", 4)
    assert cap.used() == 4 and cap.take(1) == 0
    assert P.DailyCap(env.state / "claude_calls.json", 4, today=lambda: "2999-01-01").take(3) == 3
    # his words of the silent turn stay in the transcript; no word was made up for the agent
    assert [e.text for e in pool.entries][-1] == "three"
    assert all(e.speaker == "his" or e.text in ("Sure. That works.",) for e in pool.entries
               if isinstance(e, TranscriptText))


def test_limit_shrinks_the_pool_then_silence(env):
    env.set({"mode": "limit"})
    clock = [1000.0]
    cfg = env.cfg()

    async def go():
        pool = P.Pool(cfg, now=lambda: clock[0])
        texts = []
        try:
            await pool.start()
            r1 = await pool.turn(his("a"), (), on_text=texts.append)
            s1 = pool.sizer.size
            r2 = await pool.turn(his("b"), (), on_text=texts.append)
            s2 = pool.sizer.size
            r3 = await pool.turn(his("c"), (), on_text=texts.append)     # at size 1: silent until the limit resets
            n_before = len(env.log("limit"))
            r4 = await pool.turn(his("d"), (), on_text=texts.append)
            n_after = len(env.log("limit"))
            clock[0] += 31 * 60                                             # reset: one probe turn at size 1
            env.set({"text": "Back again. Yes."})
            r5 = await pool.turn(his("e"), (), on_text=texts.append)
            clock[0] += 31 * 60
            size_later = pool.sizer.current()
            return (r1, r2, r3, r4, r5), (s1, s2), (n_before, n_after), size_later, texts
        finally:
            await pool.close()

    rs, sizes, counts, size_later, texts = run(go())
    assert [r.reason for r in rs[:4]] == ["silent:limit"] * 4
    assert sizes == (2, 1)
    assert counts[0] == counts[1]                                           # nothing sent while silent
    assert rs[4].reply is not None and rs[4].drafts == 1
    assert size_later == 2
    assert texts == [rs[4].reply.text]                                      # no words of its own at the limit


def test_slow_first_sentences_shrink_the_pool():
    clock = [0.0]
    s = P.PoolSizer(3, now=lambda: clock[0])
    for _ in range(P.RESIZE_TURNS):
        s.record_latency(3.5)
    assert s.size == 2
    clock[0] += P.RESIZE_WINDOW_S
    assert s.current() == 3


# ------------------------------------------------------------------------------------------------ deadline
def test_deadline_selection_and_losers_killed(env):
    env.set({}, [{"match": A, "first_delay": 0.05, "text": "Alpha here. Second alpha. Third."},
                 {"match": B, "first_delay": 0.30, "text": "Beta here. Second beta. Third."},
                 {"match": C, "first_delay": 1.50, "text": "Gamma here. Second gamma. Third."}])
    rank = {"Alpha": 1.0, "Beta": 2.0, "Gamma": 3.0}

    async def scorer(first):
        await asyncio.sleep(0.01)
        return rank[first.split()[0]]

    async def go():
        pool = P.Pool(env.cfg())
        try:
            await pool.start()
            r = await pool.turn(his("Pick one."), (), scorer=scorer)
            gamma = [x["pid"] for x in env.log("recv") if x["message"].endswith(C)]
            return r, list(pool.killed_pids), pool, gamma, [p for p in gamma if pid_alive(p)]
        finally:
            await pool.close()

    r, killed, pool, gamma, gamma_alive = run(go())
    assert r.fork == 1 and r.reply.text == "Beta here. Second beta."           # Gamma came after the deadline
    assert gamma and gamma[0] in killed and gamma_alive == []                 # the loser was killed, not drained
    assert pool.max_alive <= isolation.MAX_PROCESSES


def test_deadline_cap_gives_silence(env):
    env.set({"first_delay": 0.6, "text": "Late. Too late."})

    async def go():
        pool = P.Pool(env.cfg())
        try:
            await pool.start()
            t_end = asyncio.get_running_loop().time() - (ENTRIES["draft_deadline_s"].value["cap_after_turn_end"] - 0.2)
            return await pool.turn(his("Anyone?"), (), t_turn_end=t_end)
        finally:
            await pool.close()

    r = run(go())
    assert r.reply is None and r.reason == "silent:deadline"


@pytest.mark.parametrize("mode,reason", [("crash", "silent:failure"), ("hang", "silent:deadline")])
def test_no_answer_gives_silence(env, mode, reason):
    env.set({"mode": mode})
    results, pool = run(session(env.cfg(), [(his("Hello?"), ())]))
    assert results[0].reply is None and results[0].reason == reason
    assert not any(pid_alive(s["pid"]) for s in env.log("start"))


def test_missing_cli_gives_silence(env):
    results, pool = run(session(env.cfg(cli=(str(env.tmp / "no-such-claude"),)), [(his("Hello?"), ())]))
    assert results[0].reply is None and results[0].reason == "silent:no_process"


# ------------------------------------------------------------------------------------------------ cut, interruption
def test_cut_at_second_sentence_and_at_sixty_words(env):
    env.set({"word_delay": 0.02, "text": "One thing first. Then a second thing. A third that is never said. More."})
    results, _ = run(session(env.cfg(), [(his("Tell me."), ())]))
    assert results[0].reason == "cut" and results[0].reply.text == "One thing first. Then a second thing."
    words = " ".join("w%s" % chr(97 + i % 26) for i in range(80))
    env.set({"word_delay": 0.002, "text": words})
    results, _ = run(session(env.cfg(), [(his("Tell me."), ())]))
    assert len(results[0].reply.text.split()) == 60


def test_interruption_while_speaking_and_before(env):
    env.set({"word_delay": 0.05, "text": "Well, " + " ".join(["and so on"] * 30) + "."})

    async def go():
        pool = P.Pool(env.cfg())
        got = []

        def on_text(t):
            got.append(t)
            pool.interrupt()
        try:
            await pool.start()
            env.set({"first_delay": 0.05, "word_delay": 0.05, "text": "First. " + " ".join(["and so on"] * 30) + "."})
            r1 = await pool.turn(his("Talk."), (), on_text=on_text)
            alive1 = pool.alive_count()
            env.set({"first_delay": 1.0, "text": "Too slow."})
            asyncio.get_running_loop().call_later(0.2, pool.interrupt)
            n_entries = len(pool.entries)
            r2 = await pool.turn(his("Wait, I"), ())
            return r1, r2, got, alive1, n_entries, len(pool.entries)
        finally:
            await pool.close()

    r1, r2, got, alive1, n0, n1 = run(go())
    assert r1.reason == "interrupted" and r1.reply.text == "".join(got).strip()
    assert len(r1.reply.text.split()) < 10
    assert alive1 <= isolation.MAX_PROCESSES
    assert r2.reason == "interrupted" and r2.reply is None and n0 == n1         # a false start adds nothing
    assert not any(pid_alive(s["pid"]) for s in env.log("start"))


# ------------------------------------------------------------------------------------------------ lifecycle
def test_pool_lifecycle(env):
    env.set({}, [{"match": A, "first_delay": 0.02, "text": "Quick one. Done."},
                 {"match": B, "first_delay": 0.10, "word_delay": 0.05, "text": "Slower one. Done too."},
                 {"match": C, "first_delay": 0.15, "word_delay": 0.05, "text": "Slowest. Also done."}])

    async def go():
        pool = P.Pool(env.cfg())
        seen = []
        try:
            await pool.start()
            seen.append(pool.alive_count())
            for i in range(5):
                r = await pool.turn(his(SAYINGS[i]), ())
                assert r.reply is not None
                await asyncio.sleep(0.05)
                seen.append(pool.alive_count())
                files = sorted(p.name for p in pool.canonical.dir.glob("*.jsonl"))
                assert files == [pool.canonical.path.name]                     # fork files deleted at idle
            return pool, seen
        finally:
            await pool.close()

    pool, seen = run(go())
    assert seen[0] == 3 and all(n <= isolation.MAX_PROCESSES for n in seen)
    assert pool.max_alive <= isolation.MAX_PROCESSES
    assert pool.killed_pids and not any(pid_alive(p) for p in pool.killed_pids)
    assert not any(pid_alive(s["pid"]) for s in env.log("start"))             # nothing left running
    assert list(pool.canonical.dir.glob("*.jsonl")) == []
    # the canonical transcript holds his words and the chosen replies only
    hist = pool.canonical.history
    assert all(not any(ln in t for ln in L.LINES) for _, t in hist)


def test_line_in_system_prompt_fallback(env):
    env.set({"text": "Right. Okay."})
    run(session(env.cfg(line_in_system=True), [(his("Hi."), ()), (his("Again."), ())]))
    done = env.log("recv")
    assert sorted(r["system"] for r in done[:3]) == sorted(L.instruction() + "\n" + ln for ln in L.LINES)
    assert all(not any(ln in r["message"] for ln in L.LINES) for r in done)


# ------------------------------------------------------------------------------------------------ A11
@pytest.mark.parametrize("mode", ["tamper_canonical", "misrecord"])
def test_integrity_failure_stops_the_route(env, mode):
    env.set({"mode": mode, "text": "Hm. Yes."})
    results, pool = run(session(env.cfg(), [(his("Hi."), ()), (his("Hi again."), ()), (his("And again."), ())]))
    first_bad = 1 if mode == "tamper_canonical" else 0      # the first turn has no resumed canonical to tamper with
    assert results[first_bad].reason == "silent:a11"
    assert all(r.reason == "silent:route_stopped" for r in results[first_bad + 1:])
    assert pool.stopped


def test_compaction_makes_the_turn_silent(env):
    env.set({"mode": "compact", "text": "Hm. Yes."})
    results, pool = run(session(env.cfg(), [(his("Hi."), ()), (his("Hi again."), ())]))
    assert [r.reason for r in results] == ["silent:compaction"] * 2
    assert pool.stopped is None and any(e["event"] == "a11_compaction" for e in pool.log)


# ------------------------------------------------------------------------------------------------ retrieval
def test_retrieval_alibi_and_switch():
    day = retrieval.DAY_S
    s_old = snippet([his("old talk", 0.0)])
    s_new = snippet([his("new talk", 13 * day)])
    assert retrieval.retrieve([(s_old, 1.0), (s_new, 0.5)], 14 * day, True) == (s_new, s_old)   # 1 - 2 < 0.5 - 1/7
    assert retrieval.retrieve([(s_old, 1.0)], 14 * day, False) == ()
    many = [(snippet([his("t %s" % chr(97 + i), float(i))]), 1.0) for i in range(6)]
    assert len(retrieval.retrieve(many, 10.0, True)) == 3
    with pytest.raises(TypeError):
        retrieval.retrieve([("text", 1.0)], 0.0, True)


def test_snippets_off_are_never_sent(env):
    env.set({"text": "Okay. Sure."})
    s = snippet([his("We planted beans.", 0.0)])
    run(session(env.cfg(send_snippets=False), [(his("Hi."), (s,))]))
    assert all("beans" not in r["message"] for r in env.log("recv"))


# ------------------------------------------------------------------------------------------------ F19 (omega side)
def _py(top):
    return sorted((ROOT / top).rglob("*.py"))


def test_f19_reply_text_reaches_the_state_only_as_own_heard():
    """The omega package never makes OwnHeard and imports nothing of the state but the prompt types; nothing below
    it imports omega; ChosenReply is made only in engine/omega/pool.py; the ports refuse anything but OwnHeard."""
    for p in _py("engine"):
        rel = p.relative_to(ROOT).as_posix()
        tree = ast.parse(p.read_text(encoding="utf-8"))
        mods = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        mods |= {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        if rel.startswith("engine/omega/"):
            assert not {m for m in mods if m.startswith("engine.state") and m != "engine.state.types"}, rel
            assert not {m for m in mods if m.split(".")[:2] in (["engine", "routes"], ["engine", "shadow"],
                                                               ["engine", "boundary"], ["engine", "learn"])}, rel
            assert "heard_at_playback" not in calls and "OwnHeard" not in calls, rel
        else:
            assert not any(m.startswith("engine.omega") for m in mods), rel
        if rel != "engine/omega/pool.py" and rel != "engine/state/types.py":
            assert "_chosen_reply" not in calls, rel
    reply = _chosen_reply("Some words.", 0.0)
    for port in (lambda x: ports.lambda_own(x, None, None), lambda x: ports.p_name(x, None, None),
                 ports.own_turn_events, lambda x: ports.turn_question_bit(x, True)):
        with pytest.raises(TypeError):
            port(reply)


# ------------------------------------------------------------------------- Fix P (D102): the model is pinned and logged
def test_a_model_change_silences_the_agent_until_pinned(env):
    """The exact model id the CLI reports is recorded; a different id later makes the turn silent and is logged, until
    the operator sets claude_model to the new exact id."""
    env.set({"text": "Hello there. Second."})
    r1, p1 = run(session(env.cfg(base_env={"FAKE_CLAUDE_MODEL": "m-a"}), [(his("Hi."), ()), (his("Again."), ())]))
    assert all(r.reply is not None for r in r1)
    assert any(e["event"] == "model_recorded" and e["model"] == "m-a" for e in p1.log)
    r2, p2 = run(session(env.cfg(base_env={"FAKE_CLAUDE_MODEL": "m-b"}), [(his("Still there?"), ())]))
    assert r2[0].reply is None and r2[0].reason == "silent:model_changed"
    assert any(e["event"] == "model_changed" and e["was"] == "m-a" and e["now"] == "m-b" for e in p2.log)
    r3, p3 = run(session(env.cfg(base_env={"FAKE_CLAUDE_MODEL": "m-b"}, claude_model="m-b"), [(his("Now?"), ())]))
    assert r3[0].reply is not None
