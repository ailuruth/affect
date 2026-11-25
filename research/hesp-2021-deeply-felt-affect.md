# Hesp et al. 2021: Deeply Felt Affect (valence in deep active inference)

Source read: Neural Computation 33(2), doi:10.1162/neco_a_01341, author PDF from UCL Discovery (sections 3.1.4-4, 5.4, 5.6). Code read: `spm_MDP_VB_X_emof.m` in github.com/CasperHesp/deeplyfeltaffect (precision update and valence evidence blocks).

## Claims
- Valence is inferred, not given: an agent infers a valence state from changes in the expected precision `gamma` of its action model ("subjective fitness").
- The update term for that precision is "affective charge" (AC). It is positive when evidence favours the agent's action model and negative otherwise. The authors relate it to a reward prediction error.
- A slower second level holds valence states that set the prior on precision for the level below ("parametric depth"). Positive valence means more reliance on expected free energy; negative valence means falling back on the habit prior `E`.

## Evidence
- One synthetic rat, T-maze, 64 trials, reward moves from left to right at trial 33. Preferences: reward e^4:1 over "none", shock e^-6:1. Valence states +/- set the rate beta = (0.5, 2.0), so gamma ranges over [0.5, 2.0]. Level-2 transitions: P(- to +) = 0.3, P(+ to -) = 0.2 (a built-in positivity bias).
- Results: valence becomes positive around trial 12; the rat skips the cue around trial 16; after reversal it returns to positive about 15 trials later and takes the shortcut after 22.
- Lesion (higher level removed): the rat keeps going to the old arm for 3 shocked trials (versus 1 with the intact model), then avoids both arms for 8 trials. It cannot habituate: AC is re-elicited every trial because precision resets.
- One deterministic agent and one task. No sweep over parameters and no statistics.

## Equations worth copying
- Policy prior and posterior: `pi_prior = softmax(-E - gamma*G)`, `pi_post = softmax(-E - gamma*G - F)`.
- Code form (SPM sign: `Q = -G`): `eg = (pi_post - pi_prior)' * Q`; `dFdg = qbeta - beta + eg`; `qbeta -= dFdg/2`; `gamma = 1/qbeta`. At the fixed point, `qbeta = beta - AC` with `AC = eg`.
- Paper eq. 3.2-3.3: `dbeta/dt = beta - AC - beta_bar`, so the precision swing is proportional to AC.
- Evidence for valence state k (Bayesian model reduction): `-ln[ ((beta_k - AC)/beta_k) * (beta/(beta - AC)) ]`, added to the level-2 log prior `ln(B s_{T-1})` and passed through a softmax. Zero AC means no change.
- Caveat: the sign of AC is written as `(pi - pi_bar)·G` in Table 4 and as `(pi_bar - pi)·G` in section 3.3.3. Follow the code. The code also floors posterior rates at 0.03 and sharpens the valence evidence with `exp(-40*...)`. Neither constant appears in the paper.

## License
- Paper: CC BY 4.0.
- Code repo: no license file, so all rights are reserved by default. It is adapted from SPM12 (github spm/spm is GPL-2.0). Reimplement from the paper rather than copying.

## Runs on this Mac without a GPU?
Yes in principle: small discrete MDP in MATLAB with SPM12, CPU only. Not run.

## Verdict: adopt (the AC readout only)
AC is a readout computed from what the agent already does: it compares its policy confidence before and after evidence. Nothing names or sets valence, which is what Principle 2 asks. Do not adopt the discrete +/- valence states; they are a hand-named variable. The lesion result is already in the form Principle 5 needs: remove the slow level and you lose recency and habituation.

## What it gives S1
- A valence readout for the Bot. Let `pi` be the Bot's distribution over reply strategies or actions from `pi_theta(h)`. Score them with a G-like term, the predicted drift of body variables `b` from setpoint. Then `AC_t = (pi_post - pi_prior)·(-G)` after each user turn, or each silence tick. Log the AC history as the valence readout and never feed back a named label.
- Coupling `h` to confidence. A slow component of `h` sets `beta`, and so `gamma`. During a long silence the Bot's predictions about the user keep failing, AC goes negative and `gamma` falls, so on return the Bot leans on habit `E` (cautious, default greetings) rather than its user model. Repeated good reunions push `beta` back toward high precision.
- Ablation prediction for S1, in Hesp's own terms: remove the slow level and the Bot (a) does not get more cautious after a long silence, and (b) shows the same size of reaction at every reunion, with no habituation.
- Failure mode: a positivity bias was built into the level-2 transitions (0.3 vs 0.2). Any such asymmetry in S1 should be a stated, ablatable parameter.
