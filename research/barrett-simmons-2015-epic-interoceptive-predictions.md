# Interoceptive predictions in the brain (the EPIC model)

Lisa Feldman Barrett and W. Kyle Simmons, *Nature Reviews Neuroscience* 16(7):419–429, 2015, doi:10.1038/nrn3950. Read from the author-hosted PDF at affective-science.org. © Macmillan; quote sparingly.

## What was read
All of the main text was extracted with pdftotext: abstract, laminar architecture, M1, the EPIC model, Boxes 1–3, the illness section and the conclusion. The figures were read as captions. I did not read the supplementary boxes (S1–S3) or the reference list beyond the first 28 entries.

## Claims
- **Interoception is mostly prediction.** "Interoceptive experience may largely reflect limbic predictions about the expected state of the body that are constrained by ascending visceral sensations."
- **Architecture: the structural model of Barbas, combined with active inference.**
  - Less-laminated (agranular) cortex sends predictions from its deep layers.
  - More-laminated (granular) cortex computes prediction errors in its superficial layers and sends them back.
  - Precision units in layers II and IIIa set the gain on the errors.
- **The interoceptive system.**
  - Agranular visceromotor cortices (cingulate BA24/25/32, posterior vmPFC BA14c, posterior OFC BA13a, ventral anterior insula) "estimate the balance between the autonomic, metabolic and immunological resources that are available to the body, and the predicted requirements of the body".
  - From that estimate they issue **allostatic visceromotor predictions** to the hypothalamus, brainstem and spinal cord.
  - **At the same time** they send **interoceptive predictions** (efference copies) to the granular mid and posterior insula. There, ascending lamina I and vagal input is compared with the prediction.
- **Visceromotor predictions are slow to update.** Agranular visceromotor cortex is "relatively insensitive to prediction-error signals". So interoceptive predictions are "fairly stable compared with the fluctuating state of the body". "Interoceptive perception is largely a construction of beliefs that are kept in check by the actual state of the body (rather than vice versa)." "Perceptions follow actions."
- **Three ways to reduce error.** Update the prediction; act on the body to make the prediction come true; or reduce sampling (attention and precision, including thalamic reticular gating).
- **The system works as a hub.** The visceromotor regions are rich-club hubs, so "interoceptive representations are a central part of every mental event". "Affective properties such as pleasure, displeasure and arousal ... are fundamental properties of conscious experience". Perception is "directed more by the homeostatic relevance of information than by the need for accuracy".
- **Degeneracy (Box 3).** The anterior insula is not necessary for emotional awareness. Patients "Roger" and "Boswell", with bilateral destruction of the anterior insula, "show remarkably preserved affective experience, self-awareness and conscious 'presence'".
- **Illness.**
  1. Chronically mispredicted energy needs, together with noisy afferents, lead the system to keep its predictions and ignore error.
  2. This is a positive-feedback loop with cumulative bodily cost.
  3. When error finally overcomes the insensitivity, the result is sickness behaviour.
  4. In this account, that sickness behaviour is depression.
  The authors cite their own finding (Avery et al. 2014): depression severity correlated negatively with dorsal mid-insula activity and positively with mid-insula–sgACC connectivity.

## Evidence
- Macaque tract tracing behind the structural model.
- Dorsal mid-insula responses to food images are reduced by circulating glucose, while (agranular) anterior insula responses are not (their ref. 64). This is offered as evidence for stable predictions.
- Avery et al. 2014, above.
- An opinion piece: no new experiments, and no simulation.

## Mechanistic commitments
1. **One generative model drives both action and perception.** A single visceromotor prediction serves as the command to the body and as the expected interoceptive input, through efference copy.
2. **Asymmetric learning rates.** The interoceptive prior updates slowly, more slowly than the body changes. That asymmetry is the persistence of affect.
3. **Precision as a learned gain** on interoceptive error.
4. **A shared hub broadcast.** Interoceptive prediction is sent to every network, so affect colours all processing.
5. **Allostasis is about a budget.** What is predicted is resource demand, not a set point.

## What it implies for a single formal core
This is the most mechanistic version of Barrett's programme and maps onto an active-inference or control core:
- the core's predicted body trajectory is $\hat b_{t+k}$, and the visceromotor output is the control that makes it true;
- affect is read out of the prediction, not out of the sensed body;
- persistence follows from a slow prior, with no separate decay variable needed.

A prediction to test in the engine: **the affect read-out should follow the predicted body more closely than the sensed body.** If the body is perturbed without the agent's model expecting it (sensor noise, or a clamp on one body variable), a predictive core's readout should lag and keep its prior. A reactive core's readout should follow the sensor at once.

Their illness loop has a counterpart in the core. With low precision on interoceptive error plus actions that try to confirm the prediction, the system can lock into a costly attractor. That gives the engine a **failure mode to test for** (a stuck low state), not just a feature.

## What an ablation could separate
- **Prediction versus error.** Set the learning rate of the interoceptive prior high, so the prior equals the current sensation. Then:
  - affect should become volatile;
  - anticipatory regulation should disappear, with no response before a deficit;
  - persistence should drop.
- **Precision.** Fix the interoceptive precision gain. With a gain that is too low, the state should become insensitive to the body and drift with context alone. With a gain that is too high, it should be twitchy. Either way, learned precision should matter.
- **Hub broadcast.** Cut the path from $h$ to attention and memory retrieval while keeping the path to the face. Face output should remain while state-congruent perception and recall vanish. This separates "interoceptive representation in every mental event" from expression alone.

## Verdict: adopt (mechanism for allostatic prediction and precision; source of the predicted-versus-sensed readout test)
Barrett 2017 gives the theory; this paper gives the architecture. Its slow-prior and precision claims are directly testable in a core.
