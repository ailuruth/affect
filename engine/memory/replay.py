"""Nightly replay (spec §1.9, §2.4, §6 M8): a separate process, launched only when no session is live, inside the
operator's approved idle window (the M8 Ask, operator switch `nightly_schedule`), under a wall-clock budget of
1 h and a memory budget of 2 GB (INNATE `replay_budget`). It skips every session flagged by an A5 or A14 failure.

Order of one night (`Replay.run`):
  1. gate: schedule answered; no live session (store live lock); the Mac idle for the approved time; the local hour
     inside the window; A12 clean (else quarantine and stop); disk above the operator's free floor;
  2. take the replay lock (a live session cannot open while it is held);
  3. the retention job (engine/memory/retention.py), which deletes nothing before the operator's answer;
  4. load the night: closed, unflagged sessions not yet replayed, each at its 2-Hz ticks (his 30-Hz face is read
     from the memory map at those ticks only, never loaded whole);
  5. the learning steps of engine/learn/nightly.py, each after a budget check with its memory estimate; a step that
     would pass either budget, or passes one while running, is undone and every later step is deferred to the next
     night; a step that leaves a set (A6, A7, A8) is undone and logged;
  6. save the learned weights (and the last valid copy), the per-person latches, mark the sessions replayed, write
     the night's report to consolidated/replay_log.jsonl.
"""
from __future__ import annotations

import copy
import os
import shutil
import time
from dataclasses import dataclass, field

import numpy as np

from engine.config.innate import ENTRIES
from engine.config.operator import require
from engine.learn import nightly as NL
from engine.learn import projections as PJ
from engine.learn import weights as WB
from engine.memory.retention import run_retention
from engine.memory.store import SCHEMAS, Store, StoreRefused, enforce_a12

BUDGET = ENTRIES["replay_budget"].value
WALL_S = float(BUDGET["wall_s"])
MEM_BYTES = int(BUDGET["memory_gb"] * 1024 ** 3)
DISK_FLOOR = float(ENTRIES["m1_thresholds"].value["disk_floor_fraction"])
TICK_STREAMS = ("own_loads", "drivers", "xi_A", "cone_lateral", "z_T")


def current_rss() -> int:
    """Resident memory of this process in bytes (Linux /proc; elsewhere the peak from getrusage)."""
    try:
        with open("/proc/self/statm") as f:
            return int(f.read().split()[1]) * os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError, IndexError):
        import resource
        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(r if os.uname().sysname == "Darwin" else r * 1024)


class Budget:
    """Wall clock and memory budget of one night. `check(extra)` raises BudgetExceeded when the elapsed time has
    reached the wall budget or the resident memory plus `extra` bytes would pass the memory budget."""

    def __init__(self, wall_s: float = WALL_S, mem_bytes: int = MEM_BYTES, clock=time.monotonic, rss=current_rss):
        self.wall_s, self.mem_bytes, self.clock, self.rss = float(wall_s), int(mem_bytes), clock, rss
        self.t0 = clock()
        self.peak = 0

    def elapsed(self) -> float:
        return self.clock() - self.t0

    def check(self, extra: int = 0) -> None:
        m = int(self.rss())
        self.peak = max(self.peak, m + int(extra))
        if self.elapsed() >= self.wall_s:
            raise NL.BudgetExceeded(f"wall budget {self.wall_s:.0f} s reached")
        if m + int(extra) > self.mem_bytes:
            raise NL.BudgetExceeded(f"memory budget {self.mem_bytes} bytes would be passed")


@dataclass
class ReplayReport:
    ran: bool
    reason: str = ""
    sessions: list = field(default_factory=list)
    skipped_flagged: list = field(default_factory=list)
    steps: list = field(default_factory=list)            # (name, status, detail)
    violations: list = field(default_factory=list)
    lr_scale: float = 1.0
    elapsed_s: float = 0.0
    peak_bytes: int = 0
    retention: object = None


def _at_ticks(mm, n_ticks: int, hz: float) -> np.ndarray:
    """Rows of a stream at the 2-Hz ticks (nearest earlier row), float64; zeros where the stream has no row."""
    w = mm.shape[1]
    out = np.zeros((n_ticks, w))
    if mm.shape[0] == 0:
        return out
    idx = np.minimum((np.arange(n_ticks) * (hz / NL.SLOW_HZ)).astype(np.int64), mm.shape[0] - 1)
    out[:] = np.asarray(mm[idx], dtype=np.float64)
    return out


def load_session(reader) -> NL.SessionData:
    body = np.asarray(reader.array("body"), dtype=np.float64)
    n = body.shape[0]
    streams = {}
    for s in TICK_STREAMS:
        streams[s] = _at_ticks(reader.array(s), n, SCHEMAS[s]["hz"])
    his = [(e.text, e.t) for e, _ in reader.transcript() if e.speaker == "his"]
    return NL.SessionData(reader.sid, reader.manifest["identity"], float(reader.manifest["t0"]), body,
                          streams["own_loads"], streams["drivers"], streams["xi_A"], streams["cone_lateral"],
                          streams["z_T"], _at_ticks(reader.array("own_face"), n, SCHEMAS["own_face"]["hz"]),
                          _at_ticks(reader.array("u"), n, SCHEMAS["u"]["hz"]),
                          _at_ticks(reader.array("rendered"), n, SCHEMAS["rendered"]["hz"]), his, reader.events())


class Replay:
    def __init__(self, store: Store, learned, switches: dict | None = None, budget: Budget | None = None,
                 disk_usage=shutil.disk_usage, dyad_prior=None):
        self.store, self.L, self.switches = store, learned, switches
        self.budget = budget
        self.disk_usage = disk_usage
        self.dyad_prior = dyad_prior

    # ------------------------------------------------------------------------------------------ the gate
    def may_start(self, idle_s: float, local_hour: float) -> tuple:
        try:
            sched = require("nightly_schedule", switches=self.switches)["nightly_schedule"]
        except Exception as e:                              # Unanswered
            return False, str(e)
        if self.store.live():
            return False, "a live session is running"
        if (self.store.root / "replay.lock").exists():
            return False, "replay is already running"
        if float(idle_s) < float(sched["idle_min_s"]):
            return False, f"the Mac has been idle {idle_s:.0f} s < {sched['idle_min_s']:.0f} s"
        a, b = float(sched["start_hour"]), float(sched["end_hour"])
        h = float(local_hour) % 24.0
        inside = a <= h < b if a <= b else (h >= a or h < b)
        if not inside:
            return False, f"hour {h:.2f} outside the approved window {a:g}-{b:g}"
        du = self.disk_usage(self.store.root)
        if du.free < DISK_FLOOR * du.total:
            return False, "disk below the operator's free floor"
        return True, "ok"

    # ------------------------------------------------------------------------------------------ one night
    def run(self, idle_s: float, local_hour: float, now_s: float) -> ReplayReport:
        ok, why = self.may_start(idle_s, local_hour)
        if not ok:
            return ReplayReport(False, why)
        enforce_a12(self.store.root)                         # A12 at every night: quarantine and stop on a hit
        try:
            self.store._take("replay.lock")
        except StoreRefused as e:
            return ReplayReport(False, str(e))
        try:
            return self._night(now_s)
        finally:
            self.store._release("replay.lock")

    def _night(self, now_s: float) -> ReplayReport:
        budget = self.budget if self.budget is not None else Budget()
        rep = ReplayReport(True, "ok")
        rep.retention = run_retention(self.store, now_s, self.switches)
        readers = [s for s in self.store.sessions() if s.manifest.get("t_end") is not None
                   and not s.manifest.get("replayed")]
        flagged = [s for s in readers if s.manifest["flags"].get("A5") or s.manifest["flags"].get("A14")]
        rep.skipped_flagged = [s.sid for s in flagged]
        todo = [s for s in readers if s not in flagged]
        persons = self.store.read_json("persons.json", {"agent": {}, "persons": {}})
        theta0 = NL.restore(self.L, self.store.load_arrays("learned.npz"))
        sessions = []
        try:
            for r in todo:
                budget.check()
                sessions.append(load_session(r))
        except NL.BudgetExceeded as e:                       # nothing learned, nothing saved; next night again
            rep.steps = [("load", "stopped at budget", str(e))] + [(n, "deferred", "loading reached a budget")
                                                                   for n, _, _ in NL.STEPS]
            rep.elapsed_s, rep.peak_bytes = budget.elapsed(), budget.peak
            self.store.append_log("replay_log.jsonl", {"t": float(now_s), "stopped": str(e)})
            return rep
        rep.sessions = [s.sid for s in sessions]
        drops = [float(ev.get("amp", 0.0)) for s in sessions for ev in s.events if ev.get("kind") == "drop_event"]
        rep.lr_scale = WB.lr_scale(drops)
        night = NL.Night(self.L, persons, sessions, check=budget.check, theta0=theta0, lr=rep.lr_scale,
                         dyad_prior=self.dyad_prior)
        data_bytes = sum(s.nbytes() for s in sessions)
        last_valid = NL.export(self.L, theta0)
        deferred = False
        for name, fn, parts in NL.STEPS:
            if fn is None:
                rep.steps.append((name, "not built", parts))
                continue
            if deferred:
                rep.steps.append((name, "deferred", "an earlier step reached a budget"))
                continue
            snap = NL.snapshot(self.L, parts)
            dsnap = {p: copy.deepcopy(getattr(self.L, p)) for p in parts if isinstance(getattr(self.L, p), dict)}
            psnap = copy.deepcopy(night.persons)
            trained = {p: getattr(self.L, p).trained for p in parts if hasattr(getattr(self.L, p), "trained")}
            try:
                budget.check(4 * data_bytes)
                detail = fn(night)
            except NL.BudgetExceeded as e:
                NL.put_back(self.L, snap)
                night.persons.clear()
                night.persons.update(psnap)
                for p, t in trained.items():
                    getattr(self.L, p).trained = t
                for p, d in dsnap.items():
                    setattr(self.L, p, d)
                rep.steps.append((name, "stopped at budget", str(e)))
                deferred = True
                continue
            bad = PJ.check_all(self.L, night.omegas(), self.dyad_prior) + NL.carried_levels_in_range(night.persons)
            if bad:
                NL.put_back(self.L, snap)
                night.persons.clear()
                night.persons.update(psnap)
                for p, t in trained.items():
                    getattr(self.L, p).trained = t
                for p, d in dsnap.items():
                    setattr(self.L, p, d)
                rep.violations += [(name,) + tuple(b) for b in bad]
                rep.steps.append((name, "undone", f"left its set: {bad[:3]}"))
                continue
            rep.steps.append((name, "done", detail))
        final = PJ.check_all(self.L, night.omegas(), self.dyad_prior)
        if final:                                            # never expected: every step was checked
            NL.restore(self.L, last_valid)
            rep.violations += [("final",) + tuple(b) for b in final]
        else:
            self.store.save_arrays("learned_last_valid.npz", last_valid)
        self.store.save_arrays("learned.npz", NL.export(self.L, night.theta0))
        self.store.write_json("persons.json", night.persons)
        if not deferred:
            for r in todo:
                r.set_replayed()
        rep.elapsed_s, rep.peak_bytes = budget.elapsed(), budget.peak
        self.store.append_log("replay_log.jsonl", {
            "t": float(now_s), "sessions": rep.sessions, "skipped_flagged": rep.skipped_flagged,
            "steps": [[n, s, str(d)] for n, s, d in rep.steps], "violations": [str(v) for v in rep.violations],
            "lr_scale": rep.lr_scale, "elapsed_s": rep.elapsed_s, "peak_bytes": rep.peak_bytes})
        return rep
