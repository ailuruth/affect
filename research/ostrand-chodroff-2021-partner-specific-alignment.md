# Ostrand & Chodroff 2021: speakers align on some features but not others within a dialogue

Ostrand, R. & Chodroff, E. (2021). "It's alignment all the way down, but not all the way up: Speakers align on some features but not others within a dialogue." *Journal of Phonetics* 88:101074. doi:10.1016/j.wocn.2021.101074. Open copy: https://pmc.ncbi.nlm.nih.gov/articles/PMC8345023/ (author manuscript). Data and scripts: osf.io/3hu5r, osf.io/4y6wn (not opened).

**How fully read:** the full text from PMC, from the abstract through the conclusion and footnotes, including Table 1 (the 323 features) and the difference-score formulas. Table 2 (the experimenters' raw temporal values) and Table 3 (the cross-level correlation matrix) were lost in the HTML extraction. Their content is taken from the prose. Figures were read by their captions only. The reference list was not read.

## What it says
- **Question.** Is alignment one phenomenon, so that alignment on one feature or level implies alignment on the others? And is it partner-specific: does a speaker take on the profile of the listener in front of her, or only drift toward recent input in general?
- **Design.** 96 UCSD students played a picture-matching game with two experimenters who differed sharply:
  - Experimenter A was a female native speaker of Mandarin with a strong accent; Experimenter B was a male native speaker of American English.
  - For each participant, one experimenter used only double-object datives and the other only prepositional datives, counterbalanced.
  - **Exposure phase:** four rounds in which each experimenter in turn described six pictures. **Test phase:** four rounds of about 70 s each, in which the participant described 12 pictures, alternating between the two experimenters.
  - So any alignment at test must come from a per-partner profile learned during exposure. It cannot come from recency priming: all exposure came before all test trials.
- **Measure.** Global proximity. For each feature, the squared distance to the current listener is compared with the squared distance to the other experimenter, summed over the four test rounds. Speaking identically to both experimenters gives no alignment, whatever one's own baseline.
- **Results.**
  - **Holistic (323 features, elastic-net logistic regression, leave-one-subject-out):** 55.0 % correct against a chance of 50 % (p = .003). The authors note this is about the size of AXB similarity judgments, around 56 % (Pardo et al. 2018).
  - **Speech rate aligned to the current partner:** distance to listener 0.94 vs non-listener 1.07 syllables/s (t(95) = 4.50, p < .0001).
  - **Longest pause (95th percentile of the inter-utterance pause) aligned:** 3.60 vs 4.06 s (t(95) = 4.18, p < .0001).
  - **Not aligned:**
    - F1 of any corner vowel (all p > .07, the one trend in the direction of anti-alignment);
    - vowel-triangle area (p = .93);
    - dative structure (43.2 vs 43.9 % prepositional datives, p = .94).
  - **No consistency across levels within a speaker:** of 17 cross-level correlations, the largest was R² = 0.027 (p = .11), most below 0.01.
  - The non-native experimenter spoke faster and paused less than the native one. Participants matched her by speeding up, so the effect is alignment and not "foreigner talk".
- **Their reading.** Alignment is "a constellation of loosely-related effects" and not an automatic priming cascade (against Pickering & Garrod 2004). Features that bring communicative or social benefit (tempo, pauses) are learned per partner. Features that do not (F1) may move only transiently, by priming. They cite Weise & Levitan 2018 and Cohen Priva & Sanker 2018, which also found no correlation of alignment across features. Neither paper was read here.
- **Not measured individually:** F0 and intensity entered only the holistic set.

## What matters for this engine
- **Held, partner-specific levels exist in humans for tempo and pausing.** People keep a different speaking rate and pause length for each of two partners over minutes, after a few minutes of exposure, and switch back and forth between them. That is "proximity" to a partner's habitual value, learned per person. It is the kind of convergence that the build core's held cone cannot produce, because the cone multiplies only his deviation from his own baseline b_id (spec §1.5.1, rule 6). See new-core-search-15-synthesis.md §3.
- **The effect is small and patchy.** The rate gap closes by about 0.13 syllables/s. The holistic classifier is only 5 points over chance. Alignment on one feature predicts nothing about alignment on another (R² ≤ 0.027). So a single "accommodation" gain across the voice channels would be wrong for humans too. Per-channel coupling, which Q18 already requires, fits the data.
- **Proximity, not trend.** The measure is closeness of levels to each partner, not co-movement over time. It is the measure the engine should use to test whether its held voice levels differ by partner. Its prediction is that they do not, except through each partner's own deviations (the marker in the synthesis, §6).
- **A ready-made test.** The two-partner alternating design with Listener vs Non-listener squared distances is robust to each speaker's own baseline. It is also the cleanest instrument for the vocal analogue of S5: does the operator's rate and pause length move toward the agent's, in a design where his own baseline is controlled?

## Verdict: adopt (evidence map and instrument)
One task (picture description), students, two strongly contrasting confederates. Partner differences were large and partly categorical (sex, accent), which may exaggerate what happens with an ordinary partner. Pitch and loudness were not tested one by one.
