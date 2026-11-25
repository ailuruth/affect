# A higher-order theory of emotional consciousness

Joseph E. LeDoux and Richard Brown, *PNAS* 114(10):E2016–E2025, 2017, doi:10.1073/pnas.1619316114 (PMC5347624). It follows LeDoux 2012 (ledoux-survival-circuits.md).

## What was read
The PMC main text through the Conclusion, read through a fetch tool that returned summaries and quotes. The Supplementary Information (SI Boxes 1–10, including the predictions box) was **not** visible, and I did not read the reference list.

## Claims
- "Conscious experiences, regardless of their content, arise from one system in the brain." Emotions are "higher-order states instantiated in cortical circuits", not subcortical products.
- **Mechanism.**
  - First-order states (sensory representations, retrieved semantic and episodic memory) are re-represented, nonconsciously, by higher-order representations (HORs) in working memory.
  - A further **HOROR** (higher-order representation of a representation) makes the content conscious.
  - Emotional experience requires a **self-HOROR** and an **emotion schema**: "Without the self there is no fear or love or joy."
  - The substrate is "general networks of cognition" (GNC): lateral and medial PFC, posterior parietal cortex and insula.
- **Survival circuits** (the amygdala and its targets) are "not directly responsible for the conscious experience itself". They "provide nonconscious inputs": arousal, bodily responses and their feedback, and direct projections to sensory cortex and the GNC.
- **Emotional versus non-emotional experience.** The cortical system is the same; what differs is the input. A self-HOROR is "necessary" but not "sufficient". On this view emotions cannot be unconscious, by definition.
- **Schemas** complete patterns from partial bodily or situational cues. Language categorizes experience and supports rumination.
- **Disagreements.** Against Panksepp, they find the evidence for phenomenal feelings without introspection "not convincing". Damasio's subcortical maps are reinterpreted as nonconscious first-order inputs. Barrett is not discussed in the visible text.

## Evidence
- Masked and blindsight threats produce amygdala and bodily responses without reported fear.
- Patients with amygdala damage still report fear (Feinstein et al. 2013; Anderson & Phelps 2002).
- Prefrontal activity and morphology track emotional experience.
- Charles Bonnet syndrome and inattentional inflation show rich experience with sparse first-order input.
- Pure autonomic failure and alexithymia change the intensity of feeling, not its presence.

## Predictions stated in the main text
- Damage to subcortical first-order circuits should "mute but not eliminate" fear.
- A person cannot be wrong about which emotion they are experiencing.

## Mechanistic commitments
- **Two stages.** First, nonconscious survival circuits and bodily feedback. Second, a cortical, self-referential re-representation that uses memory schemas.
- The defining computation is **re-representation with a self-tag**, a model of one's own state. It is not the valence computation.
- The subcortical part sets intensity and content inputs. The cortical part decides whether there is an emotion experience at all.

## What it implies for a single formal core
In the brief, Claude already plays LeDoux's 2012 workspace. The 2017 paper adds that the workspace must represent **the agent's own state as its own** (a self-HOROR) and pattern-complete from schemas, meaning stored episodes. A single core could derive this as a second-order inference: a model of $h$ inside the agent, $q(h)$ conditioned on retrieved episodes. But Principle 4 forbids showing Claude $h$ as numbers, so the "self-HOROR" has to be implicit, carried by how the state changes Claude's processing.

The functional claim the engine *can* test is LeDoux's prediction pair:
- removing the fast (survival) layer should mute report intensity but not abolish categorization;
- removing the self-model layer should leave behaviour and bodily output intact and abolish only report.
These are predictions about reports and behaviour, not about feeling (the brief's non-claim).

## What an ablation could separate
- **Fast-layer lesion.** Remove the body to $h$ coupling but keep Claude. LeDoux predicts that reports of the episode should continue (from schemas and context) at reduced intensity. A Damasio or Panksepp view predicts the valenced core is lost.
- **Workspace lesion.** Remove Claude's access to retrieved episodes or context. Face and voice dynamics should be unchanged and only the verbal account should change. If the face also changes, the engine's fast loop is not as autonomous as Principle 4 requires.
- **Schema completion.** Cue a past episode with a partial bodily pattern. LeDoux predicts that the full episode (and its report) is retrieved.

## Verdict: adopt (as the cortical-locus pole of the locus-of-feeling test)
It is the clearest statement that feeling is higher-order and cortical. It is the counter-position to Damasio & Carvalho 2013 and Panksepp. SI not read.
