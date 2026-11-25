"""TH7: dark room vs predictability set point vs novelty seeking. See PREDICTIONS.md."""
import json
import numpy as np
eL = lambda n: 0.05 + 0.95 * np.exp(-n / 50); ERR = {"N": lambda n: 1.0, "B": lambda n: 0.05}
def forecast(ch, n, H=200, g=0.99):
    tot = 0.0; m = n
    for k in range(H):
        e = eL(m) if ch == "L" else ERR[ch](m); tot += g ** k * e
        if ch == "L": m += 1
    return tot
def agent1():
    n = 0; out = []
    for t in range(300):
        ch = min("LNB", key=lambda c: forecast(c, n)); out.append(ch)
        if ch == "L": n += 1
    return out
def agent2():
    n = 0; bp = 0.95; out = []; bps = []
    for t in range(300):
        errs = {"L": eL(n), "N": 1.0, "B": 0.05}; mu = -2 * (bp - 0.6)
        ch = max("LNB", key=lambda c: mu * ((1 - errs[c]) - bp) / 10); out.append(ch)
        bp += ((1 - errs[ch]) - bp) / 10; bps.append(bp)
        if ch == "L": n += 1
    return out, bps
def agent3():
    n = 0; out = []
    for t in range(300):
        errs = {"L": eL(n), "N": 1.0, "B": 0.05}; ch = max("LNB", key=errs.get); out.append(ch)
        if ch == "L": n += 1
    return out
a1 = agent1(); a2, bps = agent2(); a3 = agent3()
frac = lambda seq, c: float(np.mean([x == c for x in seq]))
res = dict(agent1={c: frac(a1, c) for c in "LNB"}, agent2={c: frac(a2, c) for c in "LNB"}, agent3={c: frac(a3, c) for c in "LNB"},
           agent2_mean_absdev_20_100=float(np.mean(np.abs(np.array(bps[20:100]) - 0.6))))
print(json.dumps(res, indent=1))
