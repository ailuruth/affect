# Creating Connection with Autonomous Facial Animation (BabyX)

Sagar, Seymour and Henderson, *Communications of the ACM* 59(12):82–91, December 2016, doi:10.1145/2950041.

## Source read
The full article text, read from the Internet Archive's copy of the CACM full-text web page (snapshot 2022-09-01 of cacm.acm.org/magazines/2016/12/210362-…/fulltext). I read every section, the figure captions and the reference list. The figures themselves (including the architecture diagram, Figure 5) were not visible in the text copy, and the "Key Insights" sidebar did not come through.

History of access: an earlier attempt got HTTP 403 from cacm.acm.org (a Cloudflare block) and 401 from the Auckland ResearchSpace copy (handle 2292/32527, restricted). Semantic Scholar lists the paper as closed. The archived public web page was the only readable copy.

The companion technical papers were not read. Sagar et al. 2014 (SIGGRAPH Asia workshop, doi:10.1145/2668956.2668960) and Sagar et al. 2015, "BL: a visual computing framework…" (UCNC, LNCS) are both closed. The equations of the neural models are in those papers, not in this one. For the later architecture see babyx-2023-turn-taking.md and knott-sagar-takac-2022-babyx-ethics-emotion-model.md.

## Claims
- A face's behavior "emerges from many systems interacting on multiple levels", so BabyX models the nervous system at a low level and drives a biomechanical face from it.
- The design is deliberately an assembly: "Our goal is to integrate different current theories and models to create a holistic 'large functioning sketch'"; "our choice is to opt for flexibility and develop a 'system to build systems' in a Lego-like manner"; components are interchangeable "while exploring different theoretical models".
- Facial mimicry can be learned, not copied, by associative sequence learning (Heyes) from spontaneous babbling and a caregiver who mirrors it.
- Audiences react viscerally (the SIGGRAPH 2015 demo). The authors offer this as evidence of "creating connection".

## Architecture (as given; no equations in this paper)
- **Framework (BL, "Brain Language").** A library of time-stepping modules and connectors: leaky integrators, spiking neurons, mean-field models and SOMs, recurrent and convolutional nets. Learning is online. Any variable can drive any graphics parameter, and models can be swapped at run time.
- **Face.** Biomechanical model built from MRI and anatomy: deep and superficial fat, muscle, fascia and connective tissue, with large-deformation finite-element elasticity. "Individual and combined muscle activations were simulated to form an expression space, interpolated on the fly in BL as the face animates." So the real-time face interpolates precomputed FEM solutions. It does not run live FEM.
- **Two facial motor routes converge on a simulated facial nucleus.** Subcortical circuits produce innate patterns: brainstem central pattern generators for crying and laughing. Cortical circuits produce learned, "voluntary" expressions (citing Cattaneo & Pavesi 2014 and Gothard 2014).
- **Brain modules named in the text:** basal ganglia for action selection (after Redgrave et al.), superior and inferior colliculus driving the oculomotor network, pulvinar as a saliency map, amygdala and hippocampus as "hebbian associators", hypothalamus releasing "virtual hormones", and cortex as recurrent and multilayer nets and SOMs.
- **Emotion.** "Emotions in BabyX are, in fact, coordinated brain-body states that modulate activity in other circuits (such as increasing the gain on perceptual circuits)… stress lowers the threshold for triggering a brainstem central pattern generator that… generates the motor pattern of facial muscles in crying."
- **Neuromodulators.** Virtual dopamine drives motor activity and reinforcement learning, modulates plasticity, and shows in pupil dilation and blink rate. "The user can adjust BabyX's behavioral dynamics, sensitivities, and even temperament by adjusting virtual neurotransmitter levels."
- **Mimicry learning:**
  - Spontaneous network activity drives facial pattern generators (motor babbling).
  - The caregiver mirrors the result, and "the activity and feedback from this facial movement is associated with a delayed visual sensory pattern from the caregiver's facial response. Associative learning is modulated by phasic dopamine. Strengthening bidirectional associative connections results in the caregiver's expression being able elicit a similar expression in BabyX."
  - Praise after a successful imitation releases more dopamine and strengthens the connections further.
  - Attention is a precondition: the caregiver's face must win the colliculus competition and fall on the virtual fovea.
  - Bidirectional links from mimicked expressions back into the affective circuits that generate them are proposed as "a basis for 'virtual empathy'" (facial feedback).
- **Other learning demos.** Pong by motor babbling plus reward, with the user able to "release virtual dopamine". A "First Words Book" in which trained image–word associations trigger a vocalization.
- **Wired, not learned:** "Lip shapes are pre-associated with acoustic elements"; the voice is sampled from a real child's phonemes.
- **Separation.** "If BabyX is abandoned, depending on oxytocin levels, her stress system can activate a cascade of virtual hormones, and she becomes increasingly distressed."

## Evidence with numbers
None. The article reports no quantitative result, no number of sessions, no learning curve for mimicry, and no comparison condition. All evidence is demonstration and anecdote: public forums, the SIGGRAPH 2015 audience reacting to the offer of a pain demonstration, and laughter feeding back into BabyX. Validation is future work: "we will be exploring how well the model elicits naturalistic responses from parents… compared to their own or another child". The authors also write: "Introducing synthetic lesions could be an effective way to explore lower-level validation."

## Failure modes, reported or evident
- **Assembled modules, not one principle.** The authors chose this on purpose ("Lego-like", "system to build systems"). No objective ties homeostasis, attention, reward and expression together. Each module comes from a different theory.
- **Mimicry is learned in principle, but the claim is untested.** The mechanism is described and a video is cited (vimeo 123986611). The paper never shows that the map was learned rather than seeded. It gives no accuracy figure, no measure of how many caregiver mirrorings it takes, and no non-contingent control. Its success criterion also leans on reward: the caregiver's praise releases dopamine. That makes the user's positive affect a reinforcer, which Principle 6 forbids.
- **Emotion is hand-named.** Stress, oxytocin and dopamine are named state variables, and temperament is a dial. This conflicts with Principle 2.
- **Persistence.** No statement says that state or learned weights persist across sessions or days. The demos are single sessions.
- **Ablations.** Proposed ("could be an effective way"), not run.
- **Evaluation.** Demos only.

## License
© ACM 2016. No code. BabyX and BL are proprietary (University of Auckland, later Soul Machines).

## Runs on this Mac without a GPU?
n.a. No public code.

## Verdict: watch (read), as the closest precedent for the learned self–other face map and for a muscle face. Reject it as an architecture.

## What it implies for this engine
- **Brief clause "muscle-driven face":** confirmed, with one qualification. The real-time face interpolates an expression space precomputed by FEM. This is the same move the brief plans for S4 (a muscle model trained on ArtiSynth simulations). BabyX shows that it renders convincingly in real time. It also shows nothing about learning, because the muscle space was given.
- **Brief clause "subcortical circuits":** confirmed (basal ganglia, colliculus, pulvinar, amygdala, hypothalamus, brainstem CPGs).
- **Brief clause "ablations were planned and never run":** this paper proposes lesions as a future validation route. No lesion result appears here or in the 2022 and 2023 papers read for the sibling notes. "Never" cannot be proven from three papers. Write it as "proposed (2016) and not reported since".
- **Brief clause "no controlled evaluation":** confirmed for 2016. The 2023 paper adds a controlled human study, but BabyX is not measured in it (see babyx-2023-turn-taking.md).
- **Brief clause "no conceptual layer":** true of this paper. Later papers add a rudimentary one (event representations, episodic memory, word learning, an introspective "I like dogs" mode). Qualify the clause.
- **Brief clause "no long-term living":** no evidence of multi-day persistence in anything read. Confirmed as "not reported".
- **What survives the Principles:**
  - The specific mechanism: babbling, then contingent caregiver mirroring, then a delayed association between efference and the visual pattern, giving a bidirectional map. This is exactly the learned self–other face map the engine wants, already proposed for a face.
  - The engine can beat BabyX here by measuring it. Measure map accuracy against the number of mirroring episodes, compare contingent with yoked non-contingent mirroring, and lesion the map and show that reading the other person's face degrades.
  - Do the learning without a dopamine bonus for praise. Contingency alone, or prediction-error reduction, should drive it, so it does not conflict with Principle 6.
  - Keep the delay explicit (see stoytchev-2011-self-detection-temporal-contingency.md).
- **The two-route face** (innate subcortical CPGs plus a learned cortical route converging on one nucleus) matches gothard-2014-amygdalo-motor-facial.md. It is compatible with Principle 2 only if the CPG triggers are body-variable thresholds and not named emotions.
- **Warning from the demos:** audiences "anticipate and seek emotional responses" and reacted as if to a real infant. Strong human response is not evidence of internal state. It is the confound this engine's evaluation has to rule out (ablate the state, and the human response should change).
