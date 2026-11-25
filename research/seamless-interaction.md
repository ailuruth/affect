# Meta Seamless Interaction: dataset and dyadic motion models (arXiv 2506.22554, 2025)

Sources read: github.com/facebookresearch/seamless_interaction README (full); arXiv 2506.22554 full PDF (via text search of sections 1, 2, 4.4, appendix); Meta publication page abstract.

## Claims
- Dataset: over 4,000 hours of face-to-face interaction from more than 4,000 participants, Naturalistic and Improvised, with transcripts, VAD, SMPL-H body, keypoints and "Imitator" movement features at 30 Hz.
- Models: "Dyadic Motion Models" that generate face and body codes "aligned with human speech" and "can take as input both the speech and visual behavior of their interlocutors", an LLM-speech variant, and controllable variants that "adapt emotional responses".

## Evidence
- README feature table: `FAUValue` gives 24 action-unit intensities (InnerBrowRaiser ... EyesClosed); `emotion_scores` gives 8 categorical emotion scores; `emotion_valence` and `emotion_arousal` in [-1, 1].
- Emotion control (Sec. 4.4.1) buckets arousal and valence from "an internal tool" and conditions the generator on them; LLM-guided generation predicts 12-bin valence and arousal tokens.
- README: HyperModel-related features "are extracted from or designed for proprietary models that are not yet being released publicly." I found no released model weights in the repo.
- Size: about 27 TB in total, or about 50 GB per HF batch.

## License (paper, code, model weights)
- Dataset: CC-BY-NC 4.0 (README). Repo code: GitHub reports NOASSERTION (I did not read a separate code license). Models: not released.

## Runs on this Mac without a GPU?
- Models: not applicable (unreleased; decoders were trained on H100s per the report). Dataset: streaming single examples (~100 MB) works on any machine.

## Verdict: watch (dataset only)
- Models: their face moves because the partner's audio and video predict it, with emotion as a valence and arousal knob. That breaks the item rule as a "when/why" source and Principle 2.
- The dataset's precomputed features include classifier outputs (`emotion_scores`), so we must not read them, but `FAUValue` (24 AUs at 30 Hz) could give a human reference for the R-DGG-style contingency test. It must never be used to train when the Bot's face moves.

## Role in S2
- none (possible offline evaluation reference)

## 2026-11-24: does it publish a human reference for dyadic mimicry or timing?

Sources read: arXiv 2506.22554 HTML, characters 0-300,000 of 316,038; the last 16,038 characters were not read; README "Annotation Types" and limitations sections.

- No. The paper reports no statistics on facial mimicry, cross-partner correlation, lag between partners' expressions, smile mirroring, nod timing or turn-taking gaps for human data. "Smile mirroring" appears only as a qualitative claim about the generated models (Sec. 1).
- Its automatic metrics compare generated output to ground truth, not to the partner: "FFD is the Fréchet distance of Imitator features between predictions and ground truth"; "Sync-C and Sync-D assess the lip synchronization with speech" (Sec. 6.2.1). Neither is an interpersonal synchrony measure.
- A human reference would have to be computed by us: run WCC plus surrogates (moulder-2018-synchrony-surrogates.md) on the two partners' `FAUValue` series. That is a derived number, not a published one.
- New and relevant to "face follows internal state": released self-report annotations. README: 1P-IS "1st-party internal state annotations", 751 annotations over 1.1 h; 3P-IS third-party, 5,132 over 4.7 h; 3P-V visual descriptions. Paper App. A.4: participants, about 24 h later, review timestamped moments and "try to annotate their internal states at those moments". Short text (mean 5.8 tokens per 1P-IS annotation); no rating scale is described; no inter-rater agreement reported. Usable at most as a qualitative human reference.
- Timing caveat (README): human time-stamping errors leave "approximately 10% of the interactions" affected (start/end times, prompt alignment). This concerns segment boundaries, not the alignment between the two partners' streams.

## 2026-11-25: file layout for candidate tests

Sources read: Hugging Face dataset card `facebook/seamless-interaction` (README.md, full) and its file tree (21,970 files, listed with `huggingface_hub`); GitHub README (full), `src/seamless_interaction/constants.py` and `fs.py` (S3 paths); the four metadata CSVs. Files inspected locally (in `research/data/seamless/`, no video or audio): the CSVs, one dev transcript tar and one dev VAD tar from HF, and, from S3, `FAUValue`, `is_valid`, transcript and VAD files for one naturalistic pair (`V00_S0080_I00000377`, participants `P0115` and `P0116`). Counts below are computed from `filelist.csv` and the CSVs; durations from HTTP HEAD sizes of 600 V00 and 300 V02 `FAUValue` files (no download).

### Identifiers
- One file per participant per interaction: `V<vendor>_S<session>_I<interaction>_P<participant>` (e.g. `V00_S0080_I00000377_P0115`). A pair = the two file IDs sharing `V.._S.._I..`; 64,619 of 64,751 interactions have both partners, 132 have one.
- `I<interaction>` is the prompt hash (`prompt_hash` in `interactions.csv`), not an ordinal: 1,206 of 1,292 prompt hashes recur in more than one session.
- Participant IDs are vendor-scoped and sometimes alphanumeric (`P0844A`, `P0933A`): 685 `participant_id` values recur across vendors in `participants.csv`, and 20,533 file IDs have a non-numeric participant. Key a person as `(vendor, participant_id)`. The repo's own regex `V(\d+)_S(\d+)_I(\d+)_P(\d+)` truncates the `A` suffix; use `P(\w+)`. README also warns of "Duplicate participant identifiers being assigned to different individuals" and the reverse.
- `participants.csv`: `extraversion_raw, agreeableness_raw, conscientiousness_raw, neuroticism_raw, openness_raw, vendor_id, participant_id` (BFI-2; 1,937 of 4,284 rows "Undisclosed"). No demographics, no dates.

### Familiar vs stranger, repeat partners
- `relationships.csv`: `vendor_id, session_id, relationship, relationship_detail`, one row per session (5,098 sessions). `relationship` is `familiar` (1,751) or `stranger` (3,347). `relationship_detail` is `friends` 1,059, `coworkers` 232, `family-generic` 155, `familiar-generic` 154, `dating/spouse/romantic_partner` 98, `classmates` 38, `siblings` 8, `parent_child` 4, `neighbors` 2, `roommates` 1, else `stranger`. Join key: `vendor_id` (`V00`) + `_S` + `session_id` matches the file ID's session (97.7% of file IDs match; the rest have no label).
- All improvised sessions are `stranger` (or unlabeled). Familiar pairs exist only in naturalistic.
- Repeat partners (same two vendor-scoped IDs in at least two sessions): V00 has 195 such pairs, all improvised (actor pairs), median 27 interactions per pair, up to 12 sessions (e.g. `P0933A`/`P0974A`). V00 naturalistic pairs never repeat, though naturalistic participants meet up to 10 different partners. V02 has 7 repeat pairs, 5 of them labeled `familiar` in one session and `stranger` in another (label noise or acquaintance; unresolved).
- Session order and dates: not released. No timestamp column anywhere; `session_id` is numeric but its ordering is undocumented; `batch_idx`/`archive_idx` are not chronological; interaction order within a session is not given (only "active time" is released; "Meta time" between prompts is not).

### Where `FAUValue` lives and who has it
- Per participant per interaction, one array. On S3: `https://dl.fbaipublicfiles.com/seamless_interaction/{label}/{split}/movement/FAUValue/{file_id}.npy` and `.../movement_v4/FAUValue/{file_id}.npy` (v4 added December 2025, "gradually rolled out"). On HF it is only inside the ~1 GB WebDataset tars (`{label}/{split}/{batch:04d}/{archive:04d}.tar`), as npz key `movement:FAUValue`, bundled with that participant's `mp4` and `wav`.
- Observed: `float64`, shape `(T, 24)`, T = 30 Hz frames; both partners of the sampled pair have T = 2640 (88 s), and transcript times run 0-84 s, so the two streams share one interaction clock (observed in one pair; not documented). Values 0 to about 2, not FACS 0-5. `movement/is_valid` is `(T, 1)`. v1 and v4 `FAUValue` differ (max abs difference 0.46 in one file).
- Column names (GitHub README, "maps to 24 dimensions including"): `InnerBrowRaiser`, `OuterBrowRaiser`, `BrowLowerer`, `UpperLidRaiser`, `CheekRaiser`, `LidTightener`, `NoseWrinkler`, `UpperLipRaiser`, `LipCornerPuller`, `CheekPuffer`, `Dimpler`, `LipCornerDepressor`, `LowerLipDepressor`, `ChinRaiser`, `LipPuckerer`, `LipStretcher`, `LipFunneler`, `LipTightener`, `LipPressor`, `LipsParts`, `JawDrop`, `LipSuck`, `JawSideways`, `EyesClosed`. The README does not say this is the column order. Checks on the one pair: column 20 (`JawDrop`) has the highest correlation with own VAD speech (r = .51, .59), which fits; columns 12 and 19 (`LowerLipDepressor`, `LipsParts`) are byte-identical in both participants; column 23 (`EyesClosed`) has mean 1.28, implausible for an awake speaker. Treat the order as unverified until checked on more files.
- Availability: `filelist.csv` column `has_imitator_movement` is 1 for 42,932 of 129,370 files, all of them vendor V00 (and every V00 file). HEAD probes: `movement/FAUValue` 403 for all sampled V01, V02, V03 files; `movement_v4/FAUValue` 200 for 37/40 V02 files, 58/60 V00 files, 0/40 V01 and 0/40 V03. So usable AU data: V00 (v1 and v4) and most of V02 (v4 only).
- `filelist.csv` columns: `file_id, label, split, batch_idx, archive_idx, has_imitator_movement, has_annotation_1p, has_annotation_3p`. It is not complete: HF dev transcripts include `V03_S0752_*`, which is absent from it.

### Transcripts and VAD
- S3: `.../{label}/{split}/metadata/transcript/{file_id}.jsonl`, one segment per line: `{"words": [{"word", "start", "end", "score"}, ...], "start", "end", "transcript"}`; times in seconds from interaction start. HF: `{label}/{split}/extras/metadata/transcript/NNNN.tar` (1-33 MB each) holds `{file_id}.json` containing a JSON array with one string of the same JSONL.
- VAD: `.../metadata/vad/{file_id}.jsonl`, lines `{"start", "end"}` in seconds (README says "100 Hz"; the released form is segments). HF: `extras/metadata/vad/NNNN.tar`.
- Turns are not given; derive them from the two partners' VAD or word timestamps.

### Splits and minutes
- `naturalistic` ("Prompted conversations that can be carried out by normal people") and `improvised` ("predefined scenarios with guided prompts with at least one professional actor"), each with train/dev/test. 99 participants appear in more than one split.
- V00 (AU data): 1,316 participants, 2,000 sessions, 21,532 interactions; files improvised train/dev/test 24,816/340/186, naturalistic 16,464/622/504. Interactions per session median 9. Mean interaction length (HEAD sample): improvised 281 s, naturalistic 208 s. Estimated AU minutes per participant: median 56, p90 209; 610 participants have at least 60 min, 209 at least 120 min. Mix: 674 familiar-only, 475 stranger-only, 160 both.
- V02 (v4 AU only): 540 participants, all naturalistic, 925 sessions (familiar 7,300 / stranger 7,786 interactions), median 17 interactions per session, mean 180 s each. Estimated minutes per participant: median 90, p90 454; 205 participants have both familiar and stranger sessions, a within-person familiarity contrast.

### Feature-only download
- Yes, via S3 per-file URLs above; no video or audio needs to be fetched. Per interaction-participant: `FAUValue` about 0.5 MB (88 s), `is_valid` 21 KB, transcript about 10 KB, VAD about 1 KB. `FAUValue` is float64, 5.76 KB per second, so all V00 FAU is about 60 GB (24,816 improvised files × 1.6 MB + 18,116 naturalistic × 1.2 MB, from mean durations; not measured). A pair-level pilot of a few hundred interactions is under 1 GB.
- HF has no feature-only shards for movement; its `extras/` holds only `audio`, `video`, `smplh` and `metadata/{transcript,vad}`.
- Safety: one `movement_v4/is_occluded` file was a pickled object array; I deleted it. Always `np.load(..., allow_pickle=False)`.

### Licenses seen
- Dataset `LICENSE` on HF and the GitHub repo's `LICENSE` are both the CC BY-NC 4.0 legal text (the repo code is therefore also CC BY-NC, which settles the earlier "NOASSERTION"; `constants.py` headers still say "BSD-style license").

### Minimal loader plan
1. Inputs: `filelist.csv`, `relationships.csv`, `participants.csv` (IDs only; BFI not needed). Select V00 (and V02 for v4) file IDs, group into pairs by `V_S_I`, join `relationship` by session, key people by `(vendor, participant_id)`.
2. Fetch only an allowlist of URL suffixes: `movement/FAUValue`, `movement/is_valid` (or the `movement_v4/` versions, never mixing the two within one analysis), `metadata/transcript`, `metadata/vad`. The loader builds URLs from this allowlist; nothing else is requested, so the classifier files are never downloaded.
3. Denylist, enforced in code with an assertion on every URL and npz key: `emotion_scores`, `emotion_valence`, `emotion_arousal`, `EmotionValenceToken`, `EmotionArousalToken` (the tokens are quantized classifier outputs). Never use the HF tars or the repo's `gather_file_id_data_from_s3` (it fetches every modality including video and the emotion files). If an npz is ever used, open it lazily and index only `movement:FAUValue` and `movement:is_valid`; never iterate its keys.
4. Load with `np.load(path, allow_pickle=False)`; mask frames where `is_valid` is 0; check both partners have equal T before pairing; if columns 12 and 19 are identical in a file, keep one; record v1 vs v4.
5. Store under `research/data/seamless/s3/{label}/{split}/...` mirroring the S3 path.
