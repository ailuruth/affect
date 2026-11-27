# Compositional Game Theory (Ghani, Hedges, Winschel & Zahn)

Citation: N. Ghani, J. Hedges, V. Winschel, P. Zahn. "Compositional Game Theory." *Proceedings of LICS 2018*, 472–481. arXiv:1603.04641v3.

Source read: the arXiv PDF (v3, 10 pages), text-extracted, read in full. The paper omits proofs; they are in Hedges' thesis and "Morphisms of open games" (arXiv:1711.07059), **not read**. Iterated open games (Ghani, Kupke, Lambert & Nordvall Forsberg) and mixed strategies are only mentioned as future or other work.

## What the paper does
- **Selection functions first.** A higher-order game gives each player a selection function δ_i : (X_i → R) → P(X_i), the moves considered good in a context k : X_i → R. A context is the utility of each unilateral deviation with the others' strategies fixed. With δ_i = argmax this is Nash equilibrium.
- **An open game** G : (X, S) → (Y, R) is a 4-tuple (Σ_G, P_G, C_G, B_G):
  - Σ_G strategy profiles;
  - play P_G : Σ_G × X → Y (observations to moves);
  - coplay C_G : Σ_G × X × R → S, the **coutility** the game returns to its environment;
  - best response B_G : X × (Y → R) → Rel(Σ_G), defined relative to an arbitrary context (a state x and a continuation k).
  X, Y flow forward; R, S flow backward. "The future is abstracted into a single utility function."
- **Lens view (Lemma 1).** For each strategy σ, (P_G(σ, −), C_G(σ, −, −)) is a lens (X, S) → (Y, R): get X → Y, put X × R → S. An open game is a family of lenses plus a best-response function on points and co-points.
- **Atoms.**
  - A decision D : (X, 1) → (Y, R): strategies X → Y, trivial coplay, (σ, σ′) ∈ B iff σ′(x) ∈ argmax k. The pre-deviation σ plays no role (nothing to be a best response to in a one-player game).
  - Strategically trivial games (f, g) from functions (play f, coplay g).
  - The counit ε_X : (X, X) → (1, 1), coplay returns the forward value as a backward one: it identifies an ordinary value "as the value about which some past agent is reasoning". **There is no unit** (1, 1) → (X, X); game theory is not symmetric in its forward and backward facets, and open games are not compact closed.
- **Composition** H ∘ G: play composes; coplay C_{H∘G}((σ, τ), x, q) = C_G(σ, x, C_H(τ, P_G(σ, x), q)); best response: G is judged in context (x, k′) with k′(y) = C_H(τ, y, k(P_H(τ, y))), H in context (P_G(σ, x), k). In lens terms, G's continuation is k ∘ τ.
- **Monoidal product** (simultaneous play): player 1's continuation k₁(y₁) = π₁ k(y₁, P_{G₂}(σ₂, x₂)), the other's move held fixed.
- **Results.** A monoidal product of decisions capped by a counit through the outcome function q reproduces the best-response relation of an n-player simultaneous game (Theorem 2); a recursive construction reproduces finite sequential games of perfect information (Theorem 3). With non-argmax selection functions: two "fix" players (each wants to equal the other's choice) give a coordination game; two "anti-fix" players an anti-coordination game; one of each gives matching pennies, which has no pure equilibrium.
- **Limits stated.** Nash is built into the definition; pure strategies only; repeated games need further operators; a symmetric theory would need the Int construction on a traced category.

## The mathematical object
**A bidirectional process with a forward play wire and a backward coutility wire, whose equilibrium is a fixed point of a best-response relation computed against a context (past state, future continuation).** Coutility is what one system hands back as utility for another.

## What it means for the design
1. **"Copying" and "following" are selection functions.** The fix selection (choose what the other chooses) is literally the copy rule, and the paper shows it composes into a coordination game whose equilibria are the matched profiles. A matched (copy) state is an equilibrium of any dyad in which either side's selection is fix-like. Anti-fix on one side gives no pure equilibrium (endless chase).
2. **Coutility is the approval channel, typed.** In the formalism the partner's returned utility travels on its own backward wire. A design rule "the agent's continuation never includes the partner's coplay" is expressible exactly.
3. **In a human dyad the two wires are one signal.** A smile is a move (play) and a returned utility (coplay) at once. The formal separation has no observable counterpart unless the agent can infer which part of the partner's movement is a move and which is a return. That inference problem is what the causal-representation notes of this pass address.
4. **The missing unit matters.** Backward-flowing values can be bent forward (counit) but not created from nothing. An agent cannot manufacture the partner's future utility as its own present input except through a model of the partner, which is where a design must place it.

## Verdict
- **watch (vocabulary and one result).** It supplies an exact language for play versus returned utility and shows copy-as-selection yields coordination equilibria. It is game theory made compositional, with Nash built in. It has no learning dynamics, no time scales and no closed loop without extensions not read here.
