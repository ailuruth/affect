"""TH7b: fair dark-room test (learnable asymptote below boring). See PREDICTIONS.md."""
import json
import numpy as np
eL = lambda n: 0.01 + 0.99 * np.exp(-n / 50)
def forecast(ch, n, H=200, g=0.99):
    tot, m = 0.0, n
    for k in range(H):
        e = eL(m) if ch == "L" else (1.0 if ch == "N" else 0.05); tot += g ** k * e
        if ch == "L": m += 1
    return tot
n = 0; seq = []
for t in range(300):
    ch = min("LNB", key=lambda c: forecast(c, n)); seq.append(ch)
    if ch == "L": n += 1
print(json.dumps(dict(B_frac=seq.count("B") / 300, L_frac=seq.count("L") / 300, forecast_L0=forecast("L", 0), forecast_B=forecast("B", 0)), indent=1))
