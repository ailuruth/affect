"""TH1: no affective perpetuum mobile (conservative) and its breakdown with an internal rhythm. See PREDICTIONS.md."""
import json
import numpy as np

T, DT, TAU = 0.5, 0.01, 10.0
NSTEP = int(TAU / DT)

def gradU(z, o):
    g = z - o
    g[:, 0] += 0.4 * z[:, 0] * z[:, 1] ** 2
    g[:, 1] += 0.4 * z[:, 1] * z[:, 0] ** 2
    return g

def dUdt(z, o, odot):  # partial time derivative of U at fixed z
    return -np.sum((z - o) * odot, axis=1)

def run(proto, gamma, n=4000, burn=20, meas=40, seed=0):
    r = np.random.default_rng(seed); z = np.zeros((n, 2))
    W = []
    for c in range(burn + meas):
        w = np.zeros(n)
        for k in range(NSTEP):
            t = k * DT
            o, odot = proto(t)
            if c >= burn: w += dUdt(z, o, odot) * DT
            drift = -gradU(z, o) + gamma * np.stack([-z[:, 1], z[:, 0]], 1)
            z = z + drift * DT + np.sqrt(2 * T * DT) * r.standard_normal(z.shape)
        if c >= burn: W.append(w.mean())
    W = np.array(W)
    v = -W / TAU
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))

def fourier(seed):
    r = np.random.default_rng(seed); a = r.normal(0, 0.5, (2, 3)); b = r.normal(0, 0.5, (2, 3))
    w = 2 * np.pi / TAU * np.arange(1, 4)
    def p(t):
        o = (a * np.cos(w * t) + b * np.sin(w * t)).sum(1)
        od = (-a * w * np.sin(w * t) + b * w * np.cos(w * t)).sum(1)
        return o, od
    return p

def square(t):
    s = 1.0 if (t % TAU) < TAU / 2 else 0.0
    return np.array([s, 0.0]), np.zeros(2)  # jumps handled below

def rot(r_, w):
    def p(t):
        return np.array([r_ * np.cos(w * t), r_ * np.sin(w * t)]), np.array([-r_ * w * np.sin(w * t), r_ * w * np.cos(w * t)])
    return p

out = {}
res = [run(fourier(s), 0.0, n=1000, seed=s) for s in range(50)]
out["TH1a_random_max_v_over_SE"] = float(max(m / se for m, se in res))
out["TH1a_random_n_positive_beyond_2SE"] = int(sum(m > 2 * se for m, se in res))
# square wave: work is delivered at jumps; approximate with a steep logistic ramp
def smooth_square(t, k=50.0):
    ph = t % TAU
    s = 1 / (1 + np.exp(-k * (ph - 0.5))) - 1 / (1 + np.exp(-k * (ph - TAU / 2)))
    ds = k * np.exp(-k * (ph - 0.5)) / (1 + np.exp(-k * (ph - 0.5))) ** 2 - k * np.exp(-k * (ph - TAU / 2)) / (1 + np.exp(-k * (ph - TAU / 2))) ** 2
    return np.array([s, 0.0]), np.array([ds, 0.0])
m, se = run(smooth_square, 0.0, n=2000); out["TH1a_smile_schedule"] = dict(mean_v=m, se=se)
for r_ in (1.0, 2.0):
    for w in (0.5, -0.5):
        m, se = run(rot(r_, w), 1.0, n=2000)
        analytic = -(w * r_ ** 2 * (w - 1.0) / (1 + (w - 1.0) ** 2))
        out[f"TH1b_gamma1_r{r_}_w{w}"] = dict(mean_v=m, se=se, analytic_harmonic=analytic)
for w in (0.5,):
    m, se = run(rot(1.0, w), 0.0, n=2000); out["TH1_control_gamma0_r1_w0.5"] = dict(mean_v=m, se=se)
out["TH1c_ratio_r2_over_r1"] = out["TH1b_gamma1_r2.0_w0.5"]["mean_v"] / out["TH1b_gamma1_r1.0_w0.5"]["mean_v"]
print(json.dumps(out, indent=1))
