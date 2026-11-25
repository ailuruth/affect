# Candidate 2: Thermodynamic mirror flow — affect as the energetics of a free-energy-descending flow, driven by a field of needs

**Status:** **stood down as an independent candidate on 2026-11-25**, after three independent verifications (sims/thermo/VERIFICATION.md, -2.md, -3.md).

**Why.** Each revision fixed what the last check found and exposed a new structural gap:
1. The stated objective, a tilted path measure, did not match the dynamics simulated, a gradient flow.
2. Putting body decay into the flow broke the Boltzmann condition, and an arrival read as negative valence.
3. Making the body an input fixed both, but:
   - removed the candidate's main distinctive prediction. Valence is no longer silent during a separation: TH4b's own run integrates to −0.104 over 25–55 s;
   - left the needs with no path into the latent or the face;
   - made body satisfaction rest entirely on the §2.4 choice rule, which is Costate's rule.

By the project's rule that a step failing twice is stood down, the candidate is not revised a fourth time.

**What it leaves as results.** All were verified, and each can be reused by any core:
- **The no-pump theorem, as a written KL-monotonicity proof** (§5). It is correct line by line (VERIFICATION-3). It needs constant M, J and T, open-loop inputs, and a Boltzmann-preserving latent flow.
- **A stronger guarantee the third reviewer found.** The need part of valence, −Σ ∂D/∂b·ḃ, averages to zero over *any* bounded body trajectory, closed-loop included, because Σ D(b) is a state function. Need-driven valence cannot be pumped, whoever drives the body.
- **Reading another person as Bayesian filtering with one's own model** (TH2d: R² 0.73; mismatched model −1.82). A deterministic synchronized copy fails (TH2a: −0.06).
- **Emotion types as metastable sets of a latent flow, read from the spectral gap** (TH5: K = 3, ARI 0.9996). Mood exits follow Kramers rates.
- **Reappraisal moves a deep mood only past a time threshold** set by depth over temperature (TH8).
- **Need-conditioned attention selects by who and what is needed, from structure and not capacity** (TH6, TH10). TH13-2 holds by construction (VERIFICATION-3).
- **Learning-progress curiosity** (shared toy) and **work-weighted replay** (TH9).

**Results so far (sims/thermo/RESULTS.md):**
- The no-pump theorem holds for any open-loop protocol when the frozen-input stationary density is Boltzmann. The KL proof is in §5. TH1a and TH12-1 confirm it.
- Circulation fixed in the agent's own frame that breaks the Boltzmann condition pumps valence, more as the input's amplitude grows (TH1b, c).
- **Reading by synchronization failed** (TH2a, R² −0.06). Reading by filtering with the agent's own model works (TH2d, R² 0.73), and the candidate is revised to use it. A mismatched model misreads (R² −1.82).
- Work-valence is silent during relaxation (TH4).
- Metastable sets are recovered (TH5).
- Toys TH1–TH9, TH2d and the shared curiosity toy are run.
- Independent verification is in progress.

**Sources:**
- the physicist sketch (sketches/physicist.md), for the tilted path measure, work as valence and metastable sets;
- the dynamical-systems sketch (sketches/dynamical-systems-mathematician.md), for the mirrored slow-fast flow and reading by synchronization.

**Simulations:** sims/thermo/. Parameters and predictions are fixed in sims/thermo/PREDICTIONS.md, and results are in sims/thermo/RESULTS.md.

## 1. Idea

The agent's latent and face are a stochastic flow that descends a **potential** 𝒰 at an affective temperature T. Its stationary density is Boltzmann, ∝ e^{−𝒰/T} (§2.2, second revision). The body is an input to that flow. It is driven by its own physics and by the agent's choices.

The potential is defined over a *field* of needs. Body variables are indexed over a learned space of entities (people, topics, episodes), so the agent can need contact with *this* person and predictability about *that* topic. It also contains the surprisal of the agent's own generative map, evaluated on the self and on a *set* of mirror replicas, one per known person. Each replica is a posterior ensemble of the agent's own stochastic model, filtered on that person's face (K-sep: inference only).

Everything affective is an energetic readout of this one system:
- **Valence** is the work the world and Claude do on the agent.
- **Arousal** is the dissipation rate. Its excess over the equilibrium value drives the global gain.
- **Emotions** are metastable sets of the learned flow.
- **Mood and temperament** are its slow coordinates.
- **Attention** to cues, memories and actions is a Boltzmann choice over discrete items (§2.4). The query is the cost-to-go gradient over the entity field, and the key is each item's predicted effect on that field. What the agent needs selects what it perceives, remembers and does, by content.

## 2. Formal statement

### 2.1 Variables

| Symbol | Domain | Meaning |
|---|---|---|
| ℰ | ℝ^{d_e}, d_e ≈ 16–32 | A learned embedding space of entities: people, topics, episodes. Each known entity is a point e ∈ ℰ. The set of known entities grows with experience. |
| b(e) | ℝ^k, for each known e | The body field. k innate need types (contact, predictability, activity) are indexed over entities: b_c(p) is contact with person p, b_p(τ) is predictability about topic τ. The activity budget is global, a field over a single point. |
| b*_k | ℝ | Innate set point per need type. It is shared across entities, so no entity-specific set point is innate. |
| b_lp(τ) | ℝ, for each topic or channel τ | *Added 2026-11-25 (D62).* Learning progress on τ: the windowed drop in the agent's own prediction error there (IAC; research/oudeyer-kaplan-hafner-2007-iac.md). It is a body variable with an innate set point, D_lp = (b_lp − b_lp*)². Curiosity comes from this variable, not from surprisal (TH7: dark room) or from a predictability set point (TH7: noisy TV). **The set point is this project's own addition (Principle 6). The source maximizes learning progress.** Shared toy: sims/curiosity/. |
| w(e) | ℝ_{≥0} | Weight of entity e in the potential. Learned from how much e has moved the body, which gives attachment-like weighting. |
| h | ℝ^{n_h} | The self's unnamed latent. |
| a | [0,1]^{n_a} | The agent's own action units and voice parameters. These are state coordinates, not outputs. |
| x̂_p = (ĥ_p, â_p, b̂_p) | for each known person p | Mirror replica of p: a copy of the agent's own flow driven by p's face. |
| θ | ℝ^P | Learned parameters (the generative map g_θ, the entity embeddings, w): temperament. |
| o | — | Observations: the agent's own face features, voice and body sensors, and each present person's AUs, prosody and conversation events. No labels. |
| u | — | Claude's only inputs to the engine: voluntary motor commands on a, and the conversation events its words cause. |
| T | ℝ_{>0} | Affective temperature: the price of departing from innate behavior. |

### 2.2 The single objective: a free-energy-descending Langevin flow on 𝒰 (revised after verification, 2026-11-25)

*[verification]* The first version of this section defined the objective as a path measure tilted by exp(−∫𝒰/T), while every toy simulated a gradient flow on 𝒰. The two are not the same: tilting gives a drift f₀ + 2TM∇ln φ_t, not −M∇𝒰 (sims/thermo/VERIFICATION.md). The candidate now adopts the dynamics its toys actually test.

**Second revision (after VERIFICATION-2).** The agent's flow covers z = (h, a) and the replica posteriors only. The body field b is an **input**, like the observations o. It is driven by its own innate physics (decay, satiation by partners' contact and events) and by the outcomes of the agent's discrete choices (§2.4). It is not driven by descent on 𝒰.

$$dz = -(M + J)\,\nabla_z\,\mathcal U_\theta(z;\,b_t, o_t, u_t)\,dt + \sqrt{2TM}\,dW,\qquad J=-J^\top,\ \ M, J \text{ constant},$$

$$\mathcal U_\theta(z;b,o,u) = \underbrace{\textstyle\sum_e w(e)\sum_k D_k\big(b_k(e)\big)}_{\text{depends on the input } b} + S_\theta(o^{\rm self}\mid h,a) + \text{(self-side social terms, §2.2 K-sep)} .$$

- With b, o and u frozen, and M and J constant (otherwise the drift needs the Ma–Chen–Fox correction), the stationary density of z is ∝ e^{−𝒰/T}. *[verification 2]* The J part conserves F; only the M part descends it. Equivalently, the flow descends the free energy F[p] = ⟨𝒰⟩_p − T·H[p]. **That is the single objective:** the agent's distribution over states relaxes toward low-potential states, at temperature T.
- *[verification 2]* **The innate reflexes, body decay and CONSPEC orienting are no longer in the agent's flow.** Body decay and supply are the body input's own physics. Reflexes are fixed functions of b and o that act on the body or on attention through §2.4. This keeps the Boltzmann condition.
- **J** is skew-symmetric. It carries the rhythms and circulation that *preserve* the Boltzmann density (see P1).
- **M** fixes the time scales: about 0.1 s for faces, 0.1 s to 10⁴ s across h, about 10⁶ s for θ.
- **D_k** is satiable: convex, with minimum 0 at b*_k. The fields include contact per person, predictability and learning progress per topic or channel (b_lp, D62), and the activity budget.
- **S_θ** is surprisal under the agent's own map g_θ.
- **Constraint K-sep, inference is not care** *[verification]*.
  - The replicas x̂_p are *posteriors*. They are updated by filtering with the agent's own map, the observation likelihood only (an EnKF, TH2d). They are **not** moved by the λ or κ terms.
  - The λ term, the other's inferred need, and the κ term, the pull toward the replica's face, act only on the agent's own a, u and choices.
  - Otherwise 𝒰's descent would bias the reading toward "the other looks like me" (κ) and "the other is fine" (λ).
  - With K-sep, the reading's independence of κ (TH2b) holds **by construction**. It is a constraint, not a result.
- **Planning.** For discrete choices made at about 1 Hz in the slow sector (§2.4), the agent evaluates expected cost-to-go. This is where the path-integral view survives: as an approximation used for choices, not as the dynamics.

### 2.3 Readouts, never set

- **Valence** v_t = −∂_t𝒰|_z = −(∂𝒰/∂b)·ḃ − (∂𝒰/∂o)·ȯ − (∂𝒰/∂u)·u̇. *[verification 2]* Body changes are work done by the world: an arrival that refills contact lowers Σ D(b) and gives positive valence. Over any periodic body schedule, the D part contributes zero net work, because it is a state function of b. It is minus the rate of work done on the agent by changes in its inputs (the Sekimoto split d𝒰 = δW + δQ; research/seifert-2012-stochastic-thermodynamics.md). The agent's own relaxation is heat, not valence (TH4). The sign convention: positive valence when the world lowers the agent's potential.
- **Arousal** α_t = T⁻¹∇𝒰ᵀM∇𝒰: the instantaneous **dissipation rate**. *[verification]* The first version called it "excess" dissipation, but it is nonzero at equilibrium. The excess version subtracts its equilibrium expectation, α_t − ⟨α⟩_eq, which is what should drive the global gain.
- **Emotions:** the metastable sets of the flow on (b, h), read from the spectral gap of its transfer operator (TH5). PCCA+ assumes reversibility, so J ≠ 0 needs a non-reversible variant.
- **Mood and temperament:** mood is the current basin of 𝒰_eff(h_slow) = −T ln ∫e^{−𝒰/T}dh_fast, and temperament is its shape, set by θ.

### 2.4 Attention: need-conditioned, content-dependent selection (sign convention fixed after verification)

When the agent chooses one item i from a set 𝒞 (a perceived cue to attend to, a memory to retrieve, an action to take, or a cue to pass to Claude), it uses

$$P(i) \;\propto\; P_0(i)\,\exp\!\Big(\tfrac1T\Big[\underbrace{-\,\partial V/\partial b}_{\text{query}}\cdot\underbrace{\textstyle\int \mathbb E[\Delta b(\cdot,t)\mid i]\,dt}_{\text{key}} \;-\; \Delta S_i\Big]\Big).$$

- **Query:** minus the gradient of the cost-to-go V with respect to the body field. *[verification]* The Feynman–Kac first-order expansion gives ∇V, not ∇𝒰. The myopic approximation −∂𝒰/∂b is what TH6 used, and it is valid only when the item's effect is short compared with the body's relaxation.
- **Key:** the item's predicted effect on the body field, integrated over the time it persists.
- **ΔS_i:** the item's expected *change* in surprisal. A reduction raises P(i). *[verification]* The first version added it with the wrong sign.
- **P₀(i):** the prior over items.

**This rule converges on Costate's.** With the exact cost-to-go, the query is Costate's μ field. The two candidates differ in the dynamics, in what valence is (work against −dV/dt), and in the no-pump theorem, but not in attention.

## 3. Derivations of the Principle 10 components

- **Homeostasis.** The D_k terms are zero, with zero gradient, at b*. A satisfied entity exerts no force. Satiation is per entity: contact with A can be full while contact with B is not.
- **Curiosity, in this formalism.**
  - Learning progress per topic or channel, b_lp(τ), is part of the body input field, with D_lp = (b_lp − b_lp*)² in 𝒰.
  - Choosing what to attend to is the §2.4 rule with query −∂V/∂b_lp and key E[Δb_lp | item]: the predicted learning progress on that item. With the myopic query, this is exactly the shared curiosity toy's selection rule (sims/curiosity/), which avoided both the noisy TV (3.3%) and the dark room (3.6%).
  - The earlier text, superseded: θ and the predictability field are part of the state. Visiting states that are learnable *about topic τ* lowers future surprisal on τ. Irreducible noise raises 𝒰 permanently, so there is no noisy-TV trap. Curiosity vanishes per topic as θ converges on it. 

> *[2026-11-25, thermo toy TH7, applies to this candidate]* **Curiosity as derived here fails a noisy-TV test.** With a pure-noise channel on offer, an agent with a two-sided predictability set point satisfies its set point with noise (39% of choices) and almost never chooses the learnable channel. Pure surprisal minimization gives the opposite failure, the dark room. Curiosity for *learnability* (learning progress) is not derived by any candidate yet. This is an open limit (sims/thermo/RESULTS.md TH7).

> *[2026-11-25, shared curiosity toy, sims/curiosity/RESULTS.md]* **Proposed fix.** Make *learning progress*, the recent drop in prediction error on a channel, an innate body variable with a set point. In the shared toy this agent avoided both the noisy TV (3.3%) and the dark room (3.6%), and it learned both learnable channels. To be stated in this candidate's formalism and tested with its own toy.


- **Valence and arousal.** §2.3. TH1 gives the guarantee and its limit; TH4 separates work from heat.
- **Mood, temperament, time scales.** Adiabatic elimination of fast variables, with ratios fixed by M.
- **Mimicry: an explicit coupling constraint, not derived** (restated 2026-11-25).
  - The physicist sketch derived κ as "gauge fixing": the term that makes the other's motor coordinates identifiable in the agent's own coordinates.
  - But the replicas here use the agent's *own* map g_θ, and its motor coordinates are already fixed, so there is no gauge freedom left for κ to fix.
  - So the κ term, ½κ‖a − â_p‖², is a stated coupling constraint, Principle 3's "perceived features drive the agent's own motor pathways".
  - Its consequences are derived:
    - overt mimicry gain κ/(k_a + κ);
    - its separate lesionability from reading (TH2b);
    - the S5 lag shift (TH3a).
  - Claude's voluntary u can suppress it.
- **Reading others (revised after TH2 and TH2d).** Each replica is a **posterior ensemble** of the agent's own stochastic flow, conditioned on the person's face: Bayesian filtering with one's own model, as in the physicist sketch's "posterior of (h̃, b̃) under my own g_θ".
  - The deterministic synchronization observer of the dynamical-systems sketch was tested and **failed** (TH2a: R² −0.06). It tracks the face but not the hidden body, because it has no process noise.
  - The ensemble filter reads the hidden body at R² 0.73 with the agent's own model (TH2d). With a mismatched model it reads at −1.82: misreading, not mere ignorance.
  - The contraction bound (Lohmiller & Slotine) still describes the deterministic part of the flow, but it is not the reading mechanism.
  - The reading is independent of κ (TH2b).
  - Empathy is λw(p). Mineness is the replica index.
- **Regulation by Claude.** Claude acts only by doing work on 𝒰, through its words as events and its voluntary face. A finite-time second law bounds it: moving mood from basin A to basin B in time τ costs at least ΔF_AB + ℒ²/τ, where ℒ is the thermodynamic length. A fast reappraisal of a deep mood is expensive.
  - **TH8:** in a double well with a high barrier, work is spent but the mood mostly does not move (2–31% crossed for τ ≤ 16), and excess·τ is not constant.
  - **The derived prediction is therefore a time threshold:** reappraisal moves a mood only when the time allowed approaches its escape time, e^{ΔU/T}.
- **Claude interface.** Claude couples to the engine only through attention (§2.4) and slow coordinates:
  - retrieval is the §2.4 softmax over stored episodes, which gives need- and person-specific recall;
  - the cues passed on are the top-k of the same softmax;
  - thinking budget and latency scale with the relaxation time of the slow modes ψ;
  - Claude sees its own rendered face.
  
  By averaging theory, only coordinates slower than one turn carry information across a turn (dynamical-systems sketch).
- **Replay.** The θ-force is a path expectation of ∂_θ𝒰. Offline it is estimated by re-running stored feature streams, with importance weights. The minimum-variance weight is ∝ |∂_θ𝒰|, approximated by the episode's work |W|. Replay weighted by "how much it moved the agent" follows, up to that approximation.
  - **TH9:** importance weights ∝ |work| cut the estimator's variance to 0.11 of uniform replay, unbiased.
- **Perception of face and voice.** This is analysis by synthesis: perceiving person p is *filtering*: the replica ensemble x̂_p is conditioned on o^p through the agent's own map g_θ (TH2d). *[verification 2: the first version had replicas relaxing by descent, the mechanism TH2a refuted.]* The three routes are three observation channels into that filter:
  - the coarse route is a fast, low-resolution observation channel, with an innate CONSPEC prior as its initial weights;
  - the dynamic route is the temporal part of g_θ;
  - the body route is â_p in the agent's own AU coordinates.
  
  Voice works the same way in prosody coordinates.

## 4. What it cannot derive

- The choice of need types and set points (innate).
- CONSPEC.
- The front-end feature extractors.
- The content of what Claude says.
- **Which face goes with which energetic readout.** Like Costate, it needs an innate expressive map.
- **The theorem against pumping valence needs the frozen-input stationary density to be ∝ e^{−𝒰/T}** (P1). Rhythms of the form −J∇𝒰 preserve it; other circulation can pump valence (TH1b).

## 5. Propositions (results in RESULTS.md)

- **P1, no affective perpetuum mobile (restated after verification).**
  - **Condition:** with θ frozen and the protocol frozen at any value, the stationary density is ∝ e^{−𝒰/T}. Under that condition, every periodic open-loop protocol gives period-averaged valence ≤ 0.
  - *[verification]* The first statement's condition, "conservative f₀", was not the right one. The reviewer reran TH1 with a rhythm of the form −(I + γJ)∇U, which preserves the Boltzmann density, and found no pumping: v from −0.06 to −0.63. TH1b's rotation γAz does not preserve it, and it pumps.
  - So the design constraint is **"rhythms only of the form −J∇𝒰"**, not "rhythms kept out of user-driven coordinates".
  - **Proof (KL form, written 2026-11-25).**
    - *Setup.* Let λ_t collect the inputs (b, o, u) and follow a τ-periodic open-loop protocol. Let z follow dz = −(M + J)∇U(z; λ_t)dt + √(2TM)dW, with M ≻ 0 symmetric and J skew, both constant. Let π_λ ∝ e^{−U/T} and F_λ = −T ln Z_λ. The density p_t solves ∂_t p = ∇·[(M + J)p∇U + TM∇p].
    1. *The relative entropy.* Write D_t = ∫p ln(p/π_λ). Then dD/dt = ∫∂_t p·ln(p/π) − ∫p ∂_t ln π_λ.
    2. *The skew part contributes nothing.* ∫∇·(Jp∇U) ln(p/π) = −∫(J∇U)·∇p − (1/T)∫p (J∇U)·∇U. The second term vanishes because J is skew. The first equals ∫p tr(J∇²U), which vanishes because J is skew and ∇²U is symmetric.
    3. *The dissipative part.* With ∇U = −T∇ln π, the M part gives −T∫p ∇ln(p/π)ᵀ M ∇ln(p/π) =: −T·I_M(t) ≤ 0.
    4. *The input term.* −∂_t ln π_λ = (∂_tU − Ḟ_λ)/T.
    5. *So* dD/dt = −T·I_M + (⟨∂_tU⟩_p − Ḟ)/T.
    6. *Over one cycle in the periodic steady state,* ∮dD = 0 and ∮Ḟ = 0. Hence ∮⟨∂_tU⟩dt = T²∮I_M dt ≥ 0. The mean work per cycle is non-negative, and the mean valence −⟨W⟩/τ ≤ 0.
    7. *Equality* holds iff p_t = π_{λ_t} throughout: the quasi-static limit. ∎
  - **Scope.**
    - λ must be open-loop: not a function of z. Any input that reacts to the agent (a responsive user, Claude reacting to the rendered face, the agent's own choices that move b) is excluded unless its information flow is counted.
    - *[verification 2]* The condition is sufficient, not necessary.
    - Circulation of the form −J∇U preserves π but creates no limit cycle, because U is a Lyapunov function of the deterministic part. A genuine autonomous rhythm (a limit cycle) violates the condition and can be pumped. TH12: Boltzmann-preserving circulation pumps nothing. A Hopf rhythm centred on the input was not pumped either, because it moves with the input. Circulation fixed in the agent's own frame (TH1b) was pumped.
  - In the periodic steady state, ⟨ΔV⟩ = 0 and ⟨Δs⟩ = 0 over a cycle. So ⟨w⟩ = ⟨q⟩ = T⟨Δs_tot⟩ ≥ 0, from Seifert 2012's integral fluctuation theorem ⟨exp(−Δs_tot)⟩ = 1 (research/seifert-2012-stochastic-thermodynamics.md). No source states this per-cycle form directly; the derivation is ours.
  - **Conditions:**
    - one bath, with the Einstein relation;
    - noise unaffected by the driving;
    - **no measurement or feedback.** Seifert notes that feedback can "extract work in a cyclic process". *[verification]* Claude closes such a loop too, because it reacts to the agent's rendered face.
  - **Consequence for the claim.** A user whose smiles respond to the agent's face is a closed loop. So P1 covers *open-loop* protocols, such as scheduled smiles. For a responsive user it holds only once information flow is counted. That caveat is the honest scope of the Principle 6 guarantee.
  - Tested in TH1, including where it breaks under internal rhythms.
- **P2 (revised).** The replica is an ensemble-filter posterior (TH2d) and, under K-sep, κ does not enter it. The κ lesion therefore spares reading **by construction** and removes mimicry (TH2b). The synchronization-observer version failed (TH2a).
- **P3, metastable sets.** The number of emotion types equals the number of eigenvalues above the largest gap of the transfer operator. Mood exits occur at Kramers rates ∝ e^{−ΔU/T} (TH5).
  - PCCA+ (research/deuflhard-weber-2005-pcca-plus.md) chooses the number k of sets "by eye" from the gap. It checks k by diagonal dominance (w_ii > 0.5) and assumes a reversible, self-adjoint transfer operator.
  - The agent's flow is not reversible once there are rhythms (J ≠ 0), so a non-reversible variant is needed. TH5 used a reversible potential and symmetrized counts.
- **P4, attention (§2.4).** A first-order expansion: the query is the cost-to-go gradient, and the myopic ∂𝒰/∂b is an approximation. Tested with the myopic query in TH6.

## 6. Expressive structure (brief.md requirement): toy TH6, run

**Result summary (sims/thermo/RESULTS.md TH6):**
- The scenario: A is present and sated, B is absent for 3 days, topic X is over-exposed.
- The field version attends to B's photo (0.99), chooses "message B" (0.99), and retrieves 4 of 5 B-episodes.
- *[verification]* **TH6-1 is refuted as a whole.** Its collapsed clause failed: noise ranked B above C. The keys were hand-set, not computed from content embeddings, and the collapsed arm's keys are identical by construction. A re-pre-registered variant with keys from content embeddings is owed.
- When A and B swap needs, with total need magnitude ‖F‖ held fixed at 2.5214, the selection switches to A.
- The collapsed two-gauge version, with the same keys summed and the same zero learned parameters:
  - splits evenly between A and B (ratio 1.00);
  - does not change its retrieval ranks under the swap;
  - gives the most retrieval mass to the sated person.
- **Effective dimensionality:** participation ratio 2.85 for the field (the pre-registered ≥ 3 was refuted narrowly) against 1.07 collapsed. *[verification]* The 2.85 depends on an unspecified schedule rule and one seed. The reviewer's reimplementation gives 1.9–3.2 across seeds, and 3.4–4.3 with topic exposure independent of presence. It is **not a property of the candidate**, and needs a re-pre-registered run with ≥ 10 seeds.

The original plan follows.

- **Effective dimensionality.**
  - The state is (h, a) plus one replica per known person, plus the body field over all known entities.
  - With N_p people and N_τ topics, the body field has about k·(N_p + N_τ) components. The latent dimension n_h adds to that.
  - The participation ratio of the state covariance is reported in TH6.
- **A behavior the low-dimensional version cannot produce.** Missing a particular person while socially sated.
  - With A present and contact with A full, but contact with long-absent B depleted, the field version's attention retrieves B-related memories and passes B-related cues.
  - *[verification: this was the plan, and the result differs]* In TH6 the collapsed version did not "attend to nothing social". It split 0.49/0.49 between A and B. What it cannot do is choose *which* person.
  - The ablation collapses ℰ to a point.
- **The richness comes from structure, not parameters.** The same g_θ and D_k serve every entity, and only the entity embeddings and weights w(e) grow.

## 7. Failure modes and the strongest published critique

- **Learned recurrent dynamics are not gradient flows.** Circulation that does not preserve e^{−𝒰/T} can pump valence (TH1b). The realization must parametrize the flow as −(M + J)∇𝒰_θ with J skew-symmetric (a Helmholtz-constrained network), or the Principle 6 theorem fails.
- A few hours of data a day may never produce a clear spectral gap. Emotion types would then be ill-defined, and Claude's names would drift.
- **Strongest published critiques.**
  - **Gershman 2019** (research/gershman-2019-free-energy-principle.md): "utilities can always be formulated as log probabilities". Planning as inference is therefore "a notational variant of Bayesian decision theory". The tilted path measure, with desirability z = exp(−V), is exactly such a variant (Todorov 2009; Kappen 2005). **Answer owed:** each claim must carry a prediction a plain utility-maximizer would not make. Candidates:
    - work-valence being zero during relaxation (TH4);
    - the S5 lag shift and persistence (TH3);
    - Kramers-rate mood exits (TH5);
    - reappraisal succeeding only past a time threshold set by the mood's depth over the affective temperature (TH8). That holds below the spinodal; above it, a large enough tilt moves the mood at once.
  - **Bruineberg et al. 2022** (research/bruineberg-2022-emperors-new-markov-blankets.md): "mathematical abstractions are treated as worldly entities". The formalism is so broad that "even the humble Watt governor" qualifies. By the same argument, "valence = work, arousal = dissipation" fits *any* Langevin system and cannot pick out affect by itself. **Answer:** this candidate claims only a functional readout that changes behavior under ablation (Principle 5). Whether these readouts deserve the names is decided by the evaluation protocols, not by the mathematics.
  - *[After the §2.2 revision the dynamics are a gradient flow, so linear solvability matters only for the slow-sector planning approximation.]* **The linear solvability needs noise and control cost tied together:** "ν = λBR⁻¹Bᵀ"; "noise and control should operate in the same dimensions" (research/kappen-2005-path-integrals-symmetry-breaking.md, research/todorov-2009-linearly-solvable-mdps.md). Body variables that the agent controls but that have no noise of their own, such as a deterministic activity budget, fall outside it.

## 8. Relation to the other candidates

- **Costate.** The attention rules converge (§2.4: with the exact cost-to-go, the query is Costate's μ field). The core dynamics differ: here a free-energy-descending Langevin flow on 𝒰, there an optimal controller of the cost-to-go. This candidate adds:
  - surprisal in the potential;
  - work-valence in place of total change;
  - a theorem against pumping valence (KL proof, §5) for open-loop inputs, given Boltzmann-preserving dynamics;
  - replicas in place of tied slots.
- **S5, after TH3.**
  - Under this candidate's own lesion of the agent's mimicry, the human's following persists (10/10 runs), and the peak shifts to an agent-leading lag (TH3a).
  - Under the emotional-pathway lesion that S5 names, following of sparse voluntary expressions was detectable in only 2/10 sessions.
  - The candidate's earlier prediction that S5 is "false as worded" was refuted in its own toy.
- **Contingency and parity.**
  - That candidate's directed contingency could be one of the D_k fields here, contact per partner as predictive dependence, which would make contact blind to polarity.
  - Its parity reader is this candidate's ensemble filter with a learned, linear-Gaussian map.
  - Its typed interface (icon and index up, sign down) is compatible with §3's interface.
  - The two differ on the source of mimicry: an explicit κ constraint here, the water-filling optimum there.

## 8b. Realization on this Mac, and data

- **The flow.** A Helmholtz-constrained network: drift −(M + J)∇𝒰_θ, where 𝒰_θ is a small MLP over (h, a, b-field) and J is a learned skew-symmetric matrix. This keeps P1's condition by construction. It runs at 30 Hz on CPU: one gradient evaluation per step, about 10⁵ parameters.
- **Replicas.** An ensemble filter of about 50–100 members per present person, running the agent's own flow at 30 Hz, the TH2d design. It is cheap with numpy or MPS.
- **Entity field.** Embeddings ℰ of 16–32 dimensions per known person, topic and episode, learned from co-occurrence and from which entities predict body changes. The weights w(e) ≥ 0.
- **Metastable sets.** Estimated offline, nightly, by a Markov state model over stored trajectories of (b, h).
- **Data.**
  - g_θ and the emission map come from self-babbling against the placeholder renderer. That needs no user data.
  - 𝒰_θ's learned part, the entity field and θ come from the operator's few hours a day.
  - The innate body physics, D_k, set points and T need none.
  - **The risk:** too few mood transitions per week to estimate a spectral gap (§7).

## 8c. Numeric predictions for the stage claims

- **S1-a (E3).** Coupling through κ beats both surrogates (TH3b: intact 10/10).
- **S1-c (E1).** The κ lesion removes the agent's mimicry. The partner's following of the agent survives with an agent-leading lag shift: zero-lag ρ from 0.333 to 0.234, and a peak of 0.270 at 0.18 s for k₀ = 2/s (TH3a, analytic and simulated).
- **S1-b (E2).** Steering the latent coordinate that sets own-expression precision changes the partner-driven share κ/(k_a + κ) of the face.
  - TH11: derived direction ρ = 0.74 (p ≈ 1e-18), random direction flat (p = 0.40).
  - One non-monotone step (0.319 → 0.317) failed the strict-monotonicity clause.
  - The full evaluation.md protocol (≥ 20 runs per level, sham lesion, both window settings, AU channel pairs) is for the engine.
- **S1-d (secondary).** Valence is exactly zero during a steady separation and nonzero only at departure and return (TH4). Costate predicts nonzero valence throughout the relaxation. This is a measurable difference between the two candidates.
- **S2-b.** After the emotional-pathway lesion, following of voluntary expressions is rarely detectable at sparse expression rates (TH3b: 2/10). The S2-b and S5 designs must control for statistical power.

## 9. Independent verification

Pending.
