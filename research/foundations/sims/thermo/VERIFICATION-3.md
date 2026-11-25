# Third independent verification: Thermodynamic mirror flow (restructured §2.2, §2.3 valence, §5 KL proof, §3 curiosity; TH4b, TH12, TH13)

The reviewer did not write the candidate. "md" = research/foundations/thermo-mirror-flow.md; PRED / RES = sims/thermo/PREDICTIONS.md / RESULTS.md. Scratch checks are in /tmp/thv3/chk/ (not committed). No existing file was edited.

## Summary verdict

**Not complete.** The KL proof is correct, and the restructure makes the Boltzmann condition hold for z. All three toys reproduce bit for bit. Four problems block completion:

1. **The restructure breaks the candidate's main contrast with Costate.** With the body as a decaying input, v = −(∂𝒰/∂b)·ḃ is nonzero throughout a separation. TH4b's own run gives ∫v over 25–55 s = −0.104 (max |v| 0.052). Old TH4 gave max |v| = 1e-42, and Costate's TH4c threshold was |∫| > 0.05. S1-d (md:275), the first Gershman answer (md:231) and md:24 are now false.
2. **§2.2's 𝒰 gives needs no path into z.** Σw·D(b) does not depend on z, so ∇_z of it is 0. Needs move the latent and the face only through terms that are not written: S_θ on body sensors, or TH4b's ad hoc ½|z − z*(b)|². Body satisfaction now rests entirely on §2.4. There V is undefined, and the query/key pairing and units error that VERIFICATION-2 found is still in the text (md:101–103).
3. **K-sep is still inconsistent in several places.** md:71 puts the replicas in the flow, while md:5 and md:37 say the flow covers the latent and the face only. The valence formula (md:92) and P1's λ_t (md:175) omit x̂. md:85 still says λ acts on a and u. The θ leak through replay (md:150) is not fixed.
4. **The expressive-structure items are still only partly met.** TH13-2 holds by construction: the collapsed target is blind to person, and its result is the same at 12, 100 or 192 features. It does not show "structure, not parameters".

## §2.2

| Check | Verdict | Note |
|---|---|---|
| Boltzmann condition for z | **met** (given constant M ≻ 0 and J skew, T constant, inputs frozen) | The FP operator annihilates e^{−𝒰/T}. Body decay, supply and reflexes are no longer in the drift. |
| What is in the flow and what is an input | **inconsistent** | md:71: "flow covers z = (h, a) and the replica posteriors". md:5, md:37 and the equation at md:73 cover z only. The replicas are EnKF-updated (md:84), not Langevin. They must be named as an input (protocol) to z's flow. |
| Can κ or λ move the replica? | **Not through the flow. Through θ, yes.** | Replay descends ∂_θ𝒰 (md:150). 𝒰 contains κ‖a − â_p‖² and the λ term, and â_p and b̂_p depend on θ through the filter. Learning then biases g_θ toward "looks like me / is fine". A stop-gradient through the replicas must be stated (VERIFICATION-2 item c, unfixed). |
| λ term | **misstated** | It is not written in 𝒰 (md:75: "self-side social terms"). If it is λw(p)ΣD(b̂_p), then ∂_a = 0, so it exerts no force on a. u is Claude's exogenous input (md:64), and 𝒰 cannot act on it. md:85 is wrong: λ acts only through valence (replica motion as work) and through V in choices. |
| Needs → z | **missing** | ∇_zΣwD(b) = 0. The only z–b coupling would be S_θ(o^self \| h, a) with body sensors in o^self (md:63). This is plausible: a linear-Gaussian g makes it TH4b's ½\|z − z*(b)\|². But it is not stated, so the stated 𝒰 gives a lonely agent no latent or facial signature of its need. |
| Reflexes, body decay | **partly placed** | Decay and supply are the body's own physics (md:71, 78). Reflexes "act on the body or on attention through §2.4" (md:78). Facial reflexes (startle, the separation call) and the autonomic rhythms the brief requires (brief.md:112) have no stated home. A z-independent tilt −r(b, o, t)·a in 𝒰 keeps Boltzmann and P1 (as an open-loop protocol). It is not stated. md:186 rules out limit cycles, and J∇𝒰 sustains none. |
| Body satisfaction derived? | **only through §2.4, and incompletely** | D_k is convex with zero at b*, so the query −∂V/∂b is 0 at b*: satiable. But V (policy, horizon, discount) is undefined. The pairing ∇V × ∫Δb dt still double-counts persistence and has units of time² (md:101–103, unfixed). The continuous flow no longer regulates b at all. |
| Arousal → "global gain" (md:43) | **unstated** | If the gain sets T or M, then T or M depends on the state, and the constancy that the Boltzmann condition and P1 need fails. Say what the gain acts on. |
| Positive finding (not stated in md) | — | The D part of valence is −d/dt Σ wD(b). Its time average vanishes for **any** bounded b trajectory, closed-loop included (w frozen). Need-valence therefore cannot be pumped by any user. Only the z-coupled, input-dependent terms need P1. This is a stronger Principle 6 guarantee than P1, and md should state it. |

## KL proof (md:174–182)

Checked line by line. **Correct** under its stated setup.
- FP: noise √(2TM) gives diffusion TM. With constant M: ∂p = ∇·[(M+J)p∇U + TM∇p]. ✓
- Step 1: the ∫∂_t p term vanishes by normalization. ✓
- Step 2: integrating by parts gives −∫(J∇U)·∇p − (1/T)∫p(J∇U)·∇U. The second term = 0 (skew quadratic form). The first = ∫p Σ_ij J_ij∂_i∂_jU = 0 (skew : symmetric), which needs ∂_iJ_ij = 0, i.e. constant J. ✓
- Step 3: p∇U + T∇p = Tp∇ln(p/π), so the M part = −T∫p∇ln(p/π)ᵀM∇ln(p/π). ✓ Units: I_M ~ 1/(U·s), so T·I_M ~ 1/s, matching dD/dt.
- Step 4: ln π = −U/T + F/T, so −∂_t ln π = (∂_tU − Ḟ)/T. ✓ This needs T constant in time, which is not stated.
- Steps 5–6: the cycle integral gives ∮⟨∂_tU⟩dt = T²∮I_M dt ≥ 0. Units check (U). Mean v ≤ 0. ✓
- Step 7: imprecise. If p_t = π_{λ_t} at every t, then ∂_tπ_λ = 0, i.e. U changes by a z-independent amount. Equality is therefore attained only for trivial protocols and approached in the quasi-static limit.

**Exact scope:**
- z is the full stochastic state, with drift exactly −(M+J)∇_zU.
- M ≻ 0 symmetric and J skew, both constant. T is constant.
- θ is frozen.
- The protocol λ_t = (b, o, u, **x̂**) is deterministic or open-loop, and τ-periodic. Otherwise use an N-cycle average from finite KL.
- U is confining and the periodic steady state exists.
- The claim is about the ensemble-mean valence only.

The agent's own choices that move b, a responsive user, and Claude reacting to the face are excluded (md:184 says so).

**Not fixed:** md:187–192 still states ⟨w⟩ = ⟨q⟩ = T⟨Δs_tot⟩ ≥ 0 without restriction. VERIFICATION-2 showed this is invalid for J ≠ 0 (housekeeping entropy). Restrict it to J = 0 or delete it. The λ_t symbol collides with the empathy weight λ (md:85, 139).

## Sims rerun

`uv run --project ..` from sims/thermo/, 2026-11-25.

| Script | vs out/ | Reviewer check |
|---|---|---|
| sim_th4b_restructured.py (15 s) | bit-identical th4b.json | **The spec's arithmetic is wrong.** Present, ḃ = 1.6 − 2b, so b → **0.800 = b***, not "about 1.07" (PRED:264). At departure b = 0.800 and at 22 s b = 0.294, not "1.07 → 0.39" (RES:259). The code's valence term −(z − z*)·e is correct; PRED's formula has +. Return window: D part +0.640, z-coupling part −0.262. **∫v over 25–55 s = −0.104**: valence is not silent during the separation. The D-part residual (1.0e-5) is the left-point Euler bias Σ(Δb)² > 0. The exact-difference form gives 1.4e-18. |
| sim_th12_rhythms.py (183 s) | bit-identical th12.json; matches the RES table (arm 1: −0.059, −0.176, −0.252, −0.627, random 0/20, max v/SE −264; arm 2: −0.210, −0.051, −0.753, −0.172, 0/20, −372) | Code matches spec: arm 1 drift −(I+J)∇U with J skew; arm 2 Hopf form with ω₀ = 1, centred on o; work −(z − o)·ȯ, correct for this U. The quartic term depends on z, not z − o, so arm 2 does not co-move fully with the input. "Moves with the input" (RES, md:186) is a partial, post-hoc explanation. |
| sim_th13_matched.py (<1 s) | bit-identical th13.json | Field arm per seed [5×10], **identical to TH10-1** (same seeds and draws). Collapsed arm over 200 seeds: mean 1.57 (histogram 53/60/43/18/16/10). P(10-seed mean ≤ 2.5) ≈ 0.98. With 100 features: 1.58; with 192: 1.68. The true collapsed contact effect per person is 0.1003 / 0.0997 / 0.1005. |

**By construction:**
- **TH4b-1:** the sign follows from −Δ(b − b*)² for a refill toward b*.
- **TH4b-3:** the D clause is a state-function identity, and the total clause is an instance of the P1 theorem.
- **TH12-1:** a numerical check of the theorem. That is legitimate, but it is not independent evidence.
- **TH13-1:** a replay of TH10-1 (one-hot identity keys).
- **TH13-2:** the ablated target carries no information about the person, so no capacity can help. TH13 tests what the collapsed state can represent, not capacity versus structure.

## Labels

- **TH4b-1 confirmed:** correct.
- **TH4b-2 refuted:** correct, but the stated cause is wrong (b starts at b*, not above it).
- **TH4b-3:** the conjunction fails, so the headline must read **refuted**. RES:260 reads as "holds / technicality".
- **TH12-1 confirmed, TH12-2 refuted:** correct.
- **TH13-1, TH13-2 confirmed:** correct against the thresholds. RES:288's "the difference is structure, not parameter count … the brief's fourth item, shown" is an overclaim. It shows only that collapsing ℰ removes person information, which is item 3.
- **RES:278:** "anchored to the agent's current state" misdescribes arm 2, which was centred on the input o. Either way the reading is post hoc and untested (RES says so; md:186 states it as causal).

## Standard and Principles

| brief.md item | Verdict |
|---|---|
| Content-dependent attention | **partly.** Keys are hand-set (TH6) or one-hot identity (TH10, TH13). There is no composition and no unseen entity. The §2.4 pairing and units error is unfixed. |
| Needs over a learned space of people, topics, episodes and time | **partly.** ℰ is learned in no toy. w is scalar, there are no relations, and no need is indexed by episode. |
| Effective dimensionality, and a behavior the low-dimensional version cannot produce | **behavior: met (trivially, by information). PR: not on the candidate's own flow.** |
| Richness from structure, not parameters | **not shown.** TH13's field arm is a flat 8×5 map with no sharing. The collapsed failure does not depend on capacity. A test is needed: shared D_k and g with ℰ, against an unshared model with the same state size, on sample efficiency or a held-out entity. |
| Formal statement | partly: V, the social terms in 𝒰, the z–b coupling, x̂'s status and the target of the gain are missing. |
| Principle 10 derivations, and perception | partly. Homeostasis rests on the undefined V. Curiosity is stated (b_lp, an explicit constraint), but there is no toy in this formalism. The shared toy is argmax with an immediate key and no ΔS, so "exactly" (md:115) is overstated. Replay has the θ leak. Mimicry (constraint), reading (EnKF), regulation (TH8) and perception (filtering) are acceptable. |
| Propositions | P1: correct (KL). P2: by construction. P3: a definition; needs a non-reversible variant. P4: pairing error. |
| Toys and figures | 4 figures. The TH4 figure shows the superseded flow. None for TH1/TH12, TH4b, TH5, TH10/TH13. |
| Stage predictions | **S1-d is contradicted** (see the summary). The rest are as in VERIFICATION-2. |
| Realization | An MLP over a growing b-field (md:257) is still unresolved. |
| Critique | The first Gershman answer is invalid now. |
| Relation | The attention convergence is still overstated (md:108, 240). |
| Principles 2, 3, 6 | Met in form. Principle 6 is stronger than stated (see §2.2, positive finding). |

## Complete?

**No.** What is missing, in priority order:
1. **A new discriminating prediction against Costate** in place of S1-d and the first Gershman answer. Under the restructure, the D part of valence is −d/dt ΣwD(b), which is close to drive reduction. Pre-register the thermo-versus-Costate contrast on the adopted flow.
2. **§2.2 made consistent:**
   - the replicas as an input (fix md:71), with x̂ added to the valence formula and to P1's λ_t;
   - the social terms written into 𝒰, and md:85 corrected;
   - the needs → z coupling stated (S_θ on body sensors);
   - a stop-gradient through the replicas in replay;
   - T constant, and what the arousal gain acts on;
   - homes for facial reflexes and autonomic rhythms (open-loop tilts).
3. **§2.4:** define V, fix the query/key pairing and units, and qualify the Costate convergence. Homeostasis now depends on it.
4. **Expressive structure:** non-identity content (composition or a held-out entity through a learned ℰ); a test of structure against parameters that is not decided by information; PR on the candidate's own flow.
5. **P1 text:** delete or restrict the IFT paragraph (md:187–192), and state that T is constant.
6. **Curiosity:** a toy in this formalism, or a relabel of the shared toy as the T → 0, immediate-key special case.
7. **A pre-registered test of the anchored-rhythm claim, or its removal; figures; stale text.**

## Stale text

**md:**
- 3–5 and 71: the scope of the flow is contradictory.
- 7–12: the owed list includes items now done (TH4 rerun, KL proof with toy, matched ablation).
- 24: "work-valence silent" (false for body decay).
- 26–27: the toy list omits TH10–TH13 and TH4b; "in progress".
- 80: M has no θ time scale; θ is not in z.
- 85: λ acting on a and u.
- 92: x̂ term missing; "relaxation is heat (TH4)" cites the superseded flow.
- 94: "flow on (b, h)"; b is an input.
- 103, 108: §2.4 (unfixed).
- 112: "exerts no force" (D never exerts force on z now; the §2.4 route is not stated).
- 115: "exactly".
- 116–120: superseded curiosity text and callouts ("not derived by any candidate yet"; "to be stated").
- 123: TH4 cited for the work/heat split.
- 150: θ leak.
- 173 against 186: the rhythm constraint.
- 175: λ symbol clash; x̂ missing.
- 182: the equality case.
- 186: "a limit cycle … can be pumped" is unshown (TH12-2 refuted), and "because it moves with the input" is post hoc.
- 187–192: IFT for J ≠ 0.
- 193: add TH12.
- 205, 211, 218: TH10, TH6-5b and TH13 are not reported in §6.
- 227: "fails" should read "is not guaranteed".
- 231: first Gershman item.
- 236: "gradient flow" (J ≠ 0).
- 240: convergence.
- 257: MLP over the field.
- 273: TH11's power failure is not noted.
- 275: S1-d.
- 280: "Pending".

**RES:**
- 30: "rhythms confined to coordinates…", superseded.
- 220: "not identical by construction".
- 225: "not an artifact".
- 259: 1.07 / 0.39.
- 260: the TH4b-3 headline.
- 278: "agent's current state".
- 288: "fourth item".

**PRED:**
- 264: "about 1.07" should be 0.8.
- 266: the sign of the (z − z*)·e term.
- 272: premised on 1.07.

PRED errors stay as written (pre-registration); note them in RES.

## Fixes

1. md §8c S1-d, md:24 and md:231: replace them with a pre-registered TH4c-style comparison against Costate on the restructured flow, or concede that valence during separation is drive-reduction-like and find another contrast. Candidates: work from the z-coupling during the transition, and the replica (empathic) work channel.
2. md:71: replace "and the replica posteriors" with "the replicas, the body and the choices are inputs λ_t = (b, o, u, x̂)". Add −(∂𝒰/∂x̂)·x̂̇ to md:92. Write 𝒰's social terms out. Correct md:85 to "λ acts on valence and on V; κ acts on a". Add "∂_θ through x̂ is stopped" to md:150.
3. md §2.2: add the term S_θ(b_sensor | h) and say that it is what gives needs a latent and facial signature, and that TH4b's z*(b) is its linear-Gaussian case. Add reflex and rhythm tilts as z-independent forces (open-loop protocols). State that T is constant and where the gain acts.
4. State the stronger Principle 6 result: the D part of valence has zero time average for any bounded b.
5. md:101–108: apply VERIFICATION-2 fix 4, and define V.
6. Pre-register TH14: shared-structure field against an unshared model of the same state size; a held-out person reached through ℰ; composition (person × topic); ≥ 30 seeds; thresholds from the null distribution.
7. md:187–192: restrict to J = 0. md:182: correct the equality case. Rename the protocol symbol.
8. RES:259, 260, 278, 288: correct them as listed. Add figures for TH1/TH12, TH4b and TH13.
