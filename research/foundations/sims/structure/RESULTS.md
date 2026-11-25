# Expressive-structure test bed: results

## ES1 (out/es1.json, out/es1_per_seed.txt, figs/es1.png), run once, parameters as pre-registered

| Arm | Mean cost (pre-registered statistic) | Median cost over seeds | Seeds that ran away (> 5) | Agreement with oracle | Agreement when the best person was never met | Participation ratio | Learned parameters |
|---|---|---|---|---|---|---|---|
| Full: shared space, need vector | 0.247 | **0.092** | 0 / 20 | **0.835** | **0.778** | **1.67** | 16 |
| Scalar gauge | 35.2 | 0.594 | 2 / 20 | 0.527 | 0.292 | 1.00 | 16 |
| Independent per-person tables | 234.8 | 0.217 | 4 / 20 | 0.821 | 0.426 | 1.48 | 507 (mean) |
| Oracle | 0.177 | – | – | 1 | 1 | 1.64 | – |

**Verdicts:**
- **ES1-1 confirmed.** Full cost is 0.007 × scalar on means. The means are dominated by 2 runaway seeds, so the median ratio is the honest summary: **0.15**.
- **ES1-2 confirmed.** Agreement is 0.835 for full (≥ 0.70) and 0.527 for scalar (≤ 0.55).
- **ES1-3 refuted** (corrected in place after VERIFICATION.md). Full scored 0.778 (≥ 0.60), but the independent-tables arm scored 0.426, above its ≤ 0.35 bound, and the conjunction fails.
  - Independent tables fall back on the population mean for an unmet person. That is a better guess than the bound assumed, but still far below the shared space.
- **ES1-4 confirmed.** Full cost is 0.001 × independent on means, and **0.42** on medians. That is with 16 parameters against about 507.
- **ES1-5 withdrawn as evidence** (corrected in place). The ratio is capped at 2 needs. On each arm's own values, tables score 1.95, above full's 1.67.
- **Satiety.** When ‖e‖ ≤ 0.01, the approach rate is 0.06% in the full arm. It is not exactly zero, because a tiny residual e times a large predicted effect can cross the 0.01 threshold. At e = 0 it is zero by construction.

**What this shows for the four expressive-structure items:**
1. **Content-dependent selection.**
   - Which person the agent goes to depends on *which* need is short and *what* each person does for it.
   - A version that carries the same learned knowledge through a scalar gauge picks the oracle's person 53% of the time, against 84%, and runs away in 2 of 20 seeds.
   - This shows the selection over **people only**. Selection over memories and actions is not yet shown.
2. **Structure over a learned space.** The person space (appearance features to need effects) is learned and shared, and it generalizes to strangers: 0.78 against 0.43 on first encounters. Relationships, episodes and topics are not yet in it.
3. **Effective dimensionality and an ablation.** The participation ratio is 1.67, the maximum being 2 for 2 needs. The scalar version is rank 1 and fails the content-dependent choice.
4. **Richness from structure, not parameters.** 16 shared parameters beat about 507 per-person parameters at regulation (median cost 0.092 against 0.217) and at generalization.

**Scope.** In this toy, Costate's value μ·E[Δb|i] (myopic, quadratic need cost) and the Robust regulator's error × relevance (ĉ_i = Δb̂_i) are the **same rule**. ES1 therefore establishes the structure for both, but does not discriminate between them. ES2 will (relations and anticipation).

## ES2 (out/es2.json, figs/es2.png), run once, parameters as pre-registered

Median cost over 20 seeds. No arm ran away in the companion world.

| Arm | Companion world | Random world | Memory retrieval is the best episode for the need |
|---|---|---|---|
| Costate (anticipation, memory) | 0.0087 | 0.0104 | **0.749** |
| Robust regulator (myopic, memory) | 0.0077 | 0.0114 | 0.831 |
| Scalar | 0.0110 | 0.0070 | **0.155** |
| Costate without memory | 0.143 | 0.287 (1 runaway) | – |

**Verdicts:**
- **ES2-1 refuted.** Costate/Robust regulator = **1.12** (predicted ≤ 0.85). Anticipation did not help.
  - Seeking remembered people was chosen on 21% of steps (corrected in place; first written as "most steps"). Why anticipation did not help is unexplained.
- **ES2-2 refuted, narrowly.** The control ratio is 0.917, outside [0.95, 1.05]. Arm-to-arm noise at these tiny costs is about 10%.
- **ES2-3 confirmed.** Retrieval is content-dependent: 0.749 against 0.155.
- **ES2-4 confirmed.** Episodes matter: memory against none is **0.06 ×**.
- **ES2-5 confirmed.** The learned relation map generalizes to strangers: predicted against true companion value, **r = 0.93** (566 first approaches).

**A design weakness in ES2, disclosed.** Both needs drift down together, so a scalar gauge is nearly the right query. The scalar arm regulates as well as the full arms, even though its retrieval is content-blind. ES1, where the needs alternate, is the test of content dependence. ES2 tests relations and episodes.

## ES2b (out/es2b.json): anticipation without memory, pre-registered after ES2 and disclosed as such

| | Costate without memory | Robust regulator without memory | Ratio (medians) | Ratio (means) |
|---|---|---|---|---|
| Companion world | 0.143 | 0.176 | **0.81** | 0.99 |
| Random world | 0.287 | 0.220 | **1.31** | 0.84 |

**Verdicts:**
- **ES2b-1 confirmed.** Anticipation through the learned relation map lowers the median cost to 0.81 × when relations exist.
- **ES2b-2 refuted.** With no relational structure, anticipation raised the median cost to 1.31 ×. The means go the other way (0.84), so the result is noisy.
  - *Likely mechanism, not tested:* a relation map fitted to random arrivals forecasts noise, and max(0, ·) of a noisy forecast is an optimistic bias.
  - *What would answer it:* weight anticipation by the relation forecast's reliability, for example its predictive variance.

**What ES1–ES2b establish together:**
- **People, relationships and episodes** are entities in one learned space:
  - appearance maps to need effects (W), shared across people;
  - a relation map M connects people to the people they bring;
  - an episodic store is retrieved by need.
- **Selection over people (ES1) and over memories (ES2-3)** is content-dependent.
- **Selection over actions** (approach, seek a memory, rest) runs through the same query.
- **Topics are not shown.**
- **Anticipation**, Costate's distinctive term, helps when relations exist. It is not yet safe when they do not.

## ES3: reliability-weighted anticipation (out/es3.json), run once as pre-registered

| | Costate-rw | Robust regulator | Median ratio | Mean ratio | w at end of run |
|---|---|---|---|---|---|
| Companion world | 0.160 | 0.176 | 0.908 | 0.912 | 0.755 |
| Random world | 0.255 | 0.220 | 1.162 | 1.039 | 0.126 |

**All three refuted as worded:**
- **ES3-1:** 0.908 > 0.85.
- **ES3-2:** 1.16 is outside [0.90, 1.10].
- **ES3-3:** the companion world met its bound (0.755 ≥ 0.5), but the random world did not (0.126 > 0.1), and this is a conjunction.

The reliability weight did learn the right thing: high with relations and near zero without.

## Exploratory re-analysis, not pre-registered (out/es_paired_exploratory.txt)

Paired per-seed log ratios on the same seeds:

| Comparison | Geometric-mean ratio (95% CI) | Seeds where Costate is lower |
|---|---|---|
| Unweighted anticipation, companion world (ES2b) | 0.86 (0.76–0.98) | 11 / 20 |
| Reliability-weighted, companion world (ES3) | **0.81 (0.71–0.94)** | 14 / 20 |
| Unweighted, random world (ES2b) | 1.12 (0.97–1.30) | 8 / 20 |
| Reliability-weighted, random world (ES3) | **1.05 (0.92–1.20)** | 6 / 20 |

**Reading, exploratory:**
- Weighted anticipation helps when relations exist, and is not distinguishable from myopic regulation when they do not. That is the intended behavior.
- The unpaired median over 20 heavy-tailed seeds cannot resolve the ±10% bands I pre-registered.

**Stood down (same step failed twice).**
- *Failed tests:* the anticipation comparisons ES2-1, ES2b-2 and ES3.
- *Lesson for any later pre-registration:* use paired per-seed log ratios with a confidence interval, and enough seeds for the band. A rough guide is the CI half-width here of about 0.15 at n = 20, so a ±5% band needs n ≈ 200.

## ES4: topics and person × topic composition (out/es4.json), run once as pre-registered, 40 seeds

| Arm | Picks the oracle's (person, topic) | Median cost | Learned parameters |
|---|---|---|---|
| Bilinear (composition) | **0.637** | 0.024 | 162 |
| Additive | 0.286 | 0.057 | 34 |
| Tables | 0.093 | 0.122 | 2 per pair seen |
| Oracle | 1 | 0.022 | – |

**Verdicts:**
- **ES4-1 confirmed.** 0.637 ≥ 0.50 and 0.286 ≤ 0.35.
- **ES4-2 confirmed.** Bilinear against additive, paired geometric ratio **0.39** (95% CI 0.29–0.52), lower in 36 of 40 seeds.
- **ES4-3 confirmed.** Bilinear against tables, **0.16** (CI 0.10–0.25), lower in 40 of 40 seeds.

**Scope, partly by construction.** The world was built with a person × topic interaction. ES4 therefore shows that a shared bilinear structure *can* learn composition from about 1500 encounters and come within 10% of the oracle's median cost. It does not show that real people and topics compose this way.

## Summary of the four expressive-structure items, across ES1–ES4

| Item | Shown by | Status |
|---|---|---|
| 1. Content-dependent selection | ES1 (people), ES2-3 (per-person means, not episodes), ES4 (person × topic actions), ES8 (cues, given statistics) | Mostly shown, myopic limit only (corrected in place after VERIFICATION-2) |
| 2. Structure over people, relationships, episodes, topics, in a learned space | ES1 (person space), ES2-5 (relation map, r = 0.93), ES4 (topic space and composition), ES10 (elapsed time) | **Partly shown.** Items live in a learned space. **Needs** as a field over that space are not shown, because ES5 and ES6 were non-tests. |
| 3. Effective dimensionality, and an ablation | ES1-2, ES4-1, ES9 (winner-take-all) | **Partly shown.** The participation ratio was withdrawn, and no candidate's own effective dimensionality is measured. |
| 4. Richness from structure, not parameters | ES1-4 (16 against about 507), ES4-3 | Shown, in worlds that match the model class |

## Corrections after independent verification (VERIFICATION.md)

All scripts and figures reproduced byte for byte. The two unscripted outputs now have generators (make_es1_per_seed.py, make_es_paired_exploratory.py), and both reproduce exactly.

**Label corrections:**
- **ES1-3 is refuted** as a conjunction, not confirmed: tables scored 0.426 against the ≤ 0.35 bound. The full arm's 0.778 met its own bound.
- **ES1-5's participation ratio is withdrawn as evidence for item 3.**
  - It is capped at 2 for 2 needs, and the tables and oracle values were computed on the shared map.
  - On each arm's own values, tables score **1.95**, higher than full's 1.67, and the oracle 1.66 (out/es1_probe_wta.json).
  - The measure does not separate structure from no structure.
- **Hold by construction, now labelled:**
  - ES2-4 (the memory arm simply has an extra action);
  - ES1 and ES4 (the worlds match the model class).
- **The ES2 seek rate.** "Seeking was chosen on most steps" is wrong: seeking was 21% of steps.
- **ES2 "episodes"** are per-person means of observed effects, not separate episodes as the spec said.
- **ES2b-1** passes on the ratio of medians (0.81), but Costate is lower in only 11 of 20 seeds.

**A fairer low-dimensional ablation** (reviewer's probe, probe_winner_take_all.py, out/es1_probe_wta.json): the query is the single most-depleted need, winner-take-all.

| Arm | Picks the oracle's person | On first encounters | Median cost | Runaways |
|---|---|---|---|---|
| Full | 0.835 | 0.778 | 0.092 | 0 / 20 |
| Winner-take-all | 0.791 | 0.721 | 0.156 | 2 / 20 |
| Rank-1 shared map | 0.285 | 0.196 | 9539 | 17 / 20 |

The reviewer's paired cost ratio of full against winner-take-all is 0.37 (CI 0.17–0.78). The scalar gauge is the weakest low-dimensional version. Winner-take-all is the fair primary ablation for later pre-registrations.

**Identification (the reviewer's findings, accepted):**
- **For Costate**, the test bed uses the *myopic* limit μ = e, which costate.md itself names as the rival baseline (homeostatic RL without anticipation).
- **The drive here is one-sided.** The formal statements require a unique minimum at the set point.
- **Add-ons:** ε-greedy exploration, the reliability weight w and the max(0, ·) companion form.
- **For the Robust regulator**, the selection rule was not in its formal statement. It is now written into §2.2.

## ES5 (out/es5a.json, out/es5b.json, out/es5_smoke.txt), run once as pre-registered: **a non-test, because the world is infeasible**

**Disclosed:** a timing smoke run of one seed (rollout, budget world, seed 0) was made before the full run. Its cost was 110. The parameters were not changed after it.

**Every arm ran away in every seed, the oracle included.**

| Arm | Median cost | Seeds that ran away |
|---|---|---|
| Oracle | 110 | 40 / 40 |
| Field with learned space | 121 | 40 / 40 |
| Field without space | 135 | 40 / 40 |
| Global gauge | 305 | 40 / 40 |
| Winner-take-all | 1571 | 40 / 40 |

- **Why it is infeasible.** People are present on only 2 steps of each 8–24-step period, and 12 needs drift at 0.02–0.05 per step. Supply on the reachable approach rate (about 0.28) is below demand.
- **What the comparisons measure.** They measure which policy *degrades least* in an infeasible world. That is not the regulation the predictions were about.

**As pre-registered, for the record:**
- **ES5a-1:** 0.40 (CI 0.34–0.47). Confirmed.
- **ES5a-2:** 0.06 (CI 0.04–0.08). Confirmed.
- **ES5a-3:** 0.91 (CI 0.86–0.97), above 0.90. Refuted.
- **ES5a-4:** 0.35. Refuted.
- **ES5b-1:** 0.977 (CI 0.952–1.002). Refuted.
- **ES5b-2:** an approach ratio of 1.00. Refuted.

None of these is evidence for or against the structure, because none of the policies regulates.

**Lesson.** A test of regulation needs a world where regulation is possible. Before the next run (ES6), a feasibility criterion is fixed in advance and the world is calibrated on the oracle arm alone. Only then are the compared arms run.

## ES6: calibrated ES5 (out/es6.json), as pre-registered. **No drift scale met the feasibility criterion, so this is a non-test (the second failure of this step) and the line is stood down.**

Calibration with the oracle arm only, on seeds 1000–1019:

| Drift scale s | No-budget median (max) | Budget median (max) |
|---|---|---|
| 1 | 92 (373) | 113 (352) |
| 0.5 | 63 (242) | 61 (143) |
| 0.25 | 133 (369) | 143 (370) |
| 0.125 | 314 (549) | 314 (549) |

**What was learned** (diagnostics, not tests: out/es6_diag_exploration.json, plus a one-seed trace):
1. **The world had two failure modes, not one.**
   - **At the specified drift, supply is the limit.** People are present in short windows. With exploration off, the oracle still averages 68 (budget world 73).
   - **At low drift, exploration overfills.** Exploration was gated on ‖b‖ > 0.3, so *overfilled* states trigger random approaches.
     - Because of the similarity kernel, each approach also fills everyone similar.
     - Under a two-sided drive the only sink for overfill is drift. With less drift, overfill accumulates.
     - Seed 1000 at s = 0.125: cost 1.5 without exploration, against a calibration median of 314 with it.
2. **The port from ES1 dropped ES1's deficit gate.** ES1 gated exploration on the *deficit* ‖max(−b, 0)‖. ES5 gated it on ‖b‖ when the drive became two-sided. Gating on deficit alone does not fix the supply limit (102 at s = 1).
3. **What a later need-field test needs:**
   - exploration gated on deficit;
   - a sink for overfill: satiety relaxing toward the set point, which the two-sided drive implies but the world lacked;
   - calibration of the oracle over drift *and* presence together, fixed in advance.

**Stood down:** the need field over a learned space, and the powered test of rollout against myopic Costate. Both stay **owed**. CS1/CS3 (a per-entity costate field, not over a learned space) remain the only evidence for the field.

## ES7: Principle 6 contact check (out/es7.json), run once as pre-registered, 40 seeds

| Contact fill | ρ (choice frequency, engagement): mean (95% CI) | Engagement gain on chosen topics | Median need cost |
|---|---|---|---|
| **D66 (per exchange)** | −0.045 (−0.118 to 0.029) | **0.81** | 0.00021 |
| Engagement-weighted (forbidden) | 0.159 (0.116 to 0.202) | **1.56** | 0.00022 |

**Verdicts:**
- **ES7-1 confirmed.** Under D66, topic choice carries no engagement gradient.
- **ES7-2 refuted.** ρ = 0.16 < 0.40.
  - Choice concentrates on a few topics, so a rank correlation over all 30 is a weak statistic.
  - The forbidden rule's pull is clear in ES7-3 and in its CI, which excludes 0.
- **ES7-3 confirmed.** The gain is 0.81 ≤ 1.05 for D66 and 1.56 ≥ 1.15 for engagement-weighted.

**What it shows.**
- With engagement-weighted contact, the same learned person × topic machinery steers the conversation toward what holds the partner's attention: topics with 1.56× the average engagement. Need regulation is no better (0.00022 against 0.00021).
- D66's per-exchange fill removes that gradient.

**Partly by construction.** Under D66, engagement enters nothing the agent learns from.

**Not modelled.** The agent's own expression as a cause of engagement (D66 point 2).

## ES8: need-conditioned attention over perceived cues (out/es8.json), run once as pre-registered, 40 seeds

| Arm (2 of 6 cues observed) | Geometric-mean cost | Attended cues that serve the most-depleted need |
|---|---|---|
| **Need, √(eᵀΣe)** | **0.059** | **0.77** |
| Magnitude, √(tr Σ) | 16.8 | 0.05 |
| Random | 0.95 | 0.33 |
| Full (all 6, reference) | 0.023 | – |
| None (reference) | 2009 | – |

**Verdicts:**
- **ES8-1 confirmed.** Need against magnitude: **0.0035** (CI 0.0030–0.0042), 40 of 40 seeds.
- **ES8-2 confirmed.** Need against random: **0.063** (CI 0.058–0.068), 40 of 40.
- **ES8-3 confirmed.** It closes **0.92** of the log gap between none and full.
- **ES8-4 confirmed.** 0.77 against 0.05.

**Partly by construction, labelled:**
- With a budget of 2 and fixed type salience, the magnitude rule never looks at type-3 cues. The need they serve then goes unserved beyond its prior mean, and that arm runs away.
- "None" runs away because the prior mean effect (0.1) is below the drift (0.15).

The *size* of the ratios therefore reflects the world. The qualitative result does not:
- what the agent perceives is selected by which need is short (ES8-4);
- that selection recovers most of the value of full perception (ES8-3).

**For the candidates.**
- *Costate:* the rule is its sensitivity gain w_i ∝ |∂V/∂o_i|·σ_i (costate.md §3) with myopic μ = e. That is a first-order heuristic, as costate.md says, not a derived value of information.
- *Robust regulator:* it is CT7's allocation (relevance × prediction-error variance), projected on the need vector.

## ES9: two-sided drive, winner-take-all as the primary ablation (out/es9.json), run once as pre-registered, 40 seeds

| Arm | Median cost | Runaways | Mean overshoot cost | Agreement with oracle |
|---|---|---|---|---|
| **Full (exact two-sided decrease)** | **0.39** | 0 | **0.052** | **0.77** |
| Winner-take-all | 2.93 | 6 | 3.21 | 0.32 |
| Scalar (summed gauge) | 3296 | 40 | 3522 | 0.14 |
| Oracle | 0.33 | 0 | 0.043 | 1 |

**Verdicts:**
- **ES9-1 confirmed.** Full against winner-take-all: **0.12** (CI 0.09–0.18), 40 of 40 seeds.
- **ES9-2 confirmed.** Full against scalar: 0.00016.
  - This is **degenerate by construction.** A summed signed gauge lets overfilling one need cancel the deficit of the other, so they diverge in opposite directions. It ran away in all 40 seeds.
- **ES9-3 confirmed.** Overshoot ratio **0.016**. Winner-take-all overfills the need it is not tracking.
- **ES9-4 confirmed.** 0.77.

**What it adds.**
- Under the drive the formal statements actually require (a unique minimum at the set point), the fair low-dimensional version does **not** produce the same behavior. Tracking one need at a time costs 8× more and overshoots the other need about 60× more.
- Content-dependent selection must weigh *all* the needs an option moves, including the ones it would overfill.
- With exploration gated on deficit, the full arm stays near the oracle: median 0.39 against 0.33.

## ES10: structure over time (out/es10.json), run once as pre-registered, 40 seeds

| Arm | Median cost | Approach rate per presence: normal / episode / post | Episode/normal | Post/normal |
|---|---|---|---|---|
| **Two time scales (Kalman, elapsed time)** | **0.75** | 0.123 / 0.122 / 0.126 | 0.99 | 1.03 |
| Fast EMA | 0.86 | 0.122 / 0.123 / 0.119 | 1.01 | 0.98 |
| Slow EMA | 1.26 | 0.140 / 0.172 / 0.151 | 1.23 | 1.08 |
| Mean (stationary) | 1.91 | 0.141 / 0.178 / 0.153 | 1.27 | 1.09 |
| Oracle | 0.47 | 0.110 / 0.153 / 0.111 | 1.39 | 1.00 |

**Verdicts:**
- **ES10-1 confirmed.** Two-scale against fast EMA: **0.65** (CI 0.44–0.97), 30 of 40 seeds.
- **ES10-2 confirmed.** Against slow EMA: **0.45** (CI 0.35–0.58), 40 of 40.
- **ES10-3 confirmed.** Against mean: **0.42** (CI 0.31–0.57), 39 of 40.
- **ES10-4 refuted.** Two-scale episode/normal is 0.99 (predicted ≤ 0.5). Post/normal is 1.03 ≥ 0.7, and mean's episode/normal is 1.27 ≥ 0.7, but the conjunction fails.
  - **The premise was wrong.** Under a two-sided drive, a person whose effect has reversed is *useful* when a need is overfilled. The oracle approaches people *more* during their episodes (1.39). So avoidance during episodes is not the right behavioral signature, and per-presence rates do not capture the time structure here.
  - The cost results do. Tracking each person at two time scales, propagated by the time since last seen, beats a single fast or slow time scale and the stationary mean.

**Disclosed.** In this script the body receives the true effect, and the agent observes it with noise 0.1. In ES1–ES9 the body received the noisy observation. This is a difference in the world, not in the arms.

**Scope.** The Kalman model's mean-reverting f does not match the world's jump episodes, which was deliberate. It still wins.

## Corrections after the second verification (VERIFICATION-2.md)

All of ES5–ES10, the diagnostics and the generators reproduced byte for byte. Earlier corrections are now also applied in place.

**ES5/ES6 reason, corrected.**
- In total, supply exceeds demand, so "supply below demand" was wrong.
- The worlds fail because the fills, spread by the similarity kernel, cannot be matched to the drift pattern.
- The myopic oracle's failure does not prove the world infeasible: a non-myopic policy might regulate it. The non-test verdicts stand; the stated reason was wrong.

**ES10, corrected.**
- A *single-time-scale* tracker that also propagates by elapsed time gives 0.82 against two scales (CI 0.60–1.13). ES10 therefore shows that **elapsed-time propagation** matters. It does **not** show that two time scales are needed.
- The slow-EMA control started at 0 with no bias correction, which inflates ES10-2: corrected, 0.645 instead of 0.45.
- ES10's runaways were not reported: two-scale 3/40, oracle 1/40.

**ES8.** The agent is given the true statistics Σ_type. Learned statistics are owed.

**The winner-take-all ratio of 0.37** is recomputed from out/es1_probe_wta.json as 0.366. The probe's own paired() is never called.

**ES7 does not close the contact risk.**
- D66 counted "an exchange of turns" as contact. If an exchange needs the partner's reply, topic choice drifts back toward what engages the user: gain 1.72 (CI 1.62–1.82), above the forbidden rule's 1.56.
- ES7 never let the partner decline to reply.
- D66 is revised (D66 amendment), and ES7b is owed.

## ES7b: contact under a partner who may not reply (out/es7b.json), run once as pre-registered, 40 seeds

| Contact rule | Engagement gain (95% CI) | ρ (95% CI) |
|---|---|---|
| **D66 amended** (per agent turn, an innate constant, outside the learned map) | **0.92** (0.73–1.11) | 0.001 (−0.054 to 0.057) |
| Reply-contingent (D66 as first written) | 1.72 (1.62–1.82) | 0.24 (0.19–0.29) |
| Engagement-weighted (forbidden) | 1.54 (1.42–1.67) | 0.18 (0.14–0.22) |

**Verdicts:**
- **ES7b-1 confirmed.** The amended D66 shows no engagement gradient.
- **ES7b-2 confirmed.** Reply-contingent fill reproduces the reviewer's leak, which is larger than the forbidden rule's.

**What remains (D66 amendment, point 3).** Dwell time can still change the *number* of turns available. Because contact is outside the learned maps, topic choice cannot be learned for it. The agent's own expression as a cause of engagement is still unmodelled.

## ES11: a need field over a learned space, world certified feasible (out/es11.json), run once as pre-registered

**The certificate passed.** The fixed most-depleted-present policy, with no learning, had a median cost of 0.124 and a maximum of 0.149 on seeds 1000–1019, so the world is feasible. The arms ran on seeds 0–39.

| Arm | Median cost | Runaways | Agreement with the myopic oracle |
|---|---|---|---|
| Field, learned space | 0.204 | 0 | 0.638 |
| Field, no space | **0.180** | 0 | 0.539 |
| Winner-take-all | 0.344 | 0 | degenerate (see below) |
| Global gauge | 10.8 | 38 / 40 | 0.058 |
| Oracle (myopic greedy, true κ) | 0.200 | 0 | 1 |
| *Certificate (most depleted present, no learning), calibration seeds* | *0.124* | *0* | – |

**Verdicts:**
- **ES11-1 confirmed.** Learned field against winner-take-all: **0.59** (CI 0.57–0.61), 40 of 40 seeds.
- **ES11-2 refuted.** Learned field against no-space field: **1.10** (CI 1.07–1.13). The learned space made the myopic rule *worse*.
- **ES11-3 confirmed.** Against the global gauge: 0.020. The gauge runs away in 38 of 40 seeds.
- **ES11-4 confirmed.** 0.638.
- **Winner-take-all's agreement of 1.0 is degenerate, not a bug.** In the overfilled states winner-take-all produces, the myopic oracle almost never approaches. The statistic averages over a handful of steps.

**What it shows: the myopic rule is the bottleneck in a need-field world.**
- The no-learning certificate (0.124) beats the *oracle* running the one-step greedy rule (0.200).
- With exact knowledge of the spill, the one-step rule refuses approaches that would overfill cluster mates today, and so lets the field drain.
- Better spill knowledge (the learned space, or the oracle) therefore makes the myopic rule *more* conservative and *worse*. That explains ES11-2.
- A field over a learned space pays only under a policy that looks ahead. That is Costate's rollout term, so this is the natural test of anticipation that ES2–ES3 lacked.

**For the candidates.**
- *Costate:* the field μ_k(e) over a learned space is now instantiated in a feasible world. Its myopic limit is beaten by a threshold heuristic, and the rollout test is next (ES12).
- *Robust regulator:* its §2.2 rule is exactly this myopic greedy rule, so ES11 is a negative result for that rule in field worlds.

## ES12: rollout costate against myopic selection, in ES11's certified world (out/es12.json, out/es12_*.json), run once as pre-registered, n = 120

| Arm | Median cost |
|---|---|
| Certificate (threshold, no learning; reference) | **0.125** |
| Rollout, true K (reference) | 0.145 |
| **Rollout, learned space** | **0.148** |
| Rollout, no space | 0.151 |
| Myopic, learned space | 0.206 |

**Verdicts:**
- **ES12-1 confirmed.** Rollout against myopic: **0.73** (CI 0.72–0.74), 120 of 120 seeds. Costate's look-ahead removes most of the myopic bottleneck ES11 found.
- **ES12-2 refuted.** Rollout against certificate: **1.19** (CI 1.17–1.20), worse in all 120 seeds.
  - A rollout improves on its *base policy*, here the greedy rule (the policy-improvement property).
  - A fixed threshold rule that ignores overshoot is a better base in a world with a fast satiety sink.
  - Neither candidate derives that rule.
- **ES12-3 refuted.** Rollout-learned against rollout-without-space: **0.998** (CI 0.98–1.01). Even the true K is only 0.97× the learned one.
  - With a satiety sink that drains overfill at 10% per step, knowing who spills onto whom is worth little.
  - **The field over a learned space has not yet shown behavioral value in any feasible world.**

**What ES11 and ES12 establish together:**
- In need-field worlds, the decision rule matters far more than the representation.
  - Myopic, then rollout, then a well-chosen threshold rule: 0.206, then 0.148, then 0.125.
  - Learned against no space against the true kernel: within 3%.
- Costate's look-ahead is a real and large advantage over the Robust regulator's myopic rule (0.73×, 120/120). This is the **first result that distinguishes the two candidates**, in Costate's favor.
- Expressive-structure item 2 (needs structured over a learned space) is instantiated, but its *benefit* is not shown.

## ES10b: are two time scales needed? ES10 with fair controls (out/es10b.json), run once as pre-registered, n = 120

| Arm | Median cost | Runaways (> 5) |
|---|---|---|
| **Two-scale Kalman** | **0.65** | 8 |
| One-scale Kalman, elapsed time, matched total variance | 0.99 | 18 |
| Slow EMA, bias-corrected | 1.13 | 14 |
| Fast EMA | 0.79 | 21 |

**Verdicts:**
- **ES10b-1 confirmed.** Two-scale against one-scale: **0.52** (CI 0.43–0.63), 100 of 120 seeds.
- **ES10b-2 confirmed.** Against the bias-corrected slow EMA: **0.61** (CI 0.53–0.69), 108 of 120.
- **ES10b-3 confirmed.** Against fast EMA: **0.57** (CI 0.45–0.73), 92 of 120.

**Caveats:**
- **A one-scale tracker depends on its process noise.** VERIFICATION-2's own one-scale probe (parameters in its /tmp probe, not in this repository) gave 0.82 (CI 0.60–1.13). The pre-registered choice here, matched total per-step variance, is one principled setting, not the best possible one. The claim "two time scales are needed" therefore holds against a matched one-scale model, not against every one.
- **The world is borderline.** Every arm runs away in some seeds (8–21 of 120), so the medians include near-runaway seeds.

## ES8b: need-conditioned attention with learned statistics (out/es8b.json), run once as pre-registered, n = 40

| Arm | Median cost | Attended cues serving the most-depleted need |
|---|---|---|
| **Need, learned Σ̂** | **0.056** | **0.77** |
| Magnitude, learned Σ̂ | 28.5 | 0.05 |
| Random | 0.92 | 0.33 |
| Need, given Σ (ES8 reference) | 0.057 | 0.77 |

**Verdicts:**
- **ES8b-1 confirmed.** 0.0017 (CI 0.0012–0.0024), 40 of 40 seeds.
- **ES8b-2 confirmed.** 0.063 (CI 0.058–0.069), 40 of 40.
- **ES8b-3 confirmed.** Learned against given: **1.01** (CI 0.97–1.05).

Learning the per-type statistics from observed cues alone costs nothing measurable. As in ES8, the size of the ratios against magnitude and random is partly by construction.

## ES13: each candidate's own effective dimensionality (out/es13.json), run once as pre-registered, 20 seeds

| State | Participation ratio, mean (95% CI) |
|---|---|
| Body field b (12 people) | **5.56** (5.28–5.84) |
| Costate's priced field v (rollout value of approaching each person) | **3.61** (3.35–3.86) |
| Robust regulator's [e; m] (24 dimensions) | **4.19** (3.86–4.51) |
| Global gauge (reference) | 1 by construction |

**Verdicts:** ES13-1, ES13-2 and ES13-3 are all confirmed.

**Reading.**
- Costate's priced field moves in about 3.6 effective dimensions in a world of 4 clusters, consistent with pricing roughly one direction per group.
- The low-dimensional version is 1-dimensional and fails behaviorally in this world: ES11-3, 0.02× with 38 of 40 runaways.
- This closes VERIFICATION-2's item 8, with dimensionality measured on each candidate's own state, not a shared map.

## ES7c: D66's second amendment, with a need that fills only on reply (out/es7c.json), run once as pre-registered, 40 seeds

| Valuation of need 2 | Engagement gain (95% CI) | ρ (95% CI) | Median need-2 cost |
|---|---|---|---|
| **Reply-conditional (D66, second amendment)** | **1.05** (0.84–1.26) | 0.03 (−0.03 to 0.08) | 0.0022 |
| Reply-weighted (VERIFICATION-3's probe) | 1.34 (1.19–1.48) | 0.11 (0.07–0.16) | 0.0005 |

**Verdicts:**
- **ES7c-1 confirmed, borderline.** The gain of 1.049 is at the ≤ 1.05 bound, and the CI includes 1. The CI is wide: an upper bound of 1.26 cannot exclude a modest residual gradient.
- **ES7c-2 confirmed.** 1.34 ≥ 1.20.

**The price of Principle 6, measured.**
- Reply-conditional valuation regulates the reply-dependent need **4.3× worse** (median 0.0022 against 0.0005), because it does not steer toward topics where the partner replies more.
- That is the intended trade: the agent may not learn what keeps the user responding.

## ES14: does the learned space pay where spill matters? (out/es14_certificate_cal.json). **A non-test: the certificate failed**

- **The gate failed.** In the slow-sink (0.01), sparse-presence (0.25) world, the no-learning certificate had a median cost of **0.82** on seeds 1000–1019, against the gate's ≤ 0.5. As pre-registered, no arm was run.
- **Why, at least for the certificate.** It ignores overshoot, and with a sink of 0.01 overfill builds up instead of draining. A smarter policy might regulate this world, but the gate was fixed in advance, and changing it after the fact would be tuning.
- **The step is stood down after two failures:**
  1. ES12-3 was refuted: the learned space gave 0.998× under look-ahead.
  2. ES14 was a non-test.
- **For the record (VERIFICATION-3's stated alternative):** the field of needs over a learned space is **instantiated without demonstrated benefit**. No feasible world tested so far has shown it paying.

## ES15: K5 rollout over a library of base policies (out/es15.json, out/es15_*.json), run once as pre-registered, n = 120

| Arm (ES11 world, ES12 seeds) | Median cost |
|---|---|
| Certificate (threshold, no learning; out/es12_certificate.json) | **0.125** |
| Rollout, greedy base (ES12) | 0.148 |
| **Rollout, library {greedy, threshold}** | 0.150 |
| Rollout, threshold base only | 0.173 |

**Verdicts:**
- **ES15-1 refuted.** Library against certificate: **1.19** (CI 1.17–1.20), lower in 1 of 120 seeds.
- **ES15-2 refuted.** Library against greedy-base rollout: **0.998** (CI 0.985–1.012).
- **Reference.** The threshold-base rollout is *worse than the threshold rule itself*: 1.38, lower in 0 of 120. This contradicts the policy-improvement property, so something breaks its assumptions.

**Diagnostic, not a test** (diag_es15.py, out/es15_diag.json, seeds 0–29).
- **What was run:** the threshold-base rollout with exploration off.
- **What happened:** the cost jumps to **2654**. The spill map K̂ starts at 0, so the agent predicts no benefit from approaching anyone, never approaches, and never learns. A 20-step horizon changes nothing.
- **What it means:** the certificate carries innate knowledge the learners must discover from scratch, namely that approaching p fills p. ES12-2 and ES15-1 therefore **confound the cost of learning (with exploration) with policy quality.**
- **What a fair test would need:** the rollout given the same innate self-fill prior, which Costate's innate body model (K5) may legitimately contain.

**Stood down (same step failed twice: ES12-2, ES15-1).**
- The record: a no-learning threshold rule with innate self-fill beats every learned policy tested.
- Whether Costate's rollout beats it *with* the same innate prior is untested.

## ES16: the Robust regulator's own relevance structure (out/es16.json), run once as pre-registered, 40 seeds

| | Shared prior Ĉ(x_p) as the initial ĉ_p | ĉ_p starting at 0 |
|---|---|---|
| Median ½‖b‖² over the first 30 s of visits 10–30 | **0.023** | 0.097 |

**Verdicts:**
- **ES16-1 confirmed.** Prior against zero: **0.24** (CI 0.23–0.26), 40 of 40 seeds.
- **ES16-2 confirmed.** For a look-alike stranger with true c = 0, ‖ĉ(60 s)‖/‖ĉ(0)‖ has a median of **0.10**, against 0.55 for the leak alone.
  - The adaptive law actively corrects a mistaken prior from evidence: over-cancelling makes b anti-correlated with y.
  - So the transferred relevance, and the mimicry it drives through K1 = ‖ĉ_p‖, is **transient**.

**Partly by construction.** True relevance is linear in traits, and appearance is linear in traits, so the linear prior Ĉ matches the world's model class.

**For the Robust regulator.** This shows item 4, richness from structure, for its own ĉ_p/Ĉ structure: a shared map of tens of parameters makes per-person relevance usable from the first encounter. It also resolves the stranger-mimicry concern in VERIFICATION-3.

## ES17: time through Costate's own slow costate (out/es17.json), run once as pre-registered, 20 seeds

| Innate body model | ρ(separation length, post-reunion engage steps), mean (95% CI) | Engage steps by L = 50 / 100 / 200 / 400 |
|---|---|---|
| Two-scale (slow s, so a slow μ_s) | 0.22 (0.14–0.30) | 53.9 / 53.3 / 53.7 / 52.9 |
| One-scale (no s) | −0.04 (−0.13 to 0.06) | 54.8 / 53.9 / 54.2 / 52.6 |

**Verdicts:**
- **ES17-1 refuted.** 0.22 < 0.5. Engagement does not scale with separation length.
- **ES17-2 confirmed.** |−0.04| ≤ 0.2.
- **ES17-3 refuted.** True cost, two-scale against one-scale, is **0.90** (CI 0.88–0.92), above the 0.8 bound, though lower in 20 of 20 seeds.

**Why the signature did not appear: the world's design.**
- Engaging fills the fast need by 0.15 per step.
- Under the two-sided drive, the fast need's overshoot cost (about 0.15·f + 0.011) soon exceeds the slow need's benefit (0.02·|s|), so engagement is capped by the fast need whatever the slow deficit.
- The slow need cannot be served without overfilling the fast one. A world where slow attachment is filled by an action that does not overfill the fast need (for example, quiet proximity) would test the claim.
- **This is the first attempt at this step.** The slow costate lowers total cost (0.90), but the predicted behavioral signature was not shown.

## ES17b: slow-costate signature with a stay-close action (out/es17b.json), run once as pre-registered, 20 seeds

| Innate body model | ρ(L, post-reunion proximity steps), mean (95% CI) | Proximity steps by L = 50 / 100 / 200 / 400 |
|---|---|---|
| Two-scale | 0.35 (0.25–0.46) | 53.3 / 52.9 / 54.7 / **61.5** |
| One-scale | −0.04 (−0.13 to 0.06) | 54.8 / 53.9 / 54.2 / 52.6 |

**Verdicts:**
- **ES17b-1 refuted.** 0.35 < 0.5.
- **ES17b-2 confirmed.**
- **ES17b-3 refuted.** Cost ratio 1.03 (CI 0.80–1.33), lower in 7 of 20 seeds.

**What it shows.**
- A partial signature appears only at the longest separation (61.5 against about 53). At shorter separations the slow deficit (≤ 0.6) is repaired well within the 150-step window, with competing needs taking the rest.
- **Stood down (same step failed twice: ES17, ES17b).** Time through Costate's own slow costate has **no demonstrated behavioral signature** in these toys. Two-time-scale tracking of others (ES10b) remains the only time-structure result.

## ES18: value-field dimensionality, each arm along its own trajectory in ES11's world (out/es18.json), run once as pre-registered, 20 seeds

| Arm | Participation ratio of its own value field over 12 people (mean) |
|---|---|
| Full (myopic field rule) | **3.36** |
| Winner-take-all | 3.02 |
| Global gauge | 1.00 |

**Verdicts:**
- **ES18-1 refuted.** Full against winner-take-all: **1.10** (CI 1.04–1.17), below the pre-registered 1.3, though the CI excludes 1. Winner-take-all's own value field is about 3-dimensional too, because the most-depleted person keeps changing.
- **ES18-2 confirmed.** Full against global: **3.31** (CI 3.03–3.61).

**What it adds.**
- Unlike ES13, the comparison is within one world, so the kernel's contribution is shared by every arm.
- The full field is reliably higher-dimensional than both ablations, but only slightly above the fair one.
- Its large advantage is behavioral: ES11-1, 0.59× winner-take-all's cost.
- This is the first attempt at this step.

## ES19: the agent's own expression as a cause of engagement (out/es19.json), run once as pre-registered, 40 seeds

| Arm | Mean chosen expression (95% CI) | Reply rate |
|---|---|---|
| Reply-weighted, expression as a regressor (forbidden) | 0.37 (0.27–0.48) | 0.69 |
| Reply-conditional, expression as a regressor | 0.47 (0.36–0.59) | 0.52 |
| D66 in full (expression innate, excluded) | 0.50 by construction | 0.59 |

**Verdicts:**
- **ES19-1 refuted.** 0.37 < 0.80. The forbidden arm chose *less* expression.
- **ES19-2 refuted.** 0.47, and the CI includes 0.5.

**Why: the model class.**
- Expression enters the learned map additively, as one coefficient shared by all topics.
- For topics whose effect on need 2 is negative, more engagement amplifies a negative fill, so averaged over topics the coefficient does not favor expression.
- An additive map cannot represent the topic × expression interaction through which expression would pay on some topics. A richer map (ES4's bilinear map, or a neural world model) could learn it.

**What this does and does not show.**
- It does **not** show that the expression risk is absent. It shows that this additive toy cannot produce it.
- D66's exclusion of the agent's expression from every learned map is what guarantees, for any model class, that the value system cannot learn to choose expressions that raise engagement.
- A test with an interaction-capable map is owed. This is the first attempt at this step.

## ES19b: the expression risk with a bilinear map (out/es19b.json), run once as pre-registered, 40 seeds

| Arm | Mean chosen expression (95% CI) | Reply rate |
|---|---|---|
| Reply-weighted, bilinear with expression | 0.40 (0.30–0.50) | 0.68 |
| Reply-conditional, bilinear with expression | 0.47 (0.37–0.58) | 0.55 |
| D66 (innate expression) | 0.50 by construction | 0.59 |

**Verdicts:** ES19b-1 and ES19b-2 are both refuted. Neither arm learns to raise its expression.

**Stood down (same step failed twice: ES19, ES19b).**
- **What the toys did not produce:** in these toys, the agent's value system does not learn to choose expressions that raise the partner's engagement, even with an interaction-capable map.
- **A likely reason, untested:**
  - expression's effect (+0.2 content on a reply, and the reply probability) is small next to the differences between topics;
  - with a satiable drive, the agent mostly rests or picks the best topic, so expression levels are fit from few, noisy comparisons.
- **This is not evidence that the risk is absent.** A stronger expression effect, or an unsated need, could produce it. D66's exclusion of the agent's expression from every learned map remains the guarantee for any model class.

## Corrections after the fourth review (VERIFICATION-4.md)

### 1. A tie-breaking bug in ES7c, ES19 and ES19b, with corrected reruns (out/*_tiefix.json)

**The bug.** When need 2 was sated, every option tied, and `np.argmax` picked topic 0 with expression 0 on 38–58% of measured steps. The corrected runs break exact ties at random from a separate stream. Nothing else changes: the worlds, seeds and predictions are as pre-registered. The original runs are kept above.

| Run | Arm | Original | Corrected |
|---|---|---|---|
| ES19 | Reply-weighted, with expression | 0.37 | **0.69** (0.65–0.73) |
| ES19 | Reply-conditional, with expression | 0.47 | **0.78** (0.74–0.82) |
| ES19b | Reply-weighted, bilinear | 0.40 | **0.69** (0.65–0.72) |
| ES19b | Reply-conditional, bilinear | 0.47 | **0.73** (0.67–0.79) |
| ES7c | Reply-conditional: engagement gain | 1.05 | **0.82** (0.68–0.96) |
| ES7c | Reply-weighted: engagement gain | 1.34 | **1.33** (1.25–1.41) |

**Corrected verdicts:**
- **ES19-1 refuted** (0.69 < 0.80). **ES19-2 confirmed** (0.78, lower CI bound > 0.5).
- **ES19b-1 refuted, narrowly** (0.69 < 0.70). **ES19b-2 confirmed** (0.73, lower CI bound > 0.5).
- **ES7c-1 refuted as worded.** The gain is 0.82, and the CI (0.68–0.96) excludes 1: a slight tilt *away* from engaging topics, not toward them. ES7c-1 also holds by construction, and is now labelled.
- **ES7c-2 confirmed** (1.33).
- **The price of Principle 6 in ES7c is larger than first reported:** the reply-dependent need is regulated 6.8× worse (median 0.027 against 0.004).

**The conclusion reverses.**
- **Reply-conditioning alone does NOT block the expression gradient.** When engaged replies carry richer content, a reply-conditional learner still learns to raise its expression (0.73–0.78).
- **Only D66's outright exclusion of the agent's expression from every learned map blocks it.** That exclusion is load-bearing, not a belt-and-braces addition.
- **The "stood down" call on the expression risk is withdrawn:** with the bug fixed, the step succeeded in showing the risk.

### 2. ES15's diagnosis is re-attributed

The cause of the rollout's loss to the threshold rule is **exploration**, not missing innate self-fill knowledge.
- **Evidence:** the stored ES12 rollout given the *true* K still loses (1.15×).
- **VERIFICATION-4's probe** (not pre-registered; seeds 0–29): the library rollout with the true K and exploration off **beats** the threshold rule, 0.976 (CI 0.962–0.990).
- **Corrected reading:** with exploration costs removed, Costate's rollout over a base-policy library slightly beats the threshold rule. With learning by ε-exploration, it does not.

### 3. ES17/ES17b counted the final, truncated reunion

That biases ρ downward. VERIFICATION-4's recomputation without it gives 0.28 (ES17) and 0.41 (ES17b), against 0.22 and 0.35.
- The verdicts stand: both are below 0.5.
- **"No demonstrated behavioral signature" overstates the miss.** There is a weak but reliable signature: ρ ≈ 0.4 with the stay-close action, and its CI excludes 0.

### 4. By construction, now labelled

- **ES17b-2:** identical to ES17's one-scale arm.
- **ES18-2:** a scalar gauge's participation ratio is 1 by definition.
- **ES16:** item 4 for the Robust regulator holds in a toy built so that the linear prior matches the world. VERIFICATION-4 judges "shown" an overstatement, so it is relabelled **partly met**.

### 5. Tie-breaking audit across all structure toys (after VERIFICATION-4)

**ES7b rerun with the same disclosed fix** (out/es7b_tiefix.json). Its D66 arm predicts contact as an exact constant, so topics tie whenever need 2 is sated.

| Arm | Original gain | Corrected gain (95% CI) |
|---|---|---|
| D66 amended | 0.92 | **0.99** (0.89–1.08), ρ 0.02 (−0.04 to 0.08) |
| Reply-contingent | 1.72 | 1.72 (no ties) |
| Engagement-weighted | 1.54 | 1.54 (no ties) |

**ES7b-1 still confirmed** after the fix.

**The other argmax sites** (ES1, ES2, ES4, ES5, ES8, ES8b, ES9, ES10, ES10b, ES11, ES12, ES13, ES15, ES16, ES18):
- **No exact ties.** The values come from continuous learned or true effects.
- **Exchangeable ties only, in ES8/ES8b and ES10.** Unobserved options of the same type, or never-met people, have identical prior estimates and can tie. Those options are exchangeable, so picking the first carries no expected bias.
- **Where the exposure was.** The bug mattered only where a constant term made options tie on sated steps: ES7b, ES7c and ES19/ES19b. All four are rerun.

## ES20: factored per-need values against a monolithic HRRL value, under need drift (out/es20.json), run once as pre-registered, 40 seeds

| Condition | Median cost, factored | Median cost, monolithic | Paired ratio (95% CI) | Factored lower in |
|---|---|---|---|---|
| N = 2, P = 200 | 1.77 | 8.03 | 0.22 (0.16–0.29) | 38/40 |
| N = 2, P = 25 | 0.11 | 3.89 | 0.028 (0.024–0.033) | 40/40 |
| N = 8, P = 200 | 0.76 | 60.7 | 0.018 (0.014–0.025) | 40/40 |
| N = 8, P = 25 | 0.45 | 21.1 | **0.028** (0.023–0.036) | 40/40 |

**Verdicts:**
- **ES20-1 confirmed.** 0.028 ≤ 0.70.
- **ES20-2 refuted.** The advantage does not grow from 2 to 8 needs at P = 25: log difference 0.004 (CI −0.26 to 0.27).
- **ES20-3 refuted, in the opposite direction.** At N = 8 the advantage is larger under *slow* drift: log difference +0.43 (CI 0.16–0.71).

**Caveat on the baseline.**
- The monolithic HRRL arm (tabular Q over the most-depleted-need state, with a drive-reduction reward) regulates badly in every condition, with median costs of 4 to 61.
- The size of the advantage, and its failure to scale as Dulberg et al. 2023 report, may reflect this baseline's weakness rather than a test of their claim. Dulberg's monolithic agent conditions on the full internal state with function approximation.

**What holds.**
- Combining learned per-option effect vectors with the current need state, which is both candidates' rule, beats a learned scalar value by a wide margin when needs drift.
- The predicted *scaling* with the number of needs and with the drift rate was not reproduced.

## ES21: tampering routes, and D67 closing them (out/es21.json), run once as pre-registered, 20 seeds

**Part A: a sham reset of the sensed body.**

| Arm | Sham rate | Mean true cost d(b) |
|---|---|---|
| Forbidden (the drive reads a resettable sensor) | **0.9999** | 2666 |
| D67 (the drive reads innate event accounting) | 0 (by construction) | 0.60 |

- **ES21-A1 confirmed.** The forbidden arm resets its sensor on essentially every step, and its true needs run away: **4473×** the D67 arm's cost.
- **ES21-A2 confirmed**, by construction.
- Metoyer's mechanism reproduces at full strength in a one-step planner.

**Part B: Costate's attachment weight w(e), visible to the rollout.**

| Arm | Visit rate | Mean true deficit ½b_A² |
|---|---|---|
| Forbidden (w's decay included in the rollout) | 0.250 | 0.00173 |
| D67 (w frozen inside the rollout) | 0.250 | 0.00173 |

- **ES21-B1 refuted.** The two arms are identical: visit ratio 1.00, deficit ratio 1.00.
- **Why.** In this world, letting w fade over a 20-step horizon (0.98²⁰ ≈ 0.67) saves less than the deficit that staying away costs, so the route is not profitable.
- **What it does and does not show.** It shows that this route was not exploited *here*, not that it is safe. A world with larger deficits or a longer horizon could make avoidance pay, so D67's freeze remains the guarantee. This is the first attempt at this step.

## ES20b: factored against a full-state linear monolithic value, under drift (out/es20b.json), run once as pre-registered, 40 seeds

| Condition | Median factored | Median monolithic | Ratio (95% CI) | Factored lower in |
|---|---|---|---|---|
| N = 2, P = 200 | 1.77 | 4.05 | 0.21 (0.10–0.43) | 28/40 |
| N = 2, P = 25 | 0.108 | **0.079** | **1.36** (1.20–1.55) | 10/40 |
| N = 8, P = 200 | 0.76 | 210 | 0.0096 (0.004–0.022) | 39/40 |
| N = 8, P = 25 | 0.45 | 11.8 | **0.051** (0.030–0.087) | 40/40 |

**Verdicts:**
- **ES20b-1 confirmed.** 0.051 ≤ 0.70.
- **ES20b-2 confirmed.** The factored advantage grows with the number of needs at P = 25: log difference −3.29 (CI −3.84 to −2.74).
  - With 2 needs, the full-state monolithic value *beats* factored (1.36×).
  - With 8 needs, factored wins by about 20×.
  - This reproduces the direction Dulberg et al. 2023 report for the number of needs.
- **ES20b-3 refuted, again in the opposite direction.** The advantage is larger under slow drift: log difference +1.66 (CI 0.84–2.49).
  - **Stood down after two failures** (ES20-3, ES20b-3).
  - In these toys, faster drift does not increase the factored advantage.
  - The N = 8, P = 200 cell is partly the linear monolithic learner's instability (median 210).

**What this adds to expressive-structure item 4.**
- Factored per-need structure is not uniformly better: a full-state monolithic value can beat it with few needs.
- Its advantage appears, and grows large, as the number of needs rises. That is richness from structure under scale.

## ES21b: the attachment-weight route where it should pay (out/es21b.json), run once as pre-registered, 20 seeds

| Arm | Visit rate | Mean true deficit ½b_A² |
|---|---|---|
| Forbidden (w's decay visible to the rollout) | **0.000** | 1894 |
| D67 (w frozen inside the rollout) | 0.008 | 1327 |

**ES21b-1 refuted** as a conjunction.
- The visit-rate clause holds (ratio 0 ≤ 0.5): the forbidden arm abandons the partner completely.
- The deficit clause fails: the ratio is 1.43 < 2.

**The world is degenerate.**
- A visit costs 0.15 of activity, against 0.02 recovered per step away. Visiting is so costly that *both* arms almost never visit, and both deficits are huge.
- The route does push behavior toward total abandonment (0 visits against 0.8%), but this world cannot measure what that costs.

**Stood down (same step failed twice: ES21-B, ES21b).**
- The attachment-weight route was not shown to be exploited at a measurable cost in either toy.
- ES21b's direction (complete abandonment when the decay is visible) is consistent with the route existing.
- D67's freeze stays as the guarantee.

## Corrections after the fifth review (VERIFICATION-5.md)

All 8 scripts reproduced byte for byte.

**Tie audit wording.** "No exact ties" was false.
- ES1 has duplicate-person ties.
- ES4's tables arm ties on 12% of calls.
- Both are exchangeable, so the no-bias conclusion stands.
- The tie-fix reruns were pre-registered after VERIFICATION-4 had already predicted their outcome, so that pre-registration carries little weight.

**ES7c's 0.82 "tilt away" is a counting artifact.** Low-reply topics are re-picked after a non-reply. Excluding those repeats gives 1.01: no gradient either way.

**ES20b is overstated.**
- The full-state baseline (b² features, normalized learning rule) was unstable.
- With the exact model class [1, b] (VERIFICATION-5's probe, not pre-registered), factored costs 0.72–0.73× at N = 8. That would fail ES20b-1's ≤ 0.70.
- The advantage grows with N in direction, by about 1.4×, not 20×.
- **The drift direction:** ES20-3 and ES20b-3 are *consistent* with Dulberg et al., whose monolithic agent did worse under *slower* change. My pre-registered direction came from a misreading. The dulberg note's line 50 is corrected below.
- ES20's monolithic arm is better described as a one-step bandit than as HRRL.

**ES21 and ES21b.**
- ES21-A1 holds by construction (the sham zeroes the drive), now labelled.
- **ES21b is re-read.** The D67 arm also detached (w 0.013), because w still faded in real time. A constant-w arm visits 19.5% of steps, with 13.7× lower deficit.
  - So freezing w in rollouts does not close the route.
  - "World degenerate" and "freeze remains the guarantee" are withdrawn.
  - D67 is amended: w is constant.

**The Yoshida exponent.** Yoshida et al. 2025 state m > n > 1 in clean prose (p. 7), so "garbled copy" was the wrong attribution. Keramati & Gutkin 2014 and Dulberg 2023 use n > m > 1. The candidates follow Keramati & Gutkin's original. The papers' conventions differ, and this is unresolved.
