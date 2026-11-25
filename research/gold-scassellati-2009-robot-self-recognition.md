# Gold & Scassellati 2009, "Using probabilistic reasoning over time to self-recognize"

Robotics and Autonomous Systems 57(4):384-392, doi:10.1016/j.robot.2008.07.006. Sections 2-4 appeared earlier as "A Bayesian robot that distinguishes 'self' from 'other'" (CogSci 2007).

Source read: the authors' preprint ("Preprint submitted to Elsevier, 1 August 2008", 23 pages) from the Yale Social Robotics Lab site (scazlab.yale.edu/sites/default/files/files/Gold-RAS-08.pdf), read in full, including figures, captions and references. The published journal version was not read; page layout and minor wording may differ.

## Claims
- A robot can learn which visual objects are its own motor-controlled parts (including its mirror image) from motion timing alone, with no model of appearance or kinematics, by comparing three dynamic Bayesian models per tracked object at every frame: "self", "animate other", "inanimate".
- The "animate other" model is the robot's own self model with the motor variable made hidden. Self and other share one model; what differs is whether the motor cause is observed (one's own efference) or must be inferred.
- Because the forward algorithm carries the whole history of each object, evidence that an object once moved without the robot's motor command persists. A person who walks in and then mirrors the robot stays "other".
- A person who mirrors the robot from the moment it starts is ambiguous to the robot. The authors call this reasonable: "anything that the robot can control so effectively, probably may as well be classified as 'self' until some evidence is acquired to the contrary."
- Speculative: self-recognition by this route needs an action-recognition model of others (the hidden-state inference), so a species that can self-recognize should be able to imitate.

## Mechanism (equations as given)
Boolean events per frame: object motion M_t ∈ {m, ¬m}; own motor activity Φ_t ∈ {φ, ¬φ}.
- Inanimate: one parameter P(r), the chance of spurious motion per frame; frames independent.
- Self: λσ_t = ∏_t P(M_t | Φ_t), with P(M_t|Φ_t) taken from two learned parameters P(m|φ) and P(m|¬φ) (they need not sum to 1). Update in constant time: λσ_{t+1} = P(M_{t+1}|Φ_{t+1}) λσ_t. Motor-to-motor arrows do not matter because Φ is observed.
- Animate other: the same emission model with Φ hidden (an HMM). Forward algorithm: λω_{t+1} = Σ_{Φ_{t+1}} P(M_{t+1}|Φ_{t+1}) Σ_{Φ_t} P(Φ_{t+1}|Φ_t) P(Φ_t). The emission probabilities are copied from the self model. The transition probabilities P(φ_{t+1}|¬φ_t), P(¬φ_{t+1}|φ_t) are counted from the robot's own motor transitions ("objects in motion tend to stay in motion").
- Posterior: P_t(self) = λσ_t / (λσ_t + λω_t + λν_t), times class priors P(inanimate) = 0.8, P(self) = P(other) = 0.1. Normalized likelihoods are propagated to avoid underflow.
- Online learning (a running, non-revisiting EM): P(r) = Σ_it P_it(inanimate) M_it / Σ_it P_it(inanimate); P(m|φ) = Σ_it P_it(self) M_it Φ_t / Σ_it P_it(self) Φ_t; P(m|¬φ) = Σ_it P_it(self) M_it (1−Φ_t) / Σ_it P_it(self)(1−Φ_t). Each observation is weighted by the current belief that the object belongs to that class.
- Contingency is same-frame: Φ_t explains M_t. No lag parameter. The authors attribute dips in P(self) to the motor-to-visible-motion lag.

## Evidence with numbers
- Robot Nico (upper torso, one-year-old kinematics), 3 arm DOF used; 320×240 at about 30 fps, background subtraction, classification at about 9 fps (8.3 Hz in the adversarial runs). The arm made about 1-s sweeps to random extremal positions every 5 s.
- Learning: 4 min, parameters started at the implausible value 0.5 with the weight of 30 virtual observations, with distractors (lights, students passing). After 4 min across 20 runs: P(r) ≈ 0.020, P(m|φ) ≈ 0.73, P(m|¬φ) ≈ 0.11 (95% CIs in Fig. 6). That motion is more likely during motor activity was learned, not given.
- Test with parameters frozen: the mirror image was classified "self" after one complete arm motion and stayed so. The experimenter (sitting, drinking, juggling) was "animate other" within about 2 s and stayed so, in all 20 runs.
- Adversarial, mimic from switch-on (10 runs): P(self) > 0.5 at some point in 9 of 10 runs. The robot stayed mostly uncertain: for half the minute the upper 95% CI of P(self) was below 0.5. Human reaction lag of hundreds of ms was not enough to rule out "self" at this frame rate.
- Adversarial, 5 s walk-on then mimic for 55 s or more (5 runs): P(self) stayed below 0.1 for the first 30 s in all runs; it exceeded 0.5 in only 2 of 5 runs, late. In the other 3, P(animate other) stayed near 1 throughout.
- Caveats from the authors: only the arm can be recognized (background subtraction hides the static body); the usefulness of the "inanimate" class is unclear; the structure of the models is given, not learned.

## What it implies for an engine learning a partner model and its self–other face map from live contingency
- The confound in critique-design-dyadic-sheaf.md (C13) has an exact mirror here: a partner who perfectly follows the agent is indistinguishable from the agent's own effect. Contingency alone cannot tell "it follows me" from "I control it" when the only variation is the agent's. What separates them is variation the agent did not cause: the walk-on segment, where the partner moved with Φ = ¬φ. For the engine the converse holds too. To learn that the partner responds to it, it needs its own variation that the partner did not cause (spontaneous acts, not its following).
- Use likelihood comparison of whole histories, not a windowed regression. Keep, per partner channel, competing generative hypotheses: "partner moves on its own (hidden-state HMM)", "partner responds to my efference", "my state follows the partner". Each is scored by the forward algorithm over the whole session, so early evidence of independence is not washed out by a later run of mimicry. This is a direct template for a contingency estimator that does not self-reinforce.
- Make the "other" model the self model with the cause hidden. This is the same structure as associative sequence learning plus inference of the partner's hidden state. It ties self–other mapping to action recognition. It fits the project's "one sign map expresses and reads" commitment, and the authors' speculation that self-recognition implies imitation.
- Condition on efference, not on the agent's sensed face. The self model conditions on Φ, the motor command the robot knows it issued. The engine's equivalent is an efference record of its own expression commands, kept apart from what it sees of itself. A rule that regresses on the agent's own state trace (which already contains its following of the partner) loses this.
- Lag matters at fine scale. Same-frame contingency at 9 Hz could not reject a human mimic lagging by hundreds of ms. The engine should model the response lag explicitly (see stoytchev-2011-self-detection-temporal-contingency.md).
- Weighting each observation by the current class posterior (running EM) can lock in an early misclassification. Here it worked from bad priors, but the parameters were learned in a 4-min solo phase before any partner. An engine learning in live interaction has no solo phase, so it should freeze or anchor its self-model timing from periods when the partner is absent or still.

## License
Elsevier journal article, all rights reserved; author preprint hosted by the lab. No code released.

## Runs on this Mac without a GPU?
Yes, trivially: per object two multiplications and a two-state forward step per frame.

## Verdict: adopt (as the estimator template for "self / responds-to-me / independent other" by whole-history likelihood comparison; and as the clearest demonstration that a follower is unidentifiable without independent variation)
Single robot, Boolean motion, 20 + 10 + 5 runs; engineering result, not a model of infants (the authors say so).
