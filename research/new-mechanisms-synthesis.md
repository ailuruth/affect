# How new computational mechanisms were found, and what that suggests for the affective core

Written 2026-11-25. This synthesis covers 14 notes on 18 primary sources, each read on arXiv or in the authors' PDF; each note says what was read and what was skipped. It is an argument from reading. Nothing here is measured, and the directions at the end are not designs.

Sources:
- **Origins:**
  - [Bahdanau et al. 2014](bahdanau-2014-attention.md)
  - [Vaswani et al. 2017](vaswani-2017-transformer.md)
  - [Hochreiter & Schmidhuber 1997](hochreiter-schmidhuber-1997-lstm.md)
  - [He et al. 2015](he-2016-resnet.md)
  - [HiPPO and S4](gu-2020-2021-hippo-s4.md)
  - [Neural ODEs](chen-2018-neural-odes.md)
  - [Neural Turing Machine](graves-2014-neural-turing-machine.md)
- **Recent:**
  - [AKOrN](miyato-2025-akorn.md)
  - [TTT layers](sun-2024-test-time-training-layers.md)
  - [Neural cellular automata](mordvintsev-2020-neural-cellular-automata.md)
  - [Liquid time-constant networks](hasani-2021-liquid-time-constant.md)
  - [Complex autoencoder and Rotating Features](lowe-2022-2023-complex-autoencoder-rotating-features.md)
  - [Self-referential weight matrix](irie-kirsch-2022-self-referential-weight-matrix.md)
  - [Equilibrium propagation](scellier-bengio-2017-equilibrium-propagation.md)

## 1. The finding that comes first: by the project's parts test, attention is a recombination too

Every source in this set fails the strict novelty test of research/foundations/sketches/v2-README.md (Q9), including the two the operator names as the standard:
- **Bahdanau attention** is Nadaraya-Watson kernel regression with a learned kernel. It also uses a mixture-of-experts softmax gate and Graves's 2013 soft window.
- **The Transformer** is presented by its own authors as a recombination: dot-product attention, self-attention, memory networks, residuals, layer norm and 1×1 convolutions. Its novelty claim is a subtraction.
- **The LSTM**'s parts (a self-loop of weight 1, multiplicative units, truncated gradients) all predate it. **ResNet**'s shortcut is decades old.

A test that only lists parts would have rejected every mechanism the operator wants matched. This does not rescue the twelve sketches: they fail for other reasons (see section 4). But the test needs a second clause that says what *did* make these mechanisms new.

## 2. The pattern: what actually changed each time

The origins share four features. The recent primitives mostly lack the first.

1. **A failure that was measured, or derived, before the mechanism existed.**

   | Source | The failure |
   |---|---|
   | Bahdanau | BLEU falls with sentence length (RNNencdec-50: 17.82 BLEU against RNNsearch-50: 26.75) |
   | LSTM | Error decays exponentially with lag (RTRL 0% at a 10-step lag; LSTM 100% at 100 steps) |
   | ResNet | Deeper plain nets have higher *training* error (plain-34 28.54% against plain-18 27.94%) |
   | NTM | LSTM "rapidly degrades beyond length 20" on copy |
   | HiPPO | Baselines collapse when the sampling rate changes at test time (LMU 6.0%, LegS 88.8%) |
   | EqProp | The contrastive Hebbian objective becomes inconsistent when the two phases settle in different basins |

   Two cases differ:
   - Vaswani's bottleneck was argued from complexity (Table 1), not from a failure curve.
   - Neural ODEs came from taking a limit of ResNet. The failures it fixed were found afterwards.

2. **Before inventing, the obvious explanations were ruled out.** ResNet is the model case:
   - an existence argument: a deeper net can always copy the shallower one;
   - gradient norms measured healthy;
   - three times more iterations tried.

   Only then did it conclude that the solver could not find the identity. The LSTM paper derived the exact factor, f′·w, that had to equal 1.

3. **The fix is an invariant or a definition, and the mechanism is derived from it.**

   | Source | Invariant or definition |
   |---|---|
   | LSTM | ∂s(t)/∂s(t−1) = 1 |
   | ResNet | the default map is the identity: y = F(x) + x |
   | HiPPO | the state *is* the optimal projection of the past under a measure; its ODE is derived; LegS is timescale-equivariant by construction |
   | EqProp | the gradient is the β → 0 tangent of the equilibrium |
   | Bahdanau | the conditioning changes signature from c = q(input) to c_i = f(reader state, stored set) |
   | Neural ODEs | volume change is −tr(∂f/∂z) |

4. **A knob is often removed, not tuned.**
   - ResNet removed highway's gate: "our identity shortcuts are never closed".
   - LegS has no timescale parameter.
   - EqProp divides out the magnitude of its "influence parameter".
   - The Transformer fixes its softmax temperature at 1/√d_k from a variance argument, and removes recurrence.
   - Multi-head attention replaces one averaging route, because "averaging inhibits this" (one head: 24.9 BLEU; eight heads: 25.8).

**Summary:** a new mechanism changed *what is computed*: the signature of the map, the default the optimiser starts from, or the definition of the state. It did not change *how a given computation is parameterised*. And it removed a measured failure by construction, usually by deleting a free scalar.

The recent primitives (AKOrN, TTT, LTC, Rotating Features, SRWM, NCA) are mostly recombinations that scale old ideas:
- TTT is linear attention or self-attention by its own Theorems 1-2.
- LTC is the conductance or shunting neuron.
- Rotating Features is Reichert & Serre's 2014 phase binding.
- The SRWM is Schmidhuber 1992 plus DeltaNet, and Kirsch & Schmidhuber prove it is no more expressive than a memory RNN.
- AKOrN is the vector Kuramoto model plus a Heisenberg field.
- NCA is, in its authors' words, a "Recurrent Residual Convolutional Networks with ‘per-pixel’ Dropout"; what is new is its training objective, not its rule.

None of these started from a measured failure as sharp as the origins' failures. Each still contains one structural idea worth keeping (section 3).

## 3. A proposed second clause for the novelty test

Keep the parts list. Add: *a mechanism counts as new if it changes the signature or the defining invariant of the computation, derives the update from that invariant, and thereby removes a named, measured failure, ideally by deleting a free scalar.* On this clause:
- attention, the CEC, the residual identity, LegS and the EqProp tangent qualify;
- a new key space, a new write gate, a new temperature or a new input definition does not.

The twelve sketches fail both clauses: each kept a free scalar that carries the failure.

## 4. Computation types that are not among the excluded frameworks

The excluded frameworks are active inference, homeostatic RL, optimal control, attention/Hopfield retrieval, fast weights, diffusion, oscillators and linear operators. The types below come from the reading. Each lists its source, what it would bring, and where the dial comes back.

1. **A path that cannot be closed (identity by invariant).** Sources: the LSTM CEC; the ResNet identity shortcut.
   - What it brings: the agent's own continuation is a parameter-free path that no learned or regulated quantity can switch off, and partner input can only add to it. This removes the convex blend (1−g)·self + g·partner, which is the shape of every one-gain sketch.
   - Where the dial returns: a correction F = p − x, which copies the partner, is easy to learn. The partner channel needs a second constraint.
2. **The state defined as an optimum under a measure.** Source: HiPPO.
   - What it brings: the partner's share is a *measure over the past* (a function that need could tilt), not a gain.
   - Caveat: this sits close to "linear operators", and time-invariant forms give only a fixed response profile.
3. **Location addressing: a focus that moves and persists.** Source: the NTM.
   - What it brings: partner signals could emit only addresses and shifts (which of the agent's *own* stored episodes, and in what order or tempo), never content.
   - Where the dial returns: key strength β and sharpening γ.
4. **Linear response of an equilibrium to a vanishing probe.** Source: EqProp.
   - What it brings: the outside world acts as an infinitesimal potential, and what is computed is ds/dβ at β = 0 = −(∂²F/∂s²)⁻¹∂C/∂s. That is the partner's pull filtered through the agent's own inverse curvature: a state-dependent matrix. The fast state stays in the agent's own basin, and the contrast writes to slow parameters.
   - The paper names the dial outright: β runs from free (0) to fully clamped (∞), which is copying (contrastive Hebbian learning).
5. **Divergence-free coupling.** Source: the Neural ODE trace identity.
   - What it brings: a diffusive coupling κ(p − x) has trace −κn on the self-minus-partner coordinates, so the dial *is* a trace. A partner term restricted to zero trace (skew or rotational) adds no contraction toward the partner at any strength.
   - Caveat: it can still contract some directions while expanding others.
6. **Binding channel separate from strength.** Sources: the complex autoencoder and Rotating Features; AKOrN's rotation-invariant readout; the Transformer's rotation-based positional code.
   - What it brings: each feature carries "whose" (an orientation) apart from "how much" (a magnitude). Summation is gated by agreement. Contagion becomes a per-feature alignment event, not a gain.
   - Where the dial returns: binding follows surface similarity, and the fixed ½/½ magnitude mix would become the dial if it were learned.
7. **Selection among the agent's own levels (shunting or conductance).** Source: LTC.
   - What it brings: the state is Σ g_j A_j / (g_L + Σ g_j) over self-owned reversal levels A_j. The partner can drive conductances, but its result is bounded inside the agent's own range. The partner selects; it cannot author.
   - Where the dial returns: the total conductance Σ g_j is a scalar.
8. **Self-modification confined to the agent's own output space.** Source: the SRWM.
   - What it brings: W_t = W_0·M_t, so partner-driven rewrites re-coordinate how input is read but never leave col(W_0). This binds only if the expressive map is deliberately low rank.
9. **Non-reciprocal coupling.** Source: AKOrN's antisymmetric J, and the active-matter work it cites (not read).
   - What it brings: the antisymmetric part produces a chasing regime with a persistent relational lag, which is neither copy nor indifference. Oscillators are excluded, but non-reciprocity is a property of coupling, not of oscillators.
10. **A distributed set point trained as an attractor.** Source: NCA.
    - What it brings: identical local rules hold a global configuration, and training on the model's own past states and on damage widens the basin. The partner could enter as a perturbation the configuration regrows from, as the *place* a perturbation lands, or as a rotation of the perception frame (Experiment 4 rotates the pattern without retraining). Each changes the profile of the response, not a gain.
    - Where the dial returns: a continuous additive partner input, whose strength against basin depth runs from regrowth (flat) to overwrite (copy).
    - Only NTM location addressing and this objective come close to a new computation among the 14 notes; the update rule itself is a recombination.

## 5. Directions for an affective core

These are directions, not designs. Each names what it would compute differently, and where a critic should look for the dial.

**A. The partner as a probe, not a clamp.** Sources: EqProp, with LTC and the SRWM as bounds.
- *The change:* the partner's expression acts on the agent only as a weak potential. What is computed is the agent's own susceptibility, the response of its equilibrium filtered through its own curvature. That response is written into the slow landscape, never directly into the face.
- *Partner influence becomes:* a state-dependent operator, with no single gain.
- *The distinguishing prediction:* the agent yields along its soft directions and not its stiff ones, and which directions are soft changes with need.
- *Where the dial would come back:* any finite β used as an online coupling.

**B. A self path that cannot be closed, plus an invariant on the partner channel.** Sources: the LSTM CEC, the ResNet identity, the Neural ODE trace.
- *The change:* the agent's own dynamics are an ungated identity path. The partner enters only through a term that satisfies a stated invariant: for example zero divergence on the self-minus-partner coordinates, or no access to the agent's own state, so that it cannot synthesise the "cancel myself" term −x.
- *Why it removes the copy end:* copying would then require the agent's *own* flow to contract onto the partner, so the dial has no copy end to turn toward.
- *Test:* the trace of the partner-coupling Jacobian on the difference coordinates, for every candidate.

**C. The partner addresses, the self authors.** Sources: the NTM, LTC, the SRWM, the attention signature.
- *The change:* partner signals emit only selection quantities:
  - which of the agent's own episodes to read;
  - which shift or tempo to move through them at;
  - which of the agent's own conductances to open.
- *What partner signals never supply:* content, meaning the values that end up in expression.
- *The consequence:* the partner changes the *profile* of expression, not its amplitude, which is the outcome the D75 dial analysis asks about.
- *Where the dial would come back:* the retrieval sharpness β and the sharpening γ. Keys must not be computed from the partner's appearance alone.

**D. A binding channel for "whose".** Sources: the complex autoencoder and Rotating Features, AKOrN's readout, NCA's frame rotation.
- *The change:* every affective variable carries an orientation (self or partner, initialised apart) as well as a magnitude, and combinations are gated by agreement.
- *Contagion becomes:* a measurable per-feature alignment that can happen for the mouth and not the brow.
- *Lesion test:* do different feature groups align differently within one situation? If everything aligns together, the scalar is back.

**E. Measure the curve first, then remove a scalar by construction.** This is the historical method.
- The D75 dial analysis in research/harness/HARNESS.md asks whether the partner's influence on human listeners is a gain on a fixed profile or a profile that changes. It plays the role of Bahdanau's BLEU-against-length curve or ResNet's training error against depth.
- Pair it with an existence argument (what a perfect listener model could do) and with explicit elimination of the cheap explanations: delayed copy, smoothing and the REACT mirror baseline.
- Only then state the invariant that makes the measured failure impossible, and derive the mechanism from it.

## Open items

- **Unread primary sources:** Gers et al. 2000 (the forget gate), Mamba (input-dependent selection), the non-reciprocal phase-transition physics behind direction 9, and Reichert & Serre 2014.
- **None of the directions is simulated.** Directions A and B have closed-form checks: for A, susceptibility along the Hessian eigenvectors; for B, the trace on the difference coordinates. Both checks can be run on a two-variable toy before any data is used.
