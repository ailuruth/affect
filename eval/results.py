"""Result files (spec §6 M9: results in research/build/results/). JSON and CSV only, never .npy / .npz, and no
per-frame arrays: a result holds summaries (means, the per-instance distribution, surrogate distributions, the
score). Every file carries the schema marker the CI data guard looks for (tools/ci.py).

Synthetic runs (harness self-tests on stand-ins) are not evidence: `write_json` / `write_csv` refuse to put a
synthetic result anywhere under research/build/results/, and the CI data guard refuses any file there marked
synthetic. `make eval-dry` writes to a temporary directory instead.
"""
from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from eval.registry import _jsonable

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "research" / "build" / "results"
SCHEMA_RESULT = "affect-eval-result/1"
ALLOWED_SUFFIXES = (".json", ".csv")
MAX_BYTES = 1024 * 1024


class ResultRefused(Exception):
    pass


def _inside_results(path: Path) -> bool:
    try:
        Path(path).resolve().relative_to(RESULTS_DIR.resolve())
        return True
    except ValueError:
        return False


def _check(path: Path, synthetic: bool) -> Path:
    path = Path(path)
    if path.suffix not in ALLOWED_SUFFIXES:
        raise ResultRefused(f"{path.name}: results are JSON or CSV only (no arrays)")
    if synthetic and _inside_results(path):
        raise ResultRefused(f"{path}: a synthetic stand-in run is never evidence; not written to {RESULTS_DIR}")
    return path


def write_json(path, payload: dict, synthetic: bool) -> Path:
    path = _check(Path(path), synthetic)
    if is_dataclass(payload):
        payload = asdict(payload)
    doc = {"schema": SCHEMA_RESULT, "synthetic": bool(synthetic), "evidence": not synthetic, **_jsonable(payload)}
    text = json.dumps(doc, indent=1, allow_nan=False) + "\n"
    if len(text.encode()) > MAX_BYTES:
        raise ResultRefused(f"{path.name}: {len(text)} bytes; a result is a summary, not data")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_csv(path, header: list, rows: list, synthetic: bool) -> Path:
    path = _check(Path(path), synthetic)
    buf = io.StringIO()
    buf.write(f"# {SCHEMA_RESULT} synthetic={'true' if synthetic else 'false'}\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow([_jsonable(x) for x in r])
    text = buf.getvalue()
    if len(text.encode()) > MAX_BYTES:
        raise ResultRefused(f"{path.name}: too large for a summary")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def score_record(score, extra: dict | None = None) -> dict:
    """The result document of one scored test: the prediction as written, both timestamps, the hash, the score."""
    d = asdict(score)
    d.update(extra or {})
    return d
