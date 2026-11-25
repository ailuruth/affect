# Hasani, Lechner, Amini, Rus & Grosu 2021: Liquid Time-constant Networks

Citation: R. Hasani, M. Lechner, A. Amini, D. Rus, R. Grosu. "Liquid Time-constant Networks." *AAAI* 35(9): 7657-7666, 2021. arXiv 2006.04439 (v4, 14 Dec 2020). Code: github.com/raminmh/liquid_time_constant_networks.

Source read: the arXiv v4 PDF via text extraction. Read in full: abstract, sections 1-6 (introduction, fused solver, BPTT training, bounds on τ and state, expressivity and trajectory length, time-series experiments), related work, and conclusions with limitations. Tables 3 and 4 read. Not read: the appendix proofs of Theorems 1-5 and the per-experiment setup, and Table 5 and 6 values (only their captions and the text about them).

## The failure or bottleneck it answered

The paper does not start from a measured failure. It starts from an open question about Neural ODEs: "how expressive are neural ODEs in their current formalism, and can we improve their structure to enable richer representation learning and expressiveness?" The measured gap it then shows is one of expressivity, using the trajectory-length measure of Raghu et al. 2017. With Hard-tanh units (Table 2), the solver takes 0.61 ± 0.02 steps per input for a Neural ODE, 4.05 ± 2.17 for a CT-RNN and 81.01 ± 10.05 for an LTC. In one example (Fig. 2) the latent trajectory length is 108.2 for a Neural ODE, 90.5 for a CT-RNN and 12,481.0 for an LTC.

On the benchmarks (Table 3, n = 5) LTC is best on four of seven tasks. For example:
- Traffic squared error: 0.099 ± 0.0095 against LSTM 0.169 ± 0.004.
- Gesture accuracy: 69.55% ± 1.13 against CT-GRU 68.31% ± 1.78.

It loses on three:
- Activity recognition: 95.67% against Neural ODE 97.26%.
- Sequential MNIST: 97.57% against LSTM 98.41%.
- Power: 0.642 against CT-GRU 0.586.

The authors' own summary is "between 5% to 70% performance improvement ... in four out of seven experiments and comparable performance in the other three". The limitations they state:
- "LTCs express the vanishing gradient phenomenon".
- Performance is "majorly influenced when off-the-shelf explicit Euler methods are used".
- They are slower than Neural ODEs, "at the expense of elevated time and memory complexity".

## The new computation, in one equation

    dx/dt = −[ 1/τ + f(x, I, t; θ) ] ⊙ x + f(x, I, t; θ) ⊙ A,    so that τ_sys = τ / (1 + τ f)

A learned nonnegative sigmoidal network f does two jobs at once:
- It drives the state toward a fixed target A, the "bias vector", which plays the role of a reversal potential.
- It shortens that unit's time constant.

So the input decides how fast and how strongly each unit relaxes toward its own target, not where the unit ends up. Theorem 2 bounds the state: "min(0, A_min) ≤ x_i(t) ≤ max(0, A_max)". Theorem 1 bounds the time constant: "τ_i/(1 + τ_i W_i) ≤ τ_sys_i ≤ τ_i".

## New computation or recombination?

Recombination. The parts:
1. **A leaky linear neuron**, dv/dt = −g_l v + S. The paper credits this to Lapicque 1907 and Koch & Segev 1998.
2. **A synaptic current of the form S = f(v, I)(A − v).** This is the conductance-based synapse with a reversal potential. The paper says so: "All synaptic currents to the cell can be approximated in steady-state by the following nonlinearity (Koch and Segev 1998; Wicks, Roehrig, and Rankin 1996)". Plugging it in "we obtain an equation similar to Eq. 1."
3. **A bilinear input-by-state term.** The paper itself notes the resemblance to dynamic causal models, "dx/dt = (A + I(t)B)x(t) + CI(t)" (Friston, Harrison & Penny 2003).
4. **A semi-implicit ("fused") Euler step**, which makes the stiff ODE solvable step by step:

       x(t+Δt) = [x(t) + Δt f A] / [1 + Δt(1/τ + f)]

5. **BPTT through the solver** instead of the adjoint method.
6. **A trajectory-length expressivity measure** carried over from Raghu et al. 2017.

From my own knowledge, not from the paper: an input-gated conductance pulling a bounded state toward a fixed excitatory level is Grossberg's shunting equation (dx/dt = −Ax + (B − x)E − ...), from the 1970s. The paper does not cite Grossberg.

What LTC adds is training such units end to end with sigmoidal conductances, and showing that they are more expressive than CT-RNNs. That is a choice of parameterisation inside a known neuron model, not a change of what is computed. By the project's test (v2-README, Q9), LTC is the conductance-based neuron made trainable.

## What it suggests for an affective core

The useful object is the steady state of a unit with several conductances:

    x* = Σ_j g_j A_j / (g_L + Σ_j g_j)

Here each g_j is an input-gated conductance and A_j is its reversal potential. This is the textbook generalisation of Eq. 1 to one conductance per synapse; Eq. 1 as written has one A per neuron. Three properties matter for the target "partner influence is not one scalar gain":

1. **The partner can choose, but cannot author.** If the partner's signals enter only through conductances g_j, the state is a convex combination of the agent's own targets A_j. A partner can move the agent between its own levels, but cannot put a value outside [min A, max A] into it (Theorem 2). Copying requires the A_j to be learned from partner data, and then the copy sits in the targets, not in a gain. A lesion test follows directly: freeze the A_j from self-only data and measure whether partner-driven expression still tracks the partner.
2. **The influence is a vector, not one number.** With several partner-driven conductances, the partner's effect is the vector (g_1, ..., g_k) over the agent's own targets. Its direction changes with the situation, so the response profile can change, not only its amplitude. That is the "profile change" outcome the dial analysis (D75) asks about.
3. **Speed and strength are coupled, through the input.** The same f that pulls toward A also shortens τ_sys. A strongly driving partner makes the agent both more pulled and faster.

Does the input-dependent time constant just move the dial into the input? Partly yes. For a single conductance, x* = A·fτ/(1 + fτ): a saturating gain on a fixed target. If f is in effect one scalar function of "partner intensity", the dial is back, only now set by the partner instead of the designer. Flat affect (f → 0) to full pull (f → ∞) remains a one-dimensional axis, though the end point is the agent's own A and not the partner's value. The dial is removed only if two conditions hold together:
- several conductances with distinct, self-owned A_j;
- partner features that drive them selectively.

That is a condition on structure, not something LTC provides by default. Even then, the total conductance Σ g_j is a scalar that sets the agent's overall responsiveness and speed. Expect a critic to call that the dial, and to ask what keeps Σ g_j bounded.

## Verdict

reject as a new core (a conductance-based or shunting neuron, made trainable). Watch the conductance-weighted steady state as a bounded form of partner influence: the partner selects among the agent's own reversal levels and can never write a level of its own.
