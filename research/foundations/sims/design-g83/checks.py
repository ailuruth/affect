"""Checks for design-cayley-ledger.md, revision 8.3 (M1-M5): voice and breathing may only extend the face-only limit, never reset it.

Checks of the design's own rules on constructed partners; NOT evidence about behaviour, people or data (brief.md: no toy worlds).
Loads ../design-g82/checks.py's definitions (engine, Agent81, Agent82, lag_face, voice_read) unchanged, exactly as the 8.2 checker's
../check-cayley82/check.py does (its L0-L4 loops skipped). Revision 8.3 changes only the face-only rule, in Agent83 below (a copy of
Agent82.step with the evidence split):
  - hard evidence H = max(C_L (his decoded words), V_c(sobs)); soft evidence S = max(V_v (his voice, 90-s mean), the breathing term);
  - the clock counts the time the look is on while H < 0.02 (soft evidence does not stop or reset it); it is refilled only by H >= 0.02
    or by T_REF without the look (as 8.2);
  - the look is withdrawn when the clock reaches T_MAX = 180 s while S < 0.02, and in any case at T_MAX_EXT = 600 s;
  - refractory: for T_REF = 120 s after that, his face (and breathing) count for nothing in the posture unless H >= 0.02.
M1  the 8.2 checker's B3 speaking answerer (every 60/80/120/240 s, EN -0.03/-0.05, three codes) and B1 answering breather
    (beta 0.5/0.7/0.9), plus both at once, 60 min: longest no-H stretch of the posture <= T_MAX_EXT, duty <= T_MAX_EXT/(T_MAX_EXT+T_REF);
M2  mute answerers and adversarial faces (subset of 8.2's L1 and the checker's A): unchanged from 8.2 (<= T_MAX, 60 %);
M3  genuine distress: words and sobs keep the look steadily; sad voice and panic breathing now 10 min on / 2 min off (the cost);
M4  the residual: a partner who sobs (or names distress) in answer to the look: sob threshold and what happens;
M5  the visible-look margins (stretch, duty) against the posture's on-state.
Run:  python3 -I checks.py > out.txt   (engine load about 4 min; checks a few minutes)
"""
import io, os, time, contextlib
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
D81 = os.path.join(HERE, "..", "design-g81"); D82 = os.path.join(HERE, "..", "design-g82")
SRC = open(os.path.join(D81, "checks.py")).read()
pre, rest = SRC.split("BODY81 = r'''", 1)
body, _ = rest.split("# =========================================================== K1", 1)
pre = pre.replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = ' + repr(D81))
S82 = open(os.path.join(D82, "checks.py")).read()
NEW82 = S82.split("NEW = r'''", 1)[1].split("OK = {}", 1)[0]
MINE = r'''
T_MAX_EXT = 600.0
class Agent83(Agent82):
    def __init__(s, *a, tmax_ext=T_MAX_EXT, **kw):
        super().__init__(*a, **kw); s.tmax_ext = tmax_ext; s.H = 0.0; s.S = 0.0
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
        for k in SQ_CH:
            b_ = s.pp.base.get(k, 0.0); f3r[k] = b_ + (1.0 - wg) * (s.f3.get(k, b_) - b_)
        rp = posture_read(s.pp, f3r, False); Ab = v_breath(s.pp, s.br3); Lf = load_p(rp["V"], Ab); Bt = Lf - Vc(rp["V"])
        if ev.get("voiced", False): s.vbuf.append((t, voice_read(s.pp, face)))
        s.vbuf = [x for x in s.vbuf if x[0] > t - T_VOICE]
        s.Nv = float(np.mean([x[1] for x in s.vbuf])) if s.vbuf else 0.0
        H = max(s.Cl, sob); S = max(s.Nv, Bt); s.H, s.S = H, S; s.N = max(H, S)      # 8.3: hard (words, sobs) and soft (voice, breathing)
        face_ok = (t >= s.ref_until) or H >= N_MIN       # 8.3: in the refractory period only words or sobs count
        Lfe = Lf if face_ok else 0.0
        s.Lface = Lfe
        M = max(Lfe, s.Cl, sob)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            s.hf = s.hf + DT if H < N_MIN else 0.0        # 8.3: only words or sobs reset the clock
            if s.hf >= s.tmax_ext or (s.hf >= s.tmax and S < N_MIN):
                s.on = False; s.last_off = t; s.offs.append((t, "Text" if s.hf >= s.tmax_ext else "Tmax")); s.ref_until = t + s.tref; s.hf = 0.0
            elif s.below >= REL8:
                s.on = False; s.last_off = t; s.offs.append((t, "release"))
            if not s.on: s.below = 0.0
        else:
            if H >= N_MIN or t - s.last_off >= s.tref: s.hf = 0.0
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
        s.post = shown; y["post"] = shown; y["Lp"] = Lfe; y["N"] = s.N; y["H"] = H; y["S"] = S; y["on"] = float(s.on)
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        gt = s.gfn(s.xg)
        s.gate = gt if gt < s.gate else s.gate + (gt - s.gate) * min(1.0, DT / GATE_TAU)
        y["gate"] = s.gate
        return y

def stretch(rec, key, thr=None):
    """longest stretch of the posture's on-state (thr None) or of the visible look (post > thr) with H < N_MIN throughout"""
    best = cur = 0.0
    for r in rec:
        c = (r["on"] > 0.5) if thr is None else (r["post"] > thr)
        cur = cur + DT if (c and r[key] < N_MIN) else 0.0; best = max(best, cur)
    return best
RES = {"M1": [], "M2": [], "M4": [], "vis": []}
def summ(lab, ag, rec, grp, t0=300):
    t1 = rec[-1]["t"] + DT
    so = stretch(rec, "H"); sv = stretch(rec, "H", 0.05); du = duty(rec, t0, t1); dv = duty(rec, t0, t1, "post")
    RES[grp].append((so, du)); RES["vis"].append((grp, sv, dv))
    k = [o[1] for o in ag.offs]
    print(f"   {lab:62s} onsets {len(ag.onsets):2d}, ends T_ext {k.count('Text'):2d} / T_max {k.count('Tmax'):2d} / release {k.count('release'):2d}; "
          f"longest stretch on {so:5.1f} s (visible {sv:5.1f} s); on {100*du:5.1f}% (visible {100*dv:5.1f}%) after {t0} s; "
          f"agent BI mean after {t0} s {np.mean([r['BI'] for r in rec if r['t'] >= t0]):+.3f}; S mean {np.mean([r['S'] for r in rec if r['t'] >= t0]):.3f}", flush=True)
    return so, du
op, qu, dc = CODES[0][1], CODES[1][1], CODES[2][1]
DUTY_EXT = T_MAX_EXT / (T_MAX_EXT + T_REF)
print(f"=== 8.3 constants: T_MAX {T_MAX:.0f} s (no soft evidence), T_MAX_EXT {T_MAX_EXT:.0f} s (soft evidence: voice, breathing), T_REF {T_REF:.0f} s; "
      f"duty bounds {DUTY:.3f} / {DUTY_EXT:.3f}")
def spk(P, dur, start=60):
    evv = {}
    for k0 in range(start, dur, P):
        for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
    return evv
DUR = 3600
print(f"=== M1: answering face (mu 1, tau 300, carried on: C1b) plus voice and/or breathing that answer; {DUR // 60} min. "
      f"Pass: longest no-word/no-sob stretch of the posture <= {T_MAX_EXT:.0f} s, duty <= {100 * DUTY_EXT:.1f}%")
for lab, pp in (("operator", op), ("quiet 0.3", qu), ("different channels", dc)):
    for d, P in ((0.03, 60), (0.03, 80), (0.05, 80), (0.03, 120), (0.05, 120), (0.03, 240)):
        evv = spk(P, DUR); ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); rest = pp.code()
        def face(t, fa=fa, evv=evv, rest=rest, d=d):
            f = dict(fa(t))
            if at_(t) in evv:
                for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
                f["EN"] = rest.get("EN", 0.0) - d
            return f
        summ(f"{lab}: B3 soft voice EN -{d:.2f} every {P} s", ag, run6(ag, DUR, face, evv), "M1")
for lab, pp in (("operator", op), ("different channels", dc)):
    for beta in (0.5, 0.7, 0.9):
        ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); st = {"b": 0.0}
        def face(t, ag=ag, fa=fa, st=st, beta=beta, pp=pp):
            f = dict(fa(t)); st["b"] += (ag.post - st["b"]) * DT / 30.0
            if t >= 40: f["BR"] = BR_GAIN * br_amp(pp) * beta * st["b"]
            return f
        summ(f"{lab}: B1 breath answer beta {beta}", ag, run6(ag, DUR, face, {}), "M1")
    # both: breathing beta 0.9 and soft voice EN -0.05 every 80 s
    evv = spk(80, DUR); ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); st = {"b": 0.0}; rest = pp.code()
    def face(t, ag=ag, fa=fa, st=st, pp=pp, evv=evv, rest=rest):
        f = dict(fa(t)); st["b"] += (ag.post - st["b"]) * DT / 30.0
        if t >= 40: f["BR"] = BR_GAIN * br_amp(pp) * 0.9 * st["b"]
        if at_(t) in evv:
            for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
            f["EN"] = rest.get("EN", 0.0) - 0.05
        return f
    summ(f"{lab}: B1+B3 breath beta 0.9 and voice EN -0.05 every 80 s", ag, run6(ag, DUR, face, evv), "M1")
m1 = RES["M1"]
OK = {"M1": max(x[0] for x in m1) <= T_MAX_EXT + 1 and max(x[1] for x in m1) <= DUTY_EXT + 0.01}
print(f"M1 {'PASS' if OK['M1'] else 'FAIL'}: {len(m1)} partners; longest stretch {max(x[0] for x in m1):.1f} s; highest duty {100 * max(x[1] for x in m1):.1f}%")

print("=== M2: mute answerers and adversarial faces (subset of 8.2's L1 and the 8.2 checker's A), 30 min: unchanged bound T_MAX, 60 %")
for lab, pp in (("operator", op), ("different channels", dc)):
    for mode, mu, par, m0 in (("lp", 1.0, 300, 0.8), ("lp", 3.0, 90, 0.8 / 3), ("delay", 1.0, 150, 0.0)):
        ag = Agent83(person=pp); summ(f"{lab}: mute answerer {mode} {par} s mu {mu}", ag, run6(ag, 1800, lag_face(pp, mode, mu, par, m0=m0)(ag), {}), "M2")
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in pp.code().items() if k not in NOV}
    for Don, Doff in ((150, 25), (170, 21)):
        ag = Agent83(person=pp); st = {"mode": "sad", "t": 0.0}
        def face(t, ag=ag, st=st, sad=sad, neu=neu, Don=Don, Doff=Doff):
            if st["mode"] == "sad" and ag.on and t - st.get("on_t", t) >= Don: st["mode"] = "neu"; st["t"] = t
            if st["mode"] == "neu" and t - st["t"] >= Doff: st["mode"] = "sad"; st.pop("on_t", None)
            if ag.on and "on_t" not in st: st["on_t"] = t
            return sad if st["mode"] == "sad" else neu
        summ(f"{lab}: cycler sad {Don} s of look-on, rest {Doff} s", ag, run6(ag, 1800, face, {}), "M2")
m2 = RES["M2"]
OK["M2"] = max(x[0] for x in m2) <= T_MAX + 1 and max(x[1] for x in m2) <= DUTY + 0.01
print(f"M2 {'PASS' if OK['M2'] else 'FAIL'}: longest stretch {max(x[0] for x in m2):.1f} s; highest duty {100 * max(x[1] for x in m2):.1f}%")

print("=== M3: genuine distress (30 min, every code). Words and sobs: one onset, never withdrawn while they are present; voice or breathing only: the cost")
M3 = []
for lab, pp in CODES:
    sadf = {k: v for k, v in pp.code(V=.6, Tr=.2).items() if k not in NOV}
    sadv = dict(pp.code(V=.6, Tr=.2)); evv = spk(75, 1800)
    pan = with_breath(pp, {k: v for k, v in pp.code(V=.3, A=.9).items() if k not in NOV}, .9)
    cry = {k: v for k, v in pp.code(V=.9, Tr=.2).items() if k not in NOV}; cry["BU_S"] = .4
    cases = [("hard", "silent sadness V .6, 'just tired, things at work' at 60 s", lambda t, f=sadf: f, U6(60, z="just tired, things at work")),
             ("hard", "silent sadness V .6, 'my father died' at 8 s", lambda t, f=sadf: f, U6(8, z="my father died")),
             ("hard", "crying with sobs (V .9)", lambda t, f=cry: f, {}),
             ("soft", "sadness V .6, speaking 4 s every 75 s in his sad voice", lambda t, ev=evv, a=sadv, b=sadf: a if at_(t) in ev else b, evv),
             ("soft", "silent panic (V .3, A .9, breathing)", lambda t, f=pan: f, {})]
    for kind, nm, fn, evs in cases:
        ag = Agent83(person=pp); rec = run6(ag, 1800, fn, evs); seg = [r for r in rec if r["t"] >= 30]
        du = duty(rec, 30, 1800)
        if kind == "hard":
            tw = next((r["t"] for r in rec if r["t"] >= 70 and r["H"] < N_MIN), None)
            t_end = tw + T_MAX - 1.0 if tw is not None else 1e9
            ok = len([o for o in ag.onsets if o < t_end]) == 1 and not [o for o in ag.offs if o[0] < t_end]
        else:
            # stated: on T_MAX_EXT from each onset, off T_REF (+ dwell) after each withdrawal; long-run duty T_MAX_EXT/(T_MAX_EXT+T_REF)
            ok = (len(ag.offs) >= 2 and all(abs(o[0] - n - T_MAX_EXT) < 2 for o, n in zip(ag.offs, ag.onsets))
                  and all(0 <= n - o[0] - T_REF < 6 for o, n in zip(ag.offs, ag.onsets[1:])))
            cyc = ag.onsets[2] - ag.onsets[1]; du = (ag.offs[1][0] - ag.onsets[1]) / cyc
            tw = None
        M3.append(ok)
        print(f"   {lab:18s} [{kind}] {nm:58s}: on at {ag.onsets[:3]} s, ends {[(round(o[0], 1), o[1]) for o in ag.offs[:3]]}, posture on {100 * du:.1f}% {'of 0.5-30 min' if kind == 'hard' else 'per cycle (2nd)'}, "
              f"agent BI mean {np.mean([r['BI'] for r in seg]):.3f}" + (f"; words current until {tw:.0f} s" if tw else "") + f" -> {'ok' if ok else 'NOT as stated'}", flush=True)
OK["M3"] = all(M3)
print(f"M3 {'PASS' if OK['M3'] else 'FAIL'}: {sum(M3)} of {len(M3)} as stated (hard: steady; soft: on T_MAX_EXT, off T_REF, duty {100 * DUTY_EXT:.1f}% per cycle)")

print("=== M4: the residual. Sob reading: V_c(min(1, 2.5 BU_S)) >= 0.02 needs BU_S >= " + f"{(0.1 + np.sqrt(0.02 / 0.8)) / 2.5:.3f}")
for lab, pp in (("operator", op),):
    for g in (0.05, 0.10, 0.20):
        ag = Agent83(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); st = {"b": 0.0}
        def face(t, ag=ag, fa=fa, st=st, g=g):
            f = dict(fa(t)); st["b"] += (ag.post - st["b"]) * DT / 30.0
            if t >= 40: f["BU_S"] = g * st["b"]
            return f
        summ(f"{lab}: sobs answer the look, BU_S = {g:.2f} x lowpass(look, 30 s)", ag, run6(ag, 1800, face, {}), "M4")

print("=== M5: visible margins over every run above (visible = posture output > 0.05)")
for grp, T in (("M1", T_MAX_EXT), ("M2", T_MAX)):
    v = [x for x in RES["vis"] if x[0] == grp]
    print(f"   {grp}: posture on-state stretch max {max(x[0] for x in RES[grp]):.1f} s (bound {T:.0f} s), duty max {100 * max(x[1] for x in RES[grp]):.1f}%; "
          f"visible stretch max {max(x[1] for x in v):.1f} s (T + {max(x[1] for x in v) - T:.1f} s), visible duty max {100 * max(x[2] for x in v):.1f}%")
print("SUMMARY " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in OK.items()))
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time() - T0:.0f} s]", flush=True)
exec(compile(body + NEW82 + MINE, "chk83", "exec"), G)
print(f"[done in {time.time() - T0:.0f} s]")
