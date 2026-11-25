# How should neuroscience study emotions? By distinguishing emotion states, concepts, and experiences

Ralph Adolphs, *Social Cognitive and Affective Neuroscience* 12(1):24–31, 2017, doi:10.1093/scan/nsw153 (PMC5390692; full text). This is the companion piece to Barrett 2017 in the same debate issue (barrett-constructed-emotion.md).

## What was read
The PMC full text, read through a fetch tool that returned summaries and the verbatim quotes I asked for. That covers Table 1 in full and the captions of Figures 1–2. The figures themselves are images, and I did not see their contents, including Figure 2's feature list.

## Claims
- "I view emotion states as evolved functional states that regulate complex behavior, in both people and animals." It is a functionalist definition: "defined by what it does rather than by how it is constituted". It follows that animals "and, in principle, even robots—could nonetheless be in similar emotion states."
- **Three strata.** States, concepts and experiences are distinct. "Just like concepts of planets are not planets, concepts of emotions are not emotions." Being in a state "typically also causes conceptual representations of emotions." He calls the causal interactions between the strata an open challenge.
- **Features of emotion states** (Figure 2 is "not necessary and sufficient conditions, and the list is no doubt incomplete"):
  - a low-dimensional similarity space ("perhaps corresponding to something like valence and arousal");
  - **decoupling**: states "'decouple' stimuli from responses, thus affording much more flexibility";
  - **persistence**: "central states that persist for some time, and so can accumulate a host of contextual information before triggering behavioral decisions";
  - a rich **interface with cognition**;
  - **coordination**: "Given the multiple causal effects of an emotion state, these need to be coordinated in some way";
  - **pre-potent control**: "an 'interrupt' mechanism that can terminate ongoing goal-directed behavior";
  - **learning**: themes recur, but their "specific sensory features ... are highly variable", so emotions "critically involve learning";
  - **social functions**;
  - some **volitional regulation** in adults.
- **Level of complexity.** "Emotions regulate behavior at a level of complexity intermediate to that of reflexes and volitional behavior." Reflexes "do not interface in a rich way with other psychological states."
- **Table 1** classes these as central to an emotion state: emotion–cognition interactions, emotional learning and memory, and eliciting strong emotions with ecological stimuli. It classes these as less central: perceiving others' emotional signals, theory of mind, semantic processing about emotion, and emotion words.
- **On LeDoux.** He agrees that conscious experience confounds the study of emotion. He rejects LeDoux's conclusion that the words "fear" and "emotion" should be dropped, and proposes instead a scientific concept of emotion states "that is not based on conscious experience".

## Evidence
A position paper. Its evidence is the patient S.M., in whom fear dissociates from panic and from fear concepts, and the partial overlap with amygdala lesions in animals. No new data.

## Mechanistic commitments
- A latent state that sits between stimulus and response and integrates context over time.
- One state with many coordinated effects.
- A priority signal that can interrupt the current policy.
- Learned elicitors.
- Concepts are a separate system, caused by the state and able to act back on it.

## What it implies for a single formal core
His three strata match the brief's split: the fast learned state $h$ is the emotion state; Claude's categorization is the concept; and experience is set aside by the brief's non-claim. His "decoupling plus persistence" names what an affect state contributes over a reflex arc: the response depends on accumulated context, not only on the current input. In a single core, that is the difference between a policy conditioned on $o_t$ and one conditioned on a belief state or integrator $h_t$. **Pre-potent control** has to come out of the objective itself. One candidate: when the drive gradient becomes large, it dominates action selection, so the interrupt is not a separate switch.

## What an ablation could separate
- **Decoupling.** Replace $h$ with the current observation. Responses to the same partner expression should then stop depending on the preceding minutes.
- **Interrupt.** Cap the influence of $h$ on policy switching. Ongoing behaviour (a reply in progress, a gaze pattern) should then no longer be cut off by a sudden aversive cue, even though $h$ itself still changes.
- **The concept stratum.** Remove Claude's categorization. On Adolphs's account the state's behavioural effects should survive and only reports change. On Barrett's account differentiation should also degrade. This is one of the engine's theory-discriminating tests (see emotion-elements-synthesis.md).

## Verdict: adopt (feature list and three-strata split)
The functionalist definition is the one the brief already uses. His feature list includes interrupt and decoupling, which the 2014 primitives lack.
