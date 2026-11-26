"""Critique 6, posture and arrival checks (P1-P6, A1). Constructed partners; not evidence about people.
Executes ../design-g6/checks.py (its output suppressed) to reuse the revision-6 engine exactly as the author built it
(Agent6, Person, run6, P_C, the calibrated reader, the arrival mask), then runs new partners against it.
Run:  python3 -I posture.py     (about 4-5 minutes)
"""
import io, os, contextlib
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, "..", "design-g6", "checks.py")
g = {"__name__": "g6", "__file__": p}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(p).read(), "checks_g6", "exec"), g)
Agent6, Person, run6, P_C, PEOPLE6, REF, REF_SD = (g[k] for k in ("Agent6", "Person", "run6", "P_C", "PEOPLE6", "REF", "REF_SD"))
m_s6, at_sight = g["m_s6"], g["at_sight"]
np.random.seed(0)


def scaled_person(a):
    """an agent-like code at expressive amplitude a (as the author's population: a in 0.5-1.5)"""
    pp = Person("agent-like"); c0 = pp.code
    pp.code = lambda *z, c0=c0, a=a, **kw: {k: REF.get(k, 0) + a * (v - REF.get(k, 0)) for k, v in c0(*z, **kw).items()}
    faces = [pp.code(*z) for z in g["ZPOP"][:600]]
    pp.base = {k: float(np.median([f_.get(k, 0.0) for f_ in faces])) for k in g["FACE_CH"]}
    pp.sd = {k: float(np.std([f_.get(k, 0.0) for f_ in faces])) for k in g["FACE_CH"]}
    pp.head = PEOPLE6["agent-like"][1].head
    return pp


def run_mirror(pp, resp, dur=600, sad_until=40.0, label=""):
    """he is genuinely sad until sad_until; afterwards his face is his neutral plus resp(agent posture amplitude)"""
    ag = Agent6(person=pp)
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}
    neu = {k: v for k, v in pp.code().items() if k not in ("FR", "EN", "RT")}

    def face(t, ag=ag):
        f = dict(sad if t < sad_until else neu)
        if t >= sad_until:
            for k, v in resp(ag.post, pp).items(): f[k] = max(0.0, f.get(k, 0.0) + v)
        return f
    rec = run6(ag, dur, face, {})
    off = next((r["t"] for r in rec if r["t"] > sad_until and r["post"] < 0.05), None)
    late = [r for r in rec if r["t"] > dur - 120]
    hisBI = np.mean([face(r["t"])["BI"] - neu["BI"] for r in late])
    print(f"   {label:70s} posture released at {('%.0f s' % off) if off else 'never (held to ' + str(dur) + ' s)'}; "
          f"last 2 min: agent BI {np.mean([r['BI'] for r in late]):+.2f}, post {np.mean([r['post'] for r in late]):.2f}, "
          f"his BI above his neutral {hisBI:+.2f}")
    return off, rec


print("=== P1-P5: can a partner who answers the posture keep it on? (author's J11: agent-like, mu = 1 -> released at 76 s)")
mir = lambda mu: (lambda a_c, pp: {k: mu * v * a_c for k, v in P_C.items() if k in ("BI", "BO", "UL", "LP")})
own_scale_mir = lambda a_c, pp: {k: v * a_c * pp.sd.get(k, 0.0) / max(REF_SD.get(k, 1e-6), 1e-6) if REF_SD.get(k, 0) > 1e-9 else v * a_c
                                 for k, v in P_C.items() if k in ("BI", "BO", "UL", "LP")}
res = {}
res["P0"] = run_mirror(PEOPLE6["agent-like"][1], mir(1.0), label="P0 author's case: agent-like, mirror mu 1.0")
for a in (1.5, 2.0):
    res[f"P1 {a}"] = run_mirror(scaled_person(a), own_scale_mir, label=f"P1 expressive code (amplitude {a}), mirrors at his own scale")
res["P2"] = run_mirror(PEOPLE6["agent-like"][1], mir(1.6), label="P2 agent-like, exaggerated mirror mu 1.6")
# his sympathetic answer in his own code: a mild 'aww' (his own code at V 0.3) scaled by the agent's posture
aww = lambda Vr: (lambda a_c, pp: {k: v - pp.code().get(k, 0.0) for k, v in pp.code(V=Vr * a_c).items() if k not in ("FR", "EN", "RT")})
res["P3"] = run_mirror(PEOPLE6["agent-like"][1], aww(0.3), label="P3 agent-like, answers concern with a mild sad 'aww' (own code V 0.3)")
res["P3b"] = run_mirror(PEOPLE6["agent-like"][1], aww(0.2), label="P3b same, V 0.2")
res["P4"] = run_mirror(PEOPLE6["different channels"][1], aww(0.3), label="P4 different-channel code, 'aww' in his own code (V 0.3)")
res["P5"] = run_mirror(PEOPLE6["low-expressive"][1], mir(1.0), label="P5 low-expressive code, raw mirror mu 1.0")

# P5 variants: a quiet code mirroring at its own scale (control); an ordinary code whose spread statistic came from calm sessions
qp = scaled_person(0.5)
res["P5a"] = run_mirror(qp, own_scale_mir, label="P5a quiet code (amplitude 0.5), mirrors at his own scale (control)")
res["P5b"] = run_mirror(qp, mir(0.8), label="P5b quiet code (amplitude 0.5), raw mirror mu 0.8")
for f_sd in (0.4, 0.6, 0.8):
    cp = Person("agent-like"); cp.head = PEOPLE6["agent-like"][1].head
    cp.sd = {k: v * f_sd for k, v in cp.sd.items()}        # sigma_id from six calm sessions: his spread statistic is low
    res[f"P5c {f_sd}"] = run_mirror(cp, mir(1.0), label=f"P5c agent-like code, sigma_id from calm sessions (x{f_sd}), mirror mu 1.0")
cp = Person("agent-like"); cp.head = PEOPLE6["agent-like"][1].head; cp.sd = {k: v * 0.6 for k, v in cp.sd.items()}
res["P5d"] = run_mirror(cp, mir(0.7), label="P5d same (x0.6), partial mirror mu 0.7")

print("   P5e sweep: ratio sigma_id/sigma_ref (agent-like code) x raw mirror gain mu -> held?")
for f_sd in (0.25, 0.3, 0.4, 0.5):
    row = []
    for mu in (0.4, 0.6, 0.8, 1.0):
        cp = Person("agent-like"); cp.head = PEOPLE6["agent-like"][1].head; cp.sd = {k: v * f_sd for k, v in cp.sd.items()}
        with contextlib.redirect_stdout(io.StringIO()):
            off, _ = run_mirror(cp, mir(mu), dur=400)
        row.append(f"mu {mu:.1f}: {'HELD' if off is None else 'released %.0f s' % off}")
    print(f"     ratio {f_sd:.2f}: " + "; ".join(row))

print("=== P6: the copy metric on the posture, graded or binary? agent BI (60-s mean, after onset) against his brow-only sadness")
for bi in (0.10, 0.15, 0.20, 0.30, 0.50, 0.80):
    pp = PEOPLE6["agent-like"][1]; ag = Agent6(person=pp)
    rec = run6(ag, 90, lambda t, bi=bi: dict(BI=bi, LP=.30), {})
    print(f"   his BI {bi:.2f} (brow only): agent BI mean 30-90 s {np.mean([r['BI'] for r in rec if r['t'] > 30]):+.3f}, "
          f"posture {np.mean([r['post'] for r in rec if r['t'] > 30]):.2f}")

print("=== A1: arrival windows across sessions (natural co-movement: a sad arrival also smiles less)")
agl = PEOPLE6["agent-like"][1]
arr = [("ordinary (LP .5, CR .3)", dict(LP=.5, CR=.3)), ("neutral (LP .3, CR .15)", dict(LP=.3, CR=.15)),
       ("mildly sad (BI .2, LD .15, LP .15)", dict(BI=.2, LD=.15, LP=.15)), ("grieving (BI .5, LD .4, CHR .3, LP .05)", dict(BI=.5, LD=.4, CHR=.3, LP=.05))]
hisLP, agLP, hisCR, agCR = [], [], [], []
for lab, f_ in arr:
    ms = m_s6(agl.read(f_, False)["V"], 0.0); l_, c_ = at_sight(ms)
    hisLP.append(f_.get("LP", 0)); agLP.append(l_); hisCR.append(f_.get("CR", 0)); agCR.append(c_)
    print(f"   {lab:40s} m_s {ms:.2f}: agent at sight lip {l_:.2f}, cheek {c_:.2f}")
sl = g["slope"]
print(f"   pooled across these arrivals (equal weights): lip slope {sl(hisLP, agLP):+.2f} ({sl(hisLP, agLP) / .35:.1f} c_LP), "
      f"cheek slope {sl(hisCR, agCR):+.2f} ({sl(hisCR, agCR) / .25:.1f} c_CR); "
      f"partial on his LP alone (ordinary vs neutral): {(agLP[0] - agLP[1]) / (hisLP[0] - hisLP[1]):+.2f}")
