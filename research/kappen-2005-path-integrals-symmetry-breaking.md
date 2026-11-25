# Kappen 2005, "Path integrals and symmetry breaking for optimal control theory" (J. Stat. Mech. P11011; arXiv physics/0505066v4)

Source read: arXiv PDF v4 (dated 7 Oct 2005 on the arXiv stamp), read via text extraction: abstract, sections 1-3 in full (stochastic HJB, linear HJB, forward diffusion, path integral), section 4.1 (Laplace approximation, start), the double-slit symmetry-breaking result in section 6.1 (Fig. 5 and Eq. 34), and the Discussion (section 7). Not read: sections 4.2-4.3 (linear-quadratic example, multimodal Laplace mixture) beyond the abstract and introduction's summary of them, section 5 (MC sampling, importance sampling), section 6.2 details, references. The published J. Stat. Mech. version was not compared with arXiv v4.

## Claims
- Setting (Eqs. 6-7): "dx = (b(x, t) + Bu)dt + dξ" with cost "φ(x(tf)) + ∫ dt (½ u(t)ᵀRu(t) + V(x(t), t))". "B, R and ν are independent of x, u, t. b and V are arbitrary functions of x and t and φ is an arbitrary function of x." The control is "restricted to the simple LQ form" (linear in u, quadratic cost).
- Optimal control (Eq. 8): "u = −R⁻¹Bᵀ∂ₓJ(x, t)".
- Log transform: "Define ψ(x, t) through J(x, t) = −λ log ψ(x, t)". The quadratic terms "vanish if and only if there exists a scalar λ such that ν = λBR⁻¹Bᵀ (9)". When it holds, "∂ₜψ = (V/λ − bᵀ∂ₓ − ½Tr(ν∂ₓ²))ψ = −Hψ (10)", linear, with end condition "ψ(x, tf) = exp(−φ(x)/λ)".
- When the condition holds and when it is a restriction: "In the one dimensional case, such a λ always exists, and Eq. 9 is not a restriction. In the higher dimensional case, Eq. 9 restricts the possible choices for the matrices R and ν." With B the identity and R, ν diagonal, "Eq. 9 states R ∝ ν⁻¹. In a direction with low noise, control is expensive (Rᵢᵢ large) and only small control steps are permitted. In the limiting case of no noise, we deduce that u should be set to zero: no control is allowed in noiseless directions. ... Loosely speaking, Eq. 9 states that noise and control should operate in the same dimensions." Footnote 1 example (second-order system, B = (0, 1)ᵀ): the condition "states that the stochastic dynamics must have the noise restricted to the second component only", with "λ = νR". The form λR⁻¹ = ν is the special case the paper then adopts: "we assume the control dimension m = n and B the unit matrix."
- Feynman-Kac / forward computation (Eqs. 13-14): "ψ(x, t) = ∫ dy ρ(y, tf|x, t)ψ(y, tf)" and "J(x, t) = −λ log ∫ dy ρ(y, tf|x, t) exp(−φ(y)/λ)", where ρ is the uncontrolled diffusion with annihilation: "the potential term takes out probability density at a rate V(x, t)dt/λ". "Note that when V = 0 this diffusion process is identical to the original control dynamics Eq. 6 in the absence of control (u = 0)."
- Free-energy reading (Eq. 17): "J(x, t) = −λ log ∫[dx]ₓ exp(−S(x(t → tf))/λ)" ... "The path integral Eq. 17 is a log partition sum and therefore can be interpreted as a free energy. ... S(x(t → tf)) plays the role of the energy of a trajectory and λ is the temperature."
- Symmetry breaking (double slit, ν = R = 1): "symmetry breaking at νT = 1 ... For T > 1/ν (far in the past) it is best to steer towards x = 0 (between the targets) and delay the choice"; optimal control "u = (1/T)(tanh(x/(νT)) − x)" (Eq. 34). The author warns: "Clearly, this will not be true in general. For an arbitrary control problem, S does not need to be monotonic in T".

## Evidence
Analytical derivation plus one-dimensional numerical examples (double slit, drunken spider with ν = 0.001 and ν = 0.1, 1000 MC trajectories per x). No high-dimensional benchmark in the parts read.

## License
arXiv abstract page lists "assumed-1991-2003" (arXiv default licence). No code.

## Runs on this Mac without a GPU?
Yes in principle: the forward computation is Monte Carlo sampling of an uncontrolled diffusion with killing rate V/λ; the paper's examples are one-dimensional. No code was released or checked.

## Verdict: adopt (as the control layer's mathematics, with Eq. 9 as an explicit design constraint)
- For (a): J = −λ log ψ makes the cost-to-go a free energy with λ as temperature. This is the bridge from control to thermodynamic language, but it is a formal free energy over trajectories, not a physical one; the paper says "can be interpreted as".
- The condition ν = λBR⁻¹Bᵀ is exact and two-sided ("if and only if"). It excludes: noise in directions the control cannot reach (and control in noiseless directions, which must cost infinitely), state- or control-dependent B, R or ν, and independent choice of noise level and control cost. Any agent body built on this must put its noise only in actuated channels. Raising the noise automatically cheapens control; the two cannot be tuned separately.
- Symmetry breaking (delayed choice until T < 1/ν) is a candidate mechanism for indecision before commitment, but the νT threshold is specific to the example.
