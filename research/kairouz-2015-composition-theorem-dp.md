# The composition theorem for differential privacy (Kairouz, Oh & Viswanath)

Peter Kairouz, Sewoong Oh & Pramod Viswanath, "The Composition Theorem for Differential Privacy", ICML 2015 (pp. 1376–1385); extended version arXiv:1311.0776v4 (6 Dec 2015), 32 pp.; journal version *IEEE Trans. Inf. Theory* 63(6), 2017.

This note stands in for **Dwork & Roth 2014, *The Algorithmic Foundations of Differential Privacy*** (ch. 2–3). The book's host (cis.upenn.edu) was not reachable from this session, so the book was not read. Kairouz et al. restate the standard definition, post-processing, basic composition and the Dwork–Rothblum–Vadhan 2010 advanced composition theorem (their Theorems 3.1–3.2), and those restatements are what is cited here. **Dwork, Rothblum & Vadhan 2010 itself was not read.**

## What was read
arXiv v4, extracted text.
- **Read in full:** §1 (introduction, Definition 1.1), §2 (DP as hypothesis testing: Theorem 2.1, privacy regions, Corollary 2.3, the data-processing inequality Theorem 2.4 and its converse Theorem 2.5), §3 (composition experiment, Theorems 3.1–3.5), §4 (noise variance under composition, Corollaries 4.1–4.2, Theorems 4.3–4.4), §5 (multi-party DP; randomized response is optimal, Theorem 5.1).
- **Read the opening only:** §6 (the achievability construction, eqs. 17–18).
- **Not read:** the remaining proofs (§6 converse, §7–9, appendices).

## The computation, precisely

**Definition 1.1.** A randomized mechanism M is (ε, δ)-differentially private if, for all neighbouring inputs D ~ D′ and all output sets S,

  P(M(D) ∈ S) ≤ e^ε P(M(D′) ∈ S) + δ.

"Neighbouring" is a design choice. Here it means "differ in one individual", but the theorems hold for any symmetric relation.

**Theorem 2.1 (DP is a limit on hypothesis tests).** M is (ε, δ)-DP iff, for every pair of neighbours and every rejection region S (H₀: the output came from D₀; H₁: from D₁),

  P_FA + e^ε P_MD ≥ 1 − δ  and  e^ε P_FA + P_MD ≥ 1 − δ.

So **no observer, with any test, can tell neighbours apart** with both error rates small. The privacy region R(ε, δ) is the set of (P_MD, P_FA) pairs allowed. M is (ε, δ)-DP iff R(M) ⊆ R(ε, δ) (Corollary 2.3).

**Theorem 2.4 (data processing).** If the chain D–X–Y is Markov (Y depends on D only through X = M(D)), then R(M′, D₁, D₂) ⊆ R(M, D₁, D₂). **Anything computed from a private output is at least as private, for every pair of inputs.**

**Theorem 2.5 (the converse, Blackwell 1953).** If the privacy region of M′ lies inside that of M, then M′ *is* a post-processing of M under some coupling. So the privacy region is the complete invariant: **two mechanisms with the same region cannot be told apart by any downstream use.**

**Composition experiment (after DRV10).** For i = 1..k, an adversary picks a neighbouring pair (D_{i,0}, D_{i,1}), a query and a mechanism M_i from a class 𝓜, **adaptively, as a function of all previous outputs**. It receives y_i = M_i(D_{i,b}). Its view is V^b = (R, Y₁^b, …, Y_k^b). Privacy of the composition means V⁰ and V¹ are (ε̃, δ̃)-indistinguishable.

**Theorem 3.1 (basic composition).** k-fold adaptive composition of (ε, δ)-DP mechanisms is (kε, kδ)-DP. Heterogeneous: (Σ ε_i, Σ δ_i). This is tight if no extra δ is allowed.

**Theorem 3.2 (advanced composition, DRV10 Theorem III.3, as restated).** For any δ̃ ∈ (0, 1], k-fold adaptive composition of (ε, δ)-DP mechanisms is (ε̃, kδ + δ̃)-DP with

  ε̃ = kε(e^ε − 1) + ε √(2k log(1/δ̃)).

**Theorem 3.3 (optimal composition).** The class of (ε, δ)-DP mechanisms under k-fold adaptive composition satisfies, for every i = 0..⌊k/2⌋,

  ((k − 2i)ε, 1 − (1 − δ)^k (1 − δ_i))-DP,  δ_i = Σ_{ℓ=0}^{i−1} C(k, ℓ)(e^{(k−ℓ)ε} − e^{(k−2i+ℓ)ε}) / (1 + e^ε)^k.

The exact region is the intersection of these. It is achieved by composing the four-outcome randomized response of eqs. 17–18, so no family can degrade privacy more.

**Theorem 3.4 (closed form).**

  ε̃ = min{ kε, (e^ε − 1)εk/(e^ε + 1) + ε √(2k log(e + √(kε²)/δ̃)), (e^ε − 1)εk/(e^ε + 1) + ε √(2k log(1/δ̃)) },

with δ-part 1 − (1 − δ)^k(1 − δ̃). For ε ≤ 0.9 the first-order terms are kε² and ε√(2k log(·)). **Privacy loss grows like √k, not k, once a small δ̃ is allowed.** Theorem 3.5: for heterogeneous ε_ℓ, replace kε² by Σ ε_ℓ² and kε by Σ ε_ℓ.

**Noise under composition (Theorem 4.3).** For real queries with sensitivity Δ = max_{D~D′}|q(D) − q(D′)|, Gaussian noise with variance 8kΔ² log(e + ε/δ)/ε² gives (ε, δ)-DP under k-fold adaptive composition. Laplace and staircase noise give the same privacy at about the same variance (Corollaries 4.1–4.2): "there is nothing special about … Gaussian noise".

**Theorem 5.1 (randomizing at the source is optimal).** In k-party computation with local (ε_i, δ_i) constraints, *non-interactive* randomized response of each party's own bit, followed by optimal decoding, maximises every party's accuracy over all interactive private protocols. The authors note a precondition: "Differential privacy implicitly imposes independence in a multi-party setting."

## Evidence with numbers
These are theorems, not data. The paper's worked comparison (Figure 3) uses 30-fold composition of (0.1, 0.001)-DP mechanisms, where Theorem 3.3's region is visibly tighter than Theorems 3.1 and 3.2. Theorem 4.3 improves the known sufficient Gaussian variance by a log(1/δ) factor when δ = Θ(ε).

## What it means for the designs
Let M be the whole agent: partner input stream P → (face synergies, voice prosody, Claude's draft choice, memory writes, learned weights). Suppose M is (ε, δ)-DP with respect to a neighbouring relation ~ on partner streams.

1. **The guarantee is on every route at once.** Theorem 2.1 is a statement about the joint output distribution. It counts any route by which the partner moves any output: the base tilt (K1), event proposals that see ℓ − b̃ (K3), and Claude's selection reading ŝ (K9). None of them needs to be enumerated. They all spend the same ε. This is what per-route caps never had.
2. **Post-processing closure (Theorem 2.4) covers the agent's own downstream state.** A slow integrator that reads only the agent's own face, a memory consolidation that reads only the agent's own logs, a learner trained only on the agent's own outputs: each is post-processing and costs nothing extra. *But* any component that reads the raw partner stream is not post-processing. It is part of M and must be inside the proof. The "route-completeness" lemma of every design reappears as one structural check: **is the sanitizer the only component that touches partner data?** That is a taint check on the code graph, much easier than the Jacobian inventories the critiques had to do.
3. **Adaptive interaction is already in the definition.** In the composition experiment the adversary chooses the next query after seeing earlier outputs. In the dyad, the partner chooses their next expression after seeing the agent's face. That is the same game, with the partner as adversary.
4. **A copy ceiling straight from Theorem 2.1** (my derivation). Let p, p′ be partner histories that are neighbours. Let the agent "copy" mean that some statistic of its output (for example its window-mean face on one synergy) lands within half the p–p′ gap of the partner's value, with probability q under both. The test "statistic above the midpoint" then has P_FA, P_MD ≤ 1 − q. Theorem 2.1 gives (1 − q)(1 + e^ε) ≥ 1 − δ, so

   **q ≤ (e^ε + δ)/(1 + e^ε).**

   With δ = 0: ε = 0.1 → q ≤ 0.525 (chance); ε = 1 → 0.73; ε = 3 → 0.95. This bounds copying at the resolution set by the neighbouring relation, over every route and every adaptive partner, for every downstream use of the output.
5. **Composition sets the cost of hours.** Theorem 3.4 says the loss grows as √k. Over an hour at 10 Hz (k = 36,000 frames), an hourly user-level budget of ε̃ = 1 with δ̃ = 10⁻⁵ allows about ε ≈ 1/√(2k ln 10⁵) ≈ 0.0011 per frame (my arithmetic, leading term only). That is useless for a reflex. So **the neighbouring relation cannot be "any frame differs" composed over hours**. It must be defined directly on the feature to be protected (see mironov-2017 and the synthesis).
6. **Randomize at the gate (Theorem 5.1).** If partner features are privatized at perception (local DP), then everything downstream is post-processing by construction, including Claude, memory and learning. Kairouz et al. show that for multi-party problems this loses nothing relative to interactive protocols. The price is that the agent then *perceives* the partner only through the budget.
7. **It cannot see sign.** Theorem 2.5 says the privacy region is the only invariant. A bijective relabelling of the output (copy y = p versus anti-copy y = −p) has the same region. **DP bounds how much the agent's output depends on the partner, never in which direction.**

## Verdict
**adopt (the definition and its closure properties; a hypothesis-test copy ceiling, q ≤ (e^ε + δ)/(1 + e^ε), on all routes and all adaptive partners).** It is not a new affect computation. It is the accounting currency the per-route designs lacked. The cost is that it is sign-blind, and that composition over hours forces the neighbouring relation to be defined on the protected feature, not on frames.
