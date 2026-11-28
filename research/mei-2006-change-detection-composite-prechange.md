# Sequential change-point detection when unknown parameters are present in the pre-change distribution (Mei)

Yajun Mei, *Annals of Statistics* 34(1), 92–122, 2006; arXiv:math/0605322v2 (15 May 2006). https://arxiv.org/abs/math/0605322

## What was read
arXiv v2, extracted text: §1 and §2 **in full** up to Theorem 2.2 (problem, examples, Lorden's asymptotic efficiency, the open-ended test M(a) with Theorem 2.1 and Corollary 2.1, Lorden's Lemma 2.1 turning an open-ended test into a change detector, the change-point rule M*(a)). §3 (both pre- and post-change composite), §4 (normal means) and §5 (proofs) **not read**.

## What it says, precisely
- **Lorden's bound restated (eq. 1.2):** for each pair (θ, λ), E_λN ≥ (1 + o(1)) log E_θN / I(λ, θ) as E_θN → ∞, where E_λN is Lorden's worst-case delay and I the KL; Page's CUSUM attains it and is exactly optimal (Moustakides 1986; Ritov 1990).
- **Composite pre-change hypothesis, as in "in control while the parameter is below a fixed limit".** If the aim is to maximise the worst ARL to false alarm over pre-change parameters θ ∈ [θ₀, θ₁] subject to a delay constraint at a post-change λ > θ₁, **the exactly optimal rule is the CUSUM designed against the boundary θ₁** (a referee's remark the paper records, §2), because inf_θ E_θN ≤ E_{θ₁}N with equality for that CUSUM.
- Asking for asymptotic efficiency at **every** θ in the interval needs the rule M*(a) (simultaneous one-sided SPRTs at θ₀ and θ₁, restarted at every k), whose delay is a + O(√a); the GLR does **not** give asymptotically optimal procedures under this formulation.
- **Lorden's Lemma 2.1:** from any open-ended test N with P_θ(N < ∞) ≤ α one gets a change detector N* = min_k(N_k + k − 1) with E_θN* ≥ 1/α and delay ≤ E_λN.

## What matters for this engine
1. **The governor's null is composite in exactly this way**: ordinary partners give the partner-caused part some slope anywhere in [0, κ_g c_k] (0.33–0.51 c measured), and only slopes above the boundary κ_g c_k should engage. Mei's remark says the minimax-optimal design is the CUSUM whose pre-change model sits **at the boundary** κ_g c_k, which is what the pass-12 bank does (s₀ = κ_g in units of c_k).
2. **Ordinary partners whose slope sits well below the boundary pay less**: their ARL to false engagement is larger than at the boundary, by a factor that grows with the gap (efficiency at interior θ is what M*(a) improves).
3. Lemma 2.1 is the bridge used in the synthesis between a per-batch test and a running detector.

## Verdict
**adopt (design rule: set the detector's pre-change model at the boundary κ_g c_k).**
