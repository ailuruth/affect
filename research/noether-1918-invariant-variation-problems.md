# Noether 1918, "Invariante Variationsprobleme" (Invariant variation problems)

Citation: E. Noether, "Invariante Variationsprobleme", Nachr. d. König. Gesellsch. d. Wiss. zu Göttingen, Math-phys. Klasse, 235–257 (1918). English translation by M. A. Tavel, Transport Theory and Statistical Physics 1(3):183–207 (1971); LaTeX reproduction arXiv:physics/0503066v3 (2018).

Source read: the Tavel translation (arXiv PDF, 14 pp.), read in full: §1 (definitions, Theorems I and II), §2 (divergence relationships and dependencies), §3–4 (converses for finite and infinite groups), §5 (invariance of the constituents), §6 (Hilbert's assertion, proper and improper conservation laws), with footnotes. The German original was not read.

## What the paper proves
- **Setting.** An integral I = ∫ f(x, u, ∂u/∂x, …) dx and a group of transformations of x and u. ψ_i are the Lagrange expressions (left sides of the Euler–Lagrange equations). The basic identity is Σ ψ_i δu_i = δf + Div A (eq. 3).
- **Theorem I (finite group G_ρ, ρ parameters).** If I is invariant, then ρ linearly independent combinations of the Lagrange expressions are divergences: Σ ψ_i δu_i^{(λ)} = Div B^{(λ)} (eq. 13). Conversely, such divergence relations imply invariance. On solutions (ψ = 0) these are the conservation laws; in one dimension, ρ first integrals B^{(λ)} = const, "between which, however, non-linear dependencies may subsist".
- **Theorem II (infinite group G_∞ρ, ρ arbitrary functions p(x), with derivatives up to order σ).** Invariance gives ρ *identities* among the Lagrange expressions and their derivatives (eq. 16), holding whether or not the equations are solved: "ρ of the Lagrange equations are a consequence of the rest". Converse holds.
- **Sources (footnote 15).** If instead of ψ_i = 0 one has field equations ψ_i = T_i with "newly adjoined functions" T_i, the identities become Div B^{(λ)} = Σ T_i δu_i^{(λ)}: the conserved current is changed exactly by the source projected on the symmetry's infinitesimal direction δu^{(λ)}.
- **§6 (Hilbert's assertion).** For a finite subgroup of an infinite group under which I is invariant, the divergence relations are "improper": the B's are built from the Lagrange expressions and functions whose divergence vanishes identically. Local (gauge-type) invariance therefore produces no new conserved charge of its own; "the failure of proper laws of conservation of energy" is a feature of such invariance. Classical mechanics and special relativity have "proper" laws because "no infinite groups occur".
- Closing remark (footnote 27, quoting Klein): "relativity" can be replaced by "invariance relative to a group".

## What it means for the design
1. **Global symmetry gives a charge; local symmetry gives redundancy.** A gauge principle (invariance under a per-moment, per-person change of expression coordinates) yields identities, not slow variables. It can type an architecture, but it cannot by itself produce persistent state or time scales. This closes a tempting route ("time scales from gauge symmetry").
2. **The sourced form is the useful one.** Div B = Σ T δu says exactly which external input can change which charge: only the component of the input along the symmetry direction at the current state. If the partner enters only as a transformation *of the symmetry group itself* (δu along the orbit), its projection onto every Casimir-type invariant vanishes, and only non-symmetric own-body sources change those invariants. This is the derivation used for Direction 1 of new-core-search-3-synthesis.md.
3. **Nonlinear dependencies among first integrals** (u′ and u′² both conserved) are the warning that the number of conserved quantities is not the number of independent slow variables.

## License
1918 original in the public domain; translation © 1971 publisher, reproduced on arXiv. No code.

## Runs on this Mac without a GPU?
n.a. (mathematics).

## Verdict: adopt (as a derivation principle)
The sourced Theorem I gives the precise form "this input can change that slow variable only through its projection on the symmetry direction". Theorem II and §6 are the reason a local (gauge) symmetry is a constraint, not a mechanism.
