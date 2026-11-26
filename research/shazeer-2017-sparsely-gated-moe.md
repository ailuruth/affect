# Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer (Shazeer et al.)

Citation: N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, J. Dean. "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer." ICLR 2017. arXiv:1701.06538.

Source read: arXiv PDF, text-extracted. Read in full: sections 1–6 (motivation, the MoE structure, softmax and noisy top-k gating, the shrinking-batch and bandwidth problems, balancing expert utilisation, language-modelling and translation experiments, conclusion) and Appendix A (load-balancing loss, Table 6). Read in part: Appendices C–E (architectures, Table 7, the expert-specialisation Table 9). Not read: Appendices B (hierarchical MoE details), F (strictly balanced gating) and G (attention variant).

## The derivation story
- Conditional computation had been proposed for years (Bengio et al. 2013, 2015; Eigen et al. 2013; Jacobs et al. 1991 for the mixture itself). The obstacles named were engineering ones: GPUs dislike branching, sparse routing shrinks per-expert batches, bandwidth, and "loss terms may be necessary to achieve the desired level of sparsity".
- The layer is y = Σ_i G(x)_i E_i(x) with **noisy top-k gating**: H(x)_i = (xW_g)_i + N(0,1)·softplus((xW_noise)_i), G = softmax(KeepTopK(H, k)). Gradients flow only through the k chosen gates.
- **The central failure is self-reinforcing collapse:** "the gating network tends to converge to a state where it always produces large weights for the same few experts. This imbalance is self-reinforcing, as the favored experts are trained more rapidly and thus are selected even more." The fix is *two hand-weighted soft losses* (importance CV² and a smooth load estimator built from the gate noise, P(x,i) = Φ(((xW_g)_i − kth_excluding)/softplus(…))), plus zero initialisation of W_g and W_noise so training starts balanced.
- Table 6 (MoE-256): with no balancing loss, test perplexity 39.8 and CV(importance) 3.04; with either loss, ~35.6–35.7 and CV 0.03–0.48. Capacity gains: 4096 experts gave 24% lower perplexity than the compute-matched baseline at ~8M ops/timestep; on 100B words, gains up to 65,536 experts, then degradation at 131,072 ("possibly a result of too much sparsity").
- Experts specialise by syntax and meaning (Table 9).

## What it means for the design
1. **Routing collapse is the copy attractor's twin.** In both, a learned selection is reinforced by its own use until one option takes everything. MoE did not remove the instability by structure; it added a balancing *penalty* with a hand-tuned weight. Under D78 that weight is a scalar that decides whether collapse happens — the same kind of quantity the project rules out.
2. **Selection over the agent's own repertoire is not new for this project.** Partner context selecting among the agent's own experts is the partner-regulator design's "dictionary of operators" (design-partner-regulator.md) with sparse top-k gating. MoE adds the engineering (sparse gates, noise for differentiable load) but not a new coupling.
3. **One structural trick worth keeping:** top-k with a fixed k is a hard, innate cardinality limit on how many expressive programs the partner can engage at once, independent of any learned weight. The softmax among the k chosen is still a learned blend.

## Verdict
- [Sparsely-gated mixture-of-experts (Shazeer et al.)](shazeer-2017-sparsely-gated-moe.md) — 2017 — reject as core, watch fixed-k sparsity — routing collapse is self-reinforcing and was fixed by hand-weighted balancing losses (perplexity 39.8 → 35.6), the mirror of a copy attractor tamed by a dial; partner-selected own experts is the partner-regulator design again.
