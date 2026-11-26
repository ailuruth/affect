"""Critique of design-commutator-coupling.md: concrete mechanism exhibits on constructed signals (not evidence about people).
The design's own operators are read verbatim from ../design-cc/checks.py at run time (signal generators, echo, the two-stage
coherent limiter, the independent metric, the commutator tree); only the inputs are new. Two textual hooks are added to
record the limiter's per-band factors and its broadband factor (no change to what it computes).

A1 calibration on the expressive path: x~ = ref + (x - b)*sigma_ref/max(sigma_id, 0.25 sigma_ref) feeds the echo and is the
   limiter's reference. A reserved partner (sigma_id = 0.25 sigma_ref): exact raw copy, and the echo, judged on his RAW channel.
A2 his word-event counts are level-1 own-path inputs held factual in S0: any route through them has delta == 0 exactly.
A3 slow following beyond the scanned lags: a 90-s and a 5-min delayed copy, and a 5-min low-pass follow, 2 h.
A4 zero and small ceilings: an independent (non-copy) partner-caused route at c = 0, 0.10, 0.35; an away route at c = 0.
A5 attenuate-only and the echo's share: per-band factors make |out| > |in| and sign flips; the echo when a same-channel
   following route shares the budget.
A6 the divisive floor eps_j = nu_a nu_x 2^j against bounded slow expression: rho at slow scales for a maximal-area pair.
Run:  python3 -I cc_routes.py     (numpy, scipy; about 6-8 min)
"""
import os
import time
import numpy as np
from scipy.signal import lfilter

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "design-cc", "checks.py")).read()
FS = 30.0
ns = {"np": np, "lfilter": lfilter, "FS": FS, "NULL_OFFSET": 300.0, "ALPHAS": [], "BBF": []}
exec(SRC[SRC.index("def split_commutators"):SRC.index("out = {}")], ns)
seg = SRC[SRC.index("def expr_signal"):SRC.index('print("C6')]
seg = seg.replace("        y += alpha * bd\n", "        y += alpha * bd\n        ALPHAS.append(alpha)\n")
seg = seg.replace("    return a * y\n", "    BBF.append(a)\n    return a * y\n")
exec(seg, ns)
g = ns
expr_signal, delay, lowpass, echo = g["expr_signal"], g["delay"], g["lowpass"], g["echo"]
atrous, limiter, broadband_cap, prm = g["atrous"], g["limiter"], g["broadband_cap"], g["pooled_regression_max"]
rho_nodes = g["rho_nodes"]


def full(d, ref, c):
    g["ALPHAS"].clear(); g["BBF"].clear()
    y = broadband_cap(limiter(d, ref, c), ref, c)
    return y, list(g["ALPHAS"]), g["BBF"][-1]


def apply_factors(e, alphas, bbf, J=11):
    De, Re = atrous(e, J)
    return bbf * sum(a * b for a, b in zip(alphas, De + [Re]))


def bm_slope(y, p, W, lags):
    """block-mean slope of y on p(t - lag), best lag (slow content; the design's metric removes window means)."""
    w = int(W * FS); best = (0.0, 0)
    for L in lags:
        pl = delay(p, L * FS); n = (len(y) // w) * w
        Y = y[:n].reshape(-1, w).mean(1); P = pl[:n].reshape(-1, w).mean(1)
        Y = Y - Y.mean(); P = P - P.mean()
        b = (Y @ P) / (P @ P)
        if abs(b) > abs(best[0]): best = (b, L)
    return best


rng = np.random.default_rng(2026)
n20 = int(20 * 60 * FS)

# ------------------------------------------------------------------ A1
print("A1  reserved partner: raw smile = 0.25 x the C6 partner (sigma_id = 0.25 sigma_ref, the x4 floor); x~ = ref + 4 (x - b)")
p_raw = 0.25 * expr_signal(rng, n20)
b_read = np.median(p_raw)
xt = 0.3 + 4.0 * (p_raw - b_read)                     # calibrated, the design's x~ (ref 0.3)
for lab, d in [("exact raw copy, lag 0.9 s", delay(p_raw, 0.9 * FS) - p_raw.mean()),
               ("exact raw copy, lag 0", p_raw - p_raw.mean()),
               ("frozen echo on x~ (G 0.224, 0.9 s)", echo(xt))]:
    y1, _, _ = full(d, xt, 0.35)                      # inner cap c_LP, then outer c_tot 0.55 (as y = s0 + Lim_tot(Lim_c(.)))
    y2, _, _ = full(y1, xt, 0.55)
    print(f"     {lab:36s} vs x~: before {prm(d, xt)[0]:+.3f} after {prm(y2, xt)[0]:+.3f} | vs his RAW channel: before "
          f"{prm(d, p_raw)[0]:+.3f} after {prm(y2, p_raw)[0]:+.3f}; rms out/in {np.std(y2)/np.std(d):.2f}; "
          f"peak {d.max():.3f} (his raw peak {p_raw.max() - b_read:.3f} above his baseline)")

# ------------------------------------------------------------------ A2
print("A2  his utterance-onset counts enter u_j (level 1) and are held factual in S0: a route through them")
n2 = int(60 * 60 * FS)
rate = np.repeat(rng.uniform(1.5, 4.5, size=n2 // int(120 * FS) + 1), int(120 * FS))[:n2]   # his syllable-rate regime, 2-min stretches
onsets = (rng.random(n2) < rate / FS / 3.0).astype(float)                                      # his word onsets
zf = lowpass(onsets, 20.0) * FS * 3.0                    # a leaky integrator of his onset counts (one CDE coordinate)
gain = 0.5                                               # a readout of that coordinate onto the agent's own rate target
own_rate_f = 3.0 + gain * (zf - zf.mean())               # factual
own_rate_s0 = 3.0 + gain * (zf - zf.mean())              # S0: same own inputs, same word events -> identical
delta = own_rate_f - own_rate_s0
yl, _, _ = full(delta, rate, 0.10)
print(f"     delta = factual - S0: max |delta| {np.abs(delta).max():.1e}; limiter output max {np.abs(yl).max():.1e}; rendered rate "
      f"slope on his rate (2-min means) {bm_slope(own_rate_f, rate, 120, [0, 20, 40, 60])[0]:+.2f}  (c_tot rate 0.10)")

# ------------------------------------------------------------------ A3
print("A3  slow following, 2 h: partner = C6 smile bursts + session-scale drift (OU tau 10 min, SD 0.08); smile ceiling 0.35")
n3 = int(2 * 3600 * FS)
pb = expr_signal(np.random.default_rng(31), n3, drift=0.0)
ou = lowpass(np.random.default_rng(32).normal(size=n3), 600.0); ou = 0.08 * ou / ou.std()
p3 = np.clip(pb + ou + 0.2, 0, 1)
for lab, d in [("copy, lag 90 s", delay(p3, 90 * FS) - p3.mean()),
               ("copy, lag 5 min", delay(p3, 300 * FS) - p3.mean()),
               ("low-pass follow, tau 5 min (unit DC)", lowpass(p3 - p3.mean(), 300.0))]:
    y, _, _ = full(d, p3, 0.35)
    k = int(30 * 60 * FS)                                  # score the last 90 min
    a0 = prm(d[k:], p3[k:])[0]; a1 = prm(y[k:], p3[k:])[0]
    s0 = bm_slope(d[k:], p3[k:], 60, range(0, 601, 30)); s1 = bm_slope(y[k:], p3[k:], 60, range(0, 601, 30))
    s5 = bm_slope(y[k:], p3[k:], 300, range(0, 601, 60))
    print(f"     {lab:38s} design metric (<=60 s lags, window-centred) before {a0:+.3f} after {a1:+.3f} | 1-min block means, "
          f"lags 0-10 min: before {s0[0]:+.3f} after {s1[0]:+.3f} (lag {s1[1]} s); 5-min means after {s5[0]:+.3f} (lag {s5[1]} s); "
          f"rms out/in {np.std(y[k:])/np.std(d[k:]):.2f}")

# ------------------------------------------------------------------ A4
print("A4  an independent (non-copy) partner-caused route (C6's last row) and an away route, by ceiling")
p4 = expr_signal(np.random.default_rng(41), n20)
ind = expr_signal(np.random.default_rng(99), n20, 6, 0.3) - 0.1
away = -0.3 * (delay(p4, 1.0 * FS) - p4.mean())
for c in (0.0, 0.03, 0.10, 0.35):
    y, _, _ = full(ind, p4, c)
    k = int(5 * 60 * FS)
    print(f"     c = {c:.2f}: independent route rms out/in {np.std(y[k:])/np.std(ind[k:]):.2f} (corr with input "
          f"{np.corrcoef(y[k:], ind[k:])[0,1]:+.2f})", end="")
    if c == 0.0:
        ya, _, _ = full(away, p4, c)
        print(f"; away route (-0.3 x his, lag 1 s) rms out/in {np.std(ya[k:])/np.std(away[k:]):.2f}")
    else:
        print()

# ------------------------------------------------------------------ A5
print("A5  attenuate-only? and the echo's share of the same-channel budget (smile, c 0.35)")
e = echo(p4)
for lab, f in [("echo alone", 0 * p4), ("echo + following route 0.5 x his at 1.0 s", 0.5 * (delay(p4, 1.0 * FS) - p4.mean())),
               ("echo + following route 0.3 x his at 1.5 s", 0.3 * (delay(p4, 1.5 * FS) - p4.mean()))]:
    d = e + f
    y, al, bbf = full(d, p4, 0.35)
    ye = apply_factors(e, al, bbf)
    k = int(5 * 60 * FS); act = np.abs(d[k:]) > 0.01
    grow = np.mean(np.abs(y[k:])[act] > np.abs(d[k:])[act] + 1e-3); flip = np.mean((y[k:] * d[k:])[act] < -1e-6)
    made = np.mean(np.abs(y[k:])[~act] > 0.01) if (~act).any() else 0.0
    print(f"     {lab:42s} frames with |out| > |in|: {grow:.3f}, sign flips: {flip:.3f}, output where input < 0.01: {made:.3f}; "
          f"echo part: peak {e.max():.3f} -> {ye.max():.3f}, rms x{np.std(ye[k:])/np.std(e[k:]):.2f}")

# ------------------------------------------------------------------ A6
print("A6  rho at the matched scale for a maximal-area pair (quarter-period lead, amplitude 0.1 each, white tracker noise SD 0.005)")
nu = 0.005
for j in (6, 9, 12, 14, 16, 18, 20):
    T = 2 ** j; nn = 8 * T + 1
    t = np.arange(nn)
    w = 2 * np.pi / (2 * T)
    r6 = np.random.default_rng(j)
    a = 0.1 * np.sin(w * t) + nu * r6.normal(size=nn); x = 0.1 * np.sin(w * t - np.pi / 2) + nu * r6.normal(size=nn)
    r_design = rho_nodes(a, x, j, nu * nu * 2 ** j)
    r_flat = rho_nodes(a, x, j, 2 * nu * nu)
    print(f"     j {j:>2} (node {T / FS / 60:8.1f} min): mean rho with eps = nu^2 2^j: {r_design.mean():+.3f}; with a white-noise "
          f"floor 2 nu^2: {r_flat.mean():+.3f}")
print(f"done in {time.time() - T0:.0f} s")
