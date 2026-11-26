# Nonlinear dynamics of networks: the groupoid formalism (Golubitsky & Stewart)

Martin Golubitsky & Ian Stewart, "Nonlinear dynamics of networks: the groupoid formalism", *Bulletin of the American Mathematical Society* 43(3):305–364, 2006. The synchrony theorem it surveys is from I. Stewart, M. Golubitsky & M. Pivato, "Symmetry groupoids and patterns of synchrony in coupled cell networks", *SIAM J. Applied Dynamical Systems* 2(4):609–646, 2003.

## What was read

**The primary text was not read in this session.** ams.org (and arxiv.org) are not on this cloud session's network allowlist; fetches failed at DNS. A web search confirmed the bibliographic details and the headline theorem as stated by secondary summaries ("a set of cells can be robustly synchronous if and only if the cells are in the same equivalence class of some balanced equivalence relation"; "for networks of finite type, the flow-invariant polydiagonals are precisely those that correspond to balanced equivalence relations"; robust synchronous dynamics lives on quotient networks). Everything else below is my prior knowledge of the framework, stated as standard definitions. The checks I ran are in `foundations/sims/symmetry-no-copy/checks.py`. Do not cite this note for anything beyond the balanced-colouring theorem and the definitions.

## The computation, precisely

**Coupled cell network.** A finite set of cells $C$, each with a cell type, and arrows $E$, each with an arrow type and a head and a tail. The *input set* $I(c)$ is the set of arrows whose head is $c$. Cells $c,d$ are *input-equivalent* if there is a type-preserving bijection $\beta: I(c)\to I(d)$. Each cell has a phase space $P_c$ (equal for cells of the same type). An *admissible vector field* has the form
$$\dot x_c = f_c\big(x_c,\; x_{T(I(c))}\big),$$
where $f_c$ depends only on the cell's own state and the states at the tails of its input arrows. It is the same function $f$ for input-equivalent cells, up to permuting inputs by $\beta$, and is symmetric in inputs whose arrows have the same type. The set of input bijections forms the **symmetry groupoid**, which is more general than the automorphism group: two cells can be forced to behave alike without any global symmetry of the network.

**Polydiagonal.** For an equivalence relation $\bowtie$ on cells, $\Delta_{\bowtie} = \{x : x_c = x_d \text{ whenever } c\bowtie d\}$. These are the candidate synchrony subspaces.

**Balanced.** $\bowtie$ is *balanced* if whenever $c\bowtie d$ there is an input isomorphism $\beta: I(c)\to I(d)$ such that the tail of every arrow $i$ is $\bowtie$-equivalent to the tail of $\beta(i)$. In other words, synchronised cells receive inputs of the same types from synchronised clusters.

**Theorem (Stewart–Golubitsky–Pivato 2003).** $\Delta_{\bowtie}$ is flow-invariant for *every* admissible vector field if and only if $\bowtie$ is balanced. The restriction of the dynamics to $\Delta_{\bowtie}$ is an admissible vector field on the *quotient network*.

**Consequences.**
- A synchrony pattern that is not balanced is not invariant for generic admissible dynamics. It can occur only by tuning, never "robustly".
- Network symmetry (automorphisms) gives fixed-point subspaces $\mathrm{Fix}(\Sigma)$, which are always balanced. But balanced colourings exist without any symmetry. The groupoid is the right object, not the group.
- *Feedforward* networks (no directed cycles; nilpotent adjacency) are a special class in the same programme, known for anomalous growth rates at synchrony-breaking bifurcations. I state this from memory only.

## What it means for the designs

**The dyad as a network.** Take two cells, self $S$ and partner $P$, with $P$ exogenous (no arrow $S\to P$ inside the agent). Then $S$ and $P$ are not input-equivalent: $S$ has an input from $P$, and $P$ has no matching input. So the copy relation $S\bowtie P$ is **not balanced**, and the copy diagonal $\{x_S=x_P\}$ is not robustly invariant.

This is a true structural statement, but it is too weak for the design question.
1. Non-invariance does not stop the copy diagonal being *approached*. High-gain tracking keeps $x_S$ within $\varepsilon$ of $x_P$ without the diagonal being invariant. The critiques' copy defect is a distance, not an invariance.
2. With the partner exogenous, $x_S\equiv x_P$ is not a solution anyway unless the partner happens to obey the agent's own dynamics. The balanced-colouring theorem therefore gives nothing a drive-response tracking analysis would not.

**Where it does bite: inside the agent.** The useful use of the theorem is inside the agent's own network, not across the dyad. A balanced colouring of the agent's own cells, for example the cells that receive the partner's percept, gives a subspace $V$ that is invariant for *every* admissible vector field. That covers every parameter value, every learned weight that respects the cell and arrow types, and every route, because any composition of admissible maps is admissible. The proposed mechanism has three steps.
1. **Gate.** Let the partner's percept enter only through arrows whose heads lie in one colour class.
2. **Constraint.** Require the agent's own coupling to respect the colouring, a constraint on the wiring types, not on a gain.
3. **Result.** Partner-driven deviations then stay in a polydiagonal whose dimension is the number of colours. Copying on any subspace not contained in it is impossible, with relative defect at least 1.

This is the "bottleneck that the agent's own dynamics cannot spread" form of no-copy. It is structural, but it restricts *which* face directions the partner can touch at all. It does not make strong coupling on those directions non-copying.

**Is it an excluded framework?** No. It is a theorem about which invariant subspaces are forced by wiring, usable as a constraint on any core. The cells need not be oscillators.

**Verdict for the cycle.** Use it as the *invariance* half of a structural no-copy theorem: robust invariant subspaces come from wiring types, not tuning. The *which-way* half has to come from equivariance with a twist (see `golubitsky-2002-symmetry-perspective.md` and the synthesis).

## Verdict
**watch (constraint lemma, primary text not read).** Its value is that it decides which synchrony subspaces are forced for all parameters, with balanced colourings as the criterion. Across the dyad it only says copy is not invariant, which is weaker than not attracting.
