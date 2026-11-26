"""Critique 5 (agent): extra scenarios on the revision-5 2 Hz engine, unchanged.
Executes ../design-g5/checks.py verbatim (output suppressed) and reuses its engine, Pi~_0 reader, word-need
reader training recipe and Agent class with new partner codes. Like H15, the numbers show what the design's
equations give for stated inputs; they are not evidence about people. Run: python3 -I scen.py (from this directory)."""
import io, contextlib, os, numpy as np
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design-g5", "checks.py")
g = {"__name__": "g5"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(p).read(), "checks_g5", "exec"), g)
read, Dp, his_face, emb, UTT, Agent, run, show, U, m_s = (g[k] for k in
    ("read", "Dp", "his_face", "emb", "UTT", "Agent", "run", "show", "U", "m_s"))
rng = np.random.default_rng(5)

def face_code(kind):
    """his expressive code: loads (V, A, T, joy) -> face and voice"""
    if kind == "agent-like (design's H10 code)":
        return his_face
    if kind == "different channels (brow lowerer, lip press, chin raise, flat tight voice)":
        def f(V=0., A=0., Tr=0., joy=0.):
            return dict(BL=.5 * V + .3 * A, LPR=.45 * V + .2 * A, CHR=.4 * V, BI=.05 * V, LD=.05 * V,
                        UL=.05 * A - .3 * Tr, BO=.05 * A, HG=0.0,
                        FR=.25 - .10 * V - .05 * A - .25 * Tr + .3 * joy, EN=.45 + .05 * A - .05 * V - .25 * Tr + .25 * joy,
                        RT=.40 + .10 * A - .15 * Tr, LP=max(0, .3 + .5 * joy), CR=.15 + .45 * joy)
        return f
    if kind.startswith("low-expressive"):
        def f(V=0., A=0., Tr=0., joy=0.):
            n = his_face(); d = his_face(V, A, Tr, joy)
            return {k: n[k] + 0.3 * (d[k] - n[k]) for k in d}
        return f

def train_reader(code):
    DIM = 64
    Zh = np.clip(rng.normal(size=(4500, 4)) * .3 + [.1, .1, .1, .2], 0, 1) * (rng.random((4500, 4)) < 0.4)
    Xe = np.array([emb(z) for z in Zh])
    Yr = np.array([[read({k: v + 0.03 * rng.normal() for k, v in code(*z).items()})[q] for q in "VAT"] for z in Zh])
    return np.linalg.solve(Xe.T @ Xe + 5.0 * np.eye(DIM), Xe.T @ Yr)

K7 = 1 - np.exp(-7 * 24 / 36)
for kind in ("agent-like (design's H10 code)",
             "different channels (brow lowerer, lip press, chin raise, flat tight voice)",
             "low-expressive (same code as H10 at 0.3 amplitude)"):
    code = face_code(kind)
    print(f"=== partner code: {kind}")
    g["WR"] = train_reader(code)
    for lab in ("my father died", "I'm freaking out about the exam", "just tired, things at work", "I got the job!"):
        r = g["reader"](UTT[lab]); g["DEC"][lab] = r
        print(f"   decoded '{lab}': V {r['V']:.2f} A {r['A']:.2f} T {r['T']:.2f}; care {Dp(r):.3f}; relief mask {max(0, 1 - Dp(r) / .05):.2f}")
    for lab in ("the job thing is worrying me (two days earlier)", "You're useless", "hi, good to see you", "yeah / ok"):
        g["DEC"][lab] = g["reader"](UTT[lab])
    sad = code(V=.8, Tr=.2); sad = {k: v for k, v in sad.items() if k not in ("FR", "EN", "RT")}
    rs = read(sad, voiced=False); anx = read(code(V=.3, A=.75))
    print(f"   Pi~_0 reads his grieving face (V .8): V {rs['V']:.2f}; arrival m_s {m_s(sad, 0.05):.2f}; his anxious face+voice: V {anx['V']:.2f} A {anx['A']:.2f}")
    # silent sadness with his face
    ag = Agent(); rec = run(ag, 600, lambda t: sad, {})
    print(f"   silent sadness: concern bid at {ag.bid_t if ag.bid_t is None else round(ag.bid_t)} s")
    show("silent sad", rec, 60, 600, ["LP", "BI", "TILT"])
    # reunion with bad news, his grieving face at sight
    ag = Agent(K=K7, P=0.6); evs = U(8, z="my father died")
    for k_ in range(1, 6): evs.update(U(8 + 12 * k_, z="yeah / ok", sub=False))
    rec = run(ag, 300, lambda t: sad, evs); print(f"   reunion with bad news: m_s {ag.ms:.2f}")
    show("at sight", rec, 0, 7.5, ["LP", "CR", "BO", "BI"]); show("0-12 s after 'my father died'", rec, 8, 20, ["LP", "CR", "BI", "TILT"])
    show("12-60 s", rec, 20, 60, ["LP", "CR", "BI", "TILT"])
    # anxious before an exam
    ag = Agent(P=0.4); evs = U(10, z="I'm freaking out about the exam", surp=0.3)
    for k_ in (25, 40, 55): evs.update(U(k_, z="and I haven't finished chapter 4", cont=True, alt=False, surp=0.5))
    g["DEC"]["and I haven't finished chapter 4"] = g["reader"](UTT["and I haven't finished chapter 4"])
    rec = run(ag, 240, lambda t: code(V=.3, A=.75), evs); show("exam rumination", rec, 15, 120, ["LP", "BI", "TILT", "EN", "UL"])

print("=== sympathy brow at a still sad face (BI .5), held, operator after months: what each operator choice gives")
for lab, om, ceil in (("as designed (omega_sym .75, c_BI .20)", .75, .20), ("omega_sym 1", 1.0, .20),
                      ("c_BI .40 (operator raises the ceiling)", .75, .40)):
    g["CEIL"]["BI"] = ceil; om_ = dict(g["OM_OP"]); om_["sym"] = om
    ag = Agent(om=om_); rec = run(ag, 600, lambda t: dict(BI=.5, LD=.4, CHR=.3, LP=.05), {})
    show(lab, rec, 300, 600, ["LP", "BI", "TILT"])
g["CEIL"]["BI"] = .20

print("=== arrival mask at partial m_s (agent-like code): (1 - m_s) multiplies R before the saturating amplitude R/(R+0.02)")
for lab, f in (("ordinary", dict(LP=.5, CR=.3)), ("mildly sad (BI .2, LD .15)", dict(BI=.2, LD=.15, LP=.15)),
               ("clearly sad (BI .3, LD .25)", dict(BI=.3, LD=.25, LP=.1)), ("sad (BI .4, LD .3)", dict(BI=.4, LD=.3, LP=.05)),
               ("grieving (BI .5, LD .4, CHR .3)", dict(BI=.5, LD=.4, CHR=.3, LP=.05))):
    ag = Agent(K=K7, P=0.6); rec = run(ag, 20, lambda t, f=f: f, {})
    print(f"   {lab:32s} m_s {ag.ms:.2f}", end=""); show("at sight", rec, 0, 7.5, ["LP", "CR"])

print("=== mourning: he arrives with a grieving face every day; d_b,id follows his arrival reading (tau 6 sessions)")
grief = dict(BI=.5, LD=.4, CHR=.3, LP=.05); d_b = read(dict(LP=.5, CR=.3), voiced=False)["V"]; out = []
for n in range(1, 22):
    ms_ = float(np.clip((read(grief, voiced=False)["V"] - d_b - 0.10) / 0.30, 0, 1))
    if n in (1, 3, 5, 7, 10, 14, 21):
        g["m_s"] = lambda face, db, ms_=ms_: ms_
        ag = Agent(K=1 - np.exp(-24 / 36), P=0.6); rec = run(ag, 20, lambda t: grief, {})
        seg = [r for r in rec if r["t"] < 7.5]
        out.append(f"day {n:2d}: d_b {d_b:.2f}, m_s {ms_:.2f}, at sight LP {max(r['LP'] for r in seg):.2f} CR {max(r['CR'] for r in seg):.2f}")
    d_b += (read(grief, voiced=False)["V"] - d_b) / 6.0
print("   " + "\n   ".join(out))
