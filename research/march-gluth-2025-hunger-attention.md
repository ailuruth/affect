# March & Gluth 2024/2025: Hunger shifts attention and attribute weighting in dietary choice

Citation: J. March, S. Gluth. "Hunger shifts attention and attribute weighting in dietary choice." *eLife* 13: RP103736. Reviewed preprint 2024; Version of Record published 2 July 2025. doi:10.7554/eLife.103736. Preregistration: osf.io/tmdw3.

Source read: the eLife Version of Record PDF (56 pages). I read the abstract, introduction, behavioural and eye-tracking results, the model comparison table, the discussion opening, and the mediation tables in Appendix 7. Figure-only parameter posteriors (Fig. 5) were not extracted as numbers.

## Claims
- Hunger makes people weight taste over health more, and attention mediates this: "hungry participants focused more on tasty options, leading them to make less healthy decisions."
- In the best model, hunger acts in two separable places. It raises the decision weight on the taste attribute (ω). Separately, it raises the attention-dependent discounting of the unattended health attribute (φ_H), but not of taste. "Hunger did not only increase the relative taste compared to health weight, but it also increased the fixation-related discounting of health but not taste information."

## Evidence
- Design: 70 participants, within-subject, hungry and sated sessions in counterbalanced order, binary food choices with eye tracking. Taste was conveyed by food images and health by Nutri-Scores.
- Manipulation check: hunger ratings rose in the hungry session (mean change +22.4) and fell in the sated session (−36.3); F(1) = 26.31, p < .001.
- Choice GLMM:
  - tasty options were preferred overall (β_intercept = 0.73, SE 0.098);
  - satiety lowered tasty choice (β_sated = −0.211, SE 0.103, p = 0.04);
  - relative dwell time on the tasty option predicted choosing it (β = 0.998, SE 0.027).
- Mediation (hierarchical Bayesian):
  - the direct path from hunger to choice was 0.27, CI [0.03, 0.52];
  - with attention in the model, the direct path fell to 0.19, CI [−0.02, 0.41];
  - the indirect path a·b was 0.08, CI [0.01, 0.16].
- Model comparison by DIC (lower is better): DDM 69,646; aDDM 65,561; maaDDM 65,155; maaDDM2φ 64,002 (best). maaDDM2φ has separate attentional discounting for taste and for health.

## License
- Paper: CC BY.
- Code and data: github.com/JenniferMarch/HungryLens, GPL-3.0 (Bayesian DDM fits and behavioural analyses).

## Runs on this Mac without a GPU?
The behavioural analyses, yes. Hierarchical Bayesian DDM fitting runs on CPU but is slow. Not run. Nothing here would go into the engine.

## Verdict: watch (as a human benchmark for need-conditioned attention; not a mechanism to copy)
- It is the best recent quantitative evidence that a need state changes what is attended, broken down by content (attribute), and that attention carries part of the need's effect on choice.
- It is a descriptive decision model with one need (hunger), two states and two attributes. It is not an agent model, and it learns nothing.

## What it implies for the open question
- A need does more than scale the value of an option. It changes which attribute's information is discounted when unattended.
- A model with one gain on value fits these data worse than models with attribute-specific attention parameters. DIC falls from aDDM (65,561), through maaDDM with one shared attribute discount (65,155), to maaDDM2φ with separate taste and health discounts (64,002). Under hunger only the health discount changed.
- This is a human analogue of the brief's "selection depends on content, not only on magnitudes."
- The structure that pays here is need × attribute: an attention discount per attribute, modulated by need.
- Test template for a candidate: split the effect of a need into (a) a value-weight change and (b) an attention-allocation change. Ablate (b) and check whether the need's effect on choice is partly lost, as the mediation predicts.
