# Bahdanau, Cho & Bengio 2014: Neural Machine Translation by Jointly Learning to Align and Translate

Citation: D. Bahdanau, K. Cho, Y. Bengio. "Neural Machine Translation by Jointly Learning to Align and Translate." ICLR 2015. arXiv:1409.0473 (v7, 19 May 2016).

Source read: arXiv v7 via text extraction. Read in full: abstract, sections 1-7 (introduction, background, the model, experiment settings, quantitative and qualitative results, related work, conclusion) and Appendix A.1.2 (the alignment model's exact form). Skimmed: Appendix A.1.1 (gated unit), A.2, B (training details). Not read: Appendix C (sample translations).

## The failure or bottleneck it answered
- The bottleneck was named before the mechanism: "we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder–decoder architecture".
- It rested on a measured failure in earlier work: "Cho et al. (2014b) showed that indeed the performance of a basic encoder–decoder deteriorates rapidly as the length of an input sentence increases."
- The paper's own measurement (Table 1, BLEU on WMT'14 En-Fr test, all sentences / sentences with no unknown words):
  - RNNencdec-30: 13.93 / 24.19; RNNsearch-30: 21.50 / 31.44.
  - RNNencdec-50: 17.82 / 26.71; RNNsearch-50: 26.75 / 34.16.
  - Moses (phrase-based): 33.30 / 35.63.
- Fig. 2 plots BLEU against sentence length: "the performance of RNNencdec dramatically drops as the length of the sentences increases", while "RNNsearch-50, especially, shows no performance deterioration even with sentences of length 50 or more." Qualitatively, the encoder-decoder "began deviating from the actual meaning of the source sentence after generating approximately 30 words".

## The new computation, in one equation

  c_i = Σ_j α_ij h_j,  α_ij = exp(e_ij) / Σ_k exp(e_ik),  e_ij = v_aᵀ tanh(W_a s_{i−1} + U_a h_j)

Before, the decoder was conditioned on one vector c = q({h_1, …, h_T}), computed once and independent of what the decoder was doing. Now every output step computes its own context c_i, and which input positions it draws on is a function of the reader's current state s_{i−1}. The authors read c_i as "the expected annotation over all the annotations with probabilities α_ij": an expectation over a soft, differentiable alignment that is "not considered to be a latent variable". The cost of the read scales with input length, which the paper names as the price: "requires computing the annotation weight of every word in the source sentence for each word in the translation."

## New computation or recombination?
Parts:
1. A bidirectional RNN encoder (Schuster & Paliwal 1997), with Cho et al.'s gated units.
2. A one-hidden-layer MLP scoring function.
3. A softmax normalisation over positions.
4. A convex weighted sum of stored vectors.
5. Joint training by backpropagation.

None of the parts is new. A softmax-normalised similarity-weighted average of stored values is Nadaraya-Watson kernel regression with a learned kernel. Softmax gating conditioned on the current input is the mixture-of-experts gate (Jacobs et al. 1991). The paper itself cites Graves 2013, where a Gaussian window over the input, "location, width and mixture coefficient … predicted from an alignment model", already did soft alignment, restricted to move monotonically. The Neural Turing Machine's content addressing appeared the same month.

So by the project's strict parts test (research/foundations/sketches/v2-README.md, Q9), attention is a recombination. This is the main finding of this note. What made it count as new was not a new part but **a change in the signature of the computation**: from c = q(input) to c_i = f(reader state, set of stored items). The conditioning stopped being a fixed summary and became a query-dependent read, with variable arity. A test that only lists parts would have rejected the mechanism that started the field. A better test asks whether the *dependency structure* (what is a function of what) changed in a way that removes a measured failure.

## What it suggests for an affective core
- **The analogy is exact enough to use.** "One scalar gain on the partner" is the affective version of the fixed-length vector: one global quantity, computed regardless of the receiver's state, that every later step must use. Bahdanau's answer was to make the conditioning a function of the *receiver's* current state, recomputed at every step, over a set whose size is not fixed.
- **Translated:** the partner should enter as a read, chosen by the agent's own current state (need, its own last expression, what it is about to do), over a stored set of the partner's moments and the agent's own moments. It should not enter as a gain on the partner's current expression.
- **The convex weights decide *which*, not *how much*.** Σ_j α_ij = 1, so the read always returns exactly one unit of context. In this mechanism the "how much partner" question disappears from the read and moves to how c_i is used downstream (g and f in Eq. 4).
- **Where it collapses back into a dial.**
  - The scale of v_a acts as a softmax temperature: large scales give hard alignment, small scales give a uniform average.
  - If the partner's recent frames sit in the same set as the agent's own frames, a sharp read can bind every step to the partner. The v2 attention-architect critique found exactly this: every slot binding to the partner gives a delayed copy.
  - So the lesson is the *signature change*: a receiver-state-dependent read over a growing set. Softmax over a shared pool of self and partner items is not the lesson.
- **Measurement first, as the paper did.** The bottleneck was a measured curve: BLEU against sentence length. The affective equivalent is a curve against something that should not matter to a well-built agent, for example how far into an episode the agent is, or how many partners it has known. Such a curve should exist for the one-gain sketches before a new mechanism is designed.

## Verdict
- [Neural machine translation by jointly learning to align and translate (Bahdanau, Cho & Bengio)](bahdanau-2014-attention.md) — 2014 — adopt (as the historical pattern) — a measured length curve, then a change of signature from c = q(input) to c_i = f(reader state, stored set); recombination by the parts test, which the test should note.
