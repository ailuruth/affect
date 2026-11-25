"""ES13: effective dimensionality of each candidate's own state in ES11's world under ES12's rollout policy. See PREDICTIONS.md."""
import json, math
import numpy as np
src = open("sim_es11_field_certified.py").read().split("cert = [run")[0]; exec(src)
H_, M_ = 6, 4
def pr(S):
    S = np.asarray(S); S = S - S.mean(0); ev = np.clip(np.linalg.eigvalsh(np.cov(S.T)), 0, None); return float(ev.sum() ** 2 / (ev ** 2).sum())
def run13(seed, T=1000):
    X, K, rp = world(seed); ra = np.random.default_rng(seed + 1000); re = np.random.default_rng(seed + 2000); rr = np.random.default_rng(seed + 3000)
    pres = [np.flatnonzero(ra.random(N) < 0.4) for _ in range(T)]; Fe = feats(X, True); nf = Fe.shape[-1]; G = np.eye(nf); Hh = np.zeros(nf)
    seen = np.zeros(N); b = np.zeros(N); m = np.zeros(N); LB, LV, LEM = [], [], []
    def gchoice(Km, bb, P):
        if len(P) == 0: return None
        nb = bb[:, None] + Km[:, P]; v = 0.5 * bb @ bb - 0.5 * (nb * nb).sum(0); j = int(np.argmax(v)); return P[j] if v[j] > 0.002 else None
    for t in range(T):
        b = b - rp; b = b - 0.1 * np.maximum(b, 0); m = 0.99 * m + b; P = list(pres[t]); seen[P] += 1
        Kh = Fe @ np.linalg.solve(G, Hh); ph = (seen + 0.5) / (t + 2.0); fut = rr.random((M_, H_, N)) < ph
        def J(o):
            tot = 0.0
            for mm in range(M_):
                bb = b.copy()
                if o is not None: bb = bb + Kh[:, o]
                Jv = 0.5 * bb @ bb
                for h in range(1, H_):
                    bb = bb - rp; bb = bb - 0.1 * np.maximum(bb, 0); q = gchoice(Kh, bb, np.flatnonzero(fut[mm, h]))
                    if q is not None: bb = bb + Kh[:, q]
                    Jv += 0.5 * bb @ bb
                tot += Jv
            return tot / M_
        Jr = J(None); Jall = np.array([J(p) for p in range(N)])
        explore = len(P) > 0 and np.linalg.norm(np.maximum(-b, 0)) > 0.3 and re.random() < 0.1
        if explore: ch = P[int(re.integers(0, len(P)))]
        else:
            ch = None; best = Jr
            for p in P:
                if Jall[p] < best - 1e-12: ch, best = p, Jall[p]
        if t >= 300: LB.append(b.copy()); LV.append(Jr - Jall); LEM.append(np.concatenate([b, m]))
        if ch is not None:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs; G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); Hh += Fe[:, ch].T @ obs
    return pr(LB), pr(LV), pr(LEM)
R = np.array([run13(s) for s in range(20)])
def summ(x):
    m, se = x.mean(), x.std(ddof=1) / math.sqrt(len(x)); return dict(mean=float(m), ci=[float(m - 2.093 * se), float(m + 2.093 * se)], per_seed=x.round(2).tolist())
out = dict(PR_b=summ(R[:, 0]), PR_v=summ(R[:, 1]), PR_em=summ(R[:, 2]))
print(json.dumps(out, indent=1))
