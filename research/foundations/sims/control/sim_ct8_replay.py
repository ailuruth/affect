"""CT8: replay by persistence of excitation vs uniform. See PREDICTIONS.md second batch."""
import json
import numpy as np
def run(seed, sel):
    r = np.random.default_rng(seed); eps = []
    for i in range(200):
        amp = 1.0 if r.random() < 0.2 else 0.05; t = np.arange(0, 10, 0.05); y = amp * np.sin(1.5 * t + r.uniform(0, 6.28))
        d = 0.6 * y + 0.1 * r.standard_normal(len(t)); eps.append((y, d))
    if sel: idx = np.argsort([-np.sum(y ** 2) for y, _ in eps])[:20]
    else: idx = r.choice(200, 20, replace=False)
    Y = np.concatenate([eps[i][0] for i in idx]); D = np.concatenate([eps[i][1] for i in idx])
    return abs(float(Y @ D / (Y @ Y)) - 0.6)
E = [run(s, True) for s in range(50)]; U = [run(s, False) for s in range(50)]
print(json.dumps(dict(median_err_excitation=float(np.median(E)), median_err_uniform=float(np.median(U)), ratio=float(np.median(E) / np.median(U))), indent=1))
