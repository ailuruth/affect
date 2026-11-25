# Irie, Schlag, Csordás & Schmidhuber 2022: A Modern Self-Referential Weight Matrix That Learns to Modify Itself (with Kirsch & Schmidhuber 2022)

Citations:
- **Primary.** K. Irie, I. Schlag, R. Csordás, J. Schmidhuber. "A Modern Self-Referential Weight Matrix That Learns to Modify Itself." *ICML* 2022, PMLR 162. arXiv 2202.05780 (v2). Code: github.com/IDSIA/modern-srwm.
- **Companion.** L. Kirsch, J. Schmidhuber. "Eliminating Meta Optimization Through Self-Referential Meta Learning." ICML 2022 DARL workshop. arXiv 2212.14392 (v1).

Sources read (both arXiv PDFs, via text extraction):
- **Irie et al.** Read in full: sections 1-7, Tables 1-3, the Table 4 values without their column headers, and Appendix A (the per-submatrix equations and multi-head setup). Not read: Appendices B.2-C (hyperparameters, FC100, the memory-distribution ProcGen runs). Table 1's accuracy values did not survive extraction, so none are quoted.
- **Kirsch & Schmidhuber.** Read in full: the main text (about 4 pages: Observations 2.1-2.2, fitness monotonic execution (FME), bandit and Cartpole experiments, related work, limitations). Not read: Appendix A.

## The failure or bottleneck it answered

Weights that freeze after training. Irie et al.: "The WM becomes permanent once training ends", while "Many environments, however, continue to evolve after training has halted". Fast weight programmers (FWPs) adapt at runtime, but a "typical FWP has a slow NN with a weight matrix that remains fixed after training". Stacking programmers does not help: "such a hierarchy has no end, as the highest level programmer would still have a fixed weight matrix."

Kirsch & Schmidhuber name a second bottleneck. Meta-learning "creates a dependency on human engineering on the meta-level".

Measured results (Irie et al.):

| Test | DeltaNet | Self-referential weight matrix (SRWM) |
|---|---|---|
| Sequential Omniglot→Mini-ImageNet, total accuracy on the Mini-ImageNet segment | 50.4% | 53.3% |
| Same, on the Omniglot segment | 92.2% | 92.3% |
| ProcGen, 6 games, normalised test score | 18.6 (1.7) | 20.0 (1.8) |

- The two are close on single-task few-shot learning: "DeltaNet and SRWM tend to have similar performance".
- On ProcGen the other baselines score: feedforward 16.4, LSTM 15.7, "Fake SR" (no self-modification) 15.3.
- The SRWM-over-DeltaNet gap on ProcGen is within one standard deviation.
- Resetting the self-modifications every 50 steps removes the gain: 16.1 (2.2), "similar to those of the baseline without self-modification".

## The new computation, in one equation

    [y_t, k_t, q_t, β_t] = W_{t−1} φ(x_t);   W_t = W_{t−1} + σ(β_t) · W_{t−1}(φ(q_t) − φ(k_t)) ⊗ φ(k_t)

One matrix produces the output, plus its own key, query and learning rate. It then rewrites itself by the delta rule toward a target value that it also retrieves from itself (v_t = W_{t−1}φ(q_t)). Only W_0 is trained by gradient descent. The authors state, "the initial values of the SRWM W0 are the only parameters in this layer which are trained by gradient descent."

What is computed that a DeltaNet does not compute: the map that generates keys and learning rates is itself rewritten, so "SRWMs can potentially learn to even adapt the way it adapts itself".

A property I derive (not stated in the paper), treating β_t as given:

    W_t = W_{t−1} [I + σ(β_t)(φ(q_t) − φ(k_t)) φ(k_t)ᵀ] = W_0 · M_t

M_t is a product of rank-one perturbations of the identity on the input side. This holds for Irie et al.'s Eq. 8. It does not hold for Kirsch & Schmidhuber's variant, which writes ψ(v_t) − ψ(v̄_t) with ψ = tanh. Self-modification therefore never leaves the column space of W_0, and rank(W_t) ≤ rank(W_0). The system can re-coordinate how it reads its inputs, but it cannot create output directions that W_0 lacks.

## New computation or recombination?

Recombination. The parts:
1. **The self-referential weight matrix idea.** Schmidhuber 1992a and 1993a-c. In the original, an RNN with "special input and output units to directly address, read, and modify any of its own current weights through an index for each weight".
2. **Outer-product (key ⊗ value) fast-weight writes.** Schmidhuber 1991 and 1993d. The paper says so: "the use of outer products to parameterise fast weight generation itself is not" modern.
3. **The delta update rule with a generated learning rate.** Schlag, Irie & Schmidhuber 2021 (DeltaNet), after Widrow & Hoff 1960.
4. **A positive normalised φ (softmax) for stable reads and writes.** Schlag et al. 2021.
5. **Multi-head splitting**, as in Transformers.
6. **Collapsing slow and fast nets into one matrix.** This is the paper's contribution.

The project's critique-fast-weights.md already classed delta-rule fast-weight memory (Titans, Schlag) as a recombination. The SRWM adds only self-application of the same update.

Kirsch & Schmidhuber then prove that self-reference adds no representational power. Observation 2.2: for any self-referential architecture "we can find a memory architecture ... such that for any sequence of x1:T" the outputs are equal. Hence "from a representability perspective there is no advantage in self-referential architectures" when initial variables are meta-optimised. Their one change to the learning process is FME:
- Self-modified variants are kept.
- Compute time is allocated "monotonic in their performance".
- No meta-gradient is used.

FME is a selection rule over self-modifications. The authors relate it to portfolio algorithms and the 1997 success-story algorithm. It is not a new forward computation. Its evidence is small: two-armed bandits and a Cartpole policy that "balances the pole for about 100 steps". The authors call the evaluation "still minimalistic".

By the project's test, this is a choice of what writes the weights (the weights themselves), not a new computation. By Kirsch's own argument, it is equivalent to a recurrent net with memory.

## What it suggests for an affective core

1. **Partner influence as a rewrite of the reading map, not a gain on the response.** In an SRWM layer, the partner's input generates the key, query and rate. Those rewrite the matrix that will produce future keys, queries and rates. The partner's effect is therefore a change of profile: a different W, which reads all later input differently. It is not an amplitude on a fixed profile. That is the "profile change" outcome the dial analysis (D75) looks for in people.
2. **A structural guard against copying, if the expressive map is low rank.** By the W_t = W_0 M_t identity, every output stays in col(W_0) whatever the partner does. Partner-driven self-modification can recombine the agent's own expressive directions but cannot add new ones. In the paper this is a weak constraint: W_0 is (d_out + 2d_in + 4) × d_in, so the rank is at most d_in, and the y-part is usually full rank whenever d_out ≤ d_in. It would bind only if the agent's expressive map were deliberately low rank (its own repertoire) and the partner were seen in a higher-dimensional space. This is a design condition, not a property the paper provides.
3. **Where it collapses back into a dial.**
   - σ(β_t) scales every rewrite. In the RL runs all four rates sat in a narrow band: "vary between 0.50 and 0.65 depending on the input". A critic would read the mean write rate as the flat-to-copy dial, as the fast-weights critique did for the write gate.
   - The "learn to adapt how you adapt" claim also contains no satiation. The paper itself warns that "there is no guarantee that the SRWM's self-modifications preserve the original objective function it is trained for".
4. **FME as a different kind of answer.** Kirsch's selection over self-modified copies puts the partner's influence into *which variant of the self runs longer*, not into any weight. That is not a gain on expression. But the fitness signal is a scalar ranking, and if partner approval enters it, the result is selection for flattery: the Principle 6 failure seen in the embodied mortal agent note.

## Verdict

reject as a new core. It is a recombination of the 1992-93 self-referential net and delta-rule fast weights, and Kirsch & Schmidhuber show it matches a memory RNN in function class. Watch the W_t = W_0·M_t structure: partner-driven self-modification that can re-coordinate input but never leave the agent's own output space.
