"""TH6-5b: participation ratio of the body field, two specified schedules, 10 seeds (characterization)."""
import json
import numpy as np
def week(seed, variant):
    r = np.random.default_rng(seed); b = np.full(5, 0.5); traj = []
    for day in range(7):
        pres = {p: (r.random() < 0.5, int(r.uniform(1, 3) * 60), int(r.uniform(8, 20) * 60)) for p in range(3)}
        topic_hour = {t: int(r.integers(8, 21)) * 60 for t in (3, 4)}
        topic = 3
        for m in range(1440):
            any_p = False
            for p in range(3):
                on, dur, st = pres[p]
                if on and st <= m < st + dur: b[p] += (1 - b[p]) / 60; any_p = True
                else: b[p] -= b[p] / 360
            if variant == "A":
                if m % 60 == 0: topic = int(r.choice([3, 4]))
                for t in (3, 4):
                    if t == topic and any_p: b[t] += 2 * (1 - b[t]) / 60
                    else: b[t] -= b[t] / 720
            else:
                for t in (3, 4):
                    if topic_hour[t] <= m < topic_hour[t] + 60: b[t] += 2 * (1 - b[t]) / 60
                    else: b[t] -= b[t] / 720
            traj.append(b.copy())
    return np.array(traj)
def pr(X):
    ev = np.linalg.eigvalsh(np.cov(X.T)); return float(ev.sum() ** 2 / (ev ** 2).sum())
out = {}
for v in ("A", "B"):
    f, c = [], []
    for s in range(10):
        X = week(s, v); f.append(pr(X)); c.append(pr(np.c_[X[:, :3].mean(1), X[:, 3:].mean(1)]))
    out[v] = dict(field=[round(x, 2) for x in f], field_mean=float(np.mean(f)), collapsed=[round(x, 2) for x in c], collapsed_mean=float(np.mean(c)))
print(json.dumps(out, indent=1))
