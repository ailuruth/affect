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
    b = np.zeros(N); cost, agree = [], []
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
            cost.append(d(b)); oc = greedy(K, P)
            if oc is not None and not explore: agree.append(ch == oc)
        if ch is not None:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs
            G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); H += Fe[:, ch].T @ obs; ts[ch] += obs.mean(); tn[ch] += 1
    return float(np.mean(cost)), (float(np.mean(agree)) if agree else None)
def paired(a, b):
    lr = np.log(np.array(a) / np.array(b)); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
cert = [run(s, "certificate")[0] for s in range(1000, 1020)]
out = dict(certificate=dict(median=float(np.median(cert)), max=float(max(cert)), ok=bool(np.median(cert) <= 0.5 and max(cert) <= 5)))
if out["certificate"]["ok"]:
    for arm in ("learned", "identity", "wta", "global", "oracle"):
        R = [run(s, arm) for s in range(40)]; out[arm] = dict(costs=[c for c, _ in R], median=float(np.median([c for c, _ in R])), runaway=int(sum(c > 5 for c, _ in R)),
                                                             agree=float(np.mean([a for _, a in R if a is not None])))
    c = lambda k: out[k]["costs"]
    out["checks"] = dict(ES11_1=paired(c("learned"), c("wta")), ES11_2=paired(c("learned"), c("identity")), ES11_3=paired(c("learned"), c("global")), ES11_4=out["learned"]["agree"])
print(json.dumps(out, indent=1))
