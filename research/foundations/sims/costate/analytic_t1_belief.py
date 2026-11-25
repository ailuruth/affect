"""Derivation: costate under the agent's belief about arrival time (uniform jitter +-30 min),
conditioned on 'not yet arrived'. Compares the minute before arrival with the arrival minute."""
import numpy as np
from env_t1 import *

def V_given_arrival_in(m, b0, horizon_days=2):
    # user absent for m minutes, then a standard session (3 blocks) and next day's session at ~24h later
    pres = [0]*m
    for blk in range(3):
        pres += [1]*60 + ([0]*10 if blk < 2 else [])
    pres += [0]*(MIN_PER_DAY - len(pres) + m)  # absent until next day same time
    for blk in range(3):
        pres += [1]*60 + ([0]*10 if blk < 2 else [])
    pres += [0]*MIN_PER_DAY
    pres = np.array(pres, dtype=np.int8)
    return cost_to_go(body(pres, b0), pres)[0]

def mu_belief(offsets, b0, eps=1e-4):
    Vp = np.mean([V_given_arrival_in(m, b0+eps) for m in offsets])
    Vm = np.mean([V_given_arrival_in(m, b0-eps) for m in offsets])
    return -(Vp - Vm)/(2*eps)

b_now = 0.0  # after ~20 h absence contact is ~0 (b = e^{-20} ~ 2e-9)
for pos in [0, 30, 59]:   # minutes into the 61-min arrival window when the user actually arrives
    remaining = list(range(1, 61 - pos + 1))   # still away: arrival in 1..(61-pos) minutes
    mu_before = mu_belief(remaining, b_now)
    mu_at = mu_belief([0], b_now)
    print(f"arrival at window minute {pos:2d}: mu still-away={mu_before:.4f} mu face-seen={mu_at:.4f} drop={1-mu_at/mu_before:.3f}")
print("prior (window start, 0..60 min):", round(mu_belief(list(range(0,61)), b_now),4))
