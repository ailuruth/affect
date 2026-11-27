"""E2: the steering harness on the engine's own state (spec §5.3), and the input clamps (F5, F18, F19, F23).

Steering. A controlled perturbation of one named latent component is injected at time t_s, at five strengths of
each sign along the component's direction, with a random direction of equal norm in the same state block as the
control. The step is applied to the factual and the shadow run alike (both compute the same T state; a T field
changed in one run only would be an F -> T leak and fire A5). The step is an exogenous intervention outside the
drives' declared terms, so the harness opens a new A14 accounting epoch at the step (DriveAccount restarted from the
stepped state): A14 then checks the engine's own dynamics after it. Values are clipped to each field's range.

Targets (directions from the equations, not from labels; spec §5.3):
  K        a step in K_id             (block: the body loads E, A_L, h_word, K, P_play, I_lp)
  h_word   a step in h_word           (same block)
  N_L.V    the partner-load estimate N-hat along its V coordinate (block: N-hat's (V, A, T), the same step added to
           every topic slot of N_L), so D_p moves along N-hat's V coordinate
  omega.<group>  omega_g of one group (block: omega), latched at session start (omega is a session latch)
Readouts after t_s minus the unsteered run's (eval/drive.summary). Observed: the dose-response list (ordered by
signed dose), |effect| at the largest dose along the named and along the random direction, the largest |effect|
on the unrelated readouts the prediction names, and assertion failures.

Input clamps. One of his input streams is transformed (scaled, swapped) while everything else is replayed; the
predicted invariance is exact: the T-state digest (A5's) at every tick equals the unclamped run's.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from engine.config.channels import TABLE
from engine.invariants.asserts import DriveAccount
from engine.state.body import Session
from eval import config as C
from eval import drive, planner
from eval.registry import Registry
from eval.results import score_record, write_json

LOADS = ("E", "A_L", "h_word", "K", "P_play", "I_lp")


def _block(target: str) -> str:
    if target in LOADS:
        return "loads"
    if target == "N_L.V":
        return "N_L"
    if target.startswith("omega."):
        return "omega"
    raise KeyError(f"unknown steering target {target!r}")


def named_direction(target: str, body_like=None) -> np.ndarray:
    blk = _block(target)
    if blk == "loads":
        v = np.zeros(len(LOADS))
        v[LOADS.index(target)] = 1.0
        return v
    if blk == "N_L":
        return np.array([1.0, 0.0, 0.0])
    groups = _groups()
    v = np.zeros(len(groups))
    v[groups.index(target.split(".", 1)[1])] = 1.0
    return v


def _groups():
    from engine.routes.cone import GROUPS
    return GROUPS


def random_direction(target: str, rng) -> np.ndarray:
    v = rng.standard_normal(named_direction(target).shape)
    return v / np.linalg.norm(v)


@dataclass
class Step:
    """Add `delta` (shaped like the target's block) to the block at the first tick at or after t."""
    target: str
    delta: np.ndarray
    t: float

    def apply(self, pair) -> None:
        blk = _block(self.target)
        for body in (pair.factual.body, pair.shadow.body):
            if blk == "loads":
                for name, d in zip(LOADS, np.reshape(self.delta, -1)):
                    object.__setattr__(body, name, np.float64(np.clip(float(getattr(body, name)) + d, 0.0, 1.0)))
            elif blk == "N_L":
                body.N_L = np.clip(body.N_L + np.reshape(self.delta, (1, 3)), 0.0, 1.0)
            else:
                raise ValueError("omega is a session latch: steer it through the session (run_steering does)")
            body.account = DriveAccount(body.b(), body.f_id)


def _run_dose(ps, learned, target, delta, t_s, seed):
    if _block(target) == "omega":
        om = np.clip(np.asarray(Session().omega, float) + np.reshape(delta, -1), -1.0, 1.0)
        tr = drive.run(ps, learned, seed=seed, session=Session(K=0.6, omega=tuple(om)))
        return drive.summary(tr)
    tr = drive.run(ps, learned, steer=Step(target, delta, t_s), seed=seed)
    return drive.summary(tr, after=tr.steer_t)


def run_steering(registry: Registry, test_id: str, target: str, readout: str, ps, learned, out_dir, synthetic: bool,
                 step: float, t_s: float, unrelated=(), seed: int = 0, doses=C.STEER_DOSES, split: bool = False,
                 approved: str | None = None) -> dict:
    tok = registry.start_run(test_id)
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed + 7919)
    u_named = named_direction(target)
    u_rand = random_direction(target, rng)
    base = _run_dose(ps, learned, target, 0.0 * u_named, t_s, seed)
    planner.guard((time.perf_counter() - t0) * (len(doses) + 3) / 3600.0, split=split, approved=approved)
    eff, unrel, fails = [], [], base["assert_failures"]
    for d in sorted(doses):
        s = _run_dose(ps, learned, target, d * step * u_named, t_s, seed)
        eff.append(s[readout] - base[readout])
        unrel += [abs(s[k] - base[k]) for k in unrelated]
        fails += s["assert_failures"]
    dmax = max(abs(d) for d in doses)
    named_abs = 0.5 * (abs(eff[0]) + abs(eff[-1]))
    rand = [_run_dose(ps, learned, target, sg * dmax * step * u_rand, t_s, seed) for sg in (-1, 1)]
    rand_abs = float(np.mean([abs(s[readout] - base[readout]) for s in rand]))
    fails += sum(s["assert_failures"] for s in rand)
    observed = {"doses": [float(d * step) for d in sorted(doses)], "dose_response": eff, "named_abs": named_abs,
                "random_abs": rand_abs, "unrelated_max_abs": float(max(unrel) if unrel else 0.0),
                "assert_failures": float(fails), "baseline": base[readout]}
    sc = registry.score(tok, observed)
    doc = score_record(sc, {"harness": "steering", "target": target, "readout": readout, "block": _block(target),
                            "unrelated": list(unrelated), "wall_s": time.perf_counter() - t0})
    write_json(Path(out_dir) / f"{test_id}.json", doc, synthetic)
    return doc


# ==================================================================================================== input clamps
def scale_channels(codes, factor):
    idx = [TABLE.index(c) for c in codes]

    def f(U):
        U[:, idx] = U[:, idx] * factor
        return U
    return f


def replace_channels(codes, U_other):
    idx = [TABLE.index(c) for c in codes]

    def f(U):
        m = min(U.shape[0], U_other.shape[0])
        U[:m, idx] = U_other[:m, idx]
        return U
    return f


def run_clamp(registry: Registry, test_id: str, ps, learned, transforms: dict, out_dir, synthetic: bool,
              seed: int = 0) -> dict:
    """transforms: name -> face_fn. Observed: ticks whose T-state digest differs from the unclamped run (summed over
    transforms), and the fraction of frames whose factual output y changed (the clamp did reach the F side)."""
    tok = registry.start_run(test_id)
    ref = drive.run(ps, learned, seed=seed)
    mism, changed, per = 0, [], {}
    for name, fn in transforms.items():
        tr = drive.run(ps, learned, seed=seed, face_fn=fn)
        m = sum(a != b for a, b in zip(ref.digests, tr.digests)) + abs(len(ref.digests) - len(tr.digests))
        c = float(np.mean(np.any(np.abs(tr.y - ref.y) > 1e-12, axis=1)))
        mism += m
        changed.append(c)
        per[name] = {"t_state_mismatch_ticks": m, "output_changed_frames": c}
    observed = {"t_state_mismatch_ticks": float(mism), "output_changed_frames_min": float(min(changed)),
                "ticks": float(len(ref.digests)), "per_transform": per}
    sc = registry.score(tok, observed)
    doc = score_record(sc, {"harness": "steering.clamp", "transforms": list(transforms)})
    write_json(Path(out_dir) / f"{test_id}.json", doc, synthetic)
    return doc
