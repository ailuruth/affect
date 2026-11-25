# Dendritic action potentials and computation in human layer 2/3 cortical neurons (Gidon et al.)

Albert Gidon, Timothy A. Zolnik, Pawel Fidzinski, Felix Bolduan, Athanasia Papoutsi, Panayiota Poirazi, Martin Holtkamp, Imre Vida & Matthew E. Larkum, *Science* 367(6473):83–87, 2020, doi:10.1126/science.aax6239.

**Substitution, stated honestly.** The operator's candidates were Larkum 2013 (*TINS*, "A cellular mechanism for cortical associations") and Poirazi & Papoutsi 2020 (*Nat Rev Neurosci*). Both are paywalled and no author copy was reachable (the Larkum lab page is behind a bot challenge; the NRN review has no open copy). I read instead the author manuscript of Gidon et al. 2020 — Larkum's lab, Poirazi and Papoutsi as co-authors, and the paper that reports a dendritic activation function *unlike* the amplifying one Larkum 2013 is about. Larkum's BAC-firing claim is covered in this cycle by `phillips-2016-apical-amplification-arousal.md`, which I did read in full.

## What was read
The full author's accepted manuscript PDF (49 pages, Zenodo record 3758325, posted by AAAS permission), text-extracted (~9,700 words): abstract, complete main text, all main figure captions (Figs. 1–3), acknowledgements, and the Methods passage giving the dCaAP model equations. Supplementary figures S1–S12 were available only as references in the text, not as images. Numbers below are quoted from the manuscript.

## The computation, precisely

**The finding.** In human L2/3 pyramidal dendrites there is a class of dendritic action potential (dCaAP) whose **amplitude is maximal exactly at threshold and decreases as the input grows**:

> "In contrast to typical 'all-or-none' action potentials, dCaAPs were graded; their amplitudes were maximal for threshold-level stimuli but dampened for stronger stimuli."
> "The dendritic activation function (namely, the amplitude of dCaAPs as a function of the intensity of the current injection in the dendrite, Idend) reached its maximal value at rheobase (i.e. for Idend = Irhe ...) and decayed for stronger Idend".

So the dendritic transfer function is $A(I) \approx A_{\max}\exp\!\big(-(I-I_{\text{rhe}})/(\tau_{\mathrm{dCaAP}} I_{\text{rhe}})\big)$ for $I \ge I_{\text{rhe}}$ and $0$ below, with measured $\tau_{\mathrm{dCaAP}} = 0.39$ (median 0.38) **in units of rheobase**. The soma, for comparison, is the ordinary step: "once a somatic AP was triggered, its amplitude was virtually independent of the input intensity" (exponential fit $\tau_{\mathrm{AP}} = 82$, in units of somatic rheobase — i.e. flat over the tested range).

**The consequence, and it is the point.** Because the function falls, **two input pathways that each drive the dendrite will, together, drive it less**:

> "Due to the activation function of the dCaAPs in our simulation, coincident activation of two synaptic input pathways diminished the dCaAP amplitude ... in contrast to other dendritic APs that amplify coincident dendritic inputs ... Our simulation is therefore a simple and explicit demonstration of how the dendritic mechanism observed in human L2/3 pyramidal neurons computes an **anti-coincident function** for multiple input pathways, limiting the number and/or strength of inputs integrated in the dendrite."
> "We found that the dCaAP's activation function allowed them to effectively compute the XOR operation in the dendrite by suppressing the amplitude of the dCaAP when the input is above the optimal strength."

The proposed cellular algebra: "XOR operation is performed in the dendrites with dCaAPs, whereas AND/OR operations are performed at the soma and tuft/basal dendrites with sodium and NMDA spikes, respectively."

**Inhibition restores, rather than reduces, the dendritic response** — the counter-intuitive structural piece:

> "Inhibition ... placed at the same dendritic subregion (20 GABAergic synapses), in addition to the two excitatory pathways, repolarized the membrane and recovered the amplitude of the dCaAPs ... indicate a counter-intuitive role for inhibition in enhancing the excitability of the dendrite."

**The model, as given in Methods.** dCaAPs were simulated as "sum of current sources with a sigmoidal shape", triggered when $V$ crossed $-36$ mV, with rise/decay sigmoids ($\tau_{\text{rise}} = 3$ ms, $\tau_{\text{decay}} = 0.4$ ms, $\Delta t' = 21$ ms), amplitude ~50–60 mV at threshold, and the suppression factor
$K(v)$ with "$v_{th}$ ... the threshold ($-36$ mV) for dCaAP, $F = 1/(v_{th} - v_{rest})$ ... a normalization factor and $\tau_K$, the dCaAP amplitude decay constant was 0.3 (dimensionless)", refractory period "explicitly set to 200 ms such that dCaAPs fired with 5 Hz or less". (The manuscript's extracted text drops the typeset formulae for $A$, $B$ and $K$; the parameters are as quoted. The NEURON code is at ModelDB 254217 and 260178.)

## Evidence with numbers
- Steady-state attenuation length $\lambda_{\text{steady}} = 195\ \mu$m ($n = 23$); bAP attenuation $\lambda_{\mathrm{bAP}} = 290\ \mu$m ($n = 31$); somata "~850 μm below the pia mater, on average" — so "strong attenuation governs the electrical activity to and from most synapses".
- dCaAP width $4.4 \pm 1.4$ ms (range 2.6–8.0; $n = 32$), amplitude at threshold $43.8 \pm 13.8$ mV (range 13–67; $n = 32$), **independent of distance from soma** ($r^2 = 0.0009$, $n = 28$), unlike the bAP.
- 27 of 39 cells showed trains at $4.6 \pm 1.7$ Hz; 12 showed a single dCaAP.
- Pharmacology: not blocked by TTX 1 μM ($n = 4$); abolished by Cd²⁺ 200 μM ($n = 5$) — hence calcium, not sodium, and not NMDA-dependent.
- Coupling to the soma: 17/37 coupled, with delays 21.6–116.9 ms ($53.8 \pm 26.8$ ms in 11/17); uncoupled cells were more distal ($335 \pm 113$ μm vs $265 \pm 71$ μm, $p = 0.077$, not significant). "Without exception, each coupled dCaAP triggered a single somatic AP" — no bursts, unlike rodent L5.
- The inverted input–output relation was seen in **4 of 12 cells** with repetitive coupled dCaAPs: in the example, $I_{\text{dend}}$ of "260 pA and 275 pA, but neither smaller nor larger current, resulted in somatic APs."
- Activation-function width $\tau_{\mathrm{dCaAP}} = 0.39$ (median 0.38), $n = 12$ dendrites; heterogeneous across dendrites in threshold and width.
- Present in tumour as well as epilepsy tissue ($n = 4$ cells, 3 patients), so "neither regionally confined nor related to pathology".

**Limits to state:** ex vivo human slices from surgical patients; the anti-coincidence/XOR claim is a *simulation* built on a phenomenological fit of the measured activation function, not a measured XOR; the inverted I/O was 4/12 cells.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) a compartmental cable model (**excluded**: linear operator with structure); (ii) a threshold-triggered current (spiking, standard); (iii) a **non-monotone, unimodal** transfer function peaking at its own threshold.

(iii) is the live question. Non-monotone units exist in machine learning (radial basis functions, bump functions, "Mexican hat" tuning, products in sigma-pi units), so a bump activation per se is not new. But three things here are not in the excluded list and not in the twelve sketches recorded in `foundations/designs.md`:

- **The peak sits at the unit's own threshold, which is a property of the mechanism, not a centre parameter.** An RBF has a learned centre $\mu$; here the maximum is *at* $I_{\text{rhe}}$ by construction, and the width is measured in units of $I_{\text{rhe}}$ (0.39), i.e. **scale-free relative to the unit's own threshold**. There is no free centre and no free width in absolute units. That is exactly the shape of invariant the previous reading cycle identified as what makes a mechanism new (`new-mechanisms-synthesis.md` §3: "deleting a free scalar").
- **Summation of two inputs decreases the output.** For any excluded mechanism I can name — attention, Hopfield retrieval, fast weights, SSMs, diffusion, oscillator coupling, structured linear operators — adding a second source of agreement increases or at best saturates the response. Here agreement **cancels**. That is a different sign of the second derivative in the one place this project cares about.
- **Inhibition is restorative, not subtractive, in effect:** adding inhibition recovers the response. Gain-based accounts cannot produce that without a special case.

**Verdict on novelty: yes, with a caveat.** The unimodal-at-own-threshold activation with anti-coincidence is a computation that is not on the excluded list and is not what any of the seventeen designs used. The caveat is that it is an *activation function*, and the project's own novelty test (Q9) warns that a new nonlinearity is the cheapest kind of claim. What raises it above that is the derived peak location and the sign reversal of coincidence.

## What it suggests for an affective core where the partner is structured, not a gain

1. **The dial loses its top end by construction.** Let the route by which the partner's expression reaches the agent's own expressive unit pass through a dCaAP-like unit, so the unit's response to total drive $I = I_{\text{self}} + I_{\text{partner}}$ is $A(I)$, unimodal with peak at $I_{\text{rhe}}$. Then increasing partner drive past the peak **reduces** the response. There is no setting of partner strength that maximises matching: the map from partner strength to matching is not monotone, so "turn it up to copy" is false as a matter of the activation's shape. Relative to Q18, this is a candidate answer that does not require per-channel bounds to be learned: the ceiling is the peak, and the peak is at the unit's own threshold.
2. **"Reading the other through one's own body" becomes an arithmetic fact.** Because $A$ is unimodal in the *sum*, the partner's contribution has an effect that depends on the agent's own current drive with opposite sign on the two sides of the peak: when the agent is quiet ($I_{\text{self}} < I_{\text{rhe}}$) the partner's face *adds*; when the agent is already aroused ($I_{\text{self}} > I_{\text{rhe}}$) the same partner face *subtracts*. One mechanism, one parameterless rule, and it produces a **sign flip with context** — which is item 6 of the open gaps in `foundations/designs.md` ("some responses flip sign") without a learned sign.
3. **Per-channel heterogeneity is measured, not posited.** "L2/3 dendrites were heterogeneous in their activation function threshold and width" — so different expressive channels (mouth, brow, voice) having different thresholds and widths is the biological default, and the shape-not-size requirement of `mimicry-context-synthesis.md` follows from heterogeneity of $I_{\text{rhe}}$ alone.
4. **Inhibition as a re-opener.** If a slow inhibitory term (a need or relationship variable) repolarises the unit, it *restores* the agent's responsiveness rather than muting it: a satiable concern mechanism in which being regulated increases, not decreases, availability to the partner. Worth a closed-form check on the two-variable toy before it is believed.
5. **Falsifiable prediction for the D75 measurement** (research/harness/HARNESS.md): if human listeners' responses to a partner follow an amplifying dendritic rule, response grows with partner intensity; if they follow an anti-coincidence rule, there is an **interior optimum** — the strongest matching occurs at intermediate partner intensity, and very strong partner displays *reduce* matching. That is a curve to measure in Seamless Interaction data, and it is the "measured failure plus derived invariant" pattern the previous cycle says a new mechanism needs.

## Verdict
**adopt (candidate primitive: the unimodal-at-own-threshold anti-coincidence unit).** Evidence is from human slices with small $n$ (4/12 cells for the inverted I/O) and the XOR claim is simulated, so the computation must be treated as a hypothesis with a sharp shape, not an established fact. The shape is the asset: a response that peaks at the unit's own threshold and falls, with a width of 0.39 rheobase and no free centre.
