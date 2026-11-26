# The price of differential privacy under continual observation (Jain, Raskhodnikova, Sivakumar & Smith)

Palak Jain, Sofya Raskhodnikova, Satchit Sivakumar & Adam Smith, "The Price of Differential Privacy under Continual Observation", arXiv:2112.00828v4 (11 Jan 2022), 28 pp.; published at ICML 2023.

This note stands in for **Dwork, Naor, Pitassi & Rothblum 2010, "Differential privacy under continual observation" (STOC)**, which is not on arXiv. Its author hosts were not reachable from this session, so DNPR 2010 was not read. It is cited only as Jain et al. restate it: the continual-release model, the binary tree mechanism with error O(log² T), the Ω(log T) lower bound, and the event-level versus user-level distinction.

## What was read
arXiv v4, extracted text.
- **Read in full:** §1 (introduction, contributions, related work including the event-level and user-level paragraphs), §2 (Definitions 2.1–2.18: DP, group privacy Lemma 2.3, post-processing Lemma 2.4, the Laplace, Gaussian and exponential mechanisms, Rényi divergence, ρ-zCDP and its composition and conversion, the nonadaptive continual-release model), §3 (MaxSum lower bound: Theorem 3.1, Lemmas 3.3–3.4, Algorithm 1), §5.1–5.3 (adaptive continual release: Algorithm 3, Definitions 5.1–5.3, Theorems 5.4–5.8, the binary tree mechanism Algorithm 4, Lemma 5.10's simulation argument), and the start of §5.4 (recompute at intervals: Algorithm 7, Claim 5.12).
- **Skimmed:** §4 (SumSelect lower bound) and the rest of §5.4.
- **Not read:** Appendix A.

## The computation, precisely

**Continual release.** A mechanism receives x₁, …, x_T one at a time and outputs a_t after each. It is DP if the batch algorithm that outputs the **whole vector** (a₁, …, a_T) is DP (Definition 2.17). "The main challenge for privacy is that each individual record contributes to outputs at multiple time steps."

**Event-level versus user-level.** "For continual release mechanisms, we study event-level privacy, where each user's data appears in a single record, as opposed to user-level privacy, where a user's data could be distributed over multiple records." User-level is the more stringent. Event-level does not imply user-level. Group privacy (Lemma 2.3) is the only bridge: (ε, δ)-DP gives (ℓε, δ(e^{ℓε} − 1)/(e^ε − 1)) for records differing in ℓ places.

**Adaptive continual release (§5.1, Algorithm 3).** An adversary Adv produces x_{t+1} **after seeing a₁..a_t**. At one challenge step t* it supplies two records, and a hidden bit decides which one the mechanism receives. Privacy (Definition 5.3) requires Adv's whole view, its coins and transcript, to be (ε, δ)-indistinguishable (or ρ-close for zCDP) across the two versions. "The adversary Adv combines the data generation process and the attack itself in one entity, so that our model allows for an arbitrary relationship between them."

**ρ-zCDP (Definitions 2.11–2.12).** D_ξ(A(y)‖A(y′)) ≤ ξρ for all ξ > 1. Composition adds ρ (Lemma 2.13). The Gaussian mechanism with ℓ₂-sensitivity Δ₂ and noise σ is Δ₂²/(2σ²)-zCDP (Lemma 2.14). ρ-zCDP ⇒ (ρ + 2√(ρ log(1/δ)), δ)-DP (Lemma 2.15).

**Binary tree mechanism (Algorithm 4, after DNPR10 and Chan et al. 2010).**
- Build a complete binary tree over T leaves. Each node stores a noisy partial sum of its interval, with Gaussian noise σ = √(d(log₂ T + 1)/(2ρ)) on d coordinates.
- Each record lies in log₂ T + 1 nodes, so by composition the mechanism is ρ-zCDP.
- The running sum at t uses at most log t + 1 nodes, one per level of the dyadic decomposition. So the error is polylog(T), not √T.
- Lemma 5.10 proves privacy in the *adaptive* model by simulation. Only the log T + 1 nodes whose interval contains t* depend on the challenge, so the whole view reduces to one Gaussian mechanism.

**Recompute at intervals (Algorithm 7).** Release f(x_{[t]}) + noise every r steps and hold it in between. Fewer releases cost less budget, but the held answer goes stale. This is user-level private whenever the recomputation is.

**Lower bounds (Theorem 3.1).** MaxSum_d is the maximum over d attributes of the running sum. Any (ε, δ)-DP continual-release mechanism with δ = o(ε/T) has error α = Ω̃(min{T^{1/3}/ε^{2/3}, √d/ε, T}). The batch model needs only O(1/ε). Pure DP: Ω̃(min{√(T/ε), d/ε, T}). **Tracking the largest of several running sums is polynomially harder than tracking one sum.** The reduction (Algorithm 1) streams the dataset and then forces each attribute to be the maximum in turn. It is private by post-processing.

## Evidence with numbers
Table 1 (upper and lower bounds match up to polylog T). Continual-release error exceeds batch error by Ω̃(T^{1/3}) for MaxSum under approximate DP, against the previously known polylog gap for plain summation (O(log² T) achievable, Ω(log T) necessary, per DNPR10).

## What it means for the designs
1. **A face streamed for hours is a continual-release problem with an adaptive adversary.** The partner chooses the next frame after seeing the agent's face. This is exactly Algorithm 3, so a guarantee in this model is a guarantee about the closed loop. The proof style (Lemma 5.10) also transfers: privacy follows because only the nodes that touch the challenge depend on it.
2. **Event-level maps onto "reflex can respond".** With event-level ε, a single partner expression event (an onset, a burst) can move the agent's output by a bounded likelihood ratio e^ε. A reflex needs ε_event of order 1 so that one smile onset is detectable.
3. **"Temperament cannot be dictated" is not user-level privacy.** User-level privacy over an hour would make the whole hour of partner behaviour nearly invisible to the agent. That forbids relationship learning and contingent care as well as copying. Conversely, event-level privacy says nothing about sustained patterns: by group privacy, T events cost Tε (√T with advanced composition), which is vacuous over an hour. **Neither standard granularity is the right one.** The right neighbouring relation is "differ by a sustained offset in held level over a window", with its own budget. The fast route can then spend generously on events while the slow route spends almost nothing on levels (see mironov-2017, point 3, and the synthesis).
4. **The binary tree is a design for a slow state.** Suppose the agent must hold *some* partner-dependent slow quantity (a relationship estimate, a running count of shared positive moments). The tree mechanism releases it continuously at polylog(T) error for log T + 1 noisy writes per record. So **memory should be written as dyadic noisy partial sums, not as an exponentially smoothed raw estimate**. Each partner record then touches log T writes, all priced. This is the principled form of "persistent state written only by gated, budgeted events" that the fibred design tried to build from tokens.
5. **Recompute-and-hold is the budget-efficient slow channel.** A held value refreshed every r steps costs T/r releases. That is the same trade as the fibred design's slow base, but here the cost of each refresh is priced and the staleness is explicit.
6. **The MaxSum lower bound warns against "track the dominant partner feature".** A slow state that follows *whichever* partner expression is currently strongest is a MaxSum or SumSelect problem. Under continual observation it costs T^{1/3} more error than tracking a fixed feature. A design that lets the partner's dominant channel steer a shared slow variable is buying the most expensive query in the family.

## Verdict
**adopt (the adaptive continual-release model as the right formal setting for a dyad over hours; the binary tree as a priced write discipline for persistent state; event-level and user-level are both wrong for temperament, and a level-offset neighbouring relation is needed).** The primary source, DNPR 2010, was not read.
