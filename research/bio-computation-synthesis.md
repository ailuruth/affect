# What the brain computes for affect and social behaviour that is not on the excluded list

Written 2026-11-26. This synthesis covers 13 notes on 15 primary sources, each read as full text (PMC/Europe PMC author manuscripts, publisher PDFs, or — in one case — a bioRxiv preprint standing in for a paywalled *Cell* paper). Each note states what was read and what was skipped. Two of the operator's candidates could not be obtained and were substituted with full reads of closely related papers, which is recorded in the notes (Larkum 2013 → Gidon et al. 2020 and Phillips et al. 2016, both with Larkum as co-author; Bargmann 2012 *BioEssays* → Bargmann & Marder 2013 *Nature Methods*; Anderson 2016 *Nat Rev Neurosci* was metadata-only everywhere and is **not** covered — its topic is covered by four primary papers from the same lab).

Nothing here is simulated or measured by me. This is an argument from reading, and the directions at the end are not designs.

Sources:
- **Neuromodulation as circuit switching:** [Marder 2012](marder-2012-neuromodulation-switches-circuits.md) · [Bargmann & Marder 2013](bargmann-marder-2013-connectome-to-function.md) · [Froemke & Young 2021](froemke-young-2021-oxytocin-social-salience.md)
- **Dendrites:** [London & Häusser 2005](london-hausser-2005-dendritic-computation.md) · [Gidon et al. 2020](gidon-2020-human-dcaap-anticoincidence.md) · [Phillips, Larkum et al. 2016](phillips-2016-apical-amplification-arousal.md)
- **Hypothalamic persistent states:** [Kennedy et al. 2020](kennedy-2020-stimulus-specific-persistent-state.md) · [Nair et al. 2023](nair-2023-vmhvl-line-attractor.md) · [Vinograd et al. 2024](vinograd-2024-causal-line-attractor.md) · [Mountoufaris et al. 2024](mountoufaris-2024-neuropeptide-line-attractor.md) · [Liu et al. 2024](liu-2024-female-line-attractor-hormone.md) · [Jung et al. 2020](jung-2020-pcd-persistence-network.md) (with Lee et al. 2014 read inside that note)
- **Interoception:** [Chen et al. 2021](chen-2021-interoception-framework.md)

---

## 1. The honest headline: almost none of the *mathematics* is new; several of the *constraints* are

Every model in this set is built from the excluded list. rSLDS — the tool behind all four line-attractor papers — is a bank of linear dynamical systems with a softmax gate: a mixture of experts over SSMs. The spiking models are leaky integrate-and-fire networks with recurrent excitation and global inhibition. The dendritic models are cable equations plus sigmoids. The leaky integrator in flies is one pole. By this project's Q9 parts test, **every one of these papers is a recombination.**

What the biology does supply, and what the previous reading cycle said was the real signature of a new mechanism (`new-mechanisms-synthesis.md` §3: change the signature or defining invariant, derive the update from it, delete a free scalar), is a set of **constraints on how an outside signal may enter a system** — several of which delete a free scalar by construction rather than bounding it. Those are listed in §2. §3 lists what reduces to the excluded list. §4 states the single strongest finding of the cycle.

A second honest point: three papers in this set converge on a pattern the project should take seriously as a *method*, not just a result. In each, the authors tried a gain and showed by measurement that it was the wrong parameter:
- Kennedy et al. 2020: raising excitatory gain preserved stimulus identity but broke the measured autocorrelation; only a 20 s synaptic constant, or structured connectivity, fitted both.
- Vinograd et al. 2024: a fast-synapse attractor needs $\lambda_{\max}$ tuned to within ~$10^{-3}$ of 1; with $\tau_s \approx 20$ s the same network time constants arise "across a wide range of connectivity densities".
- Jung et al. 2020: two opposite-looking behavioural curves (a decline, and a failure to escalate) were fitted with **one** structural leak parameter, with the sensory input constrained equal across all groups.

That is the Bahdanau/ResNet pattern applied to affect, and it is the template for the D75 measurement in `harness/HARNESS.md`.

---

## 2. Candidate primitives that are not on the excluded list

Each is stated precisely enough to be attacked, with the property it would give and where a critic should look for the dial. None is a design.

### P1. The unimodal-at-own-threshold unit (anti-coincidence)
**Statement.** A unit whose response to total drive is $A(I) = A_{\max}\exp\!\big(-(I - I_{\mathrm{rhe}})/(\tau I_{\mathrm{rhe}})\big)$ for $I \ge I_{\mathrm{rhe}}$, and $0$ otherwise: maximal *at its own threshold* and decreasing above it. Measured in human L2/3 dendrites with $\tau = 0.39$ (median 0.38) in units of rheobase; amplitude independent of distance from the soma ($r^2 = 0.0009$) (Gidon et al. 2020).
**Property it would give.** With $I = I_{\text{self}} + I_{\text{partner}}$, the map from partner drive to matching is **not monotone**: past the peak, more partner produces less response. The dial has no copy end, not because of a ceiling parameter but because of the shape of the activation; and the *sign* of the partner's effect flips with the agent's own level of drive (adds when the agent is quiet, subtracts when the agent is already aroused). Per-channel differences follow from heterogeneity of $I_{\mathrm{rhe}}$ alone, giving shape-not-size changes with no per-channel gains. The peak location and width have no free centre: both are defined relative to the unit's own threshold.
**Where the dial could return.** $A_{\max}$ is a magnitude; if it is learned per channel, the scalar is back. The guard is that $A_{\max}$ must belong to the agent's own repertoire and be independent of any partner quantity.
**Status of the evidence.** Human slices, $n = 32$ dendrites for the waveform, but the inverted input–output relation was in **4 of 12 cells**, and the anti-coincidence/XOR claim is simulated from a phenomenological fit. Treat as a hypothesis with a sharp shape.

### P2. Coupling that inactivates with the variable it couples
**Statement.** Two integration zones, A (the agent's own drive) and B (the partner's signal), with inter-zone coupling $c(V)$ supplied by a leak conductance that **inactivates with depolarisation**: $c$ is near zero while either zone is subthreshold, and large once a local spike occurs. Consequence: "subthreshold events are processed almost exclusively in their respective compartments ... until threshold is reached for a local spike that can then influence the other compartment" (Phillips, Larkum et al. 2016).
**Property it would give.** The *number of interacting subsystems* is state-dependent: one system when engaged, two independent systems when not. For an agent at rest, $\partial(\text{output})/\partial(\text{partner}) \equiv 0$ on an open set of states — not small, zero. Combined with the placement rule ("the partner is on zone B, the agent's own need on zone A"), three of the six interaction primitives in that paper are the zero map whenever the agent's own drive is absent. Both too much and too little coupling are failures, so the quantity has an interior correct value and is not something to maximise.
**Where the dial could return.** If $c$ is made a learned function of partner features rather than of the agent's own state, this becomes gain modulation, which is what most of the apical-amplification literature actually describes. The guard: $c$ may depend only on the agent's own variables.
**Evidence.** In-vitro, assembled across literatures; Ih blockade shifts tuft resting potential 17 mV vs 11 mV at the soma; tuft Ih density rises 10-fold postnatally, so the two-zone structure is grown.

### P3. Occlusive convergence: a shared saturable site as the derived ceiling
**Statement.** All modulatory channels — the agent's own and any partner-derived — converge on **one** current through receptors that occlude each other: $g = g_{\max}\,\dfrac{\sum_j c_j}{K + \sum_j c_j}$. Marder 2012 documents five peptides converging on one voltage-dependent current, with the result that "if a neuron is already highly activated by one of these modulatory substances, a second of them will be relatively ineffective"; plus postsynaptic saturation (several-fold synaptic strengthening that does not change rhythm frequency) and a voltage-dependent peptide current with reversal near 0 mV that "increases the amplitude of the oscillations ... without producing a depolarization of the baseline".
**Property it would give.** Three separate ceilings, none of them a parameter: (a) the partner's marginal influence is bounded *by the agent's own concurrent drive* through a shared denominator — no ceiling $\vartheta$ to tune; (b) a coupling of the form $I_p = g_p(\text{partner})(x - E)$ with $E = x_{\text{rest}}$ has **zero** effect at the agent's resting state, so a neutral agent cannot be moved by any partner strength (it can only amplify an oscillation the agent is already producing); (c) saturation of a feedback synapse's effect means strengthening the partner channel past a point changes nothing measurable.
**Where the dial could return.** $g_{\max}$ and $K$ are parameters; but they are *shared across all channels*, so they cannot differentially favour the partner — the thing the critiques kept finding (one scalar from flat to copy on the partner channel) is structurally unavailable.
**Evidence.** All from cited primary work (Swensen & Marder 2000; Golowasch & Marder 1992; Thirumalai et al. 2006), not measured in the review; concentrations nanomolar in hemolymph vs much higher at terminals.

### P4. Two channel types per edge, with type-level selection
**Statement.** Each ordered pair (partner feature, own expressive unit) is joined by two structurally different couplings: a **symmetric, state-sharing** one (gap-junction-like: it equalises) and a **directed, signed** one (chemical-synapse-like: it can oppose). A slow modulator deletes one channel type while sparing the other. Bargmann & Marder 2013: the ADL neuron drives avoidance through its chemical synapses and aggregation through its gap junctions; the peptide receptor NPR-1 "effectively silences this gap-junction circuit, while sparing other functions of the input sensory neurons that are mediated through chemical synapses."
**Property it would give.** "How strongly does the partner influence me" is no longer one scalar but a **type assignment** over edges taking values in a finite set. There is no continuous path from symmetric to directed, so no single quantity runs the face from flat to copy; the design question becomes which type assignments are reachable, and the copy assignment can be excluded at build time. Sign flips and per-channel gating (`mimicry-context-synthesis.md`) fall out of the type algebra rather than from learned per-expression gains. Also, from the same paper: in the worm fewer than 10% of anatomical synapses carried the behaviour, so the right object is a dense *potential* map with a sparse active selection.
**Where the dial could return.** Give each channel a learned magnitude and the scalar reappears inside the type. Guard: types carry fixed, shared magnitudes; only the assignment is learned.

### P5. A persistent state whose position selects the expression mapping (line attractor), with the partner restricted to the input term
**Statement.** A slow one-dimensional manifold in the agent's own latent, approximated by $x_t = A x_{t-1} + b + W u_t$ with one eigenvalue near 1 and all others fast; the partner's acts enter **only** through $u_t$ (discrete events), never through $A$. The expressive readout is a function of *position* in kind: ordered regions of the manifold select different expressive repertoires, each repertoire's amplitude set by the agent's own fast dynamics. Measured: $\tau_1 > 100$ s against $\tau_2 \approx 20$–40 s; line attractor score $\log_2(\tau_1/\tau_2) \approx 1.5$–1.9 when present, ≈ 0 when absent; position progresses sniff → mount → attack (Nair et al. 2023), and in females tracks the animal's own receptivity ($r^2 = 0.62$) rather than the partner's behaviour (Liu et al. 2024).
**Property it would give.** The partner changes *which mapping is in use*, not how loud one mapping is. Four supporting invariants, all measured:
- **finite manifold** — integration "saturated ... after the third pulse", with a finite-length model beating an infinite one ($p < 0.001$); a built-in ceiling rather than a ceiling parameter;
- **off-manifold perturbations return to the current position, not to baseline** — so fast partner events leave nothing, and only input with a component along the slow direction changes the episode;
- **ramp and decay are separately owned** — decay correlates with the agent's own functional connectivity ($R^2 = 0.87$, $n=8$) while ramp rate does not ($r^2 = 0.01$), i.e. the partner can set the rate of climb and nothing else; the invariant to prove is $\partial\tau/\partial(\text{partner}) \equiv 0$;
- **temperament is one eigenvalue** — the leading time constant predicts aggressiveness across animals ($r^2 = 0.77$, $n = 14$).
**Where the dial could return.** $W$ is a gain on the partner's events. The guard is the ramp/decay dissociation plus the finite manifold: a bounded manifold with the agent owning $A$ means larger $W$ moves the state faster to the same ceiling, which is a different object from "more copying" — and that is a closed-form check, not an assertion.
**Status.** This is a continuous attractor, which is classical mathematics and *not* new; what is outside the excluded list is the role (position selects the mapping) and the input/dynamics separation.

### P6. A slow channel that decides whether the persistent state exists at all (topology switch)
**Statement.** Put a second synaptic channel with timescale $\tau_s \approx 20$ s on the **same** weight matrix as the fast channel, with strength $\alpha$ set by a slow social/physiological variable. Then $\tau_n \approx \tau_s/(1-\lambda_{\max}(\alpha W))$, and lowering $\alpha$ moves the system from a **line attractor** to a **point attractor** — a bifurcation, not a reduction in amplitude.
**Evidence, and it is the cleanest dissociation in the cycle.** Disrupting oxytocin and vasopressin receptors in the attractor's own cells left the content intact — intruder-sex and behaviour decoders stayed at "virtually 100%" accuracy in both groups — while the line attractor score fell from ~1.5 to ~0, τ fell from ~100–120 s to <50 s, single-cell autocorrelation half-width fell from 28.6 ± 1.23 s to 9.86 ± 1 s, and the ramp-and-hold profile became a "sawtooth" (Mountoufaris et al. 2024, read as preprint). Independently, in females the same switch is thrown by hormonal state over days with **no change in mean activity**: line attractor score 1.9 ± 0.2 (receptive) vs 0.05 ± 0.02 (unreceptive), carried by a 39 ± 5% subpopulation whose autocorrelation half-width changed (25.2 vs 16.1 s) while non-contributing cells did not (Liu et al. 2024).
**Property it would give.** The social variable controls *whether the agent has an episode-level memory*, while leaving the agent's instantaneous expressive content untouched (decoders unchanged) — so it cannot be used to copy. It is lesionable and measurable with one number ($\log_2(\tau_1/\tau_2)$). Because the slow channel shares the fast channel's weight matrix, **no setting of $\alpha$ can introduce a direction absent from $W$'s spectrum**: the partner can only make the agent persist along the agent's own existing directions. That is "reading the other through one's own body" as an algebraic statement, and it is free.
**Where the dial could return.** $\alpha$ is a scalar. But it is a scalar on *persistence*, not on *expression*, and the two measured dissociations say those are separable parameters. A critique should attack exactly this: show whether moving $\alpha$ can produce copying through any route.
**Also:** slow transmission deletes a tuning parameter. With $\tau_s = 0.1$ s, $\lambda_{\max}$ must sit within ~$10^{-3}$ of 1; with $\tau_s = 20$ s, $\lambda_{\max} \approx 0.6$–0.9 suffices. The knife-edge becomes a basin.

### P7. Persistence as a loop property with no write port
**Statement.** The persistent variable exists only as a property of a recurrent loop, so no single unit — and therefore no external signal addressed to a unit — can set it. Measured: direct stimulation of the candidate node gave $\tau \approx 13.4$ s, whereas indirect, network-driven activation gave $\tau \approx 83$ s; transient inhibition of the node during the decay phase caused a ~68% drop with **no recovery** (while a neighbouring population recovered fully), so the node is inside the loop (Jung et al. 2020). The mammalian analogue: holographic stimulation of five on-manifold cells moved the state along the manifold, but the manifold itself was the network's (Vinograd et al. 2024).
**Property it would give.** "The partner cannot author the state" becomes a structural fact rather than a constraint to enforce: there is no variable to write. The partner can only perturb the loop's input.
**Where the dial could return.** Nowhere obvious, which is why this is worth developing; the risk is instead that the loop is hard to keep stable without tuning — which is what P6's slow channel buys.

### P8. State changes the agent's own input sensitivity, not its output amplitude
**Statement.** The persistent state multiplies the agent's **perceptual** sensitivities. Measured: after the state was induced, the fraction of cells responsive to an aggression-promoting pheromone rose from 50% to 90%, with peak responses ×1.8 (median) (Jung et al. 2020). The oxytocin review's second-order mode is the same shape from the other side: tonic (self-generated) activity down and evoked (stimulus-driven) response up in one move, i.e. a change of **ratio** with the mean roughly unchanged (Froemke & Young 2021).
**Property it would give.** Partner influence that changes *what the agent can notice next*, with the output map untouched. The observable is a signal-to-noise change, not a bigger face. Reaches expression only through the agent's own appraisal, which is Principle 3 by construction.
**Where the dial could return.** A uniform sensitivity scale is a gain. The guard is that sensitivity changes must be channel-specific and must be accompanied by the tonic-down half (a ratio, not a level).

### P9. The modulator as a write-enable that is afterwards dispensable
**Statement.** The social signal gates whether the current episode is **written to slow parameters**, and does not specify what is written or how much is expressed now. Measured: oxytocin transiently suppressed evoked inhibition, allowing LTP within minutes, after which "blocking cortical oxytocin receptors did not substantially affect pup retrieval abilities" (Froemke & Young 2021).
**Property it would give.** The partner's influence on the agent's face at time $t$ is identically zero; all of its influence is on what the agent becomes. The dial is removed from the expressive path by construction, and the design makes a falsifiable prediction (dispensability after the window).
**Where the dial could return.** A learning-rate scalar is a gain on plasticity; three-factor learning rules are an existing mechanism. The novelty, if any, is in P10.

### P10. Influence as a receptor map over subsystems, not a coefficient
**Statement.** A modulator's effect is determined by **which** of the agent's subsystems express its receptor — a slow, discrete, learned/structural map — and not by its level. Measured consequences: the same peptide suppresses one dopaminergic nucleus and boosts another because only one expresses the receptor on its principal cells, "biasing overall activity away from substantia nigra and toward VTA"; the same peptide raises signal and lowers noise in CA1 because the receptor is on interneurons, while in CA2 it changes the firing *mode* of principal cells (burst versus tonic); individual animals differ genetically in receptor density and that difference determines whether early neglect disrupts adult bonding (Froemke & Young 2021). Marder 2012 generalises it: electrically coupled neurons "could respond differently to the same modulatory substance", and dopamine modulates several currents in one neuron and "the same current ... differently in different target neurons".
**Property it would give.** The dial factorises into (bounded level) × (discrete map). Changing the level cannot change which computation is favoured; changing the map can. Per-channel gating, sign flips, partner-specific patterns and individual differences all live in the map, with no per-channel scalars. Two agents with identical circuits and identical social-variable levels compute differently if their maps differ.
**Where the dial could return.** If the map is dense and continuous it is just a weight matrix. The guard is sparsity and type-level (not magnitude-level) entries — which connects it to P4.

### P11. The partner as an address, not an amplitude (place-not-strength inhibition)
**Statement.** The partner channel has no access to magnitudes; it may only **place** a divisive (shunting) term at a location in the agent's own expressive tree. A shunt's effect is additive when far from the excitation and strongly divisive when on the path between that excitation and the output (London & Häusser 2005, after Rall).
**Property it would give.** A checkable containment result: a divisive term on the path from subtree $S$ to the output can only shrink $S$'s contribution toward zero, so the reachable set of outputs is contained in the convex hull of the agent's own outputs with subsets of subtrees silenced. **Copying is outside that image**, because shunting cannot synthesise a value the agent does not already produce. Partner influence is characterised by a finite, enumerable set of placements.
**Where the dial could return.** Shunt strength. The guard is that strength is fixed by the agent and only placement is partner-driven.

### P12. The persistent state as a *position*, not a magnitude (bistable front)
**Statement.** A bistable field on a line, with an up-state at one end and a down-state at the other, holds a standing front; incoming transients reposition the front, and in the absence of input the front stays. "The location of the wavefront represents the result of the integral such that incoming transient synaptic input repositions the location of the front ... the dendrite will preserve the 'working memory'", with persistence "far longer than its intrinsic time constant" (London & Häusser 2005, reporting Loewenstein & Sompolinsky 2003).
**Property it would give.** Persistence from structure (bistability), not from a tuned leak — which is the brief's "time scales from structure" requirement in its strongest form. It is the same object P5 arrives at from population recordings, but with a mechanism that does not require an eigenvalue near 1 at all. The state variable is a location; "how much" is not a property of it.
**Where the dial could return.** The input's displacement per event is a scalar. The front's range is finite, so as in P5 a larger displacement moves the state faster to the same ends.

---

## 3. What reduces to the excluded list (and should not be claimed as new)

| Mechanism in these sources | Reduces to |
|---|---|
| rSLDS / switching linear dynamical systems (all four line-attractor papers) | mixture of experts over **SSMs**; linear operators with structure |
| Leaky integration, the integration dimension, "ramp to threshold" | **SSM** (one pole); value/threshold readout |
| Leaky-bucket drive model $\dot r = -r/\tau + I$ (flies) | **SSM**; the same equation as homeostatic-RL drive |
| Recurrent excitation + global feedback inhibition (ISN) in all spiking models | **recurrent networks** |
| Two synaptic timescales on one weight matrix | **SSM** with two poles per channel |
| Continuous / line / point attractors as such | classical attractor dynamics (**energy models**, Hopfield-adjacent) |
| Cable equation, passive dendritic filtering, electrotonic compartments | **linear operators with structure** |
| Sigmoidal dendritic subunits summed at the soma ("two-layer network in one neuron") | an **MLP**; the authors say so |
| Divisive shunting as such | **gain / normalisation** |
| Dendritic coincidence detection, NMDA spikes, BAC firing as amplification | **multiplication / AND**; gain modulation |
| Oxytocin as "social salience", signal-to-noise, first-order depolarisation | **gain** — and the review itself says first-order modulation "enhanc[es] all inputs ... at the cost of discriminating between similar signals" |
| Plasticity gating by a third factor (write-enable, as a bare rule) | **fast weights** / three-factor learning |
| Interoception as ascending sensing + central integration + descending regulation (Chen et al. 2021) | **active inference / optimal control**; no computation is stated, and the paper concedes the affect link is "mostly unknown" |
| Modulator as parameter scheduling over a fixed graph (Marder, read as dynamics) | input-dependent **SSM** coefficients (Mamba-style selection); already recorded as a recombination in `foundations/designs.md` |

A further caution for designs: **P1 is an activation function**, and Q9 warns that a new nonlinearity is the cheapest novelty claim. What lifts it above that is the derived peak location (at the unit's own threshold, width measured in units of rheobase) and the sign reversal of coincidence — not the bump itself.

---

## 4. The single strongest finding of this cycle

> **A slow chemical variable can decide *whether a persistent state exists*, while leaving the instantaneous content of the population code untouched.**

Two independent demonstrations, different causes, different timescales, same dissociation:
- Oxytocin/vasopressin receptor disruption in the attractor's own cells: content decoders at ~100% in both groups; line attractor score 1.5 → ~0; τ 100–120 s → <50 s; single-cell persistence 28.6 → 9.86 s (Mountoufaris et al. 2024).
- Hormonal state across the oestrous cycle: **no change in mean population activity**; line attractor score 1.9 → 0.05; a 39 ± 5% subpopulation changes its time constants and nothing else does; ovariectomy removes the attractor and hormone priming restores it (Liu et al. 2024).

This is the operator's question answered in the affirmative by measurement: a neuromodulator *can* switch which circuit computes rather than scaling one, and the switch is a bifurcation in the topology of the flow (line attractor → point attractor), not a change of gain. It is the one place in this reading where "structured, not a gain" is a measured fact rather than a design aspiration, and it comes with a one-number diagnostic — $\log_2(\tau_1/\tau_2)$ — that can be computed on any candidate core's fitted latent dynamics.

---

## 5. Directions (not designs), with where a critic should look

**A. Topology switch + input/dynamics separation (P6 + P5 + P7).** The agent owns $A$ (its own recurrent structure, hence its persistence and its temperament); the partner owns only $u_t$ (discrete perceived events) through a fixed $W$; a slow social/need variable $\alpha$ sets whether the slow manifold exists at all, by scaling a 20 s channel on the same $W$ that carries the fast dynamics. Invariants to prove: (i) $\partial\tau/\partial(\text{partner}) \equiv 0$; (ii) no $\alpha$ introduces a direction outside $\mathrm{spec}(W)$; (iii) the manifold is finite. Diagnostics: the line attractor score; the ramp/decay dissociation; off-manifold return. **Critic's target:** whether any route from $\alpha$ or $W$ to the expressive readout can produce copying; and whether a bounded manifold with a larger $W$ is genuinely a different object from a larger gain.

**B. Anti-coincidence on the partner's route (P1 + P2).** The partner's signal reaches the expressive path only through units that are unimodal at their own threshold, and only when the agent's own drive is already above its own threshold (the coupling inactivates otherwise). Predicted signature: an **interior optimum** — matching is strongest at intermediate partner intensity and *falls* for very strong partner displays — and a sign flip with the agent's own arousal. **Critic's target:** $A_{\max}$, and whether heterogeneity of thresholds is learned from partner data (in which case the per-channel dial is back).

**C. Occlusion and reversal potential as the entry law (P3).** Every modulatory channel, own and partner-derived, shares one saturable site, and the partner's coupling has its reversal at the agent's resting state. Then: a neutral agent is immovable, and an already-driven agent is nearly saturated. **Critic's target:** whether the shared-denominator form survives when the agent's own drive is near zero but non-zero, i.e. the small-signal regime.

**D. Address-and-type, never content (P4 + P10 + P11).** The partner emits only (i) a type assignment over a sparse set of edges, and (ii) placements of divisive terms in the agent's own tree. No partner-derived quantity multiplies an expressive magnitude. Containment result to prove: the reachable output set is the convex hull of the agent's own outputs under subtree silencing, which excludes the copy point. **Critic's target:** whether types are really finite in the implementation, or become continuous once learned.

**E. Write-enable only (P9 + P8).** The partner's influence at time $t$ on the face is identically zero; it gates what is written to slow parameters and what the agent can perceive next. Falsifiable: after the learning window, removing the social signal leaves behaviour unchanged (the dispensability result). **Critic's target:** whether the learning-rate gate is just a fast-weight write gain, which Q9 excludes.

**F. Measure first, then delete a scalar.** Before any of the above, run the pattern all three strong papers in this set used: pick two statistics that a gain and a structural change fit *differently* (Kennedy's autocorrelation-versus-lag and cross-stimulus correlation are a ready-made pair), measure them on human dyadic data, and show which parameter the data require. The strongest available discriminating prediction is in direction B: a gain model says response rises monotonically with partner intensity; an anti-coincidence model says there is an interior optimum.

## 6. Open items

- **Anderson 2016** (*Nat Rev Neurosci* 17:692–704), the operator's named review on circuit modules linking internal states to social behaviour, is metadata-only at Caltech and paywalled at Nature; it was **not read**. Its content is covered here by five primary papers from the same lab, but the review's own framing of "scalable and persistent internal states" is unverified.
- **Bargmann 2012** (*BioEssays*) and **Larkum 2013** (*TINS*) and **Poirazi & Papoutsi 2020** (*Nat Rev Neurosci*) were paywalled; substitutes were read in full and are named in the notes.
- **Mountoufaris et al. 2024** was read as the 2023 bioRxiv preprint; the numbers must be re-checked against *Cell* 187:5998–6015 before a design cites them.
- **Nothing here is simulated.** Three directions have closed-form checks runnable on a two-variable toy before any data: (A) the Jacobian of the partner coupling with respect to $\tau$; (B) the sign of $\partial A/\partial I_{\text{partner}}$ either side of the peak; (C) the small-signal limit of the occlusion form.
- **Unread primary sources behind claims used here:** Swensen & Marder 2000 (occlusion), Golowasch & Marder 1992 (voltage-dependent peptide current), Loewenstein & Sompolinsky 2003 (bistable front), Berger et al. 2001/2003 (Ih and coupling), Carcea et al. 2019 (oxytocin neurons learning a social receptive field), Harnett et al. 2013/2015 (Ih and KV in the tuft). Each is cited in a note and none was read.
- **Principle 6 warning carried forward.** Liu et al. 2024 is a receptivity variable driven by a partner's contact, and Froemke & Young 2021 is explicit that the salience modulator raises agonistic as well as prosocial behaviour. Nothing in this cycle licenses a Bot variable that escalates with user attention; the transferable abstraction is the topology switch, not the drive it implements in mice.
