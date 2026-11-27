# Activation of serotonin neurons promotes active persistence in a probabilistic foraging task (Lottem, Banerjee, Vertechi, Sarra, oude Lohuis & Mainen)

Citation: E. Lottem, D. Banerjee, P. Vertechi, D. Sarra, M. oude Lohuis, Z. F. Mainen. "Activation of serotonin neurons promotes active persistence in a probabilistic foraging task." *Nature Communications* 9, 1000 (2018). doi:10.1038/s41467-018-03438-y. PMC5843608.

Source read: the PMC full-text HTML, text-extracted, read in full (abstract, introduction, results, discussion, methods). **Not read:** the Supplementary Information PDF (Supplementary Figs. 1–8, including the model comparison and the ODC–hazard correlation details).

Flavell et al. 2013 (serotonin and PDF initiating and extending opposing behavioural states in *C. elegans*), the intended companion source, could not be read: the PMC page returned a CAPTCHA and the lab-hosted PDF did not download from this environment.

## What the paper does
- **The question.** Does serotonin (5-HT) promote passivity (Soubrié's behavioural inhibition) or persistence in an ongoing action that is costly but leads to delayed benefit? In waiting tasks the two coincide by design.
- **Task.** Water-restricted mice shuttle between two ports at the ends of a 50 cm box. At a port, each nose-poke is rewarded with probability A_i e^{−(n−1)/5} (A = 0.5, 0.75, 1 for low, medium and high patches, uncued, interleaved). Leaving and travelling (≈ 3.3 s) is the alternative. Waiting here requires active poking.
- **Near-optimal foraging.** Reward rate at leaving equals the session's average reward rate (0.20 vs 0.19 s⁻¹; marginal value theorem). Mice poke more in better patches (F(2,45) = 3.49, p = 0.04) and leave at the same estimated reward probability across patch types (p = 0.95). Shuffled controls reverse both.
- **Photostimulation of dorsal raphe 5-HT neurons** (SERT-Cre, ChR2; 25 Hz, 5 mW; on 50 % of correct trials, from the first poke until leaving):
  - more pokes per trial: 14.73 vs 13.61 (p = 0.014, n = 10); stimulated-minus-control 1.12 vs −0.46 in wild-type controls (p = 0.0047);
  - longer delay from last poke to exit: 4.26 vs 3.84 s (p = 0.0039);
  - **no effect on travel time**, including when stimulation was delivered during travel (3.19 vs 3.02 s, p = 0.22);
  - **no carry-over** to following unstimulated trials, and no dependence on runs of stimulated trials.
- **Model.** A discrete proportional-hazards (Cox) model fits better than an MVT-based stochastic model in 15 of 16 mice: after each omission the mouse leaves with hazard λ_n, where logit λ_n = logit λ₀(n) + βx; λ₀ is a baseline hazard over omissions since the last reward; **each reward resets the clock** (to a covariate-dependent value), giving high win-stay even after late "lucky" rewards. Cross-validated simulations reproduce individual mice and per-mouse stimulation effects. The stimulation coefficient is significantly negative in SERT-Cre mice (p = 0.014): 5-HT **multiplicatively scales down the hazard of switching**. Its effect was constant across the stimulation period.
- **A behavioural read-out of the latent decision variable.** The omission duty cycle (poke duration over poke plus preceding interval; poking vigour) falls through a trial and jumps back after a reward (hazard 0.056 → 0.014; ODC 0.86 → 0.87), tracking the model's hazard. Stimulation raises ODC (p = 0.0098), and has no effect on ODC once conditioned on the modelled hazard (p = 0.90).
- **Interpretation (the authors').** 5-HT "stabilize[s] an on-going behavior by reducing the probability of switching to the next one" and acts as a "multiplicative bias on the latent decision variable". They favour an effect through uncertainty (5-HT neurons report unexpected events of either valence; 5-HT stimulation does not produce place preference or bias two-choice value decisions in their hands), and suggest a common action on integration-to-bound circuits across waiting, flexibility and sensorimotor gain. The task is too complex for the model to be the optimal solution.

## The mathematical object
**A survival process over the current behavioural mode: the hazard of leaving is a baseline function of time since the last reset event, multiplied by exp(β·m) for a neuromodulatory level m; resets come from the agent's own outcomes; m changes dwell, not destination or transit.**

## What it means for the design
1. **A structural source of intermediate time scales.** Dwell time in a mode is set by a product of a clock (time since own reset) and a slow multiplicative modulator. Nesting the same form (the modulator itself occupying modes with their own hazards) gives a hierarchy of time scales without hand-set time constants at each level. This is a hidden semi-Markov structure **(standard)**.
2. **Modulator changes "how long", not "where to".** Stimulation lengthened the current mode and left travel and the next mode unaffected. A partner signal confined to this slot would change the agent's dwell, never choose its content.
3. **The selection hazard.** In a semi-Markov process the time-averaged occupation of mode i is π_i μ_i / Σ_j π_j μ_j (π the jump-chain stationary law, μ the mean dwell) **(standard)**. Any modulator that correlates with which mode the agent is in changes occupation without any learning. If the partner's signal sits in the hazard and the partner reacts differently to different agent modes, the agent spends more time in the modes the partner rewards with a low-hazard signal.
4. **Vigour as a readable latent.** Poking vigour tracked the hidden hazard. A rich latent's dwell variable could be read in the agent's own motor microstructure (tempo, effort), as a derived evaluation probe.

## Verdict
- **adopt (object for time scales; hazard of dwell-time selection).** It gives a measured, multiplicative, transition-specific modulator with no carry-over. The object, a proportional-hazards semi-Markov process, is standard.
