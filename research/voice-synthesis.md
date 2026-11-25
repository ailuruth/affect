# The emotional voice and conversational timing: synthesis

Sources (each read as its note says): banse-scherer-1996-acoustic-profiles.md, scherer-2003-vocal-communication-review.md, juslin-laukka-2003-vocal-music-same-code.md (abstract only), eyben-2016-gemaps.md, levitan-2011-2012-acoustic-prosodic-entrainment.md, pardo-2006-phonetic-convergence.md, stivers-2009-turn-taking-universals.md (summarizing fetch), levinson-torreira-2015-turn-taking-timing.md, ward-tsukahara-2000-backchannel-low-pitch.md, oller-2013-functional-flexibility-protophones.md (summarizing fetch), goldstein-schwade-2008-social-feedback-babbling.md, morise-2016-world-vocoder.md. Related notes already in the index: macos-speech-synthesis.md, pitchy.md, coordination-synthesis.md, fusaroli-2014-dialog-interpersonal-synergy.md, gergely-watson-1996-social-biofeedback.md, messinger-fogel-2007-social-smiling.md, jones-2009-development-of-imitation.md.

This note states constraints the engine's formal core must meet for the voice (Principle 10). It does not add a voice module.

## 1. What in the voice is innate and what is learned

Innate (present without social learning, fixed sign or fixed form):
- A source-filter body with a few physiological settings: breath (subglottal pressure, inhalation), laryngeal tension and register (F0 level), glottal adduction (pressed vs breathy, spectral tilt), pharyngeal width and lip spreading (formant shifts), articulation rate. Scherer's component-patterning predictions (Table 5 in scherer-2003) are stated at this level: "wide/narrow", "tense/relaxed/lax", "full/thin" voices are body settings, not emotions.
- A few fixed-sign vocal signals: cry (negative) and laugh (positive) have no individual differences and almost never occur with a neutral face (4%) (oller-2013). Scherer adds a novelty reflex: interrupted phonation and sudden inhalation.
- Turn alternation itself: proto-conversation with gaps of about 1.5 s at 3 months, shortening to about 800 ms before language (levinson-torreira-2015). Infants anticipate turn ends from prosody before they understand words.
- Probably a listener reflex to a prosodic cue: back-channels follow a 110 ms low-pitch region and can be produced without attending to content (ward-tsukahara-2000). The authors call it reflex-like; that is their reading, not a test.

Learned (shaped by living with particular people):
- Which vocal settings go with which internal state. Protophones (squeal, vowel-like, growl) carry positive, neutral and negative affect in every infant, with individual patterns, by 3-4 months (oller-2013). Only weak innate biases remain (squeals at affective extremes, vowel-like sounds near neutral).
- Vocal form, through contingency: 9.5-month-olds took up the pattern (resonant vowels or CV alternation) of their mother's contingent responses within 10 minutes, not her phonemes, and did not change with identical non-contingent responses (goldstein-schwade-2008). The learning signal is the timing of the partner's response relative to one's own act, not its warmth (smiles and touch were matched in both groups).
- Calibration of timing: what counts as "on time" (about 200 ms in Danish and Lao, under 100 ms in Japanese and Tzeltal; stivers-2009), back-channel uptake and latency (350 vs 700 ms after the cue; ward-tsukahara-2000), gap length accommodated to a new partner (ten Bosch, in levinson-torreira-2015).
- Accent and pronunciation drift toward partners, cumulative within a conversation and persisting after it (pardo-2006).

So the engine's innate vocal body should be a set of continuous physiological settings plus three or four fixed reflexes, and the map from latent state to those settings should be mostly learned. A fixed state-to-voice table (Scherer's predictions as a lookup) would contradict the protophone data. Scherer's predictions are better used as a prior or an initial bias than as the mapping itself.

## 2. Which acoustic dimensions carry affect

- Activation (arousal) axis: F0 level, F0 range and variability, loudness, tempo. These move together (F0-energy r = .62 in banse-scherer-1996). Emotion explains about 50-55% of residual variance in mean F0 and energy after speaker identity is removed. In resynthesis, F0 range had the largest effect on listeners (narrow = sad, wide = high-arousal negative) and the effects were mostly additive (scherer-2003).
- Quality axis: spectral balance and voice quality (low-frequency energy share, Hammarberg index, spectral slope above 1 kHz, H1-H2, HNR, jitter, shimmer). These can move against activation: sadness has mid F0 but the lowest energy and the most low-frequency energy, a lax voice from low coping potential (banse-scherer-1996). Scherer argues valence acts more through the source and spectrum than through F0, energy and rate.
- Speaker identity dominates: it explains more variance than sex in every domain except F0 (banse-scherer-1996). All features must be read relative to the speaker's own running baseline.
- Valence is weak in the voice alone. Every feature set from 62 to 6,373 parameters reaches about 80% binary recall for arousal and only 65-67% for valence (eyben-2016). Infants' identical protophones carry opposite valence, which the face disambiguates (oller-2013). The engine's valence has to live in the shared latent state and be expressed jointly by face and voice.
- Some states hardly use sentence prosody: disgust (15% recognized) and shame (22%) seem to be expressed by bursts or by silence (banse-scherer-1996). The voice body needs non-speech vocalizations and the option of not speaking.
- The feature list for perception and for measuring the engine's own output: GeMAPS LLDs (eyben-2016): semitone F0, jitter, shimmer, loudness, HNR, alpha ratio, Hammarberg index, spectral slopes 0-500 and 500-1500 Hz, F1-F3, H1-H2, H1-A3, plus voiced/unvoiced timing. Read these as continuous inputs, never as classifier outputs (Principle 1).

## 3. How vocal coupling between partners is structured

The data reject a single coupling gain. Per feature and per time scale:

| Feature | Global (session) | Local (turn exchange) | Time course | Source |
|---|---|---|---|---|
| Loudness | Proximity; the partner pulls a speaker off her own baseline | Strongest synchrony (r ≈ .47-.50) | Early, then increasing | levitan-2011 |
| Pitch level | Personal; closer to self than to partner; never reaches proximity | Proximity and small synchrony (r ≈ .28); only verified turn-level convergence | Continuous local adjustment | levitan-2011 |
| Voice quality (shimmer, NHR) | Personal style, converges | Weak synchrony | Late onset (second half of a session) | levitan-2011 |
| Jitter | No proximity | Synchrony small | Entrainment on it goes with awkwardness | levitan-2012 |
| Speaking rate | Personal but adjusts toward partner | Synchrony r ≈ .15 | Outliers draw more accommodation | levitan-2011, 2012 |
| Pronunciation | Converges, partially, never matches | n/a | Cumulative; persists after the conversation | pardo-2006 |
| Gap length | Accommodated to the partner | n/a | Over a conversation | levinson-torreira-2015 |
| Floor (who speaks) | Anti-phase by definition | Alternation | Continuous | levinson-torreira-2015, fusaroli-2014 |
| Back-channels | Complementary: listener answers the speaker's low-pitch cue | 350-700 ms after the cue | Per cue | ward-tsukahara-2000 |

Structural properties that follow:
- Convergence on some features (loudness, rate, pronunciation, gap length), relative synchrony without proximity on others (pitch), slow late convergence on voice quality, possible divergence on some (jitter), and complementarity on floor and back-channel. A coupling operator with one scalar gain cannot produce this; coordination-synthesis.md reaches the same conclusion for faces and physiology.
- Coupling is partial and keeps the producer's own bias: even shadowing never matches (pardo-2006). The engine approaches the operator in its own body's coordinates, consistent with Principle 3 and the rejection of direct mirroring.
- Coupling is directional and socially modulated: who converges to whom depended on role and sex, and reversed between pairs (pardo-2006); entrainment tracked "giving encouragement" and "trying to be liked" but not "trying to dominate" (levitan-2012). Each direction needs its own state-dependent gain.
- Salience raises coupling: partners of unusually loud or fast speakers accommodate more (levitan-2012). In a predictive perception model, coupling strength can scale with the surprise of the operator's value relative to the operator's own baseline.
- Slow vocal habit is a state, not a gain: convergence accumulates and persists (pardo-2006). The engine needs a slowly drifting vocal-habit variable per relationship, which is also the substrate for "manner of speaking learned by living" (S6).
- Principle 6 applies. Vocal convergence is read socially as wanting to be liked (levitan-2012); it must not become an instrument for approval. It should follow from the coupled dynamics, and divergence must stay available.

## 4. Timing constraints for a real-time engine

Numbers to design against:
- Floor transfer offset: mode about 200 ms (0-200 ms per language), mean about 200 ms across 10 languages, all language means within ±250 ms; 70-82% of transitions under 500 ms; gaps and overlaps under 120 ms are not perceived (stivers-2009, levinson-torreira-2015).
- Overlap: 30% of transitions are brief overlaps (modal 96 ms), only 3.8% of time is simultaneous talk, mostly back-channels (Switchboard, levinson-torreira-2015).
- Delay carries meaning: non-answers +132 ms, disconfirmations about +200 ms, visible responses -87 ms, questioner gaze -69 ms, the same in every language (stivers-2009). A system whose floor latency is 600-800 ms sounds dispreferred on every turn.
- Production is slow: 600 ms for a word, about 1500 ms for a sentence; inhalation for a long reply over 500 ms, usually starting about 15 ms after the other's turn ends; articulator preparation 120-180 ms before sound (levinson-torreira-2015).
- Reacting to silence cannot produce the observed distribution (at least 400-550 ms); turn ends are predicted from prosody, and a short go-signal releases a prepared response.
- Back-channel opportunity: after 700 ms of the other's speech, a 110 ms region below the 26th percentile of the speaker's recent pitch, a refractory 800-1000 ms; respond 350-700 ms later; ±500 ms is still heard as natural; listeners take only some opportunities (ward-tsukahara-2000).
- Contingency window for learning: partner responses within about 2 s of one's own vocal act (goldstein-schwade-2008).

Consequences: Claude cannot be on the floor-transfer path (Principle 4 already says so). The fast loop must (a) predict the operator's turn end from prosody continuously, (b) hold a prepared opening (breath, particle, back-channel, nod, facial onset) in the vocal and facial body, (c) release it on a go-signal at 100-300 ms, and (d) set its own latency from state, so that hesitation and disagreement are audible. Words from Claude arrive later and continue a turn the body has already opened. A silence-threshold endpointer (500-800 ms) is the baseline to beat, not the design.

## 5. Implications for the engine's voice body

A proposal at the level of constraints, for the core to derive or reject:

1. Vocal body = continuous source-filter settings, updated per 5-10 ms frame: F0 level and range (semitones relative to an innate baseline), loudness, tempo and segment lengthening, spectral tilt (pressed vs breathy), aperiodicity (breathiness, roughness), formant shift (tract length, lip spreading, shared with the face's lip corners), breath events. WORLD resynthesis over macOS TTS output realises all of these on CPU at about 0.04 of real time for analysis plus synthesis and 0.007 for synthesis alone, measured here (morise-2016). The voice identity remains the operator's choice (Principle 8).
2. Innate reflexes with fixed sign: cry-like and laugh-like vocalizations, the novelty catch (interrupted phonation, inhalation), and the low-pitch back-channel reflex (opportunity only; uptake by state).
3. Learned map from latent state to vocal settings, initialised by a weak prior (Scherer's check-to-setting table, banse-scherer-1996 results) and shaped by the operator's contingent responses to the engine's own vocalizations (goldstein-schwade-2008), never by imitation of the operator's surface voice and never by approval as reward.
4. Perception through the same parameters: the operator's GeMAPS-style features relative to the operator's running baseline, read by inverting the engine's own vocal body (Principle 3; the Brunswikian lens of scherer-2003 with the engine's encoding weights as its cue-utilization weights).
5. Coupling per feature and per time scale, directional and state-modulated, as in the table in section 3, with a slow vocal-habit state per relationship.
6. Timing as an output of state, under the budget in section 4, executed by the fast loop.

Ablation predictions to write before building (Principle 5):
- Remove the spectral-tilt and aperiodicity controls, keep F0, loudness and rate: third-party listeners should still track the engine's arousal but lose most of its quality differences (tense vs lax), and the engine's voice should stop distinguishing states that share activation.
- Remove contingency from vocal learning (yoke the operator's responses to another session's timing): vocal form should stop drifting toward patterns the operator responds to, while vocal amount still rises with arousal (the yoked result).
- Remove the slow coupling term: second-half voice-quality convergence should vanish while turn-level loudness synchrony remains (levitan-2011 measures).
- Replace prosodic turn-end prediction with a silence endpointer: floor-transfer offsets should shift from a 200 ms mode to 500 ms or more, and the confirmation/disconfirmation latency difference should be swamped.
- Clamp response latency to a constant: the latency difference between agreeing and disagreeing turns (130-200 ms in humans) should disappear.

## Open problems

- No source here tests vocal coupling against surrogates the way moulder-2018-synchrony-surrogates.md requires; Levitan's ten-permutation check is weaker. Engine evaluation should use proper surrogates.
- Valence in the voice: no feature set gets past 67%; the joint face-voice reading has not been measured in the same way.
- Whether back-channelling is a reflex or an attended act is untested; it decides whether the cue detector belongs to the innate body.
- Protophone flexibility shows learned use of vocal settings, but nobody has shown how the mapping is learned; the contingency result is the best candidate mechanism.
- Pardo's role and sex effects reversed between pairs; nothing yet predicts the direction of convergence from a measurable state.
- The LF glottal source model was not read; whether a physiological source beats WORLD's envelope-plus-aperiodicity for voice quality is undecided.
- Juslin & Laukka 2003 was read only as an abstract; its cue tables would refine section 2.
- Everything here is from adult-adult or infant-caregiver dyads; how people couple vocally with a synthetic voice, and whether the operator converges on the engine's voice (the vocal analogue of S5), is unmeasured.
