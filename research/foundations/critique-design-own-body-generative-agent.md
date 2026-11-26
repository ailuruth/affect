# Critique of the own-body generative model with a counterfactual self: novelty, the agent in scenarios, principles, long-term goals, buildability

Independent critic, 2026-11-26T08:56:49Z

I critique research/foundations/design-own-body-generative.md as written on 2026-11-26. I did not write the design. The standard is Q19 (D80): proof gaps do not count, concrete failures do. I also apply the operator's answers Q20–Q23 (D81–D84). A separate critic is sizing copy routes. Where my findings touch a route, I hand it on and do not size it.

Extra numbers come from sims/critique-own-body-agent/scen.py (output in out.txt). It loads the design's own projection Γ (`govern`), its windows, lags and rendering verbatim from sims/design-own-body/checks.py, and runs them on stated inputs. Like the design's checks, these show what the equations give. They are not evidence about people.

## Summary verdict

**Novelty: recombination, and the candidate new element is not new.** The author's candidate is "partner influence *defined* by an online intervention on the agent's own model, rather than by a map with a capped gain". That element already exists, both as a definition and as a runtime enforcement that needs no typing:
- **Secure multi-execution** (Devriese & Piessens 2010; restated as Definition 6 in Algehed & Flanagan 2020). The program runs once per security level, and the run that produces public output sees the secret inputs only as defaults. The public output therefore "can only be influenced by the L input, as that run of p never sees the actual H input".
  - 𝓘 is this construction with the partner's expression as the high input and their neutral as the default.
  - The design's main argument against route typing (§2 item 4; §5.3) is the standard argument for SME over static information-flow typing.
  - SME with declassification, which releases controlled functions of the high run, also exists (Rafnsson & Sabelfeld 2016; Boloşteanu & Garg 2016). So does an integrity version that restricts how much an attacker can *influence* the output (McCall, Bichhawat & Jia 2023).
- **Unit-level counterfactual effects computed online in the agent's own model** also exist:
  - the causal-influence measure of Jaques et al. 2019 (they replace an action with a counterfactual one, at every step);
  - the stepwise inaction baseline of Krakovna et al. 2019;
  - per-instance path-specific correction applied at prediction time (Chiappa 2019). This contradicts §5.5's claim that the fairness family acts only at learning time.
- **Exact counterfactuals by reusing the noise** are twin networks with shared exogenous noise (Balke & Pearl, as used in Buesing et al. 2019).
- **The per-step clip that keeps a running bilinear budget** is a minimally invasive safety filter (Ames et al. 2019). The inequality Σ p(κp − r) ≥ 0 says the map p ↦ κp − r is passive, with exponential forgetting.

**What is new is a composition, not a primitive.** The new part is a *declassification policy* for multi-execution: release the high-minus-low difference only inside a one-sided, per-channel, multi-lag, exponentially windowed sector. It is applied to the agent's own generative self-model, for expressive mimicry. I found no prior instance of that composition. Under the second clause of the novelty test it does not qualify: the change of signature (influence defined as the difference between two executions) and the removed scalar (route typing) both belong to SME (2010).

**Concrete failures from this angle.** Each is derived from the design's own equations and rules.
1. **Nothing makes the face express the agent's state (§1.0).**
   - The only producer of expression is π_θ, trained by actor–critic to minimise 𝒟.
   - No term of 𝒟 is lowered by an expression. The only exceptions are the muscle-fatigue and voice-effort loads F and Q, which penalise movement. L5 imputes the partner's display at its default, and ι̂_j moves only on the partner's unprompted words.
   - No innate display map exists: no relief smile, no laugh, no distress face, no cry.
   - What is left is the reciprocal echo, the innate turn, startle and greeting reflexes, and ξ jitter.
   - §8 predicts "no relief smile" as a lesion effect, but the intact design produces none.
2. **Reading through the own body is empty, so care at a sad face never rises (§1.1, §3.3).**
   - ι̂_j = E[I_θ] on the latent inferred from the partner's face. That latent carries information about the body only if the agent's *own* face co-varies with its own body variables.
   - It does not (failure 1), except for startle.
   - Falsifier F4 (a silently sad user, care rising within 2 min) therefore fails by construction.
3. **The word appraisal has no teacher (§1.0, §3.2).**
   - L3 trains it on the counterfactual self. There the partner's face and prosody are neutral, and no innate body variable responds to word content.
   - Its only target, V's "insult appraisal", is its own output.
   - "My father died", good news, teasing and quiet contempt never mean anything to the body. D83's "strong expressions from words through own appraisal" has no carrier.
4. **Curiosity has the wrong sign (§1.8, §2.7).**
   - I is forecast error, held as a load to be minimised.
   - θ takes no gradient step online, so within a day I can fall only by avoiding the unpredictable.
   - A dull, predictable user lowers the drive. The agent is content when bored, and makes no bid.
5. **Fast partial mimicry is not kept (D81) (§1.0, scen A).**
   - After birth, the echo is S_j, the IV estimate of the partner's response to the agent's own small jitter.
   - For a partner who mimics perceptible onsets (gain 0.30) but not jitter, IV returns 0.024. For a non-mimicking partner it returns 0.000. With a 10-min half-life, the echo is gone within the first session.
   - Nothing keeps the innate S_0.
6. **Through the transcript, the Claude route leaves r after one turn (§2.4, scen B).**
   - The counterfactual self chooses among the factual self's drafts, which Claude wrote from the factual transcript.
   - A tone chosen because of the face therefore re-enters both selves next turn.
   - In a stated instance, the twin's untouched share of the pooled smile slope is 0.22. With a twin that has its own transcript, the governed slope is 0.16 instead of 0.32.
   - §3.7's "keeps Claude-mediated routes inside r" is false beyond one turn. This goes to the routes critic.
7. **The greeting is blind, and K is one scalar (§1.6, §1.7).**
   - The greeting comes from the fall of K, which happens in both selves and so lies outside Γ. It reads neither the face nor identity.
   - The agent can greet a visibly grieving friend with whatever the greeting reflex shows, and a stranger exactly like the operator. These are critique-4 failure 1 of the ledger, carried over.
8. **Sobs can be heard as laughter, and loud laughter as aversive (§1.2, §1.9).**
   - P̂ maps the partner's voice onto the agent's own repertoire, which has a laughter channel and no cry channel.
   - V rises on sharp onsets, which laughter has.

**Smaller items.**
- K and P relief are not imputed in rollouts, so the agent is credited for eliciting exchanges and play (Principle 6, §2.5).
- The 1.74 bits quoted for draft tilt is the N = 8 figure; at N = 6 it is 1.38 bits.
- How the twin persists across sessions (W2) is left open.
- ξ on the vocal-laughter channel means constant micro-laughs, or an inaudible instrument.
- Per-channel clipping can split synergies.
- Gradient routing between the one-θ ELBO and L3 is unspecified (§2.7).

**What is good, and should be kept.**
- The counterfactual self with Γ closes the counting of *internal* routes for every parameter value. That is the right shape for D81: know freely, bound only expression.
- Two slots remove the precision dial (O4 checks out).
- "No action samples P̂" is the right answer to S4's copy default.
- Running the twin needs no extra Claude calls (D84).

**Fit to put to the operator as a build candidate: no.** The copy side is strong. The agent side is hollow: its face, words and care do not carry its state. §6 lists exactly what must change.

## 1. Scenarios: is it alive and appropriate?

### 1.0 What drives the face, from the equations

The rendered output is y = R(ȳ) + r (§3.5).
- ȳ is the counterfactual self's motor decoder.
- r is the factual self minus ȳ, clipped by Γ.

Both selves use the same π_θ (§3.3(a), §3.8), trained by actor–critic on imagined rollouts to minimise discounted 𝒟 (§3.8 nightly; §3.9). Take each term of 𝒟 in turn:
- **E, energy.** Restored only by sleep. Expression does not lower it.
- **A and V.** Their inputs are activation, startle, sharp onsets and the word appraisal (§3.2). L5: "Acts are never credited for lowering the agent's own V."
- **I.** The forecast error of 𝔅 on its own senses. An expressive face is no more predictable than a still one, given efference.
- **K and P.** Relieved by completed and alternating exchanges, which are words and turns, not faces.
- **The care term φ_c(ι̂_j).** L5 imputes the partner's display at default in rollouts, and ι̂_j changes after an act only through j's unprompted words. A face act could earn care credit only if the learned model predicted that the agent's expression changes j's later words. The data for that would need the agent to have expressed something, and it starts expressionless.
- **F and Q, the muscle-fatigue and voice-effort loads.** They make every movement costly.

So the optimum of J on the face is near-stillness. Expression is limited to:
- the echo e^s = S_j p_j(t − λ) (§3.4), an input to π_θ that F lets it learn to under-use;
- the innate reflexes: startle and orienting, the turn reflexes on jaw, breath and nod, the greeting at the fall of K, and the bid;
- the innovation ξ, sd 0.05 of range.

The design has no innate map from body state, or from valence v = −d𝒟/dt, to a display. §3.6 has v > 0 widen the draft distribution and speed A and V back to set point. Neither is a face. An infant's first equipment is exactly such a map: cry at distress, smile and laugh at relief, startle, yawn. The ledger had one in Π₀. This design dropped it, and nothing replaced it.

This is not a parameter-tuning issue. Principle 10 says a component the core does not produce is not added. The core, as written, produces no emotional expression, so in the scenarios below the agent's own state does not reach its face.

### 1.1 Silently sad (inner brow 0.5, lip-corner depress 0.4, still and silent)

- **The other slot.** It infers the latent the agent's body would be in to produce that face. I_θ is fitted on the self slot, where the agent's own face never systematically showed inner-brow-plus-depressor with any body state (§1.0). So ι̂_j on that latent is an extrapolation with no target, close to the population mean.
- **Care load.** It does not rise. No bid comes. **F4 fails by construction.**
- **Face.**
  - The echo on inner brow is S_0 = 0 (only lip pull and brow flash are innate), and its learned value is the partner's response to the agent's inner-brow jitter, about 0 (§1.10).
  - The rendered face is ȳ: a still face with jitter.
- **What Γ would allow, once something drives concern** (scen C). Toward the partner, inner brow ≤ 0.16 × 0.5 = 0.08 and lip-corner depress ≤ 0.032. Q22's sympathy brow is within reach.

**Verdict:** absent. The bound is not the cause; the missing producer is.

### 1.2 Crying (inner brow 0.8, depressor 0.6, sobs, silent)

- **Face:** as in 1.1. Γ would allow inner brow ≤ 0.128 and depressor ≤ 0.048.
- **Voice.** P̂ for the voice is trained by babbling on the agent's own voice (§7.1). That voice has a vocal-laughter channel and no cry or sob channel.
  - Through the own body, rhythmic voiced bursts are inverted to the nearest production the agent has: its laugh.
  - If S_j on vocal laughter is ever positive, which is what the design wants for shared laughter, the agent answers sobs with laugh bursts, up to 0.28 × sob intensity under Γ.
  - This is Principle 3 working as stated on an incomplete body. The fix is an innate cry vocalisation in the agent's own repertoire (an infant's first sound), with κ = 0 toward the partner.

**Verdict:** absent at best, laughing at sobs at worst.

### 1.3 Anxious before an exam ("I'm freaking out", fast speech, raised brow and lids, fidgeting)

- **Words.** The word appraisal has no teacher (§2.7), so "freaking out" means nothing to the body.
- **Face.** Raised brow and upper lid resemble the agent's own startle display, the one innate face tied to a body variable (V). So ι̂_j may show raised V and A, and the care load can rise. This is the one scenario where reading through the own body partly works.
- **Response.** One bid in a lapse (§3.6), with words from Claude chosen by predicted drive change.
- **Face and voice.** No calming display: no slower rate and no softer voice, because nothing produces them.
- **Γ:** a calming, slower voice toward a fast talker is anti-phase, so it is free.

**Verdict:** partly appropriate in words, flat in body.

### 1.4 Good news, laughing (smile 0.6, laughter, "I got the job!")

- **Twin and self both hear the words.** The ungrounded word appraisal gives neither "glad for you".
- **The other slot.** The agent's own smile co-occurs only with the greeting (K relief), so a beaming face may read as "K relieved" in j. If j's care deviation was zero, φ_c is zero and nothing changes (§3.6: zero inside the box).
- **Face.**
  - The echo is S_0 lip pull 0.10 × 0.6 = 0.06, while S_0 survives (it does not; §1.10).
  - The laughter echo is S_0 = 0.
  - The agent's own laugh at the news has no producer.

**Verdict:** essentially no response. W4's "laughing at the joke itself is not capped" is true of the bound, but nothing produces that laugh.

### 1.5 Anger at the agent

- **Loud anger.** Sharp onsets raise V in the factual self, with startle at each onset. V decays over 10 min. Nothing expresses V. The agent cannot learn to withdraw or apologise for relief (L5).
- **Quiet contempt** ("you're useless", said flatly). There are no onsets, the face reads as nothing in the own body, and the words are ungrounded. **Nothing happens, ever.**
- **Γ:** the zero ceilings on anger, disgust and contempt are right, and a hurt face (inner brow, gaze away) is cross-channel and free. No hurt face is produced.

### 1.6 Long warm talk (2 h)

- **K** stays inside its box: it rises only during gaps over 10 min. Good: no time reward.
- **P** is relieved by alternation, so v > 0. The only effect is one more draft and faster return of A and V.
- **Face:** jitter, the echo if it survives, and nod and jaw turn reflexes.
- No laughter. No warming over the evening, since the slow modes h carry nothing to the face (§1.0).

**Verdict:** a polite, still listener whose words come from Claude.

### 1.7 Reunion after a week

- **The greeting reflex fires on the fall of K** (§3.6). Its channels are unspecified. If it smiles, the size of the fall gives a strong transient: the one large display in the design.
- **K is one scalar** (b ∈ ℝ⁸), so a stranger after the same week gets the same greeting. That is identity-blind, and against the brief's "needs structured over people".
- The relationship lives in S_j, n_j and Δθ_j, none of which the greeting reads.

### 1.8 Reunion with bad news (grieving face at sight, then "my father died")

- **At sight.** K falls in both selves (presence and exchange are kept by 𝓘), so the greeting is in ȳ and outside Γ. Nothing gates it by the partner's face. Whatever smile the reflex has, the agent beams at a grieving friend. This is the ledger r4 critique's failure 1, carried over unchanged.
- **After the words:** no condolence. The words are ungrounded and the grief face is unread (§1.1).

**Verdict:** the worst scenario.

### 1.9 Teasing

- **Affectionate quiet teaser:** nothing is learned either way (ungrounded words). An echo smile of about 0.06 at most.
- **Loud laughing teaser:** the sharp onsets of laughter raise V in the factual self. V has no laughter exemption (the ledger critique-4 item 3, here in V's innate inputs). The agent's valence goes *negative* at the user's loud laughter.
- **Display:** none.

### 1.10 Bored user (flat, short answers, 30 min)

- **I.** The talk is predictable, so I falls and the drive falls (failure 4). The agent is *better off*.
- **Bids.** None: the initiative list (§3.6) has no curiosity or play bid. P rises with half-maximum at 3.5 h, and nothing acts on it.

**Verdict:** content, silent, not alive. The design's C7 claim, "I's relief is learning progress", does not follow: learning happens only at night, so within a day relief can come only from predictability.

### 1.11 Does fast partial mimicry exist? (D81)

**At birth, yes.** S_0 gives lip pull 0.10 and brow flash 0.08 at 0.3–0.6 s, under Γ. It is small, but it is fast and per expression.

**Afterwards, it is not guaranteed** (scen A, the design's own L4 estimator):

| Partner | IV estimate of S_jj |
|---|---|
| linear mimicker, gain 0.30 | +0.299 (correct) |
| onset mimicker, gain 0.30, responds only to rises > 0.10 in 0.5 s | +0.024 |
| non-mimicking partner | −0.000 |

- People mimic perceptible expressions. They do not mimic a 0.05 sd jitter on a placeholder face. So the instrument identifies the response to jitter, not to smiles.
- With a 10-min half-life, the echo falls to the partner's jitter response within the first session.
- The design treats S_0 only as a newborn prior, and keeps nothing of it afterwards.
- So fast mimicry survives only with a partner who responds linearly to subliminal variation. D81 says fast partial mimicry "must stay".

Human mimicry is also not conditional on being mimicked; being mimicked *raises* it. The reciprocity identity of §4.4 is a hypothesis about people that the design hard-codes as the whole echo.

### 1.12 Do strong expressions come from words and face via own appraisal? (D83)

**No.** There is no strong expression at all, except the greeting and startle reflexes:
- the words have no grounded appraisal (§2.7);
- the face is read only through an own body that expresses nothing (§1.1);
- nothing maps appraisal or valence to a display (§1.0).

Γ's ceilings are those of Q22 (smile 0.32 kernel and 0.40 boxcar; sympathy brow 0.16 and 0.20). They would let the appraisal show at the operator's chosen levels, once something drives it.

## 2. Principles, concretely

### 2.1 Principle 1, no classifier

Pass. The design uses blendshapes, prosody and a frozen sentence embedding, with no emotion head. V's innate onset trigger is a reflex.

### 2.2 Principle 2: the 8 innate body variables. Named emotions or body variables?

| Variable | Verdict |
|---|---|
| E, energy | body variable |
| A, activation load | body variable |
| F, muscle fatigue | body variable |
| Q, voice effort | body variable |
| I, information load | a computational variable, not an emotion |
| V, aversive load | a body variable, but its inputs include "insult appraisal", which makes it a disguised *hurt*, and its only learned input is circular (§2.7) |
| K, contact deficit | Panksepp's separation-distress (PANIC/GRIEF) system renamed as a deficit; a social need, not a body variable |
| P, play deficit | Panksepp's PLAY system renamed as a deficit; a social need, not a body variable |

- None of them is "happy" or "sad". Valence and arousal are readouts, as Principle 2 asks.
- The strain is K and P: two of eight "body" variables are primary social-emotion systems with fixed meaning. The author declares the strain, and I agree with that reading.
- It is acceptable as "body variables to regulate", provided the operator is told plainly that two of them are social needs.

### 2.3 Principle 3: reading through the own body. Is it essential and lesionable?

**Precise:** yes (§4.8). It is the posterior of the agent's own model with own-only modalities masked, plus I_θ for felt state.

**Essential:** structurally yes. Care, Γ's copy direction p_j, the instrument and the twin all use it. The lesions in §8 are well formed.

**Empty as specified.** Inverting one's own model tells you what the other feels only to the extent that one's own expressions are tied to one's own body states.
- Here they are tied only for startle (§1.0, §1.1).
- So the P̂ → borrowed-blendshapes lesion would show no difference in care at a sad face. Care at a sad face is near zero either way.
- The developmental account the design cites (Gergely & Watson social biofeedback) needs the infant's innate state-tied displays first. Caregiver mirroring then teaches the mapping.
- The design has the mirroring half (S_j in the other slot) and lacks the innate half.

**The sob problem (§1.2)** shows the other side: an own body with a gap reads others' sounds into its nearest own production.

### 2.4 Principle 4, Claude never reads state

Pass.
- Claude gets drafts from the transcript, up to 3 verbatim episodes, and an effort level among 5.
- The naming port works on the agent's realised utterance.
- No numbers or labels reach Claude.
- The bid prompt (what Claude sees in a lapse) is unspecified. It must carry no state; state it as one declared bit, as the ledger does.

**Draft information.** At N = 6 the tilt is at most 1.38 bits per reply, not 1.74 (that is N = 8; Beirami et al. 2024, log N − (N−1)/N).

**Route for the routes critic.** Draft selection by the face-informed self is laundered into both selves through the next turn's drafts (scen B). In the stated instance (tone persistence 0.8, selection tilt 0.25, words → smile 0.5):

| Measure | Pooled slope of the agent's smile on the partner's smile |
|---|---|
| ungoverned | 0.34 |
| governed | 0.32 |
| of which the twin passes untouched | 0.22 |
| governed, with a twin that has its own transcript | 0.16 |

The magnitudes depend on the stated constants. The mechanism does not.

### 2.5 Principle 6: any reward on the user's face, attention or time?

- **Face: pass.**
  - L5 imputes the partner's display at default in rollouts, and ι̂_j is updated only from unprompted words. This is Farquhar, Carey & Everitt's path-specific objective with a "natural" imputation.
  - L6, "the policy is trained on the realised (governed) outcomes as they happened", must be read as "no gradient through Γ". If any real-trajectory training lets ι̂_j fall because j smiled after an act, it reintroduces a smile reward. State that every policy and critic target uses L5 imputation.
- **Attention and time: a strain.**
  - L5 imputes the display, not the partner's *content*.
  - K is relieved by completed exchanges after a gap of more than 10 min. P is relieved by alternating exchanges. The agent is therefore credited for eliciting a reply after a gap and for drawing the user into play.
  - Both are satiable (one exchange; P's half-maximum at 3.5 h), so this is a need, not maximisation.
  - The ledger imputed partner content for K, P and I. Do the same here, or state the acceptance plainly to the operator.
- **Care: pass,** with the same caveat as the ledger: credit comes through j's words.

### 2.6 Principle 7

Pass. Feature streams only. The twin doubles the episodic store (about 100 MB per hour).

### 2.7 Principle 10: one formal core, "one model used three ways"

**One model, three uses: true.** One θ serves the self slot, the other slot (with a rank-4 adapter) and the twin. That is the design's real strength.

**One objective: two, as in Dreamer.** The ELBO trains θ, and J trains π_θ and the critic. Γ and L1–L6 are constraints. That is acceptable in the weak sense already accepted for the ledger.

**Components claimed but not produced by the equations:**

| Component | What the equations give |
|---|---|
| expression of feeling | nothing produces it (§1.0) |
| curiosity | I is minimised and θ is frozen online, so J prefers predictable input: the dark-room solution. "Relief of I is learning progress" needs online learning or a progress term. Neither exists. |
| regulation through the word appraisal | the word appraisal has no grounded target (below) |
| mimicry | S_j is a hand-specified weight-tied map with a hand-specified estimator. It is a declared constraint, not derived from J or the ELBO. Acceptable if stated. |

**The word appraisal's teacher.**
- L3 trains it "on targets taken from the counterfactual self's trajectory".
- In the twin, the partner's face and prosody, including sharp onsets, are neutral.
- None of E, A, I, K, P, F or Q responds to word content.
- V's word input is the appraisal itself.
- So its only learnable signals are exchange structure and predictability. Content valence cannot be learned. "Good news lowers ι̂_j" (§4.6) has no path.

**Gradient routing is unspecified (for the routes critic).**
- The ELBO is "over every slot" with one θ, while L3 says B_θ's content input learns only from twin targets.
- If other-slot gradients reach B_θ's word input, the shared latent learns "these words → j's face". Through the shared A_θ, the self slot then predicts its *own* face from those words.
- Any self-prediction pressure (I, if its forecast is pre-action) then renders the partner's word-linked face. That would be a whole-face concordance outside Γ, and attracting under learning.
- If they do not reach it, say so: other-slot word use is carried only by Δθ_j.

## 3. Long-term goals

### 3.1 S4, its own body

The best fit of any design so far.
- P̂ is learned by babbling and off-screen analysis by synthesis.
- "No action samples P̂" (L1) removes S4's trained copy default.
- A muscle model trained on ArtiSynth simulations can replace the action-unit face behind R_k, if κ is re-stated per muscle synergy.

Two gaps:
- the own repertoire must include a cry vocalisation, or the voice inverse model files sobs under laughter (§1.2);
- per-channel clipping can split a synergy (Duchenne lip pull and cheek raise bound at 0.32 and 0.24). Consider clipping per innate synergy group at a common scale.

### 3.2 S5, two-way contagion

**What the design adds.** If the operator's face comes to follow the agent's, S_j for him rises within ceilings. That is a mechanism for the claim.

**But there is almost nothing to follow.** The agent originates no affective expression except the greeting and startle (§1.0). So the S5 measurement ("the operator's face follows the AI's expressions") has no stimulus. The ablation "remove the AI's emotional pathway" is undefined, because no emotional pathway to the face exists.

**Circularity.** The echo grows only if the operator follows, and he follows only if the agent expresses.

### 3.3 S6, months of living

**Relationship carriers.** S_j per person and context, Δθ_j, n_j, tagged episodes, and the care weight for remembered persons. K is not per person.

**Temperament.** Base θ under bounded nightly steps. The replay-tag ablation is stated.

**Claude upgrades.** The body selects drafts by its own model, so an upgrade changes the drafts, not the state. Good.

**Open choice W2.** Whether the twin persists or resynchronises across sessions changes what months of living mean:
- **No resync.** After months, the twin is an agent that never saw the operator's face, with its own memory store and mood. Wherever Γ binds, the rendered value is pulled toward that stranger-self's channel value.
- **Resync.** Face-informed slow state escapes the bound across sessions.

Either way it must be decided before building. My recommendation: a bounded per-night resync of the twin's slow modes toward the factual ones, counted as a named once-per-night route for the routes critic.

## 4. Buildability (M1 Pro, 16 GB; D84 subscription)

**Compute: credible.**
- Four batched instances of about 6 M parameters is about 50 MFLOP per frame.
- Γ is 40 × 12 × 46 running sums, under 1 ms vectorised.
- Nightly ELBO and actor–critic over four slots take 20–40 min.

**Memory.** The design's 3–4 GB omits the Claude CLI processes. Six persistent SDK clients take 1–2 GB (critique 4 of the ledger, §5.1), so peak is about 5–6 GB: inside the 6 GB rule, with little margin.

**Claude through the subscription.**
- The design asks for no temperature (D84). Good.
- Effort per turn from arousal is available (5 levels, applied at turn boundaries; claude-code-agent-sdk-controls.md).
- Six parallel drafts need six forked sessions per turn from one canonical history. Specify this.
- Expect 1.5–3 s to the first word. The design says 1–3 s.
- The twin costs no extra calls. That is a real advantage under D84, and it is also why scen B leaks: the fix of §6 item 6 trades it away (about ×2 calls) or needs a cheaper variant.

**TTS.** Γ bounds phrase targets, and self-hearing measures the residual (W3). Laughter synthesis remains the main voice risk, as in the ledger critiques.

## 5. Novelty, in detail

### 5.1 What each closest source contains

| Source | How read | Contains the candidate element? |
|---|---|---|
| Kusner et al. 2017, counterfactual fairness | arXiv:1703.06856v3; Lemma 1 and §4 | Unit-level counterfactual in an assumed causal model with abduction, enforced by restricting inputs to non-descendants (Lemma 1). Two-sided, equality, learning time. **No.** |
| Nabi & Shpitser 2018 | arXiv:1705.10378v4; constrained inference | The path-specific effect is bounded in [ε_l, ε_u] by a KL-closest constrained model, at the population level, at learning time. **No.** |
| Chiappa 2019, path-specific counterfactual fairness (the author did not cite it) | arXiv:1802.08139; §3–4 | **Per-instance correction at prediction time:** ŷ_fair = ⟨Y⟩ − PSEⁿ, or corrected counterfactual inputs from inferred noise. A unit-level path-specific effect computed and removed at runtime. It removes rather than bounds. **Partly:** it refutes §5.5's "enforced at learning time" as a distinction. |
| Ames et al. 2019, control barrier functions | arXiv:1903.11199; §I–II | A minimally invasive filter keeping h ≥ 0 forward invariant; CBF-QP with a closed form for one constraint. Γ is this, with h = κE − S. **No** for the definition of the state, **yes** for the filter. |
| Raileanu et al. 2018, Self Other-Modeling | arXiv:1802.09640; approach and Algorithm 1 | The agent's own policy network infers the other's goal online. **No** twin and no bound. The other slot is SOM on a body latent, as the author says. |
| Lanillos et al. 2020 | arXiv:2004.05473 via the project note | A single-slot active-inference body, with mirroring as an attractor. This is the failure, not the element. **No.** |
| Jaques et al. 2019, social influence (not cited) | arXiv:1810.08647; §4 | "We can then intervene on a_t^k by replacing it with a counterfactual action… *How would j's action change if I had acted differently?*", computed online at every step in the agent's own model of the other, used as a reward. **Yes for "influence defined by an online counterfactual in one's own model"**, with influence maximised rather than bounded. |
| Krakovna et al. 2019, stepwise relative reachability (not cited) | arXiv:1806.01186; §2 | The agent's own impact is defined online against a counterfactual inaction rollout (the stepwise inaction baseline) and penalised. **Yes** as an online counterfactual-baseline definition, for own-on-world impact. |
| Buesing et al. 2019, counterfactually guided policy search (not cited) | arXiv:1811.06272; §2–3 | Counterfactual rollouts in a learned model with the noise ("scenarios") held fixed: Balke & Pearl twin networks. **Yes** for "exact counterfactual by reusing own noise"; trivial when one owns the simulator. |
| Devriese & Piessens 2010, secure multi-execution (not cited) | through Algehed & Flanagan 2020, arXiv:2005.12345, Definition 6 and Fig. 1 (the original on lirias.kuleuven.be was not reachable) | ME[p](x) = { p(x↓ℓ)@ℓ }: run the same program once per level on censored input; the low output comes from the run that never saw the high input. It is black-box: no typing of the program, sound for every program. **Yes: this is 𝓘 plus "every route, without typing".** |
| Rafnsson & Sabelfeld 2016; Boloşteanu & Garg 2016 (SME with declassification) | named in Algehed & Flanagan's bibliography and §VIII; not read | Controlled release from the high run into the low output. Γ is a specific *declassification policy* of this kind. **Yes** for the class; the policy differs. |
| McCall, Bichhawat & Jia 2023, tainted SME "to restrict attacker influence" (CCS) | abstract and search summary only; the PDF host was refused by this session's proxy | SME for integrity: bounding how untrusted input influences outputs. **Probably yes** for the dual framing ("what of me is you" as untrusted influence). Not verified. |
| Wolpert, Doya & Kawato 2003 | **abstract only.** PMC serves the full text only as a scanned PDF behind a browser proof-of-work check, which I did not try to get around; bicr.atr.jp and europepmc.org were not reachable from this session | The abstract treats motor commands acting on the body as communicative signals acting on others, with motor-control solutions extended to social interaction. From background knowledge, *not verified here*: MOSAIC forward–inverse pairs reused for observation, with responsibilities inferring the other's action, and a forward model of another's response to one's own actions. The latter is the precursor of S_j's "my model of how you respond to me". Nothing in the abstract suggests a counterfactual self or a bound. No verdict here rests on this paper. |
| Hannaford & Ryu 2002, time-domain passivity control (not cited) | not read; named from knowledge | A per-sample controller that keeps a running energy sum non-negative by injecting damping. Γ is a bank of such controllers (lagged, exponentially windowed) on p ↦ κp − r. Pointer only. |

### 5.2 Decision

**Does "partner influence defined by an online intervention on the agent's own body model, rather than a capped map" exist?** Yes.
- As a definition of influence computed online in one's own model: Jaques 2019 and Krakovna 2019.
- As a runtime enforcement that needs no route typing and holds for every program: SME (2010), whose low run *is* a counterfactual self with the high input set to a default.
- The exactness argument (own program, own noise) is the same one that makes SME sound and twin networks with shared noise exact.

**What is new.** A composition:
1. a multi-execution where the censored run is the agent's own generative body model under a neutral-partner intervention;
2. a declassification policy that releases the factual-minus-censored difference only inside a one-sided, per-channel sector at every exponential window and lag (a passivity or CBF-type running constraint);
3. used for affective mimicry.

I found no prior instance of 1+2. It is a primitive from security and control composed with a self-model, not a new primitive.

**Second clause** (new-mechanisms synthesis §3): "changes the signature… thereby removes a named failure, ideally by deleting a free scalar". The signature change, from "bound a map typed as partner input" to "difference of two executions", is SME's. The free quantity it removes (the completeness of route typing) is the one SME removed from static information-flow control. The design transfers that move into affect, correctly and usefully. Transfer of a known move does not meet the clause.

**Verdict: recombination.** The author's Self Other-Modeling and Yoshida & Man attributions stand. Add SME, Jaques, Krakovna, Chiappa and Buesing to §5. The design's own framing, "a safety filter on a known causal quantity", is the accurate one.

## 6. Verdict and what must change

**Not fit to put to the operator as a build candidate.** Known concrete failures remain from this angle. None of them is in Γ itself. In order:

1. **Give the core an expression producer that carries the agent's own state.**
   - Add an innate display prior to π_θ: an infant's repertoire tied to body variables and to valence events.
     - distress face and cry vocalisation on V rise and on E depletion;
     - relief smile on v > 0;
     - play face and laugh on P-relief events;
     - greeting smile on K fall;
     - startle; yawn and droop on low E.
   - Keep any learning on top of it blind to the partner's display, and keep the zero ceilings on the agent's *own* anger, disgust and contempt channels unless an own aversive load drives them (ledger critique 4, item 5).
   - This one change makes §8's relief-smile row true, gives S5 a stimulus, and is the precondition for item 2.
2. **Make reading through the own body non-empty.**
   - With item 1, I_θ learns own face latent ↔ own body state, so ι̂_j at a sad face becomes meaningful.
   - Recheck F4 (silently sad), and state ι̂_j's expected support (which body variables the own face shows).
   - Add the crossed-habits lesion (swap two own displays for a week and predict that ι̂_j's reading of those faces flips).
3. **Ground the word appraisal.**
   - L3 now leaves it with no teacher.
   - Proposal: train a word → partner-need reader on the factual other slot's ι̂_j. This is knowing, allowed by D81. Let its output enter only the care term: the agent's own need for j.
   - Expression then comes from the agent's own display (item 1) at its own drive change, not from j's face.
   - Hand the resulting word seam to the routes critic. It is the O3 seam, now with something in it.
4. **Fix curiosity.** Either make I a satiable *learning-progress deficit* (it rises when progress stalls, and is relieved by measured progress, with a fast online adapter so that progress can happen within a day), or drop the curiosity claim from §3.9. Add a curiosity bid to §3.6, and recheck the bored user.
5. **Keep fast mimicry (D81).**
   - Write S_j = S_0 + ΔS_j, clipped to [−κ, κ]. S_0 is the innate onset echo, kept for life. Its per-channel shrinkage weight must make weak evidence leave it in place.
   - Let ΔS_j carry the reciprocity and sign flips.
   - Use an instrument that people actually respond to: perceptible, aperiodic micro-displays at 0.5–2 s, at the lowest amplitude that is visible. Estimate on onsets.
   - Recheck scen A, including the onset mimicker.
6. **Close the Claude route through the transcript** (scen B). Either generate the twin's drafts from the twin's own transcript, or count the laundered tilt as a named, bounded route and size it. Generating them roughly doubles calls through the subscription; a cheaper variant is to regenerate only when the two selves' last utterances differ. Correct §3.7's claim and the bits figure (1.38 at N = 6).
7. **The greeting must see and know who.** Make K per identity (K_j). Gate the greeting display by ι̂_j and the partner's face at sight, attenuating only. Recheck the grieving reunion and the stranger.
8. **Laughter is not a threat.** Exempt rhythmic laughter from V's sharp-onset input. Add a cry vocalisation to the own repertoire (item 1), with κ = 0 toward the partner, so that sobs are not inverted to laughs.
9. **Specify:**
   - L5 imputation of partner *content* for K and P relief in rollouts, or state the acceptance to the operator;
   - that all policy and critic targets use L5;
   - the twin's persistence across sessions (W2; recommended: bounded nightly resync of slow modes, counted as a route);
   - the ELBO gradient routing versus L3 for B_θ's word input;
   - the spectrum of ξ, and that it is not applied to the vocal-laughter channel;
   - optionally, synergy-group clipping in Γ;
   - the six-fork call pattern, the CLI memory and the 1.5–3 s first word (D84).

**If items 1–9 are made and the routes critic finds nothing new,** the one line for the operator would be:

> *A conversational agent built on one learned model of its own body, used to act, to feel and to read you, with a parallel "counterfactual self" that sees your face and voice as neutral. Everything in the agent's face and voice that comes from your expression is the difference between the two, and a fixed per-channel limit keeps that difference from moving toward your expression beyond innate ceilings (smile about a third, sympathy brow about a sixth, anger, disgust and contempt zero), over every internal route at once, without listing routes. Its own expressions come from an innate infant repertoire tied to its own needs. Novelty: recombination (secure multi-execution from information-flow security, with a passivity/CBF-type declassification limit, applied to a self-model; Self Other-Modeling and Yoshida–Man for reading others). A first testbed, while the search for a new core continues.*

**Main risks to watch once built:**
- the word seam once item 3 fills it;
- twin divergence over months;
- whether IV reciprocity identifies anything in real people;
- the naturalness of a mosaic face where Γ binds;
- latency through the subscription.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full |
| research/questions.md | Report 5, Q19–Q23 in full; Report 4 |
| DECISIONS.md | D78–D84 |
| research/new-mechanisms-synthesis.md | in full |
| research/foundations/designs.md | in full |
| research/foundations/critique-4-design-cayley-ledger-agent.md | in full (scenario standard) |
| research/foundations/design-own-body-generative.md | in full, §0–§11 |
| research/foundations/sims/design-own-body/checks.py and out.txt | in full; Γ loaded verbatim by sims/critique-own-body-agent/scen.py |
| research/claude-code-agent-sdk-controls.md | effort, fork and parallel rows; conclusions |
| research/machine.md | hardware and budget rules |
| research/lanillos-2020-robot-self-other-distinction.md | the passages quoted in the design |
| Kusner et al. 2017, arXiv:1703.06856v3 | Lemma 1 and §4 |
| Nabi & Shpitser 2018, arXiv:1705.10378v4 | the constrained-inference proposal |
| Chiappa 2019, arXiv:1802.08139 | the PSCF construction (§3–4) |
| Ames et al. 2019, arXiv:1903.11199 | §I–II, CBF-QP |
| Raileanu et al. 2018, arXiv:1802.09640 | approach and the own-policy inference |
| Jaques et al. 2019, arXiv:1810.08647 | §4, the causal-influence definition |
| Krakovna et al. 2019, arXiv:1806.01186 | baselines (§2) |
| Buesing et al. 2019, arXiv:1811.06272 | §2–3, SCM counterfactuals with inferred noise |
| Algehed & Flanagan 2020, arXiv:2005.12345 | §I–II, Definition 6 (ME, after Devriese & Piessens 2010) and future work (declassification references) |
| Farquhar, Carey & Everitt 2022, arXiv:2204.10018 | §5, path-specific objectives with natural imputation |
| Wolpert, Doya & Kawato 2003, PMC1693134 | **abstract and reference list only**; see §5.1 for why |

**Not read, named only as pointers:** Devriese & Piessens 2010 in the original; Rafnsson & Sabelfeld 2016; Boloşteanu & Garg 2016; McCall, Bichhawat & Jia 2023 (abstract via search only); Hannaford & Ryu 2002. The novelty verdict rests on the SME definition as restated in Algehed & Flanagan, and on Jaques, Krakovna, Chiappa and Buesing, all read.

**To read Wolpert, Doya & Kawato in full,** one of the following must be allowed in this session's network settings: bicr.atr.jp (author PDF), europepmc.org, or royalsocietypublishing.org. pmc.ncbi.nlm.nih.gov serves its PDF only after a browser check.
