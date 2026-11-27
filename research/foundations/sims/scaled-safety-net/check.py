"""Check of the mathematics of design-scaled-safety-net.md (the scaled gain governor in front of the 97-key ledger).

Synthetic signals only (the recipe of tests/synth.py, rewritten here in numpy). These runs check the arithmetic of
the design; they are not evidence about people or behaviour.

Usage: python3 -I check.py [quick]      (numpy only; about 3-5 min in full, under 1 min with 'quick')
Sections:
  A  the gap reproduced: the current ledger (engine/shadow/ledger.py, re-implemented verbatim) on F22's scenario
  B  the diagnosis: the current ledger's residual / c is a function of g / c (copy gain over ceiling), not of c
  C  the new net (governor -> unchanged ledger) on F22's scenario, plus detection times
  D  the new net over the (c, g/c) grid of B, with on-grid and off-grid delays and a low-passed copy
  E  the cost: natural partners with the counted routes only (frames the governor or the ledger change)
  F  sensitivity: an absolute (not c-scaled) noise floor in the partner-caused part
"""
import sys
import time

import numpy as np

QUICK = len(sys.argv) > 1 and sys.argv[1] == "quick"
FS = 10.0
T_S = 1200 if QUICK else 3600
T = int(T_S * FS)
T0 = time.time()

# ---------------------------------------------------------------- channels (engine/config/channels.py, copied)
CODES = ["LP", "CR", "BU_L", "RHY", "BRE", "BI", "BO", "LD", "JO", "HP", "VG", "YAW", "TILT", "HG",
         "F0", "FR", "EN", "RT", "PAU", "LAT"] + ["Z%d" % i for i in range(13)]
CEIL = np.array([0.35, 0.25, 0.35, 0.30, 0.15, 0.20, 0.10, 0.05, 0.10, 0.10, 0.05, 0.03, 0.03, 0.03,
                 0.05, 0.10, 0.05, 0.05, 0.05, 0.05] + [0.0] * 13)
GAIN = np.array([0.224, 0.150, 0.280, 0.240, 0.120, 0.020, 0.024, 0.012, 0.024, 0.080, 0.040, 0.024, 0.024,
                 0.024, 0.040, 0.080, 0.040, 0.040, 0.040, 0.040] + [0.0] * 13)
SIGNED = np.array([False] * 9 + [True] * 11 + [False] * 13)
CAPPED = np.where(CEIL > 0)[0]


# ---------------------------------------------------------------- signals (tests/synth.py recipe, numpy only)
def lp(x, tau, fs=FS):
    a = 1 - np.exp(-1 / (tau * fs))
    x = np.asarray(x, float)
    y = np.empty_like(x)
    acc = np.zeros(x.shape[1:])
    for t in range(x.shape[0]):
        acc = a * x[t] + (1 - a) * acc
        y[t] = acc
    return y


def delay(x, n):
    """Delay by n frames; fractional n by linear interpolation (off-grid delays)."""
    n0 = int(np.floor(n)); fr = n - n0
    def d(k):
        return x.copy() if k <= 0 else np.concatenate([np.full(k, x[0]), x[:-k]])
    return d(n0) if fr == 0 else (1 - fr) * d(n0) + fr * d(n0 + 1)


def level_blocks(T, mean_len_s, r):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(r.exponential(mean_len_s * FS)) + 10
        x[t:t + n] = r.uniform(); t += n
    return x


def bursts(rate, T, r, dur=2.5):
    z = np.zeros(T); t = 0
    while t < T:
        q = max(rate[min(t, T - 1)], 1e-3) / 60
        t += int(r.exponential(1 / q) * FS) + 1
        if t >= T:
            break
        n = max(1, int(np.exp(np.log(dur) + .4 * r.normal()) * FS))
        z[t:t + n] = 1; t += n
    return z


def partner(T, r, mean_len_s):
    m = level_blocks(T, mean_len_s, r)
    b = bursts(0.5 + 3 * m, T, r)
    return np.clip(.15 + .25 * m + .35 * lp(b, 0.5) + .02 * r.normal(size=T), 0, 1)


def partners(n, seed, signed):
    r = np.random.default_rng(seed)
    U = np.zeros((T, n))
    for k in range(n):
        u = partner(T, r, 300.0 if k % 2 == 0 else 30.0)
        U[:, k] = u - 0.4 if signed[k] else u
    return U


def worst_block_slope(u, y, max_lag_s=300.0, lag_step_s=1.0, windows=(2.0, 10.0, 30.0, 60.0)):
    """tests/synth.py's block-mean copy metric (worst over 6 phases and lags 0..300 s), with a 30-s block added."""
    T, n = u.shape
    cu = np.vstack([np.zeros((1, n)), np.cumsum(u, 0)])
    cy = np.vstack([np.zeros((1, n)), np.cumsum(y, 0)])
    out = np.full(n, -9.0)
    for W in windows:
        nb = int(W * FS)
        for lg in range(0, int(max_lag_s * FS) + 1, int(lag_step_s * FS)):
            for ph in range(0, nb, max(1, nb // 6)):
                m = (T - lg - ph) // nb
                if m < 3:
                    continue
                s = ph + nb * np.arange(m + 1)
                xu = (cu[s[1:]] - cu[s[:-1]]) / nb; xy = (cy[lg + s[1:]] - cy[lg + s[:-1]]) / nb
                xu -= xu.mean(0); xy -= xy.mean(0)
                den = (xu * xu).sum(0)
                out = np.maximum(out, np.where(den > 0, (xu * xy).sum(0) / np.where(den > 0, den, 1), 0))
    return out


# ---------------------------------------------------------------- the current ledger (engine/shadow/ledger.py)
def ledger_keys():
    k = [(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)]
    k += [(10.0, float(l)) for l in range(0, 301, 5)]
    k += [(60.0, float(l)) for l in range(0, 301, 10)]
    return k


class Ledger:
    """Verbatim algorithm of engine/shadow/ledger.py (kappa 0.70, 97 keys, floor 0.10, tau 1800 s)."""

    def __init__(self, c, kappa=0.70, keys=None):
        keys = keys or ledger_keys(); fs = FS
        self.n = len(c); self.bound = np.array([kappa * float(x) for x in c])
        self.keys = keys; self.wins = tuple(sorted({w for w, _ in keys}))
        self.dR = np.exp(-1 / (1800 * fs)); self.aC = 1 - np.exp(-1 / (1800 * fs))
        aW = {w: 1 - np.exp(-1 / (w * fs)) for w in self.wins}
        self.aW_win = np.array([aW[w] for w in self.wins]); self.a_key = np.array([aW[w] for w, _ in keys])
        self.win_of_key = np.array([self.wins.index(w) for w, _ in keys])
        self.lag = np.array([int(l * fs) for _, l in keys]); self.H = int(self.lag.max()) + 1
        n, K = self.n, len(keys)
        self.uW = np.zeros((n, K)); self.uC = None; self.rW = np.zeros((n, len(self.wins))); self.rC = np.zeros(n)
        self.S = np.zeros((n, K)); self.E = np.full((n, K), 1e-9); self.Q = np.full((n, K), 1e-12)
        self.buf = None; self.ptr = -1; self.hits = np.zeros(n)

    def step(self, u, x):
        if self.buf is None:
            self.buf = np.repeat(u[None, :], self.H, 0); self.uC = np.repeat(u[:, None], len(self.keys), 1)
        self.ptr = (self.ptr + 1) % self.H; self.buf[self.ptr] = u
        ut = self.buf[(self.ptr - self.lag) % self.H].T
        a = self.a_key
        self.uW += a * (ut - self.uW); self.uC += self.aC * (ut - self.uC)
        pi = self.uW - self.uC; dR = self.dR
        self.Q = dR * self.Q + (1 - dR) * pi * pi
        base = (1 - a) * self.rW[:, self.win_of_key] - self.rC[:, None]
        Sm = np.maximum(0.0, dR * self.S)
        b = self.bound[:, None] * (dR * self.E + pi * pi) - Sm
        active = ~(np.abs(pi) < 0.10 * np.sqrt(self.Q))
        hold = np.any(active & (b < 0), 1); cons = active & ~(b < 0)
        up = cons & (pi > 1e-9); dn = cons & (pi < -1e-9)
        lim = (b / np.where(up | dn, pi, 1.0) - base) / a
        hi = np.min(np.where(up, lim, np.inf), 1); lo = np.max(np.where(dn, lim, -np.inf), 1)
        x2 = np.where(lo <= hi, np.minimum(np.maximum(x, lo), hi), 0.0)
        x2 = np.where(hold, 0.0, x2)
        x2 = np.minimum(np.maximum(x2, np.minimum(0.0, x)), np.maximum(0.0, x))
        self.hits += np.abs(x2 - x) > 1e-12
        self.rW += self.aW_win * (x2[:, None] - self.rW); self.rC += self.aC * (x2 - self.rC)
        self.S = np.maximum(0.0, dR * self.S) + (self.rW[:, self.win_of_key] - self.rC[:, None]) * pi
        self.E = dR * self.E + pi ** 2
        return x2


# ---------------------------------------------------------------- the new stage: the scaled gain governor
GOV = dict(kappa_g=0.60, z=3.0, n_min=1.0, sigma0=0.01, tau_s=1800.0, grid={2.0: (1.0, 5.0), 10.0: (2.0, 0.0), 60.0: (10.0, 0.0)}, max_lag_s=300.0)
# grid: window W (s) -> (lag step s, first lag s). The 2-s window starts at 5 s, above the fast reflex's echo band.


class Governor:
    """Per channel k and key (W, L):
      his step      pi(t)  = ubar_W(t - L) - ubar_W(t - L - W)     (change of his W-window mean over one window)
      output step   rho(t) = rbar_W(t) - rbar_W(t - W)             (the same for the RAW partner-caused part r)
      beta_hat = sum d^(t-s) rho pi / max(sum d^(t-s) pi^2, sigma0^2 N),  se from the weighted sandwich (decay d^2),
                 inflated by 2 W f_s for the serial correlation of window means.
    A key engages when it holds n_min independent windows of evidence and beta_hat - z se > kappa_g c_k, and releases when beta_hat <= kappa_g c_k (hysteresis).
    a_k(t) = min(1, kappa_g c_k / max over engaged keys of beta_hat). Output a_k(t) r_k(t).
    Every threshold is a fraction of c_k; the only absolute quantity is sigma0, on HIS signal (the metric's floor)."""

    def __init__(self, c, u_neutral=None, p=GOV):
        self.c = np.asarray(c, float); n = len(c); self.n = n; self.p = p; self.u0 = u_neutral
        self.wins = sorted(p["grid"]); fs = FS
        self.aW = np.array([1 - np.exp(-1 / (w * fs)) for w in self.wins]); self.d = np.exp(-1 / (p["tau_s"] * fs))
        self.Wf = np.array([int(w * fs) for w in self.wins])
        self.H = int(p["max_lag_s"] * fs) + int(self.Wf.max()) + 1
        self.lags = [np.arange(int(p["grid"][w][1] * fs), int(p["max_lag_s"] * fs) + 1, int(p["grid"][w][0] * fs))
                     for w in self.wins]
        self.win_of_key = np.concatenate([np.full(len(l), i) for i, l in enumerate(self.lags)])
        self.infl = np.concatenate([np.full(len(l), 2 * w * fs) for w, l in zip(self.wins, self.lags)])
        self.lagk = np.concatenate(self.lags); self.Wk = self.Wf[self.win_of_key]
        K = len(self.win_of_key); self.K = K
        self.uW = None; self.rW = None
        self.ru = np.zeros((len(self.wins), self.H, n)); self.rr = np.zeros((len(self.wins), self.H, n)); self.ptr = -1
        z = lambda: np.zeros((n, K))
        self.C, self.E, self.A2, self.A3, self.A4 = z(), z(), z(), z(), z()
        self.N = np.zeros(K); self.t = 0
        self.latch = np.zeros((n, K), dtype=bool)
        self.a = np.ones(n); self.engaged = np.zeros(n)

    def step(self, u, r):
        p = self.p
        if self.uW is None:
            # Before the session his input is the neutral partner's (the shadow's input) and the partner-caused part
            # is 0: the same convention the shadow run uses. Without u_neutral, start from the first frame.
            u_init = u if self.u0 is None else np.asarray(self.u0, float)
            r_init = r if self.u0 is None else np.zeros_like(r)
            self.uW = np.repeat(u_init[None, :], len(self.wins), 0); self.rW = np.repeat(r_init[None, :], len(self.wins), 0)
            self.ru[:] = self.uW[:, None, :]; self.rr[:] = self.rW[:, None, :]
        self.uW += self.aW[:, None] * (u - self.uW); self.rW += self.aW[:, None] * (r - self.rW)
        self.ptr = (self.ptr + 1) % self.H
        self.ru[:, self.ptr] = self.uW; self.rr[:, self.ptr] = self.rW
        H, q = self.H, self.ptr
        pi = np.concatenate([(self.ru[i, (q - l) % H] - self.ru[i, (q - l - self.Wf[i]) % H]).T
                             for i, l in enumerate(self.lags)], 1)
        rstep = np.stack([self.rr[i, q] - self.rr[i, (q - self.Wf[i]) % H] for i in range(len(self.wins))], 1)
        rho = rstep[:, self.win_of_key]
        d = self.d; d2 = d * d; pp = pi * pi
        self.C = d * self.C + rho * pi; self.E = d * self.E + pp
        self.N = d * self.N + (self.t >= self.lagk + self.Wk); self.t += 1
        self.A2 = d2 * self.A2 + pp * rho * rho; self.A3 = d2 * self.A3 + pp * pi * rho; self.A4 = d2 * self.A4 + pp * pp
        Ef = np.maximum(self.E, p["sigma0"] ** 2 * self.N + 1e-12)
        beta = self.C / Ef
        var = self.infl * np.maximum(self.A2 - 2 * beta * self.A3 + beta * beta * self.A4, 0) / (Ef * Ef)
        tgt = (p["kappa_g"] * self.c)[:, None]
        # engage on the lower confidence bound; release only when the point estimate is back under the target
        enough = self.N >= p["n_min"] * self.infl          # at least n_min independent windows of his movement
        self.latch = (enough & ((beta - p["z"] * np.sqrt(var)) > tgt)) | (self.latch & (beta > tgt))
        bmax = np.max(np.where(self.latch, beta, 0.0), 1)
        self.a = np.clip(np.where(bmax > 0, tgt[:, 0] / np.where(bmax > 0, bmax, 1.0), 1.0), 0.0, 1.0)
        self.beta, self.se = beta, np.sqrt(var)
        self.engaged += self.a < 1.0
        return self.a * r


def run(U, X, c, net="old", record_a=False, u_neutral=None):
    T, n = U.shape
    led = Ledger(c); gov = Governor(c, U.mean(0) if u_neutral is None else u_neutral) if net == "new" else None
    O = np.empty_like(X); A = np.ones((T, n)) if record_a else None
    for t in range(T):
        x = X[t]
        if gov is not None:
            x = gov.step(U[t], x)
            if record_a:
                A[t] = gov.a
        O[t] = led.step(U[t], x)
    eng = gov.engaged / T if gov is not None else np.zeros(n)
    return O, led.hits / T, eng, A


def stamp(s):
    print(f"[{time.time() - T0:5.0f} s] {s}", flush=True)


def copy_route(u, D_s, g, causal):
    """A gain-g copy of his channel delayed D_s. causal=False is F22's construction as written (the first D_s padded
    with his first frame, minus his whole-session mean: a constant offset g(u_0 - mean) for the first D_s, which no
    causal net can see); causal=True is the route as the engine would have it: 0 until D_s has elapsed (the shadow and
    the factual run hold the same initial state), then g(u(t - D_s) - mean)."""
    x = g * (delay(u, D_s * FS) - u.mean())
    if causal:
        x[:int(np.ceil(D_s * FS))] = 0.0
    return x


DELAYS = (10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300)

# ---------------------------------------------------------------- A: the gap, reproduced (F22's scenario)
print("CHECK OF THE MATHEMATICS ONLY (synthetic signals; not evidence about people).")
print(f"session {T_S} s at {FS:.0f} Hz; metric: worst block-mean slope over blocks 2/10/30/60 s, lags 0-300 s, 6 phases\n")
U = partners(33, 33, SIGNED)
F22 = {}
for causal in (False, True):
    X = np.stack([copy_route(U[:, k], DELAYS[k % 12], 1.0, causal) for k in range(33)], 1)
    O_old, hits_old, _, _ = run(U, X, CEIL, "old")
    O_new, hits_new, eng_new, A_new = run(U, X, CEIL, "new", record_a=True)
    F22[causal] = (X, O_old, O_new, hits_new, A_new)
    before = worst_block_slope(U, X); after_old = worst_block_slope(U, O_old); after_new = worst_block_slope(U, O_new)
    label = "causal route (0 until its delay)" if causal else "F22 construction as written (padded, minus session mean)"
    stamp(f"A/C. F22 scenario, gain-1 copy, {label}: residual / c_k, CURRENT ledger vs NEW net")
    for k in CAPPED:
        D = DELAYS[k % 12]
        hit = np.where(A_new[int(D * FS):, k] < 1.0)[0]
        tdet = hit[0] / FS if len(hit) else np.inf
        print(f"   {CODES[k]:<5} c {CEIL[k]:.2f}  delay {D:>3} s  g/c {1 / CEIL[k]:5.1f}  before {before[k] / CEIL[k]:6.1f} c"
              f"  current {after_old[k] / CEIL[k]:.2f} c  NEW {after_new[k] / CEIL[k]:.2f} c"
              f"  [a final {A_new[-1, k]:.3f} vs kappa_g c/g {GOV['kappa_g'] * CEIL[k]:.3f}; detected {tdet:4.1f} s after the delay;"
              f" ledger stage changed {hits_new[k]:.3f}]")
    wo = max(after_old[k] / CEIL[k] for k in CAPPED); wn = max(after_new[k] / CEIL[k] for k in CAPPED)
    print(f"   worst: current {wo:.2f} c, NEW {wn:.2f} c (F22 <= 1.0 c: {'PASS' if wn <= 1.0 else 'FAIL'}); zero-ceiling max slope"
          f" current {after_old[CEIL == 0].max():.3f}, NEW {after_new[CEIL == 0].max():.3f}; NEW attenuate-only "
          f"{bool(np.all(np.abs(O_new) <= np.abs(X) + 1e-15) and np.all(O_new * X >= 0))}")
    if causal:
        cut = int(600 * FS)
        r6 = worst_block_slope(U[cut:], O_new[cut:])
        print(f"   NEW, metric read from 600 s on (after every detection): worst {max(r6[k] / CEIL[k] for k in CAPPED):.2f} c")
    print()

# ---------------------------------------------------------------- B and D: the (c, g/c) grid
CS = (0.03, 0.05, 0.10, 0.35)
GR = (1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 33.0)
grid = [(cc, gg) for cc in CS for gg in GR]
ng = len(grid)
Ug = partners(ng, 101, [False] * ng)
cg = np.array([cc for cc, _ in grid])


def grid_run(delay_s, net, lowpass=None):
    Xg = np.zeros((T, ng))
    for j, (cc, gg) in enumerate(grid):
        d = copy_route(Ug[:, j], delay_s, 1.0, True)
        if lowpass:
            d = lp(d[:, None], lowpass)[:, 0]
        Xg[:, j] = gg * cc * d
    O, h, e, _ = run(Ug, Xg, cg, net)
    return worst_block_slope(Ug, O) / cg, worst_block_slope(Ug, Xg) / cg, e


def show_grid(title, res):
    stamp(title)
    print("   c \\ g/c " + "".join(f"{gg:>7.1f}" for gg in GR))
    for i, cc in enumerate(CS):
        print(f"   {cc:<8.2f}" + "".join(f"{res[i * len(GR) + j]:>7.2f}" for j in range(len(GR))))
    print()


rB, rawB, _ = grid_run(90.0, "old")
show_grid("B. CURRENT ledger, causal copy delayed 90 s: residual / c by ceiling (rows) and copy gain g/c (columns)", rB)

# ---------------------------------------------------------------- D: the new net over the grid
for dl, lpz, title in ((90.0, None, "delay 90 s (on the key grid)"), (47.35, None, "delay 47.35 s (off every grid)"),
                       (213.7, None, "delay 213.7 s (off every grid)"),
                       (120.0, 30.0, "delay 120 s, copy low-passed tau 30 s")):
    if QUICK and dl not in (90.0, 47.35):
        continue
    rD, rawD, eD = grid_run(dl, "new", lpz)
    show_grid(f"D. NEW net, {title}: residual / c", rD)

# ---------------------------------------------------------------- E: the cost on natural partners
stamp("E. cost: natural partners, counted routes only (fast gear 0.45 s + held 2-min route 0.22 c_k), no unlisted route")
for seed in ((7, 8) if not QUICK else (7,)):
    Un = partners(33, seed, SIGNED)
    Y = np.zeros_like(Un)
    for k in range(33):
        m0 = Un[:, k].mean(); xd = delay(Un[:, k], 0.45 * FS); xd[:5] = m0  # before the session: the neutral partner
        e = xd - (m0 + lp((xd - m0)[:, None], 4.0)[:, 0])  # 4-s onset filter, at rest at the neutral level
        fast = GAIN[k] * (np.maximum(e, 0) if not SIGNED[k] else e)
        Y[:, k] = fast + 0.22 * CEIL[k] * lp((Un[:, k] - Un[:, k].mean())[:, None], 120.0)[:, 0]
    Oo, ho, _, _ = run(Un, Y, CEIL, "old")
    On, hn, en, _ = run(Un, Y, CEIL, "new")
    sl = worst_block_slope(Un, Y)
    print(f"   seed {seed}: counted-route slope max {max(sl[k] / CEIL[k] for k in CAPPED):.2f} c | ledger frames changed "
          f"old {ho[CAPPED].max():.4f}, new {hn[CAPPED].max():.4f} | governor engaged (a<1) on "
          f"{en[CAPPED].max():.4f} of frames (worst channel), mean {en[CAPPED].mean():.4f}")
print()

# ---------------------------------------------------------------- F: absolute noise floor sensitivity
stamp("F. sensitivity: gain-1.5 c copy (90 s) plus ABSOLUTE white noise sigma_abs in the partner-caused part")
for sab in ((0.0, 0.005, 0.02) if not QUICK else (0.02,)):
    r = np.random.default_rng(5)
    Xg = np.zeros((T, ng))
    for j, (cc, gg) in enumerate(grid):
        Xg[:, j] = copy_route(Ug[:, j], 90.0, gg * cc, True) + sab * r.normal(size=T)
    O, h, e, _ = run(Ug, Xg, cg, "new")
    res = worst_block_slope(Ug, O) / cg
    show_grid(f"F. NEW net, sigma_abs {sab}: residual / c (governor engaged on natural noise is the cost)", res)

stamp("done")
