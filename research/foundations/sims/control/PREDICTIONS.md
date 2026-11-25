# Robust regulator (control-theory candidate): toys, parameters and predictions fixed before any run

Written 2026-11-25, before any run. Results go to RESULTS.md. Where a prediction holds by construction, that is said here in advance.

## CT1. The internal model of the other, and mimicry scaled by relevance (sim_ct1_imp.py)

**Setup:**
- dt = 0.01 s, 600 s.
- The partner's face: y_u(t) = sin(1.57t). The agent perceives y = y_u + N(0, 0.1²).
- The body: ḃ = −0.1b + u + c·y_u, with set point 0 and error e = b.
- **PI only:** u = −k_p e − k_I m, with ṁ = e, k_p = 1, k_I = 0.1.
- **Internal model:**
  - The agent reconstructs the partner's face, ŷ, by filtering y through a first-order low-pass with a 0.05 s time constant.
  - It adds the feedforward cancellation u_im = −ĉ ŷ, with ĉ adapted as dĉ/dt = γ e ŷ − σ(ĉ − 0), with γ = 0.5 and σ = 0.001. The innate start is ĉ₀ = 0.5.
- **Face (explicit constraint, Principle 3).** The internal model runs on the agent's own expressive substrate, and the face shows its *reconstruction* weighted by relevance: a = κ ĉ ŷ, with κ = 0.3. The sign comes from the reconstruction, not from the cancellation.

**Predictions:**
- **CT1-1 (analytic).** PI only, c = 0.5: steady RMS error = 0.379·c = 0.190, within ±5%. Derivation: |s/(s² + 1.1s + 0.1)| at ω = 1.57 is 0.536, and 0.536/√2 = 0.379.
- **CT1-2.** With the internal model, c = 0.5: RMS error over the last 200 s ≤ 5% of CT1-1's.
- **CT1-3.**
  - The peak cross-correlation of the face a with y_u is ≥ 0.9, at |lag| ≤ 0.25 s.
  - The standard deviation of a over the last 200 s is linear in c across c ∈ {0.25, 0.5, 1}, with R² ≥ 0.98.
  - *This follows from the constraint a = κĉŷ together with ĉ → c. It tests the adaptation, not the emergence of mimicry.*
- **CT1-4.** At c = 0, with ĉ starting at the innate 0.5, the standard deviation of the face in minute 10 is ≤ 10% of its value in minute 1. Mimicry of someone who does not move the body is pruned.

## CT2. Interface sector: safety and influence for the frozen language model (sim_ct2_interface.py)

**CT2a (safety, small gain).**
- Body error: ė = −e + d. Mood: ṁ = −0.1m + e. Claude's settings: s = g_s m.
- Claude is modelled as an adversarial operator with gain g_C = 1 that chooses the sign of its effect d = g_C|s|·sign(m), the worst case for amplification.
- The loop gain is L = g_s·g_C·(1/1)·(1/0.1) = 10 g_s.
- g_s ∈ {0.05, 0.09, 0.11, 0.2}, which gives L ∈ {0.5, 0.9, 1.1, 2}. m(0) = 1, 1,000 s.
- **Prediction:** |m| stays ≤ 10 for L < 1, and exceeds 100 for L > 1.

**CT2b (influence, observability).**
- The slow state m ∈ ℝ³ is drawn i.i.d. N(0, I), 5,000 samples.
- Claude's observable behavior features (reply length, latency, retrieval breadth and similar) are f = HΓm + N(0, 0.05²), where Γ maps the state to the settings and H maps the settings to behavior.
- **Prediction:**
  - with Γ of rank 3 (three independent settings), every direction of m is linearly recoverable from f with R² ≥ 0.95;
  - with Γ of rank 1 (only the thinking budget varies), at most 1 direction has R² ≥ 0.5, and the others have R² ≤ 0.05.
- *Linear algebra, nearly by construction. It states the interface requirement: k independently modulated settings are needed for k slow dimensions to change Claude's behavior.*

## CT3. Temperament as the placement of the waterbed (sim_ct3_bode.py)

**Setup:**
- The plant is P(s) = 1/((s + 0.1)(0.1s + 1)), of relative degree 2.
- Two stable controllers:
  - K₁ = 1 + 0.5/s;
  - K₂ = 4(s + 0.2)/(s + 2) + 0.2/s.
- S = 1/(1 + KP). The integral ∫₀^{10³} ln|S(jω)| dω is computed numerically.

**Predictions:**
- **CT3-1.** Both closed loops are stable, and both integrals satisfy |∫| ≤ 0.05·∫|ln|S|| dω. That is the Bode integral, zero for an open-loop-stable plant of relative degree ≥ 2, up to truncation.
- **CT3-2.** The frequency of peak |S| differs between the controllers by ≥ 2×. Different temperaments put the amplification at different time scales.

## CT4. Expressive structure: one internal model per person, against one shared model (sim_ct4_people.py)

**Setup:**
- Three partners, A, B and C, present in turn in 20-s blocks, cycling for 1,200 s.
- Each moves the agent's body with c_A = 0.8, c_B = 0.1 and c_C = 0.4. Their face rhythms are at frequencies 1.57, 1.2 and 2.0.
- **Field version:** a separate ĉ_p per partner, each adapted only while that partner is present.
- **Collapsed version:** one ĉ shared across partners.
- Everything else as in CT1.

**Predictions:**
- **CT4-1.** In the last 400 s, the field version's face amplitude toward A divided by its amplitude toward B is ≥ 4.
- **CT4-2.** The collapsed version's ratio lies within [0.8, 1.25].
- **CT4-3 (not by construction).** The collapsed version's body RMS error over the last 400 s is ≥ 1.5 × the field version's. One shared internal model under-cancels A and over-cancels B.

---
# Second batch, written 2026-11-25 before any run of CT5–CT8

## CT5. Reading the other's slow state: stochastic observer against deterministic observer (sim_ct5_observer.py)

**Setup:**
- The partner's state is x = (face f, slow s). ṡ = −s/30 + 0.3ξ_s, and ḟ = −(f − 0.8s)/0.5 + 0.3ξ_f.
- The agent sees y = f + N(0, 0.05²) at 30 Hz, for 10 min.
- The agent's own model is the same linear system (its F and G).
- **Arms:**
  - **(a) Kalman observer** with the correct process noise;
  - **(b) deterministic observer** with gain L on the face only, L = 10 (the synchronization form);
  - **(c) Kalman observer with a mismatched model:** coupling 0.8 replaced by −0.8.
- 10 seeds.

**Predictions:**
- **CT5-1.** (a) recovers the slow state with R² ≥ 0.6.
- **CT5-2.** (b) recovers it with R² ≤ 0.3.
- **CT5-3.** (c) recovers it with R² ≤ 0.

## CT6. S1-b: steering relevance ĉ, when the agent has its own expressive variance (sim_ct6_dose.py)

**Setup:**
- Face a = κ ĉ ŷ + o, where o is the agent's own state-driven expression: OU, 1 s, standard deviation 0.5.
- The partner's face is OU, 2 s, unit variance, with ŷ its reconstruction.
- κ = 0.3, and the baseline ĉ is 0.5.
- **Steering:** ĉ = max(0, 0.5 + s·(u·d)), with s ∈ {−0.4, −0.2, 0, 0.2, 0.4}. Derived direction u, and a random control direction.
- 20 runs per level, 10 min each. Score as CP5.

**Predictions:**
- **CT6-1.** The derived direction gives a Spearman p < .05 one-sided, and the means are monotone.
- **CT6-2.** The random direction gives p > .05, two-sided.

## CT7. Content-dependent attention: observer gain goes where regulation is most sensitive (sim_ct7_attention.py)

**Setup:**
- Two partners are present at once: A (c = 0.8) and B (c = 0.1). Each has a face rhythm at its own frequency.
- The agent has a fixed total observer budget, L_A + L_B = 10, and splits it each second.
- **Rule:** L_p ∝ ĉ_p·(the recent prediction-error variance of p's model).
- **Comparison:** an equal split.
- 10 seeds, 600 s.

**Predictions:**
- **CT7-1.** The rule puts ≥ 75% of the budget on A in the last 300 s.
- **CT7-2.** The rule's body RMS error over the last 300 s is ≤ 0.9 × the equal split's.

## CT8. Replay chosen by excitation, against uniform replay (sim_ct8_replay.py)

**Setup:**
- A store holds 200 episodes of 10 s each, from a partner with true c = 0.6.
- Only 20% of the episodes have the partner's face moving: amplitude 1, against 0.05 in the rest. Those are the informative ones.
- Each night has a budget of 20 episodes. ĉ is updated by least squares on the replayed episodes.
- **Arms:** episodes chosen by the regressor energy Σŷ² (persistence of excitation), against uniform.
- 50 seeds.

**Predictions:**
- **CT8-1.** After one night, the excitation-selected |ĉ − 0.6| is ≤ 0.5 × uniform's, in the median over seeds.
