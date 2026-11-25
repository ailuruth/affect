"""Derivation for CS1: per-person costate under each person's predicted schedule (T1 body dynamics).
Fixed after VERIFICATION-2: the CS1 scenario is B returning in 10 min (PREDICTIONS CS1); the first version of
this script printed a 60-min case, while sim_cs1_field.py hard-coded the 10-min value. Also sweeps B's return delay."""
import numpy as np
from env_t1 import body, cost_to_go
def mu_person(b0, absent_min, present_min, eps=1e-4):
    pres = np.array([0]*absent_min + [1]*present_min + [0]*(48*60), dtype=np.int8)
    f = lambda x: cost_to_go(body(pres, x), pres)[0]
    return -(f(b0+eps) - f(b0-eps))/(2*eps)
if __name__ == "__main__":
    print("A present now (b=0.95, stays 1h more):", round(mu_person(0.95, 0, 60), 4))
    print("B absent 3d, back in 10 min for 3h (b=0.0):", round(mu_person(0.0, 10, 180), 4))
    print("C absent 12h, back in 24h for 3h (b=0.15):", round(mu_person(0.15, 24*60, 180), 4))
    muC = mu_person(0.15, 24*60, 180)
    for m in [0, 10, 20, 30, 45, 55, 58, 60, 90, 120]:
        muB = mu_person(0.0, m, 180); print(f"B back in {m:3d} min: mu_B={muB:.4f}  mu_B<mu_C: {muB < muC}")
