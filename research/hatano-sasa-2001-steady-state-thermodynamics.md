# Hatano & Sasa 2001, "Steady-state thermodynamics of Langevin systems" (Phys. Rev. Lett. 86:3463; arXiv cond-mat/0010405v1)

Source read: arXiv PDF v1 (26 Oct 2000) in full, all four pages, via text extraction (some equation lines garbled; equations below were checked against surrounding text). The published PRL version was not compared, and v1 may differ from it.

## Claims
- Model (Eq. 3): "γẋ = −∂U(x; λ)/∂x + f + ξ(t)", noise intensity "2γk_BT", "periodic boundary conditions, and thus the particle flows due to the nonconservative force f." The authors add: "multi-dimensional cases, including many-particle systems, are essentially the same", without showing it.
- Split (Eq. 1, following Oono and Paniconi): "Qex ≡ Qtot − Qhk", where house-keeping heat is "steadily generated heat, which is generated even when the system remains in a single state". Sign: "positive when it flows from the system to the heat bath." Langevin form: "Qhk = ∫₀^τ dt b(x)ẋ(t)" (16), with "b(x) = f − ∂U/∂x + β⁻¹ ∂φ/∂x" (14), shown to equal "γjss/ρss(x; α)" (27), "propotional to the local average velocity."
- The potential: "φ(x; α) = −log ρss(x; α)" (4), the negative log of the steady-state density, not the energy U.
- Identity (Eq. 11, equivalently Eq. 8): "⟨exp(−∫₀^τ dt α̇ ∂φ(x; α)/∂α)⟩ = 1", i.e. "⟨exp[−βQex − ∆φ]⟩ = 1". Assumptions: "We assume that the system is initially in a steady state, and after the completion of the manipulation it converges to a new steady state", and a unique steady state for each parameter value.
- Inequality (Eq. 17): "β⟨Qex⟩ + ⟨∆φ⟩ ≥ 0", which with the Shannon entropy "S(α) = −∫dx ρss log ρss" becomes "T∆S ≥ −⟨Qex⟩" (19), assuming "τ is sufficiently large, so that the correlation between x₀ and x_N can be ignored." Equality holds for "a slow process in which the distribution function of the system can be regarded as ρss(xᵢ; αᵢ) at each time".
- Contrast with the total-heat route: the ordinary fluctuation theorem gives "T∆S ≥ −⟨Qtot⟩" but "the equality cannot be realized since −⟨Qtot⟩ is negative infinite for slow processes." The generalized Jarzynski equality "is not directly related to the fluctuation theorem" because detailed balance is violated.
- Free-energy form: "⟨Wex⟩ − ∆F ≥ 0" (25) with "Wex = Qex + ∆U" and "F(α) = ∫dx ρss U − TS(α)" (23).

## Evidence
Analytical derivation for a one-dimensional driven Langevin ring. No simulation or experiment in the paper (experimental verification is cited by Seifert 2012, not here).

## License
arXiv abstract page lists "assumed-1991-2003" (arXiv default licence). No code.

## Runs on this Mac without a GPU?
n.a. (theory). Estimating φ needs the steady-state density of the agent's dynamics.

## Verdict: adopt (the excess/housekeeping split); watch (using the inequality per cycle)
- For (a): the split separates dissipation spent on staying in a nonequilibrium steady state (house-keeping, tonic) from dissipation spent on changing state (excess, phasic). That is a defensible two-part arousal.
- The inequality is stated in terms of φ = −ln ρss, the nonequilibrium potential, not the agent's energy U. If valence is defined on the agent's "potential", one must say which: U (Sekimoto work) or φ (Hatano-Sasa).
- For (b): the inequality is derived for transitions that start in a steady state and end relaxed in one. It is not a statement about a periodic steady state, where the distribution is not ρss of any single α. Applying it per cycle needs a separate derivation.
