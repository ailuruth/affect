# Li et al. 2023, "StyleTTS 2: Towards Human-Level Text-to-Speech through Style Diffusion and Adversarial Training with Large Speech Language Models"

Li, Y. A., Han, C., Raghavan, V. S., Mischler, G. & Mesgarani, N. (2023). NeurIPS 2023. arXiv:2306.07691 (v2). https://arxiv.org/abs/2306.07691. Code: github.com/yl4579/StyleTTS2 (README and LICENSE read).

**How fully read:** main text in full; appendices A (feedback, expressiveness, ablation), B.3–B.4 (long-form, style transfer) and D (SLM discriminator) read; appendices C, E, F, G skimmed for the decoder inputs only. Figures from captions. Demos not listened to. The pretrained checkpoints on Hugging Face were not reachable from this session (huggingface.co is outside its network).

## What it says
- Speech is modelled as p(x|t) = ∫ p(x|t, s) p(s|t) ds with a fixed-length **style vector** s = [s_p, s_a] (prosodic and acoustic halves), "any characteristic in speech beyond phonetic content ... including but not limited to prosody, lexical stress, formant transitions, and speaking rate". s is sampled from text by a small diffusion model (3–5 steps), or taken from a reference clip's style encoder.
- The decoder generates the waveform from aligned phoneme features, s, and **explicit pitch and energy curves**: x̂ = G(h_algn, s, p_x, n_x). In training p_x comes from a pitch extractor and n_x is the energy of the recording; at inference they come from a prosody predictor P(h_bert, s_p), and durations from a duration predictor S.
- Quality: CMOS +0.28 over the LJSpeech recordings (p = 0.021), −0.02 against VCTK recordings; MOS 3.83 on LJSpeech. RTF 0.0185 on a GPU.
- Emotion: style vectors sampled from 500 GPT-4-written sentences "across five emotions" cluster by emotion in t-SNE, and mean F0 and energy separate by text emotion (Fig. 2, App. A.2): "expressive speech in varied emotions without explicit emotion labels during training". Style vectors control "pauses, emotions, speaking rates, and sound quality" (App. A.3). Style vectors are approximately convex: interpolation gives intermediate styles (App. B.3).
- Zero-shot cloning from a 3-s clip (LibriTTS model). The authors' conditions of use require telling listeners the speech is synthetic unless the voice's speaker has given permission to be cloned.
- Licence: code MIT; pretrained models under those conditions of use; inference "depends on a GPL-licensed package" (the phonemizer).

## What matters for this engine
- Two different things live in one model. (1) The style vector: a single learned latent that moves pitch, energy, pauses, rate and voice quality together, organised by the emotional content of the text. Driving it from the agent's state would be design (c): human expressive statistics, mixed channels, no per-channel ceilings. Rejected. (2) The decoder's explicit F0 and energy inputs and the explicit per-phoneme durations: these are design (b), the separate channels the engine needs.
- The text-to-style route is a second, unledgered route from Claude's words to the voice (sentiment of the words → F0 and energy). The spec's innate templates "chosen by the text's question form only" avoid it; any StyleTTS 2-family model must be run with a fixed style vector and the engine's own contour, not the predictor's.
- The LJSpeech checkpoint is one real person's voice (a public-domain audiobook reader); the LibriTTS model is built to clone. Both are voice-identity decisions for the operator.

## Verdict: watch (the architecture, through Kokoro); reject style diffusion and cloning for this engine
