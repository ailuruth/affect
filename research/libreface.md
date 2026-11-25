# LibreFace and LibreFace 2.0 (Chang et al., WACV 2024; Guan et al., FG 2026)

Sources read: github.com/ihp-lab/LibreFace README and LICENSE.rst, repo tree. I did not read the papers themselves.

## Claims
- An open toolkit for real-time facial expression analysis with CPU-only and GPU versions: AU detection, AU intensity, facial expression recognition and (2.0) gaze, from ResNet-18 and RepVGG students distilled from pretrained encoders.
- 2.0 adds 240,000+ synthetic frames (Stable Diffusion 3.5 identities driven with LivePortrait) to improve fairness on RAF-AU and AffWild2.

## Evidence
- AU intensity is reported as average PCC over the 12 DISFA AUs, against OpenFace 2.0 and others (README figure; values only in images).
- Python API: `libreface.get_facial_attributes(path, device="cpu" | "cuda:0")`, batch size 256 by default; weights auto-download.
- ONNX weights ship inside a .NET NuGet package (OpenSense); the console app is "Windows and CUDA is mandatory". No browser build.
- The repo has a `Facial_Expression_Recognition` module alongside `AU_Detection` and `AU_Recognition`.

## License (paper, code, model weights)
- Code: USC Research License, free for "educational, research and non-profit purposes"; commercial use needs USC Stevens. The weights are distributed with the code; I found no separate weights license.

## Runs on this Mac without a GPU?
- The Python path supports CPU, but no CPU frame rate is stated. Not in-browser without porting the ONNX models to onnxruntime-web.

## Verdict: watch
- It gives true FACS AU intensities, which MediaPipe's ARKit blendshapes do not, so it is the obvious offline cross-check for any blendshape-to-AU mapping.
- For the live loop it loses to MediaPipe: Python or .NET rather than browser, a noncommercial license, and only 12 AUs.
- If used, call only the AU heads; the expression-recognition head is an emotion classifier and is barred by Principle 1.

## Role in S2
- none (offline validation of perception features)
