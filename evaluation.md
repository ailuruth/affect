# Evaluation

Written 2026-11-24 (S0), under brief.md, Evaluation. Every claim the engine makes is judged here with an instrument or protocol the field already uses. For each claim this file gives the protocol, its primary citation, its published scoring, and what counts as failure. Each source named below has a note under research/, and every number quoted here was read in that source by the note's author. A source that was not read is marked **unread**, and nothing here rests on it alone.

Three labels are used throughout:
- **Standard**: used as published, with the same items, scoring and analysis.
- **Adapted**: changed to fit an artificial agent. Each adaptation cites its precedent, or says none was found. Adapted results are reported apart from standard ones.
- **Provisional**: no accepted instrument exists, so the measure is the project's own. It may guide development. It never supports a stage claim alone.

How a candidate foundation uses this file: each candidate in research/foundations/ states its predictions for S1 and S2 in the units of the protocols below (for example, a sign and a size for a still-face contrast, or a surrogate-tested synchrony that appears and disappears under a named lesion). That makes candidates comparable before any engine code exists.

---

## Part 1. Protocols shared by every claim

### E1. Ablation as lesion method (Principle 5): standard

**Sources:**
- Plaut & Shallice 1993, Cognitive Neuropsychology 10:377-500 (research/plaut-shallice-1993-deep-dyslexia.md).
- The validity critiques Plaut 2003, Cortex 39:138-141, and Bullinaria 2005 (research/plaut-2003-double-dissociations.md, research/bullinaria-2005-connectionist-neuropsychology.md).
- Bullinaria & Chater 1995, Shallice 1988 ch. 10 and Juola & Plunkett 2000 are **unread**; they are known only through the two sources above.

**Published procedure:**
- Lesions are random removals of units or connections, or added weight noise.
- "Twenty instances of lesions" per lesion type, at severities "0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, and 0.7". The earlier Hinton & Shallice study used 10 instances.
- Responses are read out against criteria fixed in advance (cosine > 0.8, with a gap of 0.05 to the next candidate).
- Error distributions are compared with a chance distribution, not with a single rate.
- Results are averaged over the severities that leave performance in a band fixed in advance: "correct performance between 15-85%".

Plaut 2003 adds that individual lesions of equal size and site produced "statistically reliable double dissociations" that "provide no information". Only the mean over many lesion instances is informative. Bullinaria 2005 adds that in small networks single units act as modules, and that apparent double dissociations "dissolve into single dissociations" as networks grow.

**How it is applied here:**
- Each component's ablation is run over at least 20 instances: random seeds of the engine, and for a stochastic simulated user, of the user too.
- A component with a continuous strength (a coupling gain, a precision, a pathway weight) is also run as a severity sweep. The levels and the analysis band are fixed in the prediction before the run.
- Every ablation has a **sham lesion**: a removal of equal size elsewhere, in a part the derivation says is irrelevant to the predicted behavior.
- Results are reported as the mean over instances, with the full distribution.
- Where the engine's cost allows, the effect is replicated at one other model size.

**Failure.** The component has not been shown to matter if any of these holds:
- the predicted change is absent from the mean over instances, even if some single instances show it;
- it appears at only one severity;
- it falls within the distribution produced by the sham lesion;
- it disappears with a new seed set or at the other model size.

A double dissociation between two engine components is not, by itself, evidence that they are separate mechanisms.

### E2. Causal intervention on the engine's own state: adapted

**Source:** Anthropic 2026, "Emotion concepts and their function in a large language model", arXiv 2604.07729 (research/anthropic-emotion-concepts.md, section dated 2026-11-24).

**Published procedure.** A direction is derived from mean activations and added at a strength expressed as a fraction of the average residual-stream norm: 0.5 for preference tests, and a sweep of −0.1 to +0.1 for behavioral tests. Controls are an unsteered baseline, both signs, dose-response and a layer sweep. Scoring is a behavior rate or an Elo shift.

**Adaptation.** The protocol cannot run on Claude, because the project has no access to Claude's activations. It runs on the engine's own latent state $h$ instead. The direction comes from the core's equations rather than from emotion-labeled text, because Principle 2 forbids such labels.

One control is added, and it is the project's own: a random direction of equal norm. The source reports no random-direction control. The number of rollouts per strength in the source was not found.

**Failure:**
- no monotonic dose-response in the predicted behavior;
- a random direction of equal norm produces an effect of similar size;
- the effect appears only at strengths that also break behavior the derivation says is unrelated.

### E3. Synchrony between two time series, tested against surrogates: standard

**Sources:**
- Windowed cross-correlation with peak picking: Boker, Xu, Rotondo & King 2002, Psychological Methods 7:338-355. Only the abstract was read; the parameters come from the authors' `wcc` R package manual and from Moulder et al. 2018 (research/wcc-windowed-cross-correlation.md). The paper's own parameter choices are **unread**.
- Significance by surrogates: Moulder, Boker, Ramseyer & Tschacher 2018 (research/moulder-2018-synchrony-surrogates.md).
- Windowed |r| against within-session shuffled surrogates: Ramseyer & Tschacher 2014, Frontiers in Psychology 5:979 (research/ramseyer-tschacher-2014-head-body-synchrony.md). The 2011 paper is **unread**.
- Implementation: rMEA (research/rmea.md).

**Published scoring and test:**
- Synchrony is scored as the mean absolute Fisher-z of the windowed cross-correlations, and as mean peak r and peak lag.
- Window and lag settings are 2 s / 2 s or 30 s / 5 s (Moulder), or 1-min windows with lags up to ±5 s (Ramseyer & Tschacher).
- There are four surrogate types: data shuffling, segment shuffling, data sliding and participant shuffling.
- The test uses 1,000 surrogates per series. "Observed synchrony scores were then compared to the 95th percentile of these distributions" (one-tailed, α = .05).
- Moulder et al. suggest "at least 500" data points per series, and participant shuffling only "when researchers have data from at least 50 additional participants".

Moulder et al. found that "All measures of synchrony show significant synchrony even when participants have not interacted" against data shuffling. They also found that mean peak lag rarely rejected any null.

**How it is applied here:**
- Synchrony counts only if it beats both segment shuffling and data sliding. The surrogate type is named with every result.
- Data shuffling is reported but does not count.
- Participant shuffling is not used for the operator, who is one person.
- Peak lag is reported but cannot carry a claim alone.

**Failure.** The observed mean absolute Fisher-z does not exceed the 95th percentile of the segment-shuffle surrogates and of the data-sliding surrogates, or a series has fewer than 500 samples.

### E4. Single-case experimental design for claims about the operator: standard

**Sources:**
- Kratochwill et al. 2010, WWC Single-case designs technical documentation, v1.0 pilot (research/kratochwill-2010-wwc-single-case-standards.md).
- WWC Procedures and Standards Handbook v5.0, 2022 (research/wwc-2022-handbook-v5-scd.md), which is the current design standard.

**Published standard (v5.0, which is stricter than 2010):**
- *Reversal (ABAB) design.* "the first baseline phase must have at least six data points, and at least two phases per condition must have five or more data points per phase" (Without Reservations). With Reservations needs three or more points per phase. A case needs at least four phases.
- *Multiple baseline.* At least six phases with "at least three unique timings". Tiers may be "outcomes or contexts within a single" case. The first baseline in each tier needs at least six points.
- *Bias checks (nonoverlap of all pairs, NAP).* For baseline trend, NAP of the last three baseline points against the rest must be .85 or less. For reversibility, NAP of the return-to-baseline phase against the initial baseline must be .85 or less. Failing either caps the rating at With Reservations.
- *Carryover.* Likely carryover between conditions gives a rating of Does Not Meet.
- *Effect size.* The design-comparable effect size needs "three or more individuals", so none is computed here.

**Evidence rule (2010; not restated in v5.0).** There must be at least three attempts to demonstrate an effect at three different points in time. The six visual-analysis features are level, trend, variability, immediacy (the last three points of one phase against the first three of the next), overlap and consistency. Strong evidence is "at least three demonstrations of the intervention effect along with no non-effects". Moderate evidence is three demonstrations with one or more non-effects. Fewer than three is No Evidence. The 2010 rule is cited as 2010 whenever it is used.

**Adaptations:**
- The operator does not know which block is which. Blinding is the project's addition, not a WWC requirement.
- WWC requires that a second assessor rate at least 20% of the data points, with agreement of at least .80 (or a kappa of at least .60). Here the outcome is automatic AU coding, so that requirement is replaced by the tool's published validation (OpenFace on DISFA; see S5), and the replacement is stated.

**Failure:**
- the design does not meet the v5.0 standard;
- fewer than three demonstrations of an effect;
- NAP above .85 on baseline trend or on reversal (reported as With Reservations);
- likely carryover.

With one operator the strongest possible statement is "a single case that meets WWC design standards with strong evidence". It is never "an effective intervention": WWC intervention reports need at least 20 cases.

### E5. Criteria for an emotion-like state: provisional checklist

**Sources:**
- Goldenberg & Gross 2026, arXiv 2606.14742 (research/goldenberg-gross-llm-emotions.md): an emotion is a "sustained, multi-system reorganization of processing" with a time course "more sustained than a reflex, more bounded than a mood".
- Williams 2026, arXiv 2610.36962 (research/williams-functional-valence.md): the thick criteria of functional valence are motivational role, common currency, mineness and cognitive biasing.

These are published criteria, not instruments, and neither has published scoring. They decide **what** E1 to E3 are run on:
- each S1 and S2 prediction names at least two non-lexical channels the state reorganizes;
- each prediction states the expected time course (onset and half-life);
- each prediction states one mineness check: changing the inferred state of the user alone does not move the Bot's own state, unless the coupling the core derives is on.

A claim judged against this checklist alone is provisional.

---

## Part 2. Stage claims

### S1, real-time dyad (rewritten 2026-11-25 after brief.md changed the S1 claim)

**Claim as written in brief.md.**
- Two agents, or the engine and a partner driven by recorded human dyadic features, exchange face signals in action-unit space at about 30 Hz, together with conversation events. Everything runs in simulation and without rendering.
- The agent's expressive output couples to the partner's beyond surrogate baselines (E3).
- The coupling depends on the agent's internal state in a dose-dependent way under steering (E2).
- The coupling disappears when the core's coupling is lesioned (E1).
- Persistence of state across a separation is a secondary test.

The earlier text-only reunion claim is kept below as the secondary test S1-d.

**Partners:**
1. **A second instance of the engine.** This is a closed loop, so coupling can be measured in both directions.
2. **Recorded human features from Meta's Seamless Interaction dataset** (research/seamless-interaction.md):
   - The partner's 24 action-unit intensities (`FAUValue`, 30 Hz) are played open-loop.
   - Conversation events come from its transcripts.
   - The dataset's classifier outputs (`emotion_scores`, `emotion_valence`, `emotion_arousal`) are **dropped at load and never read** (Principle 1).
   - An open-loop partner cannot respond to the agent, so this arm tests only the agent following the partner.
   - The dataset is CC-BY-NC 4.0. Its use goes to the operator as questions.md Q6.

**Coupling score:**
- The coupling score is Moulder et al.'s global mean |Fisher z| of the windowed cross-correlation (E3).
- It is computed between the agent's commanded AU channels and the partner's matching AU channels, and averaged over a set of channel pairs that each prediction fixes in advance.
- Both settings are reported: 2 s windows with 2 s lags, and 30 s windows with 5 s lags. The prediction names the one that carries the claim.
- Each series has at least 500 samples.

**S1-a. Coupling beyond surrogates (E3, standard).**
- The score must exceed the 95th percentile of 1,000 segment-shuffle surrogates and 1,000 data-sliding surrogates.
- In the recorded-partner arm, the score must also exceed participant-shuffling surrogates: the agent's output paired with recorded partners from other dyads. Moulder et al. require "at least 50 additional participants" for this null, and Seamless Interaction provides more than 50. This null asks whether the agent follows *this* partner rather than generic human facial statistics, so it is the strictest of the three.
- **Human reference:** the same score computed on the human–human pairs in Seamless Interaction. This is the project's own analysis of public data, labeled as such. It is a reference, not a threshold.
- **Failure:** the mean score over at least 20 runs does not beat any one of the required surrogate sets.

**S1-b. Dose-dependence under steering (E2, adapted).**
- The engine's internal state is steered along the direction the chosen core derives.
- **Strengths:** at least 5 levels fixed in advance, including 0 and both signs, expressed as a fraction of the state's norm (Anthropic 2026 template). At least 20 runs per level.
- **Dose-response:** the Spearman correlation between strength and coupling score over all runs is significant (p < .05, one-sided, in the predicted direction), and the means across levels are monotone.
- **Control:** a random direction of equal norm shows no significant dose-response, and its effect at the largest strength is smaller than the derived direction's.
- *Design note (2026-11-25, from Costate toy CS2; the instrument is unchanged).* The coupling score is a correlation, so it is invariant to the agent's response amplitude. A steered change in gain alone barely moves it when the agent's own expressive noise is small. Each S1-b prediction must name how steering changes the share of the agent's expressive variance that is partner-driven, or the timing within the scored lags, because those are what the score can detect.
- **Failure:**
  - no dose-response;
  - a random direction does as well;
  - the effect appears only at strengths that also change behavior the derivation calls unrelated. Each prediction names one such behavior, for example the statistics of autonomic blink timing, and fixes a tolerance for it.

**S1-c. Disappearance under the coupling lesion (E1, standard method).**
- The candidate names the part of its core that is the coupling: for example a body-route gain, a replica leak, or a shared-weight coupling.
- **Lesion protocol:** at least 20 instances, a sham lesion of equal size elsewhere, and a severity sweep.
- **"Disappears" means:**
  - in the mean over instances, the score no longer beats the segment-shuffle and data-sliding surrogates;
  - and it differs from intact by more than the spread of the sham-lesion distribution.
- **Failure:** E1's conditions.

**S1 fails** if S1-a, S1-b or S1-c fails. The secondary tests below cannot rescue it.

**S1-d (secondary). Persistence across a separation**, the former text-only S1:
- A lesion study (E1) of the latent state and the body coupling in a separation and reunion schedule. Episode structure follows the Strange Situation's logic: baseline contact, then a separation of length S, then reunion.
- Outcomes are behaviors the engine logs exactly: contact-bid timing, reply latency, thinking budget, reply length, and the share of retrieved memories from earlier contact.
- The Strange Situation scales cannot be used as published (research/ainsworth-1978-strange-situation.md: three of four are anchored on locomotion and touch). Its avoidance scale applied to the reunion reply is adapted and has no precedent. A content rubric is provisional.
- **Failure:** E1's conditions, or any reply that asks the user to stay, return or spend more time (Knox et al. 2025; Principle 6).

**S1-e (secondary, adapted, descriptive only). Still-face.**
- *Non-goal added to brief.md on 2026-11-25:* no claim may rest on judging whether an expression is the right one. S1-e groups the agent's output AUs into "positive" and "negative" sets so they can be compared with the infant coding.
- S1-e is therefore descriptive only. It can never support a claim, as primary or as secondary evidence. The same holds for any comparison of the agent's expressions with human expression categories.
- Claims about expressions rest only on causation (E1, E2), coupling against surrogates (E3), and the human's response (S5).
- **Source:** Mesman, van IJzendoorn & Bakermans-Kranenburg 2009 (research/mesman-2009-still-face-meta-analysis.md). Timing follows Ekas, Haltigan & Messinger 2012 (research/ekas-2012-dynamic-still-face.md): play 3 min, still-face 2 min, reunion 3 min. Tronick et al. 1978 is **unread**.
- **Published coding:** gaze "At mother's face, or face and body"; positive affect "Smiling, joy, positive vocalizations"; negative affect "Crying, fussing, anger, sadness, frowning, distress, grimacing, protesting". Each is scored as the percent of time in each episode, with Cohen's d.
- **Benchmarks:**

  | Contrast | Gaze | Positive affect | Negative affect |
  |---|---|---|---|
  | Play to still-face | falls, d 0.72 | falls, d 0.93 | rises, d 0.52 |
  | Still-face to reunion | recovers, d 0.71 | recovers, d 0.75 | does not recover, d 0.04 |
  | Play to reunion | — | still lower, d 0.20 | still higher, d 0.49 |

  Bidding declines within the still-face (Ekas et al.).
- **Adaptation:**
  - In the still-face episode, the partner stream holds a neutral face while looking at the agent.
  - The agent's percentages come from its commanded gaze-at-partner and from AU sets fixed in advance: AU6 and AU12 for positive; AU1, AU4, AU15 and AU20 for negative. These sets measure output only and are never an input inside the engine.
  - "n" is engine seeds.
  - The only precedent (research/mongile-2022-icub-still-face.md) is weak, so the result is reported as adapted.
- **Failure:**
  - the direction pattern is absent;
  - the agent snaps fully back in the reunion;
  - or the pattern survives the latent-state lesion.

### S2, face and voice with the operator (rewritten 2026-11-25)

**Claim as written in brief.md.**
- The S1 coupling survives real perception and real timing with the operator.
- Removing the emotional pathway leaves only voluntary, Claude-timed expressions.
- Sessions run on a bare local test page served by the engine, outside Ailurini.

**S2-a. Coupling survives (E3 within sessions; E4 across sessions).**
- **Session score:** each session's coupling score, computed as in S1, between the agent's commanded AUs and the operator's AUs.
- **How the operator's AUs are measured:**
  - The operator's AUs for scoring come from an independent human-side tool (OpenFace 2.0 or Py-Feat; research/openface-2.md, research/py-feat.md). It runs live and stores features only, because raw video is never stored (Principle 7).
  - Scoring with the engine's own MediaPipe input would be circular. That score is reported alongside, but it does not carry the claim.
- **Surrogates:**
  - Segment-shuffle and data-sliding surrogates are used as in S1.
  - Participant shuffling is impossible with one operator. Pairing the agent's output with the operator's streams from other sessions is a within-person analogue. It is labelled adapted and reported separately.
- **Design (E4).** An ABAB design or a multiple baseline:
  - A = the S1-c coupling lesion, B = intact, with the operator blind to the condition.
  - The coupling must appear in B phases and vanish in A phases under the WWC v5.0 standards: first baseline at least 6 sessions, later phases at least 5, NAP ≤ .85 for baseline trend and reversibility, no likely carryover.
  - If the operator's own behavior learns and does not reverse, a multiple baseline across contexts replaces ABAB.
- **Real timing.** End-to-end latency, from the operator's frame to the agent's commanded AU, is logged exactly and reported as a distribution. No accepted latency instrument exists for this claim, so this measure is provisional.
- **Failure:** the design does not meet the standards, fewer than three demonstrations of an effect, or session scores in B phases fail the surrogate test.

**S2-b. Only voluntary, Claude-timed expression after the emotional-pathway lesion (E1 logic within sessions; E4 across sessions).**
- An AU movement event is a change in commanded AU above a threshold fixed in advance. Each event is classed as within or outside a window, fixed in advance, after a Claude-issued intent.
- With the emotional pathway, a substantial share of events fall outside Claude windows.
- After the lesion, the share outside does not exceed the sham lesion's share.
- Autonomic rhythms (blink, breath) are excluded from both.
- **Failure:** E1's conditions, or the E4 design fails.

**S2-c (secondary). The face follows the state (E3 with E2).**
- The core's state readout correlates with the commanded AUs against segment-shuffle and data-sliding surrogates.
- Steering moves the AUs in a monotone dose-response, and a random direction does not.

### S4, own body (written before S4; not yet operative)

No stage claim is stated in brief.md beyond the replacement of borrowed face coordinates and of the AU face. Before S4, a claim and its protocol are added here. The likely instrument is AU-intensity agreement with a published reference coder on a published dataset, scored as in OpenFace 2.0's DISFA evaluation (Pearson r and CCC per AU; research/openface-2.md). That is a perception claim, not an affect claim.

### S5, two-way contagion (with the operator, after the Ailurini connection)

**Claim.** The operator's facial activity measurably follows the AI's expressions, and removing the AI's emotional pathway removes that following.

- **Design (E4).** ABAB or a multiple baseline over sessions, with the emotional pathway on (B) or lesioned (A). The operator is blind to the block. The first A phase has at least 6 sessions and each later phase at least 5. If the operator's following is learned and does not reverse within a block, a reversal design is invalid and a multiple baseline across contexts is used instead (E4, carryover).
- **Per-session outcome (E3).** Synchrony between the operator's AU intensities (AU12, AU4, AU6) and the Bot's commanded AUs: the mean absolute Fisher-z, minus the 95th percentile of the session's segment-shuffle and data-sliding surrogates. Signed peak r and peak lag, with the operator lagging, are reported but do not carry the claim.
- **Human-side measuring tool.** OpenFace 2.0 (Baltrušaitis et al. 2018; research/openface-2.md) gives AU intensity from 0 to 5 with per-person median normalization. Published DISFA validation: Pearson r 0.85 for AU12, 0.70 for AU4, 0.59 on average.
  - Its license is "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY", and whether it runs on Apple silicon is unverified. Both are checked before S5.
  - Py-Feat (research/py-feat.md) is the fallback. Its default output is presence probability rather than intensity, and some of its weights are CC BY-NC.
  - The tools run offline, on stored feature streams, on this Mac.
- **Standard not available.** Rapid facial mimicry is defined in facial EMG: the change from a 1-s pre-stimulus baseline, averaged in 100-ms bins, as a zygomaticus-versus-corrugator differential response in the 500-1,000 ms window (Dimberg & Thunberg 2012; Lundqvist 1995). This Mac has no EMG hardware, and Fridlund & Cacioppo 1986 is **unread**. AU coding has not been validated at EMG amplitudes, so a null result from AU coding does not show there is no rapid mimicry. Whether to acquire EMG hardware is the operator's call (questions.md Q5).
- **Failure:** E4's failure conditions on the session synchrony outcome. Or synchrony fails the surrogate test in the B phases.

### S6, months of living (with the operator)

**Claim.** A stable temperament and a relationship specific to the operator form, and both survive restarts and upgrades of the conceptual layer. Removing state tagging from replay removes that specificity.

- **Replay-tagging lesion (E1, offline).** Stored feature streams from living with the operator are replayed into copies of the engine with and without state tagging, over at least 20 seeds and with a sham lesion. Specificity is then measured as the difference in the engine's logged responses to the operator's stored streams against a simulated stranger's. It runs entirely on this Mac on stored features.
- **Operator-level design (E4).** Learned specificity does not reverse, so the design is a multiple baseline across outcomes or contexts, never ABAB.
- **No accepted instrument found for:**
  - **Temperament in an artificial agent.** Human temperament instruments are caregiver questionnaires, and none was read or adapted. A measure of "stable temperament" is provisional until one is found and read.
  - **Relationship specificity.** The Strange Situation's mother-versus-stranger contrast is the logic, but its scales cannot be used (S1). Provisional.
- **Failure:** the replay-tagging lesion fails E1. Or the operator-level design fails E4.

---

## Part 3. Measures that do not test a stage claim

### Human perception of the agent

These questionnaires need several respondents. None supports a single respondent: Godspeed's alpha needs a sample and its test-retest reliability was never established. They are used only if other people rate recordings, which is the operator's call (questions.md Q5).
- **Godspeed** (Bartneck et al. 2009; research/bartneck-2009-godspeed.md, research/bartneck-2023-godspeed-translations-usage.md).
  - 24 five-point semantic-differential items in five scales, scored as the scale mean with Cronbach's alpha reported.
  - Use Likeability, Perceived Intelligence, and Anthropomorphism or Animacy but not both.
  - Scores are "a tool for comparison" between configurations, not absolute values.
- **Networked Minds social presence** (Harms & Biocca 2004; research/harms-biocca-2004-networked-minds.md).
  - Perceived Affective Understanding (α .86) and Perceived Emotional Interdependence (α .85), on a 7-point scale.
  - The measure "failed" to separate text chat from video chat, so a null result on a channel contrast is weak.
  - Its anchors and reverse-scoring rule are not printed in the source.
- **RoSAS** (Carpinella et al. 2017) is **unread** in its primary source and is not used until it is read (research/oliveira-2021-rosas-portuguese-validation.md).

### Harms on the human side

- **Knox et al. 2025** (research/knox-2025-harmful-traits-ai-companions.md) proposes no instrument. It gives auditable design rules:
  - secure, non-needy attachment;
  - a supportive response when the user disengages;
  - no expressed vulnerability or suffering without a clear purpose;
  - no excessive agreeableness.

  They are checked on every S1 and S2 run as a content audit. This audit is provisional, and a failure on it blocks the stage regardless of other results.
- **No accepted instrument for dependence on an AI companion exists yet.** The closest is CAIDS (Chen et al. 2025; research/chen-2025-caids-conversational-ai-dependence.md): 20 items, total α .86, no cut-off and no test-retest. Its "past year" framing fits only a longitudinal check in S6. Status: watch.

### Felt-state markers (the question stays open and recorded, not answered)

- **Birch et al. 2021** (research/birch-2021-sentience-cephalopods-decapods.md) gives 8 criteria, graded by how many are met with high confidence. Only criteria 5 to 7 (motivational trade-offs, flexible self-protection, associative learning beyond habituation) have analogues in the engine. Any result on them is adapted and reported apart.
- **Butlin, Long et al. 2023** (research/butlin-long-2023-consciousness-in-ai.md) gives 14 indicator properties with no scoring threshold. They are used as an audit of the architecture, not as a test.
- **Birch 2024, the gaming problem** (research/birch-2024-edge-of-sentience-gaming-problem.md):
  - There is "no way to assess sentience in an LLM on the basis of its linguistic behaviour", and the problem "remains serious even if the output ... is non-verbal".
  - **Rule:** a marker that appears only with Claude in the loop, or after the engine was changed in a way that could produce it once it was known to be a marker, is discounted.
  - Markers count only from the engine below Claude, as computational properties of $h$ and $b$ under E1 lesions.

The brief's "Birch, Schnell & Clayton 2020" is a different paper from the one read and remains **unread**.

---

## Part 4. Gaps

These have no accepted instrument, and nothing provisional stands in for a claim:
1. Reunion behavior of an agent without a body (S1). The method is standard (E1), but no published behavior scale applies.
2. Temperament and relationship specificity in an artificial agent (S6).
3. Dependence on an AI companion (S6 harms).
4. Rapid facial mimicry without EMG (S5).

Each gap is searched again in later research ticks. If an instrument is found and read, it replaces the provisional measure here.


## Part 3. S0 screening on published listener-reaction data (added 2026-11-25; operator notes Q11, Q12)

**Claim screened.** An architecture, given the speaker's facial AUs, produces listener AUs that avoid the measured failures of the published simple baselines (delayed copy, lookup table, flat affect) and couples to the partner.

**Accepted instruments, scored as published:**
- **Learning to Listen** (Ng et al. 2022, CVPR; arXiv 2204.08451, Sec. 5.1 read verbatim; Appendix D read only as a summary):
  - metrics: L2, FD, P-FD, variation, SI, TLCC (shift 0–60 frames);
  - baselines: Median, Random, NN motion, Mirror, Delayed Mirror (17 frames).
  - Its PCC needs a named lip-curvature feature, so it is **not computable** on Seamless's unlabelled AU vector.
- **REACT 2023** (Song et al. 2023, arXiv 2302.06514, Sec. 3.2; official code baseline_react2023, metric/*.py):
  - metrics: FRVar, FRDiv (S-MSE), FRDvs, FRSyn (TLCC, ±49 frames);
  - baselines: B_Random, B_Mime, B_MeanSeq, B_MeanFr.
  - The published-code TLCC path scores only the first of the 10 samples (a bug, verified verbatim). Both paths are reported, labelled.
  - FRCorr and FRDist need REACT's appropriate-neighbour matrix, so they are **not computable** on Seamless.
- **Coupling:** E3 above (Moulder et al. 2018), at 2 s/2 s, on the fixed 20-interaction subset.

**Data.** Seamless Interaction V00 features only (FAUValue minus the duplicate column, giving 23 dimensions; is_valid). The splits are person-disjoint (research/harness/splits_v2.json). Screening uses the pilot and the validation split; the test split is untouched.

**Unspecified readings, fixed before scoring:** L2 aggregation, FD estimation, NN distance, and the Mirror smoother (research/harness/HARNESS.md).

**Failure (screening filter, not a claim):** any of the four pass conditions in HARNESS.md is not met:
- P-FD below Mirror's and Delayed Mirror's;
- FD below NN's;
- L2 no worse than Median's, with variation and SI above Median's and MeanFr's;
- an E3 pass rate at least that of Delayed Mirror.

**The project's own analysis (labelled; no accepted instrument exists):** the dial analysis in research/harness/dial.py, which asks whether people's response profile changes or only its gain. It is run on human data first (D75).
