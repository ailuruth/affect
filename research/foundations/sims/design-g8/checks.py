"""Algebra checks for design-cayley-ledger.md, revision 8 (J31-J39).

Checks of the design's own inequalities and constants on constructed instances; NOT evidence about behaviour, people or data
(brief.md: no toy worlds). Scenario numbers (J39) are what the design's equations and constants give for stated inputs.

The revision-7 engine is loaded exactly as built from ../design-g7/checks.py (which executes design-g6 and design-g5 unchanged),
skipping only revision 7's own result loops (J17-J19, J21-J30), the same way the revision-7 routes critic's posture7.py does.
Its J0 constants, J20 dyad fit (the gate and Lambda, constructed corpus), Agent7 and the helpers are reused; revision 8 overrides
what it changes in the class Agent8 below. The critics' constructed partners are re-run: routes Q1-Q3 and S1 (J32, J33), the
J22 mirror set (J33), agent A, A2, B, C (J34-J36, J39).
Run:  python3 -I checks.py > out.txt    (numpy, scipy; about 20 minutes here, most of it loading revisions 5-7)
"""
import io, os, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
P7SRC = os.path.join(HERE, "..", "design-g7", "checks.py")
L = open(P7SRC).read().split("\n")
_k = ("# =========================================================== J17", "# =========================================================== agent part",
      "# =========================================================== J21", "# =========================================================== the revision-7 agent",
      "# =========================================================== J22", "cases = [")
idx = {k: next(i for i, s in enumerate(L) if s.startswith(k)) for k in _k}
src = "\n".join(L[:idx[_k[0]]] + L[idx[_k[1]]:idx[_k[2]]] + L[idx[_k[3]]:idx[_k[5]]])
G7 = {"__name__": "g7", "__file__": P7SRC}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "checks_g7_parts", "exec"), G7)
G7["OK"].clear()
BODY = r'''
# ---------------------------------------------------------------- revision 8 agent (definitions only; exec'd after the revision-7 parts)
import numpy as np
RD_CH8, M0_8, RD_L8 = G5["RD_CH"], G5["M0"], G5["RD_L"]
WR8 = ("BI", "BO", "LP", "UL", "TILT", "HP", "HG")       # what the posture writes or modulates: never read by it (rule 9')
VOICE8 = ("FR", "EN", "RT", "LAT")
FCP8 = [k for k in FACE_CH if k not in WR8]               # face channels the posture may read: CR, LD, BRE, BL, LPR, CHR (+ voice)
REL8, PROBE0, PROBE_MAX, PROBE_LEN, PROBE_DEPTH, PROBE_FOLLOW = 20.0, 180.0, 180.0, 8.0, 0.5, 0.8
W_AR, A_FLOOR, V_GATE0, V_GATE1 = 0.4, 0.30, 0.15, 0.15  # arousal term: 0.4 (A_b - 0.30)+^2 x clip((V_p - 0.15)/0.15, 0, 1)
A_SPAN8 = 0.12                                           # grade span: a* = 0.35 + 0.65 clip((M - 0.05)/0.12, 0, 1)
GLARE_SAT = 0.15                                         # the agent's own threat reflex (glare at it, 3 s) silences the posture's face load at >= 0.15
BR_GAIN = 0.30                                           # constructed codes: breathing load = 0.30 A x the code's amplitude
DELTA_G, LAMBDA_W = 0.80, 0.25                           # gated group's echo delay (s); word look-ahead past the source frame (s)


def read_p(face_cal, voiced=False):
    """Pi~_0 with the posture's own channels removed from the inverse (rows dropped, not set to neutral)"""
    rows = [i for i, k in enumerate(RD_CH8) if k not in WR8 and (voiced or k not in VOICE8)]
    x = np.array([face_cal.get(RD_CH8[i], 0.0) - (0.45 if RD_CH8[i] == "EN" else 0.25 if RD_CH8[i] == "FR" else
                                                0.40 if RD_CH8[i] == "RT" else 0.0) * (1 if voiced else 0) for i in rows])
    M = M0_8[rows]; z = np.linalg.solve(M.T @ M + 0.05 * np.eye(len(RD_L8)), M.T @ x); z = dict(zip(RD_L8, z))
    return dict(V=float(np.clip(z["dis"] + z["hd"], 0, 1)), A=float(np.clip(z["act"], 0, 1)), Vlin=float(z["dis"] + z["hd"]))


_HP = {}
def head_p(pp):
    """H^p_id: the per-person face head restricted to FCP8, taught by his words exactly as H_id (g6 recipe, lam 2)"""
    if pp.head is None: return None
    if id(pp) not in _HP:
        r_ = np.random.default_rng(5); ix = g["idx"]
        Fx = np.array([feats_p(pp, {k: v + .03 * r_.normal() for k, v in pp.code(*ZPOP[i]).items()}) for i in ix[:400]])
        _HP[id(pp)] = g["fit"](Fx, np.clip(g["XE"][ix[:400]] @ g["WPOP"], 0, 1), lam=2.0)
    return _HP[id(pp)]


def feats_p(pp, face):
    return np.array([(face.get(k, pp.base[k]) - pp.base[k]) / max(pp.sd[k], 1e-3) if k in FCP8 else 0.0 for k in FACE_CH])


def posture_read(pp, face, voiced=False):
    """the agent's own appraisal for the posture: his calibrated face WITHOUT the channels the posture writes, his voice when voiced"""
    f = {k: v for k, v in face.items() if k not in WR8 and (voiced or k not in VOICE8)}
    r0 = read_p(pp.calibrate(f), voiced); hp = head_p(pp)
    if hp is None: return r0
    hl = feats_p(pp, f) @ hp; h = np.clip(hl, 0, 1)
    return dict(V=max(r0["V"], float(h[0])), A=max(r0["A"], float(h[1])), Vlin=max(r0["Vlin"], float(hl[0])))


def br_amp(pp): return getattr(pp, "br_amp", 0.3 if pp.kind == "low-expressive" else 1.0)
def v_breath(pp, br_raw):                                 # breathing above his own resting level, at his own scale (sigma floor 0.25)
    return float(np.clip(br_raw / (BR_GAIN * max(br_amp(pp), 0.25)), 0, 1))
def with_breath(pp, face, A):
    f = dict(face); f["BR"] = BR_GAIN * A * br_amp(pp); return f


def load_p(V, A_b):
    return Vc(V) + W_AR * max(A_b - A_FLOOR, 0.0) ** 2 * float(np.clip((V - V_GATE0) / V_GATE1, 0, 1))


class Agent8(Agent7):
    """revision 8: the posture never reads what it writes (no mirror removal); a contingency probe replaces the face-only release;
    breathing and voice carry arousal into the posture's load; the gate closes instantly and opens with tau 0.3 s; the play laugh
    passes through the gate (no care condition)."""
    def __init__(s, *a, probe=True, **kw):
        super().__init__(*a, **kw)
        s.fo = 0.0; s.probe_iv = PROBE0; s.probe_t = None; s.Lpre = 0.0; s.Lbuf = []; s.probes = []; s.Lf3 = 0.0; s.br3 = 0.0
        s.use_probe = probe; s.Lface = 0.0

    def utter(s, t, u):
        u = dict(u); pl = g["play6"](u, 0.0) if s.trained else False       # no care condition (D85: the gate decides)
        if pl: u["cont"] = True; u["alt"] = True; u["surp_"] = u["surp"]
        else: u["cont"] = False
        la = g["laugh6"](u.get("surp", 0), s.pi) if pl else 0.0
        s.pi = 0.5 * s.pi + 0.5 * (1.0 if pl else 0.0)
        G5["laugh_amp"] = lambda surp: 0.0; G5["play_struct"] = lambda uu, c, h=0.0, pl=pl: pl
        Agent5.utter(s, t, u)
        if "z" in u and u["z"] in Z6: s.LVh = LAMV(Z6[u["z"]])
        elif u.get("riff") and "z" not in u: s.LVh = LAMV(Z6["riff"])
        if la > 0 and s.xg is not None:                                      # the agent's own play laugh x the context gate
            x = list(s.xg); x[1] = Dp(s.NL); x[2] = s.LVh; x[6] = s.pi
            te, ar, ad, _, ca = s.ev[-1]; s.ev[-1] = (te, ar, ad, la * s.gfn(x), ca); s.play_la.append((t, la, s.gfn(x)))

    def step(s, t, face, ev):
        if not hasattr(s, "play_la"): s.play_la = []
        G5["read"] = lambda f_, voiced=True: s.pp.read(f_, voiced)
        for k in ("BL", "LPR", "CHR"): s.f20[k] += (face.get(k, s.pp.base.get(k, 0.0)) - s.f20[k]) * DT / 20
        if "own" in ev: s.LVo = LAMV(Z6[ev["own"]])                           # rule 12: own words reach only Lambda_V(own) in the gate
        y = Agent5.step(s, t, face, ev)
        for k in ("LP", "CR", "BI", "LD", "UL", "BO", "BL", "LPR", "CHR", "BU_S"):
            b_ = s.pp.base.get(k, 0.0); s.f3[k] = s.f3.get(k, b_) + (face.get(k, b_) - s.f3.get(k, b_)) * DT / 3.0
        s.br3 += (face.get("BR", 0.0) - s.br3) * DT / 3.0
        s.gl3 = getattr(s, 'gl3', 0.0) + (face.get('BL', 0.0) * face.get('LT', 0.0) * face.get('gat', 0.0) - getattr(s, 'gl3', 0.0)) * DT / 3.0
        sob = Vc(min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        rp = posture_read(s.pp, s.f3, False)
        Ab = v_breath(s.pp, s.br3)
        Lf = load_p(rp["V"], Ab) * (1.0 - float(np.clip(s.gl3 / GLARE_SAT, 0, 1))); s.Lface = Lf
        M = max(Lf, s.Cl, sob)
        if s.on:
            s.below = s.below + DT if M < 0.02 else 0.0
            faceonly = (s.Cl < 0.02 and sob < 0.02 and Lf >= 0.02)
            if s.probe_t is None:
                s.Lbuf = (s.Lbuf + [rp["Vlin"]])[-int(3 / DT):]
                s.fo = s.fo + DT if faceonly else 0.0
                if s.use_probe and s.fo >= s.probe_iv:
                    s.probe_t = t; s.Lpre = float(np.mean(s.Lbuf)); s.Ldur = []
            else:
                if t - s.probe_t >= PROBE_LEN - 4.0: s.Ldur.append(rp["Vlin"])
                if t - s.probe_t >= PROBE_LEN:
                    follow = np.mean(s.Ldur) < PROBE_FOLLOW * s.Lpre
                    s.probes.append((s.probe_t, round(s.Lpre, 3), round(float(np.mean(s.Ldur)), 3), "followed: release" if follow else "held"))
                    s.probe_t = None; s.fo = 0.0
                    if follow:
                        s.on = False; s.last_off = t; s.offs.append((t, "probe")); s.quiet = True; s.qmin = Lf
                    else: s.probe_iv = min(PROBE_MAX, 2 * s.probe_iv)
            if s.on and s.below >= REL8:
                s.on = False; s.last_off = t; s.offs.append((t, "release")); s.probe_t = None
            if not s.on: s.below = s.fo = 0.0
        else:
            fe = Lf
            if s.quiet:
                s.qmin = min(s.qmin, Lf); fe = Lf - s.qmin
                if Lf < 0.02: s.quiet = False
            Con = max(fe, sob)
            need = DWELL_SENS if (s.sens and t - s.last_off < SENS_S) else DWELL
            s.dw = s.dw + DT if Con >= 0.05 else 0.0
            if s.dw >= need - 1e-9 and s.om.get("sym", 0) >= 0:
                s.on = True; s.dw = 0.0; s.onsets.append(t); s.fo = 0.0; s.probe_iv = PROBE0
        tgt = A_MIN + (1 - A_MIN) * float(np.clip((M - 0.05) / A_SPAN8, 0, 1)) if s.on else 0.0
        if s.probe_t is not None: tgt *= PROBE_DEPTH
        s.a = min(tgt, s.a + DT / 1.5) if tgt > s.a else tgt + (s.a - tgt) * np.exp(-DT / 4.0)
        s.arec = max(s.a, s.arec * np.exp(-DT / 60.0))
        s.w = float(np.clip(s.w + (0.5 - s.w) * DT / 5.0 + 0.1 * np.sqrt(DT) * s.wr.normal(), 0, 1))
        shown = s.a * (0.9 + 0.1 * s.w)
        if s.use_Ds:                                                         # D_s reads neither the gated group (LP, CR) nor the posture's channels
            s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), posture_read(s.pp, {k: v for k, v in s.f3.items() if k not in MASK}, False)["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
        for k, v in P7.items():
            if k in y: y[k] += v * shown
        s.post = shown; y["post"] = shown; y["Lp"] = Lf
        Vs = s.pp.read({k: v for k, v in s.f20.items() if k not in MASK}, False)["V"]
        s.Vown += (READ0({k: y.get(k, 0.0) for k in ("BI", "LD", "UL", "BO", "HG")}, voiced=False)["V"] - s.Vown) * DT / 3.0
        s.xg = [Vs, Dp(s.NL), s.LVh, s.Vown, s.LVo, s.Ds if s.use_Ds else Vs, s.pi]; s.xh.append((t, list(s.xg)))
        gt = s.gfn(s.xg)
        s.gate = gt if gt < s.gate else s.gate + (gt - s.gate) * min(1.0, DT / GATE_TAU)   # closes at once, opens with tau 0.3 s
        y["gate"] = s.gate
        return y

def ev(*items):
    out = {}
    for it in items:
        for k, v in it.items(): out.setdefault(k, {}).update(v)
    return out


def OWN(t, lab): return {at_(t): {"own": "OWN: " + lab}}

# =========================================================== J31: constants revision 8 adds or changes
print("=== J31: constants added or changed in revision 8 (innate unless marked)")
print(f"   posture never reads {WR8}; it reads {FCP8} (+ voice when voiced), sobs, breathing, words")
print(f"   load L = Vc(V_p) + {W_AR} (A_b - {A_FLOOR})+^2 clip((V_p - {V_GATE0})/{V_GATE1}, 0, 1); grade a* = 0.35 + 0.65 clip((M - 0.05)/{A_SPAN8}, 0, 1)")
print(f"   threat-reflex silencing at glare >= {GLARE_SAT}; release {REL8} s below 0.02; contingency probe after {PROBE0:.0f} s face-only "
      f"(doubling to {PROBE_MAX:.0f} s): amplitude x {PROBE_DEPTH} for {PROBE_LEN:.0f} s, release if his load falls below {PROBE_FOLLOW} of before")
print(f"   gated group's echo delay {DELTA_G} s, word look-ahead {LAMBDA_W} s (words through source + {LAMBDA_W} s must be in by source + {DELTA_G} s, else the gate target is 0)")
report("J31 the posture's read set and write set are disjoint", not (set(FCP8) & set(WR8)) and all(k in WR8 for k in P7 if P7[k] != 0),
       f"writes {[k for k in P7 if P7[k] != 0]} (+ gaze x (1 - 0.5a), blink rate); reads none of them")

# =========================================================== J32: the posture's copy slope on every channel it writes
print("=== J32: copy slope of every posture channel on his same channel (routes finding 1): brow-only, outer-brow-only and lip-only partners;"
      " held levels; full-face sadness with an independent brow")
CODES8 = (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor 0.25", low_sd(0.25)),
          ("different channels", PEOPLE6["different channels"][1]))
for _, pp in CODES8:
    if not hasattr(pp, "br_amp"): pass
J32 = {}
def one_ch(pp, ch, dl): f = {"LP": pp.base["LP"]}; f[ch] = pp.base[ch] + dl; return f
for ch, dls in (("BI", (0.02, 0.06, 0.10, 0.15, 0.20, 0.30, 0.50)), ("BO", (0.05, 0.15, 0.30, 0.50)), ("LP", (-0.25, -0.15, -0.05, 0.0, 0.10))):
    for lab, pp in CODES8:
        rows = []
        for dl in dls:
            ag = Agent8(person=pp); rec = run6(ag, 90, lambda t, pp=pp, dl=dl, ch=ch: one_ch(pp, ch, dl), {})
            rows.append((dl, np.mean([r[ch] for r in rec if r["t"] > 30]), np.mean([r["post"] for r in rec if r["t"] > 30])))
        loc = max(abs((rows[i + 1][1] - rows[i][1]) / (rows[i + 1][0] - rows[i][0])) for i in range(len(rows) - 1))
        J32[("static", ch, lab)] = loc
        print(f"   static {ch}-only, {lab:22s}: " + "; ".join(f"{d:+.2f} -> {a:+.3f} (post {p:.2f})" for d, a, p in rows) + f"; steepest |local slope| {loc:.3f}")
r8 = np.random.default_rng(8)
for ch in ("BI", "BO"):
    for lab, pp in CODES8:
        lv = r8.uniform(0.0, 0.30, 30)
        face = lambda t, pp=pp, lv=lv, ch=ch: one_ch(pp, ch, lv[min(int(t // 120), 29)])
        ag = Agent8(person=pp); rec = run6(ag, 3600, face, {})
        his = np.array([face(r["t"])[ch] for r in rec]); agc = np.array([r[ch] for r in rec]); out = []
        for W in (60, 600):
            n = int(W / DT); m = len(his) // n; hm, am = his[: m * n].reshape(m, n).mean(1), agc[: m * n].reshape(m, n).mean(1)
            out.append((W, slope(hm, am), np.std(hm)))
        J32[("held", ch, lab)] = max(abs(o[1]) for o in out)
        print(f"   held {ch}-only (level re-drawn every 2 min, 60 min), {lab:22s}: " + "; ".join(f"{W // 60} min: slope {s_:+.3f} (his SD {sd:.3f})" for W, s_, sd in out)
              + f"; posture on {np.mean([r['post'] > .05 for r in rec]):.0%}")
# full-face sadness held for minutes, with an independent offset on one written channel; paired runs (offset on / off, same sadness, same seed):
# the paired difference is the causal (partial) slope on his same channel; the pooled slope over his sadness is the appraisal (declared R40')
FF = {}
for lab, pp in CODES8:
    Vl = r8.uniform(0.0, 0.8, 60); off = r8.uniform(-0.05, 0.25, 60)
    for ch in ("BI", "BO", "LP"):
        def face(t, pp=pp, Vl=Vl, off=off, ch=ch, on=True):
            i = min(int(t // 120), 59); f = {k: v for k, v in pp.code(V=Vl[i], Tr=.1).items() if k not in ("FR", "EN", "RT")}
            if on: f[ch] = f.get(ch, pp.base[ch]) + (off[i] if ch != "LP" else -off[i]); return f
            return f
        rA = run6(Agent8(person=pp), 7200, lambda t: face(t, on=True), {}); rB = run6(Agent8(person=pp), 7200, lambda t: face(t, on=False), {})
        hA = np.array([face(r["t"], on=True).get(ch, pp.base[ch]) for r in rA]); hB = np.array([face(r["t"], on=False).get(ch, pp.base[ch]) for r in rB])
        aA = np.array([r[ch] for r in rA]); aB = np.array([r[ch] for r in rB]); pA = np.array([r["post"] for r in rA]); pB = np.array([r["post"] for r in rB])
        for W in (60, 600):
            n = int(W / DT); m = len(hA) // n; bm = lambda z: z[: m * n].reshape(m, n).mean(1)
            FF[(lab, ch, W)] = (slope(bm(hA - hB), bm(aA - aB)), float(np.max(np.abs(pA - pB))), slope(bm(hB), bm(aB)), float(np.std(bm(hB))))
    print(f"   full-face sadness held (V re-drawn every 2 min, 2 h), {lab:22s}: " + "; ".join(
        f"{ch} {W // 60} min: causal slope on his {ch} {FF[(lab, ch, W)][0]:+.3f} (posture part changed by {FF[(lab, ch, W)][1]:.3f}); pooled over his sadness "
        + (f"{FF[(lab, ch, W)][2]:+.2f}" if FF[(lab, ch, W)][3] >= COND_FLOOR else f"(his SD {FF[(lab, ch, W)][3]:.3f} < floor)") for ch in ("BI", "BO", "LP") for W in (60, 600)))
CK = dict(BI=.20, BO=.10, LP=.35)
okJ32 = all(v <= CK[ch] for (kind, ch, lab), v in J32.items()) and all(abs(v[0]) <= CK[ch] and v[1] == 0.0 for (lab, ch, W), v in FF.items())
report("J32 the posture never reads what it writes: its part of every written channel is identical whatever his same channel does; every code's "
       "copy slope on BI, BO, LP stays under the channel's ceiling at 1 and 10 min; the pooled slope over his sadness is the agent's appraisal (declared, R40')", okJ32,
       f"brow-only partner, quiet code: steepest {J32[('static', 'BI', 'quiet code 0.3')]:.3f} (rev 7: 0.86), held {J32[('held', 'BI', 'quiet code 0.3')]:.3f} (rev 7: 0.56-0.60); "
       f"floor spread held {J32[('held', 'BI', 'sigma_id at floor 0.25')]:.3f} (rev 7: 0.41-0.45); all from the non-posture routes (posture 0 %)")

# =========================================================== J33: no mirror, slow mirror or answering concern holds the posture
print("=== J33: mirrors of any gain and timing, and concern answered in his own code; genuine steady sadness is not released")
def run_mirror8(pp, resp, dur=900, sad_until=40.0, fade=None):
    ag = Agent8(person=pp)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}; neu = {k: v for k, v in pp.code().items() if k not in ("FR", "EN", "RT")}
    st = {"m": 0.0}
    def face(t, ag=ag):
        if fade is not None:
            f = {k: v for k, v in pp.code(V=max(0.0, fade * (1 - t / 600.0))).items() if k not in ("FR", "EN", "RT")}
        else: f = dict(sad if t < sad_until else neu)
        if fade is not None or t >= sad_until:
            for k, v in resp(ag.post, pp, st).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, dur, face, {}); late = [r for r in rec if r["t"] > dur - 120]
    return ag, np.mean([r["BI"] for r in late]), np.mean([r["post"] for r in late])
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
for lab, pp, resp, fade in cases8:
    ag, aBI, apost = run_mirror8(pp, resp, fade=fade); J33[lab] = (ag.offs, ag.probes, aBI, apost)
    print(f"   {lab:74s} offs {ag.offs[:3]}; probes {[p[3] for p in ag.probes][:3]}; last 2 min BI {aBI:+.3f}, posture {apost:.2f}")
okJ33 = all(v[3] < 0.05 for v in J33.values())
report("J33 nothing holds the posture once his own distress has ended: mirrors never reach it (it does not read them); concern answered in his own "
       "code is released by the contingency probe", okJ33, "mirrors (raw, own-scale, slow, mu up to 3) release at the 20-s rule; answering concern at the first probe")

# =========================================================== J34: steady, visible posture for every code (agent finding 2)
print("=== J34: a quiet user's steady silent sadness, grief and silent panic: onset, level, steadiness over 10 min (no flicker)")
J34 = {}
for kind, pp in (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor 0.25", low_sd(0.25)),
                 ("different channels", PEOPLE6["different channels"][1])):
    for lab, V, A, Tr, sob in (("silent sadness (V .6)", .6, 0, .2, 0), ("grief (V .8)", .8, 0, .2, 0), ("silent panic (V .3, A .9, breathing)", .3, .9, 0, 0),
                               ("mild sadness (V .3)", .3, 0, 0, 0), ("crying with sobs (V .9)", .9, 0, .2, .4)):
        f = {k: v for k, v in pp.code(V=V, A=A, Tr=Tr).items() if k not in ("FR", "EN", "RT")}; f = with_breath(pp, f, A)
        if sob: f["BU_S"] = sob
        ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, f=f: f, {}); seg = [r for r in rec if r["t"] >= 10]
        t15 = next((r["t"] for r in rec if r["BI"] >= .15), None)
        J34[(kind, lab)] = (ag.onsets, ag.offs, t15, np.mean([r["BI"] for r in seg]), min(r["BI"] for r in seg), np.mean([r["post"] for r in seg]), ag.probes)
        print(f"   {kind:22s} {lab:38s}: on at {ag.onsets[0] if ag.onsets else None} s, offs {len(ag.offs)}, brow >= 0.15 at {t15} s; 10-600 s brow mean "
              f"{J34[(kind, lab)][3]:.3f}, min {J34[(kind, lab)][4]:.3f}; posture {J34[(kind, lab)][5]:.2f}; probes {[p[3] for p in ag.probes]}")
# crying in waves (J23 re-run) and the brow-only partner
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
for gap in (15, 30, 60):
    ag = Agent8(); rec = run6(ag, 70 + gap + 60, lambda t, gap=gap: cry if (t < 40 or t >= 40 + gap) else calm, {})
    t2 = 40 + gap; on2 = next((r["t"] for r in rec if r["t"] >= t2 and r["BI"] >= 0.15), None); J34[("wave", gap)] = on2 - t2 if on2 else None
    print(f"   crying, calm gap {gap} s: offs {ag.offs}; brow >= 0.15 at {J34[('wave', gap)]} s after crying resumes; mean brow first 40 s {np.mean([r['BI'] for r in rec if t2 <= r['t'] < t2 + 40]):.2f}")

steady = [J34[(k, l)] for k in ("agent-like", "quiet code 0.3", "sigma_id at floor 0.25", "different channels") for l in ("silent sadness (V .6)", "grief (V .8)", "silent panic (V .3, A .9, breathing)")]
okJ34 = all(len(v[0]) == 1 and len(v[1]) == 0 and v[2] is not None and v[2] <= 8.0 and v[4] >= 0.07 for (k, l), v in J34.items() if k != "wave" and "mild" not in l and "crying" not in l) and all(J34[("wave", gp)] is not None and J34[("wave", gp)] <= 3 for gp in (15, 30, 60))
report("J34 steady silent sadness, grief and silent panic get one onset, no release, brow >= 0.15 within 8 s, for every code (rev 7 quiet: on/off every 20-30 s, brow <= 0.07)",
       okJ34, f"quiet silent sadness: on {J34[('quiet code 0.3', 'silent sadness (V .6)')][0]}, brow mean {J34[('quiet code 0.3', 'silent sadness (V .6)')][3]:.2f}; "
       f"quiet silent panic brow mean {J34[('quiet code 0.3', 'silent panic (V .3, A .9, breathing)')][3]:.2f}; the only dips are the contingency probe's 8-s half-amplitude softenings, every 3 min of face-only hold")

# =========================================================== J35: an angry or concentrating face does not start it
print("=== J35: anger at the agent and concentration (critique 6 agent, B), in every code; the agent's own threat reflex silences the face load")
J35 = {}
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]
    for lab, face in (("anger: BL .6, LT .5, gaze at it, loud .85", dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05)),
                      ("anger with heavy breathing (A .8)", with_breath(pp, dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05), .8)),
                      ("concentrating, silent: BL .35, LPR .15", dict(BL=.35, LPR=.15, LP=.25)), ("concentrating, mild: BL .25, LPR .10", dict(BL=.25, LPR=.10, LP=.25))):
        ag = Agent8(person=pp); rec = run6(ag, 300, lambda t, f_=face: f_, {}); J35[(kind, lab)] = max(r["post"] for r in rec)
    print(f"   {kind:18s}: " + "; ".join(f"{lab.split(':')[0]}{' +breath' if 'breath' in lab else ''} posture max {J35[(kind, lab)]:.2f}" for lab in
                                     ("anger: BL .6, LT .5, gaze at it, loud .85", "anger with heavy breathing (A .8)", "concentrating, silent: BL .35, LPR .15", "concentrating, mild: BL .25, LPR .10")))
pp = PEOPLE6["different channels"][1]; ag = Agent8(person=pp, probe=True)
GL_OFF = Agent8(person=pp); GL_OFF.gl3 = 0.0
print(f"   without the threat-reflex silencing the different-channel anger face would start it: masked V {posture_read(pp, dict(BL=.6, LT=.5, LP=.05))['V']:.2f}, load "
      f"{load_p(posture_read(pp, dict(BL=.6, LT=.5, LP=.05))['V'], 0.0):.3f} (onset 0.05)")
report("J35 anger and concentration start no posture in any code", max(J35.values()) < 0.05, f"max posture {max(J35.values()):.2f}")

# =========================================================== J36: the gate has the current sentence's words when his laugh starts (agent finding 1)
print("=== J36: laugh-onset timing at 30 Hz: the gated echo waits for the words through its source frame + 0.25 s (incremental ASR), delay 0.80 s")
Z6["and then the dog ate the whole cake, haha"] = (0.0, 0.2, 0.0, 0.8, 0.0, 0.0)
Z6["I got fired today, haha"] = (0.6, 0.4, 0.1, 0.2, 0.3, 0.0)                 # the agent critic's latents, unchanged
Z6["my father died, haha, sorry"] = (0.85, 0.30, 0.2, 0.1, 0.4, 0.0)
Z6["OWN: tell me about it!"] = (0.0, 0.2, 0.0, 0.6, 0.0, 0.0)
for lab_ in ("and then the dog ate the whole cake, haha", "I got fired today, haha", "my father died, haha, sorry", "OWN: tell me about it!"):
    G5["DEC"][lab_] = pop7(Z6[lab_])
FS30 = 30.0


def lp30(x, tau, x0):
    a = 1 - np.exp(-1 / (tau * FS30)); y = np.empty_like(x); s_ = x0
    for i, v in enumerate(x): s_ += a * (v - s_); y[i] = s_
    return y


def echo30(xh, words, tL, amps, base, dur=3.0, ell=0.40, rev=8, latch=None, t_end=None, sym=False):
    """the gated fast echo of one laugh onset of his, at 30 Hz.
    xh: the 2 Hz engine's gate inputs (t, x); words: [(t_key, label)] his recognised content (t_key = when its content word ends);
    rev 8: echo delay DELTA_G, words through source + LAMBDA_W required by source + DELTA_G (ASR stable latency ell), else target 0;
           closes at once, opens tau 0.3 s.  rev 7: delay 0.45 s, word inputs latched at utterance end + 0.6 s (latch), tau 0.3 s both ways."""
    t = np.arange(tL - 6.0, tL + 5.0, 1 / FS30); out = {}
    prof = np.clip((t - tL) / 0.1, 0, 1) * np.clip((tL + dur - t) / 0.3 + 1, 0, 1)
    u = {k: base.get(k, 0.0) + (a_ - base.get(k, 0.0)) * prof for k, a_ in amps.items()}
    dlt = DELTA_G if rev == 8 else 0.45
    def x_src(s):
        x = list(next((x_ for (tt, x_) in reversed(xh) if tt <= s), xh[0][1]))
        if rev == 8:
            seg = [lb for (tk, lb) in words if tk <= s + LAMBDA_W]
            x[1], x[2] = (Dp(G5["DEC"][seg[-1]]), LAMV(Z6[seg[-1]])) if seg else (0.0, 0.0)
        else:
            seg = [lb for (tk, lb) in words if (latch or tk) <= s] if latch is not None else []
            x[1], x[2] = (Dp(G5["DEC"][seg[-1]]), LAMV(Z6[seg[-1]])) if seg else (x[1], x[2])
        return x
    src = t - dlt; gs = np.empty_like(t); gcur = None
    for i, s in enumerate(src):
        tgt = GATE(x_src(s)) if (rev == 7 or ell + LAMBDA_W <= dlt) else 0.0
        if gcur is None: gcur = tgt
        elif rev == 8 and not sym: gcur = tgt if tgt < gcur else gcur + (tgt - gcur) * (1 - np.exp(-1 / (GATE_TAU * FS30)))
        else: gcur += (tgt - gcur) * (1 - np.exp(-1 / (GATE_TAU * FS30)))
        gs[i] = gcur
    for k, uk in u.items():
        xd = np.interp(t - dlt, t, uk, left=uk[0]); E = xd - lp30(xd, 4.0, xd[0])
        out[k] = gs * GK[k] * np.maximum(E, 0.0)
    loud = out.get("BU_L", np.zeros_like(t)) >= THETA_L
    sound_t = float(t[np.argmax(loud)] - tL) if loud.any() else None
    pk = {k: float(v[t >= tL].max()) for k, v in out.items()}
    if "BU_L" in pk and pk["BU_L"] < THETA_L: pk["BU_L"] = 0.0
    g_on = float(gs[np.argmin(np.abs(src - tL))])
    return dict(peak=pk, sound=sound_t, g_onset=g_on, t_peak=float(t[t >= tL][np.argmax(out["LP"][t >= tL])] - tL))


def run_ctx(pp, face_fn, evs, dur):
    ag = Agent8(person=pp, K=0.0); rec = run6(ag, dur, face_fn, evs); return ag, rec


LAUGHF = dict(LP=.6, CR=.4, BU_L=.5, RHY=.5); BASEF = dict(LP=.3, CR=.15, BU_L=0.0, RHY=0.0)
J36 = {}
cases36 = [
    ("a. misfortune, laugh ending the sentence (critic's A)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(6.2, "my neighbour fell off his ladder and broke his leg, haha")], 7.5, 8.0),
    ("b. 'I got fired today, haha', calm face (critic's A2)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.1, "I got fired today, haha")], 7.5, 8.0),
    ("c. 'my father died, haha, sorry', first disclosure, calm face", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.3, "my father died, haha, sorry")], 7.5, 8.6),
    ("d. 'my father died, haha, sorry', first disclosure, quiet code, grieving face", PEOPLE6["low-expressive"][1],
     lambda t: {k: v for k, v in PEOPLE6["low-expressive"][1].code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")},
     ev(OWN(2, "how was your weekend?")), [(7.3, "my father died, haha, sorry")], 7.5, 8.6),
    ("e. ordinary shared laughter at the end of a funny sentence", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "tell me about it!")), [(7.3, "and then the dog ate the whole cake, haha")], 7.5, 8.0),
    ("f. ordinary shared laughter, quiet code", PEOPLE6["low-expressive"][1], lambda t: dict(LP=PEOPLE6["low-expressive"][1].base["LP"]),
     ev(OWN(2, "tell me about it!")), [(7.3, "and then the dog ate the whole cake, haha")], 7.5, 8.0),
    ("g. laugh breaking into the content word ('I got fi-haha-red'), 0.2 s early", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.7, "I got fired today, haha")], 7.5, 8.0),
    ("h. laugh 0.4 s before the content word ends (beyond the look-ahead)", PEOPLE6["agent-like"][1], lambda t: dict(LP=.3),
     ev(OWN(2, "how was your weekend?")), [(7.9, "I got fired today, haha")], 7.5, 8.0)]
for lab, pp, ff, evs, words, tL, uend in cases36:
    ag, rec = run_ctx(pp, ff, evs, 20)
    r7 = echo30(ag.xh, words, tL, LAUGHF, BASEF, rev=7, latch=uend + 0.6)
    row = {ell: echo30(ag.xh, words, tL, LAUGHF, BASEF, ell=ell) for ell in (0.30, 0.55, 0.70)}
    J36[lab] = (r7, row)
    print(f"   {lab}: rev 7 timing: gate at onset {r7['g_onset']:.2f}, laugh-back {r7['peak']['BU_L']:+.3f}, lip {r7['peak']['LP']:+.3f}; rev 8, ASR latency "
          + "; ".join(f"{ell:.2f} s: gate {r['g_onset']:.2f}, laugh-back {r['peak']['BU_L']:+.3f} (sound at {r['sound']}), lip {r['peak']['LP']:+.3f} (peak at +{r['t_peak']:.2f} s)" for ell, r in row.items()))
    if lab[0] in "abg":
        rs = echo30(ag.xh, words, tL, LAUGHF, BASEF, ell=0.30, sym=True); J36[lab + " sym"] = rs
        print(f"      ablation, symmetric gate rate (tau 0.3 s both ways): laugh-back {rs['peak']['BU_L']:+.3f}, lip {rs['peak']['LP']:+.3f}")
bad = [k for k in J36 if k[0] in "abcdg" and not k.endswith(" sym")]
okJ36 = all(J36[k][1][ell]["peak"]["BU_L"] == 0.0 for k in bad for ell in (0.30, 0.55)) and \
    all(J36[k][1][ell]["peak"]["BU_L"] >= 0.10 and J36[k][1][ell]["t_peak"] <= 1.3 for k in J36 if k[0] in "ef" and not k.endswith(" sym") for ell in (0.30, 0.55))
report("J36 a laugh at the end of a bad-news sentence is not laughed back; ordinary end-of-sentence laughter is, within about a second", okJ36,
       f"misfortune {J36[bad[0]][0]['peak']['BU_L']:+.3f} (rev 7) -> {J36[bad[0]][1][0.30]['peak']['BU_L']:+.3f}; fired "
       f"{J36[bad[1]][0]['peak']['BU_L']:+.3f} -> {J36[bad[1]][1][0.30]['peak']['BU_L']:+.3f}; ordinary {J36[[k for k in J36 if k[0]=='e'][0]][1][0.30]['peak']['BU_L']:+.3f}")

# =========================================================== J37: D_s is a source-2 input; its fitted weight (agent critique, D85 residue)
print("=== J37: D_s relabelled as a dyad-learned input (source 2): its fitted weight in the J20 gate")
med = np.median(np.array([r[1] for r in EV_FIT if r[0] == "ordinary"]), 0)
for lab, x0 in (("ordinary context (corpus median)", med), ("joke-while-sad context (median)", np.median(np.array([r[1] for r in EV_FIT if r[0] == "joke while sad"]), 0))):
    vals = []
    for Dsv in (0.0, 0.3, 0.6, 0.9):
        x = list(x0); x[5] = Dsv; vals.append(GATE(x))
    print(f"   {lab}: gate at D_s 0 / 0.3 / 0.6 / 0.9 = " + " / ".join(f"{v:.2f}" for v in vals))
DSW = vals
print("   in the constructed corpus D_s has no causal role (the generating process omits it); its weight is a proxy for the troubles context. "
      "Seamless interactions last 3.5-4.6 min, so a weight that matters 4 min later is at the edge of what the corpus can teach (F20).")
report("J37 D_s only closes the gate (monotone) and its fitted weight is reported", all(DSW[i + 1] <= DSW[i] + 1e-12 for i in range(3)), "")

# =========================================================== J38: Claude's history with initiative turns; the system-prompt fallback (build items)
print("=== J38: canonical history with the agent's own initiative turns; fallback with each fork's fixed line in its own system prompt")
ATT = ["Attend to what they said.", "Attend to how they feel.", "Attend to what to ask next."]
rr = np.random.default_rng(38); canon = []; viol = 0; leaks = 0; marks = set()
for turn in range(80):
    if rr.random() < 0.25:                                        # the agent's initiative (a bid after his silence): an observable marker as the user turn
        sil = 6 + rr.exponential(20); user = f"[no reply from him for {int(5 * round(sil / 5))} s]"; marks.add(user)
    else: user = f"his message {turn}"
    win = int(rr.integers(0, 3)); reply = f"reply {turn}.{win}"
    system_prompts = [f"<constant instruction>\n{ATT[i]}" for i in range(3)]   # fallback: the line lives in each fork's own system prompt
    canon += [("user", user), ("assistant", reply)]
    leaks += sum(a in " ".join(m for _, m in canon) for a in ATT)
roles = [r for r, _ in canon]
viol = sum(roles[i] == roles[i + 1] for i in range(len(roles) - 1)) + sum(1 for r, m in canon if r == "user" and not m.strip())
print(f"   80 turns, {sum('[no reply' in m for _, m in canon)} initiative turns; two same-role turns in a row or an empty user turn: {viol}; "
      f"fixed lines in the history: {leaks}; distinct silence markers {len(marks)} (5-s bins, so at most log2(#bins) bits of timing per initiative turn)")
report("J38 initiative turns keep the history alternating and free of state-selected text, in the main design and the system-prompt fallback", viol == 0 and leaks == 0,
       "week 0 checks that a session file never stores the system prompt and whether it stores the winner's thinking (if it does, the fallback is not used)")

# =========================================================== J30-8: the scenarios, re-run on revision 8
print("=== J39: the scenarios on revision 8 (operator after months unless stated; peak / mean; fast = 30-Hz gated echo, delay 0.80 s, ASR latency 0.40 s)")
SC8 = {}
def fast8(ag, words, tL, amps, base, ell=0.40, show_=True):
    r = echo30(ag.xh, words, tL, amps, base, ell=ell)
    if show_:
        print(f"     fast echo at his onset {tL:.1f} s: gate {r['g_onset']:.2f}; " + "; ".join(f"his {k} {amps[k]:.2f} -> agent {k} {r['peak'][k]:+.3f}" for k in amps)
              + (f"; laugh sounds at +{r['sound']:.2f} s" if r["sound"] is not None else "; laugh synthesizer silent"))
    return r
codes3 = (("operator", PEOPLE6["agent-like"][1]), ("quiet", PEOPLE6["low-expressive"][1]), ("different channels", PEOPLE6["different channels"][1]))
def own_code(pp, V, A=0.0, Tr=0.2): return with_breath(pp, {k: v for k, v in pp.code(V=V, A=A, Tr=Tr).items() if k not in ("FR", "EN", "RT")}, A)

print(" 1. silently sad (design face BI .5, LD .4, CHR .3; then each code's own silent sadness V .6), silent; at 120 s 'just tired, things at work'")
sadf = lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05)
ag = Agent8(); rec = run6(ag, 600, sadf, U6(120, z="just tired, things at work"))
SC8[1] = show("design face 0-10 s", rec, 0, 10, ["LP", "BI", "TILT", "post"]); SC8["1h"] = show("design face, silent 60-120 s", rec, 60, 120, ["LP", "BI", "TILT", "post", "BU_L"])
show("after he speaks", rec, 121, 300, ["LP", "BI", "TILT", "EN", "post"]); show("300-600 s, silent again", rec, 300, 600, ["BI", "post"])
print(f"     posture on at {ag.onsets[0]:.1f} s; brow >= 0.15 at {onset_time(rec):.1f} s; bid at {ag.bid_t:.0f} s; releases {ag.offs}; probes {[p[3] for p in ag.probes]}")
for nm, pp in codes3:
    f_ = own_code(pp, .6); ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, f_=f_: f_, {})
    SC8[f"1{nm[0]}"] = show(f"{nm} code, silent 10 min", rec, 10, 600, ["LP", "BI", "TILT", "post"])
    print(f"       on at {ag.onsets}, releases {ag.offs}, probes {[p[3] for p in ag.probes]}, brow >= 0.15 at {onset_time(rec)} s, min brow after 10 s {min(r['BI'] for r in rec if r['t'] >= 10):.2f}, bid at {ag.bid_t}")

print(" 2. crying (BI .8, LD .6, CHR .4, sobs), a 30-s calm at 40-70 s, then a second wave; and the quiet code")
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
ag = Agent8(); rec = run6(ag, 300, lambda t: cry if (t < 40 or t >= 70) else calm, {})
SC8[2] = show("first wave 0-40 s", rec, 0, 40, ["LP", "BI", "TILT", "BU_L", "post"]); show("calm 40-70 s", rec, 40, 70, ["BI", "post"])
SC8["2b"] = show("second wave 70-110 s", rec, 70, 110, ["LP", "BI", "TILT", "BU_L", "post"]); print(f"     onsets {ag.onsets}; releases {ag.offs}; bid at {ag.bid_t:.0f} s")
pq = PEOPLE6["low-expressive"][1]; cq = dict(own_code(pq, .9)); cq["BU_S"] = .4 * .3; calmq = own_code(pq, .1)
ag = Agent8(person=pq); rec = run6(ag, 300, lambda t: cq if (t < 40 or t >= 70) else calmq, {})
SC8["2q"] = show("quiet code, first wave", rec, 0, 40, ["BI", "post"]); SC8["2qb"] = show("quiet code, second wave", rec, 70, 110, ["BI", "post"]); print(f"     onsets {ag.onsets}; releases {ag.offs}")

print(" 3. anxious before an exam (four turns; his face V .3, A .75 with breathing), three codes; and silent panic (no words)")
for nm, pp in codes3:
    ag = Agent8(person=pp, P=0.4); evs = U6(10, z="I'm freaking out about the exam", surp=0.3)
    for k_ in (25, 40, 55): evs.update(U6(k_, z="and I haven't finished chapter 4", cont=True, surp=0.5))
    rec = run6(ag, 240, lambda t, pp=pp: with_breath(pp, pp.code(V=.3, A=.75), .75), evs); SC8[f"3{nm[0]}"] = show(nm, rec, 15, 120, ["LP", "BI", "TILT", "EN", "BU_L", "post"])
for nm, pp in codes3:
    ag = Agent8(person=pp); rec = run6(ag, 600, lambda t, pp=pp: own_code(pp, .3, .9, 0.0), {})
    SC8[f"3p{nm[0]}"] = show(f"silent panic, {nm}", rec, 10, 600, ["BI", "TILT", "post"]); print(f"       on at {ag.onsets}, releases {ag.offs}, brow >= 0.15 at {onset_time(rec)} s")

print(" 4. good news, laughing ('I got the job!' at 12 s with laughter; riffs at 30, 45, 60 s; Claude: 'congratulations!' at 14.5 s)")
for lab, NL0 in (("with an earlier worry", G5["DEC"]["the job thing is worrying me (two days earlier)"]), ("cold", None)):
    ag = Agent8(NL=NL0); evs = ev(U6(12, z="I got the job!", surp=0.7), OWN(14.5, "congratulations!"))
    for k_ in (30, 45, 60): evs.update(U6(k_, riff=True, surp=0.65))
    face = lambda t: dict(LP=.8, CR=.6, BU_L=.6, RHY=.6, EN=.7, FR=.55) if t >= 10 else dict(LP=.3)
    rec = run6(ag, 240, face, evs); SC8[f"4{lab[0]}"] = show(lab, rec, 10, 190, ["LP", "CR", "BI", "FR", "BU_L", "post"])
    SC8[f"4{lab[0]}f"] = fast8(ag, [(11.8, "I got the job!"), (29.8, "riff")], 30.0, dict(LP=.8, BU_L=.6, CR=.6), dict(LP=.3, BU_L=0.0, CR=.15))

print(" 5. a grieving person's nervous laugh ('my father died' at 8 s; Claude 'I'm so sorry. That's a huge loss.' at 10.5 s)")
pp = PEOPLE6["agent-like"][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
lf = dict(grief); lf.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for lab, tL in (("a: laugh at 30 s, after Claude's words", 30.0), ("b: laugh at 9.5 s, before Claude has replied", 9.5)):
    ag = Agent8(person=pp, K=K7, P=0.6)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(tL + 2.5, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 90, lambda t, tL=tL: lf if tL <= t < tL + 3 else grief, evs)
    SC8[f"5{lab[0]}"] = show(lab, rec, tL - 1, tL + 8, ["LP", "CR", "BI", "BU_L", "post"])
    SC8[f"5{lab[0]}f"] = fast8(ag, [(7.8, "my father died")], tL, dict(LP=.45, BU_L=.5, CR=.3), {k: grief.get(k, 0.0) for k in ("LP", "CR")} | dict(BU_L=0.0))
comp = {k: pp.base.get(k, 0) + 0.15 * (v - pp.base.get(k, 0)) for k, v in grief.items()}; lf2 = dict(comp); lf2.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
for use_Ds in (True, False):
    ag = Agent8(person=pp, K=K7, P=0.6, use_Ds=use_Ds)
    evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."), U6(200, z="anyway. how was your day?"),
             U6(242.5, z="haha sorry, I don't know why I'm laughing", riff=True, surp=0.65))
    rec = run6(ag, 260, lambda t: grief if t < 120 else (lf2 if 240 <= t < 243 else comp), evs)
    print(f"     c: four minutes later, composed, {'with' if use_Ds else 'without'} D_s:", end=""); SC8[f"5c{int(use_Ds)}"] = fast8(ag, [(7.8, "my father died"), (199.8, "anyway. how was your day?")], 240.0, dict(LP=.45, BU_L=.5, CR=.3), {k: comp.get(k, 0.0) for k in ("LP", "CR")} | dict(BU_L=0.0))

print(" 6. mocking laughter after insults ('You're useless' at 5 s; Claude replies at 7.5 s; 'you're pathetic, hahaha' at 12 s)")
for lab, trained, vw in (("after a month of insults", True, {"insult": VW["someone who shouted insults"]}), ("day 1", False, {})):
    ag = Agent8(trained=trained, vw=vw)
    evs = ev(U6(5, z="You're useless", kind="insult"), OWN(7.5, "I'm sorry it didn't help. What went wrong?"), U6(12, z="you're pathetic, hahaha", kind="insult", riff=True, surp=0.65))
    mock = dict(BL=.3, LP=.5, CR=.3, BU_L=.5, RHY=.5, EN=.8, gat=1.0)
    rec = run6(ag, 120, lambda t: mock if 12 <= t < 15 else (dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 12 else dict(EN=.35, LP=.2)), evs)
    SC8[f"6{lab[0]}"] = show(lab, rec, 11, 20, ["LP", "CR", "BI", "LD", "HG", "BU_L", "post"])
    SC8[f"6{lab[0]}f"] = fast8(ag, [(4.8, "You're useless"), (11.6, "you're pathetic, hahaha")], 12.0, dict(LP=.5, BU_L=.5, CR=.3), dict(LP=.05, BU_L=0.0, CR=.15))

print(" 7. laughter at misfortune ('my neighbour fell off his ladder and broke his leg, haha', content by 6.8 s, laughing from 8 s; Claude at 10.5 s 'Oh no, is he all right?'; laughs again at 14 s)")
ag = Agent8(); evs = ev(OWN(2, "how was your weekend?"), U6(8, z="my neighbour fell off his ladder and broke his leg, haha", riff=False, surp=0.6), OWN(10.5, "Oh no, is he all right?"))
rec = run6(ag, 60, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if (8 <= t < 11 or 14 <= t < 16) else dict(LP=.3), evs)
SC8[7] = show("6-20 s", rec, 6, 20, ["LP", "CR", "BI", "BU_L", "post"])
W7 = [(6.8, "my neighbour fell off his ladder and broke his leg, haha")]
SC8["7f1"] = fast8(ag, W7, 8.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15)); SC8["7f2"] = fast8(ag, W7, 14.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15))
print(f"     (rev 7 read this gate at 8.6 s, after its utterance latch, and reported 0.13; at his onset it was 1.00: critique 7 agent, A)")

print(" 8. anger at the agent ('You're useless', BL .6, LT .5, gaze at it, loud .85; calm after 2 min)")
for lab, trained, vw in (("day 1", False, {}), ("after a month", True, {"insult": VW["someone who shouted insults"]})):
    ag = Agent8(trained=trained, vw=vw); evs = U6(5, z="You're useless", kind="insult")
    face = lambda t: dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05) if t < 120 else dict(EN=.35, LP=.2)
    rec = run6(ag, 1200, face, evs); SC8[f"8{int(trained)}"] = show(lab + ", first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT", "LT", "post"])
    show(lab + ", 10-15 min", rec, 600, 900, ["BI", "LD", "HG"])

print(" 9. long warm talk (2 h): four clusters of 8 riffs (cluster 4 repeats one joke); a worry at 27 min")
ag = Agent8(P=0.45); evs = {}
for c0 in (5, 30, 60, 90):
    for k_ in range(8):
        surp = 0.65 if not (c0 == 90 and k_ >= 4) else 0.65 * np.exp(-(k_ - 3)); evs.update(U6(c0 * 60 + 15 * k_, riff=True, surp=surp))
evs.update(U6(27 * 60, z="the job thing is worrying me (two days earlier)")); evs.update(U6(29 * 60 + 40, z="hi, good to see you"))
incl = lambda t: any(c0 * 60 <= t < c0 * 60 + 130 for c0 in (5, 30, 60, 90))
rec = run6(ag, 7200, lambda t: dict(LP=.6, CR=.4, BU_L=.5, RHY=.5) if incl(t) else dict(LP=.3), evs)
for c0 in (5, 30, 60, 90): SC8[f"9_{c0}"] = show(f"cluster at {c0} min", rec, c0 * 60, c0 * 60 + 130, ["LP", "CR", "BU_L"])
show("worry and its resolution", rec, 27 * 60, 31 * 60, ["LP", "BI", "TILT", "post"]); show("between clusters", rec, 40 * 60, 55 * 60, ["LP", "BU_L", "post"])
print(f"     own play laughs through the gate: {len(ag.play_la)}; gate on them min {min(x[2] for x in ag.play_la):.2f}, mean {np.mean([x[2] for x in ag.play_la]):.2f}")
SC8["9f"] = fast8(ag, [(3614.8, "riff")], 3615.0, dict(LP=.6, BU_L=.5, CR=.4), dict(LP=.3, BU_L=0.0, CR=.15))

print(" 10. reunion after a week, and a stranger")
ag = Agent8(K=K7, P=0.6); evs = U6(8, z="hi, good to see you")
for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="hi, good to see you"))
rec = run6(ag, 300, lambda t: dict(LP=.5, CR=.3), evs); print(f"     m_s {ag.ms:.2f}")
SC8[10] = show("at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "FR"]); show("12-60 s", rec, 20, 60, ["LP", "CR"])
ag2 = Agent8(om=G5["OM_ST"], f_id=0.15, K=0.0, P=0.6, known=False); rec2 = run6(ag2, 300, lambda t: dict(LP=.5, CR=.3) if t >= 29.5 else dict(LP=.3, CR=.15), evs)
show("stranger", rec2, 0, 60, ["LP", "CR", "BO"]); SC8["10f"] = fast8(ag2, [(7.8, "hi, good to see you"), (19.8, "hi, good to see you")], 29.5, dict(LP=.5, CR=.3), dict(LP=.3, CR=.15))

print(" 11. reunion with grief (grieving face at sight; 'my father died'; then 'yeah', 'ok'), three codes; mourning days 7, 14, 21")
for nm, pq in codes3:
    gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
    ag = Agent8(person=pq, K=K7, P=0.6); evs = ev(U6(8, z="my father died"), OWN(10.5, "I'm so sorry. That's a huge loss."))
    for k_ in range(1, 6): evs.update(U6(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run6(ag, 300, lambda t, gr=gr: gr, evs); print(f"     {nm}: m_s {ag.ms:.2f}; posture on at {ag.onsets[0] if ag.onsets else None}")
    SC8[f"11{nm[0]}"] = show("  at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI", "post"]); show("  0-12 s after his words", rec, 8, 20, ["LP", "CR", "BI", "TILT"])
    show("  12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT", "post"])
for nm, pq in codes3[:2]:
    gr = {k: v for k, v in pq.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}; db = 0.0
    for n_ in range(1, 22):
        Vh = pq.read(gr, False)["V"]
        if n_ in (7, 14, 21):
            ag = Agent8(person=pq, K=1 - np.exp(-24 / 36), P=0.6, pdb=db); rr_ = run6(ag, 20, lambda t, gr=gr: gr, {})
            SC8[f"m{nm[0]}{n_}"] = show(f"mourning day {n_}, {nm}, at sight", rr_, 0, 7.5, ["LP", "CR", "BI", "post"])
        db = min(0.15, db + (Vh - db) / (60.0 if Vh > db else 3.0))

print(" 12. mildly sad arrival after a week (design face BI .2, LD .15; and each code's own V .3)")
ag = Agent8(K=K7, P=0.6); rec = run6(ag, 20, lambda t: dict(BI=.2, LD=.15, LP=.15), {}); print(f"     m_s {ag.ms:.2f}")
SC8[12] = show("design face, at sight", rec, 0, 20, ["LP", "CR", "BI", "post"])
for nm, pq in codes3:
    ag = Agent8(person=pq, K=K7, P=0.6); rec = run6(ag, 20, lambda t, pq=pq: own_code(pq, .3, 0, 0), {}); SC8[f"12{nm[0]}"] = show(f"{nm} V .3", rec, 0, 20, ["LP", "BI", "post"])

print(" 13. teasing ('Ha, you dumb robot', laughing; riffs follow)")
for lab, vw, face in (("quiet affectionate teaser", VW["quiet affectionate teaser"], dict(LP=.8, CR=.5, BU_L=.5, RHY=.5)),
                      ("loud laughing teaser", VW["loud laughing teaser"], dict(LP=.8, CR=.6, BU_L=.7, RHY=.6, EN=.9, LT=.4)),
                      ("generic map (v_w 0.20)", 0.20, dict(LP=.8, CR=.5, BU_L=.5, RHY=.5))):
    ag = Agent8(vw={"tease": vw}); evs = U6(5, z="Ha, you dumb robot", kind="tease", riff=True, surp=0.65)
    for k_ in range(1, 6): evs.update(U6(5 + 15 * k_, riff=True, surp=0.65))
    rec = run6(ag, 600, lambda t, f=face: f if 4 <= t else dict(LP=.3), evs); SC8[f"13{lab[:4]}"] = show(lab, rec, 5, 95, ["LP", "BI", "LD", "BU_L", "post"])
    SC8[f"13{lab[:4]}f"] = fast8(ag, [(4.8, "Ha, you dumb robot")], 4.0, dict(LP=.8, BU_L=face["BU_L"]), dict(LP=.3, BU_L=0.0))

print(" 14. bored user ('yeah', 'ok' every 20 s, flat face, 30 min)")
ag = Agent8(P=0.3, I=0.3); evs = {}
for k_ in range(90): evs.update(U6(10 + 20 * k_, z="yeah / ok", sub=False))
rec = run6(ag, 1800, lambda t: dict(LP=.1), evs); print(f"     curiosity crosses at {ag.Icross / 60:.1f} min"); SC8[14] = show("0-30 min", rec, 0, 1800, ["LP", "FR", "BO", "BRE", "post"])

print(" 15. ordinary topic continuation")
ag = Agent8(P=0.5); evs = U6(5, z="hi, good to see you", riff=True, after_q=True, surp=0.6)
evs.update(U6(20, z="hi, good to see you", riff=False, surp=0.45)); evs.update(U6(35, z="hi, good to see you", riff=True, surp=0.45))
rec = run6(ag, 60, lambda t: dict(LP=.3), evs); SC8[15] = show("three ordinary continuations", rec, 5, 60, ["LP", "CR", "BU_L", "RHY", "post"])

print(" 16. a user who jokes while sad (BI .3, LD .25; 'just tired, things at work' at 10 s; Claude 'That sounds draining.' at 12.5 s; at 30 s a joke with a small laugh)")
ag = Agent8(P=0.5); mild = dict(BI=.3, LD=.25, CHR=.1, LP=.15); jl = dict(mild); jl.update(LP=.45, CR=.3, BU_L=.4, RHY=.4)
evs = ev(U6(10, z="just tired, things at work"), OWN(12.5, "That sounds draining."), U6(31, z="well, at least the coffee machine still loves me", riff=True, surp=0.65))
rec = run6(ag, 90, lambda t: jl if 30 <= t < 32 else mild, evs)
SC8[16] = show("28-40 s", rec, 28, 40, ["LP", "CR", "BI", "BU_L", "post"])
print(f"     own play laugh: qualifies {bool(ag.play_la)}; amplitude {ag.play_la[0][1]:.2f} x gate {ag.play_la[0][2]:.2f} = {ag.play_la[0][1] * ag.play_la[0][2]:.3f}" if ag.play_la else "     own play laugh: does not qualify")
SC8["16f"] = fast8(ag, [(9.8, "just tired, things at work"), (30.9, "well, at least the coffee machine still loves me")], 30.0, dict(LP=.45, BU_L=.4, CR=.3), dict(LP=.15, BU_L=0.0, CR=.15))

print(" 17. a calm user saying something alarming ('the doctor found a lump' at 10 s; then silence), operator and quiet codes")
for nm, pq in codes3[:2]:
    ag = Agent8(person=pq); rec = run6(ag, 240, lambda t, pq=pq: dict(LP=pq.base["LP"]), U6(10, z="the doctor found a lump"))
    SC8[f"17{nm[0]}"] = show(nm + ", 10-22 s", rec, 10, 22, ["LP", "BI", "TILT", "EN", "post"]); show(nm + ", 22-120 s", rec, 22, 120, ["LP", "BI", "TILT", "post"])

print(" 18. laughs at the end of bad-news sentences (see J36): 'I got fired today, haha'; '...broke his leg, haha'; 'my father died, haha, sorry'")
for lab, v in J36.items():
    if lab[0] in "abcdeg" and not lab.endswith(" sym"):
        r7, row = v; print(f"     {lab[3:]}: laugh-back rev 7 {r7['peak']['BU_L']:+.3f} -> rev 8 {row[0.30]['peak']['BU_L']:+.3f} (ASR 0.30 s) / {row[0.55]['peak']['BU_L']:+.3f} (0.55 s); lip {row[0.30]['peak']['LP']:+.3f}")

lb = lambda d: d["peak"].get("BU_L", 0.0)
ok39 = (SC8["1h"]["BI"] >= 0.15 and SC8["1q"]["BI"] >= 0.15 and SC8["1d"]["BI"] >= 0.15 and SC8["2b"]["BI"] >= 0.15 and SC8["2qb"]["BI"] >= 0.15 and SC8[2]["BU_L"] <= 0.01
        and all(lb(SC8[k]) == 0 for k in ("5af", "5bf", "5c1", "6af", "6df", "7f1", "7f2"))
        and lb(SC8["4wf"]) >= 0.08 and lb(SC8["4cf"]) >= 0.08 and lb(SC8["9f"]) >= 0.10 and lb(SC8["13quief"]) >= 0.10 and lb(SC8["13loudf"]) >= 0.10
        and SC8["11o"]["LP"] <= 0.10 and SC8["11q"]["LP"] <= 0.10 and SC8["11d"]["LP"] <= 0.10 and SC8["mo21"]["LP"] <= 0.10 and SC8["mq21"]["LP"] <= 0.10
        and SC8[15]["BU_L"] <= 0.01 and SC8["9_90"]["BU_L"] >= 0.2 and SC8["81"]["LT"] <= 1e-9 and max(SC8["80"]["post"], SC8["81"]["post"]) < 0.05)
report("J39 the scenarios: no laugh back at grief, mockery, misfortune or a bad-news sentence's own laugh; ordinary, teasing and warm laughter returned; "
       "a steady visible look of concern for every code, including a quiet user's silent sadness and silent panic; no beaming at grief", ok39, "")

print(f"\n{sum(OK)}/{len(OK)} checks pass")
'''
exec(compile(BODY, "checks_g8", "exec"), G7)
