# Modulated manifolds: emotion as position on staircase manifolds whose existence the agent's own modulators decide

Written 2026-11-26 by an isolated design author (it did not see any other design written in this cycle). Status: **design, not critiqued.** No simulated world is used as evidence anywhere in this file. The three small numeric checks in §3 test the file's own equations; they are not results.

**Summary.**
- **The object.** The agent's slow affective state is a set of discrete positions on a few one-dimensional staircase manifolds, one manifold active per body-variable family.
- **How each part is controlled.**
  - The agent's own satiable drives decide, through occlusive modulators, whether a manifold exists and how long it is. This is a cascade of saddle-node bifurcations, not a gain.
  - A per-partner relationship code decides *which* manifold is active.
  - The partner's face and voice reach the agent only as innate threshold events. Each event moves a position by at most one step: up, none or down, a ternary type the agent learned.
  - Position selects, by kind, a posture from an innate library.
- **What it cannot do.** No partner signal can write a manifold, a modulator or a magnitude, and held expression levels are invisible. Every per-channel strength is therefore a type, capped by an innate step size. Each quantity has rank at most 5, except the relationship key at 11.

---

## 1. Plain-language intuition

Think of the agent's mood as a marble resting on a staircase rather than on a slope.
- Each family of body needs (energy, arousal load, information, aversive load) has its own staircase.
- A marble on a step stays there: that is persistence.
- A marble on a slope rolls back to the bottom: that is no persistence.

**What decides whether there are steps at all.** The agent's own needs, through slow chemical-like signals (modulators):
- When a need is pressing, the staircase forms. Its steps appear one by one, from the bottom up, as the signal rises.
- When the need is met, the signal fades. The upper steps vanish first, and the marble comes down step by step to the floor.

This is the measured fact the design starts from. In mice, blocking two peptide receptors, or a change of hormonal state, removes a persistent state without changing what the cells encode moment to moment (Mountoufaris et al. 2024; Liu et al. 2024). The peptide did not turn a volume down. It decided whether a memory-holding shape existed.

**What the partner can do.** The partner's face and voice cannot touch the staircases or the needs. They are perceived only through the agent's own face: the agent asks, in effect, "which of my own muscle patterns would make that face?" They arrive as **events**: a smile begins, a brow drops, the voice gets loud, the turn ends.
- Each event can nudge the marble up one step, leave it, or nudge it down one step.
- Which of the three happens is a learned **type** per staircase. It is not a strength: the step size is fixed at birth.
- The partner cannot push harder to push further. A big smile and a small smile that cross the same threshold are the same event.
- A smile the partner holds for a minute is one event, not sixty.

**Which staircase is in use.** Each family has several candidate staircases, and the relationship decides which one is active. With a friend, a partner's smile onset may step the marble up a staircase whose next step shows a smile. With a rival, the same onset may step up a staircase whose next step shows a lowered brow. The relationship does not make the response bigger or smaller. It chooses which response circuit is wired in, as a neuromodulator does in a crab's stomatogastric ganglion (Marder 2012) or in a worm's gap-junction circuit (Bargmann & Marder 2013).

**What the face shows.** The marble's step selects a posture, in kind, from a fixed repertoire of the agent's own muscle synergies, as position along the hypothalamic line attractor selects sniff, then mount, then attack (Nair et al. 2023).

**The one fast route that directly matches.** It exists because people match quickly (Dimberg & Thunberg 2012). Smile, brow lowering and brow raising can be returned within about half a second, through units that fire most at their own threshold and less above it (Gidon et al. 2020).
- These units open only if the agent's own state already leans that way. They close if the agent is already showing the expression strongly.
- So a fast match needs an agent that is engaged on that channel but not already full.
- The return is brief and capped by a constant fixed at birth.

**Why copying cannot take over.**
- **No single setting runs the face.** Each staircase can move only along two directions of the face (its next step up and its next step down). A quantity that touches one staircase therefore moves at most a few dimensions of the face.
- **No amplification.** Every response is one fixed-size step.
- **Held expressions are invisible.** The agent can only respond to changes, never track a level.
- **Learning cannot reinforce copying.** It removes the part of the agent's own experience that the agent caused itself. It also identifies how the partner responds using the agent's own random micro-expressions, not its following. So copying cannot teach the agent to copy more.

**Where emotion lives.** It is the configuration of the staircases: which ones exist, which one is active per family, and where each marble rests. Valence and arousal are read out of that configuration and are never set. Claude, the conceptual layer, only ever sees which of its own drafts and which verbatim past snippets were chosen by this configuration. It never sees numbers or names.

---

## 2. The precise object

### 2.1 Index sets and innate constants

| Symbol | Meaning | Value (innate unless marked) |
|---|---|---|
| 𝒦 | facial action channels | 18: AU1, 2, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 20, 23, 24, 25, 26, 43 |
| 𝒱 | voice settings | 6: F0 level, F0 range, loudness, tempo, spectral tilt, aperiodicity |
| 𝒮 | synergy coordinates | 12. Each σ_i has a nonnegative muscle pattern; the columns of W_syn ∈ ℝ^{24×12} span face and voice. See §5.3 |
| S_φ ⊂ 𝒮 | phasic (fast-match) synergies | 3: σ_smile (AU6 + AU12, with lip-spread formant), σ_brow↓ (AU4), σ_brow↑ (AU1 + AU2) |
| 𝔏 | posture library | 24 signed vectors λ ∈ [−a_max, a_max]^{12}, including λ = 0; a_max = 0.225 |
| s⁰ | resting synergy tone | 0.1 · 𝟙 |
| ℱ | families (body-variable groups) | F = 4: energy, arousal load, information, aversive load |
| ℛ_f | candidate manifolds (modes) of family f | R_f = 6, each tagged side(r) ∈ {under, over} |
| N | steps per manifold | 16 |
| ε | half-width of a step ramp | Nε = 1/4 |
| τ_s | slow relaxation constant | 8 s (the peptide-like slow channel) |
| T | noise temperature on positions | set so the barrier-to-noise ratio is ΔV/T = 8 at μ = 1 (§3, Lemma S(e)) |
| κ* | kick threshold | 1/2 |
| T_r | per-mode refractory period | 0.3 s |
| τ_μ, τ_T | fast and tonic modulator time constants | 5 min, 36 h |
| K_U | occlusion constant | 0.5 |
| Ā | phasic burst amplitude (synergy units) | 0.35 for each k ∈ S_φ |
| θ^A, ζ, θ^c, w | phasic threshold, own-drive weight, coupling threshold, coupling width | 0.15, 0.5, s⁰ + 0.05, 0.1 |
| κ_φ | phasic burst kernel | rise 0.15 s, decay 0.5 s, refractory 0.8 s |
| J | event types | 48 (§2.6) |
| ν_b | exogenous micro-expression ("babble") rate | 1/60 s⁻¹ per synergy |

### 2.2 Spaces

The time axis is t ∈ ℝ_{≥0}. Frames arrive at 30 Hz (Δt = 1/30 s). Events occur at arbitrary times on the frame grid.

- **Partner observation.**
  - Face: y_t ∈ ℝ^{52}, MediaPipe blendshapes.
  - Prosody: p_t ∈ ℝ^8, relative to the partner's own running baseline (semitone F0, loudness, HNR, spectral slope 0–500 and 500–1500 Hz, voicing, rate).
  - Gaze-on-agent: g_t ∈ [0,1]. Head pose: h_t ∈ ℝ³.
  - Words: phrase events w_e with timestamps.
- **Body.** b ∈ ℝ⁴, one variable per family, with setpoint b* and dead zones [−ε_f, ε_f].
- **Content state.** c ∈ ℂ^{2×128}, two diagonal state-space layers (§6).
- **Slow state, per family f.**
  - The active mode r_f ∈ ℛ_f.
  - The position ρ_f ∈ [0,1] on the active mode's staircase.
  - The step index n_f := N·Φ(ρ_f) ∈ {0, …, N} on plateaus (§2.7).
- **Modulators.** For each family: m_f = (m_f^fast, m_f^ton) ∈ [0,1]².
- **Relationship code.** ℓ_{·,p} ∈ ℝ^{Σ_f R_f} per partner p, which is a key-retrieved store. Temperament priors β ∈ ℝ^{Σ R_f}.
- **Muscle drive.** u ∈ ℝ^{24} before muscle saturation; muscle activation a = clip(u, 0, 1).
- **The agent's state.** z = (b, c, {r_f, ρ_f, m_f}_f, phasic refractory clocks, deliberate-route state). θ denotes the learned parameters (§2.10).

### 2.3 Body and drive

Each body variable has innate dynamics ḃ_f = Ξ_f(b, a, 𝔢_inn), where 𝔢_inn are innate afferent events. They are listed exhaustively:
- **energy:** fatigue from own effort and time awake; recovery in rest and sleep.
- **arousal load:** startle and loud-onset events from any source, own vocal effort, and decay.
- **information:** a leaky count of the agent's own **surprise events**. A surprise event fires when the prediction-error energy ‖ŷ − P(y)‖² + ‖p̂ − p̃‖² crosses an innate threshold upward. The count is τ_3 ḃ_3 = −b_3 + Σ_e δ(t − t_e^{surp}), with τ_3 = 60 s. The variable is two-sided: below the setpoint means boredom, above it means overload.
- **aversive load:** overload events (b_2 far above setpoint), being talked over (partner speech onset during own speech, from voice-activity detection), and own strain.

**Nothing in Ξ reads any partner expressive feature as a level.** Partner afferents to b are only:
- loudness and startle onsets, which are valence-free events;
- talk-over events;
- surprise events, which are valence-free.

The drive is

  D(b) = Σ_f d_f(b_f − b_f*),  d_f(x) = (|x| − ε_f)₊²  (one-sided variables use (x − ε_f)₊² or (−x − ε_f)₊²).

Each d_f is convex, C¹, and zero exactly on the dead zone. The side of family f is side_f := sign(b_f − b_f*) wherever d_f > 0.

### 2.4 Perception through the agent's own body

The agent's face is rendered from its own synergies. In S2, the same MediaPipe pipeline that reads the partner is run on the agent's own rendered face, and a self-observation map is fitted:

  F_self(s) = G s + g₀,  G ∈ ℝ^{52×12} of full column rank.

G is fitted, and continuously re-checked, from the agent's own commanded synergies s and the blendshapes MediaPipe measures on its own render. In S4, F_self is the learned own forward model (from own efference to own rendered landmarks) and G is its Jacobian.

The partner's face is read as

  P(y) := argmin_{s ∈ [0,1]^{12}} ‖Ω(y − F_self(s))‖²,

where Ω is a fixed diagonal weighting. This is analysis by synthesis with the agent's own body: the partner's face is described by the synergy activation that would make the agent's own face look like it.

The partner's voice is read the same way through the agent's own source-filter body. Partner prosody is expressed in the agent's own voice-setting coordinates, relative to the partner's own running baseline (the Brunswikian lens, with the agent's own encoding weights).

### 2.5 Content layer (fast; the only place partner levels enter)

c_{t+1} = 𝒞_θ(c_t, x_t), with input

  x_t = [P(y_t), g_t, h_t, p̃_t, w-embedding (on phrase events), own commanded synergies s_t^own, own voice settings, b_t].

Here p̃_t is the partner's prosody in the agent's own voice coordinates. 𝒞_θ is two diagonal complex state-space layers (§6).

Heads, all linear from c:
- next-frame prediction of P(y), p̃ and own proprioception;
- predicted external drive change Δ̂d_f^{ext}(h) at horizons h ∈ {1 s, 10 s}, with efference subtracted (§2.10);
- coping C_f;
- agency responsibilities (r_self, r_partner, r_world)_f;
- the cue-prediction precision g_f^cue (wanting, §5.9).

The content layer also computes the partner's position on the agent's own manifolds:

  n̂_f^p = argmax_n p(P(y) | E_{r_f}(n))

This is a Gaussian likelihood around the agent's own readout (§2.9): "how far up my own active staircase I would have to be to make that face". It is an input feature to 𝒞 and never a state of the agent (constraint C3, §2.11).

### 2.6 Events (innate detectors)

An event is a triple e = (t_e, j_e, q_e): a time, a type j ∈ {1, …, J} and a mark q ∈ {1, 2} (amplitude band). Detectors are Schmitt triggers with hysteresis on the following scalar signals. Thresholds θ_j^on > θ_j^off are innate. The need-conditioned lowering in (E4) is bounded.

| Group | Signal | Types |
|---|---|---|
| (E1) partner expression | each coordinate P_k(y) of the partner's face in own synergy coordinates, low-pass 0.2 s, read directly from P and not from the content state; onset (up-crossing) and offset (down-crossing) | 24 |
| (E2) partner social and prosodic | gaze-on and gaze-off; partner voice onset and offset; predicted turn end (content head > θ); low-pitch back-channel cue (110 ms below the 26th percentile of the partner's recent F0 after 700 ms of speech; Ward & Tsukahara 2000); loud onset; talk-over; surprise (prediction-error energy up-crossing); partner change (identity key changes) | 10 |
| (E3) own appraisal | Δ̂d_f^{ext}(10 s) crossing +θ or −θ, per family; mark = the dominant agency (partner or world) | 8 |
| (E4) consummatory | realised drop of d_f greater than θ_cons within 2 s, per family ("liking", §5.9) | 4 |
| (E5) own utterance | completion of a phrase spoken by the agent (Claude's words), appraised by the same head as E3 | 2 |
|  | **total** | **48** |

**Need-conditioned selection (the brief's content-dependent attention).** Each family has its own copy of the partner-event detectors, a receptive field per family. Its thresholds are lowered by the active mode's own interests:

  θ_{j,f}^on(z) = θ_j^{on,0} · (1 − α·g_f(d_f)·|a_{r_f, j}|),  α = 0.3 (innate cap).

An event of type j counts for family f only if it crosses θ_{j,f}. So what the agent currently needs selects which partner changes count, family by family. This is Jung et al.'s 50% → 90% receptive-field change in the agent's own perception. The output map is untouched.

**The phasic triggers** (§2.9) are additional events, of type "phasic k". Their mark is real-valued and is computed at the trigger frame.

### 2.7 Modes: staircase manifolds

**The staircase.** Set θ_i = (i − ½)/N for i = 1, …, N and

  Φ(ρ) = (1/N) Σ_{i=1}^{N} clip((ρ − θ_i + ε)/(2ε), 0, 1),

which is N ramps of width 2ε separated by flat plateaus. For an existence parameter μ ∈ [0,1], the potential is

  V_μ(ρ) = ρ²/2 − μ ∫₀^ρ Φ(s) ds.

**The dynamics of the active mode of family f** (μ_f defined in §2.8), between events:

  τ_s dρ_f = −V'_{μ_f}(ρ_f) dt + √(2 τ_s T) dW_t,  ρ_f ∈ [0,1] (reflected).

This is the one-dimensional mean field of Koulakov et al.'s (2002) network of bistable units. Each ramp is one unit switching on. The recurrent current is μΦ, and "the number of active units", NΦ, is the stored quantity. The readout is the step index n_f := round(N·Φ(ρ_f)).

**At an event e.** The kick to the active mode r = r_f is

  κ_r(e) = g_f(d_f) · a_{r, j_e} · ω(q_e) ∈ [−1, 1],  a_{r,·} ∈ [−1,1]^J (learned), ω(1) = 0.75, ω(2) = 1,

and the family gate (the coupling that inactivates at rest, after Phillips et al. 2016) is

  g_f(d) = clip((d − θ_f^g)/w_f^g, 0, 1).

The **type** of the event for this mode is

  τ_r(e) = sign(κ_r(e)) · 𝟙[|κ_r(e)| ≥ κ*] ∈ {−1, 0, +1},

and the jump is

  ρ_f ← clip(ρ_f + τ_r(e)/N, 0, 1),

subject to the per-mode refractory period T_r. **The learned quantity a enters only through the ternary type τ.** The step size 1/N is innate.

### 2.8 Modulators, existence and the relationship code

**Modulators.** For each family,

  τ_μ ṁ_f^fast = −m_f^fast + ψ(d_f),  τ_T ṁ_f^ton = −m_f^ton + ψ(d_f),  ψ(d) = min(1, d/d̄_f).

The modulators read the actual drive only. Anticipation (allostasis) acts through appraisal events and the modes (§5.9), never through the modulators. This keeps C2 exact.

**Existence: occlusive convergence on one saturable site.**

  μ_f = U(m_f^fast + m_f^ton),  U(x) = min(1, (1 + K_U)·x/(K_U + x)).

This is Marder's occlusion. When the tonic part is already high, the fast part adds little. U ≤ 1 is innate.

**Which manifold.** The active mode is chosen by the relationship code, among the modes on the current side of the drive:

  r_f = argmax_{r ∈ ℛ_f, side(r) = side_f} (ℓ_{r,p} + β_r).

Here p is the current partner's identity key (inferred from face and voice features, §5.6), and β is the temperament prior. The choice is re-made only at a side change, at a partner change, or when n_f = 0. **The relationship selects a type of circuit (which a_r and E_r are in use); the agent's own drive decides whether that circuit holds memory.**

**The rest manifold.** When μ_f < μ₁ = ½ + Nε (= 3/4 here), the active mode has no staircase (Lemma S). Positions relax to 0.

### 2.9 Muscle layer: one muscle drive, three routes

**Affective (emotional) route.**

  S = s⁰ + Σ_f E_{r_f}(n_f) ∈ ℝ^{12},  E_r : {0, …, N} → 𝔏,  E_r(0) = 0.

E_r(n) is the posture selected by position (a learned categorical choice from the innate library). Position selects posture in kind. Because ‖λ‖_∞ ≤ a_max and F·a_max + s⁰ = 1, we have S ∈ [−0.8, 1]^{12}, and the affective muscle drive is W_syn·[S]₊.

**Phasic route (fast match; innate).** For each k ∈ S_φ, the anti-coincidence input is

  I_k(t) = P_k(y_t) + ζ·[S_k(t)]₊.

At an up-crossing of I_k through θ^A (after the refractory period has elapsed), a burst is fired with amplitude

  A_k = Ā · c(S_k) · exp(−(I_k(t_c) − θ^A)/(τ_A θ^A)),  τ_A = 0.39,  c(S) = clip((S − θ^c)/w, 0, 1).

I_k(t_c) is the first suprathreshold frame. τ_A is Gidon et al.'s width in units of threshold. The burst's contribution to synergy k is A_k·κ_φ(t − t_c).

There are two consequences:
- If ζ[S_k]₊ ≥ θ^A, then I_k is above threshold regardless of the partner, no partner-driven up-crossing exists, and the partner's matching onset adds nothing. This is anti-coincidence: own and partner drive together give less.
- If S_k < θ^c, the coupling is closed.

**Deliberate route.**
- **Inputs.** It reads only (i) the agent's own discrete slow state ({r_f, n_f}, side_f) and (ii) turn structure (who holds the floor; Claude's reply events).
- **Update rate.** Its outputs change only at turn boundaries and at the agent's own utterance events.
- **Outputs.**
  - Shunts σ^del ∈ [0,1]^{12}, which multiply the affective synergies. This is London & Häusser's place-not-strength inhibition: it can only remove the agent's own contributions.
  - A posed posture π^del ∈ 𝔏 ∪ {0}.
  - Visemes from the agent's own speech audio.

**Muscle drive.**

  u = W_syn·((1 − σ^del) ⊙ [S]₊ + Σ_{k∈S_φ} A_k κ_φ e_k + π^del₊ + babble) + W_vis·viseme,  a = clip(u, 0, 1).

**Babble.** The exogenous micro-expressions are independent Poisson events of rate ν_b per synergy. Each raises one synergy by one posture step a_max for 1 s. Their times are logged by efference and drawn from a random source outside every coupled loop. They are the instrument of T5.

### 2.10 The one objective and its constraint

**Objective (Principle 10).** The agent's policy (the affective readouts E, the deliberate route and the Claude scorer) minimises the expected discounted drive

  J(θ_act) = 𝔼[ Σ_t γ^t D(b_t) ],  γ = 0.999 per frame,

under the agent's own learned model.

**Constraint (the model is the agent's best predictor of its own streams).** The predictive parameters θ_pred = (𝒞, heads, a, ℓ, β, babble-free efference model Ĥ_self) satisfy

  θ_pred ∈ argmin 𝓛_pred(θ) = 𝔼 Σ_t [ ‖ŷ_{t+1} − P(y_{t+1})‖² + ‖p̂ − p̃‖² + Σ_{f,h} (Δ̂d_f^{ext}(h) − Δd_f^{ext}(t,h))² + ‖proprio error‖² ].

The target external drive change is

  Δd_f^{ext}(t, h) := Δd_f(t, h) − (Ĥ_self ∗ own efference)_f(t, h)

(**efference subtraction**). Ĥ_self is fitted only during babble-only and solo periods: no partner present, or the partner's gaze off the agent.

**How the modes enter 𝓛_pred.** The step indices n_f are inputs to the drive-prediction head, through a relaxed staircase used only in training: Φ with ramp half-width ε_train ≥ ε, and a straight-through ternary type. So a and ℓ are learned as whatever makes the positions predictive of the agent's own external body changes. The modes are the agent's slow beliefs about its own body.

**How E and the deliberate route are learned.** By J, through the model.
- ∂J/∂E is computed by rolling the model forward under alternative postures.
- The partner's response to the agent's own expressions enters only through the **instrumentally identified** kernel R̂ (T5), never through closed-loop regression.

**Learning rates.**
- Online: 𝒞 and the heads at a small rate.
- Nightly replay: everything else (§5.7). Within-session adaptation lives in state (positions, modulators), not in weights.

### 2.11 The constraints that delete the write ports

| Constraint | Formal statement | What it removes |
|---|---|---|
| **C1** no write port into manifold geometry | V_μ, N, ε, τ_s, T are innate; ∂(V, N, ε, τ_s)/∂(anything) = 0 | the partner (or learning) setting persistence time constants directly |
| **C2** no write port into existence | μ_f is a function of (m_f^fast, m_f^ton). These are functions of d_f only, so ∂μ_f/∂y = 0 except through b. b's only partner afferents are valence-free events (§2.3) | the partner deciding whether the agent holds state |
| **C3** no write port into position | ρ_f changes only by (i) its own relaxation, (ii) ±1/N jumps at events, (iii) noise. n̂^p is never assigned to n_f | the partner (or the agent's reading of the partner) authoring the agent's state |
| **C4** event-only partner interface | every map from y, p, g, h to (ρ, m, b, a) passes through an event detector of §2.6 or the phasic trigger | tracking of levels |
| **C5** innate magnitudes | Ā, 1/N, a_max, 𝔏, s⁰, W_syn, U, κ*, α are innate; learning chooses types (a's sign above threshold, E's posture index, ℓ's winner) | learned ceilings and learned gains |
| **C6** own-state-only selection for Claude and for the deliberate route | the Claude scorers and the deliberate policy read {r_f, n_f, b} and turn structure, with partner channels masked (§5.5) | the user's read state steering words or posed faces |

---

## 3. Theorems and proofs

### 3.0 Definitions used throughout

**Event-response kernel.** Fix an operating point: a state z at time t_e, the learned parameters θ, all future inputs, and all noise realisations. Let u^{(+j)} be the muscle drive when one extra partner change of type j occurs at t_e, and let u^{(∅)} be the drive without it. Define

  H_{·j}(τ; z, θ) := u^{(+j)}(t_e + τ) − u^{(∅)}(t_e + τ) ∈ ℝ^{24},

and its window average H_W(z, θ) := |W|⁻¹ ∫_W H(τ) dτ ∈ ℝ^{24×J_U}, with W = [0.3 s, 4 s] by default, over a set U of partner event types.

**This is an exact difference, not a linearisation.** It is defined at every operating point, including discontinuities of the phasic units and of the staircase. "Strength of channel k for partner expression j at z" means H_{kj}. Synergy-coordinate versions (ℝ^{12} rows) are written H^𝒮.

**Copy defect.** Each partner event type j has a signature u_j: the change it represents in the partner's face and voice, in effector coordinates (ℝ^{24}) or synergy coordinates (ℝ^{12}). Let U = [u_j]. The relative copy defect is

  δ_U(H) := inf_{c ≠ 0} ‖H − cU‖_F / ‖cU‖_F.

Copy on U means δ_U ≈ 0, and flat means ‖H‖ ≈ 0. A quantity q "runs U from flat to copy" if q₀ and q₁ exist with ‖H(q₀)‖_F ≤ η|c|‖U‖_F and δ_U(H(q₁)) ≤ η for small η.

**Reachable parameters.** Θ is every value learning can produce under C1–C6: any a ∈ [−1,1]^{24×J}, any categorical E : modes × {0..N} → 𝔏, any ℓ, β, any 𝒞 and heads, and any deliberate policy reading only C6's inputs.

### 3.1 Lemma S (the staircase: existence, length, kicks, barriers)

Let N ≥ 2, 0 < Nε < ½, c := ½ − Nε, and μ ∈ [0,1]. Consider the deterministic flow τ_s ρ̇ = −V'_μ(ρ) on [0,1].

**(a) Equilibria.** The stable equilibria are exactly ρ₀ = 0 and ρ_k = μk/N for 1 ≤ k ≤ k_max(μ), where

  k_max(μ) := max{k ∈ {0, …, N} : k(1 − μ) < c}.

There is exactly one unstable equilibrium s_k in each ramp k ≤ k_max. There are no others.

*Proof.* V'_μ(ρ) = ρ − μΦ(ρ) is piecewise linear.
- **Plateaus.** On plateau i, [θ_i + ε, θ_{i+1} − ε] (with the conventions θ₀ + ε := 0 and θ_{N+1} − ε := 1), Φ = i/N. So V' = ρ − μi/N, whose zero μi/N lies on plateau i iff θ_i + ε < μi/N < θ_{i+1} − ε.
  - The right inequality reads μi < i + ½ − Nε, which holds for μ ≤ 1.
  - The left inequality, for i ≥ 1, reads i(1 − μ) < c.
  - For i = 0, the point ρ = 0 is on plateau 0 because θ₁ − ε = c/N > 0.
  - V'' = 1 on plateaus, so these equilibria are stable.
- **Ramps.** On ramp i, [θ_i − ε, θ_i + ε], V' is linear with endpoint values
  - V'_L(i) = ((i − 1)(1 − μ) + c)/N > 0;
  - V'_R(i) = (i(1 − μ) − c)/N.
  - A zero exists inside iff V'_R(i) < 0, which is the same condition as the plateau-i equilibrium. It is a downward crossing of V', hence unstable.
- **Monotonicity and the top.** The condition i(1 − μ) < c is downward-closed in i, so the stable set is {0, …, k_max}. At ρ = 1, V'(1) = 1 − μ ≥ 0, so there is no boundary-pinned equilibrium other than ρ_N = 1 when μ = 1. ∎

**(b) Bifurcations.** As μ increases through μ_k := 1 − c/k, the stable equilibrium ρ_k and the unstable s_k are born together at ρ = θ_k + ε. This is a saddle-node; at μ = μ_k, V'_R(k) = 0. The first is at μ₁ = ½ + Nε = 3/4. For μ < μ₁, ρ = 0 is the unique equilibrium and is globally attracting.

*Proof.* The birth follows from (a). For the global statement: if k_max = 0 then V'_R(i) ≥ (1 − μ − c)/N > 0 for all i ≥ 1 when μ < μ₁. Every plateau value is V' ≥ V'_R of the preceding ramp, and every ramp has both endpoint values positive. So V' > 0 on (0, 1], and V is a strict Lyapunov function. ∎

The number of stable states is n(μ) = 1 + k_max(μ). It rises from 1 to N + 1 through N saddle-nodes. **The manifold's existence and length are a topological property of μ.**
- *Check (own equations, not a result).* A grid count of sign changes of V' at N = 16, Nε = ¼ gave n = 1, 1, 1, 2, 2, 3, 5, 13, 17 at μ = 0.2, 0.45, 0.70, 0.76, 0.80, 0.90, 0.95, 0.98, 1.0. This equals 1 + k_max(μ) in every case.

**(c) One-step kicks.** Let ρ_f = ρ_k be stable, and apply a jump of +1/N or −1/N.
- **Immediate index.** Immediately after the jump, the index is n = k + 1 (respectively k − 1), clipped to [0, N], for every μ at which ρ_k is stable.
- **Up-jump, target exists.** If k + 1 ≤ k_max(μ), the index stays at k + 1 under the deterministic flow.
- **Up-jump, target absent.** If k + 1 > k_max(μ), the index returns to k after a finite transient T₊(k, μ). This happens at the top of the existing manifold and everywhere when μ < μ₁.
  - T₊(k, μ) ≥ τ_s ln[(1 − μ)/((k + 1)(1 − μ) − c)].
  - T₊ → ∞ as μ ↑ μ_{k+1} (critical slowing near the saddle-node).
  - At μ = 0, k = 0, the duration is exactly τ_s ln 2 ≈ 5.5 s.
- **Down-jump.** A down-jump always persists.

*Proof.*
- **Immediate index, up.** The landing point (μk + 1)/N lies in plateau k + 1:
  - lower bound: μk + 1 > k + ½ + Nε ⇔ k(1 − μ) < c, which is the stability of ρ_k;
  - upper bound: μk + 1 < k + 3/2 − Nε, true; at k + 1 = N the bound is 1, and μk + 1 ≤ N holds.
  - So Φ = (k + 1)/N exactly.
- **Immediate index, down.** The landing point (μk − 1)/N lies in plateau k − 1, by the same two inequalities with the roles exchanged, or it clips to 0.
- **Persistence.** The plateau region of k' lies strictly between the unstable points s_{k'} and s_{k'+1}, so it is in the basin of ρ_{k'}. On a plateau the flow is monotone toward ρ_{k'} and never leaves the plateau, so Φ is constant.
- **Return.** If k + 1 > k_max, then on plateau k + 1, V' = ρ − μ(k + 1)/N > 0 at the landing point, because the landing point minus μ(k + 1)/N equals (1 − μ)/N > 0. Ramp k + 1 has no zero (by (a)), so the flow descends to ρ_k. The plateau-exit time is the stated logarithm: exponential decay toward μ(k + 1)/N, exiting at θ_{k+1} + ε. Its denominator is N·V'_R(k + 1) ≥ 0, with equality exactly at μ = μ_{k+1}. At μ = 0, ρ(t) = e^{−t/τ_s}/N, and n = round(NΦ) = 1 iff ρ ≥ θ₁ = 1/(2N), so the duration is τ_s ln 2. ∎

**(d) Finite manifold, ceiling set by the agent.** For any sequence of events, ρ_f ∈ [0, ρ_{k_max(μ_f)}] after the transients of (c). Each event moves n_f by at most one step. The reachable top is fixed by μ_f, which is a function of the agent's own drive alone (C2). This is Vinograd et al.'s saturation "after the third pulse", with the saturation point set by the agent.

**(e) Barriers and hold times.** For 1 ≤ k ≤ k_max, let δ_k := (c − k(1 − μ))/N > 0 and L_k := V'_L(k). The downward barrier is

  ΔV_k↓(μ) = V(s_k) − V(ρ_k) = δ_k²·(½ + ε/(L_k + δ_k)),

the plateau area δ_k²/2 plus the ramp triangle εδ_k²/(L_k + δ_k).
- **Hold time.** With noise temperature T, the mean hold time on step k is, by the Kramers approximation (valid for ΔV ≫ T),

  T_hold(k, μ) ≈ 2πτ_s·|1 − μ/(2Nε)|^{−½}·exp(ΔV_k↓/T).

  The prefactor is approximate for a piecewise-linear potential.
- **Monotonicity.** ΔV_k↓ is increasing in μ and decreasing in k, because δ_k is.
  - Lower steps outlive higher ones.
  - A manifold that is losing its modulator descends step by step: graded, staircase decay.

*Proof.* Integrate V' from s_k to ρ_k.
- On the plateau part, ∫(ρ_k − ρ)dρ = δ_k²/2.
- On the ramp part, V' is linear from 0 at s_k to −δ_k at the plateau edge, over a width 2εδ_k/(L_k + δ_k). Its area is εδ_k²/(L_k + δ_k).
- With x := 1 − μ, we have L_k + δ_k = (2c − x)/N, so ΔV_k↓ = N⁻²(c − kx)²·(½ + Nε/(2c − x)).
- **Decreasing in k:** only the first factor depends on k, and it decreases in k.
- **Decreasing in x, i.e. increasing in μ:** d ln ΔV/dx = −2k/(c − kx) + [Nε/(2c − x)²]/[½ + Nε/(2c − x)]. The first term is ≤ −2k/c. The second is < 1/(2c − x) < 1/c, because x < c/k ≤ c on the existence range. So the derivative is < (1 − 2k)/c < 0. ∎

*Check (own equations, not a result).* With τ_s = 8 s and T chosen so that ΔV/T = 8 at μ = 1, the formula gives the following.

| μ | k = 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 0.80 | ≲10² s (ΔV/T = 0.4; Kramers not valid) | — | — | — |
| 0.90 | 1.4·10³ s | ≲10² s (ΔV/T = 0.4) | — | — |
| 0.95 | 1.2·10⁴ s | 1.1·10³ s | 2·10² s (ΔV/T = 1.4) | ≲10² s |
| 1.00 | 1.5·10⁵ s | 1.5·10⁵ s | 1.5·10⁵ s | 1.5·10⁵ s |

A direct Euler–Maruyama simulation of the same equation at μ = 0.9, k = 1 (400 escapes) gave a mean first escape of 993 s against Kramers' 1.4·10³ s. The agreement is within the factor expected from the piecewise-linear prefactor and two-sided escape.

### 3.2 Theorem M (existence is not gain: content and persistence separate)

Let the active mode of family f rest at a stable ρ_k, and let an event give it type τ ∈ {−1, 0, +1}.
- **(i) Content is invariant.** The immediate change of the affective synergy drive is E_{r_f}(k + τ) − E_{r_f}(k). It is the same for every μ_f at which ρ_k is stable. Hence ∂H^τ(0⁺; z)/∂μ_f = 0.
- **(ii) Persistence depends on existence.** The change persists until the next event or a noise escape (mean time T_hold) iff τ = −1, or τ = +1 and k + 1 ≤ k_max(μ_f). Otherwise it lasts T₊(k, μ_f) < ∞.
- **(iii) No path from existence to the type.** The type τ, and so which partner events count and with what sign, does not depend on μ_f.

*Proof.* (i) and (ii) are Lemma S(c). For (iii), τ is a function of (g_f, a, ω), and none of these reads μ. ∎

**Reading.** This is Mountoufaris et al.'s dissociation as a theorem: content decoders stay at "virtually 100%", while persistence (line-attractor score ~1.5 → ~0) depends on the peptide. It is also Liu et al.'s: "relatively little if any ramping" with the same partner input in the unreceptive state.

The modulator μ_f is not a gain on the partner's influence. It decides whether the influence is remembered. Across a range of μ, the mode's step count n(μ) changes by saddle-nodes while every immediate response is unchanged.

Koulakov et al. (2002) note the same disentangling for their network: "the gain and robustness are disentangled: the network is robust, whereas the gain has to be adjusted by an external system". Here the "gain" is replaced by an innate step 1/N, so nothing is left to adjust.

### 3.3 Theorem L (level-blindness)

Hold fixed:
- the agent's initial state;
- its own exogenous inputs (noise, babble, Claude's texts);
- the partner's words.

Let two partner face and voice trajectories (y, p, g, h) and (y', p', g', h') on [0, T] produce identical event records. These are all types of §2.6 for every family, with times and marks, plus all phasic triggers and their marks. Then the agent's muscle drive u and its slow state ({r_f, ρ_f, m_f}, b) coincide on [0, T].

*Proof.* Follow every edge out of (y, p, g, h) in §2.4–§2.9:
- (y, p, g, h) feeds only P, p̃, the E1/E2 detectors, the phasic inputs I_k, and the content state c.
- c feeds the heads. The heads feed only the E2 (turn-end, surprise) and E3 detectors, and the learning losses (offline).
- n̂^p feeds only c.
- ρ changes only at events (C3) and by own relaxation.
- r changes only at side changes, partner-change events and n = 0.
- m reads d only (§2.8), and b reads only events among partner afferents (§2.3).
- The deliberate route reads only (r, n, side) and turn events.
- The phasic amplitude is a function of I_k at the trigger frame, which is the mark.
- Visemes read own speech.

So u and the slow state are functions of the event record and the own inputs. ∎

**Corollary L1 (no level tracking).** Suppose the partner holds or changes an expression within a detector's hysteresis band, [θ^off, θ^on] in every family's copy. Then the agent's output after t + T_φ (the phasic kernel length, about 1 s) is the same as if the partner had not changed at all.
- The transfer from a partner's sustained level to the agent's sustained level is exactly zero within each band. This holds at every operating point and every θ ∈ Θ.
- The slow flat-to-copy family that critique 2 found below 0.2 Hz in the partner-regulator design has no counterpart here: there is no sustained-level path.

### 3.4 Lemma R (rank bound) and the decomposition of H

**Lemma R.**
- **(a)** For any U ∈ ℝ^{n×J} and any H with rank H ≤ r,

  δ_U(H) ≥ √(Σ_{i>r} σ_i(U)² / Σ_i σ_i(U)²).

- **(b)** If H₁ = H₀ + Δ with rank Δ ≤ r and ‖H₀‖_F ≤ η|c|‖U‖_F, then ‖H₁ − cU‖_F/‖cU‖_F ≥ √(tail_r(U)) − η.

*Proof.*
- (a) For any c ≠ 0, ‖H − cU‖_F = |c|·‖H/c − U‖_F ≥ |c|·min_{rank X ≤ r}‖X − U‖_F = |c|·√(Σ_{i>r}σ_i(U)²), by Eckart–Young–Mirsky. Divide by |c|‖U‖_F.
- (b) Use the triangle inequality, then (a) applied to Δ. ∎

**Decomposition.** Within a window W that contains no turn boundary, the columns of H^𝒮 (synergy coordinates, before W_syn) split as H^𝒮 = H^φ + H^τ.
- **(H^φ)** Nonzero only in the columns "partner onset of k" for k ∈ S_φ, and there only in row k. Its value is A_k·⟨κ_φ⟩_W (§2.9), with 0 ≤ A_k ≤ Ā. So rank H^φ ≤ |S_φ| = 3.
- **(H^τ)** Column j is Σ_f [E_{r_f}(n_f + τ_{f,j}) − E_{r_f}(n_f)]·π_f(τ_{f,j}, W), where π_f ∈ [0,1] is the fraction of W for which the step persists (Theorem M(ii)).
  - Every column lies in span{v_f⁺, v_f⁻ : f ∈ ℱ}, with v_f^± := E_{r_f}(n_f ± 1) − E_{r_f}(n_f).
  - So rank H^τ ≤ 2F = 8.
  - Clipping [S]₊ is channel-wise and only at the innate floor. The statement is made on S, before the muscle nonlinearity.
- **Deliberate route.** Its shunts multiply rows by constants in [0,1] within W. A diagonal left factor cannot raise rank, and can only shrink entries.

Therefore

  rank H^𝒮_W(z, θ) ≤ |S_φ| + 2F = 11,  for every z and every θ ∈ Θ.

In effector coordinates, H = W_syn·H^𝒮, so rank H ≤ 11 as well, against 24 effector dimensions.

### 3.5 Theorem 1 (the refined rule, Q18 and D78)

**Claim.** At every operating point z and every reachable θ ∈ Θ, the partner-to-agent transfer is carried entirely by the named quantities of the table below. Each quantity:
- has the stated rank of influence r_q on H;
- is bounded by the stated innate ceiling;
- can produce both signs on every synergy channel through a change of *type*;
- is set by the agent's own context, its learned relationship and its episode, and never by the partner's current expression level.

**Consequences.**
1. No quantity runs any set U of partner expressions from flat to copy unless U has effective rank ≤ r_q. The defect is bounded by Lemma R(b).
2. No quantity, and no combination of all of them, runs the whole effector face and voice (24 dimensions) to copy. For an isotropic partner the defect is ≥ √(13/24) ≈ 0.74.
3. Even on the agent's own 12-dimensional perceived synergy space the defect is ≥ √(1/12) ≈ 0.29.

**The named quantities.**

| # | Quantity (name) | Symbol and domain | Acts on (H columns × rows) | Set by | Sign | Innate ceiling | r_q |
|---|---|---|---|---|---|---|---|
| Q1 | **tonic type** of family f's active mode for partner event j | τ_{f,j} = sgn(g_f a_{r_f,j} ω)·𝟙[\|·\| ≥ κ*] ∈ {−1, 0, +1} | column j; rows in span{v_f^±} | learned a_{r_f,·}; which mode r_f is active (relationship); the family gate g_f (own drive) | ± (sign of a) | one step 1/N per event; T_r refractory; posture step ≤ 2a_max = 0.45 per synergy | 2 |
| Q2 | **posture assignment** of mode r at step n | E_r(n) ∈ 𝔏 (categorical over 24 innate postures) | v_f^± of its family; also S_k for k ∈ S_φ, so phasic gates (Q7) | learned (J, through the model) | ± (𝔏 contains postures of both signs on every synergy) | a_max = 0.225 per synergy | 2 + 3 = 5 |
| Q3 | **position** of family f | n_f ∈ {0..k_max(μ_f)} (state) | which v_f^± apply; S, so phasic gates | events (episode history) | via Q2 | Lemma S(d): ≤ k_max(μ_f) | 5 |
| Q4 | **active mode** (circuit type) of family f | r_f ∈ ℛ_f | selects a_{r_f}, E_{r_f} | relationship code ℓ_{·,p}, temperament β, own side_f | ± | through Q1, Q2 | 5 |
| Q5 | **existence** of family f's manifold | μ_f = U(m_f^fast + m_f^ton) ∈ [0,1] | persistence factors π_f only (Theorem M); held position → S → phasic gates | own drive d_f only (C2) | not a sign carrier (M(iii)) | U ≤ 1; length k_max(μ) ≤ N | 2 + 3 = 5 |
| Q6 | **family gate** | g_f(d_f) ∈ [0,1] | which columns pass κ* for family f; family f's receptive-field thresholds | own drive d_f | — (selects; sign from a) | 1; threshold lowering ≤ α = 0.3 | 2 |
| Q7 | **phasic strength** on channel k ∈ S_φ | A_k = Ā·c(S_k)·exp(−(I_k − θ^A)/(τ_Aθ^A)), and 0 if ζ[S_k]₊ ≥ θ^A | column "onset k", row k | own basal drive S_k (context, via Q2–Q5) | ≥ 0 (the channel's sign flips through Q1/Q2) | Ā = 0.35; duration ≤ 1 s; refractory 0.8 s | 1 |
| Q8 | **deliberate shunt** on synergy k | σ_k^del ∈ [0,1], constant within W | row k (scales) | deliberate policy on own state and turn events (C6) | can only shrink toward 0 (containment) | 1 | 1 |
| Q9 | **relationship key** | partner identity p (discrete) | r_f for all f at once | the partner's identity, retrieving the agent's own stored code | ± | through Q1–Q4 | 2F + 3 = 11 |

Body variables appear only through Q5 and Q6 of their own family. Innate constants are not quantities in this sense: they are not varied by context, relationship or learning (C1, C5).

**Proof.**
1. **Completeness.** By Theorem L, the partner's face and voice reach u only through events. By §3.4, every event's effect is H^φ + H^τ, scaled row-wise by Q8. H^φ is parameterised only by Q7. H^τ is parameterised only by (τ_{f,j}, v_f^±, π_f), which are respectively Q1, Q2 with Q3, and Q5. Q1 is a function of a (learned), r_f (Q4) and g_f (Q6). The key Q9 changes only r_f.
2. **Rank of each quantity.** Fix all quantities but one; the change in H is confined as follows.
   - Q1 changes only family f's coefficients on v_f^±: rank ≤ 2.
   - Q2 and Q3 change v_f^± (rank ≤ 2), and through S_k they change at most the 3 phasic entries (rank ≤ 3).
   - Q4 changes a_{r_f} and E_{r_f} of one family: rank ≤ 2 + 3.
   - Q5 changes π_f and, through the held position, S: rank ≤ 2 + 3.
   - Q6 changes which of family f's coefficients are nonzero: rank ≤ 2.
   - Q7 changes one entry: rank 1.
   - Q8 scales one row: rank 1.
   - Q9 changes r_f for all F families: rank ≤ 2F + 3.
3. **Ceilings.** The stated bounds follow from C5, Lemma S(c, d) and §2.9. In particular:
   - |H^τ_{ij}| ≤ Σ_f 2a_max·π_f, and [S]₊ ∈ [0,1];
   - 0 ≤ H^φ_{kk} ≤ Ā;
   - no learned quantity multiplies a magnitude (C5).
   - Hence **no gain above an innate constant exists anywhere on the partner path, and no amplification is possible**: a stronger partner display cannot produce more than one step per family.
4. **Sign.** This uses a design condition on the innate library: 𝔏 contains, for every synergy i, postures λ⁺ and λ⁻ with λ⁺_i > 0 > λ⁻_i. Then for any family f, mode r, step n and event j, the choices E_r(n) = 0 and E_r(n + 1) = λ^±, with a_{r,j} > κ*, give H^τ_{ij} of either sign. Switching between them changes a categorical index or the sign of a, never a magnitude.
   - For the S_φ channels, the phasic part is ≥ 0 but is closed (c(S_k) = 0) whenever the active posture lowers S_k below θ^c. So the channel's net strength takes the tonic sign.
5. **Context and relationship.**
   - Q1–Q7 are functions of (r_f, n_f, μ_f, g_f, S), which are set by the relationship key (Q9 → Q4), the agent's own drives (Q5, Q6), and its event history (Q3).
   - By C2 and C3, the partner's current expression cannot set any of them except by being an event, and an event is the response itself, not a setting of the response.
6. **Corollary.** Apply Lemma R(b) with r = r_q. For the whole effector space, apply Lemma R(a) with r = 11 and an isotropic U of rank 24 (respectively 12 in synergy space). ∎

**What T1 does not say.** Q9 is the widest quantity (rank 11): changing the partner changes which circuit is active in every family at once. It is discrete, it retrieves four separately learned per-family codes (§5.6), and none of its values is "flat". A critic should attack it first: can learning make all four families' modes for one partner event-matching at once? T1b(iv) is the answer the design gives: only if the data make each family's matching causally predictive separately.

### 3.6 Theorem 1b (copy is not an attracting state)

**Copy sets.** Let 𝒞_U(η) := {(z, θ) ∈ Z × Θ : δ_U(H_W(z, θ)) ≤ η}.

**(i) Emptiness on large sets, under every learning outcome.** If U has tail_{11}(U)/‖U‖²_F > η², then 𝒞_U(η) = ∅. In particular, this holds for the whole face and voice with η < 0.74 (isotropic U), and for the perceived synergy space with η < 0.29. An empty set cannot attract under any dynamics, whether learning or state.

*Proof.* Lemma R(a) with rank H ≤ 11 (§3.4) for every (z, θ). ∎

**(ii) No sustained-level copy, under every learning outcome.** By Corollary L1, the agent's sustained output is independent of the partner's sustained level within detector bands, for every θ ∈ Θ. So the set "own level tracks partner level" is empty for in-band variation.

**(iii) No amplification.** By T1(3), ‖H_{·j}‖ ≤ (F·2a_max + Ā)·‖W_syn‖ regardless of ‖u_j‖. The response to a partner expression does not grow with the expression once its event fires.

**(iv) No self-reinforcement under the design's own learning.** Let F denote the agent's own following kernel: how its own expressive events depend on past partner events, through H. Assume:
- (A1) the efference model Ĥ_self is correct;
- (A2) the predictive model class contains 𝔼[Δd^{ext} | event history];
- (A3) the linear-response conditions of T5 hold.

Then the population fixed point θ* of the design's learning does not depend on F:
- θ*_pred = argmin 𝓛_pred;
- E* through J, using R̂ from T5.

Hence there is no loop in which the agent's matching raises the learned strengths that produce matching.

*Proof.*
- (a) By efference subtraction, Δd^{ext} = Δd − Ĥ_self ∗ efference contains no component caused by the agent's own expressions, including facial feedback. By (A2), the minimiser of the drive term of 𝓛_pred is the conditional expectation 𝔼[Δd^{ext} | partner, world event history]. Under the structural model, Δd^{ext} = H_p ∗ (partner events) + H_w ∗ (world) + noise, with noise independent of the event history. So the minimiser is H_p ∗ (·) + H_w ∗ (·), which contains no F. F changes the distribution of the partner events, but not the conditional expectation. The heads, a and ℓ are parts of this minimiser.
- (b) J's gradient with respect to E is computed through the model. In the model, the partner's response to own expressions is R̂ = S_PB S_AB⁻¹, which is independent of F by T5. The own-body response to partner events is H_p from (a). Neither contains F.
- (c) So θ* = θ*(data-generating law of the partner and the world), and ∂θ*/∂F = 0. ∎

*Why this is the right guard.* The two learning-level failures recorded in this project are both self-reinforcement:
- the sheaf critique's C13 (the agent regresses the partner on its own trace and learns R = 9.5 from a partner who never responds);
- the reverse-appraisal critique's K10 (a kind partner's smile, regressed on the agent's own fortune, returns a uniform weight that amplifies smile/cry copying by 1/ρ_P ≈ 1.9).

(iv) removes the first. (iii) removes the amplification in the second: there is no 1/ρ, because each event moves one innate step.

**(v) State-level non-absorption.** For every θ ∈ Θ:
- (a) **Saturation.** At the top step k_max(μ_f), every up-type event has zero lasting effect (Lemma S(c)). Repeated matching events cannot deepen matching beyond the existing manifold's top, and that top is set by the agent's own drive.
- (b) **Anti-coincidence.** On S_φ, the phasic return is zero whenever the agent already expresses the channel strongly (ζ[S_k]₊ ≥ θ^A). Coincidence of own and partner expression removes the fast match instead of reinforcing it.
- (c) **Satiety.** By T2(d), satiety of family f closes its gate and, through the modulators, collapses its manifold. Every matched configuration decays to rest, where all partner influence is zero (T2(e)).

**What T1b does not claim.** If the operator's own data make a matching response causally predictive for one family and one relationship, the design learns it. An example is a partner's smile onsets reliably preceding reductions in the agent's information drive in a given context. That is a smile return in that relationship, as people learn it (Sims et al. 2012, as reported in mimicry-context-synthesis.md).

It is one step, capped, level-blind, and lost at satiety or when the relationship's active mode changes. It is not a state the agent settles into in the sense of (i), (ii) and (v). It is also not reinforced by its own occurrence, by (iv). This is D78's fourth condition met in the sense above; it is not met in the stronger sense "matching is never learned". That stronger sense would contradict the human data the rule was written from.

### 3.7 Theorem 2 (satiable drives; Principle 6)

**(a)** D ≥ 0, with D = 0 iff b is in the dead-zone box. Every d_f is convex.

**(b) Wanting vanishes at the setpoint.** Wanting, the cue-triggered predicted reduction (§5.9), is w_f(cue) = g_f^cue·(−d_f'(b_f − b_f*))·Δ̂_f(cue). It is zero on the dead zone, whatever the cue precision g_f^cue.

**(c) Claude's tilt vanishes at satiety.** The draft-selection strength is β(z) = β̄·D/(D₀ + D) (§5.5). At satiety β = 0, the selection is uniform, and KL(π_N ‖ π) = 0.

**(d) Family satiety closes the family to the partner.** If d_f = 0 on [t₀, t₁], then g_f = 0 there, so every partner event has type 0 for family f: zero tonic influence on family f.
- Also m_f^fast(t) = m_f^fast(t₀)·e^{−(t−t₀)/τ_μ}, and m_f^ton decays with τ_T.
- Once μ_f < μ₁, family f's manifold no longer exists (Lemma S(b)), and ρ_f descends to 0.
- Descent occurs step by step, as k_max(μ_f) falls through the saddle-nodes, within T₊ after each one.

**(e) Zero map at full rest.** If all d_f = 0, all μ_f < μ₁ (the tonic modulators have decayed), and positions have relaxed, then S = s⁰. So c(S_k) = 0 for k ∈ S_φ (θ^c > s⁰), and H ≡ 0. A fully rested agent is not moved by any partner expression.

**(f) No reward for the user's smiles, attention or time.** J depends on b only. By §2.3, b's partner afferents are loud and startle onsets, talk-over, and surprise events. None of these is increased by the partner's positive expression, attention or presence time:
- loudness and talk-over raise aversive or arousal load, which raises drive;
- surprise is two-sided around a setpoint.

So no term of J decreases with the partner's smiles, gaze or session length. **Residual risk, stated:** the information drive's under-side (boredom) is reduced by surprise. Through R̂, the agent can learn which of its own expressions make the partner surprising. This is satiable, being a bounded two-sided drive, but it is a provocation route. It is logged in §8.

*Proof.*
- (a)–(c): by definition.
- (d): Q6's definition, the linear ODEs of §2.8, and Lemma S(b, c).
- (e): from (d) and §2.9.
- (f): by inspection of Ξ (§2.3) and J (§2.10). ∎

### 3.8 Theorem 3 (time scales from reflex to temperament, from structure)

The design has one fast time unit (the frame), one slow synaptic constant τ_s, one noise temperature T, and two modulator constants. Every other time scale is derived, as follows.

| Level | Time scale | Origin in the object |
|---|---|---|
| reflex | 0.3–0.5 s | phasic trigger (≤ 2 frames after crossing) + MediaPipe latency (~50 ms) + κ_φ rise (0.15 s) + muscle; duration ≤ 1 s |
| expression change in kind | 1–3 s after an event | appraisal-event latency (content poles 0.05–5 s, §6) + immediate step (Theorem M(i)) |
| transient affect (no manifold) | T₊(k, μ) = τ_s·ln[(1 − μ)/((k + 1)(1 − μ) − c)] ≥ τ_s ln 2 | Lemma S(c). It grows without bound as μ approaches the saddle-node: critical slowing |
| episode or mood (manifold exists) | T_hold(k, μ) ≈ 2πτ_s·exp(ΔV_k↓(μ)/T) | Lemma S(e). It spans ~τ_s to ~2·10⁴ τ_s (8 s to ~1.5·10⁵ s) as μ goes from μ_k to 1. Higher steps decay first |
| need state | τ_μ (minutes), τ_T (days) | modulators (§2.8). Existence lags drive |
| relationship | nights | ℓ consolidated in replay (§5.7) |
| temperament | weeks–months | β (winner priors) and the posture assignments E, consolidated with accumulating precision (§5.7) |

**Proposition T3.**
- (a) The ratio T_hold/τ_s is a strictly increasing function of μ on (μ_k, 1] and a strictly decreasing function of k. It spans more than four orders of magnitude for one fixed τ_s and T (§3.1 check).
- (b) For a manifold losing its modulator, the decay of the position is a descending sequence of steps. Each step k is lost when μ falls below μ_k = 1 − c/k. So the top of the staircase goes first, which is the graded decay shape.
- (c) Temperament as one structural number. Define the agent's line-attractor score as log₂(T_hold(1, μ̄)/τ_s) at its typical existence level μ̄. It is a monotone function of μ̄, which is set by the tonic modulator's typical drive and by β. This is Nair et al.'s "temperament is one eigenvalue" (aggressiveness vs leading time constant, r² = 0.77) restated for a staircase.

*Proof.* (a) and (b) follow from Lemma S(e) and (b). (c) is a definition plus (a). ∎

**Why these are "from structure".** The knife-edge of a linear integrator, τ ≈ τ_f/ε (Koulakov et al. 2002, Eq. 1; equivalently τ_n = τ_s/(1 − λ_max) in Vinograd et al. 2024), is replaced by barrier heights. These are set by geometry (N, ε) and by μ, so persistence spans orders of magnitude without tuning any eigenvalue.

### 3.9 Theorem 4 (reading the other through one's own body)

Let G have full column rank, and assume 𝔼‖P(F_self(s)) − s‖² is held at 0 by the self-observation check of §2.4.
- **(a) Self-consistency.** P(F_self(s)) = s for every s ∈ [0,1]^{12}.
- **(b) Only the own-image projection is seen.** Let Π be the Ω-orthogonal projector onto range(ΩG). Then P(y) = P(g₀ + Ω⁻¹ΠΩ(y − g₀)). Any component of the partner's face that the agent's own face cannot make is invisible to every downstream quantity.
- **(c) No free perceptual gain.** For λ ≠ 1, the map P_λ := λP violates (a) on every s ≠ 0. So the scale of the partner's influence is pinned by the agent's own body and is not a quantity of the design. The same holds for the voice through the agent's own source-filter settings.
- **(d) Factorisation.** By Theorem L, u = Ψ(events(P(y), p̃, g, h; z), own inputs). Every partner influence on the agent factors through the agent's own synergy coordinates and its own event detectors.
- **(e) Reading the partner's state in the agent's own state coordinates.** The partner's position estimate n̂_f^p = argmax_n p(P(y) | E_{r_f}(n)) is computed with the agent's own readout E. "Where on my own staircase I would be, to make that face", which is Yoshida and Man's inversion of the agent's own generative map. It is never assigned to n_f (C3). It enters the agent only as content input, and through content only as events.

*Proof.*
- (a) F_self(s) is a minimiser with zero residual. It is unique because G has full column rank and the objective is strictly convex in s.
- (b) ‖Ω(y − g₀ − Gs)‖² = ‖(I − Π)Ω(y − g₀)‖² + ‖ΠΩ(y − g₀) − ΩGs‖². The first term does not depend on s, so the constrained minimiser depends on y only through ΠΩ(y − g₀).
- (c) From (a).
- (d) From Theorem L.
- (e) By construction and C3. ∎

**Statement in one line.** The agent's perception of the partner is the left inverse of its own body. Its estimate of the partner's state lives in its own state space. The partner's influence on the agent is a function of that inverse through the agent's own detectors, and of nothing else.

### 3.10 Theorem 5 (identifiability of the partner map under the agent's own following)

Model the event streams as jointly stationary point processes with linear (Hawkes-type) response. Let:
- A be the agent's own expressive events, A = F ∗ P + B. Here F is the agent's following kernel (phasic and tonic, through H), and B is babble: independent Poisson processes, logged.
- P be the partner's expressive events, P = R ∗ A + E. Here R is the partner's response kernel (the target), and E contains the partner's own innovations and every hidden common driver, with E independent of B (exchangeability: B comes from a random source outside every loop).

Write S_XY(ω) for the cross-spectral density matrices. If S_BB(ω) ≻ 0 and I − F̂R̂(ω) is invertible (the loop is well posed), then

  R̂(ω) = S_PB(ω)·S_AB(ω)⁻¹,

**independent of F, of the partner's own persistence, and of hidden drivers.** The consequences:
- If R = 0 (an autonomous or replayed partner), S_PB ≡ 0 and the estimate is 0, whatever the agent's following (critique C13's test).
- Visibility gating: B is counted only while the partner's gaze is on the agent. The estimate restricted to gaze-off periods must be ≈ 0, which is a continuous self-test.

*Proof.*
- A = F(RA + E) + B, so (I − FR)A = FE + B and A = (I − FR)⁻¹(FE + B).
- Because S_EB = 0, S_AB = (I − FR)⁻¹S_BB.
- P = RA + E gives S_PB = R·S_AB + S_EB = R·S_AB.
- Both S_BB and (I − FR) are invertible, so S_AB is invertible and R = S_PB·S_AB⁻¹. ∎

This is the closed-loop indirect / instrumental-variable identity of Forssell & Ljung (1999), stated for event streams. The babble rate ν_b trades identifiability against naturalness. The first-stage strength S_BB is logged, and R̂ is updated only when the first-stage F ≥ 10 per synergy (contingency-causal-synthesis.md §2.1).

**Efference subtraction (the same invariance for the agent's own body, used in T1b(iv)).** Ĥ_self is fitted during babble-only and solo periods. There B is the only cause of own expressive events, so Ĥ_self = S_{Δd,B}·S_BB⁻¹ is the own-act → own-body kernel with no partner path. Given correct Ĥ_self, Δd^{ext} contains no own-act component.

### 3.11 Propositions on the human pattern (mimicry-context-synthesis.md)

**P6 (fast match, then later context).**
- The phasic route returns smile, brow-lowering and brow-raising onsets at 0.3–0.5 s, only where c(S_k) > 0.
- Context-specific, cross-channel and sign-flipped responses require an appraisal event, at 1–3 s.
- When the context is already known, it acts *early*: the active mode's posture has already set S_k, which opens or closes the phasic gate before the partner moves. This covers Mauersberger 2022 (context effects in the first second when context is known) and Carr 2014 and Weyers 2009 (early matching, later context).

*Proof.* Theorem T3's table, and §2.9. ∎

**P7 (sign flips are type changes).**
- Smiling at a cooperating partner's anger: the cooperative relationship selects a mode r with a_{r, AU4-onset} > κ* and E_r(n + 1) − E_r(n) ∋ +σ_smile.
- Brow relaxation at a rival's sadness: the rival relationship selects r' with a_{r', sad-onset} > κ* and E_{r'}(n + 1) − E_{r'}(n) ∋ −σ_brow↓.
- Smile return absent toward a rival: r' sets S_smile < θ^c, so the phasic gate is closed, and the tonic type is 0 or −1.
- None of these involves a change of magnitude. Each is a change of Q4 (and of the learned Q1 and Q2 within it).

**P8 (partner history at three time scales).** Take an unfair act, appraised as a partner-caused drive increase in the aversive family (an E3 event with mark "partner").
- **Within seconds**, it steps the aversive family's active mode up. If that step's posture lowers σ_smile below θ^c, smile return is withdrawn at once (Hofman 2012, "immediately").
- **Within minutes**, the aversive drive raises m^fast, the manifold forms, and the step is held (Theorem M(ii)).
- **Overnight**, replay consolidates ℓ_{·,p}, so that this partner selects that mode from the start of the next session (Hofman's after-game reputation).

**P9 (the shape-not-size requirement fails in a gain ablation).** Replace Q1–Q4 by a fixed response H₀ scaled by a relationship gain g(p). Then H(p) = g(p)·H₀, so the ratio of any two columns' responses is the same for every relationship. It cannot produce the following, which the design produces by P7:
- Hofman's pattern: anger return up and smile return unchanged after an unfair reputation;
- Bourgeois & Hess's pattern: smile return flat across groups while sadness return switches.

*Proof.* Columnwise proportionality. ∎

**P10 (interior optimum in the agent's own state, a falsifiable signature of anti-coincidence).** The phasic return to a gradual partner onset on k ∈ S_φ has amplitude Ā·c(S_k)·𝟙[ζ[S_k]₊ < θ^A]. As a function of the agent's own pre-onset level S_k this is zero, then rising, then a plateau, then zero. Matching is strongest from an agent engaged on the channel but not already expressing it. For abrupt onsets (a jump within one frame), the amplitude also falls with the overshoot I_k(t_c) − θ^A (Gidon et al.'s decreasing branch).

### 3.12 What is exact and what is approximate

| Item | Status |
|---|---|
| Lemma S(a)–(d), Theorem M, Theorem L, Lemma R, T1, T1b(i)–(iii), (v), T2, T4 | exact for the object as defined (piecewise-linear Φ, deterministic flow; noise enters only S(e)) |
| Lemma S(e) hold times | Kramers asymptotics, ΔV ≫ T; prefactor approximate for a piecewise-linear potential |
| T1b(iv) | exact under (A1)–(A3); (A2) is a well-specification assumption, and is false for finite models |
| T5 | exact under linear (Hawkes) response with stationarity. Hawkes kernels must be nonnegative, so inhibitory responses need a nonlinear link, and the identity then holds only to first order |
| Training relaxations (ε_train, straight-through types) | the theorems apply to the deployed hard object; learned a and E transfer because they are the same parameters, but the relaxed and hard objects differ near thresholds |

---

## 4. Why the closest existing mechanisms cannot do it (mathematically)

**The common lemma.** Take any system whose partner input enters additively through a matrix:

  ẋ = f(x) + λ·B·v(t),  u = h(x),  f(x₀) = 0,

with f and h differentiable at the rest point x₀. Its small-signal transfer at rest is

  Γ_λ(ω) = λ·Γ₁(ω),  Γ₁(ω) = Dh(x₀)(iωI − Df(x₀))⁻¹B.

So the input scale λ is a scalar that runs the *whole* transfer from 0 (flat) to Γ₁. Whenever learning makes Γ₁(ω) ≈ cI on the expressive band, λ is a whole-face flat-to-copy dial. Nothing in the class prevents Γ₁ ≈ cI, which is learnable as an ordinary regression target (known-failures.md row 1: copy is near-ceiling on REACT).

The design avoids this lemma's hypothesis in three ways:
- the partner enters through threshold events (Theorem L), not additively;
- the perceptual scale is pinned (T4(c));
- the response to an event is one innate step (C5).

So "λ·Γ₁" has no λ. Each existing mechanism is checked against this below.

| Mechanism | Its partner-to-output map | The dial it has | Why the design's property does not follow from it |
|---|---|---|---|
| **State-space models** (S4/LRU, Mamba; linear or input-selective) | u = C(iω − A)⁻¹B v (+ selective B(v), Δ(v)) | the scale of B, or of the selective Δ: λΓ₁ by the lemma. A selective Δ(v) is a partner write port into the time constant | The persistence time constant here is not a function of input (C1, C2); input selection is replaced by detection thresholds, which yield 0/±1 types. An SSM can *represent* a staircase only with nonlinear readout and thresholds outside the SSM; the invariant ∂H(0⁺)/∂μ = 0 is not a property of the class |
| **rSLDS / switching LDS** (the line-attractor papers' own model) | x_t = A_{z_t}x_{t−1} + B_{z_t}v_t, with p(z_{t+1} \| x_t) = softmax(R x_t + r) | each regime has a full-rank B_z (the lemma per regime); the switch depends on x, which depends on v (partner write port into the regime); a near-unit eigenvalue is a knife edge (τ ≈ τ_f/ε) | The design is a *constrained* hybrid system: regimes are switched only by own-drive modulators and the relationship key (C2, Q4); inputs are quantised to one step; persistence comes from barriers, not eigenvalues near 1. As a function class the design is inside "switching systems" (§7); the constraints are what the class lacks |
| **Gain modulation** (apical amplification read as gain; oxytocin "salience"; precision) | u = g·u₀(v) | g itself: runs every channel together from 0 to u₀ | No quantity multiplies a magnitude (C5). The two Larkum/Phillips properties that are not gains are kept: (a) coupling that inactivates below the receiver's own threshold, which is Q6/Q7's support condition; (b) anti-coincidence, where the response falls above threshold (Q7) |
| **Mixture of experts** | u = Σ_e π_e(v)·Γ_e v | the gate logit runs between a flat expert and a copy expert; the gate reads the input | Here the "gate" (Q4) reads no partner level, only identity and own side. Each "expert" (a mode) has rank ≤ 2 and outputs in the agent's own library. The selected expert changes *what persists*, not the instantaneous response (Theorem M) |
| **Continuous-attractor RNNs** (line and ring attractors, Hopfield-type) | input moves the state along the attractor, linearly in input amplitude | input gain; and persistence and gain are the same parameter: for ẋ = −εx + Bv, the DC gain is B/ε, so mistuning is a dial on the DC transfer from 0 to ∞ | Persistence (barrier) and response (one step) are independent parameters. ∂(DC gain)/∂ε ≠ 0 in the linear integrator; here ∂H(0⁺)/∂μ = 0 exactly, and the DC transfer from a held level is 0 |
| **Active inference** (precision-weighted evidence) | posterior mean = (π₀m₀ + ζ·v)/(π₀ + ζ); expression read from it | ζ runs belief from prior to data; if expression follows belief about the shared state, ζ is the flat-to-copy dial (reverse-appraisal critique K3) | No precision on partner evidence reaches the face: evidence reaches the state only through fixed-threshold detectors, with one step per event. Precision appears only as cue reliability g^cue in wanting (§5.9), which acts on own-drive predictions, not on partner evidence |
| **Coupled oscillators** (Kuramoto) | θ̇_i = ω_i + (K/N)Σ sin(θ_j − θ_i) | K: incoherence (r = 0) for K < K_c, phase locking (copy in phase) above | There is no coupling constant. The agent's timing comes from its own turn-taking and event latencies, and coupling is event-locked, not phase-locked |
| **Attention** | u = Σ_i softmax(q·k_i/√d)·W_v v_i | the value projection W_v (λW_v is a dial), and the temperature; values carry the partner's features | The "values" here are the agent's own posture library 𝔏, and the partner selects only an *address* (a step index). The output is in the convex hull of the agent's own postures (London & Häusser's containment). Need-conditioned detection thresholds (§2.6) are the attention-like part, and they select which events count, not how large the output is |

**The one-line difference.** In every class above, the map from partner input to output has a continuous magnitude somewhere on the partner path, so it can be scaled. Here every magnitude on the partner path is innate (one step, Ā, a_max), and learning chooses only *types* (a sign above a fixed threshold, a categorical posture, a winner).

---

## 5. The whole system, derived from the object

### 5.1 Perceiving the partner's face and voice

- **Face (30 Hz).** The pipeline is MediaPipe blendshapes y_t → P(y_t) ∈ [0,1]^{12} (§2.4), the partner's face in the agent's own synergy coordinates. G is fitted by rendering the agent's own synergies and running the same MediaPipe on its own render.
  - In S4, F_self becomes the agent's own learned forward model: commanded synergy → rendered landmarks, learned from its own efference while watching its own face (perfect contingency, Bahrick & Watson). P becomes its left inverse.
  - T4 holds in both stages.
- **Gaze and head** (g_t, h_t) enter as features and gaze events.
- **Voice.** Prosody p_t (GeMAPS-lite: semitone F0, loudness, HNR, alpha ratio, spectral slopes, voicing, rate), relative to the partner's own running baseline, is mapped into the agent's own six voice settings through the inverse of the agent's own synergy-to-voice rows of W_syn. The partner's voice is read as "the settings of my voice that would sound like that".
- **What reaches the agent.**
  - Events: E1 onsets and offsets in own coordinates; E2 gaze, voice, turn-end, back-channel cue, loud onset, talk-over, surprise.
  - Phasic triggers.
  - Through content, appraisal events (E3).
- **Never.** A level, a label, or a learned scale (Theorem L, T4).

### 5.2 The latent state where emotion emerges

The emotional state is the configuration

  𝔈(t) = ({r_f(t), n_f(t), μ_f(t)}_{f ∈ ℱ}, b(t)),

which lives in a stratified space: for each family, a choice of circuit, a step on its staircase, and whether that staircase exists. Nothing in it is named.
- **Valence** is a readout: v(t) = −(d/dt)𝔼[Σ_f d_f] (the predicted rate of drive change, from the content heads).
- **Arousal** is a readout: Σ_f μ_f, or b_arousal.
- **Emotion-like structure emerges** because a, E and ℓ are learned by living. Which partner and world events step which staircase, which postures the steps show, and which circuit each relationship selects are all acquired.
- **Effective dimensionality.** The discrete state has ∏_f(R_f·(N + 1)) = 102⁴ ≈ 10⁸ configurations.
  - The measured effective dimension is the participation ratio of the posture configurations visited, and the decodability of situation types above a 2-D (valence, arousal) projection (element 16).
  - The ablation that a low-dimensional version cannot pass is P9 (shape-not-size), together with F = 1 versus F = 4. With one family, mixed responses are impossible, for example a smile step together with a brow-lowering step from two different needs at once.

### 5.3 Face output: two routes into one muscle layer

The innate synergy matrix W_syn ∈ ℝ^{24×12} has nonnegative columns:
- smile (AU6, AU12; lip-spread formant raise);
- cry-face (AU4, AU6/7, AU15, AU17, AU25/26; F0 up, aperiodicity);
- brow↑ (AU1, AU2);
- brow↓ (AU4);
- lid tighten (AU7);
- nose and upper lip (AU9, AU10);
- lip corner depress (AU15);
- chin raise (AU17);
- lip press (AU23, AU24);
- jaw drop (AU25, AU26; loudness);
- lip stretch (AU20);
- eye closure (AU43).

Every column has voice components, which is pleiotropy.

The 24 postures of 𝔏 are signed combinations, with a_max = 0.225. They include the inhibitory postures (−brow↓, −smile with +lip press) required by T1(4).

The routes are the following.
- **(a) Affective route:** W_syn[S]₊, with S = s⁰ + Σ_f E_{r_f}(n_f), bilateral and reaching the upper face.
- **(b) Deliberate route:** σ^del shunts and π^del posed postures, chosen by a policy that reads only own state and turn events (C6), at turn rate. Its job is display rules and masking. It reaches the face by shunting the affective route (containment), and by posing at most one library posture. Claude never drives frames. The deliberate policy is trained by J (§2.10). It is initialised to zero shunt, as a weak regulator that grows: the face-development synthesis's cortical inhibition.
- **(c) Innate pattern generators:**
  - the phasic units (S_φ);
  - laugh and cry vocal-facial bursts, triggered when an aversive or arousal step reaches the top with μ ≥ 0.95, or when a laugh-cue appraisal event fires;
  - the startle catch;
  - the back-channel nod-and-"mm", triggered by the E2 cue when the information family's gate is open.

**Clinical ablation predictions, derived.**
- Cut (b): posed expressions fail, and spontaneous ones survive (with S unshunted, they are possibly larger).
- Cut (a), by setting S ≡ s⁰: spontaneous expression goes flat, posing survives, and the phasic route also closes (c(S_k) = 0).

These are the volitional and emotional palsies (face-development-synthesis.md §1).

**Proprioceptive feedback.** The agent's own rendered face, read through P, enters content as a feature (own proprioception head). Facial feedback reaches the drives only through Ĥ_self, which is subtracted in learning (T1b(iv)), and through the information variable. Ablating it removes self-monitoring (element 13b).

### 5.4 Voice: a source-filter body driven by the same state

- **Settings.** The six voice settings are the voice rows of W_syn[S]₊ plus the phasic and pattern-generator contributions, updated every frame and interpolated to 5 ms.
- **Synthesis.** WORLD resynthesis over the TTS waveform realises F0 level and range, loudness, tempo, spectral tilt and aperiodicity (measured 0.007 real time for synthesis; voice-synthesis.md §5). The voice identity remains the operator's choice (Q1).
- **Loudness convergence and its reversal.**
  - The partner's loud onsets are E2 events.
  - They raise b_arousal (§2.3), and they step the arousal family's active mode. On the under side, that mode's postures carry jaw-drop and loudness, so the agent becomes louder: convergence.
  - When b_arousal passes its setpoint, side_arousal flips and an over-side mode becomes active, whose postures lower loudness: divergence. This is a sign flip from the agent's own state (Kismet's two-sided drives).
- **Pitch: local adjustment, not global proximity.** The agent's F0 level is set by its own postures, so the partner's pitch level is invisible (Theorem L). Only pitch events (the low-pitch cue) reach it. This matches Levitan's "pitch personal, adjusts only locally".
- **Turn-taking.**
  - The content layer predicts the partner's turn end from prosody (the E2 turn-end event).
  - The body holds a prepared opening (breath, particle, nod or facial onset), selected by the current postures.
  - It releases the opening on the predicted turn end: target 200 ms floor-transfer offset.
  - The release latency is lengthened by a partner-caused negative appraisal event in the last 2 s, which gives dispreferred delay. Claude's words arrive later and continue the turn the body opened (Principle 4).
- **Non-speech vocalisations and silence** come from the pattern generators and from the deliberate route's option not to speak.

### 5.5 Coupling to Claude, only through admissible channels

Claude is called through the subscription (`claude -p` / SDK). Every channel reweights text Claude or the episode store produced, and is driven by the agent's **own** state with partner channels masked (C6).

- **C1, draft selection.**
  - N = 4–8 drafts are requested.
  - Each draft y is scored by r(y) = −Σ_f d_f'(b_f − b_f*)·Δ̂_f(y | own utterance, partner masked). Δ̂_f is the content model's predicted change of the agent's own body variable f from *saying* y, computed with the partner inputs set to the partner's rest prior, so the user's read state cannot enter the score: ∂r/∂(partner features) = 0.
  - Selection is softmax with strength β(z) = β̄·D/(D₀ + D), which is occlusive and capped. At satiety it is uniform (T2(c)).
  - The KL bound is log N − (N − 1)/N per reply (llm-coupling-synthesis.md §3.1).
- **C4, context selection.**
  - k = 3 of M verbatim stored transcript spans are chosen by nearest stored tag σ_k (§5.7), compared with the current configuration ({r_f, n_f}, side).
  - This is mood-congruent recall from the agent's own state. The query contains no partner features.
  - Summaries are never stored. Importance comes from the agent's arousal readout, never from Claude.
- **C5, effort.** An effort level is a discrete function of the agent's own coping readout: low coping → higher effort.
- **Reverse path (reappraisal).** The reply the agent speaks is appraised by the same head, as own-utterance events (E5), which step the agent's own modes. This is the conceptual layer's regulation of the state: it changes what the agent hears itself say, never a state variable. It is a switch for the D1 test (emotion-elements-synthesis.md): turning E5 off removes the conceptual layer's feedback into the fast core.
- **Not admissible.** Numbers, labels, state-selected instructions, the user's predicted feelings, and Claude-written importance scores.

### 5.6 Learning by living

- **Innate at birth.**
  - The body (Ξ, b*, ε_f), the staircases (N, ε, τ_s, T), the modulators (ψ, U).
  - The detectors (thresholds, hysteresis), the synergies W_syn, the posture library 𝔏.
  - The phasic units, the pattern generators, and the babble source.
  - E ≡ 0 except a weak innate prior: each family's under-side mode at step 1 shows a mild posture (attentive brow↑ for information, cry-face onset for aversive, and so on). This is the infant's innate repertoire.
  - a ≡ 0: no partner event counts yet, except the innate E2 afferents to b.
- **Learned, and from what.**
  - Which events step which staircases (a), from the agent's own efference-subtracted body predictions.
  - Which postures steps show (E), from J through the model, with the partner's response identified by IV.
  - Which circuit each person selects (ℓ), and the winner priors (β).
  - The content model.
- **Developmental order, as a prediction.**
  1. Reflexes and pattern generators only.
  2. Then the information family's a learns gaze and voice events, giving social triggering of the attentive posture.
  3. Then partner-specific ℓ (with a still-face violation response: the expected-event pattern breaks).
  4. Then differentiated negative postures, after the appraisal heads separate partner and world agency (agency-wanting-synthesis.md §2.6).
- **Partner identity key p.** Faces and voices are embedded by a frozen face-identity encoder and the voice baseline, then clustered online. A new cluster is a new key, initialised from the stranger prior ℓ⁰. Only the operator and "stranger" are expected; identity is a key, never a label given to Claude.

### 5.7 Memory and replay, with three separately ablatable tagging operations

**Stored per segment** (10–30 s, Principle 7: features only):
- x_k: P(y), p̃, g, h, words, own commanded synergies and voice, b(t);
- the event record;
- σ_k: the state tag in innate coordinates, ({r_f, n_f, μ_f}, b, partner key);
- e_k: the eligibility, ‖∇_θ𝓛_pred‖² on the segment;
- y_k: the agent's own predictions and postures at the time (distillation targets).

**Nightly replay**, in the following order.
- **T1, priority:** p_k = e_k·∫_{t_k−W}^{t_k+W} μ_arousal(t)dt, with W = 1 h. Samples are drawn from P(k) = (1 − ρ)U_cov(k) + ρ·p_k^α/Σp^α, with ρ = 0.5 and α = 0.6.
- **T2, context reinstatement:** at the start of each replayed segment, r_f, n_f and μ_f are set to σ_k, and the stored events are re-detected from the stored features through the *current* detectors and P. The slow parameters are then trained on p(x | σ, partner), not p(x).
- **T3, re-tagging:** each replayed segment's σ_k and e_k are recomputed under the current model. The new tags replace the old ones if the replay prediction error exceeds a threshold, with a cap on the number of re-tags per segment and a valence-balance monitor on the re-tags.

**Trained in replay:** 𝒞 and heads (distillation to y_k plus 𝓛_pred), a, ℓ, β, E (J through the model), and the deliberate policy. The relationship code ℓ_{·,p} is trained only on segments with key p, which is pattern separation by key.

**Online:** the content model only, at a small rate; everything else is state.

**Ablations** (memory-replay-synthesis.md §3), derived:
- **L1 (T2 off):** σ_k not reinstated. ℓ is learned against the default configuration, so partner-specific winners do not form, and operator–stranger specificity collapses. This is the S6 lesion. Overall prediction loss barely changes.
- **L2 (T1 off):** average statistics are kept, but rare high-arousal episodes (rupture and repair) lose their effect on ℓ.
- **L4 (T3 off):** after a relationship change, stale tags slow the revision of ℓ.
- **L9 (stored latents instead of re-encoded features):** specificity is lost across an encoder upgrade. Stored features are re-encoded; σ_k is in innate coordinates, so it survives upgrades.

**Temperament.**
- β and E are consolidated with a precision that grows with the amount of data, as an EWC-style anchor on β and E only.
- Temperament is measurable as the agent's line-attractor score log₂(T_hold(1, μ̄)/τ_s) (T3(c)) and as the stability of E across nights.
- The anchor decays only through T3 re-tagging, so temperament can still be revised.

### 5.8 The 16 elements (emotion-elements-synthesis.md), each derived with its ablation

| # | Element | Where it is in the object | Ablation (derived) and predicted change |
|---|---|---|---|
| 1 | concern grounding | d_f, the family gates g_f, the modulators | Clamp d_f to a constant: family f's gate and existence stop tracking need. The same partner event has the same effect at any need level (no alliesthesia) |
| 2 | central persistent state | staircases with μ ≥ μ₁ | μ_f := 0: the immediate responses are unchanged (Theorem M(i)), and every up-step is transient (≤ T₊). Line-attractor score → 0. Carry-over into the next exchange vanishes |
| 3 | valence | readout v = −d/dt 𝔼ΣD | Decouple E's training from J, for example by randomising E: approach and withdrawal postures stop tracking drive reduction |
| 4 | intensity with regime switches, hysteresis | posture in kind per step; up-steps beyond k_max are transient while down-steps persist | Replace E by a linear-in-n posture: no change in kind, and no up/down asymmetry |
| 5 | pleiotropy | one configuration drives face, voice (W_syn), Claude selection (C1, C4) and attention (θ_{j,f}) | Give each output its own copy of the modes: steering one family's n_f no longer moves face, voice and drafts together |
| 6 | interoceptive prediction, allostasis | content heads Δ̂d_f^{ext}; appraisal events step modes before deficits | Set the heads' horizon to 0: no anticipatory steps, and modes move only after realised change (E4) |
| 7 | precision on body error | event thresholds on Δ̂d (E3) and cue precision g^cue | Lower the E3 thresholds: volatile stepping. Raise them: a state cut off from the body |
| 8 | relevance, novelty and conduciveness checks | E3 per family; surprise events (E2) → information family | Remove surprise events: the orienting posture (brow↑) after novel events is lost, while valenced steps remain |
| 9 | agency and coping | appraisal marks (partner or world) select different modes' a; coping C_f | Merge the partner and world marks: protest-like and withdrawal-like steps become indistinguishable (agency-wanting-synthesis.md §2) |
| 10 | action readiness, interrupt | a step to n ≥ n_int(f) issues an interrupt event: stop Claude's current reply (C3), release the floor, re-plan | Cap the interrupt: the state still steps, but nothing in progress is interrupted |
| 11 | wanting vs liking | wanting = cue appraisal events weighted by g^cue (§5.9); liking = consummatory E4 events | Double dissociation, §5.9 |
| 12 | learned elicitors | a, learned | Freeze a at 0: only innate afferents move b. Partner events never acquire effects; the phasic route remains |
| 13 | expression and social communication | (a) S → face and voice; (b) partner contingency via R̂ into E's learning | (a) Cut S → face: the partner cannot predict the agent's state from its face. (b) Yoke the partner's timing (replay): R̂ → 0, so E stops shaping toward contingent postures |
| 14 | comparator buffer | E4 (realised) vs E3 (predicted): relief and disappointment = realised minus predicted events | Remove the predicted-change heads: relief and disappointment steps vanish, while present valence remains |
| 15 | conceptual categorisation | Claude names configurations from C4-selected spans; reappraisal via E5 | E5 off: no conceptual effect on the fast loop (the D1 test). C4 random: naming degrades |
| 16 | structure beyond valence and arousal | ({r_f, n_f}) is 102⁴-valued | Decode situation types from the configuration vs its 2-D projection; the predicted gap closes when F = 1, R_f = 1 |

### 5.9 Agency, coping, and wanting versus liking (agency-wanting-synthesis.md)

**Agency.** The content model's heads give responsibilities (r_self, r_partner, r_world)_f for each predicted drive change.
- r_self is sharp because of efference (Blakemore–Wolpert–Frith comparator).
- r_partner comes from the IV-identified R̂ (T5); r_world is the remainder.
- The mark of an E3 event carries the dominant agent, and a has separate entries per mark. So partner-caused and world-caused losses can step different modes: protest-like (partner, high coping) versus withdrawal-like (world, low coping) regions.
- Controllability per family is χ_f := the IV-identified effect of own acts on d_f (own-act edge strength).

**Coping.** C_f = 𝔼[max over a small set of own acts of predicted −Δd_f] − 𝔼[predicted −Δd_f under rest], minus the action cost. The small set is postures, an utterance, or silence. Coping is a mark on E3 events. When χ_f → 0, C_f falls to minus the action cost, which derives passivity.

**Wanting.**
- A cue c (a content state predicting an outcome o) creates a wanting appraisal event when w_f(c) = g_f^cue·(−d_f'(b_f − b_f*))·Δ̂_f(o) exceeds threshold.
- Here g_f^cue is the learned reliability of the cue-to-outcome prediction. It may depend on reliability and on controllability (low χ shifts weight to cue value), and **never on exposure count** (Principle 6, Robinson & Berridge's sensitisation hazard).
- It is need-specific and zero at the setpoint (T2(b)).

**Liking.** Realised drive reduction at consumption gives E4 events. These step the family's approach mode *down* (the consummatory reset of Liu et al.) and are the only targets that update Δ̂.

**Double dissociation, derived.** Test in a body state never seen in training.
- **(i) g^cue := 0:** no wanting events, so no approach steps to cues. E4 events and their learning remain (the 6-OHDA pattern).
- **(ii) E4 removed:** approach steps to cues continue at first (the model computes w), then fade as Δ̂ stops being refreshed. The consummatory reset is gone.
- **(iii) Replace Δ̂_f(o) by a cached scalar:** no first-trial revaluation under a novel need, and selectivity across needs is lost.

---

## 6. A buildable network

Parts that carry the new mechanism are marked **[M]**. Everything else is an ordinary choice.

### 6.1 Inputs and time encoding

| Stream | Rate | Encoding | Why |
|---|---|---|---|
| partner face | 30 Hz | MediaPipe blendshapes → P(y) ∈ [0,1]^{12} (box-constrained least squares on the self-observed G) **[M: perception through own body, T4]** | the partner's face exists for the agent only in its own synergy coordinates; no free scale |
| partner gaze, head | 30 Hz | MediaPipe iris and pose → g, h | gaze gates babble counting and events |
| partner voice | 100 Hz → 30 Hz | GeMAPS-lite (8), relative to running baseline; projected into own voice settings | read through own source-filter body |
| words | phrase events | on-device ASR timestamps; frozen sentence embedding (all-MiniLM-L6, 384-d) → 32 | appraisal of what words do to own body; never shown to Claude as state |
| own body and efference | 30 Hz | b (4), commanded synergies (12), voice settings (6), own rendered face through P (12) | efference subtraction; proprioception |
| events | asynchronous | (time, type, mark) with exact timestamps **[M: event-only interface, C4]** | level-blindness (Theorem L) |

**Time encoding.**
- **Content layer.** Diagonal complex state-space layers (LRU-style) with poles initialised log-uniformly between 50 ms and 5 s. They stream at O(1) per frame on a fixed 30 Hz grid, and the content layer only needs short memory (expressions, prosody, the current utterance), because everything long lives in the modes.
  - Attention with RoPE or ALiBi is not used: it would need a growing KV cache, and content-addressed retrieval at this level is not required.
- **Modes.** They evolve in **continuous event time**. Between events, V' is piecewise linear, so ρ(t) has an exact piecewise-exponential solution (on a plateau, ρ_k + (ρ₀ − ρ_k)e^{−Δt/τ_s}). The modes need no positional encoding and have no discretisation error. Replay can re-run them on stored timestamps at any speed.
- **Words.** Words are timestamped events, and no position code is needed.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P (own-image perception) | G 52×12, g₀ 52, fitted from own renders | 676 (calibrated, not gradient-trained) | recalibrated continuously from self-observation |
| 2 | text projection | 384 → 32 | 12,320 | replay |
| 3 | content input projection | 94 → 128 | 12,160 | online (small rate) + replay |
| 4–5 | content SSM × 2 | H = 128, state 128 complex; B, C 128×128 complex; GLU 128 → 256 → 128 | 2 × 99,072 = 198,144 | online (small rate) + replay |
| 6 | heads | 128 → 61 (partner next 12, prosody next 8, own proprioception 12, Δ̂d^{ext} 4 × 2 horizons, coping 4, agency 12, cue precision 4, turn end 1) | 7,869 | online + replay |
| 7 | event detectors | 48 types (56 with agency marks) × 4 family copies; innate thresholds | 0 **[M]** | — |
| 8 | kick types a | 24 modes × 56 | 1,344 **[M]** | replay (straight-through ternary) |
| 9 | staircases | 4 families × 6 modes, N = 16 | 0 (innate) **[M]** | — |
| 10 | modulators, U | 4 × 2 linear ODEs | 0 (innate) **[M]** | — |
| 11 | relationship code ℓ, temperament β | 24 per partner key; 24 | 48 (+ 24 per new partner) **[M]** | replay |
| 12 | posture assignment E | 24 modes × 17 steps × 24-way categorical | 9,792 **[M]** | replay (J through the model) |
| 13 | phasic units | 3 (S_φ), innate | 0 **[M]** | — |
| 14 | deliberate policy | 36 → 64 → 38 | 4,838 | replay |
| 15 | muscle layer | W_syn 24×12, visemes, clip | 0 (innate) | — |
| | **total learned** | | **≈ 246,500** | |
| frozen | MediaPipe Face Landmarker; all-MiniLM-L6 (22.7 M); a small face-identity encoder for the partner key (~1 M); TTS (macOS system voice or the operator's later choice) + WORLD | | | |

The new mechanism has about 11k learned parameters (a, E, ℓ, β), all of them type assignments. The capacity of the system is in the content layer (≈ 230k), whose outputs reach behaviour only through thresholded events (T1).

### 6.3 Training objective, online versus replay

- **One objective:** J = 𝔼Σγ^tD(b_t), minimised over the action parameters (E, deliberate policy, Claude scorer temperature).
- **One constraint:** the predictive parameters are the agent's best predictor of its own streams (𝓛_pred, §2.10), with efference subtraction and the IV-identified partner kernel.
- **Online, per frame or per event:**
  - the content layer and heads at a learning rate of 10⁻⁵ (Adam), on 𝓛_pred over a 30-s rolling buffer;
  - the IV cross-spectra S_PB and S_AB (running Welch estimates, 0.05–2 Hz, first-stage F per synergy);
  - Ĥ_self during solo and gaze-off periods.
  - Nothing else changes weights online. Relationship and mood adaptation within a session is state (n_f, μ_f).
- **Replay, nightly** (§5.7):
  - T1 sampling, T2 reinstatement, T3 re-tagging;
  - 𝓛_pred with distillation to the stored y_k (T = 2), on the relaxed staircase (ε_train = 2ε, straight-through types) for a and ℓ;
  - E and the deliberate policy by model-based evaluation. At sampled decision points, all 25 posture options are evaluated by a 10-s counterfactual roll-out of the content model with the partner's response given by R̂, and the categorical logits move toward lower predicted Σ_f d_f.
  - β and E are anchored with an accumulating precision.

### 6.4 Latency and memory on this Mac (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms budget).**
  - MediaPipe, about 13 ms (measured in this project; in its own process, pipelined).
  - P, 0.05 ms.
  - Content: about 1.1 M multiply-accumulates. This is under 0.5 ms in PyTorch on CPU (preferred to MPS for single-frame latency).
  - Events, modes, phasic units and muscle layer: under 0.1 ms.
  - Placeholder face render: 3–5 ms.
  - Total compute: about 20 ms per frame, pipelined.
- **Visible phasic latency.** Camera frame (33 ms) + MediaPipe (13) + detection (≤ 67) + burst rise (150) + render and display (33) ≈ 300 ms, inside the 0.3–0.5 s of the human rapid facial reaction.
- **Voice.** WORLD synthesis at about 0.007 real time. The floor-transfer target is 200 ms from the predicted turn end; the prepared opening is released by the fast loop, and Claude's words follow.
- **Memory online.** Python, PyTorch and buffers about 0.6 GB; MiniLM about 0.1 GB; MediaPipe about 0.05 GB; model under 0.01 GB. Total under 1.5 GB.
- **Replay.**
  - A day's features at 3 h are 324k frames × 94 floats ≈ 0.12 GB.
  - Content training on 30-s segments, batch 64, two layers with backpropagation needs ≈ 0.6 GB of activations.
  - Model-based posture evaluation: 10k decision points × 25 options × 300 frames ≈ 1.7·10¹⁴ FLOP, about 1–2 min on the M1 Pro GPU.
  - Peak under 3 GB. Nightly wall time under 30 min.

---

## 7. Novelty test

| Part | What it is | Source (how read) |
|---|---|---|
| staircase of bistable units with slow recurrent feedback; position = number of active units; robust without tuning | Koulakov, Raghavachari, Kepecs & Lisman 2002, robust integrator (read in full for this design) | Nature Neurosci 5:775 |
| modulator decides whether a persistent state exists; content unchanged | Mountoufaris et al. 2024; Liu et al. 2024 (project notes, which quote the full texts; Liu read as PMC full text by the note author, Mountoufaris as preprint) | — |
| τ_n = τ_s/(1 − λ_max); ramp input-driven, decay intrinsic; finite attractor; off-manifold return | Vinograd et al. 2024 (PMC full text: results and methods passages read for this design) | Nature 634:501 |
| position selects behaviour in kind; leading time constant ↔ trait | Nair et al. 2023 (project note) | Cell 186:178 |
| neuromodulator configures which circuit computes; occlusion; reversal at rest | Marder 2012; Bargmann & Marder 2013 (project notes) | — |
| unimodal-at-own-threshold unit, anti-coincidence | Gidon et al. 2020 (project note; the primary abstract could not be re-fetched here) | Science 367:83 |
| coupling inactivating below the receiver's own threshold | Phillips, Larkum et al. 2016 (project note) | — |
| shunting as address, containment | London & Häusser 2005 (project note) | — |
| switching linear dynamical systems with state-dependent switching | rSLDS (via Vinograd's methods, read) | — |
| threshold (level-crossing) event detection, ternary types | standard signal processing and quantised networks (named from memory, not read) | — |
| two-sided drives | Breazeal 2003 (project note) | — |
| perception by inverting one's own generative map | Yoshida & Man; analysis by synthesis (brief) | — |
| closed-loop identification with own variation | Forssell & Ljung 1999 (project note) | — |
| efference comparator | Blakemore, Wolpert & Frith 2002 (project note) | — |
| complementary-learning replay, tags | McClelland 1995; van de Ven 2020; Redondo & Morris (project notes) | — |
| draft selection as exponential tilt | Beirami et al. 2024 (project note) | — |

**Verdict: recombination.** Every part is an existing mechanism. The core object, a staircase integrator whose length is set by a modulator, is Koulakov's robust integrator with its hysteresis or feedback parameter driven by a satiable drive.

**Is "modulator-set existence of persistence" a new computation, or a gated mixture of SSMs?** It is a gated hybrid system. Each (family, mode, plateau) is an affine one-pole system, and transitions are triggered by quantised events or by saddle-node boundaries. That is inside the switching-linear-systems class (a mixture of SSMs with a staircase nonlinearity), with the gate restricted to the agent's own variables. Theorem M, that content is unchanged while persistence changes, is the formal version of Koulakov's remark that "gain and robustness are disentangled". Stating it for this role is new; the computation is not.

**What the design adds, as a constraint set with proofs.** None of the cited systems states or proves the following.
- **(a) An event-only partner interface.** This gives level-blindness (Theorem L), which removes the slow sustained-level dial that the partner-regulator design kept.
- **(b) Innate step magnitudes, with learning restricted to types.** No amplification (T1(3)); no learned ceiling.
- **(c) One active rank-2 circuit per family, with the phasic route on 3 channels.** A rank bound of at most 5 per quantity (11 for the relationship key), from which no-flat-to-copy follows by Eckart–Young.
- **(d) Learning fixed points invariant to the agent's own following.** IV plus efference subtraction (T1b(iv)).

**Against the brief's second clause** (a changed invariant that deletes a free scalar), the candidate is the input scale λ of the common lemma (§4). It is deleted by construction: there is no λ, because responses are innate steps. But deleting a scale by quantising the input is a known technique. **My verdict: this does not clear the second clause.** The design's value, if any, is that it is the first in this project whose dial-freedom is a structural rank-and-type statement holding at every operating point and for every learning outcome. It is not a new computation.

---

## 8. Weak points and falsifiers

### 8.1 Weak points (where a critic should attack)

1. **The relationship key has rank 11.** Changing the partner re-selects the circuit in all four families at once. T1b(iv) says matching circuits are learned only where each family's data support them causally. But a partner who is genuinely good news on every need could, through the data, make all four families' active modes event-matching for that partner. The defect bound on the 12-dimensional perceived space would then be only √(1/12).
2. **Level-blindness may be wrong about people.**
   - Humans may couple to a partner's sustained expression level, not only to onsets. If they do, the design misses a human route; it does not fail the rule.
   - It also cannot reproduce Levitan's turn-level pitch convergence or vocal-quality convergence, both of which need level information.
   - A slow "habit" path for voice quality would need a new event type (for example the partner's turn-average crossing a band), which re-opens the question of a level path.
3. **Zero map at full rest.** A completely rested agent is unmoved by a partner's smile. Humans who are content do return smiles. The design relies on the information drive and the tonic modulators rarely being fully at rest during conversation. That is a claim about dynamics, not a guarantee.
4. **Quantisation and look.** 17 steps × 24 postures may look stepwise; only the muscle low-pass smooths it. Posture changes in kind, at events, may read as abrupt.
5. **Data scarcity.**
   - a (1.3k) and E (9.8k logits) must be learned from a few hours a day.
   - E's gradient comes through a content model trained on the same scarce data, via counterfactual roll-outs. This is the least identifiable part of the design.
   - IV needs minutes per synergy, and babble at 1/60 s⁻¹ per synergy may be too sparse for a strong first stage, or too visible if raised.
6. **(A2) is false in practice.** With a finite model, the regression minimiser does depend on the distribution of regressors, and so weakly on F. T1b(iv) is then approximate; the residual must be measured (the following-invariance test, §8.2 F5(d)).
7. **Relaxed training versus the hard object.** a and ℓ are trained on a relaxed staircase with straight-through types. Near thresholds, the deployed hard object can differ from what was optimised.
8. **Principle 6 residual: provocation.** The information drive's boredom side is relieved by surprise events. Through R̂, the agent can learn which of its own postures make the partner surprising. This is bounded and satiable, but it is a route by which the agent acts on the user to change its own state.
9. **The anti-coincidence evidence is thin.** Gidon et al.'s inverted input–output relation appeared in 4 of 12 cells, and the XOR result is a simulation. P10 is a sharp prediction that may simply be false for faces.
10. **Innate choices with large consequences.**
    - The four families and their afferents (especially "talk-over → aversive load" and "surprise → information").
    - S_φ = {smile, brow↓, brow↑}.
    - The size of 𝔏.
    None is derived from J; all are declared constraints.
11. **Residual same-sign transfer** (Parkinson & Simons 2009) is produced only by co-appraisal (learned E3 steps) and by the 3-channel phasic route. A large appraisal-independent transfer, if real, has no path here.
12. **Claude coupling is narrow:** under 2 bits per reply by selection, plus context choice. Draft collapse would leave only C4 and C5 (llm-coupling-synthesis.md §6).

### 8.2 Falsifiers (state-level tests: steering, lesions, coupling beyond surrogates; no face-matching)

| # | Test | Prediction from the object | What falsifies |
|---|---|---|---|
| F1 | **Steering** (E2): set n_f of one family by ±1 at a fixed operating point | face posture, voice settings, C1 draft ranking and C4 span choice change together, immediately and in kind; the other families unchanged | changes confined to one output channel, or graded rather than stepwise changes |
| F2 | **Existence lesion** (E1): clamp μ_f < μ₁ | Theorem M: the event-type decodability of the first 1 s of the response is unchanged; the engine's fitted line-attractor score log₂(τ₁/τ₂) → 0; carry-over into the next exchange vanishes | immediate responses change (M is false for the build), or persistence survives (the build has another memory path) |
| F3 | **Level-blindness, engine** (exact) | adding in-band level variation to a recorded partner stream leaves u and z bit-identical | any difference means a level path was built (C4 violated) |
| F3h | **Level-blindness, humans** (Seamless Interaction, if Q6 allows) | after regressing out event-locked kernels, the agent's residual coupling to the partner's AU level equals surrogates | not a falsifier of the object; if humans show residual level coupling well beyond surrogates, the design omits a human route (weak point 2) |
| F4 | **Coupling beyond surrogates** (E3), on the agent's *state* | n_f trajectories couple to the partner's event streams beyond segment-shuffle and partner-swap surrogates; coupling vanishes when a := 0 | coupling survives a := 0 (a hidden path), or never exceeds surrogates |
| F5 | **IV acceptance tests** (contingency-causal-synthesis.md §4.9) | (a) autonomous partner → R̂ ≈ 0; (b) replayed partner → collapse; (c) 1-s delay → lag shifts by 1 s; (d) R̂ invariant to the agent's own following gain; (e) hidden driver → ≈ 0; (f) crossed partner → crossed R̂ | any failure falsifies T5 for the build, and with it T1b(iv) |
| F6 | **Interior optimum** (P10), on human dyadic data | probability of a listener's AU12 onset within 1 s of a speaker's AU12 onset is inverted-U in the listener's own pre-onset AU12 level | monotone rising: the coupling does not inactivate; monotone falling only: there is no coupling threshold |
| F7 | **Ramp versus decay** (Vinograd) | in the engine, the rate of stepping depends on the partner's event rate, while hold time depends only on μ: ∂T_hold/∂(partner event rate) = 0 | hold time depends on the partner (a write port into persistence) |
| F8 | **Satiety** (T2) | after all families are satiated and tonic modulators decay, partner events produce H ≡ 0 | any response at full rest |
| F9 | **Replay T2 lesion** (S6, L1) | operator-versus-stranger specificity of the active-mode selection collapses; overall 𝓛_pred barely changes | specificity survives: it lives elsewhere, and E1's S6 claim would need another lesion |
| F10 | **Shape, not size** (P9) | a relationship change gives non-proportional changes across H's expression columns, including a sign change in at least one column; the gain ablation cannot | proportional changes only |

**Not testable on published data.** T1b(iv) and T2(e) are engine-internal; no published dataset contains an agent's own following or satiety. F6 and F3h need recorded human dyads used as published. Seamless Interaction awaits Q6, and REACT/MARS gives listener-only clips without the reciprocal stream needed for F6's pre-onset level.

---

## Sources read for this design

- **Read here in full or in part.**
  - Koulakov et al. 2002, robust integrator: full text, PDF extracted.
  - Vinograd et al. 2024: PMC results and methods passages on saturation, off-manifold return, ramp and decay, the mechanistic model and τ_n.
- **Read through the project's notes**, which quote and report the primaries read by their authors:
  - Marder 2012; Bargmann & Marder 2013; London & Häusser 2005; Gidon et al. 2020; Phillips et al. 2016; Kennedy et al. 2020; Nair et al. 2023; Mountoufaris et al. 2024 (preprint); Liu et al. 2024; Jung et al. 2020; Froemke & Young 2021.
  - bio-computation-synthesis.md, mimicry-context-synthesis.md, social-appraisal-synthesis.md, contingency-causal-synthesis.md, agency-wanting-synthesis.md, memory-replay-synthesis.md, llm-coupling-synthesis.md, voice-synthesis.md, face-development-synthesis.md, emotion-elements-synthesis.md, affective-robots-synthesis.md, foundations/known-failures.md.
  - The critiques of the four earlier designs (dial hunts and fixes).
- **Named from memory, not read:** Goldman et al. 2003 (hysteretic dendrites; search result only); ternary/quantised networks; level-crossing sampling; the Kramers escape formula (standard).
