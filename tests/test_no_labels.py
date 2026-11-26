"""The label lint (spec §7.4): the repository is clean, and the lint catches every spelling class."""
from pathlib import Path

import lint_stems
from tools import lint_labels as L

ROOT = Path(__file__).resolve().parents[1]


def test_repository_has_no_forbidden_token():
    hits = L.scan(ROOT)
    assert hits == [], hits[:20]


def test_tokeniser():
    for text, toks in lint_stems.TOKENISER_CASES:
        assert L.tokens(text) == toks


def test_self_test_spelling_classes():
    for w in lint_stems.MUST_FAIL:
        assert L.hits_in(w), w
    for w in lint_stems.MUST_PASS:
        assert not L.hits_in(w), w


def _word(i):                     # forbidden words are taken from the allowlisted table, never spelled here
    return lint_stems.MUST_FAIL[i]


def test_scan_catches_names_strings_comments_and_escapes(tmp_path):
    (tmp_path / "engine").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "lint_stems.py").write_text("STEMS = ()\n")
    (tmp_path / "engine" / "ok.py").write_text("x = 1  # feature career\n")
    (tmp_path / "engine" / f"{_word(0)}.py").write_text("x = 1\n")
    (tmp_path / "engine" / "b.py").write_text(f"# {_word(1)}\n")
    (tmp_path / "engine" / "c.py").write_text(f"y = dict({_word(3)}=1)\n")
    escaped = "".join(f"\\x{ord(ch):02x}" for ch in _word(4))
    (tmp_path / "engine" / "d.py").write_text(f"s = '{escaped}'\n")
    (tmp_path / "engine" / "e.json").write_text('{"%s": 1}' % _word(6))
    (tmp_path / "engine" / "f.js").write_text(f"let {_word(9)} = 0;\n")
    files = {rel for rel, _, _ in L.scan(tmp_path)}
    assert files == {f"engine/{_word(0)}.py", "engine/b.py", "engine/c.py", "engine/d.py", "engine/e.json",
                     "engine/f.js"}


def test_allowlisted_constant_is_blanked():
    src = f"DENY_FIELDS = ('{_word(5)}',)\nOTHER = 1\n"
    assert not L.hits_in(L._blank_constants(src, {"DENY_FIELDS"}))
    assert L.hits_in(src)
