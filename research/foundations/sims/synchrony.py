"""Shared synchrony scoring (Moulder et al. 2018 global mean |Fisher z| of WCC; segment-shuffle and data-sliding surrogates). Copied verbatim from costate/sim_c_mimicry.py."""
import numpy as np

def wcc_score(a, b, W=300, winc=50, L=50):
    zs = []
    for w0 in range(L, len(a) - W - L, winc):
        x = a[w0:w0 + W]; x = (x - x.mean()) / x.std()
        for lag in range(-L, L + 1):
            y = b[w0 + lag:w0 + lag + W]; y = (y - y.mean()) / y.std()
            rr = np.clip((x * y).mean(), -0.999999, 0.999999); zs.append(abs(np.arctanh(rr)))
    return float(np.mean(zs))


def surrogates(a, b, kind, n, rng):
    out = []
    for _ in range(n):
        if kind == "segment":
            m = 300; segs = [b[i:i + m] for i in range(0, len(b) - len(b) % m, m)]; rng.shuffle(segs); bb = np.concatenate(segs)
            aa = a[:len(bb)]
        else:
            cut = rng.integers(int(0.2 * len(b)), int(0.8 * len(b))); bb = np.concatenate([b[cut:], b[:cut]]); aa = a
        out.append(wcc_score(aa, bb))
    return np.array(out)
