# Geo-indistinguishability: differential privacy for location-based systems (Andrés, Bordenabe, Chatzikokolakis & Palamidessi)

Miguel E. Andrés, Nicolás E. Bordenabe, Konstantinos Chatzikokolakis & Catuscia Palamidessi, *Proc. ACM CCS 2013*, pp. 901–914, doi:10.1145/2508859.2516735; arXiv:1212.1984v3 (20 Feb 2014), 15 pp.

This note stands in for **Chatzikokolakis, Andrés, Bordenabe & Palamidessi 2013, "Broadening the scope of differential privacy using metrics" (PETS)**, which defines d-privacy for general metrics. That paper was not reachable (HAL was blocked from this session). It is cited only through this paper's restatement: Theorems 3.1–3.2 here are its general-metric characterisations instantiated to the Euclidean metric.

## What was read
arXiv v3:
- **Read in full:** §1–4 (existing notions; Definition 3.1; Theorems 3.1–3.2; protecting location sets with d∞; aggregates; the planar Laplace mechanism; discretisation, Theorem 4.1; truncation, Theorem 4.2).
- **Skimmed:** §5 (LBS case study, bandwidth), §6 (comparison with optimal Bayesian mechanisms), §7–8.

Proofs are in a separate report and were not read.

## The computation, precisely

**Multiplicative distance.** d_P(σ₁, σ₂) = sup_S |ln(σ₁(S)/σ₂(S))|.

**Definition 3.1 (ε-geo-indistinguishability, d-privacy with Euclidean d).** For all x, x′,

  d_P(K(x), K(x′)) ≤ ε d(x, x′),  i.e.  K(x)(Z) ≤ e^{ε d(x,x′)} K(x′)(Z).

Standard DP is the case d = Hamming distance on databases. Points within radius r get "εr-privacy": nearby secrets are hard to tell apart, far ones are allowed to be told apart. ε has units of inverse distance.

**Theorem 3.1 (hiding).** K is ε-geo-indistinguishable iff, for every hiding function φ, every prior π and every Z, d_P(Bayes(π, K, Z), Bayes(π, K∘φ, Z)) ≤ 2ε sup_x d(x, φ(x)).

**Theorem 3.2 (informed attacker).** Equivalently, for every set N, every prior and every Z, d_P(π|_N, σ|_N) ≤ ε d(N), where d(N) is the diameter of N. An attacker who already knows the secret to within N learns at most ε·diam(N) more.

**Abstracting from the prior.** "the user's value is not protected under any prior information" (the Terry Gross example). DP and d-privacy bound what the *observation adds*, not what can be inferred from correlated side information.

**Traces.** For tuples x = (x₁..x_n), use d∞(x, x′) = max_i d(x_i, x′_i). Applying an ε-mechanism independently to each point gives only **nε**-geo-indistinguishability, because the points may be correlated (in the extreme, x₁ = x₂). Better results need noise designed on the whole tuple.

**Aggregates.** If f is Δ-sensitive w.r.t. (d∞, d), i.e. d(f(x), f(x′)) ≤ Δ d∞(x, x′), then K∘f is εΔ-geo-indistinguishable. For a centroid this needs far less noise than Hamming DP.

**Mechanism.** The planar Laplacian has density D_ε(x₀)(x) = (ε²/2π) e^{−ε d(x₀, x)}. In polar coordinates the radius is Gamma(2, 1/ε) and the angle is uniform. Sample r = C_ε^{−1}(p) = −(1/ε)(W_{−1}((p − 1)/e) + 1), with C_ε(r) = 1 − (1 + εr)e^{−εr}.

**Discretisation can break the guarantee.** Theorem 4.1: remapping to a grid of unit u preserves ε-geo-indistinguishability within r_max only if a tighter ε′ is used, with ε′ + (1/u) ln((q + 2e^{εu})/(q − 2e^{εu})) ≤ ε and q = u/(r_max δ_θ). Beyond r_max it fails for any finite ε. Truncation to a fixed admissible set A restores the full guarantee (Theorem 4.2).

## Evidence with numbers
Figure 5: with double precision the extra noise needed for discretisation is negligible at r_max = 100 km. §6 reports that, among prior-independent mechanisms, planar Laplace gives the best privacy for equal quality loss. This was not checked in detail.

## What it means for the designs
1. **A metric lets the budget distinguish *what kind* of partner difference is protected.** Choose a metric on partner streams that is anisotropic:

   d(p, p′) = κ_e·(difference in onset events) + κ_L·(difference in held level over windows) + …,

   with κ_L ≫ κ_e. Then d-privacy says the agent may become e^{εκ_e}-sure about a single onset, so the fast reflex can respond, but only e^{εκ_L·ΔL}-sure about a held-level difference ΔL. This is the "directional" extension the brief asked for. It is the formal version of "reflex can respond, temperament cannot be dictated", stated on *inputs* rather than on routes. (My construction. The paper uses one isotropic metric.)
2. **It still does not see copy versus anti-copy.** The metric sits on the *partner's* side. The guarantee is a divergence between output distributions, so it is invariant to any bijection of the output. An agent that knows a partner onset happened can mirror it or counter it at the same cost. What the metric buys is *resolution*: the agent cannot resolve small held-level differences, so it cannot track a level finely. It can still respond to large, categorical differences, like a markedly sad partner versus a neutral one.
3. **Traces degrade linearly under independent per-frame noise (nε).** That is precisely why per-frame noise on a held-level route fails over hours. A level held for n frames, read with fresh noise each frame, is averaged back out. Noise must be designed on the whole trace, for example by high-passing the partner signal *before* the noise, so that a sustained offset produces a bounded, not growing, output difference. This is the same conclusion as the DC-gain bound in mironov-2017, reached from the trace side.
4. **Sensitivity in the metric gives per-channel ceilings.** For a map f from partner to agent channel i with d-sensitivity Δ_i (the incremental gain), adding planar or Gaussian noise gives an εΔ_i guarantee. So the REN's incremental ceilings c_i (whole-loop-bounds-synthesis) are exactly the Δ_i of a d-private composition. **A Lipschitz certificate plus calibrated noise is a d-privacy certificate.** The REN supplies the sensitivity and the noise supplies the indistinguishability.
5. **Discretisation warning.** Theorem 4.1 is a real hazard for an implementation. Quantising expression channels, or event thresholds, after noise can break the guarantee unless done as in Theorem 4.2 (truncate to a fixed admissible set, tighten ε′). Any code path that rounds partner-sensitive values must be inside the proof.
6. **Correlated side information is not covered** (the Terry Gross point). If the partner's words also carry their mood, d-privacy on the face is silent about mood leaking through words.

## Verdict
**adopt (d-privacy with an anisotropic metric on partner streams as the way to give the reflex a large budget and held levels a tiny one; noise must be designed on traces, not frames; Lipschitz sensitivity plus noise is a d-privacy certificate).** It does not, and cannot, distinguish copy from anti-copy.
