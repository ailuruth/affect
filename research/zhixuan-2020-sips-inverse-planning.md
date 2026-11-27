# Online Bayesian Goal Inference for Boundedly-Rational Planning Agents (Zhi-Xuan, Mann, Silver, Tenenbaum & Mansinghka)

Citation: T. Zhi-Xuan, J. L. Mann, T. Silver, J. B. Tenenbaum, V. K. Mansinghka. "Online Bayesian Goal Inference for Boundedly-Rational Planning Agents." *NeurIPS* 2020. arXiv:2006.07532.

Source read: arXiv v2 PDF, text-extracted. Read in full: abstract, §1–9 (including Algorithm 1, Table 1, Broader Impact). **Not read:** the supplement (extra trajectories, experimental parameters).

## The model
- **Generative process for the observed agent:** goal g ∼ P(g); plan update p_t ∼ P(p_t | s_t, p_{t−1}, g); action a_t ∼ P(a_t | s_t, p_t); state transition; observation noise. The plan p_t is an explicit latent: the agent's partial plan, its intention.
- **Bounded rationality is in planning, not in acting.**
  - The agent replans only when it reaches the end of its current plan or meets a state the plan did not anticipate.
  - Each replanning has a node budget η ∼ NegativeBinomial(r, q) (persistence), and runs a stochastic A* that expands successors with probability ∝ exp(−f(s, g)/γ), where f = path cost + heuristic.
  - It executes the partial plan to the best state found, then continues.
- **Inference: Sequential Inverse Plan Search (SIPS).** A particle filter over (goal, plan) hypotheses. A particle's plan is extended only when the observed time runs past it, so computation is spent only on surprise. Resampling when the effective sample size drops; two Metropolis–Hastings rejuvenation kernels: a heuristic goal proposal (reintroduce goals close to the current state) and an error-driven replanning proposal (resample a time near where hypothesis and observation diverge, and replan from there).

## Results
- **Human-likeness.** On ten Doors-Keys-Gems trajectories (six sub-optimal or failed), with 8 pilot subjects, SIPS correlates with mean human goal inferences at r = 0.89 overall, against 0.51 for Bayesian IRL (oracle). On one backtracking trajectory, r = 0.99 vs 0.80. Boltzmann action noise gives too much likelihood to undoing past actions.
- **Accuracy and speed** (Table 1a): across Taxi, Doors-Keys-Gems, Block Words and Intrusion Detection (|S| up to ~10³⁰, 20 goals), SIPS beats unbiased BIRL, whose value iteration often fails to converge, and is comparable to oracle BIRL, often with far less computation. With matched parameters, 10 particles per goal suffice without rejuvenation.
- **Robustness** (Table 1b): top-1 accuracy holds roughly under mismatched persistence, noise and heuristic, and on Boltzmann-rational and optimal agents; on 5 pilot humans, 0.77 (Doors-Keys-Gems) and 0.43 (Block Words).
- **Limits stated.** Finite goal sets; final, non-hierarchical goals; deterministic symbolic domains.

## The mathematical object
The other's mind as **a partial plan produced by a resource-bounded search in a shared world model, revised only when it fails to predict**. The observer runs the same kind of planner forward, so it reads the other through its own planning machinery. Two structural points:
- randomness lives at the level of planning, so a few observations are strongly informative;
- the inference does work only at divergence points.

## What it means for the design
1. **"Read the other through one's own body" as running one's own controller in inverse.** For faces and voices the analogue is the agent's own motor plan (the expression it would be producing) inferred for the partner from the partner's movement in the agent's coordinates. The index already holds the affective version (houlihan-2023-emotion-prediction-generative-tom.md) and the Yoshida–Man decoder.
2. **Divergence-triggered updating gives event time from structure.** The partner model changes only when the partner leaves the predicted plan. The rate of such events, not a time constant, sets how fast the partner model moves. That is a structural time scale, and it carries contingency (a partner whose plan changes right after the agent's act).
3. **The hazard.** If the inferred partner plan is expressed in the agent's own motor coordinates and anything reads it into the agent's own plan, it is a copy route by construction. The inferred plan must stay typed as "theirs".

## Verdict
- **watch (object: intention as a bounded partial plan, updated at divergence).** It is Bayesian inverse planning with an SMC inference scheme in symbolic domains. For continuous faces it would need a continuous planner and a learned body model; as a core it is BToM, a known framework.
