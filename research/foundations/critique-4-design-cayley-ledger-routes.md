# Critique 4 of the Cayley–ledger core (revision 4): routes, copying and the learning loops

Independent critic, 2026-11-26T08:22:43Z. I did not write the design.

**Standard.** Written under questions.md Q19 and DECISIONS.md D78 and D80, on the recommended readings of Q20, Q21 and Q22: the inner state may know the partner closely; only expression is bounded; per-expression innate ceilings; the face feeds the agent's own appraisal. Proof gaps are not reported. Each finding is a concrete scenario with numbers. "Copy" is measured on the rendered output after `sat`, at any lag or time scale.

**Read:**
- brief.md;
- questions.md: Report 5, the Q18 answer, Q19, Q20, Q21, Q22;
- DECISIONS.md D78, D80;
- critique-3-design-cayley-ledger-routes.md, to know what was already found;
- design-cayley-ledger.md, revision 4, in full;
- sims/design-g4/checks.py (H0–H11, all of it) and out.txt.

**Checks.** They are in `research/foundations/sims/critique-cayley4-routes/checks.py`, sections D1–D8. Run `python3 -I checks.py` (numpy and scipy, a few seconds). The output is in `out.txt`.
- They use the design's own constants: τ_m, F_m, N_m, c_k, the 0.5/0.2/0.4 shares, the 20–90 s band-pass, the θ₀ echo (0.121 per unit onset at 0.45 s, through the 4-s high-pass), the ω update and s_smile formula of §2.12, and the distress rows of Π₀.
- The partners are constructed. They are not evidence about people. Where a result depends on a property of real partners, the property is stated.

## Summary

Revision 4 closes revision 3's four main failures as specified. I tried each of the eight areas I was asked to attack. One concrete failure of the D78 type remains, at a time scale the design does not measure. Two more are medium, and the rest are low or none.

**Ranked:**

1. **Medium–high (D78: a level-correlated gain on a DC path, one quantity on a five-channel group). The word seam comes back at the weeks scale, through ω.**
   - **The route.** ω_smile is latched per session, so Lemma S's rule 4 holds inside a session. But ω is learned over about 20 sessions from the agent's own play relief and its V integral with him.
   - **Why that matters.** Both of those track his mood over weeks: he plays when he is in a good month, and he is louder or glares more when he is in a bad one. So the cone coefficient on his smile co-varies with his smile level across sessions. That is Lemma S case (ii), with the gate set by the relationship instead of by words.
   - **Numbers (D3, D3b).** Two years of daily sessions, with month-long good and low periods:
     - his session-mean smile 0.30 vs 0.45: session-pooled rendered LP slope **+0.31**;
     - 0.38 vs 0.43: **+0.89**;
     - with some irritation in the low months: **+0.52** at 0.30/0.45. ω then swings from −0.75 to +0.98.
   - **Against what bound.** The within-session slope is ≤ 0.175, the ceiling c_LP is 0.35, and the claim "≤ 0.955 c_k pooled over any stationary partner process" is broken.
   - **Size.** The absolute effect is small: held LP 0.13–0.15 against 0.05–0.10. The pooled slope is large because his month-to-month change is small, which is exactly how the design reads its own 13.6.
   - **Scope.** ω_smile moves LP, CR, BU, RHY and BRE together.
2. **Medium (type rule, a written-spec route). As written in §2.1, the distress and relief events read F, and they drive the uncapped free display.**
   - **What the text says.** S_n is defined as "rises of the care term and of 𝒟_V", where care = max(N̂_F, N̂_L) uses the face and V = V_F + h uses loudness and glare. R_n includes "drops of the care term".
   - **What follows if it is built that way (D4).**
     - A loud, glaring partner gives agent lid tightener **0.23–0.24** (c_LT = 0, "no frown back"), inner brow 0.41–0.44 and depressor 0.32–0.34.
     - A silent sad face (face-read distress 0.3–0.6) gives inner brow **0.32–0.42** (c_BI = 0.20; the design's scenario 1 reports 0.02).
     - When his sad face lifts, the care-term drop fires the relief row: lip pull up to 0.55 as his smile returns.
   - **Where this came from.** The H11 engine uses word need and hurt only. So the numbers in §3.14 are right, and the text is not.
3. **Low–medium (copy partly attracting in style, the loop asked about in item 4). Co-training moves the agent's display code toward his.**
   - **Why it moves.** The legibility loss is invariant to which code the face uses: any code is legible once Π̃ adapts. So the only forces on Δ are ‖δ‖², which pulls toward Π₀, and the 0.1 anchor, which pulls toward his code.
   - **Numbers (D5b, a linear instance with his code reusing the agent's synergies).**
     - The cosine between the agent's state → face map and his goes from 0.01 to **0.26**, and to 0.27 at anchor weight 0.3.
     - The agent's own legibility gets worse (0.03 → 0.15).
     - Reading him barely improves (2.23 → 1.79).
     - With disjoint codes (D5) there is no drift.
   - **What it is and is not.** It is not a within-session route: no F input reaches Δ. It is the agent learning his way of expressing a state, and the brief arguably wants that. But it can bring his zero-ceiling channels (a lip press or brow lowerer he uses when distressed) into the agent's word-driven concern display. It is the mechanism behind the design's own F8.

**Lower:**
- **4. Low (accuracy).**
  - **The fast wrap's "pooled 1-min ≤ 0.01" is false after `sat`.** On channels that are silent at rest, `sat` clips the 4-s high-pass undershoot of the θ₀ echo. For a laughing partner, burst energy reaches **+0.071** and cheek raise +0.029 (D1).
  - **Totals stay inside the ceilings.** Burst energy 0.09–0.11 and lip pull 0.11–0.13, against 0.33.
- **5. Low (fitness of a D78 quantity).**
  - **ω_smile is a play indicator, not a relationship estimate.** Under the design's own formula s_smile = (play relief − V)/0.05, a single play turn per daily session gives s = 2.4 and ω → 0.98. The held smile return then sits at its cap, 0.172–0.175, for every partner who plays at all (D6).
  - **H4 does not use that formula.** Its ε = 0 baseline (0.051) assumes s = 0.3.
  - **Not copy.** But the "learned per relationship" strength has two values in practice, and it flips sign only through loudness and glare.

**No concrete failure found:**
- **(1) Lemma S itself.** I tried the constant gate, the innate m_glad, an afterglow gate, a full-wave sign(ξ_A) gate and a word-seam × sign gate on a constant-rate laugh carrier (demodulation).
  - The partners were natural laughing partners, whose variance lies mostly *above* 1/min: BU 6 %, CR 21 % and LP 41 % of their variance falls below 1/min. That violates assumption 5.
  - Even so, y_A's 1-min slope stayed at ≤ 0.14 c_k, and the rendered totals at ≤ 0.13 (D1, D2, D2b). ξ_A is simply too small for demodulation to matter.
  - Phrase targets are sampled at the agent's phrase onsets, which are partner-timed. That sampling of a band-passed voice channel gives a ripple of order 0.06 × level × 0.4 c, and c is 0.05–0.10 there, so it is negligible.
- **(2) T1, apart from finding 1.**
  - K is session-latched. P and I rise on the agent's own clock. The hurt latch is halved per play turn and decays over 10 min; with the words fixed, only the decay depends on tempo, and τ = 10 min is much longer than a turn.
  - The session-start K encodes his visiting schedule, but it reaches the face only as greeting relief.
  - ω reads V_F, which is F (a type slip noted in finding 1). Within a session it is constant.
- **(3) The per-expression ceilings and the face–voice mask.**
  - The cone's cross entries are innate (G₀), so adversarial bases are moot.
  - The worst natural case I found is a partner whose inner brow rises with his smile. That co-movement is consistent with the design's own groups through JO, but the mask sets S(LP, BI) = −1. It makes G₀'s warm LP ← BI and the sympathy basis's LP ← BI in phase, and it gives a rendered LP of **+0.27** at loading 1 (D8). That is under c_LP 0.35, and under the design's own residual formula, which gives 0.335.
  - The whole face stays ≤ 0.35.
- **(5) The appraisal display as a route.** As (1).
- **(6) The relationship loop.** ω rises under *any* playful partner (finding 5), not specifically a mimicry-rewarding one. Its cap is 0.175 on LP.
- **(7) Counter-mimics.** Even with every F route at its away extreme on one channel (cone −N, appraisal −0.4c, fast −0.49 with a 0.45-s lag), max|G| = 0.599. So the dyad is small-gain stable for |μ| < 1.67 at any partner lag (D7). The design's −1.1 is conservative. The anti-phase mode is clipped and is not copy.
- **(8) New dials.**
  - **Curiosity.** I is relieved per partner-initiated utterance by learning progress computed per utterance. Its level reaches only bids and retrieval.
  - **Turn gating.** It has fixed amplitudes (breath 0.15, outer brow 0.10). Its timing follows his F0, but its 1-min mean contribution is about 0.01.
  - I found no dial in either.

---

## 1. ω carries the word seam to the weeks scale (medium–high)

**Mechanism, from the design's text.**
- **§2.5.** The held in-phase diagonal is F_m · 0.5 c_k · ω_g, and ω_g ∈ [−1, 1] maps to [−N_m, +F_m · 0.5 c_k].
- **§2.12 item 8.** s_smile = (own play relief with this person − own V integral with him)/0.05, and ω ← ω + (tanh s − ω)/20 once per session.
- **The inputs.** Play relief is the drop of 𝒟_P at his play-structured turns, read from his words. The V integral contains V_F = f_loud + f_glare, read from his voice and face.
- **What follows.** ω is constant within a session, so Lemma S rule 4 holds. But ω follows his last ~20 sessions.
  - A partner in a good month plays, so s > 0 and ω → +1.
  - In a low month he does not play, and any loudness or glare makes s < 0, so ω drifts toward 0 or below.
  - His session-mean smile goes with the month too.
- **The result.** The coefficient on his smile and his smile level co-vary. Pooled over sessions, this is Lemma S (ii): β = (g_hi·hi − g_lo·lo)/(hi − lo), unbounded as hi → lo.

**Scenario (D3, D3b).**
- **Setup.** 730 daily sessions, with good and low months at random.
  - Good months: 4 play turns per session, his held smile `hi`.
  - Low months: no play, his held smile `lo`, and a V integral of 0 (D3) or 0.05 (D3b, mild irritability).
- **The agent.** Held LP = sat(0.10 familiarity + diagonal × level), using ω from the design's update.

| his smile lo/hi | low months | agent LP good / low | session-pooled slope |
|---|---|---|---|
| 0.20 / 0.50 | V 0 | 0.155 / 0.101 | +0.18 |
| 0.30 / 0.45 | V 0 | 0.149 / 0.102 | +0.31 |
| 0.38 / 0.43 | V 0 | 0.147 / 0.102 | +0.89 |
| 0.20 / 0.50 | V 0.05 | 0.134 / 0.062 | +0.24 |
| 0.30 / 0.45 | V 0.05 | 0.130 / 0.051 | +0.52 |

**Why it counts.**
- **Against the design's claims.** The design states "≤ 0.955 c_k pooled over any stationary partner process" and says the word seam is "closed by removing every context gate from DC-passing partner paths". A month-scale mood process is stationary, and ω is a context gate on a DC-passing path, learned from his words and his face.
- **Scope.** One quantity, ω_smile, moves five channels together (LP, CR, BU, RHY, BRE).
- **How much.** The absolute effect is ≤ 0.5 c_k × level ≈ 0.05–0.08 on LP. That is small, but it is the same kind of number the design used to condemn revision 3's seam: 13.6 at 0.45/0.50.
- **What the falsifier would see.** F1's within-session surrogates do not see it, because ω is latched. A month-scale surrogate (swap his face across months, keeping ω's history) would.

**Fix.** Any of these:
- Make ω's time constant much longer than any mood period, for example 1/200 per session (a year), or freeze ω after a learning period.
- Floor ω_smile at a positive value, so that a low month cannot flip it to away. That shrinks the session-scale seam to (0.175·hi − ω_min·0.175·lo)/(hi − lo), which is still unbounded, so pair it with the first fix.
- Retype ω's V input as F and remove it. V_F is F, and §2.2 forbids T values computed from F.
- Add the month-scale surrogate to F1.

## 2. The event definitions in §2.1 route F into the free display (medium)

**Mechanism.**
- **The text.** §2.1 defines R_n as the drops of 𝒟_K, 𝒟_P, 𝒟_I and of the care term, and S_n as the rises of the care term and of 𝒟_V.
- **What those terms read.**
  - §2.8: care C = w_C 𝒟_p(max(N̂_F, N̂_L)), and N̂_F comes from f_dist, his face through Π̃.
  - §2.1: V = V_F + h, and V_F is his loudness and glare.
- **Where it goes.** Π_o is typed T-only, yet it reads the envelopes of R_n and S_n.
  - The distress row is BI +0.45, LD +0.35, LT +0.25.
  - The relief row is LP +0.55 and CR +0.45.
- **What the engine does.** H11 computes S_n from word need and hurt only, so the scenario numbers do not show this.

**Numbers (D4), if the text is built as written.**
- **Angry partner.** Loud 0.85, brow lowerer 0.6, gaze at the agent, his lid tightener 0 to 0.75: V_F 0.50–0.95, a_d 0.91–0.98. The agent gets:
  - **lid tightener 0.23–0.24**, on a zero-ceiling anger channel, in phase with his anger face;
  - inner brow 0.41–0.44;
  - depressor 0.32–0.34.
- **Silent sad face.** Face-read distress 0.3 gives a_d 0.71 and inner brow **0.32**; 0.6 gives 0.42. The ceiling on this channel is 0.20, and the design's scenario 1 reports 0.02.
- **His sadness lifting.** The care-term drop is a relief event, so his smile returning fires the agent's lip pull (0.55 × a_r) in phase with it.

**Fix.** Define R_n and S_n from T parts only: the drops and rises of 𝒟_p(N_L) (word care), of h, and of K, P and I. That is what the engine does. Keep N̂_F and V_F for knowing (C_F, bids) and for the cone and appraisal inputs.

## 3. The co-training loop: style drift toward his code (low–medium)

**Mechanism.**
- **The nightly steps.**
  - Step 2 fits Π̃ on own (state, face) pairs, plus a 0.1-weight anchor that maps his face to his decoded need.
  - Step 5 trains Δ to make own states legible to Π̃_self, with a 0.1‖δ‖² penalty.
- **What the anchor does.** If self-reading and partner-reading share load coordinates, as Principle 3's "one map" and f_dist = Π̃(Rξ₀) imply, Π̃ is pulled toward reading *his* code.
- **What legibility does.** Δ then follows Π̃. Legibility itself prefers no code, so nothing resists the anchor except ‖δ‖².

**Numbers (D5, D5b).** A linear instance: 3 own states, 3 synergies, Π̃ fitted nightly by least squares, Δ by gradient steps within ±0.3.

| Instance | Night 1 | Night 10 | Night 100 | Night 400 |
|---|---|---|---|---|
| D5: disjoint codes (he uses other synergies), cosine to his code | 0.00 | 0.00 | 0.00 | 0.00 |
| D5b: his code permutes the agent's synergies, anchor 0.1 | cos 0.01 | 0.15 | 0.26 | 0.26 |
| D5b, anchor 0.3 | 0.07 | 0.26 | 0.27 | 0.27 |

- **D5b, anchor 0.1, the errors.** Own-legibility error goes 0.03 → 0.15, and the error reading him goes 2.23 → 1.79.

**What it means.**
- **Not copy.** It is not within-session copy, since Δ reads only T. And it is bounded: by the cosine plateau, by ±0.3 per synergy and by the 23-synergy basis.
- **What it does.** The agent's expression of its own concern takes on the form he uses for distress. If that form uses zero-ceiling channels (a lip press, a brow lowerer), the agent's word-driven concern display acquires them, and they fire whenever his words carry distress.
- **Under the design's definitions.** That is common cause by definition (R14). But the ceilings that Q22 sets for anger, disgust and contempt do not cover this route.
- **The cost.** The agent becomes less legible to itself without reading him much better.

**Fix.**
- Give the self and partner heads separate output layers on the shared trunk. Or block the anchor's gradient into whatever trunk features the self head reads.
- Add zero-ceiling synergies to Δ's mask, so Δ cannot put weight on anger, disgust or contempt synergies.
- Run F8 as stated.

## 4. Accuracy and fitness notes (low)

- **Fast wrap after `sat` (D1).**
  - **The claim.** §3.1 says the fast wrap's pooled 1-min slope is ≤ 0.01.
  - **What `sat` does.** On channels at 0 at rest, it clips the echo's high-pass undershoot.
  - **Numbers.** For a laughing partner with 0.5–3.5 laughs per minute, rendered 1-min slopes are burst energy **+0.071** and cheek raise +0.029. Lip pull, with a 0.10 resting smile, is +0.001.
  - **Fix.** Add a rectification allowance (about 0.6 κ_k × the fraction of time at rest) to the totals table. It fits inside the shares for every channel tested.
- **ω's saturation (D6).** The table below gives ω after 200 daily sessions, by play turns per session.

  | Play turns per session | s_smile | ω | Held LP in-phase |
  |---|---|---|---|
  | 0 | 0 | 0 | 0 |
  | 1 | 2.4 | 0.98 | 0.172 |
  | 2 | 4.1 | 1.00 | 0.175 |
  | 4 | 6.2 | 1.00 | 0.175 |
  | 8 | 7.6 | 1.00 | 0.175 |

  - **What it means.** The divisor of 0.05 makes tanh saturate. The relationship strength is effectively "plays at all", and the smile return sits at its cap for almost everyone. H4's ε = 0 baseline (s = 0.3, giving 0.051) is not the §2.12 formula.
  - **Fix.** Normalise s by the session's available play deficit, and use a divisor near the typical relief (≈ 0.3).
- **The G₀ entries on the 20-s trace.** The engine places LP ← f_glare −0.07 and BI ← f_glare 0.04 on the 20-s trace. These are charged entries (f_glare has no sign in the mask), but F₀ = 0, so the charged budget there is 0. G₀ is therefore outside its own set 𝒢₀. The effect is small, 0.07 × his LP–glare loading. Move them to the 2-min trace.

## 5. Areas checked with no concrete failure

- **Lemma S and the appraisal display (items 1 and 5).**
  - **What I tried (D1, D2, D2b).** Five gates, including the adversarial full-wave and demodulating word-seam gates, on natural pulsed laughter whose variance lies mostly above 1/min. That violates assumption 5, yet the bound still held: y_A's 1-min slope was ≤ 0.144 c_k and the rendered totals ≤ 0.13.
  - **Why.** The band-pass keeps E|ξ_A| small: the absolute DC that demodulation produces is ≤ 0.003.
  - **Phrase-onset sampling of y_A on voice channels.** Negligible: ripple × 0.4 c with c ≤ 0.10.
- **T1 (item 2).** No T variable integrates his timing within a session, apart from ω at the session scale (§1).
- **Ceilings and the sign mask (item 3).** The cross entries are innate. The worst natural sign-reversal (brow rising with the smile) gives LP +0.27 rendered (D8), under 0.35. The whole face stays ≤ 0.35.
- **The relationship loop (item 6).** It is bounded at 0.175 on LP (D6).
- **Counter-mimics (item 7).** Small-gain stable for |μ| < 1.67 with every route at its away extreme (D7).
- **Curiosity and turn gating (item 8).** Covered in the summary.
- **Credit (H5).** Only separated reports are credited. I found no route by which J reaches any F → face parameter.

## 6. Verdict

Lemma S, T1, the per-channel ceilings, the sign mask and the removal of J from the face all hold against every within-session attack I could build, at 1-min and 5-min pooling, on the rendered output.

The one D78-type failure (§1) is the same seam one level up. A per-session latched gain that is learned from his recent weeks is a level-correlated gain at the weeks scale. It is local to ω's update rule, and its absolute size is small.

§2 is a specification slip that the engine already avoids. §3 is the co-training risk the author named, here shown to move style but not to produce within-session copy.

With §1's and §2's fixes, I found nothing left that carries copying beyond the ceilings at any time scale I tested.
