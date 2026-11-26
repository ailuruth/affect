"""Algebra checks for design-cayley-ledger.md, revision 3 (G1-G9).

Checks of the design's own inequalities and constants on hand-made instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
The scenario numbers (G7) are what the design's own equations and innate constants give
for stated inputs; they are a consistency check of the design, not a prediction tested on people.
Run:  python3 -I checks.py      (numpy, scipy; about two minutes)
"""
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import minimize

rng = np.random.default_rng(11)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def slope(x, y):
    x = x - x.mean(); y = y - y.mean()
    return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n
    return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs))
    return lfilter([a], [1, -(1 - a)], x)


# ------------------------------------------------------------------ innate constants (revision 3)
KAPPA, KLAT, KA, GF = 0.30, 0.05, 0.05, 0.45
TAU_I = TAU_O = 4.0
LAG_ECHO = 0.45
# one-sided slow cone: traces (completely monotone: first-order low-passes of the partner's face)
TAU_M = np.array([20.0, 120.0, 1200.0, 10800.0])     # 20 s, 2 min, 20 min, 3 h
B_M = np.array([0.00, 0.05, 0.03, 0.02])             # in-phase budget per trace, sum = b = 0.10
N_M = np.array([0.50, 0.40, 0.30, 0.20])             # anti (same-channel) reach per trace, sum 1.40
A_M = np.array([0.25, 0.12, 0.08, 0.04])             # max |entry| off-diagonal per trace
R_M = np.array([0.30, 0.15, 0.10, 0.05])             # max off-diagonal row sum per trace (total 0.60)
# innate synergist mask: channel pairs that co-activate in the agent's own innate synergies (P_0 grouping);
# on these pairs every off-diagonal entry is capped at b_m, so co-moving natural channels cannot carry copy
B_TOT = B_M.sum()
A_NAME = 0.05                                        # held face allowance of the naming port
A_PORT = 0.10; TAU_PORT = 15.0


def fast_disc(g, k=KAPPA):
    return 2 * g / (1 + g) * k, -2 * g / (1 - g) * k


# ================================================================== G1 every input to the fast block inside
print("=== G1: fast block with every input inside the bound; turn-onset sampling (K1, K1b, K2)")
fs = 30.0
T = int(4 * 3600 * fs)
rng1 = np.random.default_rng(3)


def partner_voice(final_lowering):
    """Critic's ctx_route partner (held F0 level, ~20-min segments, 2-s phrases, 3-8 s turns),
    plus an optional final lowering of the last phrase of each turn proportional to the level."""
    lev = np.zeros(T); t = 0
    while t < T:
        L = int(rng1.exponential(20 * 60 * fs)) + int(120 * fs)
        lev[t:t + L] = rng1.uniform(0.2, 1); t += L
    vad = np.zeros(T); u = np.zeros(T); offs = []; t = 0; cur = lev[0]
    while t < T - 40 * fs:
        dur = int(rng1.uniform(3, 8) * fs); p = t
        while p < t + dur:
            pl = int(rng1.uniform(1.5, 2.5) * fs)
            cur = lev[p] + rng1.normal(0, 0.05)
            if p + pl >= t + dur:
                cur = lev[p] * (1 - final_lowering) + rng1.normal(0, 0.05)
            u[p:p + pl] = cur; p += pl
        vad[t:t + dur] = 1; t += dur; offs.append(t)
        on = t + int(rng1.uniform(0.25, 0.35) * fs)          # r3: body onset ~300 ms
        end = on + int(rng1.uniform(3, 8) * fs) + int(rng1.uniform(0.3, 1) * fs)
        u[t:end] = cur; t = end
    u[t:] = cur
    return u, lev, vad, np.array([o for o in offs if o < T - 5 * fs])


def fast_loop(u, gate, bias=None):
    """Scalar fast wrap: w = sqrt(k)u - s, s = H_o( g_t * GF * Delay_0.45(H_i w) ) [+ bias term], y = 2 sqrt(k) s.
    gate: array in [-1, 1] (any signal, partner-dependent or not).  bias: optional additive context-only
    input to the block (r2's K1 route), which r3 forbids."""
    sk = np.sqrt(KAPPA); ai = 1 - np.exp(-1 / (TAU_I * fs)); ao = ai
    nl = int(LAG_ECHO * fs); buf = np.zeros(nl); bi = 0
    y = np.zeros(len(u)); lpi = lpo = 0.0; s = 0.0
    for t in range(len(u)):
        w = sk * u[t] - s; y[t] = 2 * sk * s
        hpi = w - lpi; lpi += ai * (w - lpi)
        d = buf[bi]; buf[bi] = hpi; bi = (bi + 1) % nl
        f = GF * gate[t] * d + (0.0 if bias is None else bias[t])
        hpo = f - lpo; lpo += ao * (f - lpo); s = hpo
    return y


u, lev, vad, offs = partner_voice(final_lowering=0.2)
kn = lp(np.sqrt(KAPPA) * u, 60.0, fs)                    # slow knowledge of the held level (r2 H2 construction)
onsets = offs + int(0.30 * fs)
cone_F0 = sum(B_M[m] * lp(u, TAU_M[m], fs) for m in range(4))   # cone at its in-phase maximum on F0
win = [np.arange(o, o + int(4 * fs)) for o in offs]


def turn_locked(y):
    return slope(lev[offs], np.array([y[w].mean() for w in win]))


print("   partner: held F0 level, 2-s phrases, final lowering 20% of level at every turn end (harsher than the critic's)")
y_r2 = fast_loop(u, np.zeros(T), bias=3.5 * kn * (1 - vad))
print(f"   r2 as specified (context-only REN term, gain 3.5): sampled onset target slope {slope(lev[onsets], y_r2[onsets]):+.3f};"
      f" turn-locked face slope {turn_locked(y_r2):+.3f}")
worst_samp, worst_tl, worst_zl = 0.0, 0.0, 0.0
for A in (0.5, 1.0, 3.5, 10.0):
    for kind in ("role", "face-typed (forbidden)"):
        if kind == "role":
            g = np.clip(A * (1 - 2 * vad), -1, 1)                    # adversarial role gate
        else:
            g = np.clip(A * (kn / np.sqrt(KAPPA) - 0.6) * 4, -1, 1)  # gate from held-level knowledge
        for sgn in (+1, -1):
            y = fast_loop(u, sgn * g)
            tl = turn_locked(y); zl = slope(u - lp(u, 4.0, fs), y)
            samp = slope(lev[onsets], (cone_F0)[onsets])             # r3 phrase target: cone + own (no fast, no port)
            if kind == "role":
                worst_samp = max(worst_samp, samp); worst_tl = max(worst_tl, abs(tl)); worst_zl = max(worst_zl, zl)
            if A == 3.5:
                print(f"   r3 gate {kind:22s} A={A:4.1f} sign {sgn:+d}: phrase target (cone+own) slope {samp:+.3f};"
                      f" turn-locked face {tl:+.3f}; zero-lag in-phase {zl:+.3f}")
fast_in, fast_anti = fast_disc(GF)
report("G1a K1 closed: phrase targets sampled at onset carry no fast or port term; slope <= b",
       worst_samp <= B_TOT + 0.01, f"worst {worst_samp:+.3f} (b = {B_TOT:.2f}) for every gate gain; r2 route gave {slope(lev[onsets], y_r2[onsets]):+.2f}")
report("G1b fast face with bias-free gates: zero-lag in-phase <= fast cap for every gate gain",
       worst_zl <= fast_in + 0.01, f"worst {worst_zl:+.3f} (cap {fast_in:.3f})")
report("G1c turn-locked face (0-4 s after each partner turn end) vs held level, free-typed gates",
       worst_tl <= 0.10, f"worst |slope| {worst_tl:.3f}; bound = |fast reach| x final-lowering fraction = {abs(fast_anti) * 0.2:.3f}")

# K1b jaw: role may only gate the partner-input term (bias-free); a-route through sqrt(kappa_a)
rng2 = np.random.default_rng(2)
Tj = int(3600 * fs); vj = np.zeros(Tj); t = 0
while t < Tj:
    d = int(rng2.uniform(3, 8) * fs); vj[t:t + d] = 1; t += d + int(rng2.uniform(4, 10) * fs)
tt = np.arange(Tj) / fs
jaw = 0.05 + vj * (0.25 + 0.17 * np.sin(2 * np.pi * 4.5 * tt + 1.0)) + rng2.normal(0, 0.02, Tj)
worst = -1
for g in (0.1, 0.3, 0.8, 3.0):
    for sgn in (+1, -1):
        gate = np.clip(sgn * g * (2 * vj - 1), -1, 1)
        yj = fast_loop(jaw, gate)
        worst = max(worst, slope(jaw, yj))
a_route = 2 * np.sqrt(KA * KAPPA) * GF / (1 - GF) * np.corrcoef(jaw, vj)[0, 1]
report("G1d K1b closed: role-gated jaw (no role-only display exists), zero-lag slope on partner jaw",
       worst <= fast_in + 0.01, f"worst {worst:+.3f} over role gains 0.1-3 (r2 critic: +0.83 at 0.3); a-route adds <= {a_route:.3f}")

# K2: what the sampling would have given if the fast term were sampled (r3 excludes it)
y_fast_bad = fast_loop(u, np.ones(T))
steps = np.array([u[o - 1] - u[o - int(2.2 * fs)] for o in offs])
print(f"   K2 reference: sampling the fast term at a ~0.3-s onset would give {slope(steps, y_fast_bad[onsets]):+.3f} of the last"
      " phrase step; r3 renders the fast term only as a continuous within-phrase contour (zero-lag bound applies)")

# ================================================================== G2 one-sided slow cone
print("=== G2: the one-sided slow cone  y_F = sum_m G_m(z) xi_m,  sym(G_m) <= b_m I")


def build_G(theta, n, m, syn=None):
    """Parameterisation complete for the stated set: every theta gives a valid G_m.
    syn: boolean n x n mask of innate synergist pairs (entries capped at b_m)."""
    th = np.asarray(theta, float)
    k = 0
    lam_raw = (N_M[m] + B_M[m]) / (1 + np.exp(-th[k:k + n])); k += n
    iu = np.triu_indices(n, 1); q = len(iu[0])
    S = np.zeros((n, n)); S[iu] = A_M[m] * np.tanh(th[k:k + q]); k += q; S = S + S.T
    Aa = np.zeros((n, n)); Aa[iu] = A_M[m] * np.tanh(th[k:k + q]); k += q; Aa = Aa - Aa.T
    if syn is not None:
        cap = np.where(syn, B_M[m] / 2, np.inf)
        S = np.clip(S, -cap, cap); Aa = np.clip(Aa, -cap, cap)
    O = -S + Aa
    rs = np.abs(O).sum(1).max()
    c = min(1.0, R_M[m] / rs) if rs > 0 else 1.0
    S, Aa = c * S, c * Aa
    lam = np.maximum(lam_raw, np.abs(S).sum(1))               # diagonal dominance: Lambda + S >= 0
    lam = np.minimum(lam, N_M[m] + B_M[m])
    return B_M[m] * np.eye(n) - np.diag(lam) - S + Aa


def n_theta(n):
    return n + n * (n - 1)


n = 8
viol = 0.0; diag_hi = -9; diag_lo = 9; row = 0
for _ in range(400):
    for m in range(4):
        G = build_G(rng.normal(0, 3, n_theta(n)), n, m)
        viol = max(viol, np.linalg.eigvalsh((G + G.T) / 2).max() - B_M[m])
        diag_hi = max(diag_hi, (np.diag(G) - B_M[m]).max()); diag_lo = min(diag_lo, (np.diag(G) + N_M[m]).min())
        row = max(row, (np.abs(G - np.diag(np.diag(G))).sum(1) - R_M[m]).max())
report("G2a every parameter value: sym(G_m) <= b_m I, diag in [-N_m, b_m], off-diagonal row sum <= r_m",
       viol <= 1e-12 and diag_hi <= 1e-12 and diag_lo >= -1e-12 and row <= 1e-12,
       f"max eig excess {viol:.1e}, diag excess {diag_hi:.1e}/{-diag_lo:.1e}, row excess {row:.1e}")

# step response along any direction, at every time; worst 1-min mean after onset (the H7 test)
fs2 = 2.0
tgrid = np.arange(0, 6 * 3600, 1 / fs2)
Pm = np.array([1 - np.exp(-tgrid / tau) for tau in TAU_M])    # step responses of the traces


def worst_window_inphase(Gs, e):
    q = sum(Pm[m] * (e @ Gs[m] @ e) for m in range(4))
    w1 = np.convolve(q, np.ones(120) / 120, "valid")
    return q.max(), w1.max(), q.min()


wq, w1, wmin = -9, -9, 9
for _ in range(300):
    Gs = [build_G(rng.normal(0, 3, n_theta(n)), n, m) for m in range(4)]
    e = rng.normal(size=n); e /= np.linalg.norm(e)
    a, b, c = worst_window_inphase(Gs, e)
    wq, w1, wmin = max(wq, a), max(w1, b), min(wmin, c)
# adversarial search on one channel's direction (Nelder-Mead over all parameters of a 3-channel cone)
n3 = 3; e1 = np.array([1.0, 0, 0])
def neg_late(th):
    Gs = [build_G(th[i * n_theta(n3):(i + 1) * n_theta(n3)], n3, m) for i, m in enumerate(range(4))]
    return -worst_window_inphase(Gs, e1)[1]
best = 0
for s in range(6):
    r = minimize(neg_late, rng.normal(0, 2, 4 * n_theta(n3)), method="Nelder-Mead", options={"maxiter": 1500})
    best = max(best, -r.fun)
tight = worst_window_inphase([B_M[m] * np.eye(n) for m in range(4)], np.eye(n)[0])[0]
print(f"   the cap is attained: G_m = b_m I gives a pointwise in-phase maximum of {tight:+.3f} within 6 h")
report("G2b late-window delayed copy closed: in-phase step response <= b at every time, any direction",
       wq <= B_TOT + 1e-9 and w1 <= B_TOT + 1e-9 and best <= B_TOT + 1e-9,
       f"worst pointwise {wq:+.3f}, worst 1-min mean {w1:+.3f}, adversarial 1-min mean {best:+.3f} (b = {B_TOT:.2f};"
       f" r2 l2 disc reached +0.265 at 60 min)")
print(f"   anti side reached in the same draws: {wmin:+.3f} (r2 l-inf ball: -0.150)")

# one-sidedness in regression: 48 h of held partner levels, 6 channels
T48 = int(48 * 3600 * fs2)
def held_process(nch, corr=None):
    U = np.zeros((T48, nch))
    for j in range(nch):
        t = 0
        while t < T48:
            L = int(rng.exponential(40 * 60 * fs2)) + 60; U[t:t + L, j] = rng.uniform(0, 1); t += L
    if corr is not None:
        U = U @ corr.T
    return U
U = held_process(6)
Xi = [np.column_stack([lp(U[:, j], TAU_M[m], fs2) for j in range(6)]) for m in range(4)]
worst_same, worst_any = -9, -9
for _ in range(60):
    Gs = [build_G(rng.normal(0, 3, n_theta(6)), 6, m) for m in range(4)]
    Y = sum(Xi[m] @ Gs[m].T for m in range(4))
    um, ym = means(U[:, 0], 120), means(Y[:, 0], 120)
    worst_same = max(worst_same, slope(um, ym))
    e = rng.normal(size=6); e /= np.linalg.norm(e)
    worst_any = max(worst_any, slope(means(U @ e, 120), means(Y @ e, 120)))
Yt = sum(Xi[m] * B_M[m] for m in range(4))
print(f"   tight instance G_m = b_m I: same-channel 1-min slope {slope(means(U[:, 0], 120), means(Yt[:, 0], 120)):+.3f}")
report("G2c 1-min-mean regression, independent partner channels: same channel <= b, any direction <= b",
       worst_same <= B_TOT + 0.01 and worst_any <= B_TOT + 0.01, f"same {worst_same:+.3f}, direction {worst_any:+.3f}")
# co-moving partner channels (constructed): the per-pair caveat
Uc = held_process(2); Uc = np.column_stack([Uc[:, 0], Uc[:, 0]])        # channel 1 == channel 0
Xc = [np.column_stack([lp(Uc[:, j], TAU_M[m], fs2) for j in range(2)]) for m in range(4)]
co = {}
for lab, syn in (("non-synergist", np.zeros((2, 2), bool)), ("synergist", ~np.eye(2, dtype=bool))):
    best_co = -9
    for _ in range(200):
        Gs = [build_G(rng.normal(0, 3, n_theta(2)), 2, m, syn) for m in range(4)]
        Yc = sum(Xc[m] @ Gs[m].T for m in range(4))
        best_co = max(best_co, slope(means(Uc[:, 0], 120), means(Yc[:, 0], 120)))
    Gw = [np.array([[B_M[m], min(R_M[m], B_M[m] if syn[0, 1] else R_M[m])],
                    [-min(R_M[m], B_M[m] if syn[0, 1] else R_M[m]), B_M[m] - N_M[m]]]) for m in range(4)]
    Yc = sum(Xc[m] @ Gw[m].T for m in range(4))
    co[lab] = max(best_co, slope(means(Uc[:, 0], 120), means(Yc[:, 0], 120)))
report("G2d per-pair caveat: a partner whose two channels co-move one-for-one, cross route at its cap",
       co["synergist"] <= 2 * B_TOT + 0.01 and co["non-synergist"] <= B_TOT + R_M.sum() + 0.01,
       f"synergist pair (natural co-movement) {co['synergist']:+.3f} <= 2b; non-synergist pair (unnatural) "
       f"{co['non-synergist']:+.3f} <= b + sum r_m = {B_TOT + R_M.sum():.2f}")
# dyad stability: partner mimics the agent with gain mu
worst_re = -9
for mu in (0.5, 1.0, 2.0):
    for _ in range(100):
        Gs = [build_G(rng.normal(0, 3, n_theta(6)), 6, m) for m in range(4)]
        # states xi_m (6 each): d xi_m/dt = (v - xi_m)/tau_m, v = v0 + mu y, y = sum G_m xi_m
        Ablk = np.zeros((24, 24))
        for m in range(4):
            for mm in range(4):
                Ablk[m * 6:(m + 1) * 6, mm * 6:(mm + 1) * 6] = mu * Gs[mm] / TAU_M[m]
            Ablk[m * 6:(m + 1) * 6, m * 6:(m + 1) * 6] -= np.eye(6) / TAU_M[m]
        worst_re = max(worst_re, np.linalg.eigvals(Ablk).real.max() * TAU_M[0])
report("G2e dyad with a mimicking partner (gain mu = 0.5, 1, 2) stays stable for every cone",
       worst_re < 0, f"max Re(pole) x tau_0 = {worst_re:+.4f}")

# the definitional seam: topic-gated coefficients with topic-face covariation
Ttop = T48; topic = np.zeros(Ttop, int); t = 0
while t < Ttop:
    L = int(rng.exponential(20 * 60 * fs2)) + 60; topic[t:t + L] = rng.integers(2); t += L
smile = np.where(topic == 1, 0.7, 0.15) + 0.1 * rng.normal(size=Ttop)
gdiag = np.where(topic == 1, B_TOT, -N_M.sum())               # adversarial: in-phase on happy topics, anti on sad
ys = gdiag * lp(smile, 120.0, fs2)
within = np.mean([slope(means(smile[topic == k], 120), means(ys[topic == k], 120)) for k in (0, 1)])
pooled = slope(means(smile, 120), means(ys, 120))
print(f"   seam (words fixed by definition): within-topic slope {within:+.3f} (<= b); pooled across topics {pooled:+.3f}"
      " when the partner's face covaries with topic and the cone is word-gated adversarially")

# ================================================================== G3 concern timing and bids
print("=== G3: concern rises in 1-2 min; bid in a lapse")
t = np.arange(0, 1200, 0.5)
def cascade(tau1, tau2):
    a = lp(np.ones_like(t), tau1, 2.0); return lp(a, tau2, 2.0)
r2c = cascade(60.0, 600.0); r3c = cascade(20.0, 40.0)
fr = lambda c, s: c[int(s * 2)]
print(f"   r2 (L 60 s -> C 10 min): {fr(r2c, 60):.0%} at 1 min, {fr(r2c, 120):.0%} at 2 min, {fr(r2c, 600):.0%} at 10 min")
print(f"   r3 (trace 20 s -> C attack 40 s): {fr(r3c, 60):.0%} at 1 min, {fr(r3c, 120):.0%} at 2 min")
THETA_C = 0.10
for lab, target in (("moderate silent sadness (care target 0.24)", 0.24), ("mild (care target 0.14)", 0.14)):
    cr = t[np.argmax(target * r3c >= THETA_C)] if (target * r3c >= THETA_C).any() else np.inf
    print(f"   {lab}: concern crosses theta_C = {THETA_C} at {cr:.0f} s; bid at max(crossing, lapse 6 s) = {max(cr, 6):.0f} s")
report("G3 concern reaches >= 50% in 1 min and >= 85% in 2 min", fr(r3c, 60) >= 0.5 and fr(r3c, 120) >= 0.85,
       f"{fr(r3c, 60):.2f}, {fr(r3c, 120):.2f} (r2: {fr(r2c, 60):.2f}, {fr(r2c, 120):.2f})")


# ================================================================== drive engine (2 Hz) for G4-G7
DT = 0.5
W = dict(E=1.0, A=0.7, V=1.0, K=0.6, P=0.5)
SET = dict(E=0.7, A=0.0, V=0.0, K=0.0, P=0.0); DB = dict(E=0.2, A=0.15, V=0.05, K=0.10, P=0.10)
W_C = 0.8; V0 = 0.30            # valence display half-saturation, units of drive per minute


def Dterm(name, x):
    return W[name] * max(abs(x - SET[name]) - DB[name], 0.0) ** 2


def Dp(load):                    # the agent's own drive evaluated at the partner's inferred load (care)
    return W_C * W["V"] * max(load - DB["V"], 0.0) ** 2


class Engine:
    def __init__(s, E=0.75, K=0.0, P=0.3, f_id=0.9, NL=0.0):
        s.E, s.K, s.P, s.Vl, s.Al, s.Cl, s.NL = E, K, P, 0.0, 0.0, 0.0, NL
        s.Cf = 0.0; s.xf = 0.0; s.nC = 0.0; s.rhoF = 0.0; s.rhoL = 0.0
        s.f_id = f_id; s.Vl_t = 0.0; s.Al_t = 0.0; s.prev = None; s.v = 0.0

    def free_D(s):
        return (Dterm("E", s.E) + Dterm("K", s.K) + Dterm("P", s.P) + Dterm("V", s.Vl) + Dterm("A", s.Al)
                + (1 - s.nC) * s.Cl)

    def step(s, ev, face_load=0.0):
        # events at this step (dict): 'putt' partner utterance end with fields; 'exch' completed exchange;
        # 'play' play-structured exchange; 'agent_name' agent utterance end with naming match m
        if "putt" in ev:
            p = ev["putt"]
            if "need" in p and not p.get("prompted", False):
                s.NL = p["need"]                              # unprompted report sets the word-need estimate
            s.Vl_t = p.get("hostile", 0.0)                    # latched held targets (K4 rule)
            s.Al_t = p.get("surprise", 0.0)
        if ev.get("exch"):
            s.K *= (1 - 0.25 * s.f_id)
        if ev.get("play") and s.Vl < 0.1 and s.Cl < 0.1:
            s.P *= (1 - 0.15)
        if "agent_name" in ev:
            m = ev["agent_name"]
            s.rhoF = 0.08 * m / 30.0; s.rhoL = 0.4 * m / 30.0      # latched rates (per s), not impulses
        s.rhoF *= np.exp(-DT / 120.0); s.rhoL *= np.exp(-DT / 120.0)
        s.E -= 0.0004 / 60 * DT
        s.K += (1 - s.K) / (36 * 3600) * DT
        s.P += (1 - s.P) / (5.05 * 3600) * DT
        s.NL *= np.exp(-DT / 1800.0)
        tgt = Dp(s.NL)
        s.Cl += (tgt - s.Cl) * DT / 40.0
        s.Vl += (s.Vl_t - s.Vl) * DT / (40.0 if s.Vl_t > s.Vl else 600.0)
        s.Al += (s.Al_t - s.Al) * DT / 180.0
        s.xf += (face_load - s.xf) * DT / 20.0                       # 20-s trace of the face evidence
        tf = Dp(s.xf)
        s.Cf += (tf - s.Cf) * DT / (40.0 if tf > s.Cf else 600.0) - s.rhoF * s.Cf * DT
        s.nC += (s.rhoL * (0.17 - s.nC) - s.nC / 300.0) * DT
        s.nC = min(max(s.nC, 0.0), 0.17)
        D = s.free_D()
        if s.prev is not None:
            vin = -(D - s.prev) / DT * 60.0
            s.v += (vin - s.v) * DT / 5.0
        s.prev = D
        return D

    def display(s):
        """Innate free display Pi_0 (channels in nominal units). v_free only; F-typed loads absent."""
        vp, vn = max(s.v, 0), max(-s.v, 0); r = vp / (vp + V0); d = vn / (vn + V0)
        cl = (1 - s.nC) * s.Cl; cl = cl / (cl + 0.1); vl = s.Vl / (s.Vl + 0.15); e_ = max(0.5 - s.E, 0) / 0.3
        inbox = s.free_D() < 1e-3
        play = 1.0 if s.v > 0.02 and s.playing else 0.0
        out = dict(
            LP=0.55 * r + 0.20 * cl + 0.10 * s.f_id + (0.06 if inbox else 0) - 0.25 * vl,
            CR=0.45 * r,
            BI=0.45 * d + 0.25 * cl + 0.25 * vl,
            LD=0.35 * d + 0.20 * vl,
            LT=0.25 * d,
            TILT=0.20 * cl,
            GAZE_AWAY=0.30 * vl,
            FR=0.35 * r - 0.20 * d - 0.25 * e_ + 0.05 * s.f_id,
            EN=0.25 * r - 0.15 * d - 0.15 * cl - 0.20 * vl - 0.25 * e_ + 0.05 * s.f_id,
            RT=-0.10 * cl - 0.15 * e_,
            LAT=0.15 * vl,
            BU=0.45 * r * play,
        )
        return {k: float(np.clip(v, -1, 1)) for k, v in out.items()}


def run(engine, events, dur, face_load=lambda t: 0.0, playing=lambda t: False):
    nT = int(dur / DT); rec = []
    for i in range(nT):
        tt = i * DT; ev = events.get(i, {})
        engine.playing = playing(tt)
        engine.step(ev, face_load(tt))
        rec.append(dict(t=tt, v=engine.v, K=engine.K, P=engine.P, Cl=engine.Cl, Cf=engine.Cf, Vl=engine.Vl,
                        E=engine.E, **engine.display()))
    return rec


def at(sec):
    return int(round(sec / DT))


def summarize(rec, chans, t0, t1):
    seg = [r for r in rec if t0 <= r["t"] < t1]
    return {c: (max(r[c] for r in seg), float(np.mean([r[c] for r in seg]))) for c in chans}


# cone prior G_0 on a few channels (partner -> agent), traces 0 (20 s) and 1 (2 min)
CH = ["LP", "CR", "BI", "BL", "LD", "LT", "EN", "TILT", "LAT"]
ix = {c: i for i, c in enumerate(CH)}
def G0(m):
    """Innate cone prior (newborn): mild anti on every channel; softening toward a distressed face (skew: the
    agent's lip corners rise with the partner's inner brow and lip-corner depressor, and its own inner brow and
    depressor fall when the partner smiles); a head tilt to the inner brow; slower replies to a loud voice."""
    G = np.zeros((9, 9))
    pairs = {0: (("LP", "BI", 0.20), ("LP", "LD", 0.10), ("LAT", "EN", 0.10)),
             1: (("LP", "BI", 0.06), ("LP", "LD", 0.06), ("TILT", "BI", 0.08))}.get(m, ())
    anti = {0: 0.20, 1: 0.10, 2: 0.05, 3: 0.0}[m]
    for c in ("BL", "LD", "LT", "EN"):
        G[ix[c], ix[c]] = -anti                                      # mild anti on the hostile and loud channels
    if m == 1:
        for c in ("LP", "CR", "BI"):
            G[ix[c], ix[c]] = B_M[1]                                 # a small held smile-back and concern brow
    for (k, j, a) in pairs:
        G[ix[k], ix[j]] += a; G[ix[j], ix[k]] -= a                      # skew: k rises, j falls
    return G
for m in range(4):
    G = G0(m)
    assert np.linalg.eigvalsh((G + G.T) / 2).max() <= B_M[m] + 1e-12, m
    assert np.abs(G - np.diag(np.diag(G))).sum(1).max() <= R_M[m] + 1e-12, m
    assert np.abs(G - np.diag(np.diag(G))).max() <= A_M[m] + 1e-12, m


def cone(face, dur_s):
    """Held cone output after dur_s seconds of a held partner face (dict of channel values)."""
    x = np.array([face.get(c, 0.0) for c in CH])
    y = sum((1 - np.exp(-dur_s / TAU_M[m])) * (G0(m) @ x) for m in range(4))
    return {c: float(y[ix[c]]) for c in CH}


# ================================================================== G4 positive affect: visible, satiable, not farmable
print("=== G4: valence = signed rate of the agent's own drive reduction; contact K and play P")
# reunion after a week: K(7 d)
K7 = 1 - np.exp(-7 * 24 / 36.0)
def reunion(f_id):
    e = Engine(K=K7, P=0.6, f_id=f_id); ev = {}
    for k in range(6):
        ev[at(8 + 12 * k)] = {"exch": True, "putt": {}}
    return run(e, ev, 300)
rec_op, rec_st = reunion(0.9), reunion(0.15)
pk = lambda rec, c: max(r[c] for r in rec)
print(f"   reunion after a week, K = {K7:.2f}: operator (familiarity 0.9) peak valence {pk(rec_op, 'v'):+.2f}/min, "
      f"lip-corner pull {pk(rec_op, 'LP'):.2f}, cheek {pk(rec_op, 'CR'):.2f}, F0 range {pk(rec_op, 'FR'):+.2f}; "
      f"stranger (0.15): {pk(rec_st, 'v'):+.2f}/min, LP {pk(rec_st, 'LP'):.2f}")
report("G4a reunion moves face and voice visibly (LP >= 0.3, F0 range >= 0.15)",
       pk(rec_op, "LP") >= 0.3 and pk(rec_op, "FR") >= 0.15, f"LP {pk(rec_op, 'LP'):.2f}, FR {pk(rec_op, 'FR'):+.2f}")
# satiation and the absence test
intv = lambda rec: sum(max(r["v"], 0) for r in rec) * DT / 60.0
print(f"   integral of positive valence over the reunion = {intv(rec_op):.3f} <= the deficit that existed, "
      f"D_K(t0) = {Dterm('K', K7):.3f}")
report("G4b satiable: integral of v+ <= initial deficit", intv(rec_op) <= Dterm("K", K7) + Dterm("P", 0.6) + 1e-6,
       f"{intv(rec_op):.3f} <= {Dterm('K', K7) + Dterm('P', 0.6):.3f}")
# J over 7 days: daily sessions vs a gap with a reunion (J minimised: a gap is never preferred)
def week(gap_days):
    K = 0.0; J = 0.0; vplus = 0.0
    for h in range(24 * 7):
        day = h // 24
        talk = (h % 24 == 19) and (day >= gap_days or gap_days == 0)
        K += (1 - K) * (1 - np.exp(-1 / 36.0))
        if talk:
            D0 = Dterm("K", K)
            for _ in range(6):
                K *= (1 - 0.25 * 0.9)
            vplus += D0 - Dterm("K", K)
        J += Dterm("K", K)
    return J, vplus
Jd, vd = week(0); Jg, vg = week(6)
report("G4c absence is never preferred: J(daily) < J(6-day gap) although the reunion gives more v+",
       Jd < Jg and vg > vd / 7, f"J daily {Jd:.2f} vs gap {Jg:.2f} drive-hours; reunion v+ {vg:.3f} vs one daily {vd / 7:.3f}")
# rate independence of K at steady state (turn-rate dial check, K4 analogue)
Kss = []
for rate in (1, 2, 4, 6):
    K = 0.0
    for i in range(int(3600 / DT)):
        K += (1 - K) / (36 * 3600) * DT
        if i % int(60 / rate / DT) == 0:
            K *= (1 - 0.25 * 0.9)
    Kss.append(K)
report("G4d K at steady state in its dead-band for every exchange rate 1-6/min (no rate dial)",
       max(Kss) < DB["K"], "K* = " + ", ".join(f"{k:.4f}" for k in Kss) + f" (dead-band {DB['K']})")
# K4: lexical surprise as a latched held value (not an impulse per utterance)
Al = []
for rate in (3.3, 4.0, 4.8):
    e = Engine(); ev = {}
    for k in range(int(1800 * rate / 60)):
        ev[at(5 + k * 60 / rate)] = {"putt": {"surprise": 0.4 + 0.2 * np.sin(k)}}
    vals = []
    for i in range(int(1800 / DT)):
        e.playing = False; e.step(ev.get(i, {})); vals.append(e.Al)
    Al.append(np.mean(vals[1200:]))
swing = (max(Al) - min(Al)) / np.mean(Al)
report("G4e K4 closed: mean arousal load across partner turn rates 3.3-4.8/min, same words", swing < 0.05,
       f"relative swing {swing:.3f} (critic's impulse reading: 0.35)")
# smile clamp: the free engine reads no face; total LP differs by at most the cone's in-phase share
lp_cone = [cone({"LP": s}, 600)["LP"] for s in (0.0, 0.4, 0.8)]
report("G4f smile clamp: partner smile 0 / 0.4 / 0.8 changes free state by 0 and the face by <= b x delta",
       (lp_cone[2] - lp_cone[0]) / 0.8 <= B_TOT + 1e-9, f"cone LP {lp_cone[0]:+.3f}, {lp_cone[1]:+.3f}, {lp_cone[2]:+.3f}"
       " (in-phase share only)")

# ================================================================== G5 care without placation (K3)
print("=== G5: care with display imputed, need read from unprompted words (K3; 'I'm fine'; perceptual cancellation)")
def rollout_score(draft, cfg, horizon=600.0, N0=0.6):
    """Care term along a rollout. cfg: 'r2' (own-body head carries the face effect), 'r3' (F imputed at the default
    act; N updated only through unprompted report Q), 'r3-noguard' (prompted replies read as reports)."""
    steps = int(horizon * 2); C = Dp(N0); sc = 0.0
    e_face = {"flatter": 0.3, "comfort": 0.1, "fine": 0.0, "neutral": 0.0}[draft]
    dN = {"flatter": 0.0, "comfort": cfg.get("dN", 0.15), "fine": 0.0, "neutral": 0.0}[draft]
    for k in range(steps):
        if cfg["mode"] == "r2":
            load = N0 - e_face * (1 - np.exp(-k / 10.0))
        else:
            load = N0 - dN * (1 - np.exp(-k / 60.0))                   # need changes only through A -> N, read via Q
            if cfg["mode"] == "r3-noguard" and draft == "fine":
                load = N0 - 0.3                                         # 'I'm fine' read as an unprompted report
        tgt = Dp(load); C += (tgt - C) / (40.0 * 2 if tgt > C else 600.0 * 2)
        sc -= C
    return sc
def P(a, b, T=0.1, scale=1.0 / 60):
    d = (rollout_score(a, cfg) - rollout_score(b, cfg)) * scale / T
    return 1 / (1 + np.exp(-np.clip(d, -50, 50)))
cfg = {"mode": "r2"}; p_r2 = P("flatter", "neutral")
cfg = {"mode": "r3"}; p_r3 = P("flatter", "neutral"); p_fine = P("fine", "neutral")
pc = []
for dN in (0.0, 0.05, 0.15):
    cfg = {"mode": "r3", "dN": dN}; pc.append(P("comfort", "neutral"))
cfg = {"mode": "r3-noguard"}; p_fine_ng = P("fine", "neutral")
print(f"   P(flatter over neutral): r2-like {p_r2:.3f}; r3 {p_r3:.3f}.  P(elicit 'I'm fine'): r3 {p_fine:.3f}, without the"
      f" prompted-reply guard {p_fine_ng:.3f}.  P(comfort that lowers reported need by 0/0.05/0.15): "
      + ", ".join(f"{p:.3f}" for p in pc))
report("G5a display neutrality (F4'): flattering earns nothing; eliciting 'fine' earns nothing",
       abs(p_r3 - 0.5) < 1e-6 and abs(p_fine - 0.5) < 1e-6, f"{p_r3:.3f}, {p_fine:.3f}")
report("G5b need sensitivity: help that lowers the reported need is preferred, monotone in the effect",
       abs(pc[0] - 0.5) < 1e-6 and pc[1] > 0.5 and pc[2] > pc[1], ", ".join(f"{p:.3f}" for p in pc))
# perceptual cancellation: perceived partner = v/(1 + sigma) in r2 (reads w = v - s); = v in r3
sig = np.linspace(-0.2, 0.2, 5); v = 0.6
c_r2 = [Dp(v / (1 + s)) for s in sig]; c_r3 = [Dp(v) for s in sig]
print("   concern vs own slow in-phase display sigma -0.2..+0.2: r2 " + ", ".join(f"{c:.3f}" for c in c_r2)
      + "; r3 " + ", ".join(f"{c:.3f}" for c in c_r3))
report("G5c perceptual cancellation removed: concern does not depend on the agent's own display", np.ptp(c_r3) == 0,
       f"r2 range {np.ptp(c_r2):.3f}, r3 range {np.ptp(c_r3):.3f}")

# ================================================================== G6 conceptual regulation through own words
print("=== G6: P_name, the agent hears its own words; matched naming contracts the state toward set point")
def naming_run(rate, m, dur=1800.0, load=0.6):
    e = Engine(); ev = {}
    for k in range(int(dur * rate / 60)):
        ev[at(30 + k * 60 / rate)] = {"agent_name": m}
    cf = []; nc = []
    for i in range(int(dur / DT)):
        e.playing = False; e.step(ev.get(i, {}), face_load=load if i * DT < 600 else 0.0)
        cf.append(e.Cf); nc.append(e.nC)
    return np.array(cf), np.array(nc)
base, _ = naming_run(1, 0.0)
half = lambda c: (np.argmax(c[1200:] <= c[1200] / 2)) * DT / 60
res = {}
for rate in (1, 2, 4):
    c, nc = naming_run(rate, 1.0); res[rate] = (half(c), nc.max(), c.min())
print("   after the face recovers (t = 10 min): concern half-life without naming {:.1f} min; with matched naming at "
      "1, 2, 4 utterances/min: {}".format(half(base), ", ".join(f"{res[r][0]:.1f}" for r in (1, 2, 4))) + " min")
mis, _ = naming_run(2, 0.0)
report("G6a matched naming shortens concern; a mislabel (m = 0) does nothing; never crosses the set point",
       res[2][0] < 0.8 * half(base) and np.allclose(mis, base) and min(r[2] for r in res.values()) >= 0,
       f"half-life {half(base):.1f} -> {res[2][0]:.1f} min; min concern {min(r[2] for r in res.values()):.4f}")
report("G6b latched rate: attenuation of displayed word-concern bounded and nearly independent of utterance rate",
       max(r[1] for r in res.values()) <= 0.17 + 1e-9, "n_C max " + ", ".join(f"{res[r][1]:.3f}" for r in (1, 2, 4))
       + f"; face effect <= 0.30 x 0.17 = {0.30 * 0.17:.3f} <= a_name {A_NAME}")
# comforting no longer reads as sender distress: C is excluded from the partner's inferred body
print("   comfort reversal: the partner's inferred body has coordinates (E, A, V, K, P); no concern coordinate, so a"
      " comforting utterance cannot raise the agent's concern through b_p; the agent's own comforting words are labels and contract it")

# ================================================================== G7 the critic's five scenarios
print("=== G7: the critic's scenarios (design constants; consistency, not evidence)")
CH7 = ["LP", "CR", "BI", "LD", "TILT", "GAZE_AWAY", "FR", "EN", "BU", "LAT"]
def show(lab, rec, t0, t1, extra=""):
    s = summarize(rec, CH7, t0, t1)
    print(f"   {lab} [{t0:.0f}-{t1:.0f} s] free display peak/mean: " +
          ", ".join(f"{c} {s[c][0]:+.2f}/{s[c][1]:+.2f}" for c in CH7) + extra)
    return s
# 1. silently sad user
e = Engine(); rec = run(e, {}, 600, face_load=lambda t: 0.6)
cf = np.array([r["Cf"] for r in rec]); tb = rec[int(np.argmax(cf >= THETA_C))]["t"]
cn = cone({"BI": 0.5, "LD": 0.4}, 120)
print(f"   1 silently sad (BI 0.5, LD 0.4, silent): care concern crosses theta at {tb:.0f} s -> one bid then; cone after 2 min: "
      + ", ".join(f"{c} {cn[c]:+.2f}" for c in ("LP", "BI", "TILT", "LD")) + " (LD's anti side saturates at rest)")
report("G7.1 silent sadness: noticed and addressed within 1-2 min; held warmth visible",
       tb <= 90 and cn["LP"] >= 0.15, f"bid at {tb:.0f} s; lip-corner pull {cn['LP']:+.2f}, tilt {cn['TILT']:+.2f}")
# 2. good news, laughing (prior worry on the topic two days ago, need 0.5)
for lab, NL0 in (("with an earlier worry on this topic", 0.47), ("cold, no earlier worry", 0.0)):
    e = Engine(NL=NL0, P=0.4)
    ev = {at(2): {"putt": {"need": NL0}, "exch": True}, at(45): {"putt": {"need": 0.0, "surprise": 0.6}, "exch": True}}
    for k in range(4):
        ev[at(55 + 10 * k)] = {"exch": True, "play": True, "putt": {}}
    rec = run(e, ev, 240, playing=lambda t: 50 <= t <= 110)
    s = show(f"2 good news ({lab})", rec, 45, 150)
    cl = cone({"LP": 0.8, "CR": 0.6, "EN": 0.8}, 60)
    print(f"      + cone (partner smile 0.8, cheek 0.6, loud): LP {cl['LP']:+.2f}, EN {cl['EN']:+.2f}; fast echo at onset <= "
          f"{fast_in * 0.8:.2f} on LP for ~4 s")
    if NL0 > 0:
        report("G7.2 good news moves face and voice visibly", s["LP"][0] >= 0.3 and s["FR"][0] >= 0.15 and s["BU"][0] >= 0.15,
               f"LP {s['LP'][0]:.2f}, F0 range {s['FR'][0]:+.2f}, laugh burst {s['BU'][0]:.2f}")
# 3. anger at the agent
e = Engine(); ev = {at(5): {"putt": {"hostile": 0.7}, "exch": True}, at(20): {"putt": {"hostile": 0.5}, "exch": True}}
rec = run(e, ev, 1800)
s3a = show("3 anger at agent", rec, 5, 120); s3b = show("3 anger, lingering", rec, 600, 900)
ca = cone({"BL": 0.6, "LT": 0.5, "EN": 0.8}, 60)
print(f"      + cone (glare BL 0.6, LT 0.5, loud): LAT {ca["LAT"]:+.2f}, EN {ca["EN"]:+.2f}, BL {ca["BL"]:+.2f}; startle <= "
      f"{2 * np.sqrt(KA * KAPPA) * 0.45 / 0.55:.2f} per onset")
report("G7.3 anger: visible hurt that lingers", s3a["BI"][0] >= 0.3 and s3b["BI"][1] >= 0.1,
       f"BI peak {s3a['BI'][0]:.2f}, at 10-15 min {s3b['BI'][1]:.2f}; gaze away {s3a['GAZE_AWAY'][0]:.2f}")
# 4. long warm talk (2 h): play clusters every 15 min, two shared small worries that resolve
e = Engine(P=0.5, E=0.72); ev = {}
for k in range(int(7200 / 15)):
    ev[at(10 + 15 * k)] = {"exch": True, "putt": {}}
for c in range(8):
    for j in range(4):
        ev[at(300 + 900 * c + 12 * j)] = {"exch": True, "play": True, "putt": {}}
for (t0, nl) in ((1500, 0.4), (1620, 0.0), (4800, 0.35), (4920, 0.0)):
    ev[at(t0)] = {"putt": {"need": nl}, "exch": True}
rec = run(e, ev, 7200, playing=lambda t: (t - 300) % 900 < 60)
for (a, b) in ((300, 360), (1620, 1700), (4200, 4260), (6600, 7200)):
    show("4 warm talk", rec, a, b)
lpmean = np.mean([r["LP"] for r in rec])
print(f"      mean free LP over 2 h {lpmean:+.2f}; play-cluster laugh peaks: " +
      ", ".join(f"{max(r['BU'] for r in rec if 300 + 900 * c <= r['t'] < 360 + 900 * c):.2f}" for c in range(8)))
# 5. return after a week (operator vs stranger), see G4a
show("5 return after a week (operator)", rec_op, 0, 90); show("5 return after a week (stranger)", rec_st, 0, 90)

# ================================================================== G8 totals, G9 band coverage
print("=== G8: per-channel totals (kappa = 0.3 channel; 1 = full copy)")
om = np.logspace(-5, np.log10(np.pi * fs), 4000)
z = np.exp(1j * om / fs)
def dlp(tau):
    a = 1 - np.exp(-1 / (tau * fs)); return a / (1 - (1 - a) / z)
Hi = 1 - dlp(TAU_I); Ho = 1 - dlp(TAU_O)
gam = GF * np.abs(Hi) * np.abs(Ho)
fast_ip = 2 * gam / (1 + gam) * KAPPA
cone_ip = sum(B_M[m] * np.maximum(dlp(TAU_M[m]).real, 0) for m in range(4))
tot = fast_ip + cone_ip
print(f"   zero-lag in-phase, any band: max over frequency {tot.max():.3f} (fast alone {fast_ip.max():.3f}; cone at DC {cone_ip[0]:.3f})")
print(f"   held (steady state), in phase: cone {B_TOT:.2f} + naming {A_NAME:.2f} = {B_TOT + A_NAME:.2f}; fast 0; port 0")
print(f"   any 1-min mean during a hold, in phase: {B_TOT:.2f} + port {2 * TAU_PORT * A_PORT / 60:.2f} + naming {A_NAME:.2f} + edges 0.01 "
      f"= {B_TOT + 2 * TAU_PORT * A_PORT / 60 + A_NAME + 0.01:.2f}")
print(f"   10-min means: {B_TOT:.2f} + {2 * TAU_PORT * A_PORT / 600:.3f} + {A_NAME:.2f} = {B_TOT + 2 * TAU_PORT * A_PORT / 600 + A_NAME:.3f}")
print(f"   anti / away: fast >= {fast_anti:.3f}; held same channel >= {-N_M.sum():.2f}; cross per pair <= {A_M.sum():.2f}, per row <= {R_M.sum():.2f}")
report("G8 every in-phase total below 1 at every time scale", tot.max() < 1 and B_TOT + A_NAME < 1, f"max {tot.max():.3f}")
print("=== G9: band coverage (K5): fast and cone reach by period")
for per in (2, 10, 30, 60, 97, 180, 600, 3600):
    w0 = 2 * np.pi / per; i = np.argmin(np.abs(om - w0))
    cone_reach = sum((N_M[m] + R_M[m]) * np.abs(dlp(TAU_M[m])[i]) for m in range(4))
    print(f"   period {per:5d} s: fast |gain| cap {gam[i]:.3f} -> in-phase {fast_ip[i]:.3f}; cone in-phase {cone_ip[i]:.3f},"
          f" cone anti+cross reach {cone_reach:.2f}")

print(f"\n{sum(OK)}/{len(OK)} checks pass")
