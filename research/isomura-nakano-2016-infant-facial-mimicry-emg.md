# Isomura & Nakano 2016, "Automatic facial mimicry in response to dynamic emotional stimuli in five-month-old infants" (Proceedings of the Royal Society B 283:20161948, doi:10.1098/rspb.2016.1948, PMC5204153)

Source read: the full article from PubMed Central (introduction, methods, results with Tables 1 and 2, discussion and limitations). The supplementary waveform figure (S1) was NOT read; the data on Dryad were not downloaded.

Read for search pass 8 (topic 3: development of facial mimicry and its limits).

## Key claims
- **Design.** Facial EMG over left corrugator supercilii (brow lowerer) and zygomaticus major (lip-corner puller) in 4-5-month-olds (final N = 15, mean 154.6 days; 25 more recruited and excluded, 16 of them for crying or incomplete data). Clips of three adult women, 3 s each, three per trial. Conditions: **AV** (crying or laughing face with congruent vocalisation, deliberately not temporally synchronised), **V** (expressive face with a neutral voice), **A** (expressive voice with a neutral face), and a neutral control. Baseline from the preceding fixation clip; 500-ms windows; Wilcoxon tests, Bonferroni p < .05/18.
- **AV only, 500-1000 ms:**
  - brow muscle to crying vs control: Z = 3.2, p = .0004, r = .82;
  - cheek muscle to laughter vs control: Z = 3.0, p = .001, r = .78;
  - both effects at 500-1000 ms after onset, the same latency as in adults (about 500 ms).
- **No response to unimodal stimuli** (face only, or voice only) in any window, for either muscle. A study cited as unpublished reports no EMG mimicry at 3 months.
- **Repetition:** brow activity fell across the three clips of a trial (significant for auditory cry and for neutral control), cheek activity rose (significant for neutral control); the authors attribute this to the muscle, not to the stimulus content.
- **Proposed mechanism (discussion, not tested):** infants' own expressions "often induce adults around them to produce similar expressions", providing visual input that links motor output to their own experience; "Hebbian associative learning" across perception, action and affect.
- **Limits stated:** small N; conservative statistics may hide unimodal effects; asynchronous AV stimuli; only female models; baseline variability from different fixation clips.

## What it means for the engine
1. **Early mimicry needs agreement across senses.** At 4-5 months the brow and cheek responses appear only when face and voice carry the same content. In engine terms: an early echo route that fires only when the partner's face channel and voice channel agree, which is a property a learned multimodal gate gives without a rule (the agreement is learned from co-occurrence). It is also a natural robustness: a single deceptive channel does not drive the echo.
2. **Channel-specific dynamics under repetition** (brow habituates, cheek sensitises) show that per-channel echo strength is not one gain even within a 9-s trial. The engine's per-channel ceilings (D93) are compatible; a single shared habituation constant would not reproduce this.
3. **Timing.** 500-1000 ms onset of the echo matches the build core's quick echo latency (about 0.45 s onset, 0.8-1.0 s laugh echo) closely enough; no change.
4. **What it does not show:** whether this is matching of the seen movement or the infant's own reaction to the situation (the authors say they cannot separate them). So it is not evidence for an innate seen → done map; it fits a learned one (Hebbian, as the authors propose) as well.
5. Vocabulary: "crying" and "laughter" are the stimulus categories of the source; in the engine only the channels (brow lowerer, lip-corner puller, voice features) exist.

## Verdict
- **background (developmental timing and limits; small N).** Mimicry of two channels is present by 5 months, only for multimodal input, with channel-specific repetition effects. It constrains the engine's early echo (multimodal agreement; per-channel dynamics) and does not change the learning question.
