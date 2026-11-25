# Synofzik, Vosgerau & Newen 2008; Synofzik, Vosgerau & Voss 2013: from comparator to cue integration in agency

Citations:
- M. Synofzik, G. Vosgerau, A. Newen. "Beyond the comparator model: a multifactorial two-step account of agency." *Consciousness and Cognition* 17(1): 219–239, 2008. doi:10.1016/j.concog.2007.03.010.
- M. Synofzik, G. Vosgerau, M. Voss. "The experience of agency: an interplay between prediction and postdiction." *Frontiers in Psychology* 4: 127, 2013. doi:10.3389/fpsyg.2013.00127 (CC BY 3.0, PMC3597983).

Source read:
- **2008: abstract only.** It is closed access, and no free copy was found. The abstract and secondary descriptions say it separates a non-conceptual *feeling* of agency from a conceptual *judgement* of agency, and argues that the comparator explains neither. In its place, "a multifactorial weighting process of different agency indicators accounts for the feeling of agency", and conceptual processes then form the judgement.
- **2013: read in full** (PMC XML). The 2013 paper restates the 2008 two-level distinction and makes the weighting explicit as optimal cue integration, so this note rests mainly on 2013.
- The experiments it cites (Gentsch 2012, Synofzik 2010, Moore 2009, Wegner 2004, Wilke 2012) were not read.

## Claims (2013)
- **Two levels.** The feeling of agency is "a non-conceptual, automatic registration of whether I am the agent or not". The judgement of agency is "the formation of a belief about who the initiator of the movement was". The judgement takes in "context information, background beliefs, general social norms".
- **Neither account suffices on its own.**
  - The comparator (Frith) can explain the feeling but "cannot explain the actual conceptual attribution". It is also not necessary: in Wegner's "helping hands" pantomime, people felt agency over another person's hands when they heard previews of the movements. There was no efference copy.
  - Wegner's post-hoc inference cannot explain the feeling. It would arise too late, and crickets already separate self-produced from external input.
- **Proposal.** "The brain constantly integrates several different authorship cues and weights each cue according to its relative reliability". "The variance within one agency cue should be directly related to the reliance on another."
- **Cue types:**
  - Predictive cues ("sensorimotor priors"): efference-copy predictions, action selection, primes.
  - Postdictive cues: visual and proprioceptive feedback, and the affective valence of the outcome.
  - Cognitive cues: background beliefs, and the context of who else is present.
- **Valence is an agency cue.** "Emotional appraisal, anticipation of reward or punishment or value attribution may influence the weighing of internal or external signals on both the sensorimotor and cognitive level." Delusions of control rarely concern trivial acts. They concern acts "with high affective and moral value".
- **Schizophrenia as reweighting.** Imprecise internal predictions cause over-reliance on post-hoc cues. Misattribution can then go either way, under-attribution (delusions of influence) or over-attribution (delusions of reference), depending on which alternative cues are available.

## Evidence (as summarised in 2013)
- Gentsch et al. 2012. A keypress produced an arrow with 75% (high) or 50% (low) contingency, preceded by a congruent or incongruent prime. Priming changed judged causal strength **only in the low-contingency condition**. This is the signature of reliability weighting.
- Moore et al. 2009a. Primes changed intentional binding for both active and passive movements, but more for passive ones, where there is no motor prediction.
- Synofzik et al. 2010 and Voss et al. 2010. Patients' imprecision in predicting the consequences of their own actions correlated with the severity of delusions of influence. Patients relied more on visual feedback. The paper gives no effect sizes.

## Formal model (implied; the paper gives no equations)
Standard cue combination (Ernst & Banks), applied to a latent authorship variable a:
- Each cue gives an estimate â_i with variance σ_i².
- The combined estimate is â = Σ_i w_i â_i, with w_i = σ_i⁻² / Σ_j σ_j⁻².
- In Bayesian form for a binary author (self, other, world): P(author = k | cues) ∝ P(k) · Π_i p(cue_i | k), with each likelihood's sharpness set by its precision.
- The prior P(k) is where background beliefs and context enter (the judgement level). The feeling level is the likelihood product of the sensorimotor cues.

## License
2013: CC BY 3.0. 2008: © Elsevier.

## Verdict: adopt (as the form agency attribution must take in the core: precision-weighted inference over causes)
- It turns "agency" from a comparator difference into posterior inference over who caused an event.
- That is exactly the form a generative-model core produces for free.
- Its evidence base is thin and partly patient-correlational, as the authors acknowledge ("only limited and preliminary experimental evidence").

## What it implies for the single core
- **Agency attribution is a posterior over cause channels:** P(c ∈ {self, partner, world} | o, u, context). It is precision-weighted, and the precisions are already the core's quantities (element 7 in emotion-elements-synthesis.md). Nothing named "agency" needs to be added: it is the responsibility of each causal channel in the generative model for the observed change.
- **Two levels map onto the project's layering.**
  - The feeling is the fast posterior in the core.
  - The judgement belongs to Claude (Principle 4). Claude may reinterpret who caused an event, and that may feed back as a prior.
- This gives a clean D1-style ablation: cut Claude's prior feedback. Fast attribution stays; context-driven reattribution, such as "they didn't mean it", vanishes.
- **Valence feeds attribution: a loop to guard.** If outcome valence is an agency cue, the core can learn self-serving attribution (good outcomes to self, bad outcomes to the partner). Haggard 2017 reports exactly this bias in humans. In the engine it would push partner-caused attributions of bad outcomes, and therefore anger-like approach, upward. This must come out of precision weighting, not a hand-set bias, and it should be measured.
- **Reliability-weighting ablation, derived directly from Gentsch 2012.** Lower the precision of the agent's own forward model of the partner's responses (low contingency).
  - Prediction: attribution becomes dominated by context cues, the slower priors.
  - Clamping all precisions equal removes the contingency-by-prime interaction.
- **Schizophrenia analogue as a stress test.** Inflate the forward-model noise. Attribution should flip episodically in both directions, and flip more for high-valence events. That is a specific, falsifiable prediction for a core with valence-modulated precision.
