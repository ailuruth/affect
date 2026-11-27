# Distributed neural processing predictors of multi-dimensional properties of affect (Bush, Inman, Hamann, Kilts & James)

Citation: K. A. Bush, C. S. Inman, S. Hamann, C. D. Kilts, G. A. James. "Distributed Neural Processing Predictors of Multi-dimensional Properties of Affect." *Frontiers in Human Neuroscience* 11, 459 (2017). doi:10.3389/fnhum.2017.00459.

Source read: the frontiersin.org full-text HTML, text-extracted, read in full (abstract, introduction, methods, results with Tables 1–3, discussion). **Not read:** the supplementary tables and figures (full individual-ROI and intra-subject results, sex-difference maps).

Intended sources for the representational geometry of affect in brains that could **not be reached**: Horikawa, Cowen, Keltner & Kamitani 2020 (*iScience*; bioRxiv returned a Cloudflare rate-limit error, cell.com refused by the proxy); Abdel-Ghaffar et al. 2024 (*Nature Communications*, occipital-temporal tuning to semantic and affective features; nature.com refused by the proxy). This note is therefore the only brain source on affect geometry in this pass, and it is a decoding study, not an RSA study.

## What the paper does
- **Data.** 32 healthy adults (diverse in age, sex, race, education), 3T fMRI, an incidental "Encoding of Affective Pictures" task: 45 of 90 images per person (53 IAPS, 37 lab images rescaled to IAPS norms; 15 positive, 15 neutral, 15 negative), 2.5 s each, rating valence with a button press. Beta-series per trial (single-trial activation maps).
- **Labels.** Normative valence and arousal, each binarised at 5.0 on the 9-point scale (and self-reported valence).
- **Analyses.** Univariate GLM contrasts; linear SVM multivoxel classification on whole-brain grey matter, on all GLM ROIs, on relaxed ROIs, and on single ROIs; inter-subject (leave-one-subject-out) and intra-subject (leave-one-stimulus-out) cross-validation; Haufe-transformed encoding maps; a Gaussian process over affect space of where trials are misclassified.
- **Results.**
  - Inter-subject whole-brain accuracy: **valence 0.589** (95 % CI 0.568–0.610), **arousal 0.555** (0.533–0.578), self-reported valence 0.610; valence better than arousal (p < 0.05). Normative and self-reported valence do not differ.
  - **Whole brain beats every ROI set**, including liberal ones with 10× more voxels (valence aROI 0.511, relaxed p < 0.05 0.554). Of single ROIs only left precuneus predicted valence above chance (0.524), and it is outside the "neural reference space" of affect. The amygdala responds in univariate contrasts (negative valence, high arousal) but does not predict either dimension alone.
  - **Intra-subject** classification is at chance for valence (whole brain) and **below chance for arousal** (whole brain, left visual cortex, left amygdala), which the authors attribute to anti-learning with 40 training trials of 36,594 voxels.
  - SVM hyperplane distance correlates with normative ratings (valence r = 0.55, arousal r = 0.46).
  - **Where the geometry fails:** systematic misclassification for clearly positive or negative images of moderate arousal (V ≈ 7.2 and 2.5 at A ≈ 4.5).
- **Interpretation (the authors').** Valence and arousal are encoded in a highly distributed way; single-region accounts are untenable; neurofeedback should target distributed read-outs. Their main stated limitation: affect may be non-linearly organised in brain state space, and they used only a linear classifier on binary labels.

## The mathematical object
**Linear separability, across people, of single-trial whole-brain activity by externally rated valence and arousal, measured against region-restricted subsets.**

## What it means for the engine
1. **Valence and arousal are weak linear axes in brain activity.** Across 32 people, the best linear read-out of binarised valence is 59 % and of arousal 56 %, and it fails where arousal is moderate. Consistent with Kragel & LaBar 2016 (already in the index: categories decode beyond valence/arousal) and Russell 2003 (components share 10–15 % of variance): **a two-axis affect latent is not what brains show**. The engine's latent should be rich, with valence and arousal as noisy, partial read-outs (Principle 2; brief's expressive-structure item).
2. **Distributed, not localised.** No region carries the dimensions; the whole state does. For the engine this argues against a dedicated "affect block" and for affect as directions read across the whole latent, with ablations aimed at distributed directions, not at modules.
3. **Within-person read-out is the hard case.** With one person and few labelled trials the linear read-out anti-learned. The engine lives with one person and will never have many labelled trials (it has none). So any check of "valence emerges" must use the agent's own drive change as the target and many unlabelled hours, not a handful of rated episodes.

## Verdict
- **background (evidence about the geometry: affect is distributed and only weakly, partially linear in valence and arousal).** Small images-only paradigm, binary labels, linear classifier; not a mechanism.
