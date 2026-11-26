"""Critic's scenarios for design-cayley-ledger.md revision 6 (agent critique 6).
Executes ../design-g6/checks.py unchanged (output suppressed) and reuses its Agent6, PEOPLE6, run6, GK.
Numbers are what the design's equations give for stated inputs; not evidence about people.
Run: python3 -I scen.py
"""
import io, os, contextlib
import numpy as np
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design-g6", "checks.py")
g = {"__name__": "g6", "__file__": p}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(p).read(), "checks_g6", "exec"), g)
Agent6, PEOPLE6, run6, U6, GK, show, P_C = (g[k] for k in ("Agent6", "PEOPLE6", "run6", "U6", "GK", "show", "P_C"))

def seg(rec, t0, t1, c): s_ = [r[c] for r in rec if t0 <= r["t"] < t1]; return max(s_), float(np.mean(s_))

print("=== A. crying in waves: cry 0-40 s, calm 40-70 s, cry again from 70 s (operator code)")
cry = dict(BI=.8, LD=.6, CHR=.4, BU_S=.4, LP=.02); calm = dict(BI=.08, LD=.06, LP=.25)
for gap in (30, 15):
    ag = Agent6(); f = lambda t, gap=gap: cry if (t < 40 or t >= 40 + gap) else calm
    rec = run6(ag, 260, f, {})
    off = next((r["t"] for r in rec if r["t"] > 40 and r["post"] < 0.05), None)
    on2 = next((r["t"] for r in rec if r["t"] > 40 + gap and r["post"] > 0.5), None)
    print(f"   calm gap {gap} s: posture released at {off} s; on again at {on2} s (crying resumed at {40 + gap} s)")
    show(f"second wave, first 40 s", rec, 40 + gap, 80 + gap, ["LP", "BI", "TILT", "post", "BU_L"])

print("=== B. different-channel user (face head trained): anger at the agent and concentration")
pp = PEOPLE6["different channels"][1]
for lab, face in (("anger: BL .6, LT .5, gaze at it, loud .85", dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05)),
                  ("concentrating, silent: BL .35, LPR .15", dict(BL=.35, LPR=.15, LP=.25)),
                  ("concentrating, mild: BL .25, LPR .10", dict(BL=.25, LPR=.10, LP=.25))):
    rd = pp.read(face, False)
    ag = Agent6(person=pp); rec = run6(ag, 300, lambda t, f_=face: f_, {})
    on = next((r["t"] for r in rec if r["post"] > 0.5), None)
    print(f"   {lab}: read V {rd['V']:.2f} A {rd['A']:.2f}; posture on at {on}; concern bid at {ag.bid_t}")
    show("   0-300 s", rec, 0, 300, ["BI", "TILT", "post"])
pa = PEOPLE6["agent-like"][1]
rd = pa.read(dict(BL=.35, LPR=.15, LP=.25), False); print(f"   operator code, concentrating: read V {rd['V']:.2f}")

print("=== C. calm but alarming: neutral face (LP .3), high-need words at 10 s ('my father died' as stand-in), silent after")
for kind in ("agent-like", "low-expressive"):
    pp = PEOPLE6[kind][1]; ag = Agent6(person=pp)
    rec = run6(ag, 240, lambda t: dict(LP=.3), U6(10, z="my father died"))
    on = next((r["t"] for r in rec if r["post"] > 0.5), None)
    print(f"   {kind}: posture on at {on}")
    show("   10-22 s", rec, 10, 22, ["LP", "BI", "TILT", "EN", "post"]); show("   22-120 s", rec, 22, 120, ["LP", "BI", "TILT", "post"])

print("=== D. grief with nervous laughter / a dark joke: grieving face, 'my father died' at 8 s; at 30 s he laughs (3 s) on a riff")
pp = PEOPLE6["agent-like"][1]; grief = {k: v for k, v in pp.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
lf = dict(grief); lf.update(LP=.45, CR=.3, BU_L=.5, RHY=.5)
ag = Agent6(person=pp, K=g["K7"], P=0.6); evs = U6(8, z="my father died"); evs.update(U6(30, riff=True, surp=0.65))
rec = run6(ag, 120, lambda t: lf if 30 <= t < 33 else grief, evs)
show("   28-40 s (2 Hz engine, no fast gear)", rec, 28, 40, ["LP", "CR", "BI", "BU_L", "RHY", "post"])
print(f"   fast gear at 0.45 s (frozen, context-free): his BU_L onset 0.50 -> agent BU_L +{GK['BU_L'] * .5:.2f}, "
      f"RHY +{GK['RHY'] * .5:.2f}; his LP onset 0.40 -> agent LP +{GK['LP'] * .4:.2f}  (synthesizer reads y_BU_L, y_RHY, y_BRE)")
print("   the same fast echo for: mocking laughter after a month of insults (omega_sym < 0, hurt latched), schadenfreude laughter")

print("=== E. silent and visibly frightened or panicking (his code at V .3, A .9; no words), three codes")
for kind in ("agent-like", "low-expressive", "different channels"):
    pp = PEOPLE6[kind][1]; f_ = pp.code(V=.3, A=.9); rd = pp.read(f_, False)
    ag = Agent6(person=pp); rec = run6(ag, 180, lambda t, f_=f_: f_, {})
    on = next((r["t"] for r in rec if r["post"] > 0.5), None)
    print(f"   {kind}: read V {rd['V']:.2f} A {rd['A']:.2f}; posture on at {on}; concern bid at {ag.bid_t}")
    show("   0-180 s", rec, 0, 180, ["LP", "BI", "TILT", "UL", "post"])
