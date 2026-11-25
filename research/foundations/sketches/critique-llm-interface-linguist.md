# Critique: v2-llm-interface-linguist (the paralinguistic remainder and the sayability monitor)

Critic: an independent subagent that did not write the sketch. Written 2026-11-25 for the Q8 critique round and the Q9 novelty test. No data or weights were downloaded. Quotes are from primary sources I fetched and read; the extent of each reading is stated in §2.

**Verdict: recombination.** The sketch's one-line "new mechanism" splits into three existing computations:
- **The remainder is a forward-model comparator residual.** Pickering & Garrod 2013 (the comparator of an efference-copy forward model, also run on the other through covert imitation). Skerry-Ryan et al. 2018 ("Prosody is the variation in speech signals that remains after accounting for variation due to phonetics…").
- **The referent-indexed stance field is a keyed slot memory with gated writes.** Recurrent Entity Networks, Henaff et al. 2017.
- **The sayability monitor is residual-energy importance resampling of a frozen language model's samples.** Deng et al. 2020.

The new elements are a new *choice of what to subtract*: an innate articulator, applied to both face and voice, for self and other. Q9 rules that a new input space, key space or naming is not a new computation.

---

## 1. Parts list (novelty test)

| # | Part, as written in the sketch | Existing mechanism | Source (read) |
|---|---|---|---|
| 1 | $\varepsilon^x_t=m^x_t-A_\varphi(w^x)$: the face and voice left over after one's own articulator explains the words | **Forward-model comparator / reafference subtraction**: the predicted consequence of the motor command is compared with the actual percept, and the discrepancy is the signal | Pickering & Garrod 2013 §2.1: "the predicted percept is compared to the actual percept … Any discrepancy between these two sensations (as determined by the comparator) is fed back". |
| 1′ | The same subtraction on the voice | **Prosody defined as a residual** after phonetic content | Skerry-Ryan et al. 2018: "Prosody is the variation in speech signals that remains after accounting for variation due to phonetics, speaker identity, and channel effects". The encoder "must model via its bottleneck representation … the unexplained variation in the signal". |
| 1″ | Separating articulation from the rest of the face | Conditioning face generation on a separate articulatory (lip) model | Ng et al. 2024 (Audio2Photoreal): "we generate facial motion F using a diffusion network conditioned on both audio and the output of a lip regression network". |
| 2 | $\varepsilon^o$: the other's face explained by *my* articulator saying *their* words | **The simulation route of covert imitation** | P&G §2.2: "use the mechanisms that she would use to move her own hand to predict her partner's hand movement". §3.2 does the same for language: the comprehender "covertly imitates B's unfolding utterance … and uses forward modeling". |
| 3 | $A_\varphi$: an innate, fixed articulator (visemes, jaw, F0 declination, blink, breath) | A hand-engineered articulatory synthesizer used as the forward model. Not a computation in itself. | — |
| 4 | $\alpha_{t,j}=\mathrm{softmax}_j(k_j^\top W_q[g;e(w)])$ | Attention | Q9 text |
| 5 | $v_j\leftarrow\lambda_jv_j+\alpha_{t,j}U[\varepsilon^s;\varepsilon^o]$, one slot per discourse referent | **A keyed slot memory with gated additive writes** (EntNet). Equivalently, a fast-weight additive outer-product write with decay. | Henaff et al. 2017: each memory has a "key $w_j$ and a vector value … $h_j$". The gate has "a 'location' term $s_t^Tw_j$ which causes the gate to open for memory slots whose key matches the input". Keys can be tied "with the embeddings of specific words". Schlag et al. 2021: fast-weight writes are "additive outer products of … keys and values". Yang et al. 2023: decay "is … crucial in RNNs". |
| 6 | $g_{t+1}=\Lambda g_t+B[\cdot]$ with diagonal decays from 33 ms to weeks | A diagonal linear state-space model or recurrence | Orvieto et al. 2023 (LRU): "Dense linear RNN layers can be reparameterized to a complex diagonal form without affecting the expressivity". |
| 7 | One forward model $F_\theta$ for both speakers, trained by maximum likelihood on the next remainder and the next discourse move | **A parity forward model** (P&G), trained by standard sequence maximum likelihood | P&G §3.3: "both A and B predict both A and B". |
| 8 | $q_\theta(g^o\mid\cdot)$: amortized inversion | Amortized inference, which the brief already lists as an existing ML substrate | brief.md |
| 9 | Output face: $m^s=A_\varphi(w^s)+\varepsilon^s$, with $\varepsilon^s\sim p_\theta(\cdot\mid g,H)$ | A decoder conditioned on a residual latent, as in the prosody-transfer decoder | Skerry-Ryan et al. 2018 |
| 10 | Speak draft $i$ with probability $\propto\exp(\beta\log p_\theta(\delta(c_i)\mid g,H))$ | **Residual-EBM self-normalized importance resampling** with $E=-\beta\log p_\theta(\delta\mid g,H)$. This is a Bayes-rule reweighting of a frozen generator by an attribute model, with a strength exponent. | Deng et al. 2020 §3.3: "a) sampling from the auto-regressive language model, followed by b) resampling according to the energy function". Yang & Klein 2021 (FUDGE): "$P(x_i\mid x_{1:i-1},a)\propto P(a\mid x_{1:i})P(x_i\mid x_{1:i-1})$", and "it is possible (and trivial) to adjust the conditioning strength … by multiplying the binary predictors' output logits by a constant". |
| 11 | If no draft clears $\theta_r$: hesitate, resample the contexts, and the latency grows | Rejection sampling with retry. In psycholinguistic terms, P&G's monitor → repair loop. | P&G §3.1: "The production implementer makes occasional errors, and the monitor detects such errors by noting mismatches between outputs of the production implementer and outputs of the forward model. It may then trigger a correction". |
| 12 | $\kappa(g)$: thinking budget and reply length | The brief's provisional coupling, as the sketch itself says | brief.md |
| 13 | Memories for each draft context retrieved by attention with query $g$ | Attention or Hopfield retrieval | Q9 text |
| 14 | Arousal $\lVert\dot\varepsilon\rVert$ weighted by precision; valence $=-\tfrac{d}{dt}$ of the sayability deficit | Readouts. Q9 lists "value or price readouts" as existing, and a rate-of-change of a loss is the same kind of thing. | Q9 text |
| 15 | Regulation by re-keying $k_j$ | Editing keys in a key–value memory | Henaff et al. 2017 (keys as learned or tied embeddings) |
| 16 | Replay weighted by the deficit | Prioritized replay by a surprise-type error. **Primary source not re-read by me**; I rely on the project's own note, research/schaul-2016-prioritized-experience-replay.md. | — |
| 17 | Emotion words become referents whose $v_j$ accumulates remainders (grounding) | The same slot write as row 5, keyed by a word embedding | Henaff et al. 2017 (keys tied to word embeddings) |

**Is any part new?** No single computation is.
- The strongest candidate, *affect = the comparator residual of an innate articulator, run on self and on other*, is the P&G comparator (row 1) with Skerry-Ryan's residual definition of prosody (row 1′), extended to the face. P&G apply the simulation route to "semantics, syntax, and phonology", not to paralinguistic signals. That is a new *domain*, not a new operation.
- The "sayability" monitor is the Deng et al. sampler with a state-conditioned energy. FUDGE shows that the coupling exponent $\beta$ is the standard strength knob.

## 2. Closest prior work, read in primary sources

What I read:
- Pickering & Garrod 2013, BBS target article §§1–4 (pp. 329–347 of the 64-page PDF; the commentaries were not read). The sketch's author read only "the abstract and §1".
- Skerry-Ryan et al. 2018, §§1–3.
- Deng et al. 2020, §§1–3.
- Henaff et al. 2017, the model section and related work.
- Yang & Klein 2021, §§1–3.
- Ng et al. 2024 (Audio2Photoreal), §3.
- Kendrick & Torreira 2015, the submitted version on White Rose: abstract and results.
- Learning to Listen, §§3–5 and the appendix on per-person models.
- Avatar Forcing, introduction, §3 and App. E.

1. **Pickering & Garrod 2013 (psycholinguistics). The closest prior work.**
   - **What P&G already have:**
     - a forward model with a comparator;
     - covert imitation of the other "using the inverse model and context";
     - one predictive machinery used for self and other ("both A and B predict both A and B");
     - monitoring and repair of one's own output;
     - an explicit link from prediction to turn timing ("why intervals between turns are so close to 0 ms … and why interlocutors are so good at using the content of utterances to predict when they are likely to end");
     - the observation that "people can straightforwardly predict that a person who looks confused is likely to respond slowly" (association route).
   - **What the sketch adds:** (i) it applies the comparator to *paralinguistic* face and voice and treats the residual as the affective substrate; (ii) production is *selection among a frozen generator's outputs* rather than generation.
   - **What does not differ:** the parity principle, the comparator, and the mapping from monitor mismatch to repair or delay.
2. **Skerry-Ryan et al. 2018 (ML, speech).**
   - **What it already has:** the definition of a paralinguistic residual *as what remains after the linguistic content is accounted for*, learned as a bottleneck, together with a decoder that regenerates speech from text plus that residual.
   - **What the sketch adds:** the residual is computed by explicit subtraction through a fixed, innate articulator rather than a learned bottleneck. The sketch also extends it to the face and to the other person.
   - **Where it does not differ:** the residual Skerry-Ryan learn also absorbs "speaker identity, and channel effects". The sketch's $\varepsilon$ will absorb $A_\varphi$'s modelling error in the same way, a risk the sketch itself names in §6.
3. **Deng et al. 2020 and FUDGE (ML).**
   - **What they already have:** the exact sampler (draw from the frozen language model, then resample by $\exp(-E)$), and the attribute-model reweighting with a strength knob.
   - **What the sketch claims to add:**
     - **"No named attribute."** The attribute is $\delta$, a vector of dialogue act, referents and hedges, which is exactly a set of named linguistic attributes. Its target is set by a state rather than by the user. That is a new conditioning variable, not a new operation.
     - **"Satiable, no draft can be 'more than sayable'."** This is false for the formula as written. $\exp(\beta\log p)=p^\beta$ strictly prefers the more likely draft, and as $\beta\to\infty$ it becomes argmax. Only the repair threshold $\theta_r$ is a bounded, satisficing element.
   - **What does not differ:** the sampler itself.
4. **Recurrent Entity Networks, Henaff et al. 2017 (ML).**
   - **What it already has:** one memory slot per entity, keys tied to word embeddings, writes gated by key match, and a state "to maintain an estimate of the current state of the world".
   - **What the sketch adds:** the written value is the paralinguistic remainder rather than the story content, with a softmax rather than independent gates, and a per-slot decay.

**A note for the Q8 grounding record.** The sketch's prediction P1 has a close precedent in conversation analysis that the sketch does not cite. Kendrick & Torreira 2015 found that "after approximately 700 ms, the proportion of dispreferreds was greater than that of preferreds". They also found that "Small departures from a normal gap duration (>300 ms) decrease the likelihood of an unqualified acceptance and increase the likelihood that a response … will have a dispreferred turn format". Dispreferred turns also carry "pre-beginning components … in-breaths, clicks", which are visible and audible pre-turn behavior.

## 3. Reduction attempt

**Rewrite.** P&G's parity forward model with a comparator, with these additions:
- (a) a comparator residual computed against an innate articulator and taken as the affective state (Skerry-Ryan's prosody-as-residual, extended to the face);
- (b) an EntNet keyed slot memory over discourse referents, written with the residual;
- (c) a diagonal linear SSM global state (LRU);
- (d) Deng et al. residual-EBM resampling of Claude drafts, with energy $-\beta\log p(\delta\mid g,H)$ and a rejection threshold whose failures are rendered as hesitation;
- (e) arousal and valence readouts;
- (f) deficit-prioritized replay.

Nothing is left over.

**Verdict: recombination.** The idea most worth keeping, *what the words did not require is the affect channel*, is a new **input definition**, and it is testable. It is not a new computation. The v2-README already adopts the sayability selection as "the shared Claude interface, which every candidate uses and none claims as its novelty". This critique confirms that this is the right status: the energy-diffusion sketch's draft selection is the same Deng et al. sampler.

## 4. Break attempts on the shared risks

### (a) Collapse into a delayed copy of the partner
**Scenario.**
1. While the agent listens it has no words, so $A_\varphi(w^s)=0$ and its whole face is $\varepsilon^s\sim p_\theta(\cdot\mid g,H)$.
2. $g$ is a *linear* diagonal SSM driven by $B[\varepsilon^s;\varepsilon^o;\ldots]$. During listening the only fresh input is the partner's remainder $\varepsilon^o$.
3. $F_\theta$ is pretrained on human dyads and learned "mostly from *the other person's* speech and body". It will learn the dominant listener regularity in that data: following the speaker's non-articulatory expression at about 0.5 s. Learning to Listen measured the ground-truth listener's peak lag at "≈17 frames … ≈0.5 s". A model it compared against "defaulted to mirroring the speaker".
4. Result: the listening face is a linear-filtered, delayed copy of $\varepsilon^o$.
5. The stance traces $v_j$ are running averages of $U[\varepsilon^s;\varepsilon^o]$ per referent, so on slow time scales they too are a referent-indexed delayed average of the partner's expression.

**Does the sketch answer it?** Only for the mouth: "remainder-level mimicry does not copy the other's mouth articulation". Subtracting $A_\varphi(w^o)$ removes lip-sync from what gets copied, but delayed copying of smiles and brows (the channels that matter for mimicry) is untouched. No term penalizes $\varepsilon^s_t\approx\varepsilon^o_{t-\delta}$.

### (b) A single hidden dial from flat affect to rigid imitation
**Argument.** Two knobs combine into one effective gain:
- the input gain of $\varepsilon^o$ into $g$ (the $\varepsilon^o$ block of $B$);
- the sampling temperature of $p_\theta(\varepsilon\mid g)$.

Because $g$ is linear and, with little data, $F$'s mean will be close to linear in $g$, the listening face's mean is a linear filter of the partner's remainder with one overall gain $k=\lVert B_o\rVert\cdot\lVert\partial F/\partial g\rVert$:
- $k=0$: $\varepsilon^s\approx$ its mean, and the face is only articulation ($A_\varphi$), a talking head with no affect.
- $k\approx1$ at short lag: imitation.

On the language side, $\beta$ is the same kind of knob, and FUDGE says so: conditioning strength is adjusted "by multiplying … logits by a constant".
- $\beta\to0$: the state never changes what Claude says.
- $\beta\to\infty$: argmax, the most stereotyped draft for the state. This is the sketch's own secondary concern about blandness, in another form.

**Does the sketch answer it?** Partly.
- It points to content-dependent structure: the effective dimension $d_g+|R_t|d_v$, and different drafts for "your sister called" against "your boss called".
- But in listening stretches with one referent in play, $H$ attends to one slot and the system reduces to the linear SSM. Nothing guarantees structure beyond the gain in the regime where mimicry is measured.
- The sketch's failure mode (§6, draft collapse) admits that on the language side "$\beta$ would act on noise".

### (c) A lookup table of past faces under scarce data
**Argument.** $H$ is, by construction, a key–value table:
- keys are referent embeddings;
- values are running averages of the faces and voices that occurred while each referent was salient;
- updates are "Hebbian-like accumulation with no gradient".

When "your sister" is mentioned, the agent emits roughly the stored mean remainder for that key. That is a lookup of past faces indexed by topic. Generalizing to a new referent works only through the similarity of keys in $e(\cdot)$.

The sketch's own low-dimensional ablation argument, the same words with "a different remainder depending on which person is being talked about", describes exactly what such a table does. A per-referent mean-face table with no $g$, $F$ or monitor would produce it too. So the ablation does not show that the structure does more than a table.

**Does the sketch answer it?** No. It treats per-referent recall as the evidence of richness. It needs a stronger ablation: per-referent mean-remainder lookup plus a lag filter as the low-dimensional baseline.

### Further problems found while reading
- **P1 is confounded with preference organization.**
  - $\delta$ deliberately includes "hedges and intensifiers … dialogue act".
  - Kendrick & Torreira show that gaps above about 300–700 ms predict dispreferred actions and qualified turn formats ("well", hedges), and that such turns begin with visible and audible "pre-beginning components".
  - So a poor fit of $p_F(\delta(\text{first clause})\mid\varepsilon_{-2s:0})$ can track dispreference through hedges in $\delta$. Longer gaps would then follow from the known preference effect, not from a paralinguistic sayability deficit.
  - The listed controls (length, lexical surprisal, question or not, partner remainder magnitude) do not include preference or turn format.
  - **Needed:** add dispreferred action and qualified format as covariates, or drop hedge and dialogue-act features from $\delta$ for P1.
- **The ablation "raw $m$ gives a smaller slope" can fail benignly.** If $A_\varphi$ is a weak model of articulation, which the sketch flags in §6, subtraction adds noise. That lowers or raises the slope for reasons unrelated to affect. Report the $R^2$ of $A_\varphi$ on lower-face AUs alongside the test, as the sketch itself suggests.
- **Self-confirming loop.** The selected drafts become Claude's history ("a path-dependent steering signal") and the agent's own $w^s$. Its own $\varepsilon^s$ feeds $g$, which selects the next draft, and nightly replay trains $F$ on episodes in which $F$ chose the words. The parity model is therefore partly trained on its own selections. No mechanism stops lock-in into one stance.
- **"Satiable" is overstated** (see §2, item 3).

## 5. Which measured failure of published listener models this might fix (hypothesis only)

None of these baselines has yet been run on Seamless Interaction in this project (Q9, Q11). The failures below are those the published papers report themselves.

- **Context blindness.**
  - **Published fact:** Learning to Listen conditions the listener on the speaker's audio and 3D face motion, not on the words. In its words, it uses "a motion-audio cross attention transformer".
  - **Hypothesis:** a listener whose reaction is computed relative to the words and the referent would separate reactions that look the same on the surface but differ in meaning (the brief's Aviezer context rule). This would be measured as better cross-lagged coupling conditioned on topic, on Seamless's WhisperX transcripts.
- **No topic- or partner-specific carry-over.**
  - **Published fact:** Learning to Listen is trained per listener with a short window (T=64 frames; trained past t=32 frames at 30 fps).
  - **Hypothesis:** referent-indexed stance would carry reactions across sessions with a returning partner who brings the same topic back. **Caution:** this is the lookup-table behavior of break (c), so it needs the per-referent-mean baseline.
- **Stiff listening** (Avatar Forcing: "less diverse, stiff motions"). Not plausibly fixed. The sketch adds no mechanism for variability beyond sampling $p_\theta(\varepsilon\mid g)$.

## Sources read (primary)
- Pickering, M. J., Garrod, S. (2013). An integrated theory of language production and comprehension. BBS 36:329–347 (target article).
- Skerry-Ryan, R. J. et al. (2018). Towards End-to-End Prosody Transfer for Expressive Speech Synthesis with Tacotron. arXiv 1803.09047.
- Hsu, W.-N. et al. (2019). Hierarchical Generative Modeling for Controllable Speech Synthesis. arXiv 1810.07217 (related work only, which describes prior latents as capturing "residual attributes that are not specified by other input streams").
- Deng, Y., Bakhtin, A., Ott, M., Szlam, A., Ranzato, M. (2020). Residual Energy-Based Models for Text Generation. arXiv 2004.11714.
- Yang, K., Klein, D. (2021). FUDGE. arXiv 2104.05218.
- Henaff, M., Weston, J., Szlam, A., Bordes, A., LeCun, Y. (2017). Tracking the World State with Recurrent Entity Networks. arXiv 1612.03969.
- Schlag, I., Irie, K., Schmidhuber, J. (2021). Linear Transformers Are Secretly Fast Weight Programmers. arXiv 2102.11174 (abstract and §2).
- Yang, S. et al. (2023). Gated Linear Attention Transformers. arXiv 2312.06635 (§§2–4).
- Orvieto, A. et al. (2023). Resurrecting Recurrent Neural Networks for Long Sequences (LRU). arXiv 2303.06349 (§3).
- Ng, E. et al. (2024). From Audio to Photoreal Embodiment. arXiv 2401.01885 (§3).
- Kendrick, K. H., Torreira, F. (2015). The Timing and Construction of Preference. Discourse Processes 52:255–289 (submitted version).
- Ng, E. et al. (2022). Learning to Listen. arXiv 2204.08451.
- Ki, T. et al. (2026). Avatar Forcing. arXiv 2601.00664.
