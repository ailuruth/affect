"""ES4: topics and person x topic composition. See PREDICTIONS.md."""
import json, math
import numpy as np
NP, NT, T, K, F = 400, 30, 2000, 3, 8
W = 0.5 * np.array([[1, 0.8, 0, 0], [0, 0, 1, 0.8]])
def feats(arm, x, t):
    if arm == "bilinear": return np.einsum("...i,...j->...ij", np.concatenate([np.ones(x.shape[:-1] + (1,)), x], -1), np.concatenate([np.ones(t.shape[:-1] + (1,)), t], -1)).reshape(x.shape[:-1] + (81,))
    return np.concatenate([np.ones(x.shape[:-1] + (1,)), x, t], -1)
def run(seed, arm):
    r = np.random.default_rng(seed); Z = r.standard_normal((NP, 4)); A = r.standard_normal((F, 4)) / 2; X = Z @ A.T + 0.3 * r.standard_normal((NP, F))
    Y = r.standard_normal((NT, 4)); B = r.standard_normal((F, 4)) / 2; TT = Y @ B.T + 0.3 * r.standard_normal((NT, F))
    def true_db(p, k): return 0.5 * Z[p] @ W.T + 0.5 * Y[k] @ W.T + (Z[p] * Y[k]) @ W.T
    ra = np.random.default_rng(seed + 1000); pres = [np.where(ra.random(K) < 0.7, ra.integers(0, 20, K), ra.integers(20, NP, K)) for _ in range(T)]
    re = np.random.default_rng(seed + 2000); D = 81 if arm == "bilinear" else 17
    G = np.eye(D); H = np.zeros((D, 2)); tab = {}; allobs = []; b = np.zeros(2); cost, agree = [], []
    for t in range(T):
        drift = np.array([0.2, 0.02]) if (t // 50) % 2 == 0 else np.array([0.02, 0.2])
        b = np.minimum(b - drift, 1.0); e = np.maximum(-b, 0); P = pres[t]
        pp, kk = np.meshgrid(P, np.arange(NT), indexing="ij"); pp, kk = pp.ravel(), kk.ravel()
        TD = np.array([true_db(p, k) for p, k in zip(pp, kk)])
        if arm == "oracle": pred = TD
        elif arm == "tables":
            mu = np.mean(allobs, 0) if allobs else np.zeros(2); pred = np.array([np.mean(tab[(p, k)], 0) if (p, k) in tab else mu for p, k in zip(pp, kk)])
        else: pred = feats(arm, X[pp], TT[kk]) @ np.linalg.solve(G, H)
        val = pred @ e; ov = TD @ e; oc = int(np.argmax(ov)) if ov.max() > 0.01 else -1
        explore = np.linalg.norm(e) > 0.1 and re.random() < 0.1
        ch = int(re.integers(0, len(pp))) if explore else (int(np.argmax(val)) if val.max() > 0.01 else -1)
        if t >= 500:
            cost.append(0.5 * e @ e)
            if oc >= 0 and not explore: agree.append(ch == oc)
        if ch >= 0:
            p, k = pp[ch], kk[ch]; obs = true_db(p, k) + 0.1 * re.standard_normal(2); b = np.minimum(b + obs, 1.0)
            if arm in ("bilinear", "additive"): f = feats(arm, X[p], TT[k]); G += np.outer(f, f); H += np.outer(f, obs)
            tab.setdefault((p, k), []).append(obs); allobs.append(obs)
    return float(np.mean(cost)), float(np.mean(agree))
out = {}
for arm in ("bilinear", "additive", "tables", "oracle"):
    R = [run(s, arm) for s in range(40)]; out[arm] = dict(costs=[c for c, _ in R], agree=float(np.mean([a for _, a in R])), median_cost=float(np.median([c for c, _ in R])))
def paired(a, b):
    lr = np.log(np.array(out[a]["costs"]) / np.array(out[b]["costs"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
out["checks"] = dict(ES4_1_bilinear=out["bilinear"]["agree"], ES4_1_additive=out["additive"]["agree"], ES4_2=paired("bilinear", "additive"), ES4_3=paired("bilinear", "tables"))
print(json.dumps(out, indent=1))
