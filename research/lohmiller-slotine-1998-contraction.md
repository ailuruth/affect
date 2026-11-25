# Lohmiller & Slotine 1998, "On contraction analysis for non-linear systems" (Automatica 34(6):683-696)

Source read: authors' preprint PDF from the MIT Nonlinear Systems Laboratory (web.mit.edu/nsl/www/preprints/contraction.pdf), marked "NSL-961001, October, 1996. Revised, August, 1997. Final version, December 1997". Read via text extraction: abstract, introduction, sections 2 and 3 in full (basic result, generalized metric, converse theorem, linear properties including the disturbance bound and periodic inputs, combinations of contracting systems, additional remarks), section 4.1 (PD observers, start of Example 4.1), section 4.3.2-4.3.4 headings and the observer-error passage, and section 6 (conclusions). Not read in detail: the rest of section 4 (controller examples), section 5 (discrete time) beyond Theorem 3's statement, and references. The typeset Automatica version was not compared.

## Claims
- Scope: "We consider general deterministic systems of the form ẋ = f(x, t)"; "all quantities are assumed to be real and smooth".
- Basic bound (Eq. 3): with λmax(x, t) the largest eigenvalue of the symmetric part of ∂f/∂x, "d/dt(δxᵀδx) ≤ 2λmax δxᵀδx" and hence "‖δx‖ ≤ ‖δx₀‖ e^{∫₀ᵗ λmax(x,t)dt}".
- Definition 1: a contraction region is where "∃ β > 0, ∀x, ∀t ≥ 0, ½(∂f/∂x + ∂f/∂xᵀ) ≤ −βI < 0".
- Definition 2 (general metric M = ΘᵀΘ, uniformly positive definite): contraction if "F in (7) is uniformly negative definite or ∂f/∂xᵀM + M∂f/∂x + Ṁ ≤ −β_M M (with constant β_M > 0)", where "F = (Θ̇ + Θ ∂f/∂x)Θ⁻¹".
- Theorem 2: "any trajectory, which starts in a ball of constant radius with respect to the metric M(x,t), centered at a given trajectory and contained at all times in a contraction region with respect to M(x,t), remains in that ball and converges exponentially to this trajectory. Furthermore global exponential convergence to the given trajectory is guaranteed if the whole state space is a contraction region".
- Converse (section 3.5): "any exponentially convergent system is contracting with respect to a suitable metric", so "Theorem 2 actually corresponds to a necessary and sufficient condition for exponential convergence".
- Robustness (remark vii, Eq. 15): for a disturbed flow "ẋ = f(x, t) + d(x, t)", the distance R between desired and actual trajectories obeys "Ṙ + |λmax|R ≤ ‖Θd‖"; "For bounded disturbance ‖Θd‖ any trajectory remains in a boundary ball ... any trajectory converges exponentially to a ball of radius R in (15) with arbitrary initial condition".
- Entrainment (remark vi): "The output of any time-invariant contracting system driven by a periodic input tends exponentially to a periodic signal with the same period."
- Observers: "In an observer context, one then needs only verify that the observer equations contain the actual plant state as a particular solution to automatically guarantee convergence to that state." PD observer (Eq. 17): "x̄̇ = f(x̂, t) − K_P(ŷ − y) − K_D ẏ̂, x̂ = x̄ + K_D y". Contraction is preserved under parallel, feedback (with conditions) and hierarchical combination (section 3.8). The paper also notes Theorem 2 "can also be used to show exponential divergence of two neighboring trajectories".

## Evidence
Mathematical theorems with worked physical examples (underwater vehicle observer, chemical reactor observer, simple plants). No statistics.

## License
Preprint posted on the authors' lab site; journal version © Elsevier. No licence stated on the preprint. No code.

## Runs on this Mac without a GPU?
Yes. Checking contraction is an eigenvalue test on the Jacobian, and running an observer is integrating one extra copy of the dynamics.

## Verdict: adopt (as the formal basis of Principle 3, reading another through one's own dynamics)
- For (c): build an observer that is a copy of the agent's own dynamics driven by the other's observed outputs. If the copy is contracting and the other's true state is a particular solution of the copy, the copy converges to it exponentially, whatever the initial guess.
- The other agent is not literally the self. The mismatch between the self-model and the other enters as a disturbance d, so by Eq. 15 the copy converges to a ball whose size scales with the mismatch over the contraction rate, not to the other's state. The residual is a readable quantity: a large persistent residual means the other does not run on dynamics like mine.
- The 1998 results are deterministic. Noisy observations need the stochastic extension, which is not in this paper and was not read.
