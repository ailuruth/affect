"""Independent check of revision 8.2's face-only limit. Loads ../design-g82/checks.py's definitions (engine, Agent81, Agent82,
lag_face) unchanged and skips its L0-L4 loops; runs only new constructed partners (NOT evidence about people).
A  adversarial faces: timed on/off cyclers (release gaming), a window answerer who knows T_ref, random telegraph faces.
B  non-face channels as routes: (B0) what the agent's own voice does while the look is on; (B1) his breathing answering the look;
   (B2) his voice converging on the agent's voice when he speaks (vocal accommodation), with an answering face.
Run: python3 -I check_b.py > out_b.txt"""
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
class AgentY(Agent82):
    def step(s, t, face, ev):
        y = super().step(t, face, ev); s.y = y; return y
def summ(lab, ag, rec, t0=300):
    fs = fo_stretch(rec); du = duty(rec, t0, rec[-1]["t"] + DT); dv = duty(rec, t0, rec[-1]["t"] + DT, "post")
    k = [o[1] for o in ag.offs]
    print(f"   {lab:70s} onsets {len(ag.onsets):2d}, T_max {k.count('Tmax'):2d}, release {k.count('release'):2d}; face-only stretch {fs:6.1f} s; "
          f"on {100*du:5.1f}% (visible {100*dv:5.1f}%) after {t0}s; BI last 5 min {np.mean([r['BI'] for r in rec if r['t'] >= rec[-1]['t'] - 300]):+.3f}; N mean {np.mean([r['N'] for r in rec if r['t']>=300]):.3f}", flush=True)
op, qu, dc = CODES[0][1], CODES[1][1], CODES[2][1]
print("=== B3: answering face (mu 1, tau 300, carried on: the 8.1 checker's C1b) plus a soft voice: he speaks 4 s every P s, no distress words, his voice EN lowered by d from his rest (FR, RT, LAT at rest); 30 min")
for lab, pp in (("operator", op), ("quiet 0.3", qu), ("different channels", dc)):
    print(f"   {lab}: V_v of rest voice with EN -0.02 / -0.03 / -0.05: " + " / ".join(f"{voice_read(pp, dict(pp.code(), EN=pp.code().get('EN',0)-d)):.3f}" for d in (.02,.03,.05)))
    for d, P in ((0.0, 80), (0.03, 80), (0.05, 80), (0.03, 120)):
        evv = {}
        for k0 in range(60, 1800, P):
            for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
        ag = AgentY(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); rest = pp.code()
        def face(t, fa=fa, evv=evv, rest=rest, d=d):
            f = dict(fa(t))
            if at_(t) in evv:
                for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
                f["EN"] = rest.get("EN", 0.0) - d
            return f
        rec = run6(ag, 1800, face, evv); summ(f"{lab}: soft voice EN -{d:.2f} every {P} s", ag, rec)
print("=== B3b: same soft voice (EN -0.03 every 80 s) with a NEUTRAL face after 40 s (control: no hold expected)")
for lab, pp in (("operator", op),):
    evv = {}
    for k0 in range(60, 1800, 80):
        for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
    ag = AgentY(person=pp); rest = pp.code(); sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in rest.items() if k not in NOV}
    def face(t):
        f = dict(sad if t < 40 else neu)
        if at_(t) in evv:
            for k in ("FR", "EN", "RT", "LAT"): f[k] = rest.get(k, 0.0)
            f["EN"] = rest.get("EN", 0.0) - 0.03
        return f
    rec = run6(ag, 900, face, evv); summ(f"{lab}: neutral face + soft voice", ag, rec)
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time() - T0:.0f} s]", flush=True)
exec(compile(body + NEW82 + MINE, "chk82x", "exec"), G)
print(f"[done in {time.time() - T0:.0f} s]")
