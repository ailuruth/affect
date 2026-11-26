# Copy forbidden by symmetry, not by tuning (synthesis)

Reading round on structures where self-copies-partner is impossible or unstable for every parameter value. Written 2026-11-26.

**A caveat on sources.** This session's network allowlist blocked arxiv.org and ams.org, so **no primary text was read**. Each note says so and is written from prior knowledge, with search snippets used only to confirm bibliography and headline claims. The mathematical claims this synthesis relies on are proved here or checked numerically in `foundations/sims/symmetry-no-copy/checks.py` (C1–C6, numpy/scipy, run with `python3 -I checks.py`).

**Notes.**
- `golubitsky-2006-groupoid-network-synchrony.md` (watch)
- `golubitsky-2002-symmetry-perspective.md` (adopt)
- `pecora-1998-master-stability-function.md` (watch)
- `hansen-2021-discourse-sheaves.md` (watch)
- `chang-2019-antisymmetricrnn.md` (reject)
- `abrams-2004-chimera-states.md` (reject)

Shi, Altafini & Baras 2019 was already read for `altafini-2013-signed-consensus.md` and was not redone.

## What failed, and why it is instructive

| Route | Result | Why it fails for the open dyad |
|---|---|---|
| Copy not invariant: an unbalanced colouring (Golubitsky–Stewart) | true | Not invariant does not mean not approached. High-gain tracking gets arbitrarily close. |
| Copy transversally unstable (MSF trace) | true for traceless coupling **if** $\langle\mathrm{tr}\,DF\rangle\ge0$ | A resting agent contracts: 191 of 20,000 random traceless couplings made copy stable once $\mathrm{tr}\,A<0$ (C5). |
| Conserving or skew coupling (AntisymmetricRNN, Hamiltonian) | no attractors when closed | With an exogenous partner, error-driven skew coupling tracks, with DC transfer approaching $I$ (C1). Rotation equals delay for quadrature signals (zero-lag copy correlation 0.895, C2). Two skew stages compose to the identity, $JJ^\top=I$ (C3). |
| Sheaf obstruction (holonomy on a cycle) | no global section | Under diffusion the frustrated subspace decays to flat (Altafini), so coupling is not strong. With one edge there is no holonomy. |
| Feedforward / nilpotent wiring | exact copy impossible (all eigenvalues 0) | Approximate copy returns at large norm: defect 0.22, 0.04, 0.0025, 0.0001 at $\|N\|$ = 2, 5, 20, 100 (C4b). A cap again. |
| Chimera | partial sync | Bistable with full sync. Copy is avoided by history, not forbidden. |

The common lesson matches the recurring failure in the designs. **A no-copy property survives only if the class of maps it holds for is closed under every way routes combine:** sums (parallel routes), products (series routes), feedback (loops), limits (learning) and time. Skew maps are closed under sums but not products. Groups are closed under products but not sums. Nilpotent maps are closed under all of these, but only for exact copy.

## The strongest route: twisted equivariance through one gate

**The class.** The class closed under all of the above is the set of **$G$-equivariant maps** for a compact group $G$. Define the twisted part of the agent's face as the isotypic components $W$ where the agent's face carries $\rho=\chi\pi$, with a character $\chi(g)=-1$, while the partner's percept carries $\pi$. The identity is not an intertwiner on $W$. Add the multiplicative group $\mathbb R_{>0}$ acting by scaling on the partner's percept and trivially inside the agent. This is a projective gate: the partner supplies *which* expression, and the agent's own body supplies *how much*.

**Architectural constraint (A).**
- The partner's face and voice enter the agent at exactly one place, a gate $Q$ that is equivariant for $G$ and invariant for $\mathbb R_{>0}$.
- Every downstream module is $G$-equivariant by construction (weight-tying, as in a G-CNN): state, memory and replay, learning updates, the inversion model, Claude coupling and face output.
- No module receives the raw percept, and no loss puts the partner's raw face on the agent's output.

No numerical constant appears in (A). It is a typing rule.

**Theorem (sketch of what a design would prove).** Under (A), for every parameter value, every learned weight, every coupling strength and every route:

1. **No exact copy.** For any $c>0$, any partner face $u$ and any $\lambda>0$:
   $$\max\big(\|x(u)-cu\|,\ \|x(\lambda u)-c\lambda u\|\big)\ \ge\ \tfrac{c}{2}|1-\lambda|\,\|u\|.$$
   Proof: $x(\lambda u)=x(u)$, by invariance inherited downstream, plus the triangle inequality. The partner cannot push harder to push further, because the information needed to copy intensity is destroyed at the gate, and no function downstream can recover it (data processing).
2. **No copy at any scale on twisted components.** For $g$ with $\chi(g)=-1$ on $W$ and all $c>0$:
   $$\|e(u)\|+\|e(gu)\|\ \ge\ 2c\,\|u_W\|,\qquad e(u)=x(u)-cu .$$
   Proof in `golubitsky-2002-symmetry-perspective.md`. Check C6 found a minimum of 1.0009 against the bound 1 over 2,000 random equivariant networks with weight scales from 0.1 to 100. The linear part is a twisted intertwiner, so it is traceless, and the MSF trace corollary applies as well.
3. **Closure.** Statements 1 and 2 hold for any composition, sum or feedback interconnection of modules satisfying (A). They also hold under any learning rule whose updates keep the weight-tying, for example gradients of any loss with respect to tied parameters. This answers the recurring failure directly: there is no indirect route, because there is no non-equivariant map anywhere for a route to use.
4. **Sharpness (Schur no-go).** On components where $\pi\cong\rho$ (call them the mimic components $M$), the commutant contains $I$. No symmetry class can exclude $cI$ on $M$ while allowing any non-zero same-feature drive there. On $M$, copy can be excluded only up to scale (by statement 1) or by dynamics (a phasic, zero-DC route). It cannot be excluded by symmetry.
5. **The lag caveat.** If $G$ contains time shifts, or the partner's channels have quadrature orbits, a twist can be realised as a delay (H/K theorem; C2). The theorem's copy test must be run at all lags, and $G$ must not contain time shifts.

**What stays strong.**
- $\mathrm{Hom}_G(\pi,\chi\pi)$ is a large learned space. Per-channel signed maps are allowed, including $-I$-type sign flips, which are intertwiners on any component.
- Magnitude comes from the agent's own satiable drives.
- The partner's influence on which expression appears is unbounded in the sense that matters: any learned equivariant map, with no gain cap.

## Where it conflicts with Principle 3

Principle 3 has two clauses, and the route costs something on each.

1. **"Perceived features drive the agent's own motor pathways" (mimicry).** Same-feature positive drive is a non-zero multiple of $I$ on its component, so by Schur it lives on $M$, where symmetry cannot forbid copy. The best this route offers there:
   - exact copy is impossible (statement 1);
   - **scaled copy at the agent's own amplitude** remains.

   The critiques' copy metric minimises over the scale $c$, so it would flag this. **The operator must decide** whether "the partner sets which expression, the agent's body sets how much, and the partner cannot move how much" meets D78 on the mimic channels. If not, the mimic channels must be phasic (zero DC), as in partner-regulator revision 3, with an innate amplitude, which is a ceiling.
2. **"The agent infers another's state by inverting its own generative mapping" (inversion).** Under (A) the inversion model sees only the gate's invariant features, so it can infer *what kind* of state the partner is in, but not *how intense*, and nothing on twisted components in a sign-sensitive way. Letting any module see the partner's magnitude while keeping a path to the face breaks closure (statement 3) and reopens exactly the indirect route that sank every design. **The guarantee is all-or-nothing.** If a magnitude-aware partner model is wanted, its only admissible outputs are ones that cannot reach the face: for example, a write-only channel to Claude's text, whose effect returns as a new percept through the gate.

**Choosing $G$ is the open design problem.** Candidates and their costs:
- **Scale ($\mathbb R_{>0}$).** The self owns intensity. Cheap and meaningful. Voice loudness and face intensity must scale jointly, or loudness leaks the magnitude back in.
- **Left–right mirror with a sign twist.** Meaningful only for lateral channels; it gives the "symmetric in, asymmetric out" behaviour.
- **Sign of the partner's deviation, twisted on non-mimic channels.** Strong, but those channels can then respond only to how much the partner moved, not which way.

A design built on this route should pick $G$ from what the agent must *not* be able to distinguish. It then proves statements 1–5 for that $G$, and states the lost information as an ablation prediction (Principle 5): break the tying and copy returns on $W$.
