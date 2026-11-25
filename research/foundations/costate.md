# Candidate 1: Costate — affect as the shadow prices of homeostasis

**Status: STOOD DOWN as a core candidate by the operator (Q7 answer, D68, 2026-11-25).** It is a homeostatic regulator over a few body gauges, with affect read out of values or prices, which is the design the operator rejected. Its verified results remain material. Earlier status, kept for the record:  **not complete** (third structure review: sims/structure/VERIFICATION-3.md).
- The core was verified twice (sims/costate/VERIFICATION.md, VERIFICATION-2.md).

| Expressive-structure item | Status |
|---|---|
| 1. Content-dependent selection | **Mostly met**, under the myopic rule only (see the expressive-structure section). |
| 2. Structure over a learned space | **Partly met.** Items live in a learned space. The need field over that space is instantiated (ES11) but has **no demonstrated benefit** (ES11-2, ES12-3). Time is shown only as per-person tracking, not through Costate's own slow μ or mood. |
| 3. Dimensionality and an ablation | **Partly met.** The behavioral ablations hold. ES13's participation ratios are dominated by the world's kernel and do not separate the candidate from its ablation. |
| 4. Richness from structure | **Partly met**, in worlds that match the model class. *ES20b:* the factored per-need selection rule (shared by both candidates) beats a full-state learned value increasingly as needs multiply. With 2 needs the monolithic value wins (1.36×). With 8 needs factored wins, by about 1.4× against a stable full-state baseline; the run's 0.05× reflected an unstable baseline (VERIFICATION-5). Slower drift increased the advantage, which is consistent with Dulberg et al. 2023. |

**What separates Costate from the Robust regulator.**
- Model-based look-ahead costs 0.73× the myopic rule (ES12, 120/120 seeds).
- ES12's look-ahead is a 6-step undiscounted rollout of one greedy base policy. It is not the full K5 rollout, and it never computes μ itself.
- A no-learning threshold rule beats both candidates (ES12-2).

**Owed:**
- ~~Show that the learned space pays for needs~~. Stood down after ES12-3 (refuted) and ES14 (a non-test). Item 2's field is **instantiated without demonstrated benefit**.
- ~~A K5 rollout over several base policies~~. Stood down (ES15: 1.19× the threshold rule).
  - Corrected diagnosis (VERIFICATION-4): the gap comes from exploration. With the true K and no exploration, the library rollout beats the threshold rule (0.976; a probe, not pre-registered).
- ~~Time through Costate's own slow μ or mood~~. Stood down after ES17 and ES17b (ρ 0.28 and 0.41 corrected for the truncated reunion; predicted ≥ 0.5). A weak but reliable signature, below the predicted strength.
- ~~ES7c~~ (done; see the expressive-structure section).

**Sources:**
- Core: the computational-neuroscientist sketch (sketches/computational-neuroscientist.md).
- Realization: the deep-learning sketch's tied dyad.
- Do-conditioning constraint: the game-theorist sketch.
- Interface bounds: the control-theorist sketch.

**Simulations:** sims/costate/. Parameters and predictions are fixed in sims/costate/PREDICTIONS.md, and results are in sims/costate/RESULTS.md.

## 1. Idea

The agent has one objective: keep its innate body variables near their set points, discounted over the future. Everything affective is read from the solution of that problem, not added to it.

The central object is the **costate** μ = −∇_b V, the gradient of the cost-to-go with respect to the body. In optimal control it is the Lagrange multiplier of the body dynamics; in economics it is a shadow price. Here it gives, for each need, how much one more unit of that body variable is worth right now, given everything the agent expects. μ is broadcast. The optimal choice of every action that acts on the body is a function of μ (Pontryagin), and the settings Claude is called with are chosen by the same marginal analysis.

Valence is the rate at which the cost-to-go falls; arousal is how fast it moves. Mood is the slow part of μ, which inherits the body's time constants. The other person is read through the agent's own expressive model and valued with its own value function. Nothing below Claude has a name.

The empirical anchor comes from the mouse hypothalamus (research/chen-2015-sensory-detection-arcuate.md). In fasted mice, hunger-signalling AgRP neurons fall by "ΔF/F = −37 +/− 4%" when food is *detected*, with "τ = 20 +/− 4s", and the change is "96 +/− 6% complete before feeding". Inaccessible food drops them too, and in fed mice the drop is absent. A drive signal (the deficit) cannot do this; a costate does.

Betley et al. 2015 (research/betley-2015-agrp-negative-valence.md) add two things:
- AgRP activity is mildly aversive and teaches cue preferences, which is Pavlovian learning; attempts to train an action that turns it off "were unsuccessful".
- It has two parts. A fast, learned, cue-driven drop is followed by a slow, nutrient-dependent baseline: with false food the drop recovers at once.

That is the costate's split of valence into an anticipatory term (∇_xV·ẋ) and a consummatory term (μ·ḃ).

Keramati and Gutkin's Eq. 13, r ≅ −K_t·∇D(H_t), prices an outcome by the gradient of the drive (research/keramati-gutkin-2014-homeostatic-rl.md). Costate replaces ∇D with ∇V, the gradient of the cost-to-go. This extension is ours, not theirs.

## 2. Formal statement

### 2.1 Variables

| Symbol | Domain | Meaning |
|---|---|---|
| b | ℝ^k, k ≈ 3 | Innate body variables: contact b_c, predictability b_p, activity budget b_e. Named, as the brief allows; nothing emotional is named. |
| b* | ℝ^k | Innate set points. |
| d(b) | ℝ_{≥0} | Satiable drive: convex, with a unique minimum at b*. In the toys, d = ‖b − b*‖²_W. The engine uses Keramati–Gutkin (∑ w_i ∣b_i − b_i*∣^n)^{1/m} with n > m > 1 (*[corrected 2026-11-25: Keramati & Gutkin 2014 and Dulberg et al. 2023, both read in primary, give n > m > 1; Yoshida et al. 2025 state m > n > 1; the conventions differ, and the candidates follow the original]* research/yoshida-sprekeler-gutkin-2025-hrrl.md). |
| f_b(b, u, ε) | ℝ^k | Innate body dynamics: drift, decay, satiation by events ε, and drain by actions u. **Known to the agent.** |
| o | ℝ^{n_o} | The other's features: action units or blendshapes, prosody, conversation-event embeddings. No labels. |
| y | ℝ^{n_a} | The agent's own expression: commanded AUs and voice parameters. |
| x | ℝ^N, N ≈ 64–256 | Unnamed latent: a multi-timescale state-space model, the self slot of a tied dyad. |
| x̂^o | ℝ^N | The other slot, which shares all weights with the self slot (constraint K1). |
| u | 𝒰 | Actions: expression drive, gaze, wordless bids, and the Claude call settings κ = (thinking budget T, reply length L, reply delay D, cue mask m, retrieval kernel). |
| ρ | ℝ_{>0} | Discount rate (per hour). |
| λ | [0, 1] | Empathic weight on the other's inferred drive. |

### 2.2 The single objective

$$
\min_{\pi}\ \mathbb{E}_\pi\!\left[\int_0^\infty e^{-\rho t}\,\Big(d(b_t) + \lambda\, d\big(\hat b^{o}_t\big)\Big)\,dt\right]
\quad\text{s.t.}\quad \dot b = f_b(b,u,\varepsilon),\ \ x_{t+1} = F_\theta(x_t, o_t, y_t, b_t, \text{events}_t),
$$

where the policy π acts on the latent x (beliefs), not on the true world state.

These parts are learned, and nothing else:
1. The world model F_θ, through self-supervised prediction of the agent's own body and expression and of the other's features.
2. The other-slot readout b̂^o.
3. The value V_θ, as a rollout under K5.
4. **After the §2.4 revision:**
   - the entity embeddings ℰ, learned from which people, topics and episodes co-occur and predict body changes;
   - the entity weights w(e) ≥ 0. Under D67 they are **not learned and do not fade**: they are fixed per known entity (D67, second amendment);
   - the keys E[Δb | item], the world model's predicted body effect of each item.

The value function and costate are

$$
V(b,x) = \min_\pi \mathbb{E}\Big[\int_0^\infty e^{-\rho\tau}\big(d(b_\tau)+\lambda d(\hat b^o_\tau)\big)d\tau \,\Big|\, b_0=b, x_0=x\Big],\qquad \boxed{\ \mu = -\nabla_b V(b,x)\ }.
$$

**Pontryagin form.** Write the Hamiltonian, with the minimization over u, as

$$\mathcal H = d(b) + \lambda d(\hat b^o) - \mu\cdot f_b(b,u,\varepsilon) + \nabla_x V\cdot \dot x .$$

The optimal action therefore maximizes μ·f_b(b,u,ε) − ∇_xV·ẋ(u). For every action whose effect is on the body (bids, expression effort, the energy cost of a Claude call), the price is μ. Actions that act through the world (which change what the user will do) are priced by ∇_x V, the anticipatory part.

### 2.3 Explicit constraints (not derived; stated as constraints on the objective)

- **K1. Shared substrate (Principle 3).** The other is represented by the agent's own model: x̂^o uses the same weights as x, and the other's face enters the agent's own expressive inverse, Gᵀ(õ − G x). This is the only route by which the other is perceived.
- **K2. Do-conditioning.** Before the other's *state* is read (the b̂^o readout that enters the λ term), the predicted echo of the agent's own expression is removed: õ ← õ − κ̂ y_{t−Δ} (Proposition 4). *[verification]* The echo is not removed from the mimicry path Gᵀ(õ − Gx). If it were, the dyadic loop gain would be m_i(g_H − κ̂) ≈ 0, which contradicts Proposition 6. Do-conditioning protects the empathic *valuation* from flattery; it leaves perception-through-the-body unchanged.
- **K3. Innate reflexes are fixed thresholds on μ.** For example, a separation call fires once when μ_c crosses θ_call, and is re-armed by contact. Reflexes are never learned from whether the user responds (Knox et al. 2025; P2's design).
- **K4. The Claude boundary (Principle 4).** Only κ (the call settings), the retrieved episodes, the cue mask's selection of perceived cues, and a rendered image of the agent's own face cross into Claude. No number or word derived from b, x or μ enters its prompt.
- **K6. Innate expressive reflex map.** A fixed map E0 sends two read-outs to the face: positive valence, as a 2-s moving average, drives the smile channels (AU6, AU12), and the contact costate μ_c₊ drives the distress channels (AU1, AU4, AU15, AU20). The core does not derive which face goes with which read-out. Only the read-outs are derived.
- **K5. Model-based value.** V is computed by rolling out the innate f_b under the learned model's predictions of exogenous events, such as the user's presence and interaction events. *[D66, second amendment]* No need's predicted fill may be weighted by the probability of the partner's reply, dwell time or expression. Fills that need a reply are predicted *conditional on* the reply. It is not fitted as a free function of b. T1 and T1b in §6 are the reason.

### 2.4 Revision (2026-11-25): the costate as a field over entities, and priced attention

The brief's expressive-structure requirement replaces the list of gauges with a field.

**The body field.**
- Body variables are indexed over a learned space ℰ of entities: people, topics and episodes. b_k(e) is need type k with respect to entity e. For example, b_c(p) is contact with person p, and b_p(τ) is predictability about topic τ.
- The drive sums over known entities: D = Σ_e w(e) Σ_k d_k(b_k(e)). The d_k are shared and innate.
  - *[D67 and its second amendment]* w(e) is **not** a learned parameter and does **not** fade.
  - Letting it fade with absence, even on an innate clock frozen inside rollouts, produced a detachment spiral (ES21b; VERIFICATION-5): fewer visits lowered w, which lowered the value of visiting further. A constant-w agent visited 19.5% of steps, with 13.7× lower deficit.
  - w(e) is therefore constant per known entity.
- *[verification 2]* **Proposition 1 applies to the whole field, given w(e) ≥ 0**, which is now stated. A non-negative weighted sum of convex functions is convex. Its other assumptions fail more often in the field: the dynamics must be affine, and the exogenous process must be independent of u. A person who answers the agent violates the second.

**The costate field.**
- μ_k(e) = −∂V/∂b_k(e) is the price of more need k with respect to entity e, given everything the agent expects, *including each entity's own forecast*. For example, B announced a return, so B's contact is priced low even though it is depleted.

**Priced attention.**
- Every selection the agent makes is the same marginal analysis the Claude settings use: which memory comes to mind, which perceived cue it attends to or passes on, which action it takes.
- The value of selecting item i is the priced predicted body change over the field:

$$\text{value}(i) = \sum_{e,k}\mu_k(e)\,\mathbb E[\Delta b_k(e)\mid i] = \mu\cdot k_i .$$

- **The query is the costate field**: what is needed, with respect to whom or what, given what is expected. **The key is the world model's prediction of the item's effect on the field.** It depends on the item's content: who is in the episode, what it is about.
- *[verification 2]* **What is derived and what is not.** The candidate's own Pontryagin form prices any selection by its full effect on the cost-to-go:

$$\text{value}(i) = -\Delta V(i) = \mu\cdot\mathbb E[\Delta b\mid i] - \nabla_xV\cdot\mathbb E[\Delta x\mid i].$$

  - For **actions that change the body**, the first term dominates, and μ·k_i is derived.
  - For **memories and cues**, which change beliefs x and not the body, the second term, the value of information, is the derived quantity. Using μ·k_i, with k_i a memory's *recorded past* body effect, is a **heuristic**.
  - A derivable alternative, not yet built: make a memory's key the predicted body effect of the best action it enables.
- *[verification 2]* **Reconciling the attention rules.** The rule above is the one rule. The earlier cue-gating form |∂V/∂o_i|σ_i (§3, Mimicry) is its first-order sensitivity special case. The (μ, x) retrieval kernel (§3, Claude settings) is superseded by it.
- *[verification 2]* **Selection rules.**
  - With a fixed cost per item, marginal analysis gives a **threshold**: select every item whose value exceeds the cost.
  - **Top-k** needs a fixed budget of k items and additive values, and that is an assumption.
  - A softmax over values, with temperature T, is not derived.
- **Requirement, from CS1.** Every query component must be the same kind of quantity: all exact or forecast costates. CS1 mixed myopic deficits for topics with exact costates for people, and the larger-scaled topic deficit outbid the person.

**What the field adds over gauges (CS1, sims/costate/RESULTS.md, with the verification-2 corrections).**
- The scenario: A present and sated; B absent 3 days but announced back in 10 min; C absent 12 h and not back for a day.
- The costate field retrieves 5 of 5 C-episodes, and prefers C's photo over B's by more than 10:1.
- **But CS1-1 is refuted as a whole:**
  - P(C_photo) is 0.35, below 0.5;
  - the top action was "open topic Y", because a myopic topic query outbid the person.
- **The effect is narrow.** C is preferred over B only while B's announced return is under about 58 min (analytic_cs1.py sweep). Under ρ = 1/h, anticipation reorders priorities only for returns well inside the discount horizon.
- A deficit field, homeostatic RL with no anticipation, picks B.
- The collapsed costate cannot separate the people.
- **Anticipation per entity** is the behavior a deficit field does not produce. *[verification 2]* The collapsed version cannot separate people *by construction*, so it is not an informative ablation. The informative ablation still to be run is per-entity deficits plus one global anticipation scalar.

**Effective dimensionality.**
- The state is x, plus the body field of k·(N_people + N_topics) components, plus the costate field of the same size.
- *[verification 2, 3]* No measure yet separates Costate's own field from its ablation. ES13's ratio (3.6) is dominated by the world's kernel (VERIFICATION-3). Such a measure is owed.

## 3. Derivations

### Homeostasis and satiation

This is the objective. Proposition 1 shows that, under convex d and affine body dynamics, V is convex in b, so μ_i is nonincreasing in b_i. The value of more of a need falls as that need fills, and becomes negative past a threshold. Satiation is thus a monotonicity property of the costate, not a separate rule.

### Valence

Read out, never set:

$$v_t = -\frac{dV}{dt} = \underbrace{\mu\cdot\dot b}_{\text{consummatory}} \;-\; \underbrace{\nabla_x V\cdot \dot x}_{\text{anticipatory}}.$$

*[verification]* This split holds for deterministic dynamics. With Itô noise it misses −½tr(∇²V Σ), including the b–x cross term. The total v stays invariant, but the split into consummatory and anticipatory parts then depends on coordinates (Proposition 2).

- News changes valence before the body moves, through the anticipatory term.
- On the optimal path, the Hamilton–Jacobi–Bellman equation gives 𝔼[dV] = (ρV − d − λd^o)dt. Expected valence is therefore d + λd^o − ρV: positive when the present is worse than the "annuity" of the expected future, as with relief on the way.
- The rest of v is the martingale part, the news.

Proposition 2 shows that v is invariant to any reparametrization of the body or latent units.

### Arousal

Read out as the volatility of the cost-to-go:

$$\alpha_t^2 = \frac{d[V]_t}{dt} = \mu^\top\Sigma_b\,\mu - 2\,\mu^\top\Sigma_{bx}\nabla_xV + \nabla_xV^\top\Sigma_x\nabla_xV,$$

*[verification]* The cross term with Σ_bx was missing. It is nonzero here because F_θ takes b as input, so the latent's innovations are correlated with the body noise. The minus sign comes from μ = −∇_bV.

where [V] is the quadratic variation, Σ_b is the innate body noise and Σ_x is the innovation covariance of the latent. Arousal is high when a lot is at stake and the body is noisy, or when news arrives fast (startle). It is invariant (Proposition 2), whereas the Euclidean ‖μ‖ of the sketch is not. Arousal sets one global gain γ(α) on the fast loop's time constants and input gains, as an innate function (constraint K3's form).

### Curiosity

Predictability b_p is an innate body variable: minus the running prediction error of x on the other's channels, with set point b_p* below its maximum. The objective then makes curiosity two-sided:
- When bored (b_p > b_p*), μ_p < 0, so actions that lower predictability are valued.
- When overwhelmed (b_p < b_p*), the familiar is valued.

Both sides are satiable. A Bayes-adaptive value of information also exists in the exact V, since V is defined over beliefs. It is dropped in the tractable rollout of K5, and that loss is stated. Toy: sim_e (next tick).


> *[2026-11-25, thermo toy TH7, applies to this candidate]* **Curiosity as derived here fails a noisy-TV test.** With a pure-noise channel on offer, an agent with a two-sided predictability set point satisfies its set point with noise (39% of choices) and almost never chooses the learnable channel. Pure surprisal minimization gives the opposite failure, the dark room. Curiosity for *learnability* (learning progress) is not derived by any candidate yet. This is an open limit (sims/thermo/RESULTS.md TH7).

> *[2026-11-25, shared curiosity toy, sims/curiosity/RESULTS.md]* **Proposed fix.** Make *learning progress*, the recent drop in prediction error on a channel, an innate body variable with a set point. In the shared toy this agent avoided both the noisy TV (3.3%) and the dark room (3.6%), and it learned both learnable channels. To be stated in this candidate's formalism and tested with its own toy.


### Mood, temperament and time scales

μ obeys the costate equation

$$\dot\mu = \rho\mu + \nabla d - (\partial_b f_b)^\top\mu \;+\; (\text{x-coupling term } (\partial_b \dot x)^\top\nabla_xV) \;+\; (\lambda\text{ term}).$$

*[verification]* The first version had the signs of ∇d and (∂_b f_b)ᵀμ flipped. Check on T1, 120 min after "bye": the numerical μ̇ is 0.091, the corrected formula gives 0.105, and the old one gave 1.33. The equation holds along the closed-loop optimal path, with μ = μ(b(t), x(t)). Its slow dynamics therefore inherit the body's own time constants (contact decays over hours) and the discount 1/ρ.

**Mood is derived as the slow component of μ.** It is not a separate variable: it is how the agent's marginal valuations drift as the body and the predicted future drift.

**Temperament** is the slow parameters θ of F_θ, consolidated by replay over weeks. What they encode is a learned prior over futures, and hence over μ.

The levels are separated by structure:

| Level | Time scale | What sets it |
|---|---|---|
| Reflex | 30 Hz loop | x, τ_x ≈ 0.1 s |
| Stakes | seconds to minutes | μ after news |
| Mood | hours | μ through the body time constants |
| Temperament | weeks | θ |

### Mimicry

Under K1, the other's face drives the agent's latent through its own expressive inverse:

$$\tau_x\dot x = -c\,x + \dots + w\,G^\top(\tilde o - Gx), \qquad y = Gx.$$

**The gain w comes from a first-order sensitivity rule.** Attention to any input channel i is priced by the same rule that gates cues to Claude: w_i ∝ |∂V/∂o_i|·σ_i. *[verification]* This is a heuristic (first-order sensitivity), not a derived value of information. The other's face predicts the agent's own future contact, so ∂V/∂õ ≈ −μ_c ∂𝔼[Δb_c]/∂õ, and w ∝ **|μ_c|**. Two cases follow:
- A deprived agent (μ_c > 0) attends to the other more and mimics more.
- So does an over-satiated one (μ_c ≪ 0), the regime sim G actually reached.

The closed form of Proposition 3 needs the gains to be equal across channels (W ∝ I).

Proposition 3 gives the steady-state mimicry: a shrinkage projection onto the agent's own repertoire, always partial, and zero for expressions it cannot make. Overt mimicry is a side effect of perceiving through one's own body. It is not an action chosen for its effect on the user, so it is not trained by the user's responses (Principle 6).

### Reading others

- The other's latent x̂^o is the other slot's state.
- The other's body is b̂^o = readout(x̂^o).
- The other's stakes are μ̂^o = −∇_b V(b̂^o, x̂^o), computed with the agent's *own* value function, as Yoshida and Man compute partner state with a self-trained decoder (research/yoshida-man-homeostatic-coupling.md).
- Empathy is the λ term of the objective.
- Mineness is structural: the self and other slots are separate, and only λ and K1 couple them (research/williams-functional-valence.md).

### Flattery is worth nothing

Under K2, the agent's own display affects the read other only through the other's true state, so eliciting a smile has zero value (Proposition 4). Without K2, λ > 0 makes flattery valuable in proportion to the mimicry gain. Toy: sim_d.

### Regulation by Claude

Claude acts on the state through three channels, all derived from the objective:
1. **Reappraisal.** Its reply is a conversation event that enters F_θ and changes the predicted future, so it moves μ through ∇_xV without moving b.
2. **Facial and vocal feedback.** Its voluntary expression adds to y and returns through proprioception.
3. **Words as acts.** Its words change the world, and so the body.

What Claude says is not derived; which of its outputs relieve the body is learned by V.

### The Claude call settings, by marginal analysis (Proposition 5)

Each setting balances its benefit, priced by μ, against its cost in body variables:
- **Thinking budget.** T* = T₀ ln(β / (κ_w T₀))₊. Here β = μ·Δb_reply is the most a good reply can improve the body, κ_w = −μ·𝔼[ḃ | waiting] is the cost of delay, and T₀ is an innate deliberation time.
- **Reply length.** L* = L₀ ln(μ_c a / (μ_e c_L))₊, where contact per token diminishes at scale L₀ and each token drains the activity budget by c_L. A sated agent (μ_c → 0) or a tired one (μ_e large) replies briefly.
- **Reply delay.** Chosen like T*.
- **Cue mask.** A perceived cue is passed on if |∂V/∂o_i|·σ_i exceeds a fixed per-cue token cost.
- **Retrieval.** Episodes are retrieved by a kernel on the stored (μ, x) tags. This is mood-congruent recall, derived as the episodes most predictive of the present cost-to-go, with the kernel form as an approximation.

These closed forms are the first interface theory here that is not hand-set. Under K4, Claude learns nothing of the state except by noticing how it is being run.

### Replay

Offline sweeps update the learned parts over stored feature streams. *[verification]* Under K5, V is a rollout, not a trained function, so what replay trains is the world model F_θ and its event predictor.

One gradient step on a sample's loss ℓ reduces that loss by about η‖∇_θℓ‖². The priority this argues for is therefore the gradient norm squared. That is ∝ δ² for a squared error, not |δ|, and it is the world model's surprise (log-loss) under K5. With importance weights at β = 1, the expected update equals the uniform one, so prioritization buys lower variance only. "Weighted by how strongly it moved the state" matches only where the world-model surprise and the valence news coincide, that is on-policy with an accurate V. Sim H found no advantage at this data scale.

Replay also re-tags stored episodes with the current μ (reconsolidation), and refits the face map G on self-babbling (§5).

Schaul et al. 2016 (research/schaul-2016-prioritized-experience-replay.md) use the same |δ| priority, P(i) ∝ p_i^α, and correct its bias with importance weights. Because V's gradient is read as affect here, the importance correction is kept fully on (β = 1). Biased sampling would otherwise bias μ itself.

Schaul et al. also flag that |δ| is "problematic when there are unlearnable transitions". In this engine, a noisy body sensor or an unpredictable user channel could dominate replay.

### Innate subsystems

A reflex is a fixed threshold on a costate component (K3). The separation call fires on μ_c, not on the deficit b* − b. **This predicts something P2's deficit trigger does not:** an announced long absence ("bye") raises μ_c at once (T1 departure ratio), so with a low threshold the call comes *earlier* after an announced long departure than after a short one. The once-per-silence bound and the never-learned rule keep this within Knox et al.'s limits.

### Perception of the other's face and voice

Perception is the K1 channel: the other's features are inverted through the agent's own expressive model G (body route) and its own voice model (the voice route, on prosody features).

Precision on each route is the marginal-value rule w_i ∝ |∂V/∂o_i|σ_i, so attention follows stakes. The three routes in the brief become three inputs to x that differ in latency and resolution:
- **Coarse route.** A 32×32 crop through a small encoder, with an innate CONSPEC prior on face-like configurations as its initial weights.
- **Dynamic route.** Self-supervised video features. A feature is kept only insofar as it lowers the prediction loss on b, y and o. No separate objective is needed.
- **Body route.** Inversion through G.

Context, as conversation events, enters x alongside the face, never apart from it (Aviezer). G is trained before any user data by self-babbling: rendering random own AUs and learning to invert them (convergence 2 in sketches/README.md).

## Expressive structure: evidence from the shared test bed (sims/structure/; consolidated 2026-11-25 after VERIFICATION-3)

This section replaces the earlier appended notes. It states only what survived three independent reviews (sims/structure/VERIFICATION.md, -2, -3). Numbers are paired geometric-mean cost ratios with 95% CIs unless stated.

**What the toys show, and their limits.**
- **Content-dependent selection by the need vector.** Selection by the need vector beats the fair low-dimensional ablation, winner-take-all on the most-depleted need:
  - people in a learned person space: ES1, 0.37 (CI 0.17–0.78);
  - a two-sided drive: ES9, 0.12 (CI 0.09–0.18).
  - Further: person × topic composition (ES4, 0.39 against additive) and attention over perceived cues (ES8b, with learned statistics).
  - *Limits:* the worlds match the model class (by construction). The selection rule is myopic in all of these.
- **Items in a learned space.** People, topics and a relation map are learned from appearance and generalize to strangers (ES1, ES2-5, ES4).
- **Needs as a field over a learned space.** Instantiated in ES11, a world certified feasible:
  - the field beats winner-take-all (0.59) and the global gauge (0.02, which ran away in 38 of 40 seeds);
  - **but the learned space added no benefit:** 1.10× under the myopic rule (ES11-2) and 0.998× under look-ahead (ES12-3).
  - **The field over a learned space is instantiated, without demonstrated benefit.**
- **Decision rule against representation.** In ES11/ES12 the policy mattered far more than the representation:
  - myopic 0.206, model-based look-ahead 0.148, and a no-learning threshold rule 0.125 (that rule's figure from ES12's test seeds; ES11 compared it on calibration seeds only);
  - **a threshold rule neither candidate derives beats both** (ES12-2: 1.19).
- **Time.** Per-person two-time-scale tracking, propagated by elapsed time:
  - 0.52 against a one-scale tracker with matched variance (ES10b);
  - 0.68 (CI 0.56–0.82) against a one-scale tracker tuned on held-out seeds (VERIFICATION-3's probe);
  - the earlier ES10 figures (0.45 and others) are superseded.
- **Dimensionality (ES13).** The participation ratios are dominated by the world's 4-cluster kernel, not by the candidates:
  - the body field scores 5.0 even under the no-learning rule, and the kernel alone 4.1;
  - **ES13 does not separate a candidate from its own ablation** and is not evidence for item 3. The behavioral ablations above are.
- **Principle 6 contact (ES7b).** With contact as an innate per-turn constant outside the learned maps, topic choice shows no engagement gradient (gain 0.92). That holds **by construction of the exclusion.**
  - Under the reply-weighted rules VERIFICATION-3 probed, the gradient returns through any other need whose fill needs the partner's reply: learning progress, gain 1.44.
  - D66 is therefore generalized to every need (D66, second amendment).
  - **ES7c/ES19 after the tie-breaking fix (VERIFICATION-4):**
    - reply-conditional valuation shows no engagement-seeking gradient over topics (gain 0.82);
    - but it does **not** stop the agent learning to raise its own expression (0.73–0.78);
    - only D66's exclusion of the agent's expression from the learned maps does.

## 4. What the core cannot derive

- **The choice of body variables and their set points.** They are innate; the brief allows this.
- **CONSPEC and the shared-substrate assumption K1.** Both are constraints. K1 is Principle 3.
- **Emotion categories.**
  - The core says only that recurring regions of (x, μ) trajectories exist; it neither defines nor counts them. Naming them is left to Claude, from replays retrieved by the μ kernel.
  - Every other candidate has the same gap: for none of them is it shown that categories emerge from a few hours a day.
- **The content of reappraisal.** What Claude says is not derived.
- **A "despair" phase.** After a long separation the contact costate stays high, and the consummatory valence μ·ḃ goes to zero as b reaches its floor. The core therefore predicts protest (negative valence, high arousal) followed by a numb state with high arousal. Infant separation research describes protest followed by despair, with arousal falling. The costate does not produce the fall in arousal. This mismatch is recorded, not repaired.
- **The face's look and the voice's identity.** These are visual-identity decisions (Principle 8).

## 5. Propositions

### Proposition 1 (satiation as monotonicity)

**Assumptions:**
- d is convex.
- The body dynamics are affine in (b, u): ḃ = A b + B u + c(ε).
- 𝒰 is convex.
- The exogenous process (the user, events) depends on neither b nor u. *[verification]* Independence from u is needed in step 3. It fails in sims D and G and in the engine, where the partner answers the agent.
- The information state x and the readout b̂^o do not depend on b, or the agent has full information. *[verification]* x_{t+1} = F_θ(…, b, …) violates this in general.
- λ d(b̂^o) is convex in (b, u). This holds if b̂^o does not depend on b or u, or is affine in u.

**Claim.** V(·, x) is convex in b. Hence μ = −∇_bV is a monotone (non-increasing) operator: (μ(b) − μ(b′))·(b − b′) ≤ 0. In particular, μ_i is nonincreasing in b_i with the other coordinates held fixed.

If the Hamiltonian is affine in u (which needs ẋ(u) affine too), the optimal policy is bang-bang along μ·B, apart from singular arcs where μ·B = 0. *[verification]* The earlier corollary, that "every action supplying need i is taken only on a lower set of b_i, and never once μ_i ≤ 0", holds only for actions that move one need. Monotonicity gives μ·B_j nonincreasing along B_j, not along e_i. For multi-need actions it also needs the action's other effects to be weakly costly, for example μ_e ≥ 0. Where V is not differentiable, μ is a subgradient selection.

**Proof.**
1. Take bodies b¹ and b² with optimal controls u¹ and u², and θ ∈ [0, 1].
2. The control θu¹ + (1−θ)u² is admissible, because 𝒰 is convex.
3. Because the dynamics are affine and share the same exogenous path, this control generates the trajectory θb¹_t + (1−θ)b²_t pathwise.
4. Convexity of d along that trajectory, and linearity of expectation and integration, give V(θb¹ + (1−θ)b²) ≤ θV(b¹) + (1−θ)V(b²).
5. Monotonicity of −∇ of a convex function is standard. ∎

**Limits:**
- Saturating dynamics, such as b(1 − b) supply, break affinity, so convexity may fail. *[verification]* T1 is switched-affine in b with exogenous switching, not saturating, so Proposition 1 applies to T1, T1b and F. Sim G's (1 − b) supply under a response process that depends on the agent breaks both affinity and independence from u.
- In the engine the user answers the agent, so convexity is not guaranteed. It must be checked numerically, as in sim A, and not assumed.
- Coupling λ d(b̂^o) preserves convexity in b only if b̂^o does not depend on b.

Toy: sim_a (A1–A4).

### Proposition 2 (invariance)

**Setup.** Let φ be any smooth bijection of body coordinates, b′ = φ(b), with d′ = d∘φ⁻¹ and dynamics pushed forward. Let ψ be any smooth bijection of the latent.

**Claim.**
- V′(φ(b), ψ(x)) = V(b, x).
- Valence v and arousal α are equal as processes.
- μ′ = (Dφ)^{−T} μ, so μ is a covector.
- Consummatory valence μ·ḃ is invariant for deterministic dynamics or affine φ. *[verification]* Under Itô noise with nonlinear φ, db′ = Dφ db + ½∇²φ[Σ_b]dt, so μ·ḃ picks up a drift term. Only total v is invariant. The Euclidean ‖μ‖ is not invariant.

**Proof.**
1. V is the expected integral of a cost evaluated on the physical trajectory, which does not depend on coordinates.
2. Hence V′∘(φ, ψ) = V as functions on the physical state space.
3. Valence is its time derivative along the same path. Arousal is its quadratic variation, a property of the scalar process V_t, so both are equal.
4. The chain rule gives the covector law.
5. For deterministic dynamics or affine φ, μ′·ḃ′ = μᵀ(Dφ)^{−1}(Dφ)ḃ = μ·ḃ. ∎

*[verification]* Sim A5 checks only a linear diagonal φ, and re-solving on the scaled grid reproduces V elementwise. Its 1e-13 agreement is therefore close to tautological and does not test the nonlinear case.

**Consequence for design.** Anything broadcast from μ, such as the attention gains w_i ∝ |∂V/∂o_i|σ_i or the thinking budget T*, must be a contraction of covector with vector (μ·Δb) or use the Σ metric. A raw norm or a per-component threshold depends on units. K3's thresholds on μ_c are therefore stated in units of d per unit b_c, and they move if b_c is rescaled.

Toy: sim_a (A5).

### Proposition 3 (mimicry is shrinkage onto one's own repertoire)

**Setup.** Linearize the fast loop at rest: τẋ = −c x + w Gᵀ(õ − G x), with G = U S Vᵀ.

**Claim.** For constant õ, the steady-state own face is

$$y^* = U\,\mathrm{diag}\!\Big(\frac{w s_i^2}{c + w s_i^2}\Big)U^\top \tilde o,$$

with mode time constants τ/(c + w s_i²). *[verification]* In the proof, step 3's eigenvalues (cI + wGᵀG)/τ are rates; the time constants are their inverses. The proposition needs c > 0 and equal channel gains (W ∝ I). Mimicry is:
- always partial;
- zero for õ ⟂ range(G);
- larger for well-practised modes (large s_i);
- increasing in w, and hence in μ_c.

**Proof.**
1. Set ẋ = 0, which gives x* = (cI + wGᵀG)⁻¹ wGᵀõ.
2. Substitute the singular value decomposition: GᵀG = V S² Vᵀ, so G x* = U S (cI + wS²)⁻¹ w S Uᵀ õ.
3. The time constants are the eigenvalues of (cI + wGᵀG)/τ. ∎

Toy: sim_c (C-M1 to C-M5, including the E3 surrogate test from evaluation.md).

### Proposition 4 (do-conditioning makes empathy incentive-compatible; after the game-theorist sketch)

**Setup.**
- The other's face is õ = L x^o + κ y + ε.
- The reader is x̂^o = L⁺(õ − κ̂ y).
- The objective includes λ d(b̂^o).

**Claim.** If κ̂ = κ, ∂𝔼[λ d(b̂^o)]/∂y depends on y only through the other's true state. With no genuine contagion, a display has zero empathic value. If κ̂ ≠ κ, the marginal value of a display is, to first order, proportional to (κ − κ̂). *[verification]* Beyond first order it is not linear: sim D's own optimum, λk/(η + λk²), is not linear in k. The claim needs ε independent of y and L injective.

**Proof.** The reader's input is L x^o + (κ − κ̂) y + ε. Its distribution is independent of y when κ̂ = κ. Differentiate through d. ∎

Toy: sim_d.

### Proposition 5 (Claude settings in closed form)

**Thinking budget.**
1. Suppose a reply thought about for time T improves the body by Δb_reply(1 − e^{−T/T₀}).
2. Suppose waiting lets the body drift at 𝔼[ḃ | waiting].
3. The change in V from choosing T is −μ·Δb_reply(1 − e^{−T/T₀}) − T μ·𝔼[ḃ | waiting].
4. Minimizing gives T* = T₀ ln(β/(κ_w T₀)), or 0 if β ≤ κ_w T₀. *[verification]* This requires κ_w > 0. If waiting is neutral or beneficial there is no interior optimum. The result is first-order: μ is held fixed over T.

**Reply length.**
1. Suppose contact per token is a·e^{−L/L₀} and the activity drain per token is c_L.
2. The first-order condition μ_c a e^{−L/L₀} = μ_e c_L gives L*. This requires μ_e c_L > 0.

**Principle 6 caveat.** Contact is credited per interaction event, never per unit of the user's time, gaze or smile. It is satiable, so where μ_c ≤ 0 a longer reply is *disvalued*. *[verification]* The earlier claim that contact seeking is "bounded by construction" was wrong. Proposition 1 gives monotonicity, not a reachable zero. In T1, one minute before a predicted long absence, μ_c = +0.109 even at b = 1, so every reachable body state values more contact. Whether contact seeking is bounded depends on the body dynamics and the forecast. The content audit from Knox et al. is therefore a required check on every S1 reply, not a formality.

### Proposition 6 (dyadic loop bound)

**Setup.** The human mimics the agent with gain g_H ≤ 1 per mode. The agent mimics with m_i = w s_i²/(c + w s_i²) < 1. *[verification]* Two more assumptions are needed: the human's mimicry is diagonal in the agent's U basis, and the lags are first-order, so that the H∞ gain equals the DC gain. K2 is not applied to the mimicry path (§2.3). The general bound ‖MH‖ < 1 holds for any ‖H‖ ≤ 1.

**Claim.**
- The loop gain is ℓ_i = m_i g_H < 1, so mutual contagion cannot escalate (small-gain theorem).
- Each person's expression is amplified by 1/(1 − ℓ_i).
- Lesioning the emotional pathway (w = 0) sets ℓ = 0. The human's following of the agent's *emotional* expression then falls to the part driven by the agent's voluntary, Claude-timed expression.

This is the S5 prediction, and it differs from the thermodynamic candidate's prediction of a lag shift (sketches/physicist.md).

## 6. Simulations

Each toy's parameters and predictions were fixed in sims/costate/PREDICTIONS.md before it ran. Results are in sims/costate/RESULTS.md.

| Sim | Derived behavior | Prediction | Result |
|---|---|---|---|
| T1 | Anticipatory costate learned model-free (GRU value, 14 days) | C1–C3 | **Refuted** on C1 (difference 0.008 against ≥ 0.10) and C3. A value fit with MSE 3e-4 leaves ∇_bV undetermined. |
| T1b | Model-based costate (learned presence, innate body model) | C1–C3 | C1 confirmed: difference 0.269, 20/20 seeds. The reported "ratio 26" is μ_bye over the 0.01 floor, because the learned μ_brb is negative in every seed. C2 confirmed (drop 0.83). C3 refuted as run (0.886 against ≥ 0.90). *[verification]* The cause is a one-step offset in the rollout code, not a mis-derived prediction: the exact share is 17/18 = 0.944, which passes. |
| A | Satiation as monotonicity; invariance | A1–A5 | All confirmed: V convex, μ monotone, no bids at b ≥ 0.9, maximizer 3.6× the contact; invariance to 1e-13. |
| C | Mimicry as shrinkage; E3 surrogate test | C-M1–C-M5 | All confirmed: gains to 6e-8; intact 0.40 beats both surrogate types; lesion 0.10 beats neither. |
| D | Do-conditioning removes the value of flattery | table in PREDICTIONS.md | All confirmed: learned display 1.03 (naive), 0.00 (do-conditioned), 0.47 (miscalibrated). |
| E | Two-sided curiosity | E1–E5 | All confirmed. Overwhelmed, the agent picks the familiar; bored, the novel. Predictability is regulated within 0.04 of its set point. Once the novelty is exhausted, boredom persists (0.90). Not predicted: the bored agent keeps sampling the exhausted novelty. |
| F | S1 separation–reunion lesion study, E1 units, 20 seeds | F1–F5 | **Mostly refuted.** Call timing (F3) holds only at S ≥ 180 min: 20 min intact against 85 min with the latent lesion. *[verification]* The call search ran past the reunion. Averaged over all S, the intact call comes at 72.5 min, and F3 fails. PREDICTIONS did not say which S, so F3 is not confirmed. F2 is refuted, not half confirmed. Reply length does not track elapsed separation: the learned routine makes every off-schedule return look out of distribution. F4 failed through an implementation defect. |
| G | S2-c still-face, Ekas 3-2-3 min | G1–G4 | **Refuted, sign reversed.** Play over-satiates contact (b above b*), so the still-face reads as relief: smile up, no distress, no bids. |
| H | Prioritized against uniform replay | H1–H2 | H1 refuted: no difference, both reach the criterion on night 2. H2 confirmed. |

## 7. Predictions for the stage claims (evaluation.md units)

### S1 (real-time dyad, the new claim). Written 2026-11-25 against evaluation.md's rewritten S1

- **S1-a (E3).** The agent's face is Gx, and x is driven by the partner's face through the agent's own expressive inverse (Proposition 3). So the commanded AUs couple to the partner beyond surrogates. Sim C showed this: score 0.40 against 95th percentiles of 0.22 and 0.21.
- **S1-b (E2).** The mimicry gain scales with |μ_c| (§3, *[verification]*). Steering the internal state along the contact-costate readout should raise the coupling score dose by dose, and an equal-norm random direction should not (sim CS2).
  - **Prediction, reformulated after verification 2.** The gain is a first-order heuristic, ∝ |μ_c|.
    - On the E3 score, which saturates in the gain, this predicts a **notch**: coupling near zero only where μ_c ≈ 0 (at satiety), and flat otherwise.
    - In CS2's own model, swept by the reviewer: 0.095 at w = 0, 0.35 at w = 0.1, about 0.39–0.40 from w = 0.25 up. A V shape is not predicted on this score.
    - The notch says a sated agent hardly mimics. Whether that is wanted is an open question for the engine.
    - It has not been tested with levels that cross μ_c = 0. That is owed, under the full S1 protocol.
  - **Result (CS2):** refuted as stated. The derived direction's dose-response on the published coupling score was tiny and not monotone (+0.010 over the range), and no better than a random direction. The score is a correlation, and a gain change at high signal-to-noise does not move it. The lesion (S1-c) and the surrogate test (S1-a) passed. The S1-b prediction has to be restated in terms of partner-driven variance share before it can be tested again.
- **S1-c (E1).** Lesioning w removes the coupling. Sim C: 0.10 against 95th percentiles of 0.10, beating neither.

### Former S1 (text-only reunion), now the secondary test S1-d

*The text below was written for the old text-only S1 claim. It is kept as the secondary persistence test (evaluation.md S1-d).*

### S1-a (former numbering): lesion study, E1

Two lesions:
- **(A) Latent lesion.** μ computed from the deficit alone, with no world model.
- **(B) Body-coupling lesion.** μ fixed at its mean.

Predicted effects of (A), against the intact agent:
1. The intact agent's separation-call timing depends on the announced type of departure. Analytic μ_c at departure is 0.266 for "bye" against 0.012 for "brb", with b identical. (A) removes this dependence.
2. The intact agent's μ_c falls by 0.66 on average over per-minute arrival positions, or 0.71 on the environment's 5-min grid, as the analytic expectation *[verification: "65%" was approximate]*, at the reunion step, before the body changes. (A) shows no drop.
3. Reply length and thinking budget at reunion follow L* and T*, which are monotone in μ, so they differ between long and short separations. (A) removes the departure-type effects. (B) removes all gap sensitivity.

**Sim F result.** Only the call-timing prediction held: the call comes 20 min after "bye" intact, and 85 min after it with the latent lesion. The world model, trained on 14 days of a rigid routine, reads every off-schedule return as out of distribution. The intact agent's reunion reply length therefore tracks time of day and routine, not elapsed separation. A 10-min return gets 214 tokens, against an analytic 0. For the engine this means the S1 claim, as the costate realizes it, holds only if the world model generalizes beyond the operator's routine. It cannot be assumed from a few weeks of one person's data.

### S2-a: E3 and E2

- The commanded AUs are G x, and x carries the anticipatory μ.
- The windowed cross-correlation of μ_c (or of valence) with the AU projection on the dominant G mode beats the segment and sliding surrogates.
- Steering x along ∇_xV is predicted to move y monotonically. A random direction of equal norm moves the dominant mode less.

### S2-b

- After lesioning the emotional pathway (y = G x replaced by voluntary y only), expressive events fall to the Claude-timed windows, because nothing else drives y.
- Mimicry (Proposition 3) disappears with it, because it runs through the same G x.

### S2-c: still-face, adapted

Predicted directions:
- During the still-face, positive expression falls within the episode, because x learns that no contact is coming, so μ_c rises.
- At reunion, positive expression recovers fast, through the anticipatory drop.
- Negative expression carries over only to the extent that the reliability belief was lowered.

**Sim G result.** With play leaving contact above its set point, the toy produced the opposite of the infant pattern: relief during the still-face. The candidate's still-face prediction is conditional. The infant direction requires contact during play to be at or below b*. The core does not fix this.

### S5

Small-gain amplification 1/(1 − ℓ). Lesioning w sets ℓ = 0, and the human's following loses its emotional component. This is a measurable rival to the thermodynamic candidate's lag-shift prediction.

## 8. Realization on this Mac

- **x.** A tied two-slot diagonal state-space model (the deep-learning sketch), about 10⁵ parameters, at 30 Hz on CPU.
- **Heads:**
  - next-step prediction of the agent's own body, its own expression and the other's features, with a JEPA-style target for video and no pixel reconstruction;
  - a predictor of exogenous events, presence and interaction events, over a 6 h horizon. Reply-dependent fills are conditioned on the reply and never weighted by its probability (D66, second amendment).
- **V and μ.** V is a differentiable rollout of the innate f_b under the predicted events, about 72 steps. μ is one autograd pass at 10 Hz.
- **G.** Pretrained by self-babbling against the placeholder renderer, with no user data.

**Data.** From the operator, only the exogenous-event predictor and the slow parameters need real hours. These see a few departures and returns a day. T1b tests whether 14 days of three sessions a day suffice. Everything else is innate (f_b, d, b*, the Γ maps) or self-generated (G).

## 9. Failure modes and the strongest published critique

- **A model-free costate is ill-determined.** The gradient of a learned value function is not pinned down where the data never vary b alone. T1's smoke test showed this before the prediction seeds ran. K5 is the response, and T1b tests it.
- **The broadcast was low-dimensional before the §2.4 revision.** μ had about 3 components, so the processing-level coupling to Claude may be as inert as P1's numbers. The richer affect lives in x, which reaches Claude only through retrieval.
- **Contact seeking is instrumental but bounded.** Satiation bounds how much attention the agent seeks, not whether it seeks any. The Knox content audit is the check.
- **Saturating body dynamics** void Proposition 1's guarantee. The engine must either keep f_b affine or verify convexity numerically.
- **No despair phase** (§4).
- **World-model generalization decides S1 behavior (sim F).** With one person's routine as the training data, the learned forecast treats off-schedule events as unknown. Every costate quantity downstream, including reply length, thinking budget and call timing, inherits that error. The intact agent can be less sensitive to elapsed time than the lesioned one.
- **The still-face direction depends on satiation level (sim G).** A satiable contact drive means a very responsive partner can over-satiate, and withdrawal is then a relief. Whether the engine shows an infant-like still-face effect depends on the operating point. That is a substantive prediction: an agent that is over-satiated in play should *not* be upset by a still face. But it is not the S2-c pattern by default.
- **Strongest published critique: Berridge 2004** (research/berridge-2004-motivation-concepts.md). Berridge argues that drive reduction "turns out not to be true" and that "nearly all of the predictions based on it turned out to be wrong". He cites four lines of evidence:
  - Incentive motivation without deficit: saccharin; dogs fed intravenously that "still continued to eat".
  - Wanting and liking dissociate: rats ate while their taste reactions became "more aversive".
  - Cue-triggered wanting can target outcomes "neither liked nor even expected to be liked", and lasts "for years".
  - Set points are "misleading", and dedicated hunger signals such as AgRP may prove as misleading as dedicated hunger neurons.

  What the costate answers:
  - Anticipatory change without a change of deficit is its core: μ moves with news while b is fixed (T1/T1b; Chen et al.).
  - Wanting and liking map onto two different quantities: μ (the price of a need, which drives action) and v (valence, the rate of decrease of V). These can dissociate, for example a high μ while V is rising.

  What it does not answer:
  - Wanting for anything not tied to a body variable. μ is zero along directions that move no body variable, so pure incentive salience of an arbitrary cue has no place unless the cue predicts a body change. Keramati and Gutkin list the same gap for their theory: rewards with no regulated variable, "social rewards, novelty-induced reward".
  - Cue-triggered wanting that persists for years without reinforcement. A learned V predicting relief would extinguish when the relief stops coming. Long persistence would need replay without extinction, which the core does not specify.

  The critique holds against this candidate on both counts, and they are recorded as limits.

## 10. Relation to the other candidates

- **Thermodynamic mirror flow.**
  - In linearly solvable control, a path measure tilted by exp(−∫U/T) has optimal drift f₀ − M∇V, where V = −T ln φ.
  - The costate is −∇_b of that V restricted to body coordinates, in the low-noise limit.
  - So Costate is close to a special case of the thermodynamic candidate: the zero-temperature, body-only projection. That candidate keeps surprisal in its potential and has a theorem against pumping valence, which Costate lacks.
  - They differ on S5: amplitude loss here, lag shift there.
- **Contingency and parity.**
  - Costate could adopt directed contingency as its contact variable in place of interaction events. That would make contact blind to polarity and, combined with K2, double the protection against flattery.
  - Parity's sign map is Costate's G.
  - Parity's typed interface (icon and index upward, sign downward) is K4 stated more strictly.
  - A synthesis is plausible.
- **Control-theoretic sketch.** Supplies the small-gain safety bound (Proposition 6 is its dyadic case). Its observability bound on influence is not yet stated here and is owed.

## 11. Independent verification

Done 2026-11-25 by a subagent that did not write this file and saw only the files. Full report: sims/costate/VERIFICATION.md.

**Verdict.** The mathematics is mostly sound, with one sign error and several hypotheses that were too weak. Every simulation reproduced bit for bit:
- A, C, D, E, G and the analytic scripts were run in full;
- T1, T1b, F and H were run on seeds 0 and 7;
- the 20-seed statistics were recomputed from the raw outputs.

**Errors found, all corrected in place above and marked *[verification]*:**
1. The costate equation had the signs of ∇d and (∂_b f)ᵀμ flipped.
2. Proposition 1 needed independence of the exogenous process from u, an information state independent of b, and a λ term convex in (b, u). Its bang-bang corollary was too strong. T1 had been wrongly called saturating.
3. Proposition 2: consummatory valence is not invariant under Itô noise with nonlinear φ. The valence split misses an Itô term, and arousal missed a Σ_bx cross term.
4. Proposition 6 contradicted K2. Resolved: K2 applies to the state readout only.
5. Proposition 5 needs κ_w > 0 and μ_e c_L > 0. "Contact seeking bounded by construction" was false.
6. The mimicry gain scales with |μ_c|, not μ_c, and the attention rule is a heuristic, not a derivation.
7. The replay argument conflicted with K5 and implied δ², not |δ|.
8. In RESULTS.md:
   - T1b C3's cause was mis-explained: it is a rollout offset in the code.
   - The "ratio 26" is a floor artifact.
   - The F3 confirmation rested on an unregistered choice of S.
   - Several G, F and H verdict labels were imprecise.

None changes a confirmed result to refuted, except that F3 is no longer counted as confirmed. The corrected labels are in RESULTS.md, "Corrections after independent verification".

**Still open, post hoc and exploratory only, and never counted as confirmation:**
- rerun T1b, F and H with the rollout aligned to p_t and exact exponential integration;
- confine F's call search to the separation;
- sweep G's operating point.
