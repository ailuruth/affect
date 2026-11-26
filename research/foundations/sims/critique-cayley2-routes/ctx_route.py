"""K1. The context route: S_s's states (which know the partner's held level) enter S_f as context c~,
with no Lipschitz bound in c~ (s2.4: 'context c~ ... free inputs'), and role (from partner VAD) is in c~.
A c~-only term of the REN (no partner input w at all) times the role switch passes H_o as a transient.
The TTS then samples y at the agent's turn onset and holds it for the phrase (s2.8.5).

Everything else is the design's own: 30 Hz, v = sqrt(k) u, w = v - s, y = 2 sqrt(k) s, s strictly causal,
H_o first-order 4 s, knowledge = LP_60s(w + s) as in checks.py H2, S_s output 0, fast partner path 0
(both set to zero to isolate this route; adding them changes nothing below by more than their caps).

Partner: one voice channel (F0 level), held level l in [0,1] changing every ~20 min, per-phrase jitter.
Turns: partner speaks 3-8 s; agent onset 1-3 s after partner VAD offset (Claude latency, R15);
agent speaks 3-8 s; gap 0.3-1 s.
"""
import numpy as np
rng = np.random.default_rng(3)
fs, K = 30.0, 0.30
sk = np.sqrt(K)
T = int(8 * 3600 * fs)

# held levels
lev = np.zeros(T); t = 0
while t < T:
    L = int(rng.exponential(20 * 60 * fs)) + int(120 * fs)
    lev[t:t + L] = rng.uniform(0, 1); t += L
# turn structure
vad = np.zeros(T); u = np.zeros(T); onsets = []; t = 0; cur = lev[0]
while t < T - 30 * fs:
    dur = int(rng.uniform(3, 8) * fs)
    p = t
    while p < t + dur:                      # partner phrases ~2 s, zero-order held level
        pl = int(rng.uniform(1.5, 2.5) * fs)
        cur = lev[p] + rng.normal(0, 0.05)
        u[p:p + pl] = cur; p += pl
    vad[t:t + dur] = 1
    t += dur
    on = t + int(rng.uniform(1, 3) * fs); onsets.append(on)
    u[t:on] = cur
    end = on + int(rng.uniform(3, 8) * fs) + int(rng.uniform(0.3, 1) * fs)
    u[on:end] = cur
    t = end
u[t:] = cur
onsets = np.array([o for o in onsets if o < T])

a_o = 1 - np.exp(-1 / (4.0 * fs)); a_L = 1 - np.exp(-1 / (60.0 * fs))

def run(A):
    y = np.zeros(T); s = 0.0; lpo = 0.0; kn = 0.0
    for t in range(T):
        w = sk * u[t] - s
        y[t] = 2 * sk * s
        kn += a_L * ((w + s) - kn)          # S_s knowledge of v (H2's construction)
        role_floor = 1.0 - vad[t]           # role in c~: partner not speaking
        o = A * kn * role_floor             # c~-only REN output (no partner-input term)
        hpo = o - lpo; lpo += a_o * (o - lpo)
        s = hpo                             # used at t+1 (strictly causal)
    return y

def slope(x, y):
    x = x - x.mean(); y = y - y.mean(); return float(x @ y / (x @ x))

print("A = c~-path gain inside the REN (times gf*sigma <= 0.45; the REN's c~ gain is unbounded)")
for A in (0.0, 1.0, 2.0, 3.5):
    y = run(A)
    samp = y[onsets]                        # TTS phrase target at agent onset, held for the phrase
    lv = u[onsets]
    sl = slope(lv, samp); r = np.corrcoef(lv, samp)[0, 1] if A > 0 else 0.0
    # design's own metrics over the whole run
    n1, n10 = int(60 * fs), int(600 * fs)
    m = lambda x, n: x[: len(x) // n * n].reshape(-1, n).mean(1)
    zl = slope(u, y)
    s1 = slope(m(u, n1), m(y, n1)); s10 = slope(m(u, n10), m(y, n10))
    print(f"A={A:3.1f}: rendered turn-onset F0 target vs partner held level: slope {sl:+.3f}, r {r:.3f} | "
          f"design metrics: zero-lag slope {zl:+.3f}, 1-min {s1:+.3f}, 10-min {s10:+.3f} | "
          f"max |y| {np.max(np.abs(y)):.2f}")
print("claims: zero-lag in-phase <= 0.198; any instant (held) <= 0.150; 10-min <= 0.105")
