# Training robust neural networks using Lipschitz bounds (Pauli, Koch, Berberich, Kohler & Allgöwer)

Patricia Pauli, Anne Koch, Julian Berberich, Paul Kohler & Frank Allgöwer, *IEEE Control Systems Letters* 6, 2022 (published online 2021); arXiv:2005.02929v2 (15 Sep 2020), 6 pp.

## What was read
arXiv v2, extracted text, **in full**: introduction, §II (problem, LipSDP estimation, Theorem 1, the counterexample), §III (training with the weights as decision variables, the ADMM scheme, Theorem 6 on enforcing a bound, computational tractability), §IV (2-D example and MNIST, Table I), conclusion.

## The computation, precisely
**Estimation (Theorem 1).** For a multi-layer network with slope-restricted activations (α ≤ (φ(x) − φ(y))/(x − y) ≤ β), if there are L² > 0 and a **diagonal** T with P_l(L², T) ⪯ 0 (an LMI built from the stacked weights A, B and the last layer W_l), the network is L-Lipschitz. The smallest L is an SDP over (L², T).

**The counterexample to LipSDP's coupled multipliers (§II-C).** One hidden layer of 2 tanh units, W⁰ = [−1; −1], b⁰ = [−1; 1], W¹ = [−1, 1], b¹ = −0.5. The network fits cos x on [−π/2, π/2] within 0.0843, so its true Lipschitz constant is about 1. Yet the LMI with the coupled multiplier T = (e₁ − e₂)(e₁ − e₂)ᵀ ∈ T_n is feasible for arbitrarily small L². So Lemma 1 and Theorems 1–2 of Fazlyab et al. 2019, in their most accurate variant, are false; T must be diagonal.

**Training (§III).** With T fixed and α = 0 the LMI is linear in (L², W). An ADMM scheme alternates an SGD loss step on W with an SDP step on (L², W̄); a penalty ρ couples them. Version (i) regularises the bound; version (ii) adds the indicator of {L ≤ L_des} and, by Theorem 6, the network with weights W̄ satisfies the desired bound **at every iteration**. The SDP step is the bottleneck; cost grows cubically with the number of decision variables.

## Evidence with numbers
Table I (CEL / test accuracy / Lipschitz bound L / training time):
- 2-D example: nominal 0.07 / 88.66 % / 242 / 12.6 s; L2-regularised 0.27 / 86.10 % / 69.5 / 16.9 s; Lipschitz-regularised 0.22 / 90.56 % / 67.2 / 531 s.
- MNIST (one pooling layer, 50 tanh units): nominal 0.09 / 96.65 % / 96.6 / 56.4 s; L2 0.26 / 90.58 % / 9.49 / 57.4 s; Lipschitz 0.20 / 96.45 % / 8.74 / 2566 s.
So the certified bound fell from 96.6 to 8.74 for 0.2 points of accuracy, at about 45 times the training time.

## What it means for the designs
1. **A correction the repo must carry.** fazlyab-2019-lipsdp.md records LipSDP as "a joint certificate on the stacked map … far tighter than per-layer products". That remains true for the diagonal-multiplier variants; the coupled-multiplier variant is invalid (this paper; Revay et al. 2020; Wang & Manchester 2023, Remark 2.2). Any ceiling certificate in the engine must use diagonal multipliers only.
2. **Enforcement by projection works but is slow.** ADMM with an SDP step gives a bound that holds at every iteration, but at ~45× the training cost on a 50-unit network. Nightly replay on the operator's Mac could afford it for small readouts; direct parameterisation (Revay et al. 2023; Wang & Manchester 2023) makes it unnecessary.
3. **Accuracy is not where the cost falls.** In both examples the bound shrank by an order of magnitude with no loss of test accuracy, which is weak, task-specific evidence that tight ceilings need not destroy fit; it says nothing about expression routes.

## Verdict
**adopt (as the correction to LipSDP and as the projection-based alternative to direct parameterisation).**
