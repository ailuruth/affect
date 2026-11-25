"""TH2: reading by synchronization; mimicry lesion spares reading. See PREDICTIONS.md."""
import json, sys
import numpy as np

NA, NB, NH = 4, 2, 10; N = NA + NB + NH
Tvec = np.array([0.05] * NA + [30.0] * NB + [1.0] * NH)
DT, SIG, L, MINUTES, FS = 0.001, 0.3, 10.0, 10, 10
ia, ib, ih = slice(0, NA), slice(NA, NA + NB), slice(NA + NB, N)

def make_landscape(seed):
    r = np.random.default_rng(seed)
    Uo, _ = np.linalg.qr(r.standard_normal((N, N))); Q = Uo @ np.diag(r.uniform(0.5, 2.0, N)) @ Uo.T
    J = r.standard_normal((N, N)); J = J - J.T; J *= 0.5 / np.linalg.norm(J, 2)
    m = r.uniform(-1.5, 1.5, (3, NH))
    return Q, J, m

def grad(x, Q, m):
    g = x @ Q.T
    h = x[..., ih]
    for j in range(3):
        e = np.exp(-np.sum((h - m[j]) ** 2, -1, keepdims=True) / 2)
        g[..., ih] += 1.5 * e * (h - m[j])
    s = np.sum(x ** 2, -1, keepdims=True)
    g += 2 * x * 0.1 * s * (2 + s) / (1 + s) ** 2
    return g

def run(seed, kappa, redraw=False):
    th = make_landscape(1000 + seed)          # B's (shared) model
    thA = make_landscape(5000 + seed) if redraw else th
    r = np.random.default_rng(seed)
    xA = np.zeros(N); xB = np.zeros(N); xh = np.zeros(N)
    M = np.eye(N) + th[1]; MA = np.eye(N) + thA[1]
    n = int(MINUTES * 60 / DT); every = int(1 / (FS * DT))
    rec = {"bA": [], "bh": [], "aA": [], "aB": []}
    for k in range(n):
        y = xA[ia] + 0.05 * r.standard_normal(NA)
        dA = -(MA @ grad(xA, thA[0], thA[2])) / Tvec
        dB = -(M @ grad(xB, th[0], th[2])) / Tvec
        dB[ia] += kappa * (xh[ia] - xB[ia]) / Tvec[ia]
        dh = -(M @ grad(xh, th[0], th[2])) / Tvec
        dh[ia] += L * (y - xh[ia]) / Tvec[ia]
        xA = xA + dA * DT + SIG * np.sqrt(DT) * r.standard_normal(N)
        xB = xB + dB * DT + SIG * np.sqrt(DT) * r.standard_normal(N)
        xh = xh + dh * DT
        if k % every == 0:
            rec["bA"].append(xA[ib].copy()); rec["bh"].append(xh[ib].copy()); rec["aA"].append(xA[ia].copy()); rec["aB"].append(xB[ia].copy())
    R = {k_: np.array(v) for k_, v in rec.items()}
    r2 = np.mean([1 - np.sum((R["bh"][:, i] - R["bA"][:, i]) ** 2) / np.sum((R["bA"][:, i] - R["bA"][:, i].mean()) ** 2) for i in range(NB)])
    cors, lags = [], []
    for i in range(NA):
        a, b = R["aA"][:, i] - R["aA"][:, i].mean(), R["aB"][:, i] - R["aB"][:, i].mean()
        cc = [np.corrcoef(a[: len(a) - l], b[l:])[0, 1] for l in range(0, 21)]
        cors.append(max(cc)); lags.append(int(np.argmax(cc)) / FS)
    return dict(seed=seed, kappa=kappa, redraw=redraw, r2=float(r2), face_corr=float(np.mean(cors)), lag=float(np.median(lags)))

if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        for kappa, redraw in ((3.0, False), (0.0, False), (3.0, True)):
            print(json.dumps(run(s, kappa, redraw)), flush=True)
