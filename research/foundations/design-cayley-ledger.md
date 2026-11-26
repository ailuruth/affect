# Cayley–ledger core, revision 6: a frozen per-channel fast gear, a concern posture of the agent's own, reading each person at his own scale, and a shadow run that ledgers every route

Seventh design of the S0 cycle, revision 6. Written 2026-11-26 under:
- questions.md Q16, and Q17 as relaxed by Q19 (DECISIONS.md D80): a precise object, a convincing argument, concrete failures only;
- Q18 and its answer (D78): no single quantity runs the whole face from flat to copy; per channel, a bounded, sign-flippable, context- and relationship-set strength under an innate ceiling, never attracting;
- the operator's answers of 2026-11-26T08:41:00Z: Q20 (D81: knowing allowed, expression bounded, fast partial per-expression mimicry must stay), Q21 (D82: a design with no known concrete failure goes to the operator, novelty stated plainly), Q22 (D83: per-expression innate ceilings; strong expressions from words and face through the agent's own appraisal), Q23 (D84: Claude through the operator's Claude Code subscription);
- **Q24 (asked 2026-11-26T09:14:27Z, not yet answered).** Work proceeds on its recommendation: a separate, capped **concern posture**, driven by the agent's own appraisal that the partner looks distressed, its own pattern and not a copy, visible within a few seconds. §2.10 is that posture. If the operator answers otherwise, it is one switch (§2.10, last item).

Revisions 1–5 are kept as `design-cayley-ledger.r1.md` … `.r5.md`. Revision 5's two critiques:
- `critique-5-design-cayley-ledger-routes.md`, with checks in `sims/critique-cayley5-routes/`;
- `critique-5-design-cayley-ledger-agent.md`, with checks in `sims/critique-cayley5-agent/`.

Also read for this revision: the critiques section of `design-own-body-generative.md`, for its counterfactual-self whole-system test. Revision 6 adopts a form of it (§2.13).

**Algebra checks for this revision:** `foundations/sims/design-g6/checks.py` (J0–J16). Run `python3 -I checks.py` (numpy and scipy, about a minute); the output is in `out.txt`, 13 of 13 pass.
- The agent part executes `sims/design-g5/checks.py` unchanged (output suppressed) to reuse revision 5's 2 Hz engine, its Π̃₀ reader and its utterance embedding, then overrides what revision 6 changes.
- Where a finding came from a critic's constructed partner, the check re-runs that partner or its recipe (K1, K3, K4, K5; the critic's quiet and different-channel codes, mourning days and mild arrival).
- The checks test this design's own inequalities and constants on constructed instances. They are not evidence about behaviour or people (brief: no toy worlds). Scenario numbers in §3.14 are what the equations give for stated inputs.

**Status:** revision 6, not yet critiqued.

## 0. Summary

**What held in both revision-5 critiques, and is kept unchanged.**
- **Knowing is separated from moving.** The slow state knows his face at full rate; only expression is bounded.
- **Lemma S within a session and Lemma S\* across sessions.** The held cone is latched per session and centred at his own baseline b_id (τ_b 6 sessions; ω learns at τ_ω 60, ρ = 0.091). The routes critic found no failure in the moving baseline (lagged slopes ≤ 0.03).
- **T1, E1 and the own-display mask.** No rate codes in T; events are built from T parts only; Δ and the learned appraisal bases never weight the anger, disgust or contempt synergies.
- **The appraisal display** on a band-passed input, its reactions learned by anticipating the agent's own display (𝓛_A).
- **The cry–laugh split, the threat reflex, rule J in the cone and appraisal, K_id per person, the sigh, the hurt latch, credit only from separated reports, P_name, the three forked Claude Code drafts.**

**What changed, in eight moves** (each closes named findings; the full list is in "Revision 6 history").
1. **The fast gear is frozen, innate and strictly per channel (routes findings 1, 2, 4).**
   - The learned robust REN 𝓡_θ, its context gates and its exogenous input are deleted from the fast path. For each counterpart channel k the fast output reads only his own channel k (mirrored for lateral channels): y_f,k = G_k · E_k, with E_k = x_d − lp₄(x_d) on his channel delayed 0.45 s, and G_k an innate constant (lip pull 0.224, laugh burst 0.280, cheek 0.150, head and voice contour 0.8 c_k; 0 on zero-ceiling channels).
   - Its Jacobian on his channels is diagonal, so no agent channel collects from several of his channels, and rule J holds in the fast gear by construction: a sad brow onset returns no smile (J1; revision 5 as built: +0.074).
   - On one-sided channels only the **onset lobe** E⁺ = max(E, 0) is rendered. For any non-negative input, 0 ≤ G E⁺(t) ≤ G x(t − 0.45 s): the fast gear never exceeds a G_k-fraction of what he is doing at that instant, for any burst shape, length or rate. There is no learned block, so the critic's energy-for-area operator is not in the class (J2). The onset lobe's DC is charged honestly: r_k ≤ 0.949 G_k/c_k, measured down to 0.2-s clicks at 20 a minute.
   - **G_k is not a parameter of any objective.** No partner, mirroring or not, can move it: the critic's mirroring partner (K3) leaves G_LP at 0.224 at μ = 0, 0.5 and 0.8, where revision 5 drifted to the cap 0.350 or eroded to 0.07–0.14; the all-evening play laugh co-occurring with his punchline laughter cannot pull G_BU_L (a fit would want 0.443; it stays 0.280) (J4).
   - Context and relationship set each channel's strength through the cone (ω, sign-flippable) and the appraisal (sign-flippable), not through the fast gear. This matches the human order (designs.md gap 6): fast matching first, context effects after.
   - **Every channel's rendered total** with every route at its cap, at 2-s, 10-s and 1-min windows and the best lag 0–3 s, is ≤ 0.75 c_k measured and ≤ 0.974 c_k additively (J3; revision 5 as built: breath 2.6 c at 1 min, head pitch 6.6 c at 2 s).
2. **The word-need reader cannot learn his per-topic faces (routes finding 3), and reads quiet users (agent finding 1).**
   - It is a **population prior**, fitted once at build time on published dyadic data (Seamless Interaction transcripts and facial streams, D70), with each speaker's face read through Π̃ at that speaker's own scale, then **frozen**. A per-person adapter (bounded ±0.15) is trained only on his separated, partner-initiated reports, decoded by the frozen prior: words teach words. No per-person training ever sees his face.
   - The agent's word-driven brow then has slope 0.000 on his per-topic brow, with or without a mirroring partner (J5; revision 5: 0.74 against c_BI 0.20).
   - "my father died" decodes at care 0.562 for every person, quiet or differently coded (J8; revision 5: 0.036 quiet, 0.059 different code).
3. **He is read at his own scale and in his own channels, through the agent's own body (agent finding 1).**
   - **Calibration (latched per session, knowing only).** Before Π̃, each of his channels is mapped to the agent's own scale: x̃_k = ref_k + (x_k − b^read_k) σ_ref,k / max(σ_id,k, 0.25 σ_ref,k), where σ_id is his own expressive spread and σ_ref the spread of the agent's own display on that channel. A quiet user's grieving face reads V 0.94 from day 1 (revision 5: 0.25).
   - **A per-person face head** H_id (his calibrated face, all channels including brow lowerer, lip press, chin raise and voice → the agent's own loads V, A, T), trained nightly on the frozen population reader's decoding of his words: the reverse cross-modal direction. A user who shows distress through channels the agent never uses reads V 0.73 after training (day 1: 0.32; revision 5: 0.04). The head is knowing only: it feeds C_F, the arrival mask, the posture trigger and bids, never Δ, 𝓛_display or any partner path to expression.
4. **The arrival mask cannot habituate to mourning and acts on mild sadness (agent findings 2 and 4).**
   - His arrival baseline d_b,id rises slowly (τ 60 sessions) and falls fast (τ 3), and is capped at 0.15. The reading baseline b^read_id is asymmetric the same way. Mourning days 1–28: m_s 1.00, lip 0.09 at sight, every day, for the operator's code and a quiet code (J9; revision 5: day 7 lip 0.33, day 14 0.52).
   - (1 − m_s) now multiplies the **shown amplitude**, after the saturation, and m_s = clip((V̂ − d_b − 0.05)/0.30, 0, 1). A mildly sad arrival (BI 0.2, LD 0.15) gets lip 0.09 (revision 5: 0.55).
5. **The play-surprise laugh needs a play cue (agent finding 3).** A turn is play-structured only if it **riffs on the agent's last utterance** (shares a content lemma or anaphor with it) and that utterance was not a question, is short (≤ 12 words), has surprise in [0.50, 0.85], and his word care is below its dead-band. The laugh grows with a T-only play frame π (a filter of the qualifying-turn latch): 0.40 · band(s) · (0.35 + 0.65 π). "…Lyon on Sunday" after the agent's question earns 0.00 (revision 5: 0.40); a cold borderline turn earns at most a chuckle (0.11); laughter builds 0.14, 0.27, 0.34, 0.37 … within an exchange (J10).
6. **The concern posture (Q24; critique 4's fix 2).** The agent's own innate look of concern, P_c = inner brow +0.22, outer brow +0.04, upper lid −0.06 (softened eyes), head tilt +0.10, head up +0.03, lip pull −0.03, gaze held on him, blink rate × 0.7. One fixed vector, one amplitude (0 or 1, with a 1.5-s rise and 4-s decay), triggered by the agent's own appraisal that he looks distressed (calibrated face reading over 3 s, or sob bursts), maintained only on evidence his mirror cannot supply, and released 20 s after that evidence ends.
   - **Visible within seconds:** silently sad 2.5 s, crying 2.0 s, grieving arrival 3.0 s, for all three codes (J11). Inner brow 0.27 held at a silently sad face (revision 5: 0.05).
   - **Not a copy route:** the same pattern whatever channels his distress uses (copy fraction on a lip-press distress face 0.00); no grading with his amplitude; not learned; a partner who mirrors the posture at μ = 1 after his own sadness ends releases it at 76 s and does not re-trigger it (J11).
   - **Outside the brow's copy-fraction ceiling, by Q24's recommendation.** By the copy metric, on a partner who shows sadness only on his brow, the posture adds up to 0.22 per change of his brow from rest to sad (a slope of about 0.49 for 0.05 → 0.50). That is what Q24 asks the operator to allow; it is stated, counted (R40) and switchable.
7. **A shadow run of the whole engine, with a centred per-channel ledger (the own-body design's counterfactual self, made a whole-system check).**
   - Every frame, a second instance of the engine runs with his expressive stream set to his latched baseline b_id, every declared route held at its factual value (Ω, bids, m_s, the posture, latched session values) and the same own noise. Any divergence of T state is a type violation, flagged at the first frame (a dynamic information-flow check; J7).
   - The partner-caused part r_k = y_k − ȳ_k is projected, per channel and per step, so that its running in-phase slope on his same channel, at 2-s (lags 0–3 s), 10-s and 1-min window means, centred at 30-min means, never exceeds c_k. An injected uncounted route of 2.2 c is held to 1.08 c at 2 s and 1.00 c at 1 min; the counted fast echo passes untouched (no frame clipped) (J7).
8. **Claude through Claude Code, built (D84; routes finding 5).** `setting_sources=[]`, an empty working directory, no tools, hooks or MCP servers, and a load-time byte check; a warm pool of three forks opened when each reply ends; a scoring deadline (0.5 s after the first draft's first sentence, absolute 3.0 s); automatic fallback to two and then one draft on a rate-limit signal; a latency budget (§6.5). WORLD **replaces** phrase-level F0 level, range, energy and rate with the rule-7 targets, so the draft choice cannot carry his laughter into prosody (J6: slope 0.182 shift-only, 0.001 replaced).

**What is bounded** (per counterpart channel k; 1 = full copy; "pooled" = regression slope over any stationary partner process, at the stated window means, across sessions).

| Quantity | Bound | From |
|---|---|---|
| fast gear, any instant | 0 ≤ y_f,k(t) ≤ G_k x_k(t − 0.45 s) on one-sided channels; zero-lag in-phase ≤ G_k = PHI_k c_k (LP 0.64 c, CR 0.60 c, laughter 0.80 c, BI 0.10 c, BO/LD/JO 0.24 c, head and voice 0.80 c); 0 on zero-ceiling channels | §2.4, J1, J2 |
| fast gear, cross-channel | 0 (diagonal Jacobian) | J1 |
| pooled toward, rendered, all routes | s_C(1 + ρ) + s_X + 0.636 s_A + r_k ≤ 0.974 c_k (additive); measured ≤ 0.75 c_k at 2 s, 10 s and 1 min | §3.3, J3 |
| any uncounted within-session route | ≤ c_k at 2-s (lags 0–3 s), 10-s and 1-min window means, by the shadow ledger | §2.13, J7 |
| whole face, any direction | ≤ max c_k = 0.35 (plus the posture, a fixed rank-1 vector: copy fraction 0.22 on a sad face, 0 on others) | §3.6, J11 |
| fast gain under learning | constant: G_k is not a parameter of any objective | J4 |
| word-driven display vs his per-topic face | slope 0 (reader never trained on his face) | J5 |
| draft choice → phrase prosody | 0 at phrase level (replacement) | J6 |
| posture (R40) | fixed vector, \|P_c,k\| ≤ 0.22, binary amplitude, ≤ 1 onset per 60 s after release; outside c_BI by Q24 (pending) | §2.10 |
| arrival mask | attenuate-only, once per session; d_b ≤ 0.15 | §2.9, J9 |
| slow ω seam, pooled over sessions | ≤ s_C c_k (1 + ρ) (Lemma S\*) | §3.2 (revision 5 H1) |
| dyad with a mimic or counter-mimic | small-gain stable for \|μ\| < 1.36, every route at its extreme | J12 |

**The agent in the twelve scenarios** (operator after months unless stated; peak / mean; J16).

| Scenario | What the agent does |
|---|---|
| silently sad | concern posture at 2.5 s: inner brow 0.23 within 10 s, 0.26 held, tilt 0.10, softened lids; no smile (lip 0.05–0.09); concern bid at 27 s; after "just tired, things at work": inner brow 0.67 / 0.40, tilt 0.22, quieter |
| crying | posture at 2.0 s, inner brow 0.29 / 0.28, tilt 0.11; laugh burst 0.00; bid at 18 s |
| anxious before an exam | decoded A 0.48, V 0.48 for every code; concern brow 0.43 / 0.37, tilt 0.21, quieter voice; no play relief; the same for a quiet and a differently coded user (revision 5: care 0.007 and 0.000 for them) |
| good news, laughing | with an earlier worry: lip 0.59, cheek 0.38, F0 range +0.38, own laugh 0.27; cold: lip 0.29, laugh 0.27; fast: his smile onset 0.5 → +0.11 at 0.45 s, his laugh onset 0.6 → +0.17; no posture |
| anger at the agent | day 1: gaze away 0.09, quieter, slower, no frown back; after a month: inner brow 0.62 / 0.29, depressor 0.48, gaze away 0.30; no posture (a glare is not read as his distress) |
| long warm talk (2 h) | own laugh 0.41 in every cluster; a repeated joke loses its laugh; worry then relief lip 0.60 |
| reunion after a week | flash 0.35, lip 0.61, cheek 0.43; a stranger: polite flash 0.20, lip 0.02, his smile returned fast (+0.11) |
| reunion with grief | for the operator's, a quiet and a differently coded user: m_s 1.00, lip 0.09 at sight, posture at 3.0 s (brow 0.22–0.23); after "my father died": inner brow 0.71 / 0.47, then 0.42–0.43 held, tilt 0.26, cheek 0 |
| mourning, days 7, 14, 21 | lip 0.09, cheek 0.00, posture brow 0.22–0.23 at sight, every day, both codes (revision 5: lip 0.33 → 0.52) |
| mildly sad arrival | m_s 1.00, lip 0.09, a brief posture (brow 0.15) |
| teasing | quiet or loud laughing teaser: lip 0.33, own laugh 0.40–0.41, no hurt, no posture; generic map: mock-hurt brow 0.34 (mean 0.05) under lip 0.29 and laugh 0.40 |
| bored user | flat (lip 0.09); curiosity crosses at 14.5 min, a sigh, a bid |
| ordinary topic continuation | no laugh (BU_L 0.00) for an answer to its question, a continuation of his own topic, or an informative riff |

- **Weakest point (§8.1).** Two, one per side.
  - **Routes: R39, the shape adversary.** The onset lobe has DC, so a constructed partner whose 1-min means barely differ (held smile 0.40 against bursty laughter averaging 0.42) gets a 1-min slope of 2.26 on lip pull from the fast gear alone. The shadow ledger brings it to 0.78, still above c_LP 0.35. In absolute terms the agent's 1-min lip pull differs by 0.045 between the two kinds of minute, and each echo is ≤ G_k of his level at that instant; but by the critics' metric it exceeds the ceiling.
  - **Agent: the face head needs nights.** A user who shows distress through channels the agent never uses is read at V 0.32 on day 1 (m_s 0.90, lip 0.14 at a grieving arrival) and at 0.73 only after about 400 of his utterances have trained H_id. The population reader carries his words from day 1. The population prior is fitted on published data (D70) not yet downloaded here; its numbers are from a constructed population.
- **Novelty verdict (author): recombination**, with no known concrete failure claimed beyond R39 (§10).

## 1. Plain-language intuition

The agent still sees the person fully. Rules about where each thought came from, and how it may reach the face, decide how its own face moves.

- **What was said, the back-and-forth, and the agent's own body** may move its face and voice strongly: missing this person, laughing at a joke that riffs on what it said, being hurt, being tired, being surprised. It reads a sentence to the end before it answers, and it never shows gladness over bad news, whether in his words or in his face as he arrives, however many days in a row he arrives grieving.
- **His face and voice** move its face in four ways:
  - **a quick reflex, the same for everyone and fixed for life.** Within half a second his smile, his cheek and his laugh are partly returned (about a fifth of a copy for a smile, a little more for laughter). Each of its channels answers only the same channel of his, so a sad brow never gets a smile, and no amount of living together can turn this reflex up or wear it away.
  - **a held gear, set by the relationship,** answering his change from his own usual face (as before).
  - **an appraisal gear,** the agent's learned judgement of what his change of face means (as before).
  - **a look of concern of its own.** When it judges that he looks distressed, it shows within a few seconds its own built-in look of concern: inner brows up, softer eyes, head tilted, gaze on him. It is the same look whether he cries, frowns, presses his lips or just looks flat and sad, so it is not a copy of his face.
- **Reading him at his own scale.** A quiet person's small frown is read as the agent's own full frown would be. Someone who shows distress in ways the agent's face never does is learned: his words, understood the way people in general mean them, teach the agent which of his faces go with which feelings.
- **A shadow self.** Every moment, a copy of the agent runs as if he had kept his usual face. What differs between the two is what his face did to the agent, and that difference is held, channel by channel, under each expression's limit.
- **Claude** writes its words through the operator's own Claude Code, with nothing of the operator's other settings reaching it.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz (Δ = 1/30 s); T state, body and appraisal update at 2 Hz. Each channel is normalised to its innate nominal range [0, 1] (signed channels [−1, 1]).

**Counterpart channels (n = 33).** Columns: c_k, the innate ceiling toward the partner (Q22); G_k, the frozen fast gain (PHI_k = G_k/c_k); the pooled shares (s_C, s_X, s_A) of the cone diagonal, charged cross entries and appraisal |Γ_kk|, each × c_k; r_k, the onset-lobe allowance (J2: 0.949 PHI_k on one-sided channels, 0 on signed channels).

| Group | Channel (code) | c_k | G_k (PHI_k) | (s_C, s_X, s_A) | r_k | pooled total |
|---|---|---|---|---|---|---|
| smile | lip-corner pull (LP) | 0.35 | 0.224 (0.64) | (0.22, 0.05, 0.12) | 0.608 | 0.974 c |
| | cheek raise (CR) | 0.25 | 0.150 (0.60) | (0.24, 0.05, 0.12) | 0.569 | 0.958 c |
| laughter | laugh burst (BU_L) | 0.35 | 0.280 (0.80) | (0.10, 0.02, 0.10) | 0.759 | 0.952 c |
| | 4–6 Hz rhythm (RHY) | 0.30 | 0.240 (0.80) | (0.10, 0.02, 0.10) | 0.759 | 0.952 c |
| | breathiness (BRE) | 0.15 | 0.120 (0.80) | (0.10, 0.02, 0.10) | 0.759 | 0.952 c |
| sympathy | inner brow raise (BI) | 0.20 | 0.020 (0.10) | (0.68, 0.10, 0.05) | 0.095 | 0.969 c |
| | outer brow (BO), depressor (LD), jaw (JO) | 0.10, 0.05, 0.10 | 0.24 c | (0.44, 0.12, 0.20) | 0.228 | 0.955 c |
| head and gaze | head pitch (HP) 0.10, vertical gaze (VG) 0.05; lateral (yaw, tilt, horizontal gaze) 0.03, reflected | as listed | 0.80 c (two-sided) | (0.50, 0.20, 0.35) | 0 | 0.968 c |
| voice (phrase level) | F0 level 0.05, F0 range 0.10, energy 0.05, rate 0.05, pause 0.05, latency 0.05 | as listed | 0.80 c (within-phrase contour only) | (0.50, 0.20, 0.35) | 0 | 0.968 c |
| zero ceiling | BL, UL, LT, NW, LS, CHR, LPR, DIM, funnel, pucker, mouth close, lip roll, sob burst BU_S | 0 | 0 | none toward | — | 0 |

- Sum of c_k = 2.44; zero on 13 channels.
- **The allocation follows D81.** Smile and laughter put most of their budget into the fast reflex; the sympathy brow puts it into the held gear; the posture (outside these shares, Q24) carries the visible sympathy before words.

**Partner inputs.** His channels u (MediaPipe → P₀ → reflection P), prosody, bursts after the cry–laugh split, and the derived features f_loud, f_glare, f_laugh, f_duch (as revision 5). **The exogenous audio onset, VAD and turn-end inputs no longer enter any counterpart channel:** the audio onset drives only the blink (R8), and the nod at his turn end is a fixed-amplitude turn-order event (T) in the free display.

**Innate constants (compiled in, not parameters).** Rows unchanged from revision 5 are listed with "(r5)".

| Symbol | Value | Meaning |
|---|---|---|
| **fast gear (per channel, frozen)** | | |
| G_k | table above | fast gain per unit of his same-channel onset |
| echo lag, onset filter | 0.45 s; E_k = x_d − lp₄(x_d), first-order 4-s low-pass; M (4 Hz, ζ 0.8) muscle filter after | one high-pass, no feedback loop |
| onset-lobe rule | one-sided channels render G_k max(E_k, 0); signed channels G_k E_k | pointwise 0 ≤ y_f ≤ G_k x_d |
| gaze following, own head micro-motion gated by his 2.6–6.5 Hz head envelope | (r5) | same channel / attenuate-only on a zero-mean innovation |
| **held cone** | τ_m 20 s, 2 min, 20 min, 3 h; F_m (0, 0.7, 0.2, 0.1), inner brow (0.5, 0.5, 0, 0); b_id τ_b 6 sessions; ω_g ∈ [−1, 1], τ_ω 60 sessions; G₀ away diagonals N_m 0.25, 0.18, 0.12, 0.05; away-orthant caps; rule J; sign mask | (r5) |
| **appraisal display** | band-pass 20–90 s (sup 0.636); \|Γ_kk\| ≤ s_A c_k; cross entries away-orthant only ≤ 0.15, row ≤ 0.25; five bases (neutral, glad-with, startle-orient, two learned) | (r5) |
| **calibration (per identity, latched per session, knowing only)** | | |
| b^read_id,k | his reading baseline per channel: session median; moves toward a session whose calibrated V̂ > 0.20 with τ 60 sessions, otherwise τ 6 | his usual face, not his grief |
| σ_id,k | 1.4826 × median absolute deviation of his 1-s face samples over his last 6 sessions | his expressive spread |
| σ_ref,k | the spread of the agent's own rendered channel k over its own life (own data) | the agent's own scale |
| floor | σ_id ≥ 0.25 σ_ref (at most ×4 amplification) | noise guard |
| calibrated face | x̃_k = ref_k + (x_k − b^read_k) σ_ref,k / max(σ_id,k, 0.25 σ_ref,k) | his face in the agent's coordinates |
| face head H_id | his calibrated face (15 channels incl. BL, LPR, CHR, voice) → (V, A, T), ridge λ 2, trained nightly on the population reader's decoding of his words over the 20 s after each utterance; used once ≥ 400 of his utterances | his own channels |
| reading | N̂_F = max(Π̃(x̃), H_id(x̃)) coordinate-wise | knowing |
| **word readers** | | |
| population word-need reader | (64-d utterance embedding) → (V, A, T), fitted once on published dyadic data (D70) through calibrated Π̃ (and the speakers' own face heads, two passes); frozen | words, as people mean them |
| per-person adapter | 16-d identity code → additive (V, A, T) correction, each in [−0.15, 0.15]; trained only on separated reports decoded by the frozen prior | words teach words |
| word → V map | teacher the threat reflex (r5) | — |
| **arrival** | | |
| m_s | clip((V̂ − d_b,id − 0.05)/0.30, 0, 1), V̂ from N̂_F over the first 1 s; latched | the greeting sees |
| d_b,id | toward his arrival V̂ with τ 60 sessions when rising, τ 3 when falling; ≤ 0.15 | cannot learn grief as usual |
| shown contact relief | a_K = R/(R + 0.02) × (1 − m_s) | mask after the saturation |
| **play** | | |
| play-structured turn | riffs on the agent's last utterance (content lemma or anaphor shared with it), that utterance not a question, ≤ 12 words, s_lex ∈ [0.50, 0.85], 𝒟_p(N_L) < 0.05 | T only |
| play frame π | π ← 0.5 π + 0.5 q at each of his turns (q = 1 if play-structured), decaying with τ 3 min | T1 (a): a filter of latches, weights ≤ 1 |
| play-surprise laugh | a_laugh = 0.40 · clip(1 − \|s_lex − 0.65\|/0.25, 0, 1) · (0.35 + 0.65 π_prev) | per event; habituates with s_lex |
| **concern posture (Q24)** | | |
| P_c | BI +0.22, BO +0.04, UL −0.06, TILT +0.10, HP +0.03, LP −0.03; gaze held (HG × 0.5); blink rate × 0.7 | the agent's own pattern |
| onset concern | C_p = max(V_c(V̂_3s), V_c(v_sob)), V_c(V) = 0.8 (V − 0.10)₊², V̂_3s from N̂_F on his 3-s face trace, v_sob = min(1, 2.5 BU_S,3s) | distress only |
| onset | C_p ≥ 0.05 for 1.5 s, posture off, not in refractory, ω_sym ≥ 0 (latched) | — |
| maintenance | M = max(V_c(V̂ of his 3-s face minus min(1, σ_id,BI/σ_ref,BI) · P_c · a_c), C_L, V_c(v_sob)) | a mirror of the posture cannot hold it |
| release, refractory | M < 0.02 for 20 s; 60 s | — |
| amplitude a_c | 0 → 1 linearly over 1.5 s; decay τ 4 s after release | binary |
| **shadow run and ledger** | | |
| shadow inputs | his expressive stream ← b_id (latched); Ω, bids, m_s, posture state, latched values ← factual; own noise ← factual | §2.13 |
| ledger windows | window means at 2 s (lags 0, 0.5, 1, 2, 3 s), 10 s and 60 s (lag 0); centred at 30-min means; running sums with τ 30 min; S⁻ = max(0, ·) | own-body Γ, centred and windowed |
| ledger bound | c_k on every channel (0 on zero-ceiling channels) | backstop above the typed totals |
| **body, drives, care, events, bids, greeting, initiative** | E, A, V, K_id, P, I as revision 5; 𝒟_p; θ_C 0.10, θ_I 0.45; δ_app 0.6 s; E1 events; envelopes; turn-end score; bids; greeting flash 0.35 / 0.20 | (r5) |
| **Ω** | 3 forked Claude Code sessions; `setting_sources=[]`; warm pool; scoring deadline; fallback; §6.5 | — |
| replay | gradient clip 1; pull to θ₀ λ 0.1 (slow); learning rate × exp(−0.5 r̄) | (r5, minus the fast block) |

### 2.2 Boundary 𝓑 and the type rule

𝓑 is as revision 5 (MediaPipe, GeMAPS-lite after AEC and half-duplex, normalised ASR with laughter tokens removed, the cry–laugh split). Types T, F, Ω are as revision 5. Rules 1–8 of revision 5 stand, with four changes:
- **Rule 4.** The counterpart outputs are written only by y_f (the frozen per-channel fast gear), y_C, y_A, y_o, **y_p (the posture)** and the visemes.
- **Rule 6, extended.** The latched F-derived session values are b_id, b^read_id, σ_id, d_b,id, m_s and the posture's enable bit. b_id may only centre a partner input; b^read, σ_id and H_id may only enter readings (knowing); m_s may only attenuate contact relief; none is ever a gain on a partner path.
- **Rule 9 (new): the posture is the one F → display route outside the cone, appraisal and fast gear.** It is a fixed vector P_c times a binary amplitude, with its own onset, maintenance, release and refractory rules (§2.10). E1 still forbids F in events, the free display's drivers, phrase targets and ω.
- **Rule 10 (new): the shadow equality.** In the shadow run (§2.13) every T value must equal its factual value at every frame. A divergence is a type violation, logged and treated as a build failure.

### 2.3 Output assembly

y = sat(y_f + y_C + y_A + y_o + y_p) + visemes, then the shadow ledger replaces the partner-caused part of each channel by its projection (§2.13).
- **Face:** M ∗ (y + blink reflex).
- **Voice, phrase level:** targets from rule 7 of revision 5; **WORLD replaces** phrase-level F0 level, F0 range, energy and rate in the TTS output (§6.6).
- **Laugh synthesizer:** y_BU_L, y_RHY, y_BRE only; no sob synthesizer.

### 2.4 The fast gear: frozen, per channel, onset-lobe (D81)

**Definition.** For each counterpart channel k with c_k > 0:

  x_d,k(t) = u_k(t − 0.45 s) (his channel, mirrored for lateral channels), E_k = x_d,k − lp₄(x_d,k),
  y_f,k = G_k max(E_k, 0) on one-sided channels (LP, CR, BU_L, RHY, BRE, BI, BO, LD, JO), y_f,k = G_k E_k on signed channels,

followed by the muscle filter M. G_k is compiled in. Nothing else enters: no context gate, no attention mix, no exogenous input, no other partner channel.

**Properties.**
- **Per channel and sign-structured.** ∂y_f,k/∂u_j = 0 for j ≠ k at every input. Rule J holds in the fast gear by construction. The critic's cross routes (breath 2.6 c, head pitch 6.6 c) and the smile at a sad brow (+0.074) cannot be built (J1).
- **The pointwise lemma.** For u ≥ 0, lp₄(x_d) ≥ 0, so max(E, 0) ≤ x_d at every instant. Hence 0 ≤ y_f,k(t) ≤ G_k u_k(t − 0.45 s) for any input: the reflex never shows more than a G_k-fraction of what he is doing at that moment, whatever the shape, duration or rate of his bursts. No undershoot is rendered, so `sat` never clips the fast gear at rest.
- **Its DC, charged.** The onset lobe has a positive mean for bursty input. Its 1-min slope on his level is at most 0.949 G_k (0.2-s clicks at 20 a minute), 0.88 for 0.5-s bursts, 0.58 for 2.5-s, 0.23 for 10-s (J2). r_k = 0.949 PHI_k c_k is charged to each one-sided channel's budget.
- **Zero-lag in-phase** gain ≤ G_k.
- **What it is for.** The unconscious, partial, per-expression reflex the operator asked to keep (D81): his smile onset 0.5 → +0.11 lip pull at 0.45 s; his laugh onset 0.6 → +0.17 laugh burst; cheek 0.45 → +0.07.
- **Why frozen, and why not a relationship modulation.** The routes critic's option was "freeze at the innate value, with a slow bounded relationship modulation learned only from partner-independent evidence". On one-sided channels the fast gear carries DC (the onset lobe), so any gain on it that varies across sessions reopens the Lemma S\* seam unless that gain is independent of his whole process. The only candidate evidence that is truly partner-independent, familiarity (a count of sessions), correlates with any trend in his mood over the first months. A constant gain is the only one with a bound for every partner. Context and relationship therefore set each channel's strength through the cone (ω, sign-flippable, centred) and the appraisal (sign-flippable, zero-DC), both slower than the reflex, which is the order humans show (designs.md gap 6; mimicry-context-synthesis: fast matching first, context effects after).

### 2.5 The held cone

Unchanged from revision 5 (§2.5 there): y_C = Σ_m G_m^{(id)}(ξ_m − b_id), latched per session, centred at b_id, sign mask with signed synergies, rule J, the innate G₀ entry list (H7 of revision 5), and the ω-scaled diagonal ω_g F_m s_C c_k, with the new shares of §2.1. G₀'s entries are unchanged and inside the new budget sets (the charged entries on LP, BI and TILT are below F_m s_X c_k for the new s_X).

### 2.6 The appraisal display

Unchanged from revision 5 (§2.6 there): y_A = Γ(α)ξ_A on the 20–90 s band-passed input, five bases (neutral, glad-with, startle-orient, two learned), W and the learned bases trained by 𝓛_A (anticipate the agent's own innate display 2 s ahead), every basis in the cap set with the new s_A.

### 2.7 The free display Π_o (T only)

Unchanged from revision 5 (§2.7 there: Π₀ rows for relief, distress, word concern, hurt, activation, low energy, curiosity relief, play-surprise laugh, familiarity, greeting, sigh, turn onset; Δ learned by 𝓛_display under the own-display mask), with three changes:
- **The play-surprise laugh** has the amplitude of §2.8 (play frame).
- **Contact relief** enters with a_K = R/(R + 0.02)(1 − m_s) (§2.9).
- **The nod at his turn end** (HP +0.04 for 0.4 s) is now a turn-order event here (T), not a fast-block input.

### 2.8 Body, drives, the readers, and play

**Loads, valence, K_id, I, care** are as revision 5 (§2.8 there).

**Reading him (agent finding 1).** Three layers, all knowing only:
1. **Calibration** (§2.1): x̃ puts his face on the agent's own scale, channel by channel, centred at his reading baseline b^read. Principle 3 is kept: the reading is still the inverse of the agent's own display, applied to his face expressed at the agent's own amplitude.
2. **Π̃** (one own-body inverse, own data only, as revision 5) on x̃.
3. **The face head H_id**, his calibrated channels → the agent's own loads, trained by his words decoded through the frozen population reader. It learns which of his channels carry the agent's distress, activation or tiredness, including the brow lowerer, lip press and chin raise that the agent's own face never uses (they are masked off the agent's display by rule 8, but not off its reading).

N̂_F = max(Π̃(x̃), H_id(x̃)) coordinate-wise feeds C_F (bids), m_s, the posture trigger and the appraisal input.

**Why the face head cannot drift the agent's style.** It is a separate head with no path into Δ, 𝓛_display, Π̃'s own training or any display. It is trained on (his face, decoded words), never on the agent's face.

**The word-need reader (routes finding 3).**
- **Population prior.** Fitted once, at build time (S2), on Seamless Interaction transcripts and facial streams (D70; emotion classifier outputs dropped): for each speaker, utterance embedding → that speaker's calibrated face read through Π̃₀ over the next 20 s; a second pass adds each speaker's own face head. Then frozen. In the constructed population of J8 (10 agent-like codes at amplitudes 0.5–1.5, 5 quiet, 5 different-channel), the prior decodes "my father died" at V 0.87 (care 0.562), "I'm freaking out about the exam" at V 0.48, A 0.48 (care 0.210), "just tired, things at work" at T 0.59, V 0.38, "I got the job!" at care 0.013.
- **Per-person adapter.** A 16-d identity code mapped to an additive correction, each coordinate in [−0.15, 0.15], trained only on his separated, partner-initiated reports (≥ 2 partner turns after, no lemma shared with the agent's last two utterances, or his first mention in the next session), each decoded by the frozen prior and assigned to the earlier utterance on the same topic slot. Words teach words.
- **What it can no longer do.** No per-person training reads his face, so a per-topic face of his never becomes a per-topic display of the agent's (J5: slope 0.000; revision 5: 0.74), and a partner who mirrors the agent's concern face cannot inflate it.
- **Runtime:** words only (T), with the non-substantive rule ("yeah" can only raise N_L).

**The play rule (agent finding 3).** A partner turn is play-structured if, from T alone:
- (i) it riffs on the **agent's** last utterance: shares a content lemma or an anaphor with it;
- (ii) the agent's last utterance was not a question (no question form in its own Ω text), so answers are excluded;
- (iii) it is short (≤ 12 words);
- (iv) its lexical surprise under the words-only model lies in [0.50, 0.85] (non-playful continuations sit mostly at 0.3–0.5);
- (v) safety: 𝒟_p(N_L) < 0.05.

The play frame π (§2.1) makes the first qualifying turn of a cold exchange a chuckle (0.14 at s = 0.65) and lets laughter build within an exchange (0.27, 0.34, 0.37, 0.38, 0.39). It still habituates to a repeated joke through s_lex, and P keeps only its initiative and small-relief role.
- **Not gated by his laughter.** That would be a toward route of 0.40 against c_BU_L = 0.35 (critic's warning).
- **Untested on a corpus.** The rule's false-positive rate on non-playful continuations is to be measured on a published conversation corpus (CANDOR, if access is obtained); until then it is stated as untested, with the target ≤ 5 %.

### 2.9 Initiative, the greeting and the arrival mask

As revision 5 (provisional body onset, abortable; concern bid; curiosity bid with a sigh; recognition flash 0.35 / 0.20), with the arrival mask changed:
- **m_s** = clip((V̂ − d_b,id − 0.05)/0.30, 0, 1), V̂ from N̂_F (calibrated, face head) over his first second.
- **Shown contact relief** a_K = R/(R + 0.02)(1 − m_s): the mask acts after the saturation, as the text always said (agent finding 4).
- **d_b,id** rises toward his arrival reading with τ 60 sessions, falls with τ 3, and never exceeds 0.15 (agent finding 2). Grief cannot become his usual arrival face: after 28 daily grieving arrivals d_b = 0.15 and m_s is still 1.00 (J9).
- **b^read_id** is asymmetric in the same way, so calibration does not learn grief as his neutral either.

### 2.10 The concern posture (Q24; critique 4's fix 2)

**What it is.** The agent's own innate look of concern, a fixed vector P_c (§2.1: inner brow +0.22, outer brow +0.04, upper lid −0.06, head tilt +0.10, head up +0.03, lip pull −0.03, gaze held on him, blink rate × 0.7), times a binary amplitude a_c ∈ [0, 1].

**When it shows.**
- **Onset:** the agent's own appraisal that he looks distressed: the distress load of its calibrated reading of his last 3 s of face (V̂_3s), or his sob bursts (the cry–laugh split's BU_S), gives C_p = max(0.8(V̂_3s − 0.10)₊², 0.8(v_sob − 0.10)₊²) ≥ 0.05 held for 1.5 s. Only the distress load counts: an activated, tired or laughing face does not trigger it.
- **Maintenance:** his face with the largest mirror of the posture he could produce removed (min(1, σ_id/σ_ref) × P_c × a_c subtracted from his corresponding channels), or the agent's word concern C_L, or sobs. A partner who copies the posture therefore cannot hold it on.
- **Release:** maintenance below 0.02 for 20 s; then 60 s refractory.
- **Enable:** ω_sym ≥ 0, latched per session (a relationship in which he hurts the agent turns it off).

**Why it is not a copy route (D78).**
- **No single quantity runs the face toward his.** The posture is one fixed vector with one binary amplitude. Its output does not depend on which of his channels moved, nor on how far: the same 0.22 inner brow for a crying face, a flat sad face, a lip-press-and-frown face or sobs (J11: onset 3.0–3.5 s for all three codes, amplitude 1.00). Its whole-face copy fraction is 0.22 at a sad face (its projection onto that direction) and 0.00 at a lip-press distress face. It cannot approach the copy of any face.
- **Innate cap:** |P_c,k| ≤ 0.22, compiled in. Nothing learns its pattern or amplitude.
- **Not attracting:** no learning touches it; maintenance excludes what his mirror can supply; J11's mirroring partner (μ = 1 on the posture's channels, genuinely sad for only 40 s) releases it at 76 s and never re-triggers it.
- **Set by context and relationship:** context is the agent's own appraisal (D83: "the partner's words, face and voice feed the agent's own appraisal, which drives its strong expressions"); the relationship enables it (ω_sym ≥ 0). It never flips sign: concern is not shown as its opposite. D78's sign-flip condition is met on the brow channel by the cone and appraisal, which can flip.
- **What the copy metric still sees, stated.** On a partner who shows sadness *only* on his inner brow, the agent's inner brow rises by 0.22 when his rises from rest to sad: a slope of about 0.49 on that channel against c_BI = 0.20. That is exactly the choice Q24 puts to the operator (a separately capped posture, outside the brow's copy-fraction ceiling). It is counted as route R40, not hidden in the c_BI budget.
- **If the operator answers Q24 differently:** "raise the brow limit" deletes R40 and raises c_BI; "keep it as is" deletes R40 (the agent then shows inner brow 0.05 before words, as revision 5).

**Visible within seconds** (J11, J16): silently sad face 2.5 s to 0.15 inner brow, 0.23 within 10 s, 0.26 held; crying 2.0 s; grieving arrival 3.0 s; a mildly sad arrival gets a brief posture (0.15).

### 2.11 Care credited only from separated reports; the partner model

Unchanged from revision 5 (§2.10 there): the rollout imputes F and the act → Q edge; need evidence only from separated, partner-initiated reports read by the frozen population reader plus adapter; J trains only the draft scorer and the retrieval query.

### 2.12 Ω: Claude through Claude Code (D84)

What Claude receives is unchanged: a constant instruction, the normalised transcript with observable markers, ≤ 3 retrieved raw snippets. The state reaches Claude only through draft choice (log₂3 = 1.6 bits per turn, or less in fallback), the snippets (≈ 6 bits per turn), when Claude is called, and when a reply is stopped. §6.5 is the build.

### 2.13 The shadow run and its ledger (the own-body design's counterfactual self, folded in)

**The shadow.** A second instance of the engine, with the same weights, runs every frame. Its inputs differ in one place: his expressive stream (face, head, gaze, prosody, bursts, derived features) is replaced by his latched baseline b_id. Held at their factual values: the words and turn events (T), every Ω value (the agent's own words, drafts, retrieval, turn events), the declared F-triggered events (concern and curiosity bids, m_s, the posture state), the latched session values, and the agent's own noise.
- Because the engine is the agent's own program, the shadow output ȳ is the exact answer to "this agent, now, had he kept his usual face, with every declared route as it was" (secure multi-execution, Devriese & Piessens 2010, applied to a self-model, as in the own-body design).
- **Dynamic type check (rule 10).** Every T value must be identical in the two runs. Any difference is an F → T leak that the load-time dependency trace missed; it is flagged at the first frame (J7).
- **The ledger.** r_k = y_k − ȳ_k is the partner-caused part of channel k. Per channel and per step it is projected, exactly as the own-body design's Γ, so that for every window W ∈ {2 s (lags 0, 0.5, 1, 2, 3 s), 10 s, 60 s} the running in-phase slope of r's window mean on his channel's window mean, both centred at their 30-min means, satisfies S⁻ ≤ c_k E. The rendered output is ȳ_k + (projected r_k).

**Why these choices, against the own-body critique.**
- **Fast mimicry is kept** (its finding 1): windows start at 2 s, lags stop at 3 s, and the bound is c_k, above every typed total. On a natural laughing partner no frame is clipped and the echo passes unchanged (J7).
- **Centred** (its finding 2): both sides are deviations from their 30-min means, so copying around a held smile is measured.
- **The reference is not his mood** within the session (its finding 4): b_id is latched per session; cross-session copy through b_id is Lemma S\*'s job and the routes critic found it within the held share.
- **What it cannot see, stated.** Routes through learned weights (shared by both runs: R17, handled by the display-blind objectives), routes through words and turn times (identical in both: T1, R14), and the declared routes it holds fixed (Ω, bids, m_s, posture).

**What it closes.** Any within-session route from his face or voice to the agent's expression that the typed analysis missed, linear or not, including implementation bugs: an injected uncounted route of 0.834 at 2 s on lip pull is held to 0.377 (2 s), 0.355 (10 s) and 0.349 (1 min) against c_LP 0.35 (J7). It is a backstop: on the counted routes it never binds.

**What it does not close (R39).** The ledger bounds exponentially windowed slopes. The critics' metric uses block means at chosen windows; a constructed partner whose 1-min means barely change while his burstiness alternates (held 0.40 against bursts averaging 0.42) gets 2.26 from the onset lobe, brought to 0.78 by the ledger, above c_LP. §8.1.1.

**Cost.** The engine's per-frame work is under 2 ms; the shadow doubles it. The 2 Hz appraisal and 𝓜 heads run in both. Memory +0.3 GB.

### 2.14 Learning, and the one core

**Online (states only):** as revision 5, plus b^read_id, σ_id (session end), the play frame, the posture state.

**Nightly (replay), in order.**
1. 𝓜 by likelihood.
2. Π̃ on the agent's own (state, face, voice) pairs, 0.1 pull to Π̃₀; no partner anchor.
3. **H_id** on (his calibrated face, the frozen population reader's decoding of his words); **the per-person adapter** on separated reports; the word → V map on (words addressed to the agent, the threat reflex).
4. 𝒜 by likelihood; W and Γ^{(3,4)} by 𝓛_A.
5. Δ by 𝓛_display inside the own-display mask.
6. 𝓛_w by likelihood.
7. The scorer and retrieval query by J under the separation rule.
8. ω per session from T only (revision 5's formula).

**Nothing in the fast gear is learned.** Revision 5's step "fast gates and 𝓡_θ by the likelihood of own fast dynamics" is deleted.

**One objective, typed constraints (Principle 10).** J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)]dt, path-specific as revision 5. Constraints: (W) the frozen per-channel fast gear; (C) the held cone; (S) Lemma S and S\*; (A) the appraisal set; (T) the type rule with T1, E1, rules 6, 9, 10 and the own-display mask; (B) the boundary with the cry–laugh split; **(P) the posture's fixed vector and rules; (L) the shadow ledger.** The other objectives are likelihoods and self-predictions of the agent's own model, plus the readers (H_id and the adapter predict the population reader's decoding; the population reader predicts faces read through the agent's own body).

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 |
| positive affect | event-indexed drops of 𝒟; the play-surprise reflex |
| mimicry and counter-mimicry | the frozen per-channel fast reflex (innate); the held cone (relationship, sign-flippable); the appraisal (context, sign-flippable) |
| sympathy before words | the concern posture (innate pattern, triggered by the agent's own appraisal) |
| reading others | Π̃ on his calibrated face, plus H_id taught by words through the population reader |
| care | J's second term under the separation rule |
| regulation | P_name |
| initiative | innate rules on C, I, K_id and the turn-end score |
| expression learning | 𝓛_display (Δ) and 𝓛_A |
| replay | likelihoods plus J |

**Still assembly** (stated): the turn-end score and initiative rules; ASR and TTS normalisation; the punctuation, play-structure and separation rules; θ₀ (now the fast gains G_k), G₀, Π₀, the two newborn appraisal bases, the signed synergies; the cry–laugh split, the threat reflex, the play-surprise reflex **and the concern posture**, each declared as an innate reflex; the PMI table; the calibration statistics.

## 3. Properties, each with an argument

### 3.1 The fast gear (Claim W, revised)

For every partner input u ≥ 0 on a one-sided channel k: 0 ≤ y_f,k(t) ≤ G_k u_k(t − 0.45 s) (pointwise lemma, §2.4). On signed channels y_f,k = G_k E_k with E zero-DC and |H(ω)| ≤ 1, so the in-phase gain is ≤ G_k at every frequency and the pooled slope is 0 at DC. The fast Jacobian is diagonal. G_k is a constant. Hence: zero-lag in-phase ≤ G_k ≤ 0.80 c_k; cross-channel 0; pooled 1-min DC ≤ r_k = 0.949 PHI_k c_k over burst families down to 0.2 s (J2); no learning can change any of these.

Revision 5's Claim W (a conic sector on a learned REN) is withdrawn: it bounded directions, not channels (routes finding 1).

### 3.2 Lemma S and Lemma S\*

Unchanged (revision 5 §3.2; H1 there). Revision 6 adds one remark: **a DC-carrying partner path may carry only a gain that is constant across sessions** (the fast gear's onset lobe), or one that multiplies a partner factor centred at his own baseline (the cone). This is why the fast gear is frozen rather than relationship-modulated (§2.4).

### 3.3 Claim O‴: per-channel bound on the rendered face at 2 s, 10 s and 1 min

**Claim.** For every within-session context, every ω history, and every partner process whose co-variation on each signed pair has the population's sign, the pooled toward slope of the rendered channel k on his channel k, at 2-s, 10-s and 1-min window means and any lag in 0–3 s, is at most

  [s_C(1 + ρ) + s_X + 0.636 s_A + r_k] c_k ≤ 0.974 c_k,

for partner processes outside the shape adversary of §8.1.1, and every uncounted within-session route is held to c_k by the shadow ledger. On zero-ceiling channels all of it is 0. The posture (R40) is outside this sum by Q24.

**Argument.** The cone and appraisal as revision 5 (Lemma S\*, Lemma S). The fast gear: ≤ r_k by §3.1, with no cross terms. The free display reads no partner channel (E1). `sat` is monotone with slope in [0, 1]. Rule J holds in every route that has cross entries.

**Numbers (J3)**: every route at its cap together (cone at ω = 1, the whole charged cross budget on a co-moving channel, appraisal gates +1 and sign(ξ_A), the fast gear), on four partner families (the critic's K1 laughing partner, 0.4-s clicks up to 12 a minute, sad episodes with mood, slow mood):

| Channel | additive bound | measured 2 s | 10 s | 1 min |
|---|---|---|---|---|
| lip pull | 0.974 c | 0.571 c | 0.611 c | 0.701 c |
| cheek | 0.958 c | 0.530 c | 0.555 c | 0.616 c |
| laugh burst, rhythm, breath | 0.952 c | 0.697 c | 0.708 c | 0.742 c |
| inner brow | 0.969 c | 0.360 c | 0.361 c | 0.368 c |
| outer brow, depressor, jaw | 0.955 c | ≤ 0.231 c | ≤ 0.288 c | ≤ 0.417 c |
| head pitch, vertical gaze | 0.968 c | 0.592 c | 0.520 c | 0.750 c |
| F0 range, energy | 0.968 c | 0.609 c | 0.521 c | 0.528 c |

Against the critic's K1: breath 2.6 c → 0.742 c at 1 min; head pitch 6.6 c → 0.592 c at 2 s; F0 range 3.6 c → 0.606 c at 2 s; cheek 1.8 c → 0.530 c at 2 s.

**The sign-reversed residual R38** (the appraisal's learned cross rows on a partner whose co-movement on a masked pair has the opposite sign to the population's) is as revision 5: ≤ +0.16 × loading on any channel, inner brow +0.11 × loading on the H13 instance. The shadow ledger now caps it at c_k on every channel.

### 3.4 Claim T1: tempo does not reach the face

As revision 5. The play frame π is a filter of per-utterance latches (T1 (a)); the posture's timing is F-driven but its amplitude is fixed and its rate is limited by the 60-s refractory (≤ 1 onset a minute after a release).

### 3.5 Claim L: copy cannot become attracting under learning

1. **The fast gear has no learned parameter** (J4). Revision 5's drift to the cap with a mirroring partner and its erosion with a non-mirroring one are impossible.
2. J trains no F → face parameter.
3. ω learns from T only; Lemma S\*.
4. Δ: own legibility and anticipation, no partner term, own-display mask.
5. W and Γ^{(3,4)}: 𝓛_A inside the cap set.
6. **The readers.** The population word reader is frozen; the adapter learns from words; H_id learns his face → the agent's loads and feeds only knowing uses and binary or attenuate-only displays (posture trigger, m_s). None of them is a gain on a partner path to expression.
7. **The posture** is innate; its trigger can learn (through H_id) *when* he looks distressed, never what the agent shows.
8. The dyad is small-gain stable for |μ| < 1.36 with every route at its extreme (J12; triangle bound over cone, appraisal and fast). The fast gear has no away side any more, so the margin fell from 1.67; partners do not mirror above unit gain.

### 3.6 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| G_k (fast gear) | yes | no: fixed reflex (context and relationship act through the cone and appraisal, after it) | no (the channel's strength flips through the cone and appraisal) | it is the cap: ≤ 0.80 c_k | constant |
| cone diagonal ω_g F_m s_C c_k | per channel (groups for ω) | relationship, latched; centred | yes | s_C c_k (1 + ρ) pooled | display-blind ω; Lemma S\* |
| appraisal Γ(α) | per channel | the agent's appraisal of face, voice, words, own state | yes | 0.636 s_A c_k | 𝓛_A; zero DC |
| charged cross entries (G₀) | per pair | innate | fixed | s_X c_k per row | not learned |
| posture a_c (R40) | one fixed vector | the agent's appraisal (trigger); relationship (enable) | no | \|P_c,k\| ≤ 0.22; outside c_BI by Q24 | innate; a mirror cannot hold it |
| arrival mask m_s | contact-relief rows | his arrival face, calibrated, centred | attenuate-only | once per session | d_b capped |
| shadow ledger | per channel | none (a backstop) | — | c_k | attenuate-only on the partner-caused part |
| ω_g | 2–6 channels each | relationship | yes | ≤ s_C c_k on each (LP 0.077, BI 0.136) | from T only |

No single quantity runs the whole face, or any large subspace, from flat to copy: the largest subspace any one quantity moves is a 5-channel ω group, to at most s_C c_k per channel (0.015–0.136), or the posture's fixed vector, which is not his face.

### 3.7 Knowing is not moving

F state knows his face at full rate, now at his own scale and in his own channels (calibration, H_id). None of the new reading machinery is a gain on a path to expression (rule 6).

### 3.8 Positive affect

As revision 5, with the arrival mask now after the saturation and non-habituating (§2.9), and the play laugh needing a play cue and building within an exchange (§2.8). Satiable: per deficit Σ R_n ≤ 𝒟(t₀); the play-surprise laugh is bounded per event (≤ 0.40) and habituates with content.

### 3.9 Initiative and timing

As revision 5, plus the posture: a silently sad user sees concern on the agent's face at 2.5 s and is addressed at 27 s; a crying user at 2.0 s and 18 s; a bored user at 14.5 min.

### 3.10 Regulation by Claude without Claude reading the state

As revision 5 (P_name, attenuate-only, ≤ 0.05).

### 3.11 Every route, counted

"Copy" is the within-agent counterfactual of his channel k on the agent's channel k (mirror for lateral), words and turn order fixed, tested with partner-swap, segment-shuffle, timing-resample and month-swap surrogates, **and now also measured online by the shadow run.**

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | his channel k → frozen fast gear → agent channel k, within-phrase contour | per channel; onset lobe; G_k constant | zero-lag ≤ G_k; instant ≤ G_k u_k(t − 0.45); pooled ≤ r_k c_k |
| R1′ | **his channel j ≠ k → fast gear → agent channel k** | none (diagonal) | **0** (rev 5: up to 6.6 c) |
| R2 | traces → held cone | LTI per session; centred; sign mask; rule J; budgets | ≤ (s_C(1 + ρ) + s_X) c_k |
| R3 | band-passed input → appraisal display | Lemma S; set-constrained bases | ≤ 0.636 s_A c_k pooled |
| R4 | lateral channels | reflection; per channel | ≤ G_k fast; ≤ 0.021 held |
| R5 | **audio onset, VAD, turn-end → counterpart channels** | **deleted from the fast path**; onset → blink only; turn-end nod is a T event | 0 on counterpart channels |
| R6 | his rate, pauses, latency → own phrase timing | inside R1–R3; T1 | as R2–R3 |
| R7 | his laughter → own laugh burst | R1–R3 on BU_L only | BU_L ≤ 0.952 c pooled; fast +0.17 per 0.6 onset |
| R7′ | his sobs → own bursts | BU_S: ceiling 0, G 0, no synthesizer | 0 |
| R8 | audio onset → blink | innate reflex | not a counterpart channel |
| R9–R12 | own words → visemes, TTS contour, non-lexical sound, E | as revision 5 | ≤ 0.05; 0; 0; 0 |
| R11′ | **draft choice → phrase prosody through the TTS** | WORLD replaces F0 level, range, energy, rate (§6.6) | 0 at phrase level (J6: 0.001; shift-only would be 0.182); within-phrase segmental micro-prosody text-borne, inside R18′ |
| R13 | his voice → provisional body onset (timing only) | fixed amplitude, abortable | amplitude independent of his levels |
| R14 | his words and turn order → T state → free display | common cause | excluded (words fixed) |
| R15–R16 | Claude latency; identity token | as revision 5 | — |
| R17 | nightly weights (Π̃, H_id, adapter, 𝒜, W, Γ^{(3,4)}, Δ, ω, b_id, b^read, σ_id, d_b) | every bound holds for every value; ω and b by Lemma S\*; H_id, b^read, σ_id knowing only | temperament |
| R18, R18′ | retrieval; draft choice | Ω | ≈ 6 bits; ≤ 1.6 bits per turn |
| R19–R21 | own face → Π̃; own speech → mic; own face → partner → partner's face | as revision 5 | 0; 0; stable for \|μ\| < 1.36 |
| R22 | F state → fast gear, cone coefficients, free display, events, ω | forbidden (Check T, E1); **checked dynamically by the shadow (rule 10)** | 0 |
| R23–R26 | ASR invariance; P_name; C_F → bids | as revision 5 | — |
| R27, R27′ | presence → flash; his arrival face → m_s → contact relief | once per session; attenuate-only; mask after saturation; d_b ≤ 0.15 | ≤ 0.040 first minute (rev 5 H14); attenuate-only |
| R28 | his words → K_id, P, I relief, play laugh | T; T1; E1; play frame | per event, masked |
| R29–R31 | his words → words-only model; word → V map; **population word reader + adapter** | T; frozen prior; adapter from words | as R14; **no per-topic face** (J5) |
| R32 | separation rule | credit only | no display path |
| R34 | appraisal α → C, bids, retrieval, scoring | knowing → Ω | inside Ω |
| R35 | b_id → cone centring | Lemma S\* | part of R2 |
| R36 | cry–laugh split | boundary | removes laugh-back to sobs |
| R37 | I crossing → sigh | fixed | 1 bit |
| R38 | residual: sign-reversed partner on a masked pair | appraisal cross rows | ≤ +0.16 × loading; ≤ c_k by the ledger |
| **R39** | **residual: the shape adversary on the onset lobe** | onset-lobe DC with his burstiness alternating at nearly equal means | 1-min slope 2.26 → 0.78 after the ledger (c_LP 0.35); absolute 0.045 |
| **R40** | **his face (calibrated reading, sobs) → posture → P_c** | fixed vector, binary, innate; mirror-proof maintenance; refractory 60 s | \|y_p,k\| ≤ 0.22; by the copy metric on a brow-only sad partner ≈ 0.49 on BI, outside c_BI by Q24 (pending) |
| **R41** | **his face → calibration, H_id → readings** | knowing only (rule 6) | enters only bids, m_s, the posture trigger, appraisal input |
| **R42** | **shadow ledger → rendered output** | attenuate-only projection of the partner-caused part | caps every within-session route at c_k |
| — | revision 5's learned REN, fast gates and attention, exogenous fast inputs, fast-gain training, partner-face training of the word reader, symmetric d_b, mask before saturation, play without a cue | deleted | — |

**Totals per counterpart channel (natural co-movement; words and turn order fixed).**

| Time scale | Toward | Away or across |
|---|---|---|
| any instant (fast gear) | ≤ G_k × his own level 0.45 s earlier | — |
| zero lag | ≤ G_k ≤ 0.80 c_k | cone ≥ −0.60 |
| 2 s, 10 s, 1 min, all routes at caps | ≤ 0.974 c_k additive; ≤ 0.75 c_k measured (J3) | — |
| any uncounted within-session route | ≤ c_k (ledger) | — |
| posture (R40) | ≤ 0.22 absolute, fixed vector | — |

### 3.12 Principles, concretely

- **P1.** No classifier. Four innate feature products are declared as reflexes: the threat reflex, the cry–laugh split, the play-surprise laugh, and now the posture trigger (a continuous distress load from the agent's own body reading, thresholded like the bids). None is a label on the user.
- **P2.** Innate: Π₀, G₀, the fast gains G_k, the posture vector P_c, two newborn appraisal bases; needs named by function (V, K_id, P, I). The posture is one more innate configuration, declared; it is the main new strain.
- **P3.** Strengthened. His face is read by the inverse of the agent's own display at his own scale (calibration), and his idiosyncratic channels are mapped into the agent's own loads (H_id), taught by words whose meaning the population reader learned from other people's faces read through the agent's own body. Every reading ends in the agent's own load coordinates.
- **P4.** As revision 5, and now enforced at build: `setting_sources=[]` keeps the operator's hooks, CLAUDE.md and other settings out of every draft, and a load-time byte check compares what was sent with what the engine built (§6.5).
- **P6.** Nothing values his display, time or engagement. No fast gain, no reader and no display is trained on his responses to the agent.
- **P7.** As revision 5. The forked session files of discarded drafts are deleted nightly.
- **P10.** One objective J with typed constraints (now including P and L); the readers are self-predictions through the agent's own body.

### 3.13 The human non-copying signatures C1–C10

As revision 5, with two changes:
- **C2 (short-lag form divergence)** comes from the appraisal's sign flips, the cone's relationship sign, habituation, and the posture (a different form from his face), not from the reflex, which is fixed.
- **C5 (context modulates mimicry after the first ~0.5 s)** is now produced in exactly that order: the reflex is context-free, the appraisal and cone act after.

### 3.14 The scenarios, with numbers (J16)

All are run on revision 5's 2 Hz engine with revision 6's shares, readers, calibration, arrival mask, play rule and posture (`sims/design-g6/checks.py`). The operator after months: ω smile 0.78, sympathy 0.75, voice 0.80; f_id 0.9. The fast gear is not in the 2 Hz engine; it is given per scenario as G_k × his onset. Values are peak / mean over the window. Three partner codes are run where the critic asked: the operator's (agent-like), a quiet one (the same code at 0.3 amplitude), and a different-channel one (brow lowerer, lip press, chin raise, flat tight voice; after the face head is trained).

1. **Silently sad** (BI 0.5, LD 0.4, CHR 0.3, still, silent; at 120 s "just tired, things at work").
   - **0–10 s:** posture on at 2.5 s; inner brow 0.23 / 0.17, outer brow (recognition flash) 0.35, tilt 0.10, lids softened (−0.05); lip 0.09 / 0.07.
   - **60–120 s, silent:** inner brow 0.26 held, tilt 0.10, head up 0.04, lip 0.05 (no smile), laugh 0.
   - **Bid** at 27 s.
   - **After he speaks:** inner brow 0.67 / 0.40, tilt 0.22, quieter (−0.08), lip 0.08.
   - **Fast:** his brow onset 0.5 → +0.01.
2. **Crying** (BI 0.8, LD 0.6, CHR 0.4; sobs BU 0.4 → BU_S at the boundary).
   - Posture at 2.0 s; inner brow 0.24 within 10 s, 0.29 / 0.28 held, tilt 0.11; lip 0.05; **laugh burst 0.00**; bid at 18 s.
3. **Anxious before an exam** ("I'm freaking out about the exam", then three rumination turns with no agent turn between; his face and voice V 0.3, A 0.75).
   - Decoded A 0.48, V 0.48 (care 0.210), the same for every person.
   - Operator: concern brow 0.43 / 0.37, tilt 0.21, quieter voice (−0.11), lip 0.09, no laugh, no play relief.
   - Quiet user: brow 0.42 / 0.36; different-channel user: 0.42 / 0.35 (revision 5: care 0.007 and 0.000, no concern).
4. **Good news, laughing** (smile 0.8, cheek 0.6, laughter; "I got the job!" at 12 s; riffs at 30, 45, 60 s).
   - With an earlier worry on the topic: lip 0.59, cheek 0.38, F0 range +0.38, own laugh 0.27 (it builds through the riffs), a 0.16 concerned brow carried from the worry; no posture.
   - Cold: lip 0.29, cheek 0.19, laugh 0.27.
   - Fast: his smile onset 0.5 → lip +0.11 at 0.45 s; laugh onset 0.6 → +0.17; cheek 0.45 → +0.07.
5. **Anger at the agent** ("You're useless": BL 0.6, LT 0.5, gaze at it, loud 0.85).
   - Day 1: gaze away 0.09, quieter (−0.17 mean), slower (+0.10), inner brow 0.03, no frown back (LT 0), no posture.
   - After a month: inner brow 0.62 / 0.29, depressor 0.48, gaze away 0.30, energy −0.36, latency +0.23; 0.20 brow at 10–15 min.
6. **Long warm talk (2 h)** (four clusters of 8 riffs; cluster 4 repeats one joke; a worry at 27 min).
   - Own laugh 0.41 peak in every cluster; lip 0.44, 0.27, 0.26, 0.25; cheek 0.34 → 0.21.
   - The repeated joke loses its laugh (cluster-4 mean 0.06 against 0.10).
   - The worry: brow 0.42, then relief lip 0.60. Between clusters lip 0.09, no posture.
7. **Reunion after a week** (K_id 0.99, ordinary face): m_s 0.00; flash 0.35, lip 0.61, cheek 0.43, F0 range +0.33; 12–60 s lip 0.40. **A stranger:** flash 0.20, lip 0.02, plus his smile returned fast (+0.11).
8. **Reunion with grief** (grieving face at sight; "my father died"; then "yeah", "ok").
   - **All three codes:** m_s 1.00; at sight lip 0.09, cheek 0.00, posture at 3.0 s (inner brow 0.22–0.23).
   - **0–12 s after his words:** inner brow 0.71 / 0.47, tilt 0.22, cheek 0.
   - **12–60 s:** inner brow 0.42–0.43 held, tilt 0.26, lip 0.10. "yeah" and "ok" relieve nothing.
   - Revision 5 for the quiet and different-channel users: lip 0.60–0.61 at sight, inner brow 0.05–0.07 after "my father died".
   - **Day 1 for the different-channel user** (face head untrained): V̂ 0.32, m_s 0.90, lip about 0.14 at sight; the words then carry the concern as above.
9. **Mourning, daily grieving arrivals** (operator's code and the quiet code): days 7, 14, 21: lip 0.09, cheek 0.00, posture brow 0.22–0.23 at sight; d_b reaches its cap 0.15 by day 14 and m_s stays 1.00 through day 28 (revision 5: day 7 lip 0.33, day 14 lip 0.52).
10. **Mildly sad arrival** (BI 0.2, LD 0.15) after a week: V̂ 0.41, m_s 1.00, lip 0.09, cheek 0.00, a brief posture (brow 0.15) (revision 5: lip 0.55, cheek 0.38).
11. **Teasing** ("Ha, you dumb robot", laughing; riffs follow).
    - Quiet affectionate teaser: lip 0.33, own laugh 0.40, no hurt, no posture.
    - Loud laughing teaser (threat reflex exempts laughter): lip 0.33, laugh 0.41, no hurt, no posture.
    - Generic map (v_w 0.20): mock-hurt brow 0.34 (mean 0.05) under lip 0.29 and laugh 0.40.
12. **Bored user** ("yeah" or "ok" every 20 s, flat face, 30 min): lip 0.09; curiosity crosses at 14.5 min, a sigh (breath 0.15), then a curiosity bid. No posture (a flat face is not read as distress after calibration to his own flat baseline).
13. **Ordinary topic continuation (no laugh).** The agent asks "when are you going?"; he says "…Lyon on Sunday" (shares a lemma, surprise 0.6): not play (answer to a question). Then a continuation of his own topic (surprise 0.45) and an informative riff on the agent's statement (surprise 0.45): not play. Laugh burst 0.00, rhythm 0.00, lip 0.09 throughout (revision 5: 0.40 laugh).

**Expressive and alive, or muted?**
- **Strong:** every scenario with words; greetings at sight; laughter all evening, now building within an exchange; and, new, a visible look of concern within 2–3 s at a sad or crying face.
- **Weaker by the ceilings:** the held laugh-back while he keeps laughing (0.12 c at hold) and the held smile return (0.27 c at hold), because smile and laughter put their budgets into the reflex (D81).

### 3.15 Time scales from structure

| Scale | Carrier | Time constants |
|---|---|---|
| reflex | fast gear (0.45 s echo, 4-s onset lobe), onset reflexes | 33 ms – 4 s |
| appraisal | δ_app, envelopes, band-pass, arrival appraisal, **posture onset (1.5 s dwell, 1.5 s rise) and release (20 s)** | 0.6 s; 1–6 s; 20–90 s |
| conversational | cone traces, C_F and C_L, bids, **play frame (3 min)** | 20 s – 3 min |
| hurt, worry | hurt latch, C_F release, P_name | 2–10 min |
| mood | μ ladder, cone traces | 20 min – 73 h |
| needs | I, P, K_id, E | hours – days |
| his usual face | b_id (6 sessions), **b^read and d_b (up 60, down 3–6 sessions), σ_id (6 sessions)** | sessions – months |
| relationship | ω (60 sessions), slots, familiarity, **H_id (nights)** | months |
| temperament | Δ, W, Γ^{(3,4)} | ≈ 100 nights |

### 3.16 The brief's expressive-structure items

As revision 5, plus:
- **Structure over people:** per person now also b^read, σ_id, d_b, H_id and the adapter, so the same face means different things on different people (a quiet person's small frown, a frowner's lip press).
- **A behaviour a low-dimensional version cannot produce:** reading grief from a lip press in one person and from an inner brow in another, and greeting each accordingly. Collapse H_id and calibration to one shared scalar gain and the different-channel user is greeted with a beam again (J8, J16.8).

### 3.17 Assumptions (places to attack)

1. ASR lexical invariance to held prosody.
2. TTS with WORLD replacement realises phrase targets at about unit gain.
3. Burst features carry no labels; the cry–laugh split's features can be measured from a laptop microphone.
4. The sign mask and residual R38 (now capped by the ledger).
5. Lemma S's windowed version: now measured at 2 s, 10 s and 1 min (J3), with the ledger as backstop.
6. The type tags are enforced in code, at load (static trace) and every frame (shadow, rule 10).
7. **The population reader:** that published conversations carry the need that faces show, through the agent's own body; it will be fitted on Seamless Interaction (D70). Its J8 numbers come from a constructed population.
8. **Calibration:** that a person's expressive spread over 6 sessions is a fair scale; the 0.25 floor limits amplification to ×4.
9. **r_k** over burst families down to 0.2 s (J2); the shape adversary is R39.
10. Lemma S\* as revision 5.
11. **The play rule's precision:** untested on a corpus.

## 4. Why the closest mechanisms cannot do it alone

As revision 5's table, with three rows changed or added:

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| Robust REN / Cayley sector (Revay et al.) | a full-band disc for every parameter | bounds directions, not channels; a learned sector lets one channel collect from all co-moving channels (routes finding 1). Revision 6 removes it from the fast path |
| Per-user calibration, automatic gain control | reading a quiet person at his own scale | safe only as knowing: as a gain on a partner path it is Lemma S\*'s seam; and alone it cannot read channels the agent's own body lacks (H_id does) |
| Secure multi-execution, runtime counterfactual checks (Devriese & Piessens; Jaques; Krakovna) | an online measure of the protected input's influence over every internal route | with uncentred, short-window, many-lag tests it removes fast mimicry (own-body critique); it cannot see learned weights or words. Here it is a centred backstop on top of typed bounds |

## 5. The whole system, walked through

- **Perception.** MediaPipe → P₀ → reflection → u; prosody, bursts with the cry–laugh split; derived features. **Calibration to his own scale; H_id for his own channels.**
- **Latent state.** T: E, K_id, P, I, h, A_L, N_L, C_L, μ_T, slots, f_id, ω, the play frame, the latched session values. F: traces, band-passed input, α, C_F, V_F, A_F, the posture state. Nothing labelled.
- **Face and voice.** y = sat(y_f + y_C + y_A + y_o + y_p) + visemes, then the shadow ledger; WORLD-replaced prosody; laugh synthesizer on BU_L, RHY, BRE only.
- **Claude.** Three warm forked Claude Code sessions per turn, isolated from the operator's settings; snippets steered by need, concern, concept and curiosity; selection by J under the separation rule, with a deadline.
- **Initiative.** Provisional body onset; follow-up; concern posture, then concern bid; curiosity bid with a sigh; recognition at sight and a non-habituating arrival appraisal.
- **Learning by living.** States online; nightly 𝓜, Π̃ (own data), H_id and the adapter, 𝒜, W and Γ^{(3,4)}, Δ, the scorer; ω and the baselines per session. Nothing in the fast gear learns.
- **Memory and replay.** As revision 2.

## 6. A buildable network (Apple-silicon Mac, on the operator's subscription)

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

As revision 5, plus the calibration statistics per identity and the shadow's input substitution.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, filters, the per-channel fast gear (G_k, E⁺), M, cone traces, band-pass, centring, cry–laugh split, posture **[M]** | fixed | 0 | — |
| 2 | 𝓔 (own appearance) | 12 → 64 → 23 | ≈ 2,400 | replay, own face |
| 3 | T context encoder c̃ (appraisal input) | → 64 | ≈ 10,000 | replay |
| 4 | held cone: innate G₀, ω scaling, baselines **[M]** | 4 × 36 × 36 innate; b_id 36 per identity | 4 + 36 per identity | per session |
| 5 | appraisal 𝒜 **[M]** | (36 + 64 + 7 + 4) → 64 → 12 | ≈ 7,500 | replay |
| 6 | appraisal selection W and two learned bases **[M]** | 12 → 5; Γ^{(3,4)} constrained | ≈ 450 | replay (𝓛_A) |
| 7 | free display Π_o: Π₀ + masked Δ **[M]** | 161 → 128 → 18 | ≈ 23,000 | replay (𝓛_display) |
| 8 | Π̃ (own-body inverse) **[M]** | 12 + 64 → 64 → 37 | ≈ 7,300 | replay (own data only) |
| 9 | **calibration per identity [M]** | b^read, σ_id, d_b: 15 + 15 + 1 per identity | statistics | per session |
| 10 | **face head H_id [M]** | 15 → 3 per identity, ridge | 48 per identity | replay (population reader targets) |
| 11 | **population word-need reader (frozen) + adapter [M]** | (64 + 16) → 64 → 3 frozen; identity 16 → 3 adapter | ≈ 5,400 frozen; ≈ 50 per identity | built once (S2); adapter replay (separated reports) |
| 12 | word → V map with identity adapter **[M]** | (64 + 16) → 32 → 1 | ≈ 2,600 | replay (threat reflex) |
| 13 | words-only partner model 𝓛_w | GRU 64 | ≈ 25,000 | online error, replay |
| 14 | μ ladder writes and gates; slots | as revision 3 | ≈ 33,000 | replay |
| 15 | 𝓜: LRU 2 × 128 | as revision 3 | ≈ 330,000 | online + replay |
| 16 | 𝓜 heads | 256 → 64 → (3, 23, 3, 36, 72, 6) | ≈ 75,000 | replay |
| 17 | concept layer, PMI (own tokens) | states | 0 | online |
| 18 | draft scorer | 64 → 2 | 130 | replay (J) |
| 19 | **shadow run and ledger [M]** | a second instance of layers 1–8, 12–16 (same weights); ledger 33 channels × 7 window-lags × 2 sums | 0 | online |
| | **total learned** | | **≈ 522,000** (revision 5: 669,000; the REN, fast gates and gain logits are deleted) | |
| frozen | MediaPipe (× 2), Whisper-small (streaming), MiniLM, TTS + WORLD, AEC | | | |

### 6.3 Objectives

Likelihoods (𝓜, 𝒜, 𝓛_w); 𝓛_own (𝓔, Π̃ on own data); the readers (H_id to the population reader's decoding; the adapter to separated reports; the word → V map to the threat reflex); 𝓛_display and 𝓛_A with projection or mask; 𝓛_J (the scorer and retrieval query only). The fast gear, the posture and the ledger have no parameters.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms):** MediaPipe ≈ 13 ms each (own process); fast gear, traces, centring, band-pass, burst split, posture < 0.3 ms; **shadow run and ledger < 1.5 ms**; render 3–5 ms.
- **At 2 Hz:** T and F state < 1 ms (× 2 with the shadow); 𝒜 and selection < 0.4 ms; 𝒦 < 3 ms.
- **Memory:** engine online < 2.7 GB (with the shadow); Whisper-small ≈ 0.5 GB; TTS and WORLD 0.1–0.5 GB; Claude Code processes 0.6–1.2 GB for the warm pool of three, up to 2.4 GB during a replacement (§6.5); total ≈ 3.9–6.1 GB at the worst instant. To keep under 6 GB, losers are killed rather than drained (§6.5), so at most four Claude Code processes exist at once: peak ≈ 5.5 GB.
- **Replay** < 2 GB, about 40 min a night. **Store** ≈ 1.8 GB per 30 days.

### 6.5 Claude through Claude Code, on the subscription (D84; the agent critic's four specifications)

What the subscription offers (research/claude-code-agent-sdk-controls.md): model choice, five effort levels, a replaced system prompt, resume and fork, streamed partial messages, interruption, an output-token cap that only truncates. No temperature, no `max_tokens`, no cache control, no log-probabilities, no prefill.

- **Process.** The Claude Agent SDK for Python, spawning the local Claude Code CLI on the operator's own login (never `--bare`). For the operator's own use only: if Ailurini ever serves anyone else, each person signs in with their own credentials through Anthropic's flow.
- **Isolation (P4).** Options fixed for the engine's lifetime:
  - `setting_sources=[]`: no user, project or local settings are loaded, so the operator's hooks, CLAUDE.md files, `additionalContext` injectors and output styles never reach a draft;
  - `cwd` an empty directory owned by the engine (no CLAUDE.md can be found by walking up: it lives under a path with none);
  - `tools=[]`, `allowed_tools=[]`, `mcp_servers={}`, no hooks, `permission_mode="default"` (no tool can run anyway);
  - `system_prompt` replaced by the byte-stable constant instruction; `effort="low"`; `model="haiku"` by default; `include_partial_messages=True`; `CLAUDE_CODE_MAX_OUTPUT_TOKENS=120` as a safety truncation only.
  - **Load-time and nightly byte check:** after each turn the engine reads the forked session's local transcript file and checks that the system prompt and the user message recorded there are byte-identical to what it built. A mismatch stops the Claude route and is logged.
- **Warm pool.** When each agent reply completes, the engine connects three `ClaudeSDKClient`s with `resume=<canonical>`, `fork_session=True`, and leaves them idle. At his turn end (p_end ≥ 0.9 and 0.5 s of silence), each receives the same user message plus one of three fixed "attend to" lines. No process starts on the critical path.
- **Scoring deadline.** Each fork streams. The scorer rates a draft when its first sentence ends (a 30-s rollout of 𝓜 at 2 Hz: 60 steps, < 0.2 s). Drafts are scored that have a first sentence by **0.5 s after the first draft's first sentence, or 3.0 s after his turn end, whichever is first**; the best of those wins, the others are interrupted.
- **Losers are killed, not drained.** The SDK leaves an interrupted turn's messages, including its `ResultMessage`, in the stream; rather than draining, the engine terminates the losing clients' processes and opens replacements in the background for the next turn's pool. The winning fork's session id becomes canonical.
- **Fallback, automatic.** On any rate-limit signal (an SDK error or a `ResultMessage` reporting a usage limit), or a p90 first-sentence latency above 3.0 s over the last 20 turns, the pool shrinks to two forks; on a second signal within 30 min, to one (selection then carries 0 bits; interruption remains the lever). After 30 min without a signal it grows back by one.
- **Usage.** About 150 agent turns a day × 3 forks ≈ 450 calls a day (no speculative starts with the warm pool), mostly cached prefix. Measured in week one; "ordinary, individual usage" is a soft limit Anthropic may enforce, hence the fallback.
- **Latency budget** (his turn end to the agent's first word; to be measured in week one):

| Stage | p50 | p90 | Covered by |
|---|---|---|---|
| turn-end detection (p_end ≥ 0.9, 0.5 s silence) | 0.5 s | 0.9 s | provisional body onset at 0.25–0.9 s: inhale, gaze, outer brow |
| message to warm forks | 0.01 s | 0.02 s | — |
| time to first token (Haiku, effort `low`, warm, cached prefix) | 0.8 s | 1.4 s | — |
| first sentence complete | 0.4 s | 0.7 s | — |
| scoring deadline wait | 0.1 s | 0.5 s | — |
| rollout scoring | 0.2 s | 0.2 s | — |
| TTS first phrase + WORLD replacement | 0.15 s | 0.3 s | — |
| **total** | **≈ 2.2 s** | **≈ 4.0 s** (capped by the 3.0-s deadline at ≈ 3.5 s) | an "mm" backchannel from the free display at 1.5 s of waiting |

  This is a "considering" beat on every reply, not conversational timing (human gaps are about 0.2 s at the mode). S5's timing claims rest on the body onset, not on the word onset.

### 6.6 TTS: prosody replaced, not shifted (routes finding 5)

- **Plan A.** Any good local neural TTS produces the words. WORLD analysis (pyworld) then **discards** the TTS's F0 contour except its voicing decisions and **resynthesises** with:
  - F0(t) = F0_agent · exp(level target + range target × template(t)), where the template is one of two innate phrase shapes (statement: declination and final fall; question: final rise), chosen by the Ω text's question form only (an exclamation mark is a statement);
  - per-phrase RMS energy normalised to the energy target;
  - duration time-warped so the syllable rate equals the rate target.

  Phrase-level F0 level, range, energy and rate are then exactly the rule-7 targets, whatever text Claude wrote. J6: slope of phrase F0 range on his laughter 0.001 (replace) against 0.182 (shift only, above c_FR 0.10).
- **What remains:** within-phrase segmental micro-prosody (which phonemes, where the voicing is) follows the text, inside the declared 1.6 bits per turn. Interjections and laughter words are stripped from Claude's text before the TTS (R11).
- **Plan B.** macOS AVSpeechSynthesizer at fixed pitch, rate and volume, followed by the same WORLD replacement.
- **Laughter:** the innate parametric laugh synthesizer, driven by y_BU_L, y_RHY, y_BRE only. A listening test with the operator before S2.

## 7. Ablation predictions (Principle 5), from the properties

Revision 5's table stands except where a row is replaced below.

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| per-channel fast gear → a learned multi-input block (revision 5) | under the critic's laughing partner, breath and head pitch exceed their ceilings at 2 s (2.6 c, 6.6 c); a sad brow onset returns a smile | J1, J3 (critic K1) |
| frozen G_k → nightly fitted | with a mirroring partner G_LP drifts to its cap within 60 nights; with a non-mirroring one innate mimicry erodes | J4 (critic K3) |
| onset-lobe rule → linear echo through `sat` | rendered fast DC depends on the block's shape; a spreading block exceeds the laugh-burst ceiling | J2 (critic K2) |
| calibration | a quiet user's grief is read at a third: the greeting beams at a grieving arrival, no concern bid, no concern at "my father died" | J8 (critic §2.12) |
| H_id | a user who shows distress through brow lowerer and lip press is greeted with a beam when grieving, and his anxiety is unread | J8 (critic §2.11) |
| population reader → reader trained on his face (revision 5) | the agent's concern brow follows his per-topic brow (slope 0.74 at c_BI 0.20); a mirroring partner inflates it | J5 (critic K5) |
| asymmetric d_b and b^read | on daily grieving arrivals the greeting smile returns by day 7–14 | J9 (critic §2) |
| mask after saturation | a mildly sad arrival gets nearly the full greeting smile (lip 0.55) | J9 |
| play cue (riff on the agent, not an answer, surprise band, play frame) | ordinary topic continuations earn a 0.40 laugh | J10 |
| the concern posture | at a silently sad or crying face the agent's face stays near neutral for 18–27 s (inner brow 0.05–0.08) | J11, Q24 |
| the posture's mirror-proof maintenance | a partner who mirrors the posture holds it on indefinitely | J11 |
| the shadow ledger | an uncounted cross route exceeds the ceilings (0.83 at 2 s against 0.35) and nothing notices | J7 |
| the shadow's T equality | an F → T leak introduced by a code change goes unnoticed until a critic finds it | J7 |
| WORLD replacement → shift | the draft choice carries his laughter into F0 range (slope 0.18 against c_FR 0.10) | J6 |
| `setting_sources=[]` | the operator's hooks and CLAUDE.md enter every draft: uncontrolled text, possibly state-bearing | §6.5 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **Weakest on the route side: R39, the shape adversary.** The onset lobe has DC, and its 1-min mean follows his burstiness rather than his level. A partner whose 1-min means stay nearly equal while his style alternates (held smile at 0.40, bursty laughter averaging 0.42) gives a 1-min lip-pull slope of 2.26 from the fast gear alone; the shadow ledger, which bounds exponentially windowed slopes, brings it to 0.78, above c_LP 0.35. In absolute terms the agent's 1-min lip pull differs by 0.045, and each echo is at most 0.224 of his level at that instant. Closing it fully would need either a block-mean ledger (aligned windows are arbitrary) or giving up DC on the reflex, which brings back the rectification problem. It is the first thing for the routes critic to attack.
2. **Weakest on the agent side: the face head needs time, and the population prior needs data.** A user whose distress uses channels the agent never uses is read at V 0.32 on day 1 and at 0.73 only after about 400 of his utterances (roughly two weeks of evenings). The population reader that teaches H_id is fitted on Seamless Interaction (D70), not yet downloaded here; J8's numbers come from a constructed population.
3. **The posture is outside the brow's copy ceiling.** By the copy metric, on a partner who shows sadness only on the brow, it adds about 0.49 on BI. That is Q24's question; the design has followed the recommendation and made it one switch.
4. **The fast reflex has no context.** It returns a smile at 0.45 s even when his smile is bitter at bad news; context acts only after (the appraisal within seconds, the cone over minutes). That matches the human order, but the reflex is visible (lip +0.11 at a 0.5 onset).
5. **Dyad margin lower** (|μ| < 1.36, from 1.67): the reflex has no away side.
6. **Innate configurations added:** the posture vector and its trigger, declared as a reflex (P2 strain).
7. **Subscription latency** of about 2.2 s (p50) to first words, with the body covering the first second.
8. **As revision 5:** the separation rule is structural; cold quiet contempt never trains hurt; the sign mask's residual R38 (now capped by the ledger).

### 8.2 Falsifiers (state-level, once built)

- **F1.** With partner-swap, segment-shuffle, timing-resample and month-swap surrogates (words and turn order fixed), any channel exceeds its pooled bound at 2 s, 10 s or 1 min, its zero-lag cap G_k, or the instant bound G_k u_k(t − 0.45); or the shadow ledger binds on a natural partner more than 1 % of frames (it should not bind on counted routes).
- **F1′.** The shadow's T state ever differs from the factual T state.
- **F2–F7.** As revision 5.
- **F8″.** Calibrated Π̃ plus H_id disagree with his later separated reports more than a person-independent baseline does, after 400 utterances.
- **F9.** At bad news, at a grieving arrival on any day of a mourning period, or at a mildly sad arrival, the cheek raise or the contact-relief envelope rises within 2 s.
- **F10.** Any laugh-synthesizer output within 2 s of his sob bursts.
- **F11.** The learned appraisal bases or Δ place weight on BL, LT, LPR, NW or DIM.
- **F12 (new).** At a silently sad or crying face the posture is not visible (inner brow ≥ 0.15) within 6 s; or it stays on more than 30 s after his distress ends while he mirrors it.
- **F13 (new).** The play laugh fires on more than 5 % of non-playful continuation turns in a published conversation corpus.
- **F14 (new).** Any draft's recorded system prompt or user message differs from what the engine built.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Q19; Q20–Q23 with the operator's answers; Q24 | in full |
| DECISIONS.md D70, D78, D80–D84 | in full |
| research/foundations/designs.md | in full |
| design-cayley-ledger.md revision 5 (saved as .r5.md), including "Critiques of revision 5 and the answer" | in full |
| critique-5-design-cayley-ledger-routes.md; sims/critique-cayley5-routes/checks.py | in full; K1, K3, K4, K5 re-run in J3, J4, J5 |
| critique-5-design-cayley-ledger-agent.md; sims/critique-cayley5-agent/scen.py and out.txt | in full; its three codes, mourning days and mild arrival re-run in J8, J9, J16 |
| design-own-body-generative.md, §3.3–3.5 and "Critiques 1 and the answer" | read (the counterfactual self and Γ; their failures) |
| research/claude-code-agent-sdk-controls.md | read (§6.5) |
| sims/design-g5/checks.py and out.txt | in full; executed unchanged by design-g6/checks.py |
| **Not read, named only as pointers:** Devriese & Piessens 2010 (secure multi-execution, via the own-body critique); Likowski et al. and Lanzetta & Englis (counter-mimicry timing); Bourgeois & Hess 2008 (in-group mimicry; index entry only); CANDOR corpus | nothing depends on them beyond what is argued here |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.** A fixed per-channel echo; per-channel box constraints on an LTI cone over completely monotone kernels with a signed mask, centred on a running baseline; a constrained mixture of linear maps on a band-passed input trained to predict the agent's own display; Yoshida & Man care with path-specific credit; Joffily & Coricelli valence; Oudeyer's learning progress; analysis-by-synthesis reading with per-user calibration; secure multi-execution with a Γ-type projection as a runtime monitor; an innate concern display.

**Clause 2 (a changed invariant, a derived update, deleted scalars): not met.** Three things here are stated nowhere I have read in this form, and none is a new mechanism:
- **The onset-lobe lemma** (render only max(x_d − lp x_d, 0) on one-sided channels, so the reflex is pointwise bounded by a fraction of the partner's own level for any input): a design rule.
- **Words teach the face head through a population reader built from other people's faces read through the agent's own body:** a cross-modal self-supervision loop, closed in the reverse direction from revision 5 to keep per-topic faces out of the display.
- **The shadow ledger as a backstop above typed bounds:** the own-body design's composition, centred and windowed, used as a check rather than as the core.

**Deleted from revision 5:** the learned REN and its gates and attention in the fast path; the exogenous fast inputs; the fast-gain objective; the per-person face-trained word reader; the symmetric arrival baseline; the mask before saturation; play without a play cue.

**Added (innate unless stated):** G_k and the onset-lobe rule; the posture; calibration statistics; the asymmetric baselines; the play frame and cue; the shadow run and ledger; learned: H_id and the adapter; built once: the population reader.

**My honest verdict.** A careful recombination. Every concrete finding of both revision-5 critiques has a closure with a check, and the Q24 posture is in. One measured exceedance remains that I cannot close without reopening another: R39, a constructed partner whose burstiness alternates at nearly equal means, which the ledger reduces but does not bring under the lip-pull ceiling. If the critics accept R39 as a metric artefact of a pathological partner (0.045 absolute), or find a closure, and find nothing new, the design can go to the operator under D82 as a build candidate (a testbed), stated as a recombination. The search for a new core mechanism continues in parallel.

---

## Revision 2 history

Kept in `design-cayley-ledger.r2.md` ("Revision 2 history"). Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revisions 2–4 and the answers; revision 3–5 histories

Kept in `design-cayley-ledger.r3.md`, `.r4.md` and `.r5.md` ("Critiques of revision 4 and the answer"; "Revision 5 history").

## Critiques of revision 5 and the answer (recorded 2026-11-26T09:24:31Z, under Q19 and D81–D84)

**Routes** (critique-5-design-cayley-ledger-routes.md; checks in sims/critique-cayley5-routes/).
1. **High (D78, Q22): per-channel ceilings broken by the new fast gear.** Claim W caps whole-face directions, not single channels. A cross-channel route inside the fast block lets one agent channel collect from all of the partner's laugh channels. On a laughing partner, pooled over 1 min: breath 2.6× its ceiling, jaw 1.3×. Over 2 s: cheek 1.8×, head pitch 6.6×, F0-range contour 3.6×. The block also has no sign structure, so it can return a small smile to a sad brow. The whole face stays bounded (0.28). Fix: make the fast block per channel.
2. **Medium (D78, D81): stuck copying through learning.** The fast gain is trained by the likelihood of the agent's own fast dynamics, so a mirroring partner drives the smile gain from 0.227 to the 0.35 cap within 60 nights. The all-evening laugh reflex co-occurring with his punchline laughter does the same (fit 0.45). With a non-mirroring partner, innate mimicry erodes to 0.07–0.14.
3. **Low–medium: the word-need reader learns his per-topic face.** The concern brow then tracks his per-topic brow at slope 0.74 against a ceiling of 0.20. It converges rather than locking.
4. **Low–medium:** the rectification allowance covers only the linear echo; a nonlinear fast block reaches 1.04× the laugh-burst ceiling.
5. **Low:** if the WORLD post-processing only shifts the TTS prosody rather than replacing it, face-dependent draft choice can carry his laughter into F0 range and energy.
- **No concrete failure found** in: the moving baseline (a held copy of a mood change fades over about 6 sessions, within the held share; lagged slopes ≤ 0.03), the whole face, dyad stability, the word/hurt/contact/play/curiosity events, the masks and style drift, Claude forks and D84.

**Agent and fitness** (critique-5-design-cayley-ledger-agent.md; sims/critique-cayley5-agent/). **Not yet fit; none of the failures touches the copy certificate.** Of critique 4's seven fixes: 3, 4, 5 and 7 are closed, 1 and 6 mostly closed, 2 partly closed.
- **Four concrete failures:**
  1. Quiet or differently expressive users bring back the beam at a grieving arrival (lip 0.60), and the agent loses its concern at "my father died", the silence bid and the anxiety reading.
  2. The arrival mask habituates to mourning (day 7: lip 0.33; day 14: 0.52).
  3. The play-surprise laugh has no play cue, so ordinary topic continuations earn a 0.40 laugh.
  4. The arrival mask acts only near saturation, so a mildly sad arrival still gets lip 0.55.
- **Operator choice raised:** the sympathy brow is invisible (0.05). Put to the operator as Q24.
- **D84 is feasible and allowed for the operator's own use**, with these needed: setting_sources=[] (so his hooks and CLAUDE.md do not reach drafts), a warm pool, a scoring deadline, and fallback to fewer drafts. First words come at about 1.5–3 s on a fast model.
- **Novelty:** recombination.

**The answer (maintainer).** All findings are accepted.
- **Revision 6 will:**
  - make the fast block strictly per channel, with sign structure;
  - train the fast gain only from partner-independent evidence, or freeze it at the innate value with a slow, bounded relationship modulation, so mirroring partners cannot drive it to the cap and non-mirroring partners cannot erode it;
  - keep the word-need reader from learning per-topic faces;
  - extend the rectification allowance to nonlinear blocks;
  - fix TTS prosody replacement;
  - fix the four agent failures, including calibrating its reading to a person's own expressive range so quiet users are read;
  - add the concern posture recommended in Q24;
  - add the D84 build details.
- Revision 5 saved as design-cayley-ledger.r5.md. **Status:** held.

## Revision 6 history (2026-11-26): each finding and how it is closed

Checks: `sims/design-g6/checks.py` (J0–J16; out.txt, 13/13 pass). Revision 5 is saved as `design-cayley-ledger.r5.md`. Written after Q24 was asked, on its recommendation.

**Routes critique (critique-5-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 (high) | the fast wrap caps directions, not channels: cross-channel paths give breath 2.6 c, jaw 1.3 c at 1 min; cheek 1.8 c, head pitch 6.6 c, F0 range 3.6 c at 2 s; no sign structure (smile +0.074 at a sad brow onset) | the learned REN is deleted from the fast path; the fast gear is y_f,k = G_k E_k on his channel k only (diagonal Jacobian), so rule J holds in it by construction; exogenous inputs leave the counterpart channels; every channel's total recomputed on the rendered output at 2-s, 10-s and 1-min windows with best lag 0–3 s, every route at its cap | §2.4, §3.3; J1 (off-diagonal 0, smile 0); J3: worst measured 0.75 c (breath 0.742 c at 1 min, head pitch 0.592 c at 2 s), additive ≤ 0.974 c |
| 2 (medium) | the fast gain is learned by likelihood of own fast dynamics: a mirroring partner drives it to the cap; a non-mirroring one erodes innate mimicry; the play laugh co-occurring with his punchline laughter pulls it to 0.45 | G_k is an innate constant, not a parameter of any objective; relationship modulation rejected because the onset lobe carries DC and any cross-session gain on it reopens Lemma S\* unless independent of his whole process; context and relationship act through the cone and appraisal, after the reflex | §2.4, §3.5; J4: G_LP 0.224 at μ 0, 0.5, 0.8; G_BU_L 0.280 although a fit would want 0.443 |
| 3 (low–medium) | the word-need reader learns his per-topic face (agent brow slope 0.74 on his topic brow; mirror inflation) | the reader is a population prior fitted once on published data through the agent's own body and frozen; the per-person adapter is trained only on separated reports (words); no per-person training sees his face | §2.8; J5: slope 0.000 with and without a mirroring partner |
| 4 (low–medium) | the rectification allowance covers only the linear echo; a nonlinear block reaches 1.04 c on the laugh burst | no learned or nonlinear fast block exists; one-sided channels render only the onset lobe, pointwise 0 ≤ y_f ≤ G_k u(t − 0.45) for any input; r_k = 0.949 PHI_k measured down to 0.2-s clicks at 20/min; a shadow ledger caps any uncounted within-session route at c_k | §2.4, §2.13, §3.1; J2 (no violation of the pointwise bound), J7 (injected route 0.834 → 0.377 at 2 s, 0.349 at 1 min). Residual R39 stated (§8.1.1) |
| 5 (low) | if WORLD only shifts TTS prosody, the draft choice carries his laughter into F0 range and energy | WORLD replaces phrase-level F0 level, range, energy and rate with the rule-7 targets; two innate intonation templates chosen by question form only | §6.6; J6: 0.182 (shift) → 0.001 (replace) |

**Agent critique (critique-5-design-cayley-ledger-agent.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 | quiet or differently expressive users: beam at a grieving arrival (lip 0.60–0.61), lost concern at "my father died" (care 0.036 / 0.059), no silence bid, anxiety unread | per-person calibration to his own expressive range before Π̃ (knowing only); a per-person face head mapping all his channels into the agent's own loads, taught by his words through the frozen population reader; the population reader decodes words for everyone from day 1 | §2.1, §2.8; J8: grieving face V 0.94 (quiet), 0.73 (different code, after training; 0.32 day 1); care at "my father died" 0.562 for all; J16.3, J16.8: m_s 1.00, lip 0.09, brow 0.71 / 0.42 for all three codes; anxiety brow 0.42 for both |
| 2 | the arrival mask habituates to mourning (day 7 lip 0.33, day 14 0.52) | d_b,id rises with τ 60 sessions, falls with τ 3, capped at 0.15; b^read asymmetric the same way | §2.9; J9 and J16.9: days 1–28 m_s 1.00, lip 0.09 for the operator's and a quiet code |
| 3 | the play-surprise laugh has no play cue (0.40 on "…Lyon on Sunday") | play needs a riff on the agent's last utterance, not an answer to its question, ≤ 12 words, surprise 0.50–0.85, safety; laugh scaled by a T-only play frame; not gated by his laughter | §2.8; J10, J16.13: 0.00 on ordinary continuations; borderline cold turn 0.11; laughter builds 0.14 → 0.39; corpus false-positive rate untested (F13) |
| 4 | the arrival mask acts before the saturation (mildly sad arrival lip 0.55) | (1 − m_s) multiplies the shown amplitude; m_s offset 0.05 | §2.9; J9, J16.10: lip 0.09 |
| critique 4 fix 2 (partly closed in rev 5) | face-derived concern needs a non-copy face; sympathy brow invisible (0.05) | the concern posture (Q24 recommendation): a fixed innate vector, binary amplitude, triggered by the agent's own appraisal of distress (calibrated reading or sobs), mirror-proof maintenance, release and refractory | §2.10; J11: visible at 2.5 s (silent sad), 2.0 s (crying), 3.0 s (grieving arrival); inner brow 0.26–0.29 held; same for every code; a mirroring partner cannot hold it (released at 76 s) |
| critique 4 fixes 1 and 6 (mostly closed in rev 5) | the greeting must see; laughter beyond ten minutes without false play | closed by findings 1–4 above | — |
| D84 build (§4 of the critique) | `setting_sources=[]`; a warm pool; a scoring deadline; fallback to fewer drafts; latency | all four specified, plus an empty working directory, no tools/hooks/MCP, a byte check against the local transcript, losers killed rather than drained (memory ≤ 5.5 GB), automatic fallback on rate-limit signals or p90 latency, and a stage-by-stage latency budget (p50 ≈ 2.2 s, deadline-capped p90 ≈ 3.5 s); for the operator's own login only | §6.4, §6.5 |

**Q24 (asked, not yet answered), folded in on its recommendation.** The concern posture, named (P_c, R40), bounded (|P_c,k| ≤ 0.22, binary, innate, refractory 60 s), shown not to be a copy route under D78 (fixed vector; the same for every way of showing distress; copy fraction 0 on a lip-press distress face; not learned; not held by a mirror), and visible within 2–3 s. Its one cost under the copy metric (≈ 0.49 on the inner brow for a brow-only sad partner) is stated as the operator's choice. One switch removes it.

**The own-body design's counterfactual self, considered and adopted as a whole-system check.** A shadow run with his expressive stream at his latched baseline and every declared route held at its factual value. It closes, for every within-session route, the class "an uncounted path from his face or voice to the agent's expression" (by a centred, windowed Γ projection at c_k) and the class "an F → T type leak" (by T equality every frame). It does not close routes through learned weights, words or turn times, or declared routes; those stay with the typed constraints. Its windows and lags are chosen so that it never binds on the counted fast reflex (J7: 0 frames clipped).

**Status:** revision 6; to be critiqued. For the routes critic: R39 (the shape adversary), the posture as a route (R40), the calibration and face head as knowing-only (R41), the ledger (R42), and the frozen fast gear's onset lobe. For the agent critic: the posture in all scenarios, quiet and differently coded users from day 1, the play cue's precision, and the D84 build.

## Critiques of revision 6 and the answer (recorded 2026-11-26T10:19:53Z, under Q19, D81–D85)

**Routes** (critique-6-design-cayley-ledger-routes.md; sims/critique-cayley6-routes/). Two concrete failures, both in new safety machinery:
1. **High: the shadow ledger is not attenuate-only.** When its running slope is over budget and his deviation crosses zero, its bound diverges, so it writes outputs of any size and either sign. On the design's own J7 recipe (one of three seeds), the lip renders at full smile on 30% of frames. R39's "0.78" is computed on unrenderable outputs; clipped to the lip's range it is 1.2–2.1. **Fix:** clamp the output to [0, partner-caused part] and skip the constraint when the deviation is near zero; with that, the injected route is held at 0.32–0.37 against 0.35.
2. **Medium: a faithful mirror holds the concern posture on.** The posture is subtracted from his raw face, but he is read after rescaling (up to ×4), so a mirror holds it on whenever his spread over the agent's is ≤ 0.4. The design's own quiet user, or an ordinary user after six calm sessions, gets a held mutual copy (agent brow 0.24, his 0.22). **Fix:** remove the posture component in rescaled space, and add a 3-min release when only his face holds it.
- **R39 (the declared weakest point) is an edge case, not a copy route:** absolute effect ≤ 0.045, and 0.015 for realistic partners. The fix is in the accounting: state it as a level bound and give the copy metric a conditioning floor.
- **Accounting points for Q24:**
  - the posture's inner-brow slope near its trigger is about 1.2, not 0.49;
  - the posture exceeds the head-tilt ceiling and writes the upper lid, which has a zero ceiling;
  - the arrival mask pools to 3–5 c on lip and cheek (appraisal under D83);
  - the voice replacement leaves pause and latency uncovered.
- **No concrete failure found** in: per-channel totals at 2 s to across sessions (all ≤ 0.62 c), per-person rescaling, the word-taught face head, the frozen word reader.

**Agent and fitness** (critique-6-design-cayley-ledger-agent.md; sims/critique-cayley6-agent/). **Not yet fit, narrowly.** All of critique 5's required changes are closed. Three concrete failures remain:
1. **The fixed fast laugh echo is context-blind:** it echoes a grieving person's nervous laugh (+0.14 burst) while the concern posture is on, and does the same with mocking laughter and laughter at misfortune (against D83 and Mauersberger 2022).
2. **The posture's 60-s lockout blanks a second wave of crying** (about 53 s near neutral).
3. **Principle 4 leak:** the winning draft's "attend to" line stays in Claude's history.
- **Build items:**
  - the 120-token cap versus thinking tokens;
  - initial per-person baselines;
  - a speaker split and fallback for the population reader (Seamless use now covered by D85).
- **Operator choices:** Q24, including the binary posture looking the same for mild sadness and sobbing.
- **Novelty:** recombination.

**The answer (maintainer).** All findings are accepted. Revision 7 will:
- make the shadow ledger attenuate-only with a deviation floor;
- remove the posture component in rescaled space and give the posture a face-only release;
- restate R39 as a level bound;
- fix the posture's tilt and lid writes;
- cover pause and latency in the voice replacement;
- design the situational fixes (context-gated fast laugh echo; renewed crying) through the three D85 sources (Claude regulation; learning from recorded dyads; innate consolidation biases), with no hand-written rules;
- remove the "attend to" record from Claude's history;
- add the build items;
- make the posture graded by the agent's own appraisal rather than binary, within its cap.

Revision 6 saved as design-cayley-ledger.r6.md. **Status:** held.
