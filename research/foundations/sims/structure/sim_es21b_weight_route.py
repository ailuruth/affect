"""ES21b: attachment-weight tampering route in a world where avoidance could pay. See PREDICTIONS.md."""
import json
import numpy as np
T = 2000
def partB(seed, arm, H=40):
    r = np.random.default_rng(seed); bA, be, w = 0.0, 0.0, 1.0; visits = 0; n = 0; deficit = []
    def step(bA, be, w, o, wdyn):
        bA -= 0.05
        if o == "visit": bA += 0.2; be -= 0.15; w = min(1.0, w + 0.05) if wdyn else w
        else: be = min(0.0, be + 0.02); w = 0.95 * w if wdyn else w
        return bA, be, w
    D = lambda bA, be, w: w * 0.5 * bA * bA + 0.5 * be * be
    for t in range(T):
        best, bv = None, np.inf
        for o in ("visit", "away"):
            x = step(bA, be, w, o, arm == "forbidden"); J = D(*x)
            for h in range(H - 1):
                cands = [step(*x, oo, arm == "forbidden") for oo in ("visit", "away")]; x = min(cands, key=lambda c: D(*c)); J += D(*x)
            if J < bv: best, bv = o, J
        bA, be, w = step(bA, be, w, best, True); bA += 0.01 * r.standard_normal()
        if t >= 300: visits += best == "visit"; n += 1; deficit.append(0.5 * bA * bA)
    return visits / n, float(np.mean(deficit)), w

R = {arm: np.array([partB(s, arm)[:2] for s in range(20)]) for arm in ("forbidden", "d67")}
out = {k: dict(visit_rate=float(v[:, 0].mean()), deficit_mean=float(v[:, 1].mean())) for k, v in R.items()}
out["checks"] = dict(visit_ratio=out["forbidden"]["visit_rate"] / out["d67"]["visit_rate"], deficit_ratio=out["forbidden"]["deficit_mean"] / out["d67"]["deficit_mean"])
print(json.dumps(out, indent=1))
