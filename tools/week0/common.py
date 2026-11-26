"""Shared parts of the M1 checks (spec §6 row M1; research/build/handoff.md step 7).

- Approval: a check that needs a model, the camera, the microphone or Claude calls `require_approval` with the
  operator switches it depends on (engine/config/operator.py; Q34 items 1, 4, 5, 10). An unanswered switch refuses
  the run with the missing answer named; nothing is imported, opened or sent before that.
- Lazy imports: macOS-only packages and model runtimes are imported only inside a check, after its approval
  (`lazy`); a missing package refuses the run with the install command.
- Full load: the numbers count only at full load (spec §6: every process running, a scripted 10-min session), so
  a timed check refuses unless `load_session` is running (`require_full_load`). `--dry-run` runs a check without
  that and without approvals that it does not need, and writes nothing to research/build/week0.md.
- Local data (recordings, page samples, the load heartbeat) live in WEEK0_DIR, outside the repository
  (default ~/.affect-week0). Only numbers and branch names go into week0.md.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEEK0_MD = ROOT / "research" / "build" / "week0.md"
WEEK0_DIR = Path(os.environ.get("AFFECT_WEEK0_DIR", Path.home() / ".affect-week0"))
HEARTBEAT = WEEK0_DIR / "load_session.json"
HEARTBEAT_MAX_AGE_S = 10.0
PAGE_PORT = 8765


class Refused(SystemExit):
    """A check that may not run yet. Exit status 2; the message says what is missing."""

    def __init__(self, msg: str):
        print(f"week0: refused: {msg}", file=sys.stderr)
        super().__init__(2)
        self.msg = msg


def require_approval(*switches: str) -> dict:
    """Values of the operator switches, or Refused naming each missing answer (engine/config/operator.py)."""
    from engine.config import operator as op
    try:
        return op.require(*switches)
    except op.Unanswered as err:
        raise Refused(f"{err}. Record the answer in engine/config/operator.py (answered=True) first.") from None


def require_mac() -> None:
    if sys.platform != "darwin":
        raise Refused(f"this check measures the operator's Mac; this is {sys.platform}")


def lazy(module: str, install: str):
    """Import a package only now (after approval); refuse with the install command if it is missing."""
    try:
        return importlib.import_module(module)
    except ImportError:
        raise Refused(f"package {module!r} is not installed; install it with: {install}") from None


def require_tool(binary: str, hint: str) -> str:
    path = shutil.which(binary)
    if path is None:
        raise Refused(f"command {binary!r} not found; {hint}")
    return path


def load_status(now: float | None = None) -> dict | None:
    """The running load session's heartbeat (components, pids), or None if none is running."""
    try:
        hb = json.loads(HEARTBEAT.read_text())
    except (OSError, ValueError):
        return None
    now = time.time() if now is None else now
    return hb if now - float(hb.get("t", 0.0)) <= HEARTBEAT_MAX_AGE_S else None


def require_full_load(args) -> str:
    """Name of the load the number is measured under; refuses without a running load session (unless dry run)."""
    hb = load_status()
    if hb is None:
        if args.dry_run:
            return "none (dry run)"
        raise Refused("no load session is running. Start it first in another Terminal window: "
                      "uv run python -m tools.week0.load_session")
    return "+".join(hb.get("components", [])) or "core"


def parser(doc: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=(doc or "").strip().splitlines()[0])
    p.add_argument("--dry-run", action="store_true",
                   help="run without the load session and write nothing to research/build/week0.md")
    return p


def finish(verdict, args, load: str = "", note: str = "") -> int:
    """Print the number and its branch; append it to research/build/week0.md unless this is a dry run."""
    from tools.week0 import record
    print(f"{verdict.check}: {verdict.outcome} -> {verdict.selects}")
    print("  measured: " + json.dumps(verdict.measured, sort_keys=True))
    if args.dry_run:
        print("  (dry run: nothing written)")
    else:
        record.append(verdict, load=load, note=note)
        print(f"  appended to {WEEK0_MD.relative_to(ROOT)}")
    return 0 if verdict.outcome != "fail" else 1


def local_path(name: str) -> Path:
    WEEK0_DIR.mkdir(parents=True, exist_ok=True)
    return WEEK0_DIR / name


def require_page() -> None:
    """The browser page with the face tracker (M2's web/, at least its tracking part)."""
    if not (ROOT / "web" / "index.html").is_file():
        raise Refused("the browser page web/index.html (M2, its tracking part) is not built yet")


def receive_page_samples(kind: str, n: int, timeout_s: float, port: int = PAGE_PORT) -> list:
    """Collect `n` samples of one kind that the page POSTs to http://127.0.0.1:port/week0 as JSON
    {"kind": kind, "values": [...]}. Loopback only. Returns the values (may be fewer on timeout)."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    got: list = []

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            try:
                msg = json.loads(body)
                if msg.get("kind") == kind:
                    got.extend(msg.get("values", []))
                self.send_response(204)
            except ValueError:
                self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "http://localhost")
            self.end_headers()

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", port), H)
    srv.timeout = 0.5
    t_end = time.time() + timeout_s
    try:
        while len(got) < n and time.time() < t_end:
            srv.handle_request()
    finally:
        srv.server_close()
    return got[:n]


def samples_from(args, kind: str, n: int, timeout_s: float) -> list:
    """From --from-file (a JSON list the page saved) or live from the page."""
    if getattr(args, "from_file", None):
        return [float(x) for x in json.loads(Path(args.from_file).read_text())]
    require_page()
    print(f"waiting for {n} '{kind}' samples from the page (up to {timeout_s:.0f} s) on 127.0.0.1:{PAGE_PORT} ...")
    return [float(x) if not isinstance(x, (dict, list)) else x for x in receive_page_samples(kind, n, timeout_s)]
