"""Each harness of eval/ runs end to end on tiny synthetic stand-ins (harness tests, never evidence): lesions,
steering and input clamps, surrogates (all five kinds), the mirror-only partner, F22 ledger-only, and the dry-run
orchestrator itself. Every readout is internal state."""
import json

import numpy as np
import pytest

from engine.config.channels import TABLE
from eval import drive, synthetic
from eval import surrogates as SG
from eval.dry_run import Config, dry_run
from eval.f22_delayed_copy import copy_of, ledger_only
from eval.lesions import run_lesion
from eval.mirror import run_mirror
from eval.registry import MissingPrediction, Prediction, Registry
from eval.steering import named_direction, random_direction, run_clamp, run_steering, scale_channels
from eval.switches import LESIONS, NotBuilt

FS = 10.0


@pytest.fixture(scope="module")
def L():
    return synthetic.learned(3)


def _reg(tmp_path, tid, crit, harness="lesions"):
    reg = Registry(tmp_path / "reg")
    reg.register(Prediction(tid, "harness test", crit, harness, synthetic=True))
    return reg


def test_drive_readouts_are_internal_state(L):
    tr = drive.run(synthetic.partner(8.0, FS, seed=1), L, seed=0)
    s = drive.summary(tr)
    assert set(s) == set(drive.READOUTS)
    assert tr.safety_log == [] and len(tr.digests) == len(tr.tick_t) == 16
    np.testing.assert_array_equal(tr.rendered, tr.ybar + tr.x2)


def test_lesion_harness_end_to_end(tmp_path, L):
    crit = {"op": "all", "of": [{"op": "eq", "readout": "q_hat.lesioned", "value": 0.0},
                                {"op": "abs_le", "readout": "D.sham_effect_abs_max", "value": 1e-12}]}
    reg = _reg(tmp_path, "t.qhat", crit)
    inst = [(synthetic.partner(8.0, FS, seed=10 + i), i) for i in range(2)]
    doc = run_lesion(reg, "t.qhat", "qhat_zero", inst, L, tmp_path / "res", synthetic=True)
    assert doc["passed"] and doc["observed"]["instances"] == 2
    assert len(doc["observed"]["q_hat.effect_dist"]) == 2
    assert json.loads((tmp_path / "res" / "t.qhat.json").read_text())["synthetic"] is True
    with pytest.raises(ValueError):                              # >= 20 instances outside a synthetic run
        run_lesion(reg, "t.qhat", "qhat_zero", inst, L, tmp_path / "res", synthetic=False)
    with pytest.raises(MissingPrediction):
        run_lesion(reg, "t.unregistered", "qhat_zero", inst, L, tmp_path / "res", synthetic=True)
    with pytest.raises(NotBuilt):
        run_lesion(reg, "t.qhat", "turns_fixed_6s", inst, L, tmp_path / "res", synthetic=True)


def test_ledger_lesion_on_injected_copy(tmp_path, L):
    reg = _reg(tmp_path, "t.kappa", {"op": "ge", "readout": "copy_worst_c.effect", "value": 0.0})
    inst = [(synthetic.partner(150.0, FS, seed=3, words_every_s=0, own_every_s=0), 0)]
    doc = run_lesion(reg, "t.kappa", "ledger_kappa_1", inst, L, tmp_path, True, ledger_channels=("LP",),
                     delays=(10, 40), max_lag_s=60.0)
    o = doc["observed"]
    assert o["copy_worst_c.sham_effect"] == 0.0 and o["copy_worst_c.effect"] == pytest.approx(
        o["copy_worst_c.lesioned"] - o["copy_worst_c.intact"])
    assert doc["passed"] == (o["copy_worst_c.effect"] >= 0.0)


def test_every_lesion_switch_is_documented():
    for name, les in LESIONS.items():
        assert les.part and les.how and les.spec_row and les.sham
        assert les.built or les.reason
        assert les.sham == "sham_unread" or les.sham in LESIONS


def test_steering_harness_end_to_end(tmp_path, L):
    crit = {"op": "all", "of": [{"op": "monotone", "readout": "dose_response", "sign": 1},
                                {"op": "eq", "readout": "assert_failures", "value": 0.0}]}
    reg = _reg(tmp_path, "t.K", crit, "steering")
    ps = synthetic.partner(10.0, FS, seed=4)
    doc = run_steering(reg, "t.K", "K", "K", ps, L, tmp_path, True, step=0.04, t_s=4.0, doses=(-2, -1, 1, 2),
                       unrelated=("zero_ceiling_x2_abs",))
    o = doc["observed"]
    assert doc["passed"] and len(o["dose_response"]) == 4 and o["named_abs"] > 0
    v = random_direction("N_L.V", np.random.default_rng(0))
    assert np.isclose(np.linalg.norm(v), np.linalg.norm(named_direction("N_L.V")))


def test_input_clamp_leaves_t_state_bit_identical(tmp_path, L):
    crit = {"op": "eq", "readout": "t_state_mismatch_ticks", "value": 0.0}
    reg = _reg(tmp_path, "t.F5", crit, "steering")
    ps = synthetic.partner(10.0, FS, seed=5)
    doc = run_clamp(reg, "t.F5", ps, L, {"x0": scale_channels(("LP", "CR"), 0.0),
                                         "x2": scale_channels(("LP", "CR"), 2.0)}, tmp_path, True)
    assert doc["passed"] and doc["observed"]["output_changed_frames_min"] > 0


def test_surrogate_kinds_and_refusals():
    r = np.random.default_rng(0)
    u = r.standard_normal(3000)
    assert sorted(SG.segment_shuffle(u, FS, r)) == sorted(u)
    assert sorted(SG.data_slide(u, FS, r)) == sorted(u)
    assert SG.timing_resample(u, FS, r).shape == u.shape
    with pytest.raises(SG.SurrogateRefused):
        SG.Battery(FS, kinds=("segment_shuffle", "partner_swap"))
    with pytest.raises(SG.SurrogateRefused):
        SG.month_swap_index(0, [float(d) for d in range(29)], r)
    j = SG.month_swap_index(0, [7.0 * d for d in range(30)], r)
    assert j >= 4


def test_surrogate_battery_separates_coupling_from_none(tmp_path):
    r = np.random.default_rng(1)
    us = [synthetic.channel(1800, FS, r) for _ in range(3)]
    coupled = [np.concatenate([np.zeros(5), u[:-5]]) * 0.3 + 0.01 * r.standard_normal(u.size) for u in us]
    indep = [synthetic.channel(1800, FS, r) * 0.3 for _ in range(3)]
    kinds = ("segment_shuffle", "data_slide", "partner_swap", "timing_resample", "month_swap")
    b = SG.Battery(FS, windows=(2.0, 10.0), lags_s=(0.0, 0.5), n=100, kinds=kinds[:4])
    rc, ri = b.run(us, coupled), b.run(us, indep)
    assert rc["observed.W2"] > rc["surrogate_q95_max.W2"]
    assert ri["observed.W2"] <= ri["surrogate_q95_max.W2"] + 0.05
    # the re-run path (engine re-driven with the surrogate face, words fixed): here a stand-in callable
    rr = b.run(us, coupled, rerun=lambda i, face: np.concatenate([np.zeros(5), face[:-5]]) * 0.3, n_rerun=5)
    assert rr["n"]["partner_swap"] == 5 and rr["n"]["segment_shuffle"] == 100
    crit = {"op": "gt_quantile", "readout": "observed.W2", "null": "data_slide.W2.dist", "q": 0.95}
    reg = _reg(tmp_path, "t.E3", crit, "surrogates")
    days = [7.0 * d for d in range(30)]
    us30 = [synthetic.channel(300, FS, r) for _ in range(30)]
    ys30 = [0.3 * u for u in us30]
    doc = SG.run_surrogates(reg, "t.E3", us30, ys30, FS, 0.35, tmp_path, True, kinds=("segment_shuffle", "data_slide",
                            "month_swap"), n=50, windows=(2.0,), days=days)
    assert doc["passed"] and doc["observed"]["observed_c.W2"] == pytest.approx(0.3 / 0.35)


def test_mirror_harness_end_to_end(tmp_path, L):
    crit = {"op": "eq", "readout": "t_state_mismatch_ticks", "value": 0.0}
    reg = _reg(tmp_path, "t.mirror", crit, "mirror")
    doc = run_mirror(reg, "t.mirror", L, tmp_path, True, minutes=0.4, fs=FS)
    o = doc["observed"]
    assert doc["passed"] and o["ticks"] == 48 and 0.0 <= o["ledger_frames_changed"] <= 1.0


def test_f22_ledger_only_batched_over_delays():
    u = synthetic.channel(1500, FS, np.random.default_rng(2))
    x = copy_of(u, 10.0, FS)
    assert x.shape == u.shape and abs(x[:100].std()) < abs(x[200:].std()) + 1.0
    r = ledger_only(u, float(TABLE.c[TABLE.index("LP")]), FS, delays=(10, 20), max_lag_s=30.0)
    assert np.asarray(r["worst_c"]).shape == (3, 2) and r["frames_changed_counted"] == 0.0


def test_dry_run_orchestrator_tiny(tmp_path):
    tiny = Config(lesion_instances=1, lesion_seconds=6.0, steer_seconds=8.0, steer_t=3.0, surrogate_people=2,
                  surrogate_seconds=40.0, surrogate_n=20, month_seconds=3.0, mirror_minutes=0.3, f22_seconds=60.0,
                  f22_delays=(10,), f22_max_lag_s=20.0, ledger_lesion_seconds=60.0, ledger_lesion_instances=1)
    s = dry_run(tmp_path, tiny)
    assert len(s["tests"]) == s["registered"] == 24
    files = list((tmp_path / "results").iterdir())
    assert files and all(p.suffix in (".json", ".csv") for p in files)
    assert all(json.loads(p.read_text())["synthetic"] is True for p in files if p.suffix == ".json")
    assert all(max(h for h in s["f22_plan_sittings_h"]) <= 5.0 for _ in [0])
