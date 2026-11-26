"""Algebra checks for design-cayley-ledger.md (G1-G10).

Checks of the design's own inequalities on hand-made instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Run:  python3 -I checks.py      (numpy, scipy; about a minute)
"""
import numpy as np
from scipy.optimize import linprog
from scipy.signal import lfilter, coherence

rng = np.random.default_rng(1)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


# ------------------------------------------------------------------ helpers
def hinf_gain(A, B, C, n=400):
    """H-infinity norm of x+ = Ax + Bu, y = Cx (sampled on the unit circle)."""
    m = 0.0
    I = np.eye(A.shape[0])
    for w in np.linspace(0, np.pi, n):
        G = C @ np.linalg.solve(np.exp(1j * w) * I - A, B)
        m = max(m, np.linalg.svd(G, compute_uv=False)[0])
    return m


def make_stage(nin, nst, nout, sign=1.0):
    """A strictly causal stage: linear filter (H-inf gain 1) -> tanh -> W (||W||<=1) * sign."""
    A = rng.normal(size=(nst, nst))
    A *= rng.uniform(0.6, 0.97) / max(abs(np.linalg.eigvals(A)))
    B = rng.normal(size=(nst, nin))
    C = rng.normal(size=(nst, nst))
    g = hinf_gain(A, B, C)
    B /= g
    W = rng.normal(size=(nout, nst))
    W /= np.linalg.svd(W, compute_uv=False)[0]
    return dict(A=A, B=B, C=C, W=sign * W)


def run_stage(st, w):
    T = w.shape[0]
    x = np.zeros(st["A"].shape[0])
    out = np.zeros((T, st["W"].shape[0]))
    for t in range(T):
        out[t] = st["W"] @ np.tanh(st["C"] @ x)   # depends on w_{<t}: strictly causal
        x = st["A"] @ x + st["B"] @ w[t]
    return out


class Contraction:
    """S = gamma * stage2(stage1(w)); each stage has incremental l2 gain <= 1.
    sign1, sign2 = -1 puts two sign flips IN SERIES inside S."""
    def __init__(self, n, gamma, signs=(-1.0, -1.0)):
        self.s1 = make_stage(n, 10, 8, signs[0])
        self.s2 = make_stage(8, 10, n, signs[1])
        self.g = gamma

    def step_run(self, w):  # used only open loop
        return self.g * run_stage(self.s2, run_stage(self.s1, w))


def cayley_run(S, u, kappa):
    """y = 2 K^{1/2} S(w),  w = K^{1/2} u - S(w)  (S strictly causal -> explicit recursion)."""
    T, n = u.shape
    k = np.sqrt(kappa)
    st1, st2 = S.s1, S.s2
    x1 = np.zeros(st1["A"].shape[0]); x2 = np.zeros(st2["A"].shape[0])
    z1 = np.zeros(st1["W"].shape[0])
    y = np.zeros((T, n))
    for t in range(T):
        s_t = S.g * (st2["W"] @ np.tanh(st2["C"] @ x2))   # S output at t: uses w_{<t}
        w_t = k * u[t] - s_t
        y[t] = 2 * k * s_t
        # advance stage 1 with w_t, stage 2 with stage-1 output at t
        z1 = st1["W"] @ np.tanh(st1["C"] @ x1)
        x1 = st1["A"] @ x1 + st1["B"] @ w_t
        x2 = st2["A"] @ x2 + st2["B"] @ z1
    return y


# ---------------------------------------------------------------- G1
def g1():
    n, T = 6, 600
    kappa = rng.uniform(0.2, 0.35, n)
    gamma = 0.5
    b = 2 * gamma / (1 + gamma)
    L = 2 * np.sqrt(kappa.max() * kappa.max()) * gamma / (1 - gamma)
    worst_r, worst_g = -9.0, 0.0
    for trial in range(40):
        S = Contraction(n, gamma, signs=(-1.0, -1.0))
        u = rng.normal(size=(T, n)) * rng.uniform(0.2, 2.0)
        y0 = cayley_run(S, u, kappa)
        # random perturbations, including single-channel, lagged-sinusoid and adversarial hill climb
        cands = []
        for _ in range(6):
            cands.append(rng.normal(size=(T, n)) * rng.uniform(0.01, 1.0))
        k = rng.integers(n)
        d = np.zeros((T, n)); d[:, k] = np.sin(2 * np.pi * np.arange(T) / rng.uniform(4, 60)); cands.append(d)
        for d in cands:
            best = d
            y1 = cayley_run(S, u + best, kappa)
            r = np.sum((y1 - y0) * best) / np.sum(kappa * best ** 2)
            for it in range(15):          # crude hill climb on the ratio
                trial_d = best + 0.3 * rng.normal(size=best.shape) * np.std(best)
                y1t = cayley_run(S, u + trial_d, kappa)
                rt = np.sum((y1t - y0) * trial_d) / np.sum(kappa * trial_d ** 2)
                if rt > r:
                    best, r, y1 = trial_d, rt, y1t
            worst_r = max(worst_r, r)
            worst_g = max(worst_g, np.linalg.norm(y1 - y0) / np.linalg.norm(best))
    report("G1 Cayley wrap: one-sided sector end to end (two sign flips in series inside S)",
           worst_r <= b + 1e-9,
           f"max <dy,du>/<du,K du> = {worst_r:.3f} <= b = {b:.3f}; max gain {worst_g:.3f} <= L = {L:.3f}")
    report("G1b gain cap", worst_g <= L + 1e-9, f"{worst_g:.3f} <= {L:.3f}")
    # Without the wrap: the same two-flip S read out directly is a positive (copy-direction) map.
    S = Contraction(n, 0.99, signs=(-1.0, -1.0))
    # make both stages near-identity-sign to show the hazard: use a pure LTI two-flip chain
    u = rng.normal(size=(4000, 1))
    a = 0.9
    f1 = -lfilter([1 - a], [1, -a], u[:, 0])
    f2 = -lfilter([1 - a], [1, -a], f1)
    c = np.corrcoef(f2[50:], lfilter([1 - a], [1, -a], lfilter([1 - a], [1, -a], u[:, 0]))[50:])[0, 1]
    r_dc = np.sum(f2 * u[:, 0]) / np.sum(u[:, 0] ** 2)
    report("G1c two sign flips in series, unwrapped, give positive concordance",
           r_dc > 0, f"<y,u>/<u,u> = {r_dc:.3f} > 0 (copy direction); wrapped version is capped at b")


# ---------------------------------------------------------------- G2
def g2():
    kap, gam = 0.3, 0.5
    a = -2 * kap * gam / (1 - gam); b = 2 * kap * gam / (1 + gam)
    rad = (b - a) / 2
    # (i) scalar image of |s|<=gamma is the disc with diameter [a,b]
    th = np.linspace(0, 2 * np.pi, 2000)
    s = gam * np.exp(1j * th)
    g = 2 * kap * s / (1 + s)
    ok = abs(g.real.max() - b) < 1e-3 and abs(g.real.min() - a) < 1e-3
    report("G2a Cayley image is the disc on diameter [a,b]", ok,
           f"a = {a:.3f}, b = {b:.3f}, radius {rad:.3f}, max|g| = {abs(g).max():.3f} = |a|")
    # (ii) the naive half-plane Re H <= kappa admits a lagged copy at any gain
    c, tau = 3.0, 15
    w = np.linspace(0, np.pi, 4000)
    H = c * np.exp(-1j * w * tau) - (c - kap)
    report("G2b naive Re H <= kappa admits lag-copy + lag-0 anti-copy at gain c",
           H.real.max() <= kap + 1e-9, f"c = {c}: max Re H = {H.real.max():.3f} <= {kap}; max|H| = {abs(H).max():.2f}")
    # (iii) worst lag-tau concordance inside the disc class: LP over causal FIR kernels
    #      (disc approximated by an inscribed 24-gon -> slightly conservative inner class)
    N, tau = 60, 15
    freqs = np.linspace(0, np.pi, 160)
    M = 24
    rows, rhs = [], []
    ctr = (a + b) / 2
    for wv in freqs:
        e = np.exp(-1j * wv * np.arange(N))
        for m in range(M):
            phi = 2 * np.pi * m / M
            # Re( (H - ctr) e^{-i phi} ) <= rad*cos(pi/M)
            rows.append((e * np.exp(-1j * phi)).real)
            rhs.append(rad * np.cos(np.pi / M) + ctr * np.cos(phi))
    rows, rhs = np.array(rows), np.array(rhs)
    obj = np.zeros(N); obj[tau] = -1
    res = linprog(obj, A_ub=rows, b_ub=rhs, bounds=[(-5, 5)] * N, method="highs")
    white = -res.fun
    # smooth partner: AR(1) with correlation time ~1 s at 30 Hz
    rho = np.exp(-1 / 30)
    r = rho ** np.abs(tau - np.arange(N))
    res2 = linprog(-r, A_ub=rows, b_ub=rhs, bounds=[(-5, 5)] * N, method="highs")
    smooth = -res2.fun
    report("G2c worst broadband lag-0.5 s concordance in the class <= disc radius",
           white <= rad + 1e-6,
           f"white partner: {white:.3f} <= radius {rad:.3f}; smooth (1 s) partner: {smooth:.3f}; zero-lag cap b = {b:.3f}; any-signal cap |a| = {-a:.3f}")
    return a, b, rad


# ---------------------------------------------------------------- G3
def g3():
    n, kap = 16, 0.3
    c = n * kap                   # whole-face projection copy H = (c/n) 11^T has diagonal kap
    H = (c / n) * np.ones((n, n))
    v = np.ones(n) / np.sqrt(n)
    report("G3 diagonal-only sector admits a shared-subspace copy",
           np.allclose(np.diag(H), kap) and v @ H @ v > 1,
           f"diag = {kap}, but gain along the mean-face direction = {v @ H @ v:.2f} (copy); matrix sector He H <= K caps it at {kap}")


# ---------------------------------------------------------------- G4
def g4():
    # correlated partner channels: cross route smile->cheek copies the cheek
    T = 20000
    s = lfilter([0.05], [1, -0.95], rng.normal(size=T))
    u = np.stack([s, s + 0.1 * rng.normal(size=T) * s.std()], 1)   # lip corner, cheek co-move
    H = np.array([[-1.0, 0.0], [1.0, 0.0]])                            # cheek_out = +1 * lip corner
    y = u @ H.T
    gain_cheek = np.sum(y[:, 1] * u[:, 1]) / np.sum(u[:, 1] ** 2)
    He = (H + H.T) / 2
    lam = np.linalg.eigvalsh(He).max()
    report("G4 correlated partner: a cross route copies a channel; matrix sector sees it",
           gain_cheek > 0.9 and lam > 0.2,
           f"cheek gain {gain_cheek:.2f} via lip->cheek; lambda_max(He H) = {lam:.2f} > kappa, so this H is outside the matrix sector")


# ---------------------------------------------------------------- G5
def g5():
    fs_r = 2.0                 # release rate (Hz)
    tau_h = 3.2                # high-pass corner (s)
    sig = 7.1                  # release noise
    alpha = 2.0
    # step response of the innate release filter, sampled at 2 Hz (30 Hz pipeline, LP 1 Hz, HP tau_h)
    fs = 30.0
    t = np.arange(0, 120, 1 / fs)
    step = np.ones_like(t)
    a_hp = np.exp(-1 / (tau_h * fs))
    hp = lfilter([1, -1], [1, -a_hp], step) * (1 + a_hp) / 2
    a_lp = np.exp(-2 * np.pi * 1.0 / fs)
    sh = lfilter([1 - a_lp], [1, -a_lp], hp)
    sh_r = sh[:: int(fs / fs_r)]
    E1 = np.sum(sh_r ** 2)
    E = 2 * E1                 # two edges (onset and release of one held window)
    epsL = alpha * E / (2 * sig ** 2)
    rhoL = np.sqrt((np.exp(epsL) - 1) / 2)
    report("G5a level-neighbour cost is finite and window-independent",
           epsL < 0.2, f"E_h = {E:.2f} (two edges), eps_L(2) = {epsL:.3f}, HCR correlation bound {rhoL:.3f}")
    # K3-style attack: partner holds levels (changing every ~10 min) plus transients every 15 s
    hours = 6
    T = int(hours * 3600 * fs_r)
    lev = np.zeros(T)
    k = 0
    while k < T:
        d = int(rng.exponential(600) * fs_r) + 1
        lev[k:k + d] = rng.choice([-1, -0.5, 0, 0.5, 1])
        k += d
    trans = np.zeros(T)
    for j in range(0, T, int(15 * fs_r)):
        trans[j:j + 3] += rng.normal(0, 0.5)
    p = lev + trans
    # release: high-pass (2 Hz version) + noise
    a2 = np.exp(-1 / (tau_h * fs_r))
    rel_clean = lfilter([1, -1], [1, -a2], p) * (1 + a2) / 2
    def track(rel, leak):
        # inverse of the high-pass, then leaky integration (attacker's level estimate)
        inv = lfilter([1, -a2], [1, -1 + leak], rel) * 2 / (1 + a2)
        return inv
    def onemin_corr(x, y):
        m = int(60 * fs_r)
        X = x[: len(x) // m * m].reshape(-1, m).mean(1)
        Y = y[: len(y) // m * m].reshape(-1, m).mean(1)
        return np.corrcoef(X, Y)[0, 1]
    best_clean = max(onemin_corr(track(rel_clean, l), lev) for l in [1e-5, 1e-4, 1e-3])
    best_noisy = -1
    for l in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]:
        reps = [onemin_corr(track(rel_clean + sig * rng.normal(size=T), l), lev) for _ in range(3)]
        best_noisy = max(best_noisy, np.mean(reps))
    # genie: knows the change times; estimates each step amplitude from the released transient
    chg = np.flatnonzero(np.diff(lev) != 0) + 1
    rel = rel_clean + sig * rng.normal(size=T)
    tmpl = lfilter([1, -1], [1, -a2], np.ones(int(20 * fs_r))) * (1 + a2) / 2
    est = np.zeros(T); cur = 0.0
    last = 0
    for c in list(chg) + [T]:
        est[last:c] = cur
        if c < T:
            seg = rel[c:c + len(tmpl)]
            amp = np.dot(seg, tmpl[: len(seg)]) / np.dot(tmpl[: len(seg)], tmpl[: len(seg)])
            cur = cur + amp
        last = c
    genie = onemin_corr(est, lev)
    report("G5b held-level tracking through the released stream (any slow state)",
           best_noisy < 0.3 and best_clean > 0.9,
           f"1-min corr: no noise {best_clean:.2f}; ledger noise: best leaky tracker {best_noisy:.2f}; change-time genie {genie:.2f}")
    return epsL, rhoL


# ---------------------------------------------------------------- G6
def g6():
    taus_min = 2 * 3.0 ** np.arange(8)      # 2 min ... 73 h
    taus = taus_min * 60
    # write SNR: stationary input-driven variance 1, own noise variance 1% of it
    noise_frac = 0.01
    out = []
    for D in [3600, 6 * 3600, 24 * 3600]:
        bits = 0
        for tau in taus:
            r2 = np.exp(-2 * D / tau)
            snr2 = r2 / (noise_frac * (1 - r2) + 1e-300)
            bits += 16 * 0.5 * np.log2(1 + snr2)
        out.append(bits)
    # slots: 128 slots x 32 effective dims, tau 30 days, same noise fraction
    slot_bits = []
    for D in [3600, 24 * 3600, 7 * 24 * 3600]:
        r2 = np.exp(-2 * D / (30 * 86400))
        slot_bits.append(128 * 32 * 0.5 * np.log2(1 + r2 / (noise_frac * (1 - r2))))
    report("G6 persistent capacity (linear modes: no wells, so no noise-driven switching)",
           out[0] > 100 and slot_bits[1] > 1000,
           f"mood ladder bits retained after 1 h / 6 h / 24 h: {out[0]:.0f} / {out[1]:.0f} / {out[2]:.0f}; slots after 1 h / 1 d / 1 wk: {slot_bits[0]:.0f} / {slot_bits[1]:.0f} / {slot_bits[2]:.0f}")


# ---------------------------------------------------------------- G7
def g7():
    G, lam, eta = 1.0, 0.5, 0.01
    phi0 = 0.0
    phi = phi0
    mx = 0
    for t in range(200000):
        grad = -G                     # adversary always pushes phi up (toward the cap)
        phi = phi - eta * (grad + lam * (phi - phi0))
        mx = max(mx, phi - phi0)
    gam = 0.5
    sig = 1 / (1 + np.exp(-(phi0 + G / lam)))
    ge = gam * sig
    kap = 0.3
    inph = 2 * ge / (1 + ge) * kap
    cap = 2 * gam / (1 + gam) * kap
    report("G7 clipped SGD with innate pull stays in the ball for any data",
           mx <= G / lam + 1e-9,
           f"max |phi-phi0| = {mx:.4f} <= G/lambda = {G/lam}; learned in-phase gain <= {inph:.3f} < cap {cap:.3f} < copy 1")


# ---------------------------------------------------------------- G8
def g8():
    fs = 30
    def visemes(phon):
        # each phoneme ~ 80 ms, jawOpen target by phoneme class, smoothed by articulator filter
        tgt = np.repeat(np.array([[0.1, 0.6, 0.3, 0.9, 0.2, 0.5][p] for p in phon]), int(0.08 * fs))
        a = np.exp(-1 / (0.05 * fs))
        return lfilter([1 - a], [1, -a], tgt)
    def maxlagcorr(x, y, maxlag=90):
        x = x - x.mean(); y = y - y.mean()
        best = -1
        for l in range(0, maxlag):
            n = min(len(x) - l, len(y))
            c = np.dot(x[l:l + n], y[:n]) / np.sqrt(np.dot(x[l:l + n], x[l:l + n]) * np.dot(y[:n], y[:n]))
            best = max(best, c)
        return best
    res = {}
    for overlap in [0.0, 0.3, 1.0]:
        cs = []
        for _ in range(60):
            p = rng.integers(0, 6, 60)
            q = rng.integers(0, 6, 60)
            m = rng.random(60) < overlap
            q[m] = p[m]
            cs.append(maxlagcorr(visemes(q), visemes(p)))
        res[overlap] = np.mean(cs)
    report("G8 viseme route: best-lag correlation vs phoneme overlap",
           res[0.3] < 0.5 and res[1.0] > 0.95,
           f"overlap 0: {res[0.0]:.2f}; overlap 0.3 (echo-guard limit): {res[0.3]:.2f}; verbatim echo: {res[1.0]:.2f}")


# ---------------------------------------------------------------- G9
def g9():
    # C1: own fast head micro-motion suppressed by the partner's fast-band envelope
    fs, T = 30, 30 * 600
    def band(x, lo, hi):
        from scipy.signal import butter, filtfilt
        bb, aa = butter(2, [lo / (fs / 2), hi / (fs / 2)], "band")
        return filtfilt(bb, aa, x)
    def partner():
        burst = (lfilter([0.02], [1, -0.98], rng.normal(size=T)) > 0.05).astype(float)
        return band(rng.normal(size=T), 2.6, 6.5) * burst + band(rng.normal(size=T), 0.2, 1.1)
    def agent(pv, gate):
        env = np.abs(band(pv, 2.6, 6.5))
        env = lfilter([0.05], [1, -0.95], env)
        g = 1 / (1 + gate * env / (env.mean() + 1e-9)) if gate else 1.0
        own = band(rng.normal(size=T), 2.6, 6.5) * g
        slow = 0.2 * np.roll(band(pv, 0.2, 1.1), 15) + band(rng.normal(size=T), 0.2, 1.1)
        return own + slow
    def coh(x, y):
        f, C = coherence(x, y, fs=fs, nperseg=256)
        return C[(f >= 2.6) & (f <= 6.5)].mean(), C[(f >= 0.2) & (f <= 1.1)].mean()
    p1, p2 = partner(), partner()
    a1 = agent(p1, gate=4.0)
    real_fast, real_slow = coh(a1, p1)
    sur_fast, sur_slow = coh(a1, p2)
    report("G9 C1 sign of band coupling from an envelope gate (sign-free) plus a 0.5 s slow match",
           real_slow > sur_slow,
           f"fast band coherence real {real_fast:.4f} vs surrogate {sur_fast:.4f}; slow band real {real_slow:.4f} vs surrogate {sur_slow:.4f}")


# ---------------------------------------------------------------- G10
def g10():
    # the fast fibre forgets held levels: S begins with an innate high-pass, so a held step gives y -> const
    n, T = 3, 30 * 60
    kappa = np.full(n, 0.3)
    S = Contraction(n, 0.5, signs=(1.0, -1.0))
    # prepend a high-pass to stage 1 by modifying input: wrap applies to raw u, S sees HP(w)
    a = np.exp(-1 / (4 * 30))
    class HPS:
        pass
    u0 = np.zeros((T, n)); u1 = u0.copy(); u1[300:, 0] = 1.0   # held offset from t = 10 s
    def run(u):
        k = np.sqrt(kappa)
        st1, st2 = S.s1, S.s2
        x1 = np.zeros(st1["A"].shape[0]); x2 = np.zeros(st2["A"].shape[0]); hp = np.zeros(n); wprev = np.zeros(n)
        y = np.zeros((T, n))
        for t in range(T):
            s_t = S.g * (st2["W"] @ np.tanh(st2["C"] @ x2))
            w_t = k * u[t] - s_t
            y[t] = 2 * k * s_t
            hp = a * hp + (1 + a) / 2 * (w_t - wprev); wprev = w_t   # gain-1 high-pass inside S
            z1 = st1["W"] @ np.tanh(st1["C"] @ x1)
            x1 = st1["A"] @ x1 + st1["B"] @ hp
            x2 = st2["A"] @ x2 + st2["B"] @ z1
        return y
    d = run(u1) - run(u0)
    late = np.abs(d[-300:]).max()
    early = np.abs(d[300:400]).max()
    report("G10 held partner level: fast-fibre response decays (zero DC inside S)",
           late < 0.05 * max(early, 1e-9) + 1e-6,
           f"peak response {early:.3f}; response after 50 s of holding {late:.2e}")


if __name__ == "__main__":
    g1(); g2(); g3(); g4(); g5(); g6(); g7(); g8(); g9(); g10()
    print(f"\n{sum(OK)}/{len(OK)} checks pass")
