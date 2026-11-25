# Critique: Partner as learned regulator (design-partner-regulator.md)

Independent critic, 2026-11-25, written under questions.md Q16 and Q17. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

**Summary verdict.**
- **Proofs.** 28 items checked: 12 valid, 10 with a gap, 6 with an error.
- **The worst error.** The claim that the learned partner input gain is "deleted, not tuned" (§4.0, T1 iv, T1 vii) holds only at one operating point, h = 0. The agent never stays there: the contingency deficit drifts upward by design, and the innate ports push N on every frame. At any operating drive h₀ ≠ 0, the bilinear term linearises to an ordinary additive input, δẋ = A δx + π 𝒯(c)[h₀] δo. That is Lemma A's form with B_eff = π𝒯(c)[h₀]. Scaling ā, π, or the tonic drive |h₀| then runs the steady partner-to-act transfer from exactly 0 to a diagonal copy (C4: Γ = 0 → 0.07·I → 0.26·I; partner–act correlation 0.98). The design's own example in T1(vii) (α(o) = −o_k) is this copier.
- **The dial.** Yes, several, and T1(iv) itself states one. "Scaling changes size, never profile" is the definition of a single gain on a fixed profile. Other dials: the dictionary damping scale b̄ (or r_N) crosses the P6 threshold and takes the agent from rest at x* to a sustained attractor ±z_e(c) whose direction the partner's context sets (C5); κ_s sets that attractor's size. The learned K_b is a Lemma-A additive path from the partner-driven plant (arousal contagion).
- **Human sign flips.** Partly. Relationship-dependent sign flips are representable through α(c). Given a one-signed tonic drive, the partner's context then sets the sign of the response (C6), which contradicts the reading of T1(v). But (a) the design has no robust, context-poor smile-to-smile core: its response at true satiety is zero in theory, and in the full system it is second-order and slow (C6); (b) the body that teaches α is content-blind, so the antagonistic flips (a rival's distress is my gain) have no learning signal; (c) fast matching followed by later context (Carr 2014) is not produced for a known relationship. This is a serious mismatch, though not fatal.
- **Novelty.** The author's verdict, recombination, is confirmed. The second-clause candidate fails. The "derived invariants" (equilibrium invariance, susceptibility linear in state, oddness, non-actuated subspace) are the defining properties of homogeneous bilinear control systems. The common Lyapunov function is the standard one for port-Hamiltonian systems with modulated structure matrices. The deletion of the input gain is imposed (B = 0), not derived. It is also incomplete (K_b), and at h₀ ≠ 0 the gain comes back.
- **Top fix.** Replace "no dial" with an operating-point theorem: bound the transfer B_eff = π𝒯(c)[h₀] and prove a positive copy defect δ_Γ by a structural constraint. Candidate constraint: no dictionary atom may be driven by the partner's version of the act it produces. Declare a separate, fixed, innate matching subspace for the robust human smile core.

## Sources read for this critique

| Source | How read |
|---|---|
| The design, research/foundations/design-partner-regulator.md | in full, 677 lines |
| questions.md Q16–Q17; brief.md (Principles, Prior work, foundations section); foundations/designs.md | in full |
| math-objects-, mimicry-context-, coordination-synthesis.md | in full |
| emotion-elements-synthesis.md | in full |
| face-development-synthesis.md | in full |
| memory-replay-synthesis.md | §2–§4 in full; §1 headings and first paragraphs |
| llm-coupling-synthesis.md | §2–§7 in full; §1 skipped |
| Prior work named in §4 (Mohler 1973 and Elliott 2009 on bilinear control systems; Brockett 1972; Valentin, Magos & Maschke 2007 and van der Schaft & Jeltsema 2014 on switched and modulated port-Hamiltonian systems; Shamma & Athans 1990 on gain scheduling; Sutskever, Martens & Hinton 2011 multiplicative RNN; Ha et al. 2016 hypernetworks; Linderman et al. 2017 rSLDS; Salinas & Thier 2000 gain modulation; Feldman & Friston 2010 attention as precision) | **Not read for this critique.** Named from memory, as pointers for the author to check. No proof below rests on them. |

**Numerical checks.** The script is `research/foundations/sims/critique-partner-regulator/check.py`. Run it with `uv run python critique-partner-regulator/check.py` from sims/. Each check runs the design's own equation (★) on a hand-set instance of 2–3 states. These are algebra checks, not evidence about behaviour or people. They are cited below as C1–C10.

---

## 1. Proof check, theorem by theorem

### L1 (drive map): **valid**
- Steps 1–4 check. h_i′ = q_i + φ_i″ ≥ q_i gives a C¹ bijection.
- Convexity with φ(0) = 0 gives φ(z) ≤ zφ′(z).
- φ ≥ 0, because φ is even and convex with φ(0) = φ′(0) = 0. With this, |h_i|² ≥ q_i²z² + 2q_iφ ≥ q_iH_i. The constant could be 2q_min, but the stated bound is correct.
- Notation: β_i (wall scale) collides with β_q (dictionary damping coefficients) and with Mamba's β. Rename one.

### T0, the power-balance identity: **valid**
dH/dt = hᵀẋ, and hᵀJ(t)h = 0 pointwise for any skew J(t). No dwell time is needed. This is correct and standard.

### T0(a), exponential return under bounded contagion: **gap**
The algebra is right for the system it states. That system does not run, for three reasons.
1. **The interoceptive term is learned state feedback, not an input.** K_b(b − C_b x_N) contains −K_b C_b x_N, which is linear in x. K_b and C_b are learned and unconstrained (θ contains both).
   - The proof's "zero additive inputs" needs b ≡ C_b x_N, which nothing enforces.
   - With b held at b* = 0, the term is −K_b C_b x_N. If its symmetric part is negative enough, it removes need damping like contagion, but outside the δ̄ bookkeeping.
   - **Counterexample (C2).** r_N = 0.2, d = +0.1 (bounded contagion holds), r_M = 2, ω = 1, K_bC_b = −1. The eigenvalues are +0.257 and −1.557, and |z| grows from 0.1 to 6.7×10⁵ in 60 s without saturation.
2. **δ̄ undercounts partners.** π̇_j = (p_j − π_j)/τ_π never returns to exactly 0, so every person ever met has π_j > 0 forever. "|𝒫_present|" must be |𝒫| (plus Claude), which grows. The per-person cap ā, b̄ of P7 does not bound the sum.
3. **(A4) assumes the plant b is bounded.** That is not shown. §2.6 lets looming and loudness *remove* damping (K_p + Σ s_kΔ_k can lose definiteness), so b can grow while those inputs persist. A condition such as K_p + Σ_k s̄_k min(Δ_k, 0) ≻ 0 must be added.

### T0(b), bounded escalation: **gap**
- The ball argument is right in substance. Outside the (N, M) ball R ⪰ ρ_*I. Inside it, the C block is a stable linear system driven by bounded h_N, so it is ISS. The cubic saturation dominates the linear feedback −K_bC_b x_N for large |z_NM|, so (b) survives point 1 above.
- But the proof treats K_b(b − C_b x_N) as a bounded input ū. That is circular, because boundedness of x_N is what is being proved. Step 4 also drops J′_CC; this is harmless, since the energy form handles it.
- C1 reproduces the plateaus exactly (0.8715 and 1.7410).
- **Important by-product.** The plateau is a new equilibrium, not x*. See T1(vii).

### T1(i), equilibrium invariance: **valid (under its hypotheses)**
- With s, b-error and ξ all zero, F(x*)h(x*) = 0.
- Uniqueness uses R(x, c) ≻ 0 at the candidate x, not at x*. That holds, because R₀(x) − R₀(x*) = κ_s|z_NM|²Π_NM ⪰ 0.
- The hypotheses matter more than the proof. Every claim the design builds on it ("the partner cannot move my resting point", §1; "no partner-dependent equilibrium at all", §4.4) drops them. See T1(vii) and §2.

### T1(ii), susceptibility linear in h: **valid**
Direct differentiation. The bound is also correct.

### T1(iii), no state-independent copying: **gap (proof valid, conclusion over-read)**
- The proof is correct: a linear map that is constant on an open set is zero.
- The definition makes the theorem vacuous. Every bilinear system has a state-dependent susceptibility, so no bilinear system "copies" in this sense.
- The behaviour the known-failures row describes is different: the agent's act time series follows the partner's at the operating point. That is a statement about the input–output map along trajectories. An agent with a nearly constant tonic drive h₀ has ∂ẋ_M/∂o ≈ 𝒯[h₀] ≈ constant on the region it actually visits.
- C4: with a tonic need u_N = 0.3 and the design's own α(o) = −ā tanh(o_k), the agent's acts correlate 0.98 with the partner's channels (ā = 0.2) under a slowly varying partner signal.

### T1(iv), scaling changes size, never profile: **error**
- The algebra 𝒯_γ = γ𝒯 at a fixed state is correct.
- The conclusion "no one-parameter scaling of the partner path runs from flat to copy" is false for the closed loop.
  - **Counterexample 1 (C4), at a tonic drive.** With u_N > 0, the equilibrium act vector is z_M = ā u_N tanh(o) / (r_M r_N + ā²|tanh o|²). In the instance this is a diagonal copy of the partner's channels. The fitted steady transfer is Γ = 0 at ā = 0, 0.074·I at ā = 0.1 and 0.26·I at ā = 0.5 (R² ≥ 0.98).
  - **Counterexample 2 (C5), through the threshold.** Scaling β by γ moves d(c) across −r_{N,eff}. Below threshold the agent rests at x*. Above it the agent sits at ±z_e(c), a sustained state whose direction the partner context chooses: (z_N, smile, frown) = (0.80, 0.34, 0) under context A and (0.80, 0, 0.34) under context B.
- And the statement itself names a dial: at each drive state, the partner's effect is one fixed profile times one scalar.

### T1(v), no sign authorship: **gap**
- The proof is valid for an open-loop context history c(·).
- **The design's own context is closed-loop.** e is retrieved with the score γ cos(h, h_μ) (§5.7), which is odd in h. So c(−z) ≠ c(z), and oddness fails (C7: z(3; z₀) + z(3; −z₀) = (−0.022, 0.066, −0.010) ≠ 0). The online update of r_j also depends on x's history.
- **The interpretation is weaker than it sounds.** Oddness says flipping the agent's deviation flips the response. It does not stop the partner from setting the sign of ∂x/∂o. With a one-signed tonic or innately seeded drive, the sign of the response is sign(∂α/∂o) — learned and partner-dependent (C6).

### T1(vi), dial rank, copy cone, copy defect: **gap**
- The definitions are sound, and 𝒦_Γ is a convex cone.
- The escape clause "Γ-like only while the drive is resupplied" covers the normal case. The design resupplies the contingency deficit continuously (drift ν), and the innate ports push N whenever a face is present.
- δ_Γ is left to learning. No structural constraint makes it positive.

### T1(vii), survival of the math-objects reductions: **error (first bullet)**
- **First bullet, "the equilibrium set is {x*} for every partner state", is false in two regimes the design allows.**
  1. **Net contagion.** (A3) allows it, and P6 and T0(b) use it. The equilibrium set is then {x*} ∪ {±z_e(c)}, and x* is unstable. Small noise ξ (always on) sends the agent to ±z_e(c). The partner's context sets its direction and the agent sets only its sign (C1, C5).
  2. **Any constant additive input u₀.** This means body drift through K_b, or innate G s. The equilibrium is then h_eq(c) = −F(c)⁻¹u₀. Its derivative is ∂h_eq/∂c = F⁻¹(∂F/∂c)F⁻¹u₀ ≠ 0, a general learned linear map of the partner context.

  So the sheaf-style "harmonic extension" A⁺Bu is not 0. It is −F(c)⁻¹u₀, a transport whose content is the agent's own tonic drive, routed by the partner.
- **Second bullet (cross-block, same-channel countering): valid.** Note that its example α(o) = −o_k is a copier whenever h_{N,i} > 0, which is the agent's normal state.
- **Third bullet (Altafini across states): valid but vacuous** on a one-signed visited set. The author says so.

### T2(i), (ii), (iv): **valid**
(ii) holds conditionally on zero input.

### T2(iii), nothing acts at satiety: **gap**
- At the instant x = x*, ẋ_M = 0, because G and K_b feed only N. That is true.
- But x* is not invariant once a partner is present. The innate ports and the learned K_b move N, and then learned routing acts.
- C6 shows this. From x* with an innate mutual-gaze seed G s = 0.2, the learned route produces a smile act of 0.05 at 1 s and 0.13 at 3 s, with a sign set by α(o, r_j).
- "Response zero at satiety" holds only in the stripped system.

### T2(v), no reward for smiles, attention or time: **gap**
- There is no ∇U, by inspection. That is correct.
- But the only teacher is the plant, and its partner-dependent terms are contingency, mutual-gaze damping and prosodic smoothness. The agent therefore learns which of its acts elicit the partner's contingent responses and gaze. It does so as need relief: the act drive is −J_NMᵀh_N, need-scaled.
- That is attention-seeking gated by need. It is satiable, as Principle 6 requires, but it is the attention gradient the principle names. The author's "residual risk" understates it: it is what α is trained on.

### T3(a), spectral bound: **valid**
The linearisation at x* is (J − R)Q, because h(x*) = 0 removes the dR₀/dx term. It is similar to J′ − R′, and the Rayleigh-quotient argument holds.

### T3(b), the ladder: **valid** (algebra and numbers reproduced)
- C9 reproduces the eigenvalues −19.95, −0.1002 and −4.0×10⁻⁵.
- But the design's check uses r_C = 0, which violates (A2) (R_min ≻ 0). With r_C > 0, the slowest rate is r_C + ω_NC²/r_{N,eff} ≥ r_C (C9). The innate floor r_C caps the temperament scale from above.

### T3(c), slow rates are not free constants: **error (minor algebra) and gap**
- **Algebra.** Δr_{N,eff} = π[(ω + α_jω_q)² − ω²]/r_M should be [(ω + πα_jω_q)² − ω²]/r_M. Ω enters as πΩ, so the quadratic term carries π², not π. C9: at π = 0.5 the exact value is 0.281 and the design's formula gives 0.313.
- **Substance.** τ_C ≈ r_{N,eff}/ω_NC². ω_NC is a free learned constant, and choosing it is choosing the mood time constant.
- Worse, it is not identifiable. 𝓛 uses horizons of at most 10 s and replay rollouts of 20 s, so a 7 h mode contributes about 10 s / 7 h ≈ 4×10⁻⁴ of its decay to any target. ω_NC therefore stays where initialisation and regularisation put it.
- "Time scales from structure" holds for the fast and middle rungs. The slow rung is a set constant in disguise.

### T4(a), perceiving a partner act as an induced transition: **valid**
- Correct under fixed body inputs and an open-loop c. The plant route (s → b → K_b) is a second, additive perception route that this statement excludes.
- It is also the defining property of bilinear systems: inputs act only as elements of span{B_k}.

### T4(b), private subspace: **error**
- **The bound.** dim 𝒱 ≤ 4K is false in general. range Ω_q ⊆ span(U_q, V_q) gives 4 dimensions, and range D_q = span A_q adds up to 2 more in N. C8: K = 1 gives 6 and K = 4 gives 24. The figure 128 at K = 32 is right for a different reason: all U_q and A_q lie in N, which has dimension 64, and V_q contributes at most 2K = 64.
- **The interpretation.** "At least half the state is unreachable by the partner" is false. 𝒱^⊥ is not *directly actuated*, but J₀ couples N to C, so the partner reaches every C coordinate over time. C8: a C coordinate outside span V moves from 0.009 to 0.021 when the partner's damping changes.
- **Further limit.** The whole N block (all needs) can lie inside 𝒱. Only acts and mood can be private.

### T4(c), observer convergence: **gap**
- This is a correct application of contraction theory, given that f − LE is contracting.
- That premise is not shown and is unlikely to hold everywhere. E depends only on z_M, through a saturating σ. So ∂E → 0 at high expression intensity, and N and C are observable only through J₀. L is trained for open-loop prediction, not for contraction.
- The ball radius also needs the metric's condition number.

### T4(d), tracking separate from aligning: **valid** (structural)
The author's own §8.8 flags that the λ_o loss shares weights with the self-model.

### P5, per-channel signed coupling: **valid**
(Ω_q h)_M = −V_{q,M}U_qᵀh_N checks.

### P6, coregulation versus contagion: **error**
- "Stable iff d > −r_{N,eff}; the trace is then negative" is false when acts are underdamped (ω > r_M), which is the regime the design calls distinctive (§4.7, §8.7).
- The trace is −(r_N + d + r_M). It can be positive while the determinant is positive.
- **Counterexample (C3).** r_N = 0.2, r_M = 0.5, ω = 2, d = −1.5. Here det = 3.35 > 0, but trace = +0.8 and the eigenvalues are 0.4 ± 1.79i. The loop is unstable although d ≫ −r_{N,eff} = −8.2.
- The correct threshold is d > −r_N − min(r_M, ω²/r_M). In the underdamped regime the loss of stability is a Hopf bifurcation, not a pitchfork.
- With saturation, the result is a limit cycle whose sign alternates (z_N ∈ [−0.93, 0.93]). So "its sign is the sign of the agent's own initial deviation" fails there too.

### P7, protest then despair; dependence bound: **gap**
- The peak formula is valid (C10: 65.917 s).
- **Despair needs an extra condition.** The generic routing J₀ is partner-independent, so the act drive is (ω₀ + π_jω_j)h_N, not π_jh_N. With ω₀ = 0.3 the drive keeps rising after the partner leaves and there is no despair (C10: 0.60 at peak, 0.34 at 400 s, against 0.036 with ω₀ = 0). Despair requires that the social need's routing to acts be wholly partner-specific. That is unstated, and it conflicts with generalisation to strangers.
- The dependence bound is valid per person, with the π² correction. It does not cover the sum over people (T0(a) point 2).

### P8, fast tracking then gated aligning: **gap**
- The latency bookkeeping is valid.
- "Consistent with Carr 2014" does not follow. Carr's context (power) is known in advance, so in the design it acts at route 2's latency, together with any matching. And the design has no context-free content route that could produce the early matching. See §3.

### P9, roles: **valid**
Linearity gives D = π‖𝒯[u]‖(|h_A| − |h_B|).

### Lemma A: **valid**

### §4.0's claim "(★) has B_θ ≡ 0 on every learned partner path": **error**
1. **K_b is learned, and b is driven by the partner.** It is driven through G_b s and the Δ_k modulators. So K_b(b − C_b x_N) is exactly Lemma A's B_θ(c)p with p = b(s(partner)). Scaling K_b runs content-blind arousal contagion from none to strong.
2. **At an operating drive h₀ ≠ 0, the multiplicative path is first-order additive.** B_eff = π𝒯(c)[h₀], and Lemma A applies to it (C4).

### Tally

| Result | Verdict |
|---|---|
| L1; T0 identity; T1(i); T1(ii); T2(i, ii, iv); T3(a); T3(b); T4(a); T4(d); P5; P9; Lemma A | valid (12) |
| T0(a); T0(b); T1(iii); T1(v); T1(vi); T2(iii); T2(v); T4(c); P7; P8 | gap (10) |
| T1(iv); T1(vii) first bullet; T3(c); T4(b); P6; §4.0 "B ≡ 0" | error (6) |

---

## 2. Dial hunt

The design moves the dial from a parameter into the state ("the dial is my own drive"). That relocation is sound only if the drive actually visits zero and both signs. Neither happens by design: the contingency deficit drifts upward, the innate ports push N in fixed directions, and most needs are one-sided deficits. The visited set is a one-signed region around a tonic h₀, where the system is a linear additive-input system with B_eff = π𝒯(c)[h₀].

| Scalar | Runs from | To | Check |
|---|---|---|---|
| ā (scale of α), or π_j | flat: Γ = 0 | a steady copy Γ ∝ ā u_N /(r_M r_N) on whatever profile 𝒯[h₀] has learned; a diagonal copy for the design's own α(o) = −o_k | C4 |
| tonic drive level: the drift rate ν, K_b, or the plant set point b* | flat at u_N = 0 | the same copy, with gain ∝ u_N | C4 (u_N = 0 gives 0 exactly) |
| b̄, or r_N, through the P6 threshold | rest at x* | a sustained attractor ±z_e(c) whose direction the partner's context chooses | C5 |
| κ_s | — | the size of that attractor, ∝ κ_s^{−1/2} | C1 |
| K_b (learned) | body-blind | additive, content-blind arousal contagion from the partner's loudness, looming and motion | Lemma A directly |
| λ_o (observer loss weight) | — | over months, the self-model J₀, R₀ drifts toward the partner's dynamics (the author's §8.8) | not checked; the slowest dial, and a candidate "becoming the other" |
| r_M | — | the copy gain ∝ 1/r_M, and the switch between overdamped (pitchfork) and underdamped (Hopf, C3) escalation | C3, C4 |

**Answer.** A dial exists. T1(iv) is itself one: at a fixed drive, the partner contributes a fixed profile times one scalar. What the design does add is a second index of profile change: the drive direction u ↦ 𝒯(c)[u] and the context c. That is real, but it is the dial rank of a learned bilinear map, not the absence of a dial. Whether 𝒯 can contain a copy on the visited cone is left to learning (δ_Γ), so "never copies" is not established.

---

## 3. Against the human data

**Context-dependent sign flips** (Carr; Häfner & IJzerman; Likowski; Seibt; Reed's in-phase versus anti-phase by influence).
- *Representable.* χ_{k,l} = πΣ_q ∂_{o_l}α_q(c) (Ω_qh)_{M,k}, and ∂α/∂o depends on r_j and e. Given a one-signed drive, the relationship sets the sign of the response to each partner channel, channel by channel (C6: the same seed produces +0.14 or −0.14 on the smile channel depending on α). The coordination requirements 1–2 can be met.
- *Not learnable for antagonistic flips.* α is trained only through the plant, whose partner terms are content-blind (contingency, gaze, loudness, looming, smoothness, motion). "Smile at a rival's pain" requires the partner's distress to be good *for the agent*. No variable in the plant registers the partner's state, and ĥ_j enters only as context, never as a target. So the reactive, antagonistic route of Hess & Fischer has no teaching signal.
- *Learnable only if engagement-relevant.* Complementary flips (smiling at a cooperator's anger) are learned only if smiling elicits more contingency or gaze, or less loudness, from that partner. They are learned as engagement tactics, not as regulation of the partner. The author's §8.10 already concedes that no regard for the partner's need is possible.

**Smiling back at a calm partner when satiated.**
- The theorem says no response; the full system gives a slow one. The innate mutual-gaze or contingency port seeds h_N, and α then routes it. The onset grows like t² (C6: about a third of the asymptote at 1 s).
- Human smile return to strangers is the most robust finding in the mimicry synthesis. It needs no deprivation, and EMG onset is at about 500 ms.
- The design has no content-bearing innate route and no drive-independent learned route, so it lacks the "robust, context-poor core" the synthesis asks for.
- Lakin 2008 (abstract) shows that need *raises* mimicry. It does not show mimicry *vanishing* at satiety.

**Fast matching, then later context** (Carr 2014; Weyers 2009).
- In the design, a known context (a power relation, a competition prime) enters α at the same latency as the content (P8 route 2). Only partner-*state*-dependent effects are late (route 3, through the observer).
- So the design predicts context effects from the start for known relations. That matches Mauersberger 2022 but not Carr's corrugator-early, zygomaticus-late split.
- It produces early context-free matching only if something drive-independent and content-bearing exists, and nothing does.

**An odd prediction the data do not support.** By T1(v) and P5, an over-satiated agent (z_N < 0 on a social need) counter-mimics: it frowns at smiles. No source in the syntheses reports this. If the author keeps the symmetric H, this should be listed as a falsifier.

**Verdict.** Not fatal for relationship-dependent sign flips, which α can carry. It is a serious, structural mismatch for the robust fast smile core and for learning antagonistic responses. Both trace to the same cause: the only partner content that reaches learning passes through a content-blind body, and the only content-bearing path is gated by the agent's drive.

---

## 4. Reduction attempt

| Design part | Existing mechanism it reduces to | Exactness |
|---|---|---|
| ẋ = [J(t) − R(x, t)]∇H, with partner-dependent J and R | port-Hamiltonian system with modulated or switched structure matrices (Valentin, Magos & Maschke 2007; van der Schaft & Jeltsema 2014). H as a common Lyapunov function under arbitrary switching is the standard passivity statement for this class | exact |
| Partner selects coefficients (α, β) over a fixed operator dictionary | gain scheduling / LPV with affine dependence, A(ρ) = A₀ + Σρ_qA_q, with the partner as the exogenous scheduling signal (Shamma & Athans 1990). Quadratic stability under arbitrary scheduling holds here by construction | exact |
| No additive input; equilibrium at 0 for every input; susceptibility linear in state; odd flow; inputs perceived as elements of span{A_q}; non-actuated subspace | **homogeneous bilinear control system** ẋ = (A + Σu_qB_q)x (Mohler 1973; Elliott 2009), here composed with ∇H. Each of T1(i), (ii), (v), T4(a) and T4(b) is a textbook property of this class. Its reachability is governed by the Lie algebra generated by {A, B_q} (Brockett 1972), which is the correct tool for the "private subspace" claim | exact, modulo ∇H |
| Dictionary plus gating MLP | multiplicative or factored-transition RNN W(x) = Σ_f x_f W_f (Sutskever et al. 2011); hypernetwork-generated operators (Ha et al. 2016); switching linear dynamics with context-dependent switching (rSLDS, Linderman 2017). As a selective SSM, it is Mamba with input-dependent A (Δ) and B = 0 | exact up to the skew/symmetric parameterisation |
| D(c), partner-modulated damping on needs | in active inference, context-set precision on one's own prediction errors (attention as precision, Feldman & Friston 2010). In neuroscience, multiplicative gain modulation (Salinas & Thier 2000) | close analogy |
| Act law z_M ≈ −r_M⁻¹J_NMᵀh_N | reflex-arc action and damping injection (the author's §4.7) | exact, in the overdamped limit |
| IDA-PBC framing (§4.6) | **correction:** IDA-PBC assigns (J_d, R_d) through a control input solving matching equations. Here no control realises the structure; the matrices are simply modulated by an exogenous signal. "pH system with exogenously modulated interconnection and damping" is the accurate name. Calling it IDA-PBC overstates the link to control design | — |

**Is "the learned partner input gain is deleted" a genuine derived invariant?** No, for three reasons.
1. It is imposed by parameterisation (B = 0). It is not derived from a changed signature. Everything said to follow from it follows from homogeneity of a bilinear system.
2. It is incomplete: K_b is a learned additive path from the partner-driven plant.
3. It does not survive linearisation at any operating drive h₀ ≠ 0, where B_eff = π𝒯(c)[h₀]. The design's dynamics never sit at h₀ = 0 while a partner is present.

What is specific to the design is the bookkeeping: a skew/symmetric split that makes act tendencies the transpose of learned consequences, and the placement of the partner on the operator side. These are useful modelling choices. Neither is a new computation.

**Verdict: recombination; the second clause is not met.**

---

## 5. What it fails to explain

**From emotion-elements-synthesis.md.**
- **Row 1, row 11 and D8: incentive wanting without deficit** (Berridge). Wanting is −J_NMᵀh_N, which is 0 at satiety. Cue-triggered wanting in a sated agent is impossible by construction. The design takes the drive-reduction side of the D8 dispute and cannot test it.
- **Row 3: valence.** −dH/dt = hᵀRh − hᵀu. hᵀΩh = 0, so all partner *routing* is valence-neutral. Only damping changes carry valence. A sated agent (h = 0) has zero valence whatever happens, so pleasure in a friend's smile at rest is impossible. Laughter and positive affect at rest have no source.
- **Row 4: hysteresis.** Absent (the author's item 13). The underdamped branch gives Hopf oscillation instead (C3).
- **Row 7: precision.** K_b gets **no gradient**: §2.10's rollouts contain "no interoceptive correction". So the one precision parameter is fixed at initialisation. The row's ablation tests an untrained constant.
- **Row 8: novelty from observer error.** The table says the uncertainty variable is "driven by observer error", but no equation wires observer error into the plant or into N.
- **Row 13(b).** Shuffling the partner's timing should lower confidence (S13). The design has no posterior or confidence variable, only a rising contingency deficit.
- **D1(a).** Claude can modulate only an existing drive. At satiety a reappraisal does nothing, so the constructionist prediction is partly decided by design (the synthesis warns about this).
- **D4.** K_b is a fixed small constant, so "prediction-led" is assumed, not testable.

**From face-development-synthesis.md.**
- **Facial feedback** (§1 property 2; §4 item 4). The muscle state, and the deliberate route a_del, never feed back into x. Posing a smile cannot change state. The closed loop the synthesis requires is missing.
- **Learning imitation by contingency** (Ray & Heyes; Cook). There is no see-x/do-x map, and the body teacher is content-blind ("a contingent frown satisfies it as much as a contingent smile"). So the synthesis's falsifiable test, crossed training reversing mimicry into counter-mimicry, comes out *null* in this design. Humans reverse after 50–90 minutes.
- **Murray's result.** The *form* of mirroring predicts expressiveness and overall contingency does not. The design's only social teacher is overall contingency.
- **Still-face.** The partner is present (π = 1) but unresponsive. The deficit rises and act drive *keeps growing* (bidding) with no mechanism for the documented drop in positive affect and the rise in gaze aversion.
- **Social smiling.** It tracks postconceptional age, not experience (Messinger & Fogel). The design derives it from learning J_NM.

**From memory-replay-synthesis.md.**
- **Tag rot.** Tags store h and (α, β) in coordinates of the dictionary, and replay retrains that dictionary nightly. Retrieval scores −β_μ·u(h) then mix old coefficients with new atoms. No re-tagging (T3, L4) and no innate-coordinate tags (§2, L9).
- **No coverage term.** Priority ∝ |error| × |h| is pure salience. This is the L3 failure (everyday low-arousal interaction fades; negative drift).
- **No post-event window** (L7). Significance that becomes clear minutes later is lost.
- **No distillation or anchor term** (L10, §1.5). Nothing stabilises temperament across nightly retraining. λ_o actively pulls J₀ toward partners.
- **E1 lesion.** The design's S6 lesion is "uniform priority without tags", which mixes L1 and L2. The synthesis predicts that L2 alone leaves specificity largely intact, so the stated lesion can fail for the wrong reason.

**From llm-coupling-synthesis.md.**
- **"Claude never drives frames becomes a theorem" is not true of the design.**
  - The deliberate route a_del = 𝒟el(d) maps Claude's display intent directly to muscle targets.
  - Through β_κ < 0, Claude can push the agent past the contagion threshold and select the attractor direction (C5 applies to κ like any partner).
- **Draft scoring is not homeostatic.** cos(Δ_M(d), ẋ_M) is scale-free, so the tilt is full-strength (≤ log 3 nats) at any |h| above the noise floor. It does not scale with need as §3.4 of the synthesis requires. Use the inner product, which scales with |h|².
- **Draft collapse** (§3.2). All three drafts pass through MiniLM into the same small MLP. Similar drafts give near-identical (α_κ, β_κ), so Var ≈ 0 and selection is dead. This is unmeasured.
- **History drift** (§6.5). Unaddressed.
- **Reverse grounding.** "Names enter as text in later prompts". If a cluster name is inserted when the agent is in that cluster, it is a state-selected label, which is inadmissible under the synthesis's criterion and Principle 4. The design must say that names enter only through verbatim retrieved episodes.

---

## 6. Buildability on an M1 Pro, 16 GB

- **Parameter counts.** I recomputed every row: total 209,394, matching "≈ 209k". The FLOP estimate and the fast-loop latency (about 20–25 ms per frame) are plausible.
- **Online learning does not fit as stated.** SGD every 1 s on 2 s rollouts means 60 frames × 16 RK4 evaluations = 960 sequential small evaluations, plus backward. In eager PyTorch on CPU that is roughly 0.5–1.5 s per update (my estimate; not measured). It must run in a separate process and will occupy about one core continuously. A 2 s rollout also cannot compute 𝓛's 10 s horizon term.
- **Replay memory.** The 160 MB figure counts states only. RK4 stage intermediates (MLP activations and dictionary projections, about 1k floats per evaluation) bring 64 × 600 × 16 evaluations to roughly 2–4 GB without checkpointing. It fits in 16 GB, and "under 3 GB" needs gradient checkpointing.
- **Numerical hazard.** cosh walls (φ′ = β sinh z) and an unbounded learned R_ℓ, integrated by explicit RK4 at a fixed 8.3 ms, become unstable once any rate exceeds about 340 s⁻¹. Training near the contagion threshold also gives exploding BPTT gradients. A cap on R_ℓ and an implicit or IMEX step for the R part are needed.
- **Identifiability is the real obstacle.**
  - K_b gets no gradient (§5 above).
  - The M-block parameters (R_ℓ on M, J_MM, J_MC) get none either, because z_M is clamped to efference copies in the rollouts.
  - The C modes are invisible to a 10 s horizon (T3(c)).
  - The 28.9k reading-map parameters and the 20.5k dictionary are taught only by 10 plant channels, whose partner dependence is 6 content-blind features. The content-dependent gating that the mimicry data require has almost no teaching signal.

**Verdict.** Buildable on the Mac; the compute is trivial. As specified, the learning problem is under-identified exactly where the design's claims live (mood time scales, precision, content-dependent partner gating).

---

## 7. The most important fixes, in order

1. **Replace "no dial" with an operating-point theorem and a structural copy defect.**
   - State the transfer at the visited drive: δx_eq = F(c)⁻¹π𝒯(c)[h₀]δo. Bound its norm.
   - Make δ_Γ > 0 by construction. One candidate: parameterise α_q(c) = α_q(P_q^⊥õ, r_j, ĥ_j, e), where P_q^⊥ removes the partner channels that correspond (through E) to the act directions V_q routes into. No atom can then be driven by the partner's version of its own act, and the copy matrix lies outside the image of 𝒯 for every c and h.
   - Then declare a **separate, fixed, innate matching subspace** (smile to smile, brow relaxation to smile). This gives the robust human core of the mimicry synthesis. The no-copy theorem then holds off that declared subspace, as math-objects §2(a)(ii) asks.
2. **Close the K_b loophole and give it a gradient.** Either make the interoceptive correction dissipative (for example −C_bᵀΓC_b h_N with Γ ⪰ 0, which keeps T0 intact) and innate, or admit it as a learned additive partner path and bound it. Include the correction in the rollouts, or K_b is never learned.
3. **Correct the proofs.**
   - P6: add the Hopf branch; the threshold is −r_N − min(r_M, ω²/r_M).
   - T1(vii) and §1: the equilibrium set under contagion is {x*} ∪ {±z_e(c)}.
   - T1(v): make retrieval even in h (|cos|), or state the closed-loop exception.
   - T4(b): the correct bound, and "not directly actuated" instead of "unreachable"; use the Lie-algebra rank condition for real reachability.
   - T3(c): the π² term.
   - T0: a plant-boundedness condition and δ̄ summed over all known people.
4. **Give content a teacher.** The body is content-blind, so add a learning rule that sees partner content: a contingency (prediction-error) rule between own and partner acts, as in Cook and Heyes. Or let the observer loss train α. Write down the crossed-training prediction.
5. **Time scales.** Admit that r_C and ω_NC set the temperament scale, or add a day-scale objective in replay so that C modes are identifiable.
6. **Memory and Claude.**
   - Re-tag stored (α, β, h) after each nightly update, or tag in innate coordinates (b, s).
   - Add a coverage term to replay priority.
   - Score drafts by inner product, not cosine.
   - Restate Principle 4 compliance with the deliberate route included.
