# Py-Feat (Cheong, Jolly, Xie, Byrne, Kenney & Chang, "Py-Feat: Python Facial Expression Analysis Toolbox", Affective Science 2023; arXiv 2104.03509)

Source read: arXiv 2104.03509 PDF (the Affective Science revision manuscript, "FEAT_MS_AffSci_Revision"), AU sections, limitations and supplementary training details; github.com/cosanlab/py-feat README and LICENSES/PYFEAT-V1.md. I did not read the typeset journal version or run the code.

## Claims
- An open Python toolbox for face detection, landmarks, head pose, AUs and emotion categories, with analysis and plotting tools.

## Evidence
- AU models: HOG features from the landmark convex hull, PCA to 95% variance ("5,408 HOG features" to "1,195"), then per-AU linear SVM (Feat-SVM) or XGBoost (Feat-XGB). Trained on BP4D, BP4D+, DISFA, CK+, Shoulder Pain and others, "20 in total" AUs. The AU-to-landmark visualizer lists "AUs 1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18, 20, 23, 24, 25, 26, 28, 43".
- Output is presence probability, not intensity: Feat-XGB is the default "as it provides AU detection probability estimates rather than binary classifications."
- Validation (Table 6, F1 on DISFA+ for 12 AUs): Feat-XGB average .54 (AU1 .60, AU4 .64, AU6 .71, AU12 .78, AU15 .25, AU17 .26); OpenFace average .57 (AU12 .83, AU4 .69); FACET-iMotions .59.
- Speed: "a single image in about 400 milliseconds with a GPU and about 1.5 seconds on a CPU"; the authors "have not yet attempted to optimize our toolbox for speed".
- README (current): "Py-Feat runs on CPU, NVIDIA (CUDA) GPUs, and — since v0.7 — Apple Silicon GPUs via Metal (MPS)"; "the default is `cpu`"; requires Python 3.11+. The 2023 paper's models are now exposed as `Detectorv1`.

## License
- Code and docs: "MIT License, including commercial use".
- Weights: "Pretrained weights, third-party code, and research datasets have separate terms." PYFEAT-V1.md: "There is no single license covering every `Detectorv1` configuration"; img2pose is CC BY-NC 4.0; several weight grants are unresolved. Treat as research-only.

## Runs on this Mac without a GPU?
Yes for offline video, slowly: 1.5 s per frame on CPU in the paper (MPS supported now). A 10-minute 30 fps session is about 7.5 h on CPU at that rate unless frames are downsampled. Not usable live. Speed on this Mac unverified.

## Verdict: watch (human side only)
- Its default AU output is a presence probability with lower F1 than OpenFace on the same benchmark, so for continuous mimicry time series OpenFace's intensity output is the better instrument. Py-Feat is the MIT-code fallback and a cross-check.
- Its emotion-category head must not be used (classifier output, not a measurement of AUs). Never fed to the agent.
