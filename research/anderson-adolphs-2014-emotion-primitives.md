# A framework for studying emotions across phylogeny (emotion primitives)

David J. Anderson and Ralph Adolphs, *Cell* 157(1):187–200, 2014, doi:10.1016/j.cell.2014.03.003 (PMC4098837, NIH author manuscript). PMC gives the title as "...across Phylogeny"; Caltech's repository lists it as "...across Species".

## What was read
The PMC full text, read through a fetch tool that returned summaries plus verbatim quotes I asked for. It covered the main text through "Future Directions" and the Box 1–4 text (the first 100k of 143k characters; the rest is references). Figures were seen only as captions. I did not read the text line by line, so the quotes below are the ones I asked for, not a full reading.

**Correction to the brief's candidate list.** This paper does not list seven primitives. Its named "building blocks" are **scalability (intensity), valence, persistence and generalization**. Within generalization it adds **pleiotropy** (several parallel effects) and **trans-situationality**. Global coordination is the paper's "acid test", not a primitive. Learning is covered in Box 3. Social communication comes up as expression, not as a primitive. "Automaticity" does not appear as a primitive. The seven-item list in the brief probably comes from Adolphs & Anderson's 2018 book, which I did not read.

## Claims
- An emotion is "an internal, central (as in Central Nervous System) state", triggered by stimuli, that causes behavioural, cognitive, somatic and physiological responses. "Emotional behaviors are a class of behaviors that express internal emotion states."
- "Valence and intensity can be thought of as evolutionary building blocks of emotion, or emotion 'primitives.'" The paper then covers:
  - **Scalability:** graded intensity. At high intensity the response can change in kind (freezing gives way to flight; an octopus switches from camouflage to ink jetting).
  - **Valence:** Darwin's principle of antithesis (opposed postures for opposed states).
  - **Persistence:** "these behaviors, or associated state variables, often outlast the stimuli that elicit them."
  - **Generalization:** "context generalization, or 'trans-situationality'"; "Emotion States are also pleiotropic, meaning that they have multiple, parallel effects."
- **Mechanism:** the central state "could be a neuromodulator system, a neuroanatomical structure, a distributed neural network, a type of firing pattern", or a combination, possibly spread over "distinct but coupled systems". The paper suggests that "increases in the scalar value of state parameters ... may reflect the integration or accumulation over time of sensory inputs", and that "many instantiations of neural integrators require persistent activity of some sort".
- **Feelings are set aside:** "animals, like humans, have central emotion states even if they are not consciously aware of them."
- **Robots:** "if robots lack central emotion states, then by definition they lack 'emotions.'"
- **Hunger** is "sometimes called a 'homeostatic emotion'". The paper draws no sharp line between emotion and drive.
- **Learning (Box 3):** Pavlovian conditioning lets "multiple stimuli, through learning, to access or evoke an emotion state."

## Evidence
A review. The examples are fly air-puff hyperactivity that depends on dopamine; *C. elegans* roaming states; P1-neuron activation that produces singing lasting "for minutes"; Asahina et al.'s tachykinin neurons, which change several aggressive behaviours in parallel; CeM manipulations that change behavioural, autonomic and endocrine fear outputs together; and the honeybee "pessimistic cognitive bias" after shaking. Almost no numbers are given.

## Mechanistic commitments
1. A **central state variable** that sits between stimulus and response. It is not a reflex arc.
2. **Temporal integration**: the state accumulates evidence and decays slowly, so persistence is integrator dynamics.
3. **Fan-out**: one state drives many effectors at once.
4. **Nonlinear output mapping**: intensity can switch which behaviour is selected.
5. **Learnable input mapping**: new cues come to evoke the same state.

## What it implies for a single formal core
The primitives are properties to measure in the engine's learned latent $h$. They are not variables to name (Principle 2), and each corresponds to a measurable property of the core's dynamics:
- persistence is a relaxation time of $h$ that is longer than the stimulus;
- scalability is a graded drive whose policy readout changes regime with intensity, for example through a bifurcation;
- pleiotropy means one low-dimensional direction in $h$ moves face, voice, policy and memory retrieval together;
- generalization means distinct inputs map onto the same region of $h$.

The authors' "acid test" is to perturb the state and see whether several outputs move "in a parallel, coordinated manner", as with the circadian clock. That test transfers directly to a perturbation in the latent space of a simulation.

## What an ablation could separate
- **Persistence:** reset $h$ every step, or shorten its time constant. Outputs should then track the stimulus with no aftereffect. In the engine this means no carry-over of affect after the partner's face turns neutral.
- **Pleiotropy versus separate channels:** give each output channel its own private latent. Perturbing one channel's latent should then leave the others unchanged; with a shared latent, they all move.
- **Learning:** freeze the input mapping. Only innate triggers should then evoke the state.
- **Scalability:** linearize the policy readout. The change in behaviour class at high intensity should then disappear.

## Verdict: adopt (as the measurement checklist for "is this an emotion state")
Four primitives plus pleiotropy, and a perturbation test. These primitives are testable properties of a latent state, consistent with Principles 2 and 5.
