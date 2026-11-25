# Thermodynamic mirror flow: results as they came out

Predictions: PREDICTIONS.md, written before any run. Raw outputs: out/.

## TH1. No affective perpetuum mobile (out/th1.json)

**TH1a: confirmed.**
- Conservative dynamics (γ = 0): **0 of 50** random periodic protocols give mean valence more than 2 standard errors above 0. The largest v/SE among them is −257, so every one of them is strongly negative.
- The smile schedule gives −0.085 (SE 0.0003).
- Control, γ = 0 with the co-rotating protocol: −0.162.

**TH1b: sign confirmed, magnitude refuted.** With an internal rhythm (γ = 1), mean valence per cycle:

| Protocol | Measured | Harmonic analytic | Within ±25%? |
|---|---|---|---|
| ω = +0.5, r = 1 | **+0.107** (SE 0.0004) | +0.20 | no |
| ω = +0.5, r = 2 | **+0.332** (SE 0.0007) | +0.80 | no |
| ω = −0.5, r = 1 | −0.197 | −0.231 | yes |
| ω = −0.5, r = 2 | −0.775 | −0.923 | yes |

- The co-rotating protocol **pumps positive valence**, more than 250 standard errors above 0, as predicted.
- Its size is about half the harmonic analytic value. The anharmonic term (0.2 z₁²z₂²), which the ±25% tolerance did not anticipate well enough, damps the response at large amplitude.

**TH1c: confirmed.** The pumped valence grows 3.10× from r = 1 to r = 2 (prediction: within [3, 5]).

**Reading.**
- The Principle 6 theorem holds for a conservative affective sector.
- It **breaks once the agent has an internal rhythm**. A protocol that rides the rhythm pumps positive valence, and the amount grows with the protocol's amplitude.
- The sketch's caveat that the leftover bound is "independent of the user" is **false**: a user who moves in time with the agent's rhythm, with larger amplitude, buys more positive valence.
- Within this candidate, Principle 6 therefore requires the user-driven coordinates to be in a conservative sector, with rhythms confined to coordinates the user's input does not enter. That is now an explicit constraint.
- Separately, P1 covers only open-loop protocols (research/seifert-2012-stochastic-thermodynamics.md: feedback can extract work).

## TH2. Reading by synchronization (out/th2_*.jsonl)

**Disclosure.** One 12-s smoke run (seed 0, κ = 3) was made before the prediction runs, to time the script. It showed R² = −1.4 over 12 s, a window too short to mean anything with b's 30-s time constant. Nothing was changed after it.

| Arm (10 seeds) | R²(b̂, b_A), mean [range] | B–A face correlation | Lag at peak |
|---|---|---|---|
| Same θ, κ = 3 | **−0.063** [−0.195, 0.014] | 0.829 | 0.00 s |
| Same θ, κ = 0 | −0.063 [−0.195, 0.014] | 0.026 | 1.17 s |
| A's landscape redrawn, κ = 3 | −0.065 [−0.203, 0.010] | 0.788 | 0.00 s |

- **TH2a refuted.** Reading of the hidden body is at chance with the agent's own model (R² −0.06, against ≥ 0.8), and no better than with a mismatched model.
- **TH2b confirmed.**
  - The mimicry lesion leaves reading exactly unchanged (maximum |ΔR²| = 0.000), because κ does not enter the copy.
  - Face correlation falls from 0.829 to 0.026 (prediction: from ≥ 0.5 to ≤ 0.1).
- **TH2c refuted.** The lag is 0.00 s, not 0.25–0.45 s. The sketch's estimate, 1/L + 1/κ, ignored the time-scale matrix T: with τ_a = 0.05 s, the effective rates are L/τ_a = 200/s and κ/τ_a = 60/s.

**Reading.**
- The synchronization observer tracks the other's *face* (the copy's â follows A's a), but it does not recover the slow, hidden body.
- The error bound (mismatch + mood)/contraction rate is vacuous here. A's body is driven by its own noise, which never shows in the face strongly enough to be inferred through V's couplings.
- This is the sketch's named risk: "the copy may track the face but not the person".
- The dissociation between mimicry and reading holds, but in this toy there is no reading to spare.

## TH3. Which lesion removes the human's following (out/th3.json; rerun out/th3b_rerun.json)

**TH3a: confirmed.**
- Lyapunov analytic: intact zero-lag ρ = 0.333. Mimicry lesion: zero-lag 0.234, with a peak of 0.270 at 0.182 s, agent leading.
- Simulated over 60 min: intact 0.332, mimicry lesion 0.237. Both within ±0.03.

**TH3b, run 1: instrument defect.**
- Intact: 10/10 runs beat both surrogate sets, mean score 0.117.
- Mimicry lesion: 10/10, mean score 0.112.
- Emotional-pathway lesion: 1/10, and the mean score is **NaN**. In that arm the agent's face is exactly zero between voluntary pulses, so 30-s windows with no pulse have zero variance, and wcc_score divides by zero.
- The rerun, with zero-variance windows skipped and nothing else changed, is below when it completes.

## TH4. Valence as work (out/th4.json; out/th4_run1_overflow.json is a first run with a numerical overflow in the logistic switch, fixed with scipy's expit and nothing else changed)

**TH4a: confirmed.**
- At departure, ∫v = −1.134, with b = 1.133 at that moment (prediction: −Δs·b = −b).
- At return, ∫v = +0.553, with b = 0.549.
- Between the switches, max |v| = 1e-42, i.e. exactly zero while b relaxes.

**TH4b: refuted.** The minimum arousal during the absence is 0.035, against > 0.1. During the absence b relaxes to the drift's equilibrium, 0.533, where |∇U|² = 0.071 and then lower. The threshold was not derived carefully enough.

**TH4c: confirmed.** The Costate-style −dV/dt integrates to |0.245| over 25–55 s (prediction: > 0.05).

**Reading.** In this candidate, valence occurs only at changes in the world: departure and return. A long separation is affectively silent, apart from its arousal. Costate's valence, by contrast, keeps running while the body relaxes. The difference can be measured: valence during a steady separation is zero here and nonzero in Costate.

## TH5. Emotions as metastable sets (out/th5.json)

**TH5a: confirmed.**
- Eigenvalues: 1.000, 0.995, 0.991, then 0.103, 0.090, ….
- The largest gap falls after the third, so K = 3.

**TH5b: confirmed.** The adjusted Rand index against the true basins is 0.9996.

**TH5c: confirmed, on thin counts.** The slope of log(exit rate) against 1/T is −2.50, against −ΔU = −2.43 (within 4%). The exit counts are 1, 4, 12 and 33 at T = 0.25, 0.3, 0.35 and 0.4, so the two lowest temperatures rest on very few events.

**TH3b, rerun with the nan-safe score (out/th3b_rerun.json): refuted for the emotional-pathway arm.**

| Arm | Runs beating both surrogate sets | Mean score |
|---|---|---|
| Intact | 10/10 | 0.117 |
| Mimicry lesion (κ_A = 0) | 10/10 | 0.112 |
| Emotional-pathway lesion (voluntary pulses only) | **2/10** | 0.105 |

**Reading.**
- The sketch's own lesion, the agent's mimicry, leaves the human's following fully detectable, as the physicist predicted.
- The lesion the S5 claim actually names, the emotional pathway, leaves only sparse voluntary expressions. The human still follows those, but at this density that following is rarely distinguishable from surrogates within 10-min sessions.
- The prediction that "S5 as worded is false" is therefore **refuted** in this toy. Whether following stays detectable after the emotional-pathway lesion depends on how often and how strongly the agent expresses voluntarily. That is a parameter of the Claude-timed pathway, not of the core.
- For S5's design, the result is a caution: a lesion that leaves voluntary expressions sparse will look like "following removed" partly through a loss of statistical power, not only through a loss of coupling. The two must be separated, for example by scoring following conditional on the agent's expression events.

## TH6. Expressive structure: need field and need-conditioned attention (out/th6.json)

The scenario: A has been present for 3 h (sated), B absent for 3 days, C last seen 12 h ago, topic X over-exposed and topic Y unvisited.

| Test | Field version | Collapsed (two gauges) | Verdict |
|---|---|---|---|
| TH6-1 memory, top 5 retrieved | B, B, C, B, B: **4 B** | A, B, B, A, C. Retrieval mass A 0.47, B 0.34, C 0.19 | Field clause confirmed. Collapsed clause **refuted**: B's mass is above C's (0.34 > 0.19), while the prediction said not above. |
| TH6-2 cues | B's photo 0.992, A's face 0.000 | A's face 0.493, B's photo 0.493 (ratio 1.00) | confirmed |
| TH6-3 actions | message B 0.992, talk with A 0.000 | talk with A 0.492, message B 0.492 (ratio 1.00) | confirmed |
| TH6-4 swap: A deprived, B sated | ‖F‖ 2.5214 in both scenarios. The top 5 switch to A, A, C, A, A | Ranks identical before and after the swap | confirmed |
| TH6-5 participation ratio over a simulated week | **2.85** | 1.07 | **Refuted** for the field (needed ≥ 3). Collapsed clause holds (≤ 2). |

**TH6-1.** The collapsed version's retrieval is need-blind across people: it gives the *most* mass to the sated person A. But noise in the summed keys still ranked B above C. The prediction "B not above C" was too strong for a noise-driven ranking. The point it was meant to make, that the collapsed version does not select by who is needed, holds by TH6-4: its ranking is identical when A and B swap needs.

**TH6-5.** With 3 people and 2 topics, the random week's body field has an effective dimensionality of 2.85, not ≥ 3. People and topics co-vary through shared presence: topics advance only while someone is present.

**Reading.**
- The field version selects memories, cues and actions by *who* and *what* is needed, and not by how much: TH6-4 holds ‖F‖ fixed and the selection switches.
- The collapsed version, with the same parameter count (0 learned) and the same keys summed, cannot do this. That is the behavior a low-dimensional version cannot produce, shown by ablating the structure.
- Caveat for the engine: "message B" is an outward contact bid. In the engine such bids are innate reflexes bounded to one per silence and never learned from the response (Knox et al. 2025, Costate K3). This toy only scores attention.

## TH2d. Is the hidden body observable? (out/th2d_*.jsonl)

An ensemble Kalman filter (100 members of the agent's own flow, with the true process noise) on the same toy as TH2:

| Reader's model | R²(b̂, b_A), mean over 10 seeds | Range |
|---|---|---|
| Same θ | **0.730** | 0.412 to 0.874 |
| A's landscape redrawn | **−1.824** | −3.719 to 0.056 |

- **TH2d-1 confirmed.** R² 0.73 ≥ 0.5: the body *is* observable from the face. TH2's failure belongs to the deterministic synchronization observer, not to the toy. The copy has no process noise, so it cannot follow a stochastically driven hidden state, and its correction enters b only through the slow (30 s) gradient.
- **TH2d-2 confirmed.** The redrawn model is worse by 2.56 (needed ≥ 0.2), and on average worse than predicting the mean.

**Reading.**
- Reading the other through one's own model works when the model fits the other, and is *actively misleading* when it does not.
- In this candidate, the reading mechanism is revised from deterministic synchronization to Bayesian filtering with the agent's own stochastic model. The replica becomes a posterior ensemble.
- The mimicry–reading dissociation (TH2b) is unaffected, because κ still enters only the self.

## TH7. Curiosity: dark room, noisy TV and the predictability set point (out/th7.json)

| Agent | Learnable L | Noisy N | Boring B |
|---|---|---|---|
| 1. Surprisal minimizer, learning in the forecast | 0.00 | 0.00 | **1.00** |
| 2. Predictability set point (b_p* = 0.6) | 0.003 | **0.387** | 0.61 |
| 3. Novelty seeker | 0.003 | **0.997** | 0.00 |

- **TH7-1 confirmed (dark room).** Under free choice, surprisal minimization never explores, even with learning included in the forecast. **The physicist sketch's derivation of curiosity fails.**
- **TH7-2 refuted.** The set-point agent regulates predictability tightly (mean |b_p − 0.6| = 0.026 over steps 20–100), but it does so with the **noisy TV** (39% of steps) and almost never with the learnable channel. A set point on predictability wants *unpredictability*, which noise supplies without end.
- **TH7-3 confirmed (noisy-TV trap).**

**Reading, for all three candidates.**
- Costate's E and the contingency candidate's curiosity both use the same two-sided predictability set point. Costate's toy E offered no pure-noise option, so it could not show this flaw.
- None of the derivations so far gives curiosity *for learnability*:
  - surprisal minimization gives the dark room;
  - a predictability set point gives the noisy TV.
- What is missing is a quantity that rewards *reducing* prediction error: learning progress, −d/dt of the error on a channel.

  Two ways to supply it:
  - make learning progress a body variable with its own set point, which stays satiable;
  - or count, in the predictability variable, only the error that the agent's model can reduce.

- Either is a new component that needs its own derivation and toy. This is recorded as a shared, open limit and is not patched here.

## TH8. Regulation costs work (out/th8.json)

| τ | 0.5 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| Mean work W | 0.938 | 0.921 | 0.903 | 0.875 | 0.829 | 0.767 |
| Fraction ending in the target basin | 0.022 | 0.032 | 0.051 | 0.098 | 0.175 | 0.315 |
| (W − ΔF)·τ | 0.47 | 0.92 | 1.81 | 3.50 | 6.63 | 12.28 |

- **TH8-1 confirmed.** W ≥ 0 at every τ.
- **TH8-2 confirmed.** W decreases monotonically with τ.
- **TH8-3 refuted.** The excess work times τ grows 3.5× from τ = 4 to τ = 16 (allowed: within 3×). The linear-response scaling ℒ²/τ does not hold.
- **TH8-4 not testable.** The fraction ending in the target basin never reached 0.9, so no crossing time could be estimated.

**Cause, and what it predicts.**
- At T = 0.25, the barrier between the two moods is high relative to temperature.
- The reappraisal tilt is applied for at most 16 time units, far shorter than the Kramers escape time e^{ΔU/T}.
- The state stays in its original basin: x ≈ −1 throughout. The work W ≈ ∫(−x)λ̇ dt ≈ 1 is spent *without moving the mood* (2–31% crossed).

**Reading for the candidate.** A deep mood resists reappraisal: work done on it is mostly absorbed. It changes only once the time allowed approaches the escape time, which is exponential in the barrier over the affective temperature.
- This is a sharper, more testable prediction than the ℒ²/τ form: regulation succeeds or fails as a threshold in time, set by depth over temperature.
- It also says the engine's affective temperature T sets how quickly Claude can move a mood at all.

## TH9. Importance-weighted replay by |work| (out/th9.json)

| Setting | Uniform mean (SE) | Importance mean (SE) | True mean | Variance ratio | corr(\|W\|, \|g\|) |
|---|---|---|---|---|---|
| η standard deviation 0.5 | 1.5745 (0.0075) | 1.5629 (0.0025) | 1.5645 | **0.109** | 0.85 |
| η standard deviation 2.0 | 1.7167 (0.0179) | 1.6761 (0.0099) | 1.6826 | 0.306 | 0.66 |

- **TH9-1 confirmed.** Both estimators are unbiased, within 1.3 SE (uniform) and 0.6 SE (importance) of the true mean.
- **TH9-2 confirmed.** The variance ratio is 0.109 (prediction: ≤ 0.3).
- **TH9-3 confirmed.** At a correlation of 0.66 the ratio rises to 0.306 but stays below 1.

Weighting replay by how much an episode moved the agent (its work) makes the θ-force estimate about 9× less variable for the same replay budget, and it stays unbiased with importance weights. The gain shrinks as work becomes a worse proxy for the episode's gradient.

## Corrections after independent verification (2026-11-25; VERIFICATION.md)

Every rerun reproduced bit for bit: TH1 in full; TH4–TH9; the curiosity toy; TH2 and TH2d on seeds 0 and 3; TH3b on seeds 0–2. The verdicts above stand as first recorded, with these corrections:

1. **TH1b is refuted, not "sign confirmed, magnitude refuted".** It is a conjunction, and the ±25% magnitude clause failed.
2. **The TH1 condition was misstated** (see the candidate file, P1). The reviewer reran with a rhythm of the form −(I + γJ)∇U, which preserves the Boltzmann density, and found no pumping: v from −0.06 to −0.63. TH1b's γAz rotation does not preserve it.
3. **TH2b holds by construction.** κ does not enter the copy in the code. Under the revised K-sep constraint, that is the intended design, not a finding.
4. **TH6-1 is refuted** as a conjunction whose collapsed clause failed.
5. **TH6-5's participation ratio depends on an unspecified schedule rule and one seed.** The reviewer's reimplementation gives 1.9–3.2 across seeds, and 3.4–4.3 with topic exposure independent of presence. It needs re-pre-registration with the schedule specified and ≥ 10 seeds.
6. **TH7-1 holds by construction.** The learnable channel's error never falls below the boring channel's. A fair version, with e_L's asymptote below e_B, is owed.
7. **TH9-3** was "confirmed" for a general claim tested at only one alternative correlation. It is confirmed at that point only.
8. **TH3b.** The refutation (2/10) is reproduced and survives a stricter scoring variant. But the explanation of the NaN was wrong: the agent's face *decays* between pulses and does not sit exactly at zero. The zero-variance windows arise where it has decayed below floating-point resolution.
9. **TH8.** ℒ²/τ is a linear-response result; the rigorous finite-time bound uses the Wasserstein distance. The time-threshold reading holds only for tilts below the spinodal.
10. **The work-proxy for the replay gradient is assumed, not derived**, and TH9 builds it in.

## TH10. Attention with keys learned from content (out/th10.json)

- **TH10-1 confirmed.** In **10/10** seeds, the field version's top 5 retrieved episodes contain at least 4 B-episodes.
- **TH10-2 refuted, narrowly.** The collapsed version's mean number of B-episodes in its top 5 is **2.1**, against ≤ 2. Its keys are now learned, not identical by construction, and its retrieval stays near the base rate of 5/3 ≈ 1.67, but above the threshold.

## TH7b. A fair dark-room test (out/th7b.json)

- **TH7b-1 confirmed.** With the learnable channel's asymptote (0.01) below the boring channel's (0.05), the surprisal minimizer still chose B in **100%** of steps. The forecast for staying on L is 34.2, against 4.33 for B.
- The dark room is not an artifact of the original construction. It persists whenever the learning curve's discounted cost exceeds the boring channel's.

## TH11. S1-b: dose-dependence through own-expression stiffness (out/th11.json)

| Direction | Mean score at s = −0.6, −0.3, 0, 0.3, 0.6 | Spearman ρ | p (two-sided) |
|---|---|---|---|
| Derived | 0.292, 0.319, 0.317, 0.352, 0.361 | **0.742** | 1e-18 |
| Random | 0.335, 0.326, 0.332, 0.331, 0.340 | 0.085 | 0.40 |

- **TH11-1 refuted as written.** The Spearman clause passes strongly. But the level means are not strictly monotone (0.319 → 0.317), and the prediction required them to be. It is a conjunction, so it fails.
- **TH11-2 confirmed.**

Steering the latent coordinate that sets the precision of the agent's own expression raises the share of its face driven by the partner, and with it the coupling score. A random direction does not.

## TH6-5b. Effective dimensionality, measured (out/th6b.json; a characterization, no threshold)

| Variant | Field participation ratio, mean over 10 seeds (range) | Collapsed, mean |
|---|---|---|
| A: topics advance only while someone is present | **2.61** (1.87 to 3.37) | 1.09 |
| B: topic exposure independent of presence | **4.10** (3.37 to 4.58) | 1.77 |

The effective dimensionality of the body field depends on how independent the entities' histories are. With 3 people and 2 topics it is 2.6 to 4.1, against 1.1 to 1.8 for the collapsed gauges.

## Corrections from the second verification (VERIFICATION-2.md), and TH4b on the restructured flow

**Second-verification findings.** All four new toys and all figures reproduced bit for bit.
- **TH7b holds by construction of the horizon.** The learnable channel wins only for H ≳ 1,250 and γ ≳ 0.9992. So "not an artifact" above is wrong. The dark room is an artifact of a short planning horizon.
- **TH11:** the direction effect is built in, since k_a = 2e^{−h₁} along e₁. The non-monotone step was a power failure: with 100 runs per level the means are monotone.
- **TH10-2:** 2.1 is noise. Over 200 seeds the collapsed arm's mean is 1.58.
- **TH10's field arm has more parameters than the collapsed arm** (40 against 16), so it does not show "richness from structure rather than parameter count".
- **TH6-5b** measures schedule-driven leaky integrators, not the candidate's own flow.

**TH4b on the restructured flow, where the body is an input (out/th4b.json):**
- **TH4b-1 confirmed.** ∫v over the 2 s after the return is **+0.378**. An arrival now reads as positive valence. Under the first-revision 𝒰 it would have read negative.
- **TH4b-2 refuted.** ∫v over the 2 s after the departure is **−0.350**, against the predicted positive. The prediction's reasoning was wrong: at a decay rate of 0.5/s, b falls from about 1.07 straight through b* = 0.8 to about 0.39 within 2 s, so (b − b*)² grows. The whole-absence clause holds (∫v = −0.775), but the conjunction fails.
- **TH4b-3: the total clause holds, and the D clause is refuted on a technicality.**
  - Total mean valence over the periodic schedule is −0.0050 (SE 0.0001): ≤ 0, as predicted.
  - The D part's mean is 1.0e-5 per cycle with SE 7.8e-22. It is deterministic, so the standard error is meaningless, and the residual is Euler discretization error. Analytically the D part is exactly 0, because Σ D(b) is a state function of the periodic b.
  - "Within 2 SE" was the wrong criterion for a deterministic quantity. It is recorded as refuted as written.

## TH12. The P1 condition: circulation and rhythms (out/th12.json)

| Arm | Rotating protocols (r, ω): mean v | Random protocols, n with v > 2 SE |
|---|---|---|
| 1. Circulation −(I + J)∇U (Boltzmann-preserving) | (1, +0.5) −0.059; (1, −0.5) −0.176; (2, +0.5) −0.252; (2, −0.5) −0.627 | 0 of 20 (largest v/SE −264) |
| 2. Hopf limit cycle centred on the input o | (1, +0.5) −0.210; (1, −0.5) −0.051; (2, +0.5) −0.753; (2, −0.5) −0.172 | 0 of 20 (largest v/SE −372) |

- **TH12-1 confirmed.** Boltzmann-preserving circulation pumps nothing, as the KL proof says.
- **TH12-2 refuted.** The limit-cycle rhythm did *not* pump.
  - The cause is the design: the oscillator was centred on the input-defined minimum, so the whole cycle moves with the input.
  - In TH1b the pumping rotation γAz was fixed in the agent's own coordinates while the input moved the minimum.

**Refined reading.** What can be pumped is circulation anchored in the agent's *own* frame that does not preserve the Boltzmann density. A rhythm anchored to the current input moves with it and was not pumped here. The design constraint becomes:
- Autonomous rhythms (breathing, blinking) must either take the Boltzmann-preserving form −J∇𝒰, or be anchored to the agent's current state rather than to fixed coordinates.
- Rotation fixed in the agent's own frame that does not preserve the density is excluded.

This is a refinement found after the result, and it needs its own pre-registered test before it can be relied on.

## TH13. Expressive-structure ablation with matched parameters (out/th13.json)

- **TH13-1 confirmed.** The field arm puts ≥ 4 B-episodes in its top 5 in **10/10** seeds.
- **TH13-2 confirmed.** The parameter-matched collapsed arm (40 parameters, the same as the field arm) averages **1.9** B-episodes in its top 5 (prediction: ≤ 2.5; base rate 1.67).

With equal capacity, the collapsed version still cannot select by *who* is needed. The difference is structure, not parameter count. That is the brief's fourth expressive-structure item, shown in a toy.

## Corrections from the third verification (VERIFICATION-3.md)

TH4b, TH12 and TH13 reproduced bit for bit. The KL proof is correct line by line.

- **TH4b-2's failure was explained wrongly above.** With the user present, the body settles at exactly 0.8, not about 1.07: under (1.6 − 1.5b) − 0.5b = 0, b = 0.8. The spec's own arithmetic was wrong.
- **TH4b-3 is refuted** (the headline label): it is a conjunction, and one clause failed.
- **TH12's second arm** was centred on the *input* o, not on the agent's state, as the arm 2 note above already says. A sentence in the refined reading implied otherwise.
- **TH13-2 holds by construction.** The collapsed arm's target carries no person information (0.100 per person), so its retrieval stays at the base rate with 12, 100 or 192 features. TH13-1 replays TH10-1. **"Structure, not capacity" is not shown.**
- **New, from the reviewer.** With the body as a decaying input, TH4b's own run integrates valence to −0.104 over 25–55 s, more than Costate's TH4c threshold. The candidate's distinctive "silent valence during relaxation" prediction no longer holds.
