"""Critique 6, L3: the design's J7 injected-route recipe, with the ledger output clipped to what the lip can render.
Run: python3 -I ledger_inject.py"""
import numpy as np
src = open(__file__.replace("ledger_inject.py", "routes.py")).read().split("T = int(3 * 3600 * fs)")[0]
exec(src)
TAU_M = [20, 120, 1200, 10800]; F_M = [0, .7, .2, .1]
def blocks(T, L):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(rng.exponential(L * fs)) + 10; x[t:t + n] = rng.uniform(); t += n
    return x
def laughs(rate, T, dur=2.5, spread=0.4):
    z = np.zeros(T); t = 0
    while t < T:
        r = max(rate[min(t, T - 1)], 1e-3) / 60; t += int(rng.exponential(1 / r) * fs) + 1
        if t >= T: break
        dd = max(1, int(np.exp(np.log(dur) + spread * rng.normal()) * fs)); z[t:t + dd] = 1; t += dd
    return z
for seed in range(3):
    rng = np.random.default_rng(100 + seed)
    T7 = int(4 * 3600 * fs); m7 = blocks(T7, 600); L7 = laughs(0.5 + 3 * m7, T7)
    u = np.clip(.15 + .25 * m7 + .35 * L7 + .03 * rng.normal(size=T7), 0, 1)
    yF = fast(u, .224); yC = sum(F_M[m] * .22 * .35 * lp(u - u.mean(), TAU_M[m]) for m in range(4))
    cr = np.clip(.05 + .1 * m7 + .3 * L7, 0, 1); dcr = delay(cr, d)
    inj = 1.6 * np.maximum(dcr - lp(dcr, 4), 0) + 1.0 * lp(cr - cr.mean(), 60)
    ri = np.clip(.09 + yF + inj, 0, 1) - .09
    rp, h, gr = ledger(u, ri, .35); rr = np.clip(rp, -.09, .91); ra, _, _ = ledger(u, ri, .35, atten_only=True)
    f = lambda y: ", ".join(f"{W}: {bslope(u, y, int(W * fs), tuple(range(0, 31, 5)) if W < 60 else (0,)):.2f}" for W in (2, 10, 60))
    print(f"   seed {seed}: injected before [{f(ri)}]; ledger as specified [{f(rp)}], clipped {h:.3f}, |out|>|in| {gr:.3f}, min {rp.min():+.2f}; "
          f"rendered [{f(rr)}]; attenuate-only [{f(ra)}]  (c 0.35)")
    print(f"      ledger output above the input by > 0.3 (a lip-pull flash the partner-caused part did not contain): {np.mean(rp > ri + 0.3):.4f} of frames; "
          f"frames rendered at the lip's top (1.0): {np.mean(rr >= .91 - 1e-9):.4f}; at its floor (0): {np.mean(rr <= -.09 + 1e-9):.4f}")
