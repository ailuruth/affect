# Mastering Diverse Domains through World Models, DreamerV3 (Hafner, Pasukonis, Ba & Lillicrap)

Citation: D. Hafner, J. Pasukonis, J. Ba, T. Lillicrap. "Mastering Diverse Domains through World Models." arXiv:2301.04104 (v2, 17 Apr 2024).

Source read: arXiv PDF, text-extracted. Read in full: main text (introduction, world model, critic, actor, robust predictions, results on 8 domains, Minecraft, ablations, scaling, previous work, conclusion). **Not read:** methods appendix and supplementary per-task curves; figures not seen, numbers from text and captions.

## Key claims, with numbers
- **World model (RSSM):** h_t = f(h_{t−1}, z_{t−1}, a_{t−1}); encoder z_t ~ q(z_t | h_t, x_t); dynamics predictor ẑ_t ~ p(ẑ_t | h_t); heads for reward, continuation and decoder (Eq. 1). Discrete stochastic latents (vectors of softmaxes, straight-through gradients), mixed 1 % uniform to keep KLs well behaved.
- **Loss** (Eqs. 2–3): L = β_pred L_pred + β_dyn L_dyn + β_rep L_rep, β = 1, 1, 0.1; L_dyn = max(1, KL[sg(q) ‖ p]), L_rep = max(1, KL[q ‖ sg(p)]): KL balancing plus **free bits of 1 nat**, which "disables them while they are already minimized well to focus learning on the prediction loss". Vector inputs pass through symlog(x) = sign(x) ln(|x| + 1).
- **Behaviour learned in imagination:** actor and critic act on s_t = (h_t, z_t) over imagined horizon T = 16, γ = 0.997, λ-returns; critic is a categorical over exponentially spaced bins (symexp twohot); returns normalised by the 5th–95th percentile range S (EMA 0.99), only scaled down when S > 1; entropy scale η = 3 × 10⁻⁴ fixed across domains.
- **Results:** one configuration across over 150 tasks in 8 domains; first algorithm to collect diamonds in Minecraft from scratch (all trained agents, within 100 M steps); outperforms tuned specialists on Atari (200 M frames), ProcGen, DMLab (100 M frames vs IMPALA/R2D2+ at 1 B), Atari100k, proprio and visual control, BSuite.
- **Ablation that matters here:** "the performance of Dreamer predominantly rests on the unsupervised reconstruction loss of its world model", unlike prior algorithms that rely mainly on reward and value gradients. Model size 12 M → 400 M raises performance and lowers the data needed.

## What it means for the engine
1. **The latent is made by prediction, behaviour by the critic.** Since representations rest mainly on the reconstruction/prediction loss, what the latent holds is decided by what the world model is asked to predict (the APD past terms), and the reward head only steers behaviour. For the engine this separates two questions: what affect-like structure the latent holds (prediction targets), and whether any partner-dependent quantity trains the actor (the approval route).
2. **The approval route in Dreamer form.** Any reward head or critic whose target depends on the partner's future face or voice (directly or through a body variable the partner moves) trains the actor in imagination to produce the partner states that score well. Imagination makes this worse, not better: the actor can search the model for expressions that elicit partner reactions without ever trying them on the person.
3. **Free bits is a minimum-information floor per step**, a reminder that "how much the latent holds" is set by hand-tuned rate constants (as in CW-VAE), not derived.
4. **Not label-free in its reward:** Dreamer's reward is task-given. The engine's analogue is own-drive change; whether that keeps the approval route closed depends on whether the partner can move the drives (pass-7 synthesis).

## Verdict
- **background (substrate; strongest evidence that representation is set by the prediction objective).** It is the RSSM family the brief already names. Reject as core.
