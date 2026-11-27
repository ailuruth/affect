"""The run planner respects machine.md's sitting rule: no sitting is planned above 5 h, a single sitting predicted
above 6 h is refused without the operator's recorded answer, and §5.5's F22 recipe splits and subsamples."""
import pytest

from eval import config as C
from eval import planner as P


def test_guard():
    assert "<=" in P.guard(4.9)
    with pytest.raises(P.Refused):
        P.guard(5.5)
    with pytest.raises(P.Refused):
        P.guard(5.5, split=True)                                   # split means: through plan(), in chunks
    assert "approval" in P.guard(5.5, approved="operator, 2026-11-27: yes")
    with pytest.raises(P.Refused):
        P.guard(7.0)
    with pytest.raises(P.Refused):
        P.guard(7.0, approved="  ")
    with pytest.raises(P.Refused):
        P.guard(1.0, memory_gb=8.0)


def test_plan_never_exceeds_the_limit():
    units = [P.Unit(f"u{i}", h, divisible=4) for i, h in enumerate((0.5, 4.0, 4.9, 1.2, 9.5, 3.3, 0.1))]
    plan = P.plan(units)
    assert plan.hours and max(plan.hours) <= C.SITTING_START_LIMIT_H + 1e-9
    assert plan.total_h == pytest.approx(sum(u.hours for u in units))
    assert any("split" in n for n in plan.notes)
    with pytest.raises(P.Refused):
        P.plan([P.Unit("big", 12.0, divisible=1)])
    with pytest.raises(P.Refused):
        P.plan([P.Unit("mem", 1.0, memory_gb=7.0)])
    assert P.plan([P.Unit("big", 12.0)], approved="operator: yes").hours == [12.0]


def test_f22_plan_of_the_spec_example():
    """§5.5: 12 delays x 50 people x 2 h at 30 Hz at about 1 ms per frame naively is about 36 CPU-hours; batched and
    spread over the cores it must come out as sittings of <= 5 h."""
    per_frame_batch12 = 1e-3 / 12 * 1.5                          # batched cost per (person x delay) at batch 12
    plan = P.f22_plan(per_frame_batch12)
    assert max(plan.hours) <= C.SITTING_START_LIMIT_H
    assert sum(len(s) for s in plan.sittings) == 20               # every capped channel planned
    slow = P.f22_plan(2.5e-3)                                     # too slow at 50 people: subsampled to 25
    assert any("subsampled" in n for n in slow.notes) and max(slow.hours) <= C.SITTING_START_LIMIT_H
    with pytest.raises(P.Refused):
        P.f22_plan(5e-3)                                          # even 25 people exceed a sitting: ask


def test_pilot_times_a_step():
    assert P.pilot(lambda i: sum(range(100)), 5) >= 0.0
