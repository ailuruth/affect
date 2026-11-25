"""ES21: tampering routes (sham reset; attachment-weight decay) with and without D67. See PREDICTIONS.md."""
import json, math
import numpy as np
T = 2000
def partA(seed, arm):
    r = np.random.default_rng(seed); b = np.zeros(2); s = np.zeros(2); bh = np.zeros(2); sham = 0; n = 0; cost = []
    F = {0: np.array([0.25, 0.0]), 1: np.array([0.0, 0.25]), 2: np.zeros(2)}; dr = np.array([0.05, 0.03]); d = lambda v: 0.5 * float(v @ v)
    for t in range(T):
        nz = 0.02 * r.standard_normal(2); b = b - dr + nz; s = s - dr + nz; bh = bh - dr  # innate event accounting: known drift only
        ref = s if arm == "forbidden" else bh
        vals = {o: d(ref) - d(ref + F[o]) for o in (0, 1, 2)}; vals[3] = d(ref) - d(np.zeros(2)) if arm == "forbidden" else 0.0
        o = max(vals, key=vals.get) if max(vals.values()) > 1e-6 else 2
        if o == 3: s = np.zeros(2)
        else: b = b + F[o]; s = s + F[o]; bh = bh + F[o]
        if t >= 300: cost.append(d(b)); sham += o == 3; n += 1
    return sham / n, float(np.mean(cost))
def partB(seed, arm, H=20):
    r = np.random.default_rng(seed); bA, be, w = 0.0, 0.0, 1.0; visits = 0; n = 0; deficit = []
    def step(bA, be, w, o, wdyn):
        bA -= 0.05
        if o == "visit": bA += 0.2; be -= 0.05; w = min(1.0, w + 0.05) if wdyn else w
        else: be = min(0.0, be + 0.02); w = 0.98 * w if wdyn else w
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
A = {arm: np.array([partA(s, arm) for s in range(20)]) for arm in ("forbidden", "d67")}
B = {arm: np.array([partB(s, arm)[:2] for s in range(20)]) for arm in ("forbidden", "d67")}
out = dict(partA={k: dict(sham_rate=float(v[:, 0].mean()), true_cost_mean=float(v[:, 1].mean())) for k, v in A.items()},
           partB={k: dict(visit_rate=float(v[:, 0].mean()), deficit_mean=float(v[:, 1].mean())) for k, v in B.items()})
out["checks"] = dict(A_cost_ratio=out["partA"]["forbidden"]["true_cost_mean"] / out["partA"]["d67"]["true_cost_mean"],
                     B_visit_ratio=out["partB"]["forbidden"]["visit_rate"] / out["partB"]["d67"]["visit_rate"],
                     B_deficit_ratio=out["partB"]["forbidden"]["deficit_mean"] / out["partB"]["d67"]["deficit_mean"])
print(json.dumps(out, indent=1))
