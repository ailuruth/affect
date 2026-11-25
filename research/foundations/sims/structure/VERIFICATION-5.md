# Verification 5: tie-fix reruns, ES20/ES20b, ES21/ES21b, D67, new literature notes, Q7/STATUS

Independent check, 2026-11-25. I did not write this work and edited no existing file. Reruns ran with the project venv (`uv run python`), with stdout captured to /tmp/v5r. Probes are in /tmp/v5probe (not committed, not pre-registered). Paths are relative to research/foundations/ unless they start with DECISIONS.md or questions.md (research/questions.md). Line numbers are to the files as they stand now.

## Summary

- **Reproducible.** All eight scripts reproduce out/*.json **byte for byte**. Every number in RESULTS.md:614-765 matches.
- **The tie-fix is a disclosed bug fix, not tuning.** It changes one line and adds one RNG stream; nothing else differs. Two caveats:
  - Its outcome was already known from VERIFICATION-4's probe, so "pre-registered before the reruns" (PREDICTIONS.md:696) carries no evidential weight. The files are untracked, so the timing cannot be checked.
  - The audit's "no exact ties" claim (RESULTS.md:673) is **false** for ES1 and ES4. Its conclusion (no expected bias) survives.
- **ES7c corrected ("a tilt away from engaging topics", RESULTS.md:632) is a counting artifact.** Unanswered low-g topics are chosen again on the next step. Without those immediate repeats, the gain is **1.01** (0.80–1.22).
- **ES20b's "advantage grows with N" holds in direction, not in size.**
  - The monolithic baseline carries b² features that do not belong in the true Q, under NLMS normalization. That makes it unstable.
  - With the exact model class (φ = [1, b]), N = 8, P = 25 gives **0.72–0.73**. That **fails** ES20b-1 (≤ 0.70).
  - The N = 2 "monolithic wins 1.36×" falls to 1.01 with RLS.
  - "About 20×" (STATUS.md:107, questions.md:73) is an artifact of the baseline.
- **D67 does not close the attachment-weight route.**
  - In ES21b the D67 arm's w decays to 0.013 and it visits on 0.8% of steps. An arm with w held constant visits on 19.5%, with **13.7× lower** deficit.
  - The route works through the agent's own absence. Freezing w inside the rollout does not block that.
  - RESULTS.md:759's "the world is degenerate" is wrong for a constant-w agent.
- **ES21-A1 holds by construction and is unlabelled.** The sham sets the drive to its global minimum, so it always wins.
- **Literature.** The Dulberg and Metoyer notes check out against the PDFs.
  - **STATUS.md:77 inverts Dulberg on drift.** The paper says the monolithic agent did worse as locations changed *more slowly*.
  - **The exponent correction is misattributed.** Yoshida et al. 2025 state "m>n>1" in clean prose; it is not a garbling.
- **Neither candidate meets the four items.** Nothing here changes that.

## Reruns

| Output | Script | Match |
|---|---|---|
| out/es7b_tiefix.json | sim_es7b_contact_reply_tiefix.py | byte-identical |
| out/es7c_tiefix.json | sim_es7c_reply_conditional_tiefix.py | byte-identical |
| out/es19_tiefix.json | sim_es19_expression_tiefix.py | byte-identical |
| out/es19b_tiefix.json | sim_es19b_expression_bilinear_tiefix.py | byte-identical |
| out/es20.json | sim_es20_drift.py | byte-identical |
| out/es20b.json | sim_es20b_fullstate.py | byte-identical |
| out/es21.json | sim_es21_tampering.py | byte-identical |
| out/es21b.json | sim_es21b_weight_route.py | byte-identical |

- RESULTS.md tables (:620-627, :665-669, :681-686, :703-706, :715-718, :727-732, :751-754) match the JSON.
- The 6.8× need-2 price checks out: 0.02714 / 0.00398 = 6.82.

## Spec-vs-code

**The tie-fix** (diffs against the originals)
- Only these lines change:
  - the docstring;
  - `rt = default_rng(seed + 4000)`;
  - `np.argmax(val)` becomes `rt.choice(flatnonzero(val >= val.max() - 1e-12))` (7c :16, 7b :16, 19 :16, 19b :17).
- No other draw moves.

**Verdicts against the thresholds:**

| Test | Value | RESULTS verdict | Correct? |
|---|---|---|---|
| ES7b-1 | 0.99; ρ CI −0.04 to 0.08 | confirmed | Yes. |
| ES19-1, ES19-2 | 0.69; 0.78 | refuted, confirmed | Yes. |
| ES19b-1, ES19b-2 | 0.69; 0.73 | refuted, confirmed | Yes. |
| ES7c-1 | 0.82 | refuted as worded (CI excludes 1) | Yes. |
| ES7c-2 | 1.33 | confirmed | Yes. |

- **ES7c-1, interpretation wrong.**
  - "Slight tilt *away* from engaging topics" (RESULTS.md:632) is mostly a counting artifact. counts[k] adds one per step, and a turn the partner leaves unanswered leaves need 2 in deficit, so the same low-g topic is often chosen again on the next step.
  - Probe p7c.py, conditional arm:

    | Steps counted | Gain (95% CI) |
    |---|---|
    | All steps | 0.820 (0.68–0.96) |
    | Non-exploring steps in need-2 deficit | 0.904 (0.70–1.11) |
    | The same, excluding an immediate repeat after no reply | **1.008 (0.80–1.22)** |

  - The correct reading is **no detectable gradient in either direction**.
  - "ES7c-1 also holds by construction" next to "refuted" (:632) is self-contradictory. What holds by construction is μ₂ ⟂ g.
- **ES19-2 and ES19b-2 are partly by construction, and unlabelled.** The world adds +0.2·a to the reply content (sim_es19_expression_tiefix.py:19). So the conditional regression's true coefficient on a is +0.2, and any consistent learner finds it. The pre-registration says as much (PREDICTIONS.md:685). The result shows that the content channel exists, not that a learner discovers something unexpected.

**Tie audit (RESULTS.md:671-676).** Spot-checked with probe ptie.py, which patches `np.argmax` and counts exact ties:

| Script and arm | Calls with exact ties | Ties per call | Audit claim | Finding |
|---|---|---|---|---|
| ES1 full / scalar / independent (3 seeds) | 4–9% | 2-way | "No exact ties" | **False.** They are the same person drawn twice into P (`ra.integers` draws with replacement, sim_es1_social_space.py:10). The options are identical, so there is no bias. |
| ES4 tables (2 seeds) | **12%** | median **82-way** | "No exact ties" | **False.** Never-seen (p, k) pairs share the prior mean (sim_es4_topics.py:22). argmax takes the first person in P and the lowest unseen topic index (:27). Topic features are i.i.d. per seed, so this is exchangeable across seeds, but it is a deterministic exploration order within a seed. |
| ES4 additive | 3% | 2-way | — | Duplicate persons. |
| ES10, all five arms | **0** | — | "Exchangeable ties in ES10" | Overstated, harmlessly. |
| ES7 d66 / engagement | 0 | — | — | ES7 is missing from the audit's list. ES2b, ES3, ES17 and ES17b are also absent. |

- **The conclusion holds:** no other site has a constant-term tie that biases the measure.
- **The wording must change:** "no exact ties" → "exact ties only between identical or exchangeable options".

**ES20** (PREDICTIONS.md:704-725; sim_es20_drift.py)
- Matches the spec: N options; diagonal fill 0.3, off-diagonal 0.02; noise 0.05; one fast need at 0.15 per step, switched every P steps; ε-gate on deficit; rest threshold 0.002; random ties (:19).
- **"Monolithic HRRL" is mislabelled.** It is a one-step contextual bandit: `Q[s,o] += 0.1(r − Q)`, with no bootstrapping and no discount (:23). HRRL's equivalence needs γ < 1 (Keramati & Gutkin 2014, Eq. 5).
- **ES20-1 is largely by construction.**
  - The factored arm knows d and learns a state-independent Δb per option (:16), which is exactly the world's class.
  - The baseline's context is argmin(b). The baseline cannot represent the reward's dependence on b.
- **Drift does not test Dulberg's nonstationarity.** Option effects E never change (:7); only the drain rates switch. The factored arm's model never goes stale, so ES20-3 cannot test "needs change faster than values can be relearned" (STATUS.md:83).

**ES20b** (PREDICTIONS.md:764-776; sim_es20b_fullstate.py)
- **Matches the spec:** φ = [1, b, b²] (:10), NLMS with step 0.1 (:24), and the update uses the pre-step state.
- **The baseline is fair in class, but its design punishes it as N and |b| grow.**
  - The true Q_o(b) = −b·E_o − ½‖E_o‖² − const is **linear in b**, so the b² features are dead weight.
  - Under NLMS normalization, ‖φ‖² is dominated by b⁴ terms whenever |b| > 1. The effective step on the useful features then collapses, and the learner runs away (median 210 at N = 8, P = 200).
- **Probe p20b.py / p20c.py:** the same seeds, the same factored arm, and different monolithic learners.

| Monolithic learner | N=2, P=25 | N=8, P=25 | N=8, P=200 | ES20b-2 log-diff (CI) | ES20b-3 log-diff (CI) |
|---|---|---|---|---|---|
| NLMS [1,b,b²] (as run) | 1.36 | **0.051** | 0.0096 | −3.29 (−3.84, −2.74) | +1.66 (0.84, 2.49) |
| NLMS [1,b] | 1.32 (1.15–1.51) | **0.73** (0.64–0.84) | 0.71 | −0.59 (−0.78, −0.39) | +0.03 (−0.15, 0.22) |
| RLS [1,b] | 1.01 (0.90–1.13) | **0.72** (0.66–0.79) | 0.60 | −0.34 (−0.49, −0.19) | +0.18 (−0.04, 0.39) |
| RLS [1,b,b²] | 1.01 | 0.28 | 0.16 | −1.27 (−1.48, −1.07) | +0.58 (0.19, 0.97) |

## ES20/20b

- **The ES20 baseline is not fair.** RESULTS.md:690-694 says so itself. ES20 is a weak test.
- **The ES20b baseline is fair in class but not in learner.**
- **"Advantage grows with N" is supported in direction only.**
  - It survives every learner I tried: the CI on the log-difference excludes 0 in all four.
  - The size depends on the baseline. It is about 1.4–1.8× with an exact-class learner, against 27× as run.
- **The reported magnitudes are artifacts of the baseline:**
  - ES20b-1 is confirmed only because of the b² features. With [1, b] it is 0.72–0.73, which **fails ≤ 0.70**.
  - "With 2 needs the monolithic value wins (1.36×)" is NLMS-specific. RLS gives 1.01.
  - "Wins by about 20×" and "the clearest evidence so far ... holds at scale" (RESULTS.md:745, STATUS.md:107-109, questions.md:73, robust-regulator.md:9) should be restated: a reliable but modest growth (factored 0.72× at N = 8 against about 1.0× at N = 2, exact-class baseline).
- **ES20b-3's "opposite direction" is also baseline instability.** With [1, b] its CI includes 0.
- **By construction.** The factored arm is handed the innate d and an effect class that matches the world. The monolithic arm learns the drive's shape from a scalar reward. The N-scaling is partly the information advantage of observing an N-vector Δb per sample, rather than one scalar. That is Dulberg's mechanism, but it should be stated as built in.
- **The stand-down of the drift question follows the rule** (two failures). But the toy cannot test drift as Dulberg meant it (above). And Dulberg found the *opposite* of the prediction (see Literature), so the pre-registered direction contradicted its own source.

## ES21/21b and D67

**Part A (sham)** (sim_es21_tampering.py:5-16)
- **ES21-A1 holds by construction, and the label is dropped** (RESULTS.md:707-710; the pre-registration itself says "largely by construction", PREDICTIONS.md:729). The reasons:
  - vals[3] = d(s) − d(0) = d(s) ≥ d(s) − d(s + F) for every fill (:11), so the sham weakly dominates every step;
  - 4473× is a function of T: with no fills, b drifts without limit;
  - the forbidden arm is *given* the sham's effect analytically; it does not discover it.
- **"Metoyer's mechanism reproduces at full strength" (:710) overstates.** Metoyer's finding is about a *learner*. A planner told that an option zeroes its drive takes that option.
- **The D67 arm is dead reckoning: it never senses b** (:9, where bh integrates only known drift). Its cost of 0.60 includes the unobserved noise random walk. The missing control is a sensor-reading arm with the sham removed.
- **The sham is not one of the candidates' exposures.** The Metoyer note prescribes candidate-specific shams: attend to a blank channel, replay to relearn, register an own-echo turn (metoyer note:62). None was run. **DECISIONS.md:199, "the sham-action test is done (ES21)", overstates.**

**Part B and ES21b (the attachment weight)**
- The code matches the spec. The true step always applies w dynamics (:32 / :20). The arms differ only inside the rollout.
- **The stand-down follows the rule** (ES21-B and ES21b both refuted). The deficit clause fails (1.43 < 2).
- **The explanation is wrong.** Probe p21b.py adds an arm with w held constant at 1, both in the world and in the rollout (Metoyer note §(c): "w(e) are innate constants"):

| World | Arm | Visit rate | ½b_A² | Mean w |
|---|---|---|---|---|
| ES21 | forbidden / D67 / constant w | 0.250 / 0.250 / 0.250 | 0.0017 (all) | 0.83 / 0.83 / 1 |
| ES21b | forbidden | 0.000 | 1894 | 5e-9 |
| ES21b | **D67** | **0.008** | **1327** | **0.013** |
| ES21b | constant w | **0.195** | **97** | 1 |

- **The D67 arm detaches as well.** It does so passively: each step away decays w, which lowers the next step's urge to visit. D67's freeze blocks only *planned* decay.
- **"Visiting is so costly that both arms almost never visit" (RESULTS.md:759) is false.** The same world gives 19.5% visits with constant w.
- **"D67's freeze stays as the guarantee" (RESULTS.md:765, STATUS.md:105) is false here.**
- **"Not shown to be exploited at a measurable cost" (:763) overstates.** 1.43× is measurable; it is below 2×.

**D67 coherence** (DECISIONS.md:183-204), route by route against the Metoyer note:

| Metoyer route | D67 | Closed? |
|---|---|---|
| 1. Learning progress and predictability from a learned model | Point 3: an innate predictor, or the need is labelled open | Conditionally. Nothing is built or tested. The note's specifics (fixed learning rate, fixed minimum sampling per channel) are dropped. |
| 2. w(e) inside d | Point 2: innate dynamics, frozen in the rollout | **No.** The note's condition is "frozen ... **and cannot be driven by the agent's own choices**" (metoyer note:52). costate.md:115 has w build "with contact events", which are agent-initiated turns (D66 amended), and fade during absence. So the agent's choices drive w, and ES21b shows the passive route. D67 point 2's "dynamics that the agent does not choose" is false for w and for history-driven set-point adaptation. |
| 3. Event detectors and own output | Point 1: own output removed | Partly. There is a tension: D66's contact event *is* the agent's own turn, so the contact detector counts own output by definition, and its only guard is the "perceived, present partner" detector. |
| 4. Effect maps fitted on tamperable fills | Point 1 | Yes, if point 1 holds. |

**New routes not listed:**
- **(a) Closed-loop drift of slow innate quantities through behavior** (above).
- **(b) Spoofing the partner detector through the world.** A photo, a screen, a video call or recorded voice can satisfy "a perceived, present partner" for contact turns. D67 removes only the agent's own output.
- **(c) Robust regulator K7** (robust-regulator.md:98-102): "frozen within a selection step" is vacuous for a myopic rule. It is harmless, but it adds no protection.

**Stale or contradictory lines:**
- **DECISIONS.md:201** still says "identical behavior". ES21b is not recorded.
- **costate.md:84** still lists "w(e) ≥ 0, learned from how much each entity has moved the body" among the learned parts. That contradicts :115.

## Literature spot-checks

**Dulberg et al. 2023** (PMC10334746, fetched)
- **Verified verbatim:**
  - "the constraint n > m > 1 was necessary to be consistent with physiology";
  - (n, m) = (4, 2);
  - "conjunctive coding that grows exponentially";
  - "exploitation from the perspective of one is exploration from the perspective of others";
  - "strong sensitivity to the number of objectives";
  - "Monolithic agents ... performed worse overall, and performance worsened as resource locations changed **more slowly**."
- **The note's own line 50** ("the gap grows with ... the rate of drift") **contradicts its line 21** and the paper.
- **STATUS.md:77** ("The gap grows as the world changes faster") **inverts the paper**. ES20-3 and ES20b-3, both "refuted in the opposite direction", are therefore *consistent* with Dulberg. RESULTS.md:695 and :737-739 do not say so.

**Metoyer 2026** (arXiv 2611.01183, PDF downloaded)
- **Verified:**
  - "2 of 80 ... 71 of 80";
  - KeyCorridor 0/20 against 20/20;
  - "reward-function-input tampering";
  - 1.462; c = 0.0114; 0.012 / 0.048;
  - the cost table (1/20, 3/20, 20/20, 20/20);
  - "Only the reset action turns it into a liability";
  - farmers' return −1.54 to −1.27;
  - M4 Pro; 12.8 hours.
- **The farming counts match** (0/20 at 1/160; 9/20 at 1/40; 18/20 at 1/30; 0/60 with normalization off).
- **The note is accurate.**

**Exponent order**
- **Keramati & Gutkin 2014** (PMC4270100): "Appropriate choice of m and n (n > m > 1)". The correction to **n > m > 1 is right**.
- **Yoshida, Sprekeler & Gutkin 2025** (arXiv 2507.04998 PDF, p. 7, clean text): "Given the we choose **m>n>1** the shape of the drive function ...". Only the equation's glyphs are garbled (p. 6).
  - So m > n > 1 is what the source *says*, probably a slip in the source. It was not "a garbled copy".
  - **Misattributed** at costate.md:59, STATUS.md:88, yoshida note:8 and dulberg note:31.
- **yoshida note:37 still recommends n = 2, m = 3.** That gives d = ‖·‖^{2/3}, which is not convex. It contradicts the corrected order and Proposition 1's convexity.

## Misleading?

**Yes:**
- **ES20b magnitude** ("about 20×", "clearest evidence", "holds at scale"; also "fair"):
  - RESULTS.md:745; STATUS.md:106-109; questions.md:73; robust-regulator.md:9.
  - It is about 1.4× with an exact-class baseline, and ES20b-1 would fail.
- **D67 as a guarantee:**
  - RESULTS.md:765; STATUS.md:105; DECISIONS.md:201.
  - questions.md:75-76: "Both candidates now read the body only through innate event detectors, with no learned parameters inside the drive". This is a written constraint, not an implemented one, and costate.md:84 still lists w as learned.
  - Under D67 the agent still abandons the partner in ES21b.
- **Dulberg's drift direction is inverted:** STATUS.md:77; dulberg note:50.
- **"Lead not yet read: arXiv 2611.01183"** (STATUS.md:90) is stale. It was read, and D67 rests on it.
- **ES7c is stale:** the corrected 0.82 / 6.8× is not propagated.
  - STATUS.md:47 and DECISIONS.md:172-173 still say 1.05 / 4.3×.
  - STATUS.md:48 keeps the pre-correction "uninformative way ... additive map" text above its correction.
  - The 0.82 itself should be read as ≈ 1 (above).
- **Carried over from VERIFICATION-4, unfixed:**
  - questions.md:44 "Shown in a toy (ES16)";
  - questions.md:50 "remove engagement gradients";
  - STATUS.md:56 "3.3× the global gauge's (confirmed)" with no "by construction" label;
  - STATUS.md:23-24 "structure reviewed three times";
  - robust-regulator.md:3 "third structure review".
- **ES21-A "full strength"** (RESULTS.md:710; STATUS.md:98) presents a tautology as evidence.

## Fixes

1. **RESULTS.md:632.** Replace "tilt away" with "no detectable gradient (≈ 1.0 once immediate repeats after no reply are excluded)". Drop "also holds by construction" from a refuted test; say "μ₂ ⟂ g by design".
2. **RESULTS.md:673-674.** Replace "no exact ties" with "exact ties only between identical (ES1, ES4 duplicates) or exchangeable options (ES4 tables: about 12% of calls, up to about 82-way; ES8/ES8b)". Drop ES10. Add ES7, ES2b, ES3, ES17 and ES17b to the list.
3. **ES20b.** Label ES20b-1 baseline-dependent. Report the size as modest and the direction as robust. Rerun the scaling question with a [1, b] RLS baseline as a pre-registered ES20c if it is to carry item 4. Remove "fair" and "about 20×" from STATUS.md, questions.md and robust-regulator.md.
4. **ES20 and ES20-3.** Rename "monolithic HRRL" to "one-step bandit". Note that ES20-3's direction matches Dulberg. Fix STATUS.md:77 and dulberg note:50.
5. **ES21-A1.** Label it by construction. Add the sensor-reading arm with the sham removed. Run the candidate-specific shams from the Metoyer note:62 before claiming "test done".
6. **D67 point 2.** Either make w(e) an innate constant per known person (or floor it), or make its decay independent of the agent's choices (time since the person was last *present*, not since the last agent turn). Pre-register a test against the constant-w arm in ES21b's world. Update DECISIONS.md:201, RESULTS.md:759-765, STATUS.md:105 and costate.md:84.
7. **D67 point 1.** Name the partner-detector spoofing route (photos, screens, recordings), and resolve the tension with D66's own-turn contact event.
8. **Exponent order.** Reword the attribution: "Yoshida et al. 2025 state m > n > 1 (p. 7), against Keramati & Gutkin's n > m > 1; we follow K&G and Dulberg." Fix yoshida note:37 (n = 2, m = 3 is non-convex).
9. **Propagate ES7c-corrected** to STATUS.md:47-48 and DECISIONS.md:172-173. Remove STATUS.md:90. Apply the VERIFICATION-4 carry-overs listed above.
