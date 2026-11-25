"""ES8: need-conditioned attention over perceived cues. See PREDICTIONS.md."""
import json, math
import numpy as np
SIG = np.array([0.35, 0.30, 0.25]); T, M, KOBS = 2000, 6, 2
MU = 0.1 * np.eye(3); SD = np.full((3, 3), 0.05); np.fill_diagonal(SD, SIG)  # SD[type, need]
def run(seed, arm):
    rw = np.random.default_rng(seed); ra = np.random.default_rng(seed + 3000)
    types = rw.integers(0, 3, (T, M)); DB = MU[types] + SD[types] * rw.standard_normal((T, M, 3)); obsn = 0.05 * rw.standard_normal((T, M, 3))
    b = np.zeros(3); cost = []; match = []
    for t in range(T):
        dr = np.full(3, 0.02); dr[(t // 50) % 3] = 0.15; b = np.minimum(b - dr, 1.0); e = np.maximum(-b, 0); ty = types[t]
        if arm == "full": obs = np.arange(M)
        elif arm == "none": obs = np.array([], int)
        else:
            if arm == "need": sc = np.sqrt(((SD[ty] ** 2) * e ** 2).sum(1))
            elif arm == "magnitude": sc = np.sqrt((SD[ty] ** 2).sum(1))
            else: sc = np.zeros(M)
            sc = sc + 1e-9 * ra.random(M); obs = np.argsort(-sc)[:KOBS]
        est = MU[ty].copy(); est[obs] = DB[t, obs] + obsn[t, obs]; val = est @ e
        ch = int(np.argmax(val)) if val.max() > 0.01 else -1
        if t >= 200:
            cost.append(0.5 * e @ e)
            if arm in ("need", "magnitude", "random") and e.max() > 0: match.append(float(np.mean(ty[obs] == int(np.argmax(e)))))
        if ch >= 0: b = np.minimum(b + DB[t, ch], 1.0)
    return float(np.mean(cost)), (float(np.mean(match)) if match else None)
out = {}
for arm in ("need", "magnitude", "random", "full", "none"):
    R = [run(s, arm) for s in range(40)]; out[arm] = dict(costs=[c for c, _ in R], match=(float(np.mean([m for _, m in R])) if R[0][1] is not None else None), geo=float(np.exp(np.mean(np.log([c for c, _ in R])))))
def paired(a, b):
    lr = np.log(np.array(out[a]["costs"]) / np.array(out[b]["costs"])); m, se = lr.mean(), lr.std(ddof=1) / math.sqrt(len(lr))
    return dict(geo_ratio=float(np.exp(m)), ci=[float(np.exp(m - 1.96 * se)), float(np.exp(m + 1.96 * se))], wins=int((lr < 0).sum()), n=len(lr))
g = {k: out[k]["geo"] for k in out}
out["checks"] = dict(ES8_1=paired("need", "magnitude"), ES8_2=paired("need", "random"), ES8_3_gap_closed=(math.log(g["none"]) - math.log(g["need"])) / (math.log(g["none"]) - math.log(g["full"])),
                     ES8_4_need=out["need"]["match"], ES8_4_magnitude=out["magnitude"]["match"])
print(json.dumps(out, indent=1))
