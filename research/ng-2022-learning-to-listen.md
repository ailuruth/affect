# Learning to Listen (Ng, Joo, Hu, Li, Darrell, Kanazawa, Ginosar; CVPR 2022)

Sources read: arXiv 2204.08451 full PDF (Sec. 3 Method, Sec. 4 Dataset, Sec. 5 Experiments, Appendix B-D incl. metric definitions); github.com/evonneng/learning2listen README (full), `src/requirements.txt`, `src/test_vq_decoder.py` (CUDA calls), repo file list and GitHub license field; Google Drive download pages for the four model tars (names and sizes only, nothing downloaded); HTTP HEAD on two data tars.

## What it predicts, from what
- Output: listener face per frame as `f_t = [β_t, R_t]`: "The 3DMM defines 50 expression coefficients along with a 3D jaw rotation (d_m = 53), and 3D head rotation in Euler angles" (Sec. 4). Coefficients come from DECA (FLAME), extracted at 30 fps. No voice output.
- Input: speaker audio and speaker face motion. "From the speaker, we take as input both audio a = A^S_{1:t+w}, and facial motion m = F^S_{1:t+w}. Here, w is the amount of additional future context" (Sec. 3.3), w = 8 frames. Audio is a librosa mel spectrogram (128 bins, 16 kHz, 4x the frame rate, max-pooled to 30 Hz; App. B). Speaker audio is cleaned of listener back-channels by sound-source separation.
- Model: transformer VQ-VAE codebook of listener motion (K = 200, window 8 frames), then an autoregressive transformer predicting the next codebook index from a cross-modal (audio-queries, motion-keys) speaker embedding; nucleus sampling at test time (Sec. 3.2-3.4, 4).
- Person-specific: "each codebook and predictor model is trained on a specific listener" (Sec. 5).
- Training data: 72 h of split-screen YouTube interviews from 6 channels (Conan, Devi, Fallon, Kimmel, Stephen, Trevor); train/val/test 70/20/10.

## Released code and weights
- Code: yes. GitHub license field: none; no LICENSE file in the repo. Treat as all rights reserved.
- Weights: yes, four person-specific models (Conan, Fallon, Stephen, Trevor), Google Drive: `conan_models.tar` 212 MB, `fallon_models.tar` 212 MB, `stephen_models.tar` 212 MB, `trevor_models.tar` 212 MB (sizes from the Drive download page). Each holds a VQ-VAE and a predictor. No weights license stated.
- Data: `http://learning2listen.berkeleyvision.org/<name>_data.tar`; `conan_data.tar` is 14.4 GB, `fallon_data.tar` 5.8 GB (Content-Length). Precomputed DECA (184-d per frame: expression 50, pose 6, detail 128) and mel features; raw video on request.
- Photoreal renderer not released ("As part of responsible practices").

## Published metrics (Table 1, aggregated over 4 listeners)
Definitions (Sec. 5.1, App. D), computed separately on expression and rotation, "against the raw ground truth listener motion":
- L2: `d = ||y − ŷ||` to ground truth.
- FD: Fréchet distance "in the expression space R^{T×d_m} or the head pose space R^{T×3} on the full motion sequence".
- variation: "variance along the axis representing the temporal extent T ... then average over B and F".
- SI: k-means on training expressions/rotations (k = 15, 9), "avg. entropy (Shannon index) of the cluster id histogram".
- P-FD: FD on "concatenated listener-speaker expression R^{T×(d_m+d_m)} / pose R^{T×(3+3)}".
- PCC: Pearson correlation of lip curvature (smile) and of up/down head motion between listener and speaker.
- TLCC: speaker shifted 0-60 frames; peak gives lag.

Expression results: Ours L2 33.16, FD 3.55 (×10³), variation 2.01 (GT 2.90), SI 2.48 (GT 2.61), P-FD 5.15 (×10³), PCC 0.07 (GT 0.09). Strongest baseline NN motion: L2 45.76, FD 20.66, P-FD 21.94, PCC 0.02. Median: L2 43.18, FD 64.48. Mirror: PCC 1.00, P-FD 75.30. Rotation: Ours L2 4.75, FD 0.81 (×10²).
- TLCC: "the average TLCC calculated for GT and Ours were both ≈ 17 frames ... ≈ 0.5s".
- User study: Ours preferred over NN by 75.3%, over a+m ablation 71.1%, over GT renders 50.1% (150 evaluators, 50 curated clips).

## Runs on this Mac as published?
- No. Tested with "cuda/9.0 ... python 3.6.11"; `test_vq_decoder.py` calls `.cuda()` unconditionally (lines 75, 104, 111, 186), so inference fails without CUDA unless the code is edited. README also requires editing torch's own `conv.py`. Models are small (~212 MB per person), so memory would not be the limit after porting; no custom CUDA kernels seen.
- Rendering: DECA renderer (pytorch3d) for meshes; not needed for the metrics.

## Runnable on Seamless features as published?
- No. Input needs speaker DECA/FLAME expression + jaw + head rotation and a speaker mel spectrogram from raw audio; Seamless gives 24 `FAUValue` AU intensities, transcripts and VAD, no FLAME, and we use no audio. Output is FLAME coefficients; there is no published map to Seamless AUs. The listener models are fixed to four TV hosts.

## Verdict: not runnable (needs DECA/FLAME speaker motion and raw audio; CUDA-only code; no license)
- Takeaway for us: its naive baselines and metrics are representation-agnostic and could be computed on Seamless AU series directly: Median, Random (training clip), NN motion, Mirror, Delayed Mirror (17 frames ≈ 0.5 s, chosen by TLCC), plus L2, FD, P-FD, variation, SI, PCC, TLCC. That is a re-use of the protocol, not of the model.
