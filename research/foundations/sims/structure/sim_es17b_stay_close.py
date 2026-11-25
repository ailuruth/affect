"""ES17b (stay-close option added): post-reunion engagement vs separation length under a two-scale vs one-scale innate body model. See PREDICTIONS.md."""
import json, math
import numpy as np
from scipy.stats import spearmanr
def run(seed, arm, T=6000):
    r = np.random.default_rng(seed); f = s = a = 0.0; t = 0; recs = []; cost = []
    dh = (lambda f, s, a: 0.5 * (f * f + s * s + a * a)) if arm == "two" else (lambda f, s, a: 0.5 * (f * f + a * a))
    while t < T:
        L = int(r.choice([50, 100, 200, 400]))
        for phase, n in (("absent", L), ("present", 150)):
            eng = 0
            for _ in range(n):
                if t >= T: break
                f = max(f - 0.05, -1); s = max(s - 0.003, -3); a = max(a - 0.03, -1)
                opts = {"rest": (f, s, a), "other": (f, s, a + 0.12)}
                if phase == "present": opts["engage"] = (f + 0.15, s + 0.02, a); opts["close"] = (f, s + 0.02, a)
                base = dh(f, s, a); best, bv = "rest", 0.001
                for k, v in opts.items():
                    if k != "rest" and base - dh(*v) > bv: best, bv = k, base - dh(*v)
                f, s, a = opts[best]; eng += best in ("engage", "close"); cost.append(0.5 * (f * f + s * s + a * a)); t += 1
            if phase == "present" and t <= T: recs.append((L, eng))
    Ls, Es = zip(*recs); rho = spearmanr(Ls, Es).statistic
    return (0.0 if np.isnan(rho) else float(rho)), float(np.mean(cost)), recs
out = {}
for arm in ("two", "one"):
    R = [run(sd, arm) for sd in range(20)]; rho = np.array([x[0] for x in R]); se = rho.std(ddof=1) / math.sqrt(20)
    byL = {L: float(np.mean([e for x in R for (l, e) in x[2] if l == L])) for L in (50, 100, 200, 400)}
    out[arm] = dict(rho_mean=float(rho.mean()), rho_ci=[float(rho.mean() - 2.093 * se), float(rho.mean() + 2.093 * se)], engage_by_L=byL, costs=[x[1] for x in R])
lr = np.log(np.array(out["two"]["costs"]) / np.array(out["one"]["costs"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(20)
out["ES17_3"] = dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 2.093 * se)), float(np.exp(m + 2.093 * se))], wins=int((lr < 0).sum()), n=20)
print(json.dumps(out, indent=1))
