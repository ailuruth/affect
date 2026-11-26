"""Independent check of revision 8.1's two fixes (face-only cap; squint drop). Loads design-g81/checks.py's engine and Agent81
unchanged (its K1-K5 loops are skipped) and runs only new constructed partners. Run: python3 -I check.py > out.txt"""
import io, os, time, contextlib
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "design-g81", "checks.py")).read()
pre, rest = SRC.split("BODY81 = r'''", 1)
body, _ = rest.split("# =========================================================== K1", 1)
pre = pre.replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = ' + repr(os.path.join(HERE, "..", "design-g81")))
NEW = r'''
def lag_face(pp, mode, mu, par, sad_until=40.0, V0=.8):
    st = {"m": 0.0, "h": []}
    sad = {k: v for k, v in pp.code(V=V0).items() if k not in NOV}
    def mk(ag):
        def face(t):
            a = ag.post; st["h"].append(a)
            if mode == "lp": st["m"] = st["m"] + (a - st["m"]) * (1 - np.exp(-DT / par)); x = st["m"]
            else: n = int(round(par / DT)); x = st["h"][-n - 1] if len(st["h"]) > n else 0.0
            if t < sad_until: return dict(sad)
            return {k: v for k, v in pp.code(V=float(np.clip(mu * x, 0, 1))).items() if k not in NOV}
        return face
    return mk
def run_lag(pp, mode, mu, par, dur):
    ag = Agent81(person=pp); rec = run6(ag, dur, lag_face(pp, mode, mu, par)(ag), {})
    on = lambda t0, t1: np.mean([r["post"] > 0.05 for r in rec if t0 <= r["t"] < t1])
    return ag, rec, on
print("=== C1: answering concern beyond the author's range (sadness V .8 until 40 s; then his code at V = mu x lag(look)); 60 min")
for lab, pp in (CODES[0], CODES[2]):
    for mode, mu, par in (("lp", 1.0, 300), ("lp", 1.0, 400), ("lp", 1.0, 600), ("lp", 2.0, 60), ("lp", 2.0, 90), ("lp", 3.0, 90), ("lp", 2.0, 180)):
        ag, rec, on = run_lag(pp, mode, mu, par, 3600)
        print(f"   {lab:18s} low-pass tau {par:3d} s mu {mu}: offs {ag.offs[:3]}, tests {tests_line(ag)[:5]}, look on in 50-60 min {100*on(3000,3600):.0f}%, BI last 10 min {np.mean([r['BI'] for r in rec if r['t']>=3000]):+.3f}", flush=True)
print("=== C2: pure-delay answerer (his face = his code at V = mu x look(t - d)); 30 min")
for lab, pp in (CODES[0], CODES[2]):
    for d in (10, 30, 90, 150):
        ag, rec, on = run_lag(pp, "delay", 1.0, d, 1800)
        print(f"   {lab:18s} delay {d:3d} s: onsets {len(ag.onsets)}, offs kinds {sorted(set(o[1] for o in ag.offs))} n {len(ag.offs)}, look on in 20-30 min {100*on(1200,1800):.0f}%", flush=True)
print("=== C3: steady genuine silent sadness (V .6), 60 min: test times and look withdrawn")
for lab, pp in CODES:
    f = {k: v for k, v in pp.code(V=.6, Tr=.2).items() if k not in NOV}
    ag = Agent81(person=pp); rec = run6(ag, 3600, lambda t, f=f: f, {})
    print(f"   {lab:18s}: tests {[(p[0], p[5]) for p in ag.probes]}, releases {len(ag.offs)}, look < 0.05 for {sum(r['post']<0.05 for r in rec if r['t']>10)*DT:.0f} s of 3600", flush=True)
print("=== C4: anger at the agent with a chin raise or lip depressor (channels the squint drop keeps), 180 s, rev 8 vs 8.1")
for kind, pp in (("operator", CODES[0][1]), ("quiet", CODES[1][1]), ("diff-channel", CODES[2][1])):
    for add in (dict(CHR=.2), dict(CHR=.4), dict(LD=.3), dict(CHR=.3, LD=.2)):
        f = dict(BL=.6, LT=.5, gat=1.0, EN=.85, LP=.05); f.update(add)
        res = []
        for mk in (MK8, MK81):
            ag = mk(pp); rec = run6(ag, 180, lambda t, f=f: f, {}); res.append((max(r["post"] for r in rec), ag.onsets[:1]))
        print(f"   {kind:12s} anger + {add}: rev 8 posture max {res[0][0]:.2f} | 8.1 posture max {res[1][0]:.2f}, on at {res[1][1]}", flush=True)
print("=== C5: different-channel user frowning and squinting (BL .6, LT .5) who follows the agent's gaze (his gaze-at = 1 - 1.0 x look); glances away 5-8 s; 15 min")
pp = CODES[2][1]
for base in (dict(BL=.6, LT=.5), dict(BL=.35, LT=.4, LPR=.15)):
    ag = Agent81(person=pp)
    def face(t, ag=ag, base=base):
        f = dict(base); f["gat"] = 0.0 if 5 <= t < 8 else float(np.clip(1 - 1.0 * ag.post, 0, 1)); return f
    rec = run6(ag, 900, face, {})
    print(f"   {base}: onsets {ag.onsets[:3]}, offs {ag.offs[:3]}, look on {100*np.mean([r['post']>0.05 for r in rec]):.0f}% of 15 min", flush=True)
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time()-T0:.0f} s]", flush=True)
exec(compile(body + NEW, "chk81", "exec"), G)
print(f"[done in {time.time()-T0:.0f} s]")
