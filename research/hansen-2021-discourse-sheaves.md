# Opinion dynamics on discourse sheaves (Hansen & Ghrist)

Jakob Hansen & Robert Ghrist, "Opinion dynamics on discourse sheaves", *SIAM Journal on Applied Mathematics* 81(5):2033–2060, 2021; arXiv:2005.12798 (v1, 26 May 2020).

## What was read
The arXiv v1 text in full: §§1–13, about 12,000 words, all theorems and proofs. Figures were seen only as captions; the reference list was skimmed. The companion "Toward a spectral theory of cellular sheaves" (2019) was not read. Statements marked **[own]** are my derivations, not the paper's.

## The computation, precisely

**Cellular sheaf (§2.1).**
> "a vector space F(v) for each vertex v of G, a vector space F(e) for each edge e of G, and a linear map F_{v⊴e} : F(v) → F(e) for each incident vertex-edge pair."

**Coboundary and Laplacian.**
- For an oriented edge $e=u\to v$: $(\delta x)_e = F_{v⊴e}x_v - F_{u⊴e}x_u$ (2.3).
- $H^0(G;F)=\ker\delta$, the global sections (2.4).
- $L_F=\delta^\top\delta$ (2.5).
- **Theorem 2.2 (Hodge):** $H^0=\ker L_F$.

**Discourse sheaf (§3).**
> "If the agents hold opinions x_u ∈ F(u) and x_v ∈ F(v), then they have expressed consensus when F_{u⊴e}(x_u) = F_{v⊴e}(x_v) ... this does not imply that u and v have the same opinions: it means that their expressions of personally held opinions have the appearance of agreement."

On lying:
> "Negative scalar multiplication in a restriction map permits falsehoods: one can model agents who lie. Such dissembling or deception can be done selectively."

**Theorem 4.1.** The dynamics $\dot x=-\alpha L_Fx$ converge to the orthogonal projection of $x(0)$ onto $H^0$. The paper adds:
> "If this sheaf has no nontrivial global sections, the only stable opinions will be everywhere zero: an uninteresting solution."

**Theorem 5.1 (stubborn agents).** If the agents on $U$ are held fixed, the rest converge exponentially to "the harmonic extension of $u=(x_0)|_U$ nearest to $x_0$". This is "a minimizer of $\|\delta x\|^2$ subject to $x|_U=u$", and "harmonic extensions are not in general global sections."

**Theorem 6.1 (control).** If $H^0(G,U;F)=0$, the system $\dot x=-\alpha L_Fx+Bu$ is stabilizable from $U$. Example 6.3 makes the point that for the constant sheaf, "it is only necessary to have arbitrary influence on a single individual in order to ensure eventual global consensus on any given opinion."

**Theorem 8.1 (learning to lie).** Restriction maps evolve by $\dot F_{v⊴e}=-\beta(F_{v⊴e}x_v-F_{u⊴e}x_u)x_v^\top$. The sheaf converges to
> "the nearest sheaf such that x is a global section ... measured by the squared Frobenius norm."

In Example 8.2, an agent with opinion −4 facing +1 "changes their expressed opinion's sign, but also downplays its magnitude".

**Joint opinion–expression diffusion (§9).** $\Psi=\tfrac12 x^\top\delta^\top\delta x$ is non-increasing (Lemma 9.1). The equilibria are a singular variety. Smooth equilibria are Lyapunov stable but not asymptotically stable (Thm 9.2). If a diagonal block of $\alpha\delta_0^\top\delta_0-\beta x_0x_0^\top$ is indefinite, the limit has $x_\infty\neq0$ (Thm 9.3).

**Antagonistic edges (§12).** Edge potentials $-\|y\|^2$ on negative edges give $L^S_F=\delta^\top S\delta$, which "is not necessarily positive semidefinite, so its corresponding diffusion dynamics may be unstable". Proposition 12.1: a cutset of negative edges whose local sections do not extend gives an indefinite $L^S_F$. "For the constant sheaf on G ... a graph with a cutset of negative edges always has an indefinite signed Laplacian, and hence unstable opinion dynamics."

## What it means for the designs
1. **The private/expressed split is the self/face split, and the paper's own result shows that agreement in expression is what learning finds.** Theorem 8.1 is a warning for any design with learned expression maps. If the maps are trained to reduce local disagreement, they converge to the nearest maps under which the current state looks like agreement: copy in a learned frame. The "lie" is a sign flip plus a shrink. Learned sign flips are not evidence against copying; they are how copy-in-a-frame is reached. This is the dyadic-sheaf design's failure, now with the paper's theorem behind it.
2. **Harmonic extension is the drive–response case.** Make the partner the stubborn node. Theorem 5.1 then sends the self to the harmonic extension of the partner's expression, and Example 6.3 says one node with influence fixes everyone's consensus on a constant sheaf. That is copy, by the paper's own reading.
3. **Obstruction to agreement only yields flat.** Theorem 4.1 and its remark: with no global sections, diffusion goes to zero. **[own]** On a cycle, the composite of restriction maps around it (the holonomy) decides which sections exist. The paper does not discuss holonomy; this is my derivation. A twisted holonomy forbids copy only by forbidding any lasting coupled state.
4. **Antagonism gives instability, not structured non-copy.** Proposition 12.1: signed potentials make the Laplacian indefinite, so dynamics diverge. This is consistent with Shi, Altafini & Baras's repelling rule (see `altafini-2013-signed-consensus.md`).
5. **What survives.** The relative-cohomology controllability test (Thm 6.1) is a precise tool. "Can the partner steer the self's expression to any section?" is decidable by computing $H^0(G,U;F)$ with the partner as the input set $U$. **[own]** A design can try to prove $H^0(G,\{P\};F)\neq0$ on the expression-copy subspace, meaning the partner cannot reach it. But under diffusion, unreachable directions are exactly the ones that decay.

**Is it an excluded framework?** It is linear diffusion: on the excluded list as a core. Usable as an analysis tool (relative cohomology for reachability), and as the clearest theorem that learned expression maps drift toward copy-in-a-frame.

## Verdict
**watch (analysis tool and warning).** Theorem 8.1 proves that learning restriction maps to reduce disagreement converges to the nearest maps that make the current state look like agreement. Obstruction gives only flat; antagonism gives only instability.
