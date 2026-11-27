# Object-Centric Learning with Slot Attention (Locatello, Weissenborn, Unterthiner, Mahendran, Heigold, Uszkoreit, Dosovitskiy & Kipf)

Citation: F. Locatello, D. Weissenborn, T. Unterthiner, A. Mahendran, G. Heigold, J. Uszkoreit, A. Dosovitskiy, T. Kipf. "Object-Centric Learning with Slot Attention." *NeurIPS* 2020. arXiv:2006.15055.

Source read: arXiv v2 PDF, text-extracted. Read in full: abstract, §1–5, Algorithm 1, Proposition 1, Table 1, figure captions, Broader Impact. **Not read:** the supplementary material (proof of Proposition 1, ablations, further results).

## The module
- **Inputs** N feature vectors (CNN feature map plus position embeddings); **outputs** K slots, initialised by sampling from one shared learned Gaussian N(μ, diag σ), refined for T = 3 iterations.
- **Each iteration.**
  - attn = softmax over **slots** of k(inputs)·q(slots)ᵀ/√D. Normalising over the queries, not the keys, makes slots **compete** to explain each input; every input's weights sum to one, so no input can be ignored.
  - updates = weighted **mean** of v(inputs) per slot (more stable than a sum, since weights are normalised over slots).
  - slots = GRU(previous slots, updates), shared across slots, plus an optional residual MLP; LayerNorm on inputs and slots.
  - Complexity O(T·D·N·K).
- **Proposition 1.** SlotAttention(π_i·inputs, π_s·slots) = π_s·SlotAttention(inputs, slots): invariant to input order, equivariant to slot order. Slots share one representational format, so any slot can bind any object, unlike capsules or per-element initialisations (DETR, Set Transformer, DSPN), which cannot generalise to more elements.
- **Relation to known methods (the authors').** Soft k-means with learned projections and a learned update; a variant of interacting-memory models (RMC, RIM), differing in normalising over slots; related to mixtures of experts, but parameters are fully shared.

## Results
- **Unsupervised object discovery** (reconstruction loss only; ARI excluding background, 5 seeds): CLEVR6 98.8 ± 0.3 (IODINE 98.8 ± 0.0, MONet 96.2 ± 0.6); Multi-dSprites 91.3 ± 0.3 (IODINE 76.7 ± 5.6); Tetrominoes 99.5 ± 0.2 with one of five seeds excluded (it segmented the image into stripes).
- **Generalisation.** Trained with T = 3 and K = 7, more test-time iterations improve ARI; with K = 11 it still segments CLEVR10 scenes with more objects than seen in training. Surplus slots stay empty. Background is spread across all slots.
- **Efficiency.** Batch 64 on one 16 GB V100 vs 4 for IODINE; ~24 h vs ~7 days on 8 GPUs.
- **Supervised set prediction** (CLEVR10, Hungarian matching): matches or beats DSPN with a smaller encoder; attention masks segment objects with no mask supervision (ARI 78.0 ± 2.9).
- **Limits stated.** Synthetic, well-controlled scenes only; expected to struggle with complex textures and backgrounds.

## The mathematical object
A **competitive, exchangeable binding of inputs to a set of latent entities that all share one update rule**: an iterated soft assignment normalised over the entities, followed by a shared recurrent update per entity. Its symmetry is the permutation group on slots.

## What it means for the design
1. **"Read the other through one's own body" as weight sharing.** If the agent's own state and its model of the partner are two slots of one set, updated by the same learned body dynamics, then the partner is modelled by literally the agent's own model. Proposition 1 makes that exact, not approximate.
2. **Binding by competition is "who caused this".** Normalising over slots means each sensory feature is explained by one entity at a time, so self- and partner-caused input explain each other away.
3. **The hazard this predicts.** Competition gives each input to the slot that predicts it best. A partner who moves in synchrony with the agent is predicted best by the self slot, so it is claimed by the self. That is the enfacement failure measured in maister-2013-mirror-touch-enfacement.md. And slot symmetry makes "self slot and partner slot in the same state" a distinguished configuration, as the two-agent equivariance lesson of new-core-search-3 found for EGNN.
4. **Variable cardinality.** Dyads and groups, and new people, are handled by adding slots with no new parameters.

## Verdict
- **watch (object for binding self, partner and episodes as exchangeable entities).** As a mechanism it is soft k-means with a learned update; for the dyad it is a recombination with a predicted copy hazard.
