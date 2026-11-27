"""The prediction registry (eval/registry.py) and result files (eval/results.py): a prediction must be written,
timestamped and hashed before its run; late, missing or changed predictions are refused. Synthetic results never
reach research/build/results/, and the CI data guard accepts only eval/ summaries there."""
import json

import pytest

from eval import registry as R
from eval import results as RS
from tools.ci import data_violations, result_file_ok

T0 = "2026-11-27T10:00:00.000000+00:00"
T1 = "2026-11-27T10:00:01.000000+00:00"
T2 = "2026-11-27T10:00:02.000000+00:00"


def _pred(tid="t.one", value=0.0, **kw):
    return R.Prediction(tid, "readout x stays at 0", {"op": "eq", "readout": "x", "value": value}, "lesions", **kw)


def test_register_start_score(tmp_path):
    reg = R.Registry(tmp_path)
    rec = reg.register(_pred(), now=T0)
    assert rec["written_at"] == T0 and len(rec["sha256"]) == 64
    tok = reg.start_run("t.one", now=T1)
    sc = reg.score(tok, {"x": 0.0}, now=T2)
    assert sc.passed and sc.written_at == T0 and sc.started_at == T1
    assert reg.score(reg.start_run("t.one", now=T2), {"x": 1.0}).passed is False
    assert [x["event"] for x in reg.verify_log()] == ["register", "start", "score", "start", "score"]


def test_missing_prediction_is_refused(tmp_path):
    reg = R.Registry(tmp_path)
    with pytest.raises(R.MissingPrediction):
        reg.start_run("t.none")
    reg.register(_pred(), now=T0)
    tok = reg.start_run("t.one", now=T1)
    (tmp_path / "predictions" / "t.one.json").unlink()
    with pytest.raises(R.MissingPrediction):
        reg.score(tok, {"x": 0.0})


def test_late_prediction_is_refused(tmp_path):
    reg = R.Registry(tmp_path)
    reg.register(_pred(), now=T1)
    with pytest.raises(R.LatePrediction):
        reg.start_run("t.one", now=T1)                        # not strictly before
    with pytest.raises(R.LatePrediction):
        reg.start_run("t.one", now=T0)


def test_prediction_changed_after_start_is_refused(tmp_path):
    reg = R.Registry(tmp_path)
    reg.register(_pred(), now=T0)
    tok = reg.start_run("t.one", now=T1)
    p = tmp_path / "predictions" / "t.one.json"
    rec = json.loads(p.read_text())
    rec["prediction"]["criterion"]["value"] = 5.0             # edited, hash not updated
    p.write_text(json.dumps(rec))
    with pytest.raises(R.PredictionChanged):
        reg.score(tok, {"x": 5.0})
    # edited consistently (every hash recomputed, timestamp kept): still refused against the start record
    core = {"prediction": rec["prediction"], "written_at": rec["written_at"],
            "content_sha256": R.sha256(rec["prediction"])}
    rec.update(content_sha256=core["content_sha256"], sha256=R.sha256(core))
    p.write_text(json.dumps(rec))
    with pytest.raises(R.PredictionChanged):
        reg.score(tok, {"x": 5.0})


def test_changed_prediction_cannot_be_reregistered(tmp_path):
    reg = R.Registry(tmp_path)
    reg.register(_pred(), now=T0)
    assert reg.register(_pred())["written_at"] == T0           # identical content: idempotent, original time kept
    with pytest.raises(R.PredictionChanged):
        reg.register(_pred(value=1.0))


def test_replaced_file_and_log_tampering_are_refused(tmp_path):
    reg = R.Registry(tmp_path)
    reg.register(_pred(), now=T0)
    tok = reg.start_run("t.one", now=T1)
    other = R.Registry(tmp_path / "other")                     # a new, self-consistent file written later
    other.register(_pred(value=7.0), now=T0)
    (tmp_path / "predictions" / "t.one.json").write_text((tmp_path / "other" / "predictions" / "t.one.json").read_text())
    with pytest.raises(R.PredictionChanged):
        reg.score(tok, {"x": 7.0})
    lines = (tmp_path / "log.jsonl").read_text().splitlines()
    first = json.loads(lines[0])
    first["at"] = "2020-01-01T00:00:00+00:00"
    (tmp_path / "log.jsonl").write_text("\n".join([json.dumps(first)] + lines[1:]) + "\n")
    with pytest.raises(R.RegistryTampered):
        reg.verify_log()


def test_a_run_is_scored_once(tmp_path):
    reg = R.Registry(tmp_path)
    reg.register(_pred(), now=T0)
    tok = reg.start_run("t.one", now=T1)
    reg.score(tok, {"x": 0.0})
    with pytest.raises(R.RegistryError):
        reg.score(tok, {"x": 0.0})


def test_criteria():
    ev = R.evaluate
    obs = {"a": 1.0, "b": 2.0, "d": [0.0, 0.1, 0.1, 0.3], "null": list(range(101)), "s": 96.0}
    assert ev({"op": "lt_readout", "readout": "a", "other": "b"}, obs)[0]
    assert ev({"op": "monotone", "readout": "d", "sign": 1}, obs)[0]
    assert not ev({"op": "monotone", "readout": "d", "sign": 1, "strict": True}, obs)[0]
    assert not ev({"op": "monotone", "readout": "d", "sign": -1}, obs)[0]
    assert ev({"op": "gt_quantile", "readout": "s", "null": "null", "q": 0.95}, obs)[0]
    assert ev({"op": "le_quantile", "readout": "a", "null": "null"}, obs)[0]
    assert ev({"op": "all", "of": [{"op": "abs_le", "readout": "a", "value": 1.0},
                                   {"op": "eq", "readout": "b", "value": 2.1, "tol": 0.11}]}, obs)[0]
    with pytest.raises(ValueError):
        R.Registry("/nonexistent").register(R.Prediction("x", "-", {"op": "near"}, "lesions"))


def test_results_are_json_csv_and_synthetic_kept_out(tmp_path):
    p = RS.write_json(tmp_path / "r.json", {"a": 1}, synthetic=True)
    assert json.loads(p.read_text())["synthetic"] is True
    with pytest.raises(RS.ResultRefused):
        RS.write_json(RS.RESULTS_DIR / "dry.json", {"a": 1}, synthetic=True)
    with pytest.raises(RS.ResultRefused):
        RS.write_json(tmp_path / "r.npy", {"a": 1}, synthetic=False)
    assert not (RS.RESULTS_DIR / "dry.json").exists()
    RS.write_csv(tmp_path / "t.csv", ["a"], [[1]], synthetic=False)
    assert result_file_ok(tmp_path / "t.csv")


def test_data_guard_on_results(tmp_path):
    res = tmp_path / "research" / "build" / "results"
    RS.write_json(res / "real.json", {"a": 1}, synthetic=False)
    RS.write_csv(res / "real.csv", ["a"], [[1]], synthetic=False)
    reg = R.Registry(res / "registry")
    reg.register(_pred(), now=T0)
    reg.start_run("t.one", now=T1)
    (res / "notes.md").write_text("x")
    assert data_violations(tmp_path) == []
    RS.write_json(tmp_path / "x.json", {"a": 1}, synthetic=True)
    (res / "x.json").write_text((tmp_path / "x.json").read_text())       # synthetic copied in by hand
    (res / "arr.npy").write_bytes(b"0")
    (res / "plain.json").write_text('{"a": 1}')
    assert {p for p, _ in data_violations(tmp_path)} == {
        "research/build/results/x.json", "research/build/results/arr.npy", "research/build/results/plain.json"}
