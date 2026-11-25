# Ward & Tsukahara 2000, "Prosodic features which cue back-channel responses in English and Japanese"

Journal of Pragmatics 32(9):1177-1207. doi:10.1016/S0378-2166(99)00109-5.

Source read: the author's PDF (Ward's UTEP site), sections 1-6.6 read in full except the example transcripts with pitch plots in section 2.1 (skimmed); sections 6.7-7 (conversation analysis method, summary) skimmed. Table 1-2 values were recovered from text extraction and matched to rows using the prose.

## Claims
- Definition of back-channel feedback (from the producer's side): (D1) responds directly to the content of the other's utterance, (D2) is optional, (D3) does not require acknowledgement by the other. Not defined by lexical items (laughter, coughs and sniffs can function the same) nor by function: back-channels can show attention or boredom, agreement or scepticism, and look both backward (receipt) and forward ("channel is open, please continue").
- Prevalence: 19% of utterances in 1,155 American English conversations (Jurafsky et al. 1997); more frequent in Japanese.
- The cue: a region of low pitch late in an utterance. Rule for English: (P1) pitch below the speaker's 26th-percentile level, (P2) lasting at least 110 ms, (P3) after at least 700 ms of speech, (P4) no back-channel output in the preceding 800 ms, (P5) then produce a back-channel 700 ms later. Japanese: P1 = 28th percentile, P2 = 110 ms, P3 = 700 ms, P4 = 1000 ms, P5 = 350 ms.
- Implementation runs online: 10 ms frames, 8 kHz audio, percentile thresholds computed only from past input, the pitch distribution over the last 50 s (so the threshold adapts to the speaker's current range), pitch "spread" up to 80 ms across unvoiced frames to bridge consonants, creak and fading phrase ends; speech/non-speech from an energy histogram with gaps up to 250 ms merged.
- What low-pitch regions do: mark "this completes that thought, did you follow?"; occur with disfluencies ("I'm stuck, but keep listening"; the lengthened "the", "and", "um"); with Japanese "ne"; and in groans, parentheticals and self-directed speech (where they mislead the rule). An abrupt drop in pitch and/or energy tends to mark turn end instead, and an upturn after low pitch turns the cue into a request for a full reply.
- Corpus: English 8 conversations, 68 min, 12 speakers (the first author in 5), 359 back-channels; Japanese 18 conversations, 80 min, 24 speakers, 873 back-channels. Mostly seated without sight of each other (telephone-like), so no gaze or nod cues.
- Evaluation: a prediction counts if within ±500 ms of an observed back-channel onset (shifts of 500 ms were judged still natural). English low-pitch rule: coverage 48% (172/359), accuracy 18% (172/936) vs random 13%. Japanese: accuracy 34% vs random 24%. The rule beat random for 15 of 16 English speaker-sides and most Japanese ones, and with windows down to 100 ms. Silence onset is a poor cue: a 150 ms silence rule was less accurate than random (5% vs 13% English; 16% vs 24% Japanese). Lexical cues (ne, kedo, kara) were at chance. Vowel lengthening and creak mostly co-occur with low pitch.
- Ceiling: of the Japanese rule's misses, 16% fell during the other's speech and 44% were places a back-channel "could naturally have appeared" but the listener chose silence; judged against one speaker alone the rule reached 66% accuracy and 69% coverage. Estimated ceiling for any speaker-only rule: about 95% coverage, 61% accuracy. Respondent-internal factors (speed of understanding, attitude to the speaker) decide the rest.
- English and Japanese differ in uptake (English listeners take fewer opportunities) and in latency from cue to response (700 vs 350 ms). "Some of the huge perceived differences in conversation style and culture may reside in this 350ms timing difference."
- Live test: a system back-channelling on the low-pitch rule sounded natural to third-party judges and random back-channels sounded odd; the people talking to the system were not obviously affected.
- Status: back-channels can be produced without attending to content for 5-10 s; the authors suggest a reflex-like response to a prosodic cue, handled by a channel separate from comprehension, with which back-channel is produced (its form) left to other factors. Non-word back-channels ("grunts") may be composed on the spot, each sound component carrying meaning.

## Evidence with numbers
See above. Small corpora; one author is a speaker in 5 of 8 English conversations; parameters tuned on the same data used to evaluate them; ±500 ms tolerance is generous.

## What it implies for an engine whose voice is driven from an internal state through an innate vocal body, with real-time timing
- Back-channelling is the clearest case of a fast vocal reflex that runs without the conceptual layer, which is exactly what Principle 4 requires of the fast loop. A low-pitch detector on speaker-relative pitch (running percentile, 110 ms region, refractory period) is cheap and fits the S2 perception stack (pitchy gives pitch and voicing per frame at ~0.12 ms).
- The rule gives the timing structure of a listener reflex: cue -> refractory gate -> fixed latency (350-700 ms here) -> response. In the engine the latency, the uptake probability and the refractory interval should be state-dependent and learned per operator (the cultural difference is in exactly these parameters), while the cue detector is innate.
- Whether to respond is not determined by the cue: 44% of "misses" were optional silence. So the cue sets an opportunity, and the engine's internal state (attention, arousal, interest in the content) decides uptake. This is a good place for need-conditioned selection (brief, Expressive structure): the same cue produces a back-channel, a nod, a smile or nothing depending on state.
- Form carries state: back-channels can express boredom or scepticism as well as interest. The innate vocal body should produce non-lexical vocalizations (grunts, "mm", breath, laughter) whose sound components (pitch movement, length, nasality, loudness) are set from state, which is also a path to the face (nods and smiles are visible back-channels, absent from this voice-only corpus).
- The finding that listeners did not notice random back-channel timing while third parties did cautions evaluation: naturalness judged by the operator in the loop may be insensitive; use third-party judges and objective timing distributions too.
- Silence is not the cue. Turn-taking and back-channelling should both be driven by prosodic prediction, not end-of-speech detection (consistent with levinson-torreira-2015-turn-taking-timing.md).

## License
Elsevier, all rights reserved; author copy. No code or corpus released.

## Verdict: adopt (low-pitch back-channel cue as an innate listener reflex with learned, state-dependent uptake and timing)
Replicated in later work (Ward and others) but with modest accuracy; treat as one cue among several, not a complete listener model.
