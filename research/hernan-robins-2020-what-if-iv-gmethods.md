# Hernán & Robins, *Causal Inference: What If* (Chapman & Hall/CRC 2020; free PDF version dated 19 Aug 2026), ch. 16 (instrumental variables) and ch. 19–21 (time-varying treatments, treatment–confounder feedback, g-methods)

Source read: the authors' free PDF (hernanrobins_WhatIf_19aug26.pdf, from miguelhernan.org/whatifbook).
- **Read in full:** ch. 16 main text §16.1–16.6, with Technical Points 16.1, 16.2, 16.5, 16.6, part of 16.7, and Fine Points 16.1–16.2; §20.1–20.4.
- **Read in part:** ch. 19 (§19.1, Fine Point 19.1, the parts of §19.3–19.4 defining sequential randomisation and sequential exchangeability, §19.6); ch. 21 (§21.1 g-formula and §21.2 IP weighting).
- **Not read:** §16.3 except its opening, §19.2, §19.5, §20.5, §21.3–21.6 (doubly robust estimators, g-estimation of structural nested models, censoring, the big g-formula), and ch. 22.

## Claims
**Instrumental variables (ch. 16)**
- An instrument Z must satisfy three conditions.
  - (i) Relevance: Z is associated with treatment A. This is the only condition that can be checked.
  - (ii) Exclusion: Z has no effect on outcome Y except through A.
  - (iii) Exchangeability: Z and Y share no causes.
  - (ii) and (iii) "cannot be empirically verified", and falsification tests have power only against a small subset of violations.
- The three conditions alone identify only bounds, which are often wide and include 0. Point identification needs a fourth condition: either effect homogeneity or monotonicity.
  - Under homogeneity, the usual estimand is the average causal effect.
  - Under monotonicity (no "defiers"), it is the effect in the compliers (Imbens & Angrist 1994).
- The usual IV estimand is (E[Y|Z=1] − E[Y|Z=0]) / (E[A|Z=1] − E[A|Z=0]); for continuous Z it is Cov(Y,Z)/Cov(A,Z) (the Wald estimator). It equals two-stage least squares. "The IV estimand bypasses the need to adjust for the confounders by inflating the effect of assignment."
- Weak instruments cause three problems:
  - wide intervals;
  - amplification of any violation of (ii) or (iii), since the numerator bias is divided by a small denominator;
  - finite-sample bias even with a valid instrument.
  A common rule of thumb calls an instrument weak if the first-stage F < 10. "A strong proposed instrument that slightly violates conditions (ii) and (iii) may be preferable to a less invalid, but weaker, proposed instrument." Coarsening a continuous treatment can break exclusion (Fig. 16.9).
- IV is "better reserved for" settings with a dichotomous, time-fixed treatment and a strong, causal instrument, so the book does not use it for sustained, time-varying treatments.

**Time-varying treatments (ch. 19–21)**
- A sequentially randomised experiment assigns A_k at random with probabilities that depend only on recorded history (Ā_{k−1}, L̄_k). It implies sequential exchangeability: Y^g ⊥⊥ A_k | Ā_{k−1}, L̄_k for all strategies g. Observational studies cannot be shown to meet it.
- Treatment–confounder feedback: the time-varying confounder L_k affects later treatment, and earlier treatment affects L_k (A_{k−1} → L_k → A_k). Feedback cycles are drawn as acyclic graphs unrolled in time (Fine Point 20.1).
- Under treatment–confounder feedback, "traditional methods cannot be used to correctly adjust for those confounders," even with sequential exchangeability and all confounders measured.
  - Stratification or regression on L_k conditions on a collider (A_{k−1} → L_k ← U → Y), which opens a non-causal path.
  - Not adjusting leaves confounding.
  - The bias "cannot be fixed" by more flexible regression, "because regression is a conventional stratification-based method itself."
- G-methods handle it:
  - the g-formula E[Y^{a0,a1}] = Σ_{l1} E[Y | A0=a0, L1=l1, A1=a1] f(l1 | a0);
  - IP weighting with W^Ā = ∏_k 1/f(A_k | Ā_{k−1}, L̄_k), or stabilised SW^Ā = ∏_k f(A_k | Ā_{k−1}) / f(A_k | Ā_{k−1}, L̄_k);
  - g-estimation (not read).
- Random strategies are dominated by the best deterministic one, but "random strategies (i.e., randomized trials) remain scientifically necessary because, before the trial, it is unknown which deterministic strategy is optimal" (Fine Point 19.1).

## Evidence with numbers
- IV worked example (smoking cessation and weight, NHEFS; instrument: cigarette price > $1.50 in the state of birth):
  - numerator 2.686 − 2.536 = 0.1503 kg; denominator 0.2578 − 0.1951 = 0.0627; Wald estimate 2.4 kg;
  - 95% CI −36.5 to 41.3; first-stage F = 0.8;
  - moving the threshold to $1.60, $1.70, $1.80 or $1.90 gives 41.3, −40.9, −21.1 or −12.8 kg;
  - any numerator bias is multiplied by about 15.9 (= 1/0.0627).
- Treatment–confounder feedback example (Table 20.1; hypothetical sequential trial, N = 32,000; A0 randomised at 0.5; A1 randomised at 0.4 if L1 = 0 and 0.8 if L1 = 1; true effect 0):
  - unadjusted contrast of "always" vs "never" treated: −13.3;
  - stratified on L1: −8 in both strata;
  - g-formula: 84×0.25 + 52×0.75 = 60 for never treated, 76×0.5 + 44×0.5 = 60 for always treated, effect 0;
  - IP weighting: also 0.

## Mechanism
The IV estimand is a ratio of two intention-to-treat effects. The Z→A effect can be causal (randomisation) or a surrogate association. Under treatment–confounder feedback, the joint effect of the sequence Ā is identified by modelling either:
- the confounder's evolution given past treatment (g-formula), or
- the treatment's assignment given the past (IP weighting).
Never stratify on L_k.

## What it implies for an engine that learns a partner model from closed-loop interaction
Translate the variables:
- treatment A_k = the agent's expression x_k at step k;
- time-varying confounder L_k = the partner's face z_k: it drives the agent's next expression through following, and, if the partner responds, it is itself driven by the agent's earlier expression;
- unmeasured U = the partner's hidden state (mood, topic, what they are listening to);
- outcome Y = the partner's later face.

This is textbook treatment–confounder feedback.
1. **Why both naive rules fail.**
   - Regressing z on the agent's lagged x without z's past leaves the backdoor x_k ← z_{k−1} → z_{k+1} open. That is C13.
   - Regressing on x_k *and* z_k (the ARX/Granger fix) conditions on a collider, x_{k−1} → z_k ← U → z_{k+1}, whenever the partner has hidden persistent state.
   - The book's statement that this "cannot be fixed" by better regression matches our simulation in forssell-ljung-1999-closed-loop-identification.md: ARX stayed biased under a hidden slow partner drive.
2. **The agent can be its own sequentially randomised trial.** The book's hardest requirement is knowing or estimating f(A_k | history). The agent *owns* its expression policy. If x_k = g(history) + b_k with b_k drawn from a known, logged distribution, then:
   - f(x_k | history) is known exactly;
   - sequential exchangeability holds *by construction*, provided nothing unlogged that also drives the partner enters x_k;
   - positivity requires that every expression level keeps non-zero probability in every history, so the agent must never follow deterministically.
   IP weighting with the agent's own known propensities is then available without any model of the partner's dynamics. This is a second identification route beside IV: weight each (x_k, z_{k+τ}) pair by f(x_k)/f(x_k | history).
3. **IV with the micro-variation as Z.** b_k satisfies (iii) if it is drawn independently of the partner, and (i) if it moves the expression enough (first-stage F ≫ 10). Exclusion (ii) is the delicate one. b must reach the partner only through the expression channel whose effect is being learned.
   - If b also moves voice or head pose, and the partner responds to those, an R learned on the face alone absorbs those effects. Either include all channels b moves in x, or give each channel its own independent b.
   - Coarsening x, for example learning R on a few summary axes while b moves the full 52-blendshape face, can break exclusion exactly as Fig. 16.9 warns.
4. **Weak-instrument danger is real at expression scale.** Micro-variations small enough to be invisible are, almost by definition, weak instruments. They amplify any leak in exclusion and give finite-sample bias toward the confounded estimate. Required diagnostics:
   - log the first-stage strength (b→x) per channel and per window;
   - refuse to update R when it is weak;
   - prefer a somewhat larger, cleaner probe to a tiny one ("a strong proposed instrument that slightly violates (ii) and (iii) may be preferable").
5. **Heterogeneity.** With a continuous, time-varying x, the IV estimand is a weighted average effect. The weights are set by where b moves x most, a LATE-like quantity. If the partner responds differently to large and to micro expressions, R learned from micro-variation may not extrapolate to full expressions. This argues for probes at more than one amplitude.

## License
Book, © Hernán & Robins; free PDF distributed by the authors for personal use. No code used here (they provide R, Stata, SAS and Python programs for the NHEFS examples; not downloaded).

## Verdict: adopt (the identification conditions and the "own known propensity" route)
Ch. 16 supplies the checklist for using micro-variations as instruments: relevance, exclusion, exchangeability, a fourth condition, and weak-instrument diagnostics. Ch. 20 proves on a 32,000-person example that adjusting for the partner's past face is not a fix under feedback. Ch. 21's IP weighting fits an agent that knows its own randomisation probabilities. Caveats:
- The book's methods are for discrete times, populations of individuals and fixed strategies. The dyad is one long series with one partner, so ergodicity and stationarity within windows take the place of a population.
- The book itself reserves IV for time-fixed treatments, and its time-varying IV extension (g-estimation of structural nested mean models with instruments, Technical Point 16.6) was not read.
