# Hochreiter & Schmidhuber 1997: Long Short-Term Memory

Citation: S. Hochreiter, J. Schmidhuber. "Long Short-Term Memory." *Neural Computation* 9(8): 1735-1780, 1997. Read from the authors' PDF hosted at bioinf.jku.at (publications/older/2604.pdf, 32 pages).

Source read: sections 1-7 in full (introduction, previous work, the vanishing-error analysis, the naive constant-error unit, the LSTM architecture, all six experiments with Tables 1-11, discussion, conclusion). Not read: Appendix A.1 (algorithm details) and A.2 (explicit error-flow formulae). The text came from a PDF-to-text extraction that dropped "fi"/"fl" ligatures; quotes below restore them. This is the 1997 cell: it has input and output gates but **no forget gate**, which came later (Gers, Schmidhuber & Cummins 2000, not read).

## The failure or bottleneck it answered

- The failure is a measured property of the backward pass. In BPTT and RTRL, "error signals 'flowing backwards in time' tend to either (1) blow up or (2) vanish: the temporal evolution of the backpropagated error exponentially depends on the size of the weights (Hochreiter 1991)."
- Section 3.1 derives the scaling factor of an error sent back q steps as a sum of products of f′(net)·w terms. With the logistic sigmoid, f′ is at most 0.25, so "the error flow tends to vanish as long as the weights have absolute values below 4.0". Raising the initial weights or the learning rate does not help: the latter "will not change the ratio of long-range error flow and short-range error flow. BPTT is too sensitive to recent distractions."
- Measured (Table 2, Task 2a, means of 18 trials): RTRL solved a 4-step lag in 78% of trials (learning rate 1.0) and a 10-step lag in 0%. At a 100-step lag, RTRL and BPTT had 0% success after 5,000,000 sequences, while LSTM had 100% after 5,040.
- A second failure is named before the fix. A single linear self-loop (the "naive approach") has an **input weight conflict** and an **output weight conflict**: the same weight must both store an input and ignore later inputs, and both release the stored content and keep it from disturbing other units.

## The new computation, in one equation

s_c(t) = s_c(t−1) + y_in(t) · g(net_c(t)),  y_c(t) = y_out(t) · h(s_c(t)),  with ∂s_c(t)/∂s_c(t−1) = 1

The cell's state is a linear integrator whose self-derivative is exactly 1, the "constant error carrousel" (CEC). The derivation runs backwards from the gradient: requiring f′_j(net_j(t))·w_jj = 1.0 forces "f_j has to be linear, and unit j's activation has to remain constant". Two multiplicative gates, each computed from the network's own state, decide when the integrator is written and when it is read. What is new is the backward computation. Error is carried across any number of steps unscaled, "Error signals trapped within a memory cell's CEC cannot change", and is truncated as it leaves the cell.

## New computation or recombination?

Parts, and where each came from:

1. A self-connection of weight 1 with a linear unit. This is close to Mozer's (1992) time constants, which the paper itself cites: "a time constant of 1.0 is appropriate for potentially infinite time lags". It is also close to Sun et al. (1993), which adds the old activation to the scaled net input.
2. Multiplicative units. The paper names Watrous & Kuhn (1992) second-order nets and Miller & Giles (1993): "It is not the first recurrent net method using MUs though."
3. Truncated gradients (Williams & Peng 1990), plus storing only ∂s/∂w as in Mozer's (1989) focused backprop.
4. Gate biases and constructive growth (Fahlman 1991), used as fixes for the "abuse problem".

Every part existed. What did not exist was the **invariant that selected and placed them**: unit derivative of the state with respect to its own past, with gates used *only* to protect that path. The paper states the difference from second-order nets in those terms: Watrous and Kuhn's architecture "does not enforce constant error flow", while LSTM's multiplicative units "are used only to gate access to constant error flow."

By the project's test (v2-README, Q9), the LSTM is a recombination at the level of parts. Its novelty is a **change of what is computed in credit assignment** (a protected, unscaled error path), derived from a measured failure, not a choice of what is stored or keyed. HiPPO (gu-2020-2021-hippo-s4.md, section 2.5) later showed that a gate is a first-order memory with an adaptive step size Δt. On that reading the gate is a learned clock rate, not a new kind of operation.

## What it suggests for an affective core

- **Separate storing from perturbing.** The output gate exists because a stored content must not disturb outputs that are already correct: "the multiplicative output gate protects other units from perturbation by currently irrelevant memory contents." For the affect core, this splits partner influence into two places:
  - what the partner *writes* into a protected store;
  - when that store is *allowed to move* the agent's own expression.

  The read gate would be computed from the agent's own state (need, ongoing activity), not from the partner's signal. Partner influence then has no single magnitude. It is a vector of per-cell write events, each released by a different state-dependent read condition.
- **Protection as an invariant, not a gain.** The CEC is defined by a constraint (∂s/∂s = 1), not tuned. The analogous move is to state an invariant that the partner channel must satisfy, and derive the architecture from it. An example invariant: "the partner can change which stored episode is released, but not the gain of release."
- **Where it collapses into the dial.**
  - Each gate is a scalar gain per cell. If the input gate learns to track the partner's signal magnitude while the read gate stays open, the cell is a leaky copy of the partner, and the mean gate opening is the familiar flat-to-copy dial.
  - The 1997 cell's integrator never forgets without a forget gate. A forget gate reintroduces a timescale parameter, which is a known source of the dial (the ridge ratio (1−λ)/η in the contingency sketch).
  - The paper's own "abuse problem" is a warning. Cells get used "as bias cells", so a store meant for partner content can degrade into a constant offset.
- **Credit through time.** The real lesson is methodological. The authors measured *why* learning failed (an exponential factor in the backward pass) and changed the computation so that factor is exactly 1. The same move for us: measure the dial's mechanism on human data (the D75 dial analysis in research/harness/HARNESS.md), then change what is computed so that the measured failure is impossible by construction, not tuned away.

## Verdict

watch. The protected integrator with state-gated read and write is the cleanest precedent for separating "partner writes" from "partner moves the face". But its gates are per-cell scalar gains, so on its own it does not remove the dial. Its method, an invariant derived from a measured gradient failure, is the part to copy.
