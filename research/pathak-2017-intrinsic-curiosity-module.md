# Curiosity-driven exploration by self-supervised prediction, ICM (Pathak, Agrawal, Efros & Darrell)

Citation: D. Pathak, P. Agrawal, A. A. Efros, T. Darrell. "Curiosity-driven Exploration by Self-supervised Prediction." ICML 2017. arXiv:1705.05363.

Source read: arXiv PDF, text-extracted. Read in full: §1–2 (motivation, the three sources of observation change, ICM), §3 (setup, architecture), §4.1 (sparse reward, noise distractor, TRPO-VIME comparison), §4.2 (no-reward exploration in VizDoom and Mario) and §6 (discussion). **Skimmed:** §4.3 (generalisation by fine-tuning on new maps and levels) and §5 (related work). Figures not seen.

## Key claims, with numbers
- **Three kinds of change in observations:** (1) things the agent controls; (2) things it cannot control that affect it ("a vehicle driven by another agent"); (3) things it neither controls nor is affected by (leaves in the wind). "A good feature space for curiosity should model (1) and (2) and be unaffected by (3)."
- **ICM:** features φ(s) trained only by an **inverse model** â_t = g(φ(s_t), φ(s_{t+1})) (Eq. 2–3); a forward model φ̂(s_{t+1}) = f(φ(s_t), a_t) trained by ½‖φ̂ − φ‖² (Eq. 5); intrinsic reward r^i_t = (η/2)‖φ̂(s_{t+1}) − φ(s_{t+1})‖² (Eq. 6); joint loss −λ E[Σ r] + (1−β) L_I + β L_F with β = 0.2, λ = 0.1 (Eq. 7). φ has 288 dimensions.
- **Robustness to uncontrollable noise:** with 40 % of each frame replaced by white noise, ICM still reaches the VizDoom goal; pixel-prediction curiosity "struggles". "Very sparse" reward: ICM + A3C succeeds in 66 % of runs, A3C and ICM-pixels never. Sparse: ICM + A3C 100 % (median 100 %) vs VIME + TRPO 46.1 % (27.1 %), TRPO 26.0 %, A3C 0 %. Random-noise "curiosity" never reaches the goal.
- **No reward at all:** the agent learns corridor following and covers far rooms in VizDoom; in Mario it crosses over 30 % of level 1 and learns to kill or dodge enemies "because getting killed … will result in only seeing a small part of the game space". It stops at a pit at 38 % needing 15–20 exact key presses.
- **Stated limit:** learning progress "has been proposed … as one solution", but "there are currently no known computationally feasible mechanisms for measuring learning progress"; ICM is prediction error, not progress.

## What it means for the engine
1. **The inverse model decides which part of the partner the agent's curiosity sees.** A partner is source (2) and, through contingency, partly source (1). Features trained to recover the agent's own action from consecutive states keep exactly the parts of the partner's face that reveal what the agent just did. A partner who mirrors the agent is the most action-revealing input there is, so the inverse-model features over a dyad concentrate on the mirrored channels, and the curiosity reward then values unpredictable contingent responses. That is a drive to elicit new reactions from the partner: the approval route by curiosity.
2. **Type (2) is missed by construction.** The paper says a good feature space should model sources the agent cannot control but that affect it, yet an inverse-model feature space has no incentive to encode them (its own text: "no incentive … to encode any environmental features that can not influence or are not influenced by the agent's actions"). A partner's independent distress, which the engine must know (D81), is type (2) and would be lost.
3. **For own-body use it is the right typing.** Restricted to the agent's own body variables and own motor channels, an inverse model learns the self-caused part of the body state, which is the identifiability argument of pass 5 (Lachapelle et al.) in practical form.

## Verdict
- **background (noisy-TV fix by action-relevant features; its dyadic failure).** Reject as core: prediction-error curiosity is heterostatic, and its dyadic form turns the partner's contingent reactions into reward.
