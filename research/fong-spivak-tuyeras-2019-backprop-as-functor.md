# Backprop as Functor: a compositional perspective on supervised learning (Fong, Spivak & Tuyéras)

Citation: B. Fong, D. I. Spivak, R. Tuyéras. "Backprop as Functor: A compositional perspective on supervised learning." *Proceedings of LICS 2019* (IEEE). arXiv:1711.10455v3.

Source read: the arXiv PDF (v3, 17 pages), text-extracted, read in full, including Appendices A–C (proof of Proposition II.4, proof of Theorem III.2 in its generalised form A.1, category-theory background). Two cited works that the paper leans on were **not read**: Fong & Johnson, "Lenses and Learners" (arXiv:1903.03671) and Hedges, "From Open Learners to Open Games" (arXiv:1902.08666).

## What the paper does
- **The question.** Given learners for A → B and B → C, can one build a learner for A → C? Not from (parameters, implementation, update) alone: the first learner has no training pair (a, b′), because nothing says what b′ should be.
- **The missing piece: a request function.** A learner A → B is a tuple (P, I, U, r):
  - I : P × A → B (implementation),
  - U : P × A × B → P (update),
  - r : P × A × B → A (request: "the input that would have served you better").
  The request is "superfluous to a stand-alone learning algorithm" but "crucial in composing": there is no composite update without it (Remark II.2).
- **Composition** (the category Learn). For (P, I, U, r) : A → B and (Q, J, V, s) : B → C,
  - (I ∗ J)(p, q, a) = J(q, I(p, a)),
  - (U ∗ V)(p, q, a, c) = ( U(p, a, s(q, I(p, a), c)), V(q, I(p, a), c) ),
  - (r ∗ s)(p, q, a, c) = r(p, a, s(q, I(p, a), c)).
  The upstream learner's parameter update depends on the downstream learner **only through the request s** it receives. The monoidal product runs learners side by side with no exchange at all. Learn is a symmetric monoidal category (Proposition II.4); associativity holds only up to the bijection (P × Q) × N ≅ P × (Q × N), which is why morphisms are equivalence classes.
- **Main theorem (III.2).** Fix a step size ε > 0 and an error e(x, y) whose partial ∂e/∂x(x₀, −) is invertible for each x₀. Then gradient descent gives a faithful, injective-on-objects, strong symmetric monoidal functor L_{ε,e} : Para → Learn with
  - U_I(p, a, b) = p − ε ∇_p E_I(p, a, b),
  - r_I(p, a, b) = f_a(∇_a E_I(p, a, b)), with f_a the componentwise inverse of ∂e/∂x(a_i, −).
  Functoriality is the chain rule: training the composite equals composing the trained parts. For quadratic error the request is r_I(p, a, b) = a − ∇_a ½‖I(p, a) − b‖², and its resemblance to the update (without ε) is called "something of a coincidence" (Remark III.5).
- **Networks as a language.** Splitting and merging wires are bimonoids in Learn, each fixed by the error function (for quadratic error: merge µ requests (a₃ − a₂, a₃ − a₁); copy δ requests a₂ + a₃ − a₁). Every neural network is generated from three learners: scalar multiplication, bias and activation. Weight tying is a parameter wire split by a comonoid, which updates on the **sum** of the requests of its users.
- **Learn is bigger than gradient descent.** Update and request need not be derivatives, and the error can vary across the network (Section VII-B).
- **Relations (Section VII-D).** Lens ↪ Learn ↪ Game: asymmetric lenses are learners with trivial parameter space; learners are open games with a singleton best-response condition. Implementation corresponds to get and play; request to put and coplay; update to the best-response function. No convergence ("well-behavedness") condition is imposed on learners.

## The mathematical object
**A bidirectional morphism (P, I, U, r) whose backward wire, the request, is the only channel by which a downstream system shapes an upstream system's parameters.** Composition is defined by that wire; parallel product has none.

## What it means for the design
1. **A precise statement of the copy and flattery route.** If the partner is modelled as a learner downstream of the agent's expression (agent's face → partner), then the composite's update trains the agent's expression parameters on the partner's request, "the expression of yours that would have served my target better". That is the formal shape of approval-driven drift (sharma-2024-sycophancy.md). The theorem says this is the **only** downstream-to-upstream parameter route in a composite.
2. **But not the only route in a dyad.** The partner's movement also enters the agent as forward input A, and U(p, a, b) depends on a. A learner can be shaped by what it is shown, not only by what is requested of it. Cutting the request wire (training the agent's own expression on its own body outcomes, never on partner requests) is the existing project rule (learning never uses the partner's smiles, attention or time as reward). It does not bound the forward route.
3. **The dyad is a loop, and Learn has no loop.** Composition is sequential and monoidal; there is no trace. The copy attractor is a property of the closed loop, which this formalism cannot state without an extension (feedback or coalgebraic iteration; not given here).
4. **Weight tying sums requests.** If one parameter is shared between the agent's own expression model and its model of the partner (the shared-body-model idea of earlier passes), it is updated by the sum of the self request and the partner request. That is a concrete way a shared self/other model gets pulled toward the partner.

## Verdict
- **adopt (as a typing tool and a probe), reject as a core.** The request wire gives an exact vocabulary for "which updates came from whom" and an exact statement of the approval route. It is a framework for composing learners, not a learning mechanism, and it does not represent the closed dyad.
