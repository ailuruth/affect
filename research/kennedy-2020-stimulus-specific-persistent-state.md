# Stimulus-specific hypothalamic encoding of a persistent defensive state (Kennedy et al.)

Ann Kennedy, Prabhat S. Kunwar, Ling-yun Li, Stefanos Stagkourakis, Daniel A. Wagenaar & David J. Anderson, *Nature* 586(7831):730–734, 2020, doi:10.1038/s41586-020-2728-4 (PMC7606611, author manuscript).

## What was read
The full NIH author manuscript (fetched as JATS XML from NCBI, ~11,000 words): summary, complete main text, and the Methods, including the four model classes in "Slow neuromodulation model", "Spiking recurrent neural network model + NMDA", "Spiking recurrent neural network model + slow excitation (sRNN)" and the locally-connected variant. Figures were seen only as captions/Methods text. I did not read the Extended Data figures as images.

## The computation, precisely

**The claim.** A persistent internal state in VMHdm$^{SF1}$ neurons is implemented by population dynamics that keep **both** a slowly decaying amplitude **and** the identity of the stimulus that caused it:

> "in response to naturalistic threatening stimuli, VMHdmSF1 neurons exhibit persistent activity lasting many tens of seconds ... Unexpectedly, distinct but overlapping VMHdmSF1 subpopulations were persistently activated by different modalities of threatening stimuli. Computational modeling suggests that neither recurrent excitation nor slow-acting neuromodulators alone can account for persistent activity that maintains stimulus identity."

So the computation is not "an integrator holding a scalar". It is: **a decaying trajectory in a high-dimensional space whose direction encodes which stimulus occurred, and whose magnitude decays over tens of seconds**, with the stimulus still decodable after the stimulus is gone.

> "the slow decay of the population response reflects a diverse, time-evolving pattern of activity among individual cells."
> "stimulus identity also remained decodable for tens of seconds after stimulus onset ... the VMHdmSF1 population response can persistently encode the identity of the presented stimulus, even after stimulus removal."

**The model comparison is the valuable part, and it is a negative result stated precisely.** Four model classes were fit against two measured features — the autocorrelation of population activity as a function of lag $|t-t'|$ over a 45 s window, and the time-evolving Pearson correlation between rat-evoked and ultrasonic-sweep-evoked activity (the stimulus-specificity measure):

- **Peptide-only (no recurrence):** $N = 1000$ neurons, 10% receive peptidergic input per stimulus, $r_i(t) = g\,p_i(t)$, $g \sim U(0,60)$, with $\tau_p \,\mathrm{d}p_i/\mathrm{d}t = -p_i(t) + \delta(t)$ and $\tau_p = 25$ s "set to match the observed decay time constant of the population average". **Failed** the autocorrelation structure.
- **Recurrent + NMDA only:** also **failed**.
- **sRNN (recurrent excitation + fast feedback inhibition + slow excitation):** membrane dynamics given explicitly as
  $\tau_m \,\mathrm{d}x_i/\mathrm{d}t = -x_i + g\sum_j J_{ij} p^{\text{fast}}_j(t) + g\sum_j J_{ij} p^{\text{slow}}_j(t) - g_{\text{inh}} I_{\text{inh}}(t) + w_i s(t)$,
  with "the synaptic weight matrix J was the same for both fast and slow components of excitation", and three variants: "in the 'low gain' model, g = 1, ginh = 8.8, τEslow = 6 sec; in the 'high gain' model, g = 6, ginh = 7.8, τEslow = 6 sec; in the 'high τS' model, g = 2.5, ginh = 4.25, τEslow = 20 sec".
- **sRNN + distance-dependent connectivity:** $p_{ij} = p_0 e^{-|i-j|^2/\sigma}$, $p_0 = 0.1$, with "a mild spatial bias ... on stimulus-specific inputs": "the middle 50% of model neurons in the band could receive input from both rat and USS stimuli, while the outermost 25% could only receive rat or USS input".

The decisive result: **raising the gain of excitation can preserve stimulus identity but then breaks the measured temporal dynamics; only two models satisfy both constraints** —

> "Maintaining stimulus specific representations during persistence could be achieved in the sRNN by increasing the gain (strength) of excitatory synapses ... but such models failed to match the autocorrelation dynamics of observed activity. However, both temporal dynamics and stimulus specificity could be matched by one of two models: in the first, the synaptic time constant was increased to 20 seconds; in the second, connectivity between neuron pairs decreased slightly with distance, and a mild spatial bias was imposed on stimulus-specific inputs ... only two models satisfied both conditions."

In other words: *gain is the wrong knob; a slow time constant (20 s) or a spatial structure in connectivity is required.* That is a measured elimination of a gain, which is the pattern `new-mechanisms-synthesis.md` identifies as how new mechanisms were found.

Also stated: unlike a hormone, this persistence is addressed — "Unlike circulating hormones, however, persistent activity in VMHdmSF1 neurons is stimulus-specific, preventing over-generalization of defensive responses."

## Evidence with numbers
- Photometry after a 10 s rat presentation: activity "persisted for over a minute following rat removal (time constant τdecay = 26.7 ± 2.2 seconds)"; a toy rat "evoked a weaker and shorter response".
- Open-field assay: 15 s rat exposure produced thigmotaxis "lasting minutes"; introducing the mouse *after* the rat ruled out lingering odour.
- Optogenetic silencing (iC++) before rat exposure "prevented the increase in thigmotaxis"; silencing started after rat removal let thigmotaxis rise then return "to baseline faster than in controls" — so "ongoing VMHdmSF1 neuronal activity is essential for maintaining a persistent defensive response".
- Blocking transmitter release from these cells (TetTox) gave "significantly faster bulk calcium decay kinetics than control ... while the peak response was not affected" — persistence is network-dependent, the response is not.
- Imaging: $n=5$ mice, $187.3 \pm 8.1$ cells/day, 78 cells tracked across days; among cells responding to ≥1 stimulus (74.4%), "43.6% responded to only one, and over 70% responded to ≤ 2 of the five tested stimuli".
- A 5-way naive Bayes decoder predicted stimulus identity above chance across three days.
- Ex vivo: mono- and di-synaptic glutamatergic connectivity among these neurons; single-cell stimulation activated multiple follower cells.
- Cell-biological grounding for the slow component: "VMHdmSF1 neurons express almost 40 neuropeptides as well as 115 GPCRs".
- Timescale framing: "orders of magnitude longer than that supporting working memory in the cortex".

**Limits stated by the authors:** alternatives such as astrocytic K⁺ clearance are not excluded; feedback from downstream targets is not excluded; all experiments in males (sex differences and oestrous cycle explicitly set aside).

## Is this a new computation relative to the excluded frameworks?

Parts: (i) leaky integrate-and-fire neurons; (ii) recurrent excitation with global feedback inhibition (an inhibition-stabilised network — standard); (iii) a second, slow synaptic channel sharing the same weight matrix $J$; (iv) distance-dependent connectivity; (v) stimulus-specific input bias.

(i)–(ii) are a recurrent network: **excluded**. (iv)–(v) are architecture, not computation. (iii) is the interesting one: **two synaptic channels with the same connectivity but different time constants (0.1 s and 6–20 s)**, so the *same* graph transmits a fast and a slow copy of every signal. That is multiplexing two timescales on one weight matrix rather than two weight matrices — and it was *required* by the data, since gain variants failed.

Still, honestly: two filters on one weight matrix is within the reach of an SSM with two poles per channel, which is excluded. The thing that is not a recombination is the **finding**, not the model:

> **A gain increase and a slow time constant are not interchangeable: they fit different, measurable features. Gain restored content, only the 20 s constant restored dynamics.**

That is the empirical statement this project needs to break the dial: it says that in biology, "how much" and "what is preserved" are carried by different parameters, and no setting of the gain buys what the slow channel buys.

## What it suggests for an affective core where the partner is structured, not a gain

1. **Persistence must carry identity, and that forbids a scalar arousal.** The core's persistent affective state should be a *direction plus magnitude*, where the direction says what happened (which partner, which event, which channel) and the magnitude decays. Reset the direction and the agent is not merely calmer: it has forgotten what it is in a state *about*. This gives a concrete lesion to run (shuffle the direction, keep the magnitude) and a concrete prediction: carry-over with a returning partner should be stimulus-specific, which is one of the measured failures named in Q9.
2. **The 20 s constant comes from the chemistry, not from a hyperparameter.** Peptide/GPCR transmission supplies a ~20 s synaptic time constant on the same connectivity. In the core this is a second read of the *same* learned structure at a different timescale — no new partner-specific parameters, and the slow channel is what makes a state outlast an event.
3. **But a slow channel alone cannot do it.** The peptide-only model failed; recurrence plus fast inhibition was needed to hold identity. For the core: a slow social variable on its own cannot produce a persistent affective state; it has to act on a recurrent structure that is already holding the agent's own pattern. This is an argument against designs where the partner's influence is purely a slow scalar added on top.
4. **Over-generalisation is the failure to design against.** The authors' phrase — persistence is stimulus-specific, "preventing over-generalization of defensive responses" — is the affective analogue of the project's Principle-6 worry. A core whose persistent state is one scalar will generalise the last partner's effect to everyone; one whose state is a direction will not.
5. **The method is the template.** Two measured statistics (autocorrelation versus lag; cross-stimulus correlation versus time) were used to *eliminate* gain as the explanation. The same pair of statistics can be computed on human dyadic data in the D75 analysis: if a listener's state is a gain on a fixed profile, the cross-condition correlation of their response does not change with time since the partner's display; if it is a slow structured state, it does.

## Verdict
**adopt (as the measured elimination of gain, and for the "persistence carries identity" requirement); not a new computation.** The model is an inhibition-stabilised recurrent network with a slow second synaptic channel — recombination by the project's test. Its value is the negative result: gain fits one feature, a 20 s constant and structured connectivity fit the other, and no gain setting substitutes.
