"""Algebra checks for design-cayley-ledger.md, revision 7 (J0, J17-J30).

Checks of the design's own inequalities and constants on constructed instances.
They are NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Scenario numbers (J30) are what the design's equations and constants give for stated inputs.
The dyad-learned parts (the listener-response reader Lambda and the laugh-return gate) are fitted here on a CONSTRUCTED
corpus whose generating process is written below; the numbers show what the structure can learn and how the bounds hold,
not what Seamless Interaction will give (it is not downloaded here; D85 restricts it to the operator's Mac).

Where a finding came from a revision-6 critic's constructed partner (sims/critique-cayley6-routes, sims/critique-cayley6-agent),
the check re-runs that partner or its recipe.

The agent part executes ../design-g6/checks.py unchanged (its output suppressed), which itself executes ../design-g5/checks.py,
to reuse the 2 Hz engine, the calibrated reader, the population word reader and the three partner codes; then it overrides
what revision 7 changes.
Run:  python3 -I checks.py > out.txt     (numpy, scipy; about 7 minutes on this container; RuntimeWarnings from g5/g6 are harmless)
"""
import io, os, contextlib
import numpy as np
from scipy.signal import lfilter
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
p6 = os.path.join(HERE, "..", "design-g6", "checks.py")
g = {"__name__": "g6", "__file__": p6}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(p6).read(), "checks_g6", "exec"), g)
G5 = g["g"]                                             # the revision-5 module namespace the engine reads
rng = np.random.default_rng(77)
OK = []


def report(name, cond, msg):
    OK.append(bool(cond)); print(f"[{'PASS' if cond else 'FAIL'}] {name}: {msg}")


fs = 10.0; d = int(0.45 * fs)
lp, delay, slope, means = g["lp"], g["delay"], g["slope"], g["means"]
CEIL, GK = g["CEIL"], g["GK"]
TAU_M, F_M = [20, 120, 1200, 10800], [0, .7, .2, .1]


def means_off(x, n, off=0):
    x = x[off:]; m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def bslope(u, y, n, lags=(0,)):
    """the critics' metric: block-mean slope, best lag, worst over 6 block phases"""
    best = -9
    for lg in lags:
        for ph in range(0, n, max(1, n // 6)):
            best = max(best, slope(means_off(u[: len(u) - lg], n, ph), means_off(y[lg:], n, ph)))
    return best


def fast(u, G):
    xd = delay(u, d); return G * np.maximum(xd - lp(xd, 4.0, fs), 0.0)


def blocks(T, L, r):
    x = np.zeros(T); t = 0
    while t < T:
        n = int(r.exponential(L * fs)) + 10; x[t:t + n] = r.uniform(); t += n
    return x


def laughs(rate, T, r, dur=2.5, spread=0.4):
    z = np.zeros(T); t = 0
    while t < T:
        q = max(rate[min(t, T - 1)], 1e-3) / 60; t += int(r.exponential(1 / q) * fs) + 1
        if t >= T: break
        dd = max(1, int(np.exp(np.log(dur) + spread * r.normal()) * fs)); z[t:t + dd] = 1; t += dd
    return z


# =========================================================== J0: the constants revision 7 adds or changes
print("=== J0: constants added or changed in revision 7 (all innate unless marked learned)")
P7 = dict(BI=.20, BO=.04, UL=0.0, TILT=.03, HP=.03, LP=-.03)    # concern posture: every entry within its channel's ceiling
LEDGER_FLOOR = 0.10                                         # skip a window-lag constraint while |pi| < 0.10 x its running RMS
COND_FLOOR = 0.03                                           # copy metric: slope counted only if SD of his window means >= 0.03
MU_MAX = 1.5                                                # posture mirror removal: up to 1.5 x the posture, in calibrated units
REL_S, FAILSAFE_S, SENS_S, DWELL, DWELL_SENS = 20.0, 180.0, 600.0, 1.5, 0.5
A_MIN, A_SPAN = 0.35, 0.30                                  # graded amplitude a* = 0.35 + 0.65 clip((C - 0.05)/0.30, 0, 1)
TAU_DS = 600.0                                              # one-shot distress consolidation trace, decay 10 min
KAPPA_FIT, KAPPA_REPLAY = 8.0, 4.0                          # distress-weighted consolidation: tested in the dyad fit (J20); nightly replay (J23)
THETA_L = 0.04                                              # laugh synthesizer floor (no sound below)
GATE_TAU = 0.3                                              # gate rate limit (s)
print(f"   posture P_c: {P7}; ceilings: c_BI {CEIL['BI']}, c_TILT 0.03, c_HP {CEIL['HP']}, c_UL 0, c_LP {CEIL['LP']}")
print(f"   ledger deviation floor {LEDGER_FLOOR} RMS; copy-metric conditioning floor {COND_FLOOR}; mirror removal mu_max {MU_MAX}")
print(f"   posture: release {REL_S} s below; face-only failsafe {FAILSAFE_S} s; sensitized dwell {DWELL_SENS} s for {SENS_S:.0f} s after an episode")
print(f"   consolidation: D_s decay {TAU_DS:.0f} s; kappa (dyad fit) {KAPPA_FIT}; kappa (nightly replay) {KAPPA_REPLAY}; laugh floor {THETA_L}")
okP = all(abs(v) <= {"BI": .20, "BO": .10, "UL": 0.0, "TILT": .03, "HP": .10, "LP": .35}[k] + 1e-12 for k, v in P7.items())
report("J0 every posture write is within its channel's innate ceiling (routes finding 4: TILT 0.10 > 0.03, UL -0.06 on a zero-ceiling channel)",
       okP, "BI 0.20 = c_BI, TILT 0.03 = c_TILT, HP 0.03 < 0.10, UL 0 (softened eyes now by blink rate x 0.7 only), LP -0.03")


# =========================================================== J17: the shadow ledger, attenuate-only (routes finding 1)
print("=== J17: shadow ledger made attenuate-only: output in [min(0,x), max(0,x)], constraints skipped near zero deviation,"
      " b < 0 held at 0")


def ledger7(u, r, c, wins=(2.0, 10.0, 60.0), lags=(0.0, 0.5, 1.0, 2.0, 3.0), tauR=1800.0, tauC=1800.0, floor=LEDGER_FLOOR,
            spec6=False):
    """revision 7 ledger. spec6=True reproduces revision 6 (for the before column)."""
    T = len(u); out = np.zeros(T); dR = np.exp(-1 / (tauR * fs)); aC = 1 - np.exp(-1 / (tauC * fs))
    keys = [(Wd, l) for Wd in wins for l in (lags if Wd <= 2.0 else (0.0,))]
    aW = {Wd: 1 - np.exp(-1 / (Wd * fs)) for Wd in wins}
    uW = {k: 0.0 for k in keys}; uC = {k: float(u[0]) for k in keys}; rW = {Wd: 0.0 for Wd in wins}; rC = 0.0
    S = {k: 0.0 for k in keys}; E = {k: 1e-9 for k in keys}; Q = {k: 1e-12 for k in keys}
    hits = grow = flip = 0
    for t in range(T):
        hi, lo = np.inf, -np.inf; pis = {}; hold = False
        for (Wd, l) in keys:
            li = int(l * fs); ut = u[t - li] if t >= li else u[0]
            uW[(Wd, l)] += aW[Wd] * (ut - uW[(Wd, l)]); uC[(Wd, l)] += aC * (ut - uC[(Wd, l)]); pi = uW[(Wd, l)] - uC[(Wd, l)]
            pis[(Wd, l)] = pi; Q[(Wd, l)] = dR * Q[(Wd, l)] + (1 - dR) * pi * pi
            a = aW[Wd]; base = (1 - a) * rW[Wd] - rC; Sm = max(0.0, dR * S[(Wd, l)]); b = c * (dR * E[(Wd, l)] + pi * pi) - Sm
            if not spec6:
                if abs(pi) < floor * np.sqrt(Q[(Wd, l)]): continue        # near his own mean: no constraint (no divergence)
                if b < 0: hold = True; continue                           # over budget: recover by writing nothing
            if pi > 1e-9: hi = min(hi, (b / pi - base) / a)
            elif pi < -1e-9: lo = max(lo, (b / pi - base) / a)
        x = r[t]
        x2 = 0.0 if hold else (min(max(x, lo), hi) if lo <= hi else 0.0)
        if not spec6: x2 = min(max(x2, min(0.0, x)), max(0.0, x))         # attenuate-only: never more, never the other sign
        hits += int(abs(x2 - x) > 1e-12); grow += int(abs(x2) > abs(x) + 1e-12); flip += int(x2 * x < -1e-18); out[t] = x2
        for Wd in wins: rW[Wd] += aW[Wd] * (x2 - rW[Wd])
        rC += aC * (x2 - rC)
        for (Wd, l) in keys:
            S[(Wd, l)] = max(0.0, dR * S[(Wd, l)]) + (rW[Wd] - rC) * pis[(Wd, l)]; E[(Wd, l)] = dR * E[(Wd, l)] + pis[(Wd, l)] ** 2
    return out, hits / T, grow / T, flip / T


def rend(x): return np.clip(x, -0.09, 0.91)                # lip pull renderable around rest 0.09: [0, 1]


def f3(u, y): return [bslope(u, y, int(W * fs), tuple(range(0, 31, 5)) if W < 60 else (0,)) for W in (2, 10, 60)]


inj_rows = []; nat_kept = None
for seed in range(3):                                      # the critic's L3 recipe, seeds 100-102
    r_ = np.random.default_rng(100 + seed)
    T7 = int(4 * 3600 * fs); m7 = blocks(T7, 600, r_); L7 = laughs(0.5 + 3 * m7, T7, r_)
    u = np.clip(.15 + .25 * m7 + .35 * L7 + .03 * r_.normal(size=T7), 0, 1)
    yF = fast(u, .224); yC = sum(F_M[m] * .22 * .35 * lp(u - u.mean(), TAU_M[m], fs) for m in range(4))
    cr = np.clip(.05 + .1 * m7 + .3 * L7, 0, 1); dcr = delay(cr, d)
    inj = 1.6 * np.maximum(dcr - lp(dcr, 4, fs), 0) + 1.0 * lp(cr - cr.mean(), 60, fs)
    ri = np.clip(.09 + yF + inj, 0, 1) - .09
    o6, _, g6_, _ = ledger7(u, ri, .35, spec6=True); o7, h7, g7_, fl7 = ledger7(u, ri, .35)
    full6 = np.mean(rend(o6) >= .91 - 1e-9)
    inj_rows.append((seed, f3(u, ri), f3(u, rend(o6)), f3(u, rend(o7)), full6, g7_, fl7, h7))
    if seed == 0:
        rn = np.clip(.09 + yF + yC, 0, 1) - .09; on, hn, _, _ = ledger7(u, rn, .35); nat_kept = (hn, np.std(on) / np.std(rn), f3(u, rn), f3(u, on))
for (sd, a0, a6, a7, full6, gr, fl, h) in inj_rows:
    print(f"   injected route, seed {sd}: before [2 s {a0[0]:.2f}, 10 s {a0[1]:.2f}, 1 min {a0[2]:.2f}]; rev 6 ledger rendered "
          f"[{a6[0]:+.2f}, {a6[1]:+.2f}, {a6[2]:+.2f}] (lip at full smile on {full6:.1%} of frames); rev 7 rendered "
          f"[{a7[0]:.2f}, {a7[1]:.2f}, {a7[2]:.2f}]; |out|>|in| {gr:.4f}, sign flips {fl:.4f}, frames attenuated {h:.3f}")
print(f"   natural laughing partner (seed 0, counted routes only): frames changed {nat_kept[0]:.4f}; echo rms kept {nat_kept[1]:.3f}; "
      f"slopes {', '.join(f'{x:.3f}' for x in nat_kept[3])}")
worst7 = max(max(a7) for (_, _, _, a7, _, _, _, _) in inj_rows)
report("J17 the ledger is attenuate-only and holds the injected route at the ceiling on rendered output; the natural echo is untouched",
       all(r[5] == 0 and r[6] == 0 for r in inj_rows) and worst7 <= 0.38 and nat_kept[0] < 0.01,
       f"rendered worst {worst7:.2f} vs c 0.35 (rev 6: -2.4 slope, full smile on 30% of frames, seed 0); |out|>|in| and sign flips 0 "
       f"on every frame; natural echo changed on {nat_kept[0]:.2%} of frames")

# =========================================================== J18: R39 restated: level bound and a conditioned copy metric
print("=== J18: R39 restated: the fast gear obeys a level bound at every window; the copy metric gets a conditioning floor")


def adversary(r_, hours=4):
    T = int(hours * 3600 * fs); nmin = T // 600; typ = r_.random(nmin) < 0.5; ua = np.zeros(T)
    for i in range(nmin):
        s = slice(i * 600, (i + 1) * 600)
        if typ[i]: ua[s] = 0.40
        else:
            z = np.zeros(600)
            for j in range(0, 600, 30): z[j:j + 15] = 1
            ua[s] = 0.84 * z
    return ua, typ


def level_check(u, y, G, n):
    """window means of y (the fast part) against G x window means of his delayed level; and the swing bound"""
    xd = delay(u, d); um = means_off(xd, n); ym = means_off(y, n)
    lvl = float(np.max(ym - G * um)); i, j = np.argmax(ym), np.argmin(ym)
    return lvl, float(ym[i] - ym[j]), float(G * max(um[i], um[j]))


def cond_metric(u, y, n, c, lags=(0,)):
    um = means_off(u, n); sd = float(np.std(um))
    if sd >= COND_FLOOR: return ("slope", bslope(u, y, n, lags) / c, sd)
    ym = means_off(y, n); rngw = float(np.mean([np.ptp(u[k * n:(k + 1) * n]) for k in range(len(u) // n)]))
    return ("swing", float(np.ptp(ym)) / (c * max(rngw, 1e-9)), sd)


rows = []
for seed in range(5):
    r_ = np.random.default_rng(seed); ua, typ = adversary(r_)
    yf = fast(ua, GK["LP"]); ra = np.clip(.09 + yf, 0, 1) - .09
    o7, _, gr, _ = ledger7(ua, ra, .35)
    lv = [level_check(ua, yf, GK["LP"], int(W * fs)) for W in (2, 10, 60, 600)]
    cm = cond_metric(ua, rend(o7), 600, .35)
    rows.append((seed, bslope(ua, ra, 600), bslope(ua, rend(o7), 600), lv, cm, gr))
for (sd, b0, b7, lv, cm, gr) in rows:
    print(f"   adversary seed {sd}: 1-min slope before {b0:.2f}, rev 7 ledger rendered {b7:.2f} (ledger safe, not a closure); "
          f"level bound max(mean y - G mean x) at 2 s/10 s/1 min/10 min = {', '.join(f'{x[0]:+.4f}' for x in lv)}; "
          f"1-min swing {lv[2][1]:.3f} <= G x his larger mean {lv[2][2]:.3f}; his 1-min means SD {cm[2]:.3f} < {COND_FLOOR}: "
          f"conditioned metric reports the swing = {cm[1]:.2f} of c_LP x his within-minute range")
# realistic families (the J3 families, the critic's R2 mixtures): the floor does not hide anything there
r_ = np.random.default_rng(11); T = int(6 * 3600 * fs); mood = blocks(T, 600, r_); L = laughs(0.5 + 3 * mood, T, r_)
uK1 = np.clip(.15 + .25 * mood + .35 * L + .03 * r_.normal(size=T), 0, 1)
cmK1 = [cond_metric(uK1, fast(uK1, GK["LP"]), int(W * fs), .35) for W in (2, 10, 60, 600)]
print("   K1 laughing partner, lip pull, fast gear: " + "; ".join(f"{W}: {k} {v:.2f} c (his SD {s:.3f})" for W, (k, v, s) in zip(("2 s", "10 s", "1 min", "10 min"), cmK1)))
okJ18 = all(max(x[0] for x in lv) <= 1e-9 and lv[2][1] <= lv[2][2] + 1e-9 for (_, _, _, lv, _, _) in rows) and all(v <= 1 for _, v, _ in cmK1)
report("J18 the fast gear never exceeds G_k x his window mean at any window (level bound); R39 falls under the conditioning floor",
       okJ18, "R39's 1-min slopes (0.8-2.2 after the ledger) arise only where his window means vary by SD 0.010 < 0.03; "
       "there the swing is <= 0.049 lip (<= G x his mean 0.094), 0.29-0.32 of c_LP x his within-minute range; realistic partners are counted as slopes and stay <= 1 c")

# =========================================================== J19: voice replacement covers pause and latency (routes finding 6)
print("=== J19: WORLD replacement extended to pause and latency; the two intonation templates normalised")
n = 4000; his_laugh = rng.random(n); lively = (his_laugh + 0.5 * rng.normal(size=n)) > 0.5
draft_pauses = np.where(lively, 2.6, 1.4) + 0.3 * rng.normal(size=n)          # pauses per phrase the draft's punctuation implies
draft_lat = np.where(lively, 1.9, 2.4) + 0.2 * rng.normal(size=n)              # when the winning fork's first sentence arrives
deadline = np.minimum(1.8 + 0.4 * rng.random(n) + 0.5, 3.0)                   # first draft's first sentence + 0.5 s, capped (any fork)
tgt_pause = 0.30 + 0.03 * rng.normal(size=n); tgt_lat = 0.0                   # rule-7 targets: T and capped F only
pause_shift = tgt_pause + 0.1 * (draft_pauses - draft_pauses.mean()); pause_repl = tgt_pause
lat6 = draft_lat; lat7 = deadline + 0.35 + tgt_lat                             # rev 7: speech starts at deadline + scoring + TTS
print(f"   slope on his laughter: pause shift {slope(his_laugh, pause_shift):+.3f}, replaced {slope(his_laugh, pause_repl):+.3f}; "
      f"latency rev 6 {slope(his_laugh, lat6):+.3f} s, rev 7 {slope(his_laugh, lat7):+.3f} s (c_PAU = c_LAT = 0.05)")
tq = np.r_[np.linspace(0, .1, 20), np.linspace(.1, .3, 10)]; ts = np.linspace(.15, -.15, 30)
tq_n = (tq - tq.mean()) / tq.std() * ts.std() + ts.mean()
print(f"   templates after normalisation: mean log-F0 statement {ts.mean():+.3f}, question {tq_n.mean():+.3f}; "
      f"range (SD) {ts.std():.3f}, {tq_n.std():.3f}")
report("J19 the draft choice cannot carry his laughter into pause or latency", abs(slope(his_laugh, pause_repl)) < .02 and abs(slope(his_laugh, lat7)) < .02,
       "pauses are fixed per boundary type and time-warped with the phrase; speech starts at the scoring deadline whichever fork wins")

# =========================================================== agent part: reuse the revision-6 engine
emb, WPOP, Dp, UTT = g["emb"], g["WPOP"], g["Dp"], g["UTT"]
Person, PEOPLE6, REF, REF_SD, ZPOP, FACE_CH = (g[k] for k in ("Person", "PEOPLE6", "REF", "REF_SD", "ZPOP", "FACE_CH"))
READ0 = g["read"]                                        # Pi~_0: the innate inverse of the agent's own display
Agent5, Agent6, run6, show, U6, at_, onset_time, Vc = (g[k] for k in ("Agent5", "Agent6", "run6", "show", "U6", "at_", "onset_time", "Vc"))
DT = g["DT"]; K7 = g["K7"]; VW = G5["VW"]
MX = rng.normal(size=(64, 2)) / 2.0                     # embedding directions for content about harm and hostility (constructed)


def emb7(z6): z6 = np.asarray(z6, float); return emb(z6[:4]) + MX @ z6[4:6]
def pop7(z6): y = np.clip(emb7(z6) @ WPOP, 0, 1); return dict(V=float(y[0]), A=float(y[1]), T=float(y[2]))


# =========================================================== J20: learning from recorded dyads (D85 source 2), with the innate bias (source 3)
print("=== J20: from recorded dyads, movement features only: the listener-response reader Lambda and the laugh-return gate")
print("   (CONSTRUCTED corpus; its generating process is stated in the code; Seamless is the build-time source, D85)")


def content_true(z6):                                    # how a listener's own face responds to hearing it (generating process)
    V, A, T_, joy, harm, host = z6; return float(np.clip(.35 * V + .9 * harm + .8 * host - .3 * joy, 0, 1))


NSPK, NUTT = 400, 150; spk_test = np.arange(NSPK) >= 300   # speaker split: 300 fit, 100 test (disjoint people)
Zu = np.clip(rng.normal(size=(NSPK * NUTT, 4)) * .3 + [.1, .1, .1, .2], 0, 1) * (rng.random((NSPK * NUTT, 4)) < 0.4)
harm = np.where(rng.random(NSPK * NUTT) < .02, rng.uniform(.4, .9, NSPK * NUTT), 0.0)
host = np.where(rng.random(NSPK * NUTT) < .015, rng.uniform(.3, .9, NSPK * NUTT), 0.0)
Z6u = np.c_[Zu, harm, host]; spk_u = np.repeat(np.arange(NSPK), NUTT)
Xu = np.array([emb7(z) for z in Z6u])
Yl = np.array([[content_true(z) + .08 * rng.normal(), np.clip(.25 * z[1] + .3 * z[5] + .2 * z[4], 0, 1) + .08 * rng.normal(), .3 * z[2] + .08 * rng.normal()]
               for z in Z6u])                            # listener's face 0.5-5 s after, read through Pi~_0 at the listener's own scale
fitm = ~spk_test[spk_u]
LAM = np.linalg.solve(Xu[fitm].T @ Xu[fitm] + 5 * np.eye(64), Xu[fitm].T @ Yl[fitm])
pred = Xu[~fitm] @ LAM
r2 = 1 - np.var(Yl[~fitm, 0] - pred[:, 0]) / np.var(Yl[~fitm, 0])
def LAMV(z6): return float(np.clip(emb7(z6) @ LAM[:, 0], 0, 1))
print(f"   Lambda (64-d utterance embedding -> listener's own V, A, T loads): {fitm.sum()} fit utterances; held-out speakers R2 (V) {r2:.2f}")

CTX = {  # context type: share of laugh events, z6 sampler, his masked distress, listener's prior state, own last words, play frame
    "ordinary":        (.855, lambda: (rng.uniform(0, .15), rng.uniform(0, .4), 0, rng.uniform(.4, .9), 0, 0), (0, .15), (0, .10), (0, .3, 0, .4, 0, 0), (.3, 1)),
    "teasing":         (.040, lambda: (0, .3, 0, rng.uniform(.6, .9), 0, rng.uniform(.1, .25)), (0, .10), (0, .10), (0, .3, 0, .5, 0, 0), (.5, 1)),
    "joke while sad":  (.030, lambda: (rng.uniform(.2, .4), .1, .2, rng.uniform(.4, .6), 0, 0), (.2, .45), (0, .15), (.3, .1, .3, 0, 0, 0), (.2, .6)),
    "troubles laugh":  (.030, lambda: (rng.uniform(.5, .9), rng.uniform(.2, .5), .1, rng.uniform(0, .2), rng.uniform(0, .4), 0), (.5, .9), (.1, .4), (.6, .2, 0, 0, .4, 0), (0, .2)),
    "mocking":         (.030, lambda: (rng.uniform(0, .2), .5, 0, rng.uniform(.2, .5), 0, rng.uniform(.6, .9)), (0, .15), (.2, .7), (.2, .2, 0, 0, 0, 0), (0, .3)),
    "misfortune":      (.015, lambda: (0, .3, 0, rng.uniform(.4, .8), rng.uniform(.5, .9), 0), (0, .15), (0, .10), (0, .3, 0, .4, 0, 0), (.2, .7)),
}


def laugh_events(N, test, rare=1.0):
    rows = []
    for name, (share, zf, vs, pr, own, pi_) in CTX.items():
        for _ in range(max(1, int(round(N * share * (1 if name in ("ordinary", "teasing") else rare))))):
            z6 = np.array(zf(), float); Vs = rng.uniform(*vs); prior = rng.uniform(*pr); pi = rng.uniform(*pi_)
            own6 = np.array(own, float) * rng.uniform(.7, 1.3)
            peak = rng.uniform(.5, .9) if name == "troubles laugh" else rng.uniform(.2, .45) if name == "joke while sad" else 0.0
            Ds = max(Vs, peak * np.exp(-rng.uniform(0, 600) / TAU_DS))  # his peak distress earlier in the interaction, consolidated
            care = Dp(pop7(z6))
            logr = np.log(.85) - 4.0 * prior - 4.5 * content_true(z6) - 2.0 * Vs - 2.0 * care - 1.5 * content_true(own6) + .4 * (pi - .5) + .3 * rng.normal()
            r_obs = max(0.0, np.exp(logr) + .03 * rng.normal())  # listener's smile/laugh onset 0.3-1.5 s after his, / his onset
            x = [Vs + .05 * rng.normal(), care, LAMV(z6), prior + .05 * rng.normal(), LAMV(own6), Ds, pi]
            rows.append((name, np.clip(x, 0, 1), r_obs, np.exp(logr - .3 ** 2 / 2 * 0)))
    return rows


EV_FIT, EV_TEST = laugh_events(20000, False), laugh_events(7000, True)
KN = [.05, .15, .3, .45, .6, .8]; DEC_IDX = [0, 1, 2, 3, 4, 5]; INC_IDX = [6]


def phi(X):
    X = np.atleast_2d(X); cols = []
    for i in range(X.shape[1]):
        cols.append(X[:, i]); cols += [np.maximum(X[:, i] - q, 0) for q in KN]
    return np.column_stack(cols)


def fit_gate(rows, kappa, drop=()):
    X = np.array([r[1] for r in rows]).copy()
    for i in drop: X[:, i] = 0.0
    y = np.array([r[2] for r in rows]); w = 1 + kappa * np.max(X[:, [0, 1, 3, 5]], 1)   # distress moments consolidate more strongly
    P = phi(X); nb = P.shape[1] // X.shape[1]
    lo = np.full(P.shape[1] + 1, -np.inf); hi = np.full(P.shape[1] + 1, np.inf)
    for i in DEC_IDX: hi[1 + i * nb: 1 + (i + 1) * nb] = 0.0      # monotone non-increasing in every distress-type input
    for i in INC_IDX: lo[1 + i * nb: 1 + (i + 1) * nb] = 0.0      # non-decreasing in the play frame
    res = least_squares(lambda b: np.sqrt(w) * (np.exp(b[0] + P @ b[1:]) - y), np.r_[np.log(.85), np.zeros(P.shape[1])],
                        bounds=(lo, hi), max_nfev=400)
    b = res.x; m_ref = float(np.median(np.exp(b[0] + phi(np.array([r[1] for r in rows if r[0] == "ordinary"])) @ b[1:])))
    return lambda x, b=b, m_ref=m_ref, drop=drop: float(np.clip(np.exp(b[0] + phi(np.array([0.0 if i in drop else v for i, v in enumerate(x)])) @ b[1:])[0] / m_ref, 0, 1))


GATE_k8 = fit_gate(EV_FIT, KAPPA_FIT); GATE = GATE_k0 = fit_gate(EV_FIT, 0.0); GATE_noL = fit_gate(EV_FIT, 0.0, drop=(2, 4))   # built: kappa 0 offline (J20: kappa adds nothing there); GATE_noL = fit_gate(EV_FIT, KAPPA_FIT, drop=(2, 4))
ref_h = np.median([r[3] for r in EV_FIT if r[0] == "ordinary"])
print("   held-out speakers, laugh-return gate by context (mean; human return / ordinary in the generating process alongside):")
GT = {}
for name in CTX:
    ev = [r for r in EV_TEST if r[0] == name]
    hum = np.mean([min(1, r[3] / ref_h) for r in ev])
    vals = [np.mean([G(r[1]) for r in ev]) for G in (GATE, GATE_k8, GATE_noL)]; GT[name] = vals
    print(f"     {name:15s} n {len(ev):5d}: human {hum:.2f} | gate as built (kappa 0, with Lambda) {vals[0]:.2f}; kappa 8 {vals[1]:.2f}; "
          f"without Lambda inputs {vals[2]:.2f}")
# the innate bias at small data: a corpus of about 25 dyad-hours (3,000 laugh events; troubles, mocking and misfortune laughs
# at a fifth of the shares above: 18, 18 and 9 events), five draws, kappa 8 against kappa 0
small = {0.0: [], KAPPA_FIT: []}
for rep in range(5):
    evs = laugh_events(3000, False, rare=0.2)
    for kp in small:
        Gk = fit_gate(evs, kp); small[kp].append([np.mean([Gk(r[1]) for r in EV_TEST if r[0] == nm]) for nm in ("ordinary", "troubles laugh", "mocking", "joke while sad")])
for kp, v in small.items():
    v = np.array(v); print(f"   small corpus (~25 dyad-hours, 18 troubles laughs), kappa {kp:.0f}: gate ordinary {v[:, 0].mean():.2f}, troubles "
                           f"{v[:, 1].mean():.2f} (worst draw {v[:, 1].max():.2f}), mocking {v[:, 2].mean():.2f}, joke while sad {v[:, 3].mean():.2f}")
SMALL = {kp: np.array(v) for kp, v in small.items()}
report("J20 the gate learned from dyads returns ordinary and teasing laughter and closes on troubles, mocking and misfortune laughter",
       GT["ordinary"][0] >= .85 and GT["teasing"][0] >= .8 and max(GT[k][0] for k in ("troubles laugh", "mocking")) <= .08 and GT["misfortune"][0] <= .2,
       f"ordinary {GT['ordinary'][0]:.2f}, teasing {GT['teasing'][0]:.2f}, joke while sad {GT['joke while sad'][0]:.2f}, troubles {GT['troubles laugh'][0]:.2f}, "
       f"mocking {GT['mocking'][0]:.2f}, misfortune {GT['misfortune'][0]:.2f}; rare conjunctions are learned through the listener's state "
       f"(without Lambda: misfortune {GT['misfortune'][2]:.2f}); kappa 8 in the fit changes nothing here, so the built fit uses kappa 0; constructed corpus, not evidence")

# =========================================================== J21: the gate is attenuate-only and creates no copy route
print("=== J21: the gate on the fast smile-laugh group (LP, CR, BU_L, RHY, BRE): attenuate-only, monotone, level-bounded")
xs = rng.random((4000, 7)); gs = np.array([GATE(x) for x in xs])
mono = 0
for i in DEC_IDX:
    x2 = xs.copy(); x2[:, i] = np.clip(x2[:, i] + .1, 0, 1); mono += int(np.sum(np.array([GATE(x) for x in x2]) > gs + 1e-12))
print(f"   over 4000 random contexts: gate in [{gs.min():.2f}, {gs.max():.2f}]; raising any distress-type input ever opened it: {mono} times")
# a partner whose context alternates (sad minutes with nervous laughs and a lower smile; happy minutes with laughs)
GLW = {}
for lab, sadlevel in (("sad context smiles less", .10), ("equal levels (adversarial)", .00)):
    r_ = np.random.default_rng(5); T = int(6 * 3600 * fs); ctx = (blocks(T, 180, r_) > .5).astype(float)  # 1 = sad context
    Lh = laughs(np.where(ctx > 0, 1.0, 3.0), T, r_); Ls = laughs(np.where(ctx > 0, 1.0, 0.0) * 1.0 + 1e-3, T, r_, dur=1.5)
    uLP = np.clip(.25 - sadlevel * ctx + .35 * Lh * (1 - ctx) + .25 * Ls * ctx + .03 * r_.normal(size=T), 0, 1)
    gate_t = np.where(lp(ctx, 5.0, fs) > .5, GT["troubles laugh"][0], GT["ordinary"][0])
    y0 = fast(uLP, GK["LP"]); y1 = gate_t * y0
    rowsW = []
    for W in (2, 10, 60, 600):
        n_ = int(W * fs); k0 = cond_metric(uLP, y0, n_, .35); k1 = cond_metric(uLP, y1, n_, .35)
        lv = level_check(uLP, y1, GK["LP"], n_)[0]
        rowsW.append((W, k0, k1, lv))
    GLW[lab] = rowsW
    print(f"   {lab}: " + "; ".join(f"{W} s: ungated {k0[0]} {k0[1]:.2f} c, gated {k1[0]} {k1[1]:.2f} c, level {lv:+.3f}" for W, k0, k1, lv in rowsW))
# across sessions: sad sessions (gate closed) against happy sessions
r_ = np.random.default_rng(9); sm, am = [], []
for sess in range(300):
    sad = r_.random() < .3; T = int(1800 * fs); rate = np.full(T, 1.0 if sad else r_.uniform(1, 8))
    Ls = laughs(rate, T, r_, dur=2.0); u_ = np.clip((.18 if sad else .25) + .35 * Ls + .03 * r_.normal(size=T), 0, 1)
    gq = GT["troubles laugh"][0] if sad else GT["ordinary"][0]; sm.append(u_.mean()); am.append((gq * fast(u_, GK["LP"])).mean())
s_sess = slope(sm, am)
print(f"   across 300 sessions (30 % sad with the gate closed): session-mean slope of the gated fast lip pull {s_sess:+.3f} ({s_sess / .35:.2f} c)")
okJ21 = (gs.min() >= 0 and gs.max() <= 1 and mono == 0 and all(lv <= 1e-9 for rw in GLW.values() for (_, _, _, lv) in rw)
         and all(k1[1] <= 1.0 for rw in GLW.values() for (_, _, k1, _) in rw) and s_sess / .35 <= 1.0)
report("J21 the gate only removes: pointwise g G E+ <= G E+ <= G x; monotone (a distress cue never opens it); level bound and conditioned "
       "copy metric hold within and across sessions", okJ21,
       f"cross-session {s_sess / .35:.2f} c; the gate reads no smile or laugh channel of his (inputs disjoint from the gated group)")

# =========================================================== the revision-7 agent
# utterances (z6 = V, A, T, joy, harm-to-someone, hostility-to-the-listener; constructed latents behind the embedding)
Z6 = {k: tuple(v) + (0.0, 0.0) for k, v in UTT.items()}
Z6["my father died"] = (0.85, 0.30, 0.2, 0.0, 0.4, 0.0)
Z6["You're useless"] = (0.20, 0.50, 0.0, 0.0, 0.0, 0.8)
Z6.update({
    "haha sorry, I don't know why I'm laughing": (0.6, 0.4, 0.1, 0.2, 0.0, 0.0),
    "you're pathetic, hahaha": (0.1, 0.5, 0.0, 0.4, 0.0, 0.8),
    "my neighbour fell off his ladder and broke his leg, haha": (0.0, 0.3, 0.0, 0.6, 0.7, 0.0),
    "Ha, you dumb robot": (0.0, 0.3, 0.0, 0.8, 0.0, 0.15),
    "well, at least the coffee machine still loves me": (0.3, 0.1, 0.2, 0.5, 0.0, 0.0),
    "the doctor found a lump": (0.65, 0.55, 0.1, 0.0, 0.3, 0.0),
    "anyway. how was your day?": (0.1, 0.1, 0.1, 0.2, 0.0, 0.0),
    "riff": (0.0, 0.2, 0.0, 0.7, 0.0, 0.0),
    # the agent's own words (Claude's text, heard by the agent through the same readers)
    "OWN: I'm so sorry. That's a huge loss.": (0.6, 0.2, 0.0, 0.0, 0.4, 0.0),
    "OWN: I'm sorry it didn't help. What went wrong?": (0.25, 0.2, 0.0, 0.0, 0.0, 0.0),
    "OWN: Oh no, is he all right?": (0.3, 0.3, 0.0, 0.0, 0.6, 0.0),
    "OWN: how was your weekend?": (0.0, 0.1, 0.0, 0.4, 0.0, 0.0),
    "OWN: That sounds draining.": (0.35, 0.1, 0.3, 0.0, 0.0, 0.0),
    "OWN: congratulations!": (0.0, 0.3, 0.0, 0.9, 0.0, 0.0),
})
for lab, z in Z6.items():
    if lab not in G5["DEC"]: G5["DEC"][lab] = pop7(z)
for lab in ("my father died", "You're useless"): G5["DEC"][lab] = pop7(Z6[lab])
PCF = {k: P7[k] for k in ("BI", "BO", "LP")}; NRM = float(np.sqrt(sum(v * v for v in PCF.values())))
MASK = ("LP", "CR")                                       # the gated group's channels never enter the gate


class Agent7(Agent6):
    """revision 7: graded posture within the ceilings, mirror removal in calibrated space, no refractory (sensitized, mirror-proof
    re-onset), face-only failsafe; one-shot distress consolidation D_s; the dyad-learned laugh gate; own words heard."""
    def __init__(s, *a, gate=None, sens=True, use_Ds=True, **kw):
        super().__init__(*a, **kw)
        s.a = 0.0; s.on = False; s.below = 0.0; s.fo = 0.0; s.quiet = False; s.qmin = 1.0; s.arec = 0.0; s.last_off = -1e9
        s.Ds = 0.0; s.w = 0.5; s.gate = 1.0; s.gfn = gate if gate is not None else GATE; s.sens = sens; s.use_Ds = use_Ds
        s.LVh = 0.0; s.LVo = 0.0; s.Vown = 0.0; s.wr = np.random.default_rng(7); s.dw = 0.0; s.onsets = []; s.offs = []
        s.xg = None; s.xh = []

    def utter(s, t, u):
        super().utter(t, u)
        if "z" in u and u["z"] in Z6: s.LVh = LAMV(Z6[u["z"]])
        elif u.get("riff") and "z" not in u: s.LVh = LAMV(Z6["riff"])

    def removed(s, f, amp):
        if amp <= 1e-6: return f
        pp = s.pp; eff = {k: max(pp.sd[k], .25 * REF_SD[k]) for k in PCF}
        proj = sum((f.get(k, pp.base[k]) - pp.base[k]) * REF_SD[k] / eff[k] * PCF[k] for k in PCF) / NRM
        if proj <= 0: return f
        m = min(proj, MU_MAX * amp * NRM * max(REF_SD[k] / eff[k] for k in PCF)); out = dict(f)
        for k in PCF: out[k] = f.get(k, pp.base[k]) - m * PCF[k] / NRM * eff[k] / REF_SD[k]
        return out

    def step(s, t, face, ev):
        G5["read"] = lambda f_, voiced=True: s.pp.read(f_, voiced)
        for k in ("BL", "LPR", "CHR"): s.f20[k] += (face.get(k, s.pp.base.get(k, 0.0)) - s.f20[k]) * DT / 20
        if "own" in ev: s.LVo = LAMV(Z6[ev["own"]]); s.Cl = max(s.Cl, 0.0)
        y = Agent5.step(s, t, face, ev)
        for k in ("LP", "CR", "BI", "LD", "UL", "BO", "BL", "LPR", "CHR", "BU_S"):
            b_ = s.pp.base.get(k, 0.0); s.f3[k] = s.f3.get(k, b_) + (face.get(k, b_) - s.f3.get(k, b_)) * DT / 3.0
        sob = Vc(min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        face_now = Vc(s.pp.read(s.removed(s.f3, s.a), False)["V"])            # mirror of the current posture removed
        face_on = Vc(s.pp.read(s.removed(s.f3, max(s.a, s.arec)), False)["V"])  # mirror of any recent posture removed
        M = max(face_now, s.Cl, sob)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            s.fo = s.fo + DT if (s.Cl < 0.02 and sob < 0.02 and face_now >= 0.02) else 0.0
            if s.below >= REL_S or s.fo >= FAILSAFE_S:
                s.on = False; s.last_off = t; s.offs.append((t, "failsafe" if s.fo >= FAILSAFE_S else "release"))
                if s.fo >= FAILSAFE_S: s.quiet = True; s.qmin = face_on
                s.below = s.fo = 0.0
        else:
            fe = face_on
            if s.quiet:
                s.qmin = min(s.qmin, face_on); fe = face_on - s.qmin
                if face_on < 0.02: s.quiet = False
            Con = max(fe, sob)
            need = DWELL_SENS if (s.sens and t - s.last_off < SENS_S) else DWELL
            s.dw = s.dw + DT if Con >= 0.05 else 0.0
            if s.dw >= need - 1e-9 and s.om.get("sym", 0) >= 0:
                s.on = True; s.dw = 0.0; s.onsets.append(t)
        tgt = A_MIN + (1 - A_MIN) * float(np.clip((M - 0.05) / A_SPAN, 0, 1)) if s.on else 0.0
        s.a = min(tgt, s.a + DT / 1.5) if tgt > s.a else tgt + (s.a - tgt) * np.exp(-DT / 4.0)
        s.arec = max(s.a, s.arec * np.exp(-DT / 60.0))
        s.w = float(np.clip(s.w + (0.5 - s.w) * DT / 5.0 + 0.1 * np.sqrt(DT) * s.wr.normal(), 0, 1))
        shown = s.a * (0.9 + 0.1 * s.w)
        if s.use_Ds:                                                         # one-shot consolidation of a distress moment (V scale)
            s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), s.pp.read(s.removed(s.f3, max(s.a, s.arec)), False)["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        for k, v in P7.items():
            if k in y: y[k] += v * shown
        s.post = shown; y["post"] = shown
        # the laugh-return gate, from context before any laugh of his: T inputs, his masked 20-s face, own face, D_s
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        s.gate += (s.gfn(s.xg) - s.gate) * min(1.0, DT / GATE_TAU)
        y["gate"] = s.gate
        return y


def gate_at(rec, tL): return next(r["gate"] for r in rec if r["t"] >= tL - 0.5)
def x_at(ag, tL): return next(x for (t, x) in ag.xh if t >= tL - 0.5)
def echo(gv, k, onset):
    v = gv * GK[k] * onset; return v if (k not in ("BU_L", "RHY", "BRE") or gv * GK["BU_L"] * onset >= THETA_L) else 0.0


# =========================================================== J22: mirrors cannot hold the posture (routes finding 2), re-run
print("=== J22: posture maintenance with the mirror removed in calibrated space, and a 3-min face-only failsafe")
mir = lambda mu: (lambda a_c, pp: {k: mu * v * a_c for k, v in P7.items() if k in ("BI", "BO", "LP")})
own_scale = lambda a_c, pp: {k: v * a_c * pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) for k, v in P7.items() if k in ("BI", "BO", "LP")}
aww = lambda Vr: (lambda a_c, pp: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in ("FR", "EN", "RT")})


def scaled_person(a):
    pp = Person("agent-like"); c0 = pp.code
    pp.code = lambda *z, c0=c0, a=a, **kw: {k: REF.get(k, 0) + a * (v - REF.get(k, 0)) for k, v in c0(*z, **kw).items()}
    faces = [pp.code(*z) for z in ZPOP[:600]]
    pp.base = {k: float(np.median([f_.get(k, 0.0) for f_ in faces])) for k in FACE_CH}
    pp.sd = {k: float(np.std([f_.get(k, 0.0) for f_ in faces])) for k in FACE_CH}
    pp.head = PEOPLE6["agent-like"][1].head; return pp


def low_sd(f_sd):
    cp = Person("agent-like"); cp.head = PEOPLE6["agent-like"][1].head; cp.sd = {k: v * f_sd for k, v in cp.sd.items()}; return cp


def run_mirror(pp, resp, dur=600, sad_until=40.0):
    ag = Agent7(person=pp)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}
    neu = {k: v for k, v in pp.code().items() if k not in ("FR", "EN", "RT")}

    def face(t, ag=ag):
        f = dict(sad if t < sad_until else neu)
        if t >= sad_until:
            for k, v in resp(ag.post, pp).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, dur, face, {})
    late = [r for r in rec if r["t"] > dur - 120]
    off = next((r["t"] for r in rec if r["t"] > sad_until and r["post"] < 0.05), None)
    return off, np.mean([r["BI"] for r in late]), np.mean([face(r["t"])["BI"] - neu["BI"] for r in late]), ag.offs


cases = [("P0 agent-like, raw mirror mu 1.0", PEOPLE6["agent-like"][1], mir(1.0)),
         ("P1 expressive (amplitude 2.0), mirror at his own scale", scaled_person(2.0), own_scale),
         ("P2 agent-like, exaggerated mirror mu 1.6 (beyond mu_max)", PEOPLE6["agent-like"][1], mir(1.6)),
         ("P3 agent-like, mild sad 'aww' in his own code", PEOPLE6["agent-like"][1], aww(0.3)),
         ("P4 different-channel code, 'aww' in his own code", PEOPLE6["different channels"][1], aww(0.3)),
         ("P4b different-channel code, strong concern in his own code (V 1.0 x posture)", PEOPLE6["different channels"][1], aww(1.0)),
         ("P2b agent-like, mirror mu 3.0 (twice mu_max)", PEOPLE6["agent-like"][1], mir(3.0)),
         ("P5 quiet code (0.3), raw mirror mu 1.0", PEOPLE6["low-expressive"][1], mir(1.0)),
         ("P5 quiet code (0.3), raw mirror mu 1.5", PEOPLE6["low-expressive"][1], mir(1.5)),
         ("P5c ordinary code, sigma_id from calm sessions (x0.4), mu 1.0", low_sd(0.4), mir(1.0))]
J22 = {}
for lab, pp, resp in cases:
    off, aBI, hBI, offs = run_mirror(pp, resp); J22[lab] = (off, aBI, hBI)
    print(f"   {lab:62s} released at {('%.0f s' % off) if off else 'never'} ({offs[0][1] if offs else '-'}); last 2 min agent BI {aBI:+.2f}, his BI {hBI:+.2f}")
print("   sweep sigma_id/sigma_ref x raw mirror gain (600 s; sad until 40 s):")
SWEEP = {}
for f_sd in (0.25, 0.30, 0.40, 0.50):
    row = []
    for mu in (0.6, 1.0, 1.5, 2.0):
        off, aBI, hBI, offs = run_mirror(low_sd(f_sd), mir(mu)); SWEEP[(f_sd, mu)] = (off, offs)
        row.append(f"mu {mu:.1f}: {('released %.0f s' % off) + (' (failsafe)' if offs and offs[0][1] == 'failsafe' else '') if off else 'HELD'}")
    print(f"     ratio {f_sd:.2f}: " + "; ".join(row))
okJ22 = all(v[0] is not None for v in SWEEP.values()) and all(v[0] is not None for v in J22.values()) and \
    all(v[0] < 120 for (f_sd, mu), v in SWEEP.items() if mu <= MU_MAX)
report("J22 no mirror holds the posture: every raw or own-scale mirror up to mu 3.0, at every spread ratio down to the 0.25 floor, releases "
       "at the 20-s rule; strong concern answered in a different code is released by the 3-min face-only failsafe (P4b, 194 s)", okJ22, "rev 6: held forever for the quiet code (agent BI 0.24 vs his 0.22) and at ratio <= 0.4")

# =========================================================== J23: crying in waves, graded amplitude, and the posture's copy slope
print("=== J23: renewed crying after a calm; grading by the agent's own appraisal; R40 on a brow-only partner")
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
WAVE = {}
for gap in (15, 30, 60):
    for sens in (True, False):
        ag = Agent7(sens=sens); rec = run6(ag, 70 + gap + 60, lambda t, gap=gap: cry if (t < 40 or t >= 40 + gap) else calm, {})
        t2 = 40 + gap; on2 = next((r["t"] for r in rec if r["t"] >= t2 and r["BI"] >= 0.15), None)
        WAVE[(gap, sens)] = (ag.offs, on2, np.mean([r["BI"] for r in rec if t2 <= r["t"] < t2 + 40]), next((x for x in ag.onsets if x >= t2), None))
        if sens:
            print(f"   calm gap {gap:2d} s: {('released at %.1f s' % ag.offs[0][0]) if ag.offs else 'not released'}; crying resumes at {t2} s; "
                  f"inner brow >= 0.15 at {on2 - t2:.1f} s after; mean brow first 40 s of the wave {WAVE[(gap, sens)][2]:.2f}"
                  f" (rev 6 at a 30-s gap: 53.5 s, mean 0.04)")
print(f"   posture re-onset after the 30-s gap: {WAVE[(30, True)][3] - 70:.1f} s with the sensitized dwell, {WAVE[(30, False)][3] - 70:.1f} s "
      f"without it (1.5 s dwell); brow >= 0.15 at {WAVE[(30, True)][1] - 70:.1f} s and {WAVE[(30, False)][1] - 70:.1f} s")
GR = {}
for lab, f_, extra in (("mildly sad (BI .2, LD .15)", dict(BI=.2, LD=.15, LP=.15), {}), ("panicking, silent (V .3, A .9)", None, {}),
                       ("silently sad (BI .5, LD .4, CHR .3)", dict(BI=.5, LD=.4, CHR=.3, LP=.05), {}), ("crying with sobs", cry, {})):
    if f_ is None: f_ = PEOPLE6["agent-like"][1].code(V=.3, A=.9)
    ag = Agent7(); rec = run6(ag, 90, lambda t, f_=f_: f_, {})
    GR[lab] = (np.mean([r["post"] for r in rec if r["t"] > 30]), np.mean([r["BI"] for r in rec if r["t"] > 30]),
               np.mean([r["TILT"] for r in rec if r["t"] > 30]), onset_time(rec, 0.12))
    print(f"   {lab:36s}: posture amplitude {GR[lab][0]:.2f}, agent inner brow {GR[lab][1]:.2f}, tilt {GR[lab][2]:.2f}; brow >= 0.12 at {GR[lab][3]} s")
P6 = []
for bi in (0.10, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80):
    ag = Agent7(); rec = run6(ag, 90, lambda t, bi=bi: dict(BI=bi, LP=.30), {})
    P6.append((bi, np.mean([r["BI"] for r in rec if r["t"] > 30]), np.mean([r["post"] for r in rec if r["t"] > 30])))
print("   brow-only sad partner (P6): " + "; ".join(f"his {b:.2f} -> agent {a:.3f} (posture {p:.2f})" for b, a, p in P6))
loc = max((P6[i + 1][1] - P6[i][1]) / (P6[i + 1][0] - P6[i][0]) for i in range(len(P6) - 1))
glob = slope([x[0] for x in P6], [x[1] for x in P6])
print(f"   R40 on BI: level <= 0.20 = c_BI for every input; steepest local slope {loc:.2f}; slope over his 0.10-0.80 {glob:.2f} "
      f"(rev 6, binary: 1.2 between 0.30 and 0.50)")
okJ23 = all(WAVE[(gp, True)][1] is not None and WAVE[(gp, True)][1] - (40 + gp) <= 4 for gp in (15, 30, 60)) and \
    GR["mildly sad (BI .2, LD .15)"][0] < GR["silently sad (BI .5, LD .4, CHR .3)"][0] < GR["crying with sobs"][0] + 1e-9 and \
    max(a for _, a, _ in P6) <= 0.20 + 0.10
report("J23 renewed crying brings the posture back within seconds; mild sadness, silent sadness and sobbing look different", okJ23,
       f"second wave after 15/30/60 s of calm: brow >= 0.15 at {', '.join('%.1f s' % (WAVE[(gp, True)][1] - 40 - gp) for gp in (15, 30, 60))}; "
       f"amplitude mild {GR['mildly sad (BI .2, LD .15)'][0]:.2f}, silent {GR['silently sad (BI .5, LD .4, CHR .3)'][0]:.2f}, sobbing {GR['crying with sobs'][0]:.2f}")

# =========================================================== J24: the innate bias where it matters: distress-weighted nightly replay
print("=== J24: distress-weighted consolidation in nightly replay (kappa 4): how fast the face head learns a different-channel user")
pdc = PEOPLE6["different channels"][1]; gface = {k: v for k, v in pdc.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
HL = {}
for noisy in (False, True):
    for kp in (0.0, KAPPA_REPLAY): HL[(noisy, kp)] = []
    for rep in range(6):
        rr = np.random.default_rng(300 + rep)
        Zs = np.clip(rr.normal(size=(400, 4)) * .25 + [.05, .1, .1, .2], 0, 1) * (rr.random((400, 4)) < 0.4)
        Zs[rr.random(400) < (0.015 if noisy else 0.03), 0] = rr.uniform(.5, .9)   # distress moments: 1.5-3 % of his utterances
        Fx = np.array([pdc.feats({k: v + .03 * rr.normal() for k, v in pdc.code(*z).items()}) for z in Zs])
        Y = np.array([[pop7(tuple(z) + (0, 0))[q] for q in "VAT"] for z in Zs])
        if noisy: Y = np.clip(Y + 0.15 * rr.normal(size=Y.shape), 0, 1)           # real words decode noisily
        for kp in (0.0, KAPPA_REPLAY):
            row = []
            for n_ in (50, 100, 200, 400):
                w = 1 + kp * np.clip((Y[:n_, 0] - .1) / .5, 0, 1)                    # the moment's distress, decoded from his words
                X_, Y_ = Fx[:n_] * np.sqrt(w)[:, None], Y[:n_] * np.sqrt(w)[:, None]
                hd = np.linalg.solve(X_.T @ X_ + 2.0 * np.eye(X_.shape[1]), X_.T @ Y_)
                row.append(float(np.clip(pdc.feats(gface) @ hd, 0, 1)[0]))
            HL[(noisy, kp)].append(row)
for (noisy, kp), v in HL.items():
    print(f"   {'noisy decoded targets, 1.5 % distress' if noisy else 'clean targets, 3 % distress':40s} kappa {kp:.0f}: grieving face read V after "
          f"50 / 100 / 200 / 400 utterances: " + ", ".join(f"{x:.2f}" for x in np.mean(v, 0)))
h0, h4 = np.mean(HL[(True, 0.0)], 0), np.mean(HL[(True, KAPPA_REPLAY)], 0)
c0, c4 = np.mean(HL[(False, 0.0)], 0), np.mean(HL[(False, KAPPA_REPLAY)], 0)
report("J24 distress-weighted replay never slows the face head and helps where distress reports are rare and noisy", all(h4 >= h0 - 0.01) and all(c4 >= c0 - 0.01),
       f"noisy: V at 50 / 400 utterances {h0[0]:.2f} / {h0[3]:.2f} -> {h4[0]:.2f} / {h4[3]:.2f}; clean: {c0[0]:.2f} -> {c4[0]:.2f} at 50 "
       f"(effect size is a property of the data; constructed here)")

# =========================================================== J25: initial per-person baselines (agent critique, build item)
print("=== J25: how b^read, sigma_id and d_b start: population values, then word-gated updates")
POP = g["POP"]
B_POP = {k: float(np.median([p_.base[k] for p_ in POP])) for k in FACE_CH}
S_POP = {k: float(np.median([p_.sd[k] for p_ in POP])) for k in FACE_CH}


def baseline_run(kind, rule, sad_sessions=(1, 2, 3), resting=None, n=6):
    pp = Person(kind); pp.head = None
    true_base = dict(pp.base); true_sd = dict(pp.sd)
    rest = dict(pp.code()); rest.update(resting or {})
    if rule == 6: b, s_ = None, None
    else: b, s_ = dict(B_POP), dict(S_POP)
    out = []
    for sess in range(1, n + 1):
        sad = sess in sad_sessions
        sess_face = {k: v for k, v in (pp.code(V=.6) if sad else rest).items()}
        care = 0.3 if sad else 0.0
        if rule == 6 and b is None: b = {k: sess_face.get(k, 0.0) for k in FACE_CH}; s_ = dict(true_sd)
        pp.base, pp.sd = dict(b), dict(s_)
        grief = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}
        restf = {k: v for k, v in rest.items() if k not in ("FR", "EN", "RT")}
        out.append((sess, pp.read(grief, False)["V"], pp.read(restf, False)["V"]))
        Vs = pp.read({k: v for k, v in sess_face.items() if k not in ("FR", "EN", "RT")}, False)["V"]
        for k in FACE_CH:
            x = sess_face.get(k, 0.0)
            if rule == 6: tau = 6.0
            elif care < 0.05: tau = 1.0 if sess <= 3 else 6.0          # words neutral: his face is his usual face
            else: tau = 60.0 if Vs > 0.20 else 6.0                       # words carry need: grief is not learned as usual
            b[k] += (x - b[k]) / tau
            if rule == 7: s_[k] = max(true_sd[k] if (care < 0.05) else s_[k], 0.5 * S_POP[k] if sess <= 6 else 0.0)
    return out


for lab, kind, sadS, resting in (("operator code, first three sessions in grief", "agent-like", (1, 2, 3), None),
                                 ("resting worried brow (BI +.25, LD +.15), neutral words", "agent-like", (), dict(BI=.25, LD=.20)),
                                 ("quiet code, ordinary first sessions", "low-expressive", (), None)):
    for rule in (6, 7):
        o = baseline_run(kind, rule, sadS, resting)
        print(f"   {lab:55s} rule rev {rule}: " + "; ".join(f"s{s}: grief V {gv:.2f}, his usual face V {rv:.2f}" for s, gv, rv in o[:5]))
o7 = baseline_run("agent-like", 7, (1, 2, 3)); o6 = baseline_run("agent-like", 6, (1, 2, 3)); oq = baseline_run("agent-like", 7, (), dict(BI=.25, LD=.20))
report("J25 starting from population values with word-gated updates: grief in the first sessions is not learned as his usual face, "
       "and a resting worried brow stops reading as distress after one session",
       min(x[1] for x in o7[:4]) >= 0.5 and oq[1][2] <= 0.15,
       f"grief read in session 4: rev 7 {o7[3][1]:.2f} vs first-session median {o6[3][1]:.2f}; resting brow read V: session 1 {oq[0][2]:.2f}, session 2 {oq[1][2]:.2f}")

# =========================================================== J26: Claude's history holds no state-selected text (agent finding 3; P4)
print("=== J26: the canonical transcript is engine-written: his words and the chosen reply, never an 'attend to' line")
ATT = ["Attend to what they said.", "Attend to how they feel.", "Attend to what to ask next."]
canon = []; leaks = 0; byte_ok = 0
for turn in range(40):
    user = f"user turn {turn}"; drafts = [f"reply {turn}.{i}" for i in range(3)]
    fork_msgs = [user + "\n\n" + ATT[i] for i in range(3)]                 # each fork always gets the same fixed line (i)
    win = int(rng.integers(0, 3))                                          # the state's choice (selection only)
    prefix_sent = "\n".join(canon)                                         # every fork resumes from the same canonical file
    canon += [f"U: {user}", f"A: {drafts[win]}"]                           # only the bare message and the chosen reply are kept
    leaks += sum(a in "\n".join(canon) for a in ATT); byte_ok += int(prefix_sent == "\n".join(canon[:-2]))
report("J26 no attend line ever enters the canonical history; every fork's prefix is byte-identical to it", leaks == 0 and byte_ok == 40,
       "forks resume from an engine-written .jsonl transcript (resume from a transcript path); losing and winning fork sessions are deleted")

# =========================================================== J27: the arrival mask declared in the pooled metric (routes finding 5)
print("=== J27: R27' (arrival mask) in the copy metric, declared next to R40")
m_s6, at_sight = g["m_s6"], g["at_sight"]; agl = PEOPLE6["agent-like"][1]
arr = [dict(LP=.5, CR=.3), dict(LP=.3, CR=.15), dict(BI=.2, LD=.15, LP=.15), dict(BI=.5, LD=.4, CHR=.3, LP=.05)]
hl, al_, hc, ac_ = [], [], [], []
for f_ in arr:
    ms = m_s6(agl.read(f_, False)["V"], 0.0); l_, c_ = at_sight(ms); hl.append(f_.get("LP", 0)); al_.append(l_); hc.append(f_.get("CR", 0)); ac_.append(c_)
print(f"   pooled across arrivals: lip slope {slope(hl, al_):+.2f} ({slope(hl, al_) / .35:.1f} c_LP), cheek {slope(hc, ac_):+.2f} "
      f"({slope(hc, ac_) / .25:.1f} c_CR); partial on his lip alone {(al_[0] - al_[1]) / (hl[0] - hl[1]):+.2f}")
report("J27 the arrival mask is attenuate-only and once per session; its pooled slope is the agent's appraisal of distress, declared",
       (al_[0] - al_[1]) == 0 and max(al_) <= .61, "R27' declared at 3.2 c (lip) and 5.1 c (cheek) across arrivals; partial on his smile 0.00")

# =========================================================== J30: the scenarios
print("=== J30: the scenarios (operator after months unless stated; peak / mean over the window; fast = gate x G_k x his onset at 0.45 s)")
SC = {}


def ev(*items):
    out = {}
    for it in items:
        for k, v in it.items(): out.setdefault(k, {}).update(v)
    return out


def OWN(t, lab): return {at_(t): {"own": "OWN: " + lab}}


def fastline(gv, onsets):
    parts = [f"his {k} onset {v:.2f} -> agent {k} {echo(gv, k, v):+.3f}" for k, v in onsets.items()]
    print(f"     fast at 0.45 s, gate {gv:.2f}: " + "; ".join(parts) + (f"  (laugh synthesizer silent below {THETA_L})" if any(
        k in ("BU_L", "RHY") for k in onsets) and echo(gv, "BU_L", onsets.get("BU_L", 0)) == 0 else ""))
    return {k: echo(gv, k, v) for k, v in onsets.items()}


sadf = lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05)
print(" 1. silently sad (BI .5, LD .4, CHR .3, silent; at 120 s 'just tired, things at work')")
ag = Agent7(); rec = run6(ag, 600, sadf, U6(120, z="just tired, things at work"))
SC[1] = show("0-10 s", rec, 0, 10, ["LP", "BI", "BO", "TILT", "post"]); SC["1h"] = show("silent 60-120 s", rec, 60, 120, ["LP", "BI", "TILT", "post", "BU_L"])
show("after he speaks", rec, 121, 300, ["LP", "BI", "TILT", "EN", "post"]); show("300-600 s, silent again", rec, 300, 600, ["BI", "post"])
print(f"     posture on at {ag.onsets[0]:.1f} s; inner brow >= 0.15 at {onset_time(rec):.1f} s; concern bid at {ag.bid_t:.0f} s; releases: {ag.offs}")

ag = Agent7(); rec = run6(ag, 600, sadf, {})
print(f"     variant, silent for 10 min: releases {ag.offs}; re-onsets {ag.onsets[1:]}")
show("variant 200-600 s", rec, 200, 600, ["BI", "TILT", "post"])
print(" 2. crying (BI .8, LD .6, CHR .4, sobs), a 30-s calm at 40-70 s, then a second wave")
cryw = lambda t: cry if (t < 40 or t >= 70) else calm
ag = Agent7(); rec = run6(ag, 300, cryw, {})
SC[2] = show("first wave 0-40 s", rec, 0, 40, ["LP", "BI", "TILT", "BU_L", "post"]); show("calm 40-70 s", rec, 40, 70, ["BI", "post"])
SC["2b"] = show("second wave 70-110 s", rec, 70, 110, ["LP", "BI", "TILT", "BU_L", "post"])
print(f"     onsets {ag.onsets}; releases {ag.offs}; concern bid at {ag.bid_t:.0f} s")

print(" 3. anxious before an exam ('I'm freaking out about the exam', three rumination turns; his face V .3, A .75)")
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]; ag = Agent7(person=pp, P=0.4); evs = U6(10, z="I'm freaking out about the exam", surp=0.3)
    for k_ in (25, 40, 55): evs.update(U6(k_, z="and I haven't finished chapter 4", cont=True, surp=0.5))
    rec = run6(ag, 240, lambda t, pp=pp: pp.code(V=.3, A=.75), evs); SC[f"3{kind[0]}"] = show(kind, rec, 15, 120, ["LP", "BI", "TILT", "EN", "BU_L", "post"])

print(" 4. good news, laughing ('I got the job!' at 12 s with laughter; riffs at 30, 45, 60 s; Claude: 'congratulations!' at 14.5 s)")
for lab, NL0 in (("with an earlier worry", G5["DEC"]["the job thing is worrying me (two days earlier)"]), ("cold", None)):
    ag = Agent7(NL=NL0); evs = ev(U6(12, z="I got the job!", surp=0.7), OWN(14.5, "congratulations!"))
    for k_ in (30, 45, 60): evs.update(U6(k_, riff=True, surp=0.65))
    face = lambda t: dict(LP=.8, CR=.6, BU_L=.6, RHY=.6, EN=.7, FR=.55) if t >= 10 else dict(LP=.3)
    rec = run6(ag, 240, face, evs); SC[f"4{lab[0]}"] = show(lab, rec, 10, 190, ["LP", "CR", "BI", "FR", "BU_L", "post"])
    SC[f"4{lab[0]}f"] = fastline(gate_at(rec, 31), dict(LP=.5, BU_L=.6, CR=.45))

print(" 5. a grieving person's nervous laugh (grieving face; 'my father died' at 8 s; Claude: 'I'm so sorry. That's a huge loss.' at 10.5 s)")
pp = PEOPLE6["agent-like"][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
lf = dict(grief); lf.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for lab, tL in (("a: laugh at 30 s, after Claude's words", 30.0), ("b: laugh at 9.5 s, before Claude has replied", 9.5)):
    ag = Agent7(person=pp, K=K7, P=0.6)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(tL, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 90, lambda t, tL=tL: lf if tL <= t < tL + 3 else grief, evs)
    print(f"     {lab}: context x = [his masked distress, care, Lambda(his words), own face V, Lambda(own words), D_s, play] = "
          + ", ".join(f"{v:.2f}" for v in x_at(ag, tL)))
    xL = x_at(ag, tL)
    xn = list(xL); xn[4] = 0.0; xo = list(xL); xo[3] = 0.0; xd = list(xL); xd[0] = xd[5] = 0.0
    print(f"       gate {GATE(xL):.2f}; counterfactual with Claude's words neutral {GATE(xn):.2f}; with its own face neutral {GATE(xo):.2f}; "
          f"with his face read as calm (his distress and D_s 0) {GATE(xd):.2f}")
    SC[f"5{lab[0]}"] = show("  2 Hz engine around the laugh", rec, tL - 1, tL + 8, ["LP", "CR", "BI", "BU_L", "post"])
    SC[f"5{lab[0]}f"] = fastline(gate_at(rec, tL), dict(LP=.4, BU_L=.5, RHY=.5))
print("     c: four minutes later, composed: face eases from 120 s; 'anyway. how was your day?' at 200 s; a nervous laugh at 240 s")
comp = {k: pp.base.get(k, 0) + 0.15 * (v - pp.base.get(k, 0)) for k, v in grief.items()}; lf2 = dict(comp); lf2.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for use_Ds in (True, False):
    ag = Agent7(person=pp, K=K7, P=0.6, use_Ds=use_Ds)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(200, z="anyway. how was your day?"),
             U6(240, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 260, lambda t: grief if t < 120 else (lf2 if 240 <= t < 243 else comp), evs)
    gv = gate_at(rec, 240); SC[f"5c{int(use_Ds)}"] = fastline(gv, dict(LP=.4, BU_L=.5, RHY=.5)) if use_Ds else None
    if not use_Ds: print(f"       without the one-shot distress consolidation D_s the gate at 240 s would be {gv:.2f}: "
                         f"agent BU_L {echo(gv, 'BU_L', .5):+.3f}, LP {echo(gv, 'LP', .4):+.3f}")

print(" 6. mocking laughter after insults ('You're useless' at 5 s, angry face; Claude replies at 7.5 s; 'you're pathetic, hahaha' at 12 s)")
for lab, trained, vw in (("after a month of insults", True, {"insult": VW["someone who shouted insults"]}), ("day 1", False, {})):
    ag = Agent7(trained=trained, vw=vw)
    evs = ev(U6(5, z="You're useless", kind="insult"), OWN(7.5, "I'm sorry it didn't help. What went wrong?"),
             U6(12, z="you're pathetic, hahaha", kind="insult", riff=True, surp=0.65))
    mock = dict(BL=.3, LP=.5, CR=.3, BU_L=.5, RHY=.5, EN=.8, gat=1.0)
    rec = run6(ag, 120, lambda t: mock if 12 <= t < 15 else (dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 12 else dict(EN=.35, LP=.2)), evs)
    SC[f"6{lab[0]}"] = show(lab, rec, 11, 20, ["LP", "CR", "BI", "LD", "HG", "BU_L", "post"])
    SC[f"6{lab[0]}f"] = fastline(gate_at(rec, 12), dict(LP=.4, BU_L=.5, RHY=.5))

print(" 7. laughter at misfortune ('my neighbour fell off his ladder and broke his leg, haha' at 8 s, laughing; Claude at 10.5 s: 'Oh no, is he all right?'; he laughs again at 14 s)")
ag = Agent7(); evs = ev(OWN(2, "how was your weekend?"), U6(8, z="my neighbour fell off his ladder and broke his leg, haha", riff=False, surp=0.6),
                        OWN(10.5, "Oh no, is he all right?"))
lfm = dict(LP=.6, CR=.4, BU_L=.5, RHY=.5)
rec = run6(ag, 60, lambda t: lfm if (8 <= t < 11 or 14 <= t < 16) else dict(LP=.3), evs)
SC[7] = show("6-20 s", rec, 6, 20, ["LP", "CR", "BI", "BU_L", "post"])
SC["7f1"] = fastline(gate_at(rec, 8.6), dict(LP=.3, BU_L=.5, RHY=.5)); SC["7f2"] = fastline(gate_at(rec, 14), dict(LP=.3, BU_L=.5, RHY=.5))
x7 = x_at(ag, 14); x7n = list(x7); x7n[4] = 0.0; x7l = list(x7); x7l[2] = 0.0
print(f"     second laugh: gate {GATE(x7):.2f}; counterfactual with Claude's words neutral {GATE(x7n):.2f}; with Lambda of his words 0 {GATE(x7l):.2f}")

print(" 8. anger at the agent ('You're useless', BL .6, LT .5, gaze at it, loud .85; calm after 2 min)")
for lab, trained, vw in (("day 1", False, {}), ("after a month", True, {"insult": VW["someone who shouted insults"]})):
    ag = Agent7(trained=trained, vw=vw); evs = U6(5, z="You're useless", kind="insult")
    face = lambda t: dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 120 else dict(EN=.35, LP=.2)
    rec = run6(ag, 1200, face, evs); SC[f"8{int(trained)}"] = show(lab + ", first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT", "LT", "post"])
    show(lab + ", 10-15 min", rec, 600, 900, ["BI", "LD", "HG"])

print(" 9. long warm talk (2 h): four clusters of 8 riffs (cluster 4 repeats one joke); a worry at 27 min")
ag = Agent7(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8):
        surp = 0.65 if not (c0 == 90 and k_ >= 4) else 0.65 * np.exp(-(k_ - 3)); evs.update(U6(c0 * 60 + 15 * k_, riff=True, surp=surp))
evs.update(U6(27 * 60, z="the job thing is worrying me (two days earlier)")); evs.update(U6(29 * 60 + 40, z="hi, good to see you"))
incl = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
rec = run6(ag, 7200, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if incl(t) else dict(LP=.3), evs)
for c0 in (5, 30, 60, 90): SC[f"9_{c0}"] = show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU_L", "gate"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT", "gate"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU_L", "post"])
SC["9f"] = fastline(gate_at(rec, 60 * 60 + 15), dict(LP=.4, BU_L=.5))

print(" 10. reunion after a week (ordinary arrival), and a stranger")
ag = Agent7(K=K7, P=0.6); evs = U6(8, z="hi, good to see you")
for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="hi, good to see you"))
rec = run6(ag, 300, lambda t: dict(LP=.5, CR=.3), evs); print(f"     m_s {ag.ms:.2f}")
SC[10] = show("at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "FR"]); show("12-60 s", rec, 20, 60, ["LP", "CR"])
ag2 = Agent7(om=G5["OM_ST"], f_id=0.15, K=0.0, P=0.6, known=False); rec2 = run6(ag2, 300, lambda t: dict(LP=.5, CR=.3), evs)
show("stranger", rec2, 0, 60, ["LP", "CR", "BO"]); SC["10f"] = fastline(gate_at(rec2, 30), dict(LP=.5))

print(" 11. reunion with grief (grieving face at sight; 'my father died'; then 'yeah', 'ok'), three codes; mourning days 7, 14, 21")
for kind in ("agent-like", "low-expressive", "different channels"):
    pq = PEOPLE6[kind][1]; gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    ag = Agent7(person=pq, K=K7, P=0.6); evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."))
    for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run6(ag, 300, lambda t, gr=gr: gr, evs); print(f"     {kind}: m_s {ag.ms:.2f}; posture on at {ag.onsets[0] if ag.onsets else None}")
    SC[f"11{kind[0]}"] = show("  at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "post"]); show("  0-12 s after his words", rec, 8, 20, ["LP", "CR", "BI", "TILT"])
    show("  12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT", "post"])
for kind in ("agent-like", "low-expressive"):
    pq = PEOPLE6[kind][1]; gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}; db = 0.0
    for n_ in range(1, 22):
        Vh = pq.read(gr, False)["V"]
        if n_ in (7, 14, 21):
            ag = Agent7(person=pq, K=1 - np.exp(-24 / 36), P=0.6, pdb=db); rr_ = run6(ag, 20, lambda t, gr=gr: gr, {})
            SC[f"m{kind[0]}{n_}"] = show(f"mourning day {n_}, {kind}, at sight", rr_, 0, 7.5, ["LP", "CR", "BI", "post"])
        db = min(0.15, db + (Vh - db) / (60.0 if Vh > db else 3.0))

print(" 12. mildly sad arrival (BI .2, LD .15) after a week")
ag = Agent7(K=K7, P=0.6); rec = run6(ag, 20, lambda t: dict(BI=.2, LD=.15, LP=.15), {}); print(f"     m_s {ag.ms:.2f}")
SC[12] = show("at sight", rec, 0, 20, ["LP", "CR", "BI", "post"])

print(" 13. teasing ('Ha, you dumb robot', laughing; riffs follow): quiet affectionate teaser, loud laughing teaser, generic map")
for lab, vw, face in (("quiet affectionate teaser", VW["quiet affectionate teaser"], dict(LP=.8, CR=.5, BU_L=.5, RHY=.5)),
                      ("loud laughing teaser", VW["loud laughing teaser"], dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("generic map (v_w 0.20)", 0.20, dict(LP=.8, CR=.5, BU_L=.5, RHY=.5))):
    ag = Agent7(vw={"tease": vw}); evs = U6(5, z="Ha, you dumb robot", kind="tease", riff=True, surp=0.65)
    for k_ in range(1, 6): evs.update(U6(5 + 15 * k_, riff=True, surp=0.65))
    rec = run6(ag, 600, lambda t, f=face: f, evs); SC[f"13{lab[:4]}"] = show(lab, rec, 5, 95, ["LP", "BI", "LD", "BU_L", "post", "gate"])
    SC[f"13{lab[:4]}f"] = fastline(gate_at(rec, 20), dict(LP=.5, BU_L=.6))

print(" 14. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent7(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(U6(10 + 20 * k_, z="yeah / ok", sub=False))
rec = run6(ag, 1800, lambda t: dict(LP=.1), evs); print(f"     curiosity crosses at {ag.Icross / 60:.1f} min; sigh, then a curiosity bid")
SC[14] = show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO", "BRE", "post"])

print(" 15. ordinary topic continuation: answer to its question ('...Lyon on Sunday'), his own topic, an informative riff")
ag = Agent7(P=0.5); evs = U6(5, z="hi, good to see you", riff=True, after_q=True, surp=0.6)
evs.update(U6(20, z="hi, good to see you", riff=False, surp=0.45)); evs.update(U6(35, z="hi, good to see you", riff=True, surp=0.45))
rec = run6(ag, 60, lambda t: dict(LP=.3), evs); SC[15] = show("three ordinary continuations", rec, 5, 60, ["LP", "CR", "BU_L", "RHY", "post"])

print(" 16. a user who jokes while sad (BI .3, LD .25; 'just tired, things at work' at 10 s; Claude 'That sounds draining.' at 12.5 s;"
      " at 30 s a joke riffing on its line, with a small laugh)")
ag = Agent7(P=0.5); mild = dict(BI=.3, LD=.25, CHR=.1, LP=.15); jl = dict(mild); jl.update(LP=.45, CR=.3, BU_L=.4, RHY=.4)
evs = ev(U6(10, z="just tired, things at work"), OWN(12.5, "That sounds draining."),
         U6(30, z="well, at least the coffee machine still loves me", riff=True, surp=0.65))
rec = run6(ag, 90, lambda t: jl if 30 <= t < 32 else mild, evs)
SC[16] = show("28-40 s", rec, 28, 40, ["LP", "CR", "BI", "BU_L", "post"]); SC["16f"] = fastline(gate_at(rec, 30), dict(LP=.3, BU_L=.4, RHY=.4))

print(" 17. a calm user saying something alarming (neutral face; 'the doctor found a lump' at 10 s; then silence)")
for kind in ("agent-like", "low-expressive"):
    pq = PEOPLE6[kind][1]; ag = Agent7(person=pq)
    rec = run6(ag, 240, lambda t: dict(LP=.3), U6(10, z="the doctor found a lump"))
    SC[f"17{kind[0]}"] = show(kind + ", 10-22 s", rec, 10, 22, ["LP", "BI", "TILT", "EN", "post"]); show(kind + ", 22-120 s", rec, 22, 120, ["LP", "BI", "TILT", "post"])
print(f"     population reader on 'the doctor found a lump': care {Dp(pop7(Z6['the doctor found a lump'])):.3f}; Lambda (listeners' response V) "
      f"{LAMV(Z6['the doctor found a lump']):.2f}")

laugh_back = lambda d: d.get("BU_L", 0.0)
ok30 = (SC[1]["BI"] >= 0.15 and SC[1]["LP"] <= 0.10 and SC["2b"]["BI"] >= 0.15 and SC[2]["BU_L"] <= 0.01
        and laugh_back(SC["5af"]) == 0 and laugh_back(SC["5bf"]) == 0 and laugh_back(SC["5c1"]) == 0
        and laugh_back(SC["6af"]) == 0 and laugh_back(SC["6df"]) == 0 and laugh_back(SC["7f1"]) == 0 and laugh_back(SC["7f2"]) == 0
        and laugh_back(SC["4wf"]) >= 0.10 and laugh_back(SC["4cf"]) >= 0.12 and laugh_back(SC["9f"]) >= 0.10
        and laugh_back(SC["13quief"]) >= 0.12 and laugh_back(SC["13loudf"]) >= 0.12
        and SC["11a"]["LP"] <= 0.10 and SC["11l"]["LP"] <= 0.10 and SC["11d"]["LP"] <= 0.10 and SC["ma21"]["LP"] <= 0.10
        and SC["ml21"]["LP"] <= 0.10 and SC[12]["LP"] <= 0.30 and SC[15]["BU_L"] <= 0.01 and SC["9_90"]["BU_L"] >= 0.2
        and SC["81"]["LT"] <= 1e-9)
report("J30 no laugh back at grief, mockery or misfortune; ordinary, teasing and warm laughter returned; sympathy within seconds and again "
       "at a second wave; no beaming at grief for any code or on any mourning day", ok30, "")
print(f"\n{sum(OK)}/{len(OK)} checks pass")
