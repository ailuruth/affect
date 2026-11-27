# Action and Perception as Divergence Minimization (Hafner, Ortega, Ba, Parr, Friston & Heess)

Citation: D. Hafner, P. A. Ortega, J. Ba, T. Parr, K. Friston, N. Heess. "Action and Perception as Divergence Minimization." arXiv:2009.01791 (v3, 13 Feb 2022).

Source read: arXiv PDF, text-extracted. Read in full: abstract, §1 (introduction), §2 (framework: joint KL, information bounds, models as preferences, past and future), §3 (unifying review: variational inference, amortized inference, future inputs, control, maximum-entropy RL, empowerment, skill discovery, information gain), §4 (related work) and §5 (conclusion). **Not read:** Appendix A (detailed comparison with active inference), B (KL as preference plus entropy) and C (background). The paper states it "includes no empirical study".

## Key claims
- **One objective.** Action and perception jointly minimise APD(φ) = KL[p_φ(x, z) ‖ τ(x, z)] (Eq. 2): x all inputs, z all latents (representations, parameters, actions, skills), p_φ the actual distribution the agent can shape, τ a target that is both the agent's model and its preferences (can be unnormalised).
- **Two decompositions** (Eqs. 3, 4): joint KL = latent (or input) preference KL − a variational bound on I(x; z). With an expressive target, minimising it maximises mutual information between inputs and latents.
- **Past/future split** (Eq. 6), the paper's main decomposition:
  KL ≤ E KL[p(z | x<) ‖ τ(z)] − E[ln τ(x< | z) − ln p(x<)]  (representation learning on the past)
     + E KL[p(x> | x<, z) ‖ τ(x> | x<)] − E[ln τ(z | x) − ln p(z | x<)]  (control toward preferred future inputs; information gain and empowerment).
  "Because past actions and skills are realized, their mutual information with realized past inputs is constant and thus contributes no past objective terms."
- **Table 1 (the lattice):** actions with factorised target → action entropy (A3C, SQL, SAC); actions with expressive target → empowerment; skills → skill discovery (VIC, DIAYN, VALOR); latent states → representation learning + information gain; parameters → model learning + information gain (VIME, MAX, Plan2Explore).
- **Input density exploration** (Eq. 15): with no latents, KL control = expected log preference + input entropy; pseudo-counts, RND and ICM are estimators of this entropy term. Expected-reward RL puts the controlled dynamics into the target and cancels the curiosity term.
- **Niche seeking.** The marginal τ(x) is the agent's preferred input distribution; the agent "converges to a natural equilibrium or niche … where it sees inputs proportionally to how well it can learn to understand them, while avoiding inputs that are inherently unpredictable given its model class". Surprise minimisation is the special case of constant input entropy; the information-gain terms prevent the dark-room collapse.
- **Against active inference** (in text): divergence minimisation matches the input distribution where active inference maximises its probability (smaller niches in heteroskedastic environments); active inference optimises exploration only with respect to actions and needs a specific action prior.
- **Recipe:** "When introducing new agent objectives, we recommend deriving them from the joint KL by choosing a latent structure and target."

## What it means for the engine
1. **This is the reduction test for any new objective.** Any objective of the form "a latent structure plus a target over inputs and latents" is an APD instance. A pass-7 candidate is new only if it cannot be written as a choice of z and τ, or if the choice itself contains a mechanism APD's review lacks.
2. **The approval route lives only in the future terms.** The past terms (ELBO, contrastive bounds) shape what the latent holds and never select actions. The future terms (preferred inputs τ(x>), information gain, empowerment, skills) are what train behaviour. So whether a partner's reaction becomes a training signal for the agent's expression is decided entirely by whether the partner's future inputs appear in the future terms, and with what target. This is the structural fact the pass-7 synthesis builds on.
3. **Niche seeking selects partners and partner states.** If partner inputs are in x>, the agent is driven toward partner behaviour its model class can predict well and away from unpredictable partners. A partner who mirrors the agent is the most predictable input there is. That is a selection pressure toward being mirrored, by preference matching rather than reward, and it is a copy-adjacent attractor of the dyad.
4. **Representations follow from what is predicted** (as in CPC and CW-VAE notes): the past terms are where affect-like structure can emerge without touching behaviour.

## Verdict
- **adopt (as the reduction lattice and the past/future split), reject as core.** It is a framework, by its authors' description, and it absorbs active inference, KL control, empowerment and curiosity under one KL.
