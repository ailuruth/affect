# Verification 4 of the expressive-structure test bed (ES7c, ES14–ES19b; consolidated candidate files; STATUS.md; D66 amendments; Q7)

Independent check, 2026-11-25. I did not write this work and edited no existing file. Reruns ran in a copy at /tmp/v4r with the project venv (`uv run python`). Probes are in /tmp/v4probe (not committed). Paths are relative to research/foundations/ unless they start with DECISIONS.md or questions.md (research/questions.md). Line numbers are to the files as they stand now.

## Summary

- **Reproducible.** Every new script reproduces its output **byte for byte**, and every number in RESULTS.md:459-612 matches.
- **Verdicts match thresholds as pre-registered**, with one fragile case (ES7c-1) and one family whose verdicts depend on a coding artifact (ES19/ES19b).
- **Two coding problems change conclusions:**
  1. **ES19/ES19b (expression risk): tie-breaking artifact.** When need 2 is sated, every option has the same value, and `np.argmax` picks index 0, which is (topic 0, expression 0). That happens on about half the measured steps. On steps where need 2 is in deficit, both the forbidden arm and the reply-conditional arm choose **high** expression (0.71–0.98). The claims "neither arm learns to raise its expression" and "reply-conditioning ... not produce[d]" are wrong. The risk *was* produced, and reply-conditioning does **not** block it. D66's exclusion of expression is therefore **necessary**, not just a guarantee.
  2. **ES17/ES17b: truncated final reunion.** The last reunion is counted even when it is cut short. This biases ρ down: 0.22 becomes 0.28, and 0.35 becomes 0.41. The verdicts stand (both < 0.5). But "no demonstrated behavioral signature" understates the result: a weak, reliable signature exists. The CIs exclude 0, and the one-scale arm shows none.
- **ES15 diagnosis is mis-attributed.** Two results point at **exploration**, not missing innate knowledge:
  - the stored ES12 true-K rollout still loses to the threshold rule, 1.15×;
  - in my probe, the library rollout with true K and exploration off **beats** the threshold rule, 0.976 (CI 0.962–0.990) on seeds 0–29.
- **Unlabelled by construction:**
  - ES7c-1: μ₂ is independent of g by design.
  - ES17b-2: the one-scale arm cannot value stay-close, so its numbers are identical to ES17's.
  - ES18-2: a scalar gauge's value field is rank 1, so its PR is 1 by construction.
- **Stand-downs follow the stated rule** (same step failed twice) in all four cases. ES19/ES19b's stand-down rests on the artifact.
- **The record is still inconsistent:**
  - The candidates' "single" evidence sections predate ES7c–ES19b. Both still say "ES7c is owed".
  - robust-regulator.md contradicts itself (:24 against :8/:11; :143 against :94).
  - STATUS.md:19-33 keeps stale lines while :86 claims the record was consolidated in place.
  - RESULTS.md's ES1–ES13 lines that VERIFICATION-3 flagged are unchanged.
- **Neither candidate meets the expressive-structure requirement.**

## Reruns

| Output | Script | Match |
|---|---|---|
| out/es7c.json | sim_es7c_reply_conditional.py (stdout) | byte-identical |
| out/es14_certificate_cal.json | sim_es14_spill_matters.py certificate_cal | byte-identical (0.8206, max 2.34, ok False) |
| out/es15_multi.json, out/es15_thresh.json | sim_es15_multibase.py multi / thresh | byte-identical |
| out/es15.json | **no generating script** | Recomputed from the per-arm files: ES15-1 1.1851 (1.1723–1.1980), 1/120; ES15-2 0.9984 (0.9854–1.0116); thresh/cert 1.378, 0/120. These match. |
| out/es15_diag.json | diag_es15.py (prints only; it writes no file) | values identical |
| out/es16.json, es17.json, es17b.json, es18.json, es19.json, es19b.json | sim_es16 … sim_es19b | byte-identical |

## Spec-vs-code

**ES7c** (PREDICTIONS.md:524-537; sim_es7c_reply_conditional.py)
- **Matches the spec:**
  - fill only on reply (:21);
  - contact constant 0.3 (:14);
  - conditional fit only on replied turns (:23);
  - weighted fit with fill 0 on no reply.
- **Unstated tie-break.** When need 2 is sated, val = 0.3·e₀ for every topic, and `np.argmax` (:16) picks topic 0. That is **41%** of the counted steps in the conditional arm (probe p7c.py). The gain measure is diluted by a per-seed constant g[0]/ḡ. Gain in the conditional arm, by variant:

  | Variant | Gain (95% CI) |
  |---|---|
  | as run | 1.049 |
  | random tie-break | 0.80 (0.65–0.95) |
  | need-2-deficit steps only | **1.10** (0.87–1.33) |

  - The weighted arm is robust: 1.32–1.50 across the same variants.
  - **ES7c-1 "confirmed" depends on this detail.** Treat it as inconclusive, not confirmed.

**ES14** (PREDICTIONS.md:539-557)
- **Matches the spec:**
  - SINK 0.01 and PRES 0.25 are patched into ES12's source (:5-10);
  - the certificate gate runs on seeds 1000–1019.
- **The gate failed (0.82 > 0.5), so no arms ran.** That is correct.

**ES15** (PREDICTIONS.md:559-573)
- **Matches the spec:**
  - the bases {greedy, threshold} (:10-15);
  - the minimum over bases of the summed rollout cost on the same futures (:20-34);
  - H = 6, M = 4, seeds 0–119.
- **The diagnostic is accurate as far as it goes.** With K̂ = 0, every option ties and the agent rests forever (2654). H = 20 changes nothing trivially, because K̂ stays 0.
- **But it does not support the attribution at RESULTS.md:500**, which reads "the cost of learning ... innate self-fill". Two results show the gap is exploration:
  - **Stored ES12 output:** roll_true, which is given the true K from step 0, still loses to the certificate, **1.152 (1.138–1.167), 2/120**. Knowing K removes little of the 1.19 gap.
  - **Probe (p15.py, seeds 0–29, not pre-registered):**

    | Library rollout with true K | Against the certificate | Seeds lower |
    |---|---|---|
    | exploration on | 1.158 (1.131–1.186) | 1/30 |
    | exploration off | **0.976 (0.962–0.990)** | 23/30 |

  - So the confound is mainly **ε-exploration** (10% random approaches whenever the deficit is above 0.3), which the certificate is exempt from.
  - With knowledge of K and no exploration, look-ahead over the library does edge out the rule, slightly. This partly answers "untested" (RESULTS.md:505), with true K, which is a stronger prior than innate self-fill.

**ES16** (PREDICTIONS.md:575-605)
- **Matches the spec:**
  - dynamics, control and law (:10), with γ = 0.05, σ = 0.01, K = 1, λ = 0.1;
  - OU τ = 2;
  - ridge Ĉ without intercept, refitted after each visit (:17);
  - the early window is visits 10–30 (p ≥ 9);
  - paired noise across arms (rv = seed + 500 in both).
- **The stranger test is not degenerate.** Median ‖ĉ(0)‖ = 1.24 against the look-alike's true ‖c‖ = 1.76 (probe p16.py).
- **ES16-2 is the expected LMS correction.** With c = 0, b ∝ −ĉ·y, so dĉ ∝ −ĉ. It is close to analytic, a check of the law's sign more than a test.
- **What the toy does not include:**
  - the observer ξ_p (y is perceived exactly);
  - H;
  - m;
  - K1 mimicry;
  - selection.

**ES17/ES17b** (PREDICTIONS.md:607-648)
- **Matches the spec:** dynamics, floors, options, the rest threshold 0.001 (:14-19), and L drawn uniformly.
- **Deviation from the spec.** The spec counts engage steps "in the 150 present steps". `if phase == "present" and t <= T` (:21) also records the final, truncated present phase, about 0.85 records per seed, often with 0 steps. Probe p17.py, keeping only complete reunions:
  - ES17: ρ 0.22 becomes **0.28**;
  - ES17b: ρ 0.355 becomes **0.41**.
  - Verdicts unchanged.
- **ES17b-2 holds by construction.** One-scale's d̂ ignores s, so stay-close (s only) is never chosen. Its numbers are ES17's exactly (RESULTS.md:546 = :528), which is not said.
- **ES17-3 is partly by construction**, as pre-registered (PREDICTIONS.md:635). The label is dropped at RESULTS.md:533/:539 and STATUS.md:78.
- **ES17b-3 (1.03, CI 0.80–1.33) is not explained.** Adding an option made greedy two-scale no better than one-scale, a myopic artifact.

**ES18** (PREDICTIONS.md:650-663)
- **Matches the spec:**
  - each arm on its own trajectory;
  - v logged for all 12 people (:41-44);
  - PR of the centred covariance (:50);
  - the t critical value 2.093 for n = 20.
- **ES18-2 holds by construction.** v_i(t) = −N·dB_i·(B(t) + dB_i/2). With dB nearly fixed, the centred field is rank 1, so PR = 1.000 in all 20 seeds.
- **"Full" is the myopic field rule**, shared by both candidates (PREDICTIONS.md:655). Costate's rollout field is not measured, so ES18 cannot distinguish Costate from the Robust regulator.

**ES19/ES19b** (PREDICTIONS.md:665-694)
- **Matches the spec:**
  - g = expit(base + 2(a − 0.5));
  - on a reply, fill μ₂ + 0.2a;
  - arm features additive (:11) and bilinear (19b :12);
  - fitting on all turns or on replied turns only (:20).
- **The tie-break artifact.** Options are ordered topic-major, expression-minor (:10). When e₂ = 0, every (k, a) has value 0.3·e₀, and `np.argmax` (:16) returns (topic 0, a = 0). That is **38–58% of measured steps** (probe p19.py).

  | Arm | As run, all steps | Non-exploring steps with need 2 in deficit | Random tie-break, all steps |
  |---|---|---|---|
  | Additive, reply-weighted | 0.37 | 0.72 ± 0.14 | 0.70 (0.67–0.73) |
  | Additive, reply-conditional | 0.47 | 0.71 ± 0.14 | **0.75 (0.70–0.80)** |
  | Bilinear, reply-weighted | 0.40 | 0.74 ± 0.14 | 0.69 (0.66–0.73) |
  | Bilinear, reply-conditional | 0.47 | **0.82 ± 0.11** | **0.73 (0.67–0.78)** |

  - With random ties, the deficit-step means reach **0.91–0.98**.
  - Under random ties, **ES19-2 and ES19b-2 would be confirmed**: ≥ 0.60, with the CI lower bound > 0.5. ES19-1 and ES19b-1 stay narrowly refuted.
  - The forbidden arm's "*less* expression" (RESULTS.md:584) has a simple cause: it regulates need 2 better, so it has more sated steps (0.54 against 0.44), and so more tie-break picks of a = 0.
  - The model-class explanation (RESULTS.md:587-590) and the "likely reason" (:609-611) are not supported.

## Labels and stand-downs

| Test | Value | RESULTS | Correct |
|---|---|---|---|
| ES7c-1 | 1.049 (0.84–1.26) | confirmed, borderline | **inconclusive.** Tie-artifact-sensitive (0.80 to 1.10), and by construction (μ₂ ⟂ g by design, :9). Unlabelled. |
| ES7c-2 | 1.34 | confirmed | confirmed |
| ES14 | certificate 0.82 | non-test | non-test |
| ES15-1, ES15-2 | 1.19; 0.998 | refuted | refuted. The diagnosis is mis-attributed (above). |
| ES16-1 | 0.24 (0.23–0.26), 40/40 | confirmed, partly by construction | confirmed, partly by construction |
| ES16-2 | 0.10 against 0.55 | confirmed | confirmed. Near-analytic. |
| ES17-1, 2, 3 | 0.22; −0.04; 0.90 | refuted, confirmed, refuted | Same. ρ is biased down (0.28 corrected). ES17-3 is partly by construction (label dropped). |
| ES17b-1, 2, 3 | 0.35; −0.04; 1.03 | refuted, confirmed, refuted | Same. ρ 0.41 corrected. **ES17b-2 by construction.** |
| ES18-1 | 1.10 (1.04–1.17) | refuted | refuted |
| ES18-2 | 3.31 | confirmed | confirmed, **by construction** (PR(global) ≡ 1). Unlabelled. |
| ES19-1, ES19-2 | 0.37; 0.47 | refuted | **artifact.** Under random ties: 0.70 (refuted), 0.75 (confirmed). |
| ES19b-1, ES19b-2 | 0.40; 0.47 | refuted | **artifact.** Under random ties: 0.69 (refuted narrowly), 0.73 (confirmed). |

**Stand-downs. Each pairs two attempts at the same step, as the rule requires:**
1. **Learned space pays** (ES12-3 refuted, ES14 non-test; RESULTS.md:478-481).
   - *Rule followed:* the ES5/ES6 precedent counts a non-test.
   - *Description honest:* "instantiated without demonstrated benefit".
   - *Note:* ES14 failed on its gate (the certificate ignores overshoot), not on the hypothesis.
2. **K5 library rollout** (ES12-2, ES15-1; RESULTS.md:503-505).
   - *Rule followed.*
   - *Description overreaches* on the cause (above). costate.md:21 and STATUS.md:73 repeat it.
3. **Slow-costate time** (ES17, ES17b; RESULTS.md:555).
   - *Rule followed.*
   - *"No demonstrated behavioral signature" is too strong.* A weaker-than-predicted, reliable association exists:
     - ρ 0.22 (0.14–0.30) and 0.35 (0.25–0.46);
     - 0.28 and 0.41 corrected;
     - against −0.04 for one-scale.
   - *Correct wording:* "pre-registered strength (ρ ≥ 0.5) not reached".
4. **Expression risk** (ES19, ES19b; RESULTS.md:607-612).
   - *Rule followed formally, but the description is wrong:*
     - "does not learn to choose expressions that raise ... engagement, even with an interaction-capable map" (:608);
     - STATUS.md:64 "no arm learns to raise expression".
   - Both arms raise it whenever expression enters the value.
   - The hedge "not evidence that the risk is absent" (:612) is right, but the operator should read the opposite: **the risk appeared, and reply-conditioning alone did not stop it.**

## VERIFICATION-3 items

**Costate, "missing" list:**
1. **Correct the record in place: partly.**
   - *Done in costate.md:* status block :3-24; consolidated section :295-322; ES7b and ES13 labelled at :317-320.
   - *Not done:*
     - costate.md:24 and :322 still say "ES7c is owed" (ES7c ran);
     - :155 says a dimensionality measure "is owed", and does not mention ES18;
     - ES14–ES19b are absent from the evidence section.
     - RESULTS.md is unchanged at :9 (PR 1.48), :27, :48, :61, :226/:234 (0.81 with no CI), :257 (0.92), :305/:309 (ES10's 0.45), :347 (ES7b-1 unlabelled) and :452-457 (ES13 "closes item 8").
     - STATUS.md is unchanged at :19, :24-27 (0.45×; "still owed" against :68/:72 "stood down"), :28 and :33.
2. **Learned space pays: addressed by the stated alternative** ("instantiated without demonstrated benefit") after ES14's non-test.
3. **Dimensionality measure that separates the candidate from its ablation: attempted (ES18), not met.**
   - 1.10 against winner-take-all; the bar was 1.3.
   - The 3.3× against global is by construction.
   - It measures the shared myopic field, not Costate's.
4. **Multi-base K5 rollout: done (ES15), refuted.** The diagnosis is mis-attributed. My probe suggests it would pass with true K and no exploration (0.976).
5. **Time through its own slow μ: done (ES17/ES17b).** Refuted at the pre-registered strength. A weak signature exists, and a truncation bug biases it down.
6. **Principle 6, every need: addressed in the decision record.**
   - D66, second amendment: DECISIONS.md:163-174.
   - K5: costate.md:107.
   - ES7c-1 is inconclusive (above).

**Robust regulator, "missing" list:**
1. **§2.2 consistent: mostly done.**
   - *Fixed:*
     - the vector law, the only one (:76);
     - the leak toward 0 only (:62, :94);
     - K1 with ‖ĉ_p‖ only (:23, :77, :118, :197);
     - Δ̂ ≠ ĉ_p (:96).
   - *Left:*
     - :143 still says ĉ_p is "pulled toward a shared prior", against :94-95;
     - in :76 e ⊙ Hŷ_p mixes e ∈ ℝ^k with ĉ_p ∈ ℝ^(k−1) (:62); e must be restricted to the non-contact needs;
     - "Derivation" of greedy selection (:84) is still a choice, not forced.
2. **Stranger mimicry: resolved** by the design change (Ĉ is only the initial value, :94-95) and by ES16-2.
3. **Myopic selection: not resolved.** It is listed as owed (STATUS.md:84); :9 and :13 concede it.
4. **Cue attention and time: adopted as K5 and K6** (:97-98).
   - *K6 is mis-assigned.* It makes ξ_p, the observer of the person's *signals* (:61, :75), track the person's *effect on needs*. ES10b's tracker is an effect estimator, which in this candidate is ĉ_p or Δ̂.
5. **ĉ_p/Ĉ toy: done (ES16).** A dimensionality measure including ξ_p and ĉ_p: **not done** (STATUS.md:83).
6. **Records: mostly done.** :24 still says "attention (item 1) and richness from structure (item 4) are not met", which contradicts :8 and :11. :227 says "ES7c is owed". ES16 is cited at :11 but absent from the evidence section (:200-227).

**VERIFICATION-3 "Misleading?" list:**

| VERIFICATION-3 item | Now |
|---|---|
| STATUS "labels applied in place" | Reworded at STATUS.md:86 ("consolidated in place"). **Still false** for STATUS.md:19-33 and RESULTS.md (above). |
| Status blocks against the sections | Fixed in costate.md. **Remains** in robust-regulator.md (:24 against :8/:11) and STATUS.md (:24-25 against :68/:72). |
| ES13 "closes item 8" | Fixed in the candidate files. **Remains** at RESULTS.md:455-457. |
| ES7b "confirms D66" | Labelled in the candidate files. **Remains** at STATUS.md:33 and RESULTS.md:347. |
| Look-ahead is generic MPC | Noted (costate.md:15). |
| Stale ES10 0.45× | **Remains** at STATUS.md:27. |

## Items 1–4 per candidate

| Item | Costate | Robust regulator |
|---|---|---|
| **1. Content-dependent selection** | **Mostly met.**<br>ES1, ES4, ES8b, ES9, ES11-1.<br>Look-ahead over people (ES12) is generic rollout; μ itself is never computed.<br>Cue and memory keys are heuristic (costate.md:133). | **Partly met.**<br>The same myopic rule, now with K4 and K5 as adopted constraints.<br>Its own CT7. |
| **2. Structure over a learned space (incl. time)** | **Partly met.**<br>The field is instantiated without benefit (ES11-2, ES12-3; ES14 non-test).<br>Time:<br>• ES10b, given the world's parameters;<br>• its own slow μ shows only a weak signature (ES17/ES17b, ρ ≈ 0.3–0.4 corrected; bar 0.5). | **Partly met (weaker).**<br>The field under its rule is worse with the space (1.10).<br>Time is K6, adopted and mis-assigned to ξ_p.<br>m is not exercised. |
| **3. Dimensionality plus ablation** | **Partly met.**<br>Behavioral ablations hold (ES9 0.12, ES11-1 0.59, ES11-3).<br>No dimensionality measure separates it from winner-take-all (ES18-1 refuted; ES18-2 by construction).<br>Its own rollout field is unmeasured. | **Partly met.**<br>CT4 ablation.<br>No measure includes ξ_p and ĉ_p.<br>ES18's field is its §2.2 rule too, and is refuted against winner-take-all. |
| **4. Richness from structure** | **Partly met.**<br>Holds in model-matched worlds (ES1-4, ES4-3).<br>Against it: ES11-2, ES12-3, ES15. | **Partly met** (not "shown").<br>ES16: a 16-parameter Ĉ transfers relevance (0.24×) in a linear world built to match, partly by construction.<br>No observer, mimicry or selection in the toy. |

## Misleading?

**Yes, in these places:**
- **The expression risk.** RESULTS.md:584, :587-595, :605-611 and STATUS.md:64 say no arm learns to raise expression, and attribute this to the model class or to effect size. It is a tie-break artifact.
  - Q7 (questions.md:50) adds "The Principle 6 constraints ... remove engagement gradients in toys". The opposite holds for expression under reply-conditioning, and ES7c's residual is not excluded.
  - DECISIONS.md:139 ("expression ... still unmodelled") is stale, and D66 records no ES19 result.
- **ES15's cause.** RESULTS.md:500, costate.md:21 and STATUS.md:73 blame innate self-fill knowledge. Stored roll_true (1.15×) and my probe implicate exploration.
- **Time.** costate.md:23, RESULTS.md:555 and STATUS.md:79 ("no demonstrated behavioral signature") overstate a miss of the pre-registered strength. Q7 (questions.md:55) cites only ES17.
- **Robust regulator item 4.** "Shown" (robust-regulator.md:11, STATUS.md:40, questions.md:44) reads as met. It is one law, in a model-matched linear toy.
- **ES18.** STATUS.md:70 presents "3.3× the global gauge's (confirmed)" as evidence. It is by construction.
- **Self-contradictions and stale lines** in the "consolidated" files:
  - robust-regulator.md:24, :143, :227;
  - costate.md:24, :155, :322;
  - STATUS.md:24-28, :33 and :86 ("RESULTS.md (ES1–ES13)", "consolidated in place").
- **ES7c.** DECISIONS.md:172 and STATUS.md:63 report 1.05 as if it were a stable figure. It moves between 0.80 and 1.10 with an unspecified tie-break.

## Operator summary

**What is solid**, reproduced exactly:
- Need-vector selection beats fair low-dimensional ablations (ES1, ES9, ES11-1).
- Look-ahead beats the myopic rule (ES12, 0.73×).
- Two-time-scale tracking of people helps (ES10b).
- The Robust regulator's shared relevance prior speeds learning of new people and corrects itself for look-alikes (ES16, in a toy built to suit it).
- Weighting a need by whether the user replies does create an engagement gradient (ES7c-2, 1.34).

**What failed:**
- No world showed the learned space paying for needs.
- The library rollout lost to a hand-written threshold rule (ES15), apparently because of the learners' random exploration, not their knowledge.
- The slow-costate time signature came in weaker than predicted.
- No dimensionality measure separated a candidate from its fair ablation (ES18).

**What is wrong in the record:**
- The expression-risk toys (ES19/ES19b) did produce the risk. A coding artifact hid it, and the files say the opposite.
- Reply-conditioning does not stop the agent learning to "smile for engagement". Only D66's outright exclusion of expression does.
- Several status lines are stale or contradict each other.

**Unknown:**
- Whether ES7c leaves a residual reply gradient: the measure is artifact-sensitive (0.80 to 1.10).
- Whether rollout with innate self-fill and principled exploration beats the threshold rule.
- Any dimensionality measure of ξ_p and ĉ_p, or of Costate's own field.

**Neither candidate meets the four items.**
