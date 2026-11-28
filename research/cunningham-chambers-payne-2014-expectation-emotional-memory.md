# Cunningham, Chambers & Payne 2014: expectation of future use and the emotional memory trade-off across sleep and wake

Cunningham, T. J., Chambers, A. M. & Payne, J. D. (2014). "Prospection and emotional memory: how expectation affects emotional memory formation following sleep and wake." *Frontiers in Psychology* 5:862. doi:10.3389/fpsyg.2014.00862. Open copy: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00862/full.

This is one of the two Cunningham et al. 2014 datasets in Lipinska et al. 2019 (Table 1, "2014a/b"). The other, Cunningham, Crowell, Alger et al. 2014 (*Neurobiology of Learning and Memory*, psychophysiological arousal at encoding), is on a host this session cannot reach and was not read.

**How fully read:** the publisher PDF, read in full on 2026-11-28 (abstract, Introduction, Methods, Results with Table 1, Discussion, Conclusion; figures by caption). Reference list not read.

## What it says
- **Design.** 80 students; 68 scenes, each a negative arousing or a neutral object on a neutral background (Payne 2008's paradigm), 6 s each, incidental encoding with valence and arousal ratings. After encoding, half were told a memory test would follow (expected), half were not. 12 h of sleep (polysomnography in the lab) or day wake; then objects and backgrounds tested separately (old/new, false-alarm corrected). "Trade-off" = object memory minus background memory.
- **Results.**
  - Valence × component F(1,76) = 70.9: the trade-off is much larger for negative scenes.
  - Expectation × component F(1,76) = 4.7, and the three-way valence × component × expectation F(1,76) = 4.3, p = .04: telling people a test is coming more than doubles the negative trade-off (t(78) = 2.6) and leaves neutral scenes unchanged.
  - Without expectation the negative trade-off is significant after sleep (t(17) = 2.8) and not after wake (t(20) = 1.2), replicating Payne 2008.
  - With expectation it is present after both (sleep t(20) = 6.0; wake t(19) = 4.7). In the wake group expectation tripled it (t(39) = 2.02, p = .05); in the sleep group expectation changed nothing (t(37) = 1.5, p = .14).
- **Their reading.** Emotional salience and expected future use are both "future relevance" cues. Sleep appears to tag the emotional centre as relevant automatically; awake, an explicit expectation produces about the same selectivity. The authors suggest rehearsal during wake may stand in for sleep's processing. They note possible circadian confounds and that positive scenes were not tested.

## What matters for this engine
- **What sets priority in this study is expected future use, and emotional salience behaves as one cue for it.** An explicit statement that the material will be needed produces the same selective keeping of the emotional centre that sleep produces. That fits a need-based reading of priority (Mattar & Daw's "need": how likely the memory is to be used again) better than a pure distress reading.
- **The trade-off is selection within an episode, not across episodes.** What is kept is the arousing object, and what is lost is the neutral context around it. The engine weights 2-Hz moments, which is already sub-episode (the existing sleep note's recommendation). But the engine's weight never *lowers* anything: every moment keeps weight ≥ 1. Forgetting of context happens only through retention deletion after 30 days.
- **Negative material only.** As in Lipinska 2019, the evidence is about aversive scenes; it says nothing about whether positive moments should be weighted the same way.

## Verdict: watch
One study, modest effects (p = .04–.05 on the key contrasts), a negative-only stimulus set and a circadian confound. Useful mainly as evidence that "relevance for the future" and "emotional salience" act through the same selection, which supports a need term in replay priority (new-core-search-16-synthesis.md §1).
