# Yoshida & Man 2024/2025: Empathic / Homeostatic Coupling for Prosocial Behavior

Sources read: arXiv 2412.12103v1 (NeurIPS 2024 IMOL workshop) and arXiv 2506.12894v1 (full paper; cited by Sanyal 2026 as ALIFE 2025 proceedings 37:32), both in full. Code read: README and `train_foodshare_decoder_learning.py` of github.com/ugo-nama-kun/empathy_homeostatic_rl. That repo is matched to the paper because it has the same name as the paper's expired anonymous link (`empathy_homeostatic_rl-7E8F`) and the owner hosts Yoshida's other HRRL repos. The README cites "Anonymous Authors", so authorship is inferred, not stated.

## Claims
- Homeostatic agents that regulate only their own body do not learn to share food.
- Observing the partner's internal state ("cognitive empathy") does not change that.
- Adding the partner's drive to one's own ("affective empathy", homeostatic coupling) produces sharing. Coupling plus observation shares more selectively.
- 2025 addition: an agent can infer a partner's hidden state by running its own self-trained decoder on the partner's expression, assuming both share the same fixed expression generator.

## Evidence
- Three environments; PPO with an MLP encoder and LSTM; n=20 runs per condition; 95% confidence intervals.
  - Food-share: binary energy, P(High to Low) = 0.1, 25k steps, hidden 16.
  - 1-D grid with 5 cells: 1M steps, hidden 32.
  - 2-D field with two mobile agents: 20M steps, hidden 64, shared weights, injury p = 0.0005.
- Drive and reward: `D = D_self + w*D_partner` with `w = 0.5`; `r_{t+1} = beta*(D_t - D_{t+1})`.
  - Food-share uses `D = -ln P*(s)` with `P*(High) = 0.95`.
  - Grid and field use `D = s^2` (setpoint 0) and `beta = 100`.
- Energy dynamics: `s_{t+1} = s_t - delta_out + delta_in*I_t`. The grid has `delta_out = 0.003` and `delta_in = 0.1`. The field has `delta_out = 0.001`; the gain is 0.1 in the 2025 text and 0.3 in the 2024 appendix. Agents are immobile below -0.7 and the episode ends outside [-1, 1].
- Decoder experiment: the expression is a 5-d vector from a fixed random MLP (1 to 20 to 5, ReLU), shared by both agents. The decoder mirrors it and is trained by MSE on the agent's own (expression, state) pairs, then used as `D~_partner = ||dec(v_partner)||^2`.
- Grid survival in steps, mean ± CI:

| Condition | trained decoder | untrained decoder |
|---|---|---|
| Cognitive, type A | 356 ± 29 | 368 ± 31 |
| Affective only | 2147 ± 558 | 1628 ± 795 |
| Full, type A | 2625 ± 499 | 1125 ± 802 |
| Full, type B | 2812 ± 368 | 1182 ± 791 |

- Toy scale only: 1-d energy, 2 agents, discrete actions.

## License
- Papers: CC BY 4.0 (arXiv).
- Code: MIT. The environments come from the `tiny_empathy` package, also MIT, by the same owner.

## Runs on this Mac without a GPU?
Yes. The scripts default to `cuda=False` and use small MLP/LSTM PPO (CleanRL style). Food-share (25k steps) and grid (1M) are minutes to hours on CPU. The 2-D field (20M steps) is slow but feasible. Not run.

## Verdict: adopt
This is Principle 3 (read others through one's own body; infer by inverting one's own generative mapping) in executable form, and Principle 6 holds: the drive is satiable and the reward is drive reduction, not partner approval.

## What it gives S1
- Coupling term: `D_bot = D(b) + w*D(b_hat_user)` with `w` a stated, ablatable constant (start at 0.5). `b_hat_user` is never a label. It is the Bot's decoder output on user features. In S1 those are text-side signals such as reply latency, message length and edit/typing timing; in S2, AUs and prosody.
- Self-decoder recipe: keep the Bot's own `b -> expression` map fixed (innate), log (expression, b) pairs from the Bot's own life, train `dec` by MSE, and apply it to the user. For S2 this requires the Bot's expression space to match the perceived feature space (AUs to AUs). In S1 the shared space would be text-timing features.
- Failure modes:
  - With coupling but no observation, the agent over-helps: it "supplies an excess of food" and feeds the partner at any energy level.
  - An untrained, random decoder still raised survival in the grid (1628 steps). The authors leave this unexplained, so the decoder ablation can be confounded by the continuous state.
  - The coupled drive rewards reducing the user's inferred need, not the user's smiles. Keep it that way to avoid training flattery (Principle 6).
- S1 ablation hook: with `w = 0`, the Bot's response to a returning user should depend only on its own contact deficit. With `w > 0`, it should also track the user's inferred state at return, for example a slow, terse reply pattern.

## Re-read for helping without placation (2026-11-26)
Both arXiv papers were re-read in full: 2412.12103v1 (main text and discussion) and 2506.12894v1 (main text, Table 1 and appendices A–B). The question was whether "care blind to its effect will not learn to help".

**What the papers show on that question.**
- **The coupling *is* a path from act to the partner's state to one's own reward.** D = D_self + w·D_partner, with r = β(D_t − D_{t+1}). PASS lowers D_partner, so PASS is rewarded. That is precisely the path the ledger design's action-blind partner head cuts.
- **Observing without that path does not help.** The "cognitive" condition observes the partner's state but has no coupling. It learns no sharing in any environment: grid survival 356 ± 29 (trained decoder, type A) against 2147–2812 for coupled conditions.
  - The ledger design is not the cognitive condition, because its drive does contain 𝒟(b̂_p).
  - But with the partner head action-blind, the planner predicts that no act changes b̂_p. Within rollouts, care therefore behaves as uncoupled. Only R (self-simulated relief) can make an act look good.
  - So the critic is right: Yoshida & Man's result says that, without a modelled act → partner → own-drive path, helping is not learned from the partner's outcomes.
- **Coupling without observation over-helps.** "Supplying an excess of food to the Partner"; the partner is "fed indiscriminately ... at various energy values". Selectivity needs both the path and the observation (full condition: more PASS when the partner is Low).
- **In the decoder experiment the coupled term reads the partner's *expression*.** D̃_partner = ||dec_θ(v_partner)||², with v from a fixed, shared, honest generator. So the act → partner state → **partner face** → decoder → reward path is the learning signal.
  - This is safe in their world only because the agent cannot change v except by changing s (no contagion, no politeness, no masking).
  - In a human dyad that assumption fails. Their mechanism transplanted as written is a reward on the partner's display, which Principle 6 forbids.
- **Unexplained:** an untrained, random decoder still gave 1628 ± 795 steps (affective) in the grid. The authors put this down to the continuous state. It means the "learned reading" credit is partly confounded.

## What it means for the designs (helping without placation)
1. **Keep a path, but not through the face.** The fix is not to drop the coupling, which kills helping, or to keep it on the decoded face, which brings back placation. Restore the act → need → own-drive path and cut only the act → display edge, per Farquhar et al. 2022's path-specific objective. In rollouts, the partner's *display* is imputed from the action-blind baseline. The partner's *need* is updated by the act and read from channels other than the face: the content of their words about their situation, and the moves they make next.
2. **The self-decoder idea carries over to those channels.** The agent can learn need-from-words the same way Yoshida & Man learn state-from-face: train on its own (own words, own body) pairs and apply the result to the partner (P3). That is the lexical-body head the design already has. It must then be *frozen and private* in rollouts (Everitt et al. 2021 Claim 9) so the planner cannot gain by eliciting misleading words.
3. **Keep the full-condition lesson: path plus observation.** A path without observation gives indiscriminate comfort, the conversational form of over-feeding. The observation half is the face as *response* evidence (when to care), which Principle 6 allows.
4. Verdict unchanged (adopt), with the amendment: the coupled drive's partner term must be computed from a need estimate that has no edge from the partner's post-act display.
