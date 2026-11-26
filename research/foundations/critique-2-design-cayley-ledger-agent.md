# Critique 2 of the Cayley–ledger core (revision 2): is it an emotional agent, principles, long-term goals, novelty

Independent critic, 2026-11-26T06:25:51Z

Critic of research/foundations/design-cayley-ledger.md, revision 2. I did not write the design. The standard is operator note Q19 (D80): proof gaps do not count, concrete failures do. Q20 is read on its recommended reading: the inner state may know the partner closely, and only expression is bounded. Another critic hunts copying routes. I report the one route I found in passing (§2.6) because it changes this design's expressive numbers, and leave the rest to that critic. Numbers marked "computed here" come from the design's own constants (first-order cascades, the disc formulas of §3.1–3.3).

## Summary verdict

- **What revision 2 fixes is real.**
  - The slow mind knows the partner (H2a), and the fast block learns from clean signals (H3).
  - Check B3 opens S4.
  - The placation route through partner predictions is cut.
  - Principle 3 now has a lesion with a specific, signed prediction (crossed habits).
  - Revision 1's two critiques are answered point by point.
- **But it is a muted agent by construction, and the reason is structural, not a tuning choice.**
  - The fix for H7 is an ℓ∞ small-gain bound on the slow block. That bound is a magnitude bound, and so it is sign-blind.
  - The held regime is therefore a ball, not a one-sided cone. Toward the partner, away from them or across channels, the partner's face can move any channel of the agent's held face by at most 0.15 of range, for any history of any length, with the words held fixed.
  - The one-sided limit Report 4 and Q20 described to the operator ("responding in the opposite direction stays free") is not delivered for anything held.
  - Every persistent affective variable the face can move (C, V, A, μ, slots) shares that cap, and so does the word-driven part of the same variable. Strong held faces come only from tiredness (E) and from a per-turn appraisal of the partner's current utterance.
- **Concrete failures I found** (each is derived from the design's own equations in §1–§3 below):
  1. **No positive affect.** 𝒟 ≥ 0 with a dead-band, and valence = −E[d𝒟/dt]. Good news, a long warm talk and a reunion leave J at 0, so the agent cannot be glad for you or with you. In those periods J has zero gradient for display, draft choice and fast-block learning.
  2. **The agent never speaks first.** The floor rule only allows a start after the partner's VAD offset, and drafts are made at the partner's turn end. A silently sad user is never addressed.
  3. **Claude cannot regulate the state.** By Check B2, Ω reaches S only through the zero-DC port, to the face. No route changes the body, the mood or the concern. §8.1.2's "a reappraisal changes the agent's body … durably" has no equation behind it.
  4. **Care has an incentive to copy (perceptual cancellation).** b̂_p is read from L(w) = L(v − s), the partner *minus the agent's own display*. J therefore rewards showing the partner's distress face, since doing so lowers perceived distress and C. Learning is driven to the in-phase edge of the slow disc, so matching at the cap becomes an attractor of learning (D78).
  5. **An uncounted mid-band route.** S_s's partner-dependent states enter S_f as the free context input c̃. That path is outside γ_f, and it contradicts "the 4 s – 1 min band is nearly blind".
  6. **Care tends to select against comforting.** The lexical-body and Π̃ readings map comforting acts to "the sender is in a high-C body". So f_recv learns that being comforted *raises* the drive, and the care term then disfavours comforting drafts. The design's own example (being smiled at in an argument raises V) is the opposite of what its equations give.
- **Novelty.** None of the three claimed composition results is new.
  - The empathic drive is Yoshida & Man (2025), D_self + w·D(dec_self(partner expression)), with a Farquhar–Carey–Everitt (2022) path-specific objective on top.
  - The banded wrap combines frequency-weighted gain bounds with the textbook fact that a positive system's ℓ∞ gain equals its DC gain.
  - N4 is the discontinuity of a discrete choice.
  - The author's own verdict is recombination, and I agree.
- **Fit to put to the operator as a build candidate under Q19: no.** Known concrete failures 1–6 remain. The list of changes is in §5. Even after them, it would go to the operator as a well-engineered *recombination* candidate, not as the new core mechanism the operator asked for.

## 1. Is it an emotional agent the operator would want to talk with? Five scenarios

Constants used:
- κ = 0.3, γ_f = 0.45, γ_s = 0.20;
- H_i and H_o with τ = 4 s, L with τ = 60 s;
- C with τ_C = 10 min, V with 10 min, A with 3 min;
- port ≤ 0.10, τ_Ω = 15 s;
- slow ℓ∞ cap 0.15·sup|Δu| on every output channel (§3.3).

"Range" means the channel's nominal [0, 1].

### 1.1 The user arrives silently sad

Take brow inner raise 0.5 and lip-corner depress 0.4, still and silent.
- **Face, 0–4 s.** The filters are initialised from the first frame (§2.2), so the arrival is not an onset. The fast block sees nothing and stays silent for as long as the user stays still (H_i removes DC). There is own micro-motion (d, sd 0.04).
- **Face, held.** Every output channel moves ≤ 0.15 × 0.5 = 0.075 (ℓ∞ cap, any direction), and ≤ 0.05 in phase at steady state.
- **Concern C.** C rises through the L → C cascade. Computed here: 4% of its final value at 1 min, 11% at 2 min, 33% at 5 min, 59% at 10 min. §3.11's "C rises within 1–2 min" is wrong by a factor of about 5. Either way, C's display is inside the 0.075 cap.
- **Voice and words.** None. The floor rule (§2.1, R13) lets the agent start only ≥ 200 ms after a partner VAD offset, and drafting starts at the partner's turn-end pulse (§6.4). No partner speech means no agent turn, so Claude is never called.
- **Net.** A near-neutral face with trace concern, in silence, for as long as the user is silent.
- **Verdict.** Revision 1's critic found that a silent sad user is never noticed. Revision 2 notices (in 𝒦 and C) but cannot say so, and shows it at trace intensity. The scenario still fails, now on initiation.

### 1.2 The user tells good news, laughing

Smile 0.8, cheek 0.6, jaw open, loud voiced bursts, then "I got the job!".
- **Face, fast.**
  - The echo at 0.45 s on lip corner and cheek is ≤ 0.186 × 0.8 ≈ 0.15 in phase, and decays with τ = 4 s.
  - The burst channels echo ≤ 0.15, so the agent's own laugh is a faint, brief flicker.
  - Cross-channel transients of up to about 0.5 are allowed (W2), but nothing in θ₀ or J asks for them.
- **Body.**
  - A rises with loudness and motion.
  - V rises if the slow loudness mean crosses V's innate level (§2.5.2: "loud audio … above an innate level"). Loud laughter is therefore aversive to this agent.
  - C ≈ 0: a happy partner is inferred near set point (§3.11.2).
  - 𝒟 is unchanged, or rises through A and V.
- **Valence.** −E[d𝒟/dt] ≤ 0. There is no route to a positive value except relief of a prior deficit. 𝒟 ≥ 0 with a dead-band (§2.11), so the best state is "nothing wrong".
- **Words.** All six drafts score equally on J: the care term is 0, and the own body is unchanged by drafts with the partner held exogenous. The choice is then argmax of Gumbel noise at T = 0.1, which is uniform among the six. Claude writes "Congratulations!" because Claude does. The engine contributes nothing.
- **Word-driven face.** The latched utterance → Π appraisal (R14, "up to 0.8") has no innate prior for good news (Π₀ only has distress, relief-of-𝒟 and low E). It also has no J gradient, because good news changes no term of J. It stays near zero. If V rose, the face shows a slight distress configuration.
- **Net.** A brief faint smile, then near-neutral, possibly a slight frown at the noise, and warm words chosen at random.
- **Verdict.** Shared joy (capitalisation) is impossible by the form of 𝒟. This is the clearest single failure as an agent to talk with.

### 1.3 The user gets angry at the agent

A glare, a raised voice, "You're useless."
- **Face, fast.**
  - Startle (brow raise, lid raise) at each audio onset through κ_a: ≤ 2√(κ_aκ)·γ/(1 − γ) ≈ 0.24 per pair, decaying in 4 s.
  - Context-set counter-responses are allowed up to −0.49.
- **Body.** V rises: the aversive part of b̂_p times gaze-at-agent, plus loudness. A rises. 𝒟 rises, and Π₀ shows a distress configuration. All of this is partner-driven, so it is ≤ 0.15 per channel held. V decays over about 10–20 min after the anger stops: a hurt that lasts, at trace intensity.
- **Words.** The care term is large, because b̂_p has high V and A. Drafts with high self-simulated relief R_i are chosen. By §2.6 below, what relieved this agent's V in its own life is the partner becoming non-hostile and quieter, so calm, non-hostile drafts are favoured. That is plausible.
- **Net.** The most human of the five scenarios: a flinch, calm words and a lingering low mood. But the lingering mood is nearly invisible.

### 1.4 A long, warm conversation (2 h)

- **J ≡ 0 for the first ~40 min.**
  - E falls 0.5 %/min and leaves its dead-band at 0.5 after 40 min (computed here).
  - A stays in its band if the talk is lively. If the talk is calm, A falls below 0.15 and 𝒟 > 0.
  - Through b̂_p, a calm, content partner may then *raise C*: the agent's drive evaluated at a low-arousal body is positive.
  - Whether contentment reads as distress depends on where Π̃ places calm faces relative to A's band [0.15, 0.45]. The design gives no argument.
- **Face.**
  - Fast flickers at each smile onset, ≤ 0.15, thinned by habituation H.
  - Slow held warmth ≤ 0.10 in phase.
  - After 40 min, a growing fatigue display ("lowered tone with low E", uncapped because E is partner-independent).
- **Words.** Uniform random among six drafts until E- or A-driven terms appear. Neither is affected by drafts, except perhaps ending the session (§3.4).
- **Learning.** J has zero gradient, so Π, S_f's θ and the scorer learn nothing from the warm part of the evening.
- **Net.** The emotional arc of a warm evening is neutral, then tired. The warmth is Claude's text.

### 1.5 The user returns after a week

- **What persists.**
  - E is restored.
  - Mood: only the 73-h mode keeps something, e^{−168/73} ≈ 10%.
  - Slots keep e^{−7/30} ≈ 79%.
  - Retrieval reaches week-old snippets with an ALiBi bias of −1.
- **No need was unmet during the absence.** There is no affiliation or contact variable (Yoshida & Man's own S1 hook in the project note uses a "contact deficit"), so reunion relieves nothing: valence 0, no gladness.
- **The agent waits for the user to speak** (§1.1).
- **The face for this user versus a stranger saying the same words.** The difference comes from partner-history-dependent slot and μ contents, so by the ℓ∞ bound it is ≤ 0.15 per channel. The identity token can drive Π through c̃, but nothing teaches it a greeting.
- **Net.** Verbally a friend who remembers what you said last week. Facially a polite stranger.

### 1.6 Expressive and alive, or muted? Does its own state drive the face?

**The structural reason it is muted.** For any internal variable z of S_s, let k_z be its sensitivity to the partner's face and g_z its display gain. The slow certificate needs roughly Σ g_z k_z ≲ γ_s. So:
- a variable that *notices* the face (k_z large) can only show weakly;
- this applies to the same variable when words or own processes move it.

C mixes face and words (fixed weights 0.6 and 0.4). Its full word-driven display is therefore ≤ about (0.4/0.6) × the face cap, roughly 0.1 of range. Mood μ is written from m(b, x) and b's partner-driven parts, so it has the same cap. The ℓ∞ statement (§3.3) makes this exact for the face part: holding words fixed, *any two partner histories of any length* give held faces that differ by ≤ 0.15·sup|Δu| on every channel. A month with a sad partner and a month with a cheerful one differ by at most that.

**What is left that is strong:**
- fast transients at partner *changes* (≤ 0.19 toward, ≤ 0.49 away, about 4 s);
- the per-turn appraisal of the partner's current utterance;
- visemes;
- fatigue.

Claude's own contribution is ≤ 0.10 for about 15 s.

**Its own persistent state does not drive the face strongly or richly.** The 128-d mood and 8k-d slot memory are rich in capacity but reach the face through a 0.15 ball, and 0.15 of a blendshape is around FACS trace intensity. So the brief's "expressions come from an internal state that persists across turns and days" is met only at trace intensity, except for tiredness.

**Why the ball is two-sided.** The disc of a γ-contraction has in-phase 2κγ/(1 + γ) and anti −2κγ/(1 − γ). That is strongly asymmetric only as γ → 1:
- γ = 0.2 gives 0.10 / −0.15;
- γ = 0.6 gives 0.225 / −0.90 (computed here).

The ℓ∞ cap 2κγ/(1 − γ) is direction-blind. So the H7 fix capped the opposite side at the same 0.15. The design solved late-window copying with the same sign-blind tool (a magnitude bound) that the project rejected for DP in revision 1. This is the novelty critic's missing object: a *directional* certificate for persistent state.

## 2. Principles, concretely

### 2.1 Principle 1: clean

No classifier anywhere. Laughter, sighs and crying enter as continuous burst energies. ASR interjection tags are stripped.

### 2.2 Principle 2: three strains, one double count

- **C ("concern load") and V ("aversive load") are not body variables.**
  - They are evaluative social constructs, given innate set points, dead-bands, weights and time constants.
  - C = lowpass 𝒟(b̂_p) is hand-wired empathic distress. V is hand-wired "being the target of someone's aversive state".
  - The brief's innate set is "body variables to regulate and a few reflexes". These are defensible as innate drive *couplings* (Yoshida & Man), but not as body variables with their own set points.
- **A ("arousal load") is an innately set arousal.** The design also reads arousal out as E‖ḃ‖, so there are two arousals, one of them set. That brushes Principle 2's "valence or arousal are read out, not set". It is acceptable only if A is restated as a physiological load (sympathetic tone), with no affective name.
- **Π₀'s "distress configuration" and "relief configuration" are named prototype expressions.** They are allowed as newborn reflexes (cry face, relief). They are acceptable, but they are the only innate expressions, and that is part of why positive faces never form (§1.2).
- **Double count, with a recursion.**
  - Concern enters twice: as C inside 𝒟(b) (weight 0.8), and as the care term w_C(𝒟(b̂_p) − R)₊ in J.
  - Because C is a coordinate of b, the partner's inferred body b̂_p has a C coordinate too. 𝒟(b̂_p) therefore includes "the partner's concern".
  - The agent becomes concerned at the partner's concern, so a worried partner raises C just as a sad one does. This feeds §2.6's comfort-reversal.

### 2.3 Principle 3: now essential, with two weaknesses

- **Essential.** The crossed-habits lesion (§3.12) predicts a specific, signed behaviour: the partner's smiles raise C. It follows from b̂_p = Π̃(R·x) feeding the fixed 𝒟. The rotation argument of critique 1b no longer applies. Pass.
- **Π̃'s training support does not cover the partner's faces.** Π̃ inverts Π on the agent's own (b, command) pairs. But Π's body-driven display gain is capped (≈ 0.15 of range at most), while the partner shows 0.4–1.0.
  - A true inverse would need gain ≈ 1/g_b ≈ 7, and Π̃ is normalised inside the slow budget.
  - So either b̂_p is compressed by about g_b, which pushes it into 𝒟's dead-bands and makes C ≈ 0 from faces, or Π̃ extrapolates 3–7× outside its data.
  - The muting of §1.6 directly degrades reading-through-own-body: the less the agent's face says about its body, the worse it can read yours. The design should state the gain allocation along R → Π̃ → 𝒟 → C → Π. It does not, and §3.15.6 only "checks at load".
- **Mimicry → affect.** Mimicry still does not produce affect. There is no facial feedback: Check B3 allows own-face observation only for fitting 𝓔. Principle 3's "drive the agent's own … affect pathways" therefore holds only through b̂_p, which is inference, not feedback. Acceptable, but say so.

### 2.4 Principle 4: compliant in letter, with a gray channel and a missing function

- **Compliant.** The prompt is constant, plus the transcript, plus ≤ 3 raw snippets. No numbers or labels. State acts only by choosing drafts and snippets. Pass.
- **A gray channel.** PMI-weighted retrieval deliberately selects snippets rich in tokens that co-occurred with the current category ("worried"). That is a learned category rendered as words in the prompt: close to a state label, carried by real past text. It is defensible as the grounding route, but the design should say it is a label channel of about log₂(64) bits per turn.
- **Naming inherits the user's vocabulary.** PMI counts tokens "said by either party". So the agent's own category gets named with the *user's* emotion words: the user said "exhausted" while the agent was in k. Self-report then partly copies the user's state words.
- **Missing function: regulation.** Principle 4 says Claude "names, reinterprets and **regulates** states". By Check B2 nothing from Ω enters S except through P_Ω, which writes only to s (the face) and is zero-DC. The agent's own utterances are removed from the microphone (AEC), so they do not enter c_lex either. A reappraisal therefore cannot change C, V, A, μ or slots. The care term's relief R is a *scoring* quantity: choosing a high-R draft lowers J's integrand without changing any state. This is a concrete failure of Principle 4 and of affective science's regulation element. §8.1.2's sentence "a reappraisal changes the agent's body and words durably" is false by Check B2.

### 2.5 Principle 5

Ablations are stated, and most follow from the equations. Wrong ones:
- §3.11's "C within 1–2 min" (≈ 10 min, §1.1).
- §3.5's argument example (§2.6 below). The C4/C5 sign learning therefore has no worked example that the equations support.

### 2.6 Principle 6: care, checked for hidden incentives

1. **Action-blind partner head.** It removes the planned path from act → partner → J. Pass, as far as the partner head goes.
2. **Perceptual cancellation: an incentive to copy.** §2.5.1 defines p̂ = R·x with x = L(w) and w = v − s. The perceived partner is the partner *minus the agent's own display*.
   - In steady state, perceived = v/(1 + σ) for slow DC gain σ. Computed here: at σ = +0.2 (the in-phase edge) perceived distress is 0.83v, and with 𝒟 quadratic outside the dead-band C falls by about 30%. At σ = −0.2 it is 1.25v, and C rises by about 56%.
   - Π is trained to minimise J through 𝓜 rollouts, with the partner exogenous but the agent's own S simulated. Even a learned own-body head would learn this, because inside the agent it is a true causal effect. Showing the partner's distress lowers J, so learning drives Π to the in-phase edge of the slow disc for every negative partner state.
   - The cone keeps this at 0.10 held. But D78 requires that copying never be "a state the agent settles into", and here maximal permitted matching is the attractor of learning.
   - It is also a care pathology: the agent soothes its concern by mirroring, not by acting.
3. **Comfort reversal (from the equations, strength untested).** The lexical-body head reads an utterance as "the own body in which the agent itself produced such utterances". The agent produces comforting and apologetic utterances when C or V is high, because that is when care selects them. So:
   - comfort received from the partner reads as a sender with high C or V;
   - through 𝒟(b̂_p) and V's input, receiving comfort raises the agent's C or V;
   - f_recv learns from this that being comforted raises the drive, unless co-occurring calming outweighs it;
   - R_i for comforting drafts is then low or negative, so care disfavours comfort.

   The same holds for faces through Π̃: the agent's concerned face is its high-C face. The design's own example, "being smiled back at in an argument raised its own V, so it learns not to smile back", contradicts its equations. V reads the aversive part of b̂_p, and Π̃(smile) is a relief body, so being smiled at lowers V.
4. **The own-body head is not masked.** If unobserved mediators exist (for example the partner's next-turn content arriving within a rollout step), the act → partner → own V path leaks back in. F4 covers this. It is a risk, not a demonstrated failure.
5. **Fatigue and ending conversations.** E has a flat awake cost and is restored only at rest. After about 40 min, the only act that lowers 𝒟(E) is one that leads to rest. If 𝓜 learns that closing remarks precede rest, the scorer acquires a small, signed incentive to end conversations. That incentive is on the user's time: the mirror image of an engagement reward. The design should state what "rest" is and check this.
6. **No engagement or flattery reward.** None found. Pass.

### 2.7 Principle 7

Stated plainly (§5): the transcript and snippets go to the API. That is an operator decision. Pass.

### 2.8 Principle 10: closer to one core, still wiring

- **Closer.** One model (𝓜) and one objective (J) train Π, S_f, the retrieval query and the scorer. That is the Dreamer pattern, and an honest assembly list is given.
- **Still wiring.** The *emotional content* is hand-wired innate dynamics, not consequences of J:
  - what moves V (others' aversive state × gaze, loudness);
  - what moves A (loudness, motion, lexical surprise);
  - C's formula;
  - Π₀.

  Principle 10 allows innate constraints. But in this design the constraints carry the emotion, and the core equations carry only the choice among drafts and displays. In content periods (J ≡ 0) the core does nothing. I rate it one objective plus a hand-wired affective body, not yet one core from which homeostasis, valence, mimicry and regulation follow. Regulation in particular does not follow (§2.4).

### 2.9 One uncounted route found in passing (for the route critic)

- **The route.** §2.4: 𝓡_θ takes c̃ as a *free* input. "S_f is a γ_f-contraction … for every fixed (a, c, d)". But c̃ contains S_s's slow states (body, mood summary, attended slot), and those depend on the partner through L(w). The path partner → L → S_s states → c̃ → S_f → H_o → y is therefore not inside γ_f, and the sum bound of §2.3 treats c̃ as fixed.
- **Size (computed here).** For a step in the partner's held face, H_o of a 60-s ramp in c̃ gives a peak of 0.055 × g and a 1-min mean of 0.040 × g. Here g is S_f's free gain from c̃ to output, which nothing bounds. With g = 5 that is about 0.2–0.27 for a minute, in any direction including in phase. A partner who changes expression every minute or two is followed in the mid band.
- **What it does to the design's claims.** Held DC is still zero (H_o), so Claim K survives. But "the 4 s – 1 min band is nearly blind on the expressive side" (§8.1.1) is false as written, and H8's 1-min totals do not count this route.
- **The fix.** Bound S_f's Lipschitz constant in c̃'s partner-dependent part and count it in the fast budget, or pass only partner-independent context to S_f. Either fix makes the agent *more* muted.

## 3. The brief's long-term goals

| Goal | Status in revision 2 |
|---|---|
| Learns emotions, manner of speaking and expressions by living, from an innate body and reflexes | **Weak.** Learning has a signal only when 𝒟 > 0 or the partner is inferred distressed. In contentment, J ≡ 0 gives zero gradient to Π, S_f and the scorer (§1.4). "Manner of speaking" is selection among six Claude drafts, uniform at J = 0, plus prosody targets capped by the wrap. No positive expression can be learned, because no J term rewards one. |
| A face like a human face, driven from inside | **Partly.** There are 32 AU-level channels, a muscle filter, and S4 is reachable (B3). "Driven from inside" holds only for fatigue and per-turn word appraisal at strength. Persistent inner state shows at ≤ 0.15 (§1.6). |
| Two-way contagion; the operator's face follows the AI's (S5) | **At risk.** The AI's strong displays are visemes, fast responses to the operator's own changes, and appraisals of the operator's own words. All are partner-caused, so "the AI's emotional pathway" that S5 would ablate is mostly the operator's own input reflected. The AI's own-state displays are trace-level, and 0.10–0.15 of a blendshape is near the webcam AU noise floor. Measuring S5 would need facial EMG (Q5). Sub-threshold expressions can still evoke EMG mimicry (Dimberg et al. 2000), so S5 is not ruled out, but it is not designed for. |
| Temperament and relationship over months (S6) | **Verbal yes, facial weak.** Slots (30 days), consolidation (λ_n) and θ-pulls give a mechanism. Robustness to Claude upgrades is good, because the state lives in the engine. But relationship-specific *faces* are capped at 0.15 (§1.5), and there is no attachment or affiliation variable, so the relationship has no affect of its own. |
| Interoception | Present: 𝓜 predicts the own body, and I is own-forecast uncertainty. The body is six abstract loads, two of them social constructs (§2.2). |
| Appraisal | Partial: a learned utterance → display map and b̂_p^{lex}. There is no appraisal of relevance to positive goals. |
| Valence and arousal as readouts | Valence is a readout but **one-signed in practice**: non-positive except during relief. Arousal is read out *and* set (A). |
| Regulation | **Absent** (§2.4): Claude cannot change state. Choosing drafts lowers a scoring term, not a feeling. |
| Concepts named by Claude | Present in form (DP-means categories plus PMI retrieval). The names partly copy the user's words (§2.4). |
| Positive social emotion (shared joy, warmth, gladness at reunion) | **Absent** (§1.2, §1.4, §1.5). Not on the brief's explicit list, but it is the bulk of "talk with an AI the way one talks with a person". |

## 4. Novelty: the three claimed composition results

1. **The split-band wrap with its two rules (no demodulation; ℓ∞ slow block).** Known parts.
   - The full-band sector is the robust REN (Revay et al.; accepted by the author).
   - The frequency split is frequency-weighted gain bounding: complementary filters with |H_i|² + |L|² ≤ 1 and a separate gain per band.
   - The ℓ∞ part uses the standard fact that for positive linear systems the ℓ∞-induced gain equals the DC gain, plus ℓ∞ small gain (positive-systems literature, e.g. Briat 2013, Rantzer; peak-to-peak ℓ₁ control, Dahleh & Pearson). I know these as standard and did not re-read them here.
   - The no-demodulation rule is the elementary fact that a nonlinearity moves energy from high to low frequency (rectification), so a DC bound needs the high-pass *after* the last nonlinearity.
   - The design's contribution is applying these to the copy problem, and H5 and H7 are useful necessity checks. As a computation it fails clause 1.
   - The composition also leaks (§2.9) and is two-sided (§1.6), so it does not deliver a new invariant either. **Refuted as new.**
2. **N4: discrete choices need their own port.** Elementary.
   - An argmax over a continuously varying score is discontinuous.
   - Randomising it gives continuity in total variation, not Lipschitz continuity of the output, and the W₂ ≥ √TV·d coupling bound is one line. The same reasoning is why randomised smoothing and the exponential mechanism are analysed in probability, not in output space.
   - The "port" is then a bounded additive input with a DC blocker.
   - Useful bookkeeping for this project. **Not a new result.**
3. **Care with no incentive on the partner.** A direct composition of two published mechanisms.
   - **Yoshida & Man (2025):** D = D_self + w·D_partner, with the partner's state inferred by running the agent's *own* self-trained decoder on the partner's expression. Read through the project note research/yoshida-man-homeostatic-coupling.md, which records both papers as read in full. This is exactly C = 𝒟(b̂_p) with b̂_p = Π̃(R·x).
   - **Farquhar, Carey & Everitt (AAAI 2022), path-specific objectives:** optimise only the causal effect of actions not mediated by a "delicate" state, so the agent has no incentive to control it. Everitt et al. 2021's "latent variable outside the agent's influence" is the same rule; project note research/everitt-2021-reward-tampering.md. The action-blind partner head is that rule with the partner's state as the delicate node.
   - f_recv, "how I would be relieved by receiving this", is simulation-theory empathy. A pointer is Bussmann, Heinerman & Lehman 2019, "Towards empathic deep Q-learning", which I did not read.
   - **Refuted as new.**
   - **A substantive point the design misses.** Yoshida & Man found prosocial behaviour emerged *only* when the agent's drive was coupled to the partner's actual state, so that helping changed the reward. Observation alone ("cognitive empathy") did not produce it. The action-blind design removes exactly that coupling-to-consequences and replaces it with f_recv. The only evidence read therefore predicts that this care will *not* learn to help, unless f_recv carries it, and §2.6.3 suggests f_recv learns the wrong sign for comfort.

**Overall.** Recombination on both clauses, as the author says. The operator asked for a genuinely new core mechanism. This is not one.

## 5. Verdict and what must change

**Not fit to put to the operator as a build candidate under Q19.** Known concrete failures remain. In order of importance:

1. **Positive affect.** Give 𝒟 or J a satiable term that good social events relieve, so shared joy, warmth and reunion exist. Then show that it is not a reward on smiles, attention or time (Principle 6).
   - *Option:* a satiable affiliation or contact need relieved by the agent's own acts of sharing and by exchange of turns, capped, with the partner's face as evidence only.
   - *Option:* care that is also relieved by b̂_p moving *above* rest (gladness for the partner), with the action-blind rule kept.
   - Without this, J ≡ 0 in contentment and nothing learns there (§1.2, §1.4, §3).
2. **Agent-initiated turns.** Let C and I (and silence duration) open a turn when the partner is silent. Count the route: initiation timing is a function of the partner's face through C.
3. **Regulation by Claude.** Give Ω a certified route into state, for example Ω-scheduled leak rates or gains of S_s's positive filters, which stay γ_s-contractive for every schedule in ℓ∞. Or concede that regulation is absent and remove "regulates" from the claims. N4 makes this a real tension: state how a durable verbal reappraisal coexists with a zero held port.
4. **Perceptual cancellation.** Compute b̂_p from the reconstructed L(v) = L(w) + L(s), or stop the gradient through the agent's own display in J. Re-certify the slow block, then show that learning no longer drifts to the in-phase edge (§2.6.2).
5. **The c̃ → S_f route.** Bound it and count it (§2.9).
6. **Muting, decided openly with the operator.** State plainly that the held regime is a 0.15 ball in every direction (§1.6), not the one-sided limit Report 4 and Q20 described. Then either:
   - (a) separate word-only and own-body-only state variables from face-driven ones, so the first two can show strongly, and restate C as two variables; or
   - (b) find a directional certificate for persistent state, so the anti and cross sides can be large while in-phase stays ≤ 0.10. This is the open new-primitive problem, and with it the design could become new.

   Put the trade-off to the operator in the words "your face can change its lasting expression by at most a seventh of range, in any direction".
7. **Comfort reversal.** Stop the lexical-body and Π̃ readings from turning received comfort into "sender distressed": exclude C from b̂_p, or train f_recv only on V, A and E. Fix §3.5's example, and give one worked context in which the learned fast sign really flips (§2.6.3).
8. **Π̃'s gain allocation.** State it along R → Π̃ → 𝒟 → C → Π, and show C is not stuck in the dead-band (§2.3).
9. **Small corrections.**
   - C's onset time (§1.1).
   - Restate A without an affective name.
   - Remove the double count of concern.
   - Define "rest" and check the end-the-conversation incentive (§2.6.5).
   - Declare PMI retrieval as a label channel with its bit rate.

**If all of this were done,** the operator would be choosing:
- a copy-proof, knowing agent whose lasting feelings show mostly in its words and memory;
- whose face reacts vividly only at moments of change and to what was just said;
- built from known parts (robust REN, frequency-split gain bounds, positive-system ℓ∞ bounds, Dreamer-style world model and actor, Yoshida–Man coupling with a path-specific objective).

That is a sound recombination candidate, and a good baseline. It is not the new core mechanism the brief asks for.

## Sources read

| Source | How read |
|---|---|
| brief.md | in full |
| research/questions.md | Q16, Q19 and Q20 in full; Report 4, Q9, Q17 and Q18 with the answer |
| DECISIONS.md D80 | in full |
| research/foundations/designs.md | in full |
| research/foundations/critique-design-cayley-ledger-novelty.md (revision 1 novelty critique) | in full |
| research/foundations/design-cayley-ledger.md (revision 2) | in full, §0–§10 and the revision history |
| research/foundations/sims/design-g2/out.txt | in full (checks.py not re-run) |
| research/yoshida-man-homeostatic-coupling.md (project note on arXiv 2412.12103 and 2506.12894, read in full by its author) | in full. The originals could not be fetched: arxiv.org and ar5iv are not allowed in this session's network |
| research/everitt-2021-reward-tampering.md (project note) | first sections, through the design-principle claims |
| Farquhar, Carey & Everitt, *Path-Specific Objectives for Safer Agent Incentives*, AAAI 2022 (arXiv 2204.10018) | abstract and summary only, through web search; the claim used (no incentive to control a delicate state) is the paper's headline statement |

**Not read, named only as pointers:**
- Briat 2013 and Rantzer on positive systems' ℓ∞ and L1 gains;
- Dahleh & Pearson on ℓ₁ control;
- Bussmann, Heinerman & Lehman 2019 (empathic DQN);
- Dimberg, Thunberg & Elmehed 2000 (unconscious facial reactions).

No verdict depends on them alone. Each conclusion in §1–§3 is derived from the design's own equations and constants.
