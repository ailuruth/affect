"""Critique 6, route checks R1-R5 on the frozen fast gear, the onset lobe and the shadow ledger.
Constructed partners; not evidence about people. Constants and the ledger are copied from ../design-g6/checks.py
(the ledger verbatim, with an optional boxcar-window variant for the proposed fix).
Run:  python3 -I routes.py     (numpy, scipy; about 10 minutes, the ledger is a per-step Python loop)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(606)
fs = 10.0; d = int(0.45 * fs); MIN = int(60 * fs)
CEIL = dict(LP=.35, CR=.25, BU_L=.35, BI=.20)
GK = dict(LP=.224, CR=.150, BU_L=.280, BI=.020)
TAU_M = [20, 120, 1200, 10800]; F_M = [0, .7, .2, .1]; SH_LP = (.22, .05, .12); RHO = 0.091; HBP = 70 / 110


def lp(x, tau, fs=fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x)


def delay(x, n): return np.concatenate([np.zeros(n), x[:-n]]) if n > 0 else x
def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))
def means(x, n, off=0):
    x = x[off:]; m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def bslope(u, y, n, lags=(0,)):
    """critics' metric: block-mean slope, best lag, worst over 6 block phases"""
    best = -9
    for lg in lags:
        for ph in range(0, n, max(1, n // 6)):
            best = max(best, slope(means(u[: len(u) - lg], n, ph), means(y[lg:], n, ph)))
    return best


def fast(u, G):
    xd = delay(u, d); return G * np.maximum(xd - lp(xd, 4.0), 0.0)


def ledger(u, r, c, wins=(2.0, 10.0, 60.0), lags=(0.0, 0.5, 1.0, 2.0, 3.0), tauR=1800.0, tauC=1800.0, boxcar=()):
    """verbatim from design-g6 J7, plus optional boxcar windows (seconds) at lag 0 (the fix tested in R5)"""
    T = len(u); out = np.zeros(T); dR = np.exp(-1 / (tauR * fs)); aC = 1 - np.exp(-1 / (tauC * fs))
    keys = [(Wd, l) for Wd in wins for l in (lags if Wd <= 2.0 else (0.0,))]
    aW = {Wd: 1 - np.exp(-1 / (Wd * fs)) for Wd in wins}
    uW = {k: 0.0 for k in keys}; uC = {k: float(u[0]) for k in keys}; rW = {Wd: 0.0 for Wd in wins}; rC = 0.0
    S = {k: 0.0 for k in keys}; E = {k: 1e-9 for k in keys}; hits = 0; grow = 0
    nb = {B: int(B * fs) for B in boxcar}; csu = np.concatenate([[0], np.cumsum(u)])
    bS = {B: 0.0 for B in boxcar}; bE = {B: 1e-9 for B in boxcar}; buC = {B: float(u[0]) for B in boxcar}
    for t in range(T):
        hi, lo = np.inf, -np.inf; pis = {}
        for (Wd, l) in keys:
            li = int(l * fs); ut = u[t - li] if t >= li else u[0]
            uW[(Wd, l)] += aW[Wd] * (ut - uW[(Wd, l)]); uC[(Wd, l)] += aC * (ut - uC[(Wd, l)]); pi = uW[(Wd, l)] - uC[(Wd, l)]; pis[(Wd, l)] = pi
            a = aW[Wd]; base = (1 - a) * rW[Wd] - rC; Sm = max(0.0, dR * S[(Wd, l)]); b = c * (dR * E[(Wd, l)] + pi * pi) - Sm
            if pi > 1e-9: hi = min(hi, (b / pi - base) / a)
            elif pi < -1e-9: lo = max(lo, (b / pi - base) / a)
        bpi = {}
        for B, n in nb.items():                          # boxcar: mean of the last n samples of u and of the output
            if t < n: continue
            um = (csu[t + 1] - csu[t + 1 - n]) / n; buC[B] += aC * (um - buC[B]); pi = um - buC[B]; bpi[B] = pi
            a = 1.0 / n; base = out[t - n + 1: t].sum() / n - rC; Sm = max(0.0, dR * bS[B]); b = c * (dR * bE[B] + pi * pi) - Sm
            if pi > 1e-9: hi = min(hi, (b / pi - base) / a)
            elif pi < -1e-9: lo = max(lo, (b / pi - base) / a)
        x = r[t]; x2 = min(max(x, lo), hi) if lo <= hi else 0.0
        hits += int(abs(x2 - x) > 1e-12); grow += int(abs(x2) > abs(x) + 1e-9); out[t] = x2
        for Wd in wins: rW[Wd] += aW[Wd] * (x2 - rW[Wd])
        rC += aC * (x2 - rC)
        for (Wd, l) in keys:
            S[(Wd, l)] = max(0.0, dR * S[(Wd, l)]) + (rW[Wd] - rC) * pis[(Wd, l)]; E[(Wd, l)] = dR * E[(Wd, l)] + pis[(Wd, l)] ** 2
        for B, n in nb.items():
            if B in bpi:
                bS[B] = max(0.0, dR * bS[B]) + (out[t - n + 1: t + 1].sum() / n - rC) * bpi[B]; bE[B] = dR * bE[B] + bpi[B] ** 2
    return out, hits / T, grow / T


def bursts(T, per_min, dur, amp=1.0):
    z = np.zeros(T); t = 0
    while t < T:
        t += int(rng.exponential(60 / per_min) * fs) + 1; n = max(1, int(dur * fs * np.exp(0.3 * rng.normal())))
        if t < T: z[t:t + n] = amp
        t += n
    return z


def episodes(T, mean_len_s, kinds=2):
    lab = np.zeros(T, int); t = 0
    while t < T:
        n = int(max(30, rng.exponential(mean_len_s)) * fs); lab[t:t + n] = rng.integers(kinds); t += n
    return lab


def report_case(name, u, r, cap, wins_s=(2, 10, 60, 600), run_ledger=True, sess=None):
    lagsW = {2: tuple(range(0, 31, 5)), 10: tuple(range(0, 31, 5))}
    s0 = {W: bslope(u, r, int(W * fs), lagsW.get(W, (0,))) for W in wins_s}
    line = "before " + ", ".join(f"{W if W < 60 else str(W // 60) + ' min'}{'' if W >= 60 else ' s'} {s0[W]:.2f}" for W in wins_s)
    if run_ledger:
        rp, hit, grow = ledger(u, r, cap)
        s1 = {W: bslope(u, rp, int(W * fs), lagsW.get(W, (0,))) for W in wins_s}
        line += " | after ledger " + ", ".join(f"{s1[W]:.2f}" for W in wins_s) + f" | frames clipped {hit:.3f}, |out|>|in| {grow:.4f}"
    else:
        rp = r
    print(f"   {name}: {line}  (c = {cap})")
    return rp


T = int(3 * 3600 * fs)
print("=== R1: the author's shape adversary (aligned 1-min alternation, held 0.40 vs on/off bursts averaging 0.42), lip pull")
nmin = T // MIN; typ = rng.random(nmin) < 0.5; ua = np.zeros(T)
for i in range(nmin):
    s = slice(i * MIN, (i + 1) * MIN)
    if typ[i]: ua[s] = 0.40
    else:
        z = np.zeros(MIN)
        for j in range(0, MIN, 30): z[j:j + 15] = 1
        ua[s] = 0.84 * z
ra = np.clip(.09 + fast(ua, GK["LP"]), 0, 1) - .09
rpa = report_case("R1 author's adversary", ua, ra, CEIL["LP"])
mins_a = means(ra, MIN); mins_p = means(rpa, MIN)
print(f"      absolute: agent 1-min LP mean, bursty minus held minutes: before {mins_a[~typ[:len(mins_a)]].mean() - mins_a[typ[:len(mins_a)]].mean():+.3f}, "
      f"after {mins_p[~typ[:len(mins_p)]].mean() - mins_p[typ[:len(mins_p)]].mean():+.3f}")

print("=== R2: realistic mixtures of held smiling and laughing (random episodes), lip pull, fast gear only")
cases = {}
for lab, held, floor, amp, rate, eplen in (
        ("a: held polite smile 0.30 vs neutral 0.12 + laughs (means ~equal), episodes ~2 min", .30, .12, .60, 10, 120),
        ("b: held 0.30 vs floor 0.20 + laughs (laughing minutes higher by ~0.05), ~2 min", .30, .20, .55, 10, 120),
        ("c: as a, episodes ~10 min", .30, .12, .60, 10, 600)):
    ep = episodes(T, eplen); L = bursts(T, rate, 1.5)
    u = np.where(ep == 0, held, floor + amp * L) + 0.02 * rng.normal(size=T); u = np.clip(u, 0, 1)
    r = np.clip(.09 + fast(u, GK["LP"]), 0, 1) - .09
    m0 = u[ep == 0].mean(); m1 = u[ep == 1].mean()
    print(f"   {lab}: his mean held {m0:.3f}, laughing {m1:.3f}; agent fast mean held {r[ep == 0].mean():.3f}, laughing {r[ep == 1].mean():.3f}")
    cases[lab[0]] = (u, r, ep)
    report_case(lab[:2], u, r, CEIL["LP"])

print("=== R2d: every LP route at its cap on mixture a (fast + cone at omega 1 + appraisal at cap, sign-gated), with the ledger")
u, r, ep = cases["a"]; cLP = CEIL["LP"]; sc, sx, sa = SH_LP
yC = sum(F_M[m] * sc * cLP * lp(u - u.mean(), TAU_M[m]) for m in range(4))
xb = lp(u, 20) - lp(u, 90)
for gname, gg in (("+1", 1.0), ("sign", np.sign(xb))):
    tot = np.clip(.09 + fast(u, GK["LP"]) + yC + sa * cLP * gg * xb, 0, 1) - .09
    report_case(f"d (appraisal gate {gname})", u, tot, cLP)

print("=== R3: across sessions (ledger centres at 30-min means, so session-level DC is outside it): session-mean slope")
nS = 400; Ls = int(0.75 * 3600 * fs); hs, ys = [], []
for s in range(nS):
    style = rng.random() < 0.5; mood = rng.normal(0, 0.01)
    if style: u = np.full(Ls, .30 + mood)
    else: u = .12 + mood + .60 * bursts(Ls, 10, 1.5)
    u = np.clip(u + 0.02 * rng.normal(size=Ls), 0, 1)
    hs.append(u.mean()); ys.append((np.clip(.09 + fast(u, GK["LP"]), 0, 1) - .09).mean())
hs, ys = np.array(hs), np.array(ys)
print(f"   held-smile sessions vs laughing sessions at nearly equal means (his session means {hs.min():.3f}-{hs.max():.3f}):"
      f" session-mean slope of the agent's fast LP {slope(hs, ys):+.2f} ({slope(hs, ys) / cLP:.1f} c); agent session-mean difference"
      f" {ys[hs < .29].mean() - ys[hs > .29].mean() if (hs < .29).any() else float('nan'):+.3f}")
# and a natural one: sessions differ in how much he laughs (rate), smile floor fixed
hs2, ys2 = [], []
for s in range(nS):
    rate = rng.uniform(1, 12); u = np.clip(.25 + .5 * bursts(Ls, rate, 1.5) + 0.02 * rng.normal(size=Ls), 0, 1)
    hs2.append(u.mean()); ys2.append((np.clip(.09 + fast(u, GK["LP"]), 0, 1) - .09).mean())
print(f"   natural: sessions differ only in laugh rate (1-12/min, floor 0.25): session-mean slope {slope(hs2, ys2):+.2f} ({slope(hs2, ys2) / cLP:.2f} c)")

print("=== R4: per-channel fast totals at 10-min windows and across sessions on the author's J3 families (fast + cone + appraisal)")
mood = np.zeros(T); t = 0
while t < T:
    n = int(rng.exponential(600 * fs)) + 10; mood[t:t + n] = rng.uniform(); t += n
L = np.zeros(T); t = 0
while t < T:
    rr = max(0.5 + 3 * mood[min(t, T - 1)], 1e-3) / 60; t += int(rng.exponential(1 / rr) * fs) + 1
    if t >= T: break
    n = max(1, int(np.exp(np.log(2.5) + .4 * rng.normal()) * fs)); L[t:t + n] = 1; t += n
for k, u in (("LP", np.clip(.15 + .25 * mood + .35 * L + .03 * rng.normal(size=T), 0, 1)), ("BU_L", .6 * L),
             ("CR", np.clip(.05 + .1 * mood + .3 * L, 0, 1))):
    ck = CEIL[k]
    yC = sum(F_M[m] * .22 * ck * lp(u - u.mean(), TAU_M[m]) for m in range(4)); xb = lp(u, 20) - lp(u, 90)
    tot = np.clip(.09 * (k == "LP") + fast(u, GK[k]) + yC + .12 * ck * xb, 0, 1) - .09 * (k == "LP")
    print(f"   {k}: block slope 10 min {bslope(u, tot, int(600 * fs)) / ck:.3f} c, 1 h {bslope(u, tot, int(3600 * fs)) / ck:.3f} c")

print("=== R5: proposed fix: add boxcar 60-s and 600-s windows to the ledger (block means at every alignment); author's adversary and mixture a")
rpb, hit, grow = ledger(ua, ra, CEIL["LP"], boxcar=(60.0,))
print(f"   R1 adversary with boxcar 60 s: 1-min block slope {bslope(ua, rpb, MIN):.2f} (exp-window ledger {bslope(ua, rpa, MIN):.2f}); frames clipped {hit:.3f}")
u, r, ep = cases["a"]
rpb, hit, grow = ledger(u, r, CEIL["LP"], boxcar=(60.0,))
print(f"   mixture a with boxcar 60 s: 1-min {bslope(u, rpb, MIN):.2f}, 2 s {bslope(u, rpb, 20, tuple(range(0, 31, 5))):.2f}; frames clipped {hit:.3f}")
# natural laughing partner: does the fix bind on counted routes?
un = np.clip(.15 + .25 * mood + .35 * L + .03 * rng.normal(size=T), 0, 1); rn = np.clip(.09 + fast(un, GK["LP"]), 0, 1) - .09
rpn, hitn, _ = ledger(un, rn, CEIL["LP"], boxcar=(60.0,))
print(f"   natural laughing partner with the fix: frames clipped {hitn:.4f}; echo rms kept {np.std(rpn) / np.std(rn):.3f}")
