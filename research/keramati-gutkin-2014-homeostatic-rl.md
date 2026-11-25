# Keramati & Gutkin 2014, "Homeostatic reinforcement learning for integrating reward collection and physiological stability" (eLife 3:e04811)

Source read: the eLife PDF (v1, 26 pages), read in full on 2026-11-24, from the abstract and digest through Results, Discussion, "Limitations and future directions", Conclusion and the Materials and methods proof. The equations were checked against the eLife XML (MathML) because PDF extraction garbles them. Not read: the reference list, the figure source-data tables of free parameters, and the figure supplements other than their legends.

## Claims
- The drive is a distance of the internal state H_t from the setpoint H* in "homeostatic space": D(H_t) = m-th root of Σ_i |h*_i − h_i,t|^n (Eq. 1). "m and n are free parameters". The authors also propose that drive equals surprise, "D(H_t) = −ln p(H_t)".
- Primary reward is the drive reduction caused by an outcome K_t: "r(H_t, K_t) = D(H_t) − D(H_t + K_t)" (Eq. 2).
- The equivalence result: "any behavioral policy, π, that maximizes the sum of discounted rewards (SDR) also minimizes the sum of discounted deviations from the setpoint, and vice versa", "if γ < 1" (Eq. 5). Without discounting, "the rewarding value of a behavioral policy that changes the internal state only depends on the initial and final internal states, regardless of its trajectory", so "to maintain internal stability, it is necessary to discount future rewards."
- In practice the reward is computed from a sensory estimate of the outcome, "r(H_t, K̂_t) = D(H_t) − D(H_t + K̂_t)" (Eq. 10), "as soon as they are sensed/consumed, without having to wait for the outcome to be digested". "The rationality of our theory ... holds only as long as K̂_t is an unbiased estimation of K_t."
- A linear approximation gives a gradient form: "r(H_t, K_t) ≅ −K_t·∇D_H(H_t) + O(∇²D_H(H_t))" (Eq. 13). That is, "the rewarding value of outcomes is linearly proportional to their need-reduction capacity (K_t), as well as a function (the gradient of drive) of the deprivation level."
- Anticipatory responding is explained as learned optimal control. In the authors' words, "the tolerance response caused by predicted hypothermia is an optimal behavior in terms of minimizing homeostatic deviation and thus, maximizing reward". It predicts that "animals are capable of learning not only Pavlovian ... but also instrumental anticipatory responding". The authors argue that incentive salience theory "cannot give a computational account of anticipatory responding", because at cue time "the animal's internal state is not deviated".

## Evidence
Theory plus small simulations; no new data.

- The proof (Methods): over trajectories P(H0) "that if start from H0, will end up at H*", SDR = D0 + (γ − 1)·SDD (Eq. S5). "Since D0 has a fixed value and γ – 1 < 0", maximizing SDR minimizes SDD. Note the restriction to trajectories that end at the setpoint. The Results text states the equivalence for any policy without that qualifier.
- With "n > m > 1" the drive reproduces four effects: reward increases with dose (Eq. 6), deprivation potentiates reward (Eq. 7), irrelevant drives inhibit it (Eq. 8), and concavity gives risk aversion (Eq. 9). The authors add that "the equations in this section hold only when the internal state remains below the setpoint".
- Ethanol tolerance (data from Mansfield & Cunningham 1980): the temperature drop "was significant on the first day, but gradually disappeared over 8 days". The simulation's learning curves are "averaged over 500 simulated agents". After learning, omitting ethanol makes the cue-triggered response push temperature "beyond the setpoint".
- Avoiding extreme states without experiencing them: starting at 30 with the setpoint at 0, a single agent "never visits states with a deviation of more than 40 units after 10^6 trials". Across "10^5 agents over the 1500 trials" the maximum deviation "was 61".
- Oral versus intragastric water (McFarland 1969) and the rise-fall response pattern: "classical RL models only explain the ascending, and classical HR models only explain the descending pattern".
- Over-eating needs an extra drive-independent term: "r(H_t, K_t) = D(H_t) – D(H_t + K_t) + T" (Eq. 11), with "T > 0 for palatable foods". For m/n = 1 this is equivalent to a shifted setpoint, "H* + T/2K_t".
- A small discrepancy in the source: the text says that for "m = n = 1, the drive function reduces to Euclidian distance". With m = n = 1, Eq. 1 is the sum of absolute deviations. The Euclidean case is m = n = 2, as the later Yoshida et al. 2025 note states (yoshida-sprekeler-gutkin-2025-hrrl.md).

What the authors say the theory cannot explain:
- "our theory only applies to rewards that have a corresponding regulatory system. How to extend our theory to rewards without a corresponding homeostatic regulation system (e.g., social rewards, novelty-induced reward, etc.) remains a key challenge".
- Survival "may themselves be seen as means of guaranteeing reproduction", and can be "replaced with parental sacrifice".
- The setup assumes full observability ("as opposed to the fully-observable setup we used") and a fixed setpoint. The drive form cannot produce "asymmetric risk-aversion toward gains vs. losses".
- Irrational behaviour such as binge eating is outside the normative core and needs the ad hoc T term. The theory "does not purport to explain the full gamut of animal behavior".
- They list Berridge 2004 among "major criticisms" of drive reduction and claim to fix three of them: anticipatory responding, secondary reinforcers, and the non-reward of intravenous food.

## License
CC BY: "distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use and redistribution provided that the original author and source are credited." I saw no code link in the article text. The simulations are small tabular MDPs.

## Runs on this Mac without a GPU?
Yes, by reimplementation. This is our judgment, not a claim in the paper: the models are tabular RL over a one- or two-dimensional internal state, so CPU seconds to minutes.

## Verdict: adopt (as the formal base, with the gradient form as the bridge to a costate)
- For (a), the costate: Eq. 13 is the closest published statement to our design. Reward to first order is −K·∇D, so the gradient of drive with respect to body variables is the per-unit price of each need, and an outcome's reward is that price times what it delivers. Our step is to replace ∇D, the gradient of the instantaneous drive, with ∂V/∂H, the gradient of the learned value. Under the authors' equivalence, V is minus the discounted sum of future drive plus a constant, so ∂V/∂H is a forward-looking shadow price. That extension is ours, not theirs. Watch the proof's restriction to trajectories that end at H*.
- For (b), anticipation: K̂ (Eq. 10) makes reward fire on sensing, before the body changes. This matches the seconds-scale AgRP drop in Chen 2015 and Betley 2015. The theory says nothing about the relapse when the predicted K never arrives, which Chen measured at τ ≈ 258 s. In this framework that would have to come from correcting K̂, or from H actually not changing.
- For (c), the critique: by the authors' own account, rewards with no regulated variable (social, novelty) are outside the theory, and palatability-driven intake needs an extra term T. Both are exactly Berridge's ground (berridge-2004-motivation-concepts.md). For a companion agent whose main currency is social, this limitation is central, not marginal.
