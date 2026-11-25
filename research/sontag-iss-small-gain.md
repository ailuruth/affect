# Sontag 1989, "Smooth stabilization implies coprime factorization" (IEEE TAC 34(4):435-443); Sontag 2008, "Input to State Stability: Basic Concepts and Results" (LNM 1932:163-220); ISS small-gain theorem (Jiang, Teel & Praly 1994, via Sontag & Ingalls 2002)

Source read, 2026-11-25, all from author copies:
1. Sontag 1989, "coprime-factorizations.pdf" on sontaglab.org. Read: the abstract, §I and §II up to Definition 2.2. The PDF is a scanned reprint and the text extraction garbles the symbols, so the formulas below are given in the 2008 survey's notation and the 1989 prose is quoted with its symbols re-typed.
2. Sontag 2008, "04cetraro_reprint.pdf" on sontaglab.org. Read: §1, §2.8-2.10 (the ISS definition and the linear case), §3.1-3.4 (superposition, robust stability, dissipation) and §4 up to the hand-off to Jiang–Teel–Praly. Only theorem headers were read in §5 onward (iISS and related).
3. Jiang, Teel & Praly 1994 (MCSS 7:95-120) was NOT accessible: the copy on Praly's site returns 404 and no open copy was found. Its interconnection theorem was read as restated in Sontag & Ingalls 2002, "A small-gain theorem with applications to input/output systems, incremental stability, detectability, and interconnections", J. Franklin Inst. 339:211-229 ("small-gain-as-published.pdf" on sontaglab.org). Read: §1-3 (definitions and Theorem 1) and §4.5.1 (Corollary 4.5, which "first appeared as Theorem 2.1 of [11]", i.e. JTP 1994).

## Claims
- Intent of ISS (1989): "Our definition of input-to-state stability is intended to capture the idea of bounded input bounded output behavior together with decay of states under small inputs."
- Definition (2008 §2.9): "there should exist some β ∈ KL and γ ∈ K∞ such that |x(t)| ≤ β(|x0|, t) + γ(‖u‖∞) (ISS) holds for all solutions". "All solutions" means "all inputs u(·), all initial conditions x0, and all t ≥ 0". The 1989 Definition 2.1 has the same form, with "β of class KL" and "γ of class K", and "for each measurable essentially bounded control u(·) and each initial state".
- Interpretation (1989): "For a bounded control u, trajectories remain in the ball of radius β(|ξ0|, 0) + γ(‖u‖). Furthermore, as t increases, all trajectories approach ... the smaller ball of radius γ(‖u‖)." Also: "Since γ(0) = 0, an ISS system is necessarily GAS", but "in general ... GAS does not imply ISS". Unlike total stability, "here we wish to have bounded behavior for arbitrary bounded controls."
- Linear case (2008 §2.10): "For internally stable linear systems ẋ = Ax + Bu ... |x(t)| ≤ β(t)|x0| + γ‖u‖∞", with "β(t) = ‖e^{tA}‖ → 0" and "γ = ‖B‖ ∫₀^∞ ‖e^{sA}‖ ds < ∞".
- Equivalences (2008 §3):
  - "Theorem 3.1. A system is ISS if and only if it is 0-stable and AG", where the asymptotic gain (AG) is "lim sup_{t→+∞} |x(t, x0, u)| ≤ γ(‖u‖∞)".
  - "Theorem 3.3. A system is ISS if and only if it is robustly stable", meaning it stays GAS under all feedback perturbations bounded by a margin ρ ∈ K∞, "|∆(t, x)| ≤ ρ(|x|)".
  - "Theorem 3.4. A system is ISS if and only if it admits a smooth ISS-Lyapunov function."
- Cascades (2008 §4): "a cascade (Fig. 12) of ISS systems is again ISS". A small feedback is allowed when "|k(z)| ≤ θ̃⁻¹((1 − ε)α(|z|))". Sontag then hands off: "A much more interesting version of this result ... is the ISS small-gain theorem due to Jiang, Teel, and Praly."
- The JTP interconnection theorem (Sontag & Ingalls 2002, Corollary 4.5):
  - Hypotheses: two subsystems with outputs bounded as "|y1(t)| ≤ max{β1(|x1|, t), γy1(‖y2‖[0,t]), γu1(‖u1‖[0,t]), C1}" (and symmetrically for y2), plus state bounds "|x1(t)| ≤ max{σ11(|x1|), σ31(‖y1‖[0,t]), σ41(‖u1‖[0,t]), d1}".
  - Small-gain condition: "Suppose further that there exists r0 ≥ 0 so that γy1(γy2(r)) < r ... ∀r > r0."
  - Conclusion: "the interconnection is practically IOS", that is, "|(y1(t), y2(t))| ≤ max{β(|(x1, x2)|, t), γ(‖(u1, u2)‖[0,t]), C}" with "C = 0 when C1 = C2 = d1 = d2 = r0 = 0".
  - In general terms: "The small-gain condition appears as the typical requirement that an appropriate composition of gains is a contraction."
- The general version (Sontag & Ingalls Theorem 1) needs "a K-function γ for which γ(r) < r if r > r0". Its conclusion carries the offsets "3C, 3r0", so bounded constant terms survive the interconnection as a bounded residual.

## Evidence
Theorems with proofs (1989; 2002 including an appendix). The 2008 survey is expository by its own account ("an intuitive and informal presentation"), with references to the proofs.

## License
- IEEE TAC 1989: © IEEE.
- LNM 2008: © Springer.
- J. Franklin Inst. 2002: © Elsevier; there is also an arXiv version, math/0110317.

All three were read as author reprints on sontaglab.org. No code.

## Runs on this Mac without a GPU?
Yes. Checking ISS needs only a Lyapunov or bound argument, plus simulation of small ODEs to check gain estimates empirically. No model weights are involved.

## Verdict: adopt (as the safety argument for coupling a frozen language model to the regulator)
For (b), a guaranteed-safe coupling of a frozen LM to a regulator:
- The theorems need each subsystem to satisfy a bound with known comparison functions. A frozen LM has no such certified gain from regulator state to its output, so the LM cannot be treated as an ISS subsystem with a known γ.
- What does work, from the statements read: put a hard saturation between the LM and the regulator, so the LM's influence u satisfies |u| ≤ U whatever the LM does. If the regulator is ISS in u, its state obeys |x(t)| ≤ β(|x0|, t) + γ(U) for every LM behaviour, adversarial or not. No small-gain condition is needed for that bound.
- In small-gain terms: the saturated LM channel is a subsystem whose output bound is a constant C (gain γ ≡ 0 above r0). The condition γy1(γy2(r)) < r for r > r0 then holds trivially, and the price is the residual offset (3C, 3r0). This is boundedness, not convergence to the set point while the LM keeps pushing.
- Two obligations follow for the design. Prove the regulator ISS, which is a stronger requirement than GAS ("GAS does not imply ISS"). And make the saturation a structural fact of the code, not a learned behaviour.
- JTP 1994 itself was not read. Cite it through Sontag & Ingalls Corollary 4.5 until the original is obtained.
