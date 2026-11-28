# The five-pass conjecture: a guarantee against copying that holds for every partner is a per-channel bound on steerable gain

Written 2026-11-27. This note attempts the conjecture that ends `research/new-core-search-5-synthesis.md` ("Across five passes"). Standard: Q19/D80 (a precise object and a convincing argument, not full rigour). Constraints read: D78 (condition 4 above all), D81, D83, D88; Q18, Q19, Q28; reports 8, 9 and 13; `derivation-self-invariant-maps.md` (Theorems 5 and 6); `critique-isospectral-q35.md`; the ledger metric in `design-cayley-ledger.md` §2.13.

Checks: `foundations/sims/conjecture-five-passes/checks.py` (`python3 -I checks.py`; numpy and scipy; about 3 s; output in `out.txt`). They are hand-made instances that verify the mathematics below (K1–K4). They are not evidence about behaviour or about people (brief: no toy worlds).

---

## 0. Result in one paragraph

**(a) Proved, in a sharpened form.** Suppose the guarantee is read the way the ledger states it: the toward slope of the partner-caused part (the difference from the neutral-partner run) stays at or below c_j on every channel j, for every partner policy, measured on the metric's windows. Then every core has, on every channel, a bound on its **steerable gain**: the amount by which any two partner behaviours can make the agent's channel j differ. This holds for every core, however nonlinear, learning or non-stationary. The bound is c_j per unit of his movement on that channel, with a floor of about 6 c_j σ₀ (Theorem 1). It applies to every route at once (face, words, timing, appraisal, contingency), as a total at the output. For linear time-invariant cores the guarantee and a weighted H∞ row-gain bound are exactly equivalent (Theorem 2; K1: predicted 0.098, measured 0.098).

**Contingency plays no part in the proof.** "You responded to me" is itself a partner behaviour, so its effect on expression falls under the same bound (Corollary 1b). Self-invariance is not a second way to the guarantee: it removes the partner's answers, but leaves his news uncapped (Corollary 1c; K2c: exactly invariant to 2 × 10⁻¹⁶, toward slope 54 c).

**(b) The literal conjecture has one counterexample.** It needs the expectation or long-run reading of the guarantee: **private randomisation**. A fresh secret sign on a high-gain response gives unbounded gain with a long-run slope equal to c for every partner policy (Proposition 4). It fails the ledger's finite windows unless the gain is small. It is a known mechanism (the mixed strategy of matching pennies; dither), and as a face it is noise, not a candidate.

**(c) Two sub-claims remain open.** The first is the gap between the necessary pairwise bound and a sufficient full incremental-gain bound for nonlinear cores with memory (§5, O1). The second is whether a guarantee over a *modelled* class of partners, not every partner, could do without the bound (O3). That second question changes the promise; it is not a gap in the proof.

---

## 1. Precise statement

### 1.1 Spaces and the class of cores
- **Time.** t ∈ ℤ≥0, at the camera rate.
- **The agent's own channels.** j = 1, …, m; own expression y_t ∈ [0, 1]^m (face, voice and timing channels in the agent's own coordinates).
- **Partner input.** u_t ∈ 𝒰 is everything the agent receives from the partner: face and voice features read into its own coordinates, his words, his timing events.
  - For each own channel j, a coordinate map gives his **counterpart** p_{j,t} = π_j(u_t) ∈ [0, 1]: his same expression in the agent's coordinates.
  - u⁰ is the neutral partner: his neutral face, silence.
  - Which coordinates u⁰ holds neutral is part of the definition (see §4, point 3).
- **The agent's private randomness ξ.** Own noise, body, sampling. The partner sees ξ only through y.
- **A core.** A causal map Γ with y_t = Γ_t(u_{≤t−1}, ξ_{≤t}). All learning belongs to Γ: parameters updated causally from the same data, nightly replay included.
- **The core class 𝒞.** Every setting the core can learn into. **Innate** means: true of every member of 𝒞.
- **Partner-caused part** (the shadow run, the neutral counterfactual): Δ_t(u, ξ) = Γ_t(u, ξ) − Γ_t(u⁰, ξ).

### 1.2 The class of partner policies
Π is the set of all causal maps u_t = P_t(y_{≤t−1}, ε_{≤t}) with values in the admissible range, where ε is the partner's own randomness, independent of ξ. Π contains:
- open-loop partners, who ignore the agent;
- mirrors, at any gain, lag, sign or cross-channel map;
- contingent partners, responsive in some periods and not in others;
- adversaries who know Γ exactly.

### 1.3 The toward slope (the ledger's metric)
- Fix a channel j, a lag L ∈ ℒ = [0, L_max], a block length b and a window.
- Form the block means P̄_n of his counterpart p_j shifted by L, and D̄_n of Δ_j, over the window.
- Then

  β_j(L) = Ĉov(D̄, P̄) / max(V̂ar(P̄), σ₀²),

  with the ledger's floor σ₀ = 0.03 on the SD of his block means. The ledger's own rule below the floor ("swing ≤ c × his within-window range") gives the same orders of magnitude.

### 1.4 The guarantee: "no copy attractor for every partner policy"
**CG(c).** For every Γ ∈ 𝒞, every P ∈ Π, almost surely in (ξ, ε), every window and every L ∈ ℒ: β_j(L) ≤ c_j on every channel.
- **CG_E** is the expectation or long-run variant: the same bound on the slope computed in the long-window limit, or on E[Δ | u].
- **Why this is the right reading of D78 condition 4** (Proposition 3, K4). Copying as a *dynamical* attractor of the dyad cannot be excluded for every partner policy by any core that responds at all. A mirror whose gain exceeds 1/c_j locks the dyad at the rails for any c_j > 0. K4: with c = 0.05 and partner gain 40, the partner's final means are 0.00 to 1.00, and the agent's partner-caused offset is ±0.025 = c × 0.5. At partner gain 10 nothing locks.
- What an agent can guarantee is its own share: the partner-caused part does not follow. Under "every partner policy", D78's condition 3 (innate ceiling) and condition 4 (copy not attracting) therefore become **one condition, CG**.

### 1.5 "Contingency kept"
- **Kept in the state.** There are ε, g ≠ 0 and Γ ∈ 𝒞 for which the agent's state trajectory under u = ε + g(y) differs from its trajectory under u = ε. This is the negation of Theorem 6c of the derivation.
- **Expressed on channel j.** The difference reaches Δ_j.
- Contingency kept only in the state is compatible with anything. D81 allows full knowing, so the conjecture is only about expression.

### 1.6 "Per-channel gain bound" and "innate ceiling"
- **Steerable gain on channel j.** Let B and B′ be any two partner behaviours (members of Π, contingent ones included) that hold his counterpart block means at constants μ_B and μ_B′. Run them alternately in blocks. Let D̄_B and D̄_B′ be the means of Δ_j over B blocks and B′ blocks within a window. The steerable gain is the largest value of |D̄_B − D̄_B′| relative to max(|μ_B − μ_B′|, 2σ₀).
- **Innate ceiling.** A value c_j, fixed for the whole class 𝒞, that bounds the steerable gain. It is not learned and is the same for every partner.
- **The conjecture as stated in the synthesis:** CG(c) + contingency kept ⇒ an innate per-channel gain bound.

---

## 2. Two structural lemmas

**Lemma 1 (for a deterministic core, "every partner policy" means "every partner path").**
- Let Γ be deterministic given ξ, and let the partner observe y.
- Under a closed-loop policy, Δ is computed by replaying the realised path u against u⁰ with the same ξ. Its value is the open-loop Δ on that path.
- Every path can be produced by an open-loop policy.
- So the supremum over Π of any slope of Δ equals the supremum over admissible paths.

*Argument.* Δ_t(u, ξ) depends only on (u, ξ), not on how u arose. ∎

*Consequence.* For the necessity direction, closed loops and small-gain arguments add nothing. The question is open-loop: what must Γ satisfy so that **no path** makes Δ_j follow p_j?
- **Exception:** a core with private randomness. A closed-loop partner can then condition on past ξ through y, which is an adaptive adversary. That is where randomisation can be beaten (K3, the held sign).

**Lemma 2 (with a two-valued regressor, the slope is a difference of group means).**
- In a window where P̄ takes the value μ on n blocks and μ′ on n blocks, |μ − μ′| ≥ 2σ₀, the slope is exactly β = (D̄_μ − D̄_μ′)/(μ − μ′).
- This holds whatever D̄ does inside each group. The floor does not bind, since V̂ar = (μ − μ′)²/4 ≥ σ₀².

*Argument.* This is OLS on a binary regressor. ∎

---

## 3. Results

### Theorem 1 (steerability: the guarantee is a per-channel bound on steerable gain)

**Statement.** Assume CG(c) with block length b, windows of at least 2b, and 0 ∈ ℒ. Then, for every core Γ ∈ 𝒞 (deterministic, or pathwise almost surely), every channel j, and every pair of partner behaviours B and B′ alternated in blocks of length b, in every window:
- (i) if |μ_B − μ_B′| ≥ 2σ₀: |D̄_B − D̄_B′| ≤ c_j |μ_B − μ_B′|;
- (ii) if B and B′ hold his counterpart at the same or nearly the same level: |D̄_B − D̄_B′| ≤ 6 c_j σ₀.

**Argument.**
- (i) The partner runs B and B′ in alternate blocks and holds p_j at the block constant. He is free to make either behaviour the one with the higher counterpart level.
- By Lemma 2, β_j(0) = ±(D̄_B − D̄_B′)/(μ_B − μ_B′), with the sign his to choose. CG then bounds the absolute value.
- (ii) Insert B″: B′ with his counterpart shifted so that |μ_B″ − μ_B| = 2σ₀ and |μ_B″ − μ_B′| ≤ 4σ₀. Apply (i) twice and the triangle inequality.
- The shifted behaviour is admissible wherever the range leaves 2σ₀ of room. ∎

**What the theorem does not assume.** No linearity, stationarity, fading memory or time invariance. "D̄_B" is whatever the agent actually does in those blocks, learning included. The only requirements:
- the partner can hold his counterpart channel at a level while doing anything else;
- the metric looks at that block scale.

**Corollary 1a (the bound covers every route, as a total at the output).**
- B and B′ may differ in anything the partner controls: his words (sad news or none), his other channels, his tempo, his breathing, his responsiveness.
- The theorem bounds the **sum** of every route's effect on channel j.
- Per-route caps are one way to meet it, if their sup-gains add up to at most c_j, as the ledger's counted routes do (≤ 0.974 c_k). Measuring at the output is another (the ledger's net). A bound on the internal state alone cannot meet it. This is the conclusion of the isospectral critique, now as a theorem.

**Corollary 1b (contingency is a steerable route).**
- Take B = "answers the agent" (u = ε + g(y)) and B′ = "does not answer" (u = ε), with the same counterpart level.
- Then the expressed effect of "you responded to me" on channel j is at most 6 c_j σ₀.
- On LD (c = 0.05) that is 0.009, and 0.0030 at the 2c_jσ₀ scale of K2. Contingency may be known without limit (D81), but it may move each expression only inside the ceiling.
- K2b: an agent whose channel j reads its own estimate of the partner's responsiveness (tanh of an exponentially weighted regression coefficient) at amplitude 0.058 is driven to 20 c by a partner who alternates answering and not answering every 30 s and moves his counterpart by ±σ₀ in step. Predicted 20.3 c.

**Corollary 1c (self-invariance is not an alternative to the bound).**
- Theorem 6 of the derivation gives zero loop gain through the partner's answers g(y) ∈ ⟨G⟩. The partner's **news** ε is a behaviour he controls, and Theorem 1 applies to it unchanged.
- K2c: an exact OLS echo canceller (invariance checked to 2.2 × 10⁻¹⁶) passing his news on another channel at amplitude 0.16 gives 54 c against a co-modulating partner (predicted 54.4 c).
- This corrects one sentence of the synthesis ("a guarantee for every partner policy can come only from invariance or from a gain bound"). Invariance gives no such guarantee; only the bound does. Invariance removes one route (the partner's following) from the loop, which is how the derivation already placed it (§6, "the honest accounting").

**Corollary 1d (zero ceilings).**
- c_j = 0 forces D̄_B = D̄_B′ for **every** pair of partner behaviours.
- On the zero-ceiling channels (anger, disgust, contempt; D83), nothing the partner does may move the agent's expression at the metric's scales. This includes his words, if the counterfactual neutralises them (§4, point 3).

### Theorem 2 (linear time-invariant cores: exact equivalence with a weighted H∞ row bound)

**Statement.** Let Δ_j = Σ_i K_ji ∗ v_i, where:
- v_1 = p_j − p⁰_j is his counterpart;
- v_i, i ≥ 2, are his other inputs (other channels, word or timing signals), with admissible amplitude a_i;
- the metric is the frame-level slope over long windows, with lags dense on [0, L_max] and L_max at least the longest period that matters.

Then

  sup_{P ∈ Π} β_j = sup_ω [ |K_j1(ω)| + Σ_{i≥2} (a_i / (√2 σ₀)) |K_ji(ω)| ].

So CG(c) holds exactly when this weighted row gain is at most c_j: a per-channel gain bound in the strict sense.

**Argument.**
- **Upper bound.** For a stationary input, the slope at lag L is ∫ Re[(K_j1 S_11 + Σ_i K_ji S_i1)(ω) e^{iωL}] dω / ∫ S_11, where S are the (cross-)spectra.
  - Cauchy–Schwarz bounds |S_i1| by √(S_ii S_11).
  - The amplitude limits bound S_ii relative to S_11, which is at least σ₀² by the floor.
  - A ratio of integrals is at most the supremum of its integrand.
- **Lower bound.** Let v_1 be a sinusoid at the maximising ω with SD σ₀, and each v_i a sinusoid at the same ω with amplitude a_i and its phase set so that every term aligns with K_j1. The lag then takes up the common phase. ∎
- **K1:** a resonant own-channel response (|K_11| peak 0.084 at 0.2 Hz) plus a weak cross route (DC 0.003). Predicted supremum 0.098; the adversarial sinusoid pair gives 0.098. With the cross route silent, 0.084 = ‖K_11‖_∞. A natural OU partner gives 0.022, so the supremum is reached only by a partner who aims at it.
- **What K1 shows.** Cross routes enter weighted by a_i/(√2 σ₀), here about 7. A route from his *other* inputs costs about seven times its own gain against the ceiling, because the partner can keep his counterpart at the floor while driving the cross input at full range. This is the reserved-partner effect that report 8 and the isospectral critique met.

### Proposition 3 (for every partner policy, the dynamical copy attractor cannot be excluded)
- Let channel j have any nonzero response, with saturation.
- Then a mirroring partner with gain above 1/(the agent's gain) makes the copy configuration (both at the same rail) attracting.
- The agent's share of the locked state is bounded by its own ceiling: K4, an offset of ±0.025 = c × 0.5.

*Argument.* At such a gain the loop gain exceeds 1 and saturation gives fixed points at the rails. ∎

So "no copy attractor for every partner policy" can only mean CG (§1.4).

### Proposition 4 (the counterexample: private randomisation)

**The core.**
- Let Δ_{j,t} = (c + k s_t) x_{t−d}, with x = p_j − p̄_j, d ≥ 1, and s_t ∈ {±1} i.i.d. and private, drawn fresh at every frame.
- Its incremental gain is c + k, with k as large as one likes.
- E[Δ | u] = c x_{t−d}: the conditional-mean gain is c.

**What it satisfies.**
- **CG_E holds for every partner policy.** s_t is independent of everything the partner's x_{t−d} depends on, which reaches back only to y_{≤t−d−1}. Σ s_t x²_{t−d} / Σ x² is therefore a martingale ratio and tends to 0 whenever no single sample dominates. So the long-run slope tends to c.
- **Contingency** can be kept by any other route; the randomised part may read it too.

**Checks (K3).**
- **Long run.** For k = 1 and 10, the pooled 1-h slope is −0.72 to 1.04 c against a co-modulating square wave, a natural partner, and a closed-loop exploiter who reads the agent's last sign from its face and modulates his amplitude.
- **It fails CG at finite windows.** At k = 10, the worst 60-s window reads 20–48 c (1.0–1.2 c at k = 0). The ledger's pooled 1-h block metric reads 3.5 c on a natural partner, from sampling noise alone. Under the pathwise metric the random part's gain is itself bounded, by about c √N_eff over the window's effective sample count.
- **The randomness must be fresh at every reaction step.** With the sign held for 2 s, the exploiter reaches 15 c (k = 1) and 136 c (k = 10). That is Lemma 1's exception: an adaptive adversary.

**Judgement.** It is a known mechanism: the mixed equilibrium of matching pennies, which is the copier-versus-differentiator game of pass 5, read in Ghani et al.'s terms; dither in control. It is not a candidate core:
- it adds partner-driven noise to the face, which is no component of the brief;
- D81's fast partial mimicry must still sit inside c;
- it meets only the long-run reading, which the ledger does not use.

---

## 4. What follows for the conjecture and the design

1. **The conjecture is true in the form that matters.** Under the ledger's pathwise metric, any core that meets the copy guarantee for every partner policy has an innate per-channel bound on steerable gain, on every route summed. Keeping contingency does not avoid it, because contingency is one of the things it bounds.
   - The bound is c_j itself, the ceiling the guarantee is stated with. No core can do without the ceiling. A core can differ only in **how** the ceiling is enforced:
     - per-route caps whose sup-gains sum to at most c_j (Theorem 2 gives the exact weights);
     - an output-side governor;
     - normalisation by an estimate of the partner's own gain (R2 of the derivation, which is κ_j/s, a cap).
2. **The only escape is private randomness under a long-run reading** (Proposition 4). It is known and useless.
3. **The guarantee is only as wide as the counterfactual.**
   - Theorem 1 bounds the effect of everything the shadow run holds neutral.
   - **If u⁰ neutralises his words,** D83's strong appraisal-driven expressions are bounded at about 6 c_j σ₀ against a partner who co-modulates. For example, he frowns 0.03 while telling sad news: K2a, where a words-driven display of amplitude 0.08 reads 28 c. Anger at an insult is then impossible on a zero-ceiling channel (Corollary 1d).
   - **If u⁰ does not neutralise his words,** the words route is outside the guarantee. A partner whose sad words come with a slight frown then gets real following through it, which the metric does not count.
   - Real partners co-vary their words and face naturally. So this is not only an adversarial case. In K2a the natural partner's words were independent of his face, and it read ≤ 1.4 c.
   - The design must state which inputs u⁰ holds neutral. That choice decides what D83 allows and where the guarantee stops. I did not establish from the design text which choice the build makes.
4. **Time scales.** The bound reaches exactly the scales the metric resolves. Effects slower than the longest window or the pooling span are not constrained, for example cross-session effects through nightly learning, which the design already declares outside the within-session ledger (its audit row S23). A cross-session ceiling would need a cross-session metric. This is a fact about scope, not a gap in the proof.
5. **For Q35.** The theorem explains why every algebraic net on the internal state has failed. The bound is a statement about the output relative to his counterpart, summed over all routes, so a catch-all net must measure there. The ledger's design is the right shape. The size of its margin remains an engineering question.

---

## 5. What is not proved (open sub-claims)

- **O1. Necessity versus sufficiency for nonlinear cores with memory.**
  - Theorem 1 bounds **pairwise** steerable differences at block scale; it is necessary.
  - A sufficient condition is a weighted incremental ℓ² gain bound from the block-level partner input to D̄_j: by Cauchy–Schwarz, slope ≤ SD(D̄)/max(SD(P̄), σ₀).
  - For linear time-invariant cores the two meet (Theorem 2). For nonlinear cores with memory they do not obviously meet. A core can satisfy the pairwise bound while a lagged, history-dependent response to graded partner paths still exceeds c at some lag.
  - What is open is a characterisation of CG for nonlinear cores that is both necessary and sufficient. The likely object is an incremental-gain bound on the block-level operator, weighted as in Theorem 2.
  - This does not affect the conclusion that a bound is forced. It affects only how tight the bound must be.
- **O2. Shifting his counterpart needs room in the range.** At a rail, Theorem 1(ii) holds only one-sidedly. This is minor.
- **O3. Guarantees over a modelled partner class.** If Π is restricted, for example to partners whose words are independent of their face, or to stationary partners who do not aim at the agent's routes, the co-modulation construction is not available. A core with large steerable routes can then pass: K2's natural partners read ≤ 1.6 c even at amplitudes that read 54–135 c against the adversary. Whether a broad, defensible partner model admits a guarantee without a gain bound is open. It is a different promise ("for the partners we expect", not "for every partner"), so it is for the operator to decide, not a proof gap.
- **Assumptions that made parts easy.**
  - Theorem 1 needs only determinism (or the pathwise reading) and a partner able to hold his counterpart channel at a level.
  - Theorem 2 uses linearity, time invariance and long windows. Its exact formula does not survive without them, but the necessity of Theorem 1 does.
  - Lemma 1 uses determinism given ξ. With private randomness, the closed-loop class is strictly larger.

---

## 6. Numerical checks (K1–K4, `sims/conjecture-five-passes/out.txt`)

| Check | Construction | Result |
|---|---|---|
| K1 | LTI core: resonant own route plus weak cross route; adversarial sinusoid pair vs natural OU partner | sup slope predicted 0.098, measured 0.098; own route alone 0.084 = ‖K₁₁‖∞; natural partner 0.022 |
| K2a | words-driven display, partner alternates sad words and none every 30 s with his counterpart at ±σ₀ | amplitude 0.0015 → 1.47 c (pred. 1.50); 0.08 → 27.7 c (27.9); 0.40 → 135 c (135); natural partner ≤ 1.4 c |
| K2b | contingency read (tanh of his estimated response gain), partner alternates answering and not answering | 0.0015 → 1.47 c; 0.058 → 20.2 c (20.3); 0.29 → 97 c (97); natural ≤ 1.0 c |
| K2c | exactly invariant echo-cancelled news (2.2 × 10⁻¹⁶) | 0.0015 → 1.47 c; 0.032 → 11.6 c (11.7); 0.16 → 54 c (54.4); natural ≤ 1.6 c |
| K3 | private fresh sign, gain k = 1 and 10 | long-run −0.72 to 1.04 c (all partners, closed-loop exploiter included); worst 60-s window 20–48 c at k = 10; sign held 2 s, with exploiter: 15 c and 136 c |
| K4 | saturating dyad, mirror with gain 10 vs 40, c = 0.05 | no lock at loop gain 0.5; rails locked at 2.0, agent offset ±0.025 = c × 0.5 |

All the ledger-style figures use 30-s block means, lags 0–300 s in 10-s steps, and the floor σ₀ = 0.03. In K2, the mimicry share alone reads 0.97 c, so the allowed amplitude of every other steerable route together is close to zero. That is the 2 c σ₀ = 0.003 scale on LD.

---

## 7. For the operator: what this means for the search (D82)

For five passes the search looked for a new core that would never get stuck copying you, whatever you do, without a built-in limit on each expression and without going blind to "you responded to me". This note shows that no such core exists. Take any core with that promise. If you alternate between two ways of behaving, and move your own eyebrow very slightly in step, the agent's eyebrow difference between the two shows up as following your eyebrow. So the promise itself is a limit on how much anything you do, your words and your responsiveness included, can move each of the agent's expressions. A new core cannot remove the limit; it can only enforce it differently. The main design already has it, both route by route and as an output-side check.

The one loophole is to make the agent's reactions secretly random. It is a known trick, it only works in the long-run average, and it would make the face noisy, so it is no candidate.

What remains open is a choice, not a proof. One choice is which of your inputs the agent's "what if you had stayed neutral" run holds still: if it includes your words, strong expressions in response to your words are limited too. The other is whether the promise should hold "for every partner" or only for the kinds of partners we expect.

My recommendation is to stop searching for a core that avoids the per-expression limits. If the search continues, it should take the limits as given and look for novelty where the brief asks for it (attention, structure, time scales). This note does not settle that choice.


## Note (2026-11-28T00:50:12Z): pass 10 on the open gap

research/new-core-search-10-synthesis.md: for learned routes built as robust recurrent equilibrium networks, one per channel with a 1-Lipschitz readout, the per-channel incremental gain from the partner-input path is bounded by construction for every parameter value, which closes the necessary-vs-sufficient gap for those routes in the long-window reading of the slope. The pathwise reading (every window and lag) is not met by any gain bound (a lag-timed partner pushes a plain linear copy at 0.5 c to 1.11 c), so the ledger stays. Recombination (RENs/IQCs).
