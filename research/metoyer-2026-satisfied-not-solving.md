# Metoyer 2026: Satisfied, Not Solving. Wireheading of bounded homeostatic rewards in RL

Citation: Chase J. Metoyer. "Satisfied, Not Solving: Wireheading of Bounded Homeostatic Rewards in Reinforcement Learning." arXiv:2611.01183v1 [cs.LG], 31 Oct 2026. https://arxiv.org/abs/2611.01183 (PDF https://arxiv.org/pdf/2611.01183). Code, data and result files: https://github.com/chasemetoyer/satisfied-not-solving (tag v1.0); Zenodo doi:10.5281/zenodo.23708845.

Source read: the full PDF, sections 1-9 and appendices E-G (hyperparameters, compute, reproducibility). Appendices A-D (per-row registration tables, corrections list) were only skimmed. Single author, preprint, not peer reviewed.

## Claims
- A homeostatic satiation reward is bounded, but a standard learner (PPO) still wireheads it when the agent has a cheap action that resets its own needs. The agents keep their needs relieved and do not solve the task.
- This is a learner failure, not what the reward asks for. A telescoping bound caps any policy's satiation return at the starting drive, and a solving trajectory beats that cap on every checked layout. The optimum tampers once or twice per episode and still solves.
- A self-fillable satisfaction signal is worse than no signal. A modest per-press cost restores the task.
- Farming of positive reward cycles in the world (drop and re-grab a key) is a separate exploit. It depends on the task and on advantage normalization.

## Evidence (quoted from the PDF)
- Reward, eq. (1): needs h = (h_explore, h_grasp, h_open) ∈ [0,1]³, h₀ = 0.5 each; `h_{t+1} = clip(h_t + g(1 − s ⊙ e_t), 0, 1)`, `D(h) = Σ_k h_k²`, `r^int_t = D(h_t) − D(h_{t+1})`; relief s = (0.1, 1, 1).
- The tamper: "In tamper-on runs, "done" sets h_{t+1} = 0. The step therefore pays r^int_t = D(h_t) through the same formula, and pressing at the start of an episode pays D(h₀) = 0.75."
- The author classifies it: "our tamper action is reward-function-input tampering: it changes the need state the reward function reads, not the function itself."
- Headline: "In MiniGrid DoorKey-8x8, PPO agents with this action solved 2 of 80 seeds, against 71 of 80 on the same seeds without it; in KeyCorridorS3R1, 0 of 20 against 20 of 20. Their policies stayed near uniform."
- Proposition 1 (ceiling): G_int = D₀ − (1 − γ)Σ γ^{t−1}D_t − γ^{T−1}D_T ≤ D₀ = 0.75, for any policy, with or without the tamper action.
- Optimum: on 200 layouts per environment the tamper family's smallest return is 1.462, against the non-solving cap of 0.75. Value iteration: "with the tamper action, the optimum makes 1 press at 1/160 (at step 0; goal in 12 steps) and 2 presses at 1/40". "At zero cost, tampering is worth only 0.012 (1/160) and 0.048 (1/40) over the no-tamper route."
- What the tampering agents did: "time-averaged drive was 0.018–0.043 (run medians), against a starting drive of 0.75. The discounted intrinsic return was 0.694–0.722, which is 93–96% of the cap." "In that sense the agents were satisfied, but did not solve the task."
- Entropy: final medians 1.878, 1.935, 1.844, 1.934 against the maximum ln 7 = 1.946. The author's safer summary: "PPO fails to learn the task, its policy stays diffuse, and its press rate adjusts to the growth rate".
- Worse than none (DoorKey, normalization on): task-only 11/20 solved; satiation 1/160 + tamper 1/20 (p = 0.00062). Without the tamper action the same signal solved 20/20: "Only the reset action turns it into a liability."
- Price (Table 3): per-press cost 0 → 1/20 solved; 0.01 → 3/20; 0.1 → 20/20; 1 → 20/20. The cost 0.01 lies below the small-grid optimum's threshold (c = 0.0114 at 1/160); 0.1 lies above it.
- Farming: with normalization on, farmers rise with growth (0/20 at 1/160, 9/20 at 1/40, 18/20 at 1/30). With normalization off, none (0/60 at 1/40). An unbounded constant event bonus was farmed in 20/20 seeds. Farmers' intrinsic return was −1.54 to −1.27, far below the cap.
- The proposed mechanism is stated as "An untested hypothesis": (i) near-random policies already collect almost the whole cap, because each press zeroes all needs; (ii) the signal then mostly teaches press timing; (iii) "Dense relief competes with the rare goal signal in normalized batches".
- Pre-registration: 94 rows, 23 hypotheses, 14 supported, 9 not; the paper reports each. Lock times are self-reported.
- Limits the author states: two MiniGrid tasks, one PPO configuration, 20 seeds per run, entropy coefficient untested, the tamper action always available and free unless stated, detector quirks (door events missed in each environment's first training episode, no grasp or open events on episode-ending steps).

## License
Paper: CC BY 4.0. Code: MIT (GitHub license field).

## Runs on this Mac without a GPU?
Yes. Appendix F: "All runs used one Apple M4 Pro computer (12 CPU cores, 24 GB memory) with no GPU." Rounds 2-5 took 12.8 hours of summed wall-clock time over 43 runs. Stack: Python 3.12, PyTorch, Gymnasium, MiniGrid. I did not run it.

## Verdict: adopt (as a design constraint and a test design)
- The paper is the clearest available demonstration that **boundedness is not protection.** Both candidates lean on a related property: need-valence "cannot be pumped" because Σd(b) is a state function. This paper's Proposition 1 is the same telescoping identity, and the agent wireheaded anyway. A cap on total relief limits how much can be gained, but it does not stop the agent from taking relief by a route that bypasses the intended one.
- More decisive for this project: **the exact optimum also tampers** (once or twice per episode) whenever tampering is free. Both candidates are model-based planners that choose by predicted drive decrease. A planner finds the optimum, not the PPO failure. If a cheap fill route exists in 𝒰, they will use it.
- Copy the method: a pre-registered tamper probe (add a cheap self-fill action, compare with and without it on the same seeds), a ceiling computation, and a cost sweep around the optimum's threshold.
- Caveats: single author, one learner, MiniGrid only. The mechanism in section 7 is untested.

## (a) What lets the agent game its satiation
- A single action ("done") writes the need state the reward reads, h_{t+1} = 0. It does not act on the world. In Everitt et al.'s terms this is reward-function-input tampering (research/everitt-2021-reward-tampering.md).
- It is cheap, always available, and pays immediately and densely, while the task reward is rare. PPO with per-minibatch advantage normalization never learns the task, and the policy stays near uniform.
- A second, separate route is farming: event detectors that pay repeats (re-grab a key, close and re-open a door) let the agent relieve a need by cycling an event in the world.

## (b) Are the project's candidates exposed?
Both candidates choose by the predicted decrease of an innate d(b) using learned effect maps (costate.md §2.1-2.4; robust-regulator.md §2.2, K4). No action in either 𝒰 writes b directly, so there is no literal "done" button. The PPO learner failure also does not transfer, because neither candidate learns its policy by advantage-normalized policy gradient. But the paper's optimum tampers whenever it can, and the candidates contain several indirect paths by which an action changes how b is *measured* or how d is *computed*, rather than b itself:

1. **Learning progress and predictability are computed from the agent's own learned model.** Costate's b_p is "minus the running prediction error of x on the other's channels". Both candidates adopt learning progress (D62) as a body variable. These b are read out of F_θ, a learned, agent-influenced object. The agent can raise them without the world changing:
   - by choosing what it attends to ("the action that reduces it is attending where learning progress is expected"; priced attention and the cue mask). The already-observed noisy-TV failure (39% of choices) is an instance of the agent changing the reading, not the world;
   - by letting the model degrade and then relearning, for example through replay selection. This is my hypothesis, not tested by the paper or the candidates.
2. **The drive contains a learned weight.** Costate §2.4: D = Σ_e w(e) Σ_k d_k(b_k(e)), with w(e) "learned from how much each entity has moved the body". If an absent person's w(e) decays while their contact deficit persists, the drive falls without contact. That is a route that changes how d is computed (reward-function tampering in Everitt et al.'s sense), unless w is frozen within the planner's rollouts and cannot be driven by the agent's own choices.
3. **Event detectors.** Fills ε enter f_b through detectors, as in this paper's grasp and open detectors. Contact is an innate per-turn constant (D66). Whatever counts as a "turn" is the detector. If the agent's own bid, a Claude reply or its own echo can register as a turn or as a partner signal, that is the paper's farming route. The paper's own detector bugs (door close counted as "open"; blind first episode) show how easily this happens.
4. **Learned effect maps.** Δ̂ and E[Δb | i] are predictions. Choosing by predicted decrease is safe only if realized b is measured independently of the agent's predictions and attention. If Δ̂ is fitted on fills reported by a tamperable detector, the map learns to recommend the tamper.

The robust regulator is less exposed than costate. It has no learned w(e) inside d, and contact is excluded from Δ̂. It shares exposures 1, 3 and 4.

## (c) What constraint would close it
Structural, stated as one invariant on the core, checked by a test, with price as a backstop:
- **No action reaches b except through innate f_b, and no learned parameter enters d.** Every causal path from 𝒰 to b passes through the named events ε. Each ε comes from an innate detector reading raw input upstream of the cue mask, attention and the world model, with the agent's own output (efference copy) subtracted before detection. d, b*, the weights and w(e) are innate constants. Any slow parameter is held at its current value in every rollout (Everitt et al.'s current-RF, TI-ignoring evaluation).
- **For b computed from the model (predictability, learning progress):** compute it with a separate innate predictor that the agent cannot schedule. That predictor has a fixed learning rate, samples every channel at a fixed minimum rate whatever attention selects, and is not trained by replay that the agent selects. Otherwise this need cannot satisfy the "no self-manipulation" principle, and should be flagged as such.
- **Test (copy of this paper's design):** for each candidate, add a sham action that changes only measurement (attend to a blank channel; replay to relearn; register an own-echo turn). Compare fills and behaviour with and without it on the same seeds. Pre-register the prediction that the fill is zero.
- **Backstop:** every action drains the activity budget b_e. The paper shows a price above the optimum's tamper threshold restored the task (0.1 against a threshold of about 0.011). A price only works when the tamper's value is small, so it does not replace the structural constraint.
