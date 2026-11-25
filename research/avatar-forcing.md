# Avatar Forcing (Ki, Jang, Jo, Yoon, Hwang; arXiv 2601.00664, CVPR 2026)

Sources read: arXiv 2601.00664v2 full PDF (incl. appendix limitations); project page taekyungki.github.io/AvatarForcing; github.com/TaekyungKi/AvatarForcing README and LICENSE.md.

## Claims
- Real-time interactive head-avatar video from a portrait, conditioned on the user's audio and motion plus the avatar's audio, via causal diffusion forcing in a motion-latent space; latency about 500 ms, 6.8x faster than the baseline.
- A DPO variant that uses "synthetic losing samples constructed by dropping user conditions" to make reactions more expressive; preferred over 80% against the baseline in human evaluation.

## Evidence
- Motion latents come from a retrained motion auto-encoder (Ki et al.); audio features from Wav2Vec2.0; 10 NFEs Euler; blocks of 10 frames with 2 look-ahead frames.
- "All the experiments are conducted on a single NVIDIA H100 GPU." Trained on RealTalk and ViCo dyadic video.
- Fig. 1: "The avatar naturally mirrors the user's expression, such as smiling when the user smiles."
- Limitations (appendix): more explicit control, "such as directing eye gaze or emphasizing emotional shifts", is future work, possibly via "emotion-tracking inputs".
- README: install pins CUDA 11.8 torch; inference uses `CUDA_VISIBLE_DEVICES`; real-time conversation demo "not included".

## License (paper, code, model weights)
- Code: CC BY-NC 4.0 (LICENSE.md). Weights: downloaded via script or Google Drive; no separate license found, so assume the repo's CC BY-NC 4.0. Paper: arXiv.

## Runs on this Mac without a GPU?
- No. Reported on an H100; the code path is CUDA-only.

## Verdict: reject
- Under the item rule it could only be a rendering or motor layer, and it fails that too: it needs a datacenter GPU and outputs photoreal video (a non-goal).
- Its "mirroring" is learned co-occurrence from human video, the very thing the brief sets out to beat. Our mimicry must route perceived features through the agent's own motor and affect pathways (Principle 3), not a learned user-to-avatar mapping.
- The DPO trick of rewarding more reaction to the user leans toward the engagement optimization Principle 6 rules out.

## Role in S2
- none
