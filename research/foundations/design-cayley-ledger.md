# Cayley–ledger core, revision 2: one wrapped mind that may know the partner but cannot move toward them

Seventh design of the S0 cycle, revision 2. Written 2026-11-26 under questions.md Q16, Q17 as relaxed by Q19 (precise object, convincing arguments, concrete failures only), Q18 and its answer (DECISIONS.md D78, D80), and Q20 on its recommended reading: the inner state may know the partner's face and voice as closely as perception allows; every path from inner state to the agent's own expression is bounded against copying by construction. Revision 1 is kept as `design-cayley-ledger.r1.md`, with its two critiques and the answer. Algebra checks for this revision: `foundations/sims/design-g2/checks.py` (H1–H8, `python3 -I checks.py`, numpy and scipy, about 30 s; output in `out.txt`). They check this design's own inequalities on constructed instances and are not evidence about behaviour or people (brief: no toy worlds).

**Status:** revision 2, not yet critiqued.

## 0. Summary

**What changed from revision 1, in one line.** Revision 1 stopped copying by hiding the partner from the slow mind behind heavy noise, which also stopped care. Revision 2 removes the noise. It moves the whole expressive mind, moods, body, relationship memory and display policy included, *inside* the Cayley wrap, so it can know the partner's face and voice in full while every path from it to the agent's face and voice stays in a one-sided cone. The ledger survives only as a name: what replaces it is one zero-DC port for the one route a cone cannot contain, the agent's own chosen words.

- **Core object.** One boundary module 𝓑 reads camera, microphone and ASR. Everything the agent shows on its counterpart channels (32 channels: face, gaze, articulators, voice levels, turn timing, non-lexical vocal bursts) is

  y = 2K^{1/2}s,  w = K^{1/2}P u − s,  s = H_o S_f(H_i w) + S_s(L w) + P_Ω(e),

  with P a fixed reflection of the lateral channels, K = diag(κ) innate weights, and three blocks:
  1. **S_f, the fast block:** a strictly causal γ_f-contraction (a robust REN) between an innate 4-s high-pass H_i on its input and an innate 4-s high-pass H_o on its output. Reflexes, fast context-set mimicry and counter-mimicry live here.
  2. **S_s, the slow block:** a strictly causal contraction with gain γ_s in *both* ℓ₂ and ℓ∞, reading the partner only through an innate 60-s low-pass L. The agent's slow body, concern, mood ladder (2 min to 73 h), relationship slots (30 days) and display policy live here. It knows the partner's held face: its 1-min knowledge tracks the held level at r = 0.994 (H2a).
  3. **P_Ω, the port:** the only entry for Ω, the discrete layer (Claude's drafts, draft choice, retrieval, concepts). It is Lipschitz-capped at a_Ω = 0.10 per channel and high-passed at its *output* (τ_Ω = 15 s), so it has exactly zero DC.
- **What is bounded, for every parameter value (per channel unless stated; 1 = full copy):**

  | Quantity | Bound | Where it comes from |
  |---|---|---|
  | zero-lag in-phase gain, any band, any partner direction | ≤ 0.198 | the wrap of S, γ_eff = √(γ_f² + γ_s²) = 0.492 |
  | held level (DC), in phase | ≤ 0.100 | the wrap of S_s alone (DC passes only through L) |
  | held level, any direction (care, counter-display) | ≥ −0.150 | same |
  | any 1-min mean during a hold, any time after onset | ≤ 0.15 + port 0.05 + edges 0.01 | ℓ∞ bound on S_s (H7) |
  | 10-min means | ≤ 0.10 + 0.005 | port is zero-DC |
  | lateral channels (head yaw, roll, horizontal gaze), both handednesses | mirror ≤ 0.031, anatomical ≤ 0.082 | reflection P, κ_lat = 0.05 (H4) |
  | fast, any signal, any direction | ≥ −0.491 | fast disc |
- **Knowing is separated from moving.** A slow state that knows the partner's held face at r = 0.994, read out by a copy-seeking policy, moves the agent's 1-min means by 0.092 of the partner's level (H2b). Read straight to the face, the same knowledge copies at 0.906. Held copying is impossible through slow paths because DC reaches the face only through the wrap of S_s, and the wrap's DC gain is 2κσ/(1 + σ) ≤ 0.10 for every σ ∈ [−γ_s, γ_s] (§3.2).
- **It is an emotional agent now (§3.11).**
  - Body variables respond to what is said and done: the partner's words and face move the agent's concern C and aversive load V through its own body (P3), and its arousal and energy follow events.
  - Care for a silently sad partner arises from the agent's own drive evaluated at the partner's inferred body, 𝒟(b̂_p), relieved only by the agent's own acts as it would itself be relieved ("comfort as I would be comforted"). The planner's partner model is action-blind, so no term rewards changing the partner. The placation incentive of revision 1 is gone.
  - The display policy minimises the same objective J.
  - Emotion concepts are categories of the world model over interoceptive and exteroceptive states, named by Claude only through which raw past dialogue it is shown.
- **The fast block learns from clean signals.** Replay stores the partner's feature streams. A two-tap context-gated learner reaches +0.135 (target +0.15) in a friendly context and −0.238 (target −0.40, bound −0.33) in an opposed one; a copy target saturates inside the cone (H3). Revision 1's noised release gave +0.0002.
- **New weakest point (§8.1).** After the first few seconds of a change, the partner's face and voice can move the agent's face and voice by at most 0.15 of range in any direction, and the 4 s – 1 min band is nearly blind on the expressive side. Strong sustained displays come only from words and the agent's own body. Whether that reads as warm or detached is untested.
- **Novelty verdict (author):** recombination. Three composition results are new to this project (§10): the banded wrap with an ℓ∞ slow block and its no-demodulation rule; the necessity of a port for discrete routes (N4); the empathic drive under an action-blind partner model.

## 1. Plain-language intuition

The agent still has one door. Behind it, now, the whole house can see the partner clearly: it knows that he has looked sad since ten o'clock, that he laughed twice, that he speaks slowly tonight.

What changed is how the house is allowed to *move the agent's own face and voice*. All of that movement leaves through one gearbox at the door, the wrap. The gearbox has two gears:
- a quick gear for the first seconds after the partner changes (a smile back, a flinch, a nod at a pause), which can push back hard but follows him only a little;
- a slow gear for everything held (moods, worry, the relationship), which can push back a little and follow even less.

However the house has learned, and however well it knows him, the gearbox caps how far the agent's face can drift toward the partner's: a fifth of his movement in the first seconds, a tenth for anything he holds.

Claude stands at a separate window. It knows what the house knows and chooses what the agent says. Its words cannot be put through the gearbox, because a choice between sentences jumps. So they reach the agent's face through a small side door that lets through only brief, small changes, and nothing that lasts.

Care is the agent's own discomfort at the state it reads in him through its own body, eased only by what it does for him in the way it would itself want to be treated. Nothing in it pays the agent for changing his face.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz (Δ = 1/30 s) except where stated. Every channel is normalised so that its innate nominal range is [0, 1] (signed channels: [−1, 1]).

**Counterpart channels (n = 32; the copy metric is defined on these).** The innate correspondence P₀ (fixed: left/right averaging and grouping of MediaPipe's 52 blendshapes, head pose and gaze) gives:

| Group | Channels | n | κ |
|---|---|---|---|
| symmetric face | brow inner raise, brow outer raise, brow lower, upper-lid raise, lid tighten, cheek raise, nose wrinkle, lip-corner pull, lip-corner depress, lip stretch, chin raise, lip press, dimpler, head pitch; vertical gaze | 15 | 0.30 |
| lateral | head yaw, head roll, horizontal gaze; **reflected** by P (sign flipped) before the wrap | 3 | 0.05 |
| articulators | jaw open, lip funnel, pucker, mouth close, lip roll | 5 | 0.30 |
| voice and timing (phrase or turn level, zero-order held at 30 Hz) | F0 level, F0 range, energy, speech rate, within-turn pause, response latency | 6 | 0.30 |
| non-lexical vocal bursts (continuous, no labels) | non-lexical voiced energy (voiced audio not aligned to an ASR word), 4–6 Hz burst-rhythm energy, breathiness | 3 | 0.30 |

**Exogenous partner inputs (not counterpart; enter S, not fed back):** a ∈ [0,1]³: audio onset envelope, partner voice activity (VAD), partner turn-end pulse. Input weight κ_a = 0.05.

**Non-counterpart outputs:** blink (1), driven outside the wrap by the innate startle reflex and own noise (route R7).

**Innate constants (compiled in, not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| κ, κ_lat, κ_a | 0.30, 0.05, 0.05 | wrap weights; lateral; exogenous inputs |
| γ | 0.50 | overall contraction bound of S |
| γ_f, γ_s | 0.45, 0.20 | fast and slow block gains; √(γ_f² + γ_s²) = 0.492 ≤ γ |
| fast disc (κ = 0.3) | in-phase ≤ 0.186, anti ≥ −0.491, centre −0.152, radius 0.339 | wrap of a 0.45-contraction |
| slow disc (κ = 0.3) | in-phase ≤ 0.100, anti ≥ −0.150, centre −0.025, radius 0.125 | wrap of a 0.20-contraction |
| ℓ∞ cap of the slow block | 2κγ_s/(1 − γ_s) = 0.150 | pointwise in time (§3.3) |
| H_i, H_o | first-order high-pass, τ = 4 s, at the input and the output of S_f | fast block sees and makes no DC |
| L | first-order low-pass, τ_L = 60 s, at the input of S_s | slow block sees only slow content; |H_i|² + |L|² ≤ 1 (H1a) |
| filter bank inside S_f | band-passes centred 0.15, 0.4, 1.0, 2.5, 4.5 Hz, each scaled 1/√5; lag line 0.15, 0.3, 0.45, 0.6, 0.8 s | time-scale coordinates of the fast block |
| ℓ_echo | 0.45 s | lag of the innate echo |
| M(s) | ω_n = 2π·4 rad/s, ζ = 0.8, peak gain 1, inside both blocks | muscle filter |
| P_Ω | Lipschitz cap a_Ω = 0.10 per output channel; output high-pass τ_Ω = 15 s | the port |
| P_txt | 0.15 | amplitude of the normalised (zero-mean) text-driven pitch and energy contour within a phrase |
| V_A | 0.8 | viseme amplitude cap on articulators |
| ω_max | 0.30 | echo guard: maximum phoneme-trigram overlap of a draft with the partner's last two utterances |
| ℓ_blink | 0.6 | startle reflex: audio onset → blink |
| body set points b*, dead-bands δ, weights w | E (0.7, 0.2, 1.0); A (0.3, 0.15, 0.7); V (0, 0.05, 1.0); C (0, 0.05, 0.8); H (0, 0.1, 0.4); I (0, 0.1, 0.5) | drive 𝒟 |
| body time constants | E: −0.5 %/min awake, +2 %/min at rest; A 3 min; V 10 min; C 10 min; H 2 min | innate dynamics |
| mood ladder | 8 groups × 16 coordinates, τ_j = 2 min·3^j (2, 6, 18, 54 min; 2.7, 8.1, 24, 73 h) | positive leaky modes |
| slots | 128 slots, key 64, value 64, τ_slot = 30 days | relationship and episode memory |
| K_d, T_d | 6 drafts; selection temperature 0.1 | draft choice |
| scoring horizon | 30 s of 𝓜 rollout at 2 Hz | draft score |
| retrieval | ≤ 3 snippets; ALiBi slope 1/(7 days) | Claude context |
| concepts | DP-means threshold λ_DP = 1.5 (in units of the slow summary's sd), ≤ 64 categories; PMI window ±1 turn; retrieval bonus β = 1.0 | grounding |
| replay | gradient clip G = 1; pull to θ₀: λ = 0.5 (S_f), 0.1 (S_s); nightly consolidation λ_n = 0.01 | learning stop |
| floor | may start ≥ 200 ms after partner VAD offset; latency = 0.4 s + 1.0 s × latency output | turn-taking |

### 2.2 The boundary 𝓑 and the structural checks

𝓑 is the only code that imports camera frames, microphone audio, ASR output or anything computed from them. It produces:

| Output | To | How |
|---|---|---|
| u_t ∈ R^{32} (counterpart partner channels) and a_t ∈ R³ | the wrap's input only | MediaPipe → P₀ → reflection P; GeMAPS-lite after AEC and half-duplex gate; voice and timing per phrase and turn; burst features from VAD minus ASR word alignment; samples held over tracking dropouts (last valid frame), filters initialised from the first frame of a session |
| lexical word stream c_lex | S (as context), 𝒦, Ω | Whisper-small, then **normalised**: lower case, lexical tokens only; non-speech tags, bracketed events and an innate list of about 60 interjections ("haha", "hmm", "uh"...) removed; punctuation removed and re-inserted by an innate lexical rule ("?" iff the utterance starts with one of about 40 interrogative or auxiliary words; "." otherwise). Text order only: S receives utterance n's embedding as a turn-indexed input (§2.5) |
| u_t, a_t, c_lex (full) | 𝒦, the knowing register | read only, never back into S (Check B2) |
| identity token | S, 𝒦 | once per session |
| own-face observation | 𝓔 fit only | a second MediaPipe instance on the agent's own rendered frames, own-tagged (S4) |

**Check B1 (imports).** No module outside 𝓑 reads a camera, microphone or ASR stream, or anything derived from them, except the outputs above.

**Check B2 (the only roads to expression).** The only writers of the 32 counterpart outputs are y = 2K^{1/2}s (the wrap, with the port inside s) and, on articulators only, visemes. Nothing in 𝒦 or Ω is an input to S_f or S_s. Ω reaches s only through P_Ω. The TTS receives phrase-level voice and timing targets only from y; text supplies phonemes and a zero-mean contour.

**Check B3 (no read-back except own-tagged).** The agent's rendered face is observed only by the own-tagged MediaPipe instance, whose output fits 𝓔 in replay and nothing else. Own speech is removed from the microphone by AEC plus the half-duplex gate.

Revision 1's Check A forbade any self-observation and so blocked S4; B3 replaces it.

### 2.3 The banded wrap

**The wrap.**
- v_t = K^{1/2}P u_t.
- s_t = S(w_{<t}; a_{≤t}, c_{≤t}, d_{≤t}) + P_Ω(e_{≤t}), with S strictly causal (one frame).
- w_t = v_t − s_t, y_t = 2K^{1/2}s_t.

Read as operators, y = 2K^{1/2}S(I + S)^{−1}K^{1/2}Pu for fixed (a, c, d, e).

**Interpretation.** w is the partner's face *minus the agent's own expressive contribution*, in the agent's own scaled coordinates: the core perceives the partner as a difference from itself. Since S also knows its own s, w loses nothing about u: knowing is complete (§3.2).

**The banded S.** S(w) = H_o ∘ S_f ∘ H_i (w) + S_s ∘ L (w), where:
- S_f is a γ_f-contraction in its partner input (ℓ₂, incremental, every causal truncation), for every fixed (a, c, d) and every parameter value;
- S_s is a γ_s-contraction in its partner input in both ℓ₂ and ℓ∞ (incremental), for every fixed (c, d) and every parameter value;
- **no state is shared from S_f into S_s.** S_f may read S_s's states as context; S_s may not read S_f's states. This is the no-demodulation rule (§3.4).

Because |H_i|² + |L|² ≤ 1 at every frequency (H1a) and |H_o| ≤ 1:

‖ΔS‖ ≤ γ_f‖H_iΔw‖ + γ_s‖LΔw‖ ≤ √(γ_f² + γ_s²)‖Δw‖ = 0.492‖Δw‖ ≤ γ‖Δw‖.

So the whole S is a 0.5-contraction, and revision 1's Claim W applies unchanged to the whole map (§3.1).

### 2.4 Inside S_f, the fast block

S_f(ŵ) = diag(γ_f σ(φ_k)) · A(c̃) · M ∘ 𝓡_θ([Φ_R(F ŵ), √κ_a a], c̃, d), ŵ = H_i w.

1. **F:** the innate filter bank and lag line (§2.1), H∞ gain ≤ 1, carrying the one-frame delay.
2. **Φ_R:** the own-body reading, per band. R = 𝓔^{−1} at rest: the regularised inverse of the agent's own appearance map 𝓔 (own command synergies → own observed face; fitted from self-observation and babbling, §2.10). It is spectrally normalised.
   - The partner reaches every learned and innate part of S_f only in the agent's own 12 synergy coordinates, plus the 6 voice/timing, 3 burst and 3 lateral coordinates, whose correspondence is innate.
   - The innate echo is realised on Φ_R, not on raw channels. This fixes revision 1's "mimicry bypasses R".
3. **𝓡_θ:** an acyclic robust REN (direct parameterisation, Revay, Wang & Manchester), Lipschitz 1 in its partner input. Context c̃ (below) and own innovation d (band-limited noise, 2.6–6.5 Hz, sd 0.04) are free inputs. Its states include:
   - motor habituation H (rises with the 2-min autocorrelation of the joint pattern [own display, ŵ]; it scales the gain of own innovation d);
   - the startle/orienting reflex from a.
4. **M:** the muscle filter, inside.
5. **A(c̃):** need-conditioned attention. Each output channel takes a softmax over the 32 REN outputs. The query comes from context, the keys are learned, ‖A‖₂ ≤ 1.
6. **diag(γ_f σ(φ_k)):** learned per-channel gains, sign-free here (sign is set inside 𝓡). The pull holds φ in a ball (§3.10).

**Context c̃** = (S_s's slow states: body, mood summary, attended slot; the current lexical-utterance embedding; role from partner VAD; identity token). Through c̃, context and the learned relationship set each channel's fast sign and size within 0.5–1 s. That is D78's "set by context and learned relationship, can flip sign".

**The innate prior θ₀ (reflexes).** These are what a newborn agent does before learning:
1. a positive echo at ℓ_echo = 0.45 s on lip-corner pull, cheek raise, brow raises and head pitch, in own synergy coordinates;
2. gaze following at the same lag, in the reflected frame (bounded by κ_lat);
3. own fast head micro-motion gated down by the partner's 2.6–6.5 Hz head envelope (C1);
4. a nod at the partner's turn-end pulse;
5. a startle (brow raise, lid raise) at audio onsets, through κ_a.

### 2.5 Inside S_s, the slow block

S_s reads the partner only through x_t = L(w)_t. It runs at 2 Hz on x decimated after L, and its output is held and linearly interpolated at 30 Hz, causally. It is built from three kinds of piece:
- positive linear filters (leaky integrators, ℓ₁ norm = DC gain ≤ 1);
- memoryless maps with weight matrices normalised by max(‖W‖₂, ‖W‖_{∞→∞}), so each is Lipschitz in both norms;
- one certified recurrence: the body ↔ slot-read loop, with loop gain ≤ 0.5 of the innate body leak.

The composite partner gain is ≤ γ_s in ℓ₂ and in ℓ∞ for every parameter value.

**1. Reading the partner's body through the agent's own body (P3).**
- p̂ = R·x: the partner's slow face in own command synergies.
- b̂_p = Π̃(p̂, c̃): the agent's own body state that, under its own display policy Π, would show this face. Π̃ is an amortised inverse of Π, trained on own data only: pairs (own b, own command) from the agent's own life. It is tied to Π by that training and has no other input layer.
- A word-side reading b̂_p^{lex} runs the same way from the lexical embedding: the own body state in which the agent itself produced utterances like this one (learned from own utterances and own body, §2.10).
- The two are combined by fixed precision weights 0.6 (face) and 0.4 (words).

**2. Body variables (innate dynamics; slow ones here).**
- **E, energy.** Flat awake cost; restored at rest. It is partner-independent by construction: the fast block pays no partner-proportional tax.
- **A, arousal load.** Driven by the slow mean of the partner's audio energy and motion in x (no fast demodulation), by event words in c_lex (the world model's surprise on the *lexical* stream, computed in S_s from the turn-indexed embedding), and by own body change. τ = 3 min.
- **V, aversive load.** Driven by two innate inputs:
  - being the target of another's aversive state: the aversive and arousal parts of b̂_p, times the partner's slow gaze-at-agent;
  - loud audio, the slow mean above an innate level.

  τ = 10 min. The undefined "own-predicted harm" of revision 1 is removed.
- **C, concern load.** τ_C Ċ = −C + 𝒟(b̂_p): the agent's own drive, evaluated at the partner's inferred body. τ_C = 10 min.

  C is the agent's own variable. The partner's face and words are its evidence. Nothing regulates the partner (§3.11).

**3. Mood ladder μ ∈ R^{128}.** μ_j(t+δ) = e^{−δ/τ_j}μ_j + (1 − e^{−δ/τ_j})·W_j^+ g_j(c̃)·m(b, x), with:
- nonnegative mixing W_j^+;
- write gates g_j driven by c̃'s non-partner part only;
- m a normalised feature map.

These are linear leaky modes with no wells, and positive filters.

**4. Relationship and episode slots.** 128 slots (k_m, V_m).
- Addresses come from c only: identity × topic embedding × episode index.
- For a fixed address, a write is the convex update V_m ← (1 − αa_m)V_m + αa_m·v(b, b̂_p, μ), so it is linear in the written value and a positive filter.
- Values decay with τ_slot = 30 days.
- Reads: a softmax over keys with query q(∇𝒟(b), b̂_p, μ), whose norm is capped so that the read's Lipschitz constant is inside the budget.
- This is where the relationship lives as *state*: how this partner's slow face, words and the agent's own concern have gone together, per topic.

**5. Display policy Π.** s_s = Π(b, μ, slot read, c̃, x; ψ). It is a 2-layer MLP normalised in both norms, with its partner-path gain counted in γ_s.
- **Objective:** it minimises J (§2.11), trained in replay through 𝓜 as a differentiable simulator.
- **Innate prior Π₀** (reflexes on the own drive, as in a newborn):
  - a distress configuration (brow inner raise, lip-corner depress, lid tighten) scaled by the rise of 𝒟;
  - a relief configuration (lip-corner pull, cheek raise) scaled by the fall of 𝒟;
  - lowered tone with low E.
- The words' own appraisal (c̃ → Π) has its own gain, outside the partner budget. Words are common cause.

**6. Turn-indexed lexical input.** S_s (and c̃ for S_f) receive utterance n's embedding as a value latched at the partner's turn-end pulse.
- The turn-end pulse reaches S through a (inside the wrap).
- The leak of the lexical state is per *turn*, not per second.
- So no state of S integrates inter-utterance time. The partner's speech rate and pauses reach S only through u's timing channels, inside the wrap.

### 2.6 The port P_Ω

P_Ω(e) = HP_{τ_Ω}(G_Ω(e, c̃)), where:
- e = (embedding of the agent's own realised utterance, own speech activity, the self-simulated relief R of the act chosen, §2.11);
- G_Ω is a 2-layer MLP with Lipschitz cap in e such that its effect on every counterpart output, after the closed loop's amplification 2√κ/(1 − γ), is ≤ a_Ω = 0.10;
- HP_{τ_Ω} is applied at the port's *output*, so the port's contribution to s has zero DC for every input. A nonlinearity before the high-pass cannot rectify into DC.

The port is how Claude's words show on the agent's face. A reappraising sentence, or the act of comforting, gives a brief relief or concern display (≤ 0.10, decaying over 15 s).

### 2.7 The knowing register 𝒦 and the world model 𝓜 (outside S)

𝒦 reads everything:
- full-rate u, a, c_lex with its timing;
- S's states and outputs, and own body.

It cannot write to S (Check B2). It holds:
- **𝓜, the world model.** An LRU stack, 2 layers × 128 complex modes, with innate moduli (1 s to 2 min) and learned phases and couplings. Heads:
  - (i) **own body** next b, and own observed face;
  - (ii) **the partner's streams** (face, voice, bursts, timing, lexical embedding). This head is **action-blind**: it is trained with the agent's own outputs masked from its inputs, so 𝓜 cannot represent any effect of the agent's acts on the partner;
  - (iii) **f_recv:** the agent's own body change after *receiving* a partner act (words, voice, face) given its own state;
  - (iv) **lexical-body:** own body in which own utterances were produced.
- **The rich partner model:** 𝓜's partner-head state, plus a slot copy keyed like S_s's, but written from full-rate data. This is what lets Claude's retrieval know that the partner laughed twice, speaks slowly tonight, and has looked sad since ten.
- **I, own-forecast uncertainty.** The predictive variance of 𝓜's own-body head over the next minute, above an innate floor. It is a body variable that drives Ω only.
- **Concepts** (§2.8.4).

### 2.8 Ω: Claude, drafts, retrieval and naming

1. **Drafts.** At each agent turn, Claude, frozen and called through the API, receives:
   - a constant instruction to write six replies that differ in what they attend to;
   - the normalised lexical transcript;
   - up to 3 retrieved snippets of raw past dialogue text.

   No body values, latents, category ids or labels are sent.
2. **Retrieval.** Need-conditioned attention over 𝒦's episodic store.
   - The query is built from ∇𝒟 over the full body (including C and I), b̂_p and the current concept posterior.
   - An ALiBi recency bias is added, plus β × the PMI of each snippet's tokens with the current category.
   - Through this, a silently sad partner changes which past dialogue Claude sees (for example, an evening when the partner said he was low), and so what it writes.
3. **Selection.** Each draft i is scored by an 𝓜 rollout, partner exogenous:

   score_i = −E[Σ_{30 s}(𝒟(b̂) + w_C(𝒟(b̂_p) − R_i)₊)],  R_i = 𝒟(b̂_p) − 𝒟(f_recv(b̂_p, draft i)).

   R_i is the self-simulated relief: how much draft i would relieve the agent if it were in the partner's inferred state. Drafts violating the echo guard are excluded first. The choice is argmax plus Gumbel noise at temperature 0.1.
4. **Concepts and naming.** The slow summary z = (b, C, μ summary, attended slot) is clustered online by DP-means; each category is a discrete latent of 𝓜's slow prior. For every lexical token the system keeps a pointwise mutual information with the category posterior, over tokens said by either party within ±1 turn. Claude names a state only through retrieval:
   - when the agent is in category k, snippets rich in tokens that have gone with k ("tired", "worried", whatever this household actually said) are favoured;
   - asked "how are you?", Claude answers from those snippets.

   The state reaches Claude only as which raw text it is shown (P4).
5. **Speech.**
   - Phonemes become visemes on the articulators (amplitude ≤ V_A, scaled by y's articulation-energy channel).
   - The TTS takes phrase targets (F0 level, F0 range, energy, rate, pause) from y at phrase onset, latency from y at turn onset, and from text only the zero-mean contour (±P_txt).
   - Non-lexical vocalisations come only from y's burst channels, never from text. Claude's text is stripped like the ASR text before the TTS.

### 2.9 Output assembly

- **Face:** M ∗ (visemes + blink reflex) + Q_render(y), where y already includes M inside both blocks.
- **Voice:** as in §2.8.5. The renderer and TTS apply no further partner-dependent processing.

### 2.10 Learning, and what it may read

- **Online (states only):** S_f's and S_s's states (body, μ, slots, H), 𝒦's states and 𝓜's fast heads (one SGD step per 10 s), concept centroids, PMI counts.
- **Nightly replay** from the episodic store. The store holds u, a (float16, 30 Hz, the last 30 days; decimated to 2 Hz after that), the lexical transcript, own states, own outputs and own-face observations. These are feature streams, not raw video or audio (P7).
  - 𝓜 is trained by predictive likelihood (all heads).
  - 𝓔 is fitted from own-face observations; R follows.
  - Π̃ and the lexical-body head are fitted from own data only.
  - Π, S_f's θ (REN, A, φ) and the draft scorer minimise J through 𝓜 rollouts with the partner exogenous. The fast block learns from clean u.
- **Innate stop.** Gradients are clipped at G = 1 and pulled to θ₀ (λ = 0.5 for S_f, 0.1 for S_s). Consolidation pulls each night's weights to the last with λ_n = 0.01.
- **Bias-free S.** No layer of S_f or S_s has a constant offset on its output path, so that S(0; c = ∅, d = 0, b = b*) = 0 for every θ. At reference conditions the agent's face is at innate rest whatever was learned (§3.10).

### 2.11 The one core (Principle 10)

**One generative model, one objective, two structural constraints.**
- **Model.** 𝓜: the predictive likelihood of own body, own observed face, the partner's streams (action-blind) and words, with a category prior over slow states.
- **Objective.**

  J = E ∫ [𝒟(b_t) + w_C(𝒟(b̂_p,t) − R(a_t; b̂_p,t))₊] dt,  𝒟(b) = Σ_i w_i ψ(|b_i − b_i*| − δ_i)₊,  ψ(x) = x².

  Every choice minimises J: the display policy, the fast block's learned part, draft choice, retrieval queries and write gates. Rollouts hold the partner exogenous (the action-blind head). That is the path-specific reading of Principle 6: no path from the agent's acts through the partner's state is ever evaluated.
- **(W)** Every counterpart output is the banded wrap of §2.3, plus visemes.
- **(B)** One boundary, Checks B1–B3.

**How each component follows.**
- **Homeostasis:** 𝒟.
- **Curiosity:** I, satiated as own-body forecasts improve.
- **Valence and arousal:** readouts of 𝓜: −E[d𝒟/dt] and E‖ḃ‖ over the next minute.
- **Mimicry:** θ₀ in S_f, refined by J (self-simulated relief of being responded to).
- **Reading others:** b̂_p = Π̃(R·x), the inversion of the agent's own display policy and appearance map.
- **Care:** the second term of J.
- **Regulation:** draft choice by J, and own words through the port.
- **Replay:** likelihood plus J.
- **Concepts:** the category prior.
- **Anti-repetition:** H.

**Where it is still an assembly** (stated honestly, §10): the echo guard, the floor rule, ASR and TTS normalisation, the punctuation rule, the five reflexes of θ₀, Π₀, and the PMI table. Each is a fixed innate rule, not a consequence of J.

## 3. Properties, each with an argument

### 3.1 The wrap, kept (Claim W)

For any S strictly causal with incremental ℓ₂ gain ≤ γ < 1 in w (for fixed exogenous inputs), on every causal truncation:
- (W1) ⟨Δy, Δu⟩ ≤ b⟨Δu, KΔu⟩ with b = 2γ/(1 + γ), in every partner direction;
- (W2) per pair (k ← j): ‖Δy_k‖ ≤ 2√(κ_kκ_j)·γ/(1 − γ)·‖Δu_j‖;
- (W3) the disc ‖ŷ − mv̂‖ ≤ r‖v̂‖, with m = −2γ²/(1 − γ²) and r = 2γ/(1 − γ²);
- (W4) the parameterisation is complete for the sector.

The argument is revision 1's §3.1, unchanged. As the novelty critic noted, the image equals "centre plus radius times a contraction", the robust-REN feedthrough form. The Cayley form is kept because S = 0 is flat (no response), so the innate prior sits at the origin.

The banded S has γ_eff = 0.492 (H1b), so for every signal: in-phase ≤ 0.198, any ≥ −0.582. The band structure then sharpens these per band (§3.2, §3.3).

### 3.2 Knowing is not moving: no held copying through any slow path (Claim K)

**Claim K.** For every parameter value, every fixed word stream and identity, and every own-noise path, let the partner hold any expression offset Δ (a unit direction e in counterpart space, any length of hold). Then, at steady state, the agent's counterpart response along e satisfies:

  −0.150 ≤ ⟨Δy, e⟩ / ‖Δ‖ ≤ 0.100 (κ = 0.3 channels),

and the in-phase ratio of the hold's running mean from onset is ≤ 0.100 on every truncation. This holds although S_s's states may encode the held level exactly.

**Argument.**
1. **DC passes only one block.** H_i has zero DC gain, so S_f sees no held level. H_o has zero DC gain, so S_f's output has none either (and S_f cannot rectify into the output DC, because H_o is last). P_Ω has zero DC by its output high-pass. So the steady-state map from a held v to s is the wrap of S_s∘L, and L(DC) = 1.
2. **The wrap of a γ_s-contraction has DC gain 2κσ/(1 + σ), σ ∈ [−γ_s, γ_s]** (incrementally: the disc of W3 with γ_s). Its range is [2κ(−0.2)/(0.8), 2κ(0.2)/(1.2)] = [−0.150, +0.100].
3. **Knowledge is complete.** S_s's internal state can hold L(w + s) = L(v), the partner's held face exactly, because S_s knows its own output. H2a: the 1-min knowledge correlates with the partner's 1-min mean at **0.994**. What the contraction constrains is how any function of that knowledge can move s, not what it represents.
4. **Every slow path is inside S_s:** mood μ, slots (relationship), body (C, V, A, E), the display policy Π, and the lexical latch. The only slow states outside S_s are in 𝒦 and Ω, and they reach s only through P_Ω, which is zero-DC.

**Numbers (H2, 48 h of held levels changing every ~60 min, with transients):**

| Readout of the same knowledge | 1-min-mean slope on the partner's 1-min mean |
|---|---|
| straight to the face (no wrap) | +0.906 |
| through the wrap, copy-seeking policy (σ = +γ_s) | +0.092 (cap 0.100) |
| through the wrap, opposite-sign policy (σ = −γ_s) | −0.133 (cap −0.150) |

**What the agent can still do with the knowledge.**
- Show it gently on the face: a held concern of up to 0.15 of range in any direction, 0.10 toward the partner's expression.
- Act on it fully in words: C and b̂_p drive retrieval and draft choice in Ω.
- Show it richly in *other* directions in the fast block (sign-flipped and cross-channel up to the fast disc) whenever the partner moves.
- Let it set the fast block's context: a held sad face changes how the agent responds to the partner's next smile.

### 3.3 Why an ℓ∞ bound on the slow block is needed, and what it gives

The ℓ₂ disc alone bounds the *running* mean from onset and the steady state, but not a later window.

**The problem (H7).** Searching over all operators in the slow disc (LP over 2-h FIR kernels at 30-s steps), the worst 1-min mean of the in-phase response to a held unit step is:

| Time after onset | Worst 1-min mean |
|---|---|
| 1 min | +0.132 |
| 5 min | +0.179 |
| 30 min | +0.246 |
| 60 min | +0.265 |

An operator can respond negatively at first and positively later, keeping the running mean ≤ 0.10. Over a long hold, that is a delayed near-copy. It is the slow-time analogue of N3 (a sign flip at a slow frequency is a copy at a long lag).

**The fix.** S_s is also a γ_s-contraction in ℓ∞:
- its linear parts are positive filters (‖h‖₁ = DC gain ≤ 1);
- its maps are Lipschitz in the ∞-norm;
- its one recurrence is certified by ∞-small gain.

Then, pointwise in time, |Δs_s(t)| ≤ γ_s·sup_{τ<t}|L(Δw)(τ)| ≤ γ_s·sup|Δv − Δs|. By small gain, |Δy_k(t)| ≤ 2κγ_s/(1 − γ_s)·sup|Δu| = **0.150** at every instant.

H7 checks the closed loop for every open-loop slow kernel with ‖h‖₁ ≤ γ_s: in 300 random and 20 adversarial (Nelder–Mead) kernels, the worst 1-min mean found is **+0.120 ≤ 0.150**.

**Residual leak from the fast block into the slow loop.** L∘H_o is a band-pass with ℓ₁ norm ≈ 0.11, so fast-block output leaks into L(w) at ≤ 0.11 × its peak. An onset peak of at most 0.27 contributes ≤ 0.01 of range to a 1-min mean.

### 3.4 No demodulation: the event-rate dial is closed by structure

A slow state fed by rectified fast features (event counts, the energy of bursts) converts the *rate* of the partner's transient expressions into a held output. The full-band cone does not stop this, because its bound is on in-phase *energy*, and spiky signals have far more energy than DC.

**H5.** A partner smiles in 1.5-s bursts at a rate that varies by episode, with no held level.

| Structure | 1-min-mean slope |
|---|---|
| this design (S_s reads L(w) only) | +0.015 |
| forbidden variant: slow output fed by the rectified fast band at the fast gain (still a valid 0.45-contraction in ℓ₂) | +0.109, above the slow cap |

Hence the rule in §2.3 that no state flows from S_f into S_s. The rate of the partner's smiles reaches the slow block only through their local mean, which L passes and the slow disc caps. Rate *knowledge* is free in 𝒦.

The modulated-manifolds design failed on exactly this route ("event trains integrate, so event rate is a dial"). Here it is closed structurally.

### 3.5 The fast block learns context-set, sign-flippable, relationship-specific strengths from real signals

- **Signals.** Replay holds u at 30 Hz, so S_f's θ is trained on the partner's clean features. The wrap holds for every θ, by construction. Learning therefore needs no noise, and no learned value can leave the cone.
- **H3.** S_f is a two-tap context-gated block (taps at 0.45 and 0.9 s, |g₁| + |g₂| ≤ 1, scaled by γ_f), trained per context by MSE to a target response on 10 min of clean u:

  | Context | Target lag-0.45 s gain | Learned | Lag bound [mρ − r, mρ + r]κ |
  |---|---|---|---|
  | friendly | +0.15 | +0.135 | [−0.33, +0.34] |
  | opposed | −0.40 | −0.238 | [−0.33, +0.35] |
  | copy target | +1.00 | +0.129 | inside the cone |

  The same learner given revision 1's release (σ = 7.1 on a 2-Hz stream) learns **+0.00018**.
- **What sets the sign in the real system.** The sign is a function of c̃: the relationship slot read, role, the lexical utterance and mood. Its learning signal is J's care term, through f_recv: the agent learns, from its *own* experience of being responded to, which fast responses relieved it in which contexts, and offers those. For example, being smiled back at in an argument raised its own V, so it learns not to smile back in arguments. That is relationship-specific because the context includes the identity-keyed slot.
- **Within minutes.** Slot *states* are written online. A partner's last few minutes change c̃, and so the fast signs, without any weight change. This is Golland's second-clip effect, carried in state.

### 3.6 Lateral channels: reflected, then capped on both sides

- **The fix.** Head yaw, head roll and horizontal gaze are reflected by P before the wrap, so mirror imitation (what an observer sees as following) is the in-phase side. Their weight κ_lat = 0.05 caps that side at 0.031 (fast) and 0.017 (slow), and the anatomical side at 0.082 and 0.025.
- **H4** (the critic's K4 setup) measures, for a mirror-seeking or anatomical-seeking fast block, a mirror-copy gain of ≤ **0.045** and an anatomical gain of ≤ **0.078**, against revision 1's 0.58.
- **Cross routes.** Symmetric → lateral routes are capped per pair by (W2): 2√(0.05·0.3)·0.45/0.55 = **0.20** (H1c). They matter only if the partner's lateral motion is perfectly correlated with a symmetric channel.
- **Price.** Gaze following is weak in the fast block (lagged broadband ≤ 0.056). Joint attention to a referent comes through words.

### 3.7 Why a discrete route cannot be inside any cone (N4), and the port

**N4.** Let a route choose among finitely many outputs (drafts) with probabilities that depend continuously on the partner input. Then:
- For a fixed own-noise path, the chosen output jumps at a switching surface, so no incremental ℓ₂ gain is finite there. W1–W3 need ‖Δs‖ ≤ γ‖Δw‖ pathwise and fail.
- Over the own noise, the optimal coupling of the two runs' choices agrees with probability 1 − TV and differs by a fixed distance d otherwise. So W₂(law(u), law(u′)) ≥ √(TV)·d ∝ ‖Δu‖^{1/2}: Hölder-½, not Lipschitz, for small perturbations.

So no per-path or W₂-mean version of the wrap contains a discrete choice whose effect on expression is nonzero. Draft choice, retrieval and Claude's words must reach the face through something other than the cone: a magnitude allowance.

**The port is the smallest allowance that keeps every held bound:**
- Lipschitz in e, capped at a_Ω = 0.10 per channel (sign-blind; it counts toward the 0.198 zero-lag total only when e itself moves in phase with the partner);
- zero DC by its output high-pass, so 10-min means move ≤ 2τ_Ωa_Ω/600 = 0.005 and 1-min means ≤ 0.05.

**H6.** An adversary makes Claude's words track the partner's held level exactly. The port's 1-min and 10-min contributions have slope +0.003, and the worst |1-min mean| is 0.024 ≤ 0.05.

**What else Ω touches, each closed** (routes R9–R12 in §3.8):
- the realised text drives visemes (articulators only, half-duplex, echo guard);
- the TTS contour is zero-mean;
- non-lexical sounds are stripped;
- speaking time does not tax E in proportion.

### 3.8 Every route, counted

"Copy" means concordance of the agent's rendered counterpart channel with the partner's same channel (anatomical, or mirror for the lateral channels), holding the partner's lexical words and identity fixed (the C8 surrogate).

| # | Route | Mechanism | Bound |
|---|---|---|---|
| R1 | partner face (symmetric), voice, timing, bursts → fast block → all 32 outputs | wrap of S_f behind H_i, H_o | in-phase ≤ 0.186; lag ≤ r_f + m_fρ_u(τ) ≤ 0.339 broadband; any ≥ −0.491; zero DC |
| R2 | same partner channels → L → slow block (knowing, body C/V/A/E, mood, slots, Π) → all outputs | wrap of S_s, ℓ₂ and ℓ∞ | held: [−0.150, +0.100]; any instant ≤ 0.150; 1-min means with port and edges ≤ 0.21 at worst transient, → 0.10 + 0.005 at steady state |
| R3 | lateral channels, either block | reflection P, κ_lat | mirror ≤ 0.031, anatomical ≤ 0.082; cross from symmetric ≤ 0.20 per pair |
| R4 | exogenous a (audio onset, VAD, turn-end) → S → outputs | √κ_a input | ≤ 0.20 per pair × corr(a, partner channel) |
| R5 | speech rate, pauses, latency → own TTS rate, pauses, latency | voice/timing channels inside R1/R2; TTS targets from y only | as R1/R2 per channel (failure 2 of critique 1a closed) |
| R6 | partner laughter, sighs, crying → own vocal bursts and face | burst channels inside R1/R2; non-lexical ASR tokens removed | as R1/R2 (failure 5 closed) |
| R7 | audio onset → blink (non-counterpart) | innate reflex outside the wrap | ≤ ℓ_blink·corr(partner onsets, partner blinks) |
| R8 | 𝒦 / S states → Ω (retrieval, draft choice, concepts) → own words → P_Ω → outputs | port | RMS ≤ 0.10; 1-min means ≤ 0.05; 10-min ≤ 0.005; DC 0 |
| R9 | own words → visemes (articulators) | half-duplex (lag-0 overlap 0); echo guard | best-lag excess over surrogate ≤ 0.05 (revision 1's G8); verbatim echo excluded |
| R10 | own words → TTS contour | zero-mean contour; phrase targets from y | 0 on phrase-level counterpart values (assumption: TTS realises targets, §3.15) |
| R11 | own words → non-lexical TTS output | text stripped | 0 |
| R12 | own speaking time → E → Π | E's cost is flat; speech activity enters only e | through the port |
| R13 | partner VAD → floor flag → when the agent may start | memoryless gate; onset latency from y | anti-concordant on voice activity; latency inside R5 |
| R14 | partner's lexical words → S (c̃ and Π's word input), 𝒦, Ω | common cause; turn-indexed, no time integration | excluded by definition (words fixed); amplitude ≤ 0.8. Named so it is counted |
| R15 | Claude API readiness → own latency | the onset waits for the draft | partner-independent, up to the length of the partner's last utterance |
| R16 | identity token | once per session | ≤ log₂(#partners) bits per session |
| R17 | nightly weights (S_f, S_s, Π, 𝓜, scorer) | wrap for every θ; bias-free S; pulls | per-θ cone holds; cross-world shaping bounded by the θ-ball (§3.10) |
| R18 | episodic store → retrieval → Claude | inside R8 | as R8 |
| R19 | own rendered face → own-tagged MediaPipe → 𝓔 → R | own data only | no partner dependence |
| R20 | own speech → microphone → u | AEC + half-duplex | 0 while speaking; residue enters u, inside R1/R2 |
| R21 | own face → partner → partner's face → u | external loop | W1–W3 hold for the partner's *actual* face; fast-dyad stability needs only partner mimicry gain < 1/0.582 = 1.7 |
| R22 | concept categories → retrieval → Claude | inside R8 | as R8 |
| R23 | 𝒦 → S | forbidden (Check B2) | 0 |
| R24 | ASR word choice depending on prosody | assumption (§3.15) | 0 if ASR's lexical output is invariant to held prosody |

**Totals per counterpart channel (κ = 0.3), words fixed.**

| Time scale | In phase (toward the partner) | Away from the partner / any direction |
|---|---|---|
| zero lag, any band | 0.198 (+ a-route 0.20 × corr; + port only if words move in phase) | −0.582 |
| fast lag, broadband | 0.339 | — |
| held, steady state | **0.100** | −0.150 |
| any 1-min mean during a hold | 0.15 (ℓ∞) + 0.05 (port) + 0.01 (edges) = 0.21 worst transient | — |
| 10-min means | 0.105 | — |

Every number is below 1 at every time scale. The held number, the one revision 1's critics broke three times through slow paths, is 0.10 for every route but R14 (words, by definition) and R4 (only through the partner's own audio–face correlation).

### 3.9 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy non-attracting under own learning |
|---|---|---|---|---|---|
| κ_k, κ_lat, κ_a | yes | no (innate) | — | it *is* the cap | — |
| γ_f σ(φ_k) | yes | learned per channel | — | γ_f = 0.45 innate; φ in a ball | yes: in the cone for every φ |
| 𝓡_θ and A(c̃) (fast gates) | per output | yes, through c̃ (slots keyed by identity, role, words, mood) within 0.5–1 s | yes, anywhere in the fast disc [−0.49, +0.19] | Lipschitz 1, innate | parameters in a ball around θ₀ |
| Π and the slow gains | per output | yes (slots, mood, words) | yes, in [−0.15, +0.10] | γ_s = 0.20 innate, ℓ₂ and ℓ∞ | yes |
| shared context coordinates (one stance value driving all channels) | shared | yes | yes | the matrix sector: ≤ 0.198 in phase in every direction | — |
| a_Ω (port) | per channel | yes (G_Ω reads c̃) | yes | 0.10, zero DC | — |
| ℓ_blink, V_A, P_txt, ω_max | per channel | — | — | innate | — |

**No single quantity runs the whole face or a large shared subspace from flat to copy.** The matrix sector bounds every direction, the whole face included, at 0.198 in phase (0.100 held).

### 3.10 Copy is not attracting under learning; what nightly learning can and cannot shift

- **(a) Every learned value stays in the cone.** For every θ the wrap holds, so no learning trajectory reaches copy. Clipped SGD with the pull keeps φ within |φ − φ₀| ≤ G/λ, as in revision 1's G7.
- **(b) The rest face cannot be learned away.** S has no output bias, so at reference conditions (partner at rest, body at set point, no words, no noise) s = 0 for every θ. Learning cannot give the agent a resting expression shaped like the partner's.
- **(c) Cross-world shaping is not copying, and it is bounded.** Compare an agent raised with a chronically sad partner with one raised with a cheerful partner. Their weights differ, so their responses to the *same* words can differ. That is temperament and relationship shaping, which the brief wants (S6) and C9 permits. It is not the within-agent counterfactual that defines copying. It is bounded by the θ-ball and by (b).
- **(d) Partner-specific adaptation lives in states,** which are inside S and inside the cone: slots (30 days), μ (up to 73 h), C. Weights need not carry it.

### 3.11 An emotional agent

**(1) Body variables that respond to what is said and done.**

| Event | Body response | Path |
|---|---|---|
| the partner says his dog died, with a neutral face | b̂_p^{lex} (the body in which the agent itself said things like this) has high V → 𝒟(b̂_p) rises → C rises over minutes | words (R14), own body (P3) |
| the partner looks silently sad for 20 min while talking about plans | b̂_p from p̂ = R·L(v) → C rises within 1–2 min (τ_L, τ_C), and stays while the face stays | R2, P3 |
| the partner glares at the agent and raises his voice | V rises (target of an aversive state, with gaze at the agent); A rises with the slow loudness mean | R2 |
| a 1-s shout | the startle reflex in S_f (brow and lid raise, blink) within 0.1 s; 𝒦 registers it at full rate; draft choice responds | R1, R7, R8 |
| the agent talks for an hour | E falls at its flat awake rate | — |
| a surprising remark | A rises through the lexical surprise in S_s | R14 |

**Valence** is −E[d𝒟/dt], so it now moves with social meaning: a sad story raises C and lowers valence.

**(2) Care for a silently sad partner, from the agent's own concerns, with no incentive on the partner (Claim C).**
- **Concern is the agent's own drive at the partner's inferred body**, 𝒟(b̂_p). It is innate in form; its content comes entirely from the agent's own body model (P3).
- **What concern does:**
  - the face shows a gentle held concern (≤ 0.15 any direction; for example a slight brow-inner raise, in phase but ≤ 0.10, or a softened lip corner, cross-channel);
  - retrieval brings up past dialogue about how he has been;
  - draft choice favours replies with high self-simulated relief R_i.
- **No term of J rewards a change in the partner.** 𝓜's partner head is action-blind, so in every rollout b̂_p is exogenous. The only way an act lowers the care term (𝒟(b̂_p) − R)₊ is through R, the agent's model of how *it* would be relieved by receiving that act.
  - The partner looking happier afterwards lowers C in the *body* (evidence), but the planner never predicts or values it.
  - So there is no placation, flattery or engagement gradient.
  - The term is satiable: zero when the partner is not inferred distressed, and R ≤ 𝒟(b̂_p).
- **Revision 1's placation route is removed** (critique 1b, §1.4). A and V still respond to the partner's loudness and gaze, but only as evidence; no rollout predicts that a reply will quiet the partner.
- **Unusual happiness is not distress.** 𝒟(b̂_p) is the agent's drive at the inferred body, so a happy partner, inferred at or near set point, gives C ≈ 0 (revision 3 of the partner regulator could not tell them apart).

**(3) The display policy has a stated objective.** Π minimises J. Its ties to the agent's state are explicit: the innate Π₀ reflexes on the rise and fall of 𝒟, the care term (displays the agent itself found relieving when distressed), and motor cost and habituation. So the display follows valence (the rise and fall of 𝒟), concern and energy, not only self-repetition.

**(4) Concepts, and how Claude names them (P4).** Categories are latents of 𝓜's slow prior over (b, C, μ, slot). Each category's words come from what was actually said around it, by either party. Claude meets a category only as raw past dialogue chosen for it. It can then say "I've been a bit worried about you" because snippets from earlier worried states contained such words. It never sees a number or a label.

**(5) What the agent still cannot do** (honest, §8.1):
- show a strong *held* facial reaction to the partner's face (≤ 0.15);
- converge strongly on the partner's held vocal register within a conversation (≤ 0.10);
- let Claude's reappraisal change its face for more than about 15 s.

### 3.12 Principle 3 made essential

**Statement.**
1. Every partner influence on S passes through R = 𝓔^{−1} (own appearance coordinates) or the innate voice, timing and burst correspondences, and the innate echo itself runs on Φ_R.
2. The partner's body state is inferred as b̂_p = Π̃(R·x): the agent's own body state that, by its own display policy, would look like this.
3. b̂_p enters the *innate* drive 𝒟 (no learned input layer), which drives C and the care term.

**Why the rotation argument of critique 1b no longer applies.** That argument worked because every consumer of R's output had a learned input layer that replay refits. Here the consumer of b̂_p is 𝒟, which is fixed, and Π̃ is tied to Π, the policy that actually drives the agent's own face, by own-data training. Rotating R's coordinates changes b̂_p's mapping to body variables, so it changes which faces trigger concern. Nothing refits that away, because Π is pinned by its own role in producing the agent's face.

**Lesions, with specific predictions (§7):**
- **Replace Π̃ by the inverse of another agent's display policy** (or a generic face-to-body regression of equal norm). Concern is then triggered by the partner's faces that look distressed *to that other policy*.

  Prediction: C's correlation with the partner's self-reported distress drops, and C begins to respond to expressions the agent itself uses when calm.
- **Crossed habits (a Cook-style manipulation).** Retrain the agent's own Π so that its own high-V display uses lip-corner pull.

  Prediction: the partner's smiles now raise C and draw comforting replies. This is a behaviour no other design here predicts, and its sign follows from the equations.
- **Remove f_recv** (no self-simulated relief). Care acts become unspecific, and draft choice under high C becomes indistinguishable from choice under C = 0 with the same words.
- **Remove R** (partner input zero in S). The fast echo, the face-driven C and the face-driven fast sign setting vanish. Word-driven care remains.

### 3.13 Satiable drives and Principle 6

- **Satiable.** 𝒟 ≥ 0, and 𝒟 = 0 on the box ∏[b_i* ± δ_i]. The care term is zero when b̂_p is in the box, and R ≤ 𝒟(b̂_p). So J = 0 is reachable at rest with a content partner.
- **I is satiable in the strong sense.** It is predictive variance above a floor, not a constant-rate rise, so it does not demand perpetual progress (fixes critique 1b §1.4's side point).
- **Principle 6.**
  - The partner's face is evidence (C, V, A inputs) and never a target: no loss has the partner's features as a target except 𝓜's prediction head, and prediction is not regulation.
  - No rollout represents the agent's effect on the partner.
  - No body variable rises with the partner's smiles, attention or time spent.
  - Prolonging the conversation earns nothing.

### 3.14 Time scales from structure

| Scale | Carrier | Time constants | Set by |
|---|---|---|---|
| reflex | S_f: filter bank, REN contraction, M | 33 ms – 4 s (echo 0.45 s) | innate filters and H_i, H_o |
| appraisal | S_s body and lexical latch; 𝓜 | 1 s – 10 min | innate τ of A, V, C; LRU moduli |
| mood | μ ladder in S_s | 2 min – 73 h | innate τ_j |
| relationship | slots in S_s and 𝒦 | 30 days | innate τ_slot |
| temperament | consolidated weights | ≈ 100 nights | λ_n |

The ladder is a geometric sum of Lorentzians, so the state's spectrum is about 1/f between 1/(2π·73 h) and 1/(2π·2 min). That is a property of the structure.

### 3.15 What is assumed (the places to attack)

1. **ASR lexical invariance.** The ASR's lexical output, after normalisation, is invariant to held prosody. Test: pitch-shifted and energy-scaled replays, counting token changes, including the interjection list and the punctuation rule.
2. **TTS realisation.** The TTS realises phrase-level targets monotonically at about unit gain, and the zero-mean contour does not shift phrase means.
3. **Burst features carry no labels.** They are continuous energies of voiced audio not aligned to words; their quality depends on the alignment.
4. **The leak from the fast block into the slow loop is ≤ 0.01** (§3.3). That figure is computed for an onset peak ≤ 0.27.
5. **Claude API latency** is independent of the partner beyond the utterance length.
6. **The certified slow block.** Its ∞-norm normalisation and the body–slot loop's small gain are enforced in code, and checked at load with a randomised test of the composite Lipschitz constants.

### 3.16 The human non-copying signatures C1–C10

| | Signature | How this design produces it | Status |
|---|---|---|---|
| C1 | head coherence above surrogate at 0.2–1.1 Hz, below at 2.6–6.5 Hz | innate echo on head pitch (0.45 s); own fast micro-motion gated down by the partner's fast-band envelope (revision 1's G9, 40/40 seeds in critique K6) | produced |
| C2 | short-lag form divergence, relaxing; self-repetition ≤ chance | echo guard (words); H penalises joint-pattern repetition; S_f forgets within ~4 s | produced |
| C3 | shared referent, different form | the referent enters as words (R14); the form comes from the agent's own Π and repertoire | produced |
| C4 | role sets the sign | role ∈ c̃ (from partner VAD, inside the wrap) switches S_f's gates; now learnable from clean u (H3) | produced |
| C5 | episode sets net level, including below chance | slots and words set the fast sign anywhere in [−0.49, +0.19] and the slow one in [−0.15, +0.10], learned from clean signals | produced |
| C6 | stance and monitoring act separately | stance: slot read → sign; monitoring: I and C → attention-query magnitude. Two quantities | produced |
| C7 | joint-trajectory novelty rising over minutes | H is driven by the *joint* pattern [own display, ŵ], so the anti-repetition is dyadic (critique 1a §6 found revision 1's self-only) | produced; strength untested |
| C8 | coupling mostly common cause; partner-specific excess about a third; slower when event and face disagree | words (R14, up to 0.8, 1–2 s) against the fast echo (≤ 0.19 at 0.45 s); when c̃ disagrees, gates suppress the echo | produced |
| C9 | converge in parameters, not output | slow statistics of own movement can shift through slots and weights (§3.10c); output concordance ≤ 0.10 held | produced |
| C10 | coupling cannot disable self-restoration | the homeostatic pull and Π₀ act inside S_s on own body; the wrap bounds the partner's share of s at every instant | produced |

### 3.17 The brief's expressive-structure items

- **Content-dependent selection.** Need-conditioned attention runs in five places:
  - S_f's per-channel mixing A(c̃);
  - slot reads in S_s;
  - 𝒦's retrieval (the query from ∇𝒟, b̂_p and the concept posterior);
  - draft scoring;
  - concept-weighted snippet choice.

  Unlike revision 1, the knowing side can select over the partner's face content at full resolution (𝒦), because it is not on an expressive path.
- **Structure over people, episodes, topics and time:** slots keyed by identity × topic × episode in both S_s and 𝒦; the time-constant ladder; concept categories.
- **Effective dimensionality:**
  - S_s: 128 (μ) + 128 × 64 (slot values) + 6 (body);
  - 𝒦: 512 (𝓜) + 128 × 64 (slots) + 64 (categories);
  - S_f: 64.
- **A behaviour a low-dimensional version cannot produce.** The same words, from two partners whose faces have gone differently with the same topic, produce different fast signs and different concern, through different slots. Collapsing slots and μ to 2-d valence and arousal removes partner × topic specificity (§7).
- **Richness from structure:** about 0.7 M learned parameters (§6).

## 4. Why the closest mechanisms cannot do it alone

The table of revision 1 §4 stands; three rows change.

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| **Robust REN with a conic IQC (Revay et al.)** | the full-band sector for every parameter | One full-band sector bounds in-phase *energy*. It lets a slow state convert the partner's event rate into a held output (H5: +0.109), and an ℓ₂ disc lets a slow state respond late in phase (H7: +0.265 at 60 min). The band split with no demodulation, and the ℓ∞ slow block, are what bound held copying. A REN alone has neither |
| **Differential privacy / ledgers** | magnitude bounds that compose | Sign-blind (Kairouz): copying and anti-copying cost the same. Used here only in the degenerate form the port needs (a magnitude allowance on the discrete route), because N4 shows no cone contains a discrete choice |
| **Active inference; control as inference** | perception and action from one error | If the agent's model includes its effect on the partner and the partner's state enters its objective, action descends toward changing the partner (placation, or Lanillos' mirroring). Here the partner head is action-blind, and the partner enters J only as evidence for the agent's own drive at the inferred body |

## 5. The whole system, walked through

- **Perception through the body.** MediaPipe → P₀ → reflection → u; GeMAPS-lite and timing → voice channels; voiced non-lexical energy → burst channels. In S, the partner is read as the own synergy state that would look like this (R), and as the own body that would show it (Π̃). In 𝒦 it is read at full rate.
- **Latent state.** S_s's body, μ and slots; 𝒦's 𝓜 and categories. Nothing is labelled. Valence and arousal are readouts.
- **Face and voice.** One expression y = 2K^{1/2}s: fast reflexes and context-set responses, slow concern and mood, the port's brief responses to own words. Visemes are added on the articulators. TTS levels come from y.
- **Claude.** It is given 6-way drafts, retrieval steered by need, concern and concept, and selection by J with self-simulated relief. It names states only through retrieved text. Its words reach the face only through the port.
- **Learning by living.** States are online; weights nightly from clean feature streams; the fast block learns signs from the agent's own experience of being responded to.
- **Memory and replay.** The store holds feature streams (30 days at 30 Hz; 2 Hz after), the lexical transcript and own data. Replay samples by state tag (high |Δ𝒟|, novel categories).

  Ablation: remove the state tags, and slot specificity to partners decays across nights (S6).
- **Data leaving the Mac (P7, stated plainly).** The lexical transcript and up to 3 retrieved past snippets are sent to the Claude API every turn. Speech content leaves the Mac; features, video and audio do not. That is an operator decision (cf. Q3). Revision 1's "stricter than Principle 7" was inaccurate.

## 6. A buildable network

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

| Stream | Rate | Encoding | Why |
|---|---|---|---|
| partner face, gaze, articulators | 30 Hz | MediaPipe → P₀ → reflection P → u (23) **[M]** | the copy metric and wrap are defined here |
| partner voice and timing | per phrase or turn, held at 30 Hz | AEC + half-duplex → GeMAPS-lite (F0 level, range, energy); syllable rate from ASR alignment; pause and latency from VAD → u (6) **[M]** | timing is inside the bound (critique failure 2) |
| partner bursts | 30 Hz | voiced energy outside ASR word spans; 4–6 Hz modulation energy; breathiness (H1–H2 proxy) → u (3) **[M]** | laughter without labels (failure 5) |
| exogenous a | 30 Hz | onset envelope, VAD, turn-end pulse → √κ_a a | startle, nod, role |
| words | per utterance | Whisper-small → normalisation → MiniLM (384) → fixed random 64 projection; turn-indexed into S | meaning without timing |
| own body, display, role | 2 Hz (S_s, 𝒦), 30 Hz (S_f) | own-typed | — |

**Time encoding.**
- **S_f:** innate filter-bank band index and lag line. No positional encoding: a KV cache over the partner's past would be an uncertified memory.
- **S_s:** continuous time through innate positive leaky modes. Its lexical state is clocked by turns.
- **𝒦:** innate LRU moduli, exact event timestamps, and ALiBi recency for retrieval. 𝒦 needs no certificate, because it never writes to S.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, F, H_i, H_o, L, M, HP_Ω | fixed | 0 | — |
| 2 | 𝓔 (own appearance map; R its ridge inverse) **[M]** | 12 → 64 → 23 | ≈ 2,400 | replay, own-face observations |
| 3 | 𝓡_θ, acyclic robust REN, Lipschitz 1 **[M]** | n = 64, q = 128; input 60 (R-bands) + 15 (lateral bands) + 30 (voice, burst bands) + 3 (a) + 64 (c̃) + 6 (d) = 178; output 32 | ≈ 125,000 | replay |
| 4 | attention A(c̃) **[M]** | queries 64 → 32 × 16; keys 32 × 16 | ≈ 33,000 | replay |
| 5 | gain logits φ_k **[M]** | 32 | 32 | replay, pull |
| 6 | context encoder c̃ | (S_s summary 64 + lexical 64 + role 2 + identity 16) → 64, spectral norm | ≈ 9,500 | replay |
| 7 | S_s: Π̃ (own-body inverse) **[M]** | 12 + 64 → 64 → 6 | ≈ 5,300 | replay, own data |
| 8 | S_s: μ write maps (nonnegative) and gates **[M]** | 8 × (48 → 16) + gates 8 × 64 | ≈ 7,000 | replay |
| 9 | S_s: slot key, value and query maps **[M]** | identity/topic 80 → 64; value 48 → 64; query 76 → 64 | ≈ 13,000 | replay (states online) |
| 10 | S_s: display policy Π **[M]** | (6 + 32 + 64 + 64 + 32) → 128 → 32, two-norm normalised | ≈ 30,000 | replay (J) |
| 11 | port G_Ω **[M]** | (64 + 1 + 1 + 64) → 32 → 32 | ≈ 5,300 | replay |
| 12 | 𝓜 (in 𝒦): LRU 2 × 128 complex modes, innate moduli | inputs 35 + 3 + 64 + 6 + 32 | ≈ 330,000 | online fast heads + replay |
| 13 | 𝓜 heads: own body, own face, partner (action-blind), f_recv, lexical-body | 256 → 64 → (6, 23, 102, 6, 6) | ≈ 70,000 | replay |
| 14 | 𝒦 slots (maps) | as 9 | ≈ 13,000 | replay |
| 15 | concept layer | ≤ 64 centroids × 64 (states); PMI counts (states) | 0 | online |
| 16 | draft scorer head | 64 → 1 | 65 | replay |
| 17 | lexical projection | 384 → 64 | 24,600 | fixed random (innate) |
| | **total learned** | | **≈ 670,000** | |
| frozen | MediaPipe (×2: partner, own), Whisper-small, MiniLM (22.7 M), TTS, AEC | | | |

The mechanism ([M]) holds ≈ 225k parameters, mostly the REN and Π.

### 6.3 Objectives

- **𝓛_𝓜**, negative log-likelihood of all of 𝓜's heads. The partner head gets inputs with the agent's own outputs masked (action-blind).
- **𝓛_J**, the J of §2.11 by 𝓜 rollouts (Dreamer-style actor), with the partner exogenous. It trains Π, S_f's θ (REN, A, φ), the retrieval query and the draft scorer.
- **𝓛_own**, own-data fits of 𝓔, Π̃ (inverting Π on own samples) and the lexical-body head.
- **Anchors:** λ‖θ − θ₀‖², λ_n‖θ − θ_prev‖². Gradient clip G = 1.

Every constraint holds for every value of the free vector:
- the REN by direct parameterisation;
- A, R, Π, Π̃ and the c̃ encoder by normalisation (S_s's maps by max(‖W‖₂, ‖W‖_∞));
- the slot and μ writes by sigmoid gates and nonnegative weights;
- the wrap, filters and port high-pass are fixed.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms):**
  - MediaPipe on the partner ≈ 13 ms in its own process (the own-face instance runs only in babbling and replay sessions, not live);
  - P₀, P and the filters < 0.1 ms;
  - REN < 1 ms on CPU;
  - attention and the wrap < 0.1 ms;
  - S_s interpolation < 0.01 ms;
  - render 3–5 ms.
- **At 2 Hz:** S_s < 1 ms; 𝒦 (𝓜 ≈ 0.7 MFLOP) < 3 ms.
- **Per turn:**
  - MiniLM ≈ 10 ms per text, so 6 drafts ≈ 60 ms;
  - 6 rollouts of 60 steps ≈ 20 ms;
  - Claude: one API call returning 6 drafts, typically 1–3 s, outside the fast loop. The onset waits for it (R15). Earlier drafting starts at the partner's turn-end pulse.
- **Visible fast match:** 0.45 s plus about 80 ms of pipeline.
- **Memory online:** MediaPipe 0.3 GB, Whisper-small 0.5 GB, MiniLM 0.1 GB, TTS ≤ 1 GB, engine < 0.3 GB. Total < 2.3 GB.
- **Replay:**
  - S_f on 10-min 30-Hz segments, TBPTT 30 s, batch 16;
  - S_s and 𝓜 at 2 Hz;
  - < 2 GB, ≈ 30–45 min nightly on MPS.
- **Store:** 35 channels × 30 Hz × float16 ≈ 7.6 MB/h, so ≈ 1.8 GB for 30 days. After decimation, ≈ 0.5 MB/h.

## 7. Ablation predictions (Principle 5), from the properties

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the wrap (s read straight as y) | held concordance up to the knowledge's fidelity (H2: 0.906 on 1-min means); learning drives the fast face toward same-sign following | §3.2 |
| L at S_s's input, or the no-demodulation rule | event rate becomes a held dial: 1-min-mean slope on bursty partners rises above the slow cap (H5: 0.109) | §3.4 |
| the ℓ∞ structure of S_s | late-window held concordance can exceed 0.10 (H7: up to 0.265 at 60 min) | §3.3 |
| H_o (output high-pass of S_f) | S_f rectifies partner transients into held output; held concordance no longer ≤ 0.10 | §3.2 |
| the port's output high-pass | Claude's words can hold the face toward the partner (port DC up to 0.10, in phase when words track the face) | §3.7 |
| the reflection P, or κ_lat → κ | mirror copy on yaw, roll and gaze up to about 0.6 (critique K4) | §3.6 |
| the action-blind partner head | draft choice drifts toward replies predicted to make the partner quieter or smile (placation), visible as a rising correlation between the predicted partner-state change and draft choice | §3.11 |
| f_recv (self-simulated relief) | care acts unspecific; choice under high C ≈ choice at C = 0 | §3.12 |
| Π̃ replaced by another policy's inverse | C triggered by the wrong faces | §3.12 |
| crossed habits (own Π smiles under high V) | the partner's smiles raise C | §3.12 |
| R (partner input to S zero) | fast echo and face-driven concern vanish; word-driven care remains | §3.12 |
| the concept–snippet link (shuffle categories) | Claude's self-descriptions become state-independent (agreement between self-report words and category falls to chance) | §3.11 |
| slots → 2-d valence/arousal | partner × topic specificity gone | §3.17 |
| state tags in replay (S6) | partner-specific slot recall decays across nights | §5 |
| clean u in replay → noised release | learned fast signs collapse to θ₀ (H3: +0.0002) | §3.5 |

## 8. Weak points and falsifiers

### 8.1 Weak points (where a critic should attack)

1. **New weakest point: the partner's face has narrow expressive reach after the first seconds.**
   - What the bounds allow:
     - by construction, a held partner expression can move the agent's face by at most 0.15 of range in any direction (0.10 toward it);
     - the 4 s – 1 min band is nearly blind on the expressive side (|H_i|² + |L|² ≈ 0.08 at 30 s);
     - strong, sustained reactions come only from words and the agent's own body.
   - What it may look like: a person whose friend starts crying shows a strong, lasting face within seconds. This agent shows a strong flicker (≤ 0.49 against the partner, any direction, for ~4 s), says something caring at its next turn, and then holds a gentle concern.
   - Whether this reads as warm or as detached is the empirical question.
   - The knobs are innate and named: γ_s (held reach), τ_L (how fast the slow block sees), τ_o (how long fast responses last). Raising them trades directly against the held copy cap: held in-phase = 2κγ_s/(1 + γ_s).
2. **Claude's regulation shows on the face only briefly** (N4 forces the port; zero DC). A reappraisal changes the agent's body and words durably, but its face for only ~15 s. Mood shifts through words come from the *partner's* words (R14), not the agent's own.
3. **The common-cause route R14 is excluded from "copy" by definition.** Lexical words drive the face up to 0.8. Laughter, punctuation and timing are now removed from words, but a partner who narrates his own face ("I'm smiling") still drives an appraisal display. I hold that this is understanding; it remains the definitional seam.
4. **Care depends on learned self-simulation.** f_recv must learn, from the agent's own life, what relieves it, and the lexical-body head must learn which words go with which own body. Early on (few nights) care is driven by Π₀ and the innate 𝒟 only.
5. **Cross-world shaping by weights** (§3.10c) is bounded but not by a copy-specific number. An agent raised by a chronically sad partner may become more somber in response to words. I call that temperament (C9); a critic may call it slow copying.
6. **Assumptions §3.15**, especially ASR lexical invariance and TTS target realisation.
7. **Lateral gaze following is weak** (≤ 0.056 lagged).

### 8.2 Falsifiers (state-level, once built)

- **F1.** Under partner-swap and segment-shuffle surrogates, with words fixed: the agent's held (10-min) in-phase regression on any counterpart channel exceeds 0.10 (+ port 0.005), or the 1-min-mean in-phase exceeds 0.21 at any time after onset, or the zero-lag in-phase gain exceeds 0.198 (+ the a-route). Each means an uncounted route.
- **F2.** A decoder on S_s's states recovers the partner's held level, while the face does not follow it beyond F1's bounds. This is the *intended* outcome; if the decoder fails (corr < 0.9 on 1-min means), the knowing claim is false.
- **F3.** The crossed-habits manipulation does not change which partner faces raise C (contradicts §3.12).
- **F4.** Draft choice correlates with 𝓜-predicted changes in the partner beyond what C and words explain (the action-blind head leaks; contradicts §3.11).
- **F5.** μ coordinates lose autocorrelation faster than e^{−Δ/τ_j}.
- **F6.** Removing H does not reduce joint-pattern novelty (C7).

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (all Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Report 4, Q16, Q17, Q18 and answer, Q19, Q20 | in full |
| DECISIONS.md D78, D80 | in full |
| research/foundations/designs.md | in full |
| design-cayley-ledger.md revision 1, including critiques 1a, 1b and the answer | in full |
| critique-design-cayley-ledger-routes.md; critique-design-cayley-ledger-novelty.md | in full |
| sims/critique-cayley-routes/out.txt; mirror_lateral.py | out.txt in full; K4 script in full (reused in H4) |
| non-copying-dynamics-synthesis.md (C1–C10); self-other-control-synthesis.md; directional-influence-synthesis.md | in full |
| Revision 1's sources (Revay et al. note, Mironov note, influence-bounds and capacity syntheses) | as recorded in revision 1 §9; not re-read |
| **Not read, named only as pointers:** path-specific objectives in the causal-incentives literature (Farquhar, Carey & Everitt); peak-to-peak (ℓ∞) gain of positive systems; Susskind et al. 2008 on expression function; infant expression repertoires (Oster) | nothing in the design depends on them; N4, §3.3 and Claim C are argued here and checked in H6–H7 |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.** The parts are known:
- the wrap is a robust REN with a conic sector;
- the filters are classical;
- ℓ∞ small gain and positive filters are textbook;
- 𝓜 is an LRU world model with Dreamer-style actor training;
- slots and retrieval are attention;
- the concept layer is DP-means plus PMI;
- care-as-own-drive at another's inferred state is a version of simulation-theory empathy.

**Clause 2 (a changed invariant, a derived update, deleted scalars): arguable, probably not met.** Three composition results are new to this project and, as far as I have read, not stated elsewhere:
1. **A held-level one-sided bound that a knowing slow state cannot escape.** It is the banded wrap (zero-DC fast block between two high-passes; slow block behind a low-pass) plus two necessity results:
   - without the no-demodulation rule, event rate becomes a dial (H5);
   - without the ℓ∞ structure, ℓ₂ sectors allow late in-phase holds (H7).
2. **N4:** no per-path or W₂-mean cone contains a discrete choice, so the discrete route must be a zero-DC magnitude allowance. This turns the project's recurring "uncounted route through Claude" into one named port with a proved held bound of 0.
3. **The empathic drive with an action-blind partner model:** care that is satiable, specific to the agent's own body model, and has no gradient through the partner's state.

**What it deletes from revision 1:**
- the release noise σ_s and its ledger ε_L, the scalar the novelty critic named "the knob";
- the "verbal and meta account" with its noise-free timing;
- Check A, which blocked S4.

**What it adds:** two innate gains (γ_f, γ_s) in place of one, and one port gain a_Ω.

**My honest verdict:** a careful recombination, now with no concrete failure I can find, and with the project's knowing/moving distinction made exact.

---

## Revision 2 history (2026-11-26): each critic finding and how it is closed

Revision 1's critiques are recorded in full in `design-cayley-ledger.r1.md` (section "Critiques 1a and 1b and the answer"). Each finding, and what revision 2 does about it:

| # | Finding (critic) | Closed by | Where |
|---|---|---|---|
| 1a-1 | slow mind and fibre blind to the partner (reliability 1.35·10⁻⁴; shout SNR 0.16; sad hour 57%); learned signs ±0.0002; P3, long-term goal, C4, C5 and D78 failed in practice (routes) | the release noise is removed. The slow mind sits inside the wrap and knows held levels (H2a r = 0.994); 𝒦 knows everything at full rate; replay stores clean u, so the fast block learns signs (H3: +0.135 / −0.238 against +0.0002) | §2.3, §2.7, §3.2, §3.5 |
| 1a-2 | speech rate leaks through noise-free turn times (r 0.74–0.98) into own voice, uncapped (0.8) | timing is in u: rate, pause and latency are counterpart channels inside the wrap. The TTS takes rate, pause and latency only from y. S's lexical input is turn-indexed with a per-turn leak, so no state of S integrates time between utterances. Knowing the rate (𝒦) is allowed | §2.1, §2.5.6, R5, R13, R15 |
| 1a-3 | held-level cost grows with duration for non-additive signals; dropouts add edges | moot: there is no ledger. The cone is a property of the map for every u, additive or not. Dropouts are sample-and-held anyway | §2.2 |
| 1a-4 | mirror copy on yaw, roll and horizontal gaze at 0.58 | reflection P before the wrap and κ_lat = 0.05: mirror ≤ 0.031–0.045, anatomical ≤ 0.078 (H4); cross ≤ 0.20 per pair | §3.6 |
| 1a-5 | laughter tokens and punctuation in ASR text, uncounted | ASR normalised to lexical tokens; punctuation from an innate lexical rule; laughter, sighs and crying as continuous burst channels inside the wrap; Claude's text stripped before the TTS; non-lexical sound only from y | §2.2, §2.8.5, R6, R11 |
| 1a side | the c-only path shares γ_k with the partner path | sign and context live in 𝓡 and A; c̃'s w-independent output is bias-free | §2.4, §2.10 |
| 1a §6 | C7 only self-repetition | H on the joint pattern [own display, ŵ] | §2.4, C7 |
| 1b 1.1 | "harm" undefined; "stance code" undefined; fixed name list | harm removed (V has two defined innate inputs); stance is the slot read, defined in §2.5.4; the name list is P₀, unchanged until S4 | §2.5 |
| 1b 1.2 | P3 neither real nor essential: R a projection on commands; rotation-invariant after replay; mimicry bypasses R; affect half cut; Check A blocks S4 | 𝓔 is now an appearance map fitted from self-observation (B3 allows S4); b̂_p = Π̃(R·x) infers the partner's *body*; it feeds the innate 𝒟, so no refit undoes a rotation; the echo runs on Φ_R; the partner's face drives the agent's C, V and A | §2.2, §2.4, §2.5.1, §3.12 |
| 1b 1.3 | Claude blind to the face, ≤ 2 bits per turn, no naming | 𝒦 steers retrieval with full-rate knowledge, b̂_p and C; 6 drafts (2.6 bits) plus retrieval; naming through concept-weighted snippets | §2.8 |
| 1b 1.4 | A and V fed by the partner make draft choice placate (P6); I satiable only weakly | action-blind partner head: no rollout represents an effect on the partner; partner signals are evidence only; I is predictive variance above a floor | §2.7, §2.11, §3.11, §3.13 |
| 1b 1.5 | "stricter than P7" inaccurate | stated plainly: lexical transcript and snippets go to the API | §5 |
| 1b 1.6 | speech rate released noise-free | as 1a-2 | — |
| 1b 1.7 | P10: an assembly of seven losses; Π has no objective | one model (𝓜, with own-data heads) and one objective J; Π, S_f, retrieval and scorer all minimise J; the residual innate rules are listed as assembly | §2.11, §6.3 |
| 1b §2 | not an emotional agent (silent sad user never noticed; no smile back held; not moved by a sad story; no reaction to words; fast route unlearnable; no vocal convergence; thin interoception; no concepts) | C from 𝒟(b̂_p) (face and words) notices a silent sad partner within 1–2 min; a held smile gets ≤ 0.10 back; words move C, A and V; S_f learns from clean u; held vocal convergence up to 0.10 (C9); concepts and naming. Strong held reactions to the *face* remain impossible (§8.1.1) | §3.11 |
| 1b §3 | novelty: wrap = REN; ledger = Le Ny & Pappas; both clauses fail | accepted for the wrap. The ledger is removed. The new composition results are stated, and the verdict stays recombination | §10 |
| 1b lead | contraction forbids multistability, not slow memory, so moods can sit inside the bounded path | adopted. Moods, slots and body are slow contracting positive filters inside S_s. Two things were added that the lead did not foresee and the checks show are necessary: the no-demodulation rule (H5) and the ℓ∞ slow block (H7) | §3.2–3.4 |

**Status:** revision 2; to be critiqued (routes and copying; principles, emotional fitness and novelty).
