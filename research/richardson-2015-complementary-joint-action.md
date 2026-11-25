# Richardson, Harrison, Kallen, Walton, Eiler, Saltzman & Schmidt 2015, "Self-organized complementary joint action: Behavioral dynamics of an interpersonal collision-avoidance task" (JEP: Human Perception and Performance 41(3):665-679, doi 10.1037/xhp0000041)

Source read, 2026-11-25: author manuscript on PMC (PMC4801327), through a fetch tool, characters 0-100k of 129k. That covers the Introduction, Method, Results (frequency, ellipticality δ, relative phase, coupling directionality), Dynamical Modeling, Discussion and Table 1. The last 29k characters, mostly references, were not read. The equations were reconstructed from garbled text by the fetch tool, so the symbols are reliable but the typesetting is not.

## Claims
- Most coordination-dynamics work studies in-phase and anti-phase rhythmic patterns. The question here is whether the same dynamics organize goal-directed complementary joint action.
- The task builds in "a conflict between the natural attraction toward synchronizing their movements' inphase" and avoiding collisions.
- Pairs "quickly converged onto a stable, asymmetric pattern of movement coordination", with one more elliptical path, one straighter path, and a phase lag. That asymmetry "was essential to task success".
- The roles were emergent: one participant became "phase leader" and the other "phase follower". "Most participants were not aware of the role they played." Pairs imposed "a differential 'leader–follower' type solution".
- The asymmetry is attributed to "participant-specific differences" in the coupling and repeller functions. It is framed as a symmetry break, comparable to frequency detuning in bimanual coordination. "There also appeared to be an asymmetry in coupling strength between coactors."
- The organization "emerged over trials and was determined by the dynamics of trial outcomes".

## Evidence
- **Design.** 12 pairs of right-handed undergraduates, sitting back to back. Each moved a dot on a 50-inch monitor between diagonally opposed targets; each saw both dots.
  - Polhemus tracking at 60 Hz.
  - No talking and no instruction about the form of coordination.
  - 15 points needed to finish.
  - One pair was dropped, leaving 11 pairs and 164 successful trials.
- **Learning.** A mean of 21 trials to reach 15 points (range 15-36, median 19). Most failures came in the first 20 s of a trial.
- **Frequency** rose from ~0.4 Hz to ~0.58 Hz: F(2,20) = 47.22, p < .01, ηp² = .83.
- **Ellipticality δ** rose over blocks: F(2,20) = 8.40, p < .01, ηp² = .47.
  - The difference between partners, Δδ, was marginal across blocks: F(2,20) = 3.02, p = .07.
  - Trial 1 vs trial 8: F(2,20) = 4.55, p < .05.
- **Relative phase.** The distribution peaked at about −30°; most pairs settled between ~10° and 40° of lag. The more elliptical partner lagged the straighter one.
- **Coupling directionality** d(pE,pS), by the evolution-map method of Rosenblum & Pikovsky 2001, was "slightly positive" on every trial and above zero on average: t(10) = 3.46, p < .01. It did not change across blocks (F < 1). The mean is shown only in a figure.
  - The straighter partner drove the elliptical one, but the effect is "by no means large".
- **Correlation of Δδ with d,** by block: r = .08, .37 and .85 (first, middle, last). Only the last block was significant (p < .05).
- **Role stability (Table 1).**
  - In 9 of 11 pairs, role differentiation stayed constant or grew.
  - Pairs 7 and 10 swapped roles (40/60% and 53/47%).
  - In pairs 1, 2, 6 and 12, the same person was the more elliptical one in 100% of trials.
- **Collisions after differentiation:** at most 5 in 9 of 11 pairs; the other two pairs had 6 and 15.

## Formal models
Task-dynamic model (eqs. 1-5). For each participant i, x is the main movement axis and y the orthogonal axis:

ẍ₁ − b_x1 ẋ₁ + c_x1 x₁² ẋ₁ + k_x1 x₁ = α_x1(ẋ₂ − ẋ₁) − γ_x1 (x₁ + y₂) e^{−|x₁ + y₂|}
ÿ₁ + b_y1 ẏ₁ + k_y1 y₁ = γ_y1 (y₁ − x₂) e^{−|y₁ − x₂|}
ẍ₂ − b_x2 ẋ₂ + c_x2 x₂² ẋ₂ + k_x2 x₂ = α_x2(ẋ₁ − ẋ₂) + γ_x2 (x₂ − y₁) e^{−|x₂ − y₁|}
ÿ₂ + b_y2 ẏ₂ + k_y2 y₂ = −γ_y2 (y₂ + x₁) e^{−|y₂ + x₁|}

- The main axis is a van der Pol limit cycle; the orthogonal axis is a damped point attractor.
- α is linear dissipative coupling between the main axes. HKB coupling was deliberately left out because in-phase vs anti-phase is arbitrary in this task.
- γ are participant-specific repellers that decay exponentially with the projected distance to the other's dot.
- Simulation values: b_x = 1, b_y = 2, k = 2π, c_x = .5, α = .5, γ ∈ {0, 7.5, 15, 20}, noise SD = 5.
- Equal γ gives symmetric ellipses and zero lag. Unequal γ gives the observed asymmetric ellipses and lag.
- These are qualitative simulations, not fits to data.

## What it implies for a dyadic affective core
- **Complementarity is two kinds of coupling.**
  - The model has an attractive term (α, pulling toward synchrony) and a repulsive, state-dependent term (γ, pushing away from the partner's position along a different axis).
  - Success requires the repeller. A one-gain attraction model would collide every time, which is the motor analogue of copying the partner.
- **Roles come from asymmetric parameters, and they persist.**
  - The leader-follower split appeared from unequal γ, with no instruction.
  - It was stable within most pairs (the same person elliptical in 100% of trials in 4 of 11 pairs) yet could swap (2 pairs).
  - A dyadic core needs partner-specific, possibly learned, asymmetric coupling: its role with this partner.
  - The rise of the Δδ-d correlation from .08 to .85 shows the role structure forming across trials. That is a slower time scale than within-trial coordination.
- **The partner's influence is axis-specific.** Attraction acts on the main axis, repulsion on both. The agent responds to the partner in different ways in different dimensions, which a single scalar cannot express.
- **Not shown:**
  - No affect, face or voice; one task, 11 pairs, undergraduates only.
  - The coupling asymmetry is small, and attention differences were not ruled out.
  - The γ asymmetry is inferred from simulations, not estimated.
  - Whether the change was a bifurcation in a control parameter or a structural change is left open.

## Verdict: adopt (as the formal template for complementarity), watch (as evidence)
- Adopt the attractor-plus-repeller form, an attractive α on some dimensions plus a partner-relative repulsive γ on others, with participant-specific parameters. It is the smallest model in which complementary, role-differentiated coordination emerges without instruction, and the γ asymmetry is an ablatable component (Principle 5).
- The evidence is from one motor task with a small sample and weak directionality effects.
