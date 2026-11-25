# Löwe, Lippe, Rudolph & Welling 2022, and Löwe et al. 2023: Complex-Valued Autoencoders and Rotating Features for Object Discovery

## Citations

- S. Löwe, P. Lippe, M. Rudolph, M. Welling. "Complex-Valued Autoencoders for Object Discovery." *Transactions on Machine Learning Research*, 11/2022. arXiv 2204.02075 (v5). Code: github.com/loeweX/ComplexAutoEncoder.
- S. Löwe, P. Lippe, F. Locatello, M. Welling. "Rotating Features for Object Discovery." *NeurIPS* 2023. arXiv 2306.00600 (v2). Code: github.com/loeweX/RotatingFeatures.

## Source read

Both arXiv PDFs, via text extraction.

**Complex AutoEncoder (CAE).**
- Read in full: abstract, sections 1-6 (the temporal correlation hypothesis, method, experiments, related work, conclusion and limitations), and Tables 1-2.
- Read in the appendix: only the layer equation restated in Eq. 11.
- Not read: the rotation-equivariance proof (D.1) and the re-implementation details of the deep Boltzmann machine (DBM) and SlotAttention baselines (C.2, C.3).

**Rotating Features (RF).**
- Read in full: sections 1-6 and Table 1.
- Read in the appendix: only the limitation sentence in D.2.
- Not read: the hypersphere-capacity analysis (D.1) and the multi-dSprites and CLEVR results (D.6).

## The failure or bottleneck it answered

The bottleneck is the binding problem: how a network with fixed weights keeps track of which features belong together. CAE argues against slot methods. Slots need "involved architectures with iterative procedures, elaborate structural biases, and intricate training schemes". They limit "the information flow and expressiveness of the model", and they "cannot inherently represent part-whole hierarchies".

The prior complex-valued method, Reichert & Serre 2014, had three problems:
- It trains a real-valued DBM and adds phases only at test time.
- It is "slow to evaluate as it requires 100s-1000s of iterations to settle".
- Its phases "may not be representative of object identity".

Measured results, ARI-BG (object-only adjusted Rand index), 8 seeds:

| Dataset | CAE | DBM | SlotAttention |
|---|---|---|---|
| 3Shapes | 1.000 | 0.419 ± 0.023 | — |
| MNIST&Shape | 0.971 ± 0.011 | 0.175 ± 0.006 | close to chance (stated in the text) |

CAE trains "between 10.0 and 99.8 times faster" than SlotAttention.

CAE then fails at four objects (ARI-BG 0.669 ± 0.029). RF answers this with the claim that a one-dimensional phase "is severely limited in the number of object representations it can separate". It also says the evaluation method is "only applicable to single-channel inputs".

RF's results:
- With rotation dimension n ≥ 6 it separates all four shapes.
- It reaches ARI-BG 0.959 ± 0.022 on ten shapes.
- On Pascal VOC, using DINO features, it reaches MBO_c 0.460 ± 0.001. That sits between DINOSAUR-MLP (0.409) and DINOSAUR-Transformer (0.512).

## The new computation, in one equation

For a layer with input z ∈ R^{n×d_in} (n = 2 is the complex case):

    ψ = f_w(z) + b,   χ = f_w(‖z‖),   z_out = ReLU(BN(½‖ψ‖ + ½χ)) · ψ/‖ψ‖

The same weights act on two things:
- the oriented vectors, giving ψ, whose norm shrinks when the inputs point in different directions (destructive interference);
- the input magnitudes alone, giving χ, which ignores orientation.

Averaging the two magnitudes turns subtraction into masking. CAE states that with this term "the net contribution of z2 to the output is zero" for a maximally out-of-phase input. The output orientation comes from ψ alone, with a learned orientation bias per feature.

So each unit carries two separate messages:
- **magnitude**: "how much of this feature";
- **orientation**: "which group it belongs to".

A unit's effective connectivity depends on whether the orientations of its inputs agree. That agreement is computed on every forward pass and is not stored in the weights.

## New computation or recombination?

Recombination, of an old and distinct idea. The parts:
1. **Magnitude as rate code and phase as synchrony.** This is the temporal correlation hypothesis (von der Malsburg; Singer & Gray 1995). The abstraction to complex numbers is taken "Following Reichert & Serre (2014)".
2. **The χ gate that masks out-of-phase inputs.** Its masking effect is credited directly to Reichert & Serre: "As shown by Reichert & Serre (2014), this implementation effectively masks out inputs that have an opposite phase compared to the overall output."
3. **Phase biases b_ϕ.** These are new in CAE. Without them the model "achieves no meaningful phase separation between objects" (ARI-BG 0.100 ± 0.035 on 2Shapes; removing χ gives 0.074 ± 0.068).
4. **A ReLU on the magnitude with the phase kept.** This is new in CAE.
5. **End-to-end MSE training on magnitudes only.** This is what makes the method one forward pass instead of settling dynamics.
6. **k-means or agglomerative clustering on the orientations**, used only for evaluation.
7. **RF's extension to n dimensions**, with a bias per rotation dimension. This gives up the global rotation equivariance that CAE has.
8. **RF's weighted average of orientations across channels**, again only for evaluation.

Earlier supervised and weakly supervised phase-binding networks: Mozer et al. 1992, Zemel et al. 1995, Rao et al. 2008-2011.

By the project's test, these two papers change the training and the dimensionality, not what is computed. The underlying computation is different in kind from attention: a second channel carried on every activation, orthogonal to strength, that gates summation by agreement. But that computation dates from 1981-2014. It also sits next to the excluded oscillator family, as synchrony without time. CAE has no dynamics: phase is a static coordinate, and "the point in time at which a stimulus is perceived (here: input phase) should influence when the stimulus is processed (here: output phase), but it should not influence how it is processed".

## What it suggests for an affective core

The idea worth taking is the separation it enforces: **"whose state is this" is carried by orientation, "how strong" by magnitude, and whether two signals combine is decided by their angle, per feature.**

1. **Partner influence as per-feature alignment, not a gain.** Suppose the agent's own body features and the features read from the partner both carry an orientation, initialised apart (self and other). A downstream unit sums only the inputs aligned with its own output. Then the partner's share in any one unit is set by cos(θ_partner, θ_unit) for that feature, and it varies across features and situations. Contagion becomes a measurable event (orientations coming into line) that can happen for some features and not others. A single gain cannot do that. The analogue of the RF uncertainty maps, the distance to the nearest cluster centre, would give a graded per-feature measure of "half-bound to the partner".
2. **Relational, not absolute.** CAE's global rotation equivariance means only phase differences carry meaning. That suits self against other, which is a relation rather than a label. RF drops equivariance for performance. A self-other code should probably keep it, so the agent cannot learn a fixed "partner direction".
3. **Two groups is the regime that works.** RF can extract only "up to two objects at a time" in its bottleneck. CAE handles two or three. A self/other split needs exactly two groups, inside the demonstrated capacity.

Where it collapses back into a dial:
- **The fixed ½/½ mix.** The constant weighting ‖ψ‖ against χ decides how hard misaligned input is suppressed. Make that mix learnable, or drive it from one arousal variable, and it becomes the flat-to-copy dial: everything merges, or nothing does.
- **Binding by surface similarity.** RF reports "their tendency to group different shapes together based on shared color". Binding follows surface similarity unless higher-level input separates the groups. For a face, that means the agent's features would bind to the partner's whenever the two faces look alike, which is mimicry by similarity.
- **A built-in self-similarity grouping objective.** Nothing in these papers prevents a training objective, such as reconstructing the dyad, from making alignment the cheapest solution.

Any use would need a lesion test: does the alignment differ across feature groups within one situation? If everything aligns together, it is a scalar again.

## Verdict

watch. The computation (magnitude for presence, orientation for binding, summation gated by agreement) is old: Reichert & Serre 2014 and the temporal correlation hypothesis. These papers make it trainable and scale it. It is the one non-attention binding mechanism read so far in which "whose" is a separate channel from "how much", and it could make partner influence a per-feature angle instead of a gain.
