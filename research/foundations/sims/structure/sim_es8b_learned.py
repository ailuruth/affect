"""ES8b: ES8 with learned per-type statistics. See PREDICTIONS.md."""
import json, math
import numpy as np
SIG = np.array([0.35, 0.30, 0.25]); T, M, KOBS = 2000, 6, 2
MU = 0.1 * np.eye(3); SD = np.full((3, 3), 0.05); np.fill_diagonal(SD, SIG)  # SD[type, need]
def run(seed, arm):
    rw = np.random.default_rng(seed); ra = np.random.default_rng(seed + 3000)
    types = rw.integers(0, 3, (T, M)); DB = MU[types] + SD[types] * rw.standard_normal((T, M, 3)); obsn = 0.05 * rw.standard_normal((T, M, 3))
    b = np.zeros(3); cost = []; match = []; learned = arm.endswith("_l")
    n0 = 2.0; cnt = np.full((3, 1), n0); s1 = np.zeros((3, 3)); s2 = np.full((3, 3), n0 * 0.1 ** 2)
    for t in range(T):
        MUh = s1 / cnt if learned else MU; SDh = np.sqrt(np.maximum(s2 / cnt - (s1 / cnt) ** 2, 1e-6)) if learned else SD
        dr = np.full(3, 0.02); dr[(t // 50) % 3] = 0.15; b = np.minimum(b - dr, 1.0); e = np.maximum(-b, 0); ty = types[t]
        if arm == "full": obs = np.arange(M)
        elif arm == "none": obs = np.array([], int)
        else:
            if arm in ("need", "need_l"): sc = np.sqrt(((SDh[ty] ** 2) * e ** 2).sum(1))
            elif arm == "magnitude_l": sc = np.sqrt((SDh[ty] ** 2).sum(1))
            else: sc = np.zeros(M)
            sc = sc + 1e-9 * ra.random(M); obs = np.argsort(-sc)[:KOBS]
        est = MUh[ty].copy(); est[obs] = DB[t, obs] + obsn[t, obs]; val = est @ e
        for j in obs: o_ = DB[t, j] + obsn[t, j]; cnt[ty[j]] += 1; s1[ty[j]] += o_; s2[ty[j]] += o_ ** 2
        ch = int(np.argmax(val)) if val.max() > 0.01 else -1
        if t >= 200:
            cost.append(0.5 * e @ e)
            if arm in ("need", "need_l", "magnitude_l", "random") and e.max() > 0: match.append(float(np.mean(ty[obs] == int(np.argmax(e)))))
        if ch >= 0: b = np.minimum(b + DB[t, ch], 1.0)
    return float(np.mean(cost)), (float(np.mean(match)) if match else None)
out = {}
for arm in ("need_l", "magnitude_l", "random", "need"):
    R = [run(s, arm) for s in range(40)]; out[arm] = dict(costs=[c for c, _ in R], match=(float(np.mean([m for _, m in R])) if R[0][1] is not None else None), median=float(np.median([c for c, _ in R])))
def paired(a, b):
    lr = np.log(np.array(out[a]["costs"]) / np.array(out[b]["costs"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
out["checks"] = dict(ES8b_1=paired("need_l", "magnitude_l"), ES8b_2=paired("need_l", "random"), ES8b_3=paired("need_l", "need"))
print(json.dumps(out, indent=1))
