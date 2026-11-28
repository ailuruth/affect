# Borrie, Lubold & Pon-Barry 2015: disordered speech disrupts conversational entrainment

Borrie, S. A., Lubold, N. & Pon-Barry, H. (2015). "Disordered speech disrupts conversational entrainment: a study of acoustic-prosodic entrainment and communicative success in populations with communication challenges." *Frontiers in Psychology* 6:1187. doi:10.3389/fpsyg.2015.01187. Open: https://pmc.ncbi.nlm.nih.gov/articles/PMC4532918/ (CC BY).

**How fully read:** the full text from PMC, from the abstract through the conclusion, with Tables 1–4. Figure 1 was read by its caption only. The reference list was not read.

## What it says
- **Participants.** 60 face-to-face dyads in three groups of 20:
  - Control: two healthy native speakers of American English;
  - Accented: a native speaker with a strongly Chinese-accented speaker;
  - Disordered: a native speaker with a speaker with mild dysarthria (80–95 % words correct on the SIT).

  Dyads were matched for gender and age.
- **Task.** Diapix spot-the-difference, unscripted, 12 minutes of dialogue per dyad, on lavalier microphones.
- **Features.** Per turn (openSMILE): mean intensity, mean pitch (male pitch rescaled to the female range), jitter and shimmer.
- **Entrainment measures** (after Lubold & Pon-Barry 2014), both local, turn by turn:
  - *synchrony:* Pearson r between adjacent turns of the two speakers, rescaled to [0, 1], so 0.5 means r = 0;
  - *proximity:* |t| of a paired test of the adjacent-turn difference against the mean difference to 10 non-adjacent turns.
- **Communicative success:** differences found in 12 min.
- **Results by group** (synchrony; my conversion to r = 2s − 1 in brackets):
  - Control: intensity 0.59 [r ≈ .18], pitch 0.57 [.14], jitter 0.54, shimmer 0.52.
  - Disordered: intensity 0.53 [.06], pitch 0.53 [.06].
  - Accented: between the two.
  - Group effects (one-way ANOVA): intensity synchrony η² = .14, pitch .13, jitter .11. Pitch proximity η² = .12, with the Control group's mean |t| 1.58 against the Disordered group's 0.76. Shimmer showed no group effect.
  - The Disordered group was lower than Control (Hedges g > 0.8). The Accented group differed from neither.
- **Success** (17.9, 13.3 and 9.1 differences found for Control, Accented and Disordered) correlated across dyads with:
  - synchrony of pitch (r = .57), intensity (.43) and jitter (.36);
  - pitch proximity (Table 4 prints r = −.54. Its sign is opposite to the text, which calls the relation positive, and the table's intensity proximity entry "−0.95, p = .476" is evidently a typo).
- **Within groups,** only pitch synchrony predicted success: r = .53 (Disordered), .81 (Accented), .85 (Control), each n = 20.
- **Background claim (Borrie & Liss 2014, cited, not read here):** healthy listeners shifted their speech rate and pitch variation toward recorded dysarthric speech in a quasi-conversational task.

## What matters for this engine
- **Local pitch and loudness coupling is real but small.** In healthy dyads the turn-to-turn correlation is r ≈ .14–.18. That is lower than Levitan & Hirschberg's .28–.50 on the Columbia Games corpus, with a different extraction and normalisation. Neither study used surrogates beyond non-adjacent turns. The size of the local effect therefore depends on corpus and method. A local voice coupling in the engine should be sized near the low end.
- **It co-varies with how well the conversation goes.** Pitch synchrony tracks task success within every group (r = .53–.85 on 20 dyads each). The study is correlational: easier conversations may produce both. There is no evidence here that entraining causes success, and none about held levels over minutes.
- **The partner's own speech can make entrainment fail.** Variable, pathological prosody lowers it. If the engine's voice is unnatural (WORLD artefacts, flat templates), the operator may entrain less to it. That bears on measuring the vocal analogue of S5, not on the engine's own coupling.
- **No held levels, no time course, no social variable** other than group. This source answers only the "local" row of the synthesis.

## Verdict: adopt (local-coupling sizes; success correlate)
Sixty dyads, 12 minutes each, one task. Many tests without correction. A table sign is inconsistent with the text. The pitch normalisation for male speakers is a simple rescaling.
