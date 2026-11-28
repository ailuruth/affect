# Skerry-Ryan et al. 2018, "Towards End-to-End Prosody Transfer for Expressive Speech Synthesis with Tacotron"

Skerry-Ryan, RJ, Battenberg, E., Xiao, Y., Wang, Y., Stanton, D., Shor, J., Weiss, R. J., Clark, R. & Saurous, R. A. (2018). Proc. ICML 2018. arXiv:1803.09047. https://arxiv.org/abs/1803.09047

**How fully read:** the arXiv PDF (v1) in full except the reference list. Table 1 was read from the layout extraction. Audio demos not listened to.

## What it says
- "Subtractive" definition: prosody is the variation left after phonetics, speaker identity and channel are accounted for.
- A reference encoder (6 conv layers, 128-unit GRU, then a projection with tanh; 128-d works best) compresses a reference spectrogram into a fixed-length prosody embedding, concatenated to the text encodings with a speaker embedding. It is trained only by reconstruction; the bottleneck has to be narrow enough that the model cannot just copy the input.
- Results (Table 1): MCD13 and F0 frame error fall against the baseline in every condition, e.g. single speaker, same-speaker reference: MCD13 10.63 → 7.92, FFE 53.2 % → 28.1 %; subjective "closer to the reference" +1.611 ± 0.164 on a −3..3 scale. With an unseen speaker in the multi-speaker model: FFE 60.0 % → 41.3 %, +1.146 ± 0.246.
- Transfer is **pitch-absolute**: female targets driven by male references "sound as if they're imitating a person with a deeper voice". A speaker-ID model labelled the outputs as the *reference* speaker in 61 % of cases and the target in 21 % (MFCC-based ID: 41 % vs 32 %). Prosody and identity are entangled. Larger bottlenecks copy more of the reference.
- Variable-length (per-frame) embeddings carry a stronger timing signal and are less robust to text and speaker changes.

## What matters for this engine
- This is the cleanest statement of what a learned prosody latent does: it copies a reference's prosody, finely time-aligned, including some of the reference speaker's identity. Driven by the operator's voice, it would be mirroring at the level of the whole contour, with no per-channel ceilings and a leak of his identity into the agent's voice.
- Its definition of prosody (what remains after text and speaker) is the right one for the engine's six phrase channels; the engine sets those as explicit numbers instead of as a learned embedding.

## Verdict: reject
Background for why prosody transfer is copying by design.
