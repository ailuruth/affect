# Emergence of Social Reality of Emotion through a Social Allostasis Model with Dynamic Interpretants

Nomura, Tsubamoto and Horii (University of Osaka), arXiv 2605.07761, May 2026. Read in full (a short preprint).

## Claims
- The paper implements the constructed-emotion idea of **social reality**: emotion concepts for interoceptive states become shared by community agreement. Two agents regulate their own bodies by active inference and exchange symbols. The symbols are "regarded as socially shared emotion concepts".
- Each agent is a discrete POMDP over interoception: 6 energy levels × 6 temperature levels = 36 states, with 5 actions (Cool, Warm, Eat, Play, Sleep).
  - Each agent picks the symbol whose actions minimize expected free energy.
  - A Metropolis–Hastings Naming Game decides whose symbol is used.
  - A shared matrix $E$ maps symbols to actions.
- When an agent's symbol is rejected, it moves its **own prior preference** (body setpoint) toward what the partner's symbol predicts. The preferences converge to a compromise: the Jensen–Shannon divergence falls over about 2.5M iterations. Symbol meanings drift, for example some "Eat" symbols become "Sleep" once preferences align.

## Evidence
- One simulated scenario. Agent A starts preferring high temperature and agent B low; both prefer moderate energy.
- The transition model $B$ and initial-state prior $D$ are given exactly. The likelihood $A$, preference $C$ and interpretation $E$ are learned online.
- Results are figures of one trajectory. No seeds, statistics, baselines or ablations are reported. The authors list the limitation as "restricted to a discrete environment and a discrete generative model".

## License
- Paper: CC BY 4.0.
- Code: none linked.

## Runs on this Mac without a GPU?
Yes in principle (tiny discrete POMDPs), but no code is released.

## Verdict: watch
It is the only computational model found that puts Barrett's social side, where concepts get their meaning by agreement, on top of interoceptive active inference. That fits the brief's split between body and concept.

Against the Principles:
- Its "emotion concepts" are really **action symbols**. The evidence is one unablated run (Principle 5).
- Its core mechanism lets the partner shift the agent's **body setpoints**. If carried over to the Bot and user, the user's words would move what the Bot's body needs. That is a conformity channel close to the flattery Principle 6 guards against.

## What it gives S1
- **A model for naming that is negotiated, not fixed.** In S1, Claude's names for recurring latent states can be stored per user and revised when the user offers a different word ("you sound tired, not sad"). The stored name is keyed to a region of $h$, not to an emotion list. This is Barrett's "category as population" with a social anchor. It needs no emotion variables (Principle 2).
- **A hard boundary for S1.** Names and reappraisals may change $h$ (prediction) but must **not** change body setpoints $C$. Contact need, predictability and activity budget stay innate and satiable. This is the opposite of the paper's preference update, and it should be written into the S1 design as a deliberate departure.
- **Testable later, not S1:** whether the Bot's vocabulary for its own states converges with the user's over weeks, measured as distance between the label distributions per region of $h$. This belongs to S3 ("person-specific attitudes").
