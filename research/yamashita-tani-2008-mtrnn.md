# Emergence of functional hierarchy in a multiple timescale neural network model: a humanoid robot experiment (Yamashita & Tani)

Citation: Y. Yamashita, J. Tani. "Emergence of Functional Hierarchy in a Multiple Timescale Neural Network Model: A Humanoid Robot Experiment." *PLoS Computational Biology* 4(11), e1000220 (2008). doi:10.1371/journal.pcbi.1000220.

Source read: the journals.plos.org full-text HTML, text-extracted, read in full (abstract, introduction, results, discussion, methods). **Not read:** the numbers inside Table 1 (learning error and success rates per behaviour; an image in the HTML), the equations themselves (images; their roles are described in the text and summarised below), and the robot video.

## What the paper does
- **The question.** In a motor system, how do continuous sensorimotor flows get segmented into reusable primitives, and how are primitives recombined into sequences, without hand-built modules and gating (mixture of experts, MOSAIC)?
- **Network (MTRNN).** A continuous-time RNN of 180 leaky firing-rate units, Euler-integrated at the robot's 150 ms step: u_{t+1} = (1 − 1/τ_i) u_t + (1/τ_i) Σ_j w_ij x_j; context units use a sigmoid, output groups a softmax.
  - 100 input-output units: proprioception (8 joint angles) and vision (2-D object position), each sparsely encoded by a topology-preserving map (8×8 and 6×6), τ = 2;
  - 60 **fast** context units, τ = 5;
  - 20 **slow** context units, τ = 70;
  - **connectivity constraint:** inputs/outputs are never connected to slow units (and proprioception and vision units are not connected to each other). Slow units reach the world only through fast units.
- **Training.** Supervised, offline BPTT (KL loss on the softmax outputs; learning rate 5 × 10⁻⁴; 5000 iterations; 5 seeds) in closed loop on 5 tutored behaviours × 5 object positions (clap at 1 position). Each target behaviour gets an **experimenter-set initial state of the slow units** (chosen to maximise distance between behaviours); fast units always start at 0. A small share of the teacher signal is mixed into the fed-back prediction.
- **Results.**
  - The robot reproduces all behaviours in the physical world and adapts to object position (Table 1, numbers not read; text: "nearly perfectly").
  - **Functional differentiation:** fast-unit PCA trajectories are cycles that shift with object position (primitives, generalised over location); slow units change gradually, carry almost no location information, and "drive switching between movements".
  - **Recombination:** training only slow↔fast weights (everything else frozen) teaches two novel sequences of known primitives; fast-unit trajectories for each primitive are preserved.
  - **Time-scale ratio ablation** (τ_fast fixed at 5): ratios 1 and 2 are significantly worse (p < 0.01, randomisation test) for basic training; ratio 1 much worse for novel-sequence training; ratios above 5 do better. The authors relate the best ratio to total sequence length over primitive length.
- **Mechanism, as the authors explain it.** Fast units cannot hold goal information through branch points, so they mispredict there; this prediction error is what drives slow units to learn dynamics that hold the goal and select branches. Primitives are therefore segmented at branch points. The authors name two other contributors: the goal is injected only as the slow units' initial state, and the slow units are cut off from inputs (a hub/bottleneck, as in Paine's evolved networks). They argue time scales are essential because the ratio-1 network had the same connectivity and initial-state scheme and still failed.

## The mathematical object
**A leaky RNN partitioned by fixed per-unit time constants, with the slowest block cut off from input and output, trained end-to-end on prediction: the slow block becomes whatever the fast block cannot carry across its own horizon.**

## What it means for the engine
1. **What makes a slow variable emerge (stated as mechanism, not tuned constant):** (a) a separation of leak rates; (b) the slow block's only access to the world is through the fast block; (c) a prediction loss with information the fast block cannot hold over its horizon. In the engine's terms: a slow latent block that never reads raw partner features or face channels directly, only the fast block, becomes the carrier of what the fast dynamics cannot keep: episode and goal context. Whether that becomes "mood" depends on what persistent information the training stream contains (see saxena-ba-hafner-2021-clockwork-vae.md for the danger that it becomes session nuisance instead).
2. **Magnitudes still set by rates.** The hierarchy's order comes from τ; its durations are τ = 5 and 70 steps (0.75 s and 10.5 s at 150 ms). This confirms the five-pass lesson: structure gives order, not magnitude.
3. **Slow-only relearning.** Novel sequences were learned by changing only slow↔fast weights. A "regulation by reappraisal" route that only rewrites the slow block (Claude's regulation path) has a precedent here: it recombines existing fast primitives without touching them.
4. **Not from life.** Training is tutored, supervised and offline, with goals set by the experimenter as initial states. Nothing here is learned by living, and the slow initial states are labels in disguise (one per behaviour). The engine could not copy that part (Principle 2): slow initial states would have to be inferred.
5. **Partner route.** A partner who reaches only the fast block still reaches the slow block through it, as it is learned. A design that wanted "the partner cannot write the slow block" would not get it from this constraint; it only removes the direct path.

## Verdict
- **background (mechanism for slow-variable emergence; prior art).** The three conditions above are the clearest statement read so far of why slow variables form. The object is a CTRNN with block time constants (standard; the Clockwork RNN of koutnik-2014 is the discrete cousin already in the index). Not a candidate core.
