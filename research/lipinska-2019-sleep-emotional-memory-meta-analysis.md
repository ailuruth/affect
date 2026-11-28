# Lipinska, Stuart, Thomas, Baldwin & Bolinger 2019: does sleep preferentially consolidate emotional memory? (meta-analysis)

Lipinska, G., Stuart, B., Thomas, K. G. F., Baldwin, D. S. & Bolinger, E. (2019). "Preferential Consolidation of Emotional Memory During Sleep: A Meta-Analysis." *Frontiers in Psychology* 10:1014. doi:10.3389/fpsyg.2019.01014. Open copy: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01014/full (CC BY).

**How fully read:** the publisher PDF (38 pages), read in full on 2026-11-28 from the abstract through Methods, Results, Discussion, Summary and Limitations, including Table 1 (the 36 datasets), Table 2 (sensitivity analyses, partly garbled in text extraction) and every forest-plot caption. The forest plots themselves were read by caption only. The reference list was not read, and none of the 31 primary studies was read for this note (their results below are as the meta-analysis pools them).

## What it says
- **Question.** After sleep, is the advantage of emotional over neutral material larger than after an equal time awake? This is the "preferential consolidation" claim of Payne 2008, Wagner 2001 and Hu 2006.
- **Data.** 31 articles, 36 datasets, N = 2,832 healthy people. Pictures in most; texts, faces and cartoons in a few. Sleep was a full night or a nap; the control was daytime waking or a night of sleep deprivation. Random-effects meta-analysis of standardised mean differences (emotional minus neutral), run separately after sleep and after wake.
- **Main result: no overall sleep-specific advantage.**
  - Negative vs neutral: d = 0.52 after sleep (k = 20, n = 785, I² = 62 %) and d = 0.58 after wake (k = 20, n = 739, I² = 23 %). Negative material is remembered better whether one sleeps or not.
  - Positive vs neutral: d = 0.22 after sleep, 0.12 after wake; both confidence intervals include 0.
  - Combined negative and positive vs neutral: d = 1.35 after sleep, 1.33 after wake.
- **Moderators where an effect appears.**
  - **Baseline-controlled retention** (delayed score minus pre-delay score; 9 datasets): negative vs neutral d = 0.64 [0.22, 1.07] after sleep against 0.18 [−0.06, 0.43] after wake. Positive vs neutral 0.21 vs 0.11, both with intervals spanning 0. This is the clearest sleep-specific signal, and it is for negative material only.
  - **Free recall vs recognition** (combined emotional): after sleep d = 1.79 with free recall against 0.85 with recognition (p = .003); no such difference after wake.
  - **Sleep deprivation as control** makes the emotional advantage after the waking control larger (negative: d = 0.80 vs 0.56 with daytime waking, p = .03). Deprivation itself raises emotional reactivity, so it is a poor control.
  - All-male samples show larger post-sleep effects (d = 1.08 vs 0.50); nap vs full night and intentional vs incidental encoding gave no reliable difference.
- **What it does not test.** The "trade-off" (emotional centre kept, neutral background lost) is not analysed; the authors name it as a qualitative change their method cannot see.
- **Their conclusion.** The literature "does not conclusively demonstrate that sleep preferentially consolidates emotional over neutral memories"; preferential consolidation appears "only under particular methodological conditions" (free recall, baseline-controlled retention).

## What matters for this engine
- **The distress weight's strongest human support is weaker than the repo assumed.** sleep-emotional-memory-walker-payne-kensinger.md and memory-replay-synthesis.md §1.6 took Payne 2008 as the primary evidence for tag-weighted offline replay. Pooled over 36 datasets, emotional (mostly negative) material is favoured about equally by sleep and by waking. Emotional encoding is stronger; sleep adds a preference only in some designs. So "offline replay should weight aversive moments more" is not established as what sleep does.
- **Where a sleep effect exists it is for negative, not positive material.** A replay weight that tracks distress would reproduce exactly the asymmetry humans show in the retention studies. Whether that is a feature or a bias is a design choice, not something the evidence forces. Nothing here shows that people need it to function well.
- **Initial learning matters.** The effect appears only once encoding strength is controlled. That points to the gain side of priority (how much is still to learn), which Schapiro-type results also point to, not to the salience side alone.
- **No support for a large gain.** Effects of d ≈ 0.5 against d ≈ 0.2 in retention do not translate into a factor; nothing here supports a 4× weight specifically. κ_replay = 4 is a declared constraint, not a fitted value.

## Verdict: adopt (as evidence); the claim "sleep preferentially consolidates aversive moments" is demoted to watch
Adopt as the current best quantitative summary. It weakens, but does not refute, the biological motivation for κ_replay: arousal at encoding helps memory in general (both sleep and wake), and the sleep-specific boost is small, design-dependent and negative-only. See new-core-search-16-synthesis.md §1.
