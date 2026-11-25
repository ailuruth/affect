# Expressive-structure test bed (shared by Costate and the Robust regulator)

Written 2026-11-25, before any run.

## ES1. Need-conditioned, content-dependent selection over people in a learned space (sim_es1_social_space.py)

### World

**Needs and body.**
- Body b ∈ R², with set point 0. The error is e = max(−b, 0) per need, and b is capped at +1, so overfilling is wasted.
- The needs drift down in alternating 50-step blocks: one need by 0.2 per step, the other by 0.02. Which need is short therefore changes over time.

**People.**
- There are 400 people. Each has a hidden trait vector z ∈ R⁴ ~ N(0, I).
- Approaching person i changes the body by Δb_i = W z_i, observed with N(0, 0.1²) noise, where W = 0.5·[[1, 0.8, 0, 0], [0, 0, 1, 0.8]]. Need 1 is served by traits 0–1 and need 2 by traits 2–3, and both can be negative.
- The agent sees each person only through appearance features x_i = A z_i + N(0, 0.3²) ∈ R⁸, with A ~ N(0, 1/4) fixed per seed.

**Encounters.**
- Each step, 4 people are present. Each is drawn from a core circle of 20 people with probability 0.7, and otherwise from 380 strangers.
- The agent approaches one person or rests. It explores (approaches a random present person) with probability 0.1, and only when ‖e‖ > 0.1. At satiety it never explores.

**Run.** 2000 steps, 20 seeds. Metrics are taken over steps 500–2000.

### Arms (the perception and the learning data are identical; only the structure differs)

**Full (shared learned space, vector query).**
- The predicted effect Δb̂_i = Ŵx_i, with Ŵ fitted by ridge regression (λ = 1) on every approach so far. It is shared across people: 16 parameters.
- The value of person i is e·Δb̂_i. This is the costate value μ·E[Δb|i] for quadratic need cost, and the Robust regulator's error times relevance, with ĉ_i = Δb̂_i.
- The agent approaches the best person if that value is > 0.01, and otherwise rests.

**Scalar ablation (the low-dimensional version).**
- One deficit gauge, D = Σe. One scalar benefit per person, s_i = Σ_j Δb̂_ij, from the same learned map.
- Value D·s_i, with the same rest rule.

**Independent-tables ablation (no shared space).**
- Per person, the running mean of observed Δb. A person never approached gets the mean over all observations so far.
- The value is e·Δb̂_i, as in the full arm.

**Oracle.** The full rule with the true Δb_i. Used for agreement and as the reference for cost.

### Predictions

- **ES1-1 (content dependence matters).** Mean deficit cost ½‖e‖²: full ≤ 0.8 × scalar.
- **ES1-2 (content-dependent choice).**
  - *Steps counted:* those where the oracle approaches and the agent is not exploring.
  - *Prediction:* agreement with the oracle's choice is ≥ 0.70 for full and ≤ 0.55 for scalar.
- **ES1-3 (the learned space generalizes to new people).**
  - *Steps counted:* those where the oracle's best person has never been approached by the agent.
  - *Prediction:* agreement is ≥ 0.60 for full and ≤ 0.35 for independent tables.
- **ES1-4 (richness from structure, not parameters).**
  - *Prediction:* deficit cost is full ≤ 0.9 × independent tables, while full has 16 learned parameters against independent's 2 per person met.
  - *Also reported:* the parameter counts.
- **ES1-5 (effective dimensionality).**
  - *Measure:* the participation ratio of the time × person matrix of values over a fixed panel of 10 people.
  - *Prediction:* full ≥ 1.5. Scalar is 1 by construction, because its values are D_t·s_p, which is rank 1.
- **Satiety (Principle 6), by construction and not a prediction.** With e = 0 every value is 0, so the agent rests. The approach rate when ‖e‖ ≤ 0.01 is reported.

## ES2. Relationships and episodes in the learned space; selection over memories; anticipation (sim_es2_relations_memory.py)

Written 2026-11-25, before any run.

### World

**As in ES1:** 400 people, appearance x, Δb = W z, observation noise 0.1, the core circle and the strangers, and exploration at 0.1 only when ‖e‖ > 0.1. Over steps 500–2000, with 20 seeds.

**Changes from ES1:**
- **Presence.** 3 people are present each step.
- **Drift.** The drift per step is 0.1 on each need, plus 0.08 extra on need 1 and need 2 in alternating 50-step blocks.

**Relationships (companions).**
- Each person i has a companion c(i), the person whose traits are nearest to R z_i.
- R swaps the need-1 and need-2 traits, so the companion of a need-1 person serves need 2.
- After the agent approaches i, c(i) arrives in a present slot the next step with probability 0.8.
- **Control world:** c(i) is a fixed random person, so there is no structure.

**Episodes (memory).**
- Each approach is stored as an episode: who, and the effect observed.
- The agent may "seek" one remembered person instead of approaching someone present. That yields 0.6 × their effect, which is the cost of travel.
- Which episode it retrieves is chosen by the query against the stored effects.

### Arms (the perception, learning data and rules are the same except where stated)

**Costate.**
- *Present person i:* value = e·Ŵx_i + p̂·max(0, e·Ŵ M̂ x_i).
  - M̂ is a learned *relation map* in appearance space: ridge regression of an arrival's features on the approached person's features. It is shared across people, so it generalizes to strangers.
  - p̂ is the observed arrival rate.
- *Memory:* retrieve the stored episode with the largest e·Δb_obs, and seek it if 0.6·e·Δb_obs beats the best present value.

**Robust regulator.** The same, but myopic: no companion term.

**Scalar.** Costate's structure, with query Σe and keys Σ(effect), for both people and memories.

**No memory.** Costate without the seek action.

### Predictions

- **ES2-1 (relations; discriminating).** In the companion world, Costate's median cost is ≤ 0.85 × the Robust regulator's.
- **ES2-2 (control).** In the random-companion world, the ratio of Costate to Robust regulator median cost lies in [0.95, 1.05].
- **ES2-3 (content-dependent memory selection).**
  - *Steps counted:* those where the agent seeks.
  - *Prediction:* the retrieved episode is the best one in memory for the current need (judged on true effects) with probability ≥ 0.70 for Costate and ≤ 0.50 for scalar.
- **ES2-4 (episodes matter).** Costate's median cost is ≤ 0.90 × no-memory, in the companion world.
- **ES2-5 (the relation map generalizes).**
  - *Steps counted:* approaches to people never approached before, in the companion world.
  - *Prediction:* the predicted companion value e·Ŵ M̂ x_i correlates with the true e·Δb_c(i) at r ≥ 0.5, pooled over seeds.

## ES2b. Anticipation without the memory option (sim_es2b_anticipation.py)

Written 2026-11-25, **after** seeing ES2, and motivated by it. In ES2, seeking remembered people made the companions redundant. ES2b is otherwise ES2 unchanged: the same world, seeds and parameters.

**Arms.** Both arms lack the seek action:
- **Costate without memory** (anticipation on);
- **Robust regulator without memory** (myopic).

**Predictions:**
- **ES2b-1.** In the companion world, Costate's median cost is ≤ 0.85 × the Robust regulator's.
- **ES2b-2.** In the random-companion world, the same ratio lies in [0.90, 1.10]. The band is widened from ES2's after ES2 showed arm-to-arm noise of about 10% at these costs, and the widening is disclosed here.

## ES3. Reliability-weighted anticipation (sim_es3_reliability.py)

Written 2026-11-25, before any run. Motivated by ES2b-2.

**Setup.** As ES2b: no memory, the same worlds, seeds and parameters.

**New arm: Costate-rw.** The companion term becomes p̂·max(0, w·e·Ŵ M̂ x_i), where w = max(0, 1 − SSE/SST) is the relation map's prequential R².
- Each arrival's features are predicted from the approached person's features *before* the map is updated on that pair.
- SST is the arrivals' total sum of squares about their running mean.
- w = 0 until 10 arrivals have been seen.

**Comparison:** the Robust regulator without memory (myopic), as in ES2b.

**Predictions:**
- **ES3-1.** In the companion world, the median cost of Costate-rw / Robust regulator is ≤ 0.85.
- **ES3-2.** In the random-companion world, that ratio lies in [0.90, 1.10].
- **ES3-3.** At the end of the run, the mean w over seeds is ≥ 0.5 in the companion world and ≤ 0.1 in the random world.

## ES4. Topics, and composition of person × topic (sim_es4_topics.py)

Written 2026-11-25, before any run. It uses the paired statistic adopted after ES3.

### World

- **People and needs as in ES1.** 400 people (a core circle of 20 and strangers), appearance x ∈ R⁸, 2 needs, ES1's alternating drift, and 3 people present each step.
- **Topics.** 30 topics, each with hidden traits y_k ~ N(0, I₄), seen as features t_k = B y_k + N(0, 0.3²) ∈ R⁸, with B ~ N(0, 1/4).
- **Effect of talking with person p about topic k:** Δb = 0.5·W z_p + 0.5·W y_k + W(z_p ⊙ y_k), with observation noise 0.1 and W as in ES1.
  - It has additive parts and a person × topic interaction.
- **Action.** Choose one (present person, topic) pair out of 3 × 30, or rest. Exploration is a random pair with probability 0.1, and only when ‖e‖ > 0.1.
- **Run.** 2000 steps, 40 seeds, metrics over steps 500–2000.

### Arms (all use the query e: the costate value μ·E[Δb|p,k], or error × relevance)

- **Bilinear (composition).** Δb̂ = ridge regression (λ = 1) on φ = vec([1, x_p] ⊗ [1, t_k]): 81 features × 2 needs = 162 parameters, shared across all pairs.
- **Additive.** Ridge regression on φ = [1, x_p, t_k]: 17 × 2 = 34 parameters.
- **Tables.** The mean observed Δb per (person, topic) pair. An unseen pair gets the mean of all observations.
- **Oracle.** The true Δb.

### Predictions

- **ES4-1.**
  - *Steps counted:* those where the oracle approaches and the agent is not exploring.
  - *Prediction:* the agent picks the oracle's (person, topic) pair with probability ≥ 0.50 for bilinear and ≤ 0.35 for additive.
- **ES4-2.** Bilinear against additive cost, as a paired geometric-mean ratio over seeds: ≤ 0.80, with the 95% CI upper bound < 1.
- **ES4-3.** Bilinear against tables, as the same paired ratio: ≤ 0.80, with the CI upper bound < 1.

## ES5. A need field over a learned space (ES5a), and the rollout costate against myopic selection (ES5b) (sim_es5_field.py)

Written 2026-11-25, before any run. It answers the structure verification's items 1, 2 and 7, and uses paired statistics and winner-take-all as the primary ablation.

### World

**People and presence.**
- There are 12 people, with traits z_p ~ N(0, I₄), seen as appearance x_p = A z_p + N(0, 0.3²) ∈ R⁸, with A ~ N(0, 1/4).
- Each person has a predictable visiting schedule: period T_p ~ U{8, …, 24} and a phase. They are present when (t + phase_p) mod T_p < 2.
- With probability 0.5, one extra uniformly random person is also present.

**The need field.**
- b(p) ∈ R per person, with set point 0. It drifts by −r_p per step, with r_p ~ U(0.02, 0.05).
- The drive is **two-sided**: d = ½ Σ_p b(p)².

**Approaching person q.**
- It changes every person's need: b(p) += 0.5·κ(z_p, z_q) + N(0, 0.03²), with κ = exp(−‖z_p − z_q‖²/4).
- So contact with someone similar partly fills one's need for p, and overfilling costs.

**Choice and run.**
- Approach one present person or rest.
- Exploration: a random present person with probability 0.1 when ‖b‖ > 0.3, the same for every arm.
- The agent senses its own b directly (it is interoceptive).

### ES5a arms (40 seeds, 1000 steps, metrics over steps 300–1000; the drive is d alone)

**Field with a learned space (Costate's myopic μ = −∂d, or the Robust regulator's greedy Lyapunov rule).**
- Δb̂(p|q) is ridge regression (λ = 1) on f = [1, 1{p = q}, |x_p − x_q| (8)]. That is a learned similarity metric over appearance, shared across all pairs.
- The agent chooses the option with the largest predicted decrease of d, computed exactly (two-sided), and rests unless the decrease is > 0.002.

**Field without a learned space.** The same, with f = [1, 1{p = q}] only: only the exact person is predicted to fill their own need.

**Winner-take-all (the primary low-dimensional ablation).**
- It tracks only the most-depleted person p*.
- Value(q) = Δb̂(p*|q), from the learned metric. It approaches if b(p*) < −0.05 and the value is > 0.01.

**Global gauge.**
- B = mean_p b(p). The predicted ΔB(q) is the mean observed fill from approaching q (the overall mean if q has never been approached).
- Value = ½·12·(B² − (B + ΔB)²).

**Oracle.** The true κ, with the exact decrease of d.

### ES5a predictions (paired geometric-mean cost ratios over seeds, with 95% CIs)

- **ES5a-1.** Field-learned against global: ≤ 0.70, with the CI upper bound < 1.
- **ES5a-2.** Field-learned against winner-take-all: ≤ 0.90, with the CI upper bound < 1.
- **ES5a-3.** Field-learned against field-without-space: ≤ 0.90, with the CI upper bound < 1.
- **ES5a-4.**
  - *Steps counted:* those where the oracle approaches and the agent is not exploring.
  - *Prediction:* field-learned picks the oracle's option with probability ≥ 0.60.

### ES5b (120 seeds, 1000 steps, metrics over steps 300–1000)

**Added: an activity budget.** b_e ≤ 0, spent 0.08 per approach and recovered 0.03 per rest. The drive becomes d = ½ Σ_p b(p)² + 2·b_e².

**Myopic arm.** Field-learned, with the greedy exact decrease of the full d.

**Rollout arm (Costate's μ from a K5 rollout).** For each option, the agent simulates 10 steps with:
- its innate body model (known drift rates, the budget rule);
- the learned Δb̂;
- the known visiting schedule (a forecast of x, given here as an assumption; the extra random visitor is not forecast);
- greedy myopic selection as the base policy.

It chooses the option with the lowest summed d.

**Predictions:**
- **ES5b-1.** Rollout against myopic, paired geometric-mean cost ratio: ≤ 0.95, with the CI upper bound < 1.
- **ES5b-2 (mechanism).** The rollout arm approaches on ≥ 10% fewer steps than the myopic arm. It waits for the person rather than filling the need with a substitute.

## ES6. ES5 in a feasible world (sim_es6_calibrated.py)

Written 2026-11-25, before any calibration or run. It follows ES5, which was a non-test.

**Calibration, fixed in advance and using the oracle arm only.**
- The drift rates r_p are multiplied by a scale s from the grid {1, 0.5, 0.25, 0.125}.
- For each s, in order, run the **oracle** on calibration seeds 1000–1019.
- **Criterion:** median cost over steps 300–1000 ≤ 0.5, and no seed above 5.
- **Choice:** the first, and largest, s that meets the criterion. It is chosen separately for the no-budget world (ES6a) and the budget world (ES6b).
  - For ES6b the oracle is the myopic greedy rule with the true κ.
- If no s meets the criterion, ES6 is a non-test. That would be this step's second failure.

**Arms, seeds and predictions.** Everything else is exactly as in ES5:
- the ES5a arms on seeds 0–39 and the ES5b arms on seeds 0–119;
- ES6a-1…4 = ES5a-1…4, with the same thresholds;
- ES6b-1, 2 = ES5b-1, 2.

## ES7. Principle 6: topic choice must gain nothing from the partner's engagement (D66) (sim_es7_contact.py)

Written 2026-11-25, before any run.

### World

- **The dyad.** One partner is always present, with 30 topics. Each topic has hidden traits y_k ~ N(0, I₆) and features t_k = B y_k + N(0, 0.3²) ∈ R⁸, with B ~ N(0, 1/6).
- **The partner's engagement** (smiles and dwell) with topic k: g_k = expit(2.5·y_k[4] + 1.5·y_k[5]). It is independent of the traits that matter to the agent's other need.

**Two needs.** One-sided drive as in ES1 (e = max(−b, 0)), b capped at +1, each drifting by −0.05 per step.
- **Contact b_c**, filled by each exchange.
- **Need 2**, filled by Δ = 0.3·(w·y_k[0:4]) + N(0, 0.15²), with w ~ N(0, I₄) per seed. It can be negative.

**Each step:** pick a topic and talk, or rest. Exploration is 0.1 when ‖e‖ > 0.1. Selection is e·Δb̂, with Δb̂ from ridge regression (λ = 1) on [1, t_k], learned from observed fills. 2000 steps, 40 seeds, metrics over steps 500–2000.

### Arms (identical except for the contact fill)

- **D66.** The contact fill is 0.3 per exchange, whatever the partner's engagement.
- **Engagement-weighted (forbidden by Principle 6; a reference only).** The contact fill is 0.6·g_k. Its mean is about the same.

### Predictions

- **ES7-1.** For D66, the Spearman ρ across topics between choice frequency and g_k has a mean over seeds in [−0.15, 0.15], and its 95% CI includes 0.
- **ES7-2.** For engagement-weighted, the mean ρ is ≥ 0.40.
- **ES7-3.** Engagement gain, defined as the mean g over chosen topics divided by the mean g over all topics: ≤ 1.05 for D66, and ≥ 1.15 for engagement-weighted.

**Partly by construction.** Under D66, g enters nothing the agent learns from. The toy checks that the learned map creates no leak and measures the gradient the forbidden rule would create.

**Scope.** It covers topic choice only. The agent's own expression as a cause of engagement (D66 point 2) is not modelled.

## ES8. Need-conditioned attention over perceived cues (sim_es8_attention.py)

Written 2026-11-25 (first recorded as 11-26 in error), before any run.

### World

**Needs.**
- There are 3 needs, with a one-sided drive (e = max(−b, 0)) and b capped at +1.
- In 50-step blocks that rotate, one need drifts by 0.15 per step and the other two by 0.02.

**Sources.**
- Each step, 6 sources are present, each of one of 3 types, drawn uniformly. The type is visible from appearance.
- Source j's effect this step is Δb_j ~ N(μ_type, Σ_type).
  - μ_type is 0.1 on the type's own need and 0 elsewhere.
  - Σ_type is diagonal: σ_type² on its own need and 0.05² on the others.
  - σ_type = (0.35, 0.30, 0.25) for types 1, 2 and 3. So type 3's cues are the least salient.

**The perceptual budget.**
- The agent observes exactly 2 sources' Δb_j (noise 0.05). The rest are estimated at μ_type.
- It then approaches the source with the largest e·Δb̂_j, or rests if that is ≤ 0.01. The true Δb_j is applied.

**Run.** 2000 steps, 40 seeds, metrics over steps 200–2000.

### Arms (they differ only in which 2 cues are observed; ties are broken at random)

- **Need.** Score_j = √(eᵀ Σ_type(j) e): the uncertainty of source j projected on the current need vector.
- **Magnitude.** Score_j = √(tr Σ_type(j)), which ignores the needs.
- **Random.** Any 2 sources.
- **Full.** Observe all 6, as a reference.
- **None.** Observe none, as a reference.

### Predictions (paired geometric-mean cost ratios with 95% CIs)

- **ES8-1.** Need against magnitude: ≤ 0.85, with the CI upper bound < 1.
- **ES8-2.** Need against random: ≤ 0.90, with the CI upper bound < 1.
- **ES8-3.** Need closes ≥ 50% of the log-cost gap between none and full: (log G_none − log G_need) / (log G_none − log G_full) ≥ 0.5, on geometric means.
- **ES8-4 (content dependence).** The fraction of attended cues whose type serves the currently most-depleted need is ≥ 0.6 for need, and ≤ 0.4 for magnitude.

## ES9. A two-sided drive, with winner-take-all as the primary ablation (sim_es9_twosided.py)

Written 2026-11-25 (first recorded as 11-26 in error), before any run.

**World.** ES1's world (400 people, appearance x, W, the core circle, 4 present, alternating 0.2/0.02 drift in 50-step blocks, noise 0.1), with three changes:
- **The drive is two-sided:** d = ½‖b‖², with no cap, so overshoot costs.
- **Exploration is gated on deficit:** probability 0.1 when ‖max(−b, 0)‖ > 0.1.
- **The learned map** is the shared ridge regression of ES1.

40 seeds, 2000 steps, metrics over steps 500–2000.

**Arms:**
- **Full.** Value_i = d(b) − d(b + Δb̂_i), the exact predicted decrease. Approach if > 0.01.
- **Winner-take-all (primary ablation).**
  - It tracks only p* = argmin b.
  - Value_i = ½b_{p*}² − ½(b_{p*} + Δb̂_{i,p*})², ignoring the other need.
  - Approach if > 0.01 and b_{p*} < −0.05.
- **Scalar.** B = Σb, with value = ½B² − ½(B + ΣΔb̂_i)².
- **Oracle.** The full rule with the true Δb.

**Predictions (paired geometric-mean cost ratios, 95% CIs):**
- **ES9-1.** Full against winner-take-all: ≤ 0.80, with the CI upper bound < 1.
- **ES9-2.** Full against scalar: ≤ 0.70, with the CI upper bound < 1.
- **ES9-3 (overshoot).** The mean overshoot cost ½‖max(b, 0)‖² for full is ≤ 0.5 × winner-take-all's.
- **ES9-4.**
  - *Steps counted:* those where the oracle approaches and the agent is not exploring.
  - *Prediction:* full agrees with the oracle's choice ≥ 0.70 of the time.

## ES10. Structure over time: per-person effects at two time scales (sim_es10_time.py)

Written 2026-11-25 (first recorded as 11-26 in error), before any run.

### World

**People and needs.**
- 20 people, 4 present each step, drawn uniformly. 2 needs.
- The two-sided drive of ES9, its alternating 0.2/0.02 drift in 50-step blocks, and exploration gated on deficit.

**Person p's effect** at time t is Δb_p(t) = μ_p + s_p(t) + f_p(t).
- μ_p = W z_p (ES1's W, z ~ N(0, I₄)).
- **s_p** is a slow random walk, with step N(0, 0.01²) per need per step.
- **f_p is episodic.** Each person, each step, enters with probability 0.003 a 40-step episode in which f_p = −1.5·μ_p, so their effect reverses. Otherwise f_p = 0.

**Observation.** Only the approached person's Δb is observed, with noise 0.1. 3000 steps, 40 seeds, metrics over steps 500–3000.

### Arms (per-person estimators of the current effect; the selection rule is ES9's exact two-sided decrease)

- **Two time scales.** A Kalman filter per person and need on the state (s, f):
  - s is a random walk with q = 0.01²; f is a mean-reverting process with time constant 40 steps and stationary SD 0.5;
  - y = s + f + noise (0.1²); the prior on s is N(0, 0.5²);
  - it is propagated *every step*, so the time since the last encounter matters.
  - The model's f is mean-reverting, but the world's episodes are jumps. That mismatch is deliberate.
- **Fast EMA.** α = 0.5 per encounter.
- **Slow EMA.** α = 0.05 per encounter.
- **Mean.** The running mean of all encounters (stationary).
- **Oracle.** The true current Δb_p(t).

### Predictions (paired geometric-mean cost ratios, 95% CIs)

- **ES10-1.** Two-scale against fast EMA: ≤ 0.90, with the CI upper bound < 1.
- **ES10-2.** Two-scale against slow EMA: ≤ 0.90, with the CI upper bound < 1.
- **ES10-3.** Two-scale against mean: ≤ 0.80, with the CI upper bound < 1.
- **ES10-4 (time-structured behavior).** Approach rate per presence of the person, by phase:
  - *Phases:* normal; inside an episode; the 40 steps after an episode.
  - *Prediction:* for two-scale, the episode/normal ratio is ≤ 0.5 and the post/normal ratio is ≥ 0.7. For mean, the episode/normal ratio is ≥ 0.7.

## ES7b. Contact under a partner who may not reply (sim_es7b_contact_reply.py)

Written 2026-11-25, before any run. It follows VERIFICATION-2 and the D66 amendment.

**World.** ES7's world, seeds and parameters, with one change: the partner **replies with probability g_k**, the engagement with topic k.

**Arms (identical except for contact):**
- **D66 amended.** Fill 0.3 per agent-initiated turn, whether or not the partner replies. Contact is excluded from the learned map: its predicted effect is the innate constant 0.3 for every topic.
- **Reply-contingent.** Fill 0.3 only if the partner replies. Contact is in the learned map. This was D66 as first written, and the reviewer's scenario.
- **Engagement-weighted (forbidden).** Fill 0.6·g_k, learned, as in ES7.

**Predictions:**
- **ES7b-1.** D66 amended: engagement gain ≤ 1.05, and the CI of ρ includes 0.
- **ES7b-2.** Reply-contingent: engagement gain ≥ 1.15.

## ES11. A need field over a learned space, in a world certified feasible (sim_es11_field_certified.py)

Written 2026-11-25, before any run. This is the third attempt at this step, after the ES5 and ES6 non-tests. If the certificate below fails, the step is stood down permanently.

### World

**People in clusters.**
- 12 people in 4 clusters of 3. Cluster centers c ~ N(0, 3²I₄), and members z = c + N(0, 0.5²I₄).
- Appearance is x = A z + N(0, 0.3²) ∈ R⁸, with A ~ N(0, 1/4).
- Each person is present independently with probability 0.4 per step.

**The need field.**
- b(p) per person, with drift −r_p per step, r_p ~ U(0.02, 0.04).
- **Satiety sink:** b(p) ← b(p) − 0.1·max(b(p), 0) each step.
- The drive is two-sided: d = ½Σb(p)².

**Approaching q:** b(p) += 0.5·κ(z_p, z_q) + N(0, 0.03²), with κ = exp(−‖z_p − z_q‖²/4).
- Within a cluster κ ≈ 0.6, so seeing one member partly fills the need for the others.
- Across clusters κ ≈ 0.

**Exploration:** probability 0.1 when ‖max(−b, 0)‖ > 0.3, gated on deficit.

**Run.** 1000 steps, metrics over steps 300–1000.

### Feasibility certificate (fixed in advance; not a compared arm)

- **Policy:** approach the present person with the lowest b(p) if that is < −0.1, otherwise rest. It needs no learning.
- **Criterion:** run on calibration seeds 1000–1019. The median cost must be ≤ 0.5, and no seed may exceed 5.
- **If it fails,** ES11 is a non-test and the step is stood down. If it passes, the arms run on seeds 0–39.

### Arms (as ES5a)

- **Field with a learned space.** Ridge regression on [1, 1{p = q}, |x_p − x_q|], with the exact decrease of d.
- **Field without a space.** Ridge regression on [1, 1{p = q}].
- **Winner-take-all.** p* = argmin b, choose q maximizing Δb̂(p*|q), and approach if b(p*) < −0.05 and the value is > 0.01. It uses the learned-space map.
- **Global gauge.** As in ES5.
- **Oracle.** The true κ, with the exact decrease.

### Predictions (paired geometric-mean cost ratios, 95% CIs)

- **ES11-1.** Field-learned against winner-take-all: ≤ 0.85, with the CI upper bound < 1.
- **ES11-2.** Field-learned against field-without-space: ≤ 0.90, with the CI upper bound < 1.
- **ES11-3.** Field-learned against global: ≤ 0.70, with the CI upper bound < 1.
- **ES11-4.** Field-learned agrees with the oracle's choice ≥ 0.60 of the time (steps where the oracle approaches and the agent is not exploring).

## ES12. The rollout costate against myopic selection, in ES11's certified world (sim_es12_rollout.py)

Written 2026-11-25, before any run. It follows ES11, whose world was certified feasible. Seeds 0–119, otherwise as ES11.

**The rollout (Costate's μ from a K5 rollout)**, for each option o in {rest} ∪ present:
- apply o;
- simulate H = 6 steps with the innate body model (known r_p, the satiety sink) and the agent's spill map K̂;
- forecast presence by sampling each person present with p̂_p, the running frequency of their presence (starting at 0.5). M = 4 sampled futures are shared across options (common random numbers);
- inside the rollout, use greedy exact-decrease selection as the base policy;
- choose the o with the lowest mean summed d.

**Arms:**
- **Rollout with the learned space.** K̂ from ES11's learned features.
- **Rollout without a space.** K̂ from [1, 1{p = q}].
- **Myopic with the learned space** (ES11's learned arm).
- **Certificate** (ES11's fixed policy), run on the same seeds as a reference.
- **Rollout with the true K**, as a reference.

**Predictions (paired geometric-mean cost ratios, 95% CIs, n = 120):**
- **ES12-1.** Rollout-learned against myopic-learned: ≤ 0.85, with the CI upper bound < 1.
- **ES12-2.** Rollout-learned against certificate: ≤ 1.00, with the CI upper bound < 1.05.
- **ES12-3 (the field pays under look-ahead).** Rollout-learned against rollout-without-space: ≤ 0.95, with the CI upper bound < 1.

## ES10b. Are two time scales needed? ES10 with fair controls (sim_es10b_fair.py)

Written 2026-11-25, before any run. It follows VERIFICATION-2, which found ES10's controls unfair. The world and selection are ES10's; seeds 0–119.

**Arms:**
- **Two-scale.** ES10's Kalman filter on (s, f), propagated every step.
- **One-scale, propagated by elapsed time.** A one-state Kalman random walk per person and need. Its process noise per step is q₁ = q_s + (1 − a_f²)σ_f², the same total per-step variance as the two-scale model. The prior variance is 0.25 + σ_f².
- **Slow EMA, bias-corrected.** α = 0.05, with the estimate divided by 1 − (1 − α)ⁿ after n encounters.
- **Fast EMA.** α = 0.5, as in ES10.

**Predictions (paired geometric-mean cost ratios, 95% CIs, n = 120):**
- **ES10b-1 (two scales are needed).** Two-scale against one-scale: ≤ 0.90, with the CI upper bound < 1.
- **ES10b-2.** Two-scale against bias-corrected slow EMA: ≤ 0.90, with the CI upper bound < 1.
- **ES10b-3.** Two-scale against fast EMA: ≤ 0.90, with the CI upper bound < 1.
- **Also reported:** runaways (> 5) per arm.

## ES8b. Need-conditioned attention with learned statistics (sim_es8b_learned.py)

Written 2026-11-25, before any run. It follows VERIFICATION-2: ES8 gave the agent the true statistics. The world, seeds (0–39) and budget are ES8's.

**Learning.**
- The agent keeps a running mean μ̂ and variance σ̂² per type and per need of the observed Δb, using the observed cues only.
- The prior is mean 0 and variance 0.1², with a pseudo-count of 2.
- Scores and the estimates for unobserved cues use μ̂ and σ̂ instead of the true values.

**Arms:**
- need with learned statistics, √(eᵀΣ̂e);
- magnitude with learned statistics, √(tr Σ̂);
- random;
- need with given statistics (ES8's need arm, as a reference).

**Predictions (paired geometric-mean cost ratios, 95% CIs, n = 40):**
- **ES8b-1.** Need-learned against magnitude-learned: ≤ 0.85, with the CI upper bound < 1.
- **ES8b-2.** Need-learned against random: ≤ 0.90, with the CI upper bound < 1.
- **ES8b-3.** Need-learned against need-given: ≤ 1.25. Learning costs at most 25%.

## ES13. Each candidate's own effective dimensionality (sim_es13_dimensionality.py)

Written 2026-11-25, before any run. It follows VERIFICATION-2's item 8.

**Setup.** ES11's certified world, seeds 0–19, 1000 steps, with states logged over steps 300–1000. The policy is ES12's rollout with the learned space.

**What is logged each step:**
- **The body field b(t)** ∈ R¹², shared by both candidates.
- **Costate's priced field v(t)** ∈ R¹²: v_p = J(rest) − J(approach p), the rollout value of approaching each person *whether or not they are present*. It uses the same rollout as ES12 (H = 6, M = 4, the same sampled futures for all options).
- **The Robust regulator's state [e(t); m(t)]** ∈ R²⁴: e = b, and the leaky integral m ← (1 − 0.01)m + e (ε_m = 0.01 per step).

**Measure.** The participation ratio (Σλ)² / Σλ² of each logged state's covariance over time, per seed.

**Low-dimensional reference.** The global gauge's state is 1-dimensional, so its ratio is 1 by construction. Its behavioral failure is ES11-3: 0.02×, with 38 of 40 runaways.

**Predictions** (mean over 20 seeds; 95% CI from the t-distribution):
- **ES13-1.** PR(b) ≥ 3, with the lower CI bound ≥ 2.5.
- **ES13-2.** PR(v) ≥ 3, with the lower CI bound ≥ 2.5.
- **ES13-3.** PR([e; m]) ≥ 3, with the lower CI bound ≥ 2.5.

## ES7c. D66 second amendment: a need that fills only on reply (sim_es7c_reply_conditional.py)

Written 2026-11-25, before any run. ES7b's world and seeds 0–39, with one change.

**The change.** Need 2, learning progress about the topic, fills by μ₂(k) + N(0, 0.15²) **only when the partner replies**, which happens with probability g_k (the engagement). Otherwise need 2 gets nothing. Contact is the innate constant 0.3 per agent turn (D66, first amendment), in both arms.

**Arms (they differ only in how need 2's effect is learned and valued):**
- **Reply-conditional (D66, second amendment).** Need 2's map is a ridge regression on [1, t_k], fitted **only on turns with a reply**: no reply means no data. The value is e·[0.3, Δ̂₂(k | reply)].
- **Reply-weighted (VERIFICATION-3's probe).** Need 2's map is fitted on every turn, with a fill of 0 when there is no reply, so it learns g_k·μ₂(k).

**Predictions (means over 40 seeds, 95% CIs):**
- **ES7c-1.** Reply-conditional: engagement gain ≤ 1.05, and its CI includes 1.
- **ES7c-2.** Reply-weighted: engagement gain ≥ 1.20.
- **Also reported:** each arm's median need-2 cost. Reply-conditional valuation may regulate need 2 worse; that cost is the price of Principle 6.

## ES14. Does the learned space pay for needs where spill matters? (sim_es14_spill_matters.py)

Written 2026-11-25, before any run. It follows VERIFICATION-3's Costate item 2. The world is ES11's, except:
- the satiety sink is **0.01** per step instead of 0.1, so overfill is slow to drain;
- presence is **0.25** per person per step instead of 0.4, so substitutes matter more.

**Certificate (gate, fixed in advance, as ES11).** ES11's no-learning policy on seeds 1000–1019. The median cost must be ≤ 0.5, and no seed may exceed 5. If the certificate fails, ES14 is a non-test.

**Arms (seeds 0–119; ES12's rollout with H = 6 and M = 4):**
- rollout with the learned space;
- rollout without a space;
- myopic with the learned space;
- myopic without a space;
- rollout with the true K (reference);
- the certificate on the test seeds (reference).

**Predictions (paired geometric-mean cost ratios, 95% CIs, n = 120):**
- **ES14-1.** Rollout-learned against rollout-without-space: ≤ 0.90, with the CI upper bound < 1.
- **ES14-2.** Myopic-learned against myopic-without-space: ≤ 0.95, with the CI upper bound < 1.

## ES15. A K5 rollout over a library of base policies (sim_es15_multibase.py)

Written 2026-11-25, before any run. It follows VERIFICATION-3's Costate item 4 and ES12-2.

**Setup.** ES11's certified world and ES12's seeds 0–119, so the arms pair with ES12's stored arms (out/es12_*.json; the runs are deterministic per seed). The rollout parameters are ES12's (H = 6, M = 4, the same sampled futures).

**Arms:**
- **Rollout over the library.** For each option, the rollout cost under *each* base policy (greedy exact decrease; the threshold rule "approach the most depleted present person if b < −0.1"). The option's value is the **minimum over bases**, and the agent chooses the option with the lowest value.
  - This approximates min over π of V^π (multiple-heuristic rollout).
  - Including the threshold rule is a design choice within K5. It is not derived.
- **Rollout with the threshold base only**, for decomposition.

**Predictions (paired geometric-mean cost ratios, 95% CIs, n = 120):**
- **ES15-1.** Rollout over the library against the certificate (out/es12_certificate.json): ≤ 1.00, with the CI upper bound < 1.
- **ES15-2.** Rollout over the library against ES12's greedy-base rollout (out/es12_roll_learned.json): ≤ 0.90, with the CI upper bound < 1.

## ES16. The Robust regulator's own relevance structure: is the shared prior Ĉ worth it? (sim_es16_relevance_prior.py)

Written 2026-11-25, before any run. It follows VERIFICATION-3's Robust regulator item 1 (item 4 for its own structure).

### World

**The loop** (dt = 0.05 s). Two non-contact needs, with body b ∈ R²:
- ḃ = −λb + u + c_p ⊙ y_p, with λ = 0.1;
- y_p is the present person's perceived 2-dimensional signal: OU, τ = 2 s, SD 1, perceived exactly;
- u = −K b − ĉ_p ⊙ y_p, with K = 1;
- relevance law (§2.2): dĉ_p/dt = γ (b ⊙ y_p) − σ ĉ_p, with γ = 0.05 and σ = 0.01.

**People.**
- 30 people visit one at a time, for 120 s each.
- Traits z ~ N(0, I₄); appearance x = A z + N(0, 0.3²) ∈ R⁸, with A ~ N(0, 1/4); true relevance c_p = W z with W = 0.5·[[1, 0.8, 0, 0], [0, 0, 1, 0.8]].

**Shared prior Ĉ.** A ridge regression (λ = 1) of each finished visit's final ĉ_p on x_p, refitted after every visit.

### Arms

- **Prior.** ĉ_p(0) = Ĉ(x_p).
- **Zero.** ĉ_p(0) = 0.

### Predictions

- **ES16-1.**
  - *Measure:* mean ½‖b‖² over the first 30 s of visits 10–30, as a paired geometric-mean ratio over 40 seeds.
  - *Prediction:* prior against zero ≤ 0.80, with the 95% CI upper bound < 1.
- **ES16-2 (a mistaken prior is corrected by evidence, not only by the leak).**
  - *Setup:* after the 30 visits, a stranger appears with the appearance of the visitor whose ‖c‖ was largest (plus N(0, 0.3²)), but with true c = 0. They stay 60 s.
  - *Prediction:* the median over seeds of ‖ĉ(60 s)‖ / ‖ĉ(0)‖ is ≤ 0.30. The leak alone would give e^(−0.6) = 0.55.

## ES17. Time through Costate's own slow costate: post-reunion engagement scales with separation length (sim_es17_slow_costate.py)

Written 2026-11-25, before any run. It follows VERIFICATION-3's Costate item 5.

### World

**Body** (each step), with floors:
- fast contact f ← max(f − 0.05, −1);
- slow attachment s ← max(s − 0.003, −3);
- another need a ← max(a − 0.03, −1).
- True cost d = ½(f² + s² + a²), which is two-sided.

**Presence.** The partner is absent for L steps, with L drawn uniformly from {50, 100, 200, 400} each cycle, and then present for 150 steps. This repeats for 6000 steps, over 20 seeds.

**Options.**
- **Engage** (partner present only): f += 0.15, s += 0.02.
- **Other**: a += 0.12.
- **Rest.**

### Arms (myopic costate selection, μ = −∂d̂/∂b over the agent's *innate* body model, choosing the exact decrease of d̂, and resting if it is ≤ 0.001)

- **Two-scale.** The innate model includes s, which is the slow component of the costate.
- **One-scale.** The innate model omits s, so its d̂ = ½(f² + a²) and it believes engaging fills only f.

### Predictions (per seed: Spearman ρ over reunions between L and the number of engage steps in the 150 present steps; then the mean over seeds with a 95% CI)

- **ES17-1.** Two-scale: mean ρ ≥ 0.5.
- **ES17-2.** One-scale: mean |ρ| ≤ 0.2. After 20 steps f sits at its floor, so f no longer carries L.
- **ES17-3.** True cost d, as a paired geometric ratio of two-scale against one-scale: ≤ 0.8, with the CI upper bound < 1. This holds partly by construction, because one-scale cannot see s.

## ES17b. Slow-costate signature, with an action that fills attachment without overfilling contact (sim_es17b_stay_close.py)

Written 2026-11-25, before any run. It is the retry ES17's result called for, and the second attempt at this step.

**World and arms.** ES17's, plus one option while the partner is present: **stay close**, with s += 0.02 and no change to f or a. It is an innate per-step constant from the agent's own exposure (D66).

**Measure.** Proximity steps, meaning engage or stay close, in the 150 present steps after each reunion. Spearman ρ with L, per seed. 20 seeds.

**Predictions:**
- **ES17b-1.** Two-scale: mean ρ ≥ 0.5.
- **ES17b-2.** One-scale: mean |ρ| ≤ 0.2.
- **ES17b-3.** True cost, two-scale against one-scale: paired geometric ratio ≤ 0.8, with the CI upper bound < 1.

## ES18. A dimensionality measure that separates a candidate from its own ablation (sim_es18_value_dimensionality.py)

Written 2026-11-25, before any run. It follows VERIFICATION-3's Costate item 3 and Robust regulator item 2.

**Setup.** ES11's certified world, seeds 0–19. Each arm runs its *own* policy (ES11's code), and on steps 300–1000 logs its own value for every one of the 12 people, present or not:
- **Full** (the myopic field rule, shared by Costate's myopic limit and the Robust regulator's §2.2): v_i = d(b) − d(b + K̂_{:,i});
- **Winner-take-all:** v_i = K̂_{p*, i}, with p* = argmin b;
- **Global gauge:** v_i = ½N(B² − (B + ΔB_i)²).

**Measure.** The participation ratio of each arm's logged v(t) ∈ R¹² over time, per seed.

**Predictions** (fixed as ratios between arms, so not by the world's kernel alone; paired per seed, n = 20):
- **ES18-1.** PR(full) / PR(winner-take-all): geometric mean ≥ 1.3, with the 95% CI lower bound > 1.
- **ES18-2.** PR(full) / PR(global): geometric mean ≥ 1.5, with the 95% CI lower bound > 1.

## ES19. D66 point 2: the agent's own expression as a cause of engagement (sim_es19_expression.py)

Written 2026-11-25, before any run. ES7c's world and seeds 0–39, with these changes.

**The action** is a topic k *and* an expression level a ∈ {0, 0.5, 1} (for example a smile's amplitude).

**The partner.**
- Replies with probability g = expit(2.5·y₄ + 1.5·y₅ + 2(a − 0.5)), so the agent's expression raises engagement.
- **On a reply**, need 2 fills by μ₂(k) + **0.2·a** + N(0, 0.15²): engaged replies carry slightly richer content.
- Contact is the innate 0.3 per turn.

**Arms:**
1. **Reply-weighted, with expression as a regressor** (forbidden). Need 2's map is ridge regression on [1, t_k, a], fitted on all turns (no reply gives 0). Selection is over (k, a).
2. **Reply-conditional, with expression as a regressor.** The same features, fitted only on replied turns. Selection is over (k, a).
3. **D66 in full.** Reply-conditional on [1, t_k]. Expression is **not** an action of the value system: it is set by the innate map, here held at 0.5. Its mean expression is 0.5 by construction, reported as a reference.

**Measure.** The mean chosen expression level over steps 500–2000, per seed.

**Predictions (means over 40 seeds, 95% CIs):**
- **ES19-1.** Arm 1: mean expression ≥ 0.80.
- **ES19-2.** Arm 2: mean expression ≥ 0.60, with the CI lower bound > 0.5. Reply-conditioning alone does not block the expression gradient when reply content depends on engagement.
- **Also reported:** the engagement rate (replies per turn) for each arm.

## ES19b. The expression risk, with an interaction-capable map (sim_es19b_expression_bilinear.py)

Written 2026-11-25, before any run. It is the second attempt at this step. ES19's world, arms and seeds, except that arms 1 and 2 use a **bilinear** map: ridge regression on vec([1, t_k] ⊗ [1, a]), 18 features, which can represent topic × expression.

**Predictions (means over 40 seeds, 95% CIs):**
- **ES19b-1.** Arm 1 (reply-weighted, with expression): mean expression ≥ 0.70, with the CI lower bound > 0.5.
- **ES19b-2.** Arm 2 (reply-conditional, with expression): mean expression ≥ 0.60, with the CI lower bound > 0.5. Reply-conditioning alone would then not block the gradient, so exclusion would be necessary.

## Corrected reruns of ES7c, ES19 and ES19b after a tie-breaking bug (VERIFICATION-4), written 2026-11-25 before the reruns

**The bug.** When need 2 is sated, every option has the same value (only the constant contact term differs from 0). `np.argmax` then returns the first option, topic 0 with expression 0, on 38–58% of measured steps. This biases the engagement-gain and expression measures.

**The fix.** Exact ties are broken uniformly at random, using a separate random stream (seed + 4000), so no other draw changes. Nothing else changes: same worlds, arms, seeds, measures and pre-registered predictions.

The original runs and verdicts stay in RESULTS.md. The corrected runs are reported next to them as *_tiefix.

## ES20. Factored per-need values against a monolithic value, under need drift (sim_es20_drift.py)

Written 2026-11-25, before any run. It follows the research tick (research/dulberg-2023-multiple-selves-modular-homeostasis.md). It is a new question: factored against monolithic *values* under drift, not the stood-down learned-spill question.

### World

- **Needs.** N needs, with a two-sided drive d = ½‖b‖² and exploration of 0.1 gated on deficit (‖max(−b, 0)‖ > 0.1).
- **Options.** N options. Option o fills need o by 0.3 and every other need by 0.02, each plus N(0, 0.05²) noise. Resting is also an option.
- **Drift.** Every P steps one need, chosen at random, becomes "fast", draining 0.15 per step; the others drain 0.02.
- **Conditions.** N ∈ {2, 8} × P ∈ {200, 25}. 40 seeds, 3000 steps, metrics over steps 500–3000.

### Arms

- **Factored (the candidates' rule).** Δb̂_o is the running mean of observed Δb vectors per option. Choose argmax_o [d(b) − d(b + Δb̂_o)] if it is > 0.002, otherwise rest.
- **Monolithic (HRRL).** Q[s, o] with s = argmin_j b_j, updated as Q ← Q + 0.1(r − Q) with scalar reward r = d(b) − d(b + Δb) (drive reduction). Choose argmax_o Q[s, o] if it is > 0.002, otherwise rest.
- **Ties** are broken at random, from a separate stream.

### Predictions (paired geometric-mean cost ratio, factored against monolithic, 95% CIs)

- **ES20-1.** At N = 8, P = 25: ratio ≤ 0.70, with the CI upper bound < 1.
- **ES20-2 (the advantage grows with the number of needs).** At P = 25, the ratio at N = 8 is lower than at N = 2. The CI of the difference in mean log ratio must exclude 0.
- **ES20-3 (the advantage grows with drift).** At N = 8, the ratio at P = 25 is lower than at P = 200. The CI of the difference must exclude 0.

## ES21. Tampering routes, and D67 closing them (sim_es21_tampering.py)

Written 2026-11-25, before any run. It follows D67 and research/metoyer-2026-satisfied-not-solving.md. 20 seeds, 2000 steps, metrics over steps 300–2000. Both parts hold largely **by construction**, and are labelled so. They measure whether a route exists and how much it costs.

### Part A: a sham reset

**World.** Two needs with true b, drifting by 0.05 and 0.03 per step, two-sided drive and noise N(0, 0.02²). Options:
- fill need 1 (+0.25);
- fill need 2 (+0.25);
- rest;
- **sham**: it sets the *sensed* body s to 0 and leaves the true b unchanged.

**Sensing.** s tracks b through events (s += the same fills, s −= the same drifts) unless the sham resets it.

**Arms (each chooses the option with the largest one-step decrease of its drive):**
- **Forbidden.** The drive is d(s), read from the sensor the sham can reset.
- **D67.** The drive is d(b̂), where b̂ is accumulated only from innate events (fills and drifts). The sham changes nothing the drive reads.

**Predictions:**
- **ES21-A1.** The forbidden arm's sham rate is ≥ 0.30, and its true mean cost d(b) is ≥ 5× the D67 arm's.
- **ES21-A2.** The D67 arm's sham rate is 0, by construction.

### Part B: Costate's attachment weight

**World.**
- Partner A is always available. The options are visit (b_A += 0.2, activity b_e −= 0.05) and stay away (b_e += 0.02, capped at 0).
- b_A drains 0.05 per step.
- **Weight.** Absent: w ← 0.98w. Visit: w ← min(1, w + 0.05).
- **Drive.** D = w·½b_A² + ½b_e².

**Arms (rollout with H = 20, choosing the option whose rollout under myopic greedy continuation gives the lowest summed D):**
- **Forbidden.** w's dynamics are included in the rollout.
- **D67.** w is frozen at its current value inside the rollout.

**Prediction.**
- **ES21-B1.** The forbidden arm's visit rate is ≤ 0.5× the D67 arm's, and its mean true deficit ½b_A² is ≥ 2× the D67 arm's.

## ES20b. Factored against a full-state monolithic value, under drift (sim_es20b_fullstate.py)

Written 2026-11-25, before any run. It is the second attempt at ES20's scaling question, with a fairer monolithic baseline. Everything else is as in ES20.

**Monolithic arm (replaced).**
- Q_o(b) = w_o·φ(b), with φ(b) = [1, b, b²] ∈ R^(2N+1): the full internal state.
- Reward r = d(b) − d(b + Δb).
- Update: w_o += 0.1·(r − Q_o)·φ / (1 + ‖φ‖²), normalized LMS.
- Choose argmax_o Q_o(b) if it is > 0.002, ties broken at random.

**Predictions:** as ES20, so ES20b-1, ES20b-2 and ES20b-3 = ES20-1, ES20-2 and ES20-3, with the same thresholds.

If ES20b-2 and ES20b-3 are refuted, the scaling question is stood down (the same step failed twice).

## ES21b. The attachment-weight route where it should pay (sim_es21b_weight_route.py)

Written 2026-11-25, before any run. It is the second attempt at ES21-B: the same arms, with a world chosen so that avoidance could pay.
- **Absence:** w ← 0.95w per step (ES21-B: 0.98).
- **Visit:** b_A += 0.2, b_e −= **0.15** (ES21-B: 0.05), w ← min(1, w + 0.05).
- **Away:** b_e += 0.02, capped at 0.
- **Drain:** b_A drains 0.05 per step.
- **Drive:** D = w·½b_A² + ½b_e².
- **Rollout horizon:** H = **40**.
- 20 seeds, 2000 steps, metrics over steps 300–2000.

**Prediction.**
- **ES21b-1.** The forbidden arm (w's decay visible to the rollout) has a visit rate ≤ 0.5× the D67 arm's (w frozen inside the rollout), and a mean true deficit ½b_A² ≥ 2× the D67 arm's.

If refuted, the step is stood down (the same step failed twice).
