"""Toy environment T1 for the Costate candidate: one need (contact), a scripted user.

Not engine code. Parameters are fixed here and are not changed after results are seen.
Time step 1 min. Contact b in [0,1]:
  user absent : db/dt = -K_A * b             (K_A = 1/h)
  user present: db/dt =  K_P * (1 - b)       (K_P = 6/h)
Drive d(b) = (b - B_STAR)^2, B_STAR = 0.8. Discount RHO = 1/h.
Day schedule: session starts at 09:00 + U(-30,30) min; three 60-min blocks of presence separated by
10-min breaks announced 'brb'; the last block ends with 'bye'. Events: arrive, brb, bye.
"""
import numpy as np

DT_H = 1.0 / 60.0
K_A, K_P, B_STAR, RHO = 1.0, 6.0, 0.8, 1.0
EVENTS = ["none", "arrive", "brb", "bye"]
MIN_PER_DAY = 24 * 60


def schedule(n_days, rng):
    """Return per-minute arrays: present (0/1), event index."""
    T = n_days * MIN_PER_DAY
    present = np.zeros(T, dtype=np.int8)
    event = np.zeros(T, dtype=np.int8)
    for d in range(n_days):
        t = d * MIN_PER_DAY + 9 * 60 + 5 * int(rng.integers(-6, 7))
        for blk in range(3):
            event[t] = 1  # arrive
            present[t:t + 60] = 1
            t += 60
            if blk < 2:
                event[t] = 2  # brb (10-min break)
                t += 10
            else:
                event[t] = 3  # bye
    return present, event


def body(present, b0=0.0):
    b = np.empty(len(present))
    x = b0
    for t, p in enumerate(present):
        b[t] = x
        x = x + DT_H * (K_P * (1 - x) if p else -K_A * x)
    return b


def drive(b):
    return (b - B_STAR) ** 2


def cost_to_go(b, present):
    """Exact discounted cost-to-go V_t = sum_{s>=t} e^{-rho (s-t) dt} d(b_s) dt (backward recursion)."""
    g = np.exp(-RHO * DT_H)
    V = np.zeros(len(b))
    acc = 0.0
    for t in range(len(b) - 1, -1, -1):
        acc = drive(b[t]) * DT_H + g * acc
        V[t] = acc
    return V


def costate_at(t, present, b_override, eps=1e-4):
    """mu = -dV/db at time t, holding the user's future schedule fixed (finite difference)."""
    def V_from(b0):
        b = body(present[t:], b0)
        return cost_to_go(b, present[t:])[0]
    return -(V_from(b_override + eps) - V_from(b_override - eps)) / (2 * eps)
