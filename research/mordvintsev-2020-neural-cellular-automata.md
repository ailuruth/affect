# Mordvintsev, Randazzo, Niklasson & Levin 2020: Growing Neural Cellular Automata

Citation: A. Mordvintsev, E. Randazzo, E. Niklasson, M. Levin. "Growing Neural Cellular Automata: Differentiable Model of Morphogenesis." *Distill*, 11 Feb 2020. doi:10.23915/distill.00023. Text and diagrams CC-BY 4.0.

Source read: the Distill HTML article, read in full as text stripped from the HTML (introduction, Model, Experiments 1-4, Related Work, Discussion, implementation details). The article's results are shown as videos and interactive demos; I saw none of them, only their captions and the surrounding text. The article reports no quantitative regeneration metric, so there are no measured effect sizes to quote. The accompanying Colab notebook was not opened.

## The failure or bottleneck it answered
- The question is biological: "how the cell collective knows what to build and when to stop", and how a target anatomy is stored and restored. The authors cite evidence that "the target morphology is not hard coded by the DNA, but is maintained by a physiological circuit that stores a setpoint for this anatomical homeostasis".
- The engineering gap: CA rules that build a given pattern had been found by hand or by evolutionary search (e.g. J. Miller's French flag). Continuous CAs (SmoothLife, Lenia) produce life-like forms but are not trained to a target.
- The measured failure inside the article is Experiment 1: a rule trained by BPTT to reach the target after 64-96 steps does not hold it. "Some tend to die out, some don't seem to know how to stop growing, but some happen to be almost stable". The fix is the article's main move: "making the target pattern an attractor", by training from a pool of the model's own earlier outputs (Experiment 2) and from damaged states (Experiment 3).

## The new computation, in one equation
Every cell i of a 2-D grid holds a 16-channel state s(i) (RGB, alpha "alive" channel, 12 hidden channels), and every cell runs the same learned rule:

  s_{t+1}(i) = A_t(i) · [ s_t(i) + m_t(i) · f_θ( s_t(i), (K_x ∗ s_t)(i), (K_y ∗ s_t)(i) ) ],  m_t(i) ~ Bernoulli(0.5),  A_t(i) = 1[ max_{3×3 around i} α_t > 0.1 ],

with K_x, K_y fixed Sobel kernels, f_θ a two-layer per-cell network of about 8,000 parameters whose last layer is initialized to zero, and θ trained so that the target is reached and *kept* from seeds, from the model's own intermediate states (a pool of 1,024), and from states with circular regions erased.

What is computed is a **global shape held as an attractor by purely local, asynchronous, identical rules**, with no cell knowing its position or the target. The training procedure, not the update equation, is what makes this a set-point system: the pool trains "how to persist or even improve an already formed pattern", and damage training widens the basin, so that models "exposed to damage during training are much more robust, including to types of damage not experienced in the training process".

## New computation or recombination?
Parts, each with its prior:
1. Cellular automata (von Neumann; Conway; Wolfram), and continuous CA (SmoothLife, Lenia), all cited.
2. Reaction-diffusion as a model of morphogenesis (Turing 1952; Gray-Scott), cited.
3. Fixed gradient perception by Sobel filters: a discretized spatial gradient, i.e. the diffusion-and-gradient sensing of a PDE.
4. A per-cell MLP implemented as 1×1 convolutions (a CNN).
5. A residual update with a zero-initialized last layer, "Inspired by residual neural networks".
6. Asynchronous update as "per-cell dropout".
7. Alive masking by a thresholded max-pool.
8. Backpropagation through time.
9. Sample-pool training, structurally an experience-replay buffer of the model's own states, with the highest-loss sample reseeded.
10. Damage augmentation.
11. CA rules evolved toward target patterns (Miller), and the Neural GPU as "a computational architecture very similar to ours".

The authors themselves say the model "could potentially be named “Recurrent Residual Convolutional Networks with ‘per-pixel’ Dropout”". By the project's test the **update rule is a recombination**. The change of what is computed lies in the **objective and its training distribution**: the rule is trained not to map an input to an output but to make a chosen global configuration an attractor of a local, noisy, decentralized dynamics, with the basin shaped by the perturbations presented. That idea (shape the basin by training on one's own trajectories and on damage) is close to denoising training and to the "what persists, exists" logic of attractor networks, so it is not without prior either. Judged strictly: recombination of parts, with a genuinely different target of computation (a robust distributed set point) shown at small scale and without numbers.

## What it suggests for an affective core
- **Affect as a regenerating morphology, partner as perturbation.** The core could be a field of identical local units whose joint configuration is the affective state (face, voice and body channels as "tissue"). Training on damage makes the agent's own repertoire of configurations attractors. The partner's signal then enters as a *perturbation* the configuration absorbs, partly or wholly, and regenerates from. Influence is measured by which parts of the configuration are reshaped and which regrow, not by a gain.
- **Influence that depends on where it lands.** The article reports that regenerating models are strong "especially in the central area", and that models never trained on damage could instead develop "explosive mitoses (uncontrolled growth), unresponsiveness to damage (overstabilization), or even self destruction". So the response of a trained NCA to a perturbation depends on the location and shape of the perturbation. A partner's expression arriving in different channels or regions of the state would have different, structured effects: a *profile* change with the situation, which is what the project's dial analysis asks a new mechanism to produce.
- **Influence as a change of frame.** Experiment 4 rotates the Sobel kernels and obtains "rotated versions of the pattern for an angle of choosing without retraining". A partner could act on the core's *perception frame* (a group element applied to how cells sense gradients) rather than on its content. The agent's own pattern then appears in an orientation the partner sets: coordinated with the partner, but not a copy of the partner.
- **Where it collapses into a dial.** If the partner is written into the cells every step as an input field, the balance between that drive and the depth of the trained basin is one scalar: weak drive and the pattern regrows its own shape (flat to the partner); strong drive and the pattern is overwritten (copy). The structural versions above avoid this only if the partner enters as damage events, as the location of perturbations, or as a frame, not as a continuous additive input.
- **Set points held by a distributed circuit** match the project's homeostasis principles better than a scalar drive: Levin's point that the set point is a stored, rewritable physiological state suggests that a long-term relationship could rewrite *which* configuration is the attractor (the two-headed planarian), not just scale a response. That is a direction for slow attachment change.
- **Practical.** About 8.3K parameters; trains "in a matter of minutes with a current generation GPU"; a 64×64×16 grid is small enough for CPU. Untested here.

## Verdict: watch (recombination of CA, residual CNN and replay parts; the trained-attractor-plus-damage objective is the transferable idea)
The update rule is a residual convolutional network with per-cell dropout, as the authors say. What it adds is a way to make a global configuration an attractor of local dynamics and to shape its basin by perturbation. For the affective core this suggests partner influence as perturbation, location of perturbation, or change of perceptual frame acting on the agent's own regenerating configuration, each of which changes the profile of the response. A continuous additive partner input would bring back the flat-to-copy dial.
