# Grimbly et al. 2026: Interoceptive Attention as Dynamic Homeostatic Prioritization (AffectWorld)

Source read: arXiv 2608.04232v1 (SAB 2026 paper plus supplement sections A onward), main text in full. Code: README and LICENSE of github.com/sgrimbly/attention-aif-sab2026-snapshot.

## Claims
- An active-inference agent with a fixed total interoceptive precision budget survives better when, at each step, it gives most of that budget to the channel its own beliefs say is most needed.
- The benefit comes mostly through planning: the precision-shaped likelihood enters the expected free energy (EFE) planner, not only perception.
- Direction matters. Aiming precision at the least-needed channel does worse than spreading it evenly.
- The attended channel's likelihood is learned about 2x faster per observation.

## Evidence
- AffectWorld: 6x6 grid with 2 food and 2 water tiles, episodes up to 60 steps.
- Body channels: hunger and thirst (lethal at 0), suffocation (non-lethal, drains on water), and an inert control channel. Body levels run 0-5.
- Observation likelihood: `A[o,s] = kappa_m` if `o = s`, else `(1 - kappa_m)/5`. Budget: `sum kappa_m <= K = 2.60`, `kappa in [0.05, 1]`. The attended channel gets `kappa = 0.90` and the rest `0.567`; uniform is `0.65`.
- Selector: `m* = argmax_m E_q[need_m]` with `need = (s_max - s)/s_max`, read from the agent's own posterior, never from ground truth. B (body dynamics) is fixed; A is learned with Dirichlet counts (alpha0 = 0.1); planning horizon is 3.
- Survival over the learning phase (11 layouts x 32 seeds x 100 trials): attentive 0.414 [0.365, 0.463], uniform 0.199, anti-aligned 0.144. The oracle planner reaches only ~0.66.
- Ablations: an inference-only variant (planner sees the unshaped A) loses 20 pp at alpha0 = 0.1 and 88 pp at alpha0 = 10. Need-aligned allocation stays ahead by 32-56 pp for K from 1.5 to 4.0.
- Inconsistency: policy precision is gamma = 16 in the main text and gamma = 1 in supplement A ("the planning library's default").

## License
- Paper: arXiv non-exclusive distribution licence (not CC).
- Code: MIT. Python 3.10+, JAX ≥ 0.9, `inferactively-pymdp` ≥ 1.0.2 (github infer-actively/pymdp is MIT).

## Runs on this Mac without a GPU?
Yes. The README says "A GPU is not required but substantially reduces runtime for the full sweep"; the default install is CPU JAX. A single agent is cheap; the paper's full sweep is slow on CPU. Not run.

## Verdict: watch
- For: it lines up with the brief's body variables and innate subsystems. The selector is a fixed reflex over body variables, not an emotion. Nothing is named, and nothing is rewarded except staying in range.
- Against adopting it now: it is a discrete active-inference stack (pymdp/JAX). S1's latent `h` is a learned recurrent state, so this would add a second inference engine. Reuse the idea, not the code.

## What it gives S1
- A cheap innate subsystem to add: precision routing. Each tick, pick `m* = argmax E[need_m]` over S1's body variables (contact, predictability, activity budget). Raise the gain on that variable's prediction error into `h` and its weight in action selection, within a fixed budget.
- Silence prediction: during a long silence, contact becomes the most-needed channel. With routing, the Bot's first replies on return are dominated by contact regulation. Without routing (uniform gain), the effect is diluted. This is a separate, ablatable component from the latent state itself.
- Planning matters more than perception. If routing only changes how `h` is updated and not how replies are scored, expect about half the effect, or less when priors are rigid. Route precision into the action-scoring path too.
- Failure mode (stated by the authors): if the body-state belief is miscalibrated, routing sends precision to the wrong channel. Log the belief against true `b` in S1.
