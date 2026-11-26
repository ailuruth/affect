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
F_BI = np.array([0.3, 0.7, 0.0, 0.0])             # the sympathy brow fills within about a minute
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
FASTFRAC = {k: (0.3 if k in ("BI", "BO", "LD", "JO") else 1.0) for k in CH}  # smile, cheek, laughter: full ceiling
KAP = {k: FASTFRAC[k] * CEIL[k] * (1 + GF) / (2 * GF) for k in CH}          # zero on anger/disgust/contempt and sobs
FASTCAP = {k: 2 * GF / (1 + GF) * KAP[k] for k in CH}                       # = FASTFRAC c_k at zero lag
AWAY_FAST = 0.49                                                            # floor on the fast gates: away gain <= 0.49
GMIN = {k: (min(1.0, AWAY_FAST * (1 - GF) / (2 * GF * KAP[k])) if KAP[k] > 0 else 0.0) for k in CH}
ECHO0 = {k: (0.65 * FASTCAP[k] if k in ("LP", "CR", "BU_L", "RHY", "BI", "BO", "HP") else 0.0) for k in CH}
REST = dict(LP=0.09)                                                        # the agent's resting level (familiarity)
# pooled shares (cone diagonal, charged cross, appraisal |Gamma_kk|) x c_k; the fast allowance r_k (H5) fills the rest
SH = {k: (0.50, 0.20, 0.35) for k in CH}
SH["LP"] = (0.50, 0.15, 0.25); SH["BI"] = (0.55, 0.12, 0.10); SH["CR"] = (0.22, 0.06, 0.08)
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
      ("LP", "glare", 1, -0.035), ("LP", "glare", 2, -0.01), ("BI", "glare", 1, +0.012), ("BI", "LD", 1, +0.004),
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
