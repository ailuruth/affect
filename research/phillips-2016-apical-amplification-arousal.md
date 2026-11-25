# Convergent evidence for central nervous system arousal regulating apical amplification (Phillips, Larkum, Harley & Silverstein)

W. A. Phillips, M. E. Larkum, C. W. Harley & S. M. Silverstein, "The effects of arousal on apical amplification and conscious state", *Neuroscience of Consciousness* 2016(1):niw015, doi:10.1093/nc/niw015 (PMC5934888).

**Why this paper.** It is the open-access review of exactly the mechanism in the operator's candidate Larkum 2013 (*TINS*, paywalled, lab copy behind a bot challenge — see `gidon-2020-human-dcaap-anticoincidence.md`), written with Larkum as a co-author, and it states the mechanism as a *computational primitive* and names what regulates it.

## What was read
The full PMC author text (~9,700 words): abstract, "Introduction", "Suprathreshold Depolarization of the Apical Integration Zone Amplifies Response to Basal and Perisomatic Inputs", "Adrenergic Arousal Enhances the Effects of Prioritization", "Ih-Currents Regulate AA", "Arousal Regulates Ih-Currents", "Arousal Enhances AA by Reducing Apical Ih-Currents", and the figure captions for Figs. 1–2. I read the later sections on schizophrenia, GANE, Coherent Infomax, anaesthesia and consciousness more quickly — their claims are noted but not relied on here, and the consciousness argument is outside this project's scope (Principle 1–2 territory, and the paper itself is speculative there). No equations appear.

## The computation, precisely

**Apical amplification (AA).** The cell has **two** integration zones, not one:

> "Neocortical pyramidal cells can integrate two classes of input separately and use one to modulate response to the other. Their tuft dendrites are electrotonically separated from basal dendrites and soma by the apical dendrite, and apical hyperpolarization-activated currents (Ih) further isolate subthreshold integration of tuft inputs. When apical depolarization exceeds a threshold, however, it can enhance response to the basal inputs that specify the cell's selective sensitivity."

The two zones carry different kinds of information, by anatomy: "Tuft synapses in layer 1 receive long-range inputs that convey contextual information from diverse feedback, lateral, thalamic, and subcortical sources, whereas the basal and perisomatic inputs receive feed-forward synaptic inputs that specify the cell's receptive-field selectivity."

**The new primitives claimed.** The paper's own framing is that AA is not excitation:

> "apical amplification, together with the disamplifying effects of inhibitory interneurons that specifically target the tuft, provides neurocomputational primitives that can be clearly distinguished from the well-known primitives of excitation, inhibition, and disinhibition"
> "Amplification must be distinguished from somatic excitation because, in the absence of basal/perisomatic depolarization, depolarizing input to the tuft can be strong while having little or no effect on AP generation. Disamplification must be distinguished from basal/perisomatic inhibition because it can be strong without inhibiting AP output. Dis-disamplification must be distinguished from disinhibition because its effects are dependent upon the presence of excitatory input to the apical integration zone."

So the algebra has six interaction types between pyramidal cells (Fig. 2), of which three (amplify, disamplify, dis-disamplify) have **no effect at all when the receiving cell's own basal drive is absent**. Inhibitory interneurons targeting layer 1, "such as Martinotti cells, produce disamplification. They suppress amplification without inhibiting action-potential output."

**What switches the coupling: a leak conductance, not a weight.** This is the part that matters most for this project.

> "Ih-channels reduce the coupling between apical and somatic integration zones by providing a short-circuit that reduces current flow along the dendrite by increasing current flow across the dendritic membrane."
> "This applies only at subthreshold levels of postsynaptic potential, however, because the activation curve for these channels is such that they inactivate with depolarization. This has the consequence that **subthreshold events are processed almost exclusively in their respective compartments (apical or basal) until threshold is reached for a local spike that can then influence the other compartment.**"

Hence the functional form: the inter-compartment coupling $c(V)$ is *small* below threshold and *large* above it, because the shunt itself inactivates with depolarisation. Communication between the two streams is **all-or-none in kind**, not graded in amplitude. And a neuromodulator sets where that boundary sits: "adrenergic arousal regulates Ih and thus the interaction between somatic and apical integration zones"; "arousal enhances AA and regulates conscious state by controlling flow through Ih-channels"; noradrenaline acts via α2a-adrenoreceptors that "colocalize with Ih-currents near the synapse and in the spine neck".

**Both extremes are pathological**, which is an unusually explicit statement of why this is not a dial to be turned up:

> "If the Ih-currents are too strong then there will be little or no communication between the apical and somatic zones. This could lead to incoherent and unregulated responses to sensory input, and thus to high levels of distractibility and uncontrolled impulsive responses."
> "We also assume that Ih-currents can be too weak ... AP output could then be generated by either basal or apical input alone. Consider first the case where APs are generated by apical depolarization alone. This is likely to lead to incoherent unpredictable outcomes because the cell's output will then lose its dependence on the basal input that specifies the cell's selective sensitivity."

And the trade it implements: with low Ih, "AP generation by feedforward basal drive [takes] precedence over relaxation by iterations of AA, and this could be achieved by reducing Ih-currents, which is exactly the effect produced by high levels of NE during stressful situations." Reflective (recurrent, context-sensitive) versus reactive (feedforward) is one conductance.

## Evidence with numbers
- Ih density "increases greatly with distance from the soma along the apical trunk and plateaus at a uniformly high level within the tuft" (Harnett et al. 2015); HCN1 subunits dominate in the apical tree.
- "the distal apical tuft compartment of adult neocortical pyramidal neurons is electrotonically isolated from the basal compartment and has the same input resistance as the much larger cell body" (Zhu 2000).
- Tonic Ih leak shifts resting potential "~10–20 mV unevenly as a function of location such that the tuft dendrite is tonically more depolarized than the cell body"; blocking Ih hyperpolarises the tuft by **17 mV** against **11 mV** at the soma (Berger et al. 2001), "rendering the resulting membrane potential everywhere in the cell the same without Ih-current".
- Developmental: Ih density in distal trunk and tuft "increases 10-fold during the early stages of development" (rat; Atkinson & Williams 2009), so "in young animals (<post-natal day10 in rodents) pyramidal neurons act as compact single-site integrators" and only later become two-zone integrators. **The two-zone structure is grown, not given.**
- Blocking KV channels "enhances the effect of tuft input on AP generation, but has no effect on AP generation by basal inputs alone" (Harnett et al. 2013) — a selective, stream-specific manipulation.
- NE dose asymmetry quoted from the GANE literature: "NE concentrations that mediate LTP effects are an order of magnitude higher than those that mediate LTD effects" (Salgado et al. 2012).

**Limits:** a review, and it says so — "Much of the evidence for AA comes from in vitro studies ... Hypotheses based on in vitro evidence therefore require testing in vivo"; the arousal→Ih→AA chain is assembled from separate literatures, and the paper lists its own reservations. The consciousness claims are not used here.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) two-compartment cable dynamics (**excluded**: linear operator with structure); (ii) a threshold nonlinearity (standard); (iii) a **voltage-inactivating leak that sets the inter-compartment coupling**; (iv) modulatory control of (iii).

Taken as "context multiplies drive", AA is gain modulation and therefore excluded — and this is the honest risk: much of the literature describes AA as a gain increase. What is *not* a gain:

- **The coupling is a function of the state it couples** ($c(V)$, large only above threshold), so the two input streams are **separate objects below threshold and one object above it**. The *number of interacting subsystems* changes with activity. No excluded mechanism has a state-dependent count of subsystems; attention, fast weights and SSMs all keep one coupled system and vary coefficients.
- **Three of the six interaction primitives are identically zero when the receiver's own drive is zero.** That is a *support* constraint, not a small gain: for a cell with no basal input, the map from apical input to output is the zero map for all apical magnitudes.
- **Both too much and too little coupling are failures**, so the quantity is not something a learner should maximise; there is an interior correct value, which is a different optimisation geometry from a gain.

**Verdict on novelty: partly.** The mechanism as implemented is two compartments plus a threshold (recombination). The two properties worth taking — a coupling that inactivates with the variable it couples, and primitives whose support is conditioned on the receiver's own drive — are not on the excluded list.

## What it suggests for an affective core where the partner is structured, not a gain

1. **Put the partner on the apical stream, by construction.** The agent's own body/need signal is the basal stream (it "specifies the cell's selective sensitivity", i.e. *what* is expressed); the partner's face and voice arrive only on the apical stream (context, "which signals are currently relevant"). Then the invariant to prove is immediate and is exactly the brief's Principle 3: **with the agent's own drive at zero, no partner signal of any magnitude produces expression** (the zero map above). Copying requires the partner to set content; on this architecture the partner can never set content, only modulate the agent's own.
2. **The relationship is a coupling conductance that inactivates with the agent's own state.** Let $c = c(x_{\text{self}})$ be large only when the agent's own drive has crossed its own threshold. Then: a calm agent is *structurally* decoupled from the partner (not weakly coupled — decoupled, because subthreshold events "are processed almost exclusively in their respective compartments"); an engaged agent is coupled. The flat-to-copy path now runs through the agent's own activation, so the partner cannot traverse it alone. Worth checking in closed form on a two-variable toy: $\partial(\text{output})/\partial(\text{partner})$ should be identically zero on an open set of agent states, not merely small.
3. **A disamplification primitive gives sign flips and per-channel gating without weights.** An inhibitory interneuron targeting the apical zone "suppresses amplification without inhibiting action-potential output": a slow social variable can remove the partner's purchase on one channel (mouth) while leaving another (brow) and leaving the agent's own expression intact. That is `mimicry-context-synthesis.md`'s per-expression gating as a primitive, not as a learned per-expression scalar.
4. **Reactive versus reflective is one quantity with an interior optimum.** High arousal → low Ih → feedforward dominance (fast reflex, which the brief wants as the innate onset match); low arousal → high Ih → iterated contextual relaxation (slow appraisal). One structural variable produces the documented fast-match-then-context ordering, with the time scales coming from the relaxation dynamics rather than from two hand-set constants.
5. **Development is the right place for the two-zone split.** Ih density rises 10-fold postnatally and the cell *becomes* a two-zone integrator. An affective core could start as a single compartment (the agent's own body only) and grow the apical (social) zone with experience — "learning by living" expressed as a change in the number of integration zones, not in weights.

## Verdict
**adopt (mechanism: two input zones with a coupling that inactivates with the receiver's own drive; disamplification as a primitive).** Evidence is in-vitro and assembled across literatures; the arousal→Ih→AA chain is a hypothesis the authors themselves mark as needing in-vivo tests. Do not use the consciousness framing.
