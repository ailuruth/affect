# Critique: Cayley–ledger core (design-cayley-ledger.md): routes, the cone end to end, the ledger, learning, and human-like behaviour

Independent critic, 2026-11-26T05:38:50Z. I did not write the design. Written under questions.md Q19 and DECISIONS.md D80: proof gaps are not reported. Only concrete failure mechanisms are, each with a scenario and, where possible, a numeric check. The checks are judged against D78 (the refined dial rule), brief.md Principles 1–10 and C1–C10 (non-copying-dynamics-synthesis.md). Nothing was downloaded.

The checks are in `research/foundations/sims/critique-cayley-routes/`. Each script is listed below. The output of all of them is in `out.txt`, and all run with `python3 -I <script>` in a few seconds.

| Script | Check |
|---|---|
| `speech_rate_leak.py` | K1 |
| `held_level_modulation.py` | K2 |
| `fibre_learnability.py` | K3 |
| `mirror_lateral.py` | K4 |
| `loud_event_snr.py` | K5 |
| `g9_seeds.py` | K6 |

The checks use the design's own constants (σ_s = 7.1, h_s, κ = 0.3, γ = 0.5). They test the design's own claims on constructed inputs, and are not evidence about people (brief: no toy worlds). Where a check depends on a property of the partner or of a frozen component (ASR, MediaPipe), that property is stated as an assumption, to be measured once built.

## Summary verdict

Five concrete failures, ranked by severity. None is a proof gap.

1. **The slow mind and the learned fibre are blind to the partner's face and voice (K3, K5). Severe; this is the human-likeness failure.**
   - The release noise that makes the ledger work leaves almost nothing to learn from:
     - per-sample reliability is 1.35·10⁻⁴;
     - a full-range shout lasting 1 s has a matched-filter SNR of 0.16;
     - an hour-long held sad face and voice is told apart from neutral with at best 57% balanced accuracy.
   - The fibre's context- and relationship-dependent signs are trained only on that stream. They are learned at **0.0002** where the target is ±0.5, a 2500-fold attenuation that more data does not reduce.
   - So in practice:
     - the fast face is the innate positive echo in every context;
     - the agent's state is not moved by the partner's expression;
     - arousal does not respond to a raised voice.
   - This fails four things:
     - Principle 3 (there is nothing to invert);
     - the brief's long-term goal ("each side's expression moves the other's state");
     - C4 and C5 on the face (the sign cannot be learned to flip by role or episode);
     - in practice, D78's "set by context and learned relationship".
   - The design names this as its weak point 1. Under the task's item 6 it is a concrete failure, and its size is larger than the design states: the learned fibre is inert, not merely weakly trained.
2. **Speech rate leaks through the noise-free turn times (K1). Severe for Claim L.**
   - The neighbouring relation offsets speech rate (a released voice channel) while declaring turn times identical. No physical speaker can produce that pair: a slower held rate makes every turn longer.
   - From Q alone, the mind's estimate of a held speech rate correlates with it at:
     - **0.74** over 20 turns from durations alone;
     - **0.93–0.98** when utterance length is known;
     - against the ledger's bound of 0.25.
   - The full-range neighbouring pair is detected with **0.97** accuracy, against a promised ≤ 0.567.
   - The route Q → μ / slots → Π_ψ → own speech rate is not in the route table. Its only cap is A_k = 0.8, with a free sign. That is a near-copy strength that is neither named nor bounded under D78.
3. **A held level costs privacy in proportion to its duration once the partner's signal is not a pure additive offset (K2). High.**
   - **Speech modulation.** Suppose articulation lowers a held smile's measured value by a fraction β while the partner talks, and the mind knows exactly when the partner talks (from Q). Then the realised ε(2) grows from 0.116 to:
     - **1.7** over 1 h at β = 0.3;
     - **5.0** over 3 h;
     - which gives a matched-filter correlation of 0.35–0.54 with the held level.
   - **Dropouts and session starts.** Face-tracking dropouts or session starts that reset to rest add one edge pair each: an hour with a dropout every 3 min reaches ε(2) = 2.3 (78% accuracy).
   - **The design's learning does this.** 𝓜's predictive-likelihood objective is exactly the matched filter that exploits this. So "no build-up" fails for realistic partners.
4. **Mirror copy on the lateral channels (K4). Medium.**
   - The one-sided sector caps the same-sign (anatomical) direction. On head yaw, head roll and horizontal gaze, the sign-flipped side it frees up to 0.60 *is* mirror imitation, which an observer sees as following.
   - With the wrap of S = −γ·(high-pass, one-frame delay), the regression gain on the mirrored partner is **0.58**. That is three times the "every direction ≤ 0.20" claim. It holds for every θ, including the innate gaze-following reflex if that reflex is implemented in world coordinates.
5. **Non-lexical ASR output carries nonverbal expression into Q and Claude, without noise and uncounted. Medium; no numeric check, since ASR is frozen and was not run.**
   - The carriers are laughter tokens ("haha"), exclamation marks and question marks driven by intonation, and fillers.
   - In this scenario the partner laughs and then:
     - the agent smiles at up to 0.8 on the smile channels within 1–2 s, through own appraisal (R14);
     - Claude laughs back in text, which the TTS speaks.
   - A partner who stays excited all evening (held high F0 and energy) produces "!"-heavy transcripts. Claude mirrors the enthusiasm, which raises the agent's held vocal register by up to P_txt + A_k, with no ledger.
   - The design's proposed ASR test counts word changes only, so it would not catch this.

**Areas with no concrete failure found:**
- **The Cayley cone end to end (item 2).** I found no series path that puts a second sign flip after the wrap. Two checks came out clean:
  - c (the fibre's context) depends on the partner only through X^s and Q, and nothing reads y^F back;
  - the voice wrap is separate from the face wrap.

  The only end-to-end breaches are the ones listed above: K4 (handedness), and the Q routes of K1 and failure 5.
- **Noise averaged away by replay or nightly learning (item 3).** Replay stores the already-noised X^s, so re-reading it averages nothing. No jitter on the agent's face: the mind's learned weights on X^s are driven to near zero. That is the other face of failure 1.
- **The cap becoming attracting through a partner echo (item 4).** The partner-driven gradient on φ_k is attenuated by about 10⁻⁴, so the pull holds φ at φ₀. A side note follows in §6.
- **Persistence (item 5).** μ and the slots are linear and have no wells, tilt or event port. The only leaks into them are K1, K2 and failure 5.
- **C1 (K6).** G9's "fast band below surrogate" is systematic: it holds in 40 of 40 seeds with the gate, against 45% without it. The Welch-estimator mechanism (anti-correlated power envelopes) is real.

---

## 1. Failure 1: the slow mind and the learned fibre are blind to the partner (K3, K5)

### Scenario A: the partner's sad face
- **The partner.** He sits down, visibly sad (brows raised at the inner corners, lip corners down, low voice energy), and holds it for an hour. He talks about neutral things (plans for the weekend).
- **The agent's face.**
  - The fibre echoes only the edges: a 0.16-scaled flicker on brow-inner-raise at the onset. It decays to 3·10⁻⁴ within 50 s (G10).
  - The ledger gives the mind an episode-level signal with GDP μ = 0.34. The best possible test tells "sad for an hour" from "neutral" with **56.8%** balanced accuracy, and detects it at a 5% false-alarm rate with probability **0.096** (K5).
  - μ, the slots, b and draft choice cannot differ by more than 0.35 sd.
- **What the agent does.** It says and shows nothing about the partner's state, for the whole hour. A person would show concern within seconds and keep it.

### Scenario B: a shout
- **The partner.** He shouts for 1 s.
- **What reaches the mind.** The audio-energy coordinate of X^s carries it with matched-filter SNR **0.16** (K5). The prediction-error magnitude that drives the arousal load A is 857 per release from noise alone. A full-range edge adds 0.09% to it.
- **What the agent does.**
  - Only the startle blink (the a-route) responds.
  - Arousal, aversive load and appraisal do not.
  - The arousal readout is the same whether the partner shouts or whispers.

### Scenario C: an argument
- **The context.** It is an argument, and context c (from words) says the stance is opposed.
- **The intent.** The fibre is meant to learn to flip its smile response (C4/C5; D78 "set by context and learned relationship, can flip sign").
- **What it learns.** Its only training input is X^s, since replay never stores u (§2.9). K3 gives it the most favourable case possible:
  - the own display truly follows partner smile transients at +0.5 in friendly and −0.5 in opposed contexts;
  - 240 h of data;
  - the best linear 4-s causal filter per context.

  It learns run-time gains of **+0.0002** and **−0.0002**. Trained on clean u, the same learner would get +0.500 and −0.501.
- **Why.** The attenuation is errors-in-variables (reliability var(signal)/(var + σ²) = 1.35·10⁻⁴). It does not shrink with more data.
- **The innate pull.** The equilibrium shift of φ is about 10⁻⁴, so φ stays at φ₀.
- **The result.** The agent's fast face echoes the partner's (sarcastic, contemptuous) smile at the innate gain 0.16 in the argument, exactly as with a friend. Net face coupling on the echo channels is positive in every episode, so C5's "below chance in opposed episodes" cannot occur on the face.
- **What still works.** The words still reach y^own within 1–2 s (R14). So the agent can frown at what is *said*, but not at a face.

### What this violates
- **Principle 3.** "The agent infers another's state by inverting its own generative mapping": R is there, but what passes through R reaches the inferring parts at SNR 0.27 per episode.
- **The brief's long-term goal.** Its first bullet: "largely unconscious emotional exchange through faces and voices, where each side's expression moves the other's state".
- **C4 and C5 on the face.**
- **D78.** Its "per expression, set by context and learned relationship" is met only by the capacity of the parameterisation, not by anything the design's learning can reach.

### Fix
- The ledger's protection is set for the *slow* side, but the fibre's *training* inherits it. Train the fibre inside 𝓑, from clean u, against its own target:
  - an online or short-buffer learner inside the boundary;
  - a training buffer that is never exported and is erased within a bounded time;
  - weights that are themselves outputs of 𝓑.
- **Price.** The fibre's weights then become a partner-dependent persistent state. They need their own bound:
  - the wrap bounds what any θ can do;
  - the φ ball bounds the gain;
  - but the weights could encode held levels. So the weights, or a summary of them, must be released to the slow side only through the ledger, or not at all.
- **For the slow side's blindness.** The only lever is ε_L. The design names it (ε_L(2) = 0.5 gives per-episode SNR 0.56). Even that leaves a shout or a sad hour near chance.
- **A structural alternative.** Release *events* (onsets of a channel above a size threshold), not filtered levels, with their own neighbouring relation. Onset counts are not held levels, so they may be priced more cheaply. That is a design change, not a constant.

## 2. Failure 2: speech rate and timing leak through turn times (K1)

### Scenario
- **The partner.** Tired, he speaks slowly all evening: a held speech-rate offset on voice channel 4.
- **What Q releases.** Turn start and end times on a 100-ms grid, with no noise, plus each utterance's text and embedding. Turn duration equals syllables / rate + pauses. Speech rate is therefore in Q whatever the ledger does to R_V ū.

### Evidence (K1)
- The model:
  - rate level r ∈ [0,1] maps to 3–6 syllables per second;
  - utterance length is lognormal (median 20 syllables, sd(log) 0.8), independent of rate;
  - within-turn pauses follow Beta(2, 8).
- Results:

  | Estimator | 1 turn | 5 turns | 20 turns |
  |---|---|---|---|
  | duration only: corr with held rate | 0.27 | 0.46 | 0.74 |
  | duration and length (length from the embedding or the stored transcript): corr | 0.76 | 0.93 | 0.98 |
  | full-range neighbouring pair, duration only: balanced accuracy | – | 0.834 | **0.970** |

  Ledger bounds: correlation ≤ 0.25; accuracy ≤ 0.567.

### Where it goes
- Q feeds the mind, which feeds μ (2 min–73 h), the slots and Π_ψ. Π_ψ drives the agent's own phrase prosody, including speech rate, at up to A_k = 0.8 of range, with a sign learned freely.
- The route is not in §3.6. Its cap of 0.8 is not a copy cap, so under D78 it is an unnamed per-channel strength near copy.
- **The same route carries partner response latency and pause length.** Their slow, held changes are among the voice cues to low mood, so a single "tempo" coordinate in μ can also set the agent's whole-face mood through Π_ψ.
  - I did not find a learning pressure in the design that would make this attracting. But nothing bounds it either.

### Fix
- Make turn times a function of words, or of noise, only:
  - release turn boundaries to the mind on a coarse grid (for example, a turn-index count and nothing finer);
  - or add ledger noise to durations, and include speech rate, pauses and latencies in the nonverbal neighbouring relation, accounting for them in the same ε_L.
- Floor-taking can stay inside 𝓑 (the floor flag already does).
- Strip length from the embedding passed to the mind, or accept the leak and bound the route by naming it: an innate per-channel cap on the slow path into own speech rate.

## 3. Failure 3: duration-proportional cost for real held expressions (K2)

### Scenario (a): speech modulation
- **The partner.** He holds a smile for the evening while talking.
- **What the measurement does.** Talking moves the lip corners and cheeks, so the measured lip-corner-pull of the held smile drops by a fraction β whenever he speaks. The partner's signal is then x_t = ℓ(1 − β s_t), not ℓ·1_W.
- **Why the zero-DC filter does not remove it.** The difference between ℓ = 1 and ℓ = 0 contains β·s_t throughout the window. That term is a turn-rate square wave, and the filter passes it.
- **What the mind can do with it.** It knows s_t exactly from Q's turn times, so it can correlate X^s with h_s ∗ s_t.

Evidence (K2a): the design's exact filter and noise, with turns of about 7 s.

| β | hold | ε(2) | GDP μ | best accuracy | matched-filter corr(ℓ) |
|---|---|---|---|---|---|
| 0.1 | 3 h | 0.63 | 0.80 | 0.655 | 0.22 |
| 0.3 | 1 h | **1.72** | 1.31 | 0.744 | 0.35 (Monte Carlo without the edges: 0.25) |
| 0.3 | 3 h | **5.01** | 2.24 | 0.868 | 0.54 |

The design promises ε(2) = 0.116, accuracy ≤ 0.567 and correlation ≤ 0.25 for every duration.

- β is an assumption about MediaPipe under articulation, to be measured. Any β > 0 makes the cost linear in time.
- The same holds for any partner signal whose deviation scales with the held level and coincides with something the mind knows:
  - the partner's responses to the agent's own probes (own variables are known exactly), which are clipped near the ceiling when the held level is high;
  - the bias of expression estimates with head pose.

### Scenario (b): dropouts and session starts
- **The trigger.** The partner turns away or puts a hand to his mouth, and MediaPipe loses the face.
- **What happens if u is reset to rest.** If u then falls to rest (or the release filter restarts at zero at the session start), every reacquisition is a new edge pair.
- **The cost.** k such events cost k·0.116:

  | Case | ε(2) | Best accuracy |
  |---|---|---|
  | a dropout every 3 min for 1 h | 2.3 | 0.777 |
  | 30 sessions of a chronically sad face | 3.5 | 0.825 |
  | 30 sessions with dropouts | 70 | ≈ 1.0 |

- **What the design leaves unspecified.** It states neither sample-and-hold on dropout nor filter-state initialisation at session start.

### The design's own learning finds this
𝓜 is trained by predictive likelihood of the next X^s given Q events and own variables. The part of X^s that is predictable from turn times has amplitude βℓ. Predicting it requires carrying an estimate of ℓ across the evening. A trained 𝓜 is therefore a held-level tracker to whatever extent the data allow, and K2 shows that this extent grows with time.

### Fix
- **(b) is easy:**
  - sample-and-hold the last valid frame on dropout;
  - initialise h_s's state from the first frame of each session (no step);
  - release nothing during a dropout.
- **(a) needs two things inside 𝓑:**
  - **Articulation compensation.** Regress the speech-driven component of each counterpart channel out against the partner's own audio, before R. That reduces β.
  - **An honest statement.** Admit a per-hour accrual (for example, a ledger with exponential forgetting, so the cost is per recent window), or widen the neighbouring relation to multiplicative offsets ℓ·g_t, with g_t any Q-known modulation of bounded size, and price those.

  "No build-up for every duration" holds only for exactly additive partners.

## 4. Failure 4: mirror copy on lateral channels (K4)

### Scenario
- **The partner.** He tilts his head to his left shoulder and looks to his left.
- **The agent.** At 0.1–0.5 s, it tilts to *its* right shoulder and looks to its right: mirror imitation, at gain 0.58.
- **Why the design allows it.** Its coordinates are "the same map for partner and agent". In them this is a sign-flipped response, which the sector allows down to −0.60. An observer facing the agent sees it follow.

### Evidence (K4)
- The setup:
  - partner yaw at 0.2–1.1 Hz;
  - the exact wrap with S = −γ·(innate high-pass, one-frame delay);
  - regression of agent yaw on the partner's yaw, at the best lag in 0–1 s.
- Results:
  - anatomical (+u): +0.30;
  - mirror (−u): **+0.58**.
- The claim in §3.1 is "≤ 0.20 in every direction". Three channels can carry about 3× that, for every θ, and the innate gaze-following reflex can sit there if it is built in world coordinates.
- Under D78 this is per channel, and still below 1. But it is the copy direction that the design labels "free sign flip", so the totals in §3.6 understate copying on head roll, head yaw and horizontal gaze.

### Fix
On signed lateral channels, either:
- replace the one-sided sector with a symmetric disc |H| ≤ 0.20 (centre 0), giving up "free" flips there, which have no expressive meaning on yaw anyway; or
- re-express them as unsigned magnitude (turning or tilting away) plus a side bit that the fibre cannot drive.

## 5. Failure 5: non-lexical ASR output (scenario only)

### Scenario
- **The partner laughs.** Whisper writes "Haha" or "(laughs)", and Q carries it with no noise.
- **The agent's face.** The mind's appraisal of the token drives the smile subspace (lip-corner pull, cheek raise) through Π_ψ, at up to 0.8, within 1–2 s.
- **The agent's voice.** Claude, which mirrors register strongly, writes "Haha, …". The TTS speaks a laugh. The echo guard passes it: a "haha" in a 15-trigram reply is an overlap well under 0.3.
- **A held register.** A partner who is excited all evening (held high F0 and energy) yields "!"-heavy transcripts. Claude replies with exclamations, so the text-driven prosody (P_txt = 0.15) and the appraisal (A_k) raise the agent's own held register.
- **What this is.** The partner's *expression*, not a shared referent, encoded in text. The copy test of §3.6 holds the transcript fixed, so it is blind to it by construction.
- **Caveats.**
  - Laughing back is human. The failure is not that it happens: it is uncounted, its cap is 0.8, and it bypasses the ledger that is meant to cover voice.
  - I did not run Whisper. How often these tokens occur is the thing to measure.

### Fix
- Normalise the ASR output before Q: lower-case, lexical words only, no laughter, filler or sound tags. Restore punctuation with a text-only model, so that "?" is a function of the words.
- Route laughter, sighs and crying through 𝓑 as nonverbal events under the ledger. Laughter as an a-feature gets its own Lipschitz cap.
- Extend assumption 1's test to punctuation and non-lexical tokens.

## 6. Areas checked with no concrete failure

- **Item 1 (the boundary), other routes checked:**
  - draft selection and retrieval: post-processing of X^s and Q;
  - replay and the episodic store: X^s, never u;
  - identity: one token per session;
  - floor flag: inside 𝓑, memoryless;
  - visemes: articulators, which the partner's u does not contain;
  - startle: ℓ_a.

  The leaks found are all in Q's unnoised content (K1, failure 5) and in the neighbouring relation's additivity (K2).
- **Item 2 (the cone end to end):**
  - y^own does not depend on u except through the ledger and Q;
  - nothing reads y^F;
  - c has unbounded influence on the fibre's *w-independent* output, but c is ledger- and Q-bounded.

  No second flip after the wrap was found, apart from K4's handedness.
- **Item 3 (averaging):**
  - replay re-reads the same noise sample;
  - learning cannot average it away beyond the k-episode composition the design already admits;
  - jitter: the mind's weights on X^s are driven to near zero by the same attenuation as K3, so the noise does not show on the face; the information does not get through either.

  The across-session accrual is K2(b).
- **Item 4 (learning):**
  - G7's ball holds;
  - the partner-driven gradient on φ is about 10⁻⁴ (K3), so no partner echo pushes the gain to the cap.
  - Side note, not a failure: the fibre's output includes a c-driven part that is independent of w and multiplied by the same γ_k. Its gradient against the own-display target is not attenuated, so it can push φ_k to the ball edge (γ_k ≈ 0.476), lifting the partner in-phase gain from 0.161 to 0.194 in every context, for a reason unrelated to the partner. This is still below the 0.20 cap.
  - Fix if wanted: give the c-only path its own gain, separate from γ_k.
- **Item 5 (persistence).** Linear modes have no wells, so there is no noise-driven switching or tilt. A held-level offset enters them only through K1, K2 or failure 5.
- **Item 6 (timing):**
  - the fast match arrives at 0.45 s + 80 ms ≈ 0.53 s, which fits;
  - word-driven appraisal reaches the face in 1–2 s, which fits for words;
  - C1 holds over seeds (K6: real < surrogate in 40/40 seeds with the gate, 18/40 without);
  - C4, C5 and face-driven sign flips fail (failure 1);
  - partner history within minutes is available from words and from many-episode statistics only, about SNR 1.2 after 20 smiles in 5 min (as the design states);
  - C7's "joint pattern" cannot see the partner half on the face, because the partner half is in X^s at reliability 10⁻⁴. The drive I is lowered only by own-body learning progress, so the anti-repetition it produces is anti-repetition of the self, not of the dyad. That is weaker than C7 asks; the design marks it untested.

## 7. Sources read for this critique

| Source | How read |
|---|---|
| research/foundations/design-cayley-ledger.md | in full |
| research/foundations/sims/design-g/checks.py, out.txt | out.txt in full; checks.py G5 and G9 in full, the rest skimmed |
| brief.md | in full |
| research/questions.md | Q18 with answer; Q19 |
| DECISIONS.md | D78, D80 |
| research/non-copying-dynamics-synthesis.md | in full |
| critique-design-fibred-attribution-core-proofs.md, critique-design-fibred-attribution-core-novelty.md | summaries, for the recurring failure patterns |
| Whisper, MediaPipe behaviour under laughter, articulation and dropouts | **not measured.** Failures 3(a) and 5 state these as assumptions to measure |
