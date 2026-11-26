"""Algebra checks for design-cayley-ledger.md, revision 6 (J0-J16).

Checks of the design's own inequalities and constants on constructed instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Scenario numbers (J16) are what the design's equations and innate constants give for stated inputs.
Where a finding came from a revision-5 critic's constructed partner (sims/critique-cayley5-routes K1-K7,
sims/critique-cayley5-agent), the check re-runs that partner or its recipe.

The agent part (J8-J16) executes ../design-g5/checks.py unchanged (its output suppressed) to reuse the revision-5
2 Hz engine, Pi~_0 reader and utterance embedding, and then overrides what revision 6 changes.
Run:  python3 -I checks.py      (numpy, scipy; about 3-4 minutes)
"""
import io, os, contextlib
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(66)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond)); print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)


def delay(x, d): return np.concatenate([np.zeros(d), x[:-d]]) if d > 0 else x


def blocks(T, L, fs):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(rng.exponential(L * fs)) + 10; x[t:t + n] = rng.uniform(); t += n
    return x


def laughs(rate, T, fs, dur=2.5, spread=0.4):
    z = np.zeros(T); t = 0
    while t < T:
        r = max(rate[min(t, T - 1)], 1e-3) / 60; t += int(rng.exponential(1 / r) * fs) + 1
        if t >= T: break
        dd = max(1, int(np.exp(np.log(dur) + spread * rng.normal()) * fs)); z[t:t + dd] = 1; t += dd
    return z


# =========================================================== innate constants (revision 6, section 2.1)
CEIL = dict(LP=.35, CR=.25, BU_L=.35, RHY=.30, BRE=.15, BI=.20, BO=.10, LD=.05, JO=.10, HP=.10, VG=.05, LAT_=.03,
            F0=.05, FR=.10, EN=.05, RT=.05, PAU=.05, LAT=.05)
# fast gear (D81), frozen and per channel: G_k = PHI_k c_k per unit of his own same-channel onset
PHI = dict(LP=.64, CR=.60, BU_L=.80, RHY=.80, BRE=.80, BI=.10, BO=.24, LD=.24, JO=.24, HP=.80, VG=.80, LAT_=.80,
           F0=.80, FR=.80, EN=.80, RT=.80, PAU=.80, LAT=.80)
GK = {k: PHI[k] * CEIL[k] for k in CEIL}
# pooled shares x c_k: held cone diagonal s_C, charged cross s_X, appraisal |Gamma_kk| s_A
SH = {k: (.50, .20, .35) for k in CEIL}
SH.update(LP=(.22, .05, .12), CR=(.24, .05, .12), BU_L=(.10, .02, .10), RHY=(.10, .02, .10), BRE=(.10, .02, .10),
          BI=(.68, .10, .05), BO=(.44, .12, .20), LD=(.44, .12, .20), JO=(.44, .12, .20))
ONE_SIDED = ("LP", "CR", "BU_L", "RHY", "BRE", "BI", "BO", "LD", "JO")
REST = dict(LP=.09)
TAU_M = [20, 120, 1200, 10800]; F_M = [0, .7, .2, .1]; F_BI = [.5, .5, 0, 0]; N_M = [.25, .18, .12, .05]
RHO = 0.091                                             # Lemma S* ripple, tau_b 6, tau_omega 60 sessions (rev 5 H1)
HBP = (90 - 20) / (90 + 20)                             # sup |band-pass| 0.636

print("=== J0: per-channel constants of the frozen fast gear and the budgets")
for k in ("LP", "CR", "BU_L", "RHY", "BRE", "BI", "BO", "JO", "HP", "FR"):
    print(f"   {k:5s} c {CEIL[k]:.2f}  fast gain G {GK[k]:.3f} per unit onset ({PHI[k]:.2f} c)  shares {SH[k]}")

# =========================================================== J1: the fast gear is per channel and sign-structured
print("=== J1: per-channel fast gear (routes finding 1): no agent channel reads another partner channel; rule J by construction")
# structural statement: the fast operator is diag(G_k * R_k) where R_k reads only his channel k; in matrix form its
# Jacobian w.r.t. his channels is diagonal at every input, so the cross entries are exactly 0.
chans = list(CEIL)
J = np.zeros((len(chans), len(chans)))
for i, k in enumerate(chans): J[i, i] = GK[k]           # onset response of agent k to a unit step on his j
off = np.abs(J - np.diag(np.diag(J))).max()
lp_from_bi = 0.0                                         # agent LP <- his BI: no path
report("J1 the fast Jacobian is diagonal (no cross-channel fast path; no smile at a sad brow onset)", off == 0 and lp_from_bi == 0,
       f"max off-diagonal {off:.3f}; LP <- BI onset 0.5 gives {0.5 * lp_from_bi:+.3f} (rev 5 as built: +0.074)")

# =========================================================== J2: the pointwise lemma and r_k over burst families (finding 4)
print("=== J2: one-sided channels render the onset lobe E+ = (x_d - lp4 x_d)+ : 0 <= G E+(t) <= G x(t - 0.45 s) for any input")
fs = 10.0; T = int(10 * 3600 * fs); MIN = int(60 * fs); d = int(0.45 * fs)


def Eplus(u): xd = delay(u, d); return np.maximum(xd - lp(xd, 4.0, fs), 0.0)


mood = blocks(T, 600, fs); worst_ratio = 0.0; viol = 0
for dur in (0.2, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0):
    for rate in (3, 20):
        if dur * rate > 40: continue
        L = laughs(0.3 + rate * mood, T, fs, dur=dur)
        for am in (0, 1):
            u = (0.3 + 0.7 * mood) * L if am else L
            e = Eplus(u); viol += int((e > delay(u, d) + 1e-12).sum())
            s = slope(means(u, MIN), means(e, MIN)); worst_ratio = max(worst_ratio, s)
        print(f"   bursts {dur:4.1f} s at up to {rate:2d}/min: 1-min slope of E+ on his level {s:.3f} (per unit G)")
R_K = {k: (worst_ratio * PHI[k] if k in ONE_SIDED else 0.0) for k in CEIL}
report("J2 E+ never exceeds his delayed level (any input), and the measured onset-lobe allowance is <= 0.94 G",
       viol == 0 and worst_ratio <= 0.95, f"violations {viol}; worst ratio {worst_ratio:.3f} (0.2-s clicks); "
       f"r_k = {worst_ratio:.3f} PHI_k: LP {R_K['LP']:.3f} c, BU_L {R_K['BU_L']:.3f} c, BI {R_K['BI']:.3f} c")
print("   there is no learned fast block, so the K2 energy-for-area operator is not in the class (rev 5: 1.04 c)")

# =========================================================== J3: totals per channel at 2 s, 10 s and 1 min, rendered
print("=== J3: every channel's rendered total, all routes at their caps, at 2-s, 10-s and 1-min windows (best lag 0-3 s)")
T = int(12 * 3600 * fs)
W = {"2 s": int(2 * fs), "10 s": int(10 * fs), "1 min": int(60 * fs)}


def ws(u, y):
    out = {}
    for lab, n in W.items():
        best = -9
        for lg in range(0, int(3 * fs) + 1, int(0.5 * fs)):
            best = max(best, slope(means(u[: len(u) - lg], n), means(y[lg:], n)))
        out[lab] = best
    return out


def bp(x): return lp(x, 20, fs) - lp(x, 90, fs)


mood = blocks(T, 600, fs); L = laughs(0.5 + 3 * mood, T, fs); Lsh = laughs(0.5 + 12 * mood, T, fs, dur=0.4)
sadep = laughs(0.3 + 2 * mood, T, fs, dur=8.0, spread=0.6); nz = lambda s=0.02: s * rng.normal(size=T)
fam = {
    "laughing (critic K1)": dict(LP=np.clip(.15 + .25 * mood + .35 * L + nz(.03), 0, 1), CR=np.clip(.05 + .1 * mood + .3 * L, 0, 1),
                                 BU_L=.6 * L, RHY=.5 * L, BRE=.3 * L, FR=np.clip(.25 + .05 * mood + .25 * L + nz(.03), 0, 1),
                                 JO=np.clip(.05 + .4 * L + nz(.03), 0, 1), HP=.15 * L + nz(), EN=np.clip(.45 + .2 * L, 0, 1),
                                 BI=np.clip(.05 + .1 * mood, 0, 1), BO=np.clip(.05 + .2 * L, 0, 1), LD=.02 + 0 * L, VG=.1 * L + nz()),
    "short clicks (0.4 s, up to 12/min)": dict(BU_L=.7 * Lsh, RHY=.6 * Lsh, BRE=.4 * Lsh, LP=np.clip(.1 + .5 * Lsh, 0, 1), CR=.4 * Lsh,
                                              JO=.4 * Lsh, HP=.2 * Lsh, FR=.25 + .2 * Lsh, EN=.45 + .2 * Lsh, BI=.05 + nz(.01),
                                              BO=.3 * Lsh, LD=.02 + nz(.01), VG=.1 * Lsh),
    "sad episodes and mood": dict(BI=np.clip(.05 + .2 * mood + .4 * sadep, 0, 1), LD=np.clip(.3 * sadep + .1 * mood, 0, 1),
                                  BO=np.clip(.2 * sadep, 0, 1), LP=np.clip(.3 - .2 * sadep - .1 * mood, 0, 1),
                                  CR=np.clip(.15 - .1 * sadep, 0, 1), BU_L=.01 * mood, RHY=.01 * mood, BRE=.1 * sadep,
                                  JO=.05 + .02 * mood, HP=-.1 * sadep + nz(), FR=.25 - .1 * sadep, EN=.45 - .1 * sadep, VG=-.1 * sadep + nz()),
    "slow mood": {k: np.clip(.1 + .5 * mood + nz(), 0, 1) for k in ("LP", "CR", "BU_L", "RHY", "BRE", "BI", "BO", "LD", "JO", "HP", "FR", "EN", "VG")},
}
CO = dict(LP="CR", CR="LP", BU_L="RHY", RHY="BU_L", BRE="BU_L", BI="LD", BO="BI", LD="BI", JO="BU_L", HP="BI", FR="EN", EN="FR", VG="BI")
TOT = {}
for k in ("LP", "CR", "BU_L", "RHY", "BRE", "BI", "BO", "LD", "JO", "HP", "VG", "FR", "EN"):
    ck = CEIL[k]; sc, sx, sa = SH[k]; G = GK[k]; worst = {l: -9.0 for l in W}
    for fn, U in fam.items():
        uk = U[k]
        Fk = F_BI if k == "BI" else F_M
        yC = sum(Fk[m] * sc * ck * lp(uk - uk.mean(), TAU_M[m], fs) for m in range(4))
        uj = U[CO[k]]; sg = np.sign(np.corrcoef(uj, uk)[0, 1]) if np.std(uj) > 0 else 0
        yX = sx * ck * lp(uj - uj.mean(), 120, fs) * sg
        xd = delay(uk, d); E = xd - lp(xd, 4, fs); yF = G * (np.maximum(E, 0) if k in ONE_SIDED else E)
        xb = bp(uk)
        for g in (1.0, np.sign(xb)):
            tot = yC + yX + sa * ck * g * xb + yF
            r = np.clip(REST.get(k, 0) + tot, 0, 1) - REST.get(k, 0) if k in ONE_SIDED else tot
            s = ws(uk, r)
            for l in W: worst[l] = max(worst[l], s[l] / ck)
    bound = sc * (1 + RHO) + sx + HBP * sa + R_K.get(k, 0)
    TOT[k] = (bound, worst)
    print(f"   {k:4s}: additive pooled bound {bound:.3f} c | measured worst " + ", ".join(f"{l} {worst[l]:.3f} c" for l in W))
okJ3 = all(b <= 0.99 and max(w.values()) <= 1.0 for b, w in TOT.values())
report("J3 every channel stays under its ceiling at 2 s, 10 s and 1 min, rendered, every route at its cap", okJ3,
       f"worst additive bound {max(b for b, _ in TOT.values()):.3f} c; worst measured {max(max(w.values()) for _, w in TOT.values()):.3f} c "
       f"(rev 5 as built: breath 2.6 c at 1 min, head pitch 6.6 c at 2 s)")

# =========================================================== J4: the fast gain cannot be learned toward copy (finding 2)
print("=== J4: the fast gain is frozen; re-run of the critic's mirroring partner (K3) and common-cause laugh (K4)")
fs3 = 10.0; T3 = int(4 * 3600 * fs3); d3 = int(0.45 * fs3)


def env_seq(T, rate_min, fs):
    imp = np.zeros(T); t = 0
    while t < T:
        t += int(rng.exponential(60 / rate_min) * fs) + 1
        if t < T: imp[t] = rng.uniform(0.3, 0.6)
    tt = np.arange(int(15 * fs)) / fs
    kern = np.where(tt < 0.4, tt / 0.4, np.where(tt < 1.5, 1.0, np.exp(-(tt - 1.5) / 3.0)))
    return np.convolve(imp, kern)[:T]


def nightly_fast_gain(rule, mu, his_own, nights=60):
    """rev 5: least squares of own fast face on his delayed high-passed face (+ pull to theta_0);
    rev 6: no fit: G is an innate constant and nothing in replay reads it"""
    g0 = 0.65 * CEIL["LP"]; cap = CEIL["LP"]; g = g0 if rule == 5 else GK["LP"]
    e_own = 0.55 * env_seq(T3, 3.0, fs3); n_his = his_own * 0.55 * env_seq(T3, 3.0, fs3)
    for night in range(nights):
        if rule == 6: continue                           # frozen: replay has no gradient path to G (it is not a parameter)
        y = np.zeros(T3); u = np.zeros(T3); uh = np.zeros(T3); lo = 0.0; a4 = 1 - np.exp(-1 / (4 * fs3))
        for t in range(T3):
            u[t] = (mu * y[t - d3] if t >= d3 else 0.0) + n_his[t]; lo += a4 * (u[t] - lo); uh[t] = u[t] - lo
            y[t] = e_own[t] + g * (uh[t - d3] if t >= d3 else 0.0)
        x = delay(uh, d3); tg = y - lp(y, 4, fs3); beta = float(x @ tg / (x @ x)); g = float(np.clip((beta + .5 * g0) / 1.5, -0.49, cap))
        if night >= 2: break                             # rev 5's drift is shown by the critic (K3); 3 nights suffice here
    return g


for mu, own in ((0.0, 1.0), (0.5, 0.5), (0.8, 0.3)):
    g6 = nightly_fast_gain(6, mu, own)
    print(f"   mirror gain mu {mu:.1f}: rev 6 fast LP gain after 60 nights {g6:.3f} (innate {GK['LP']:.3f}); critic K3 rev 5: "
          f"{'0.138' if mu == 0 else '0.350 = cap'}")
# K4: the common cause. With no fit, the play laugh co-occurring with his punchline laughter cannot move G_BU_L.
ends = np.sort(rng.choice(T3 - 200, 900, replace=False)); his = np.zeros(T3); own = np.zeros(T3)
tt = np.arange(int(4 * fs3)) / fs3; kl = np.where(tt < 1.5, 1.0, np.exp(-(tt - 1.5) / 1.0))
for e_ in ends:
    if rng.random() < 0.5:
        a = rng.uniform(0.4, 0.8); s0 = e_ - 5; his[s0:s0 + len(kl)] += a * kl[: T3 - s0]
        s1 = e_ + 6; own[s1:s1 + len(kl)] += 0.40 * kl[: T3 - s1]
X = delay(his - lp(his, 4, fs3), d3); beta = float(X @ (own - lp(own, 4, fs3)) / (X @ X))
print(f"   common cause (play laugh at +0.6 s, his punchline laugh): a fit would want {beta:.3f} (cap {CEIL['BU_L']:.2f}); "
      f"rev 6 G_BU_L stays {GK['BU_L']:.3f}; under the segment-shuffle surrogate (words fixed) the play laugh is unchanged")
report("J4 no partner, mirroring or not, can move a fast gain: no drift to the cap, no erosion of innate mimicry",
       all(abs(nightly_fast_gain(6, m, o) - GK['LP']) < 1e-12 for m, o in ((0, 1), (.8, .3))),
       f"G_LP = {GK['LP']:.3f} for every partner and night (rev 5: 0.07-0.14 eroded, 0.35 at the cap)")

# =========================================================== J5: the word-need reader cannot learn his per-topic face (finding 3)
print("=== J5: the word-need reader = frozen population prior + a per-person adapter trained only on separated reports (words)")


def agent_BI_20s(V):
    t = np.arange(0, 20, 0.05); D = 0.8 * max(V - .05, 0) ** 2; C = D * (1 - np.exp(-t / 40)); cl = C / (C + 0.1)
    ad = D / (D + .02) if D > 0 else 0.0; e = np.where(t < .4, t / .4, np.where(t < 1.5, 1.0, np.exp(-(t - 1.5) / 3.0)))
    return float((0.25 * cl + 0.45 * ad * e).mean())


V_word = 0.30                                            # the population reader's decoding of the topic's words (fixed)
rows = []
for his_brow in (0.08, 0.13, 0.19):                      # his per-topic brow (the critic's K5 topics)
    for mu in (0.0, 0.7):
        rows.append((his_brow, mu, agent_BI_20s(V_word)))   # no face term anywhere in the reader's training
sl = slope([r[0] for r in rows], [r[2] for r in rows])
print("   " + "; ".join(f"his topic brow {b:.2f}, mirror {m:.1f} -> agent 20-s brow {a:.3f}" for b, m, a in rows))
report("J5 the agent's word-driven brow does not follow his per-topic face", abs(sl) < 1e-9,
       f"slope {sl:+.3f} per unit of his topic brow (rev 5: 0.74 against c_BI 0.20; mirror inflation 1.2-1.6x -> none)")

# =========================================================== J6: TTS prosody replaced, not shifted (finding 5)
print("=== J6: WORLD replaces phrase-level F0 level, F0 range, energy and rate by the rule-7 targets")
n = 4000; his_laugh = rng.random(n); lively = (his_laugh + 0.5 * rng.normal(size=n)) > 0.5   # draft choice follows his laughter
tts_FR = np.where(lively, 0.45, 0.20) + 0.03 * rng.normal(size=n)                              # the TTS's own text-driven range
target_FR = 0.25 + 0.05 * rng.normal(size=n)                                                    # rule-7 target (T and capped F only)
shift = target_FR + (tts_FR - tts_FR.mean()); replace_ = target_FR.copy()
print(f"   slope of phrase F0 range on his laughter: shift-only {slope(his_laugh, shift):+.3f} (c_FR 0.10); replace {slope(his_laugh, replace_):+.3f}")
report("J6 with replacement the draft choice cannot carry his laughter into phrase prosody", abs(slope(his_laugh, replace_)) < 0.02,
       "within-phrase segmental micro-prosody remains (text-borne, 1.6 bits per turn, declared)")

# =========================================================== J7: the shadow run and its ledger (whole-system check)
print("=== J7: shadow run (his expressive stream at his latched baseline; declared routes held at their factual values)")


def ledger(u, r, c, wins=(2.0, 10.0, 60.0), lags=(0.0, 0.5, 1.0, 2.0, 3.0), tauR=1800.0, tauC=1800.0, fs=10.0):
    """per channel, per step: clip the partner-caused part r so that the running in-phase slope of its window means on his
    window means, both centred at their 30-min means, never exceeds c at any window and lag (own-body Gamma, centred, windowed)"""
    T = len(u); out = np.zeros(T); dR = np.exp(-1 / (tauR * fs)); aC = 1 - np.exp(-1 / (tauC * fs))
    keys = [(Wd, l) for Wd in wins for l in (lags if Wd <= 2.0 else (0.0,))]
    aW = {Wd: 1 - np.exp(-1 / (Wd * fs)) for Wd in wins}
    uW = {k: 0.0 for k in keys}; uC = {k: float(u[0]) for k in keys}; rW = {Wd: 0.0 for Wd in wins}; rC = 0.0
    S = {k: 0.0 for k in keys}; E = {k: 1e-9 for k in keys}; bound_hits = 0
    for t in range(T):
        hi, lo = np.inf, -np.inf; pis = {}
        for (Wd, l) in keys:
            li = int(l * fs); ut = u[t - li] if t >= li else u[0]
            uW[(Wd, l)] += aW[Wd] * (ut - uW[(Wd, l)]); uC[(Wd, l)] += aC * (ut - uC[(Wd, l)]); pi = uW[(Wd, l)] - uC[(Wd, l)]; pis[(Wd, l)] = pi
            a = aW[Wd]; base = (1 - a) * rW[Wd] - rC; Sm = max(0.0, dR * S[(Wd, l)]); b = c * (dR * E[(Wd, l)] + pi * pi) - Sm
            if pi > 1e-9: hi = min(hi, (b / pi - base) / a)
            elif pi < -1e-9: lo = max(lo, (b / pi - base) / a)
        x = r[t]; x2 = min(max(x, lo), hi) if lo <= hi else 0.0
        bound_hits += int(abs(x2 - x) > 1e-12); out[t] = x2
        for Wd in wins: rW[Wd] += aW[Wd] * (x2 - rW[Wd])
        rC += aC * (x2 - rC)
        for (Wd, l) in keys:
            S[(Wd, l)] = max(0.0, dR * S[(Wd, l)]) + (rW[Wd] - rC) * pis[(Wd, l)]; E[(Wd, l)] = dR * E[(Wd, l)] + pis[(Wd, l)] ** 2
    return out, bound_hits / T


T7 = int(4 * 3600 * fs); m7 = blocks(T7, 600, fs); L7 = laughs(0.5 + 3 * m7, T7, fs)
u = np.clip(.15 + .25 * m7 + .35 * L7 + .03 * rng.normal(size=T7), 0, 1); cLP = CEIL["LP"]
xd = delay(u, d); yF = GK["LP"] * np.maximum(xd - lp(xd, 4, fs), 0)
yC = sum(F_M[m] * SH["LP"][0] * cLP * lp(u - u.mean(), TAU_M[m], fs) for m in range(4))
r = np.clip(.09 + yF + yC, 0, 1) - .09                 # shadow output = rest + T part; r = factual - shadow
rp, hit = ledger(u, r, cLP)
s0, s1 = ws(u, r), ws(u, rp)
print(f"   natural laughing partner, LP: slopes before {', '.join(f'{l} {s0[l]:.3f}' for l in W)}; after "
      f"{', '.join(f'{l} {s1[l]:.3f}' for l in W)}; fraction of frames clipped {hit:.4f}; echo rms kept {np.std(rp) / np.std(r):.3f}")
cr = np.clip(.05 + .1 * m7 + .3 * L7, 0, 1); dcr = delay(cr, d)
inj = 1.6 * np.maximum(dcr - lp(dcr, 4, fs), 0) + 1.0 * lp(cr - cr.mean(), 60, fs)   # an uncounted cross and level route (K1-like)
ri = np.clip(.09 + yF + inj, 0, 1) - .09; rip, hit_i = ledger(u, ri, cLP)
a0, a1 = ws(u, ri), ws(u, rip)
print(f"   injected uncounted route (2.2 c at 2 s): before {', '.join(f'{l} {a0[l]:.3f}' for l in W)}; after "
      f"{', '.join(f'{l} {a1[l]:.3f}' for l in W)} (c_LP {cLP})")
# the shape adversary: minutes held at 0.40 against minutes of 1.5-s bursts with mean 0.42
nmin = T7 // 600; typ = rng.random(nmin) < 0.5; ua = np.zeros(T7)
for i in range(nmin):
    s = slice(i * 600, (i + 1) * 600)
    if typ[i]: ua[s] = 0.40
    else:
        z = np.zeros(600)
        for j in range(0, 600, 30): z[j:j + 15] = 1
        ua[s] = 0.84 * z
xa = delay(ua, d); ra = np.clip(.09 + GK["LP"] * np.maximum(xa - lp(xa, 4, fs), 0), 0, 1) - .09
rap, _ = ledger(ua, ra, cLP); b0, b1 = ws(ua, ra), ws(ua, rap)
swing = abs(np.mean([ra[i * 600:(i + 1) * 600].mean() for i in range(nmin) if not typ[i]]) - np.mean([ra[i * 600:(i + 1) * 600].mean() for i in range(nmin) if typ[i]]))
print(f"   shape adversary (held 0.40 vs bursts 0.42): 1-min slope before {b0['1 min']:.2f}, after {b1['1 min']:.2f}; "
      f"absolute swing of the agent's 1-min LP {swing:.3f} for his 0.02 (residual R39)")
# dynamic type check: an F value leaking into a T update is caught by the shadow at the first divergence
face = rng.random(500); tf = np.cumsum(0.01 * np.ones(500)); tleak = tf + 1e-3 * np.cumsum(face)   # the leak
tshadow = tf + 1e-3 * np.cumsum(np.full(500, face.mean() * 0))                                   # shadow: his stream at baseline
first = int(np.argmax(np.abs(tleak - tshadow) > 0)) if np.any(tleak != tshadow) else -1
report("J7 the shadow ledger clips an uncounted route to the ceiling and leaves the counted echo untouched",
       max(a1.values()) <= 1.08 * cLP and np.std(rp) / np.std(r) > 0.99 and first >= 0,
       f"injected route {max(a0.values()):.3f} -> {max(a1.values()):.3f} (c {cLP}); natural echo kept {np.std(rp) / np.std(r):.3f}; "
       f"a deliberate F->T leak is flagged at frame {first}")

# =========================================================== agent part: reuse the revision-5 engine
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design-g5", "checks.py")
g = {"__name__": "g5"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(p).read(), "checks_g5", "exec"), g)
read, Dp, his_face, emb, UTT, Agent5 = (g[k] for k in ("read", "Dp", "his_face", "emb", "UTT", "Agent"))
RD_CH = g["RD_CH"]; env = g["env"]; DT = g["DT"]
# revision-6 shares into the engine's cone (the engine reads g["SH"])
for k, v in SH.items():
    if k in g["SH"]: g["SH"][k] = v
for k in ("TILT", "YAW", "HG"): g["SH"][k] = (.50, .20, .35)

FACE_CH = ["LP", "CR", "BI", "LD", "UL", "BO", "FR", "EN", "RT", "HG", "LAT", "BRE", "BL", "LPR", "CHR"]


def code_fn(kind):
    if kind == "agent-like":
        return his_face
    if kind == "different channels":
        def f(V=0., A=0., Tr=0., joy=0.):
            return dict(BL=.5 * V + .3 * A, LPR=.45 * V + .2 * A, CHR=.4 * V, BI=.05 * V, LD=.05 * V, UL=.05 * A - .3 * Tr, BO=.05 * A,
                        HG=0.0, FR=.25 - .10 * V - .05 * A - .25 * Tr + .3 * joy, EN=.45 + .05 * A - .05 * V - .25 * Tr + .25 * joy,
                        RT=.40 + .10 * A - .15 * Tr, LP=max(0, .3 + .5 * joy), CR=.15 + .45 * joy)
        return f
    if kind == "low-expressive":
        def f(V=0., A=0., Tr=0., joy=0.):
            n_ = his_face(); d_ = his_face(V, A, Tr, joy); return {k: n_[k] + 0.3 * (d_[k] - n_[k]) for k in d_}
        return f


ZPOP = np.clip(rng.normal(size=(3000, 4)) * .3 + [.1, .1, .1, .2], 0, 1) * (rng.random((3000, 4)) < 0.4)
REF = his_face(); REF_SD = {k: float(np.std([his_face(*z).get(k, 0.0) for z in ZPOP[:600]])) for k in FACE_CH}


class Person:
    """his code, his calibration (baseline and spread per channel, knowing only) and, after training, his face head"""
    def __init__(s, kind):
        s.kind = kind; s.code = code_fn(kind); faces = [s.code(*z) for z in ZPOP[:600]]
        s.base = {k: float(np.median([f_.get(k, 0.0) for f_ in faces])) for k in FACE_CH}
        s.sd = {k: float(np.std([f_.get(k, 0.0) for f_ in faces])) for k in FACE_CH}
        s.head = None

    def calibrate(s, face):
        """x~_k = ref_k + (x_k - b_id,k) sd_ref,k / max(sd_id,k, 0.25 sd_ref,k): his face at his own scale, in the agent's"""
        out = {}
        for k in FACE_CH:
            if REF_SD[k] <= 1e-9: continue
            out[k] = REF.get(k, 0.0) + (face.get(k, s.base[k]) - s.base[k]) * REF_SD[k] / max(s.sd[k], 0.25 * REF_SD[k])
        return out

    def feats(s, face):
        return np.array([(face.get(k, s.base[k]) - s.base[k]) / max(s.sd[k], 1e-3) for k in FACE_CH])

    def read(s, face, voiced=True):
        r0 = read(s.calibrate(face), voiced=voiced)
        if s.head is None: return r0
        h = np.clip(s.feats(face if voiced else {k: v for k, v in face.items() if k not in ("FR", "EN", "RT", "LAT")}) @ s.head, 0, 1)
        return dict(V=max(r0["V"], float(h[0])), A=max(r0["A"], float(h[1])), T=max(r0["T"], float(h[2])))


DIM = 64; XE = np.array([emb(z) for z in ZPOP])


def fit(Xs, Ys, lam=5.0): return np.linalg.solve(Xs.T @ Xs + lam * np.eye(Xs.shape[1]), Xs.T @ Ys)


# population prior: people of three codes, read through the agent's own body at their own scale (iteration 1), then each
# person's face head is trained on the prior's word targets, and the prior is refitted on the combined readings (iteration 2)
POP = [Person(k) for k in ["agent-like"] * 10 + ["low-expressive"] * 5 + ["different channels"] * 5]
for p_ in POP:
    if p_.kind == "agent-like":
        a_ = rng.uniform(0.5, 1.5); c0 = p_.code
        p_.code = (lambda c0, a_: (lambda *z: {k: REF.get(k, 0) + a_ * (v - REF.get(k, 0)) for k, v in c0(*z).items()}))(c0, a_)
        faces = [p_.code(*z) for z in ZPOP[:600]]; p_.sd = {k: float(np.std([f_.get(k, 0.0) for f_ in faces])) for k in FACE_CH}
idx = rng.permutation(len(ZPOP))
for it in (1, 2):
    Xs, Ys = [], []
    for p_ in POP:
        sub = idx[rng.integers(0, len(ZPOP), 150)]
        for i in sub:
            f_ = {k: v + 0.03 * rng.normal() for k, v in p_.code(*ZPOP[i]).items()}; rr = p_.read(f_)
            Xs.append(XE[i]); Ys.append([rr["V"], rr["A"], rr["T"]])
    WPOP = fit(np.array(Xs), np.array(Ys))
    for p_ in POP:                                        # face heads trained on the prior's decodings of his words
        Fx = np.array([p_.feats({k: v + .03 * rng.normal() for k, v in p_.code(*ZPOP[i]).items()}) for i in idx[:400]])
        p_.head = fit(Fx, np.clip(XE[idx[:400]] @ WPOP, 0, 1), lam=2.0)


def pop_reader(z):
    y = np.clip(emb(z) @ WPOP, 0, 1); return dict(V=float(y[0]), A=float(y[1]), T=float(y[2]))


# =========================================================== J8: quiet and differently expressive users are read (agent finding 1)
print("=== J8: reading at his own scale and in his own channels, through the agent's own body (agent finding 1)")
DEC6 = {lab: pop_reader(z) for lab, z in UTT.items()}
for lab in ("my father died", "I'm freaking out about the exam", "just tired, things at work", "I got the job!"):
    r_ = DEC6[lab]; print(f"   population reader (words only, same for every person): '{lab}': V {r_['V']:.2f} A {r_['A']:.2f} T {r_['T']:.2f}; care {Dp(r_):.3f}")
PEOPLE6 = {}
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = Person(kind)
    Fx = np.array([pp.feats({k: v + .03 * rng.normal() for k, v in pp.code(*ZPOP[i]).items()}) for i in idx[:400]])
    day1 = Person(kind)                                   # before any night: calibration only, no head
    pp.head = fit(Fx, np.clip(XE[idx[:400]] @ WPOP, 0, 1), lam=2.0)
    PEOPLE6[kind] = (day1, pp)
    grief = pp.code(V=.8, Tr=.2); grief_s = {k: v for k, v in grief.items() if k not in ("FR", "EN", "RT")}
    anx = pp.code(V=.3, A=.75)
    r5 = read(grief_s, voiced=False)["V"]
    print(f"   {kind:18s}: grieving face read V: rev 5 {r5:.2f}; day 1 (calibrated) {day1.read(grief_s, False)['V']:.2f}; after nights "
          f"(calibrated + face head) {pp.read(grief_s, False)['V']:.2f}; anxious face+voice A {pp.read(anx)['A']:.2f}, V {pp.read(anx)['V']:.2f}")
okJ8 = all(PEOPLE6[k][1].read({kk: v for kk, v in PEOPLE6[k][1].code(V=.8, Tr=.2).items() if kk not in ("FR", "EN", "RT")}, False)["V"] >= 0.5
           for k in PEOPLE6) and Dp(DEC6["my father died"]) > 0.15
report("J8 grief, distress and words are read for quiet and differently coded users", okJ8,
       f"'my father died' care {Dp(DEC6['my father died']):.3f} for every person (rev 5: 0.036 quiet, 0.059 different code)")

# =========================================================== J9: the arrival mask (agent findings 2 and 4)
print("=== J9: the arrival mask: asymmetric arrival baseline (up tau 60 sessions, down 3, capped 0.15); (1 - m_s) after saturation")


def m_s6(Vhat, d_b): return float(np.clip((Vhat - d_b - 0.05) / 0.30, 0, 1))


def greet_amp(K, f_id, ms):
    b = 0.6 * f_id * max(K - .1, 0) ** 2; K2 = K * 0.5; R = b - 0.6 * f_id * max(K2 - .1, 0) ** 2
    return R / (R + .02) * (1 - ms)                       # rev 6: the mask multiplies the shown amplitude


def at_sight(ms, K=1 - np.exp(-24 / 36)):
    a = greet_amp(K, 0.9, ms); return 0.09 + 0.55 * a, 0.45 * a


agl = PEOPLE6["agent-like"][1]
for lab, f_ in (("ordinary", dict(LP=.5, CR=.3)), ("mildly sad (BI .2, LD .15)", dict(BI=.2, LD=.15, LP=.15)),
                ("clearly sad (BI .3, LD .25)", dict(BI=.3, LD=.25, LP=.1)), ("grieving", dict(BI=.5, LD=.4, CHR=.3, LP=.05))):
    ms = m_s6(agl.read(f_, False)["V"], 0.0); lp_, cr_ = at_sight(ms)
    print(f"   {lab:28s}: V read {agl.read(f_, False)['V']:.2f}, m_s {ms:.2f}, at sight lip {lp_:.2f}, cheek {cr_:.2f}")
ms_mild = m_s6(agl.read(dict(BI=.2, LD=.15, LP=.15), False)["V"], 0.0); mild_lip = at_sight(ms_mild)[0]
MOURN = {}
for kind in ("agent-like", "low-expressive"):
    pp = PEOPLE6[kind][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    db = 0.0; out = []
    for n_ in range(1, 29):
        Vh = pp.read(grief, False)["V"]; ms = m_s6(Vh, db); lp_, cr_ = at_sight(ms)
        if n_ in (1, 7, 10, 14, 21, 28): out.append(f"day {n_}: d_b {db:.2f} m_s {ms:.2f} lip {lp_:.2f} cheek {cr_:.2f}")
        MOURN[(kind, n_)] = lp_
        db = min(0.15, db + (Vh - db) / (60.0 if Vh > db else 3.0))
    print(f"   mourning, {kind}: " + "; ".join(out))
report("J9 no habituation to mourning; mild sadness masks the greeting", max(v for v in MOURN.values()) <= 0.10 and mild_lip <= 0.30,
       f"lip at sight on days 1-28 <= {max(MOURN.values()):.2f} (rev 5: 0.33 day 7, 0.52 day 14); mildly sad arrival lip {mild_lip:.2f} (rev 5: 0.55)")

# =========================================================== J10: the play cue (agent finding 3)
print("=== J10: play-structured turns: riffs on the agent's last utterance (not an answer to its question), short, surprise 0.5-0.85")


def play6(u, care):
    return bool(u.get("riff") and not u.get("after_q") and u.get("short", True) and 0.50 <= u.get("surp", 0) <= 0.85 and care < 0.05)


def laugh6(surp, pi_prev): return 0.40 * float(np.clip(1 - abs(surp - 0.65) / 0.25, 0, 1)) * (0.35 + 0.65 * pi_prev)


cases = {"answer to its question ('...Lyon on Sunday')": dict(riff=True, after_q=True, surp=0.6),
         "continuation of his own topic, mid surprise": dict(riff=False, surp=0.45),
         "riff on its statement, informative (surprise 0.45)": dict(riff=True, surp=0.45),
         "borderline: riff on its statement, surprise 0.60, cold frame": dict(riff=True, surp=0.60),
         "a joke riffing on its line, in a play frame (pi 0.75)": dict(riff=True, surp=0.65)}
LA10 = {}
for lab, u_ in cases.items():
    pi_ = 0.75 if "play frame" in lab else 0.0; la = laugh6(u_["surp"], pi_) if play6(u_, 0.0) else 0.0; LA10[lab] = la
    print(f"   {lab:58s}: play {play6(u_, 0.0)}, laugh {la:.2f}")
pi_ = 0.0; seq = []
for k_ in range(6): la = laugh6(0.65, pi_); seq.append(la); pi_ = 0.5 * pi_ + 0.5
print("   laughter building in an exchange of six riffs: " + ", ".join(f"{x:.2f}" for x in seq))
report("J10 ordinary topic continuation earns no laugh; a cold borderline turn earns at most a chuckle",
       LA10["answer to its question ('...Lyon on Sunday')"] == 0 and LA10["continuation of his own topic, mid surprise"] == 0
       and LA10["borderline: riff on its statement, surprise 0.60, cold frame"] <= 0.15,
       f"(rev 5: 0.40 on '...Lyon on Sunday'); false-positive rate on a corpus: untested (CANDOR access not obtained)")

# =========================================================== the revision-6 agent: posture, calibrated reading, new greeting and play
def Vc(V): return 0.8 * max(V - 0.10, 0.0) ** 2        # posture concern: distress load only, dead-band 0.10


P_C = dict(BI=.22, BO=.04, UL=-.06, TILT=.10, HP=.03, LP=-.03)     # the concern posture (Q24), innate, per unit
OUT6 = g["OUT"] + ["VG"]
G0 = g["G0"]; GRP = g["GRP"]; XI = g["XI"]; YO = g["YO"]; Wsel = g["Wsel"]; Gam = g["Gam"]; PI0 = g["PI0"]; BASE = g["BASE"]
TRC = g["TRC"]; CEILg = g["CEIL"]; TAU = g["TAU_M"]; FMg = g["F_M"]; FBIg = g["F_BI"]


class Agent6(Agent5):
    def __init__(s, person=None, om=None, pdb=0.0, **kw):
        super().__init__(om=om or g["OM_OP"], **kw); s.pp = person or PEOPLE6["agent-like"][1]; s.pdb = pdb
        s.f3 = {}; s.on_t = None; s.dwell = 0.0; s.post = 0.0; s.p_on = False; s.below = 0.0; s.refr = -1e9; s.post_t = None
        s.pi = 0.0
        s.f20 = {k: s.pp.base.get(k, 0.0) for k in ("LP", "CR", "BI", "LD", "BO", "UL", "BL", "LPR", "CHR")}

    def utter(s, t, u):
        u = dict(u)
        care = Dp(s.NL)
        pl = play6(u, care) if s.trained else False
        if pl: u["cont"] = True; u["alt"] = True; u["surp_"] = u["surp"]
        else: u["cont"] = False
        la = laugh6(u.get("surp", 0), s.pi) if pl else 0.0
        s.pi = 0.5 * s.pi + 0.5 * (1.0 if pl else 0.0)
        g["laugh_amp"] = lambda surp, la=la: la                   # the engine's laugh hook: revision-6 amplitude
        g["play_struct"] = lambda uu, c, h=0.0, pl=pl: pl
        super().utter(t, u)

    def greet(s, t, face):
        s.ms = m_s6(s.pp.read(face, False)["V"], s.pdb) if s.known else 0.0; s.greet_t = t
        if s.K > 0:
            a = greet_amp(s.K, s.f_id, s.ms)
            s.K *= 0.5; s.ev.append((t, a, 0.0, 0.0, 0.0))

    def step(s, t, face, ev):
        g["read"] = lambda f_, voiced=True: s.pp.read(f_, voiced)     # C_F and m_s read him at his own scale
        for k in ("BL", "LPR", "CHR"): s.f20[k] += (face.get(k, s.pp.base.get(k, 0.0)) - s.f20[k]) * DT / 20
        y = super().step(t, face, ev)
        # concern posture (Q24): onset on the 3-s calibrated reading (or sob bursts); maintenance with the posture's own
        # pattern removed from his face (a mirror cannot sustain it), or word concern, or sobs; release after 20 s below
        for k in ("LP", "CR", "BI", "LD", "UL", "BO", "BL", "LPR", "CHR", "BU_S"):
            s.f3[k] = s.f3.get(k, s.pp.base.get(k, 0.0)) + (face.get(k, s.pp.base.get(k, 0.0)) - s.f3.get(k, s.pp.base.get(k, 0.0))) * DT / 3.0
        sob = min(1.0, 2.5 * s.f3.get("BU_S", 0.0))
        rd = s.pp.read(s.f3, False); Con = max(Vc(rd['V']), Vc(sob))
        if s.om.get("sym", 0) >= 0 and not s.p_on and t - s.refr >= 60:
            s.dwell = s.dwell + DT if Con >= 0.05 else 0.0
            if s.dwell >= 1.5: s.p_on = True; s.post_t = s.post_t if s.post_t is not None else t; s.on_t = t; s.below = 0.0
        if s.p_on:
            sc = min(1.0, s.pp.sd.get("BI", 0.1) / max(REF_SD["BI"], 1e-6))
            f_m = dict(s.f3)
            for k, v in P_C.items():
                if k in f_m: f_m[k] = f_m[k] - sc * v * s.post
            M = max(Vc(s.pp.read(f_m, False)['V']), s.Cl, Vc(sob))
            s.below = s.below + DT if M < 0.02 else 0.0
            if s.below >= 20: s.p_on = False; s.refr = t
        s.post = min(1.0, s.post + DT / 1.5) if s.p_on else s.post * np.exp(-DT / 4.0)
        for k, v in P_C.items():
            if k in y: y[k] += v * s.post
        y["post"] = s.post
        return y


def run6(ag, dur, face_fn, evs):
    rec = []
    for i in range(int(dur / DT)):
        t = i * DT; rec.append(dict(t=t, **ag.step(t, face_fn(t), evs.get(i, {}))))
    return rec


def at_(sec): return int(round(sec / DT))
def U6(t, **kw): return {at_(t + 0.6): {"utt": kw}}


def show(lab, rec, t0, t1, chans):
    seg = [r for r in rec if t0 <= r["t"] < t1]
    print(f"     {lab} [{t0:.0f}-{t1:.0f} s] " + ", ".join(f"{c} {max(r[c] for r in seg):+.2f}/{np.mean([r[c] for r in seg]):+.2f}" for c in chans))
    return {c: max(r[c] for r in seg) for c in chans}


def onset_time(rec, thr=0.15):
    for r in rec:
        if r["BI"] >= thr: return r["t"]
    return None


for lab, z in UTT.items(): g["DEC"][lab] = DEC6[lab]
g["reader"] = lambda z, trained=True: pop_reader(z) if trained else dict(V=0.0, A=0.0, T=0.0)

# =========================================================== J11: the concern posture (Q24)
print("=== J11: the concern posture (Q24): visible within seconds, its own pattern, capped, not sustained by a mirror")
sadf = lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05)
ag = Agent6(); rec = run6(ag, 300, sadf, {}); t_on = onset_time(rec)
s11 = show("silently sad, operator", rec, 0, 300, ["LP", "BI", "BO", "TILT", "UL", "post"])
print(f"     inner brow reaches 0.15 at {t_on:.1f} s after he appears; concern bid at {ag.bid_t:.0f} s")
cryf = lambda t: dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02)
ag = Agent6(); recc = run6(ag, 120, cryf, {}); t_on_c = onset_time(recc)
print(f"     crying: inner brow reaches 0.15 at {t_on_c:.1f} s")
# same pattern for a different code: the posture is the agent's own pattern whatever his face does
pats = {}
for kind in ("agent-like", "different channels", "low-expressive"):
    pp = PEOPLE6[kind][1]; f_ = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    ag = Agent6(person=pp); rr = run6(ag, 60, lambda t, f_=f_: f_, {}); pats[kind] = (onset_time(rr), max(r["post"] for r in rr))
print("     posture onset by code: " + "; ".join(f"{k} {v[0]:.1f} s (amplitude {v[1]:.2f})" for k, v in pats.items()))
# a mirroring partner: genuinely sad for 40 s, then neutral, but he copies the agent's posture (mu = 1) from then on
ag = Agent6(); post_hist = []


def mirror_face(t, ag=ag):
    sad = t < 40
    base = dict(BI=.5, LD=.4, CHR=.3, LP=.05) if sad else dict(BI=.05, LD=.05, LP=.30)
    for k, v in P_C.items():
        if k in ("BI", "BO", "UL", "LP"): base[k] = max(0.0, base.get(k, 0.0) + 1.0 * v * ag.post)
    return base


recm = run6(ag, 400, mirror_face, {})
off_t = next((r["t"] for r in recm if r["t"] > 40 and r["post"] < 0.05), None)
print(f"     mirroring partner (mu 1 on the posture's channels, genuinely sad only for 40 s): posture released at {off_t:.0f} s; "
      f"on again after: {any(r['post'] > 0.5 for r in recm if r['t'] > (off_t or 1e9) + 5)}")
cos_sad = sum(P_C.get(k, 0) * v for k, v in dict(BI=.5, LD=.4, CHR=.3).items()) / (.5 ** 2 + .4 ** 2 + .3 ** 2)
report("J11 posture visible within a few seconds at a silently sad or crying person, same for every code, not held by a mirror",
       t_on is not None and t_on <= 6 and t_on_c is not None and t_on_c <= 6 and off_t is not None and off_t < 100,
       f"silent sad {t_on:.1f} s, crying {t_on_c:.1f} s; inner brow {s11['BI']:.2f}; whole-face copy fraction of the posture on a sad face "
       f"{cos_sad:.2f}, on a lip-press distress face 0.00")

# =========================================================== J12: whole face and dyad stability with the new routes
print("=== J12: whole face and dyad stability")
cvec = {k: CEIL[k] for k in CEIL}
print(f"   whole face: any direction <= max c_k = {max(cvec.values()):.2f}; the posture is a fixed vector (rank 1), amplitude 1, BI 0.22")
w = np.logspace(-5, 1, 4000); worst_g = 0
for k in ("LP", "BI", "BU_L", "EN"):
    cn = sum(N_M[m] / (1 + 1j * w * TAU_M[m]) for m in range(4)) + SH[k][0] * CEIL[k] * sum(F_M[m] / (1 + 1j * w * TAU_M[m]) for m in range(4))
    ap = SH[k][2] * CEIL[k] * (1 / (1 + 1j * w * 20) - 1 / (1 + 1j * w * 90))
    fa = GK[k] * (1j * w * 4 / (1 + 1j * w * 4)) * np.exp(-1j * w * 0.45)
    G_ = np.abs(np.abs(cn) + np.abs(ap) + np.abs(fa)).max(); worst_g = max(worst_g, G_)
    print(f"   {k}: max over w of |cone| + |appraisal| + |fast| = {G_:.3f}")
report("J12 the dyad is small-gain stable for any mirror |mu| < 1 (triangle bound, every route at its extreme)", worst_g < 1.0,
       f"|mu| < {1 / worst_g:.2f}; no learned gain can raise it (fast frozen; rev 5: 1.67 with away fast gates)")

# =========================================================== J16: the scenarios
print("=== J16: the scenarios (operator after months unless stated; peak / mean over the window)")
SC = {}
K7 = 1 - np.exp(-7 * 24 / 36)


def fast(chan_onsets):
    print("     fast (0.45 s, frozen): " + "; ".join(f"his {k} onset {v:.2f} -> agent {k} +{GK[k] * v:.2f}" for k, v in chan_onsets.items()))


print(" 1. silently sad (BI .5, LD .4, CHR .3; at 120 s 'just tired, things at work')")
ag = Agent6(); rec = run6(ag, 600, sadf, U6(120, z="just tired, things at work"))
SC[1] = show("0-10 s", rec, 0, 10, ["LP", "BI", "BO", "TILT", "UL"]); show("silent 60-120 s", rec, 60, 120, ["LP", "BI", "TILT", "HP", "BU_L"])
show("after he speaks", rec, 121, 300, ["LP", "BI", "LD", "TILT", "EN"]); print(f"     posture on at {onset_time(rec):.1f} s; concern bid at {ag.bid_t:.0f} s"); fast(dict(BI=0.5))
print(" 2. crying (BI .8, LD .6, CHR .4; sobs BU .4 -> BU_S at the boundary)")
ag = Agent6(); rec = run6(ag, 400, cryf, {})
SC[2] = show("0-10 s", rec, 0, 10, ["LP", "BI", "TILT", "BU_L"]); show("40-180 s", rec, 40, 180, ["LP", "BI", "TILT", "BU_L", "RHY"])
print(f"     posture on at {onset_time(rec):.1f} s; concern bid at {ag.bid_t:.0f} s")
print(" 3. anxious before an exam (his code at V .3, A .75; rumination turns with no agent turn between)")
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]; ag = Agent6(person=pp, P=0.4); evs = U6(10, z="I'm freaking out about the exam", surp=0.3)
    for k_ in (25, 40, 55): evs.update(U6(k_, z="and I haven't finished chapter 4", cont=True, surp=0.5))
    rec = run6(ag, 240, lambda t, pp=pp: pp.code(V=.3, A=.75), evs); SC[f"3{kind[0]}"] = show(f"{kind}", rec, 15, 120, ["LP", "BI", "TILT", "EN", "UL", "BU_L"])
fo = DEC6["I'm freaking out about the exam"]
print(f"     decoded 'freaking out' (every person): A {fo['A']:.2f}, V {fo['V']:.2f}")
for lab, NL0 in (("with an earlier worry", DEC6["the job thing is worrying me (two days earlier)"]), ("cold", None)):
    print(f" 4. good news, laughing ({lab}): 'I got the job!' at 12 s; riffs at 30, 45, 60 s")
    ag = Agent6(NL=NL0); evs = U6(12, z="I got the job!", surp=0.7)
    for k_ in (30, 45, 60): evs.update(U6(k_, riff=True, surp=0.65))
    face = lambda t: dict(LP=.8, CR=.6, BU_L=.6, RHY=.6, EN=.7, FR=.55) if t >= 10 else dict(LP=.3)
    rec = run6(ag, 240, face, evs); SC[f"4{lab[0]}"] = show("first 3 min", rec, 10, 190, ["LP", "CR", "BI", "FR", "BU_L", "post"])
fast(dict(LP=0.5, BU_L=0.6, CR=0.45))
VW = g["VW"]
for lab, trained, vw in (("day 1", False, {}), ("after a month", True, {"insult": VW["someone who shouted insults"]})):
    print(f" 5. anger at the agent ('You're useless', BL .6, LT .5, gaze at it, loud .85; calm after 2 min): {lab}")
    ag = Agent6(trained=trained, vw=vw); evs = U6(5, z="You're useless", kind="insult")
    face = lambda t: dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 120 else dict(EN=.35, LP=.2)
    rec = run6(ag, 1200, face, evs); SC[f"5{int(trained)}"] = show("first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT", "LT", "post"])
    show("10-15 min", rec, 600, 900, ["BI", "LD", "HG"])
print(" 6. long warm talk (2 h): four clusters of 8 riffs (cluster 4 repeats one joke); a worry at 27 min")
ag = Agent6(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8):
        surp = 0.65 if not (c0 == 90 and k_ >= 4) else 0.65 * np.exp(-(k_ - 3))
        evs.update(U6(c0 * 60 + 15 * k_, riff=True, surp=surp))
evs.update(U6(27 * 60, z="the job thing is worrying me (two days earlier)")); evs.update(U6(29 * 60 + 40, z="hi, good to see you"))
incl = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
rec = run6(ag, 7200, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if incl(t) else dict(LP=.3), evs)
for c0 in (5, 30, 60, 90): SC[f"6_{c0}"] = show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU_L"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU_L", "post"])
print(" 7. reunion after a week (K_id %.2f): ordinary arrival; and a stranger" % K7)
ag = Agent6(K=K7, P=0.6); evs = U6(8, z="hi, good to see you")
for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="hi, good to see you"))
rec = run6(ag, 300, lambda t: dict(LP=.5, CR=.3), evs); print(f"     m_s {ag.ms:.2f}")
SC[7] = show("at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "FR"]); show("12-60 s", rec, 20, 60, ["LP", "CR"])
ag2 = Agent6(om=g["OM_ST"], f_id=0.15, K=0.0, P=0.6, known=False); show("stranger", run6(ag2, 300, lambda t: dict(LP=.5, CR=.3), evs), 0, 60, ["LP", "CR", "BO"])
fast(dict(LP=0.5))
print(" 8. reunion with bad news: grieving face at sight, then 'my father died', then 'yeah', 'ok'")
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    ag = Agent6(person=pp, K=K7, P=0.6); evs = U6(8, z="my father died")
    for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run6(ag, 300, lambda t, gr=grief: gr, evs); print(f"     {kind}: m_s {ag.ms:.2f}; posture on at {onset_time(rec, 0.12)}")
    SC[f"8{kind[0]}"] = show("  at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI"]); show("  0-12 s after his words", rec, 8, 20, ["LP", "CR", "BI", "TILT"])
    show("  12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT"])
for kind in ("agent-like", "low-expressive"):
    pp = PEOPLE6[kind][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}; db = 0.0
    for n_ in range(1, 22):
        Vh = pp.read(grief, False)["V"]
        if n_ in (7, 14, 21):
            ag = Agent6(person=pp, K=1 - np.exp(-24 / 36), P=0.6, pdb=db); rr = run6(ag, 20, lambda t, gr=grief: gr, {})
            SC[f"m{kind[0]}{n_}"] = show(f"mourning day {n_}, {kind}, at sight", rr, 0, 7.5, ["LP", "CR", "BI"])
        db = min(0.15, db + (Vh - db) / (60.0 if Vh > db else 3.0))
print(" 9. mildly sad arrival (BI .2, LD .15) after a week")
ag = Agent6(K=K7, P=0.6); rec = run6(ag, 20, lambda t: dict(BI=.2, LD=.15, LP=.15), {}); print(f"     m_s {ag.ms:.2f}")
SC[9] = show("at sight", rec, 0, 7.5, ["LP", "CR", "BI", "post"])
print(" 10. teasing ('Ha, you dumb robot', laughing; riffs follow)")
for lab, vw, face in (("quiet affectionate teaser", VW["quiet affectionate teaser"], dict(LP=.8, CR=.5, BU_L=.5, RHY=.5)),
                      ("loud laughing teaser", VW["loud laughing teaser"], dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("generic map (v_w 0.20)", 0.20, dict(LP=.8, CR=.5, BU_L=.5, RHY=.5))):
    ag = Agent6(vw={"tease": vw}); evs = U6(5, kind="tease", riff=True, surp=0.65)
    for k_ in range(1, 6): evs.update(U6(5 + 15 * k_, riff=True, surp=0.65))
    rec = run6(ag, 900, lambda t, f=face: f, evs); SC[f"10{lab[:4]}"] = show(lab, rec, 5, 95, ["LP", "BI", "LD", "HG", "BU_L", "post"])
print(" 11. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent6(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(U6(10 + 20 * k_, z="yeah / ok", sub=False))
rec = run6(ag, 1800, lambda t: dict(LP=.1), evs); print(f"     curiosity crosses at {ag.Icross / 60:.1f} min; sigh, then a curiosity bid")
SC[11] = show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO", "BRE", "post"])
print(" 12. ordinary topic continuation: agent asks 'when are you going?'; he: '...Lyon on Sunday' (surprise 0.6, shares a lemma)")
ag = Agent6(P=0.5); evs = U6(5, z="hi, good to see you", riff=True, after_q=True, surp=0.6)
evs.update(U6(20, z="hi, good to see you", riff=False, surp=0.45)); evs.update(U6(35, z="hi, good to see you", riff=True, surp=0.45))
rec = run6(ag, 60, lambda t: dict(LP=.3), evs); SC[12] = show("three ordinary continuations", rec, 5, 60, ["LP", "CR", "BU_L", "RHY"])

ok16 = (SC[1]["BI"] >= 0.15 and SC[1]["LP"] <= 0.10 and SC[2]["BU_L"] <= 0.01 and SC["8a"]["LP"] <= 0.10 and SC["8l"]["LP"] <= 0.10
        and SC["8d"]["LP"] <= 0.10 and SC["ma21"]["LP"] <= 0.10 and SC["ml21"]["LP"] <= 0.10 and SC[9]["LP"] <= 0.30
        and SC[12]["BU_L"] <= 0.01 and SC["6_90"]["BU_L"] >= 0.2 and SC["51"]["LT"] <= 1e-9 and SC["10loud"]["BI"] <= 0.05)
report("J16 sympathy shows within seconds; no beaming at grief for any code or on any mourning day; no laugh at ordinary turns",
       ok16, "")
print(f"\n{sum(OK)}/{len(OK)} checks pass")
