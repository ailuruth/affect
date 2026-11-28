# F5-TTS and E2 TTS (SWivid / SJTU X-LANCE; v1 base model 2025-03-12)

Code: github.com/SWivid/F5-TTS (README read in full). MLX port: github.com/lucasnewman/f5-tts-mlx (listed in the README; not read).

**How fully read:** README only. Paper and model card not read.

## What it says
- Flow-matching diffusion transformer TTS. Inference takes `--ref_audio` and its transcript `--ref_text`: the voice is **cloned from a reference clip**. The README documents speed and inference-step settings; no pitch or energy input is documented.
- Licence: "code is released under MIT License. The pre-trained models are licensed under the CC-BY-NC license due to the training data Emilia, which is an in-the-wild dataset."
- Apple-silicon install instructions and an MLX implementation exist.

## What matters for this engine
- Identity comes only from a real person's recorded clip, so using it means cloning someone (consent; and, if the clip were the operator's, the agent copying him at the level of identity). Weights are non-commercial. Prosody controls are speed only.

## Verdict: reject
