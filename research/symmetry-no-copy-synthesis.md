# Copy forbidden by symmetry, not by tuning (synthesis)

Reading round on structures in which "self copies partner" is impossible or unstable for every parameter value. Written 2026-11-26; revised the same day after the primary texts became reachable.

## Sources

**Read:**
- Nijholt, Rink & Sanders 2014: §§1–4 in full.
- Pecora et al. 2014: main text and Methods.
- Hansen & Ghrist 2020/21: in full.
- Chang et al. 2019: main text and Appendix B.
- Haber & Ruthotto 2017: §§3–4.
- Abrams & Strogatz 2004: in full.

**Not read, claims unverified, nothing here relies on them:**
- Golubitsky & Stewart 2006: ams.org unreachable, no arXiv copy.
- Golubitsky & Stewart 2002: a book.
- Pecora & Carroll 1998: paywalled.

**Own derivations and checks.** Statements marked **[own]** are mine. Each is proved here or checked in `foundations/sims/symmetry-no-copy/checks.py`. Run C1–C7 with `python3 -I checks.py`; numpy and scipy are needed.

Shi, Altafini & Baras 2019 was already read for `altafini-2013-signed-consensus.md` and was not redone.

## What fails, and why it is instructive

| Route | What the source proves | Why it fails for the open dyad |
|---|---|---|
| Copy is not a robust synchrony (Nijholt et al. Thm 4.1: robust ⇔ balanced) | invariance "for all choices of response functions" | Self and an exogenous partner have different input sets, so copy is never a balanced (robust) synchrony **[own]**. That makes it non-invariant, not non-attracting. High-gain tracking approaches it (C1). |
| Symmetry decides which clusters exist (Pecora et al.) | IRR block form; clusters "can be" synchronous | Whether they attract is a Lyapunov question that changes with parameters. The paper's own clusters desynchronise as the feedback β varies. |
| Conserving or skew coupling (Chang; Haber & Ruthotto) | closed-system Jacobian has imaginary spectrum, "stable regardless of the spectrum or size of K" | **[own]** With the input inside tanh, copy is a centre, never attracting (final distance 0.74), but the orbit's time-average is copy (0.008), and any γ > 0 makes copy attract (C7). Error-driven skew coupling tracks (C1). Rotation acts as delay (C2: 0.895 at zero lag). Two skew stages give the identity (C3). |
| Sheaf obstruction (Hansen & Ghrist) | no global sections ⇒ "the only stable opinions will be everywhere zero" | An obstruction gives flat, not strong coupling. Antagonistic edges give an indefinite Laplacian and instability (Prop. 12.1). **Learning the restriction maps converges to "the nearest sheaf such that x is a global section" (Thm 8.1): learned maps drift to copy-in-a-frame.** |
| Chimera (Abrams & Strogatz) | partial locking among identical oscillators | "it occurs even if the uniform state is stable": bistable with full synchrony. |
| Feedforward / nilpotent wiring (Nijholt et al. network A is triangular) | – | **[own]** Exact copy is impossible, but approximate copy returns at large weights: defect 0.22 → 0.0001 as the norm grows from 2 to 100 (C4b). |

**The common lesson [own].** A no-copy property survives indirect routes only if the class of maps it holds for is closed under:
- sums (parallel routes);
- products (series routes);
- feedback (loops);
- learning (parameter updates);
- time.

Skew maps are closed under sums but not products. Orthogonal groups are closed under products but not sums. Nilpotent maps are closed under all of these, but only for exact copy. Hansen & Ghrist's Theorem 8.1 shows the last item concretely: an *unconstrained* learning rule on expression maps actively finds copy-in-a-frame.

## The strongest route: twisted equivariance through one gate

**The class.** The class closed under everything above is the **maps that commute with a group action**, the G-equivariant maps. Sums, products, inverses $(I-A)^{-1}$ and limits of commuting maps all commute. Nijholt et al. show that network structure is itself equivariance under a semigroupoid ("network systems are examples of equivariant dynamical systems", Thm 1.1). Pecora et al. give the decomposition of any commuting matrix: a direct sum $\bigoplus_l I_{d^{(l)}}\otimes C^l$ over the group's irreducible representations, computed by the character projections $P^{(l)}=\frac{d^{(l)}}{h}\sum_K\alpha^{(l)}_K\sum_{g\in K}R_g$.

**Constraint (A) [own].**
- The partner's face and voice enter at exactly one gate $Q$. Let the partner's percept carry the representation $\pi$. Let the agent's face carry $\rho$, which equals $\chi\pi$ on a set of "twisted" components $W$, where $\chi$ is a sign character ($\chi(g)=-1$).
- $Q$ is also invariant under scaling of the percept by $\lambda>0$. The partner supplies *which* expression; the agent's own body supplies *how much*.
- Every downstream module commutes with the action by construction, through weight-tying: state, memory and replay, learning updates, the inversion model and face output.
- No module sees the raw percept, and no loss puts the partner's raw face on the agent's output.

(A) contains no numerical constant. It is a typing rule.

**Theorem sketch [own].** Under (A), for every parameter, learned weight, coupling strength and route, write $e(u)=x(u)-cu$ for the copy error at scale $c>0$.

1. **No exact copy.** For any $c,\lambda>0$:
   $$\max(\|e(u)\|,\|e(\lambda u)\|)\ \ge\ \tfrac c2|1-\lambda|\,\|u\| .$$
   Proof: $x(\lambda u)=x(u)$, because invariance is inherited by every function of the gate's output, plus the triangle inequality.
2. **No copy at any scale on twisted components.** For $g$ with $\chi(g)=-1$:
   $$\|e(u)\|+\|e(gu)\|\ \ge\ 2c\|u_W\| .$$
   Proof: $e(gu)=-2c\,\pi(g)u-\pi(g)e(u)$, and $\pi$ is orthogonal. Check C6: over 2,000 random equivariant networks with weight scales from 0.1 to 100, the minimum normalised value was 1.0009, against the bound 1. Twisted intertwiners are also traceless, so the Liouville trace corollary in the Pecora 2014 note applies.
3. **Closure.** Statements 1 and 2 survive any composition, sum, feedback interconnection and tied learning update. This answers the recurring failure directly: no indirect route exists, because no non-equivariant map exists for a route to use.
4. **Sharpness (Schur no-go).** On components where $\pi$ and $\rho$ contain the same irreducible, the block $C^l$ is free, and it includes the identity. No equivariant class can exclude $cI$ on those components while allowing same-feature drive there. On them, copy can be excluded only up to scale (statement 1), or by dynamics (a phasic, zero-DC route), or by a cap.
5. **Caveat: time.** A rotation acts as a delay for signals in quadrature (C2). The copy test must be run at all lags, and $G$ must not contain time shifts. The H/K-theorem framing of this point came from an unread source and is not relied on.
6. **Caveat: invariance is not attraction.** Pecora et al. show that symmetry decides which synchronies exist, while stability is parameter-dependent. Statements 1–2 escape this because they are **impossibility** results about the response map, holding at every point, not stability results about a manifold. That is why the route goes through a typed response map, not through a synchrony subspace.

**What stays strong.** The free blocks $C^l$ are large learned matrices on each matching component. Sign flips are intertwiners. The partner's influence on which expression appears needs no gain cap.

## Where it conflicts with Principle 3

1. **Mimicry clause.** Same-feature positive drive is a non-zero identity block on a matching component. By the block form (statement 4), symmetry cannot forbid copy there. The best this route gives on those channels:
   - exact copy is impossible;
   - a **scaled copy at the agent's own amplitude** remains, which the partner cannot move.

   The critiques' metric minimises over the scale $c$ and would flag this. **The operator must decide** whether "the partner sets which expression, the agent's body sets how much" meets D78 on the mimicry channels. Otherwise those channels must be phasic with an innate amplitude, which is a ceiling.
2. **Inversion clause.** Under (A), the inversion model sees only the gate's invariant features. It infers *what kind* of state the partner is in, not its intensity, and nothing sign-sensitive on twisted components. A magnitude-aware module with any path to the face breaks closure (statement 3), and Hansen & Ghrist's Theorem 8.1 shows what learning then does: it finds the maps that make the current state look like agreement. **The guarantee is all-or-nothing.**

**Choosing $G$ is the open design problem.** Candidates and their costs:
- **Scaling ($\mathbb R_{>0}$).** Cheap and meaningful. Face and voice must be scaled jointly, or voice loudness leaks the magnitude back in.
- **Left–right mirror with a sign twist.** Lateral channels only.
- **Sign of the partner's deviation, twisted.** Strong, but those channels then respond only to how much the partner moved, not which way.

A design picks $G$ from what the agent must *not* be able to distinguish. It proves statements 1–4 for that $G$, and writes the Principle 5 ablation: break the weight-tying and copy returns on $W$.
