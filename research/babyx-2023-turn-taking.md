# Deconstructing and reconstructing turn-taking in caregiver–infant interactions (BabyX)

Sagar, Henderson, Takac, Morrison, Knott, Moser, Yeh, Pages and Jawed, "Deconstructing and reconstructing turn-taking in caregiver-infant interactions: a platform for embodied models of early cooperation", *Journal of the Royal Society of New Zealand* 53(1):148–168, 2023 (online 2022), doi:10.1080/03036758.2022.2098781; PMC11459835.

## Source read
The full text, including all tables, figure captions and the reference list. I read it from the Internet Archive's snapshot (2025-03-06) of the PMC article page, because both live PMC and tandfonline returned bot-check pages. Figures were not visible; their captions were.

## Claims
- Building infant cooperation first is a route to models of adult cooperation. BabyX is now an 18-month-old with a body, a virtual touchscreen and a camera view of the user.
- BabyX's turn-taking is "largely a side-effect of distinct brain circuits implementing event-perception and event-execution processes, and of mechanisms requiring the infant to choose between these modes". The authors call this mode choice "an innate protocol for turn-taking".
- Two predictions from the model were tested on human infants:
  - infants will not start an action while the caregiver is acting;
  - infants will cede the floor when the caregiver interrupts them.
- "Our results offer broad support for the model."

## Architecture (as given; equations are in Takac et al. 2020 and Knott & Takac 2021, not here)
- **Events (after Zacks).** Experience is segmented into events. Each event is experienced as a deictic routine: attend to an object, classify it, track it or reach for it. The routine is held in a working-memory (WM) event medium. At event boundaries it is written to long-term episodic memory (LTeM), stored in synaptic weights.
- **Cognitive modes.** At each boundary, evidence accumulators choose between two modes:
  - Execution mode: a desired event drives sensorimotor processing. Evidence comes from "a simple planning system".
  - Perception mode: salience drives processing, with top-down expectations. Evidence comes from visual change, such as an object appearing or starting to move.
  Both modes record the routine in the WM event medium.
- **LTeM as SOMs.**
  - A recurrent sequencing SOM predicts the next event.
  - A planning SOM detects subsequences that recur or end in reward, together with the state update they produce. It supports plan execution (query it with the desired state update) and plan inference about the user (query it with ongoing events to guess the user's goal).
- **Joint action by erasure.** "The 'agent' field of event representations is ignored, so an event performed by herself is indistinguishable from one performed by someone else." BabyX can therefore complete the user's plan, but only because she has no self/other distinction in the plan.
- **Interruption.** A dedicated accumulator watches for large visual change or loud sound throughout an event. At threshold it abandons the event and clears WM (after Corbetta's reorienting system).
- **Language.** A separate phonological WM (after Baddeley). Words are learned cross-situationally (Siskind) at event boundaries, by pairing a WM event with the utterance heard. User utterances are treated as imperatives. BabyX can describe ongoing events.
- **Innate vs learned.** The mode competition, the interruption accumulator and the turn-taking protocol are wired. Event sequences, plans and word meanings are learned. Emotion is not part of this paper's model; the authors point to Knott et al. 2021 for it.

## Evidence with numbers
- **The human study only.** 45 caregiver–infant dyads; infant age mean 21.14 months (SD 1.99); 46.7% female; a highly educated, mostly NZ-European sample. A touchscreen "Blocks" game in two 45 s segments (free play, then "Build a tower together"), played through screens with a curtain between the pair. Touch logs were scored automatically; an interrupter's continued action counted as new 400 ms after the interrupted agent stopped.
- 1303 actions in total (caregiver 595, infant 708) and 220 interruptions (caregiver 111, infant 109).
- Share of total task time spent acting: caregiver 0.259, infant 0.232, overlapping 0.054. Overlap is 8.7% of acting time.
- Infants interrupted a mean of 0.24 (median 0.21) of caregiver actions. Only 9 of 45 infants (20%) never interrupted.
- Floor ceding was 0.71 after an interrupted infant action vs 0.31 after an uninterrupted one. Reported as "W = 168"; no p-value or effect size is given in the text.
- Latency to cede after an interruption: mean 0.88 s, median 0.56 s. Age trends were read from scatterplots, with no test reported.
- **BabyX's own behavior is not measured.** No BabyX–user sessions, rates or comparison with the human numbers are reported. The abstract says the paper "introduce[s] a novel empirical paradigm for testing BabyX's model"; the test itself is future work.

## Failure modes, reported or evident
- **No test of the model.** The predictions were checked against humans, not BabyX's output against humans. Nothing shows that BabyX produces the human rates.
- **Weak support for the first prediction even in humans.** Infants interrupted about a quarter of caregiver actions. A rough independence baseline (my computation from the reported means, not the authors'): if infant and caregiver acted independently, overlap would be about 0.259 × 0.232 ≈ 0.060 of task time. The observed overlap is 0.054. Avoidance of overlap is therefore barely above chance at the group level. The authors report no chance or surrogate baseline. The ceding result (0.71 vs 0.31) is the stronger finding.
- **Assembled.** Modes, accumulators, SOMs, interruption circuit and phonological WM each come from a different theory (Zacks, Ballard, Corbetta, Baddeley, Siskind).
- **Turn-taking is wired.** The authors say so: an "innate protocol", not something learned from the partner.
- **No self–other distinction in plans.** The authors list this as a limitation they are extending.
- **Persistence.** LTeM is in weights, but persistence across sessions or days is not discussed.
- **Ablations.** None. The obvious one (disable the mode competition and check whether overlap rises) is not run.

## License
© 2022 The Royal Society of New Zealand; PMC deposit (green OA). No code.

## Runs on this Mac without a GPU?
n.a. No public code. The described mechanisms (accumulators, SOMs) would be light.

## Verdict: watch (read). Use the human dataset description and the ceding measure. Do not count the paper as an evaluation of BabyX.

## What it implies for this engine
- **On the brief's BabyX gap:**
  - "No controlled evaluation" still holds for BabyX as an agent. The only controlled data are human–human, and the model's output is not compared with them.
  - "No conceptual layer" needs qualifying by 2023. BabyX has event representations, episodic memory, plan inference and word learning: a small symbolic layer, though not a language model.
  - "Ablations planned and never run": no ablation here either.
- **Turn-taking measure.** Use floor ceding after interruption, and its latency (about 0.5–0.9 s in 21-month-olds), as candidate measures of whether a partner treats the engine's actions as turns. Score them against a surrogate baseline. The authors' own overlap statistic shows why a baseline is needed.
- **"Agent field ignored" is the cheap route to joint action, and the wrong one for this engine.** Principle 3 needs the self–other map to keep "whose" while sharing "what". Compare gold-scassellati-2009-robot-self-recognition.md (other = self model with the cause hidden) and lowe-2022-2023-complex-autoencoder-rotating-features.md (orientation carries "whose").
- **A wired turn-taking protocol fails Principle 10.** If the engine needs turn-taking, it should fall out of the core: for example, perceiving and acting competing for the same precision or attention budget. The ablation would then be derived, not asserted.
