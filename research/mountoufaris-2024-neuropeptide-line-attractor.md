# A line attractor encoding a persistent internal state requires neuropeptide signalling (Mountoufaris et al.)

George Mountoufaris, Aditya Nair, Bin Yang, Dong-Wook Kim, Amit Vinograd, Samuel Kim, Scott W. Linderman & David J. Anderson, *Cell* 187(21):5998–6015, 2024, doi:10.1016/j.cell.2024.08.015 (PMC11490375).

## What was read
The published version is in PMC but its full text would not come back from either Europe PMC or NCBI E-utilities over several attempts (only a stub returned). I therefore read **the bioRxiv preprint of the same work in full**: "Neuropeptide Signaling is Required to Implement a Line Attractor Encoding a Persistent Internal Behavioral State", doi:10.1101/2023.11.01.565073, posted 5 November 2023 — PDF downloaded and text-extracted (~22,300 words): abstract, introduction, all Results sections, Discussion, and the methodological-considerations section. Figures were not read as images. **Numbers below are the preprint's**; the peer-reviewed *Cell* version may differ, and I have not checked it. Where the published abstract (read via search) agrees, I say so.

## The computation, precisely

**The question.** The companion papers inferred, from a density/timescale trade-off in a network model, that the VMHvl line attractor needs *slow* transmission (`vinograd-2024-causal-line-attractor.md`). This paper tests that chemically, by CRISPR-disrupting the receptors for two neuropeptides in the attractor's own cells.

**The manipulation.** Multiplexed CRISPR/Cas9 ("CRISPRoscopy") co-disrupting *Oxtr* (oxytocin receptor) and *Avpr1a* (vasopressin 1a receptor) in adult VMHvl$^{Esr1}$ neurons, with simultaneous single-cell calcium imaging, unilaterally (to avoid confounding the behaviour).

**The result, which is the point.** The *content* of the code survives; the *dynamics* do not.

What survives:
- "linear SVM decoders trained on imaging data from either control or experimental mice correctly predicted intruder sex with virtually 100% accuracy ... co-targeting of Oxtr/Avpr1a in VMHvlEsr1 cells does not disrupt the population coding of intruder sex".
- "Decoders trained on data from each group were able to accurately distinguish these behaviors in held out testing data with close to 100% accuracy. Thus, the population coding of social behavior by VMHvlEsr1 neurons is not affected."
- Mean activity changes were small: "slightly but significantly decreased"; among cells "active" (≥2σ) "did not differ".

What is destroyed:
- "In control mice, the time constant (τ) of the 1st rSLDS dimension ... was much higher than that of the 2nd dimension (~100-120s vs ~40s). This yielded a line attractor score ... of ~1.5 ... In contrast, in experimental mice the first two rSLDS dimensions had statistically indistinguishable τ values (<50s) ... and consequently a line attractor score close to zero."
- "in experimental mice this line attractor was absent and was replaced by a point attractor ... from which the population activity vector made transient excursions during bouts of sniffing or attack. This point attractor is a 'trivial' fixed point, corresponding to the resting state of a system in which activity decays to baseline in the absence of inputs."
- The time course changes shape: control activity "ramped up during the progression from male-directed sniffing to attack, eventually reaching a plateau where it decayed slowly between attack bouts ... and remained elevated between sequential trials with different intruders. In contrast, in experimental mice activity in the 1st dimension decayed rapidly in between attack bouts, displaying a 'sawtooth' profile" — i.e. "these neurons are still active during attack, but do not integrate recent experiences in the same way as normal mice."
- Single-cell persistence: autocorrelation half-width of first-dimension cells fell from $28.6 \pm 1.23$ s (control) to $9.86 \pm 1$ s (experimental), "by ~20 seconds"; a 50.9% reduction population-wide, 65.4% for first-dimension cells; only ~22% reduction during male–**female** interactions.

**The converse, ex vivo.** Bath-applying the peptides creates the same two-timescale split: with OXT+AVP perfusion, a 2-dimensional rSLDS captured 85% of variance and "The time constant of dimension x1 (~90s) was ~8-9 -fold greater than that of x2 (~15s) ... similar as what we observed in vivo ... x1 neurons exhibited slowly decaying responses to OXT+AVP application, while x2 neurons exhibited more transient responses", over *distinct* cells.

**Behaviour.** Bilateral disruption reduced attack probability, total attack time and bout duration, and increased latency to first attack, with locomotion unaffected. Ex vivo, peptide responses were reduced (~ several-fold) but "they do not eliminate such responses completely". Receptor anatomy: "~78% of Esr1+ cells in VMHvl expressed Oxtr mRNA, and ~61% of these cells also expressed Avpr1a".

**Tuning shifts, worth recording:** attack-tuned units fell ~70–80%, sniff-tuned ~40–70%, with "a concomitant ~18% increase in the fraction of units exhibiting mixed selectivity", and female-directed tuning *increased*. So removing the slow channel did not silence cells; it **re-sorted them from specific to mixed selectivity** and shifted the balance between the male- and female-directed codes.

## Evidence with numbers
As quoted: $n = 4$ control and $n = 7$ experimental mice for imaging; ~66% of imaged cells co-infected; τ ~100–120 s → <50 s; line attractor score ~1.5 → ~0; ACHW 28.6 → 9.86 s; ex vivo τ ratio 8–9×; Oxtr in ~78% of Esr1+ cells. Decoder accuracies ~100% in both groups.

**Limits (the authors state them):** between-subject comparisons cannot say whether the population τ fell because individual cells changed or because fewer cells were active; CRISPR efficiency was not quantified at mRNA/protein level ("the lack of equally specific immune reagents"); aggression was reduced but not abolished; this is a preprint and the published numbers may differ.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) rSLDS (**excluded**); (ii) recurrent network with slow synaptic channel (**excluded**); (iii) GPCR-mediated slow synaptic conductance — biology, not a new computation.

**No new computation here either.** What this paper contributes is the cleanest *dissociation* I have found in this cycle, and it is directly the thing the operator is asking for:

> **The same cells, the same weights, the same decodable content — and the attractor is present or absent depending on one chemical channel. A peptide does not scale the state; it determines whether a persistent state exists at all.**

Formally: let the network have fast coupling $W$ and a slow channel with conductance timescale $\tau_s$ and strength $\alpha$ on the *same* $W$. Then $\tau_n \approx \tau_s/(1-\lambda_{\max}(\alpha W))$, and for $\alpha \to 0$ the leading eigenvalue drops away from 1 and the line attractor collapses to a point attractor — a **bifurcation**, not a reduction in gain. The output of the network before and after is nearly identical instant-by-instant (decoders at ~100% both ways); what changes is the topology of the flow.

That is a qualitative change of computation produced by a slow chemical variable, with the content untouched: the biological existence proof that "a modulator switches which computation happens" is real and measurable.

## What it suggests for an affective core where the partner is structured, not a gain

1. **The strongest single idea in this cycle: let the social variable control the existence of the persistent state, not its size.** Give the core a slow channel on its *own* recurrent structure, with a conductance $\alpha$ set by social/need state. At low $\alpha$: a point attractor — the agent responds to events and returns to rest, no carry-over, no episode. At higher $\alpha$: a line attractor — the agent accumulates and holds. This is a **bifurcation controlled by relationship**, and it has properties the project has been unable to get from a gain:
   - the flat-to-copy question changes type, because what varies is the number and type of fixed points, not an amplitude on a fixed map;
   - the agent's instantaneous expressive content is *unchanged* by $\alpha$ (as decoders showed), so the social variable cannot be used to copy;
   - it is lesionable and measurable with one number: the line attractor score $\log_2(\tau_1/\tau_2)$, which went 1.5 → 0.
2. **A derived invariant worth proving:** if the slow channel shares the fast channel's weight matrix, then no setting of $\alpha$ can introduce a direction that was not already in $W$'s spectrum. The partner (through $\alpha$) can therefore only make the agent *persist along its own existing directions* — it cannot create a new expressive direction, let alone the partner's. This is "reading the other through one's own body" as an algebraic statement, and it comes free from sharing $W$.
3. **Removing persistence re-sorts selectivity toward mixed.** A prediction for the core: with the slow channel off, per-channel specificity of the agent's expression should fall and channels should become more correlated (more mixed selectivity). That is a measurable signature of whether the core's own slow state is doing the work the design claims.
4. **The asymmetry across contexts matters.** The same disruption cut persistence 65% in male-directed interaction but only ~22% in female-directed interaction. The slow channel is not a global clock: it is engaged per social context. In the core, $\alpha$ should be context-indexed (per relationship, per situation), which gives relationship structure without partner-specific expressive weights.
5. **Oxytocin/vasopressin are not "prosocial gain" here.** This is a useful corrective to the usual framing (see `froemke-young-2021-oxytocin-social-salience.md`): in this system the peptide's job is to supply a ~20 s synaptic timescale so a population can integrate. If the Bot has an "oxytocin-like" variable, its job should be *to hold a state*, not to make it nicer.

## Verdict
**adopt (the key dissociation of this cycle: a slow chemical channel controls whether a persistent state exists, while leaving instantaneous content decodable; implemented as a bifurcation in the agent's own recurrent structure).** Read as a preprint, so numbers must be re-checked against *Cell* 2024 before any design cites them. The mathematics is excluded (switching linear systems, recurrent networks); the dissociation is not.
