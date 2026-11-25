# TalkingHead (3D) (Mika Suominen; github.com/met4citizen/TalkingHead, 2023-2026)

Sources read: README (full: options, API table, avatar requirements, asset licenses, FAQ), LICENSE, repo tree.

## Claims
- A JavaScript class for real-time lip-sync on full-body three.js avatars with a Mixamo-compatible rig plus 52 ARKit blendshapes and 15 Oculus visemes.

## Evidence
- Default speech path is Google Cloud TTS (`ttsEndpoint`, `ttsApikey`); `speakAudio()` accepts local audio with word timings (or visemes) instead, and can carry an `anim` template that drives our own blendshape data in sync with playback.
- Built-in autonomous behavior: `avatarMood` presets ("neutral", "happy", "angry", "sad", "fear", "disgust", "love", "sleep"), `makeEyeContact`, `lookAtCamera`, gestures, emoji-driven expressions, and `startListening(analyser)` state changes.
- Bundled avatars and licenses: `mpfb.glb` (made with Blender + MPFB, CC0, 36.8 MB); `brunette.glb` (Ready Player Me, CC BY-NC 4.0); `avatar.glb` (Avaturn), `avatarsdk.glb`, `vroid.glb` (non-commercial).
- README also points to Microsoft RocketBox characters (MIT, with ARKit + Oculus shapes; need re-rigging).
- Example import map pulls three 0.186 from jsDelivr (would need local copies offline). Last push 2026-11-04, 1,703 stars.

## License (paper, code, model weights)
- Code: MIT ("Copyright (c) 2023-2024 Mika Suominen"). Assets: per file, as above. three.js: MIT.

## Runs on this Mac without a GPU?
- Yes in principle (WebGL on the integrated GPU). No frame-rate numbers are stated.

## Verdict: watch (use the CC0 ARKit-52 rig convention and asset, not the class)
- The class decides when the face moves (moods, eye contact, listening reactions, emoji presets). That conflicts with Principle 2 and the Body rule ("never by emotion presets"), and its default TTS is a cloud service.
- `mpfb.glb` is the only permissively licensed (CC0) ARKit-52 + viseme rig found. Its morph names equal MediaPipe's blendshape names, which suits identity-basis mimicry.
- It is a realistic human, so using it is a look decision the operator must approve first (Principle 8). A grey, untextured render is the closest neutral option.

## Role in S2
- rendering (asset and rig convention only)
