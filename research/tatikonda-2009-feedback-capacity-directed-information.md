# The capacity of channels with feedback (Tatikonda & Mitter)

Sekhar Tatikonda & Sanjoy Mitter, *IEEE Transactions on Information Theory* 55(1):323–349, 2009; preprint arXiv:cs/0609139v1 (25 Sep 2006), 50 pp. This note also carries **Massey 1990, "Causality, feedback and directed information" (Proc. ISITA, Waikiki, pp. 303–305)**. Massey's paper itself was not reachable: the ETH archive host did not resolve. His definition is cited here as Tatikonda & Mitter restate and generalise it.

## What was read
The arXiv preprint (extracted text):
- **Read in full:** §1–4 (introduction, feedback and causality, channels with feedback, the interconnection lemma 3.1, Definitions 4.1–4.2 of directed stochastic kernels and directed information, Lemmas 4.1–4.2, the capacity definitions (4)) and §5 up to the converse (Theorem 5.1 and Lemma 5.5).
- **Skimmed (headings and theorem statements only):** §6–9 (Markov channels, the POMDP/ACOE formulation, simple sufficient statistics, ML decoding) and the conclusion.

## The computation, precisely

**Causal ordering.** Message, A₁, B₁, A₂, B₂, …, A_T, B_T, decoded message. The channel is a sequence of kernels p(db_t | a^t, b^{t−1}). The encoder is a sequence of *code-functions* a_t = f_t(b^{t−1}).

**Why mutual information is wrong under feedback (§2).** "One should not use the mutual information I(A^T; B^T) when there is feedback … Even though A_{t+1} occurs after B_t it still has a probabilistic influence on it." Massey: "statistical dependence, unlike causality, has no inherent directivity."

**Directed information (Massey, restated after Definition 4.2).**

  I(A^T → B^T) = Σ_{t=1}^T I(A^t; B_t | B^{t−1}).

The superscript is t, not T: only the *past and present* of A count. Equivalently, I(A^T → B^T) = E log[ p⃗(B^T | A^T) / P(B^T) ].

**Conservation law.**

  I(A^T; B^T) = I(A^T → B^T) + I(B^T → A^T),  with I(B^T → A^T) = Σ_t I(A_t; B^{t−1} | A^{t−1}).

There is no feedback iff A_t − A^{t−1} − B^{t−1} is a Markov chain, iff I(B^T → A^T) = 0. Hence I(A^T; B^T) ≥ I(A^T → B^T), with equality iff there is no feedback. Mutual information **splits exactly** into the two directions of a loop.

**Capacity (Theorem 5.1).** C^o = C = sup over channel input distributions {p(da_t | a^{t−1}, b^{t−1})} of the (lim-inf-in-probability) directed information rate. The supremum runs over *causal* conditioning only. The operational capacity of a channel used with feedback equals this.
- The converse (Lemma 5.5) holds for every code and every encoder strategy that uses feedback: no strategy beats the directed-information supremum.
- The interconnection Lemma 3.1 converts the feedback problem into a no-feedback channel from code-functions to outputs, with kernel p(b_t | f^t(b^{t−1}), b^{t−1}).

## Evidence with numbers
None in the sense of data. These are theorems. (The paper cites Shannon's result that feedback does not increase the capacity of a memoryless channel; it can increase it for channels with memory, which is why the supremum is over feedback-dependent input laws.)

## What it means for the designs
1. **A currency that is conserved over all routes.** Directed information obeys data processing along any causal chain. If every partner→agent route passes through a perceptual stage Π (camera, face reading in own synergy coordinates, voice reading), then for any internal architecture, learned or not, looped or not:

   I(P^T → F^T) ≤ capacity of Π over T steps,

   where P is the partner's face and F the agent's face. Every route — the direct route, a comfort loop, a shared estimate, content events — draws on the same budget, because all of them sit downstream of Π. (My application of the converse: the agent is the "decoder plus re-encoder", and its output cannot carry more about P than came through Π. The feedback to the partner, the agent's face seen by the partner, is exactly the feedback this theorem allows for.) **This is a whole-system ceiling by construction, not by enumeration.**
2. **Per channel and innate.** Make the perceptual bottleneck channel-wise: smile, brow, lids, head, F0, each read through a separate noisy channel with innate noise σ_i² and power limit. Then the per-channel budget is C_i = ½log(1 + SNR_i) per sample (Gaussian case, see wan-2025-information-limits-feedback.md for the feedback-capacity statement). The noise is a property of the sensor, not a learned parameter, so learning cannot exceed it. Cross-channel routes (the partner's brow informing the agent's smile) draw on C_brow. A whole-face copy needs Σ_i of the partner's entropy rates.
3. **From bits to a copy defect (rate–distortion).** For a Gaussian partner channel with variance s_i², any agent output y_i satisfies E(y_i − p_i)² ≥ s_i²·2^{−2R_i}, where R_i is the information rate it carries about p_i (rate–distortion; standard, not from this paper). So an innate C_i gives a **copy-defect floor** 2^{−2C_i} (relative MSE) on channel i, whatever the architecture.
4. **Directed, not symmetric.** The split I = I(→) + I(←) lets a design measure and bound "the partner drives me" separately from "I drive the partner". It is the right statistic for the contingency work: transfer entropy is its stationary rate form (schreiber-2000-transfer-entropy.md).
5. **Where it falls short.**
   - **Information is sign-blind and gain-blind.** A perfect anti-copy (inverted smile) carries as many bits as a copy. A ceiling in bits does not stop a *slow, low-entropy* expression from being copied exactly: a held smile changing once every few seconds is a few bits per second. The copy-defect floor 2^{−2C_i} binds only where the partner's channel has high entropy rate relative to C_i. Human faces in conversation are slow, so the bound may be loose exactly where copying matters.
   - **Copy is about fidelity of the map, not about bits.** An agent that responds to the smile with its own, different appraisal and one that copies can carry the same directed information. Bits bound *how much* of the partner can be in the face, not *how* it is in the face.
   - **Estimation, not control.** Capacity is a supremum over encoders. Bounding it requires an innate noisy front end. In the designs, Claude content events are a second, non-perceptual route whose capacity is not innate (text is high-capacity), so it must be given its own explicit low-rate channel.
   - **Existing framework.** Information theory is a measure, not a core. It is usable as a **constraint on the partner port**: an innate, per-channel noisy bottleneck.

## Verdict
**adopt (as a second, sign-free ceiling over all routes: per-channel innate perceptual capacity bounds the directed information from partner to face; rate–distortion converts it into a copy-defect floor).** It does not replace a gain bound: it fails on slow, low-entropy expressions. Massey 1990 not reached; its definition is cited through this paper.
