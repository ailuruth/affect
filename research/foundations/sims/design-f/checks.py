"""Algebra checks for design-fibred-attribution-core.md (F1-F10).

These are checks of the design's own inequalities on hand-made instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Run:  python3 -I checks.py      (numpy, scipy)
"""
import numpy as np
from scipy.linalg import svdvals

rng = np.random.default_rng(0)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


# ---------------------------------------------------------------- F1
# Lemma Q (product-set lemma): for diagonal (Q,S,R), a diagonal static
# transfer diag(t) satisfies the quadratic constraint iff every scalar
# q_k t_k^2 + 2 s_k t_k + r_k >= 0. Hence g*I is admissible iff each
# single-channel g*e_k e_k^T is: a diagonal IQC cannot separate
# "match one channel" from "match the whole face".
def f1():
    n = 12
    bad = 0
    for _ in range(2000):
        q = -rng.uniform(0.5, 3, n)
        s = rng.normal(0, 0.3, n)
        r = rng.uniform(0.1, 1, n)
        g = rng.uniform(-1.5, 1.5)
        M = lambda t: np.diag(q * t * t + 2 * s * t + r)  # [T;I]^T [[Q,S],[S,R]] [T;I]
        whole = np.min(np.linalg.eigvalsh(M(np.full(n, g)))) >= -1e-12
        singles = all(q[k] * g * g + 2 * s[k] * g + r[k] >= -1e-12 for k in range(n))
        bad += whole != singles
    report("F1 product-set lemma", bad == 0, f"mismatches {bad}/2000")


# ---------------------------------------------------------------- F2
# Lemma J (joint budget): if ||W1 T W2^{-1}||_2 <= 1, W1 = diag(1/c), W2 = I/sqrt(m),
# then for the gate moving coherently (dg = a*1) a uniform copy g on K output
# channels needs g <= c/sqrt(K); the bound is attained.
def f2():
    m, nout, c = 80, 48, 0.2
    worst = 0.0
    for K in (1, 4, 12, 32):
        # attaining construction T = g 1_K 1^T / m with g = c/sqrt(K)
        g = c / np.sqrt(K)
        T = np.zeros((nout, m)); T[:K, :] = g / m
        nrm = svdvals(np.diag(np.full(nout, 1 / c)) @ T @ (np.sqrt(m) * np.eye(m)))[0]
        worst = max(worst, abs(nrm - 1))
        # random admissible T never beats it
        best = 0.0
        for _ in range(300):
            A = rng.normal(size=(nout, m))
            A /= svdvals(np.diag(np.full(nout, 1 / c)) @ A * np.sqrt(m))[0]
            y = A @ np.ones(m)
            best = max(best, np.min(y[:K]))
        assert best <= c / np.sqrt(K) + 1e-9
    report("F2 joint budget", worst < 1e-9, "g_max = c/sqrt(K) attained, never exceeded (K=1,4,12,32)")


# ---------------------------------------------------------------- F3
# Router: mass, caps, pointwise bound, incremental bound with context + adaptation.
def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()


def router_run(u, ghat, P, w, tau=0.6, L=4.0, gamma=1.0, astar=0.15, TR=3600, tw=60, lags=(15, 60)):
    T, nS = u.shape
    nslot = nS * 2 * 2
    zh = np.zeros(nslot); A = np.zeros(nslot)
    y = np.zeros_like(u); Z = np.zeros((T, nslot)); OM = np.zeros((T, nS, 2))
    for t in range(T):
        zh = zh + (P @ ghat[t] - zh) / tw                     # 2-s low-pass of a Lipschitz map of the gate
        z = np.clip(zh, -L, L) - gamma * np.maximum(A - astar, 0)
        mu = softmax(np.concatenate([z, [0.0]]))[:-1]         # null slot has logit 0
        A = A + (mu - A) / TR
        mu = mu.reshape(nS, 2, 2)                             # (channel, tap, sign)
        om = np.clip(tau * (mu[:, :, 0] - mu[:, :, 1]), -w, w)
        OM[t] = om; Z[t] = z
        for a, l in enumerate(lags):
            if t - l >= 0:
                y[t] += om[:, a] * u[t - l]
    return y, OM, Z


def f3():
    T, nS, Umax = 1500, 32, 2.0
    w = np.full((nS, 2), 0.10); w[:4, 0] = 0.20; w[:4, 1] = 0.15
    P = rng.normal(size=(nS * 4, 80)); P *= 1.0 / svdvals(P)[0] / 8.0   # ||P|| = c_omega * (1/8), c_omega=1
    def gate(u):
        g = np.zeros((len(u), 80)); g[:, :nS] = u; g[:, nS:2 * nS] = np.abs(u) * 0.5
        return g
    u1 = Umax * np.tanh(np.cumsum(rng.normal(0, .2, (T, nS)), 0) / 5)
    u2 = u1 + 0.3 * np.tanh(rng.normal(0, 1, (T, nS)))
    u2 = np.clip(u2, -Umax, Umax)
    y1, om1, z1 = router_run(u1, gate(u1), P, w)
    y2, om2, z2 = router_run(u2, gate(u2), P, w)
    mass = np.abs(om1).sum(axis=(1, 2)).max()
    capok = np.all(np.abs(om1) <= w + 1e-12)
    pw = np.all(np.abs(y1[60:]) <= (w[:, 0] * np.abs(u1[45:-15]) + w[:, 1] * np.abs(u1[:-60])) + 1e-12)
    # incremental bound: ||dy_k|| <= W_k ||du_k|| + Umax * tau * ||dzhat||/(1-gamma/2)
    dzh = np.linalg.norm(z1 - z2)  # conservative: z includes adaptation term already
    lhs = np.linalg.norm(y1 - y2, axis=0)
    rhs = w.sum(1) * np.linalg.norm(u1 - u2, axis=0) + Umax * 0.6 * dzh
    report("F3 router", mass <= 0.6 + 1e-12 and capok and pw and np.all(lhs <= rhs),
           f"max mass {mass:.3f} <= 0.6; caps ok {capok}; pointwise ok {pw}; incremental ok {np.all(lhs<=rhs)}")
    # softmax Jacobian spectral norm <= 1/2 (Popoviciu)
    mx = 0
    for _ in range(3000):
        mu = softmax(rng.normal(0, rng.uniform(0.1, 8), rng.integers(2, 130)))
        J = np.diag(mu) - np.outer(mu, mu); mx = max(mx, np.linalg.eigvalsh(J)[-1])
    # stress the mass bound: strong constant logits on many slots
    P2 = np.zeros((nS * 4, 80)); y3, om3, _ = router_run(u1, gate(u1) * 0, P2, w)
    om_big = None
    zbig = np.full(nS * 4, 4.0)
    mu = softmax(np.concatenate([zbig, [0.0]]))[:-1].reshape(nS, 2, 2)
    mu[:, :, 1] = 0; om_big = np.clip(0.6 * mu[:, :, 0], -w, w)
    report("F3c mass under saturation", np.abs(om_big).sum() <= 0.6, f"all 128 slots at max logit: sum|omega| = {np.abs(om_big).sum():.3f} <= tau; per-channel uniform gain {np.abs(om_big).sum(1).mean():.4f} = tau/32 ~ {0.6/32:.4f}")
    report("F3b softmax Lipschitz", mx <= 0.5 + 1e-12, f"max eig {mx:.4f} <= 1/2")


# ---------------------------------------------------------------- F4
# Twisted channels: any functional of (rest, |fast|) has zero covariance with a
# sign-symmetric fast component; for a skewed one |corr| <= A (conditional sign asymmetry).
def f4():
    T = 200000
    rest = np.convolve(rng.normal(size=T), np.ones(30) / 30, 'same')
    for kind in ("symmetric", "skewed"):
        if kind == "symmetric":
            c = rng.normal(size=T) * (1 + 0.5 * np.abs(rest))
        else:
            e = rng.exponential(size=T); c = (e - 1) * (1 + 0.5 * np.abs(rest))
        env = np.convolve(np.abs(c), np.ones(10) / 10, 'same')
        # a random nonlinear functional of the invariant features, with memory
        h = np.zeros(T); W = rng.normal(size=3)
        for t in range(1, T):
            h[t] = 0.9 * h[t - 1] + np.tanh(W[0] * env[t] + W[1] * rest[t] + W[2] * np.abs(c[t]))
        y = h - h.mean()
        corr = max(abs(np.corrcoef(y[l:], c[:T - l])[0, 1]) for l in (0, 3, 15))
        # A: sqrt(E[c^2 delta^2]/E c^2), delta = E[sign c | |c|, rest] (binned estimate)
        bins_r = np.digitize(np.abs(c), np.quantile(np.abs(c), np.linspace(0, 1, 41)[1:-1]))
        bins_s = np.digitize(rest, np.quantile(rest, np.linspace(0, 1, 6)[1:-1]))
        key = bins_r * 10 + bins_s
        delta = np.zeros(T)
        for kk in np.unique(key):
            idx = key == kk; delta[idx] = np.mean(np.sign(c[idx]))
        A = np.sqrt(np.mean(c ** 2 * delta ** 2) / np.mean(c ** 2))
        noise = 4 / np.sqrt(T)
        if kind == "symmetric":
            report("F4a twisted, symmetric", corr < noise + A, f"max|corr| {corr:.4f}, A {A:.4f}, sampling 4/sqrt(T) {noise:.4f}")
        else:
            report("F4b twisted, skewed", corr <= A + noise, f"max|corr| {corr:.4f} <= A {A:.4f}")


# ---------------------------------------------------------------- F5
# Lemma N (no free persistence): equal-well base, two port types, then the bucket.
def f5():
    D, beta, N = 0.5, 200.0, 9
    m = D * np.arange(N)
    def Vp(b):
        a = -beta * (b - m) ** 2 / 2; p = np.exp(a - a.max()); p /= p.sum()
        return np.sum(p * (b - m))            # dV/db for V = -(1/beta) log sum exp(...)
    def run(s, b0=m[4], dt=0.01):
        b = b0; out = []
        for st in s:
            b += dt * (-Vp(b) + st); out.append(b)
        return np.array(out)
    well = lambda b: int(np.argmin(np.abs(b - m)))
    Fmax = max(abs(Vp(x)) for x in np.linspace(m[4], m[4] + D / 2, 2000))
    # (a) gain port: held level above the barrier force switches; below it never does
    hi = run(np.full(4000, 1.05 * Fmax)); lo = run(np.full(4000, 0.95 * Fmax))
    a_ok = well(hi[-1]) > 4 and well(lo[-1]) == 4
    # (b) derivative port k*dphi/dt, |phi|<=Phi: slow rise, fast fall ratchets one well per cycle
    Phi = 0.35 * D
    cyc = np.concatenate([np.full(3000, 2 * Phi / 30.0), np.full(10, -2 * Phi / 0.1), np.zeros(1000)])
    traj = run(np.tile(cyc, 3))
    nsw = 4 - well(traj[-1])
    b_ok = nsw == 3
    # (c) bucket: capacity 1, refill one token per 60 s: events cannot exceed 1 + T/60
    times = np.sort(rng.uniform(0, 600, 500)); tok, last, fired = 1.0, 0.0, 0
    for t in times:
        tok = min(1.0, tok + (t - last) / 60.0); last = t
        if tok >= 1: tok -= 1; fired += 1
    c_ok = fired <= 1 + 600 / 60
    report("F5 ratchet lemma", a_ok and b_ok and c_ok,
           f"held level switches iff k*S > F_max={Fmax:.3f}: {a_ok}; sawtooth (|phi|<=0.35D) ratchets {nsw} wells in 3 cycles; bucket fired {fired} <= 11")


# ---------------------------------------------------------------- F6
# Learning loop of a routing coefficient with partner echo (mean field).
def f6():
    w = 0.35
    res = []
    for s_star in (-0.3, 0.0, 0.3):
        for gp in (0.5, 1.0):
            for abar in (0.0, 0.8):
                om = 0.0
                for _ in range(200):
                    s = np.clip(s_star + (1 - abar) * gp * om / w * w, -1, 1)  # normalised target with innate scale
                    om = w * s
                fix = w * np.clip(s_star / (1 - (1 - abar) * gp * w), -1, 1)
                res.append(abs(om - fix) < 1e-6 and abs(om) <= w)
    # correlation-normalised rule (sign learner) is bistable without attribution:
    bist = []
    for om0 in (-0.2, 0.2):
        om = om0
        for _ in range(200):
            cov = 0.0 + 1.0 * om; om = w * cov / np.sqrt(cov ** 2 + 0.01 ** 2)
        bist.append(round(om, 3))
    report("F6 learning loop", all(res) and bist[0] == -bist[1] and abs(bist[0]) > 0.34,
           f"linear rule: unique stable fixed point w*s*/(1-(1-a)g_p w) in all 12 cases; correlation rule: fixed points {bist} (bistable, why it is not used)")


# ---------------------------------------------------------------- F7
# Defect floor from own variation: y = m(u) + d, gain(m) <= C, Var d >= sd^2.
def f7():
    T = 20000
    u = np.convolve(rng.normal(size=T), np.ones(20) / np.sqrt(20), 'same')
    u /= u.std()
    ok = True; rows = []
    for C in (0.1, 0.35, 0.6):
        for sd in (0.1, 0.15):
            worst = 1.0
            for _ in range(50):
                # adversarial m: the best copy C*u plus arbitrary own (u-independent) parts
                m = C * u
                d = sd * np.convolve(rng.normal(size=T), np.ones(10) / np.sqrt(10), 'same')
                y = m + d
                rho = np.corrcoef(y, u)[0, 1]
                worst = min(worst, np.sqrt(1 - rho ** 2))
            floor = sd / np.sqrt(C ** 2 + sd ** 2)
            # finite-T: the floor holds up to the sampling error of corr(d,u), ~ 3/sqrt(T_eff)
            tol = 3 / np.sqrt(T / 20)
            ok &= worst >= floor - tol
            rows.append(f"C={C},sd={sd}: worst defect {worst:.3f} >= {floor:.3f} - {tol:.3f}")
    report("F7 defect floor", ok, "; ".join(rows))


# ---------------------------------------------------------------- F8
# Lemma B: centres with separation >= dmin, beta large, tilt <= tmax: every centre keeps
# a stable equilibrium within r.
def f8():
    nb, C, dmin, beta, hmax, tmax, r = 24, 64, 0.5, 200.0, 0.5, 0.05, 0.1
    mu = []
    while len(mu) < C:
        x = rng.normal(size=nb); x *= rng.uniform(0, 1) ** (1 / nb) / np.linalg.norm(x)
        if all(np.linalg.norm(x - y) >= dmin for y in mu): mu.append(x)
    mu = np.array(mu)
    worst = 0
    for trial in range(5):
        h = rng.uniform(-hmax, hmax, C); tilt = rng.normal(size=nb); tilt *= tmax / np.linalg.norm(tilt)
        def grad(b):
            a = -beta * ((b - mu) ** 2).sum(1) / 2 + h; p = np.exp(a - a.max()); p /= p.sum()
            return (p[:, None] * (b - mu)).sum(0) - tilt
        for c in range(C):
            b = mu[c] + rng.normal(size=nb) * 0.02
            for _ in range(400): b -= 0.5 * grad(b)
            worst = max(worst, np.linalg.norm(b - mu[c]))
    report("F8 landscape persistence", worst < r, f"max distance of equilibrium from its centre {worst:.4f} < r={r} (tilt {tmax})")


# ---------------------------------------------------------------- F9
# Slew-limited display contributes RMS <= V/omega_c above a high-pass corner omega_c.
def f9():
    fs, T = 30.0, 30 * 3600
    V = 1 / 300.0  # per second
    x = np.zeros(T); tgt = 0.0
    for t in range(1, T):
        if rng.uniform() < 1 / (30 * 20): tgt = rng.uniform(-1, 1)
        x[t] = x[t - 1] + np.clip(tgt - x[t - 1], -V / fs, V / fs)
    wc = 1 / 60.0
    a = np.exp(-wc / fs); hp = np.zeros(T)
    for t in range(1, T): hp[t] = a * (hp[t - 1] + x[t] - x[t - 1])
    rms = np.sqrt(np.mean(hp ** 2))
    report("F9 slew bound", rms <= V / wc, f"RMS above corner {rms:.4f} <= V/w_c {V/wc:.4f}")


# ---------------------------------------------------------------- F10
# Totals table (section 3.5) from the innate constants.
def f10():
    # innate constants of section 2.1 (design-fibred-attribution-core.md)
    c, cT, cw, O = 0.15, 1.0, 0.2, 0.08            # REN Schur / twisted ceilings, logit Lipschitz, role cap
    A, vb, kb, kz, vz, nz = 0.25, 1/600, 0.5, 0.25, 1/600, 5
    tau, sd, m = 0.6, 0.15, 80
    Lown = 0.05
    slow = A * vb + c * (kb * vb + kz * np.sqrt(nz) * vz) + Lown * (vb + np.sqrt(nz) * vz)  # per second
    W = {"smile/brow mid": 0.30, "smile/brow slow": 0.25, "other mid/slow": 0.20}
    print(f"     slow-route rate Sigma = {slow:.2e} /s")
    print("     channel           T=4s   T=10s  T=30s  T=60s   (W_k + c_k + O_k + 2*Sigma*T), partner RMS a=1")
    mx = 0
    for k, Wk in W.items():
        vals = [Wk + c + O + 2 * slow * Tw for Tw in (4, 10, 30, 60)]
        mx = max(mx, max(vals))
        print(f"     {k:16s}  " + "  ".join(f"{v:.3f}" for v in vals))
    fl = lambda C, a=1.0: sd / np.sqrt((C * a) ** 2 + sd ** 2)
    K = 32
    whole = tau / K + c * np.sqrt(m / K) / np.sqrt(m) + O + 2 * slow * 10
    four = min(0.30, tau / 4) + c * np.sqrt(m / 4) / np.sqrt(m) + O + 2 * slow * 10
    # incremental (loop) gain of the continuous part, window T<=30 s, gamma=4, T_R=120 s
    Ga = np.sqrt(0.30 * tau) + cT / np.sqrt(m) + 2 * 2.0 * tau * cw / (1 - 4 * 30 / (2 * 120)) / np.sqrt(m)  # Schur test + REN + context
    report("F10 totals", mx < 0.65 and whole < 0.15,
           f"max single-channel {mx:.3f}; 4-channel subspace {four:.3f}; whole Schur face {whole:.3f}; "
           f"observable defect floors (sd=0.15, a=1): single {fl(mx):.2f}, 4-ch {fl(four):.2f}, whole {fl(whole):.2f}; "
           f"at a=2: single {fl(mx,2):.2f}, whole {fl(whole,2):.2f}; loop gain Gamma_A {Ga:.3f}; "
           f"floor at single 0.549 with sd doubled: {0.30/np.sqrt(0.549**2+0.09):.2f}")


def f11():
    # Whole-face router factor varpi_K = ||M|| ||M'|| / ||u_K||^2 for independent partner coordinates,
    # with the innate tap-lag dispersion (tap 1: 0.35-0.65 s, tap 2: 1.5-2.5 s at 30 Hz).
    r = np.random.default_rng(1); out = []
    for K in (4, 32):
        T = 30000
        u = np.array([np.convolve(r.normal(size=T), np.ones(30) / np.sqrt(30), 'same') for _ in range(K)]).T
        lags = set(r.integers(10, 20, K)) | set(r.integers(45, 75, K))
        M = np.max(np.abs(np.stack([np.roll(u, l, axis=0) for l in lags])), axis=(0, 2))
        Mp = np.max(np.abs(np.roll(u, 15, axis=0)), axis=1)
        out.append((K, np.linalg.norm(M) * np.linalg.norm(Mp) / np.sum(u ** 2)))
    w32 = out[1][1]
    S = 0.25 / 600 + 0.15 * (0.5 / 600 + 0.25 * np.sqrt(5) / 600) + 0.05 * (1 / 600 + np.sqrt(5) / 600)
    whole = 0.6 * w32 + 0.15 * np.sqrt(80 / 32) / np.sqrt(80) + 0.08 + 2 * S * 10
    four = min(0.30, 0.6 * out[0][1]) + 0.15 * np.sqrt(80 / 4) / np.sqrt(80) + 0.08 + 2 * S * 10
    fl = lambda C: 0.15 / np.sqrt(C ** 2 + 0.15 ** 2)
    report("F11 attention-chasing worst case", whole < 0.3 and four < 0.5,
           f"varpi_4={out[0][1]:.3f}, varpi_32={w32:.3f}; worst whole Schur face {whole:.3f} (floor {fl(whole):.2f}); "
           f"worst 4-channel {four:.3f} (floor {fl(four):.2f})")


for f in (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11):
    f()
print(f"\n{sum(OK)}/{len(OK)} checks pass")
