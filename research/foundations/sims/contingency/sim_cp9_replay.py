"""CP9: prioritized replay tracks a changed relationship. See PREDICTIONS.md."""
import json
import numpy as np
def run(seed, prioritized):
    r = np.random.default_rng(seed); store = []; k = 0.5; traj = []
    for day in range(1, 22):
        true = 0.8 if day <= 7 else 0.2
        store += list(true + 0.15 * r.standard_normal(10)); S = np.array(store)
        p = (np.abs(S - k) + 0.01) if prioritized else np.ones(len(S)); p = p / p.sum()
        for i in r.choice(len(S), 8, p=p): k += 0.3 * (S[i] - k)
        traj.append(k)
    return traj
out = {}
for name, pr in (("uniform", False), ("prioritized", True)):
    T = np.array([run(s, pr) for s in range(50)])
    nights = [next((d - 7 for d in range(8, 22) if abs(t[d - 1] - 0.2) < 0.15), None) for t in T]
    out[name] = dict(median_nights=float(np.median([n if n is not None else 99 for n in nights])), n_never=sum(n is None for n in nights),
                     final_frac_within_0p1=float(np.mean(np.abs(T[:, -1] - 0.2) < 0.1)), final_mean=float(T[:, -1].mean()))
print(json.dumps(out, indent=1))
