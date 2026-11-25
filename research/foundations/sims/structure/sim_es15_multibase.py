"""ES15: K5 rollout over a library of base policies, ES11 world, ES12 seeds. See PREDICTIONS.md."""
import json, math, sys
import numpy as np
src = open("sim_es11_field_certified.py").read().split("cert = [run")[0]; exec(src)
H_, M_ = 6, 4
def run15(seed, arm, T=1000):
    X, K, rp = world(seed); ra = np.random.default_rng(seed + 1000); re = np.random.default_rng(seed + 2000); rr = np.random.default_rng(seed + 3000)
    pres = [np.flatnonzero(ra.random(N) < 0.4) for _ in range(T)]; Fe = feats(X, True); nf = Fe.shape[-1]; G = np.eye(nf); Hh = np.zeros(nf)
    seen = np.zeros(N); b = np.zeros(N); cost = []
    def greedy(Km, bb, P):
        if len(P) == 0: return None
        nb = bb[:, None] + Km[:, P]; v = 0.5 * bb @ bb - 0.5 * (nb * nb).sum(0); j = int(np.argmax(v)); return P[j] if v[j] > 0.002 else None
    def thresh(Km, bb, P):
        if len(P) == 0: return None
        q = P[int(np.argmin(bb[P]))]; return q if bb[q] < -0.1 else None
    bases = [greedy, thresh] if arm == "multi" else [thresh]
    for t in range(T):
        b = b - rp; b = b - 0.1 * np.maximum(b, 0); P = list(pres[t]); seen[P] += 1
        Kh = Fe @ np.linalg.solve(G, Hh); explore = len(P) > 0 and np.linalg.norm(np.maximum(-b, 0)) > 0.3 and re.random() < 0.1
        if explore: ch = P[int(re.integers(0, len(P)))]
        else:
            ph = (seen + 0.5) / (t + 1 + 1.0); fut = rr.random((M_, H_, N)) < ph; best, bestv = None, np.inf
            for o in [None] + P:
                vals = []
                for base in bases:
                    tot = 0.0
                    for m in range(M_):
                        bb = b.copy()
                        if o is not None: bb = bb + Kh[:, o]
                        J = 0.5 * bb @ bb
                        for h in range(1, H_):
                            bb = bb - rp; bb = bb - 0.1 * np.maximum(bb, 0); q = base(Kh, bb, np.flatnonzero(fut[m, h]))
                            if q is not None: bb = bb + Kh[:, q]
                            J += 0.5 * bb @ bb
                        tot += J
                    vals.append(tot)
                v = min(vals)
                if v < bestv - 1e-12: best, bestv = o, v
            ch = best
        if t >= 300: cost.append(0.5 * b @ b)
        if ch is not None:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs; G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); Hh += Fe[:, ch].T @ obs
    return float(np.mean(cost))
arm = sys.argv[1]; c = [run15(s, arm) for s in range(120)]
json.dump(dict(arm=arm, costs=c, median=float(np.median(c)), runaway=int(sum(x > 5 for x in c))), open(f"out/es15_{arm}.json", "w")); print(arm, np.median(c))
