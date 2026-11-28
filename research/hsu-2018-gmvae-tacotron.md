# Hsu et al. 2018, "Hierarchical Generative Modeling for Controllable Speech Synthesis" (GMVAE-Tacotron)

Hsu, W.-N., Zhang, Y., Weiss, R. J., Zen, H., Wu, Y., Wang, Y., Cao, Y., Jia, Y., Chen, Z., Shen, J., Nguyen, P. & Pang, R. (2018/2019). ICLR 2019. arXiv:1810.07217. https://arxiv.org/abs/1810.07217

**How fully read:** sections 1–4 in full and appendix G.1 (Table 10 from the layout extraction); other appendices skimmed. Demos not listened to.

## What it says
- Tacotron 2 with two latent levels: a K-way categorical y_l and, given it, a 16-d diagonal Gaussian z_l, so the prior on z_l is a Gaussian mixture; optionally a second pair for speaker-related attributes. Trained as a VAE without attribute labels. Diagonal covariances "encourage each dimension to capture a statistically uncorrelated factor".
- Dimensions are found after training by traversal and by an inter-/intra-component variance ratio; on the 147-h single-narrator audiobook corpus (the same one GST used) individual dimensions control F0, speaking rate, accent, initial silence; on noisy data one dimension controls noise level (ratio 21.5 vs 0.6 for the next).
- Table 10 (±3 σ on one dimension, 250 utterances each): the "pitch" dimension moves mean F0 178.3 → 187.1 → 204.4 Hz with duration fixed at 3.5 s; the "speaking rate" dimension moves duration 3.0 → 3.5 → 4.0 s **and mean F0 197.1 → 189.7 → 182.5 Hz** (about 8 % over the range).
- Against GST: GST token weights are correlated; setting one GST weight to −0.1 gave "tremolo at the end" and "abnormally long duration for the first syllable" (Fig. 7a); GST needed careful tuning to find a stable sampling region.

## What matters for this engine
- The best case for design (c): continuous, unsupervised, nearly one dimension per attribute. Even here the disentanglement is partial (rate moves pitch), the axes are discovered and named after training, their meaning is the training corpus's expressive modes, and their effect is text- and seed-dependent. A per-channel ceiling c_k would have to be checked on the rendered audio, not on the latent.
- Negative or out-of-range values are where the agent needs sign flips; the paper shows GST degrades there and reports GMVAE traversals only within ±3 σ of the training marginal.

## Verdict: reject (for the voice channels); background on why learned prosody axes are not channels
