# Verification 3 of the expressive-structure test bed (ES7b, ES8b, ES10b, ES11, ES12, ES13; §2.2 rewrite; D66 amendment)

Independent check, 2026-11-25. I did not write this work and edited no existing file. Reruns ran in a copy at /tmp/v3r2 with the project venv (sims/.venv, numpy 2.5.5, scipy 1.18.1). Probes are in /tmp/v3probe (not committed). Paths below are relative to research/foundations/ unless they start with DECISIONS.md. Line numbers are to the files as they stand now.

## Summary verdict

- **Reproducible.** All six new scripts, and all five ES12 arms, reproduce **byte for byte**.
- **Honest on the new verdicts.** The new results are reported correctly against their thresholds. ES11-2, ES12-2 and ES12-3 are reported as refuted.
- **Two new results lack a by-construction label:**
  - **ES7b-1.** Contact is hard-coded as a constant outside learning.
  - **ES13.** The participation ratios are set by the world and by the scale of m, not by either candidate's structure.
- **The in-place corrections were made in RESULTS.md only, and only partly.** costate.md, robust-regulator.md and STATUS.md still carry every stale line VERIFICATION-2 listed, and STATUS.md:70 says "labels applied in place". Both candidate files contradict themselves again, between their headers and their new sections.
- **§2.2 of robust-regulator.md:**
  - *Fixed:* the selection rule now has the right sign and is the exact decrease.
  - *New error:* ĉ_p is now a vector, but its adaptive law is still scalar.
  - *Not resolved:* the old and new laws coexist; |ĉ_p| and ‖ĉ_p‖ are both used; :200 contradicts :92; the stranger-mimicry contradiction is still there.
- **D66 amended:**
  - *Closed:* the reply leak through the contact channel itself.
  - *Not closed for Principle 6:* a probe shows the same leak through any other need whose fill needs the partner's reply. The gain is **1.44** (probe below).
- **ES12 is the first result that separates the candidates.** Look-ahead beats the myopic rule: 0.73×, 120/120 seeds.
- **The learned space has still shown no benefit for needs** (ES11-2, ES12-3), and a no-learning threshold rule beats both candidates (ES12-2).
- **Neither candidate yet meets the expressive-structure requirement.**

## Reruns

| Output | Script | Match |
|---|---|---|
| out/es7b.json | sim_es7b_contact_reply.py | byte-identical |
| out/es8b.json | sim_es8b_learned.py | byte-identical |
| out/es10b.json | sim_es10b_fair.py | byte-identical |
| out/es11.json | sim_es11_field_certified.py | byte-identical |
| out/es12_{roll_learned, roll_identity, myopic_learned, certificate, roll_true}.json and .log | sim_es12_rollout.py <arm> | byte-identical (each arm took about 2 min) |
| out/es13.json | sim_es13_dimensionality.py | byte-identical |
| out/es12.json (aggregate checks) | **no generating script** | I recomputed it from the per-arm files: 0.727 (0.715–0.739), 120/120; 1.187 (1.173–1.201), 0/120; 0.998 (0.981–1.014), 58/120; true/learned 0.971. These match. |

**Every number in RESULTS.md:338-457 matches the outputs.** One extra figure: roll_identity against myopic is 0.729 (0.716–0.742), 120/120. The rollout gain therefore does not depend on the learned space.

## Spec against code

**ES7b (PREDICTIONS.md:385-398; sim_es7b_contact_reply.py).**
- **The code matches the spec:**
  - the reply is drawn with probability g_k in every arm (:19);
  - in the amended arm, the contact prediction is overwritten with 0.3 (:14) and the fill is 0.3 (:20);
  - the reply-contingent fill is 0.3·reply, and the engagement fill is 0.6·g_k;
  - seeds 0–39.
- **ES7b-1 holds by construction.**
  - In the amended arm, contact cannot vary across topics.
  - The only other need, mu2, depends on Y[:, :4], while g depends on Y[:, 4:6] (:9). They are independent by design.
  - The gain of 0.92 (CI 0.73–1.11) is noise around 1.
  - RESULTS.md:347 does not label this. ES7's "partly by construction" note is at :240.

**ES11 (PREDICTIONS.md:400-443; sim_es11_field_certified.py).**
- **The code matches the spec:**
  - the world: clusters N(0, 3²), members ±0.5, A with SD 1/2, presence 0.4, r_p ~ U(0.02, 0.04), the 10% satiety sink, κ = 0.5·exp(−‖Δz‖²/4), noise 0.03;
  - exploration gated on deficit, and exempt for the certificate;
  - features [1, 1{p = q}, |x_p − x_q|] with ridge λ = 1;
  - the winner-take-all gates;
  - the certificate's policy, seeds and criterion (:49-51).
- **Unstated in the spec:** the greedy rest threshold is 0.002 (:19).
- **The certificate is not a compared arm in ES11.** It only gates the run, which is correct.
- **RESULTS.md:363 and :373 do compare it informally**, on calibration seeds 1000–1019 against arms on seeds 0–39, so the comparison is unpaired. ES12 later supports it on the same seeds: certificate 0.125. But the myopic oracle was never run on those seeds.

**ES12 (PREDICTIONS.md:445-466; sim_es12_rollout.py).**
- **The code matches the spec:**
  - options are {rest} ∪ present;
  - the known r_p and sink, and K̂;
  - p̂ = (seen + 0.5)/(t + 2);
  - M = 4 common futures per step (:24);
  - a greedy exact-decrease base policy;
  - choice by the lowest summed d;
  - seeds 0–119.
- **"H = 6" means the immediate step plus 5 propagated steps** (:32).
- **Is this a faithful instance of Costate's K5 rollout costate? Partly.**
  - *What matches:* V is a rollout of the innate f_b under the forecast presence (costate.md:97). Options are ranked by the exact −ΔV(i), the full form at costate.md:120.
  - *How it departs from K5's V = min_π*, which is discounted (costate.md:81):
    - It is the value of **one fixed base policy (greedy)**, truncated at 6 steps, undiscounted, and sampled 4 times. That is one step of policy improvement, which gives an upper bound on V.
    - The costate μ = −∇_bV itself is **never computed**. Selection is by rollout differences, not by μ·k_i.
  - So ES12 tests model-based look-ahead, the same thing generic MPC would do, more than Costate's distinctive broadcast price.
  - ES12-2's refutation is a property of the greedy base policy, which RESULTS.md:395 says. A rollout over several base policies, the threshold rule among them, is still within K5 and was not tried.
- **Not isolated:** only the rollout arms know r_p and the sink. The myopic arm ignores drift.

**ES10b (PREDICTIONS.md:468-482; sim_es10b_fair.py).**
- **The code matches the spec:**
  - q₁ = q_s + (1 − a_f²)σ_f² (:12);
  - the prior is 0.25 + σ_f²;
  - the filter propagates every step;
  - the slow EMA is bias-corrected (:24).
- **The one-scale control is weak.**
  - The matched-variance rule matches a *saturating* Ornstein–Uhlenbeck variance with a random walk. That gives q₁ ≈ 0.111², which makes the filter close to "last observation".
  - It loses to the fixed fast EMA (median 0.99 against 0.79).
  - **Probe** (/tmp/v3probe/p_es10b_q*.py). I tuned q on held-out seeds 1000–1039 over {0, 0.003², 0.005², 0.01², 0.02², 0.03², 0.05², 0.07², 0.111²}:
    - the pre-registered q was the *worst* (geometric-mean cost 2.78), and 0.01² was the best (1.22);
    - against the tuned one-scale filter on seeds 0–119, two-scale is **0.68 (CI 0.56–0.82), 92/120**.
  - **ES10b-1 survives a fair control.** RESULTS.md:424 can cite this figure instead of the 40-seed 0.82.
- **Still given the world's generative parameters:** the two-scale filter is (:5). VERIFICATION-2 asked for "all or none".

**ES8b (PREDICTIONS.md:484-502; sim_es8b_learned.py).**
- **The code matches the spec:** the prior, the pseudo-count, updates from observed cues only, and the μ̂ fill-in (:10-22).
- **Not labelled:** the cue *types* are given (`ty`), so the attention runs over a given partition, not a learned space.
- **The magnitude arm is still crippled by the world's design.** It never observes type-3 cues. Random is the fair comparator: 0.063.

**ES13 (PREDICTIONS.md:504-522; sim_es13_dimensionality.py).**
- **The code matches the spec.**
- **The pre-registration was written after ES11.** It quotes ES11-3's result (PREDICTIONS.md:517), so the 4-cluster world was known when the ≥ 3 thresholds were set.
- **Probe** (/tmp/v3probe/p_es13.py, the same 20 seeds):

  | Quantity | PR |
  |---|---|
  | b under the certificate (no learning, no candidate) | **5.02** (ES13-1 claims 5.56 as a candidate property) |
  | The world kernel, PR(KKᵀ) | **4.09** (4 clusters) |
  | Costate's rollout-priced field v | 3.61 |
  | The *myopic* priced field on the same trajectories | **3.18** (also passes ≥ 3) |
  | [e; m] as run | 4.19 |
  | m alone | **4.15** (m is **40×** the scale of e) |
  | [e; m] standardized | 10.05 |

  - **PR(b) is a property of the world and the policy**, not of the candidate.
  - **PR(v) is bounded by the kernel's cluster structure**, and the myopic field nearly matches it.
  - **PR([e; m]) is PR of a low-passed body field.** It leaves out ξ_p and ĉ_p, the Robust regulator's distinctive per-person state.
  - The "1-dimensional reference" is 1 by definition, not measured.
  - **ES13 does not measure either candidate's structure.** RESULTS.md:457 says it "closes item 8", and it does not.

**Pre-registration order.** PREDICTIONS.md was last modified at 12:02:29, after every new output (11:31–12:03). The order cannot be checked from file times. The "11-26" dates are corrected (PREDICTIONS.md:283, :321, :349).

## Labels and verdicts against thresholds

| Test | Value | RESULTS | Correct |
|---|---|---|---|
| ES7b-1 | gain 0.92 (0.73–1.11); ρ 0.001 (−0.054 to 0.057) | confirmed | confirmed, **by construction (unlabelled)** |
| ES7b-2 | 1.72 | confirmed | confirmed |
| ES11-1 | 0.59 (0.57–0.61) | confirmed | confirmed |
| ES11-2 | 1.10 (1.07–1.13) | refuted | refuted |
| ES11-3 | 0.020 | confirmed | confirmed. The gauge runs away (38/40), so the comparison is degenerate in the way ES9-2 was. |
| ES11-4 | 0.638 | confirmed | confirmed, against the *myopic* oracle |
| ES12-1 | 0.727 (0.715–0.739), 120/120 | confirmed | confirmed |
| ES12-2 | 1.187 | refuted | refuted |
| ES12-3 | 0.998 (0.981–1.014) | refuted | refuted |
| ES10b-1, 2, 3 | 0.52; 0.61; 0.57 | confirmed | confirmed. ES10b-1 also holds against a held-out-tuned one-scale filter (0.68). |
| ES8b-1, 2, 3 | 0.0017; 0.063; 1.01 | confirmed | confirmed. ES8b-1's size is by construction (labelled). |
| ES13-1, 2, 3 | 5.56; 3.61; 4.19 | confirmed | confirmed as worded, **but uninformative**: world-determined, and the myopic field also passes (see above). Unlabelled. |

## VERIFICATION-2 "Missing" items addressed?

1. **Principle 6 / D66: mostly, for the contact channel only.**
   - D66 is amended (DECISIONS.md:143-161), and ES7b is run and pre-registered against 1.05.
   - *ES7b-1 is by construction.*
   - *A leak remains through the other needs* (see Principles).
   - *costate.md:97 and :576 still say the rollout predicts "interaction events and reply effects"*, against DECISIONS.md:155.
2. **Labels in place: not done outside RESULTS.md, and partly within it.**
   - *RESULTS.md, fixed:* :15, :18, :45, :129-132.
   - *RESULTS.md, still in place:*
     - the tables' PR of 1.48 (:9; own value 1.95);
     - the PR cited for item 3 (:27);
     - ES2-4 unlabelled (:48);
     - ES2b-1 without 11/20 (:61);
     - ES7's gain without a CI (:226, :234; also DECISIONS.md:137);
     - ES10-2's 0.45 and "beats a single … time scale" (:305, :309);
     - ES8-3's 92% (:257).
     The ES10 runaways are only appended, at :327.
   - *costate.md: none fixed.*
     - "Time is not shown" (:10);
     - the PR of 1.48 (:300);
     - "Items 3 and 4 are shown" (:306, :321);
     - 0.06× unlabelled (:312);
     - 0.81× without a caveat (:315);
     - w adopted on exploratory evidence (:327);
     - 92% (:337);
     - 0.45× (:349).
   - *robust-regulator.md: none fixed:* :20, :210, :216, :222, :225, :231, :247, :259.
   - *STATUS.md: not fixed:* :19, :27, :39.
   - *Dates: fixed.*
3. **Robust regulator §2.2: partly.**
   - *Done:*
     - the sign, and the exact decrease (:75-83);
     - a learning law for Ĉ (:90);
     - the leak toward Ĉ (:89);
     - §4 and §7b updated (:138, :189-193);
     - add-ons marked (:6, :8, :282).
   - *Not done:* see "§2.2 consistency" below. Selection still ignores m.
4. **Needs as a field in a certified-feasible world: done (ES11).**
   - The certificate is empirical, not the fluid linear program, which is adequate.
   - The learned space did not help (ES11-2).
5. **Non-myopic Costate, powered: done (ES12, n = 120).**
6. **ES10 redo: partly.**
   - *Done:* fair controls; the verdict holds against tuned controls.
   - *Not done:*
     - the two-scale filter still gets the world's parameters;
     - no time signature was pre-registered;
     - mood (m, slow μ) is still not exercised behaviorally.
7. **ES8 with learned statistics: done (ES8b).** The types are given.
8. **Own effective dimensionality: done nominally, not substantively** (ES13 above).

**§2.2 consistency (robust-regulator.md).**
- **Dimension error.** ĉ_p is "a vector over needs" (:88), but its law γ⟨e, Hŷ_p⟩ (:72, :89) has a scalar right-hand side. The action term ĉ_p Hŷ_p (:70) is then undefined, or needs an elementwise product.
- **Two laws for one variable.** :72 leaks toward 0, and so does :58. :89 leaks toward Ĉ.
- **Two mimicry forms.** K1 uses |ĉ_p| at :19, :73 and :192, ‖ĉ_p‖ at :91, and signed "κ ĉ_p ŷ_p" at :113.
- **:200 contradicts :92.** :200 says "ĉ_i = Δb̂_i read from the shared map". :92 says Δ̂ and ĉ_p "are different objects". The same sentence is at costate.md:290.
- **The stranger contradiction is unresolved.**
  - With the leak toward Ĉ(x_p), a stranger who resembles relevant people but moves nothing settles at ĉ_p = Ĉ(x_p) ≠ 0.
  - Such a stranger is permanently mimicked, and permanently "cancelled" by a spurious feedforward.
  - That contradicts "pruned for people who do not move the body" (:43, :115, :171), the candidate's distinctive prediction.
- **Ĉ is circular.** It is fitted to "converged ĉ_p" (:90), which are themselves pulled toward Ĉ.
- **"Derivation" overstated.** Greedy control-Lyapunov selection (:80) is one admissible choice, not forced by the problem at :65-67. ES11 and ES12 show it is the bottleneck in field worlds.

## Items 1–4 per candidate

| Item | Costate | Robust regulator |
|---|---|---|
| **1. Content-dependent selection over cues, memories and actions** | **Mostly met.**<br>People: ES1, ES9, ES11. Topics: ES4. Cues: ES8/ES8b, learned statistics but given types. Look-ahead over people: ES12.<br>The cue and memory rules are the first-order heuristic (costate.md:123, :218). Only people get the rollout. | **Partly met.**<br>People and options: through §2.2 plus K4, an explicit constraint, myopic by construction. ES11 and ES12 show that rule is the bottleneck.<br>Cue attention and memory are add-ons. |
| **2. Needs structured over people, relationships, episodes, topics and time, over a learned space** | **Partly met.**<br>The need field is instantiated over a learned space (ES11), but the space shows **no benefit**, either myopic (1.10×) or with look-ahead (0.998×).<br>Episodes are per-person means. Relations: ES2-5.<br>Time: ES10b's two-scale filter is per-person and given the world's parameters. Costate's own slow μ and mood are not exercised. | **Partly met (weaker).**<br>b(e) is instantiated only under its myopic rule, where the space hurts (ES11-2).<br>Relations are unused. Time is an add-on: the ES10b filter is not ξ_p, and m is not exercised. |
| **3. Effective dimensionality, and an ablation** | **Partly met.**<br>Ablation: yes (ES9 0.12×, ES11-1 0.59×, ES11-3 0.02×).<br>Dimensionality: measured (3.6), but set by the world. The kernel's PR is 4.1, and the myopic field scores 3.2. | **Partly met.**<br>Ablation: CT4, ES9, ES11-1.<br>Dimensionality: PR([e; m]) ≈ PR(m). ξ_p and ĉ_p are excluded. |
| **4. Richness from structure, not parameters** | **Partly met.** ES1-4 and ES4-3 hold in worlds that match the model class. ES11-2 and ES12-3 count against it for needs. | **Not shown for its own structure.** No toy exercises ĉ_p with the Ĉ prior. The ES results run through K4's Δ̂. |

**Add-ons, not derivable from the formal statements:**
- **Both candidates:**
  - ε-greedy exploration and its deficit gate;
  - the rest thresholds (0.002, 0.01);
  - the two-scale Kalman filter given the world's parameters (ES10b);
  - per-type running statistics over given types (ES8b);
  - the threshold certificate rule, which beats both candidates and neither derives;
  - D66's innate contact constant (a constraint).
- **Costate:**
  - the reliability weight w and the max(0, ·) form;
  - the cue rule w ∝ |∂V/∂o|σ;
  - memory keys as recorded effects;
  - the rollout's specifics: H = 6, M = 4, a greedy base policy, no discount.
- **Robust regulator:**
  - K4 (Δ̂);
  - greedy selection;
  - need-projected attention;
  - time tracking;
  - Ĉ's regression.

## Principles

- **Principle 2 (no named emotion variables): no problem.**
- **Principle 6 (satiable drives): satisfied** in ES7b, ES8b, ES10b and ES11–ES13. The drives are capped or two-sided, with a sink.
- **Principle 6 (no reward for smiles, attention or time): closed for the contact channel only.**
  - **Probe** (/tmp/v3probe/p_es7b_info.py). This is the amended D66 arm, but need 2 fills only when the partner replies, as learning progress about a topic would (D62; robust-regulator.md:53). Result: **ρ 0.12 ± 0.04, gain 1.44 ± 0.15**, close to the forbidden 1.54.
  - D66 amended excludes only contact from the learned maps (DECISIONS.md:149-151).
  - **Other gaps:**
    - D66 point 2 (expression do-conditioning) still has no toy;
    - dwell-time opportunity is acknowledged (DECISIONS.md:153);
    - DECISIONS.md:149 drops Ĉ/ĉ_p from its list, though the original D66 had Ĉ (:135). The Robust regulator's ĉ_p contact component is still adapted from the partner's face (robust-regulator.md:72);
    - costate.md:97 and :576 are not updated.
- **Principle 10 (one formal core):** the add-ons above, and the §2.2 inconsistencies.

## Can either candidate now be considered to meet the requirement?

**No, for both.**

**Costate, missing in priority order:**
1. **Correct the record in place:** costate.md:5-14, :145, :300-327, :337, :349, :372-374, and STATUS.md:19, :24-27, :39, :70. Label ES7b-1 and ES13 as holding by construction.
2. **Item 2/4: show that the learned space pays for needs.** Use a pre-registered field world where spill knowledge matters under look-ahead, for example overfill that is costly or slow to drain, or sparse presence. Otherwise state that item 2 is instantiated without demonstrated benefit.
3. **Item 3: a dimensionality measure that can tell the candidate from its own ablation** in the same world, and that is not fixed by the kernel. For example, the costate field with and without anticipation, or the latent x, with the threshold set before the world is known.
4. **A K5 rollout closer to min_π:** several base policies, including the threshold rule, to address ES12-2.
5. **Time through Costate's own slow μ or mood,** with a behavioral signature.
6. **Principle 6:** exclude reply-dependent fills of every need from the learned maps and the rollout, or show that the leak is acceptable.

**Robust regulator, missing in priority order:**
1. Make §2.2 consistent: the vector law, a single leak, a single K1 form, and :200.
2. Resolve the stranger-mimicry contradiction that the Ĉ prior creates.
3. Its selection is myopic by its own construction (:83), and that loses in field worlds (ES11, ES12-1). Either accept that item 2 is not met behaviorally, or add look-ahead and say how it then differs from Costate.
4. Derive cue attention and time, or adopt them as numbered constraints.
5. A toy of its own ĉ_p/Ĉ structure (item 4), and a dimensionality measure that includes ξ_p and ĉ_p (item 3).
6. The same records fixes as Costate: robust-regulator.md:5, :9, :20, :210-231, :247, :259.

## Misleading?

**Yes, in these places:**
- **STATUS.md:70** says "labels applied in place", which is false for three files.
- **The status blocks contradict the new sections:**
  - STATUS.md:24-25 ("stood down, still owed") against :73-76 ("done");
  - costate.md:10 and :14 (time not shown; rollout owed), :145 (PR owed) and :372-374 (field and rollout "still owed") against :353-370;
  - robust-regulator.md:9 and :20 against :282.
- **RESULTS.md:455-457 and STATUS.md:86** present ES13 as measuring each candidate's own dimensionality and as closing item 8. It measures the world, and the Robust regulator's figure is m's.
- **STATUS.md:33 and RESULTS.md:347** present ES7b as confirming D66. It confirms a by-construction exclusion, and the leak through other needs is untested.
- **RESULTS.md:406 and STATUS.md:77** ("first result that separates the candidates") are accurate as written. An operator should also read two facts with them:
  - the gain is from generic look-ahead, not from μ itself;
  - a no-learning threshold rule beats both candidates (ES12-2).
- **Stale figures still read as evidence:** the old ES10 figures (0.45×) at STATUS.md:27, costate.md:349 and robust-regulator.md:259, and the 92% at costate.md:337 and robust-regulator.md:247.
