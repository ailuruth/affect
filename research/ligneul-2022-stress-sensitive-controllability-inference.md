# Ligneul, Mainen, Ly & Cools 2022: Stress-sensitive inference of task controllability

Citation: R. Ligneul, Z. Mainen, V. Ly, R. Cools. *Nature Human Behaviour* 6: 812–822, 2022. doi:10.1038/s41562-022-01306-w. Preprint: bioRxiv 10.1101/2020.11.19.390393 (v3, 9 January 2022, the version that became the journal paper). Context: R. Ligneul, "Prediction or causation? Towards a redefinition of task controllability", *Trends in Cognitive Sciences* 25(6): 431–433, 2021, doi:10.1016/j.tics.2021.02.009.

Source read: the full **bioRxiv v3 PDF** (27 pages), extracted with pdftotext, covering the abstract, introduction, results, discussion, methods (computational model equations, task, stress induction, fMRI pipeline) and figure captions. The journal version is paywalled. Only its abstract was read, and it matches v3. The Supplementary Notes (the TE derivation, the Ω-versus-TE differences, the alternative H and JS models, parameter tables) were not read. The TICS piece is closed access, so only its two-sentence abstract was read.

## Claims
- A task is controllable when actions carry information about the next state *beyond* what the current state carries. "A task can thus be deemed controllable when the transfer entropy (TE) … linking state and action time-series is positive. By comparing the entropy of observed states given previous states and actions [H(S'|S,A)] to the entropy of observed states given previous states only [H(S'|S)], this information-theoretic quantity isolates the effective causal influence of actions."
- Controllability ≠ predictability. Mutual information between action and outcome is "necessary but not sufficient". The forecaster example: the forecaster's statements predict rain but do not control it, because both depend on the past weather. The TICS abstract: "Reframing controllable environments as environments that allow agents to exert causal influences over state transitions can circumvent the confounding influence of predictability."
- Humans estimate controllability "by comparing the predictions of an 'actor' model with those of a reduced 'spectator' model". They then arbitrate between the two when predicting.
- "Exposure to inescapable stressors biased controllability estimates downward and increased reliance on the spectator model in an anxiety-dependent fashion." The authors read this as support for a *general* reduction in expected control, not an aversive-specific one.
- The authors explicitly equate the spectator model with Pavlovian learning and the actor model with instrumental learning, which explains Dorfman & Gershman's result.
- TE "requires exploration": with no action variability, H(S'|S) and H(S'|S,A) are both zero and controllability cannot be read.

## Evidence
- Task: 3 states × 3 actions with no reinforcers. Four hidden rules: two controllable (C1, C2; next state set by the action) and two uncontrollable (U1, U2; next state set by the previous state). Transition noise 0.05–0.2, with covert reversals. After 6–7 exploratory trials comes a counterfactual prediction pair (the same state, two actions). Different answers count as "subjectively controllable". Controllability was varied independently of predictability (their Fig. 1d).
- N: behavioural 50, fMRI 32 (3T, multiband TR 0.7 s), stress 54 analysed (27 per yoked group, from 62 recruited).
- Model comparison (pooled over three experiments): SAS'–SS'–Ω beat SAS' alone and two controllability schemes built only on SAS' statistics (conditional entropy H, or Jensen–Shannon divergence between counterfactual actions). It predicted subjective controllability around reversals better than SAS' alone: **72.1% vs 66.5%**, z(49) = 3.90, d = 0.64.
- Decision times: both prediction errors slowed responses (δ_SAS' d = 0.79, δ_SS' d = 0.49), and so did higher ω (d = 0.74). Controllability-related slowing correlated with accuracy across subjects (ρ = 0.67).
- fMRI: mPFC and NAcc encoded δ_SS' − δ_SAS' (= p_SAS' − p_SS') negatively, responding to δ_SAS' and not to δ_SS'. The second-order error δΩ was encoded negatively in PCC, right dorsal anterior insula, right TPJ and mPFC. Subjective controllability was decodable from the precuneus, right TPJ, SMA, left premotor cortex and left dlPFC. Only the right TPJ and dorsal mPFC showed all three effects.
- Stress (yoked active-avoidance shocks before the task):
  - The threshold thres_Ω rose after uncontrollable shock: t(52) = 4.56, **d = 1.1**.
  - Mean ω fell: z = 2.60, **d = 0.77**.
  - Counterfactual predictions were more often identical: z = 1.69, p = .045, one-tailed.
  - Prediction-error slowing shifted toward the spectator model (group × PE interaction F(1,52) = 5.97, η² = 0.07).
  - Accuracy and decision times did not differ (U 0.61 vs C 0.65, p = .43). So this is not a loss of motivation.
  - State anxiety predicted lower ω only after uncontrollable shock (r = −0.46, against r = 0.30 after controllable shock; the difference z = 2.87).
- Confound noted by the authors: only rule C2 allowed state repetition, which served as a salient controllability cue. It was modelled by a "prior injection" λ.

## Formal model (quoted from Methods)
- Actor (SAS'): realized transitions `P(s'|s,a) ← P(s'|s,a) + α(1 − P(s'|s,a))`, unrealized ones `P(s'|s,a) ← P(s'|s,a)(1 − α)`. Prediction error `δ_SAS' = 1 − P(s'|s,a)`.
- Spectator (SS'): the same with `P(s'|s)`, error `δ_SS' = 1 − P(s'|s)`.
- Causality signal: `Ω ← Ω + α_Ω (P(s'|s,a) − P(s'|s) − Ω)`, so the second-order error is `δΩ = δ_SS' − δ_SAS' − Ω`.
- Controllability estimate: `ω = 1/(1 + exp(−β_Ω(Ω − thres_Ω)))`, with thres_Ω ∈ [−1, 1].
- Prediction: `p(S' = i) = ω p(S' = i | S, A) + (1 − ω) p(S' = i | S)`. Report: softmax with β_choice.
- Target quantity (standard identity, not written in the paper): `TE = H(S'|S) − H(S'|S,A) = I(A; S' | S)`, the conditional mutual information between action and next state given the current state. Ω is an online, probability-difference proxy for it, not a log-ratio. The paper says the exact Ω–TE relation is in the Supplementary Notes, which were not read.

## License
Preprint CC-BY-ND 4.0. Journal version is subscription only. Code and task: github.com/romainligneul/NHBcontrollability. Data on the Donders repository (access by ORCID login; not downloaded).

## Runs on this Mac without a GPU?
Yes. It is a few delta-rule updates per step.

## Verdict: adopt (controllability as conditional mutual information between own action and next state, computed by comparing an actor and a spectator predictor)
- Of the three formal accounts, it is the one that separates controllability from predictability. It works without reward, so it applies to any state channel, including the partner's face and voice. It was also shown to shift after uncontrollable stress in humans, with a large effect on the threshold (d = 1.1).
- Limits: Ω is a heuristic running difference, not a Bayes factor (Dorfman & Gershman's L is the principled version). The model fits only prediction trials. The tasks are small and abstract, and the stress groups have 27 people each.

## What it implies for the engine
- **One equation for controllability and agency attribution.** In a world model that predicts the next interoceptive and exteroceptive state, compare three predictors of the next state of any channel X (my body, the partner's face, the room):
  - `p(x'|x)`, the spectator;
  - `p(x'|x, a_self)`, me as cause;
  - `p(x'|x, a_partner)`, the partner as cause.

  `I(a_self; x' | x)` is my controllability over X. `I(a_partner; x' | x, a_self)` is the partner's agency over X. A large drop in a need-relevant variable with high partner-TE and low self-TE is "the other did it, and I could not stop it". This is the appraisal configuration that the appraisal literature says separates anger from sadness (Moors et al. 2013), written without any emotion variable. Whether the behaviour that follows looks like protest or like withdrawal must then come from the core's policy, not from a label.
- **It answers the open problem in the contingency synthesis.** The existing note contingency-causal-synthesis.md says Watson's sufficiency and necessity indices "do not separate 'I follow it' from 'it follows me'". Conditioning on the past state (TE, not MI) is exactly the correction: a mimic that follows me raises `I(a_self; x'|x)`, whereas my following the partner raises `I(a_partner; my_state' | my_state)`. The lag structure decides between them. That synthesis's use of the agent's own logged variation as an instrument is also the "requires exploration" condition here.
- **Exploration is a precondition, not a luxury.** With no action variability, controllability cannot be estimated (their Fig. 1e). A core that becomes passive (Maier & Seligman's default) also stops generating the evidence that would show control. That is a positive-feedback trap that the engine's equations should reproduce, and its curiosity or exploration term should be what breaks it.
- **The stress effect sits on a threshold or prior, not on learning.** Uncontrollable shock shifted thres_Ω (how much causal evidence is needed), not the learning rates or accuracy. In a Bayesian core that is a shift in the prior log-odds L_0, Huys & Dayan's hyperprior over χ, carried across tasks. It agrees with Maier & Seligman's EXPECT as a slow, cross-situational weight.
- **Relation to wanting.** Spectator dominance under low control means cue → state prediction drives behaviour. In a reward setting, that is the Pavlovian (cue-wanting) channel of Dorfman & Gershman.

## Ablations that separate it
1. **Spectator removed (actor only, the paper's SAS' model).** Controllability is no longer estimated, so predictions do not switch at reversals between controllable and uncontrollable rules. Uncontrollable exposure leaves no trace in later prediction. Behaviourally this is the losing model (72.1% vs 66.5% tracking).
2. **TE replaced by MI** (dropping the conditioning on the previous state). Prediction: the engine credits itself with control over partner states that merely co-vary with its actions through a shared driver (the forecaster confound). The same happens with a partner who mimics it (the "it follows me" confound). A yoked-replay test of the partner detects this.
3. **Partner-conditioned predictor removed.** Partner-caused and world-caused losses become the same. That is the ablation the emotion-elements synthesis lists for row 9.
4. **thres_Ω (or L_0) frozen.** Uncontrollable episodes no longer shift later controllability estimates. Learning within a task is intact, but transfer across contexts is lost (the stress effect disappears).
