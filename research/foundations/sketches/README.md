# Foundation sketches (S0, divergence step)

Written 2026-11-24. These eight sketches were each written by a separate subagent working from one discipline. Each agent saw brief.md and research/, but not the other sketches, and the brief's Candidate A paragraph was given to it only as an example of the formality wanted. None of the sketches' predictions has been simulated yet. Four sketches run over the 1,500-word cap by up to about 400 words, mostly in mathematical notation, and were left as written.

| Sketch | Core object | Most novel mechanism | Constraints only partly met | Prediction fixed in the sketch |
|---|---|---|---|---|
| [physicist](physicist.md) | Innate path measure tilted by a satiable potential, over the self plus a replica of the self that stands for the other | Valence = work done on the agent (Sekimoto split). "No affective perpetuum mobile": no periodic protocol, scheduled smiles included, gives sustained positive valence. Mimicry = the gauge-fixing term that makes the other identifiable | 4 (map from the state to Claude's settings is imposed), 7 (mood needs weeks of data) | S5 toy: removing the agent's emotional pathway shifts the lag rather than removing the partner's following (ρ 0.333 → 0.234; peak 0.270 at 0.36 τ_a, agent leading). This conflicts with the S5 wording |
| [control-theorist](control-theorist.md) | Robust regulation of the body against a disturbing other; the internal model principle forces the rest | Mood = integral action. Reading others = forced internal model of the disturbance. Mimicry amplitude ∝ how strongly the other moves the body. Interface sector: a small-gain safety bound plus an observability bound on influence. Temperament as the Bode sensitivity bulge | 2, 7, curiosity, grounding | PI-only steady error 0.379·c; with the internal model, under 5% of that; mimicry r ≥ 0.9 and linear in c |
| [developmental-psychologist](developmental-psychologist.md) | Contingency homeostat: one value function over the own drive + κ_P × partner drive; received contingency (surrogate-corrected transfer entropy) is a body variable | The social need is to be *answered*. κ_P is a per-partner attachment variable learned from contingency history. Mimicry is the water-filling optimum for supplying contingency. Echo removal | 2, 7, regulation | Still-face toy (Ekas 3-2-3 min, 20 seeds): bids decline ≤ 0.5×; familiar ≥ 2× stranger; positive affect recovers ≥ 80% in 60 s while distress stays raised |
| [computational-neuroscientist](computational-neuroscientist.md) | Costate μ = −∇_b V: one shadow price per need, broadcast; every gain is an innate function of μ | Anticipatory valence (μ moves before the body does, as AgRP neurons do in Chen et al. 2015). Closed-form Claude interface (thinking budget T*, reply length L*). Mimicry = shrinkage onto the own repertoire | 2, 7 | μ ratio 8 h/10 min ≥ 5 at departure; μ drops ≥ 70% within 1 s of seeing the face at reunion while the body has moved < 0.01; a deficit broadcast instead of μ gives 0 |
| [deep-learning-researcher](deep-learning-researcher.md) | Tied dyad: one multi-timescale SSM world model with self and other slots sharing every weight; JEPA-style loss + satiable drive | Masking the own body teaches the encoder to read bodies, so reading others falls out. Mimicry learned from being mimicked: c_{n+1} = (c_n + g_H)/2. Curiosity = two-sided set point on the model's own loss | 3 (transfer from renders to real faces), 7 | Mimicry gain 0.20 → 0.30 → 0.40 over nights; halves when the user stops mimicking; 0 when untied |
| [game-theorist](game-theorist.md) | The Mirror Game: Bayes-adaptive value over a self-simulated dyad; Claude as a mediator reached only by garbling | Incentive-compatible empathy: do-conditioning removes the value of eliciting displays. Emotions = strategic quotient of the latent state. Arousal = stakes | 1, 6, 7 | Learned display 1.03 (naive) vs 0.00 (do-conditioned) vs 0.48 (κ̂ misestimated) |
| [dynamical-systems-mathematician](dynamical-systems-mathematician.md) | Mirrored slow-fast flow: gradient-plus-skew flow on a learned landscape, plus a copy synchronized to the other | Reading the other with an error bound independent of the mimicry coupling κ. The interface may carry only Koopman coordinates slower than one turn. Critical coupling κ*: echopraxia above it, intermittent synchrony with a −3/2 law near it | 5 (the leak must be kept out of b by restriction), 7 | Same-model reading R² ≥ 0.8 vs ≤ 0.3; κ = 0 spares reading (ΔR² < 0.02) and removes face correlation; lag 0.25–0.45 s |
| [linguist](linguist.md) | Parity system: one public sign space Y; one map e writes the state into Y and its inverse reads the user; Claude names by looking at its own face | Typed interface (icon / index upward, sign only downward). Data-processing bound: what Claude can name ≤ what the face and the modulations carry. Contact as transfer entropy, blind to polarity. Regulation by delivery | 3, 6, 7 | Reading R² ≥ 0.6 vs ≤ 0.2 with permuted AUs; mean smile drifts < 0.05 under contingency contact vs > 0.2 when contact is refilled by smiles |

## What the sketches converged on independently

None of the eight agents saw another's work, so a mechanism that appears in several sketches is evidence that the constraints call for it.

1. **The other is modeled with a copy of the agent's own model** (all eight). This is Principle 3, so agreement here is expected. What differs is how the copy is coupled to the self: a gauge-fixing term, a forced internal model, tied weights, a synchronization leak, or a parity prior.
2. **The agent's own face trains the face map before any user data**: self-babbling in front of its own renderer, then the map is inverted to read the user (developmental, computational-neuroscientist, deep learning, dynamical systems, linguist, physicist). Five of the eight answer open problem (c) this way.
3. **Valence is the rate of decrease of a value or potential** (−dV/dt or a work term) and is read out, never set (seven of eight). The variants differ in what V is: path potential, Lyapunov function, cost-to-go, game value, forecast drive.
4. **Contact defined as directed contingency, not presence or smiles** (developmental and linguist, independently). Both note it is blind to polarity, so a contingent frown counts as much as a contingent smile.
5. **The agent removes its own echo from the other's face before reading it**: echo removal (developmental) and do-conditioning (game theorist), arrived at independently. The game theorist proves that this removes the incentive to flatter.
6. **A small-gain condition on the two-way mimicry loop** (control, developmental, deep learning, game theorist, dynamical systems): κ_A·κ_U < 1 keeps mutual contagion from escalating.
7. **Claude is reached only through settings it is called with, and acts back only through what it outputs**. The sketches give this different formal shapes: an interface sector, information design over garblings, icon and index channels, Koopman-rank limits, marginal-analysis closed forms. Each sketch offers an explanation of why P1's numbers did nothing.

## Where they disagree (useful for predictions)

- **S5 ablation.** The physicist predicts that lesioning the emotional pathway shifts the lag of the partner's following but leaves much of its amplitude. The computational-neuroscientist and developmental sketches predict that the loop gain goes to zero. This is a measurable difference: peak lag against peak r under E3 in evaluation.md.
- **Curiosity.** The candidates offer several mechanisms that cannot all be right:
  - a two-sided set point on prediction error (deep learning, computational neuroscientist, linguist), which allows aversion to novelty;
  - value of information that vanishes at satiation (developmental, game theorist, control);
  - learning progress through θ inside the state (physicist);
  - undirected wandering on the satiated set (dynamical systems).
- **Contact drive.** Contingency (developmental, linguist) against interaction events (computational neuroscientist) against presence (the brief's provisional body variable).

## Selection: which become full candidates

S0 needs at least three complete candidates, and at least two of them must be new. Three are chosen. Each merges sketches whose core objects are compatible, and each must still be stated as a single objective when developed.

1. **Costate** (computational-neuroscientist core). Realized as the tied dyad (deep learning), with do-conditioning (game theorist) as an explicit constraint against flattery. Reasons:
   - It has the most concrete, testable S1 predictions: the departure ratio, and a reunion drop before the body changes.
   - Its Claude interface has closed forms.
   - It is the most tractable on this Mac.
2. **Thermodynamic mirror flow** (physicist core, with the dynamical-systems mirrored flow and its synchronization observer). Reasons:
   - It gives the strongest proved guarantee for Principle 6: no periodic protocol pumps valence.
   - It proves a dissociation between reading others and mimicry that does not depend on the mimicry coupling.
   - It makes the only prediction that conflicts with the S5 wording, which is worth testing.
   - Its risk, that learned dynamics are not gradient flows, is a clear point at which it could break.
3. **Contingency and parity** (developmental core, with the linguist's parity constraint and typed interface). Reasons:
   - It is the only line that attacks the grounding problem with a bound (the data-processing inequality).
   - It defines the social drive as being answered, which is blind to polarity and so refuses flattery at the level of the drive.
   - Its still-face predictions are stated directly in the units of evaluation.md S2-c.

The **control-theoretic** sketch is kept as the source of two bounds that every candidate must state: the small-gain safety bound and the observability bound in its interface sector. If a fourth candidate is developed, this sketch is next: it derives mimicry from the internal model principle and needs no learned value function. Nothing in the other sketches is discarded. Their mechanisms are cited where a candidate uses them.

Order of development: Costate first, because it can be checked soonest against S1. Thermodynamic mirror flow second. Contingency and parity third.
