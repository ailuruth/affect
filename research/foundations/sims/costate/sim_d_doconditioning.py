"""D: do-conditioning removes the value of flattery. Parameters in PREDICTIONS.md."""
import json
import numpy as np

KAPPA, ETA, LAM, SIG_N, SIG_P = 0.3, 0.1, 0.5, 0.1, 0.2


def learn(khat, alpha, seed, steps=20000, lr=1e-3):
    r = np.random.default_rng(seed); m = 0.0; base = 0.0
    for _ in range(steps):
        a = m + SIG_P * r.standard_normal()
        x = -1.0 + alpha * a
        y = x + KAPPA * a + SIG_N * r.standard_normal()
        xhat = y - khat * a
        cost = ETA * a ** 2 + LAM * xhat ** 2
        m -= lr * (cost - base) * (a - m) / SIG_P ** 2
        base += 0.01 * (cost - base)
    return m


out = {}
for name, khat, alpha in [("naive_a0", 0.0, 0.0), ("do_a0", 0.3, 0.0), ("miscal_a0", 0.2, 0.0), ("naive_a005", 0.0, 0.05), ("do_a005", 0.3, 0.05)]:
    ms = [learn(khat, alpha, s) for s in range(10)]
    k = KAPPA - khat + alpha
    out[name] = dict(mean=float(np.mean(ms)), sd=float(np.std(ms)), analytic=LAM * k / (ETA + LAM * k ** 2))
print(json.dumps(out, indent=1))
