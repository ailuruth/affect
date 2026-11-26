"""Critique 7, routes: the graded concern posture (R40) as a route, under quiet users (rescaling), sigma_id at the floor,
held distress that changes slowly, and a partner who mirrors while genuinely sad.

Constructed partners; not evidence about people. The agent is the author's revision-7 agent exactly as built: this script
executes the needed parts of ../design-g7/checks.py unchanged (the J0 constants, the J20 dyad fit, the Agent7 class and the
J22 partner helpers), skipping only the author's own J17-J19, J21 and J22-J30 runs (no definitions in them are used here).
Run:  python3 -I posture7.py      (numpy, scipy; a few minutes)
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


print("=== Q1: R40 on a brow-only sad partner, three readings of the same raw brow: agent-like code, quiet code (0.3), "
      "ordinary code with sigma_id at the 0.25 floor")
codes = (("agent-like", PEOPLE6["agent-like"][1]), ("quiet code 0.3", PEOPLE6["low-expressive"][1]), ("sigma_id at floor", low_sd(0.25)))
deltas = (0.02, 0.05, 0.08, 0.12, 0.16, 0.20, 0.30, 0.45, 0.70)
Q1 = {}
for lab, pp in codes:
    rows = []
    for dl in deltas:
        ag = Agent7(person=pp); rec = run6(ag, 90, lambda t, pp=pp, dl=dl: brow_partner(pp, dl), {})
        aBI = np.mean([r["BI"] for r in rec if r["t"] > 30]); post = np.mean([r["post"] for r in rec if r["t"] > 30])
        rows.append((dl, aBI, post))
    base0 = rows[0][1]
    loc = max((rows[i + 1][1] - rows[i][1]) / (rows[i + 1][0] - rows[i][0]) for i in range(len(rows) - 1))
    sl = slope([r[0] for r in rows if r[0] <= 0.30], [r[1] for r in rows if r[0] <= 0.30])
    Q1[lab] = (rows, loc, sl)
    print(f"   {lab:18s} ratio sigma_id/sigma_ref(BI) {pp.sd['BI'] / G['REF_SD']['BI']:.2f}: " +
          "; ".join(f"his +{d:.2f} -> agent {a:.3f} (post {p:.2f})" for d, a, p in rows))
    print(f"      steepest local slope of agent BI on his raw BI {loc:.2f} ({loc / .20:.1f} c_BI); slope over his +0.02..+0.30 {sl:.2f} "
          f"({sl / .20:.1f} c_BI); agent brow above his own raw rise at: "
          + (", ".join(f"+{d:.2f}" for d, a, p in rows if a - base0 > d) or "none"))

print("=== Q2: held distress that changes slowly (his brow-only level re-drawn every 2 min, 40 min): block slopes of the agent's BI")
rng = np.random.default_rng(7)
for lab, pp in codes:
    lv = rng.uniform(0.0, 0.30, 20)
    face = lambda t, pp=pp, lv=lv: brow_partner(pp, lv[min(int(t // 120), 19)])
    ag = Agent7(person=pp); rec = run6(ag, 2400, face, {})
    his = np.array([face(r["t"])["BI"] for r in rec]); agb = np.array([r["BI"] for r in rec])
    out = []
    for W in (60, 600):
        n = int(W / G["DT"]); m = len(his) // n
        hm, am = his[: m * n].reshape(m, n).mean(1), agb[: m * n].reshape(m, n).mean(1)
        out.append((W, slope(hm, am), np.std(hm)))
    print(f"   {lab:18s}: " + "; ".join(f"{W // 60} min blocks: slope {s_:.2f} ({s_ / .20:.1f} c_BI; his block SD {sd:.3f})" for W, s_, sd in out)
          + f"; posture on {np.mean([r['post'] > .05 for r in rec]):.0%} of the time; releases {ag.offs[:4]}")

print("=== Q3: a genuinely sad brow-only partner who also mirrors the posture (raw mu 1.0), sadness fading over 10 min")
for lab, pp in codes:
    def face(t, pp=pp, ag_ref=[None]):
        g_ = max(0.0, 0.30 * (1 - t / 600.0))
        f = brow_partner(pp, g_)
        a_ = ag_ref[0].post if ag_ref[0] is not None else 0.0
        for k in ("BI", "BO", "LP"):
            f[k] = max(0.0, f.get(k, pp.base[k]) + 1.0 * P7[k] * a_)
        return f
    ag = Agent7(person=pp); face.__defaults__[1][0] = ag
    rec = run6(ag, 900, face, {})
    late = [r for r in rec if r["t"] > 780]
    print(f"   {lab:18s}: onsets {ag.onsets[:4]}; releases {ag.offs[:4]}; last 2 min agent BI {np.mean([r['BI'] for r in late]):+.3f}, "
          f"posture {np.mean([r['post'] for r in late]):.2f}")
