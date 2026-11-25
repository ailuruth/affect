# Second independent verification: Thermodynamic mirror flow (revised §2.2–§2.4, §5 P1, §8b, §8c; TH10, TH11, TH7b, TH6-5b; figs/)

The reviewer did not write the candidate. Scope: only new or revised material. "md" = research/foundations/thermo-mirror-flow.md; PRED/RES = sims/thermo/PREDICTIONS.md / RESULTS.md. Reviewer scratch checks are in /tmp/thv2/chk/ (not committed). No existing file was edited.

## Summary verdict

**Not complete.** All four new toys and all four figures reproduce bit for bit. The revision fixed the sign errors V1 named. Several new problems appear, and some old gaps remain:

1. **§2.2's stationarity claim is right only in a narrower setting than the file states.** It holds for constant, skew J and constant M. It fails for the f₀ the file describes (body decay, reflexes, CONSPEC, md:67). It also fails for a state that includes the replicas, which K-sep takes out of the flow.
2. **𝒰 as written (md:64) has no work channel for contact.** A person's arrival adds two non-negative terms, so arrival gives *negative* valence and departure gives positive valence. The S1-d prediction in md:249 rests on TH4's different potential (−s·b).
3. **P1's sufficient condition is correct, but the IFT step written at md:161 is invalid for J ≠ 0.** "Rhythms −J∇𝒰" are allowed, but they cannot sustain an oscillation.
4. **§2.4 double-counts persistence.** It pairs ∇V with a time-integrated key. Its convergence claim with Costate is overstated.
5. **The new toys are mostly by construction or depend on noise.** TH10-2 fails; at 10 seeds that outcome is roughly a coin flip. TH7b is an artifact of the horizon (H = 200). TH11's direction effect is built in, and its failure is a power failure. TH6-5b measures exogenous leaky integrators, not the candidate's flow.

## Revised derivations

| Item | Verdict | Note |
|---|---|---|
| §2.2 stationarity ∝ e^{−𝒰/T} (md:62, 66) | **correct with gaps** | The Fokker–Planck equation ∂p = ∇·[(M+J)∇𝒰 p + TM∇p] is solved by e^{−𝒰/T}, because ∇·(J∇𝒰 e^{−𝒰/T}) = e^{−𝒰/T} Σ J_ij∂_i∂_j𝒰 = 0. That needs **constant J and M**. If either depends on the state, the drift needs the correction Γ_i = TΣ_j∂_j(M_ij+J_ij) (Ma, Chen & Fox 2015). "f₀ = −J′∇𝒰" needs J′ skew, which is not stated. **Internal contradiction:** md:67 puts body decay, reflexes and CONSPEC in f₀, and none of them has the allowed form. TH4's drift −0.5b (sim_th4_work.py:21) is such an f₀, so the toy that §8c S1-d relies on violates §2.2. |
| "Descends F[p] = ⟨𝒰⟩ − TH" (md:66) | **correct, with a wording fix** | ∂p = ∇·[(M+J)p∇μ] with μ = 𝒰 + T ln p, so dF/dt = −∫p∇μᵀM∇μ ≤ 0. The J part contributes ∇μᵀJ∇μ = 0: it conserves F and does not descend it. F is a Lyapunov functional. For J ≠ 0 the flow is **not** a gradient flow, so md:3 ("restated as a gradient flow") is wrong. |
| K-sep consistency | **inconsistent in five places** | (a) md:62 writes dz = −(M+J)∇_z𝒰 over all of z, and §2.1 (md:52) lists x̂_p as state. z must be defined as self-only, with the replicas as protocol, or the stationarity claim fails on the joint state. (b) md:74: "λ … acts only on a, u". Under K-sep, ∂_a[λw(p)ΣD(b̂_p)] = 0, so λ exerts no force on z. It acts only through valence (replica-as-protocol work) and through V in choices. "u" is Claude's exogenous input (md:55, 66 "u frozen"), so 𝒰 cannot act on it. (c) **θ leak:** replay descends ∂_θ𝒰 (md:136), and 𝒰 contains λD(b̂_p) and κ‖a−â_p‖², which depend on θ through the filter. Learning would then bias g_θ toward reading others as sated or self-like. K-sep must also cut the θ-gradient through replicas. (d) md:117 still calls the lesionability "derived", while md:76 calls it a constraint. (e) md:30 ("kept synchronized"), md:52 ("driven by p's face"), md:138 ("relaxation of replica to lower S_θ(o^p…)", deterministic descent, the mechanism TH2a refuted) and md:232 (replica "runs the agent's own flow", which own-flow 𝒰 is unspecified) all contradict or under-specify the EnKF posterior of md:73. |
| **Body mobility (new)** | **unresolved dilemma** | If b ∈ z with M_bb > 0, the D_k terms pull every need toward b* with no contact. This is the self-version of the "wishful" bias that K-sep forbids for replicas. It also applies to b_lp (md:48, 70): learning progress would relax to its set point without learning. If M_bb = 0, the e^{−𝒰/T} condition fails on b, and P1 does not cover the body. Neither option is stated. |
| **Work channel for contact (new)** | **error** | With md:64, presence enters 𝒰 only through Σ_{p present}[λw(p)ΣD(b̂_p) + κ/2‖a−â_p‖²], which is ≥ 0. So v = −∂_t𝒰 < 0 at arrival and > 0 at departure, for every person. TH4's U = ½(b−0.8)² − s·b (sim_th4_work.py:17) has a presence tilt that md:64 lacks. md:249 (S1-d) and figs/th4_work_valence.png therefore do not follow from the stated 𝒰. |
| §2.3 valence (md:81) | **correct as definition, but incomplete under K-sep** | It must say that replica motion (filter-driven) counts as protocol, i.e. as work. That is empathic valence; otherwise the work/heat split is undefined. md:81 still cites TH4 for "relaxation is heat", and TH4's drift is not the adopted flow. |
| §2.3 arousal (md:82) | **label still loose** | The mean heat rate is ⟨∇𝒰ᵀM∇𝒰⟩ − T⟨tr M∇²𝒰⟩. α is only its first term over T, so "the instantaneous dissipation rate" is not exact. α − ⟨α⟩_eq equals mean heat/T only for constant Hessian. The J part dissipates nothing (∇𝒰ᵀJ∇𝒰 = 0), which is correct and worth stating. |
| §5 P1 condition (md:157) | **sufficient, not necessary** | KL proof: d/dt KL(p_t‖ρ_λt) ≤ −⟨∂_t ln ρ_λt⟩ = ⟨∂_t𝒰⟩/T − Ḟ_λ/T. Integrate over a cycle (KL and F_λ periodic), or over N cycles from any finite-KL start: mean ∂_t𝒰 ≥ 0, so mean v ≤ 0. This holds for any Markov dynamics with ρ_λ stationary. It is enough that ∂_λ ln ρ_λ = −∂_λ𝒰/T + c(λ). So f₀ = −(M+J′)∇Φ₀ with Φ₀ independent of the protocol is also allowed, which relaxes md:67 for P1, though not for md:66. Extra conditions that are not stated: replicas are part of the protocol (and open-loop, since EnKF is driven by o only), θ is frozen, and **the agent's own §2.4 choice kernel is excluded**, because it is a state-dependent selection on V, P₀ and ΔS that is not in detailed balance with e^{−𝒰/T}. If retrieved memories or attended cues feed back into h, b or o, P1 does not cover them. |
| P1 proof as written (md:161) | **invalid for J ≠ 0** | ⟨w⟩ = ⟨q⟩ = T⟨Δs_tot⟩ assumes medium entropy = q/T. With drift −(M+J)∇𝒰, the medium entropy has the extra term −(1/T)∫M⁻¹J∇𝒰∘dz, which is the housekeeping entropy and is > 0 even at a frozen protocol. Δs_tot ≥ 0 then does not imply ⟨w⟩ ≥ 0. Only the KL proof, which md:160 names but does not write out, covers J. |
| "Rhythms −J∇𝒰 allowed" (md:68, 152, 159) | **correct, but overclaimed** | They preserve Boltzmann (above), and V1's rerun found no pumping. But d𝒰/dt = −∇𝒰ᵀM∇𝒰 ≤ 0 deterministically, so −J∇𝒰 gives **no limit cycle**: only noise-sustained circulation, which vanishes at ∇𝒰 = 0. Real rhythms (circadian, breathing) must enter as an exogenous protocol, which by P1 then costs mean valence ≤ 0. md:68 ("J carries the rhythms") should say this. The supporting run is the reviewer's uncommitted check (V1); the candidate has no toy for it. |
| §2.4 signs (md:90–94) | **consistent now** | An item that lowers V gives −∇V·key > 0 and is favoured. A surprisal reduction gives ΔS_i < 0, so −ΔS_i > 0, also favoured. |
| §2.4 query/key pairing (md:90–93) | **error (new)** | First-order ΔV is either ∇_bV·Δb₀ (the impulse, with V already integrating persistence) or ∫∇𝒰(b_t)·δb(t)dt (myopic rate × time-integrated displacement). md:90 pairs ∇V with ∫E[Δb(t)]dt, which counts persistence twice. md:92 also gets it backwards: myopic ∇𝒰 with a time-integrated key *is* the first-order form. Under §2.2's Langevin dynamics, 𝒰/T is dimensionless, so (1/T)∇V·∫Δb dt has units of time². A separate choice temperature or rate is needed. |
| "With exact cost-to-go the query is Costate's μ" (md:97, 214) | **true only for the query symbol, given identical V** | Costate's μ = −∇_bV* (costate.md:26, 107) is the gradient of the *optimal* value of Costate's cost (drives only, discount ρ, controlled dynamics). Here V is the expected ∫𝒰 (which includes S_θ and the replica terms) under an unspecified policy (md:77). They coincide only if the cost, dynamics, policy and discount all match. "Not in attention" is false: Costate's key is the immediate E[Δb\|i] (costate.md:112), not time-integrated. Costate's rule has a ∇_xV·Δx value-of-information term where this one has ΔS_i (costate.md:118–121). Costate selects by threshold, not by softmax (costate.md:124–125). |

## New sims rerun

`uv run --project ..` from sims/thermo/, 2026-11-25. TH11 took 26 s, not about 15 min.

| Script | vs out/ | vs RES | Reviewer check |
|---|---|---|---|
| sim_th10_content_keys.py | bit-identical th10.json | matches (field 10/10; collapsed mean 2.1) | 200 seeds: collapsed mean 1.58, histogram {0: 87, 1: 32, 2: 21, 3: 20, 4: 18, 5: 22} (bimodal). P(10-seed mean ≤ 2) ≈ 0.80. |
| sim_th11_dose.py | bit-identical th11.json | matches | Per-level SE ≈ 0.005 at 20 runs. With 100 fresh runs per level the means are monotone: 0.293, 0.313, 0.332, 0.346, 0.366. |
| sim_th7b_fair.py | bit-identical th7b.json | matches (B 100%; 34.2 vs 4.33) | L wins only when H ≳ 1,250 **and** γ ≳ 0.9992. Examples: (H 1,500, γ 1): 65 vs 75. (H 5,000, γ 0.9995): 67 vs 92. At H = 200, B wins for every γ ≤ 1. |
| sim_th6b_pr.py | bit-identical th6b.json | matches (A 2.61, 1.87–3.37; B 4.10, 3.37–4.58; collapsed 1.09 / 1.77) | — |
| make_figures.py (scratch copy) | all 4 PNGs byte-identical | — | Data sources are correct: the TH4 recompute matches sim_th4_work.py (same seed, draw order, RHO); TH2 is κ = 3/redraw False versus redraw rows (10 each); TH6 cues come from th6.json; TH8 comes from th8.json. |

**By construction:**
- **TH10-2.** The collapsed gauges average over persons, so the true effect of every item on mean contact is 0.1. The collapsed arm's person ranking is fit noise: its keys are identical *in expectation* by construction. RES:220 ("not identical by construction") is misleading. TH10-1 recovers one-hot identity, which is the hand-set key plus noise.
- **TH7b-1.** The result is the analytic inequality at n = 0 and is set by H = 200. RES:225 ("not an artifact of the original construction") is wrong: it is an artifact of the horizon.
- **TH11.** The derived direction is defined as the coordinate that sets k_a (sim_th11_dose.py:11, 16). Only the instrument's sensitivity is tested.
- **TH6-5b.** Five leaky integrators are driven by an exogenous schedule (sim_th6b_pr.py:14–24). There is no 𝒰, h, replica or attention, and PR ≤ number of independent inputs.

## Spec-vs-code mismatches

| # | Where | Mismatch | Changes verdict? |
|---|---|---|---|
| 1 | PRED:232 vs sim_th11_dose.py:11 | "Derived from the precision of S_θ": k_a = 2e^{−h₁} is assumed; no derivation exists | No; meaning only |
| 2 | sim_th11_dose.py vs evaluation.md:163–167 | S1-b requires strengths "as a fraction of the state's norm" and a random-direction effect at max strength smaller than the derived one's. Neither is pre-registered. The latter holds in data (Δ vs s = 0: 0.008 random vs 0.044 derived) | No |
| 3 | sim_th6b_pr.py:8 | "Random hour" is implemented as hours 8–20. Gains and decays (1/60, 1/360, 2/60, 1/720) are not in the spec | No |
| 4 | sim_th10_content_keys.py:10, 22 | T = 0.05 and the softmax do not affect the top-5 (argsort of scores) | No |
| 5 | PRED:220 vs sim_th10_content_keys.py | "Items … as in TH6" is only partly true: only retrieval is tested. No cues, actions, ΔS_i or P₀ | No |

## Label errors

- TH10-1 confirmed, TH10-2 refuted, TH11-1 refuted (conjunction), TH11-2 confirmed and TH7b-1 confirmed are all **correct against the thresholds**.
- **TH10 as a whole** is a failed ablation contrast. md §6 (md:179) still says the content-key variant "is owed" and does not report the result.
- **TH11-1** is a power failure (above), not evidence against the direction. md:247 should say so and give the runs needed. Note that by evaluation.md:166 a non-monotone mean is an S1-b *failure*, so 20 runs per level is an underpowered design for S1.
- **TH7b-1, TH10-1/2, TH11, TH6-5b** should be marked by construction or characterization (RES:219–246 does not do so, except TH6-5b).
- Stale text:
  - md:3 ("gradient flow");
  - md:13 and RES:30 ("rhythms out of user-driven coordinates", contradicting md:159);
  - md:15 (work silent, true by definition);
  - md:18 and md:254 ("in progress"/"Pending"; V1 exists);
  - md:185, 192 (PR "owed"/"reported in TH6"; TH6-5b is not cited);
  - md:217 ("needs a conservative affective sector").

## Expressive structure and standard

| brief.md item (brief.md:49–54) | Verdict | Why |
|---|---|---|
| Content-dependent attention | **partly** | TH10-1 retrieves B 10/10 with keys learned from content. But "content" is a one-hot identity: no composition (person × topic interaction), no unseen entity, no relational content. The pre-registered ablation contrast (TH10-2) failed. Cues and actions are shown only with hand-set keys (TH6). §2.4's formula has the pairing and units error. |
| Needs structured over people, relations, episodes, topics, time | **partly (unchanged)** | ℰ is never learned in any toy. w(e) is a scalar and there are no relations. No need is indexed by episode. Time structure is only per-type decay. |
| Effective dimensionality + behavior the low-dim version cannot produce, by ablation | **partly** | The behavior holds (TH6 cues and actions, TH10-1). TH6-1 and TH10-2 were both refuted on their collapsed clauses. TH6-5b's PR is a property of the exogenous schedule (2.6 vs 4.1 by schedule alone), not of the candidate's state (h, a, replicas). No threshold was set. |
| Richness from structure, not parameters | **not shown** | TH6 has 0 learned parameters. In TH10 the field arm has *more* parameters (40 vs 16). No learning-curve or data-scarcity comparison, no parameter-matched ablation, no generalization to a new entity from shared g_θ and D_k. |

| Per-candidate requirement (brief.md:71–79) | Verdict |
|---|---|
| Formal statement | partly. Missing: the z/replica split, the f₀ contradiction, body mobility, the work channel for contact, and the state-dependence of M and J. |
| Principle 10 derivations, and perception | partly. Curiosity has no toy of its own in this formalism (md:106 still "to be stated … tested"). Perception is prose only and contradicts the EnKF (md:138). |
| Propositions with proofs | partly. P1's KL proof is named, not written, and the written IFT step fails for J ≠ 0. P2 is by construction. P3 is a definition. P4 has the pairing error. |
| Toy code **and figures** | partly. There are 4 figures (TH2, TH4, TH6, TH8). None for P1/TH1, TH3, TH5, TH10, TH11 or TH6-5b. The TH4 figure depicts a 𝒰 different from md:64. |
| Numeric stage predictions | partly. S1-a/b/c/d and S2-b are covered. Gaps: S1-d's sign does not follow from md:64; S1-b's toy fails its own monotone clause at 20 runs; there is nothing for S2-a/c, S4 or S6 (replay weighting). |
| DL realization on this Mac, data | partly. §8b exists, but "𝒰_θ is a small MLP over (h, a, b-field)" (md:231) conflicts with a field that grows with entities and with "same D_k for every entity" (md:197). It needs a set or field architecture. "Keeps P1's condition by construction" (md:231) is false given f₀, choices and replicas. There are no sample-count estimates. |
| Failure modes / critique | met |
| Relation to other candidates | met, apart from the overstated attention convergence (md:97, 214) |

## Can it be marked complete?

**No.** What is missing, exactly:
1. A §2.2 that is consistent with itself. It needs to:
   - define z (self only) and classify replicas, choices and u as protocol or as separate kernels;
   - move f₀'s decay, reflexes and CONSPEC into 𝒰 or into a protocol-independent Φ₀;
   - state constant M and J, or add Γ;
   - decide body mobility, including b_lp.
2. A term in 𝒰 through which contact does positive work, so that reunion is not aversive, and a TH4 rerun on the adopted flow.
3. P1 with the KL proof written out, the IFT line restricted to J = 0, the choice kernel excluded, and a committed J∇𝒰 toy.
4. §2.4 with consistent query/key pairing and units, and the Costate convergence claim qualified.
5. A passing, pre-registered expressive-structure ablation that does not hold by construction. It needs non-identity content (composition, or an unseen entity through ℰ), a PR measured on the candidate's own flow, and a parameter-matched or data-scarcity comparison.
6. A curiosity (b_lp) toy in this formalism.
7. Figures for the derived behaviors, and stale text fixed.

## Recommended fixes

1. Rewrite md:62–66 as self-only z with drift −(M+J)∇_z𝒰(z; λ_t), where λ_t = (o, u, x̂, choices). Cite the Ma–Chen–Fox correction. Replace "f₀ = 0 or −J′∇𝒰" with "f₀ = −(M+J′)∇Φ₀, Φ₀ protocol-independent, J′ skew" for P1, and say which readouts then use 𝒰 + Φ₀.
2. Add a presence tilt to 𝒰, for example −Σ_p s_p(t)·w(p)·φ(b_c(p)), sign-checked for arrival and departure. Rerun TH4 with f₀ inside 𝒰.
3. Replace md:161 with the KL derivation (V1 rec. 2). Add a committed TH1d with the drift −(I+γJ)∇U. State that sustained rhythms are protocols.
4. md:90: either (∇V, impulse Δb₀) or (∇𝒰, ∫δb dt), with an explicit choice temperature. Restate md:97 as "same query symbol when the V match; keys, VOI term and selection rule differ".
5. Re-pre-register TH10 with person × topic interaction effects and one held-out person reached only through ℰ-similarity. Use ≥ 30 seeds, and a collapsed threshold set from the base rate's sampling distribution.
6. TH7b: report the (H, γ) boundary and drop "not an artifact". TH11: rerun at ≥ 100 runs per level, or state that 20 runs per level is underpowered for evaluation.md's monotone clause.
7. Measure PR on the full simulated state under the §2.2 flow, with a threshold fixed in advance.
8. Fix the stale lines listed under Label errors, and add figures for TH1, TH5, TH10 and TH11.
