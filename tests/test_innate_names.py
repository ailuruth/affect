"""A15: categories, subtypes, the reviewed name allowlist and the situation-name test (spec §3.3)."""
import json
import re

import pytest

import lint_stems
from engine.config import innate
from engine.invariants.asserts import InvariantError, check_a15_entries
from tools.lint_labels import hits_in, tokens

SINGLE = [w for w in lint_stems.SITUATION_WORDS if "_" not in w]
MULTI = [w.split("_") for w in lint_stems.SITUATION_WORDS if "_" in w]


def situation_hits(text: str) -> list:
    tk = tokens(text)
    out = [t for t in tk if any(t.startswith(w) for w in SINGLE)]
    for seq in MULTI:
        out += ["_".join(seq) for i in range(len(tk) - len(seq) + 1) if tk[i:i + len(seq)] == seq]
    return out + hits_in(text)


def _entries():
    return json.loads(innate.LOCK_PATH.read_bytes())["entries"]


def test_a15_entries_pass():
    check_a15_entries()


def test_every_entry_categorised():
    for name, e in _entries().items():
        assert e["category"] in innate.CATEGORIES, name
        if e["category"] == "generic":
            assert e["subtype"] in innate.GENERIC_SUBTYPES, name


@pytest.mark.parametrize("mutate", ["category", "subtype", "name"])
def test_a15_refuses(mutate):
    e = _entries()
    if mutate == "category":
        e["ledger_kappa"]["category"] = "misc"
    elif mutate == "subtype":
        del e["theta_end_default"]["subtype"]
    else:
        e["unreviewed_constant"] = dict(e["ledger_kappa"])
    with pytest.raises(InvariantError, match="A15"):
        check_a15_entries(e)


def test_no_situation_or_label_word_in_keys_units_comments():
    for name, e in _entries().items():
        for field in (name, e["unit"], e["why"], e["source"]):
            assert not situation_hits(field), (name, field, situation_hits(field))
        if isinstance(e["value"], dict):
            for k in e["value"]:
                assert not situation_hits(k), (name, k)


def test_situation_matcher_self_test():
    for w in lint_stems.SITUATION_MUST_FAIL:
        assert situation_hits(w), w
    for w in lint_stems.SITUATION_MUST_PASS:
        assert not situation_hits(w), w


def test_allowlist_file_is_sorted_and_unique():
    names = [ln for ln in innate.LOCK_PATH.with_name("innate_names.txt").read_text().splitlines()
             if ln and not ln.startswith("#")]
    assert names == sorted(set(names))
    assert not [n for n in names if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", n)]
