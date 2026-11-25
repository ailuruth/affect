# Hoffman & Breazeal 2007, "Cost-based anticipatory action selection for human–robot fluency"

Guy Hoffman and Cynthia Breazeal, *IEEE Transactions on Robotics* 23(5):952–961, October 2007, doi:10.1109/TRO.2007.907483. This is the journal version of the HRI 2007 paper "Effects of anticipatory action on human-robot teamwork efficiency, fluency, and perception of team". Its abstract and study design match, and it adds the cost analysis.

Source read: the published IEEE PDF, hosted on the author's lab site (hrc2.github.io/assets/pdfs/papers/HoffmanBreazealTRO07.pdf), all 10 pages, read in full including Table I (read from the page image). The HRI 2007 conference paper itself was not reachable as an open copy and was not read. The later perceptual-simulation papers (AAAI 2008; HRI 2010 "Effects of anticipatory perceptual simulation on practiced human-robot tasks") were not read.

## Claims
- A robot teammate that learns a model of the human's habits and acts in anticipation, weighing confidence against the cost of being wrong, makes a joint task more efficient than a purely reactive robot. People also rate it as contributing more, as more committed and as more fluent.
- Fluency is separate from task time. Perceived fluency differed strongly between conditions, while mean task time did not differ significantly.
- Three candidate objective fluency measures are proposed: concurrent motion, human idle time and functional delay (the time from the human's act to the robot's response).

## Mechanism (as given)
- **World**: a deterministic, discrete-time process with two agents. The full state is s = ⟨s^w, s^h, s^r⟩ (workspace, human, robot), with |Σ| = 2,160,900 in the factory task. Actions take time: a transition s_k → s_l costs d(s_k, s_l) frames, and the agent can act again only after that delay. The robot perceives the workbench only when it is at the workbench.
- **Task**: build carts (Body, Floor, 2 Axles, 4 Wheels). The human brings parts; the robot fetches and applies the matching tool (welder, rivet gun, two wrenches) through a lookup function Φ(workbench) → tool.
- **Reactive baselines**:
  - Naive: return each tool after use, which costs 6d + 5 when the same tool is needed twice.
  - "Conservative tool return": hold the tool until the workbench changes, at cost 2d + 3 + δ, where δ = max(0, h − (2d + 2)).
- **Learned model**: a first-order Markov model of which tool the next workbench state will need. Transition counts use a Laplace correction: p_{x|j} = (n_{x|j} + 1) / Σ_k (n_{k|j} + 1). There is no discounting, and the model persists only within the session.
- **Action selection**: at the workbench the robot computes the expected duration cost of four "protosequences" and picks the cheapest:
  1. fetch tool x and use it;
  2. return the held tool;
  3. swap to tool y and use it;
  4. wait.

  For example, Cost1(x) = p_{x|j}(2d_{0x} + 2) + Σ_{y≠x} p_{y|j}(3d_{0x} + d_{xy} + d_{0y} + 4), and the wait costs carry "+ h". Here h, the estimated human turnaround time, is a hand-set risk parameter: low h gives the risk-averse reactive policy, high h acts on the first trial. The reactive policies are special cases of this selection rule.

## Evidence with numbers
- **Simulation** (h = 250, consistent simulated human): the robot overtakes the reactive agents within about 2 trials and is fully anticipatory within about 10. Against a human who is 70/30 inconsistent, waiting stays optimal for 12 trials. Under h = 100, the correct anticipation comes at trial 16 instead of trial 5. In a pilot with one expert human, per-cart cost fell from about 800 (reactive) to about 650 frames.
- **Human study**: 32 MIT participants (15 female) in a simulated factory game, between subjects; 27 were analyzed (A reactive n = 14, B anticipatory n = 13). Cost is in frames at 30 fps (Table I):
  - Best cart: A 1091.6 ± 200.5, B 930.1 ± 105.6; T(25) = 2.59, p < 0.02.
  - Mean over 10 carts: A 1423.5 ± 328.6, B 1233.3 ± 227.5; T(25) = 1.73, not significant.
  - Tenth cart: A 1182.4 ± 274.3, B 1030.7 ± 154.8; T(25) = 1.75, not significant.
- **Survey** (7-point Likert, all 32): rows below are A versus B.

  | Item | A | B | Test |
  |---|---|---|---|
  | Robot contributed to success | 4.88 | 6.38 | T(30) = 2.87, p < 0.01 |
  | Robot contributed to fluency | 4.13 | 5.69 | T(30) = 2.99, p < 0.01 |
  | Robot committed to the team | 2.8 | 5.0 | T(30) = 3.21, p < 0.005 |
  | Own commitment; trust in the robot | 6–7 | 6–7 | no difference |

- **Post-hoc fluency measures** (A versus B):
  - Concurrent motion: 0.227 versus 0.322 of frames, T(25) = 3.11, p < 0.005.
  - Human idle time: no difference.
  - Functional delay (human PutDown to robot Use): 436.78 versus 310.64 frames, T(25) = 5.04, p < 0.001. In the second half of trials it was 432.07 versus 205.08, T(25) = 6.28, p < 0.001. The reactive robot's delay did not change across trials.
- **Qualitative**: many reactive-condition subjects, uninformed, complained that the robot did not anticipate them. They called it "a tool", not a team member. In the anticipatory condition, subjects who noticed the adaptation began experimenting to probe it, which slowed the model's convergence. The authors also blame the on-screen best-score display for inducing strategy changes.

## Failure modes (reported or evident)
- **No affect at all.** This is a timing-and-prediction architecture. It is included here because it is the clearest controlled demonstration that anticipation, not reaction, is what people read as commitment and fluency.
- **Hand-structured task model.** Φ, the four protosequences, the cost formulas and h are all given. Only the transition counts are learned. The authors list as future work separating the effect of learning the transitions from the effect of the cost analysis; they did not ablate the two parts.
- **Ablation, partly.** The between-subjects comparison of reactive and anticipatory agents is a real lesion of anticipation, and it was preregistered in the sense that the predictions were stated before the study. The efficiency prediction failed on the mean and last-trial measures. The fluency measures were chosen post hoc.
- **The partner adapts to the adapter.** Once subjects noticed the robot learning, they changed strategy to probe it, which made their behavior less stationary and slowed the robot's learning. A first-order count model with no discounting cannot follow this. The authors propose recency discounting.
- **Simulated robot, game setting, one session, no persistence.**

## License
IEEE article; the author's copy is hosted on the lab site. No code released.

## Runs on this Mac without a GPU?
Yes, trivially: count tables and a handful of expected-cost sums.

## Verdict: watch (adopt the fluency measures and the result, not the architecture)
The architecture is a task planner with nothing affective in it. Two things are worth keeping:
- **The result.** With task time held roughly equal, an agent that acts on its expectation of the partner is perceived as more committed and more fluent. The objective measure that tracks this best is functional delay, not idle time.
- **The measures** (concurrent motion, functional delay), carried over to face and voice timing: the lag from the user's expression to the Bot's response, and the fraction of time both faces are moving.

## What it implies for this engine
- **Anticipation is the visible signature of a partner model.** People read the robot's commitment from when it acted, not from what it did. For the engine, the timing of the face (expression before or with the partner's, not after) is evidence of an internal model of the other. It should be measured as functional delay that shrinks with familiarity, which a reactive mimic cannot produce. This matches the Keepon authors' point that a purely reactive system cannot be in phase (see kozima-2009-keepon.md) and the strong-anticipation literature (stepp-turvey-2010-strong-anticipation.md).
- **An ablation prediction for the S6 relationship claim.** With the operator-specific partner model removed, the Bot's response latency to the operator's habitual expressions should stay flat across days instead of falling. The result here suggests the operator would notice.
- **Partner nonstationarity is real and partly caused by the agent.** Users change behavior once they notice adaptation. A learned self–other map or partner model must use recency weighting or a hierarchical prior. It must also treat the user's reaction to its own adaptation as part of the dyad, not as noise.
- **Not to copy**: the hand-given task structure and the hand-set risk parameter h. In the engine, the cost of waiting versus acting early should follow from the core's objective (expected change in the regulated variables), not from a tuned constant.
