# Representation learning with contrastive predictive coding (van den Oord, Li & Vinyals)

Citation: A. van den Oord, Y. Li, O. Vinyals. "Representation Learning with Contrastive Predictive Coding." arXiv:1807.03748 (v2, 2019).

Source read: arXiv PDF, text-extracted. Read in full: abstract, sections 1–4 (motivation, architecture, InfoNCE and its MI bound, related work, experiments on LibriSpeech, ImageNet, BookCorpus transfer tasks and DeepMind Lab, conclusion) and Appendix A.1 (the derivation I(x_{t+k}; c_t) ≥ log N − L_N).

## The derivation story (read for the method of discovery)
- **The diagnosis.** Unimodal losses (MSE, cross-entropy) are poor for high-dimensional targets, and generative models "waste capacity at modeling the complex relationships in the data x, often ignoring the context c". Images hold thousands of bits; the shared latent may hold ten.
- **The move: model a ratio, not the data.** Instead of p(x_{t+k} | c_t), learn f_k(x_{t+k}, c_t) ∝ p(x_{t+k} | c_t)/p(x_{t+k}) with a log-bilinear score exp(z_{t+k}ᵀ W_k c_t), one W_k per step k.
- **Why it works (a proof, not a tuning result).** With one positive and N − 1 negatives from the proposal p(x), the cross-entropy of picking the positive (InfoNCE) has its optimum at the density ratio, "independent of the choice of the number of negative samples". At the optimum I(x_{t+k}; c_t) ≥ log N − L_N (Appendix A.1, with an approximation in eq. 8 that "quickly becomes more accurate as N increases").
- **The negatives define what is learned.** Table 2: drawing negatives only from the same sequence (same speaker) or excluding the current sequence changes phone accuracy (64.6 mixed-speaker; 65.5 same speaker; 57.3 mixed speaker excluding the current sequence; 65.2 current sequence only). The representation encodes exactly what tells the positive from the negatives.
- **Prediction horizon sets the time scale.** Predicting 2 steps: 28.5% phone accuracy; 4: 57.6; 8: 63.6; 12: 64.6; 16: 63.8. Far targets force "slow features".

## Evidence with numbers
- LibriSpeech (251 speakers): phone 64.6% (supervised 74.6; MFCC 39.7); speaker 97.4% (supervised 98.5), both by linear probe; one hidden layer raises phone to 72.5%.
- ImageNet linear probe: top-1 48.7% (+9 points over prior best), top-5 73.6%.
- DeepMind Lab: CPC as auxiliary loss helps 4 of 5 tasks; no effect on a purely reactive task.

## What it means for the design
1. **The method is the lesson.** CPC did not add a module; it changed what is compared with what. Its structural fact: a learned critic is forced to encode whatever separates the true future from the chosen negatives, and nothing else.
2. **A self–other objective by choice of negatives (mine, derived).** Let the agent predict *its own* future body and face features from its latent, with negatives that include the *partner's* matched-time future mapped into the agent's own coordinates (and the partner's future at a set of lags). If the agent's future equals the partner's on a channel, the positive and that negative are identical, so for any critic the term is at least log 2 above its floor: a copied channel is the worst case of the objective. Doing the opposite is discriminable and costs nothing. This is the property report 4 said no information measure has ("copying and doing the opposite carry exactly the same information"): the density-ratio critic is not a symmetric information quantity, so it can tell them apart.
3. **Shortcut warning, from the paper's own ablation.** Negatives determine the solution; a critic will use the easiest discriminating feature. A single pooled InfoNCE can be satisfied by one idiosyncratic channel while all others copy. Per-channel heads and lagged partner negatives would be required.
4. **Slow features from horizon.** The step ablation says the horizon set determines the time scale the latent must hold; horizons from frames to minutes would ask for structure across that range, not a tuned decay.

## Verdict
- **adopt (as method and as a candidate objective).** CPC itself is a representation-learning loss, not a core; contrastive learning is not on the excluded list. The derived use (partner futures as negatives) makes copying a maximum of the loss rather than something a ceiling must stop; whether it has prior art was checked with one web search only, which found nothing of the kind, and that is not proof of absence.
