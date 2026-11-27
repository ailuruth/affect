"""`make eval-dry`: every harness of the battery end to end on synthetic stand-ins (eval/synthetic.py), to test the
harness itself. Nothing here is evidence: every prediction is registered with `synthetic: true`, every result file is
marked synthetic, and the output goes to a temporary directory (never research/build/results/).

Order: (1) every prediction of the dry run is registered (timestamp + hash) before any run starts; (2) the runs, each
opened and scored through the registry; (3) the F-list table, the run plan and a summary.

The predictions here are mechanism-level ones the derivation fixes exactly (a disabled part reads its constant, a
sham of an unread part moves nothing, a face clamp leaves the T state bit-identical, ...) plus a few that the
synthetic stand-ins may or may not meet; a failed synthetic prediction is reported, not hidden, and says nothing
about the engine's behaviour with people.

Usage: python -m eval.dry_run [--out DIR] [--quick]
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from engine.config.channels import TABLE
from eval import config as C
from eval import drive, flist, synthetic
from eval.f22_delayed_copy import plan_full, run_people
from eval.lesions import run_lesion
from eval.mirror import run_mirror
from eval.registry import Prediction, Registry
from eval.results import score_record, write_csv, write_json
from eval.steering import replace_channels, run_clamp, run_steering, scale_channels
from eval.surrogates import run_surrogates
from eval.switches import LESIONS


@dataclass
class Config:
    fs: float = 10.0
    lesion_instances: int = 20
    lesion_seconds: float = 12.0
    steer_seconds: float = 30.0
    steer_t: float = 10.0
    surrogate_people: int = 4
    surrogate_seconds: float = 180.0
    surrogate_n: int = C.SURROGATE_N
    month_sessions: int = C.MONTH_SWAP_MIN_SESSIONS
    month_seconds: float = 30.0
    mirror_minutes: float = 6.0
    f22_seconds: float = 720.0
    f22_delays: tuple = C.F22_DELAYS_S
    f22_max_lag_s: float = C.F22_MAX_LAG_S
    ledger_lesion_seconds: float = 720.0
    ledger_lesion_instances: int = 2


QUICK = Config(lesion_instances=3, lesion_seconds=12.0, steer_seconds=16.0, steer_t=6.0, surrogate_people=3,
               surrogate_seconds=90.0, surrogate_n=60, month_seconds=8.0, mirror_minutes=1.5, f22_seconds=200.0,
               f22_delays=(10, 40, 120), f22_max_lag_s=150.0, ledger_lesion_seconds=200.0, ledger_lesion_instances=1)

ENGINE_LESIONS = {
    "qhat_zero": ("q_hat.lesioned", "eq", 0.0, "with q-hat <- 0, q-hat reads 0 at every tick and the own-laugh "
                  "envelope stays 0"),
    "gate_go_const": ("g_o.lesioned", "eq", 1.0, "with g_o <- 1 the own-display gate reads 1 at every frame"),
    "gate_g_const": ("g.lesioned", "eq", 1.0, "with g <- 1 the echo gate reads 1 at every frame"),
    "listener_zero": ("L_d_abs.lesioned", "eq", 0.0, "with L_d <- 0 the listener display is 0 at every tick"),
    "dtau_removed": ("assert_failures.lesioned", "eq", 0.0, "with D_tau held at 0 the run stays free of assertion "
                     "failures (A5 holds: the held copy reaches both runs)"),
    "p_name_removed": ("assert_failures.lesioned", "eq", 0.0, "with P_name removed no assertion fires"),
}


def _sham_clause(readout_prefix: str) -> dict:
    return {"op": "abs_le", "readout": f"{readout_prefix}.sham_effect_abs_max", "value": 1e-12}


def predictions(cfg: Config) -> list:
    P = []
    for name, (ro, op, v, text) in ENGINE_LESIONS.items():
        crit = {"op": "all", "of": [{"op": op, "readout": ro, "value": v, "tol": 1e-12},
                                     _sham_clause("D"), _sham_clause("smile_laugh_rendered"),
                                     {"op": "eq", "readout": "assert_failures.intact", "value": 0.0}]}
        if name == "qhat_zero":
            crit["of"].append({"op": "eq", "readout": "env_laugh.lesioned", "value": 0.0, "tol": 1e-12})
        P.append(Prediction(f"dry.E1.{name}", text + "; its sham of equal size (an unread part) moves no readout",
                            crit, "lesions", source=LESIONS[name].spec_row, synthetic=True))
    for name in ("ledger_kappa_1", "ledger_lags_0_3"):
        P.append(Prediction(f"dry.E1.{name}", f"{LESIONS[name].how}: the injected delayed copy renders at least as "
                            "high as under the intact ledger (worst slope / c_k not lower)",
                            {"op": "ge", "readout": "copy_worst_c.effect", "value": 0.0}, "lesions",
                            source=LESIONS[name].spec_row, synthetic=True))
    for tgt, ro in (("K", "K"), ("h_word", "h_word"), ("N_L.V", "Dp_word")):
        P.append(Prediction(f"dry.E2.{tgt}", f"a step along {tgt} moves {ro} monotonically with the dose, more than a "
                            "random direction of equal norm in the same block, without assertion failures and "
                            "without moving the zero-ceiling ledger output",
                            {"op": "all", "of": [{"op": "monotone", "readout": "dose_response", "sign": 1},
                                                 {"op": "lt_readout", "readout": "random_abs", "other": "named_abs"},
                                                 {"op": "eq", "readout": "assert_failures", "value": 0.0},
                                                 {"op": "abs_le", "readout": "unrelated_max_abs", "value": 1e-12}]},
                            "steering", source="spec §5.3", synthetic=True))
    P.append(Prediction("dry.E2.omega.smile_laugh", "a step in omega of the smile_laugh group runs without assertion "
                        "failures (dose-response recorded, not predicted on stand-ins)",
                        {"op": "eq", "readout": "assert_failures", "value": 0.0}, "steering", source="spec §5.3",
                        synthetic=True))
    P.append(Prediction("dry.F5.clamp", "scaling only his LP, CR by 0, 0.5 and 2 leaves the T state bit-identical at "
                        "every tick, while the factual output does change",
                        {"op": "all", "of": [{"op": "eq", "readout": "t_state_mismatch_ticks", "value": 0.0},
                                             {"op": "gt", "readout": "output_changed_frames_min", "value": 0.0}]},
                        "steering", falsifier="F5", source="spec §5.1 F5", synthetic=True))
    P.append(Prediction("dry.F23.face_swap", "swapping his whole face for another person's (words fixed) leaves the T "
                        "state, L_d included, bit-identical at every tick",
                        {"op": "eq", "readout": "t_state_mismatch_ticks", "value": 0.0}, "steering",
                        falsifier="F23", source="spec §5.1 F23", synthetic=True))
    for w in C.WINDOWS_S:
        P.append(Prediction(f"dry.E3.bounded.LP.W{w:g}", f"LP's pooled slope on his LP at {w:g} s stays <= c_LP",
                            {"op": "le", "readout": f"observed_c.W{w:g}", "value": 1.0}, "surrogates",
                            falsifier="F1", source="spec §5.4 Bounded", synthetic=True))
    kinds = ("segment_shuffle", "data_slide", "partner_swap", "timing_resample")
    P.append(Prediction("dry.E3.present.LP", "fast coupling of LP on his LP at lags < 1 s (2-s window) exceeds the 95th "
                        "percentile of every surrogate",
                        {"op": "all", "of": [{"op": "gt_quantile", "readout": "observed.W2", "null": f"{k}.W2.dist",
                                              "q": 0.95} for k in kinds]}, "surrogates", source="spec §5.4 Present",
                        synthetic=True))
    P.append(Prediction("dry.E3.present.LP.gain_zero", "under G_k <- 0 on the smile_laugh group the fast coupling is "
                        "gone: not above the segment-shuffle 95th percentile",
                        {"op": "le_quantile", "readout": "observed.W2", "null": "segment_shuffle.W2.dist", "q": 0.95},
                        "surrogates", source="spec §5.4 Present (lesion)", synthetic=True))
    P.append(Prediction("dry.E3.month_swap.LP", "the month-swap surrogate runs on >= 30 sessions; LP's pooled "
                        "2-s slope / c_LP <= 1", {"op": "le", "readout": "observed_c.W2", "value": 1.0}, "surrogates",
                        falsifier="F1", source="spec §5.4 month-swap", synthetic=True))
    P.append(Prediction("dry.mirror", "under a mirror-only partner the T state equals the no-partner run's at every "
                        "tick, no capped channel's conditioned slope exceeds c_k, no channel drifts monotonically, and "
                        "no assertion fires",
                        {"op": "all", "of": [{"op": "eq", "readout": "t_state_mismatch_ticks", "value": 0.0},
                                             {"op": "le", "readout": "slope_c_max", "value": 1.0},
                                             {"op": "eq", "readout": "drift_channels", "value": 0.0},
                                             {"op": "eq", "readout": "assert_failures", "value": 0.0}]},
                        "mirror", source="spec §5.4 mirror-only partner", synthetic=True))
    P.append(Prediction("dry.mirror.ledger_frames", "under the mirror-only partner the ledger changes <= 1 % of frames",
                        {"op": "le", "readout": "ledger_frames_changed", "value": C.LEDGER_FRAMES_MAX}, "mirror",
                        source="spec §5.4 mirror-only partner", synthetic=True))
    for code in ("LP", "BI"):
        P.append(Prediction(f"dry.F22.{code}", f"an injected gain-1 copy of his {code} delayed 10-300 s renders <= 1.0 "
                            f"c_{code} (worst over windows and lags), and the counted routes alone have <= 1 % of "
                            "frames changed",
                            {"op": "all", "of": [{"op": "le", "readout": "worst_c", "value": 1.0},
                                                 {"op": "le", "readout": "frames_changed_counted",
                                                  "value": C.LEDGER_FRAMES_MAX}]},
                            "f22", falsifier="F22", source="spec §5.1 F22", synthetic=True))
    return P


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="synthetic dry run of the evaluation battery (never evidence)")
    ap.add_argument("--out", default=None, help="output directory (default: a new temporary directory)")
    ap.add_argument("--quick", action="store_true", help="the small configuration the test suite uses")
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix="eval-dry-"))
    summary = dry_run(out, QUICK if a.quick else Config())
    for t in summary["tests"]:
        print(f"{'pass' if t['passed'] else 'FAIL'}  {t['test_id']}  ({t['wall_s']:.1f} s)")
    print(f"{summary['passed']}/{len(summary['tests'])} synthetic predictions met; results (synthetic, not evidence) "
          f"in {out}")
    return 0


def dry_run(out: Path, cfg: Config) -> dict:
    out = Path(out)
    t_all = time.perf_counter()
    reg = Registry(out / "registry")
    res_dir = out / "results"
    preds = predictions(cfg)
    for p in preds:                                    # (1) every prediction before any run
        reg.register(p)
    time.sleep(0.001)
    L = synthetic.learned(5)
    fs = cfg.fs
    docs = []

    def timed(fn, *args, **kw):
        t0 = time.perf_counter()
        d = fn(*args, **kw)
        d["wall_s"] = time.perf_counter() - t0
        docs.append(d)
        return d

    # (2a) E1 lesions
    inst = [(synthetic.partner(cfg.lesion_seconds, fs, seed=100 + i), i) for i in range(cfg.lesion_instances)]
    for name in ENGINE_LESIONS:
        timed(run_lesion, reg, f"dry.E1.{name}", name, inst, L, res_dir, True)
    linst = [(synthetic.partner(cfg.ledger_lesion_seconds, fs, seed=200 + i, words_every_s=0, own_every_s=0), i)
             for i in range(cfg.ledger_lesion_instances)]
    for name in ("ledger_kappa_1", "ledger_lags_0_3"):
        timed(run_lesion, reg, f"dry.E1.{name}", name, linst, L, res_dir, True, delays=cfg.f22_delays,
              max_lag_s=cfg.f22_max_lag_s)

    # (2b) E2 steering and input clamps
    ps = synthetic.partner(cfg.steer_seconds, fs, seed=300)
    steps = {"K": 0.05, "h_word": 0.05, "N_L.V": 0.05, "omega.smile_laugh": 0.1}
    for tgt, step in steps.items():
        ro = {"K": "K", "h_word": "h_word", "N_L.V": "Dp_word", "omega.smile_laugh": "partner_part_abs"}[tgt]
        timed(run_steering, reg, f"dry.E2.{tgt}", tgt, ro, ps, L, res_dir, True, step=step, t_s=cfg.steer_t,
              unrelated=("zero_ceiling_x2_abs",))
    timed(run_clamp, reg, "dry.F5.clamp", ps, L,
          {f"LPCRx{f:g}": scale_channels(("LP", "CR"), f) for f in (0.0, 0.5, 2.0)}, res_dir, True)
    other = synthetic.face(cfg.steer_seconds, fs, seed=301)
    timed(run_clamp, reg, "dry.F23.face_swap", ps, L, {"face_swap": replace_channels(TABLE.codes, other)},
          res_dir, True)

    # (2c) E3 surrogates: stored outputs of intact and G_k <- 0 runs
    k = TABLE.index("LP")
    people = [synthetic.partner(cfg.surrogate_seconds, fs, seed=400 + i) for i in range(cfg.surrogate_people)]
    intact = [drive.run(p, L, seed=i) for i, p in enumerate(people)]
    gain0 = [drive.run(p, L, seed=i, lesion=LESIONS["echo_gain_zero_SL"]) for i, p in enumerate(people)]
    us = [tr.U[:, k] for tr in intact]
    kinds = ("segment_shuffle", "data_slide", "partner_swap", "timing_resample")
    kw = dict(kinds=kinds, n=cfg.surrogate_n, lags_s=C.PRESENT_LAGS_S)
    c_lp = float(TABLE.c[k])
    bounded = timed(run_surrogates, reg, "dry.E3.present.LP", us, [tr.x2[:, k] for tr in intact], fs, c_lp,
                    res_dir, True, **kw)
    for w in C.WINDOWS_S:                               # Bounded: scored on the same stored outputs
        tok = reg.start_run(f"dry.E3.bounded.LP.W{w:g}")
        sc = reg.score(tok, bounded["observed"])
        d = score_record(sc, {"harness": "surrogates", "wall_s": 0.0})
        write_json(res_dir / f"dry.E3.bounded.LP.W{w:g}.json", d, True)
        docs.append(d)
    timed(run_surrogates, reg, "dry.E3.present.LP.gain_zero", [tr.U[:, k] for tr in gain0],
          [tr.x2[:, k] for tr in gain0], fs, c_lp, res_dir, True, **kw)
    sess = [synthetic.partner(cfg.month_seconds, fs, seed=500 + i, day=7.0 * i) for i in range(cfg.month_sessions)]
    mtr = [drive.run(p, L, seed=i) for i, p in enumerate(sess)]
    timed(run_surrogates, reg, "dry.E3.month_swap.LP", [t.U[:, k] for t in mtr], [t.x2[:, k] for t in mtr], fs,
          c_lp, res_dir, True, kinds=("segment_shuffle", "data_slide", "month_swap"), n=cfg.surrogate_n,
          days=[p.day for p in sess], windows=(2.0, 10.0) if cfg.month_seconds >= 30 else (2.0,))

    # (2d) mirror-only partner
    timed(run_mirror, reg, "dry.mirror", L, res_dir, True, minutes=cfg.mirror_minutes, fs=fs)
    tok = reg.start_run("dry.mirror.ledger_frames")
    sc = reg.score(tok, docs[-1]["observed"])
    docs.append(dict(score_record(sc, {"harness": "mirror"}), wall_s=0.0))
    write_json(res_dir / "dry.mirror.ledger_frames.json", docs[-1], True)

    # (2e) F22, ledger only, on stand-ins with the engine's own partner-caused part
    f22p = synthetic.partner(cfg.f22_seconds, fs, seed=600)
    f22tr = drive.run(f22p, L, seed=0)
    for code in ("LP", "BI"):
        j = TABLE.index(code)
        t0 = time.perf_counter()
        tok = reg.start_run(f"dry.F22.{code}")
        r = run_people([{"u": f22tr.U[:, j], "r_routes": f22tr.r[:, j]}], float(TABLE.c[j]),
                       fs, delays=cfg.f22_delays, max_lag_s=cfg.f22_max_lag_s)
        sc = reg.score(tok, r)
        d = score_record(sc, {"harness": "f22", "channel": code, "wall_s": time.perf_counter() - t0})
        write_json(res_dir / f"dry.F22.{code}.json", d, True)
        docs.append(d)

    # (3) F-list, run plan, summary
    write_csv(res_dir / "flist.csv", ["fid", "status", "test", "milestone", "machine", "data"], flist.rows(), True)
    plan = plan_full(30.0, 5.0)
    write_json(res_dir / "plan_f22.json", {"plan": plan.as_dict()}, True)
    tests = [{"test_id": d["test_id"], "passed": bool(d["passed"]), "wall_s": float(d.get("wall_s", 0.0))}
             for d in docs]
    summary = {"tests": tests, "passed": sum(t["passed"] for t in tests), "registered": len(preds),
               "wall_s": time.perf_counter() - t_all, "config": cfg.__dict__ | {"f22_delays": list(cfg.f22_delays)},
               "f22_plan_sittings_h": plan.hours, "registry_log_lines": len(reg.verify_log())}
    write_json(res_dir / "summary.json", summary, True)
    (out / "README.txt").write_text("Synthetic dry run of eval/ (make eval-dry). Not evidence.\n", encoding="utf-8")
    return json.loads(json.dumps(summary))


if __name__ == "__main__":
    sys.exit(main())
