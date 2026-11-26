# Graph fibrations and symmetries of network dynamics (Nijholt, Rink & Sanders)

Eddie Nijholt, Bob Rink & Jan Sanders, "Graph fibrations and symmetries of network dynamics", *Journal of Differential Equations* 261(9):4861–4896, 2016; arXiv:1410.6021 (v1, 22 Oct 2014).

This note was read in place of Golubitsky & Stewart 2006 (Bull. AMS), which could not be reached; see `golubitsky-2006-groupoid-network-synchrony.md`. It restates the Golubitsky–Stewart balanced-partition theorem with a proof.

## What was read
§§1–4 in full: the introduction, the three examples, networks and network maps, and graph fibrations with robust synchrony, including the proof of Theorem 4.1. §§5–7, on homogeneous networks and the fundamental network, were skimmed for theorem statements. §§8–11 were not read.

## The computation, precisely
**Network (Def. 3.1).** A finite directed graph with coloured cells and arrows, such that "if two vertices v1, v2 ∈ V have the same colour, then there is a colour-preserving bijection $\beta_{v_2,v_1}: t^{-1}(v_1)\to t^{-1}(v_2)$". These bijections form the **symmetry groupoid**.

**Network (admissible) maps (Def. 3.2).** $(\gamma_f)_v(x)=f^v(\pi_vx)$, where $\pi_v$ collects the states at the sources of the arrows into $v$. The response functions are "groupoid-invariant: $f^{v_1}\circ\beta^*_{v_2,v_1}=f^{v_2}$".

**Theorem 4.1 (Golubitsky–Stewart et al., with proof).** For a partition $P$ of the cells, the following are equivalent:
- (i) $\gamma_f(\mathrm{Syn}_P)\subset\mathrm{Syn}_P$ "for all choices of response functions" (a *robust synchrony space*);
- (ii) for all $v_1\sim_Pv_2$ there is a $\beta_{v_2,v_1}$ with $s(a)\sim_Ps(\beta(a))$ for every arrow into $v_1$ (the partition is *balanced*).

The proof of (i)⇒(ii) builds special linear response functions that count same-coloured inputs from each class.

**Graph fibrations (Def. 4.2, Thm 4.3, DeVille & Lerman).** A colour-preserving graph map that is a bijection on the input sets of each cell. Pulling back by the fibration sends solutions of the quotient to solutions of the lift, and "every robust synchrony of N₁ arises from a graph fibration in this way".

**Theorem 1.1.**
> "Such a network is the quotient of a network with a semigroup(oid) Σ_N of self-fibrations. The dynamics of this 'lift' is thus Σ_N-equivariant. Moreover, every robust synchrony in the lift ... is an invariant subspace for any Σ_N-equivariant dynamical system."

The paper's conclusion is that "network systems are examples of equivariant dynamical systems".

**Feedforward example (§2).** Network A ($\dot x_{v_1}=f(x_{v_1},x_{v_1},x_{v_1})$, $\dot x_{v_2}=f(x_{v_2},x_{v_1},x_{v_1})$, $\dot x_{v_3}=f(x_{v_3},x_{v_2},x_{v_1})$) has a lower-triangular linearisation $\begin{psmallmatrix}a+b+c&0&0\\b+c&a&0\\c&b&a\end{psmallmatrix}$. Networks A, B and C have the same robust synchronies and spectra, but "their synchrony breaking bifurcations are very different", and the difference is "fully determined by nonlinearities".

## What it means for the designs
1. **Robust means for every response function.** Invariance of a balanced synchrony holds "for all choices of response functions", which is every parameter and every learned weight that respects the colouring. That is the cap-free *kind* of guarantee the operator wants. But it is a guarantee of **invariance**, which comes from wiring. **Attraction** is a separate question (see `pecora-2014-symmetry-cluster-synchronization.md`).
2. **The dyad.** **[own]** Put the self cell $S$ and an exogenous partner cell $P$ in one network, where $S$ has an arrow from $P$ and $P$ has none from $S$. They then have different input sets, so they cannot share a colour. If they could, the partition $\{S,P\}$ would not be balanced. Copy is therefore never a robust synchrony. That only means it is not invariant for generic $f$. High-gain tracking can still bring it arbitrarily close (C1). **Not invariant does not mean not attracting.**
3. **The useful direction: inside the agent.** **[own]** A balanced partition of the agent's own cells gives a subspace that is invariant for every admissible map. If the partner percept is wired only into one colour class and all couplings respect the colours, partner-driven deviations stay in a polydiagonal of known dimension for every parameter. That is a structural bottleneck. Copy on any subspace outside it is impossible, with relative defect at least 1. It limits *which* face directions the partner can touch, not whether touching them copies.
4. **Hidden symmetry means equivariance is the general language.** By Theorem 1.1, network structure *is* equivariance under a semigroupoid. A design can state its no-copy constraint as equivariance and inherit the network results. The synthesis does this.
5. **Feedforward wiring is nilpotent.** **[own]** In the strictly triangular part, the linearisation has no non-zero eigenvalue, so exact copy is impossible. But approximate copy returns at large weights: defect 0.22, 0.04, 0.0025 and 0.0001 at weight norm 2, 5, 20 and 100 (C4b). That is a cap again.

**Is it an excluded framework?** No. It is a theorem class about admissible maps, usable as a typing constraint on a core.

## Verdict
**adopt (as the invariance lemma, read in place of Golubitsky & Stewart 2006).** Balanced partitions are exactly the synchronies invariant for every response function, and network structure is hidden equivariance. Across the dyad this gives only "copy is not invariant", which is weaker than "copy does not attract".
