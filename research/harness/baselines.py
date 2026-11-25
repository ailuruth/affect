"""Published simple baselines, harness v2 (fixes REVIEW-1 B7, B8, S1; invalid windows dropped).
L2L methods work on 64-frame windows; REACT methods on REACT_CLIP-frame clips. Every method and the ground truth are
scored on one shared list of window starts per series (valid_starts). UNSPEC readings are fixed in HARNESS.md."""
import json, re
import numpy as np
import loader as Ld

T_WIN = 64; DELAY = 17
SPLITS = "research/harness/splits_v3.json"
_pid = re.compile(r"^(V\d+)_S\d+_I\d+_P(\d+)A?$")

def person(file_id):
    v, p = _pid.match(file_id).groups(); return f"{v}_P{p}"

def valid_starts(valid, length, first=DELAY, stride=None):
    """Window starts s with first <= s <= T-length, all frames [s-first, s+length) valid (so Delayed Mirror's source
    window is valid too). Non-overlapping by default."""
    T = len(valid); stride = stride or length; bad = np.concatenate([[0], np.cumsum(~valid)])
    s = np.arange(first, T - length + 1, stride)
    return s[(bad[s + length] - bad[s - first]) == 0]

class TrainBank:
    """Built from train-split file pairs only (REVIEW-1 B8): asserts every file id is in train and that no person in
    the bank is in `query_files`. Windows with any invalid frame are dropped."""
    def __init__(self, pair_ids, query_files=(), length=T_WIN):
        train = set(json.load(open(SPLITS))["files"]["train"])
        qp = {person(f) for f in query_files}
        S, Lw = [], []
        for (label, split, fs, fl) in pair_ids:
            assert fs in train and fl in train, (fs, fl)
            assert person(fs) not in qp and person(fl) not in qp
            spk, vs = Ld.load_aus(label, split, fs); lis, vl = Ld.load_aus(label, split, fl)
            n = min(len(spk), len(lis)); v = vs[:n] & vl[:n]
            for s in valid_starts(v, length, first=0): S.append(spk[s:s + length]); Lw.append(lis[s:s + length])
        self.spk = np.stack(S).astype(np.float32); self.lis = np.stack(Lw).astype(np.float32)
        self.median = np.median(self.lis.reshape(-1, self.lis.shape[-1]), axis=0)
        pooled = np.concatenate([self.spk, self.lis])          # REACT pools speaker and listener emotions
        self.mean_seq = pooled.mean(0); self.mean_fr = self.mean_seq.mean(0)

def _check(starts, T, length, first):
    assert all(first <= t <= T - length for t in starts), "window start out of range"

def l2l_median(bank, spk, starts):
    return np.broadcast_to(bank.median, (len(starts), T_WIN, len(bank.median))).copy()

def l2l_random(bank, spk, starts, rng):
    return bank.lis[rng.integers(0, len(bank.lis), len(starts))]

def l2l_nn(bank, spk, starts):
    _check(starts, len(spk), T_WIN, 0)
    Q = np.stack([spk[s:s + T_WIN] for s in starts]).reshape(len(starts), -1); B = bank.spk.reshape(len(bank.spk), -1)
    d = (Q * Q).sum(1)[:, None] - 2 * Q @ B.T + (B * B).sum(1)[None]
    return bank.lis[np.argmin(d, 1)]

def _smooth(x, k):
    if k <= 1: return x
    ker = np.ones(k) / k; pad = np.pad(x, ((k // 2, k // 2), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, j], ker, mode="valid") for j in range(x.shape[1])], 1)

def l2l_mirror(spk, starts, smooth_k=1):
    _check(starts, len(spk), T_WIN, 0); s = _smooth(spk, smooth_k); return np.stack([s[t:t + T_WIN] for t in starts])

def l2l_delayed_mirror(spk, starts, delay=DELAY, smooth_k=1):
    _check(starts, len(spk), T_WIN, delay); s = _smooth(spk, smooth_k)
    return np.stack([s[t - delay:t - delay + T_WIN] for t in starts])

# REACT 2023 run_baselines.py, on clips of `length` frames
def react_random(n, d, rng, length, num_pred=10):
    return rng.random((n, num_pred, length, d)).astype(np.float32)

def react_mime(spk, starts, length, num_pred=10):
    _check(starts, len(spk), length, 0); w = np.stack([spk[t:t + length] for t in starts]); return np.repeat(w[:, None], num_pred, 1)

def react_mean_seq(bank, n, num_pred=10):
    """bank must be built with length = the REACT clip length."""
    return np.broadcast_to(bank.mean_seq, (n, num_pred) + bank.mean_seq.shape).copy()

def react_mean_fr(bank, n, length, num_pred=10):
    return np.broadcast_to(bank.mean_fr, (n, num_pred, length, len(bank.mean_fr))).copy()
