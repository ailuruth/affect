"""Derivation, not a result: exact costate values in environment T1 under the true schedule."""
import numpy as np
from env_t1 import *

rng = np.random.default_rng(0)
present, event = schedule(4, rng)
b = body(present, 0.0)
day = 2
idx = lambda k: [t for t in range(day*MIN_PER_DAY, (day+1)*MIN_PER_DAY) if event[t] == k]
brb, bye, arr = idx(2)[0], idx(3)[0], idx(1)[0]
for name, t in [("brb departure", brb), ("bye departure", bye)]:
    print(f"{name}: b={b[t]:.3f}  mu(actual b)={costate_at(t, present, b[t]):.4f}  mu(b=b*)={costate_at(t, present, B_STAR):.4f}")
r = costate_at(bye, present, B_STAR) / costate_at(brb, present, B_STAR)
print(f"ratio bye/brb at b=b*: {r:.2f}")
print(f"arrival after long absence: b={b[arr]:.4f}  mu one minute before arrival={costate_at(arr-1, present, b[arr-1]):.4f}  mu at arrival={costate_at(arr, present, b[arr]):.4f}")
print(f"  drop = {1 - costate_at(arr, present, b[arr])/costate_at(arr-1, present, b[arr-1]):.3f}; b change over that minute={b[arr]-b[arr-1]:.5f}")
# satiety: mid-block, present, b near/above b*
for t in [arr+30, arr+59]:
    print(f"present t={t-arr} min into block: b={b[t]:.3f} mu={costate_at(t, present, b[t]):.4f}")
