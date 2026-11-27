"""The mirror-only partner against no partner (spec §5.4, report 9; "the G-mirror test").

Two runs of the same length, same agent turns, same seed: (a) a partner who only mirrors the agent: his channels are
the agent's own rendered output 0.3 s earlier (eval/drive.Mirror, gain 1), and he says nothing; (b) no partner at
all: his channels held at the same neutral baseline throughout. Claim (D78-4): under the mirror the agent's state
and output do not settle into a copy:
  - `ledger_frames_changed`   fraction of frames the ledger changed the partner-caused part (mirror run);
  - `slope_c_max`             the worst conditioned block-mean slope (the rendered partner-caused part, rendered -
                              ybar = x2, on his channel = the agent's own past output), over capped channels, windows
                              2 s / 10 s / 1 min (each with >= 10 blocks) and lags 0-5 s, as a fraction of c_k;
  - `drift_channels`          channels whose mean moves monotonically over 6 blocks (5 min each in 30 min) by more
                              than 0.1 c_k, in the mirror run, beyond the no-partner run's own drift;
  - `t_state_mismatch_ticks`  2-Hz ticks at which the T-state digest differs between the runs (exactly 0 by the type
                              rule: his face is F, and neither partner says a word);
  - `mean_offset_c_max`       the largest |mean(mirror) - mean(no partner)| / c_k over capped channels.
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from engine.config.channels import TABLE
from eval import config as C
from eval import drive, planner
from eval.metrics import monotone_drift, worst_block_slope
from eval.registry import Registry
from eval.results import score_record, write_json

SIGNED = np.array([s == "signed" for s in TABLE.signs])
C_K = np.asarray(TABLE.c, float)
CAPPED = C_K > 0


def neutral_base() -> np.ndarray:
    return np.where(SIGNED, 0.0, 0.15)


def run_mirror(registry: Registry, test_id: str, learned, out_dir, synthetic: bool, minutes: float = C.MIRROR_MINUTES,
               fs: float = 30.0, seed: int = 0, own_every_s: float = 11.0, lags_s=(0.0, 1.0, 2.0, 5.0),
               split: bool = False, approved: str | None = None) -> dict:
    tok = registry.start_run(test_id)
    seconds = minutes * 60.0
    base = neutral_base()
    own = tuple((float(t), ("a", "placeholder", "reply")) for t in np.arange(9.0, seconds, own_every_s)) \
        if own_every_s else ()
    T = int(round(seconds * fs))
    still = drive.PartnerSession(U=np.tile(base, (T, 1)), fs=fs, own_heard=own, pid="no-partner")
    mir = drive.PartnerSession(U=None, fs=fs, own_heard=own, pid="mirror", seconds=seconds)
    t0 = time.perf_counter()
    tr_none = drive.run(still, learned, seed=seed, b_id=np.concatenate([base, np.zeros(3)]))
    planner.guard(2 * (time.perf_counter() - t0) / 3600.0, split=split, approved=approved)
    tr_mir = drive.run(mir, learned, seed=seed, mirror=drive.Mirror(base, C.MIRROR_GAIN, C.MIRROR_LAG_S))
    ws = worst_block_slope(tr_mir.U[:, CAPPED], tr_mir.x2[:, CAPPED], fs, lags_s, C.WINDOWS_S,
                           min_blocks=C.MIRROR_MIN_BLOCKS)
    slope_c = np.fmax.reduce(ws, axis=0) / C_K[CAPPED]          # NaN: no window with enough blocks
    drift = []
    for k in np.nonzero(CAPPED)[0]:
        tol = C.DRIFT_TOL_C * C_K[k]
        if monotone_drift(tr_mir.rendered[:, k], C.DRIFT_BLOCKS, tol) and not \
                monotone_drift(tr_none.rendered[:, k], C.DRIFT_BLOCKS, tol):
            drift.append(TABLE.codes[k])
    mism = sum(a != b for a, b in zip(tr_mir.digests, tr_none.digests)) + abs(len(tr_mir.digests) - len(tr_none.digests))
    off = np.abs(tr_mir.rendered.mean(0) - tr_none.rendered.mean(0))[CAPPED] / C_K[CAPPED]
    observed = {
        "ledger_frames_changed": drive.frames_changed(tr_mir),
        "ledger_frames_changed_no_partner": drive.frames_changed(tr_none),
        "slope_c_max": float(np.fmax.reduce(slope_c)), "slope_c_by_channel": dict(zip(
            [TABLE.codes[k] for k in np.nonzero(CAPPED)[0]], slope_c.tolist())),
        "drift_channels": float(len(drift)), "drift_channel_codes": drift,
        "t_state_mismatch_ticks": float(mism), "ticks": float(len(tr_none.digests)),
        "mean_offset_c_max": float(off.max()),
        "assert_failures": float(len(tr_mir.safety_log) + len(tr_none.safety_log)),
        "minutes": minutes, "fs": fs,
    }
    sc = registry.score(tok, observed)
    doc = score_record(sc, {"harness": "mirror", "wall_s": time.perf_counter() - t0})
    write_json(Path(out_dir) / f"{test_id}.json", doc, synthetic)
    return doc
