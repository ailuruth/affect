# Timmons, Margolin & Saxbe 2015, "Physiological linkage in couples and its implications for individual and interpersonal functioning: A literature review" (J Fam Psychol 29(5):720-731, doi 10.1037/fam0000115); with Helm, Sbarra & Ferrer 2012 (Emotion 12(4):748-762, doi 10.1037/a0025036), Helm, Sbarra & Ferrer 2014 (Emotion 14(3):522-531), Ferrer & Helm 2013 (Int J Psychophysiol 88:296-308) and Reed, Randall, Post & Butler 2013 (Int J Psychophysiol 88:309-316)

Source read, 2026-11-25:
- **Timmons et al. 2015:** full text, NIH author manuscript, PMC4593729 (fetched as HTML). Read: the abstract, theory, the four hypotheses, method, Tables 1-2, results, discussion and conclusion. Appendix A (the per-study linkage methods) is in a supplement that was not opened.
- **Helm et al. 2012, Helm et al. 2014, Ferrer & Helm 2013, Reed et al. 2013:** abstracts only (PubMed). All four are closed access; no open copy was found by OpenAlex, Semantic Scholar or web search. Their results below come from those abstracts and from Timmons et al.'s tables, not from the papers.
- **Unread:** the closely related McAssey et al. 2013 (Methodology 9:41-53, the same 32-couple dataset) has an open PDF on research.vu.nl, but it was blocked by a Cloudflare check.

## Claims
- Linkage is "covariation between two people in their physiological states". The review asks "when is linkage 'good' or 'bad'", rather than whether.
- Four hypotheses, "not mutually exclusive":
  1. co-activation of the SNS or HPA axis is "bad" (negative-affect reciprocity, escalation);
  2. moderate linkage is "just right" (curvilinear);
  3. linkage is harmful when the couple is overloaded ("catch" each other's stress instead of down-regulating);
  4. its meaning depends on the emotional context (hard versus soft affect).
- Conclusion: "linkage is neither wholly 'good' nor 'bad' ... may reflect closeness and attunement but may be maladaptive in other cases, especially if it occurs in the context of repeated and chronic stress responding." Linkage is "a double-edged sword".
- On inverse linkage: "several studies reported inverse associations in partners' physiology". One explanation is "that more satisfied couples show a pattern of responding in which one partner de-activates when the other activates, resulting in a regulation process that occurs around a stable point rather than partners jointly activating". The other is turn-taking, "though this would not explain the inverse associations observed in cortisol".
- Open questions they list: "who drives whom? Does the direction of influence depend on gender? ... what mediates the transfer ... vocal, facial, tactile, or olfactory cues?"

## Evidence
**Timmons et al. 2015 (systematic review):**
- **Corpus:** 24 articles on romantic couples (to end-2014), with samples of 4-221 couples ("71 percent of studies including 50 or fewer couples"). No same-sex couples and no clinical samples.
- **Where linkage was found:** cortisol "eight out of nine studies"; also HR, BP, EDA, fMRI, prolactin, pulse, RSA, respiration and thoracic impedance. Not found for estradiol, oxytocin, DHEAS or testosterone. Reed et al. 2013 found it for BP but not HR or EDA.
- **Time spans** from 10-s epochs over 20 min to weekly samples over months. "It is unclear exactly how long it takes for the physiology of one person to affect the other."
- **Satisfaction:** of 17 tests of linkage against satisfaction-type variables, 13 were significant and 4 were not.
  - Cortisol linkage went with poorer relationship quality (Liu et al. 2013; Saxbe & Repetti 2010; Schneiderman et al. 2014).
  - Levenson & Gottman 1983: a composite linkage went with lower satisfaction "during conflict but not events of the day discussion".
  - Helm et al. 2014: RSA linkage went with higher satisfaction.
- **Sign flips with context:**
  - Reed et al. 2013: "at low levels of demand-withdraw behavior, the association between partners' BP was negative whereas at high levels, the association was positive".
  - Liu et al. 2013: diurnal cortisol slope linkage was "+ at ↑ spousal disagreement and − at ↓ spousal disagreement" (likewise for spousal strain).
- **Role asymmetry and moderators:**
  - Hubler 2013: "↓– linkage from Ms to Fs = ↑ relationship satisfaction".
  - Thomsen & Gilbert 1998: "In Fs, ↑ linkage = ↓ listening".
  - Reuf 2001: in women, more linkage went with more empathic accuracy.
  - Chatel-Goldman et al. 2014: EDA linkage rose with touch, and the effect was larger in low-empathy participants.
  - Saxbe & Repetti 2010: cortisol linkage appeared at home (together), not at work (apart).
  - Schneiderman et al. 2014: "When both partners had ↑ cortisol, they had ↓ empathy and had a ↑ likelihood of breaking up 6 months later."
- **Helm et al. 2012, as tabled by Timmons:**
  - Tasks were baseline, gazing, and "try to synchronize their physiology", 3 min per task.
  - Linkage was found in HR and respiration, but "Results varied by task or the way the physiological index was computed".
  - Respiration linkage went with "greater satisfaction in females during the resting task but lower satisfaction in males during the imitation task (an experimental task in which the researchers explicitly instructed the couples to try to synchronize their physiology)".
  - Attachment associations were "complex"; there was no association with relationship length.

**From the abstracts:**
- **Helm 2012:** coupled linear oscillators (Boker & Nesselroade 2002) on respiration and HR; "associations were detectable within all three tasks, with different patterns of coupling within each task".
- **Ferrer & Helm 2013:** a Felmlee & Greenberg 1999 dyadic differential-equation system with "parameters representing self-regulation and coregulation for each individual", fitted to the same 32 couples per dyad and compared across the three tasks.
- **Helm 2014:** cross-lagged panel model of RSA in 32 couples. "Men's and women's RSA were associated with their partners' previous RSA responses, and this pattern was stronger for those couples with higher relationship satisfaction."
- **Reed et al. 2013:** 44 couples discussing how they influence each other's health; BP, IBI and skin conductance. "At low levels of influence linkage was 'anti-phase' and at high levels linkage was 'in-phase'." The effects were "not due to relationship conflict, emotional experience, or simply the pattern of blood pressure over time". They predicted anti-phase linkage from "the behavioral coordination of turn taking".

## Formal models
None in the review itself; it lists multilevel and time-series methods with no gold standard. From the abstracts:
- Helm 2012 uses the Boker-Nesselroade coupled linear oscillator, with the second derivative regressed on own and partner level and velocity. See research/butler-2011-temporal-interpersonal-emotion-systems.md for the rties form, ẍ_i = η_i x_i + ζ_i ẋ_i + η_ij x_j + ζ_ij ẋ_j.
- Ferrer & Helm 2013 use Felmlee & Greenberg's self-regulation-plus-coregulation system. Its equations were not read.
- Helm 2014 and Reed 2013 use lagged regressions whose cross-partner coefficient sign marks in-phase versus anti-phase.

## What it implies for a dyadic affective core
- **The sign of the partner coefficient is not fixed in human data.** It flips from negative (anti-phase) to positive (in-phase) as partner influence, demand-withdraw, disagreement or strain increase (Reed 2013; Liu 2013). A single non-negative gain from "flat" to "copy" lives only on the in-phase side. It cannot produce the anti-phase regime that low-conflict, low-influence couples show, which the authors read as regulation "around a stable point".
- **Direction and role matter:** M→F and F→M linkage carry different correlates (Hubler 2013; Thomsen & Gilbert 1998), so the coupling matrix is asymmetric. Who drives whom is listed as unanswered.
- **The channel matters:** cortisol linkage (hours) tracks poorer quality; RSA linkage (seconds-minutes) tracks better quality. Coupling strength and its value differ per subsystem and time scale.
- **Instructed synchrony is not good synchrony.** In Helm 2012 the "try to synchronize" task was the one where men's respiration linkage went with lower satisfaction. Driving an agent toward maximal synchrony with the user is not supported as a goal; this fits Principle 6.
- **What is NOT shown:**
  - All correlational; most samples are ≤ 50 couples.
  - Publication bias and shared-environment confounds are acknowledged.
  - Only one curvilinear test, which was non-significant.
  - Turn-taking may explain anti-phase autonomic linkage. That would make it complementarity at the behavioural level, not regulation.
  - The four primary papers here were not read beyond their abstracts.

## Verdict: adopt (as evidence that partner coupling changes sign with context and is role-asymmetric); watch Helm 2012 and Reed 2013 until their full texts are read
- **Evaluation:** the sign flip with influence or conflict (Reed 2013) is a concrete human pattern a one-gain model cannot produce. It is the kind of profile change the dial analysis (research/harness/HARNESS.md) tests for.
- **Primary-source check:** before relying on the numbers, obtain Reed et al. 2013 and Helm et al. 2012 or McAssey et al. 2013.
