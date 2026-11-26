# Cayley–ledger core: the partner's face is wrapped once at the boundary, and the rest of the mind is only told

Seventh design of the S0 cycle. Written 2026-11-26 under questions.md Q16, Q17 (as relaxed by Q19: precise object, convincing arguments, effort on making the mechanism concretely work), Q18 and its answer (DECISIONS.md D78), the constraints C1–C10 of research/non-copying-dynamics-synthesis.md, and the two-part answer of Report 4. Algebra checks: `foundations/sims/design-g/checks.py` (G1–G10, `python3 -I checks.py`, numpy and scipy, about 30 s; output in `out.txt`). They check this design's own inequalities on constructed instances. They are not evidence about behaviour or people (brief: no toy worlds).

**Status:** new, not yet critiqued.

## 0. Summary

- **Core object.** Everything that reads the partner sits inside one boundary module 𝓑. 𝓑 has exactly three kinds of output. Route completeness is the single structural check that nothing else imports camera, microphone or transcript data.
  1. **The fast fibre.** A face and voice contribution y^F = 𝒞_K(S_θ)(u). Here 𝒞_K is a **Cayley wrap**, y = 2K^{1/2}S(w) with w = K^{1/2}u − S(w), around an arbitrary learned strictly causal contraction S_θ. The fibre is forgetful and has no read-back.
  2. **The ledger release.** A level-private stream X^s for the rest of the mind: an innate zero-DC filter, plus Gaussian noise, applied to a linear own-body reading of the partner.
  3. **A verbal and meta account**: words, turn times and identity. It is accounted, not hidden.
- **Part (2), the concordance ceiling, by construction.**
  - The Cayley transform maps γ-contractions one to one onto operators in an incremental **conic sector** with centre m = −2γ²K/(1−γ²) and radius r = 2γK/(1−γ²).
  - So, for every parameter value:
    - zero-lag in-phase gain ≤ (m + r) = 2γκ/(1+γ) in *every* partner direction (per channel, every subspace, the whole face);
    - incremental gain ≤ |m − r| = 2γκ/(1−γ);
    - lag-τ concordance ≤ r + m·ρ_u(τ), where ρ_u is the partner's own autocorrelation.
  - With κ = 0.30 and γ = 0.5 these are **0.20 in phase, 0.60 in any direction, 0.40 at any lag for broadband partners**.
  - One-sidedness is not closed under series composition (two flips make a copy), but contraction is. The whole fast computation lives inside S, with as many internal sign flips as learning likes, and is **wrapped once**.
- **Part (1), one budget.**
  - The neighbouring relation is a held-level offset of full channel range on any expression direction, over a window of any length.
  - The release filter has zero DC gain, so one held episode costs a constant ε_L(2) = 0.116, however long it lasts and however long the agent lives. No budget is consumed over time, so care is not forbidden.
  - Every slow route (mood, memory, slots, learning, replay, Claude's draft choice and retrieval, body variables, the display of the agent's own state) is post-processing of the release. So any slow statistic of the agent correlates with any one held partner level by at most 0.25.
  - The fast fibre cannot hold a level: zero DC inside S, and contraction.
- **Persistent state.** Linear multi-time-scale modes (2 min to 3 days) and content-addressed slots (30 days). They have no wells, so there is no noise-driven switching. Retained capacity is about 330 bits after 1 h for the mood ladder alone, and about 2·10⁴ bits after a day in the slots (G6, under a stated write-SNR assumption).
- **Novelty verdict (author).** Recombination by clause 1. Every primitive is known:
  - Zames' loop transformation / Revay's robust REN with a conic-sector IQC;
  - the Gaussian RDP mechanism;
  - LRU state-space models;
  - attention.

  Two composition results are new to this project and, as far as I have read, not stated elsewhere: the **wrap-once closure plus its necessity results**, and the **forgetful-fibre / level-ledger split**. Together they delete the scalars and typing rules of earlier designs instead of adding caps (§10).
- **Weakest point.** The slow mind learns almost nothing about the partner's face from the face itself (per-episode SNR ≈ 0.27 for a full-range change). Care, relationship and history must come mostly from words, identity and statistics over many episodes. Whether that is enough is an empirical question. It may be the price of "no slow state tracks the held face" (§8).

## 1. Plain-language intuition

Picture the agent as a house with one door. Everything the partner does arrives at the door.

At the door stands a reflex: it can move the agent's face back at the partner at once. It may smile back a little, frown a little, look where the partner looks, or nod at a pause. But it has no memory of more than a few seconds, it writes nothing down, and it cannot see held expressions, only changes. Its arithmetic is arranged so that, however it learns, its echo is always smaller in the copying direction (at most a fifth of the partner's movement) than in any other direction. The arrangement makes a reflex chain that turns the face over twice still land on the small side.

Everything else in the house (moods, memories, the relationship, how the agent chooses what to say) is never shown the partner's face. It is handed a note from the door: a blurred, change-only, noise-covered reading of the partner, written in the agent's own muscle coordinates. The note is blurred so much that no part of the house, however clever and however long it reads, can tell whether the partner has been holding a sad face for an hour or not, beyond a small margin.

It can still tell what the partner says, who the partner is, and what the partner tends to do over many episodes.

So the agent:
- reacts to the partner's face the way people do: quickly, partly, and in context;
- has moods of its own that persist;
- understands the partner mainly through words and a long acquaintance;
- cannot drift into wearing the partner's face, because neither half of the house can do it.

## 2. The object

### 2.1 Channels, time and innate constants

Time is discrete at the camera rate, f_s = 30 Hz (Δ = 1/30 s), except where stated.

**Counterpart channels (the copy metric is defined on these).**
- **Face and gaze: n_F = 18.** Sixteen face synergies:
  - brow inner raise, brow outer raise, brow lower;
  - upper-lid raise, lid tighten;
  - cheek raise, nose wrinkle;
  - lip-corner pull, lip-corner depress, lip stretch, chin raise, lip press, dimpler;
  - head pitch, head yaw, head roll.

  Plus 2 gaze angles.
- **Voice: n_V = 4,** at phrase level: F0 level, F0 range, energy, speech rate.
- **The innate correspondence P₀** maps MediaPipe's 52 blendshapes plus head pose plus gaze to the 18 coordinates. It is fixed: left/right averaging and grouping. It is the same map for partner and agent.
- **Normalisation.** Each channel is scaled so that its innate nominal range is [0, 1].
- **Partner features:**
  - u_t ∈ [0,1]^{18} for face and gaze;
  - ū_n ∈ [0,1]^4 for voice, the n-th partner phrase. ū comes from a GeMAPS-lite analyser, after echo cancellation, and only while the agent's TTS is silent (plus a 200-ms tail).

**Non-counterpart channels.**
- **Articulators (n_A = 5):** jaw open, lip funnel, pucker, mouth close, lip roll.
- **Blink (1).**
- The copy metric excludes articulators. Their route is bounded separately (§3.6, R8).

**Non-counterpart partner signals.** a_t ∈ [0,1]³:
- the audio-onset envelope (the startle input);
- the partner's speech envelope;
- partner voice activity.

**Innate constants (compiled in, not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| κ_k | 0.30, all 18 face/gaze and all 4 voice channels | wrap weight K = diag(κ) |
| γ | 0.5 | gain of the contraction S |
| b = 2γ/(1+γ) | 0.667 | in-phase ratio. **In-phase cap bκ = 0.20** |
| m = −2γ²/(1−γ²), r = 2γ/(1−γ²) | −0.667, 1.333 | disc centre and radius. Per channel mκ = −0.20, **rκ = 0.40** |
| L = 2γκ/(1−γ) | **0.60** | incremental gain cap per channel |
| φ₀, λ_φ, G | 1.0, 0.5, 1.0 | innate pull and gradient clip on the per-channel gain logits (§2.9) |
| τ_in | 4 s | innate high-pass at the input of S (zero DC) |
| ℓ_echo | 0.45 s | innate echo lag of the reflex prior S₀ |
| filter bank | high-pass τ_in, then band-passes centred 0.15, 0.4, 1.0, 2.5, 4.5 Hz plus one 0.05–0.15 Hz band; each band scaled by 1/√6 | time-scale coordinates inside S |
| M(s) | ω_n = 2π·4 rad/s, ζ = 0.8, peak gain 1 | muscle filter, *inside* S for the fibre |
| ℓ_a | 0.15 per face channel; 0.6 onto blink | Lipschitz bound of the a-route (startle, backchannel, envelope gating) |
| f_r | 2 Hz | ledger release rate |
| h_s | high-pass τ_h = 3.2 s, then low-pass 1 Hz | release filter, zero DC |
| σ_s | 7.1 per coordinate per release | release noise |
| Δ_L | 1 (unit-norm offset in normalised counterpart space) | protected held-level size |
| ε_L(2) | 0.116 | per held episode, any duration (G5a) |
| ρ_L | 0.25 | held-level correlation bound for any slow statistic |
| ω_max | 0.30 | echo guard: maximum phoneme-trigram overlap of a draft with the partner's last two utterances |
| V_A | 0.8 | viseme amplitude cap on articulators |
| P_txt | 0.15 | cap on text-driven TTS prosody (normalised voice units) |
| A_k | 0.8 | per-channel range of the agent's own display |
| c_F | 2% of the resting energy draw | flat energy tax of the fast fibre (partner-independent) |

### 2.2 The boundary 𝓑 and the one structural check

𝓑 is the only code that imports camera frames, microphone audio, ASR output or any feature computed from them. Its outputs are exactly the following:

| Output | To | Partner-dependence |
|---|---|---|
| y^F_t ∈ R^{18} (fast face/gaze contribution, already muscle-filtered) | the renderer's summing node, write-only | the face wrap 𝒞_K(S_θ) |
| y^{FV}_n ∈ R^4 (phrase prosody offsets for the agent's next phrase) | the TTS control, write-only | the voice wrap (§2.3, voice) |
| y^a_t (startle blink, backchannel nod) | the renderer, write-only | the a-route, Lipschitz ℓ_a |
| floor flag f_t ∈ {may speak, hold} | the TTS scheduler | partner VAD, memoryless beyond 1 s (R10) |
| X^s_j ∈ R^{17}, at 2 Hz | the rest of the mind | the ledger mechanism (§2.4) |
| verbal and meta account Q | the rest of the mind and Claude | per partner utterance: the transcript text (to Claude) and a 64-d embedding (to the mind); turn start and end times (100 ms grid); one identity token per session |

**Check (A).** No module outside 𝓑 reads a camera, microphone or ASR stream, or anything derived from them except the outputs above. No module reads y^F, y^{FV}, y^a or the rendered face or voice back: the agent never sees or hears itself. Four places need care:
- the microphone path removes own speech by echo cancellation plus a half-duplex gate;
- the self-model is trained on the own-tagged display y^own only (§2.9);
- replay stores only X^s, Q and own variables, never u, ū or a;
- Claude receives only the transcript and texts chosen by the mind (§2.8).

This is one property of the code graph: an import check plus a read-back check. It replaces the route-by-route inventories that every earlier critique broke.

### 2.3 The fast fibre: a Cayley wrap around a contraction

**The wrap (face).** Let S_θ be a strictly causal operator from w ∈ ℓ₂(R^{18}) to ℓ₂(R^{18}), with "context" inputs c and own innovation d that are not partner-raw (defined below). Assume S_θ has incremental ℓ₂ gain ≤ γ in w, for every fixed (c, d) path and every θ, over every causal truncation. The fibre is:

  s_t = S_θ(w_{<t}; c_{≤t}, d_{≤t}),  w_t = K^{1/2}u_t − s_t,  y^F_t = 2K^{1/2}s_t.

Strict causality (S sees w up to t − 1; one frame, 33 ms) makes this an explicit recursion. There is no algebraic loop and no equilibrium solve. Read as operators, y^F = 2K^{1/2}S(I + S)^{−1}K^{1/2}u: the Cayley transform of S, weighted by K.

**The contraction S_θ (what is inside).** S_θ is built so that its gain bound holds for every θ:

  S_θ(w) = diag(γ_k(θ)) · A(c) · M ∘ 𝓡_θ( [Φ_R(F w), a-features], c, d ),  γ_k(θ) = γ·σ(φ_k), ‖A(c)‖₂ ≤ 1.

1. **F: the innate filter bank.**
   - It applies the zero-DC high-pass τ_in, then 6 bands per channel, plus the innate lag line (taps 0.15, 0.3, 0.45, 0.6, 0.8 s).
   - It is scaled to H∞ gain ≤ 1, and it carries the one-frame delay.
   - The band index is the time-scale coordinate.
2. **Φ_R: the own-body reading.**
   - The learned linear map R ∈ R^{12×18} is applied per band (§2.5). It is spectrally normalised, ‖R‖₂ ≤ 1.
   - The partner reaches the fibre's learned core only in the agent's own 12 face-synergy coordinates.
3. **𝓡_θ: the core.**
   - An acyclic robust REN (Revay, Wang & Manchester; direct parameterisation), with Lipschitz bound 1 from its partner input.
   - Its other inputs:
     - context c (non-partner-raw);
     - own innovation d (innate band-limited noise, 2.6–6.5 Hz, sd 0.04, used for micro-motion);
     - the a-features with their own scale.
   - All gating, recurrence, sign choice and cross-channel structure is learned here.
4. **M: the muscle filter.** Peak gain 1, no feedthrough, so the rendered fast contribution *is* the wrap's output.
5. **A(c): need-conditioned attention.**
   - Each output channel k forms a softmax over the 32 REN outputs. The query is q_k(c), from the agent's needs and expected body change. The keys are learned embeddings of the REN output slots.
   - The matrix is rescaled to ‖A‖₂ ≤ 1.
   - Partner content does not enter the weights, only the values, so the bound holds.
6. **diag(γ_k(θ)):** learned per-channel gains γ_k = γσ(φ_k) ≤ γ.

Since F, Φ_R, M and A have gain ≤ 1, 𝓡 has Lipschitz bound 1 in its partner input, and γ_k ≤ γ, the composition has incremental gain ≤ γ in w for every θ and every (c, d) path. Contractions compose. No sign bookkeeping is needed inside S.

**The innate prior S₀ (θ = θ₀, the reflex).** 𝓡 at θ₀ realises four reflexes:
1. **A transient positive echo** on lip-corner pull, cheek raise, brow inner/outer raise and head pitch: the high-passed partner channel delayed by ℓ_echo = 0.45 s, through M.
2. **Gaze following** at the same lag.
3. **Envelope gating of own micro-motion:** own d on the head channels × (1 + 4·env_{2.6–6.5 Hz}(partner head))⁻¹. Lipschitz ≤ 0.1 in w.
4. **A pause-triggered nod** from a (partner VAD offset → head pitch pulse).

At φ₀ = 1, the per-channel γ_k = 0.37, so the innate in-phase cap is 0.16 (G7).

**Context c.** c is a 64-d vector computed outside 𝓑 from things that are not partner-raw:
- the mind's state (𝓜 readout, μ, the attended slot; all post-processing of X^s and Q);
- the current utterance embedding from Q;
- role (own TTS active; partner turn state from Q's turn times);
- own body b.

Through c, context and the learned relationship set each channel's response sign and size within 0.5–1 s (the gate time constants inside 𝓡).

**The wrap (voice).** The same construction runs in the phrase index n:
- input: the partner's last-phrase prosody ū_n, high-passed across phrases (innate, zero DC over phrases, τ = 3 phrases);
- output: the agent's next-phrase prosody offset y^{FV}_n;
- S_V: a small REN over phrase index with gain ≤ γ and the same κ, γ.

The partner's face never enters S_V (the face reaches the agent's voice only through the ledger), and the partner's voice reaches the face only as a-features.

### 2.4 The ledger: one release, one neighbouring relation

**Release mechanism 𝓢.**

  X^s_j = D_{2 Hz}[ h_s ∗ ( R u , R_V ū , env_audio ) ]_j + n_j,  n_j ~ N(0, σ_s² I₁₇) i.i.d., j = release index.

- R u is 12-d; R_V ū is 4-d (R_V spectrally normalised, held between phrases); env_audio is 1-d (normalised).
- D_{2 Hz} decimates after the 1-Hz low-pass in h_s.
- The noise is drawn from OS entropy inside 𝓑, added in float64, and nothing rounds after it (Andrés et al.'s rounding hazard).
- The noise values are never stored or exported.

**Neighbouring relation (innate).**
- P ~_L P′ iff P′ = P + Δ_L·v·1_W on the nonverbal counterpart stream (face, gaze, voice prosody, audio energy), for any unit direction v and any window W of any length.
- Words, turn times and identity are identical in P and P′. Offsets that leave the normalised range are clipped by the physical face, which only lowers the sensitivity.

**Ledger accounts.** One accountant, at one boundary:

| Account | Relation | Cost | What is claimed |
|---|---|---|---|
| nonverbal level | ~_L | ε_L(α) = αΔ_L²‖[R,R_V,1]‖²·E_h/(2σ_s²), with E_h = 5.85 (two edges of the filter's step response, sampled at 2 Hz; G5a). ε_L(2) = 0.116 | everything outside 𝓑 is (α, ε_L(α))-RDP with respect to one held episode of any length |
| verbal | one utterance changed | ∞ (released without noise) | nothing. Meaning is meant to be heard |
| meta | turn times; identity | ∞; one discrete token per session | nothing beyond the counts |

**Why this neighbouring relation solves the "vacuous over an hour, or forbids care" dilemma.** The cost of a held episode is set by its two edges. A zero-DC filter removes the hold itself, so the cost does not grow with the duration of the hold, and different episodes are different neighbouring pairs. Nothing is spent over time, and nothing needs to halt.
- What is hidden is any *one* held level, however long it lasts.
- What is not hidden is a pattern over many episodes (group privacy: k episodes cost k²ε_L at worst). So the mind can learn that this partner smiles often, which is partner history over minutes. It cannot learn whether the partner has been holding a sad face since 10 am.

### 2.5 Reading the other through the agent's own body: R

- **The own expression map.** 𝓔: own display state → own face. It is learned in replay from the agent's own life: pairs (z_own, y^own), the own-tagged display only.
- **R** is the regularised linear inverse of its Jacobian at rest, R = (JᵀJ + λ_R I)⁻¹Jᵀ, with J = ∂𝓔/∂z ∈ R^{18×12} and λ_R = 0.05, then spectrally normalised. It is fitted only on the agent's own data. No partner data and no partner labels are ever used.
- **R_V** is the same construction for voice.

**Statement.** For a partner face u:
- R u is the own synergy state whose expression best explains u, in least squares at the agent's operating point.
- If u = J z + u₀ for some own z, then R u = z up to the ridge.
- Components of u in ker R (expressions the agent's own body cannot make) are released as nothing: for offsets v ∈ ker R, X^s has *exactly* the same law under P and P′.

### 2.6 The rest of the mind (everything outside 𝓑)

All of it is post-processing of (X^s, Q, own variables, own noise).

**Body and drives.**
- b ∈ R⁵: energy E, arousal load A, information need I, aversive load V, motor habituation H. All are innate variables with innate dynamics and set points b*.
- Drive: 𝒟(b) = Σ_i w_i ψ(|b_i − b_i*| − δ_i)₊, with ψ(x) = x² and dead-bands δ_i. Weights w = (1, 0.7, 0.5, 1, 0.4).
- Dynamics (per second):
  - **Energy E:** ė_E = −(c_rest + c_speech·[own TTS] + c_F) + r_rest·[low activity]. The fast fibre pays a *flat* tax c_F, never in proportion to its partner-driven output.
  - **Arousal load A:** driven by the magnitude of 𝓜's prediction error on X^s and on the own body, and by audio energy in X^s. It decays with τ = 3 min.
  - **Information need I:** rises at 1/30 min⁻¹. It is lowered only by the learning progress of 𝓜 on *own-body* prediction (the drop in its own-body loss), never by surprise in the partner's words or face.
  - **Aversive load V:** driven by loud-audio energy in X^s and by own-predicted harm. It decays with τ = 10 min.
  - **Motor habituation H:** rises with the 2-min autocorrelation of the own display y^own (self-repetition) and decays with τ = 2 min.

**World model 𝓜.**
- Inputs: X^s, Q events, b, y^own and role.
- An LRU stack of 2 layers × 128 complex modes. Each layer holds 128 complex modes, carried as 256 real coordinates. Updated at 2 Hz and at events.
- The mode **moduli are innate**, log-spaced to give time constants from 1 s to 2 min. Phases, couplings and heads are learned.
- Heads predict the next X^s, the next own body b, and the next own display.

**Mood ladder μ ∈ R^{128}.** Eight groups of 16 coordinates. Group j has innate time constant τ_j = 2 min·3^j (2, 6, 18, 54 min, 2.7, 8.1, 24, 73 h):

  μ_j(t+δ) = e^{−δ/τ_j} μ_j(t) + (1 − e^{−δ/τ_j}) W_j g_j(t) ⊙ 𝓜-readout(t) + σ_μ √(1−e^{−2δ/τ_j}) ξ_j.

- g_j is a learned write gate.
- σ_μ is the own noise: its stationary variance is 1% of the input-driven variance.
- These are linear leaky modes. They have no wells.

**Relationship and episode slots.**
- M = 128 slots (k_m ∈ R^{64}, V_m ∈ R^{128}), holding the expected own-body change, its precision, and a stance code.
- Keys combine the identity token, a topic embedding from Q, and an episode context.
- **Writes** are attention-weighted, with the query from 𝓜's state and the current need gradient ∇𝒟(b). Slot values decay with τ_slot = 30 days.
- **Reads** are need-conditioned attention: the query q = W_q[∇𝒟(b), expected Δb, 𝓜-readout] over the keys.

**Episodic store.** Segments of (X^s, Q embeddings, own state snapshots), plus the raw transcript text for Claude, tagged with the state at storage.

**Own display.**
- y^own = Π_ψ(μ, 𝓜-readout, attended slot, b, role) ∈ [0, A_k] per channel, over the 18 counterpart, 5 articulator and 1 blink channels. It is muscle-filtered by M outside 𝓑.
- Π_ψ is a 2-layer MLP with a per-channel output range A_k = 0.8, and Lipschitz ≤ A_k in each input group (spectral normalisation).
- This is how the agent's own state, including its appraisal of what was said, reaches its face within 1–2 s.

### 2.7 Output assembly

- **Face:** face_t = M ∗ (y^own + y^vis + y^a_blink) + y^F_t, with articulators y^vis from visemes (§2.8).
- **Voice:** TTS prosody targets per phrase = y^{own,V} (from Π_ψ) + y^{FV}_n + text-driven prosody, capped at P_txt.
- The renderer applies nothing further. The muscle filter for the fibre is already inside S (§2.3), which is why the wrap's guarantee is a guarantee on the rendered face.

### 2.8 Claude

1. **Drafts.** At each agent turn, Claude, frozen and called through the API, receives:
   - the transcript;
   - up to 3 retrieved snippets: raw past dialogue text, chosen by the mind's need-conditioned attention over the episodic store with an ALiBi-style recency bias.

   It returns K = 4 alternative replies. The prompt is constant. It never contains body values, latents, labels or anything about the agent's state.
2. **Selection.**
   - Each draft's 64-d embedding enters the mind through Q. For each draft i, the mind rolls 𝓜 forward with "I say draft i" and scores it: s_i = −E[Σ_{30 s} 𝒟(b̂)].
   - Drafts that violate the echo guard (phoneme-trigram overlap > ω_max with the partner's last two utterances) are excluded first, by an innate rule.
   - The choice is argmax(s_i + Gumbel own noise at temperature 0.1).
3. **Speech.**
   - Phonemes → visemes on articulators (amplitude ≤ V_A).
   - TTS prosody: §2.7. Timing is set by the floor flag f_t.
4. **Regulation and reinterpretation.** Claude's chosen text is the agent's own utterance. Its embedding re-enters the mind through Q, and 𝓜 appraises it. This is how Claude "names, reinterprets and regulates": it chooses words, and words change the state. The state never reaches Claude as numbers or words.

### 2.9 Learning, and what it may read

- **Online.** Only states change (𝓜, μ, slots, b), plus 𝓜's fast heads, by one SGD step every 10 s on X^s, Q and own data. No weight reads u, ū or a.
- **Replay, nightly.** All weights are updated from the episodic store (X^s, Q, own variables only):
  - 𝓜 by predictive likelihood;
  - Π_ψ and 𝓔 (and so R) from own data;
  - the slot and μ write gates;
  - the draft scorer;
  - the fibre's θ (the REN, the attention queries, the φ_k).
  The fibre's training signal is to predict the agent's *own* display one to two seconds ahead from the released partner stream and the context: the reflex learns to anticipate its own appraisal. Inputs are X^s, upsampled, with noise augmentation. The target is never the partner.
- **Innate stop on the fibre.**
  - Every replay gradient is clipped to norm G = 1.
  - The per-channel gain logits are pulled to φ₀ with λ_φ = 0.5.
  - All other fibre parameters are pulled to θ₀ with λ = 0.5.
- **Consolidation (temperament).** Each night's weights are pulled to the previous night's with λ_n = 0.01 per night, against a learning rate that gives a 100-night effective time constant.

### 2.10 The one core (Principle 10)

The single objective is homeostatic. The agent's choices (draft selection, the attention queries, write gates, own display policy) minimise J = E[∫ 𝒟(b_t) dt]. They do so under one world model 𝓜, fitted by predictive likelihood of the agent's own body and its released percepts. Two innate structural constraints hold throughout:
1. **(W)** the partner's fast influence is 𝒞_K(S_θ) for some contraction S_θ;
2. **(L)** everything else sees the partner only as X^s and Q.

How the components follow:
- **Homeostasis** is 𝒟.
- **Curiosity** is the satiable body variable I, satiated by own-body learning progress.
- **Valence** and **arousal** are read out of 𝓜 as −E[d𝒟/dt] and E‖ḃ‖ over the next minute. They are not set.
- **Mimicry** is the wrap's prior S₀ plus learned anticipation of own display.
- **Reading others** is R inside both the wrap and the release.
- **Regulation** is Claude's drafts, chosen by J.
- **Replay** fits 𝓜 by the same likelihood.
- **Anti-repetition** (C7) is I, whose satiation falls when the joint pattern repeats.

## 3. Properties, each with an argument

### 3.1 The wrap is exactly a one-sided conic sector, for every parameter, through any internal composition

**Claim W.** Take any S strictly causal with incremental gain ≤ γ < 1 in w (for fixed c, d) on every causal truncation. Write Δ for the difference of two runs with the same (c, d) and partner inputs u, u + Δu, and ⟨·,·⟩ for the inner product over [0, T]. Then for every T:

- (W1) ⟨Δy, Δu⟩ ≤ b·⟨Δu, KΔu⟩, with b = 2γ/(1+γ). *In every partner direction:* single channel, any subspace, the whole face.
- (W2) ‖Δy_k‖ ≤ 2√(κ_k κ_max)·γ/(1−γ)·‖Δu‖ = L_k‖Δu‖.
- (W3) Conic form: ‖ŷ − m v̂‖ ≤ r‖v̂‖, with v̂ = K^{1/2}Δu, ŷ = K^{−1/2}Δy, m = −2γ²/(1−γ²) and r = 2γ/(1−γ²).
- (W4) Conversely, every operator satisfying (W3) is the wrap of a γ-contraction. The parameterisation is complete for the sector.

**Argument.** Put x = ΔS (= Δs) and z = Δw. Then Δv = K^{1/2}Δu = z + x and Δy = 2K^{1/2}x, with ‖x‖ ≤ γ‖z‖ on every truncation.
- (W1): ⟨Δy,Δu⟩ = 2⟨x, z + x⟩ and ⟨Δu,KΔu⟩ = ‖z + x‖². Then b‖z+x‖² − 2⟨x,z+x⟩ ≥ 0 reduces, after multiplying by (1+γ)/2 and writing ‖x‖ = tγ‖z‖, to γ‖z‖²(1 − t)(1 + tγ) ≥ 0 at the worst angle.
- (W3): expanding ‖2x − m(z+x)‖² − r²‖z+x‖², the cross term ⟨x,z⟩ has coefficient −2[(2−m)m + r²] = 0. What remains is ((2−m)² − r²)(‖x‖² − γ²‖z‖²) ≤ 0 (checked symbolically for these m, r).
- (W2) follows from ‖z‖ ≤ ‖Δv‖/(1−γ).
- (W4) is the inverse Möbius map, S = Ĝ(I − Ĝ)⁻¹ with Ĝ = ½K^{−1/2}GK^{−1/2}.

G1 checks (W1)–(W2) on three families:
- pure delays with orthogonal mixing (ratio 0.47 of the 0.667 cap);
- two first-order stages with **two sign flips in series** (0.61 of 0.667; unwrapped, the same chain is copy-direction, G1c);
- deep nonlinear stages.

**Why this is the closure the readers asked for.** One-sided bounds are closed under sums, not under products: −·− = +. Contractions are closed under products (gains multiply), under sums (after normalisation), under feedback (small gain), and under any learning step that stays in the class. The Cayley transform turns the half-plane into the disc. So the whole partner-dependent fast computation lives inside S, and the copy direction is decided once, at the boundary, by the wrap.
- "Two sign flips in series make a copy" is defeated because both flips are inside S, where only gain matters.
- The flips that would matter are those *after* the wrap or *outside* 𝓑. After the wrap there is only the renderer's sum: M was moved inside S, and the renderer applies no filter. Outside 𝓑 everything is behind the ledger (§3.3).

**Numbers (κ = 0.30, γ = 0.5).**

| Quantity | Value |
|---|---|
| zero-lag in-phase gain, any direction | ≤ 0.20 |
| incremental gain | ≤ 0.60 |
| lag-τ concordance | ≤ 0.40 − 0.20·ρ_u(τ), where ρ_u(τ) = ⟨v̂, S_τv̂⟩/‖v̂‖² ∈ [−1, 1] is the partner's own normalised autocorrelation at lag τ |

Special cases of the lag bound:
- **Broadband partner** (ρ_u ≈ 0): ≤ 0.40. G2c's linear programme over causal FIR kernels attains 0.397.
- **Smooth partner** (1-s correlation): ≤ 0.276 at 0.5 s.
- **Partner anti-correlated with itself at τ** (an oscillation at period 2τ): ≤ 0.60. That is the gain cap, and it is unavoidable (§3.2).

**Onset peaks.** The energy-sector cap does not bound the first-pass peak of a single onset response. That peak is ≤ 2γ_kκ_k ≤ 0.30 (G10: 0.299), and the loop feeds it back from 2ℓ_echo onward.

### 3.2 Why the matrix sector, and why not "free" fast sign flips: three necessity results

**N1. A diagonal-only ceiling admits a shared-subspace copy.**
- Re H_kk ≤ κ for each k (others frozen) allows H = κ𝟙𝟙ᵀ. Each diagonal entry is κ, yet the gain along the mean-face direction is nκ: 4.8 for n = 16 (G3).
- That is exactly D78's "large shared subspace" failure. The matrix sector He(H) ⪯ bK caps every direction.

**N2. Per-channel ceilings with free cross-channel terms are impossible for real partners.**
- Partner channels co-vary: lip-corner pull and cheek raise in a Duchenne smile. A cross route "partner lip corner → own cheek" at gain 1 gives the agent's cheek a gain of 0.99 on the partner's cheek (G4).
- For every partner with arbitrary channel correlations, a per-channel bound needs Σ_j|H_kj|σ_j/σ_k ≤ κ.
- The weakest quadratic condition that bounds concordance *along whatever the partner actually does* is the matrix sector. Inside it, two kinds of cross-channel structure are free:
  - its skew part (rotations);
  - symmetric cross terms paid for by sign-flipped diagonals: (κ_j − H_jj)(κ_k − H_kk) ≥ ¼(H_jk + H_kj)². For example, with an own smile response of −0.6, a smile-to-brow coupling up to 2√(0.9·0.3) = 1.04 is admissible before the gain cap.

**N3. The lag–sign frontier.**
- Concordance at lag τ for a partner signal concentrated at frequency ω is |H(jω)|cos(φ + ωτ). Over τ ∈ [0, 2π/ω] it reaches |H(jω)|.
- So *no* class can exclude copying at every lag for every partner signal while allowing fast sign flips larger than the copy cap: a sign flip at frequency ω *is* a copy at lag π/ω.
- The half-plane Re H ≤ κ alone is far worse. It admits y = c·u(t − τ) − (c − κ)u(t) for every c (G2b: c = 3, max Re H = 0.30). That is a lagged copy at any gain, paid for by an instantaneous anti-copy.
- The disc is the right object: it caps sign flips at |a|κ = 0.60, broadband lagged copies at rκ = 0.40, and zero-lag copies at bκ = 0.20.
- So sign flips are free *relative to copying*, 3× larger, but not unbounded. The task's request "sign-flipped responses free" is met in the only form the frontier allows.
- Prediction: large opposite-sign responses to the partner's face come from the slow side (§3.4), not the fibre.

### 3.3 The ledger: nothing outside the boundary can track a held level

**Claim L.**
- Every random variable computed outside 𝓑 is a measurable function of (X^s, Q, own variables, own noise). Over the agent's whole life it is (α, ε_L(α))-RDP with respect to ~_L, with ε_L(2) = 0.116. This holds for every parameter value and every learning trajectory, and for an adaptive partner. It holds for:
  - μ, slots, 𝓜, b;
  - every weight after any number of nights;
  - draft choices, retrievals, snippets sent to Claude;
  - y^own and its effect on the face and voice.
- Hence, for any functional f of all of that: |E_P f − E_{P′} f| ≤ √(e^{ε_L(2)} − 1)·sd_{P′}(f) = 0.35 sd.
- And the correlation between any such statistic and a binary held-level difference is ≤ ρ_L = √((e^{ε_L(2)}−1)/2) = 0.25.

**Argument.**
- The release is a Gaussian mechanism. Its mean difference under ~_L is h_s ∗ (Δ_L R̃ v 1_W) sampled at 2 Hz, with R̃ = [R, R_V, 1].
- Because h_s has zero DC gain, that difference is the filter's response to two edges. Its squared norm is ≤ Δ_L²‖R̃‖²E_h, with E_h = 5.85 whatever |W| is (G5a).
- Gaussian RDP is αs²/(2σ²) (Mironov, Table II). Adaptive composition over releases adds the per-sample costs, which sum to the same norm.
- Post-processing is free (Mironov, Table I).
- The functional bound is Hammersley–Chapman–Robbins, using χ² = e^{D₂} − 1.
- Q, turn times and identity are identical under ~_L by definition. (ASR invariance to prosody is an assumption: §3.12.)

**Concrete check against the critics' tracker (K3).**
- G5b sets a partner who holds levels in [0, 1] that change every ~10 min, with transients every 15 s, for 6 h. An attacker inverts the release filter and integrates with the best of seven leaks.
- Without noise it tracks the level at a 1-min correlation of 0.99.
- With the ledger noise it reaches **0.07 ± 0.13**, below the bound 0.25.
- This covers every slow route at once: event proposals, base tilt, draft choice, retrieval, body variables. Any such route is one of the attacker's possible post-processings.

**What the mind still learns.**
- **Statistics over many episodes.** k independent episodes give SNR ≈ 0.27√k; 20 smiles in 5 min give about 1.2.
- **Everything in words.**
- **Identity.**
- **Turn structure.**

### 3.4 The fast fibre cannot hold a level

- S begins with the innate high-pass τ_in, so a held partner level reaches S only through its edges.
- The loop w = v − S(w) is contracting. For a held step, the difference between the two runs' w converges to K^{1/2}Δ (a constant), and its high-pass decays, so S's output difference decays and y^F's difference → 0.
- G10: onset peak 0.299; after 50 s of holding, 3·10⁻⁴.
- The fibre has no other memory longer than its filter bank (the slowest band, 0.05–0.15 Hz, rings out within about 30 s) and the REN's contraction (rate ᾱ = 0.97 per frame, an innate choice in the direct parameterisation: memory ≈ 1 s).
- So no state of the fibre carries a held level past about 30 s, and its contribution to any 1-min mean is the edge transient: ≤ 0.30 × 1.5 s/60 s ≈ 0.008 of the level per edge.

### 3.5 Copy is not attracting under the design's own learning

- (a) For every θ, copy at any gain above the caps of §3.1 is outside the fibre's image. For every θ, the slow side's partner-attributable correlation is ≤ 0.25 (§3.3).
- (b) **The fibre does not settle at its cap either.**
  - Replay is clipped SGD with an innate pull: φ_{t+1} = φ_t − η(g_t + λ_φ(φ_t − φ₀)), ‖g_t‖ ≤ G. For any data, any loss and any partner, induction gives |φ_t − φ₀| ≤ G/λ_φ = 2 (G7, adversarial gradient).
  - So γ_k ≤ γσ(3) = 0.476, and the learned in-phase gain is ≤ 0.194 < cap 0.20 ≪ copy 1. Innate is 0.161.
  - The same induction bounds every fibre parameter to a ball around θ₀.
  - No correct-model or partner-model assumption is used.
- (c) **The dyadic loop.**
  - The agent's map from the partner's *actual* face to its own is the wrap, whatever the partner does. So (W1)–(W3) hold in closed loop.
  - Stability of the fast dyad needs only L·g_p < 1, i.e. g_p < 1.67 for the partner's incremental mimicry gain. Human facial mimicry gains are far below 1 (mimicry synthesis).

### 3.6 Every route, counted

"Copy" below means concordance of the agent's rendered counterpart channel k with the partner's channel k, holding the partner's words, turn times and identity fixed. That is the C8 surrogate logic: a recording of another partner exposed to the same events.

| # | Route | Mechanism | Bound (κ = 0.3, γ = 0.5) |
|---|---|---|---|
| R1 | partner face/gaze → fast face/gaze, every internal path (own-body reading, attention, gates, REN loops, muscle filter) | wrap | in-phase ≤ 0.20 (learned ≤ 0.194); any direction ≤ 0.60; any lag broadband ≤ 0.40; held level → 0 |
| R2 | partner phrase prosody → own next-phrase prosody | voice wrap | same numbers per voice channel, phrase level; held register → 0 (phrase high-pass) |
| R3 | startle, backchannel nods, envelope gating (a → face) | a-route inside S with its own Lipschitz | ≤ ℓ_a·ρ(a, u_k) ≤ 0.15 per face channel; blink ≤ 0.6·ρ(onsets, partner blinks) |
| R4 | partner (face, voice, energy) → X^s → mind → y^own → face and voice | ledger | per held episode, correlation ≤ 0.25; any statistic shifts ≤ 0.35 sd |
| R5 | → mind → draft choice → own text → Q → mind → y^own | ledger (post-processing) | inside R4 |
| R6 | → mind → retrieval → snippets → Claude → text | ledger (post-processing); Claude sees only text | inside R4 |
| R7 | → learning, replay, consolidation (all weights) | replay stores X^s, Q, own only; post-processing | inside R4 |
| R8 | Claude text → visemes (articulators) | phonemes only; echo guard | articulators are outside the copy metric. G8: best-lag (0–3 s) correlation at the 0.3 overlap limit is 0.47 against a surrogate of 0.43 (excess ≤ 0.05); verbatim echo, 1.0, is excluded by the guard |
| R9 | Claude text → TTS text-driven prosody | capped | ≤ P_txt = 0.15 per voice channel. Partner-face dependence is inside R4; word dependence is common cause |
| R10 | partner VAD → floor flag → when the agent speaks | memoryless beyond 1 s, inside 𝓑 | turn-taking is anti-concordant on voice activity, the only channel it touches; visemes as R8 |
| R11 | fast fibre activity → own energy | flat tax c_F | 0: no partner dependence |
| R12 | own speech → microphone → u, ū | AEC plus half-duplex gate | 0 while TTS is active plus 200 ms; residual echo after AEC enters as "partner" input, and is therefore inside R1–R4 |
| R13 | identity token | once per session | ≤ log₂(#enrolled partners) bits per session. It cannot follow a held expression within a session |
| R14 | words → mind → y^own (appraisal of meaning) | not a partner-channel → same-channel strength. Common cause (C8), and words are fixed in the copy test | amplitude ≤ A_k = 0.8. Named so that it is counted, not hidden |
| R15 | rendered face → partner → partner's face → agent | external loop | (W1)–(W3) hold for the actual partner face (§3.5c) |

**Totals per counterpart channel (R1 + R3 + R4; words fixed).**

| Time scale | Per channel | Whole face, any direction |
|---|---|---|
| zero lag, in phase (gain) | 0.20 + 0.15 = 0.35 | 0.20 + 0.15 |
| any lag, broadband (gain) | 0.40 + 0.15 = 0.55 | same |
| any lag, any signal (gain) | 0.60 + 0.15 = 0.75 | same |
| 1-min means, held level | fibre ≈ 0.008 per edge; slow side correlation ≤ 0.25 | same |

Two notes on the totals:
- The 0.15 a-route term is reached only if the partner makes his loudness, speech envelope or voice activity a perfect copy of that face channel's movement.
- Every number is below 1 at every time scale. The most copy-like one (lag 0, in phase) is 0.20 for every partner.

### 3.7 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy non-attracting under own learning |
|---|---|---|---|---|---|
| κ_k (wrap weight) | yes | no (innate) | – | it *is* the cap | – |
| γ_k = γσ(φ_k) | yes | learned per channel in replay | – | γ = 0.5 innate; φ in the ball (§3.5b) | yes: ≤ 0.194 < 0.20 for any data |
| 𝓡_θ gates and attention A(c) | per channel (A rows; REN outputs) | yes: c carries role, stance (slots), needs and words, within 0.5–1 s | yes: sign is set inside S, anywhere in [−0.60, +0.20] | Lipschitz 1, innate | parameters in a ball around θ₀ |
| shared context quantities in c (e.g. one stance coordinate driving every channel) | no, shared | yes | yes | the matrix sector: whatever c does, in-phase ≤ 0.20 in every direction | – |
| ℓ_a (a-route) | per channel | gated by c | yes | 0.15 / 0.6, innate | inside the ball |
| ε_L, σ_s (ledger) | all slow routes | – | (sign-blind) | ε_L(2) = 0.116, innate | holds for every weight, every night |
| A_k, P_txt, V_A, ω_max | per channel | – | – | innate | – |

**No single quantity runs the whole face or a large shared subspace from flat to copy.** The only shared quantities are:
- γ, innate;
- context coordinates, which the matrix sector caps at 0.20 in phase in every direction;
- the slow state, capped by the ledger.

### 3.8 Persistent states persist, and cannot be driven

- **No noise-driven switching.** μ and the slots are linear leaky modes with innate time constants. There are no wells, so there are no barriers to cross. The failure of the fibred design (Kramers exponent 1.5, residence 37 s) cannot occur. Under own noise each coordinate has autocorrelation e^{−Δ/τ_j} exactly.
- **Capacity.** Assume a write SNR of 100:1 (own-noise variance 1% of input-driven variance; an assumption about σ_μ). Then the bits written at t and readable at t + Δ (G6) are:

  | Store | After 1 h | After 6 h | After 24 h | After 1 week |
  |---|---|---|---|---|
  | mood ladder | 327 | 180 | 90 | – |
  | slots (128 × 32 effective dimensions) | ≈ 31,000 | – | ≈ 21,500 (1 day) | ≈ 15,000 |

  This is not ~6 bits. The richness is in structure: content-addressed slots over people, topics and episodes, and a time-constant ladder. It is not in a categorical well index.
- **"Rich" without "trackable".** All of this capacity is written from (X^s, Q, own). By §3.3, no part of it can encode a held partner level beyond ρ_L.
- **Tilt and event-rate dials do not exist.** There are no partner-written events and no partner-reachable tilt. A "rate" of anything derived from X^s is post-processing, and so it is inside the ledger.

### 3.9 Satiable drives; Principle 6

- **Satiable.** 𝒟 ≥ 0, and 𝒟 = 0 exactly on the box ∏[b_i* − δ_i, b_i* + δ_i]. Every choice minimises predicted 𝒟. At satiety, no action has positive expected value except through predicted future deviation. The agent can rest.
- **Information need is satiable.** It is lowered only by own-body learning progress, which falls as the own model converges. So it has no incentive to elicit partner novelty. Partner words and faces are inputs to 𝓜, never targets of I.
- **Principle 6.** The partner's face appears in no loss and no target:
  - the fibre's target is the agent's own future display;
  - 𝓜's targets are own body and released percepts (prediction, not regulation);
  - the draft score depends on own b only.

  No body variable is fed by the partner's smiles, attention or time. Prolonging the conversation earns nothing.

### 3.10 Time scales from structure

| Scale | Carrier | Time constants | Set by |
|---|---|---|---|
| reflex | fibre: filter bank, REN contraction, muscle filter | 33 ms – 2.5 s (echo at 0.45 s) | innate filter poles; REN contraction rate (direct parameterisation) |
| episode, appraisal | 𝓜 | 1 s – 2 min | innate LRU moduli |
| mood | μ ladder | 2 min – 73 h (×3 per group) | innate τ_j |
| relationship | slots | 30 days | innate τ_slot |
| temperament | consolidated weights | ≈ 100 nights | innate λ_n and learning-rate schedule |

The ladder is a sum of Lorentzians with geometric spacing, so the state's spectrum is about 1/f between 1/(2π·73 h) and 1/(2π·2 min). That is a property of the structure, not of learning.

### 3.11 Reading the other through one's own body, and why it is essential

**Statement.** R = (JᵀJ + λ_R I)⁻¹Jᵀ, with J the Jacobian of the agent's own expression map at rest, learned only from the agent's own life. Then:
1. Every partner influence on the learned part of the fibre, and every bit the mind ever receives about the partner's face, passes through R u: the own synergy state that would best produce u.
2. Offsets in ker R change nothing outside 𝓑, *in law*: the release is identical. The agent cannot perceive in others what its own body cannot do.
3. As the agent's repertoire grows (babbling and living widen rank J), what it can perceive of others grows with it. This is a developmental prediction.

**Essential to behaviour.**
- Replace R by zero: the mind's knowledge of the partner's face and the fibre's learned responses vanish, while the reflex prior's echo stays on the raw high-passed input path in F. Prediction: context-appropriate fast responses and face-informed slot learning disappear, and the echo remains.
- Replace R by a generic encoder of equal norm (not own-fitted): the released reading no longer lies in the coordinates 𝓜 uses for its own body. So 𝓜's own-body appraisal model cannot be applied to it, and face-derived evidence stops moving the agent's expected body change.
- These are the ablations of §7.

### 3.12 What is assumed (the places to attack)

1. **ASR word output is invariant to the partner's held prosody level.** If it is not, prosody leaks through Q. Test: pitch-shifted and energy-scaled replays through the ASR, counting word changes.
2. **TTS realises phrase-level prosody targets monotonically, at about unit gain.** Otherwise R2's numbers scale by the realisation gain.
3. **Acoustic echo cancellation residue is small.** If it is not, it enters as "partner" input, which is still inside R1–R4, but it adds self-echo.
4. **Identity recognition does not flip with expression within a session.** It is decided once.
5. **The write-SNR assumption in §3.8.**
6. **The viseme surrogate in R8.** It comes from synthetic phoneme strings; real speech must be measured.

### 3.13 The human non-copying signatures C1–C10

| | Signature | How this design produces it | Status |
|---|---|---|---|
| C1 | head coherence above surrogate at 0.2–1.1 Hz, below at 2.6–6.5 Hz (listening) | 0.45-s echo on head pitch (positive, slow band); own fast micro-motion gated down by the partner's fast-band envelope. G9: fast band 0.0026 against a surrogate of 0.0072; slow band 0.044 against 0.0078 | produced (mechanism; not tested on data) |
| C2 | short-lag form divergence relaxing to chance; self-repetition ≤ chance | language: the echo guard (other-repetition below chance at the next turn); face: motor habituation H penalises self-repetition through 𝒟; the fibre has no memory past ~30 s, so divergence relaxes | produced |
| C3 | shared referent, different form | the referent enters through Q (R14, common cause); form comes from the agent's own display Π_ψ in its own repertoire | produced |
| C4 | role sets the sign | role ∈ c switches the gates in S; the wrap holds in each role | produced |
| C5 | episode sets net level, including below chance | stance (slots, from words and long statistics) sets the fibre's in-phase coefficient anywhere in [−0.60, 0.20], so it can sit below chance | produced |
| C6 | stance and monitoring act separately | stance: slot stance code → sign. Monitoring: information need I → the attention query weight on partner slots, i.e. magnitude. Two quantities | produced |
| C7 | joint-trajectory novelty rising over minutes | I is satiated by learning progress. A repeating joint pattern (in X^s and own output) yields no progress, so I rises and the scorer prefers drafts and displays that vary | produced; strength untested |
| C8 | face coupling mostly common cause; partner-specific excess about a third; slower (~1.75 s) when event and face disagree | content route (R14, amplitude up to 0.8, latency 1–2 s) against fibre (≤ 0.20). When context disagrees, the gates suppress the 0.45-s echo, and any smile arrives through own appraisal at 1.5–2 s | produced; proportions set by A_k and κ |
| C9 | converge in parameters, not output | the slow side can shift the agent's own movement statistics toward the partner's from many-episode statistics (group privacy); moment-to-moment ≤ fibre caps | produced, weakly (ledger) |
| C10 | coupling cannot disable self-restoration | y^own and the homeostatic pull are additive and outside the fibre; the fibre's contribution is bounded and can never zero them | produced |

### 3.14 The brief's expressive-structure items

- **Content-dependent selection.** Need-conditioned attention runs in four places:
  - the fibre's per-channel mixing A(c), where queries come from needs and expected body change;
  - slot reads and writes;
  - episodic retrieval for Claude;
  - draft scoring.

  Selection depends on *what* the agent needs and expects, and on what was said, through c. It cannot depend on the partner's fast face content in the weights (the values only). That is the price of the gain bound.
- **Structure over people, episodes, topics and time:** slots keyed by identity × topic × episode, plus the time-constant ladder.
- **Effective dimensionality:** 128 (μ) + 128 × (64 + 128) (slots) + 512 (𝓜 state).
- **A behaviour the low-dimensional version cannot produce:** the same words from two partners on the same topic produce different own displays and draft choices, through different slots. Collapsing μ and the slots to 2 dimensions (valence and arousal readouts) removes partner × topic specificity. This is an ablation (§7).
- **Richness from structure, not size:** about 800k learned parameters in all (§6).

## 4. Why the closest mechanisms cannot do it alone

| Mechanism | What it gives | Why it does not give the properties (mathematically) |
|---|---|---|
| **RENs / IQC (Revay et al.)** | contraction; any single (Q,S,R) with Q ≺ 0 by direct parameterisation, *including the conic sector used here* | The fibre **is** a robust REN with this sector. RENs are the right primitive, and the parameterisation is not claimed as new. A REN alone fails on two counts. (i) Contraction forbids persistent states, so they must live outside, where the REN certifies nothing: the fibred design's failure. (ii) Discrete routes (draft choice, retrieval, memory writes) have unbounded incremental gain: a choice flip is a jump, so no IQC can certify them. The ledger is what certifies them |
| **Differential privacy (RDP)** | one additive ledger, closed under post-processing and adaptive composition | Divergences are invariant to output bijections (Kairouz, Theorem 2.5), so copying and anti-copying cost the same, and DP cannot make the direction one-sided. A fast onset mirror would need ε large enough to see onsets, and then it bounds nothing about held levels (an onset is the first edge of a held window). Only the forgetful, noise-free, wrapped fibre can respond fast without the slow side learning held levels |
| **Information bottleneck / rate–distortion / directed information** | capacity per channel | Sign-blind, like DP. Held levels are cheap: copy fidelity Cτ ln2/(1 + Cτ ln2) → 1 as τ grows (capacity synthesis), so a rate cap does not stop held-level copying. A level-neighbour relation does, because it prices the episode, not the rate |
| **Active inference** | perception and action from one prediction error | Action descends the error on the other's observation unless attribution gates it. Lanillos' robot mirrors, and copy is then an attractor of the gradient flow whenever the generative model maps the other into the self's coordinates. Here the partner's face is never a prediction target of action. 𝓜 predicts it, and only the agent's own b is regulated |
| **Attention / Hopfield** | content-addressed selection; wells | Softmax attention over partner-keyed content is not globally Lipschitz in the keys, so no gain bound holds. Modern-Hopfield wells give persistence with barriers that the fibred critique measured at 1.5 kT under realistic noise, and a partner write port into them is a tipping route (Ashwin's B/R/N-tipping). Here attention uses non-partner keys, and persistence has no wells |
| **SSMs (S4, LRU, Mamba)** | multi-scale memory | An LTI SSM with learned B, C reaches H = cI on any band, which is copy, and selective SSMs make B input-dependent with no bound. Used here only *inside* S (bounded by the wrap) or *behind* the ledger |
| **Coupled oscillators (Kuramoto)** | synchrony | Phase locking is attracting above a critical coupling K_c: one scalar runs the dyad from incoherence to copy (phase lock). That is the dial D78 forbids |

**Recombination verdict:** see §10.

## 5. The whole system, walked through

- **Perception of the face and voice through the body.** MediaPipe (52 blendshapes, head pose, gaze) → P₀ → u (18). GeMAPS-lite → ū (4). Both enter 𝓑 only.
  - Inside 𝓑, the fibre reads them through F and then R (own coordinates).
  - The release reads them through R and R_V.
  - The partner is perceived *as the own state that would look like this*, at two rates and with two guarantees.
- **Latent state where emotion emerges.**
  - 𝓜's latent, μ and the slots, learned by predicting own body and released percepts.
  - No label is set. Valence and arousal are readouts.
  - Claude names states only in the sense that its words are chosen by what they predict for the agent's body, and the words then act on the state (§2.8).
- **Face output.**
  - Own display, through Π_ψ and M, within 1–2 s of an appraisal.
  - Plus the fibre's fast contribution (0.45 s, ≤ 0.20 in phase).
  - Plus visemes and startle.
- **Voice output.** Phrase prosody from own display, plus the voice wrap, plus capped text prosody. Turn-taking comes from the floor flag.
- **Claude coupling without text.** Drafts plus retrieved snippets, chosen by the homeostatic score. Claude never sees state. The draft and retrieval route is inside the ledger (R5–R6).
- **Learning by living.** Online: states and the fast heads of 𝓜. Nightly: all weights, from the episodic store. The innate stop applies to the fibre.
- **Memory and replay.**
  - The episodic store holds X^s (17 × 2 Hz ≈ 3 MB per 8-h day), Q embeddings, own snapshots and transcript text.
  - Replay samples by state tag (high |Δ𝒟|, novel slots). Raw partner video and audio features are never stored, which is stricter than Principle 7.
  - Ablation: remove state tags from replay, and slot specificity to partners decays (S6).

## 6. A buildable network

Parts carrying the new mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

| Stream | Rate | Encoding | Why |
|---|---|---|---|
| partner face/gaze | 30 Hz | MediaPipe → P₀ (fixed) → u ∈ R^{18} → 𝓑 **[M]** | copy metric and wrap defined here |
| partner voice | phrase | AEC + half-duplex gate → GeMAPS-lite → ū ∈ R⁴ → 𝓑 **[M]** | turn-level vocal convergence is what is measured |
| partner audio events | 30 Hz | envelope, VAD → a ∈ R³ → 𝓑 | startle, backchannel, floor |
| released stream | 2 Hz | X^s ∈ R^{17} **[M]** | the only face/voice the mind sees |
| words | per utterance | Whisper-small (local) → text → Claude; MiniLM → fixed 384 → 64 projection → Q | meaning, no timestamps beyond turn times |
| own body, display, role | 2 Hz (mind), 30 Hz (renderer) | b, y^own, role | own-typed |

**Time encoding.**
- **Fast path:** no positional encoding. Time is carried by the filter-bank band index (the time-scale coordinate) and the explicit lag line, both innate. A KV-cache attention over the partner's past would be an unwrapped memory route, and F's lags must be inside S to be certified.
- **Mind:** continuous time through innate LRU moduli and μ's τ_j. Event timestamps are exact.
- **Episodic retrieval:** ALiBi-style linear recency bias added to the need-conditioned key score. It is a monotone, translation-invariant recency prior, outside 𝓑, so it needs no certificate.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, F (filter bank, lag line), M | fixed | 0 | – |
| 2 | R, R_V **[M]** | 12×18, 4×4; ridge inverse of J | (derived from 𝓔) | replay, own data |
| 3 | 𝓡_θ, acyclic robust REN, Lipschitz 1 **[M]** | n = 64, q = 128, input 72 (R-bands) + 6 (a) + 64 (c) + 6 (d), output 32. Direct param.: X 256², Y₁ 64², B₂ 64×148, D₁₂ 128×148, C₂ 32×64, D₂₁ 32×128, D₂₂ 32×148 | ≈ 110,000 | replay |
| 4 | attention A(c) **[M]** | queries 64 → 18×16; keys 32×16 | ≈ 19,000 | replay |
| 5 | gain logits φ_k **[M]** | 18 + 4 | 22 | replay, innate pull |
| 6 | Cayley wrap (face, voice) **[M]** | y = 2K^{1/2}s, w = K^{1/2}u − s | 0 | – |
| 7 | voice REN S_V **[M]** | n = 16, q = 32, input 4 + 64 | ≈ 9,000 | replay |
| 8 | context encoder c | (𝓜 readout 64 + μ summary 32 + slot 32 + Q 64 + role 4 + b 5) → 64 | ≈ 13,000 | replay |
| 9 | release 𝓢 **[M]** | h_s, decimation, Gaussian noise | 0 | – |
| 10 | 𝓜, LRU 2 × 128 complex modes, innate moduli | inputs 17 + 64 + 5 + 24 + 4 | ≈ 330,000 + heads 40,000 | online (fast heads) + replay |
| 11 | μ write maps and gates | 8 × (64 → 16) × 2 | ≈ 17,000 | replay |
| 12 | slots: query, key, value maps | 256 → 64, 256 → 128, identity/topic → 64 | ≈ 54,000 | replay (states online) |
| 13 | display Π_ψ | 201 → 128 → 24, spectral norm | ≈ 29,000 | replay |
| 14 | own expression map 𝓔 | 12 → 64 → 18 | ≈ 2,000 | replay (own) |
| 15 | draft scorer (𝓜 rollouts + head) | 64 → 1 | 65 | replay |
| 16 | Q projection | 384 → 64 | 24,600 | fixed random (innate) |
| | **total learned** | | **≈ 650,000** | |
| frozen | MediaPipe, Whisper-small, MiniLM (22.7 M), TTS, AEC | | | |

The new mechanism ([M]) holds ≈ 140k parameters, almost all in the REN.

### 6.3 Objectives

- **Replay (nightly).**
  - 𝓛_𝓜: negative log-likelihood of the next X^s, b and y^own, plus Q embeddings at events.
  - 𝓛_F: the fibre's prediction of own display 1–2 s ahead, from the X^s-upsampled partner stream with noise augmentation, plus c. This trains the REN, A and φ.
  - 𝓛_𝓔: own expression reconstruction (own data); R follows.
  - 𝓛_slot, 𝓛_μ: contrastive predictiveness of slot recall and μ for future Δb.
  - 𝓛_score: calibration of predicted 𝒟 for chosen drafts.
  - The anchors: λ‖θ_F − θ₀‖², λ_φ(φ − φ₀)², λ_n‖θ − θ_prev‖².
  - Gradients are clipped globally at G = 1 (innate).
- **Online:** state updates, and 𝓛_𝓜's fast heads every 10 s.
- **Every constraint holds for every value of the free vector**: the REN by direct parameterisation; A, R and Π_ψ by normalisation; γ_k by the sigmoid; the wrap and release are fixed.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms budget).**
  - MediaPipe ≈ 13 ms, in its own process.
  - F and the R-bands < 0.05 ms.
  - REN: 128 sequential scalar activations plus ≈ 0.08 MFLOP, < 1 ms on CPU.
  - Attention and wrap < 0.1 ms.
  - Render 3–5 ms.
- **At 2 Hz:** release, 𝓜 (≈ 0.7 MFLOP), μ, slots < 3 ms.
- **Per turn:** MiniLM ≈ 10 ms per text. Four draft rollouts of 𝓜 over 30 s ≈ 15 ms. Claude API latency is outside the fast loop.
- **Visible fast match:** innate lag 0.45 s plus pipeline ≈ 80 ms.
- **Memory online:** MediaPipe ≈ 0.3 GB; Whisper-small ≈ 0.5 GB; MiniLM 0.1 GB; TTS (macOS system voice or a small local model) ≤ 1 GB; engine < 0.2 GB. Total < 2.2 GB.
- **Replay:** TBPTT on 10-min segments at 2 Hz, batch 32, < 1 GB. Nightly run time ≈ 15–30 min on the M1 Pro GPU (MPS). The store grows by ≈ 3 MB per day (X^s) plus text.

## 7. Ablation predictions (Principle 5), from the properties

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the wrap (read s directly as y^F, same S) | the in-phase gain is no longer bounded by 0.20. Learning on 𝓛_F (own display correlates with partner through common cause) drives the fast face toward same-sign following; copy fraction rises with training | §3.1, G1c |
| matrix sector → diagonal-only cap | whole-face mean-direction concordance can exceed per-channel caps; a shared stance coordinate moves all channels in phase together | N1 |
| the ledger noise (σ_s → 0) | slow states and draft choice track held partner levels (1-min correlation → 0.99 under the K3 tracker) | §3.3, G5b |
| zero-DC release filter → DC-passing | per-episode cost grows with hold duration; at fixed σ_s, held-level tracking returns over long holds | §2.4 |
| high-pass inside S | the fast face sustains up to 0.20 of a held partner level | §3.4 |
| R → generic encoder | face evidence stops moving expected own-body change; slot learning from faces vanishes; reflex echo unchanged | §3.11 |
| the echo guard | more verbatim lexical echo; C2 at turn level fails | R8 |
| information need I | C7 joint-novelty growth disappears; more repetition | §3.13 |
| slots → 2-d valence/arousal | partner × topic specificity gone (same words, same display for any partner) | §3.14 |
| state tags in replay (S6) | partner-specific slot recall decays across nights | §5 |
| innate pull on φ | learned in-phase gain drifts to the 0.20 cap (still bounded, but at the corner) | §3.5b |

## 8. Weak points and falsifiers

### 8.1 Weak points (where a critic should attack)

1. **The slow mind barely sees the face.**
   - A full-range expression change gives the mind SNR ≈ 0.27. Care for a silent sad partner is close to impossible: the agent knows it from words, or from many episodes, or not at all.
   - This is forced by "no slow state tracks the held face" plus the edge argument: an onset is the first edge of a held window.
   - The operator may judge the price too high. The knob is ε_L: ε_L(2) = 0.5 gives ρ_L = 0.57 and per-episode SNR 0.56.
2. **The fibre is small in every direction (≤ 0.60).** Large fast sign flips (strong counter-mimicry within a second) are impossible by the lag–sign frontier (N3), not by choice. If human data show large fast counter-mimicry, the frontier says it must look like a lagged copy for some partner signal. That is a falsifier of the frontier's relevance, not of its mathematics.
3. **Vocal convergence on held levels.** Only weak, through many-episode statistics (C9). Strong convergence of held pitch register within a conversation (Pardo, Levitan) is outside what the ledger allows.
4. **The common-cause route R14 is excluded from "copy" by definition.** A partner who narrates his own face ("I'm smiling") gets an appraisal-driven own display. I hold that this is understanding, not copying (C8 surrogate), but it is the place where a definitional dispute can arise.
5. **Assumptions §3.12** (ASR, TTS, AEC, identity, write SNR, visemes).
6. **The fibre's training signal is weak.** It learns from a noisy 2-Hz stream upsampled to 30 Hz. The reflex prior S₀ carries most of its behaviour. Learned per-partner fast coupling within minutes (Golland's second clip) comes through c (stance from words and statistics), not through fast weights.
7. **Information need as the C7 generator is a hypothesis.** Learning progress may not fall enough on joint repetition to produce Ravreby's novelty growth.

### 8.2 Falsifiers (state-level, once built)

- **F1.** Under partner-swap and segment-shuffle surrogates, the agent's zero-lag in-phase regression gain on any counterpart channel exceeds 0.20 (+ a-route), or the lag-τ gain exceeds 0.40 on broadband segments. Either means a route is uncounted.
- **F2.** Running the K3 tracker (or any decoder) on μ, the slots, 𝓜 or draft choices recovers a held partner level with 1-min correlation > 0.25.
- **F3.** Lesioning R does not change slot learning from faces (contradicts §3.11).
- **F4.** Removing the information need does not reduce joint-pattern novelty (contradicts C7's derivation).
- **F5.** μ coordinates lose autocorrelation faster than e^{−Δ/τ_j} (would mean a hidden nonlinearity or a write leak).

## 9. Sources read for this design

| Source | How read |
|---|---|
| brief.md (all Principles; Expressive structure; Foundations research) | in full |
| research/questions.md: Report 4, Q16, Q17, Q18 and answer, Q19 | in full |
| DECISIONS.md D78 | in full |
| research/foundations/designs.md (all rows, open gaps); known-failures.md | in full |
| critique-design-fibred-attribution-core-proofs.md | in full |
| critique-design-fibred-attribution-core-novelty.md | summary, §1, §2 in full; remaining section headings |
| influence-bounds, directional-influence, capacity-limited-agent, whole-loop-bounds, symmetry-no-copy, self-other-control and non-copying-dynamics syntheses | in full |
| revay-2023-recurrent-equilibrium-networks.md (the reader's note on the full arXiv v3 text) | in full. The (Q,S,R) robust REN with Q ≺ 0, of which the wrap is a special case, is used as the note states it |
| mironov-2017-renyi-differential-privacy.md | in full: Gaussian RDP, post-processing, adaptive composition |
| design-fibred-attribution-core.md | §6 (network) and the heading structure |
| **Not read:** Zames 1966 (conic sectors, loop transformation); Anderson & Vongpanitlerd (bounded-real/positive-real via Cayley) | The Cayley correspondence is derived here in two lines (§3.1) and checked numerically (G1, G2). Nothing depends on these texts |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.**
- The wrap is the classical Cayley/loop transformation between contractions and conic sectors (Zames), and a robust REN with a conic-sector IQC (Revay) realises it.
- The release is the Gaussian RDP mechanism with a level-neighbour relation (the influence-bounds synthesis proposed it).
- 𝓜 is an LRU; the slots and retrieval are attention; the drives are homeostatic.

**Clause 2 (a changed invariant, derived update, deleted scalars): arguable, and I think closer than any earlier design.**
1. **The invariant is one-sidedness end to end, obtained by wrapping once.** The project's six earlier designs tried to keep sign or direction across compositions (sign-blind gates, twisted equivariance, typing rules) and failed at a causal filter or a second flip. The wrap makes direction a property of one map at the boundary. The necessity results N1–N3 show the matrix disc is the weakest object that bounds copying in every partner direction, and that it sits exactly on the lag–sign frontier.
2. **The forgetful-fibre / level-ledger split.** It is what lets a fast reflex see onsets, while no slow state can learn held levels, at a cost that does not grow with time. Neither DP (it cannot let the reflex see onsets without the slow side learning them) nor a REN (it cannot certify the discrete and persistent routes) gives this alone.
3. **What it deletes from the fibred design:**
   - the token bucket;
   - the event proposals and jump sizes;
   - the router's conserved mass τ, its row caps and habituation;
   - the sign-blind gate Γ;
   - the defect-floor noise σ₀;
   - the base wells, tilt and slew;
   - the eight typing rules A1–A8.

   They are replaced by one wrap (κ, γ) and one release (h_s, σ_s), plus one structural check.

Whether this is "a new primitive" in the brief's sense is for the critic. My honest verdict: **a recombination with two new composition results.** It is the first design in the project whose copy bound is end to end by construction for every parameter, and whose slow states provably cannot track the held face.

## Critiques 1a and 1b and the answer (recorded 2026-11-26T05:41:07Z, under Q19: concrete failures only)

**Critique 1a, routes and copying** (critique-design-cayley-ledger-routes.md; checks in sims/critique-cayley-routes/). Five concrete failures, worst first:
1. **The slow mind and the fibre's learning are blind to the partner (severe).** The release passes about 1.35·10⁻⁴ of the signal per sample. A context sign whose target is ±0.5 is learned at about ±0.0002. An hour of held sad face and voice is detected at best 57% of the time. A 1-s shout reaches the mind at SNR 0.16. In practice the fast face is the innate positive echo in every context. This fails Principle 3, the two-way-exchange goal, C4 and C5, and D78's "set by context and learned relationship".
2. **Speech rate leaks through turn times (severe).** Turn times reach the mind noise-free. The mind can track the partner's held speech rate at r = 0.74 over 20 turns (0.93–0.98 if it knows utterance length), against the claimed 0.25. This route into the agent's voice is absent from the route table.
3. **Held expressions cost more the longer they last (high).** The constant-cost claim needs a pure additive offset. If talking lowers the measured held smile by 30%, the cost reaches ε = 1.7 after 1 h and 5.0 after 3 h, against 0.116. Each tracking dropout or restart adds one unit.
4. **Mirror copy on head yaw, head roll and horizontal gaze (medium).** The "free" sign-flipped side of the cone is mirror imitation on these channels: gain 0.58, against the claimed 0.20.
5. **Laughter tokens and punctuation in the ASR text (medium).** They carry the partner's nonverbal expression noise-free to the mind and to Claude.

No concrete failure was found in these areas: a second sign flip in series (apart from item 4), replay averaging the noise away, jitter on the agent's face, partner echo driving gain to the cap, wells in the persistent modes, and C1.

**Critique 1b, principles, novelty and fitness** (critique-design-cayley-ledger-novelty.md). **Not fit to put to the operator.**
- **Concrete failures:**
  - A silently sad user is never noticed, and Claude never sees the face.
  - Principle 3 is not essential: rotating R changes nothing after replay, and innate mimicry bypasses R.
  - Principle 6: the arousal and aversive gauges, fed by the partner's release and loudness, push draft choice toward keeping the user quiet and predictable.
  - Not an emotional agent: no body variable responds to what is said or done, the display policy has no objective, and there are no emotion concepts.
  - Principle 10: an assembly of seven losses.
- **Novelty:**
  - The wrap is the robust-REN parameterisation (Revay et al., eqs. 31–33) plus a classical loop transformation.
  - The ledger is Le Ny & Pappas output perturbation.
  - Recombination on both clauses.
- **Main lead:** the design's premise that contraction forbids persistence is wrong. Contraction forbids multistability, not slow memory. Moods could therefore live inside the bounded face path and know the partner's face, with the noisy release kept only for discrete routes.

**The answer (maintainer).** All failures are accepted.
- **The central lesson:** noise that blinds the slow mind to copying also blinds it to care. Hiding the partner from the mind is the wrong way to stop copying.
- **What survives:**
  - the Cayley-wrapped fast path (the one-sided cone by construction), with the mirror case on head yaw, head roll and horizontal gaze to be fixed by reflecting those channels before the cone;
  - the single input boundary, with turn timing, ASR non-word tokens and punctuation moved inside it.
- **Next revision:** knowing the partner and moving toward the partner are separated. The slow state may model the partner's face richly; the cone then bounds every path from that state to the agent's own expression. Whether that reading of the rule is acceptable is put to the operator (Q20).

**Status:** critiqued; held.
