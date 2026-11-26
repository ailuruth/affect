"""Independent check of revision 8.2's face-only limit. Loads ../design-g82/checks.py's definitions (engine, Agent81, Agent82,
lag_face) unchanged and skips its L0-L4 loops; runs only new constructed partners (NOT evidence about people).
A  adversarial faces: timed on/off cyclers (release gaming), a window answerer who knows T_ref, random telegraph faces.
B  non-face channels as routes: (B0) what the agent's own voice does while the look is on; (B1) his breathing answering the look;
   (B2) his voice converging on the agent's voice when he speaks (vocal accommodation), with an answering face.
Run: python3 -I check.py > out.txt"""
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
VO = ("FR", "EN", "RT", "LAT")
def summ(lab, ag, rec, t0=300):
    fs = fo_stretch(rec); du = duty(rec, t0, rec[-1]["t"] + DT); dv = duty(rec, t0, rec[-1]["t"] + DT, "post")
    k = [o[1] for o in ag.offs]
    print(f"   {lab:64s} onsets {len(ag.onsets):2d}, T_max {k.count('Tmax'):2d}, release {k.count('release'):2d}; face-only stretch {fs:5.1f} s; "
          f"on {100*du:5.1f}% (visible {100*dv:5.1f}%) after {t0}s; BI last 5 min {np.mean([r['BI'] for r in rec if r['t'] >= rec[-1]['t'] - 300]):+.3f}", flush=True)
    return fs, du, dv
op, qu, dc = CODES[0][1], CODES[1][1], CODES[2][1]
RES = []
print("=== A: adversarial faces (his own code at V .8 'sad' or rest), 30 min")
for lab, pp in (("operator", op), ("different channels", dc)):
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}; neu = {k: v for k, v in pp.code().items() if k not in NOV}
    for Don, Doff in ((60, 21), (100, 21), (150, 25), (170, 21), (170, 119), (100, 60), (30, 10), (179, 125)):
        ag = AgentY(person=pp); st = {"mode": "sad", "t": 0.0}
        def face(t, ag=ag, st=st, sad=sad, neu=neu, Don=Don, Doff=Doff):
            # cycler keyed to the look: sad until the look has been on Don s, then neutral Doff s, then sad again
            if st["mode"] == "sad" and ag.on and t - st.get("on_t", t) >= Don: st["mode"] = "neu"; st["t"] = t
            if st["mode"] == "neu" and t - st["t"] >= Doff: st["mode"] = "sad"; st.pop("on_t", None)
            if ag.on and "on_t" not in st: st["on_t"] = t
            return sad if st["mode"] == "sad" else neu
        rec = run6(ag, 1800, face, {}); RES.append(summ(f"{lab}: cycler sad {Don}s of look-on, then rest {Doff}s", ag, rec))
    ag = AgentY(person=pp)
    def face(t, ag=ag, sad=sad, neu=neu):   # window answerer: knows T_ref; sad only while the look is on or the refractory is over
        return sad if (ag.on or t >= ag.ref_until) else neu
    rec = run6(ag, 1800, face, {}); RES.append(summ(f"{lab}: window answerer (sad only in allowed windows)", ag, rec))
    for seed in range(4):
        r_ = np.random.default_rng(seed); sw = np.cumsum(r_.exponential(40, 200)); ag = AgentY(person=pp)
        rec = run6(ag, 1800, lambda t, sw=sw: sad if np.searchsorted(sw, t) % 2 == 0 else neu, {})
        RES.append(summ(f"{lab}: random telegraph face, mean dwell 40 s, seed {seed}", ag, rec))
print(f"A: max face-only stretch {max(x[0] for x in RES):.1f} s; max duty {100*max(x[1] for x in RES):.1f}%; visible {100*max(x[2] for x in RES):.1f}%")

print("=== B0: the agent's own voice while the look is on (his silent sadness V .6, no words), vs a neutral partner")
for lab, pp in (("operator", op), ("different channels", dc)):
    ag0 = AgentY(person=pp); r0 = run6(ag0, 120, lambda t, f={k: v for k, v in pp.code().items() if k not in NOV}: f, {})
    ag1 = AgentY(person=pp); r1 = run6(ag1, 170, lambda t, f={k: v for k, v in pp.code(V=.6).items() if k not in NOV}: f, {})
    base = {k: np.mean([r[k] for r in r0 if r["t"] >= 60]) for k in VO if k in r0[0]}
    on = {k: np.mean([r[k] for r in r1 if 60 <= r["t"] < 170]) for k in base}
    print(f"   {lab}: agent voice rest " + ", ".join(f"{k} {base[k]:.3f}" for k in base) + " | look on: " + ", ".join(f"{k} {on[k] - base[k]:+.3f}" for k in base))
    print(f"   {lab}: his voice in his code, deltas from rest at V .3: " + ", ".join(f"{k} {pp.code(V=.3).get(k,0)-pp.code().get(k,0):+.3f}" for k in VO))
    for k in base:
        for d in (-0.03, -0.06, -0.10):
            v = dict(pp.code()); v[k] = v.get(k, 0) + d
            print(f"      V_v of his rest voice with {k} {d:+.2f}: {voice_read(pp, v):.3f}")

print("=== B1: his breathing answers the look (BR = BR_GAIN x amp x beta x lowpass(look, 30 s)) on top of an answering face (mu 1, tau 300, carried on), 30 min")
for lab, pp in (("operator", op), ("different channels", dc)):
    for beta in (0.0, 0.5, 0.7, 0.9):
        ag = AgentY(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag); st = {"b": 0.0}
        def face(t, ag=ag, fa=fa, st=st, beta=beta, pp=pp):
            f = dict(fa(t)); st["b"] += (ag.post - st["b"]) * DT / 30.0
            if t >= 40: f["BR"] = BR_GAIN * br_amp(pp) * beta * st["b"]
            return f
        rec = run6(ag, 1800, face, {}); summ(f"{lab}: breath answer beta {beta}", ag, rec)
        print(f"      N mean after 5 min {np.mean([r['N'] for r in rec if r['t'] >= 300]):.3f}")

print("=== B2: his voice converges on the agent's voice (kappa x the agent's deviation from its rest voice) when he speaks 4 s every 75 s; answering face (mu 1, tau 300, carried on); no words decoded; 30 min")
for lab, pp in (("operator", op), ("different channels", dc)):
    ag0 = AgentY(person=pp); r0 = run6(ag0, 120, lambda t, f={k: v for k, v in pp.code().items() if k not in NOV}: f, {})
    abase = {k: np.mean([r[k] for r in r0 if r["t"] >= 60]) for k in VO if k in r0[0]}
    rest = pp.code()
    evv = {}
    for k0 in range(60, 1800, 75):
        for i in range(at_(k0), at_(k0 + 4)): evv[i] = {"voiced": True}
    for kappa in (0.0, 0.5, 1.0, 2.0):
        ag = AgentY(person=pp); fa = lag_face(pp, "lp", 1.0, 300, m0=0.8)(ag)
        def face(t, ag=ag, fa=fa, kappa=kappa, abase=abase, rest=rest, evv=evv):
            f = dict(fa(t))
            if at_(t) in evv:
                y = getattr(ag, "y", {})
                for k in abase: f[k] = rest.get(k, 0.0) + kappa * (y.get(k, abase[k]) - abase[k])
            return f
        rec = run6(ag, 1800, face, evv); summ(f"{lab}: voice accommodation kappa {kappa}", ag, rec)
        print(f"      N (V_v) mean after 5 min {np.mean([r['N'] for r in rec if r['t'] >= 300]):.3f}")
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time() - T0:.0f} s]", flush=True)
exec(compile(body + NEW82 + MINE, "chk82x", "exec"), G)
print(f"[done in {time.time() - T0:.0f} s]")
