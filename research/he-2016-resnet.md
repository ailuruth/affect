# He, Zhang, Ren & Sun 2015: Deep Residual Learning for Image Recognition

Citation: K. He, X. Zhang, S. Ren, J. Sun. "Deep Residual Learning for Image Recognition." CVPR 2016. arXiv:1512.03385 (v1, 10 Dec 2015).

Source read: arXiv v1 via text extraction. Read in full: abstract, sections 1-3 (introduction, related work, residual learning, identity shortcuts, architectures, implementation) and section 4.1 (ImageNet, including identity against projection shortcuts). Read in part: section 4.2 (CIFAR-10 setup, Table 6, the 110- and 1202-layer runs). Not read: the layer-response analysis text around Fig. 7 (only its claim in section 3.1), section 4.3 (detection) and the appendices.

## The failure or bottleneck it answered
- The failure was a measured anomaly, and the paper took care to rule out the obvious explanations.
- **The anomaly:** "with the network depth increasing, accuracy gets saturated … and then degrades rapidly. Unexpectedly, such degradation is not caused by overfitting, and adding more layers to a suitably deep model leads to higher *training* error". On ImageNet the plain 34-layer net had 28.54% top-1 validation error against 27.94% for the 18-layer net (Table 2). The 34-layer net "has higher training error throughout the whole training procedure, even though the solution space of the 18-layer plain network is a subspace of that of the 34-layer one."
- **An existence argument showed it was an optimisation failure:** "There exists a solution by construction to the deeper model: the added layers are identity mapping … experiments show that our current solvers on hand are unable to find solutions that are comparably good or better".
- **Vanishing gradients were ruled out by measurement:** the plain nets use batch normalisation, and "We also verify that the backward propagated gradients exhibit healthy norms with BN. So neither forward nor backward signals vanish."
- **More training was ruled out too:** "We have experimented with more training iterations (3×) and still observed the degradation problem".
- The diagnosis: "the solvers might have difficulties in approximating identity mappings by multiple nonlinear layers."

## The new computation, in one equation

  y = F(x, {W_i}) + x

The stacked layers stop computing the mapping H(x) and compute its difference from the identity, F(x) := H(x) − x. Each block now outputs a *correction relative to passing its input on unchanged*. The default, F = 0, is "do nothing" rather than "output zero". The authors' measured consequence: "the learned residual functions in general have small responses, suggesting that identity mappings provide reasonable preconditioning."

## New computation or recombination?
Parts:
1. Shortcut connections. "Practices and theories that lead to shortcut connections … have been studied for a long time", including a linear input-to-output layer in early MLPs.
2. Element-wise addition.
3. Residual reformulation as preconditioning, credited to multigrid and hierarchical-basis solvers and to VLAD-style residual vectors.
4. Concurrent highway networks: the same shortcut, but gated.
5. The identity path is also the LSTM constant error carousel (research/hochreiter-schmidhuber-1997-lstm.md) unrolled over depth instead of time, with the gate fixed open.

So this is a recombination by the parts test. The decisive difference from its nearest neighbour is again a **subtraction**, and the subtraction is of a gain. Highway networks route through gates that "are data-dependent and have parameters … When a gated shortcut is 'closed' (approaching zero), the layers in highway networks represent non-residual functions. On the contrary, our formulation always learns residual functions; our identity shortcuts are never closed, and all information is always passed through". Removing that learnable gain is what the paper's evidence supports:
- "highway networks have not demonstrated accuracy gains with extremely increased depth (e.g., over 100 layers)";
- the 110-layer ResNet reached 6.43% CIFAR-10 test error with 1.7M parameters, against 7.54% (19 layers) and 8.80% (32 layers) for highway nets (Table 6).

Identity, zero-padded and projection shortcuts differed little (ResNet-34 A/B/C: 25.03/24.52/24.19 top-1). "Projection shortcuts are not essential for addressing the degradation problem." The parameter-free identity carries the effect.

## What it suggests for an affective core
- **Remove the gain instead of tuning it.** The structural parallel to the project's dial is close.
  - A highway gate is a learned scalar T(x) that blends "pass the input through" with "replace it": y = T·H(x) + (1−T)·x. Run T from 0 to 1 and the layer goes from pure carry to pure replacement.
  - That is the shape of every one-gain sketch: (1−g)·self + g·partner, which runs from flat to copy.
  - ResNet's answer was to make the carry path unconditional and parameter-free, and let the learned part be only an additive correction.
- **For affect:** the agent's own continuation (its state propagated by its own dynamics) would be an identity path that no learned or regulated quantity can close. The partner would enter only through F(own state, partner) added on top. A convex blend cannot express this.
- **Where it collapses back.** The residual form does *not* make copying impossible. Copying the partner p means H = p, and the residual to learn is F = p − x, which is easy to learn. ResNet makes "keep myself" the default and cheap; it does not forbid "cancel myself and add the partner".
  - The structural answer therefore needs a second constraint on F. For example, F may see the partner only through a channel that cannot carry −x (it has no access to the agent's own state), or its output may be restricted to a subspace.
  - That is a design question, not something the paper answers.
- **Measure the size of the correction.** He et al. measured the layer responses (the standard deviation of F's outputs, Fig. 7) to show the residuals stay small. The affective equivalent is a direct readout: the norm of the partner-driven correction against the norm of the own-dynamics step, measured over time and across partners. One scalar gain predicts a fixed ratio. A structural mechanism predicts a ratio that changes with the situation, which is the D75 profile question.
- **The pattern of discovery:**
  1. a measured anomaly that contradicts an existence argument (a deeper model can always copy the shallower one);
  2. explicit elimination of the standard explanations (overfitting, vanishing gradients, too few iterations);
  3. a reformulation that changes the default the optimiser starts from.

## Verdict
- [Deep residual learning (He et al.)](he-2016-resnet.md) — 2015 — adopt (as pattern) — degradation measured (plain-34 28.54% vs plain-18 27.94% top-1), with vanishing gradients ruled out; the fix removed highway's gain and left the self path parameter-free and never closed; residuals do not stop copying, since F = p − x is easy to learn.
