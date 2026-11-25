# Press, Smith & Lewis 2022: Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation

## Citation

O. Press, N. A. Smith, M. Lewis. "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation." International Conference on Learning Representations (ICLR) 2022. arXiv 2108.12409. Version read: v2 (22 Apr 2022), the latest. Code: github.com/ofirpress/attention_with_linear_biases.

## What was read

PDF from arXiv (v2), text extracted with pdftotext.

- Read in full: abstract; sections 1 (introduction), 2 (current approaches: sinusoidal, rotary, T5 bias), 3 (ALiBi, including footnotes 9-11), 4 (results), 5 (related work), 6 (conclusion); Appendix A.1-A.4 text; Appendix B (sliding-window evaluation, the early token curse, and Tables 13-15).
- Read as tables: Tables 1, 5, 6, 11, 12.
- Skimmed: Tables 2-4 and 7-10.
- Not read: references.

The paper contains no theorem and no proof. Everything below marked "proof" is my derivation.

## The object, exactly

Causal self-attention, one head, head dimension d. For query position i (1 <= i <= L), q_i in R^{1 x d}, keys K in R^{i x d} (the first i keys). ALiBi adds no position embedding anywhere and replaces the score row by

    softmax(q_i K^T + m * [-(i-1), ..., -2, -1, 0])

that is, the score of key j <= i is q_i . k_j + m (j - i) = q_i . k_j - m (i - j). Further details:
- The bias is not multiplied by the 1/sqrt(d_k) factor (footnote 10).
- m > 0 is a head-specific scalar, "fixed before training", not learned.
- Values carry no position.
- Implemented by adding the n x L x L bias to the causal mask.

Slopes. For n heads, m_h = 2^{-8h/n}, h = 1..n: a geometric sequence starting at 2^{-8/n} with that same ratio. For 8 heads: 1/2, 1/4, ..., 1/256. For 16 heads: 1/2^0.5, 1/2^1, ..., 1/2^8. Each head's recency time constant 1/m_h is therefore log-spaced:

| Heads | 1/m_h (tokens) | At 30 Hz |
|---|---|---|
| 8 | 2, 4, 8, ..., 256 | 0.067 s to 8.5 s |
| 16 | 1.41 to 256 | 0.047 s to 8.5 s |

Facts the paper reports about the slopes (empirical):
- Trainable slopes "did not yield strong extrapolation results" and cost 3% speed.
- The slopes were chosen by "a brief manual exploration of around ten slope sets". Good sets have slopes in (0, 1), denser near 0.
- The method is "robust to slope choice". Random draws from an exponential distribution sometimes worked, "with high variance".
- Multiplying scores by the distance function instead of adding degraded performance (results not presented).
- The same slopes transferred to the Toronto BookCorpus and to a 1.3B model on CC100+RoBERTa without retuning.

## The key property and its proof, step by step

### What the paper claims, and on what basis

1. **Extrapolation (empirical only).** Models trained on length L keep, or improve, perplexity on L_valid > L. Examples:
   - WikiText-103, L = 512: 19.73 at 512 and 18.40 at 3072 (Table 5).
   - The sinusoidal model degrades within a few dozen tokens of L.
   - Rotary improves for up to k = 200 (L = 512) and k = 100 (L = 1024) extra tokens and then degrades.
   - T5 bias improves to about 2L.
   On the 1.3B model ALiBi's best score is near 2L. The paper offers a guess: beyond 2L "less than half of the predictions ... are on subsequences of lengths seen during training".
2. **The paper's own explanation, Appendix B.** With nonoverlapping evaluation, longer L_valid means fewer predictions near the start of a chunk (the "early token curse"). With sliding-window evaluation at stride 1, every prediction gets maximal context, and ALiBi's perplexity stays roughly flat as L_valid grows:
   - L = 512: 17.98 at 512 and 18.3 at 3072 (Table 15).
   The authors conclude the gains come from explanation 2 (fewer early tokens), "not explanation 1" (using longer context), and that "ALiBi might not be using contexts longer than the ones it was trained on." So the paper's own reading of "extrapolation" is: the model does not break when given more tokens. It is not that it uses them.
3. **Inductive bias towards recency.** Stated, not formalised. Why values are kept free of position: "We hypothesize that these properties might be beneficial for extrapolation."

### What can be proved from the object (my derivations)

**Lemma 1 (time-shift invariance).** The bias m (j - i) depends only on i - j, so the bias matrix is Toeplitz.

Proof. With no position anywhere else (values and inputs carry none), shifting the whole input sequence by s, with the earlier context removed equally, shifts the attention pattern by s. QED.

This is the same relative-position property RoPE has, obtained additively instead of by rotation.

**Lemma 2 (bounded effective horizon).** Suppose |q_i . k_j| <= B for all i, j, which holds for a trained model with bounded activations. For a head with slope m, the attention mass on keys farther than D from the query is at most

    e^{2B} e^{-m(D+1)} / (1 - e^{-m}).

Proof.
1. The weight on key j is e^{s_j - m(i-j)} / Z, where s_j = q_i . k_j.
2. The denominator Z >= e^{s_i} >= e^{-B}, since the query's own key, at distance 0, is always included.
3. The numerator is sum_{r > D} e^{s_{i-r} - m r} <= e^{B} sum_{r >= D+1} e^{-m r} = e^{B} e^{-m(D+1)}/(1 - e^{-m}).
4. Divide. QED.

Corollary. Changing any keys or values at distance > D changes the head's output by at most 2 max_j ||v_j|| times that bound. Each head therefore has a horizon D_eps ~ (2B + ln(1/eps))/m that does not depend on L. In one layer, outputs at length L_valid > L are eps-close to outputs computed on the last D_eps tokens. That is a mathematical reason the model "does not break" past L. It matches Appendix B: the model does not use the extra context.

The bound is only as good as B. Large logits widen the horizon, and depth widens it further, roughly additively per layer. The paper measures none of this.

**Lemma 3 (content-blind limit = a bank of leaky integrators).** If q_i . k_j is constant in j (content-blind scores), head h computes

    o_i = sum_{r=0}^{i-1} e^{-m_h r} v_{i-r} / sum_{r=0}^{i-1} e^{-m_h r},

a normalised exponential moving average with decay e^{-m_h} per token and time constant about 1/m_h.

Proof. Substitute into the softmax. The constant cancels. QED.

So ALiBi's prior is exactly a log-spaced bank of n exponential filters, from 2 to 256 tokens for 8 heads. The content scores then reweight within each filter.

## What it would mean for a dyadic affective core

All of this section is my inference.

**(c) Time scales from structure.** ALiBi is the cleanest existing case of time scales fixed by structure rather than learned: one recency constant per head, log-spaced. At 30 Hz the default set covers about 47 ms to 8.5 s. That spans reflex (the sub-second matching responses reported for Carr 2014 in mimicry-context-synthesis.md) to a few seconds of an exchange. The span is set by the head count and the base 2^{-8/n}; it is not discovered. Its limits:
- It cannot reach temperament (days to months). That would need m of order 1/(30 * 86400) per frame, and a softmax over that many cached frames, which is impossible on this machine.
- So ALiBi can supply the fast end of (c). The slow end (partner history, temperament) must be a different state with its own dynamics, not a longer ALiBi window.
- The paper's finding that trainable slopes extrapolate worse is a warning: letting the time constants be fit freely tends to destroy the structure that made them useful.

**(a) Partner influence.** ALiBi adds nothing here. With self and partner frames in one sequence, the partner contribution of one layer is sum_h alpha_h M_h xbar^h, as derived in the RoPE note (su-2021-roformer-rope.md):
- M_h = W_O^h W_V^h is fixed;
- alpha_h in [0, 1] is head h's mass on partner frames;
- xbar^h is a recency-weighted partner average.

In the content-blind limit (Lemma 3) it is exactly a fixed linear time-invariant filter of the partner's face:

    y_self(t) <- sum_h alpha_h M_h EMA_{m_h}[x_other](t).

With one head and M = I, that is "copy the partner, smoothed, with a gain alpha": the excluded mechanism, plus a lag. Per-expression signs are possible only through fixed M_h, and nothing in ALiBi makes them depend on learned partner history.

**(b) Whose vs what.** ALiBi keeps position out of the values, which is the same separation RoPE makes. A natural extension is a separate slope set per source: m_h^self for one's own past frames and m_h^other for the partner's. This would make "how long the other's expression stays with me" a structural property distinct from "how long my own does". By Lemma 2, it would give a separate horizon per source and per head.

**(d)** Not addressed.

**The theorem a design would need, if it uses ALiBi-like heads.** A two-scale separation statement: the fast state (the ALiBi heads, horizon D_eps per Lemma 2) and the slow partner-history state h, updated over minutes to days, must be such that:
1. the fast heads' output is eps-independent of frames older than D_eps;
2. the slow state alone carries the partner's history;
3. the per-expression, signed partner-to-self map is a function of h, as M(h) in the value path, not of the slopes.

Then (a) cannot reduce to a gain on a smoothed copy unless M(h) is confined to a one-dimensional family.

## Verdict

**watch**, possibly adopt for the fast end of (c).

- ALiBi is a fixed, log-spaced bank of recency time constants with a provable bounded horizon (Lemma 2, mine). It is a good structural prior for reflex-to-seconds time scales on 30 Hz streams.
- The paper proves nothing, and its own analysis says it does not use context beyond the training length.
- It contributes nothing to per-expression, signed, history-dependent coupling. In its content-blind limit, partner influence is a smoothed copy times a gain.
