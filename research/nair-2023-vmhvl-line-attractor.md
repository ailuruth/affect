# An approximate line attractor in the hypothalamus encodes an aggressive state (Nair et al.)

Aditya Nair, Tomomi Karigo, Bin Yang, Surya Ganguli, Mark J. Schnitzer, Scott W. Linderman, David J. Anderson & Ann Kennedy, *Cell* 186(1):178–193, 2023, doi:10.1016/j.cell.2022.11.027.

## What was read
The published PDF (Stanford Schnitzer-lab copy), text-extracted (~15,100 words): abstract, introduction, all Results sections (dynamical analysis of VMHvl; line attractor and escalation; MPOA rotational dynamics; VMHvl during mating; MPOA during aggression), the Discussion in full, and all main figure captions (Figs. 1–6). STAR Methods were read only where the figure captions pointed (line attractor score, time constants); the equations of rSLDS itself I take from the companion paper's Methods, which I read in full (`vinograd-2024-causal-line-attractor.md`). Supplementary figures were seen as caption text only.

## The computation, precisely

**Object.** Fit a recurrent switching linear dynamical system (rSLDS) to calcium imaging of VMHvl$^{Esr1}$ neurons during male–male encounters: $x_t = A_{z_t} x_{t-1} + b_{z_t} + \epsilon_t$, $y_t = Cx_t + d + \delta_t$, with a discrete state $z_t$ whose transitions depend on $x_t$. Then read the eigenvalues:

> "The eigenvalues of this matrix reflect the rate at which activity along each of these dimensions decays to zero following external input and can be converted to a time constant for each dimension. Input to dimensions with short time constants will quickly decay to zero, whereas input to dimensions with long (large) time constants persists and decays slowly. Strikingly, one of the rSLDS dimensions had an estimated time constant of over 100 s that was significantly higher than that of all other dimensions ... Because systems with long time constants approximately integrate their input over time, we refer to the longest time constant dimension as the 'integration' dimension."

**Line attractor score** (defined here, used by all four papers in this cycle): $\log_2(\tau_n/\tau_{n-1})$, the base-2 log ratio of the largest to the second-largest time constant of the dynamics matrix. "this ratio has a relatively high value in systems containing a single integration dimension (forming an approximate line attractor) and is otherwise close to zero."

**What the position along the line does.** It is not a magnitude of one behaviour; it **selects which behaviour is emitted**:

> "As population activity progressed along the line attractor from low to high values of PC1, behavior progressed from sniffing to dominance mounting to attack ... suggesting an encoding of an underlying continuous [variable]"

and in the mating case in the same nucleus, "sniffing occurred at the lowest values, USV+ mounting at intermediate values, and intromission at the highest values of this dimension", with pairwise decoders "intromission versus sniffing: F1 = 0.92 ± 0.01 N = 4 animals; mounting versus sniffing: F1 = 0.81 ± 0.02 N = 6 animals".

The Discussion names the two readings, and allows both: "the line attractor serves to maintain the system in a stable internal motive state that persists continuously during stochastic expressions of observable attack"; or "it may serve as an integrator that accumulates 'evidence' used to make behavioral decisions ... Such a function would require that different behaviors be triggered at different threshold values of the integrator. This type of ramp-to-threshold mechanism has been suggested to control sequential actions during male courtship behavior in Drosophila and predator escape in mice. These two hypotheses are not incompatible."

**The contrast that makes it a claim about computation, not about a region.** The medial preoptic area, which drives mating, has **no** line attractor; it has rotational dynamics and sequential cell-identity coding:

> "No dominant 'slow' dimension was apparent in the time constants of the rSLDS dimensions ... MPOA activity during aggression lacks the persistence, ramping, and line attractor dynamics seen in VMHvl"
> "MPOA represents behavior via a cell identity code, whereas VMHvl apparently does so via population coding."
> "Put simply, VMHvl coding of behavior appears to be analog, whereas MPOA coding of behavior appears more digital."

And the *same* VMHvl population has **two different line attractors** for aggression and mating, built from almost disjoint neuron sets: "the integration dimension seen during mating was biased toward neurons tuned to female intruders, whereas male-tuned neurons primarily contributed to this dimension during aggression (**7.73% ± 0.8% overlap**, n = 6 mice)". So the attractor is not a property of the tissue; it is instantiated per social context over different cells.

## Evidence with numbers
- $n = 6$ mice for VMHvl, $n = 3$ for MPOA; recordings from two prior studies; "average duration 5.1 ± 0.68 min and 11.4 ± 0.68 min" for male–male and male–female.
- Integration dimension time constant "over 100 s", significantly longer than all others ($p < 0.001$, $n = 6$); eight rSLDS dimensions.
- Line attractor score > 0 in all VMHvl mice; "close to zero" in MPOA and significantly different ($p < 0.005$; $n = 3$ MPOA vs $n = 6$ VMHvl).
- **Individual differences:** "animals that displayed more aggressive behavior (calculated as the fraction of time spent attacking) also exhibited an integration dimension with a longer time constant ($r^2 = 0.77$, $n = 14$ animals)", holding across studies and GCaMP variants (6s vs 7f).
- The integration dimension is not movement: variance explained by "the acceleration, facing angle, or velocity of the resident, or from the distance between mice (mean $R^2$: 0.28 ± 0.04, $N = 6$)".
- Single-neuron tuning is weak in VMHvl: "most VMHvlEsr1 neurons exhibit mixed behavioral selectivity"; MPOA clusters are action-specific.
- MPOA: "85% GABAergic"; VMH "primarily glutamatergic" — and the authors note "to our knowledge, there is no way to achieve similar graded and persistent signals within a population of inhibitory neurons", so the coding scheme follows the cell type.
- Behaviour escalation in the aggression case progresses sniff → dominance mount → attack with the dimension's value; transient excursions off the line occurred at intruder entry and aligned with PC2.

**Limits:** correlational (the causal test is Vinograd et al. 2024); rSLDS is a fitted statistical model (the authors check it against FORCE-trained RNNs in the companion mating paper); small $n$; calcium imaging.

## Is this a new computation relative to the excluded frameworks?

Parts: (i) switching linear dynamical systems — **excluded** (linear operators with structure; rSLDS is literally a bank of linear systems with a softmax gate, i.e. a mixture-of-experts over SSMs); (ii) a near-unity eigenvalue = a leaky integrator — **excluded**; (iii) a continuous attractor — classical (Seung, Ben-Yishai); (iv) a threshold readout selecting discrete actions — **excluded** (ramp-to-threshold).

So **as a model, this is a recombination of excluded parts, and I should say so plainly.** What is not on the excluded list is the *role* the object plays, and it is worth stating as a design primitive because none of the seventeen designs used it:

- **The persistent state's position sets the expression mapping, not the expression amplitude.** Moving along the line changes *which* behaviour is emitted (sniff → mount → attack), with the same population. A scalar gain cannot do this; a position on a slow manifold with ordered thresholds can.
- **The attractor is instantiated per context over near-disjoint cell sets (7.7% overlap).** The same tissue holds two different line attractors, selected by which social partner is present. That is "a neuromodulator switches *which* circuit computes" realised at the level of population dynamics: the dynamical object itself is context-selected, not scaled.
- **One structural parameter — the leading time constant — predicts a trait** ($r^2 = 0.77$ with aggressiveness across 14 animals). Temperament is the relaxation time of the state, not a gain on a readout.

## What it suggests for an affective core where the partner is structured, not a gain

1. **The exact primitive the operator describes: a line attractor whose position sets the expression mapping.** Let $s \in \mathbb{R}$ be the position of the core's state on a slow manifold, with the agent's own events as the integrated input. Make the *expressive readout a function of $s$ in kind*: ordered regions of $s$ select different expressive repertoires (a quiet attentive face; a warm engaged face; a distressed face), with each repertoire's amplitude set by the agent's own fast dynamics. Then the partner, by moving $s$, changes **the shape of the response and the repertoire in use** — never its magnitude. This separates "how much the partner moves me" (a displacement along one direction) from "what I then do" (a mapping chosen by position), and the dial question changes form: a displacement along $s$ cannot produce copying unless the copy mapping is one of the repertoires at some $s$, which is a design-time fact that can be excluded by construction.
2. **Two attractors over near-disjoint sets = relationship-specific dynamics without partner-specific weights on expression.** Per partner (or per relationship mode), a different subset of the agent's own units carries the integration dimension. Carry-over with a returning partner is then the re-selection of that subset, which is a measurable, discrete event, and an ablation target.
3. **Temperament from structure.** If the leading time constant is the temperament parameter, slow and fast temperaments differ in one eigenvalue of the agent's own dynamics, and the prediction is quantitative: the correlation between that constant and expressed intensity over an episode should be strong ($r^2 \approx 0.8$ in mice), which is a target for the project's own evaluation.
4. **The MPOA contrast is a warning and a tool.** The same brain solves a closely related social behaviour *without* a line attractor, using rotational dynamics over action-specific cells. So a persistent scalable state is not needed for all social behaviour — it is specifically for the escalating, de-escalatable kind. A core that uses one object for both (greeting sequences and affective escalation) is probably wrong; the line attractor belongs to intensity, the rotation belongs to sequencing.
5. **Measure the line attractor score in the core.** $\log_2(\tau_n/\tau_{n-1})$ on the fitted dynamics of the core's latent is a cheap, publishable diagnostic: it says whether the design *actually has* a one-dimensional persistent state or merely has slow weights. This should be run on every candidate design's latent, since three of the four papers in this cycle use it as the test.

## Verdict
**adopt (the primitive: a position on a slow manifold that selects the expression mapping; plus the line-attractor-score diagnostic and the 7.7%-overlap context selection).** The model itself is excluded mathematics (switching linear systems, leaky integration, ramp-to-threshold); the computation worth taking is the role, and its causal status comes from `vinograd-2024-causal-line-attractor.md` and its chemical implementation from `mountoufaris-2024-neuropeptide-line-attractor.md`.
