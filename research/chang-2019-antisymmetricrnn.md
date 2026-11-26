# AntisymmetricRNN, and stable architectures for deep networks (Chang et al.; Haber & Ruthotto)

Bo Chang, Minmin Chen, Eldad Haber & Ed H. Chi, "AntisymmetricRNN: A dynamical system view on recurrent neural networks", *ICLR* 2019, arXiv:1902.09689. Companion: Eldad Haber & Lars Ruthotto, "Stable architectures for deep neural networks", *Inverse Problems* 34(1):014004, 2018, arXiv:1705.03341 (v3).

## What was read
- **Chang et al.:** the arXiv text in full, §§1–5, Appendix B (the proof) and Appendix C (experimental details). Figures were seen only as captions, and the CIFAR and noise-padded tables were skimmed.
- **Haber & Ruthotto:** the abstract and §§1, 3 and 4.1–4.3 (stability, antisymmetric weights, Hamiltonian networks, symplectic propagation). §§4.4–6 (derivatives, regularisation, experiments) were skimmed only.

Claims about the dyad are mine and are checked in `foundations/sims/symmetry-no-copy/checks.py` (C1–C3, C7).

## The computation, precisely
**The critical criterion (Chang §3.2).** The paper argues that $\mathrm{Re}(\lambda_i(J))\ll0$ "results in a lossy system", so it asks for:
> "Re(λ_i(J(t))) ≈ 0, ∀i ... a condition we referred to as the critical criterion."

**The antisymmetric ODE.** $h'(t)=\tanh\big((W_h-W_h^\top)h+V_hx(t)+b_h\big)$ (eq. 8). Its Jacobian is $J=\mathrm{diag}(\tanh'(\cdot))(W_h-W_h^\top)$, "whose eigenvalues are all imaginary".

**Proposition 3 (App. B).** If $W$ is antisymmetric and $D$ is an invertible diagonal matrix, then $\mathrm{Re}\,\lambda_i(DW)=0$. Proof: $v^*Wv=\lambda\,v^*D^{-1}v$, where the left side is imaginary and $v^*D^{-1}v$ is real.

The paper also stresses that "the input and bias term only affect the bounded diagonal matrix": **the input enters inside the nonlinearity, so it cannot change the imaginary spectrum.**

**Forward Euler needs diffusion.** With imaginary eigenvalues, $|1+\epsilon\lambda|>1$. Hence the AntisymmetricRNN is $h_t=h_{t-1}+\epsilon\tanh((W_h-W_h^\top-\gamma I)h_{t-1}+V_hx_t+b_h)$ (eq. 12), with $\gamma\in\{0.001,\dots,1\}$ (App. C).

**Haber & Ruthotto.**
- **Antisymmetric ResNet (eq. 4.12):** $Y_{j+1}=Y_j+h\sigma(\tfrac12 Y_j(K_j-K_j^\top-\gamma I)+b_j)$.
- **Hamiltonian networks.** They use $\dot y=-\nabla_zH$, $\dot z=\nabla_yH$, which "conserve rather than increase or dissipate the energy". The key form is eq. 4.15:
  $$\dot y=\sigma(K z+b),\quad \dot z=-\sigma(K^\top y+b),$$
  which "is stable regardless of the spectrum or size of the matrices K(t) since the overall matrix in the linear transformation is antisymmetric". It is integrated with Verlet (4.17). The paper's Example 1 adds that $K_-$ (eigenvalues −2) gives "a contraction that annihilates differences in the features".

## What it means for the designs
The operator's suggestion was that coupling which conserves rather than contracts leaves no attracting copy. **The papers' guarantee is about a closed system's own Jacobian. The dyad is open, and the guarantee does not carry over.**

1. **H&R's 4.15 is a self–partner pair, but closed.** Read $y$ as self and $z$ as partner-model: the antisymmetric interconnection preserves energy, and nothing attracts. But the real partner is exogenous. It is not a state variable whose back-reaction $-\sigma(K^\top y)$ the agent controls.
2. **The input placement matters, and helps only nominally (C7).** In Chang's form the partner enters inside the tanh. Take $V=-\Omega$, so that $h=u$ (copy) is an equilibrium. With $\gamma=0$, copy is a centre: never attracting, with final distance 0.74. **But the time-average of the orbit equals copy (distance 0.008).** With the $\gamma>0$ the paper needs for discretisation, copy attracts (final distance 0.027). "Never attracting" is hollow when the orbit circles the copy.
3. **Error-driven skew coupling tracks (C1).** $\dot x=-dx+gK(u-x)$ with $K$ skew has DC transfer approaching $I$ as $g\to\infty$ (distance 0.98, 0.45, 0.05, 0.005 at $g$ = 0.1, 1, 10, 100).
4. **Skew forcing copies quadrature signals (C2).** $\dot x=-dx+gJu$: for independent (time-reversible) partner channels the zero-lag same-channel correlation is about 0. For channels in quadrature it is 0.895, and 0.999 at the best lag. A rotation acts as a delay.
5. **Skew stages in series compose to the identity (C3).** $JJ^\top=I$. Skew maps are closed under sums but not under products, so a two-stage indirect route reopens copy.

**The positive residue.** A non-contracting internal memory, from Hamiltonian or skew layers, suits persistent affect. Parameterisation by construction (the H&R 4.15 form is "stable regardless of the spectrum or size of the matrices") is the right *kind* of guarantee: a property of the parameter class, not of tuned values. But the property needed for no-copy must be closed under products and sums, which skewness is not.

**Is it an excluded framework?** Yes as a core: an RNN cell, a linear operator plus a nonlinearity. Usable as a numerical device.

## Verdict
**reject (as a no-copy mechanism).** Conservation holds for the closed system's Jacobian. In the open dyad:
- copy is a centre whose time-average is copy;
- error-driven skew coupling tracks;
- rotation acts as delay;
- two skew stages give the identity.

Keep the lesson that guarantees should hold for a whole parameter class.
