# Critique: Modulated manifolds (design-modulated-manifolds.md)

Independent critic, 2026-11-25T16:16:59Z. Written under questions.md Q16 and Q17, and judged against the refined rule (Q18 answer, DECISIONS.md D78). I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

## Summary verdict

- **Proofs.** 44 items checked: **26 valid, 7 with a gap, 11 with an error.** The one-dimensional staircase mathematics (Lemma S(a)–(c), (e)), Theorem M, Theorem L as a conditional statement, Lemma R, the satiety statements and the instrumental-variable identity (T5) are correct. The errors sit in the claims built on top of them: the rank bound, level-blindness, and the claim that the agent's own drive caps how far a partner can move it.
- **The worst error.** The rank decomposition in §3.4 leaves out events that the partner's change sets off *through the content layer*: surprise and turn-end events (E2), appraisal events (E3) and own-utterance appraisals (E5). The design itself uses these for every context-dependent and sign-flipped response, 1–3 s after the partner's change (P6, P7), which is inside the window W = [0.3, 4] s. Once they are counted, one family can contribute more than two directions per event. The bound rank H ≤ 11 then fails. So do T1's consequences 1–3 and the "empty copy set" in T1b(i). In the reachable parameter set Θ, a whole-face copy on all 12 perceived synergy dimensions exists, with defect about 0.05 or less (counterexample C1).
- **Two further errors on central claims.**
  - **Held partner levels do have sustained effects** (Corollary L1 and T1b(ii) are false). A content head learns a weight on the partner's smile level, and its E3 threshold then becomes a learned threshold on that level. Four families give a four-level thermometer code of the partner's held smile, and the code is held by the manifolds (C2).
  - **Repeated events integrate, and the agent's drive does not set the ceiling** (Lemma S(d) and T1b(v)(a) are false). The refractory period (0.3 s) is far shorter than the return transient (T₊ ≥ 5.5 s). So a train of same-type events climbs the staircase whether or not the steps exist. In my numerical check with *no manifold at all* (μ = 0.7, k_max = 0), one event every 2 s held the position at step 13 of 16. At μ = 0.9 (k_max = 2), one event every 4 s held it at the top step, 16 (C3). "The partner cannot push harder to push further" is false: the partner pushes further by pushing more often.
- **The dial (D78).**
  - On the direct event path there is no scalar whole-face dial, and every magnitude on the partner path has an innate ceiling. That is genuine, and better than any earlier design in this project.
  - But the design fails D78 as proved, for three reasons.
    1. The relationship key Q9 is a single quantity whose values run from flat (the stranger prior, a ≡ 0) to a copy of a large shared subspace. The design's own bound is defect 0.29 on the 12-dimensional perceived face, which means 11 of 12 synergies copied. With C1 the bound drops to about 0. Under D78 this is "a quantity that runs ... a large shared subspace from flat to copy". Nothing in the design shows that this configuration does not attract under learning.
    2. A single family's position opens or closes the phasic copy on smile, brow-lowering and brow-raising at once. These are the three channels that carry nearly all the mimicry evidence. The phasic strength cannot flip sign on its own route.
    3. The partner's event rate acts as a continuous intensity dial on each family's position (C3).
- **Principles.**
  - No Principle 1 violation.
  - Principle 2 is borderline. "Aversive load" and "arousal load" are a valence gauge and an arousal gauge installed as body variables, and arousal is read out as b_arousal. The innate cry-face prior and the laugh and cry generators are hand-wired emotional displays. They are defensible as reflexes, but they should be declared as such.
  - Principle 3 is real for perception (analysis by synthesis through the agent's own synergies). The "inference of the other's state" (n̂^p) is a thin, ill-posed feature.
  - Principle 6 holds for satiability. It has a residual reward for the partner's presence on the boredom side of the information drive.
  - Claude coupling is text-free. The claim that the user's state is masked from it is false, because the content state c carries partner history.
  - Expressive structure: the affective core is four quantised one-dimensional gauges, each with a 6-way circuit selector. Read strictly, that is close to the "few scalar gauges" sketch the brief rejects. The 10⁸ figure counts configurations; it is not a dimensionality.
- **Novelty.** The author's verdict, **recombination**, is confirmed, and the basis is weaker than claimed.
  - The staircase is not Koulakov et al.'s *robust* integrator. Koulakov's robustness comes from hysteretic (individually bistable) units. The design's Φ is single-valued, so all 16 steps need μ within 1.6% of 1 (μ > 0.984). That is the classic tuning problem, and the design uses it as its "existence" control.
  - Theorem M's invariance (the immediate response does not depend on the persistence parameter) also holds for an ordinary leaky integrator driven by impulses, so it does not separate the design from existing mechanisms.
  - The core reduces to a per-family, event-driven, leaky up/down counter whose leak is set by drive, with a categorical readout: a gated switched linear system with quantised input.

## Sources read for this critique

| Source | How read |
|---|---|
| research/foundations/design-modulated-manifolds.md | in full, 1107 lines |
| brief.md | in full |
| questions.md Q16, Q17, Q18 (with the operator's answer); DECISIONS.md D78 | in full |
| research/foundations/known-failures.md; research/mimicry-context-synthesis.md | known-failures in full; the synthesis §§1–3 and the open questions |
| research/foundations/critique-design-dyadic-sheaf.md | summary and §1, for format |
| Koulakov, Raghavachari, Kepecs & Lisman 2002 (Nat Neurosci 5:775) | **abstract-level only**, via a web search, to confirm that the robustness comes from bistable hysteretic units and that earlier integrators needed better than 1% tuning. Full text not read |

**Numerical checks.** These are a short Python script in my scratchpad, not in the repository. They check the design's own equations (N = 16, Nε = ¼, τ_s = 8 s) and are not evidence about behaviour.
- Counts of stable states: they reproduce the design's 1, 1, 1, 2, 2, 3, 5, 13, 17.
- Kramers hold times: they reproduce 1.4·10³ s, 1.2·10⁴ s, 1.1·10³ s and 1.5·10⁵ s.
- Event-train runs: they give the C3 numbers.

---

## 1. Item-by-item check

### Lemma S(a), equilibria: valid
- On plateau i, V′ = ρ − μi/N, and its zero lies on the plateau iff i(1 − μ) < c.
- The ramp endpoint values are ((i − 1)(1 − μ) + c)/N > 0 and (i(1 − μ) − c)/N. Both are correct.
- The left endpoint is always positive, so there is exactly one unstable zero per ramp k ≤ k_max.
- The condition is downward-closed. Every step checks.

### Lemma S(b), cascade of folds: valid, with a wording note
- Births occur at μ_k = 1 − c/k: 0.75, 0.875, 0.917, …, 0.984. They are bottom-up, and the global-attraction argument for μ < μ₁ is right. So "a cascade of saddle-nodes" is correct as a count of births.
- These are **non-smooth folds**. V is C¹ but V″ jumps at the ramp–plateau junction, and the pair is born at the kink. There is no quadratic normal form. Consequently the slowing near the fold is logarithmic (the T₊ formula), not the inverse-square-root passage time of a smooth saddle-node.
- Calling it "critical slowing" is fine. Citing smooth saddle-node scaling would not be.

### Lemma S(c), one-step kicks from an equilibrium: valid as stated
- Both landing-plateau inequalities reduce to the stability condition k(1 − μ) < c, as claimed.
- The return-time formula is the exit time from plateau k + 1. Since the readout round(NΦ) switches at the ramp midpoint, it is correctly a lower bound.
- At μ = 0 the duration τ_s ln 2 is exact.
- **The hypothesis matters: the kick arrives at a stable equilibrium.** The design's refractory period T_r = 0.3 s is 18 to 100 times shorter than T₊, so later events usually arrive mid-transient. See S(d).

### Lemma S(d), "finite manifold, ceiling set by the agent": error
- "After the transients" is never reached under a sustained event train, because each event restarts the transient before it ends.
- Below the first fold, V′ is roughly (1 − μ)ρ on average, so the position is a leaky integrator of events with time constant about τ_s/(1 − μ). That is 24 s at μ = 0.67, and it grows without bound toward μ₁.
- Counterexample C3 (§2). The reachable index depends on the partner's event rate, not on μ.
- The statement is true only for isolated events (inter-event interval greater than T₊).

### Lemma S(e), barriers and hold times: valid
- The plateau area δ_k²/2 and the ramp triangle εδ_k²/(L_k + δ_k) are right, and L_k + δ_k = (2c − x)/N.
- The monotonicity derivative is right: (1 − 2k)/c < 0.
- The upward barrier is always larger (the plateau part is ((kx + c)/N)²/2 against (c − kx)²/(2N²)), so using the downward barrier is justified.
- The Kramers prefactor 2πτ_s/√|1 − 2μ| matches the overdamped formula with V″ = 1 in the well and 1 − 2μ on the ramp.
- At μ = 1 the saddle region √(T/|V″|) ≈ 0.0055 fits inside the linear zone (ε ≈ 0.0156), but only barely.

### Hold-time table: valid
Reproduced to the stated digits.

### Theorem M, existence is not gain: valid, but not distinguishing
- (i) follows from the immediate-index part of S(c). (ii) follows from S(c). (iii) holds because τ reads g_f, a and ω, never μ.
- Note that τ and μ are both functions of the same d_f history, so they are confounded, though not causally linked.
- **The §4 use of M is wrong.** For the linear integrator ẋ = −εx + s·Σδ(t − t_e), the jump at the event is s, whatever ε is. So ∂H(0⁺)/∂ε = 0 holds there too.
- §4 compares this immediate response with the linear integrator's DC gain, which is a different quantity. The window-averaged H_W depends on μ in the design, just as it depends on ε in the linear integrator.

### Theorem L, level-blindness given identical event records: valid as a conditional statement
The edge enumeration is complete. Its hypothesis, however, includes identical E2, E3 and E5 records, and those are learned functions of partner levels through c (below).

### Corollary L1, in-band variation has no effect: error
- The corollary assumes that variation inside every E1 hysteresis band leaves the event record unchanged. It does not, for three reasons.
  1. c reads P(y), p̃, g and h at every frame. The heads read c. E3 fires when Δ̂d_f^{ext} crosses ±θ, and E2 surprise and turn-end fire on head outputs. So in-band level changes alter E2 and E3.
  2. The need-conditioned thresholds θ_{j,f}^on(z) = θ^{on,0}(1 − α·g_f·|a|) move with the agent's own drive. A partner holding a level between 0.7θ^{on,0} and θ^{on,0} produces an up-crossing when the agent's need rises, and a partner holding a lower level does not.
  3. The phasic trigger fires on up-crossings of I_k = P_k + ζ[S_k]₊. An own step that raises S_k makes I_k cross θ^A iff the partner's held P_k is high enough. So whether the agent's own step produces a phasic burst depends on the partner's held level.
- Counterexample C2 (§2).
- The design's own §2.6 also gives every event an amplitude mark q, and ω(q) decides whether |κ| ≥ κ*. That contradicts §1's "a big smile and a small smile that cross the same threshold are the same event".

### Lemma R, Eckart–Young bound: valid
(a) and (b) are correct.

### §3.4 decomposition and rank H^𝒮 ≤ 11: error
- **What is valid.** For effects carried *only* by the extra event's direct type, family f's column depends on τ_{f,j} ∈ {−1, 0, +1} alone. So it takes at most two nonzero values per family, even when later events, refractory blocking and mode re-selection are included. That part of the argument survives.
- **What is missing.** The definition of H (one extra partner change, all downstream effects) also includes:
  - content-mediated E2 events (surprise is almost certain after an onset);
  - E3 appraisal events, which the design's own P6 places at 1–3 s, inside W;
  - E5 appraisals.
  These depend on j through learned heads. A direct +1 followed by an appraisal +1 gives the vector E(n + 2) − E(n), which lies outside span{v_f⁺, v_f⁻}.
- **The correct bound.** Per family, the rank is up to 2m, where m is the number of steps the change can trigger within W. With the refractory period, m can be as large as 12. So rank H^𝒮 ≤ 12 holds only trivially, because there are 12 synergies.
- Counterexample C1.

### Theorem 1, step by step
1. **Completeness: gap.** It routes everything through events, which is right, but it asserts that each event's effect is H^φ + H^τ. That inherits the omission above.
2. **Rank per quantity: error.** Q1–Q5 each gain content-mediated directions. Q9's rank of 11 is not an upper bound.
3. **Ceilings: valid.** These are robust even after C1 and C3: S ∈ [−0.8, 1], Ā is innate, a difference of two library postures is at most 2a_max per synergy, and no learned magnitude multiplies an output. This is the design's strongest result.
4. **Sign: valid,** given the stated library condition. The phasic route itself is never negative; only the channel's net sign can flip.
5. **"The partner's current expression cannot set any of them except by being an event": error.** Learned heads on c make the partner's held level set E3 events, and so positions (C2). The phrase "an event is the response itself" hides a learned level quantiser.
6. **Corollary (0.74 and 0.29): error.**
   - **The 0.74 is vacuous.** H = W_syn·H^𝒮 has rank at most 12 for *any* design with 12 synergies, and an isotropic rank-24 U cannot be perceived: by T4(b) the agent sees only range(G), which is 12-dimensional. The 0.74 measures the agent's small face, not the absence of a dial.
   - **The 0.29 does not survive C1.** It also assumes an isotropic U. Real partner expression is strongly anisotropic, with smile and brow movements dominating, so even a rank-5 quantity has a small tail on realistic U.

### Theorem 1b
- **(i) Copy set empty: error.** It inherits the rank error. C1 is a nonempty copy set in Θ.
- **(ii) No sustained-level copy: error.** C2.
- **(iii) No amplification per event: valid.** It is false per unit time (C3), which (iii) does not claim but §1 and §4 do.
- **(iv) Learning fixed point independent of the agent's own following F: gap.**
  - (a) is correct under (A1)–(A2), and the author already flags (A2).
  - (b) is not correct even then. E is chosen per (mode, step) by J, evaluated at decision points sampled from the agent's own experience. The conditional distribution of content states given (mode, step) depends on F, so the argmin over postures does too.
  - (A1) is fitted only in solo and gaze-off periods. Social facial feedback may differ from solo facial feedback.
  - The guard removes the *self*-reinforcement loop of the sheaf critique's C13. It says nothing about a *partner*-driven gradient toward matching postures: people respond to being mimicked, and that response enters through R̂.
- **(v) State-level non-absorption: error.**
  - (a) fails under event trains (C3).
  - (c) is weaker than stated. After satiety the gate closes at once, but m^ton decays with τ_T = 36 h, and μ stays above μ₁ until m_fast + m_ton < ½. That is up to about 25 h for a chronically driven family. The configuration last reached is held for that long. It is not copying (H = 0 with the gate closed), but it is "settling".
  - (b), anti-coincidence, is valid.

### Theorem 2, satiable drives
- (a)–(d): **valid.**
- **(e) Zero map at full rest: gap.** The startle catch and the laugh and cry generators are pattern generators triggered by events, and their conditions at rest are not stated. A partner's loud onset produces a startle at rest and also raises b_arousal, which takes the agent out of rest. The theorem should say H ≡ 0 on the expressive (E1) columns only.
- **(f) No reward for the user's smiles, attention or time: gap.**
  - When the agent is bored, surprise events lower the information drive.
  - An engaged, present partner is the main source of surprise.
  - So J does decrease with partner presence and engagement on the under side. This goes beyond the provocation route the author lists.
  - It is satiable, but the sentence "no term of J decreases with ... session length" is not true.

### Theorem 3, time scales
- **(a): error (minor).**
  - "Strictly decreasing in k" fails at μ = 1, where ΔV_k↓ = c²(½ + Nε/2c)/N² for every k. The table itself shows 1.5·10⁵ s in every column.
  - The lower end of the span is not τ_s. Near μ_k the Kramers form is invalid, and the prefactor alone is about 70 s.
- **(b): valid.**
- **(c) "temperament set by ... β": error.** All modes share one V_μ, N, ε and τ_s, and μ depends on d_f only. So β, which chooses among modes, has no path to T_hold(1, μ̄). Temperament as defined is a function of the drive history, which the environment sets, not the agent.
- **"Persistence without tuning any eigenvalue."** Hold times are exp(ΔV/T), so the elasticity with respect to the innate T is −ΔV/T = −8. That is sharper than a linear integrator's elasticity of 1 with respect to its eigenvalue gap. The tuning has moved into T; it has not gone away.

### Theorem 4, reading through one's own body
- **(a): valid** (trivial for the affine F_self). It needs ΩG to have full column rank, which requires Ω to be positive on enough rows.
- **(b): valid** (Pythagoras on range(ΩG)).
- **(c) "No free perceptual gain": gap (vacuous).**
  - A perceptual gain λ is equivalent to thresholds θ/λ.
  - The design's own need-conditioned lowering, up to α = 0.3, *is* a state-dependent perceptual gain of up to 1/0.7 ≈ 1.43 per family and type, chosen by learned |a|.
  - The cap is innate, so it is acceptable under D78. But (c) does not show that no gain exists.
- **(d): valid,** conditional on Theorem L.
- **(e): gap.** n̂_f^p = argmax_n p(P(y) | E_{r_f}(n)) is ill-posed. E is learned for drive reduction, not invertibility; E(0) = 0, and several steps typically share a posture, so the argmax has ties. It is also computed on the circuit the partner's own key selected. "Inverting one's own generative model" here is a feature fed to c, not an inference that any part of the state uses.

### Theorem 5, instrumental-variable identity: valid
- S_AB = (I − FR)⁻¹S_BB, and S_PB = R·S_AB. The proof checks.
- It needs only the partner's equation to be linear and E ⊥ B. The agent's side may be nonlinear, which is a strength the author does not claim.
- The practical first stage is very weak. Babble at 1/60 s⁻¹ per synergy, gaze-gated, gives about 10 instruments per synergy in a 10-minute session.

### Propositions on the human pattern
- **P6: valid** as a derivation of timing.
- **P7: valid** (constructive).
- **P8: valid.** m^fast reaches ½ in about 3.5 min at ψ = 1.
- **P9: valid** but trivial (columnwise proportionality).
- **P10: valid** by construction.

### §4, why existing mechanisms cannot do it
- **The common lemma: valid.**
- **The table: gap.**
  - The continuous-attractor row claims that ∂H(0⁺)/∂μ = 0 separates the design. It does not (see Theorem M).
  - It also claims that the DC transfer from a held level is 0. That is false (C2).
  - The table omits the closest mechanism: an event-driven, bounded, leaky up/down counter.

### Count

| Status | Items |
|---|---|
| **valid (26)** | S(a), S(b), S(c), S(e), hold-time table, M, L, R, T1-3, T1-4, T1b(iii), T2(a)–(d) (4), T3(b), T4(a), T4(b), T4(d), T5, P6–P10 (5), §4 lemma |
| **gap (7)** | T1-1, T1b(iv), T2(e), T2(f), T4(c), T4(e), §4 table |
| **error (11)** | S(d), L1, §3.4 rank decomposition, T1-2, T1-5, T1-6, T1b(i), T1b(ii), T1b(v), T3(a), T3(c) |

Inconsistencies that are not counted:
- n_f is defined as N·Φ in §2.2 and as round(N·Φ) in §2.7.
- 𝔏 has "24 postures including 0" in §2.1, but §6.3 evaluates "all 25 posture options".
- β names both the temperament prior and the Claude selection strength.

---

## 2. Counterexamples

### C1: a full-face copy in Θ (refutes rank ≤ 11, T1 consequences 1–3, T1b(i))

**Operating point and parameters.**
- All μ_f = 1, so every step exists.
- Families 1–3 sit at step n = 2 in their active modes.
- Choose E_r(n) = 0 and E_r(n + 1) = a_max e_{k1}, E_r(n + 2) = a_max e_{k2}, E_r(n − 1) = a_max e_{k3}, E_r(n − 2) = a_max e_{k4}. Use distinct synergies across families, so 3 × 4 = 12 synergies in all.
  - This needs single-synergy postures in 𝔏. Twelve positive ones exist in a library of ±a_max e_i, which also satisfies T1(4)'s sign condition.
  - E is an arbitrary categorical map, so this choice is reachable.
- Learned types a: onset of k1 → +1 in family 1, and onset of k3 → −1. For onsets of k2 and k4, add a content head whose E3 event for family 1 fires 0.3 s after that onset. Give the E3 type the same sign as the direct one: +1 then +1 for k2, −1 then −1 for k4. Heads and a are arbitrary in Θ.

**The result.**
- Over W = [0.3, 4] s, column k1 is a_max e_{k1}, column k2 is a_max e_{k2}, and so on.
- The phasic route adds a nonnegative diagonal on the 3 S_φ channels, which is also copy-shaped.
- So H^𝒮 is close to c·I₁₂, with a residual only from a second step landing later than 0.3 s. A delay of 0.2 s gives a defect of about 0.05.
- Rank 12, defect ≈ 0, on the agent's whole perceived face.

**What this does and does not show.** C1 shows that the set is nonempty, so the emptiness proof fails. It does not show that learning goes there; the content heads are trained to predict drive, not to produce copies. The design's guard against copy is therefore only T1b(iv) and (v), and both have gaps.

### C2: held partner levels have sustained effects (refutes L1 and T1b(ii))

**The setup.**
- Give each family's E3 head the form Δ̂d_f^{ext} = w_f(P_smile(y) − m_f) + (other terms). This is a learned linear head on c, which carries P(y).
- The up event fires when P_smile rises through m_f + θ/w_f. The down event fires when it falls through m_f − θ/w_f.
- Let all four families' active modes step +1 on their own E3-up and −1 on E3-down, with postures that add +a_max on smile.
- Place the learned crossing points at 0.30, 0.40, 0.50 and 0.60, all inside the E1 smile hysteresis band (no E1 events), and set μ_f near 1.

**The result.**
- A partner who slowly raises the smile to 0.45 and holds it leaves the agent holding +2a_max of smile.
- A partner who holds 0.65 leaves +4a_max. A partner who holds 0.25 leaves none.
- The positions are held for hours (T_hold ≈ 1.5·10⁵ s at μ = 1), and they come down when the partner's level comes down.
- This is a hysteretic four-level copy of the partner's sustained smile level, with gain about 4a_max/0.3 ≈ 3 over the band.
- It lies on one synergy, so it is a per-channel strength in D78's sense, with an innate ceiling. But it is exactly the "sustained-level path" that §1, L1, T1b(ii), §4 and known-failures row 1's "copy" concern say does not exist.

**Two simpler variants.**
- Need-conditioned thresholds: the partner holds AU12 at 0.8θ^{on}, and the agent's need rises, so the family's threshold drops to 0.7θ^{on} and an onset event fires with no partner change.
- Phasic trigger: an own step raises ζS_k from 0.03 to 0.06, and a phasic burst fires iff the partner's held P_k > 0.09.

### C3: event trains climb a staircase that does not exist (refutes S(d), T1b(v)(a), §1 "cannot push harder")

The design's own flow, Euler-integrated, with one +1/N event every Δ seconds and the index averaged over the last 40 s:

| μ (k_max) | Δ = 4 s | Δ = 2 s | Δ = 1 s |
|---|---|---|---|
| 0.0 (0) | mean n = 2.0 | 4.0 | 8.0 |
| 0.6 (0) | 5.0 | 10.0 | 15.6 |
| 0.7 (0) | 6.7 | 13.3 | 15.9 |
| 0.9 (2) | 15.7 | 16.0 | 16.0 |

**Why it matters.**
- With no manifold at all, a partner producing one counted event every 2 s holds the agent at step 13 of 16. Partner events at about 0.5 Hz are ordinary in conversation: onsets, offsets, gaze, voice onsets and back-channel cues. They count for a family whenever |g_f·a| ≥ κ*.
- So the posture the agent shows is E(n) with n set by the partner's event rate. Across 16 steps that can be 16 different library postures, far from "one step per family".
- The innate ceiling still holds: S ≤ 1.
- But "existence and length set by the agent's own drive" is false while the train lasts. The persistence and existence story (Theorem M, Vinograd's "decay intrinsic") holds only once the train stops.

### C4: the relationship key under D78 (the author's weak point 1)

**What Q9 can do.**
- Q9 is discrete, but it is a single quantity. Its stranger value is flat: ℓ⁰ selects modes that start with a ≡ 0, and E_r(0) = 0 gives S = s⁰, so the phasic gates are closed too.
- Its operator value can be the C1 configuration, or the design's own rank-11 configuration.
- So switching the key runs 11 of 12 (by the design's count) or 12 of 12 (by C1) perceived synergies from flat to copy.

**Why this fails D78 as the theorem stands.** D78's first disqualifier is "a quantity that runs the whole face (or a large shared subspace) from flat to copy". A defect of 0.29 means a single missing synergy. That cannot be called "not copy", and with a realistic, anisotropic partner U the missing synergy carries even less weight.

**The design's defences, and why they do not settle it.**
- **The per-family modes are learned separately.** True. But D78 asks for strengths set *per expression*, while one mode choice sets the types for all 56 event types of its family at once. The relationship's per-expression control is therefore a choice among R_f = 6 joint patterns per family.
- **Learning goes there only if every family's data support matching.** That is not proved, and T1b(iv)(b) has a gap. A partner who rewards being mimicked creates exactly that support through R̂ in E's learning.

**What would settle it.** A constraint that holds for every key. Fix 4 in §4 gives one.

---

## 3. Dial hunt under D78

| Quantity | Whole face or large shared subspace, flat to copy? | Per-expression | Sign-flippable | Innate ceiling | Copy non-attracting under own learning |
|---|---|---|---|---|---|
| Q9 relationship key | **Yes, in Θ** (C4): 11–12 of 12 perceived synergies | no: 6 joint patterns per family | yes | yes | not shown |
| Q4 active mode (one family) | 2 tonic directions + 3 phasic channels, or more by C1 | no: one choice sets all event types of the family | yes | yes | not shown |
| Q3 position (one family) | **opens or closes the phasic copy on smile, brow↓ and brow↑ together** (one posture can raise all three S_k above θ^c) | no | the phasic part is ≥ 0; the net sign is tonic | Ā innate | partly: anti-coincidence (valid) |
| Partner event rate (input side) | intensity of each family's position, continuous (C3) | per family | via E | S ≤ 1 | not addressed |
| E3 head weight w_f (learned) | a learned level threshold per family (C2); 4 families give a thermometer code | per family, not per expression | yes | yes | not addressed |
| Need threshold lowering α·g_f·\|a\| | a perceptual gain of up to 1.43 per (family, type) | yes | — | α = 0.3, innate | yes |
| Modulators μ_f | persistence only; immediate response unchanged (M) | per family | — | U ≤ 1 | yes |
| Deliberate shunt σ^del | can only shrink affective synergies (not phasic) | per synergy | no | 1 | yes |
| Innate constants (θ^on, E3 θ, T, Ā, a_max) | not varied, so not dials; but a shared E3 θ would run every appraisal-mediated response at once if it were ever made adaptive (element 7 "precision" is a fixed constant here, which is itself a gap for element 7) | — | — | — | — |

**Verdict.**
- There is no scalar whole-face dial on the direct path, and every per-channel strength has an innate ceiling. Those are real gains over all previous designs.
- But the design fails D78 as proved. Q9 runs a large shared subspace from flat to copy in Θ with no proof that the configuration does not attract. The 3-channel phasic gate is shared, and its strength never flips sign on its own route. Two unnamed quantities (event rate; learned E3 level thresholds) are missing from the design's Q-table.

---

## 4. Principles and the brief's expressive-structure items

- **Principle 1: met.** Inputs are blendshapes and prosody; there is no classifier.
- **Principle 2: borderline.**
  - Energy and information are neutral body variables.
  - "Arousal load" is an arousal gauge installed as a body variable, and §5.2 reads arousal out as b_arousal. That is closer to "set" than "read out".
  - "Aversive load" is a valence gauge whose afferents are hand-chosen social appraisals ("being talked over"). The brief allows innate body variables, but this one carries negative valence by construction.
  - The innate cry-face prior and the laugh and cry generators are named emotional displays. They are acceptable as infant reflexes only if declared as such.
  - The synergies (smile, cry-face) are expression units, not emotion variables, so they are acceptable.
  - The four families are not emotion names. The posture library is not labelled by emotion.
- **Principle 3: partly real.**
  - Perception through the agent's own body is genuine: P is the left inverse of the agent's own face, and the voice is mapped into its own source-filter settings.
  - "Perceived features drive own motor and affect pathways": yes, through events and the phasic route.
  - "Infer the other's state by inverting own generative mapping": only n̂^p, which is ill-posed and unused except as a content input (T4(e)).
- **Principle 4: text-free coupling (selection, context, effort), met.** The claim ∂r/∂(partner features) = 0 is false if c is the running SSM state, which integrates partner inputs with poles up to 5 s. Masking the *inputs* at scoring time does not remove the *state*. E5's types are likewise functions of partner history.
- **Principle 6: satiable (T2), met.** The boredom side rewards partner presence and engagement (T2(f) gap), and the provocation route remains.
- **Principle 10: partly met.** One objective plus one predictive constraint, as in earlier designs. Many large structures are declared constraints rather than derived (the four families, S_φ, 𝔏, the event list). The author lists this honestly.
- **Expressive structure: close to a sketch.**
  - **Effective dimensionality.** The affective core is 4 quantised positions on one-dimensional staircases, 4 existence scalars and 4 categorical selectors (6-way). That is about 12 coordinates, 8 of them discrete. 102⁴ ≈ 10⁸ is a count of configurations, not a dimensionality.
  - **Content-dependent selection.** "Need-conditioned attention" is a threshold lowering of at most 30% per (family, type). That is selection by magnitude, not by content.
  - **Structure over people.** It is a key-to-24-number lookup, with nothing over topics or episodes beyond replay tags.
  - **What rescues it.** The categorical, non-monotone readout E and the mode switching give it more than linear maps. P9 is a valid low-dimensional-ablation argument, but a weak one. On balance it sits at the boundary the brief draws.

---

## 5. Reduction and novelty

**What the core reduces to.**
- **Per family, for fixed μ ≥ μ₁:** a bounded up/down counter whose states have noise-escape lifetimes. That is a multistable discrete-attractor chain, or quantised line attractor.
- **Per family, for μ < μ₁:** a leaky integrator of event counts with τ ≈ τ_s/(1 − μ) (C3).
- **The modulator:** the detuning parameter of a recurrent loop, i.e. how close the feedback gain is to 1.
- **Overall:** a switched linear system with quantised, thresholded input and a categorical readout. That is a member of the rSLDS / gated-SSM class, as the author says.
- **Each piece is known:**
  - the input quantisation is level-crossing sampling;
  - the phasic units are innate, gated reflex generators;
  - "modulator configures which circuit" is mixture-of-experts gating by own variables;
  - T5 is standard closed-loop instrumental-variable identification.

**Koulakov.**
- Koulakov et al.'s robustness comes from units that are individually bistable, with hysteresis. Abstract-level check: earlier recurrent integrators needed better than 1% tuning.
- The design's Φ is single-valued. In its mean field, all N = 16 steps exist only for μ > 1 − c/N = 0.984. That is the old tuning requirement.
- The design *uses* this fragility as its control: modulators remove steps by detuning. That is a coherent idea, but it is the opposite of Koulakov's robustness. The novelty table's "robust without tuning" should be withdrawn, or the units made hysteretic (fix 5).

**The second clause.**
- Theorem M is shared by any impulse-driven leaky integrator (§1), so it is not a new invariant.
- Deleting the input scale λ by quantising the input is known, as the author says.
- **The verdict "recombination" is confirmed.**
- The design's real distinctive contribution is the constraint set (innate magnitudes, learning restricted to types, event-only interface, instrumental-variable learning) and the honesty of its Q-table. As shown above, the proofs that the constraint set delivers dial-freedom do not hold yet.

---

## 6. What it fails to explain

- **Vocal convergence on held levels (pitch, voice quality, turn-level pitch; Levitan).**
  - The direct path cannot produce it. The author concedes this.
  - The content path (C2) can produce only a few quantised, hysteretic levels per family, which compete with every other use of those families' steps. That is not graded convergence.
  - Graded intensity effects, where a stronger smile is returned more strongly, are also out of reach.
- **Fast match, then context at 2–4 s.** The timing is covered: phasic at 0.3–0.5 s, appraisal at 1–3 s. But it conflicts with Carr et al. 2014, where the *early*, matching response was corrugator, and zygomaticus came at 2–4 s and carried the context. The design's fast route includes the smile. Context-gating of the phasic smile through S (P6) helps only when the context is already known.
- **Sign flips.** Tonic sign flips are covered by mode choice (P7). The phasic route never flips sign. With R_f = 6, a family has at most six relationship patterns per side.
- **Partner history learned in minutes.**
  - ℓ, a and E are learned only overnight in replay.
  - r_f is re-chosen only at a side change, a partner change or n_f = 0.
  - Within a session, a stranger's growing rapport, or a sudden "this person is unfair" that should re-select the circuit, can act only through positions and modulators, which are own-drive and event state.
  - Hofman's immediate withdrawal of smile return is covered (P8). Learning a new relationship-specific *circuit* within one conversation is not.
- **Time scales, reflex to temperament.**
  - Reflex, episode and mood are well structured, with exponential hold times.
  - Temperament is not structural: β has no path to T_hold, T3(c).
  - Hold times are exponentially sensitive to the innate T, with an elasticity of 8.
  - The tonic modulator's 36 h constant makes satiety-driven release take up to a day.

---

## 7. Concrete fixes

1. **Close the content route in the rank proof.** Do one of the following:
   - (a) Enforce a per-family **event budget**: at most one step per family per partner change within W, implemented as a family-level refractory period of length |W| after any partner-triggered step. Then rank ≤ 2 per family is true by construction.
   - (b) Count content-mediated events as named quantities with their own rank, and re-prove T1 with them.

   Also state the phasic contribution of own-step-triggered bursts.
2. **Make the staircase cap real under event trains.**
   - Kicks must land only on existing plateaus: clip the jump target to k_max(μ_f). A step that does not exist cannot be taken.
   - Alternatively, set T_r ≥ T₊(k_max, μ).
   - Then prove a rate theorem: for any event train, n_f ≤ k_max(μ_f) at all times.
   - Add the partner's event rate to the Q-table if any rate dependence remains.
3. **State level-blindness honestly.**
   - Either forbid E3, E2-surprise and E5 heads from reading partner *levels* (feed them event histories only), or name each E3 head weight as a per-family quantity Q10 with its rank, ceiling and sign.
   - Remove the need-conditioned threshold crossings that occur without partner movement: count an event only on movement of the partner's signal.
   - Re-prove L1 on that basis.
4. **Bound the relationship key.**
   - Replace the isotropic 24-dimensional bound with a bound on the operator's measured, anisotropic perceived U in 12 dimensions.
   - Add an innate constraint that holds for every key: for example, cap the summed alignment Σ_f ⟨H_f, U⟩ across families, or require that at most one family's active mode has positive alignment with U for any one partner.
   - Give the phasic route per-channel gates that a single posture cannot open together, and a learned inhibitory phasic option, so that the phasic channel's own sign can flip.
5. **Fix the dynamical-systems attributions.**
   - Either use hysteretic units (a multi-valued Φ, as in Koulakov and in Goldman et al. 2003), with modulators shrinking the hysteresis width, or drop "robust without tuning" and report the tuning window (μ > 0.984 for all steps).
   - Call the births non-smooth folds.
   - Correct T3(a) at μ = 1 and T3(c) (β).
   - Correct the §4 comparison: Theorem M holds for linear impulse-driven integrators too.
6. **Smaller items.**
   - Make the Claude scorer recompute c with partner inputs masked from the start of the window, or state that partner history reaches it.
   - Restrict T2(e) to the expressive columns.
   - Restate T2(f) with the boredom-side presence reward.
   - Fix the 24/25 postures, the two definitions of n_f, and the double use of β.
   - Declare "arousal load" and "aversive load" explicitly as innate valenced gauges, or replace them with neutral afferent variables.
