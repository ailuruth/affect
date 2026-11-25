# Causal evidence of a line attractor encoding an affective state (Vinograd, Nair et al.)

Amit Vinograd, Aditya Nair, Joseph H. Kim, Scott W. Linderman & David J. Anderson, *Nature* 634(8035):501–508, 2024, doi:10.1038/s41586-024-07915-x (PMC11499281).

## What was read
The full PMC author text (fetched as JATS XML, ~13,500 words): abstract, main text sections "Line attractor for observing aggression", "Holographic activation shows integration", "Line-attractor neurons form ensembles", "Attractor stability ties to connectivity", Discussion, and the Methods in full — including the rSLDS equations, the time-constant and line-attractor-score definitions, and the mechanistic integrate-and-fire model with all parameters. Extended Data figures were read as their caption text (which in this manuscript carries most of the numbers). Figures themselves not seen.

## The computation, precisely

**The model fitted to data (quoted equations).**
$p(z_{t+1} \mid z_t = k, x_t) = \mathrm{softmax}(R_k x_t + r_k)$;
$x_t = A_{z_t} x_{t-1} + b_{z_t} + \epsilon_t$, $\epsilon_t \sim \mathcal{N}(0, Q_{z_t})$;
$y_t = C x_t + d + \delta_t$, $\delta_t \sim \mathcal{N}(0, S)$.
Time constants from eigenvalues: $\tau_a = 1/\log(\lambda_a)$ (as printed). Line attractor score $= \log_2(t_n/t_{n-1})$, the ratio of the two largest time constants. Two-dimensional models were used; the two dimensions were near-orthogonal ("subspace angle ... 88.1 ± 0.87°, n = 9 mice"), and the columns of $C$ identify which neurons belong to $x_1$ (slow, integrating) and $x_2$ (fast).

**The causal test.** Neurons were assigned to $x_1$ or $x_2$ by the fit, then five of them were stimulated holographically ("2 s, 20 Hz, 5 mW ... with a 20 s interstimulus interval"), in head-fixed mice that had watched a fight.

- **On-manifold ($x_1$):** "optogenetic reactivation of cohorts of five individual x1 neurons yielded robust integration of activity in the entire x1 dimension-weighted population, as evidenced by progressively increasing peak activity during the 20 s ISI after each consecutive pulse ... Activity decayed slowly after each peak but did not return to pre-stimulus baseline." In state space: "Activation pulses transiently moved the population activity vector (PAV) 'up' the line attractor, followed by relaxation back down the attractor to a point that was higher than the initial position of the system."
- **The attractor is finite:** "integration of optogenetic stimulation pulses saturated in the x1 dimension after the third pulse, suggesting that the line attractor occupies a finite portion of the neural state space" — and a finite-length model beat an infinite one on mean squared error ($p<0.001$, $n=8$).
- **Off-manifold ($x_2$):** "we observed stimulus-locked transient activity in the x2 dimension followed by a decay back to the baseline during the ISI period ... the PAV relaxed back into the attractor, near to the initial location that it occupied before the stimulus." And after first moving up the line with $x_1$ stimulation, an $x_2$ perturbation relaxed back "to the position occupied after the previous x1 stimulation ... rather than simply relaxing back to the baseline. This experiment confirms the attractive nature of different points along the line."
- **Specificity:** random (unweighted) neurons produced nothing in either dimension; $x_1$ stimulation did not drive $x_2$ and vice versa.

**The implementation, and the result that matters most here.** Single-cell stimulation measured functional connectivity: "The fraction of $x_1\!\to\!x_1$ pairs above this threshold was around 36%" (threshold = the strongest $x_1\!\to\!x_2$ influence, z ≈ 0.6; $n = 99$ pairs, 7 mice), with no distance dependence and surviving a 50 μm exclusion zone. Then an excitatory integrate-and-fire network ($N=1000$) was fitted:
$\tau_m \mathrm{d}x_i/\mathrm{d}t = -x_i(t) + g\sum_j W p_i(t) + w_i s(t)$, $\tau_m = 20$ ms, threshold $\theta = 0.1$; synaptic current $\tau_s \mathrm{d}p_i/\mathrm{d}t = -p_i + r_i$; network time constant derived as $\tau_n = \tau_s/(1-\lambda_{\max})$; feedback inhibition $\tau_I \mathrm{d}I_{\text{inh}}/\mathrm{d}t = -I_{\text{inh}} + \frac1N\sum r_N$, $\tau_I = 50$ ms, entering as $-g_{\text{inh}} I_{\text{inh}}$; a 200-neuron (20%) integration subnetwork with density varied; $W_{ij}\sim U(0,1/\sqrt N)$ overall and $U(0,1/\sqrt{N_p})$ in the subnetwork, $N_p = 200$.

> "only artificial networks based on relatively sparse connectivity (around 8–12%) and slow synaptic time constants (around 20 s) could yield network time constants (τn) in the experimentally observed range (~50–200 s) ... By contrast, networks with fast glutamatergic connectivity failed to do so over the same range of connection densities."
> "The addition of global strong feedback inhibition allowed networks to match the observed connection density (36%) but, importantly, maintained the slow nature of the functional connectivity (20 s)."
> "they differ from most continuous attractor models by invoking slow neuromodulatory transmission rather than fast glutamatergic excitation. Numerous theoretical studies have posited that continuous attractors relying on recurrent glutamatergic connectivity require precise tuning of synaptic weights to sustain stable attractor dynamics. By contrast, the inclusion of slow neurotransmission in our mechanistic models yielded network time constants in the observed range **across a wide range of connectivity densities**."

**This is the deleted free parameter.** A fast-synapse line attractor needs its weights tuned to put an eigenvalue at 1 (a knife-edge). With $\tau_s \approx 20$ s, the same $\tau_n$ range is reached over a broad band of densities — the precision requirement is removed by the slow channel, not by tuning. The authors also note the slow timescale may exist "not only to ensure attractor robustness, but also to implement the relatively long time scales of internal affective or motive states".

**A mirror-like finding, relevant to a dyad.** The line attractor appeared in mice *observing* a fight, over largely the same cells as when fighting: "a highly overlapping set of neurons (70%) contributes to line-attractor dynamics during observing or engaging in attack", and a decoder trained on the observation data read out engagement ($p = 0.0079$, $n=5$).

## Evidence with numbers
- $n = 9$ mice for 2P imaging; $n = 8$ for $x_1$ perturbation, $n = 7$ for $x_2$; 25 single $x_1$ neurons and 18 single $x_2$ neurons stimulated across mice.
- Line-attractor neurons are "around 20–25% of Esr1+ neurons".
- $x_1$ neurons are more persistent than $x_2$ (ACHW: $p = 0.0078$); mean ACHW during observation $25 \pm 0.8$ s vs engagement $20 \pm 1.7$ s.
- Model cross-validation: cvR² ≥ 70% required; 84.7 ± 0.03% (engagement), 67.2 ± 0.02% (observation); perturbation predictions ~85%.
- Non-targeted $x_1$ follower activity decoded the targeted cells' integration with "80% versus 40%" variance explained compared with $x_2$ or random ($p = 0.01$, $p = 0.0003$).
- **Individual differences:** decay time constant vs functional connectivity strength (AUC after the 3rd stimulus) $R^2 = 0.87$ ($p<0.001$, $n=8$); after the 1st stimulus $R^2 = 0.59$. **Ramp rate** was *not* correlated ($r^2 = 0.01$), "suggesting that the latter might be driven by extrinsic inputs to the VMHvl". So decay is intrinsic, ramp is input-driven — two separable halves.
- Mean distance of follower cells 139 ± 35 μm; only 11% within 50 μm, so not light spillover.

**Limits:** head-fixed observation (not fighting); the attractor is "approximate"; the mechanistic model is a fit, not a measurement of synapse kinetics; the slow-transmission conclusion is inference from the density/timescale trade-off (with the neuropeptide test in the companion paper, `mountoufaris-2024-neuropeptide-line-attractor.md`).

## Is this a new computation relative to the excluded frameworks?

Parts: (i) rSLDS = switching linear systems (**excluded**); (ii) leaky-integrate-and-fire with recurrent excitation and global inhibition (**excluded**: recurrent network); (iii) continuous attractor (classical); (iv) two synaptic timescales on one weight matrix (as in Kennedy 2020).

**No new computation.** But two findings function as the "derived invariant that deletes a free scalar" this project is looking for:

1. **Slow transmission removes the weight-tuning parameter.** $\tau_n = \tau_s/(1-\lambda_{\max})$: to reach $\tau_n \in [50,200]$ s with $\tau_s = 0.1$ s you need $\lambda_{\max}$ within $\sim 10^{-3}$ of 1; with $\tau_s = 20$ s you need only $\lambda_{\max} \approx 0.6$–$0.9$. The slow channel converts a knife-edge into a broad basin. This is a one-line, checkable statement, and it is the kind of argument (a parameter deleted by construction) that `new-mechanisms-synthesis.md` identifies as the signature of a new mechanism.
2. **Decay and ramp are separately caused** ($R^2 = 0.87$ vs $r^2 = 0.01$): the agent's own structure sets how long a state lasts; the outside world sets how fast it rises. That is a decomposition of "partner influence" into a part the partner owns (rate of climb) and a part the agent owns (persistence) — with no shared scalar.

## What it suggests for an affective core where the partner is structured, not a gain

1. **The partner may set the ramp; only the agent's own connectivity sets the decay.** Build the core so that partner-derived input enters *only* as an input term $Wu_t$ to the integration dimension, while the dimension's eigenvalue (its persistence) is a function of the agent's own learned recurrent structure. Then the invariant is: $\partial \tau / \partial(\text{partner}) = 0$ identically. The partner can move the agent along the manifold but cannot change how long the agent stays there — which is exactly "structured influence, not a gain", and it is measurable (fit $\tau$ with and without the partner).
2. **The attractor has finite length — a built-in ceiling.** Integration "saturated ... after the third pulse". The agent's state cannot be pushed arbitrarily far by repeated partner displays; the manifold ends. A design can inherit this (a bounded manifold) rather than imposing a ceiling parameter $\vartheta$ — the critique's objection to the dyadic-sheaf design was precisely that its ceiling was a dial.
3. **Off-manifold perturbations return to where the state already was, not to baseline.** This is the mathematical form of "the partner's momentary display does not erase the relationship state": transient inputs orthogonal to the slow direction decay with no lasting effect, and the state returns to its current position, not to zero. For the core: fast facial events live on $x_2$ and leave nothing; only input with a component along $x_1$ changes the episode.
4. **Two subpopulations with selective functional coupling (36% within, near-zero across).** The core's slow (affective) and fast (reflex) units should be separate sets with dense within-set and sparse across-set coupling, which is a measurable structural property and a target for the "effector mask" idea in `foundations/design-partner-regulator.md` — here it is derived from data rather than asserted.
5. **The observation result is directly on this project's topic.** The same slow state, over 70% of the same cells, formed while merely *watching* an interaction. So a persistent affective state built from observing a partner is not a metaphor; and a decoder trained on observation generalised to engagement. For the Bot: the state it builds while listening is the same object as the state that drives its own expression — one latent, two uses, which is the pleiotropy requirement from `anderson-adolphs-2014-emotion-primitives.md`.

## Verdict
**adopt (as the causal grounding of the line-attractor primitive and the source of two invariants: slow transmission deletes the weight-tuning parameter; ramp and decay are separately owned).** The computation is excluded mathematics; the physics of its implementation is what is worth copying.
