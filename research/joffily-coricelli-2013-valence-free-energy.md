# Emotional valence and the free-energy principle (Joffily & Coricelli)

Mateus Joffily & Giorgio Coricelli, *PLoS Computational Biology* 9(6):e1003094, 2013, doi:10.1371/journal.pcbi.1003094 (PMC3681730).

## What was read
The full text from PMC: abstract, author summary, introduction, Models (free-energy principle, valence, basic forms of emotion, emotional regulation of uncertainty), Results (dynamic vs static perceptual models, reference scenario, factive vs epistemic uncertainty) and the Discussion. PMC rendered the equations as images, so the key ones (Eqs. 4, 5, 20) were read from the PLOS equation images. Figures not seen; Table 1's sign columns were partly lost in extraction and are reconstructed from the text.

## Findings / the computation, precisely

**Valence is a rate, not a level.** "we formally define the valence of a state visited by an agent at time t as the negative first time-derivative of free-energy at that state", per level i of a hierarchical model: valence_i = −dF_i/dt. In discrete time (Eq. 20) ∇F_i^(k) = F_i^(k) − F_i^(k−1). "when free-energy is constant ... neutral valenced states may also be characterized by low or high levels of surprise."

**Second derivative splits emotion forms.** With F′ and F″:
- F′ < 0, F″ < 0 (falling faster): hope; F′ < 0, F″ > 0 (falling slower): happiness;
- F′ > 0, F″ > 0: fear; F′ > 0, F″ < 0: unhappiness;
- F′ crossing from − to +: disappointment; from + to −: relief.

"transitions from negative to positive emotions can only occur by passing through relief, and transitions from positive to negative emotions can only occur by passing through disappointment".

**Valence sets learning rate (Eq. 4).** ln σ̂_i(t) = ln σ_i(t) + λ·F′_i(t) − τ, with σ_i = argmin F_i (Eq. 5). "positive and negative valence exponentially decreases and increases, respectively, the estimation uncertainty". λ is "sensitiveness" to valence; τ is a constant offset the authors call **mood**: "In a negative mood (τ < 0), the agent overweights recent inputs ... In a positive mood (τ > 0), the agent overweight past inputs".

**Simulation.** A one-armed bandit, 320 trials: 100 at p = 0.5, then 120 alternating 0.9/0.1 every 20 trials, then the first 100 repeated. The static model with valence (2 states, 2 parameters) tracked volatility like the Mathys et al. hierarchical model (3 states, 3 parameters) and, unlike it, returned to a stable baseline in the last stage. λ = 0.8 makes it track fast changes; τ = −0.13 alone tracks volatility. With λ = 0.4, τ = −0.13 over 100 runs, posterior variance after epistemic (hope/fear) events exceeded factive (happy/unhappy) ones: low volatility 0.68 vs 0.58, high 1.07 vs 0.69.

**The reunion example, in the authors' words.** An old friend appears at the door: low-level physical expectations are violated (negative valence there), while "this same sensation should also fulfil more abstract expectations that we might have of being close to beloved ones", giving positive valence at a higher level: "'we are surprised about the unexpected visit of a friend but happy to be close to a beloved one'." And "When the state under consideration is the fate of another person, this can be understood as a specific form of happiness ... usually known as 'joy for another'". They link value to Keramati & Gutkin's homeostatic RL: value as the complement of free energy, valence as its rate.

**Admitted weak points.** The meta-learning rule "may appear a bit ad hoc"; flexibility over generative models raises falsifiability concerns; F″ has no clear psychological reading.

## What it means for the designs
- **The direct answer to "no positive affect".** In the Cayley ledger the objective is 𝒟 ≥ 0 with a dead-band, so good news leaves J at 0. Take valence as v = −d𝒟_total/dt (or the sum of −dD_i/dt over the agent's own drives, C and a new contact deficit K included). Good news that lowers C, or a reunion that lowers K, then gives a positive transient even though J ends at 0. Positive affect exists only while a deficit is being relieved.
- **Satiable by construction.** For any interval, ∫ v dt = 𝒟(t₀) − 𝒟(t₁) ≤ 𝒟(t₀). Total positive affect is bounded by the deficit that existed; it cannot be farmed without first letting a deficit rebuild, and Keramati & Gutkin's discounting result (keramati-gutkin-2014-homeostatic-rl.md) makes letting it rebuild a net loss. This is the cleanest available form of a "satiable positive drive": it is not a new drive at all, it is the sign of change of the existing ones.
- **Show it on the face via the rate, not a named variable.** The innate display prior Π₀ already reflexes "on the rise and fall of 𝒟" (§3.13 of the design); this paper supplies the reading: fall = positive, and the F′/F″ quadrant gives a relief-shaped onset (fast) versus a settled, slower contentment. No "joy" variable is named.
- **"Joy for another" without rewarding the partner's smile.** Put the partner's situation as a level in the agent's model whose free energy is the agent's own concern C = 𝒟(b̂_p). News that the partner's situation resolved lowers C, so v > 0. The agent cannot raise v by making the partner *look* better unless that also lowers C, which is K3's hazard (critique-2): keep b̂_p's lexical/appraisal channel (what happened) the main evidence for news, and keep the action-blind partner model so no rollout values changing the partner's display.
- **Valence → learning rate is a second consequence worth testing.** After good news, the agent's per-partner slow state should update more slowly (consolidate), after bad news faster. That is a measurable asymmetry, testable by lesioning λ.
- **Limits.** One toy simulation; F″ categories are labels on quadrants; valence as rate predicts no positive affect from a stable good state, which fits a satiable design but not tonic contentment — the positivity offset (fredrickson-2001-broaden-and-build.md) would have to be a set-point display, separately.
