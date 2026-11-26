"""Checks for design-cayley-ledger.md, revision 8.2 (L1-L4): the face-only cap replaced by a construction.

Checks of the design's own rules on constructed partners; NOT evidence about behaviour, people or data (brief.md: no toy worlds).
The engine and Agent81 are loaded unchanged from ../design-g81/checks.py exactly as the 8.1 checker's ../check-cayley81/check.py
does (its K1-K5 loops are skipped); that executes revisions 5-8 unchanged. Revision 8.2 changes only the posture's face-only
rule, in the class Agent82 below (a copy of Agent81.step with the cap test removed and the construction added):
  - non-face evidence N = max(C_L (his words), V_c(sobs), N_v (his voice while he speaks, held 40 s), B (the breathing term of the load));
  - face-only hold: on while N < 0.02; it lasts at most T_MAX s (a clock reset only by N >= 0.02); at T_MAX the look is withdrawn;
  - refractory: for T_REF s after that, his face counts for nothing in the posture (onset, grade, hold); N alone can restart it.
L1  the 8.1 checker's partners (low-pass answerers tau 90-600 s, gain 1.0-3.0, from 0 and continuing his sadness; pure delays 10-400 s;
    the routes critic's lagged partners tau 0-90 s): longest face-only stretch <= T_MAX + margin; duty <= T_MAX/(T_MAX+T_REF) + margin;
L2  genuine distress with non-face evidence (words, voice, breathing, sobs) keeps the look steadily (one onset, no withdrawal);
L3  the cost: steady silent, wordless sadness (60 min, every code): look on T_MAX/(T_MAX+T_REF) of the time;
L4  J33's mirrors and answering partners still end (subset), as in 8.1.
Run:  python3 -I checks.py > out.txt   (numpy, scipy; engine load about 4 min, checks about 4-5 min)
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
T_MAX, T_REF, N_MIN, TAU_NV = 180.0, 120.0, 0.02, 40.0
VCH = ("FR", "EN", "RT")
_HV = {}
def read_v(pp, v):
    """H^v_id: his voice alone (FR, EN, RT at his own scale), a per-person ridge head taught by his words exactly as H^p_id (g6 recipe, lam 2)"""
    if id(pp) not in _HV:
        r_ = np.random.default_rng(6); ix = g["idx"]
        Fx = np.array([[(f_[k] + .03 * r_.normal() - pp.base[k]) / max(pp.sd[k], 1e-3) for k in VCH] for f_ in (pp.code(*ZPOP[i]) for i in ix[:400])])
        _HV[id(pp)] = g["fit"](Fx, np.clip(g["XE"][ix[:400]] @ g["WPOP"], 0, 1), lam=2.0)
    x = np.array([(v.get(k, pp.base[k]) - pp.base[k]) / max(pp.sd[k], 1e-3) for k in VCH])
    return float(np.clip(x @ _HV[id(pp)], 0, 1)[0])

class Agent82(Agent81):
    """revision 8.2: no test lapses; a face-only hold lasts at most T_MAX, then his face is ignored by the posture for T_REF."""
    def __init__(s, *a, tmax=T_MAX, tref=T_REF, **kw):
        super().__init__(*a, **kw)
        s.tmax, s.tref = tmax, tref; s.hf = 0.0; s.ref_until = -1e9; s.Nv = 0.0; s.v3 = {}; s.N = 0.0; s.Nmax = 0.0

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
        for k in SQ_CH:                                  # 8.1's squint drop, unchanged
            b_ = s.pp.base.get(k, 0.0); f3r[k] = b_ + (1.0 - wg) * (s.f3.get(k, b_) - b_)
        rp = posture_read(s.pp, f3r, False); Ab = v_breath(s.pp, s.br3); Lf = load_p(rp["V"], Ab); B = Lf - Vc(rp["V"])
        # 8.2: his voice while he speaks (3-s smoothing of the voice channels; the reading held with tau 40 s, as his words' C_L)
        voiced = ev.get("voiced", False)
        if voiced:
            for k in ("FR", "EN", "RT"):
                if k in face: s.v3[k] = s.v3.get(k, face[k]) + (face[k] - s.v3.get(k, face[k])) * DT / 3.0
        s.Nv *= np.exp(-DT / TAU_NV)
        if voiced and s.v3: s.Nv = max(s.Nv, Vc(read_v(s.pp, s.v3)))
        N = max(s.Cl, sob, s.Nv, B); s.N = N; s.Nmax = max(s.Nmax, s.Nv)
        face_ok = t >= s.ref_until                       # 8.2: his face counts for nothing during the refractory period
        Lfe = Lf if face_ok else 0.0
        s.Lface = Lfe
        M = max(Lfe, N)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            s.hf = s.hf + DT if N < N_MIN else 0.0       # face-only clock; any non-face evidence resets it
            if s.hf >= s.tmax:
                s.on = False; s.last_off = t; s.offs.append((t, "Tmax")); s.ref_until = t + s.tref
            elif s.below >= REL8:
                s.on = False; s.last_off = t; s.offs.append((t, "release"))
            if not s.on: s.below = 0.0; s.hf = 0.0
        else:
            Con = max(Lfe, N)
            need = DWELL_SENS if (s.sens and t - s.last_off < SENS_S) else DWELL
            s.dw = s.dw + DT if Con >= 0.05 else 0.0
            if s.dw >= need - 1e-9 and s.om.get("sym", 0) >= 0:
                s.on = True; s.dw = 0.0; s.onsets.append(t); s.hf = 0.0
        Mg = max(Lfe, N)
        tgt = A_MIN + (1 - A_MIN) * float(np.clip((Mg - 0.05) / A_SPAN8, 0, 1)) if s.on else 0.0
        s.a = min(tgt, s.a + DT / 1.5) if tgt > s.a else tgt + (s.a - tgt) * np.exp(-DT / 4.0)
        s.arec = max(s.a, s.arec * np.exp(-DT / 60.0))
        s.w = float(np.clip(s.w + (0.5 - s.w) * DT / 5.0 + 0.1 * np.sqrt(DT) * s.wr.normal(), 0, 1))
        shown = s.a * (0.9 + 0.1 * s.w)
        if s.use_Ds:
            s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), posture_read(s.pp, {k: v for k, v in s.f3.items() if k not in MASK}, False)["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        for k, v in P7.items():
            if k in y: y[k] += v * shown
        s.post = shown; y["post"] = shown; y["Lp"] = Lfe; y["N"] = N
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        gt = s.gfn(s.xg)
        s.gate = gt if gt < s.gate else s.gate + (gt - s.gate) * min(1.0, DT / GATE_TAU)
        y["gate"] = s.gate
        return y

DUTY = T_MAX / (T_MAX + T_REF); MARGIN = 15.0
def stretches(rec, thr=0.05):
    out = []; st = None
    for r in rec:
        if r["post"] > thr and st is None: st = r["t"]
        if r["post"] <= thr and st is not None: out.append((st, r["t"] - st)); st = None
    if st is not None: out.append((st, rec[-1]["t"] + DT - st))
    return out
def fo_stretch(rec, thr=0.05):
    """longest stretch of look on with no non-face evidence (N < N_MIN) throughout"""
    best = cur = 0.0
    for r in rec:
        cur = cur + DT if (r["post"] > thr and r["N"] < N_MIN) else 0.0; best = max(best, cur)
    return best
def duty(rec, t0, t1): return float(np.mean([r["post"] > 0.05 for r in rec if t0 <= r["t"] < t1]))
def lag_face(pp, mode, mu, par, sad_until=40.0, V0=.8, m0=0.0):
    st = {"m": m0, "h": []}
    sad = {k: v for k, v in pp.code(V=V0).items() if k not in NOV}
    def mk(ag):
        def face(t):
            a = ag.post; st["h"].append(a)
            if mode == "lp": st["m"] = st["m"] + (a - st["m"]) * (1 - np.exp(-DT / par)) if par > 0 else a; x = st["m"]
            else: n = int(round(par / DT)); x = st["h"][-n - 1] if len(st["h"]) > n else 0.0
            if t < sad_until: return dict(sad)
            return {k: v for k, v in pp.code(V=float(np.clip(mu * x, 0, 1))).items() if k not in NOV}
        return face
    return mk
OK = {}

# ---------------------------------------------------------------- L0: the voice reading (his own code, voiced, at V levels)
print(f"=== 8.2 constants: T_MAX {T_MAX:.0f} s, T_REF {T_REF:.0f} s, non-face threshold {N_MIN}, voice hold tau {TAU_NV:.0f} s; duty bound T_MAX/(T_MAX+T_REF) = {DUTY:.3f}")
print("=== L0: N_v = V_c(voice-only reading) of each code's own voice (FR, EN, RT), by his sadness V")
for lab, pp in CODES:
    print(f"   {lab:18s} " + ", ".join(f"V {V:.1f}: read {read_v(pp, {k: pp.code(V=V)[k] for k in ('FR','EN','RT')}):.2f} -> N_v {Vc(read_v(pp, {k: pp.code(V=V)[k] for k in ('FR','EN','RT')})):.3f}" for V in (0, .3, .6, .8)))
for z in ("just tired, things at work", "my father died", "yeah / ok"):
    print(f"   words '{z}': D_p {Dp(g['DEC6'][z]):.3f} (C_L tends to this with tau 40 s; NL decays with tau 30 min)")

# ---------------------------------------------------------------- L1: the 8.1 checker's partners
print(f"=== L1: answering partners (his sadness V .8 until 40 s, then his code at V = mu x lag(look)); 40 min. Pass: face-only stretch <= T_MAX + {MARGIN:.0f} s, duty over 10-40 min <= {DUTY:.2f} + 0.02")
L1 = []
def l1(lab, pp, mode, mu, par, m0, dur=2400):
    ag = Agent82(person=pp); rec = run6(ag, dur, lag_face(pp, mode, mu, par, m0=m0)(ag), {})
    fs = fo_stretch(rec); du = duty(rec, 600, dur); L1.append((fs, du))
    print(f"   {lab:18s} {mode:5s} {'tau' if mode == 'lp' else 'd'} {par:3d} s mu {mu} start {m0:.2f}: onsets {len(ag.onsets)}, ends {[o[1] for o in ag.offs][:4]}{'...' if len(ag.offs) > 4 else ''}, "
          f"longest face-only stretch {fs:.0f} s, look on {100 * du:.0f}% of 10-40 min, BI last 10 min {np.mean([r['BI'] for r in rec if r['t'] >= dur - 600]):+.3f}", flush=True)
op, dc = CODES[0][1], CODES[2][1]
for mu in (1.0, 1.2, 1.5, 2.0, 3.0):
    for tau in (90, 150, 300, 600):
        l1("operator", op, "lp", mu, tau, min(1.0, 0.8 / mu))
for mu, tau in ((1.0, 300), (1.0, 600), (1.2, 240), (2.0, 180), (3.0, 90)):
    l1("operator", op, "lp", mu, tau, 0.0)
    l1("different channels", dc, "lp", mu, tau, min(1.0, 0.8 / mu))
for d in (10, 30, 90, 150, 240, 400):
    for lab, pp in (("operator", op), ("different channels", dc)):
        l1(lab, pp, "delay", 1.0, d, 0.0)
for lab, pp in CODES:
    for tau in (0, 30, 90):
        l1(lab, pp, "lp", 1.0, tau, 0.0, dur=900)
OK["L1"] = max(f for f, d in L1) <= T_MAX + MARGIN and max(d for f, d in L1) <= DUTY + 0.02
print(f"L1 {'PASS' if OK['L1'] else 'FAIL'}: longest face-only stretch {max(f for f, d in L1):.0f} s (bound {T_MAX + MARGIN:.0f}); highest duty {100 * max(d for f, d in L1):.1f}% (bound {100 * DUTY:.1f}%)")

# ---------------------------------------------------------------- L2: genuine distress with non-face evidence: steady
print("=== L2: genuine distress carried also by words, voice, breathing or sobs (30 min, every code): one onset, never withdrawn")
L2 = []
for lab, pp in CODES:
    sadf = {k: v for k, v in pp.code(V=.6, Tr=.2).items() if k not in NOV}
    sadv = {k: v for k, v in pp.code(V=.6, Tr=.2).items()}
    cases = [("silent sadness, 'just tired, things at work' at 30 s", lambda t, f=sadf: f, U6(30, z="just tired, things at work")),
             ("silent sadness, 'my father died' at 8 s", lambda t, f=sadf: f, U6(8, z="my father died"))]
    evv = {}
    for k0 in range(60, 1800, 75):                   # he speaks for 4 s every 75 s, sad voice, no distress words
        for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
    cases.append(("sad face, speaking 4 s every 75 s in a sad voice", lambda t, ev=evv: sadv if at_(t) in ev else sadf, evv))
    pan = with_breath(pp, {k: v for k, v in pp.code(V=.3, A=.9).items() if k not in NOV}, .9)
    cases.append(("silent panic (V .3, A .9, breathing)", lambda t, f=pan: f, {}))
    cry = dict({k: v for k, v in pp.code(V=.9, Tr=.2).items() if k not in NOV}); cry["BU_S"] = .4
    cases.append(("crying with sobs", lambda t, f=cry: f, {}))
    for nm, fn, evs in cases:
        ag = Agent82(person=pp); rec = run6(ag, 1800, fn, evs); seg = [r for r in rec if r["t"] >= 20]
        ok = len(ag.onsets) == 1 and not ag.offs; L2.append(ok)
        print(f"   {lab:18s} {nm:52s}: on at {ag.onsets[:1]}, ends {ag.offs[:2]}, look on {100 * duty(rec, 20, 1800):.0f}% of 20-1800 s, brow mean {np.mean([r['BI'] for r in seg]):.3f}, min {min(r['BI'] for r in seg):.3f}", flush=True)
OK["L2"] = all(L2)
print(f"L2 {'PASS' if OK['L2'] else 'FAIL'}: {sum(L2)} of {len(L2)} keep one onset and no withdrawal")

# ---------------------------------------------------------------- L3: the cost
print("=== L3: steady silent, wordless sadness (V .6; also grief V .8), 60 min: the look on T_MAX/(T_MAX+T_REF) of the time")
L3 = []
for lab, pp in CODES + (("sigma_id at floor 0.25", low_sd(0.25)),):
    for V in (.6, .8):
        f = {k: v for k, v in pp.code(V=V, Tr=.2).items() if k not in NOV}
        ag = Agent82(person=pp); rec = run6(ag, 3600, lambda t, f=f: f, {}); du = duty(rec, 0, 3600); L3.append(du)
        st_ = stretches(rec)
        print(f"   {lab:22s} V {V}: onsets {len(ag.onsets)} (first {ag.onsets[0] if ag.onsets else None} s), withdrawals {len(ag.offs)}, on-stretches {sorted(set(round(d) for _, d in st_))} s, "
              f"look on {100 * du:.1f}% of 60 min ({3600 * (1 - du) / 60:.1f} min off)", flush=True)
OK["L3"] = all(abs(d - DUTY) < 0.05 for d in L3)
print(f"L3 {'PASS' if OK['L3'] else 'FAIL'}: duty {100 * min(L3):.1f}-{100 * max(L3):.1f}% (T_MAX/(T_MAX+T_REF) = {100 * DUTY:.1f}%)")

# ---------------------------------------------------------------- L4: J33 subset still ends
print("=== L4: J33 mirrors and answering partners (subset), 15 min")
def mir8(mu, tau=None):
    def f(a_c, pp, st):
        if tau: st["m"] += (a_c - st["m"]) * DT / tau; a_c = st["m"]
        return {k: mu * v * a_c for k, v in P7.items() if k in ("BI", "BO", "LP")}
    return f
aww8 = lambda Vr: (lambda a_c, pp, st: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in NOV})
L4 = []
for lab, pp, resp in (("P0 agent-like, raw mirror mu 1.0", op, mir8(1.0)), ("P2b agent-like, mirror mu 3.0", op, mir8(3.0)),
                      ("S1 slow mirror tau 240 s, floor spread", low_sd(0.25), mir8(1.0, 240)),
                      ("P4b different channels, strong concern (V 1.0 x posture)", dc, aww8(1.0)), ("P4c agent-like, strong concern", op, aww8(1.0))):
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
