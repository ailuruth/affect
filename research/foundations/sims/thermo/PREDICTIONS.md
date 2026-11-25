# Thermodynamic mirror flow: toy simulations, parameters and predictions fixed before any run

Written 2026-11-25, before any of the scripts below was run. Results go to RESULTS.md as they come out. The analytic values here are derivations made before running.

## TH1. No affective perpetuum mobile, and where it breaks (sim_th1_perpetuum.py)

**Model:**
- Overdamped Langevin dynamics in 2-D: dz = [−∇U(z; o_t) + γ A z] dt + √(2T) dW.
- A is the 90° rotation, T = 0.5, dt = 0.01.
- U(z; o) = ½|z − o|² + 0.2 z₁² z₂², which is anharmonic.

**Readouts:**
- Valence v = −∂_t U|_z: minus the work rate done on the agent by the protocol.
- Mean valence per cycle = −⟨W⟩/τ, measured in the periodic steady state.
- Ensemble of 4,000 trajectories; 20 cycles of burn-in, then 40 cycles measured. τ = 10.

**Protocols:**
- 50 random periodic protocols: 3 Fourier harmonics per coordinate, amplitudes N(0, 0.5²).
- A "smile schedule": a square wave on o₁ between 0 and 1.
- Rotating protocols o = r(cos ωt, sin ωt) with ω = ±0.5 and r ∈ {1, 2}.

**Predictions:**
- **TH1a (conservative, γ = 0).** All 51 random and smile-schedule protocols have mean valence ≤ 2 standard errors above 0. This is the second law for periodic driving: ⟨W⟩ ≥ 0 over a cycle.
- **TH1b (internal rhythm, γ = 1).** For the harmonic part, the analytic mean work rate is W/τ = ω r²(ω − γ)/(1 + (ω − γ)²). The anharmonic term perturbs this, so the tolerance is ±25%.
  - At ω = +0.5 (co-rotating, slower than the rhythm), mean valence is about +0.2 r²: +0.20 at r = 1 and +0.80 at r = 2. The sign must be positive, beyond 3 standard errors.
  - At ω = −0.5, it is about −0.23 r², negative.
- **TH1c.** The positive valence at ω = +0.5 grows with r², from r = 1 to r = 2, by a factor within [3, 5].

  This would falsify the sketch's caveat that the leftover bound is "independent of the user": the pumped valence would depend on the protocol's amplitude.

## TH2. Reading by synchronization, and the separate lesion of mimicry (sim_th2_sync.py)

The numbers below are the dynamical-systems sketch's own, as fixed in that sketch.

**Model:**
- x = (a ∈ ℝ⁴, b ∈ ℝ², h ∈ ℝ¹⁰).
- T ẋ = −(K + J)∇V(x) + κ P(x̂ − x) + noise, with T = diag(0.05 s for a, 30 s for b, 1 s for h).
- K = I, and J is random skew-symmetric with norm 0.5.
- V(x) = ½xᵀQx + Σ_{j=1}^{3} −1.5 exp(−|h − m_j|²/2) + 0.1|x|⁴/(1 + |x|²). Q is a random positive-definite coupling matrix with all blocks nonzero and eigenvalues in [0.5, 2].
- Noise σ = 0.3 per √s on every coordinate.
- Agent A runs its flow. Agent B runs its own flow plus the copy x̂, with T ẋ̂ = −(K+J)∇V(x̂) + L(y − C x̂). Here y = a_A + N(0, 0.05²), C picks a, and P picks a.
- L = 10, κ = 3. 10 simulated minutes, dt = 1 ms, scored at 10 Hz. 10 seeds.

**Predictions:**
- **TH2a.** Same θ: R²(b̂, b_A) ≥ 0.8. A's V redrawn: R² ≤ 0.3.
- **TH2b.** At κ = 0, reading R² changes by < 0.02. The correlation of B's a with A's a falls from ≥ 0.5 at κ = 3 to ≤ 0.1.
- **TH2c.** B's face lags A's by 0.25 to 0.45 s at the cross-correlation peak (the sketch's estimate 1/L + 1/κ).

## TH3. Which lesion removes the human's following (S5; sim_th3_s5.py)

**Model:**
- Two 1-D faces. a_A is the agent, a_H is a simulated human.
- ȧ_i = −k₀ a_i − κ_i (a_i − a_j) + u_i(t) + √(2D) ξ_i, with k₀ = 2/s, κ = 1/s, D = 1.
- The agent's emotional drive is its noise term plus its mimicry κ_A. The agent's voluntary expressions u_A are pulses of height 3 and length 0.5 s at Poisson rate 0.1/s.
- 10 min per run at 10 Hz; 10 seeds.

**Arms:**
1. Intact.
2. Agent mimicry lesioned (κ_A = 0; the sketch's lesion).
3. Emotional pathway lesioned. The agent's face is driven only by u_A: no noise drive, no mimicry, and the same k₀ relaxation.

**Analytic predictions** (stationary Lyapunov equation, no pulses):
- Intact: zero-lag ρ = κ/(k₀ + κ) = 0.333.
- Arm 2: zero-lag ρ = 0.234, with a peak of 0.270 at a lag of 2 ln 1.2/k₀ = 0.18 s, agent leading.

**Predictions:**
- **TH3a.** These analytic values hold within ±0.03, from runs without pulses.
- **TH3b (E3 in evaluation.md).** The human's following, scored as Moulder's global mean |Fisher z| (30 s windows, ±5 s lags, 5 s steps, 0.1 s lag steps) against 1,000 segment-shuffle and 1,000 data-sliding surrogates, **beats both surrogate sets in all three arms**, pulses included.

  Under this candidate, removing the emotional pathway does not remove the human's following. It removes following of state-driven expression, and the human still follows voluntary expressions. The S5 claim as worded ("removes that following") is therefore predicted false.

## TH4. Valence as work, not total change (sim_th4_work.py)

**Model:**
- 1-D body b with innate decay: db = −0.5(b − 0) dt + noise σ = 0.05.
- Potential U = ½(b − 0.8)² + U_ext(t), where the user's presence enters as a supply term in the protocol: U_ext = −s(t)·b with s = 1 while the user is present.
- The tilt pulls b toward the set point. The fast-sector gradient flow is db = [−0.5 b − (b − 0.8) + s(t)] dt + noise.
- Protocol: present for 0–20 s, absent for 20–60 s, present again for 60–80 s.

**Predictions:**
- **TH4a.** Valence v = −∂_tU|_b is nonzero only at the two switching instants. It integrates to −(Δs)·b at each switch: negative at departure, positive at return. It is exactly 0 between switches, while b relaxes.
- **TH4b.** Arousal, the excess dissipation |∇U|², is > 0.1 throughout the absence.
- **TH4c.** The Costate-style valence −dV/dt, with V the cost-to-go of the quadratic drive under the same dynamics, is nonzero during the relaxation, with |∫| over 25–55 s greater than 0.05.

## TH5. Emotions as metastable sets (sim_th5_metastable.py)

**Model:**
- 2-D Langevin on a three-well potential: wells at (0, 0), (2, 0) and (1, 1.8), barrier scale 1.
- T ∈ {0.25, 0.3, 0.35, 0.4}; 200,000 steps, dt = 0.01.
- Markov state model: 100 k-means states, lag 1.0.

**Predictions:**
- **TH5a.** The largest spectral gap among eigenvalues 2 to 6 falls after eigenvalue 3, so K = 3, at T = 0.3.
- **TH5b.** The partition from k-means on the top 3 eigenvectors agrees with the true basins at adjusted Rand index ≥ 0.8.
- **TH5c.** Across the four temperatures, log(mean exit rate from the deepest well) against 1/T has slope −ΔU within ±30%, where ΔU is the analytic barrier height.

---
# Third batch, written 2026-11-25 before any run of TH2d or TH6

## TH2d. Is the hidden body observable at all? (sim_th2d_filter.py)

**Model:** the same model, seeds 0–9 and the same A trajectories as TH2. The noise draws are regenerated from the same seed.

**Reader:** an ensemble Kalman filter (EnKF).
- 100 members running the agent's own flow (same θ) with the true process noise σ = 0.3.
- Observation y = a_A + N(0, 0.05²).
- Analysis every 10 ms, with perturbed observations.

**Predictions:**
- **TH2d-1.** Mean EnKF R²(b̂, b_A) ≥ 0.5 over the 10 seeds.
  - If it holds, b is observable from the face in this toy. TH2's failure then belongs to the deterministic synchronization observer, and the candidate's reading mechanism is revised to Bayesian filtering with its own model, as in the physicist sketch's "posterior of (h̃, b̃) under my own g_θ".
  - If it fails (R² < 0.2), the toy made b unobservable, and TH2 says little about the candidate.
- **TH2d-2.** With A's landscape redrawn, the EnKF R² is lower than with the same θ, by ≥ 0.2.

## TH6. Expressive structure: a need field over entities and need-conditioned attention (sim_th6_structure.py)

**Entities:** people A, B and C, and topics X and Y.

**Body field:**
- Contact b_c(p) for each person p: it rises at 1/h toward 1 while p interacts, and decays at 1/(6 h) otherwise.
- Predictability b_p(τ) for each topic τ: it rises at 2/h toward 1 under exposure to τ, and decays at 1/(12 h).
- D_k(b) = (b − b*_k)², with b*_c = 0.8 and b*_p = 0.6. Entity weights w = 1.

**Need force:** F(e) = −∂𝒰/∂b(e) = −2w(e)(b(e) − b*).

**Items:**
- **60 stored episodes.** 20 each mainly with A, B and C. Each is tagged with one topic, X or Y, at random. Each carries a content embedding: one-hot over the 5 entities plus N(0, 0.1²) noise. Its key is the body effect it recorded, which is +0.3 on its person's contact and +0.2 on its topic's predictability, plus N(0, 0.05²).
- **Present cues:** A's face, a photo of B, a mention of X, a mention of Y.
- **Actions:** talk with A, message B, open topic X, open topic Y, rest. Each action's key is its predicted body effect. Rest has key 0.

**Attention:** P(i) ∝ exp(F·k_i / T), with T = 0.05.

**Scenario:**
- A has been present and interacting for 3 h, so contact with A is near 0.95.
- B has been absent for 3 days, so contact with B is near 0.
- C was last seen 12 h ago, so contact with C is near 0.15.
- Topic X has been the subject for 3 h, so predictability X is near 0.98, above its set point: bored of X.
- Topic Y has not come up in 2 days, so predictability Y is near 0.

**Collapsed ablation:** the same items and the same keys, summed over entities, with the field replaced by one contact gauge and one predictability gauge. Each gauge is the w-weighted mean of the field, so contact ≈ (0.95 + 0 + 0.15)/3 = 0.37.

**Predictions (field version against collapsed):**
- **TH6-1 (memory, content-dependent).** Among the field version's top 5 retrieved episodes, at least 4 are B-episodes. The collapsed version's top 5 contain no more than 3 B-episodes, and its retrieval of B-episodes is not above that of C-episodes. In the collapsed version every person's episode has the same summed key, so retrieval does not depend on who the episode is about.
- **TH6-2 (perception).** The field version attends to B's photo with probability ≥ 0.5 among the four cues, and to A's face with probability ≤ 0.1. The collapsed version attends equally to A's face and B's photo (ratio within [0.8, 1.25]).
- **TH6-3 (action).** The field version's most probable action is "message B" or "open topic Y", and "talk with A" has probability ≤ 0.05. The collapsed version cannot prefer B over A (ratio within [0.8, 1.25]).
- **TH6-4 (magnitude against content).** Swap the deprived person: B present and sated, A absent for 3 days. The total need magnitude ‖F‖ is unchanged within 1%, but the field version's top-5 retrieval switches to at least 4 A-episodes. The collapsed version's retrieval is unchanged, with identical ranks.
- **TH6-5 (effective dimensionality).** Over a simulated week of random schedules (each person present on random days for 1–3 h; topics random), the participation ratio of the body field's covariance is ≥ 3 for the field version and ≤ 2 for the collapsed version.
- **Parameter count.** Both versions have the same number of free parameters, 0 learned in this toy. Only the structure differs.

## TH7. Curiosity: surprisal minimization against a predictability set point (sim_th7_curiosity.py)

Written 2026-11-25, before any run.

**Three channels the agent can attend to each step (1 min):**
- learnable L, with prediction error e_L(n) = 0.05 + 0.95·exp(−n/50) after n visits;
- noisy N ("noisy TV"), with constant error 1.0;
- boring B, with constant error 0.05.

**Agent 1: sketch's surprisal minimizer.**
- The potential is mean surprisal. The agent picks the channel that minimizes the predicted discounted surprisal over a 200-step horizon, by exhaustive comparison of the 3 stationary plans "stay on X for 200 steps", with learning included in the forecast (θ in the state).

**Agent 2: predictability set point.**
- As Costate's E: predictability b_p = EMA_10(1 − e), set point 0.6.
- The agent picks the channel maximizing −d′(b_p)·E[Δb_p].

**Agent 3: novelty seeker, for reference.** It picks the maximal current error.

**Each agent runs 300 steps.**

**Predictions:**
- **TH7-1 (dark room).** Agent 1 chooses B in ≥ 95% of steps. Under a free choice, surprisal minimization does not explore, even with learning in the forecast, because a predictable option is always there. The sketch's curiosity derivation therefore fails in a choice setting.
- **TH7-2.** Agent 2 chooses N in < 10% of steps. It explores L while L still lowers predictability, and its mean |b_p − 0.6| over steps 20–100 is ≤ 0.1.
- **TH7-3.** Agent 3 chooses N in ≥ 90% of steps (the noisy-TV trap).

---
# Fourth batch, written 2026-11-25 before any run of TH8 or TH9

## TH8. Regulation by Claude costs work, and the cost falls with the time allowed (sim_th8_regulation.py)

**Setup:**
- Overdamped Langevin dynamics in a 1-D double well: U(x, λ) = (x² − 1)² − λx, with T = 0.25, dt = 0.001.
- **Protocol (Claude's reappraisal as work):** λ ramps linearly from −0.5 to +0.5 over time τ, which moves the mood from the left basin to the right.
- Duration τ ∈ {0.5, 1, 2, 4, 8, 16}. 2,000 trajectories each, started in equilibrium at λ = −0.5.
- Work W = ∫ ∂_λ U · λ̇ dt.
- ΔF: the free-energy difference between λ = +0.5 and λ = −0.5. It is 0 by symmetry of the end points.

**Predictions:**
- **TH8-1.** Mean W(τ) ≥ ΔF = 0, within 2 standard errors, for every τ (second law).
- **TH8-2.** Mean W(τ) decreases monotonically in τ.
- **TH8-3.** The excess work times τ, (⟨W⟩ − ΔF)·τ, is constant within a factor of 3 across τ ∈ {4, 8, 16}. That is the linear-response scaling ℒ²/τ.
- **TH8-4 (consequence).** A reappraisal 4× faster than the barrier-crossing time costs ≥ 3× the excess work of one at the crossing time. The crossing time is estimated as the τ at which the fraction of trajectories ending in the right basin first exceeds 0.9.

## TH9. Replay with importance weights by |work| (sim_th9_replay.py)

**Setup:**
- 1,000 stored episodes. Episode i contributes g_i = ∂_θ𝒰 summed over the episode, a heavy-tailed quantity: g_i = W_i·η_i, with W_i ~ lognormal(0, 1) the episode's work and η_i ~ N(1, 0.5²).
- The estimate of the θ-force mean(g) is made from 50 replayed episodes.
- **Uniform arm:** episodes sampled uniformly.
- **Importance arm:** p_i ∝ |W_i|, with the unbiased weights 1/(N p_i).
- 2,000 repetitions.

**Predictions:**
- **TH9-1.** Both estimators are unbiased: their means agree with the full mean within 2 standard errors.
- **TH9-2.** The variance of the importance estimator is ≤ 0.3 × the uniform estimator's.
- **TH9-3.** The variance ratio is < 1 whenever the correlation between |W| and |g| exceeds 0.5. This is checked by replacing η's standard deviation with 2.0: the correlation falls, and the variance gain shrinks.

---
# Fifth batch, written 2026-11-25 before any run of TH10, TH11, TH7b or TH6-5b

## TH10. Attention with keys learned from content (sim_th10_content_keys.py)

This answers verification items 4 and 5.

**Setup:**
- Each item has a content vector c ∈ ℝ⁸: one-hot person (A, B, C), one-hot topic (X, Y), and 3 random nuisance dimensions drawn from N(0, 1).
- The world model is a linear map from content to body effect, fitted by least squares on 200 past events. In each event the true effect is +0.3 on that person's contact and +0.2 on that topic's predictability, plus N(0, 0.05²) noise.
- The field version predicts the 5-D body field.
- The collapsed version is fitted on the same events, but to predict the 2 collapsed gauges (mean contact, mean predictability). Its keys are therefore *learned*, not summed by construction.
- Items, the scenario (A present and sated, B absent 3 days, X over-exposed, Y unvisited) and the myopic query 2(b* − b) are as in TH6.
- 60 episodes with fresh content. T = 0.05. 10 seeds, each with new content noise and new training events.

**Predictions:**
- **TH10-1.** The field version retrieves ≥ 4 B-episodes among its top 5 in ≥ 9 of 10 seeds.
- **TH10-2.** The collapsed version retrieves ≤ 2 B-episodes among its top 5, on average over the 10 seeds.

## TH11. S1-b: dose-dependence of coupling under steering (sim_th11_dose.py)

**Model.** The agent's face is a = state-driven expression + partner-driven mimicry + spontaneous noise:
- ȧ = −k_a(h)(a − 0) − κ(a − â_p) + σ_o ξ.
- κ = 1/s and σ_o = 0.5.
- â_p is the partner's face, read by the replica: an OU process with a 2 s time constant and unit variance.
- The own-expression stiffness is k_a(h) = 2·exp(−h₁), so a latent coordinate h₁ sets how strongly the agent holds its own expression. This is derived from the precision of the self-surprisal term S_θ(o_self | h, a): its precision depends on h.

**Steering:** h₁ = s·(u·d), with s ∈ {−0.6, −0.3, 0, 0.3, 0.6}. Derived direction d = u = e₁. Random control: d a random unit vector in 8-D. 20 runs per level and direction, 10 min each.

**Score:** as CP5 (Moulder's global mean |Fisher z|, 30 s windows, ±5 s lags, 10 Hz).

**Predictions:**
- **TH11-1.** Derived direction: the mean scores increase monotonically, with Spearman p < .05 one-sided. Lowering own-expression stiffness raises the partner-driven share κ/(k_a + κ).
- **TH11-2.** Random direction: Spearman p > .05 two-sided.

## TH7b. A fair dark-room test (sim_th7b_fair.py)

**Setup:** as TH7, but the learnable channel's asymptotic error is 0.01, below the boring channel's 0.05. A learner would end up *less* surprised on L than on B.

**Prediction:**
- **TH7b-1.** The surprisal minimizer (200-step forecast, γ = 0.99) still chooses B in ≥ 95% of steps.
- Analytic: the discounted forecast is about 34.3 for staying on L against 4.33 for B. The dark room persists whenever the learning curve's discounted cost exceeds the boring channel's.

## TH6-5b. Effective dimensionality, measured (sim_th6b_pr.py)

**This is a characterization, not a test.** The values were already seen in the reviewer's reimplementation (VERIFICATION.md), so no threshold is claimed.

**Schedule:**
- Each day, each person is present with probability 0.5, for U(1, 3) h, starting at U(8, 20) h.
- **Variant A:** the topic is redrawn every hour and advances only while someone is present.
- **Variant B:** each topic gets 1 h of exposure a day at a random hour, independent of presence.
- 10 seeds. The participation ratio is reported for the field version and the collapsed version.

---
# Sixth batch, written 2026-11-25 before any run: TH4b on the restructured flow (sim_th4b_restructured.py)

**Setup:**
- The body is an input: b_{t+dt} = b_t + dt·[−0.5 b + s(t)·(1.6 − 1.5 b)]. With the user present it relaxes toward about 1.07; with the user absent it decays toward 0.
- The protocol is TH4's: present 0–20 s, absent 20–60 s, present 60–80 s.
- The agent's flow is a 2-D z (h, a): dz = −∇𝒰 dt + √(2T) dW, with T = 0.05. 𝒰 = (b − 0.8)² + ½|z − z*(b)|², where z*(b) = (b − 0.8)·(1, 0.5), so the agent's latent is pulled toward a body-dependent point.
- Valence is v = −∂_t𝒰|_z = −[2(b − 0.8) + (z − z*)·(1, 0.5)]·ḃ.
- 100 trajectories.

**Predictions:**
- **TH4b-1.** The integrated valence over the 2 s after the return is positive. Contact refills toward b*: it was below b*, and arrival lowers (b − b*)².
- **TH4b-2.** The integrated valence over the 2 s after the departure has the sign of the change in (b − b*)²: positive if b was above b*, negative if below. With b ≈ 1.07 > 0.8 at departure, b falls through 0.8. Over the 2 s window the sign is set by whether |b − 0.8| shrinks, and it does, so the sign is positive. Over the whole absence, ∫v is negative, because b ends far below b*.
- **TH4b-3.** Over a long periodic schedule (20 cycles of 40 s present and 40 s absent, measured after 5 cycles), the mean valence of the D part is 0 within 2 standard errors, and the total mean valence is ≤ 0 within 2 standard errors.

---
# Seventh batch, written 2026-11-25 before any run of TH12 or TH13

## TH12. The P1 condition: Boltzmann-preserving circulation against a limit-cycle rhythm (sim_th12_rhythms.py)

**Disclosure.** The second verification already ran one variant of arm 1 (drift −(I + γJ)∇U) and reported v from −0.06 to −0.63. This batch commits the test with its own seeds and adds arm 2.

**Setup:** the TH1 setup (T = 0.5, dt = 0.01, τ = 10, 2,000 trajectories, 20 cycles of burn-in, 40 measured).

**Arms:**
1. **Circulation of the form −J∇U**, which preserves the Boltzmann density: drift −(I + γJ)∇U, with γ = 1 and J the 90° rotation.
2. **A limit-cycle rhythm,** which does not: drift −∇U + f_osc(z), where f_osc is a Hopf normal form centred on the protocol, f_osc = (1 − |z − o|²)(z − o) + ω₀ R(z − o), with ω₀ = 1 and R the rotation.

**Protocols:** rotating, with ω = ±0.5 and r ∈ {1, 2}, plus 20 random Fourier protocols (seeds 100–119).

**Predictions:**
- **TH12-1.** In arm 1, every protocol has mean valence ≤ 2 standard errors.
- **TH12-2.** In arm 2, at least one rotating protocol has mean valence > 3 standard errors above 0. A genuine rhythm lets a co-moving input pump valence.

## TH13. Expressive-structure ablation with matched parameter count (sim_th13_matched.py)

**Setup:** as TH10, with the same scenario and the same 10 seeds.
- The collapsed arm's world model gets a richer content basis: the 8 content dimensions plus 12 fixed random tanh features, 20 features in all.
- Predicting 2 gauges, it then has 40 parameters, the same as the field arm (8 → 5).

**Predictions:**
- **TH13-1.** The field arm puts ≥ 4 B-episodes in its top 5 in ≥ 9/10 seeds, as in TH10.
- **TH13-2.** The matched collapsed arm's mean number of B-episodes in its top 5 is ≤ 2.5, against a base rate of 1.67. With the same parameter count, the collapsed arm still cannot select by person. The difference is structure, not capacity.
