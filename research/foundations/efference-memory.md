# Candidate E1: Efference-keyed somatic memory

**Status:** in development (S0, after the operator's redirection, D68/D69). Nothing is tested yet. Experiments run only on published data (Meta Seamless Interaction, approved under D70), and none has run. This file is the formal statement. Derivations, propositions and experiments are added section by section.

**Sources merged** (research/foundations/sketches/v2-README.md):
- v2-attention-architect (efference keys);
- v2-fast-weights (self-rewriting memory at three rates);
- v2-interoception-neuroscience (somatic completion);
- v2-routing-modular (a charge shared across self and other, kept as an ablation).

The Claude coupling uses the shared "sayability" interface from v2-llm-interface-linguist.

## 1. Idea

**The mechanism.** The agent's affective core is **attention whose metric is the agent's own body**. Every item the agent can attend to is keyed by the motor program the agent itself would issue to produce it:
- a face or voice it perceives;
- its own current expression;
- a remembered episode;
- a body need;
- a sentence Claude proposes.

**What is attended over.** The keys index a memory of short trajectories that the agent's **own body actually lived**: face, voice, rhythms and body variables. Retrieval brings those trajectories back, and the present body moves along their continuation.

**What emotion is.** Nothing is named. Emotion is **which of its own past bodies the agent is completing, and how that retrieval regime recurs across time scales**.
- Mood is the slow part of the regime.
- Temperament is the memory that nightly replay has consolidated.
- A reflex is a memory that was there before birth.

**What drives what.** The same attention weights drive the face, the voice, which memories reach Claude, and which of Claude's drafts the agent speaks. The agent reads the other person by running the other's face through its own keys, which retrieves its own episodes of making that face.

## 2. Formal statement

### 2.1 Spaces

| Symbol | Domain | Meaning |
|---|---|---|
| 𝒜 | ℝ^{L×(d_m+d_v)} | own-motor space: a window of L frames (about 1 s at 30 Hz) of the agent's facial action-unit activations (d_m) and voice-source and prosody parameters (d_v) |
| x_t | ℝ^{d_x} | the body now, in the agent's own coordinates: x = (m, v, r, b). These are face AUs, voice parameters, innate rhythm phases (breath, blink) and body variables b with set points b* |
| μ: tokens → 𝒜 | fixed or learned map | **the efference key**: the own-motor trajectory that would reproduce a token (2.2) |
| 𝓜_t | finite set | the somatic memory, {(k_i, τ_i, w_i, e_i, r_i)}: key k_i = μ(onset window) ∈ 𝒜, lived trajectory τ_i ∈ ℝ^{H×d_x}, strength w_i ≥ 0, episode pointer e_i (feature streams and transcript only, never raw video), and plasticity class r_i ∈ {innate, slow, fast} |
| s_j, j = 1..J | ℝ^d | query slots with time constants T_j, log-spaced from about 50 ms to weeks |
| α_{j,i} | Δ^{|𝓜|} | attention of slot j over the memory |

### 2.2 The efference key μ

μ is one map with four routes into the same space 𝒜:
1. **Own expression:** the efference copy, the motor command actually issued.
2. **The other's face and voice:** μ = E_ψ(observed AUs and prosody), an inverse model into own coordinates.
   - Before the agent has a face: E_ψ is a fixed linear map from published AU streams (for example FAUValue) onto own AUs.
   - Once it has a face: ψ is trained by self-reproduction, E_ψ(render(a)) ≈ a.
3. **A sentence:** μ = the face and prosody trajectory the agent's own articulator would produce saying it.
4. **A body need:** a token in 𝒜 whose key is the stored onset of the episodes during which that need fell. Its log-mass is log relu(|b_k − b_k*| − ε_k), so it leaves the pool at the set point.

### 2.3 Dynamics (one step)

**Attention.** For each slot j and memory item i:

α_{j,i} = softmax_i( β·⟨W_q s_j, k_i⟩/√d + log w_i + log ν_i − ρ_i )

Here ν_i is a need token's mass (1 for ordinary items), and ρ_i is a habituation (refractory) term that grows while item i is being completed.

**Slots.**

T_j ṡ_j = −s_j + Σ_i α_{j,i} W_v ν(τ_i, φ_i) + Σ_l β_{jl} U s_l

Here ν(τ_i, φ_i) encodes the trajectory at its current phase φ_i. Slow slots bias fast slots' queries through β_{jl}.

**Somatic completion** (the body):

x_{t+1} = x_t + Δt [ R(x_t, o_t) + κ Σ_j π_j Σ_i α_{j,i} ( τ_i[φ_i+1] − τ_i[φ_i] + λ(τ_i[φ_i] − x_t) ) ] + voluntary(Claude) + σξ_t

- R is the innate reflex field: startle, orienting, blink, breath, separation call, contact seeking. It is fixed.
- π_j weights each slot's contribution.
- φ_i advances while α_{·,i} > ε, and resets otherwise.

**Writes**, at three rates on one memory:
- **Fast.** If the surprise ‖x_{t+1} − x̂_{t+1}‖ exceeds θ_w, write a new item (k = μ(onset), τ = the next H frames lived, w from the surprise). All fast strengths decay, ẇ = −γ_f w.
- **Slow.** Nightly replay re-runs stored feature streams through the same attention and moves each fast item to the slow class with probability proportional to its cumulative retrieval mass. Slow items decay at γ_s ≪ γ_f.
- **Innate.** Items are fixed and never written. The reflex templates and the CONSPEC face prior are here.

### 2.4 Objective

One self-supervised objective, over the parameters θ = (W_q, W_v, U, β_{jl}, κ, λ, β, E_ψ):

J(θ) = Σ_t log Σ_j π_j Σ_i α_{j,i} 𝒩( x_{t+1:t+h} ; τ_i[φ_i+1 : φ_i+h] + (x_t − τ_i[φ_i]), Σ )

That is: predict the agent's own embodied future as a mixture of continuations of its own past bodies.

**Not derived from J:** the write threshold θ_w, the decay rates γ_f and γ_s, and the replay rule. These are constraints (K-W), labelled as such.

### 2.5 Coupling to Claude (the shared interface; Claude sees no number or label)

- **Recall.** The episodes e_i with the largest Σ_j α_{j,i} supply verbatim transcript snippets to Claude's context.
- **Speech choice.** Claude writes N drafts. The agent speaks the draft d maximizing Σ_j π_j logsumexp_i(β⟨W_q s_j, k_i⟩) at k = μ(d): the draft whose own-body trajectory the current state retrieves most readily. If none exceeds a threshold, the body hesitates (filled pause, gaze aversion) and new drafts are requested.
- **Timing.** Reply latency and thinking budget follow the settling time of α, meaning the time until its entropy stops changing.
- **Own face.** Claude also sees a rendered image of the agent's own face.

## 3. Why this is a new mechanism (relation to prior work)

| Prior work | What it shares | The precise difference |
|---|---|---|
| MOSAIC (Wolpert, Doya & Kawato 2003; read pp. 593–598, via v2-routing) | own forward and inverse modules reused to understand others | MOSAIC picks among a few fixed modules by prediction error. Here an open, growing memory of *lived trajectories* is queried by multi-time-scale slots in a key space shared by self, other, memory, needs and language. |
| Slot Attention, Perceiver (not yet re-read) | slots cross-attending to tokens | their keys are learned input projections; here the key space is fixed by embodiment and is common to every token type |
| Modern Hopfield networks (Ramsauer et al. 2020; abstract read) | retrieval as attention | they retrieve static patterns; here the retrieved objects are *trajectories whose velocities drive a body*, and the memory is rewritten online by surprise |
| Fast weights, Titans (Ba et al. 2016; Schlag et al. 2021; Behrouz et al. 2025, eqs. 8–14) | surprise-gated memory writes | they model token sequences; here the written object is a joint sensorimotor and interoceptive pattern in own-motor coordinates, and the write rate is split into three plasticity classes |
| Motion matching (Holden et al. 2020; author page read) | selecting the next clip by feature match | there the database is actors' motion curated offline; here it is the agent's own life, written online and keyed by need and by the other's body |
| Active inference (brief.md, Candidate A) | action fulfils predicted bodily trajectories | there is no parametric generative model here, no posterior over hidden states, no preference prior and no expected free energy; needs act only by *which past bodies come back* |

**The claimed new primitive:** attention with an **embodied metric**, keys in the agent's own motor space, over a memory of its own lived trajectories that the same attention rewrites.

*[Owed:]* Slot Attention, Perceiver, MOSAIC (full), and episodic-control papers are to be re-read in their primary sources before this claim is final.

## 4. Principle 10 components (first pass; derivations owed in §6)

| Component | How it arises | Derived or constraint |
|---|---|---|
| Homeostasis | need tokens with mass relu(\|b−b*\|−ε) bias retrieval toward episodes in which that need fell; at the set point the token leaves the pool | derived from μ(need), with the set points innate |
| Curiosity | not yet derived (open) | — |
| Valence | readout: the predicted change in total need-token mass under the current α (never set) | readout |
| Arousal | readout: the rate of change of α, the routing turnover | readout |
| Mimicry | the other's face, through E_ψ, retrieves own episodes keyed by that motor program; their continuation moves the own face | derived; the amplitude is set by κ, β and the strength of the retrieved items |
| Reading others | the body part (b, r) of retrieved own episodes is the agent's reading of the other | derived; it dissociates from mimicry under a motor-part lesion (a prediction) |
| Regulation by Claude | reappraisal: Claude's words enter as μ(text) tokens and change retrieval. Suppression: the voluntary motor path | interface constraint |
| Replay | nightly consolidation of fast items into slow ones | constraint (K-W) |
| Face and voice perception | the four routes of μ in 2.2; the coarse, dynamic and body routes are the inputs to E_ψ | E_ψ trained by self-reproduction |

## 5. Expressive structure (brief.md's four items): what must be shown on published data

1. **Content-dependent selection.** Need and the other's face, as a query, select which own episodes return. *Test:* on Seamless, do listener responses depend on *which* partner expression occurred, beyond its magnitude?
2. **Structure over people, episodes and time.** Items carry episode pointers. Slots span time scales. Partner identity enters through context.
3. **Effective dimensionality, and an ablation.** Compare with collapsing the memory to a single prototype (one item), and with removing the efference keys (generic learned keys).
4. **Richness from structure.** The memory grows with lived experience; the parameters (W_q, W_v, E_ψ) are small.

## 6. Predictions on published data (drafts: to be pre-registered after the file layout is confirmed)

- **P1 (own-history completion).** On Seamless Interaction, after a partner's expression onset, a listener's next 2 s of AUs are predicted better by retrieval from that listener's *own* earlier responses (held-out sessions) than by:
  - (a) a lagged copy of the partner;
  - (b) other people's responses to similar partner expressions.
  - The advantage should be larger with a repeat partner than with a stranger.
- **P2 (repertoire-biased mimicry).** The listener's echo of a partner expression is shifted toward the listener's own most frequent expressions. *Measure:* the projection of the echo onto the listener's own expression covariance, against surrogates.
- **P3 (partner-specific carry-over): untestable on the published data.** Seamless Interaction releases no session dates or order (research/seamless-interaction.md, 2026-11-25 layout), so it is left untested.

**Data constraints that shape P1 and P2** (research/seamless-interaction.md):
- AUs are FAUValue, (T, 24) at 30 Hz, from vendor V00 and most of V02.
- The AU column order is unverified, and columns 12 and 19 are identical. The tests therefore treat the AUs as an **unlabelled vector**: column 19 is dropped, and no claim depends on which AU a column is.
- **Repeat partners:** 195 V00 pairs, all improvising actors.
- **Familiar against stranger:** V02 naturalistic sessions, with 205 people who have both.
- P1's "repeat partner" arm therefore splits into:
  - **P1a:** repeat pair against non-repeat, in V00 improvised sessions;
  - **P1b:** familiar against stranger, in V02 naturalistic sessions.

**Not testable on published data,** and left untested: the Claude coupling (2.5), satiable drives, nightly consolidation, and the face renderer.

## 7. Owed

- The formal propositions (2.3 well-posed; satiation; the mimicry/reading dissociation).
- Re-reading the prior work for §3.
- The P1–P3 pre-registration and loader, once research/seamless-interaction.md has the file layout.
- An independent verification.
