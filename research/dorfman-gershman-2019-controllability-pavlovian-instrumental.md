# Dorfman & Gershman 2019: Controllability governs the balance between Pavlovian and instrumental action selection

Citation: H. M. Dorfman, S. J. Gershman. *Nature Communications* 10: 5826, 2019. doi:10.1038/s41467-019-13737-7. PMC6925275. Publisher correction: *Nat Commun* 11: 3497 (2020), doi:10.1038/s41467-020-17420-0. The correction only fixes a label in the Fig. 2b table: the last row should read "High Control Decoy".

Source read: the full text via the Europe PMC open-access XML, covering the abstract, results, discussion, methods (Eqs. 1–11) and figure captions, plus the correction notice. The **Supplementary Information was not read**. That includes the full derivation for the controllable model, the parameter table and the disaggregated data. The Fig. 2b reward table was seen only through the text and the correction, so I do not know the decoy's No-Go reward probability. **The paper has no EEG or neural data.** It is behaviour plus model comparison only. The adaptive weight is offered as a target for later neuroimaging.

## Claims
- "The brain arbitrates between Pavlovian and instrumental control by inferring which is a better predictor of reward. … The Pavlovian predictor will be favored when rewards are relatively uncontrollable, because the additional flexibility of the instrumental predictor is not useful."
- Pavlovian and instrumental systems are two predictive models: one indexed by stimulus (θ_s) and one by stimulus–action (θ_sa). The instrumental model nests the Pavlovian one. Bayesian Occam's razor favours the simpler model until the data justify the action dependence. "Asymptotically, the instrumental predictor will always be favored."
- The Pavlovian weight w "is determined endogenously by an arbitration process", not fitted as a fixed trait. w is literally "the posterior probability of the uncontrollable environment".
- The authors' framing: "agency is one factor that can mediate the trade-off between learning processes." They link the account to learned helplessness and to Huys & Dayan's Bayesian controllability.

## Evidence
- Task: Go/No-Go for reward only (no punishment). Go-to-Win cue: Go rewarded 75%. No-Go-to-Win cue: No-Go rewarded 75%. Decoy cue: Go rewarded 50% under Low Control (LC) and 80% under High Control (HC). Exp. 1 is between subjects (120 trials, 40 per cue). Exp. 2 is within subjects (240 trials, two blocks).
- N: Exp. 1 recruited 271 and kept 185. Exp. 2 recruited 183 and kept 129 (exclusions for ≥ 50% errors overall or < 30% on any condition; the supplement reports results without exclusions). All were MTurk adults.
- Go bias (accuracy on Go-to-Win minus No-Go-to-Win) was larger under LC than HC. Exp. 1: t(183) = 2.06, p < .05, **d = 0.31**. Exp. 2: t(128) = 2.06, p < .05, **d = 0.18**. These are small effects.
- Model comparison: the adaptive model (w updated by Bayes) beat the fixed-w model with protected exceedance probability **> 0.99** in both experiments.
- Within participants, Go bias rose with the model's w quantile (lowest versus highest quantile: Exp. 1 t(177) = 12.30, d = 0.92; Exp. 2 t(54) = 6.16, d = 0.83). The adaptive w time series correlated with fixed-model w estimates (r = 0.51 and r = 0.63).
- Go bias declined over trials, roughly exponentially (regression on log trial: Exp. 1 t(184) = 2.93, d = 0.22; Exp. 2 t(128) = 5.55, d = 0.49).
- Bias–variance: HC gave lower choice bias in both experiments (d = 0.31, d = 0.18). It gave higher choice variance in Exp. 2 (d = 0.21) and only a trend in Exp. 1 (p = .09).
- Caveat stated by the authors: Swart et al. show part of the Go bias is an *instrumental* learning asymmetry (faster learning from rewarded Go), "not accounted for by our modeling framework". A symmetric No-Go bias under punishment is predicted but untested.

## Formal model (quoted from Methods)
- Model m ∈ {controllable, uncontrollable}. Parameters `θ_s = E[r | s]` (uncontrollable) or `θ_sa` (controllable). Beta prior `Beta(θ_0 η_0, (1−θ_0) η_0)` (the extracted text writes the arguments with a "/2" that may be an extraction artifact).
- Learning: `Δθ̂_s = η_s⁻¹ δ`, `δ = r − θ̂_s`. The counter η_s starts at η_0 and increments on each visit, so the learning rate is 1/count (exact Bayesian posterior mean).
- Model evidence: `P(m | D) ∝ P(D | m) P(m)`, with `P(D | m) = ∫ P(D | θ, m) P(θ) dθ`.
- Log-odds `L = log P(uncontrollable)/P(controllable)`, updated each trial by the log ratio of one-step predictive probabilities:
  `ΔL = r·log(θ̂_s / θ̂_sa) + (1 − r)·log((1 − θ̂_s)/(1 − θ̂_sa))`.
- Pavlovian action value: `V_P(s, Go) = θ̂_s` and `V_P(s, NoGo) = 0` ("Pavlovian reward expectations invigorate action"). Instrumental: `V_I(s, a) = θ̂_sa`.
- Arbitration: `V(s, a) = w V_P(s, a) + (1 − w) V_I(s, a)`, with `w = 1/(1 + e^{−L})`.
- Choice: softmax with inverse temperature β. Free parameters: β, and (θ_0, η_0) per condition. A model fitting L_0 lost to "fixing L_0 = 0.5" (as written; on a log-odds scale this is a slight prior toward uncontrollable).

## License
CC BY 4.0. Data and model code: github.com/sjgershm/GoNogo-control. Task code: github.com/hayleydorfman/pavlovian-instrumental-arbitration.

## Runs on this Mac without a GPU?
Yes. The model is closed-form counting.

## Verdict: adopt (as the arbitration equation: controllability = the Bayes factor between action-conditioned and action-free predictors)
- It is the cleanest statement that a controllability estimate does not need to be a separate module or a named variable. It is the posterior over model structure in a learner that already keeps both predictors, and it then sets how much cue-driven (Pavlovian) versus action-contingent value drives behaviour.
- The behavioural effects are small (d = 0.18–0.31), reward-only, and online samples with heavy exclusion. The model comparison is strong, but it compares only two models.

## What it implies for the engine
- **A label-free controllability term.** If the core's generative model predicts need reduction both with and without conditioning on its own action, the running log Bayes factor L is controllability. Nothing is named. Huys & Dayan's χ is the prior side, and this L is the evidence side.
- **It ties controllability to wanting.** The Pavlovian value `θ̂_s` acts on vigour toward the cue regardless of the action's consequence. That is the cue-triggered "wanting" channel (Berridge's incentive salience, Zhang & Berridge's κ-scaled cached value). Low controllability *raises* the weight of that channel. Two predictions for the engine follow:
  - after uncontrollable episodes, cue-driven approach and withdrawal (toward the partner's face cues, say) should dominate over action-contingent choice;
  - incentive salience and controllability are not independent axes, because w couples them.

  The consummatory readout ("liking") is untouched by w, since both predictors learn from the same realized r. That is one half of the dissociation: w can raise pursuit without changing the hedonic signal on contact.
- **Satiable drives.** With r replaced by realized drive reduction, κ_i-modulated θ̂_s gives need-specific Pavlovian values. The arbitration weight can then be indexed per need (w_i) or per context. Making w a single scalar would reintroduce the flat-gauge failure the brief warns about.
- **Who caused it.** The two-model comparison is the minimal case. Adding a third predictor, conditioned on the *partner's* action, would give a posterior over "my action / their action / neither" as causes. This paper does not do that, but its equations extend directly (see the Ligneul note).

## Ablations that separate it
1. **Fix w** (the paper's own "fixed model"). The Pavlovian bias stops tracking controllability, and the Go bias stops declining with experience. Behaviourally this is the losing model, so the effect it removes is measurable.
2. **Remove the action-free predictor** (instrumental only, w = 0). No Pavlovian misbehaviour and no controllability-dependent cue approach. Cue-triggered pursuit disappears while the realized readout on contact is unchanged: half of the wanting/liking double dissociation.
3. **Remove the action-conditioned predictor** (w = 1). Behaviour is all cue-driven. The agent cannot learn the omission contingency (negative automaintenance, Hershberger's chicks).
4. **Shared versus need-indexed w.** With one shared w, an uncontrollable episode about one need raises cue-driven behaviour for every need. With w_i, only that need's cues are affected. This is the same selectivity test as Zhang & Berridge's κ_i.
