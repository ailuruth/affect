# Interventional Causal Representation Learning (Ahuja, Mahajan, Wang & Bengio)

Citation: K. Ahuja, D. Mahajan, Y. Wang, Y. Bengio. "Interventional Causal Representation Learning." *Proceedings of ICML 2023*, PMLR 202. arXiv:2209.11924v4.

Source read: the arXiv PDF, text-extracted. Read in full: Sections 1–9 (main text, pp. 1–9). **Not read:** the proofs and supplementary experiments in Appendices A and B (Theorems A.5, A.8, A.12 are cited from their informal statements in the main text only).

## What the paper does
- **Setting.** x = g(z) with an injective decoder g; observational data z ∼ P_Z and interventional data z ∼ P_Z^{(i)} for an intervention on z_i. No assumption on the distribution or graph of z beyond geometry of its support.
- **Key observation.** Interventions leave a geometric signature on the **support** of the latents: a perfect (do) intervention on a child makes the child's support independent of its parents' (Fig. 1); many imperfect interventions do too. Support independence (Wang & Jordan 2021) means the joint support is the Cartesian product of the marginal supports; variables can be dependent yet have independent support.
- **Theorem 4.4 (affine identification).** If g is a finite-degree polynomial with full-column-rank coefficient matrix and the support has non-empty interior, an autoencoder with a polynomial decoder that reconstructs observational plus interventional data recovers ẑ = A z + c with A invertible. The argument: if ẑ were a higher-degree polynomial of z, ẑ² would exceed the decoder's degree.
- **Theorem 5.3 (do interventions).** Under a do intervention z_i = z*, with the support of the unintervened latents having non-empty interior, constraining one encoder component to a constant on the interventional data identifies z_i up to shift and scale: ẑ_k = e z_i + b. The learner need not know which latent was intervened or its value. With one do intervention per latent, all latents are identified up to permutation, shift and scale. Beyond polynomial g, many do interventions per latent give approximate identification (Theorem A.12, informal).
- **Theorem 5.8 (imperfect interventions).** If the intervention makes z_i's support independent of a set S of other latents, a support-independence constraint gives block-affine identification: ẑ_k depends on at most d − |S′| latents and the ẑ_m for m ∈ S′ avoid them.
- **Theorem 6.3 (observational data).** If the latents already have pairwise independent supports (bounded, with ζ-thick boundary), identification up to permutation, shift and scale holds without interventions: an extension of linear ICA to dependent but support-independent latents.
- **Practice.** Two steps: fit a reconstruction autoencoder; then learn a linear (or MLP) map that makes the representation constant on each interventional dataset (Eq. 7) or minimises a Hausdorff-distance measure of support dependence (Eq. 8).
- **Results.** Polynomial decoders (n = 200, d = 6 or 10, degree 2–3): R² ≈ 0.72–1.00 after step 1; with do data MCC rises from ≈ 60–80 to ≈ 95–100. Image data (two balls rendered by PyGame, 64 × 64): MCC rises with the number of do-interventional distributions per latent, e.g. from 34 (one) to ≈ 73 (three or more) for independent uniform latents, and to ≈ 86 for a linear SCM with nine.
- **Placement on Pearl's ladder.** This uses level-two (interventional distribution) data; methods using paired pre/post observations (Lippe et al., Lachapelle et al., Brehmer et al.) use more than level two.

## The mathematical object
**Support geometry under intervention: a do intervention pins one latent and leaves the others' support full, and requiring a learned coordinate to be constant on exactly that data recovers the pinned latent up to shift and scale.**

## What it means for the design
1. **The agent's own held expression is a do intervention.** When the agent holds a channel fixed, that latent is pinned while the rest of the dyad varies. The project's existing "what if your face had stayed neutral" second run is the counterfactual cousin of this: a do on the agent's own face. This paper says such interventions are what make the agent's own channels identifiable without distributional assumptions.
2. **The agent can only intervene on itself.** It cannot do() the partner's face. Partner latents are identified only as non-descendants or descendants of the agent's interventions, not by their own pinning.
3. **Again up to shift and scale.** As in Lachapelle et al., identification is per coordinate up to an affine map, sign included.
4. **Support, not strength.** Support independence is about which values can co-occur, not how strongly one latent drives another. It says nothing about bounding coupling.

## Verdict
- **adopt (as an identification principle for self-caused channels), reject as a core.** It supplies a clean reason why holding still on a channel teaches the agent what that channel does, and why a counterfactual neutral run is a well-posed object. It is a representation-identification result, not a dyadic mechanism.
