# Parler-TTS (Hugging Face; Lacombe, Srivastav & Gandhi 2024), after Lyth & King 2024

Code: github.com/huggingface/parler-tts. Annotation pipeline: github.com/huggingface/dataspeech. Paper reproduced: Lyth & King 2024, arXiv:2402.01912 (not read).

**How fully read:** both READMEs in full and the LICENSE header of parler-tts. Model cards on Hugging Face not reachable from this session; the paper not read.

## What it says
- Speech is conditioned on a free-text **description** of the voice and delivery ("A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch..."). Checkpoints (Aug 2024): Mini 880M and Large 2.3B parameters, trained on 45k hours of audiobook data. 34 named speakers for consistency.
- The descriptions are built by Data-Speech: continuous measures (speaking rate, SNR, reverberation, utterance pitch mean and std, monotony) are **mapped to categorical bins and then to keywords**, e.g. 7 rate bins from "very slowly" to "very fast"; a speaker's pitch keyword is computed relative to speakers of the same gender. Gender and speaker id columns are required.
- Apple silicon needs a nightly PyTorch for bfloat16 (README). Code and weights stated as permissively licensed (code Apache-2.0).

## What matters for this engine
- The controls are words over quantised bins, encoded by a text encoder, plus whatever else the text says ("expressive", "animated"). That is label-like control in the sense of Principles 1 and 2, and one sentence moves every channel at once, so per-channel ceilings cannot be set. Large autoregressive models also strain the latency budget.

## Verdict: reject (label-like, word-binned controls)
