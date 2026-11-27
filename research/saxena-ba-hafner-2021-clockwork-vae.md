# Clockwork Variational Autoencoders (Saxena, Ba & Hafner)

Citation: V. Saxena, J. Ba, D. Hafner. "Clockwork Variational Autoencoders." arXiv:2102.09532v2 (2021). Published at NeurIPS 2021.

Source read: the arXiv PDF, text-extracted, main text read in full; appendices A (RSSM background), B (related work), C (architecture) and D (hyperparameters) read; the sample-gallery appendices (E–G figures) not inspected. Figure values were read from the text where the text states them; the per-dataset Table 1 cells did not extract cleanly and are not quoted.

Intended companion: Gumbsch, Sajid, Martius & Butz 2024 (THICK, ICLR), the adaptive-time-scale hierarchical world model. **Not reachable**: proceedings.iclr.cc does not resolve from this environment and openreview.net returned 403 for the PDF; no arXiv version was found. Nothing below rests on it.

## What the paper does
- **Model.** A hierarchy of L recurrent latent chains on top of an RSSM (deterministic GRU state h plus diagonal-Gaussian stochastic state z per level). Level l is active only at steps t with t mod k^{l−1} = 1, so it ticks k times slower than the level below and otherwise copies its last state. Each active state at level l conditions the k states of level l − 1 below it:
  - prior p(s^l_t | s^l_{t−1}, s^{l+1}_t);
  - posterior q(s^l_t | s^l_{t−1}, s^{l+1}_t, e^l_t), where e^l_t embeds the k^{l−1} frames under that tick;
  - decoder p(x_t | s^1_t) from the lowest level only.
- **Objective.** ELBO: reconstruction at the lowest level minus the KL[q‖p] at every level, **summed over that level's active steps only**.
- **Why slow content moves up (the paper's argument).** The KL limits how much information enters from the encoder. A higher level pays KL once per tick, a lower level once per frame. Information that persists is cheaper to store once high up than to re-extract or carry along at the lower level.
- **Results (from the text).**
  - On 4 datasets (MineRL Navigate, KTH, GQN Mazes, Moving MNIST) CW-VAE has the best mean rank over SSIM, PSNR, LPIPS and FVD against SVG-LP, VTA, RSSM and an ablation with all levels at the fastest rate (NoTmpAbs). The gain from temporal abstraction is larger than the gain from hierarchical latents alone.
  - MineRL: accurate predictions for over 400 frames; prior work fails before or around 150. Moving MNIST: digit identities kept for 1000 frames, about 6× as long as baselines before reaching the "random" line. Larger abstraction factors (2, 4, 6, 8) keep predictions accurate for longer at equal parameter count.
  - **What the top level stores** (GQN Mazes, top level sampled from its prior while lower levels see context): camera position and nearby walls stay correct, **wall and floor textures are randomised**. The top level holds per-episode global appearance; motion and position live lower down.
  - **KL per level (Table 2, nats summed over a sequence):** 4-level 397.10 / 41.20 / 2.66 / 0.0001; 3-level 366.70 / 45.28 / 6.29; 2-level 389.40 / 39.18; 1-level 440.50. Higher levels store little; adding levels takes information off the lowest level.
  - **Adapting to speed** (Moving MNIST at 3 %–300 % speed): faster digits raise lowest-level KL and lower the upper levels'; slower digits do the reverse. The top level stores about 5 nats, about what the two digit identities need.
- **Limits stated.** Trained on 100-frame sequences (with 3 levels and factor 8 the top level ticks once per sequence); small encoders; metrics poor for long horizons.
- **Size.** 20-dimensional stochastic and 200-dimensional deterministic state per level (100 and 800 on MineRL); 2.5 days on one Titan Xp.

## The mathematical object
**A hierarchical state-space VAE whose level l transitions on the clock k^{l−1} and whose KL is charged per transition: the information placed at each level is priced by how often that level ticks, so persistence of a factor in the data decides its level.**

## What it means for the engine
1. **A derived reason slow latents hold slow content.** The rate-priced KL gives a variational argument for where information goes, not only a leak constant. For an engine latent trained by prediction on the agent's own body, the partner's movement and words, slow levels would hold whatever is constant over their tick: this is the closest thing read so far to "mood and temperament emerge as levels".
2. **The concrete danger: the top level stores nuisance.** In GQN Mazes the slowest level stored textures, the per-episode constants. In a living engine the per-session constants are lighting, camera pose, microphone gain, sensor placement and the person's identity. Trained on raw feature streams, the slowest levels would encode "which session, which room", not anything affective, unless those factors are removed upstream or given their own variables. The physiological SSL papers read in this pass show the same failure from the other side (sarkar-etemad-2020-self-supervised-ecg.md: subject-independent performance poor).
3. **Information content per level is measurable.** The level KL is a label-free, built-in read-out of how much each time scale holds. That gives an internal-state measurement (brief: judged on internal state) for a claim such as "a temperament level exists and holds k nats about the person"; ablating a level is a lesion with a predicted KL shift to the level below.
4. **Order, not magnitude, again.** k sets the tick. Durations from reflex to temperament still require choosing k and L, so the five-pass lesson stands.
5. **Q18.** Nothing here touches the per-expression ceilings: the decoder is the lowest level and every route to expression still passes the output-side caps. But a slow level that stores the partner's persistent face (as earlier designs' slow states did: r ≈ 0.9 on one-minute means) is "knowing" (D81), allowed only because the ceilings bound expression.

## Verdict
- **adopt (the rate-priced KL as the reason for, and measurement of, slow levels); reject as a core.** It is a known world-model family (RSSM plus fixed clocks: Clockwork RNN, VTA, Ladder VAE are its parts). Its top-level-stores-nuisance result is the most useful warning for any "mood as a slow latent" design.
