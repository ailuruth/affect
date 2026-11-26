# Divergence in dialogue (Healey, Purver & Howes)

Patrick G. T. Healey, Matthew Purver & Christine Howes, *PLoS ONE* 9(6):e98598, 2014, doi:10.1371/journal.pone.0098598 (PMC4053332).

## What was read
The full PMC open-access text: abstract, introduction, review of corpus and experimental evidence, hypotheses, methods (corpora, similarity measures, chance construction), results, discussion and conclusions. Some test statistics lost their symbols in extraction (F and β values appear without the letter); the numbers below are reported as printed. The supplementary file (worked similarity calculations, parse-tree examples) was not seen.

## Findings, precisely

**Data.** Two corpora of unscripted everyday spoken conversation in the UK: DCPSE (hand-annotated parse trees; 6,616 turns, 92 people) and the BNC spoken component (machine CCG parses; 95,169 turns, 2,020 people).

**Measures.** For each turn, similarity to each of the **five preceding turns** by the partner (other-similarity) or by the same speaker (self-similarity), giving a 10-turn moving window. Syntactic similarity = shared complete subtrees normalised by total structures in both turns; lexical similarity = matching word pairs normalised by total words. Both 0–1.

**Chance.** "Chance Other": the person's real turns interleaved with turns sampled at random from the rest of the corpus. "Chance Self": the person's own turns re-ordered (no turn matched with itself). Random pairings still show sizeable lexical and syntactic matches (worked example in Table 2), which is why the baseline matters.

**Model.** GLMMs on average cross-turn syntactic similarity, factors Conversation (real vs chance) × Distance (1–5 turns back), subjects as random intercept, **lexical similarity as covariate** (so syntax is tested net of word reuse).

**Results.**
- Lexical similarity strongly predicts syntactic similarity (DCPSE coefficient +0.927; BNC +0.446) — word reuse drags structure with it, even in random pairs.
- **Other-repetition of syntax, net of words, is below chance at the next turn**, then rises to chance:
  - DCPSE: main effect of Conversation (real < chance). Pairwise real − chance: T-1 **−0.024** (p < .001), T-2 −0.010 (p = .034), T-3 +0.002, T-4 +0.003 (n.s.), T-5 +0.009.
  - BNC: Conversation × Distance interaction. T-1 **−0.011** (p < .001); T-2 to T-5 not different from chance.
- **Self-repetition of syntax is not above chance** at any distance in either corpus once word reuse is controlled.
- Absolute lexical repetition is low: ~9% in real conversation vs ~6% by chance in the BNC; "over 90%" of words are not repeated.
- All three priming predictions fail: no repetition above chance (repetition), word and structure reuse pull in **opposite** directions at adjacent turns (percolation), and other-repetition *rises* with distance toward chance rather than decaying from a peak (decay).

**Interpretation (authors).** People reuse some of the partner's words but put them into different structures to produce "contrasts, elaborations and corrections" — e.g. A: "And it's Eileen's anniversary as well today." B: "Oh bugger Eileen!". Structural priming effects shown in the lab are "overwhelmed by the need to actively engage with our conversational partners and respond productively". They note the test is of the general claim (all structures), not of specific rare constructions.

## What it means for the designs
1. **Divergence is local and decays to chance, not to an anti-copy.** The signature is: below chance at a lag of one exchange, at chance by two to three exchanges. A design must not produce a stable anti-correlation (that is copying with a minus sign and is just as predictable); it must produce a **short-lag deficit that relaxes to independence**. Concretely: the agent's response at exchange *t* must be *less* similar in form to the partner's exchange *t−1* than a surrogate partner's would be, and no different from a surrogate at *t−3*.
2. **Content is shared while form diverges.** Lexical reuse is above chance while structural reuse, net of it, is below chance. The analogue for a face or voice: the agent can take up *what* the partner's signal is about (its referent or target) while producing it in a **different form** (different channel, configuration or timing). A design whose matching operates on the whole expression vector cannot separate these; it needs at least two components with opposite-sign coupling — one for the shared referent, one for form.
3. **No self-priming either.** The agent should not re-use its own previous form above chance; this rules out designs whose non-copying comes from a strong self-persistence that just happens to dominate the partner term.
4. **Time scale:** one turn (seconds). Says nothing about minutes or sessions.
5. **Caution on transfer:** this is syntax in talk, not a nonverbal channel. It is the strongest corpus-scale demonstration that people diverge from partners *more than chance*, and it fixes the shape (short-lag dip, relax to chance) a design should be tested for on every channel.

## Verdict
**adopt** — large-corpus evidence (two corpora, ~100k turns) that other-repetition of structure is below chance at the next turn and relaxes to chance within two to three turns, net of word reuse; supplies the test shape for "divergence above chance at short lags".
