# Piper TTS (Open Home Foundation; piper1-gpl, successor to rhasspy/piper)

Sources read: github.com/OHF-Voice/piper1-gpl README, docs/LICENSING.md, docs/COMMERCIAL_USE.md, docs/API_PYTHON.md, docs/CLI.md; GitHub metadata for rhasspy/piper.

## Claims
- "A fast and local neural text-to-speech engine that embeds espeak-ng for phonemization." Used by Home Assistant and NVDA.
- Python, C/C++ (libpiper), HTTP server and CLI; voices are ONNX models downloaded per voice.

## Evidence
- Synthesis config (API_PYTHON.md): `volume`, `length_scale` ("2.0 twice as slow"), `noise_scale` ("more audio variation"), `noise_w_scale` ("more speaking variation"), `normalize_audio`. Streaming via `PiperVoice.synthesize()` chunks.
- No pitch control in the documented API.
- The old rhasspy/piper repo is archived (MIT); the active repo is GPL-3.0; last push 2026-11-23.
- LICENSING.md: the project "makes no license grant of its own over voice models". Each voice's MODEL_CARD names only its own dataset's license, and most voices are fine-tuned from another voice, so the whole chain matters. COMMERCIAL_USE.md notes many voices were "retrained in late 2026 to remove a lessac base from their chain".
- No CPU speed numbers in the docs read; not measured here.

## License (paper, code, model weights)
- Engine: GPL-3.0-or-later. Voices: per-voice, decided by the training-data chain; no grant from the project.

## Runs on this Mac without a GPU?
- Yes (CPU ONNX; CUDA is optional). Speed not stated in the sources read.

## Verdict: watch
- Local and streamable, but continuous control is limited to rate, volume and two noise scales; no pitch, so it cannot express the state dimensions `say` can.
- GPL-3 is fine for a local single-user tool, but voice licensing needs a per-voice chain audit.
- Choosing a voice is a voice-identity decision for the operator.

## Role in S2
- none now (candidate voice)
