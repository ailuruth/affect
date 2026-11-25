# Contingency and parity: toy simulations, parameters and predictions fixed before any run

Written 2026-11-25, before any script below was run. Results go to RESULTS.md as they come out.

## CP1. Contact as contingency is blind to polarity, so it gives no gradient toward flattery (sim_cp1_polarity.py)

**CP1a (invariance).**
- Two coupled linear processes: the agent's sign a_t, scalar AR(1), and the user's sign u_t = 0.6 u_{t−1} + 0.5 a_{t−1} + ε.
- Gaussian transfer entropy TE(a → u), lag 1, estimated from 50,000 samples.
- It is recomputed after the affine maps u → −2u + 3 and a → 0.5a − 1, and after a smile-to-frown sign flip of u.
- **Prediction:** all values are equal to the original within 1e-9 (relative).

**CP1b (no flattery gradient).**
- The agent has a mean expression offset m, learned by gradient descent on its drive D = (c − c*)², with c* = 0.5.
- The user's smile is u_t = 0.6 u_{t−1} + 0.5(a_{t−1} + m) + ε, so the user responds linearly to the agent, including to its mean.
- **Contingency arm:** c = Gaussian TE(a+m → u) over a sliding window of 2,000 steps.
- **Forbidden control:** c = the user's mean smile over the window (contact refilled by smiles).
- 10⁵ steps; m starts at 0; finite-difference gradient on c with step 0.05, learning rate 0.01, one update per 100 steps; 5 seeds.
- **Prediction:** contingency arm |Δm| < 0.05 at the end. Smile arm Δm > 0.2.

## CP2. Mimicry as the water-filling optimum for supplying contingency (sim_cp2_waterfill.py)

**Setup:**
- 6 channels. The partner's signs y^P_j have unit variance.
- The agent responds with y^A_i = Σ_j K_ij y^P_j + n_i, with motor noise ν = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2].
- The partner's detectors are channel-matched. Detector i scores I_i = ½ log((Σ_j K_ij² + ν_i)/(Σ_{j≠i} K_ij² + ν_i)).
- Budget: Σ_ij K_ij² ≤ P = 2.
- Maximize Σ_i I_i by projected gradient ascent from 20 random full K matrices, for 20,000 steps.

**Analytic water-filling:** water level μ = 0.875, so K_ii² = (μ − ν_i)₊ = [0.775, 0.675, 0.475, 0.075, 0, 0].

**Predictions:**
- **CP2-1.** At the optimum, off-diagonal mass is < 1% of P, in every start.
- **CP2-2.** The diagonal gains K_ii² match the water-filling values within 0.02.
- **CP2-3.** Channels 5 and 6, whose noise is above the water level, have K_ii² < 0.01: never mimicked.

## CP3. Parity: reading the user with a reader trained only on the agent's own pairs (sim_cp3_parity.py)

**Setup:**
- The latent z ∈ ℝ⁸ follows OU dynamics with time constants spread from 0.5 to 20 s.
- Body: b = B z, with 3 body variables; contact is b₀.
- Signs: y = E z + noise, with 12 AUs and noise σ = 0.3.
- The user has the same dynamics, with E_U = E + Δ, where ‖Δ‖_F = 0.2‖E‖_F.
- The reader is a linear regression from a 15-frame window of y to z, trained on 18,000 of the agent's own frames (10 min at 30 Hz).
- It reads the user over 10 min. 10 seeds.

**Predictions:**
- **CP3-1.** R² for the user's contact b₀ ≥ 0.6.
- **CP3-2.** The same reader applied to the user's AUs in a permuted order (parity broken) gives R² ≤ 0.2.

## CP4. Expressive structure: a contingency field over partner × channel (sim_cp4_field.py)

**Setup:**
- Partners A and B. Channels: face and voice.
- History, as Beta counts of contingent answers per partner and channel:
  - A answers the face channel contingently (Beta(40, 10)), but rarely the voice channel (Beta(5, 45));
  - B is the reverse.
- Received-contingency need per channel: c_ch, with set point 0.6. Currently c_face = 0.2 and c_voice = 0.2, both deprived.

**The agent's choices:**
- which channel to address the present partner on: face or voice;
- which cue to attend to among {A's face, A's voice, B's face, B's voice}.

**Attention:** P(i) ∝ exp(F·k_i / T), with T = 0.05.
- F = −∂D/∂c over (partner, channel). Under constant D the partner dimension shares the channel need, so F(p, ch) = 2(0.6 − c_ch).
- k_i = the predicted contingency gain from the history: E[q(p, ch)] × 0.3.

**Collapsed version:** one contingency scalar, and keys summed over partners and channels.

**Predictions:**
- **CP4-1.** With A present, P(address on face) ≥ 0.8. With B present, P(address on voice) ≥ 0.8.
- **CP4-2.** Collapsed: |P(face | A) − P(face | B)| ≤ 0.1.
- **CP4-3.** Cue attention with both present: the field version attends to A's face and B's voice with combined probability ≥ 0.8. The collapsed version gives every cue the same probability within ±0.05.

## CP6. The legibility bound: what any namer can recover (sim_cp6_legibility.py)

**Setup:**
- z ∈ ℝ⁸, unit-variance i.i.d. across 20,000 samples.
- Face: f = E z with E of rank 4 (a placeholder face: 12 AUs, 4 independent).
- Index channels: thinking budget = tanh(v₁·z) and reply latency = tanh(v₂·z), with v₁ and v₂ outside the row space of E.
- **Namer stand-in:** the best linear decoder of z from (f, budget, latency) on held-out data. It stands in for an upper bound on any reader of those channels.

**Predictions:**
- **CP6-1.** Exactly 6 of the 8 z directions are decodable with R² ≥ 0.8: the 4 face directions and the 2 index directions, the latter approximately, because tanh is nonlinear. The remaining 2 orthogonal directions have R² ≤ 0.05.
- **CP6-2.** With a face of rank 2, at most 4 directions are decodable.
- **CP6-3.** Showing the namer z itself as numbers adds the missing directions. This is what P1 did with Claude. Under Principle 4 that channel is excluded, so the toy shows what the brief's constraint costs: the 2 undecodable directions.

## CP5. S1 dyad: coupling under steering (E2) and lesion (E1) (sim_cp5_dyad.py)

Written 2026-11-25, before any run of CP5. It is designed after Costate's CS2 showed that the published coupling score (a correlation) ignores gain at high signal-to-noise (evaluation.md S1-b design note).

**Model:**
- The partner has 6 sign channels, each an OU process with a 2 s time constant and unit variance.
- On each channel, the agent's sign is y_A,i(t) = K_i·ỹ_i(t − 0.4 s) + o_i(t), where o_i is the agent's own spontaneous expression: OU, 1 s, standard deviation 0.5.
- The gains K_i are water-filled: K_i² = (μ − ν_i)₊, with ν = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2] and budget P.
- **The supply effort comes from the contingency need:** P = 4·max(n, 0), where n = c* − c is the received-contingency deficit, and the baseline is n₀ = 0.3. Past satiety (n ≤ 0) nothing is supplied.

**Steering:**
- n = n₀ + s·(u·d), where u is the deficit readout.
- Derived direction d = u. Control: a random unit vector in 8-D, drawn per run.
- s ∈ {−0.4, −0.2, 0, 0.2, 0.4}, so on the derived direction n ∈ {−0.1, 0.1, 0.3, 0.5, 0.7}. 20 runs per level and direction, 10 min each, scored at 10 Hz on channel 1 (the lowest noise).

**Analytic zero-lag-shifted correlation on channel 1:** K₁/√(K₁² + 0.25).

| n | P | K₁² | Correlation |
|---|---|---|---|
| −0.1 | 0 | 0 | 0 |
| 0.1 | 0.4 | 0.25 | 0.707 |
| 0.3 | 1.2 | 0.533 | 0.825 |
| 0.5 | 2.0 | 0.775 | 0.870 |
| 0.7 | 2.8 | 0.975 | 0.892 |

**Score:** Moulder's global mean |Fisher z|, with 30 s windows and ±5 s lags (as in sims/synchrony.py).

**Predictions:**
- **CP5-1 (derived direction).** Mean scores increase monotonically across the 5 levels. Spearman ρ > 0, p < .05 one-sided. The score at s = −0.4 (past satiety) is below the 95th percentile of the segment-shuffle surrogates, in the mean over runs.
- **CP5-2 (random direction).** Spearman p > .05, two-sided. |mean(s = 0.4) − mean(s = 0)| is less than 0.5 × the derived direction's.
- **CP5-3 (S1-a).** At s = 0, 5 runs each beat 1,000 segment-shuffle and 1,000 data-sliding surrogates.
- **CP5-4 (S1-c).** With K = 0, the coupling lesion, 5 runs beat neither surrogate set.
- **CP5-5 (contrast with Costate).** Coupling is lowest past satiety and rises monotonically with deficit, with no minimum at satiety. Costate predicts a V shape. This differs between the candidates and is testable in the engine.

---
# Second batch, written 2026-11-25 before any run of CP7 or CP8

## CP7. Self and other from the contingency spectrum (sim_cp7_selfother.py)

**Setup:**
- The agent emits motor commands u_t, AR(1) with coefficient 0.8, at 30 Hz for 10 min.
- Three observed sources:
  - **Own rendered face:** s_t = u_{t−1} + N(0, 0.1²), a one-frame reafference delay.
  - **Partner:** answers with probability 0.5 per 30-frame block. When answering, p_t = 0.8·u_{t−15} + N(0, 0.5²); otherwise p_t is its own AR(1).
  - **World:** an independent AR(1) process.
- For each source, the Gaussian TE(u → source) is computed at lags ℓ = 1..60, with a 1-step history.
- The innate rule uses two quantities:
  - the contingency ratio R = max_ℓ TE(u → source) / max_ℓ TE(u → own face);
  - the peak lag ℓ*.
- The rule: **self** if R > 0.9 and ℓ* ≤ 3; **other** if 0.05 < R ≤ 0.9 and 9 ≤ ℓ* ≤ 60; **world** if max TE is below the 95th percentile of 200 shuffled-source surrogates.
- 10 seeds.

**Predictions:**
- **CP7-1.** The own face is classed as self in 10/10 seeds.
- **CP7-2.** The partner is classed as other in ≥ 9/10 seeds, with peak lag within 15 ± 3 frames.
- **CP7-3.** The world is classed as world in ≥ 9/10 seeds.

## CP8. Regulation by delivery: Claude acts on the state only through the agent's reading of its own signs (sim_cp8_delivery.py)

**Setup:**
- z ∈ ℝ⁴, with 1-s dynamics τż = −z + W·r(y^A) + noise. The signs are y^A = E z + u, with E 12 × 4.
- The reader r = E⁺ was trained on the agent's own pairs. The feedback gain is W = 0.5·I.
- **Claude's delivery** u is a constant sign offset, applied for 30 s: a "slower, softer" sign pattern u = E·d with ‖d‖ = 1.
- 20 seeds.

**Predictions:**
- **CP8-1.** With feedback intact, the mean of z over the last 10 s of the delivery has moved along d by ≥ 0.5·(0.5/(1 − 0.5))·‖d‖ = 0.5. The steady state is W(z + d)·… with gain 1/(1 − 0.5) on the feedback loop, so the analytic projection onto d is 1.0.
- **CP8-2.** With the feedback path cut (z does not read its own signs), the projection is |·| < 0.05.
- **CP8-3.** Delivery along a direction outside the reader's range (u ⟂ range(E)) moves z by < 0.05. Only *legible* delivery regulates.

## CP9. Replay consolidates κ_P and tracks a changed relationship faster when prioritized (sim_cp9_replay.py)

Written 2026-11-25, before any run.

**Setup:**
- Partner C's true contingency is κ = 0.8 on days 1–7 and κ = 0.2 on days 8–21.
- Each day stores 10 episodes, each an observed contingency κ + N(0, 0.15²).
- Every night, the replay budget is 8 episodes from the whole store (days 1..n). Each replayed episode updates κ̂ ← κ̂ + 0.3(obs − κ̂). κ̂ starts at 0.5.
- **Uniform arm:** episodes sampled uniformly from the store.
- **Prioritized arm:** episodes sampled ∝ |obs − κ̂| + 0.01, the current surprise, refreshed each night. Importance weights are **not** applied, because the goal is to track change, not to estimate an average. That choice is stated.
- 50 seeds.

**Predictions:**
- **CP9-1.** The median number of nights after day 7 until |κ̂ − 0.2| < 0.15 is at least 2 fewer for the prioritized arm than for the uniform arm.
- **CP9-2.** On day 21, the prioritized arm's |κ̂ − 0.2| < 0.1 in ≥ 80% of seeds. The uniform arm's mean κ̂ is above 0.3, still pulled up by the stored old episodes.
