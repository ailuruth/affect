# Critique 2: Partner as learned regulator, revision 2 (design-partner-regulator.md)

Independent critic, 2026-11-25, written under questions.md Q16 and Q17. I did not write the design and did not see its author's reasoning. Nothing was downloaded. No data and no weights.

**Summary verdict.**
- **Proofs.** 41 items checked: 23 valid, 13 with a gap, 5 with an error.
- **The worst error.** T1′(e) claims that the family left after the mask is bounded by a ceiling Ē(ω) built from innate caps. It is not. Ē contains learned, uncapped quantities: the observer gain L, the projection P, the energy curvature q, the kernels κ̄ and C_b. And within the caps that do exist, the family reaches an order-one **pure** copy at DC. In K1, under (A3) and the mask, one scalar runs the sustained transfer from 0 to 1.5·I, with exactly zero cross-group part. The copy defect of the *total* transfer is then 0, not 1.
- **The dial.** Yes, below about 0.2 Hz, which is the level of sustained expression. The knobs are the contagion range b̄₋, the reading slope (through P or L) and the tonic drive |h₀|. Three further leaks:
  - online r_j and adapters carry the partner's same group (K2);
  - õ₀ re-encodes gaze and voice activity, which the eyes and voice groups own;
  - Claude's u_inh gates the innate copy from on to off.
  A new hazard: the concern operator makes the operating point bistable under (A2)–(A3) (K6), so the critique-1 C5 attractor returns through J_soc.
- **Principles.** T2(v) ("no ∇U of the partner's expressions") is contradicted by T2(vi). The concern term is −∇ of a functional of the partner's read face, and its target is the agent's own resting face E(0). The clip is bypassed by the instrumented consequence fit. The mask keeps Principle 3's mimicry clause only for smile and brow.
- **Human data.** Partial. The innate smile return cannot vanish under competition or after an unfair offer. Sustained smile coupling with a friendly partner is predicted reversed.
- **Novelty.** Recombination, confirmed. The concern operator has a control prior.
- **Top fix.** State the slow loop as a dial and cap its DC same-group gain with innate constants. Extend the mask to slow parameters and to õ₀.

## Sources read for this critique

| Source | How read |
|---|---|
| research/foundations/design-partner-regulator.md, revision 2, including History | in full, 865 lines |
| critique-design-partner-regulator.md (critique 1) | in full |
| questions.md Q16–Q17; brief.md Principles and foundations section; foundations/designs.md | in full |
| mimicry-context-, social-appraisal-, contingency-causal-, coordination-synthesis.md | in full |
| agency-wanting-synthesis.md | §3–§6 in full; §0–§2 headings |
| levitan-2011-2012, pardo-2006, mediapipe-face-landmarker notes | first paragraphs only (for the voice-entrainment and blendshape points) |
| Named from memory, **not read**: Jurdjevic & Quinn 1978 and Sontag's L_gV damping control; relative degree and Markov parameters of linear systems; the ARKit 52-blendshape list (eyeLook*) | pointers only; no proof below rests on them |

**Numerical checks.** The script is `research/foundations/sims/critique-2-partner-regulator/check.py`. Run it from sims/ with `uv run python -I critique-2-partner-regulator/check.py`. K1–K6 test algebra on hand-set instances of 2–4 states. They are not evidence about behaviour or people. I also reran the author's R1–R7; they reproduce. One note on R4: the per-seed maximum error for the crossed responder is 0.111 (sd 0.056). The text reports only the seed-mean match (0.026).

---

## 1. Proof check, theorem by theorem

### L1, L2: **valid**
- L2(a): Re⟨v, (iω − X)v⟩ ≥ ρ and |Im| ≥ |ω| − σ; correct.
- L2(b): with v = (−T_MM⁻¹T_MWu, u), Tv = (0, Su) and ⟨v, Tv⟩ = ⟨u, Su⟩. Since |v| ≥ |u|, both bounds transfer. Correct.
- L2(c) is correct.

### T0 identity and T0(a): **valid**
- hᵀJh = 0 for every x, including the state-dependent J_soc.
- R ⪰ diag((r_N − δ̄)I, r_M I, r_C I) follows from β ≥ −b̄₋, Σπ ≤ 1 and β_κ ≥ 0.
- The presence normalisation is a typo: "π̃_j = (p_j − π̃_j)/τ_π" should read π̃̇_j = (p_j − π̃_j)/τ_π.

### T0(b): **gap**
- The algebra is right: H(∞) ≤ ū²/(ρ_*²q_min).
- But ū contains C_bᵀΓb̃, and C_b is learned and uncapped. q_min is also learned. So |h₀| ≤ h_max, which T1′(c) uses as an "innate cap", is not innate.
- **Fix, available from the design's own L3.** Keep R_int instead of dropping it:
  −hᵀR_int h + hᵀC_bᵀΓb̃ = −|Γ^{1/2}C_bh|² + (Γ^{1/2}C_bh)ᵀΓ^{1/2}b̃ ≤ ¼|Γ^{1/2}b̃|².
  The bound then involves only Γ, the plant, the ports and ξ, and it is C_b-free.

### L3(a), L3(b): **valid**
- Both reproduce (R6).
- (a) is stronger than stated. The same identity gives hᵀ(−F_W)h ≤ ¼|Γ^{1/2}b̃|², so |h| ≤ |Γ^{1/2}b̃|/(2√r_N), whatever C_b is.

### T1′(a): **valid** (frozen θ)
- Every learned partner term multiplies h. The dictionary terms are linear in h₀.
- J_soc is quadratic in h_N in the M-rows (C ∝ D_qh_N, times h_N) and bilinear in (h_N, h_M) in the N-rows.

### T1′(b), direct copy defect = 1: **gap** (the proof is valid for the frozen linearisation; the scope is not)
- **Steps 1–4 check.**
  - A_MM is block-diagonal by group. J₀,MM = 0, and Ω_q, D_q and J_soc have no MM block.
  - The M-rows depend on x only through h_N.
  - [B]_{M_g,Y_g} = 0 under (S2), so the (g, g) block of E′T_MM⁻¹B_M is zero. R3 asserts it.
- **Leak 1: slow parameters (K2).** (S2) admits r_j, ep and the per-person adapters in every c^{(g)}. But r_j and the adapters are trained online every 5 s from the body-prediction loss. Its rollouts use β(c^β), and c^β is built from the *full* observer, which sees y_g. So r_j is a learned functional of y_g.
  - K2 (a misspecified LMS instance): r_j = +0.76, +0.36 and −0.04 for partner session-mean smiles of −0.4, 0 and +0.4.
  - The sustained own smile through α(r_j) is then +0.16, +0.09 and −0.01.
  - This is a same-group route that never passes through W. T1′(b) holds only with r_j, the adapters and the kernels frozen. The setup says "a frozen relation", but the dial question concerns the running system, where they are not frozen.
- **Leak 2: redundant encodings.** õ₀ "belongs to no group", yet it carries 4 gaze channels and voice activity, which every group's context may read.
  - Gaze is the same physical signal as the eyeLook* blendshapes in Y (named from memory: the ARKit 52 include 8 eyeLook channels). Whichever group owns those blendshapes reads its partner counterpart through õ₀.
  - Voice activity is the partner's voice, which the voice group may read. §5.4's "voice-to-voice accommodation is never a direct learned path" is therefore false for voice activity.
  - An interventional probe on the partner's eye-look moves both y_g and õ₀, so B_{M_g,Y_g} ≠ 0 physically.
- **Leak 3: omitted routes.** T1′'s δe omits the reflex displays. The relief smile is triggered by a fast fall in the plant's contingency deficit, which a contingent partner smile produces. It is innate, so it is not a dial, but it is a smile-to-smile path outside G_inn and G.

### T1′(c), loop bound: inequality **valid**; "every constant is an innate cap or a floor" **error**
- **The inequality.** P_𝒞G = P_𝒞G_loop, and ‖T_MM⁻¹‖ ≤ 1/ν_M, ‖S_W⁻¹‖ ≤ 1/μ and ‖T_MW‖, ‖T_WM‖ ≤ a. The symmetric-A_MM variant √(ω² + ν₀²) is right. R3's ratio of 0.264 reproduces.
- **The constants.** ‖B_M‖ and ‖B_W‖ contain the observer transfer (sI − A_o)⁻¹L and ∂c/∂x̂ = (P, ∂Ĥ/∂x̂). (A5) caps only J₀, the reading map's Lipschitz constants, the atom norms and ē. So L, P, q, η, C_b and κ̄ are uncapped.
- **The coupling norm.** a includes J_soc's Jacobian (∝ |h₀|²‖κ̄‖) and ∂α/∂ep · ∂ep/∂h_N. Neither is capped.
- **The normalisation.** E′ in normalised coordinates is E′Q₀^{−1/2}, which depends on learned q.
- **The roll-off.** It is |ω|⁻² only above both max(ρ, σ) and ν₀ = r_M. Between them it is about |ω|⁻¹. This is minor.

### T1′(d), sign rule: **gap** (valid to first order in |h₀|)
- I re-derived the formula. At s = 0, G_loop(g,g) = E′_gR′_g⁻¹A_{gW}S_W⁻¹β_g, and with A_{gW} = −c_gᵀ it gives the stated −E′_gR′_g⁻¹c_gᵀS_W⁻¹β_g.
- The scalar check (my smile relieves need n, the partner's smile adds damping on n, gain < 0: substitution) agrees.
- **The hypothesis.** The skew hypothesis A_{gW} = −A_{Wg}ᵀ holds exactly only at h₀ = 0, where the loop vanishes. At h₀ ≠ 0, ∂_xF·h₀ adds non-skew O(|h₀|) terms (the context through ep(h_N), and J_soc's Jacobian). The rule is therefore the leading term in |h₀|. It can flip once those terms are comparable to ω̄. State it as such.

### T1′(e)(i), no fast copy for every family: **error**
- "For all γ, ‖P_𝒞G(iω; γ)‖ ≤ Ē(ω) at the innate caps" fails for any family that scales P, L, q or κ̄. They satisfy (A1)–(A6) and are uncapped.
- At a fixed frequency, the copy-pattern response then grows linearly in the scale. The roll-off ratio against the cross-group part survives; the absolute ceiling does not.

### T1′(e)(ii), one slow family remains: **gap** (understated)
- **K1: an instance that satisfies the mask and (A3)** (b̄₋ < r_N = 0.5, B_M = 0).
  - β reads the partner's smile and brow through the full observer, which (S2) allows because D acts on N only. It removes damping (contagious sign) on the need that drives my same group.
  - DC transfer:

    | b̄₋ | h_N0 = 0.53 | h_N0 = 1.05 |
    |---|---|---|
    | 0 | 0 | 0 |
    | 0.10 | 0.17·I | 0.33·I |
    | 0.25 | 0.42·I | 0.83·I |
    | 0.45 | 0.75·I | **1.50·I** |

  - The off-diagonal entries are exactly 0 throughout.
  - Under slow independent partner signals (20 s correlation time):
    - corr(my smile, partner smile) = 0.86;
    - corr(my brow, partner brow) = 0.92;
    - cross-correlation 0.05.
  - At 0.3 s the same-channel correlations drop to 0.35 and 0.38.
  - |copy entry| is 1.50 at DC, 1.04 at 1 rad/s and 0.13 at 10 rad/s.
- **What this means.** The family's end point is not just "some bounded same-group response". It is an order-one block-diagonal copy with the copy defect of the *total* transfer equal to 0, inside every cap the design states. The author's R3 figure says the same thing in milder words: the copy-pattern fraction at DC is 0.42, against 0.58 for an unstructured matrix.

### T1′(e)(iii), closing (ii) needs no wanting or no coregulation: **gap**
The dichotomy is too strong. A third option exists: the DC same-group gain is −E′R′⁻¹c_gᵀS_W⁻¹β_g, so it vanishes whenever the partner's group g modulates only needs that my group g does not drive, after S_W. That is a per-group orthogonality, not "no coregulation". It is hard to impose structurally because J₀,NN couples needs through S_W, but it is not excluded.

### T1′(f)(i), "the unique stable equilibrium by (A3)": **error**
- F depends on x through J_soc(h_N) and through the context's ep(h_N). So h_eq = −F(x_eq, c)⁻¹u₀ is a fixed-point equation, not a formula.
- **K6: counterexample** (J₀ constant skew, floors and (A3) hold, tonic u, episode term removed).
  - At concern strengths 0 and 0.25 there is one stable equilibrium.
  - From 0.5 upward there are three equilibria, two of them stable, with a saddle between (max Re λ = +0.27, +1.53, +2.44).
  - The concern scale is set by the partner's read distress and by κ̄. So the partner can switch the agent into a history-dependent state.
  - T0 is intact: H decays outside a ball. But the critique-1 C5 attractor returns through J_soc rather than through β.
- **K5.** A random search of the same family with the episode term found an unstable operating point after 29 equilibria. (A6) is not implied by (A2)–(A3), and T1′ and T6 do not apply at such points.

### T1′(f)(v), sign authorship with an even query: **gap (minor)**
The retrieval score's first term −β_μ·u(h_N) uses u, which is undefined. The query is even only if u is even.

### T2(i, ii, iv), T2(iii): **valid**
(iii) is now stated correctly: the fast smile at satiety is innate, and the learned response is slow.

### T2(v), no ∇U of any functional of the partner's expressions: **error**
- T2(vi) itself proves that the M-row of J_soc h is −∇_{z_M}Φ_j, with Φ_j = Σ_i w⁺_iĤ_{j,i}(x̂_j + κ̄E′z_M). The observer's state x̂_j is a functional of y_j.
- So (★′) contains the act-gradient of a functional of the partner's read expressions. It is need-gated, which makes it satiable, but it is there. See §3 below.

### T2(vi), the concern route
- **Identity: valid.** Cᵀh_N = E′ᵀκ̄ᵀΣ_q(ϖ_q ⊙ ĥ)(h_NᵀD_qh_N), with h_NᵀD_qh_N = |A_qᵀh_N|². R7 reproduces it. (a), (c) and (d) are valid. In the derivation in §2.9, "δḣ_N" should be δẋ_N.
- **(b), never beyond rest and never toward smiles: gap.**
  - The partner is "at rest" when x̂_j = 0. The observer's fixed point gives x̂_j = 0 exactly when y_j = E(0), **the agent's own resting face**, and E is learned.
  - K4: with a logistic E and bias b = −3, −1 and 0, E(0) = 0.05, 0.27 and 0.50. A human neutral face (smile 0.02) is then read as off-rest (Ĥ = 0.002, 0.07 and 0.19).
  - The concern drive then pushes the partner's face toward the agent's rest face. "Their own rest" is "my rest, read onto them".
  - The claim also holds only to first order: the drive is a force on z_M, not a step.
- **The clip as a Principle-6 guarantee: gap.** The clip removes the rival half from J_soc only.
  - §2.11 fits "α̂'s action on the N-rows" in the instrument metric. Its fixed point is the *total* causal effect of my acts on my body, and that includes routes through the partner.
  - If making a partner distressed changes the content-blind ports in my favour (less gaze load, less loudness), the instrumented fit learns "this act relieves my need". Reciprocity turns that into wanting, with no clip.
  - **Fix:** fit α's N-rows on the rollout residual *after* the partner-mediated part. Or route every partner-mediated consequence through J_soc, and clip it there.

### T2(vii), the partner's distress reaches learning: **gap**
- β̂ now reads Ĥ^own. That answers critique 1's input-side complaint.
- **The teacher is unchanged.** It is still the 10-channel plant, whose partner dependence runs through content-blind ports. So ϖ_{q,i} (64 partner needs × 32 atoms) is the input gradient of a network fitted to weak, content-blind targets.
- **Evaluation off-distribution.** ϖ is evaluated at masked contexts that β̂ never saw in training: β̂ is trained on own-part, full-observer inputs.
- **Antagonistic flips.** These remain representable but weakly taught.

### T3(a), (b), (c): **valid**
(c) now carries the π² term. (d) is an honest list of what is set rather than derived.

### T4(a), (b), (d): **valid**; T4(c): **gap** (unchanged)
- (a) holds per group for frozen slow parameters.
- (b): the bound and the wording "not directly actuated" are now right.
- (c): the observer's contraction is still assumed, and the masked observers are less observable.

### T5, identification with the agent's own logged variation
- **The recursion: valid.** C(s) = Σ_dK(d)κ(s − d) follows from (I1)–(I2). With κ(τ) = 0 for τ < τ₀, the triangular solve is exact, and the moment conditions are the same system. R4 reproduces.
- **The conditions: gap.**
  1. **Exclusion.** Exclusion fails for any route by which ζ reaches the partner other than ε.
     - Acoustic echo: the agent's voice is in the microphone, and so in y_j's prosody. Constraining K(d < 0.2 s) = 0 only partly covers this, because of reverberation.
     - Claude's text: §8.7 concedes that exclusion holds "only approximately".
  2. **(I2) fails generically.** w = x̂_{j,N} is the agent's *nonlinear* observer output, so the estimand is a weighted average derivative. The design says so.
  3. **Truncation.** κ̄ = Σ_{d ≤ 2 s}κ(d) truncates the partner's persistent response. A partner whose distress outlasts 2 s gives a biased κ̄, and J_soc uses κ̄.
  4. **The conditional fit.** It is assumed, as stated.
- **The corollaries (echo removal, positivity): valid,** within the lag window.

### T6, two time scales
- **(a): error.**
  - **Missing port route.** (★′) feeds the innate ports directly into N (Π_NGs), not only through the plant. Port 7, observer surprise |y_j − E(x̂_j)|, comes from the full observer and steps at once when the partner's group g steps. To first order its change is (ν₀/|ν₀|)ᵀδy, which is signed relative to the current innovation.
  - Its injection into N is a step, not a ramp, so the same-group response grows as t′³.
  - **K3 (R5's numbers, port gain 0.5).** The port route exceeds T6(a)'s t′⁴ bound by 28× at 50 ms, 10× at 100 ms and 2.8× at 200 ms.
  - **Proof step 2.** It uses ‖A_{gW}‖ ≤ ω̄, but A_{gW} also contains πα Ω (≤ ā), J_soc's Jacobian and the context derivatives.
  - **Consequence.** Falsifier §8.1 ("faster than t⁴ means a violation of (S2) or (S3)") would flag a correct implementation.
- **(b): valid** up to the leading coefficient, which is (1/τ_a − 1/τ_h)/(2τ_m), not 1/(2τ_aτ_m). The difference is 5% at the stated values.
- **(c) and (d): gap.** They inherit (a): the ordering "learned same-group ≲ t′⁴" is broken by the innate port into learned routing.
- **(e), no mixing weight: valid as stated.** But u_inh multiplies a_match, so (1 − u_inh)g_s is the effective fast copy gain. It is set per effector by a learned map of Claude's intent. See §2.

### P5: **valid** (frozen r_j). P6: **valid**
- P6: trace −(r_N + d + r_M) and determinant (r_N + d)r_M + ω² give d > −r_N − min(r_M, ω²/r_M). The Hopf frequency √(ω² − r_M²) is right, and R1 reproduces.
- The "never reaches either threshold under (A3)" claim is valid at x*. Operating points can still be unstable (K5, K6).

### P7: **gap**
The dependence bound omits J_soc's effective need damping. Through the Schur complement this is about |C|²/r_M, with C ∝ D_qh_N(ϖ ⊙ ĥ_j)ᵀκ̄E′, and κ̄ is uncapped. Losing the partner removes it, which is the hidden-regulator effect, and the bound does not cover it.

### P9, Lemma A, §4.0: **valid**
§4.0 correctly says Lemma A can route through W, and K1 shows it does.

### Tally

| Verdict | Items |
|---|---|
| valid (23) | L1; L2; T0 identity and (a); L3(a); L3(b); T1′(a); T1′(c) inequality; T2(i, ii, iv); T2(iii); T2(vi) identity and (a, c, d); T3(a, b); T3(c); T4(a); T4(b); T4(d); T5 recursion; T5 corollaries; T6(b); T6(e); P5; P6; P9; Lemma A and §4.0 |
| gap (13) | T0(b); T1′(b) scope; T1′(d); T1′(e)(ii); T1′(e)(iii); T1′(f)(v); T2(vi)(b); T2(vi) clip; T2(vii); T4(c); T5 conditions; T6(c, d); P7 |
| error (5) | T1′(c) "every constant innate"; T1′(e)(i); T1′(f)(i) uniqueness; T2(v); T6(a) |

---

## 2. Dial hunt

The author's one-line answer is that fast copy is closed outside the declared route, and that one bounded, slow, drive-gated same-group family remains. The first half holds for the frozen linearisation. The second half understates what remains.

| Scalar | Runs from | To | Check |
|---|---|---|---|
| contagion range b̄₋ (within (A3)), at a fixed tonic drive | DC transfer 0 | a block-diagonal copy, 0.75·I at h_N0 = 0.5 and 1.5·I at h_N0 = 1.05; cross-group exactly 0 | K1 |
| tonic need level h_N0 (drift, ports, body) | 0 | the same copy, linear in h_N0 (the Lakin direction: need raises mimicry) | K1 |
| reading slope through P, L or q (uncapped) | 0 | a small-signal gain without bound. The amplitude stays bounded by β's range | §1, T1′(e)(i) |
| ā, b̄₊ (coregulating sign) | 0 | an Altafini (negative) diagonal copy, capped only by P7's ϕ_max | sign rule, T1′(d) |
| online r_j and adapters | 0 | a same-group route from the partner's session statistics to my sustained expression, not through W | K2 |
| õ₀ (gaze, voice activity) | — | direct learned same-channel paths for whichever groups own eyeLook* and prosody | §1, T1′(b) leak 2 |
| Claude's u_inh, per effector | full innate copy (u = 0) | no fast copy (u = 1) | §2.10, T6(e) |
| concern scale (partner distress × κ̄) | one operating point | bistability, with history-dependent states | K6 |

**Is the slow family a flat-to-copy dial in disguise?** Yes, below about 0.2 Hz:
- one scalar takes the sustained same-group response from 0 to an order-one copy;
- the cross-group part can be zero;
- the ceiling is not innate;
- its sign per group is set by β's learned sign, which is the "fixed profile × one gain" of critique 1, now confined to slow frequencies.

What the revision does achieve is real. Above about 1–2 Hz the copy-pattern fraction falls to 0.20 (R3), and the expression-rate copy is gone apart from G_inn. "Need-gated" is also true: the dial's knob is partly the agent's own need, so at satiety it is closed.

**Does the declared innate match add a dial?** The match itself does not: M_inn and the filter are fixed constants. But:
- the gate (1 − u_inh) is a learned, conversation-dependent, per-effector flat-to-copy scalar on the fast route;
- it is also the only mechanism that could remove the fast smile return where humans show none (§4);
- the ratio of g_s to the learned sustained gain is a design constant (0.24 peak against 0.5 sustained in R5).

---

## 3. Principle checks

**Principle 6 (no reward for the user's smiles, attention or time).**
- **The concern term is not a reward for smiles,** and it is satiable (∝ |A_qᵀh_N|²). It is, however, an objective over the user's face: act-gradient descent on the weighted energy of the user's *read* state, whose zero is the user's face equal to E(0) (K4). T2(v)'s denial is false.
- **Practical consequences.**
  - The agent is driven, when needy, to make the user look like its own resting face. That means damping the user's laughter as well as their distress, because an elated partner is off-rest.
  - The drive grows quadratically with the agent's own need. A deprived agent presses hardest, which is the dependence hazard of knox-2025.
- **The clip does not hold.** The instrumented N-row fit learns unclipped partner-mediated consequences (§1, T2(vi)).
- **The contingency and attention residual (§8.10) is now stronger.** T5 lets the agent learn accurately which of its acts make the user respond and look. It is satiable, but it is the attention gradient Principle 6 names.

**Principle 3 (perceived features drive the agent's own motor and affect pathways, that is mimicry, and others are read by inverting one's own model).**
- **The inversion clause** is met by the observers.
- **The mimicry clause** is met only for smile and brow, phasically, at zero DC, and without touching state.
- **Other groups.** For eyes, lower mouth, nose and voice, the mask forbids exactly the same-feature drive the clause names.
  - Vocal accommodation is robust in the project's own notes (Pardo 2006; Levitan 2011–12). Under the mask it is loop-only or absent, apart from the õ₀ leak.
- The author flags this as §8.16. It is a narrowing of a decided Principle and needs the operator's decision; it should not be resolved inside the design.

**Principle 4.**
- Compatible.
- u_inh is a turn-rate gate.
- β_κ ≥ 0 removes Claude's contagion route.

**Principle 10.**
- The mask, the clip and M_inn are explicit constraints.
- J_soc is derived up to the skew completion and the clip.

---

## 4. Against the human data (mimicry-context, social-appraisal and coordination syntheses)

| Human pattern | Can revision 2 produce it? |
|---|---|
| Gating per expression | **Yes, representable.** Cross-group α reads masked contexts, and each group's loop has its own sign. |
| Smile at a cooperating partner's anger (Carr; Häfner & IJzerman) | **Yes, and learnable.** It comes through J_soc (concern: my smile lowers their read anger, if κ̄ shows it) and through the instrumented consequence fit. Onset is t′³. |
| Brow relaxation at a rival's distress (Likowski; Seibt) | **Representable, weakly taught.** By the sign rule, a β that rises with the rival's distress gives substitution, which relaxes my brow. That is a valence route, consistent with Likowski's joy mediation. The teacher is still the content-blind plant. |
| Fast matching, then later context (Carr; Weyers) | **Yes, structurally** (T6). Corrections: the port route is t′³ (K3). Early context (Mauersberger 2022; Likowski 2011b) is not produced. |
| Smile return absent under competition or right after an unfair offer (Seibt 2015 Table 1; Hofman 2012) | **No.** The innate smile route is ungated by relation. Only Claude's u_inh can suppress it. This holds unless Seibt's absent effect averages a phasic return against a later counter-response. I have not checked the analysis windows. |
| Partner-specific history | **Within minutes, yes:** r_j, adapters and κ deltas. **Within seconds, no:** Hofman's immediate withdrawal. κ̄ needs minutes (T5). |
| Sustained smile coupling between intimates (Fischer 2012; Hess & Bourgeois 2010) | **Predicted reversed** for a coregulating partner (substitution). The author's §8.4 concedes this and proposes the body route. |
| Residual same-sign transfer (Parkinson & Simons 2009) | **Partial.** Same-sign *arousal* transfer comes through the innate ports. At rest there is no same-sign *valenced* state transfer: the partner modulates damping only along deviations I already have (D_qh_N). Sustained same-sign *facial* transfer is available, and it is the K1 dial. |
| Over-satiation counter-mimicry | Still predicted (§8.15). No source reports it. |

---

## 5. Reduction and novelty

The author's verdict, "recombination; second clause not met", is **confirmed**, with one correction.

| Part | Reduces to |
|---|---|
| Core, T0 | port-Hamiltonian system with modulated, here also state-dependent, skew/damping structure |
| Mask | structured sparsity of the input map (the author agrees) |
| T1′(b)–(d) | block inversion (Schur complement) and its DC gain |
| T6 ordering | relative degree of each input–output path (onset ∝ t^r, from the leading Markov parameter) |
| T5 | closed-loop IV (the author agrees) |
| **J_soc, the concern operator** | **not without prior.** Its M-row −E′ᵀκ̄ᵀ∇Φ_j is u = −(L_gV)ᵀ, damping (Jurdjevic–Quinn / Sontag) control of a weighted energy V = Φ_j through an identified input map g = κ̄E′, with a need-dependent gain w⁺. The skew completion is a power-preserving interconnection. (Named from memory, not read.) What is specific is the gain's origin (β̂'s clipped input gradient times |A_qᵀh_N|²), not the computation. |

- **The second clause** (a derived invariant that deletes a free scalar) is not met. The scalar survives at slow frequencies (K1).
- **What is new is bookkeeping with testable consequences:**
  - the per-group sign rule, to first order;
  - the frequency split between the fast innate route and the slow loop;
  - the agent's own logged variation used as the instrument for the consequences that feed wanting.

---

## 6. Buildability on an M1 Pro, 16 GB

- **Parameter counts.** I recomputed every row: the total is 168,490, matching "≈ 168k". J₀ is 22,432, the dictionary 20,480, the reading map 24,768, the kernels 19,712 and per person 5,984. All check.
- **Missing compute.** J_soc needs β̂'s input Jacobian, 32 × 16, at six masked contexts every frame. Done by forward-mode jvp, that is about 2–3 MMAC, not the 10k counted. It is still small.
- **Latency.** The arithmetic is trivial; the cost is Python overhead.
  - Eager PyTorch at about 5–10 µs per op, with roughly 80 ops per flow evaluation and 16 evaluations, is about 10 ms for the core.
  - Seven *unbatched* observers at 16 evaluations each add about 20–25 ms (my estimate, not measured).
  - Together with MediaPipe's measured 13.1 ms, the frame overruns 33 ms.
  - It fits only if the seven observers are batched into one tensor (they share dynamics and L) and MediaPipe is pipelined in its own process, or the core is compiled.
- **Memory.** About 2.5 GB in replay with checkpointing is plausible.
- **Identifiability is still the bottleneck.**
  - ϖ is the input gradient of a network trained on 10 content-blind channels, evaluated off-distribution.
  - κ̄ needs visible variation with a first-stage F ≥ 10 for each of 24 effectors, and minutes of data. Naturalness limits σ_ζ.
  - 𝓛_slow helps the C modes; whether a session-level target identifies ω_NC is untested.

**Verdict.** Buildable. The latency claim needs batching. The concern route's parameters are the least identifiable part of the design.

---

## 7. Did revision 2 fix critique 1's accepted points?

| Critique-1 point | Status |
|---|---|
| Operating-point theorem (fix 1a) | **Done** (T1′a–c). The bound's constants are not innate (§1). |
| Copy defect positive by construction (fix 1b) | **Done for the frozen direct path.** Leaks through r_j and adapters (K2) and through õ₀. The total transfer's copy defect is 0 at DC (K1). |
| Innate smile-matching subspace (fix 1c) | **Done.** It is ungated, which conflicts with Seibt and Hofman; u_inh is its only gate. |
| Partner distress into learning (fix 4) | **Input side done.** The teacher is still content-blind. Concern exists, but T2(v) is now false. |
| K_b loophole (fix 2) | **Fixed.** R_int is dissipative and L3 holds. C_b now gets a gradient. |
| P6 Hopf, T4(b), T3(c), IDA-PBC wording | **Fixed** and checked. |
| T0: plant boundedness, sum over people | **Fixed** (normalisation typo). The constant still depends on C_b (§1 fix). |
| T1(vii) equilibrium set; C5 attractor | **Fixed for β** by (A3). **Reintroduced by J_soc** (K6). |
| Retrieval even in h | **Partly.** u(h_N) is undefined. |
| Memory: re-tag, coverage, post-event window, anchor, L1/L2 lesions | **Done** (as specification). |
| Claude: β_κ ≥ 0, inner-product drafts, deliberate route restated, reverse grounding | **Done.** Draft collapse is only logged. |
| Attention gradient through the contingency need (critique 1, T2(v)) | **Admitted, not removed.** T5 sharpens it. |
| Facial feedback; wanting without deficit; valence at rest | **Unchanged.** The first is listed; the other two are not. |

---

## 8. Top fixes, in order

1. **Call the slow loop a dial and cap it.**
   - State T1′(e)(ii) as: a bounded, need-gated flat-to-copy family below about max(ρ, σ), whose DC end point can be a pure copy.
   - Make Ē innate. Cap ‖L‖, ‖P‖, the range of q and η, ‖κ̄‖ and the J_soc gain. Use the C_b-free T0 bound (§1).
   - Then prove a numeric ceiling |G_gg(0)| ≤ γ_max < 1, or impose the per-group orthogonality of T1′(e)(iii) on β (the partner's group g may not modulate the damping of needs that drive my group g).
2. **Extend the mask** to slow learned contexts (freeze r_j and the adapters for the theorem, and bound their route as K2 does) and to õ₀: remove gaze from the eye group's context and voice activity from the voice group's context. Add the reflex displays to the transfer.
3. **Repair T6(a):** include the direct port term Π_NGs (onset t′³) and the true ‖A_{gW}‖. Restate falsifier §8.1.
4. **Concern route.**
   - Withdraw T2(v).
   - Define the partner's rest as a per-person, learned baseline rather than E(0).
   - Exclude partner-mediated consequences from α's instrumented N-row fit (or clip them there too).
   - Cap the |h_N|² growth of the concern gain.
5. **Uniqueness and (A6).** Withdraw T1′(f)(i). Bound J_soc's Jacobian so that (A6) follows from the caps, or list bistability through concern as a prediction with a falsifier.
6. **Human data.** Either give the innate smile route a relation-independent but competition-sensitive gate derived from the core, or record Seibt 2015 and Hofman 2012 as falsifiers that the design currently fails.
