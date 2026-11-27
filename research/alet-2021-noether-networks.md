# Noether Networks: meta-learning useful conserved quantities (Alet, Doblar, Zhou, Tenenbaum, Kawaguchi & Finn)

Citation: F. Alet, D. Doblar, A. Zhou, J. Tenenbaum, K. Kawaguchi, C. Finn, "Noether Networks: Meta-Learning Useful Conserved Quantities", NeurIPS 2021. arXiv:2112.03321v1.

Source read: arXiv PDF, text-extracted. Read in full: abstract, §§1–6 (theory, method, experiments, related work, discussion) and Appendices B and C (why trivial conserved quantities are avoided; scientific-data details). Appendix A (the proof of Theorem 1) and the video-experiment appendices were skimmed.

## What the paper does
- **Idea.** Symmetries are hard to discover "because they are global properties linked to counterfactuals about unobserved perturbations of the data", whereas "conserved quantities can be directly observed in the true data". So learn a conserved quantity g_φ instead of a symmetry.
- **Mechanism (tailoring).** A predictor f_θ rolls out x̃_{1:T}; one inner gradient step on L_Noether = Σ_t |g_φ(x₀) − g_φ(x̃_t)|² adapts θ for this query (eqs. 2–3); the outer loss trains φ and θ through the inner step (second-order, MAML-like). The conservation loss is optimised at prediction time, so it holds on test queries too.
- **Theorem 1.** For models f_θ(x) = x + v_θ whose preimages under g_φ are m-dimensional affine subspaces, enforcing g(f(x)) = g(x) replaces d by m in the generalisation bound. m = 0 (g invertible) forces f(x) = x; m = d (g constant) gives nothing.
- **Trivial quantities (App. B).** A constant g gives no improvement of the post-update task loss, so meta-learning pushes g to be useful, not merely conserved.
- **Evidence.** Program search over 41,460 (pendulum) and 72,372 (spring) candidate formulas recovers p² − 2.99 cos q (true 3.00) and q² + 1.002 p² (true 1.000); on a real, dissipative pendulum it finds p² − 2.39 cos q and beats the MLP by more than an order of magnitude and Hamiltonian NNs (Fig. 2). On real video (311 training sequences) gains over SVG are "modest" (Fig. 4).

## What it means for the design
1. **Approximate conservation, learned, as a source of slow variables.** A quantity the agent's own dynamics should approximately conserve is directly observable in its own history, unlike a symmetry. This is a learning route to "temperament as a conserved quantity of one's own dynamics" without naming it.
2. **The m-dimensional preimage is the trade-off.** Conserving more (smaller m) constrains more and generalises better, but m = 0 freezes the state. A design using conserved charges must say which are exactly conserved, which only approximately, and by which inputs they may change (Noether's sourced form).
3. **Not an architecture.** The conservation is a loss inside the prediction function, not a structural property; by the brief's standard (properties for every parameter value) it would be a training objective, like contrastive individuation in new-core-search-2-synthesis.md.

## License
Paper: NeurIPS (author copyright). Code stated to be public at the authors' lab site (licence not checked).

## Runs on this Mac without a GPU?
The scientific-data experiments are small MLPs; the video experiments use SVG with second-order gradients and would be slow on CPU. Not run.

## Verdict: watch (method for learning own-dynamics invariants)
Useful as the learned counterpart of the structural Casimir invariants in new-core-search-3-synthesis.md, Direction 1; not a core mechanism.
