# Encoding of female mating dynamics by a hypothalamic line attractor (Liu et al.)

Mengyu Liu, Aditya Nair, Nestor Coria, Scott W. Linderman & David J. Anderson, *Nature* 634(8035):901–909, 2024, doi:10.1038/s41586-024-07916-w (PMC11499253).

## What was read
The full PMC author text (JATS XML, ~12,900 words): abstract, main text sections "Dynamics of female behaviours in mating", "Tuning of female VMHvl neurons in mating", "Neural dynamics in female VMHvl", "Perturbations of the female line attractor", "Attractor encodes level of receptivity", Discussion, and the Methods sections for dynamical-system modelling, time constants, the integrator-input model and the spiking network. Figure captions read; figures not seen as images.

## The computation, precisely

**Same object as the aggression line attractor, in the same nucleus, in females during mating** — but with one property the male papers do not have: **it appears and disappears with hormonal state, over days.**

> "Unsupervised modelling of VMHvl α-cell activity using a dynamical systems approach revealed an approximate line attractor in neural state space, **which disappeared during non-receptive phases of the oestrus cycle and was hormone dependent**."
> "To our knowledge, no previous example of a line attractor that appears and disappears with periodic changes in behavioural/hormonal state on a timescale of days exists."

**What the position encodes.** Not a behaviour and not a stimulus: the graded receptivity of the animal.

> "the degree of movement along the attractor was highly correlated ($r^2 = 0.62$) with the level of receptivity as measured by the frequency of accepting behaviours ... By contrast, the integration dimension was not well correlated with other female behaviours."
> "Projecting neural activity into the integration dimension revealed ramping activity that began to increase at the onset of sniffing, mounting or intromission ... and that continued to increase across multiple mating bouts and IBIs."

**What moves it.** Fitted explicitly as an integrator with behavioural inputs: $x_t = A_z x_{t-1} + b_{z_t} + \epsilon_t + W u_t$, "where x refers to weighted activity of the integration dimension and W is a matrix used to linearly combine behavioural inputs (male sniff, mounting and intromission)". The fit "fits with high accuracy (cvR² of 0.88 ± 0.02) and possess a large intrinsic time constant (more than 200 s)", and the recovered input "peaks following every male contact ... male-contact-driven input, in combination with sustained input during male-engagement behaviours such as intromission, is used to integrate activity over time."

**And it is not the input.** Three dissociations:
- During copulation pauses the state stays put: "the average value of the integration dimension during copulation IBIs was relatively high, similar to and statistically indistinguishable from that measured during the preceding copulation bout", and a decoder could not tell bout from pause (0.52 ± 0.007 vs shuffle 0.49 ± 0.03, $p = 0.2$, $n = 4$).
- Remotely stopping the male (optogenetic activation of his VMHdm$^{Sf1}$ cells, forcing a 1–5 min pause, far longer than the natural 13.7 s inter-bout interval) left the female's state elevated "for minutes".
- Trials with plenty of male intromission but low female receptivity showed "relatively little if any ramping", so "ramping does not simply reflect accumulated mechanosensory inputs derived from male intromission."

**The hormonal switch is the distinctive computation.**
- On unreceptive days: "Models fit to data from unreceptive days failed to identify a single dimension with a very long time constant, indicating the absence of a line attractor"; line attractor score $0.05 \pm 0.02$ (unreceptive) vs $1.9 \pm 0.2$ (receptive), $p = 0.02$, $n = 4$. The flow field instead "contained a single point attractor, reflecting stable baseline activity before interaction with the male, from which the population vector made rapid excursions during sniffing and mounting, returning to the same point attractor after interaction."
- Projecting unreceptive-day activity into the receptive-day model: no ramping, and "the neural population activity vector remained at one end of the line attractor" — even though mounting occurred.
- The cellular correlate is a change of **time constants, not of mean activity**: "no change in average VMHvl α-cell population activity ... was apparent on receptive versus unreceptive days"; but first-dimension cells' autocorrelation half-width was $16.1 \pm 0.8$ s (unreceptive) vs $25.2 \pm 1.5$ s (receptive), $p < 0.001$, with "a subpopulation (39 ± 5%) of line attractor-weighted neurons whose ACHW was higher on receptive than on unreceptive days"; cells not in that dimension showed no change. A spiking network with those ACHW changes reproduced the loss of the attractor.
- Ovariectomy removed the attractor; hormone priming (oestrogen/progesterone) restored it.

**Conclusion as stated:** "neural population dynamics represent the dynamics of female mating receptivity and can be **reversibly sculpted by physiological state**."

## Evidence with numbers
- $n = 15$ mice for imaging; 16–207 units per mouse (mean $89 \pm 12$); rSLDS mean variance explained $64.08 \pm 6.8\%$.
- Integration dimension time constant $110.7 \pm 13.6$ s vs second dimension $24.5 \pm 5.1$ s ($p = 6.5\times10^{-5}$, $n = 15$).
- Single-cell tuning is weak: only ~2–13% of cells "tuned" to specific mating behaviours; GLM on female behaviour explains cvR² = 0.08, male behaviour 0.14, both 0.15 — but **adding neuron-to-neuron coupling filters takes it to 0.46**: "local circuit interactions contribute more than behaviour to neuronal variance".
- 30% of cells had ACHW > 25 s (mean 20 s), longer than the mean inter-bout interval of 13.7 s; with the male behind a barrier, ACHW fell to $14.3 \pm 0.42$ s vs $19.64 \pm 0.58$ s free interaction — so persistence is not persistent odour.
- Behaviour: females' behaviour is 83.9% male-responsive vs 16.1% self-initiated; males spend 11.3× more time on self-initiated mating behaviour. During pauses females continued social behaviours for 23% of the interval.
- Perturbation: optogenetic inhibition during imaging produced "transient off-manifold responses ... with the neural trajectory returning to the nearest fixed point along the line attractor post-inhibition", at several positions along the line.
- Mechanistic model: integration subnetwork of 200/1000 neurons at 12% density vs 1% elsewhere, $\tau_s$ = 20 s in the subnetwork and 100 ms elsewhere, $\tau_m$ = 20 ms, $\tau_I$ = 50 ms.
- Ejaculation: the dimension "peaked just before ejaculation, and immediately dropped thereafter" — a consummatory reset.

**Limits:** $n = 4$ mice for the longitudinal across-cycle comparison; correlational apart from the inhibition and behavioural-pause perturbations; calcium imaging; "approximate" attractor from a fitted model (cross-checked with FORCE-trained RNNs).

## Is this a new computation relative to the excluded frameworks?

Parts: (i) rSLDS / switching linear systems (**excluded**); (ii) leaky integration with input matrix $W$ (**excluded**: an SSM); (iii) continuous attractor (classical); (iv) slow synaptic channel in a subnetwork (as in the companion papers).

**Not a new computation.** The contribution is a second, independent demonstration of the dissociation in `mountoufaris-2024-neuropeptide-line-attractor.md`, with a different cause (hormone rather than peptide receptor) and a different timescale (days rather than acute):

> **Mean activity unchanged; time constants of a specific 39% subpopulation changed; the dynamical object changes from a point attractor to a line attractor. A slow physiological variable decides which dynamics the same cells implement.**

Two further points that are not in the excluded list as *roles*:
- **The state is about the agent, not the stimulus.** It correlates with the animal's own receptivity ($r^2 = 0.62$) and *not* with the partner's behaviour, even though the partner's contacts are what move it ($u_t$). An integrator whose readout is "my own disposition", driven by the partner's acts, is precisely the structure this project wants: the partner supplies increments; the variable means something about the self.
- **Coupling explains more than behaviour** (cvR² 0.08–0.15 → 0.46): most of the variance is internal interaction, not stimulus-locked response. A core whose latent is mostly a function of the partner's features is the wrong shape.

## What it suggests for an affective core where the partner is structured, not a gain

1. **A slow relationship/physiological variable that decides whether the episode has a memory at all.** Here, hormonal state over days switches between *point* attractor (respond and return) and *line* attractor (accumulate and hold). In the core, make the slow variable (trust in this partner, own need state, time since last contact) set the time constants of a *subpopulation* — 39% is the measured figure — and let the topology follow. Important: this must be a change in the agent's own cells' persistence, not a change in how strongly the partner is heard.
2. **The partner enters only as $u_t$ through a fixed $W$; the attractor is the agent's.** This is the cleanest template in the cycle for "the partner's influence is structured". The partner's acts (sniff, mount, intromission; for the Bot: a smile, a question, a silence) are discrete events that push along a direction the agent owns. The invariant: the partner's input matrix $W$ has no component that can change $A$. State-space-wise, $u$ and $A$ are separate objects, and the design must forbid any path from $u$ to $A$.
3. **Dissociation test to copy directly.** The decisive measurement here is: *the same quantity of partner input produces ramping in one physiological state and none in another* ("trials with high male intromission rates but low female receptivity ... relatively little if any ramping"). That is the experiment to run on the core: hold the partner's behaviour fixed, change the agent's own state, and show that the carry-over appears or vanishes. If the core's carry-over tracks the partner's input regardless of own state, the design is a gain.
4. **Consummatory reset.** The state "peaked just before ejaculation, and immediately dropped thereafter" — a satiable drive with an event-triggered collapse, which is the brief's satiability requirement realised as a structural reset rather than a decay constant.
5. **An honest caution for this project's Principle 6.** This is a mating/receptivity variable in mice. Nothing here licenses building an agent whose "receptivity to the user" ramps with the user's contact; the useful abstraction is the *topology switch*, not the drive it implements. The companion risk (an agent that escalates engagement with user attention) is exactly the flattery path the brief forbids, so the slow variable in the core should be gated by the agent's own satiable needs and never by the amount of user attention.

## Verdict
**adopt (second, independent evidence that a slow physiological variable switches the dynamical topology of the same cells while leaving mean activity unchanged; plus the $x_t = A x_{t-1} + W u_t$ separation as the template for partner input).** Mathematics is excluded; the dissociation and the separation are the assets. $n = 4$ for the central longitudinal result, so treat the effect size as indicative.
