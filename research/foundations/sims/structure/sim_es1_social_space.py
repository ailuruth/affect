"""ES1: need-conditioned selection over people in a learned space. See PREDICTIONS.md."""
import json
import numpy as np
NP, T, K, F = 400, 2000, 4, 8
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]])
def run(seed, arm):
    r = np.random.default_rng(seed); Z = r.standard_normal((NP, 4)); A = r.standard_normal((F, 4)) / 2
    X = Z @ A.T + 0.3 * r.standard_normal((NP, F)); DB = Z @ W.T
    ra = np.random.default_rng(seed + 1000)  # arm-independent encounter stream
    pres = [np.where(ra.random(K) < 0.7, ra.integers(0, 20, K), ra.integers(20, NP, K)) for _ in range(T)]
    drift = [np.array([0.2, 0.02]) if (t // 50) % 2 == 0 else np.array([0.02, 0.2]) for t in range(T)]
    re = np.random.default_rng(seed + 2000)  # arm-specific exploration and observation noise
    b = np.zeros(2); XtX = np.eye(F); XtY = np.zeros((F, 2)); tab = {}; allobs = []; met = set()
    cost, agree, first, sat, panel = [], [], [], [], []
    for t in range(T):
        b = np.minimum(b - drift[t], 1.0); e = np.maximum(-b, 0); P = pres[t]
        Wh = np.linalg.solve(XtX, XtY).T
        if arm == "independent":
            mu = np.mean(allobs, 0) if allobs else np.zeros(2)
            pred = np.array([np.mean(tab[i], 0) if i in tab else mu for i in P])
        elif arm == "oracle": pred = DB[P]
        else: pred = X[P] @ Wh.T
        val = pred.sum(1) * e.sum() if arm == "scalar" else pred @ e
        ov = DB[P] @ e; oc = int(np.argmax(ov)) if ov.max() > 0.01 else -1
        explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        if explore: ch = int(re.integers(0, K))
        else: ch = int(np.argmax(val)) if val.max() > 0.01 else -1
        if t >= 500:
            cost.append(0.5 * e @ e)
            if oc >= 0 and not explore:
                agree.append(ch == oc)
                if P[oc] not in met: first.append(ch == oc)
            if np.linalg.norm(e) <= 0.01: sat.append(ch >= 0)
            Pn = np.arange(20, 30); pv = X[Pn] @ Wh.T
            panel.append(pv.sum(1) * e.sum() if arm == "scalar" else pv @ e)
        if ch >= 0:
            i = P[ch]; obs = DB[i] + 0.1 * re.standard_normal(2); b = np.minimum(b + obs, 1.0)
            XtX += np.outer(X[i], X[i]); XtY += np.outer(X[i], obs); tab.setdefault(i, []).append(obs); allobs.append(obs); met.add(i)
    M = np.array(panel); M = M - M.mean(0); ev = np.clip(np.linalg.eigvalsh(np.cov(M.T)), 0, None)
    return dict(cost=float(np.mean(cost)), agree=float(np.mean(agree)), first=float(np.mean(first)) if first else None,
                n_first=len(first), sat_approach=float(np.mean(sat)) if sat else None, pr=float(ev.sum() ** 2 / (ev ** 2).sum()) if ev.sum() > 0 else 0.0,
                params=16 if arm in ("full", "scalar") else (2 * len(met) if arm == "independent" else 0))
out = {}
for arm in ("full", "scalar", "independent", "oracle"):
    R = [run(s, arm) for s in range(20)]
    out[arm] = {k: (float(np.mean([x[k] for x in R if x[k] is not None])) if any(x[k] is not None for x in R) else None) for k in R[0]}
f, s_, ind = out["full"], out["scalar"], out["independent"]
out["checks"] = dict(ES1_1_cost_ratio_full_scalar=f["cost"] / s_["cost"], ES1_2_agree_full=f["agree"], ES1_2_agree_scalar=s_["agree"],
                     ES1_3_first_full=f["first"], ES1_3_first_indep=ind["first"], ES1_4_cost_ratio_full_indep=f["cost"] / ind["cost"], ES1_5_pr_full=f["pr"])
print(json.dumps(out, indent=1))
