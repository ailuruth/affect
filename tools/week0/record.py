"""research/build/week0.md: one row per measurement, appended; `report` adds the summary (latest row per check and
the branch each selects). Only numbers and branch names are written (no transcript, audio or video)."""
from __future__ import annotations

import json
import time
from pathlib import Path

from tools.week0.thresholds import Verdict, asr_plan

HEADER = """# Week-0 measurements (M1)

Written by `tools/week0/` on the operator's Mac (spec §6 row M1 and its branch table; research/build/handoff.md).
Each row is one measurement and the branch its threshold selects, mechanically (tools/week0/thresholds.py, numbers
from INNATE `m1_thresholds`). Only numbers and branch names are recorded.

| UTC | check | outcome | selects | measured | load | note |
|---|---|---|---|---|---|---|
"""
SUMMARY_MARK = "<!-- week0 summary -->"

REQUIRED = ("env_check", "download_models", "tracker", "echo_rig", "clock", "asr_stream", "asr_utterance", "breath",
            "fast_tick", "slow_tick", "memory", "sandbox", "claude_resume", "claude_thinking", "claude_latency",
            "claude_compaction", "claude_tokens")


def _default_path() -> Path:
    from tools.week0.common import WEEK0_MD
    return WEEK0_MD


def _cell(s: str) -> str:
    return str(s).replace("|", "/").replace("\n", " ")


def append(v: Verdict, path: Path | None = None, load: str = "", note: str = "", when: str | None = None) -> None:
    path = _default_path() if path is None else Path(path)
    text = path.read_text() if path.exists() else HEADER
    body, _, _ = text.partition(SUMMARY_MARK)          # the summary is rewritten by `report`; rows stay above it
    when = when or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    row = (f"| {when} | {v.check} | {v.outcome} | {_cell(v.selects)} | `{json.dumps(v.measured, sort_keys=True)}` "
           f"| {_cell(load)} | {_cell(note)} |\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip("\n") + "\n" + row)


def parse(path: Path | None = None) -> list:
    path = _default_path() if path is None else Path(path)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().partition(SUMMARY_MARK)[0].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7 or cells[0] in ("UTC", "---") or not cells[0][:4].isdigit():
            continue
        rows.append({"when": cells[0], "check": cells[1], "outcome": cells[2], "selects": cells[3],
                     "measured": json.loads(cells[4].strip("`")), "load": cells[5], "note": cells[6]})
    return rows


def summary(rows: list) -> dict:
    """Latest row per check; the combined recogniser plan; M1's status:
    'stopped' if any latest outcome is fail; 'open' if a check is missing, needs a re-measurement or is a gap;
    'complete' otherwise."""
    latest = {}
    for r in rows:
        latest[r["check"]] = r
    out = {"latest": latest}
    if "asr_stream" in latest and "asr_utterance" in latest:
        s, u = latest["asr_stream"], latest["asr_utterance"]
        plan = asr_plan(Verdict("asr_stream", s["outcome"], s["selects"]),
                        Verdict("asr_utterance", u["outcome"], u["selects"]))
        out["asr_plan"] = plan
    missing = [c for c in REQUIRED if c not in latest]
    open_ = [c for c, r in latest.items() if r["outcome"] in ("remeasure", "gap")]
    failed = [c for c, r in latest.items() if r["outcome"] == "fail"]
    if "asr_plan" in out and out["asr_plan"].outcome == "fail":
        failed.append("asr_plan")
    out.update(missing=missing, open=sorted(open_), failed=sorted(failed),
               status="stopped" if failed else ("open" if missing or open_ else "complete"))
    return out


def write_summary(path: Path | None = None) -> dict:
    path = _default_path() if path is None else Path(path)
    s = summary(parse(path))
    text = path.read_text() if path.exists() else HEADER
    body = text.partition(SUMMARY_MARK)[0].rstrip("\n")
    lines = [SUMMARY_MARK, "", "## Summary (latest measurement of each check)", "",
             f"M1 status: **{s['status']}**" + (f"; failed: {', '.join(s['failed'])}" if s["failed"] else "")
             + (f"; open: {', '.join(s['open'])}" if s["open"] else "")
             + (f"; not yet measured: {', '.join(s['missing'])}" if s["missing"] else ""), "",
             "| check | outcome | selects |", "|---|---|---|"]
    for c in REQUIRED:
        r = s["latest"].get(c)
        lines.append(f"| {c} | {r['outcome']} | {r['selects']} |" if r else f"| {c} | not measured | |")
    if "asr_plan" in s:
        p = s["asr_plan"]
        lines.append(f"| asr_plan (checks 4 and 5) | {p.outcome} | {p.selects} |")
    path.write_text(body + "\n\n" + "\n".join(lines) + "\n")
    return s
