# Zhang, Berridge, Tindell, Smith & Aldridge 2009: A neural computational model of incentive salience

Citation: J. Zhang, K. C. Berridge, A. J. Tindell, K. S. Smith, J. W. Aldridge. *PLoS Computational Biology* 5(7): e1000437, 2009. doi:10.1371/journal.pcbi.1000437. Full text: PMC2703828.

Source read: the full text via the Europe PMC XML, covering the abstract, introduction, model, Test 1 (salt appetite) and the opening of Test 2 (amphetamine and sensitization). The equation images were lost in text extraction. The forms below are rebuilt from the paper's own prose and the Fig. 1 caption ("either multiplicatively (V*κ) or additively (V+log κ)"). The neural data are reanalysed from Tindell et al. 2009, which was not read.

## Claims
- Cue-triggered "wanting" (incentive salience) is computed fresh each time a cue is met, from two inputs: the cached learned value and the current physiological state. "Computational models can adequately capture fluctuations in cue-triggered 'wanting' only by incorporating modulation of previously learned values by natural appetite and addiction-related states."
- Model: the incentive value of state `s_t` is "the motivationally-modulated value of the immediate reward r_t plus the discounted value of the expected reward in the next state". The modulation is either multiplicative, `κ·r`, which changes magnitude, or additive, `r + log κ`, which can flip sign. `κ < 1` means devaluation, `κ > 1` means enhancement, and "When κ = 1 our model reduces to the conventional temporal difference model".
- κ is specific to each need. "There can be different values of κ at any given time for different CSs that are associated with different reward UCSs (food, salt, water, sex etc.)." "Each appetitive system would specifically modulate the values of its own UCS array … and simultaneously modulate most powerfully specific CSs associated with its UCSs."
- Learned values are protected from state, "a firewall between motivation and learning that protects the integrity of learned values." The cached V is not rewritten when κ changes.
- Additive versus multiplicative: flipping the sign in a multiplicative model "would invert the rank order", so the most-liked salt would become the most disliked. The additive form keeps "the 'best' stimulus … best relative to the others" while all of them cross zero.

## Evidence
- Test 1, from Tindell et al. 2009 (rats, ventral pallidum recordings). Training pairs one tone with intense salt (three times seawater) and another with sucrose; a third tone is a control. Under first-ever sodium depletion, with no salt re-tasted and the tones presented in extinction, "the salt CS now elicited a high level of firing that was equal to or even higher than the sucrose CS". The boost "did not apply to a control CS that predicted nothing, nor did it further boost firing to the CS for sucrose."
- The simulations in Fig. 1 are illustrations only. Learning follows `V(t) = A(1 − exp(−t/τ))` with A = ±1.3 and τ = 3. κ ∈ {5, 4, 2, 1, 0.7, 0.2, 0.1} is applied at t = 11. No model is fitted to the neural data.

## License
Paper: Creative Commons Public Domain declaration (per the article's licence statement). No code.

## Runs on this Mac without a GPU?
n.a. The model is one line of arithmetic.

## Verdict: adopt (as the formal statement of need-specific motivational salience)
- It is the canonical computational statement that "hunger makes food cues salient" is a per-need gain on learned cue values, applied at retrieval time with no relearning.
- It fits Principle 2: κ is a body-state gain, not a named emotion.
- It is a theory paper with re-plotted data, and it does not model attention allocation itself. Combine it with a selection mechanism that uses κ-modulated values as attention weights.

## What it implies for the open question
- The neural and behavioural signature that a scalar drive cannot produce is selectivity. Salt depletion raised the salt cue and left the sucrose and control cues unchanged.
- A single scalar drive multiplying all cached values would raise every cue together. A winner-take-all over needs would pick salt but has no graded way to keep sucrose wanted. Need-specific κ_i, each attached to the cues of its own outcome, is the smallest structure that reproduces the data.
- Structure pays here in a first-ever or rare need state, where there is no experience to relearn from.
- A Bot ablation follows from this. Replace κ_i with one shared κ, and a long silence from one person should raise the salience of every person's cues rather than that person's. That is a testable loss of selectivity.
