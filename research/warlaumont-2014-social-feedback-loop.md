# Warlaumont, Richards, Gilkerson & Oller 2014, "A social feedback loop for speech development and its reduction in autism" (Psychological Science 25(7):1314-1324, doi:10.1177/0956797614531023, PMC4237681)

Source read: the NIH author manuscript on PubMed Central, in full (introduction, method, results, discussion); the supplementary material (contingency computation, statistics, computational model) was not read, so model details and some βs' exact specifications are only as the main text gives them.

Read for search pass 9 (contingent shaping of the child's own output in naturalistic data).

## Key claims
- **Data.** LENA daylong recordings, 1,153 recordings, 13,836 h: 106 typically developing children (8-48 months) and 77 with autism (16-48 months). Automatic segmentation into child speech-related vocalizations (speech, babble, singing) vs non-speech (cry, laugh, vegetative) and adult vocalizations. "Response" = any adult vocalization starting within 1 s of the end of the child vocalization.
- **Two contingencies (TD, matched subsample):**
  - adult → child content: P(response | speech-related) − P(response | non-speech) = 0.065, p < .001;
  - child ← adult: P(next child vocalization speech-related | previous speech-related one answered) − P(… | not answered) = 0.036, p < .001.
- **Autism:** fewer vocalizations (β = −0.274), lower speech-related proportion (β = −0.275), adult contingency on content weaker (0.048; difference β = −0.134, p = .008); the child's dependence on prior response did not differ (0.042). Less interaction overall (cross-recurrence height β = −.166) and a lower child-leads/child-follows ratio.
- **SES and age:** adult contingency on content rises with age (β = .111) and maternal education (β = .209); the child-side contingency does not vary with any demographic.
- **Scale argument.** Both effects are about .05, but children produce "well over 2,000" vocalizations a day; a simple model (supplement, not read) is used to argue that the differences compound into the ASD–TD divergence.
- **Caveat stated by the authors:** correlational; the causal test would be to manipulate adult response contingencies (which is what the Goldstein experiments do).

## What it means for the engine
1. **The partner's response is selective by content, and the child's production follows the response.** This is the receiver-predisposition structure: what the partner answers defines the direction the child's output moves. Proposition 1(a), open.
2. **Small per-event gains compound.** A per-step effect of a few percent over thousands of events a day is a strong learning signal. For the engine this means a bound on the per-update gain of any partner-credited learner says nothing about where it ends; only an output bound (D93's per-expression ceilings) bounds the end state, and inside the band the learner will go where the partner's selectivity points.
3. **Adult-side learning.** The authors note that the adults' contingency may itself be learned from the child's behaviour: the dyad is two coupled learners. That is the dyadic setting in which the engine's approval audit must hold (the user learns too).

## Verdict
- **background (naturalistic magnitude of the open route: partner contingency on content ≈ .065, child dependence on prior response ≈ .036, compounding over thousands of events).** Automatic labelling, 1-s window, correlational.
