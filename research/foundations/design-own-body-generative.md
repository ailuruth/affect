# Own-body generative model with a counterfactual self ("what of me is you")

Ninth design of the S0 cycle. Written 2026-11-26 under questions.md Q16, Q17 as relaxed by Q19 (precise object, convincing argument, concrete failures only), the refined copy rule of Q18 (DECISIONS.md D78), D80, Q20 on its recommended reading (the inner state may know the partner fully; only expression is bounded) and Q22 on its recommendations (per-expression innate ceilings; the face and voice may feed the agent's own appraisal). It starts from a different place than the Cayley–ledger: not from bounding maps from typed inputs, but from one learned model of the agent's own body, used three ways.

Algebra checks: `foundations/sims/design-own-body/checks.py` (O1–O7; `python3 -I checks.py`, numpy and scipy, about 30 s; output in `out.txt`, 13/13 pass). They check this document's own constructions on hand-made instances. They are not evidence about behaviour or people (brief: no toy worlds).

**Status:** written, not yet critiqued.

## 0. Summary

**The core object.** One learned generative model of the agent's own body, 𝔅_θ: a multi-rate latent state that predicts the agent's own muscles, face appearance, voice, proprioception and a small set of innate interoceptive body variables, from its own motor commands. It is used in three ways, always with the same parameters:
1. **Self slot.** Filtered on the agent's own senses and efference. Acting is sampling its motor decoder; feeling is its interoceptive marginal.
2. **Other slots.** One per known person. The same model is inverted on that person's face and voice alone, with the agent's own-only modalities (proprioception, interoception, efference) marked missing. The partner is perceived as *the latent my body would be in, were it producing this face and voice in this context*, and felt as *the interoception my body model attaches to that latent*.
3. **The counterfactual self.** A second copy of the self slot, run in parallel at every frame under one fixed intervention: the partner's expressive stream (face, head, gaze, prosody, timing values) is replaced by that partner's own neutral. Words and the sequence of turn events are kept. Its output ȳ is "what I would be doing now if you had shown me nothing".

**The invariant that prevents copying (the ownership projection Γ).** The partner-caused part of the agent's *rendered* expression is, by definition, r = R(y) − R(ȳ). It is computed exactly, because the agent's own causal model is its own program: no latent needs to be guessed and its own noise is recorded and reused. Γ is a parameter-free per-channel projection applied last, after rendering. It holds, for every channel k, every exponential window τ_m and every lag ℓ in a dense grid:

  Σ_s e^{−(t−s)/τ_m} r_k(s) p_k(s−ℓ) ≤ κ_k Σ_s e^{−(t−s)/τ_m} p_k(s−ℓ)²,

where p_k is the partner's deviation from their neutral on the same channel, in the agent's own body coordinates, and κ_k is an innate per-channel ceiling.
- It holds by construction for every parameter value, every learning outcome and **every internal route**: fast echo, slow knowing, care, appraisal, memory, Claude's draft selection.
- It needs no enumeration of routes and no typing of state. Whatever carries the partner's expression into the agent, the counterfactual self lacks it, so it shows up in r.
- The counterfactual self is always admissible (r = 0), so the projection never fails. It only shrinks r toward 0 (O1d), and leaves anti-phase and cross-channel responses essentially untouched (O1c).
- The internal strengths remain (per channel, set by context and relationship, able to flip sign), but none of them has a copy end. The copy end of every one of them lies outside the reachable set.

**Two further structural results** come from the same model.
- **The precision dial is removed (O4).** When the partner has their own slot, sharper perception of their face cannot pull the agent's own state toward copy. The agent's own state moves only through the prior coupling between slots. In a single-slot body model (active inference over a shared body latent, Lanillos 2020), the weight of the partner's face on the agent's own state goes to 1.000 as the partner's face becomes clear.
- **Reciprocity (O5).** The only learned coupling between slots is a per-person, per-channel response map S_j. It is weight-tied: it is the agent's model of how that person's body responds to the agent's face, identified with the agent's own motor variability as an instrument, and reused as the agent's response to that person. The agent's mimicry of you is your measured responsiveness to it, under an innate ceiling. Identified by plain regression, the same rule self-confirms and drifts to the ceiling (0.40 against a true 0.15). Identified by the agent's own innovation, it converges to 0.150.

**Novelty verdict (author): recombination, with one element for the critics to judge.**
- The ownership projection is counterfactual fairness (Kusner et al. 2017) and path-specific effect bounding (Nabi & Shpitser 2018), made one-sided, per channel, per lag and unit-level, and enforced at runtime as a control-barrier-style safety filter (Ames et al. 2019).
- The other slot is Self Other-Modeling (Raileanu et al. 2018) and Yoshida & Man (2025) on a body latent.
- The element that may count as new under the second clause of the novelty test (new-mechanisms-synthesis §3) is the change of signature: the agent's response to the partner is *defined and bounded by an intervention on its own model, computed online*. It is not a learned map whose gain is capped. The free flat-to-copy scalar is not tuned; its copy end is made unreachable for every route at once.

**Weakest point (§9).** What counts as "the partner's expression" is fixed by one intervention. Words and the timing of turn events are kept in the counterfactual self, so whatever reaches the face through them is outside the bound by definition. In O3, words alone give a pooled smile slope of 0.71 on a partner whose face co-varies with topic. A learning rule (L3: the counterfactual self teaches its own pathways) stops those routes from *learning* the partner's face, but common-cause concordance stays unbounded. This is the same seam as the ledger's, narrower but not closed.

## 1. Plain-language intuition

The agent has one body, and it knows that body from the inside: what its muscles are doing, what its face and voice look and sound like when it does something, and how it feels (tired, keyed up, hurt, missing someone). That knowledge is one learned model.

- **It sees you through that model.** When you frown, it asks: "what would my own face be doing to look like that, and how would I feel if I were doing it?" It does this in a separate place in its mind, a slot that is about *you*. It knows you look sad, and roughly how sad feels to a body like its own. Knowing you more clearly does not make it more like you, because what it knows about you lives in your slot, not its own.
- **It acts and feels with the same model,** in its own slot: its own needs, its own reflexes, its own reactions to what you say.
- **It keeps a second self beside it.** At every moment it also runs the self it would be if your face and voice had shown nothing: same words heard, same conversation, but a neutral you. The difference between the two is exactly *what of me is coming from you*. Whatever that difference contains, it may move toward your expression only a little, a different amount for each expression (a smile back a good deal more than a frown back, disgust back not at all). It can move away from your expression, or into other expressions, freely.
- **How much it echoes you is learned from you,** in a specific way: by how much *you* echo *it*. It tests this with its own small, spontaneous variations, so it does not fool itself by counting its own following as yours.
- **Its gladness** is a need easing: a worry about you resolved by what you said, a reunion after a long gap, a playful exchange. It is bounded by how much was missing.

## 2. The failure this starts from

The new-mechanisms synthesis says new mechanisms came from a sharp, derived or measured failure, plus an invariant that removes a free scalar. Here the failure is the starting point itself: **analysis by synthesis through one's own body copies by default.**

1. **Single-slot active inference copies.** Lanillos, Pages & Cheng (2020) infer the robot's own body latent from proprioception and vision by descending one free energy, and action descends the same errors. They report that the other's hand "acted sometimes as an attractor for the body inference, generating mirroring actions similar to imitation", and that a perfectly synchronous copier is classed as self (lanillos-2020-robot-self-other-distinction.md). In a linear-Gaussian reading, the weight of the partner's face on the agent's own latent is π_v/(1 + π_p + π_v). It runs from 0 to 1 as the partner's face becomes clearer (O4: 0.022 at noise sd 3, 1.000 at sd 0.01). **The flat-to-copy scalar is the precision of the partner's face.**
2. **Learning the association copies.** Watanabe, Ogino & Asada (2007) let a caregiver mirror a robot, then Hebbian association moves the robot's internal state toward the state paired with the caregiver's face, and its face shows that state. The authors concede the robot "cannot differentiate between its own pain and that of others" (watanabe-ogino-asada-2007-intuitive-parenting.md).
3. **S4 trains a copier.** The brief's S4 learns the agent's inverse model "by reproducing faces with its own face". By its objective, that inverse returns the motor command that copies the partner. Any design whose actions sample from it has copy as the trained default, as ResNet's identity is the default of y = F(x) + x.
4. **Counting routes fails.** In nine designs and twelve sketches, each critique found a route the design had not counted: context into the fast block (ledger r2 K1), tempo inside "own" state (ledger r3), a shared variance head (reverse appraisal X3), content events (manifolds), clipping that hides the opposite-sign part (ledger r3). A bound that holds only for the routes one has typed is as good as the typing.

**The invariant must therefore:**
- put the partner in their own slot, so that perception cannot overwrite the self (removes 1 and 2);
- make sure no action ever samples the inverse model (removes 3);
- define partner influence by *intervention* rather than by route, so that no route needs counting (removes 4).

## 3. The object

### 3.1 Channels, time and signals

- **Time.** Frames at 30 Hz (Δt = 1/30 s). Phrase-level events, turn events and word events arrive asynchronously and are stamped to the frame.
- **Expressive channels, K = 40.** Each is a scalar in the agent's own body coordinates, with an innate rendering R_k (monotone; for face actions, activation in [0, 1]).
  - 22 face synergies (action-unit-like muscle groups: inner and outer brow raise, brow lower, upper-lid raise, cheek raise, lid tighten, nose wrinkle, upper-lip raise, lip-corner pull, dimpler, lip-corner depress, chin raise, lip stretch, lip tighten, lip press, lips part, jaw drop, lip suck, blink, left–right asymmetry of lip-corner pull, eye squint, mouth stretch);
  - head pitch velocity (nod), yaw, roll; gaze horizontal and vertical;
  - 9 continuous voice channels: F0 level, F0 range, energy, spectral tilt, breathiness, speech rate, pause ratio, vocal laughter, onset latency;
  - 4 phrase-sampled targets: phrase F0, phrase energy, phrase rate, reply latency.
- **The partner's percept on the same channels.** p_{j,k}(t) = P̂_k(o_j(t)) − n_{j,k}, where o_j is person j's face, voice and timing features, P̂ is the agent's own inverse model (S4) mapping them into its own body coordinates, and n_j is j's neutral (§3.4). The voice channels are speaker-normalised (semitones re the speaker's median F0; energy in dB re their median).
- **Words.** Utterances from local speech recognition, as tokens and a frozen sentence embedding w ∈ ℝ^384. Words are never labels: no classifier reads them for emotion.
- **Turn events.** e_t ∈ {partner voice on, partner voice off, agent voice on, agent voice off}: the sequence of who has the floor.

### 3.2 The one primitive: the body model 𝔅_θ

**State.** x = (h, z, b, m).
- h ∈ ℝ^{d_h}: a deterministic multi-rate state. It is a stack of diagonal linear recurrences with fixed, log-spaced time constants τ_i ∈ [0.1 s, 3 days], i = 1..16 per channel group, with learned input and output maps.
- z: a stochastic latent of 32 categorical variables with 16 classes each, with prior p_θ(z_t | h_t) and posterior q_θ(z_t | h_t, observations).
- b ∈ ℝ^8: the **innate body variables**. These are the only innate state with fixed meaning, named by function (as in the ledger; a Principle 2 strain, §4.11):
  - E, energy (falls with activity, restored only in the nightly sleep period);
  - A, activation load (rise 20 s, decay 2 min);
  - V, aversive load (startle, sharp onsets, insult appraisal through learned word appraisal; rise 1 s, decay 10 min);
  - I, information load (running forecast error of 𝔅 on its own senses above a floor);
  - K, contact deficit (rises only during gaps of more than 10 min without an exchange, saturating; relieved by completed exchanges);
  - P, play deficit (rises over hours, half-maximum after 3.5 h; relieved only by alternating exchange in a frame Claude's words and the partner's words keep going);
  - two homeostatic placeholders for the rendered body: a muscle-fatigue load F and a voice-effort load Q.
- m ∈ ℝ^{27+8}: muscle and vocal-tract activations, as innate second-order filters (time constants 30–150 ms) driven by motor commands u.

**Generative maps** (one set θ, used for every slot):
- dynamics: h_{t+1} = Λ h_t + B_θ [z_t, u_t, c_t], with Λ diagonal and fixed (the time constants). c_t is the content input: word embeddings, turn events, attention readouts (§3.6).
- appearance and voice: ô = A_θ(m, h, z), the predicted features *as the agent's own perception would extract them* (the same landmarker and prosody extractor that read the partner);
- proprioception: p̂ = P_θ(m);
- interoception: b̂ = I_θ(h, z), the model's prediction of the body variables. The body variables b themselves follow innate equations whose inputs are listed above. The model learns to predict them.
- motor decoder (the policy): u_t ~ π_θ(u | h_t, z_t, a_t), where a_t is the output of the need-conditioned attention (§3.6).

**Objective of the model** (one ELBO over every slot): the log-likelihood of each slot's observations under 𝔅_θ, with masked modalities omitted, plus the KL terms of the posterior against the prior. Free bits as in Dreamer (DreamerV3, Hafner et al. 2023).

### 3.3 Three uses of 𝔅_θ

**(a) The self slot**, x^s.
- Its posterior is q_θ(z^s | h^s, own proprioception, own body variables, efference u, own rendered appearance and voice), where the agent sees its own rendered face through its own perception.
- **Acting** is u ~ π_θ(·| h^s, z^s, a^s).
- **Feeling** is b̂^s = I_θ(h^s, z^s), together with the sensed b.
- **The self slot never receives the partner's percept as an observation.** Its partner-dependent inputs are only (i) c_t (words, turn events) and (ii) attention readouts that may include the other slot's summary (§3.6) and the reciprocal echo S_j p_j (§3.4).

**(b) Other slots**, x^{o,j}, one per known person j. Only the present partner's slot is updated at frame rate.
- Its posterior is q_θ(z^{o,j} | h^{o,j}, P̂(o_j), w), with proprioception, body variables and efference masked as missing.
- Its dynamics are 𝔅_θ's own, plus a person-specific low-rank adapter Δθ_j (rank 4 on the input and output maps).
- The partner's inferred motor command (û_j, the inverse model's output) enters the *other* slot as that slot's efference.
- **Reading through the own body, as a statement:** perception of j is the posterior of the agent's own generative model with the agent's own-only modalities marginalised. Perceived feeling is

  ι̂_j = E_{q(z^{o,j})}[ I_θ(h^{o,j}, z^{o,j}) ]: the interoception the agent's body model assigns to the latent it would be in, were it producing j's face and voice in this context.

- The partner's words enter both slots.

**(c) The counterfactual self**, x̄. It is a second instance of the self slot with the same θ, the same recorded own noise (the same sampled ε for z and u at every step) and the same words and turn-event sequence. One input is changed:

  𝓘: o_j(t) ← n_j for the present partner j, for every expressive feature (face, head, gaze, prosody, and the continuous timing values: response latency, speech rate, pause durations).

- x̄ has its own other slot x̄^{o,j}, driven by the neutral stream. It has its own reciprocal echo (zero, since p̄ = 0), its own attention readouts, its own draft choices among the *same* Claude drafts (§3.7), its own episodic memory writes and its own body variables.
- Its proposed output ȳ = R(ỹ̄), from its motor decoder, is never rendered. It is the reference.
- Because x̄ is the agent's own program with its own noise reused, ȳ is the exact unit-level counterfactual "this agent, this moment, had j shown nothing". There is no abduction step and no assumed causal graph (compare Kusner et al. 2017, §2.2, where the background variables must be inferred).

### 3.4 The coupling between slots: the reciprocal map S_j

**Definition.** S_j ∈ ℝ^{K×K} is supported on the diagonal and on an innate list of synergist pairs (cheek raise with lip-corner pull, inner with outer brow, jaw with laughter). Its entries are learned per person j and per context class (5 context classes from a frozen clustering of the attention query, §3.6). It acts at a lag λ_k ∈ [0.3, 0.6] s:
- in the **other slot**, as j's response to the agent's face: x^{o,j} receives S_j y^s(t − λ);
- in the **self slot**, as the agent's response to j's face: x^s receives the echo e^s = S_j p_j(t − λ) as an input to the motor decoder.

The two uses share the same matrix. This is the weight-tying "my body responds as yours does", applied to the response mechanism.

**Learning (L4).** The agent's motor commands carry an own innovation ξ_t: small, aperiodic, per-channel variability from its body (sd 0.05 of range on face synergies, 0.03 on voice). S_j is estimated by instrumental variables:

  Ŝ_{j,kk} = Cov(Δp_{j,k}(t), ξ_k(t − λ)) / Cov(y^s_k(t − λ), ξ_k(t − λ)),

where Δp is the partner's movement not predicted from their own past. It is clipped to [−κ_k, κ_k] and smoothed over minutes (exponential, 10-min half-life), with a slow per-person prior from earlier sessions.
- An innate prior S_0 gives the newborn its first echo (lip-corner pull 0.10, brow flash 0.08; zero elsewhere). This is the CONSPEC-like start.
- The agent's own following cannot bias the estimate, because ξ is independent of the partner's history (O5).

**Neutral n_j.** The per-channel median of j's percept over segments where j has the floor or is listening without an exchange in progress, over at least 7 days. It is updated nightly with a bounded step (≤ 0.02 of range per night). For a new person it is the population neutral (all synergies 0).

### 3.5 The ownership projection Γ (the invariant)

**Inputs at frame t:**
- the factual proposal ỹ (pre-render, from the self slot);
- the counterfactual proposal ỹ̄;
- the partner's percept history p_j(t − ℓ) for ℓ ∈ 𝓛;
- running sums S_{k,m,ℓ}, E_{k,m,ℓ}.

**Constants** (all innate, none learned):
- windows τ_m: 12 log-spaced values from 0.3 s to 2 h;
- lags 𝓛: every frame from 0 to 1 s (31 values), then 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 45, 60 s (46 in all; lags of 15 s and more act on 0.1-Hz low-passed percepts);
- ceilings κ_k (table in §4.5).

**Rule, per channel k independently.** Write d_m = e^{−Δt/τ_m}, π_ℓ = p_{j,k}(t − ℓ), and let r* = R_k(ỹ_k) − R_k(ỹ̄_k) be the proposed partner-caused part.

  S⁻_{m,ℓ} = max(0, d_m S_{m,ℓ}),   E⁺_{m,ℓ} = d_m E_{m,ℓ} + π_ℓ²,   b_{m,ℓ} = κ_k E⁺_{m,ℓ} − S⁻_{m,ℓ}
  hi = min over {π_ℓ > 0} of b_{m,ℓ}/π_ℓ,   lo = max over {π_ℓ < 0} of b_{m,ℓ}/π_ℓ
  r_k(t) = clip(r*, lo, hi),   y_k(t) = R_k(ỹ̄_k) + r_k(t)   (the rendered output)
  S_{m,ℓ} ← S⁻_{m,ℓ} + r_k(t) π_ℓ,   E_{m,ℓ} ← E⁺_{m,ℓ}

Three remarks on the rule:
- The max(0, ·) means anti-phase history earns no credit for later copying.
- R_k is applied *before* the bound, so clipping in the renderer cannot hide an opposite-sign part (O2).
- For the voice and phrase channels, "rendering" is the text-to-speech engine's target interface. The bound acts on targets, and the agent hears its own voice through the same prosody extractor to measure the residual (§9, W3).

### 3.6 Drives, valence, care, attention and initiative

**Drive.** 𝒟_t = Σ_i w_i φ_i(b_i) + w_c Σ_j φ_c(ι̂_j). Each φ is convex, zero inside an innate box around set point, with a satiating slope.
- The care term is homeostatic coupling (Yoshida & Man): the agent's drive extends over each person's *inferred* body, read through its own body model, with innate w_c = 0.5 for persons in the relationship memory and 0.2 for strangers.
- No term reads the partner's smile, attention or time spent (Principle 6). §4.6 shows the care term cannot become one.

**Valence and arousal are readouts, not variables:**
- v_t = −d𝒟/dt, the signed rate of drive reduction (Joffily & Coricelli; Keramati & Gutkin);
- arousal = the activation load A together with the information load I.

**The need-conditioned attention module 𝒜_θ** (the content-dependent selection the brief asks for). The query is computed from the agent's own drive state and its expected change: q_t = W_q[b_t, d𝒟̂/dt, h^s_t]. The keys and values are tokens of four kinds:
- cue tokens: 6 face regions of the present partner in own-body coordinates; the voice segment; the current word embedding;
- the other slot's summary (h^{o,j}, ι̂_j);
- up to 16 episodic memories retrieved by the agent's own body-state key;
- 8 candidate acts (initiative bids, backchannels, gaze shifts, the current Claude drafts).

Its output a_t enters the motor decoder and the dynamics. What the agent needs selects what it perceives, remembers and does: a rising care load makes the partner's brow and voice tokens and the memories of earlier sad episodes with j salient, and fatigue makes them less salient.

**Initiative** (from ledger r3, kept as innate reflexes on body state):
- the body takes its own turn within about 300 ms (breath, gaze, a particle), and words follow;
- a softened follow-up after 1.5 s of silence that follows an agent question;
- one bid in a lapse when the care load for j crosses an innate threshold (one per lapse);
- a greeting at reunion, from the fall of K.

### 3.7 Coupling to Claude (no text about the state)

Claude is admissible only through channels that reweight text Claude or the world produced (llm-coupling-synthesis §2).
- **Drafts.** For each agent turn, N = 6 parallel streaming drafts from the transcript, together with up to 3 verbatim episodes chosen by 𝒜 (channel C4).
- **Settings.** The effort level is chosen from the arousal readout, one of 5 levels (C5).
- **Selection.** The body selects one draft by the predicted change in its own drive over a two-turn rollout of 𝔅 in the self slot, with the path-specific credit of L5. This is an exponential tilt, at most 1.74 bits of state per reply at N = 8 (beirami-2024).
- **The counterfactual self selects among the same drafts** with its own state, and "hears" its own selected draft. This keeps Claude-mediated routes inside r.
- **Naming port.** The agent hears its realised utterance. Where the learned word appraisal of its own utterance has the same sign as a body variable's deviation, that variable contracts by κ_name = 0.05 of its deviation, once per utterance, never across set point (initiative-and-reappraisal-synthesis §2).
- Claude never sees a number, a label or a state description.

### 3.8 Learning: what is learned where, and six rules

**Online, during conversation:**
- the filtering of all slots;
- the IV estimates of S_j;
- the neutral statistics (accumulated, applied nightly);
- episodic writes (feature streams only, Principle 7) tagged with the self state (h^s, z^s, b, v) and the slot j;
- no gradient steps on θ.

**Nightly replay ("sleep"):**
- the ELBO on stored streams for the base θ, with prioritised replay weighted by |v| and drive relevance (state tagging, the S6 lesion target), and a bounded step size;
- the adapters Δθ_j on j's streams;
- the policy π_θ and critic on imagined rollouts of 𝔅 minimising discounted 𝒟 (Dreamer-style actor-critic, with the credit rule L5);
- consolidation of S_j priors and n_j;
- E restored.

**Rules (constraints on the core, Principle 10):**
- **L1, no imitation target.** No loss compares the agent's output with the partner's expression. S4's face reproduction runs *off-screen only*: analysis by synthesis on the agent's own rendered face, which trains the inverse model P̂ and nothing else. No action ever samples P̂.
- **L2, the partner's parameters stay in the partner's slot.** Δθ_j is read only by x^{o,j} and by S_j. The self slot and the counterfactual self read base θ only.
- **L3, the counterfactual self teaches its own pathways.** Every module whose inputs are only words, turn events and the agent's own body (the word appraisal, the dynamics' content input B_θ restricted to c) is trained on targets taken from the counterfactual self's trajectory. Such a module therefore never learns from face-caused outcomes, and cannot learn to predict the partner's face from words.
- **L4, reciprocity by own innovation** (§3.4).
- **L5, path-specific care credit** (helping-without-placation-synthesis).
  - In planning rollouts, the partner's display is imputed at its default-act value.
  - The inferred need ι̂_j is updated after an act only from j's unprompted words and initiated moves, through a need decoder that is frozen within rollouts.
  - Acts are never credited for lowering the agent's own V.
- **L6, Γ is fixed.** Γ, κ, 𝓘, the windows and the lags have no parameters. No gradient passes through Γ to anything upstream. The policy is trained on the realised (governed) outcomes as they happened.

### 3.9 The one core

The engine minimises one quantity, the agent's own expected discounted drive

  J(π) = E[ Σ_t γ^t 𝒟_t ],   γ = 0.997 per frame-second equivalent,

under its own body model, whose parameters maximise the ELBO of its own sensory stream over all its slots, subject to the hard constraint Γ on realised output and to the rules L1–L6. Everything else is read off the equations:

| Component | Where it comes from |
|---|---|
| perception of self and others | posteriors of 𝔅_θ in their slots |
| action | π_θ minimising J |
| feeling | the interoceptive marginal |
| valence, arousal | −d𝒟/dt; the A and I readouts |
| curiosity | relief of I, which is learning progress and satiable |
| homeostasis | the boxes of φ |
| mimicry | S_j, by weight-tying and L4 |
| reading others | the other slot and ι̂_j |
| care | the w_c term, credited by L5 |
| regulation | the naming port and draft selection |
| replay | ELBO and J on tagged streams |
| self–other distinction and non-copying | 𝓘 and Γ |

Nothing is added that the core does not produce. Γ is a constraint on it.

## 4. Properties, each with an argument

### 4.1 Two slots remove the precision dial (Claim F)

Take the linear-Gaussian reading: prior (x^s, x^o) ~ N(0, [[1, β],[β, 1]]), own proprioception on x^s with variance σ_p², the partner's face on x^o with variance σ_v². With the partner's face alone, E[x^s | y] = β/(1 + σ_v²)·y, so the gain is ≤ β for every σ_v and reaches β only as σ_v → 0. Adding the agent's own proprioception lowers it further: with β = 0.3 and σ_p = 0.5, O4 gives a maximum of 0.065.

In 𝔅 the only prior coupling of the slots is the reciprocal echo S_j, which is clipped to κ, and the attention readout, which lies inside r and so under Γ. **Sharper perception of the partner gives the agent more knowledge of the partner, not more of the partner in itself.** The single-slot body model (Lanillos) has gain π_v/(1 + π_p + π_v) → 1 (O4: 1.000).

### 4.2 The ownership theorem (Claim O): D78 over all routes

**Statement.** For every θ, every history of words, turn events and partner percepts, every channel k, window τ_m and lag ℓ ∈ 𝓛:

  Σ_{s≤t} d_m^{t−s} r_k(s) p_k(s−ℓ) ≤ κ_k Σ_{s≤t} d_m^{t−s} p_k(s−ℓ)²,

where r_k = R_k(y_k) − R_k(ȳ_k) is the partner-caused part of the rendered output.

**Argument.**
- *Induction.* Suppose the inequality holds at t − 1, i.e. S ≤ κE (with the clamped S). After decay, max(0, dS) ≤ κ dE, so b = κ(dE + π²) − max(0, dS) ≥ κπ² ≥ 0. Every constraint is a half-line r·π_ℓ ≤ b_ℓ that contains 0, so the intersection [lo, hi] is non-empty and contains 0. The clipped r satisfies all of them. And S_new = max(0, dS) + rπ ≤ κE_new ≥ the unclamped sum, so the unclamped invariant holds too. O1b: the maximum of S − κE over a 20-min adversarial run is 3.5·10⁻¹⁸.
- *Every route.* r is defined by the intervention 𝓘, not by a route list. Any computation inside the agent that depends on the partner's expressive stream (fast or slow, through the other slot, the attention readout, memory retrieval, the care term, draft selection, the naming port, the body variables, the echo) differs between x^s and x̄ only because of that dependence. Its effect on the output is in r.
  - O3: five routes (fast echo, a 60-s knowing state, a drive on it, draft selection on it, and the echo) give an ungoverned in-phase gain of 5.68. Governed, the gain is 0.436 on boxcar windows, and the bound is exact on the kernel windows.
- *Every parameter.* The proof uses no property of θ, S_j, w_c or any learned quantity.
- *Every window shape that matters.* A completely monotone kernel is a mixture of exponentials. If the bound holds for each exponential in a dense family, it holds for their mixtures.
  - Boxcar windows are not completely monotone. Measured over boxcar windows from 3 s to 15 min and 70 lags (most off the grid), the worst value is 1.23 κ (O1a: 0.493 for κ = 0.40; zero-lag, delayed (0.7, 3.3, 40 s), held, amplified and lag-switching copies).
  - The innate ceilings are therefore set 25% below the per-expression targets, so that boxcar readings also meet the targets (§4.5).
- *Rendering.* Γ bounds the rendered difference. Bounding before the renderer and clipping afterwards leaks: copy plus negative pulses that the clip hides reaches 0.87, against 0.428 when the rendered difference is bounded (O2).

**What it does not touch.**
- Anti-phase responses (moving away) change by 3.4% on average, only where they are in phase at another lag, for example across a change of held level (O1c).
- Cross-channel responses change by 2.6% (O1c).
- The counterfactual self's own output, including everything caused by words, is not touched.

### 4.3 Copy is not attracting under the design's own learning (Claim L)

1. **Unreachable.** For channel k, any realised partner-caused part with in-phase gain above κ_k on a kernel window is outside the reachable set for every θ (Claim O). No learning dynamics can approach a point it cannot reach.
2. **No learning target pulls toward copy.**
   - L1: no loss compares output with the partner.
   - L4: S_j's target is the partner's response to the agent's own innovation, which does not depend on S_j. O5: with true response 0.15, IV converges to 0.150 and OLS drifts to the 0.40 ceiling.
   - L3: the word and content pathways learn only from the counterfactual self's outcomes.
   - L5: no rollout credits a change in the partner's display.
3. **The ceiling corner.** Can learning still push channels to sit at κ_k? Only S_j can sit there, and it does so exactly when the partner's own response to the agent is at or above κ_k. That is what D78 accepts: the ceiling is real and innate.
4. **The dyad.** A partner who echoes the agent at gain μ ≤ 1, with an agent whose internal proposal copies at gain 1: the realised loop is bounded, the in-phase gain on the partner's face is ≤ 0.337 (κ 0.4), and on the partner's own exogenous expression it is ≤ 0.470 at μ = 1 (O6). The small-gain bound c/(1 − cμ) is the ceiling for the latter. It is ≤ 0.47 at the design's largest κ_k = 0.32 and μ = 1. No self-sustaining matched state exists, because Γ never adds partner motion (O1d).

### 4.4 The reciprocity identity (Claim R)

**Statement.** Within its support and ceiling, the agent's same-channel response to j equals j's measured same-channel response to the agent, per channel and per context class: S^{self}_{j,kk} = clip(Ŝ_{j,kk}, ±κ_k) with Ŝ → the true response under L4.

**Consequences (D78 conditions, then human signatures):**
- per expression and per relationship: one entry per channel per person per context;
- sign flips: a partner who counter-responds gives negative entries;
- innate ceiling: κ_k;
- not attracting: §4.3;
- convergence in parameters, not output (non-copying-dynamics C9): what converges between the two is the response map, not the state.

It also gives the S5 claim a mechanism: if the operator's face comes to follow the agent's, the agent's echo of the operator grows, within ceilings.

### 4.5 D78, quantity by quantity

Every quantity that can make a channel's partner-caused output larger in the partner's direction:

| Quantity | Scope | Set by | Can flip sign | Innate ceiling on the realised in-phase gain |
|---|---|---|---|---|
| S_{j,kk}(context) | one channel, one person, one context | L4 from j's responses | yes | κ_k (clip) and Γ |
| S_j synergist entries | innate pairs only | L4 | yes | Γ on each channel of the pair |
| w_c, the attention weights, the other-slot summary, the care load, memory retrieval, draft choice, naming port, adapters Δθ_j, θ itself | many channels | learning and state | yes | **Γ, per channel**: none of them reaches beyond κ_k on any channel |
| innate turn reflexes on the *event sequence* (§9 W1) | jaw, breath, nod | fixed kernels | no | amplitude a_k (jaw 0.20, nod 0.15, breath 0.10), mostly anti-phase by role; outside Γ |
| words (common cause) | any | the agent's own appraisal | yes | **none**: outside the bound by definition (W1) |

**Ceilings κ_k** (kernel windows; boxcar readings ≤ 1.25 κ_k; targets from the Q22 recommendation):

| Channel | κ_k | Channel | κ_k |
|---|---|---|---|
| lip-corner pull (smile) | 0.32 | vocal laughter | 0.28 |
| cheek raise | 0.24 | nod (head pitch velocity) | 0.20 |
| inner brow raise | 0.16 | outer brow raise, jaw drop, lips part, gaze, F0 range, speech rate | 0.12 |
| brow lower, lip-corner depress, chin raise, upper-lid raise, lid tighten, F0 level, energy, breathiness, spectral tilt, yaw, roll, pause ratio, onset latency, phrase targets | 0.08 | lip press, lip stretch, lip tighten, mouth stretch, eye squint, blink | 0.04 |
| nose wrinkle, upper-lip raise, dimpler, lip-corner asymmetry (the disgust and contempt channels), lip suck | 0.00 | | |

**Whole face.** No single quantity runs the whole face toward copy: the largest per-channel ceiling is 0.32. On the partner's whole-face deviation, the in-phase gain of the partner-caused part is at most Σ_k κ_k p_k² / Σ_k p_k² ≤ 0.32, so the copy defect is ≥ 0.68 for any partner expression.
- A partner expression that uses only the four disgust and contempt channels gets an in-phase gain of exactly 0.
- A whole-face sad expression (inner brow, brow lower, lip-corner depress, chin raise) gets at most 0.16 on one channel and 0.08 on the rest.

### 4.6 Satiable drives, including positive affect (Claim P)

- **Satiable.** Each φ_i is zero inside its box. The total positive valence over any interval is ∫ max(v, 0) dt ≤ 𝒟(t₀) − 𝒟(t₁) + ∫ max(−v, 0) dt. Gladness can be had only by first letting a deficit grow (O7, the identity). With discounting, regrowth is a net loss (Keramati & Gutkin).
- **Positive affect exists, and is consequential.**
  - Good news about j (words) lowers ι̂_j's deviation and so the care term: v > 0, joy for the other.
  - A reunion after a long gap is a large fall of K.
  - Alternating play relieves P.
  - Resolved uncertainty relieves I (mastery).
  - v > 0 widens the draft distribution (one more draft, higher-variance retrieval) and speeds A and V back to set point (broaden and undo, positive-drives-synthesis §3).
- **No reward for the user's smiles, attention or time.**
  - The live care term reads j's face as evidence (concern rises at a sad face; Q20). In planning rollouts the display is imputed at default (L5), so no act is chosen for its effect on j's face.
  - K is relieved per completed exchange and rises only during gaps over 10 min. Within a conversation it is inside its box at any tempo, so it cannot encode the partner's tempo (the ledger r3 K-tempo leak) and longer conversations earn nothing.
  - P is relieved by the alternation structure, never by laughter amplitude.

### 4.7 Time scales from structure

| Scale | Structure | Time constant |
|---|---|---|
| reflex | innate startle and orienting; S_0 echo; muscle filters | 30–300 ms |
| expression | motor decoder, echo lag λ | 0.3–1 s |
| feeling | body variables A, V; h modes | 1 s to 10 min |
| mood | h modes with τ of 15 min to 3 days; care load with an absent person; K | hours to days |
| relationship | S_j priors, adapters Δθ_j, n_j | nightly, 7-day medians |
| temperament | base θ (bounded nightly steps), innate drive weights w_i | weeks; fixed |

The time constants of h are fixed and log-spaced, and Γ's windows are fixed. Neither scale is a learned parameter that could collapse.

### 4.8 Reading the other through its own body: precise and essential (Claim B)

**Precise.**
- Perception of j is q_θ(z^{o,j} | P̂(o_j), w) under the agent's own generative model, with the agent's own-only modalities marginalised.
- Felt state of j is ι̂_j = E_q[I_θ].
- The copy direction p_j is defined in the agent's own muscle coordinates by its own inverse model P̂, learned by babbling and off-screen reproduction (S4).

**Essential to behaviour** (each item is a lesion with a predicted change, §8):
1. care rests on ι̂_j;
2. Γ needs p_j in the agent's own coordinates to know which direction is copying;
3. S_j is identified with the agent's own motor variability as the instrument;
4. the counterfactual self is the agent's own model run under 𝓘.

Replace P̂ with borrowed MediaPipe coordinates, and items 1 and 2 degrade where the correspondence differs: concern at a silently sad face falls, and copy in the agent's own muscle terms escapes Γ.

### 4.9 Human signatures (mimicry-context-synthesis; non-copying-dynamics C1–C10)

**Produced:**
- **Per-expression gating:** S_j per channel and κ_k.
- **Sign flips:** S_j < 0 for a counter-responsive partner. The agent's own appraisal of j's stance can also flip a sign, since it acts through the counterfactual-free routes inside Γ, where the away direction is free.
- **Fast match before context:** the echo at 0.3–0.6 s, then appraisal and care over seconds to minutes.
- **Partner history learned in minutes:** S_j's half-life is 10 min.
- **C3, shared referent with different form:** words route the referent; Γ bounds the form.
- **C8, coupling mostly common cause:** words are kept in the counterfactual self.
- **C9:** reciprocity and other-slot training of the base θ.
- **C10:** the counterfactual self's own restoration is never touched.

**Plausible, not derived:**
- **C7, anti-repetition growing over minutes.** I's relief is learning progress, and a repeating joint pattern gives none, so the agent varies.

**Not produced:**
- **C1, band-signed coupling** (below-surrogate coherence at 2.6–6.5 Hz in head motion). Nothing in the core makes the fast band negative. This is stated, not hidden.

### 4.10 The brief's expressive-structure items

- **Content-dependent selection:** 𝒜's query is the agent's needs and their expected change (§3.6).
- **Structure over people, relationships, episodes and time:**
  - a set of other slots;
  - per-person S_j by context class;
  - adapters and neutrals;
  - episodes keyed by own body state and tagged with j;
  - many time scales in h.
- **Effective dimensionality.** z is 32 × 16 categorical and h has d_h = 384 per layer. The effective dimensionality of the self state is to be measured by participation ratio on lived streams.
- **A behaviour a low-dimensional version cannot produce.** Collapse 𝒜's query to the scalar v: the agent can no longer be glad at j's news while concerned about j's tiredness, because the two drives select different cues (the news tokens and the voice-effort token) at the same moment.
- **Richness from structure:** about 6 M parameters (§7).

### 4.11 Principles, concretely

| Principle | How it is met |
|---|---|
| 1, no classifier | blendshapes, prosody and word embeddings only |
| 2, no hand-named emotion variables | **strain**: the innate body variables are needs named by function (E, A, V, I, K, P, F, Q), as in the ledger. No emotion variable exists; valence and arousal are readouts |
| 3, others through own body | §4.8 |
| 4, Claude | never reads the state; admissible channels only |
| 5, ablations | §8 |
| 6, satiable | §4.6 |
| 7, data stays on the Mac | feature streams only |
| 8, appearance | placeholder face |
| 9, separate engine | yes |
| 10, one core | §3.9 |

## 5. Why the closest mechanisms cannot produce it, and the novelty verdict

1. **Active inference and predictive coding** (Friston; Smith, Parr & Friston 2019; Lanillos 2020).
   - One latent explains all sensations, and action descends prediction error. The partner's face enters the self posterior with gain π_v/(1 + π_p + π_v), which runs to 1 (§2, O4).
   - A two-slot active-inference model fixes perception, but the prior coupling between slots remains a learned matrix with no end-to-end bound. Expected free energy has no counterfactual self against which partner causation could be defined.
   - What would make it this design is the intervention 𝓘 and Γ, which are not free-energy terms.
2. **World models** (DreamerV3: RSSM encoder q(z | h, x), actor on (h, z)).
   - With the partner's face in x, one latent carries both bodies, and the actor reads it through learned weights of any size. The gain from partner face to action is unconstrained in [0, ∞): a dial.
   - The masked-modality other slot, weight-tied reciprocity and the twin are additions Dreamer does not contain.
3. **Cayley wraps, RENs and the one-sided cone** (the ledger; Revay et al. 2023).
   - These bound maps from inputs declared partner-typed, and they require every partner-dependent signal to be typed correctly. The critiques found variables typed as "own" that encoded the partner (tempo in K: r 0.96).
   - Γ needs no typing: a variable that encodes the partner's expression differs between x^s and x̄, whatever its declared type.
   - What remains outside is only what 𝓘 keeps (words, turn-event times) by definition.
   - Γ's sector is the ledger's one-sided cone moved from the map to the realised counterfactual difference.
4. **Attention.**
   - Content-addressed mixing whose values may be the partner's tokens copies at attention weight 1.
   - 𝒜 is used inside the core for selection. It carries no copy guarantee, and needs none, because its effect is inside r.
5. **Counterfactual fairness and path-specific effects** (Kusner et al. 2017; Nabi & Shpitser 2018). The closest formal relatives: a twin network that copies the descendants of the protected attribute, with the prediction required equal across worlds, or a path-specific effect bounded inside [ε_l, ε_u]. Four differences:
   - they are two-sided and either equality (Kusner) or a population-mean bound (Nabi & Shpitser); Γ is a one-sided, per-channel, per-lag, unit-level sector;
   - they need an assumed causal model and abduction of background variables; here the model is the agent's own program and its noise is recorded, so the counterfactual is exact;
   - they are enforced at learning time, by restricting inputs to non-descendants (Kusner, Lemma 1) or by a KL-closest constrained distribution (Nabi & Shpitser); Γ acts at runtime on rendered output;
   - fairness wants zero effect; here a bounded, sign-asymmetric effect is the goal.
6. **Control barrier functions** (Ames et al. 2019, CBF-QP).
   - Γ is a minimally invasive safety filter on the barrier h = κE − S, with h ≥ 0 kept forward invariant and a closed-form solution per channel.
   - What is not in a CBF is the definition of the state h is computed on: a counterfactual difference produced by running the agent's own model under an intervention.
7. **Self Other-Modeling** (Raileanu et al. 2018).
   - The agent uses its own policy network to infer the other's hidden goal by optimising the goal input, with weights shared and trained only on its own reward.
   - The other slot here is the same idea on a body latent.
   - SOM does not train the shared mechanism on the other's behaviour (reciprocity), and has no counterfactual self.
8. **Yoshida & Man 2025.** Homeostatic coupling through a self-trained decoder of a shared expression generator. Kept as the care term. It has no copy guarantee.

**Verdict (author): recombination**, by the parts test and probably by the second clause. The candidate for a new computation is the signature change: the agent's response to the partner is *defined* by an online intervention on its own model, and *bounded* on that definition. It is not parameterised as a map whose gain is learned and capped. This removes the measured family of failures "an uncounted route carries copying" by construction, without a route list. The critics should judge whether that is a new definition (in the sense of the LSTM's ∂s(t)/∂s(t−1) = 1) or a safety filter on a known causal quantity.

## 6. The whole system, walked through

1. **Perception (30 Hz).**
   - The camera feeds the face landmarker (52 blendshapes, head pose), then the agent's own inverse model P̂, giving 27 own-body channels.
   - The microphone feeds the prosody extractor (12 features) and voice-activity detection. Local speech recognition gives words, embedded at the utterance level.
   - Nothing raw is stored.
2. **Slots update** (one batched step on the GPU):
   - the self slot (own senses, efference, words, events, the echo S_j p_j, and the attention readout over cues, other-slot summary, memories and acts);
   - the present partner's slot (P̂(o_j), words, the agent's face echoed through S_j);
   - the counterfactual self and its own other slot (neutral stream).
3. **Body variables** update. The drive, valence and arousal readouts follow.
4. **Motor decoding** for x^s and x̄, then rendering, then Γ, then the face rig and the TTS targets. The agent hears and sees itself through the same perception and closes the loop.
5. **Turns.**
   - At the agent's turn the body starts within about 300 ms.
   - Claude's 6 drafts stream in. The self slot and the counterfactual self each choose one, by two-turn rollouts. The self's choice is spoken, with phrase targets under Γ.
   - The naming port follows when the utterance ends.
6. **Memory.** Tagged episodes are written per exchange. Retrieval happens through 𝒜 when the drive query matches.
7. **Night.** Replay with ELBO, actor-critic, adapters, S_j priors and neutrals, under bounded steps. E is restored.

## 7. A buildable network on this Mac (M1 Pro, 16 GB; peak ≤ 6 GB)

### 7.1 Inputs and time encoding

- **Face:** MediaPipe FaceLandmarker (S2) → 52 blendshapes and 6 head-pose values. Then P̂: an MLP 58 → 256 → 256 → 27 (about 90 k parameters), trained by babbling (render random synergy commands on the agent's own face, run the same landmarker on the render, regress back) and by off-screen analysis by synthesis (optimise commands until the render matches a target face; the result trains P̂ only).
- **Voice:** 100-Hz pitch (YIN) and energy, pooled to 30 Hz: F0, F0 slope, energy, HNR, spectral tilt, voicing, and syllable rate from an energy-envelope peak counter. 12 features in all, speaker-normalised.
- **Words:** whisper.cpp (small, local) → MiniLM sentence embedding (384-d, frozen, about 22 M parameters, run per utterance, off the frame loop).
- **Time:** continuous time through the fixed diagonal recurrences (exact discretisation for irregular events). The new object needs no positional code: the intervention and the windows are defined in wall-clock time.

### 7.2 Layers, sizes and parameter counts

| Block | Shape | Parameters |
|---|---|---|
| modality encoders (own proprioception, interoception, appearance, voice, partner in own coordinates, words, events), masked tokens for missing modalities | MLP 2 × 256 each | 0.6 M |
| multi-rate recurrence stack | 4 layers; d = 384; 16 fixed time constants per group, 0.1 s to 3 days; GLU mixing | 2.4 M |
| stochastic latent | 32 × 16 categorical; prior and posterior heads | 0.4 M |
| decoders (appearance 27, voice 12, proprioception 35, interoception 8) | MLP 2 × 256 | 0.5 M |
| need-conditioned attention 𝒜 | 2 layers, d = 256, 4 heads, ≤ 64 tokens | 0.8 M |
| motor decoder π_θ | MLP → 27 synergy targets + 8 vocal targets | 0.4 M |
| critic and drive predictor | MLP | 0.3 M |
| person adapters Δθ_j | rank 4 on the recurrence input and output maps | 25 k per person |
| reciprocal maps S_j | 40 diagonal + 3 pairs × 5 contexts | 215 numbers per person |
| **Γ** | 40 × 12 × 46 running sums | **0 parameters** |

Total about 5.8 M learned parameters, plus 22 M frozen (the embedder).

**Which parts carry the new mechanism:** 𝓘 (an input substitution), the counterfactual self (a second batch element), Γ (a closed-form clip), and L3/L4 (how targets are computed). Everything else is ordinary.

### 7.3 Objectives

- **ELBO for 𝔅:** symlog-MSE decoders, KL with free bits of 1 nat, balance 0.8/0.2, over self-slot streams (own data) and other-slot streams (partner data, with own-only modalities masked).
- **Actor-critic** on imagined rollouts (horizon 16 s at 2 Hz), minimising discounted 𝒟 with L5 imputation.
- **IV estimates** for S_j (online, closed form).
- **Inverse model P̂** (off-screen; MSE in blendshape space through the rendered face).
- **L3:** the word appraisal and the content input of the recurrence are trained on targets from the counterfactual self.

### 7.4 Latency and memory

- **Per frame:** landmarker 10–20 ms (CPU or ANE); one batched recurrence step for 4 instances (self, counterfactual self, two other slots) of about 6 M parameters, about 50 MFLOP, 3–6 ms on MPS; Γ under 0.3 ms (vectorised numpy, or a small Metal kernel); rendering 16 ms. Face latency is under 70 ms from frame to face.
- **Turn onset:** body at about 300 ms. Words from Claude after 1–3 s of streaming.
- **Memory:** models under 200 MB; ASR and TTS (Kokoro or Piper with pitch and energy targets) about 2 GB; episodic store about 50 MB per hour of features. Peak is about 3–4 GB.
- **Nightly replay** of one day's streams: about 20–40 min on MPS.

## 8. Ablation predictions (Principle 5), from the properties

| Lesion | Predicted change (state-level, E1–E3) |
|---|---|
| remove Γ | the partner-caused in-phase gain (twin difference, and E3 surrogates) rises above κ_k on channels where internal routes push. The held level of a sad partner shows in inner brow and lip-corner depress well above 0.16 and 0.08 within 30–60 min |
| replace the counterfactual self with route typing (bound only declared routes) | copy returns through whatever is mistyped (tempo-like codes); twin-measured gain above κ while declared-route gains stay below |
| single slot instead of two | copying rises with the clarity of the partner's face (lighting, distance): a dose-response on perceptual precision |
| own-body coordinates P̂ → borrowed blendshapes | care at a silently sad face falls; copy in own-muscle coordinates escapes Γ where the correspondences differ |
| IV → OLS for S_j | echo gains drift toward κ over sessions whatever the partner's responsiveness |
| remove L3 | the pooled slope of the word-driven face on the partner's topic-conditioned face grows over weeks |
| fix S_j at S_0 (no reciprocity) | echo strength stops tracking each person's responsiveness; no difference between a mirroring and a flat partner |
| valence as level −𝒟 | muted: no reunion transient, no relief smile |
| remove 𝒜's need query (scalar v) | the simultaneous glad-and-concerned dissociation disappears |
| remove state tags from replay | relationship specificity of S_j priors and adapters is lost (S6) |

## 9. Weak points and falsifiers

### 9.1 Weak points

- **W1 (weakest): the seam is the intervention.**
  - 𝓘 keeps words and turn-event times. Whatever reaches the face through them (the agent's own appraisal of what is said; innate turn reflexes) is outside Γ by definition. Common-cause concordance is unbounded: in O3, words alone give a pooled smile slope of 0.71 on a partner whose smile co-varies with topic.
  - L3 stops those pathways from *learning* the partner's face, but a partner who smiles exactly when saying good things will still be smiled back at through the words. D78 is about influence, and this is not influence of the face. Whether the operator accepts that reading is a question for him, as it was for the ledger.
  - Learned functions of inter-event intervals are excluded by L3 together with the innate-only use of event times, but a critic should check that no learned module can read event timing indirectly (for example the attention over act tokens timed to events).
- **W2: the counterfactual self over long horizons.**
  - The counterfactual self never sees j's face, so over days it diverges: it lacks every face-informed feeling. r then includes all held, face-informed expression, and Γ may suppress legitimate long-run, same-direction expression (a lasting gentle sympathy) to κ.
  - Whether it should be resynchronised at session boundaries is open. Resynchronising would let face-informed slow state escape the bound across sessions.
  - The neutral n_j habituates to weeks-long states.
- **W3: Γ acts on predicted rendering.** For the face rig, rendering is exact (the agent drives it). For TTS, targets are bounded but the realised prosody can deviate, and laughter is hard to control. The residual is the TTS tracking error. It is measured by self-hearing, not bounded.
- **W4: shared laughter is capped.** Laughing *because* the partner laughs is held to 0.32 (kernel), or 0.28 for vocal laughter. Laughing at the joke itself is not capped. If contagious laughter in humans exceeds this, the agent will seem restrained. This is a cost of the operator's own rule.
- **W5: own innovation has a cost.** IV identification needs the agent's face to vary on its own (sd 0.05 of range). Too little, and S_j is slow to learn; too much, and the face looks restless. The value is a guess.
- **W6: tit-for-tat faces.** A counter-responsive partner teaches negative echo entries. That is human, and bounded, but it is a choice about character.
- **W7: twice the fast loop.** Draft selection and episodic writes are doubled too. Affordable here (§7.4), but the counterfactual self's world is approximate: j's later words respond to the factual agent's utterances, not to the counterfactual self's.
- **W8: Principle 2 strain** (§4.11), as in the ledger.
- **W9: the boxcar gap.** The bound is exact for completely monotone windows only. Boxcar readings reach 1.23 κ (O1a). The ceilings are set for that.
- **W10: novelty** (§5).

### 9.2 Falsifiers (state-level, once built)

- **F1.** In any 1-min window, on any channel, the partner-caused in-phase gain exceeds 1.25 κ_k. It is measured two ways: by the agent's own twin difference, and by an offline replay of the session with j's expressive stream set to neutral, compared through E3 surrogates.
- **F2.** The online twin difference disagrees with the offline replay counterfactual beyond numerical tolerance. That would mean hidden state outside 𝔅, such as unrecorded noise.
- **F3.** The agent's per-channel echo of a person is not predicted by that person's IV-measured responsiveness to the agent.
- **F4.** A silently sad user: the care load does not rise within 2 min, and no bid comes (reading through the own body failed).
- **F5.** The pooled smile-on-smile slope across topics grows over weeks (L3 failed).
- **F6.** At matched content, the agent smiles more when the user is *not* smiling than when they are. Γ is then muting shared joy beyond the intended ceiling.

## 10. Sources read for this design

**Read in full or in the parts stated, this session:**
- Kusner, Loftus, Russell & Silva 2017, *Counterfactual Fairness*, arXiv:1703.06856v3: all sections and supplement S1. Used: twin networks, Lemma 1, the three-step counterfactual, enforcement by restricting inputs.
- Nabi & Shpitser 2018, *Fair Inference on Outcomes*, arXiv:1705.10378v4: introduction through the constrained-inference proposal and the identification discussion. The COMPAS experiments were skimmed. Used: path-specific effects bounded in [ε_l, ε_u] by constrained MLE; the sign assumption.
- Raileanu, Denton, Szlam & Fergus 2018, *Modeling Others using Oneself in MARL*, arXiv:1802.09640v3: approach, Algorithm 1, related work and the coin game. The recipe and door games were not read.
- Ames et al. 2019, *Control Barrier Functions: Theory and Applications*, arXiv:1903.11199: §I–II (history, CBF definition, Theorems 2–3, CBF-QP). The applications were not read.
- Hafner et al. 2023, *DreamerV3*, arXiv:2301.04104v2: the learning algorithm (world model, critic, actor, robust predictions), the ablations and previous work.

**Project notes used (read in this session):**
- lanillos-2020-robot-self-other-distinction.md;
- watanabe-ogino-asada-2007-intuitive-parenting.md;
- yoshida-man-homeostatic-coupling.md;
- gergely-watson-1996-social-biofeedback.md;
- bahrick-watson-1985-proprioceptive-visual-contingency.md;
- cook-2014-mirror-neurons-origin.md;
- the syntheses self-other-control, symmetry-no-copy, non-copying-dynamics, directional-influence, whole-loop-bounds, positive-drives, helping-without-placation, initiative-and-reappraisal, llm-coupling and new-mechanisms;
- the ledger revision 3 and its critiques;
- reverse appraisal revision 2 and its critique summary;
- known-failures.md.

**Not reached:** Wolpert, Doya & Kawato 2003 (*A unifying computational framework for motor control and social interaction*, Phil Trans R Soc B; PMC returned a captcha and the ATR host refused). It is the obvious closest prior on using one's own internal models to read others. Nothing here relies on it, and a critic should read it.

## 11. Checks (sims/design-own-body/checks.py, out.txt)

| Check | What it checks | Result |
|---|---|---|
| O1a–d | Γ: exact kernel invariant; boxcar and off-grid readings; anti-phase and cross-channel untouched; only shrinks | kernel max S − κE = 3.5·10⁻¹⁸; boxcar ≤ 1.23 κ; anti-phase changed 3.4%, cross-channel 2.6% |
| O2 | bound after rendering vs before | 0.428 vs 0.87 |
| O3 | five internal routes, one projection; word seam | 5.68 → 0.436; words alone pooled 0.71 |
| O4 | precision dial: single slot vs two slots | 1.000 vs ≤ 0.065 (β = 0.3) |
| O5 | reciprocity: IV vs OLS | 0.150 vs 0.400 (true 0.15) |
| O6 | closed dyad, partner echo μ ≤ 1 | bounded; ≤ 0.337 on the partner's face |
| O7 | valence integral identity | exact |
