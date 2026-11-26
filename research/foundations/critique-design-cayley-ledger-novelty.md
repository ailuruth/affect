# Critique of the Cayley–ledger core: principles, fitness as an emotional agent, reduction and novelty

Independent critic, 2026-11-26T05:34:25Z

Critic of research/foundations/design-cayley-ledger.md. I did not write the design. Standard: operator note Q19. I do not count proof gaps as failures. What counts is a concrete way the mechanism fails, against brief.md, Q16–Q19 and D78. A separate critic hunts copying routes. I report the one glaring route I found (§1.6) and leave the rest to that critic.

## Summary verdict

- **The core mechanisms hold.**
  - The wrap is a correct one-sided cone, for every parameter.
  - The release is a correct Gaussian-RDP mechanism with a duration-independent cost.
- **But the agent built around them is not an emotional agent in the brief's sense.** The ledger is sign-blind (the author's own §4 point), so it blinds the slow mind to the partner's face in the caring direction as much as in the copying direction:
  - One full-range expression of any duration gives the slow mind d′ ≈ 0.34. That is at most 57% correct detection, for its whole life.
  - The fibre that does see the face writes nothing and cannot learn. Its training data is the same noised release, so its regression coefficients are diluted by a factor of about 10⁻³.
  - Nothing social moves any body variable, so valence does not track what happens between the two people.
  - The display policy has no objective that ties it to the agent's state.
  - There are no emotion concepts and no naming.
- **Two claims are false by the design's own equations:**
  - Claim L is false for speech rate, which is released noiselessly through Q.
  - The ablation of reading through one's own body (§3.11, F3) is false: replacing R by any rotation of it changes nothing after replay.
- **Novelty: both clauses fail.**
  - The wrap is the robust-REN direct parameterisation for a conic-sector IQC, the centre-plus-Cayley-radius D₂₂ of Revay et al. eq. (31). Its closure under internal composition is the reason RENs exist.
  - The ledger is Le Ny & Pappas's output-perturbation mechanism with event-level adjacency on increments.
  - The split between the two is an architecture, not a new computation.
- **Fit to put to the operator as a build candidate: no.**

## 1. Principle violations

### 1.1 Principles 1–2 (labels, hand-named emotion variables): essentially clean, with three loose ends

- No classifier, and no emotion label below Claude. Valence and arousal are readouts.
- Loose ends:
  - **Undefined driver.** "Aversive load V … driven by own-predicted harm" (§2.6) names an evaluative driver, "harm", that is never defined. If it is a learned predictor of 𝒟, it is circular. If it is anything else, it is a hand-named variable.
  - **Undefined stance code.** The slots hold a "stance code" (§2.6) that is never defined or trained. §3.13 C5–C6 rely on it.
  - **Fixed name list.** The 16 synergies and 5 articulators of P₀ are a fixed, named list. The brief allows this until S4.

### 1.2 Principle 3 (reading the other through one's own body): neither real in the Yoshida–Man sense nor essential

1. **What is inverted is not a generative model of the body.**
   - 𝓔 maps "own display state → own face". It is trained on pairs (z_own, y^own), and y^own is the agent's own *command* (§2.5, §2.9).
   - Check (A) forbids the agent to see or hear its rendered self. So 𝓔 is a model of the agent's command map, close to an identity on the 18 coordinates, not a model of how its body looks.
   - R = (JᵀJ + λI)⁻¹Jᵀ is therefore a rank-12 projection onto the agent's habitual command subspace, in MediaPipe coordinates borrowed through P₀.
   - No partner *state* is inferred: no needs, no body budget, no appraisal of the partner. Principle 3's second clause, "infers another's state by inverting its own generative mapping", is not implemented.
2. **R's "own-body" nature is not essential: rotation invariance.**
   - Let Q be any orthogonal 12×12 matrix and replace R by QR.
   - The release noise n ~ N(0, σ²I) is isotropic, so the new release X^s′ is equal in law to blockdiag(Q, I, 1)·X^s.
   - Every consumer of X^s has learned input weights refitted nightly: 𝓜's input layer, and the REN's B₂/D₁₂ inside the fibre (the Lipschitz bound is preserved under an orthogonal input map). No equation ties X^s coordinates to y^own coordinates through a shared fixed map: 𝓜 takes them as separate inputs, 17 + … + 24.
   - So after one replay the behaviour is identical in distribution.
   - The only part of R that matters is ker R: which 6 of 18 directions are discarded, plus the singular values.
   - The ablation "R → generic encoder of equal norm" in §3.11, §7 and F3 is therefore predicted wrong by the design's own equations, whenever the generic encoder shares R's row space. That is a Principle 5 failure too.
3. **Mimicry bypasses R.**
   - §3.11 says that with R = 0 "the reflex prior's echo stays on the raw high-passed input path in F". So the innate mimicry, the one behaviour that most obviously is "perceived features drive own motor pathways", runs channel to channel in P₀ coordinates, not through the own-body reading.
   - This contradicts §2.3, "the partner reaches the fibre's learned core only in the agent's own 12 coordinates".
4. **The affect half of Principle 3 is cut.**
   - Principle 3 requires perceived features to drive the agent's own *affect* pathways too.
   - The fibre's output is never read back (Check A). There is no facial feedback, so mimicry cannot produce affect.
   - The only affect route is the ledger, at d′ ≈ 0.34 per expression.
5. **Check (A) blocks S4.**
   - S4 requires the engine's own inverse model, "learned by reproducing faces with its own face". That needs perception of the agent's own rendered face.
   - Check (A) ("the agent never sees or hears itself") forbids exactly that.
   - The design cannot reach the brief's next stage without breaking its one structural check.

### 1.3 Principle 4 (Claude never reads state): satisfied, at a heavy cost

- The prompt is constant. It holds the transcript plus up to 3 raw past-dialogue snippets, and no numbers or labels. Compliant.
- The cost, concretely:
  - **Claude is blind to the face.** It sees only the transcript, so no draft can respond to a face.
  - **The state barely reaches the words.** It reaches them only by choosing 1 of K = 4 drafts (≤ 2 bits per turn) and by choosing snippets.
  - **No mood-congruent wording on demand.** A low mood can only pick the least cheerful of four drafts that were written from text alone.
  - **No naming.** Principle 4 says Claude "names, reinterprets and regulates states". In this design Claude names nothing: §5 concedes "Claude names states only in the sense that its words are chosen by what they predict for the agent's body".

### 1.4 Principle 6 (homeostasis; the face never a reward, target or regulated variable): violated through the arousal and aversive gauges

- Arousal load A is driven by "the magnitude of 𝓜's prediction error on X^s" and "audio energy in X^s". Aversive load V is driven by "loud-audio energy in X^s" (§2.6).
- X^s is the partner's released face and voice. The draft scorer picks the draft that minimises predicted Σ𝒟 over 30 s (§2.8).
- So the agent is optimised to pick replies predicted to make the partner's face and voice **less surprising and quieter**. The partner's behaviour is a regulated variable.
- This is not an engagement incentive. It is a placation incentive: avoid replies that make the user animated, emphatic or upset. That is the same family of failure as flattery: the agent shapes the user to serve its own gauges.
- §3.9's claim "the partner's face appears in no loss and no target" overlooks that A and V are regulated targets fed by X^s.
- (σ_s = 7.1 makes the face part weak. The audio-energy part is not weak, and the structure is wrong either way.)
- A smaller point: information need I rises at a constant rate and is lowered only by learning progress (§2.6). Satiety therefore requires perpetual progress at ≥ 1/30 min⁻¹. That is satiable only in the weak, Oudeyer-style sense. A test should confirm that 𝒟 does not grow without bound in a stable home life.

### 1.5 Principle 7 (data leaving the Mac)

- Raw features stay local, and replay stores only X^s, Q and text. That part is good.
- The **transcript and raw past-dialogue snippets go to the Claude API on every turn** (§2.8). They are derived from the microphone.
- This is common to every design that uses Claude through the API. It is an operator decision (cf. Q3), not a failure peculiar to this design.
- But §5's line "stricter than Principle 7" is not accurate. It should say plainly that speech content leaves the Mac.

### 1.6 A glaring uncounted route (for the route critic): speech rate is released without noise

- The neighbouring relation (§2.4) offsets "voice prosody", which includes **speech rate**, one of the 4 counterpart voice channels. It also declares "words, turn times and identity identical in P and P′".
- These two statements are inconsistent. Speech rate *is* words per unit of turn time, and Q releases both noiselessly: the transcript, and turn start and end times on a 100-ms grid.
- So for the speech-rate direction ε = ∞, and Claim L (§3.3) is false for that coordinate. The slow mind, Π_ψ's voice output and replay can track and follow the partner's held speech rate at any gain up to the display range (0.8).
- The copy metric (§3.6) hides this: it holds "turn times fixed", so a surrogate with the same turn times has the same speech rate, and following it is booked as "common cause".
- The same holds, more weakly, for audio energy through VAD-derived turn times, the floor flag and ASR dropouts (assumption §3.12.1).
- (Ironically, this is the one channel on which the agent *can* show held-level vocal convergence; see §2.)

### 1.7 Principle 10 (one formal core): an assembly under two constraints

- J = E∫𝒟 governs only the choices: draft, attention queries, write gates and display.
- The rest has its own objectives, not derived from J:
  - 𝓛_𝓜 (likelihood);
  - 𝓛_F (fibre: predict own display);
  - 𝓛_𝓔;
  - 𝓛_slot and 𝓛_μ (contrastive);
  - 𝓛_score (calibration).
- There are innate rules besides: the phoneme-trigram echo guard, the floor flag, the four reflexes and the random Q projection.
- **Π_ψ, the face's main driver, has no objective at all** in §6.3.
  - §2.10 says the display policy minimises J. But J depends on the display only through motor habituation H, a self-repetition penalty.
  - So the derived display policy is "vary, so as not to repeat yourself", with no tie to valence, appraisal or what was said.
  - The claim (R14, §2.6) that "the agent's appraisal of what was said reaches its face within 1–2 s" has no equation behind it.
- This is a well-documented assembly, like BabyX, with two strong constraint layers, (W) and (L). It is not one core that the components follow from.

## 2. Does it work as an emotional agent?

| Capacity a person has | This design | Why, from its equations |
|---|---|---|
| Notice from the face that the user is sad, and come to care | **cannot** | A held sad face reaches the slow mind at d′ ≈ 0.34 for the whole episode. That is ≤ 57% correct detection, and any slow statistic correlates ≤ 0.25 with it, *by design* (Claim L). Claude never sees the face. The fibre sees it but writes nothing, and its echo fades with τ_in = 4 s. A silently sad user is not noticed, now or later. The author concedes this (§8.1.1); I count it as a failure because it is what the core property *does*, not a tuning issue. |
| Show a smile back while the partner keeps smiling | no | The innate high-pass τ_in = 4 s inside S means the fast smile response decays to 3·10⁻⁴ after 50 s (G10), and the slow side does not know the smile is still there. A warm, sustained smile gets a brief flicker back, then a face driven by self-repetition avoidance. |
| Be moved over a conversation (a sad story lowers mood) | no | Mood μ is a linear low-pass of the 𝓜 readout. No body variable responds to social meaning: E responds to speaking, A to surprise and loudness, I to own learning, V to loudness and an undefined "harm", H to self-repetition. Valence = −E[d𝒟/dt] therefore does not move with what the story means. The ladder holds a smoothed sentence-embedding memory, not an affect. |
| React emotionally to what is said within seconds | only by assertion | R14 says Π_ψ shows the appraisal of words within 1–2 s. Π_ψ has no training objective linking it to words or valence (§1.7). |
| React to the face within a second, in context (sign set by role, stance, episode: C4, C5, C8; D78 "set by context and relationship, can flip sign") | **no, in practice** | The fibre is trained in replay only on X^s: σ_s = 7.1 per coordinate, low-passed at 1 Hz, upsampled. Regression dilution scales any learned partner→display coefficient by var(s)/(var(s)+σ²) ≈ 2·10⁻⁴ to 2·10⁻³. The 1.0, 2.5 and 4.5 Hz bands get no training signal at all. Training on raw u would break the ledger (fibre weights would depend on u), so this is structural. The fibre stays at S₀, which has no context gating and fixed positive signs. D78's per-expression, context-set, sign-flippable strengths hold for the *reachable parameter set*, never for the *learned* one. |
| A relationship specific to the user, from the face | only over very many episodes | Group composition gives SNR ≈ 0.27√k. Relationship specificity therefore comes from words and the identity token, plus slow face statistics over weeks. That is weak but not zero. |
| Vocal convergence on held levels (Pardo; Levitan & Hirschberg) | no, except speech rate through the §1.6 leak | The voice wrap high-passes across phrases (τ = 3 phrases), and the ledger hides held F0 and energy. The author concedes this (§8.1.3). |
| Interoception | thin | There are 5 innate gauges, all of them predicted by 𝓜. None is socially driven, so interoception carries no interpersonal content. |
| Temperament over months | plausible | There is a 100-night consolidation, 30-day slots and a 73-h mood mode. But the fibre is pinned to θ₀ (λ = 0.5), so fast reactivity cannot develop a temperament. |
| Emotion concepts grounded and named by Claude (the brief's grounding problem) | **absent** | There is no category formation over interoceptive and exteroceptive states, and no route by which Claude names one. |

**Is the persistent state rich, or a few gauges?**
- *Capacity* is large: 327 bits in μ after an hour, and about 2·10⁴ bits in slots, under an assumed write SNR.
- *Content* is what matters. What is written comes from (X^s at d′ 0.34, Q embeddings, 5 non-social gauges, own commands). So the rich store is a store of conversation embeddings keyed by identity and topic, plus a few gauges.
- The *affective* core, the part that has valence, is exactly what the brief calls a sketch:
  - 5 scalar gauges;
  - a scalar drive;
  - a scalar valence;
  - linear leaky maps.
- The expressive-structure item "what the agent needs and expects selects what it perceives" is met only for words and memories. §3.14 concedes that it cannot select over the partner's face content.

**Verdict on fitness as an emotional agent.** These are concrete failures that make it unfit to build as the emotion engine:
- the face-to-affect and face-to-words routes are absent;
- the fast route is unlearnable, so D78's context-set sign is met only on paper;
- no social variable moves valence;
- the display has no objective;
- concepts and naming are absent.

The design is a very good *copy-proof shell*. It is not an affective agent.

## 3. Reduction and novelty

**The wrap is the robust REN, not a new composition.**
- Revay, Wang & Manchester (arXiv 2104.05942 v3, §V-B) directly parameterise RENs that satisfy any incremental IQC (Q, S, R) with Q ≺ 0, for every parameter vector.
- Their feedthrough is D₂₂ = −Q⁻¹Sᵀ + L_Q⁻¹ N L_R, with N a Cayley transform of free matrices (eq. 31–33). That is centre m plus radius times contraction: the disc of §3.1 (W3).
- The conic sector [mκ − rκ, mκ + rκ] is one such (Q, S, R). (W1)–(W4) are the classical loop transformation between γ-contractions and conic sectors (Zames 1966; scattering ↔ positive-real in Anderson & Vongpanitlerd). The design itself says it did not read either (§9).
- "Wrap once, compose freely inside" is precisely why a single REN with one IQC is used: the certificate covers all internal recurrence, gating and sign structure (Revay §IX: "nonlinear but contracting for every Q"). The project's own note on Revay already proposed "make the *entire* partner→face path a single robust REN".
- The Cayley transform as a parameterisation device is standard:
  - Trockman & Kolter 2021, Q = (I − A)(I + A)⁻¹ for orthogonal convolutions;
  - Wang & Manchester 2023, the sandwich layer, built from Cayley for complete Lipschitz-bounded networks.
- N1 (a diagonal bound does not bound the mean direction), N2 (correlated inputs) and N3 (a sign flip at ω is a copy at lag π/ω) are elementary linear algebra and phase arithmetic. They are useful to the project, but they are not new results.
- **Verdict: known.**

**The ledger and the forgetful-fibre split: known parts, one architectural choice.**
- Le Ny & Pappas (*Differentially Private Filtering*, arXiv 1207.4305), read in full, give:
  - Corollary 1: output perturbation of a linear filter G with σ ≥ κ‖G‖·b is DP for ℓ₂-bounded adjacency;
  - Lemma 3: for impulse (event-level) adjacency the ℓ₂ sensitivity is the filter's impulse-response norm ‖g‖₂.
- The design's step offset of any duration is an impulse pair on the *increment* signal. With h_s zero-DC, the filter "integrate, then h_s" is stable, and its sensitivity is the step-response energy E_h, independent of duration. That is Lemma 3 applied to Δu. Gaussian RDP and post-processing (Mironov) finish it.
- Splitting raw data between a non-storing real-time path and a DP-released persistent path is the standard trusted-curator architecture. Pan-privacy (Dwork et al. 2010), where internal state must itself be DP, is the closest formal relative. I have not read it, so I do not rely on it.
- The split deletes the fibred design's scalars, and the author says so. But deleting another *design's* scalars is not the second clause's "removes a named, measured failure by deleting a free scalar of the computation".
- It also adds one scalar: ε_L is a single innate quantity that runs the whole slow mind from face-blind to face-tracking. The author names it "the knob" (§8.1.1).
- **Verdict: known parts. The split is an architecture, not a new computation.**

**Other parts:**
- 𝓜 is an LRU (Orvieto et al.).
- μ is a fixed bank of leaky integrators.
- The slots are attention memory.
- The drives are homeostatic RL.

**Clause 1 fails, and so does clause 2.** No computation's signature or defining invariant is new. The one invariant ("one-sided end to end") is the IQC certificate of an existing model class.

**One false premise worth fixing (§4 of the design):**
- The design says "contraction forbids persistent states, so they must live outside [the REN]". Contraction forbids *multistability*, not *slow memory*.
- A REN with contraction rate ᾱ = 1 − 10⁻⁵ per frame has hour-scale memory and is still in the sector. The design's own μ ladder is a contracting linear system.
- So moods *could* sit inside the wrap. The slow mind could then know the partner's held face, while its copy-direction effect stays ≤ 0.20 in phase at DC and sign flips up to 0.60. The ledger would be needed only for discrete routes: draft choice, retrieval and memory writes.
- This is a concrete repair for §2's worst failure. It remains a recombination.

**What would have to change for a real new primitive.**
- The project's recurrent obstacle is that every available bound is either magnitude-only (IQC) or sign-blind (DP, information).
- A genuinely new object would bound the *direction* of influence for a state that *persists and knows*. Two directions:
  1. **A directional divergence.** It would price only the part of the information about the partner that can move the agent's expression into the copy cone. For example, a ledger whose per-release cost is the RDP of the release *projected through* the sector-violating part of the downstream map. That would make care cheap and copying expensive.
     - No DP variant can do this, because divergences are invariant to bijections (Kairouz, as the author notes).
     - So a working definition, with a composition theorem and post-processing closure, would add something neither source has.
  2. **A sector certificate for non-contracting, multistable state.** It would hold over switching between wells (for example a dwell-time IQC whose DC sector holds across every well), so that persistent moods can know the face and still never move toward it beyond bκ.
- Neither is in the design. Without one, the design is a careful recombination, as its author says.

## 4. Fit to put to the operator as a build candidate (Q19)

**No.** Q19's bar is "no known concrete failure", and there are several:
1. **The emotional exchange the brief exists for does not happen, by construction.**
   - The user's face cannot change the agent's feelings, words or lasting state beyond d′ ≈ 0.34 per expression.
   - The brief's goal is "each side's expression moves the other's state".
2. **Claim L is false for speech rate** (§1.6). There is an uncounted noiseless route on a counterpart channel, and the copy metric is defined so that it cannot see it.
3. **The fast route cannot learn.** Regression dilution of about 10⁻³, and no training signal above 1 Hz. So D78's "set by context and relationship, can flip sign" is unmet in practice, and C4, C5 and C8 are not produced.
4. **Principle 3 is inessential**: invariant to rotations of R, so the §3.11 and F3 ablation is wrong. Check (A) also blocks S4.
5. **Principle 6:** the draft scorer regulates the partner's quietness and predictability through A and V.
6. **No social variable moves valence; Π_ψ has no objective; no emotion concepts or naming.**
7. **Novelty: both clauses fail.** The brief requires at least two genuinely new candidates, and this one is not one of them.

The two parts worth keeping as constraint layers for a future core are the wrap, used as a robust-REN sector certificate, and the zero-DC level-neighbour release.

## Concrete changes (in order of importance)

1. **Stop censoring knowledge; bound expression instead.**
   - Move the slow affective state (μ, and the part of 𝓜 that reads the face) *inside* a wrapped, slow-contracting REN, so it can know held partner levels while its counterpart output stays in the sector at every frequency, DC included.
   - Keep the ledger only for discrete routes: draft choice, retrieval and memory writes.
   - Then ask the operator plainly whether a slow state that *tracks* the user's held face, but cannot move toward it beyond 0.20, is acceptable. Report 4 treats tracking itself as a failure, and that criterion is what forbids care.
2. **Give Claude the face, without numbers.**
   - For example, condition retrieval on face-derived slow state, so that Claude is handed past episodes in which the user looked as they do now.
   - Or raise K and let the state select among drafts written for different stances.
   - State how many bits per turn the state can steer.
3. **Social body variables.** Add a satiable interoceptive variable moved by the agent's own appraisal of what happens to the partner, "comfort as I'd be comforted" in the regulator design's sense. Do not feed A and V with partner loudness or partner predictability. That fixes Principle 6 and gives valence social content.
4. **Give Π_ψ an objective derived from J,** for example display as the action that the 𝓜 rollout predicts lowers 𝒟, and show that the display depends on valence.
5. **Make R essential.**
   - Tie weights so the partner reading and the agent's own state pass through one shared encoder into the same latent coordinates, which makes "own-body" carry content.
   - Or drop the claim and rewrite F3.
   - Allow self-observation of the rendered face for 𝓔 (needed for S4), and recheck Check (A) with that read-back counted.
6. **Close §1.6.**
   - Either release turn times with noise, or add speech rate, pauses and VAD-derived energy to the counted routes.
   - Remove "turn times fixed" from the copy surrogate for the voice channels.
7. **Train the fibre on something it can learn from without breaking the ledger,** or concede that the fast response is innate and context-free, and reconcile that with D78 and C4, C5 and C8.
8. **Add concept formation** (categories over interoceptive and exteroceptive states) and a route by which Claude's words name them. Otherwise the grounding problem is unanswered.
9. **Novelty.** If the project wants a new primitive here, pursue one of the two objects in §3: a directional divergence ledger, or a sector certificate for multistable state. Leave the rest as is.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full |
| research/questions.md | Q16, Q17, Q19 in full; also Reports 3–4, Q8–Q10, Q15, Q18 with its answer |
| research/foundations/designs.md | in full |
| research/new-mechanisms-synthesis.md | in full |
| research/foundations/design-cayley-ledger.md | in full (§0–§10) |
| foundations/sims/design-g/out.txt | in full; checks.py grepped for G5a and G6 |
| research/revay-2023-recurrent-equilibrium-networks.md (project note) | in full |
| Revay, Wang & Manchester, arXiv 2104.05942 v3 | §III (IQC special cases) and §V-B (robust REN direct parameterisation, eq. 28–33, special cases), read in the original. Not re-read in full |
| Le Ny & Pappas, *Differentially Private Filtering*, arXiv 1207.4305 v2 | in full, references included |
| Wang & Manchester, *Direct Parameterization of Lipschitz-Bounded Deep Networks*, arXiv 2301.11526 v3 | main text §1–6 in full, appendices A–B; later appendix proofs not read |
| Trockman & Kolter, *Orthogonalizing Convolutional Layers with the Cayley Transform*, arXiv 2104.07167 | §1–4 in full (Cayley bijection, Fourier-domain inverse, properties); §5 experiment tables skimmed |

**Not read, and not relied on except as named pointers:**
- Zames 1966;
- Anderson & Vongpanitlerd (the scattering ↔ positive-real Cayley map, which I know only as standard textbook material);
- Dwork, Naor, Pitassi & Rothblum 2010 (continual observation; cited through Le Ny & Pappas);
- Dwork et al. pan-privacy;
- Kairouz et al. (cited through the design);
- Orvieto et al. (LRU).

The novelty verdict does not depend on any of these: the REN and Le Ny & Pappas texts already contain both composition results.
