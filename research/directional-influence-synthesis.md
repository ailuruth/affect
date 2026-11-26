# Bounding the copy direction, not the amount: a one-sided concordance ceiling (synthesis)

Question (designs.md open gap 1; whole-loop-bounds-synthesis): a capacity bound on partner→face influence is sign-blind, because mutual information is unchanged when the agent copies and when it does the opposite. What object bounds influence **and** makes the copy direction impossible, per expression, while leaving strong contingent and sign-flipped responses free?

**Sources read in full:**
- williams-beer-2010-partial-information-decomposition;
- bertschinger-2014-unique-information;
- mediano-2021-integrated-information-decomposition (ΦID);
- janzing-2013-quantifying-causal-influences;
- puccetti-wang-2015-extremal-dependence (open stand-in for Nelsen ch. 2).

**Not reachable:** Ay & Polani 2008 (santafe.edu blocked, mirrors timed out); it is cited only through Janzing et al. Rosas et al. 2020 ("Reconciling emergences") and Nelsen's book were not read. Nothing below relies on them.

**Own checks:** D1–D5 in `foundations/sims/directional-influence/checks.py` (`python3 -I checks.py`, numpy and scipy, under a minute; output in `checks.out`). Statements marked **[own]** are mine.

## 1. Why every information measure fails, and what does not

**The invariance argument [own].** Every quantity in the four information sources is built from KL divergences, so it is invariant under any bijection of each variable's alphabet (the group Sym):
- mutual information, transfer entropy;
- Williams–Beer and BROJA PID atoms;
- ΦID atoms, including its mode literally named "Copy";
- Janzing's causal strength.

Copying (a = p) and anti-copying (a = ¬p or a = −p) differ by such a bijection, so these measures cannot tell them apart:
- D1: both give TE = 1 bit, all of it partner-unique, with Spearman ρ = +1 versus −1;
- Bertschinger Fig. 2 shows both as corners of the same coupling square with equal values;
- Janzing's Gaussian strength depends on α² only.

**What can see the direction** is an object invariant only under *increasing* bijections (the group Inc): the copula and its concordance functionals (Spearman, Kendall, the pointwise copula order). On channel k at lag τ, **copying, up to any amplitude rescaling, is exactly the comonotone copula M, the top vertex of the coupling set. Its opposite is W, the bottom vertex.** Both maximise information (puccetti-wang-2015). Because these objects are Inc-invariant, the agent cannot escape a concordance bound by changing its own gain. They break under order reversal, which is the sign character of symmetry-no-copy-synthesis.

**"How much" and "which way" are therefore different mathematical objects.** The amount is information, which is Sym-invariant. The direction is concordance, which is Inc-invariant. A design must bound them separately.

## 2. What the human non-copying signatures are, in these terms

| Signature (non-copying-dynamics-synthesis) | Object | Measure that sees it |
|---|---|---|
| C1, C2: below-surrogate similarity at some lags and bands | copula at that lag lies below the surrogate's (negative concordance) | Spearman, copula, real part of the cross-spectrum; **not** PID or ΦID (D1: a noisy anti-copy is pure "unique") |
| C7: avoid repeating the pair's joint pattern; novelty grows | the agent's response depends on partner and own history jointly | PID synergy (D1: XOR rule gives syn = 1, ρ ≈ 0); ΦID Un→Syn, Syn→Syn, Syn→Un_a |
| C3: shared referent, different form | unique information about the referent, low concordance of form | both |

So the answer to "is the human finding a synergy-dominant regime?" is **only half yes.** Anti-repetition (C7) is synergy. Below-chance similarity (C1, C2) is a sign property that synergy measures cannot see. A human-like agent needs both a **sign ceiling** and a **synergy-generating drive**. They are separate mechanisms.

## 3. The candidate constraint

**Object [own].** Let G be the end-to-end causal map from the partner's percept u to the agent's face y, through all routes: perception, core, memory and appraisal. Choose a one-sided ceiling κ_k ∈ (0, 1) per expression channel k, innate and not learnable. Require, for every pair of partner inputs that differ only in channel k:

  ∫ (Δy_k)(Δu_k) dt ≤ κ_k ∫ (Δu_k)² dt,   and separately ‖ΔG‖ ≤ L (the existing Lipschitz/REN ceiling), with κ_k < 1 ≤ L allowed.

In words, the incremental in-phase gain from partner channel k to own channel k is at most κ_k, while the magnitude may reach L in any other direction. For an LTI linearisation this is, by Parseval, **Re H_kk(jω) ≤ κ_k for all ω**: the co-spectrum (real part) is capped, and the quadrature and anti-phase parts are free up to L. In distribution terms, the companion is a copula ceiling C_{k,τ} ≤ κM + (1 − κ)Π at every lag τ. That is linear in C, so it cuts the coupling polytope of Bertschinger et al. in a half-space that removes the M vertex and keeps W.

**What it gives, for every partner signal and every parameter value, if it holds by construction:**
- **No copy at gain above κ_k, at any lag.** Copy at scale c and delay τ is H = c·e^{−jωτ}, whose maximum real part is c. So copying is not reachable, and hence not attracting, above κ_k. The amplitude-invariant form (copula ceiling) also blocks a copy that the agent re-scales.
- **Sign flips stay strong but must be shaped.** −e^{−jωτ} has real part +1 at ω = π/τ: a fast, delayed sign flip *is* a copy in that band. D5: a fast sign flip with a 0.5 s delay reaches Re H = 0.993; low-passed (a = 2 or 0.5 s⁻¹) it reaches 0.468 or 0.171, with DC gain −1 throughout. **Prediction:** strong opposite-sign responses must be either short-lag or slow (phasic or low-passed relative to their lag). This matches C2: divergence at lag 1 that relaxes by lag 3, and "a stable negative correlation fails".
- **Mimicry stays, at the agent's own small gain.** Same-sign positive drive up to κ_k is allowed (Principle 3's fast match). This is the one-sided version of the cap that symmetry-no-copy statement 4 said was unavoidable on matching components. Unlike that cap, it does not limit opposite-sign or cross-channel strength.
- **Information is untouched.** Synergistic, contingent and cross-channel responses carry any number of bits (D4: 6-bit deterministic couplings with negative or near-zero concordance).

**How it differs from what the designs already have.** The REN or Lipschitz ceiling and the directed-information bound are symmetric: they cap |gain| or bits, so they cap sign flips as hard as copies. Twisted equivariance forbids copy only on twisted components and needs a group choice. This constraint is a **sector** [−L, κ_k] on the diagonal of the incremental gain, asymmetric in sign. It sits between the two: it is weaker than the symmetry rule on twisted channels and stronger than a cap on matching channels.

## 4. Open problems

1. **Closure.** One-sided bounds are closed under sums only additively (κ + κ′), and not under products. Dall'Aglio: two countermonotone stages compose to comonotone (D3: −0.98 and −0.99 per stage give +0.98). So the ceiling must be **certified on G end to end**, not per module. RENs enforce a full-vector (Q, S, R) incremental IQC by construction. The vector form κ‖Δu‖² − ⟨Δu, Δy⟩ ≥ 0 is supported, but it caps only the sum over channels. The **per-channel diagonal** version (others held fixed, cross-channel left free) is not a standard IQC. Requiring it for all joint perturbations forces cross-channel gains to zero [own: Δu = (1, t) gives a + bt ≤ κ for all t only if b = 0]. A parametrisation that satisfies a diagonal one-sided sector by construction, while cross-channel terms stay free, is the key missing piece. Without one, the property can only be checked after training (KYP/LipSDP-style), which is not learning-proof.
2. **Pointwise versus scalar.** The pointwise copula ceiling catches local copies: random-strip shuffles violate it by 0.016–0.064 at ρ_S ≈ 0 (D4). That may be too strict. The scalar ρ_S ≤ κ is too weak: it allows half-range copying. The right intermediate (for example a ceiling on the copula's positive-quadrant-dependence mass, or on local Kendall τ) is unchosen.
3. **Map versus distribution.** The copula is a property of the joint law under the current partner. The map-level sector is the version that holds for every partner. The exact relation between Re H_kk ≤ κ and the lagged copula ceiling is not derived; for Gaussian inputs, one does not imply the other lag by lag.
4. **Channel identity.** "Same channel" needs the partner→own correspondence P (self-other-control-synthesis). If P is learned, the ceiling applies only to the learned correspondence, and a crossed P (Cook 2014) moves the copy direction. The ceiling must be stated on the innate anatomical correspondence, with a separate argument for learned remappings.
5. **The synergy half is unbuilt.** Nothing here generates C7. The candidate is a satiable drive on the ΦID shift from Red→Red toward Syn→Syn and Syn→Un_a over the pair's recent history, evaluated offline first (MMI-ΦID on Gaussianised features). Raw TE must not be a drive: it contains the Un_p→Red copy mode (mediano-2021).
6. **Audit.** Measure each route's contribution to the copy direction with Janzing's wire-cut surrogate: the drop in ρ_S(partner_k, agent_k) when that route is fed an independent sample of its own input marginal. Per-route values need not add up (Janzing Theorem 5: repetition code, XOR), so always also cut the whole set.
