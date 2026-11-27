"""E1: the lesion harness (spec §5.2; evaluation.md E1; design §7).

For each instance (a partner session and a seed): the intact engine, the lesioned engine (a switch of
eval/switches.py) and its sham of equal size run on the same inputs; every readout is an internal-state quantity
(eval/drive.summary: body fields, drive, gates, the partner-caused part, the ledger's frames, assertion failures).
The observed results are, per readout, the means over instances of the intact, lesioned and sham values, of the
effect (lesioned - intact) and of the sham effect (sham - intact), with the full per-instance distributions.

Ledger lesions (lag scan, kappa) are read on an injected delayed copy, ledger only (eval/f22_delayed_copy): readout
`copy_worst_c` (worst slope / c_k over delays, windows, lags) and `frames_changed_counted`.

Order (the registry enforces it): the prediction is registered before `run_lesion`; `run_lesion` opens the run
(refused if the prediction is missing or late), times the first instance as its pilot and refuses a sitting predicted
above 5 h without split / approved (planner.guard), runs, scores the prediction as written, and writes the result.
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from eval import config as C
from eval import drive, planner
from eval.registry import Registry
from eval.results import score_record, write_json
from eval.switches import LESIONS, NotBuilt, Sham


def _ledger_readouts(ps, lesion_name, channels, delays, max_lag_s):
    from engine.config.channels import TABLE
    from eval.f22_delayed_copy import ledger_only
    out = {"copy_worst_c": -np.inf, "frames_changed_counted": 0.0}
    for code in channels:
        k = TABLE.index(code)
        r = ledger_only(ps.U[:, k], float(TABLE.c[k]), ps.fs, delays=delays, lesion=lesion_name, max_lag_s=max_lag_s)
        out["copy_worst_c"] = max(out["copy_worst_c"], float(np.nanmax(r["worst_c"])))
        out["frames_changed_counted"] = max(out["frames_changed_counted"], r["frames_changed_counted"])
    return out


def run_lesion(registry: Registry, test_id: str, lesion_name: str, instances, learned, out_dir,
               synthetic: bool, min_instances: int = C.LESION_MIN_INSTANCES, split: bool = False,
               approved: str | None = None, ledger_channels=("LP", "BI"), delays=C.F22_DELAYS_S,
               max_lag_s: float = C.F22_MAX_LAG_S) -> dict:
    """instances: list of (PartnerSession, seed). Returns the result document (also written to out_dir)."""
    lesion = LESIONS[lesion_name]
    if not lesion.built:
        raise NotBuilt(f"{lesion_name}: {lesion.reason}")
    if len(instances) < min_instances and not synthetic:
        raise ValueError(f"{lesion_name}: {len(instances)} instances < {min_instances} (spec §5.2)")
    tok = registry.start_run(test_id)
    rows = []
    t0 = time.perf_counter()
    for i, (ps, seed) in enumerate(instances):
        if lesion.kind == "ledger":
            a = _ledger_readouts(ps, None, ledger_channels, delays, max_lag_s)
            b = _ledger_readouts(ps, lesion_name, ledger_channels, delays, max_lag_s)
            s = dict(a)                                    # sham_unread touches no ledger: the sham is the intact ledger
        else:
            a = drive.summary(drive.run(ps, learned, seed=seed))
            b = drive.summary(drive.run(ps, learned, lesion=lesion, seed=seed))
            s = drive.summary(drive.run(ps, learned, lesion=Sham(lesion, learned, seed), seed=seed))
        rows.append((a, b, s))
        if i == 0:
            pred_h = (time.perf_counter() - t0) * len(instances) / 3600.0
            planner.guard(pred_h, split=split, approved=approved)
    observed = {"instances": len(rows)}
    for k in rows[0][0]:
        ia = np.array([r[0][k] for r in rows])
        ib = np.array([r[1][k] for r in rows])
        isham = np.array([r[2][k] for r in rows])
        observed.update({f"{k}.intact": ia.mean(), f"{k}.lesioned": ib.mean(), f"{k}.sham": isham.mean(),
                         f"{k}.effect": (ib - ia).mean(), f"{k}.sham_effect": (isham - ia).mean(),
                         f"{k}.effect_abs_max": np.abs(ib - ia).max(), f"{k}.sham_effect_abs_max": np.abs(isham - ia).max(),
                         f"{k}.effect_dist": (ib - ia).tolist(), f"{k}.sham_effect_dist": (isham - ia).tolist()})
    observed = {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in observed.items()}
    sc = registry.score(tok, observed)
    doc = score_record(sc, {"harness": "lesions", "lesion": lesion_name, "part": lesion.part, "how": lesion.how,
                            "sham": lesion.sham, "wall_s": time.perf_counter() - t0})
    write_json(Path(out_dir) / f"{test_id}.json", doc, synthetic)
    return doc
