"""K1. Speech rate (a released 'nonverbal' voice channel) leaks through the noise-free turn times in Q.

design-cayley-ledger.md: the neighbouring relation offsets the nonverbal stream (incl. speech rate,
the 4th voice channel) while keeping 'words, turn times and identity identical'. But a held offset
in speech rate changes turn durations: duration = syllables / rate + pauses. Q releases turn start
and end times (100 ms grid) with no noise. So the mind can estimate a held speech-rate level from Q.

Model (assumptions, stated): rate level r in [0,1] normalised <-> 3..6 syllables/s (innate range).
Content length per turn N ~ lognormal (median 20 syllables, sd(log) 0.8) independent of rate.
Within-turn pause fraction ~ Beta(2, 8). Times quantised to 100 ms.
Estimator 1 (duration only): mean of -log(duration) over the turns of an episode.
Estimator 2 (duration + length): if the 64-d text embedding or the stored transcript gives N.
Comparison: the ledger route alone (release noise sigma_s = 7.1 at 2 Hz) -> bound 0.25.
Not evidence about people (brief: no toy worlds); a check of the design's own claim L.
"""
import numpy as np

rng = np.random.default_rng(7)


def episode(r, n_turns, use_len):
    rate = 3.0 + 3.0 * r
    N = np.exp(np.log(20) + 0.8 * rng.normal(size=n_turns))
    pause = rng.beta(2, 8, size=n_turns)
    dur = N / rate / (1 - pause)
    dur = np.maximum(0.1, np.round(dur * 10) / 10)       # 100 ms grid
    if use_len:
        return np.mean(np.log(N) - np.log(dur))
    return -np.mean(np.log(dur))


for n_turns, label in [(1, "1 turn"), (5, "5 turns (~2 min)"), (20, "20 turns (~10 min)")]:
    for use_len in (False, True):
        r = rng.uniform(0, 1, 2000)
        est = np.array([episode(ri, n_turns, use_len) for ri in r])
        c = np.corrcoef(r, est)[0, 1]
        print(f"{label:22s} {'duration+length' if use_len else 'duration only':16s} corr(held rate, estimate) = {c:.2f}   (ledger bound rho_L = 0.25)")

# Binary held-level test (the design's own neighbouring pair, Delta_L = 1 on the rate channel)
for n_turns in (5, 20):
    a = np.array([episode(0.0, n_turns, False) for _ in range(4000)])
    b = np.array([episode(1.0, n_turns, False) for _ in range(4000)])
    thr = 0.5 * (a.mean() + b.mean())
    acc = 0.5 * ((a < thr).mean() + (b > thr).mean())
    print(f"held full-range rate offset, {n_turns} turns, duration only: balanced accuracy {acc:.3f}  "
          f"(ledger promise: <= Phi(mu/2) = 0.567)")
