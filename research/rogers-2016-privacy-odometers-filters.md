# Privacy odometers and filters: pay-as-you-go composition (Rogers, Roth, Ullman & Vadhan)

Ryan Rogers, Aaron Roth, Jonathan Ullman & Salil Vadhan, "Privacy Odometers and Filters: Pay-as-you-Go Composition", *NeurIPS 2016*; arXiv:1605.08294v3 (5 Aug 2021, corrected constants), 21 pp.

## What was read
The arXiv v3 text in full: §1 (introduction, Example1/Example2), §2 (preliminaries: Definitions 2.1–2.8, Theorems 2.5, 2.7, 2.9, 2.10), §3 (adaptive-parameter composition: Algorithms 2–3, Definitions 3.1–3.2, Lemma 3.3, Theorem 3.4), §4 (concentration: Theorems 4.1–4.5, Lemma 4.6), §5 (Theorem 5.1 and its proof), §6 (Theorem 6.1 lower bound with Lemmas 6.2–6.3 and Algorithm 4, Lemma 6.4, Theorem 6.5). Proofs were followed in outline, not checked line by line.

## The computation, precisely

**The gap they close.** All earlier composition theorems (DMNS06, DRV10, KOV15) let the *mechanisms* be chosen adaptively, but fix *the number of rounds and each round's (ε_i, δ_i)* in advance. In Example2, which keeps querying while the noisy answer stays below τ, "cannot be said to be differentially private ex ante for any non-trivial fixed values of ε and δ, because the computation might run for an arbitrarily long time that depends on the data itself."

**Privacy loss.** Loss_M(a; x, x′) = log(P[M(x) = a]/P[M(x′) = a]). Over an adaptive interaction with view v, Loss(v) = Σ_i Loss_i(v_{≤i}).

**Adaptive-parameter game (Algorithm 2).** In round i the adversary chooses neighbours, *parameters* (ε_i, δ_i), and an (ε_i, δ_i)-DP mechanism M_i, all as functions of earlier outcomes. Setting ε_i = 0 means stopping.

**Definition 3.1 (privacy filter).** COMP_{εg,δg}: (ε₁, δ₁, …) → {HALT, CONT} is valid if the interaction that runs round i only while the filter says CONT is (ε_g, δ_g)-DP (point-wise indistinguishable), for every adversary.

**Definition 3.2 (privacy odometer).** COMP_{δg}: (ε₁, δ₁, …) → ℝ is valid if, with probability at least 1 − δ_g, |Loss(v)| ≤ COMP_{δg}(ε₁, δ₁, …, ε_k, δ_k), for every adversary. It is a running meter with no pre-set budget.

**Theorem 3.4 (basic composition survives adaptivity).** Σ ε_i is a valid odometer, and "HALT iff Σ ε_i > ε_g" is a valid filter. The proof is one line: |Loss(v)| ≤ Σ_i ε_i(v_{<i}) pointwise.

**Lemma 3.3 (reduction to pure DP).** Rounds with δ_i > 0 are handled by running the pure filter or odometer on 2ε_i, at extra failure probability δ′_g ≥ Σ 2δ_i/(ε_i e^{ε_i}).

**Theorem 5.1 (advanced filter).** With x = ε_g²/(28.04 log(1/δ_g)), let

  K = Σ ε_i(e^{ε_i} − 1)/2 + √( 2(Σ ε_i² + x)(1 + ½ log(Σ ε_i²/x + 1)) log(1/δ_g) ).

Then "HALT iff K > ε_g" is a valid (ε_g, δ_g) filter for δ_g ∈ (0, 1/e). Asymptotically this matches advanced composition, ε_g = Θ(√(Σ ε_i² log(1/δ_g))). The proof uses a self-normalised martingale bound on Σ(Loss_i − μ_i), with μ_i ≤ ε_i(e^{ε_i} − 1)/2 (Lemma 4.6, from Dwork & Rothblum 2016).

**Theorem 6.1 (odometers are strictly weaker).** No valid odometer can achieve Σ ε_i (e^{ε_i} − 1)/(e^{ε_i} + 1) + o(√(Σ ε_i² log(log n/δ_g))). The adversary that forces this (Algorithm 4) uses randomized response with ε = 1/n. **It simply stops at a data-dependent time**, as soon as its realised loss is high. By the law of the iterated logarithm this happens with probability ≥ δ_g.

**Theorem 6.5 (advanced odometer).** It achieves the √(Σε_i² log(log² n/δ_g)) form, losing only a log log factor. This requires Σ ε_i² ∈ [1/n², 1].

## Evidence with numbers
Theorems only. The constant 28.04 in Theorem 5.1 was corrected after publication, which is why the 2021 version was read. The odometer/filter separation disappears when δ_g ≪ 1/n, since log(log n/δ_g) = (1 + o(1)) log(1/δ_g).

## What it means for the designs
1. **The fibred design's token bucket is a privacy filter, if each token is priced.** Its bucket (≤ N tokens per window, HALT when empty) is exactly the Theorem 3.4 filter with ε_i = 1 per token. But it is valid only if every token's firing probability is itself ε_i-DP in the partner. The critique's K3 tracker fires "up" or "down" deterministically on sign(ℓ − b̃). That is ε_i = ∞ per token. The bucket counted events, not information per event, which is why 130 tokens could carry a near-copy.
2. **Adaptive rate dials are allowed, but only as filters.** An agent may choose how much budget to spend from what it has seen. It may spend more when the partner is very expressive, or slow its event rate when it is calm. Theorem 5.1 says this is safe *if* a filter with a fixed global (ε_g, δ_g) can HALT partner-sensitive outputs. It costs only constants over the fixed-schedule bound.
3. **Do not use a running meter as the guarantee.** Theorem 6.1's adversary is just a partner who keeps pushing and stops at a well-chosen moment. An odometer cannot certify √(Σε²) against that. It loses log log n, and it never caps anything. **The budget must be a pre-set innate constant with a halt, not a monitored quantity.** This matches D78's "innate, learning-proof" requirement.
4. **What HALT means for a face.** After HALT, partner-sensitive outputs must stop depending on the partner until the window refreshes. Two things may still run: the agent's own dynamics, and post-processing of what was already released. So the agent keeps expressing, but stops *reacting*, until the window refreshes. This is an explicit, interpretable form of "the partner cannot keep steering": a refractory state, not a gain cap.
5. **Refresh horizon is a temperament decision.** A filter with budget ε_g per hour still lets the partner shift the agent by ε_g per hour, so over days the partner can still set the agent's temperament. The budget horizon (per episode, per day, lifetime) is a value judgement the design must state. It cannot be derived.

## Verdict
**adopt (filters with a fixed innate budget as the valid form of an adaptive rate dial; basic-sum filters are exact; advanced filters cost only constants; odometers are provably weaker).** It also gives an exact diagnosis of the fibred design's bucket: it priced events, not the information each event carries.
