"""Checks for research/directional-influence-synthesis.md (D1-D5).
Run: python3 -I checks.py   (numpy, scipy)"""
import itertools, numpy as np
from collections import Counter
from scipy.stats import spearmanr

rng = np.random.default_rng(0)

def H(c):
    p = np.array(list(c.values()), float); p /= p.sum()
    return -(p * np.log2(p)).sum()

def MI(xs, ys):
    return H(Counter(xs)) + H(Counter(ys)) - H(Counter(zip(xs, ys)))

def spec_info(S, A):
    """Williams-Beer specific information I(S=s;A) for every s."""
    n = len(S); ps = Counter(S); pa = Counter(A); psa = Counter(zip(S, A))
    out = {}
    for s in ps:
        v = 0.0
        for a in pa:
            if psa[(s, a)] == 0: continue
            p_a_s = psa[(s, a)] / ps[s]; p_s_a = psa[(s, a)] / pa[a]
            v += p_a_s * (np.log2(1 / (ps[s] / n)) - np.log2(1 / p_s_a))
        out[s] = v
    return out

def pid_imin(S, A1, A2):
    n = len(S); ps = Counter(S)
    i1, i2 = spec_info(S, A1), spec_info(S, A2)
    red = sum(ps[s] / n * min(i1[s], i2[s]) for s in ps)
    m1, m2, m12 = MI(S, A1), MI(S, A2), MI(S, list(zip(A1, A2)))
    return dict(red=red, unq_p=m1 - red, unq_a=m2 - red, syn=m12 - m1 - m2 + red)

# D1/D2: agent a_t from partner p_{t-1} and own a_{t-1}
T = 200000
p = rng.integers(0, 2, T)
def run(rule):
    a = np.zeros(T, int); a[0] = rng.integers(0, 2)
    for t in range(1, T):
        a[t] = rule(p[t - 1], a[t - 1])
    S, A1, A2 = list(a[1:]), list(p[:-1]), list(a[:-1])
    te = MI(S, list(zip(A1, A2))) - MI(S, A2)
    rho = spearmanr(a[1:], p[:-1])[0]
    return pid_imin(S, A1, A2), te, rho
rules = {
    "copy":        lambda pp, aa: pp,
    "anti-copy":   lambda pp, aa: 1 - pp,
    "xor (avoid repeating pair pattern)": lambda pp, aa: pp ^ aa,
    "noisy anti (p=.8)": lambda pp, aa: (1 - pp) if rng.random() < .8 else pp,
}
print("D1/D2  target a_t; sources p_{t-1}, a_{t-1} (bits; Imin PID)")
for k, r in rules.items():
    pid, te, rho = run(r)
    print(f"  {k:36s} TE={te:.3f} red={pid['red']:.3f} unq_p={pid['unq_p']:.3f} "
          f"unq_a={pid['unq_a']:.3f} syn={pid['syn']:.3f}  spearman={rho:+.3f}")

# D3: Dall'Aglio - two countermonotone stages compose to comonotone
x = rng.standard_normal(100000)
y = -np.tanh(2 * x) + 0.05 * rng.standard_normal(x.size)   # strong sign flip
z = -np.sinh(y) + 0.05 * rng.standard_normal(x.size)        # second sign flip
print(f"D3  rho_S(x,y)={spearmanr(x,y)[0]:+.3f} rho_S(y,z)={spearmanr(y,z)[0]:+.3f} "
      f"rho_S(x,z)={spearmanr(x,z)[0]:+.3f}  (two flips = copy)")

# D4: shuffles of Min: deterministic maps (high MI), with a one-sided copula
#     ceiling C <= kappa*M + (1-kappa)*Pi (kappa=.5). Strip permutation sets the
#     global sign; strip orientation sets the local sign.
def shuffle(u, m, perm, flip):
    k = np.floor(u * m).astype(int); r = u * m - k
    return perm[k] / m + ((1 - r) if flip else r) / m
def ceiling_violation(u, v, kap=0.5):
    g = np.linspace(0.01, 0.99, 99)
    su, sv = np.sort(u), np.sort(v)
    C = np.array([[np.mean((u <= a) & (v <= b)) for b in g] for a in g])
    A, B = np.meshgrid(g, g, indexing="ij")
    return np.max(C - (kap * np.minimum(A, B) + (1 - kap) * A * B))
u = rng.random(100000)
for m in (4, 16, 64):
    for pname, perm in (("reversed", np.arange(m)[::-1]), ("random", rng.permutation(m))):
        for flip in (False, True):
            v = shuffle(u, m, perm, flip)
            mi = MI(list(np.floor(u * 64).astype(int)), list(np.floor(v * 64).astype(int)))
            print(f"D4  m={m:2d} strips {pname:8s} {'decr' if flip else 'incr'}: "
                  f"rho_S={spearmanr(u, v)[0]:+.3f} MI(64-bin)={mi:.2f} "
                  f"max[C-ceiling]={ceiling_violation(u, v):+.4f}")
for name, v in (("copy M", u.copy()), ("anti-copy W", 1 - u), ("independent", rng.random(u.size))):
    print(f"D4  {name:12s}: rho_S={spearmanr(u, v)[0]:+.3f} max[C-ceiling]={ceiling_violation(u, v):+.4f}")

# D5: frequency-domain one-sided ceiling Re H(jw) <= kappa. A delayed sign flip
#     is a copy in the band w = pi/tau; a low-passed one can satisfy the ceiling.
w = np.linspace(1e-3, 200, 400001)
for a, tau in ((50, .5), (2, .5), (0.5, .5), (0.5, 0.05)):
    Hs = -(a / (1j * w + a)) * np.exp(-1j * w * tau)
    print(f"D5  -LP(a={a})*delay({tau}s): DC gain {Hs[0].real:+.2f}, max_w Re H = {Hs.real.max():+.3f}")
