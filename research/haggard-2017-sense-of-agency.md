# Haggard 2017: Sense of agency in the human brain

Citation: P. Haggard. "Sense of agency in the human brain." *Nature Reviews Neuroscience* 18(4): 196–207, 2017. doi:10.1038/nrn.2017.14.

Source read: the full accepted manuscript from UCL Discovery (green open access, 30 pp.), covering the main text, Boxes 1–2, the figure captions and the glossary. The reference list was skimmed. The primary studies it cites were not read; their numbers are as the review reports them.

## Claims
- **Definition.** The sense of agency is "the feeling of making something happen … the experience of controlling one's own motor acts and, through them, the course of external events." Haggard explicitly sets aside the social-science and computational sense of a "felt capacity to act (self-efficacy)". He focuses on instrumental control (self acting on the world) rather than social attribution (self or other). It "remains unclear whether social attribution … depends on an antecedent ability to compute and perceive instrumental agency, or vice versa."
- **Volition is necessary.** Involuntary movements, from TMS or passive displacement, give ownership but never agency. They produce less intentional binding, or reverse it.
- **Action selection contributes prospectively.**
  - Choosing among alternatives raises agency.
  - Anodal tDCS over the left DLPFC raised intentional binding only in studies where participants chose between actions (a meta-analysis of 7 studies).
  - Fluent selection, from congruent subliminal primes, raises judged agency even though the primes do not predict the outcome: "the contribution of action selection fluency … is, in a sense, illusory."
- **Limits of the comparator.** Under a comparator, agency is the absence of a prediction-error signal, so it explains non-agency ("I didn't do that") but "does not generate any neural signal that could cause" the positive "buzz" of agency. It would also attenuate the very goal outcomes one intends.
- **Agency is both prospective and retrospective.**
  - When tones followed actions with 50% probability, action binding was stronger on trials with a tone (retrospective).
  - On trials with no tone, binding was stronger in blocks where tones were likely (75%) than unlikely (50%) (prospective).
  - In schizophrenia the prospective component is absent: binding depended "entirely on the actual occurrence of the tone". "The brain may be in a constant state of surprise, attempting to understand the events it has itself generated."
- **Circuit.** Frontal areas (pre-SMA, DLPFC) carry selection and initiation, and parietal areas carry monitoring.
  - A meta-analysis of 15 studies places the temporoparietal junction and angular gyrus with *non*-agency.
  - The anterior insula is the only area consistently associated with positive self-agency.
  - Haggard favours "connectivity between frontal … and parietal areas" over a single comparator site.
- **Biases.** People overestimate their own agency, more so for positive outcomes (a "self-serving" bias). Depressed people report less control, which is possibly realistic ("depressive realism", which Haggard marks as controversial).
- **Coercion lowers agency.** Under instruction, action–tone intervals were judged longer and the auditory N1 was smaller than under free choice.
- **Box 2: agency is acquired.** "A newborn infant appears to have little or no voluntary control over its actions, and little or no sense of agency"; voluntary control, "notably smiling", emerges guided by "reinforcement of parental affective communication".

## Evidence (numbers given in the review)
- Intentional binding uses a tone 250 ms after a keypress.
- Prospective effect: 75% vs 50% tone probability.
- Meta-analyses: 7 tDCS studies, 15 neuroimaging studies.
- Explicit and implicit agency measures are only weakly correlated across individuals.
- No effect sizes are given in the text.

## Formal model
None given. The review's computational content is the comparator (its Fig. 3, three uses: correct the command, attribute agency, attenuate) plus a qualitative prospective-and-retrospective integration.

## License
Accepted manuscript, green open access on UCL Discovery; © Springer Nature. Not redistributable.

## Verdict: adopt (definitional and experimental anchor; no formalism)
It separates three things the brief tends to merge:
- instrumental agency (do my acts move the world?);
- social attribution (who did it?);
- self-efficacy (can I?), which it excludes.

Appraisal theory's "agency" (Smith & Ellsworth 1985) is the second. Its "coping potential" is closer to the third. Haggard's instrumental agency is the bridge between the two: an online, learned estimate of how much one's own acts move outcomes.

## What it implies for the single core
- **Three quantities, three ablations, one model.** In a core with a learned world model p(o' | o, u, partner):
  - Instrumental agency is the action-conditional predictive gain, something like I(U; O' | context), or prospectively the expected reduction in outcome uncertainty from choosing u. Haggard's 75%-vs-50% result says the core should carry this as a prior expectation and not compute it only after the outcome.
  - Social attribution is the posterior over cause channels (see synofzik-2008-2013-agency-cue-integration.md).
  - Coping potential (self-efficacy) is the controllability of *value* (see the controllability notes and the synthesis).
- **Prospective against retrospective ablation.** Remove the action-conditional prior, so that "agency" is computed only from realised outcomes. The prediction, after the schizophrenia result: attribution follows outcome occurrence trial by trial and loses its dependence on block-level contingency. In the engine, the agent's sense that its smile moves the partner would collapse on every non-response instead of tracking the partner's average responsiveness.
- **The positive signal Haggard says the comparator lacks.** A model-based core does produce a positive signal: the gain in predictive precision that comes from conditioning on one's own action. This is a candidate for the "buzz", and it is positive, not an absence.
- **Box 2 fits the brief's infant start.** Agency over one's own face must be learned from contingent caregiver responses. This lines up with gergely-watson-1996-social-biofeedback.md and contingency-causal-synthesis.md.
- **A warning.** Haggard's selection-fluency effect means that action-selection certainty (low policy entropy) inflates felt agency regardless of the real contingency. If the core reads agency from policy confidence, as Hesp et al.'s affective charge does, it will inherit this illusion. That may be faithful to humans, but it should be logged.
