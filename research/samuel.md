# vvolhejn/samuel: neural controller for the Pink Trombone vocal tract

Václav Volhejn, GitHub `vvolhejn/samuel` (last pushed 2026-11-22), plus the blog post "Samuel" (2026-08-17). I read the README, `deploy/model-card.md`, `configs/model.yaml`, `configs/config.yaml`, `src/samuel/model.py`, `src/samuel/ssl_loss.py`, the device handling in `src/samuel/server.py`, and `tests/test_causality.py`.

## Claims
- A causal 1D-CNN controller (SEANet-style encoder, 3.4M parameters according to the blog) listens to speech. It emits Pink Trombone articulator trajectories at about 86 Hz: voiceness, intensity, tongue index and diameter, constriction index and diameter, and lip diameter. Pitch comes from pYIN, not from the model. The physical synthesizer then "parrots" the input.
- **Analysis by synthesis.** The pipeline is controller → differentiable Pink Trombone (FIR approximation of the Kelly–Lochbaum tract) → resample → **frozen** self-supervised speech encoder (wav2vec2-base-960h, layer 6, in the default config) → L1 against the same features of the target. The `ssl_loss.py` docstring says the encoder is "frozen and kept in eval mode: gradients flow *through* it into the audio, never into its weights."
- The config comment says the perceptual loss "is what makes the controller intelligible, MFCC alone is not enough". Smoothness, acceleration and rest-pose penalties keep motion plausible.
- Causality is verified by gradient: `test_causality.py` checks that each control frame depends only on past samples.

## Evidence
- The blog reports Whisper WER 1.0 with MFCC loss only, about 0.3 with an early perceptual loss, and 0.20 for the final Gumbel-bucket head (0.24 for a direct tanh head).
- Training used 1000 h of Libri-Light. The final model took 18 h on one H100, and all experiments together about 900 GPU-hours.
- Known articulatory errors: plosives without full closure, /n/ without nasal use, and /ɔ/ produced without lip rounding.
- No human listening study is reported.

## License
- Code: GPL-3.0. Copyleft applies if we link or ship it.
- `pocket-tts/`: MIT (Kyutai).
- Model card: gpl-3.0.
- Data: Libri-Light (MIT), built from public-domain LibriVox audio.

## Runs on this Mac without a GPU?
- Inference: yes. `server.py` falls back to CPU, and the blog states it is causal and real-time on a CPU with an 11.6 ms delay. I did not run it here.
- Training: no. It needs a GPU at this scale.

## Verdict: watch
It is a perception-to-motor mapping that parrots its partner, so under the brief it can only ever be a **motor/rendering layer** (S2 voice). It must never be the source of when or why the Bot vocalizes. The method is what matters to us. It learns an inverse model of the agent's **own body** by passing its own output through a fixed perceptual front end and comparing that with the partner's percept. That is a concrete, working instance of Principle 3 ("others are read through the agent's own body"). The GPL licence and the speech-only scope keep it at watch, not adopt.

## What it gives S1
- Nothing runs in S1, which is text only. Design lessons carry forward:
  - **Template for the S2 face.** Planned chain: AU controller → placeholder face renderer → the same frozen local face-feature extractor used on the webcam (blendshapes) → loss against the user's features. That gives a learned inverse model $o \to a$ in the Bot's own motor space. Mimicry and inferring a partner's state by inverting the Bot's own mapping (Yoshida and Man) can then share one model.
  - **Keep the perceptual front end frozen and identical for self and other.** Then "how I look" and "how you look" live in one feature space. This is the precondition for self/other comparison without labels (Principle 1).
  - **Keep $h_t$ out of the controller's target.** Samuel shows a mimicry layer works without any internal state. The brief's S2 claim is the contrast: with the emotional pathway removed, only voluntary or mimicry motion should remain.
