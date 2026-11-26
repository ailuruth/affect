"""Independent routes critique of design-cayley-ledger.md, revision 5: counterexample checks K1-K7.

Constructed partners and admissible parameter values, using the design's own constants (sims/design-g5/checks.py).
They test the design's stated bounds; they are not evidence about people.
Run:  python3 -I checks.py   (numpy, scipy; about a minute)
"""
import numpy as np
from scipy.signal import lfilter

rng = np.random.default_rng(55)


def slope(x, y):
    x = np.asarray(x, float) - np.mean(x); y = np.asarray(y, float) - np.mean(y); return float(x @ y / (x @ x))


def means(x, n):
    m = len(x) // n; return x[: m * n].reshape(m, n).mean(1)


def lp(x, tau, fs):
    a = 1 - np.exp(-1 / (tau * fs)); return lfilter([a], [1, -(1 - a)], x, axis=0)


def hp(x, tau, fs): return x - lp(x, tau, fs)


def delay(x, d): return np.concatenate([np.zeros(d), x[:-d]]) if d > 0 else x


def blocks(T, mean_len, fs):
    x = np.zeros(T); t = 0
    while t < T:
        L = int(rng.exponential(mean_len * fs)) + 10; x[t:t + L] = rng.uniform(0, 1); t += L
    return x


def laughs(rate, T, fs, dur=2.5, spread=0.4):
    z = np.zeros(T); t = 0
    while t < T:
        r = max(rate[min(t, T - 1)], 1e-3) / 60.0; t += int(rng.exponential(1 / r) * fs) + 1
        if t >= T: break
        dd = max(1, int(np.exp(np.log(dur) + spread * rng.normal()) * fs)); z[t:t + dd] = 1; t += dd
    return z


# ---------------------------------------------------------------- the design's constants (revision 5, section 2.1)
GF = 0.45
CEIL = dict(LP=0.35, CR=0.25, BU_L=0.35, RHY=0.30, BRE=0.15, BI=0.20, FR=0.10, EN=0.05, JO=0.10, HP=0.10)
FASTFRAC = dict(LP=1, CR=1, BU_L=1, RHY=1, BRE=1, BI=0.15, FR=1, EN=1, JO=0.3, HP=1)
KAP = {k: FASTFRAC[k] * CEIL[k] * (1 + GF) / (2 * GF) for k in CEIL}
FASTCAP = {k: 2 * GF / (1 + GF) * KAP[k] for k in CEIL}
SH = dict(LP=(0.50, 0.15, 0.25), CR=(0.22, 0.06, 0.08), BU_L=(0.07, 0.02, 0.05), RHY=(0.07, 0.02, 0.05),
          BRE=(0.07, 0.02, 0.05), BI=(0.70, 0.10, 0.05), FR=(0.50, 0.20, 0.35), EN=(0.50, 0.20, 0.35),
          JO=(0.48, 0.15, 0.20), HP=(0.50, 0.20, 0.35))
REST = dict(LP=0.09)
B_W1 = 2 * GF / (1 + GF)

fs = 20.0; T = int(6 * 3600 * fs); d = int(0.45 * fs)
mood = blocks(T, 10 * 60, fs); L = laughs(0.5 + 3.0 * mood, T, fs)
# a laughing partner whose smile, cheek, laugh burst, rhythm, breath and F0 range co-move (H9's partner, extended)
U = dict(LP=np.clip(0.15 + 0.25 * mood + 0.35 * L + 0.03 * rng.normal(size=T), 0, 1),
         CR=np.clip(0.05 + 0.10 * mood + 0.30 * L, 0, 1), BU_L=0.6 * L, RHY=0.5 * L, BRE=0.3 * L,
         FR=np.clip(0.25 + 0.05 * mood + 0.25 * L + 0.03 * rng.normal(size=T), 0, 1),
         JO=np.clip(0.05 + 0.40 * L + 0.03 * rng.normal(size=T), 0, 1), HP=0.15 * L + 0.02 * rng.normal(size=T))
GROUP = ["LP", "CR", "BU_L", "RHY", "BRE"]
W = {"2 s": int(2 * fs), "10 s": int(10 * fs), "1 min": int(60 * fs)}


def win_slopes(u, y, lagmax_s=3.0):
    """slope of the rendered agent channel on his channel, window means, best lag in [0, lagmax]"""
    out = {}
    for lab, n in W.items():
        best = -9
        for lg in range(0, int(lagmax_s * fs) + 1, int(0.25 * fs)):
            best = max(best, slope(means(u[: T - lg], n), means(y[lg:], n)))
        out[lab] = best
    return out


SIGNED = ("FR", "EN", "HP")


def rendered(k, y):
    if k in SIGNED: return y                       # signed / contour channels: no clipping at rest
    r = REST.get(k, 0.0); return np.clip(r + y, 0, 1) - r


# ======================================================== K1: cross-channel routes inside the fast wrap
print("=== K1: the fast wrap's per-channel cap ignores cross-channel paths inside S_f (co-moving partner channels)")
Hi = {k: hp(np.sqrt(KAP[k]) * U[k], 4.0, fs) for k in U}                     # H_i(K^1/2 P u), no feedback on j != k


def cross_route(k, srcs):
    """S_f = gamma * e_k v^T (v = normalised K^1/2 1 over srcs, k not in srcs), delayed 0.45 s: ||S_f|| = gamma, so the
    design's sector (W1, W2) holds; output only on channel k, read from his co-moving channels"""
    v = np.array([np.sqrt(KAP[j]) for j in srcs]); v /= np.linalg.norm(v)
    z = GF * sum(v[i] * Hi[j] for i, j in enumerate(srcs))
    s = hp(delay(z, d), 4.0, fs)
    return 2 * np.sqrt(KAP[k]) * s


for k in ("LP", "BU_L", "CR", "BRE", "JO", "HP", "FR"):
    srcs = [j for j in GROUP if j != k]
    y = cross_route(k, srcs)
    # sector check (W1) on this run: <y, u> <= b <u, K u>, using every partner channel
    lhs = float(y @ U[k]); rhs = B_W1 * sum(KAP[j] * float(U[j] @ U[j]) for j in U)
    diag = FASTCAP[k] * hp(delay(U[k], d), 4.0, fs)                           # the design's full-gate diagonal echo
    sd, sx = win_slopes(U[k], rendered(k, diag)), win_slopes(U[k], rendered(k, y))
    print(f"   agent {k:4s} <- his {'+'.join(srcs)}: W1 lhs/rhs = {lhs / rhs:+.3f} (<= 1 holds); ceiling {CEIL[k]:.2f}")
    print(f"      design's diagonal echo at the cap: slope 2 s {sd['2 s']:+.3f}, 10 s {sd['10 s']:+.3f}, 1 min {sd['1 min']:+.3f}")
    print(f"      cross route, same sector:          slope 2 s {sx['2 s']:+.3f}, 10 s {sx['10 s']:+.3f}, 1 min {sx['1 min']:+.3f}"
          f"  ({sx['2 s'] / CEIL[k]:.1f}x c_k at 2 s, {sx['1 min'] / CEIL[k]:.2f}x c_k pooled 1 min)")
# a sadness -> joy route inside the fast block (rule J says 'anywhere'; the REN has no sign structure)
BIu = np.clip(0.05 + 0.5 * laughs(0.5 + 2 * mood, T, fs, dur=6.0), 0, 1)
yJ = 2 * np.sqrt(KAP["LP"]) * hp(delay(GF * hp(np.sqrt(KAP["BI"]) * BIu, 4.0, fs), d), 4.0, fs)
print(f"   rule J inside the fast block: agent LP <- his BI at the sector limit: 2-s slope {win_slopes(BIu, rendered('LP', yJ))['2 s']:+.3f}"
      f" (his BI onset 0.5 -> agent smile +{0.5 * 2 * GF * np.sqrt(KAP['LP'] * KAP['BI']):.3f} within 0.5 s)")

# all routes together on LP, with the cross fast route instead of the diagonal echo (H9's recipe otherwise)
TAU_M = [20.0, 120.0, 1200.0, 10800.0]; F_M = [0.0, 0.7, 0.2, 0.1]
for k in ("LP", "CR", "BRE"):
    sc, sx_, sa = SH[k]; ck = CEIL[k]; uk = U[k]
    yC = sum(F_M[m] * sc * ck * lp(uk - uk.mean(), TAU_M[m], fs) for m in range(4))
    yX = sx_ * ck * lp(U["CR"] if k != "CR" else U["LP"], 120.0, fs)
    yA = sa * ck * (lp(uk, 20.0, fs) - lp(uk, 90.0, fs))
    tot = rendered(k, yC + yX + yA + cross_route(k, [j for j in GROUP if j != k]))
    st = win_slopes(uk, tot)
    print(f"   {k}, every route at its cap with the cross fast route: 2 s {st['2 s']:+.3f}, 10 s {st['10 s']:+.3f}, "
          f"1 min {st['1 min']:+.3f} (ceiling {ck:.2f}; = {st['1 min'] / ck:.2f} c_k pooled 1 min)")

# ======================================================== K2: energy-for-area spreading by an admissible nonlinear S_f
print("=== K2: rectification allowance r_k is measured on the linear echo only; an admissible nonlinear S_f spreads a burst")
k = "BU_L"; kap = KAP[k]
car = np.sign(hp(lp(rng.normal(size=T), 0.08, fs), 0.5, fs))               # his head micro-motion (always present), sign only
car[car == 0] = 1


def run_loop(mode, D=12.0):
    """the loop w = K^1/2 u - s_f, s_f = H_o S H_i(w), S strictly causal (0.45 s); stepped sample by sample"""
    a_i = 1 - np.exp(-1 / (4.0 * fs)); a_D = 1 - np.exp(-1 / (D * fs))
    li = lo = env = 0.0; s = np.zeros(T); what = np.zeros(T); z = np.zeros(T); v = np.sqrt(kap) * U[k]
    for t in range(T):
        w = v[t] - s[t - 1] if t else v[t]                                       # feedback of the block's output
        li += a_i * (w - li); what[t] = w - li                                     # H_i
        zt_in = what[t - d] if t >= d else 0.0
        if mode == "linear": zt = GF * zt_in
        else:
            env += a_D * (zt_in * zt_in - env); zt = GF * np.sqrt(max(env, 0.0)) * car[t]
        z[t] = zt; lo += a_i * (zt - lo); s[t] = zt - lo                           # H_o
    gain_ok = np.all(np.cumsum(z ** 2) <= GF ** 2 * np.cumsum(what ** 2) + 1e-9)
    return 2 * np.sqrt(kap) * s, gain_ok


Tsub = T
for mode in ("linear", "spread"):
    y, ok = run_loop(mode)
    sl = win_slopes(U[k], rendered(k, y), lagmax_s=0.0)
    print(f"   {mode:6s} S_f: ||S_f(w)||_T <= gamma ||w||_T on every truncation: {ok}; rendered BU_L pooled 1-min slope "
          f"{sl['1 min']:+.3f} = {sl['1 min'] / CEIL[k]:.2f} c_k (design r_k 0.867 c_k; channel total with r_k: 0.996 c_k)")
    if mode == "spread": r_sp = sl["1 min"] / CEIL[k]
    else: r_lin = sl["1 min"] / CEIL[k]
sc, sx_, sa = SH[k]
print(f"   BU_L total with the spreading S_f: {sc * 1.091 + sx_ + 0.636 * sa + r_sp:.2f} c_k (bound claimed for every parameter value: 0.996)")

# ======================================================== K3: the likelihood-trained fast gain with a partner who mirrors
print("=== K3: fast gain fitted nightly by the likelihood of own fast dynamics; partner mirrors the agent at 0.45 s")
fs3 = 10.0; T3 = int(4 * 3600 * fs3); d3 = int(0.45 * fs3)


def env_seq(T, rate_min, fs):
    """the agent's own word-driven smiles: rise 0.4 s, apex to 1.5 s, decay 3 s (Pi_0 envelope), amplitude 0.3-0.6"""
    imp = np.zeros(T); t = 0
    while t < T:
        t += int(rng.exponential(60 / rate_min) * fs) + 1
        if t < T: imp[t] = rng.uniform(0.3, 0.6)
    tt = np.arange(int(15 * fs)) / fs
    kern = np.where(tt < 0.4, tt / 0.4, np.where(tt < 1.5, 1.0, np.exp(-(tt - 1.5) / 3.0)))
    return np.convolve(imp, kern)[:T]


e_own = 0.55 * env_seq(T3, 3.0, fs3)
cap = FASTCAP["LP"]; g0 = 0.65 * cap; lam = 0.5
for mu, his_own in ((0.0, 1.0), (0.3, 1.0), (0.5, 0.5), (0.8, 0.3)):
    n_his = his_own * 0.55 * env_seq(T3, 3.0, fs3)
    for target in ("rendered", "residual"):
        g = g0
        for night in range(60):
            y = np.zeros(T3); u = np.zeros(T3)
            # stepped at the echo lag (both delays 0.45 s): u(t) = mu y(t - d) + his own; y(t) = e_own + g HP(u)(t - d)
            yf = np.zeros(T3); lo = 0.0; a4 = 1 - np.exp(-1 / (4 * fs3)); uh = np.zeros(T3)
            for t in range(T3):
                u[t] = (mu * y[t - d3] if t >= d3 else 0.0) + n_his[t]
                lo += a4 * (u[t] - lo); uh[t] = u[t] - lo
                yf[t] = g * (uh[t - d3] if t >= d3 else 0.0); y[t] = e_own[t] + yf[t]
            x = delay(uh, d3); tgt = hp(y if target == "rendered" else e_own, 4.0, fs3)
            beta = float(x @ tgt / (x @ x))
            g = float(np.clip((beta + lam * g0) / (1 + lam), -0.49, cap))
            if night == 59: break
        print(f"   mirror gain mu {mu:.1f} (his own expressivity {his_own:.1f}), target = own {target:8s}: fast LP gain after 60 nights "
              f"{g:+.3f} (innate {g0:.3f}, cap {cap:.3f})")

# ======================================================== K4: the fast block learns the common cause (his laugh, own play laugh)
print("=== K4: likelihood of own fast dynamics learns his laughter as a predictor of the agent's own word-driven laugh")
# the agent's play-surprise laugh fires 0.6 s after his utterance end; he laughs at the end of his own joke
fs4 = 10.0; T4 = int(4 * 3600 * fs4)
ends = np.sort(rng.choice(T4 - 200, 900, replace=False))
his = np.zeros(T4); own = np.zeros(T4)
tt = np.arange(int(4 * fs4)) / fs4; kl = np.where(tt < 1.5, 1.0, np.exp(-(tt - 1.5) / 1.0))
for e_ in ends:
    joke = rng.random() < 0.5
    if joke:                                             # punchline: he laughs from -0.5 s, the agent's reflex laugh at +0.6 s
        a = rng.uniform(0.4, 0.8); s0 = e_ - 5; his[s0:s0 + len(kl)] += a * kl[: T4 - s0]
        s1 = e_ + 6; own[s1:s1 + len(kl)] += 0.40 * kl[: T4 - s1]
X = np.stack([delay(hp(his, 4.0, fs4), int(0.45 * fs4))], 1)
Y = hp(own, 4.0, fs4)
beta = float(np.linalg.lstsq(X, Y, rcond=None)[0][0])
print(f"   least-squares gain of own fast laugh on his laugh (0.45-s path): {beta:+.3f} per unit (cap on BU_L {FASTCAP['BU_L']:.3f}); "
      f"the fit pushes the gate to its cap (1) and, across channels, toward K1's cross route")

# ======================================================== K5: the word-need reader with a partner who mirrors the agent's concern
print("=== K5: word-need reader fitted nightly to Pi~_0 of his face over 20 s after his words; he mirrors the agent's concern face")
RD_CH = ["LP", "CR", "BI", "LD", "UL", "BO", "FR", "EN", "RT", "HG", "LAT", "BRE"]; RD_L = ["rel", "dis", "hd", "lowE", "act"]
PI0 = {"rel": dict(LP=.55, CR=.45, FR=.35, EN=.25), "dis": dict(BI=.45, LD=.35, FR=-.20, EN=-.15),
       "hd": dict(BI=.25, LD=.20, LP=-.25, HG=.30, EN=-.20, LAT=.15), "lowE": dict(UL=-.30, FR=-.25, EN=-.25, RT=-.15),
       "act": dict(UL=.20, BO=.15, FR=.15, RT=.15, BRE=.10)}
M0 = np.array([[PI0[l].get(c, 0.0) for l in RD_L] for c in RD_CH])


def read(face):
    rows = [i for i, c in enumerate(RD_CH) if c not in ("FR", "EN", "RT", "LAT")]
    x = np.array([face.get(RD_CH[i], 0.0) for i in rows]); Mm = M0[rows]
    z = np.linalg.solve(Mm.T @ Mm + 0.05 * np.eye(5), Mm.T @ x); z = dict(zip(RD_L, z))
    return float(np.clip(z["dis"] + z["hd"], 0, 1))


def Dp(V): return 0.8 * max(V - 0.05, 0) ** 2


def agent_face_20s(V):
    """mean of the agent's own display over 20 s after a word with decoded V: word concern (C_L tau 40 s, c_L = C/(C+0.1),
    BI .25) and the distress event (a_d = S/(S+0.02), envelope; BI .45, LD .35)"""
    t = np.arange(0, 20, 0.05); D = Dp(V); C = D * (1 - np.exp(-t / 40)); cl = C / (C + 0.1)
    ad = D / (D + 0.02) if D > 0 else 0.0
    e = np.where(t < 0.4, t / 0.4, np.where(t < 1.5, 1.0, np.exp(-(t - 1.5) / 3.0)))
    return dict(BI=float((0.25 * cl + 0.45 * ad * e).mean()), LD=float((0.35 * ad * e).mean()))


print(f"   Pi~_0 reads his brow alone: BI 0.05 -> V {read(dict(BI=.05)):.2f}; 0.10 -> {read(dict(BI=.10)):.2f}; 0.20 -> {read(dict(BI=.20)):.2f}")
for Vtrue in (0.15, 0.25, 0.35):
    row = []
    for mu in (0.0, 0.3, 0.5, 0.7):
        V = 0.0
        for night in range(200):
            af = agent_face_20s(V); base = read(dict(BI=0.5 * Vtrue, LD=0.4 * Vtrue))   # his own face for this word
            hisf = dict(BI=0.5 * Vtrue + mu * af["BI"], LD=0.4 * Vtrue + mu * af["LD"])
            V += 0.3 * (read(hisf) - V)
        af = agent_face_20s(V); row.append((mu, base, V, af["BI"]))
    print(f"   word whose true face reads V {row[0][1]:.2f}: " + "; ".join(
        f"mu {m:.1f} -> decoded V {v:.2f}, agent BI (20-s mean) {b:.3f}" for m, _, v, b in row))

# ======================================================== K6: the baseline b_id: lagged and held copy across sessions
print("=== K6: cone centred at b_id (tau_b 6 sessions): lagged session copy, and b reaching the face through -omega b")
nS = 3000; g = SH["LP"][0] * CEIL["LP"]
for lab, ubar in (("session-white mood", 0.3 + 0.1 * rng.normal(size=nS)),
                  ("monthly blocks", 0.3 + 0.1 * np.repeat(rng.normal(size=nS // 30 + 1), 30)[:nS])):
    for om in (+1.0, -1.0):
        b = 0.3; y = []
        for s in range(nS): y.append(om * g * (ubar[s] - b)); b += (ubar[s] - b) / 6.0
        y = np.array(y)
        lag = {k_: slope(ubar[: nS - k_], y[k_:]) for k_ in (0, 1, 3, 6, 12)}
        print(f"   {lab:18s} omega {om:+.0f}: session slope at lag 0/1/3/6/12 sessions " +
              ", ".join(f"{lag[k_]:+.3f}" for k_ in lag) + f"  (s_C c_LP {g:.3f}, ceiling 0.35)")

# ======================================================== K7: whole-face direction under K1's construction
print("=== K7: whole face: the laughing-face direction under the cross route")
e = np.array([1.0] * 5); kv = np.array([KAP[j] for j in GROUP])
# best per-direction in-phase fraction allowed by W1 for the laughing direction (all five channels equal)
print(f"   W1 bound on the laughing-face direction: b * sum(kappa)/n = {B_W1 * kv.sum() / 5:.3f} (design's H0 quadratic-form bound "
      f"{sum(CEIL[j] for j in GROUP) / 5:.3f}); the cross route spends it on one channel")
