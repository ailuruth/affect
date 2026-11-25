# Kuppens, Van Mechelen, Smits & De Boeck 2003: The appraisal basis of anger

Citation: P. Kuppens, I. Van Mechelen, D. J. M. Smits, P. De Boeck. "The appraisal basis of anger: specificity, necessity, and sufficiency of components." *Emotion* 3(3): 254–269, 2003. doi:10.1037/1528-3542.3.3.254.

Source read: the full PDF from the KU Leuven repository (Lirias), covering both studies, Tables 1–4, the necessity and sufficiency indices, and the general discussion. Figure values (bar charts of the φ indices and correlations) could not be extracted. The later diary study (Kuppens et al. 2009, *Cognition & Emotion*), which reports joint sufficiency of frustration, other presence, other accountability and hostile intention, was **not read**. It is known only from a search snippet.

## Claims
- Anger was tested against five components: goal obstacle (frustration), other accountability, unfairness (arrogant entitlement), control, and an antagonistic action tendency.
- **Specific to anger:** other accountability, and arrogant entitlement as an instance of unfairness. Unfairness in general also went with sadness.
- **Not necessary or sufficient:** "none of the components is necessary or sufficient for anger". The relation is "a contingent association, meaning that they usually co-occur." "A deterministic 'syndrome theory' of emotions … is no longer tenable."
- **Control was not associated with anger.** In Study 2 the control appraisal, "the feeling that one can influence what was happening" (wording from Ellsworth & Smith 1988), was unrelated to anger. It was positively related only to shame. The authors' explanation separates two senses of control:
  - control "over what has happened before";
  - the feeling "that one can still change something about the situation".

  "anger may mainly be hypothesized to include the feeling that one will be able to influence the future line of events (e.g., Scherer, 1984; Tiedens et al., 2000)", and the past-tense wording may have measured the first sense.
- **Sadness against anger.** Both go with goal obstacle. Sadness "is not associated with other accountability and arrogant entitlement": "when this obstruction is seen as caused by someone else … one is more likely to get angry instead of sad."

## Evidence
- Study 1: N = 110 high-school seniors (119 recruited), 305 recalled unpleasant situations. Recall instructions were manipulated so that one component was present or absent; there were 12–16 participants per cell.
  - Multivariate regression coefficients on the Anger scale: frustration .39 (p = .04), other accountability .59 (p < .01), arrogant entitlement .91 (p < .01), antagonism .20 (n.s.).
  - Same predictors on the Sadness scale: frustration .42 (p = .01), other accountability .18 (n.s.), arrogant entitlement −.00, antagonism .02.
  - F for Anger = 7.39, p < .01.
- Study 2: N = 100 university students. Components were rated, and emotions were taken from both a forced-choice list and free response.
  - Free responses: anger in 55% of recalled situations, sadness 22%, fear 19%, shame 12%. Interrater agreement .93–.98.
  - Anger coefficients: other accountability .15 (p = .03), unfairness .29 (p < .01), control .05 (n.s.).
  - Shame: control .25 (p = .01), other accountability −.33.
  - Sadness: goal obstacle .16 (p = .04), unfairness .24 (p < .01).
- **Necessity and sufficiency indices** (asymmetric φ):
  - φ_nec = [P(component | emotion) − P(component)] / [1 − P(component)]
  - φ_suff = [P(emotion | component) − P(emotion)] / [1 − P(emotion)]
  - "All asymmetrical phi values were considerably lower than 1", under every dichotomisation tried.

## Formal model
None beyond the two φ indices. These are the same form as Watson's sufficiency and necessity contingency indices (watson-1997-contingency-two-indices.md), applied here to appraisal and emotion.

## License
© APA. Repository copy; not redistributable.

## Verdict: adopt (as a constraint on how agency and control may map to state, and as a sharper statement of the control problem)
Two lessons for the engine:
1. **Appraisal-to-state mapping must be soft.** Other-agency raises the probability of the approach/protest region. It is neither necessary nor sufficient. That fits an emergent latent with a readout (Principle 2) and argues against any hard rule of the form "partner-caused loss → protest".
2. **"Control" must be future-directed.** The data show that "could I have influenced it" (retrospective, which goes with shame) is a different quantity from "can I still change the outcome" (prospective). Only the second is hypothesised to go with anger.

## What it implies for the single core
- **Define coping potential prospectively:** C_t = max_π E[V | π, b_t] − E[V | π_default, b_t]. This is the expected drive reduction available from acting now, against not acting. Retrospective control, "did my past action matter", is a separate quantity. It is the self-channel share of the cause posterior, and it goes with the shame-like region, not with anger.
- **No single component should be necessary in the engine.** An ablation that removes the partner-cause channel should *lower the rate* of protest-like states after losses, not remove them all. Other routes remain: unfairness-like prediction error on the partner's expected policy, and high goal obstruction. A core in which removing one channel abolishes the region entirely would contradict these data.
- **Ablation check derived from the φ indices.** Compute φ_nec and φ_suff between the core's cause-posterior components and the decoded approach/withdraw region on logged episodes. The human pattern to match: other-cause has positive φ for the protest region, well below 1. Prospective control has positive φ for protest. Retrospective self-cause has positive φ for the withdraw/self-focused region.
