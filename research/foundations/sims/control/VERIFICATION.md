# Robust regulator: independent verification 1

Reviewed 2026-11-25. Material: robust-regulator.md (RR), PREDICTIONS.md (PR), RESULTS.md (RS), sim_ct1–8, make_figures.py, the five cited source notes, brief.md. No existing file was edited. The reviewer's own check scripts ran from /tmp; each one is described in enough detail below to reproduce it.

## Summary verdict

**Not complete for S0.** All eight toys and all four figures reproduce exactly, and every numeric verdict label matches its threshold. The problems are in what the toys are claimed to show:

1. **The headline "forced" claim fails on the candidate's own sources.** The IMP forces an *error-driven* copy of the disturbance generator. It does not force a perceptual observer of each person. In CT1's setting, an error-driven resonator that never perceives the partner regulates better (RMS 0.0089) than the perceptual internal model (0.0191).
2. **The CT5 conclusion is wrong.** A deterministic fixed-gain observer that uses the steady-state Kalman gain reads the slow state exactly as well as the Kalman filter (R² 0.948). The "deterministic" arm cannot move its slow estimate off 0, so its result is by construction.
3. **The mimicry sign is not fixed.** ĉ_p is signed, so at c = −0.5 the face anti-mimics (correlation −0.997). That is the contingency candidate's failure, returning.
4. **A required brief item is absent:** the deep-learning realization and its data needs.
5. **Expressive-structure items 1 and 4 are not met, and items 2 and 3 are met only partly.**

Overall, the candidate is a regulation core with additions around it: three labelled constraints and at least ten unlabelled design choices.

## Derivations

| Item | Verdict | Failing step |
|---|---|---|
| Problem statement (RR:41-43) | Gap | It is a problem class, not one objective. Many controllers solve it, so components are *admitted* by it, not *produced*. Φ, H, R_θ, Γ, F_θ, G, the form of d and the contact sensor are left undefined (RR:29-51). |
| "Forced" per-person internal model (RR:16, 63) | **Wrong as stated** | The design feeds ŷ_p forward (RR:46-47), so the controller is driven while e = 0. That violates the IMP hypothesis "externally driven only when state deviates from target" (francis-wonham:16). What the IMP forces is a model driven by the error. Check: CT1 plant, u = −b − 0.1m − x₁, resonator x₁' = x₂ + e, x₂' = −ω²x₁, with no use of y. RMS 0.0089 against 0.0191 for CT1's internal model. Under the 20-s partner switching of CT4, a crude 3-mode error-driven model gives RMS 0.157 at best (gains 0.3, 1 and 3; it diverges at 10), against 0.0198 for the field version. Perceptual per-person feedforward is therefore *favored* under switching, and *forced* by nothing. RR:16 and RR:63 contradict RR:113-114 and RR:129. |
| P1 (RR:104-114) | Algebra correct (u_ss = λb* − c·y_u); scope honest | The step "realized on the motor substrate ⇒ amplitude ∝ c" fails. An internal model's state is defined only up to a similarity transform, so only its output −c·y_u is canonical, and that output has the anti-mimicry sign. The face instead shows +ĉŷ: a chosen signal, not the generator. K1 is correctly labelled a constraint (RR:113). |
| Mimicry sign (RR:49, 70, 147) | **Wrong** | dĉ = γ⟨e, Hŷ⟩ − σĉ is signed (RR:48; sim_ct1_imp.py:14). Check: CT1 with c = −0.5 gives ĉ = −0.540 and corr(face, partner) = −0.997. The sign then depends on the sign convention of H and e, which is the contingency candidate's ambiguity again. |
| Mood as integral action (RR:32, 62) | Gap | "Forces an integrator", then "the leak keeps it bounded". A leaky integrator is not an internal model of steps, and it leaves a steady error of about ε_m d/K_I. So the leaky mood is favored, not forced. No toy uses the leak: m += b·DT in sim_ct1:15, sim_ct4:15 and sim_ct7:16. |
| P2 small gain (RR:77-79) | Linear algebra correct; the saturation argument is incomplete | (a) CT2a has d = g_s·m (sim_ct2:8). That is linear positive feedback, unstable iff g_s > 0.1, so the result is by construction. (b) The saturated design, the one RR actually relies on, is never simulated. (c) ISS of the regulator, including bilinear adaptation of ĉ and θ, is assumed and not proved. sontag-iss:43 lists it as an obligation. (d) RR:75 routes Claude's words into y, then into the observers, ĉ_p, u and the face. That path bypasses the bound \|ν\| ≤ U unless it is saturated too. (e) The bound itself is about γ(U)/(a·ε_m), up to 10⁴·U/a. Claude can push mood to an extreme within the bound, so "nothing Claude says can destabilize" buys little. |
| P3 influence rank (RR:80, 116) | Correct as an upper bound; holds for smooth maps generally | RR:21 says the mood "must visibly change" Claude's behavior. A rank bound gives no lower bound, so it cannot support "must". Γ itself is not derived: the regulation objective alone is safest at Γ ≡ 0. Γ is a constraint imported from Principle 4, and it is unlabelled. |
| P4 Bode / temperament (RR:72-73, 117) | Theorem check correct; the application is vacuous | The integrals −0.009 and −0.039 equal minus the truncated tails beyond 10³ (0.0100 and 0.0400), so the full integral is ≈ 0. But the area is measured in linear ω. Suppressing \|S\| to 0.01 below 10⁻² rad/s (a mood time scale) costs area 0.046. Spread up to Ω_a = 30 Hz, that raises the mean \|S\| to 1.00024. The waterbed does not bind at mood or temperament scales. CT3's peaks are at 3.5 and 10.7 rad/s: sub-second, not temperament. The θ law (RR:50) is not linked to sensitivity placement, and CT3 has no θ. Theorem conditions not met: LTI SISO (the loop is adaptive and multi-person); 30 Hz is the face loop, not the body loop. Ω_a is labelled a constraint ✓. |
| Valence (RR:55) | Gap | The ISS-Lyapunov V is non-unique (α∘V is one too), so magnitudes are arbitrary. A standard adaptive V contains (ĉ_p − c_p)², with unknown c_p, so the agent cannot compute it. The "need part" −d/dt Σd(b) is a different quantity: Σd is not a Lyapunov function once integral and adaptive states are present. The zero-average guarantee is correct, but it holds for any bounded state function and only asymptotically. |
| Arousal (RR:56) | Internal tension | ∂u/∂e = −K∇²d. With d = \|e\|^q, the gain rises with deficit iff q > 2, and then the loop gain at the set point is 0. The linear analyses (P1, P2 "1/a", P4, CT1–CT4 with k_p = 1) assume a nonzero gain there. With q = 2, arousal is constant. |
| Curiosity (RR:74) | Assembly | Curiosity uses the D62 argmax over channels with one scalar LP drive (sim_lp.py:17-21), not u = −K∇d − …. RR:29 says "per topic". Rerun: 3.26% noisy TV and 3.60% dark room, matching. It is imported and unlabelled. |
| Replay (RR:81-82) | Heuristic | Persistence of excitation is a convergence condition, not a selection rule. CT8 regresses the disturbance d directly (sim_ct8:8-12). The core never observes d, only e in closed loop. |
| Attention rule (RR:96-98) | Heuristic, not derived | L_p ∝ ĉ_p·pev_p (sim_ct7:13) is a product of two magnitudes, and the current need e does not enter. The cue mask has no toy. |
| Claude reappraisal (RR:75) | Prose only | "Words enter y as context" is not defined for an AU/prosody observer. No toy. |
| Perception (RR:83-88) | Stated, thin | It presupposes y_p already in the agent's AU coordinates, so the front end is outside the theory. The coarse, dynamic and body routes are mapped by assertion. |

**One problem or an assembly?** An assembly. Homeostasis and an error-driven internal model follow from the problem. Nothing else does.
- **Labelled constraints:** K1 (RR:19, 49, 113), Ω_a (RR:73), the saturation \|ν\| ≤ U (RR:79).
- **Unlabelled additions:**
  - Γ and its rank;
  - perceptual feedforward ξ_p;
  - per-person identity (an oracle in every toy);
  - the relevance law;
  - the temperament law;
  - the leaks ε_m, σ, σ_θ;
  - R_θ;
  - the Kalman observer;
  - the LP body variable;
  - the attention rule;
  - the replay selection;
  - the contact sensor.

## Sims rerun

All eight scripts were rerun with `uv run python`. **Every out/*.json is byte-identical** to its rerun. make_figures.py was run in a /tmp copy: **all four PNGs are byte-identical**. RS reports every number correctly. Notes:
- Figures exist for 4 of 8 toys; there are none for CT1, CT3, CT7 or CT8. The ct4_people.png title is clipped ("when sh…").
- **CT6-2 robustness:** the random arm was rerun with 8 other seed offsets. p ranged from 0.09 to 0.93, so the pass is robust. The near-miss in the original (p = 0.056) comes from the mean u·d per level drifting −0.07 → −0.09, which moves the mean ĉ from 0.529 to 0.464.
- **CT7 lock-in test:**
  - c_A = c_B = 0.4 with innate ĉ 0.5/0.05: share 0.53, and ĉ_B recovers to 0.51.
  - c_B = 0.8, c_A = 0.1 with innate ĉ favouring A: share A 0.26, ĉ_B 0.91.
  - There is no rich-get-richer entrenchment.
- **ĉ is biased:** CT1 gives ĉ 0.54 for c = 0.5. CT7 gives ĉ_B 0.16–0.20 for c = 0.1 and ĉ_A 0.92–1.04 for c = 0.8. The ordering is kept, but RS:12 "tracks relevance" holds only loosely.

## Spec-vs-code

- **CT2b** (PR:40): "only the thinking budget varies" was implemented as a random rank-1 *mixture* (sim_ct2:19). That is why "others ≤ 0.05" failed. RS:26 calls the prediction "wrong in kind". Equally, the test chose a mixture.
- **CT5(b)** (PR:82): the code matches, but with gain on the face only and no model path from f to s, x[0] stays exactly 0 (sim_ct5:15-16; the measured max of \|x₀\| is 0.0). So R² = −mean²/var ≤ 0 by construction.
- **CT6** (PR:94): "ŷ its reconstruction". The code uses the true partner signal p (sim_ct6:12). The "8-dim direction" (sim_ct6:13, 19) acts on a toy with one causal dimension and no regulator or adaptation: ĉ is set directly.
- **CT7:** the noise σ = 0.3 and the observer form are not in PR. The observer is the deterministic synchronization form that RR:66 says cannot read people.
- **CT8:** an open-loop LS target d (see the Replay row). The number of informative episodes is binomial, not a fixed 20%.
- CT1, CT3 and CT4 match their specs.

## Labels

Every numeric verdict matches its threshold. Two need correction:
- **CT2b** should read "refuted (rank-3 clause confirmed; rank-1 clause failed)" (RS:23). A conjunction fails if any clause fails.
- **CT5** "All three confirmed" (RS:58) stands numerically, but CT5-2 and CT5-3 are by construction, and the inference at RR:66 is wrong. The fixed-gain observer gives 0.948.

**By construction but unlabelled:**
- **CT1-4:** at c = 0 the system is homogeneous, and its only equilibrium is 0.
- **CT2a:** the linear stability threshold.
- **CT3-1:** a theorem check.
- **CT3-2:** the controllers were chosen to produce it.
- **CT5-2:** see above.
- **CT5-3:** a sign flip gives 1 − 4 = −3.
- **CT6-1:** it follows from a = κĉp + o.

CT1-3 is labelled ✓. CT8's ratio is predictable analytically: √(energy ratio) ≈ 0.45.

RR:121 says "beyond surrogates", but no CT toy ran surrogates.

## Expressive structure and standard

1. **Content-dependent attention: not met.** CT7 is magnitude-only and not need-conditioned. No toy selects memories or actions.
2. **Structure over people: partly met.** It is a dictionary keyed by oracle identity, not a field over a learned space. There is no structure over relationships, episodes, topics or time.
3. **Dimensionality and ablation: partly met.** CT4 compares 3 scalar gains with 1 scalar gain. The effective dimensionality (RR:99) is stated, not measured.
4. **Richness from structure: not met.** No toy shares F_θ or G across people. Every toy is a scalar linear system: the brief's own description of a sketch (brief.md:49).

**Per-candidate list** (brief.md:71-79):
- **Deep-learning realization and data needs: missing.**
- **Toys missing for:**
  - the leaky mood;
  - valence and arousal;
  - θ;
  - the saturated interface;
  - reappraisal;
  - emotion types;
  - curiosity inside this controller.
- **Propositions without proof:** ISS of the full loop, satiability, scaling invariance of valence.
- **Stage predictions** do not follow evaluation.md:157-180:
  - no surrogates for S1-a;
  - no sham lesion or severity sweep for S1-c;
  - no named unrelated behavior with a tolerance for S1-b.
- **Sources:** F&W 1976 and JTP 1994 were not read in the original, and Sterling only as an abstract. These are disclosed.

## Principles

- **2:** passes. m is an integral state, not an emotion label.
- **4:** passes on the settings path. The words-into-y path is undefined.
- **6:** ĉ_p creates **no seeking gradient**. It enters only cancellation, face gain, observer gain and Γ, and the lock-in test is negative. Residual risks:
  - The **"contact per person" sensor is undefined** (RR:29). If it is gaze, attention or time present, the drive is a satiable demand for the user's attention, which Principle 6 bars.
  - Γ(ĉ_p) biases Claude's retrieval and cue mask toward high-ĉ people, with no constraint on what Claude does with that.
- **10:** fails. See "One problem or an assembly?".
- STATUS.md:23 still says "forced per-person internal models" and lists items as owed that RR now has.

## Complete?

**No.**

## Fixes (priority order)

1. Drop "forced" (RR:16, 21, 63) or state a problem that forces it. One candidate: identity-indexed switching disturbances, with a proposition that error-driven models cannot match perceptual feedforward there. Otherwise label ξ_p, ĉ_p and per-person indexing as constraints.
2. Rewrite the CT5 inference. The requirement is observer gain on the slow state; stochasticity is not required. Relabel CT5-2 and CT5-3.
3. Fix the mimicry sign: use \|ĉ_p\| in K1 (labelled), or concede the sign ambiguity.
4. Add the deep-learning realization and data section.
5. Toys for expressive items 1 and 4: need-conditioned, content-dependent selection over cues, memories and actions; a learned person space; a shared F_θ/G across people that beats independent models on little data.
6. Make valence computable and unique; resolve arousal against q; simulate the leaky mood and the saturated interface (including words into y); prove ISS; drop P4 or re-ground it at a time scale where it binds.
7. Bring S1-a, S1-b and S1-c to the evaluation.md protocol.
8. Label every unlabelled addition as K2…Kn; define the contact sensor.
9. Correct the CT2b label; flag the by-construction results; add figures for CT1, CT3, CT7 and CT8; fix the clipped CT4 title.
