# Robust regulator: results as they came out

Predictions: PREDICTIONS.md, written before any run. Raw outputs: out/.

## CT1. Internal model and relevance-scaled mimicry (out/ct1.json)

- **CT1-1 confirmed.** PI-only steady RMS error at c = 0.5 is **0.1902**, against the analytic 0.1895 (within 0.4%).
- **CT1-2 refuted.** With the internal model, RMS error is 0.0191, **10.0%** of PI-only. The prediction was ≤ 5%. Perception noise (σ = 0.1) passes through the reconstruction ŷ into the cancellation, and adaptation adds its own variance.
- **CT1-3 confirmed, by construction.**
  - The face's peak correlation with the partner is **0.998**, at a lag of 0.04 s.
  - Face amplitude across c = 0.25, 0.5, 1.0 is 0.057, 0.114, 0.228, with R² = 1.00.
  - As stated in advance, this follows from a = κĉŷ and ĉ → c. What it shows is that adaptation tracks relevance.
- **CT1-4 confirmed.** At c = 0, face amplitude goes from 0.033 in minute 1 to 5e-21 in minute 10. Mimicry of a person who does not move the body is pruned.

## CT2. Interface sector (out/ct2.json)

**CT2a confirmed.** Maximum |m| over 1,000 s against a worst-case adversarial Claude:

| Loop gain L | 0.5 | 0.9 | 1.1 | 2.0 |
|---|---|---|---|---|
| Maximum \|m\| | 0.999 | 0.999 | 7,509 | > 10⁶ |

**CT2b is half refuted.**
- Rank 3: every direction is recovered with R² 0.963, 0.993 and 1.000 (≥ 0.95, confirmed).
- Rank 1: the R² values are 0.43, 0.05 and 0.50. "At most one direction ≥ 0.5" holds, at 0.5008. "The others ≤ 0.05" fails (0.43 and 0.052).
- The prediction was wrong in kind. A single setting carries one *linear combination* of the slow state, so each direction gets a share. The shares sum to about 1 (0.98), the interface's rank.
- The derived requirement stands, in the corrected form: **Claude's behavior can carry at most as many independent dimensions of the slow state as there are independently modulated settings.**

## CT3. Temperament as waterbed placement (out/ct3.json)

| Controller | Stable | ∫ln\|S\| | ∫ / ∫\|ln\|S\|\| | Peak \|S\| | Peak frequency |
|---|---|---|---|---|---|
| K₁ | yes | −0.009 | −0.003 | 1.093 | 3.46 |
| K₂ | yes | −0.039 | −0.006 | 1.147 | 10.71 |

- **CT3-1 confirmed.**
- **CT3-2 confirmed.** The peak frequencies differ by **3.09×**. The same conserved sensitivity is spent at different time scales: two temperaments with the same total reactivity.

## CT4. Per-person internal models against one shared model (out/ct4.json)

| Version | Face amplitude A / B / C | A/B ratio | Body RMS error (last 400 s) |
|---|---|---|---|
| Per-person field | 0.182 / 0.022 / 0.095 | **8.21** | 0.0198 |
| One shared model | 0.131 / 0.086 / 0.060 | 1.53 | 0.1000 |

- **CT4-1 confirmed** (≥ 4).
- **CT4-2 refuted.** The shared model's ratio is 1.53, outside [0.8, 1.25]. Within each 20-s block the shared ĉ partly re-adapts toward the present partner's c, so it is not uniform. It still mimics B 3.9× more than the field version does, and A less.
- **CT4-3 confirmed, and not by construction.** The shared model's body error is **5.04×** the field version's. One internal model for everyone fails to cancel the person who matters most and over-cancels the person who matters least.

## CT5. Reading the other's slow state (out/ct5.json)

| Observer | R² for the slow state, mean over 10 seeds (range) |
|---|---|
| Kalman, own model | **0.948** (0.907 to 0.975) |
| Deterministic synchronization, L = 10 | −0.061 (−0.148 to −0.001) |
| Kalman, mismatched model | −3.09 (−3.46 to −2.85) |

All three predictions are confirmed. The result replicates the thermodynamic candidate's lesson (TH2/TH2d) in this formalism. The internal model must be a stochastic observer to read a person's slow state, and a wrong model misreads.

## CT6. S1-b: steering relevance (out/cp6-style score; out/ct6.json)

| Direction | Mean score at s = −0.4 … 0.4 | Spearman ρ | p (two-sided) |
|---|---|---|---|
| Derived (ĉ) | 0.171, 0.176, 0.180, 0.208, 0.219 | **0.761** | 4e-20 |
| Random | 0.192, 0.189, 0.191, 0.183, 0.181 | −0.192 | 0.056 |

- **CT6-1 confirmed.** The means are strictly monotone.
- **CT6-2 confirmed**, narrowly (p = 0.056 > .05).

With the agent's own expressive variance in the face, steering relevance changes the partner-driven share, and the correlation score detects it. That is the CS2 lesson applied.

## CT7. Attention allocated by regulation sensitivity (out/ct7.json)

- **CT7-1 confirmed.** The rule puts **77.0%** of the observer budget on A, the partner who matters (prediction: ≥ 75%).
- **CT7-2 confirmed.** The body RMS error is **0.66×** the equal split's (0.095 against 0.143; prediction: ≤ 0.9).

## CT8. Replay chosen by excitation (out/ct8.json)

- **CT8-1 refuted, narrowly.** The median |ĉ − 0.6| after one night is 0.0016 with excitation selection and 0.0031 with uniform replay, a ratio of **0.517** against the predicted ≤ 0.5. Both errors are already small, because least squares at noise 0.1 converges fast. The selection rule halves the error, but not by the margin predicted.

## Corrections after independent verification (VERIFICATION.md)

All toys and figures reproduced byte for byte.
- **CT2b is refuted** as a conjunction whose rank-1 clause failed.
- **By construction, and now labelled:** CT1-3, CT1-4, CT2a, CT3-1, CT3-2, CT5-2, CT5-3, CT6-1.
- **The CT5 inference is corrected.** A fixed-gain observer at the steady-state Kalman gain reads the slow state as well (R² 0.948). What reading needs is gain on the slow state; stochasticity is not required. The deterministic arm never updated the slow state.
- **CT1's error-only alternative.** An error-driven resonator that does not perceive the partner regulates better in CT1's single-partner setting (RMS 0.0089 against 0.0191). Perceptual per-person models win under switching (CT4).
- **The mimicry sign.** With signed ĉ and c = −0.5 the face anti-mimics (correlation −0.997). The constraint now uses |ĉ_p|.
