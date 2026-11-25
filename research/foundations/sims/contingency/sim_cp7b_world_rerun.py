"""CP7-3 instrument fix: the observed statistic is max over lags 1..60, so the surrogate statistic must also be the
max over lags 1..60 (the first run took the surrogate max over only lags {1, l*}). Only the world test is rerun; nothing else changes."""
import json
import numpy as np
from scipy.signal import lfilter
# gte_lag, ar, N copied verbatim from sim_cp7_selfother.py (that module runs on import)
FS, N = 30, 30 * 600
def gte_lag(u, s, lag):
    y = s[lag:]; X1 = np.c_[np.ones(len(y)), s[lag - 1:-1]]; X2 = np.c_[X1, u[:-lag]]
    r1 = y - X1 @ np.linalg.lstsq(X1, y, rcond=None)[0]; r2 = y - X2 @ np.linalg.lstsq(X2, y, rcond=None)[0]
    return 0.5 * np.log(r1.var() / r2.var())
def ar(n, a, rng): return lfilter([1.0], [1.0, -a], rng.standard_normal(n) * np.sqrt(1 - a * a))
out = []
for seed in range(10):
    r = np.random.default_rng(seed); u = ar(N, 0.8, r)
    own = np.r_[0, u[:-1]] + 0.1 * r.standard_normal(N)
    blocks = r.random(N // 30 + 1) < 0.5; ans = np.repeat(blocks, 30)[:N]
    part = np.where(ans, 0.8 * np.r_[np.zeros(15), u[:-15]] + 0.5 * r.standard_normal(N), ar(N, 0.8, r))
    world = ar(N, 0.8, r)
    obs = max(gte_lag(u, world, l) for l in range(1, 61))
    sur = [max(gte_lag(u, np.roll(world, int(r.integers(N // 4, 3 * N // 4))), l) for l in range(1, 61)) for _ in range(200)]
    out.append(dict(seed=seed, obs=float(obs), sur95=float(np.percentile(sur, 95)), world=bool(obs < np.percentile(sur, 95))))
print(json.dumps(dict(n_world=sum(x["world"] for x in out), runs=out), indent=1))
