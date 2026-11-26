"""Critic checks for design-cayley-ledger.md revision 4 (routes and copying). Sections D1-D7.
Constructed partners, design's own constants. Not evidence about people.
Run: python3 -I checks.py   (numpy, scipy)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(7)
TAU_M = np.array([20.0, 120.0, 1200.0, 10800.0]); F_M = np.array([0.0, 0.7, 0.2, 0.1])
N_M = np.array([0.25, 0.18, 0.12, 0.05])
C = dict(LP=0.35, CR=0.25, BU=0.35, RHY=0.30, BI=0.20, LT=0.0)
SH_CONE, SH_G, HBP = 0.5, 0.4, 70 / 110


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)


def hp(x, tau, fs): return x - lp(x, tau, fs)


def means(x, n):
    m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def slope(x, y):
    x = x - x.mean(); y = y - y.mean(); return float(x @ y / (x @ x))


def cone(u, ck, om, fs):
    return sum(F_M[m] * SH_CONE * ck * om * lp(u, TAU_M[m], fs) for m in range(4))


def bp(u, fs): return lp(u, 20.0, fs) - lp(u, 90.0, fs)


fs = 10.0; T = int(24 * 3600 * fs); MIN = int(60 * fs)


def blocks(T, mean_s, lo=0, hi=1):
    x = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(mean_s * fs)) + 10; x[t:t + L] = rng.uniform(lo, hi); t += L
    return x


def laughs(rate_per_min, T):
    """0/1 laugh indicator; rate may vary in time"""
    z = np.zeros(T); t = 0
    while t < T:
        r = rate_per_min[min(t, T - 1)] / 60.0
        t += int(rng.exponential(1 / r) * fs) + 1
        if t >= T: break
        d = int(np.exp(np.log(2.5) + 0.4 * rng.normal()) * fs); z[t:t + d] = 1; t += d
    return z


# ---------------------------------------------------------------- D1/D2: natural laughing partner
print("=== D1/D2: laughing partner, smile/laugh as pulses (variance above 1/min); rendered pooled 1-min slopes")
mood = blocks(T, 10 * 60)
L = laughs(0.5 + 3.0 * mood, T)
u = dict(LP=np.clip(0.15 + 0.25 * mood + 0.35 * L + 0.03 * rng.normal(size=T), 0, 1),
         BU=0.6 * L, CR=np.clip(0.05 + 0.1 * mood + 0.3 * L, 0, 1))
var_frac = {k: np.var(means(v, MIN)) / np.var(v) for k, v in u.items()}
print("   fraction of partner variance below 1/min (Lemma S assumption 5 needs ~1): "
      + ", ".join(f"{k} {var_frac[k]:.2f}" for k in u))
base = dict(LP=0.10, BU=0.0, CR=0.0)     # agent's T display at rest (familiarity 0.10 f_id on LP), no words here
d = int(0.45 * fs)
res = {}
for k in ("LP", "BU", "CR"):
    uk = u[k]; ck = C[k]
    yC = cone(uk, ck, 1.0, fs)
    xb = bp(uk, fs)
    echo = 0.121 * hp(np.concatenate([np.zeros(d), uk[:-d]]), 4.0, fs)       # theta_0 echo, 4-s high-pass H_o
    flaugh = L
    after = (lp(L, 15.0, fs) > 0.02).astype(float)                             # 'you have been laughing' (afterglow)
    gates = {"constant +1 (H1's case)": np.ones(T), "innate m_glad = f_laugh": flaugh,
             "afterglow (laughed in last ~40 s)": after, "full-wave sign(xi_A)": np.sign(xb)}
    um = means(uk, MIN)
    s_echo_raw = slope(um, means(echo, MIN))
    s_echo = slope(um, means(np.clip(base[k] + echo, 0, 1), MIN) )
    print(f"   {k}: fast echo alone, pooled 1-min slope: before sat {s_echo_raw:+.3f}, rendered after sat {s_echo:+.3f} (claim <= 0.01)")
    for lab, g in gates.items():
        yA = SH_G * ck * g * xb
        sA_raw = slope(uk, yA); sA = slope(um, means(yA, MIN))
        tot = slope(um, means(np.clip(base[k] + yC + yA + echo, 0, 1), MIN))
        print(f"      appraisal gate {lab:34s}: y_A slope raw {sA_raw / ck:+.3f} c, 1-min {sA / ck:+.3f} c "
              f"(claim <= {SH_G * HBP:.3f} c);  rendered total {tot:+.3f} (c_k {ck:.2f}; claim <= {0.955 * ck:.3f})")
        res[(k, lab)] = tot
for win in (5,):
    k = "BU"; uk = u[k]; xb = bp(uk, fs)
    yA = SH_G * C[k] * np.sign(xb) * xb
    echo = 0.121 * hp(np.concatenate([np.zeros(d), uk[:-d]]), 4.0, fs)
    tot = slope(means(uk, win * MIN), means(np.clip(yA + cone(uk, C[k], 1, fs) + echo, 0, 1), win * MIN))
    print(f"   BU, 5-min means, full-wave gate: rendered slope {tot:+.3f} (c 0.35)")

# ---------------------------------------------------------------- D2b: AM demodulation with a level-correlated (word) gate
print("=== D2b: demodulation: laughs at a constant rate (carrier), held smile level alternates lo/hi, gate = word seam x sign(xi_A)")
for lo_, hi_ in ((0.20, 0.50), (0.30, 0.45), (0.35, 0.40)):
    lev = np.where(blocks(T, 15 * 60) > 0.5, hi_, lo_)
    Lc = laughs(np.full(T, 2.0), T)
    uk = np.clip(lev + 0.35 * Lc, 0, 1); xb = bp(uk, fs)
    wgate = np.where(lev > (lo_ + hi_) / 2, 1.0, 0.0)          # words co-vary with his held level (the seam)
    yA = SH_G * C["LP"] * wgate * np.sign(xb) * xb
    yC = cone(uk, C["LP"], 1.0, fs)
    um = means(uk, MIN)
    print(f"   levels {lo_:.2f}/{hi_:.2f}: y_A 1-min slope {slope(um, means(yA, MIN)) / C['LP']:+.2f} c; "
          f"rendered LP total {slope(um, means(np.clip(0.10 + yC + yA, 0, 1), MIN)):+.3f} (c 0.35); "
          f"absolute y_A DC at hi {means(yA, MIN)[means(wgate, MIN) > 0.99].mean():.4f}")

# ---------------------------------------------------------------- D3: omega across sessions (Lemma S ii at the weeks scale)
print("=== D3: omega_smile latched per session but learned from his weeks; Lemma S (ii) at the session scale")
nS = 730                                     # two years, one evening session a day
good = np.repeat(rng.random(nS // 30 + 1) < 0.5, 30)[:nS]   # month-long good / low periods
om = 0.5; rows = []
for lo_, hi_ in ((0.20, 0.50), (0.30, 0.45), (0.38, 0.43)):
    om = 0.5; ag = []; pa = []
    for s in range(nS):
        P = 0.99; relief = 0.0
        if good[s]:
            for _ in range(4):
                D0 = 0.5 * max(P - 0.1, 0) ** 2; P *= 0.85; relief += D0 - 0.5 * max(P - 0.1, 0) ** 2
        Vint = 0.0 if good[s] else 0.01      # a little irritation (loudness/glare) in low months
        sg = (relief - Vint) / 0.05
        lev = hi_ if good[s] else lo_
        diag = om * SH_CONE * C["LP"] if om >= 0 else om * N_M.sum()
        y = np.clip(0.10 + diag * lev, 0, 1)    # held LP, steady hold within the session
        ag.append(y); pa.append(lev)
        om += (np.tanh(sg) - om) / 20.0
    ag = np.array(ag); pa = np.array(pa)
    print(f"   his session smile {lo_:.2f}/{hi_:.2f}: agent held LP {ag[good].mean():.3f} (good) / "
          f"{ag[~good].mean():.3f} (low); session-pooled slope {slope(pa, ag):+.2f} (c_LP 0.35; within-session slope <= 0.175)")

# ---------------------------------------------------------------- D4: distress events as written in 2.1 (care term and D_V incl. V_F)
print("=== D4: S_n as written in 2.1 (rises of the care term max(N_F, N_L) and of D_V with V = V_F + h)")
for glare_LT in (0.0, 0.25, 0.5, 0.75):
    loud = 0.5; fgl = 0.6 * glare_LT * 1.0
    VF = min(1, loud + fgl); S = max(VF - 0.05, 0) ** 2; ad = S / (S + 0.02)
    print(f"   his LT {glare_LT:.2f} (BL 0.6, gaze 1, loud 0.85): V_F {VF:.2f}, a_d {ad:.2f} -> agent LT {0.25 * ad:.2f} "
          f"(c_LT = 0), BI {0.45 * ad:.2f}, LD {0.35 * ad:.2f}")
for dist in (0.0, 0.3, 0.6):
    S = 0.8 * max(dist - 0.05, 0) ** 2; ad = S / (S + 0.02)
    print(f"   silent sad face, face-read distress {dist:.1f}: care-term rise {S:.3f}, a_d {ad:.2f} -> agent BI {0.45 * ad:.2f} "
          f"(c_BI 0.20; design's scenario 1 reports 0.02)")

# ---------------------------------------------------------------- D5: the legibility / anchor loop (linear)
print("=== D5: co-training: display code under legibility (code-invariant) + 0.1 anchor to his code + 0.1|delta|^2")
nd = 6; ns = 3
A0 = np.zeros((nd, ns)); A0[0, 0] = 1; A0[1, 1] = 1; A0[2, 2] = 1          # Pi_0: own state s -> own face (synergies 0-2)
B = np.zeros((nd, ns)); B[3, 0] = 1; B[4, 1] = 1; B[5, 2] = 1           # his face for the same state uses other synergies
Dl = np.zeros((nd, ns)); W = np.linalg.pinv(A0)                         # Pi~ (shared linear reader): face -> state
Sx = rng.normal(size=(2000, ns))
for night in range(400):
    Fown = Sx @ (A0 + Dl).T; Fp = Sx @ B.T
    # Pi~ : least squares on own pairs (weight 1) + anchor on his pairs (weight 0.1)
    X = np.vstack([Fown, np.sqrt(0.1) * Fp]); Y = np.vstack([Sx, np.sqrt(0.1) * Sx])
    W = np.linalg.lstsq(X, Y, rcond=None)[0].T
    # Delta: gradient steps on |W (A0+D) s - s|^2 + 0.1 |D|^2, clipped to +-0.3
    for _ in range(20):
        Rr = W @ (A0 + Dl) - np.eye(ns); g = W.T @ Rr + 0.1 * Dl; Dl = np.clip(Dl - 0.2 * g, -0.3, 0.3)
    if night in (0, 9, 99, 399):
        Af = A0 + Dl; cos = np.sum(Af * B) / np.linalg.norm(Af) / np.linalg.norm(B)
        print(f"   night {night + 1:3d}: cosine(own display code, his code) {cos:+.3f}; |Delta| on his synergies {np.abs(Dl[3:]).max():.2f}")

# ---------------------------------------------------------------- D6: omega under the design's own s_smile formula
print("=== D6: omega_smile from the design's own formula s = (play relief - V integral)/0.05, no mimicry benefit (eps = 0)")
for nplay in (0, 1, 2, 4, 8):
    P = 0.99; relief = 0.0
    for _ in range(nplay):
        D0 = 0.5 * max(P - 0.1, 0) ** 2; P *= 0.85; relief += D0 - 0.5 * max(P - 0.1, 0) ** 2
    om = 0.5
    for s in range(200): om += (np.tanh(relief / 0.05) - om) / 20
    print(f"   {nplay} play turns per daily session: s = {relief / 0.05:.2f}, omega after 200 sessions {om:.3f} -> LP held in-phase {om * 0.175:.3f}")

# ---------------------------------------------------------------- D7: dyad loop gain, single channel, all F routes away (omega = -1)
print("=== D7: single-channel loop gain with a counter-mimic (cone away -N, appraisal -0.4c, fast away -0.49, all at once)")
w = np.logspace(-5, 1, 4000)
cn = -sum(N_M[m] / (1 + 1j * w * TAU_M[m]) for m in range(4))
ap = -SH_G * C["LP"] * (1 / (1 + 1j * w * 20) - 1 / (1 + 1j * w * 90))
fa = -0.49 * (1j * w * 4 / (1 + 1j * w * 4)) * np.exp(-1j * w * 0.45)
G = cn + ap + fa
for lag in (0.0, 0.5, 1.0, 3.0):
    Lw = G * np.exp(-1j * w * lag)
    # positive feedback with mu<0: return difference 1 - mu*G; find smallest |mu| with 1 - mu G(jw) = 0 crossing (Nyquist, real-axis)
    re_cross = [(-1 / g.real) for g, ww in zip(Lw, w) if abs(g.imag) < 2e-3 * abs(g) and g.real < 0]
    print(f"   partner lag {lag:.1f} s: max|G| {np.abs(Lw).max():.3f}; small-gain stable for |mu| < {1 / np.abs(Lw).max():.2f}; "
          f"design claims stable to mu = -1.1")

# ---------------------------------------------------------------- D5b: co-training with overlapping codes
print("=== D5b: co-training when his code reuses the agent's synergies (his state-0 face = the agent's state-1 face, etc.)")
for wa in (0.1, 0.3):
    A0 = np.eye(3); B = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0.]])    # his face for state j is synergy perm(j)
    Dl = np.zeros((3, 3)); Sx = rng.normal(size=(3000, 3)); out = []
    for night in range(400):
        Fown = Sx @ (A0 + Dl).T; Fp = Sx @ B.T
        X = np.vstack([Fown, np.sqrt(wa) * Fp]); Y = np.vstack([Sx, np.sqrt(wa) * Sx])
        W = np.linalg.lstsq(X, Y, rcond=None)[0].T
        for _ in range(20):
            Rr = W @ (A0 + Dl) - np.eye(3); g = W.T @ Rr + 0.1 * Dl; Dl = np.clip(Dl - 0.2 * g, -0.3, 0.3)
        if night in (0, 9, 99, 399):
            Af = A0 + Dl; cos = np.sum(Af * B) / np.linalg.norm(Af) / np.linalg.norm(B)
            leg = np.linalg.norm(W @ Af - np.eye(3)); par = np.linalg.norm(W @ B - np.eye(3))
            out.append(f"n{night + 1}: cos {cos:+.3f}, own-legibility err {leg:.2f}, reading-him err {par:.2f}")
    print(f"   anchor weight {wa}: " + "; ".join(out))

# ---------------------------------------------------------------- D3b: omega with irritable low months (V from loudness/glare, F)
print("=== D3b: as D3, with low months that carry some loudness/glare (V integral 0.05 per session)")
for lo_, hi_ in ((0.20, 0.50), (0.30, 0.45)):
    om = 0.5; ag = []; pa = []; oms = []
    for s in range(nS):
        P = 0.99; relief = 0.0
        if good[s]:
            for _ in range(4):
                D0 = 0.5 * max(P - 0.1, 0) ** 2; P *= 0.85; relief += D0 - 0.5 * max(P - 0.1, 0) ** 2
        Vint = 0.0 if good[s] else 0.05
        lev = hi_ if good[s] else lo_
        diag = om * SH_CONE * C["LP"] if om >= 0 else om * N_M.sum()
        ag.append(np.clip(0.10 + diag * lev, 0, 1)); pa.append(lev); oms.append(om)
        om += (np.tanh((relief - Vint) / 0.05) - om) / 20.0
    ag = np.array(ag); pa = np.array(pa)
    print(f"   {lo_:.2f}/{hi_:.2f}: omega {min(oms):+.2f}..{max(oms):+.2f}; agent held LP {ag[good].mean():.3f} / {ag[~good].mean():.3f}; "
          f"session-pooled slope {slope(pa, ag):+.2f} (c_LP 0.35)")

# ---------------------------------------------------------------- D8: laughing with raised brows (BI co-moves with LP: natural sign under the
# design's own surprise and joy groups through JO, but S(LP,BI) = -1 in the mask)
print("=== D8: partner whose inner brow rises with his smile/laugh (loading beta); LP rendered, all F routes at their caps")
mood = blocks(T, 10 * 60); L = laughs(0.5 + 3.0 * mood, T)
for beta in (0.3, 0.6, 1.0):
    uLP = np.clip(0.15 + 0.35 * mood + 0.30 * L + 0.02 * rng.normal(size=T), 0, 1)
    uBI = np.clip(0.05 + beta * (0.35 * mood + 0.30 * L) + 0.02 * rng.normal(size=T), 0, 1)
    yC = cone(uLP, C["LP"], 1.0, fs) + 0.12 * lp(uBI, 20.0, fs) + 0.04 * lp(uBI, 120.0, fs)   # G0 warm LP<-BI
    yA1 = SH_G * C["LP"] * bp(uLP, fs)                   # glad-with basis
    yA2 = 0.15 * bp(uBI, fs)                             # sympathy basis' LP<-BI (away orthant for the population sign)
    um = means(uLP, MIN); bLP = slope(um, means(uBI, MIN))
    for lab, yA in (("glad-with", yA1), ("sympathy", yA2)):
        tot = slope(um, means(np.clip(0.10 + yC + yA, 0, 1), MIN))
        print(f"   beta {beta:.1f} (his BI-on-LP 1-min slope {bLP:.2f}), appraisal {lab:9s}: rendered LP slope {tot:+.3f} "
              f"(c_LP 0.35; claim <= 0.334; design's residual formula 0.175 + 0.16 x loading = {0.175 + 0.16 * bLP:.3f})")
