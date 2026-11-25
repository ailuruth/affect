"""E: two-sided curiosity from a predictability set point. Parameters in PREDICTIONS.md."""
import json
import numpy as np

def run(setpoint=0.7):
    bp, n, log = 0.3, 0.0, []
    def eps_N(n): return 0.05 + 0.6 * np.exp(-n / 60)
    for minute in range(4 * 60 + 12 * 60 + 60):
        session = minute < 240 or minute >= 240 + 720
        if session:
            mu = -2 * (bp - setpoint)
            gains = {c: (1 - e - bp) / 10 for c, e in (("F", 0.05), ("N", eps_N(n)))}
            ch = max(gains, key=lambda c: mu * gains[c])
            e = 0.05 if ch == "F" else eps_N(n)
            if ch == "N": n += 1
            else: n *= np.exp(-1 / 360)
            log.append((minute, ch, bp, eps_N(n)))
            bp += (1 - e - bp) / 10
        else:
            n *= np.exp(-1 / 360); bp += (0.95 - bp) / 10
    return log

L = run(); s1 = [r for r in L if r[0] < 240]; s2 = [r for r in L if r[0] >= 960]
out = {}
out["E1_first10_F_frac"] = np.mean([r[1] == "F" for r in s1[:10]])
bored = [r for r in s1 + s2 if r[2] > 0.75 and r[3] > 0.06]
out["E1_bored_N_frac"] = float(np.mean([r[1] == "N" for r in bored])) if bored else None
out["E1_n_bored_steps"] = len(bored)
out["E2_hour1_mean_absdev"] = float(np.mean([abs(r[2] - 0.7) for r in s1[:60]]))
out["E3_hour4_mean_bp"] = float(np.mean([r[2] for r in s1[180:240]]))
out["E4_session2_mean_absdev"] = float(np.mean([abs(r[2] - 0.7) for r in s2]))
out["N_frac_by_hour_s1"] = [float(np.mean([r[1] == "N" for r in s1[h*60:(h+1)*60]])) for h in range(4)]
La = run(setpoint=1.0); out["E5_ablation_hour1_N_frac"] = float(np.mean([r[1] == "N" for r in La[:60]]))
print(json.dumps(out, indent=1))
