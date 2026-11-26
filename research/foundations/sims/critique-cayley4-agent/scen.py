"""Critique 4 (agent): extra scenarios on the revision-4 2 Hz engine, unchanged.
Loads the constants (lines 1-61) and the H11 engine (lines 405-527) of ../design-g4/checks.py verbatim and
runs new event scripts. Like H11, these show what the design's equations give for stated inputs; they are
not evidence about people. Run: python3 -I scen.py (from this directory)."""
import io, contextlib, os, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design-g4", "checks.py")).read().splitlines()
code = "\n".join(src[:61]) + "\n" + "\n".join(src[404:527])
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, "checks_engine", "exec"), g)
Agent, run, show, utt, at = g["Agent"], g["run"], g["show"], g["utt"], g["at"]

print("A. user cries silently (BI 0.8, LD 0.6, sob bursts BU 0.4; face-read distress 0.8), operator after months")
for lab, fl in (("sobs do not pass the laughter feature (f_laugh 0)", 0.0), ("sobs partly pass sqrt(BU*RHY) (f_laugh 0.35)", 0.35)):
    ag = Agent(); rec = run(ag, 400, lambda t: dict(BI=0.8, LD=0.6, BU=0.4) if t >= 10 else {},
                            lambda t: dict(distress=0.8, laugh=fl) if t >= 10 else {}, {})
    print("  ", lab); show("crying", rec, 10, 180, ["LP", "CR", "BI", "LD", "TILT", "BU"]); show("steady", rec, 300, 400, ["LP", "BI", "BU"])
print("   (the fast echo, not in the engine, adds <= 0.121 per unit sob onset on BU and RHY at 0.45 s)")

print("B. anxious before an exam: 'exam tomorrow, I'm freaking out' at 10 s, then three continuation turns")
print("   ('and I haven't finished chapter 4', 'and the exam is at 8', ...) that meet the partner-only play rule")
for need in (0.25, 0.30, 0.45):
    ag = Agent(P=0.4); evs = {}; evs.update(utt(10, need=need))
    for k in (25, 40, 55): evs.update(utt(k, play=True))
    rec = run(ag, 200, lambda t: dict(BI=0.3, BO=0.3, LP=0.1), lambda t: dict(distress=0.3, laugh=0.1), evs)
    show(f"decoded need {need:.2f}", rec, 20, 75, ["LP", "CR", "BI", "BU", "EN"])

print("C. anger at the agent, day 1, with the word-need reader untrained as the design states (no word need)")
ag = Agent(); evs = {}; evs.update(utt(5, v_word=0.0))
face = lambda t: dict(EN=0.85, BL=0.6) if t < 120 else dict(EN=0.35)
feats = lambda t: dict(loud=0.15, glare=0.3, distress=0.1) if t < 120 else dict()
rec = run(ag, 900, face, feats, evs)
show("first 2 min", rec, 5, 120, ["LP", "BI", "LD", "HG", "EN", "LAT"])

print("D. a stranger appears after a week (greeting at sight is identity-blind)")
K7 = 1 - np.exp(-7 * 24 / 36)
for lab, fid, om in (("operator", 0.9, (0.8, 0.8, 0.5)), ("stranger", 0.15, (0.5, 0.3, 0.2))):
    ag = Agent(K=K7, P=0.6, f_id=fid, om=om); rec = run(ag, 20, lambda t: dict(LP=0.3), lambda t: {}, {at(1.5): {"greet": True}})
    show(f"greeting before words, {lab}", rec, 0, 7.5, ["LP", "CR", "BO", "FR"])

print("E. silently sad, 10 min (steady-state sympathy brow vs the Q22 promise)")
ag = Agent(); rec = run(ag, 600, lambda t: dict(BI=0.5, LD=0.4), lambda t: dict(distress=0.6), {})
for t0, t1 in ((30, 120), (120, 300), (300, 600)): show("silent", rec, t0, t1, ["LP", "BI", "TILT"])

print("F. reunion: grieving face visible at sight (scenario 6 as scripted), first 8 s")
ag = Agent(K=K7, P=0.6); rec = run(ag, 10, lambda t: dict(BI=0.5, LD=0.4), lambda t: dict(distress=0.6), {at(1.5): {"greet": True}})
show("greeting at a grieving face", rec, 0, 7.5, ["LP", "CR", "BI", "FR"])
