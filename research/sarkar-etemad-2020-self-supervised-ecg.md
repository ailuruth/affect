# Self-supervised ECG representation learning for emotion recognition (Sarkar & Etemad)

Citation: P. Sarkar, A. Etemad. "Self-supervised ECG Representation Learning for Emotion Recognition." *IEEE Transactions on Affective Computing* (2020). arXiv:2002.03898v2. (Extends their ICASSP 2020 paper, arXiv:1910.07497, whose PDF was also downloaded; the journal version was the one read.)

Source read: the arXiv PDF (journal version), text-extracted, read in full (all sections, Tables 1–6). Figures (loss curves, parameter sweeps) were read only through the text's description of them.

## What the paper does
- **Two stages.**
  1. **Self-supervised:** raw single-lead ECG (downsampled to 256 Hz, high-passed at 0.8 Hz, per-user z-scored, 10-s windows) is transformed six ways (Gaussian noise at a set SNR, scaling, negation, time reversal, segment permutation, time-warping), and a multi-task 1-D CNN (3 conv blocks shared, 7 binary heads) learns to tell each transformation from the original. No emotion labels.
  2. **Supervised:** the conv layers are frozen and transferred; new dense layers are trained on emotion labels (arousal, valence, affect state, stress) per dataset.
- **Data.** AMIGOS (40 people), DREAMER (23), WESAD (17), SWELL (25); the self-supervised stage uses all four pooled.
- **Results.**
  - Pretext recognition: mean F1 0.972, accuracy 0.992.
  - Emotion, multi-class: AMIGOS 9-class arousal / valence 0.796 / 0.783; DREAMER 5-class 0.771 / 0.749; WESAD 4 affect states 0.950; SWELL 9-class 0.926 / 0.938, stress 0.902.
  - Binary, against a fully supervised CNN of the same architecture: AMIGOS arousal 0.889 vs 0.844, valence 0.875 vs 0.811; DREAMER 0.859 vs 0.707, 0.850 vs 0.666; WESAD 3-class 0.969 vs 0.932; SWELL stress 0.933 vs 0.894.
  - **Pretext difficulty has an optimum:** too easy (strong distortion, e.g. SNR < 10, scaling outside 0.6–1.4) or too hard (nearly identical, e.g. SNR > 35) both give poor emotion accuracy; best multi-task vector (SNR 15, scale 0.9, 20 permutation segments, 9 warp segments, stretch 1.05). Multi-task beats any single task. The last conv block's features are best. Pooling the four datasets for pretraining beats single-dataset pretraining.
- **The evaluation's weakness.** Ten-fold cross-validation is done **after shuffling 10-s segments**, so segments from the same person and the same video clip fall in both training and test sets. The authors state that the method "performs poorly in subject-independent emotion recognition" and attribute it to person-specific ECG factors they did not calibrate away.

## The mathematical object
**A shared encoder trained to discriminate a fixed family of signal transformations of a person's physiological signal; its features are then probed for affect by a supervised head.**

## What it means for the engine
1. **What a label-free body latent learns first is the person.** The reported accuracies are within-person and largely within-clip; across people the representation fails. A latent body state learned without labels from physiological signals is dominated by individual and session factors. For an engine that lives with one person, the analogous nuisance is the session: electrode or sensor placement, posture, time of day. The slowest levels of a hierarchical latent will absorb these first (the same warning as the CW-VAE top level storing textures).
2. **Invariances chosen by the pretext decide what survives.** Recognising scaling and noise makes the encoder sensitive to amplitude and waveform detail; nothing in the pretext asks for change over minutes. A body latent for affect needs a temporal objective (prediction over the time scales of regulation), not instance discrimination of 10-s windows.
3. **Difficulty optimum.** The inverted-U between pretext difficulty and downstream usefulness is a practical note for any self-supervised body encoder in the engine.
4. **Labels.** The supervised stage uses arousal and valence labels and would be excluded below the Claude layer (Principle 1). Only the self-supervised encoder is admissible material.

## Verdict
- **background (cautionary).** Shows that self-supervised physiological features carry affect-related information within a person, and that the learned body latent is person- and session-bound. The headline numbers are inflated by segment-level shuffling and cannot be compared with subject-independent results.
