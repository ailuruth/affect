"""Critique 7, routes: a partner whose mirror of the concern posture is slow (his brow follows the posture through a low-pass of
time constant tau_m, as mood contagion would), against the mirror removal (current a while on; a_rec decaying over 60 s after),
the sensitized 0.5-s re-onset and the 3-min face-only failsafe.

Constructed partners; not evidence about people. The agent is the author's revision-7 agent exactly as built: this script
executes the needed parts of ../design-g7/checks.py unchanged (the J0 constants, the J20 dyad fit, the Agent7 class and the
J22 partner helpers), skipping only the author's own J17-J19, J21 and J22-J30 runs (no definitions in them are used here).
Run:  python3 -I posture7_slowmirror.py      (numpy, scipy; a few minutes)
"""
import io, os, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P7SRC = os.path.join(HERE, "..", "design-g7", "checks.py")
L = open(P7SRC).read().split("\n")
idx = {k: next(i for i, s in enumerate(L) if s.startswith(k)) for k in (
    "# =========================================================== J17", "# =========================================================== agent part",
    "# =========================================================== J21", "# =========================================================== the revision-7 agent",
    "# =========================================================== J22", "cases = [")}
src = "\n".join(L[:idx["# =========================================================== J17"]]
                + L[idx["# =========================================================== agent part"]:idx["# =========================================================== J21"]]
                + L[idx["# =========================================================== the revision-7 agent"]:idx["cases = ["]])
G = {"__name__": "g7", "__file__": P7SRC}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "checks_g7_parts", "exec"), G)
Agent7, run6, PEOPLE6, low_sd, slope = G["Agent7"], G["run6"], G["PEOPLE6"], G["low_sd"], G["slope"]
P7 = G["P7"]


def brow_partner(pp, delta):
    """his resting face with only the inner brow raised by delta (raw units, his own code's channel)"""
    return {"BI": pp.base["BI"] + delta, "LP": pp.base["LP"]}



import math
print("=== S1: slow mirror. His genuine sadness (his code at V 0.8) ends at 40 s; from then on his face is neutral plus mu x P_c x"
      " lp_tau_m(the agent's shown posture), raw units. 900 s.")
codes = (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor", low_sd(0.25)))
for lab, pp in codes:
    for tau_m in (30.0, 90.0, 240.0):
        for mu in (1.0, 1.5):
            ag = Agent7(person=pp)
            sad = {k: v for k, v in pp.code(V=.8).items() if k not in ("FR", "EN", "RT")}
            neu = {k: v for k, v in pp.code().items() if k not in ("FR", "EN", "RT")}
            st = {"m": 0.0}
            def face(t, ag=ag, st=st, mu=mu, tau_m=tau_m, sad=sad, neu=neu):
                st["m"] += (ag.post - st["m"]) * G["DT"] / tau_m
                if t < 40: return dict(sad)
                f = dict(neu)
                for k in ("BI", "BO", "LP"): f[k] = max(0.0, f.get(k, 0.0) + mu * P7[k] * st["m"])
                return f
            rec = run6(ag, 900, face, {})
            late = [r for r in rec if r["t"] > 600]
            on_frac = np.mean([r["post"] > .05 for r in late])
            print(f"   {lab:18s} tau_m {tau_m:5.0f} s mu {mu:.1f}: onsets {[round(x) for x in ag.onsets[:8]]}{' ...' if len(ag.onsets) > 8 else ''} "
                  f"({len(ag.onsets)} in all); releases {[(round(a), b[0]) for a, b in ag.offs[:6]]}; 600-900 s: posture on {on_frac:.0%}, "
                  f"agent BI {np.mean([r['BI'] for r in late]):+.3f}, his BI above neutral {mu * P7['BI'] * st['m']:+.3f} (end)")
