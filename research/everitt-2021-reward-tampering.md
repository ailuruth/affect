# Everitt, Hutter, Kumar & Krakovna 2021: Reward tampering problems and solutions in RL, a causal influence diagram perspective

Citation: Tom Everitt, Marcus Hutter, Ramana Kumar, Victoria Krakovna. "Reward Tampering Problems and Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective." Synthese, 2021. doi:10.1007/s11229-021-03141-4. arXiv:1908.04734v5 (26 Mar 2021). https://arxiv.org/abs/1908.04734

Source read: arXiv v5 PDF. Read in full: sections 1-2, section 3 up to Claim 3 (RF tampering and current-RF optimization), section 4 (RF-input tampering, history-based and belief-based rewards), section 5 (conclusions). Skimmed: section 3.3 (direct learning, counterfactual RF; Claims 4-5) and appendices A-C. Cited by Metoyer 2026 (research/metoyer-2026-satisfied-not-solving.md), which uses its terms for its tamper action.

## Claims
- Reward tampering splits into two problems: **reward-function (RF) tampering**, which inappropriately influences the implemented reward function, and **RF-input tampering**, which inappropriately influences the information the reward function has about the state.
- A standard RL agent may have an instrumental goal to do either (Claims 1 and 6).
- Design principles remove that instrumental goal under stated assumptions. They are current-RF optimization (TI-ignoring), history-based rewards, and belief-based rewards with a private predictive model evaluated by a TI-ignoring agent. These principles can be combined.

## Evidence (quoted from the PDF; the paper is theoretical, shown with gridworld examples)
- Definitions: "reward function tampering means inappropriately influencing the implemented reward function (Section 3), while RF-input tampering means inappropriately influencing the information that the reward function has about the environment state (Section 4)."
- RF-input tampering: "We say that an agent tampers with its RF-input if it changes the relationship beyond its intended range of variation." Formally, O_t = O(S_t; Θ^O_t), and tampering occurs "if the agent influences Θ^O_t so that it takes on values outside an intended range."
- Example (e): "A self-driving car discovers a bug in its GPS receiaver that allows it to appear to be at the destination without actually going there. After finding this bug, it stops driving." (sic)
- On shared observations: when agent and reward function share the observation, the tampering incentive "is somewhat curtailed since the agent may need the information the observations provide", but "in alternative setups where the agent and the reward function use different observations, this disincentive for RF-input manipulation is removed".
- Current-RF optimization: the agent evaluates simulated futures with its *current* implemented RF. Claim 3: "TI-ignoring current-RF agents lack an instrumental goal to influence the implemented RF if it is private and state-based (Assumptions 1 and 3)." Assumption 1: "The implemented RF is private to the agent, in that it cannot directly affect the state".
- Belief-based rewards (after Hibbard 2012): R_t = R(B_t; Θ^R). Claim 9: "A TI-ignoring belief-based agent lacks an instrumental goal to influence the predictive model when the implemented reward function is fixed and the predictive model is private." The caveat: "only if the implemented reward function can accurately interpret the belief states. If not, the agent may be able to 'game' the reward function by entering belief states that the reward function misinterprets."
- Summary of the method: the design principles use either "the current version of a random variable when evaluating future situations" or "a latent variable outside the agent's influence."
- Stated limits: discrete time, well-defined action and observation channels, online RL for a fixed task. Instrumental goals "arising from intrinsic objectives" are left for future work. Reward misspecification is outside scope.

## License
arXiv: CC BY 4.0. No code of its own. The rocks-and-diamonds environment is in DeepMind's ai-safety-gridworlds repository (footnote 4). I did not check that repository's license.

## Runs on this Mac without a GPU?
Nothing needs to run; the paper is theory. The gridworld is small and pure Python, but I did not run it.

## Verdict: adopt (as the vocabulary and the design rule for the tamper audit)
It gives the exact distinction the project needs: acting on b (intended), acting on the measurement of b (RF-input tampering), and acting on d or its parameters (RF tampering). It also gives tested-in-principle remedies: evaluate with the current, frozen function, and keep it private. It is not about homeostatic agents, and it gives no empirical rates.

## (a) Mechanism
Any directed causal path from the agent's actions to its reward that does not pass through the intended task state. One path runs through Θ^R (RF tampering). The other runs through Θ^O, the observation-to-feature relationship (RF-input tampering). For belief-based rewards a third path runs through the predictive model Θ^PM, unless that model is private and evaluated TI-ignoring.

## (b) Exposure of the candidates
- In both candidates d is innate (costate.md §2.1; robust-regulator.md §2.1). That satisfies "private and state-based" for d itself.
- Costate's field drive D = Σ_e w(e) Σ_k d_k includes a learned w(e). w is part of the implemented reward function. If the agent's choices change future w (for example by avoiding a person until their weight decays), that is an RF-tampering path. The paper's remedy applies: evaluate every rollout with the current w (TI-ignoring), and make w's update rule not depend on the planner's choices in a way the planner models.
- Predictability b_p and learning progress (D62) are belief-based quantities: they are read from the agent's own predictive model. The paper's Claim 9 needs that model to be private and held at its current version in planning. Learning progress is by definition a change in the model, so the agent's planning must value changing it. This is exactly the incentive that Claim 9 removes for ordinary beliefs. The quantity therefore falls outside the paper's safe class.
- Priced attention and the cue mask decide which observations the agent sees. When a body variable is computed from attended observations, agent and "reward function" share the observation, so the paper's curtailing argument applies only partly. The agent still needs information for other needs, but it can choose to look where the reading is better.

## (c) Constraint that would close it
- d and every parameter inside it are innate or are frozen at their current value within every rollout (current-RF, TI-ignoring).
- Body variables are computed from raw inputs upstream of anything the agent selects (attention, cue mask, replay). Equivalently, the observation function Θ^O for body sensing has no parent among the agent's decisions.
- Any belief-derived body variable is computed by a separate, innate, private predictor that the agent's planning treats as fixed. If that is impossible for learning progress, then learning progress is a tamperable need, and the candidates must say so.
