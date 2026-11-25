"""CP7: self/other/world from the contingency spectrum. See PREDICTIONS.md."""
import json
import numpy as np
from scipy.signal import lfilter
FS, N = 30, 30 * 600
def gte_lag(u, s, lag):
    y = s[lag:]; X1 = np.c_[np.ones(len(y)), s[lag - 1:-1]]; X2 = np.c_[X1, u[:-lag]]
    r1 = y - X1 @ np.linalg.lstsq(X1, y, rcond=None)[0]; r2 = y - X2 @ np.linalg.lstsq(X2, y, rcond=None)[0]
    return 0.5 * np.log(r1.var() / r2.var())
def ar(n, a, rng): return lfilter([1.0], [1.0, -a], rng.standard_normal(n) * np.sqrt(1 - a * a))
res = []
for seed in range(10):
    r = np.random.default_rng(seed); u = ar(N, 0.8, r)
    own = np.r_[0, u[:-1]] + 0.1 * r.standard_normal(N)
    blocks = r.random(N // 30 + 1) < 0.5; ans = np.repeat(blocks, 30)[:N]
    part = np.where(ans, 0.8 * np.r_[np.zeros(15), u[:-15]] + 0.5 * r.standard_normal(N), ar(N, 0.8, r))
    world = ar(N, 0.8, r)
    curves = {k: np.array([gte_lag(u, s, l) for l in range(1, 61)]) for k, s in (("own", own), ("partner", part), ("world", world))}
    mo = curves["own"].max(); out = {}
    for k, c in curves.items():
        R = c.max() / mo; lstar = int(np.argmax(c) + 1)
        sur = [max(gte_lag(u, np.roll(s_ := {"own": own, "partner": part, "world": world}[k], int(r.integers(N // 4, 3 * N // 4))), l) for l in (1, lstar)) for _ in range(200)]
        world_cls = c.max() < np.percentile(sur, 95)
        cls = "world" if world_cls else ("self" if (R > 0.9 and lstar <= 3) else ("other" if (0.05 < R <= 0.9 and 9 <= lstar <= 60) else "unclassified"))
        out[k] = dict(R=float(R), lag=lstar, cls=cls)
    res.append(out)
summ = {k: dict(classes=[x[k]["cls"] for x in res], lags=[x[k]["lag"] for x in res], R=[round(x[k]["R"], 3) for x in res]) for k in ("own", "partner", "world")}
print(json.dumps(summ, indent=1))
