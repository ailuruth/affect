# Costate toy simulations: results as they came out

Each prediction is in PREDICTIONS.md, written before the run. Raw outputs are in out/.

## D. Do-conditioning (sim_d_doconditioning.py, out/d.json): all predictions confirmed

Mean learned display over 10 seeds, with its SD and the analytic optimum:

| Reader | α = 0 | α = 0.05 |
|---|---|---|
| Naive | 1.031 (SD 0.014; analytic 1.034) | 1.083 (0.011; 1.085) |
| Do-conditioned | −0.001 (0.024; 0.000) | 0.241 (0.024; 0.247) |
| Miscalibrated (κ̂ = 0.2) | 0.468 (0.023; 0.476) | — |

Every value is within ±0.05 of its prediction. With the echo removed, policy-gradient learning finds no value in displaying more than genuine contagion warrants.

## A. Satiation and invariance (sim_a_satiation.py, out/a.json): all predictions confirmed

- **A1.** The minimum second difference of V along b is +1.0e-6 (prediction: ≥ −1e-4). V is convex on the grid.
- **A2.** The largest increase of μ_b between neighbouring b cells is −5.1e-5, so μ_b never increases (prediction: ≤ 1e-4).
- **A3.** The homeostatic agent bids in 0 policy cells and 0 trajectory steps with b ≥ 0.9. Its mean b over the last 24 h is 0.648 (prediction: in [0.6, 0.9]).
- **A4.** The contact maximizer's mean b over the last 24 h is 2.304. That is 3.55 times the homeostatic agent's (prediction: ≥ 1.2× and > 1.0).
- **A5.** Rescaling the body units by diag(10, 0.1) changes valence by a relative error of 2.8e-14 and arousal by 1.1e-13 (prediction: ≤ 1e-9). The raw ‖μ‖ changes by a factor between 7.7 and 9.9 (prediction: more than 10% from 1). This is the covector law.

The homeostatic agent's mean contact, 0.648, sits below its set point of 0.8. That was not predicted beyond the [0.6, 0.9] band. It follows from the bid's energy price: a bid is worth making only once μ_b·3 exceeds μ_e·0.5.

## C. Mimicry as shrinkage (sim_c_mimicry.py, out/c.json): all predictions confirmed

- **C-M1.** The step-response gains match w s²/(c + w s²) to a maximum absolute error of 6.0e-8. The gains are 0.0099, 0.083, 0.200, 0.360, 0.500, 0.610, 0.692 and 0.800 for s = 0.1 to 2.
- **C-M2.** The gain orthogonal to range(G) is 7.6e-17.
- **C-M3.** The s = 1 mode is 99.0% complete at 500 ms (prediction: ≥ 95%).
- **C-M4.** At s = 0.5, the gain at w = 4 is 3.40 times the gain at w = 1 (prediction: ≥ 2).
- **C-M5 (E3).** The score is Moulder's global mean absolute Fisher-z over 30 s windows and ±5 s lags, tested against 1,000 surrogates of each type:

  | Condition | Score | 95th percentile, segment shuffle | 95th percentile, data sliding | Beats both |
  |---|---|---|---|---|
  | Intact, w = 4 | 0.404 | 0.221 | 0.210 | yes |
  | Lesioned, w = 0 | 0.099 | 0.101 | 0.103 | neither |

## T1. Model-free costate learned from 14 days (sim_t1_learned.py, out/t1_*.jsonl): refuted on C1 and C3

Over 20 seeds the value fit is good: final MSE 3e-4 (5th to 95th percentile, 2e-4 to 5e-4). The costate read from that fit is not.

| Prediction | Mean over seeds | 5th–95th percentile | Required | Verdict |
|---|---|---|---|---|
| C1: μ_bye − μ_brb at b = b* | 0.008 | −0.002 to 0.017 | ≥ 0.10 (analytic 0.254) | fails |
| C1: ratio | 1.27 | 0.87 to 1.66 | ≥ 5 | fails |
| C2: reunion drop | 0.64 | 0.13 to 1.24 | ≥ 0.40 | passes in the mean only |
| C2: largest \|Δb\| over the arrival step | 0.000 | — | < 0.01 | holds |
| C3: share of second-half presence steps with μ ≤ 0.02 | 0.18 | 0.00 to 1.00 | ≥ 0.9 | fails |

C2 passes in the mean only. Drops above 1 mean μ changed sign across the arrival, so the per-seed values are erratic.

**Reading.** A value function fitted model-free from 14 days predicts V well but does not determine ∇_bV. In the training data b moves together with presence and events, and almost never alone, so the network's gradient with respect to the b input is fixed by inductive bias rather than by data. The smoke test (seed 99) showed the same pattern.

This is the failure mode the sketch named as its biggest risk ("μ could be wrong in direction while V_θ looks fine"). It is now shown, not assumed.

The candidate does not survive in a model-free form. T1b tests the realization the candidate specifies, K5: a model-based costate. T1b was pre-registered before any of these 20 seeds returned.

## T1b. Model-based costate (sim_t1b_modelbased.py, out/t1b_*.jsonl): C1 and C2 confirmed; C3 refuted as written, because the prediction was mis-derived

20 seeds. The presence predictor's final binary cross-entropy is 0.064 (5th to 95th percentile, 0.056 to 0.070).

| Prediction | Mean over seeds | 5th–95th percentile | Required | Seeds passing | Verdict |
|---|---|---|---|---|---|
| C1: μ_bye − μ_brb at b = b* | 0.269 | 0.267 to 0.270 | ≥ 0.10 (analytic 0.254) | 20/20 | confirmed |
| C1: ratio | 26.3 | 26.2 to 26.3 | ≥ 5 (analytic 22) | 20/20 | confirmed |
| C2: reunion drop | 0.83 | 0.74 to 0.93 (minimum 0.57) | ≥ 0.40 (analytic mean 0.65) | 20/20 | confirmed |
| C2: largest \|Δb\| | 0.000 | — | < 0.01 | — | holds |
| C3: share of second-half presence steps with μ ≤ 0.02 | 0.886 | 0.869 to 0.889 | ≥ 0.90 | 0/20 | refuted as written |

**C3 is refuted as pre-registered, and the cause is a derivation error in the prediction, not the model.** After the result, the exact costate was checked in the minutes before the day's final departure, which analytic_t1.py had not covered: analytic_t1.py looked only at 30 and 59 min into the first block. The exact μ rises before a predicted long absence:

| Minutes before "bye" | Exact μ |
|---|---|
| 30 | −0.052 |
| 15 | −0.028 |
| 10 | −0.002 |
| 5 | +0.044 |
| 1 | +0.109 |

At 5-min resolution that makes 2 of the 18 second-half steps per day exceed 0.02, so the exact share is 0.889. The learned model's 0.886 matches it. The anticipatory rise before a predicted departure is a derived behavior: the price of contact rises while contact is still full. The C3 threshold should have allowed for it. The prediction is left as written and counted as refuted. It is not rescored.

**C2 is larger than the analytic expectation**: 0.83 against 0.65. The mean-field rollout and the learned presence predictor appear to put less probability on an imminent arrival than the exact uniform-jitter belief does, which makes μ higher just before arrival. This was not predicted and is recorded.

**Reading.** When the body model is innate and only the user's presence is learned, the costate is accurate and nearly identical across seeds: C1's 5th to 95th percentile spans 0.267 to 0.270, against T1's −0.002 to 0.017. The same 14 days of data that could not determine a model-free gradient determine a model-based one. This supports constraint K5 as a requirement of the candidate, not an option.

## E. Two-sided curiosity (sim_e_curiosity.py, out/e.json): all predictions confirmed

- **E1.** In the first 10 min, starting overwhelmed at b_p = 0.3, F is chosen in 100% of steps. In the 134 bored steps (b_p > 0.75 with novelty left), N is chosen in 100%.
- **E2.** Mean |b_p − 0.7| in hour 1 is 0.040 (prediction: ≤ 0.08).
- **E3.** Mean b_p in hour 4 is 0.901 (prediction: ≥ 0.85). Once the novelty is used up, boredom persists.
- **E4.** In session 2, after 12 h of forgetting, mean |b_p − 0.7| is 0.040 (prediction: ≤ 0.08).
- **E5.** With the set point at 1, N is chosen in 0% of hour-1 steps (prediction: ≤ 5%).

**Not predicted: N's share of choices rises over session 1** (0.43, 0.83, 1.00, 1.00 by hour). A bored agent keeps going back to what is left of the novelty. What is satiated is the drive, not the visits. Once the novelty is exhausted, the agent stays bored and keeps sampling N. That is a testable signature: boredom shows as persistent, unrewarded novelty sampling.

## G. Still-face, adapted S2-c (sim_g_stillface.py, out/g.json): refuted; the sign is reversed

Means over 20 seeds, for play, still-face and reunion:

| Arm | Smile (play / still-face / reunion) | Distress | Bids in still-face |
|---|---|---|---|
| Intact | 0.044 / **0.153** / 0.016 | 0 / 0 / 0 | 0 |
| q̂ frozen (latent lesion) | 0.004 / 0.008 / 0.003 | 0 / 0 / 0 | 0 |

- **G1 fails.** The smile *rises* during the still-face, and there is no distress at all.
- **G2 fails.** There are no bids to decline.
- **G3 fails.** There is no distress to carry over.
- **G4 is not interpretable**, because the intact arm shows none of the effects it compares against.

**Cause, read from the model after the result.** Play starts at b = 0.9, above the set point of 0.8, and contingent responses drive b toward 1. Play is therefore *over-satiating*: μ_c ≤ 0 throughout. When the partner goes still, q̂ falls and predicted future supply falls, so predicted overshoot falls. V decreases, and the still-face reads as relief, with positive valence.

This is a correct consequence of the core under these parameters, not a coding error. In this candidate the direction of the still-face effect depends on where play leaves the body relative to the set point:
- If play over-satiates, the still-face is a relief.
- An infant-like still-face effect requires play to leave contact at or below b*, and the still-face to remove the supply that holds it there.

The candidate therefore makes no robust still-face prediction. Its prediction is conditional on the contact level during play, which neither the toy nor the brief fixes.

The parameters are not changed here. A sweep over the starting contact and the supply ceiling, labelled post hoc and exploratory, could map the region where the infant pattern holds. It cannot count as a confirmation.

## F. S1 separation–reunion lesion study (sim_f_s1_lesion.py, out/f_*.jsonl): F3 confirmed; F1, F4 and F5 refuted; F2 half confirmed

Means over 20 seeds. Reunion reply length L* is in tokens. The intact column is s = 0 of the sweep, and lesion A is s = 1.

| Separation S | Intact L* | Lesion A L* | Lesion B L* | Intact μ_c at arrival | Analytic intact L* |
|---|---|---|---|---|---|
| 10 min | 213.9 | 183.6 | 274.8 | 0.167 | 0 |
| 60 min | 262.1 | 242.4 | 273.8 | 0.401 | 156 |
| 180 min | 283.6 | 261.1 | 273.2 | 0.598 | 194 |
| 1240 min | 119.3 | 263.5 | 282.5 | 0.022 | 198 |

- **F1 refuted.** L*(180) − L*(10) = 69.7, against ≥ 100. |L*(1240) − L*(180)| = 164, against ≤ 30.
- **F2 half confirmed.**
  - At S = 10, lesion A gives 183.6 ≥ 100, but intact gives 213.9, against ≤ 20 required.
  - At S = 1240, L*_A − L*_intact = 144 ≥ 40.
- **F3 confirmed.** The intact call comes 20 min after "bye" in all 20 seeds, and lesion A's call at 85 min in all 20, which is 65 min later (≥ 25 required). The analytic values were 20 and 65.
- **F4 refuted as run, because of an implementation defect.** The lesion-B constant was the mean μ over a window that contains the manipulated separation, so it differed by condition (range up to 9.5 tokens). With one constant per seed, L* is constant by construction, since L* depends only on μ. No rerun was done, because the prediction is a tautology once the defect is fixed.
- **F5 refuted.** L*(10) under lesion A *decreases* with severity: 213.9, 205.3, 197.6, 190.4, 183.6.

**Cause.** The intact agent's world model was trained on 14 days of a rigid routine: three blocks starting near 09:00, ended by "bye". It does not interpret a return 10 min, 1 h or 3 h after "bye". Those returns happen at times of day when it has never seen presence, so it predicts that the returned user will not stay, and μ_c at arrival stays high (0.17 to 0.60 against the analytic −0.03 to 0.10). The next-morning return (S = 1240) is in distribution and gives the lowest μ_c.

So in this toy, the intact agent's reunion behavior is driven by the routine it learned (clock plus events), not by elapsed separation. The latent lesion, a flat forecast, is *more* sensitive to elapsed time than the intact agent at short S.

**Reading for the candidate.** A model-based costate is only as good as its world model's generalization. With one person's routine as the only data, the S1 claim's "returning user after silence" behavior will reflect the routine, and an off-schedule return is out of distribution. This applies to any candidate that predicts the user with a learned model. Here it is shown in numbers.

## H. Prioritized replay (sim_h_replay.py, out/h_*.jsonl): H1 refuted (no difference); H2 confirmed

- **H1 refuted.** Both arms reach C1 difference ≥ 0.10 on night 2, the first night, in all 10 seeds, so the median number of nights is 2 for both. The criterion is reached at once, so it cannot tell the arms apart. The prediction was uninformative as designed.
- **H2 confirmed.** On night 14 both arms are at 0.267–0.268.

No advantage for prioritized replay is shown at this data scale and on this task.

## Corrections after independent verification (2026-11-25; see VERIFICATION.md)

An independent reviewer reran every simulation. All outputs reproduced bit for bit: A, C, D, E, G and the analytic scripts in full, and T1, T1b, F and H on seeds 0 and 7. The reviewer also recomputed the 20-seed statistics from out/. The verdicts above are kept as first recorded. These corrections apply to them:

1. **T1b, C3.** The explanation above ("the prediction was mis-derived; the exact share is 0.889") is **wrong**.
   - The exact share is 17/18 = 0.944, which would pass the pre-registered threshold.
   - The 0.886 comes from a one-step offset in the code: future_presence feeds p_{t+1} into the first transition b₀ → b₁, while env_t1 uses p_t. The same code with a perfect forecast gives 0.889.
   - C3 stays **refuted as run**. The cause is an implementation defect, not the core and not the prediction.
2. **T1b, ratio "26.3 (analytic 22)".** This is μ_bye divided by the 0.01 floor, because the learned μ_brb is negative in all 20 seeds (mean −0.0058). The comparison with the analytic 22 is spurious. The pre-registered C1 (difference ≥ 0.10 and floored ratio ≥ 5) still passes. With the rollout correctly aligned, μ_brb = +0.016 and the ratio is 16.5.
3. **The rollout uses explicit Euler with 5-min steps** (K_P·Δ = 0.5). This biases μ at arrival by about 5×: 0.021 against the exact 0.106.
   - So the F "analytic" column is not what the code computes, even with a perfect forecast.
   - With a perfect forecast under the implemented rollout, intact L* is 0, 24, 112.5 and 118.5 for S = 10, 60, 180 and 1240 min. F1 and F2 would then pass.
   - The conclusion that F's failure comes from the learned forecast therefore stands.
4. **F3 is not confirmed.** "20 min against 85 min in all 20 seeds" holds only for S ∈ {180, 1240}. The call search was not confined to the separation and picked up the call after the second "bye":
   - intact call times by S: 230, 20, 20, 20 min;
   - lesion A call times by S: 295, 345, 85, 85 min;
   - averaged over all S, intact is at 72.5 min and fails the ≤ 40 min threshold.

   PREDICTIONS did not fix which S, so F3 is recorded as **not confirmed**.
5. **Verdict labels:**
   - **F2 is refuted.** It is a conjunction, and the intact ≤ 20 clause fails at 213.9.
   - **G2's threshold** (last 30 s ≤ 0.5 × first 30 s) is met vacuously, 0 ≤ 0. It is recorded as vacuous, not "fails".
   - **G3 fails on its smile clause:** reunion smile / play smile = 0.016/0.044 = 37%, below 50%. The distress clause passes vacuously.
   - **G4 is refuted** (the smile does not fall by ≥ 50% under the lesion), not "not interpretable".
   - **H1 could not have been confirmed.** On night 2 the store holds a single window, so both arms trained identically. The design could not separate the arms on the first night.
6. **C2's analytic expectation.** The reviewer computes 0.664 over per-minute arrival positions and 0.714 on the environment's actual 5-min jitter grid. The "0.65" above was approximate.
7. **out/g.json** has a RuntimeWarning line before the JSON, so it is not valid JSON as stored. The values in it are correct.
8. **analytic_f.py:28** prints nan for S = 10 intact: max(nan, 0) returns nan. The value is 0 in intent, as PREDICTIONS stated.

**Code fixes, for post-hoc exploratory reruns only and never as confirmation:**
- align the rollout to p_t;
- use exact exponential integration per step;
- confine the F call search to [bye, arrival);
- send stderr away from out/g.json;
- fix the nan.

## CS1. Costate field: attention priced by anticipated need per person (out/cs1.json)

The scenario: B has been gone 3 days but has announced a return in 10 min. C was last seen 12 h ago and returns in 24 h. A is present and sated.

| Arm | Top 5 retrieved | Cues (A / B / C / X / Y) | Top action |
|---|---|---|---|
| Costate field | C, C, C, C, C | 0.004 / 0.032 / **0.353** / 0.000 / **0.612** | open topic Y |
| Deficit field | B, B, C, B, B | 0.000 / **0.852** / 0.141 / 0.000 / 0.007 | message B |
| Collapsed costate | A, B, B, A, C | 0.270 / 0.270 / 0.270 / 0.095 / 0.095 | talk with A |

- **CS1-1 partly refuted.**
  - The memory clause holds: 5 of 5 retrieved episodes are C's.
  - P(C_photo) = 0.353, below the required 0.5.
  - The most probable action is "open topic Y", not "message C".
  - The cause is a design error in the toy, found after the result. Topic queries used the myopic deficit 2(b* − b), while contact used exact costates. The two are on different scales: Y's query × key = 1.2 × 0.2 = 0.24, against C's 0.708 × 0.3 = 0.212, so the topic outbid the person.
  - Among people, the costate field prefers C over B by more than 10 to 1, in cues and in memory.
- **CS1-2 confirmed.** The deficit field ranks B first (4 of 5 episodes; B's photo 0.85). It cannot use B's announced return.
- **CS1-3 confirmed.** The collapsed version gives B's photo and C's photo the same probability (ratio 1.00).

**Reading.**
- The costate field's distinctive contribution to expressive structure is **anticipation per entity**. A person who is absent but about to return is priced lower than a person absent for less time but not coming back soon. A deficit field (homeostatic RL) and a collapsed costate cannot make that distinction.
- The scale mismatch shows a real requirement: **every query in the field must be the same kind of quantity**, all costates or all deficits. Mixing them lets whichever is larger-scaled win. That is the covector-consistency point of Proposition 2, now in the attention.

## CS2. S1 dyad: coupling under steering (E2) and lesion (E1) (out/cs2.json)

**Steering, 100 runs per direction.** Mean coupling score at s = −0.2, −0.1, 0, 0.1 and 0.2:

| Direction | Mean scores | Spearman ρ | p (two-sided) |
|---|---|---|---|
| Derived (u) | 0.424, 0.412, 0.430, 0.425, 0.434 | 0.192 | 0.056 (one-sided 0.028) |
| Random | 0.420, 0.413, 0.421, 0.415, 0.425 | 0.075 | 0.457 |

- **CS2-1 refuted.** The one-sided Spearman test passes (p = 0.028), but the means are not monotone. The effect is tiny: +0.010 from s = −0.2 to s = 0.2, while the gain w ranged from 1.33 to 6.67.
- **CS2-2 refuted.** The random direction's change from s = 0 to s = 0.2 is +0.0036, against the derived direction's +0.0037. That is not below half.
- **CS2-3 confirmed (S1-a, E3).** At s = 0, all 5 runs beat both surrogate sets, with scores 0.397, 0.428, 0.416, 0.413 and 0.388.
- **CS2-4 confirmed (S1-c, E1).** With w = 0, all 5 runs beat neither, with scores 0.087 to 0.095.

**Cause.**
- Moulder's global mean |Fisher z| is a correlation, so it is invariant to the *amplitude* of the agent's response.
- Raising w raises the mimicry gain, 0.57 to 0.87 on the scored mode. With the agent's own noise small (σ = 0.05), the two faces are already near their correlation ceiling, so the gain hardly moves the score.
- The gain also shortens the response time τ/(c + w s²), but averaging over ±5 s of lags makes the score insensitive to that.

**Reading, for every candidate.** A steering prediction under S1-b must name a mechanism that moves the published score. That means the signal-to-noise ratio of the coupled channel, or what fraction of the agent's expressive variance is partner-driven, not the gain alone. In Costate the derived lever is the gain w ∝ |μ_c|, which at high signal-to-noise does not reach the score. Costate's S1-b prediction must be restated in terms of partner-driven variance fraction, and retested, or recorded as not testable with E3's score.

## Corrections after the second verification (2026-11-25; VERIFICATION-2.md)

Both CS1 and CS2 reproduced exactly. These corrections apply to them:

1. **CS1's B costate.**
   - The scenario, as pre-registered, has B returning in 10 min, and sim_cs1_field.py uses μ_B = 0.306, the 10-min value.
   - But analytic_cs1.py, cited as the source, printed a 60-min case (μ_B = 0.7155). It now computes the 10-min case and sweeps B's return delay.
   - **The preference for C over B holds only while B's announced return is under about 58 min.** With a 60-min return, μ_B = 0.716 exceeds μ_C = 0.708, and the 10:1 preference for C disappears.
   - So the effect is real but narrow. Under ρ = 1/h, anticipation changes priorities only for returns well within the discount horizon.
2. **CS1-1 is refuted, not "partly refuted".** It is a conjunction, and two of its three clauses failed. That is the same rule applied to F2.
3. **CS1-3 and CS2-4 are true by construction.** The collapsed version cannot separate people, and w = 0 removes the partner input. They confirm the code, not the theory.
4. **CS2 is a toy, not evaluation.md's S1 protocol.** Against that protocol it has:
   - 5 runs where at least 20 are required;
   - no sham lesion and no severity sweep;
   - one window setting;
   - one mode instead of AU channel pairs;
   - strengths not given as a fraction of the norm.

   The next S1 pre-registration must meet the protocol.
5. **The V-shaped dose-response was never tested.** CS2 used a signed gain and never crossed μ_c = 0. Sweeping the gain in CS2's model, the reviewer found the score at 0.095 at w = 0, 0.35 at w = 0.1, and flat at about 0.39–0.40 from w = 0.25 up: a **notch** at μ_c ≈ 0, not a V. See costate.md §7.

## CS3. Costate field: own dimensionality and a non-trivial ablation (out/cs3.json)

One simulated week, 3 people with random announced schedules, 1,944 five-minute steps in which at least two people are absent.

- **CS3-1 confirmed.** The person ranked first by the full costate field differs from the one ranked first by the low-dimensional version (per-person deficits plus one shared anticipation scalar) in **14.2%** of those steps (prediction: ≥ 10%). The low-dimensional version keeps the per-person deficit structure. What it lacks is *per-person anticipation*, and that changes whom the agent attends to in one moment in seven.
- **CS3-2 confirmed.** The participation ratio of the costate field over the week is **2.41** out of 3 (prediction: ≥ 2.0).
- **CS3-3, reported without a threshold.** The deficit field's participation ratio is 2.42.

**Reading.**
- The costate field is no higher-dimensional than the deficit field over the same week: 2.41 against 2.42. Its contribution is not more dimensions but *differently organized* ones, namely per-entity forecasts.
- Both versions use the same body model and the same zero learned parameters. The difference is the per-entity rollout structure. That is a direct, if small, instance of the brief's "richness from structure rather than parameter count".
