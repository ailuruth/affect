# Costate: second independent verification (revision §2.4, new S1 §7, CS1, CS2)

2026-11-25. Reviewer did not write the candidate. Scope: only what is new since VERIFICATION.md. Files read: costate.md, brief.md (Foundations research, Stages), evaluation.md (E2, E3, S1), sims/costate/{PREDICTIONS,RESULTS}.md, sim_cs1_field.py, sim_cs2_dyad_steering.py, analytic_cs1.py, env_t1.py, ../synchrony.py, ../thermo/sim_th6_structure.py and thermo PREDICTIONS/RESULTS TH6. No existing file was edited.

## Summary verdict

- **CS1 and CS2 both reproduce bit for bit** (full runs) (see Sims rerun). The numbers in RESULTS.md are the numbers the code produces.
- **But CS1's decisive input does not come from the cited derivation.** analytic_cs1.py, as committed, gives μ_B = 0.7155 (B back in 60 min), not the 0.306 hard-coded in sim_cs1_field.py:15 and quoted in PREDICTIONS.md:227. With the committed analytic value, μ_B > μ_C (0.7155 > 0.7081). The costate field would then rank B marginally above C (cue value 0.215 against 0.212), and the 10:1 C-over-B separation would vanish. 0.306 is μ_B for a 10-min return, which matches the scenario text (PREDICTIONS.md:222). The headline "anticipation per entity" result therefore depends on one parameter that RESULTS does not report: B's return delay, with a crossover near 58 min. The script cited as the source contradicts the value used.
- **§2.4's attention rule is derived only for actions on the body.** For memories and cues, the candidate's own Pontryagin form prices the effect through ∇_xV, not μ. The "top-k is derived" claim is wrong as stated: a fixed per-item cost gives a threshold, a fixed budget gives top-k.
- **The CS1-1 verdict label is wrong under the project's own rule.** CS1-1 is a three-clause conjunction with two clauses failed, so it is refuted, not "partly refuted" (RESULTS.md:174 already established this for F2). costate.md §2.4:117-122 reports only the passing clause.
- **The V-shaped S1-b prediction is not V-shaped on the published score.** On the CS2 toy the score is a notch at μ_c ≈ 0 and flat elsewhere (probe below). It rests on the |μ_c| gain that VERIFICATION.md already labelled a heuristic, and CS2 implements a signed gain, so it never tested it.
- **Expressive structure: 0 of 4 items fully met** (1 partly, 2 partly, 3 partly, 4 not met). The status line (costate.md:3) still says "not complete: revision required", which is accurate.

## §2.4 derivation

1. **The field and the drive (costate.md:99-102).** Indexing b by entity is a relabelling of b ∈ ℝ^{k·|ℰ|}. Nothing uses ℰ as a "learned space": there is no kernel, metric or smoothness across entities, so it is a finite indexed vector, a set, not a field. The drive needs w(e) ≥ 0 for convexity; this is not stated, and w(e) is "learned" with no learning signal given. §2.2:69-72 still says three parts are learned "and nothing else"; ℰ and w(e) are now also learned.
2. **The costate field (costate.md:104-105).** μ_k(e) = −∂V/∂b_k(e) is correct and follows from §2.2 unchanged. The Pontryagin Hamiltonian extends componentwise. Fine.
3. **value(i) = Σ μ_k(e)𝔼[Δb_k(e)|i] (costate.md:109-111).** First-order: −ΔV ≈ μ·𝔼[Δb|i] − ∇_xV·𝔼[Δx|i]. §2.4 drops the second term.
   - For **actions** that move the body (message_C), the dropped term is the world-acting part, and μ·𝔼[Δb|a] is the correct first-order price, consistent with Prop 5 (costate.md:361-371). Derived.
   - For **memories and cues**, selecting an item changes the information state x, not b. By costate.md:84 such effects are priced by ∇_xV, and the immediate 𝔼[Δb|i] is ~0. The key used in CS1 is the body effect the episode *recorded* (TH6 construction, thermo PREDICTIONS.md:127), not the effect of retrieving it. So for memory and perception the rule is an analogy (retrieve what once relieved the needs that are now priced high), not the marginal analysis. costate.md:113 ("the key is the world model's prediction of the item's effect on the field") does not match what CS1 implements.
   - **Three attention rules now coexist without reconciliation:** §2.4 μ·k_i (signed); cue mask and perception precision |∂V/∂o_i|σ_i (costate.md:231, 256; unsigned); retrieval by a kernel on (μ, x) tags (costate.md:232). They disagree in sign. Under §2.4 a sated agent ignores the face of the person present (CS1: P(A_face) = 0.004). Under the |μ_c| mimicry gain (costate.md:196-198) it attends to that face *more* when over-sated. Since K1 makes the face the only route to perceiving the other, this matters for S1.
   - "= μ·k_i" holds only if items' effects are additive. CS1 retrieves five near-duplicate C episodes, which an additive rule gives and a rule with diminishing returns would not.
4. **"Proposition 1 still applies per entity" (costate.md:102).** The conclusion is right but the phrasing is not. Prop 1 is a statement about joint convexity of V over the whole b vector. With w(e) ≥ 0 it applies to the whole field, including cross-entity coupling through shared actions, and per-coordinate monotonicity follows. Per-entity affine dynamics are neither necessary (affine cross-coupling is fine) nor sufficient: the other assumptions (costate.md:282-284) still bind. They fail more often in the field. Whether a person returns depends on the agent messaging them (independence from u fails). b_p(τ) is defined from x's prediction error (costate.md:160), so it is not affine in (b, u), and x depends on b.
5. **"Top k is derived" (costate.md:114): wrong as stated.** Prop 5's marginal analysis with a fixed per-item cost c selects every item with value > c, a threshold with a variable count, which is what the cue mask at costate.md:231 already does. Top-k follows from a fixed *budget* of k slots with equal costs and additive values (a knapsack with unit weights). "Softmax not derived" is correct within the candidate: there is no entropy term in §2.2. Note that CS1's cue and action clauses are stated in softmax probabilities (PREDICTIONS.md:231, 234). So the two failed clauses test the non-derived part, and the one passing clause (the argsort, sim_cs1_field.py:25) tests the derived part.
6. **"Requirement, from CS1" (costate.md:115).** The diagnosis is right, but the reason is dimensional rather than the covector law of Prop 2. 2(b*−b) = −∇d has units of d per b. μ = −∇V has units of d·h per b (roughly ∇d/(ρ + decay)). The fix (forecast costates for topics) needs an event model for topic exposure, which K5 does not supply. CS1 has not been rerun with it.

## Expressive-structure requirement (brief.md:49-54), item by item

| Item | Verdict | Reason |
|---|---|---|
| Content-dependent attention selecting what is perceived, remembered, done | **Partly met** | Stated (§2.4) and the memory clause passes in CS1. But: the pre-registered cue and action clauses failed (CS1-1); the rule is derived only for body-acting actions (§2.4 derivation, point 3); the keys are hand-set one-hots, not world-model predictions; the score is one bilinear product with a single query; three conflicting attention rules remain. |
| Needs structured over people, relationships, episodes, topics, time as sets/graphs/fields | **Partly met** | People and topics: yes, as an indexed set. Relationships (edges between people): absent. Episodes are listed as entities in ℰ (costate.md:100), but "need k with respect to an episode" is never defined; in CS1 episodes are items, not field entries. Time: unchanged multi-timescale table (costate.md:183-188). The "learned space" has no geometry. |
| Effective dimensionality, and a behavior the low-dim version cannot produce, shown by ablation | **Partly met** | Dimensionality is *stated* as a component count (costate.md:125) and *borrowed* from thermo TH6 (2.85). That number was **refuted** against its own ≥ 3 threshold (thermo RESULTS.md:114), uses thermo's body rates (not T1's) and measures the body field, not the costate field. Not computed for Costate. The ablation: the collapsed arm cannot separate people *by construction* (identical summed keys, sim_cs1_field.py:19), so CS1-3 is a tautology. The informative contrast is costate field versus deficit field. That is a different model, not a low-dimensional version, and the contrast flips with the undeclared μ_B parameter (Summary). |
| Richness from structure, not parameter count | **Not met** | Not addressed in §2.4. The only richness added is the count of components k·|ℰ|, which grows with entities. There is no composition, no relations and no multi-head or content-dependent query. Strictly, the core is still scalar gauges (now k·|ℰ| of them), a scalar V and a linear readout (μ·k). The nonlinearity sits only in V's per-entity forecast. That is real (it produced the B/C reversal), but it is one mechanism. |

Stale text contradicting the revision: costate.md:3-14 (status and "planned next"), costate.md:48 (k ≈ 3), costate.md:465 (§9 "μ has about 3 components"), and §6 table (costate.md:390-400), which has no CS1 or CS2 rows.

## S1 predictions (costate.md §7:404-410)

- **S1-a and S1-c** cite sim C (5 runs). evaluation.md requires ≥ 20 runs for S1-a (evaluation.md:161), ≥ 20 instances plus a sham lesion plus a severity sweep for S1-c (evaluation.md:176), both window settings reported (154), and AU channel pairs fixed in advance (153). CS2 and sim C use one mode, one window setting, 5 runs, no sham and no sweep. The w = 0 lesion removes the only input path, so its disappearance is guaranteed by construction. The PREDICTIONS thresholds were met; the evaluation.md S1 protocols were not.
- **V-shaped prediction (costate.md:408).**
  - It rests on w ∝ |μ_c|, which costate.md:196 and VERIFICATION.md item 6 label a heuristic. A prediction labelled "distinctive" is resting on a non-derived step.
  - It contradicts Prop 3 at costate.md:339 ("increasing in w, and hence in μ_c").
  - At μ_c = 0, w = 0, so a sated agent has no coupling and S1-a fails at satiety. The S1 claim is then conditional on the operating point, and this is not said.
  - On the published score it is a notch, not a V. Probe (CS2's own `run()`, 3 seeds × 5 min): score 0.095 at w = 0, 0.351 at w = 0.1, 0.393 to 0.400 for w = 0.25 to 6.67, and 0.365 to 0.475 for w = −0.1 to −0.9. The score saturates for |μ_c| ≳ 0.02, so there is no graded V. This is the CS2 result applied to the candidate's own prediction.
  - No pre-registered test exists. CS2's levels give μ_c ∈ [0.1, 0.5] and never cross 0.
- **CS2 recording (costate.md:409).** Accurate: it is refuted as stated, and S1-a and S1-c pass the PREDICTIONS criteria. The restatement as "partner-driven variance share" will also be near ceiling at σ = 0.05 unless the agent's own noise is raised. That should be said before the retest is pre-registered.
- Labels collide: "S1-a" names both the new E3 test (costate.md:406) and the former lesion study (costate.md:414). costate.md:412 is an empty heading.

## Sims rerun

Commands from sims/costate: `uv run python sim_cs1_field.py`, `uv run python sim_cs2_dyad_steering.py`, `uv run python analytic_cs1.py`. Outputs went to /tmp, not to out/.

- **CS1:** output identical to out/cs1.json (diff empty). Matches RESULTS.md:196-198.
- **analytic_cs1.py:** A −0.0497, **B 0.7155**, C 0.7081. RESULTS and the sim use B = 0.3062. μ_B as a function of return delay: 0 min 0.106, 5 min 0.214, **10 min 0.306**, 30 min 0.552, 55 min 0.698, 58 min 0.709, 60 min 0.716 (crossover with μ_C = 0.708 at about 58 min).
- **CS2:** run in full: all 200 steering runs and all 10 surrogate-tested runs, 41.5 min. The output is identical to out/cs2.json (diff empty) and matches RESULTS.md:217-225. Run time is dominated by the 20,000 surrogates; the steering part alone takes about 1 min.
- **Recomputed from out/cs2.json:** derived one-sided p = 0.028. Means are not monotone (0.424 > 0.412). The s = 0 → 0.2 change is 0.00372 for derived and 0.00368 for random. The random effect is not < 0.5 × the derived one.

## Spec-vs-code mismatches

CS1 (PREDICTIONS.md:215-236 against sim_cs1_field.py):
1. PREDICTIONS.md:227 cites analytic_cs1.py for μ_B = 0.306. analytic_cs1.py:9 computes a 60-min return and gives 0.7155. The sim hard-codes the value (sim_cs1_field.py:15) instead of importing it. The sim and PREDICTIONS:222 (10 min) agree with each other but not with the script cited as the source.
2. The deficit-field values, collapsed query (0.3215), T, episodes, cues and actions all match the spec and TH6's construction (rng sequence identical to thermo/sim_th6_structure.py:6-12).
3. PREDICTIONS:227 calls 2(b*−b) "the myopic costate". It is −∇d, the deficit arm's quantity. This is a naming issue, not a code mismatch.

CS2 (PREDICTIONS.md:238-259 against sim_cs2_dyad_steering.py):
1. The internal state z is not simulated. μ_c = 0.3 + s·(u·d) is a constant (line 23). This is equivalent for a static offset, but the variable `z` in the code is the *partner* (line 18), a name collision with the spec's z.
2. w is signed, w = 4μ_c/0.3 (line 34). This matches PREDICTIONS:245 but not costate.md:196/407-408 (|μ_c|). It is harmless only because μ_c stays in [0.1, 0.5].
3. Scored channel "ỹ·U₈ and y·U₈": the code uses U[:,7] (line 20), the mode with s = 2.0, the largest and most saturated. This is consistent with sim C but not stated as such.
4. Noise is added as 0.05·√dt without the 1/τ factor (line 19). That is equivalent since τ = 1.
5. Against evaluation.md S1 (not PREDICTIONS): 5 runs, not ≥ 20, for S1-a and S1-c; no sham and no severity sweep; strengths not expressed as a fraction of the state's norm (evaluation.md:165); one window setting; one mode, not AU channel pairs. These are mismatches of the pre-registration against the protocol it claims to instantiate.
6. Otherwise the code matches: OU partner τ = 2 s; c = 4, τ = 1, σ = 0.05; G from seed 7; 5 levels × 20 runs; random d per run; 10 Hz; 30 s / ±5 s windows (synchrony.py:4, W = 300, L = 50 at 10 Hz); 1,000 surrogates of each type; 95th percentile.

## Errors

1. **[major]** The CS1 headline depends on μ_B = 0.306, which the cited analytic script does not produce (it gives 0.7155, which reverses the B/C order of the costate field). Either the script or the spec is wrong, and the dependence on B's return delay (below about 58 min, μ_B < μ_C) is not stated.
2. **[major]** §2.4 claims a derivation for memory and cue attention that drops the ∇_xV term the candidate's own Pontryagin form assigns to information-changing selections.
3. **[moderate]** "Top-k is derived ... with a fixed per-item cost": a fixed cost gives a threshold; top-k needs a fixed budget and additive values.
4. **[moderate]** The RESULTS.md:200 label "CS1-1 partly refuted" should be **refuted** (a conjunction with 2 of 3 clauses failing; same rule as RESULTS.md:174). costate.md:119 reports only the passing clause.
5. **[moderate]** The V-shape prediction: it rests on a heuristic, contradicts Prop 3's wording, implies no coupling at satiety, and on the E3 score it is a notch, not a dose-response.
6. **[moderate]** Effective dimensionality is borrowed from a refuted thermo result with different dynamics.
7. **[minor]** "Prop 1 per entity" is misframed. The missing condition w(e) ≥ 0 is not stated.
8. **[minor]** CS1-3 is true by construction. CS2-4 (w = 0) is true by construction.
9. **[minor]** CS2-3 and CS2-4 are tagged "(S1-a, E3)" and "(S1-c, E1)" though they do not meet evaluation.md's S1-a or S1-c protocols.
10. **[minor]** Stale text: costate.md:3-14, 48, 69-72, 390-400, 465. Label collision at 406/414 and an empty heading at 412.

The CS2 verdict labels (RESULTS.md:222-225) follow the pre-registered thresholds. The CS1-2 and CS1-3 labels follow them.

## Recommended fixes

1. Make analytic_cs1.py compute the 10-min case (or the spec state 60 min and rerun), import μ from it in sim_cs1_field.py, and add a sweep of B's return delay to RESULTS. State the crossover (μ_B = μ_C at about a 58-min return).
2. Relabel CS1-1 as refuted in RESULTS.md, and report all three clauses in costate.md §2.4.
3. Restate §2.4's rule as value(i) = μ·𝔼[Δb|i] − ∇_xV·𝔼[Δx|i]. Call the memory and cue form a heuristic, or derive the key as the body effect of the *best action the item enables*. Reconcile it with |∂V/∂o|σ and the (μ, x) kernel, or delete those rules.
4. Replace "top k is derived" with: threshold under a per-item cost; top-k under a fixed budget, with additive values assumed.
5. State w(e) ≥ 0 and how w(e) and ℰ are learned. Update §2.2's list of learned parts.
6. Compute the effective dimensionality for Costate's own dynamics, for the costate field (not only the body field), and report it against a threshold fixed in advance. Remove the reliance on refuted TH6-5.
7. Replace the collapsed ablation with a non-tautological low-dimensional version, for example a per-entity deficit plus one global anticipation scalar, so the ablation isolates per-entity forecasting.
8. Drop or reformulate the V-shape. Either predict a notch at μ_c ≈ 0 on the E3 score (testable, with levels crossing 0 and |w| sign handling fixed in code), or predict the V on partner-driven variance share at a stated agent noise level, pre-registered.
9. Bring the next S1 pre-registration to evaluation.md's protocol: ≥ 20 runs, sham lesion, severity sweep, both window settings, AU channel pairs, strengths as a fraction of norm, and one named unrelated behavior.
10. Update the stale sections listed in Errors item 10.
