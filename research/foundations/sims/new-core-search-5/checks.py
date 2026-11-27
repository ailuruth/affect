"""Checks for new-core-search-5-synthesis.md, Direction 3 (hazard-modulated modes).
numpy only. Hand-made semi-Markov processes; verifies mechanism only, not behaviour.
C1: a partner covariate that depends on the agent's current mode shifts time-averaged
    occupancy by exp(-beta*dc) (exponential dwells), with no learning anywhere.
C2: a partner covariate that is the same for every mode (a scalar tempo signal) still
    shifts occupancy when baseline dwell shapes differ (Weibull k=1 vs k=3).
"""
import numpy as np
rng = np.random.default_rng(0)

def simulate(n_modes, base_rate, shape, cov_of_mode, beta, T=200000.0):
    # continuous-time proportional hazards: H(t) = (rate*t)^k * exp(beta*c)
    t, m = 0.0, 0
    occ = np.zeros(n_modes)
    while t < T:
        c = cov_of_mode(m)
        u = rng.random()
        # survival S(t)=exp(-(r t)^k e^{beta c}) -> t = ((-ln u)/e^{beta c})^{1/k}/r
        d = ((-np.log(u)) / np.exp(beta * c)) ** (1.0 / shape[m]) / base_rate[m]
        occ[m] += d; t += d
        m = rng.choice([j for j in range(n_modes) if j != m])  # uniform jump chain
    return occ / occ.sum()

# C1: two modes, exponential dwells, partner gives covariate 1 only in mode 0
beta = -0.5
p0 = simulate(2, [1.0, 1.0], [1, 1], lambda m: 0.0, beta)
p1 = simulate(2, [1.0, 1.0], [1, 1], lambda m: 1.0 if m == 0 else 0.0, beta)
print("C1 occupancy, no partner covariate:", np.round(p0, 3))
print("C1 occupancy, covariate in mode 0 :", np.round(p1, 3),
      " ratio", round(p1[0] / p1[1], 3), " predicted", round(np.exp(-beta), 3))

# C2: same scalar covariate in every mode, Weibull shapes differ
q0 = simulate(2, [1.0, 1.0], [1, 3], lambda m: 0.0, beta)
q1 = simulate(2, [1.0, 1.0], [1, 3], lambda m: 1.0, beta)
print("C2 occupancy, covariate 0 everywhere:", np.round(q0, 3))
print("C2 occupancy, covariate 1 everywhere:", np.round(q1, 3))
# analytic: mean dwell = Gamma(1+1/k) * e^{-beta c / k} / r
from math import gamma, exp
for c in (0.0, 1.0):
    mu = [gamma(1 + 1 / k) * exp(-beta * c / k) for k in (1, 3)]
    print("C2 analytic, c=%.0f:" % c, np.round(np.array(mu) / sum(mu), 3))
