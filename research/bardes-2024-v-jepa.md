# Revisiting feature prediction for learning visual representations from video, V-JEPA (Bardes, Garrido, Ponce, Chen, Rabbat, LeCun, Assran & Ballas)

Citation: A. Bardes, Q. Garrido, J. Ponce, X. Chen, M. Rabbat, Y. LeCun, M. Assran, N. Ballas. "Revisiting Feature Prediction for Learning Visual Representations from Video." arXiv:2404.08471 (2024).

Source read: arXiv PDF, text-extracted. Read in full: §1–7 (related work, method and its collapse argument, data and evaluation, the four ablations, comparison with pixel-prediction methods and with state of the art, label efficiency, qualitative decoding, conclusion). **Not read:** appendices (masking-size ablation, attentive-probe details for baselines, training details).

Intended companion: LeCun 2022, "A Path Towards Autonomous Machine Intelligence" (the JEPA position paper). **Not reachable:** openreview.net does not resolve from this session and no arXiv version exists. Nothing below rests on it; the JEPA idea is taken from this paper's own statement of it.

## Key claims, with numbers
- **Objective** (Eq. 1): minimise ‖P_ϕ(E_θ(x), Δ_y) − sg(Ē_θ(y))‖₁, where x and y are masked regions of the same clip, Δ_y the positions to predict, Ē an exponential moving average of the encoder. No reconstruction, no negatives, no text, no pretrained image encoder.
- **Why it does not collapse (adapted from BYOL):** with an optimal ℓ1 predictor P* = median(Y | E(x)), the encoder gradient is ∇_θ MAD(Y | E_θ(x)); "the encoder must learn to capture as much information about the video as possible to minimize the deviation of the target", assuming the EMA keeps the predictor near-optimal (a hypothesis, stated as such).
- **Masks:** multi-block, union of 8 blocks covering 15 % (short range) or 2 blocks covering 70 % (long range) per frame, repeated across time; about 90 % masked on average.
- **Ablations (ViT-L/16, frozen attentive probe):**
  - feature vs pixel targets: K400 73.7 vs 68.6; SSv2 66.2 vs 66.0; IN1K 74.8 vs 73.3;
  - **what is predicted from what matters most:** random-tube[0.9] gives K400 51.5 / SSv2 46.4 / IN1K 55.6; causal multi-block[6] (predict later frames from the first 6) 61.3 / 49.8 / 66.9; causal[12] 71.9 / 63.6 / 72.2; full multi-block 72.9 / 67.4 / 72.8;
  - attentive vs average pooling: +17.3 (K400), +16.1 (SSv2): the representation is not linearly separable by default.
- **Results:** ViT-H/16 at 384 px: K400 81.9, SSv2 72.2, IN1K 77.4 frozen; +21 points over image models on SSv2 (motion). With 10× fewer labels on K400, V-JEPA drops 12 % (to 68.2) against 30 % for VideoMAEv2.
- **Data:** 2 M videos; best average with the largest mix, but best per-task scores with task-matched pretraining data.

## What it means for the engine
1. **"What to predict from what" is the design variable.** The largest effect in the paper is the masking scheme, not the architecture. For the engine, the analogue is which streams are targets and which are only context. A JEPA whose **targets are only the agent's own future body and own motor channels**, with the partner's face, voice and words admitted only as context x, learns partner features only insofar as they predict the agent's own future. That is the object of Candidate 1 in the pass-7 synthesis.
2. **Causal prediction is weaker than bidirectional masking** (61.3 vs 72.9 on K400 for causal[6]). An online agent must predict forward; replay can use bidirectional masks. That fixes a split: forward own-body prediction online, masked bidirectional prediction in nightly replay.
3. **Feature targets drop unpredictable detail** (the authors' motivation, not measured directly). For a face stream this suggests session nuisance (lighting, pose) is cheaper to drop than in reconstruction models, which bears on pass 6's nuisance problem; untested.
4. **No action, no reward:** a pure past-term objective (in APD's sense). It cannot open the approval route by itself.

## Verdict
- **adopt (as method: target/context typing by masking; EMA-target feature prediction), reject as core.** It is a representation objective; it says nothing about affect, body or action.
