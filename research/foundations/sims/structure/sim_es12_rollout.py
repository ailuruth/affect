"""ES12: rollout costate vs myopic in ES11's certified world. See PREDICTIONS.md."""
import json, math, sys
import numpy as np
src = open("sim_es11_field_certified.py").read().split("cert = [run")[0]; exec(src)
H_, M_ = 6, 4
def run12(seed, arm, T=1000):
    X, K, rp = world(seed); ra = np.random.default_rng(seed + 1000); re = np.random.default_rng(seed + 2000); rr = np.random.default_rng(seed + 3000)
    pres = [np.flatnonzero(ra.random(N) < 0.4) for _ in range(T)]
    space = arm in ("roll_learned", "myopic_learned"); Fe = feats(X, space); nf = Fe.shape[-1]; G = np.eye(nf); Hh = np.zeros(nf)
    seen = np.zeros(N); b = np.zeros(N); cost = []
    def gchoice(Km, bb, P):
        if len(P) == 0: return None
        nb = bb[:, None] + Km[:, P]; v = 0.5 * bb @ bb - 0.5 * (nb * nb).sum(0); j = int(np.argmax(v)); return P[j] if v[j] > 0.002 else None
    for t in range(T):
        b = b - rp; b = b - 0.1 * np.maximum(b, 0); P = list(pres[t]); seen[P] += 1
        if arm == "certificate": Kh = None
        elif arm == "roll_true": Kh = K
        else: Kh = Fe @ np.linalg.solve(G, Hh)
        explore = len(P) > 0 and np.linalg.norm(np.maximum(-b, 0)) > 0.3 and re.random() < 0.1 and arm != "certificate"
        if explore: ch = P[int(re.integers(0, len(P)))]
        elif arm == "certificate": ch = min(P, key=lambda q: b[q]) if P and min(b[q] for q in P) < -0.1 else None
        elif arm == "myopic_learned": ch = gchoice(Kh, b, np.array(P, int))
        else:
            ph = (seen + 0.5) / (t + 1 + 1.0); fut = rr.random((M_, H_, N)) < ph
            best, bestv = None, np.inf
            for o in [None] + P:
                tot = 0.0
                for m in range(M_):
                    bb = b.copy()
                    if o is not None: bb = bb + Kh[:, o]
                    J = 0.5 * bb @ bb
                    for h in range(1, H_):
                        bb = bb - rp; bb = bb - 0.1 * np.maximum(bb, 0); q = gchoice(Kh, bb, np.flatnonzero(fut[m, h]))
                        if q is not None: bb = bb + Kh[:, q]
                        J += 0.5 * bb @ bb
                    tot += J
                if tot < bestv - 1e-12: best, bestv = o, tot
            ch = best
        if t >= 300: cost.append(0.5 * b @ b)
        if ch is not None:
            obs = K[:, ch] + 0.03 * re.standard_normal(N); b = b + obs; G += np.einsum("pf,pg->fg", Fe[:, ch], Fe[:, ch]); Hh += Fe[:, ch].T @ obs
    return float(np.mean(cost))
arm = sys.argv[1]; c = [run12(s, arm) for s in range(120)]
json.dump(dict(arm=arm, costs=c, median=float(np.median(c)), runaway=int(sum(x > 5 for x in c))), open(f"out/es12_{arm}.json", "w")); print(arm, np.median(c))
