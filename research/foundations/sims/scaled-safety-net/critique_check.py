"""Independent critique's check of design-scaled-safety-net.md (synthetic signals; a check of the mathematics, not
evidence about people or behaviour).

Reuses the reference Governor, Ledger, partner recipe and metric of check.py verbatim (its definitions are executed
from its source up to its first experiment), and probes routes and conventions the design did not run:
  K1  the neutral partner u0 is NOT his session mean (the engine's shadow input is b_id, a multi-session baseline)
  K2  time-varying gain: a linear ramp and exponential growth of the copy's gain (theta 300 s, 600 s)
  K3  slow routes: copies low-passed at 120 s and 300 s (the design ran 30 s only)
  K4  a fast echo away from lag 0: a 2-s high-passed copy delayed 30 s (no 2-s key at lags > 3 s in either stage)
  K5  on/off routes: 10 s on / 50 s off; and 6 min on / 24 min off (release and re-detection)
  K6  false-positive cost with u0 != session mean (counted routes only, natural partners seeds 8 and 10)
Pure routes are run at c = 0.05 only: by Lemma 0 (exact, checked in check.py section I) residual / c depends on g/c
and his signal alone. Usage: python3 -I critique_check.py > critique_check.out.txt   (numpy only; about 6-8 min)
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "check.py")).read()
src = src[:src.index("DELAYS = (10, 20, 40")]          # definitions only (signals, metric, Ledger, Governor, run)
sys.argv = ["check.py"]                                 # full 1-h sessions
ns = {"__name__": "check_defs"}
exec(compile(src, "check.py", "exec"), ns)
T, FS, partners, partner, lp, delay = ns["T"], ns["FS"], ns["partners"], ns["partner"], ns["lp"], ns["delay"]
run, wbs, CEIL, GAIN, SIGNED = ns["run"], ns["worst_block_slope"], ns["CEIL"], ns["GAIN"], ns["SIGNED"]
CAPPED = np.where(CEIL > 0)[0]
T0 = time.time()


def stamp(s):
    print(f"[{time.time() - T0:5.0f} s] {s}", flush=True)


print("CRITIQUE CHECK OF THE MATHEMATICS ONLY (synthetic signals; not evidence about people).\n")

C = 0.05
GR = (3.0, 10.0, 33.0)
NP = 2                     # partners per cell: one with 300-s level blocks, one with 30-s level blocks
tt = np.arange(T) / FS
D = 90.0


def causal(v, D_s):
    """v delayed by D_s, 0 before D_s (the shadow and the factual run agree before the route has acted)."""
    x = delay(v, D_s * FS)
    x[:int(np.ceil(D_s * FS))] = 0.0
    return x


def hp(u, tau):
    return u - lp(u[:, None], tau)[:, 0]


FAM = [
    ("copy, u0 = session mean (design's case)", lambda u, m: (causal(u - m, D), m)),
    ("copy, u0 = mean - 0.10 (b_id below today's mean)", lambda u, m: (causal(u - (m - 0.10), D), m - 0.10)),
    ("copy, u0 = mean + 0.05", lambda u, m: (causal(u - (m + 0.05), D), m + 0.05)),
    ("copy, gain ramps linearly 0 -> g over the hour", lambda u, m: (causal(u - m, D) * tt / tt[-1], m)),
    ("copy, gain grows exp., theta 600 s (ends at g)", lambda u, m: (causal(u - m, D) * np.exp((tt - tt[-1]) / 600.0), m)),
    ("copy, gain grows exp., theta 300 s (ends at g)", lambda u, m: (causal(u - m, D) * np.exp((tt - tt[-1]) / 300.0), m)),
    ("copy low-passed tau 120 s", lambda u, m: (lp(causal(u - m, D)[:, None], 120.0)[:, 0], m)),
    ("copy low-passed tau 300 s", lambda u, m: (lp(causal(u - m, D)[:, None], 300.0)[:, 0], m)),
    ("fast echo: 2-s high-passed copy, delay 30 s", lambda u, m: (causal(hp(u - m, 2.0), 30.0), m)),
    ("copy on 10 s / off 50 s", lambda u, m: (causal(u - m, D) * ((tt % 60.0) < 10.0), m)),
    ("copy on 6 min / off 24 min", lambda u, m: (causal(u - m, D) * (((tt + 600.0) % 1800.0) < 360.0), m)),
]

cols = [(fi, g, p) for fi in range(len(FAM)) for g in GR for p in range(NP)]
n = len(cols)
U = partners(n, 2024, [False] * n)
X = np.zeros((T, n)); U0 = np.zeros(n)
for j, (fi, g, p) in enumerate(cols):
    u = U[:, j]; x, u0 = FAM[fi][1](u, u.mean())
    X[:, j] = g * C * x; U0[j] = u0
cvec = np.full(n, C)
stamp(f"K1-K5: {n} pure-route columns at c = {C}, 1-h sessions; running the current ledger and the new net")
O_old, _, _, _ = run(U, X, cvec, "old")
O_new, _, eng, A = run(U, X, cvec, "new", record_a=True, u_neutral=U0)
raw = wbs(U, X) / C; old = wbs(U, O_old) / C; new = wbs(U, O_new) / C
stamp("residual / c (worst over the 2 partners); raw = the route alone")
print(f"   {'route':<50}" + "".join(f"  g/c {g:<4}  raw  cur  NEW" for g in GR))
for fi, (name, _) in enumerate(FAM):
    line = f"   {name:<50}"
    for g in GR:
        js = [j for j, (f2, g2, _) in enumerate(cols) if f2 == fi and g2 == g]
        line += f"  {'':8}{raw[js].max():5.1f} {old[js].max():4.2f} {new[js].max():4.2f}"
    print(line)
# where in time the residual sits, for the growth routes: effective gain a(t) g(t) / c at the end of the session
print("\n   effective gain a(t) g(t) / c at 50 and 60 min (growth routes; the design's target is 0.60):")
for fi in (3, 4, 5):
    for g in GR:
        j = [j for j, (f2, g2, p) in enumerate(cols) if f2 == fi and g2 == g and p == 0][0]
        gt = g * (tt / tt[-1] if fi == 3 else np.exp((tt - tt[-1]) / (600.0 if fi == 4 else 300.0)))
        i50, i60 = int(3000 * FS), T - 1
        print(f"     {FAM[fi][0]:<50} g/c {g:>4}: {A[i50, j] * gt[i50]:.2f} c, {A[i60, j] * gt[i60]:.2f} c")
print()

# ---------------------------------------------------------------- K6: false positives with u0 != his session mean
stamp("K6. cost: natural partners, counted routes only, with the neutral partner u0 = session mean + delta")
for seed in (8, 10):
    Un = partners(33, seed, SIGNED)
    if seed == 10:
        r10 = np.random.default_rng(10); Un = np.stack([partner(T, r10, 30.0) - (0.4 if SIGNED[k] else 0) for k in range(33)], 1)
    for dlt in (-0.10, 0.10):
        Y = np.zeros_like(Un); u0 = Un.mean(0) + dlt
        for k in range(33):
            xd = delay(Un[:, k], 0.45 * FS); xd[:5] = u0[k]                 # before the session: the neutral partner
            e = xd - (u0[k] + lp((xd - u0[k])[:, None], 4.0)[:, 0])
            fast = GAIN[k] * (np.maximum(e, 0) if not SIGNED[k] else e)
            Y[:, k] = fast + 0.22 * CEIL[k] * lp((Un[:, k] - u0[k])[:, None], 120.0)[:, 0]
        On, hn, en, An = run(Un, Y, CEIL, "new", record_a=True, u_neutral=u0)
        w = CAPPED[np.argmax(en[CAPPED])]
        print(f"   seed {seed}, delta {dlt:+.2f}: governor a<1 on {en[CAPPED].max():.4f} of frames (worst channel {w}),"
              f" channels with any a<1: {int((en[CAPPED] > 0).sum())}, min a {An[:, CAPPED].min():.2f};"
              f" ledger stage changed (worst) {hn[CAPPED].max():.4f}")
print()
stamp("done")
