# Rényi differential privacy (Mironov)

Ilya Mironov, "Rényi Differential Privacy", *Proc. IEEE 30th Computer Security Foundations Symposium (CSF)*, 2017, pp. 263–275; arXiv:1702.07476v3 (25 Aug 2017), 13 pp.

## What was read
The whole arXiv v3 text: §I–VIII and the property table (Table I) and mechanism table (Table II). The appendix propositions (8–11) were read where they are cited in the text (probability preservation, monotonicity, weak triangle inequality); their proofs were not checked.

## The computation, precisely

**Rényi divergence (Definition 3).** For α > 1,

  D_α(P‖Q) = (1/(α − 1)) log E_{x∼Q}[(P(x)/Q(x))^α].

D₁ is the KL divergence, and D_∞(P‖Q) = log sup_x P(x)/Q(x). ε-DP ⇔ D_∞(f(D)‖f(D′)) ≤ ε for all neighbours.

**Definition 4 ((α, ε)-RDP).** f is (α, ε)-RDP if D_α(f(D)‖f(D′)) ≤ ε for all neighbours D ~ D′. A mechanism has a **budget curve** ε(α).

**Properties (Table I and §III).**
- **Post-processing:** D_α(g(P)‖g(Q)) ≤ D_α(P‖Q) for any randomized g, so g∘f is (α, ε)-RDP.
- **Adaptive sequential composition (Proposition 1):** if f is (α, ε₁)-RDP and g(x, ·) is (α, ε₂)-RDP for every x, then (X, Y) with X ∼ f(D), Y ∼ g(X, D) is (α, ε₁ + ε₂)-RDP. The proof multiplies the inner integrals. Mironov: "the guarantee holds whether the releases of f and g are coordinated or not … It allows us to operate with a well-defined notion of a privacy budget." **Budget curves add, at each α, under adaptive composition.**
- **Group privacy (Proposition 2):** if g is 2^c-stable and α ≥ 2^{c+1}, then f∘g is (α/2^c, 3^c ε)-RDP. Pure DP scales linearly instead (2^c ε).
- **Bayes factor:** E_{f(D)}[log R_post − log R_prior] ≤ D_α(f(D)‖f(D′)). Pure DP bounds |Δ log R| ≤ ε *everywhere*. RDP bounds it in expectation and in the α-th moment: E[(R_post/R_prior)^{α−1}] ≤ e^{(α−1)ε}. Hence P[R_post > β R_prior] < e^ε/β^{1/(α−1)}.
- **"Bad outcomes":** e^{−ε} P[f(D′) ∈ S]^{α/(α−1)} ≤ P[f(D) ∈ S] ≤ (e^ε P[f(D′) ∈ S])^{(α−1)/α}.

**Proposition 3 (RDP → (ε, δ)-DP).** (α, ε)-RDP implies (ε + log(1/δ)/(α − 1), δ)-DP for every 0 < δ < 1.

**Lemma 1.** If D_∞(P‖Q), D_∞(Q‖P) ≤ ε, then D_α(P‖Q) ≤ 2αε² (the constant improves to 0.5 via Bun–Steinke).

**Proposition 4 (advanced composition, from RDP alone).** For n adaptively composed ε-DP mechanisms and any S,

  P[f(D) ∈ S] ≤ exp(2ε√(n log(1/P[f(D′) ∈ S]))) · P[f(D′) ∈ S].

Corollary 1: (4ε√(2n log(1/δ)), δ)-DP when log(1/δ) ≥ ε²n.

**Basic mechanisms (Table II).**
- Gaussian, sensitivity 1, noise N(0, σ²): **(α, α/(2σ²))-RDP**, a straight line. From Proposition 7, D_α(N(0, σ²)‖N(μ, σ²)) = αμ²/(2σ²). Composing n Gaussians with parameter σ gives the curve of one Gaussian with σ/√n.
- Laplace, scale λ: (1/(α − 1)) log[(α/(2α − 1)) e^{(α−1)/λ} + ((α − 1)/(2α − 1)) e^{−α/λ}]. This tends to 1/λ at α = ∞ and ≈ 0.5/λ² at α = 1.
- Randomized response with probability p: (1/(α − 1)) log[p^α(1 − p)^{1−α} + (1 − p)^α p^{1−α}].

**§VII.** RDP "never allows a total breach of privacy with no residual uncertainty", unlike the δ of (ε, δ)-DP. Its guarantee is baseline-dependent: for (10, 0.1)-RDP an event of probability 0.5 can move to [0.419, 0.586], one of probability 10⁻⁶ to [0.195, 4.36]·10⁻⁶. Reporting the curve at 13 fixed α values {1.5, …, 64, ∞} is nearly as tight as optimising α (Figure 3). So a **vector of numbers per mechanism, added component-wise, is an exact and adaptive budget ledger**.

## Evidence with numbers
Figure 2 (randomized response p = 0.51, Laplace λ = 20, up to 250 compositions): the RDP-specific analysis is tighter than every generic bound. Mironov's own generic Proposition 4 is beaten by the optimally tuned (ε, δ) advanced composition. The figures are worked examples, not data.

## What it means for the designs
1. **One currency for continuous and discrete routes.** A continuous route with ℓ₂ sensitivity s to a partner change, plus Gaussian noise σ, costs α s²/(2σ²) at every α. A discrete route costs its own RDP curve: an event fired by randomized response, or a choice by Claude made with a softmax over partner-dependent scores (an exponential-mechanism-style selection). The curves add (Proposition 1), whatever the interleaving and whatever the partner does in between. **This is the single ledger the five designs lacked**: the face, voice prosody, Claude's draft choice and memory writes all write to the same vector.
2. **Copy gain per channel is bounded only as gain/noise** (my derivation from Proposition 7 plus composition). Take a linear route y = g·p + n with n ∼ N(0, σ²) and a partner change of size Δ. It costs αg²Δ²/(2σ²). Under a budget ε at order α, **g ≤ (σ/Δ)√(2ε/α)**. DP does not forbid a gain of 1. It forbids a gain of 1 *at low noise*. A copy buried in noise σ ≫ Δ is still allowed, and its mean is still a copy. So DP limits how *legible* copying can be on any channel, not its average slope. Whether that is enough depends on what an observer averages over (point 3).
3. **Held-level tracking is bounded by the DC gain** (my derivation). Let neighbouring partner streams differ by a sustained offset Δ on one feature over a window of W frames. The output mean then shifts by m_t = Δ (h ∗ 1_W)_t, where h is the impulse response of the whole partner→output map. The Gaussian cost is α‖m‖²/(2σ²) ≈ αΔ²(W|H(0)|² + edge terms)/(2σ²). So:
   - a route with **zero DC gain** (an onset reflex, high-pass) pays only its finite edge energy, however long the hold;
   - any route with **non-zero DC gain** pays in proportion to W: |H(0)| ≤ (σ/Δ)√(2ε/(αW)).

   An integrator that tracks the partner's held level has H(0) ≈ 1, and its cost grows without bound with the hold. **"Reflex can respond, temperament cannot be dictated" becomes "zero DC gain from partner to output, at the given σ and budget".** This is one budget, summed over all routes, because the costs add.
4. **Moments, not worst case, for slow drifts.** RDP's Bayes-factor moment bound (P[R_post > βR_prior] < e^ε/β^{1/(α−1)}) is the natural form for "how likely is it that an observer of the agent's face over an hour becomes much surer of the partner's mood". That is the right reading of "held-level copy" when observers average.
5. **Real cost.** The noise must be real randomness on the partner-sensitive path. If it sits at the output, the agent's face carries jitter of size σ ~ sΔ/√(2ε/α) on every partner-sensitive channel. If it sits at perception, the agent sees the partner noisily. Using Gaussian noise rather than Laplace keeps it smooth and composes as one Gaussian (σ/√n). That makes low-pass-filtered perception noise a principled way to spend the budget.
6. **Sign-blind.** As with every divergence, D_α is invariant under any bijection applied to the output. Copy and anti-copy cost the same.

## Verdict
**adopt (as the ledger: additive budget curves under adaptive composition and post-processing; Gaussian cost αs²/(2σ²); the DC-gain form of the held-level bound).** RDP is the cleanest version of "one guarantee over everything the partner can influence". Its accounting turns per-route caps into a sum.
