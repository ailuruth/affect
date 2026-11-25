"""CT3: Bode sensitivity integral and temperament. See PREDICTIONS.md."""
import json
import numpy as np
w = np.linspace(1e-4, 1e3, 2_000_000); s = 1j * w
P = 1 / ((s + 0.1) * (0.1 * s + 1))
Ks = {"K1": 1 + 0.5 / s, "K2": 4 * (s + 0.2) / (s + 2) + 0.2 / s}
def stable(num_den):
    return bool(np.all(np.real(np.roots(num_den)) < 0))
# characteristic polynomials (1 + K P = 0) numerators:
# K1: (s+0.5)/s ; P = 1/((s+0.1)(0.1s+1)) -> s(s+0.1)(0.1s+1) + (s+0.5)
c1 = np.polyadd(np.polymul([1, 0], np.polymul([1, 0.1], [0.1, 1])), [1, 0.5])
# K2 = [4s(s+0.2) + 0.2(s+2)] / [s(s+2)] -> s(s+2)(s+0.1)(0.1s+1) + 4s(s+0.2) + 0.2(s+2)
num2 = np.polyadd(np.polymul([4, 0], [1, 0.2]), [0.2, 0.4]); den2 = np.polymul([1, 0], [1, 2])
c2 = np.polyadd(np.polymul(den2, np.polymul([1, 0.1], [0.1, 1])), num2)
out = {}
for name, K, cp in (("K1", Ks["K1"], c1), ("K2", Ks["K2"], c2)):
    S = 1 / (1 + K * P); lS = np.log(np.abs(S))
    I = float(np.trapezoid(lS, w)); Iabs = float(np.trapezoid(np.abs(lS), w))
    out[name] = dict(stable=stable(cp), integral=I, abs_integral=Iabs, ratio=I / Iabs, peak_freq=float(w[np.argmax(np.abs(S))]), peak=float(np.abs(S).max()))
out["peak_freq_ratio"] = max(out["K1"]["peak_freq"], out["K2"]["peak_freq"]) / min(out["K1"]["peak_freq"], out["K2"]["peak_freq"])
print(json.dumps(out, indent=1))
