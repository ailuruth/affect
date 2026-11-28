# Kokoro-82M TTS (hexgrad; v1.0 Jan 2025) and kokoro-js

Sources read: github.com/hexgrad/kokoro README; HF model card hexgrad/Kokoro-82M; kokoro-js 1.2.1 README (unpkg) and npm metadata.

## Claims
- An 82M-parameter open-weight TTS "comparable quality to larger models while being significantly faster"; v1.0 has 8 languages and 54 voices.
- Trained "exclusively on permissive/non-copyrighted audio data", a few hundred hours, about $1000 of A100 time.
- kokoro-js runs "100% locally in the browser" via Transformers.js (`device: "wasm" | "webgpu"`, or `"cpu"` in Node; dtypes fp32, fp16, q8, q4, q4f16).

## Evidence
- Synthesis controls in the API: `voice` (a named voice or a voice tensor) and `speed`. There is no pitch or energy parameter in either README.
- Apple-silicon note in the Python README: `PYTORCH_ENABLE_MPS_FALLBACK=1` for GPU acceleration.
- Measured here (Node 24, kokoro-js 1.2.1, `onnx-community/Kokoro-82M-v1.0-ONNX` q8, `device: "cpu"`, M1 Pro; weights cached in the scratchpad, ~97 MB): first load 19.6 s; one 4.5 s sentence took 2.5-2.9 s (real-time factor 0.55-0.65); `speed` 0.8 and 1.25 changed duration to 5.47 s and 3.90 s.

## License (paper, code, model weights)
- Code (kokoro and kokoro-js): Apache-2.0. Weights: Apache-2.0 (model card). Some CC BY training audio is credited in the card.

## Runs on this Mac without a GPU?
- Yes. Real-time factor about 0.6 on CPU (measured), but a whole sentence must be synthesized before playback (~2.5 s here), unless it is streamed in smaller chunks.

## Verdict: watch
- License and quality fit, but the only continuous prosody control is speed. Pitch base, range and energy, which the motor pathway needs to express state, are missing, so it would carry identity, not affect.
- Voice choice (and any voice-tensor blend) is a voice-identity decision for the operator.
- Revisit if S2 shows `say` voices are too poor, and pair it with a post-hoc pitch shift if so.

## Role in S2
- none now (candidate voice)

## Update (2026-11-28)
- **State:** no new weights; the inference library's last commits are from 2025-08-06 (Python 3.13 support, a voice-loading fix), after MPS support (2025-04-10) and batch/ONNX work (2025-07-26), read from the GitHub commit list. The Hugging Face model card could not be re-read (huggingface.co is outside this session's network).
- **New finding from the code (github.com/hexgrad/kokoro, `kokoro/model.py`, read in full):** Kokoro is the StyleTTS 2 architecture (li-2023-styletts-2.md) without style diffusion at inference. `forward_with_tokens` computes per-phoneme durations `pred_dur` (divided by `speed`), then explicit frame-level pitch and energy curves `F0_pred, N_pred = self.predictor.F0Ntrain(en, s)`, and passes them to the decoder: `self.decoder(asr, F0_pred, N_pred, ref_s[:, :128])`. The voice is a fixed 256-d tensor per phoneme count (`pack[len(ps)-1]`); its first half conditions the decoder (timbre), its second half the duration and prosody predictors. Comma-separated voices are averaged (`torch.mean` in `load_voice`), so a blended voice not tied to one recorded speaker is possible.
- **Consequence:** the public API offers only `speed`, but a few lines in the engine's own call could replace `F0_pred`, `N_pred` and `pred_dur` with the engine's contour, loudness and durations before the decoder (design (b) in new-core-search-11-synthesis.md). Untested: how faithfully the decoder follows edited curves, and whether pitch edits move loudness. The verdict changes from **watch** to **adopt as the recommended Q1 candidate (fixed voice + WORLD resynthesis now; the internal-curve path as an M5 option)**; the voice remains the operator's choice.
