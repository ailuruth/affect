# rMEA (Kleinbub & Ramseyer, "rMEA: An R package to assess nonverbal synchronization in motion energy analysis time-series", Psychotherapy Research 2020, doi 10.1080/10503307.2020.1844334)

Source read: CRAN package page and reference manual for rMEA 1.2.2 (published 2022-02-17). I did not read the Psychotherapy Research paper.

## Claims
- "Lagged synchrony between subjects can be analyzed through windowed cross-correlation." "Surrogate data generation allows an estimation of pseudosynchrony that helps to estimate the effect size of the observed synchronization."

## Evidence
- `MEAccf(mea, lagSec, winSec, incSec, r2Z = T, ABS = T)`: window, max lag and step in seconds, no defaults. Defaults apply "Fisher's r to Z transformation" and take absolute values.
- Preprocessing: `MEAscale` (divide by SD by default), `MEAsmooth` (moving average, `moving.average.win = 0.5` s; "NA values are set to 0"), `MEAoutlier` (default threshold SD x 10).
- Surrogates: `shuffle()` "creates all possible combinations between s1 and s2 of all MEA objects" with real pairings removed (participant shuffling); `shuffle_segments(mea, n_each, segSec)` "divides s1 and s2 MEA data in segments of size segSec" and "shuffles them within subject" (segment shuffling).
- Effect size: `cohens_d`; `MEAdistplot` shows "a normalized difference (Cohen's d) between the means of each group and the contrast".

## License
GPL-3.

## Runs on this Mac without a GPU?
Yes. Pure R on CPU. It reads any two-column time series, so AU intensity series can be loaded in place of MEA output.

## Verdict: adopt (analysis implementation)
- Implements the Ramseyer-Tschacher pipeline (windowed |Fisher z| plus participant- or segment-shuffled pseudosynchrony and Cohen's d) from the method's own authors, so the published procedure can be run as published. Use alongside `wcc` (peak picking) and Moulder 2018 (data sliding must be added by hand; rMEA does not list it).
