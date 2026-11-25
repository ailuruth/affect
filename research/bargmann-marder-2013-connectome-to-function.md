# From the connectome to brain function (Bargmann & Marder)

Cornelia I. Bargmann & Eve Marder, *Nature Methods* 10(6):483–490, 2013, doi:10.1038/nmeth.2451.

**Substitution, stated honestly.** The operator's candidate was Bargmann 2012, "Beyond the connectome: how neuromodulators shape neural circuits", *BioEssays* 34(6):458–465, doi:10.1002/bies.201100185. That paper is paywalled (not in PMC, no author copy found; only its abstract was visible: "one ultrastructural connectivity map can encode several circuits, some active and some latent at any given time"). I read instead the 2013 Bargmann & Marder *Nature Methods* historical perspective, which makes the same argument with the same examples, in full. Where a claim below belongs to the 2012 paper I have not read, I do not state it.

## What was read
The full eight-page PDF (a lab-hosted copy at its.caltech.edu), converted to text (~7,300 words), including all figure captions (Figs. 1–5) and the sections "What do functional and anatomical maps reveal?", "Parallel and antagonistic pathways complicate circuits", "Neuromodulation reconfigures circuit properties", "Neuronal dynamics shape the activity of circuits", "Vertebrate retina also has complex circuit properties", "Circuits interact to generate behavior", "How can we 'solve' the brain?". No equations appear in the paper.

## The computation, precisely

The thesis: **one anatomical wiring diagram is a multi-valued object; what computes is a selection from it, and the selector is chemical and dynamical state.** "We believe that anatomical inspection fails because each wiring diagram encodes many possible circuit outcomes."

Three mechanisms of selection are given, each with structure that is not a gain:

1. **Most synapses are not load-bearing for a given behaviour; a few are.**
   - *C. elegans* tail touch: "PLM forms 31 synapses with 11 classes of neurons, but only one of those targets is essential for the behavior — an interneuron called PVC that is connected to PLM by just two gap junctions and two chemical synapses."
   - Head touch: "just two of 58 synapses (again representing gap junctions) are the key link". Fig. 2 caption: the essential synapses "comprise less than 10% of the output synapses of the mechanosensory neurons."
   - "we know what most of the neurons do, we do not know what most of the connections do, we do not know which chemical connections are excitatory or inhibitory, and we cannot easily predict which connections will be important from the wiring diagram."

2. **Divergent parallel subcircuits with opposite signs, selected by channel type (chemical vs electrical).** The ADL sensory neuron: "The chemical synapses drive avoidance of the pheromone, whereas the gap junctions stimulate a pheromone-regulated aggregation behavior ... ADL to switch between these two opposing behaviors in different contexts. ADL illustrates the point that is not possible to 'read' a connectome if it is intrinsically ambiguous, encoding two different behaviors."
   The hub-and-spoke case is the cleanest: multiple sensory neurons gap-junction onto hub RMG; "Neuromodulation of RMG by the neuropeptide receptor NPR-1 effectively silences this gap-junction circuit, while sparing other functions of the input sensory neurons that are mediated through chemical synapses." One peptide **deletes one subcircuit of a shared input and leaves the other intact**. That is selection of a channel, not a volume control.

3. **Degeneracy of the switch itself.** Fig. 3 (a five-cell model from Gutierrez et al., reproduced in the paper): a hub neuron can be moved from firing with the fast pair to firing with the slow pair "by three entirely different circuit mechanisms: changing the strength of the electrical synapses, changing the strength of the synapses between f1 and s1 onto the hub neuron, and changing the strength of the reciprocal inhibitory synapses". The same qualitative reconfiguration has three different parameter routes.

Supporting claims: "the targets of neuromodulation are invisible to the electron microscope"; modulators "change neuronal functions over seconds to minutes, or even hours"; "Every synapse and every neuron in the STG is subject to modulation"; with the dynamic clamp, two STG neurons coupled artificially change their oscillation period dramatically by changing either synaptic strength *or* the single intrinsic current $I_h$ — "a given wiring diagram can produce widely different dynamics with different sets of circuit parameters, and conversely, different circuit mechanisms can give rise to similar oscillation dynamics."
Retinal case (a vertebrate circuit of ~60 cell types): "Subsets of retinal ganglion cells change their weighting of center and surround inputs in a switch-like fashion as light levels change"; "A brief period of visual stimulation can even reverse the apparent direction-selectivity" of some cells; dopamine released around dawn "closes the gap junctions between rod bipolar cells and AII amacrine cells, effectively diminishing rod input", switching cells "from properties appropriate to night vision to day vision."

## Evidence with numbers
*C. elegans*: 302 neurons; crab STG ~27–30 neurons; 31 synapses of which 1 target matters; 2 of 58 synapses; "<10%" of mechanosensory output synapses essential; "over 60% of C. elegans neuron types have defined functions"; "over 100 different neuropeptides" in the worm; retina has ~60 cell types and 20 classes of ganglion cells. Dynamic-clamp and model results are shown as traces only, without tabulated numbers, in the copy read.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) a fixed graph; (ii) a discrete selector over subgraphs; (iii) conductance dynamics; (iv) gap junctions (a symmetric linear coupling) and chemical synapses (asymmetric, sign-carrying) as *two distinct channels between the same pair of cells*; (v) sign-opposed parallel paths.

Honest test. Gating a subgraph is implementable by multiplicative masks, which is a gating network — not new. Parallel opposed paths are a residual-plus-correction structure — not new. The genuinely unusual element, and the one I cannot locate in attention, Hopfield, fast weights, SSMs, diffusion, oscillators or structured linear operators, is **(iv) with (ii)**: *the same ordered pair of units is joined by two channels with different algebra (one symmetric and state-sharing, one directed and signed), and a modulator deletes exactly one of them.* In every excluded mechanism, "how strongly does $i$ influence $j$" is a single scalar (possibly state-dependent); here it is a pair of qualitatively different relations, and the selector chooses the *relation type*, so the influence cannot be moved continuously from one to the other. The sign flip and the per-channel gating that human mimicry shows (research/mimicry-context-synthesis.md) come out of this for free, not by adding a per-expression gain.

**Verdict on novelty: the two-channel-per-edge structure with type-level selection is outside the excluded list; everything else here is a recombination.**

## What it suggests for an affective core where the partner is structured, not a gain

1. **Two relations per expression channel, not one weight.** For each pair (partner feature, own expressive unit) give the core two structurally different couplings: a *symmetric* one (shared state, what gap junctions do: it equalises, and it is what contagion looks like) and a *directed signed* one (evidence about the situation, which can oppose). The relationship is then a **type assignment** over edges, taking values in a finite set, plus the agent's own magnitudes. There is no continuous path from "symmetric only" to "directed only", so a single quantity cannot run the face from flat to copy; the design question becomes which types are reachable.
2. **An invariant to prove:** the symmetric (equalising) channel is only ever available to a *subset* of expressive units fixed at build time (an effector mask of a principled kind, cf. the partner-regulator design's mask, but here forced by the algebra rather than added), and the directed channel never writes magnitudes, only signs and selections.
3. **Deleting a subcircuit is the sharp version of "a neuromodulator switches which circuit computes".** The NPR-1 result is the existence proof the operator asked about: one slow chemical signal silenced a gap-junction circuit while "sparing other functions of the input sensory neurons". In the core: one slow internal variable (need, or relationship state) can make the whole equalising channel vanish, leaving the evidence channel untouched — a *measurable* lesion, and a prediction (contagion disappears while responsiveness to the partner's situation does not).
4. **Most edges should be inert.** <10% of anatomical synapses carried the behaviour. A core with a dense partner→self map is the wrong object; the right one is a dense *potential* map with a sparse active selection, and sparsity of the active set is a quantity to measure, not tune.
5. **Degeneracy of the switch** means the same observable reconfiguration can come from three different internal routes, so behavioural equivalence does not identify mechanism — relevant to this project's evaluation design (research/evaluation.md): a reconfiguration must be verified internally, not only from the face.

## Verdict
**adopt (mechanism: two channel types per edge, type-level selection, subcircuit deletion by a slow signal; plus the <10% sparsity finding).** The paper itself is a review with no equations; its argument that "each wiring diagram encodes many possible circuit outcomes" is the biological statement of the project's Q9 requirement that a partner change *which* computation runs.
