"""The prediction registry (spec §5.2 "the predicted state-level change written before the run"; §6 M9 done-check
"each prediction scored as written before the run").

Each test's prediction is written to its own file, `predictions/<test_id>.json`, with a UTC timestamp and the
SHA-256 of its canonical content, BEFORE its run. The run is opened with `start_run`, which records the
prediction's hash and the start time; `score` re-reads the file and refuses to score when

  - the prediction file is missing (MissingPrediction),
  - its stored hash does not match its content, or its content or hash differ from what `start_run` recorded
    (PredictionChanged: it was changed after the run started),
  - its timestamp is not strictly before the run's start (LatePrediction),
  - the append-only log `log.jsonl` (each line chained to the previous line's hash) was edited (RegistryTampered).

A registered prediction is immutable: registering the same test id with different content raises
PredictionChanged (a revised prediction is a new test id). Scoring applies the prediction's own criterion
mechanically (`evaluate`) to the observed readouts; nothing about the criterion is chosen after the run.

The criterion grammar (all on internal-state readouts, never on face matching):
  {"op": "eq", "readout": r, "value": v, "tol": t}         |obs - v| <= t (t = 0: exact)
  {"op": "lt" | "le" | "gt" | "ge", "readout": r, "value": v}
  {"op": "abs_le", "readout": r, "value": v}
  {"op": "lt_readout" | "le_readout", "readout": r, "other": r2, "abs": bool}   obs(r) < obs(r2)
  {"op": "monotone", "readout": r, "sign": +1 | -1, "strict": bool}           a list over increasing dose
  {"op": "gt_quantile" | "le_quantile", "readout": r, "null": r2, "q": 0.95}   obs vs a surrogate distribution
  {"op": "all", "of": [criteria]}    {"op": "any", "of": [criteria]}
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

SCHEMA_PREDICTION = "affect-eval-prediction/1"
SCHEMA_RUN = "affect-eval-run/1"
SCHEMA_LOG = "affect-eval-log/1"
GENESIS = "0" * 64


class RegistryError(Exception):
    pass


class MissingPrediction(RegistryError):
    pass


class PredictionChanged(RegistryError):
    pass


class LatePrediction(RegistryError):
    pass


class RegistryTampered(RegistryError):
    pass


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="microseconds")


def _parse(ts: str) -> _dt.datetime:
    return _dt.datetime.fromisoformat(ts)


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()


def sha256(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


@dataclass(frozen=True)
class Prediction:
    """One test's prediction, in state-level terms. `criterion` is applied mechanically by `evaluate`."""
    test_id: str
    statement: str
    criterion: dict
    harness: str                     # lesions | steering | surrogates | mirror | f22 | ...
    falsifier: str = ""              # F-id of spec §5.1, or "" (E1-E3 rows of §5.2-§5.4)
    source: str = ""                 # where the prediction comes from (design §7 row, spec §5.x)
    synthetic: bool = False          # a harness self-test on synthetic stand-ins: never evidence

    def body(self) -> dict:
        return asdict(self)


@dataclass
class RunToken:
    run_id: str
    test_id: str
    prediction_sha256: str
    written_at: str
    started_at: str
    synthetic: bool


@dataclass
class Score:
    test_id: str
    run_id: str
    passed: bool
    detail: dict
    prediction: dict
    prediction_sha256: str
    written_at: str
    started_at: str
    scored_at: str
    observed: dict = field(default_factory=dict)


class Registry:
    def __init__(self, root):
        self.root = Path(root)
        self.pred_dir = self.root / "predictions"
        self.run_dir = self.root / "runs"
        self.log_path = self.root / "log.jsonl"

    # ------------------------------------------------------------------------------------------ the log
    def _log_lines(self) -> list:
        if not self.log_path.exists():
            return []
        return [json.loads(x) for x in self.log_path.read_text(encoding="utf-8").splitlines() if x.strip()]

    def verify_log(self) -> list:
        prev = GENESIS
        lines = self._log_lines()
        for i, rec in enumerate(lines):
            body = {k: v for k, v in rec.items() if k != "line_sha256"}
            if rec.get("prev") != prev or sha256(body) != rec.get("line_sha256"):
                raise RegistryTampered(f"registry log line {i + 1} was edited or reordered")
            prev = rec["line_sha256"]
        return lines

    def _append(self, event: str, **kw) -> None:
        lines = self.verify_log()
        prev = lines[-1]["line_sha256"] if lines else GENESIS
        body = {"schema": SCHEMA_LOG, "event": event, "at": kw.pop("at"), "prev": prev, **kw}
        rec = dict(body, line_sha256=sha256(body))
        self.root.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=False) + "\n")

    # ------------------------------------------------------------------------------------------ predictions
    def path(self, test_id: str) -> Path:
        if not test_id or any(c in test_id for c in "/\\") or test_id.startswith("."):
            raise ValueError(f"bad test id {test_id!r}")
        return self.pred_dir / f"{test_id}.json"

    def register(self, pred: Prediction, now: str | None = None) -> dict:
        """Write the prediction file (before the run). Idempotent for identical content; refuses a change."""
        _check_criterion(pred.criterion)
        p = self.path(pred.test_id)
        content_sha = sha256(pred.body())
        if p.exists():
            rec = self._read(pred.test_id)
            if rec["content_sha256"] != content_sha:
                raise PredictionChanged(f"{pred.test_id}: a registered prediction is immutable (register a new test id)")
            return rec
        at = now or utc_now()
        core = {"prediction": pred.body(), "written_at": at, "content_sha256": content_sha}
        rec = {"schema": SCHEMA_PREDICTION, "test_id": pred.test_id, "synthetic": pred.synthetic, **core,
               "sha256": sha256(core)}
        self.pred_dir.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        self._append("register", at=at, test_id=pred.test_id, sha256=rec["sha256"])
        return rec

    def _read(self, test_id: str) -> dict:
        p = self.path(test_id)
        if not p.exists():
            raise MissingPrediction(f"{test_id}: no prediction written; register it before the run")
        rec = json.loads(p.read_text(encoding="utf-8"))
        core = {"prediction": rec.get("prediction"), "written_at": rec.get("written_at"),
                "content_sha256": rec.get("content_sha256")}
        if sha256(core) != rec.get("sha256") or sha256(rec.get("prediction")) != rec.get("content_sha256"):
            raise PredictionChanged(f"{test_id}: the prediction file does not match its own hash")
        return rec

    # ------------------------------------------------------------------------------------------ runs
    def start_run(self, test_id: str, now: str | None = None) -> RunToken:
        rec = self._read(test_id)
        at = now or utc_now()
        if not _parse(rec["written_at"]) < _parse(at):
            raise LatePrediction(f"{test_id}: prediction written at {rec['written_at']}, not before {at}")
        tok = RunToken(uuid.uuid4().hex, test_id, rec["sha256"], rec["written_at"], at,
                       bool(rec["prediction"].get("synthetic")))
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / f"{tok.run_id}.json").write_text(
            json.dumps({"schema": SCHEMA_RUN, **asdict(tok)}, indent=1) + "\n", encoding="utf-8")
        self._append("start", at=at, test_id=test_id, run_id=tok.run_id, sha256=rec["sha256"])
        return tok

    def score(self, tok: RunToken, observed: dict, now: str | None = None) -> Score:
        """Score a finished run against its prediction as written before the run (else refuse)."""
        lines = self.verify_log()
        starts = [x for x in lines if x["event"] == "start" and x.get("run_id") == tok.run_id]
        if len(starts) != 1 or starts[0]["sha256"] != tok.prediction_sha256 or starts[0]["at"] != tok.started_at:
            raise RegistryTampered(f"{tok.test_id}: run {tok.run_id} has no matching start record")
        if any(x["event"] == "score" and x.get("run_id") == tok.run_id for x in lines):
            raise RegistryError(f"{tok.test_id}: run {tok.run_id} was already scored")
        rec = self._read(tok.test_id)
        if rec["sha256"] != tok.prediction_sha256:
            raise PredictionChanged(f"{tok.test_id}: the prediction changed after run {tok.run_id} started")
        regs = [x for x in lines if x["event"] == "register" and x["test_id"] == tok.test_id]
        if not regs or regs[0]["sha256"] != rec["sha256"]:
            raise PredictionChanged(f"{tok.test_id}: the prediction differs from the one first registered")
        if not (_parse(rec["written_at"]) < _parse(tok.started_at) and _parse(regs[0]["at"]) < _parse(tok.started_at)):
            raise LatePrediction(f"{tok.test_id}: prediction not written before the run started")
        pred = rec["prediction"]
        passed, detail = evaluate(pred["criterion"], observed)
        at = now or utc_now()
        self._append("score", at=at, test_id=tok.test_id, run_id=tok.run_id, sha256=rec["sha256"], passed=passed)
        return Score(tok.test_id, tok.run_id, passed, detail, pred, rec["sha256"], rec["written_at"],
                     tok.started_at, at, _jsonable(observed))


# ============================================================================================ criteria
_OPS = {"eq", "lt", "le", "gt", "ge", "abs_le", "lt_readout", "le_readout", "monotone", "gt_quantile",
        "le_quantile", "all", "any"}


def _check_criterion(c: dict) -> None:
    if not isinstance(c, dict) or c.get("op") not in _OPS:
        raise ValueError(f"criterion op must be one of {sorted(_OPS)}: {c!r}")
    if c["op"] in ("all", "any"):
        if not c.get("of"):
            raise ValueError("'all' / 'any' need a non-empty 'of'")
        for x in c["of"]:
            _check_criterion(x)
    elif "readout" not in c:
        raise ValueError(f"criterion {c['op']!r} needs a readout")


def _get(observed: dict, name: str):
    if name not in observed:
        raise KeyError(f"readout {name!r} not in the observed results")
    return observed[name]


def _quantile(xs, q: float) -> float:
    s = sorted(float(x) for x in xs)
    if not s:
        raise ValueError("empty surrogate distribution")
    pos = q * (len(s) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def evaluate(c: dict, observed: dict):
    """Apply a criterion. Returns (passed, detail)."""
    op = c["op"]
    if op in ("all", "any"):
        parts = [evaluate(x, observed) for x in c["of"]]
        ok = all(p for p, _ in parts) if op == "all" else any(p for p, _ in parts)
        return ok, {"op": op, "parts": [d for _, d in parts]}
    v = _get(observed, c["readout"])
    d = {"op": op, "readout": c["readout"]}
    if op in ("eq", "lt", "le", "gt", "ge", "abs_le"):
        x = float(v)
        ref = float(c["value"])
        ok = {"eq": lambda: abs(x - ref) <= float(c.get("tol", 0.0)), "lt": lambda: x < ref, "le": lambda: x <= ref,
              "gt": lambda: x > ref, "ge": lambda: x >= ref, "abs_le": lambda: abs(x) <= ref}[op]()
        d.update(observed=x, value=ref)
    elif op in ("lt_readout", "le_readout"):
        x, y = float(v), float(_get(observed, c["other"]))
        if c.get("abs"):
            x, y = abs(x), abs(y)
        ok = x < y if op == "lt_readout" else x <= y
        d.update(observed=x, other=c["other"], other_value=y)
    elif op == "monotone":
        xs = [float(a) for a in v]
        s = int(c.get("sign", 1))
        diffs = [s * (b - a) for a, b in zip(xs, xs[1:])]
        ok = all(q > 0 for q in diffs) if c.get("strict") else all(q >= 0 for q in diffs)
        ok = ok and any(q > 0 for q in diffs)
        d.update(observed=xs, sign=s)
    else:
        q = float(c.get("q", 0.95))
        x, thr = float(v), _quantile(_get(observed, c["null"]), q)
        ok = x > thr if op == "gt_quantile" else x <= thr
        d.update(observed=x, null=c["null"], q=q, threshold=thr)
    return bool(ok), d


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if hasattr(x, "tolist"):
        return _jsonable(x.tolist())
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x
