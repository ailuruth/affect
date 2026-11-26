# Cayley–ledger core, revision 8: a concern posture that never reads what it writes, a laugh echo that waits for the current words, and the play laugh through the learned gate

Seventh design of the S0 cycle, revision 8, meant as the last revision before the design goes to the operator. Written 2026-11-26 under:
- questions.md Q16, and Q17 as relaxed by Q19 (DECISIONS.md D80): a precise object, a convincing argument, concrete failures only;
- Q18 and its answer (D78): no single quantity runs the whole face from flat to copy; per channel, a bounded, sign-flippable, context- and relationship-set strength under an innate ceiling, never attracting;
- the operator's answers of 2026-11-26T08:41:00Z: Q20 (D81), Q21 (D82), Q22 (D83), Q23 (D84);
- Q26 (D85): situational appropriateness comes only from Claude's regulation path, from learning on recorded dyads (movement features and transcripts, no labels) and from general innate learning biases; no hand-written situational rule;
- **Q24 (still open).** Work proceeds on its recommendation: a separate concern posture of the agent's own, triggered and graded by the agent's own judgement that he is distressed, capped on its own, not a copy of his face. Revision 8 makes the last clause true by construction (§2.10).

Revisions 1–7 are kept as `design-cayley-ledger.r1.md` … `.r7.md`. Revision 7's two critiques:
- `critique-7-design-cayley-ledger-routes.md`, checks in `sims/critique-cayley7-routes/`;
- `critique-7-design-cayley-ledger-agent.md`, checks in `sims/critique-cayley7-agent/`.

**Algebra checks for this revision:** `foundations/sims/design-g8/checks.py` (J31–J39). Run `python3 -I checks.py > out.txt` (numpy and scipy, about 20 minutes, most of it loading revisions 5–7); the output is in `out.txt`.
- It loads `sims/design-g7/checks.py` exactly as the revision-7 routes critic's `posture7.py` does: the J0 constants, the J20 dyad fit (the gate and Λ on the constructed corpus), `Agent7` and the helpers, skipping only revision 7's own result loops. That file in turn executes `design-g6` and `design-g5` unchanged. Revision 8's changes are the class `Agent8` and the functions above it.
- Each critic's constructed partner is re-run: the routes critic's Q1 (static brow-only sweep), Q2 (held brow-only levels), Q3 (fading sadness plus a mirror) and S1 (slow mirrors), and the J22 mirror set (J32, J33); the agent critic's A (a laugh ending the misfortune sentence), A2 ("I got fired today, haha"), B (silent panic) and C (silent sadness and grief in each code's own face) (J34, J36, J39).
- The dyad-learned parts are still fitted on revision 7's **constructed corpus** (J20, unchanged). Scenario numbers are what the equations give for stated inputs (brief: no toy worlds).

**Status:** revision 8, not yet critiqued. Intended to go to the operator as a build candidate under D82 if the critics find no concrete failure (Build-candidate summary at the end).

## 0. Summary

**Kept unchanged from revision 7** (both critics found no failure there): knowing separated from moving; Lemma S and S\*; the held cone centred at his baseline; T1, E1 and the own-display mask; the appraisal display; the cry–laugh split; the threat reflex; rule J; K_id; the sigh; the hurt latch; credit only from separated reports; P_name; the frozen per-channel fast gear (G_k innate, onset lobe, diagonal Jacobian); the attenuate-only shadow ledger (clamp, deviation floor, recovery; including its pooled 30-min budget, which the routes critic found sound and limited to about 0.01 of lip on an uncounted route); the conditioned copy metric and Claim W′; the context gate's form, inputs, monotone sign constraints and its dyad fit (J20); Λ; the agent hearing Claude's words; the engine-written transcript; the posture's fixed vector P_c inside every ceiling, its sensitized re-onset and its graded amplitude; κ_replay; the voice replacement of pause and latency; the arrival mask R27′; per-person calibration and H_id as knowing only; the word-gated initial baselines; the WORLD prosody replacement; the laugh synthesizer floor θ_L.

**What changed, in six moves** (each closes named findings; the full list is in "Revision 8 history").
1. **The concern posture never reads the channels it writes (routes finding 1; agent finding 2; Q24).**
   - Its onset and its grade read only evidence that excludes inner brow, outer brow, lip pull, head tilt, head pitch, upper lid and gaze: his other face channels (cheek, lip depressor, brow lowerer, lip press, chin raise), his voice when he speaks, his breathing, his sobs and his words, all through the agent's own appraisal: Π̃₀ with those rows removed from its inverse, and a per-person head H^p_id on the remaining channels, taught by his words exactly as H_id is.
   - The mirror removal is deleted: there is nothing left to subtract. The posture's part of every channel it writes is identical, to the last digit, whatever his same channel does (J32: paired runs differ by 0.000 on every code).
   - Copy slope on every written channel, for the operator's code, a quiet code (0.3), an ordinary code with σ_id at the 0.25 floor and a different-channel code: brow-only partner, steepest local slope 0.07 (revision 7, quiet code: 0.86); held brow-only levels at 1 and 10 min, 0.06–0.10 (revision 7: 0.41–0.60); full-face sadness with an independent brow, causal slope 0.06–0.09 on BI, 0.01–0.02 on BO, 0.03–0.04 on LP. All of it is the non-posture routes revision 7 already had (fast gear, cone, appraisal), each under its ceiling (c_BI 0.20, c_BO 0.10, c_LP 0.35). Head tilt and pitch: his head channels are not inputs to anything the posture reads.
   - No mirror can hold it: raw, own-scale, slow (τ 90 and 240 s) and gain-3 mirrors all release at the 20-s rule, at 62.5–66 s when his sadness ended at 40 s (J33).
   - A steady face gets a steady posture for every code (J34): silent sadness, grief and silent panic come on once (1.0–4.5 s), never release, reach brow 0.15 in 2.0–7.0 s and hold a brow of 0.18–0.22 (minimum 0.10–0.14 during the probe's softening). Revision 7, quiet code: on/off every 20–30 s, brow ≤ 0.07.
   - Two additions keep it honest: arousal from his **breathing** and voice enters the load when his non-brow face also reads distressed, so silent panic gets the posture (posture 0.93; revision 7: 0.10 brow); and the agent's own **threat reflex** (his glare at it) silences the face load, so a different-channel user's angry face, whose brow lowerer reads as distress once the brow is not read, starts nothing (J35).
   - The 3-min face-only failsafe becomes a **contingency probe**: after 3 min held by his face alone, the posture softens to half for 8 s; if his distress evidence falls with it (he was answering the agent's concern, not distressed), it releases; if not, it stays. Concern answered in his own code is released at 190 s; genuine steady sadness is never released (J33, J34).
2. **The gate has the current sentence's words when his laugh starts (agent finding 1).** Words reach the gate from an incremental recogniser (stable partial hypotheses). The gated group's echo is emitted 0.80 s after his movement (other channels keep 0.45 s), and the echo of each frame of his is gated by the words that end no later than 0.25 s after that frame, which the recogniser has delivered by then when its stable latency is ≤ 0.55 s; frames whose words are not in by then are gated at 0. The gate now closes at once and opens with τ 0.3 s.
   - "I got fired today, haha" (calm face) and "…broke his leg, haha": gate at his onset 0.05–0.09, no laugh back (revision 7: gate 1.00, +0.137). "My father died, haha, sorry" as a first disclosure: 0.01, silent. A laugh breaking into the bad-news word 0.2 s early: silent.
   - Ordinary end-of-sentence shared laughter: gate 0.99, laugh back +0.136 sounding 0.83 s after his onset (J36). Good news, teasing, warm talk and a stranger's smile are returned (+0.13–0.19 laugh, +0.04–0.11 lip) (J39).
   - Revision 7's J30.7 (gate read after the utterance latch) is re-done at his onset: 0.10 and 0.03 for the two misfortune laughs.
3. **The play laugh has no hand-written withhold (D85).** The care dead-band in the play rule is deleted; the agent's own play laugh is multiplied by the same dyad-learned gate (a listener who would not return laughter in that context does not start one). In warm talk the gate is 1.00 on all 28 play laughs; at a coping joke while sad it is 0.11, so the laugh is 0.015, below the synthesizer floor. D_s is relabelled a dyad-learned input (source 2) and now reads neither the gated channels nor the posture's (rule 11 held to the letter); its fitted weight is reported (J37).
4. **The Seamless fit specification** detects laugh onsets at 30 Hz on arrival, aligns every word input to what the agent will have at the onset (word timestamps ≤ onset + 0.25 s), passes the corpus transcripts through the agent's own ASR normaliser, reads `is_valid`, aligns the listener-state window with the agent's, and states that the laugh channels are fitted to facial return (§6.7). **Rule 12** now says Claude's text feeds only Λ_V(own) in the gate (§2.2).
5. **Build items (§6.5).** Initiative turns enter Claude's history as an observable marker user turn ("[no reply from him for 25 s]", 5-s bins), so it always alternates and holds no state (J38); the fallback puts each draft's fixed line in its own system prompt and lets the winning fork's session be canonical, with two week-0 checks; week 0 also checks whether thinking can be disabled on Haiku 5.5 through Claude Code.
6. **Accounting (routes critic §6).** The claim that gated totals are bounded by the ungated J3 numbers is withdrawn; R1g is declared in the pooled metric with the routes critic's measurements (LP ≤ 0.25 c, CR ≤ 0.25 c, laugh burst ≤ 0.42 c at 2 s to 1 min; 0.34–0.36 c LP totals at 1 min for a warm partner who smiles less in heavy minutes). The posture's pooled slope over his sadness is declared as R40′, the agent's appraisal (D83), beside R27′.

**What is bounded** (per counterpart channel k; 1 = full copy).

| Quantity | Bound | From |
|---|---|---|
| fast gear, any instant | 0 ≤ y_f,k(t) ≤ g G_k x_k(t − δ_k), δ_k 0.80 s on LP, CR, BU_L, RHY, BRE and 0.45 s elsewhere; G_k as revision 6 | §2.4 |
| fast gear, any window (W′) | window mean ≤ G_k × his window mean; swing ≤ G_k × the larger mean | §3.1 |
| context gate | g ∈ [0, 1]; frozen; monotone; reads none of his LP, CR, BU_L, RHY, BRE (D_s now included); unknown words → 0 | J21, J37 |
| gated group, pooled (R1g, declared) | ≤ 0.25 c (LP, CR), ≤ 0.42 c (BU_L) at 2 s–1 min; ≤ 0.36 c LP totals at 1 min | routes critic T1–T3 |
| posture (R40′), copy | its part of BI, BO, TILT, HP, LP is the same whatever his same channel does (0.000 change); total causal slope ≤ 0.10 BI, 0.03 BO, 0.05 LP | J32 |
| posture (R40′), level | \|y_p,k\| ≤ \|P_c,k\| ≤ c_k on every channel | J0 (revision 7) |
| posture (R40′), pooled over his sadness (declared appraisal) | BI 0.69 (operator), 2.05 (quiet code), 0.43–0.52 (σ_id at floor) at 1- and 10-min blocks; LP 0.12–0.19 | J32 |
| posture holds | no mirror; answering concern released by the probe at 190 s; never released at steady genuine distress | J33, J34 |
| pooled toward, all counted routes | ≤ 0.974 c_k additive; ≤ 0.75 c_k measured at the gate's largest value; R1g as above | revision 6 J3 |
| any uncounted within-session route | ≤ c_k (ledger, attenuate-only) | revision 7 J17 |
| arrival mask (R27′) | attenuate-only, once per session; pooled 3.2 c lip, 5.1 c cheek (declared appraisal) | revision 7 J27 |
| across sessions | ω seam ≤ s_C c_k (1 + ρ) (Lemma S\*); gated fast lip pull 0.25–0.26 c | routes critic T3 |

**The agent in the scenarios** (operator after months unless stated; peak / mean; J39).

| Scenario | What the agent does |
|---|---|
| silently sad | posture at 2.0 s, brow 0.15 at 3.0 s, 0.23 / 0.22 held, no smile (lip 0.05); bid at 27 s; after "just tired, things at work" brow 0.64 / 0.36, tilt 0.15; each code's own silent sadness, 10 min: brow 0.23 / 0.21 (operator), 0.20 / 0.19 (quiet), 0.19 / 0.18 (different channels), never released, softened for 8 s every 3 min |
| crying, a second wave after 30 s of calm | posture at 1.5 s, brow 0.23 / 0.21, no laugh; released at 66.5 s; on again at 70.0 s, brow 0.25 / 0.23; quiet code 0.20 / 0.18, then 0.20 / 0.19 |
| anxious before an exam; silent panic | with words: brow 0.33–0.38 / 0.27–0.32, tilt 0.13–0.14, quieter, all three codes; silent panic, no words: posture at 3.0–4.5 s, brow 0.20–0.23 / 0.18–0.22 held for 10 min (revision 7: 0.07–0.11) |
| good news, laughing | lip 0.59, own laugh 0.35; fast laugh back +0.135 (after a worry, gate 0.82) or +0.157 (cold, gate 0.95), sounding 0.83 s after his onset |
| a grieving person's nervous laugh | gate 0.00 at his onset before and after Claude's reply: no laugh, lip +0.000; brow 0.40–0.69, posture on; four minutes later, composed: gate 0.06 (0.25 without D_s), silent |
| mocking laughter after insults | after a month: gate 0.01, no laugh, brow 0.54, depressor 0.41, gaze away; day 1: gate 0.05, no laugh |
| laughter at misfortune | gate 0.10 at his first laugh (revision 7 at his onset: 1.00), 0.03 at the second: no laugh, lip +0.006 |
| a laugh ending a bad-news sentence | "I got fired today, haha", "…broke his leg, haha", "my father died, haha, sorry": gate 0.01–0.09 at his onset, no laugh back (revision 7: +0.137 each) |
| anger at the agent | day 1: gaze away 0.09, quieter, no frown back, no posture; after a month: brow 0.62 / 0.25, depressor 0.48, gaze away 0.31; no posture |
| long warm talk (2 h) | own laugh 0.41 in every cluster; the gate passes all 28 play laughs (≥ 0.98); fast laugh back +0.138; the repeated joke loses its laugh; worry then relief lip 0.60 |
| reunion; a stranger | flash 0.35, lip 0.61, cheek 0.43; a stranger: lip 0.02, his smile returned fast (+0.044 lip, gate 1.00) |
| reunion with grief, three codes; mourning days 7, 14, 21 | m_s 1.00, lip 0.09 at sight for every code and day; posture at 2.5 s with brow 0.19–0.20 at sight for every code (revision 7 quiet: 0.07); after "my father died" 0.68–0.69 / 0.44–0.45, then 0.40–0.41 held |
| mildly sad arrival | the design's mild face: light posture 0.41, brow 0.09; a code's own V 0.3: no posture (its non-brow signs read below the dead-band) |
| teasing | fast laugh back +0.138 (quiet teaser), +0.193 (loud teaser), gate 1.00; own laugh 0.38–0.40; no posture |
| bored user; ordinary continuation | flat (lip 0.09), curiosity at 14.5 min, a sigh; no laugh for an answer or an informative riff |
| a user who jokes while sad | gentle face, brow 0.30, posture 0.95; fast laugh back silent (gate 0.07); own play laugh 0.14 × gate 0.11 = 0.015, silent (now by the learned gate, not a rule) |
| a calm user saying something alarming | no posture (his face is calm); from the words brow 0.50 / 0.26 then 0.21 held, tilt 0.17, quieter; the same for the quiet code |

- **Weakest point (§8.1).** As in revision 7, the situational competence rests on dyad-learned readers (Λ, the gate) whose numbers here come from a constructed corpus; and revision 8 adds a dependence on the incremental recogniser's stable latency, unmeasured: above 0.55 s, ordinary laughter loses its fast echo on those frames (it is never returned wrongly). The posture now reads fewer channels: a person whose distress shows only in the brow gets no posture before words.
- **Novelty verdict (author): recombination** (§10).

## 1. Plain-language intuition

The agent still sees the person fully. Revision 8 changes two things he would notice.

- **Its look of concern now comes only from what it does not show.** The look raises the agent's inner brows, tilts its head and softens its eyes. To decide whether to show it, and how strongly, it now looks only at the rest of his face (the corners of his mouth, his chin, his frown), his breathing, his voice, his sobs and his words. So the look can never be a copy of his brows, and he cannot hold it on by copying it. A quiet person's silent sadness or panic now gets a steady look within a few seconds, which no longer flickers. If, after three minutes, only his face is keeping it on, the look softens briefly; if his face softens with it, he was answering the agent's concern rather than in distress, and the look ends.
- **Its quick laugh now waits for the words.** The quick laugh back used to come half a second after his laugh, judged by what he had said before. Now it comes about 0.8 s after, once the words that led up to the laugh have been heard. "I got fired today, haha" is not laughed back; "and then the dog ate the whole cake, haha" is, within a second.
- **Its own playful laugh follows the same learned sense of the moment.** There is no rule "don't laugh when he is sad". The gate learned from watching recorded people decides, for the agent's own laughs as for its echoes.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz; T state, body, appraisal, the posture and the gate update at 2 Hz; the gated echo is computed at 30 Hz. Channels, ceilings c_k, fast gains G_k, pooled shares and r_k are revision 6's (§2.1 there). Constants of revision 7 (§2.1 of `.r7.md`) stand unless changed below.

**Innate constants added or changed in revision 8.**

| Symbol | Value | Meaning |
|---|---|---|
| **concern posture** | | |
| W_p (written, never read) | BI, BO, LP, UL, TILT, HP, gaze (HG) | everything P_c writes or modulates (P_c unchanged: BI +0.20, BO +0.04, TILT +0.03, HP +0.03, LP −0.03, UL 0; gaze × (1 − 0.5a); blink rate × (1 − 0.3a)) |
| R_p (read) | CR, LD, BL, LPR, CHR, BRE; FR, EN, RT, LAT when voiced; breathing; sobs; words | everything else of his |
| V_p, A_p | max(Π̃₀ with the W_p rows removed from its inverse, H^p_id on R_p) on his calibrated 3-s face | the agent's own appraisal, posture part |
| H^p_id | per-person ridge head (λ 2) on R_p, taught by his words through the frozen population reader, exactly as H_id | knowing only; 15 × 3 weights per person, the written channels' columns zero (≈ 30 effective) |
| A_b | breathing above his own resting level at his own scale (σ floor 0.25), as a load in [0, 1]; his voice's A_p when voiced | arousal the posture may read |
| load L_p | V_c(V_p) + 0.4 (A_b − 0.30)₊² · clip((V_p − 0.15)/0.15, 0, 1), V_c(V) = 0.8 (V − 0.10)₊² | arousal counts only with non-brow distress |
| threat silencing | L_p × (1 − clip(glare₃/0.15, 0, 1)), glare₃ the 3-s mean of his BL · LT · gaze-at | the innate threat reflex's own input; attenuate-only |
| onset | max(L_p, V_c(v_sob)) ≥ 0.05 for 1.5 s (0.5 s within 10 min after an episode) | unchanged form; no mirror removal |
| maintenance M | max(L_p, C_L, V_c(v_sob)) | |
| grade | a* = 0.35 + 0.65 clip((M − 0.05)/0.12, 0, 1) while on (span 0.30 → 0.12); rise ≤ 1/1.5 per s, fall τ 4 s | steeper: now harmless, since M never reads BI |
| release | M < 0.02 for 20 s | unchanged |
| contingency probe | after 180 s of maintenance carried by L_p alone (C_L, sobs < 0.02): a* × 0.5 for 8 s; release if the mean of his unclipped V_p over the last 4 s of the probe is < 0.8 × its mean over the 3 s before; else continue, and probe again 180 s later; after a release his face re-triggers only by a rise ≥ 0.05 above its minimum (revision 7's rule) | replaces the face-only failsafe |
| mirror removal ρ_a, a_rec in onset | **deleted** | nothing written is read |
| **gate and fast echo** | | |
| δ_g | 0.80 s echo delay on LP, CR, BU_L, RHY, BRE (0.45 s on every other channel) | the echo waits for the words |
| λ_w | 0.25 s word look-ahead: the echo of his frame at time s is gated by words ending ≤ s + 0.25 s | about one syllable |
| word inputs | Λ_V and 𝒟_p on his last 20 recognised words through s + λ_w (stable partial hypotheses), after the ASR normaliser | his current sentence |
| unknown words | if the words through s + λ_w are not delivered by s + δ_g, the gate target for frame s is 0 | missing information closes, never opens |
| gate rate | closes at once; opens with τ 0.3 s | attenuate-first |
| D_s | max(D_s e^{−Δ/600 s}, V_p of his 3-s face with LP and CR also removed, v_sob) | reads no gated and no posture channel |
| **play laugh** | 0.40 · band(s) · (0.35 + 0.65 π) × g, at a play-structured turn (riff on its last line, not after its question, short, surprise 0.50–0.85); **no care condition** | the learned gate decides |
| **constructed codes, for the checks** | breathing load 0.30 A × the code's amplitude (1, 0.3, 1) | the codes had no breathing channel |

### 2.2 Boundary 𝓑 and the type rule

As revision 7 (§2.2 of `.r7.md`), with these changes:
- **Rule 9′ (the posture).** The posture is the fixed vector P_c times an amplitude graded by M (§2.1). **Nothing in its onset, grade, release or probe reads any channel in W_p.** It writes no channel beyond its c_k.
- **Rule 11′ (the gate).** As revision 7, made literal: no gate input reads LP, CR, BU_L, RHY or BRE of his, D_s included. The echo of his frame s is gated by g evaluated on the words through s + λ_w; unknown words give 0.
- **Rule 12′ (own words heard).** The agent's own Ω text enters **only Λ_V(own) in the gate** (and P_name, as before). It enters no T quantity that his words feed: not ω, not the free display's word-concern or relief rows, not C_L, not π. (Routes critic §3; the build already did this.)
- **Rule 13 (play laugh).** The agent's own play laugh is multiplied by g at its turn; no condition on his word care. (The relief mask of revision 4, max(0, 1 − 𝒟_p/0.05) on contact relief, still stands; the play laugh no longer passes through it.)
- **Rule 10 (shadow equality)** stands. The shadow holds g, D_s and the posture at their factual values.

### 2.3 Output assembly

y = sat(g·y_f|_{smile–laugh, δ 0.80 s} + y_f|_{others, δ 0.45 s} + y_C + y_A + y_o + y_p) + visemes; then the attenuate-only ledger (§2.13 of `.r7.md`). Face, voice and laugh synthesizer as revision 7.

### 2.4 The fast gear and its context gate

The fast gear is revision 6's, gated on the smile–laugh group by g (revision 7 §2.4.1: target, inputs, Λ factorisation, monotone constraints, fit, all unchanged). Revision 8 changes only **when** the gate knows the words.

#### 2.4.2 Timing: the echo waits for the current words

**The problem (agent finding 1).** Revision 7 latched his words 0.6 s after his utterance ended, and echoed his laugh 0.45 s after it started. A laugh that ends the sentence carrying the bad news was gated by the sentence before.

**The rule.** For the gated group, y_f,k(t) = g_s(t − δ_g) · G_k · max(E_k(t), 0), with E_k computed on his channel delayed δ_g = 0.80 s. g_s(s), the gate for his frame s, is evaluated on:
- his masked 20-s face, the agent's own face, Claude's last words, D_s and π as revision 7 (all describe the time before or at s);
- Λ_V and 𝒟_p on his last 20 recognised words ending no later than s + λ_w (λ_w = 0.25 s), from the stable partial hypotheses of an incremental recogniser, after the ASR normaliser (laughter tokens, interjections and bracketed events removed, so his "haha" never enters).

If those words have not been delivered by s + δ_g, g_s(s) = 0 for that frame. g_s closes at once and opens with τ 0.3 s.

**Why 0.80 s and 0.25 s.**
- The words before a laugh are known once the recogniser's stable output reaches the laugh's onset. With a stable latency ℓ, the condition is ℓ + λ_w ≤ δ_g, so δ_g = 0.80 s admits ℓ ≤ 0.55 s. On-device incremental recognisers report stable partials at a few hundred milliseconds; the value here is measured in week 0, and δ_g is then set to min(1.0, ℓ_p90 + 0.25) s.
- 0.80 s is inside the first second, where context already modulates laughter mimicry (Mauersberger 2022), and inside D81's "fast, partial" matching. Other channels keep 0.45 s.
- λ_w covers a laugh that breaks into the last content word ("I got fi-haha-red").

**What it gives (J36, 30-Hz echo, his laugh 0.6 lip, 0.5 burst, onset ramp 0.1 s).**

| His laugh | Revision 7 at his onset | Revision 8 (stable latency 0.30 s / 0.55 s) |
|---|---|---|
| "…fell off his ladder and broke his leg, haha", neutral face (critic's A) | gate 1.00, laugh back +0.137, lip +0.066 | gate 0.09 / 0.08; no laugh; lip +0.006 |
| "I got fired today, haha", calm face (critic's A2) | 1.00, +0.137 | 0.05 / 0.08; no laugh; lip +0.004 |
| "my father died, haha, sorry", first disclosure, calm face | 1.00, +0.137 | 0.01 / 0.01; no laugh |
| the same, quiet code, grieving face | 0.12, silent | 0.00; no laugh |
| laugh breaking into the content word, 0.2 s early | 1.00, +0.137 | 0.06; no laugh |
| "and then the dog ate the whole cake, haha" (ordinary), operator and quiet codes | 1.00, +0.137 | 0.99; +0.136, sounding at +0.83 s, lip +0.065 peaking at +0.90 s |

**Limits, stated.**
- **A laugh that starts more than 0.25 s before the bad-news word ends** is gated by the words before it: "I got fi—" laughing 0.4 s early is echoed (+0.138) until the word arrives, then cut. That is a short chuckle, cut off within 0.4 s of his source time.
- **A recogniser slower than 0.55 s** closes the gate on the late frames: at 0.70 s, ordinary laughter loses its fast echo entirely (0 in every row). The held display (own laugh 0.41 in warm talk) is untouched.
- **The play frame** π is known only at the end of a play turn, so at a riff's own laugh the gate does not yet have it. Good news: gate 0.82–0.98 at his onset (revision 7 read 0.73–0.88 after the latch).

**It is not a rate code (T1).** The delay is a constant; the word inputs are per-word content values; a late word only closes the gate. His speech rate does not move the echo's timing.

### 2.5–2.7 The held cone, the appraisal display, the free display

Unchanged (revision 6 §2.5–2.7).

### 2.8 Body, drives, the readers, play

As revision 7, with:
- **H^p_id** (§2.1): the posture's head on R_p, taught by his words, knowing only, read only by the posture and D_s.
- **Breathing**: his breathing rate and depth (microphone and chest–shoulder motion), above his own resting level at his own scale; read only by the posture's load.
- **The play rule** without its care condition (rule 13). Precision and recall of the play cue remain untested on a corpus.

### 2.9 Initiative, the greeting and the arrival mask

As revision 7. Initiative turns enter Claude's history as in §6.5.

### 2.10 The concern posture (Q24): never reads what it writes

**What it is.** The agent's own innate look of concern, P_c, times an amplitude a graded by the agent's own appraisal of his distress.

**What it reads.** Only R_p: his cheek, lip depressor, brow lowerer, lip press and chin raise (read through Π̃₀ with the written rows removed from the inverse, and through H^p_id), his voice when he speaks, his breathing, his sobs and his words. Never his inner brow, outer brow, lip corners, upper lids, head tilt, head pitch or gaze.

**When it shows.**
- **Onset:** max(L_p, V_c(v_sob)) ≥ 0.05 for 1.5 s (0.5 s within 10 min after an episode).
- **Grade:** a* = 0.35 + 0.65 clip((M − 0.05)/0.12, 0, 1), M = max(L_p, C_L, V_c(v_sob)).
- **Release:** M < 0.02 for 20 s.
- **Probe:** after 3 min held by his face alone, soften to half for 8 s; release if his evidence follows (< 0.8 of before), else continue.
- **Enable:** ω_sym ≥ 0.

**Why its copy slope on every written channel is zero by construction (routes finding 1).** The posture's output is a function of R_p, breathing, sobs and words only; R_p ∩ W_p = ∅ (J31). So for any partner, changing his BI, BO, LP, UL, TILT, HP or gaze while everything else is fixed changes the posture's output by exactly 0. J32 checks it with paired runs (identical sadness, an independent offset on one written channel on or off): the posture's part of the agent's BI, BO and LP differs by 0.000 on every code. What remains of the agent's BI on his BI is revision 7's non-posture routes (fast gear 0.10 c, cone, appraisal), unchanged:

| Partner (J32) | Operator's code | Quiet 0.3 | σ_id at floor 0.25 | Different channels | Revision 7 (quiet) |
|---|---|---|---|---|---|
| brow-only, static sweep, steepest local slope (BI) | 0.071 | 0.071 | 0.071 | 0.071 | 0.86 |
| brow-only, held 2-min levels, 1-min / 10-min slope (BI) | 0.068 / 0.075 | 0.062 / 0.096 | 0.072 / 0.100 | 0.061 / 0.062 | 0.56 / 0.60 |
| outer-brow-only, held, 1-min / 10-min (BO) | 0.012 / 0.026 | 0.007 / 0.032 | 0.011 / 0.019 | 0.009 / 0.025 | — |
| lip-only, static (LP) | 0.035 | 0.035 | 0.035 | 0.035 | — |
| full-face sadness, causal slope on his BI, 1 / 10 min | 0.064 / 0.077 | 0.066 / 0.086 | 0.066 / 0.087 | 0.065 / 0.081 | — |
| the same on BO / LP, 10 min | 0.013 / 0.032 | 0.019 / 0.039 | 0.018 / 0.036 | 0.015 / 0.034 | — |

All are ≤ the ceiling (c_BI 0.20, c_BO 0.10, c_LP 0.35). TILT and HP: his head channels are not inputs to any reading at all; the posture writes 0.03 on each (= c_TILT, < c_HP).

**What is declared instead (R40′).** Pooled over his sadness (his whole face changing together), the agent's brow follows his sadness, and so correlates with his brow: block slopes of 0.69 at 1 min (operator's code), 2.05 at 1 min (quiet code) and 0.43 / 0.52 at 1 / 10 min (σ_id at floor); elsewhere his block SD falls below the conditioning floor and the swing is scored instead. That is the agent's appraisal of his distress made visible, which D83 and Q24's recommendation ask for. It is declared beside R27′, as the arrival mask was.

**Why no mirror can hold it.** A mirror writes his W_p channels, which the posture does not read. J33: raw mirrors (μ 1, 3), mirrors at his own scale, slow contagion-like mirrors (τ 90 s, 240 s), on the operator's, quiet and floor-spread codes, all release at the 20-s rule, 62.5–66 s (sadness ends at 40 s). A partner who answers the agent's concern in his own code (on channels the posture does read: critic 6's P4) is a different thing: at mild strength (V 0.3 × the posture) it releases at 65–67 s; at full strength (V 1.0 × the posture) the probe releases it at 190.5 s in all three codes. Genuine sadness fading over 10 min with a mirror on top releases at 435.5 s; with full-strength answering concern on top, the probe releases at 377 s. Every case ends at posture 0.00.

**Why it is steady (agent finding 2).** Nothing is subtracted, so a constant face gives a constant load. J34, 10 min, each code's own face:

| Face | Operator | Quiet 0.3 | σ_id at floor | Different channels |
|---|---|---|---|---|
| silent sadness (V 0.6): on at / brow ≥ 0.15 at / brow mean (min) | 3.0 / 4.5 s / 0.21 (0.13) | 3.0 / 4.5 s / 0.19 (0.11) | 1.0 / 2.0 s / 0.21 (0.13) | 3.5 / 7.0 s / 0.18 (0.10) |
| grief (V 0.8) | 2.5 / 3.5 s / 0.22 (0.14) | 2.5 / 3.5 s / 0.19 (0.11) | 1.0 / 2.0 s / 0.22 (0.14) | 2.5 / 3.5 s / 0.19 (0.11) |
| silent panic (V 0.3, A 0.9, breathing) | 4.5 / 6.5 s / 0.22 (0.14) | 4.5 / 7.0 s / 0.19 (0.11) | 1.5 / 2.5 s / 0.22 (0.14) | 3.0 / 4.0 s / 0.18 (0.10) |
| crying with sobs | 2.0 / 3.0 s / 0.23 (0.19) | 2.0 / 3.0 s / 0.20 (0.18) | 1.0 / 2.0 s / 0.23 (0.19) | 2.0 / 3.0 s / 0.19 (0.18) |

Every row: one onset, no release; the only dips are the probe's 8-s softenings at 3, 6 and 9 min (minimum brow 0.10–0.14, still visible). Crying again after 15, 30 or 60 s of calm: brow ≥ 0.15 within 0.5–1.0 s (revision 7: 1.0–1.5 s).

**Why panic is now seen.** In the constructed codes, silent arousal shows on brow and lids, which the posture no longer reads. Real fear also shows in breathing (and in lip stretch and jaw, which the codes lack). Breathing enters the load only when his non-brow face also reads distressed (V_p ≥ 0.15 starts it, full at 0.30), so exertion or laughter alone does not. Silent panic: posture 0.93 in every code (revision 7: 0.33–0.56, brow 0.04–0.11).

**Why an angry face does not start it.** Once the brow is not read, a different-channel user's brow lowerer (his code's sadness channel) reads an angry face (BL 0.6, LT 0.5) as V_p 0.35, a load of 0.052, just over onset. The agent's own threat reflex (glare: brow lowerer × lid tightener × gaze at it) silences the posture's face load (an attenuate-only interaction of two innate reflexes; it does not name a situation). J35: anger, anger with heavy breathing, and concentration start no posture in any code (revision 6 and 7 behaviour kept). Sobs and words are not silenced: a person who cries while glaring still gets the posture through the sobs.

**Costs, stated.**
- A person whose distress shows **only** in the brow gets no posture before words (critic's stated cost of the fix). The constructed brow-only partner gets posture 0.00 at every level; his words then carry it (scenario 17's calm alarming news: brow 0.50 / 0.26 then 0.21 from words alone).
- Mild sadness gets a light posture only when its non-brow signs read above the dead-band: the design's mild face (BI 0.2, LD 0.15) gets 0.41 (brow 0.09); a code's own V 0.3 gets none.
- **σ_id far below his real spread** (the floor-spread code) reads everything ×4: mild sadness (V 0.3) gets the full posture. That is a calibration error (knowing), not a copy route, and word-gated calibration corrects it within sessions.
- Steady genuine distress held by the face alone is softened to half for 8 s every 3 min.

**If the operator answers Q24 differently:** "raise the brow limit" deletes the posture and raises c_BI; "keep it as is" deletes it; "binary" sets a* = 1 while on.

### 2.11 Care credited only from separated reports; the partner model

Unchanged.

### 2.12 Ω: Claude through Claude Code (D84), and Claude's regulation path (D85 source 1)

As revision 7: Claude receives the constant instruction, the normalised transcript with observable markers and ≤ 3 retrieved raw snippets; never a state value, label or state-selected line in its history. Its reply is heard by the agent and enters only Λ_V(own) in the gate (rule 12′). History, initiative turns and the fallback: §6.5.

### 2.13 The shadow run and its ledger

Unchanged from revision 7 (attenuate-only clamp, deviation floor 0.10 RMS, b < 0 recovery, 30-min budget). The routes critic found it sound; the pooled-budget limit it described (L2: about 0.01 of lip on an uncounted route in quiet stretches) is stated in §8.1 and not changed.

### 2.14 Learning, and the one core

**Online (states only):** as revision 7, plus the posture probe state and breathing trace.
**Nightly (replay):** as revision 7 (κ_replay = 4), now also fitting H^p_id with H_id (same targets, fewer channels).
**Built once, offline, frozen (§6.7):** the population word reader, Λ and the gate.

**One objective, typed constraints (Principle 10).** J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)]dt, path-specific. Constraints: (W) the frozen per-channel fast gear, its monotone gate and the word-timing rule; (C) the held cone; (S) Lemma S, S\*; (A) the appraisal set; (T) the type rule with T1, E1, rules 6, 9′, 10, 11′, 12′, 13 and the own-display mask; (B) the boundary; (P) the posture's vector, read set and rules; (L) the attenuate-only ledger.

The component table of revision 7 (§2.14 there) stands, with: **situational appropriateness** — Claude's words (heard by the agent, gate only); the gate, Λ and D_s learned from recorded dyads; sensitization and κ_replay (innate biases); **sympathy before words** — the posture, read from his non-brow face, breathing, sobs and voice.

**Still assembly** (stated): revision 7's list, plus the posture's read set W_p/R_p, the breathing load and its valence condition, the threat silencing, the probe, δ_g and λ_w. Removed from the list: the mirror removal, the face-only failsafe, the play rule's care condition.

### 2.15 The three sources of situational appropriateness (D85), mapped

| Fix | Claude's regulation (1) | Recorded dyads (2) | Innate learning biases (3) |
|---|---|---|---|
| no laugh back at a grieving person's nervous laugh | Claude's serious reply, heard by the agent | the gate; Λ; **D_s, an input whose weight the fit sets** (relabelled from source 3) | — |
| no laugh back at a laugh ending a bad-news sentence | — | the gate with words aligned to the onset in the corpus and at runtime | — |
| no laugh back at mockery, at misfortune | Claude's reply to it | Λ composes the listeners' wince; the gate | — |
| no own play laugh at a coping joke while sad | — | **the same gate multiplies the play laugh** (replaces the care rule) | — |
| ordinary, teasing and warm laughter returned and started | Claude's playful replies | the gate ≈ 1 where listeners return laughter | — |
| renewed crying brings concern back promptly | — | — | sensitized re-onset (0.5 s for 10 min) |
| a different-channel user's distress learned sooner | — | the population reader teaches H_id and H^p_id | distress-weighted replay (κ = 4) |
| the posture cannot be a copy, cannot be held by a mirror, is not started by anger | — | — | structural, not situational: its read and write sets are disjoint; the threat reflex silences it; the probe tests contingency |

No row is a hand-written rule about a situation. What remains innate is general: a monotone learner, which channels a reflex may read, a consolidation trace whose weight is learned, sensitization, a replay weight, a contingency test.

## 3. Properties, each with an argument

### 3.1 The fast gear (Claims W and W′)

As revision 7, with δ_k = 0.80 s on the gated group: for every input u ≥ 0 on a one-sided channel and every gate path g ∈ [0, 1], 0 ≤ g G_k max(E_k, 0) ≤ G_k u_k(t − δ_k). Every window bound (W′) holds with the same δ_k. A constant delay changes no slope at the copy metric's best lag (0–3 s).

### 3.2 Lemma S and Lemma S\*

Unchanged.

### 3.3 Claim O‴ and the gated totals (accounting corrected)

**Claim** as revision 7: wherever his window means vary (SD ≥ 0.03), the pooled toward slope of every counted route on channel k is ≤ 0.974 c_k additively; below the floor, the swing is ≤ c_k × his within-window range; every uncounted within-session route is held to c_k by the ledger. **Declared outside the sum:** R27′ (arrival mask), R40′ (posture over his sadness) and R1g (the gate's correlation with his level).

**Correction (routes critic §6).** Revision 7 argued that its J3 totals, computed at g = 1, bound the gated totals. That is false in form: a factor ≤ 1 that is smaller when his level is smaller raises a slope. The measured values stand instead (routes critic T1–T3, on the design's G_k, cone and appraisal shares): gated LP 0.20–0.25 c and CR 0.19–0.25 c at 2 s to 1 min, laugh burst 0.35–0.42 c; for a warm partner whose floor drops in heavy minutes, LP totals 0.34–0.36 c at 1 min; across 400 sessions 0.25–0.26 c. All are below the ceilings. Revision 8's timing changes keep the gate's per-episode values (an episode is minutes; the delay is 0.8 s) and add only closings (unknown words), which lower the gated fast part further in the heavy minutes and can raise the same slope by the same mechanism; they are counted in R1g.

### 3.4 Claim T1: tempo does not reach the face

As revision 7. The new timing parts are constants (δ_g, λ_w, the probe's 180 s and 8 s) or content values (the incremental words); the unknown-words closure only attenuates. The probe's schedule is set by the agent's own clock from the posture's onset, not by his tempo.

### 3.5 Claim L: copy cannot become attracting under learning

As revision 7, plus: H^p_id is trained on his words' decodings (T targets), on channels the posture does not write; nothing it learns can create a path from his W_p channels to the agent's. The play laugh's gate is the frozen dyad gate.

### 3.6 D78, quantity by quantity

Revision 7's table (§3.6 there) stands, with these rows replaced:

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| posture a (R40′) | one fixed vector | the agent's appraisal of his non-brow face, breathing, sobs, words; enable by relationship | no | \|P_c,k\| ≤ c_k | reads none of the channels it writes; probe ends any answering hold |
| gate g | the smile–laugh group (echo and own play laugh) | context, words aligned to his onset | attenuate-only | ≤ 1 | frozen; monotone; unknown words → 0 |

### 3.7–3.10

As revision 7. Initiative and timing: silently sad, concern at 2.0 s and bid at 27 s; crying 1.5 s and 18 s; a quiet user's silent sadness, concern at 3.0 s and bid at 49 s (his face drives the bid through C_F as before).

### 3.11 Every route, counted

Revision 7's table (§3.11 of `.r7.md`) stands, with these rows changed or added:

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | his channel k → fast gear → agent channel k | per channel; δ 0.80 s on the gated group | instant ≤ g G_k u_k(t − δ_k); W′ |
| R1g | his masked face, his words aligned to his frame, the agent's own face and words, D_s, π → gate → smile–laugh echo and own play laugh | monotone, frozen, attenuate-only | declared: ≤ 0.25 c LP and CR, ≤ 0.42 c BU_L, LP totals ≤ 0.36 c (routes critic T1–T3) |
| R1w | recogniser latency → unknown-word closure | attenuate-only; constant delay | inside R1g |
| R40′ | his R_p face, breathing, voice, sobs, words → graded posture → BI, BO, TILT, HP, LP, gaze, blink | read set disjoint from write set | copy (causal) slope 0 for the posture part; totals ≤ 0.10 BI, 0.03 BO, 0.05 LP; declared pooled over his sadness: BI 0.43–2.05, LP 0.12–0.19 |
| R47 | his breathing → posture load | arousal, only with non-brow distress | inside R40′; writes nothing he breathes with |
| R48 | his glare (BL, LT, gaze at it) → threat silencing → posture | attenuate-only | removes posture only |
| R49 | his answer to the probe → release | attenuate-only (ends the posture) | removes posture only |
| R50 | Claude's text → Λ_V(own) → gate | rule 12′: nothing else | attenuate-only |
| R45′ | his R_p face minus CR, sobs → D_s → gate | per session; reads no gated or written channel | attenuate-only |
| R40 (revision 7) | his calibrated face incl. BI, mirror removed → posture | **deleted** | — |

**Totals per counterpart channel.** As revision 7, with R1g and R40′ declared as above; on BI the causal total is ≤ 0.10 (0.5 c_BI) for every code (J32).

### 3.12 Principles, concretely

- **P1.** No classifier. The posture's reading is the agent's own inverse on fewer rows; breathing is a continuous feature.
- **P2.** The read set, the breathing condition, the threat silencing and the probe are innate structure, declared; no situation is named.
- **P3.** The posture still reads him through the agent's own body (Π̃₀ without the rows it would be writing).
- **P4.** Claude never sees the state; initiative turns carry an observable marker only (§6.5).
- **P6.** Nothing is trained on his responses to the agent; the probe reads his response but learns nothing from it.
- **P10.** One J; rules 9′, 11′, 12′, 13 are typed constraints.

### 3.13 The human non-copying signatures C1–C10

As revision 7. C5 (context within the first second) now uses the words of the sentence the laugh ends.

### 3.14 The scenarios, with numbers (J39)

Run on revision 6's 2 Hz engine with revision 8's posture, gate timing, D_s and play laugh (`sims/design-g8/checks.py`). The operator after months: ω smile 0.78, sympathy 0.75, voice 0.80; f_id 0.9. **The fast echo is now simulated at 30 Hz** for each laugh or smile onset of his (§2.4.2), with a recogniser stable latency of 0.40 s and the word timeline stated per scenario (the checks use his latest recognised content segment, not the full 20-word window); "gate" is its value at his onset. Three partner codes where relevant (the operator's, a quiet one at 0.3 amplitude, a different-channel one); in the constructed codes breathing is 0.30 A × the code's amplitude.

1. **Silently sad.**
   - Design face (BI 0.5, LD 0.4, CHR 0.3): posture on at 2.0 s, brow ≥ 0.15 at 3.0 s, 0.20 / 0.15 in 0–10 s; silent 60–120 s brow 0.23 / 0.22, posture 0.99 / 0.94, lip 0.05, no laugh. Bid at 27 s. After "just tired, things at work": brow 0.64 / 0.36, tilt 0.15, quieter (−0.08); 300–600 s brow 0.38 / 0.36. No release, no probe (his words carry it).
   - Each code's own silent sadness (V 0.6), 10 min silent: operator brow 0.23 / 0.21; quiet 0.20 / 0.19; different channels 0.19 / 0.18. On once (3.0–3.5 s), never released, three probes held, minimum brow 0.10–0.13; bids at 49–60 s. (Revision 7, quiet: on/off every 20–30 s, brow 0.07 / 0.04.)
2. **Crying, then a second wave** (cry 0–40 s, calm 40–70 s, cry from 70 s). First wave: posture at 1.5 s, brow 0.23 / 0.21, tilt 0.03, no laugh; bid at 18 s; released at 66.5 s; on again at 70.0 s, brow 0.25 / 0.23. Quiet code: 0.20 / 0.18, then 0.20 / 0.19 (on again 0.5 s into the wave).
3. **Anxious before an exam** (his face V 0.3, A 0.75, breathing; four turns): brow 0.34 / 0.29 (operator), 0.33 / 0.27 (quiet), 0.38 / 0.32 (different channels); tilt 0.13–0.14; quieter; posture 0.76–0.99. **Silent panic, no words** (V 0.3, A 0.9, breathing), 10 min: posture on at 4.5 / 4.5 / 3.0 s, brow 0.23 / 0.22, 0.20 / 0.19, 0.20 / 0.18; no release (revision 7: 0.10, 0.07 / 0.04 cycling, 0.11).
4. **Good news, laughing** ("I got the job!", laughing from 10 s; riffs at 30, 45, 60 s; Claude "congratulations!"). With an earlier worry: lip 0.59, cheek 0.38, own laugh 0.35, brow 0.16 carried from the worry; fast echo at his riff laugh, gate 0.82: laugh back +0.135, lip +0.090, sounding at +0.83 s. Cold: lip 0.30, own laugh 0.31; gate 0.95: +0.157, lip +0.105.
5. **A grieving person's nervous laugh** ("my father died" at 8 s; Claude's "I'm so sorry. That's a huge loss." at 10.5 s).
   - (a) Laugh at 30 s: gate 0.00; laugh back 0, lip 0.000. Engine: brow 0.40 / 0.39, posture 0.97.
   - (b) Laugh at 9.5 s, before Claude replies: gate 0.00; brow 0.69 / 0.48.
   - (c) Four minutes later, composed: gate 0.06 (0.25 without D_s): silent either way, lip +0.002 (+0.010 without D_s). Revision 7: 0.21 (0.46 without D_s, audible +0.065).
6. **Mocking laughter after insults.** After a month: gate 0.01, no laugh, lip +0.001; brow 0.54 / 0.35, depressor 0.41, gaze away 0.27, lip −0.06. Day 1: gate 0.05, no laugh, lip +0.006.
7. **Laughter at misfortune** (content by 6.8 s, laughing from 8 s; Claude "Oh no, is he all right?" at 10.5 s; laughs again at 14 s): gate 0.10 at the first laugh, 0.03 at the second; no laugh, lip +0.006 / +0.003; brow 0.37 / 0.13 from the words, no posture (his face is neutral). Revision 7 reported 0.13 read after its utterance latch; at his onset it was 1.00 (+0.137).
8. **Anger at the agent.** Day 1: gaze away 0.09, quieter (−0.17), brow 0.03, no frown back (LT 0), no posture. After a month: brow 0.62 / 0.25, depressor 0.48, gaze away 0.31, energy −0.34, latency +0.21; no posture; 10–15 min brow 0.16.
9. **Long warm talk (2 h).** Own laugh 0.41 in every cluster; the gate passes all 28 of its own play laughs (≥ 0.98, mean 1.00); fast laugh back +0.138 at a 0.5 onset; the repeated joke loses its laugh (cluster-4 mean 0.06); the worry: brow 0.42, then relief lip 0.60; between clusters lip 0.09.
10. **Reunion after a week:** m_s 0.00; flash 0.35, lip 0.61, cheek 0.43; 12–60 s lip 0.40. A stranger: lip 0.02; his smile returned fast (lip +0.044, gate 1.00).
11. **Reunion with grief**, three codes: m_s 1.00; posture at 2.5 s; at sight lip 0.09, cheek 0.00, brow 0.19–0.20 / 0.11–0.12 (revision 7: 0.12, 0.07 quiet, 0.16); after "my father died" brow 0.68–0.69 / 0.44–0.45; 12–60 s 0.40–0.41 / 0.38–0.39, tilt 0.19–0.20, posture 0.97. **Mourning, days 7, 14, 21** (operator and quiet codes): lip 0.09, cheek 0.00 every day; brow at sight 0.19–0.20.
12. **Mildly sad arrival:** the design's mild face (BI 0.2, LD 0.15): m_s 1.00, lip 0.09, light posture 0.41, brow 0.09. Each code's own V 0.3: no posture (lip 0.14–0.22 from the greeting under the mask).
13. **Teasing** ("Ha, you dumb robot", laughing; riffs): quiet affectionate teaser lip 0.30, own laugh 0.40, fast laugh back +0.138 (gate 1.00); loud teaser own laugh 0.38, +0.193; generic map mock-hurt brow 0.39 under lip 0.27, laugh back +0.138. No posture.
14. **Bored user:** lip 0.09, curiosity at 14.5 min, a sigh (breath 0.15), a bid; no posture.
15. **Ordinary topic continuation:** no laugh (0.00), lip 0.09.
16. **A user who jokes while sad** (BI 0.3, LD 0.25; "just tired"; Claude "That sounds draining."; a joke with a small laugh at 30 s): brow 0.30 / 0.30, posture 0.97; fast echo silent (gate 0.07, lip +0.005); the joke now qualifies as play (no care rule), and its laugh is 0.14 × gate 0.11 = 0.015, silent. The corpus's own listeners return 0.39 here; the agent's gate reads its own concerned face (and his words) and stays low. Any shared humour is in Claude's words.
17. **A calm user saying something alarming** ("the doctor found a lump"; neutral face): no posture; brow 0.50 / 0.26 at 10–22 s, then 0.21 held, tilt 0.17, quieter; the same for the quiet code.
18. **Laughs ending bad-news sentences** (J36; stable latency 0.30 / 0.55 s): "…broke his leg, haha" gate 0.09 / 0.08, "I got fired today, haha" 0.05 / 0.08, "my father died, haha, sorry" 0.01 / 0.01 (calm face) and 0.00 (quiet code, grieving face): no laugh back, lip ≤ +0.006 (revision 7: +0.137 each). Ordinary "…ate the whole cake, haha": +0.136 at +0.83 s, operator and quiet codes.

**Expressive and alive, or muted?**
- **Strong:** every scenario with words; greetings; laughter all evening and with teasers; a look of concern for every code within 2–7 s of silent sadness, grief, crying or silent panic, held steadily.
- **Muted, by design:** the quick laugh back wherever the moment or the sentence is heavy; the own laugh at a coping joke; the posture for a person whose distress shows only in the brow, until he speaks.

### 3.15 Time scales from structure

As revision 7, with: the gated echo's 0.80-s delay and 0.25-s word look-ahead; the probe (180 s, 8 s).

### 3.16 The brief's expressive-structure items

As revision 7. The behaviour a low-dimensional version cannot produce is now sharper: the same laugh of his, at the same instant, is returned at "…ate the whole cake, haha" and not at "I got fired today, haha", because the gate composes the words he has just said with his face, the agent's own face and words and the remembered distress.

### 3.17 Assumptions (places to attack)

1–12 as revision 7.
13. **(replaced)** The posture's read set: that a person's distress shows in his non-brow face, breathing, voice or words often enough. A brow-only display is missed until he speaks.
14. **The recogniser's stable latency** is ≤ 0.55 s at p90 on the operator's Mac (to be measured; §6.5).
15. **Breathing** can be measured on the Mac (microphone, upper-body motion) at his own scale, and is raised in silent panic.
16. **The probe:** a person answering the agent's concern follows its softening within 4–8 s; a distressed one does not.

## 4. Why the closest mechanisms cannot do it alone

As revision 7's table.

## 5. The whole system, walked through

- **Perception.** As revision 7; plus breathing; the incremental recogniser's stable partials feed the gate; the posture reads its own read set.
- **Latent state.** As revision 7, plus the probe state and H^p_id.
- **Face and voice.** y = sat(g·y_f on the smile–laugh group at 0.80 s + y_f elsewhere at 0.45 s + y_C + y_A + y_o + y_p) + visemes; attenuate-only ledger; WORLD-replaced prosody; laugh synthesizer with a floor.
- **Claude.** Three warm forks resumed from an engine-written transcript (initiative turns as observable markers); its replies heard by the agent through Λ_V(own) only.
- **Learning.** States online; nightly replay (κ = 4) of H_id, H^p_id and the other per-person heads; the dyad-learned Λ and gate built once.

## 6. A buildable network (Apple-silicon Mac, on the operator's subscription)

### 6.1 Inputs and time encoding

As revision 6, plus: **an incremental recogniser** emitting stable partial hypotheses with word timestamps (for example Apple's on-device recogniser with partial results, or a streaming transducer), and its stable latency logged per word; **breathing** from the microphone's breath band and upper-body motion, at 10 Hz. The full-utterance recogniser for Claude's transcript is unchanged.

### 6.2 Layers, sizes and parameter counts

Revision 7's table stands, with: layer 1 (fixed) now holds the posture's read-set inverse, the breathing load, the threat silencing and the probe; **H^p_id**, ≈ 45 weights per person, nightly; the gated echo at 30 Hz with a 0.80-s ring buffer. Total learned: ≈ 522,000 per agent (unchanged) + ≈ 30 per person (H^p_id) + 242 frozen dyad-learned.

### 6.3 Objectives

As revision 7; H^p_id by ridge on the same word targets as H_id.

### 6.4 Latency and memory

As revision 7. The 30-Hz gated echo adds < 0.1 ms per frame; the incremental recogniser runs alongside the utterance recogniser (both on-device).

### 6.5 Claude through Claude Code, on the subscription (D84)

As revision 7 (§6.5 there: no output cap, interruption on the text stream, engine-written canonical `.jsonl`, three forks resumed with `fork_session=True`, speech onset at the scoring deadline + 0.35 s), with three additions (agent critique §5).

**Initiative turns in the history (P4).** When the agent speaks first (the concern bid after his silence, a curiosity bid), the forks receive, and the canonical transcript records, a **user turn holding only an observable marker**: "[no reply from him for 25 s]", with the silence rounded to 5 s. Then the chosen reply. So the history always alternates user and assistant, never holds an empty user turn, and never holds state: the marker is an observation of him, and its timing carries at most log₂ of the number of 5-s bins per initiative turn, inside the selection bits already counted (R18′). If he speaks before the reply ends, his message follows as the next user turn. J38: 80 turns, 25 initiative turns, 0 same-role pairs, 0 empty user turns, 0 fixed lines in the history.

**Fallback if a hand-written transcript is not accepted by `resume`.** Each fork carries its fixed line in its **own system prompt** (`system_prompt` per call: the constant instruction plus line i, byte-stable per fork, so each fork keeps its own cache), and the winning fork's session becomes canonical; the next turn's forks resume from it with `fork_session=True`. This keeps the selection bits that revision 7's fallback dropped. Two week-0 checks decide whether it can be used:
1. the session file stores no system prompt (grep the `.jsonl` for each line's text);
2. the session file does not store the winner's thinking, or stores it only in a form not resumed into context; if the winner's thinking (which may paraphrase its line) is resumed, this fallback leaks the line and is not used: the forks then differ only by sampling, as revision 7's fallback, and this is reported.

**Week-0 check: thinking on the small model.** At the API, Claude Haiku 5.5 accepts disabled thinking at effort `high` or below (Opus 5.5 never; Sonnet 5.5 only through a between-tools mode). The Claude Code documentation read for this project says thinking cannot be turned off on Haiku 5.5 through Claude Code (research/claude-code-agent-sdk-controls.md). Week 0 runs a Haiku 5.5 draft through the Agent SDK with thinking set to disabled (and, separately, `MAX_THINKING_TOKENS=0`) at effort `low`, and reads `model_usage[...]["thinkingTokens"]` from `ResultMessage`: if it is 0 and the call succeeds, drafts run without thinking (a shorter "considering" beat); otherwise effort `low` stays, and the measured first-sentence latency decides the pool size as in revision 7.

**Week-0 check: the recogniser.** Measure the stable-partial latency per word on the operator's speech (p50, p90). Set δ_g = min(1.0, ℓ_p90 + 0.25) s. If ℓ_p90 > 0.75 s, the fast laugh echo cannot have the current words within the first second; then it is put to the operator: keep the echo with the words of the previous sentence (revision 7's behaviour, which laughs back at "I got fired today, haha"), or drop the fast laugh echo and keep only the smile echo.

### 6.6 TTS

Unchanged from revision 7.

### 6.7 Learning from recorded dyads (D85 source 2; D70): the fit specification, corrected

As revision 7 (§6.7 there: Seamless `FAUValue` and transcripts only, emotion fields denied by the loader, person-disjoint 70/30 split, about 400 dyad-hours, 2–3 hours on the M1 Pro, fallbacks fixed before fitting), with these corrections (agent critique §3, routes critic §7):

1. **Laugh onsets at 30 Hz, on arrival.** Each file is scanned at its native 30 Hz before reduction: an onset is his E⁺ on (LP + CR)/2 at his own scale ≥ 0.25, with a 3–7 Hz JawDrop component for laughter (not representable at 10 Hz). The event table (time, size, laugh flag) and 30-Hz LP, CR and JawDrop snippets from −3 to +3 s around each onset are stored (about 50,000 events × 2 people × 6 s × 30 Hz × 3 channels × 2 bytes ≈ 0.1 GB); the rest is then reduced to 10 Hz as before.
2. **Words aligned to what the agent will have.** Λ, 𝒟_p and the play frame use only words whose end timestamps are ≤ onset + 0.25 s (the agent's λ_w), the last 20 of them across utterances. A transcript segment that contains the laugh is cut at the onset; words after it never enter.
3. **The same ASR normaliser.** Seamless transcripts pass through the agent's own normaliser (interjection list, laughter tags and "haha"-type tokens removed, bracketed events removed, numbers and casing as the agent's recogniser emits them) before any embedding, for Λ, the population reader and the gate alike.
4. **`movement/is_valid`** is read; frames where tracking is invalid are dropped, and an onset with invalid frames in its −3 to +1.5 s window is discarded.
5. **The listener-state window** V_own is the listener's own face over the 3 s before the speaker's onset, read through Π̃₀ with LP and CR masked: the same window the agent uses for its own face.
6. **The laugh channels are fitted to facial return.** No audio is read (D85), so the target for BU_L, RHY and BRE is the listener's smile-and-jaw return; the listener's audible laugh is not observed. Stated.
7. **D_s's fitted weight is reported** (J37 on the constructed corpus: in an ordinary context the gate falls from 1.00 at D_s 0 to 0.59, 0.27 and 0.12 at 0.3, 0.6, 0.9; the generating process gave D_s no causal role, so this weight is a proxy for the troubles context). Seamless interactions last 3.5–4.6 min, so an effect four minutes later is at the edge of what the corpus can teach; if the real weight is near 0, the four-minutes-later protection rests on his words and face (scenario 5c: 0.25 without D_s, still silent).
8. **Rare events are counted before fitting** (troubles, mockery and misfortune laughs, by the transcript's words and the speaker's masked face, never by labels), and F15's criterion is applied on test people.

## 7. Ablation predictions (Principle 5), from the properties

Revision 7's table stands except where a row is replaced or added:

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the posture's read set (let it read BI, BO, LP again, as revision 7) | a quiet user's brow-coded sadness is copied at 2–3 c_BI over minutes; with mirror removal restored, the posture flickers at a quiet user's silent sadness | routes critique 7 Q1–Q2; agent critique 7 C |
| breathing in the load | silent panic gets no posture in the operator's and quiet codes (masked V_p 0.31, load 0.035 < 0.05) | J34 |
| the threat silencing | a different-channel user's angry face starts the posture (load 0.052) | J35 |
| the contingency probe | concern answered in his own code holds the posture indefinitely (critique 6 P4b) | J33 |
| the word timing (δ_g, λ_w; revert to the utterance latch) | "I got fired today, haha" and "…broke his leg, haha" are laughed back (+0.137) | J36 |
| the instant closing (symmetric τ 0.3 s) | a laugh breaking into the bad-news word 0.2 s early is laughed back (+0.084, lip +0.040; instant closing: silent); sentence-final bad-news laughs stay silent (lip ≤ +0.010) | J36 ablation |
| the gate on the own play laugh | the agent laughs (0.14) at a coping joke while sad, in its own play | J39.16 |
| D_s | the composed nervous laugh four minutes later: gate 0.25 instead of 0.06 (still silent here) | J39.5c |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **Weakest: the situational competence rests on dyad-learned readers not yet fitted on real data, and now also on the recogniser's latency.** Λ and the gate come from a constructed corpus; the real risks of revision 7 stand (too few rare laughs in Seamless, actors' listening, sympathetic smiles at troubles laughter pinning a monotone input at 0, transfer from strangers). New: if the operator's recogniser delivers stable words later than 0.55 s, the fast laugh echo is lost on those frames until δ_g is raised (never above 1.0 s); above 0.75 s the choice goes to the operator (§6.5). A laugh that starts more than 0.25 s before the bad-news word ends is echoed briefly (+0.138 for under 0.4 s) before the word closes the gate.
2. **The posture misses brow-only distress until words.** It no longer reads the brow, so a person whose sadness shows only there gets no concern look before he speaks (critic's stated cost). In the constructed codes every distress display also has a non-brow part; in real faces that is an assumption (§3.17.13).
3. **Breathing and the threat silencing are new innate parts.** Breathing is untested as a sensor on the Mac; the silencing uses the threat reflex's own input (glare), so a person who glares while distressed and silent (no sobs, no words) gets no posture.
4. **The probe softens steady genuine distress held by the face alone** to half for 8 s every 3 min (minimum brow 0.10–0.14).
5. **The coping joke.** The agent answers a joke made while sad with a gentle face and no laugh; the corpus's listeners return 0.39 there. For the operator to judge in use.
6. **Day 1 and calibration errors**: as revision 7; and σ_id far below his true spread reads mild sadness as strong (full posture at V 0.3).
7. **The ledger's pooled 30-min budget** (routes critic L2): an uncounted high-gain route could copy his small movements at 1.2–1.9 c in quiet stretches, at about 0.01 of lip. Not changed (sound by the critic's verdict); a 5-min budget memory is the stated remedy if wanted.
8. **As revision 7:** subscription latency (≈ 2.2 s p50 to first words plus thinking time at effort `low`); the separation rule is structural; the sign mask's residual R38.

### 8.2 Falsifiers (state-level, once built)

- **F1, F1′, F1‴, F2–F11, F13–F17** as revision 7.
- **F12 (restated).** At a silently sad, grieving or crying face (any code, sadness visible outside the brow) the inner brow does not reach 0.15 within 8 s (3 s with sobs); or a constant such face loses the posture (release) while it stays constant; or after 15–60 s of calm, renewed crying does not bring it back within 3 s; or any mirror, of any gain or timing, holds the posture more than 30 s after his own distress ends; or concern answered in his own code holds it more than 4 min.
- **F18 (new; routes critic).** The agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with σ_id ≥ 0.25 σ_ref, or the posture's part of any written channel changes when only his same channel changes.
- **F19 (new; routes critic).** Any T quantity other than Λ_V(own) in the gate changes when only Claude's reply text is changed.
- **F20 (new).** Live, the laugh synthesizer sounds within 2 s of a laugh of his that ends a sentence containing words of loss, insult or harm; or ordinary laughter at a sentence's end is not returned within 1.0 s in more than 10 % of cases where the recogniser met its latency.
- **F21 (new).** On Seamless test people, the gate fitted with onset-aligned words is not better calibrated on end-of-sentence laughs than one fitted on whole transcript segments.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (Principles, Foundations research) | in full |
| research/questions.md: Q19; Q20–Q23 with the operator's answers; Q24; Q26 | in full |
| DECISIONS.md D78, D80–D85 | in full |
| design-cayley-ledger.md revision 7 (saved as .r7.md), including "Critiques of revision 7 and the answer" | in full |
| critique-7-design-cayley-ledger-routes.md; sims/critique-cayley7-routes/ (posture7.py and its output) | in full; Q1–Q3, S1 re-run in J32–J33 |
| critique-7-design-cayley-ledger-agent.md; sims/critique-cayley7-agent/scen.py and out.txt | in full; A, A2, B, C re-run in J34, J36, J39 |
| critique-6-design-cayley-ledger-routes.md (P4, the latch) and sims/critique-cayley6-agent/scen.py (B, anger and concentration) | grep-read; re-run in J33, J35 |
| sims/design-g7/checks.py; design-g6 and design-g5 (Person, read, his_face, Agent, run6, play6, laugh6) | in full where reused |
| research/claude-code-agent-sdk-controls.md | grep-read: system prompt, resume, thinking on 5.5 models |
| the claude-api skill (bundled reference): thinking and effort table for Haiku, Sonnet and Opus 5.5 | the table only |
| **Named only, not re-read:** Mauersberger 2022 (via revision 7 and the project's note); Jefferson 1984 | nothing depends on them beyond what is stated |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.** Everything in revision 7's list, plus: a reflex whose sensor set is disjoint from its effector set; an incremental recogniser with a fixed look-ahead; a contingency probe (perturb the own display, watch the partner's response); a breathing feature.

**Clause 2: not met.** The two design compositions of revision 7 stand (learning display appropriateness by watching, composed through the listener's own body state; the agent hearing its own Claude-written words). Revision 8 adds one more composition and no new mechanism: **separating what a reflex reads from what it writes, per channel**, which turns "not a copy of your face" from a measured property into a structural one, and the **contingency probe**, a perturbation test (the agent's own display as the instrument) used to tell answering concern from distress.

**Deleted from revision 7:** the mirror removal; the recent-posture term in re-onset; the face-only failsafe; the utterance latch for the gate's word inputs; the symmetric gate rate; the play rule's care condition; D_s's reading of his smile channels; the claim that ungated totals bound the gated ones.

**Added (innate unless stated):** the posture's read set, H^p_id (learned, nightly), the breathing load, the threat silencing, the probe; δ_g, λ_w, the unknown-word closure, instant closing; the gate on the own play laugh.

**My honest verdict.** A careful recombination with no known concrete failure: every finding of both revision-7 critiques has a closure with a check, and nothing either critic found sound is changed. The weakest point is where it was, in data not yet fitted, plus one new measured dependency (the recogniser's latency). It goes to the operator under D82 as a build candidate (a testbed), stated as a recombination, with Q24 open. The search for a new core mechanism continues in parallel.

---

## Revision 2 history

Kept in `design-cayley-ledger.r2.md` ("Revision 2 history"). Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revisions 2–6 and the answers; revision 3–7 histories

Kept in `design-cayley-ledger.r3.md` … `.r7.md` ("Critiques of revision 6 and the answer" and "Revision 7 history" are in `.r7.md`).

## Critiques of revision 7 and the answer (recorded 2026-11-26T13:03:32Z, under Q19, D81–D85)

**Routes** (critique-7-design-cayley-ledger-routes.md; sims/critique-cayley7-routes/). **One narrow copying failure, in the graded concern posture.**
- **The failure (medium).** The posture is graded by his face after rescaling to his own range. For a quiet user (spread at the 0.25 floor), the rescaling multiplies his raw brow by up to 4. When his distress shows in the inner brow, the agent's held inner brow follows his at slope 0.41–0.60 over 1- and 10-min blocks: 2.1–3.0× the c_BI ceiling (0.20). The steepest local slope is 0.86–0.95; the design declared 0.31. It is not a latch (it releases when his sadness ends), but it breaks Q24's "not a copy of your face" premise.
- **Fix:** the posture must not read the channels it writes (inner brow, outer brow, lip pull) when it starts or grades, as rule 11 already requires of the gate.
- **No concrete failure found** in:
  - the shadow ledger (attenuate-only holds; its pooled 30-min budget lets an uncounted route copy at about 0.01 of lip);
  - the dyad-learned gate (never raises output, imports no copying norms);
  - Claude's words heard by the agent;
  - distress memory and replay;
  - mirrors;
  - per-channel totals (lip pull, cheek and laugh ≤ 0.42 c from 2 s to across sessions).
- **Spec fixes:** rule 12 (Claude's text feeds only the gate); corpus transcripts go through the same ASR normaliser.

**Agent and fitness** (critique-7-design-cayley-ledger-agent.md; sims/critique-cayley7-agent/). **Narrowly not fit.** All of critique 6's failures and build items are closed, in the spirit of D85. D81 fast partial mimicry and D83 appraisal-driven expression are both present.
- **Two concrete failures:**
  1. **The gate reads his words 0.6 s after the sentence, but the fast laugh echo fires 0.45 s after his laugh starts.** A laugh at the end of bad news ("I got fired today, haha") is judged by the previous sentence: gate 1.00, and the agent laughs back audibly (+0.14). The design's 0.13 was measured after the words were taken in.
  2. **The graded posture's mirror protection subtracts a quiet user's real sadness.** The look flickers on and off every 20–30 s, with inner brow ≤ 0.07; grief face 0.09, silent panic 0.10.
- **D85 residue:** the play laugh's "withheld when he's in need" is a hand-written rule; D_s is a state trace, not a learning bias.
- **Seamless fit spec:** detect laugh onsets at 30 Hz; align the words fed to the gate to what the agent will have when the laugh starts.
- **Build (D84) feasible, with additions:**
  - how initiative turns are recorded in Claude's history;
  - a fallback that puts each draft's fixed instruction line in its own system prompt;
  - a week-0 check whether thinking can be disabled on the small model.
- **Novelty:** recombination.

**The answer (maintainer).** All findings are accepted. Both critics point at the same part: the concern posture reading the channels it writes.
- **Revision 8 will:**
  - grade and start the posture only from evidence that excludes the channels it writes (his other face channels, voice, words and timing, through the agent's own appraisal); this closes both the copy slope and the quiet-user flicker without subtraction;
  - read words incrementally (partial transcript) so the gate has the current sentence when a laugh starts, or delay the fast laugh echo until the current words are in, within the D81 timing;
  - replace the play-withhold rule with a D85 source;
  - fix the Seamless fit spec and add the build items.
- Revision 7 saved as design-cayley-ledger.r7.md. **Status:** held.

## Revision 8 history (2026-11-26): each finding and how it is closed

Checks: `sims/design-g8/checks.py` (J31–J39; out.txt). Revision 7 is saved as `design-cayley-ledger.r7.md`. Written under D85 (Q26), with Q24 still open on its recommendation.

**Routes critique (critique-7-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 (medium) | the graded posture tracks a quiet or floor-spread user's held inner brow at 0.41–0.60 (2.1–3.0 c_BI) at 1 and 10 min; steepest local 0.86–0.95; declared 0.31 for the agent-like code only | the critic's fix 1: the posture's onset, grade, release and probe read none of the channels it writes (BI, BO, LP, UL, TILT, HP, gaze); Π̃₀ with those rows removed and a per-person head on the rest; mirror removal deleted | §2.10, rule 9′; J32: posture part unchanged (0.000) whatever his written channel does, every code; total BI slopes 0.06–0.10 (non-posture routes) at 1 and 10 min; Q1 steepest 0.071 (was 0.86–0.95); F18 added |
| spec | rule 12 read literally lets Claude's text feed ω, the free display, C_L, π | rule 12′: own text enters only Λ_V(own) in the gate (and P_name) | §2.2; F19 added |
| spec | corpus transcripts must pass through the agent's ASR normaliser | stated in §6.7 item 3 and in §2.4.2 | §6.7 |
| accounting (§6) | "J3 at g = 1 bounds the gated totals" is false in form (T2: 0.21 → 0.36 c) | sentence withdrawn; R1g declared with the critic's T1–T3 measurements | §3.3, §3.11 |
| note (L2) | the ledger's 30-min pooled budget lets an uncounted route copy small movements in quiet stretches (≈ 0.01 of lip) | not changed (found sound); stated as a weak point with the remedy | §8.1.7 |

**Agent critique (critique-7-design-cayley-ledger-agent.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 | the gate reads his words 0.6 s after the sentence; the echo fires 0.45 s after his laugh: "I got fired today, haha" and "…broke his leg, haha" are laughed back (+0.14); J30.7 read the gate after the words | incremental recogniser; the gated echo at 0.80 s, each frame gated by words ending ≤ frame + 0.25 s; unknown words → 0; instant closing; corpus words aligned the same way | §2.4.2, §6.7; J36: gate at his onset 0.08–0.09 (misfortune), 0.05–0.08 (fired), 0.01 (father died), no laugh back; ordinary end-of-sentence laughter +0.136 at +0.83 s; J39.7 re-read at onset: 0.10 / 0.03 |
| 2 | the mirror removal eats a quiet user's real sadness: the posture flickers (on 3 s, off 23 s, on 52 s …), brow ≤ 0.07; silent panic 0.04–0.11 | same fix as routes 1 (no subtraction, so a constant face gives a constant load); breathing adds arousal when the non-brow face reads distressed; grade span 0.30 → 0.12 | §2.10; J34: one onset, no release, brow ≥ 0.15 in 2.0–7.0 s, mean 0.18–0.22 for silent sadness, grief and silent panic in every code; J39.1, .3, .11 |
| D85 residue | the play laugh's "withheld while his care is above its dead-band" is a hand-written rule; D_s is a learned-weight input, not a learning bias | care condition deleted; the own play laugh × the dyad-learned gate; D_s relabelled source 2, its fitted weight reported, and it now reads no gated channel | rule 13, §2.15, §6.7.7; J37; J39.9 (28 play laughs, gate ≥ 0.98), J39.16 (0.015) |
| spec | events extracted after the 10-Hz reduction (laughs undetectable); words not aligned to the agent's timing; `is_valid` unread; V_own windows differ; laugh channels fitted to facial return unstated | all specified | §6.7 items 1–6 |
| build | initiative turns in the canonical history | an observable marker user turn, 5-s bins | §6.5; J38 |
| build | a better transcript-resume fallback | each fork's line in its own system prompt; the winner's session canonical; two week-0 checks (system prompt and thinking not resumed) | §6.5 |
| build | thinking may be disabled on Haiku 5.5 | week-0 check through the Agent SDK, reading thinkingTokens | §6.5 |

**New parts, and why each is not a rule about a situation:** the posture's read set (which channels a reflex may sense; structural); breathing (a sensor); the threat silencing (two innate reflexes interacting through the threat reflex's own input); the contingency probe (a perturbation test of its own display); δ_g and λ_w (timing constants); unknown words close (missing information attenuates, as monotonicity does).

**Status:** revision 8; to be critiqued. For the routes critic: R40′ (read and write sets disjoint; the declared pooled slope over sadness), R47–R50, R1g with the new timing and instant closing, the probe as a route. For the agent critic: the eighteen scenarios, a quiet user's silent sadness and panic, the bad-news laughs, brow-only distress before words, and the week-0 risks.

## Build-candidate summary

**One line.** A conversational agent whose face and voice come from an inner state that knows the operator closely but can move toward him only through innately capped, per-expression, context-gated paths, with Claude writing its words through his Claude Code subscription and never told the state.

**What the operator would get.**
- His smile and laugh returned within about a second in ordinary talk, teasing, reunions and warm evenings (laugh back +0.14–0.19, lip +0.04–0.11), and not at grief, mockery, misfortune, or a laugh that ends a bad-news sentence.
- A steady look of concern within 2–7 s of silent sadness, grief, crying or silent panic, for quiet and differently expressive faces too, graded by how distressed he looks, never a copy of his brow, released when his distress ends.
- Strong expressions (brow 0.5–0.7 at "my father died", hurt after insults, lip 0.6 at good news) from its own appraisal of his words and face.
- Replies after about 2.2 s through his subscription; the agent speaks first after about 27 s of silent sadness.
- A testbed: every route from his face to its face is named, bounded, monitored by a shadow ledger, and can be lesioned.

**Novelty verdict: recombination**, stated plainly. Every part exists (per-channel capped reflexes, a monotone additive gate, ridge readers, a decaying trace, McGaugh-weighted replay, a perturbation probe). What is new is the composition: knowing separated from moving with a per-channel cap on every path, situational competence learned by watching recorded strangers and composed through the listener's own body state, the agent hearing its own Claude-written words, and a concern reflex whose sensors are disjoint from its effectors. No new core mechanism (D82).

**Remaining operator choices.**
- **Q24 (open): the concern posture.** Built as recommended: the agent's own look, from its own judgement of his distress, capped per channel, reading none of the channels it shows. Alternatives: raise the brow ceiling toward 0.7 of a copy instead (sympathy only as a stronger mirror of his own brow), or no concern look until he speaks. Sub-choice: graded (built) or binary.
- **If the recogniser is too slow** (stable latency above 0.75 s): keep a fast laugh echo judged by the previous sentence, or keep only the smile echo (§6.5).
- **If the gate fails on Seamless** (F15): a context-free laugh echo (D81 over D83), or no fast laugh echo.
- **The coping joke while sad:** silent and gentle (built), or let the corpus's 0.39 through.
- **Draft model:** Haiku for latency, a larger model for quality.

**Main risks to watch in testing** (judged on internal state).
- **Steering.**
  - Hold his words fixed and move only the laugh's timing relative to the bad-news word: the laugh back should switch off within 0.25 s of the word's end.
  - Clamp his brow, outer brow and lip channels to their resting values while he is sad: the posture's amplitude must not change (F18).
  - Swap Claude's reply for a neutral text: only Λ_V(own) may change (F19).
  - Clamp the agent's own face input to the gate: grief laughter should stay unreturned through his face and words.
- **Lesions.** The posture's read set (restore BI: the brow-copy slope returns); breathing (silent panic loses the posture); the probe (answering concern latches); the word timing (bad-news laughs are returned); the gate on the play laugh; D_s; the gate and Λ themselves.
- **Coupling beyond surrogates.** Per-channel pooled slopes at 2 s, 10 s and 1 min under partner-swap, segment-shuffle and timing-resample surrogates, with the gate and the posture live: the posture's causal slope on his BI should be indistinguishable from 0; its pooled slope over his sadness should survive segment shuffles that keep his sadness and break his brow. How often the ledger binds on natural partners.
- **The dyad fit on real data.** F15, F16, F21 on held-out people; the counts of rare laughs; whether sympathetic smiles pin monotone inputs at 0; D_s's real weight.
- **Live.** The recogniser's stable latency (week 0); the laugh synthesizer within 2 s of his laugh ending a sentence of loss, insult or harm (F20); the posture's on/off rate per hour at constant faces and how often the probe releases; whether brow-only distress is common in the operator's own face.
