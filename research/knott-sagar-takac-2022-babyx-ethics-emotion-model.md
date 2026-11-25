# The ethics of interaction with neurorobotic agents: a case study with BabyX

Knott, Sagar and Takac, *AI and Ethics* 2:115–128, 2022 (online 21 July 2021), doi:10.1007/s43681-021-00076-x. Open access, CC BY 4.0.

## Source read
The full article HTML from the Internet Archive snapshot (2025-10-26) of the Springer page. Live Springer served a JavaScript challenge, so the archive was the only readable copy. Read closely: Abstract, §2 (features of BabyX), §3 (motivation, including the commercial link), §5 (user-related harms), §6.4 (BabyX's model of emotions, the only detailed public account of it), §6.5 (comparison with the company's commercial agent) and §7. Skimmed: §4 and §6.1–6.3, which are philosophical (Danaher's ethical behaviourism, Smids).

## Claims
- BabyX's emotions come from a brain-like mechanism, unlike the company's commercial "Level 2 Person", whose emotions are authored if–then rules. That difference is ethically relevant, against narrow ethical behaviourism.
- Mistreating a realistic baby avatar may carry over to the treatment of real babies, so access is restricted. "BabyX is currently only used by its developers, and by subjects participating in child development experiments".
- Emotionally vulnerable users (for example after losing a baby) may become attached "to something that cannot truly reciprocate".

## Architecture of emotion (§6.4, as given; no equations)
- **Core: hand-named stimulus–response circuits.** "At the core of the model of emotions implemented in BabyX is a set of stimulus–response rules that are rather similar to the 'if–then' rules of the commercial avatar." There are six circuits: "'approach/interest', 'joy', 'fear', 'anger', 'distress' and 'startle'", after Panksepp. Example: approach/interest "is triggered by human speech with a certain timbre and pitch contour, and triggers a lowering of the eyelids, and a smile."
- **Neurochemical state.** The circuits drive "a vector of 8 neurochemical concentrations". Approach/interest releases dopamine and oxytocin; joy releases dopamine; fear and anger release norepinephrine and cortisol. Cortisol raises heart and breathing rate and oxytocin lowers them. Norepinephrine raises a motor acceleration parameter, so movements become jerkier.
- **Goals and learning.** The dopamine circuit "controls the agent's operant learning, so the agent is led to do things that lead to certain emotions". Arbitrary stimuli become associated with emotions.
- **Selection.** Emotional behaviors inhibit each other through basal-ganglia action selection. Sudden switches (for example fear snapping to anger) "using catastrophe theory".
- **Cortical layer.**
  - Cortical representations receive subcortical and neurochemical input and feed back into them, forming a dynamical system with attractors. "These attractor points correspond to higher-level emotions."
  - The examples are hand-specified compositions:
    - sulking = anger + withholding action;
    - nostalgia = joy + episodic recall;
    - confusion = distress + low confidence in the next-event prediction.
- **Episodic memory.** Stores event sequences, predicts the next event and is used for action choice. Storage is weighted toward emotional and surprising events. The model has "elements of Tulving's 'autobiographical self'" but "not yet… an explicit representation of 'self'".
- **Introspection.** "A special cognitive mode where representations of world objects are activated… by the strength of their association with the agent's current emotional state… This process generates stative propositions… such as 'I like dogs'."
- **Body.** Simulated tactile receptors, including stroke-sensitive mechanoreceptors; recoil and startle reflexes.
- **Commercial link.** Soul Machines' "Digital People" are "built using engineering AI methods, rather than brain modelling methods", with some BabyX components incorporated (eye and body motor system, perceptual and emotional system).

## Evidence with numbers
None. This is an argument paper. The authors' own assessment: "BabyX's brain model, while much more complex than that of a Level 2 Person, is still extremely simple"; "still very simple, and likely to be wrong in many respects".

## Failure modes, reported or evident
- **Emotion is wired and named.** Six named basic-emotion circuits and eight named neurochemicals are the innate core, the reverse of Principle 2. Higher emotions are named compositions chosen by the designers, not structure discovered in a learned latent space.
- **Assembled.** Panksepp circuits, catastrophe theory, Scherer-style attractors, Tulving and Damasio are each bolted on. No single objective links them.
- **Reward for social signals.** Approach/interest is triggered by infant-directed speech and releases dopamine and oxytocin, which are also the operant learning signal. The agent is therefore pushed to elicit the caregiver's speech and affect, the flattery path Principle 6 rules out.
- **No evaluation and no ablation** of the emotion model.
- **Persistence.** Episodic memory is described, but persistence across sessions or days is not discussed. Use is restricted to developers and lab experiments, so no long-term living with a user took place.

## License
CC BY 4.0. No code (proprietary).

## Runs on this Mac without a GPU?
n.a.

## Verdict: watch (read). It is the only public description of BabyX's emotion model, and it shows that model conflicts with Principles 2, 6 and 10.

## What it implies for this engine
- **Correction to the brief's framing.** BabyX's emotions are not only "subcortical circuits". At the core they are hand-named basic-emotion rules plus named neuromodulators, and the authors compare them to if–then rules themselves. The brief's sharpest differentiator against BabyX is therefore Principle 2 (no named emotion variables) and Principle 10 (one objective), not only the missing conceptual layer and long-term living.
- **"No conceptual layer"** should become "a rudimentary conceptual layer". BabyX has episodic memory, emotion–object associations and a self-report mode that produces "I like dogs". What it lacks is a language model that names and regulates states without being shown them (Principle 4). Its introspection reads the emotion state directly, which is what Principle 4 forbids Claude to do.
- **Ethics.** The developers restricted access because of user attachment and carry-over effects. That supports the companion-harm notes already in the index and argues for the engine's evaluation logging the operator's dependence, not only engagement.
- **Pattern to borrow:** episodic storage weighted toward emotional and surprising events. It matches the brief's "state tagging in replay" (S6); see mcgaugh-2004-amygdala-modulates-consolidation.md. Here it is asserted, not ablated, and the engine's version must come with the S6 ablation.
