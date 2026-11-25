# Fusaroli & Tylén 2016, "Investigating conversational dynamics: Interactive alignment, interpersonal synergy, and collective task performance" (Cognitive Science 40(1):145-171, doi 10.1111/cogs.12251)

Source read, 2026-11-25: the full accepted text (online-first version, labelled "Cognitive Science (2015) 1–27") hosted by the Aarhus Interacting Minds Centre (interactingminds.au.dk, file "2015_cogsci_Investigating_conversational_dynamics…pdf"). All sections, Tables 1-2, Figure 7 captions and the notes were read. The reference list was skimmed. The page numbers above are the issue pagination. The text read is the online-first version.

## Claims
- Two accounts of dialog are compared on one corpus. In interactive alignment, interlocutors imitate each other through "automatic structural priming". In interpersonal synergy, the structure lives "at the level of the interaction—such as complementary patterns straddling speech turns and interlocutors".
- "synergetic aspects of dialog provide the best statistical predictors of collective performance and adding aspects of the alignment approach does not improve the model."
- Alignment is recast: "rather than serving as the primary engine of linguistic coordination, alignment might be better conceived as a preliminary tool, providing the means to quickly establish common ground and interactional routines … while its impact decreases once a synergy is established."
- "indiscriminate alignment can be detrimental for social coordination"; "for alignment to constructively contribute to coordination, it has to be modulated according to contents and contexts."
- Roles are interchangeable within a routine: "The interlocutor expressing confidence in one trial might be the one taking the decision in the next."
- "there is no single mechanism that makes conversations easy and effective."
- Causality is left open by the authors: "additional experiments will be required to investigate if synergic structural organization is merely a by-product of effective coordination or if it plays a causal role".

## Evidence
- **Corpus.** About 20 h of video from 16 Danish dyads (14 m / 18 f, mean age 25.2, SD 6.9). On average 92 (SD 15.5) joint-decision trials per dyad, 1,472 trials in all. This is the Bahrami et al. 2010 oddball task: two 85 ms displays of six Gabor patches, one with a contrast oddball. Partners discuss only when their private choices disagree. The same corpus was analysed in Fusaroli et al. 2012.
- **Performance.** "Collective benefit" is the dyad's psychometric slope divided by the slope of the better member. A value above 1 means the dyad beat its best member.
- **Three data streams.**
  - Word-level transcripts.
  - F0 sampled every 10 ms, filtered to 75–600 Hz.
  - Speech/pause sequences at 10 ms, where a pause is no pitch for more than 200 ms.
- **Shuffled controls.** All 18 indices (3 approaches × 3 streams × L, ENTR) beat shuffled series at p < .0001, with d from 0.84 to 0.99 (Table 1). So all three kinds of structure are present, including the individual self-consistency baseline.
- **Lexicon.**
  - Alignment: r = .50, AdjR² = 0.25, p = .01, BIC = 1.98.
  - Synergy: r = .73, AdjR² = 0.45, p = .002, BIC = 2.73.
  - Self-consistency: r = .11, AdjR² = 0.01, p = .9.
  - Stepwise selection kept only synergy ENTR: r = .73, AdjR² = 0.47, p = .01.
- **Prosody.**
  - Alignment: r = .40, AdjR² = 0.31, p = .03.
  - Synergy: r = .40, AdjR² = 0.31, p = .04.
  - Self-consistency: r = .10, p = .6.
  - Stepwise selection kept only synergy ENTR: r = .67, AdjR² = 0.39, p = .02.
- **Speech/pause.**
  - Synergy: r = .63, AdjR² = 0.31, p = .03.
  - Alignment: r = .15, p = .7.
  - Self-consistency: r = .19, p = .22.
  - Stepwise selection kept only synergy L: r = .62, AdjR² = 0.34, p = .01.
- **All streams together.**
  - Synergy: r = .89, AdjR² = 0.65, p = .01, BIC = 2.86.
  - Alignment: r = .58, AdjR² = 0.303, p = .17, BIC = 7.91.
  - Self-consistency: r = .20, p = .3, BIC = 18.37.
  - Forward stepwise over all 18 indices kept only synergy predictors (lexical ENTR, speech/pause L, prosodic ENTR): r = .97, AdjR² = 0.92, p < .000001.
- **Qualitative.** Table 2 shows a good pair moving from redundant, aligned confidence talk ("I don't know … I don't know either") in trials 43–44 to elliptical, role-swapping routines in trials 71–73.
- **Caveats, mine.**
  - n = 16 dyads. A stepwise search over 18 predictors that ends at r = .97 is very likely overfit.
  - No cross-validation is reported.
  - The control is a within-series shuffle. Surrogate pairs were rejected because spliced turns break RQA assumptions (note 2).
  - The self-consistency model uses the better-performing member. Note 3 reports the same null result for a random member and for the mean of the two.

## Formal models
No generative model. The measurement apparatus is:
- **Embedding.** Time-delay embedding (Takens) per series.
  - Transcripts: dimension 3, delay 1, radius 0 (exact match).
  - F0: dimension 4 from false nearest neighbours, delay 4 from the first minimum of average mutual information, radius set for a fixed 4% recurrence rate.
  - Speech/pause: dimension 2, delay 1, radius 0.
- **Recurrence matrix.** R_{i,j} = 1 if x_i ≈ y_j within ε, else 0 (eq. 5).
  - CRQA (x from A, y from B, with the partner's turns blanked out) measures alignment.
  - RQA on the dyad as one interleaved series ("not discriminating between interlocutors") measures synergy.
  - RQA on one person measures self-consistency.
- **L.** Mean diagonal line length, L = Σ_{l≥lmin} l P(l) / Σ_{l≥lmin} P(l) (eq. 6). It indexes the extent of patterns.
- **ENTR.** Shannon entropy of the diagonal line lengths, ENTR = −Σ p(l) ln p(l) (eq. 7). It indexes the complexity or flexibility of patterns.
- **Psychometric model.** P(Δc) = H((Δc + b)/σ), with slope s = 1/(2πσ²)^{1/2} (eqs. 1-3).

The operational definition of synergy is the key move. Recurrence is computed on the merged turn sequence, so a pattern that A starts and B completes counts, while a pattern B copies from A is what CRQA counts.

## What it implies for a dyadic affective core
- **A one-gain model is the alignment model.** A scalar that runs the agent from flat to copying the partner can only move the CRQA-type index (cross-recurrence of the agent on the partner). In this corpus that index was the weaker predictor and added nothing once synergy was in. "Indiscriminate" alignment was negatively related to benefit in the companion 2012 study (reported in the 2014 and 2013 papers, numbers not read).
- **The useful structure is joint and role-indifferent.**
  - Recurrence of the joint sequence, regardless of who produced which part, carried the predictive information.
  - A dyadic core would need a state whose dynamics are defined over the pair, with roles that can be swapped. The fixed "agent responds to partner" map is the wrong shape.
  - This favours something like the swap-symmetric/antisymmetric split of the joint-action sketch (v3), or a joint latent, over a per-agent response gain.
- **Flexibility, not only strength.** ENTR (variety of pattern lengths) predicted better than L for lexicon and prosody. A gain can make coupling stronger or weaker, but not more varied. A one-gain model therefore cannot reproduce "high ENTR with moderate L".
- **Time course.** The authors propose alignment early and routine later. An adaptive core would shift from copying-like to complementary coupling as a routine forms. That is a change in the shape of the coupling over a session, which is exactly what the project's dial analysis (HARNESS.md, D75) tests for.
- **Not shown.**
  - Affect: the task is perceptual decision-making with no emotion measures.
  - Faces: audio and transcripts only.
  - Causality.
  - Out-of-sample prediction.
  - Prosody is the only stream close to this project's inputs.

## Verdict: adopt (as a measurement and a target, not a mechanism)
- Adopt the three-way RQA contrast (cross / merged-joint / individual, each with L and ENTR, against shuffles) as a ready analysis for the human ground truth and for the agent's face-voice streams on Seamless. It fits Principle 5: an ablation of a complementary pathway should lower joint ENTR, not cross-recurrence.
- Do not adopt its numbers as effect sizes: n = 16, stepwise selection, no affect.
