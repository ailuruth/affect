"""The run planner (research/machine.md budget rules; spec §5.5).

machine.md: ask the operator before any run expected to take more than about 6 hours; plan peak memory <= 6 GB.
Spec §5.5: every eval script predicts its wall time from a pilot and refuses to start a single sitting predicted
above 5 h unless given `split` (nightly chunks, checkpointed, resumable) or `approved` (the operator's answer,
recorded in the run log). A sitting predicted above 6 h is never started without that answer, split or not.

  pilot(step, n)        seconds per call of `step` (a timing pilot on a small piece)
  Unit                  one checkpointable piece of work (e.g. one channel x delay of F22) with its predicted cost
  plan(units, ...)      packs units into sittings of <= limit_h each (longest first, first fit); a unit larger than
                        the limit is split into resumable chunks if it is divisible, else the plan refuses it
  guard(hours, ...)     the start check of a single sitting
  f22_plan(...)         §5.5's F22 recipe: batch, channels over the performance cores, split by channel across
                        nights; if a channel still exceeds a sitting, subsample people to 25 (stated); else refuse
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

from eval import config as C


class Refused(Exception):
    pass


def pilot(step, n: int = 50) -> float:
    """Mean wall seconds per call of step(i) over n calls (after one warm-up call)."""
    step(0)
    t0 = time.perf_counter()
    for i in range(n):
        step(i + 1)
    return (time.perf_counter() - t0) / max(n, 1)


@dataclass
class Unit:
    name: str
    hours: float
    divisible: int = 1                 # how many resumable chunks it can be cut into (1: not divisible)
    memory_gb: float = 0.5


@dataclass
class Plan:
    sittings: list = field(default_factory=list)     # each: list of (unit name, hours)
    limit_h: float = C.SITTING_START_LIMIT_H
    notes: list = field(default_factory=list)

    @property
    def hours(self) -> list:
        return [sum(h for _, h in s) for s in self.sittings]

    @property
    def total_h(self) -> float:
        return sum(self.hours)

    def as_dict(self) -> dict:
        return {"limit_h": self.limit_h, "sittings": [[list(x) for x in s] for s in self.sittings],
                "hours": self.hours, "total_h": self.total_h, "notes": self.notes}


def guard(hours: float, split: bool = False, approved: str | None = None, memory_gb: float = 0.0,
          limit_h: float = C.SITTING_START_LIMIT_H) -> str:
    """Start check of one sitting. Returns the reason it may start; raises Refused otherwise."""
    if memory_gb > C.MEMORY_LIMIT_GB and not approved:
        raise Refused(f"predicted peak memory {memory_gb:.1f} GB > {C.MEMORY_LIMIT_GB} GB (machine.md)")
    if hours <= limit_h:
        return f"predicted {hours:.2f} h <= {limit_h} h"
    if approved and str(approved).strip():
        return f"predicted {hours:.2f} h; operator approval recorded: {approved.strip()}"
    if hours > C.ASK_LIMIT_H:
        raise Refused(f"predicted {hours:.2f} h in one sitting > {C.ASK_LIMIT_H} h: ask the operator first "
                      "(machine.md); pass the recorded answer as approved, or plan it split")
    if split:
        raise Refused(f"predicted {hours:.2f} h > {limit_h} h: run it through plan() in chunks, not as one sitting")
    raise Refused(f"predicted {hours:.2f} h > {limit_h} h: give split (nightly chunks) or approved")


def plan(units, limit_h: float = C.SITTING_START_LIMIT_H, approved: str | None = None) -> Plan:
    out = Plan(limit_h=limit_h)
    pieces = []
    for u in units:
        if u.memory_gb > C.MEMORY_LIMIT_GB and not approved:
            raise Refused(f"{u.name}: predicted peak memory {u.memory_gb:.1f} GB > {C.MEMORY_LIMIT_GB} GB")
        if u.hours <= limit_h:
            pieces.append((u.name, u.hours))
            continue
        k = math.ceil(u.hours / limit_h)
        if k > u.divisible:
            if approved:
                out.notes.append(f"{u.name}: {u.hours:.2f} h in one sitting, approved: {approved}")
                pieces.append((u.name, u.hours))
                continue
            raise Refused(f"{u.name}: {u.hours:.2f} h cannot be cut into chunks of <= {limit_h} h "
                          f"(divisible into {u.divisible}); ask the operator")
        out.notes.append(f"{u.name}: split into {k} resumable chunks")
        pieces += [(f"{u.name}#{i + 1}/{k}", u.hours / k) for i in range(k)]
    for name, h in sorted(pieces, key=lambda p: -p[1]):
        for s in out.sittings:
            if sum(x for _, x in s) + h <= limit_h + 1e-12:
                s.append((name, h))
                break
        else:
            out.sittings.append([(name, h)])
    return out


def f22_plan(per_frame_s: float, people: int = C.F22_MIN_PEOPLE, delays: int = len(C.F22_DELAYS_S),
             channels: int = 20, fs: float = 30.0, hours_per_person: float = C.F22_HOURS_PER_PERSON,
             cores: int = C.PERFORMANCE_CORES, batch_scale=None, limit_h: float = C.SITTING_START_LIMIT_H,
             approved: str | None = None) -> Plan:
    """Spec §5.5 for F22. per_frame_s: the pilot's cost of one batched ledger frame step for one channel at the
    pilot's batch; batch_scale(people * delays) -> the factor by which a larger batch costs more (default linear in
    the batch above the pilot's 12). Channels run in parallel on `cores` processes. Returns the plan of sittings."""
    frames = hours_per_person * 3600.0 * fs
    scale = batch_scale or (lambda b: max(1.0, b / float(delays)))
    notes = []
    for n_people in (people, C.F22_SUBSAMPLE_PEOPLE):
        ch_h = per_frame_s * scale(n_people * delays) * frames / 3600.0
        if ch_h <= limit_h:
            break
        notes.append(f"{n_people} people: one channel predicted {ch_h:.2f} h > {limit_h} h")
    else:
        if not approved:
            raise Refused(f"F22: one channel predicted {ch_h:.2f} h even at {C.F22_SUBSAMPLE_PEOPLE} people; "
                          "ask the operator (machine.md)")
    if n_people < people:
        notes.append(f"people subsampled {people} -> {n_people} (each person's {hours_per_person} h kept); "
                     "the power loss is stated in the report")
    # channels in parallel on the cores: a sitting holds up to `cores` channels per round
    units = [Unit(f"F22 channel {k + 1}", ch_h, divisible=1) for k in range(channels)]
    rounds = math.ceil(channels / cores)
    p = Plan(limit_h=limit_h, notes=notes)
    per_sitting = max(1, int(limit_h // ch_h)) if ch_h > 0 else rounds
    for r0 in range(0, rounds, per_sitting):
        s = []
        for r in range(r0, min(rounds, r0 + per_sitting)):
            s += [(u.name, ch_h / min(cores, channels - r * cores)) for u in units[r * cores:(r + 1) * cores]]
        p.sittings.append(s)
    p.notes.append(f"{channels} channels x {delays} delays x {n_people} people; {cores} processes; "
                   f"{len(p.sittings)} sitting(s) of <= {limit_h} h, checkpointed per channel x delay")
    return p
