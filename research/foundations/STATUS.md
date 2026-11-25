# S0 status

**2026-11-25: S0 redirected by the operator (D68).**
- Costate and the Robust regulator are stood down as core candidates. Their verified results, and the D66/D67 constraints, remain as material.
- The core search restarts: new computational mechanisms in which emotion emerges in a rich learned latent state. The work diverges first, with at least eight isolated sketches.
- Evidence must come from published data and tasks, not self-built toy worlds.
- Everything below this line is the record of the earlier phase.

---

# S0 status (updated 2026-11-25)

**S0 ends when:**
- evaluation.md exists;
- at least three candidates are complete (written to brief.md's standard, with simulations, and independently verified);
- research/foundations/comparison.md compares them.

The operator then chooses the core.

**Done:**
- **evaluation.md:** written from primary sources. Rewritten for the new S1 (the real-time dyad) and S2 claims, with design notes.
- **Eight lens sketches:** sketches/README.md, with the convergences between them recorded.
- **A shared curiosity component:** learning progress as a satiable body variable (sims/curiosity/, D62). It answers a limit found in all three candidates: surprisal minimization falls into the dark room, and a predictability set point falls into the noisy TV.

**Not yet:** no candidate is complete, and comparison.md does not exist.

**What blocks completion (D65, amended):** both viable candidates must show all four expressive-structure items in toys. The current state, per four independent reviews (sims/structure/VERIFICATION.md through -4), is in the table below and in "Owed" at the end. The history of the toys is in sims/structure/RESULTS.md.

## Candidates (consolidated 2026-11-25 after sims/structure/VERIFICATION-3.md)

| Candidate | State | Expressive structure (brief.md's four items) | What distinguishes it |
|---|---|---|---|
| **Costate** (costate.md) | Not complete. Core verified twice; structure reviewed three times. | 1 mostly met (myopic rule only); 2, 3 and 4 partly met. The need field over a learned space is instantiated without demonstrated benefit. | Model-based look-ahead beats the myopic rule (0.73×, ES12), but a no-learning threshold rule beats both. |
| **Robust regulator** (robust-regulator.md) | Not complete. Core verified once; structure reviewed three times. | All four partly met. ES16 shows item 4 only in a world built to suit its prior. Cue attention and time are adopted constraints (K5, K6). | Per-person relevance-scaled mimicry and small-gain interface safety. Its selection rule is myopic, which loses in field worlds. |
| **Thermodynamic mirror flow** | Stood down after three failed verifications | – | Verified results kept for reuse. |
| **Contingency and parity** | Broken on its two distinctive derivations | – | Parity reading and the typed interface survive. |

## What the verifications established, across candidates

- **A model-free value gradient is unreliable at this data scale (Costate T1).** Body dynamics must be innate and the value computed by rollout.
- **A deterministic synchronized copy does not read another's hidden state (thermo TH2).** An ensemble filter running the agent's own model does (R² 0.73), and misreads badly when the model is wrong (−1.82).
- **The published coupling score is a correlation, so it is blind to response amplitude (Costate CS2).** S1-b predictions must name a change in the partner-driven share of expression.
- **A learned world model trained on one person's routine treats off-schedule events as unknown (Costate F).** Every candidate that learns the user inherits this.
- **None of the candidates derives mimicry.** In all three it is an explicit constraint, or (Contingency) its derivation failed.

## Path to the end of S0 (revised)

Two of the three chosen candidates have now broken: Thermodynamic stood down, and Contingency broke on its distinctive claims. S0 needs three complete candidates, so:
1. **Costate.** Close its remaining items. It is the strongest, and the results the stood-down candidates leave (filtering-based reading, the need-valence state-function guarantee, metastable emotion types) can be stated as explicit constraints or adopted mechanisms in it, if each is derived or constrained there.
2. **The control-theory sketch** (sketches/control-theorist.md) is developed as a new candidate. It derives mimicry from the internal model principle, which is the one route to mimicry no candidate has tested yet.
3. **A third complete candidate:** either Contingency repaired (a sign-breaking mimicry term, a bounded-sign flattery test, the provocation veto), or another sketch developed (deep learning's tied dyad, or the game theorist's mirror game). Decided after 1 and 2.
4. comparison.md, which will also report the broken candidates and why, then the operator's choice.

## Owed before either viable candidate can be marked complete (after VERIFICATION-3)

**Principle 6 (both candidates).** D66, second amendment: no need's fill may be weighted by the partner's reply, dwell or expression.
- **ES7c (corrected after the tie fix and VERIFICATION-5):** the reply-conditional gain is about 1.0 once repeat picks after non-replies are excluded (raw 0.82), against 1.33 for reply-weighted. The reply-dependent need is regulated 6.8× worse, which is the price of the principle.
- **The agent's own expression as a cause of engagement (D66 point 2): ES19, first attempt, refuted** in an uninformative way. An additive map cannot represent the topic × expression interaction, and the forbidden arm chose *less* expression. **Corrected after VERIFICATION-4 found a tie-breaking bug.**
  - With the bug fixed, both learning arms raise expression (0.69–0.78), and reply-conditioning alone does **not** block it.
  - **D66's exclusion of expression is load-bearing.** The stand-down is withdrawn.
- Still open: a powered test of the residual gradient (ES7c).

**Costate:**
1. ~~Show that the learned space pays for needs~~. **Stood down after two failures** (ES12-3 refuted; ES14 a non-test, its certificate failing at 0.82). Recorded: the need field over a learned space is **instantiated without demonstrated benefit**.
2. A dimensionality measure that separates the candidate from its own ablation. **ES18, first attempt:**
   - the value-field participation ratio is 3.3× the global gauge's (confirmed);
   - it is only 1.10× winner-take-all's (CI 1.04–1.17; the bar was 1.3, refuted).
3. ~~A K5 rollout over several base policies~~. **Stood down after two failures** (ES12-2, ES15-1: the library rollout is 1.19× the threshold rule).
   - Corrected diagnosis (VERIFICATION-4): the gap comes from exploration. With the true K and no exploration, the library rollout beats the threshold rule (0.976, CI 0.962–0.990; a probe, not pre-registered).
4. Time through its own slow μ or mood, with a behavioral signature. **ES17, first attempt, refuted:**
   - post-reunion engagement did not scale with separation (ρ 0.22);
   - fast-need overshoot capped engagement;
   - the slow costate lowered cost (0.90×, 20/20).
   - **ES17b retry, also refuted** (ρ 0.35, or 0.41 corrected for the truncated final reunion). **Stood down after two failures.** A weak but reliable signature exists; the predicted strength (ρ ≥ 0.5) was not reached.

**Robust regulator:**
1. ~~A toy of its own ĉ_p/Ĉ structure~~. **Done (ES16):** the prior cuts early cost to 0.24×; a wrong stranger prior is corrected to 0.10 in 60 s (the leak alone gives 0.55). Partly by construction.
2. A dimensionality measure including ξ_p and ĉ_p.
3. Either accept that item 2 is not met behaviorally under its myopic rule, or add look-ahead and say how it then differs from Costate.

**Completed toys and reviews:** sims/structure/RESULTS.md (ES1–ES19b and the corrections) and VERIFICATION.md through -4. The status sections were rewritten in place on 2026-11-25. RESULTS.md keeps each original verdict, with corrections appended below it and cross-referenced.

## What the literature says about when structured needs pay (research tick, 2026-11-25)

Seven new primary-source notes are in research/ and indexed. The most relevant:
- **Dulberg et al. 2023** (PNAS): one learner per need, recombined at action time, beats a single scalar homeostatic drive at matched parameter count.
  - The gap grows as the number of needs rises from 4 to 8.
  - *[corrected after VERIFICATION-5]* The monolithic agent did **worse as resources moved more slowly** (local minima); modular agents were largely insensitive to the rate of change.
  - The gap shrinks with plenty of imposed exploration.
- **Millidge et al. 2024:** per-need values re-weighted by the current need vector adapt at once when needs change. A scalar learner must re-experience reward first.
- **Zhang, Berridge et al. 2009:** salience gain is per need. A first salt appetite raised ventral-pallidum firing to the salt cue only.

**What this means for our toys:**
- **Consistent:** our need-vector selection beat the scalar gauge throughout (ES1, ES9, ES11-3).
- **Explained:** our *learned spill space* showed no benefit (ES11-2, ES12-3). Those worlds were static and explored a lot, which is the regime where Dulberg's gain shrinks.
- **What would test it properly:** a drifting world, more needs, and needs that change faster than values can be relearned.
- **Cost of structure, per the same sources:** factored values lose cross-need inhibition and can be suboptimal when needs interact.

**Correction found during the reading:** the drive-exponent order is **n > m > 1** (Keramati & Gutkin 2014; Dulberg 2023). Both candidates had copied m > n > 1 from a garbled copy of Yoshida et al. 2025, and both are now corrected.

**Read since:** arXiv 2611.01183, "Satisfied, Not Solving" (research/metoyer-2026-satisfied-not-solving.md). It led to D67.
- **ES20 (factored against monolithic values, under drift).**
  - The candidates' factored rule costs 0.02–0.22× a tabular HRRL value in every condition (40/40 seeds at N = 8).
  - The scaling Dulberg et al. report (a bigger gain with more needs and faster drift) was **not** reproduced: ES20-2 and ES20-3 were refuted.
  - The monolithic baseline regulates badly everywhere, so this is a weak test of the scaling claim.

## Tampering (D67; research/metoyer-2026-satisfied-not-solving.md; ES21)

- A drive that reads a resettable sensor is gamed on 99.99% of steps, with a 4473× true cost (ES21-A).
- D67 requires both candidates to:
  - read b only from innate event detectors (raw input, the agent's own output removed);
  - keep learned parameters out of d;
  - freeze slow terms inside rollouts;
  - compute learning progress and predictability with an innate predictor.
- Costate's w(e) now follows an innate clock. The Robust regulator has constraint K7.
- The attachment-weight route was not profitable in its toy (ES21-B, refuted), so the freeze remains the guarantee.
- **ES20b (a full-state monolithic baseline), corrected after VERIFICATION-5.**
  - The run's "about 20×" advantage at 8 needs came from an unstable baseline: its b² features and normalized learning rule.
  - With the exact model class [1, b] (VERIFICATION-5's probe, not pre-registered), factored costs **0.72–0.73×** monolithic at 8 needs. The advantage grows with the number of needs *in direction*, by roughly 1.4×, not 20×.
  - **The drift results (ES20-3, ES20b-3) are consistent with Dulberg et al.,** who found the monolithic agent did worse under *slower* change. My pre-registered direction was the misreading.
