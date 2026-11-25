# Design: the partner as a factor of the agent's own regulation ("regulator images")

## Revision 3 (2026-11-26)

Revision 2 was critiqued (critique-2-design-partner-regulator.md; summary under History). This revision is judged against the refined rule of D78 (operator answer to Q18): no single quantity may run the whole face from flat to copy; every per-channel strength must be set per expression by context and learned relationship, be able to flip sign, stay under an innate ceiling, and copying must never be an attracting state; every such quantity is named and bounded. What changed, and why:

1. **The slow loop is no longer the whole same-group face (§2.10, §2.12, T7).** Revision 2 let one route, the loop through the agent's own needs, carry every sustained same-group response, so one scalar (b̄₋, or the tonic need) ran it from 0 to 1.5·I (critique K1). Now the same-group transfer of each expression group g from each partner j is the sum of three named strengths:
   - ς^inn_{j,g}: the innate phasic match (smile, brow), multiplied by a per-group **gate** σ_{j,g} ∈ [0, 1] that is read from the relation and context through group-g-blind evidence;
   - ς^reg_{j,g}: a new **regard display**, the face showing the trace of the partner's damping operator on the agent's needs ("how much you are calming or unsettling me"), through a fixed innate synergy. Its sign per expression is set by the learned relation;
   - ς^loop_{j,g}: the remaining loop through the agent's needs, now capped by a ceiling built only from innate constants (0.08 at the design values).

   Each has an innate ceiling, proved in T7 with every constant innate. A new observer lemma (L4) makes the reading slope innate, which was the critique's main objection to revision 2's ceiling. The total ceiling is 0.60 for smile (0.33 at DC) and lower for every other group, so a copy (gain near 1) is unreachable by any quantity. The agent's own need gates only the loop and care, which can move a group by at most 0.08.
2. **Copy is not attracting under the design's own learning (T9).** Three reasons, each proved:
   - the copy set lies outside the reachable box;
   - every learned parameter is fitted on the partner's *own part* (the partner's behaviour with the agent's identified effect removed) and on the agent's *own-part body*, so the learning fixed point does not depend on how much the agent follows (check S5);
   - the self-model (J₀, q, R, E) is no longer fitted to the partner's expressions, which removes revision 2's "becoming the other" drift.
3. **The mask is extended (§2.1, §2.11, S2′).**
   - Gaze belongs to the eyes group and voice activity to the voice group; õ₀ keeps head pose only.
   - The relation embedding is split into seven group-blind embeddings r_j^(¬g), each trained only on group-g-blind inputs and on a group-g-blind body target. Because the plant is innate, that target can be computed exactly.
   - Claude's u_inh now multiplies only the affective act route. It no longer touches the innate match or the regard display. Claude can move the innate gate by at most σ̄_κ = 0.25, so it is a regulator, not a copy switch (T7 g).
4. **Concern is re-derived without any partner-response gradient (§2.9, T2 v′, vi′).** Revision 2's J_soc descended on a functional of the user's read face through κ̄, the identified effect of the agent's acts on the user. It is withdrawn. The new care operator J_care replaces "how my acts change you" with **"how my own face would calm a perceiver like me"**: the gradient of the agent's own learned reading map, evaluated on the agent's own face. The user's read distress enters only as a gate, which is evidence. The care operator:
   - descends on no functional of the user's face;
   - uses no model of how the user responds;
   - is satiable, skew and capped.

   All consequence and evidence fits now use the own-part body target, from which every partner-mediated consequence of the agent's acts is removed exactly by the innate plant. So the agent cannot learn to want the user's smiles, gaze, attention or distress. This also removes the contingency-and-attention residual of revision 2 (§8 item 10). The cost is that the agent no longer learns instrumental social acts at all (§8 item 9).
5. **Human data (§2.10, §8).**
   - Smile return can be withdrawn under competition and after unfairness. The smile gate closes, and the regard display turns a rival's smile into brow lowering.
   - Sustained smile coupling between friends now has the right sign: a friend's smile raises the regard display. The loop's substitution is capped at 0.08.
   - Anger return rises with an unfair reputation, because the brow gate opens as regard falls (Hofman 2012's opposite movements, per expression).
6. **Errors fixed.**
   - T2(v) and (vi) are replaced by T2(v′) and (vi′), which agree.
   - T1′(f)(i) uniqueness is replaced by T8: an innate small-gain cap on the care operator and the saturation makes the core contracting for frozen context, so the K6 bistability is excluded (check S4: (SG) threshold 0.136, K6 onset 1.16).
   - T6 now includes the direct port route and the regard route, which start as t′³. The innate match still leads at t′². The leading coefficient is corrected.
   - Other corrections:
     - T0(b) is C_b-free;
     - the observer contraction (T4 c) is proved (L4);
     - the retrieval query is defined and even;
     - the presence filter typo is fixed;
     - P7 includes the care term.
7. **Kept** as critique 2 found them valid: L1, L2, the T0 identity and T0(a), L3, T1′(a), the T1′(c) inequality, T2(i–iv), T3, T4(a, b, d), the T5 recursion and corollaries, T6(b, e), P5, P6, P9, Lemma A and §4.0. Critique 2's corrections are applied to T1′(d) (first order in |h₀|), T1′(e)(iii) (the third option is acknowledged) and T5 (exclusion and truncation).

**Withdrawn:**
- T1′(e)(i–ii) as worded (replaced by T7);
- T1′(f)(i) (replaced by T8);
- T2(v) and T2(vi) (replaced);
- J_soc;
- the per-person adapters;
- the learned observer gain matrix L (replaced by a scalar gain).

**Answer to the refined rule, in one line.** Every same-group strength is named, per group and per partner, set by group-blind relation evidence, sign-flippable through the regard display or the loop, and capped by innate constants with a total of at most 0.60. The only common factors are nonnegative gates (presence, and the agent's own need, which reaches at most 0.08 per group). Copy is outside the reachable set, and learning has no feedback from the agent's own following.

Status: revised, awaiting critique 3. This is a design with proofs. It is untested and is not evidence about people. The numeric checks (sims/partner-regulator-r3/check.py, S1–S6) test my own algebra on hand-set instances only.

---

Excluded frameworks, and how this design relates to them:
- Active inference and homeostatic RL are excluded as frameworks. The design has no free-energy or expected-free-energy objective, no policy posterior and no reward.
- The act law coincides, in the overdamped limit, with active inference's reflex-arc action and with damping injection (§4.7).
- Costate and Robust regulator are stood down. The innate gauges only ground learning.

## Sources this design relies on, and how they were read

| Source | How read | Used for |
|---|---|---|
| Gu & Dao 2023, Mamba (arXiv 2312.00752v2) | read by me in revision 1: §2, §3.2, §3.5, App. C | §4.1 |
| Borja & Ortega 2026, passivity-based control (arXiv 2608.15222) | read by me in revision 1: §2, §7 | §4.6 |
| Friston, Mattout & Kilner 2011 (PMC3491875) | read by me in revision 1: first 100k of 175k characters | §4.7 |
| Lakin, Chartrand & Arkin 2008 | abstract and press release only | §8, a human prediction only |
| critique-design-partner-regulator.md, critique-2-design-partner-regulator.md | both in full | every change listed above |
| brief.md, questions.md Q16–Q18 (with the operator's answer), DECISIONS.md D78 | in full this revision | the criterion (T7, T9), Principle 6 (T2 v′) |
| social-appraisal-synthesis.md, agency-wanting-synthesis.md, mimicry-context-synthesis.md, affective-robots-synthesis.md | in full this revision | evidence-only route and guards (T2 v′), care (§2.9), the regard display and gates (§2.10), human patterns (§8), the robot failures (fawning, escalating mirror loop: T9 d) |
| contingency-causal-synthesis.md, coordination-synthesis.md | in full in revision 2 | T5 |
| Notes cited by those syntheses (hofman-2012, seibt-2015, weyers-2009, fischer-2012, carr-2014, bourgeois-hess-2008, mauersberger-2022, parkinson-simons-2009, houlihan-2023, churamani-2022, lewis-canamero-2016, forssell-ljung-1999, hernan-robins-2020, and others) | **through the syntheses only**; each claim carries the synthesis's reading caveats | §2.10, §8 |
| Project notes used in revision 1 (barrett-simmons, seth, butler-randall, sbarra-hazan (abstract only), hoehl, solomon-corbit, zhang-berridge, yoshida-man, lohmiller-slotine, sontag-iss, port-Hamiltonian NN, altafini, hasani-ltc, gergely-watson) | through the notes | scaffolding lemmas (L4 and T8 use the contraction notion of lohmiller-slotine) |

No new primary source was read for this revision. **Named, not read, and not relied on beyond naming:**
- Jurdjevic & Quinn 1978 and Sontag's L_gV damping control (critique 2's reduction of J_soc);
- mediation analysis and the controlled direct effect (Pearl; VanderWeele), the closest prior to the own-part target (§4.12);
- contraction with delayed interconnections (Wang & Slotine 2006), for the delayed own-part loop in T8;
- "empathic" deep Q-learning, which uses the agent's own value to estimate another's (Bussmann et al. 2019), a possible prior for J_care (§4.11);
- DCM, Brockett and Mohler for bilinear reachability;
- Beckes & Coan's social baseline theory.

---

## 1. Plain-language intuition

Every earlier sketch let the partner in the same way: your face, or something computed from it, is added into my state through a learned map, and the map's strength runs me from ignoring you to becoming you. Revisions 1 and 2 moved the partner into my *regulation* (how fast my needs settle, where they flow) and masked the direct paths: whatever makes my smile move may not look at your smile. Critique 2 found that a slow loop remained, from your smile to my needs and from my needs to my smile. One number (how much your smile unsettles my needs, or how needy I am) then ran my whole sustained face to a copy of yours, and its ceiling depended on learned quantities.

Revision 3 does three things.

**It names every route by which your expression reaches my same expression, and caps each with a constant I was born with.**
- *Innate match.* A fast, fixed smile-to-smile and brow-to-brow echo, which fades within seconds. It is now **gated**, per expression, by how this person is regulating me, read without looking at that expression.
  - With a rival, the smile echo closes. With someone who has been unfair to me, the brow echo opens.
  - Claude can nudge the gate (by at most a quarter of its range) but cannot switch it.
- *Regard.* My face shows how much you, on your own, are calming or unsettling me: a smile with relaxed brows when you calm me, lowered brows when you unsettle me.
  - A friend's smile calms me, so I keep smiling with a friend. A rival's smile unsettles me, so my brow lowers. A rival's distress may relieve me, so my brow relaxes.
  - The sign is set by what I have learned about you, separately for each of your expressions. The display runs through one fixed pattern over smile, brow, eyes and voice, so it can never copy your whole face (L5).
- *The loop through my needs.* It remains, because I cannot stop your state from affecting my needs without losing coregulation, nor my needs from moving my face without losing wanting. Its ceiling is now small and fixed.

**It stops me from learning to want anything from your face.** I still read you, causally: my own random variation tells me which of your changes I caused. But everything I learn is fitted to two things with my effect on you removed:
- *what you do on your own*;
- *what my body does apart from what you did because of me*.

The body is innate, so that subtraction is exact. Whether you answer me or not, whether I follow you or not, I learn the same thing. I can therefore never learn to elicit your smiles, your gaze or your distress, and copying cannot feed itself through learning.

**Concern is comfort as I would be comforted.** When you show distress on the needs whose distress costs me, my own need drives my face toward the faces that have calmed *me*. I find those faces from my own learned reading of others, applied to my own face. I do not use any model of how you will respond, and I am not relieved or rewarded by your face changing. A rival's distress drives no comfort; it may show as relief on my face, never as a motive.

---

## 2. The precise mathematical object

### 2.1 Spaces

- **Time:** t ∈ ℝ≥0, in seconds.
  - Sampling: face at 30 Hz, voice features at 100 Hz, and a 10 Hz grid for identification (T5).
  - The core is a continuous-time ODE integrated between events.
- **Affective state:** x ∈ X = ℝⁿ, with n = n_N + n_M + n_C = 64 + 64 + 128 = 256. The blocks are N (needs), M (acts) and C (context and mood). z := x − x*, with x* = 0 the innate set point.
- **Effectors and groups (innate), unchanged.**
  - M = ⊕_{k=1}^{24} M_k: 16 face effectors of dimension 3 and 8 prosody effectors of dimension 2.
  - Y = ℝ⁶⁰ = ⊕_k Y_k: 52 blendshapes and 8 prosody targets.
  - G = 6 masking groups: brow, eyes/lids, smile/cheek, lower mouth and jaw, nose and other, voice.
  - M_g := ⊕_{k∈g}M_k; W := N ⊕ C.
- **Innate body (plant):** b ∈ ℝ^{10}; b̃ := b − b*.
- **Partner signals, now fully partitioned (new).**
  - Partner j's signal is y_j ∈ Y⁺ := ℝ^{65} = ⊕_{g=1}^{6} Y⁺_g. It contains the 60 expression channels in the agent's coordinates, plus 4 gaze channels **assigned to the eyes group** and voice activity **assigned to the voice group**.
  - Head pose, õ_{j,0} ∈ ℝ⁶, belongs to no group, because the agent has no head effector. If a head effector is added (nodding), head pose becomes a seventh group and is masked like the rest.
  - y_{j,¬g} is y_j with Y⁺_g removed.
- **The agent's own variation and the instrument (unchanged).**
  - ζ(t) ∈ ℝ²⁴ is i.i.d. N(0, σ_ζ²I) on the 10 Hz grid. It is logged and clipped at 4σ.
  - ξ = AR(1)(ζ) with τ_ξ = 0.3 s enters ẋ_M through a fixed B_ξ.
  - ε(t) ∈ ℝ²⁴ is the agent's effector activity.
- **The partner's own part (new).**
  - y_j^own(t) := y_j(t) − Σ_{d=d_min}^{d_max} K_{y,j}(d) ε(t − d), where K_{y,j} is the identified causal kernel from the agent's effectors to the partner's signal (T5 with target y_j; d ∈ [0.2, 4] s).
  - y_j^own is "what the partner does on their own".
- **Masked and own-part plants (new).**
  - The plant is innate, so its response to any port stream is computable exactly.
  - b^own(t): the plant driven by s(y^own) and the agent's actual acts.
  - b^{own,(¬g)}(t): the plant driven by s(y^own_{¬g}) and the agent's actual acts.
  - Seven 10-dimensional linear ODEs.
- **People:** a set 𝒫.
  - Presence beliefs: π̃̇_j = (p_j − π̃_j)/τ_π (typo fixed) and π_j := π̃_j/max(1, Σ_iπ̃_i), so Σ_jπ_j ≤ 1. Claude is a separate regulator κ with π_κ ∈ [0, 1].
  - **Relation embeddings, split by mask (new):** r_j^(¬g) ∈ [−1, 1]³² for g = 0, …, 6, where r^(¬0) := r_j is the full one.
  - **Partner baselines (new):** m_j^(¬g) ∈ ℝ^{64}, the slow (τ = 3 days) running mean of the partner's read need state from the group-g-blind observer. It is the partner's *own* rest, replacing E(0) (critique 2, K4).
- **Episode code:** ep ∈ ℝ³², updated every 2 s from retrieval. The score is s_μ = γ|cos(h_N, h_{N,μ})| + log κ(Δt_μ) − β_μ|h_N|², which is even in h_N (the undefined u of revision 2 is replaced by |h_N|²).
- **My expression:** e(t) is the muscle state of §2.10, logged by efference.

### 2.2 Energy and drive (unchanged, with innate ranges)

H(x) = Σ_i[½q_iz_i² + φ_i(z_i)], h := ∇H, φ_i(z) = η_i(cosh z − 1 − z²/2), with q_i ∈ [q_lo, q_hi] and η_i ∈ [0, η̄] by tanh parameterisation (innate ranges).

### 2.3 Dictionary, observers, contexts and the mask

- **Dictionary 𝒟 (unchanged).** 𝒟 = {(Ω_q, D_q)}_{q=1}^{32}.
  - Each atom has a group g(q) ∈ {0, …, 6} and an effector set Σ_q ⊆ g(q).
  - Ω_q = U_qV_qᵀ − V_qU_qᵀ, with U_q supported on N and V_q on M_{Σ_q} ⊕ C.
  - D_q = A_qA_qᵀ, with A_q supported on N. All columns have unit norm.
  - K := 32 and D̄ := Σ_q‖D_q‖ ≤ K.
- **Observers (new form, L4).** Each observer is the agent's *linear* own model run on a partner stream:

  x̂̇ = (J₀ − R_lin) Q_lin x̂ + ℓ Q_lin⁻¹ E₀′ᵀ Π (u − E₀ − E₀′x̂),

  - Q_lin := diag(q), R_lin := R_min + R_ℓ, E₀ and E₀′ the agent's own expression map and its slope at rest, ℓ ∈ (0, ℓ̄] a learned scalar.
  - u is the stream, and Π zeroes masked channels (it is extended to Y⁺ with a fixed innate encoding of gaze and voice activity).
  - There are 14 observers per partner: on u = y_j and on u = y_j^own, each full and group-g-blind for g = 1, …, 6. They are written x̂_j^(¬g) and x̂_j^{own,(¬g)}, with (¬0) meaning full.
  - The observer reads the partner's face through the agent's own model, which keeps Principle 3's inversion clause. It is never fitted to the partner, apart from ℓ (§2.11).
- **Contexts.** Write ĥ := Q_lin x̂ and ĥ^rel := Q_lin(x̂ − m_j^(¬g)), the read drive relative to the partner's own baseline.
  - c_j^{α,(g)} := (P ĥ_j^{own,(¬g)}, r_j^(¬g), ep, õ_{j,0}): for the α-coefficients of atoms in group g. It is own-part and blind to group g.
  - c_j^{β,(g)} := (P ĥ_j^{own,(¬g)}, r_j^(¬g), ep, õ_{j,0}), for g = 0, …, 6. Of these, c_j^{β,(0)} sets the damping (β acts on N only); the masked ones set the gates (§2.10) and the care weights (§2.9).
  - c_κ: Claude's coupling context (§5.5).
- **Coefficients.**
  - α_q := α̂_q(c_j^{α,(g(q))}) and β_q := β̂_q(c_j^{β,(0)}).
  - α̂ and β̂ form one spectrally normalised MLP with tanh outputs.
  - Bounds: |α| ≤ ā and −b̄₋ ≤ β ≤ b̄₊.
  - Lipschitz caps: L_α and L_β; context features have a Lipschitz cap p̄ in ĥ (‖P‖ ≤ p̄).
- **The extended mask (S2′).** For every group g, every partner-dependent quantity in the M_g-rows of ẋ, in the gate σ_{j,g} and in the training of r_j^(¬g) and m_j^(¬g) is a functional of y_{j,¬g}, of õ_{j,0}, of the agent's own history and ζ, of Claude's input, and of slowly learned *shared* parameters, never of y_{j,g}. The last item is a residual, bounded in T7(h).
- **Copy-pattern subspace.** 𝒞 := {Γ ∈ ℝ^{60×65} : Γ_{Y_g, Y⁺_{g′}} = 0 for g′ ≠ g}, with Frobenius projection P_𝒞. The copy set at tolerance δ is 𝒦_copy(δ) := {Γ ∈ 𝒞 : every group block has gain ≥ 1 − δ along its matched channels}.

### 2.4 The core equation

ẋ = [ J₀ + J_care(x, c) + Σ_j π_j Ω(c_j^α) + π_κ Ω(c_κ) − R₀(x) − R_int − Σ_j π_j D(c_j^{β,(0)}) − π_κ D(c_κ) ] h(x) + Π_N( G s(t) + C_bᵀ Γ b̃(t) ) + Π_M B_ξ ξ(t)    (★″)

The terms:
- Ω(c_j^α) := Σ_q α_q Ω_q and D(c) := Σ_q β_q D_q.
- **J₀** ∈ 𝔰𝔬(n) is learned, with blocks NM, NC, NN and CC. **J₀,MM = 0**. Caps: ‖J₀,NM‖, ‖J₀,NC‖ ≤ ω̄.
- **R₀(x) = R_min + R_ℓ + κ_s|z_N|²Π_N + κ_sΣ_g|z_{M_g}|²Π_{M_g}**. R_ℓ ⪰ 0 is learned on N and C only, capped at 300 s⁻¹. R₀ on M is innate and block-diagonal by group, ⪰ r_M I.
- **R_int := Π_N C_bᵀΓC_bΠ_Nᵀ**, with Γ ≻ 0 innate and diagonal, and C_b learned. This is unchanged.
- **J_care** is the care operator, skew by construction (§2.9). It replaces J_soc.
- **Claude** enters with β_κ ∈ [0, b̄₊] (unchanged).

**Structural rules.**
- **(S1) No learned partner additive path** (unchanged). Learned partner-dependent terms all multiply h.
- **(S2′) The extended mask** of §2.3.
- **(S3) Block-diagonal acts** (unchanged). J₀,MM = 0; Ω_q, D_q and J_care have no MM block; R₀ on M is block-diagonal.
- **(S4) Declared innate partner content:**
  - the gated matching filter;
  - the regard synergy and its low-pass;
  - the reflex displays;
  - the ports into the plant and N.
- **(S5) Evidence only (new).** The partner's signals enter as evidence. Formally:
  - (a) no term of ẋ, of the outputs or of Claude's coupling contains a *partner-response factor*, that is, a derivative of the partner's signal or read state with respect to the agent's present or future acts;
  - (b) every learned parameter except ℓ, m_j and K_y is fitted on own-part inputs and on the own-part body target b^own (§2.11).
- **(S6) Self-model isolation (new).** The self-model (J₀, q, η, R_ℓ, E, C_b) receives gradients only from the agent's own body and its own rendered face. It never receives gradients from the partner's expressions.

### 2.5 Assumptions and the innate caps

- (A1) H as in §2.2. (A2) J₀, Ω_q and J_care are skew. R_min ≻ 0 with floors r_N, r_M, r_C. R_ℓ, D_q, R_int ⪰ 0.
- (A3) Contagion is capped: δ̄ := b̄₋D̄ < r_N; Σ_jπ_j ≤ 1; β_κ ≥ 0.
- (A4) Inputs are bounded and the plant is contracting: K_p + Σ_k s̄_kΔ_k⁻ ≻ 0. ξ is bounded.
- (A5′) **Innate caps (all imposed by parameterisation, none learned).**

  | Cap | On | Enforced by |
  |---|---|---|
  | q_lo, q_hi, η̄ | energy curvature | tanh range |
  | ω̄ | J₀ blocks | spectral normalisation |
  | ā, b̄₋, b̄₊ | coefficient ranges | tanh |
  | L_α, L_β | reading map Lipschitz | spectral normalisation |
  | p̄ | context features in ĥ | spectral normalisation and tanh |
  | ℓ̄ | observer gain | clip |
  | ē | ‖E′‖ in normalised coordinates | weight clip |
  | k̄_y | ‖K_y(d)‖ | projection |
  | c_care, χ̄ | care operator norm and gate | norm clip (§2.9) |
  | g_s, g_b, g_r, b_g, s_g, σ̄_κ, τ_r, S_reg, r̃_s, A_relief | output routes | fixed constants |
  | Γ, K_p, Δ_k, G, G_b, F_b, B_ξ, σ_ζ | plant and ports | fixed constants |

- (A6′) Operating points are dissipative. This is **now a consequence** of (SG) in T8, not an assumption.
- (A7) The instrument conditions (I1)–(I4) of T5. (I5): the evidence model class can represent the innate plant's port law (used in T9 b).

**Derived innate constants** (each a formula in the caps above):
- Γ_o := ½√(ℓ̄/r_min), the observer gain (L4);
- β′_max := L_β p̄ Γ_o and α′_max := L_α p̄ Γ_o, the reading slopes;
- h̄, the drive bound (T0 b′);
- ρ_* := min(r_N − δ̄, r_M, r_C);
- ν₀ := r_M q_lo;
- a̅, b̄_M and b̄_W in T1′(c).

### 2.6 The innate plant (fixed)

ḃ = −[K_p + Σ_k s_k(t)Δ_k](b − b*) + G_b s(t) + F_b a(t) + ν(t), as before. It is driven three times: by s(y), giving the real b, which drives (★″); by s(y^own), giving b^own; and by s(y^own_{¬g}), giving b^{own,(¬g)}. All three use the agent's actual acts a.

### 2.7 Response kernels (T5)

- K_{y,j}(d) ∈ ℝ^{65×24}, for d ∈ [0.2, 4] s, is the causal effect of the agent's effector activity at lag d on the partner's signal. It has rank 8, on a 6-function raised-cosine lag basis, and is a generic kernel plus a rank-2 per-person delta.
- It is identified by the T5 recursion with target w = y_j. It replaces revision 2's κ_j onto read needs.
- It is used **only** to form y_j^own and b^own: bookkeeping of who did what, never as a model of the partner's response to future acts.

### 2.8 Reciprocity: consequences become tendencies, and only direct consequences count

Skewness gives ẋ_M ∋ −(J₀ + J_care + πΩ)_{NM}ᵀh_N: what my acts do to my needs, transposed, is what my needs make me do.

New in revision 3: the parameters that multiply h_M in the N-equation (J₀,NM and α̂'s N-row action) are fitted in the instrument metric **on b^own** (§2.11). By T5 and (I1)–(I2), their fixed point is the causal effect of my acts on my body *with the partner's identified response held at its own part*: the direct effect, in the terms of mediation analysis (§4.12). Effects that run through the partner's expression (they smile, gaze or calm because of what I did, and that relieves me) are excluded exactly, because the mediator-to-body law is the innate plant.

### 2.9 The care operator J_care (derived, partner-response-free)

The derivation uses only objects already in (★″) and the agent's own model.

1. **Evidence (learned).** The partner's own read distress lowers the damping I receive. The concern weights are ϖ^(g)_{q′,i} := [−∂β̂_{q′}/∂Ĥ_{j,i}]₊, evaluated at c_j^{β,(g)}. β̂ is trained with mask augmentation, so this context is on-distribution (critique 2, T2 vii).
2. **Self-model (the change).** Revision 2 used κ̄_j, the effect of my acts on *your* read state. Revision 3 uses **my own reading map applied to my own face.**
   - Let ψ_q(e) := β̂_q(c_self(e)) be the damping on atom q that a perceiver like me would receive from a face e. Here c_self(e) := (P Q_lin x̂_ss(e), r_∘, ep, õ_∘), where x̂_ss(e) = −A_o⁻¹ℓQ_lin⁻¹E₀′ᵀ(e − E₀) is the full observer's steady state for a constant face e (unique by L4), r_∘ is the generic relation, and õ_∘ is mutual-gaze head pose.
   - The comfort direction of atom q in my group-g acts is d_q^(g) := E′_{M_g}ᵀ ∇_e ψ_q(e)|_{e = E(x)}. It is a property of me alone.
3. **Anticipation through the self-model.**
   - A perceiver like me in the partner's read state ĥ_j^rel would see its need-energy rate change, per need i, by −Σ_q(d_qᵀδz_M) ĥ^rel_{j,i}(D_qĥ^rel_j)_i.
   - Over the innate horizon τ_c = 2 s, by step 1, this changes my damping on atom q′ by τ_cΣ_q χ_{j,q′q}^(g)(d_q^(g)ᵀδz_{M_g}), with

     χ_{j,q′q}^(g) := [ϖ^(g)_{q′} · (ĥ^{rel,(¬g)}_j ⊙ D_q ĥ^{rel,(¬g)}_j)]₊ ∧ χ̄ ≥ 0.
4. **Reciprocity (§2.8).** Writing that anticipated consequence as an N–M_g block and completing it to a skew pair gives

   J_care := Σ_jπ_j Σ_g [[0, −C_j^(g)], [C_j^(g)ᵀ, 0]] on (N, M_g),  C_j^(g) := clip_{c_care|h_N|}( τ_c Σ_{q′,q} χ_{j,q′q}^(g) (D_{q′}h_N) d_q^(g)ᵀ ),

   where clip_r(X) := X·min(1, r/‖X‖). The clip is a positive scalar factor, so skewness is kept.

Three constraints are declared, not derived:
- the mask (the gates use only group-g-blind evidence and the partner's own baseline);
- the clip [·]₊, which keeps only the concern half: a rival whose distress relieves me gets no comfort;
- the norm clip c_care, used by T8.

The care operator uses the *full* (not own-part) partner state: distress I caused is still distress I comfort.

### 2.10 Outputs

- **Affective route (unchanged):** a_aff,k = S_kσ(w_kᵀz_{M_k} + b_k) for face effectors; a_pros,k = w_kᵀz_{M_k} for prosody.
- **Gated innate match (changed).** a_match(t) = Σ_jπ_j^face M_inn diag(σ_{j,g}) [ℓ_{τ_a} − ℓ_{τ_h}] ∗ y_{j,𝒦}(t − t_d), with 𝒦 = {smile/cheek, brow}.
  - M_inn has three blocks: smile → smile (g_s), brow lowering → brow lowering (g_b), and smile → brow relaxation (−g_r, gated by σ_{j,smile}).
  - The gate is

    σ_{j,g} := clip_{[0,1]}( ½[1 + tanh(s_g r̃_j^(¬g)/r̃_s + b_g)] + σ̄_κ u_{κ,j,g} ).

    Its parts:
    - r̃_j^(¬g) is the group-g-blind regard (below), passed through ℓ_{0.5 s};
    - s_smile = +1, so the smile echo closes as regard falls;
    - s_brow = −1, so the brow-lowering echo opens as regard falls (Hofman 2012's opposite movements);
    - b_g = 1 (innate), so σ = 0.88 for a neutral relation;
    - u_{κ,j,g} ∈ [−1, 1] is Claude's bounded relation appraisal (§5.5), and σ̄_κ = 0.25.
- **Regard display (new).**
  - Let r̃_j^(¬g) := tr D(c_j^{β,(g)}) = 2Σ_qβ_q(c_j^{β,(g)}), the trace of partner j's damping operator on my needs: positive when they calm me, negative when they unsettle me.
  - It reads the partner's *own part* and is **not** need-gated: it is the operator, not its action on my drive.
  - The display is a_reg(t) := S_reg tanh( ℓ_{τ_r} ∗ Σ_jπ_j r̃_j^(¬0)/r̃_s ), with:
    - τ_r = 1.5 s;
    - S_reg ∈ Y an innate synergy: smile/cheek +0.25, brow lowering −0.20, lid tightening −0.10 and voice warmth +0.15 (block norms), nothing on the lower mouth or nose;
    - r̃_s := 2√K β′_max, an innate normalisation.
- **Reflex displays** (unchanged): startle; a relief smile of amplitude A_relief = 0.2 on a fast fall of the plant's contingency deficit and arousal; cry with sustained distress.
- **Deliberate route:** (a_del, u_inh) = 𝒟el(intent) from Claude's display intent, with ‖a_del‖ ≤ ā_del.
- **Muscle layer:**

  τ_kṁ_k = −m_k + sat( (1 − u_inh,k)a_aff,k + a_match,k + a_reg,k + a_del,k + reflex_k ).

  u_inh multiplies **only** a_aff. No learned weight trades the routes against each other.

### 2.11 The objective: one residual, two metrics, own-part targets

Let r_b^own(t+k | t) := b^own(t+k) − b̂(t+k | t) be the error of the open-loop rollout, with contexts built from own-part observers. Let Z(t) be the stacked instrument.

𝓛(θ) = E Σ_k‖r_b^own‖²_{Σ_b⁻¹} + λ_Z Σ_k‖Ê[r_b^own Zᵀ]‖²_F + λ_Z Σ_j‖Ê[(y_j − K_{y,j} ∗ ε)Zᵀ]‖²_F + λ_o Σ_j‖r_o‖² + λ_s 𝓛_slow + 𝓛_self.

- **First term (evidence).** It fits β̂, the α̂ N–C action, P, R_ℓ (on N and C) and C_b. β̂ is trained with **mask augmentation**: each rollout uses c^{β,(g)} for a random g ∈ {0, …, 6}.
- **Second term (consequence, instrumented).** It fits J₀,NM and the α̂ N–M action. Its stationary point is the direct effect (§2.8).
- **Third term.** It fits K_y.
- **Observer term.** r_o = y_j − E₀ − E₀′x̂_j fits only ℓ and the baselines m_j (S6).
- **𝓛_slow** is as in revision 2.
- **𝓛_self** fits the self-model on the agent's own data only:
  - E on the agent's own rendered face as perceived in solo self-observation;
  - J₀ (all blocks), q, η and R_ℓ through the first two terms, whose targets are the agent's own body.
- **Per-person, per-group relations.** r_j^(¬g) is trained online every 5 s on 2-s rollouts. Its loss is the first term with target b^{own,(¬g)} and contexts c^{β,(g)}, c^{α,(g)}, so r_j^(¬g) is a functional of y_{j,¬g} only. The full r_j uses g = 0.
- θ never receives a gradient from any functional of the partner's expressions except as a prediction target of ℓ and m_j and as the K_y moment. There is no reward term.

### 2.12 Every per-channel quantity, named and bounded

Same-group strengths are complex gains from partner group g to my group g at frequency ω, in expression units per expression unit, with gain 1 meaning copy. Slow parameters are held for the day (T7 h covers their drift). Design values are given in brackets.

| Quantity | Route | Indexed by | Set by | Sign | Innate ceiling |
|---|---|---|---|---|---|
| ς^inn_{j,g}(ω) = g_g σ_{j,g} b(ω)ℓ_{τ_m}(ω)e^{−iωt_d} | innate match | partner, g ∈ {smile, brow} | σ_{j,g}: group-g-blind regard (relation, context) ± Claude's σ̄_κ | ≥ 0 (gate) | g_g(τ_h − τ_a)/(τ_h + τ_a) [0.27 smile, 0.23 brow]; 0 at DC |
| σ_{j,g} | gate of the match | partner, g ∈ 𝒦 | r̃_j^(¬g), r_j^(¬g), ep, u_κ | ∈ [0, 1]; direction s_g per group | 1; Claude moves it ≤ σ̄_κ [0.25] |
| ς^reg_{j,g}(ω) = S_reg,g ψ′ ℓ_{τ_r}(ω) ∂_{y_g}r̃_j(ω)/r̃_s | regard display | partner, every g | ∂β̂/∂y_g at c_j^{β,(0)}: per partner channel, through r_j | sign(S_reg,g)·sign(∂_{y_g}r̃_j): flips with the relation | ‖S_reg,g‖ [0.25, 0.20, 0.10, 0.15, 0, 0] |
| ς^loop_{j,g}(ω) = [G_loop(iω)]_{gg} | loop through my needs | partner, every g | c_g (my act's consequence), β_g (partner's net push on my concerns), h₀ | T1′(d) rule; flips with the relation | ς̄^loop := (ēa̅/ν₀)(1/ρ_*)(a̅b̄_M/ν₀ + b̄_W) [0.08] |
| A_relief | relief reflex (triggered, not a gain) | smile | plant contingency fall | + | 0.2 (amplitude) |
| Care, C_j^(g) | cross-group only (mask) | partner, g | gate χ (partner's own-baseline distress × ϖ), my need | ≥ 0 routing | ‖C‖ ≤ c_care‖h_N‖ [0.05]; zero same-group |
| u_inh | Claude's display inhibition | effector | Claude | ≥ 0 | touches only a_aff: ≤ ς̄^loop_g of same-group strength |
| Common gates (not strengths) | π_j (presence); ‖h‖ (loop and care only) | — | — | cannot flip a sign | within the ceilings above |

Totals: ς̄^tot_g ≤ 0.60 smile (0.33 at DC), 0.51 brow (0.28), 0.18 eyes, 0.08 lower mouth, 0.08 nose, 0.23 voice. With δ = 0.3, 𝒦_copy(δ) is unreachable (T7 e).

---

## 3. Theorems and proofs

Notation: F(x, t) := J(x, t) − R(x, t), with J := J₀ + J_care + Σπ_jΩ + π_κΩ(c_κ) skew and R := R₀ + R_int + ΣπD + π_κD symmetric.

### L1 (the drive map), unchanged and valid
h is a C¹ diffeomorphism with h(x) = 0 ⇔ x = x*. Moreover h_iz_i ≥ q_iz_i² and |h|² ≥ q_min H.

### L2 (dissipative resolvent and Schur complement), unchanged and valid
Let sym(−X) ⪰ ρI and σ := ‖skew(X)‖. Then:
- (a) ‖(iω − X)⁻¹‖ ≤ 1/μ(ω), with μ(ω) := max(ρ, |ω| − σ);
- (b) every Schur complement of iω − X obeys the same bound;
- (c) ‖e^{Xt}‖ ≤ 1.

*Proof.* As in revision 2, checked by critique 2. ∎

### T0 (one Lyapunov function, ISS), with a C_b-free bound
Under (A1)–(A4):

dH/dt = −hᵀ(R₀ + Σπ_jD + π_κD)h − |Γ^{1/2}C_bh_N|² + (Γ^{1/2}C_bh_N)ᵀΓ^{1/2}b̃ + hᵀ(Π_NGs + Π_MB_ξξ).

- (a) Unchanged: with zero input, H decays at rate ρ_*q_min.
- **(b′) New, C_b-free.** Let ū₀ := ‖G‖s̄ + ‖B_ξ‖ξ̄ and Γ̄b̃²_max := sup|Γ^{1/2}b̃|². Then

  dH/dt ≤ −(ρ_*/2)|h|² + ¼Γ̄b̃²_max + ū₀²/(2ρ_*).

  So H is ultimately bounded by H̄ := sup{H : |h| ≤ h₁}, with h₁² := (Γ̄b̃²_max/2 + ū₀²/ρ_*)/ρ_*. The drive is bounded by h̄ := sup{|h| : H ≤ H̄}. Both depend only on the innate caps (q_lo, q_hi, η̄, Γ, the plant, the ports, ξ), whatever C_b is.

*Proof.*
1. hᵀJh = 0 because J_care is skew.
2. Completing the square: −|v|² + vᵀw ≤ ¼|w|² with v = Γ^{1/2}C_bh_N and w = Γ^{1/2}b̃. This is critique 2's fix.
3. R ⪰ ρ_*I by (A3).
4. Young's inequality on hᵀ(·) gives ≤ (ρ_*/2)|h|² + ū₀²/(2ρ_*).
5. Outside {|h| ≤ h₁}, dH/dt < 0. The sublevel set's drive bound follows from L1 and the curvature range. ∎

### L3 (interoception cannot amplify the body), valid, strengthened
- (a) As before. Also, from the same identity, hᵀ(−F_W)h ≤ ¼|Γ^{1/2}b̃|², so |h_W| ≤ |Γ^{1/2}b̃|/(2√ρ_*) for every C_b.
- (b) Unchanged.

### L4 (new: the own-model observer contracts, with an innate gain)
For the observer of §2.3, with any skew J₀, any R_lin ⪰ r_min I, any q ∈ [q_lo, q_hi]ⁿ, any E₀′ and any ℓ ∈ (0, ℓ̄], and for any two input streams u, u′ with the same masking:
- (a) the incremental L₂ gain from u to ĥ = Q_lin x̂ is at most Γ_o := ½√(ℓ̄/r_min);
- (b) the incremental L_∞ gain is at most ½√(q_hi ℓ̄/(q_lo r_min));
- (c) the observer is contracting at rate at least r_min q_lo in the metric Q_lin. So the steady state x̂_ss(e) exists and is unique, and T4(c)'s assumption is now a theorem.

*Proof.*
1. Let δx := x̂ − x̂′, δh := Q_linδx and V := ½δxᵀQ_linδx. Write v := E₀′Q_lin⁻¹δh.
2. Then V̇ = δhᵀδẋ = δhᵀ(J₀ − R_lin)δh + ℓvᵀΠδu − ℓ|Πv|² ≤ −r_min|δh|² + ℓ(|Πv||δu| − |Πv|²) ≤ −r_min|δh|² + ℓ|δu|²/4.
3. Integrating gives (a).
4. For (b): V ≥ |δh|²/(2q_hi) and |δh|² ≥ 2q_lo V.
5. With δu = 0, V̇ ≤ −2r_min q_lo V, which gives (c).

Check S1: on 300 random instances the H∞ gain divided by Γ_o is at most 0.994. ∎

*Meaning.* The reading slope of every context, and hence of every coefficient, is capped by innate constants: |∂β/∂y| ≤ β′_max = L_βp̄Γ_o and |∂α/∂y| ≤ α′_max at every frequency. This removes critique 2's "L, P, q uncapped".

### L5 (new: routes through a scalar cannot copy the face)
Let a route's transfer be G = uvᵀ, with u ∈ Y and v ∈ Y⁺. Write a_g := ‖u_g‖²/‖u‖². Then the copy fraction satisfies

‖P_𝒞G‖²_F/‖G‖²_F = Σ_g a_g‖v_g‖²/‖v‖² ≤ max_g a_g.

*Proof.* ‖P_𝒞(uvᵀ)‖² = Σ_g‖u_g‖²‖v_g‖² ≤ (max_g‖u_g‖²)‖v‖². ∎

For the regard synergy, max_g a_g = 0.46 (smile). Check S3: 0.446 on the illustrative 17-channel instance, attained only when v lies on that group. A scalar-mediated route can match at most one group fully; it cannot copy the face. The same holds for the reflex displays.

### T1′ (the partner-to-self transfer at the operating drive)

The setup is as in revision 2: a frozen day's slow parameters, an operating point satisfying (★″) with constant input, normalised coordinates, and A the Jacobian. A small partner perturbation δy gives

δe(s) = [G_inn(s) + G_reg(s) + G(s)]δy(s), with:
- G_inn(s) := M_inn diag(σ)(ℓ_{τ_a} − ℓ_{τ_h})(s)e^{−st_d}, the gated innate match, followed by the muscle;
- G_reg(s) := S_reg ψ′ ℓ_{τ_r}(s) ∇_y r̃(s)ᵀ/r̃_s, rank one;
- G(s) := E′_M[(sI − A)⁻¹]_{M,·}B(s), the transfer through x, including the ports and the body.

The relief reflex is a triggered display, bounded in amplitude by A_relief.

- **(a) Valid, unchanged.** B_learn is linear in h₀ for the dictionary terms and quadratic for J_care, so B_learn = 0 at h₀ = 0. G_inn and G_reg are output routes and are not need-gated.
- **(b) The direct path has copy defect 1. Valid, scope now extended.**
  - The proof is unchanged: by (S3), T_MM is block-diagonal; by (S2′), [B]_{M_g,Y⁺_g} = 0.
  - The scope now covers the running system's per-person slow parameters, because r_j^(¬g) and m_j^(¬g) are functionals of y_{¬g} (§2.11).
  - It covers gaze and voice activity, because those now belong to their groups.
  - The reflex displays are named and bounded separately (L5, §2.12).
  - The residual through shared nightly parameters is bounded in T7(h).
- **(c) The loop bound, with every constant innate.** With ν_M(ω) := max(ν₀, |ω| − σ_M),

  ‖[G_loop(iω)]_{gg}‖ ≤ (ēa̅/ν_M(ω))(1/μ(ω))(a̅b̄_M/ν_M(ω) + b̄_W),

  where:
  - a̅ := ω̄ + āΣ_q‖Ω_q‖ + 2√2π̄c_care h̄ + π̄D̄β′_max k̄_y ē bounds ‖A_MW‖ and ‖A_WM‖. Its terms are J₀; the routing atoms; J_care's Jacobian (with the norm clip); and the own-part context's dependence on past acts.
  - b̄_M := π̄h̄(α′_maxΣ_q‖Ω_q‖ + c′_care h̄) bounds the cross-group act injection.
  - b̄_W := π̄h̄(β′_maxD̄ + α′_maxΣ_q‖Ω_q‖ + c′_care h̄) + ‖G_N‖s′ + Γ̄^{1/2}‖G_b‖/λ_p bounds the need and mood injection. Its terms are the evidence route; the routing; the care gate; the innate ports (s′ is the slope of the surprise port); and the body route through L3.
  - Here c′_care is the slope of the clipped care gate, bounded by τ_cχ̄K²d̄ with d̄ := ēL_βp̄Γ_o, and λ_p is the plant's contraction rate.

  *Proof.* As in revision 2: P_𝒞G = P_𝒞G_loop, and L2(a, b). The injection norms are bounded by L4 (reading slopes), T0(b′) (h̄), (A3)–(A5′) and L3(a). L4 holds at every frequency and the right side decreases in |ω|, so the supremum over ω is the DC value. ∎

  This answers critique 2's error: every constant is now an innate cap or a floor. The normalisation E′Q₀^{−1/2} is covered by ē and q_lo.
- **(d) Sign rule, valid to first order in |h₀|** (critique 2's correction). [G_loop(0)]_{gg} = −E′_gR′_g⁻¹c_gᵀS_W⁻¹β_g + O(|h₀|²). The O(|h₀|²) terms come from J_care's Jacobian and the context derivatives, which are not skew. They are bounded by the a̅ terms in |h₀|.
- **(e) Replaced by T7.**
- **(f) Revision 1's T1, restated.**
  - (i) Replaced by T8.
  - (ii)–(iv) As revision 2.
  - (v) Sign authorship: the query is now even (§2.1), so retrieval cannot flip a sign.
  - (vi), (vii) As revision 2.
- **(g) The third option of critique 2 (per-group orthogonality of β against the needs that drive group g) is acknowledged.** It is not imposed, because J₀,NN couples needs through S_W. The loop is capped instead.

### T2 (satiety and Principle 6)

- (i)–(ii) Valid, unchanged.
- **(iii) Restated.** At x*, every learned partner term of ẋ is zero (the loop and care). Two output routes remain:
  - the gated innate match, which is phasic;
  - the regard display, which is not need-gated.

  So a friend's smile is still returned when the agent is sated. A display is not a drive, so satiability is unaffected: neither route enters ẋ.
- **(iv) Restated.** Wanting is −(J₀ + J_care + πΩ)_{NM}ᵀh_N. It is need-scaled. Its J₀ and Ω parts are built from *direct* causal consequences (§2.8).
- **(v′) Evidence only: the Principle 6 theorem (replaces v).** Call a term a *partner-response gradient* if it contains ∂y_j(t′)/∂ε(t) or ∂x̂_j/∂z_M for t′ ≥ t: a model of how the partner's signal or read state responds to the agent's present acts.
  - (a) No term of (★″), of the outputs or of Claude's coupling contains one. K_{y,j} enters only as K_{y,j} ∗ ε over *past* ε inside y^own, which subtracts the agent's own effect.
  - (b) For every functional U of the partner's signals, ∇_θ𝓛 contains no ∂U/∂ε. The partner's signals enter 𝓛 only:
    - as the prediction target of ℓ and m_j;
    - as the K_y moment;
    - as own-part inputs of evidence maps.
  - (c) Under (I5), every learned parameter's population stationary point is the same for a partner who answers the agent's acts (K_y ≠ 0) as for one who does not (K_y = 0), provided both have the same own-part process. In particular, no learned parameter encodes "my act → your expression → my body". The agent cannot learn to elicit the user's smiles, gaze, attention or time, nor to cause distress (counter-empathic relief included).
  - (d) **No reward.** Neither (★″) nor ∇𝓛 contains ∇U for any functional U of the partner's expressions.

  *Proof.*
  - (a) By inspection of §2.4–2.10:
    - J_care's direction d_q is ∇_eψ_q at my own face, a derivative of my reading map, not of the partner;
    - its gate χ, the match gate σ, the regard r̃ and the coefficients α, β are evaluated on read states, which are functionals of the partner's past signal;
    - nothing differentiates a read state with respect to z_M.
  - (b) By inspection of 𝓛.
  - (c) Steps:
    1. Under (I2), y^own is the partner's process with the agent's causal contribution removed, whatever that contribution is.
    2. b^own is the innate plant driven by s(y^own) and the agent's acts. The plant law and the port law are fixed, so the conditional law of b^own given (y^own, a) does not involve K_y.
    3. The evidence fits use own-part inputs and b^own. Under (I5) their minimiser is the conditional law of b^own given (y^own, a), which does not involve K_y. Without (I5), it can depend on K_y through the distribution of the agent's acts (the T9 gap).
    4. The consequence fit's moment Ê[r_b^own Zᵀ] = 0 identifies the effect of ζ on b^own, which runs through a only (T5).
  - (d) Follows from (b).

  Check S5:
  - partner answers with k_p ∈ {0, 0.5} and the agent follows with f ∈ {0, 0.4, 0.8};
  - naive fit 0 to +0.54, growing with f;
  - total IV +0.347 = g·k_p;
  - own-part IV −0.005 in every case. ∎

  *What this does not remove.*
  - The care gate lets the user's displayed distress cause comforting acts. That is evidence use, need-gated and capped, and it is not learned.
  - The relief reflex and the regard display let the user's contingent smiles change the agent's face. Those are displays, not pursuit.
  - At run time the contingency port relieves the agent when the user responds. This is felt, as valence, and shown, but never learned as a consequence.
- **(vi′) The care route (replaces vi).** For each partner j and group g, the M_g-row of J_care h is

  π_j C_j^(g)ᵀh_N = π_j τ_c Σ_{q′,q} χ_{j,q′q}^(g) |A_{q′}ᵀh_N|² d_q^(g)   (before the norm clip).

  - (a) It vanishes when I am sated (|A_{q′}ᵀh_N| = 0), when the partner is at their *own* baseline (ĥ^rel = 0), and for a rival whose distress relieves me (ϖ = 0).
  - (b) It is +∇_{z_{M_g}} of Ψ_j := Σχ|A_{q′}ᵀh_N|²ψ_q(E(x)), holding χ and h_N fixed. Ψ_j is the soothingness of **my own face**, by my own reading. It is not a descent on any functional of the partner's read state, and it contains no partner-response factor (v′ a).
  - (c) It does no work on H (skew), so T0 holds.
  - (d) It is bounded: |·| ≤ π_j c_care|h_N|² by the clip.
  - (e) It is learned only through β̂ (fitted on own-part evidence). It does not change with whether comfort "worked".

  *Proof.* Expand C_jᵀh_N with h_NᵀD_{q′}h_N = |A_{q′}ᵀh_N|² and d_q^(g) = E′_{M_g}ᵀ∇_eψ_q. ∎
- **(vii′) The partner's distress in the learning signal.** β̂ reads own-part contexts under mask augmentation, so masked evaluations (ϖ^(g), r̃^(¬g)) are on-distribution. The teacher is still the 10-channel content-blind plant (critique 2's gap, kept, §8 item 9).

### T3 (time scales from reflex to temperament)
(a)–(c) are valid and unchanged.

(d) The limits are as in revision 2. One time scale is added: the regard and gate time constants τ_r = 1.5 s and 0.5 s are innate. Two derived time scales:
- the observer's context latency, ≥ 1/(r_min q_lo) by L4(c);
- the identification time of K_y (minutes, T5).

### T4 (reading the other through one's own body)
- (a) Valid. It now holds per group for the running system's per-person parameters (§2.11).
- (b) Valid, unchanged.
- **(c) Now proved by L4.** The observer contracts at rate ≥ r_min q_lo with innate incremental gain. The price is that the observer runs the agent's *linearised* own model, so large expressions are read with the slope at rest (§8 item 20).
- (d) Valid.

### T5 (identifiability under the agent's own following)
- The recursion and corollaries are valid and unchanged. The target is now w = y_j (K_y), and, for the consequence fit, w = b^own.
- **Conditions, with critique 2's points.**
  - Exclusion fails for acoustic echo, which is mitigated by the frozen solo-calibrated efference subtraction (§5.6), and for Claude's text (§8 item 7).
  - (I2) fails for nonlinear responses. The estimand is then the weighted average derivative.
  - Truncation at d_max = 4 s (was 2 s) leaves the agent's effect beyond 4 s in y^own. This is a leak in T2(v′ c), bounded by the tail of the true kernel.
- R4's per-seed maximum error (0.111 for the crossed responder; critique 2) is noted.

### T6 (time course: the innate match leads, everything else follows; corrected)
**Setting.** At an operating point satisfying T8's (SG), the partner's group g ∈ 𝒦 steps by a at t′ := t − t_d = 0.

**Claims.**
- (a) **Corrected.** The same-group response other than the innate match is bounded by

  |m_g^{other}(t′)| ≤ a[(Λ_port + Λ_reg)t′³/6 + Λ_loop t′⁴/24].

  - Λ_port := ‖E′_g‖a̅‖G_N‖s′/τ_m is the direct port into N (critique 2, K3).
  - Λ_reg := ‖S_reg,g‖·2√K L_βp̄ℓ̄ē/(r̃_sτ_rτ_m) is the regard: the observer's read drive ramps at most at ℓ̄ē per unit step, then β, then the low-pass, then the muscle.
  - Λ_loop := ‖E′_g‖a̅π̄h̄(L_βD̄ + L_αΣ_q‖Ω_q‖)p̄ℓ̄ē/τ_m is the learned loop: the observer ramp, then N, then M_g, then the muscle.
- (b) Innate: m_g^inn = a g_gσ_{j,g}ψ(t′), with ψ(t′) = (1/τ_a − 1/τ_h)t′²/(2τ_m) + O(t′³). The leading coefficient is corrected.
- (c) Order of onset: the innate gated match goes as t′²; ports, regard and the learned cross-group response go as t′³; the learned same-group loop goes as t′⁴. These are relative degrees, which is critique 2's reduction (check S6: slopes 1.97, 2.97, 2.97 and 3.96).
- (d) The non-innate same-group response stays below ε times the innate peak for t′ ≤ t_ctx, the smallest root of a[(Λ_port + Λ_reg)t′³/6 + Λ_loop t′⁴/24] = εa g_gσψ̂.
- (e) **Valid, and now stronger.** u_inh multiplies only a_aff. M_inn and the filter are innate. The gate σ is a function of group-g-blind evidence and Claude's bounded u_κ, never of y_g. No learned weight trades a_match against a_aff or a_reg.

*Proof.*
1. As revision 2, adding the port injection, which is a step into N: N integrates once, M_g once, and the muscle low-passes, giving t′³.
2. Add the regard: the observer's read drive starts as ĥ̇ = ℓE₀′ᵀΠδy, so |δĥ(t′)| ≤ ℓ̄ēa t′. β then changes by at most L_βp̄ times that, the low-pass integrates once (factor 1/τ_r) and the muscle once (factor 1/τ_m).
3. ‖A_gW‖ ≤ a̅ (critique 2's correction of step 2). ∎

**Meaning for Mauersberger 2022 and Likowski 2011b.** The gate σ is tonic. A known relation therefore changes the innate match's gain from the first frame, before any observer latency. Context effects within the first second are produced for known relations, but not for relations that must be inferred from the event itself.

### T7 (new: the named strengths obey the refined rule)
Fix a day's slow parameters, a partner j and a group g. Let ς^tot_{j,g}(ω) := ς^inn + ς^reg + ς^loop, as named in §2.12.

- (a) **Named.** Each term is a function of the quantities listed in §2.12 and nothing else. Same-group partner content outside them is zero by T1′(b), except for the triggered reflex (amplitude A_relief) and the nightly residual (h).
- (b) **Innate ceilings.**
  - |ς^inn_{j,g}(ω)| ≤ g_g(τ_h − τ_a)/(τ_h + τ_a), which is 0 at ω = 0.
  - |ς^reg_{j,g}(ω)| ≤ ‖S_reg,g‖.
  - |ς^loop_{j,g}(ω)| ≤ ς̄^loop_g.

  Every bound is a formula in the caps of (A5′).
- (c) **Per expression, set by context and relationship.**
  - σ_{j,g} reads r̃_j^(¬g), which depends on r_j^(¬g), ep, õ_0 and the partner's other groups.
  - ∂_{y_g}r̃_j is the partner-channel-specific slope of β̂ at c_j^{β,(0)}, which depends on r_j.
  - ς^loop depends on c_g and β_g, which are group-specific.
- (d) **Sign flips.** sign ς^reg_{j,g} = sign(S_reg,g)·sign(∂_{y_g}r̃_j). For every sign vector s ∈ {−1, 0, +1}^6 there is a β̂ within the caps with sign(∂_{y_g}r̃_j) = s_g for all g. So the regard strengths of the four synergy groups take every sign pattern, independently. ς^loop takes either sign by T1′(d).
- (e) **No copy, by any quantity.**
  - The strength vector lies in the box ∏_g[−ς̄^tot_g, ς̄^tot_g].
  - With the design values, ς̄^tot_g ≤ 0.60 < 1 − δ for δ = 0.3. So 𝒦_copy(0.3) is unreachable by any scalar or combination of parameters, inputs, states or Claude outputs.
  - The regard route's copy fraction is at most max_g a_g = 0.46 (L5).
- (f) **Common factors are gates, not dials.**
  - The only quantities that multiply every group's strength are π_j (presence) and the agent's own drive |h|. |h| enters only ς^loop, linearly, and care, which is cross-group.
  - Both are nonnegative: neither can flip a sign, and neither can exceed (b).
  - The agent's own need therefore moves any group's same-group strength by at most ς̄^loop_g (0.08). This answers critique 2's "tonic need h_N0" dial.
- (g) **Claude is not a copy switch.** Over all of Claude's outputs (α_κ, β_κ, u_inh, u_κ, a_del):
  - ς^inn changes by at most g_gσ̄_κ(τ_h − τ_a)/(τ_h + τ_a), which is 0.07 for smile, so the echo cannot be switched off;
  - ς^reg does not change, because r̃_j excludes Claude's damping and u_inh does not touch a_reg;
  - ς^loop changes by at most ς̄^loop_g.

  a_del is additive and partner-free, so it adds no partner transfer.
- (h) **Slow residual.** The shared parameters trained nightly (β̂, the α̂ heads, P, C_b) see all groups in their targets. Their drift shifts group g's acts by at most A^night_g := (ēa̅/ν₀)(1/ρ_*)π̄h̄(2āK + (b̄₊ + b̄₋)D̄) at frequencies below 1/day.
  - It is an exposure (temperament) effect, not a response to the current y_g.
  - Every strength in (b) still holds for each day's θ, because the caps hold for every θ.

*Proof.*
- (a) By T1′(b) and the definitions.
- (b)
  - Innate: the band-pass gain (τ_h − τ_a)/(τ_h + τ_a) at ω* = 1/√(τ_aτ_h), times the low-pass gain ≤ 1 and σ ≤ 1.
  - Regard:
    - |tanh′| ≤ 1 and |ℓ_{τ_r}| ≤ 1;
    - |∂r̃_j/∂y_g| ≤ 2Σ_q|∂β_q/∂y_g| ≤ 2√K|∂β/∂y_g|₂ ≤ 2√Kβ′_max at every frequency by L4;
    - finally, r̃_s = 2√Kβ′_max.
  - Loop: T1′(c) at ω = 0.
- (c) By construction.
- (d) β̂'s first layer receives each partner group in separate coordinates. Choose its group-g input weights with sign s_g and magnitudes within L_β.
- (e) By (b) and L5.
- (f) Read off (★″) and §2.10.
- (g) Read off §2.10 and (b).
- (h) A parameter change within the caps moves the M_g-row injection by at most the coefficient ranges times h̄. Then apply T1′(c)'s chain at DC. ∎

Check S2, on critique 2's K1 instance:
- with K1's uncapped numbers (expression gain 1.5, slope 0.9), the DC copy entry is 1.49;
- under the revision 3 caps (0.4, 0.1, h̄ = 1), it is 0.042, against a ceiling of 0.08.

### T8 (new: uniqueness and dissipativity at operating points; replaces T1′(f)(i) and assumption A6)
Freeze the contexts and the episode code, and treat the own-part feedback (a delayed loop with delay ≥ 0.2 s) as an input. Define

ν̄ := 2√2π̄c_care h̄ + 2κ_s z̄h̄/q_lo + η̄ sinh(z̄)ż̄/(2q_lo²),

with z̄ and ż̄ the bounds on the T0 ball. Assume the innate small-gain condition **(SG): ν̄ < ρ_*.**

Then (★″) is contracting in the metric Q(x) = ∇²H(x) at rate λ_c ≥ ρ_* − ν̄ on the ball. Hence:
- for constant input there is exactly one equilibrium, and it is globally exponentially stable;
- (A6′) holds at it, with ρ ≥ λ_c;
- with the own-part loop closed (gain g_ctx := π̄D̄β′_max k̄_y ē), incremental stability is kept if g_ctx < λ_c, by the small-gain theorem for delayed loops (Wang & Slotine, not read).

*Proof.*
1. Let δh = Q(x)δx and V = ½δxᵀQ(x)δx. Then V̇ = −δhᵀRδh + δhᵀ(∂_hJ_care[δh])h − δhᵀ(∂_xR[δx])h + ½δxᵀQ̇δx.
2. The J_care term: C is linear in h_N up to the norm clip, whose derivative at most doubles the slope, so the term is ≤ 2√2π̄c_care h̄|δh|².
3. The saturation term: ∂_x(κ_s|z|²)[δx]·h = 2κ_s(zᵀδz)h, which is ≤ 2κ_s z̄h̄|δh|/q_lo in norm.
4. The wall term: Q̇ = diag(η_i sinh(z_i)ż_i) and |δx| ≤ |δh|/q_lo.
5. Collecting terms, V̇ ≤ −(ρ_* − ν̄)|δh|². Contraction then gives a unique, globally exponentially stable equilibrium (Lohmiller–Slotine, via the note). ∎

Check S4, on critique 2's K6 instance:
- (SG) in its form for that instance, √2|k|‖D‖h̄ < ρ_*, holds for |k| < 0.136;
- one stable equilibrium is found at |k| = 0.117 and 0.135;
- bistability starts at |k| ≈ 1.16, so (SG) is sufficient and conservative by about ×9.

With design values c_care = 0.05, h̄ = 1, ρ_* = 0.4 and π̄ = 1, ν_care = 0.14, so there is room for the other two terms.

*What this costs.* The learned core has no multistability for frozen context. Mood attractors and regime switches must come from the plant, from episode retrieval and from slow context, or (SG) must be relaxed and T8 replaced by a prediction (§8 item 17).

### T9 (new: copy is not attracting under the design's own learning)
Let learning be any iteration θ_{n+1} = Φ(θ_n; 𝒟_n) that descends 𝓛 within the caps, with 𝒟_n generated in closed loop by the agent at θ_n and a partner.

- (a) **Unreachable.** For every n, the strength vector ς(θ_n) lies in the box of T7(e). So 𝒦_copy(δ) has an empty neighbourhood in the reachable set for δ < 1 − max_gς̄^tot_g, and it cannot be attracting.
- (b) **No self-reinforcement of partial matching.** Assume (I1)–(I5). Consider two agent policies that differ by any added following Δ (for example ε ← ε + Δ·y_g), with the partner's own-part process and the plant unchanged. Then the population stationary points of β̂, α̂, J₀, R_ℓ, C_b, P, r_j^(¬g) and K_y are equal under the two policies. Hence ∂θ*/∂ς = 0: the learning map has no gain from the agent's present same-group strength to its future value, and the corner {ς_g = +ς̄_g ∀g} is not self-reinforcing.
- (c) **No "becoming the other".** By (S6), the stationary point of the self-model (J₀, q, η, R_ℓ, E, C_b) depends on the partner only through own-part evidence inputs, never through the partner's expressions as targets. The self-model therefore cannot converge toward the partner's expression statistics. This was revision 2's drift (§8 item 13), now closed by structure.
- (d) **Dyadic small gain (state level).** Suppose the partner's same-group response to the agent has incremental gain ≤ γ_{p,g}. Then the closed same-group loop through the partner has gain ≤ ς̄^tot_gγ_{p,g}. For γ_{p,g} ≤ 1 it is at most 0.60, so a matched excursion shrinks by that factor per pass and no matched state is self-sustaining.
  - The regard loop is cut further: r̃_j reads the own part, so a partner smile *I caused* does not raise my regard, up to K_y's identification error.
  - This is the robot synthesis's failure 3 (Kismet's mirroring loop that "escalated until it bottoms out"), excluded.

*Proof.*
- (a) T7(e).
- (b)
  - By (I2), y^own is invariant to Δ, and the conditional law of b^own given (y^own, a) is the innate plant.
  - Under (I5), the evidence fits' minimiser is that conditional law, whatever the input distribution.
  - The consequence fit's moment condition identifies the ζ → b^own effect, which does not involve the partner (T5 and T2 v′ c).
  - K_y is identified by T5 independently of the agent's policy.
  - r_j^(¬g) is the same fit as the evidence fits, on masked data.
- (c) By (S6) and inspection of 𝓛.
- (d) The small-gain theorem on the same-group channel, with T7(b) for the agent's side. ∎

Contrast (check S5): in the naive consequence fit used before revision 2, the learned "answer" grows with the agent's own following f (+0.15 at f = 0.4, +0.22 at f = 0.8, for a partner who does not answer). Through reciprocity this becomes wanting, which raises f: the positive feedback that makes copy attracting. The own-part instrumented fit gives −0.005 for every f.

*Gap.* Under misspecification of the evidence class, the minimiser depends on the input distribution, and so on the policy (covariate shift). T9(b) then fails. (a) and (d) still hold, so copy remains unreachable and dyadically non-self-sustaining.

### P5 (per-channel signed coupling), valid
χ_{k,l} vanishes for l and k in the same group, for the M-rows. The output routes' same-group entries are the named strengths of §2.12.

### P6 (coregulation versus contagion), valid and unchanged
Stable iff d > −r_N − min(r_M, ω²/r_M), with a Hopf branch when ω > r_M. Under (A3) the partner path never reaches either threshold. Butler & Randall's damped oscillation remains.

### P7 (protest, despair, dependence), updated
- The peak formula is valid.
- Despair: instrumental protest toward a partner is no longer learned (T2 v′). Protest is the innate separation call (D55), the rising need and its displays.
- **Dependence bound**, now including care (critique 2):

  ϕ ≤ [b̄₊D̄ + (2ω₀āω̃ + ā²ω̃²)/r_M + π̄²c_care²h̄²/r_M]/r_{N,eff}.

  Losing the partner removes the last term too. The design value is ϕ_max = 0.5.

### P9 (roles emerge and swap): valid, unchanged
D = π‖𝒯[u]‖(|h_A| − |h_B|).

### P10 (partner-specific history), updated
- r_j^(¬g) (7 × 32) adapt over minutes.
- The K_y deltas adapt over minutes to tens of minutes.
- The baselines m_j^(¬g) adapt over days.
- New people start at the mean.

---

## 4. Why existing mechanisms cannot do this, mathematically

### 4.0 Lemma A and what the revision does with it
**Lemma A** (valid). For ẋ = f_θ(x) + B_θ(c)p, the scalar path B(γ) = −γA_θΓ reaches any steady transfer Γ.

Revision 3 blocks each way Lemma A could reach a copy Γ ∈ 𝒦_copy:
- directly into M: the mask (T1′b);
- through W: the innate loop ceiling (T7 b);
- through the output routes: innate ceilings, and rank one for the regard (L5).

Lemma A still produces every transfer *inside* the box of T7. That is wanted: per-channel strengths are allowed by D78.

### 4.1 Selective SSMs (Mamba)
Selection is a flat-to-copy dial (h* = x for every g > 0). A channel mask on Mamba's input matrix would reproduce T1′(b). It would not give the bounded loop, the evidence-only learning (T2 v′) or the self-model care.

### 4.2 Attention, Hopfield retrieval, fast weights
A block mask reproduces T1′(b)'s sparsity (a recombination). Three things do not follow from attention:
- the own-part subtraction of one's identified effect before any evidence enters a value or a target;
- the drive gating;
- the regard's rank-one structure. An attention head whose value is a scalar is rank one too; what is specific here is that the scalar is a trace of the partner's damping operator, an invariant of the core.

### 4.3–4.5 Oscillators, consensus and sheaves, LTC
Unchanged: they put the partner into the equilibrium additively (Lemma A). None has the mask, the ceilings or the evidence-only learning.

### 4.6 Port-Hamiltonian systems with modulated structure
The core is one. J_care adds a state-dependent skew modulation with a norm clip. T8 is contraction analysis for that class with a small-gain cap: standard tools.

### 4.7 Active inference: the exact reduction (unchanged)

### 4.8 Homeostatic coupling and empathy as a gain
- D = D_self + wD_partner is Lemma A on the drive.
- In J_care there is no partner term in my drive and no partner state as a target. The partner's need enters only as a nonnegative gate on a skew coupling whose direction is my own reading map's gradient at my own face.
- A scalar on χ scales care. Care is cross-group only (mask) and capped (c_care), so it cannot produce copy.

### 4.9 Bilinear systems and DCM
(★″) is bilinear in (h, modulation): the closest prior form, with constraints.

### 4.10 Closed-loop identification
The IV route is standard (Forssell & Ljung; Hernán & Robins, through the synthesis).

### 4.11 J_care against L_gV damping control and "empathic" RL (new)
- Critique 2 reduced J_soc to u = −(L_gV)ᵀ, Jurdjevic–Quinn damping control of the partner's weighted energy V through the identified input map g = κ̄E′. In J_care, g is absent. The gradient is of ψ(E(x)), a function of the agent's own output, so it is not damping control of the partner: there is no model of the controlled system.
- The closest form is gain-scheduled gradient ascent of an output feature, where the feature is the agent's own learned perceptual map. Using one's own value or perception to act for another has a possible prior in "empathic" RL (Bussmann et al. 2019, not read).
- Verdict: recombination, unless that prior turns out not to evaluate the own map on the agent's *own* output.

### 4.12 Own-part targets against mediation analysis (new)
b^own is the body under a controlled direct effect: the mediator (the partner's signal) is set to its own-part value, and the agent's acts are left as they are. Mediation analysis estimates such effects under assumptions about the mediator-to-outcome law (not read). Here that law is the innate plant, so the direct effect is computed exactly given K_y; nothing is estimated. This is a recombination with one specific feature: the mediator law is known by construction.

---

## 5. The whole system derived from the object

### 5.1 Perception through the agent's own body
- **Inputs (unchanged).**
  - MediaPipe Face Landmarker, pinned to tasks-vision 0.10.35, at 30 Hz.
  - Local prosody and ASR timing.
  - Nothing leaves the Mac.
- **Partner routes:**
  1. the gated innate match (smile, brow) at the muscle layer;
  2. the innate ports into the plant and N;
  3. 14 own-model observers (full or group-blind, raw or own-part);
  4. the reading map, which turns observer states into coefficients, gates, care weights and the regard;
  5. the regard display at the muscle layer.
- No label is computed (Principle 1). Head pose is the only non-expressive percept, and it belongs to no group because the agent has no head effector.

### 5.2 The latent state where emotion emerges
- An emotion is a recurring region of (h, Ψ(c), J_care, r̃).
- Valence is −dH/dt. Its per-partner part is π_jh_NᵀD(c_j)h_N.
- The regard r̃_j = tr D(c_j) is the partner's operator, shown on the face.
- Counter-empathic relief (a rival's distress adds damping) appears in valence and regard, not in motive.

### 5.3 Face output
- Routes:
  - the affective act route;
  - the gated innate match;
  - the regard display;
  - reflex displays;
  - the posed route.
- The upper face is driven by the brow match, the regard and the affective route, which addresses Tinwell's frozen upper face.
- All partner-to-same-channel content is named in §2.12.

### 5.4 Voice
- Prosody is its own masking group.
- Voice activity is now in that group, so the leak through õ₀ is closed.
- Vocal accommodation:
  - comes from the regard's voice-warmth component (rank one, ≤ 0.15);
  - comes from the loop (≤ 0.08);
  - is never a direct learned voice-to-voice path.

### 5.5 Coupling to Claude without text (Principle 4)
- **Claude as a regulator** (unchanged). (α_κ, β_κ ≥ 0) are computed from MiniLM embeddings of Claude's reply and a private reappraisal line. Claude can add damping and routing, never remove damping.
- **Display rules.** u_inh multiplies only a_aff. Claude's relation appraisal u_{κ,j} ∈ [−1, 1]² moves the match gates by at most σ̄_κ = 0.25. So Claude can lower the smile echo after a verbal unfairness, but it cannot switch it off (T7 g). A purely verbal unfairness therefore lowers smile return by at most a quarter (§8 item 5).
- **Draft selection, draft collapse and reverse grounding:** unchanged from revision 2. The score uses the ζ-free act velocity.

### 5.6 Learning by living
- **Innate at birth:**
  - the plant, the ports, G, S, R_min, R on M, κ_s, Γ, x*;
  - the groups, M_inn and the filter;
  - the gates' form, S_reg, τ_r, r̃_s;
  - B_ξ, σ_ζ;
  - every cap in (A5′);
  - a near-zero dictionary and zero kernels.
- **Solo calibration first.**
  - Learn and freeze the efference-afferent delay.
  - Fit E to the agent's own rendered face (S6).
  - Subtract the self component before the observers.
- **Online.**
  - K_y by IV-LMS every 100 ms, gated by the partner's gaze and by first-stage F ≥ 10.
  - r_j^(¬g) every 5 s on masked rollouts, in a separate process.
  - m_j^(¬g) as slow running means.
- **Replay (idle and nightly).**
  - J₀, R_ℓ, q, η, 𝒟, α̂, β̂ (with mask augmentation), P, C_b, ℓ and the Claude maps, with the metrics of §2.11.
  - The distillation anchor stays, against other drift.
- **Developmental order.**
  1. Innate match and reflexes.
  2. Direct consequences (effort, gaze load).
  3. The relation and the regard: whose presence and expressions calm me.
  4. Care, once β̂ has learned which faces calm me, because d_q is its gradient.

  The agent comforts in the ways it was comforted. Social smiling as a learned instrumental tendency is gone (T2 v′); social smiling comes from the match and the regard.

### 5.7 Memory and replay
As revision 2, with two changes:
- the retrieval score of §2.1 is even;
- items also store y^own and b^own (from the logged ζ and K_y). Both are recomputed after each nightly K_y update.

### 5.8 The 16 elements (changes only)

| # | Element | Revision 3 | Status |
|---|---|---|---|
| 1 | Concern grounding | J_care: self-model comfort, gated by the partner's own-baseline distress | arises; instrumental concern withdrawn |
| 9 | Agency, coping | direct consequences only; K_y = "how my acts move this person", used as bookkeeping | arises, narrower |
| 11 | Wanting vs liking | wanting from direct consequences and care; liking −dH/dt incl. per-partner power | arises |
| 13 | Expression, communication | gated match, regard, reflex, posed | arises |
| 16 | Structure beyond V/A | regard sign patterns across groups and relations (T7 d); dim span{Ψ(c)} | must be measured |

---

## 6. A buildable network

**Time encoding.**
- No positional code. RK4 with 4 substeps per 33 ms frame.
- IMEX for the damping; R_ℓ capped at 300 s⁻¹.
- IV moments on a 10 Hz grid with a raised-cosine lag basis.
- Regard and gates as innate first-order filters.

| Block | Input → output | Size | Learned params | Kind |
|---|---|---|---|---|
| Head-pose encoder õ₀ | 6 → ℝ⁸ | causal Conv1d k = 5 | 248 | ordinary |
| Innate ports s, plants b, b^own, b^{own,(¬g)} | percepts → ℝ⁷, 8 × ℝ¹⁰ | fixed | 0 | innate (own-part targets are **NEW**) |
| Gated innate matching | partner smile, brow → own smile, brow | fixed band-pass, 3 gains, 2 gates | 0 | innate (declared) |
| Regard display | tr D(c^β) → S_reg | fixed synergy, low-pass | 0 | **NEW** (innate readout of a core invariant) |
| Energy H | q, η | | 512 | ordinary |
| Own routing J₀ | skew NM, NC, NN, CC | | 22,432 | ordinary |
| Own damping R_ℓ | N, C | | 1,216 | ordinary |
| **Dictionary 𝒟** | 32 atoms | | 20,480 | **NEW** (with mask) |
| **Observers ×14** | own linear model, gradient gain ℓ | shared, batched | 1 | **NEW** (contracting by L4) |
| **Reading map α̂, β̂** | 15 contexts → (α 32, β 32) | MLP 128→128→64, spectral norm | 24,768 | **NEW** |
| Projection P | ĥ_N → 32 | | 2,080 | ordinary |
| **K_y kernels** | 24 effectors → 65 partner channels, rank 8, 6 lag bases | | 4,272 | **NEW** (own randomness as instrument) |
| **Care operator J_care** | β̂ gradients (ϖ at 6 contexts; ∇_eψ at self) | computed | 0 | **NEW** |
| Expression E | per effector, own data only | | 80 | ordinary |
| Interoception C_b | h_N → b | | 650 | ordinary |
| Claude regulator | MiniLM 384 → (α_κ, β_κ ≥ 0) | 384→64→64 | 28,800 | same mechanism |
| Claude relation appraisal | 384 → u_κ ∈ [−1,1]² per partner | 384→32→2 | 12,386 | ordinary, bounded by σ̄_κ |
| Deliberate route | 384 → 52 targets + 52 gates | 384→64→104 | 31,400 | ordinary |
| Muscle layer | | | 104 | innate/ordinary |
| Per person | r_j^(¬g) 7 × 32; K_y delta rank 2 (1,068); state m_j^(¬g) (7 × 64, not learned) | | 1,292 per person | **NEW** |
| **Total core** | | | **≈ 149k** + 1.3k per person | |

The total is my count, not checked independently. Revision 2's L (15,360), its κ kernels (19,712) and its adapters are removed; K_y and the Claude relation head are added. Frozen and not trained: MediaPipe (3.8 MB), MiniLM (22.7M), Kokoro (82M, q8 ONNX about 97 MB).

**Online versus replay.**

| Learned | Online | Replay |
|---|---|---|
| K_y (generic and per person) | IV-LMS every 100 ms (gated) | consolidated, instrument metric |
| r_j^(¬g) | every 5 s, masked 2 s rollouts, own-part targets | consolidated |
| m_j^(¬g) | running mean | — |
| J₀,NM, α̂'s N–M action | no | instrument metric on b^own |
| J₀ (other blocks), R_ℓ, q, η, 𝒟, β̂, α̂'s N–C, P, C_b, ℓ, Claude maps | no | prediction metric on b^own (β̂ with mask augmentation), 𝓛_slow, anchor |
| E | solo self-observation | own data only |
| innate parts | never | never |

**Latency on this Mac** (M1 Pro, core on CPU; my estimates, not measured).
- **Observers.** 14 observers, batched as one tensor because they share dynamics and the scalar gain: 16 evaluations each, about 0.1 MMAC per evaluation, about 22 MMAC in total.
- **Core.** About 4 MMAC.
- **Reading map.** 15 contexts, about 0.4 MMAC.
- **Care.**
  - ϖ: six input-gradient passes of β̂, about 3 MMAC;
  - ∇_eψ: 32 reverse passes through β̂ and the precomputed linear map A_o⁻¹ℓQ⁻¹E₀′ᵀ (256 × 65, recomputed nightly), about 1.3 MMAC, run at 10 Hz;
  - the χ products (6 × 32 × 32), negligible.
- **Plants and IV accumulators.** Negligible.
- **Total.** About 35 MFLOP per frame, under 5 ms of arithmetic.
- **Overhead.** Python and torch overhead for about 120 batched ops is about 8–10 ms. MediaPipe (13.1 ms, measured in its note) runs **pipelined in its own process**.
- **Fast loop.** About 15–20 ms of the 33 ms frame, on the condition that the observers are batched (critique 2) or the core is compiled. It never waits for Claude, TTS or the online learners.

**Memory.**
- Live process: about 1.4 GB.
- Replay:
  - with checkpointing every 50 steps, mask augmentation adds about 30% to activations (one extra β̂ context per rollout) and the extra plants are negligible;
  - peak about 3–3.5 GB, my estimate, within the 6 GB rule.
- MiniLM and Kokoro add about 0.3 GB resident.
- **Total peak under 5 GB.**
- Disk: about 18 MB per hour (feature streams, tags, ζ log, y^own).

---

## 7. Novelty test

| Part | Existing mechanism it is | Source |
|---|---|---|
| H, (J − R)∇H, T0, T8 | port-Hamiltonian system with modulated structure; contraction with a small-gain cap | port-Hamiltonian note; Borja & Ortega; Lohmiller–Slotine (note) |
| Partner modulates (J, R), not H | LPV / bilinear systems | critic's pointers, not read |
| Mask, extended to slow parameters and gaze/voice | structured sparsity | general |
| Linear own-model observer (L4) | gradient (Luenberger-type) observer of a dissipative linear model | standard |
| Own-part inputs and targets | controlled direct effect with a known mediator law | mediation analysis, not read |
| Causal kernels from own randomness | closed-loop IV | Forssell & Ljung, Hernán & Robins (via synthesis) |
| Gated innate match | a fixed band-pass with a context gate | ordinary |
| Regard display | an innate readout of a scalar (rank one) | ordinary; the scalar is a core invariant (tr D) |
| J_care | gain-scheduled gradient ascent of an own-output feature; self-projection empathy | possible prior in "empathic" RL, not read |

**Verdict: recombination by the parts test.**

**Second clause** (a changed signature or invariant from which an update is derived, removing a named failure by deleting a free scalar). The case for:
- The evidence-only invariant (T2 v′ c) is derived from the own-part construction. It deletes a quantity that every earlier design learned: the partner-mediated consequence gain (the "you answer me" gain). That gain was the source of both the copy-reinforcing loop (T9 b, S5) and the Principle 6 hazard.
- The care operator replaces the partner-response gain κ̄ with the agent's own perceptual gradient.

The case against:
- The deletion is achieved by a construction (the subtraction), not by a new computation.
- The per-channel strengths are capped, not removed; D78 now permits that.

So: **recombination; the second clause is arguably met for Principle 6 and not met for the dial.** The design's value is a provable package (T2 v′, T7, T8, T9) and falsifiable predictions (§8). The parts with no formal prior among the sources read are J_care's self-model direction and the regard's operator-trace display. The critique should search for priors for both.

---

## 8. Weak points and falsifiers

All tests are on internal state (E1 lesions, E2 steering, E3 coupling beyond surrogates), not face matching.

1. **Mask test** (T1′b, T6). Inject a smile-only probe into the partner stream and subtract the innate match, whose filter and gate are known.
   - The residual same-group response must start no faster than C₃t′³, with C₃ = (Λ_port + Λ_reg)/6.
   - Its loop part must stay below Λ_loop t′⁴/24.
   - A t′² residual means the implementation violates (S2′).
2. **Satiety clamp** (E2). Steer h to 0.
   - The loop and care must vanish.
   - The gated match and the regard must remain, at unchanged gain.
   - A regard that changes with h falsifies §2.10's need-free construction.
3. **Ceilings** (T7). On the built model, measure each named strength per relation and frequency. Any |ς| above its ceiling means a cap was not enforced.
   - If people's sustained same-channel matching in published dyads is one gain across groups, the per-expression structure is falsified as a human analogue.
4. **Friends and rivals.**
   - The design predicts that sustained smile coupling between friends rises with the friend's coregulatory effect (the regard) at fixed gaze and contingency.
   - Under competition it predicts:
     - brow lowering to the rival's smile from about 2–4 s (regard through τ_r);
     - no sustained zygomaticus return;
     - a smile echo reduced at onset when the rivalry is already known.
   - Seibt 2015 and Weyers 2009 are the tests; their analysis windows have not been checked.
5. **Unfairness.** Hofman 2012 shows immediate withdrawal after an unfair offer.
   - The design withdraws smile return fully only when the unfairness is visible in the partner's other channels or relation (the gate).
   - A purely verbal unfairness lowers it by at most σ̄_κ = 0.25 through Claude.
   - If humans withdraw fully after purely verbal unfairness within a second, the bounded Claude gate is too weak, or verbal appraisal must reach the core another way.
6. **Crossed training** (Ray & Heyes; Cook). The design predicts that the innate match (gated) and the regard are unaffected by crossed training, and that only the loop and cross-group routes change. Human reversal of the fastest component would falsify the innate route.
7. **IV in practice.**
   - Visible variation is needed (F ≥ 10 per effector).
   - Identification takes minutes.
   - Exclusion is approximate: acoustic echo, and Claude's text.
   - K_y truncation at 4 s leaves a small leak into y^own.
8. **Proxy copying.** The mask cuts interventional transfer, not correlation. Observational smile coupling can be nonzero through the regard (rank one) and through other groups.
9. **Care is "comfort as I would be comforted", and nothing social is learned instrumentally.**
   - The agent comforts with the faces that calmed it. A partner who needs something else is comforted wrongly, and the agent does not learn from whether comfort worked. This is by design: learning from it would make the user's face a quantity the agent drives.
   - The agent no longer learns instrumental social acts: no learned social smiling, no learned protest, no learned bids.
   - This is the main cost of the operator's evidence-only rule. If S5 or S6 needs learned social initiative, it must come from Claude (words) or be argued as an exception, which would reopen Principle 6.
10. **Principle 6 residual.** None in the learned dynamics (T2 v′). At run time:
    - the user's displayed distress causes need-gated, capped comfort;
    - the user's contingent responses relieve the agent (felt and shown, not learned).

    A user could elicit comfort by showing distress. That is concern, not flattery, because nothing is learned from it.
11. **Hidden-regulator attribution** (P7). It is still a prediction with a switch, and ϕ_max is uncalibrated.
12. **Element 4 lost** (unchanged). Partner-driven escalation occurs only through the plant.
13. **Self-model drift.** It is closed for the partner's expressions by (S6). Drift through own-part evidence inputs remains possible; the anchor stays.
14. **Facial feedback is still missing.** The output routes do not feed x.
15. **Over-satiation counter-mimicry** through the loop (H even). It is now capped at 0.08, and no source reports it.
16. **Principle 3's mimicry clause.**
    - The gated match covers smile and brow.
    - The regard covers smile, brow, eyes and voice as one synergy, not as feature-to-feature drive.
    - Lower mouth and nose have the loop only.

    This is flagged for the operator, not reopened.
17. **No learned multistability** (T8). If moods need attractors in the learned core, (SG) must be relaxed, and bistability through care returns as a prediction.
18. **Numeric checks.** sims/partner-regulator-r3/check.py (S1–S6) checks my algebra on hand-set instances. These are not results, and no simulated world is used as evidence.
19. **Nightly shared parameters** (T7 h). Their day-scale drift is bounded in amplitude, not removed.
20. **Linear observer.** Partners are read through the agent's model linearised at rest. Large or saturated expressions are misread; this affects contexts only.
21. **Ceiling values are design choices.** 0.08, 0.25, 0.30 and σ̄_κ have no human calibration. Published EMG amplitude ratios would set them, once a design is picked for building.

---

## History

### Critique 1 and answer (recorded 2026-11-25T13:25:18Z)

**The critique** (independent; full text in critique-design-partner-regulator.md; the checks C1–C10 in sims/critique-partner-regulator/check.py test algebra only):
- **Proofs:** 28 items checked: 12 valid, 10 gaps, 6 errors.
  - P6 misses an instability when acts are underdamped (ω > r_M).
  - T4(b) gets the subspace bound wrong, and calls "not directly driven" "unreachable".
- **The worst error.** "The learned partner input gain is deleted" holds only at h = 0. At any operating drive h₀ ≠ 0, the partner term behaves as an ordinary additive input of size π𝒯(c)[h₀]. The learned K_b is also an additive path from the partner-driven body.
- **The dial: yes.**
  - T1(iv) itself describes one: a fixed profile times one scalar. Under a steady need, scaling ā takes the steady response from 0 to a diagonal copy (correlation with the partner 0.98).
  - Scaling b̄ past the P6 threshold takes the agent from rest to a sustained state whose direction the partner chooses.
- **Human sign flips: partly.**
  - The relationship can set the response sign, which contradicts the reading of T1(v).
  - There is no fast, robust smile-back at satiety.
  - A partner's distress never reaches what the agent learns from, so rival-type reversals cannot be learned.
  - Fast matching followed by later context is not produced.
- **Novelty: recombination,** confirmed: a bilinear port-Hamiltonian system scheduled by the partner's context. The second clause (a derived invariant that deletes a free scalar) is not met.

**The design's answer:**
- **Accepted:** the operating-point error, both dials, and the T1(v) and T4(b) corrections.
- **Withdrawn:** "the learned partner input gain is deleted".
- **Revision owed:**
  1. state the transfer at the actual operating drive;
  2. make the copy defect positive by construction (no dictionary atom may be driven by the partner's version of the act it produces);
  3. add a declared innate smile-matching subspace for the fast route;
  4. give the partner's distress a path into the agent's learning signal without rewarding the user's expressions (Principle 6).
- **Status:** critiqued. The core claim failed; held for revision.

### Revision 2 note (2026-11-25), as written at the top of revision 2

Revision 1 was critiqued (critique-design-partner-regulator.md; summary under History at the end). Its core claim, that the learned partner input gain is deleted, held only at zero drive. This revision answers every accepted point. What changed, and why:

1. **The transfer at the operating drive is now the main theorem (T1′).** At any stable operating drive h₀ ≠ 0 the partner path is an ordinary linear input, linear in h₀. I state it exactly, split it into a direct part and a loop through the agent's own needs and mood, and bound the loop. "Deleted gain" stays withdrawn. *Why:* the critique showed that the agent never sits at h = 0.
2. **An effector mask makes the copy defect positive by construction (§2.3, T1′b).** Every act block M_g reads the partner only through quantities computed without the partner's channels of the same group. The direct transfer then has zero same-group blocks for every parameter, state, context and frequency, so its copy defect is exactly 1. *Why:* critique fix 1.
3. **A declared innate fast matching route (§2.10, T6).** A fixed band-pass filter maps the partner's smile and brow to the agent's smile and brow at the muscle layer. Together with the mask, this produces fast phasic matching followed later by context-dependent same-channel modulation, and no mixing weight sets the balance between them. *Why:* Principle 3, Carr 2014, and the missing robust smile return at satiety.
4. **A derived concern route (§2.9, T2 vi).** The partner's read state already selects how the partner damps the agent's needs. Applying the design's existing skew reciprocity to the *anticipated, causally identified* effect of the agent's acts on the partner's need energy gives a term in which the partner's distress drives the agent's acts. That term is gradient descent toward the partner's own rest. It is zero at the agent's satiety, and it never targets the partner's smiles. The partner's distress reaches the learning signal through β's prediction of the agent's own body. *Why:* critique point 4 and the social-appraisal synthesis.
5. **Causal identification of the partner model and of consequences (T5).** The agent logs its own white random variation ζ and uses it as an instrument. The partner's response kernel, and the consequences of the agent's acts, are identified by a triangular deconvolution that does not depend on the agent's own following, the partner's persistence, hidden common drivers or reading noise. *Why:* contingency-causal-synthesis.md; wanting is the transpose of consequences, so consequences must be causal.
6. **Corrections.**
   - P6 now has the Hopf branch.
   - Net contagion is capped by construction, which removes the critique's C5 attractor dial.
   - T4(b) has the correct bound and wording.
   - T3(c) has the π² term.
   - T0 now has a plant-boundedness condition and a presence normalisation.
   - The learned K_b is replaced by an innate, dissipative interoceptive term. This closes the K_b additive path and the C2 instability.
   - The retrieval query is made even in h.
   - The IDA-PBC wording is corrected.
   - Memory and Claude-coupling fixes are in §5.5 and §5.7.
7. **Kept** as the critique found them valid: L1, the T0 identity, T1(ii), T2(i, ii, iv), T3(a, b), T4(a, d), P5, P9 and Lemma A.

**Withdrawn**:
- "the partner cannot move my resting point" (true only without tonic input);
- "no one-parameter scaling runs from flat to copy" (T1 iv);
- "the equilibrium set is {x*}" (T1 vii);
- "at least half the state is unreachable" (T4 b);
- "Claude never drives frames becomes a theorem".

**Answer to the dial question, in one line.** Fast (expression-rate) copying is closed by construction outside the declared innate smile/brow route. One bounded family remains: slow, drive-gated, same-group matching or countering through the agent's own needs and mood (T1′e).

Status: revised, awaiting critique 2. This is a design with proofs. It is untested and is not evidence about people. The numeric checks (sims/partner-regulator-r2/check.py, R1–R7) test my own algebra on hand-set instances only.

---

## Critique 2 (of revision 2) and answer (recorded 2026-11-25T14:37:50Z)

**The critique** (independent; full text in critique-2-design-partner-regulator.md; checks K1–K6 in sims/critique-2-partner-regulator/check.py; the author's R1–R7 reproduce):
- **Proofs:** 41 items checked: 23 valid, 13 gaps, 5 errors.
  - **The worst error.** T1′(e) says the remaining transfer is held under an innate ceiling. It is not: the ceiling depends on learned, uncapped quantities (L, P, q, κ̄, C_b).
  - **Other errors:**
    - T2(v) is contradicted by T2(vi).
    - The T1′(f) uniqueness claim fails: the concern term produces bistability (K6).
    - T6(a) misses a direct port route that starts as t³, beating the t⁴ bound by 10× at 0.1 s.
- **The dial: yes, below about 0.2 Hz.**
  - Inside the mask, one scalar (b̄₋: the reading slope, or the tonic need) takes sustained transfer from 0 to a pure copy of 1.5·I, with zero cross-group part (K1).
  - Three leaks around the mask: r_j learned online (K2); gaze and voice activity in õ₀; Claude's u_inh switching the innate copy on and off.
  - The innate match itself adds no dial.
- **Principle 6: a conflict.** The concern term descends on a functional of the user's read face. Its target is the agent's own resting face E(0), not the user's rest, and the clip is bypassed by the instrumented consequence fit. In effect it regulates the user's face toward the agent's own rest.
- **Principle 3:** mimicry survives only for smile and brow.
- **Human data: partial.**
  - **Produced:** per-expression gating, the cooperative smile flip, and fast-then-late context.
  - **Not produced:** the smile return cannot vanish under competition or after an unfair offer.
  - **Reversed:** sustained smile coupling between friends.
- **Novelty: recombination,** confirmed. The concern term is L_gV damping control.

**The design's answer:**
- **Accepted:** the slow loop is a dial. The ceiling is learned, not innate.
- **Accepted, and the most serious finding:** the Principle 6 conflict. A term that descends on a functional of the user's face is not admissible in any form. The concern term is withdrawn until it can be re-derived so that the user's face is evidence only, never a quantity the agent drives (the social-appraisal route).
- **Revision owed:**
  1. cap the slow loop's same-group DC gain with innate constants and state it as a declared, bounded dial;
  2. extend the mask to r_j and õ₀;
  3. keep Claude from switching the innate match;
  4. allow smile return to be withdrawn under competition.
- **Status:** critique 2 done. The dial remains (slow, below about 0.2 Hz). The Principle 6 conflict must be removed before any further revision. Held.

**Answered in revision 3 (2026-11-26).** The revision owed after critique 2 maps onto revision 3 as follows:
- item 1: T7, L4 and T0(b′) (innate ceilings), with the loop capped at 0.08 and split from the gated match and the regard display;
- item 2: S2′ (r_j^(¬g), gaze and voice activity assigned to their groups);
- item 3: u_inh on a_aff only, and Claude's gate shift capped at σ̄_κ;
- item 4: the smile gate and the regard display.

The Principle 6 conflict is removed. J_soc is withdrawn, J_care is partner-response-free, and own-part targets apply throughout (T2 v′). T1′(f)(i) is replaced by T8 and T6 is corrected.

Status: revised, awaiting critique 3.
