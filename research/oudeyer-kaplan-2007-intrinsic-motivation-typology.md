# What is intrinsic motivation? A typology of computational approaches (Oudeyer & Kaplan)

Citation: P.-Y. Oudeyer, F. Kaplan. "What is intrinsic motivation? A typology of computational approaches." *Frontiers in Neurorobotics* 1:6 (2007). doi:10.3389/neuro.12.006.2007.

Source read: the frontiersin.org full-text HTML, text-extracted, read in full (psychology review, internal/external, intrinsic/extrinsic, homeostatic/heterostatic and fixed/adaptive distinctions, the whole typology, the non-intrinsic examples and the discussion). **The equations are images and did not extract;** each reward is quoted below from the surrounding text, not from the formula. The summary table (Fig. 7) was not seen.

Already in the index: Oudeyer, Kaplan & Hafner 2007 (IAC, the learning-progress mechanism itself). This note adds the typology around it.

## Key claims
- **Intrinsic ≠ internal.** Internal/external is where the reward is computed; intrinsic/extrinsic is about instrumentalisation, which the authors find too vague computationally ("the search for novel situations … is directed by the goal of getting internal rewards, and so is technically extrinsically motivated").
- **Homeostatic vs heterostatic.** Homeostatic motivations are satiable drives that keep a variable in a comfort zone; heterostatic ones "continuously push an organism away from its habitual state" and "cannot be satiated". Novelty reward is heterostatic; a novelty reward given only at an intermediate frequency becomes homeostatic. White (1959) is quoted against drive accounts of exploration: exploration "is not homeostatic".
- **Their proposed definition:** intrinsic motivations are reward functions defined on properties of the sensorimotor flow and its relation to the agent's own knowledge and know-how, **"independently of the meaning of the sensori channels"**. A reward tied to a named channel (energy level, number of faces seen) is internal but not intrinsic. Their own non-intrinsic example: a social-presence reward peaked at an optimal number of faces seen.
- **Typology (rewards described in text):**
  - *Knowledge-based, distributional:* uncertainty (reward ∝ improbability), information gain (decrease of model uncertainty after an event), distributional surprise, distributional familiarity.
  - *Knowledge-based, predictive:* novelty (prediction error), intermediate novelty (thresholded), **learning progress** (decrease of mean error within adaptively split regions; comparing raw windows across different situations "is in fact nonsense", e.g. leaf in the wind → white wall), Schmidhuber's before/after-update error difference, predictive surprise (error relative to a meta-predicted error), predictive familiarity.
  - *Competence-based (stated as never implemented before):* self-set goals g_k on an episode time scale t_g, achievement la(g_k, t_g); maximise incompetence, **competence progress ("flow")**, or competence.
  - *Morphological:* **synchronicity motivation** (reward for high short-term correlation, mutual information or small information distance between as many sensorimotor channels as possible), stability motivation (stay near the recent mean), variance motivation.
- **Promise:** "intrinsic heterostatic adaptive motivations" (information gain, learning progress, competence progress) combine exploration and organisation; the Playground experiment's LP robot moves from body babbling to object affordances, including vocalising "to a distant 'adult' robot".
- **Warning:** some members (familiarity, competence, stability) make a robot stand still; "in certain application contexts, their intrinsic openness is a weakness".

## What it means for the engine
1. **A map of objectives to check one by one for the approval route.** The relevant split is not intrinsic/extrinsic but which channels the reward reads:
   - **Synchronicity motivation is a copy drive by construction** when the agent's own face channels and the partner's face channels are in the same pool: maximal short-term correlation between channels is maximised by copying. It must never be used over mixed self/partner channels.
   - **Learning progress over a pool that includes the partner** rewards situations where the partner's responses are learnable. The Playground robot's turn to vocalising at the "adult" robot is the developmental form; in a human dyad it is engagement-seeking, i.e. the partner's attention as reward, by a path that never names attention.
   - **Competence progress** with self-set goals on the partner's face (goal = a partner state) is the approval route in its plainest form; with goals only on the agent's own body it is the efficacy line (stephan-2016).
2. **Satiation.** Only the homeostatic members fit Principle 6 directly. Learning progress is self-limiting (it vanishes once learned) but is maximised, not satiated; its region splitting is what makes it self-limiting.
3. **"Meaning of the channel" vs Principle 2.** The authors' definition of intrinsic (channel-agnostic) matches the engine's ban on named variables, but the engine needs the opposite of agnosticism in one respect: whether a channel is the agent's own or the partner's must be typed, or the agnostic reward will treat the partner's face as just another learnable channel.

## Verdict
- **background (typology; the hazard map for intrinsic objectives).** Adopt the homeostatic/heterostatic distinction and the "synchronicity over mixed channels = copy drive" observation for the audit list.
