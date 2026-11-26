"""T1 as an AST rule (spec §4.4, A15): no counter, accumulator or event rate is a T field."""
from pathlib import Path

import pytest

from engine.invariants import t1_rule
from engine.invariants.asserts import check_a15_t1

ROOT = Path(__file__).resolve().parents[1]


def test_engine_state_and_routes_pass():
    assert t1_rule.check_tree(ROOT) == []
    assert t1_rule.check_declarations() == []
    check_a15_t1(ROOT)


BAD = [
    "self.h_word += 1",
    "q_trace += len(turns)",
    "E = len(event_times)",
    "self.I_lp = np.count_nonzero(events)",
    "P_play = np.mean(onsets)",
    "A_L = his_turns.count(x)",
    "omega = Counter(event_list)",
    "q_trace = n_utt / elapsed",
    "K = len(x) / duration",
]
GOOD = [
    "self.h_word = max(self.h_word, v_w)",
    "q_trace = q_trace * d + (1 - d) * qhat",
    "E -= 0.0004 * dt",
    "xi += 1",                                  # an F field: not the T rule's business
    "time_since_turn = t - t_last",
    "A_L = max(A_L, 0.5 * s_lex ** 2)",
]


@pytest.mark.parametrize("src", BAD)
def test_rule_fires(src):
    assert t1_rule.check_source(src), src


@pytest.mark.parametrize("src", GOOD)
def test_rule_quiet(src):
    assert t1_rule.check_source(src) == [], src


def test_declaration_rule():
    assert t1_rule.check_declarations(frozenset({"turn_count", "E"})) == [("turn_count", "counter-like T field name")]
