# Dissipativity, reciprocity and passive network synthesis: from Jan Willems' seminal Dissipative Dynamical Systems papers to the present day (Hughes & Branford, on Willems 1972)

Timothy H. Hughes & Edward H. Branford, arXiv:2102.08855v2 (3 Oct 2021), 47 pp., written for *IEEE Control Systems Magazine*'s 50th-anniversary issue on Willems (published 2022, doi:10.1109/MCS.2021.3139558 per the search listing; not verified). It retells **J. C. Willems, "Dissipative dynamical systems Part I: General theory", Arch. Rational Mech. Anal. 45:321–351 (1972)** and Part II (pp. 352–393) theorem by theorem. Willems' own PDF (KU Leuven homepage) and the Springer copy were **not reachable** from this session. Every statement attributed to Willems below is Hughes & Branford's account of it, cited by their theorem numbers.

## What was read
- **Read in full:** the introduction and the section "Dissipative Dynamical Systems Part 1" (definitions, available storage, required supply, Theorems 1–6 of Willems Part I, Willems' own stated limitations).
- **Read in part:** the section on Part II (linear systems, quadratic supply: Theorems 1–8 of Part II as summarised).
- **Skimmed:** the passive-network-synthesis and reciprocity sections, and the sidebars on H∞ and controllability.

## The computation, precisely

**The system (Willems Part I).** A state transition map x(t) = φ(t, t₀, x₀, u) obeys consistency, determinism, the semigroup property and stationarity; the readout is y = r(x, u). A *supply rate* w(u, y) is a locally integrable function of input and output.

**Dissipativity (Part I, Definition 2).** The system is dissipative with respect to w if there is a non-negative storage S(x) with

  S(x₀) + ∫_{t₀}^{t₁} w(u(t), y(t)) dt ≥ S(x(t₁))

for all x₀, all t₁ ≥ t₀ and all u. *Lossless* means equality.

**Two canonical storages.**
- The *available storage* S_a(x₀) = sup over t₁ and u of the extractable supply, −∫_{t₀}^{t₁} w dt. Part I, Theorem 1: S_a(x₀) < ∞ for all x₀ **iff** the system is dissipative.
- The *required supply* S_r(x₀) = inf of ∫_{t₋₁}^{t₀} w dt over inputs that steer the state from the minimum-storage state x* to x₀. Theorem 2: it is finite iff the system is dissipative, provided every state is reachable from x*.
- Every storage S satisfies S_a ≤ S ≤ S_r.

**Further results.**
- Theorem 3: the storage functions form a convex set.
- Theorem 4: lossless, reachable and controllable implies S_a = S_r, so the storage is unique.
- **Theorem 5:** "a neutral interconnection of dissipative systems is itself dissipative" (formalised in Part II §4, under well-posedness). The supply rates of the parts sum to the supply rate of the whole, and the internal port supplies cancel.
- Theorem 6: x* is a stable (not necessarily asymptotically stable) equilibrium if S is continuous with a strong local minimum there.

**The linear, quadratic case (Part II).** For a minimal ẋ = Ax + Bu, y = Cx + Du and w = uᵀy, the system is dissipative iff G(s) is positive real (Part II, Theorem 1). With D + Dᵀ invertible, this is equivalent to an algebraic Riccati equation having a solution X ≥ 0. Then S_a(x) = ½xᵀX₋x and S_r(x) = ½xᵀX₊x, the extremal Riccati solutions.

**The limits Willems himself named (Hughes & Branford's reading).**
- The input–state–output representation is not unique, and the theory "does not address the question of whether or not the dissipativity property depends on the specific representation". For cyclo-dissipative systems it does depend on it.
- Interconnections of passive elements need not be well-posed.

## Evidence with numbers
None. These are theorems. The retrospective contains no numerical examples relevant here.

## What it means for the designs
1. **Supply rate as the conserved currency of influence.** Willems' framing converts "how much can the partner move the face?" into "how much *supply* can the partner port deliver, and how much can the face port extract?" The available storage S_a is exactly "the most that can ever be got out of this state". A design could define a *partner supply rate* on the perception port and an *expression supply rate* on the face port. If the agent is dissipative for w = c²‖partner‖² − ‖face‖², then the face can never extract more than c² times what the partner put in, plus the initial storage. That holds over **all internal routes**, because the inequality is about the ports only.
2. **Theorem 5 is the composition rule the designs lack.** Each design bounded routes one at a time. Willems' rule says: give each module a supply rate, check that the internal connections are neutral (internal supplies cancel), and the whole is dissipative with the external supply rate. Any route that is not neutral is a port that was missed. Those are exactly the leaks the critiques found: the care loop's unbounded slope, the shared estimate, content events.
3. **The ceiling must be innate.** The storage is a property of the agent, but the supply rate is chosen by the designer. Its constant c is the innate ceiling, and it must not be a learned parameter, or it becomes the dial. Dissipativity says nothing about learning: a learned parameter that changes the dynamics must be shown to keep the inequality for every value (see revay-2023-recurrent-equilibrium-networks.md).
4. **Copy non-attracting.** Theorem 6 gives only *stability* of the minimum-storage state, not asymptotic stability. Dissipativity alone does not exclude a second attracting state (a copy state). Strict dissipativity plus positive-definite storage does (see scherer-2022-dissipativity-iqc.md, S5–S6).
5. **Shortfalls.**
   - This is an existing framework (passivity and energy methods, the ancestor of port-Hamiltonian modelling, which the partner-regulator design already uses). It is a **constraint on a core**, not a core.
   - The representation-dependence caveat matters here: the designs change representation (latent coordinates, synergies). A dissipativity claim must be stated on the external port signals (partner face, own face) to be invariant.

## Verdict
**adopt (as the composition rule: per-module supply rates, neutral interconnection, whole-system inequality; ceilings in the supply rate are innate constants).** Read only through Hughes & Branford's retelling; Willems 1972 itself was not reached.
