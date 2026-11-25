"""Derivation for sim F (S1 separation-reunion lesion study): exact costate at reunion and call timing.
Intact: exact future (standard 3-block session at reunion, then absent ~21h). Lesion A: stationary forecast p_bar.
"""
import numpy as np
from env_t1 import *
PBAR = 3.0 / 24.0

def session_after(n_before=0):
    p = [0]*n_before
    for blk in range(3):
        p += [1]*60 + ([0]*10 if blk < 2 else [])
    p += [0]*(MIN_PER_DAY*2)
    return np.array(p, dtype=np.int8)

def mu_exact(b0, pres, eps=1e-4):
    f = lambda x: cost_to_go(body(pres, x), pres)[0]
    return -(f(b0+eps) - f(b0-eps))/(2*eps)

def mu_meanfield(b0, p, eps=1e-4, H=6*60):
    def V(x):
        b=x; v=0.0
        for k in range(H):
            b = b + DT_H*(K_P*p*(1-b) - K_A*(1-p)*b); v += np.exp(-RHO*DT_H*(k+1))*(b-B_STAR)**2*DT_H
        return v
    return -(V(b0+eps)-V(b0-eps))/(2*eps)

L0, A_OVER_C, MU_E = 50.0, 10.0, 0.02
Lstar = lambda mu: L0*max(np.log(mu*A_OVER_C/MU_E), 0.0)
b_bye = 1.0
for S_min in [10, 60, 180, 1240]:
    b = b_bye*np.exp(-K_A*S_min/60)
    mi = mu_exact(b, session_after()); ma = mu_meanfield(b, PBAR)
    print(f"S={S_min:5d} min b={b:.3f}  intact mu={mi:.4f} L*={Lstar(mi):6.1f} | lesionA mu={ma:.4f} L*={Lstar(ma):6.1f}")
# call timing after bye with theta=0.3: intact exact (next session starts ~1240 min later), lesion A mean-field
TH=0.3
for name, fn in [("intact", lambda t: mu_exact(np.exp(-K_A*t/60), session_after(1240-t))), ("lesionA", lambda t: mu_meanfield(np.exp(-K_A*t/60), PBAR))]:
    tc=None
    for t in range(0, 1240, 5):
        if fn(t) >= TH: tc=t; break
    print(name, "call at min after bye:", tc)
