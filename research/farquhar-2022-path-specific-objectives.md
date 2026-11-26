# Path-specific objectives for safer agent incentives (Farquhar, Carey & Everitt)

Sebastian Farquhar, Ryan Carey & Tom Everitt, *AAAI 2022*, arXiv:2204.10018v1 (21 Apr 2022). https://arxiv.org/abs/2204.10018

## What was read
The arXiv PDF, in full: sections 1–9 (delicate state, the CID background, the general delicate MDP, path-specific objectives with Proposition 1 and the identifiability caveat, the three estimators in Table 1, unification with earlier work in Table 2, both experiments, discussion and limitations). There are no appendices. Figures 2–5 were read as extracted text, not seen. The design document (§10, table of sources) listed this paper as "not read, named only as pointers". This note is that reading.

## The computation, precisely

**Delicate state.** The state is factored into a robust part s and a delicate part z. Z is delicate when it is *subtle* ("Hard to specify a reward for"; five cases: not ordered, vague, unenforceable, illegal, structural) and *manipulable* ("Vulnerable to motivated action — intentional actions can have bad outcomes"). The method is safe only if z is also *stable*: "Robust against unmotivated action — side-effects are unlikely to be bad."

**ICI criterion (restated from Everitt et al. 2021a, Theorem E18).** "A single-decision CID G admits an ICI over X ∈ V iff G has a directed path from A to U via X."

**The objective (Definition 5.1, Proposition 1).** Evaluate each action by Pearl's path-specific effect along an edge-subgraph G′ that removes the arrows A_t′ → Z_t′+1 and S_t′ → Z_t′+1 for t′ ≥ t. Up to a constant, the PSO is

U^{G′,ā}_{π,a} = U_{π, Z_ā, a},

"the potential response of the utility under π, a, and Z_ā (the nested counterfactual Z under ā)". In words: "computing the return normally, except for imputing a 'natural' distribution to the delicate states, Z, that matches what would have happened on the default action, ā."

**Three ways to estimate the natural distribution (Table 1).**
- Policy baseline: z̄ ∼ p_π̄(Z_t+n | s_t, z_t) under a fixed, trusted default policy π̄. "The most principled solution".
- State baseline: z̄ ∼ p̂(z_t+n | z_t, s_t), a rule for how z evolves by itself.
- Fixed state: z̄ = z_t.
- Two rules: "z̄ must not depend on any descendent of A0 (this would induce an ICI over Z)" and "the intervention must not depend on the current policy". Setting z̄ from the real dynamics recovers the ordinary objective.

**What the agent still does.** It responds to z; it just does not try to move it. "An agent optimizing a PSO will not take opportunities to change the delicate state, but will act in a way that is responsive to externally-caused changes to the delicate state." And: "such a policy may still systematically affect Z as a side-effect of acting towards some other objective."

**Identifiability.** Path-specific effects are, except for one-step effects, "not identifiable from experiments" (Avin, Shpitser & Pearl 2005). They are identifiable "with further assumptions like counterfactual independence which can be assumed in simulated environments", so the PSO is computed inside a model, not estimated from logged data.

## Evidence with numbers
- **Barging gridworld.** The person is on the path (delicate). Actions: long way L (reward 1), short way S (10 if the path is clear, else nothing), barge B (pushes the person into the river).
  - Standard agent: B then S, E[U] = 10, oracle return −1.
  - Deterministic PSO agent: L, E[U] = 1, oracle 1.
  - ε-greedy PSO agent (ε = 0.1): E[U] 1.43, oracle 0.9. If it barges by accident, it then uses the short path: "responsive to changes in its environment, but will not deliberately use the delicate state as a means to an end."
- **Content recommendation** (Krueger et al. 2020 simulator): K = 10 user types, M = 10 article types, 20 environments, 2000 steps, 100 seeds. User preferences W are delicate; loyalty g is robust.
  - All three PSO variants reduce preference drift, the policy baseline (uniform random π̄) slightly more than the others, "without meaningful harm to accuracy" and without changing loyalty drift. Cost: under 15% extra training time.
  - Even a random policy drifts preferences: "This environment is not stable... removing the control incentive is not enough to ensure safety."

## Stated limits
Graph discovery ("unclear how to carve up reality"), causal estimation, **observation of the delicate state ("For psychological state, like beliefs, this can be hard")**, and the moral choice of what counts as delicate. Proving stability is "contingent, empirical, and a matter of degree."

## License
arXiv non-exclusive distribution licence (not CC). No code released with the paper.

## Verdict
**adopt (as the formal rule for Principle 6), with one correction to how the designs use it.** The paper gives the exact operation the designs need: evaluate returns with the delicate node held at its natural value under a fixed baseline. It also states the price: the agent then has no incentive to improve that node at all. If the *whole* partner is delicate, care cannot learn to help, which is the critic's point.

## What it means for the designs
1. **Make the display delicate, not the partner.** Revision 2 cuts every path from the agent's acts through the partner (the action-blind partner head). In Farquhar's terms that treats the partner's whole state as Z, so care has no instrumental incentive on the partner's welfare. It can only learn "comfort as I would be comforted" (R), never "what helps *this* person". Split the partner node into need N (robust: we want it improved), display F (face, voice prosody, smile; delicate: subtle, manipulable by contagion, mimicry and politeness), and report-and-choice K (words about their situation, what they do next). Cut the edges A → F and A → N → F *in the credit computation only*; keep A → N → K.
2. **Estimator.** In each 𝓜 rollout, replace the partner's display by its policy-baseline value: the display the partner would show if the agent had taken the default act ā (for example "a neutral acknowledgement turn"), predicted by the existing action-blind head. That head already *is* a fixed-baseline estimator of F. Revision 2 used it for the whole partner. The proposal is to use it only for F.
3. **This is also the K3 fix in one rule.** K3 leaked because head (i), the agent's own body, learned act → partner face → own C. Under the PSO, every partner-driven body variable (C, V, the partner part of A) is computed in rollouts from b̂_p whose face inputs are the imputed z̄. Head (i) can still learn anything else. Falsifier F4 becomes a direct test: at equal R, P(choice) must not depend on the predicted *display* change. It may depend on the predicted change in need inferred from K.
4. **Response yes, control no.** The face still triggers concern: C = 𝒟(b̂_p), with b̂_p read from the real face. That is a response incentive, which the paper keeps ("responsive to externally-caused changes"). Principle 6, "the face is evidence, never a target", is exactly "response incentive on F allowed, instrumental control incentive on F removed". No conflict.
5. **Stability is the open risk, and it is real here.** Human faces mimic. The agent's own smile moves the partner's face as a side effect (the paper's "unmotivated action"). The PSO removes the incentive but not the effect, so the design must still bound the agent's expressive gain toward the partner (the existing cone and ceiling). The paper's recommender result is the warning: no incentive, drift anyway.
6. **Identifiability.** N has paths both to F (cut) and to K (kept). That is exactly the Avin–Shpitser–Pearl non-identifiable case, so the cut must be computed in 𝓜 under a stated counterfactual-independence assumption (display noise independent of report noise given N). Write that assumption into the design and test it with an ablation: shuffle display–report pairings in replay; credit must not change.
