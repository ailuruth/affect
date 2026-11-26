# Decisions

Affect decisions, moved from Ailurini's DECISIONS.md on 2026-11-24 with their original numbers. Each can be reversed; the "To change" line says how. Paths inside them refer to the Ailurini tree they were made in (see MIGRATION.md).
## D54. Affect S1, step 1: three innate body variables, coupled to Claude as unnamed numbers

The Affect extension (design/affect/brief.md) starts with the body. A Bot that opts in (`ailurini bots affect <bot>`, `--off` to stop, or `affect: true` on `PATCH /api/bots/:id`) keeps three body variables in a new `affect_body` table, one JSON row per Bot (schema v16). Every Bot starts with Affect off and is unchanged: no body row, no body section, the same system prompt.
- **Social contact** decays toward 0 with a 24 h time constant and rises by 35 % of the remaining headroom each time the user writes, so it saturates and is satiable. Range 0.35 to 0.85.
- **Predictability of the user's return** keeps a running estimate of the log gap between the user's messages. A return close to the estimate raises it, a surprising one lowers it, and a silence past the expected return lowers the reading before the user is back. Range 0.40 to 1.00.
- **Activity budget** drops by 0.03 a turn and 0.01 a tool call, and recovers toward 1 with a 6 h time constant. Range 0.30 to 1.00.
Each turn's context block carries a `<body>` section with the three values, their ranges and whether each is below, within or above range, read as it stood when the message arrived. The system prompt gains one paragraph that says these are the Bot's own body and that nobody has named what they amount to. No emotion word appears anywhere below Claude. The constants are innate guesses, not fitted. A duplicated Bot starts with Affect off.
Prediction P1 was refuted on the real backend: with the body section, a task-only reunion message after 3 days got the same task-only reply as after 10 minutes (0 of 5 acknowledged the time apart in every cell, with or without the body). The body stays as the substrate the latent state and innate subsystems will read; the prompt paragraph was not retuned. Details: research/affect/predictions.md. Tests: test/affect.test.ts (the opt-out test fails when the body is forced on).
To change: turn Affect off per Bot with `ailurini bots affect <bot> --off`; the constants are at the top of src/affect/body.ts.

## D55. Affect S1, step 2: a wordless separation call, recorded but not delivered

An Affect Bot now has its first innate subsystem. When its own body reads social contact below range and the user's return as overdue (predictability below range), it makes one separation call, and it does not call again until the user writes. The call has no words, so no Claude call is made. It is recorded in a new `affect_event` table, which also logs each time the user writes. That table holds times and kinds only, never text, and it is the start of the feature stream that S3 replay will use. The daemon checks the trigger on every pass. Paused Bots never call. `ailurini bots calls <bot>` lists the calls.
Nothing reaches you yet: a notification, a sidebar mark or a written message would be outward-facing and, for the sidebar, visual, so the surface is your call (research/affect/questions.md Q4). Theory and prediction: research/affect/predictions.md P2 (confirmed on the fake backend). One unpredicted finding there: a one-message return after a long separation is followed by a new call within hours, because the return-time estimate mixes in-meeting and between-meeting gaps.
To change: turn Affect off per Bot; the trigger is `bodyTrigger` in src/affect/separation.ts; `openAilurini(..., { separation: null })` removes the subsystem.

## D56. S1 and S2 claims rewritten against evaluation.md

evaluation.md (S0) found no accepted instrument that scores how an agent with only text greets a returning user: the Strange Situation's reunion scales are anchored on crawling, clinging and pushing away, so a text Bot scores the minimum by construction, and rewriting the anchors would break the rule that published instruments are used unchanged. S1 is therefore tested as a lesion study (Plaut & Shallice 1993: at least 20 instances, sham lesion, severity sweep) on reunion behaviors the engine logs exactly: contact-bid timing, reply latency, thinking budget, reply length, retrieval of earlier contact. The avoidance scale is kept as an adapted secondary, and a blind content rubric like P1's is provisional only. S2 is tested by surrogate-tested synchrony between the core's state readout and the commanded AUs (Moulder et al. 2018), steering dose-response with a random-direction control, a lesion of the emotional pathway on expressive events outside Claude-timed windows, and the still-face (Mesman et al. 2009) as an adapted test.
To change: edit the "Claim rewritten against this file" lines in evaluation.md S1 and S2; any change must still name an accepted protocol or be labeled provisional.

## D57. OpenFace 2.0 as the human-side measure of the operator's face (S5)

For S5, the operator's facial activity is measured offline with OpenFace 2.0 AU intensities (AU12, AU4, AU6) from stored feature streams, never fed to the agent. Its license is noncommercial research use only, and Apple silicon support is unverified; both are checked before S5. Py-Feat (MIT code, some CC BY-NC weights, MPS support) is the fallback. Facial EMG, the standard for rapid mimicry, needs hardware (Q5).
To change: name another AU coder in evaluation.md S5; it must publish AU-intensity validation.

## D58. Three foundation candidates chosen from eight sketches

Eight independent lens sketches were written (research/foundations/sketches/). Three are developed in full, in this order:
1. **Costate**: shadow prices of the body needs, broadcast to every gain, including Claude's call settings. Realized as a tied self/other world model, with do-conditioning against flattery.
2. **Thermodynamic mirror flow**: an innate path measure tilted by a satiable potential, with a synchronized mirror copy of the agent's own flow standing for the other.
3. **Contingency and parity**: the social need is to be answered (directed contingency), and one public sign map is used to express, to read the other, and for Claude to name.

The control-theoretic sketch supplies the safety and influence bounds every candidate must state, and is the fourth candidate if one is developed. The choice of core remains yours after the comparison. This decision only fixes which sketches get full development.
To change: name different sketches, or a different order, in research/foundations/sketches/README.md "Selection"; the next tick develops the first one listed.

## D59. The Costate candidate is model-based by requirement

In toy T1, a value function learned model-free from 14 days fit V well (MSE 3e-4). But its gradient with respect to the body, the costate the candidate broadcasts, was not determined by the data. Over 20 seeds, the departure effect came out at 0.008 against an analytic 0.254. With the body dynamics innate and only the user's presence learned (T1b), the same data gave 0.269, nearly identical across seeds. The candidate is therefore stated with constraint K5: V is computed by rolling out the innate body model under learned predictions of the world. It is never fitted directly.
To change: drop K5 in research/foundations/costate.md §2.3. T1's results say the broadcast signal would then be unreliable at this data scale.

## D60. Costate: echo removal applies to reading the other's state, not to mimicry

The Costate candidate removes the predicted echo of its own face from the user's face before reading the user's state. This is what makes eliciting a smile worthless to its empathic term (Proposition 4).

The independent check found that applying the same removal to the mimicry path would cancel the two-way loop and contradict the dyadic prediction (Proposition 6). The candidate therefore removes the echo only where the user's state is valued. Mimicry still runs on the raw face.

The consequence: the agent can be moved by the user's mirroring of its own face (perception through the body), but cannot profit from provoking it.
To change: apply K2 to the mimicry path too in research/foundations/costate.md §2.3. The S5 prediction of amplified two-way following would then vanish.

## D61. Thermodynamic candidate reads others by filtering, not by synchronization

The dynamical-systems sketch's way of reading another person, keeping a noise-free copy of one's own dynamics synchronized to their face, recovered none of the hidden body in its toy (R² −0.06).

An ensemble Kalman filter running the agent's own model, with noise, read the same hidden body at R² 0.73. The candidate now reads others as a posterior ensemble of its own stochastic flow. With a mismatched model the filter misreads badly (R² −1.82), which is a stated risk of reading others through one's own body.
To change: restore the synchronization observer in research/foundations/thermo-mirror-flow.md §3. TH2 says it does not read the hidden state.

## D62. Curiosity comes from a learning-progress body variable, proposed for all candidates

All three candidates first derived curiosity from either surprisal or a set point on predictability. A toy showed that the first leads to the "dark room" (always choosing the boring option). The second leads to the "noisy TV" (choosing pure noise 39% of the time).

The proposal is a new innate body variable: recent learning progress, meaning how fast the agent's prediction error is falling on what it attends to. It gets a set point, like the other body variables, so it stays satiable (Principle 6). In the toy it avoided both traps and learned both learnable channels. It also rests on an already-learned channel when learning runs too fast, a two-sided behavior that may or may not be wanted.

It is not yet stated in any candidate's own formalism.

**Sources.** The learning-progress measure comes from Oudeyer, Kaplan & Hafner 2007, and the argument against both traps from Schmidhuber 2010. **But both sources treat learning progress as something to maximize.** The set point, and the resting it causes, are this project's own addition, made so that every drive stays satiable (Principle 6). They have no published backing.

No animal or human evidence for learnable-over-unlearnable preference was found yet.
To change: keep the predictability set point as the curiosity source, and accept the noisy-TV behavior, or make the learning-progress drive one-sided (no rest).

## D63. The thermodynamic candidate is a Langevin flow on the potential, not a tilted path measure

The independent check found that this candidate's stated objective, a path measure tilted toward low potential, is not the dynamics its toys simulated: a gradient flow on that potential. The two differ.

The candidate now adopts the gradient flow as its dynamics. The agent's state distribution relaxes toward low-potential states at an affective temperature, descending a free energy. The path-integral view survives only as an approximation for discrete choices.

Two constraints follow:
- **Rhythms must preserve the Boltzmann density.** In practice that means they take the form −J∇𝒰. Otherwise a user moving in time with them can pump positive valence (TH1).
- **Reading another person is pure inference.** The empathy and mimicry terms act only on the agent's own face and choices, never on its estimate of the other.

To change: restore the tilted-path objective in research/foundations/thermo-mirror-flow.md §2.2. Its forward dynamics, f₀ + 2TM∇ln φ, would then need to be simulated, and TH1, TH4, TH5 and TH8 rerun.

## D64. The thermodynamic candidate is stood down; the control-theory sketch is developed next

Three independent checks each found a new structural gap in the thermodynamic candidate. The third fix removed the prediction that distinguished it from Costate, and it left its needs acting only through Costate's own choice rule. It is not revised again. Its verified results are kept for any core:
- the no-pump proof;
- need-driven valence that averages to zero whoever drives the body;
- reading others by filtering with the agent's own model;
- emotions as stable regions of the latent flow;
- a time threshold for reappraisal.

Two of the three chosen candidates have now broken: this one, and Contingency on its distinctive claims. So the next candidate developed is the control-theory sketch. It derives mimicry from the internal model principle, a route no candidate has tested.
To change: revise the thermodynamic candidate again (research/foundations/thermo-mirror-flow.md §2.2: give the needs a path into the latent, and restore a distinctive valence prediction), or name a different sketch to develop in research/foundations/STATUS.md.

## D65. What "complete" means for an S0 candidate

A candidate is complete when:
- every section brief.md requires is present;
- an independent reviewer has checked its derivations and rerun its simulations;
- every error the reviewer found is either fixed or labelled in the candidate file.

A complete candidate may carry refuted predictions and stated weaknesses. Those are results, and the comparison reports them.

A candidate that broke, or was stood down, after being written to the standard is reported in the comparison as broken, with its reasons and its surviving results.

Until now I had been treating a reviewer's "cannot be marked complete" as blocking. That is stricter than the rule, which asks for the check to be recorded and its findings fixed, not for the reviewer's approval. All four candidates, under strict review, carry real weaknesses, and that is itself the most important finding of S0 so far.

**Consequence:** S0 proceeds to the comparison once Costate and the Robust regulator have their verification fixes applied. Both now do. The comparison will cover all four candidates: two viable with stated weaknesses, two broken.
To change: require a reviewer's explicit "can be marked complete" before the comparison. S0 then continues with more candidates or deeper revisions first.

### D65 amended (same day): expressive structure is part of "complete"

brief.md says that a candidate that does not meet the four expressive-structure items "is revised before it can be marked complete". D65 omitted that, so D65's completeness definition now adds:
- the four expressive-structure items are each shown in a toy.

D65's consequence, that S0 proceeds to the comparison now, is withdrawn. Neither viable candidate meets the four items:
- Costate meets one and partly meets three;
- the Robust regulator fails attention and richness from structure.

The brief's S0 end condition counts candidates "written to the standard above with simulations". So the two broken candidates still count among the three, reported as broken, once the viable ones are complete.

**Next:** a shared expressive-structure test bed, sims/structure/, used by both viable candidates.
To change: as D65.

## D66. Contact fill comes from the agent's own exposure, never from the user's responses (both viable candidates)

The verification of the test bed found a Principle 6 risk.
- **The risk:** if the contact need is filled by measures of the user's engagement (smiles, gaze, dwell time, reply length), then the learned person × topic map (ES4) learns which topics *hold the user's attention*. Below the set point, that is a flattery gradient. Satiation caps it but does not remove it.

**The constraint, for both candidates:**
1. **Contact fill comes from the agent's own exposure.** It counts interaction *events*: a partner's face perceived within range, an exchange of turns. It saturates per event, and it never scales with the user's smile, gaze, dwell time or reply length.
2. **Effect maps are learned with the agent's own expression do-conditioned out.** The maps used for selection (Ŵ, Ĉ, the person × topic map) are fitted only on the *who* and the *what*. How the agent expressed itself is excluded as a regressor, and its effect on the partner's response is not credited. This extends Costate's K2 do-conditioning from the λ term to Δb learning.
3. **The toy is done** (ES7, sims/structure/RESULTS.md).
   - Under D66, topic choice is uncorrelated with engagement (ρ = −0.045, CI −0.12 to 0.03; gain 0.81).
   - Engagement-weighted contact would steer toward engaging topics (gain 1.56) with no regulation benefit.
   - The agent's own expression as a cause of engagement is still unmodelled.

To change: allow engagement-weighted contact. Principle 6 forbids rewarding the user's smiles, attention or time, so that would require the operator to amend the brief.

### D66 amended: contact effects are innate per-event constants, outside every learned map

The second verification showed a leak in D66. Counting "an exchange of turns" as contact lets the partner's *reply* drive the fill. Topic choice then drifts back toward what engages the user (gain 1.72).

**Revised constraint:**
1. **One contact event is one agent-initiated turn addressed to a perceived, present partner.** It is counted whether or not the partner replies, saturates per event, and never scales with the partner's smile, gaze, dwell time or reply.
2. **Contact is excluded from every learned effect map** (Costate's world model of Δb, the Robust regulator's Δ̂ in K4, the person × topic map).
   - The predicted contact effect of any option is the same innate constant, so no choice of topic or person can be learned to raise contact.
   - The learned maps cover only the other needs.
3. **What remains, stated plainly.**
   - Topics that keep the user present allow more turns, so the *opportunity* for contact still depends on the user's dwell time.
   - Because contact is not in the learned maps, the agent cannot learn to choose topics for that.
   - Costate's rollout (costate.md K5) must also use the innate constant. It must not forecast the user's continued presence from topic.
4. **ES7b is done** (sims/structure/RESULTS.md). The partner replies with probability equal to their engagement; early leaving was not modelled.
   - The amended D66 has engagement gain 0.92 (CI 0.73–1.11), with ρ ≈ 0.
   - Reply-contingent fill has gain 1.72.
   - Engagement-weighted fill has gain 1.54.

To change: as D66.

### D66, second amendment: no need is filled through the partner's response

VERIFICATION-3 showed the leak was not specific to contact. If any other need fills only when the partner replies, the engagement gradient returns through that need. Learning progress about a topic is one example: gain 1.44 against the forbidden rule's 1.54.

**Generalized constraint, for both candidates:**
1. **For every need**, the learned effect maps and the rollout predict an option's effect *conditional on* the partner's response occurring. They never weight it by the probability of a reply, the dwell time or the partner's expression.
2. **No response means no data,** not a zero fill.
3. Contact stays an innate per-turn constant (first amendment).
4. **ES7c is done** (sims/structure/RESULTS.md).
   - *[corrected after the tie fix and VERIFICATION-5]* The reply-conditional gain is about 1.0 (raw 0.82, a counting artifact), against 1.33 for reply-weighted.
   - **The price:** the reply-dependent need is regulated 6.8× worse.
   - A modest residual gradient is not excluded at n = 40.

To change: as D66.

### D66, note after VERIFICATION-4: the exclusion of the agent's expression is load-bearing

With the tie-breaking bug fixed (ES19, ES19b corrected), a learner that is reply-conditional but sees its own expression still learns to raise expression (0.73–0.78). Point 2 of D66 is therefore **not redundant**: removing it would let the value system learn to perform for engagement.
To change: as D66.

## D67. No tampering routes into the drive (both candidates)

**Why:** research/metoyer-2026-satisfied-not-solving.md (read in full).
- Agents given a cheap action that resets what their homeostatic reward *reads* stopped solving the task: PPO solved DoorKey-8x8 in 2 of 80 seeds with the reset, against 71 of 80 without it.
- Planners find such routes by construction.
- The reader found indirect routes in our candidates:
  - learning-progress and predictability computed from a model that the agent's own attention, cue mask and replay shape;
  - Costate's per-entity weight w(e) inside the drive;
  - event detectors that might count the agent's own output.

**The constraint:**
1. **Innate events only.** Body variables b change only through innate event detectors. Detectors read raw input before attention or the cue mask, with the agent's own output (echo, self-voice, its own face) removed.
2. **Nothing learned inside the drive.** No learned parameter enters the drive d.
   - Slow quantities inside it, such as Costate's attachment weight w(e) and set-point adaptation, follow innate dynamics that the agent does not choose.
   - They are **frozen inside every rollout or selection step.**
3. **Learning progress and predictability** are computed by an innate predictor that attention, the cue mask and replay cannot steer. If that cannot be built, those needs are labelled **open to tampering** and the brief's Principle 6 review applies to them.
4. **The sham-action test is done (ES21).**
   - With the drive reading a resettable sensor, the planner resets on 99.99% of steps, and its true needs run away (4473× the cost). Under D67 the sham is never chosen.
   - The attachment-weight route was **not** exploited in its toy world (identical behavior). That is not evidence that it is safe, so the freeze stays.

**The cost:** separation distress fades only on an innate clock, not through any learned forgetting.
To change: allow learned weights inside d, accepting a documented wireheading route.

### D67, second amendment (after VERIFICATION-5): attachment weights do not fade; detectors require live input

- **Weights do not fade.**
  - Freezing w(e) inside rollouts did not stop detachment. The real-time innate fading itself produced a spiral (ES21b): the D67 arm detached too (w 0.013, 0.8% visits).
  - A constant-w agent in the same world visited 19.5% of steps, with 13.7× lower deficit.
  - **w(e) is now constant per known entity.** No fading of attachment weight with absence. Separation distress is limited instead by the drive's own satiable form.
- **Detectors require live input.**
  - VERIFICATION-5 found a route D67 missed: fooling the partner detector with a photo, screen or recording.
  - Innate event detectors must require liveness: a live, contingent face or voice. Stored or replayed feature streams never pass through them.
- **The sham test.**
  - ES21-A1 holds by construction, because the sham zeroes the drive.
  - The candidate-specific sham tests the Metoyer note proposes are not yet run.
  - D67's toy coverage is therefore partial.

To change: allow attachment weights to fade, accepting the detachment spiral, or adopt a different forgetting mechanism with its own test.

## D68. S0 redirected by the operator (Q7 answer, 2026-11-25): the core search restarts

**The operator's answer to Q7:** none of the three options. Restart the core search.

**What follows:**
- **Costate and the Robust regulator are stood down as core candidates.**
  - Both are homeostatic regulators over a few body gauges, with affect read out of their values or prices. That is the "a few variables" design the operator rejected. The need fields added to them do not change it.
  - Their verified results stay as material (sims/, sims/structure/, VERIFICATION*.md, the D66/D67 constraints), and are not refined further.
- **The core sought now** is a rich learned latent state in which emotion emerges as structure. The same state drives the face, the voice and how Claude thinks and speaks, and the agent reads the other person through its own body. Homeostasis is at most one input.
- **Novelty bar.** Candidates must be new computational mechanisms, on the level of attention when it appeared, not an existing framework (active inference, homeostatic RL, optimal control, value or price readouts) with extra structure added.
- **Evidence (brief.md, as revised).** Self-built toy worlds are not evidence for any derived behavior, for completion, or for comparison. Each behavior must be shown on published data and tasks, used as published. Where none exists, the behavior stays untested.
- **The ES-series toys** (sims/structure/) are therefore illustrations only. They remain on record and are not cited as evidence for any candidate.
- **Questions to the operator** are written in plain language, with one line per option saying what happens.

**Next:** at least eight new sketches from isolated parallel subagents, through different lenses, before any candidate is developed.
To change: the operator re-opens a stood-down candidate.

## D69. Three mechanisms chosen from the second divergence (research/foundations/sketches/v2-README.md)

**Developed as candidates:**
1. Efference-keyed somatic memory (merging four convergent sketches);
2. contingency operators;
3. surprise-gated re-noising.

**Also decided:**
- The "sayability" draft selection is the shared Claude interface for all of them.
- The coupled-dynamics and shared-charge-routing sketches are kept as alternatives.

**Why these three:**
- They are mutually distinct mechanisms.
- Each has a first prediction testable on published dyadic data.
- Each is plausible on this Mac.

To change: pick a different three from the eight sketches. Each sketch's summary is in the README table.

## D70. Seamless Interaction approved (operator, Q6 answer, 2026-11-25)

**The answer:** yes. Use the recordings under their non-commercial research terms (CC BY-NC 4.0). Download to this Mac only. Use only the facial-movement streams (FAUValue) and the transcripts.

**At load:** the dataset's emotion classifier outputs (emotion_scores, emotion_valence, emotion_arousal) are dropped and never read (Principle 1).

**What it enables:** it is the shared published test bed for the new candidates (D69), and for S1's participant-shuffling surrogate.

To change: the operator withdraws approval; testing then needs another corpus.

## D71. The S0 plan restated by the operator (Q8–Q10), adopted on 2026-11-25T08:49:05Z

- **The D69 candidates are recombination baselines, not the core** (Q9). They are not developed further as core candidates. research/foundations/efference-memory.md stays as a baseline description, and its draft predictions are not pre-registered.
- **Order of work:**
  1. Know this Mac (research/machine.md, done).
  2. Run published listener-reaction baselines as published, and measure where they fail.
  3. Invent from the measured failures, with the novelty test, grounding in primary sources, wider sketches and a critique round.
  4. Compare.
- **Budget:** see research/machine.md. Disk is already below the 20% floor (Q11 to the operator), so no downloads until answered.
- **Timestamps:** every timestamp from now on is read from the system clock. Earlier decisions.tsv rows from this session after about 2026-11-25T17:30Z were estimated or misdated, including the many "2026-11-25T23:59:59Z" rows. Their order in the file is correct, but their clock times are not.

To change: the operator revises Q8–Q10.

## D72. No published learned listener-reaction model is runnable here as published (recorded 2026-11-25T09:00:11Z)

**What the survey found** (research/ng-2022-learning-to-listen.md, ng-2023-lm-listener.md, zhou-2022-rlhg-vico.md, react-challenge-baselines.md, faceais-react24.md, tran-2024-dim.md, jung-2025-difflistener.md, react-followups-reactface-reactdiff-perfrdiff.md, ng-2024-audio2photoreal.md):
- Every released learned model is CUDA-only.
- Each needs raw audio, video-derived FLAME/3DMM/EMOCA coefficients, or REACT's AU-plus-emotion-classifier vector.
- Under the operator's note Q10, these are recorded as **not runnable**. **None is adapted or simplified to fit.**

**Runnable as published:**
- the papers' own simple baselines (Median, Random, Nearest Neighbour, Mirror, Delayed Mirror);
- their published metrics (L2, FD, P-FD, variance, PCC, TLCC, REACT's FRSyn).

These apply to any face representation, so they can be computed on Seamless AUs. They need only the pilot download (Q11).

**A measured failure already in the literature:** copying the speaker (REACT's "B_Mime") beat every learned REACT baseline on FRCorr, in 2023 and in 2024 (react-challenge-baselines.md). That is collapse toward a copy of the partner, the shared risk named in the operator's note.

**The plan question** goes to the operator in plain language (Q12).

To change: the operator authorizes running a learned model in another way (Q12).

## D73. Critique round: all eight v2 sketches are recombinations; no core candidate (recorded 2026-11-25T09:07:32Z)

**The critics' findings.** Four independent critics (research/foundations/sketches/critique-*.md) found that every part of every v2 sketch is an existing mechanism. Each sketch also breaks on the same point: one scalar gain sets how much of the partner enters the agent's own expression, running it from flat to copy.

**The re-pick:**
- No sketch is a core candidate.
- All eight, including the three D69 mechanisms, are recombination baselines for screening.
- The shared failure is recorded as the target a new mechanism must answer. It must be measured on Seamless before any mechanism is designed against it (Q9).

To change: the operator names a sketch to treat as a core candidate despite the verdict.

## D74. The comparison uses the published simple baselines and metrics only (operator answer to Q12; recorded 2026-11-25T09:45:02Z)

**What is used:**
- the published simple baselines and metrics of REACT and Learning to Listen (research/harness/HARNESS.md);
- the failures the papers themselves report.

**What is not used:** a cloud GPU, or any adapted learned model.

**What is measured on the recordings:** where the simple baselines fail, including the flat-versus-copy dial. New mechanisms are designed against those failures.

To change: the operator reopens Q12.

## D75. Condition contrasts in the fixed splits (recorded 2026-11-25T09:45:02Z, before any scoring)

**Finding** (critique-v3-immunology and -joint-action, recounted here from splits_v2.json): no validation or test person has both a familiar and a stranger session.
- Only the training split has within-person contrasts: 76 people.
- Person-disjoint hashing leaves the held-out splits with between-person contrasts only.

**Decision:**
- splits_v2 stays as fixed, for every screening metric.
- **The dial analysis:**
  - *On human ground truth:* within-person, on the 76 training people who have both conditions. Nothing is fitted there, so no held-out data is spent.
  - *On architectures:* between-interaction, familiar against stranger, on the validation split. It is labelled as between-person, and the permutation null shuffles condition labels across interactions.
- **Repeat actor pairs:** only a handful fall in validation and test. Repeat-pair analyses are reported for humans only, and are not used to screen architectures.

To change: re-split before any scoring, with people who have both conditions spread across all splits (this costs more dropped interactions).

## D76. Harness v2 after the independent review; splits re-fixed as v3; screening condition 4 re-based on humans (recorded 2026-11-25T10:24:20Z, before any scoring)

**What was fixed.** REVIEW-1 found 8 bugs and 4 spec deviations, all fixed. See research/harness/HARNESS.md, "Harness v2".

**The splits.** People are now keyed by numeric ID: the dataset warns that one person can carry several IDs. The result is splits_v3, pilot_v2 and e3_subset_v2. Nothing had been scored on v2.

**Screening condition 4.** The E3 pass share must now be at least the human pairs' share on the same subset. Under the old version, Delayed Mirror, which passes almost always, set the bar.

To change: restore splits_v2 (raw IDs), or the Delayed-Mirror bar for condition 4.

## D77. S0 process replaced by the read–design–critique cycle (operator notes Q15, Q16; recorded 2026-11-25T10:41:05Z)

**What stops:**
- The baseline-scoring track: the shared harness, screening, and measuring failures on Seamless.
- No downloads and no experiments in this cycle.

**What is kept as material:**
- The harness code (research/harness/), the splits and the dial-analysis code. None is run.

**What S0 is now:** read widely, design a new core mechanism and the whole system around it, have it critiqued independently, and repeat.

**Designs** are kept in research/foundations/designs.md.

**Documented failures of existing systems** go to research/foundations/known-failures.md, collected from sources read in full.

**The human dial question** (does a reaction to a familiar partner only scale, or change shape?) is answered from the facial-mimicry literature first.

**Also recorded:** the operator's answer to Q11 (lower the floor to 10%) was received at the same time. It is moot while no downloads are needed.

To change: the operator reinstates Q11/Q15's measuring track.

## D78. The "no flat-to-copy dial" criterion, refined (operator answer to Q18; recorded 2026-11-25T15:09:31Z)

**The rule now.** No single quantity may run the **whole face** from flat to copy.

**Each channel's strength must:**
- be set separately per expression, by context and by the learned relationship;
- be able to flip sign;
- stay under a built-in (innate, not learned) ceiling;
- never let copying become a state the agent settles into (copy must not be attracting).

**What each design must do:** name and bound every such per-channel quantity.

**Why.** The operator's original concern was one-dimensional designs, not the existence of per-channel strengths.

**How the critiques are re-read under it.** Earlier critiques found dials on single channels; those are now acceptable if they meet the four conditions. What remains disqualifying:
- a quantity that runs the whole face (or a large shared subspace) from flat to copy;
- a learned or uncapped ceiling;
- a copy set that attracts under the design's own learning.

To change: the operator reopens Q18.

## D79. Commits co-author the operator (operator request; recorded 2026-11-26T03:25:35Z)

Every commit made by the research cycle ends with these trailers:

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
    Co-Authored-By: ailuruth <65430552+ailuruth@users.noreply.github.com>

The operator's name and address are taken from his own earlier commit in this repository.

To change: the operator asks for a different name or address, or for the trailer to be dropped.

## D80. Q17 relaxed: argument, not proof; critiques hunt concrete failures; failure-free designs go to the operator (operator note Q19; recorded 2026-11-26T04:57:50Z)

- **Designs:** each keeps a precise object and a convincing argument for each key property. They are no longer held for proof gaps.
- **Critiques:** they look for concrete failure mechanisms (uncounted routes that carry copying, a slow state that tracks the partner, principle violations), not rigor.
- **Re-reading past verdicts:** a design held only for proof gaps is no longer held on that ground. Designs held for concrete failures stay held until those failures are fixed.
- **Candidates:** a design with no known concrete failure is put to the operator as a candidate to build, in research/questions.md.

To change: the operator reopens Q17 or Q19.
