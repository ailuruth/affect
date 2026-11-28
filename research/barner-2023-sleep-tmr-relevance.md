# Barner, Werner, Schörk, Born & Diekelmann 2023: sleep, targeted memory reactivation, and relevant versus irrelevant memories

Barner, C., Werner, A.-S., Schörk, S., Born, J. & Diekelmann, S. (2023). "The effects of sleep and targeted memory reactivation on the consolidation of relevant and irrelevant information." *Frontiers in Sleep* 2:1187170. doi:10.3389/frsle.2023.1187170. Open copy: https://www.frontiersin.org/articles/10.3389/frsle.2023.1187170/full (CC BY).

Read as the targeted-memory-reactivation (TMR) source for this pass, from the Born group (active systems consolidation). Oudiette & Paller 2013 (*Trends in Cognitive Sciences*), Oudiette, Antony, Creery & Paller 2013 (*J Neurosci*), Feld & Born 2017 (*Curr Opin Neurobiol*) and Joensen et al. 2022 (*Learning & Memory*, TMR-induced forgetting of overlapping memories) were not reachable (paywall, or hosts outside this session's network); Oudiette et al. 2013 and Feld et al. 2016 appear below only as Barner et al. report them.

**How fully read:** the publisher PDF, read in full on 2026-11-28 except the Experiment 2 results paragraph, which was read in part (its outcome is restated in the Abstract and Discussion, which were read in full). Table 1 read; Table 3 and the supplementary statistics not read. Reference list not read.

## What it says
- **Background as the authors state it.**
  - Active systems consolidation: during slow-wave sleep, new hippocampal traces are covertly reactivated with neocortical ones, and this is "selective", favouring memories "of future relevance". Reactivation capacity "might be limited" (Feld et al. 2016; Antony et al. 2018), so memories may compete for it.
  - Relevance cues that help sleep consolidation: an expected test, an expected reward, emotional tone, an intention for the future. They cite Bennion et al. 2016 for top-down cues (reward, test announcements) being stronger than bottom-up ones (salience, emotional valence).
  - **Oudiette et al. 2013 (as reported):** high-reward picture-locations were remembered better than low-reward ones, but cueing some *low-reward* items with their sounds during sleep rescued them to the high-reward level.
- **Experiment 1 (sleep vs wake, n = 28 + 28).** Two sets of 15 object-location pairs, learned to 60 %. *After* learning, one set was declared relevant (to be tested, €2 per correct answer), the other irrelevant. Retention at ~12 h and ~1 week.
  - Sleep > wake overall: F(1,54) = 6.71, p = .012, ηp² = .11 (at 12 h and at 1 week).
  - Relevant > irrelevant overall: F(1,54) = 8.78, p = .005.
  - Sleep × relevance: not significant (p = .12; at 1 week p = .096). Post hoc, only the sleep group kept the relevant set better than the irrelevant one (retention 58.7 vs 44.5 % at 12 h).
  - Longer slow-wave sleep went with less successful interference learning for the relevant set (r = −.38): the relevant memory was more stable.
- **Experiment 2 (odour TMR in the first SWS period, n = 23 cueing, 20 placebo).** Both sets learned with an odour; odour or vehicle re-presented in the first SWS; woken after it (~40 min of sleep).
  - Relevant > irrelevant again, after 40 min of sleep and at 1 week.
  - TMR helped neither set significantly; descriptively it helped the *irrelevant* set a little, as in Oudiette 2013.
- **Their reading.** The sleep benefit for relevant memories is real but smaller than earlier studies suggested and grows over a week. A strong top-down relevance signal may already have given relevant memories all the reactivation they can get, so external cueing can only help the memories that were not prioritised. The relevance instruction may also have changed memory strength before sleep.

## What matters for this engine
- **Priority from expected use.** What is selected for offline consolidation here is set by expected future use (a test and a reward announced after encoding), not by the material's emotional charge. The engine's κ_replay weights by the partner-need load of the moment. Expected future use, in the engine's own terms, would be how likely the moment's context (this person, this topic) is to come back. See new-core-search-16-synthesis.md §1.
- **Limited capacity, and cueing what was not chosen.** If reactivation is limited and priority-driven, deliberately cueing what priority left out evens things up (Oudiette, and the descriptive trend here). For the engine: a priority weight needs a floor (every stored moment keeps weight ≥ 1; S48 has this), and possibly a coverage term, so that low-priority moments are not starved. That matches Isele & Cosgun's coverage result in hayes-2021-replay-missing-biology.md.
- **Forgetting.** This study shows no active forgetting of the irrelevant set beyond what wake also produces. The engine has no active forgetting except retention deletion and the pull to θ₀.
- **Timing.** About 40 min of sleep, the first SWS period, already gives the relevance advantage. That is weak evidence that one early block captures most of the selective benefit (relevant to M8; synthesis §5).

## Verdict: watch
Small samples, a key interaction short of significance, and a null TMR effect. It supports *relevance or expected-use priority with a floor* as the biological account of selective offline consolidation, more than *salience priority*. It does not support any specific gain.
