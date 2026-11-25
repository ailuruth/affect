# Riley, Richardson, Shockley & Ramenzoni 2011, "Interpersonal synergies" (Frontiers in Psychology 2:38, doi 10.3389/fpsyg.2011.00038)

Source read, 2026-11-25: full text on frontiersin.org (open access), through a fetch tool. All sections: Degrees of Freedom and Synergies (dimensional compression; reciprocal compensation), Interpersonal Synergies (manual–postural synergies; UCM analysis of rhythmic coordination), Conclusion. It is a hypothesis-and-theory article. Its two studies are summaries of other work (Ramenzoni 2008, a dissertation; Black, Riley & McCord 2007, a conference report). Neither primary was read. Sample sizes are not given in this text.

## Claims
- "Interpersonal synergies are higher-order control systems" formed by coupling movement degrees of freedom (DF) across actors. They "are emergent properties of perception–action systems", not "hard-wired features of an actor's neuromuscular system".
- Two signatures define a synergy:
  - Dimensional compression: DF that "potentially are independent" become a lower-dimensional system. It "is a necessary but insufficient condition for the existence of a synergy".
  - Reciprocal compensation, the "more critical" one: "the ability of one component of a synergy to react to changes in others". The model case is the lower lip compensating for a jaw perturbation in speech (Kelso et al. 1984).
- The rival account is that actors "execute similar but independent motor programs" anchored in shared representations. It predicts compression but not compensation: "Reciprocal compensation means that the actors' movements are not independent."
- Interpersonal coordination shows weaker coupling than intrapersonal coordination (citing Schmidt et al. 1998; Richardson et al. 2008b).
- Synergies "might be prime examples of structures of process" (interaction-dominant dynamics). The article proposes, without new data, that they "can more generally facilitate performance of social cognitive or linguistic tasks".

## Evidence
- Ramenzoni 2008, manual–postural task. One person held a circular target and the other passed a pointer through it without touching the sides. Smaller circles were harder.
  - 3-D motion of hand, forearm, arm and torso: 12 series per person.
  - PCA at a 90% variance criterion:
    - Each person alone gave six components in both conditions.
    - On the joint 24-dimensional vector, the individual-task condition gave six components and the interpersonal-task condition gave four.
    - The first component explained "significantly more variance" in the interpersonal condition (no statistic reported here).
  - CRQA showed a "significantly greater degree of coordination as well as significantly more stable coordination" in the interpersonal condition.
  - The authors' caveat: "PCA cannot provide unequivocal evidence for the existence of synergies", because it does not measure compensation.
- Black, Riley & McCord 2007, an uncontrolled-manifold (UCM) analysis of pendulum swinging.
  - Conditions: in-phase (φ ≈ 0°) or anti-phase (φ ≈ 180°), two hands of one person or one hand each of two people.
  - The performance variable was relative phase φ; the elements were each hand's position and velocity.
  - Ratio of compensated to uncompensated variance (synergy if > 1), as reported:
    | | intrapersonal | interpersonal |
    |---|---|---|
    | overall mean | 2.71 | 1.995 |
    | in-phase | 3.78 | 2.31 |
    | anti-phase | 1.64 | 1.68 |
  - Mean and SD of φ conformed to HKB predictions. No inferential statistics are given in this text.
  - The authors' reading: interpersonal synergies "were weaker than intrapersonal synergies, but nonetheless exhibited reciprocal compensation and dimensional compression".

## Formal models
- No equations beyond the UCM illustration "Force_finger1 + Force_finger2 = 10 N".
- The UCM criterion: a synergy exists if the ratio of variance in the null space of the task Jacobian (compensated) to variance orthogonal to it (uncompensated) exceeds 1. "A ratio ≤ 1 means the synergy does not exist."
- HKB is invoked but not written (see kelso-2009-virtual-partner-interaction.md for the equations).

## What it implies for a dyadic affective core
- **The test of coupling is compensation, not similarity.** A synergy is diagnosed when partner A's deviation is absorbed by partner B's opposite deviation, so that a shared task variable stays fixed. That is a negative covariance between partners on the task null space.
  - A single gain that pulls the agent toward the partner's state produces positive covariance (copying), not compensation.
  - The UCM ratio is a concrete, computable alternative to correlation-based synchrony scores. It needs a declared task variable, for example a shared affective quantity of the dyad.
- **The coupling depends on the task variable.** The same two people show different compensation ratios for in-phase and anti-phase goals (2.31 vs 1.68 interpersonally). The coupling is therefore defined relative to the goal, not by a fixed partner-to-self gain.
- **The structure is in what is held constant.** One gain has no notion of "the variable the dyad stabilizes". A synergy model needs a task manifold, and the partner's influence is projected onto its orthogonal complement.
- **Not shown:**
  - Nothing about affect, faces or voices.
  - Both studies are summarized without n or inferential tests.
  - PCA compression is admitted not to establish a synergy.
  - Interpersonal synergies are reported as weaker than intrapersonal ones, not of a different kind.
  - Role asymmetry (holder vs pointer) existed in the task but was not analyzed.

## Verdict: adopt (as a measurement concept), watch (as evidence)
- Adopt the UCM compensated/uncompensated variance ratio as an E-class analysis of whether the Bot and the person form a synergy on a declared dyadic variable. It separates compensation from copying, which windowed cross-correlation cannot.
- The evidence here is thin: secondary summaries, no n, no tests.
- This fits Principle 3 only if "read through one's own body" includes compensating, not just mirroring.
