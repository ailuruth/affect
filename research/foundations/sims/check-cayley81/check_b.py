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
def lag_face(pp, mode, mu, par, sad_until=40.0, V0=.8, m0=0.0):
    st = {"m": m0, "h": []}
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
def run_lag(pp, mode, mu, par, dur, m0=0.0):
    ag = Agent81(person=pp); rec = run6(ag, dur, lag_face(pp, mode, mu, par, m0=m0)(ag), {})
    on = lambda t0, t1: np.mean([r["post"] > 0.05 for r in rec if t0 <= r["t"] < t1])
    return ag, rec, on
print("=== C1b: continuous slow answerer (his V starts at his sadness level 0.8/mu and then follows mu x low-pass(look)); 60 min")
for lab, pp in (CODES[0], CODES[2]):
    for mu, par in ((1.0, 150), (1.0, 300), (1.0, 600), (1.5, 120), (1.2, 240)):
        ag, rec, on = run_lag(pp, "lp", mu, par, 3600, m0=min(1.0, 0.8 / mu))
        print(f"   {lab:18s} low-pass tau {par:3d} s mu {mu}: offs {ag.offs[:3]}, tests {tests_line(ag)[:5]}, look on in 50-60 min {100*on(3000,3600):.0f}%, BI last 10 min {np.mean([r['BI'] for r in rec if r['t']>=3000]):+.3f}", flush=True)
'''
G8 = {"__name__": "chk"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(pre + "pass\n", "pre81", "exec"), G8)
G = G8["G"]
print(f"[engine loaded in {time.time()-T0:.0f} s]", flush=True)
exec(compile(body + NEW, "chk81", "exec"), G)
print(f"[done in {time.time()-T0:.0f} s]")
