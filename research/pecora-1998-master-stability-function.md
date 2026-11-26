# Master stability functions for synchronized coupled systems (Pecora & Carroll)

Louis M. Pecora & Thomas L. Carroll, "Master stability functions for synchronized coupled systems", *Physical Review Letters* 80(10):2109–2112, 1998, doi:10.1103/PhysRevLett.80.2109.

## What was read

**Not read in this session.** The paper is not open access. A search confirmed the citation and the abstract's claim: many coupled-oscillator arrays reduce to one form, and the stability of the synchronous state is given by a single master stability function, the largest transverse Lyapunov exponent. The equations below are the standard MSF construction as I know it. The trace result and its check (C1, C5 in `foundations/sims/symmetry-no-copy/checks.py`) are mine. Do not cite the paper beyond the MSF construction.

## The computation, precisely

**Setup.** $N$ identical systems, coupled through a coupling matrix $G$ with zero row sums and a coupling function $H$:
$$\dot x_i = F(x_i) - \sigma\sum_j G_{ij}\,H(x_j).$$
The synchronous manifold $x_1=\dots=x_N=s(t)$ is invariant, with $\dot s=F(s)$.

**Linearise and block-diagonalise.** Linearise about $s$ and diagonalise $G$ (eigenvalues $\gamma_k$, with $\gamma_0=0$ along the manifold). Each transverse mode then obeys the same variational equation
$$\dot\xi = \big[DF(s(t)) - \alpha\, DH(s(t))\big]\xi,\qquad \alpha=\sigma\gamma_k .$$

**Master stability function.** $\Lambda(\alpha)$ is the largest Lyapunov exponent of this equation, a function of one complex parameter. Synchrony is locally stable if and only if $\Lambda(\sigma\gamma_k)<0$ for all $k\ge1$. The stable region in the $\alpha$-plane depends on $F$ and $H$ only, not on the network. Known shapes: unbounded (stable for every large enough coupling), bounded interval (desynchronises at too-strong coupling), or empty (**never stable at any coupling**).

## What it means for the designs

**Drive-response form.** The partner is exogenous, so the dyad is a drive-response pair: $\dot x = F(x) + K(u-x)$, where $u$ is the partner's face. The copy error $e=x-u$ obeys $\dot e = [DF - K]e + (\text{the part of } \dot u \text{ that is not } F(u))$. Copy is attracting when $DF-K$ is uniformly Hurwitz along the partner's trajectory, and exact when the partner happens to obey $F$.

**A cap-free result, the trace theorem.** By Liouville's formula, the sum of all transverse exponents is
$$\sum_i\lambda_i^\perp = \big\langle \mathrm{tr}\,DF(u(t))\big\rangle_t - \mathrm{tr}\,K .$$
- If the coupling is **traceless** ($\mathrm{tr}\,K=0$) and the agent's own dynamics are not volume-contracting along the partner's trajectory ($\langle \mathrm{tr}\,DF\rangle\ge0$), then not all transverse exponents can be negative. **Whole-face copy is unstable for every coupling strength and every traceless $K$**, however strong and however signed per channel. Check C5: 20,000 random traceless $K$ with gains from $10^{-2}$ to $10^3$ and $\mathrm{tr}\,A=0$: zero stable cases.
- Traceless per-channel signed gains are a "zero-sum" mimicry budget: positive same-feature gain on some channels must be paid for by negative gain (anti-mimicry) on others. Twisted intertwiners (see `golubitsky-2002-symmetry-perspective.md`) are automatically traceless, so the two results connect.

**Why it does not settle the question.**
1. **A stable agent breaks the hypothesis.** An agent whose face returns to rest has $\mathrm{tr}\,DF<0$ near rest. With $\mathrm{tr}\,A=-1.2$, 191 of 20,000 random traceless couplings made copy stable (C5). The theorem holds only where the agent's own body is expanding, for example excitable or self-terminating displays held at the partner's state.
2. **It covers the whole face only.** A sum condition allows copy on the positive-gain channels as a sub-pattern, and D78 counts copy on a large shared subspace.
3. **"Conserving" coupling is not enough.** Skew $K$ (zero trace, purely imaginary spectrum) with any dissipation $D=d I$ gives transverse spectrum $-d\pm i g\theta$, which is stable for every $g$. The DC transfer $(dI+gK)^{-1}gK$ approaches $I$ as $g\to\infty$ (distance 0.98, 0.45, 0.05, 0.005 at $g$ = 0.1, 1, 10, 100; check C1). **Error-driven skew coupling copies at high gain.**

**Is it an excluded framework?** As a model, yes: it treats coupled oscillators and identical systems. As an analysis tool (transverse exponents, Liouville trace), no. The trace identity is worth keeping as a test any design can run.

## Verdict
**watch (analysis tool, primary not read).** The trace theorem gives "copy unstable for every traceless coupling" only where the agent's own flow is not contracting along the partner's trajectory. A stable, resting agent violates that, so it cannot be the core's no-copy guarantee. It shows that error-driven skew coupling copies at high gain.
