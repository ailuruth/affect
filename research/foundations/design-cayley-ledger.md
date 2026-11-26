# Cayley–ledger core, revision 5: know the partner fully; match fast and per expression within the ceilings; centre every slow gate; let the agent's own appraisal and body decide the rest

Seventh design of the S0 cycle, revision 5. Written 2026-11-26 under:
- questions.md Q16, and Q17 as relaxed by Q19 (DECISIONS.md D80): a precise object, a convincing argument, concrete failures only;
- Q18 and its answer (D78): no single quantity runs the whole face from flat to copy; per channel, a bounded, sign-flippable, context- and relationship-set strength under an innate ceiling, never attracting;
- the operator's answers of 2026-11-26T08:41:00Z:
  - Q20 (D81): the inner state may know the partner closely, and only expression is bounded. Humans mimic unconsciously, so **partial, fast, per-expression matching within the ceilings must stay**. Only whole-face copying and getting stuck in copying are ruled out.
  - Q21 (D82): a design with no known concrete failure goes to the operator, with its novelty verdict stated plainly.
  - Q22 (D83): per-expression innate ceilings (smile and laughter about 0.35, sympathetic inner-brow raise at a sad face about 0.20, anger, disgust and contempt 0). The partner's words, face and voice feed the agent's own appraisal, which drives its strong expressions.
  - Q23 (D84): the engine works through the operator's Claude subscription, because Ailurini is built on Claude Code. No API key, no temperature parameter, no API-only features.

Revisions 1–4 are kept as `design-cayley-ledger.r1.md` … `.r4.md`. Revision 4's two critiques:
- `critique-4-design-cayley-ledger-routes.md`, with checks in `sims/critique-cayley4-routes/`;
- `critique-4-design-cayley-ledger-agent.md`, with checks in `sims/critique-cayley4-agent/` and seven required fixes.

**Algebra checks for this revision:** `foundations/sims/design-g5/checks.py` (H0–H15). Run `python3 -I checks.py` (numpy and scipy, a few seconds); the output is in `out.txt`, 15 of 15 pass.
- Where a finding came from a critic's constructed partner, the check re-runs that partner.
- The checks test this design's own inequalities and constants on constructed instances. They are not evidence about behaviour or people (brief: no toy worlds).
- The scenario numbers in §3.14 are what the equations give for stated inputs.

**Status:** revision 5, not yet critiqued.

## 0. Summary

**What held in both revision-4 critiques, and is kept unchanged.**
- **Knowing is separated from moving.** The slow state knows his face at full rate; only expression is bounded.
- **The fast Cayley wrap.** A robust REN inside a conic sector, bias-free in the partner input, with context entering only as gates bounded by 1.
- **Lemma S within a session.** A context may gate a partner path only if that path has no DC. The held cone is latched per session. The appraisal display reads a band-passed input.
- **T1.** No rate codes in T.
- **The per-channel budgets** with a face–voice co-variation sign mask, on the rendered output.
- **Credit only from separated, partner-initiated reports;** J trains only the draft scorer and the retrieval query.
- **Satiable curiosity,** the gated and abortable body onset, and the relationship loop capped below the ceiling.

Both critics found no failure in these; the routes critic found no within-session route above the ceilings.

**What changed, in nine moves** (each closes named findings; the full list is in "Revision 5 history").
1. **Lemma S\*: centre every slowly learned gate (routes finding 1).** The relationship strength ω may be learned from anything, over weeks, because the cone diagonal it scales now multiplies his deviation from his *own* baseline b_id, not his level.
   - The baseline follows his session means with τ_b = 6 sessions; ω learns with τ_ω = 60 sessions.
   - Then the pooled multi-session toward slope is ≤ s_C c_k (1 + ρ), with ρ = τ_b/(τ_b + τ_ω) = 0.091, for any ω process.
   - On the critic's month-mood partners the slope falls from +0.31…+0.89 to +0.023, and an adversarial ω that tracks his level perfectly gives at most +0.001 (H1).
   - ω is also re-specified from T inputs only (play relief share, word hurt, credited care), graded rather than saturating (H2).
2. **Events are T-only (routes finding 2).** Relief and distress events are built only from drops and rises of word care 𝒟_p(N_L), word hurt h, K_id, P and I, and the play-surprise laugh. Face- and voice-borne care (N̂_F, V_F) are knowing only: bids, drafts, appraisal input, cone input. The spec now matches the engine (H3).
3. **One own-body map, no partner anchor, an own-display mask (routes finding 3, agent finding 5).**
   - Π̃, the inverse of the agent's own display, is trained only on the agent's own (state, face, voice) pairs. Reading him is that same map applied to his face; the 0.1 partner anchor is deleted.
   - The learned face Δ and the learned appraisal bases may never weight the anger, disgust or contempt synergies (BL, LT, LPR, NW, DIM). Fear lip-stretch and chin raise are allowed only under the agent's own distress envelope.
   - Style drift toward his code falls from cosine 0.26 to 0.000, with zero weight on the masked synergies (H4).
4. **Fast per-expression mimicry at the full ceilings (D81), counted honestly (routes low finding 4).**
   - The fast wrap's zero-lag in-phase cap is now the Q22 ceiling itself: κ_k = c_k(1 + γ_f)/(2γ_f) on smile, cheek and laughter. His smile, cheek or laugh onset is returned at 0.45 s by the innate echo at 0.65 of the cap (0.23 per unit onset on lip pull and laugh burst), and up to the full cap under context.
   - The brow, depressor and jaw keep 0.3 (inner brow 0.15) of the cap so that their held budget serves sympathy. Anger, disgust, contempt and sobs have κ = 0 (revision 4: 0.02).
   - A fast echo on a channel that rests at zero has positive DC after `sat`, and that DC is real copy. It is now measured on partner families as an allowance r_k (0.87 c on laugh bursts, 0.64 c on cheek, 0.14 c on lip pull) and charged to each channel's pooled budget, with the held shares sized to fit. Every channel totals ≤ 0.996 c (H5, H6), and the rendered total with every route at its cap is ≤ 0.76 c (H9).
5. **The greeting sees, and contact is per person (agent finding 1).**
   - At sight the agent shows a recognition brow flash. A latched arrival appraisal m_s (his face over the first second, read through Π̃ and centred at his own arrival baseline) then multiplies every contact-relief display of the session by (1 − m_s). The appraisal of his first words masks it further, as before.
   - The contact deficit is per identity (K_id), so a stranger gets a polite flash and his own smile returned fast, not reunion gladness.
   - Grieving face at sight: m_s = 1, lip pull 0.09 (its resting level), cheek 0 (revision 4: 0.63 and 0.43). The route is once per session and bounded at 0.040 on his lip pull in the first minute (H14).
6. **Real sympathy at silent sadness and crying, within the ceilings; sobs never reach the laugh synthesizer (agent finding 2).**
   - **Rule J:** no positive entry from his sadness synergy onto the agent's joy synergy, anywhere. The warm lip-pull ← brow entries are deleted, so a sad face gets no smile.
   - The inner brow's held share is raised to 0.70 c (fast 0.15, appraisal 0.05) and fills within about a minute.
   - The burst channel is split at the boundary into a laugh burst (BU_L: voiced, 4–6 Hz rhythm) and a sob burst (BU_S: irregular, ingressive, with the cry face), by a declared innate reflex. BU_S has ceiling 0, κ 0, no synthesizer and no laugh path.
   - Silent sadness: lip 0.07–0.08 (resting), inner brow 0.04–0.05, concern bid at 26 s, then inner brow 0.41 and a softer voice when he speaks. Crying: inner brow 0.08, laugh burst 0.00.
7. **The appraisal display's reactions are learned (agent finding 4, Principle 2).**
   - Selection W and two learned bases are trained nightly by one display-blind objective: anticipate the agent's own innate display 2 s ahead, projected onto the cap set at every step.
   - The hand-written reactions fall from eight bases with three rules to two newborn reflexes (glad-with and startle-orient).
   - On the training instance it learns, without a rule, a hurt-withdraw reaction to glare and a concern reaction to laughter over a sad topic (brow up, smile down), all inside the caps (H13).
8. **The agent reads states its own face shows through its own body, now including activation (agent finding 6).**
   - Π₀ gains an activation row driven by the agent's own latched lexical surprise (T): upper lid, outer brow, F0 range, rate, breathiness. Π̃₀, the innate ridge inverse of Π₀, therefore reads activation from day 1.
   - The word-need reader outputs (V, A, tiredness), trained on Π̃ of his face; K and P are dropped from it.
   - "I'm freaking out about the exam" decodes A 0.57, V 0.52, and the scenarios now decode every need from the words rather than setting it by hand (H10).
9. **Claude through Claude Code, and the smaller items.**
   - **Claude (D84):** three drafts as forked Agent SDK sessions on the operator's login, a replaced byte-stable system prompt, no tools, effort `low`, length by instruction, losers interrupted. No temperature, no `max_tokens`, no API key. R33 (valence → temperature) is deleted (§6.5).
   - **The hurt teacher** is a declared innate threat reflex, g_at · max(glare, loud · (1 − 2 f_pos)₊). Loud laughter and loud praise no longer train hurt (H11).
   - **Day-1 anger** is reported faithfully.
   - **Laughter lasts the evening:** a per-event play-surprise reflex habituates to repeated content, not to time, while P keeps only its initiative role (H12).
   - **The play rule** needs an agent turn between his turns and his word care below its dead-band, so anxious rumination does not qualify (H12).

**What is bounded, for every parameter value** (per counterpart channel k; 1 = full copy; "pooled" = regression slope over any stationary partner process, 1-min means, across sessions).

| Quantity | Bound | From |
|---|---|---|
| zero-lag in-phase (fast wrap, < 4 s) | FASTFRAC_k · c_k: lip pull 0.35, laugh burst 0.35, rhythm 0.30, cheek 0.25, breath 0.15, inner brow 0.03, outer brow and jaw 0.03, depressor 0.015; voice and head c_k; anger, disgust, contempt, sob 0 | §2.4 |
| pooled toward, rendered, across sessions | s_C(1 + ρ) + s_X + 0.636 s_A + r_k ≤ 0.996 c_k on every channel | §3.3, H5, H6 |
| the same, by channel | lip pull ≤ 0.346, laugh burst ≤ 0.348, rhythm ≤ 0.299, cheek ≤ 0.249, inner brow ≤ 0.198, breath ≤ 0.149, F0 range ≤ 0.097, energy ≤ 0.048; zero-ceiling channels 0 | H6 |
| steady hold | (s_C + s_X) c_k: inner brow 0.80 c, lip pull 0.65 c, cheek 0.28 c, laugh 0.09 c | H6 |
| all routes at their caps together, rendered (critic's laughing partners) | ≤ 0.76 c_k | H9 |
| whole face, any direction | ≤ max c_k = 0.35; laughing 0.25, sad 0.11, crying 0.12, angry 0.015, disgust 0 | H0 |
| slow ω seam, pooled over sessions | ≤ s_C c_k(1 + ρ) (0.191 on lip pull); measured worst +0.023 (rev. 4: +0.31 to +0.89) | Lemma S\*, H1 |
| arrival mask (once per session) | ≤ 0.040 on his lip pull in the first minute; across sessions −0.012 | H14 |
| away, same channel | cone ≥ −0.60; fast ≥ −0.49 | §2.4, §2.5 |
| dyad with a mimic or counter-mimic | small-gain stable for \|μ\| < 1.67 | H8 |
| copy under learning | no J path into any F → face parameter; ω, Δ and the appraisal bases trained by display-blind objectives inside the caps; the relation loop saturates at s_C c_k | §3.5 |

**The agent in the ten scenarios** (operator after months unless stated; peak / mean over the window; H15).

| Scenario | What the agent does |
|---|---|
| silently sad | no smile (lip 0.07–0.08, its resting level), inner brow 0.04 → 0.05 held, head up 0.01; concern bid at 26 s of silence; when he says "just tired, things at work": inner brow 0.41, tilt 0.09, quieter and slower |
| crying | inner brow 0.07 → 0.08, lip 0.06–0.08, no laugh burst (0.00: the sobs are routed to the sob channel, which has no output); concern bid at 27 s |
| anxious before an exam | decoded A 0.57, V 0.52; concern brow 0.23, tilt 0.13, quieter voice (−0.12); no play relief from his rumination (rev. 4: cheek 0.10, laugh 0.10) |
| good news, laughing | with an earlier worry: lip 0.61, cheek 0.39, F0 range +0.39, own laugh 0.33; cold: lip 0.37, laugh 0.33; fast: his smile and laugh onsets returned at 0.45 s (lip +0.11, laugh +0.14 per his onsets 0.5 and 0.6, up to +0.17 and +0.21) |
| anger at the agent | day 1, faithfully: inner brow 0.03, gaze away 0.09, quieter (−0.17), slower (+0.10), no frown back (LT 0); after a month: inner brow 0.62 / 0.29, depressor 0.48, gaze away 0.30, energy −0.36, brow still 0.21 at 10–15 min |
| long warm talk (2 h) | own laugh 0.41 at every cluster (rev. 4: 0.24, then 0.04–0.05), smile 0.53 → 0.26; a repeated joke stops getting a laugh; a worry: brow 0.43, then relief lip 0.61 |
| reunion after a week | at sight: brow flash 0.35, lip 0.61, cheek 0.43, F0 range +0.33; first words lip 0.51; a stranger: polite flash 0.20, lip 0.02 plus his own smile returned fast |
| reunion with bad news | grieving face at sight: m_s = 1, brow flash only, lip 0.09, cheek 0 (rev. 4: 0.63, 0.43); after "my father died": inner brow 0.50 → 0.23, tilt 0.17, lip 0.12, cheek 0 |
| teasing | quiet or loud laughing teaser: lip 0.38, own laugh 0.41, no hurt (with the rev-4 teacher the loud teaser got brow 0.60 and no laugh); generic map: brief mock-hurt brow 0.34 (mean 0.05) under lip 0.32 and laugh 0.41 |
| bored user | flat and polite (lip 0.09); the curiosity deficit crosses at 14.5 min, a sigh, then a curiosity bid; if he takes it up: F0 range +0.32, lip 0.39 |

- **New weakest point (§8.1).** Everything the agent knows of his inner state now passes through one map, the inverse of the agent's *own* display, with no partner anchor. That closes the co-training drift, but it means the agent reads him correctly only insofar as his expressive code resembles its own. A person who shows distress through channels the agent never uses (a lip press, a brow lowerer, a flat face over a tight voice) is under-read, and both word readers inherit the under-reading. Nothing but separated reports corrects it.
- **Second.** The sympathy brow at a silent sad face is real but small in absolute terms (0.05 at his 0.5 brow), because Q22's 0.20 is a copy fraction and this operator's learned ω_sym is 0.73. An absolute 0.20 at a still 0.5 brow would need a ceiling of 0.40, which is the operator's call, not the design's.
- **Novelty verdict (author): recombination**, with no known concrete failure claimed by the author (§10). Lemma S\* (centre slowly learned gates on the partner's own baseline) and the anticipation objective are design rules, not new mechanisms.

## 1. Plain-language intuition

The agent still sees the person fully. Rules about where each thought came from, and how it may reach the face, decide how its own face moves.

- **What was said, the back-and-forth, and the agent's own body** may move its face and voice strongly: missing this person, wanting to play, being hurt, being tired, being surprised, learning something new. It reads a sentence to the end before it answers it, and it never shows gladness over the top of bad news, whether the news is in his words or in his face as he arrives.
- **His face and voice** move its face in three ways:
  - **a quick gear.** Within half a second his smile, his cheek and his laugh are partly returned, up to the same limit that holds for the slow gears (about a third of a copy for smile and laughter). This is unconscious mimicry, and it stays.
  - **a held gear, set by the relationship.** How much of his smile it returns while he holds it, and how far its brow softens at his sadness. It answers his change from his own usual face, so a long good month or a long bad month cannot turn this gear into a copy of his mood.
  - **an appraisal gear.** The agent's judgement of what his change of face means ("you're laughing at what I said", "you're laughing, but what you said is sad", "you're glaring at me"). Which reaction each judgement selects is learned, by the agent noticing how its own feelings followed such moments.

  For each expression there is a built-in limit on how far these gears together can move it toward his: about a third for a smile or a laugh, a fifth for the sympathetic brow, zero for anger, disgust, contempt and sobbing. A sad or crying face never makes it smile, and sobs never make it laugh.
- **Reading him through itself.** The agent understands his face by asking which of its *own* states would have made its own face look like that. It now has a face for its own excitement, so it can recognise excitement and anxiety in him.
- **Claude** writes its words, through the operator's own Claude Code. The agent asks for three differently aimed drafts, chooses one by its own state, and hears its words back.
- **Care, gladness and curiosity** are as before: care is credited only when he later, on his own initiative, says things are better; gladness is a need being met; curiosity is a need for its own understanding to improve. Laughter is now also a reflex to a well-timed surprise in play. It fades for a joke it has heard before, not after ten minutes.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz (Δ = 1/30 s); T state, body and appraisal update at 2 Hz. Each channel is normalised to its innate nominal range [0, 1] (signed channels [−1, 1]).

**Counterpart channels (n = 33; the copy metric is defined on these).** Revision 4's voiced-burst channel is split into a laugh burst BU_L and a sob burst BU_S (§2.2, boundary). Columns:
- c_k: the innate ceiling toward the partner (Q22);
- FASTFRAC_k: the fraction of c_k the fast wrap may reach at zero lag;
- the pooled shares (s_C, s_X, s_A): cone diagonal, charged cross entries and appraisal |Γ_kk|, each × c_k;
- r_k: the fast-echo rectification allowance (H5).

| Group | Channel (code) | c_k | FASTFRAC | (s_C, s_X, s_A) | r_k |
|---|---|---|---|---|---|
| smile | lip-corner pull (LP) | 0.35 | 1 | (0.50, 0.15, 0.25) | 0.135 |
| | cheek raise (CR) | 0.25 | 1 | (0.22, 0.06, 0.08) | 0.644 |
| laughter | laugh burst energy (BU_L) | 0.35 | 1 | (0.07, 0.02, 0.05) | 0.867 |
| | 4–6 Hz burst rhythm (RHY) | 0.30 | 1 | (0.07, 0.02, 0.05) | 0.867 |
| | breathiness (BRE) | 0.15 | 1 | (0.07, 0.02, 0.05) | 0.867 |
| sympathy | inner brow raise (BI) | 0.20 | 0.15 | (0.70, 0.10, 0.05) | 0.097 |
| | outer brow raise (BO) | 0.10 | 0.3 | (0.48, 0.15, 0.20) | 0.193 |
| | lip-corner depressor (LD) | 0.05 | 0.3 | (0.48, 0.15, 0.20) | 0.193 |
| | jaw open (JO) | 0.10 | 0.3 | (0.48, 0.15, 0.20) | 0.193 |
| head and gaze | head pitch (HP) 0.10, vertical gaze (VG) 0.05; lateral, reflected by P: yaw, roll (TILT), horizontal gaze (HG) 0.03 | as listed | 1 | (0.50, 0.20, 0.35) | 0 (signed) |
| voice (phrase level) | F0 level 0.05, F0 range (FR) 0.10, energy (EN) 0.05, rate (RT) 0.05, pause (PAU) 0.05, latency (LAT) 0.05 | as listed | 1 (within-phrase contour only) | (0.50, 0.20, 0.35) | 0 |
| zero ceiling | brow lowerer (BL), upper-lid raise (UL), lid tightener (LT), nose wrinkle (NW), lip stretch (LS), chin raise (CHR), lip press (LPR), dimpler (DIM), lip funnel, pucker, mouth close, lip roll, **sob burst (BU_S)** | 0 | 0 | none toward | — |

- Sum of c_k = 2.44; mean 0.074; zero on 13 channels.
- The pooled total per channel is s_C(1 + ρ) + s_X + 0.636 s_A + r_k. It is ≤ 0.996 c_k on every channel (H6). Lip pull 0.989, laugh burst and rhythm 0.996, cheek 0.995, inner brow 0.992, head and voice 0.968.
- **The allocation follows D81.** Smile, cheek and laughter put their budget into the fast gear, because the operator asked that they be returned quickly up to their ceilings. Their held return is correspondingly small (laugh 0.09 c at hold). The sympathy brow puts its budget into the held gear, because sadness is held.

**Exogenous partner inputs** a ∈ [0, 1]³ (audio onset envelope, partner VAD, partner turn-end pulse) enter the fast block only through √κ_a, with κ_a = 0.05.

**Innate derived partner features** (F; per frame). Each carries the sign of its constituents in the mask (§2.5):
- loudness excess f_loud = (EN − 0.7)⁺/0.3 (sign of +EN);
- glare at the agent f_glare = BL · LT · g_at, with g_at ∈ [0, 1] his gaze at the agent's face (sign of +BL);
- laughter f_laugh = √(BU_L · RHY) (sign of +BU_L);
- Duchenne smile f_duch = √(LP · CR);
- face-read loads b̂_p = Π̃(Rξ₀) = (V̂, Â, T̂): aversive, activation and tiredness (§2.8). Knowing only.

**Innate constants (compiled in, not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| **fast wrap** | | |
| γ_f | 0.45 | sector radius |
| κ_k | FASTFRAC_k · c_k · (1 + γ_f)/(2γ_f) (LP 0.564, BU_L 0.564, RHY 0.483, CR 0.403, BI 0.048) | zero-lag in-phase cap 2γ_fκ_k/(1 + γ_f) = FASTFRAC_k · c_k |
| gate floor g_min,k | min(1, 0.49(1 − γ_f)/(2γ_f κ_k)) (LP 0.53) | away fast gain ≤ 0.49 on every channel |
| θ₀ echo | 0.45 s lag, 0.65 of the fast cap on LP, CR, BU_L, RHY, BI, BO, HP | lip pull and laugh 0.227, cheek 0.162, rhythm 0.195 per unit onset |
| H_i, H_o | first-order high-pass, τ = 4 s | no DC through the fast block (before `sat`) |
| filter bank, lag line, muscle filter M (4 Hz, ζ 0.8), own innovation d (sd 0.04, 2.6–6.5 Hz) | as revision 3 | — |
| **held cone (ungated within a session, centred)** | | |
| traces ξ_m | first-order low-passes of Pu and the derived features, τ_m = 20 s, 2 min, 20 min, 3 h; reset at session start to b_id | completely monotone |
| trace shares F_m | default (0, 0.70, 0.20, 0.10); inner brow (0.5, 0.5, 0, 0) | the sympathy brow fills within about a minute |
| partner baseline b_id,k | b ← b + (his session mean − b)/τ_b, τ_b = 6 sessions; population prior for a new person | his own usual level, per channel (F, slow) |
| ω-scaled diagonal | ω_g · F_m · s_C c_k · (ξ_m,k − b_id,k), ω_g ∈ [−1, 1] | symmetric: the relationship flips its sign |
| innate away diagonals (G₀) | ≥ −N_m, N_m = 0.25, 0.18, 0.12, 0.05 (sum 0.60) | no frown back; quieter to loudness |
| away-orthant cross caps | entry ≤ 0.25, 0.12, 0.08, 0.04; row ≤ 0.30, 0.15, 0.10, 0.05 | free cross-responses |
| charged cross budget | Σ_j λ_kj \|G_m,kj\| ≤ F_m · s_X c_k; λ = 1 on signed pairs, 0.3 on unmasked pairs | toward-orthant cross entries |
| rule J | no positive entry from his sadness synergy (BI, BL, LD, CHR, BU_S) onto the agent's joy synergy (LP, CR, LT, JO, BU_L, RHY, BRE, FR, EN) | no smile or laugh at a sad face |
| zero-ceiling rows | no toward entries, diagonal ≤ 0 | anger, disgust, contempt, sobs |
| **appraisal display** | | |
| band-pass | ξ_A = h_{20 s} ∗ x − h_{90 s} ∗ x | sup\|H\| 0.636; peak step response 0.505 |
| \|Γ_kk\| | ≤ s_A c_k | per channel |
| cross | away orthant only (and rule J); entry ≤ 0.15, row ≤ 0.25 | non-copy reactions |
| bases | 5: neutral, glad-with (innate), startle-orient (innate), two learned | §2.6 |
| **relationship (learned, display-blind)** | | |
| groups g | smile (LP, CR, BU_L, RHY, BRE); sympathy (BI, BO, LD); voice (F0, FR, EN, RT, PAU, LAT); head (HP, VG, lateral) | ω_g ∈ [−1, 1] |
| priors (a stranger) | ω = 0.5, 0.3, 0.2, 0.5 | — |
| update | ω_g ← ω_g + (s_g − ω_g)/τ_ω, τ_ω = 60 sessions | s_g from T only (§2.12) |
| **ports** | | |
| P_name (heard own words) | match m ∈ [0, 1]; F loads: extra decay 0.08 m per 30 s, τ 2 min; T loads: attenuation n ≤ 0.17, latch rate 0.4 m per 30 s, τ 5 min | attenuate-only (kept) |
| **body and drives** | | |
| 𝒟(b) = Σ_i w_i ψ(\|b_i − b_i\*\| − δ_i)₊, ψ(x) = x² | E (0.7, 0.2, 1.0); A (0, 0.15, 0.7); V (0, 0.05, 1.0); K_id (0, 0.10, 0.6 f_id); P (0, 0.10, 0.5); I (0, 0.10, 0.4) | (set point, dead-band, weight) |
| E, energy | −0.04 %/min awake; restored in sleep and replay | own clock |
| K_id, contact deficit per known person (f_id ≥ 0.3) | between his sessions rises (1 − K)/τ_K, τ_K = 36 h; frozen within a session; relieved ×0.5 at the greeting, then ×(1 − 0.25 f_id) at each of his first 4 substantive turns; 0 for a stranger | session-level, per person |
| P, play deficit | rises (1 − P)/τ_P, τ_P = 5.05 h; ×0.85 per play-structured turn | initiative and a small relief only |
| I, curiosity deficit | rises (1 − I)/τ_I, τ_I = 1 h awake; I ← max(0, I − 0.5 π_τ) at each partner-initiated utterance on topic τ | satiable |
| A, activation load | A_F (slow loudness and motion, F) + A_L (T: latched lexical surprise, A_L ← max(A_L, 0.5 s_lex²), τ 3 min) | A_L reaches the display (§2.7) |
| V, aversive load | V_F (F: the threat reflex, below) + h (T: hurt latch from the word → V map) | — |
| threat reflex (innate, declared) | V_F = g_at · max(f_glare, f_loud · (1 − 2 f_pos)₊), f_pos = max(f_laugh, f_duch) | an anger-display-at-me reflex; loud laughter and loud praise are not threats |
| hurt latch h | h ← max(h, v_w) at an addressed utterance; τ 10 min; halved at each play-structured turn | — |
| word need N_L = (V, A, T) | from the word-need reader per topic slot; τ 30 min; a non-substantive utterance can only raise it | — |
| **care, valence and display** | | |
| 𝒟_p(N) | 0.8 [ψ(V − 0.05)₊ + 0.7 ψ(A − 0.15)₊ + 0.5 ψ(T − 0.20)₊] | care over his inferred loads |
| C_F (face concern) | 20-s face trace → Π̃ → 𝒟_p; attack 40 s, release 10 min | F, knowing |
| C_L (word concern) | tracks 𝒟_p(N_L), τ 40 s | T |
| θ_C, θ_I | 0.10, 0.45 | bid thresholds |
| appraisal delay δ_app | 0.6 s after his utterance ends | words appraised before display |
| events | R_n = drops of 𝒟_p(N_L), 𝒟_K, 𝒟_P, 𝒟_I; S_n = rises of 𝒟_p(N_L) and of the h part of 𝒟_V | **T parts only** (E1) |
| masking | R′_n = max(0, R_n − 3 S_n) · max(0, 1 − 𝒟_p(N_L)/0.05); contact relief also × (1 − m_s) | no relief over his distress |
| arrival appraisal m_s | clip((V̂(his face over the first 1 s) − d_b,id − 0.10)/0.30, 0, 1), latched once per session; d_b,id his arrival baseline (τ 6 sessions) | the greeting sees |
| play-surprise laugh | a_laugh,n = 0.40 · clip(1 − \|s_lex − 0.55\|/0.25, 0, 1) at a play-structured turn, × the same mask | innate incongruity reflex; habituates with s_lex |
| display amplitude | a_r = R′/(R′ + 0.02), a_d = S/(S + 0.02) | saturating |
| envelope e(t) | linear rise 0.4 s, apex to 1.5 s, decay τ 3 s | smile dynamics |
| **initiative and turn-taking** (kept from revision 4 unless stated) | | |
| turn-end score | p_end = σ(−4 + 3 s_syn + 2.5 s_fall + 2(t_sil − 0.2)/0.5) | innate weights |
| provisional body onset | p_end ≥ 0.7 and silence ≥ 0.25 s, or silence ≥ 0.9 s; inhale (breath 0.15, 0.3 s), gaze, outer brow 0.10 | abortable within 0.40 s |
| words begin | silence ≥ 0.5 s, p_end ≥ 0.9, and the first draft sentence ready | — |
| concern bid | mutual silence ≥ 6 s, no turn owed, C ≥ θ_C; one per lapse | — |
| curiosity bid | mutual silence ≥ 8 s, I ≥ θ_I, C < θ_C; ≤ 1 per 5 min; preceded by a sigh (breath 0.15 for 1 s, gaze drift 0.10 for 2 s) | the sigh is new |
| greeting | face present ≥ 1.0 s (hysteresis 3 s): brow flash 0.35 for 0.5 s for a known person, 0.20 for a stranger; then m_s and the contact relief | recognition at sight; gladness as appraised |
| **Ω (Claude through Claude Code)** | | |
| drafts | 3 forked Agent SDK sessions per turn; effort `low`; tools none; system prompt replaced; length by instruction (one or two sentences); `CLAUDE_CODE_MAX_OUTPUT_TOKENS` 120 as a safety truncation only | §6.5 |
| scoring | first sentence of each streamed draft; 30 s of 𝓜 rollout at 2 Hz | — |
| retrieval | ≤ 3 snippets; ALiBi slope 1/(7 days) | as revision 4 |
| concepts | DP-means λ_DP = 1.5, ≤ 64 categories; PMI over own tokens | as revision 3 |
| replay | gradient clip 1; pull to θ₀ λ = 0.5 (fast), 0.1 (slow); learning rate × exp(−0.5 r̄) | — |

EOF
