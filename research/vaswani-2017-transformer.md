# Vaswani et al. 2017: Attention Is All You Need

Citation: A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin. "Attention Is All You Need." NeurIPS 2017. arXiv:1706.03762 (v7, 2 Aug 2023).

Source read: arXiv v7 via text extraction. Read in full: abstract, sections 1-6 (introduction, background, model architecture, why self-attention, training, results including Table 3 ablations and constituency parsing). Skimmed: section 7 conclusion. Not read: the appendix attention visualisations (figures only).

## The failure or bottleneck it answered
- The stated bottleneck is computational, not representational: recurrence's "inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths". Factorisation tricks and conditional computation had helped, but "The fundamental constraint of sequential computation, however, remains."
- The second bottleneck is path length. In convolutional models "the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet."
- Table 1 states the trade:
  - self-attention: O(n²·d) per layer, O(1) sequential operations, O(1) maximum path length;
  - recurrent: O(n·d²), O(n), O(n).
- Unlike Bahdanau's length curve, this bottleneck was argued from complexity, not from a measured failure curve. The evidence is the outcome:
  - 28.4 BLEU on En-De, "improving over the existing best results, including ensembles, by over 2 BLEU";
  - En-Fr at 2.3·10¹⁹ training FLOPs for the big model, against 1.4·10²⁰ for GNMT+RL (Table 2).

## The new computation, in one equation

  Attention(Q, K, V) = softmax(QKᵀ / √d_k) V, with Q = XW^Q, K = XW^K, V = XW^V, in h parallel heads

The keys, queries and values all come from the same sequence. Each position's new representation is a content-dependent mixture over all positions of its own layer. The graph that relates positions is therefore computed from the data on every pass, instead of being fixed by the architecture (a chain for RNNs, a local stencil for convolutions). Order enters only through added positional encodings. Everything else (FFN, residuals, normalisation) acts on one position at a time.

## New computation or recombination?
Parts, each credited by the paper itself:
1. Dot-product attention: "identical to our algorithm, except for the scaling factor". The paper's [2] (additive attention) is Bahdanau et al.
2. Self-attention ("intra-attention"), already "used successfully in a variety of tasks" [4, 27, 28, 22].
3. End-to-end memory networks.
4. Residual connections [11] and layer normalisation [1].
5. A position-wise two-layer ReLU network, "two convolutions with kernel size 1".
6. Sinusoidal position codes.
7. Label smoothing, dropout, Adam with warm-up.

By the parts test this is a recombination, and the authors present it as one. Their novelty claim is a *subtraction*: "the first transduction model relying entirely on self-attention … without using sequence-aligned RNNs or convolution." The change of what is computed is that the relational structure among elements becomes an output of the layer, not a fixed prior. Two small parts in it do new work, and both bear on the dial problem.
- **Multi-head attention exists to stop a single average from washing things out:** "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this." It was measured in Table 3(A): one head scored 24.9 BLEU against 25.8 for eight, and quality "also drops off with too many heads" (25.4 at 32 heads).
- **The temperature is derived, not tuned.** The 1/√d_k scale follows from a variance argument: with unit-variance components, "their dot product … has mean 0 and variance d_k". A quantity that would otherwise be a free softmax sharpness is fixed by the statistics of the representation.

## What it suggests for an affective core
- **Several parallel routes, each in its own subspace, instead of one gain.** The transformer's answer to "a single average inhibits this" is h independent compatibility functions, each with its own projections W_i^Q, W_i^K, W_i^V. Each head can attend to a different source and a different aspect.
  - Applied to the partner, influence would be a set of routes. One route might carry the partner's timing, another their mouth region against the agent's need, another the agent's own past. Each would be keyed differently, and the combination W^O would be learned.
  - The partner's share is then a pattern across routes that can change with the situation. That is the "profile change" the harness asks about (D75), not a gain change.
  - Whether it is more than a set of gains depends on the heads being forced apart (different inputs or different subspaces). Unconstrained heads can all learn the same copy route.
- **The relation between self and partner can be computed, not wired.** In self-attention, which element affects which is decided per input. An affective core built this way would compute, at each moment, *whether* the partner's current state is relevant to which of its own variables. The coupling would not be a fixed edge with a weight.
- **A dial that cannot be removed can be pinned by an invariance.** The √d_k scale shows a design move the sketches did not try: set the sharpness by a normalisation the representation itself implies, so it is not a free knob. If the harness finds that people show only a gain change (D75), this is how to set the gain without tuning it.
- **Where it collapses.** One head, a shared self-and-partner pool and a learned temperature reproduce the v2 attention-architect sketch and its copy failure. The multi-head point helps only if the heads are structurally distinct.
- **Positional encoding as rotation.** The paper chose sinusoids "since for any fixed offset k, PE_{pos+k} can be represented as a linear function of PE_pos". Relative time is a rotation. This links to phase-based binding (research/lowe-2022-2023-complex-autoencoder-rotating-features.md, research/miyato-2025-akorn.md).

## Verdict
- [Attention is all you need (Vaswani et al.)](vaswani-2017-transformer.md) — 2017 — adopt (as pattern) — a subtraction: the relation graph is computed per input; multi-head attention measured against "averaging inhibits" (24.9 vs 25.8 BLEU); the softmax temperature is pinned by a variance argument, not tuned.
