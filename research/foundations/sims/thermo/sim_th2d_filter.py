"""TH2d: EnKF with the agent's own model, to test whether the hidden body is observable. See PREDICTIONS.md."""
import json, sys
import numpy as np
from sim_th2_sync import make_landscape, grad, N, NA, NB, ia, ib, Tvec, DT, SIG, MINUTES, FS

def run(seed, redraw=False, M=100, every=10):
    th = make_landscape(1000 + seed); thA = make_landscape(5000 + seed) if redraw else th
    r = np.random.default_rng(seed); re = np.random.default_rng(10_000 + seed)
    xA = np.zeros(N); E = np.zeros((M, N))
    MA = np.eye(N) + thA[1]; Mm = np.eye(N) + th[1]
    n = int(MINUTES * 60 / DT); rec_every = int(1 / (FS * DT)); bA, bh = [], []
    R = 0.05 ** 2
    for k in range(n):
        xA = xA + (-(MA @ grad(xA, thA[0], thA[2])) / Tvec) * DT + SIG * np.sqrt(DT) * r.standard_normal(N)
        E = E + (-(grad(E, th[0], th[2]) @ Mm.T) / Tvec) * DT + SIG * np.sqrt(DT) * re.standard_normal((M, N))
        if k % every == 0:
            y = xA[ia] + 0.05 * r.standard_normal(NA)
            X = E - E.mean(0); Hx = X[:, ia]
            Pxy = X.T @ Hx / (M - 1); Pyy = Hx.T @ Hx / (M - 1) + R * np.eye(NA)
            K = Pxy @ np.linalg.inv(Pyy)
            yp = y + 0.05 * re.standard_normal((M, NA))
            E = E + (yp - E[:, ia]) @ K.T
        if k % rec_every == 0:
            bA.append(xA[ib].copy()); bh.append(E.mean(0)[ib].copy())
    bA, bh = np.array(bA), np.array(bh)
    r2 = np.mean([1 - np.sum((bh[:, i] - bA[:, i]) ** 2) / np.sum((bA[:, i] - bA[:, i].mean()) ** 2) for i in range(NB)])
    return dict(seed=seed, redraw=redraw, r2=float(r2))

if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        for red in (False, True):
            print(json.dumps(run(s, red)), flush=True)
