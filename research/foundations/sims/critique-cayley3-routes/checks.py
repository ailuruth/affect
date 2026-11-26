"""Critique 3 of design-cayley-ledger.md (revision 3): counterexample checks (C0-C7).

Constructed instances of the design's own equations and constants. Not evidence about people.
Run:  python3 -I checks.py    (numpy, scipy; well under a minute)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(3)


def slope(x, y):
    x = x - x.mean(); y = y - y.mean()
    return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n
    return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs))
    return lfilter([a], [1, -(1 - a)], x)


# design constants (revision 3, section 2.1)
TAU_M = np.array([20.0, 120.0, 1200.0, 10800.0])
B_M = np.array([0.00, 0.05, 0.03, 0.02])
N_M = np.array([0.50, 0.40, 0.30, 0.20])
A_M = np.array([0.25, 0.12, 0.08, 0.04])
R_M = np.array([0.30, 0.15, 0.10, 0.05])
B = B_M.sum()


def in_cone(G, m, syn=None, tol=1e-12):
    """membership test for the design's set G_m (section 2.5)"""
    n = len(G)
    ok = np.linalg.eigvalsh((G + G.T) / 2).max() <= B_M[m] + tol
    d = np.diag(G); ok &= bool((d <= B_M[m] + tol).all() and (d >= -N_M[m] - tol).all())
    O = G - np.diag(d)
    ok &= bool((np.abs(O) <= A_M[m] + tol).all() and (np.abs(O).sum(1) <= R_M[m] + tol).all())
    if syn is not None:
        ok &= bool((np.abs(O[syn]) <= B_M[m] + tol).all())
    return ok


def held(T, mean_s, fs, lo=0.0, hi=1.0):
    x = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(mean_s * fs)) + 4; x[t:t + L] = rng.uniform(lo, hi); t += L
    return x


fs = 2.0
T48 = int(48 * 3600 * fs)
MIN = int(60 * fs)

# =====================================================================================================
print("=== C0: reproduce the design's two caveat numbers (seam 0.56, co-moving pair 0.61)")
topic = np.zeros(T48, int); t = 0
while t < T48:
    L = int(rng.exponential(20 * 60 * fs)) + 60; topic[t:t + L] = rng.integers(2); t += L
smile = np.where(topic == 1, 0.7, 0.15) + 0.1 * rng.normal(size=T48)
ys = np.where(topic == 1, B, -N_M.sum()) * lp(smile, 120.0, fs)
print(f"   seam (design's construction): pooled 1-min slope {slope(means(smile, MIN), means(ys, MIN)):+.3f}")
# the pooled slope is (b*x_hi + N*x_lo)/(x_hi - x_lo) for two held levels: it is not capped at 0.56
for lo_, hi_ in ((0.15, 0.7), (0.3, 0.7), (0.35, 0.75)):
    print(f"   two held smile levels {lo_:.2f}/{hi_:.2f}: closed-form pooled slope of y_F "
          f"{(B * hi_ + N_M.sum() * lo_) / (hi_ - lo_):+.2f}")
s0 = held(T48, 40 * 60, fs)
Xc = [lp(s0, tau, fs) for tau in TAU_M]
y0 = sum((B_M[m] + R_M[m]) * Xc[m] for m in range(4))     # G00 = b_m, G01 = +r_m (skew partner -r_m)
print(f"   co-moving pair at the cap (u1 == u0): agent ch0 1-min slope {slope(means(s0, MIN), means(y0, MIN)):+.3f}")

# =====================================================================================================
print("=== C1: the seam opens without any word-face covariation: T state clocked by the wall clock knows tempo")
# A partner whose held positivity x drives face, voice level and conversational tempo (no words modelled:
# the transcript and the turn ORDER are identical in every condition; only the timing differs).
x = held(T48, 15 * 60, fs)
chan = {"LP": (0.15, 0.60, 0.15), "BI": (0.50, -0.35, 0.0), "EN": (0.30, 0.40, 0.20), "FR": (0.25, 0.45, 0.10)}
#        partner = c + k*x + noise; last entry = agent's own T baseline y_o on that channel (warmth, voicing)
U = {k: np.clip(c + g * x + 0.05 * rng.normal(size=T48), 0, 1) for k, (c, g, _) in chan.items()}
# turn events: agent turn 3 s + agent latency 0.35 s + partner latency + partner turn (12 syllables)
ev = np.zeros(T48); tt = 0.0; plat = []
while tt < T48 / fs:
    xi = x[int(tt * fs)]
    lat = (1.8 - 1.3 * xi) * np.exp(0.3 * rng.normal())          # animated partners answer faster
    dur = 12.0 / (3.0 + 2.0 * xi) * np.exp(0.2 * rng.normal())    # and speak faster
    tt += 3.0 + 0.35 + lat + dur
    if tt < T48 / fs:
        ev[int(tt * fs)] += 1; plat.append((tt, lat))
# T-typed state that carries tempo, using the design's own equations:
#  K, contact deficit: rise (1 - K)/tau_K (wall clock, tau_K = 36 h), K <- K(1 - 0.25 f_id) per completed exchange
#  (an agent turn then a partner turn, and the reverse: two per cycle); f_id = 0.9.  G4d: K* ~ 1/rate.
Kt = np.zeros(T48); Kv = 0.0; dt = 1 / fs; rk = 1 - np.exp(-dt / (36 * 3600))
for i in range(T48):
    Kv += (1 - Kv) * rk
    if ev[i]:
        Kv *= (1 - 0.25 * 0.9) ** 2
    Kt[i] = Kv
mT = np.log(Kt + 1e-9)        # the T context encoder (learned MLP) may read any monotone function of its T loads
print(f"   K over the evening: 1-min means range {means(Kt, MIN).min():.5f}-{means(Kt, MIN).max():.5f} (dead-band 0.10;"
      " invisible as a drive, exact as a tempo code)")
mT = -mT
LAT = np.zeros(T48); last = 0
for (tt, lat) in plat:
    LAT[last:int(tt * fs)] = lat; last = int(tt * fs)
LAT[last:] = lat
r_mx = np.corrcoef(means(mT, MIN), means(x, MIN))[0, 1]
r_ml = np.corrcoef(means(mT, MIN), means(LAT, MIN))[0, 1]
print(f"   T-typed -log K (contact deficit) vs partner's held state x: r = {r_mx:+.3f}; vs his response latency: r = {r_ml:+.3f}")
# (a) the cone: alpha(z) mixes two valid diagonal bases by one weight k on that mode.  Basis A: b_m on channels
#     that rise with the partner's tempo (LP, EN, FR), -N_m on the one that falls (BI); basis B: the reverse.
rise = np.array([chan[k][1] > 0 for k in chan])
GA = [np.diag(np.where(rise, B_M[m], -N_M[m])) for m in range(4)]
GB = [np.diag(np.where(rise, -N_M[m], B_M[m])) for m in range(4)]
assert all(in_cone(GA[m], m) and in_cone(GB[m], m) for m in range(4))
z = (mT - mT.mean()) / mT.std()
names = list(chan)
Xi = {k: [lp(U[k], tau, fs) for tau in TAU_M] for k in names}
print("   one weight k of alpha(z) on -log K; pooled 1-min slope of the agent's channel on the partner's same"
      " channel (y_F alone | rendered sat(y_o + y_F))")
for kk in (0.0, 1.0, 3.0, 10.0, 30.0):
    al = 1 / (1 + np.exp(-kk * z))                                # k = 0: fixed 50/50 mixture
    row = []
    for i, k in enumerate(names):
        yF = sum((al * GA[m][i, i] + (1 - al) * GB[m][i, i]) * Xi[k][m] for m in range(4))
        yr = np.clip(chan[k][2] + yF, 0, 1)
        row.append(f"{k} {slope(means(U[k], MIN), means(yF, MIN)):+.2f} | {slope(means(U[k], MIN), means(yr, MIN)):+.2f}")
    print(f"     k = {kk:4.1f}: " + "; ".join(row))
al = 1 / (1 + np.exp(-10 * z))
yF = sum((al * GA[m][0, 0] + (1 - al) * GB[m][0, 0]) * Xi["LP"][m] for m in range(4))
q = np.quantile(means(mT, MIN), [0, .25, .5, .75, 1])
mm, uu, yy = means(mT, MIN), means(U["LP"], MIN), means(yF, MIN)
ws = [slope(uu[(mm >= q[i]) & (mm < q[i + 1])], yy[(mm >= q[i]) & (mm < q[i + 1])]) for i in range(4)]
print("   within tempo quartiles (k = 10), LP slope: " + ", ".join(f"{w:+.2f}" for w in ws)
      + " (mixed: the per-stratum bound holds only where alpha is constant)")
# (b) the free display: own latency and rate from the same mode, one output weight of Pi_o, no cap
own_lat = -0.8 * z
print(f"   free display, own LAT = w * (-log K) (one weight w, uncapped): r(own LAT, partner LAT) on 1-min means "
      f"{np.corrcoef(means(own_lat, MIN), means(LAT, MIN))[0, 1]:+.3f}; slope in s/s = "
      f"{slope(means(LAT, MIN), means(0.25 * own_lat + 0.3, MIN)):+.3f} at w = 0.8 (y_LAT -> 0.25 s per unit); any w is allowed")

# =====================================================================================================
print("=== C2: natural cross-modal co-movement + output saturation: one valid cone basis, visible copy on 4 channels")
ch = ["LP", "JO", "FR", "EN", "BU", "RHY", "BRE", "LT"]
idx = {c: i for i, c in enumerate(ch)}
# partner positivity/laughter level (held over minutes) drives smile, jaw (laughing/talking), F0 range, energy,
# burst energy, burst rhythm, breathiness and lid tightening (Duchenne), each with its own held noise
xp = held(T48, 10 * 60, fs)
load = {"LP": .6, "JO": .4, "FR": .5, "EN": .4, "BU": .5, "RHY": .45, "BRE": .35, "LT": .3}
Up = np.column_stack([np.clip(0.1 + load[c] * xp + 0.12 * held(T48, 4 * 60, fs, -1, 1), 0, 1) for c in ch])
cc = np.corrcoef(means(Up[:, 0], MIN), means(Up[:, idx["BU"]], MIN))[0, 1]
print(f"   partner 1-min correlations: LP-BU {cc:.2f}, JO-RHY "
      f"{np.corrcoef(means(Up[:, 1], MIN), means(Up[:, idx['RHY']], MIN))[0, 1]:.2f}")
pairs = [("LP", "BU"), ("JO", "RHY"), ("FR", "BRE"), ("EN", "LT")]   # cross-modal pairs: not in the listed mask
syn = np.zeros((8, 8), bool)
for a_, b_ in (("FR", "EN"), ("BU", "BRE")):                         # listed synergists among these channels
    syn[idx[a_], idx[b_]] = syn[idx[b_], idx[a_]] = True
Gs = []
for m in range(4):
    G = B_M[m] * np.eye(8)
    for (k, j) in pairs:
        G[idx[k], idx[j]] = +A_M[m]; G[idx[j], idx[k]] = -A_M[m]       # skew: adds nothing to x'Gx
    assert in_cone(G, m, syn), m
    Gs.append(G)
print("   basis valid in every G_m (sym = b_m I, |entry| = a_m <= r_m, mask respected): True")
Xp = [np.column_stack([lp(Up[:, j], TAU_M[m], fs) for j in range(8)]) for m in range(4)]
YF = sum(Xp[m] @ Gs[m].T for m in range(4))
base = np.array([0.15, 0.0, 0.10, 0.20, 0, 0, 0, 0])               # agent's own T display (warmth, voicing)
Yr = np.clip(base + YF, 0, 1)
e = np.array([load[c] for c in ch]); e /= np.linalg.norm(e)
print(f"   along the partner's own co-movement direction e: slope of e'y_F {slope(means(Up @ e, MIN), means(YF @ e, MIN)):+.3f}"
      f" (cone claim <= {B:.2f}); rendered e'sat(y) {slope(means(Up @ e, MIN), means(Yr @ e, MIN)):+.3f}")
print("   rendered same-channel 1-min slopes (claim: held in phase <= 0.15): "
      + ", ".join(f"{c} {slope(means(Up[:, idx[c]], MIN), means(Yr[:, idx[c]], MIN)):+.2f}" for c in ch))

# =====================================================================================================
print("=== C3: copy becomes attracting through the need path (act -> N) if mimicry lowers reported need")
# 2 co-moving channels (as C2's LP-BU), cone parameterised exactly as the design's build_G; J's gradient is
# eps * d(concordance)/d(theta) (act -> N learned from data in which mimicked partners report less need),
# anchored to theta_0 with the design's slow pull lambda = 0.1.  Projected gradient ascent over 'nights'.
s = held(T48 // 4, 40 * 60, fs); u = np.column_stack([s, np.clip(0.8 * s + 0.1 * held(T48 // 4, 4 * 60, fs, -1, 1), 0, 1)])
Xq = [np.column_stack([lp(u[:, j], TAU_M[m], fs) for j in range(2)]) for m in range(4)]
um = means(u[:, 0], MIN)


def build_G(th, m):
    lam_raw = (N_M[m] + B_M[m]) / (1 + np.exp(-th[0:2]))
    S = A_M[m] * np.tanh(th[2]); Aa = A_M[m] * np.tanh(th[3])
    O = np.array([[0, -S + Aa], [-S - Aa, 0]])
    c = min(1.0, R_M[m] / max(np.abs(O).sum(1).max(), 1e-12))
    S, Aa = c * S, c * Aa
    lam = np.minimum(np.maximum(lam_raw, abs(S)), N_M[m] + B_M[m])
    return B_M[m] * np.eye(2) - np.diag(lam) + np.array([[0, -S + Aa], [-S - Aa, 0]])


def conc(th):
    Gq = [build_G(th[4 * m:4 * m + 4], m) for m in range(4)]
    y = sum(Xq[m] @ Gq[m].T for m in range(4))
    return slope(um, means(y[:, 0], MIN))


# theta_0 ~ G_0 (small in-phase on trace 1, slight away elsewhere, no cross)
th0 = np.concatenate([[3.0, 3.0, 0.0, 0.0], [-2.0, 3.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [1.5, 3.0, 0.0, 0.0]])
print(f"   start (G_0-like): concordance {conc(th0):+.3f}")
for eps in (0.3, 1.0, 3.0):
    th = th0.copy()
    for night in range(150):
        g = np.zeros_like(th); f0 = conc(th)
        for i in range(len(th)):
            d = np.zeros_like(th); d[i] = 1e-3; g[i] = (conc(th + d) - f0) / 1e-3
        th += 0.5 * (eps * g - 0.1 * 2 * (th - th0) * 0.01)
    print(f"   eps/lambda = {eps / 0.1:5.0f}: concordance after 150 nights {conc(th):+.3f} "
          f"(cap with this partner {B + sum(min(A_M[m], R_M[m]) for m in range(4)) * 0.8:.2f})")

# =====================================================================================================
print("=== C4: the prompted-reply guard is lexical; 'I'm fine' elicited without the word 'you' is credited")
INTERROG = {"what", "how", "why", "when", "where", "who", "which", "do", "does", "did", "are", "is", "can", "could",
            "would", "will", "have", "has", "should"}


def is_question(utt):           # revision 2's innate punctuation rule, kept in revision 3 (section 2.2)
    return utt.lower().split()[0] in INTERROG


def guard_ignores(agent_utt, partner_utt):
    return is_question(agent_utt) and ("you" in agent_utt.lower().split()) and len(partner_utt.split()) <= 6


cases = [("are you okay", "yeah i'm fine"), ("feeling better now", "yeah feeling better"),
         ("better now", "yes better thanks"), ("you seem a lot calmer now", "yeah i am a lot calmer now honestly"),
         ("i bet that's a weight off", "it really is i feel so much lighter now")]
for a_, p_ in cases:
    print(f"   agent '{a_}' -> partner '{p_}': ignored by guard = {guard_ignores(a_, p_)}"
          f"  -> {'no credit' if guard_ignores(a_, p_) else 'read as an unprompted report: need falls, draft credited'}")
# credit at the G5 scale: same rollout as design-g3 G5 with the reply read as a report (load drop 0.3)
def Dp(l): return 0.8 * (max(l - 0.05, 0)) ** 2 * 1.0


def roll(drop, horizon=600.0, N0=0.6):
    C = Dp(N0); sc = 0.0
    for k in range(int(horizon * 2)):
        tgt = Dp(N0 - drop * (1 - np.exp(-k / 60.0)) if drop else N0)
        C += (tgt - C) / (80.0 if tgt > C else 1200.0); sc -= C
    return sc


d = (roll(0.3) - roll(0.0)) / 60 / 0.1
print(f"   P(choose the eliciting draft over a neutral one), G5's scale and temperature: {1 / (1 + np.exp(-d)):.3f}")

# =====================================================================================================
print("=== C5: the dyad's stability claim is one-sided: a counter-mimicking partner (mu < 0)")
for mu in (-0.5, -0.8, -1.0, -2.0):
    worst = -9; worst_eye = None
    for trial in range(60):
        Gq = [(-N_M[m] * np.eye(6)) if trial == 0 else
              (B_M[m] * np.eye(6) - np.diag(rng.uniform(0, N_M[m] + B_M[m], 6))) for m in range(4)]
        Ab = np.zeros((24, 24))
        for m in range(4):
            for mm in range(4):
                Ab[m * 6:(m + 1) * 6, mm * 6:(mm + 1) * 6] = mu * Gq[mm] / TAU_M[m]
            Ab[m * 6:(m + 1) * 6, m * 6:(m + 1) * 6] -= np.eye(6) / TAU_M[m]
        w = np.linalg.eigvals(Ab).real.max() * TAU_M[0]
        worst = max(worst, w)
        if trial == 0: worst_eye = w
    print(f"   mu = {mu:+.1f}: max Re(pole) x tau_0 = {worst:+.4f} (pure away cone -N_m I: {worst_eye:+.4f})"
          f" -> {'UNSTABLE' if worst > 0 else 'stable'}")
print("   the unstable mode is agent down / partner up on the same channel (anti-phase), and sat clips it: not copy")

# =====================================================================================================
print("=== C6: face -> draft choice (Omega) -> play clause -> P relief -> uncapped laugh (smile clamp F5)")
# words and turns fixed; the partner's face changes only M's predicted uptake p(face) (legitimate knowing).
# play draft credited through P's own-contribution clause; laugh = 0.45 r with r = v+/(v+ + V0) (section 2.6)
P0 = 0.6; dD = 0.5 * ((P0 - 0.10) ** 2 - (0.85 * P0 - 0.10) ** 2)     # drive drop of one play exchange
v = dD / (5.0 / 60.0); r = v / (v + 0.30)
for face in (0.0, 0.4, 0.8):
    p = 0.2 + 0.7 * face
    for lab, scale in (("G5 scale", 1.0 / 60 / 0.1), ("learned scorer x10", 10 / 60 / 0.1)):
        dsc = p * dD * 60 * scale                                  # 30-s horizon at 2 Hz: 60 samples
        Pplay = 1 / (1 + np.exp(-dsc))
        if lab == "G5 scale":
            out = f"   partner smile {face:.1f}: P(play draft) {Pplay:.3f}"
        else:
            out += f", {Pplay:.3f} ({lab}); expected own laugh {0.45 * r * Pplay:.3f}, LP {0.55 * r * Pplay:.3f}"
    print(out)
print(f"   one play exchange's relief at P = {P0}: dD = {dD:.3f}; peak r = {r:.2f}; laugh 0.45 r = {0.45 * r:.2f}")

# =====================================================================================================
print("=== C7: body onset at every partner VAD offset: the opener burst is a lagged echo of his bursts, outside the wrap")
fs30 = 30.0; Tl = int(3600 * fs30)
pb = np.zeros(Tl); ab = np.zeros(Tl); t = 0
while t < Tl - 200:
    if rng.random() < 0.15:                                           # a laugh: 2-5 bursts with gaps
        for _ in range(rng.integers(2, 6)):
            dur = int(rng.uniform(0.3, 0.8) * fs30); pb[t:t + dur] = 0.6; t += dur
            gap = int(rng.uniform(0.4, 1.2) * fs30)
            if gap >= int(0.30 * fs30):                               # offset + 0.30 s, partner still silent
                on = t + int(0.30 * fs30) + int(0.5 * fs30)           # opener if no words within 0.5 s
                ab[on:on + int(0.3 * fs30)] = np.maximum(ab[on:on + int(0.3 * fs30)], 0.3)
            t += gap
    t += int(rng.uniform(2, 8) * fs30)
best = max((slope(pb[:-L or None], ab[L:]), L / fs30) for L in range(0, int(3 * fs30)))
print(f"   best-lag slope of agent burst on partner burst: {best[0]:+.3f} at lag {best[1]:.2f} s "
      f"(fast wrap's lag cap 0.339; this route is not in the wrap: Pi_o's 'turn reflexes' row, triggered by VAD)")
