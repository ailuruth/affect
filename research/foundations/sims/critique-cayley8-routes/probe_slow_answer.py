"""Critique 8, routes, area 1: the contingency probe against a partner who answers the agent's concern SLOWLY in his own code.

Revision 8 lets the posture read only channels it does not write (R_p), so a mirror of the posture on BI, BO, LP cannot hold it
(J33). A partner can still answer the agent's concern look on the channels it does read: his own sad face in his own code (lip
depressor, chin raise, brow lowerer, lip press), as critique 6's P4 'aww'. Revision 8's answer is the contingency probe: after
180 s held by his face alone, halve the posture for 8 s; release if the mean of his V_p over the probe's last 4 s is < 0.8 x its
mean over the 3 s before. The author's J33 tests an answer that follows the posture INSTANTLY (P4b-d: released at 190.5 s).
Critique 7's S1 used contagion-like mirrors with time constants of 90-240 s. Here the answer in his own code follows the posture
through a first-order lag tau (5-90 s): his genuine sadness ends at 40 s; afterwards his face is only his answer.

The agent is the author's Agent8 exactly as built (load8.py executes ../design-g8/checks.py up to its definitions; nothing
changed). Constructed partners; not evidence about people.
Run:  python3 -I -u probe_slow_answer.py     (numpy, scipy; the load of revisions 5-8 takes most of the time)
"""
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "load8.py")).read())
Agent8, run6, PEOPLE6, low_sd, DT = G["Agent8"], G["run6"], G["PEOPLE6"], G["low_sd"], G["DT"]
import numpy as np

CODES = (("operator (agent-like)", PEOPLE6["agent-like"][1]), ("quiet 0.3", PEOPLE6["low-expressive"][1]),
         ("different channels", PEOPLE6["different channels"][1]))
NOV = ("FR", "EN", "RT")


def run_answer(pp, mu, tau, dur=900, sad_until=40.0):
    """genuine sadness V .8 in his own code until sad_until; after it, his face = his own code at V = mu x lp_tau(posture shown)"""
    ag = Agent8(person=pp); st = {"m": 0.0}
    sad = {k: v for k, v in pp.code(V=.8).items() if k not in NOV}
    def face(t, ag=ag):
        a = ag.post
        st["m"] = a if tau == 0 else st["m"] + (a - st["m"]) * (1 - np.exp(-DT / tau))
        if t < sad_until: return dict(sad)
        return {k: v for k, v in pp.code(V=mu * st["m"]).items() if k not in NOV}
    rec = run6(ag, dur, face, {})
    late = [r for r in rec if r["t"] > dur - 120]
    his = [face_bi for face_bi in []]
    return ag, rec, float(np.mean([r["post"] for r in late])), float(np.mean([r["BI"] for r in late]))


print("=== P1: concern answered slowly in his own code (his genuine sadness ends at 40 s); 15 min")
OUT = {}
for lab, pp in CODES:
    for mu in (0.6, 1.0):
        for tau in (0, 5, 15, 30, 60, 90):
            ag, rec, pl, bl = run_answer(pp, mu, tau)
            OUT[(lab, mu, tau)] = (ag.offs, ag.probes, pl, bl)
            onf = np.mean([r["post"] > .05 for r in rec if r["t"] > 60])
            print(f"   {lab:22s} mu {mu:.1f} tau {tau:3d} s: offs {ag.offs[:4]}; probes {[(p[0], p[1], p[2], p[3]) for p in ag.probes][:5]}; "
                  f"onsets {ag.onsets[:4]}; posture on after 60 s {onf:.0%}; last 2 min posture {pl:.2f}, agent BI {bl:+.3f}", flush=True)
held = [(k, v[2]) for k, v in OUT.items() if v[2] > 0.3]
print(f"   held at 15 min (posture > 0.3 in the last 2 min): {len(held)} of {len(OUT)}: " + "; ".join(f"{k[0]} mu {k[1]} tau {k[2]}" for k, _ in held))

print("=== P2: genuine steady sadness with natural slow fluctuation (his V = 0.6 + OU, SD s, tau 10 s), 15 min: does the probe release a "
      "genuinely sad person by chance, and what then")
rng = np.random.default_rng(83)
for lab, pp in CODES:
    for sdv in (0.05, 0.10):
        rel, offl, onl = 0, [], []
        for seed in range(4):
            r_ = np.random.default_rng(100 + seed); st = {"v": 0.0, "t": -1}
            def face(t, pp=pp, st=st, r_=r_, sdv=sdv):
                if t != st["t"]: st["v"] += -st["v"] * DT / 10 + sdv * np.sqrt(2 * DT / 10) * r_.normal(); st["t"] = t
                return {k: v for k, v in pp.code(V=float(np.clip(0.6 + st["v"], 0, 1))).items() if k not in NOV}
            ag = Agent8(person=pp); rec = run6(ag, 900, face, {})
            offl.append([o for o in ag.offs]); onl.append(ag.onsets)
            rel += any(o[1] == "probe" for o in ag.offs)
            on_frac = np.mean([r["post"] > .05 for r in rec if r["t"] > 10])
            print(f"   {lab:22s} SD {sdv:.2f} seed {seed}: onsets {ag.onsets[:6]}; offs {ag.offs[:6]}; probes {[p[3] for p in ag.probes]}; on {on_frac:.0%}", flush=True)
        print(f"   -> {lab}, SD {sdv:.2f}: released by the probe in {rel} of 4 runs")
