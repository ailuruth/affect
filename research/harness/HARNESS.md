# Shared evaluation harness (operator note Q11): v1

Every architecture runs through this harness unchanged. Fixed parts are timestamped from the system clock **before any architecture is scored**.

## Splits: fixed 2026-11-25T09:02:25Z

- **File:** research/harness/splits_v2.json, sha256 prefix d0687e87d18b484f.
- **Script:** research/harness/splits_v2.py.
- **Rule:** each person is assigned to a split by sha256('affect-split-v2:' + person) mod 100: below 70 train, below 85 val, otherwise test. An interaction is kept only if all its participants share a split, so **no person appears in two splits**.
  - 10,088 interactions that straddle splits are dropped.
  - 132 single-participant interactions are excluded.
  - Only files with released movement features are used.
- **Counts:**

| Split | Files | Persons | Interactions |
|---|---|---|---|
| Train | 20,356 | 731 | 5,514 improvised + 4,664 naturalistic (6,487 stranger, 3,691 familiar) |
| Val | 1,394 | 60 | 479 improvised + 218 naturalistic (494 stranger, 203 familiar) |
| Test | 874 | 41 | 267 improvised + 170 naturalistic (288 stranger, 149 familiar) |

- **The first rule was abandoned and recorded** (research/harness/splits_v1.json): assigning whole connected groups of co-occurring people gave one giant group of 34,765 files and a test split of only 300 files.
- **The test split is never used** for tuning or model selection. Screening uses train and val only.

## Loader: fixed 2026-11-25T09:02:25Z

research/harness/loader.py:
- **Allow-list:** FAUValue, is_valid, transcript, VAD.
- **Block list:** emotion_scores, emotion_valence, emotion_arousal, EmotionValenceToken, EmotionArousalToken. These are refused by name before any file is opened.
- **Format:** allow_pickle=False. The duplicate AU column 19 is dropped, so the AU vector is 23-dimensional and unlabelled.

## Baselines and metrics (to be implemented verbatim from their primary sources before the first scoring)

- **Published simple baselines:** Median, Random, Nearest Neighbour, Mirror, Delayed Mirror (17 frames).
  - Sources: research/ng-2022-learning-to-listen.md and research/react-challenge-baselines.md.
- **Published metrics:** L2, FD, P-FD, variance, PCC, TLCC and REACT's FRSyn, each exactly as defined in those primary sources.
- **The analyses in evaluation.md:** Moulder et al.'s windowed cross-correlation with segment-shuffle, data-sliding and participant-shuffle surrogates.
- **Pass thresholds for screening:** fixed in this file, with a clock timestamp, after the metrics are implemented and before any architecture is scored.

## Data budget (research/machine.md)

- **Per file:** FAUValue is about 0.5 MB, plus about 21 kB for is_valid.
- **Pilot:** val + test (2,268 files) is about 1.2 GB. A train pilot of 300 interactions (600 files) is about 0.3 GB.
- **Full train:** about 10.6 GB.
- **Blocked:** the disk is at 12% free, below the operator's 20% floor, so even the pilot waits on research/questions.md Q11.

## Metric sources obtained so far (2026-11-25T09:07:43Z)

**REACT 2023, from the official code** (github.com/reactmultimodalchallenge/baseline_react2023, metric/*.py, read verbatim by a fetch agent):
- **FRVar:** torch.var over time (unbiased), then the mean over reactions and channels.
- **S-MSE (the paper's FRDiv):** the mean squared pairwise distance among the 10 samples per speaker clip, each flattened to T×d, divided by 10·9·(T·d).
- **FRDvs:** the same, across different speaker clips for each sample index.
- **TLCC/FRSyn:**
  - per-channel Pearson correlation at lags −49..+49 frames (`seconds=2, fps=25`), averaged over channels;
  - the reported value is |49 − argmax|, in frames, averaged over clips × samples.
- **Clip shape:** 750 frames.

**Open points, to settle before the first scoring:**
- **Lag window.** REACT fixes the lag window in frames (±49) at 25 fps. Seamless is 30 Hz. "As published" is taken to mean the published frame count (±49) *and* the published duration (±2 s = ±59 frames at 30 Hz). Both are reported, and the choice is fixed before scoring.
- **The REACT parallel path** (`_func` in TLCC.py) may return only the last sample's offset. This must be checked against the raw file before use.
- **Learning to Listen's L2, FD, P-FD, SI and the naive-baseline windows** have not yet been read verbatim: the PDF exceeded the fetch limit. Next: the arXiv HTML version (arxiv.org/html/2204.08451v1).
- **REACT's own definitions** are deferred to Song et al. 2023 (arXiv 2302.06514), not yet read.
- **FRCorr and FRDist** need REACT's appropriate-neighbour matrix, which Seamless lacks. They are recorded as **not computable on Seamless** and are not substituted.

## Metric and baseline sources, second pass (2026-11-25T09:17:23Z)

### Learning to Listen (Ng et al. 2022, arXiv HTML v1)

Sec. 5 and 5.1 were read verbatim. Appendix D came only as a summary, so it is marked [S] below and must be read verbatim before scoring.

**Settings:**
- "We use w=8, T=64". The paper does not say the test sequences are 64 frames.
- [S] Appendix D samples "from the same 256 length test sequences".

**Metrics:**
- **L2:** "Distance to ground truth expression coefficients/pose". The aggregation is not specified.
- **FD:** "in the expression space ℝT×dm ... on the full motion sequence". How μ and Σ are estimated is not specified.
- **Variation:** variance across time.
- **SI:** "k-means to cluster all listener expressions ... from training set"; "avg. entropy (Shannon index) of the cluster id histogram of predicted sequences", with k = 15.
- **P-FD:** FD on concatenated listener and speaker expressions.
- **PCC:** "lip curvature to measure smile synchrony". This needs a named lip-curvature feature, which Seamless's unlabelled AU vector does not give (the column order is unverified). **Not computable as published on Seamless.** It is recorded and not substituted.
- **TLCC:** "For x∈[0,60] frames (up to 2s) we shift the speaker forward". The peak gives the lag.

**Baselines (verbatim):**
- **Median:** "Median expression/pose from train set".
- **Random:** "a randomly-chosen 64-frame motion sequence of a listener from the training set".
- **NN motion:** "nearest neighbor [of the speaker motion] from the training set and use its corresponding listener segment"; "NN on the full 64-frame sequence". The distance is not specified.
- **Mirror:** "the speaker's motion smoothed". The smoother is not specified.
- **Delayed Mirror:** "delayed by 17 frames (≈0.5 s)", the lag being chosen "according to time lagged cross correlation".

### REACT 2023, official code (verbatim)

**TLCC.py `_func`:** the `return` is **inside** the for loop. So the parallel path, which `run_baselines.py` and `evaluate.py` use for the published tables, scores **only the first of the 10 samples** per clip. The serial `compute_TLCC` scores all 10.
- **Decision:** report the published path (as published, since it produced the published numbers) and the serial path side by side, labelled.
- This matters only for stochastic generators. For deterministic baselines the 10 samples are identical.

**run_baselines.py:**
- **B_Random:** `torch.rand`, i.e. **uniform noise in [0,1]**. This is not L2L's Random, which is a training clip. Both are kept, each under its own paper's name.
- **B_Mime:** a copy of the speaker.
- **B_MeanSeq:** the per-timestep mean over training clips (both speakers and listeners pooled, per the code).
- **B_MeanFr:** one per-dimension mean, broadcast over time.

### What "as published" cannot fix

The sources leave four things unspecified:
- the L2 aggregation;
- the FD covariance estimation;
- the NN distance;
- the Mirror smoother.

**Rule:** each is set to its simplest standard reading. That is:
- L2 is the mean Euclidean distance per frame;
- FD uses one Gaussian over flattened T×d windows across test windows;
- NN uses Euclidean distance on the flattened 64-frame speaker window;
- the Mirror smoother is none (identity), with a centred 5-frame moving average reported alongside.

Each choice is labelled "unspecified by source; reading fixed here", before any scoring. No reading is chosen after seeing a result.

**Not computable on Seamless,** recorded and not substituted: REACT's FRCorr and FRDist (they need the appropriate-neighbour matrix), and L2L's PCC (it needs a named lip feature).

## Code, and screening pass thresholds: fixed 2026-11-25T09:26:26Z, before any architecture or baseline is scored

**Code:**
- research/harness/metrics.py: L2, FD, P-FD, variation, SI, L2L TLCC, REACT FRVar, S-MSE, FRDvs and FRSyn (both paths), and E3 (Moulder global mean |Fisher z| WCC, with segment-shuffle and data-sliding surrogates).
- research/harness/baselines.py: L2L Median, Random, NN, Mirror and Delayed Mirror; REACT B_Random, B_Mime, B_MeanSeq and B_MeanFr.

**Equation checks only, not results,** run on the one local sample pair. All matched:
- a listener equal to the speaker delayed by 17 frames gives an L2L TLCC lag of 17;
- the REACT offset of a series with itself is 0;
- the vectorised WCC equals a naive loop (0.2395 = 0.2395);
- the FD of a set with itself is 0;
- the Delayed Mirror windows are exact shifts;
- S-MSE of identical samples is 0.

**E3 settings at 30 Hz:**
- 2 s windows with 2 s lag: W = 60, L = 60.
- 30 s windows with 5 s lag: W = 900, L = 150.
- Increments are 1 (the wcc defaults; the study's own increments are UNSPEC).
- Segment length equals the window.
- 1,000 surrogates of each type.
- Series shorter than 500 valid frames are excluded and counted.
- Frames with is_valid = 0 are excluded: windows containing any are dropped.

**Screening pass, per architecture, on the validation split only.** Each shared risk is expressed as a comparison with a published baseline:
1. **Delayed copy:** P-FD below Delayed Mirror's and Mirror's.
2. **Lookup table:** FD below NN motion's.
3. **Flat affect:** L2 no worse than Median's, *and* variation and SI above Median's and MeanFr's.
4. **Coupling:** the E3 score at 2 s/2 s beats both the segment-shuffle and data-sliding 95th percentiles in at least as large a share of interactions as the Delayed Mirror does.
   - The human–human share is reported as the reference.

**A dial analysis (the project's own; labelled; no accepted benchmark exists for it):**
- Within each interaction, regress the listener's AU windows on the speaker's lagged AU windows. Do this separately by condition (familiar against stranger in naturalistic sessions; repeat against first meeting for V00 improvised pairs).
- Test whether the response *profile* (the normalized regression matrix), and not only its overall gain, differs by condition, with a permutation null over condition labels.
- A one-gain model predicts the profile is the same in every condition.
- The analysis is run first on the human ground truth. If humans show no profile shift, it is not used to judge architectures.

**A screening pass is a filter, not a claim** (operator note Q11).

## Pilot subset, download path, and corrected budget (2026-11-25T09:35:15Z)

**Correction to the data budget above.** The figure of about 0.5 MB per file came from one 88-second sample. research/seamless-interaction.md gives the measured mean file sizes for V00, which are larger: about 1.6 MB per improvised file and 1.2 MB per naturalistic file. Every split file is V00, because has_imitator_movement = 1 only for V00.

| Set | Files | Approx. size |
|---|---|---|
| Train | 20,356 | ~28 GB |
| Val | 1,394 | ~2.0 GB |
| Test | 874 | ~1.2 GB |

**Pilot v1, fixed:** research/harness/pilot_v1.json (sha256 prefix 4932794aa45799da), made by pilot.py:

| Split | Interactions | Files | Improvised |
|---|---|---|---|
| Train | 300 | 600 | 155 |
| Val | 150 | 300 | 103 |

- About **1.3 GB** in total.
- The test split is untouched.

**Download path:** research/harness/fetch.py.
- **Allow-list:** FAUValue, is_valid, transcript, VAD. A deny assertion runs on every URL (emotion fields, mp4, wav, is_occluded).
- **Free-disk check:** run before every file. The script stops if free space is below 20%.
- **Not yet run:** the disk is at 12% free.
- **Peak memory planned:** under 2 GB for baselines and metrics. The FD covariance is 1472 × 1472, and the largest array is the train window bank (about 0.2 GB on the pilot).

## Dial analysis: code fixed 2026-11-25T09:55:58Z, before any data beyond the one local sample pair

research/harness/dial.py implements the analysis described above (D75), with these parameters fixed now:

**Response profile:**
- **Features:** the partner's AUs, z-scored within the interaction and averaged over lags of 1–10, 11–20 and 21–30 frames (69 features).
- **Fit:** ridge regression onto the listener's z-scored AUs, with λ = 100 (scaled by n/1000), giving B (69 × 23).
- **Decomposition:** gain g = ‖B‖_F and profile P = B/g.
- **Frames:** valid frames only, at least 500 rows.

**Within-person test:**
- D_profile = mean over people of ‖mean P(familiar) − mean P(stranger)‖_F.
- D_gain is the same comparison applied to log g.
- **Null:** condition labels permuted within each person, 1,000 times, seed 0.
- **Sensitivity:** λ = 10 and λ = 1000 are reported alongside.

**Reading the result.** If people's familiar and stranger profiles don't differ beyond the null, one dial describes humans too.

**Equation checks only, not results.**
- The lag-bin features equal their direct means.
- Synthetic records with a profile shift built in give p_profile = 0.005.
- Synthetic records with only a gain change give p_profile = 0.62 and p_gain = 0.005.

So the test separates the two cases it is meant to separate.

## Source reading: second pass, stood down (2026-11-25T09:55:58Z)

**L2L Appendix D and Table 7.** Two fetches each returned only a model summary, not verbatim text, because the page is cut off past about 40,000 characters. Under the "fails twice" rule this step is **stood down**.
- The readings already fixed for unspecified items stand.
- Table 7's TLCC values are recorded as **summary-only**, for comparison and never as a threshold: GT 17.3, NN 15.3, Random 13.2, Mirror 0.0, Delayed Mirror 17.0, Ours 15.8 (expression).

**Song et al. 2023 (arXiv 2302.06514, Sec. 3.2), REACT's metric definitions:**
- **FRDiv:** the paper's formula is a *sum* of pairwise squared errors; the official code *normalises* it.
- **TLCC:** the paper gives no lag window; the code uses ±49 frames.

The challenge's published numbers come from the code, so the code's definitions are used (as published) and the paper's are noted.

## E3 compute budget and screening subset: fixed 2026-11-25T10:05:24Z

**Measured on the local pair (2,640 frames, 23 channels):**
- one E3 score takes 0.17 s at 2 s/2 s and 0.26 s at 30 s/5 s;
- wcc_global_mc, the all-channel form, equals the per-channel mean to 6 decimals;
- one test (the observed score plus 2 × 1,000 surrogates) takes about 350 s at 2 s/2 s.

**Screening subset:** research/harness/e3_subset_v1.json, 20 validation interactions from the pilot, ordered by sha256('affect-e3-v1:'+interaction). Twenty is the minimum number of runs evaluation.md S1-a asks for.
- **Setting:** 2 s/2 s only. The 30 s/5 s setting is reported for the final candidates.
- **Direction:** the predicted listener against the real speaker.
- **Surrogates:** 1,000 of each type.
- **Processes:** 8 in parallel.

**Cost:** about 45 s per interaction per row, so about **15 minutes per row** and about **4–5 hours** for all 19 rows plus the human reference.
- Peak memory is under 1 GB.
- **Constant predictors** (Median, B_MeanFr) have no within-window variance. Their E3 score is recorded as "undefined (constant)" rather than computed.

## Harness v2: the REVIEW-1 fixes (2026-11-25T10:24:20Z, before any scoring)

An independent review (research/harness/REVIEW-1.md) found **8 bugs and 4 spec deviations**. All were fixed. Each fix was checked against its definition on the local pair or on synthetic records; these are code checks, not results.

### Bugs

| # | Fix | Check |
|---|---|---|
| B1 | E3 now masks is_valid: an element is dropped if either window holds an invalid frame, and the partner's mask moves with its surrogates | the masked score equals a naive masked loop (0.30965 = 0.30965) |
| B2 | the 500-frame rule counts jointly valid frames, and exclusions are returned | – |
| B3 | one function, wcc_global_mc, takes 1-D or 2-D input | its 2-D score equals the mean of the 1-D scores |
| B4 | the dial test now averages per session, permutes session labels within a person, and tests only people with at least 3 sessions. People with one session per condition are reported descriptively, with a warning. | in a synthetic case with no condition effect and per-session offsets, the false positive is gone (p = 0.095), while a real profile shift is still detected (p = 0.005) |
| B5 | the dial test uses a validity mask per person; z-statistics come from jointly valid frames; X, C and Y are centred. **Added:** the listener's own-lag bins as Granger-style controls, so the "response" is not the speaker following the listener. | – |
| B6 | constant predictions give TLCC (nan, nan), recorded as "undefined (constant)" | – |
| B7 | window starts are range-checked; one shared list of valid window starts (start ≥ 17, all frames from start−17 to start+64 valid) is used for every method and the ground truth | – |
| B8 | TrainBank takes train-split file IDs only, and asserts that no person overlaps the query set | both assertions fire on bad input |

### Spec deviations

- **S1:** REACT metrics and baselines run on 750-frame clips, the published length. The lag window of ±49 frames (the published frame count) and of ±59 (the published 2 s at 30 Hz) are both reported.
- **S2:** L2L TLCC and SI run on 256-frame sequences. This is UNSPEC, taken from Appendix D, which was read only as a summary. Each 256-frame sequence is four consecutive 64-frame predictions (UNSPEC).
  - The reviewer showed that on 64-frame windows white noise peaks at a lag of 52.6, so the number mostly measured window length.
  - A shuffled-pair noise floor is reported with every TLCC.
- **S3:** SI is fixed as one histogram per 256-frame sequence, natural-log Shannon entropy, averaged over sequences (UNSPEC).
- **S4:** people are keyed by numeric ID with the "A" suffix stripped. The dataset README warns that one person can have several IDs, and 7 such pairs straddled splits. This gives **splits_v3**.

### Also fixed

- FD asserts more windows than T·d, with an eps fallback that is flagged.
- REACT TLCC reports its NaN lags.
- Absolute paths throughout.

## Splits v3, pilot v2 and E3 subset v2: fixed 2026-11-25T10:24:20Z. They replace v2/v1, and nothing was scored on the old ones.

**splits_v3.json** (sha256 prefix fc2a61b23701bb21):

| Split | Files | People | Familiar / stranger interactions |
|---|---|---|---|
| Train | 21,528 | 706 | 3,740 / 7,024 |
| Val | 852 | 37 | 79 / 347 |
| Test | 970 | 50 | 135 / 350 |

- 9,725 straddling interactions are dropped.
- The splits are disjoint by numeric person ID (verified: 0 overlap).

**Derived files:**
- **pilot_v2.json** (4567f785c057432a): 300 train and 150 validation interactions, 900 files.
- **e3_subset_v2.json** (cf593441f2d4f0be): 20 validation interactions.

## Screening condition 4 revised (2026-11-25T10:24:20Z, before scoring)

The reviewer pointed out that Delayed Mirror equals the speaker at lag 17, so it passes E3 in almost every interaction. Condition 4 as written would demand that every interaction pass.

- **Revised:** the E3 pass share on the 20-interaction subset must be **at least the human ground truth's pass share** (the real listener against the real speaker) on the same subset.
- Delayed Mirror's share is reported for reference.

## Dial analysis scope (restated)

- It runs on human data in the **training split only**: neither validation nor test has a person with both familiar and stranger sessions.
- Partner identity is confounded with condition.
- The repeat-against-first-meeting contrast uses the same function, with conds = ("repeat", "first").
- Judging architectures with it on validation data remains between-person (D75).

## Screening runner (2026-11-25T10:25:24Z)

**research/harness/run_screen.py** scores these rows on the pilot's validation pairs, in both directions:
- the ground-truth listener, as a reference row;
- L2L Median, Random, NN, Mirror (identity, and a 5-frame mean) and Delayed Mirror.

Each row is written to research/runs/screen/<row>.json, with its run time and peak memory.

**Guards:**
- The runner refuses to run unless pilot_v2 is downloaded.
- The bank is built from train-split pairs through the guarded TrainBank.

**Check mode** (`--check`): runs on the local sample pair. **Numbers in check mode are not results.**

It confirmed:
- the ground truth has L2 = 0;
- Mirror's TLCC lag is 0 and Delayed Mirror's is 17;
- Median's variation and SI are 0;
- each row takes about 0.1 s and under 75 MB.

**One more fix:** float rounding made a constant predictor look non-constant (Median got a TLCC lag where it should have none). Channels with a variance below 1e-9·n now count as constant.

**Still to add to the runner:** the REACT rows (750-frame clips; FRVar, S-MSE, FRDvs, FRSyn under both lag readings) and the E3 test on e3_subset_v2 (human reference first).
