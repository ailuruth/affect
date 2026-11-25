# aniface (Alysa Chan; npm aniface 0.4.0, Nov 2025 - Jan 2026)

Sources read: aniface 0.4.0 README (jsDelivr), npm metadata, GitHub metadata and file tree for alysachan830/aniface.

## Claims
- "Animate 3D avatars with real-time facial tracking using MediaPipe and Three.js": webcam -> MediaPipe Face Landmarker -> automatic mapping onto ARKit-compatible model blendshapes.
- Supports Ready Player Me, QuickRig and custom models; per-blendshape multipliers; option to pass your own Face Landmarker instance.

## Evidence
- Dependencies: `@mediapipe/tasks-vision ^0.10.0` (the telemetry-free 0.10.x line, see mediapipe-face-landmarker.md) and `three ^0.180.0`.
- Demo assets in repo: `demo/public/raccoon_head_small.glb`, `demo/public/rpm_avatar.glb`; the repo does not state the provenance or license of either asset.
- Created 2025-11-03, last push 2026-01-29, 13 stars.

## License (paper, code, model weights)
- Code: MIT. Demo GLBs: unstated. No paper.

## Runs on this Mac without a GPU?
- Yes in principle (MediaPipe on CPU WASM, about 13 ms per frame measured for the tracker; WebGL render). No numbers stated by the project.

## Verdict: reject
- It is face puppetry: the user's tracked face directly sets the avatar's face. That is exactly a partner-video-to-motion map, which by the item rule may never be the source of when or why the face moves, and it bypasses the affect pathway that Principle 3 requires mimicry to pass through.
- The useful part (MediaPipe blendshape -> GLB morph-target retargeting with per-shape gains) is a few dozen lines we can write against our own rig. The demo assets have no stated license.

## Role in S2
- none
