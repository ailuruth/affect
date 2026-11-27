"""The F-list registry covers exactly the falsifiers of the spec's §5.1 table, each with its test, data source and
the machine and stage it runs at; and eval/ carries no affect label and is never imported by the engine."""
import re
from pathlib import Path

from eval import flist
from tools import lint_labels

ROOT = Path(__file__).resolve().parents[1]


def _spec_ids():
    text = (ROOT / "research" / "build" / "spec.md").read_text(encoding="utf-8")
    sec = text[text.index("### 5.1 Falsifiers mapped to tests"):text.index("**Measured expectations")]
    ids = set()
    for line in sec.splitlines():
        if line.startswith("| F") or line.startswith("| **F"):
            first = line.split("|")[1]
            ids |= set(re.findall(r"F\d+[′″‴]*", first))
    return ids


def test_every_spec_falsifier_is_mapped():
    ids = _spec_ids()
    assert len(ids) >= 25
    assert ids == set(flist.BY_ID)


def test_each_entry_has_test_data_machine_and_stage():
    for f in flist.FALSIFIERS:
        if f.status in ("deleted", "folded into F24"):
            assert f.stages == ()
            continue
        assert f.test and f.statement
        assert any(s.machine == flist.MAC for s in f.stages), f.fid      # evidence only on the operator's Mac
        for s in f.stages:
            assert s.milestone in ("CI", "M3", "M4", "M6", "M7", "M8"), (f.fid, s.milestone)
            if s.machine == flist.MAC:
                assert s.data and set(s.data) <= set(flist.SOURCES), f.fid
    f22 = flist.BY_ID["F22"]
    assert {flist.SEAMLESS, flist.OPERATOR_M2, flist.LIVE} <= set(f22.data)
    assert flist.rows() and all(len(r) == 6 for r in flist.rows())


def test_eval_has_no_affect_label():
    hits = [h for h in lint_labels.scan(ROOT) if h[0].startswith("eval/") or h[0].startswith("tests/test_eval")]
    assert (ROOT / "eval").is_dir() and hits == []


def test_engine_never_imports_eval():
    for p in (ROOT / "engine").rglob("*.py"):
        src = p.read_text(encoding="utf-8")
        assert not re.search(r"^\s*(from|import)\s+eval\b", src, re.M), p
