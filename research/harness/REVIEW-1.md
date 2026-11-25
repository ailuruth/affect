# Harness review 1 (independent, before any data is scored)

Scope: HARNESS.md; loader.py, splits_v2.py, pilot.py, fetch.py, metrics.py, baselines.py, dial.py; evaluation.md E3 and Part 3; the four source notes. The code was not edited.

Checks were run only on the one local pair, `naturalistic/dev/V00_S0080_I00000377_P0115/P0116`, plus synthetic arrays. They are code checks, not results.

Severity labels:
- **bug**: the code gives a wrong answer or crashes on inputs the harness will feed it.
- **spec deviation**: the code does not do what HARNESS.md says, or it makes a reading that is not labelled.
- **ok**: checked and matches.

## Summary of bugs

| # | File:line | Finding |
|---|---|---|
| B1 | metrics.py:95-129 | is_valid masking for E3 is claimed in HARNESS.md:141 and is not implemented anywhere. |
| B2 | metrics.py:129 | The ≥500 rule counts all frames, not valid frames. |
| B3 | metrics.py:98-102 | wcc_global given a (T, d) array returns a number silently, and the number is wrong (measured 0.995). |
| B4 | dial.py:35-53 | The permutation null is invalid. Interactions cluster in sessions and partners. Under a true null with only a session offset, p_profile = 0.005. |
| B5 | dial.py:20-27 | There is one validity mask, and the z-scoring includes invalid frames. |
| B6 | metrics.py:51 | tlcc_l2l crashes (nanargmax on all-NaN) for constant predictors (Median, B_MeanFr). |
| B7 | baselines.py:43 | Delayed Mirror with a start below 17 returns empty windows silently, or raises an error. |
| B8 | baselines.py:8-18 | TrainBank has no split guard, so a mis-built bank lets NN copy the ground truth exactly. |

The spec deviations that matter most are:
- S1: REACT metrics run on 64-frame windows, but the published clips are 750 frames.
- S2: L2L TLCC on 64-frame windows is dominated by short-overlap bias. White noise gives a mean peak lag of 52.6.
- S3: the SI aggregation is not labelled as a reading.
- S4: identity leakage through A-suffix IDs is possible: 7 twin pairs straddle splits.

---

## 1. Published metrics and baselines against the HARNESS.md transcription

### metrics.py:9-11, `l2`: ok

This is the mean per-frame Euclidean distance over (N, T), as fixed by the UNSPEC rule.

### metrics.py:13-19, `frechet`: ok, with one minor point

Each set is fitted with one Gaussian over flattened T×d windows, using the standard FID formula. The self-distance is 0.

Minor: the standard eps-offset fallback is missing, for when `sqrtm` returns non-finite values or when N < T·d = 1,472, where the covariance is singular.
- **Fix:** assert `len(windows) > 1472`. If `covmean` is not finite, retry with `Ca + eps·I` (as pytorch-fid does), and log when the fallback is used.

### metrics.py:21-23, `p_fd`: ok

It concatenates on the feature axis, giving (N, T, 2d), as L2L specifies.

### metrics.py:25-27, `variation`: ok

It takes the variance over the time axis (axis 1, ddof 0), then the mean over windows and features. This matches "variance along the axis representing the temporal extent T … then average over B and F".

### metrics.py:34-40, `si`: spec deviation (S3)

The code computes one entropy per window and averages them. The source text does not say whether the histogram is per sequence or pooled. HARNESS.md lists four UNSPEC readings, and this is not one of them, so the choice is unlabelled. The log base is also unlabelled.

Scale check on the local pair, with natural log:

| Reading | SI |
|---|---|
| Per 64-frame window | 0.82 |
| Per 256-frame window | 1.25 |
| One histogram pooled over the series | 1.52 |
| L2L's published GT value | 2.61 |
| ln 15 (maximum possible) | 2.71 |

L2L's GT value of 2.61 is close to the maximum. That is hard to reach with 64 frames per window, which suggests L2L pooled the histogram or used longer sequences.

- **Fix:** add SI to the fixed UNSPEC list in HARNESS.md, stating the histogram unit, the sequence length and the log base, before scoring.

### metrics.py:42-51, `tlcc_l2l`

**Direction: ok.** `listener[x:]` is paired with `speaker[:T-x]`, so listener frame t+x is paired with speaker frame t. That is the speaker shifted forward by x frames. The documented check (a listener equal to the speaker delayed by 17 frames gives a lag of 17) is consistent with this.

**Bug B6, line 51.** For a constant prediction (Median, B_MeanFr), every channel has zero variance. `_pearson_mean_channels` then returns NaN at every shift, and `np.nanargmax` raises `ValueError: All-NaN slice`.
- **Fix:** if every value is NaN, return `(nan, nan)` and record the result as "undefined (constant)", the same way E3 does (HARNESS.md:236).

**Spec deviation S2: the sequence length is not fixed.** The baselines produce 64-frame windows. Over shifts 0–60, the overlap shrinks to 4 frames, and Pearson correlations on short overlaps are extreme, so the peak drifts to large shifts.

| Input | Window | Mean peak lag | Peaks at ≥ 55 |
|---|---|---|---|
| White noise | 64 frames | 52.6 | 58% |
| White noise | 256 frames | 35.4 | — |
| Real pair | 64 frames | 44.0 | — |
| Real pair | 256 frames | 25.8 | — |

As implemented, the number mostly measures window length.
- **Fix, before scoring:**
  - Fix the TLCC sequence length. L2L App. D [S] says 256 frames.
  - Optionally require a minimum overlap.
  - Report a shuffled-pair noise floor alongside.
  - Record this as UNSPEC.
- The docstring says "as REACT", but REACT propagates NaN for a constant channel, while this code drops the channel. Relabel the docstring.

### metrics.py:54-55, `frvar`: ok

`var(axis=2, ddof=1)` over (N, S, T, d) is the unbiased variance over time. It is then averaged over reactions, samples and channels, which equals REACT's mean over k of the per-k means.

### metrics.py:57-64, `s_mse`: ok

The early return when S == 1 is kept. The sum of the squared pairwise distance matrix is divided by S·(S−1)·(T·d), then averaged over B, as transcribed.

### metrics.py:66-70, `frdvs`: ok

For each sample index k, the code takes the pairwise squared distances across the N clips and sums them over k. It then divides by N·(N−1)·S and by T·d, as transcribed.

### metrics.py:72-83, `_react_crosscorr` and `react_tlcc_offset`: ok, with a NaN gap

- The shift convention matches REACT's `shift()`.
- Lags run over −49..+49, which is 99 values, and `len//2` = 49.
- The offset is |49 − argmax|.
- The local pair gives an offset of 16 on a 750-frame clip.

**Spec deviation, lines 80-81.** The docstring says NaN rows are reported, but nothing reports them. `np.argmax` returns the first NaN index, so a constant predictor gets an offset of 49 silently.
- **Fix:** count lags with NaN per call and return the count, or log it.

### metrics.py:85-92, `frsyn`: ok

`p[:1]` reproduces the published path, which scores sample 0 only, as HARNESS.md:92 states. The serial path scores all samples.

### baselines.py:46-56 and HARNESS.md:55: spec deviation (S1)

REACT metrics are defined on 750-frame clips. Every REACT baseline here is hard-wired to `T_WIN = 64`, and B_MeanSeq is a 64-step mean sequence. With ±49 lags on 64 frames, the overlap at the extremes is 15 frames, or 5 frames under the ±59 reading.

On the local pair, the REACT offset is 31 on a 64-frame window and 16 on the 750-frame clip.
- **Fix:** give the REACT baselines and metrics their own clip length, fixed before scoring: 750 frames (the published frame count) or 900 frames (30 s at 30 Hz), paired with the ±49 or ±59 lag decision. Keep 64-frame windows for L2L only.

### baselines.py:20-30: ok

- `l2l_median` is the per-dimension median over all train listener frames.
- `l2l_random` is a random train listener window.
- `l2l_nn` uses Euclidean distance on the flattened speaker window and returns the paired listener window.

### baselines.py:32-43, Mirror and Delayed Mirror: ok, except B7

The centred k-frame mean uses edge padding. Delayed Mirror is `s[t-17 : t-17+64]`, so prediction frame t+i equals speaker frame t+i−17, which is correct.

**Bug B7, line 43.** No check enforces `t >= delay`. With a negative start, `s[-5:59]` is empty when T > 64, and the output was measured as shape (0, 23). If the empty window is mixed with normal ones, `np.stack` raises an error. The windows at the end of the series are also not checked.
- **Fix:**
  - Add `assert all(delay <= t <= len(spk) - T_WIN for t in starts)` (and the same end check in the mirror and mime functions).
  - Define one shared list of window starts (≥ 17) that every method and the ground truth are scored on.

### baselines.py:14-18, REACT pooling: ok

B_MeanSeq and B_MeanFr pool speaker and listener windows, as HARNESS.md:99 states. The bank holds both directions of each dyad, so the speaker windows are the listener windows of the reverse direction.

## 2. E3 (`wcc_global`, `wcc_global_mc`, surrogates)

### metrics.py:95-112, windowed Pearson: ok

Window starts satisfy s ∈ [L, T−W−L], so every lag fits inside the series.
- For lag ≥ 0, `a[s:s+W]` is paired with `b[s+lag : s+lag+W]`.
- For lag < 0, the cumulative-sum offsets `starts−k` index the product `a[t+k]·b[t]` correctly.

Both lag signs are computed, and the Fisher z is `arctanh` with clipping. The score is the mean |z| over all valid window×lag elements, which is Moulder's "mean absolute value of all elements in the matrix z".

I checked the vectorised code against a direct per-window `corrcoef` loop on AU channels 0, 3, 9, 17 and 18 of the local pair (W = L = 60). The vectorised code was run on both float32 and float64 input; channels 3 and 17 are nearly dead, with a maximum value of about 1e-4.
- The scores agree to 5 decimals.
- The element counts are identical (297,781).
- Channel 18 gives NaN in both, because no window has den > 1e-12.

### metrics.py:131-149, `wcc_global_mc`: ok

It uses the same index algebra on all channels at once, then takes the mean over channels of each channel's mean |z|.

Design note, not a bug: near-dead channels (3, 17, 18) contribute correlations of estimator jitter. Their |z| is about 0.24–0.26, the same size as active channels, so they dilute the 23-channel average. Surrogates share this dilution. S1 says the channel pairs are "fixed in advance", so name them.

### metrics.py:98-102, bug B3

`np.cumsum` without an axis flattens a 2-D array. `wcc_global(a[:, :3], b[:, :3], 60, 60)` returned 0.995 without any error. `e3_test` passes its inputs straight through, so a (T, 23) call would score garbage.
- **Fix:** add `assert a.ndim == b.ndim == 1 and len(a) == len(b)`.
- Also add `e3_test_mc`, which calls `wcc_global_mc` with the same 2-D surrogates. `segment_shuffle` and `data_slide` already permute rows jointly. HARNESS.md:226-231 plans the multichannel test, but no function implements it.

### metrics.py:114-119, surrogates: ok

**Segment shuffle:** m = W (60 frames = 2 s at 2 s/2 s; 900 frames = 30 s at 30 s/5 s), which matches Moulder's m = 2 s and 30 s. The remainder of fewer than m frames stays at the end, unshuffled. This is unspecified in the source and should be noted as such.

**Data slide:** the cut is drawn from [⌊0.2n⌋, ⌊0.8n⌋] inclusive, which is the middle 60%, and the tail moves to the front.

### metrics.py:121-129, test: ok

The test takes 1,000 surrogates per type and compares the observed score one-tailed against the 95th percentile (`>`).

### Bug B1: is_valid masking is not implemented

HARNESS.md:141 says "Frames with is_valid = 0 are excluded: windows containing any are dropped." Neither `wcc_global`, `wcc_global_mc` nor `e3_test` takes a mask, and nothing else in the harness applies one to E3. The only use of `is_valid` is in dial.py.

The local pair has no invalid frames, so the gap does not show on it.

- **Fix:**
  1. Pass `va` and `vb`.
  2. Build `bad = cumsum(~v)`.
  3. For each lag, drop elements where the a-window [s, s+W) or the b-window [s+lag, s+lag+W) contains an invalid frame. Apply this in both the 1-D and the multichannel functions.
  4. In the surrogates, permute or slide `vb` together with `b`.

### Bug B2: the ≥500 rule counts all frames (metrics.py:129)

`len(a) >= 500` counts all frames, but HARNESS.md:140 says "shorter than 500 valid frames are excluded and counted". Nothing counts the exclusions.
- **Fix:** use `(va & vb).sum() >= 500`. Return an `excluded` flag, and count the flags in the runner.

### Design note on screening condition 4

Delayed Mirror's prediction equals the speaker at lag 17, so every window has |r| = 1 at that lag, clipped to |z| = 7.25. Its E3 pass share will be near 100%, so condition 4 in effect requires every interaction to pass. This is legitimate as written, but say so before scoring.

## 3. Splits, loader and fetch

### splits_v2.py: ok by ID

- Re-running the script in a temporary directory reproduced splits_v2.json byte for byte (sha256 prefix d0687e87d18b484f).
- No person ID appears in two splits.
- pilot_v1.json matches its sha256 prefix (4932794aa45799da).
- The pilot has no test files.
- e3_subset_v1.json reproduces from the stated rule.

### splits_v2.py:16: spec deviation S4, identity leakage possible

The dataset README (research/data/seamless/README.md:342-345) warns of "The same individual being mapped to different identifiers".
- 23 numeric IDs have an A-suffix twin (P0844 / P0844A and so on).
- 7 of these twin pairs straddle splits:

| Twin pair | Splits |
|---|---|
| P0844A / P0844 | train / test |
| P1024A / P1024 | test / train |
| P0383A / P0383 | train / val |
| P0230A / P0230 | train / val |
| P0180A / P0180 | val / train |
| P0921A / P0921 | val / train |
| P0955A / P0955 | val / train |

- Twins never share a session. That is consistent with them being one person, but it is not proof.
- The A IDs have "Undisclosed" Big Five scores, so the traits cannot settle it.
- No two distinct IDs have identical disclosed Big Five vectors.

**Fix:** key persons by the numeric part, `P(\d+)A?` → `V00_P(\d+)`. This is conservative and moves only these 7 pairs. Re-fix as splits_v3 before any scoring, and record the reason. Any other duplicates cannot be detected from metadata. Record that as a limitation.

### splits_v2.py:29 and pilot.py:6,18: minor

These write and read paths relative to the current directory, so re-running from another directory would write a second copy elsewhere.
- **Fix:** use absolute paths, and check the sha256 prefix on load.

### loader.py:11-14: ok

The block list and the allow-list are checked in `_path`, before `np.load` is called. Both loads go through `_path`. `allow_pickle=False` is set. I confirmed that columns 12 and 19 are byte-identical in both local files.

Minor: the code does not check that the two partners have equal T, which seamless-interaction.md:83 asks for. Callers use `min(T)`.
- **Fix:** assert that the lengths are equal, or log the difference.

### fetch.py:13-20: ok

Only the four allow-listed fields are iterated. The DENY assertion runs on every URL before `urlretrieve`. Free disk space is checked before every file. The `field in ALLOW` half of the assertion is always true, because the loop iterates over ALLOW; it is harmless. The code uses `movement/` only and never `movement_v4/`, so the two are not mixed.

## 4. dial.py

### dial.py:24, causal design: ok

Row t uses only the speaker's frames from t−30 to t−1:
- bin (1, 10) is `cs[t] − cs[t−10]`, the mean of z-scored speaker frames t−10..t−1;
- bin (21, 30) is the mean of frames t−30..t−21.

I verified this against direct means at t = 40. No frame at t or later is used.

### dial.py:20-27, bug B5: the validity mask

The row filter correctly requires that frames t−30..t are all valid (line 26). But:
1. `design` takes a single `valid`. If the caller passes only the listener's mask, the speaker's invalid frames enter X.
2. `_z` (line 22) computes the mean and SD over all frames, invalid ones included.

**Fix:** take `valid_l` and `valid_s`, use `ok = valid_l & valid_s`, and compute the z-score statistics on `ok` frames only.

Minor: there is no intercept. The masked Y is not exactly centred. Either centre X and Y on the kept rows, or add an intercept.

### dial.py:32, ridge scaling: ok

X'X grows like n·Cov(X), so a penalty of λ·n/1000 is about 0.1 per unit-variance feature at λ = 100, whatever n is. B is linear in Y, so the profile P does not change if the listener's amplitude is rescaled.

Two notes:
- Y is z-scored, so "gain" means coupling strength in SD units, not expressive amplitude. Say so.
- There are no regressors for the listener's own past. Because of that, B also absorbs the speaker following the listener: S's past correlates with L's past, and L's past correlates with L_t. This matches the spec's wording, but Granger-style controls (bins of the listener's own lags as nuisance regressors) would make "response" mean what it says.

### dial.py:35-53, bug B4: the permutation null is not valid

Condition labels are permuted across a person's interactions. But a person's familiar interactions all come from the same session or sessions, with the same partner, so interactions are not exchangeable.

In the train split, 47 persons have both conditions. 18 of them have exactly 1 familiar and 1 stranger session, each with one partner, as listed below.

| Familiar sessions | Stranger sessions | Persons |
|---|---|---|
| 1 | 1 | 18 |
| 1 | 2 | 5 |
| 2 | 1 | 7 |
| … | … | … |

Synthetic check: 18 persons, 1 session per condition, 15 interactions per session, a per-session profile offset and **no condition effect**. The test gave p_profile = 0.005, a false positive. Partner and session effects are read as condition effects.

There is also a separate degeneracy. With exactly one record per condition, permuting the labels only swaps them, and D is unchanged. A synthetic huge profile shift gave p_profile = 1.0. This does not occur at the interaction level in this data, but it does occur at the session level.

**Fix:**
- Average P and log g per session (or per partner) first, and permute session labels within each person.
- Persons with 1 + 1 sessions carry no permutation information. Report them separately, or use a test that compares the between-condition profile distance with the within-condition, between-session distance, for persons with ≥ 2 sessions in a condition.
- Warn when the permutation group is trivial.
- Note in HARNESS.md that partner identity is confounded with condition.

### Coverage: spec deviation

- Val and test contain **0** persons with both conditions, so the dial analysis can run only on train (47 persons). It cannot be used to judge architectures on val as written.
- The improvised "repeat against first meeting" contrast in HARNESS.md:151 is not implemented. `within_person_test` accepts only "familiar" and "stranger".

**Fix:** state both facts in HARNESS.md, or add the contrast.

## 5. Leakage in baselines.py

### baselines.py:8-18, bug B8: no split guard

`TrainBank(pairs)` accepts any arrays. Nothing ties it to `splits_v2["files"]["train"]`.

If a validation interaction enters the bank, NN finds its own speaker window at distance 0 and returns the true listener window. The bank also holds the reverse direction, so this happens for both people. The result would be L2 = 0 for those windows.

With a correct train-only bank, no self-match is possible: persons are disjoint by ID, apart from the A-suffix issue in S4.

**Fix:** make TrainBank take file IDs, load the data itself through loader.py, and assert:
- that every ID is in the train split;
- that no person or interaction ID is shared with the query set.

### Minor: invalid frames enter the bank

Bank windows, query windows and L2/FD windows ignore `is_valid`. If invalid frames hold a fill value, NN can match on the fill.

**Fix:** drop any window containing an invalid frame, in the bank and in scoring. Use the same rule for every method.
