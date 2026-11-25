# Hayes, Krishnan, Bazhenov, Siegelmann, Sejnowski & Kanan 2021, "Replay in Deep Learning: Current Approaches and Missing Biological Elements" (Neural Computation 33(11):2908-2950; arXiv 2104.04132v2)

Source read: the arXiv v2 PDF (28 May 2021, 56 pages), read in full on 2026-11-25: Sections 1-5, Table 1, Figures 1-3 captions, and Appendix Table 2. Of the reference list, I only checked specific citations. I read the arXiv preprint, not the typeset Neural Computation version, so page-level wording may differ.

This is a review. It reports no experiments of its own. Its numbers are those it cites, and none of the cited primary studies was read for this note.

## Claims
- Biological replay replays "highly processed representations of past inputs". Most deep-learning replay stores "veridical inputs (e.g., RGB images)". Representational replay (REMIND, AR1*, BI-R) is "closer to biology".
- Consolidation is staged. The hippocampus learns fast, with "sparsity and indexing mechanisms". The medial prefrontal cortex uses "a slower learning rate and densely encoding memories with overlapping representations". The hippocampus-to-cortex switch takes "several days with several episodes of sleep", but making a memory fully hippocampus-independent "can take months or even years". "Replay during sleep determines which memories are formed for long-term storage."
- Sleep stages divide the work. NREM sleep "is associated with transfer and storage of recent experiences". REM sleep "is associated with organizing internal representations", "abstraction", protection "against interference", and "REM also selectively promotes consolidation of emotional memories (Baran et al., 2012; Wagner et al., 2001)". NREM dominates early in the night and REM late.
- Replay is selective and partial. "Weakly learned information was replayed more frequently" (citing Schapiro 2018). Selective replay is "motivated by fear (de Voogd et al., 2016) and reward". Old memories "that overlap with new memories are in the most danger ... and are preferentially replayed" (citing McClelland 2020). Partial replay "allows relevant memories with shared components to be blended", supporting generalization and schemas.
- Replay of recent experience fades. Correlations with recent experience decay "over several sleep cycles", and the decline in hippocampus and prefrontal cortex happens "within a matter of hours". REM then resets hippocampal excitability, "which may allow the hippocampus to encode new memories".
- Replay may change memories rather than copy them. Sleep may re-assign "different subsets of neurons and synapses to effectively orthogonalize memory representations" (citing González 2020).
- The gaps they list (Table 1, Section 4):
  - Artificial replay comes from a single layer, while biological replay happens in several regions, both independently and in coordination.
  - Buffers are not purged.
  - There is no notion of waking versus sleep phases.
  - Selection is uniform.
  - REM is ignored.
  - Replayed samples are "static, uncorrelated inputs", with no temporal order and no reverse replay.
  - Replay does not depend on novelty.
  - Regularization and replay "have largely been explored independently". In the brain, "normalization and synaptic changes co-occur with replay".
  - No model lets the neocortex network influence training of the hippocampal network.
  - "Epigenetic tagging mechanisms in medial prefrontal cortex have largely been ignored."

## Evidence (as cited in the review)
- Oscillations that carry replay: hippocampal sharp-wave ripples at "100-200 Hz", spindles at "7-14 Hz", and slow oscillations below "1 Hz", all nested (Staresina 2015). Cortical replay occurs during spindles and the active states of slow oscillations.
- Reverse replay is tied to reward, and "the strength of this reversal is correlated with the reward magnitude" (Ambrose 2016).
- Motor cortex replay during NREM selectively raises task-related activity and lowers task-unrelated activity after sleep (Gulati 2017). The review reads this as replay solving credit assignment.
- Memory allocation: new memories allocate neurons in both hippocampus and mPFC. The mPFC neurons are "epigenetically 'tagged' for later storage" (Kitamura 2017; Lesburguères 2011).
- Machine-learning selection results:
  - Chaudhry 2018: storing a class-mean feature vector worked best, but "uniform random sampling performed nearly as well".
  - Aljundi 2019a (maximally interfered retrieval): replaying the samples that an upcoming update would harm most beats random replay.
  - Isele & Cosgun 2018, the result most relevant to us: selection "based on TD error and absolute reward did not work well in mitigating forgetting, while selection based on distribution matching and state-space coverage had comparable performance to an unlimited replay buffer".
  - Large-scale supervised studies find uniform sampling "surprisingly well" (Hayes 2020; Wu 2019a).
- Formal setup: incremental batch learning D = ⋃_{t=1}^{T} B_t, with B_t = {(x_i, y_i)}_{i=1}^{N_t}. Streaming learning is the special case "N_t = 1" with a single epoch. The review argues streaming is the case biology faces.

## Mechanism
The review gives no equations of its own. The mechanisms it describes:
- Spontaneous replay through attractors. Neuromodulation in NREM (lower acetylcholine and monoamines, more GABA) reduces excitability and strengthens excitatory coupling. Random activity then falls into attractors laid down by learning, so the replayed content "reflects patterns of synaptic connectivity ... rather than the intrinsic state of neurons". Crick & Mitchison (1983) replay randomly chosen attractors in order to unlearn them. Robins & McCallum (1998) replay them in order to relearn them.
- Fast and slow weights on the same connection (Hinton & Plaut 1987). Fast weights learn the new material and slow weights drive generative replay (Robins 1997, 2004). This alternative to complementary learning systems uses no separate hippocampus.
- A taxonomy of supervised replay (Fig. 3):
  - veridical replay (iCaRL, GEM, BiC and others);
  - representational replay (REMIND, FA, AQM, AR1*);
  - generative veridical replay (DGR, FearNet, GDM, MeRGAN and others);
  - generative representational replay (BI-R, DAFR).
- What to replay is an open selection problem. The candidates named are:
  - uniform sampling;
  - TD error (Schaul);
  - absolute reward;
  - distribution matching or reservoir sampling;
  - state-space coverage;
  - maximal interference;
  - gradient-based diversity (GSS);
  - similarity or overlap with new learning (McClelland 2020);
  - weak learning;
  - fear;
  - novelty.

## License
arXiv non-exclusive distribution license (arxiv.org/licenses/nonexclusive-distrib/1.0). There is no code.

## Runs on this Mac without a GPU?
Not applicable. This is a review. The methods it cites range from trivial (a reservoir buffer) to heavy (GAN generators).

## Implications for the engine (our inferences unless quoted)
- **Define phases explicitly.** The review's strongest structural point is that complementary learning systems presuppose separate "awake and sleep states" and that most artificial replay has none. For us, offline replay should be a separate engine phase, run when the operator is absent, with its own regime. NREM-like replay consolidates the day's tagged episodes into the slow store, interleaved with older material. REM-like replay generates recombinations and abstractions and gives emotional episodes extra weight. The NREM/REM split is a documented division of labour, not decoration, and it gives two separately ablatable phases.
- **Salience weighting alone will not protect old knowledge.** Isele & Cosgun found that selecting by TD error or absolute reward did not mitigate forgetting, while distribution matching and coverage matched an unlimited buffer. Our hypothesis: a replay scheduler weighted only by affective salience (arousal, body-variable error, operator intensity) would make the engine better at intense moments and let calm, everyday operator interactions fade. A relationship lives in the everyday. So the replay distribution should mix (a) a coverage or reservoir component over all tagged episodes, which protects against forgetting, with (b) a salience or surprise component, which speeds learning. The mixing weight is a parameter to ablate. This matches the Schaul note's caution about |δ| priorities.
- **"Weakly learned" and "overlapping" are the right selection signals for a relationship.** For a partner-specific mapping, the memories most at risk from new partner data are those that overlap with it: other people's similar expressions, and the operator's own earlier states. Selection by overlap (McClelland 2020) or by maximal interference (Aljundi 2019a) targets exactly the interference that would erase "how I respond to others" while learning "how I respond to the operator". Both can be computed from the engine's own gradients or similarity in latent space, without labels.
- **Purge and decay.** Biological replay of recent material fades "within a matter of hours" and over several sleep cycles. For us, the fast store should hold a day or a few days of tagged episodes, then release them once consolidated. A permanent raw buffer is unbiological and conflicts with privacy pressure. A bounded buffer of feature streams already fits Principle 7. What happens to consolidated episodes in the fast store (erased, or kept but silent) is an open question the review names. It decides whether reconsolidation can revisit them.
- **State tagging as allocation.** The review's mention of mPFC neurons "epigenetically 'tagged' for later storage" at encoding is the nearest biological cousin of S6's "state tagging". In that reading, the tag is set at encoding by the state at the time and marks which slow-store units the episode will be consolidated into. It is not just a label on the replay buffer. A precise version for us: at encoding, the engine's internal state (body-variable deviations, latent affect coordinates) selects or biases a subset of slow-store units or a prior mode, and offline replay regenerates the episode through that same subset. This is our synthesis. The review does not say it.
- **Replay should be multi-level and sequential.** Biology replays in several regions and in temporal order, including reverse order tied to reward. For an engine whose content is timing and contingency between two faces, static replay of single frames throws away the thing to be learned. Replay sequences of latent states, possibly in reverse from body-variable relief, which approximates backward credit assignment.
- **Couple replay and regularization.** Synaptic normalization during sleep and replay co-occur (Tononi & Cirelli). The review's proposal is "replay informed regularization" and "regularization informed replay". For Principle 10 this is an argument for a single objective in which an importance or precision term and the replay distribution come from the same quantity, rather than two bolted-on modules.

## Verdict: watch (as a map; no mechanism to adopt directly)
- Useful as a checklist of what an engine claiming "replay" should have, and of what our S6 ablation must vary: phases, selection rule, buffer decay, sequence versus static samples, and the replay level.
- One concrete, usable warning: salience-only selection does not prevent forgetting. Coverage-based selection does.
- It does not derive anything. Its biological claims are second-hand summaries. Where a claim matters to a design choice (REM and emotional memory, epigenetic allocation tags, preferential replay of weak memories), the primary sources need to be read before we rely on them.
