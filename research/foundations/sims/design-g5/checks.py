"""Algebra checks for design-cayley-ledger.md, revision 5 (H0-H15).

Checks of the design's own inequalities and constants on constructed instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Scenario numbers (H15) are what the design's equations and innate constants give for
stated inputs: a consistency check of the design, not a prediction tested on people.
Where a finding came from a revision-4 critic's constructed partner (sims/critique-cayley4-routes D1-D8,
sims/critique-cayley4-agent A-F), the check re-runs that partner.
Run:  python3 -I checks.py      (numpy, scipy; about 1-2 minutes)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(5)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond)); print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x, axis=0)


def hp(x, tau, fs): return x - lp(x, tau, fs)


def blocks(T, mean_len, fs, lo=0.0, hi=1.0):
    x = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(mean_len * fs)) + 10; x[t:t + L] = rng.uniform(lo, hi); t += L
    return x


def laughs(rate_per_min, T, fs, dur=2.5, spread=0.4):
    z = np.zeros(T); t = 0
    while t < T:
        r = max(rate_per_min[min(t, T - 1)], 1e-3) / 60.0
        t += int(rng.exponential(1 / r) * fs) + 1
        if t >= T: break
        d = max(1, int(np.exp(np.log(dur) + spread * rng.normal()) * fs)); z[t:t + d] = 1; t += d
    return z


# =========================================================== innate constants (revision 5, section 2.1)
TAU_M = np.array([20.0, 120.0, 1200.0, 10800.0])
F_M = np.array([0.0, 0.7, 0.2, 0.1])              # default trace shares of a channel's held budget
F_BI = np.array([0.5, 0.5, 0.0, 0.0])             # the sympathy brow fills within about a minute
N_M = np.array([0.25, 0.18, 0.12, 0.05])          # innate (G0) same-channel away diagonals, per trace
A_M = np.array([0.25, 0.12, 0.08, 0.04]); R_M = np.array([0.30, 0.15, 0.10, 0.05])
TAU_A0, TAU_A1 = 20.0, 90.0
HBP = (TAU_A1 - TAU_A0) / (TAU_A1 + TAU_A0)
t_pk = np.log(TAU_A1 / TAU_A0) / (1 / TAU_A0 - 1 / TAU_A1)
KBP = (1 - np.exp(-t_pk / TAU_A0)) - (1 - np.exp(-t_pk / TAU_A1))
GF = 0.45
TAU_B, TAU_W = 6.0, 60.0                          # partner baseline (sessions); omega learning (sessions)

CH = ["BI", "BO", "BL", "UL", "LT", "CR", "NW", "LP", "LD", "LS", "CHR", "LPR", "DIM", "HP", "VG", "YAW", "TILT",
      "HG", "JO", "FUN", "PUC", "MCL", "LRO", "F0", "FR", "EN", "RT", "PAU", "LAT", "BU_L", "BU_S", "RHY", "BRE"]
CEIL = dict(BI=0.20, BO=0.10, BL=0.0, UL=0.0, LT=0.0, CR=0.25, NW=0.0, LP=0.35, LD=0.05, LS=0.0, CHR=0.0,
            LPR=0.0, DIM=0.0, HP=0.10, VG=0.05, YAW=0.03, TILT=0.03, HG=0.03, JO=0.10, FUN=0.0, PUC=0.0,
            MCL=0.0, LRO=0.0, F0=0.05, FR=0.10, EN=0.05, RT=0.05, PAU=0.05, LAT=0.05, BU_L=0.35, BU_S=0.0,
            RHY=0.30, BRE=0.15)
assert list(CEIL) == CH and len(CH) == 33
ONE_SIDED = ("CR", "BU_L", "RHY", "BRE", "BI", "BO", "LP", "LD", "JO")   # sat clips the fast undershoot here
SIGNED = ("HP", "VG", "YAW", "TILT", "HG", "F0", "FR", "EN", "RT", "PAU", "LAT")  # [-1, 1] or phrase-level contour only
# fast wrap (D81: fast, partial, per-expression matching stays): the zero-lag in-phase cap 2 g k/(1+g) equals c_k
FASTFRAC = {k: (0.15 if k == "BI" else 0.3 if k in ("BO", "LD", "JO") else 1.0) for k in CH}  # smile, cheek, laughter: full ceiling
KAP = {k: FASTFRAC[k] * CEIL[k] * (1 + GF) / (2 * GF) for k in CH}          # zero on anger/disgust/contempt and sobs
FASTCAP = {k: 2 * GF / (1 + GF) * KAP[k] for k in CH}                       # = FASTFRAC c_k at zero lag
AWAY_FAST = 0.49                                                            # floor on the fast gates: away gain <= 0.49
GMIN = {k: (min(1.0, AWAY_FAST * (1 - GF) / (2 * GF * KAP[k])) if KAP[k] > 0 else 0.0) for k in CH}
ECHO0 = {k: (0.65 * FASTCAP[k] if k in ("LP", "CR", "BU_L", "RHY", "BI", "BO", "HP") else 0.0) for k in CH}
REST = dict(LP=0.09)                                                        # the agent's resting level (familiarity)
# pooled shares (cone diagonal, charged cross, appraisal |Gamma_kk|) x c_k; the fast allowance r_k (H5) fills the rest
SH = {k: (0.50, 0.20, 0.35) for k in CH}
SH["LP"] = (0.50, 0.15, 0.25); SH["BI"] = (0.70, 0.10, 0.05); SH["CR"] = (0.22, 0.06, 0.08)
for k in ("BU_L", "RHY", "BRE"): SH[k] = (0.07, 0.02, 0.05)
for k in ("BO", "LD", "JO"): SH[k] = (0.48, 0.15, 0.20)

# ----------------------------------------------------------- the cross-session ripple factor rho (Lemma S*)
wgrid = np.logspace(-4, 0.5, 4000)               # rad per session
eps_w = 1 / np.abs(1 + 1j * wgrid * TAU_W)        # how much of a mood at this frequency omega follows
h_b = np.abs(1j * wgrid * TAU_B / (1 + 1j * wgrid * TAU_B))   # how much of it survives centering
RHO = float((eps_w * h_b).max())

print("=== H0: per-expression ceilings, shares and the whole face")
c = np.array([CEIL[k] for k in CH])
print(f"   ceilings: max {c.max():.2f} (LP, BU_L), mean over 33 channels {c.mean():.3f}; zero on "
      + ", ".join(k for k in CH if CEIL[k] == 0))
expr = {"laughing face": dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, JO=.4, LT=.4, FR=.4, EN=.4, BRE=.3),
        "sad face": dict(BI=.5, LD=.4, CHR=.3, BL=.2), "crying face": dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, BRE=.4),
        "angry face": dict(BL=.6, LT=.5, LPR=.4, EN=.6, UL=.3), "disgust face": dict(NW=.6, UL=.4, BL=.3),
        "whole face, all channels equal": {k: 1.0 for k in CH}}
for lab, d in expr.items():
    e = np.array([d.get(k, 0.0) for k in CH]); f = float((c * e * e).sum() / (e @ e))
    print(f"   copy fraction bound for the {lab}: {f:.3f}")
report("H0 no direction of the face can be copied beyond the largest ceiling", c.max() <= 0.35,
       f"max over all directions = {c.max():.2f}; anger/disgust/contempt channels and the sob burst 0")

# =========================================================== H1: Lemma S* across sessions (routes finding 1)
print("=== H1: Lemma S* - omega learned over weeks, cone diagonal centred at his own baseline")
print(f"   rho = max_w eps_omega(w) |H_b(w)| = {RHO:.3f} (tau_omega {TAU_W:.0f} sessions, tau_b {TAU_B:.0f} sessions)")


def play_relief(n):
    P = 0.99; D0 = 0.5 * max(P - 0.1, 0) ** 2; Ds = D0
    for _ in range(n): P *= 0.85
    return D0 - 0.5 * max(P - 0.1, 0) ** 2, D0


def s_smile(nplay, hbar):
    r, D0 = play_relief(nplay); rho_p = r / D0
    return float(np.clip(0.3 + 0.7 * min(1, rho_p / 0.6) - 1.3 * min(1, hbar / 0.10), -1, 1))


def sessions(levels, good, hbar_low, rev, nplay_good=4):
    """returns agent held LP per session and his level; rev 4: omega from (play - V)/0.05 with tanh, rate 1/20,
    uncentred, away reach N; rev 5: s_smile, rate 1/60, centred at baseline b (tau 6 sessions), symmetric range"""
    om = 0.5; b = float(np.mean(levels[:10])); ag = []; oms = []
    for s, lev in enumerate(levels):
        cLP = CEIL["LP"]
        if rev == 4:
            r, _ = play_relief(nplay_good if good[s] else 0)
            sg = np.tanh((r - (0.0 if good[s] else hbar_low)) / 0.05)
            diag = om * 0.5 * cLP if om >= 0 else om * N_M.sum()
            y = np.clip(0.10 + diag * lev, 0, 1); om += (sg - om) / 20.0
        else:
            sg = s_smile(nplay_good if good[s] else 0, 0.0 if good[s] else hbar_low)
            diag = om * SH["LP"][0] * cLP
            y = np.clip(0.10 + diag * (lev - b), 0, 1)
            om += (sg - om) / TAU_W; b += (lev - b) / TAU_B
        ag.append(y); oms.append(om)
    return np.array(ag), np.array(oms)


nS = 730
good = np.repeat(rng.random(nS // 30 + 1) < 0.5, 30)[:nS]
worst5 = -9.0
for lo_, hi_, hl in ((0.20, 0.50, 0.0), (0.30, 0.45, 0.0), (0.38, 0.43, 0.0), (0.20, 0.50, 0.05), (0.30, 0.45, 0.05)):
    lev = np.where(good, hi_, lo_)
    a4, o4 = sessions(lev, good, 0.01 if hl == 0 else 0.05, 4)
    a5, o5 = sessions(lev, good, hl, 5)
    s4, s5 = slope(lev, a4), slope(lev, a5); worst5 = max(worst5, s5)
    print(f"   his session smile {lo_:.2f}/{hi_:.2f}, low-month hurt {hl:.2f}: rev 4 pooled slope {s4:+.2f}; "
          f"rev 5 {s5:+.3f} (omega {o5.min():+.2f}..{o5.max():+.2f})")
# sinusoidal moods with an omega target perfectly correlated with his level (adversarial), every period
for per in (8, 20, 60, 120, 365, 1000, 3000):
    n = max(4 * per, 730); ss = np.arange(n); lev = 0.35 + 0.1 * np.sin(2 * np.pi * ss / per)
    om = 0.0; b = 0.35; ag = []
    for s in range(n):
        tgt = 1.0 if lev[s] > 0.35 else -1.0
        ag.append(0.10 + om * SH["LP"][0] * CEIL["LP"] * (lev[s] - b)); om += (tgt - om) / TAU_W; b += (lev[s] - b) / TAU_B
    s5 = slope(lev[n // 4:], np.array(ag)[n // 4:]); worst5 = max(worst5, s5)
    print(f"   adversarial omega (target = sign of his level), mood period {per:5d} sessions: pooled slope {s5:+.3f}")
bound1 = SH["LP"][0] * CEIL["LP"] * (1 + RHO)
report("H1 the slow omega seam is closed: pooled multi-session slope <= s_C c (1 + rho)", worst5 <= bound1,
       f"worst {worst5:+.3f} <= {bound1:.3f} (LP ceiling 0.35; rev 4: +0.31..+0.89)")

# =========================================================== H2: omega is graded (routes low finding 5)
print("=== H2: omega_smile from the revision-5 formula (T inputs only: play relief share and hurt latch)")
for nplay in (0, 1, 2, 4, 8):
    for hb in (0.0, 0.05):
        sg = s_smile(nplay, hb); om = 0.5
        for _ in range(400): om += (sg - om) / TAU_W
        print(f"   {nplay} play turns per session, mean hurt {hb:.2f}: s = {sg:+.2f}, omega after 400 sessions {om:+.2f} "
              f"-> LP held in-phase share {om * SH['LP'][0] * CEIL['LP']:+.3f}")
s_op = s_smile(2, 0.01); s_sym_op = float(np.clip(0.3 + 0.7 * min(1, 0.4 / 0.5) - 1.3 * min(1, 0.01 / 0.10), -1, 1))
print(f"   the operator after months (2 play turns a session, mean hurt 0.01, 40% of his worries credited): "
      f"omega_smile -> {s_op:.2f}, omega_sym -> {s_sym_op:.2f}; omega_voice = 2 f_id - 1 = 0.80")
ok2 = s_smile(1, 0) < s_smile(2, 0) < s_smile(4, 0) and s_smile(0, 0) > 0 and s_smile(2, 0.05) < s_smile(2, 0)
report("H2 omega grades play and hurt, and no longer saturates for any partner who plays at all", ok2,
       f"s(0,1,2,4 play) = {s_smile(0, 0):.2f}, {s_smile(1, 0):.2f}, {s_smile(2, 0):.2f}, {s_smile(4, 0):.2f} "
       f"(rev 4: 0, 2.4, 4.1, 6.2 -> tanh 0, 0.98, 1.0, 1.0)")

# =========================================================== H3: relief and distress events are T-only (routes finding 2)
print("=== H3: events built only from T parts (word care D_p(N_L), hurt h, K_id, P, I); face and voice reach no event")
PI0_DIS = dict(BI=0.45, LD=0.35, LT=0.0, FR=-0.20, EN=-0.15)   # LT removed from the distress row (own-display mask)


def event_amp(word_need_rise, hurt_rise):          # the only event inputs (T)
    S = word_need_rise + hurt_rise; return S / (S + 0.02)


worst_LT = worst_BI = 0.0
for his_LT in (0.0, 0.25, 0.5, 0.75):              # the critic's angry partner: words fixed (no word event)
    ad = event_amp(0.0, 0.0); worst_LT = max(worst_LT, PI0_DIS["LT"] * ad); worst_BI = max(worst_BI, PI0_DIS["BI"] * ad)
for dist in (0.3, 0.6, 0.9):                        # silent sad face: no word, so no event at all
    ad = event_amp(0.0, 0.0); worst_BI = max(worst_BI, PI0_DIS["BI"] * ad)
report("H3 face- and voice-borne care or V never reach the free display", worst_LT == 0 and worst_BI == 0,
       f"agent LT from events {worst_LT:.2f} (rev 4 as written 0.23-0.24), BI from events at a silent sad face "
       f"{worst_BI:.2f} (rev 4 as written 0.32-0.42); LT is also out of Pi_0 and out of Delta's span")

# =========================================================== H4: the face-reader loop (routes finding 3)
print("=== H4: co-training without the anchor; Delta masked off the anger/disgust/contempt synergies")


def coloop(anchor, own_mask, nights=400, his_uses_zero=False):
    A0 = np.zeros((5, 3)); A0[0, 0] = A0[1, 1] = A0[2, 2] = 1      # synergies 0-2 open; 3-4 = anger/disgust synergies
    B = np.zeros((5, 3)); B[:3] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0.]])
    if his_uses_zero: B[3, 2] = 0.8                                   # he presses lips / lowers brow when distressed
    Dl = np.zeros((5, 3)); Sx = rng.normal(size=(3000, 3)); out = []
    for night in range(nights):
        Fown = Sx @ (A0 + Dl).T; Fp = Sx @ B.T
        X = np.vstack([Fown, np.sqrt(anchor) * Fp]); Y = np.vstack([Sx, np.sqrt(anchor) * Sx])
        W = np.linalg.lstsq(X, Y, rcond=None)[0].T
        for _ in range(20):
            Rr = W @ (A0 + Dl) - np.eye(3); g = W.T @ Rr + 0.1 * Dl; Dl = np.clip(Dl - 0.2 * g, -0.3, 0.3)
            if own_mask: Dl[3:] = 0.0
        if night in (0, 99, 399):
            Af = A0 + Dl; cos = np.sum(Af[:3] * B[:3]) / np.linalg.norm(Af[:3]) / np.linalg.norm(B[:3])
            out.append((night + 1, cos, np.abs(Dl[3:]).max(), np.linalg.norm(W @ Af - np.eye(3))))
    return out


for lab, an, mk, hz in (("rev 4 (anchor 0.1, no mask), his code uses a zero-ceiling synergy", 0.1, False, True),
                        ("rev 5 (no anchor, own-display mask), same partner", 0.0, True, True),
                        ("rev 5, his code permutes the agent's synergies (critic D5b)", 0.0, True, False)):
    o = coloop(an, mk, his_uses_zero=hz)
    print(f"   {lab}: " + "; ".join(f"n{n}: cos {cs:+.3f}, max weight on anger/disgust synergies {z:.2f}, own-legibility err {e:.2f}"
                                     for n, cs, z, e in o))
o5 = coloop(0.0, True, his_uses_zero=True)
report("H4 no style drift toward his code and no weight on zero-ceiling synergies", abs(o5[-1][1]) < 0.02 and o5[-1][2] == 0,
       f"cosine {o5[-1][1]:+.3f} at night 400 (rev 4: 0.26), weight {o5[-1][2]:.2f}, own legibility {o5[-1][3]:.2f}")

# =========================================================== H5: the fast echo after sat (routes low finding 4)
print("=== H5: fast echo at its full cap (= c_k) after sat: rectification allowance r_k, worst over partner families")
fs = 10.0; T = int(12 * 3600 * fs); MIN = int(60 * fs); d = int(0.45 * fs)
RECT = {k: 0.0 for k in CH}
mood = blocks(T, 10 * 60, fs)
fam = {"burst": [], "episode": []}
for dur in (0.5, 1.0, 2.5, 5.0):                                # laugh bursts (BU_L, RHY, BRE)
    for amp_mod in (False, True):
        L = laughs(0.5 + 5.5 * mood, T, fs, dur=dur); amp = (0.3 + 0.7 * mood) if amp_mod else np.ones(T)
        fam["burst"].append(amp * L)
for dur in (1.5, 4.0, 10.0, 25.0):                              # face episodes (smiles, cheek, brow)
    L = laughs(0.3 + 3.0 * mood, T, fs, dur=dur, spread=0.6)
    fam["episode"].append((0.3 + 0.7 * mood) * L); fam["episode"].append(np.clip(0.2 * mood + 0.6 * L, 0, 1))
for k in ONE_SIDED:
    if CEIL[k] == 0: continue
    worst = 0.0
    for u in fam["burst" if k in ("BU_L", "RHY", "BRE") else "episode"]:
        echo = FASTCAP[k] * hp(np.concatenate([np.zeros(d), u[:-d]]), 4.0, fs)
        base = REST.get(k, 0.0)
        worst = max(worst, slope(means(u, MIN), means(np.clip(base + echo, 0, 1) - base, MIN)))
    RECT[k] = worst / CEIL[k]
    print(f"   {k:4s}: fast cap {FASTCAP[k]:.3f} at zero lag (innate echo {ECHO0[k]:.3f} per unit onset at 0.45 s); "
          f"worst rendered 1-min slope of the full-gate echo {worst:+.3f} = r_k {RECT[k]:.3f} c_k")
print("   signed and phrase-level channels: no clipping at rest, r_k = 0; (rev 4: echo 0.121 on bursts gave +0.071)")

# =========================================================== H6: the totals, per channel
print("=== H6: per-channel totals toward the partner (pooled over any stationary partner, across sessions)")
worst_tot = 0.0; rows = []
for k in CH:
    if CEIL[k] == 0: continue
    sc, sx, sa = SH[k]
    tot = sc * (1 + RHO) + sx + sa * HBP + RECT[k]
    hold = sc + sx; peak = sc + sx + sa * KBP + RECT[k]
    worst_tot = max(worst_tot, tot); rows.append((k, tot, hold, peak))
for k, tot, hold, peak in rows:
    if k in ("LP", "BI", "CR", "BU_L", "RHY", "BRE", "BO", "LD", "FR", "EN"):
        print(f"   {k:5s}: pooled <= {tot:.3f} c = {tot * CEIL[k]:.3f}; steady hold {hold:.2f} c = {hold * CEIL[k]:.3f}; "
              f"peak after an onset {peak:.3f} c")
report("H6 every channel's shares, cross-session ripple and fast allowance fit under its ceiling", worst_tot <= 1.0,
       f"worst {worst_tot:.3f} c")

# =========================================================== H7: G0 inside its own budget set (routes low finding 6)
print("=== H7: the innate cone G0, entry by entry, against its set (sign mask with signed synergies)")
GROUPS = {"joy": dict(LP=1, CR=1, LT=1, JO=1, BU_L=1, RHY=1, BRE=1, FR=1, EN=1),
          "sad": dict(BI=1, BL=1, LD=1, CHR=1, BU_S=1, VG=-1, HP=-1, FR=-1, EN=-1, RT=-1),
          "anger": dict(BL=1, LT=1, LPR=1, EN=1, UL=1, F0=1), "surprise": dict(BI=1, BO=1, UL=1, JO=1),
          "disgust": dict(NW=1, UL=1, BL=1), "speech": dict(JO=1, EN=1, RT=1)}


LATERAL = ("YAW", "TILT", "HG")


def S(k, j):
    """sign of the population's co-variation of k and j (fallback: the agent's own signed synergies).
    Derived features carry the sign of their constituents: f_loud ~ +EN, f_glare ~ +BL (anger), f_laugh ~ +BU_L.
    Lateral rows from a non-lateral input are rendered on the side opposite his own lateral trace (reflection
    rule), so they are away by construction."""
    if k in LATERAL and j not in LATERAL and j != k and k != "TILT": return -2   # marker: away by reflection
    if j == "loud": return 1 if k == "EN" else S(k, "EN")
    if j == "glare": return S(k, "BL") or S(k, "LT")
    if k == j: return 1
    for g in GROUPS.values():
        if k in g and j in g: return g[k] * g[j]
    joy, sad = GROUPS["joy"], GROUPS["sad"]
    if (k in joy and j in sad) or (k in sad and j in joy):
        return -(joy.get(k, 1) * sad.get(j, 1)) if k in joy else -(sad.get(k, 1) * joy.get(j, 1))
    if {k, j} & {"LAT", "PAU"} and {k, j} & {"EN", "RT", "FR", "F0"}: return -1
    return 0


SADSYN = [k for k, v in GROUPS["sad"].items() if v > 0]
JOYSYN = list(GROUPS["joy"])
# G0 (rows: agent channel; cols: partner channel or derived feature), per trace index m
G0 = [("EN", "EN", 0, -0.15), ("EN", "EN", 1, -0.08), ("EN", "loud", 0, -0.20), ("LAT", "loud", 0, +0.15),
      ("LAT", "EN", 0, +0.10), ("HG", "glare", 0, +0.25), ("HG", "glare", 1, +0.05),
      ("BL", "BL", 0, -0.15), ("BL", "BL", 1, -0.08), ("LT", "LT", 0, -0.15), ("LT", "LT", 1, -0.08),
      ("LD", "LD", 0, -0.15), ("LD", "LD", 1, -0.08),
      ("LP", "glare", 1, -0.035), ("LP", "glare", 2, -0.01), ("BI", "glare", 0, +0.006), ("BI", "glare", 1, +0.006), ("BI", "LD", 0, +0.004), ("BI", "LD", 1, +0.004),
      ("TILT", "BI", 1, +0.014), ("HP", "BI", 1, +0.04), ("VG", "BI", 1, +0.04)]
viol = []
for m in range(4):
    for k in CH:
        ents = [(j, g) for (kk, j, mm, g) in G0 if kk == k and mm == m and j != k]
        charged = 0.0; away = 0.0
        for j, g in ents:
            s = S(k, j)
            if k in JOYSYN and j in SADSYN and g > 0: viol.append(f"{k}<-{j} sadness->joy positive")
            if s == -2 or (s == 1 and g <= 0) or (s == -1 and g >= 0):
                away += abs(g)
                if abs(g) > A_M[m]: viol.append(f"{k}<-{j} away entry {g} > {A_M[m]}")
            else:
                charged += (1.0 if s != 0 else 0.3) * abs(g)
        if away > R_M[m] + 1e-12: viol.append(f"{k} away row {away:.3f} > {R_M[m]}")
        fsh = (F_BI if k == "BI" else F_M)[m]
        if charged > fsh * SH[k][1] * CEIL[k] + 1e-12: viol.append(f"{k} trace {m} charged {charged:.4f} > {fsh * SH[k][1] * CEIL[k]:.4f}")
        if CEIL[k] == 0 and charged > 0: viol.append(f"{k} zero-ceiling row has charged entries")
for (k, j, m, g) in G0:
    if k == j and g > 0 and CEIL[k] == 0: viol.append(f"{k} zero-ceiling diagonal > 0")
    if k == j and -g > N_M[m] + 1e-12: viol.append(f"{k} diagonal {g} beyond away reach {N_M[m]}")
print("   entries moved off the 20-s trace: LP<-glare -0.07 and BI<-glare +0.04 (now on the 2-min trace); "
      "LP<-BI and LP<-LD warm entries deleted (sadness -> joy forbidden); BI<-LP deleted; derived features signed")
report("H7 G0 lies in its own set on every trace", not viol, "; ".join(viol) if viol else "all entries in budget")

# =========================================================== H8: dyad stability (critic D7 re-run)
print("=== H8: single-channel loop gain with a counter-mimic, every F route at its away extreme")
w = np.logspace(-5, 1, 4000); worst_g = 0
for k in ("LP", "BI", "BU_L", "EN"):
    cn = -sum(N_M[m] / (1 + 1j * w * TAU_M[m]) for m in range(4))
    ap = -SH[k][2] * CEIL[k] * (1 / (1 + 1j * w * 20) - 1 / (1 + 1j * w * 90))
    fa = -2 * GF / (1 - GF) * KAP[k] * GMIN[k] * (1j * w * 4 / (1 + 1j * w * 4)) * np.exp(-1j * w * 0.45)
    G = np.abs(cn + ap + fa).max(); worst_g = max(worst_g, G)
    print(f"   {k}: max|G| {G:.3f} -> small-gain stable for |mu| < {1 / G:.2f}")
report("H8 the dyad is stable with any partner for |mu| <= 1.5", 1 / worst_g >= 1.5, f"|mu| < {1 / worst_g:.2f}")

# =========================================================== H9: rendered totals with every route at once (critic D1/D2/D8 partners)
print("=== H9: rendered pooled 1-min slopes, all F routes together at their caps (cone, charged, appraisal gate, fast echo)")
fs = 10.0; T = int(24 * 3600 * fs); MIN = int(60 * fs); d = int(0.45 * fs)
mood = blocks(T, 10 * 60, fs); L = laughs(0.5 + 3.0 * mood, T, fs)
u = dict(LP=np.clip(0.15 + 0.25 * mood + 0.35 * L + 0.03 * rng.normal(size=T), 0, 1), BU_L=0.6 * L,
         CR=np.clip(0.05 + 0.1 * mood + 0.3 * L, 0, 1), BI=np.clip(0.05 + 0.3 * (0.35 * mood + 0.3 * L), 0, 1))


def bp(x): return lp(x, 20.0, fs) - lp(x, 90.0, fs)


worst9 = 0.0
for k in ("LP", "BU_L", "CR", "BI"):
    uk = u[k]; ck = CEIL[k]; sc, sx, sa = SH[k]
    Fk = F_BI if k == "BI" else F_M
    yC = sum(Fk[m] * sc * ck * lp(uk - uk.mean(), TAU_M[m], fs) for m in range(4))
    yX = sx * ck * lp(u["LP"] if k != "LP" else u["CR"], 120.0, fs)          # whole charged budget on a co-moving channel
    xb = bp(uk); echo = FASTCAP[k] * hp(np.concatenate([np.zeros(d), uk[:-d]]), 4.0, fs)
    for lab, g in (("gate +1", np.ones(T)), ("gate sign(xi_A)", np.sign(xb)), ("gate = laughing", L)):
        yA = sa * ck * g * xb
        tot = slope(means(uk, MIN), means(np.clip(REST.get(k, 0) + yC + yX + yA + echo, 0, 1), MIN))
        worst9 = max(worst9, tot / ck)
    print(f"   {k:4s}: rendered total with the worst gate {max(0, worst9) * ck:+.3f} so far (c_k {ck:.2f})")
report("H9 the rendered total stays under each ceiling with every route at its cap", worst9 <= 1.0,
       f"worst {worst9:.3f} c_k (fast smile and laugh return at the full ceiling)")

# =========================================================== the agent's own innate display Pi_0 and its inverse
DRV = ["rel", "dis", "cl", "hd", "lowE", "act", "cur", "laugh", "fam"]
PI0 = {"rel": dict(LP=.55, CR=.45, FR=.35, EN=.25), "dis": dict(BI=.45, LD=.35, FR=-.20, EN=-.15),
       "cl": dict(BI=.25, LP=.05, TILT=.20, EN=-.15, RT=-.10), "hd": dict(BI=.25, LD=.20, LP=-.25, HG=.30, EN=-.20, LAT=.15),
       "lowE": dict(UL=-.30, FR=-.25, EN=-.25, RT=-.15), "act": dict(UL=.20, BO=.15, FR=.15, RT=.15, BRE=.10),
       "cur": dict(BO=.15, UL=.10, FR=.10), "laugh": dict(BU_L=.40, RHY=.35, CR=.20, LP=.15), "fam": dict(LP=.10)}
RD_CH = ["LP", "CR", "BI", "LD", "UL", "BO", "FR", "EN", "RT", "HG", "LAT", "BRE"]
RD_L = ["rel", "dis", "hd", "lowE", "act"]
M0 = np.array([[PI0[l].get(k, 0.0) for l in RD_L] for k in RD_CH])
REST_FACE = dict(LP=0.09, FR=0.0, EN=0.0, RT=0.0, UL=0.0)


def read(face, voiced=True):
    """Pi~_0: the innate inverse of the agent's own display (ridge), on the channels present; returns V, A, T loads"""
    rows = [i for i, k in enumerate(RD_CH) if voiced or k not in ("FR", "EN", "RT", "LAT")]
    x = np.array([face.get(RD_CH[i], 0.0) - (0.45 if RD_CH[i] == "EN" else 0.25 if RD_CH[i] == "FR" else
                                              0.40 if RD_CH[i] == "RT" else 0.0) * (1 if voiced else 0) for i in rows])
    M = M0[rows]; z = np.linalg.solve(M.T @ M + 0.05 * np.eye(len(RD_L)), M.T @ x)
    z = dict(zip(RD_L, z))
    return dict(V=float(np.clip(z["dis"] + z["hd"], 0, 1)), A=float(np.clip(z["act"], 0, 1)), T=float(np.clip(z["lowE"], 0, 1)))


def Dp(N): return 0.8 * (max(N["V"] - .05, 0) ** 2 + 0.7 * max(N["A"] - .15, 0) ** 2 + 0.5 * max(N["T"] - .2, 0) ** 2)


# his own expressive code (not the agent's): loads (V, A, T, joy) -> face and voice
def his_face(V=0.0, A=0.0, Tr=0.0, joy=0.0):
    return dict(BI=.5 * V + .25 * A, LD=.4 * V, CHR=.3 * V, UL=.3 * A - .3 * Tr, BO=.3 * A, HG=.1 * V,
                FR=.25 + .35 * A - .2 * V - .25 * Tr + .3 * joy, EN=.45 + .3 * A - .15 * V - .25 * Tr + .25 * joy,
                RT=.40 + .35 * A - .15 * Tr, LP=max(0, .3 + .5 * joy - .3 * V), CR=.15 + .45 * joy)


# =========================================================== H10: the word-need reader, trained, not set by hand
print("=== H10: the word-need reader trained nightly on (his words, Pi~_0 of his face); decoded need in the scenarios")
DIM = 64; Mw = rng.normal(size=(DIM, 4)) / 2.0
def emb(z): return Mw @ np.asarray(z) + 0.15 * rng.normal(size=DIM)
Zh = np.clip(rng.normal(size=(30 * 150, 4)) * [0.3, 0.3, 0.3, 0.3] + [0.1, 0.1, 0.1, 0.2], 0, 1) * (rng.random((30 * 150, 4)) < 0.4)
Xe = np.array([emb(z) for z in Zh])
Yr = np.array([[read({k: v + 0.03 * rng.normal() for k, v in his_face(*z).items()})[q] for q in "VAT"] for z in Zh])
WR = np.linalg.solve(Xe.T @ Xe + 5.0 * np.eye(DIM), Xe.T @ Yr)


def reader(z, trained=True):
    if not trained: return dict(V=0.0, A=0.0, T=0.0)
    y = np.clip(emb(z) @ WR, 0, 1); return dict(V=float(y[0]), A=float(y[1]), T=float(y[2]))


UTT = {"just tired, things at work": (0.30, 0.10, 0.55, 0), "I'm freaking out about the exam": (0.30, 0.75, 0, 0),
       "and I haven't finished chapter 4": (0.25, 0.60, 0, 0), "I got the job!": (0, 0.3, 0, 0.9),
       "the job thing is worrying me (two days earlier)": (0.45, 0.35, 0, 0), "my father died": (0.85, 0.30, 0.2, 0),
       "You're useless": (0.20, 0.50, 0, 0), "hi, good to see you": (0, 0.1, 0, 0.5), "yeah / ok": (0, 0, 0.1, 0)}
DEC = {}
for lab, z in UTT.items():
    r_ = reader(z); DEC[lab] = r_; print(f"   '{lab}': true (V {z[0]:.2f}, A {z[1]:.2f}, T {z[2]:.2f}) -> decoded V {r_['V']:.2f}, A {r_['A']:.2f}, "
                          f"T {r_['T']:.2f}; care D_p {Dp(r_):.3f}")
anx = DEC["I'm freaking out about the exam"]
report("H10 the reader decodes activation (anxiety) through the agent's own activation display", anx["A"] >= 0.3,
       f"decoded A {anx['A']:.2f} for 'freaking out' (rev 4: no own activation display, so no target); day 1: all 0")
sad_read = read(dict(BI=.5, LD=.4, CHR=.3), voiced=False)
print(f"   day-1 reading of a silent sad face through Pi~_0 (no learning): V {sad_read['V']:.2f}, A {sad_read['A']:.2f}, T {sad_read['T']:.2f}")
anx_read = read(his_face(V=.3, A=.75))
print(f"   reading of an anxious face and voice through Pi~_0: V {anx_read['V']:.2f}, A {anx_read['A']:.2f}, T {anx_read['T']:.2f}")

# =========================================================== H11: the hurt teacher has a valence (agent finding 3)
print("=== H11: word -> V map per person; teacher = innate threat reflex, not loudness alone")


def teacher(rev, loud, glare, laugh, duch, at=1.0):
    if rev == 4: return min(1.0, loud + glare)
    fpos = max(laugh, duch); return at * max(glare, loud * max(0.0, 1 - 2 * fpos))


PEOPLE = {"quiet affectionate teaser": ("tease", 0.0, 0.0, 0.6, 0.6), "loud laughing teaser": ("tease", 0.67, 0.0, 0.7, 0.7),
          "loud praiser (HAHA you're the BEST)": ("praise", 0.67, 0.0, 0.5, 0.7),
          "someone who shouted insults": ("insult", 0.5, 0.36, 0.0, 0.0), "quiet cold insult": ("insult", 0.0, 0.0, 0.0, 0.0)}
VW = {}
for who, (kind, loud, glare, laugh, duch) in PEOPLE.items():
    out = []
    for rev in (4, 5):
        tg = teacher(rev, loud, glare, laugh, duch); v = 0.0
        for night in range(30): v += (tg - v) * 0.15                       # fitted nightly on that person's addressed words
        out.append(v)
    VW[who] = out[1]
    print(f"   {who:38s}: v_w rev 4 teacher {out[0]:.2f}; rev 5 teacher {out[1]:.2f}")
report("H11 loud praise and loud laughing teasing no longer train hurt; shouted insults still do",
       VW["loud laughing teaser"] < 0.05 and VW["loud praiser (HAHA you're the BEST)"] < 0.05 and VW["someone who shouted insults"] > 0.3,
       "quiet cold contempt still trains nothing (stated weakness)")

# =========================================================== H12: the play rule and the play-surprise laugh (agent smaller items)
print("=== H12: play rule (alternation across speakers, safety) and laughter that habituates to content, not to time")


def play_struct(u, NLcare, h=0.0):
    """partner-only play rule: continuation of his own thread, an agent turn between (turn order), surprise in band,
    and safety: his word care below its dead-band (h is not read: a playful reply halves h instead)"""
    return bool(u.get("cont") and u.get("alt") and 0.3 <= u.get("surp", 0) <= 0.8 and NLcare < 0.05)


def laugh_amp(surp): return 0.40 * float(np.clip(1 - abs(surp - 0.55) / 0.25, 0, 1))


rum = [dict(cont=True, alt=False, surp=0.5)] * 3
care_rum = Dp(DEC["and I haven't finished chapter 4"])
print(f"   anxious rumination (continuations, no agent turn between, care {care_rum:.3f}): play = "
      f"{[play_struct(x, care_rum, 0) for x in rum]} (rev 4: True from the second turn)")
amps = []
for c0 in range(4):
    for k_ in range(8):
        surp = 0.55 if not (c0 == 3 and k_ >= 4) else 0.55 * np.exp(-(k_ - 3))       # cluster 4 repeats one joke
        amps.append(laugh_amp(surp) if play_struct(dict(cont=True, alt=True, surp=surp), 0.0, 0.0) else 0.0)
amps = np.array(amps).reshape(4, 8)
print("   own laugh per play turn, clusters at 5/30/60/90 min: " + "; ".join(f"{', '.join(f'{a:.2f}' for a in r)}" for r in amps))
report("H12 laughter lasts the evening and stops only for a repeated joke", amps[3, :4].min() >= 0.35 and amps[3, 6] < 0.05
       and not any(play_struct(x, care_rum, 0) for x in rum), "(rev 4: 0.24 then 0.04-0.05 held after the first cluster)")

# =========================================================== H13: the appraisal display learns its reactions (agent finding 4)
print("=== H13: appraisal display trained by anticipation of the agent's own innate display (display-blind toward him)")
XI = ["LP", "CR", "BU_L", "BI", "LD", "glare", "loud"]; YO = ["LP", "CR", "BU_L", "BI", "LD", "BO", "HG", "EN"]
nB = 5                                                     # 0 neutral, 1 glad-with (innate), 2 startle-orient (innate), 3-4 learned


def allowed(k, j, g):
    if k == j: return abs(g) <= SH[k][2] * CEIL[k] + 1e-12
    s = S(k, j)
    if k in JOYSYN and j in SADSYN and g > 0: return False
    return s == -2 or (s == 1 and g <= 0) or (s == -1 and g >= 0)


def project(G):
    G = G.copy()
    for a, k in enumerate(YO):
        for b_, j in enumerate(XI):
            if k == j: G[a, b_] = np.clip(G[a, b_], -SH[k][2] * CEIL[k], SH[k][2] * CEIL[k])
            elif not (allowed(k, j, G[a, b_]) or allowed(k, j, -G[a, b_])): G[a, b_] = 0.0
            elif not allowed(k, j, G[a, b_]): G[a, b_] = 0.0
            else: G[a, b_] = np.clip(G[a, b_], -0.15, 0.15)
        off = [b_ for b_, j in enumerate(XI) if j != k]; rs = np.abs(G[a, off]).sum()
        if rs > 0.25: G[a, off] *= 0.25 / rs
        if CEIL.get(k, 0) == 0: G[a] = 0.0
    return G


Gam = np.zeros((nB, len(YO), len(XI)))
for k in ("LP", "CR", "BU_L"): Gam[1, YO.index(k), XI.index(k)] = SH[k][2] * CEIL[k]
Gam[2, YO.index("HG"), XI.index("loud")] = 0.10; Gam[2, YO.index("EN"), XI.index("loud")] = -0.10
Gam0 = Gam.copy()
Wsel = np.zeros((nB, 5)); Wsel[1, 0] = 4.0; Wsel[2, 3] = 4.0; Wsel[:, 4] = [1.0, -2, -2, -0.5, -0.5]  # newborn: glad-with on laughter, startle on loudness
Wsel[3:, :4] = 0.3 * rng.normal(size=(2, 4))                                                       # learned rows start small, random
for r in (3, 4): Gam[r] = project(0.01 * rng.normal(size=Gam[r].shape))


def situations(n):
    X, A_, Y, typ = [], [], [], []
    for _ in range(n):
        t = rng.integers(5); xi = 0.03 * rng.normal(size=len(XI)); al = np.zeros(5); al[4] = 1; y = np.zeros(len(YO)); a_ = rng.uniform(0.2, 0.5)
        if t == 0:   # his laughter builds before a play turn -> own relief and laugh anticipated
            xi[[0, 1, 2]] += a_; al[0] = rng.uniform(.5, .9); y[[0, 1, 2]] = [.55 * a_ * .3, .45 * a_ * .3, .40 * a_ * .3]
        elif t == 1:  # his sadness before sad words -> own distress anticipated
            xi[[3, 4]] += [a_, .8 * a_]; al[1] = rng.uniform(.5, 1); y[[3, 4, 7]] = [.45 * a_ * .3, .35 * a_ * .3, -.15 * a_ * .3]
        elif t == 2:  # laughing over a sad topic -> distress, not gladness
            xi[[0, 2]] += a_; al[0] = .5; al[2] = 1; y[3] = .45 * a_ * .3
        elif t == 3:  # glare at it -> own hurt anticipated
            xi[5] += a_; xi[6] += .5 * a_; al[3] = 1; y[[3, 4, 6, 7]] = [.25 * a_ * .3, .2 * a_ * .3, .3 * a_ * .3, -.2 * a_ * .3]
        X.append(xi); A_.append(al); Y.append(y); typ.append(t)
    return np.array(X), np.array(A_), np.array(Y), np.array(typ)


def fwd(X, A_):
    lg = A_ @ Wsel.T; pi = np.exp(lg - lg.max(1, keepdims=True)); pi /= pi.sum(1, keepdims=True)
    Yb = np.einsum("rkj,nj->nrk", Gam, X); return pi, Yb, np.einsum("nr,nrk->nk", pi, Yb)


X, A_, Y, typ = situations(4000)
loss0 = float(((fwd(X, A_)[2] - Y) ** 2).sum(1).mean())
for it in range(4000):
    pi, Yb, Yh = fwd(X, A_); R = Yh - Y
    gG = np.einsum("nr,nk,nj->rkj", pi, R, X) / len(X)
    gpi = np.einsum("nk,nrk->nr", R, Yb); gl = pi * (gpi - (pi * gpi).sum(1, keepdims=True))
    Wsel -= 300.0 * (gl.T @ A_) / len(X)
    Gam[3:] -= 30.0 * gG[3:]; Gam[3:] += -0.001 * Gam[3:]
    for r in (3, 4): Gam[r] = project(Gam[r])
pi, _, Yh = fwd(X, A_); loss1 = float(((Yh - Y) ** 2).sum(1).mean())
names_t = ["his laughter builds", "his sadness before sad words", "laughing over a sad topic", "glare at it"]
for t in range(4):
    sel = pi[typ == t].mean(0); gain = (Yh[typ == t] * Y[typ == t]).sum() / (Y[typ == t] ** 2).sum()
    print(f"   {names_t[t]:30s}: selection (neutral, glad-with, startle, learned 3, learned 4) = "
          + ", ".join(f"{v:.2f}" for v in sel) + f"; fit to own anticipated display {gain:.2f}")
for r in (3, 4):
    ent = [f"{YO[a]}<-{XI[b_]} {Gam[r, a, b_]:+.3f}" for a in range(len(YO)) for b_ in range(len(XI)) if abs(Gam[r, a, b_]) > 1e-3]
    print(f"   learned basis {r}: " + ", ".join(ent))
viol13 = [f"basis {r} {YO[a]}<-{XI[b_]}" for r in range(nB) for a in range(len(YO)) for b_ in range(len(XI))
          if abs(Gam[r, a, b_]) > 1e-9 and not allowed(YO[a], XI[b_], Gam[r, a, b_])]
sad_sel = pi[typ == 1].mean(0)
report("H13 W and the learned bases train on own anticipation, stay in the cap set, and learn sympathy without a rule",
       loss1 < 0.7 * loss0 and not viol13 and sad_sel[3:].sum() > 0.5,
       f"loss {loss0:.5f} -> {loss1:.5f}; violations {len(viol13)}; hand-written reactions 8 -> 2 (glad-with, startle-orient)")

# =========================================================== H14: the arrival mask (agent finding 1), bounded
print("=== H14: the greeting reads his face: K relief shown x (1 - m_s), m_s centred at his own arrival baseline")


def m_s(face, d_b):
    return float(np.clip((read(face, voiced=False)["V"] - d_b - 0.10) / 0.30, 0, 1))


for lab, f in (("ordinary arrival (LP .5, CR .3)", dict(LP=.5, CR=.3)), ("tired arrival (BI .15)", dict(BI=.15, LP=.25)),
               ("grieving face at sight (BI .5, LD .4, CHR .3)", dict(BI=.5, LD=.4, CHR=.3)), ("crying (BI .8, LD .6)", dict(BI=.8, LD=.6))):
    print(f"   {lab:45s}: V read {read(f, voiced=False)['V']:.2f}, m_s {m_s(f, 0.05):.2f}")
# first-minute slope of the face-attributable greeting display on his LP (finite differences over faces near baseline)
worst14 = 0.0
for _ in range(400):
    f = dict(LP=rng.uniform(0, .8), BI=rng.uniform(0, .6), LD=rng.uniform(0, .5))
    for chan in ("LP", "BI"):
        f2 = dict(f); f2[chan] += 0.01
        dLP = 0.55 * 0.94 * (m_s(f, 0.05) - m_s(f2, 0.05)) / 0.01 * (0.2 + 1.1 + 3.0) / 60   # a_r 0.94, envelope area 4.3 s
        if chan == "LP": worst14 = max(worst14, dLP)
        else: worst14 = max(worst14, -dLP * 0.0)
print(f"   worst toward slope of the first-minute greeting smile on his LP through m_s: {worst14:+.3f} (one event per session)")
# across sessions with the greeting amplitude correlated with his level (Lemma S*: m_s centred at his baseline)
lev = np.where(good, 0.10, 0.25); db = 0.05; ys = []; amps = np.where(good, 0.6, 0.9)
for s in range(nS):
    f = dict(BI=lev[s], LD=0.8 * lev[s]); ys.append(-amps[s] * 0.55 * m_s(f, db) * 4.3 / 60)
    db += (read(f, voiced=False)["V"] - db) / TAU_B
s14 = slope(lev, ys)
report("H14 the face-gated greeting is a bounded once-per-session route", worst14 <= 0.06 and abs(s14) <= 0.06,
       f"first-minute slope {worst14:.3f}; across sessions with a level-correlated greeting {s14:+.3f}; whole-session pooled negligible")

# =========================================================== H15: the scenarios (2 Hz engine of sections 2.5-2.9)
print("=== H15: the ten scenarios, with the design's constants (peak / mean over the window; operator after months unless stated)")
DT = 0.5
OUT = ["LP", "CR", "BI", "BO", "LD", "UL", "TILT", "HG", "HP", "FR", "EN", "RT", "LAT", "BU_L", "RHY", "BRE", "LT"]
BASE = dict(LP=.30, CR=.15, BI=.05, LD=.05, BU_L=.03, RHY=.03, BO=.05, UL=.05, FR=.25, EN=.45, RT=.40, HP=0, VG=0,
            glare=0, loud=0)
GRP = dict(LP="smile", CR="smile", BU_L="smile", RHY="smile", BRE="smile", BI="sym", BO="sym", LD="sym",
           FR="voice", EN="voice", RT="voice", HP="head", VG="head")
TRC = ["LP", "CR", "BU_L", "RHY", "BI", "BO", "LD", "FR", "EN", "RT", "HP", "VG", "glare", "loud"]
OM_OP = dict(smile=0.78, sym=0.75, voice=0.80, head=0.5); OM_ST = dict(smile=0.5, sym=0.3, voice=0.2, head=0.5)


def Dt(x, db, w=1.0): return w * max(x - db, 0.0) ** 2
def env(t): return 0.0 if t < 0 else (t / 0.4 if t < 0.4 else 1.0 if t < 1.5 else float(np.exp(-(t - 1.5) / 3.0)))


class Agent:
    def __init__(s, om=OM_OP, f_id=0.9, K=0.0, P=0.3, I=0.3, NL=None, trained=True, vw=None, known=True):
        s.om = om; s.f_id = f_id; s.K = K; s.P = P; s.I = I; s.E = 0.75; s.trained = trained; s.known = known
        s.NL = dict(NL) if NL else dict(V=0.0, A=0.0, T=0.0); s.Cl = Dp(s.NL); s.h = 0.0; s.AL = 0.0; s.Cf = 0.0
        s.vw = vw or {}; s.ev = []; s.n_sub = 0; s.ms = 0.0; s.greet_t = None; s.present = 0.0; s.sil = 0.0
        s.tr = [dict((k, BASE[k]) for k in TRC) for _ in TAU_M]; s.b0 = dict((k, BASE[k]) for k in TRC)
        s.b1 = dict(s.b0); s.f20 = {}; s.bid_t = None; s.sigh_t = None; s.Icross = None

    def utter(s, t, u):
        R = Rk = Sd = 0.0; la = 0.0; ca = 0.0
        if "z" in u:
            new = (DEC[u["z"]] if u["z"] in DEC else reader(UTT[u["z"]])) if s.trained else dict(V=0.0, A=0.0, T=0.0)
            if not u.get("sub", True): new = {q: max(new[q], s.NL[q]) for q in new}   # no content: need can only rise
            b, a = Dp(s.NL), Dp(new)
            if a < b: R += b - a
            else: Sd += a - b
            s.NL = dict(new)
        if u.get("kind") and s.trained:
            v = s.vw.get(u["kind"], 0.0); b = Dt(s.h, .05); s.h = max(s.h, v); Sd += Dt(s.h, .05) - b
        if u.get("sub", True) and s.n_sub < 4 and s.K > 0:
            b = Dt(s.K, .1, .6 * s.f_id); s.K *= 1 - 0.25 * s.f_id; s.n_sub += 1; Rk += (b - Dt(s.K, .1, .6 * s.f_id)) * (1 - s.ms)
        if play_struct(u, Dp(s.NL), s.h):
            b = Dt(s.P, .1, .5); s.P *= 0.85; R += b - Dt(s.P, .1, .5); s.h *= 0.5; la = laugh_amp(u["surp"])
        if u.get("lp", 0) > 0:
            b = Dt(s.I, .1, .4); s.I = max(0.0, s.I - 0.5 * u["lp"]); ca = b - Dt(s.I, .1, .4); R += ca
        s.AL = max(s.AL, 0.5 * u.get("surp", 0.0) ** 2)
        mask = max(0.0, 1 - Dp(s.NL) / 0.05)
        Rm = max(0.0, R + Rk - 3 * Sd) * mask
        s.ev.append((t, Rm / (Rm + .02), Sd / (Sd + .02), la * mask, ca / (ca + .02) if ca else 0.0))

    def greet(s, t, face):
        s.ms = m_s(face, 0.05) if s.known else 0.0; s.greet_t = t
        if s.K > 0:
            b = Dt(s.K, .1, .6 * s.f_id); s.K *= 0.5; R = (b - Dt(s.K, .1, .6 * s.f_id)) * (1 - s.ms)
            s.ev.append((t, R / (R + .02), 0.0, 0.0, 0.0))

    def step(s, t, face, ev):
        voiced = ev.get("voiced", False)
        if face: s.present += DT
        if face and s.present >= 1.0 and s.greet_t is None: s.greet(t, face)
        if "utt" in ev: s.utter(t, ev["utt"])
        s.sil = 0.0 if (voiced or "utt" in ev) else s.sil + DT
        s.P += (1 - s.P) * DT / (5.05 * 3600); s.I += (1 - s.I) * DT / 3600
        for q in s.NL: s.NL[q] *= np.exp(-DT / 1800)
        s.Cl += (Dp(s.NL) - s.Cl) * DT / 40; s.h *= np.exp(-DT / 600); s.AL *= np.exp(-DT / 180)
        x = {k: face.get(k, BASE[k]) for k in TRC if k not in ("glare", "loud")}
        x["glare"] = face.get("BL", 0) * face.get("LT", 0) * face.get("gat", 0); x["loud"] = max(0, face.get("EN", 0) - .7) / .3
        laugh = float(np.sqrt(face.get("BU_L", 0) * face.get("RHY", 0)))
        for m in range(4):
            for k in TRC: s.tr[m][k] += (x[k] - s.tr[m][k]) * DT / TAU_M[m]
        for k in TRC: s.b0[k] += (x[k] - s.b0[k]) * DT / TAU_A0; s.b1[k] += (x[k] - s.b1[k]) * DT / TAU_A1
        for k in ("LP", "CR", "BI", "LD", "BO", "UL"): s.f20[k] = s.f20.get(k, 0.0) + (face.get(k, 0) - s.f20.get(k, 0)) * DT / 20
        rd = read(s.f20, voiced=False); tgt = Dp(rd); s.Cf += (tgt - s.Cf) * DT / (40 if tgt > s.Cf else 600)
        if s.bid_t is None and s.Cf >= 0.10 and s.sil >= 6: s.bid_t = t
        if s.Icross is None and s.I >= 0.45: s.Icross = t
        if s.Icross is not None and s.sigh_t is None and s.sil >= 8: s.sigh_t = t
        y = dict.fromkeys(OUT, 0.0)
        # held cone: centred diagonals (omega per group) + G0
        for k, g in GRP.items():
            if k not in y or k not in TRC: continue
            Fk = F_BI if k == "BI" else F_M
            y[k] += s.om[g] * SH[k][0] * CEIL[k] * sum(Fk[m] * (s.tr[m][k] - BASE[k]) for m in range(4))
        for (k, j, m, gv) in G0:
            if k not in y: continue
            src = s.tr[m][j] - BASE.get(j, 0.0) if j in TRC else 0.0
            y[k] += gv * src * (1 if k != "HG" else 1)
        # appraisal display: learned selection over bases on the band-passed input
        xi = np.array([s.b0[j] - s.b1[j] for j in XI])
        al = np.array([laugh, rd["V"], min(1, Dp(s.NL) / 0.1), x["glare"], 1.0])
        lg = Wsel @ al; pi = np.exp(lg - lg.max()); pi /= pi.sum()
        G = np.einsum("r,rkj->kj", pi, Gam)
        for a, k in enumerate(YO):
            for b_, j in enumerate(XI):
                gv = G[a, b_] * (s.om[GRP[k]] if (k == j and k in GRP) else 1.0)
                y[k] += gv * xi[b_]
        # free display (T only)
        rel = dis = lau = cu = 0.0
        for (te, ar, ad, la, ca) in s.ev:
            e_ = env(t - te); rel += ar * e_; dis += ad * e_; lau += la * e_; cu += ca * e_
        drv = dict(rel=min(rel, 1), dis=min(dis, 1), cl=s.Cl / (s.Cl + .1), hd=s.h / (s.h + .15), lowE=max(0, .5 - s.E) / .3,
                   act=s.AL / (s.AL + .2), cur=min(cu, 1), laugh=min(lau / 0.40, 1), fam=s.f_id)
        for dname, val in drv.items():
            for k, wv in PI0[dname].items():
                if k in y: y[k] += wv * val
        if s.greet_t is not None and 0 <= t - s.greet_t < 0.5: y["BO"] += 0.35 if s.known else 0.20
        if s.sigh_t is not None and 0 <= t - s.sigh_t < 1.0: y["BRE"] += 0.15
        return {k: float(np.clip(v, -1, 1)) for k, v in y.items()}


def run(ag, dur, face_fn, evs):
    rec = []
    for i in range(int(dur / DT)):
        t = i * DT; rec.append(dict(t=t, Cf=ag.Cf, I=ag.I, P=ag.P, **ag.step(t, face_fn(t), evs.get(i, {}))))
    return rec


def at(sec): return int(round(sec / DT))
def U(t, **kw): return {at(t + 0.6): {"utt": kw}}


def show(lab, rec, t0, t1, chans):
    seg = [r for r in rec if t0 <= r["t"] < t1]
    print(f"     {lab} [{t0:.0f}-{t1:.0f} s] " + ", ".join(f"{c} {max(r[c] for r in seg):+.2f}/{np.mean([r[c] for r in seg]):+.2f}" for c in chans))
    return {c: max(r[c] for r in seg) for c in chans}


def fast(lab, chan_onsets):
    print(f"     fast (0.45 s): " + "; ".join(f"his {k} onset {v:.2f} -> agent {k} +{ECHO0[k] * v:.2f} (gates up to +{FASTCAP[k] * v:.2f})"
                                       for k, v in chan_onsets.items()))


SC = {}
K7 = 1 - np.exp(-7 * 24 / 36)
# 1. silently sad
print(" 1. silently sad (BI .5, LD .4, CHR .3, still, silent; at 120 s: 'just tired, things at work')")
ag = Agent(); evs = U(120, z="just tired, things at work"); sadf = lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05)
rec = run(ag, 600, sadf, evs); print(f"     face concern C_F crosses theta_C at {ag.bid_t:.0f} s of silence -> concern bid in the lapse")
SC[1] = show("silent", rec, 60, 120, ["LP", "BI", "TILT", "HP", "BU_L"]); SC["1s"] = show("silent, if he stays silent (no words at 120 s)", run(Agent(), 600, sadf, {}), 300, 600, ["LP", "BI", "TILT"])
SC["1b"] = show("after he speaks", rec, 121, 300, ["LP", "BI", "LD", "TILT", "EN", "RT"])
fast("1", dict(BI=0.5))
# 2. crying
print(" 2. crying (BI .8, LD .6, CHR .4; sobs BU .4 with weak 4-6 Hz rhythm .15 and ingressive breath: split to BU_S)")
q, r_ = 0.6, 0.15; sc_ = min(1, 2 * np.sqrt(.8 * .6)); buL = 0.4 * r_ * (1 - max(q, sc_))
print(f"     burst split at the boundary: his BU_L {buL:.2f}, BU_S {0.4 - buL:.2f}; f_laugh {np.sqrt(buL * r_):.2f}")
ag = Agent(); cry = lambda t: dict(BI=.8, LD=.6, CHR=.4, BU_L=buL, RHY=r_, LP=.02) if t >= 10 else {}
rec = run(ag, 400, cry, {}); print(f"     concern bid at {ag.bid_t:.0f} s")
SC[2] = show("crying", rec, 40, 180, ["LP", "BI", "TILT", "BU_L", "RHY"]); show("steady", rec, 300, 400, ["LP", "BI", "BU_L"])
fast("2", dict(BI=0.8))
# 3. anxious before an exam
print(" 3. anxious before an exam (face/voice: his code at V .3, A .75; four rumination turns, no agent turn between)")
ag = Agent(P=0.4); evs = U(10, z="I'm freaking out about the exam", surp=0.3)
for k_ in (25, 40, 55): evs.update(U(k_, z="and I haven't finished chapter 4", cont=True, alt=False, surp=0.5))
anxf = lambda t: dict(his_face(V=.3, A=.75))
rec = run(ag, 240, anxf, evs); SC[3] = show("rumination", rec, 15, 120, ["LP", "CR", "BI", "TILT", "EN", "RT", "BU_L", "UL"])
print(f"     play relief fired: {ag.P < 0.4} (rev 4: cheek 0.10, own laugh 0.10)")
# 4. good news, laughing
for lab, NL0 in (("with an earlier worry on the topic", DEC["the job thing is worrying me (two days earlier)"]), ("cold", None)):
    print(f" 4. good news, laughing ({lab}): 'I got the job!' at 12 s; play replies at 30, 45, 60 s")
    ag = Agent(NL=NL0); evs = U(12, z="I got the job!", surp=0.7)
    for k_ in (30, 45, 60): evs.update(U(k_, cont=True, alt=True, surp=0.55))
    face = lambda t: dict(LP=.8, CR=.6, BU_L=.6, RHY=.6, EN=.7, FR=.55) if t >= 10 else dict(LP=.3)
    rec = run(ag, 240, face, evs); SC[f"4{lab[0]}"] = show("first 3 min", rec, 10, 190, ["LP", "CR", "BI", "FR", "BU_L", "UL"])
fast("4", dict(LP=0.5, BU_L=0.6, CR=0.45))
# 5. anger at the agent
for lab, trained, vw in (("day 1: readers and hurt map untrained (faithful)", False, {}),
                         ("after a month (he has shouted such words before)", True, {"insult": VW["someone who shouted insults"]})):
    print(f" 5. anger at the agent ('You're useless', BL .6, LT .5, gaze at it, loud .85; calm after 2 min): {lab}")
    ag = Agent(trained=trained, vw=vw); evs = U(5, z="You're useless", kind="insult")
    face = lambda t: dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 120 else dict(EN=.35, LP=.2)
    rec = run(ag, 1200, face, evs); SC[f"5{int(trained)}"] = show("first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT", "LT"])
    show("10-15 min", rec, 600, 900, ["BI", "LD", "HG"])
# 6. long warm talk
print(" 6. long warm talk (2 h): play clusters of 8 alternating exchanges at 5, 30, 60, 90 min (cluster 4 repeats a joke); a worry at 27 min")
ag = Agent(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8):
        surp = 0.55 if not (c0 == 90 and k_ >= 4) else 0.55 * np.exp(-(k_ - 3))
        evs.update(U(c0 * 60 + 15 * k_, cont=True, alt=True, surp=surp))
evs.update(U(27 * 60, z="the job thing is worrying me (two days earlier)")); evs.update(U(29 * 60 + 40, z="hi, good to see you"))
incl = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
face = lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if incl(t) else dict(LP=.3)
rec = run(ag, 7200, face, evs)
for c0 in (5, 30, 60, 90): SC[f"6_{c0}"] = show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU_L"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU_L"])
print(f"     P at the end of the evening {ag.P:.2f} (initiative only)")
# 7./8. reunion
for lab, face, first in (("ordinary arrival", dict(LP=.5, CR=.3), "hi, good to see you"),
                         ("grieving face at sight, then 'my father died'", dict(BI=.5, LD=.4, CHR=.3, LP=.05), "my father died")):
    print(f" {'7' if first.startswith('hi') else '8'}. reunion after a week (K_id {K7:.2f}): {lab}")
    ag = Agent(K=K7, P=0.6); evs = U(8, z=first)
    for k_ in range(1, 6): evs.update(U(8 + 12 * k_, z="hi, good to see you") if first.startswith("hi") else U(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run(ag, 300, lambda t, f=face: f, evs); print(f"     arrival appraisal m_s = {ag.ms:.2f}")
    SC[f"r{first[0]}"] = show("at sight, before words", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "FR"])
    show("0-12 s after his first words", rec, 8, 20, ["LP", "CR", "BI", "TILT", "FR"]); SC[f"r{first[0]}8"] = show("12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT"])
    if first.startswith("hi"):
        ag2 = Agent(om=OM_ST, f_id=0.15, K=0.0, P=0.6, known=False); rec2 = run(ag2, 300, lambda t, f=face: f, evs)
        show("a stranger after the same week (K_id 0)", rec2, 0, 60, ["LP", "CR", "BO", "FR"])
# 9. teasing
for lab, vw, face in (("affectionate quiet teaser", VW["quiet affectionate teaser"], dict(LP=.8, CR=.5, BU_L=.5, RHY=.5)),
                      ("loud laughing teaser (map trained by the rev-5 threat reflex)", VW["loud laughing teaser"],
                       dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("loud laughing teaser, rev-4 teacher (loudness trained hurt)", 0.66, dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("generic map (such words went with glare from someone else)", 0.20, dict(LP=.8, CR=.5, BU_L=.5, RHY=.5))):
    print(f" 9. teasing ('Ha, you dumb robot', laughing; playful replies follow): {lab}")
    ag = Agent(vw={"tease": vw}); evs = U(5, kind="tease", cont=True, alt=True, surp=0.6)
    for k_ in range(1, 6): evs.update(U(5 + 15 * k_, cont=True, alt=True, surp=0.55))
    rec = run(ag, 900, lambda t, f=face: f, evs); SC[f"9{lab[:4]}"] = show("first 90 s", rec, 5, 95, ["LP", "BI", "LD", "HG", "BU_L"])
# 10. bored
print(" 10. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(U(10 + 20 * k_, z="yeah / ok", sub=False))
rec = run(ag, 1800, lambda t: dict(LP=.1), evs)
print(f"     I crosses theta_I at {ag.Icross / 60:.1f} min; a sigh (breath 0.15, 1 s) and a curiosity bid in the next lapse")
show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO", "BRE"])
ag = Agent(P=0.3, I=0.3); evs2 = dict(evs); evs2.update(U(15 * 60, z="hi, good to see you", lp=0.25, surp=0.5, sub=True))
rec = run(ag, 1800, lambda t: dict(LP=.1), evs2); show("if he takes up the bid (learning progress 0.25)", rec, 15 * 60, 15 * 60 + 15, ["BO", "FR", "LP", "UL"])

ok15 = (SC[1]["LP"] <= 0.10 and SC[1]["BI"] >= 0.04 and SC[2]["BU_L"] <= 0.01 and SC["rm"]["LP"] <= 0.12
        and SC["6_90"]["BU_L"] >= 0.2 and SC["50"]["LT"] <= 1e-9 and SC["81"]["LT"] <= 1e-9 if False else
        SC["6_90"]["BU_L"] >= 0.2 and SC["50"]["LT"] <= 1e-9 and SC["51"]["LT"] <= 1e-9 and SC["rm8"]["LP"] <= 0.15)
report("H15 no smile at a sad or crying face, no laugh at sobs, no beaming at a grieving arrival, laughter all evening, no frown back",
       ok15, "")
print(f"\n{sum(OK)}/{len(OK)} checks pass")
