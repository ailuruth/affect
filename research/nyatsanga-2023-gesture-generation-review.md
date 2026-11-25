# A Comprehensive Review of Data-Driven Co-Speech Gesture Generation (Nyatsanga, Kucherenko, Ahuja, Henter, Neff; Eurographics STAR 2023)

Nyatsanga, S., Kucherenko, T., Ahuja, C., Henter, G. E., Neff, M. "A Comprehensive Review of Data-Driven Co-Speech Gesture Generation." Computer Graphics Forum 42(2), Eurographics 2023 State-of-the-Art Report. arXiv 2301.05339v4.

## What was read
- Sec. 2 (human gesticulation, incl. the passage on communicative intent); Sec. 5.3 opening paragraphs on deterministic regression and probabilistic models; the dyadic paragraph of Sec. 5.3 (DRAM and interlocutor-aware models); from Sec. 6 "Key Challenges": the section introduction, the opening of 6.1, and 6.3, 6.4 (all subsections) and 6.5 in full. I did not read the rest of 6.1, 6.2, Sec. 3-4, most of Sec. 5, or Sec. 7-8.

## Claims
- "Many gesture synthesis approaches, and all deep learning approaches that we are aware of, do not model a communicative intent. Instead, they synthesize gesture from audio, text or both. This necessarily means that the gestures will be redundant with these other channels, and thus more limited than actual human gesture."
- Deterministic regression "typically forces the model toward learning to generate the mean representation of the data, producing averaged motion for different inputs ... usually called regression to the mean." Probabilistic models (GANs, flows, VAEs, diffusion) are the standard response.
- Data-driven systems "tend to produce marginally natural gestures that appear more like well-timed hand waving, are not communicative and have little meaning ... they still do not handle semantic grounding of gestures properly".
- Interlocutor awareness (Sec. 6.4.4): "Characters must modify their behavior to react to the content, mood and timing of interlocutors. Characters must be able to be surprised, angered, pleased, etc. based on what their interlocutor may say." The authors present this as an open need and expect more work as dyadic data arrives.
- Emotion over time (Sec. 6.4.3): "It is important to be able to drive these emotions in a way that is consistent with a character's personality and to be able to shift mood and emotion over time."
- Separate channels (Sec. 6.5): "verbal behavior generation is considered separate from non-verbal behavior, and the generation of non-verbal behavior is in turn typically broken into several smaller sub-problems treated in isolation." "approaches that generate gesture based on text and/or audio are restricted to redundant gestures".

## Evidence (as reported in the review)
- GENEA 2022: median human-likeness of the best system was 69 (upper body) and 71 (full body), against 63 and 70 for human motion capture. The authors attribute part of this to mocap artifacts and to avatars without faces, gaze or lips.
- Interlocutor-aware models (Jonell et al. 2020; Nguyen & Celiktutan 2022) "found that statistically significant improvements in generated behaviors were achieved by being interlocutor-aware". The review gives no effect sizes.
- Weak grounding (6.4.6): even with all inputs, the gesture-given-context mapping may stay highly stochastic. The authors draw the analogy to prosody in text-to-speech.

## Failures documented
- **Regression to the mean.** Deterministic models produce averaged motion, which is flat output.
- **No communicative intent; language and nonverbal generated separately.** Motion is a function of already-produced speech, so it can only echo it.
- **Surface quality as the main research target.** "The most prominent research target ... has long been perceptual quality", because it is easier to measure than appropriateness.
- **Mood and emotion that shift over time are listed as unmet.**
