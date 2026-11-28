# Nie, Ji, Xing et al. 2026, "WordVoice: Explicit and Decoupled Multi-Dimensional Word-Level Control for LLM-Based TTS"

arXiv:2607.06461 (2026-07-07). https://arxiv.org/abs/2607.06461

**How fully read:** abstract only (arXiv listing). Paper, code and licence not read.

## What it says (abstract)
- An LLM-based, zero-shot TTS with explicit word-level control of five attributes (duration, boundary, energy, pitch, tone), trained on WordVoice-5A, a 4.7k-hour bilingual corpus annotated with those attributes; a bound-token "acoustic planning" step allows manual intervention, and a modulation module aligns word-level attributes in the waveform stage. Claims "decoupled control over multiple acoustic dimensions".

## What matters for this engine
- If the controls are continuous and the weights open, this is a recent instance of design (b) at word resolution. Unknown from the abstract: whether the attributes are continuous or binned, the licence, whether identity requires a cloned clip, and speed on Apple silicon.

## Verdict: watch (read the paper before any use)
