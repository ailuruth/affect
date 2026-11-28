# Wang et al. 2018, "Style Tokens: Unsupervised Style Modeling, Control and Transfer in End-to-End Speech Synthesis" (GST)

Wang, Y., Stanton, D., Zhang, Y., Skerry-Ryan, RJ, Battenberg, E., Shor, J., Xiao, Y., Ren, F., Jia, Y. & Saurous, R. A. (2018). Proc. ICML 2018. arXiv:1803.09017. https://arxiv.org/abs/1803.09017

**How fully read:** the arXiv PDF (v1) in full except the reference list. Figures were read from their captions and the prose; the spectrogram panels did not survive text extraction. The audio demos were not listened to.

## What it says
- A reference encoder (6 strided 2-D conv layers and a 128-unit GRU over a log-mel spectrogram) gives a reference embedding. It is the query of an attention over a bank of 10 randomly initialised 256-d "style tokens" (tanh, then softmax weights; multi-head works better). The weighted sum, the style embedding, is added to every text-encoder state of Tacotron. Trained only by Tacotron's reconstruction loss: no prosody or emotion labels.
- At inference: condition on one token (optionally scaled), on hand-set or random softmax weights, or on a reference clip (style transfer).
- Training data for the style experiments: 147 h of one audiobook narrator "in an animated and emotive storytelling style".
- What tokens turned out to be: found by listening. One "lower-pitch voice", one "decreasing pitch", one "faster speaking rate", one "animated" (more pitch variation). The authors state that "not all tokens capture single attributes": others "learn a mixture of attributes that reflect stylistic co-occurrence in the training data (a low-pitched token, for example, can also encode a slower speaking rate)". Scaling a token intensifies it; negative scales give the reverse ("fast to slow or animated to calm"), "never seen during training"; large scales can make speech unintelligible.
- On noisy found data, tokens absorb noise types (music, reverberation) and, on 439-speaker TED data with 1024 tokens, speakers. Style embeddings classify noise vs clean at 99.2 % and TED speakers at 75.0 % (i-vectors 73.4 %) with LDA.
- Side-by-side preference over a Tacotron baseline for long-form audiobook synthesis, p = 0.0038 to 0.0552 depending on reference and scale.
- The authors propose GST weights as a way to "automatically generate style annotations", naming emotion as an example attribute.

## What matters for this engine
- The tokens are unsupervised, but their meaning is the corpus's: they are the main modes of one actor's expressive narration. Driving a voice from them imports the surface statistics of human expressive speech, in the bundles in which they co-occur in that corpus. In use they are named after the fact ("animated", "calm"), which makes them label-like controls.
- They mix channels by construction (the paper's own words above). A ceiling on a token weight is not a ceiling on F0 level, F0 range, loudness or rate separately, so the per-channel ceilings c_k (spec §1.1, rows 14–19) cannot be enforced on them; one token weight moving pitch and rate together is the single quantity Q18 excludes.
- Reference-audio mode is prosody copying. Fed the operator's speech, it would make the agent's voice copy his; it would also need his audio, not features (Principle 7).

## Verdict: reject (for driving the voice channels)
Useful as an explanation of why style latents mix channels. Not to be used below Claude.
