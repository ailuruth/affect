# Context-dependent computation by recurrent dynamics in prefrontal cortex (Mante, Sussillo, Shenoy & Newsome)

Citation: V. Mante, D. Sussillo, K. V. Shenoy, W. T. Newsome. "Context-dependent computation by recurrent dynamics in prefrontal cortex." *Nature* 503(7474):78–84, 2013. doi:10.1038/nature12742. PMC4121670 (author manuscript).

Source read: the PMC author manuscript, HTML text-extracted. Read in full: abstract, introduction, all Results, Discussion, and the captions of Figs. 1–6 and Extended Data Figs. 1–10 (which carry much of the model analysis). **Not read:** the Supplementary Information (methods, the linearisation and the formal statement that the line attractor and selection vector suffice). Every claim below about the mechanism is from the main text and captions.

## The finding
- **Task.** Two monkeys saw the same random-dot stimuli and, by a context cue, reported either the motion direction or the dominant colour (163,187 trials, monkey A; 123,550, monkey F). 388 single units and 1,014 multi-units from FEF and nearby PFC, analysed as a population.
- **Early selection is absent.** The irrelevant input is *not* filtered before PFC: "irrelevant motion of high coherence … elicits a larger deflection along the motion axis … than relevant motion of intermediate coherence … Yet the former has almost no behavioral effect … while the latter has a large behavioral effect." Inputs are represented along their own axes, separable from the choice axis, in both contexts.
- **Three candidate models are ruled out** (Fig. 3): early gating; context changing the input axis; context changing the choice axis. "The PFC data from monkey A rule out any model of integration for which the degree of overlap between the direction of the momentary evidence and the axis of choice determines how much the corresponding input affects behavior."
- **The trained RNN's mechanism.** Reverse-engineered by fixed points and linearisation:
  - in each context, an approximate **line attractor** (fixed points along the choice axis, one near-zero eigenvalue, all others strongly negative), ending in two stable points; the two contexts' attractors are separated along a context axis and never coexist;
  - a **selection vector**: "the line attractor and the selection vector correspond to the right and left zero-eigenvector of the underlying linear system". An input pulse moves the state off the attractor; the relaxation back "always occurs on a path that is orthogonal to" the selection vector. So the persistent displacement along the attractor is set by the input's projection on the *left* eigenvector, not on the attractor itself;
  - context rotates the selection vector: it "projects strongly onto the relevant input, but is orthogonal to the irrelevant one", consistently along the whole attractor (Fig. 6c, Extended Data Fig. 10q–s).
- "Counter-intuitively, in the model the projection of an input onto the line attractor does not determine the extent to which it is integrated, a manifestation of 'non-normal' dynamics."
- The same left/right-eigenvector mechanism holds in two variants trained differently (with urgency; with an unstable saddle instead of a line attractor).
- Mismatch noted by the authors: input signals are transient in PFC but sustained in the model, suggesting inputs are attenuated after a decision.

## The mathematical object (stated from the captions; derivation mine, standard linear algebra)
Near a marginally stable fixed point, ẋ ≈ A x + B u with A = Σ λ_k r_k l_kᵀ (biorthogonal: l_kᵀ r_j = δ_kj), λ_1 ≈ 0. After a pulse u, the state relaxes to a displacement along r_1 of size l_1ᵀ B u. The instantaneous state change is B u, which may be large and fully decodable. **What is represented (B u) and what persists (l_1ᵀ B u) are set by different vectors.**

## What it means for the design
1. **"Know fully, move only within a limit" has a population-dynamics form.** The partner's face can deflect the agent's latent strongly (so it is known, decodable, available to appraisal and to Claude's processing) while its persistent effect on a slow mode is l_kᵀ b_j for partner channel j. The ceiling per channel is a bound on an overlap, not on a gain applied to the input.
2. **Sign and strength by context, with the input pathway fixed.** Context rotating l is exactly "set per expression by context and relationship, able to flip sign" — and it does so with no change to the input weights, which can stay innate (a shared body map).
3. **The hazard.** If context itself depends on the partner, the partner can rotate the selection vector onto its own channel: a second-order route. The ceiling must bound l(c)ᵀ b_j for every reachable context c, not just at initialisation.
4. **Time scale.** The persistent effect of a sustained input on a mode with eigenvalue −1/τ_k grows as τ_k · l_kᵀ b_j. A per-channel ceiling on the long-time effect therefore forces the partner overlap of a mode to shrink as 1/τ_k: the slowest modes (temperament) must be the hardest to move. This is derived, not in the paper.

## Verdict
- **adopt (the left/right-eigenvector split as the object for "represent vs integrate").** As a model it is a trained RNN linearised around line attractors: an existing framework (linear operators; in eigen-coordinates a diagonal state-space model with a context-dependent input matrix). What it adds is the separation of representation from integration through non-normality, and a precise place to put a per-channel ceiling.
