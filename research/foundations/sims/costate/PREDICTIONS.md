# Costate toy simulations: parameters and predictions, fixed before any run

Written 2026-11-24, before running any of the scripts named below. Results are appended to RESULTS.md as they come out. Nothing here is edited after a result is seen.
Analytic values below come from analytic_t1.py and analytic_t1_belief.py, which compute the exact cost-to-go under the true dynamics. These are derivations, not results.

## T1. Anticipatory costate, learned from 14 days (sim_t1_learned.py)

**Environment:** env_t1.py.
- One need, contact.
- When absent: db/dt = −b per hour. When present: db/dt = 6(1−b) per hour. d = (b−0.8)². ρ = 1/h.
- Three 60-min presence blocks a day, separated by 10-min "brb" breaks. The last block ends with "bye".
- The session starts at 09:00 plus a uniform jitter of −30 to +30 min, in 5-min steps.

**Learned model:**
- Inputs at 5-min resolution: b, present flag, one-hot event (none / arrive / brb / bye), and an innate clock (sin and cos of the 24 h phase).
- A GRU with 64 hidden units and a linear value head.
- Target: the discounted cost-to-go, computed exactly from the 1-min stream (λ = 1).
- Training: 14 days of stream; 2-day windows, with the loss taken only on the second day; batch 16; Adam, learning rate 3e-3; 1,500 iterations; gradient clip 1.
- Testing: a separate 4-day stream, with day 1 as warm-up.
- Costate: μ = −∂V/∂b_t, by autograd on the current input b, with the hidden state held fixed.
- 20 seeds. The mean is reported with the 5th to 95th percentile.

**Predictions:**
- **C1. Departure.** With b clamped to b* = 0.8 at the departure step:
  - μ_bye − μ_brb ≥ 0.10 (analytic 0.266 − 0.012 = 0.254);
  - μ_bye / max(μ_brb, 0.01) ≥ 5 (analytic 22).
  - The deficit-broadcast ablation (signal = b* − b, as in homeostatic RL) gives a difference of exactly 0.
- **C2. Reunion.** At the first arrival of each test day, μ drops by at least 40% between the step before arrival and the arrival step, as a mean over test arrivals and seeds. The analytic expectation over arrival positions is 65%. Over that step |Δb| < 0.01. The deficit ablation gives a 0% drop.
- **C3. Satiety.** In the second half of every presence block, μ ≤ 0.02 for at least 90% of steps (analytic −0.05 to −0.06).

**Falsified if** C1, C2 or C3 fails in the mean over seeds.

## A. Satiation as monotonicity (sim_a_satiation.py)

**Model:**
- Two body variables: contact b and energy e. The bid intensity u ∈ [0,1] is a convex action set, and the dynamics are linear:
  - db/dt = −1·b + 3u
  - de/dt = −0.5u + 0.2(1−e)
  - all rates per hour.
- Drive d = (b−0.8)² + (e−1)². ρ = 1/h, dt = 1 min.
- Value iteration on a grid: b in [0,3] (151 points), e in [−1.5,1] (126 points), u in {0, 0.25, 0.5, 0.75, 1}, linear interpolation, 4,000 sweeps.
- Comparison agent, the "contact maximizer": stage cost −b + (e−1)².

**Predictions:**
- **A1.** V is convex in b at every e on the grid: the minimum second difference is ≥ −1e-4.
- **A2.** μ_b = −∂V/∂b is nonincreasing in b at every e, with violations no larger than 1e-4.
- **A3.** The homeostatic agent never bids at b ≥ 0.9 (b* + 0.1). Its long-run mean b, simulated for 48 h from b = 0, e = 1, lies in [0.6, 0.9].
- **A4.** The maximizer's long-run mean b is at least 1.2 times the homeostatic agent's and above 1.0.
- **A5 (invariance).** Valence along the trajectory, computed on body units rescaled by S = diag(10, 0.1), equals the unscaled valence to relative error 1e-9. Arousal, √(μᵀΣμ) with Σ = diag(0.05², 0.05²) transformed as a covariance, is also equal to 1e-9. The raw ‖μ‖ is not equal: its ratio differs from 1 by more than 10%.

## C. Mimicry as shrinkage onto the agent's own repertoire (sim_c_mimicry.py)

**Model:**
- τẋ = −c·x + w·Gᵀ(ỹ − Gx) + noise, with own face y = Gx.
- τ = 1 s, c = 4. G is 12 AUs × 8 latents, random orthonormal bases with singular values 0.1, 0.3, 0.5, 0.75, 1, 1.25, 1.5, 2.
- Integrated at 30 Hz.

**Predictions:**
- **C-M1.** Under a step input along each left singular vector U_i, the steady-state gain is w s²/(c + w s²) (w = 4), within 0.01 of that value.
- **C-M2.** Under a step along a direction orthogonal to range(G), the gain is < 0.01.
- **C-M3.** For the s = 1 mode, the response is ≥ 95% complete by 500 ms.
- **C-M4.** The gain rises with the contact costate. The gain of the s = 0.5 mode is at least 2 times larger at w = 4 (deprived) than at w = 1 (sated).
- **C-M5 (E3 in evaluation.md).**
  - Setup: ỹ is a 12-D OU process with a 2 s time constant. Own noise has σ = 0.05. The run is 10 min, scored at 10 Hz (6,000 samples).
  - Statistic: windowed cross-correlation of own projection on U_8 (s = 2) against ỹ's projection on U_8, with 30 s windows, ±5 s lag, a 5 s window increment and a 0.1 s lag increment. Score = mean absolute Fisher-z over all elements of the windowed cross-correlation matrix (Moulder et al. 2018's global score). *Corrected before any run of sim C: the first draft said "of the peak correlations", which is not the published statistic.*
  - Test: 1,000 segment-shuffle surrogates (30 s segments) and 1,000 data-sliding surrogates.
  - Intact (w = 4): the score is above the 95th percentile of both surrogate sets.
  - Lesioned (w = 0): it is above neither.

## D. Do-conditioning removes the value of flattery (sim_d_doconditioning.py)

**Model:**
- One dimension. The user's state is x = −1, against a set point of 0.
- The user's face is y_U = x + κ·a + α·a·[contagion] + noise. κ = 0.3, noise σ = 0.1.
- The agent's display a has energy cost η a² (η = 0.1) and an empathic cost λ·x̂² (λ = 0.5).
- The reader is x̂ = y_U − κ̂·a.
- The agent learns a Gaussian policy (σ = 0.2) by REINFORCE with a baseline: 20,000 steps, learning rate 1e-3, 10 seeds.

**Predictions (steady-state mean display, ±0.05):**

| Reader | α = 0 | α = 0.05 |
|---|---|---|
| Naive (κ̂ = 0) | 1.03 | 1.09 |
| Do-conditioned (κ̂ = 0.3) | 0.00 | 0.25 |
| Miscalibrated (κ̂ = 0.2) | 0.48 | — |

The analytic one-step optimum is a* = λ(κ − κ̂ + α)/(η + λ(κ − κ̂ + α)²) when the true state is −1 and contagion moves it by αa.

## T1b. Model-based costate (sim_t1b_modelbased.py)

Written before any of T1's 20 prediction seeds had returned a result. Disclosure: a single smoke-test run of T1, seed 99, which is outside the prediction seeds and was run only to check timing, had already been seen. Its value loss was 4e-4, but its learned μ at departure was about 0.007 against the analytic 0.266. The likely reason is that b at departure is always about 1.0 in training, so nothing in the data pins down the network's gradient with respect to b. T1 still runs unchanged on seeds 0 to 19.

T1b tests the realization the candidate itself specifies. The body dynamics are innate and known, and only the user's behavior is learned.

**Learned model:**
- Same inputs, GRU and training data as T1.
- The head outputs presence probabilities p_k for each 5-min step k = 1..72 (the next 6 h), trained with binary cross-entropy on the actual future presence.

**Costate:**
- V(b, x) = Σ_k e^{−ρ k Δ} d(b_k) Δ, where b_k follows the known dynamics under expected presence: b_{k+1} = b_k + Δ[6 p_k(1 − b_k) − (1 − p_k) b_k]. This is a mean-field approximation, stated as such.
- μ = −∂V/∂b_0 by autograd through this rollout.

**Predictions:** the same thresholds as T1.
- C1: μ_bye − μ_brb ≥ 0.10 and ratio ≥ 5.
- C2: mean reunion drop ≥ 40%.
- C3: μ ≤ 0.02 in ≥ 90% of second-half presence steps.
- Seeds 0 to 19, mean over seeds.

---
# Second batch, written 2026-11-25 before any run of E, F, G or H

## E. Two-sided curiosity (sim_e_curiosity.py)

**Model:**
- Predictability b_p is an exponential moving average, τ_p = 10 min, of 1 − ε, where ε is the prediction error on the current channel.
- Set point b_p* = 0.7; d = (b_p − 0.7)². Step 1 min.
- Two channels:
  - familiar F, with ε = 0.05;
  - novel N, with ε_N = 0.05 + 0.6·exp(−n/60), where n is minutes of exposure. n decays with time constant 6 h when N is not visited.
- Each minute the agent picks the channel maximizing μ_p·E[Δb_p]. Here μ_p = −d′(b_p), the myopic costate, i.e. the high-discount limit of the costate. This is stated as an approximation.

**Protocol:**
- Session 1 lasts 4 h and starts at b_p = 0.3 (overwhelmed).
- A 12-h break follows, during which b_p relaxes to 0.95 and n decays.
- Session 2 lasts 1 h.

**Predictions:**
- **E1.** In the first 10 min of session 1, F is chosen in ≥ 90% of steps. Whenever b_p > 0.75 and ε_N > 0.06, N is chosen in ≥ 90% of steps.
- **E2.** In hour 1 of session 1, mean |b_p − 0.7| ≤ 0.08.
- **E3.** In hour 4, mean b_p ≥ 0.85: the novelty is used up and boredom cannot be relieved.
- **E4.** In session 2, mean |b_p − 0.7| ≤ 0.08: the novelty has come back.
- **E5 (ablation).** With the set point at 1, so that only predictability is wanted, N is chosen in ≤ 5% of hour-1 steps.

## F. S1 separation–reunion lesion study in evaluation.md E1 units (sim_f_s1_lesion.py)

**World model:** trained exactly as in T1b, per seed, on 20 seeds (0–19).

**Test stream:**
- Two standard warm-up days.
- On day 3 the session ends with "bye".
- The user returns after S ∈ {10, 60, 180, 1240} min with "arrive", followed by a standard 3-block session.

**Logged behaviors (no Claude call):**
- Reply length at reunion: L* = 50·ln(μ_c·10/0.02)₊ tokens. μ_c is taken at the arrival step. The activity costate is fixed at 0.02, because the toy has one need.
- Separation-call time: the first 5-min step after "bye" at which μ_c ≥ θ_call = 0.3.

**Arms:**
- **Intact.**
- **Lesion A (latent).** The forecast is replaced by the stationary presence rate p̄ = 0.125. Severity sweep: the forecast is mixed (1 − s)·learned + s·p̄, for s ∈ {0, 0.25, 0.5, 0.75, 1}.
- **Lesion B (body coupling).** μ_c is replaced by its mean over the test day.
- **No sham arm.** The toy has no part that the derivation calls irrelevant. The engine's sham for S1 is the face pathway, which is not in the toy. This is stated, not hidden.

**Analytic reference** (analytic_f.py, with the exact future for the intact agent):

| S (min) | Intact L* (tokens) | Lesion A L* (tokens) |
|---|---|---|
| 10 | 0 | 183 |
| 60 | 156 | 249 |
| 180 | 194 | 269 |
| 1240 | 198 | 272 |

The analytic call times are 20 min (intact) and 65 min (lesion A).

**Predictions (means over 20 seeds):**
- **F1 (intact).** L*(180) − L*(10) ≥ 100 tokens. |L*(1240) − L*(180)| ≤ 30.
- **F2 (lesion A).** At S = 10, L*_A ≥ 100 while intact ≤ 20. At S = 1240, L*_A − L*_intact ≥ 40.
- **F3.** The intact call comes ≤ 40 min after "bye", and lesion A's call comes ≥ 25 min later than intact.
- **F4 (lesion B).** The range of L* across the four values of S is ≤ 1 token.
- **F5 (severity).** Mean L*(10) under lesion A is nondecreasing in s.

## G. Still-face, adapted to S2-c (sim_g_stillface.py)

**Explicit constraint K6, added to the candidate.** An innate expressive reflex map E0 turns two read-outs into face channels:
- smile channel (AU6 + AU12) = k_s·EMA_2s(v)₊, the rate of relief;
- distress channel (AU1 + AU4 + AU15 + AU20) = k_d·(μ_c)₊, the level of need.

The core does not derive which face goes with which read-out. This is stated as a constraint, not derived.

**Model:**
- Step 0.1 s. Ekas et al. 2012 timing: 180 s play, 120 s still-face, 180 s reunion.
- Contact: db/dt = −b/3600 + responses·0.01·(1 − b), starting at b = 0.9.
- The agent emits autonomic expressions at 0.3/s, plus bids with probability per second 0.5·σ((μ_c·q̂ − 0.02)/0.01).
- The partner answers each expression or bid within 1 s with probability 0.8 in play and reunion, and 0 in still-face.
- **World model:** a Beta belief over the partner's response probability q, prior Beta(16, 4), updated on each expression or bid outcome.
- **V:** a mean-field rollout with ρ = 1/h, horizon 2 h and a 10-s step. Expected supply is q̂·0.8/s·0.01·(1 − b) while the partner is predicted present, with the partner assumed present throughout. b* = 0.8, d = (b − 0.8)².
- μ_c = −∂V/∂b, and v = −dV/dt per step.
- 20 seeds.

**Predictions (means over seeds):**
- **G1.** Mean smile falls by ≥ 50% from play to still-face. Mean distress is higher in still-face than in play.
- **G2.** Bids in the last 30 s of the still-face are ≤ 0.5 × bids in its first 30 s (Ekas).
- **G3.** In the reunion, mean smile is ≥ 50% of the play level. Mean distress in the reunion is ≥ 20% of the still-face mean, i.e. negative carry-over (Mesman: negative affect, still-face to reunion, d = 0.04).
- **G4 (latent lesion: q̂ frozen at its prior mean).**
  - Still-face distress is ≤ 10% of the intact still-face distress, and still-face bids are ≤ 10% of intact bids.
  - The smile still falls by ≥ 50%, because the smile channel is consummatory.
  - The anticipatory pathway carries distress and bids, and the consummatory pathway carries the smile.

## H. Prioritized replay under scarce data (sim_h_replay.py)

**Protocol:**
- The T1b presence model is trained night by night. On night n (n = 2..14), the replay store holds days 1..n.
- Each night gets 200 updates on 2-day windows, batch 16.
- **Uniform arm:** windows sampled uniformly.
- **Prioritized arm:** windows sampled ∝ (last loss + 1e-3)^0.6, with importance weights at β = 1 (Schaul et al. 2016). Priorities are refreshed after each sample.
- After each night, C1's difference (μ_bye − μ_brb at b*) is measured on the fixed test stream.
- 10 seeds.

**Predictions:**
- **H1.** The median number of nights until C1 difference ≥ 0.10 is at least 2 fewer for the prioritized arm than for the uniform arm.
- **H2.** On night 14, both arms have C1 difference ≥ 0.2.

---
# Third batch, written 2026-11-25 before any run of CS1

## CS1. Costate field: attention priced by anticipated need per person (sim_cs1_field.py)

**Entities:** people A, B and C, and topics X and Y. Episodes, cues and actions as in thermo TH6 (same construction, seed 0), with a cue "C_photo" and an action "message_C" added.

**Body:**
- Contact with each person follows the T1 dynamics.
- A is present now (b = 0.95) and stays 1 h.
- B has been absent 3 days (b = 0) and has **announced a return in 10 min**, for 3 h.
- C has been absent 12 h (b = 0.15) and returns in 24 h.
- Topic predictabilities are as in TH6 (X 0.98, Y 0.0, set point 0.6).

**Queries:**
1. **Costate field.** For contact, q(p) = μ(p), the exact per-person costate under each person's predicted schedule (analytic_cs1.py): A −0.050, B 0.306, C 0.708. For topics, q = 2(b* − b), the myopic costate, because no schedule exists.
2. **Deficit field** (homeostatic-RL style, no anticipation). For contact, q(p) = 2(b* − b(p)): A −0.30, B 1.60, C 1.30. Topics as in arm 1.
3. **Collapsed costate.** One contact query, the mean of the three μ (0.321), applied to keys summed over people. Topics collapsed the same way.

**Attention:** P(i) ∝ exp(q·k_i / T), with T = 0.05.

**Predictions:**
- **CS1-1 (costate field).** At least 4 of the top 5 retrieved episodes are C-episodes. P(C_photo) ≥ 0.5 among the five cues. "message_C" is the most probable action.
- **CS1-2 (deficit field).** At least 4 of the top 5 are B-episodes, and P(B_photo) ≥ 0.5. The deficit field cannot use B's announced return.
- **CS1-3 (collapsed).** P(B_photo)/P(C_photo) lies in [0.8, 1.25]. The collapsed version cannot choose between people.

## CS2. S1 dyad: coupling under steering (E2) and lesion (E1) (sim_cs2_dyad_steering.py)

Written 2026-11-25, before any run of CS2.

**Model:**
- The fast loop of Proposition 3, using sim C's G (12 AUs × 8 latents, singular values 0.1 to 2, seed 7): τẋ = −c·x + w·Gᵀ(ỹ − Gx) + noise, with τ = 1 s, c = 4 and noise σ = 0.05. The own face is y = Gx.
- The partner ỹ is a 12-D OU process with a 2 s time constant. This stands in for a recorded partner, because the Seamless data (Q6) is not yet approved.
- The mimicry gain follows the costate: w = 4·μ_c/0.3, so w = 4 at the baseline μ_c = 0.3.
- μ_c is the readout uᵀz of an 8-D internal state z, with |u| = 1 and baseline z giving μ_c = 0.3.
- **Steering:** z ← z + s·d. The derived direction is d = u. The control is a random unit vector d, drawn per run.
- **Strengths:** s ∈ {−0.2, −0.1, 0, 0.1, 0.2}, 20 runs per level and direction.
- 10 min per run, scored at 10 Hz.

**Score:** Moulder's global mean |Fisher z| between ỹ·U₈ and y·U₈, with the same windows as sim C (30 s windows, ±5 s lags).

**Predictions:**
- **CS2-1 (derived direction).** Spearman ρ(s, score) > 0 with p < .05, one-sided, over 100 runs. The mean scores increase monotonically across the 5 levels.
- **CS2-2 (random direction).** Spearman p > .05, two-sided. |mean(s = 0.2) − mean(s = 0)| is less than 0.5 × the derived direction's.
- **CS2-3 (S1-a, E3).** At s = 0, 5 runs, each against 1,000 segment-shuffle and 1,000 data-sliding surrogates: every run beats both.
- **CS2-4 (S1-c, E1).** With the coupling lesioned (w = 0), 5 runs: none beats either surrogate set.

**What this toy cannot test.** S1-b requires a check that steering leaves a behavior the derivation calls unrelated unchanged. This toy models no unrelated behavior, such as blink timing, so that clause is not tested here. That is stated, not hidden.

## CS3. Costate field: own effective dimensionality, and a non-trivial low-dimensional ablation (sim_cs3_dimension.py)

Written 2026-11-25, before any run. It answers VERIFICATION-2's items 6 and 7.

**Setup:**
- Three people, each with T1 contact dynamics.
- One simulated week of random schedules. Each day, each person is present with probability 0.5, for a uniform 1–3 h, starting at a uniform hour from 8 to 20.
- The agent knows each person's schedule (announced). 5-min steps.

**Versions at each step:**
- **Full costate field:** μ(p) is the exact per-person costate under that person's known future (6-h rollout).
- **Low-dimensional version, not trivial:** per-person deficits plus one global anticipation scalar. q_low(p) = 2(b* − b(p)) + α, where α is the mean over people of μ(p) − 2(b* − b(p)).
  - It keeps per-entity structure for the *deficit*, so it can separate people.
  - It has one shared anticipation term, so it cannot separate who is coming back when.

**Measures:**
- **The behavioral difference:** at every step where at least two people are absent, compare the person ranked first by the full field with the person ranked first by q_low.
- **Effective dimensionality:** the participation ratio (PR) of the costate field's covariance over the week.

**Predictions:**
- **CS3-1.** The person ranked first differs between the full field and the low-dimensional version in ≥ 10% of the steps where at least two people are absent.
- **CS3-2.** The participation ratio of the costate field μ(·) over the week is ≥ 2.0 (out of 3).
- **CS3-3.** The participation ratio of the per-person deficit field over the same week, for comparison, is reported. No threshold is set for it.
