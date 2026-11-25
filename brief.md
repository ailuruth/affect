# Design brief: Affect

## Goal (from the operator)

On this Mac, talk with an Ailurini Bot that sees the user's face, hears their voice, and answers with a face and a voice of its own. Its expressions must come from an internal state that persists across turns and days, changes what it says and does, and is learned by living with the user. The target is a working system grounded in cognitive science and affective neuroscience, not a talking head that reproduces the statistics of human video.

## Long-term goal (from the operator)

- Talk with an AI on this Mac the way one talks with a person: two-way, largely unconscious emotional exchange through faces and voices, where each side's expression moves the other's state and the timing feels right. Success is measured on the human too: the operator's own face should come to follow the AI's, as people's faces follow each other.
- An AI that acquires its emotions, its manner of speaking and its expressions by living with people, starting from an innate body and reflexes, the way an infant does, and not by training on emotion data.
- A face that works like a human face: muscles, skin and timing driven from inside, perceived and produced through the AI's own body rather than through someone else's coordinate system.
- One system that holds every element of emotion that cognitive science and affective neuroscience consider necessary, each shown by ablation to matter. That makes it a testbed where competing theories (for example, whether feeling lives in fast subcortical circuits or in conceptual interpretation) predict different outcomes.
- What this does not claim: that the system feels. The claim is functional, and the brief keeps it that way. The question stays open and is recorded, not answered.

Beyond S2, in order:
- S4, its own body. The engine's own inverse model, learned by reproducing faces with its own face, replaces borrowed face coordinates (MediaPipe) in the body route. A muscle model trained on ArtiSynth simulations replaces the action-unit face, behind the same interface.
- S5, two-way contagion. Claim: the operator's facial activity measurably follows the AI's expressions, and removing the AI's emotional pathway removes that following.
- S6, months of living, through Ailurini with the operator. Claim: a stable temperament and a relationship specific to the operator form, and survive restarts and model upgrades of the conceptual layer. Removing state tagging from replay removes that specificity.

## Prior work

Prior work to beat on substance, not looks:
- Data-driven conversational avatars (Avatar Forcing, AVTR-1, Meta Seamless Interaction). Natural motion, but no internal state. The face nods because people nod there, and the language model never knows its face smiled.
- BabyX (Sagar, CACM 2016). Muscle-driven face and subcortical circuits, but no conceptual layer, no long-term living, and no controlled evaluation. Ablations were planned and never run.
- Active inference models of affect (Smith, Parr and Friston 2019; Hesp et al. 2021) and homeostatic RL (Yoshida and Man 2024, 2025). The right principles, shown only in T-mazes and grid worlds.

## Principles (decided, do not reopen)

1. No emotion classifier anywhere. The user's face and voice enter as continuous low-level features (face blendshapes or action units, prosody), never as labels such as "happy".
2. No hand-named emotion variables. What is innate is a set of body variables to regulate and a few reflexes. Emotion is structure that emerges in a learned latent state, and valence or arousal are read out of it, not set.
3. Others are read through the agent's own body. Perceived features drive the agent's own motor and affect pathways (mimicry), and the agent infers another's state by inverting its own generative mapping (Yoshida and Man).
4. Claude is the conceptual layer. It names, reinterprets and regulates states and writes the words. It never drives frames, and the fast loop never waits for it. It never reads the state below it as numbers or words: no body values, latent values or state labels in its prompt. The state reaches Claude only by changing how it processes (see Coupling to Claude). A test of the shortcut, P1, found that numbers shown to Claude change nothing.
5. Every component has a stated theory basis, changes behavior, and has an ablation prediction written before it is built: remove it, and this specific behavior should change.
6. Homeostasis, not reward maximization. Every body variable is satiable. No reward for the user's smiles, attention or time spent, because that trains flattery.
7. Webcam and microphone data never leave this Mac. Replay stores feature streams, not raw video or audio.
8. The face's appearance is a visual identity decision. Use a neutral placeholder until the operator approves a look.
9. The engine is a separate project. All modeling, training, replay and experiments live in their own repository, in whatever language fits (Python with PyTorch on Apple silicon is expected). Ailurini is only the interface the operator will later talk through, and gets nothing but a thin client once the engine has earned it.
10. One formal core. The engine is derived from a single stated objective, not assembled from modules. Every component (homeostasis, curiosity, valence and arousal, mimicry, reading others, regulation, replay) must follow from the core's equations or be an explicit constraint on them, and every ablation prediction is derived from the equations rather than guessed. A component the core does not produce is not added. This is what separates the engine from BabyX, Kismet and data-driven avatars, which are well-built assemblies without one principle.

## Foundations research (S0, the current focus)

The operator's direction: first do the most creative research possible, to lay the mathematical and ML/DL foundations of the engine. Creativity applies to the theory and the model. It does not relax the Principles or the Evaluation rules: claims are still judged by accepted instruments, and sources are still read in the original.

The goal of this phase is a small set of serious candidate foundations, each a formal account from which the components in Principle 10 can be derived, and each backed by derivations, by the research it rests on read in the original, and by independent critique, rather than prose. Experiments on published data come after the operator picks designs to build (research/questions.md, Q16). Novel formalisms and syntheses across fields are wanted, not only existing frameworks. The operator chooses the core from the candidates; formalism.md is written after that choice.

The operator's judgment: existing architectures are not enough, and this phase exists to invent one. Existing frameworks are material, not answers. Rules for the invention:
- Start from the constraints, not from a framework. The constraints that no existing architecture satisfies together are: no labels anywhere below the language layer; emotion as emergent structure, not variables; others read through one's own body; a frozen language model coupled to a continuous-time state without being told that state in words; satiable drives; time scales from reflex to temperament; very little real data; a real-time face. Ask what mathematical object satisfies all of them at once, and derive from there.
- Open problems that an existing framework does not solve and the invention must: how a frozen language model is coupled to a continuous affective dynamical system without text (an interface theory); two agents' models coupled in real time as one dyadic system; learning from one person's few hours a day by leaning on innate structure; emotion concepts emerging from interoceptive and exteroceptive states and being named by the language model (the grounding problem).
- Expressive structure. The operator's experience is that one-dimensional attempts have been tried and have nearly all failed, in prior work and in work with Claude. A candidate whose affective core reduces to a few scalar gauges, a scalar value and linear maps is a sketch, not a candidate. Each candidate must state, and argue from its equations and the research it rests on (to be tested on published data once it is picked for building), the following:
  - Where content-dependent interaction happens, at the level of richness of attention: what the agent needs and expects selects what it perceives, remembers and does, and the selection depends on content, not only on magnitudes. One direction to examine is need-conditioned attention, where the agent's current needs and their expected changes form the query over perceived cues, memories and possible actions, as motivational salience does in the brain (hunger makes food cues salient).
  - How needs and states are structured over people, relationships, episodes, topics and time: as sets, graphs or fields over a learned space, not as a fixed list of gauges.
  - The effective dimensionality of its state, and a behavior that a low-dimensional version of the same candidate cannot produce, demonstrated by ablating the structure.
  - That the richness comes from structure (attention, composition, relations, multiple time scales) rather than parameter count, because real data is scarce.
  A candidate already written that does not meet this is revised before it can be marked complete.
- Diverge before converging. First write at least eight short sketches in research/foundations/sketches/, each from a different disciplinary lens (for example a physicist, a control theorist, a developmental psychologist, a computational neuroscientist, a deep learning researcher, a game theorist, a mathematician of dynamical systems, a linguist), generated by parallel subagents that do not see each other's work. Each sketch states its core object in one equation or diagram, which constraints it meets, and which it breaks. Then pick the most promising to develop in full.
- At least two of the developed candidates must be new, not an existing framework applied as is. A synthesis counts as new only if it adds a mechanism neither source has.
- Candidate A below is an example of the level of formality wanted, not a direction. Do not let it anchor the sketches.
- The comparison judges novelty too: what each candidate can do that none of the prior work in this brief can, stated concretely.

Directions to explore, as a starting point and not a limit:
- Variational and active inference (candidate A below), including dyadic forms where two agents with similar generative models come to synchronize (Friston and Frith 2015, "A duet for one").
- Homeostasis and allostasis as control: drive reduction (Keramati and Gutkin 2014), predictive regulation of a body budget (Sterling), stability and satiation stated as properties to prove, for example with Lyapunov arguments.
- Affect as dynamics: an attractor landscape in the latent state, moods as slow manifolds, shifts of state as bifurcations, multiple time scales from reflex to temperament.
- Coupled agents: interpersonal synchrony and mimicry as coupled oscillators (Kuramoto) or generalized synchronization, and what coupling strength between two agents' states would mean.
- Information-theoretic drives: empowerment (Klyubin et al.), predictive information, curiosity, and their social versions.
- Modeling the other: recursive models of another agent (interactive POMDPs, theory of mind), and reading others by inverting one's own generative model (Yoshida and Man).
- Constructed emotion made formal: emotion concepts as categories learned over interoceptive and exteroceptive states, for example by nonparametric Bayesian clustering, with Claude naming the categories (Smith, Parr and Friston 2019 as the starting point).
- Perceiving the other's face, as part of the same theory rather than a separate pipeline. Directions: analysis by synthesis, where a face is perceived by inferring the parameters that would generate it (Samuel's approach; efficient inverse graphics in primate face processing, Yildirim et al. 2020); predictive coding of faces over time, where perception is the model's running prediction of the next frame; perception through one's own motor model, where the other's face is understood in the coordinates of one's own muscles; the fast coarse, dynamic and body routes in the Perception section as parts of one hierarchical model; how an innate face prior (CONSPEC) and learning by living (CONLERN, Morton and Johnson) combine; and self-supervised video representations (V-JEPA, MARLIN) as learned substrates.
- ML/DL substrates that could realize a candidate: latent world models with interoceptive channels (the Dreamer and RSSM family), state-space sequence models for many time scales, predictive representations without labels or reconstruction (JEPA-style) for perception, amortized inference, and continual learning with generative replay (complementary learning systems).

For each candidate, write research/foundations/<candidate>.md containing:
- The formal statement: variables, their domains, the generative model or dynamics, and the objective.
- Which Principle 10 components it derives, and how, as derivations; and which it cannot. Every candidate must also say how the agent perceives the other's face and voice within it, or name the perception theory it is paired with.
- Propositions with proofs or careful derivations where possible (for example: the drive is satiable; mimicry emerges without being specified; valence as defined is invariant to how the body variables are scaled).
- No validation in toy worlds. A self-built simulated world is a benchmark the project wrote for itself and does not count as evidence for any derived behavior, for completing a candidate, or for comparing candidates. Once a design is picked for building, each derived behavior is tested on published data and tasks used as published, judged on internal state (steering, lesions, coupling beyond surrogates) rather than surface face-matching (for example recorded human dyadic data such as Meta's Seamless Interaction, scored with the analyses in evaluation.md), with code and figures under research/foundations/sims/. Where no published data or task can test a behavior, say so and leave it untested.