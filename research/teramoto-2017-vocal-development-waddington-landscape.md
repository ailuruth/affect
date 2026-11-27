# Teramoto, Takahashi, Holmes & Ghazanfar 2017, "Vocal development in a Waddington landscape" (eLife 6:e20782, doi:10.7554/eLife.20782, PMC5310845)

Source read: the full text on PubMed Central for the introduction, results (biomechanical model, vocal-tract growth, muscle control, learning with social feedback, growth vs feedback), discussion and caveats; Materials and methods skimmed for the cost function and fitting; the appendix (biomechanical equations, diffusion process) not read.

Read for search pass 9 (a formal model of how contingent partner feedback enters the learning of the infant's own output).

## Key claims
- **Object.** A songbird-derived vocal-fold/vocal-tract model adapted to marmosets; on a one-dimensional section θ ∈ [0, 1.1] (air pressure = fold tension) the model produces cries, subharmonic phees and phees in different regions. Call probability by the maximum-entropy (softmax) rule over a cost.
- **Cost.** C(θ) = −log g(θ), g = max sound pressure / max glottal pressure (gain; louder, longer, more tonal calls cost less), motivated by the ethology (contact calls bring the parents; more tonal calls are answered more often).
- **Growth alone fails.** Vocal-tract lengthening L shifts the troughs and fits the falling dominant frequency, but no (L, temperature) fits the fast cry-to-phee transition after ≈20-30 days.
- **Muscle control.** Adding λθ (effort) rotates the landscape; a falling λ (more control) fits the phee/cry ratio.
- **Social feedback as rate.** λ_t = λ_{t−1} − κF − δ, so λ_t = λ₀ − (κF + δ)t and C_t(θ) = −log g_t(θ) + λ₀θ − δtθ − κFtθ, with F the proportion of contingent parental calls (within 5 s), κ = 0.2126 fitted, δ the feedback-independent neuromuscular maturation. F = 0 (deaf or isolated) still converges, more slowly. The fit reproduces the negative relation between F and the zero-crossing day (n = 10).
- **Feedback is not explained by infant growth or call rate:** F = b₀ + b₁W + b₂N + ε, no coefficient significant (b₁ = 0.290, p = .361; b₂ = −0.051, p = .678).
- **Caveats stated:** linear trajectories assumed; self-monitoring not included; an alternative order (muscle maturation first, feedback following) is rejected only because parental call rate and interaction strength are constant over development.

## What it means for the engine
1. **A model in which the partner sets the rate and the body sets the direction.** The direction of learning (−∂C/∂θ toward higher gain) is fixed by the infant's own vocal physics; the partner's contingency F only scales how fast the landscape tilts. In this form the end point (the phee optimum) does not depend on the partner at all; only the time to reach it does. That is the one form of partner-dependent output learning read so far whose fixed point is partner-independent.
2. **But the model averages F per infant.** The data in takahashi-fenley-ghazanfar-2016 show the parents time their responses on the infant's own fluctuations (a preferred phase), and Ghazanfar & Liao report that parents answer more-adult-like calls more. With an event-level F correlated with the infant's own variability, the same update is no longer direction-free (Proposition 3 of new-core-search-9-synthesis.md). The model is approval-closed only because of its averaging, not because of the biology.
3. **For the engine:** a partner-scaled learning rate on an own-body objective is admissible only if the scale is predictable with respect to the innovations it credits (computed before them, from a statistic that does not see them). This is the candidate examined as Direction 1 of the synthesis.

## Verdict
- **adopt (form: body-set direction, partner-set rate, as a learning rule whose fixed point is partner-independent; condition: the rate must be predictable with respect to the credited output).** Ten infants, a one-dimensional section, a linear learning term chosen by the authors; the fit does not test the averaging assumption.
