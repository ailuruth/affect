# FaceAIS: Finite Scalar Quantization as Facial Tokenizer for Dyadic Reaction Generation (Dam, Nguyen, Tran, Lee; IEEE FG 2024; REACT 2024 winner)

Sources read: github.com/ais-lab/FaceAIS_REACT24 README (full) and license field; Google Drive folder listing of its checkpoints (names and sizes only). The paper is on IEEE Xplore (10581929); I did not read it and found no arXiv copy. Everything below is from the README.

## What it predicts, from what
- README "Model input and output": input "Speaker's voice: path to the audio file as the wav2vec will process the feature" and "Speaker's face: a tensor 58D containing 3DMM features" (FaceVerse); output "A tensor 58D containing 3DMM features of the listener's face" and "A tensor 25D emotion features" (REACT's 15 AUs + VA + 8 expressions).
- Method: FSQ face tokenizer (single-frame tokens) plus cross-modal attention (FIBER-style) predictor; online task.
- Training data: REACT 2024 (NoXi, RECOLA, UDIVA).

## Released code and weights
- Code: MIT.
- Weights: Google Drive folder `submission-checkpoint`: `react_predictor_epoch=91-step=9200.ckpt` 1.4 GB, `face_tokenizer_epoch=185-step=37200.ckpt` 316 MB, `external.zip` 409 MB (renderer and FaceVerse files), plus configs. About 2.1 GB in total. No separate weights license.

## Published metrics (README tables; REACT definitions, see react-challenge-baselines.md)
- Validation: FRC 0.26, FRD 86.73, FRDvs 0.1160, FRVar 0.0346, FRDiv 0.1162, FRRea 81.28, FRSyn 46.96 (README's "Mime ~ speaker lagged" row: FRC 0.37, FRD 84.78).
- Test: FRC 0.3190, FRD 82.0288, FRDvs 0.1165, FRVar 0.0344, FRDiv 0.1162, FRRea 34.6685, FRSyn 43.0918.
- On validation the README's own lagged-mime row beats it on FRC and FRD.

## Runs on this Mac as published?
- No. "developed and tested only with Python 3.10 in Ubuntu 22.04"; installs CUDA via conda and builds pytorch3d with `FORCE_CUDA=1`. A 1.4 GB predictor would fit in memory, but the environment is CUDA-only.

## Runnable on Seamless features as published?
- No. Needs raw speaker audio (wav2vec2) and FaceVerse 3DMM from video; outputs FaceVerse 3DMM and REACT 25-d attributes, not Seamless AUs.

## Verdict: not runnable (raw audio + FaceVerse 3DMM in, REACT representation out; CUDA-only)
