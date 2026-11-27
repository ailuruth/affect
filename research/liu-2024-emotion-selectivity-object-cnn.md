# Emergence of emotion selectivity in deep neural networks trained to recognize visual objects (Liu, Bo, Ding & Fang)

Citation: P. Liu, K. Bo, M. Ding, R. Fang. "Emergence of Emotion Selectivity in Deep Neural Networks Trained to Recognize Visual Objects." *PLoS Computational Biology* 20(3), e1011943 (2024). doi:10.1371/journal.pcbi.1011943.

Source read: the journals.plos.org full-text HTML, text-extracted, read in full (abstract, introduction, results, discussion, methods). **Not read:** the S1 Text supplement (AlexNet replication, GIST/SVM low-level control, object-category ANOVA) and the numeric cells of Table 1 (an image). Claims about the supplement below are the main text's own summaries.

## What the paper does
- **Question.** Is affect-specific visual representation intrinsic to a visual hierarchy, or must it come from re-entry (e.g. from the amygdala)? Tested by asking whether units in a network never trained on affect become selective for it.
- **Model and stimuli.** VGG-16 pre-trained on ImageNet object recognition, weights frozen. Grayscale images from IAPS (1,182) and NAPS (1,356), sorted by normative valence into pleasant / neutral / unpleasant (soft thresholds 4.3 ± 0.5 and 6.0 ± 0.5, plus visual inspection; IAPS 296/390/341, NAPS 352/477/281).
- **Selectivity.** Per filter ("neuron"), the mean response over the feature map; a selectivity index SI = the largest d′ between one category and the others. Neurons below the 20th SI percentile are dropped (threshold chosen by an attention-enhancement sweep); a neuron counts as selective only if selective for the same category on both IAPS and NAPS.
- **Findings.**
  - Selectivity exists in every convolutional layer and rises with depth, more clearly on IAPS. The top-100 images of a deep "pleasant" neuron are mostly high-valence.
  - Cross-dataset overlap of selective neurons exceeds the overlap of random sets in all layers, more in deep layers; a **randomly initialised** VGG-16 shows low selectivity with no layer trend and fewer selective neurons from layer 5 on. So the selectivity comes from object training.
  - **Causal tests** with a new two-unit readout trained per contrast (pleasant vs not, etc.; 50/25/25 split): raising the ReLU slope (gain, "feature attention") of the selective neurons improves recognition of their category; zeroing them degrades it, "as high as 80 %" in deep layers; the same manipulations on random neurons do little or harm. Selective-vs-random enhancement differs at p < 1.2 × 10⁻² in middle and deep layers.
- **Limits stated by the authors.** Only three valence bins; low-level confounds partly addressed (grayscale; GIST features could not decode the categories; neurons respond more to emotion than object category, with interactions in deep layers; the object analysis is called preliminary); faces and animacy not controlled; no comparison with neural recordings during emotion recognition, so neural relevance is "speculative".

## The mathematical object
**Post-hoc selectivity of units in a network trained on a non-affective objective, defined by d′ against externally rated valence bins and confirmed causally by gain and lesion of those units under a separately trained readout.**

## What it means for the engine
1. **Supports Principle 2 in a narrow sense.** A valence-like axis can be found in a representation never trained on affect: affect read out, not set. But the readout and the selection of "selective" units both use external valence ratings; the network itself has no valence variable. For the engine, the readout target must be the agent's own drive change, not human ratings (Principle 1).
2. **Content, not affect.** Object training makes units selective for what pleasant and unpleasant scenes contain (the authors cannot exclude animacy, faces). The engine's analogue: a predictive latent trained on the partner's face and words will carry partner-content structure that a readout calls "valence" without any body involvement. That is the reading-through-the-agent's-own-body principle failing silently. The test must be whether the readout tracks the agent's **own** body change.
3. **A transferable evaluation method.** Gain-up and lesion of the units most selective for a readout direction, compared with matched random units, is a cheap ablation for the engine's latent (brief Principle 5, judged on internal state).
4. **Depth trend.** Selectivity grows with depth, so in a hierarchical engine latent the affect readout should sit high (slow levels), not in the first perceptual layers.

## Verdict
- **background (evidence that affect-like structure emerges as a by-product of non-affective training; method: selective-unit gain and lesion).** Not a mechanism for the core. Its use of human valence labels to define selectivity is acceptable only as an evaluation step outside the engine.
