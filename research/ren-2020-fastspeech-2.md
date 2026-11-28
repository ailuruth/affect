# Ren et al. 2020, "FastSpeech 2: Fast and High-Quality End-to-End Text to Speech"

Ren, Y., Hu, C., Tan, X., Qin, T., Zhao, S., Zhao, Z. & Liu, T.-Y. (2020/2021). ICLR 2021. arXiv:2006.04558 (v8, 2022). https://arxiv.org/abs/2006.04558

**How fully read:** the arXiv PDF in full, including appendices A–E; reference list skimmed. Some table cells were lost in text extraction; the numbers below are from the prose or cells that survived.

## What it says
- Non-autoregressive TTS. A "variance adaptor" between encoder and mel decoder adds three explicit quantities: per-phoneme **duration** (from Montreal Forced Aligner, log domain, MSE), frame-level **pitch** (extracted with pyworld/WORLD, unvoiced frames interpolated, log, normalised per utterance, predicted as a 10-scale continuous-wavelet "pitch spectrogram" plus utterance mean and variance), and frame-level **energy** (L2 norm of each STFT frame). Pitch and energy are quantised to 256 bins and embedded. In training the ground-truth values are fed in; at inference the predictors' outputs are, or any values one chooses.
- Data: LJSpeech, one speaker, 24 h. MOS 3.83 ± 0.08 (FastSpeech 2 + Parallel WaveGAN) vs 3.70 Tacotron 2 and 4.30 ground truth. RTF about 0.02 on a V100.
- Ablation (CMOS): removing pitch −0.245, energy −0.040; predicting pitch directly instead of with the wavelet transform −0.185.
- Appendix E, "Variance control": a by-product is manual control of pitch, duration and energy; mel-spectrograms stay "high-quality" with F0 scaled from 0.75 to 1.50 times. Shown as figures and audio; no objective test of how exactly the output follows a commanded value, and none for energy or duration control.
- Licence and agreement section: the authors prohibit using the technology "to synthesize someone's speech without his/her consent". No official code or weights are released with the paper.

## What matters for this engine
- This is design (b) of new-core-search-11-synthesis.md: a TTS whose decoder takes F0, energy and duration as explicit inputs, so the engine could write F0 level, range, energy, rate and pauses directly and the decoder renders them naturally, without a vocoder pitch shift.
- Per-channel ceilings: the inputs are separate, so a ceiling on each commanded value is easy; whether the *output* obeys each one without crosstalk (for example perceived loudness moving with pitch, which co-vary in human speech) is not measured in the paper. A check after rendering (spec A9, ±1 %) stays necessary.
- The pitch path normalises per utterance and stores mean and variance separately, which maps onto the engine's F0 level and FR range.
- Kokoro-82M (kokoro-82m.md) is built on StyleTTS 2, whose decoder has the same kind of explicit F0 and energy inputs; that is the practical local form of this design.

## Verdict: adopt (the design pattern: explicit, separate F0, energy and duration inputs); no model to use from this paper itself
