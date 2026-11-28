# Lipinska et al. 2022: does sleep depotentiate emotional reactivity? (systematic review and meta-analysis)

Lipinska, G., Austin, H., Moonsamy, J. R., Henry, M., Lewis, R., Baldwin, D. S., Thomas, K. G. F. & Stuart, B. (2022). "Preferential consolidation of emotional reactivity during sleep: A systematic review and meta-analysis." *Frontiers in Behavioral Neuroscience* 16:976047. doi:10.3389/fnbeh.2022.976047. Open copy: https://www.frontiersin.org/articles/10.3389/fnbeh.2022.976047/full (CC BY). PROSPERO-registered.

Read in place of Davidson & Pace-Schott 2021 (*Current Sleep Medicine Reports* 7:31–46, "Go to bed and you MIGHT feel better in the morning"), which the brief named. That paper was not reachable: its PMC copy served a bot check, and link.springer.com is outside this session's network. It is not cited for any claim.

**How fully read:** the publisher PDF (33 pages), read in full on 2026-11-28: abstract, Introduction, Methods, risk of bias, the narrative synthesis, all meta-analyses I–X with their captions, subgroup analyses, Discussion, Limitations and Conclusion. The supplementary figures (subgroup forest plots) were not read. Reference list not read. Primary studies not read.

## What it says
- **Question.** Sleep-to-forget (Walker & van der Helm 2009) predicts that reactivity to the *same* emotional stimuli falls more over sleep than over wake. Do the data show this?
- **Data.** 24 studies (2006–2021): 14 in the meta-analysis, 10 narrative only. Reactivity measured before and after sleep or wake: heart-rate deceleration (HRD), skin conductance, pre-ejection period and LPP (physiological); valence and arousal ratings (self-report). Change scores, random effects.
- **Physiology: no effect.**
  - Negative stimuli, sleep vs wake change: SMD 0.02 [−0.44, 0.49], p = .93 (k = 5). HRD-only subset −0.30 [−0.66, 0.06], p = .10.
  - Neutral stimuli: 0.19 [−0.22, 0.60], p = .36.
- **Valence ratings: no effect** (negative −0.07, p = .76; neutral 0.44, p = .07; positive 0.11, p = .73; all I² ≥ 77 %).
- **Arousal ratings to negative stimuli: higher after sleep than after wake.** The negative-only comparison was −0.30 [−0.53, −0.07], p = .01, and the 2 × 2 (condition × valence) comparison 0.65 [0.30, 1.00], p < .001 (K = 6). The authors read both as *more* self-reported arousal to negative material after sleep, not less, and offer a "next-day readiness" account. (The sign convention of the first figure is not stated in the text; I follow the authors' reading.)
- **Moderators (self-report only):** a nap made negative pictures rated less negative, a full night slightly more; sleep deprivation made positive pictures rated more negatively; little REM went with less reactivity to neutral material.
- **Narrative synthesis.** Most studies show reactivity *maintained* after sleep, or no effect of sleep or wake. Only a few show attenuation, and some of those were not sleep-specific.
- **Their conclusion.** Sleep "does not have a statistically significant effect on psychophysiological measures of emotional reactivity"; if anything self-reported arousal to negative material rises.

## What matters for this engine
- **The "affect pass" (memory-replay-synthesis.md §1.8, L8) loses most of its support.** The existing note kept SFSR depotentiation as "watch", resting on Sterpenich 2007 versus Wagner 2002. Pooled, there is no physiological depotentiation and a small rise in rated arousal. A replay pass that clamps the arousal gain to extinguish cue-to-response mappings has no human basis to borrow from.
- **This matters for κ_replay.** One defence of distress-weighted replay is that it is self-limiting: replay of a hard moment depotentiates it, so its tag falls (the existing note's tag ← tag · r_replay/r_encode). If sleep does not depotentiate, a distress weight that is recomputed from the stored moment's distress level, not from what replay has already achieved, never falls. The engine's S48 weight is of that kind: it reads the stored 𝒟_p of the moment, which replay does not change. So the cost of κ_replay (hard moments kept heavy for as long as they are stored) is not offset by any built-in forgetting of their charge.
- **Nap versus night.** The nap/night difference in valence direction is a self-report subgroup effect confounded with the control condition (all nap studies had daytime controls). It gives no basis for an M8 choice of block length.

## Verdict: adopt (as evidence against an affect-depotentiation pass and against assuming distress tags self-extinguish)
Watch for better-powered physiological studies with REM measures, which the authors call for.
