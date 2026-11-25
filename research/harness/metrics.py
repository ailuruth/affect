"""Published metrics and E3 synchrony, harness v2 (fixes REVIEW-1 B1-B3, B6, S2, S3 and the FD/NaN notes).
Definitions and sources are in HARNESS.md. Readings the sources leave unspecified are marked UNSPEC and were fixed
before any scoring. Arrays: series (T, d); windows (N, T, d); validity masks are boolean (T,)."""
import numpy as np
from scipy import linalg
from scipy.cluster.vq import kmeans2

L2L_SEQ = 256     # UNSPEC (L2L App. D, summary only: "256 length test sequences") -> TLCC and SI on 256-frame sequences
REACT_CLIP = 750  # REACT published clip length in frames

# ---------- Learning to Listen (Ng et al. 2022, Sec. 5.1) ----------
def l2(pred, gt):
    """UNSPEC aggregation -> mean over frames of per-frame Euclidean distance, mean over windows."""
    return float(np.linalg.norm(pred - gt, axis=-1).mean())

def frechet(a_windows, b_windows, eps=1e-6):
    """UNSPEC estimation -> one Gaussian per set over flattened T*d windows; standard FID formula; pytorch-fid style
    eps fallback if sqrtm is not finite (logged in the returned flag)."""
    A = a_windows.reshape(len(a_windows), -1); B = b_windows.reshape(len(b_windows), -1)
    assert len(A) > A.shape[1] and len(B) > B.shape[1], "FD needs more windows than T*d"
    mu_a, mu_b = A.mean(0), B.mean(0); Ca, Cb = np.cov(A, rowvar=False), np.cov(B, rowvar=False)
    covmean = linalg.sqrtm(Ca @ Cb); fallback = False
    if not np.isfinite(covmean).all():
        off = eps * np.eye(len(Ca)); covmean = linalg.sqrtm((Ca + off) @ (Cb + off)); fallback = True
    covmean = np.real(covmean)
    return float(((mu_a - mu_b) ** 2).sum() + np.trace(Ca + Cb - 2 * covmean)), fallback

def p_fd(pred_l, spk, gt_l):
    return frechet(np.concatenate([pred_l, spk], -1), np.concatenate([gt_l, spk], -1))

def variation(windows):
    return float(windows.var(axis=1).mean())

def fit_si_kmeans(train_listener_frames, k=15, seed=0):
    """UNSPEC init/seed -> kmeans2 '++', seed 0, on all train listener frames (valid frames only)."""
    cent, _ = kmeans2(train_listener_frames.astype(np.float64), k, minit="++", seed=seed)
    return cent

def si(sequences, centroids):
    """UNSPEC (S3) -> one cluster-id histogram per 256-frame sequence, natural-log Shannon entropy, mean over sequences."""
    k = len(centroids); ents = []
    for w in sequences:
        ids = np.argmin(((w[:, None, :] - centroids[None]) ** 2).sum(-1), 1)
        p = np.bincount(ids, minlength=k) / len(ids); p = p[p > 0]; ents.append(-(p * np.log(p)).sum())
    return float(np.mean(ents))

def _pearson_mean_channels(x, y):
    x = np.asarray(x, np.float64); y = np.asarray(y, np.float64)
    x = x - x.mean(0); y = y - y.mean(0); den = np.sqrt((x * x).sum(0) * (y * y).sum(0))
    ok = den > 1e-9 * len(x)   # float rounding of a constant channel is treated as constant
    return float(((x * y).sum(0)[ok] / den[ok]).mean()) if ok.any() else np.nan

def tlcc_l2l(listener, speaker, max_shift=60):
    """Speaker shifted forward x in [0,60] frames on one 256-frame sequence. UNSPEC multichannel -> mean Pearson over
    channels with non-zero variance (zero-variance channels dropped; unlike REACT, which propagates NaN).
    Constant predictions -> (nan, nan), recorded as 'undefined (constant)' (REVIEW-1 B6)."""
    rs = np.array([_pearson_mean_channels(listener[x:], speaker[:len(speaker) - x]) for x in range(max_shift + 1)])
    if np.isnan(rs).all(): return np.nan, np.nan
    i = int(np.nanargmax(rs)); return i, float(rs[i])

# ---------- REACT 2023 (official code, metric/*.py); clips of REACT_CLIP frames ----------
def frvar(preds):
    return float(preds.var(axis=2, ddof=1).mean())

def s_mse(preds):
    B, S = preds.shape[:2]
    if S == 1: return 0.0
    tot = 0.0
    for b in range(B):
        X = preds[b].reshape(S, -1); D = ((X[:, None] - X[None]) ** 2).sum(-1)
        tot += D.sum() / (S * (S - 1) * X.shape[1])
    return tot / B

def frdvs(preds):
    N, S = preds.shape[:2]; X = preds.reshape(N, S, -1).transpose(1, 0, 2); tot = 0.0
    for k in range(S):
        D = ((X[k][:, None] - X[k][None]) ** 2).sum(-1); tot += D.sum()
    return tot / (N * (N - 1) * S) / X.shape[-1]

def _react_crosscorr(x, y, lag):
    if lag > 0: a, b = x[lag:], y[:-lag]
    elif lag < 0: a, b = x[:lag], y[-lag:]
    else: a, b = x, y
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.mean([np.corrcoef(a[:, i], b[:, i])[0, 1] for i in range(x.shape[1])]))

def react_tlcc_offset(pred, sp, lag_frames=49):
    """Returns (|offset| in frames, number of NaN lags). np.argmax returns the first NaN index, as torch.argmax would
    not exactly; the NaN count is reported with every result."""
    rs = np.array([_react_crosscorr(pred, sp, lag) for lag in range(-lag_frames, lag_frames + 1)])
    return abs(len(rs) // 2 - int(np.argmax(rs))), int(np.isnan(rs).sum())

def frsyn(preds, speakers, lag_frames=49, published_path=True):
    """published_path=True reproduces compute_TLCC_mp/_func (only sample 0 per clip). Returns (FRSyn, total NaN lags)."""
    offs, nans = [], 0
    for p, s in zip(preds, speakers):
        for q in (p[:1] if published_path else p):
            o, n = react_tlcc_offset(q, s, lag_frames); offs.append(o); nans += n
    return float(np.mean(offs)), nans

# ---------- E3: Moulder et al. 2018 global synchrony with surrogates (masked; REVIEW-1 B1-B3) ----------
def wcc_global_mc(A, Bm, W, L, va=None, vb=None):
    """Mean over channels of each channel's mean |Fisher z| over all window x lag elements. Same-index channel pairs.
    Increments 1. An element is dropped if its A-window [s,s+W) or B-window [s+lag,s+lag+W) holds an invalid frame,
    or if either window has zero variance. Accepts (T,) or (T,d)."""
    A = np.asarray(A, float); Bm = np.asarray(Bm, float)
    if A.ndim == 1: A, Bm = A[:, None], Bm[:, None]
    assert A.shape == Bm.shape, (A.shape, Bm.shape)
    T, d = A.shape
    va = np.ones(T, bool) if va is None else np.asarray(va, bool); vb = np.ones(T, bool) if vb is None else np.asarray(vb, bool)
    assert len(va) == len(vb) == T
    starts = np.arange(L, T - W - L + 1)
    if len(starts) == 0: return np.nan
    cum = lambda x: np.concatenate([np.zeros((1,) + x.shape[1:]), np.cumsum(x, 0)])
    ca, ca2, cb, cb2 = cum(A), cum(A * A), cum(Bm), cum(Bm * Bm)
    bad_a, bad_b = cum((~va).astype(float)), cum((~vb).astype(float))
    oka = (bad_a[starts + W] - bad_a[starts]) == 0
    sa = ca[starts + W] - ca[starts]; vaa = (ca2[starts + W] - ca2[starts]) - sa * sa / W
    tot = np.zeros(d); cnt = np.zeros(d)
    for lag in range(-L, L + 1):
        bs = starts + lag; okb = (bad_b[bs + W] - bad_b[bs]) == 0
        sb = cb[bs + W] - cb[bs]; vbb = (cb2[bs + W] - cb2[bs]) - sb * sb / W
        if lag >= 0: cab = cum(A[:T - lag] * Bm[lag:]); s_ab = cab[starts + W] - cab[starts]
        else: k = -lag; cab = cum(A[k:] * Bm[:T - k]); s_ab = cab[starts - k + W] - cab[starts - k]
        den = np.sqrt(np.clip(vaa * vbb, 0, None)); ok = (den > 1e-12) & (oka & okb)[:, None]
        r = np.where(ok, (s_ab - sa * sb / W) / np.where(ok, den, 1), 0.0)
        z = np.abs(np.arctanh(np.clip(r, -0.999999, 0.999999)))
        tot += np.where(ok, z, 0).sum(0); cnt += ok.sum(0)
    per = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)
    return float(np.nanmean(per)) if np.isfinite(per).any() else np.nan

def segment_shuffle_idx(T, m, rng):
    """Index permutation: segments of m frames shuffled; the remainder (< m frames) stays at the end (UNSPEC)."""
    n = T // m; order = rng.permutation(n)
    return np.concatenate([np.arange(i * m, (i + 1) * m) for i in order] + [np.arange(n * m, T)])

def data_slide_idx(T, rng):
    cut = int(rng.integers(int(0.2 * T), int(0.8 * T) + 1)); return np.concatenate([np.arange(cut, T), np.arange(cut)])

def e3_test(A, Bm, W, L, va=None, vb=None, n_surr=1000, seg_len=None, seed=0):
    """Observed vs the 95th percentile of segment-shuffle and data-sliding surrogates of the partner series B (its
    validity mask moves with it). One-tailed, alpha .05. Excluded if fewer than 500 jointly valid frames."""
    T = len(A); va = np.ones(T, bool) if va is None else np.asarray(va, bool); vb = np.ones(T, bool) if vb is None else np.asarray(vb, bool)
    n_valid = int((va & vb).sum())
    if n_valid < 500: return dict(excluded=True, n_valid=n_valid)
    rng = np.random.default_rng(seed); m = seg_len or W
    obs = wcc_global_mc(A, Bm, W, L, va, vb)
    seg, sld = [], []
    for _ in range(n_surr):
        i = segment_shuffle_idx(T, m, rng); seg.append(wcc_global_mc(A, Bm[i], W, L, va, vb[i]))
        j = data_slide_idx(T, rng); sld.append(wcc_global_mc(A, Bm[j], W, L, va, vb[j]))
    s95, d95 = float(np.nanpercentile(seg, 95)), float(np.nanpercentile(sld, 95))
    return dict(excluded=False, n_valid=n_valid, obs=obs, seg95=s95, slide95=d95, passes=bool(obs > s95 and obs > d95))
