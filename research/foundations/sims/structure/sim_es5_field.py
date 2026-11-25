"""ES5: need field over a learned space (ES5a) and rollout costate vs myopic (ES5b). See PREDICTIONS.md."""
import json, math, sys
import numpy as np
N, F = 12, 8
def world(seed):
    r = np.random.default_rng(seed); Z = r.standard_normal((N, 4)); A = r.standard_normal((F, 4)) / 2; X = Z @ A.T + 0.3 * r.standard_normal((N, F))
    K = 0.5 * np.exp(-((Z[:, None] - Z[None]) ** 2).sum(-1) / 4)  # K[p, q]: fill of p from approaching q
    Tp = r.integers(8, 25, N); ph = np.array([r.integers(0, t) for t in Tp]); rp = r.uniform(0.02, 0.05, N)
    return X, K, Tp, ph, rp
def sched(t, Tp, ph): return [p for p in range(N) if (t + ph[p]) % Tp[p] < 2]
def feats(X, space):
    D = np.abs(X[:, None] - X[None]); I = np.eye(N)[..., None]; one = np.ones((N, N, 1))
    return np.concatenate([one, I, D], -1) if space else np.concatenate([one, I], -1)  # [p, q, f]
def dcost(b, be, budget): return 0.5 * b @ b + (2 * be * be if budget else 0.0)
def run(seed, arm, budget, T=1000):
    X, K, Tp, ph, rp = world(seed); ra = np.random.default_rng(seed + 1000); re = np.random.default_rng(seed + 2000)
    extra = [(ra.integers(0, N) if ra.random() < 0.5 else None) for _ in range(T)]
    space = arm not in ("identity",); Fe = feats(X, space); nf = Fe.shape[-1]; G = np.eye(nf); H = np.zeros(nf)
    tabsum = np.zeros(N); tabn = np.zeros(N); b = np.zeros(N); be = 0.0; cost, agree, napp = [], [], 0
    for t in range(T):
        b = b - rp; P = sorted(set(sched(t, Tp, ph) + ([extra[t]] if extra[t] is not None else [])))
        Kh = K if arm == "oracle" else Fe @ np.linalg.solve(G, H)  # predicted fill matrix [p, q]
        def opt_val(Km, bb, bbe, q):  # decrease of d from approaching q (q=None: rest)
            if q is None: return dcost(bb, bbe, budget) - dcost(bb, min(0.0, bbe + 0.03) if budget else bbe, budget)
            return dcost(bb, bbe, budget) - dcost(bb + Km[:, q], bbe - 0.08 if budget else bbe, budget)
        def greedy(Km, bb, bbe, Pc):
            best, bv = None, (opt_val(Km, bb, bbe, None) if budget else 0.0) + 0.002
            for q in Pc:
                v = opt_val(Km, bb, bbe, q)
                if v > bv: best, bv = q, v
            return best
        explore = len(P) > 0 and np.linalg.norm(b) > 0.3 and re.random() < 0.1
        if explore: ch = P[int(re.integers(0, len(P)))]
        elif arm in ("learned", "identity", "oracle", "myopic"): ch = greedy(Kh, b, be, P)
        elif arm == "wta":
            ps = int(np.argmin(b)); vals = [Kh[ps, q] for q in P]
            ch = P[int(np.argmax(vals))] if P and b[ps] < -0.05 and max(vals) > 0.01 else None
        elif arm == "global":
            B = b.mean(); best, bv = None, 0.0
            for q in P:
                dB = tabsum[q] / tabn[q] if tabn[q] else (tabsum.sum() / tabn.sum() if tabn.sum() else 0.0)
                v = 0.5 * N * (B * B - (B + dB) ** 2)
                if v > bv: best, bv = q, v
            ch = best
        elif arm == "rollout":
            bestv, ch = np.inf, None
            for o in [None] + P:
                bb = b.copy(); bbe = be
                if o is None: bbe = min(0.0, bbe + 0.03) if budget else bbe
                else: bb = bb + Kh[:, o]; bbe = bbe - 0.08 if budget else bbe
                J = dcost(bb, bbe, budget)
                for h in range(1, 10):
                    bb = bb - rp; q = greedy(Kh, bb, bbe, sched(t + h, Tp, ph))
                    if q is None: bbe = min(0.0, bbe + 0.03) if budget else bbe
                    else: bb = bb + Kh[:, q]; bbe = bbe - 0.08 if budget else bbe
                    J += dcost(bb, bbe, budget)
                if J < bestv - 1e-12: bestv, ch = J, o
        if t >= 300:
            cost.append(dcost(b, be, budget)); oc = greedy(K, b, be, P)
            if oc is not None and not explore: agree.append(ch == oc)
            napp += ch is not None
        if ch is None: be = min(0.0, be + 0.03) if budget else be
        else:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs; be = be - 0.08 if budget else be
            G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); H += Fe[:, ch].T @ obs; tabsum[ch] += obs.mean(); tabn[ch] += 1
    return float(np.mean(cost)), float(np.mean(agree)) if agree else None, napp / (T - 300)
def paired(a, b):
    lr = np.log(np.array(a) / np.array(b)); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
part = sys.argv[1]; out = {}
if part == "a":
    for arm in ("learned", "identity", "wta", "global", "oracle"):
        R = [run(s, arm, False) for s in range(40)]; out[arm] = dict(costs=[c for c, _, _ in R], agree=float(np.mean([a for _, a, _ in R if a is not None])), app_rate=float(np.mean([n for _, _, n in R])))
    out["checks"] = dict(ES5a_1=paired(out["learned"]["costs"], out["global"]["costs"]), ES5a_2=paired(out["learned"]["costs"], out["wta"]["costs"]),
                         ES5a_3=paired(out["learned"]["costs"], out["identity"]["costs"]), ES5a_4=out["learned"]["agree"])
else:
    for arm in ("myopic", "rollout"):
        R = [run(s, arm, True) for s in range(120)]; out[arm] = dict(costs=[c for c, _, _ in R], app_rate=float(np.mean([n for _, _, n in R])))
    out["checks"] = dict(ES5b_1=paired(out["rollout"]["costs"], out["myopic"]["costs"]), ES5b_2_app_ratio=out["rollout"]["app_rate"] / out["myopic"]["app_rate"])
print(json.dumps(out, indent=1))
