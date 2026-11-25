# MIMo: Multimodal Infant Model (Mattern et al., IEEE TCDS 2024; MIMo-v2, ICDL 2025)

Sources read: github.com/trieschlab/MIMo README (branch v2/main) and repo tree; mimo.readthedocs.io landing page; arXiv 2312.04318 full text.

## Claims
- A Gymnasium + MuJoCo infant body (18-month-old proportions, five-fingered hands) with simulated vision, touch (full-body virtual skin), proprioception and vestibular input.
- Two swappable actuation models: spring-damper torque motors and a muscle model with two antagonist muscles per joint and adjustable compliance.
- MIMo-v2 adds body growth, developing visual acuity and sensorimotor delays (README citation list).

## Evidence
- Paper Sec. on face: "MIMo can also change his facial expression. This is implemented by changing the texture of the head ... six extra textures, corresponding to the six basic emotions ... These can be used to convey an internal emotional state."
- Eyes have 6 DoF; demo tasks (reach, standup, selfbody, catch) are RL with stable-baselines3.
- Benchmark: default config (256x256 vision) needs 0.69 real s per simulated s, "1.44 times faster than real time", on an AMD FX-8350, 16 GB RAM, GTX 1070, 5 ms physics steps.

## License (paper, code, model weights)
- Code: MIT (LICENSE, README). Paper: IEEE journal; arXiv preprint. No learned weights shipped.

## Runs on this Mac without a GPU?
- Probably yes for the body (MuJoCo is CPU), but no Apple-silicon numbers are stated. Vision rendering cost was measured with a GPU present.

## Verdict: reject (for S2)
- The face is six basic-emotion texture swaps, which is exactly the "emotion preset" output the brief forbids (Body component: "never by emotion presets"; Principle 2).
- No face muscles or AUs, so nothing to drive from the S2 AU interface.
- The body/touch simulator is MIT and theory-friendly (developmental robotics), so it could return as a separate body testbed after S3, but it is not an S2 component.

## Role in S2
- none
