# Levinson & Torreira 2015, "Timing in turn-taking and its implications for processing models of language"

Frontiers in Psychology 6:731. doi:10.3389/fpsyg.2015.00731. Open access (CC BY).

Source read: the published PDF (22 pp.), read in full except the conversation-analytic transcript examples in sections 2-3 (skimmed) and the references. Tables 1-3 came out of text extraction without their numbers; the values below are from the prose.

## Claims
- Puzzle: gaps between turns are typically 100-300 ms (mode about 200 ms), yet producing even a single word takes about 600 ms from concept to articulation (Indefrey & Levelt 2004; over 1000 ms cross-linguistically in Bates et al. 2003), two nouns 740-800 ms, three words 900 ms, a simple sentence about 1500 ms. Therefore responders plan their turn while the other is still speaking, which requires predicting both the content (speech act) and the end of the incoming turn.
- Corpus facts:
  - Heldner & Edlund 2010 (Dutch, English and Swedish corpora): floor-transfer-offset mode about 200 ms; about 60% of transitions gaps, 40% overlaps (any overlap over 10 ms); 41-45% of gaps longer than 200 ms; 70-82% of transitions shorter than 500 ms; 51-55% under 200 ms. A gap or overlap under 120 ms is not perceived as either (Heldner 2011).
  - Stivers et al. 2009, 10 languages, polar questions: means 7-468 ms, modes 0-200 ms; the same factors speed or slow answers everywhere.
  - New Switchboard analysis by the authors (348 telephone conversations, ~38 h): 77% of signal one speaker, 19.2% silence, 3.8% both. Between-overlaps are 30.1% of floor transfers, modal 96 ms, median 205 ms, mean 275 ms. Within-turn overlaps mostly short and mostly backchannels; overlaps occur at principled places (after a possible completion, simultaneous starts, backchannels). Average inter-pausal unit (IPU) 1680 ms.
  - Same-speaker pauses are about 140 ms (c. 25%) longer than between-speaker gaps (ten Bosch et al. 2005).
  - Individuals accommodate their gap length to a new partner (ten Bosch et al. 2004, 2005). Speaker A's speech rate correlates inversely with B's response timing: not a shared beat.
  - Overlap rises from 44% face-to-face to 52% on the telephone; transitions are faster on the phone.
  - Answers to wh-questions are slower than to polar questions; longer answers need more preparation, visible in breathing.
- Against reaction-to-silence: silence is recognizable only after about 200 ms (voiceless stops last up to 180 ms), and a prepared minimal vocal reaction takes another 200 ms, a two-choice reaction 350 ms. So reacting to silence gives at least 400-550 ms, which does not fit the modal 200 ms.
- Against a coupled-oscillator account (Wilson & Wilson 2005): human synchronization works by temporal estimation, turns vary too much in length for a firefly-style reset, and gap entrainment does not extend to within-turn pauses. A syllable-level readiness rhythm is left possible but unconfirmed.
- Development: "proto-conversation" between caregiver and infant shows alternation with gaps of about 1.5 s at 3 months, falling to about 800 ms in the pre-linguistic months; gaps lengthen again (toward 1.5 s in toddlers, about 1 s at 5 years) as language enters. 1-2-year-olds anticipate turn ends better than chance and do better with prosody alone than with words alone; adults use both. Turn-taking is established before language and "forms a framework for language acquisition".
- Production latencies in the body: decision to inhale reaches the intercostal muscles after 140-320 ms; an inhalation in dialogue is over 500 ms; short answers are made on residual air, longer ones with a planned inhalation that typically starts about 15 ms after the question ends; tongue preparation precedes acoustic onset by 120-180 ms (some effects 480 ms).
- Comprehension runs 3-4 times faster than articulation; EEG shows speech-act prediction within the first 400 ms of a turn and response preparation about 1200 ms before its end.
- Sketch model (Figure 3): the listener identifies the speech act early, plans the response in parallel with comprehension, readies the vocal apparatus (about 200 ms of pre-articulation, inhalation decided), buffers the start of articulation, and releases it on a "go-signal" from turn-final cues (prosodic and syntactic completion, possibly gesture). The modal 100-300 ms gap is the reaction time to that go-signal. Launching without waiting would make overlap or zero gap the mode; planning only after the cue would make gaps of 500 ms or more the mode.

## Evidence with numbers
As above; the Switchboard analysis is the paper's own data, the rest is review.

## What it implies for an engine whose voice is driven from an internal state through an innate vocal body, with real-time timing
- Hard timing budget. To be heard as no-gap the engine's onset must fall roughly 0-300 ms after the operator's turn end, with under 120 ms imperceptible; 500 ms is the edge of the normal distribution, beyond about 700 ms a gap becomes meaningful (see stivers-2009-turn-taking-universals.md). Claude's text generation cannot meet that from a cold start; Principle 4 already says the fast loop never waits for Claude. The engine needs a fast vocal layer that can start a turn (breath, particle, backchannel, facial onset) on the go-signal while words are still being produced.
- The architecture the paper argues for maps onto the engine: (1) a predictive model of the operator's turn end, driven by prosody (final pitch, lengthening, intensity drop) and running continuously; (2) a buffered, prepared response in the vocal body; (3) a fast go-signal detector. Reacting to silence alone (the usual voice-activity-detection endpointing, waiting 500-800 ms of silence) gives the wrong distribution and should be an ablation baseline, not the design.
- Breathing is part of the innate vocal body and of timing: inhalation is planned for long responses and starts at the other's turn end. An engine voice that inhales audibly before longer turns gives a natural "I'm about to speak" cue and a measurable timing variable.
- Gap length is coupled between partners (accommodation to a new partner's gaps) but turn-taking is anti-phase in speech: this is a case where coupling must be complementary, not imitative. The engine should converge on gap length while alternating the floor.
- The infant data say turn alternation precedes language and gaps shorten in the first months: an innate alternation reflex with a learned, shrinking latency is a developmental route the engine could follow, with timing learned from living with the operator rather than set.
- Timing itself carries affect and stance (slower answers to harder or dispreferred responses). The engine's response latency should be a state-dependent output, not only a system latency to minimise.

## License
CC BY 4.0 (Frontiers). No code; Switchboard is LDC-licensed and was not downloaded.

## Verdict: adopt (timing constraints and the predict-prepare-release architecture for the engine's fast vocal layer)
The sketch model is a proposal, not tested as a whole; its parts rest on separate experiments.
