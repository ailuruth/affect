# Levitan & Hirschberg 2011; Levitan, Gravano, Willson, Beňuš, Hirschberg & Nenkova 2012: acoustic-prosodic entrainment

- Levitan, R. & Hirschberg, J. (2011). "Measuring acoustic-prosodic entrainment with respect to multiple levels and dimensions." Proc. Interspeech 2011, 3081-3084.
- Levitan, R., Gravano, A., Willson, L., Beňuš, Š., Hirschberg, J. & Nenkova, A. (2012). "Acoustic-prosodic entrainment and social behavior." Proc. NAACL-HLT 2012, 11-19.

Source read: both papers in full from the authors' PDFs (Columbia; ACL Anthology), including all tables, excluding reference lists. The 2012 tables came out of text extraction with columns separated; values were matched to rows by order and by the prose, so treat individual coefficients as approximate and the prose summaries as authoritative.

## Claims
Both papers use the Columbia Games Corpus: 12 sessions, 13 native American English speakers (6 F, 7 M), 11 of whom came twice with different partners; cooperative computer games, partners separated by a curtain (voice only); 9 h 8 min in all (2012 uses the 4 h 19 min of Objects games, 168 tasks). Features from Praat: intensity mean and max, pitch mean and max, jitter, shimmer, noise-to-harmonics ratio (NHR), syllables per second; all z-normalized (2011 by gender, 2012 by speaker). Inter-pausal unit (IPU): speech separated by at least 50 ms of silence.

### 2011: a vocabulary of entrainment
- Five measures at two levels. Session level: proximity (partners closer than non-partners, or than the speaker herself in another session) and convergence (closer in the second half than the first). Turn level, comparing the last IPU of a turn with the first IPU of the partner's next turn: proximity (adjacent closer than ten random non-adjacent partner IPUs), synchrony (Pearson r between adjacent IPUs across speakers; relative matching, possible without proximity) and convergence (correlation of the adjacent-IPU distance with time). Correlations had to fail in at least nine of ten random permutations to count.
- Session proximity vs non-partners: significant for intensity mean (t = -5.8, p = 6.1e-6) and max (p = .0002), pitch max (p = .0008), speaking rate (p = .008), shimmer (p = .05); not for pitch mean, jitter, NHR.
- Partner vs self: speakers are closer to themselves in another session than to their partner for pitch mean (t = 5.5, p = 1.7e-5), jitter, shimmer, NHR and rate: these are personal style. Only intensity mean and max are closer to the partner than to one's own other-session value (t = -3.4, p = .003; t = -2.1, p = .04): "one's interlocutor has a greater influence on intensity than one's individual behavior."
- Time course: intensity is close from the first half and gets closer ("early" entrainment). Shimmer and NHR converge and reach proximity only in the second half (p < .0001): "late-onset entrainment". Pitch mean and jitter converge across session halves but never reach proximity.
- Turn level: proximity in every feature (p ≈ 0); synchrony in every feature but small: intensity max r = .50, intensity mean .47, pitch mean .28, jitter .23, NHR .23, pitch max .18, shimmer .16, rate .15. Turn-level convergence valid only for pitch mean (r = -.06) and max (-.05). "Pitch entrainment is a matter of continuous local adjustments, rather than global similarity."
- The authors note the game domain is highly engaging, which may inflate entrainment.

### 2012: entrainment and social behaviour
- Entrainment per task: ENTp = -|speaker1_f - speaker2_f| (task means), compared with ENTx, similarity to same-gender, same-role speakers never paired with the speaker.
- Who entrains: male-male pairs only on intensity mean, intensity max and syllables per second; female-male pairs on all eight features (each p < .01); female-female pairs on jitter, intensity max and mean, rate, shimmer, not pitch or NHR (their pitch similarity is explained by the overall similarity between females). An asymmetric turn-level measure (ENT2p) found no difference between women and men in mixed pairs.
- Social variables (Mechanical Turk, 5 raters per task, yes/no): "giving encouragement" correlates with entrainment in all three gender groups (for mixed pairs strongly with intensity mean and max); "trying to be liked" with entrainment in male-male (intensity mean) and mixed pairs (pitch mean). "Trying to dominate" correlates with none. Jitter is the exception: entrainment on jitter goes with "conversation awkward" and against "giving encouragement".
- Objective success: entrainment correlates with shorter latency between turns (female-female on most features; male-male strongly on intensity mean, pitch mean and max, jitter), more turns and more overlaps; puzzlingly also with more interruptions on shimmer and NHR.
- Outliers: when one speaker is in the 10th or 90th percentile of a feature, the pair entrains more relative to baseline on intensity mean (t = 5.66, p = 1.7e-7) and max (t = 8.29, p = 5.5e-14), shimmer and rate (p = .02), not on pitch, jitter or NHR. A salient deviation draws more accommodation.

## Evidence with numbers
See above. Sample sizes are small: 13 speakers, 12 sessions; the 2012 correlations are over 168 tasks, split three ways by gender pair, with many tests and no correction reported.

## What it implies for an engine whose voice is driven from an internal state through an innate vocal body, with structured coupling
- Coupling is per feature and per time scale, not one gain. These data give the engine a concrete starting map:
  - Loudness (intensity): fast, global and local; the partner pulls a speaker off her own baseline. Couple the engine's vocal effort to the operator's from the start, at both turn and session scale.
  - Pitch level: personal; speakers keep their own mean across partners, never reach global proximity, but adjust locally at each turn exchange (small synchrony r ≈ .28). Couple pitch only locally, relative to each side's own baseline, never by copying the operator's absolute F0.
  - Voice quality (shimmer, NHR): personal style that converges slowly, late in a session. A slow coupling term, minutes not seconds.
  - Jitter: entrainment on it goes with awkwardness. A feature not to couple, or a candidate for divergence.
  - Rate: personal but adjusts toward the partner; and outliers in rate draw accommodation.
- Synchrony (relative co-movement) and proximity (absolute closeness) are different and can dissociate. The engine's coupling should be stated in deviations from its own baseline (synchrony), which keeps its innate vocal identity (Principle 8) while still coordinating.
- Outlier-driven accommodation fits salience: a partner who is unusually loud or fast gets more adjustment. In the engine, coupling strength per feature could scale with how surprising the operator's value is relative to the operator's own baseline, which a predictive perception model gives for free.
- "Trying to dominate" did not track entrainment and "trying to be liked" did: entrainment is read socially. Principle 6 forbids rewarding the operator's approval, so the engine's vocal convergence must not be a learned instrument for being liked; it should follow from coupled state, and its absence (divergence) must remain available.
- Evaluation: the five measures and the ten-permutation check are ready-made instruments for engine-operator sessions (with the surrogate caution in moulder-2018-synchrony-surrogates.md). A prediction to write: lesion the engine's slow coupling term and voice-quality convergence in the second half of a session should vanish while turn-level intensity synchrony remains.

## License
Interspeech 2011 paper: ISCA copyright, author copy. NAACL 2012: ACL Anthology, CC BY 4.0 for newer volumes; 2012 volume under ACL's terms. Columbia Games Corpus: LDC-distributed, not downloaded.

## Verdict: adopt (the measurement vocabulary and the per-feature coupling map)
Single small task-oriented corpus, voice only, American English; replicate the per-feature pattern before building coupling constants on it.
