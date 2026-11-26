"""Algebra checks for design-cayley-ledger.md, revision 2 (H1-H8).

Checks of the design's own inequalities on hand-made instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Run:  python3 -I checks.py      (numpy, scipy; about a minute)
"""
import numpy as np
from scipy.optimize import linprog, minimize_scalar

rng = np.random.default_rng(7)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def disc(gamma, kappa):
    """In-phase cap, anti-phase cap, centre, radius of the wrap of a gamma-contraction."""
    b = 2 * gamma / (1 + gamma)
    a = 2 * gamma / (1 - gamma)
    m = -2 * gamma ** 2 / (1 - gamma ** 2)
    r = 2 * gamma / (1 - gamma ** 2)
    return b * kappa, -a * kappa, m * kappa, r * kappa


KAPPA, KLAT, GF, GS, GAMMA = 0.30, 0.05, 0.45, 0.20, 0.50
TAU_I, TAU_O, TAU_L, TAU_K, TAU_P = 4.0, 4.0, 60.0, 1200.0, 15.0
A_PORT = 0.10

# ------------------------------------------------------------------ H1 constants and band split
print("=== H1: constants, band split, combined gain")
fs = 30.0
w = np.linspace(1e-6, np.pi, 20000)
z = np.exp(1j * w)
def lp(tau, fs):
    a = 1 - np.exp(-1 / (tau * fs))
    return a / (1 - (1 - a) / z)
def hp(tau, fs):
    return 1 - lp(tau, fs)
HPi, LPl = hp(TAU_I, fs), lp(TAU_L, fs)
pc = np.max(np.abs(HPi) ** 2 + np.abs(LPl) ** 2)
report("H1a power complementarity |HP_4s|^2+|LP_60s|^2 <= 1", pc <= 1 + 1e-9, f"max = {pc:.4f}")
gmax = np.max(GF * np.abs(HPi) * np.abs(hp(TAU_O, fs)) + GS * np.abs(LPl))
geff = np.sqrt(GF ** 2 + GS ** 2)
report("H1b combined S gain <= sqrt(gf^2+gs^2) <= gamma", gmax <= geff + 1e-9 and geff <= GAMMA,
       f"max_w |S| = {gmax:.4f}, sqrt bound {geff:.4f}, gamma {GAMMA}")
for name, g, k in [("fast", GF, KAPPA), ("slow/DC", GS, KAPPA), ("overall", geff, KAPPA),
                   ("lateral fast", GF, KLAT), ("lateral slow", GS, KLAT)]:
    b, a, m, r = disc(g, k)
    print(f"   {name:13s} gamma {g:.3f} kappa {k:.2f}: in-phase <= {b:.3f}, anti >= {a:.3f}, "
          f"centre {m:.3f}, radius {r:.3f}")
cross = 2 * np.sqrt(KLAT * KAPPA) * GF / (1 - GF)
report("H1c lateral<-symmetric cross route per pair (fast) <= 0.20", cross <= 0.2005, f"{cross:.3f}")


# ------------------------------------------------------------------ wrap simulator
class Wrap:
    """Scalar banded wrap: s = HP_o(gf*sf*Delay(HP_i w)) + gs*ss*LP_k(LP_L w) (+ port), y = 2 sqrt(k) s.
    s_t depends on w_{<t} (strictly causal)."""
    def __init__(self, fs, kappa, gf, sf, gs, ss, lag=0.45, tau_k=TAU_K, slow_modes=None):
        self.fs, self.k = fs, kappa
        self.gf, self.sf, self.gs, self.ss = gf, sf, gs, ss
        self.ai = 1 - np.exp(-1 / (TAU_I * fs)); self.ao = 1 - np.exp(-1 / (TAU_O * fs))
        self.aL = 1 - np.exp(-1 / (TAU_L * fs)); self.ak = 1 - np.exp(-1 / (tau_k * fs))
        self.nl = max(1, int(round(lag * fs)))
        self.slow_modes = slow_modes

    def run(self, u, port=None, record_w=False):
        T = len(u); sk = np.sqrt(self.k)
        y = np.zeros(T); ws = np.zeros(T); ss_ = np.zeros(T)
        lpi = lpo = xL = xk = 0.0
        buf = np.zeros(self.nl); bi = 0
        sf_out = ss_out = 0.0
        for t in range(T):
            s = sf_out + ss_out
            wt = sk * u[t] - s
            y[t] = 2 * sk * s
            ws[t] = wt; ss_[t] = s
            hpi = wt - lpi; lpi += self.ai * (wt - lpi)
            d = buf[bi]; buf[bi] = hpi; bi = (bi + 1) % self.nl
            f = self.gf * self.sf * d
            hpo = f - lpo; lpo += self.ao * (f - lpo)
            sf_out = hpo
            xL += self.aL * (wt - xL); xk += self.ak * (xL - xk)
            ss_out = self.gs * self.ss * xk
        if port is not None:
            y = y + port
        return (y, ws, ss_) if record_w else y


def means(x, n):
    m = len(x) // n
    return x[: m * n].reshape(m, n).mean(1)


def slope(x, y):
    x = x - x.mean(); y = y - y.mean()
    return float(x @ y / (x @ x))


def partner_held(T, fs, seg_min=10.0, burst_every=15.0):
    """Held levels in [0,1] changing every ~seg_min (exponential), plus smile transients and noise."""
    u = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(seg_min * 60 * fs)) + int(60 * fs)
        u[t:t + L] = rng.uniform(0, 1); t += L
    lev = u.copy()
    bursts = np.zeros(T)
    for c in np.arange(0, T, int(burst_every * fs)):
        c2 = c + int(rng.uniform(0, burst_every * fs))
        bursts[c2:c2 + int(1.5 * fs)] += 0.25
    noise = np.convolve(rng.normal(0, 0.03, T), np.ones(5) / 5, "same")
    return np.clip(lev + bursts + noise, 0, 1.2), lev


# ------------------------------------------------------------------ H2 knowing vs moving at DC
print("=== H2: a slow state that knows the held face cannot copy it (DC through the wrap)")
fs2 = 2.0; T2 = int(48 * 3600 * fs2)
u, lev = partner_held(T2, fs2, seg_min=60.0)
n1 = int(60 * fs2)
res = {}
for ss in (+1.0, -1.0):
    wr = Wrap(fs2, KAPPA, GF, +1.0, GS, ss, tau_k=300.0)
    y, ws, s = wr.run(u, record_w=True)
    # knowing: the core knows its own s, so v = w + s; slow knowledge = LP_k(LP_L(w + s)) / sqrt(k)
    v = ws + s
    kn = np.zeros(T2); xL = xk = 0.0
    for t in range(T2):
        xL += wr.aL * (v[t] - xL); kn[t] = xL
    um, ym, km = means(u, n1), means(y, n1), means(kn / np.sqrt(KAPPA), n1)
    res[ss] = (slope(um, ym), np.corrcoef(km[10:], um[10:])[0, 1])
b_s, a_s, _, _ = disc(GS, KAPPA)
report("H2a knowing: slow state tracks the held level", res[1][1] > 0.9,
       f"corr(1-min knowledge, partner 1-min mean) = {res[1][1]:.3f}")
report("H2b moving, copy-seeking slow readout: 1-min-mean slope <= slow in-phase cap + edges",
       res[1][0] <= b_s + 0.02 and res[1][0] > 0.6 * b_s, f"slope {res[1][0]:+.3f} (cap {b_s:.3f})")
report("H2c moving, opposite-sign slow readout reaches the anti side", a_s - 0.02 <= res[-1][0] < 0.6 * a_s,
       f"slope {res[-1][0]:+.3f} (anti cap {a_s:.3f})")
y_direct = np.zeros(T2); xL = xk = 0.0
aL = 1 - np.exp(-1 / (TAU_L * fs2)); ak = 1 - np.exp(-1 / (300.0 * fs2))
for t in range(T2):
    xL += aL * (u[t] - xL); xk += ak * (xL - xk); y_direct[t] = xk
print(f"   same knowledge read straight to the face (no wrap): 1-min slope {slope(um, means(y_direct, n1)):+.3f}")

# ------------------------------------------------------------------ H3 learnability from clean signals
print("=== H3: context-set, sign-flippable fast strengths learned from clean u; cone holds for every value")
fs3 = 30.0; T3 = int(600 * fs3)
def fast_u(T):
    x = np.convolve(rng.normal(size=T), np.hanning(int(0.8 * fs3)), "same")
    return 0.15 * x / x.std() + 0.3
def fast_gain(y, u, lag):
    du = u - np.convolve(u, np.ones(int(4 * fs3)) / (4 * fs3), "same")
    n = int(lag * fs3)
    return np.dot(y[n:], du[:-n]) / np.dot(du[:-n], du[:-n])
uc = {c: fast_u(T3) for c in ("friendly", "opposed", "copy-target")}
targets = {"friendly": +0.15, "opposed": -0.40, "copy-target": +1.00}
caps = disc(GF, KAPPA)
def run2(uu, p):
    g1, g2 = np.tanh(p[0]), np.tanh(p[1])
    tot = abs(g1) + abs(g2)
    if tot > 1: g1, g2 = g1 / tot, g2 / tot          # |g1|+|g2| <= 1 keeps the block a GF-contraction
    T = len(uu); sk = np.sqrt(KAPPA); y = np.zeros(T)
    ai = 1 - np.exp(-1 / (TAU_I * fs3)); ao = ai
    n1_, n2_ = int(0.45 * fs3), int(0.9 * fs3)
    buf = np.zeros(n2_); bi = 0; lpi = lpo = 0.0; so = 0.0
    for t in range(T):
        wt = sk * uu[t] - so; y[t] = 2 * sk * so
        hpi = wt - lpi; lpi += ai * (wt - lpi)
        d1 = buf[(bi - n1_) % n2_]; d2 = buf[bi]; buf[bi] = hpi; bi = (bi + 1) % n2_
        f = GF * (g1 * d1 + g2 * d2)
        hpo = f - lpo; lpo += ao * (f - lpo); so = hpo
    return y
from scipy.optimize import minimize
for c, beta in targets.items():
    uu = uc[c]
    du = uu - np.convolve(uu, np.ones(int(4 * fs3)) / (4 * fs3), "same")
    nl = int(0.45 * fs3)
    ystar = np.zeros(T3); ystar[nl:] = beta * du[:-nl]
    loss = lambda p: np.mean((run2(uu, p) - ystar) ** 2)
    r = minimize(loss, x0=[0.0, 0.0], method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-9, "maxiter": 200})
    y = run2(uu, r.x)
    g = fast_gain(y, uu, 0.45)
    dd = du[nl:] @ du[:-nl] / (du @ du)              # partner's own autocorrelation at 0.45 s
    hi, lo = caps[3] + caps[2] * dd, -caps[3] + caps[2] * dd
    reach = min(abs(beta), hi if beta > 0 else -lo)
    ok = (lo - 0.02) <= g <= hi + 0.02 and np.sign(g) == np.sign(beta) and (abs(g) >= 0.6 * reach or beta > hi)
    report(f"H3 {c:11s} target {beta:+.2f}", ok,
           f"learned lag-0.45 s gain {g:+.3f}; lag bound [{lo:+.3f}, {hi:+.3f}] (rho_u = {dd:.2f})")
# the same learner trained on the r1 release (sigma 7.1 noise on a 2-Hz stream) learns nothing
uu = uc["friendly"]; du = uu - np.convolve(uu, np.ones(int(4 * fs3)) / (4 * fs3), "same")
noisy = uu + np.repeat(rng.normal(0, 7.1, T3 // 15 + 1), 15)[:T3]
ystar = np.zeros(T3); ystar[13:] = 0.15 * du[:-13]
X = noisy[:-13] - noisy[:-13].mean()
print(f"   r1-style noisy release, best linear coefficient: {np.dot(X, ystar[13:]) / np.dot(X, X):+.5f} (target +0.15)")

# ------------------------------------------------------------------ H4 lateral channels reflected, kappa_lat
print("=== H4: head yaw / roll / horizontal gaze reflected before the cone, kappa_lat = 0.05")
from scipy.signal import butter, filtfilt
bb, aa = butter(2, [0.2 / 15, 1.1 / 15], "band")
uy = filtfilt(bb, aa, rng.normal(size=int(600 * fs3))); uy = 0.15 * uy / uy.std()
refl = -uy                               # reflection into the agent's mirror frame
out = {}
for sf, name in [(+1.0, "mirror-seeking"), (-1.0, "anatomical-seeking")]:
    wr = Wrap(fs3, KLAT, GF, sf, 0.0, 0.0, lag=1 / fs3)
    ya = wr.run(refl)
    T = len(uy)
    gm = max(np.dot(ya[l:], (-uy)[:T - l]) / np.dot(uy[:T - l], uy[:T - l]) for l in range(31))
    ga = max(np.dot(ya[l:], uy[:T - l]) / np.dot(uy[:T - l], uy[:T - l]) for l in range(31))
    out[name] = (gm, ga)
    print(f"   {name:18s}: mirror-copy gain {gm:+.3f}, anatomical-copy gain {ga:+.3f}")
bl, al_, _, _ = disc(GF, KLAT)
report("H4 both handednesses of lateral copy bounded", max(out["mirror-seeking"][0], out["anatomical-seeking"][1]) <= -al_ + 0.01,
       f"max {max(out['mirror-seeking'][0], out['anatomical-seeking'][1]):.3f} (r1 critic: 0.58); caps mirror {bl:.3f}, anatomical {-al_:.3f}")

# ------------------------------------------------------------------ H5 rate dial: why the slow block reads only LP(w)
print("=== H5: event-rate dial. Partner smile bursts at varying rate, no held level")
fs5 = 10.0; ep = int(600 * fs5); E = 36
ub = np.zeros(ep * E)
for e in range(E):
    rate = rng.uniform(1 / 30, 1 / 4)
    t = e * ep
    while t < (e + 1) * ep:
        t += int(rng.exponential(1 / rate) * fs5) + 1
        ub[t:min(t + int(1.5 * fs5), (e + 1) * ep)] = 0.8
n1 = int(60 * fs5)
y_ok = Wrap(fs5, KAPPA, GF, +1.0, GS, +1.0).run(ub)
# forbidden variant: slow output fed by rectified FAST features (still a gs-contraction in l2)
def demod(u):
    T = len(u); sk = np.sqrt(KAPPA); y = np.zeros(T)
    ai = 1 - np.exp(-1 / (TAU_I * fs5)); ak = 1 - np.exp(-1 / (300 * fs5))
    lpi = xk = 0.0; s = 0.0
    for t in range(T):
        wt = sk * u[t] - s; y[t] = 2 * sk * s
        hpi = wt - lpi; lpi += ai * (wt - lpi)
        xk += ak * (abs(hpi) - xk); s = GF * xk
    return y
y_bad = demod(ub)
um = means(ub, n1)
s_ok, s_bad = slope(um, means(y_ok, n1)), slope(um, means(y_bad, n1))
report("H5 slow block on LP(w) only: 1-min-mean slope <= slow cap + edges", s_ok <= b_s + 0.03,
       f"slope {s_ok:+.3f}; forbidden fast->slow demodulation at the fast gain: {s_bad:+.3f}")

# ------------------------------------------------------------------ H6 Omega port: zero DC
print("=== H6: own-words port. Adversary: Claude's words track the partner's held level exactly")
fs6 = 1.0; T6 = int(6 * 3600 * fs6)
lev6 = np.repeat(rng.uniform(0, 1, T6 // 600 + 1), 600)[:T6]
e = np.repeat(lev6[::8], 8)[:T6]                    # per-turn (8 s) word appraisal = held level
ap = 1 - np.exp(-1 / (TAU_P * fs6)); lpp = 0.0; port = np.zeros(T6)
for t in range(T6):
    port[t] = A_PORT * (e[t] - lpp); lpp += ap * (e[t] - lpp)
for win, lab in [(60, "1-min"), (600, "10-min")]:
    sl = slope(means(lev6, win), means(port, win))
    print(f"   {lab} means: port contribution slope {sl:+.4f}")
bound = 2 * TAU_P * A_PORT / 60
mx = np.max(np.abs(means(port, 60)))
report("H6 port 1-min-mean effect <= 2 tau a / T", mx <= bound + 1e-9, f"max |1-min mean| {mx:.4f}, bound {bound:.3f}")

# ------------------------------------------------------------------ H7 worst-case transient held copy (slow disc, LP)
print("=== H7: worst held-level response over a window after onset, any operator in the slow disc")
dt = 30.0; N = 240                                  # 30-s steps, 2 h of memory
_, _, mS, rS = disc(GS, KAPPA)
om = np.linspace(0, np.pi, 300); ph = np.linspace(0, 2 * np.pi, 16, endpoint=False)
A_ub = []; b_ub = []
for o in om:
    e_ = np.exp(-1j * o * np.arange(N))
    for p in ph:                                     # Re((H - m) e^{-jp}) <= r
        A_ub.append(np.real(e_ * np.exp(-1j * p))); b_ub.append(rS + mS * np.cos(p))
A_ub = np.array(A_ub); b_ub = np.array(b_ub)
for t_on in (2, 10, 60, 120):                       # window centre after onset, in 30-s steps
    i0 = t_on
    c = -np.array([np.mean([1.0 if k <= j else 0.0 for j in (i0, i0 + 1)]) for k in range(N)])
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)] * N, method="highs")
    print(f"   1-min mean at {t_on * dt / 60:5.1f} min after onset: worst in-phase {-r.fun:+.3f} "
          f"(steady-state cap {disc(GS, KAPPA)[0]:.3f}, slow |H| cap {-disc(GS, KAPPA)[1]:.3f})")
    last = -r.fun
print("   (l2 disc alone: transient 1-min means can exceed the steady-state cap; r2 therefore adds an l-inf bound)")
# with the l-infinity structure: open-loop slow block sigma with ||h||_1 <= GS (positive filters, inf-Lipschitz maps)
def closed_step(h, n=480):
    # closed loop s = sigma * (v - s) at 30-s steps, strictly causal, unit step v = sqrt(k)
    s = np.zeros(n); w = np.zeros(n); sk = np.sqrt(KAPPA)
    for t in range(n):
        s[t] = sum(h[j] * w[t - 1 - j] for j in range(min(len(h), t)))
        w[t] = sk - s[t]
    return 2 * sk * s / 1.0
worst = 0.0
for trial in range(300):
    L = rng.integers(2, 40)
    h = rng.normal(size=L) * (rng.uniform(size=L) < 0.5)
    if not h.any(): continue
    h = GS * h / np.abs(h).sum()
    y = closed_step(h, 200)
    worst = max(worst, np.max(np.convolve(y, [0.5, 0.5], "valid")))
def adv(p):
    h = np.array(p); h = GS * h / max(np.abs(h).sum(), 1e-9)
    y = closed_step(h, 120); return -np.max(np.convolve(y, [0.5, 0.5], "valid"))
for k in range(20):
    r = minimize(adv, rng.normal(size=8), method="Nelder-Mead", options={"maxiter": 400})
    worst = max(worst, -r.fun)
capinf = 2 * KAPPA * GS / (1 - GS)
report("H7 with ||sigma||_1 <= gs: worst 1-min mean of the held response <= 2 k gs/(1-gs) at every time",
       worst <= capinf + 1e-6, f"worst found {worst:+.3f}, bound {capinf:.3f}")

# ------------------------------------------------------------------ H8 totals
print("=== H8: per-channel totals")
bf, af, mf, rf = disc(GF, KAPPA); bo = disc(geff, KAPPA)[0]
print(f"   zero-lag in-phase, any band: <= {bo:.3f} (fast alone {bf:.3f}); port RMS <= {A_PORT}")
print(f"   held (steady state): <= {b_s:.3f} in phase, >= {a_s:.3f}; port 0")
print(f"   1-min means: <= {b_s:.3f} + port {bound:.3f} + fast edges ~0.01 = {b_s + bound + 0.01:.3f}")
print(f"   10-min means: <= {b_s:.3f} + port {2 * TAU_P * A_PORT / 600:.4f}")
print(f"   lagged copy, broadband, fast: <= {rf + mf:.3f}+|m|...: radius {rf:.3f}; any-signal fast {-af:.3f}")
print(f"\n{sum(OK)}/{len(OK)} checks pass")
