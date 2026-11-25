# Stein 2003, "Respect the Unstable" (IEEE Control Systems Magazine 23(4):12-25; the 1989 Bode Lecture)

Source read, 2026-11-25:
1. The full article PDF hosted by the IEEE Control Systems Society (ieeecss.org, "Gunter Stein IEEE_2003.pdf"). Read: the introduction, "The Punch Line" theorem, the "Bode Integrals" sidebar, "A Bode Integral Interpretation", "Available Bandwidth", "An Explanation of the Broomstick", "X-29 Limitations" and "Fact 3: Local Stability". The Chernobyl case study was skimmed.
2. Stein states the integral's conditions only informally, so the formal conditions were read in Doyle, Francis & Tannenbaum 1990, *Feedback Control Theory* (PDF posted by Francis), §6.2: the Waterbed Effect (Theorem 1), the Area Formula (Theorem 2) and the chapter notes.

Freudenberg & Looze 1985 was not read.

## Claims
- The integrals as Stein gives them (sidebar): "∫₀^∞ ln|s(jω)| dω = 0" for stable plants and "∫₀^∞ ln|s(jω)| dω = π Σ_{p∈P} Re(p)" for unstable ones.
  - They are "valid for every stabilizing controller, assuming only that both plant and controller have finite bandwidths."
  - "The constant is zero for stable plants, and it is positive for unstable ones. It becomes larger as the number of unstable poles increases and/or as the poles move farther into the right-half plane. (Technically, we must count all unstable poles here, including those in the compensator, if any.)"
- Formal condition (DFT Theorem 2): "Assume that the relative degree of L is at least 2. Then ∫₀^∞ log|S(jω)| dω = π(log e)(Σ Re pᵢ)", where "{pᵢ} denote the set of poles of L in Res > 0". DFT attributes it to Bode (1945) for stable L and to "Freudenberg and Looze (1985) in the general case."
- Stein's interpretation is a conservation law: "a certain quantity—the integrated value of the log of the magnitude of the sensitivity function—is conserved under the action of feedback." He continues: "Sensitivity improvements in one frequency range must be paid for with sensitivity deteriorations in another frequency range, and the price is higher if the plant is open-loop unstable." He names the conserved quantity "dirt" and compares the designer to a ditch digger who "moves dirt from one place to another ... but he never gets rid of any of it." He does not use the word "waterbed".
- Finite available bandwidth is what makes the law bind. Stein rejects the argument that dirt can be spread "arbitrarily thin" over infinite frequency, because "physical systems ... do not exhibit good frequency response fidelity beyond a certain bandwidth", and "the available bandwidth is always finite". The integrals then reduce to "∫₀^{Ωa} ln|s(jω)| dω = δ" (stable) and "= π Σ Re(p) + δ" (unstable), where "Only a small error (δ) occurs outside that range".
- "Waterbed" in the strict sense (DFT §6.2): "As |S| is pushed down on one frequency range, it pops up somewhere else."
  - Theorem 1 needs a right-half-plane zero: "Suppose that P has a zero at z with Rez > 0. Then there exist positive constants c1 and c2 ... such that c1 log M1 + c2 log M2 ≥ log|Sap(z)⁻¹| ≥ 0."
  - "It is emphasized that the waterbed effect applies to non-minimum-phase plants only." For a plant with no right-half-plane zeros, "for every ε > 0 and δ > 1 there exists a controller C so that the feedback system is internally stable, M1 < ε, and M2 < δ."
  - "the area formula does not itself imply a peaking phenomenon, only an area conservation". Peaking follows "when another constraint is imposed, namely, controller bandwidth".
- Numbers in the article:
  - Broomstick: "an unstable pole at √(g/L)" (the text extraction dropped the radical, which I restored). The human controller is good "up to ≈2 Hz (say, 10-15 rad/s)". The minimum achievable sensitivity "is an exponential function of the ratio of unstable pole to available bandwidth (p/Ωa)", with "a dramatic increase in sensitivity ... below a foot and a half".
  - X-29: "p = 6 rad/s", "Ωa = 40 rad/s", design point "Ω1 = 3 rad/s", "smallest sensitivity penalty is ≈ 1.75", judged marginal against "a 45°-phase margin and a 6-dB gain margin" using "PM = 2sin⁻¹(1/2smin)".
- Fact 3: "Closed-loop systems with unstable components are only locally stable", because "An unstable system cannot be stabilized globally with bounded control authority." This applies to both magnitude limits and rate limits.

## Evidence
An engineering essay that applies classical theorems (proved elsewhere) to flight-control cases (the X-29, the JAS-39 crash) and to Chernobyl. DFT supplies the proofs. All results are for linear time-invariant SISO loops.

## License
- Stein 2003: © IEEE, posted free by IEEE CSS.
- DFT: © Macmillan 1990, posted free by Francis.

No code.

## Runs on this Mac without a GPU?
Yes. |S(jω)| = |1/(1+L(jω))| is computed on a frequency grid, and the integral is checked numerically in a few lines of numpy.

## Verdict: adopt (as a hard constraint on "temperament as sensitivity placement", with the scope narrowed)
For (c):
- The conservation law makes temperament a real trade-off rather than a free parameter. A regulator that suppresses slow disturbances strongly (calm under sustained pressure) must amplify some other band (twitchy to fast events), and an unstable component, such as a self-exciting arousal mode, adds π Σ Re(p) of extra "dirt".
- This holds only under the stated conditions:
  - linear, time-invariant, SISO
  - relative degree of L at least 2
  - a finite available bandwidth Ωa, which is what forbids spreading the cost thinly
  - for a strict waterbed peak, a right-half-plane zero.
- Without these conditions, DFT shows that a minimum-phase loop can get M1 < ε with M2 < δ for any δ > 1. So the agent's regulator must have an explicit, fixed bandwidth limit, for example an update rate or actuator rate limit, for the temperament claim to follow. That limit is a design commitment, not a fact about agents.
- Nonlinear or multivariable versions were not read.
- Stein's Fact 3 also bears on (b): if the regulator includes unstable modes, its stability is only local under bounded actuation. That argues for a regulator with no open-loop unstable poles.
