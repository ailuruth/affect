# Fibred attribution core: contracting where the partner reaches, multistable where only the agent lives

Design author: a design subagent, 2026-11-26. Status: **new, not yet critiqued.**

The file is named for its central object. The working title was "attributed equivariant core". The equivariant part turned out to be one of five ingredients and not the one that resolves the open problem, so the name follows the fibration.

Algebra checks: `research/foundations/sims/design-f/checks.py` (F1–F11). Run it with `python3 -I checks.py`; it needs numpy and scipy, takes about 6 s, and 14 of 14 pass. These are checks of this document's own inequalities on hand-made instances. They are **not** evidence about behaviour, people or data (brief.md, "no toy worlds").

**In five lines.**
- The agent's state is split in two. A **fibre**, which the partner reaches continuously, is a certified contracting operator with innate per-channel ceilings that no parameter value can exceed. A **base**, which holds moods, held feelings, relationship and temperament, is genuinely multistable. The partner can write to it only through a token-budgeted event port, and it shows on the face only through a slew-limited display (§2.4, §2.8).
- Same-feature matching goes through a **router**: attention over (partner coordinate, lag, sign) → own channel, with an innate per-channel cap and an innate **conserved total mass**. No quadratic (IQC-type) ceiling can express this, because a diagonal IQC cannot tell one-channel matching from whole-face matching (Lemma 4) (§2.5).
- The partner's fast band (above 2 Hz) enters every module only through its magnitude. Every agent output is therefore invariant under the sign of that band, for every parameter value (Theorem 2) (§2.3).
- The agent always carries **its own variation**, an innate independent innovation whose amplitude a satiable repetition drive raises. Together with the gain ceilings, this gives an observable copy-defect floor that no route and no learning can remove (Theorem 4) (§2.6).
- **Self and other slots** share one motor coordinate system, and only own-typed signals write the self slot. **Attribution** (an echo kernel identified by the agent's own variation as an instrument) removes the partner's echoes of the agent from base writes (§2.9).

**Main claims, each proved below:**
- **Contraction and persistence coexist (Theorem 1).** They do so only in a fibred form. Lemmas 1–2 show why: a globally contracting system has one attractor, and an unbudgeted partner port into a multistable direction is a held-level switch or a rate dial.
- **D78 holds with every per-channel quantity named and bounded (Theorem 3).** The bound counts all routes: content events, Claude, memory, replay and learning.
  - Single channel: ≤ 0.59 at 30 s.
  - Any 4-channel subspace: ≤ 0.47 in the worst case.
  - The whole Schur face: ≤ 0.27 in the worst case.
- **Copy is never attracting under the design's own learning (Theorem 5).** No assumption of a correct model is needed.

**Novelty verdict: recombination** (§10).

---

## 1. Plain-language intuition

**The pattern to beat.** Every earlier design closed the direct path from your face to the agent's face, and copying came back another way:
- through a loop whose slope nobody bounded;
- through a shared learned estimate;
- through the agent's own interpretation of the conversation;
- through how often you trigger events;
- through expressions you hold.

Each design bounded the routes it had listed. The critics found routes nobody had listed.

**This design makes listing unnecessary in five ways.**

1. **One fence around everything fast.** Everything that responds to you continuously is a single learned network whose maximum slope, per output channel, is compiled into its parameterisation (a "robust recurrent equilibrium network", Revay et al. 2023). Every loop, shared estimate and gate inside it is bounded together. No setting of its weights, learned online, in replay or over years, can exceed those slopes.

2. **Moods live outside the fence, with a slot in the door.** A fence that bounds slopes forbids moods, because a contracting system has only one resting state. So moods, held feelings and the relationship live in a separate "base". Inside the base, the agent has many stable states of its own: a landscape with many valleys.
   - You cannot push the base continuously. You can only knock: discrete events, at most a few at a time and then one a minute.
   - The base shows on the face only slowly: its display can move by at most a fixed amount per second.

   The proof that this is necessary is short:
   - if you could push the base continuously, then either holding an expression long enough tips it (a held-level leak), or repeating a gesture walks it from valley to valley (a rate dial);
   - a budget on knocks is the only innate stop.

3. **Matching is attention with a fixed budget.** The agent can match your smile strongly, or your frown, or answer your frown with its own raised brows. It does so through slots that compete for one fixed amount of "matching mass".
   - Strong matching on one or two channels is possible.
   - Matching on the whole face at once is not: the mass would be spread too thin.

   Which slots win, and with which sign, depends on the agent's needs, role and relationship. This is the brief's need-conditioned attention.

4. **Fast movements count by size, not direction.** For head and face movements faster than about 2 Hz, the agent's whole system receives only how much you moved, never which way. It can then respond to your movement energy, for example by nodding when you pause. It can never copy your fast movements, because nothing downstream can tell "up" from "down". This is what people do: listeners' fast head movements are *less* coherent with the speaker's than chance (Hale et al. 2020).

5. **There is always something of its own.** The agent's face always carries some movement that is its own and independent of you, as a person's does. Because every route from you to its face is capped, this own movement guarantees that its face can never be an accurate copy of yours, however its weights end up. When the agent's way of matching gets repetitive, a satiable drive raises that own variation. The same own variation is also how the agent tells "they respond to me" from "I respond to them" (attribution).

**Reading you through its own body.**
- Your face is mapped into the agent's own motor coordinates: the muscles it would use to make that face.
- Your state is read by inverting the agent's own map from its states to its face.
- Both results are held in an "other" slot. Nothing in the other slot is ever added to the agent's own state; it can only gate or inform the agent's own processes, and only inside the fence.

---

## 2. The precise object

### 2.1 Index sets and innate constants

Time is discrete, t ∈ ℕ, at 30 Hz. A window is [t₀, t₀ + N), with N frames and T_s = N/30 seconds. For a signal x, ‖x‖_T := (Σ_{t∈window} |x_t|²)^{1/2} and RMS_T(x) := ‖x‖_T/√N.

| Symbol | Meaning | Value (innate unless marked learned) |
|---|---|---|
| d | motor coordinates: 9 expressive face synergies, 3 head axes (pitch, yaw, roll), 4 voice (F0 deviation, loudness, rate, tension). Articulation (jaw, lip rounding, bilabial closure) is a separate viseme subspace | 16 |
| β ∈ {s, m, f} | bands of a fixed causal complementary filter bank F_s + F_m + F_f = I, with ‖F_β‖_∞ ≤ 1. s < 0.4 Hz, m 0.4–2 Hz, f > 2 Hz | – |
| k = (j, β) | a channel | n = 48 |
| 𝒮 | Schur channels {(j,s), (j,m)} (same-feature matching allowed, capped) | 32 |
| 𝒯 | twisted channels {(j,f)} (sign-blind) | 16 |
| U_max | saturation of normalised partner deviations | 2 |
| τ_p | partner baseline / scale EMA | 60 s |
| W_k | router row cap: smile axis and brow axis mid band 0.30; their slow band 0.25; all other 𝒮 channels 0.20 | – |
| τ | router total matching mass | 0.6 |
| ℓ_{1,k}, ℓ_{2,k} | router taps; innate per-coordinate dispersion: ℓ₁ ∈ [0.35, 0.65] s, ℓ₂ ∈ [1.5, 2.5] s | – |
| τ_ω | low-pass on routing logits ("context lags by seconds") | 2 s |
| c_k | REN output ceilings: 0.15 on 𝒮, 1.0 on 𝒯 | – |
| c_ω | Lipschitz of the partner-driven routing logits (key path) | 0.2 |
| m_g | partner-typed REN inputs: u^𝒮 (32), levels ℓ (16), envelopes ε (16), content pulses e (16) | 80 |
| W₂ | REN input weight: I/√m_g on partner-typed inputs; κ_b = 0.5 on b̃, κ_ζ = 0.25 on ζ̃, 1 on κ_rel and clock | – |
| ᾱ | REN contraction rate bound (per frame) | 0.99 (memory ≤ 3.3 s) |
| n_b, C | base dimension; maximum number of base centres | 24, 64 |
| d_min, β_b, h_max, t_max | centre separation, well sharpness, bias bound, tilt bound | 0.5, 200, 0.5, 0.05 |
| ε_b, σ_b | base relaxation rate; base noise | 0.2 s⁻¹, 0.09 |
| v_b | slew of the displayed base b̃ (norm per second) | 1/600 s⁻¹ |
| A_k | display amplitude / Lipschitz of H on channel k | 0.25 |
| buckets | partner-event (capacity 2, refill 1/60 s), content-event (2, 1/60 s), body-event (1, 1/120 s) | – |
| j_max | event jump norm | 0.6 |
| θ_ev | event threshold, re-arm at θ_ev/2, high-pass 10 s, refractory 2 s | 1.0 |
| n_ζ, v_ζ | body variables; their slew | 5, 1/600 s⁻¹ per coordinate |
| O_k | cap on the role (speaking/listening) pattern difference on face channels | 0.08 |
| L_own | Lipschitz of N_own in (b̃, ζ̃) per channel | 0.05 |
| σ₀ | own-variation floor (band 0.05–1 Hz, on 𝒮 channels) | 0.15 |
| γ, a*, T_R, Ψ* | matching-slot habituation gain, threshold, time constant; repetition set point | 4, 0.15, 120 s, 0.3 |

**Units.**
- Partner channels are normalised by the partner's running scale σ̄ (the typical deviation is ≈ 1).
- Agent channels are normalised by the agent's innate per-channel expressive scale (its typical expression has RMS 1).
- "Gain 1" therefore means "moves as much, relative to its own range, as the partner moves relative to theirs".

### 2.2 Spaces, slots and typing rules

**Variables.**

| Variable | Domain | Slot | Type |
|---|---|---|---|
| o_t | MediaPipe blendshapes (52) + head pose (3); partner prosody (F0, loudness, rate, tension) after acoustic echo cancellation | other | percept |
| p_t = P_φ(o_t) | [−1, 1]^16, partner in the agent's own motor coordinates | other | partner-typed |
| g_t = Γ(p)_t | ℝ^64, the gate output (§2.3), plus content pulses e_t ∈ [0,1]^16 | other | partner-typed |
| x_t | ℝ^96, fibre (REN) state | – | mixed |
| ω_t | router weights, ℝ^{2048} | self | mixed |
| b_t, b̃_t | ℝ^24, ‖b‖ ≤ 1; base and displayed base | self | own-typed (partner-written only through events) |
| ζ_t, ζ̃_t | [0,1]^5, body variables and their slew-limited copy | self | own-typed |
| A_t, Ψ_t | slot habituation ∈ [0,1]^{2048}, repetition load Ψ = ‖A‖² | self | own-typed |
| d_t | ℝ^32, own variation (innate stochastic process) | self | own randomness |
| a_t | [0,1], attribution of the latest partner change to the agent's own output | – | used only as a base-write weight and in replay |
| ŝ_t | ℝ^{29}, the partner's inferred state in the agent's own state coordinates (b̃, ζ̃) | other | partner-typed |
| r_t | {listen, speak, overlap}, the floor state | self | own decision; depends on the partner through turn timing |
| κ_rel | ℝ^8, the relationship key, computed in the first 5 s of a session and frozen | – | constant in a session |
| y_t | ℝ^48, the agent's output by channel; m_t = Σ_β y_{(·,β)}, the motor command | self | output |

**Typing rules.** These are structural constraints of the code graph, not tuned constants.
- **A1, the gate.** Every consumer of the partner's face and prosody features receives them only through Γ. This includes the fibre, router, attribution, world model 𝓜, replay store and Claude selection. No module, stored record or learning signal sees the raw fast band c^f.
  - Two partner streams are deliberately outside Γ:
    - the **words** (on-device ASR on the raw audio);
    - the **relationship key** κ_rel (a face-identity embedding computed in the first 5 s and then frozen).
  - Theorem 2 conditions on both.
- **A2, no other-to-self addition.** No map adds an other-slot variable (p, g, ŝ) into a self-slot variable (b, ζ, A, d, m), with two exceptions: the router (§2.5) and the fibre 𝓡 (§2.4). Both are certified. Action never descends an error on the other slot.
- **A3, one fence.** Every continuous map from partner-typed variables to the output passes through 𝓡_θ or the router. 𝓡 is a single robust REN, and router weights are bounded by construction for every logit value.
- **A4, discrete port.** Partner-typed variables reach b only as event jumps that pass a token bucket. Body variables reach b only as a tilt bounded by t_max, plus body events through their own bucket.
- **A5, slow display.** b and ζ reach the output and 𝓡 only through b̃ and ζ̃. Their slews are bounded by v_b and v_ζ.
- **A6, own variation.** d is generated by the agent's own random source. It is added after every other output term and is not an input to any module except the IV estimator (§2.9) and the logs.
- **A7, no partner target.** No loss whose gradient reaches an action-producing parameter has a partner-typed quantity as its target or reward. The action-producing parameters are the router, the REN face head, H, N_own, the event jumps J, the landscape ψ and the draft scorer. Partner-typed quantities may appear only as regressors or as context.
- **A8, parameters change only in replay.** During a session, only states change (baselines, A, buckets, IV spectra, attribution evidence). Weights change only in nightly replay, and every replay update stays inside the parameterisations below.

### 2.3 Perception through the agent's own body, and the gate Γ

- **P_φ** is a small network learned only from the agent's own **babbling**. The agent moves its own face through its renderer R (and later its muscle model, brief S4), observes the result through the same feature extractor, and fits P_φ(feat(R(m))) ≈ m. The partner is then perceived as the agent's own motor command that would look most like them.
- **The gate.** Let c^f := F_f p (the fast components) and r := p − c^f. Then:
  - p̄ = EMA_{60s}(r) and σ̄_j = max(σ₀^p, EMA_{60s}|r_j − p̄_j|);
  - **u^𝒮** ∈ ℝ^32: u_{(j,β)} = U_max tanh(F_β(r_j − p̄_j)/(σ̄_j U_max)) for β ∈ {s, m};
  - **ℓ** = LP_{0.4 Hz}(r) ∈ [−1, 1]^16, the levels in own coordinates, with a fixed scale;
  - **ε** ∈ ℝ^16: ε_j = LP_{1 Hz}(|c^f_j|)/σ₀^p, the fast-band envelopes.

  So Γ(p) = (u^𝒮, ℓ, ε). Content pulses e (§5.5) are appended to make the 80 partner-typed REN inputs.
- **The group.** G = {±1}^16 acts on percept histories by c^f_j ↦ σ_j c^f_j, with r unchanged. Since only |c^f| enters Γ, **Γ(σ·p) = Γ(p) exactly.** On 𝒯 the agent's output channels transform trivially while the partner's same channels flip: a sign twist, χ(σ_j) = σ_j. On 𝒮, G acts trivially on both sides, which is Schur's case: an identity intertwiner is allowed there, and copying is excluded only by caps and the floor of Theorem 4.

### 2.4 The fibre 𝓡_θ: one robust REN for every fast partner-dependent computation

𝓡_θ is an acyclic robust REN (Revay, Wang & Manchester 2023, eqs. 6–8, with the direct parameterisation of §V). Its sizes are n = 96 states and q = 192 neurons, with σ = ReLU (slope-restricted in [0, 1]).

**Input** v_t ∈ ℝ^{121}: the 80 partner-typed coordinates (u^𝒮, ℓ, ε, e), and own-typed b̃ (24), ζ̃ (5), κ_rel (8) and clock phase (2). Role and own text are deliberately **not** inputs.

**Outputs** z_t ∈ ℝ^{216}:
- y^F ∈ ℝ^48, the face/voice drive;
- κ ∈ ℝ^{16×8}, the per-partner-coordinate attention keys;
- π^ev ∈ ℝ^16, the event proposals;
- ŝ ∈ ℝ^{29} (whose weight is shared with y^F in the budget below).

**Certificate.** The incremental IQC (Q, S, R) = (−W₁ᵀW₁, 0, W₂ᵀW₂) holds, with W₁ = diag(1/c_k on y^F; 1/c_κ on keys; 1/c_ev; 1/c_s) and W₂ from §2.1. By Revay Theorem 3, **every** free vector θ ∈ ℝ^N gives a well-posed REN that is contracting with rate < ᾱ and satisfies, for all input pairs v, v′ and equal initial state:

  Σ_i c_i⁻²‖z_i − z′_i‖²_T ≤ ‖W₂(v − v′)‖²_T for every T.  (R)

The constants (c_i, W₂) are compiled into the map (Revay eqs. 29–33). They are not in θ.

**The other slot inside the fence.** The own decoder D (§2.12) is one feedforward sub-block of the equilibrium layer, a special case of the REN (Revay §III-A). So the partner's inferred state ŝ = D(ℓ) is computed inside the certificate.

### 2.5 The router: attention with a conserved matching mass

**Slots.** A slot is i = (k, j, a, σ):
- k ∈ 𝒮, the own channel;
- j ∈ 𝒮 in the same band as k, the partner coordinate (16 per band);
- a ∈ {1, 2}, the tap;
- σ ∈ {+, −}, the sign.

That gives 2 bands × 16 × 16 × 2 × 2 = 2048 slots, plus a null slot.

**Logits.** z_i = clip(z^own_i + z^key_i, −L, L) − γ(A_i − a*)₊, where:
- z^own_{(k,a,σ)·j} = ⟨q_{kaσ}(b̃, ζ̃, κ_rel, r), E_j⟩/√8. The query comes from an own-typed network N_q with ‖q‖ ≤ q_max; the E_j are learned coordinate embeddings.
- z^key_i = LP_{τ_ω}⟨q_{kaσ}, κ_j⟩/√8, with κ_j the REN keys. Its Lipschitz constant in the partner-typed input is ≤ c_ω/√m_g in the sense of (R).
- The null logit b₀ is innate, and L = 10.
- The innate reflex (declared): the slots (smile-mid, smile-mid, 1, +) and (brow-mid, brow-mid, 1, +) have prior logit bias +3. Learning can move it.

**Allocation and weights.**

  μ = softmax(z, b₀) ∈ Δ^{2048},  ω_{kja} = clip_{[−W_k, W_k]}(τ(μ_{kja+} − μ_{kja−})).

In addition, row caps are enforced: if Σ_{j,a}|ω_{kja}| > W_k, the row is scaled to W_k (a 1-Lipschitz radial projection).

**Output.**

  y^R_k(t) = Σ_{j,a} ω_{kja}(t) u_j(t − ℓ_{a,k}).

**Habituation.** A_i(t+1) = A_i(t) + (μ_i(t) − A_i(t))/(30 T_R).

### 2.6 Own variation and the repetition drive

**Own variation.** d_t = σ_d(t) ξ_t, where ξ is a unit-variance band-limited (0.05–1 Hz) aperiodic process from the agent's own random source, independent of everything else (A6). Its amplitude is

  σ_d(t) = σ₀(1 + min(1, D_R(t)/D_R^max)),  D_R := (Ψ − Ψ*)₊,  Ψ := ‖A‖².

So σ₀ ≤ σ_d ≤ 2σ₀.

**Repetition drive.** D_R is the satiable repetition drive.
- It is zero when the recent allocation is spread out or varied.
- It grows when the same slots have held mass for minutes.

It acts in two ways: as more own variation, and as habituation of those slots (the −γ(A − a*)₊ term). Its argument is the agent's own allocation history. It never contains the partner's percept.

### 2.7 Body and drive

**Body variables** ζ = (energy, motor-effort load, information deficit, sleep pressure, voice effort). All are innate, none emotional (Principle 2).

  ζ̇ = −λ_ζ(ζ − ζ*) + E(m^pre, speech) + innate circadian terms.

- m^pre is the motor command before d is added.
- λ_ζ = 1/(10 min).
- The information deficit falls with the agent's own prediction error on content and own body. The partner's face is deliberately excluded.

ζ̃ follows ζ with slew ≤ v_ζ per coordinate.

**The drive** is

  𝒟(ζ, Ψ) = Σ_i w_i(|ζ_i − ζ*_i| − ε_i)₊² + w_R(Ψ − Ψ*)₊.

### 2.8 The base: persistent multistable state, budgeted event port, slow display

**Landscape.**

  V_ψ(b) = −(1/β_b) log Σ_{c=1}^{C} exp(−β_b‖b − μ_c‖²/2 + h_c(κ_rel)) − ⟨t_ψ(ζ̃), b⟩.

Its learned parts are constrained:
- the centres μ_c have ‖μ_c‖ ≤ 1 and pairwise separation ≥ d_min (enforced in replay by projection and merging);
- |h_c| ≤ h_max (tanh);
- ‖t_ψ‖ ≤ t_max (tanh).

**Dynamics between events.**

  db = −ε_b ∇V_ψ(b) dt + σ_b dW.

**Events.** There are three sources:
- partner events: π^ev from 𝓡, then a 10-s high-pass, threshold θ_ev with re-arm hysteresis and a 2-s refractory period, weight (1 − a_t), then bucket B_p;
- content events: from content heads on transcript spans (§5.5), then bucket B_c;
- body events: innate threshold crossings of ζ, then bucket B_ζ.

An event of type e with weight w ∈ [0, 1] jumps b ← b + w J_ψ(e, κ_rel), with ‖J‖ ≤ j_max.

**Display.**

  b̃_{t+1} = b̃_t + sat_{v_b/30}(ε_d(b_t − b̃_t)),

where sat clips the step's norm. The display output is

  y^B_k = H_{ψ,k}(b̃), H_k = A_k tanh(h_k(b̃)), h_k 1-Lipschitz.

So |ΔH_k| ≤ A_k‖Δb̃‖.

### 2.9 Attribution: an echo kernel identified by the agent's own variation

**Echo kernel.**
- Online Welch cross-spectra of the own variation d with the gate u^𝒮 and with the output y are kept for 0.05–2 Hz over a 10-min window.
- Ĝ(f) = S_{ud}(f)S_{yd}(f)⁻¹ is the partner's echo kernel: how the partner's face responds to the agent's output (Lemma 8).
- A first-stage strength check is applied. If the F-statistic is below 10, Ĝ is set to 0 and a ≡ 0.

**Attribution evidence** (Lanillos et al. 2020, eqs. 11–14, with Ĝ as the own forward model of the partner's echo):

  λ_t = λ_{t−1}(1 − 1/30T_λ) + log 𝒩(Δu_t; (Ĝ*y)_t, Σ_e) − log 𝒩(Δu_t; 0, Σ_p),  a_t = sigmoid(λ_t),

with T_λ = 3 s. a_t is used only as the base-write weight (1 − a_t) on partner events (§2.8) and as a replay sample weight (§5.7).

### 2.10 Own intention, floor and articulation

**N_own**, the own-intention network. Its inputs are b̃, ζ̃, r, the clock and own-speech prosody features. It outputs:
- the set-point face;
- slow gaze and head rhythms;
- the voice channels during the agent's own speech (F0 contour, loudness and rate from the text of its own utterance and its own state).

It is Lipschitz ≤ L_own per channel in (b̃, ζ̃). The role enters only through an additive, capped per-channel term with |N_k(·, r) − N_k(·, r′)| ≤ O_k on face channels.

**The floor r** is the agent's own decision: a turn-end predictor in 𝓜 plus an innate floor rule (speak only if partner voice activity has been off for ≥ 0.2 s; overlap ≤ 0.2 s).

**Articulation** (visemes) comes from the agent's own phonemes through an innate map. It is not part of the 16 expressive coordinates.

### 2.11 Output assembly

  y_k = y^R_k + y^F_k + y^B_k + N_{own,k} + d_k  (k ∈ 𝒮),  y_k = y^F_k + N_{own,k}  (k ∈ 𝒯).

The motor command m_j = Σ_β F_β y_{(j,β)}, plus visemes, goes to an innate synergy-to-blendshape map and then to the placeholder face (Principle 8). The voice coordinates set per-word pitch, pitch range, rate and volume of macOS speech synthesis for the agent's own speech. While listening they drive backchannel vocalisations only.

### 2.12 The world model 𝓜 and the other slot

- **𝓜** is an ordinary predictive model: two diagonal-SSM (LRU-type) layers, H = 128. It predicts:
  - the next gate g (other slot);
  - own body ζ;
  - turn end;
  - own drive change.

  It sees only Γ-outputs (A1). Its outputs go only to:
  - the floor decision;
  - Claude draft selection keys and retrieval keys;
  - attribution covariances;
  - replay.

  They are never inputs to 𝓡, the router or the output (A3).
- **D**, the own decoder, lives inside 𝓡. It is trained on the agent's own (H(b̃), N_own(b̃, ζ̃)) → (b̃, ζ̃) pairs. The partner reading ŝ = D(ℓ) is in the other slot: it is never written into b or ζ (A2), and it influences the agent only through 𝓡 (certified) and through selection.

### 2.13 The one core: objective and constraints (Principle 10)

**The core** is the typed hybrid system Σ = (Γ, 𝓡_θ, router, base, body, d) above. It has one drive potential 𝒟 and one predictive constraint:

  minimise 𝔼 Σ_t γ_d^t 𝒟(ζ_t, Ψ_t) over the action parameters (router heads, REN face head, J_ψ, ψ, H, N_own, draft scorer),
  subject to A1–A8 and to 𝓛_pred (𝓜 and the REN prediction heads are the agent's best predictors of its own streams).

**What the core produces.**
- The **router**: the shared-fate target of §5.6 is the predictive constraint applied to "what does the partner's j predict about my own display on k".
- **Satiable drives**: 𝒟.
- **Persistence**: the base.
- **Reading the other**: D inside 𝓡.
- **Curiosity**: the information-deficit term of 𝒟.
- **Valence and arousal** as readouts (§5.2).
- **Replay**: as optimisation of the same objective offline (§5.7).

What is added as an explicit constraint rather than derived is listed as A1–A8 and the innate constants. **Honest note:** this is "one objective plus a predictive constraint plus typing rules", the same shape as the earlier designs. It is not a single variational functional.

---

## 3. Theorems and proofs

### 3.0 Definitions used throughout

- **Neutral counterfactual.** Fix the full state at t₀, the own randomness (ξ, base noise), the partner's words and every Claude output.
  - g⁰ is the partner history in which, from t₀ on, the partner's face and voice sit at their baseline: u^𝒮 = 0, ε = 0, ℓ = ℓ(t₀), and partner voice activity is unchanged.
  - Content pulses are recomputed from whatever Claude outputs result, so they differ between g and g⁰ when selection differs.
  - Write Δy := y(g) − y(g⁰). This is an exact difference, not a linearisation.
- **Per-channel least-squares gain at lag ℓ:** c^{LS}_k := ⟨Δy_k, S_ℓu_k⟩_T/‖S_ℓu_k‖²_T. **Pooled over a set K:** c^{LS}_K := ⟨Δy_K, S_ℓu_K⟩/‖S_ℓu_K‖².
- **Observable copy defect** of channel set K at lag ℓ: δ_K := inf_{c≠0}‖y_K − c S_ℓu_K‖/‖c S_ℓu_K‖.
  - This is the critiques' scale-free defect (design-modulated-manifolds §3.0), but on the *observed* output, not the counterfactual difference.
  - **Identity:** δ_K = (1 − ρ_K²)^{1/2}, with ρ_K the uncentred correlation ⟨y_K, S_ℓu_K⟩/(‖y_K‖‖S_ℓu_K‖).
  - *Proof.* Put x = 1/c. Then ‖y − cu‖²/‖cu‖² = (x²‖y‖² − 2x⟨y,u⟩ + ‖u‖²)/‖u‖², minimised at x = ⟨y,u⟩/‖y‖². □
- **Partner amplitudes.** a_k := RMS_T(u_k).
  - M_k(t) := max_{j,a}|u_j(t − ℓ_{a,k})| and M̄_k := RMS_T(M_k).
  - ā_g := ‖Δg‖_T/√(m_g N) is the coordinate-averaged RMS change of the partner-typed REN input (including content pulses).
  - χ_k := max(M̄_k, ā_g)/a_k ≥ 1 is the **dominance ratio**: χ_k ≈ 1 when channel k is the partner's most active coordinate.
- **Admissible parameters Θ:** every value of every learned object that the parameterisations of §2 can produce: θ ∈ ℝ^N; any router heads; ψ satisfying the constraints of §2.8; any H, N_own, J, 𝓜, P_φ, content heads; any draft scorer. Every learning rule, online or replay, stays in Θ by construction (A8).

### 3.1 Lemma 1 (contraction forbids multistability)

*Statement.* Suppose a system x_{t+1} = f(x_t, v) is contracting in the sense of Revay Definition 2, |x^a_t − x^b_t| ≤ Kα^t|a − b|, for a constant input v. Then it has at most one equilibrium, and every trajectory converges to it.

*Proof.*
- If x* ≠ x** were both equilibria, the trajectories from them would stay at distance |x* − x**| > 0 forever, contradicting Kα^t|x* − x**| → 0.
- Existence: f(·, v) is a contraction in the metric of the certificate, so the Banach fixed-point theorem applies. □

*Consequence.* A design whose entire partner→face map is a contracting operator (the whole-loop synthesis proposal) has one affective state per input history. It has no moods, no held feelings and no hysteresis. Persistence must live in a part that is not contracting.

### 3.2 Lemma 2 (no free persistence: a partner port into a multistable direction is a held-level switch or a rate dial)

*Setting.* A scalar base ḃ = −V′(b) + k s(t). V is C¹ with wells m_1 < … < m_n and barrier tops M_i ∈ (m_i, m_{i+1}). Define F_i^+ := max_{[m_i, M_i]}V′ > 0. The partner signal s is admissible with |s| ≤ S.

**(a) Gain port.**
- If kS > F_i^+, the held level s ≡ S takes b from m_i past M_i in finite time.
- If kS < F_i^+, no admissible s ever takes b from below b*_i past M_i, where b*_i is the first point in (m_i, M_i] with V′(b*_i) = kS. When s returns to 0, b returns to m_i.

*Proof.*
- First case: on [m_i, M_i], ḃ ≥ kS − F_i^+ > 0.
- Second case: at b = b*_i, ḃ ≤ −V′(b*_i) + kS = 0, so the point b*_i cannot be crossed upward. With s = 0, the gradient flow on [m_{i−1}, M_i) converges to m_i. □

**(b) Derivative port, s = φ̇ with |φ| ≤ Φ.**
- Take the staircase case with equal wells: V(b + D) = V(b) on the relevant range, and m_i − M_{i−1} = h_D.
- Suppose h_D < 2kΦ < D + h_D (one fall crosses exactly one barrier), and there is a rise time T_r with 2kΦ/T_r < min_i F_i^+.
- Then a periodic sawtooth (slow rise over T_r, fast fall in time δ → 0, then rest) moves b down one well per period. After P periods the base has switched P times.

*Proof.*
- During the slow rise, (a) applies with S = 2Φ/T_r: b stays below b*_i and then relaxes to m_i.
- The fast fall gives b(t + δ) − b(t) = −2kΦ + O(δ max|V′|). As δ → 0 this is a jump of −2kΦ ∈ (−D − h_D, −h_D), so b lands in (M_{i−2}, M_{i−1}) and relaxes to m_{i−1}.
- By translation invariance the same holds in well i − 1. Induct. □

Check: F5, 3 wells in 3 cycles with |φ| ≤ 0.35D.

**(c) The budget is the only innate stop.**
- In both port types, any admissible single switch can be repeated by repeating the partner waveform (case b), or by holding it (case a).
- The number of partner-caused switches in a window is then controlled by the partner: by a held level, or by a repetition rate.
- A token bucket of capacity B and refill ρ bounds the number of partner-caused write events by B + ρT, for every port and every partner. This holds by construction: each write consumes one token. □

*What the lemma says.* "Contraction in the partner-driven directions, persistence in the own directions, and a budgeted discrete port between them" is not one choice among many. It is the shape forced by Lemma 1 together with (a)–(c), given the requirement that persistence be partner-influenceable at all (relationships and moods do respond to people). Lemma 2 is the formal version of the critiques' "event rate is a dial" (manifolds critique C3) and "held levels leak" (C2).

### 3.3 Lemma 3 (the base landscape keeps C persistent states for every admissible parameter and tilt)

*Statement.* Let:
- r ∈ (0, d_min/2);
- η := exp(−β_b d_min(d_min − 2r)/2 + 2h_max);
- e_max := 2(C − 1)η.

Suppose 4β_b(C − 1)η < 1 and r > t_max + e_max. Then for every admissible ψ (§2.8) and every tilt ‖t‖ ≤ t_max:
- each ball B(μ_c, r) is forward-invariant under ḃ = −∇V_ψ(b);
- V_ψ is strictly convex on the ball, with unique minimiser b*_c;
- b*_c is exponentially stable with rate ≥ ε_b(1 − 4β_b(C − 1)η).

*Proof.*
- Write p_{c′}(b) ∝ exp(−β_b‖b − μ_{c′}‖²/2 + h_{c′}). Then ∇V = Σ_{c′}p_{c′}(b − μ_{c′}) − t.
- For b ∈ B(μ_c, r) and c′ ≠ c: ‖b − μ_{c′}‖ ≥ d_min − r, so p_{c′}/p_c ≤ exp(−β_b((d_min − r)² − r²)/2 + 2h_max) = η.
- Hence ∇V = (b − μ_c) − t + e(b), with e(b) = Σ_{c′≠c}p_{c′}(μ_c − μ_{c′}) and ‖e‖ ≤ (C − 1)η · 2 = e_max (since ‖μ‖ ≤ 1).
- On the sphere ‖b − μ_c‖ = r: ⟨∇V, b − μ_c⟩ ≥ r² − r(t_max + e_max) > 0. So the flow −∇V points inward, and the ball is forward-invariant.
- The Hessian is ∇²V = I − β_b Cov_p(b − μ_·), and Cov_p ⪯ Σ_{c′≠c}p_{c′}·4I ⪯ 4(C − 1)η I. So ∇²V ⪰ (1 − 4β_b(C − 1)η)I ≻ 0 on the ball.
- Strict convexity gives a unique minimiser and the stated exponential rate. □

*Numbers.* With β_b = 200, d_min = 0.5, r = 0.1, h_max = 0.5, C = 64:
- η = e^{−14} = 8.3·10⁻⁷;
- e_max = 1.0·10⁻⁴;
- 4β_b(C − 1)η = 0.042.

So all 64 states persist for every tilt ≤ 0.05. Check F8: the largest distance of an equilibrium from its centre was 0.050 < 0.1.

*Noise.*
- With σ_b > 0, persistence is metastable. The barrier between neighbouring wells is ≈ (d_min/2)²/2 = 0.031, so exp(2ΔV/σ_b²) = e^{7.7} ≈ 2200. The Kramers prefactor depends on the curvature at the barrier, which is sharp here (≈ −11.5). That gives a mean escape time of ≈ 6 h; taking the prefactor as 2π/ε_b gives ≈ 19 h.
- This is a standard estimate. **It is not proved here, and the Kramers/Freidlin–Wentzell sources were not read.** Only the deterministic persistence above is claimed as proved.
- The base state is saved across restarts.

### 3.4 Theorem 1 (fibred persistence: contracting where the partner reaches, multistable where only the agent lives)

*Statement.* For every parameter value in Θ:
- **(a) Fibre.** For any fixed path of the own-typed inputs (b̃, ζ̃, κ_rel, clock) and any partner-typed path, 𝓡_θ is contracting with rate < ᾱ and satisfies (R).
  - Two runs that differ only in their initial fibre state converge: |Δx_t| ≤ Kᾱ^t|Δx₀|.
  - The partner's influence through every continuous route therefore decays with time constant ≤ 1/(30(1 − ᾱ)) = 3.3 s once the partner input difference stops.
- **(b) Base.** Without events and noise, b has ≥ C stable equilibria (one per centre, Lemma 3), each with a forward-invariant ball. This holds for every admissible tilt path, so in particular for every body path and every partner path.
- **(c) Port.** The only partner-dependent terms that can move b out of a ball are event jumps. The number of partner-caused events in any window is ≤ Σ_src(B_src + ρ_src T_s), which is ≤ 5 + T_s/24 s.
- **(d) Display.** The base reaches the output and the fibre only through b̃, with ‖b̃(t) − b̃(t′)‖ ≤ v_b|t − t′|.

*Proof.*
- (a) is Revay Theorem 3 applied to 𝓡_θ, whose inputs include the own-typed ones. The contraction definition (Revay Def. 2) is for a common input sequence, so any fixed path qualifies.
- (b) is Lemma 3.
- (c): by A4, ḃ depends on partner-typed variables only through:
  - the tilt t_ψ(ζ̃), with ζ partner-influenced through m^pre; the tilt is bounded by t_max, so it cannot leave a ball (Lemma 3);
  - event jumps.

  Each event consumes a token. The bound follows from the bucket constants.
- (d) holds by construction of the slew. □

*Why this resolves the open problem.*
- The partner→face map is not globally contracting (Lemma 1 forbids that together with moods).
- It is contracting **in the fibre**, uniformly over the base. The base is multistable and its multistability is untouched by any partner input except through a counted, rate-limited port.
- The face sees the base only through a slew limit.
- This is a skew-product (cascade) structure, with contraction in the fibre directions and a hybrid, budgeted coupling from fibre to base. Lemma 2 shows that the budget, or an equivalent innate cap on the partner's switching rate, is necessary.

### 3.5 Lemma 4 (a diagonal IQC cannot separate one-channel matching from whole-face matching) and Lemma 5 (joint budget)

**Lemma 4.**
- *Statement.* Let Q = diag(q_k) ⪯ 0, S = diag(s_k), R = diag(r_k). A static diagonal transfer T = diag(t) satisfies the quadratic constraint [T; I]ᵀ[[Q, S],[S, R]][T; I] ⪰ 0 iff q_k t_k² + 2s_k t_k + r_k ≥ 0 for every k.
- In particular, g·I is admissible iff g·e_ke_kᵀ is admissible for every k.
- *Proof.* The matrix is diag(q_k t_k² + 2s_k t_k + r_k). □ (F1: 0 of 2000 mismatches.)
- *Meaning.* The REN's per-channel ceilings form a box. A box cannot express "strong matching on one or two channels, never on the whole face". That needs an ℓ₁-type (non-quadratic) constraint, which is what the router's mass τ is.

**Lemma 5 (joint budget).**
- *Statement.* Under (R) with W₂ = I/√m_g on the partner block, suppose the partner-typed input changes by Δg and the own-typed inputs are equal. Then Σ_k c_k⁻²‖Δy^F_k‖² ≤ ‖Δg‖²/m_g.
- For a gate moving coherently (every coordinate by a), a uniform response g·a on K output channels with equal c needs g ≤ c/√K.
- The bound is attained by T = g 1_K 1ᵀ/m_g.
- *Proof.* Substitute into (R): K g² a² N/c² ≤ m_g a² N/m_g. □ (F2.)

### 3.6 Lemma 6 (router bounds, for every logit value)

*Statement.* For every logit path (whatever z^own, z^key or A do):
1. **Mass.** Σ_{k,j,a}|ω_{kja}(t)| ≤ τ(1 − μ_null) ≤ τ.
2. **Row caps.** Σ_{j,a}|ω_{kja}(t)| ≤ W_k.
3. **Pointwise.** |y^R_k(t)| ≤ W_k M_k(t), and Σ_{k∈K}|y^R_k(t)| ≤ τ max_{k∈K}M_k(t).
4. **Incremental.** For two partner histories u, u′:

   |Δy^R_k(t)| ≤ W_k max_{j,a}|Δu_j(t − ℓ_{a,k})| + U_max Σ_{j,a}|Δω_{kja}(t)|,

   with Σ_{k,j,a}|Δω_{kja}(t)| ≤ τ‖Δμ(t)‖₁ ≤ τ osc(Δz(t)) ≤ 2τ‖Δz(t)‖_∞. Here osc is the max minus the min.

   For the whole output vector, the Schur test (row ℓ₁ sums ≤ W_max, column ℓ₁ sums ≤ τ, lag operators of norm 1) gives

   ‖Δy^R‖_T ≤ (W_max τ)^{1/2}‖Δu‖_T + 2U_max τ ‖ ‖Δz(·)‖_∞ ‖_T.
5. **Windowed bound.** Over windows with T_s < 2T_R/γ:

   ‖Δz‖_T ≤ (‖Δz^own‖_T + ‖Δz^key‖_T)/(1 − γT_s/(2T_R)).

*Proof.*
- (1): |ω_{kja}| ≤ τ(μ_{kja+} + μ_{kja−}), then sum. Clipping and the row projection only shrink.
- (2) holds by the row projection.
- (3): |y^R_k| ≤ Σ_{j,a}|ω_{kja}||u_j(t − ℓ_{a,k})| ≤ (Σ|ω_{k··}|)M_k. Summing over k and using (1) gives the second inequality.
- (4):
  - The softmax Jacobian J = diag(μ) − μμᵀ satisfies xᵀJx = Var_μ(x). By Popoviciu, Var_μ(x) ≤ (max x − min x)²/4.
  - Hence its ℓ₂ norm is ≤ ½ (for ‖x‖ = 1, max − min ≤ √2). F3b: max eigenvalue 0.4996.
  - Its ℓ∞→ℓ₁ form: Σ_i μ_i|dz_i − μᵀdz| ≤ osc(dz).
  - The clip and the projection are 1-Lipschitz.
- (5):
  - A is a first-order filter of μ with unit DC gain. Over a window starting from equal A, |ΔA(t)| ≤ (t/30T_R)·max_{s<t}|Δμ(s)|.
  - Hence ‖ΔA‖_T ≤ (T_s/T_R)‖Δμ‖_T ≤ (T_s/2T_R)‖Δz‖_T, using ½-Lipschitz softmax in ℓ₂.
  - (·)₊ is 1-Lipschitz. Solve the resulting inequality. □

Checks: F3, F3c. These check the diagonal special case (128 slots); the proofs do not depend on the number of slots. Under saturation the mass is 0.30, the per-channel uniform weight is τ/32, and the pointwise and incremental bounds hold.

### 3.7 Theorem 2 (twisted channels: sign-blindness for every parameter and every route, and what it implies)

*Statement.* Under A1, for every parameter value in Θ, every replay history, every own-randomness realisation and every behaviour of Claude, the conditional law of the agent's entire trajectory, given the percept history π, the partner's words and κ_rel, is G-invariant:

  Law(Y | σ·π, words, κ_rel) = Law(Y | π, words, κ_rel) for all σ ∈ G.

Here Y means the outputs y, base b, words, parameters and stored records.

*Proof.* By induction over frames and over nights.
- At each frame every module's input is a function of:
  - Γ-outputs, which are G-invariant because Γ(σ·p) = Γ(p);
  - own randomness, which is independent of the percept;
  - Claude's sampled text, whose conditional law depends only on its context;
  - the words and κ_rel, which are held fixed.

  Claude's context is built from transcripts, verbatim retrievals and draft selections, and all of these are functions of Γ-outputs, words and own randomness.
- Replay updates are functions of the stored records. Those are Γ-outputs, own outputs and transcripts; c^f is never stored (A1).
- So the parameters after each night are G-invariant functions of the percept history, and the induction carries on. □

**Corollary 2a (zero linear coupling).**
- Fix a twisted channel k = (j, f) and a lag ℓ. Let 𝒢 be the σ-algebra generated by r, |c^f| and own randomness.
- Define δ_{j,ℓ}(t) := 𝔼[sign c^f_j(t − ℓ) | 𝒢] and the **conditional sign asymmetry** A_{j,ℓ} := (𝔼[c^f_j(t−ℓ)² δ_{j,ℓ}²]/𝔼[c^f_j(t−ℓ)²])^{1/2} ∈ [0, 1].
- Then, in open loop (the percept process exogenous to the agent), every scalar output Y(t) of the agent, on any channel, satisfies |corr(Y(t), c^f_j(t − ℓ))| ≤ A_{j,ℓ}.
- If the percept law is invariant under the flip of c^f_j, then A_{j,ℓ} = 0 and the covariance is exactly 0.
- The observable copy defect on k is then ≥ (1 − A²_{j,ℓ})^{1/2}.

*Proof.*
- By the theorem, Y(t) is 𝒢-measurable up to own randomness, which is independent. Also |c^f| is 𝒢-measurable.
- So 𝔼[Y c^f_j] = 𝔼[Y|c^f_j| δ_{j,ℓ}].
- Cauchy–Schwarz gives |𝔼[Y c]| ≤ (𝔼Y²)^{1/2}(𝔼[c²δ²])^{1/2}. The defect follows from the identity in §3.0. □

Checks:
- F4a (sign-symmetric fast band, a random nonlinear functional with memory): max|corr| = 0.003, with sampling noise 0.009.
- F4b (strongly skewed fast band): |corr| = 0.15 ≤ A = 0.89.

**What it does and does not give.**
- On 𝒯 the guarantee holds for every route and every parameter (closure under every operation, including learning). It needs **no gain ceiling**: twisted outputs can respond strongly to the partner's movement *energy*, which is the human below-surrogate fast band (C1).
- Its strength depends on A, a measurable property of human fast-band face motion. It is ≈ 0 for oscillatory head motion. For blinks, whose band-passed waveform is skewed, it is plausibly large (§8).
- On 𝒮 the group acts trivially (Schur). There, as the symmetry synthesis states, no equivariance can exclude a scaled identity. That is why 𝒮 needs Lemma 6, Theorem 3 and Theorem 4.
- Closed loop: if the partner follows the agent, correlations at negative lags reflect the partner's following, not the agent's. The theorem is about the agent's response map.

### 3.8 Lemma 7 (route completeness)

*Statement.* By A1–A8, every partner-dependent influence on y on a window lies in exactly one of the classes below.

| Route | Path | Bounded by |
|---|---|---|
| R1 router | gate → router (both the u_j factor and the logits, including the key path through 𝓡 and the context low-pass) | Lemma 6(2)–(3): pointwise W_k M_k, whatever the logits do |
| R2 fibre | gate, content pulses, ŝ, D, keys → 𝓡 → y^F | (R) with Δv = (Δg, κ_bΔb̃, κ_ζΔζ̃) |
| R3 slow | anything → events (partner, content, body) or tilt → b → b̃ → H and 𝓡; anything → m^pre → ζ → ζ̃ → 𝓡, N_own, tilt | slews v_b, v_ζ (A5) |
| R4 floor | partner voice activity → 𝓜 → floor r → N_own role term | cap O_k (face); alternation on voice and articulation (Prop. 3c) |
| R5 Claude | gate → 𝓜 → draft selection and retrieval → Claude → text → content pulses (R2) and content events (R3); own speech → N_own voice and visemes | content enters only through R2 and R3; own-speech prosody has no gate input (§2.10) |
| R6 learning, memory and replay | any → stored records → nightly updates | parameters stay in Θ; every bound is uniform over Θ (A8) |
| R7 attribution and habituation | gate → a_t → event weights (R3); gate → keys → μ → A → logits (R1) and σ_d (R8) | as listed |
| R8 own variation | σ_d(t) depends on the partner through A, but its sign process ξ does not | Theorem 4 uses only 𝔼[d·u] = 0 |
| twisted | everything above, on 𝒯 | Theorem 2 |

*Proof.* This is an inspection of the code graph in §2.
- Every edge out of p goes to Γ (A1).
- Every edge out of Γ goes to 𝓡, the router, 𝓜 or the attribution estimator.
- 𝓜's out-edges go to the floor decision, selection/retrieval keys, attribution and replay (§2.12).
- Selection reaches the output only as text, then content pulses and content events.
- Events reach b only through buckets (A4).
- b and ζ reach the output and 𝓡 only through b̃ and ζ̃ (A5).
- Weights change only in replay (A8).
- Role reaches only N_own (role term) and the router queries. Router queries are inside R1's pointwise bound because that bound holds for every logit.
- There is no other edge. □

**What the critiques found, and which class covers it.**
- The care-loop slope → R2. Every loop is inside 𝓡.
- The shared learned estimate → R2. ŝ and D are inside 𝓡.
- The content-layer events → R2 and R3.
- Event rate → R3 and Lemma 2(c).
- Held levels → Theorem 6.
- The relationship key → constant within a session. Across sessions it is part of Θ and the own-typed inputs, and every bound is uniform over it.
- The nightly drift → R6.

### 3.9 Theorem 3 (D78: every per-channel quantity named and bounded; no quantity runs the whole face or a large subspace to copy)

**The per-channel quantities** (D78's "each channel's strength"):

| Quantity | Per expression? | Context-set? | Sign? | Innate ceiling |
|---|---|---|---|---|
| Router slot weights ω_{kja} (learned heads, context: needs ζ̃, base b̃, κ_rel, role r, partner keys) | yes, per (own channel, partner coordinate, lag) | yes | yes (± slots) | row cap W_k; total τ |
| REN face sensitivity on channel k (learned θ) | yes | yes (all own inputs) | yes | c_k |
| Base display on channel k (learned H, J, ψ) | yes | yes | yes (J learned with sign) | A_k amplitude, v_b slew; partner writes ≤ bucket |
| Role pattern on channel k | yes | yes | yes | O_k |
| Own variation | no partner content | – | – | floor σ₀ (from below) |
| Twisted channel response | yes | yes | sign-blind by construction | none needed (Thm 2) |

**Statement (all routes).** For every parameter value in Θ, every own-randomness realisation, every Claude output and every window, for each k ∈ 𝒮:

  RMS_T(Δy_k) ≤ W_k M̄_k + c_k ā_g + O_k + 2Σ_k T_s,  (3a)

with Σ_k := A_k v_b + c_k(κ_b v_b + κ_ζ√n_ζ v_ζ) + L_own(v_b + √n_ζ v_ζ). Hence:

  |c^{LS}_k| ≤ (W_k + c_k)χ_k + (O_k + 2Σ_k T_s)/a_k.  (3b)

For any K ⊆ 𝒮, the per-channel pooled RMS of Δy_K satisfies:

  RMS_T(Δy_K)/√|K| ≤ τ M̄_K/√|K| + c_max ā_g/√|K| + O_max + 2Σ_max T_s,  (3c)

with M̄_K := RMS_T(max_{k∈K}M_k). The pooled gain satisfies:

  |c^{LS}_K| ≤ τ ϖ_K + c_max ν_K/√m_g + (O_max + 2Σ_max T_s)/ā_K,  (3d)

where:
- ϖ_K := ‖max_{k∈K}M_k‖_T‖max_{k∈K}|S_ℓu_k|‖_T/‖S_ℓu_K‖²_T ∈ [1/|K|, 1];
- ν_K := ‖Δg‖_T/‖S_ℓu_K‖_T;
- ā_K is the pooled RMS of u_K.

If the allocation's partner-driven part is frozen over the window (‖Δμ‖ = 0), the router term in (3d) improves to τ/|K| for a partner moving K coordinates with equal power.

*Proof.* Decompose Δy_k by Lemma 7.
- **R1.** Lemma 6(3) gives RMS(Δy^R_k) ≤ W_k M̄_k. Under g⁰, u = 0, so y^R(g⁰) = 0.
- **R2.** By (R), ‖W₁Δz‖ ≤ ‖W₂Δv‖ ≤ ‖Δg‖/√m_g + κ_b‖Δb̃‖ + κ_ζ‖Δζ̃‖. The k-th term gives ‖Δy^F_k‖ ≤ c_k(·).
- **R3.**
  - Both runs start from the same b̃(t₀) and ζ̃(t₀), and each moves at most v_b T_s and √n_ζ v_ζ T_s.
  - So sup_t‖Δb̃(t)‖ ≤ 2v_b T_s and sup_t‖Δζ̃(t)‖ ≤ 2√n_ζ v_ζ T_s.
  - Through H (Lipschitz A_k), through 𝓡 (c_kκ_b, c_kκ_ζ) and through N_own (L_own), the RMS contributions are bounded by 2T_s times the corresponding slew rates.
- **R4.** |ΔN_own,k| ≤ O_k + L_own(‖Δb̃‖ + ‖Δζ̃‖). The second part is already in Σ.
- **R5–R7** reach y only through R1–R4 (Lemma 7).
- **R8.** d is identical in both runs (same realisation), so it cancels in Δy.
- Sum by the triangle inequality to get (3a). (3b) is Cauchy–Schwarz: |c^{LS}| ≤ RMS(Δy_k)/RMS(u_k).
- For (3c)/(3d):
  - Lemma 6(3) gives Σ_{k∈K}|y^R_k(t)| ≤ τ max_{k∈K}M_k(t), so ⟨y^R_K, S_ℓu_K⟩ ≤ τ Σ_t max_k M_k(t) max_k|S_ℓu_k(t)|. Then apply Cauchy–Schwarz in t.
  - Lemma 5 gives ‖Δy^F_K‖ ≤ c_max‖Δg‖/√m_g.
  - The rest is as in (3a).
- Frozen allocation: ω is then constant, so the pooled gain is Σ_k ω_{kk·}σ_k²/Σσ_k², plus cross terms that vanish for independent coordinates. This is ≤ τ/|K| for equal powers. □

**Numbers** (§2.1 constants: a_k = 1, χ_k = 1, Σ = 9.5·10⁻⁴ s⁻¹; F10 and F11):

| | T = 4 s | 10 s | 30 s | 60 s |
|---|---|---|---|---|
| smile/brow, mid band (W = 0.30) | 0.54 | 0.55 | 0.59 | 0.64 |
| smile/brow, slow band (W = 0.25) | 0.49 | 0.50 | 0.54 | 0.59 |
| other 𝒮 channels (W = 0.20) | 0.44 | 0.45 | 0.49 | 0.54 |

Pooled, at T = 10 s:
- Any 4-channel subspace: ≤ 0.32 with frozen allocation; **≤ 0.47** in the worst case, with the attention chasing the partner (ϖ_4 = 0.86).
- The whole Schur face (32 channels): ≤ 0.14 with frozen allocation; **≤ 0.27** in the worst case (ϖ_32 = 0.24, measured for independent coordinates with the innate lag dispersion).

**Discussion: why D78 is met, and where it is tight.**
- **No single quantity runs the whole face, or any large shared subspace, from flat to copy.** For |K| ≥ 4 the largest pooled gain any route can produce is 0.47, and for the whole Schur face 0.27. Each of these is an innate constant: the copy end of every dial is out of reach.
- **Each per-channel quantity is per expression, can flip sign and is context-set** (table above). Its ceiling is innate (§2.1), compiled into a parameterisation that every learning rule stays inside.
- **Window dependence.**
  - The bound grows with the window only through the slow routes (2ΣT), by 0.11 per minute at most.
  - Beyond 60 s the router and fibre see only the partner's deviation from their 60-s baseline.
  - The relevant long-window phenomenon is the base following the partner's mood, which is C9 ("converge in parameters"). Its total amplitude on any channel is ≤ 2A_k + 2c_kκ_b = 0.65 in the agent's own units, reached at no faster than v_b.
  - Theorem 6 shows the base is level-blind: there is no force toward the partner's held level.
- **Not covered: χ_k ≫ 1.** When channel k is a minor partner coordinate that cross-channel slots can reconstruct from major ones, the gain on k can exceed the table by χ_k. That is reconstruction, not copying of k's own signal. The fidelity bound of Theorem 4 still applies.

### 3.10 Theorem 4 (an observable copy-defect floor that no route and no learning can remove)

*Statement.* Assume open loop: the partner's percept process is independent of the agent's own randomness, and window averages converge (stationary ergodic processes, T → ∞). For any K ⊆ 𝒮 and lag ℓ, let C_K bound |c^{LS}_K|, from (3b) for one channel or (3d) for a set, and let ā be the pooled RMS of u_K. Then

  δ_K ≥ σ₀/(C_K²ā² + σ₀²)^{1/2}.

Finite windows add a sampling error of order 3/√N_eff (F7).

*Proof.*
- Write y_K = Δy_K + o_K + d_K, where o_K := y_K(g⁰) − d_K is the own part. In open loop, o_K is independent of the partner.
- Window averages ⟨d, u⟩/N, ⟨o, u⟩/N, ⟨d, Δy⟩/N and ⟨d, o⟩/N → 0. For the d terms this is because ξ is zero-mean and independent of everything else (A6).
- Let q := ⟨Δy_K, u_K⟩/‖u_K‖. Then:
  - ⟨y_K, u_K⟩ → q‖u_K‖;
  - the component of Δy_K + o_K along u_K tends to q, so ‖Δy_K + o_K‖² ≥ q² asymptotically;
  - ‖y_K‖² → ‖Δy_K + o_K‖² + ‖d_K‖².
- Hence ρ_K² ≤ q²/(q² + ‖d_K‖²), since x ↦ x/(x + c) increases.
- Now q = c^{LS}_K‖u_K‖, so q²/(|K|N) = (c^{LS}_K ā)² ≤ (C_K ā)². Also ‖d_K‖²/(|K|N) ≥ σ₀².
- Apply the identity δ = (1 − ρ²)^{1/2}. □

*Numbers* (σ₀ = 0.15, ā = 1):
- single channel: δ ≥ 0.23 (the worst case over T ≤ 60 s);
- any 4-channel subspace, worst case: δ ≥ 0.30;
- whole Schur face, worst case: δ ≥ 0.49; with frozen allocation, 0.72.

At ā = 2 (the partner at twice their typical expressiveness), single channel δ ≥ 0.12 and whole face (frozen allocation) 0.46 (F10, F11).

*Meaning.*
- The scale-free copy metric used by the critiques can be satisfied at any small gain by a counterfactual difference: Δy = 0.02u has counterfactual defect 0. On Schur components no structure can prevent that (Schur's lemma, symmetry synthesis statement 4).
- What an observer sees is y, not Δy. Because every route has a gain ceiling and the agent always carries independent own variation, the *observed* face is never better than a δ_K-defective copy, whatever the weights.
- This composes a gain certificate with an independent-innovation floor into one defect bound. It is my answer to the whole-loop synthesis's open problem 1 (composing a gain certificate with a non-gain currency), using "own variance" as the second currency.

### 3.11 Theorem 5 (copy is not an attracting state, under the design's own learning, with no correct-model assumption)

**(a) Unreachable for every parameter.**
- Theorems 2–4 hold uniformly on Θ, and every learning rule of §5.6 stays in Θ (A8).
- So the set of behaviours with δ_K below the floor is empty for every parameter any learning can reach. An empty set cannot attract.
- This uses no assumption that any model is correctly specified. It is the critique-3 loophole (X3) closed at the level of reachability.

**(b) No self-sustaining matched state in the dyad.**
- Fix the slow own-typed paths and the floor state over a window ≤ 30 s.
- The agent's continuous partner→output map (router + 𝓡) has incremental ℓ₂ gain

  Γ_A ≤ (W_max τ)^{1/2} + c_max^{all}/√m_g + 2U_max τ c_ω/((1 − γT_s/2T_R)√m_g) = 0.42 + 0.11 + 0.11 = 0.64,

  by Lemma 6(4)–(5) and (R) with the twisted c = 1.
- If the partner's incremental mimicry gain g_p (an empirical property; whole-loop synthesis, open problem 4) satisfies g_p Γ_A < 1, i.e. g_p < 1.56, then by the small-gain theorem the dyad's continuous part is contracting. Mutual matching cannot sustain itself.
- Persistent states live only in the base, which the partner reaches through ≤ 5 + T/24 s events (Theorem 1c).

**(c) The routing learning loop has a unique stable fixed point (mean field, linear echo).**
- The routing head is trained (§5.6) toward the normalised shared-fate coefficient s = cov(T_k(t+h), u^ex_j(t − ℓ_a))/(σ_T σ_u). Here σ_T := A_k v_b h is innate (the largest possible display change over the horizon h), so |s| ≤ 1.
- Suppose the partner echoes the agent's router output with gain ≤ g_p, through events weighted by (1 − ā), and the echo's effect on T is linear. Then s(ω) = s* + (1 − ā)g_p ω/w·λ_e with λ_e ≤ 1.
- The mean-field update ω ← w s(ω) is a contraction iff (1 − ā)g_p λ_e < 1. That holds for g_p < 1 with no attribution at all (ā = 0), and for g_p < 1/(1 − ā) with it.
- The fixed point is w s*/(1 − (1 − ā)g_p λ_e), clipped to [−w, w].
- F6 (instance λ_e = w): 12 of 12 cases converge to the formula. The rejected alternative (correlation-normalised learning with an estimated scale) is bistable at ±w without attribution (F6). That is why the innate normaliser σ_T is used.
- This part is conditional on a linear-response echo and g_p; parts (a) and (b) are not.

**(d) Held matching is repelled by a satiable drive.**
- If an allocation is held, Ψ = ‖A‖² rises above Ψ*. D_R > 0 then raises σ_d toward 2σ₀, which raises the floor of Theorem 4 (at a single channel with R = 0.55, from 0.26 to 0.48), and lowers the held slots' logits by γ(A − a*)₊.
- When the allocation varies, D_R returns to 0 (satiable).
- I do not claim that habituation alone bounds the time-averaged concentration. With γ = 4 it does not: the bound a* + (L − b₀ + ln((1 − a*)/a*))/γ is > 1 for L − b₀ = 4. Only the floor increase is guaranteed.

### 3.12 Theorem 6 (held levels and event rates)

**(a) A held partner expression has these effects, and only these.**
Suppose the partner's percept is constant from t_h. Then:
- **Router.** u^𝒮 → 0 with the 60-s EMA, |u(t)| ≤ |u(t_h)|e^{−(t − t_h)/60 s} up to filter transients, so the router's response to a held expression decays to 0.
- **Fibre.** 𝓡 keeps receiving the held level ℓ, so a **sustained response within c_k ā_ℓ** remains. This is declared: the design is *not* level-blind in the fibre. A concerned face toward a partner who has looked sad for a minute is wanted, and it is capped.
- **Base.** The held level writes at most B_p + ρ_p T_tr ≤ 3 events, after which b is autonomous. Here T_tr ≈ 13 s is the transient: 3.3 s of fibre memory plus the 10-s high-pass.
  - 𝓡's output converges under a constant input (contraction), so the 10-s high-passed proposal tends to 0.
  - After the transient it stays below θ_ev/2 and nothing re-arms.
  - Any re-crossings during the transient are bounded by the bucket. The base dynamics have no term in ℓ, so **no force pulls the base toward any function of the held level.** The set {b : H(b) ≈ c·ℓ} is neither invariant nor attracting unless it happens to contain a well. Even then the base reached it by events, not by tracking.

**(b) Event rate is not a dial beyond an innate rate.** In any window, the number of partner-caused base switches is ≤ B_p + ρ_p T_s, and their display effect is ≤ 2(A_k + c_kκ_b)v_b T_s whatever the rate. A partner who flashes smiles faster than once a minute moves the agent's mood no faster than one who flashes once a minute (Lemma 2(c), Theorem 1d).

*Proof.*
- (a) Router: the EMA is a stable first-order filter. Fibre: (R) and the fact that ℓ is an input. Base: the high-pass, hysteresis and refractory logic is innate, and A4.
- (b) Bucket and slew. □

### 3.13 Theorem 7 (satiable drives; Principle 6)

**(a) Satiable.**
- 𝒟 = 0 iff every ζ_i is within ε_i of ζ*_i and Ψ ≤ Ψ*.
- Draft selection uses strength β_sel = κ_s𝒟. At satiety β_sel = 0, the selection is uniform among Claude's drafts, and KL(π_sel‖π) = 0 (llm-coupling-synthesis §3.4).
- Each body variable has a restoring term −λ_ζ(ζ − ζ*). The information deficit decays without input.

**(b) Principle 6: the user's face is evidence only.**
- **Not a reward.** 𝒟's arguments are ζ and Ψ. Ψ is built from the agent's own allocation history.
- **Not a target.** By A7, no action-producing parameter has a partner-typed target:
  - the routing target is the agent's own display change;
  - the REN face head's target is the agent's own future display plus the innate prior;
  - the draft score is the agent's own predicted drive change.

  𝓜's partner-prediction loss trains 𝓜 only (stop-gradient).
- **Not regulated.**
  - No loop in Lemma 7 has the partner's percept as its controlled variable. No module plans through 𝓜's partner predictions.
  - The attribution weight *reduces* the influence of the partner's responses to the agent; it never seeks them.
  - The information drive excludes the partner's face, so the agent cannot satisfy curiosity by provoking expressions.

*Proof.* This is an inspection of the typed graph (Lemma 7) and the loss list in §6.3. □

### 3.14 Theorem 8 (time scales from reflex to temperament follow from the structure)

| Scale | Set by | Derivation |
|---|---|---|
| Reflex, 0.35–0.65 s | router tap ℓ₁ | y^R is a delayed copy-weighted sum; nothing in the router can respond before ℓ₁ + render latency |
| Context, ≥ 2 s | τ_ω low-pass and tap ℓ₂ | z^key responds to a step with time constant τ_ω, so context effects on matching lag by seconds (mimicry synthesis: 2–4 s) |
| Fibre memory, ≤ 3.3 s | contraction rate ᾱ | Theorem 1(a): the partner's influence through continuous routes decays as ᾱ^t |
| Partner baseline, 60 s; matching habituation, 2 min | τ_p, T_R | stable filters |
| Episode (held feeling), 5 s to settle, minutes to show | ε_b (Lemma 3 rate), v_b | the base settles in its well in ≈ 1/ε_b; the display moves ≤ v_b, so a full mood change on a channel takes ≥ 2A_k/(A_k v_b) = 20 min |
| Mood, hours | bucket refill and well escape | ≤ 1 partner write per minute, and Kramers 6–19 h (estimate, §3.3) |
| Temperament, weeks | nightly replay with anchoring | centres and biases move by a replay step size η_ψ per night, anchored to a precision that accumulates (§5.7) |

*Structural statement (proved).* The partner's influence lasts longer than 3.3 s only through the base (budgeted, Theorem 1c) and replay (A8). Every slower time scale is therefore a property of the agent, not of a gain.

### 3.15 Theorem 9 (reading the other through one's own body)

- **(a) Perception in own coordinates.**
  - P_φ is fitted on the agent's own renders: P_φ(R(m)) ≈ m for m in its babbling set.
  - If the partner's appearance o is in the range of R and P_φ is an exact left inverse there, then p = R⁻¹(o): the agent perceives the partner as the motor command that would make its own face look like that.
  - Outside the range, p is P_φ of the nearest-in-features own render, with error ≤ Lip(P_φ)·dist_feat(o, R(M)).
- **(b) State by inverting its own expression map.**
  - D is trained so that D∘E_own = id on the agent's own visited states, where E_own(b̃, ζ̃) := (H(b̃), N_own(b̃, ζ̃)) restricted to levels.
  - If the partner's levels satisfy ℓ = E_own(s) for an own state s, then ŝ = D(ℓ) = s exactly.
  - Otherwise ‖ŝ − D(Π ℓ)‖ ≤ Lip(D)·dist(ℓ, E_own(S_own)), with Π the nearest-point projection onto the agent's own expressive repertoire.
  - So the agent can read in another only states it has itself been in and expressed. What it has never done with its own face is read only through its projection. This is Yoshida & Man's own-decoder inference, with the decoder trained on own life only.
- **(c) Held in the other slot.** ŝ is never added to b or ζ (A2). It influences the agent only as a 𝓡-internal feature (certified) and as a selection key.

*Proof.* (a) and (b) are the left-inverse property plus Lipschitz continuity. (c) is A2. □

### 3.16 Lemma 8 (the echo kernel is identified by the agent's own variation, whatever the partner model)

*Statement.* Let the partner's gate deviation be u = G*y + n. The partner-endogenous n is independent of d (always true: d is the agent's own random source). Let y = d + F(u, own) for any causal map F, nonlinear and learned. Then S_{ud}(f) = G(f)S_{yd}(f), so Ĝ = S_{ud}S_{yd}⁻¹ = G wherever S_{yd}(f) ≠ 0.

*Proof.* S_{ud} = G S_{yd} + S_{nd}, and S_{nd} = 0 by independence. Relevance: d enters y additively, so S_{yd} ≠ 0 at frequencies where d has power and the loop has no exact cancellation. □

This is the instrumental route of Forssell & Ljung (1999), via the contingency-causal synthesis.

*Caveat.* G is the best linear echo in the dither direction. A nonlinear partner echo is identified only to first order.

### 3.17 The human non-copying signatures (non-copying-dynamics synthesis C1–C10)

Key: G = guaranteed by a theorem here; P = permitted and producible by the object, not proved.

| | Signature | Status and mechanism |
|---|---|---|
| C1 | band-signed coupling in one channel (positive 0.2–1.1 Hz, below surrogate at 2.6–6.5 Hz) | **G** for zero linear coupling on the fast band (Thm 2) and for sign freedom per band (separate slots per band). **P** for below-surrogate fast coherence: 𝓡's twisted outputs can make own fast motion complementary to partner energy (ε) |
| C2 | short-lived divergence relaxing to independence | **P**: ± slots per channel, tap ℓ₂ context sign, habituation |
| C3 | shared referent, different form | **P**: content pulses and events (referent) vs router (form) |
| C4 | role sets the sign; asymmetric lead and follow | **G** for asymmetry: router lags > 0, so the agent can only follow. **P** for role-set sign: role enters the queries |
| C5 | episode net level at or below chance | **G** that below-chance is reachable (negative slots; not a gain toward 0). **P** for when |
| C6 | no single quantity runs coupling; stance and attention can oppose | **G** (Theorem 3). Stance (κ_rel, b̃) and demand (ζ̃ information deficit, role) enter queries separately |
| C7 | anti-repetition of the joint pattern growing over minutes | **G** that held allocation raises the defect floor (Thm 5d). **P** for novelty growth |
| C8 | face coupling mostly common cause | **P**: content pulses reach 𝓡 within ~0.5 s of ASR; shared-event responses need no partner face |
| C9 | converge in parameters, not output | **G**: no output-level matching attractor (Thm 5a, 6a). **P**: the base and replay converge statistics |
| C10 | coupling does not disable self-restoration | **G**: the base gradient field ∇V and the body's −λ_ζ(ζ − ζ*) contain no partner term, so no coupling can switch them off |

### 3.18 What is exact and what is assumed

**Exact (for every parameter value):**
- Lemmas 1, 3–7;
- Theorems 1, 2, 3, 5(a);
- the route inventory;
- Theorem 6(b), 7, 9(c).

**Conditional:**
- Theorem 2's corollary (on the partner's sign asymmetry A, which is measurable);
- Theorem 4 (open loop and ergodic averages; finite-window error);
- Theorem 5(b) (g_p < 1.56, empirical);
- Theorem 5(c) (linear echo);
- Lemma 3's noise statement (Kramers, not proved);
- Lemma 8 (linear echo).

**Not claimed:**
- that any human-like signature in the P rows occurs;
- that the bounds leave enough expressivity (§8).

---

## 4. Why the closest existing mechanisms cannot do it

For each mechanism, here is the mathematical obstruction and what this design takes from it.

1. **Contraction networks and RENs (Revay et al. 2023; Lohmiller & Slotine 1998).**
   - By Lemma 1 a contracting system has one attractor per input, so no moods or held feelings.
   - By Lemma 4 its per-channel IQC ceilings form a box, which cannot separate one-channel matching from whole-face matching.
   - Theorem 2 of Revay (every contracting REN has *some* finite Lipschitz bound) offers no per-channel ℓ₁ budget.
   - Taken: the certificate, as the fence (R2).

2. **Equivariant networks (Cohen & Welling 2016; the symmetry synthesis).**
   - By Schur, on matching irreducibles the identity is an intertwiner, so equivariance excludes copying only on twisted components.
   - Taken: a sign-twisted gate on the fast band. As an object this is invariant features, which is standard.

3. **Active inference** (Lanillos et al. 2020; the reverse-appraisal critique).
   - When action and perception descend the same error, ȧ = −∂F/∂a with F ⊇ ½‖s_v − g(μ)‖²/Σ_v.
   - If the other's body falls under the self-likelihood, the fixed points have g(μ) ≈ s_v. That is imitation, which Lanillos observed ("mirroring actions similar to imitation").
   - Taken: attribution as evidence (their eqs. 11–14), used here only to weight base writes. Action never descends other-slot error (A2).

4. **Homeostatic RL** (Keramati & Gutkin 2014; Yoshida & Man 2024/25).
   - The drive is satiable, but partner influence enters through one coupling weight (Yoshida & Man: D = D_self + w·D_partner).
   - A single scalar w runs every channel together: a D78 violation by construction. A learned policy over partner-coupled rewards has no innate per-channel ceiling.
   - Taken: the satiable 𝒟 and the own-decoder reading.

5. **Attention and modern Hopfield networks.**
   - The router *is* softmax attention with a null slot. Its mass bound is the row-stochasticity of attention.
   - The base energy *is* a modern-Hopfield/log-sum-exp energy.
   - What attention and Hopfield retrieval lack:
     - a per-row cap, so a query can put all mass on one key, and nothing stops whole-face matching when keys align;
     - a budgeted write port. A partner-driven query re-retrieves every step, which is Lemma 2's unbudgeted port, so the partner's repetition rate becomes a dial.

6. **State-space models (S4, LRU, Mamba).**
   - Linear stable recurrences (|λ| < 1) are contracting, hence monostable (Lemma 1).
   - Selective SSMs can approach |λ| → 1 and hold memory as a slow integrator. That integrates held inputs: exactly the held-level leak (Lemma 2a with V′ ≈ 0).
   - Taken: 𝓜 (an ordinary predictor outside the fence).

7. **Coupled oscillators (Kuramoto).**
   - One coupling K takes identical oscillators from incoherence to locking: a whole-system dial whose locked state is attracting.
   - Nothing here is an oscillator, so the comparison only shows what is avoided.

**Conclusion of this section.** Each ingredient is an existing mechanism. The design is their composition under typing rules, plus three composition results I did not find in the sources read:
- Lemma 2 with Theorem 1 (necessity and sufficiency of a fibred, budgeted port for "contracting toward the partner, multistable within");
- Lemma 4 with the router (the ℓ₁ mass beyond any diagonal IQC);
- Theorem 4 (gain ceilings plus independent own variation give a scale-free observable defect floor).

---

## 5. The whole system, from the object

### 5.1 Perceiving the partner's face and voice

- **Face.** MediaPipe Face Landmarker gives 52 blendshapes and head pose, then P_φ maps them into own coordinates, then the gate Γ applies.
- **Voice.**
  - On-device acoustic echo cancellation with the agent's own output as reference: an innate linear adaptive filter, which is attribution for sound.
  - Then an 8-feature GeMAPS-lite stream relative to a running baseline.
  - Then an innate affine map into the agent's own voice coordinates (F0 deviation, loudness, rate, tension), replaced by the agent's own vocal inversion once S4 exists.
- **Words.** On-device ASR with timestamps feeds content heads and Claude.
- **Analysis by synthesis.** "Perceiving" the face is literally solving for the own motor command that renders like it (Theorem 9a).

### 5.2 The latent state where emotion emerges

The state is (x, b, ζ, A, ω).
- **Emotion-like structure.** It lives in the base: up to 64 wells in a 24-dimensional space, shaped by replay. A well's "meaning" is what the agent's own body, display and words do there. Nothing is labelled.
- **Effective dimensionality.** 24 (base) + 96 (fibre) + the allocation simplex. The structure is relational: wells are biased by the relationship key, allocations by needs and role.
- **Readouts only (Principle 2).**
  - valence := −d𝒟/dt, smoothed over 10 s;
  - arousal := ‖x_{t+1} − x_t‖ + Ψ.

  Neither is ever fed back.
- **Declared innate reflexes.**
  - the smile and brow onset slot prior;
  - the startle response (loud onset → blink and head-back, in N_own);
  - the innate synergy prior of H;
  - the floor rule.

### 5.3 Face output

The output is y = router + fibre + display + own intention + own variation, plus visemes, then synergies, then the placeholder face.
- The fast match appears at ℓ₁ ≈ 0.5 s.
- Context changes the sign at ~2 s.
- Moods show over minutes.
- The agent's own movement never stops.

The upper face is driven like the rest (known failure 11).

### 5.4 Voice

The agent's own speech uses macOS speech synthesis with per-word pitch, range, rate and volume from N_own. These are functions of the agent's own state and its utterance text only.

While listening, backchannels ("mm", nods) come from the router and 𝓡. Loudness convergence, which is human, is a positive slot on the loudness coordinate, capped like every other.

### 5.5 Coupling to Claude without text

Only the admissible channels of the llm-coupling synthesis are used.
- **Draft selection.**
  - N = 4 parallel drafts.
  - The score is the agent's own predicted drive change from uttering the draft, using a small own-body forward model on the draft's sentence embedding: predicted effort, information and repetition.
  - Selection strength β_sel ∝ 𝒟, so it is zero at satiety.
  - At most log 4 − 3/4 = 0.64 nats per reply.
- **Verbatim retrieval.**
  - Up to 3 of 50 candidate past spans (transcript only), chosen by a need-conditioned key from (b̃, ζ̃, κ_rel), plus ŝ as a key (certified).
  - This is mood-congruent recall and the brief's need-conditioned attention over memory.
- **Effort setting.** One of five levels from 𝒟 (admissible channel C5).
- **What Claude never sees.** No numbers, labels, descriptions or state-chosen instructions.
- **Content heads** (frozen MiniLM embedding → a small head; learned in replay to predict own drive change) turn the partner's and the agent's own utterances into:
  - content pulses e into 𝓡, counted in ā_g;
  - content events into the base, through bucket B_c.

### 5.6 Learning by living (what is learned, from what)

| Object | Target | When |
|---|---|---|
| P_φ | own babbling renders | daily babbling block + replay |
| 𝓡 face head | own future display change ΔH(b̃)(t+h) plus innate prior (A7) | replay |
| 𝓡 keys and router heads | shared-fate coefficients s = cov(T_k(t+h), u^ex_j(t−ℓ_a))/(σ_Tσ_u), u^ex = u − Ĝ*y (§3.11c) | replay |
| D (inside 𝓡) | own (E_own(s), s) pairs | replay |
| event proposals, content heads, J | own drive change after the event (does this matter to me?) | replay |
| landscape ψ | centres from visited b weighted by drive change; biases per κ_rel; separation projection | replay |
| H, N_own | display decodability (D) + innate synergy prior; own-speech prosody fit to own TTS | replay |
| 𝓜 | next gate, own body, turn end, drive change | replay (online only through states) |
| Ĝ, attribution | Welch spectra (Lemma 8) | online (states) |

### 5.7 Memory and replay

- **The episode store.** Γ-outputs, own outputs and efference, b, b̃, ζ, events, transcript spans and Claude's chosen drafts. A day is ≈ 0.15 GB. No raw video or audio (Principle 7). No c^f (A1).
- **Tags.** κ_rel, b at encoding, and 𝒟 at encoding.
- **Nightly replay.**
  1. Prioritised sampling by |Δ𝒟|.
  2. Reinstatement of the encoding-time base state as context. This is what makes learned routing and wells relationship-specific; the S6 ablation removes it.
  3. Updates of the table in §5.6, each inside its parameterisation.
  4. Temperament: centres and biases move with step η_ψ, anchored by an accumulated precision (an EWC-type quadratic anchor) so that weeks, not nights, reshape the landscape.
- **Replay never uses the partner's face as a target** (A7).

### 5.8 The brief's expressive-structure items

- **Content-dependent selection at the level of attention.** The router is attention whose queries are the agent's needs, role and relationship, and whose keys are the partner's coordinates as processed by 𝓡. Retrieval for Claude is attention over episodes keyed by needs.
- **Structure over people, episodes and time.**
  - Wells and their biases are a field over the relationship key.
  - Episodes are tagged segments.
  - Time scales come from the structure (Theorem 8).
- **What a low-dimensional version cannot do** (ablation predictions in §7):
  - **(i) Base reduced to one dimension** (one staircase). It cannot hold a relationship-specific mood and an episode-specific held feeling independently: two incompatible persistent states would have to share one coordinate.
  - **(ii) Router reduced to one shared gain per channel** (a box). It cannot produce "strong smile return while countering frowns" and also never match the whole face. A box admits g·I whenever it admits each g·e_ke_kᵀ (Lemma 4).

---

## 6. A buildable network

Parts that carry the new mechanism are marked **[M]**. The rest are ordinary choices.

### 6.1 Inputs and time encoding

| Stream | Rate | Encoding | Why |
|---|---|---|---|
| partner face | 30 Hz | MediaPipe 55 → P_φ → 16 own coordinates → filter bank → Γ **[M]** | own-body perception; sign-blind fast band |
| partner voice | 100 → 30 Hz | AEC → GeMAPS-lite 8 → 4 own voice coordinates → Γ | same gate |
| words | events | ASR timestamps → MiniLM → content heads → pulses and events | referent route |
| own body and efference | 30 Hz | ζ, m^pre, d, b̃ | own-typed |
| time | – | **no positional encoding in the fast path** | see below |

- **Why no positional encoding in the fast path.**
  - The certificate (R) is a property of a state-space recurrence. Attention over a growing context (RoPE or ALiBi with a key–value cache) would be an *uncertified memory route* from the partner's past to the face. That is exactly the kind of route the critiques found.
  - So time in 𝓡 is carried by the state, and frequency is carried explicitly by the filter bank: the band index is the time-scale coordinate.
  - The router's taps are explicit lags with an innate dispersion.
  - The base runs in continuous time with exact event timestamps.
- **Where RoPE or ALiBi is used.** Episodic retrieval for Claude uses an ALiBi-style linear recency bias on top of the need-conditioned key. That path is outside the face (R5).

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P_φ | 55 → 128 → 128 → 16 | 25,360 | replay (babbling) |
| 2 | filter bank, gate Γ **[M]** | fixed IIR, EMA, abs, LP | 0 | – |
| 3 | 𝓡_θ, robust acyclic REN **[M]** | n = 96, q = 192, m = 121, p = 216; direct parameterisation: X (384×384), Y₁ (96²), B₂, D₁₂, C₂, D₂₁, D₂₂-free, biases | ≈ 280,400 | replay |
| 4 | N_q, query net **[M]** | 39 → 64 → 128×8 | 68,160 | replay |
| 5 | coordinate embeddings E_j **[M]** | 32 × 8 | 256 | replay |
| 6 | router: softmax over 2048 + null; caps; habituation **[M]** | – | 0 | states online |
| 7 | landscape ψ **[M]** | centres 64×24; bias net 8 → 64; tilt 5 → 24 | 2,256 | replay |
| 8 | event jumps J **[M]** | 40 types × 8 (κ_rel) × 24, bilinear | 7,680 | replay |
| 9 | buckets, slews, onset logic **[M]** | innate | 0 | – |
| 10 | H display | 24 → 64 → 16, tanh | 2,640 | replay |
| 11 | N_own | 110 → 128 → 16 plus GRU 64 | ≈ 40,000 | replay |
| 12 | content heads | MiniLM (frozen) 384 → 64 → 32 | 26,720 | replay |
| 13 | 𝓜 | 2 LRU layers, H = 128 + heads | ≈ 250,000 | replay |
| 14 | draft scorer | 384 + 29 → 64 → 3 | 26,700 | replay |
| 15 | IV/attribution | Welch spectra, 32 × 32 × 20 bins | 0 (states) | online |
| | **total learned** | | **≈ 730,000** | |
| frozen | MediaPipe, MiniLM (22.7 M), ASR, AEC, TTS | | | |

The mechanism parts [M] hold ≈ 359k parameters, almost all in the REN.

### 6.3 Objectives

**Online:** none (A8). Only states change: Γ baselines, buckets, A, b, ζ, Welch spectra and λ.

**Replay, nightly.** The losses are:
- 𝓛_pred: 𝓜 and the REN prediction heads;
- 𝓛_face: 𝓡 face head toward own future display;
- 𝓛_route: cross-entropy of the allocation toward the shared-fate target allocation;
- 𝓛_D: own decoder;
- 𝓛_ev: event and content heads toward own drive change;
- 𝓛_ψ: landscape;
- 𝓛_H: decodability plus prior;
- 𝓛_scorer;
- plus the anchors.

All are minimised over free vectors whose every value lies in Θ: the REN by the direct parameterisation; ψ by tanh and projection; router heads unconstrained, because caps are applied after them.

### 6.4 Latency and memory (M1 Pro, 16 GB, peak ≤ 6 GB)

- **Per frame (33 ms budget).**
  - MediaPipe ≈ 13 ms, in its own process (measured in this project).
  - P_φ < 0.1 ms.
  - 𝓡: ≈ 0.6 MFLOP. The acyclic equilibrium layer is 192 sequential dot products, under 1 ms on CPU.
  - Router: 2048 logits × 8 dims, softmax and 2048 MACs, ≈ 0.1 ms.
  - 𝓜 ≈ 0.5 MFLOP, < 1 ms.
  - Base ODE and display < 0.1 ms.
  - Render 3–5 ms.
- **Visible fast match.** ℓ₁ (0.35–0.65 s, by design) + pipeline ≈ 80 ms.
- **Memory online** < 1.5 GB.
- **Replay.**
  - TBPTT on 30-s segments, batch 32. The direct parameterisation is recomputed per step: a 96×96 solve and Cholesky-free products.
  - ≈ 1 GB activations.
  - Nightly wall time ≈ 20–40 min on the M1 Pro GPU.

---

## 7. Ablation predictions (Principle 5), derived from the theorems

1. **Remove the sign-blind gate** (feed c^f to 𝓡). Theorem 2 then fails. After replay, linear coherence between the partner's and the agent's fast-band head motion can rise above a same-dyad surrogate. The prediction is that it rises when the partner's fast motion predicts the agent's display. C1's below-surrogate band is lost.
2. **Remove the mass τ** (row caps only). Under a "warm" context with many positive slots, the pooled whole-face gain rises from ≤ 0.27 to as much as Σ_k W_k/|K| ≈ 0.22 per channel *simultaneously*. Partner-swap surrogates then show broad same-sign whole-face coupling.
3. **Remove the buckets.** The display's mood shift over 10 minutes becomes increasing in the partner's smile-flash rate (Lemma 2b). With buckets the slope is zero above one flash per minute.
4. **Remove the slew.** Base switches show as steps on the face within a second of an event, and per-window totals rise by up to 2A_k.
5. **Remove the attribution weight.** With a partner who echoes the agent at a 3-s lag, the learned routing coefficients on the echoed channels exceed the no-echo fixed point by the factor 1/(1 − g_p λ_e) (Thm 5c). With the weight they stay at it.
6. **Remove own variation** (σ₀ = 0). The observable defect floor vanishes: lagged form similarity can approach the counterfactual gain's fidelity. Ψ-driven novelty in the joint pattern is gone.
7. **Remove the base** (C = 1). After a topic that moved the agent, carry-over in face and selection is gone beyond 3.3 s (Theorem 1a). Relationship-specific behaviour across sessions is gone.
8. **Remove D** (no own-decoder reading). ŝ-keyed retrieval and ŝ-dependent routing lose their dependence on the partner's levels in the agent's own coordinates.

---

## 8. Weak points and falsifiers

### 8.1 Weak points (where a critic should attack)

1. **Expressivity under the ceilings (the biggest risk).**
   - The REN's partner sensitivity is c = 0.15 against the *whole* 80-coordinate gate RMS. For a partner pattern on 8 coordinates, its response is ≤ 0.05 per channel.
   - Strong fast responses come only from the router, which is bilinear: weights times delayed partner coordinates. That can look mechanical.
   - The base display is slow: a full mood change takes 20 min.
   - A face that cannot show a strong sustained feeling quickly is a real risk. Raising v_b, c or W_k raises the totals linearly (Theorem 3).
2. **The twisted guarantee depends on A.** Blinks and other skewed fast events may have large conditional sign asymmetry, and then the fast band can be "copied" with fidelity up to A. A must be measured on human dyads.
3. **Dominance ratio χ_k.** (3b) bounds the gain relative to the partner's most active coordinate. Copying a minor coordinate that cross-slots reconstruct from major ones is bounded only through χ_k and by Theorem 4's floor.
4. **The defect floor relies on open loop and ergodicity.** In closed loop, partner-follows-agent correlations confound naive copy metrics. Analyses must use the agent's own variation as an instrument (Lemma 8), as evaluation E3 already requires surrogates.
5. **Theorem 5(b) needs g_p < 1.56 and Theorem 5(c) needs a linear echo.** Both are empirical.
6. **Uncertified switching elements.** The floor state r, the event thresholds and the bucket logic make the system hybrid. The dyad's contraction is proved only between switches, under a dwell time ≥ 0.2 s. A dwell-time stability proof with switching metrics is not given.
7. **Energy, not amplitude.** (R) bounds ℓ₂ energy over windows, not peak amplitude. A brief large transient within the energy budget is allowed (whole-loop synthesis, open problem 2).
8. **Principle 10.** This is one drive, one predictive constraint and eight typing rules, not a single functional. The router's shared-fate target is a regression, not a derivation from 𝒟.
9. **Principle 2.**
   - The body variables are innate and non-emotional.
   - The declared reflexes (smile/brow onset prior, startle, synergy prior, floor rule) are reflexes.
   - "Repetition load" is a body-like variable over own allocation. A critic may call it a hand-named variable.
10. **Kramers persistence is estimated, not proved.**
11. **The relationship key is frozen per session.** A change of partner within a session needs re-identification, which is not designed here.

### 8.2 Falsifiers (state-level, no face-matching)

1. **On published dyads** (Seamless, once permitted), estimate the conditional sign asymmetry A_j of fast-band face and head motion.
   - If A_j > 0.5 on most coordinates, Theorem 2 gives no practical guarantee and 𝒯 should be narrowed to the coordinates with small A.
2. **In the built system**, steer the routing queries (the E2 steering protocol) and measure the pooled gain on K = 4 and K = 32 under partner-swap surrogates.
   - Any value above 0.47 or 0.27 respectively is a proof error or an implementation error, not a tuning question.
   - With own variation logged, an observed defect below the Theorem 4 floor (beyond sampling error) falsifies the theorem's assumptions in that setting.
3. **Lesion the base (C = 1).** If mood carry-over across turns persists beyond 3.3 s, there is an uncounted persistent route, and Lemma 7 is wrong.
4. **Vary the partner's smile-flash rate** (scripted partner video, E3 style). If the 10-min display shift keeps increasing with rate above one per minute, the bucket is leaking.
5. **Human comparison (C1).** If no admissible parameters produce below-surrogate fast-band coherence while keeping positive slow-band coupling, the band-split account is insufficient.

---

## 9. Sources read for this design

| Source | How read |
|---|---|
| brief.md; research/questions.md (Reports 1–3, Q16–Q18 with the operator's answer); DECISIONS.md D68 (novelty bar), D78 | in full |
| research/foundations/designs.md; known-failures.md | in full |
| critique-3-design-partner-regulator.md, critique-2-design-reverse-appraisal.md, critique-design-modulated-manifolds.md | summary verdicts, source lists and opening proof checks (critique 3 §1 to T1′(b); manifolds critique to Lemma S(d)) |
| design-modulated-manifolds.md | §3.0 definitions and §6 network, for the copy-defect definition and the format |
| whole-loop-bounds-synthesis.md, symmetry-no-copy-synthesis.md, self-other-control-synthesis.md, non-copying-dynamics-synthesis.md | in full |
| Revay, Wang & Manchester, arXiv:2104.05942v3 | **primary text read:** §I–III and IV opening (Definitions 1–3, Remark 1, eqs. 6–12, Theorem 1 with (15)–(16), Theorem 2, Theorem 3 statement, Assumption 1). Also the project note (revay-2023-recurrent-equilibrium-networks.md). Appendices and §V construction details through the note only |
| Lanillos, Pages & Cheng, arXiv:2004.05473v1 | **primary text read:** §1–4 (Algorithm 1, eqs. 1–14, the experiments and the imitation side effect) |
| lohmiller-slotine-1998-contraction.md; forssell-ljung-1999-closed-loop-identification.md; contingency-causal-synthesis.md (IV route); llm-coupling-synthesis.md (§§1–4); yoshida-man-homeostatic-coupling.md; keramati-gutkin-2014-homeostatic-rl.md; cohen-welling-2016-group-equivariant-cnn.md; gu-2020-2021-hippo-s4.md (verdict); mimicry-context-synthesis.md (timing and per-expression rows); machine.md | project notes, read for the claims used |
| **Named but not read:** Kramers/Eyring and Freidlin–Wentzell (escape times); Golubitsky & Stewart; modern Hopfield networks (Ramsauer et al.); Mamba; Popoviciu's inequality is used as a standard fact and is proved in one line in Lemma 6 | no proof here rests on them except the labelled Kramers estimate |

---

## 10. Novelty verdict

**Recombination.** Every ingredient is an existing mechanism:
- the fibre is a robust REN;
- the router is softmax attention with a null slot and caps;
- the base energy is a log-sum-exp (modern Hopfield) landscape;
- the fast-band gate is invariant features under a sign group;
- attribution is Lanillos' model evidence with a Forssell–Ljung instrument;
- the satiable drive is homeostatic RL's drive;
- the buckets and slews are rate limiters.

**What is new is in the composition and three results about it.** I did not find these in the sources read; a critic should check them against the robust-control and hybrid-systems literature, which I did not survey.
1. **Lemma 2 with Theorem 1.** A system that is contracting toward the partner and multistable within must be fibred. Its partner→base port must carry an innate budget, or the partner's held level or repetition rate becomes a dial. The fibred, budgeted, slew-displayed structure achieves both. This answers the whole-loop synthesis's open problem 1 in one specific currency: switches per window plus a slew bound.
2. **Lemma 4 with Lemma 6.** No diagonal quadratic (IQC) ceiling can separate matching one channel from matching the whole face. An ℓ₁ conserved mass on an attention-like router does.
3. **Theorem 4.** Gain ceilings over all routes plus an independent own-variation innovation give a scale-free, observable copy-defect floor for every parameter. This closes the gap Schur's lemma leaves on same-feature channels without forbidding matching.

**Against the brief's novelty bar** (D68: a new computational mechanism on the level of attention, not an existing framework with structure added), this does **not** clear the second clause. It is best read as the first design in this project whose D78 claims hold *uniformly over every parameter value and every listed route*, with the route list made complete by typing rules rather than by enumeration. Its novelty is a constraint architecture with three theorems, not a new computation.

**The weakest point:** the price of those guarantees in expressivity (§8.1 item 1). It is unmeasured.

## Critiques 1a and 1b and the answer (recorded 2026-11-26T04:35:54Z)

**Critique 1a, proofs and the dial** (critique-design-fibred-attribution-core-proofs.md; checks in sims/critique-fibred-proofs/): 34 items, 12 valid, 11 with a gap, 11 with an error. **Fails D78 as proved.**
- **Worst error: the base does not persist under the design's own noise.** The Kramers estimate omits the relaxation rate ε_b, so the exponent is 1.53, not 7.65. With neighbouring centres at d_min, a well holds for about 37 s, not 6–19 h. The body tilt spends no token, yet at its maximum it shifts base-well occupancy about 136×. Theorem 1(c), Theorem 6(b) and Theorem 8 fail.
- **Theorem 2 (sign-blindness).** The proof needs an idempotent filter, and causal filters are not idempotent. Flipping a partner's 3 Hz motion changes the router input by 0.17–0.24 of its amplitude. A router-only agent shows 3 Hz coherence of 0.13–0.21 against a 0.01–0.02 surrogate.
- **Lemma 7 (route list) is incomplete.** Uncapped routes: N_own's speech-prosody and text input (Claude into face and voice), startle audio, voice channels with no role cap, and visemes. Best-of-4 draft selection keyed on the partner's inferred state correlates 0.78 with the partner's valence.
- **The held whole face is copied through the base.** Event proposals see both the partner's level and the displayed base, so they can act as a tracker inside the token budget. On 1-min means: correlation 0.93, defect 0.38, gain 0.36 on 16 channels. That is within the design's own whole-face figures (gain 0.27, defect floor 0.49), so those figures did not count this route. The own-variation floor does not exist outside 0.05–1 Hz.
- **Other errors:**
  - Lemma 4 is false for non-diagonal quadratic budgets (separation ratio 5.4).
  - Theorem 5: under a partner echo outside the instrument's band, learning runs to the row cap and the cap becomes attracting.
  - Lemma 6(4): the router's incremental constant reaches 1.17, not 0.42, under fast weight switching.
- **Gaps:**
  - The constants c_s, c_κ, c_ev, q_max, D_R^max and σ₀^p are never given. An exact own-decoder reading needs c_s ≥ 30.
  - The single-channel bound is quoted at 30 s and the pooled bounds at 10 s. At 30 s the pooled bounds are 0.51 and 0.31, and beyond about 3 minutes every bound is uninformative.
- **Expressivity:** the fast 0.5 s match fits the human data. But context and sign flips are possible only about once a minute, and the partner is not learned within a session. The common-cause route is capped near 0.07 against 0.3 for partner matching, the reverse of constraint C8.

**Critique 1b, reduction, novelty and principles** (critique-design-fibred-attribution-core-novelty.md): **recombination on both clauses.**
- Token bucket = average-dwell-time switching (Hespanha–Morse); Lemma 2 = bifurcation plus rate-induced tipping.
- "Contraction and persistence coexist only in fibred form" is false: p-dominance and k-contraction give multistability with contraction.
- The router = constrained softmax with fertility caps; Theorem 4 = the coherence/SNR identity; the typing rules = an information-flow type system.
- **Principles:**
  - Principle 2 is strained: the repetition drive is an installed motive.
  - Principle 3 is not essential: no behaviour needs the inversion of its own expression map.
  - Principle 6: there is a mild engagement incentive through the information drive.
  - Principle 10 fails: it is an assembly.
- **Expressive structure:** the persistent affect is about 6 bits, close to the few-gauges sketch the brief rejects.
- **Fails to explain:** held-level vocal convergence, partner history within minutes, fast reactions to content, interoception, grounding of Claude's emotion words.
- **Main lead:** a single information-capacity bound on everything the partner can influence, as a possible real primitive replacing the many caps.

**The answer (maintainer).** Both critiques are accepted.
- What survives as material:
  - the diagnosis that fast partner-driven state must be separated from persistent own state;
  - built-in per-channel ceilings parameterised so learning cannot exceed them;
  - the fast 0.5 s match;
  - the explicit typing of routes.
- The design's own route accounting missed the conceptual route, the voice and the base-tracker. This is the fourth design in a row where an uncounted route carries copying. Per-route caps, however many, keep leaking.
- That makes the novelty critic's lead the next step: a single capacity bound over everything the partner can influence.

**Status:** critiqued; held.
