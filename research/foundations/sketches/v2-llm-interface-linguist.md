# Sketch v2 (linguist / LLM-interface lens): the Paralinguistic Remainder and the Sayability Monitor

Lens: a linguist and LLM-interface researcher. The starting point is the interface. Claude only sees text and a few settings, and the engine only sees faces, voices and words. So the affective state should be defined at the place where words and bodies separate: **what a body does while speaking or listening that the words did not require.** Here that remainder *is* the substrate of affect. Claude is not told about it. It is coupled by a comprehension-based monitor that chooses among Claude's own drafts, decides when to speak, and decides what Claude remembers.

## 1. Core mechanism

Speakers $x \in \{s\ (\text{self}), o\ (\text{other})\}$. At 30 Hz:

$$
\boxed{\;\varepsilon^x_t = m^x_t - A_\varphi\!\left(w^x_{t-\tau:t+\tau}\right)\;}\qquad\text{(remainder: read through one's own articulator)}
$$

$$
\alpha_{t,j} = \operatorname{softmax}_j\!\big(k_j^{\top} W_q[g_t;\,e(w_t)]\big),\qquad
v_j \leftarrow \lambda_j v_j + \alpha_{t,j}\,U[\varepsilon^s_t;\varepsilon^o_t],\qquad
g_{t+1} = \Lambda g_t + B\big[\varepsilon^s_t;\ \varepsilon^o_t;\ \textstyle\sum_j \alpha_{t,j} v_j;\ b_t\big]
$$

**One objective, with parity.** A single forward model $F_\theta$ is used for both speakers. Given a speaker's state, it predicts that speaker's next remainder and next discourse move:

$$
\mathcal{L}(\theta) = -\sum_t \sum_{x\in\{s,o\}} \log p_\theta\!\big(\varepsilon^x_{t+1},\ \delta^x_{t+1} \,\big|\, \hat g^x_t,\ H_t\big),\qquad \hat g^s_t = g_t,\quad \hat g^o_t \sim q_\theta(g^o \mid \varepsilon^o_{\le t}, w^o_{\le t}).
$$

**Action is the self term of $\mathcal L$, satisfied only by selection.** The agent behaves the way its own model predicts a speaker in its state would behave:
- Face and voice: $m^s_t = A_\varphi(w^s) + \varepsilon^s_t$, with $\varepsilon^s_t \sim p_\theta(\cdot \mid g_t, H_t)$. The first term is the voluntary and articulatory pathway, the second the emotional one, and the two can disagree.
- Claude: draw $N$ drafts $c_i \sim \text{Claude}(C_i, \kappa(g_t))$. Each draft gets its own context $C_i$, built from memories sampled by attention with query $g_t$. Speak draft $i^*$ with probability $\propto \exp\!\big(\beta \log p_\theta(\delta(c_i)\mid g_t,H_t)\big)$, the draft's **sayability**. If $\max_i \log p_\theta(\delta(c_i)\mid\cdot) < \theta_r$, no draft is sayable. The body then produces a hesitation (a remainder sampled from $F$ during a pending turn: filled pause, gaze aversion), the contexts are resampled, and the latency grows.

Symbols:
- $m^x_t$: continuous face (AU or blendshape) and prosody (F0, energy, rate, voice quality) features.
- $w^x$: the timed word and phone stream. For self it comes from Claude's text through local TTS alignment; for the other, from local ASR.
- $A_\varphi$: the **innate articulator**, fixed and not learned from emotion data. It maps timed phones to the face and voice needed to say them: visemes, jaw, stress energy, F0 declination, plus blink and breath rhythms.
- $\varepsilon^x_t$: the paralinguistic remainder.
- $H_t=\{(k_j,v_j)\}_{j\in R_t}$: stance traces over the set $R_t$ of discourse referents in play (people, topics, episodes, the agent itself). $k_j$ is a referent key from a small local encoder $e(\cdot)$, and $v_j\in\mathbb R^{d_v}$ is the remainder that has accumulated while that referent was salient.
- $g_t\in\mathbb R^{d_g}$: the global state, a diagonal state-space model whose decays $\Lambda$ span 33 ms to weeks.
- $b_t$: body variables, entering as one input only.
- $\delta(c)$: non-affective linguistic features of an utterance: which referents it activates, dialogue act, length, hedges and intensifiers, person and tense, question or assertion.
- $\kappa(g)$: the thinking budget and maximum reply length.
- $\beta$: the coupling strength. $\theta_r$: the repair threshold.

## 2. Why it is new, and its closest prior work

- **Pickering and Garrod (2013, BBS 36:329; I read the abstract and §1).** Speakers build forward models of their own utterances. Comprehenders covertly imitate others and predict them with their own production system, and the same predictions monitor upcoming speech. *Difference:* their theory has no affect, no paralinguistic remainder and no frozen generator. Here the parity forward model is defined over the *remainder plus discourse moves*, and production is selection over another system's drafts rather than generation.
- **FUDGE (Yang and Klein, NAACL 2021; I read the abstract).** An attribute discriminator reweights a generator's logits toward a *named* attribute. *Difference:* there are no logits (subscription CLI), no named target attribute, and no reward model. The scorer is the agent's own likelihood of a discourse move given its state, learned mostly from *the other person's* speech and body (parity). A selection failure becomes bodily disfluency and turn latency, not a lower score.
- **Best-of-N reranking with a reward model.** This is the closest engineering relative, and it optimizes a preference. The monitor optimizes self-consistency, which is satiable: no draft can be "more than sayable", and the user's smiles are not in the objective.
- **Brief's provisional coupling** (mood-congruent retrieval and thinking budget). This sketch keeps both and adds three things the brief lacks: a single objective they derive from, draft selection, and timing that emerges from mismatch.
- **Not active inference with structure bolted on, though related.** There are no preferred observations, no expected free energy over policies and no precision bookkeeping. The ideomotor resemblance is real: action fulfills self-prediction. What is new is the object predicted, the definition of affect as the remainder after the agent's own articulator, the referent-indexed stance field, and control that acts only by choosing among a frozen language model's drafts.

**New mechanism, in one line:** affect lives in the remainder left after explaining a face and voice with one's own speaking body. It is indexed by discourse referents, and it steers a frozen language model by choosing what is sayable and when.

## 3. Constraints

| Constraint | Status |
|---|---|
| No labels | **Met.** The inputs are AUs, prosody and words. $\delta$ holds linguistic features only (dialogue act, referents), with no affect lexicon. |
| Emotion as emergent structure | **Met.** Emotion is the clusters and attractors in $(g, \{v_j\})$, the remainder geometry learned by $F$. Valence and arousal are readouts (§4). |
| Others read through own body | **Met, strongly.** The other's face is first explained by *my* articulator saying *their* words, and $F$ is inverted with the weights I use to predict myself. |
| Frozen LLM coupled without words | **Met.** Claude sees only (a) which memories are in its context, (b) its thinking budget and reply length, (c) its own state-selected past replies as history, and (d) the timing of the turn. The history itself becomes a path-dependent steering signal. |
| Satiable drives | **Partly met.** Self-consistency is bounded: a draft is either sayable or not. Body variables are satiable inputs. There is no reward channel to exploit. Open: $\mathcal L$ alone has no homeostatic urgency, so drives are weak. |
| Time scales, reflex to temperament | **Met.** Remainder reflexes run at 30 Hz. $\Lambda$ covers mood. Referent decays $\lambda_j$ give relationship-specific stance. Temperament is the slow modes of $\Lambda$ plus the weights of $F$. |
| Scarce real data | **Mostly met.** $A_\varphi$ is innate and absorbs most facial variance during speech, so only a small remainder must be learned. $H$ updates by Hebbian-like accumulation with no gradient. $F$ is small. Open: pretraining $F$ on unlabeled human dyads (Seamless) is not emotion data but is borrowed manner. |
| Real-time face | **Met.** The face loop is $A_\varphi$ plus a sample from $F$ and never waits for Claude. Hesitation is precisely what the body does while drafts are pending. |
| Breaks or leaves open | Needs a local referent/coreference parser and $\delta$ extractor (a small local LM, no emotion labels). The cost of $N$ parallel subscription calls. Claude's multi-second latency is far above human gaps (80–380 ms), so latency effects must ride on top of a floor. |

**Expressive structure.** The effective dimension is $d_g + |R_t|\,d_v$, and it grows with the discourse. *Low-dimensional ablation* (collapse $H$ to one vector): it cannot produce the same words with a different remainder depending on which person is being talked about, nor choose different drafts for "your sister called" and "your boss called" under an identical global mood. That attention over referents is content-dependent, with the state as the query.

## 4. Principle 10 components, and perception

- **Homeostasis:** $b_t$ drives $g$. The variable "predictability" *is* the running loss $\mathcal L$, so it is not a separate gauge.
- **Curiosity:** the weakest component. A referent with high stance variance $\operatorname{Var}[v_j]$ raises its attention weight, so drafts that mention it score as more sayable. This is a constraint on $W_q$, not derived.
- **Valence and arousal (readouts):** arousal is $\lVert\dot\varepsilon\rVert$ weighted by the precision of $F$. Valence is $-\tfrac{d}{dt}$ of the sayability deficit: things getting easier to say versus harder.
- **Mimicry:** $\varepsilon^o$ enters $g$, so $F(g)$ shifts the self remainder toward it. Parity makes mimicry emerge, and remainder-level mimicry does not copy the other's mouth articulation.
- **Reading others:** amortized inversion $q_\theta(g^o\mid\cdot)$ with the same $F$, plus each referent's stance as the *other* expresses it.
- **Regulation:** Claude re-describes a referent (reappraisal). New predicates change $k_j$, so its stance $v_j$ is retrieved under a different key and is attended less in that context. Claude regulates by re-keying the discourse model, never by reading the state.
- **Replay:** at night, stored remainder and transcript streams rerun through $F$ and $H$, weighted by how strongly each moved the state (the sayability deficit). Claude may name a replayed episode. Its emotion words become referents whose $v_j$ is learned from the remainders that occurred while they were used. That is the grounding of "I'm fine".
- **Perceiving the other's face and voice:** body-route features (MediaPipe for now, the engine's own inverse model at S4) give $m^o$. Local ASR gives $w^o$. $A_\varphi(w^o)$ removes what *I* would have had to do to say their words, and the remainder enters $g$ and $H$ together with the words that set the referent attention, which meets the brief's context rule (Aviezer). The voice works the same way: their F0 and energy minus my own declination and stress model for those words.

## 5. First distinctive prediction, on published data

**P1 (the sayability gap):** turn-initial gaps lengthen, and filled pauses become more likely, when the responder's paralinguistic remainder in the preceding 2 s predicts their eventual first clause *poorly*. This holds beyond planning-load predictors.

- **Data:** Meta Seamless Interaction (arXiv 2506.22554; I read §3), naturalistic split (2,745 h), using the published participant-disjoint train/dev/test splits. It provides 30 fps video, 48 kHz audio and WhisperX word-aligned transcripts. Faces are coded as AUs with OpenFace or Py-Feat (a measurement tool, allowed by the Evaluation rules). Replication: CANDOR (Reece et al., Science Advances 2023; I read the paper's results summary), which reports a median between-speaker interval of 80 ms, median gap 380 ms, and links longer gaps to lower partner enjoyment.
- **Analysis:** fit $F$ (remainder → $\delta$) per participant on their other sessions. Compute the deficit $D = -\log p_F(\delta(\text{first clause}) \mid \varepsilon^s_{-2\text{s}:0})$. Run a mixed model of log gap on $D$, controlling for utterance length, lexical surprisal of the first words (small LM), whether the previous turn was a question, and the partner's remainder magnitude.
- **Numbers:** standardized slope $\beta_D \ge 0.10$. The same $D$ computed from raw $m$ (no $A_\varphi$ subtraction) gives a smaller slope. $D$ from a speaker-shuffled $F$ gives $\beta\approx 0$. **Falsified** if $\beta_D$'s 95% CI lies below 0.05.
- **Caveat:** Whisper tends to drop "uh" and "um", so the filled-pause half needs a disfluency-preserving re-transcription and is reported separately.

The in-engine counterpart for S1 ablations: with $N=1$ (monitor removed), reply latency and hesitation stop covarying with $g$ under steering.

## 6. Most likely failure mode

**Draft collapse.** Claude's $N$ drafts, from nearly identical prompts, share a single trained persona. Their $\delta$ features may barely vary, so selection has nothing to choose from. The coupling to Claude would then reduce to retrieval and latency, and $\beta$ would act on noise. The mitigation is built in, since each draft gets a different state-sampled memory context. But if variance across drafts in $\delta$ is below the noise in $p_\theta$, the "state shapes what Claude says" claim fails, and the brief's provisional coupling is all that remains. A secondary risk: if $A_\varphi$ models coarticulation poorly, the "remainder" is mostly articulation error, and $F$ learns speech-motor junk rather than affect. Check this first, using the $R^2$ of $A_\varphi$ on the speaker's lower-face AUs in Seamless.
