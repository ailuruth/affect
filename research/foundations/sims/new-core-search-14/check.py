"""Pass-14 critique checks of new-core-search-13-synthesis.md, Changes A and B.

ALGEBRA ON SYNTHETIC SIGNALS ONLY. NOT evidence about people, about behaviour, or about the engine as built.
numpy only. Usage:  python3 -I -B check.py > out.txt   (well under a minute)

C1  band-pass step responses and sup gains (the 0.650 at 1.19 s, 0.505 at 39 s, kappa_F)
C2  the J3 share arithmetic on LP with a fast band carved out of s_A
C3  Change A's omega^s rule as written: saturation, late-hurt dilution, tempo, D_start -> 0
C4  a time-indexed alternative for omega^s (the general fix), same scenarios
C5  Change B with a selection that follows sign(xi_F): windowed pooled slope versus Lemma S(i)'s sup-gain bound
C6  the rectified echo under a gate that follows his slow level (R1g with a minutes-scale gate input)
"""
import numpy as np

FS = 30.0
DT = 1.0 / FS


def lp(x, tau, x0=None):
    a = 1.0 - np.exp(-DT / tau)
    y = np.empty_like(x)
    s = x[0] if x0 is None else x0
    for i in range(len(x)):
        s += a * (x[i] - s)
        y[i] = s
    return y


def ou(n, tau, sd, rng):
    a = np.exp(-DT / tau)
    e = rng.standard_normal(n) * sd * np.sqrt(1 - a * a)
    y = np.empty(n)
    s = 0.0
    for i in range(n):
        s = a * s + e[i]
        y[i] = s
    return y


def wmean(x, W):
    k = int(W * FS)
    c = np.cumsum(np.r_[0.0, x])
    return (c[k:] - c[:-k]) / k


def block_slope(y, u, W, maxlag_s=3.0):
    """pooled toward slope of block (non-overlapping) means of y on u, best lag 0..maxlag (y lags u)"""
    best = -np.inf
    k = int(W * FS)
    for L in np.arange(0, maxlag_s + 1e-9, 0.5):
        l = int(L * FS)
        yy = y[l:]
        uu = u[:len(u) - l] if l else u
        nb = len(yy) // k
        yb = yy[:nb * k].reshape(nb, k).mean(1)
        ub = uu[:nb * k].reshape(nb, k).mean(1)
        ub = ub - ub.mean()
        b = np.dot(yb - yb.mean(), ub) / np.dot(ub, ub)
        best = max(best, b)
    return best


print(__doc__)

# ---------------------------------------------------------------- C1
print("C1  band-pass h_a - h_b: step response e^{-t/b} - e^{-t/a}; sup gain (b-a)/(a+b) at w=1/sqrt(ab), phase 0 there")
for a, b in [(0.5, 4.0), (20.0, 90.0)]:
    ts = np.log(b / a) * a * b / (b - a)
    pk = np.exp(-ts / b) - np.exp(-ts / a)
    w = np.logspace(-4, 2, 200001)
    H = 1 / (1 + 1j * w * a) - 1 / (1 + 1j * w * b)
    i = np.argmax(np.abs(H))
    print(f"   {a}/{b} s: t* = {ts:.3f} s, peak = {pk:.4f}; sup|H| = {np.abs(H).max():.4f} (formula {(b-a)/(a+b):.4f}) "
          f"at {w[i]:.4f} rad/s = {w[i]/2/np.pi:.4f} Hz, phase {np.degrees(np.angle(H[i])):.2f} deg")
# step response after 4 s and 12 s for the fast band
for t in (4.0, 8.0, 12.0):
    print(f"   0.5/4 step response at {t:.0f} s: {np.exp(-t/4)-np.exp(-t/0.5):.4f}")
# a held periodic input: response stays
print("   a partner who repeats a 1-s smile every 3 s keeps the fast band at a sustained in-phase level (no 'hold' needed):")
n = int(600 * FS)
t = np.arange(n) * DT
u = ((t % 3.0) < 1.0).astype(float)
xi = lp(u, 0.5) - lp(u, 4.0)
print(f"   max|xi_F| over the last 5 min = {np.abs(xi[n//2:]).max():.3f}; mean xi_F = {xi[n//2:].mean():+.4f} "
      f"(zero DC); mean max(xi_F,0) = {np.maximum(xi[n//2:],0).mean():.4f}")

# ---------------------------------------------------------------- C2
print("\nC2  J3 share arithmetic on LP: s_C(1+rho) + s_X + 0.636 s_A^slow + kF s_F + r_k <= 0.974")
sC, sX, sA, rk, rho = 0.22, 0.05, 0.12, 0.608, 0.091
kS, kF = 70/110, 3.5/4.5
base = sC * (1 + rho) + sX + kS * sA + rk
print(f"   as built: {base:.4f} (slack to 0.974: {0.974-base:+.4f})")
for sAs, sF in [(0.06, 0.06), (0.12, 0.0), (0.06, 0.049), (0.0, 0.098)]:
    tot = sC * (1 + rho) + sX + kS * sAs + kF * sF + rk
    print(f"   s_A^slow {sAs:.3f}, s_F {sF:.3f}: total {tot:.4f}  {'OVER the as-built total' if tot > base + 1e-6 else 'within the as-built total'};"
          f" fast diagonal {sF*0.35:.4f} absolute")
print(f"   largest s_F with s_A^slow = s_A/2: {(kS*sA - kS*sA/2)/kF:.4f}")

# ---------------------------------------------------------------- C3 / C4
print("\nC3  Change A as written: s_t = clip(0.3 + 0.7 min(1, rho_rel(t)/0.6) - 1.3 min(1, hbar(t)/0.10), -1, 1),")
print("    rho_rel(t) = cumulative relief so far / Dstart, hbar(t) = running session mean of the hurt latch (tau 10 min),")
print("    omega^s <- omega^s + (s_t - omega^s)/8 at each relief or hurt event; omega^s(0) = 0.5")
print("C4  fix (event-gated delta rule on each event's own content; no running sums, no division by Dstart or by")
print("    elapsed time): at a relief event with amplitude a_r = R'/(R'+0.02): s_e = 0.3 + 0.7 a_r, step a_r/8;")
print("    at a hurt event v_w: s_e = clip(0.3 - 1.3 min(1, v_w/0.10)), step a_d/8, a_d = v_w/(v_w+0.02);")
print("    omega~ <- omega~ + step (s_e - omega~). No event, no change (so Korb-type retention without pairings)\n")


def run_A(T_min, relief_every_min, relief_amt, hurt_at_min, hurt_amt, Dstart, stop_relief_min=None, sample_mins=()):
    dt = 1.0
    nT = int(T_min * 60)
    cum = 0.0
    h = 0.0
    hint = 0.0
    om = 0.5
    omf = 0.5
    out = {}
    for i in range(nT):
        tm = i / 60.0
        ev = False
        rel = 0.0
        hurt_now = 0.0
        if relief_every_min and i > 0 and (i % int(relief_every_min * 60) == 0) and \
                (stop_relief_min is None or tm < stop_relief_min):
            rel = relief_amt
            cum += rel
            ev = True
        if hurt_at_min is not None and i == int(hurt_at_min * 60):
            h = max(h, hurt_amt)
            hurt_now = hurt_amt
            ev = True
        h *= np.exp(-dt / 600.0)
        hint += h * dt
        hbar = hint / ((i + 1) * dt)
        if ev:
            rho = cum / max(Dstart, 1e-12)
            st = np.clip(0.3 + 0.7 * min(1, rho / 0.6) - 1.3 * min(1, hbar / 0.10), -1, 1)
            om += (st - om) / 8.0
        if rel:
            ar = rel / (rel + 0.02)
            omf += ar / 8.0 * ((0.3 + 0.7 * ar) - omf)
        if hurt_now:
            ad = hurt_now / (hurt_now + 0.02)
            omf += ad / 8.0 * (np.clip(0.3 - 1.3 * min(1, hurt_now / 0.10), -1, 1) - omf)
        for m in sample_mins:
            if abs(tm - m) < 1e-9:
                out[m] = (om, omf)
    return out


mins = (5, 10, 30, 60, 95, 120)
print("   S1 friendly long session: Dstart 0.05, relief 0.01 every 2 min, no hurt (omega^s as written / omega~ fix):")
r = run_A(125, 2, 0.01, None, 0, 0.05, sample_mins=mins)
print("     " + "  ".join(f"{m}m {r[m][0]:.2f}/{r[m][1]:.2f}" for m in mins))
print("   S1' larger reliefs, 0.05 every 2 min:")
r = run_A(125, 2, 0.05, None, 0, 0.05, sample_mins=mins)
print("     " + "  ".join(f"{m}m {r[m][0]:.2f}/{r[m][1]:.2f}" for m in mins))
print("   S2 one hurt of 0.10 (his words) early (min 10) or late (min 100) in the S1 session; lowest value in the 20 min after:")
for hm in (10, 100):
    sm = [hm - 1 + k for k in range(0, 22)]
    r = run_A(130, 2, 0.01, hm, 0.10, 0.05, sample_mins=sm)
    print(f"     hurt at {hm:3d} min: 1 min before {r[hm-1][0]:.2f}/{r[hm-1][1]:.2f}  lowest in the 20 min after "
          f"{min(v[0] for v in r.values()):.2f}/{min(v[1] for v in r.values()):.2f}")
print("   S3 tempo: identical relief per event, events every 1 min vs every 4 min; minutes until >= 0.9 (as written):")
for ev in (1, 4):
    sm = tuple(range(1, 121))
    r = run_A(125, ev, 0.01, None, 0, 0.05, sample_mins=sm)
    first = next((m for m in sm if r[m][0] >= 0.9), None)
    print(f"     every {ev} min: omega^s reaches 0.9 at {first} min; omega~ at 120 min = {r[120][1]:.2f}")
print("   S4 Dstart -> 0 (every drive inside its dead-band at session start makes D = 0 reachable):")
for Ds in (0.05, 0.005, 0.0005):
    r = run_A(25, 2, 0.001, None, 0, Ds, sample_mins=(4, 20))
    print(f"     Dstart {Ds:<7}: relief 0.001 per event; omega^s at 4 min {r[4][0]:.2f}, at 20 min {r[20][0]:.2f} "
          f"(omega~ {r[20][1]:.2f}); rho_rel after one event = {0.001/Ds:.2f}")
print("   S5 retention: relief 0.05 every 2 min for 30 min, then 60 min with nothing (Korb's unreinforced test):")
r = run_A(95, 2, 0.05, None, 0, 0.05, stop_relief_min=30, sample_mins=(30, 60, 90))
print("     " + "  ".join(f"{m}m {v[0]:.2f}/{v[1]:.2f}" for m, v in r.items()))

# ---------------------------------------------------------------- C5
print("\nC5  Change B: y = Gamma^F(alpha) xi_F with diagonal in [-s, s]. Lemma S(i): |beta| <= s sup|H| holds for the")
print("    raw (unwindowed) slope whatever alpha does. The J3 bound is on WINDOWED block means. Adversary: alpha follows")
print("    sign(xi_F) (y = s|xi_F|) or half-wave (y = s max(xi_F,0)); partner: slow mood L (OU 5 min) and fast movement")
print("    whose amplitude rises with L (more active when in a smiling mood). Slope/s, best lag 0-3 s, vs 0.778:")
rng = np.random.default_rng(14)
n = int(2 * 3600 * FS)
L = 0.10 + ou(n, 300.0, 0.03, rng)
nf = ou(n, 1.5, 1.0, rng)
for label, A in [("activity independent of mood", 0.05 * np.ones(n)),
                 ("activity rises with mood", 0.05 * np.exp((L - 0.10) / 0.03))]:
    u = L + A * nf
    xi = lp(u, 0.5) - lp(u, 4.0)
    row = []
    for name, y in [("linear", xi), ("|xi|", np.abs(xi)), ("max(xi,0)", np.maximum(xi, 0))]:
        row.append(name + " " + "/".join(f"{block_slope(y, u, W):.3f}" for W in (2, 10, 60, 300)))
    print(f"   {label:30s}: W 2/10/60/300 s  " + ";  ".join(row))
print("   control, the slow band (20-90 s) under the same sign(xi_A) adversary, mood-coupled partner (vs 0.636):")
u = L + 0.05 * np.exp((L - 0.10) / 0.03) * nf
xs = lp(u, 20.0) - lp(u, 90.0)
print("     |xi_A| " + "/".join(f"{block_slope(np.abs(xs), u, W):.3f}" for W in (2, 10, 60, 300)))
xi = lp(u, 0.5) - lp(u, 4.0)
sgn = np.sign(lp(L, 60.0) - 0.10)
print("   fix: selection from T-like inputs only, slower than the band (here sign of a 60-s trace of his mood, i.e.")
print("     perfectly mood-correlated but blind to xi_F's sign): y = sgn * xi_F, mood-coupled partner:")
print("     " + "/".join(f"{block_slope(sgn * xi, u, W):.3f}" for W in (2, 10, 60, 300)) + "  (vs 0.778)")
print(f"   mood-coupled partner: mean s|xi_F| / s = {np.abs(xi).mean():.4f} (a held offset while he moves; "
      f"with s_F c = 0.0172 on LP that is {0.0172*np.abs(xi).mean():.5f} absolute)")

# ---------------------------------------------------------------- C6
print("\nC6  R1g with a minutes-scale gate input: echo per unit gain e = max(x_d - lp4(x_d), 0), x_d = u(t - 0.45 s);")
print("    smile bursts (1-s, amplitude 0.25) at a Poisson rate that follows his mood; g constant vs g following his")
print("    mood through a 5-min trace (the shape omega^s takes when his words track his mood). Block slope of g*e on u,")
print("    per unit gain, times PHI_LP = 0.64 gives units of c_LP:")
rng = np.random.default_rng(141)
n = int(2 * 3600 * FS)
Lm = ou(n, 600.0, 1.0, rng)
rate = 4.0 / 60 * np.exp(0.6 * Lm)  # bursts per s
on = rng.random(n) < rate * DT
burst = np.convolve(on.astype(float), np.ones(int(FS)), mode="full")[:n]
u = 0.05 + 0.25 * np.minimum(burst, 1.0)
d = int(0.45 * FS)
xd = np.r_[np.full(d, u[0]), u[:-d]]
e = np.maximum(xd - lp(xd, 4.0), 0)
trace = lp(Lm, 300.0)
for name, g in [("g = 1", np.ones(n)), ("g = 0.6 constant", 0.6 * np.ones(n)),
                ("g = clip(0.6 + 0.4 trace)", np.clip(0.6 + 0.4 * trace, 0, 1)),
                ("g = 1{trace > 0}", (trace > 0).astype(float))]:
    y = g * e
    s = [block_slope(y, u, W) * 0.64 for W in (60, 300)]
    print(f"   {name:28s}: 60-s blocks {s[0]:.3f} c, 5-min blocks {s[1]:.3f} c")
print("   weak coupling: his smile-burst rate changes only slightly with mood (exp(0.1 L)), while the gate input")
print("   follows his mood fully (his words track his mood; omega^s follows his words):")
rate = 4.0 / 60 * np.exp(0.1 * Lm)
on = rng.random(n) < rate * DT
burst = np.convolve(on.astype(float), np.ones(int(FS)), mode="full")[:n]
u = 0.05 + 0.25 * np.minimum(burst, 1.0)
xd = np.r_[np.full(d, u[0]), u[:-d]]
e = np.maximum(xd - lp(xd, 4.0), 0)
for name, g in [("g = 1", np.ones(n)), ("g = clip(0.6 + 0.4 trace)", np.clip(0.6 + 0.4 * trace, 0, 1)),
                ("g = 1{trace > 0}", (trace > 0).astype(float))]:
    y = g * e
    s_ = [block_slope(y, u, W) * 0.64 for W in (60, 300)]
    print(f"   {name:28s}: 60-s blocks {s_[0]:.3f} c, 5-min blocks {s_[1]:.3f} c")
print("   Lemma S(ii) case made explicit: smile bursts at a FIXED rate, his resting level higher by dU in 'up'")
print("   20-min stretches than in 'down' ones (a mood), gate input following the mood (his words do):")
rng2 = np.random.default_rng(142)
tt = np.arange(n) * DT
m = ((tt // 1200) % 2).astype(float)
mt = lp(m, 300.0)
for rate_min, dU, det in [(4.0, 0.02, False), (8.0, 0.005, False), (8.0, 0.005, True), (8.0, 0.02, True)]:
    if det:  # deterministic bursts every 60/rate s: no burst-count noise in the block means
        on = (np.arange(n) % int(FS * 60 / rate_min)) == 0
    else:
        on = rng2.random(n) < (rate_min / 60) * DT
    burst = np.convolve(on.astype(float), np.ones(int(FS)), mode="full")[:n]
    u = 0.05 + dU * m + 0.25 * np.minimum(burst, 1.0)
    xd = np.r_[np.full(d, u[0]), u[:-d]]
    e = np.maximum(xd - lp(xd, 4.0), 0)
    for name, g in [("g = 1", np.ones(n)), ("g = 0.3 + 0.7 lp_300s(mood)", 0.3 + 0.7 * mt),
                    ("g = 1{lp300(mood) > 0.5}", (mt > 0.5).astype(float))]:
        y = g * e
        s_ = [block_slope(y, u, W) * 0.64 for W in (60, 300, 1200)]
        print(f"   {'fixed' if det else 'Poisson'} {rate_min:.0f}/min, dU {dU:.3f}, {name:28s}: 60-s {s_[0]:.3f} c, 5-min {s_[1]:.3f} c, 20-min {s_[2]:.3f} c")
        if det and name != "g = 1":
            # fix: the varying part of the gate multiplies a zero-DC factor (Lemma S applied to the varying part)
            g0 = g[0]
            yc = g0 * e + (g - g0) * (e - lp(e, 60.0))
            s_ = [block_slope(yc, u, W) * 0.64 for W in (60, 300, 1200)]
            hi = g >= 0.95 * g.max()
            peak_ratio = yc[hi].max() / (g[hi] * e[hi]).max()
            print(f"     centred fix, same gate                 : 60-s {s_[0]:.3f} c, 5-min {s_[1]:.3f} c, 20-min {s_[2]:.3f} c;"
                  f" per-burst echo kept to {peak_ratio:.3f} of the uncentred peak where the gate is open;"
                  f" min output {yc.min():+.4f} (negative = below rest on a one-sided channel)")
            ycl = np.clip(yc, 0.0, np.maximum(e, 0.0))  # one-sided and never above the open echo
            s_ = [block_slope(ycl, u, W) * 0.64 for W in (60, 300, 1200)]
            print(f"     centred fix, clipped to [0, e]         : 60-s {s_[0]:.3f} c, 5-min {s_[1]:.3f} c, 20-min {s_[2]:.3f} c")
print("   above Claim O'''s floor (block SD of his means >= 0.03): bursts of 0.5 at a fixed 15/min, dU = 0.06:")
on = (np.arange(n) % int(FS * 4)) == 0
burst = np.convolve(on.astype(float), np.ones(int(FS)), mode="full")[:n]
u = 0.05 + 0.06 * m + 0.5 * np.minimum(burst, 1.0)
xd = np.r_[np.full(d, u[0]), u[:-d]]
e = np.maximum(xd - lp(xd, 4.0), 0)
k = int(300 * FS)
print(f"     SD of his 5-min block means = {u[:len(u)//k*k].reshape(-1, k).mean(1).std():.4f}")
for name, g in [("g = 1", np.ones(n)), ("g = 0.3 + 0.7 lp_300s(mood)", 0.3 + 0.7 * mt), ("g = 1{lp300(mood) > 0.5}", (mt > 0.5).astype(float))]:
    s_ = [block_slope(g * e, u, W) * 0.64 for W in (60, 300, 1200)]
    print(f"     {name:28s}: 60-s {s_[0]:.3f} c, 5-min {s_[1]:.3f} c, 20-min {s_[2]:.3f} c")
print("   (r_k, the onset-lobe allowance counted for the echo in J3, is 0.608 c on LP; R1g is declared <= 0.31 c)")
print("\n(end; synthetic algebra only)")
