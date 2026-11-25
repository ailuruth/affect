# MediaPipe Face Landmarker with Blendshape V2 (Google; npm @mediapipe/tasks-vision)

Sources read: developers.google.com Face Landmarker guide; HF model card litert-community/MediaPipe-FaceLandmarker (README plus "Model Card Blendshape V2.pdf" and "Model Card MediaPipe Face Mesh V2.pdf"); @mediapipe/tasks-vision 0.10.35 and 1.2.3 package contents (README, vision.d.ts, vision_bundle.mjs).

## Claims
- Per face: 478 3D landmarks, 52 blendshape scores in [0, 1] (ARKit-style names), and a 4x4 transform from canonical face to the detected face (head pose).
- Blendshape V2: an MLP-Mixer on 146 landmarks, "optimized for real-time performance on a wide variety of mobile devices", intended for "controlling an avatar's face".

## Evidence
- `face_landmarker.task` is 3,758,596 bytes, FP16: BlazeFace detector (230 KB, 128x128 input), FaceMesh V2 (2.55 MB, 256x256 input), blendshapes (955 KB).
- Web API: `FilesetResolver.forVisionTasks(basePath)` and `modelAssetPath` or `modelAssetBuffer` accept local URLs or bytes; `delegate: "CPU" | "GPU"`; web running modes are IMAGE and VIDEO.
- Measured here (headless Chromium via Playwright, tasks-vision 0.10.35, CPU delegate/XNNPACK, 640x480 canvas, 300 frames, Apple M1 Pro): median 13.1 ms, p90 13.5 ms per `detectForVideo` call, with 52 blendshapes returned. No official latency numbers were found in the docs.
- Offline: with wasm and model served from localhost, Chromium made zero external requests on 0.10.35.
- Telemetry: tasks-vision 1.0.0 and later (I checked 1.0.0, 1.1.0, 1.2.0 and 1.2.3; 1.0.0 was published 2026-07-28) build a logger at task creation that POSTs usage stats (task type, running mode, OS, version, latency counters) to `https://odml.pa.googleapis.com/v1/log` every 60 s and on `close()`. I observed that request with 1.2.3. The 0.10.x builds checked (0.10.22-rc, 0.10.32, 0.10.34, 0.10.35) contain no such URL.
- Limits: faces turned more than 80 degrees, under 50% visible, or far away degrade; low light and noise cause blendshape "jittering".

## License (paper, code, model weights)
- Code (npm): Apache-2.0. Model bundle and model cards: Apache-2.0.

## Runs on this Mac without a GPU?
- Yes. About 13 ms per frame on CPU WASM, so a 30 Hz loop uses about 40% of one core. wasm is 11.2 MB (0.10.35) and the model 3.8 MB.

## Verdict: adopt (pinned to 0.10.35 with CSP `connect-src 'self'`)
- Outputs continuous geometry-derived coefficients with no emotion head (Principle 1). Runs locally, and nothing but features needs to leave the tab (Principle 7) once telemetry is excluded.
- The 52 output names match the ARKit rig convention, so mimicry can map perceived coefficients into the agent's own motor space without a learned translator (Principle 3).
- Keep left/right in subject coordinates (model card mirroring note).

## Role in S2
- perception
