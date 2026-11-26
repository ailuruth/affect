"""Pure measurement helpers of the M1 checks (no device, model or clock): the real-time queue of a streaming
recogniser, word matching for delivery latency, breathing-window scoring, onset detection for the echo rig."""
from __future__ import annotations

import difflib
import re


def realtime_finish(compute_s, frame_s: float):
    """Finish time (audio clock, s from the start) of each frame when frames arrive in real time and one worker
    processes them in order: arrival_i = (i + 1) frame_s, finish_i = max(finish_{i-1}, arrival_i) + compute_i."""
    out, f = [], 0.0
    for i, c in enumerate(compute_s):
        f = max(f, (i + 1) * frame_s) + c
        out.append(f)
    return out


def _norm(w: str) -> str:
    return re.sub(r"[^\w']+", "", w.lower())


def delivery_latencies(stream_words, finish_s, ref_words):
    """Word-end-to-delivery latency of every streamed word matched to a reference word.
    stream_words: [(word, frame)]; finish_s: per-frame finish times; ref_words: [(word, start_s, end_s)] (the
    reference alignment). Words are matched by a longest-common-subsequence alignment of the normalised words."""
    a = [_norm(w) for w, _ in stream_words]
    b = [_norm(w) for w, _, _ in ref_words]
    out = []
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w, frame = stream_words[blk.a + k]
            out.append(finish_s[frame] - ref_words[blk.b + k][2])
    return out


def pearson(x, y) -> float:
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("paired samples of length >= 2 needed")
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5 if sxx > 0 and syy > 0 else 0.0


def rising_crossings(signal, fps: float, min_gap_s: float = 0.5):
    """Times (s) at which a brightness trace crosses the midpoint between its 5th and 99.9th percentiles upwards (the
    flashes are short, so the upper level is near the maximum), at least min_gap_s apart, interpolated between
    frames."""
    v = sorted(signal)
    lo, hi = v[int(0.05 * (len(v) - 1))], v[int(0.999 * (len(v) - 1))]
    mid = 0.5 * (lo + hi)
    out = []
    for i in range(1, len(signal)):
        if signal[i - 1] < mid <= signal[i]:
            t = (i - 1 + (mid - signal[i - 1]) / (signal[i] - signal[i - 1])) / fps
            if not out or t - out[-1] >= min_gap_s:
                out.append(t)
    return out


def pair_onsets(flash_s, response_s, max_lag_s: float = 1.0):
    """Lag of the first response after each flash (within max_lag_s)."""
    lags, j = [], 0
    for f in flash_s:
        while j < len(response_s) and response_s[j] < f:
            j += 1
        if j < len(response_s) and response_s[j] - f <= max_lag_s:
            lags.append(response_s[j] - f)
    return lags
