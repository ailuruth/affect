# Opinion dynamics on discourse sheaves (Hansen & Ghrist)

Jakob Hansen & Robert Ghrist, "Opinion dynamics on discourse sheaves", *SIAM Journal on Applied Mathematics* 81(5):2033–2060, 2021; arXiv:2005.12798. Background: J. Hansen & R. Ghrist, "Toward a spectral theory of cellular sheaves", *J. Applied and Computational Topology* 3:315–358, 2019.

## What was read

**Not read in full in this session.** arxiv.org failed DNS on this session's network allowlist. A web search returned the abstract-level content:
- the authors build Laplacians and diffusion on "discourse sheaves";
- the sheaves can represent selective opinion modulation and lying;
- the paper covers controllability, reachability, bounded confidence and harmonic extension;
- diffusion converges to a harmonic state in which agents express opinions consistent with their neighbours, while their private views may still differ.

The sheaf-Laplacian definitions below are standard (Hansen & Ghrist 2019) and overlap `bodnar-2022-neural-sheaf-diffusion.md`, which was read earlier. Claims about the paper's specific theorems are limited to what the search confirmed.

## The computation, precisely

**Discourse sheaf on a graph.**
- **Stalks.** Each agent $v$ has a private opinion space $\mathcal F(v)$, and each edge $e$ has a discourse space $\mathcal F(e)$.
- **Restriction maps.** A linear map $\mathcal F_{v\trianglelefteq e}:\mathcal F(v)\to\mathcal F(e)$ says how $v$ expresses its private opinion when talking to its neighbour on $e$. The maps can be selective (a projection) or "lying" (a sign flip or a distortion).

**Coboundary and Laplacian.** $(\delta x)_e=\mathcal F_{u\trianglelefteq e}x_u-\mathcal F_{v\trianglelefteq e}x_v$ for an oriented edge $e=u\to v$, and $L_{\mathcal F}=\delta^\top\delta$.
- **Global sections.** $H^0=\ker\delta=\ker L_{\mathcal F}$, the configurations where every pair agrees *in expression*.

**Dynamics.**
- **Opinion diffusion:** $\dot x=-\alpha L_{\mathcal F}x$ converges to the orthogonal projection of $x(0)$ onto $H^0$.
- **Expression (edge) dynamics:** the paper also lets the restriction maps themselves evolve; I state that only at the level of the abstract.
- **Stubborn agents:** with some agents held fixed, the limit is the *harmonic extension* of the fixed values.

**Obstruction.**
- On a tree, every choice of invertible restriction maps can be gauged to the identity, so $\dim H^0=\dim$ stalk.
- On a cycle, the composite map around the cycle (the holonomy) matters: $H^0$ restricted to the cycle equals $\mathrm{Fix}(\mathrm{Hol})$. A holonomy with no fixed vectors makes global agreement impossible. This is the sheaf form of Altafini's unbalanced cycle.

## What it means for the designs

1. **Private versus expressed is exactly the self/face split.** Copy in expression ($\mathcal F_S x_S=\mathcal F_P x_P$) can coexist with any private state. A sheaf therefore cannot forbid *face* copy unless the restriction maps themselves are constrained. With one dyadic edge there is no holonomy (Bodnar note), so any invertible maps can be gauged away: copy-in-a-frame. This is the dyadic-sheaf design's failure.
2. **A topological obstruction needs a cycle.** Add a third node, the shared world or event, or the agent's own past self. Then the holonomy $\mathrm{Hol}=\mathcal F_{SP}\mathcal F_{PW}\mathcal F_{WS}$ decides which agreements can exist. If structure fixes $\mathrm{Hol}$ to a twisted element (for example $-1$ on some channel subspace), then on that subspace **no global section other than zero exists**: copy is impossible for every scaling of the maps.
3. **Under diffusion, frustration gives flat, not strong coupling.** Diffusion on a frustrated subspace decays to zero (Altafini: unbalanced means flat). The obstruction forbids copy only by also forbidding any lasting coupled state. So a sheaf obstruction must sit under non-diffusive dynamics, such as a conservative flow on $\delta$, or a twisted-equivariant response map, if coupling is to stay strong.
4. **Harmonic extension is the drive-response case.** With the partner as a stubborn node, the self converges to the harmonic extension of the partner's expression, which is copy-in-a-frame on a tree. This confirms that with an exogenous partner the only structural lever is the *class* of the maps (their holonomy or twist), not the topology of a two-node graph.
5. **Links to the symmetry route.** Fixing the holonomy to a group element $g$ with character $\chi(g)=-1$ is the twisted-intertwiner condition in sheaf language. The group-theoretic version (`golubitsky-2002-symmetry-perspective.md`) is stronger because it constrains the *response map*, whatever the dynamics, not only the diffusion's limit.

**Is it an excluded framework?** Sheaf diffusion is a linear diffusion operator, close to the excluded list, and the dyadic-sheaf design was judged a recombination. The holonomy obstruction is usable as a constraint.

## Verdict
**watch (primary not read in full; obstruction usable only as a constraint).** Expression-level copy is forbidden only by fixing a non-trivial holonomy on a cycle. Under diffusion that yields a flat face, not strong coupling. Its private/expressed split restates the self/face problem; it does not solve it.
