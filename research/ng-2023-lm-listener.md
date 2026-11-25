# Can Language Models Learn to Listen? (Ng*, Subramanian*, Klein, Kanazawa, Darrell, Ginosar; ICCV 2023; arXiv 2308.10897v2, 3 Jun 2026)

Sources read: arXiv 2308.10897v2 full PDF (Sec. 3 Method, Sec. 4 Dataset and Metrics, Sec. 5 Results, App. B-E incl. the 2026 content-overlap addendum and Table 8); github.com/sanjayss34/lm-listener README (full), `requirements.txt`, CUDA calls in `train_t2m_trans.py`, repo file list and license field; Google Drive folder listing for the pretrained model and data (names and sizes only).

## What it predicts, from what
- Output: listener face `f_t = [β_t, R_t]`, EMOCA (FLAME) expression coefficients plus head orientation in Euler angles (Sec. 3.1, 4.1); decoded from VQ-VAE tokens (codebook 256). No voice.
- Input: speaker's transcript only, with word timestamps. "The model takes as input text tokens (blue), along with their timestamps" (Fig. 2); `f̂_t = G(W^history, W_{1:t}, M_{1:t}, F_{1:t−1})` (Sec. 3.1). Generator is GPT-2 Medium (345M parameters), fine-tuned; max 240 frames (8 s) of motion, 480 input tokens (App. B).
- Training data: Trevor Noah listener from the L2L dataset, re-segmented to up to 8 s, EMOCA instead of DECA, Whisper word-level transcripts, PyAnnote diarization; 2,366 train / 222 val / 543 test segments (Sec. 4.1). Person-specific; Conan and Stephen models in App. C.

## Released code and weights
- Code: yes; GitHub license field: none, no LICENSE file. Much code from T2M-GPT.
- Weights: Trevor Noah only, Google Drive folder `lm_listener_pretrained`: `trevor_hist3/net_last.pth` 702 MB (LM) and `VQVAE_l1smooth_c256_p8_datav2/net_iter300000.pth` 103 MB (VQ). No weights license.
- Data: `lm_listener_data.zip` 5.9 GB on Drive; updated test files (June 2026) drop clips that overlap with training videos.
- Evaluation also needs EMOCA (for the affect metric) and DECA (for visualization), each with its own model download and license.

## Published metrics
Definitions (Sec. 4.2): L2 "on ground truth expression coefficients and pose"; FD in expression R^{T×d_m} and pose R^{T×3}; Variation "Variance calculated across the sequence"; Diversity: "randomly sample 30 pairs of listener pose and expression parameters within a sequence ... average Euclidean distances"; P-FD "FD on concatenated listener-speaker motion"; L2 Affect: EMOCA valence (AffectNet-trained classifier) averaged over 1 s windows, L2 to ground truth in a sliding window. Standard errors by 10,000-sample bootstrap.

Table 1 (original test set): Full L2 0.43, FD 18.22, variation 0.116 (GT 0.11), diversity 2.81 (GT 2.59), P-FD 19.63, L2 Affect 6.36 (×10²). NN: 0.52 / 23.68 / 0.087 / 2.25 / 24.78 / 7.88. Uncond: L2 0.39 but variation 0.002.
Table 8 (2026, overlap removed): Full L2 0.53, FD 22.13, P-FD 23.83, L2 Affect 7.77; NN 0.61 / 28.32 / 29.57 / 9.29. The authors: "105 clips in the test set that come from a video which overlaps with two videos in the training set".
Human study: preferred over NN and over L2L (55.7%).

## Runs on this Mac as published?
- No. `train_t2m_trans.py` calls `.cuda()` and `torch.cuda.amp` throughout (lines 59-181); the generation command uses `--manual-bf16`. GPT-2 Medium plus VQ (~0.8 GB of weights) would fit in 16 GB after porting, but that is an adaptation.

## Runnable on Seamless features as published?
- Input: yes in principle. Seamless transcripts give word-level `start`/`end` times, which is the input format the model takes (words plus end-of-word frame index).
- Output: no. It emits Trevor Noah-style EMOCA/FLAME coefficients; Seamless gives 24 `FAUValue` AUs and no FLAME, so none of its metrics can be computed against Seamless listeners without a FLAME-to-AU mapping that the paper does not provide. Also the language domain (late-night TV) and listener (one host) differ from Seamless.

## Verdict: not runnable as published (output representation absent from Seamless; CUDA-only code; no license)
- Takeaway: the only published listener model whose input is computable from Seamless (timestamped transcript). Its text-only result (beats NN and is preferred to L2L in a user study) is a reference point that words alone predict some listener face motion. Note the 2026 erratum: train/test overlap inflated the original numbers.
