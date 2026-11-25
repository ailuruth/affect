# Chatterbox TTS family (Resemble AI; Turbo, Nano, Multilingual V3)

Sources read: github.com/resemble-ai/chatterbox README; HF API metadata for ResembleAI/chatterbox, chatterbox-turbo, chatterbox-nano.

## Claims
- Zero-shot voice-cloning TTS: original 500M with "CFG & Exaggeration tuning"; Turbo 350M with paralinguistic tags (`[laugh]`, `[cough]`, `[chuckle]`) and a one-step decoder; Nano 110M with the same architecture, "running 3x faster than realtime on 8 CPU cores".
- Every output carries Resemble's PerTh watermark.

## Evidence
- README banner: "As of August 2026, Chatterbox is retired research and is no longer maintained"; the code stays public "as an archive".
- Original-model controls: `exaggeration` (default 0.5; "Higher exaggeration tends to speed up speech") and `cfg_weight` (pacing). Turbo and Nano list tags, not exaggeration.
- Device examples: `"cuda"`, `"cpu"` or `"mps"`; Nano "also runs on CPU".
- No pitch or energy parameter is documented.

## License (paper, code, model weights)
- Code: MIT. Weights (chatterbox, -turbo, -nano on HF): MIT. No paper read.

## Runs on this Mac without a GPU?
- Nano is stated to run at 3x real time on 8 CPU cores (not on Apple silicon specifically; not measured here).

## Verdict: reject
- Unmaintained since August 2026.
- Its expressive controls are an "exaggeration" intensity scalar and discrete paralinguistic tags, closer to emotion presets than to continuous prosody (Principle 2). The motor pathway could not set pitch or energy directly.
- Voice comes from a reference clip, so using it means choosing or cloning an identity, which is an operator decision and a consent question.

## Role in S2
- none
