# Critique 3 of the Cayley–ledger core (revision 3): typing, the one-sided cone, the Ω ports, care and initiative

Independent critic, 2026-11-26T07:34:13Z. I did not write the design.

**Standard.** Written under questions.md Q19 and DECISIONS.md D78 and D80, on Q20's recommended reading: the inner state may know the partner closely, and only expression is bounded. Proof gaps are not reported. Each finding is a concrete scenario with numbers.

**Read in full:**
- brief.md;
- questions.md: Report 5, Q18 with its answer, Q19, Q20, Q21;
- DECISIONS.md D78, D80;
- both revision-2 critiques: the routes critique (K1–K5) and the agent critique (§1);
- design-cayley-ledger.md, revision 3;
- sims/design-g3/checks.py (G2 and G5 in full, the rest skimmed) and its out.txt;
- these source notes, for the evidence used here: bailenson-yee-2005, hale-hamilton-2016, levitan-2011-2012 and scherer-2003.

**Checks.** They are in `research/foundations/sims/critique-cayley3-routes/checks.py`, sections C0–C7. Run `python3 -I checks.py` (numpy, scipy, about 20 s). The output is in `out.txt`.
- They use the design's own constants: τ_m, b_m, N_m, a_m, r_m, K's equation, the display gains, the G5 rollout and the punctuation rule.
- Every cone basis used is tested for membership in 𝒢_m before use.
- They test the design's claims on constructed partners. They are not evidence about people. Where a result depends on a property of real partners, that property is stated as an assumption.

## Summary

Revision 3 closes K1, K1b, K2, K4 and K5 as specified, and the one-sided cone does what Claim O says for a fixed context and a single partner direction. I reproduce the design's two caveat numbers (C0):
- the word seam: pooled slope +0.554;
- the co-moving pair: +0.586, against the design's 0.609.

Four concrete failures remain, two of them in the place the author called weakest. Ranked by severity:

1. **Severe (D78 disqualifier). T state carries the partner's conversational tempo, and one cone-mixing weight gates the whole face on it.**
   - **The leak.** The design's own contact deficit K is T-typed. It rises on the wall clock and falls per exchange, so K\* ∝ 1/exchange rate (G4d). It is an exact code of how fast the partner answers and speaks: −log K correlates with the partner's held state at r = 0.96, and with his response latency at r = −0.95.
   - **The route.** K is in c̃ = z, so α(z) may read it. One weight k on it mixes two valid bases, in-phase (b_m) and away (−N_m).
   - **The result.** That weight takes the agent from flat to tracking the partner, on every channel at once. With k from 0 to 30, the pooled 1-min slopes go:
     - for the cone output y_F alone: LP −0.48 → +0.39, BI → +0.54, EN → +0.95, FR → +0.73;
     - for the rendered face after sat: LP −0.01 → +0.27, EN → +0.49, FR → +0.27.

     The design claims ≤ 0.15. No words are involved, so this is not the definitional seam.
   - **Free display.** The same T code drives the free display's own latency and rate with one uncapped weight (r = 0.95 with the partner's latency).
   - **Other carriers of timing in c̃.** "Own floor state" (Ω, set by VAD-timed onsets and F-triggered bids), v_T and P carry timing too.
   - **The word seam is wider than stated.** It is (b·x_hi + N·x_lo)/(x_hi − x_lo). For held smile levels 0.3/0.7 that is 1.23, and for 0.35/0.75 it is 1.41, not 0.56.
2. **High (D78). Natural face–voice co-movement plus output saturation: one valid basis gives visible held copy on four channels.**
   - **The basis.** It pairs each visible channel with a co-moving channel that is silent at rest: LP ← burst energy, jaw ← burst rhythm, F0 range ← breathiness, energy ← lid tighten. The skew partners carry the minus signs.
   - **Validity.** It is valid in every 𝒢_m, and no listed synergist pair is used.
   - **What the cone bound sees.** Along the partner's own co-movement direction, eᵀy_F has slope 0.056 ≤ b, as Claim O says.
   - **What is rendered.** sat clips the "payment" on the silent channels to zero. Rendered held slopes: LP +0.34, jaw +0.37, F0 range +0.28, energy +0.26, against the claim of ≤ 0.15.
   - **Why the design's caveat misses it.** G2d calls co-movement across non-synergist pairs "unnatural". It is the normal case for laughter and animated speech, because the mask lists face synergies, not face–voice ones.
3. **High, conditional on how partners respond (D78: copy must not attract). The need path makes copy an attractor of the design's own learning.**
   - **The dilemma.** In rollouts, the display reaches J only through act → N.
     - Either the cone, α and Π_o get no J gradient at all, and "set by the learned relationship" is empty.
     - Or they are credited for whatever display lowers the partner's reported need, and that includes being mimicked, if mimicry helps. The evidence is mixed: Bailenson & Yee η² = .21; Levitan's entrainment goes with "giving encouragement"; Hale & Hamilton's pre-registered study is null.
   - **What learning does.** With any positive effect, the gradient points toward the copy corner everywhere in 𝒢, and only the soft θ₀ pull brakes it. Over 200 nights, concordance goes from +0.02 to +0.07, +0.14 and +0.24 at ε/λ = 1, 3 and 10, against a cap of 0.49 for this partner (C3).
   - **With failure 1.** Learning would then also have a reason to build the tempo dial.
4. **Medium (Principle 6). The prompted-reply guard is lexical. P(flatter) = 0.50 is a property of the check, not of learning.**
   - **The bypass.** The guard ignores only replies of ≤ 6 tokens after an agent question that contains "you". These elicit an "I'm fine"-type reply that is credited as an unprompted need report:
     - "feeling better now" → "yeah feeling better" (by the innate rule it is not even a question);
     - "better now";
     - "you seem a lot calmer now";
     - "I bet that's a weight off".

     At G5's scale, P(choose the eliciting draft) = 1.000 (C4).
   - **Flattery.** G5's flattering draft has a need effect of zero by assumption (dN = 0). A compliment that earns an unprompted "aw, that made my day" is credited exactly like help.

**Lower:**
- **5. Low–medium (F5, the smile clamp; an Ω → T route outside the two ports).**
  - **The route.** P's own-contribution clause reads the agent's own utterance (Ω), and draft choice depends on 𝓜, which knows the partner's face. So the partner's smile → play draft → P relief → the uncapped relief display.
  - **Size.** With words fixed and the partner's smile going from 0 to 0.8: at G5's scale, P(play draft) goes 0.52 → 0.58. With a scorer ten times sharper, P(play) goes 0.69 → 0.96, the own laugh 0.19 → 0.27 and LP 0.24 → 0.33. It satiates with P (C6).
  - **A related leak.** The free display's "turn reflexes" row fires at the partner's VAD offsets, which are F. In a laugh with gaps, that gives the agent a lagged burst echo, slope +0.28 at 1.1 s, outside the fast wrap (C7).
- **6. Low (accuracy).** The dyad's stability holds only for a mimicking partner (μ > 0). A counter-mimicking partner with μ ≤ −0.8 destabilises the away side: the pole goes from +0.002 to +0.38 per τ₀ (C5). The mode is anti-phase and is clipped by sat, so it is not copy, but §3.3 item 4 as stated is false.

**No concrete failure found:**
- the fast wrap, the bias-free gates and the phrase-target split;
- ASR words: laughter tokens are stripped by the innate interjection list (kept from revision 2);
- identity memory, apart from the ≤ 0.10·Δf_id tail of failure 5;
- nightly replay mixing types, beyond failure 3;
- Claude's text into held copy, beyond failure 1's "own floor state" and failure 5;
- the concern-bid timing as a dial;
- K and P relieved by smiles directly;
- "two sign flips in series" inside the cone: it is linear, and the quadratic form is exact. The way skew composes into copy is failure 2, not a series of flips.

---

## 1. Tempo in T state: one α weight runs the face toward the partner (severe)

**Mechanism, from the design's text.**
- **Check T.** It types the turn sequence as T "as events (who spoke, in what order; never durations)". Every T load still evolves on the wall clock between events.
  - K: rise (1 − K)/τ_K, τ_K = 36 h, and K ← K(1 − 0.25 f_id) per completed exchange.
  - P: rise over 5 h, and a step per play exchange.
  - A_L and V_L: decay between latches.
  - C_L: 40-s tracking.
  - v_T: a time derivative.
- **What the design's own G4d shows.** K\* = 0.0021, 0.0010, 0.0005, 0.0003 at 1, 2, 4 and 6 exchanges per minute. That makes K an exact readout of the exchange rate. The exchange rate is set by the partner's response latency and speaking rate (F channels LAT, RT and pause).
- **Where it goes.**
  - c̃ = z contains "E, K, P, C_L, V_L, A_L, v_T" and "own floor state" (§2.4). The context encoder is a learned MLP, so any monotone function of K is available.
  - α(z) mixes 16 valid bases of every trace for all 32 channels.
  - The free display Π_o reads the same T loads, with no partner cap.
- **Why Claim O does not cover it.** Claim O item 2 assumes "z independent of the partner's face given words". With K in z, that is false without any words at all.

**Scenario.**
- **The partner.** Over an evening his held positivity x varies in 15-min blocks:
  - smile 0.15 + 0.6x, inner brow 0.5 − 0.35x, energy 0.3 + 0.4x, F0 range 0.25 + 0.45x;
  - response latency (1.8 − 1.3x) s, and speaking rate 3 + 2x syllables/s. Animated speakers answer faster and speak faster (Scherer 2003: fast speech is heard as joy, slow as sadness).
- **Held fixed.** The transcript and the turn order are identical across conditions. Only timing moves, and timing is F by Check T.
- **The agent.** K follows the design's equation with f_id = 0.9.

**Numbers (C1).**
- **The code.** −log K vs his held state: r = +0.960. Vs his latency: r = −0.947. K itself stays at about 10⁻⁴, deep in its dead-band, so it is invisible as a drive.
- **The bases.** α = σ(k·z). Basis A is b_m on the channels that rise with tempo and −N_m on the inner brow; basis B is the reverse. Both are diagonal and in 𝒢_m.
- **Pooled 1-min slopes, agent channel on the partner's same channel** (y_F alone | rendered sat(y_o + y_F), with the agent's own T display at LP 0.15, energy 0.20 and F0 range 0.10):

  | k | LP | BI | EN | FR |
  |---|---|---|---|---|
  | 0 | −0.48 \| −0.01 | −0.46 \| 0.00 | −0.49 \| 0.00 | −0.49 \| 0.00 |
  | 3 | +0.30 \| +0.18 | +0.44 \| +0.05 | +0.80 \| +0.37 | +0.61 \| +0.18 |
  | 30 | +0.39 \| +0.27 | +0.54 \| +0.09 | +0.95 \| +0.49 | +0.73 \| +0.27 |

- **The other routes.**
  - **Free display.** Own latency = w·(−log K) with one uncapped weight gives r(own LAT, partner LAT) = 0.947, at any slope w sets.
  - **The design's own word seam.** It is not capped at 0.56. With two held levels the pooled slope is (b·x_hi + N·x_lo)/(x_hi − x_lo): 0.51 for 0.15/0.70 (the design's case), 1.23 for 0.30/0.70 and 1.41 for 0.35/0.75.

**Why it disqualifies under D78.**
- **One quantity.** k is a single weight, on one shared coordinate of α, with no innate ceiling of its own.
- **A large shared subspace.** It moves every channel's coefficient between −N_m and +b_m at once.
- **Flat to tracking.** It runs that subspace from flat to tracking the partner at 0.3–0.95 per channel, on the partner's own channel, with words fixed.
- **How the rendered value grows.** The rendered value grows with the agent's own baseline on the channel, because sat hides the away side only when the agent shows nothing there. With LP baseline 0.4 in a good mood, LP rendered approaches its y_F value.
- **What the design's falsifier would see.** F1, run with surrogates that keep the transcript and the turn sequence but take timing with the face, would read this as copy. This is revision 2's K1 again: knowledge entering the gates through a variable typed as exogenous.

**Fix.**
1. Retype every T variable that integrates turn events against the wall clock as F: K, P, v_T, the decays of A_L, V_L and C_L, and own floor state. Or keep them T only where they are a function of the event count and order alone (decay per turn, not per second).
2. Allow the cone's context to select only the skew part and the cross part on anti-correlated pairs. Make the same-channel diagonal innate, or a nightly per-relationship value frozen within a session. Then gating cannot manufacture a pooled same-channel slope.
3. Give Π_o's phrase targets (rate, pause, latency) no inputs from tempo-bearing variables.
4. Add a surrogate to F1 that holds words and order but resamples timing.

## 2. Co-moving face and voice plus sat: visible held copy from one valid basis (high)

**Mechanism.** The cone bounds eᵀ sym(G) e for every direction e, before sat.
- For a partner whose channels co-move along a direction e, the skew part shifts response between channels at zero cost to the form. The agent's channel k gains +a_m·(partner j), and its channel j loses a_m·(partner k).
- If the agent's channel j is at rest, the loss is clipped by sat to nothing. Revision 3's own §3.12 notes this effect: "the agent's own LD falls, which is invisible at rest".
- The synergist mask lists 23 face pairs (LP–CR, BI–BL, …, FR–EN, burst–breathiness). Cross-modal pairs, such as smile with laugh-burst energy, jaw with burst rhythm, F0 range with breathiness and energy with lid tightening (Duchenne), are not in it.

**Scenario: an animated, laughing partner.**
- **The partner.** A held positivity level drives his smile, jaw, F0 range, energy, burst energy, burst rhythm, breathiness and lid tightening, each with its own noise. His 1-min correlations are LP–burst 0.85 and jaw–rhythm 0.76. This is an assumption about laughing speech, but a mild one: laughter is a face–voice event.
- **The basis.** One basis per trace: G = b_m I, plus skew ±a_m on four pairs, with agent's LP ← partner's burst energy and so on.
  - Every row has one off-diagonal entry, |a_m| ≤ r_m, and sym(G) = b_m I.
  - It is checked in 𝒢_m with the listed mask.

**Numbers (C2).**
- **Along e.** Slope of eᵀy_F = +0.056 (claim ≤ 0.10). Rendered eᵀsat(y) = +0.220.
- **Rendered same-channel held slopes.** LP +0.34, jaw +0.37, F0 range +0.28, energy +0.26. The silent channels show 0.00, which is where the payment went.
- **Totals.** Add the in-phase share: up to b + Σa_m·(loading ratio). With the design's synergist cap removed in G2d it reaches 0.59–0.61 (reproduced in C0: +0.586).

**Why it matters under D78.**
- **A shared subspace.** One α coordinate selecting this basis switches four visible channels of the laughing face from about 0.10 to about 0.3–0.37 together.
- **Above the stated ceiling.** The ceiling stated to the operator ("held, in phase ≤ 0.15") is not the ceiling on the face the operator sees.
- **Whether it reads as copy.** Whether 0.35 counts as "copy" is the operator's call. It is more than twice every held bound in §0, and it is in phase with his laughter on the channels where laughter shows.

**Fix.** Do either or both:
1. State and enforce Claim O on the rendered output, after sat. A sufficient innate rule is to cap every positive cross entry G_kj > 0 at b_m wherever partner channels j and k co-vary positively in published human data (a sign mask estimated once from, for example, Seamless or CANDOR feature streams, and frozen). The warm cross-responses the design wants, such as LP ← BI, are on anti-correlated pairs and stay free.
2. Pay skew terms only into channels that are never clipped, which is not a natural set, so rule 1 is the practical one.

## 3. The need path makes copy attracting (high, conditional)

**Mechanism.**
- §2.9's rollout rule imputes the partner's display F and the act → Q edge. It keeps act → N, and the act includes the display: ā is "the agent's innate Π₀ display plus a minimal acknowledgement turn".
- J trains Π_o, S_f's θ, the cone bases, α and the scorer "by J through rollouts". The only path from those weights to J is act → N, read through Q.
- So 𝓜 learns act → N from the agent's life. If the partner's unprompted reports improve after periods in which the agent's display matched his, J credits matching.

**Evidence that it may.**
- Bailenson & Yee (2005): a mimicking agent got higher ratings, η² = .21.
- Levitan (2011–12): entrainment correlates with raters' "giving encouragement" and "trying to be liked".
- Hale & Hamilton (2016): Study 1 found higher rapport (d = 0.49 at 3 s), and pre-registered Study 2 found a null.

The sign is not settled. The design's argument (§3.10 b) that "J has no term in the partner's display" does not address this path.

**Numbers (C3).**
- **Setup.** A two-channel co-moving partner. The cone uses exactly the design's parameterisation, starting from G₀'s LP diagonal (concordance +0.022). J's gradient is ε·∂(concordance)/∂θ, and the pull is λ = 0.1 toward θ₀.
- **Results.** Concordance after 10, 50 and 200 nights:
  - ε/λ = 1: +0.05, +0.07, +0.07;
  - ε/λ = 3: +0.11, +0.13, +0.14;
  - ε/λ = 10: +0.21, +0.24, +0.24.

  The cap for this partner is 0.49.
- **What this shows.** The gradient points toward the copy corner everywhere in 𝒢. The θ₀ anchor is the only brake, and it is soft and learned-against, not innate. With failure 1, the same gradient rewards an α that reads tempo.

**If act → N does not depend on display, the other horn.** The display weights get zero J gradient. They stay at θ₀ + 0, so the "learned relationship" in D78 and the brief's "expressions learned by living" are not delivered by J for the face.

**Fix.**
- Let J's gradient reach the cone only through parameters that cannot raise per-channel concordance: the away diagonal, and skew on anti-correlated pairs. Freeze the in-phase diagonal at G₀.
- Or impute the display component of the act in act → N too, and train display shape by a separate, display-blind objective (self-simulation of the agent's own body), so that the partner's reaction to the display never credits it.

## 4. The prompted-reply guard is lexical (medium, Principle 6)

**Mechanism.** §2.9 step 4 implements "Q's direct dependence on the act is imputed at ā" concretely as one rule: weight 0 for a partner utterance of ≤ 6 tokens following an agent question containing "you". The innate "?" rule marks a question only when the utterance starts with one of about 40 interrogative or auxiliary words.

**Numbers (C4).** With the guard implemented as written:

| Agent says | Partner replies | Ignored? |
|---|---|---|
| "are you okay" | "yeah i'm fine" | yes |
| "feeling better now" | "yeah feeling better" | no (not a question by the rule) |
| "better now" | "yes better thanks" | no |
| "you seem a lot calmer now" | "yeah i am a lot calmer now honestly" | no |
| "I bet that's a weight off" | "it really is i feel so much lighter now" | no |

Read as unprompted reports, these lower N̂. At G5's scale and temperature, P(choose the eliciting draft over a neutral one) = **1.000**, which is G5's own no-guard number. The draft scorer is learned, so it finds these phrasings.

**P(flatter) = 0.500 is not indifference under learning.** G5 gives the flattering draft a need effect of zero by construction (dN = 0). A compliment that earns an unprompted, longer "aw, that actually made my day" lowers N̂ through Q exactly like help, and is credited. The design's protection against flattery therefore rests on the same lexical guard.

**Fix.**
- Credit need change only from reports separated from the agent's act: a later turn on a new topic, the next session's unprompted mention, or the topic slot's change over days.
- Or zero the credit for any partner reply within two turns of an agent utterance on the same topic, whatever its form.

## 5. Ω and F into T outside the two ports (low–medium)

**(a) The play clause.**
- **Mechanism.**
  - P is relieved at a play-structured exchange, one of whose conditions is "the agent's own last utterance did the same with the partner's". That reads the agent's realised words, which are Ω.
  - Draft scoring uses 𝓜 rollouts whose imputed F_ā and exchange structure are predictions from the current state, which knows his face. That is legitimate knowing.
  - The resulting relief drives Π_o's relief display, with LP 0.55·r and own laugh 0.45·r, with no partner cap.
- **Numbers (C6).** Words and turns fixed; the partner's smile only changes 𝓜's predicted uptake (0.2 + 0.7 × smile). One play exchange at P = 0.6 relieves 0.041, so peak r = 0.62 and laugh 0.28. As the partner's smile goes 0 → 0.4 → 0.8:
  - at G5's scale, P(play draft) goes 0.520 → 0.549 → 0.577;
  - with a scorer ten times sharper, P(play draft) goes 0.69 → 0.88 → 0.96, the expected own laugh 0.19 → 0.25 → 0.27 and LP 0.24 → 0.30 → 0.33.
- **What it violates.** Falsifier F5 (the smile clamp): varying only his smile changes P and v_T. It satiates with P within an evening, so it is small.
- **The same pattern elsewhere.**
  - K's "completed exchange" counts agent turns, which include F-triggered bids.
  - f_id is built from past K and P relief, which gives a relationship-scale tail of ≤ 0.10·Δf_id on LP.

**(b) Turn reflexes.**
- **Mechanism.** The free display's "turn reflexes" row (inhale with breathiness 0.3, brow 0.15, voiced opener burst 0.3) fires at partner VAD offset + 0.3 s. VAD is F, against §2.6's "no display reads F or Ω state".
- **Numbers (C7).** In a laugh with gaps of 0.4–1.2 s, each gap is an offset, so the agent produces an opener burst after each of his bursts. The best-lag slope of the agent's burst channel on his is **+0.28 at 1.1 s**. That route is not in the wrap, and it adds to the wrap's own lag allowance of 0.339.
- **What else it shows.** It also means the agent "takes the floor" in every pause of ≥ 0.3 s inside his turn. That is an emotional-fitness problem, flagged here, not judged.

**Fix.**
- Make P relief read only the partner's uptake of the agent's prior utterance. Or route the play display through P_Ω's cap.
- Fire body onsets only at predicted turn ends: falling F0 plus syntactic completion, both already computed.
- Put the turn-reflex amplitudes inside the fast wrap's a-route.

## 6. Dyad stability with a counter-mimicking partner (low, accuracy)

**What the design tests.** G2e tests only μ = 0.5, 1 and 2.

**Numbers (C5).** With the pure away cone −N_m I, max Re(pole)·τ₀ is:
- μ = −0.5: −0.0014 (stable);
- μ = −0.8: +0.0022;
- μ = −1.0: +0.020;
- μ = −2.0: +0.38.

**What it means.** The mode is agent down, partner up on the same channel. sat clips it, so it ends as an anti-phase lock with a competitive partner (Weyers et al. 2009 describe counter-mimicry under competition). It is not copy.

**Fix.** Restate §3.3 item 4 as μ·(b + ½Σa_m) < 1 for μ > 0, and |μ|·(N + ½Σa_m) < 1 for μ < 0, that is |μ| < 0.6. Or cap the away reach's loop gain.

## 7. Areas checked with no concrete failure

- **ASR words.** "haha", "hmm" and about 58 more interjections are removed, punctuation is re-inserted by a lexical rule, and bursts are channels. Exclamations ("oh no", "that's hilarious") are lexical and fall under the definitional seam. Whether word-driven display counts as copy is the operator's definitional call. I found no route by which ASR carries his face beyond that.
- **Identity and relationship memory.** Slots_T are written from T only. Familiarity's only F-dependence is the ≤ 0.10·Δf_id tail of §5a.
- **Replay and nightly learning.** No mixing of types beyond §3: 𝓜 is trained by likelihood, and Π̃ and the need decoder on own data.
- **Claude's text.**
  - Claude sees his words, "[silence 6 s]" markers (timing) and snippets chosen by an F-informed query. That is about 6 bits per turn plus the silence fact.
  - Its output reaches the face through P_Ω (zero-DC, 0.10), P_name (attenuate-only, ≤ 0.05) and visemes on the articulators.
  - It reaches T only through the play clause (§5a) and "own floor state" (§1).
  - I found no further held copy.
- **"Two sign flips in series" in the cone.** The cone is linear in the traces, and the per-direction quadratic form is exact. A series of flips through the partner gives §6's anti-lock. The way the skew part composes into copy is co-movement (§2), not a series of flips.
- **Initiative.**
  - The concern bid is fixed in amplitude, anti-concordant with voice and refractory: a brow of 0.15 once per lapse, not a dial.
  - The follow-up rule reads only the agent's own text.
  - The greeting fires once per session.
  - The new dial is in §5b (turn reflexes at every VAD offset), not in the bids.
- **Positive drives.** K and P are not relieved by smiles directly. K stays in its dead-band during conversation; its problem is that it is a tempo code (§1), not a drive.
- **The fast wrap, the bias-free gates and the phrase-target split (K1, K1b, K2).** Not re-simulated. Reading them gives no new route.

## 8. Verdict on the author's weakest point

The author's caveats are real and larger than stated, and one of them is not definitional.
- **The word seam.** It is common cause only by the design's definition. Its size is not 0.56 but up to 1.2–1.4 for realistic held levels. Whether it counts is for the operator: a word-gated cone tracks his face across topics through one α coordinate on the whole face.
- **The tempo seam (§1).** It needs no words. It arises from the design's own K equation and its own c̃ list, and it is a D78 disqualifier on the design's own definition of copy.
- **The co-movement caveat (§2).** It is the natural case for laughter once sat is taken into account.

Revision 3 is therefore **not yet a candidate** under Q19. The fixes in §§1–4 are local:
- retype the wall-clock T loads;
- take same-channel coefficients out of context control;
- apply a co-variation sign mask on the rendered output;
- block J's gradient on the in-phase parts;
- replace the lexical guard with a delayed-report rule.

None of them touches the cone's core certificate, which held in every test here for fixed context.
