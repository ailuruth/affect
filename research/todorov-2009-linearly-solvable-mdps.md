# Todorov 2009, "Efficient computation of optimal actions" (PNAS 106(28):11478-11483; PMC2705278)

Source read: PMC full-text HTML (open access) in full, main text and figure captions. Display equations on PMC are images; Eqs. 2, 3, 6, 7, 9-13 were read from those images. Not read: the SI Appendix (PMC served a bot-check page instead of the PDF), so derivations the paper defers to it (normalisation of the KL step, the h → 0 limit, the embedding's nondegeneracy condition) are not verified here. Eqs. 1, 4, 5, 8, 14-19 were not viewed as images; the text around them was read.

## Claims
- Control as choosing transition probabilities: "we allow the agent to specify transition probabilities u(x′|x) directly." Cost (Eq. 2): "ℓ(x, u) = q(x) + KL(u(·|x)||p(·|x)) = q(x) + E_{x′∼u(·|x)}[log u(x′|x)/p(x′|x)]", where p is the passive dynamics, "the behavior of the system in the absence of controls". Constraint: "u(x′|x) = 0 whenever p(x′|x) = 0", which also prevents "making state transitions that are physically impossible".
- Desirability (Eq. 3): "z(x) = exp(−v(x))", named because "z is large at states where the cost-to-go v is small". Optimal action (Eq. 6): "u*(x′|x) = p(x′|x)z(x′)/G[z](x)". Linear Bellman equation (Eq. 7): "z(x) = exp(−q(x))G[z](x)"; in matrix form "z = Mz, where M = diag(exp(−q))P".
- Cost: "solving an optimal control problem in our formulation is computationally equivalent to half a step of policy iteration." Results reported: ≈5 times faster than dynamic programming for shortest paths on a 190,914-node graph (ρ = 40); car-on-a-hill "≈10 times faster than policy iteration and 100 times faster than value iteration"; embedding a machine-repair MDP gave "R² ... 0.993" and a policy "0.9% worse than optimal".
- Continuous case (Eqs. 9-13): "dx = a(x)dt + B(x)(u dt + σ dω)", "ℓ(x, u) = q(x) + (1/2σ²)‖u‖²", "u*(x) = −σ²B(x)ᵀvₓ(x)", linear HJB "q(x)z(x) = L[z](x)" with "L[z](x) = a(x)ᵀzₓ(x) + (σ²/2) trace(B(x)B(x)ᵀzₓₓ(x))". The KL divergence between the passive and controlled Gaussians equals the quadratic energy cost over the time step. "the continuous problem is a special case of the discrete problem."
- Average-cost version (Table 1): "exp(q − c)z̃ = G[z̃]", with c "the (unknown) average cost computed as the principal eigenvalue". The discounted case is the one non-linear entry.
- Author's own limits (Discussion): "the controls and the noise must be able to cause the same state transitions ... both the controls and the noise act in the subspace spanned by the columns of B(x). This is a more significant limitation. It prevents us from modeling systems subject to disturbances outside the actuation space." And: "the noise amplitude and the control costs are coupled, and, in particular, the control costs are large when the noise amplitude is small."

## Evidence
Analytical results plus benchmarks on stated problems (internet router graph, machine repair, grid world Z-learning vs Q-learning with 10 repeats, car-on-a-hill). No error bounds for the embedding: "We do not yet have theoretical error bounds".

## License
PNAS open access option ("Freely available online through the PNAS open access option"); PNAS copyright, not a CC licence stated on the page. No code.

## Runs on this Mac without a GPU?
Yes. The discrete solve is one sparse linear system (or power iteration z ← Mz). No code was released or checked.

## Verdict: adopt (discrete form for the engine; continuous form equals Kappen 2005)
- For (a): the KL cost from passive dynamics gives a natural "effort" term; the cost-to-go is −log z, so desirability is a Boltzmann weight. The average-cost form is an eigenproblem with principal eigenvalue c, which fits a homeostatic agent with no terminal state (Principle 6) better than discounting.
- The KL-from-passive cost assumes the agent's "do nothing" dynamics is known and fixed; the engine must say what the passive dynamics of the body is.
- The author states the noise-cost coupling as a limitation; any affect claim resting on it (for example, "more noise makes action cheaper") is a property of this problem class, not a finding.
