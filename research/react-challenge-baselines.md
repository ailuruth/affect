# REACT challenge baselines: Trans-VAE, BeLFusion, REGNN (Song et al.; REACT 2023, 2024; 2025-2026 repos)

Sources read: REACT 2023 challenge paper arXiv 2306.06583 (full PDF: Sec. 3 data, Sec. 4 metrics, Sec. 5 baselines and Tables 4-5); REACT 2024 paper arXiv 2401.05166 (Sec. IV-V, Table I); REGNN paper arXiv 2305.15270 (Sec. 5 setup and Table 1 only); READMEs of github.com/reactmultimodalchallenge/baseline_react2023, `baseline_react2024`, `baseline_react2025`, `baseline_react2026`; in `baseline_react2023`: `config/2_belfusion_ldm.yaml`, `metric/FRC.py`, `FRD.py`, `FRVar.py`, `FRDvs.py`, `S_MSE.py`, `TLCC.py`, `tool/matrix_split.py`; Google Drive folder listings (names and sizes only). I did not read the REACT 2025 or 2026 papers.

## What they predict, from what
- Output (all REACT entries): per frame a 25-d "facial attribute" vector: "15 AUs' occurrence (AU1, AU2, AU4, AU6, AU7, AU9, AU10, AU12, AU14, AU15, AU17, AU23, AU24, AU25 and AU26) are predicted by the state-of-the-art GraphAU model, while the facial affects (i.e., valence and arousal intensities) and 8 facial expression probabilities ... are predicted using the approach proposed by [37]" (2023, Sec. 5.1); plus 58-d FaceVerse v2 3DMM (52 expression, 3 rotation, 3 translation) for PIRender video. 25 fps, 751-frame (30 s) clips. Multiple samples (10) per speaker clip. No voice.
- Inputs:
  - Trans-VAE: speaker face frames through a CNN encoder plus "78-dimensional MFCC features" from audio (2023, Sec. 5.2). Offline (whole clip) and online (window w) variants.
  - BeLFusion: the speaker's 25-d facial attributes only. Config `load_video: false`, `load_audio: false`, `load_emotion: true`; `emotion_dim: 25`, window 50 frames. REACT 2024: "The competitive performance of such baseline without access to raw audio or video data".
  - REGNN: Swin-Transformer (FER2013-pretrained) on speaker face frames and VGGish on audio (REGNN paper Sec. 5; README).
- Data: REACT 2023/2024 = NoXi + RECOLA + UDIVA clips (~72 h total before split; train 8.6 h UDIVA + 13.2 h NoXi + 0.1 h RECOLA). REACT 2025/2026 = MARS dataset, signed EULA to the organisers.

## Released code and weights
- Code: `baseline_react2023` and `baseline_react2024` have no license (GitHub field none); `baseline_react2025` and `baseline_react2026` are MIT.
- Weights:
  - Trans-VAE (2023): Google Drive folder `trans-vae` (offline/online subfolders, plus `new-r.zip` 191 MB).
  - BeLFusion (2023, 2024): University of Barcelona SharePoint folder; size and license not visible without login. BeLFusion upstream repo license: NOASSERTION.
  - REGNN (2024): Drive folder `2024_REACT2024_FG_REGNN_baseline`: `mhp-epoch95-seed1.pth` (under 100 MB, no size shown), `swin_fer.pth` 106 MB, `vggish-10086976.pth` 275 MB, `vggish_pca_params`.
  - 2025 and 2026 baselines (Trans-VAE, REGNN, PerFRDiff, EEG heads): "Pretrained weights: [ ] to be released" in both READMEs (checked 2026-11-25).
  - Rendering: re-trained PIRender checkpoint and FaceVerse v2 (separate download, FaceVerse license).
- Data needed for evaluation (appropriate-reaction neighbour matrix) comes with the challenge data, which is gated.

## Published metrics and how they are computed
From the 2023 paper and `metric/*.py`:
- FRCorr (FRC): for each generated reaction, CCC against every "appropriate" real listener reaction (listeners of speakers whose behaviour is marked similar in `neighbour_emotion_*.npy`), take the max; mean over clips; then **summed** over the 10 samples (`return sum(all_FRC_list)`), so GT is ~8.7, not ~0.87.
- FRDist (FRD): DTW to the closest appropriate real reaction, weighted 1/15 over the 15 AUs, 1 over VA, 1/8 over expressions; summed over samples.
- FRDiv / S-MSE: mean squared pairwise distance between the 10 samples for the same speaker clip. FRVar: variance over time. FRDvs: pairwise distance across different speaker clips.
- FRRea: FID between rendered and real listener frames.
- FRSyn: TLCC between generated listener and speaker attributes over lags ±2 s; reported value is the mean absolute offset (frames) of the correlation peak; lower is better.

Test-set results (REACT 2024 Table I, offline): GT FRCorr 8.73, FRDist 0.00, FRSyn 47.69. B_Mime (copy speaker) 0.38 / 92.94 / 38.54. Trans-VAE 0.03 / 92.81 / 43.75. BeLFusion k=10 0.12 / 91.60 / 44.87. REGNN 0.19 / 84.54 / 41.35. REACT 2023 Table 5 (test): B_Mime FRC 0.38, FRD 92.95; best BeLFusion k=10 FRC 0.13, FRD 89.84; Trans-VAE 0.10 / 98.48.
- Read plainly: copying the speaker's face (B_Mime) beats every learned baseline on FRCorr in both years, and is close on FRDist. Only REGNN (FRDist 84.54) and later entries clearly beat it on distance.
- The REGNN paper reports the same method on another scale (FRDist 7.62, FRCorr 0.106; Table 1); its numbers are not comparable with the challenge tables.

## Runs on this Mac as published?
- No. All READMEs install CUDA builds (`torch==1.9.1+cu111`; 2025/2026: `pytorch-cuda=11.8` and a linux-64 pytorch3d CUDA wheel); scripts take `--gpu-ids`. BeLFusion's matcher and VAE are MLPs that would fit easily in memory after porting, but the published environment is CUDA-only.

## Runnable on Seamless features as published?
- Trans-VAE, REGNN: no; need speaker face video frames and raw audio.
- BeLFusion: no, though closest. Its input is the 25-channel REACT attribute vector: 15 GraphAU occurrence outputs in FACS-number order, plus VA and 8 expression probabilities from an emotion classifier. Seamless `FAUValue` is 24 intensities from a different (Meta) estimator with different units (0 to ~2) and a different AU set (the names overlap with most of REACT's 15, but Seamless adds e.g. `CheekPuffer`, `LipSuck`, `JawSideways`, `EyesClosed`, and its column order is unverified), intensities rather than occurrence, and its only VA / expression channels are classifier outputs we have denylisted (seamless-interaction.md). Feeding Seamless AUs would be an adaptation, and the 25-d output cannot be compared to Seamless listeners on the same scale.
- Metrics: FRCorr/FRDist need the dataset's appropriate-neighbour matrix, which Seamless does not have; FRVar, FRDiv, FRDvs and FRSyn (TLCC) are representation-agnostic and could be computed on AU series.

## Verdict: not runnable (raw video/audio or REACT's 25-d GraphAU+emotion representation; CUDA-only; 2025/2026 weights unreleased)
- Takeaway: the mimicry baseline B_Mime is a strong, honest floor: any listener model we evaluate on AUs should be compared with "copy the speaker's AUs" and "copy with ~0.5 s delay".
