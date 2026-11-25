"""CT5: reading the other's slow state. See PREDICTIONS.md second batch."""
import json
import numpy as np
dt = 1 / 30; n = 30 * 600
def run(seed, arm):
    r = np.random.default_rng(seed); s = f = 0.0; S, Y = [], []
    for k in range(n):
        s += -s / 30 * dt + 0.3 * np.sqrt(dt) * r.standard_normal(); f += -(f - 0.8 * s) / 0.5 * dt + 0.3 * np.sqrt(dt) * r.standard_normal()
        S.append(s); Y.append(f + 0.05 * r.standard_normal())
    S, Y = np.array(S), np.array(Y); g = 0.8 if arm != "mismatch" else -0.8
    A = np.array([[1 - dt / 30, 0], [g * dt / 0.5, 1 - dt / 0.5]]); Q = np.diag([0.09 * dt, 0.09 * dt]); R = 0.05 ** 2; H = np.array([[0.0, 1.0]])
    x = np.zeros(2); P = np.eye(2); est = []
    for y in Y:
        x = A @ x; P = A @ P @ A.T + Q
        if arm == "deterministic":
            x[1] += 10 * dt * (y - x[1])
        else:
            Sg = (H @ P @ H.T)[0, 0] + R; K = (P @ H.T)[:, 0] / Sg; x = x + K * (y - x[1]); P = P - np.outer(K, H @ P)
        est.append(x[0])
    est = np.array(est); return float(1 - np.sum((est - S) ** 2) / np.sum((S - S.mean()) ** 2))
out = {arm: [run(sd, arm) for sd in range(10)] for arm in ("kalman", "deterministic", "mismatch")}
print(json.dumps({k: dict(mean=float(np.mean(v)), min=float(np.min(v)), max=float(np.max(v))) for k, v in out.items()}, indent=1))
