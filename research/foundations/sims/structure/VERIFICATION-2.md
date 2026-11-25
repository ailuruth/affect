# Verification 2 of the expressive-structure test bed (ES5–ES10, corrections, candidate claims)

Independent check, 2026-11-25. I did not write this work and edited no existing file. Reruns and probes ran in a copy at /tmp/esv2 (probes in /tmp/esv2/probe/, not committed). Line references are to the files as they stand now.

## Summary verdict

- **Reproducible.** ES5a, ES5b, ES6, the ES6 diagnostic, ES7, ES8, ES9, ES10, both generators and the winner-take-all probe all reproduce **byte for byte**.
- **Honest about the failures.** ES5 and ES6 are reported as non-tests, ES7-2 and ES10-4 as refuted, and the smoke run is disclosed.
- **The corrections were appended, not applied.** RESULTS.md:135-166 is right, but the text it corrects is still in place: RESULTS.md:15, :19, :28, :46, :130-133. The candidate documents and STATUS.md still contradict themselves, as in VERIFICATION.md.
- **Three new substantive problems:**
  1. **D66 does not close the contact risk.** D66 counts "an exchange of turns" as a contact event (DECISIONS.md:134). If an exchange needs the partner to reply, the engagement gradient comes back at a gain of **1.72**, which is larger than the forbidden rule's 1.56 (probe below). ES7 never models a partner who can decline to reply.
  2. **The rule in robust-regulator.md §2.2 is not the rule ES9 tested.**
     - It has the wrong sign under §2.1's own e = b − b*.
     - It is first-order. With the sign fixed, the first-order rule costs **1.84×** the exact decrease ES9 used.
  3. **ES10 does not isolate "two time scales".**
     - A one-scale Kalman filter with elapsed-time propagation is not distinguishable from it: 0.82, CI 0.60–1.13.
     - The slow-EMA control starts at 0 with no bias correction, which inflates ES10-2.
- **Expressive structure: neither candidate is complete.**
  - Every toy uses the *myopic* rule, which is the same for both candidates.
  - Needs as a field over a learned space (item 2) are still not shown.
  - Costate's distinctive rollout term is still unconfirmed.
  - For the Robust regulator, cue attention (ES8) and two-scale tracking (ES10) are add-ons to its formal statement.

## Reruns

| Output | Script | Match |
|---|---|---|
| out/es5a.json, out/es5b.json | sim_es5_field.py a / b | byte-identical |
| out/es6.json, es6.err (empty) | sim_es6_calibrated.py | byte-identical |
| out/es6_diag_exploration.json | diag_es6_exploration.py | byte-identical |
| out/es7.json | sim_es7_contact.py | byte-identical |
| out/es8.json | sim_es8_attention.py | byte-identical |
| out/es9.json | sim_es9_twosided.py | byte-identical |
| out/es10.json | sim_es10_time.py | byte-identical |
| out/es1_per_seed.txt, out/es_paired_exploratory.txt | make_es1_per_seed.py, make_es_paired_exploratory.py | byte-identical |
| out/es1_probe_wta.json | probe_winner_take_all.py | byte-identical |

**Every number in RESULTS.md:168-314 matches the outputs.** Minor gaps:
- **The paired 0.37 is not produced by any script.** probe_winner_take_all.py:19-21 defines `paired()` against a key, `costs_full`, that does not exist, and never calls it. The figure can be recomputed from the rounded costs in out/es1_probe_wta.json: 0.366 (CI 0.171–0.783), 15/20.
- **The ES6 trace claim is not saved anywhere.** RESULTS.md:214 says seed 1000 at s = 0.125 with exploration off costs 1.5. I re-derived it: 1.536.
- **ES10 does not report runaways (cost > 5),** although ES9 does. They are:

  | Arm | Runaways (of 40) |
  |---|---|
  | Two-scale | 3 |
  | Fast EMA | 7 |
  | Slow EMA | 11 |
  | Mean | 11 |
  | **Oracle** | **1** |

  The world is near-infeasible for some seeds.
- **ES5a's winner-take-all agreement is NaN** (out/es5a.json:137). It does not affect any verdict.

## Spec against code; pre-registration

**ES5 (PREDICTIONS.md:165-232 against sim_es5_field.py).**
- **The code matches the spec:** the world, the kernel, the schedule, the feature sets, the winner-take-all and global arms, the rollout over 10 steps with the known schedule, seeds 40/120, and the ‖b‖ > 0.3 exploration gate.
- **The smoke run is disclosed** (RESULTS.md:170).
- **The non-test verdict is right, but the reason given is not.** RESULTS.md:182 says "supply … below demand". In seed 1000, aggregate supply is about 0.28 approaches × 1.73 total fill ≈ 0.48 per step, which is *above* the demand of 0.37.
  - I solved a fluid-limit linear program: rates bounded by presence, minimizing the worst per-person net drift. Across seeds 1000–1009 it leaves a residual of 0.002–0.015 per step.
  - The world is infeasible because the kernel's columns cannot match the drift profile, not because supply is short.
  - "The oracle ran away" does not by itself show infeasibility, because the oracle is the *myopic* greedy rule (sim_es5_field.py:59). The same point applies to ES6's calibration criterion (PREDICTIONS.md:240).
- **Pre-registration:** written before the run; the claim cannot be checked from file times.

**ES6 (PREDICTIONS.md:234-249).**
- **Written after ES5, and disclosed (PREDICTIONS.md:236).** The grid, the oracle-only calibration, the criterion and the stopping rule all match sim_es6_calibrated.py:10-17.
- **No scale met the criterion.** It was correctly declared a non-test and stood down.
- **The diagnostic is labelled as such.**

**ES7 (PREDICTIONS.md:251-279).**
- **The code matches** on B's variance of 1/6, g, the need-2 fill, drift, the cap, the exploration gate, ridge regression on [1, t_k], and fills of 0.3 against 0.6g.
- **ES7-1 holds largely by construction:** g depends on y[4:6], while the agent's need-2 effect depends on y[0:4] (sim_es7_contact.py:9). This is labelled (PREDICTIONS.md:277).
- **The D66 gain of 0.81 is noise.** Its CI is 0.62–1.01, which RESULTS does not report.

**ES8 (PREDICTIONS.md:281-317).**
- **The code matches.**
- **Not labelled: the agent is *given* the true μ_type and Σ_type** (sim_es8_attention.py:5, :15-19). Nothing is learned, so ES8 is attention without a learned space.
- **The magnitude arm is crippled by the world's design.** It never observes type-3 cues (labelled, RESULTS.md:262). The fair comparator is random.
- **Probe: need-against-random survives.**
  - With equal salience (σ = 0.30 for every type), need costs 0.064× random (CI 0.057–0.072), and magnitude is then the same as random.
  - With drift 0.09, need costs 0.105× random.
- **The figure "92% of log value" is inflated** by a degenerate "none" arm, which runs away at a geometric-mean cost of about 2000. In absolute terms, need costs **2.6× full** (0.059 against 0.023).

**ES9 (PREDICTIONS.md:319-345).**
- **The code matches.**
- **The scalar arm is degenerate, and this is labelled** (RESULTS.md:285).
- **Winner-take-all is the fair primary ablation the earlier review asked for.** Its threshold of ≤ 0.80 was set knowing the ES1 probe's 0.37 in the one-sided world. That is acceptable.

**ES10 (PREDICTIONS.md:347-383).**
- **The code matches,** including the Kalman update (sim_es10_time.py:33-35), which is a correct scalar-observation update with H = [1, 1].
- **Disclosed:** the body receives the true effect (RESULTS.md:312).
- **Not labelled: the two-scale filter is given the world's generative parameters**: q = 0.01², a 40-step constant and SD 0.5 (sim_es10_time.py:5).
- **Fairness problems (probe /tmp/esv2/probe/p_es10_fair.py, 40 seeds):**

  | Control | Two-scale / control (95% CI) | Pre-registered value |
  |---|---|---|
  | Slow EMA started at 0 (as run) | 0.45 (0.35–0.58) | |
  | Slow EMA, bias-corrected (α_n = max(1/n, 0.05)) | **0.645 (0.51–0.82)** | 0.45 |
  | Fast EMA, bias-corrected | 0.70 (0.51–0.97) | |
  | One-scale Kalman, elapsed-time propagation, q = 0.03² | **0.82 (0.60–1.13), 26/40** | |
  | One-scale Kalman, q ∈ {0.01², 0.05², 0.1²} | 0.54–0.68 | |

  - The slow EMA starts at 0 with α = 0.05 and no bias correction (sim_es10_time.py:36).
  - A tuned one-scale filter with elapsed-time propagation is therefore **not** beaten at the pre-registered standard (≤ 0.90, CI upper bound < 1).
  - ES10 shows that Bayesian tracking propagated by elapsed time beats fixed-gain EMAs. It does not show that *two* time scales are needed.
  - Caveat: the q grid was chosen post hoc on the same seeds.

**Dates.** PREDICTIONS.md:283, :321 and :349 say ES8–ES10 were "written 2026-11-26", and STATUS.md:28 says "launched 2026-11-26". The files' modification times, and today's date, are 2026-11-25. Order can only be partly checked: PREDICTIONS.md (11:19:52) predates out/es10.json (11:20:14). The dates are wrong in a pre-registration record.

## Labels and verdicts against thresholds (ES5–ES10)

| Test | Value | RESULTS says | Correct |
|---|---|---|---|
| ES5a-1…4, ES5b-1, 2 | as reported | non-test | non-test (agree) |
| ES6 | no scale chosen | non-test, stood down | agree |
| ES7-1 | ρ −0.045 (−0.118 to 0.029) | confirmed | confirmed, by construction |
| ES7-2 | 0.159 | refuted | refuted |
| ES7-3 | 0.81 and 1.56 | confirmed | confirmed |
| ES8-1…4 | 0.0035; 0.063; 0.92; 0.77 / 0.05 | confirmed | confirmed. ES8-1 is mostly by construction; ES8-3 is inflated by the "none" arm. |
| ES9-1, 3, 4 | 0.12 (0.09–0.18); 0.016; 0.77 | confirmed | confirmed |
| ES9-2 | 0.00016 | confirmed, degenerate | degenerate, labelled |
| ES10-1 | 0.65 (0.44–0.97) | confirmed | confirmed as worded, marginal (30/40) |
| ES10-2 | 0.45 | confirmed | confirmed as worded; 0.645 against a fair control |
| ES10-3 | 0.42 | confirmed | confirmed |
| ES10-4 | 0.99 against ≤ 0.5 | refuted | refuted. The premise was wrong, and this is disclosed. |

## Previous items addressed?

**1. Fix the labels: partly.**
- *ES1-3.* Refuted in RESULTS.md:140. But RESULTS.md:15 still opens with "ES1-3 confirmed", and the summary table at RESULTS.md:130-131 is unchanged.
- *Participation ratio.* Withdrawn in RESULTS.md:141-144. But it is still cited as evidence in four places:
  - RESULTS.md:9 (1.48), :19 ("ES1-5 confirmed"), :28 and :132;
  - costate.md:298 and robust-regulator.md:198 (1.48);
  - costate.md:306 and :321;
  - robust-regulator.md:204 and :219 ("items 3 and 4 shown").
- *By-construction labels.* Added in RESULTS.md:145-147. But "episodes cut cost to 0.06×" is still unlabelled at RESULTS.md:49, costate.md:313 and robust-regulator.md:210.
- *The seek rate.* Corrected at RESULTS.md:148; :46 is unchanged.
- *ES2b-1's 11/20.* Added at RESULTS.md:150. But costate.md:315, robust-regulator.md:213 and STATUS.md:19 still lead with 0.81× and no caveat, and costate.md:326 still adopts w on exploratory evidence.
- *Status blocks: not reconciled.*
  - costate.md:10-11 (items 2 and 3 partly met) against costate.md:351 ("all four … shown"). The header also still says "Time is not shown" (:10), while :346 cites ES10.
  - robust-regulator.md:20 (items 1 and 4 not met) and :9 (field owed) against :251 (all four shown).
  - STATUS.md:36 ("one item met (CS3), two partly met…") against costate.md:7-12 and STATUS.md:22.
- *"Myopic".* Added at costate.md:14, but still missing at costate.md:288.
- *Generators.* Done, and both reproduce.

**2. Robust regulator §2.2: written, but wrong or inconsistent in four places.**
- **The sign.** §2.1 defines e = b − b* (robust-regulator.md:54). An option moves e to e + Δb_i, so the decrease is d(e) − d(e + Δb_i) ≈ −∇d·Δb_i. The text says argmax ∇d·Δb̂_i and d(e) − d(e − Δb_i) (:75-76). That selects the option that *raises* d. The test bed's "e" is the deficit b* − b, which is why the code works.
- **First-order against exact.** ES9 uses the exact decrease d(b) − d(b + Δb̂) (sim_es9_twosided.py:14). Probe /tmp/esv2/probe/p_es9_firstorder.py ran the first-order rule with the sign fixed:
  - it costs **1.84× the exact rule (CI 1.74–1.96, 0/40 seeds better)** and overshoots 3× more;
  - it still beats winner-take-all (0.23×).

  §2.2 should state the exact one-step Lyapunov decrease, which needs no linearization.
- **The K2 amendment (:78-81) conflicts with the rest of the file:**
  - the adaptive law (:72) leaks ĉ_p, not r_p, toward 0, so it would erase Ĉ(x_p). The amendment has no learning law for Ĉ;
  - ĉ_p in the action law and in K1 (:70, :73) is a disturbance gain on the face reconstruction ŷ_p. Ĉ(x_p) is a need-effect vector of a discrete action. The two are conflated, and |ĉ_p| in K1 is undefined for a vector;
  - with a shared Ĉ, a stranger who resembles a relevant person is mimicked. That contradicts "pruned for people who do not move the body" (:104, :160) unless r_p cancels the resemblance, which the file does not state;
  - these lines are not updated: §4 (:127, :135, "one ĉ_p per person"), §7b:178 ("one adaptive scalar per person") and :181 ("a few scalars per person … main strength").
- **Selection ignores the integral mood m** and the feedforward terms of the continuous law it claims to be the analogue of (:70).
- **Episodes:** stated at :82. Acceptable.

**3. Needs as a field over a learned space: not addressed.** ES5 and ES6 were non-tests, and the line is stood down (RESULTS.md:221, STATUS.md:24).

**4. Non-myopic Costate: not addressed.** ES5b's 120 seeds ran in an infeasible world (RESULTS.md:190).

**5. Attention over perceived cues: done (ES8), with caveats.**
- The statistics are given, not learned.
- The magnitude control was broken by the world's design.
- Need against random is robust (probe above).

**6. Time: partly done (ES10).**
- The cost result holds, but the claim of two time scales is not isolated (see Spec against code).
- The behavioral prediction was refuted.
- The structure is per-person tables, not a learned space.
- Neither the Robust regulator's m nor Costate's slow μ is exercised.

**7. Two-sided drive and fair ablation: done (ES9).** For the Robust regulator, see item 2: ES9 tested the exact rule, not the one §2.2 states.

**8. Principle 6 toy: done (ES7), but too narrow.** See Principles.

## Items 1–4 per candidate

| Item | Costate | Robust regulator |
|---|---|---|
| **1. Content-dependent selection over cues, memories and actions** | **Mostly met, myopic limit only.**<br>People: ES1, ES9. Person × topic actions: ES4. Remembered people: ES2-3, which ranks per-person means, not episodes. Cues: ES8, whose rule is w ∝ \|∂V/∂o\|σ at costate.md:218 and :125, labelled a heuristic.<br>ES8 uses statistics that are given, not learned. | **Partly met.**<br>People and options: derivable once §2.2 is fixed (sign and exact decrease).<br>Cue attention (ES8) is **not** in the formal statement. CT7 (sims/control/PREDICTIONS.md:108) is ĉ_p × variance, need-blind, which is closer to ES8's *magnitude* arm. "CT7 projected on e" (robust-regulator.md:6) is an add-on. |
| **2. Needs structured over people, relationships, episodes, topics and time, over a learned space** | **Partly met.**<br>Items (people, topics, relations) are in a learned space.<br>The **needs** are a global vector in every toy that worked. The field μ_k(e) (costate.md:99-110) is not instantiated over a learned space (ES5/ES6 failed).<br>Episodes are per-person means.<br>Time: ES10's two-scale filter fits the multi-timescale x (costate.md:54), but one time scale does about as well, and its slow μ and mood are not exercised. | **Partly met.**<br>Relations: the relation map is fitted but not used in this candidate's selection (no anticipation term).<br>Needs as a field b(e) (:53): not instantiated.<br>Time: ES10's filter is not ξ_p, which is an observer of p's *signals*, and it is not ĉ_p's single-leak law. The claim at :8 is an add-on. m is never exercised. |
| **3. Effective dimensionality, and an ablation** | **Partly met.** The ablation now holds against the fair low-dimensional version: ES9 0.12×, ES1 winner-take-all 0.37×. The dimensionality of the costate field is **still unmeasured** (costate.md:144); the ES1 participation ratio is withdrawn. | **Partly met.** CT4 and ES9, with ES9 subject to the §2.2 fix. The dimensionality is stated (:134), not measured. |
| **4. Richness from structure, not parameters** | **Met in toys** (ES1-4, ES4-3, labelled as worlds that match the model class). ES4-2 adds parameters. ES10's filter is given the world's parameters. | **Partly met.** It depends on the shared Ĉ, whose amendment is internally inconsistent (item 2 above). §7b's data claim is per-person scalars. |

**Cross-cutting.**
- ES1–ES10 all use the myopic rule, so **no expressive-structure result discriminates the candidates.**
- For Costate, that rule is the rival baseline costate.md:137 names: homeostatic RL with no anticipation.

**Still add-ons:**
- ε-greedy exploration and its deficit gate;
- the 0.01 rest threshold;
- the reliability weight w and the max(0, ·) companion form (Costate);
- need-projected attention and two-scale effect tracking (Robust regulator).

## Principles

- **Principle 2 (no named emotion variables): no problem.** Needs are generic.
- **Principle 6 (satiable drives): satisfied in the new toys.** ES9 and ES10 use a two-sided drive, and ES7 and ES8 cap b.
- **Principle 6 (no reward for smiles, attention or time): not closed by D66.**
  - DECISIONS.md:134 counts "an exchange of turns" and "a partner's face perceived within range" as contact events. Both depend on the user: a turn needs the user to reply, and face-in-range events accumulate with dwell time.
  - ES7 has the exchange happen whenever the agent chooses (sim_es7_contact.py:20), so it cannot see this channel.
  - **Probe** (/tmp/esv2/probe/p_es7_reply.py, 40 seeds, otherwise ES7):

    | Variant | ρ (95% CI) | Gain (95% CI) |
    |---|---|---|
    | The exchange counts only if the partner replies, with probability g_k | 0.24 (0.19–0.29) | **1.72 (1.62–1.82)** |
    | Contact grows with the number of turns the partner sustains | 0.14 (0.08–0.21) | 1.29 (1.08–1.50) |
    | The forbidden engagement-weighted reference | | 1.56 |

  - In the first variant, the learned topic map learns contact ∝ P(reply), which is the forbidden gradient.
  - **Costate's own K5 already does this.** Its rollout predicts "interaction events and reply effects" (costate.md:97), so the value of a topic includes the user's reply rate.
  - **Possible fixes:**
    - count only the agent's own outgoing bids, whether or not the user replies;
    - or index the contact effect by person only, with no topic or "what" regressor (D66 point 2 currently includes the "what", DECISIONS.md:135);
    - then re-run ES7 with replies that depend on the partner.
  - D66 point 2, do-conditioning the agent's own expression, has no toy.
- **Principle 10 (one formal core).** The add-ons listed in Items 1–4, and the Robust regulator's §2.2 and K2 amendment, which are not yet consistent with its §2.1–2.2 laws.

## Missing, in priority order

1. **Principle 6.** Redefine D66's contact event so it does not depend on the user's reply or dwell: the agent's own bids, or a person-only contact key. Re-run ES7 with partner-dependent replies, and pre-register the gain against 1.05.
2. **Apply the labels in place.**
   - RESULTS.md:15, :19, :28, :46, :49, :130-133.
   - costate.md:298, :306, :313, :315, :321, :326, :351, and its header line 10 on time.
   - robust-regulator.md:20, :198, :204, :210, :213, :219, :251.
   - STATUS.md:19, :36.
   - Correct the "2026-11-26" dates. Add the ES10 runaways and the ES7 gain CI.
3. **Robust regulator §2.2.**
   - Fix the sign and state the exact one-step decrease, which is what ES9 tested.
   - Give Ĉ a learning law and r_p the leak.
   - Reconcile ĉ_p's two meanings, and |ĉ_p| in K1.
   - Update §4 and §7b.
   - Either derive need-projected attention and effect tracking over time from the formal statement, or mark items 1 (cues) and 2 (time) as add-ons.
4. **Needs as a field over a learned space** (both candidates).
   - Use a world whose feasibility is proven up front, for example by the fluid linear program above, not by a myopic oracle.
   - Gate exploration on deficit, and give overfill a sink.
5. **Non-myopic Costate.** Rollout μ against myopic, in that feasible world, with a powered paired test. Until then, no expressive-structure result distinguishes Costate from homeostatic RL.
6. **ES10 redo.**
   - Pre-register controls: a one-scale Kalman filter with elapsed-time propagation, and bias-corrected EMAs.
   - Give every estimator either the world's parameters or none.
   - Pre-register a time signature that holds under a two-sided drive.
   - Exercise mood (the Robust regulator's m, Costate's slow μ).
7. **ES8 with learned type statistics,** and need against random as the primary comparison.
8. **Measure effective dimensionality** of each candidate's own state (the costate field; Σ dim ξ_p + b + m), against a threshold fixed in advance.
