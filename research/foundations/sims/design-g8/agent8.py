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
        if s.use_Ds: s.Ds = max(s.Ds * np.exp(-DT / TAU_DS), rp["V"], min(1.0, 2.5 * s.f3.get("BU_S", 0.0)))
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
