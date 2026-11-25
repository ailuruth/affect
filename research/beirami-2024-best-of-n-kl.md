# Beirami, Agarwal, Berant, D'Amour, Eisenstein, Nagpal & Suresh 2024: Theoretical Guarantees on the Best-of-n Alignment Policy

## Citation

A. Beirami, A. Agarwal, J. Berant, A. D'Amour, J. Eisenstein, C. Nagpal, A. T. Suresh. "Theoretical Guarantees on the Best-of-n Alignment Policy." arXiv 2401.01879, first posted January 2024; version read: v3 (29 May 2025), the ICML 2025 version (PMLR 267). Google DeepMind and Google Research.

## What was read

PDF from arXiv (v3), text extracted with pdftotext.

- Read in full: abstract; sections 1 (intro, Example 1), 2 (derivation of the best-of-n PMF, Lemma 2.3), 3 (the analytical formula as an upper bound; gap upper and lower bounds), 4 (proposed estimator), 5 (win rate), 6 (rewind-and-repeat), 7 (win-rate vs KL trade-offs, Examples 2-3, Conjecture 7.2), 8 (conclusion).
- Appendix read in full: A.1-A.5 (all proofs), B (blockwise best-of-n KL bound), C.1-C.3 (experiment details).
- Figures: the extracted text keeps only captions and axis labels. I did not read curve values off Figures 1-11 except where the text states them.
- I checked: Lemma 2.3 on the binary Example 1; the proof of Theorem 3.1 (steps 48-51); the continuous-limit identity KL = log n − (n−1)/n by integration and by Monte Carlo (n = 8: 1.2032 simulated vs 1.2044 formula, 200,000 draws); Example 1's exact KL against the formula for n = 2, 4, 16, 64 (0.131 vs 0.193; 0.459 vs 0.636; 0.693 vs 1.835; 0.693 vs 3.175 nats).

## Mechanism

**Setting.** Reference policy π_ref(·|x), reward r(x, y). Draw y_1..y_n i.i.d. from π_ref and return y_{k*}, k* = argmax_k r(x, y_k) (Eq. 3). Call the resulting policy π^(n).

**Assumptions.** 2.1: rewards are unique (no ties) for all x, y. 2.2: finite support, |Y*| < ∞. The paper calls both "fairly non-restrictive".

**Lemma 2.3 (the exact best-of-n distribution).** With F(y|x) := P_{z~π_ref}[r(x,z) ≤ r(x,y)] and F⁻(y|x) := P_{z~π_ref}[r(x,z) < r(x,y)] (Eqs. 7-8),

    π^(n)(y|x) = F(y|x)^n − F⁻(y|x)^n        (Eq. 6)

Proof: sampling from π_ref is inverse-CDF sampling with u ~ U[0,1]; best-of-n is the same map applied to max(u_1..u_n), whose CDF is τ^n (Eqs. 9-12). Note that F − F⁻ = π_ref(y|x), so π^(n)(y) = π_ref(y) · [F^n − F⁻^n] / [F − F⁻]. That ratio is the density ratio. (checked)

**Continuous limit (my derivation, consistent with the paper's integrals).** If the score has a continuous distribution under π_ref (no atoms, no ties), F⁻ = F and the ratio becomes a derivative:

    π_n(y) = n · F(r(y))^(n−1) · π(y)

Then KL(π_n‖π) = E[log n + (n−1) log U_max] with U_max ~ Beta(n, 1), E[log U_max] = −1/n, so

    KL(π_n‖π) = log n − (n−1)/n   exactly.   (checked)

The paper's proof of Theorem 3.1 is exactly this integral, ∫_0^1 n v^(n−1) log(n v^(n−1)) dv = log n − (n−1)/n (Lemma A.2), split across the atoms of π_ref.

**The analytical formula and its status (Eq. 4, Theorem 3.1).** The literature (Stiennon et al. 2020, Hilton & Gao 2022, Gao et al. 2023, Coste et al. 2024, and others) states KL(π^(n)‖π_ref) = log n − (n−1)/n =: KL̃_n. The paper: "We disprove the validity of this claim, and show that it is an upper bound on the actual KL divergence." Theorem 3.1: for all n and x,

    KL(π^(n)(·|x) ‖ π_ref(·|x)) ≤ log n − (n−1)/n.

The bound does not depend on π_ref or on r. Proof: per atom, Lemma A.1 (a log-sum / KL ≥ 0 inequality) bounds each term by the integral of n v^(n−1) log(n v^(n−1)) over [F⁻, F]; the intervals tile [0, 1]. (checked)

**When the bound is tight and when it is loose.** Gap G_KL^(n)(x) := KL̃_n − KL ≥ 0 (Eq. 14).
- Upper bound on the gap (Theorem 3.4): G ≤ 2n(n−1) e^(−H_2(π_ref|x)) = 2n(n−1) Σ_y π_ref(y|x)², with H_2 the order-2 Rényi entropy. Corollary 3.5: if every outcome has probability ≤ δ, G ≤ 2n(n−1)δ. So if n²δ ≪ 1, KL ≈ log n − (n−1)/n (Eq. 18). The paper notes this assumption "is left implicit in the derivation of Hilton & Gao (2022)."
- Lower bound on the gap (Theorem 3.6): with ε_∞ := π_ref(y_max|x), the probability of the single highest-reward outcome, G ≥ g_n(1−ε_∞, 1) > 0 (Eq. 21), and as n → ∞, G ≥ log(nε_∞) + o(log n) (Corollary 3.7). When nε_∞ ≫ 1 the gap grows without bound, because the true KL saturates at log(1/ε_∞) while the formula keeps growing like log n.
- Example 1 (binary, π_ref = (½, ½), r = (0, 1)): π^(n)(0) = 2^(−n) and, by Eq. 5, KL = log 2 − h(1/2^n), with h the binary entropy. So KL ≤ log 2 for all n, while the formula diverges. (checked numerically)
- Conclusion paragraph: "if nε_n ≪ 1, the gap ... is small (Theorem 3.4); and if nε_n ≫ 1, the gap between the two may be large and unbounded (Theorem 3.6)."

**Proposed estimator (Section 4).** Let ε_n := π_ref(y|x) for y ~ π^(n) (the reference probability of the selected output; Eq. 19). A loose estimator, D̂_loose(ε_n) = log[(1 − (1−ε_n)^n)/ε_n] (Eq. 23), is an upper bound in expectation (Lemma 4.1) but is loose by (n−1)/n when nε_n ≪ 1. The proposed estimator (Definition 4.3, Eq. 25) is

    D̂_KL(ε_n) = d_n(ε_n),
    d_n(ε) = (1−ε)^n [log n + (n−1) log(1−ε) − (n−1)/n] + (1 − (1−ε)^n) log[(1 − (1−ε)^n)/ε]   (Eq. 24)

Corollary 4.2: KL ≤ d_n(ε_∞) exactly. Lemma 4.5: 0 ≤ d_n(ε_n) ≤ KL̃_n for any realization, so its standard deviation is ≤ log n. Conjecture 4.4 (no proof; "tens of thousands of randomly generated numerical experiments suggest that it holds"): KL ≤ E[d_n(ε_n)]. **The estimator needs π_ref(y|x) of the selected sample, i.e. a sequence log-probability.**

**Win rate (Section 5).** Win rate of π against π_ref under judge r, with ties counted ½ (Eq. 28). Lemma 5.1: win rate = E_{y~π}[C(x,y)], with the calibrated reward C = (F + F⁻)/2 (Eq. 30). Theorem 5.3: win rate of best-of-n ≤ n/(n+1). Gap bounds: ≤ ((n−1)/2) e^(−H_2) (Theorem 5.4), ≥ ε_∞/2 asymptotically (Corollary 5.7). So W ≈ n/(n+1) when nδ ≪ 1 (Eq. 36).

**Rewind-and-repeat (Section 6).** Draw until r ≥ Φ. With w_Φ = P_{π_ref}[r ≥ Φ]: π_Φ(y) = π_ref(y)/w_Φ on the accepted set (Eq. 40); KL = log(1/w_Φ) (Eq. 41); win rate = 1 − w_Φ/2 (Eq. 42); expected trials E[M] = 1/w_Φ. Unbiased KL estimator: H_{M−1}, the (M−1)-th harmonic number (Theorem 6.3). Best-of-n gives a better win-rate-vs-KL trade-off; rewind-and-repeat drives reward up more per unit of compute (Section 8).

**Relation to the KL-regularized optimum.** The paper writes the KL-regularized problem max E[r] − β KL(π‖π_ref) (Eq. 1) and its solution π*_β(y|x) ∝ π_ref(y|x) e^(r(x,y)/β) (Eq. 2; note β here multiplies the KL, so the tilt is 1/β). It cites Yang et al. (2024a) for best-of-n achieving "asymptotically optimal reward-KL tradeoffs" and Gui et al. (2024) for a small win-rate-vs-KL gap. Its own evidence is two toy examples: Example 2 (ternary π_ref = (0.3, 0.6, 0.1), calibrated reward (0.3, 0.75, 0.95)) and Example 3, where the best-of-n trade-off curve is "strikingly close" to the "win rate optimal" curve obtained by varying β in Eq. 2 (Figures 8-9). It also notes Eq. 6 extends to real τ ≥ 1 (π^(τ)), used for best-of-n distillation. **The paper does not propose a soft or "blended" best-of-n.**

**Exact form of that relation (my derivation, not stated in this paper).** In the continuous case, π_n(y) = π(y) · exp[(n−1) log F(r(y)) + log n]. So best-of-n is exactly the exponential tilt π ∝ π · exp(β r̃) with r̃ = log F(r(y)), the log-quantile of the score under π, and β = n − 1. It is the exact KL-regularized optimum for that transformed reward. Two consequences: (a) argmax best-of-n is invariant to any monotone rescaling of r, because only ranks matter; (b) it is not the tilt on r itself, so it cannot be tuned by rescaling r.

**Blockwise best-of-n (Appendix B, Theorem B.1).** Best-of-n over blocks of B tokens: KL ≤ E[⌈|y|/B⌉] · (log n − (n−1)/n). The bound grows linearly in the number of times selection is applied.

## Evidence

- Figure 1 / Example 1: the exact KL stays ≤ log 2 = 0.693 nats for all n, while the formula reaches 3.17 nats at n = 64 (my computation from Eqs. 4-5).
- Figure 2: uniform π_ref over L outcomes. The formula is accurate for n/L ≪ 1 and the KL saturates near n ≈ L.
- Figure 3: cherry-picked distributions where the KL plateaus until a rare high-reward outcome (probability 10⁻⁴, or 10⁻⁵ / 10⁻³ / 10⁻¹) is found. The formula "does not capture the behavior of the KL divergence at all"; the proposed estimator "closely follows" it.
- Figures 4-5, 10-11: Gemma 2 9B IT on four Alpaca and four translation prompts, rewards = log-likelihood (Fig. 4) or negative length (Fig. 5), n ≤ 50. For low-entropy prompts such as "What is the capital of France?" the formula "is loose even for n ≈ 20". The per-prompt ε_∞ values shown in the panel titles run from 0.00 to 0.23.
- Abstract: "very good tradeoffs are achievable with n < 1000."
- Quote (§3): "the analytical formula ... could be relatively accurate ... if πref is a δ-bound model, and n is sufficiently small such that n²δ ≪ 1."

## Available through `claude -p` / Agent SDK?

- **Best-of-n at the draft level: yes.** Run N independent `claude -p` calls (or N SDK queries) on the same context, score each draft in the engine, and keep one. Cost: N calls per reply. Latency: the slowest of N if they run in parallel, or N times one call if they run serially. Rewind-and-repeat (resample until the score passes a threshold) is also available, at expected cost 1/w_Φ calls.
- **The KL itself: not computable.** No logprobs, so ε_n = π(y|x) is unknown. The paper's estimator (Eq. 25) and the exact KL are unavailable.
- **The cap: available, and it needs nothing from Claude.** Theorem 3.1 gives KL(π_N‖π) ≤ log N − (N−1)/N for any π and any score without ties. That is 0.19, 0.64, 1.20, 1.84, 3.17 nats for N = 2, 4, 8, 16, 64. For long free-text drafts, each draft has tiny probability (n²δ ≪ 1), so the bound is nearly tight (my inference from Theorem 3.4).
- **A cruder cap for any selection rule (my derivation, checked).** For any rule that returns one of N i.i.d. drafts (argmax, softmax-weighted, thresholded), P(output = y) ≤ Σ_k P(y_k = y) = N π(y). So the density ratio is ≤ N and KL ≤ log N. With adaptive re-requests (a stopping rule M), P(output = y) ≤ E[M] π(y), so KL ≤ log E[M]. Rewind-and-repeat meets this with equality (Eq. 41: log 1/w_Φ = log E[M]).
- Win rate (Theorem 5.3): the selected draft beats a fresh draft under r with probability ≤ N/(N+1). Ranks are observable, so this is checkable in the engine.

## What it implies for the interface theory

1. **Draft selection is an exponential tilt, with a hard per-reply budget.** Choosing the draft with the highest engine score r_s turns Claude's draft distribution π into π_N(y) = N F_s(r_s(y))^(N−1) π(y). That is an exact tilt of π by the log-quantile of r_s, with strength N−1 (my derivation above). However the state is encoded in r_s, the selected reply differs from what Claude would have said by at most log N − (N−1)/N nats. If draft selection is the only state-dependent step, the mutual information between the state and the reply is bounded too. I(S; Y | context) = min_q E_s KL(P_{Y|s}‖q) ≤ E_s KL(π_N^s‖π) ≤ log N − (N−1)/N (my derivation, checked). At N = 4 that is 0.64 nats (0.92 bits) per reply; at N = 8, 1.20 nats (1.74 bits).
2. **The threshold-and-redraft rule in efference-memory §2.5 has the same shape of cap.** "If none exceeds a threshold ... new drafts are requested" is best-of-N mixed with rewind-and-repeat. Its cap is log E[total drafts per reply], not log N. Steering grows only logarithmically with spend: each extra nat of steering multiplies the expected number of `claude -p` calls by e (my inference from Eq. 41 and the union bound). The softmax rule in v2-llm-interface-linguist (speak draft i with probability ∝ exp(β · sayability)) is also capped at log N. It tilts less than argmax: as β → ∞ it becomes argmax; as N → ∞ it approaches π ∝ π exp(β r) (my inference).
3. **Draft collapse in exact terms.** The bound is reached only when the N drafts are distinct, low-probability outputs (n²δ ≪ 1). It collapses when Claude's drafts concentrate. If one draft type has mass ε_∞ under π, the KL saturates near log(1/ε_∞) (Theorem 3.6, Example 1: two equiprobable outcomes cap KL at log 2 for every n). What matters for the interface is the spread of r_s across drafts, not the spread of the text. Two failure cases (my inference). If differences in r_s across drafts are only noise, selection is a uniform pick: π_N ≈ π, KL ≈ 0. If r_s ranks drafts the same way whatever the state is, the KL can be near the bound while I(S;Y) ≈ 0: the tilt is real but carries no state. A measurable proxy without logprobs: the number of distinct r_s ranks among N drafts, and how stable the argmax is across states for a fixed draft set.
4. **History and Principle 4.** The chosen draft enters the transcript, so later calls read text that the state selected. The text is Claude's own words: no numbers, labels or body values. That matches the letter of Principle 4. But over T turns the history can carry up to T · (log N − (N−1)/N) nats of state information (my inference, by the chain rule, if each turn's drafts are i.i.d. given the history). Claude then "reads the state" in the weak sense that its later behaviour can be conditioned on a selection history that is correlated with state. I would treat this as the intended channel ("the state reaches Claude only by changing how it processes"), not a violation. It is bounded, and it is in the space of things Claude would have said anyway: support(π_N) ⊆ support(π).
5. **Goodhart.** The paper treats r as given. The overoptimization risk when r_s is a proxy is in Gao et al. 2023 (see gao-2023-reward-overoptimization.md). This paper adds one point: the KL budget limits how far selection can drift from Claude's own distribution, and a small N keeps the engine's proxy within the regime where it was fitted.

## Verdict

Adopt: the bound log N − (N−1)/N ≤ log N (and log E[M] with redrafts) is the hard, logprob-free cap on how much the state can steer each reply by draft selection, and Lemma 2.3 is the exact selection distribution to put in the interface theory.
