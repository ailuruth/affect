"""Checks for design-cayley-ledger.md, revision 8.1 (K1-K5): the narrow fixes to revision 8 only.

Checks of the design's own rules on constructed partners; NOT evidence about behaviour, people or data (brief.md: no toy worlds).
The revision-8 engine is loaded unchanged from ../design-g8/checks.py up to its definitions (Agent8 and helpers; its J31-J39 result
loops are skipped), exactly as the revision-8 critics' load8.py and scen.py do; that executes revisions 5-7 unchanged. Revision 8.1
changes only the concern posture's contingency test and its squint reading, in the class Agent81 below (a copy of Agent8.step with
those two parts changed). Revision 8 rows use Agent8 itself.
K1  the routes critic's lagged answering partner (critique 8, P1 = J33 with lags 0-90 s, mu 1.0 and 0.6), plus a genuine-then-answering
    partner (lags up to 240 s) and a noisy one;
K2  specificity: the routes critic's P2 (24 runs) and the agent critic's B3 (12 runs) of genuine fluctuating sadness; ablation with
    revision 8's 8-s probe kept;
K3  J33 (mirrors, answering concern, fading sadness) and J34 (steady faces, every code) re-run;
K4  the agent critic's B2 (grief + squint looking at the agent) and J35 (anger, anger with heavy breathing, concentration), rev 8 vs 8.1;
K5  D_s never reads his breath sound.
Run:  python3 -I checks.py > out.txt   (numpy, scipy; the engine load took about 4 min on an idle machine, 20-29 min under load;
      the checks themselves about 4 min)
"""
import io, os, time, contextlib
import numpy as np
_T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
P8SRC = os.path.join(HERE, "..", "design-g8", "checks.py")
_L8 = open(P8SRC).read().split("\n")
_cut = next(i for i, s in enumerate(_L8) if s.startswith("# =========================================================== J31"))
_src8 = "\n".join(_L8[:_cut] + ["'''", "exec(compile(BODY, 'checks_g8', 'exec'), G7)"])
G8 = {"__name__": "g8", "__file__": P8SRC}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src8, "checks_g8_defs", "exec"), G8)
G = G8["G7"]
print(f"[loaded the revision-8 engine in {time.time() - _T0:.0f} s]", flush=True)
_T1 = time.time()
BODY81 = r'''
import numpy as np
SQ_CH = ("BL", "LPR")
class Agent81(Agent8):
    """revision 8.1. Defaults are the design's values.
    cap      : face-only hold cap (s of face-only hold, words or sobs reset it); at the cap the look is withdrawn for a test lapse
    cap_len  : first lapse (s); len_grow/len_max: later lapses (60 -> 120 s); cap_grow: the cap doubles after a passed test (4, 8, 16 min)
    cap_thr  : release if his Vlin over the lapse's last cap_win s < cap_thr x its mean over the cap_pre s before; else the look returns
    cap_depth: target factor during the lapse (0 = withdrawn)
    iv       : revision 8's 8-s half-amplitude probe every iv s of face-only hold (1e9 = removed, as in 8.1; 180 = kept, ablation)
    sq       : 'drop' (8.1: while the glare is up, BL and LPR are taken to his rest in what the posture reads) or 'all' (revision 8)"""
    def __init__(s, *a, sq="drop", cap=240.0, cap_len=60.0, cap_depth=0.0, cap_thr=0.7, cap_win=20.0, cap_pre=30.0, cap_grow=2.0, iv=1e9, len_grow=2.0, len_max=120.0, **kw):
        super().__init__(*a, **kw)
        s.sq, s.cap, s.cap_len, s.cap_depth, s.cap_thr, s.cap_win, s.cap_pre, s.cap_grow, s.iv8 = sq, cap, cap_len, cap_depth, cap_thr, cap_win, cap_pre, cap_grow, iv
        s.len_grow, s.len_max = len_grow, len_max; s.len_now = cap_len; s.cap_now = cap; s.Lbuf20 = []; s.fo_tot = 0.0; s.Ldur = []; s.pkind = None

    def step(s, t, face, ev):
        if not hasattr(s, "play_la"): s.play_la = []
        G5["read"] = lambda f_, voiced=True: s.pp.read(f_, voiced)
        for k in ("BL", "LPR", "CHR"): s.f20[k] += (face.get(k, s.pp.base.get(k, 0.0)) - s.f20[k]) * DT / 20
        if "own" in ev: s.LVo = LAMV(Z6[ev["own"]])
        y = Agent5.step(s, t, face, ev)
        for k in ("LP", "CR", "BI", "LD", "UL", "BO", "BL", "LPR", "CHR", "BU_S"):
            b_ = s.pp.base.get(k, 0.0); s.f3[k] = s.f3.get(k, b_) + (face.get(k, b_) - s.f3.get(k, b_)) * DT / 3.0
        s.br3 += (face.get("BR", 0.0) - s.br3) * DT / 3.0
        s.gl3 = getattr(s, 'gl3', 0.0) + (face.get('BL', 0.0) * face.get('LT', 0.0) * face.get('gat', 0.0) - getattr(s, 'gl3', 0.0)) * DT / 3.0
        sob = Vc(min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        wg = float(np.clip(s.gl3 / GLARE_SAT, 0, 1))
        if s.sq == "drop":                       # 8.1: while the glare is up, BL and LPR are taken toward his rest in what the posture reads
            f3r = dict(s.f3)
            for k in SQ_CH:
                b_ = s.pp.base.get(k, 0.0); f3r[k] = b_ + (1.0 - wg) * (s.f3.get(k, b_) - b_)
            rp = posture_read(s.pp, f3r, False); Ab = v_breath(s.pp, s.br3); Lf = load_p(rp["V"], Ab)
        else:
            rp = posture_read(s.pp, s.f3, False); Ab = v_breath(s.pp, s.br3); Lf = load_p(rp["V"], Ab) * (1.0 - wg)
        s.Lface = Lf
        M = max(Lf, s.Cl, sob)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            faceonly = (s.Cl < 0.02 and sob < 0.02 and Lf >= 0.02)
            if s.probe_t is None:
                s.Lbuf = (s.Lbuf + [rp["Vlin"]])[-int(3 / DT):]
                s.Lbuf20 = (s.Lbuf20 + [rp["Vlin"]])[-int(s.cap_pre / DT):]
                s.fo = s.fo + DT if faceonly else 0.0
                s.fo_tot = s.fo_tot + DT if faceonly else 0.0
                if not faceonly and (s.Cl >= 0.02 or sob >= 0.02): s.fo_tot = 0.0; s.cap_now = s.cap
                if s.use_probe and s.cap_now is not None and s.fo_tot >= s.cap_now:      # 8.1: the face-only cap
                    s.probe_t = t; s.pkind = "cap"; s.plen = s.len_now; s.Ldur = []; s.Lpre = float(np.mean(s.Lbuf20))
                elif s.use_probe and s.fo >= s.iv8:                                         # revision 8's 8-s probe, unchanged
                    s.probe_t = t; s.pkind = "probe"; s.plen = PROBE_LEN; s.Ldur = []; s.Lpre = float(np.mean(s.Lbuf))
            else:
                if s.Cl >= 0.02 or sob >= 0.02:                                             # words or sobs renew it: test ends, held
                    s.probes.append((s.probe_t, round(s.Lpre, 3), None, "ended by words/sobs", s.pkind, t - s.probe_t)); s.probe_t = None; s.fo = 0.0; s.fo_tot = 0.0; s.cap_now = s.cap
                else:
                    w_ = 4.0 if s.pkind == "probe" else s.cap_win
                    if t - s.probe_t >= s.plen - w_: s.Ldur.append(rp["Vlin"])
                    if t - s.probe_t >= s.plen:
                        thr = PROBE_FOLLOW if s.pkind == "probe" else s.cap_thr
                        follow = np.mean(s.Ldur) < thr * s.Lpre
                        s.probes.append((s.probe_t, round(s.Lpre, 3), round(float(np.mean(s.Ldur)), 3), ("followed: release" if follow else "held"), s.pkind, s.plen))
                        s.probe_t = None; s.fo = 0.0
                        if s.pkind == "cap": s.fo_tot = 0.0; s.cap_now = s.cap_now * s.cap_grow; s.len_now = min(s.len_max, s.len_now * s.len_grow)
                        if follow:
                            s.on = False; s.last_off = t; s.offs.append((t, s.pkind)); s.quiet = True; s.qmin = Lf
            if s.on and s.below >= REL8:
                s.on = False; s.last_off = t; s.offs.append((t, "release")); s.probe_t = None
            if not s.on: s.below = s.fo = 0.0; s.fo_tot = 0.0; s.cap_now = s.cap; s.len_now = s.cap_len
        else:
            fe = Lf
            if s.quiet:
                s.qmin = min(s.qmin, Lf); fe = Lf - s.qmin
                if Lf < 0.02: s.quiet = False
            Con = max(fe, sob)
            need = DWELL_SENS if (s.sens and t - s.last_off < SENS_S) else DWELL
            s.dw = s.dw + DT if Con >= 0.05 else 0.0
            if s.dw >= need - 1e-9 and s.om.get("sym", 0) >= 0:
                s.on = True; s.dw = 0.0; s.onsets.append(t); s.fo = 0.0; s.fo_tot = 0.0; s.cap_now = s.cap; s.probe_iv = PROBE0
        tgt = A_MIN + (1 - A_MIN) * float(np.clip((M - 0.05) / A_SPAN8, 0, 1)) if s.on else 0.0
        if s.probe_t is not None: tgt *= (PROBE_DEPTH if s.pkind == 'probe' else s.cap_depth)
        s.a = min(tgt, s.a + DT / 1.5) if tgt > s.a else tgt + (s.a - tgt) * np.exp(-DT / 4.0)
        s.arec = max(s.a, s.arec * np.exp(-DT / 60.0))
        s.w = float(np.clip(s.w + (0.5 - s.w) * DT / 5.0 + 0.1 * np.sqrt(DT) * s.wr.normal(), 0, 1))
        shown = s.a * (0.9 + 0.1 * s.w)
        if s.use_Ds:
            s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), posture_read(s.pp, {k: v for k, v in s.f3.items() if k not in MASK}, False)["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        for k, v in P7.items():
            if k in y: y[k] += v * shown
        s.post = shown; y["post"] = shown; y["Lp"] = Lf
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        gt = s.gfn(s.xg)
        s.gate = gt if gt < s.gate else s.gate + (gt - s.gate) * min(1.0, DT / GATE_TAU)
        y["gate"] = s.gate
        return y
NOV = ("FR", "EN", "RT")
CODES = (("operator", PEOPLE6["agent-like"][1]), ("quiet 0.3", PEOPLE6["low-expressive"][1]), ("different channels", PEOPLE6["different channels"][1]))
def run_answer(mk, pp, mu, tau, dur=900, sad_until=40.0, noise=0.0, seed=0):
    ag = mk(pp); st = {"m": 0.0, "n": 0.0}; r_ = np.random.default_rng(seed)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}
    def face(t, ag=ag):
        a = ag.post
        st["m"] = a if tau == 0 else st["m"] + (a - st["m"]) * (1 - np.exp(-DT / tau))
        if noise: st["n"] += -st["n"] * DT / 10 + noise * np.sqrt(2 * DT / 10) * r_.normal()
        if t < sad_until: return dict(sad)
        return {k: v for k, v in pp.code(V=float(np.clip(mu * st["m"] + st["n"], 0, 1))).items() if k not in NOV}
    rec = run6(ag, dur, face, {})
    late = [r for r in rec if r["t"] > dur - 120]
    return ag, rec, float(np.mean([r["post"] for r in late])), float(np.mean([r["BI"] for r in late]))
def run_p2(mk, pp, sdv, seed, dur=900):
    r_ = np.random.default_rng(100 + seed); st = {"v": 0.0, "t": -1}
    def face(t):
        if t != st["t"]: st["v"] += -st["v"] * DT / 10 + sdv * np.sqrt(2 * DT / 10) * r_.normal(); st["t"] = t
        return {k: v for k, v in pp.code(V=float(np.clip(0.6 + st["v"], 0, 1))).items() if k not in NOV}
    ag = mk(pp); rec = run6(ag, dur, face, {}); return ag, rec
def run_b3(mk, pp, sd, seed, dur=600):
    r_ = np.random.default_rng(seed); n = int(dur / DT); v = np.empty(n); x = 0.0; a = np.exp(-DT / 5.0)
    for i in range(n): x = a * x + np.sqrt(1 - a * a) * sd * r_.normal(); v[i] = np.clip(0.6 + x, 0, 1)
    faces = [with_breath(pp, {k: val for k, val in pp.code(V=v[i], Tr=.2).items() if k not in NOV}, 0.0) for i in range(n)]
    ag = mk(pp); rec = run6(ag, dur, lambda t: faces[min(int(round(t / DT)), n - 1)], {}); return ag, rec

def rel_kind(ag): return [o for o in ag.offs if o[1] in ("probe", "cap")]
def tests_line(ag): return [(p[0], p[4], p[3][:4], round(p[2] / p[1], 2) if p[2] else None) for p in ag.probes]
MK81 = lambda pp: Agent81(person=pp)
MK8 = lambda pp: Agent8(person=pp)
OKS = {}

# =========================================================== K1: concern answered with a lag (routes critique 8, P1 = J33 with lags)
print("=== K1: concern answered in his own code with a lag tau (his genuine sadness V .8 ends at 40 s; then his face = his code at V = mu x lp_tau(posture)); 15 min")
K1 = {}
for lab, pp in CODES:
    for mu in (1.0, 0.6):
        for tau in (0, 5, 15, 30, 60, 90):
            r8 = run_answer(MK8, pp, mu, tau); r81 = run_answer(MK81, pp, mu, tau); K1[(lab, mu, tau)] = (r8, r81)
            print(f"   {lab:18s} mu {mu} tau {tau:2d} s | rev 8: offs {r8[0].offs[:1]}, last 2 min posture {r8[2]:.2f}, BI {r8[3]:+.3f} | "
                  f"8.1: offs {r81[0].offs[:1]}, tests {tests_line(r81[0])[:2]}, last 2 min posture {r81[2]:.2f}, BI {r81[3]:+.3f}", flush=True)
for lab, pp in CODES:
    for tau in (5, 30, 90):
        r81 = run_answer(MK81, pp, 1.0, tau, noise=0.10, seed=tau); K1[(lab, "noisy", tau)] = (None, r81)
        print(f"   {lab:18s} mu 1.0 tau {tau:2d} s + his own OU noise (SD .10, 10 s): 8.1 offs {r81[0].offs[:2]}, last 2 min posture {r81[2]:.2f}")
print("   genuine sadness for 10 min, THEN answering with a lag (30 min run; the cap has already passed one test):")
for lab, pp in (CODES[0], CODES[2]):
    for tau in (5, 30, 90, 180, 240):
        r81 = run_answer(MK81, pp, 1.0, tau, dur=1800, sad_until=600.0); K1[(lab, "late", tau)] = (None, r81)
        print(f"   {lab:18s} tau {tau:3d} s: 8.1 offs {r81[0].offs[:1]}, tests {tests_line(r81[0])[:3]}, last 2 min posture {r81[2]:.2f}", flush=True)
OKS["K1"] = all(v[1][2] < 0.05 and v[1][0].offs for k, v in K1.items() if k[1] != "noisy") and max(v[1][0].offs[0][0] for k, v in K1.items() if k[1] in (1.0, 0.6)) <= 310
print("   (the noisy rows are a robustness probe beyond the critic's partner and are not in the PASS criterion; see the text, section 2.10)")
print(f"K1 {'PASS' if OKS['K1'] else 'FAIL'}: every lagged answer (tau 0-90 s; 0-240 s after a genuine phase) ends the posture; latest end "
      f"{max(v[1][0].offs[0][0] for k, v in K1.items() if k[1] == 1.0):.1f} s for sadness ending at 40 s (rev 8: held 15 min at tau >= 5 s, mu 1.0)")

# =========================================================== K2: specificity on genuine fluctuating sadness
print("=== K2: genuine steady sadness with natural fluctuation: routes critique 8 P2 (V .6 + OU, SD .05/.10, tau 10 s, 15 min, 4 seeds x 3 codes) and agent critique 8 B3 (AR(1), SD .10/.20, tau 5 s, 10 min)")
K2 = {}
for nm, mk in (("rev 8", MK8), ("8.1", MK81), ("8.1 + rev 8's 8-s probe kept (ablation)", lambda pp: Agent81(person=pp, iv=180.0))):
    n_rel = 0; rs = []; lap = []
    for lab, pp in CODES:
        for sdv in (0.05, 0.10):
            for seed in range(4):
                ag, rec = run_p2(mk, pp, sdv, seed); n_rel += bool(rel_kind(ag)); lap.append(np.mean([r["post"] < 0.05 for r in rec if r["t"] > 10]))
                rs += [p[2] / p[1] for p in ag.probes if len(p) > 4 and p[4] == "cap" and p[2]]
    m_rel = 0; rs3 = []; lap3 = []; back = []
    for lab, pp in CODES[:2]:
        for sd in (0.10, 0.20):
            for seed in (1, 2, 3):
                ag, rec = run_b3(mk, pp, sd, seed); m_rel += bool(rel_kind(ag)); lap3.append(np.mean([r["post"] < 0.05 for r in rec if r["t"] >= 10]))
                rs3 += [p[2] / p[1] for p in ag.probes if len(p) > 4 and p[4] == "cap" and p[2]]
                back += [min([o for o in ag.onsets if o > t_], default=np.inf) - t_ for t_, w in rel_kind(ag)]
    K2[nm] = (n_rel, m_rel)
    print(f"   {nm:42s} P2: released by a test in {n_rel} of 24 (cap-test ratios min {min(rs) if rs else float('nan'):.2f}, n {len(rs)}); posture < 0.05 for "
          f"{100 * np.mean(lap):.1f}% of the time (max {100 * max(lap):.1f}%) | B3: released in {m_rel} of 12 (ratios min {min(rs3) if rs3 else float('nan'):.2f}), "
          f"back on after {[round(b, 1) for b in back]} s; posture < 0.05 for max {100 * max(lap3):.1f}%", flush=True)
OKS["K2"] = K2["8.1"][0] == 0
print(f"K2 {'PASS' if OKS['K2'] else 'FAIL'}: no genuine fluctuating sadness of P2 is released (8.1: {K2['8.1'][0]} of 24)")

# =========================================================== K3: J33 and J34 re-run with the 8.1 posture
# J33's partners, copied verbatim from ../design-g8/checks.py (its J33 section is not executed by the loader)
def mir8(mu, tau=None):
    def f(a_c, pp, st):
        if tau: st["m"] += (a_c - st["m"]) * DT / tau; a_c = st["m"]
        return {k: mu * v * a_c * (pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) if mu < 0 else 1.0) for k, v in P7.items() if k in ("BI", "BO", "LP")}
    return f
own8 = lambda a_c, pp, st: {k: v * a_c * pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) for k, v in P7.items() if k in ("BI", "BO", "LP")}
aww8 = lambda Vr: (lambda a_c, pp, st: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in ("FR", "EN", "RT")})
J33 = {}
cases8 = [("P0 agent-like, raw mirror mu 1.0", PEOPLE6["agent-like"][1], mir8(1.0), None), ("P1 agent-like, mirror at his own scale", PEOPLE6["agent-like"][1], own8, None),
          ("P2b agent-like, mirror mu 3.0", PEOPLE6["agent-like"][1], mir8(3.0), None), ("P5 quiet, raw mirror mu 1.0", PEOPLE6["low-expressive"][1], mir8(1.0), None),
          ("P5 quiet, raw mirror mu 3.0", PEOPLE6["low-expressive"][1], mir8(3.0), None), ("P5c sigma_id at floor 0.25, mu 2.0", low_sd(0.25), mir8(2.0), None),
          ("S1 slow mirror tau 90 s, quiet", PEOPLE6["low-expressive"][1], mir8(1.0, 90), None), ("S1 slow mirror tau 240 s, floor spread", low_sd(0.25), mir8(1.0, 240), None),
          ("P3 agent-like, mild 'aww' in his own code (V 0.3 x posture)", PEOPLE6["agent-like"][1], aww8(0.3), None),
          ("P4 different channels, mild 'aww' (V 0.3 x posture)", PEOPLE6["different channels"][1], aww8(0.3), None),
          ("P4b different channels, strong concern in his own code (V 1.0 x posture)", PEOPLE6["different channels"][1], aww8(1.0), None),
          ("P4c agent-like, strong concern in his own code (V 1.0 x posture)", PEOPLE6["agent-like"][1], aww8(1.0), None),
          ("P4d quiet, strong concern in his own code (V 1.0 x posture)", PEOPLE6["low-expressive"][1], aww8(1.0), None),
          ("Q3 quiet, genuine sadness fading over 10 min + raw mirror mu 1.0", PEOPLE6["low-expressive"][1], mir8(1.0), 0.8),
          ("Q3 floor spread, genuine sadness fading + strong 'aww' on top", low_sd(0.25), aww8(1.0), 0.8)]
print("=== K3: J33 (mirrors, answering concern at tau 0, fading sadness) and J34 (steady faces, every code), 8.1")
K3 = {}
def run_mirror81(pp, resp, dur=900, sad_until=40.0, fade=None):
    ag = Agent81(person=pp)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in pp.code().items() if k not in NOV}; st = {"m": 0.0}
    def face(t, ag=ag):
        if fade is not None: f = {k: v for k, v in pp.code(V=max(0.0, fade * (1 - t / 600.0))).items() if k not in NOV}
        else: f = dict(sad if t < sad_until else neu)
        if fade is not None or t >= sad_until:
            for k, v in resp(ag.post, pp, st).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, dur, face, {}); late = [r for r in rec if r["t"] > dur - 120]
    return ag, np.mean([r["BI"] for r in late]), np.mean([r["post"] for r in late])
for lab, pp, resp, fade in cases8:
    ag, aBI, apost = run_mirror81(pp, resp, fade=fade); K3[lab] = (ag.offs, apost)
    print(f"   {lab:74s} offs {ag.offs[:2]}; last 2 min posture {apost:.2f}")
J34r = {}
for kind, pp in (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor 0.25", low_sd(0.25)),
                 ("different channels", PEOPLE6["different channels"][1])):
    for lab, V, A, Tr, sob in (("silent sadness (V .6)", .6, 0, .2, 0), ("grief (V .8)", .8, 0, .2, 0), ("silent panic (V .3, A .9, breathing)", .3, .9, 0, 0),
                               ("crying with sobs (V .9)", .9, 0, .2, .4)):
        f = {k: v for k, v in pp.code(V=V, A=A, Tr=Tr).items() if k not in NOV}; f = with_breath(pp, f, A)
        if sob: f["BU_S"] = sob
        ag = Agent81(person=pp); rec = run6(ag, 900, lambda t, f=f: f, {}); seg = [r for r in rec if r["t"] >= 10]
        t15 = next((r["t"] for r in rec if r["BI"] >= .15), None)
        lapse = [r for r in seg if r["post"] < 0.05]
        win = [(p[0], p[0] + p[5] + 10.0) for p in ag.probes] + ([(ag.probe_t, 1e9)] if ag.probe_t is not None else [])   # incl. a test still running at the end
        outl = [r for r in seg if not any(a_ <= r["t"] < b_ for a_, b_ in win)]
        J34r[(kind, lab)] = (ag.onsets, rel_kind(ag) + [o for o in ag.offs if o[1] == "release"], t15, np.mean([r["BI"] for r in seg]), min(r["BI"] for r in outl), len(lapse) * DT, tests_line(ag))
        print(f"   {kind:22s} {lab:38s}: on at {ag.onsets[0] if ag.onsets else None} s, releases {len(J34r[(kind, lab)][1])}, brow >= 0.15 at {t15} s; "
              f"15-min brow mean {J34r[(kind, lab)][3]:.3f}, min outside the tests (+10 s) {J34r[(kind, lab)][4]:.3f}; withdrawn {J34r[(kind, lab)][5]:.0f} s in all; tests {tests_line(ag)}")
OKS["K3"] = all(v[1] < 0.05 for v in K3.values()) and all(len(v[0]) == 1 and len(v[1]) == 0 and v[2] is not None and v[2] <= 8 for v in J34r.values())
print(f"K3 {'PASS' if OKS['K3'] else 'FAIL'}: every J33 case ends; steady genuine faces keep one onset and no release (the only gaps are the cap's test lapses)")

# =========================================================== K4: the squint fix (agent critique 8 B2) with J35
print("=== K4: a silent tearful or pained face that squints while looking at the agent (B2), and anger / concentration (J35), rev 8 vs 8.1")
op, qu, dc = PEOPLE6["agent-like"][1], PEOPLE6["low-expressive"][1], PEOPLE6["different channels"][1]
def b2(pp, add, V=.8, sob=None):
    f = {k: v for k, v in pp.code(V=V, Tr=.2).items() if k not in NOV}; f.update(add)
    if sob: f["BU_S"] = sob
    return f
K4 = {}
cases = [("operator grief (reference)", op, b2(op, {})),
         ("operator grief + squint BL .4 LT .4, looking at it", op, b2(op, dict(BL=.4, LT=.4, gat=1.0))),
         ("operator grief + strong squint BL .6 LT .6, looking at it", op, b2(op, dict(BL=.6, LT=.6, gat=1.0))),
         ("operator grief + squint, looking away", op, b2(op, dict(BL=.4, LT=.4, gat=0.0))),
         ("quiet grief + squint BL .4 LT .4, looking at it", qu, b2(qu, dict(BL=.4, LT=.4, gat=1.0))),
         ("diff-channel grief (reference)", dc, b2(dc, {})),
         ("diff-channel grief + LT .4, looking at it", dc, b2(dc, dict(LT=.4, gat=1.0))),
         ("operator grief + squint + sobs, looking at it", op, b2(op, dict(BL=.4, LT=.4, gat=1.0), sob=.4))]
for kind, pp in (("operator", op), ("quiet", qu), ("diff-channel", dc)):
    cases += [(f"{kind} anger: BL .6, LT .5, gaze at it, loud", pp, dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05)),
              (f"{kind} anger with heavy breathing (A .8)", pp, with_breath(pp, dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05), .8)),
              (f"{kind} anger + lip press .4", pp, dict(BL=.6, LT=.5, LPR=.4, gat=1.0, EN=.85, LP=.05)),
              (f"{kind} concentrating, silent: BL .35, LPR .15", pp, dict(BL=.35, LPR=.15, LP=.25)),
              (f"{kind} concentrating, squinting at the screen: BL .35, LT .4, LPR .15", pp, dict(BL=.35, LT=.4, LPR=.15, gat=1.0, LP=.25))]
for lab, pp, f in cases:
    res = []
    for mk in (MK8, MK81):
        ag = mk(pp); rec = run6(ag, 180, lambda t, f=f: f, {})
        res.append((max(r["post"] for r in rec), np.mean([r["post"] for r in rec if r["t"] >= 10]), max(r["BI"] for r in rec), ag.onsets[:1]))
    K4[lab] = res
    print(f"   {lab:66s} rev 8: posture max {res[0][0]:.2f}, brow peak {res[0][2]:+.3f} | 8.1: posture max {res[1][0]:.2f} mean {res[1][1]:.2f}, brow peak {res[1][2]:+.3f}, on at {res[1][3]}")
OKS["K4"] = (K4["operator grief + squint BL .4 LT .4, looking at it"][1][0] > 0.9 and K4["operator grief + squint BL .4 LT .4, looking at it"][1][3][0] <= 4.0
             and max(v[1][0] for k, v in K4.items() if "anger" in k or "concentrating" in k) < 0.05)
print(f"K4 {'PASS' if OKS['K4'] else 'FAIL'}: grief + squint at the agent gets the posture (on within 4 s); no anger or concentration case starts it")

# =========================================================== K5: D_s never reads his breath sound (text fix; code check)
ag1 = Agent81(person=op); ag2 = Agent81(person=op); fa = b2(op, {}); fb = dict(fa); fb["BRE"] = 0.3
run6(ag1, 30, lambda t: fa, {}); run6(ag2, 30, lambda t: fb, {})
OKS["K5"] = abs(ag1.Ds - ag2.Ds) < 1e-12
print(f"K5 {'PASS' if OKS['K5'] else 'FAIL'}: D_s with and without his breath sound (BRE .3): {ag1.Ds:.4f} / {ag2.Ds:.4f}")
print("SUMMARY " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in OKS.items()))
'''
exec(compile(BODY81, "checks_g81", "exec"), G)
print(f"[checks ran in {time.time() - _T1:.0f} s]")
