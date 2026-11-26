# Layer Normalization (Ba, Kiros & Hinton)

Citation: J. L. Ba, J. R. Kiros, G. E. Hinton. "Layer Normalization." arXiv:1607.06450 (2016).

Source read: arXiv PDF, text-extracted (the PDF had a broken cross-reference table; text recovered). Read in full: abstract, sections 1–5 (motivation, batch normalisation recap, layer normalisation, layer-normalised RNNs, related work, invariance analysis with Table 1's content in the text, the Fisher-geometry analysis of normalised GLMs) and section 6's experiments (order-embeddings, attentive reader, skip-thoughts, handwriting, DRAW). Not read: the appendices (GRU/LSTM equations, gain derivations) and the conclusion paragraph on convolutional networks (truncated in extraction).

## The derivation story
- The bottleneck: batch normalisation needs batch statistics, which are impossible online (batch size 1) and awkward in RNNs, where "the summed inputs to the recurrent neurons … often vary with the length of the sequence".
- The move is a **transposition**: compute μ and σ over the H hidden units of one layer on one case, instead of over the batch for one unit. All units share the same μ, σ; each keeps its own gain g_i and bias b_i: h = f((g/σ) ⊙ (a − μ) + b).
- The justification is an invariance argument, not a tuning result: layer norm is invariant to rescaling and re-centring the *whole* weight matrix (W′ = δW + 1γᵀ) and to rescaling *each individual input case*; it is not invariant to rescaling a single unit's weights. In RNNs "the normalization terms make it invariant to re-scaling all of the summed inputs to a layer, which results in much more stable hidden-to-hidden dynamics."
- The Fisher-metric analysis: in a normalised GLM, doubling a weight vector's norm halves the curvature along it, an "implicit learning rate reduction" and "early stopping" on weight norms; learning the gain depends on prediction error, not input scale.
- Results: on order-embeddings, convergence in 60% of the time; on the attentive reader, faster and better than recurrent batch norm and insensitive to the 0.1 vs 1.0 initial-gain choice that recurrent BN needed.

## What it means for the design
1. **A shared pool statistic erases a global magnitude.** If the partner's mapped channels enter a layer that is normalised over a pool containing both the agent's own drives and the partner's, then scaling the partner's whole face up or down has no effect on the normalised pattern — the "partner intensity" dial is removed by invariance, the way LN removes the scale of the summed inputs.
2. **But a per-unit gain re-introduces a per-channel scalar.** LN's g_i is exactly a learned per-expression gain. Under D78 that is allowed only if it is innately capped and cannot reach copy; LN puts no bound on g.
3. **The derivation pattern** (keep the computation, change the set it pools over, prove the new invariance) is the same as attention's and ResNet's: a subtraction or transposition justified by an invariance.

## Verdict
- [Layer normalization (Ba, Kiros & Hinton)](ba-kiros-hinton-2016-layer-normalization.md) — 2016 — watch — pooling μ, σ across a layer instead of a batch makes the layer invariant to the scale of all its summed inputs and to each case's scale, so a self+partner pool removes the global partner-intensity dial; the per-unit gain g is an uncapped per-channel scalar.
