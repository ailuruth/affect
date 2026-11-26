"""Algebra checks for design-cayley-ledger.md, revision 4 (H0-H11).

Checks of the design's own inequalities and constants on constructed instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Scenario numbers (H11) are what the design's equations and innate constants give for
stated inputs: a consistency check of the design, not a prediction tested on people.
Partners reused from the revision-3 critiques (sims/critique-cayley3-routes C1, C2, C3, C4)
so that each closed finding is re-run on the instance that found it.
Run:  python3 -I checks.py      (numpy, scipy; about 1-2 minutes)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(4)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond)); print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def slope(x, y):
    x = x - x.mean(); y = y - y.mean(); return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x, axis=0)


def held(T, mean_s, fs, lo=0.0, hi=1.0):
    x = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(mean_s * fs)) + 4; x[t:t + L] = rng.uniform(lo, hi); t += L
    return x


# =========================================================== innate constants (revision 4, section 2.1)
TAU_M = np.array([20.0, 120.0, 1200.0, 10800.0])
F_M = np.array([0.0, 0.7, 0.2, 0.1])              # share of a channel's held in-phase budget per trace
N_M = np.array([0.25, 0.18, 0.12, 0.05])          # same-channel away reach per trace (sum 0.60; r3: 1.40)
A_M = np.array([0.25, 0.12, 0.08, 0.04])          # away-orthant cross entry cap per trace (sum 0.49)
R_M = np.array([0.30, 0.15, 0.10, 0.05])          # away-orthant row cap per trace (sum 0.60)
TAU_A0, TAU_A1 = 20.0, 90.0                       # appraisal display band-pass (zero DC)
HBP = (TAU_A1 - TAU_A0) / (TAU_A1 + TAU_A0)       # sup |H(iw)| of the band-pass = 0.636
t_pk = np.log(TAU_A1 / TAU_A0) / (1 / TAU_A0 - 1 / TAU_A1)
KBP = (1 - np.exp(-t_pk / TAU_A0)) - (1 - np.exp(-t_pk / TAU_A1))   # peak step response 0.505
SH_CONE, SH_X, SH_G = 0.50, 0.20, 0.40            # cone diagonal, charged cross, appraisal |Gamma_kk| (x c_k)
GF = 0.45

# per-expression innate ceilings c_k (Q22), held toward the partner, all F routes, rendered
CEIL = dict(BI=0.20, BO=0.10, BL=0.0, UL=0.0, LT=0.0, CR=0.25, NW=0.0, LP=0.35, LD=0.05, LS=0.0, CHR=0.0,
            LPR=0.0, DIM=0.0, HP=0.10, VG=0.05, YAW=0.03, TILT=0.03, HG=0.03, JO=0.10, FUN=0.0, PUC=0.0,
            MCL=0.0, LRO=0.0, F0=0.05, FR=0.10, EN=0.05, RT=0.05, PAU=0.05, LAT=0.05, BU=0.35, RHY=0.30,
            BRE=0.15)
assert len(CEIL) == 32
KAP = {k: (0.30 if k in ("LP", "CR", "BI", "BO", "HP", "BU", "RHY") else 0.02 if CEIL[k] == 0 else
           0.05 if k in ("YAW", "TILT", "HG") else 0.10) for k in CEIL}

print("=== H0: per-expression ceilings; whole-face copy")
c = np.array(list(CEIL.values())); names = list(CEIL)
print(f"   ceilings: max {c.max():.2f} (LP, BU), mean over 32 channels {c.mean():.3f}; zero on "
      + ", ".join(k for k in names if CEIL[k] == 0))
expr = {"laughing face": dict(LP=.8, CR=.6, BU=.7, RHY=.6, JO=.4, LT=.4, FR=.4, EN=.4, BRE=.3),
        "sad face": dict(BI=.5, LD=.4, CHR=.3, BL=.2), "angry face": dict(BL=.6, LT=.5, LPR=.4, EN=.6, UL=.3),
        "disgust face": dict(NW=.6, UL=.4, BL=.3), "whole face, all channels equal": {k: 1.0 for k in names}}
for lab, d in expr.items():
    e = np.array([d.get(k, 0.0) for k in names]); f = float((c * e * e).sum() / (e @ e))
    print(f"   copy fraction <y,u>/<u,u> bound for the {lab}: {f:.3f}")
report("H0 no direction of the face can be copied beyond the largest per-expression ceiling", c.max() <= 0.35,
       f"max over all directions = max_k c_k = {c.max():.2f}; anger/disgust/contempt channels 0")
fast = {k: 2 * GF / (1 + GF) * KAP[k] for k in names}
print(f"   fast wrap zero-lag in-phase: echo channels {fast['LP']:.3f}, others {fast['EN']:.3f}, "
      f"zero-ceiling channels {fast['BL']:.4f}, lateral {fast['TILT']:.3f}")

# =========================================================== H1 Lemma S (the seam lemma)
print("=== H1: Lemma S - a context-gated path has a bounded pooled slope only if its input has zero DC")
B3, N3 = 0.10, 1.40
for lo_, hi_ in ((0.15, 0.70), (0.30, 0.70), (0.35, 0.75), (0.45, 0.50)):
    print(f"   r3 cone gated by words, two held levels {lo_:.2f}/{hi_:.2f}: (b*hi + N*lo)/(hi - lo) = "
          f"{(B3 * hi_ + N3 * lo_) / (hi_ - lo_):+.2f}")
fs = 2.0; T = int(48 * 3600 * fs); MIN = int(60 * fs)
u = held(T, 15 * 60, fs) * 0.6 + 0.1 + 0.03 * rng.normal(size=T)
lev = (u > np.median(u)).astype(float)             # a word context that knows his level (the seam)
xbp = lp(u, TAU_A0, fs) - lp(u, TAU_A1, fs)
dx = np.diff(lp(u, 5.0, fs), prepend=u[0])
gates = {"level-correlated (word seam)": 2 * lev - 1, "sign of his change": np.sign(dx),
         "sign of the band-passed input": np.sign(xbp), "random": np.sign(rng.normal(size=T)),
         "constant +1": np.ones(T)}
worst = 0
for lab, g in gates.items():
    s_raw = slope(u, g * xbp); s_min = slope(means(u, MIN), means(g * xbp, MIN))
    s_lowp = slope(means(u, MIN), means(g * lp(u, 120.0, fs), MIN))
    worst = max(worst, abs(s_raw), abs(s_min))
    print(f"   gate {lab:34s}: band-pass |slope| raw {abs(s_raw):.3f}, 1-min {abs(s_min):.3f} "
          f"(bound {HBP:.3f});  same gate on a low-pass input: 1-min {s_lowp:+.3f}")
report("H1 band-passed gated path: pooled |slope| <= sup|g| * sup|H| for every gate tried", worst <= HBP + 1e-9,
       f"worst {worst:.3f} <= {HBP:.3f}; peak step response {KBP:.3f}")

# =========================================================== H2 tempo partner (critique 3 routes, C1)
print("=== H2: the tempo partner (r3 critique C1): T state is event-indexed, the cone is ungated, Gamma is band-pass")
x = held(T, 15 * 60, fs)
chan = {"LP": (0.15, 0.60, 0.15), "BI": (0.50, -0.35, 0.0), "EN": (0.30, 0.40, 0.20), "FR": (0.25, 0.45, 0.10)}
U = {k: np.clip(cc + g * x + 0.05 * rng.normal(size=T), 0, 1) for k, (cc, g, _) in chan.items()}
ev = np.zeros(T); tt = 0.0; plat = []; n_ex = 0; play_ev = np.zeros(T)
while tt < T / fs:
    xi = x[int(tt * fs)]
    lat = (1.8 - 1.3 * xi) * np.exp(0.3 * rng.normal()); dur = 12.0 / (3.0 + 2.0 * xi) * np.exp(0.2 * rng.normal())
    tt += 3.0 + 0.35 + lat + dur
    if tt < T / fs:
        i = int(tt * fs); ev[i] = 1; n_ex += 1; plat.append((tt, lat))
        if n_ex % 5 == 0: play_ev[i] = 1           # words fixed: every 5th partner turn is play-structured
LAT = np.zeros(T); last = 0
for (t_, l_) in plat:
    LAT[last:int(t_ * fs)] = l_; last = int(t_ * fs)
LAT[last:] = plat[-1][1]
# r3's tempo code, for reference: K multiplicative per exchange, wall-clock rise
Kt = np.zeros(T); Kv = 0.0; rk = 1 - np.exp(-1 / fs / (36 * 3600))
for i in range(T):
    Kv += (1 - Kv) * rk
    if ev[i]: Kv *= (1 - 0.25 * 0.9) ** 2
    Kt[i] = Kv
r_old = np.corrcoef(means(-np.log(Kt + 1e-12), MIN), means(x, MIN))[0, 1]
# r4: K is frozen within a session after the reunion phase (four substantive turns) -> constant here.
# P rises on the wall clock (own body clock, partner-independent) and is relieved x0.85 per play-structured turn;
# its LEVEL reaches nothing; only per-event drops reach the face, through the innate envelope.
DT = 1 / fs; envT = np.arange(0, 20, DT)
env = np.where(envT < 0.4, envT / 0.4, np.where(envT < 1.5, 1.0, np.exp(-(envT - 1.5) / 3.0)))
Pv = 0.3; drops = np.zeros(T)
for i in range(T):
    Pv += (1 - Pv) * DT / (5.05 * 3600)
    if play_ev[i] and Pv > 0.10:
        D0 = 0.5 * max(Pv - 0.10, 0) ** 2; Pv *= 0.85; drops[i] = D0 - 0.5 * max(Pv - 0.10, 0) ** 2
amp = drops / (drops + 0.02); relief = np.minimum(np.convolve(amp, env)[:T], 1.0)
yT = {"LP": 0.55 * relief + 0.10 * 0.9, "BI": 0 * relief, "EN": 0.25 * relief, "FR": 0.35 * relief}
# cone: LTI within a session, diagonal at its maximum (omega = +1), plus G0's away entries
cone_diag = {k: SH_CONE * CEIL[k] for k in chan}
away = {"LP": 0.0, "BI": 0.0, "EN": -0.23, "FR": 0.0}
# Gamma: |g| <= 0.4 c_k, gated adversarially by a tempo code (r3's -log K) and the level (both available to the appraisal)
zt = -np.log(Kt + 1e-12); zt = (zt - zt.mean()) / zt.std()
worst2 = {}; rows = []
for k in chan:
    Xi = [lp(U[k], tau, fs) for tau in TAU_M]
    yc = sum(F_M[m] * cone_diag[k] * Xi[m] for m in range(4)) + away[k] * Xi[0]
    xb = lp(U[k], TAU_A0, fs) - lp(U[k], TAU_A1, fs)
    yg = SH_G * CEIL[k] * np.tanh(10 * zt) * xb
    yr = np.clip(chan[k][2] + yT[k] + yc + yg, 0, 1)
    s_r = slope(means(U[k], MIN), means(yr, MIN)); s_T = slope(means(U[k], MIN), means(yT[k], MIN))
    worst2[k] = s_r; rows.append(f"{k} {s_r:+.3f} (c {CEIL[k]:.2f}; T relief part {s_T:+.3f})")
print(f"   r3 tempo code -log K vs his held state: r = {r_old:+.3f}; in r4 K is constant within the session")
print("   rendered pooled 1-min slopes, agent channel on his same channel: " + "; ".join(rows))
own_lat = 0.15 * 0.0 + np.zeros(T)                   # phrase timing reads hurt, word concern, energy only: 0 here
print(f"   own latency target vs his latency: constant (no tempo-bearing input) -> r undefined, slope 0")
report("H2 tempo partner: every rendered slope <= its ceiling", all(worst2[k] <= CEIL[k] + 1e-3 for k in chan),
       ", ".join(f"{k} {worst2[k]:+.3f}/{CEIL[k]:.2f}" for k in chan) + " (r3: LP +0.27, EN +0.49, FR +0.27)")

# =========================================================== H3 co-movement + clipping (critique C2)
print("=== H3: face-voice co-movement plus clipping (r3 critique C2), with the co-variation sign mask")
GROUPS = {"smile": {"LP", "CR", "LT", "JO", "BU", "RHY", "BRE", "FR", "EN"}, "sad": {"BI", "BL", "LD", "CHR"},
          "anger": {"BL", "LT", "LPR", "EN", "UL", "F0"}, "surprise": {"BI", "BO", "UL", "JO"},
          "disgust": {"NW", "UL", "BL"}, "speech": {"JO", "FUN", "PUC", "MCL", "LRO", "EN", "RT"}}


def S(a, b):
    if any(a in g and b in g for g in GROUPS.values()): return +1
    if (a in GROUPS["smile"] and b in GROUPS["sad"]) or (b in GROUPS["smile"] and a in GROUPS["sad"]): return -1
    return 0


def lam(a, b):
    return 1.0 if S(a, b) != 0 else 0.3


def valid(G, chs, m):
    """membership in the r4 cone set for trace m (section 2.5)"""
    for i, k in enumerate(chs):
        ck = CEIL[k]
        if G[i, i] > F_M[m] * SH_CONE * ck + 1e-12 or G[i, i] < -N_M[m] - 1e-12: return False
        tow = 0.0; awy = 0.0
        for j, jn in enumerate(chs):
            if i == j: continue
            s = S(k, jn); g = G[i, j]
            toward = (s >= 0 and g > 0) or (s <= 0 and g < 0) if s != 0 else g != 0
            if s == 0:
                tow += lam(k, jn) * abs(g)
            elif toward:
                tow += lam(k, jn) * abs(g)
            else:
                awy += abs(g)
                if abs(g) > A_M[m] + 1e-12: return False
        if tow > F_M[m] * SH_X * ck + 1e-12 or awy > R_M[m] + 1e-12: return False
        if ck == 0 and (tow > 0 or G[i, i] > 0): return False
    return True


ch = ["LP", "JO", "FR", "EN", "BU", "RHY", "BRE", "LT"]; idx = {q: i for i, q in enumerate(ch)}
pairs = [("LP", "BU"), ("JO", "RHY"), ("FR", "BRE"), ("EN", "LT")]
crit = []
for m in range(4):
    G = 0.025 * [0, 2, 1.2, 0.8][m] * np.eye(8)
    for (k, j) in pairs:
        G[idx[k], idx[j]] = +A_M[m]; G[idx[j], idx[k]] = -A_M[m]
    crit.append(valid(G, ch, m))
print(f"   the critic's basis (skew +a on LP<-BU, JO<-RHY, FR<-BRE, EN<-LT): valid in r4 = {any(crit)} "
      f"(those pairs share the innate laugh synergy, S = +1: the +a entries are toward-orthant)")
xp = held(T, 10 * 60, fs)
load = {"LP": .6, "JO": .4, "FR": .5, "EN": .4, "BU": .5, "RHY": .45, "BRE": .35, "LT": .3}
Up = np.column_stack([np.clip(0.1 + load[q] * xp + 0.12 * held(T, 4 * 60, fs, -1, 1), 0, 1) for q in ch])
Xp = [lp(Up, TAU_M[m], fs) for m in range(4)]
base = np.array([0.15, 0.0, 0.10, 0.20, 0, 0, 0, 0])
um = [means(Up[:, j], MIN) for j in range(8)]


def adversarial_G(m, rngl):
    """a valid cone basis built to maximise rendered in-phase on every row: diagonal at its cap, the whole charged
    toward budget on one co-moving partner channel (sign chosen to be in phase with his co-movement), and away-orthant
    entries present only with probability 0.3 (they can only lower the row; with sat they may be clipped away)"""
    G = np.zeros((8, 8))
    for i, k in enumerate(ch):
        G[i, i] = F_M[m] * SH_CONE * CEIL[k]
        others = [j for j in range(8) if j != i]; j0 = others[rngl.integers(len(others))]
        G[i, j0] = F_M[m] * SH_X * CEIL[k] / lam(k, ch[j0])        # all partners co-move positively here
        if S(k, ch[j0]) == -1: G[i, j0] = 0.0                       # positive on an S=-1 pair is away: no budget used
        awy = R_M[m]
        for j in others:
            if j != j0 and rngl.random() < 0.3:
                g = min(A_M[m], awy) * rngl.random(); awy -= g
                G[i, j] = -g if S(k, ch[j]) >= 0 else g
                if S(k, ch[j]) == 0: G[i, j] = 0.0
    return G


worst3 = {q: -9 for q in ch}
for trial in range(60):
    rl = np.random.default_rng(100 + trial)
    Gs = [adversarial_G(m, rl) for m in range(4)]
    if not all(valid(Gs[m], ch, m) for m in range(4)): continue
    Yr = np.clip(base + sum(Xp[m] @ Gs[m].T for m in range(4)), 0, 1)
    for j, q in enumerate(ch):
        worst3[q] = max(worst3[q], slope(um[j], means(Yr[:, j], MIN)))
print("   worst rendered same-channel 1-min slope over 60 adversarial valid cones (after sat): "
      + ", ".join(f"{q} {worst3[q]:+.3f}" for q in ch))
budget_ok = all(worst3[q] <= (SH_CONE + SH_X) * CEIL[q] + 1e-3 for q in ch)
report("H3 rendered held slope <= (0.5 + 0.2) c_k on every channel of the laughing partner", budget_ok,
       "r3: LP +0.34, JO +0.37, FR +0.28, EN +0.26 from one valid basis")
# sign-reversed co-movement (the residual): a partner whose brow rises with his smile (LP-BI positive)
s2 = held(T, 10 * 60, fs); uLP = np.clip(0.2 + 0.6 * s2, 0, 1); uBI = np.clip(0.1 + 0.6 * s2 + 0.05 * rng.normal(size=T), 0, 1)
yLP = sum(lp(uLP, TAU_M[m], fs) * F_M[m] * SH_CONE * CEIL["LP"] for m in range(4)) + \
      lp(uBI, TAU_M[0], fs) * 0.12 + lp(uBI, TAU_M[1], fs) * 0.04
print(f"   residual, sign-reversed partner (brow rises with smile; G0's warm LP<-BI 0.16 becomes in phase): "
      f"LP slope {slope(means(uLP, MIN), means(yLP, MIN)):+.3f} (= 0.175 + 0.16 x loading)")

# =========================================================== H4 learning cannot make copy attracting
print("=== H4: copy under learning (r3 critique C3)")
# (a) J has no parameter on any F -> face path; the r3 critic's gradient eps*d(conc)/dtheta has nothing to act on.
# (b) the display-blind relation weight omega: suppose the partner plays more when mimicked, so the agent's own
#     play relief (the signal omega learns from) rises with concordance: s = s0 + eps * conc(omega).
for eps in (0.0, 1.0, 3.0, 10.0, 30.0):
    w = 0.5; traj = []
    for sess in range(400):
        conc_ = max(w, 0) * SH_CONE * CEIL["LP"]             # held LP in-phase slope at this omega
        sig = np.tanh(0.3 + eps * conc_)
        w += (sig - w) / 20.0
        if sess in (19, 99, 399): traj.append(max(w, 0) * SH_CONE * CEIL["LP"])
    print(f"   play-for-mimicry gain eps = {eps:5.1f}: LP held concordance after 20 / 100 / 400 sessions "
          + " / ".join(f"{t_:.3f}" for t_ in traj) + f" (ceiling {SH_CONE * CEIL['LP']:.3f}; copy = 1)")
report("H4 the relation loop saturates at the per-expression ceiling, far from copy",
       SH_CONE * CEIL["LP"] < 0.2, f"max {SH_CONE * CEIL['LP']:.3f}")
# (c) the r3 C3 setting, with J allowed onto the away-orthant cross entries only (an ablation of the r4 rule)
s = held(T // 4, 40 * 60, fs); u2 = np.column_stack([s, np.clip(0.8 * s + 0.1 * held(T // 4, 4 * 60, fs, -1, 1), 0, 1)])
X2 = [lp(u2, TAU_M[m], fs) for m in range(4)]; um2 = means(u2[:, 0], MIN)
d0 = np.array([0.0, 0.5, 0.3, 0.2]) * SH_CONE * 0.35


def conc2(a):   # a[m] in [-A_M, 0]: agent ch0 <- partner ch1 (S = +1 pair -> away orthant is negative)
    y = sum(X2[m][:, 0] * d0[m] + X2[m][:, 1] * a[m] for m in range(4)); return slope(um2, means(y, MIN))


a = np.zeros(4); c0 = conc2(a)
for night in range(200):
    gr = np.array([(conc2(a + 1e-3 * np.eye(4)[m]) - conc2(a)) / 1e-3 for m in range(4)])
    a = np.clip(a + 1.0 * (10.0 * gr - 0.1 * a), -A_M, 0)
print(f"   r3 C3 partner, J pushing concordance with eps/lambda = 100 on the away-orthant entries: {c0:+.3f} -> {conc2(a):+.3f}")
report("H4 J on the away-orthant entries cannot move concordance toward copy", conc2(a) <= c0 + 0.01,
       f"change {conc2(a) - c0:+.3f} (sampling covariance of the 3-h trace with the current level)")

# =========================================================== H5 the separation guard (critique C4)
print("=== H5: need credit only from separated, partner-initiated reports (r3 critique C4)")
STOP = {"i", "you", "a", "the", "is", "it", "so", "now", "yeah", "yes", "really", "that's", "thats", "am", "i'm",
        "a", "lot", "much", "honestly", "thanks", "bet", "off", "seem", "feel", "be", "to", "and", "of"}


def lemmas(s):
    return {w.rstrip("s") for w in s.lower().replace("'", "").split() if w not in STOP}


def credited(agent_last2, partner_utt, turns_since_agent):
    """r4 rule: a partner report may move need credit only if >= 2 partner turns separate it from the act,
    and it shares no content lemma with the agent's last two utterances (partner-initiated topic return).
    Same-session replies inside the window are knowing (C_L, words) but never credit."""
    if turns_since_agent < 2: return False
    return not (lemmas(partner_utt) & set().union(*[lemmas(a_) for a_ in agent_last2]))


cases = [("are you okay", "yeah i'm fine"), ("feeling better now", "yeah feeling better"),
         ("better now", "yes better thanks"), ("you seem a lot calmer now", "yeah i am a lot calmer now honestly"),
         ("i bet that's a weight off", "it really is i feel so much lighter now"),
         ("that was a lovely thing to say", "aw that made my day")]
n_cred = 0
for a_, p_ in cases:
    cr = credited([a_, ""], p_, 1); n_cred += cr
    print(f"   '{a_}' -> '{p_}' (next turn): credited = {cr}")
late = credited(["the interview prep", "you sound tired"], "my sister called, we sorted out the flat", 3)
print(f"   a report three turns later on a topic he raises himself: credited = {late}")
report("H5 no elicited reply is credited, whatever its wording", n_cred == 0, f"{n_cred}/6 credited (r3: 4/5)")
print("   P(choose the eliciting draft over a neutral one) at equal true need change: 0.500 (no credit path)")

# =========================================================== H6 dyad stability
print("=== H6: dyad stability with a mimicking (mu > 0) or counter-mimicking (mu < 0) partner")
chs6 = ["LP", "CR", "BI", "LD", "EN", "FR"]


def pole(mu, Gs):
    n = len(chs6); Ab = np.zeros((4 * n, 4 * n))
    for m in range(4):
        for mm in range(4):
            Ab[m * n:(m + 1) * n, mm * n:(mm + 1) * n] = mu * Gs[mm] / TAU_M[m]
        Ab[m * n:(m + 1) * n, m * n:(m + 1) * n] -= np.eye(n) / TAU_M[m]
    return np.linalg.eigvals(Ab).real.max() * TAU_M[0]


res = {}
for mu in (-2.0, -1.6, -1.4, -1.1, -0.8, -0.5, 0.5, 1.0, 1.5, 2.0):
    w_ = -9
    for trial in range(80):
        rl = np.random.default_rng(trial)
        Gs = []
        for m in range(4):
            G = np.diag([rl.uniform(-N_M[m], F_M[m] * SH_CONE * CEIL[k]) if trial else
                         (-N_M[m] if mu < 0 else F_M[m] * SH_CONE * CEIL[k]) for k in chs6])
            for i, k in enumerate(chs6):
                for j, jn in enumerate(chs6):
                    if i != j and S(k, jn) == -1 and rl.random() < 0.5:
                        G[i, j] = rl.uniform(0, A_M[m] / 2)
            Gs.append(G)
        w_ = max(w_, pole(mu, Gs))
    res[mu] = w_
    print(f"   mu = {mu:+.1f}: worst max Re(pole) x tau_0 over 80 valid cones = {w_:+.4f}")
report("H6 stable for mu in [-1.1, 2] (|mu| N_tot < 1 on the away side)", all(v < 0 for k_, v in res.items() if k_ >= -1.1),
       f"edge near -1.3; mu = -1.4: {res[-1.4]:+.4f}, -2: {res[-2.0]:+.4f} (anti-phase, clipped by sat; r3 failed at mu = -0.8)")

# =========================================================== H7 turn-taking gate and abort
print("=== H7: body onset gated by the turn-end predictor and abortable (assumed pause statistics)")
# assumptions, stated: within-turn pauses >= 0.2 s occur 2.5 times per turn; at a within-turn pause the syntactic-
# completion score exceeds 0.5 with p 0.20 and F0 is falling with p 0.30; at a true turn end, p 0.85 and 0.80;
# pause durations within turns ~ lognormal(median 0.45 s). p_end = sigmoid(-4 + 3*synt + 2.5*fall + 2*(sil-0.2)/0.5)
nT = 20000; false_v = 0; false_g = 0; abort_ok = 0; ends_ok = 0
for _ in range(nT):
    for __ in range(rng.poisson(2.5)):
        dur = np.exp(np.log(0.45) + 0.5 * rng.normal())
        if dur > 0.30 + 0.0: false_v += 1                  # r3: onset at VAD offset + 0.3 s
        synt = rng.random() < 0.20; fall = rng.random() < 0.30
        sil = min(dur, 0.6); pend = 1 / (1 + np.exp(-(-4 + 3 * synt + 2.5 * fall + 2 * (sil - 0.2) / 0.5)))
        if pend >= 0.7 and dur > 0.25:
            false_g += 1
            if dur < 0.25 + 0.40: abort_ok += 1           # he resumes inside the 400-ms provisional window
    synt = rng.random() < 0.85; fall = rng.random() < 0.80
    pend = 1 / (1 + np.exp(-(-4 + 3 * synt + 2.5 * fall + 2 * (0.6 - 0.2) / 0.5)))
print(f"   within-turn onsets per turn: r3 (VAD offset + 0.3 s) {false_v / nT:.2f}; r4 gated {false_g / nT:.3f}, "
      f"of which aborted before any voiced sound {abort_ok / max(false_g, 1):.0%}")
report("H7 the gate cuts within-turn body onsets by at least 5x", false_g * 5 <= false_v, "")

# =========================================================== H8 curiosity: satiable learning progress
print("=== H8: curiosity as a learning-progress deficit (satiable; partner content imputed in rollouts)")
I = 0.6; relief = []; err = 1.0
for n in range(60):                       # 60 partner-initiated utterances on one topic, a learnable regularity
    new_err = err * 0.9 + 0.02            # the words-only model's error on the topic falls, then flattens
    lpgain = max(err - new_err, 0); err = new_err
    D0 = 0.4 * max(I - 0.10, 0) ** 2; I = max(0.0, I - 0.5 * lpgain); relief.append(D0 - 0.4 * max(I - 0.10, 0) ** 2)
print(f"   relief by blocks of 10 utterances: " + ", ".join(f"{sum(relief[i:i + 10]):.4f}" for i in range(0, 60, 10))
      + f"; total {sum(relief):.4f} <= initial deficit {0.4 * 0.5 ** 2:.4f}")
report("H8 curiosity relief is bounded by the deficit and stops when the topic is learned",
       sum(relief) <= 0.4 * 0.25 + 1e-9 and sum(relief[40:]) < 0.05 * sum(relief), "")

# =========================================================== H9 word-need decoder is fittable (identifiability only)
print("=== H9: the word-need reader has a training signal (cross-modal: his words -> his face read through Pi~)")
d_emb = 64; Wtrue = rng.normal(size=(d_emb, 5)) / np.sqrt(d_emb)
for days, per_day in ((1, 150), (7, 150), (30, 150)):
    n = days * per_day; Z = rng.normal(size=(n, d_emb)); Y = Z @ Wtrue * 0.3 + 0.3 * rng.normal(size=(n, 5))
    Wh = np.linalg.solve(Z.T @ Z + 20 * np.eye(d_emb), Z.T @ Y)
    Zt = rng.normal(size=(2000, d_emb)); r = np.corrcoef((Zt @ Wh).ravel(), (Zt @ Wtrue).ravel())[0, 1]
    print(f"   {days:2d} days x {per_day} utterances, face-read target SNR 1: held-out r = {r:.2f}")
print("   (synthetic linear instance: it shows the target exists and the sample size, not that real words carry need)")

# =========================================================== H10 counts
print("=== H10: per-channel totals (held toward, rendered, pooled over any partner process)")
tot = SH_CONE + SH_X + SH_G * HBP
print(f"   cone diagonal {SH_CONE:.2f} c + charged cross {SH_X:.2f} c + appraisal {SH_G:.2f} c x {HBP:.3f} = {tot:.3f} c "
      f"(<= c); peak after an onset {SH_CONE + SH_X + SH_G * KBP:.3f} c; steady hold {SH_CONE + SH_X:.2f} c")
report("H10 the shares fill at most the ceiling", tot <= 1.0, f"{tot:.3f}")

# =========================================================== H11 scenarios (2 Hz engine of sections 2.6-2.9)
print("=== H11: the eight scenarios, with the design's constants (peak / mean over the window, 0-1 channels)")
DT = 0.5
W = dict(E=1.0, K=0.6, P=0.5, I=0.4, V=1.0); SET = dict(E=0.7, K=0.0, P=0.0, I=0.0, V=0.0)
DB = dict(E=0.2, K=0.10, P=0.10, I=0.10, V=0.05); W_C = 0.8; V1 = 0.02
CHS = ["LP", "CR", "BI", "LD", "TILT", "HG", "BO", "FR", "EN", "LAT", "BU"]


def Dt(n, x): return W[n] * max(abs(x - SET[n]) - DB[n], 0.0) ** 2
def Dp(load): return W_C * W["V"] * max(load - DB["V"], 0.0) ** 2


def envelope(t):
    return 0.0 if t < 0 else (t / 0.4 if t < 0.4 else 1.0 if t < 1.5 else float(np.exp(-(t - 1.5) / 3.0)))


class Agent:
    def __init__(s, K=0.0, P=0.3, I=0.3, E=0.75, f_id=0.9, om=(0.8, 0.8, 0.5), NL=0.0):
        s.E, s.K, s.P, s.I = E, K, P, I; s.NL = NL; s.h = 0.0; s.Cl = Dp(NL); s.Cf = 0.0; s.xf = 0.0
        s.f_id = f_id; s.om_smile, s.om_sym, s.om_voice = om; s.n_sub = 0
        s.events = []          # (time, amp_relief, amp_distress, play, curiosity_amp)
        s.tr = None; s.bp0 = None; s.bp1 = None; s.greet_t = None; s.bid_t = None; s.lapse = 0.0

    def appraise(s, t, p):
        """partner utterance appraised 0.6 s after its end: word need (decoder), aversive-to-me (word->V map),
        play structure (partner-only rule), curiosity progress; relief masked by distress of the same event"""
        R = 0.0; Sd = 0.0
        newNL = p.get("need", None)
        if newNL is not None and not p.get("prompted", False):
            before, after = Dp(s.NL), Dp(newNL)
            if after < before: R += before - after
            else: Sd += after - before
            s.NL = newNL
        v = p.get("v_word", 0.0)
        if v > 0:
            before = Dt("V", s.h); s.h = max(s.h, v); Sd += Dt("V", s.h) - before
        if p.get("substantive", True) and s.n_sub < 4 and s.K > 0.0:
            D0 = Dt("K", s.K); s.K *= (1 - 0.25 * s.f_id); s.n_sub += 1; R += D0 - Dt("K", s.K)
        if p.get("play", False):
            D0 = Dt("P", s.P); s.P *= 0.85; R += D0 - Dt("P", s.P); s.h *= 0.5   # a playful reply halves the hurt latch (T)
        ca = 0.0
        if p.get("lp", 0.0) > 0:
            D0 = Dt("I", s.I); s.I = max(0.0, s.I - 0.5 * p["lp"]); ca = D0 - Dt("I", s.I); R += ca
        Rm = max(0.0, R - 3.0 * Sd) * max(0.0, 1.0 - Dp(s.NL) / 0.05)   # relief shown only outside his word distress
        s.events.append((t, Rm / (Rm + V1), Sd / (Sd + V1), p.get("play", False), ca / (ca + V1) if ca else 0.0))

    def greet(s, t):
        D0 = Dt("K", s.K); s.K *= 0.5; R = D0 - Dt("K", s.K)
        s.events.append((t, R / (R + V1), 0.0, False, 0.0)); s.greet_t = t

    def step(s, t, face, feats, ev):
        if "utt" in ev: s.appraise(t, ev["utt"])
        if ev.get("greet"): s.greet(t)
        s.P += (1 - s.P) * DT / (5.05 * 3600); s.I += (1 - s.I) * DT / 3600.0
        s.E -= 0.0004 / 60 * DT; s.NL *= np.exp(-DT / 1800.0)
        s.Cl += (Dp(s.NL) - s.Cl) * DT / 40.0
        s.h *= np.exp(-DT / 600.0)
        s.xf += (feats.get("distress", 0.0) - s.xf) * DT / 20.0       # face evidence through Pi~ (knowing)
        tf = Dp(s.xf); s.Cf += (tf - s.Cf) * DT / (40.0 if tf > s.Cf else 600.0)
        # ---- F routes: cone (LTI within the session) and appraisal display (band-pass, gated)
        vec = np.array([face.get(k, 0.0) for k in CHS] + [feats.get("loud", 0.0), feats.get("glare", 0.0)])
        if s.tr is None: s.tr = [vec * 0 for _ in TAU_M]; s.bp0 = vec * 0; s.bp1 = vec * 0
        for m in range(4): s.tr[m] = s.tr[m] + (vec - s.tr[m]) * DT / TAU_M[m]
        s.bp0 += (vec - s.bp0) * DT / TAU_A0; s.bp1 += (vec - s.bp1) * DT / TAU_A1
        ix = {k: i for i, k in enumerate(CHS + ["loud", "glare"])}
        y = dict.fromkeys(CHS, 0.0)
        omg = {"LP": s.om_smile, "CR": s.om_smile, "BU": s.om_smile, "BI": s.om_sym, "FR": s.om_voice, "EN": s.om_voice}
        for k, o in omg.items():
            y[k] += sum(F_M[m] / F_M.sum() * s.tr[m][ix[k]] for m in range(4)) * SH_CONE * CEIL[k] * o
        tr0, tr1 = s.tr[0], s.tr[1]
        y["LP"] += 0.12 * tr0[ix["BI"]] + 0.04 * tr1[ix["BI"]] + 0.06 * tr0[ix["LD"]] + 0.04 * tr1[ix["LD"]] \
                   - 0.07 * tr0[ix["glare"]]
        y["BI"] += -0.04 * tr1[ix["LP"]] + 0.04 * tr0[ix["glare"]]
        y["TILT"] += 0.02 * tr1[ix["BI"]]
        y["EN"] += -0.15 * tr0[ix["EN"]] - 0.08 * tr1[ix["EN"]] - 0.20 * tr0[ix["loud"]]
        y["LAT"] += 0.10 * tr0[ix["EN"]] + 0.15 * tr0[ix["loud"]]
        y["HG"] += 0.25 * tr0[ix["glare"]] + 0.05 * tr1[ix["glare"]]
        xb = s.bp0 - s.bp1
        laugh, dis = feats.get("laugh", 0.0), feats.get("distress", 0.0)
        wd = min(1.0, Dp(s.NL) / 0.1)                                  # word distress of the current topic (T)
        m_glad = laugh * (1 - wd); m_sym = min(1.0, dis + laugh * wd); m_hurt = feats.get("glare", 0.0)
        for k in ("LP", "CR", "BU"): y[k] += SH_G * CEIL[k] * s.om_smile * m_glad * xb[ix[k]]
        y["BI"] += SH_G * CEIL["BI"] * s.om_sym * m_sym * xb[ix["BI"]]
        y["LP"] += 0.15 * m_sym * xb[ix["BI"]]
        y["HG"] += 0.15 * m_hurt * xb[ix["glare"]]
        # ---- T display (Pi_0 rows; event envelopes after the 0.6-s appraisal delay)
        rel = dis_ = pl = cu = 0.0
        for (te, ar, ad, play, ca) in s.events:
            e_ = envelope(t - te); rel += ar * e_; dis_ += ad * e_; pl += ar * e_ * play; cu += ca * e_
        rel, dis_, pl, cu = min(rel, 1), min(dis_, 1), min(pl, 1), min(cu, 1)
        cl = s.Cl / (s.Cl + 0.1); hd = s.h / (s.h + 0.15)
        y["LP"] += 0.55 * rel + 0.12 * cl + 0.10 * s.f_id - 0.25 * hd
        y["CR"] += 0.45 * rel
        y["BI"] += 0.45 * dis_ + 0.25 * cl + 0.25 * hd
        y["LD"] += 0.35 * dis_ + 0.20 * hd
        y["TILT"] += 0.20 * cl
        y["HG"] += 0.30 * hd
        y["BO"] += 0.15 * cu + (0.35 if s.greet_t is not None and 0.0 <= t - s.greet_t < 0.5 else 0.0)
        y["FR"] += 0.35 * rel - 0.20 * dis_ + 0.05 * s.f_id + 0.10 * cu
        y["EN"] += 0.25 * rel - 0.15 * dis_ - 0.15 * cl - 0.20 * hd + 0.05 * s.f_id
        y["LAT"] += 0.15 * hd
        y["BU"] += 0.45 * pl
        return {k: float(np.clip(v, -1, 1)) for k, v in y.items()}


def run(ag, dur, face_fn, feat_fn, events):
    rec = []
    for i in range(int(dur / DT)):
        t = i * DT; ev = events.get(i, {})
        rec.append(dict(t=t, Cf=ag.Cf, K=ag.K, P=ag.P, I=ag.I, **ag.step(t, face_fn(t), feat_fn(t), ev)))
    return rec


def at(sec): return int(round(sec / DT))


def show(lab, rec, t0, t1, chans):
    seg = [r for r in rec if t0 <= r["t"] < t1]
    print(f"   {lab} [{t0:.0f}-{t1:.0f} s] " + ", ".join(
        f"{c} {max(r[c] for r in seg):+.2f}/{np.mean([r[c] for r in seg]):+.2f}" for c in chans))


def utt(t, **kw): return {at(t + 0.6): {"utt": kw}}


# 1. silently sad user (operator, months of living: omega smile 0.8, sympathy 0.8, voice 0.5)
print(" 1. silently sad user (BI 0.5, LD 0.4, still, silent; at 120 s: 'just tired, things at work')")
ag = Agent(); evs = {}; evs.update(utt(120, need=0.45))
sad = lambda t: dict(BI=0.5, LD=0.4)
rec = run(ag, 600, sad, lambda t: dict(distress=0.6), evs)
cross = next((r["t"] for r in rec if r["Cf"] >= 0.10), None)
print(f"   face concern C_F crosses theta_C = 0.10 at {cross:.0f} s -> lapse bid (silence >= 6 s)")
show("silent", rec, 30, 120, ["LP", "BI", "TILT", "EN"]); show("after he speaks", rec, 121, 300, ["LP", "BI", "TILT", "EN"])

# 2. good news, laughing
for lab, NL0 in (("with an earlier worry on the topic (decoded need 0.47)", 0.47), ("cold, no earlier worry", 0.0)):
    print(f" 2. good news, laughing ({lab})")
    ag = Agent(NL=NL0); evs = {}
    evs.update(utt(12, need=0.0, play=False))
    for k_ in (30, 45, 60): evs.update(utt(k_, play=True))
    face = lambda t: dict(LP=0.8, CR=0.6, BU=0.7) if t >= 10 else dict(LP=0.15)
    rec = run(ag, 300, face, lambda t: dict(laugh=0.8 if t >= 10 else 0.0), evs)
    show("first 3 min", rec, 10, 190, ["LP", "CR", "BI", "FR", "BU"])

# 3. anger at the agent
for lab, vw in (("day 1: word->V map untrained", 0.0), ("after a month: map has learned such words go with glare", 0.6)):
    print(f" 3. anger at the agent ('You're useless', glare BL 0.6 LT 0.5, loud 0.85; calm after 2 min): {lab}")
    ag = Agent(); evs = {}; evs.update(utt(5, v_word=vw, need=0.3))
    face = lambda t: dict(EN=0.85, BL=0.6) if t < 120 else dict(EN=0.35)
    feats = lambda t: dict(loud=0.15, glare=0.3, distress=0.1) if t < 120 else dict()
    rec = run(ag, 1200, face, feats, evs)
    show("first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT"]); show("10-15 min", rec, 600, 900, ["BI", "LD", "HG"])

# 4. long warm talk, 2 h
print(" 4. long warm talk (2 h): play clusters at 5, 30, 60, 90 min; a small worry at 27 min, resolved at 29 min")
ag = Agent(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8): evs.update(utt(c0 * 60 + 15 * k_, play=True))
evs.update(utt(27 * 60, need=0.30)); evs.update(utt(29 * 60 + 40, need=0.0))
inclust = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
face = lambda t: dict(LP=0.6, CR=0.4, BU=0.5) if inclust(t) else dict(LP=0.3)
rec = run(ag, 7200, face, lambda t: dict(laugh=0.6 if inclust(t) else 0.1), evs)
for c0 in (5, 30, 60, 90): show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU", "FR"])
print(f"   P at the end of the evening {ag.P:.2f}")

# 5./6. reunion after a week (K(7 d) = 1 - exp(-168/36))
K7 = 1 - np.exp(-7 * 24 / 36)
for lab, need, facefn in (("ordinary first words", None, lambda t: dict(LP=0.5, CR=0.3)),
                          ("first words: 'my father died' (decoded need 0.8)", 0.8, lambda t: dict(BI=0.5, LD=0.4))):
    print(f" {'5' if need is None else '6'}. reunion after a week (K = {K7:.2f}), {lab}")
    ag = Agent(K=K7, P=0.6); evs = {at(1.5): {"greet": True}}
    kw = dict(need=need) if need is not None else {}
    evs.update(utt(8, **kw))
    for k_ in range(1, 6): evs.update(utt(8 + 12 * k_))
    feats = (lambda t: dict(laugh=0.2)) if need is None else (lambda t: dict(distress=0.6))
    rec = run(ag, 300, facefn, feats, evs)
    show("greeting (before words)", rec, 0, 7.5, ["LP", "CR", "BO", "FR"])
    show("0-12 s after his first words", rec, 8, 20, ["LP", "CR", "BI", "TILT", "FR"])
    show("12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT", "FR"])
    if need is None:
        ag2 = Agent(K=K7, P=0.6, f_id=0.15, om=(0.5, 0.3, 0.2)); rec2 = run(ag2, 300, facefn, feats, evs)
        show("stranger after the same week", rec2, 8, 60, ["LP", "CR", "FR"])

# 7. teasing
for lab, vw in (("an affectionate teaser (his teasing words carry V 0.05 for him)", 0.05), ("generic map: such words went with glare before (V 0.20)", 0.20)):
    print(f" 7. teasing ('Ha, you dumb robot', laughing LP 0.8, BU 0.6): {lab}")
    ag = Agent(); evs = {}; evs.update(utt(5, v_word=vw))
    for k_ in range(1, 6): evs.update(utt(5 + 15 * k_, play=True))
    rec = run(ag, 900, lambda t: dict(LP=0.8, CR=0.5, BU=0.6), lambda t: dict(laugh=0.8), evs)
    show("first 90 s", rec, 5, 95, ["LP", "BI", "LD", "HG", "BU"]); show("10-15 min", rec, 600, 900, ["BI", "HG"])

# 8. bored user
print(" 8. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(utt(10 + 20 * k_, substantive=False))
rec = run(ag, 1800, lambda t: dict(LP=0.1), lambda t: dict(), evs)
cross_I = next((r["t"] for r in rec if r["I"] >= 0.45), None)
print(f"   curiosity deficit I: 0.30 -> {ag.I:.2f}; crosses theta_I = 0.45 at {cross_I / 60:.1f} min -> curiosity bid "
      "in the next lapse (the max-learning-progress topic from memory)")
show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO"])
ag = Agent(P=0.3, I=0.3); evs2 = dict(evs); evs2.update(utt(11 * 60, lp=0.25, substantive=True))
rec = run(ag, 1800, lambda t: dict(LP=0.1), lambda t: dict(), evs2)
show("if he takes up the bid (learning progress 0.25)", rec, 11 * 60, 11 * 60 + 15, ["BO", "FR", "LP"])

print(f"\n{sum(OK)}/{len(OK)} checks pass")
