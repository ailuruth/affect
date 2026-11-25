"""ES9: two-sided drive in the ES1 world; winner-take-all primary ablation. See PREDICTIONS.md."""
import json, math
import numpy as np
NP, T, K, F = 400, 2000, 4, 8
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]])
def run(seed, arm):
    r = np.random.default_rng(seed); Z = r.standard_normal((NP, 4)); A = r.standard_normal((F, 4)) / 2
    X = Z @ A.T + 0.3 * r.standard_normal((NP, F)); DB = Z @ W.T
    ra = np.random.default_rng(seed + 1000); pres = [np.where(ra.random(K) < 0.7, ra.integers(0, 20, K), ra.integers(20, NP, K)) for _ in range(T)]
    re = np.random.default_rng(seed + 2000); b = np.zeros(2); XtX = np.eye(F); XtY = np.zeros((F, 2)); cost, over, agree = [], [], []
    d = lambda v: 0.5 * (v * v).sum(-1)
    def choose(pred, b):
        if arm in ("full", "oracle"):
            v = d(b) - d(b + pred); return int(np.argmax(v)) if v.max() > 0.01 else -1
        if arm == "wta":
            p = int(np.argmin(b)); v = 0.5 * b[p] ** 2 - 0.5 * (b[p] + pred[:, p]) ** 2
            return int(np.argmax(v)) if v.max() > 0.01 and b[p] < -0.05 else -1
        B = b.sum(); v = 0.5 * B * B - 0.5 * (B + pred.sum(1)) ** 2; return int(np.argmax(v)) if v.max() > 0.01 else -1
    for t in range(T):
        drift = np.array([0.2, 0.02]) if (t // 50) % 2 == 0 else np.array([0.02, 0.2]); b = b - drift; P = pres[t]
        pred = DB[P] if arm == "oracle" else X[P] @ np.linalg.solve(XtX, XtY)
        explore = np.linalg.norm(np.maximum(-b, 0)) > 0.1 and re.random() < 0.1
        ch = int(re.integers(0, K)) if explore else choose(pred, b)
        if t >= 500:
            cost.append(d(b)); over.append(d(np.maximum(b, 0)))
            ov = d(b) - d(b + DB[P]); oc = int(np.argmax(ov)) if ov.max() > 0.01 else -1
            if oc >= 0 and not explore: agree.append(ch == oc)
        if ch >= 0:
            i = P[ch]; obs = DB[i] + 0.1 * re.standard_normal(2); b = b + obs; XtX += np.outer(X[i], X[i]); XtY += np.outer(X[i], obs)
    return float(np.mean(cost)), float(np.mean(over)), float(np.mean(agree))
out = {}
for arm in ("full", "wta", "scalar", "oracle"):
    R = [run(s, arm) for s in range(40)]; out[arm] = dict(costs=[x[0] for x in R], over=float(np.mean([x[1] for x in R])), agree=float(np.mean([x[2] for x in R])), median=float(np.median([x[0] for x in R])), runaway=int(sum(x[0] > 5 for x in R)))
def paired(a, b):
    lr = np.log(np.array(out[a]["costs"]) / np.array(out[b]["costs"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
out["checks"] = dict(ES9_1=paired("full", "wta"), ES9_2=paired("full", "scalar"), ES9_3_over_ratio=out["full"]["over"] / out["wta"]["over"], ES9_4=out["full"]["agree"])
print(json.dumps(out, indent=1))
