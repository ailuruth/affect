# Responsive Listening Head Generation, ViCo (Zhou, Bai, Zhang, Yao, Zhao, Mei; ECCV 2022)

Sources read: arXiv 2112.13548 full PDF (Sec. 3 dataset and task definition, Sec. 5 experiments, Tables 3-4); github.com/dc3ea9f/vico_challenge_baseline README (full), file list, issue list (searched for weights).

## What it predicts, from what
- Output: listener 3DMM "expression and pose" coefficients m = (β, p) per frame from Deep3DFaceRecon (BFM basis), rendered to video by PIRender with the listener's identity coefficients.
- Input: speaker audio features (45-d: 14 MFCC, 28 MFCC deltas, energy, ZCR, loudness), speaker 3DMM expression+pose per frame, a reference listener frame, and an attitude label (positive / neutral / negative). Generator is an LSTM (Sec. 5.2). Formula: `m^l_{t+1} = G(M^s_t, S^s_t, m^l_1, e)`.
- Data: ViCo, 483 YouTube clips, 92 identities (67 speakers, 76 listeners), 30 fps, 1-71 s clips.

## Released code and weights
- Code: yes (training, inference, rendering, evaluation). GitHub license field: none.
- Weights for the listener generator: not released. README gives only training commands; the only pretrained weights it links are third-party (PIRender, Deep3DFaceRecon, ArcFace for evaluation). No issue mentions released listener weights.
- Dataset on OneDrive.

## Published metrics
- "we use L1 distance between the generated features and the ground-truth features (FD)" on angle / expression / translation (Table 3, ×100). Average over attitudes, D_test: Ours 7.79 / 15.04 / 6.52; "Simulation" (repeat training motion) 10.81 / 27.37 / 13.52; Random 18.04 / 44.67 / 19.80. OOD set: Ours 8.23 / 22.83 / 8.32.
- Renderer: FID, SSIM, PSNR, CPBD (Table 4).
- DIM (Tran et al. 2024) later reports RLHG on ViCo as FD 39.02 (exp), P-FD 40.18, MSE 0.86, under its own re-implementation.

## Runs on this Mac as published?
- Not applicable for the listener model (no weights). Training scripts use `torch.distributed.launch` with 4 GPUs; renderer and face reconstruction use CUDA.

## Runnable on Seamless features as published?
- No. Needs speaker audio and BFM 3DMM coefficients from video, an attitude label, and outputs BFM 3DMM, none of which Seamless provides.

## Verdict: not runnable (no released listener weights; needs raw audio and 3DMM)
