"""ES18: participation ratio of each arm's own value field in ES11's world. See PREDICTIONS.md."""
"""ES11: need field over a learned space, world certified feasible by a fixed policy. See PREDICTIONS.md."""
import json, math
import numpy as np
N, F = 12, 8
def world(seed):
    r = np.random.default_rng(seed); C = 3 * r.standard_normal((4, 4)); Z = np.repeat(C, 3, 0) + 0.5 * r.standard_normal((N, 4))
    A = r.standard_normal((F, 4)) / 2; X = Z @ A.T + 0.3 * r.standard_normal((N, F)); K = 0.5 * np.exp(-((Z[:, None] - Z[None]) ** 2).sum(-1) / 4)
    return X, K, r.uniform(0.02, 0.04, N)
def feats(X, space):
    D = np.abs(X[:, None] - X[None]); I = np.eye(N)[..., None]; one = np.ones((N, N, 1))
    return np.concatenate([one, I, D], -1) if space else np.concatenate([one, I], -1)
d = lambda b: 0.5 * b @ b
def run(seed, arm, T=1000):
    X, K, rp = world(seed); ra = np.random.default_rng(seed + 1000); re = np.random.default_rng(seed + 2000)
    pres = [np.flatnonzero(ra.random(N) < 0.4) for _ in range(T)]
    Fe = feats(X, arm != "identity"); nf = Fe.shape[-1]; G = np.eye(nf); H = np.zeros(nf); ts = np.zeros(N); tn = np.zeros(N)
    b = np.zeros(N); cost, agree = [], []; VL = []
    def greedy(Km, P):
        best, bv = None, 0.002
        for q in P:
            v = d(b) - d(b + Km[:, q])
            if v > bv: best, bv = q, v
        return best
    for t in range(T):
        b = b - rp; b = b - 0.1 * np.maximum(b, 0); P = list(pres[t])
        Kh = K if arm == "oracle" else (Fe @ np.linalg.solve(G, H) if arm in ("learned", "identity", "wta") else None)
        explore = len(P) > 0 and np.linalg.norm(np.maximum(-b, 0)) > 0.3 and re.random() < 0.1 and arm != "certificate"
        if explore: ch = P[int(re.integers(0, len(P)))]
        elif arm == "certificate": ch = min(P, key=lambda q: b[q]) if P and min(b[q] for q in P) < -0.1 else None
        elif arm in ("learned", "identity", "oracle"): ch = greedy(Kh, P)
        elif arm == "wta":
            ps = int(np.argmin(b)); vals = [Kh[ps, q] for q in P]
            ch = P[int(np.argmax(vals))] if P and b[ps] < -0.05 and max(vals) > 0.01 else None
        else:
            B = b.mean(); ch, bv = None, 0.0
            for q in P:
                dB = ts[q] / tn[q] if tn[q] else (ts.sum() / tn.sum() if tn.sum() else 0.0); v = 0.5 * N * (B * B - (B + dB) ** 2)
                if v > bv: ch, bv = q, v
        if t >= 300:
            if arm in ("learned",): VL.append(np.array([d(b) - d(b + Kh[:, i]) for i in range(N)]))
            elif arm == "wta": VL.append(Kh[int(np.argmin(b))].copy())
            elif arm == "global":
                B = b.mean(); dB = np.array([ts[i] / tn[i] if tn[i] else (ts.sum() / tn.sum() if tn.sum() else 0.0) for i in range(N)]); VL.append(0.5 * N * (B * B - (B + dB) ** 2))
            cost.append(d(b)); oc = greedy(K, P)
            if oc is not None and not explore: agree.append(ch == oc)
        if ch is not None:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs
            G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); H += Fe[:, ch].T @ obs; ts[ch] += obs.mean(); tn[ch] += 1
    V = np.array(VL); V = V - V.mean(0); ev = np.clip(np.linalg.eigvalsh(np.cov(V.T)), 0, None); pr = float(ev.sum() ** 2 / (ev ** 2).sum()) if ev.sum() > 0 else 1.0
    return float(np.mean(cost)), pr
def paired(a, b):
    lr = np.log(np.array(a) / np.array(b)); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))

import math
PR = {arm: np.array([run(sd, arm)[1] for sd in range(20)]) for arm in ("learned", "wta", "global")}
def ratio(a, b):
    lr = np.log(PR[a] / PR[b]); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo=float(np.exp(m)), ci=[float(np.exp(m - 2.093 * se)), float(np.exp(m + 2.093 * se))])
out = dict(PR_mean={k: float(v.mean()) for k, v in PR.items()}, ES18_1=ratio("learned", "wta"), ES18_2=ratio("learned", "global"), per_seed={k: v.round(2).tolist() for k, v in PR.items()})
print(json.dumps(out, indent=1))
