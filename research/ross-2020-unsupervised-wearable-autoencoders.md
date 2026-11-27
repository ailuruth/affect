# Unsupervised multi-modal representation learning for affective computing with multi-corpus wearable data (Ross, Hungler & Etemad)

Citation: K. Ross, P. Hungler, A. Etemad. "Unsupervised Multi-Modal Representation Learning for Affective Computing with Multi-Corpus Wearable Data." arXiv:2008.10726v1 (2020).

Source read: the arXiv PDF, text-extracted, read in full (all sections, Tables I–X). The t-SNE figure was read only through the text.

## What the paper does
- **Pipeline.** ECG (Pan-Tompkins band-pass, resampled to 256 Hz) and EDA (low-pass 1 Hz, moving-average, 128 Hz), each min–max normalised per subject and cut into 10-s windows. Two stacked 1-D convolutional autoencoders (one per modality; MSE plus L1 sparsity on weights) learn latent codes **without labels**. The two codes are concatenated (feature-level fusion) and a random forest (100 trees) classifies **binary arousal**.
- **Data.** AMIGOS (40), ASCERTAIN (58), CLEAS (10, medical simulation), MAHNOB-HCI (30); arousal ratings rescaled to 1–9 and binarised (< 5 low, ≥ 6 high).
- **Results (10-fold CV, stratified by dataset).**
  - Proposed: overall accuracy / F1 **0.89 / 0.91**; AMIGOS 0.93 / 0.95, ASCERTAIN 0.79 / 0.86, CLEAS 0.99 / 0.98, MAHNOB-HCI 0.83 / 0.76.
  - Hand-crafted HRV and EDA features with LASSO selection and the same classifiers: best 0.66 / 0.72 overall (random forest). A supervised CNN on the same inputs is also reported below the proposed method (its table cells did not extract cleanly enough to quote).
  - ECG codes are more discriminative than EDA codes for arousal in both learned methods (the reverse for hand-crafted features). Multi-corpus training helps the learned methods and not the hand-crafted ones (the text's statement; per-cell values not quoted).
  - The most important hand-crafted ECG feature is the minimum RR interval (LASSO coefficient 0.886).
- **Limits stated by the authors.** k-fold cross-validation only; leave-one-subject-out and leave-one-dataset-out are named as future work; only arousal.

## The mathematical object
**Per-modality convolutional autoencoders on short windows of a person's autonomic signals, with a late supervised probe for arousal.**

## What it means for the engine
1. **Arousal-related structure is present in a reconstruction latent of autonomic signals.** It is consistent with the brief's picture of arousal as a read-out of a learned body latent. But the evaluation shuffles 10-s windows across folds, so the same person and the same stimulus occur in training and test: as in sarkar-etemad-2020-self-supervised-ecg.md, the result is mostly within-person and within-episode.
2. **Window autoencoders have no time scale above 10 s.** The latent describes a window, not a body state evolving over minutes; it cannot carry mood-like persistence. A body latent for the engine must be a state-space model over time (as in the RSSM family), with the windows as observations.
3. **The engine's own body is simulated.** The Bot has no ECG. What carries over is only the pattern: autonomic-like channels of the agent's own body, encoded without labels, with arousal read out. Its own body variables are innate (Principle 2), so the learning problem here (inferring body state from noisy physiology) applies to reading the operator through his face and voice, not to the agent's own body.

## Verdict
- **background.** Label-free physiological latents carry arousal-related information within person and episode; no time structure, leaky evaluation.
