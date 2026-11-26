# Interpersonal movement synchrony responds to high- and low-level conversational constraints (Paxton & Dale)

Alexandra Paxton & Rick Dale, *Frontiers in Psychology* 8:1135, 2017, doi:10.3389/fpsyg.2017.01135 (PMC5532444). Data and code: osf.io/4yqz8.

## What was read
The full PMC open-access text: introduction and hypotheses, methods (participants, Google Glass recording, conditions, preprocessing, CRQA, growth-curve analysis, the mixed model in full, phase-randomised baseline), results (Tables 1–2), discussion, limitations and footnotes. Figures (diagonal recurrence profiles) not seen; the appendix tables comparing to baseline (A1, A2) are described in the text but were not in the extracted file, so baseline results below are as the authors summarise them.

## Findings, precisely

**Design.** 21 dyads analysed (42 undergraduates; mostly strangers, 2 dyads acquainted). Seated ~0.97 m apart. Two 8-min conversations each, order counterbalanced: **affiliative** (find media you both like) and **argumentative** (topic chosen from their pre-surveys for most-opposed, strongest opinions; "try to convince one another"). Between dyads: a Google Glass screen flashed red at random (p = 0.1 per second); "noise" group told it was a bug, "dual-task" group told to count reds. Head acceleration (Glass accelerometer, 250 Hz → 10 Hz, Euclidean magnitude). Mean usable length 6.54 min (2.62–9.26).

**Analysis.** Cross-recurrence (embedding per false nearest neighbours; radius set for 5% recurrence) → diagonal recurrence profile over **±5 s** lags. Growth curves: linear lag term (leading/following) and quadratic lag term (inverted U = synchrony around lag 0; U = turn-taking, i.e. recurrence higher at lags than at 0). Baseline: 10 Fourier phase-randomised surrogates per conversation (keeps each person's power spectrum and autocorrelation); a shuffled baseline gave similar results.

**Results (standardised estimates).**
- **No overall time-locked synchrony** (H1 rejected). Head movement showed a turn-taking/lagged profile (LL × QL = −0.039, t = −7.09, p < .001).
- **Argument lowered recurrence** vs affiliative (Conversation = −0.601, SE 0.114, t = −5.29, p < .001), and changed its shape: affiliative recurrence higher but diffuse; argumentative lower with a distinct turn-taking U (Conversation × QL = 0.036, t = 9.07).
- **Against the surrogate:** affiliative recurrence was **not different from chance** overall (shape differed: surrogate flat); argumentative recurrence was **significantly below chance**, "in a turn-taking pattern" with some leader–follower asymmetry.
- **Low-level constraint mattered only inside argument** (Task × Conversation × QL = 0.067, t = 17.41): turn-taking U much stronger in the dual-task group; noise group nearly flat. In affiliative talk vs baseline, dual-task looked more like synchrony (inverted U) and noise more like turn-taking.
- Fixed effects explain 37% of variance; with dyad random effects 94% — dyads differ a lot (individual profiles shown in their Fig. 2).

**Caveats the authors give.** Head acceleration may be driven by each person's own speaking (results resemble their speech-signal results); different methods across head-synchrony studies give different answers (they list five method differences vs Boker 2002 and Ramseyer & Tschacher 2014); no no-screen baseline; small sample; first study of its kind.

## What it means for the designs
1. **Below-chance coupling is context-switched, not constant.** Same channel (head motion), same people, same session: at chance in a friendly conversation, below chance in an argument. A design must let the *sign* of the net partner coupling, measured against a matched surrogate, change with the episode — and in the opposed episode it must go **below** chance, which a design that only reduces a gain toward zero cannot do.
2. **Turn-taking is the dominant structure, not synchrony.** Recurrence peaks away from lag 0 (U-shape): the two heads tend to be in similar states *at different times*. For a face this is the alternation constraint: the agent's motion energy should be highest when the partner's is low and vice versa at second scales, more strongly when the episode is opposed.
3. **Interaction of slow and fast constraints is non-additive.** An irrelevant perceptual load changed coordination only within argument. So the effect of any fast perturbation on coupling must depend on the slow context state; a design where context multiplies a single coupling gain predicts proportional effects in both contexts and fails here.
4. **Large per-dyad variance (R² 0.37 → 0.94 with dyad effects)** means the partner-specific structure dominates; a design should expect to learn per-partner coupling profiles over minutes, not apply a population profile.
5. **Time scales:** lags within ±5 s; context held over 8 min.

## Verdict
**adopt (as a constraint), watch (as evidence)** — head-movement coupling at chance in friendly talk and below chance in argument against a phase-randomised surrogate, with turn-taking rather than synchrony as the shape; 21 dyads, an unusual sensor and a likely speech confound limit the weight.
