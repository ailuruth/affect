# Borrie, Barrett, Willi & Berisha 2019: sustained entrainment measured against sham conversations

Borrie, S. A., Barrett, T. S., Willi, M. M. & Berisha, V. (2019). "Syncing up for a good conversation: a clinically meaningful methodology for capturing conversational entrainment in the speech domain." *Journal of Speech, Language, and Hearing Research* 62(2):283–296. doi:10.1044/2018_JSLHR-S-18-0210. Open: https://pmc.ncbi.nlm.nih.gov/articles/PMC6436892/.

**How fully read:** the full text from PMC, from the abstract through the conclusion, including the methods for each feature set, the CRQA parameter selection, the sham construction and the discussion. Tables 2–4 were lost in the HTML extraction (cell values missing), so the numeric real-vs-sham and R² results are known only from the prose. Figure 1 was read by its caption. The appendix rating scale was skimmed. The reference list was not read.

## What it says
- 57 Diapix conversations between healthy, unacquainted students (99 women, 15 men).
- **Five reduced feature streams per speaker,** each reduced by ICA:
  - rhythmic: envelope modulation spectrum, rhythm metrics;
  - articulatory: long-term average spectrum, MFCCs;
  - phonatory: a "voice report" of F0, jitter, shimmer and HNR.
- **Entrainment measure:** cross-recurrence quantification (CRQA) over the whole conversation, at all lags. Its radius and delay were chosen as the values that best predicted five speech-language pathologists' ratings of how "in sync" each conversation was (α = .92).
- **Real vs sham:** the 57 real conversations were tested against 500 sham conversations, which paired people who never spoke together. With a Bonferroni α of .0017:
  - sustained recurrence (alignment held beyond a single instant) and maximum aligned length differed between real and sham conversations, pooled over the five streams;
  - single-instant recurrence rate, mean length and entropy did not;
  - sustained recurrence separated real from sham in the rhythmic, articulatory and phonatory streams.
- **Prediction of communicative efficiency** (task success, 10–30, mean 19.2): models built on the entrained measures beat models built on the non-entrained ones in all three learners (lasso, SVM, kNN), with moderate-to-large effect sizes. Articulatory and rhythmic recurrence carried the prediction. "Phonatory feature entrainment played virtually no role."

## What matters for this engine
- **The right null for vocal coupling is a surrogate partner.** This is the first source in the repository's voice notes that tests vocal entrainment against sham dyads (voice-synthesis.md, open problems, asked for this). The finding that survives the surrogate is *sustained* co-organisation, not momentary matching. That supports measuring any engine–operator vocal coupling against virtual pairs, with the moulder-2018 caution.
- **Phonatory (pitch and voice-quality) entrainment exists against sham but predicted success least.** Together with Levitan's "pitch is personal" this weakens any argument that the agent's held pitch level must follow the operator's for the conversation to work.
- **What it cannot say.** CRQA at all lags mixes local and global coupling and gives no direction (who follows whom). The parameters were tuned to clinicians' ratings, so the measure is partly defined by what experts hear as "in sync". No held-level time course.

## Verdict: watch (method and surrogate design; weak on held levels)
Healthy students, one task, mostly women. The key tables did not survive extraction. The parameter choice is tuned to the outcome it is compared with (clinician ratings), though the efficiency outcome is separate.
