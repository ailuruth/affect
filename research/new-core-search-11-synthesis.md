# Searching for a new core mechanism, eleventh pass: the voice. How the agent's own state should set pitch, loudness and timing under a limit per setting, and which voices to offer for Q1 (synthesis, 2026-11-28)

## In plain terms

- **This pass chooses a component. It does not look for a core.** Q1 (research/questions.md) is open: the operator will pick the agent's voice later, and speech stays off until then. This pass read the main papers on controlling the voice of a speech synthesiser, and the current open models that run locally, so that he can be given a short set of options.
- **The current plan is the right shape.** The build spec (§1.7) has a speech synthesiser say the words in a fixed voice. The engine then re-renders the sound (WORLD resynthesis) and sets six numbers itself: pitch level, pitch range, loudness, speaking rate, pauses and reply delay. Each number has its own limit, and the result is measured after rendering. The synthesiser supplies only the words and the voice. Because each setting is a separate number, each limit holds separately, which is what Q18 asks for.
- **The "style" controls from the research literature cannot do this.** Style tokens, prosody embeddings and style vectors learn a few knobs from recordings of actors and audiobook narrators, without labels. Each knob moves several settings at once. One paper says so itself: a low-pitched token "can also encode a slower speaking rate". The knobs only get their names ("animated", "calm", "speed") after someone listens to them. Driving the voice through them would copy the patterns of human emotional speech, and no separate limit per setting could be kept. Rejected.
- **One new practical finding.** Kokoro-82M is a small open voice model under the Apache-2.0 licence. Its public interface offers only a speed setting, but inside it computes a pitch curve, a loudness curve and a duration for each sound, and passes them to its sound generator. The engine could write those curves itself. That would probably give more natural intonation than re-rendering, with the same limits, as long as the after-rendering check stays in. It is an option to test later, not something to build first.
- **The choice that is the operator's** is which voice. A fixed synthetic voice and a clone of a real person are very different choices.
- **Recommendation for Q1:** one of Kokoro's fixed voices, chosen by him by listening (or a blend of two), rendered through the WORLD stage that is already built. Second choice: a macOS voice through the same stage. That works today with nothing to download. Not recommended: cloning anyone's voice, his own included.

## Scope of this pass
Q1 asks only for the voice's identity. The design question behind it is how the agent's latent state drives the six phrase-level voice channels of the channel table (spec §1.1, rows 14–19): F0 level (c = 0.05), FR F0 range (0.10), EN energy (0.05), RT rate (0.05), PAU pause (0.05) and LAT latency (0.05). Each channel is signed. The fast gear adds only a within-phrase contour. Each partner-caused part stays under κ c_k through the ledger (§4.1). The renderer is spec §1.7: TTS, then WORLD with F0(t) = F0_agent · exp(level + range × template(t)) from two innate templates (statement, question), chosen by the text's question form only; per-phrase RMS set to EN; time-warp to RT; TTS pauses replaced by 0.20 s / 0.40 s × the pause factor; onset at the latency target; A9 checks level, range, EN and RT to ±1 % after rendering. Three designs are compared:
- (a) the current plan: any TTS for identity, then WORLD resynthesis with explicit per-channel values;
- (b) a TTS whose decoder takes explicit F0, energy and duration inputs (FastSpeech 2 style);
- (c) learned style latents (GST, prosody embeddings, VAE latents, the StyleTTS 2 style vector).

## Sources read (notes in research/)

| Note | What | How fully |
|---|---|---|
| wang-2018-global-style-tokens.md | GST: unsupervised style tokens in Tacotron | full text except references; audio demos not heard |
| skerry-ryan-2018-prosody-transfer-tacotron.md | learned prosody embedding; transfer | full text except references; Table 1 from layout extraction |
| ren-2020-fastspeech-2.md | explicit duration, pitch and energy inputs | full text with appendices A–E; some table cells lost in extraction |
| li-2023-styletts-2.md | style diffusion; decoder with explicit F0 and energy curves | main text in full; appendices A, B.3–B.4, D read; C, E, F, G skimmed; GitHub README and LICENSE |
| hsu-2018-gmvae-tacotron.md | Gaussian-mixture VAE latents (optional item) | §1–4 in full, appendix G.1; other appendices skimmed |
| kokoro-82m.md (update) | current state; `kokoro/model.py` and `pipeline.py` read in full; commit list | code and README in full; model card not reachable |
| piper-tts.md (update) | current state; README, Python API, commit list | README and API doc in full |
| parler-tts.md | text-description control | parler-tts and dataspeech READMEs in full; paper not read |
| f5-tts.md | flow-matching, cloning | README only |
| melotts.md | VITS-based, fixed speakers | README and install doc |
| coqui-xtts.md | cloning; model licence | README and XTTS doc; licence text not read |
| voxcpm2.md | 2026, Apache-2.0, instruction control | README only |
| wordvoice-2026.md | 2026, explicit word-level controls | abstract only |
| magic-tts-2026.md | 2026, explicit duration and pause | abstract only |

**Already in the repository and used as their notes state:** macos-speech-synthesis.md, kokoro-82m.md, piper-tts.md, chatterbox.md, morise-2016-world-vocoder.md, voice-synthesis.md, levitan-2011-2012-acoustic-prosodic-entrainment.md; spec §1.1, §1.2.4, §1.7, §4.1; Q1 and Q18.

**Not reachable from here:**
- huggingface.co is outside this session's network. The model cards of Kokoro, StyleTTS 2, Parler-TTS, MeloTTS and F5-TTS could not be read. Kokoro's training-data and voice-provenance statements are therefore taken only from kokoro-82m.md, which read the card on an earlier pass.
- The GitHub API was refused (403); commit lists were read from github.com pages.
- Not read, so not cited for any claim: the Coqui Public Model License text, the Lyth & King 2024 paper behind Parler-TTS, and the WordVoice and MAGIC-TTS papers beyond their abstracts.

**Vocabulary.** No emotion labels or named emotion variables are proposed for any layer below Claude. Where a paper uses emotion words (StyleTTS 2's five text emotions, VoxCPM2's instructions, Parler-TTS's descriptions), that is reported and the method is rejected for it. Channel codes are the spec's.

## What this pass adds (in short)
1. **A precise condition for per-channel ceilings on the voice** (§1): the ceilings hold at the loudspeaker only if the renderer is *channel-diagonal and calibrated*: each commanded channel moves only its own measured feature, by the commanded amount. Design (a) meets it by construction, and A9 checks it. Design (b) meets it only approximately, so a check and correction after rendering are required. Design (c) cannot meet it, because a latent coordinate is not a channel.
2. **Kokoro already contains design (b).** Its decoder takes `F0_pred`, `N_pred` and per-phoneme `pred_dur`, all computed in the open in `forward_with_tokens` (kokoro-82m.md, update). Nothing else among the local, licence-clean options exposes this.
3. **A second route from words to voice, to keep closed.** StyleTTS 2-family models predict pitch and energy from the *text*, and their style vectors cluster by the emotion of the sentence (li-2023-styletts-2.md). Left in, that is a route from Claude's words to the six voice channels that bypasses the engine's state and its ledger. The spec's innate templates, chosen "by the text's question form only", already close it. Any TTS adopted must keep it closed.
4. **Draft Q1 options and a recommendation** (§4).
5. **No new core** (§5).

---

## 1. What a per-channel ceiling needs from the renderer

Let y = (y_F0, y_FR, y_EN, y_RT, y_PAU, y_LAT) be the phrase-level commands for channels 14–19. Upstream, the ledger keeps each partner-caused part |Δy_k| ≤ κ c_k (spec §4.1). Δy_k is the difference between the factual run and the run in which his face stays neutral. The renderer produces audio R(text, y). Measure it with the same functions φ the agent uses to hear the operator (spec §1.2.4), giving m_k = φ_k(R(text, y)). For any two command vectors y, y′ and the same text, suppose

  |m_k(y) − m_k(y′)| ≤ α_k |y_k − y′_k| + Σ_{j≠k} β_kj |y_j − y′_j|.

Then the partner-caused part of what the operator actually hears on channel k is bounded by κ (α_k c_k + Σ_{j≠k} β_kj c_j). That is at most κ c_k for every k only when α_k ≤ 1 and β_kj = 0. In words: each channel must move only its own feature (no crosstalk) and by no more than commanded (calibrated). Otherwise a partner-caused change on one channel leaks into another and uses up that channel's limit. If FR leaks into EN with β = 0.2, for example, EN's effective limit becomes 0.05 + 0.2 × 0.10 = 0.07, which is 40 % over.

What the other parts of Q18 ask of the renderer:
- *each channel's strength set separately:* a separate command per channel;
- *able to flip sign:* the renderer is defined and symmetric for negative y_k within ±c_k;
- *bounded:* clipping at c_k on the command, plus the check after rendering;
- *never settling into copying:* the renderer must add no partner path of its own (it must not read his audio) and must hold no state across phrases. The dynamics against copying live upstream, in the ledger and the contracting routes (new-core-search-10-synthesis.md).

## 2. The three designs compared

### (a) Any TTS for identity, then WORLD resynthesis with explicit per-channel values (current plan)
- **Calibrated and diagonal by construction.** WORLD keeps F0, spectral envelope and aperiodicity as separate streams (morise-2016-world-vocoder.md). The spec *replaces* the TTS's F0 with the engine's own formula; RMS is reset per phrase after the pitch change, so pitch cannot leak into loudness; the time-warp changes duration and nothing else; pauses and onset are inserted by the engine. A9 measures level, range, EN and RT after rendering to ±1 %. This is the only design in which β_kj = 0 holds by construction and is also checked.
- **Sign flips:** every formula is symmetric in its parameter.
- **What the TTS still contributes:** segmental quality, timbre (the identity), within-phrase relative durations (lexical stress), and its spectral envelope. None of these is a counted channel, none reads the partner, and the TTS's own learned intonation (its prosody predicted from text) is thrown away. So the choice of TTS is purely an identity choice. Its prosody quality hardly matters; clean, noise-free output matters more, because WORLD's F0 analysis (DIO) needs clean input.
- **Costs:** intonation is set by only two innate templates, so speech can sound flatter than the TTS alone would; the perceptual quality of WORLD's manipulations is untested (morise note). The ceilings are small (0.05–0.10 in normalised units), so manipulations stay near the TTS's own range, which limits artefacts.
- **Measured speed so far:** WORLD analysis plus synthesis takes RTF 0.043 on this Mac (morise note). The TTS dominates the time (below).

### (b) A TTS with explicit F0, energy and duration inputs
- **The pattern:** FastSpeech 2's variance adaptor feeds duration, a WORLD-extracted pitch contour (normalised per utterance, mean and variance stored separately) and frame energy into the decoder. In training these come from the recording; at inference they can be anything (ren-2020-fastspeech-2.md). StyleTTS 2's decoder does the same, G(h_algn, s, p_x, n_x) (li-2023-styletts-2.md), and so does Kokoro, which is built on it (`self.decoder(asr, F0_pred, N_pred, ref_s[:, :128])`).
- **For the ceilings:** separate inputs make a separate, clipped command per channel easy, and the decoder renders the requested contour as natural speech, with no vocoder pitch shift. But the decoder is a learned map. No paper read measures how exactly the output follows a commanded F0 or energy, or whether a pitch edit changes perceived loudness. FastSpeech 2 shows F0 scaled 0.75–1.5× "high-quality" in figures only, and in human speech F0 and energy co-vary (voice-synthesis.md §2). So α_k ≈ 1 and β_kj ≈ 0 must be measured, and the after-render check (A9) must become a correction: measure m, then rescale RMS or nudge F0 with WORLD until the targets are met to ±1 %. In practice (b) runs with (a) behind it as the enforcer.
- **Words-to-voice route:** the predictor's F0_pred and N_pred depend on the text and the style vector. Under (b) the engine must discard them and write its own curves, built from the innate template, F0_agent, level and range. Otherwise the TTS's text-to-prosody statistics decide the voice channels (§ "What this pass adds", item 3). Kokoro's style vector is a fixed tensor per voice (no diffusion at inference), so with a fixed voice the only remaining dependence is on the text, and it is discarded.
- **What it gains over (a):** probably more natural voice quality when the contour departs from the TTS's own, since the decoder was trained to render the given contours. The gain is unmeasured.
- **Cost:** a code change in the engine's own call into Kokoro (the public API has only `speed`), and an M5 test of decoder fidelity and crosstalk.

### (c) Learned style latents (GST, prosody embeddings, VAE latents, StyleTTS 2's style vector)
- **What they import.** In every paper read, the latent is learned from expressive human speech: GST and GMVAE from 147 h of one narrator reading "in an animated and emotive storytelling style"; StyleTTS 2 from LJSpeech, VCTK and LibriTTS. The latent captures that corpus's main modes of variation, in the bundles in which pitch, rate, energy and voice quality co-occur in those recordings. They are trained without labels, but their axes are identified and named after training by listening ("lower-pitch", "animated", "calm", "speed"). StyleTTS 2's style vectors cluster by the emotion of the text, and GST's authors propose them for automatic style annotation, emotion included. So the answer to "do style tokens import the surface statistics of human emotional speech, or label-like dimensions?" is: **both**. The statistics are imported by construction, and the dimensions become label-like in use.
- **Can per-channel ceilings be enforced on them? No.** A latent coordinate is not a channel. In the inequality of §1 the command is z, not y, and every m_k depends on every z_i through a nonlinear map that changes with the text:
  - GST: "a low-pitched token ... can also encode a slower speaking rate";
  - GMVAE, the most disentangled case: the "rate" dimension moves mean F0 from 197 to 183 Hz across ±3 σ (Table 10);
  - Skerry-Ryan: the embedding carries absolute pitch and enough identity for a speaker-ID model to name the reference speaker in 61 % of outputs.

  A bound on z_i therefore bounds several channels at once, in proportions the agent cannot set. That is exactly the single quantity that runs several channels which Q18 excludes. Bounding each m_k would need a supremum over all reachable z and all texts, which nobody can compute. The only way to enforce c_k is to measure the rendered audio and correct it, channel by channel. At that point the explicit renderer of (a) is doing the enforcing, and the latent contributes only the covariation that then gets clipped.
- **Sign flips:** outside the training range. GST reports reversed effects at negative scales; Hsu et al. report tremolo and an abnormally long first syllable at a GST weight of −0.1.
- **Copying:** reference-audio modes (GST transfer, prosody transfer, StyleTTS 2 and every cloning model) are prosody copying by design. Fed the operator's voice, they would be direct mirroring, and they would need his audio rather than features (Principle 7).
- **Verdict:** rejected for the six channels. The one admissible use of a style latent is as part of a fixed identity (Kokoro's voice tensor), held constant and never driven by the state.

| | per-channel command | calibrated, no crosstalk | sign flip | no partner path in renderer | words-to-voice route | naturalness |
|---|---|---|---|---|---|---|
| (a) TTS + WORLD | yes | by construction; A9 checks | yes | yes | closed (templates) | flatter intonation; WORLD artefacts untested |
| (b) explicit-input decoder (Kokoro internal curves) | yes | approximately; needs a check and correction after rendering | yes, within the training range of curves | yes | closed only if the predictor's curves are discarded | likely better; unmeasured |
| (c) style latent | no | no | outside the training range | no, in reference mode | open (text-conditioned style) | best in papers; human-statistics bundles |

## 3. What is the operator's: identity, licences, data

- **Which voice.** A visual-identity-style decision (Principle 8, Q1). F0_agent, the agent's rest pitch, is part of the identity. By default it should be the chosen voice's own median F0, so that WORLD shifts stay small.
- **A fixed synthetic speaker or a cloned real person:**
  - *macOS voices:* system voices, used as installed; no separate weights. The macOS licence terms for this use were not read in this or the earlier pass.
  - *Kokoro voices:* fixed voice tensors. Code and weights are Apache-2.0. The card, read on an earlier pass, says it was trained on permissive or non-copyrighted audio, including synthetic data. Two or more voices can be averaged (`load_voice` takes comma-separated names), which gives a voice not tied to one recorded speaker. Whether any single Kokoro voice resembles a specific real person is not stated in the sources read.
  - *Piper voices:* the engine is GPL-3. Each voice is trained from its own dataset, often one recorded person, with a licence chain to audit (piper-tts.md).
  - *StyleTTS 2 LJSpeech checkpoint:* one real person's public-domain audiobook recordings, under the authors' conditions of use.
  - *Cloning (F5-TTS, XTTS, VoxCPM2, StyleTTS 2 LibriTTS, Chatterbox):* needs a recording of a real person. That raises consent (FastSpeech 2's and StyleTTS 2's authors both require it), and the weights are often non-commercial (F5-TTS CC-BY-NC) or under a model licence I did not read (XTTS). His own voice would make the agent sound like him: copying at the level of identity, which the morise note already excludes by design. It would also need a stored clip or embedding of his voice, whereas the memory stores only features (Principle 7).
- **Data off the Mac:** none at run time for any option here. Kokoro needs one download from Hugging Face, covered by Q34 item 4 (model downloads), then a SHA-256 entry in `models.lock` (A17). macOS voices need none.
- **Latency (to be measured, not decided here):** the spec budgets 0.15 s (p50) and 0.3 s (p90) for TTS and WORLD on the first phrase (§1.8). No measurement so far meets it:
  - kokoro-js q8 on this Mac's CPU took 2.5–2.9 s for a 4.5-s sentence (RTF 0.55–0.65; kokoro-82m.md), so a 1-s first phrase would take about 0.6 s on CPU;
  - macOS `say` took 1.42 s per sentence including process start (macos-speech-synthesis.md); in-process AVSpeechSynthesizer was not timed;
  - Python Kokoro on MPS was not timed.

  The budget is an M5 measurement for whichever voice is picked. It may force first-phrase chunking, and it is the main reason to keep a macOS voice as the fallback.

## 4. Draft options for Q1 (one line each)

1. **A Kokoro voice (you choose one of its fixed voices by listening, or a blend of two), through the WORLD stage already built:** Apache-2.0, fully local after one download, a more natural timbre than most macOS voices, every voice setting under its own limit exactly; speed on your Mac is measured at M5.
2. **A macOS voice (you choose an installed voice), through the same WORLD stage:** works today with nothing to download, fully local, same exact limits; the timbre is that voice's (the compact voices sound robotic), and the macOS terms for this use were not checked.
3. **Option 1, plus the engine writing Kokoro's internal pitch, loudness and duration curves (checked after rendering as before):** likely the most natural intonation under the same limits; needs a small code change and a test at M5; same voice, so it can be tried later without asking you again.
4. **A Piper voice through the WORLD stage:** works and is local; GPL-3 engine (fine for use on your Mac), but each voice's licence chain must be checked, many voices are one recorded person, and it offers nothing over option 1.
5. **A cloned voice of a real person (anyone, including you):** not recommended. It needs that person's consent and a recording; the open cloning models are non-commercial or controlled by emotion words; and your own voice would make the agent copy you at the level of who it sounds like.
6. **Wait:** speech stays off; nothing else is blocked.

**Recommendation: option 1, with option 3 as a later upgrade and option 2 as the fallback.** Reasons: it is the plan already built (spec §1.7, with Kokoro as Plan A instead of Piper); its licence is the cleanest of the natural-sounding options; it is a fixed synthetic voice, so no real person's voice is copied; every one of the six settings keeps its own limit by construction; and the same model allows the more natural route of option 3 without changing the voice. If Kokoro cannot meet the first-phrase latency on his Mac at M5, option 2 needs no download and works today.

**Spec consequences if he picks 1 (for the main session; not edited here):**
- §1.7 Plan A becomes Kokoro-82M (fixed voice tensor, `speed = 1`), with Piper dropped from Plan A;
- the innate templates stay, and the TTS's own predicted contour is never used for the six channels;
- A17 lists the voice tensor;
- under option 3, A9 becomes a correction step (measure, rescale, re-check) and gains a crosstalk check: with only y_FR changed, EN stays within ±1 %, and the same for each pair of channels.

## 5. Novelty verdict
**None. This is a component choice, not a core.** WORLD resynthesis, explicit variance inputs and learned style latents are all existing methods, and the per-channel condition of §1 is ordinary bookkeeping of gains (the same per-channel accounting as new-core-search-10-synthesis.md, applied to a memoryless renderer). What this pass adds is three applications to this engine: the renderer condition, Kokoro's internal curves as a local form of design (b), and naming the words-to-voice route that a TTS's text-conditioned prosody would open. No designs.md line.

## 6. What remains open
- **Latency** of each candidate on his Mac: Python Kokoro on CPU and MPS, in-process AVSpeechSynthesizer, and the first-phrase chunking (M5).
- **Perceptual quality** of WORLD's manipulations on Kokoro and macOS output at ±c_k (untested since morise-2016), and a listening test by the operator of the candidate voices, which is how he answers Q1.
- **Option 3's fidelity:** whether Kokoro's decoder follows edited F0 and energy curves (α_k) and how far pitch edits move loudness (β_kj); measured with the §1.2.4 functions on rendered audio.
- **Provenance:** Kokoro's voice provenance and training data were not re-read (Hugging Face unreachable here); nor were the macOS licence terms for generated speech, or the Coqui Public Model License.
- **WordVoice and MAGIC-TTS** were read as abstracts only; if either has open weights with continuous controls, it is another form of design (b) to check.
- **The vocal analogue of S5:** whether the operator's voice comes to follow the agent's (voice-synthesis.md, open problems). That is untouched by the choice of voice, but it is easier to measure with a voice whose six settings are known exactly, which favours (a) and (b).
