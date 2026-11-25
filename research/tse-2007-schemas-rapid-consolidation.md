# Tse et al. 2007, "Schemas and memory consolidation" (Science 316:76-82), with McClelland 2013's CLS account of it

Tse, D., Langston, R. F., Kakeyama, M., Bethus, I., Spooner, P. A., Wood, E. R., Witter, M. P. & Morris, R. G. M. (2007). *Science* 316(5821), 76-82. doi:10.1126/science.1135935.
Read together with: McClelland, J. L. (2013). "Incorporating rapid neocortical learning of new schema-consistent information into complementary learning systems theory." *J Exp Psychol: General* 142(4), 1190-1210. doi:10.1037/a0033812.

## Source read (honestly: not the primary paper)
Read on 2026-11-25.
- **Tse et al. 2007 itself: not read.** It is closed access (OpenAlex and Semantic Scholar list no OA copy). The one hosted copy returned 403, and so did a PhD thesis on CORE. I did not try to get around either block. I read the PubMed abstract only.
- I did not read the Supporting Online Material.
- **Read in full for the relevant parts:** McClelland 2013, from the stanford.edu PDF. That covers its description of Tse 2007, including the reproduced Figure 1 caption; Simulation 1 (methods, results and the "Further exploration" mechanism analysis); the Limitations; and the General Discussion. I skimmed Simulations 2/2′ (the Tse 2011 gene-expression analogue) and Simulation 3 (competitive learning).
- **Read:** Kumaran, Hassabis & McClelland 2016 (*TICS*), section "Rapid Schema-Dependent Consolidation" and Box 8.
- **Abstract only:** the exchange in *Neurobiol Learn Mem* 89 (2008). Rudy & Sutherland's "Is it systems or cellular consolidation? Time will tell" (I saw no abstract text) and Tse et al.'s reply, "It's not just time".
- Every number below about the rat experiment is therefore secondary, taken from McClelland 2013 and Kumaran 2016. A search-engine summary said hippocampal lesions at 3 h abolished the new memory. I could not verify that against the paper, so it is not used as evidence here.

## Claims (abstract, verbatim)
- "systems consolidation can occur extremely quickly if an associative 'schema' into which new information is incorporated has previously been created."
- "the memory of flavor-place associations became persistent over time as a putative neocortical schema gradually developed. New traces, trained for only one trial, then became assimilated and rapidly hippocampal-independent."
- "Schemas also played a causal role in the creation of lasting associative memory representations during one-trial learning."

## Evidence (as described by McClelland 2013 and Kumaran 2016)
- **Apparatus.** A 1.6 m × 1.6 m "event arena" with landmarks and transparent walls. Sand wells sit at six locations, with four start boxes, one in the middle of each side.
- **Training.** In the start box the rat gets a cue flavour, then must find a larger sample of that flavour buried at the paired location. There were six flavour-place paired associates (PAs), with "one training trial with each flavor in each daily session". Unrewarded probe trials showed "gradual learning over 16 training sessions" (Kumaran: "multiple sessions distributed over several weeks"). The learning was hippocampus-dependent.
- **Critical session.** On day 20 (per the Figure 1 caption), four old PAs were trained as usual and two were replaced by new PAs at new locations near the old ones. Each new flavour got one trial. At a probe the next day, rats searched "at the new cued location far more than other locations".
- **Lesion.** 48 h after exposure, rats received extensive hippocampal or sham lesions. After recovery, lesioned rats "retained both the original and the new flavor-place associations". Only controls could learn a further pair of new PAs (the "9 and 10" set).
- **Schema dependence.** Intact rats given two new PAs in a novel arena showed no one-trial learning. Their learning there was "at the same slow pace as acquisition of the first set".
- **Follow-up (Tse 2011, via Kumaran 2016).** Neocortical plasticity-related gene expression was "significantly greater ... very shortly (80 minutes)" after new PAs in the familiar arena than after new PAs in an unfamiliar one.
- **Disputed interpretation.** Rudy & Sutherland 2008 propose that excitotoxic hippocampal lesions disrupt cortical *cellular* consolidation through transient aberrant activity. On that reading the 48 h result reflects cellular, not systems, consolidation. Tse et al. 2008 "disagree ... and cite relevant data in our original paper", and they outline experiments to separate the two accounts. I read neither argument beyond the abstracts.

## Mechanism
The paper's own account, from the abstract and the secondary descriptions: a neocortical schema (a structured map of the arena's flavour-place relations) builds up slowly with hippocampal help. Once it exists, a single hippocampally encoded new association is assimilated into neocortex within about 48 h. Kumaran 2016 adds: "even a few minutes with the hippocampus intact could allow multiple replays, each one incrementing the strength of intra-neocortical connections."

**McClelland 2013's computational account (stated precisely).**
- **Network.** The Rumelhart semantic network: 8 item inputs plus 1 spare input for the new item, and 4 relation inputs. These feed 8 representation units, then 15 hidden units, then 36 outputs. Output biases are fixed at −2. Weights are initialised U[−.45, .45]. Plain backprop with learning rate .1, no momentum and no weight decay. Schema pretraining was 1,000 epochs over 32 examples.
- **Test.** New items, each with 2 examples (isa and can). Consistent items: trout (a fish that swims) and cardinal (a bird that flies). Inconsistent item: penguin (a bird that swims). Focused learning (new items only) was compared with interleaved learning (new items plus all 32 old ones). Learning rate and all parameters were identical across conditions.
- **Result.** Focused learning of consistent items is fast and produces little interference with known animals. Penguin learning is slow and degrades related items. Interleaving slows even consistent learning slightly and is needed only for inconsistent items.
- **Why.** Gradients from a consistent item's targets propagate coherently back to the input→representation weights of the new item's input unit. Those weights alone almost suffice. The efficiency index measures the coherence:
  - TC = Σ_ij |w_ij^after − w_ij^before| over the whole training run;
  - SC = Σ_{p,e} Σ_ij |Δw_ij| summed over every single presentation p in every epoch e;
  - EI = TC / SC.

  EI = .93 for new consistent PAs vs .27 for the inconsistent "new map" condition. For an inconsistent item, error signals cancel within and across examples. Freezing everything except the new item's input→representation weights still learns trout and cardinal: within 20 epochs every output is nearer correct than incorrect. It fails for the penguin and the nonsense items even after 100 epochs.
- **Theory amendment.** "Complementary learning systems and interleaved learning are necessary when learning new information if that information is not consistent with the structure of known information." Neocortical learning should be described "not so much as fast or slow but as prior-knowledge dependent". The hippocampus's apparent prior-knowledge independence is itself conditional, because the features it binds come from slowly learned neocortex.
- **Stated limits.** Unidirectional propagation; backprop's biological status; residual interference from even a few inconsistent presentations; and the model "does not address" why the novel-map learning itself is slow beyond a general similarity.

## Implications for the engine (our inference, not the authors')
**A partner schema is the thing months of living build.** In S6, "a relationship specific to the operator" is a slow-store structure over this person: how their face and voice move, and what follows what (their expression → the engine's state change → their response). Tse's timeline matches the brief's: slow, interleaved, replay-dependent acquisition over weeks. After that, one-exposure learning of new items consistent with the schema becomes possible.

**A concrete testable S6 claim follows.** The number of exposures needed to learn a *new* operator-specific contingency should fall over the months, for contingencies consistent with what the engine already knows of the operator. It should not fall for arbitrary or inconsistent ones, or in a novel context (the novel-arena control).

**How a partner-specific mapping forms without forgetting others.** In McClelland's network, a new item gets its own input unit, and learning lands mostly on that unit's weights into a shared representation space. Mapped onto the engine:
- each partner (and perhaps each recurring situation) has its own embedding e_k into a shared latent space;
- new partner-specific learning first goes to e_k, the "item code", which by construction cannot disturb other partners' codes;
- shared weights change only to the degree the item code cannot absorb the error.

This is an architecture, not a regulariser. It fits Principle 10 only if partner identity enters as an input the core already has, not as a hand-built module.

**Fast vs slow routing can come out of gradient statistics.** McClelland's EI (coherence of per-sample updates) is a computable consistency signal. When updates from a new experience are coherent (high EI), let the slow store learn it directly and quickly. When they cancel (low EI, schema-inconsistent), route it to the fast episodic store and consolidate it only through interleaved replay with old material. This is our proposal. It would make "how fast vs slow stores interact" a derived consequence and not a design choice. It also answers how replay should be weighted: inconsistent items need many interleaved replays, consistent ones need few.

**Replay budget per night.** Kumaran's reading, that minutes of hippocampal availability give enough replays, implies schema-consistent material needs a short post-session replay burst. Most of the nightly budget should go to schema-inconsistent tagged episodes, which are the costly ones, interleaved with old episodes.

**Scarce data.** This is the main reason few hours a day could suffice later in life. Early learning of the partner schema is slow and data-hungry and cannot be shortcut (the novel-arena rats were slow). Once the schema exists, each day's handful of new interactions is cheap to integrate. A corollary for evaluation: early-weeks learning rates are not a valid predictor of month-3 learning rates.

**Interaction with state tagging.** Tse's schema is affect-neutral, so what follows is our inference. With state-tagged replay (see the sleep note), high-arousal partner events are replayed most. If such an event is schema-inconsistent (the operator behaves unusually), it is exactly the case that needs interleaving. Tag-weighted replay *without* interleaving would then be the penguin case: fast learning of the surprising event, and interference with the rest of the partner schema. That is a mechanism for a single bad day distorting the relationship model. It is also a direct ablation prediction for the "replay with tags but without interleaved old episodes" condition.

**Ablations.**
1. Remove the pretrained partner schema, i.e. a new operator. Prediction: new operator-specific contingencies need many exposures (the novel arena).
2. Disable the fast store or offline replay within about 48 h of a new consistent contingency. Prediction (Tse) for consistent items: the memory survives if replay ran before the cut, and is lost if it did not.
3. Focused vs interleaved replay of inconsistent tagged events. Prediction: focused replay degrades older partner knowledge.
4. Shared embedding vs per-partner item codes. Prediction: with shared codes, learning a second partner interferes with the first.

## Verdict: adopt (prior-knowledge-dependent slow-store learning; per-partner item codes; consistency-gated routing), watch (the rat result's generality)
- Adopt McClelland's reformulation as a design principle. Its mechanism is stated precisely, it reproduces with a tiny CPU network, and the EI computation is trivial. It suits an engine whose slow store must stay plastic for months without forgetting.
- Watch the empirical basis. I have not read the primary paper or its SOM. Its interpretation is contested (cellular vs systems consolidation). The paradigm is spatial-associative in rats, and the step to a social or affective "partner schema" is ours. Before any core cites the 48 h figure as a constraint, Tse 2007 and the 2008 exchange should be read in full.
