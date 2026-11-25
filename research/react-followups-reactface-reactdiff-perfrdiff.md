# REACT-family follow-ups: ReactFace (TVCG 2024), PerFRDiff (ACM MM 2024), ReactDiff (ACM MM 2025)

Sources read: READMEs of github.com/lingjivoo/ReactFace, github.com/xk0720/PerFRDiff, github.com/lingjivoo/ReactDiff; `configs/diffusion_model.yaml` (PerFRDiff) and `configs/config_train.json` (ReactDiff); repo license fields; ReactFace issue #1; Google Drive download pages for the two checkpoint files (names and sizes only). Papers: arXiv metadata only for ReactFace (2305.15748; Luo, Song, Xie, Spitale, Ge, Shen, Gunes). I did not read any of the three papers' methods or results, so no published metrics are quoted here.

All three are trained on REACT 2023/2024 data (NoXi, RECOLA, UDIVA; FaceVerse 58-d 3DMM, 25 fps) and evaluated with the REACT metrics (react-challenge-baselines.md).

## ReactFace (Luo et al.)
- Input: speaker video and audio (`--speaker-video`, `--speaker-audio`, plus a `--listener-portrait` for rendering); output FaceVerse 3DMM and rendered video.
- Code: MIT. Weights: not released; README only says "Path to the trained model checkpoint"; issue #1 (Jul 2025) "Is There a Pre-trained Checkpoint Available?" has no answer.
- Verdict: not runnable (no weights; raw video and audio).

## PerFRDiff (Zhu, Kong, Xie, Huang, Shen, Liu, Gunes, Song)
- Input (config): speaker audio (`audio_dim: 78`, MFCC as in REACT) and speaker 3DMM (`_3dmm_dim: 58`), with a 25-d emotion embedder; personalised weight editing from the listener's own past behaviour. Output: listener 3DMM / 25-d attributes.
- Code: MIT. Weights: one Drive file `checkpoints.tar.gz` **13 GB** (GAFRG, PWSG, PSSL blocks); externals in a second Drive file. Install uses `pytorch-cuda=11.8` and CUDA pytorch3d.
- Verdict: not runnable (raw audio + FaceVerse 3DMM; CUDA; 13 GB download).

## ReactDiff (Luo et al.)
- Input (config): `cross_visual_cond_dim: 58` (speaker FaceVerse 3DMM) and `cross_audio_cond_dim: 768` (a speech-encoder embedding of raw audio); output 58-d listener 3DMM ("58D 3DMM input, U-Net architecture with cross-attention").
- Code: GitHub license field none (no license). Weights: `reactdiff_checkpoint.pth` 359 MB on Drive. Install pins CUDA 11.8 torch and pytorch3d CUDA wheels.
- Verdict: not runnable (raw audio + FaceVerse 3DMM; CUDA; no license).

## Runnable on Seamless features as published?
- None. All need FaceVerse 3DMM extracted from speaker video and raw speaker audio, and output FaceVerse 3DMM (plus REACT 25-d attributes), neither of which exists in Seamless.
