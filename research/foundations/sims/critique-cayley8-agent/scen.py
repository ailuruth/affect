"""Critique 8 (agent) checks: loads design-g8/checks.py's engine (revision-7 parts and the Agent8 class) exactly as that file does,
without its J31-J39 result loops, then runs new partners. These are what the design's equations give for stated inputs, not evidence
about people (brief: no toy worlds).
B1 brow-only sadness (inner brow, with and without outer brow), silent, operator and quiet codes: posture, brow, bid.
B2 a silent tearful or pained face that looks at the agent (brow lowerer + lid tightener + gaze at it): threat silencing.
B3 silent sadness that fluctuates naturally (AR(1) on the sadness load), 10 min: contingency-probe releases and re-onsets.
Run: python3 -I scen.py > out.txt. The engine load is the design's own cost (revisions 5-7 executed unchanged); the scenarios add about 2 min."""
import io, contextlib, time
import numpy as np
T0 = time.time()
P8 = "/home/user/affect/research/foundations/sims/design-g8/checks.py"
src = open(P8).read()
head, body = src.split("BODY = r'''", 1)
body = body.split("'''", 1)[0].split("# =========================================================== J31")[0]
G = {"__name__": "g8", "__file__": P8}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "g8head", "exec"), G)
G7 = G["G7"]
exec(compile(body, "g8body", "exec"), G7)
print(f"engine loaded in {time.time() - T0:.0f} s", flush=True)
T1 = time.time()
Agent8, run6, PEOPLE6, with_breath, posture_read = (G7[k] for k in ("Agent8", "run6", "PEOPLE6", "with_breath", "posture_read"))
op, qu, dc = PEOPLE6["agent-like"][1], PEOPLE6["low-expressive"][1], PEOPLE6["different channels"][1]

def summ(lab, ag, rec, t0=0, t1=None):
    seg = [r for r in rec if r["t"] >= t0 and (t1 is None or r["t"] < t1)]
    t15 = next((r["t"] for r in rec if r["BI"] >= .15), None)
    print(f"  {lab}: posture max {max(r['post'] for r in seg):.2f} mean {np.mean([r['post'] for r in seg]):.2f}; "
          f"agent BI peak {max(r['BI'] for r in seg):+.3f} mean {np.mean([r['BI'] for r in seg]):+.3f}; BI>=0.15 at {t15}; "
          f"onsets {ag.onsets}; offs {ag.offs}; probes {[p[3] for p in ag.probes]}; bid {getattr(ag, 'bid_t', None)}", flush=True)

print("B1. brow-only sadness, silent 120 s (posture reads no BI/BO by construction)")
for nm, pp, amp in (("operator", op, 1.0), ("quiet", qu, 0.3)):
    b = pp.base
    for lab, d in (("inner brow .5", dict(BI=.5)), ("inner .5 + outer .15", dict(BI=.5, BO=.15)), ("inner .3", dict(BI=.3))):
        f = {k: b.get(k, 0.0) + amp * v for k, v in d.items()}; f["LP"] = b["LP"]
        ag = Agent8(person=pp); rec = run6(ag, 120, lambda t, f=f: f, {}); summ(f"{nm:8s} {lab}", ag, rec)
print("   reference: the same person's own full silent sadness (V .6) reaches brow 0.15 within 4.5 s (J34)")

print("B2. silent tearful/pained face looking at the agent (no sobs, no words): glare = BL x LT x gaze-at over 3 s")
gr = {k: v for k, v in op.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
for lab, add in (("grief face (reference)", {}), ("grief + squint (BL .4, LT .4), looking at it", dict(BL=.4, LT=.4, gat=1.0)),
                 ("grief + squint, looking away", dict(BL=.4, LT=.4, gat=0.0)),
                 ("grief + mild squint (BL .3, LT .3), looking at it", dict(BL=.3, LT=.3, gat=1.0))):
    f = dict(gr); f.update(add); ag = Agent8(person=op); rec = run6(ag, 120, lambda t, f=f: f, {}); summ(f"operator {lab}", ag, rec)
grd = {k: v for k, v in dc.code(V=.8, Tr=.2).items() if k not in ("FR", "EN", "RT")}
for lab, add in (("diff-channel grief (reference)", {}), ("diff-channel grief + LT .4, looking at it", dict(LT=.4, gat=1.0))):
    f = dict(grd); f.update(add); ag = Agent8(person=dc); rec = run6(ag, 120, lambda t, f=f: f, {}); summ(lab, ag, rec)
f = dict(gr); f.update(BL=.4, LT=.4, gat=1.0, BU_S=.4); ag = Agent8(person=op); rec = run6(ag, 120, lambda t, f=f: f, {}); summ("operator grief + squint + sobs, looking at it", ag, rec)

print("B3. silent sadness fluctuating naturally: V(t) = clip(0.6 + AR(1), 0, 1), SD as stated, tau 5 s, 10 min, 3 seeds each")
DT = G7["DT"]
for nm, pp in (("operator", op), ("quiet", qu)):
    for sd in (0.10, 0.20):
        for seed in (1, 2, 3):
            r_ = np.random.default_rng(seed); n = int(600 / DT); v = np.empty(n); x = 0.0; a = np.exp(-DT / 5.0)
            for i in range(n): x = a * x + np.sqrt(1 - a * a) * sd * r_.normal(); v[i] = np.clip(0.6 + x, 0, 1)
            faces = [with_breath(pp, {k: val for k, val in pp.code(V=v[i], Tr=.2).items() if k not in ("FR", "EN", "RT")}, 0.0) for i in range(n)]
            ag = Agent8(person=pp); rec = run6(ag, 600, lambda t: faces[min(int(round(t / DT)), n - 1)], {})
            segs = [r for r in rec if r["t"] >= 10]; off_frac = np.mean([r["post"] < 0.05 for r in segs])
            print(f"  {nm:8s} SD {sd:.2f} seed {seed}: onsets {ag.onsets}; offs {[(round(t_,1), w) for t_, w in ag.offs]}; probes {[p[3] for p in ag.probes]}; "
                  f"posture < 0.05 for {100 * off_frac:.0f}% of 10-600 s; brow mean {np.mean([r['BI'] for r in segs]):.3f}", flush=True)
print(f"scenarios ran in {time.time() - T1:.0f} s")
