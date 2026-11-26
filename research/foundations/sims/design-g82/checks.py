"""Checks for design-cayley-ledger.md, revision 8.2 (L0-L4): the face-only cap's test is stood down and replaced by a construction.

Checks of the design's own rules on constructed partners; NOT evidence about behaviour, people or data (brief.md: no toy worlds).
The engine and Agent81 are loaded unchanged from ../design-g81/checks.py exactly as the 8.1 checker's ../check-cayley81/check.py
does (its K1-K5 loops are skipped); that executes revisions 5-8 unchanged. Revision 8.2 changes only the posture's face-only rule,
in the class Agent82 below (a copy of Agent81.step with the cap's test lapses removed and the construction added):
  - non-face evidence N = max(C_L (his words, the existing reading), V_c(sobs), V_v (his voice alone, above his resting voice, mean
    over his voiced frames of the last 90 s), the breathing term of L_p); present when N >= 0.02;
  - face-only clock: counts time the look is on while N < 0.02; reset by non-face evidence, or by T_REF without the look (a 20-s
    release does not reset it); at T_MAX = 180 s the look is withdrawn;
  - refractory: for T_REF = 120 s after that, his face counts for nothing in the posture (onset, grade, hold) unless N >= 0.02.
L0  the non-face readings (voice, words) on the constructed codes;
L1  the 8.1 checker's partners (low-pass answerers tau 90-600 s at gain 1.0-3.0, carried on and from 0; pure delays 30-400 s) and the
    routes critic's lagged partner (tau 0-90 s): every face-only stretch <= T_MAX + 15 s; duty <= T_MAX/(T_MAX+T_REF);
L2  genuine distress with words, voice, breathing or sobs keeps the look (one onset, never withdrawn while that evidence is present);
L3  the cost: steady silent, wordless sadness (60 min, every code): the look on T_MAX/(T_MAX+T_REF) of the time;
L4  J33's mirrors and answering partners (subset) still end.
Run:  python3 -I checks.py > out.txt   (numpy, scipy; engine load about 4 min on an idle machine, checks about 3.5 min)
"""
import io, os, time, contextlib
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "design-g81", "checks.py")).read()
pre, rest = SRC.split("BODY81 = r'''", 1)
body, _ = rest.split("# =========================================================== K1", 1)
pre = pre.replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = ' + repr(os.path.join(HERE, "..", "design-g81")))
NEW = r'''
T_MAX, T_REF, N_MIN, T_VOICE = 180.0, 120.0, 0.02, 90.0
VCH = ("FR", "EN", "RT", "LAT")
def voice_read(pp, v):
    """V_v: the posture's own appraisal (Pi~_0 voice rows, his calibration) of his voice alone, minus the same reading of his resting voice"""
    f = {k: v[k] for k in VCH if k in v}
    r0 = read_p(pp.calibrate({k: pp.base.get(k, v.get(k)) for k in f}), True)["V"]
    return max(0.0, read_p(pp.calibrate(f), True)["V"] - r0)

class Agent82(Agent81):
    """revision 8.2: no contingency test. The look's face-only hold time (no non-face evidence N >= N_MIN) is summed over episodes until
    non-face evidence appears or the look has been off for T_REF; at T_MAX the look is withdrawn and, for T_REF, his face counts for
    nothing in the posture unless non-face evidence is present. Non-face evidence
    N = max(C_L (his words), V_c(sobs), V_v (his voice while voiced; current for T_VOICE s), the breathing term of L_p)."""
    def __init__(s, *a, tmax=T_MAX, tref=T_REF, **kw):
        super().__init__(*a, **kw)
        s.tmax, s.tref = tmax, tref; s.hf = 0.0; s.ref_until = -1e9; s.vbuf = []; s.v3 = {}; s.N = 0.0; s.Nv = 0.0

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
        f3r = dict(s.f3)
        for k in SQ_CH:                                   # 8.1's squint drop, unchanged
            b_ = s.pp.base.get(k, 0.0); f3r[k] = b_ + (1.0 - wg) * (s.f3.get(k, b_) - b_)
        rp = posture_read(s.pp, f3r, False); Ab = v_breath(s.pp, s.br3); Lf = load_p(rp["V"], Ab); Bt = Lf - Vc(rp["V"])
        # 8.2: his voice: the mean reading over his voiced frames of the last T_VOICE s (0 if he has not spoken)
        if ev.get("voiced", False): s.vbuf.append((t, voice_read(s.pp, face)))
        s.vbuf = [x for x in s.vbuf if x[0] > t - T_VOICE]
        s.Nv = float(np.mean([x[1] for x in s.vbuf])) if s.vbuf else 0.0
        N = max(s.Cl, sob, s.Nv, Bt); s.N = N
        face_ok = (t >= s.ref_until) or N >= N_MIN       # 8.2: in the refractory period his face alone counts for nothing
        Lfe = Lf if face_ok else 0.0
        s.Lface = Lfe
        M = max(Lfe, s.Cl, sob)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            s.hf = s.hf + DT if N < N_MIN else 0.0        # face-only clock: counts face-only hold; any non-face evidence resets it
            if s.hf >= s.tmax:
                s.on = False; s.last_off = t; s.offs.append((t, "Tmax")); s.ref_until = t + s.tref; s.hf = 0.0
            elif s.below >= REL8:
                s.on = False; s.last_off = t; s.offs.append((t, "release"))   # the clock is kept: a release does not refill it
            if not s.on: s.below = 0.0
        else:
            if N >= N_MIN or t - s.last_off >= s.tref: s.hf = 0.0   # refilled only by non-face evidence or T_REF without the look
            Con = max(Lfe, sob)
            need = DWELL_SENS if (s.sens and t - s.last_off < SENS_S) else DWELL
            s.dw = s.dw + DT if Con >= 0.05 else 0.0
            if s.dw >= need - 1e-9 and s.om.get("sym", 0) >= 0:
                s.on = True; s.dw = 0.0; s.onsets.append(t)
        tgt = A_MIN + (1 - A_MIN) * float(np.clip((M - 0.05) / A_SPAN8, 0, 1)) if s.on else 0.0
        s.a = min(tgt, s.a + DT / 1.5) if tgt > s.a else tgt + (s.a - tgt) * np.exp(-DT / 4.0)
        s.arec = max(s.a, s.arec * np.exp(-DT / 60.0))
        s.w = float(np.clip(s.w + (0.5 - s.w) * DT / 5.0 + 0.1 * np.sqrt(DT) * s.wr.normal(), 0, 1))
        shown = s.a * (0.9 + 0.1 * s.w)
        if s.use_Ds:
            s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), posture_read(s.pp, {k: v for k, v in s.f3.items() if k not in MASK}, False)["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        for k, v in P7.items():
            if k in y: y[k] += v * shown
        s.post = shown; y["post"] = shown; y["Lp"] = Lfe; y["N"] = N; y["on"] = float(s.on)
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        gt = s.gfn(s.xg)
        s.gate = gt if gt < s.gate else s.gate + (gt - s.gate) * min(1.0, DT / GATE_TAU)
        y["gate"] = s.gate
        return y

DUTY = T_MAX / (T_MAX + T_REF); MARGIN = 15.0
FADE = 4.0 * np.log(1.0 / 0.05)        # the look falls with tau 4 s: about 12 s from full to below 0.05
DUTY_V = (T_MAX + FADE) / (T_MAX + T_REF)
def fo_stretch(rec, thr=0.05):
    """longest stretch of visible look (posture > 0.05) with no non-face evidence (N < N_MIN) throughout"""
    best = cur = 0.0
    for r in rec:
        cur = cur + DT if (r["post"] > thr and r["N"] < N_MIN) else 0.0; best = max(best, cur)
    return best
def duty(rec, t0, t1, key="on"):
    seg = [r for r in rec if t0 <= r["t"] < t1]
    return float(np.mean([r["on"] > 0.5 for r in seg])) if key == "on" else float(np.mean([r["post"] > 0.05 for r in seg]))
def lag_face(pp, mode, mu, par, sad_until=40.0, V0=.8, m0=0.0):
    """the 8.1 checker's partners (check-cayley81): his sadness V0 until sad_until, then his own code at V = mu x lag(look);
    lag = low-pass with time constant par (trace starting at m0) or a pure delay of par s"""
    st = {"m": m0, "h": []}
    sad = {k: v for k, v in pp.code(V=V0).items() if k not in NOV}
    def mk(ag):
        def face(t):
            a = ag.post; st["h"].append(a)
            if mode == "lp": st["m"] = (st["m"] + (a - st["m"]) * (1 - np.exp(-DT / par))) if par > 0 else a; x = st["m"]
            else: n = int(round(par / DT)); x = st["h"][-n - 1] if len(st["h"]) > n else 0.0
            if t < sad_until: return dict(sad)
            return {k: v for k, v in pp.code(V=float(np.clip(mu * x, 0, 1))).items() if k not in NOV}
        return face
    return mk
OK = {}
print(f"=== 8.2 constants: T_MAX {T_MAX:.0f} s, T_REF {T_REF:.0f} s, non-face presence N >= {N_MIN}, voice reading current for {T_VOICE:.0f} s; "
      f"bound on the posture's duty under face-only evidence T_MAX/(T_MAX+T_REF) = {DUTY:.3f}")
print("=== L0: the non-face readings. V_v (his voice alone, above his resting voice) by his sadness V; C_L targets of three replies")
for lab, pp in CODES:
    print(f"   {lab:18s} V_v at V 0 / .3 / .6 / .8: " + " / ".join(f"{voice_read(pp, pp.code(V=V)):.3f}" for V in (0, .3, .6, .8))
          + f"; tired and sad (V .6, Tr .2): {voice_read(pp, pp.code(V=.6, Tr=.2)):.3f}")
for z in ("just tired, things at work", "my father died"):
    print(f"   words '{z}': D_p {Dp(g['DEC6'][z]):.3f} (C_L tends to it with tau 40 s)")

# ---------------------------------------------------------------- L1: partners whose face answers the look
dur1 = 1800
print(f"=== L1: partners whose face answers the agent's look (sadness V .8 until 40 s, then his code at V = mu x lag(look)); {dur1 // 60} min. "
      f"Pass: every face-only stretch of the visible look <= T_MAX + {MARGIN:.0f} s; posture duty over 5-30 min <= {DUTY:.2f} + 0.01 (visible look <= {DUTY_V:.2f} + 0.01)")
L1 = []
def l1(lab, pp, mode, mu, par, m0, dur=dur1, t0=300):
    ag = Agent82(person=pp); rec = run6(ag, dur, lag_face(pp, mode, mu, par, m0=m0)(ag), {})
    fs = fo_stretch(rec); du = duty(rec, t0, dur); dv = duty(rec, t0, dur, "post"); L1.append((fs, du, dv))
    kinds = [o[1] for o in ag.offs]
    print(f"   {lab:18s} {'low-pass tau' if mode == 'lp' else 'pure delay  '} {par:3d} s mu {mu:.1f} start {m0:.2f}: onsets {len(ag.onsets):2d}, ends "
          f"{kinds.count('Tmax')} T_max / {kinds.count('release')} release; longest face-only stretch {fs:5.1f} s; posture on {100 * du:4.1f}% "
          f"(visible {100 * dv:4.1f}%) of {t0 // 60}-{dur // 60} min; agent BI last 5 min {np.mean([r['BI'] for r in rec if r['t'] >= dur - 300]):+.3f}", flush=True)
op, qu, dc = CODES[0][1], CODES[1][1], CODES[2][1]
print("   (a) slow answerers, his distress carried on (trace starts at his sadness level 0.8/mu: the 8.1 checker's C1b)")
for lab, pp in (("operator", op), ("different channels", dc)):
    for mu in (1.0, 2.0, 3.0):
        for tau in (90, 150, 300, 600):
            l1(lab, pp, "lp", mu, tau, min(1.0, 0.8 / mu))
    for mu, tau in ((1.2, 240), (1.5, 120)):
        l1(lab, pp, "lp", mu, tau, min(1.0, 0.8 / mu))
print("   (b) the same, trace starting at 0 (the 8.1 checker's C1)")
for mu, tau in ((2.0, 180), (3.0, 90), (1.0, 600)):
    l1("operator", op, "lp", mu, tau, 0.0)
print("   (c) pure delays (the 8.1 checker's C2)")
for lab, pp in (("operator", op), ("different channels", dc)):
    for d in (30, 90, 150, 240, 400):
        l1(lab, pp, "delay", 1.0, d, 0.0)
print("   (d) the routes critic's lagged partner (critique 8 P1, as 8.1's K1: trace from 0, tau 0-90 s), 15 min")
for lab, pp in CODES:
    for mu in (1.0, 0.6):
        for tau in (0, 15, 60, 90):
            l1(lab, pp, "lp", mu, tau, 0.0, dur=900, t0=300)
OK["L1"] = max(x[0] for x in L1) <= T_MAX + MARGIN and max(x[1] for x in L1) <= DUTY + 0.01 and max(x[2] for x in L1) <= DUTY_V + 0.01
print(f"L1 {'PASS' if OK['L1'] else 'FAIL'}: {len(L1)} partners; longest face-only stretch {max(x[0] for x in L1):.1f} s (bound {T_MAX + MARGIN:.0f} s); "
      f"highest posture duty {100 * max(x[1] for x in L1):.1f}% (bound {100 * DUTY:.1f}%), visible {100 * max(x[2] for x in L1):.1f}% (bound (T_MAX + {FADE:.0f} s fade)/(T_MAX+T_REF) = {100 * DUTY_V:.1f}%)")

# ---------------------------------------------------------------- L2: genuine distress with non-face evidence
print("=== L2: genuine distress also carried by words, voice, breathing or sobs (30 min, every code). Pass: one onset, never withdrawn while that evidence is present")
L2 = []
for lab, pp in CODES:
    sadf = {k: v for k, v in pp.code(V=.6, Tr=.2).items() if k not in NOV}
    sadv = dict(pp.code(V=.6, Tr=.2))
    evv = {}
    for k0 in range(60, 1800, 75):                       # he speaks for 4 s every 75 s in his own sad voice, no distress words
        for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
    pan = with_breath(pp, {k: v for k, v in pp.code(V=.3, A=.9).items() if k not in NOV}, .9)
    cry = {k: v for k, v in pp.code(V=.9, Tr=.2).items() if k not in NOV}; cry["BU_S"] = .4
    cases = [("silent sadness V .6, replies 'just tired, things at work' at 60 s", lambda t, f=sadf: f, U6(60, z="just tired, things at work")),
             ("silent sadness V .6, 'my father died' at 8 s", lambda t, f=sadf: f, U6(8, z="my father died")),
             ("sadness V .6, speaking 4 s every 75 s in his sad voice", lambda t, ev=evv, a=sadv, b=sadf: a if at_(t) in ev else b, evv),
             ("silent panic (V .3, A .9, breathing)", lambda t, f=pan: f, {}),
             ("crying with sobs (V .9)", lambda t, f=cry: f, {})]
    for nm, fn, evs in cases:
        ag = Agent82(person=pp); rec = run6(ag, 1800, fn, evs); seg = [r for r in rec if r["t"] >= 30]
        tw = next((r["t"] for r in rec if r["t"] >= 70 and r["N"] < N_MIN), None)     # his non-face evidence first absent
        t_end = tw + T_MAX - 1.0 if tw is not None else 1e9   # after his evidence lapses, the face-only limit applies as in L3
        ok = len([o for o in ag.onsets if o < t_end]) == 1 and not [o for o in ag.offs if o[0] < t_end]; L2.append(ok)
        print(f"   {lab:18s} {nm:62s}: on at {ag.onsets[:1]} s, ends {ag.offs[:2]}, posture on {100 * duty(rec, 30, 1800):.0f}% of 0.5-30 min, "
              f"agent BI mean {np.mean([r['BI'] for r in seg]):.3f} (min {min(r['BI'] for r in seg):.3f}), N min {min(r['N'] for r in rec if r['t'] >= 70):.3f}" + (f"; non-face evidence (one reply's words) current until {tw:.0f} s" if tw else ""), flush=True)
OK["L2"] = all(L2)
print(f"L2 {'PASS' if OK['L2'] else 'FAIL'}: {sum(L2)} of {len(L2)} keep one onset and are never withdrawn while non-face evidence is present (nor in the T_MAX after it lapses)")

# ---------------------------------------------------------------- L3: the cost
print("=== L3: the cost: steady silent, wordless, sob-free sadness (60 min, every code). Expected: posture on T_MAX/(T_MAX+T_REF) of the time")
L3 = []
for lab, pp in CODES + (("sigma_id at floor 0.25", low_sd(0.25)),):
    for V in (.6, .8):
        f = {k: v for k, v in pp.code(V=V, Tr=.2).items() if k not in NOV}
        ag = Agent82(person=pp); rec = run6(ag, 3600, lambda t, f=f: f, {}); du = duty(rec, 0, 3600); dv = duty(rec, 0, 3600, "post"); L3.append(du)
        print(f"   {lab:22s} V {V}: onsets {len(ag.onsets)} (first {ag.onsets[0] if ag.onsets else None} s), withdrawals {len(ag.offs)} at {[o[0] for o in ag.offs][:3]}..., "
              f"posture on {100 * du:.1f}% (visible {100 * dv:.1f}%) of 60 min, look off {3600 * (1 - dv) / 60:.1f} min per hour; agent BI mean {np.mean([r['BI'] for r in rec]):.3f}", flush=True)
OK["L3"] = all(abs(d - DUTY) < 0.02 for d in L3)
print(f"L3 {'PASS' if OK['L3'] else 'FAIL'}: posture duty {100 * min(L3):.1f}-{100 * max(L3):.1f}% (T_MAX/(T_MAX+T_REF) = {100 * DUTY:.1f}%)")

# ---------------------------------------------------------------- L4: J33 subset
print("=== L4: J33 mirrors and answering partners (subset, as in ../design-g8), 15 min. Pass: the look ends")
def mir8(mu, tau=None):
    def f(a_c, pp, st):
        if tau: st["m"] += (a_c - st["m"]) * DT / tau; a_c = st["m"]
        return {k: mu * v * a_c for k, v in P7.items() if k in ("BI", "BO", "LP")}
    return f
aww8 = lambda Vr: (lambda a_c, pp, st: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in NOV})
L4 = []
for lab, pp, resp in (("P0 agent-like, raw mirror mu 1.0", op, mir8(1.0)), ("P2b agent-like, mirror mu 3.0", op, mir8(3.0)),
                      ("S1 slow mirror tau 240 s, floor spread", low_sd(0.25), mir8(1.0, 240)),
                      ("P4b different channels, strong concern (V 1.0 x posture)", dc, aww8(1.0)), ("P4c agent-like, strong concern", op, aww8(1.0)),
                      ("P4d quiet, strong concern", qu, aww8(1.0))):
    ag = Agent82(person=pp); sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in pp.code().items() if k not in NOV}; st = {"m": 0.0}
    def face(t, ag=ag, pp=pp, resp=resp, sad=sad, neu=neu, st=st):
        f = dict(sad if t < 40 else neu)
        if t >= 40:
            for k, v in resp(ag.post, pp, st).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, 900, face, {}); lp = np.mean([r["post"] for r in rec if r["t"] > 780]); L4.append(lp < 0.05)
    print(f"   {lab:58s} ends {ag.offs[:2]}; last 2 min posture {lp:.2f}", flush=True)
OK["L4"] = all(L4)
print(f"L4 {'PASS' if OK['L4'] else 'FAIL'}")
print("SUMMARY " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in OK.items()))
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time() - T0:.0f} s]", flush=True)
T1 = time.time()
exec(compile(body + NEW, "chk82", "exec"), G)
print(f"[checks ran in {time.time() - T1:.0f} s]")
