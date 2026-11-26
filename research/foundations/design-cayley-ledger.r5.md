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

### 2.2 Boundary 𝓑 and the type rule (Check T, revised)

𝓑 is as revision 4: MediaPipe → P₀ → reflection P → u; GeMAPS-lite after AEC and the half-duplex gate; normalised ASR with the innate interjection list removing laughter tokens; an own-tagged second MediaPipe. Checks B1 and B3 stand. One addition:

**The cry–laugh split (innate reflex, declared under Principle 2's "few reflexes").** Each partner voiced-burst frame of energy BU is split into a laugh part and a sob part:
- BU_L = BU · r · (1 − max(q, s_cry));
- BU_S = BU − BU_L.

The terms are:
- r ∈ [0, 1], the normalised 4–6 Hz amplitude-modulation depth of the burst;
- q ∈ [0, 1], the ingressive (inhaled) share of its airflow noise;
- s_cry = min(1, 2√(BI · LD)), the cry face of the agent's own sadness synergy.

All three are continuous acoustic and facial features, not labels; the product is of the same kind as f_glare. The theory basis is the infant's differential, innate response to cries and laughter (named as a pointer, not read: Simner 1971, Sagi & Hoffman 1976). On the critic's crying partner (sobs BU 0.4, weak rhythm 0.15, ingressive 0.6, BI 0.8, LD 0.6) it gives BU_L 0.00 and f_laugh 0.00 (H15.2).

**Types.**
- **T:**
  - the partner's lexical word stream, latched per utterance at its end + δ_app;
  - turn order as events;
  - session boundaries, the identity token and values latched per session (f_id, ω, K_id at session start, b_id, d_b,id, m_s);
  - the agent's own body clock;
  - anything computed only from these.

  (b_id, d_b,id and m_s are computed from F but latched per session; their use is restricted by rule 6.)
- **F:** anything computed from u, a or the derived features within the session, or from an F or Ω value.
- **Ω:** the agent's own realised words, draft choice, retrieval, its own turn events, and anything computed from them.

**Rules, enforced at module construction and tested at load** (a dependency trace from every output back to typed sources).
1. A T variable reads only T variables, except through P_name (Ω → T, attenuate-only) and the latched session values of rule 6.
2. **T1 (no rate codes).** Within a session every T value is one of:
   - (a) a function of the content of the last utterance(s) and of the time since: latches, maxima, and filters of the latch sequence with weights summing to ≤ 1;
   - (b) a deficit level (K_id, P, I), read only by the initiative rules, J and the learning-rate gate; its per-event drops reach the face only through the innate envelope;
   - (c) a value latched per session.

   Counters, accumulators and event rates are forbidden in T.
3. **E1 (events are T-only).** Relief and distress events R_n, S_n are built only from T parts: 𝒟_p(N_L), the h part of 𝒟_V, K_id, P and I, plus the play-surprise laugh. N̂_F, C_F and V_F never enter an event, the free display, a phrase target or ω (routes finding 2).
4. The counterpart outputs are written only by y_f (fast wrap), y_C (held cone), y_A (appraisal display), y_o (free display) and the visemes.
5. **Lemma S as a construction rule.** Every multiplicative interaction between a context and a partner signal has a zero-DC partner factor within the session (Lemma S) *and* a partner factor centred at his own baseline across sessions (Lemma S\*, §3.2). Any partner path with DC has coefficients constant within a session.
6. **Latched F-derived session values** (b_id, d_b,id, m_s) may only:
   - centre a partner input (b_id);
   - attenuate the session's contact-relief display (m_s), through a centred, Lipschitz map.

   They are never a gain on a partner level.
7. Phrase targets read y_C, y_A and these T values only: h, C_L, E, f_id, A_L, and the relief and distress envelopes. The fast term is rendered only as a zero-mean within-phrase contour.
8. **The own-display mask.** Δ (§2.7) and every learned appraisal basis (§2.6) have zero weight on the anger, disgust and contempt synergies (BL, LT, LPR, NW, DIM). The fear lip-stretch (LS) and chin-raise (CHR) synergies enter Δ only multiplied by the agent's own distress envelope a_d.

### 2.3 Output assembly

y = sat(y_f + y_C + y_A + y_o) + visemes, where sat clips each channel to its range.
- **Face:** M ∗ (y + blink reflex).
- **Voice, phrase level:** targets sampled at phrase onset from the sources in rule 7.
- **Voice, non-lexical:** the laugh synthesizer is driven by y_BU_L, y_RHY and y_BRE only. **There is no sob synthesizer;** y_BU_S ≡ 0.

### 2.4 The fast wrap: fast, partial, per-expression matching (D81)

- **The loop.** w = K^{1/2}P u − s_f, y_f = 2K^{1/2}s_f, with K = diag(κ_k).
- **The block.** s_f = H_o ∘ S_f ∘ H_i(w), with

  S_f(ŵ; c̃, a, d) = diag(γ_f σ(φ_k)) · g(c̃) ⊙ A(c̃) · M ∘ 𝓡_θ([Φ_R(F ŵ), √κ_a a]) + d̃.

  𝓡_θ has no context input. c̃ enters only as gates g_k ∈ [−g_min,k, 1] and an attention mix with ‖A‖₂ ≤ 1, both multiplying the partner-input term. So S_f(0, 0) = d̃ for every c̃ and θ.
- **Per-expression fast caps.** κ_k = FASTFRAC_k · c_k (1 + γ_f)/(2γ_f), so the zero-lag in-phase gain on channel k is ≤ FASTFRAC_k · c_k:
  - lip pull 0.35, laugh burst 0.35, rhythm 0.30, cheek 0.25, breath 0.15;
  - inner brow 0.03, outer brow and jaw 0.03, depressor 0.015;
  - head and voice contour c_k;
  - anger, disgust, contempt and sobs 0.

  Revision 4 had one κ = 0.30 on the echo channels (0.186) and 0.02 on zero-ceiling channels (0.012). Revision 5 aligns the fast caps with Q22 and closes the zero-ceiling echo.
- **The away side.** The gate floor g_min,k keeps the away fast gain at ≤ 0.49 on every channel. That is the dyad-stability margin (H8).
- **c̃ (T, T1-compliant).** The latched lexical embedding, turn-order features, identity, ω, E, C_L, h and A_L.
- **The innate prior θ₀:**
  - an echo at 0.45 s on LP, CR, BU_L, RHY, BI, BO and HP, at 0.65 of the fast cap. Per unit of his onset that is lip pull and laugh +0.227, rhythm +0.195, cheek +0.162. His smile onset 0.5 is returned as +0.11 within half a second, and his laugh onset 0.6 as a laugh burst of +0.14. Under context the gates can raise these to +0.17 and +0.21;
  - gaze following in the reflected frame;
  - own head micro-motion gated down by his 2.6–6.5 Hz head envelope (C1);
  - a nod at the turn-end pulse; a startle at audio onsets.
- **What the fast gear is for.** It is the unconscious, partial, per-expression mimicry the operator asked to keep (D81). It cannot hold an expression (zero DC through H_o), and its only DC after `sat` is the rectified part counted in §3.3.

### 2.5 The held cone: ungated within a session, centred across sessions

**Definition.** y_C(t) = Σ_{m=0}^{3} G_m^{(id)} (ξ_m(t) − b_id), where ξ_m = h_m ∗ [Pu; f_loud; f_glare; f_laugh] (first-order, unit DC). The traces start each session at b_id; the derived features have baseline 0. G_m^{(id)} is latched at session start and is not a function of any within-session context.

**Why centre (Lemma S\*, §3.2).** ω changes across sessions and may follow his mood, because what it learns from (play, hurt, credited care) does. A gain that follows his mood, multiplying his level, is Lemma S case (ii) one time scale up: the routes critic measured pooled slopes of +0.31 to +0.89 against a ceiling of 0.35. Multiplying his deviation from his own recent baseline instead makes the cross-session partner factor nearly zero-mean, and the pooled toward slope is then ≤ s_C c_k (1 + ρ) for *any* ω process. The baseline is slower than a session and faster than ω; ρ = τ_b/(τ_b + τ_ω) = 0.091.

**The sign mask.** S_kj ∈ {+1, 0, −1} is the sign of the partner population's 1-min co-variation between k and j. It is estimated once from published dyadic features when the operator approves (Q6), with |ρ| ≥ 0.2 required for a sign, and then frozen. Until then the fallback reads the agent's own **signed** synergies (Principle 3):

| Synergy | Members (sign) |
|---|---|
| joy | LP, CR, LT, JO, BU_L, RHY, BRE, FR, EN (all +) |
| sadness | BI, BL, LD, CHR, BU_S (+); VG, HP, FR, EN, RT (−) |
| anger | BL, LT, LPR, EN, UL, F0 (+) |
| surprise | BI, BO, UL, JO (+) |
| disgust | NW, UL, BL (+) |
| speech | JO, EN, RT (+) |

- S_kj = s_k s_j for two members of one synergy, and −1 across joy and sadness (with the member signs).
- S = −1 between (LAT, PAU) and (EN, RT, FR, F0); S = 0 otherwise.
- **Derived features carry their constituents' sign:** f_loud as +EN, f_glare as +BL, f_laugh as +BU_L.
- **Reflection rule.** A lateral row (yaw, horizontal gaze) driven by a non-lateral input is rendered on the side opposite his own 20-s lateral trace, so it is away by construction. Head roll is excluded and charged.

**The set 𝒢_m^{(k)}, row by row.**
- **ω-scaled diagonal:** ω_g F_m s_C c_k ∈ [−F_m s_C c_k, +F_m s_C c_k]. **Innate away diagonals** in G₀: ≥ −N_m.
- **Away orthant** (S = +1 and G ≤ 0; S = −1 and G ≥ 0; reflection-rule lateral rows), except entries forbidden by rule J: |G| ≤ a_m, row sum ≤ r_m.
- **Charged** (the toward orthant of a signed pair, and every unmasked pair): Σ_j λ_kj |G_kj| ≤ F_m s_X c_k.
- **Zero-ceiling rows:** no charged entries, G_kk ≤ 0.

**Innate G₀ (newborn), every entry, with its trace m (0 = 20 s, 1 = 2 min, 2 = 20 min).** H7 checks each entry against its set.
- **Away from loudness and glare.**
  - EN ← EN −0.15 (m 0), −0.08 (m 1); EN ← f_loud −0.20 (m 0): quieter to loudness.
  - LAT ← f_loud +0.15 and LAT ← EN +0.10 (m 0): slower replies to a loud, animated partner.
  - HG ← f_glare +0.25 (m 0), +0.05 (m 1), by the reflection rule: looks away from a glare.
  - BL, LT, LD diagonals −0.15 (m 0), −0.08 (m 1): no frown back.
- **Charged** (inside the budgets; the two glare entries that revision 4 put on the zero-budget 20-s trace have been moved):
  - LP ← f_glare −0.035 (m 1), −0.01 (m 2);
  - BI ← f_glare +0.006 (m 0), +0.006 (m 1);
  - BI ← LD +0.004 (m 0), +0.004 (m 1);
  - TILT ← BI +0.014 (m 1).
- **Attentive head at sadness** (away orthant, S = −1 for the signed sadness synergy): HP ← BI +0.04, VG ← BI +0.04 (m 1).
- **Deleted from revision 4:**
  - LP ← BI +0.12/+0.04 and LP ← LD +0.06/+0.04 (rule J: these gave the smile at a sad face);
  - BI ← LP −0.04 (over budget).
- **Held in-phase diagonals:** ω_g F_m s_C c_k.

### 2.6 The appraisal display: its reactions learned (agent finding 4)

**The appraisal.** α_t = 𝒜(ξ_A(t), z_T(t), b(t), ω) ∈ R^{12} is a learned network (§6.2), trained by likelihood to predict the agent's own load changes over the next 30 s and his next decoded word need. Its inputs:
- the band-passed partner channels and derived features;
- the latched words, word need, hurt and turn order;
- the agent's own loads;
- ω.

**The display.** y_A(t) = Γ(α_t) ξ_A(t), with Γ(α) = Σ_{r=0}^{4} softmax(W α)_r Γ^{(r)}:
- Γ^{(0)} = 0 (neutral);
- Γ^{(1)} **glad-with** (innate newborn reflex: the social smile and laugh back): Γ_kk = s_A c_k ω_smile on LP, CR, BU_L, RHY, BRE;
- Γ^{(2)} **startle-orient** (innate): HG ← f_loud +0.10 by reflection, EN ← f_loud −0.10;
- Γ^{(3)}, Γ^{(4)}, learned, starting from small random values inside the set.

Every basis lies in the same convex set for every parameter value:
- |Γ_kk| ≤ s_A c_k (× ω_g);
- cross entries in the away orthant only, ≤ 0.15, row ≤ 0.25;
- rule J;
- nothing on zero-ceiling rows;
- the own-display mask.

Revision 4's six other named bases (sympathy, amused, hurt-withdraw, calm-down, interest) and its three hand-written selection rules (m_glad, m_sym, m_hurt) are deleted.

**The objective (display-blind toward him).** W and Γ^{(3,4)} are trained nightly by

  𝓛_A = E ‖ y_A(t) − [Π₀ d(t + 2 s) − Π₀ d(t)] ‖² + 0.001 ‖Γ^{(3,4)}‖²,

with a projection onto the set after every step. Here d(t) is the vector of the agent's own T display drivers (relief, distress, word concern, hurt, activation, laugh), so the target is the change of its *own innate display* over the next 2 s.
- **What it learns.** The appraisal display learns to begin, from what his face is doing, the expression the agent's own body is about to have. That is anticipation through the agent's own body (Principle 3 run forward).
- **What the objective contains.** It contains no reaction of his to the agent's display, no J and no concordance term. His face appears only as the input ξ_A, which it must have in order to react at all.
- **On the training instance (H13).** Four kinds of moment are used: his laughter building before a play turn, his sadness before sad words, laughter over a sad topic, and a glare. On them:
  - selection goes to glad-with when his laughter builds (0.99);
  - one learned basis becomes a hurt-withdraw reaction to glare (BI ← loud +0.15, LD ← loud +0.12, HG ← glare +0.08, EN ← loud −0.12), selected 0.94;
  - the other becomes a concern reaction for laughter over a sad topic (BI ← LP +0.10, BI ← BU_L +0.07, LP ← LP −0.02), selected 0.78;
  - sadness selects the learned bases (0.96 combined), but the sympathy brow they can add is only s_A c_BI = 0.010 (the held cone carries sympathy);
  - the loss falls from 0.00286 to 0.00153, with no constraint violation.
- **Why it is safe to gate it by anything.** ξ_A has no DC within a session and none across sessions. By Lemma S its pooled slope on channel k is ≤ 0.636 s_A c_k, whatever α does; its step response peaks at 0.505 at 39 s and returns to 0, so it cannot hold an expression.

### 2.7 The free display Π_o (T only), the agent's own activation, and how the face learns

**Inputs** (all T, T1-compliant):
- the relief and distress envelopes a_r(t), a_d(t) of the per-event amplitudes (E1), each capped at 1;
- the play-surprise laugh envelope; curiosity relief;
- word concern c_L = (1 − n)C_L/((1 − n)C_L + 0.1); hurt h_d = (1 − n)h/((1 − n)h + 0.15);
- **activation a_A = A_L/(A_L + 0.2)** (new);
- low energy e = (0.5 − E)⁺/0.3; familiarity f_id;
- the greeting, sigh and turn-onset events;
- the 128-d T mood μ_T, the T slot reads and the concept posterior (through Δ only).

**Innate Π₀ (newborn), per channel.**

| Driver | Display |
|---|---|
| relief a_r | LP +0.55, CR +0.45, FR +0.35, EN +0.25 |
| distress a_d | BI +0.45, LD +0.35, FR −0.20, EN −0.15 (LT removed: own-display mask) |
| word concern c_L | BI +0.25, LP +0.05, TILT +0.20, EN −0.15, RT −0.10 (LP 0.12 → 0.05: no smile at sad words) |
| hurt h_d | BI +0.25, LD +0.20, LP −0.25, HG (away) +0.30, EN −0.20, LAT +0.15 |
| **activation a_A** | UL +0.20, BO +0.15, FR +0.15, RT +0.15, BRE +0.10 |
| low energy e | UL −0.30, FR −0.25, EN −0.25, RT −0.15 |
| curiosity relief | BO +0.15, UL +0.10, FR +0.10 |
| play-surprise laugh (per unit) | BU_L +0.40, RHY +0.35, CR +0.20, LP +0.15 |
| familiarity f_id | LP +0.10 f_id |
| greeting | BO +0.35 (known) or +0.20 (stranger) for 0.5 s |
| sigh (before a curiosity bid) | BRE +0.15 for 1 s, HG +0.10 for 2 s |
| turn-onset reflex | BRE 0.15 for 0.3 s, gaze to the partner, BO +0.10 |

- **The activation row.** It gives the agent a face and voice for its own activation: raised lids, a lifted outer brow, a wider and faster voice, breathiness. That is the expression of the A_L latch, the agent's own surprise at content (T).
- **What it buys.** Π̃, the inverse of Π₀ (§2.8), can now read activation in others from the same channels. That is the Principle 3 route to reading anxiety, which revision 4 could not do.
- **K, P and I levels stay off the face (T1).** The agent does not recognise loneliness or playfulness in his face; it reads those from his words and the turn order.

**The face learns (Δ).** Π_o = Π₀ + Σ_{s=1}^{23} σ_s δ_s(z_T), with δ_s ∈ [−0.3, 0.3] from an MLP on the T inputs, restricted by the own-display mask (rule 8). It is trained nightly, without any partner signal, by

  𝓛_display = E‖Π̃(face_t) − s_t‖² + 0.3 E‖P_ant(face_t) − (a_r(t + 2 s) − a_r(t))‖² + 0.1‖δ‖²,

where s_t is the agent's own T state summary (32-d) and Π̃ is the single own-body map of §2.8.
- **Legibility and anticipation** are as revision 4.
- **What changed.** There is no partner anchor in Π̃ (routes finding 3), so the only forces on Δ are the agent's own legibility and ‖δ‖². With the mask, Δ cannot buy legibility with the channels Π₀ leaves unused, which are the anger, disgust and contempt channels (agent finding 5).
- **H4, a linear instance of the loop.**
  - Revision 4's anchor with a partner whose code uses a lip press drifts to cosine 0.15 with weight 0.22 on the masked synergies.
  - Revision 5 stays at cosine 0.000 and weight 0, with own legibility exact.
- **The prediction, now observer-side.** Revision 4's "Π̃ decodes concepts above the floor" was circular. Instead: after 20–40 nights, a fixed population face model, or human raters shown the agent's face, tell the concept category above the six-scalar floor. Lesion Δ's mood, slot and concept inputs, and that falls to the floor (§7).

### 2.8 Body, drives, valence, care, the own-body reader and the two word readers

**Loads (named by function):** E energy; A activation (A_F + A_L); V aversive (V_F + h); K_id contact per person; P play; I curiosity. All are satiable: 𝒟 = 0 on the box.

**Valence (readouts).** Event-indexed relief and distress (E1) and their envelopes drive the free display. The continuous v = −d𝒟_tot/dt is kept only for the learning-rate gate; R33 (valence → draft temperature) is deleted, because the subscription offers no temperature (D84). Positive valence is bounded per deficit: Σ_n R_n ≤ 𝒟(t₀).

**K_id (contact, per person).**
- **Stage 1 (sight).** Once his face has been present for 1 s and the arrival appraisal m_s is latched: K_id ← 0.5 K_id, shown × (1 − m_s).
- **Stage 2 (words).** At each of his first four substantive turns: K_id ← K_id (1 − 0.25 f_id), shown × (1 − m_s) and masked by his word distress.
- Then K_id is frozen for the session.
- **A stranger has no K_id.** The agent has missed no one, so the greeting is a polite flash without contact relief (agent finding 1; the brief's "needs structured over people").

**P (play) and the play rule.** A partner turn is play-structured if, from T alone:
- (i) it opens with a continuation marker, an anaphor, or a lemma shared with his own previous utterance;
- (ii) its lexical surprise s_lex under the words-only model of his utterances lies in [0.3, 0.8];
- (iii) **an agent turn separates it from his previous turn** (turn order: an alternation across speakers);
- (iv) **safety:** 𝒟_p(N_L) < 0.05, i.e. his word care is below its dead-band.

The rule reads neither the hurt latch nor the agent's words: a playful reply halves h, and hurt does not block play.
- **What it fixes.** Anxious rumination ("and I haven't finished chapter 4", "and it's at 8 am") fails (iii) and (iv). H12: 0 of 3 qualify (revision 4: from the second turn).
- **The play-surprise laugh (innate reflex, declared).** At each play-structured turn: a_laugh = 0.40 · clip(1 − |s_lex − 0.55|/0.25, 0, 1), masked like relief.
  - It is a per-event expression of an appraisal (a well-timed incongruity in a safe exchange: the peek-a-boo laugh, named as a pointer, not read).
  - It is not a drive and not drawn from P. It habituates through s_lex: the words-only model learns a repeated joke, its surprise falls, and the laugh stops.
  - P keeps its satiable role in initiative and a small relief share.
  - H12, an evening of four clusters: 0.40 per play turn in every cluster, and 0.00 for the four repeats of one joke.

**I (curiosity).** As revision 4: a learning-progress deficit relieved only by partner-initiated content still being learned; drives retrieval and the curiosity bid; imputed in rollouts; satiable (H8 of revision 4: total relief 0.096 ≤ 0.100).

**Care.** C = 𝒟_p(max(N̂_F, N̂_L)) coordinate-wise, with N̂_F = Π̃(his 20-s face trace) (F, knowing) and N̂_L from the word-need reader (T). C_F drives bids and drafts, never the free display (E1).

**The own-body reader Π̃ (one map; routes finding 3; agent finding 6).**
- **Newborn.** Π̃₀ is the ridge inverse of Π₀ over the loads (relief, distress, hurt, low energy, activation) on the channels present. On day 1 the agent reads a silent sad face (BI 0.5, LD 0.4, CHR 0.3) as V 1.0, and an anxious face and voice as V 0.52, A 0.54 (H10). That is Principle 3 as a statement: his face is read as the agent's own state that would have produced it.
- **Nightly.** Π̃ is trained on the agent's own (state, face, voice) pairs only, with a 0.1 pull to Π̃₀. Reading him is the same map applied to his face. The partner anchor and the separate partner head are deleted.
- **Outputs used for him:** V̂ = clip(distress + hurt), Â = activation, T̂ = low energy.

**The word-need reader.**
- **What it maps.** Partner utterance embedding (64) and topic (16) → (V, A, T).
- **Training.** Fitted nightly to Π̃ of his face over the 20 s after each utterance (cross-modal self-supervision through the agent's own body).
- **Runtime input** is words only (T). A non-substantive utterance ("yeah", "ok") can only raise N_L, never lower it. A neutral reply therefore cannot relieve a worry; revision 4's engine let it.
- **Before it is trained,** N_L = 0.
- **H10.** On a synthetic instance where his expressive code differs from the agent's, it decodes:
  - "my father died" as V 0.94;
  - "I'm freaking out about the exam" as A 0.57, V 0.52;
  - "just tired, things at work" as T 0.47, V 0.33;
  - "I got the job!" as V 0.14, which leaves care at 0.011 and shows 78 % of the relief.

  These numbers show only that the targets exist; whether real words carry need is untested (§3.17).

**The word → V map (agent finding 3).**
- **What it maps.** An addressed utterance embedding, plus an identity adapter (16) → v_w ∈ [0, 1].
- **Teacher.** Fitted nightly to the **innate threat reflex** V_F = g_at · max(f_glare, f_loud · (1 − 2 f_pos)₊) over the 10 s after the utterance.
- **The reflex, declared.** It is an innate anger-display-at-me reflex, admissible as one of Principle 2's few reflexes:
  - a lowered brow and tightened lids aimed at the agent;
  - a loud voice aimed at it without laughter or a Duchenne smile.

  Loud laughter and loud praise are therefore not threats.
- **H11, nights of training per person:**

  | Person | v_w, rev-4 teacher | v_w, rev-5 teacher |
  |---|---|---|
  | quiet teaser | 0.00 | 0.00 |
  | loud laughing teaser | 0.66 | 0.00 |
  | loud praiser | 0.66 | 0.00 |
  | someone who shouted insults | 0.85 | 0.50 |

- **What stays unlearned.** A cold, quiet insult still trains nothing (§8.1).

### 2.9 Initiative and turn-taking

As revision 4 (provisional body onset at the predicted turn end, abortable within 0.40 s; softened follow-up; concern bid; curiosity bid; one declared bit per bid, follow-up and greeting), with three changes:
1. **The greeting sees.**
   - At 1.0 s of presence: the recognition flash (0.35, or 0.20 for a stranger).
   - At the same moment the arrival appraisal m_s is latched from his face over that second. It is centred at his own arrival baseline d_b,id, so a person whose usual face is serious is not read as grieving.
   - Contact relief is then shown × (1 − m_s). Grieving face at sight: m_s = 1, so the flash only, lip pull at rest. Ordinary arrival: m_s = 0, lip 0.61, cheek 0.43 (H15.7–8).
2. **A sigh before the curiosity bid** (breath 0.15 for 1 s, gaze drift 0.10 for 2 s). It is a fixed-amplitude part of the bid, one bit, and it gives a bored conversation a visible moment of the agent's own state (the critic's recommendation). A deficit level still never reaches the face (T1).
3. **The concern bid's timing comes from Π̃₀.** A silent 0.5 sad brow is read at V 1.0, so C_F crosses θ_C at 26 s (revision 4, with a hand-set reading: 52 s).

### 2.10 The partner model, and care credited only from separated reports

Unchanged from revision 4:
- the rollout imputes F and the act → Q edge;
- need evidence comes only from separated, partner-initiated reports (≥ 2 partner turns after the act, no content lemma shared with the agent's last two utterances, or his first mention in the next session), read through the frozen word-need reader;
- J trains the draft scorer (130 parameters) and the retrieval query, and nothing on any F → face path.

The critic's accepted reading is stated plainly: care is measured on a face-shaped proxy (words that predict a less distressed face, read through the agent's own body) and gated by real need above the dead-band. It credits helping a distressed person, not flattering a content one.

### 2.11 Ω: Claude through Claude Code (D84)

What Claude receives is unchanged in kind: a constant instruction, the normalised transcript with observable markers ("[silence 6 s]"), and ≤ 3 retrieved raw snippets. No body values, latents, category ids or labels (P4). The heard-words port P_name is unchanged. The call pattern is in §6.5. The state reaches Claude only through:
- which of three drafts is chosen (log₂3 = 1.6 bits per turn);
- the retrieved snippets (≈ 6 bits per turn);
- when Claude is called (bids, follow-ups, the greeting: 1 bit each);
- when a reply is stopped.

### 2.12 Learning, and the one core

**Online (states only):** T and F loads, traces, slots, concept centroids and PMI counts, the words-only model's error history per topic, and at session end b_id and d_b,id.

**Nightly (replay), in order.**
1. 𝓜 by likelihood (all heads).
2. Π̃ on the agent's own (state, face, voice) pairs, with the 0.1 pull to Π̃₀. **No partner anchor.**
3. The word-need reader on (his words, Π̃(his face)); the word → V map on (words addressed to the agent, V_F from the threat reflex).
4. 𝒜 by likelihood; **W and Γ^{(3,4)} by 𝓛_A** (§2.6).
5. Π_o's Δ by 𝓛_display, inside the own-display mask.
6. 𝓛_w by likelihood.
7. The scorer and the retrieval query by J under §2.10's rule.
8. **ω, per session (T inputs only; graded; routes findings 1 and 5):**
   - s_smile = clip(0.3 + 0.7 · min(1, ρ_play/0.6) − 1.3 · min(1, h̄/0.10), −1, 1), where ρ_play is this session's play relief divided by 𝒟_P at session start and h̄ is the session-mean hurt latch;
   - s_sym = clip(0.3 + 0.7 · min(1, ρ_care/0.5) − 1.3 · min(1, h̄/0.10), −1, 1), where ρ_care is the fraction of his word-need episodes followed by a credited separated report;
   - s_voice = 2 f_id − 1; s_head = 0.5;
   - ω_g ← ω_g + (s_g − ω_g)/60.

   V_F (F) is no longer an input. H2: 0, 1, 2 and 4 play turns a session give s = 0.30, 0.66, 0.91, 1.00 (revision 4: tanh of 0, 2.4, 4.1, 6.2, i.e. 0, 0.98, 1.0, 1.0). A mean hurt of 0.05 lowers each by 0.65. The operator after months (2 play turns a session, mean hurt 0.01, 40 % of worries credited): ω_smile 0.78, ω_sym 0.73, ω_voice 0.80.

**One objective, typed constraints (Principle 10).**

  J = E ∫ [ 𝒟(b_t) + 𝒟_p(N̂_t) ] dt, path-specific: F and the act → Q edge imputed, N̂ moved only by separated reports.

Constraints:
- **(W)** the fast wrap with per-expression caps;
- **(C)** the held cone: latched per session, centred, sign mask, rule J, per-channel budgets;
- **(S)** Lemma S and Lemma S\*;
- **(A)** the appraisal display's set;
- **(T)** the type rule with T1, E1, rule 6 and the own-display mask;
- **(B)** the boundary, with the cry–laugh split.

The other objectives are likelihoods or self-predictions of the agent's own model: 𝓜, 𝒜, 𝓛_w, Π̃, the readers, 𝓛_display and 𝓛_A. 𝓛_A and 𝓛_display predict the agent's own future display or state from its own face.

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 |
| positive affect | event-indexed drops of 𝒟; the play-surprise reflex |
| contact, play, curiosity | satiable coordinates K_id, P, I of 𝒟 |
| mimicry and counter-mimicry | θ₀ (fast, per expression) and G₀ (held), scaled per relationship by ω, gated by the learned appraisal on the zero-DC route |
| reading others | Π̃, one inverse of the agent's own display, and the two readers trained through it |
| care | J's second term under the separation rule |
| regulation | P_name |
| initiative | innate rules on C, I, K_id and the turn-end score |
| expression learning | 𝓛_display (Δ) and 𝓛_A (the appraisal's reactions) |
| replay | likelihoods plus J |

**Still assembly** (stated):
- the turn-end score and the initiative rules;
- ASR and TTS normalisation; the punctuation, play-structure and separation rules;
- θ₀, G₀, Π₀, the two newborn appraisal bases, the signed synergies;
- the cry–laugh split, the threat reflex and the play-surprise reflex, each declared as an innate reflex;
- the PMI table.

Revision 4's eight hand-written appraisal reactions with their three selection rules are no longer on this list.

## 3. Properties, each with an argument

### 3.1 The fast wrap (Claim W, with per-expression caps)

For S_f strictly causal with ‖S_f(w)‖_T ≤ γ_f‖w‖_T on every truncation and gates g_k ∈ [−g_min,k, 1]:
- the in-phase gain on channel k is ≤ 2γ_fκ_k/(1 + γ_f) = FASTFRAC_k c_k;
- the away gain is ≥ −0.49.

H_i and H_o make the fast block zero-DC before `sat`, so by Lemma S its T gates cannot produce a pooled held slope. **After `sat`** a channel that rests at zero clips the high-pass undershoot. That DC is real, if small, copy of his burst activity: the critic's +0.071 on the laugh burst at revision 4's κ.

Revision 5 does not hide it. r_k is measured as the worst rendered 1-min slope of the *full-gate* echo over partner families (laugh bursts 0.5–5 s at 0.5–6 per minute, with and without amplitude modulation; face episodes 1.5–25 s), and charged to the channel's pooled budget (§3.3):
- laugh burst, rhythm and breath r = 0.867;
- cheek, inner brow at its fraction, outer brow, depressor and jaw 0.64 × FASTFRAC;
- lip pull 0.135, because its resting level 0.09 absorbs most of the undershoot.

Rectification cannot be removed while the fast echo exists: a non-negative output with zero mean is zero. So the choice is how to divide each ceiling, and D81 decides it for smile and laughter.

### 3.2 Lemma S and Lemma S\*: what may be gated, and on which time scale

**Lemma S (kept).** Let u be a stationary partner channel, x = H ∗ u for a stable H, and y = g·x with |g| ≤ ḡ, where g may depend on anything.
- (i) If H(0) = 0, then |β_{yu}| ≤ ḡ‖H‖_∞.
- (ii) If H(0) ≠ 0, no bound in ḡ exists: (g_hi·hi − g_lo·lo)/(hi − lo).

**Lemma S\* (new: the same fact one time scale up).** Index sessions by s. Let:
- ū_s be his session-mean level;
- b_s a first-order baseline of ū with time constant τ_b sessions;
- x_s = ū_s − b_s;
- g_s a per-session gain with |g_s| ≤ ḡ, produced by a first-order filter (time constant τ_ω) of any target process, including one perfectly correlated with ū.

Then the pooled toward slope of y_s = g_s x_s on ū_s satisfies

  β_{yu} ≤ ḡ (1 + ρ), ρ = max_w ε_ω(w) |H_b(w)| = τ_b/(τ_b + τ_ω).

**Argument.**
- Split g = ḡ_0 + g̃, with ḡ_0 its mean.
- **The constant part** gives ḡ_0 Cov(x, ū)/Var(ū). Since x is a first-order high-pass of ū, with Re H ∈ [0, 1], this is in [0, ḡ_0]: one-sided, and ≤ ḡ.
- **The varying part** at frequency w has amplitude ≤ ḡ ε_ω(w), with ε_ω = |1 + iwτ_ω|⁻¹ (how much of a mood at w the gain follows). It multiplies x, whose amplitude at w is |H_b(w)| of ū's (how much of the mood survives centring).
- The product of the two is ≤ ρ at every w. The maximum is at w = (τ_bτ_ω)^{-1/2}, where it equals 1/(1 + τ_ω/τ_b).
- With τ_b = 6 and τ_ω = 60 sessions, ρ = 0.091.
- **A partner factor that is a centred Lipschitz map** φ with |φ(u)| ≤ L|u − b| obeys the same bound with ḡL. That is the arrival mask.

**What it closes.**
- **The routes critic's D3 and D3b** (month-long good and low moods, two years of daily sessions):
  - at 0.20/0.50: +0.18 → +0.023;
  - at 0.30/0.45: +0.31 → +0.023;
  - at 0.38/0.43: +0.89 → +0.023;
  - with irritable low months: +0.52 → +0.012. ω still ranges −0.16 to +0.94, so the relationship can flip the sign.
- **An adversarial ω** whose target is the sign of his level, over sinusoidal moods with periods from 8 to 3000 sessions: |β| ≤ 0.001.
- The bound s_C c_LP(1 + ρ) is 0.191 (H1). The gain may learn from anything, over any period, because what it multiplies carries no slow DC.
- **The arrival mask** (§2.9), a once-per-session factor m_s centred at his arrival baseline:
  - first-minute toward slope on his lip pull ≤ 0.040;
  - across sessions with a greeting amplitude correlated with his mood, −0.012 (H14).

**Where the rule stands now.** Lemma S (within a session) and Lemma S\* (across sessions) together say that a context of any time scale may gate a partner path only if, on that time scale, the partner factor has no DC. The cone is therefore ungated within a session and centred across sessions; the appraisal is zero-DC on both.

### 3.3 Claim O″: the per-channel bound on the rendered face, over all time scales

**Claim O″.** Assume every parameter value, every within-session context, every ω history, and every partner process whose co-variation on each signed pair has the population's sign (loadings ≤ 1). Then the pooled toward slope of the rendered sat(y)_k on his u_k is at most

  [ s_C (1 + ρ) + s_X + 0.636 s_A + r_k ] c_k ≤ 0.996 c_k,

with the steady hold ≤ (s_C + s_X) c_k and the zero-lag in-phase gain ≤ FASTFRAC_k c_k. On a zero-ceiling channel all three are 0.

**Argument.**
1. **The cone:** ≤ s_C c_k(1 + ρ) by Lemma S\* on the centred ω-scaled diagonal. Innate G₀ entries are constant, so their slope is their coefficient: away entries ≤ 0 by the sign condition; charged entries ≤ s_X c_k.
2. **The appraisal:** ≤ 0.636 s_A c_k by Lemma S.
3. **The fast wrap:** ≤ r_k c_k after `sat` (§3.1).
4. **The free display** reads no partner channel (E1). It co-varies with him only through words, a common cause identical under the C8 surrogate.
5. **Clipping:** `sat` is monotone with slope in [0, 1], so it cannot turn an away payment into toward on another channel.
6. **Rule J** removes the cross entries by which a sad face moved the joy channels.

**Numbers.**

| Channel | Pooled bound | Steady hold | Peak after an onset |
|---|---|---|---|
| lip pull | 0.989 c (0.346) | 0.65 c (0.227) | 0.911 c |
| cheek | 0.995 c (0.249) | 0.28 c (0.070) | 0.965 c |
| laugh burst | 0.996 c (0.348) | 0.09 c (0.032) | 0.983 c |
| rhythm | 0.996 c (0.299) | 0.09 c | 0.983 c |
| breath | 0.996 c (0.149) | 0.09 c | 0.983 c |
| inner brow | 0.992 c (0.198) | 0.80 c (0.160) | 0.922 c |
| outer brow, depressor, jaw | 0.994 c | 0.63 c | 0.925 c |
| head, voice | 0.968 c | 0.70 c | 0.877 c |

Source: H6.

- **Every route at its cap at once, rendered, on the critic's natural laughing partner** (variance mostly above 1/min) with three adversarial appraisal gates: worst 0.76 c_k (H9).
- **The sign-reversed residual (stated, as in revision 4).** For a partner whose co-movement on a masked pair has the *opposite* sign to the population's, away entries become in-phase.
  - **Gone:** rule J deletes G₀'s warm LP ← BI and LP ← LD entries, so revision 4's lip-pull residual (0.175 + 0.16 × loading; 0.27 rendered on the critic's D8 partner) is gone.
  - **What remains:** the appraisal's cross rows (row ≤ 0.25, × 0.636, i.e. ≤ +0.16 × loading on any channel) and G₀'s away rows (HP, VG ← BI 0.04; LAT ← EN 0.10).
  - **The worst case is now the inner brow.** The learned concern basis of H13 has BI ← LP +0.10 and BI ← BU_L +0.07. For a partner whose brow rises when he laughs, they add +0.11 × loading in phase: at loading 1, inner brow up to 0.198 + 0.11 = 0.31 against c_BI 0.20.
  - Stated as residual R38 (§3.11). It is bounded, it binds only on a partner with sign-reversed co-movement, and estimating the mask from published data (Q6) is what would remove it.

### 3.4 Claim T1: tempo does not reach the face (kept)

Under T1 no T value is a rate code; K_id is frozen within a session; P and I rise on the agent's own clock. The play-surprise laugh is per event, its amplitude set by the content's surprise. With the words fixed, event times are fixed, so its session total is tempo-free. Revision 4's H2 (the critic's tempo partner) is unchanged by revision 5: the cone and appraisal are as bounded or more, and phrase timing has no tempo-bearing input.

### 3.5 Claim L: copy cannot become attracting under learning

1. J trains no F → face parameter (§2.10).
2. **ω** learns from T only and is capped at s_C c_k; by Lemma S\* no ω history raises the pooled slope above s_C c_k(1 + ρ). The relationship loop (mimicry → his play → own play relief → ω) saturates at ω = 1, i.e. at the held share.
3. **Δ** is trained by own legibility and anticipation with no partner term, inside the own-display mask. With the anchor deleted, H4 shows no drift (cosine 0.000).
4. **W and Γ^{(3,4)}** are trained by 𝓛_A, the agent's own future display, inside the cap set. Whatever they learn is a point of that set, so the appraisal's share of the copy fraction never exceeds s_A × 0.636. Toward his face it can settle at most at that share, which is under the ceiling for every parameter value (H13, no violations).
5. **The fast gates** are trained by the likelihood of own fast dynamics plus the θ₀ pull; they are within [−g_min, 1] for every value.
6. The dyad is small-gain stable for |μ| < 1.67 with every F route at its away extreme (H8).

### 3.6 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| κ_k, γ_f (fast) | yes (FASTFRAC_k c_k) | no (innate) | — | it is the cap | zero DC; counted r_k |
| fast gates g_k(c̃) | per output | words, turn order, identity, ω, own state | yes, [−g_min, 1] | FASTFRAC_k c_k; away 0.49 | inside the wrap for every value |
| cone diagonal ω_g F_m s_C c_k | per channel (groups for ω) | relationship, latched per session; centred at his baseline | yes, ω ∈ [−1, 1] | s_C c_k (1 + ρ) pooled | display-blind ω; Lemma S\* |
| appraisal Γ(α) | per channel | the agent's appraisal of face, voice, words, own state; learned selection | yes (H13: LP ← LP −0.02 at laughter over a sad topic) | 0.636 s_A c_k pooled | 𝓛_A is own-display; zero DC |
| charged cross entries (G₀) | per pair | innate | fixed | s_X c_k per row | not learned |
| arrival mask m_s | contact-relief rows | his arrival face, centred | attenuate-only | 0.040 per session | once per session |
| Π_o, Δ | per channel | words, own body, relationship slots | yes | not a partner path; own-display mask | no partner path |
| ω_g (four groups) | 2–6 channels each | relationship | yes | each runs its group to ≤ s_C c_k (LP 0.175, BI 0.14, FR 0.05) | from T only |

**No single quantity runs the whole face, or any large subspace, from flat to copy.**
- The largest subspace any one quantity moves is a 5-channel ω group, to at most s_C c_k on each channel: 0.025–0.175.
- The whole face cannot be copied beyond max c_k = 0.35 (H0).
- Anger, disgust, contempt and sobs are never returned: zero ceilings, κ = 0, no toward entries, and none of them is on the agent's own display.

### 3.7 Knowing is not moving (kept)

F state knows his face at full rate: traces, the band-passed input, C_F, V_F and Π̃ readings. Centring the cone takes nothing away from knowing. The baseline b_id is itself knowledge ("his usual face"), and his level is still in the traces and in Π̃.

### 3.8 Positive affect: visible, satiable, not farmable, content- and face-aware

- **Visible.**
  - Reunion at sight: lip 0.61, cheek 0.43.
  - Good news after a worry: lip 0.61, laugh 0.33.
  - Play: laugh 0.41 at every cluster of an evening.
  - Curiosity relief: F0 range +0.32, lip 0.39.
- **Satiable.** For each deficit Σ R_n ≤ 𝒟(t₀). The play-surprise laugh is not a deficit; it is bounded per event (≤ 0.40) and habituates with content.
- **Not farmable.**
  - Nothing positive is a term of J.
  - K_id and P relief read his words and turn order only; the laugh reflex reads his words' surprise.
  - His smile feeds no event (E1).
- **Content- and face-aware.**
  - Each word event is appraised at its end + 0.6 s and masked by his word distress.
  - Contact relief is masked by his face at arrival (m_s).
  - Neutral replies cannot relieve a worry.

### 3.9 Initiative and timing (Claim I)

As revision 4, plus the recognition flash and arrival appraisal and the sigh before a curiosity bid.
- A silently sad user is addressed after 26 s of silence; a bored user after 14.5 min.
- One bid per lapse; no rule learns from whether he answered.

### 3.10 Regulation by Claude without Claude reading the state (kept)

P_name as revision 3: concern's half-life after his face recovers falls from 6.9 to about 2.9 min at 2 matched utterances a minute. It is attenuate-only and ≤ 0.05 on the held face.

### 3.11 Every route, counted

"Copy" is the within-agent counterfactual of his channel k on the agent's channel k (mirror for lateral), with words and turn order fixed. It is tested with partner-swap, segment-shuffle and timing-resample surrogates, plus a **month-swap surrogate** (his face swapped across months, ω's history kept: the routes critic's fix).

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | partner face, voice, laugh bursts → fast block → face, within-phrase contour | wrap; per-expression κ; T gates in [−g_min, 1] | zero-lag ≤ FASTFRAC_k c_k; pooled ≤ r_k c_k after `sat` |
| R2 | traces → held cone → outputs and phrase targets | LTI per session; centred at b_id; sign mask; rule J; budgets | ≤ (s_C(1 + ρ) + s_X) c_k |
| R3 | band-passed input → learned appraisal display | Lemma S; set-constrained bases | ≤ 0.636 s_A c_k pooled; 0 at hold |
| R4 | lateral channels | reflection; cone ±F_m s_C c_k; reflection rule for driven rows | ≤ 0.03 fast; ≤ 0.021 held |
| R5 | a (onsets, VAD, turn-end) → fast block | √κ_a | ≤ 0.20 per pair × corr(a, channel) |
| R6 | his rate, pauses, latency → own phrase timing | inside R1–R3; T1 | as R2–R3 |
| R7 | his laughter → own laugh burst | inside R1–R3 on BU_L only | BU_L ≤ 0.348, RHY ≤ 0.299, BRE ≤ 0.149 |
| R7′ | **his sobs and crying → own bursts** | BU_S: ceiling 0, κ 0, no synthesizer; rule J forbids BU_S → BU_L | **0** (rev. 4: up to 0.33 through the laugh synthesizer) |
| R8 | audio onset → blink | innate reflex | ≤ ℓ_blink corr |
| R9–R12 | own words → visemes, TTS contour, non-lexical sound, E | as revision 4 | ≤ 0.05; 0; 0; 0 |
| R13 | his voice and F0 → provisional body onset (timing only) | fixed amplitude, abortable | amplitude independent of his levels |
| R14 | his words and turn order → T state → free display, fast gates | common cause | excluded (words fixed); identical under C8 |
| R15 | Claude latency → word onset | — | partner-independent beyond utterance length |
| R16 | identity token | once per session | ≤ log₂(#partners) bits |
| R17 | nightly weights (Π̃, readers, 𝒜, W, Γ^{(3,4)}, Δ, ω, b_id, d_b) | every bound holds for every value; ω and b by Lemma S\* | temperament; ω ≤ s_C c_k(1 + ρ) |
| R18 | retrieval and concepts → Claude | Ω | ≈ 6 bits per turn, declared |
| R18′ | draft choice → Claude's words | 3 drafts | log₂3 = 1.6 bits per turn, declared |
| R19 | own rendered face → Π̃ | own data | 0 |
| R20 | own speech → microphone | AEC + half-duplex | 0 while speaking |
| R21 | own face → partner → partner's face | external loop | stable for \|μ\| < 1.67 (H8) |
| R22 | F state → fast gates, cone coefficients, free display, events, ω | forbidden (Check T, E1) | 0 |
| R23 | ASR words depending on prosody | assumption | 0 if ASR is invariant |
| R24–R25 | Ω → P_name → T and F loads | attenuate-only | held ≤ 0.05, toward rest |
| R26 | C_F → concern bid → turn events | innate rules | timing only; fixed amplitude |
| R27 | presence → recognition flash | once per session | fixed (0.35 or 0.20, 0.5 s) |
| R27′ | **his arrival face → m_s → contact-relief display** | latched, centred, Lipschitz, attenuate-only | ≤ 0.040 first minute (H14); session-pooled negligible |
| R28 | his words → K_id, P, I relief, play-surprise laugh → envelopes | T; T1; E1 | per event, masked; tempo-free |
| R29–R31 | his words → words-only model; word → V map; word-need reader → displays | T; weights from own V_F reflex and own Π̃ | as R14 |
| R32 | separation rule | credit only | no display path |
| R33 | ~~valence → draft temperature~~ | **deleted** (no temperature on the subscription) | — |
| R34 | appraisal α → C, bids, retrieval, scoring | knowing → Ω | inside Ω |
| R35 | **b_id → cone centring** | latched per session; enters as −ω F_m s_C c_k b_id | part of R2 (Lemma S\*) |
| R36 | **the cry–laugh split** (his face's cry synergy gates his burst's laugh share) | innate boundary feature | removes laugh-back to sobs; cannot raise any channel |
| R37 | **I crossing → sigh** | part of the curiosity bid | fixed (breath 0.15, 1 s); 1 bit |
| R38 | **residual: sign-reversed partner on a masked pair** | appraisal and G₀ away entries turned in-phase | ≤ +0.16 × loading on any channel; inner brow +0.11 × loading on the H13 instance |
| — | revision 4's warm LP ← BI/LD entries, BI ← LP, the partner anchor in Π̃, the eight named bases and three selection rules, V_F in ω, face and V terms in events, LT in the distress row, κ 0.02 on zero-ceiling channels, R33 | deleted | — |

**Totals per counterpart channel (natural co-movement; words and turn order fixed; H6, H9).**

| Time scale | Toward the partner | Away or across |
|---|---|---|
| zero lag (< 4 s) | ≤ FASTFRAC_k c_k: LP, BU_L 0.35; RHY 0.30; CR 0.25; BI 0.03; zero-ceiling 0 | fast ≥ −0.49 |
| peak after an onset (1-min windows) | ≤ 0.98 c_k | — |
| steady hold | ≤ (s_C + s_X) c_k (+ P_name ≤ 0.05 toward rest) | cone same channel ≥ −0.60 |
| pooled, any stationary partner, across sessions | ≤ 0.996 c_k | — |
| all routes at their caps, rendered | ≤ 0.76 c_k (H9) | — |

### 3.12 Principles, concretely

- **P1.**
  - No classifier anywhere.
  - Three innate feature products are declared as reflexes, not labels: the threat reflex, the cry–laugh split, the play-surprise laugh. Each is a continuous function of continuous features, with a stated theory basis.
- **P2.**
  - The hand-named reactions fall from eight to two newborn reflexes; the rest of the appraisal display is learned (𝓛_A).
  - V, K_id, P and I remain needs named by function; Π₀'s rows remain innate configurations. That is the main remaining strain.
- **P3.**
  - One map, the inverse of the agent's own display, both reads him and is what the agent's own face is trained to be legible to. It is innate from day 1 (Π̃₀ = Π₀⁺).
  - Activation can be read because the agent has its own activation display.
  - The appraisal learns to anticipate its own body.
- **P4.**
  - The constant instruction, the transcript with observable markers and raw snippets.
  - Declared channels: selection 1.6 bits, retrieval ≈ 6 bits per turn; bids and the greeting 1 bit each.
- **P6.**
  - Nothing values his display, his replies to prompts, his time or his engagement.
  - The face, the appraisal reactions and ω are trained without any partner-display term.
  - The laugh reflex is not a reward.
- **P7.** The transcript and snippets go to Claude through the operator's own Claude Code login, as before.
- **P10.** One objective J with typed constraints; the other objectives are likelihoods and self-predictions of the agent's own model. The assembly is listed in §2.12.

### 3.13 The human non-copying signatures C1–C10

As revision 4, all produced, with two changes:
- **C2 (short-lag form divergence) is weaker.** The fast gear now returns smiles and laughs more strongly at short lag, as the operator asked (D81). Form divergence comes from habituation, the appraisal's sign flips, and the fact that the agent's laugh comes mostly from its own play reflex rather than from his laugh.
- **C8 (coupling mostly common cause) is unchanged in the held band,** and the fast band carries more same-channel coupling than before, within FASTFRAC_k c_k.

### 3.14 The scenarios, with numbers (H15)

All are run on the 2 Hz engine of §2.5–2.9 with the constants of §2.1. They use the operator after months (ω smile 0.78, sympathy 0.73, voice 0.80; f_id 0.9; baseline b: LP 0.30, CR 0.15, BI 0.05) unless stated.
- **Not hand-set.** Every word need is decoded by the trained reader of H10 from the utterance, and every face concern by Π̃₀ from the face.
- **The fast echo** is not in the 2 Hz engine; it is given per scenario as θ₀ × his onset. Values are peak / mean over the window.

1. **Silently sad** (BI 0.5, LD 0.4, CHR 0.3, LP 0.05, still, silent; at 120 s "just tired, things at work", decoded T 0.47, V 0.33).
   - **Silent:** lip 0.08 / 0.07 (its resting familiarity level; no smile), inner brow 0.04 at 60–120 s and 0.05 at 5–10 min, head up 0.01, laugh 0.
   - **The bid:** C_F crosses θ_C after 26 s of silence; the body takes the floor in the lapse, and the drafts are re-requested with "[silence 26 s]".
   - **After he speaks:** inner brow 0.41 / 0.15, tilt 0.09 / 0.08, quieter (−0.06) and slower, lip 0.09.
   - **Fast:** his brow onset 0.5 gives +0.01.
   - **Against Q22.** At his 0.5 brow the ceiling allows 0.10 of inner brow from his face. This operator's ω_sym 0.73 gives 0.05; ω_sym = 1 would give 0.07.
2. **Crying** (BI 0.8, LD 0.6, CHR 0.4; sobs BU 0.4 with rhythm 0.15 and ingressive share 0.6).
   - **Boundary:** BU_L 0.00, BU_S 0.40, f_laugh 0.00.
   - **Face and voice:** inner brow 0.07 → 0.08 held, lip 0.06–0.08, **laugh burst 0.00, rhythm 0.00.**
   - **Bid:** concern bid at 27 s.
3. **Anxious before an exam** ("I'm freaking out about the exam", then three rumination turns "and I haven't finished chapter 4…" with no agent turn between; his face and voice show V 0.3, A 0.75).
   - **Decoded:** A 0.57, V 0.52.
   - **The agent:** concern brow 0.23 / 0.17, tilt 0.13, a quieter voice (−0.12), lip 0.12, upper lid 0.08 (its own mild activation at his surprise), no laugh.
   - **Play relief:** none (revision 4: cheek 0.10, laugh 0.10).
   - **Recognised as** activated and distressed, through the agent's own activation display.
4. **Good news, laughing** (smile 0.8, cheek 0.6, laughter; "I got the job!" at 12 s; play replies at 30, 45 and 60 s).
   - **With an earlier worry on the topic** (decoded two days before: V 0.52, A 0.28): lip 0.61, cheek 0.39, F0 range +0.39, own laugh 0.33, upper lid 0.11; a 0.17 concerned brow carried from the worry.
   - **Cold:** lip 0.37, cheek 0.27, laugh 0.33.
   - **Fast:** his smile onset 0.5 → lip +0.11 at 0.45 s; his laugh onset 0.6 → laugh burst +0.14; cheek +0.07. Up to +0.17, +0.21 and +0.11 under context.
5. **Anger at the agent** ("You're useless": BL 0.6, LT 0.5, gaze at it, loud 0.85; calm after 2 min).
   - **Day 1, faithfully** (no readers yet):
     - startle, gaze away 0.09, quieter (−0.17 mean), slower (+0.10), inner brow 0.03;
     - **no frown back** (lid tightener 0, brow lowerer 0).
     - A newborn withdraws but is not yet hurt by words. This corrects revision 4's day-1 row.
   - **After a month** (he has shouted such words before; v_w 0.50):
     - inner brow 0.62 / 0.29, depressor 0.48, gaze away 0.30, energy −0.36, latency +0.23;
     - still 0.21 brow, 0.17 gaze away at 10–15 min;
     - the words are calm, and nothing is credited for placating.
6. **A long warm talk (2 h)** (four clusters of 8 alternating playful exchanges; cluster 4 repeats one joke; a small worry at 27 min resolved at 29.7 min).
   - **Own laugh:** 0.41 in every cluster (revision 4: 0.24, then 0.04–0.05); lip 0.53, 0.32, 0.26, 0.26; cheek 0.44 → 0.21.
   - **The repeated joke** gets no laugh after its first telling (mean laugh 0.11 → 0.06 in that cluster).
   - **The worry:** brow 0.43, then relief lip 0.61.
   - **Between clusters:** lip 0.09. P ends the evening at 0.15 (initiative only).
7. **Reunion after a week** (K_id 0.99, ordinary face).
   - **At sight** (m_s 0): brow flash 0.35, lip 0.61, cheek 0.43, F0 range +0.33.
   - **His first words:** lip 0.51. **12–60 s:** lip 0.40.
   - **A stranger after the same week** (K_id 0): a polite flash 0.20 and lip 0.02 in the held display, plus his own smile returned fast (+0.11 at 0.45 s for a 0.5 smile).
8. **Reunion with bad news** (grieving face at sight: BI 0.5, LD 0.4, CHR 0.3; first words "my father died", decoded V 0.94; then "yeah", "ok").
   - **At sight:** m_s = 1.00, so the brow flash only: lip 0.09 (rest), cheek 0.00 (revision 4: lip 0.63, cheek 0.43).
   - **0–12 s after his words:** inner brow 0.50 / 0.26, tilt 0.12, lip 0.12, cheek 0.
   - **12–60 s:** inner brow 0.23 / 0.21, tilt 0.17, lip 0.12, cheek 0.
   - His later "yeah" and "ok" cannot lower the decoded need, so no relief appears. Revision 4's engine logic would have shown lip 0.65 here.
9. **Teasing** ("Ha, you dumb robot", laughing; playful replies follow).
   - **Quiet affectionate teaser:** lip 0.38, own laugh 0.41, no hurt.
   - **Loud laughing teaser** (energy 0.9, lid tightener 0.4 with laughter; map trained by the threat reflex): the same, lip 0.38, laugh 0.41, no hurt.
   - With revision 4's loudness teacher the same person would have trained v_w 0.66: brow 0.60, depressor 0.47 and gaze away under a weak smile.
   - **Generic map** (such words went with glare from someone else, v_w 0.20): a brief mock-hurt brow 0.34 (mean 0.05) under lip 0.32 and laugh 0.41, halving at each playful reply.
10. **Bored user** ("yeah" or "ok" every 20 s, flat face, 30 min).
    - Lip 0.09, F0 range 0, flat.
    - The curiosity deficit crosses at 14.5 min; a sigh (breath 0.15), then a curiosity bid on the topic of highest expected learning progress.
    - **If he takes it up** (progress 0.25): F0 range +0.32, lip 0.39, outer brow 0.15, upper lid 0.14.

**Expressive and alive, or muted?**
- **Strong:** every scenario with words, and greetings at sight; laughter now lasts the evening.
- **Weaker by the operator's ceilings:**
  - the sympathy brow at a silent face (0.05);
  - the agent's held laugh-back while he keeps laughing, small because laughter's budget went to the fast gear (D81).
- The agent's own big laughs come from its play reflex, on content.

### 3.15 Time scales from structure

| Scale | Carrier | Time constants |
|---|---|---|
| reflex | fast wrap (echo 0.45 s), onset reflexes | 33 ms – 4 s; provisional onset 0.25–0.9 s |
| appraisal | δ_app, envelopes, band-pass, arrival appraisal | 0.6 s; 1–6 s; 20–90 s |
| conversational | cone traces, C_F and C_L, bids | 20 s – 2 min; lapses 6–8 s |
| hurt, worry | hurt latch, C_F release, P_name | 2–10 min |
| mood | μ ladder, cone traces | 20 min – 73 h |
| needs | I (1 h), P (5 h), K_id (36 h), E (day) | hours – days |
| his usual face | b_id, d_b,id | ≈ 6 sessions |
| relationship | ω (≈ 60 sessions), slots, familiarity | months |
| temperament | consolidated weights, Δ, W, Γ^{(3,4)} | ≈ 100 nights |

### 3.16 The brief's expressive-structure items

- **Content-dependent selection** happens in six places:
  - the learned appraisal selection;
  - the fast attention mix;
  - 𝒦 retrieval;
  - draft scoring;
  - topic-wise need and progress;
  - concept-weighted snippets.
- **Structure over people, episodes, topics and time:**
  - identity × topic × episode slots;
  - per person: ω, b_id and d_b,id, the word → V adapter and **K_id**;
  - topic-wise need and learning progress;
  - the time-constant ladder.
- **Effective dimensionality:**
  - T: μ_T 128, slots 128 × 64, loads;
  - F: traces 4 × 36, the band-passed input;
  - α 12; the face: Π₀ plus 23 learned synergy amplitudes (masked).
- **A behaviour a low-dimensional version cannot produce.**
  - Different faces for equal loads with different concepts or slots (Δ).
  - The same teasing words read as play from one person and as hurt from another (the per-person word → V adapter and ω).
  - A reunion that is glad with one arriving face and quiet with another (m_s × K_id).
  - Collapse slots, α and Δ to valence and arousal, and all three vanish (§7).

### 3.17 Assumptions (places to attack)

1. ASR lexical invariance to held prosody.
2. TTS realises phrase targets at about unit gain.
3. Burst features carry no labels; **the cry–laugh split's features (4–6 Hz depth, ingressive share) can be measured reliably from a laptop microphone.**
4. **The sign mask** and its residual R38.
5. **Lemma S's 1-min version** (the partner's variance mostly below 1/min); the critic showed the bound holds even when this fails for laughter.
6. The type tags are enforced in code and tested at load.
7. **The word readers.** Words carry the need that his face shows, and his face is read correctly by the agent's own inverse (§8.1).
8. **The separation rule** is structural, not causal.
9. **r_k (new).** The rectification allowance is the worst over the stated partner families: laugh bursts ≥ 0.5 s at ≤ 6 per minute; face episodes ≥ 1.5 s. Shorter or denser bursts could exceed it. A partner who laughs in 0.2-s clicks at 20 a minute is outside the families.
10. **Lemma S\* (new).** His session-to-session variation is captured by a first-order baseline. A partner whose mood jumps every session, at a period shorter than τ_b, is within the bound by H1; one whose mood changes at exactly τ_ω's frequency sets ρ.

## 4. Why the closest mechanisms cannot do it alone

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| Robust REN / Cayley sector (Revay et al.) | a full-band disc for every parameter | a disc is nearly two-sided for small gains, so the agent is muted (revision 2); and it says nothing about the DC that `sat` creates from a zero-DC block (§3.1) |
| Positive-real or quadratic-form sector on held state | one-sided along every direction eᵀ | bounds a projection, not a rendered channel (routes critique 3) |
| Context-gated attention, FiLM, gated units | content-dependent gains | multiplying a DC-passing partner signal by a correlated context has no bound in the gain (Lemma S ii) |
| Automatic gain control, slowly adapted gains, per-user calibration | a gain that tracks the user over weeks | the same seam one time scale up (Lemma S ii across sessions: +0.31 to +0.89 measured on revision 4). The gain is safe only if what it multiplies is centred on a faster baseline (Lemma S\*) |
| Monotone operators, input-convex networks | one-sided incremental maps | symmetric Jacobians force "warm to your sadness" to mean "sour to your smile" |
| Path-specific objectives (Farquhar et al.) | no incentive through a delicate node | with the display as the node, expression gets no gradient; here expression has two display-blind objectives of its own (𝓛_display, 𝓛_A) |
| Bayesian reverse appraisal (Ong, Wu, Houlihan) | the partner's expression as evidence | an observer model; the response step and its bounds are not in it |
| Predictive coding of one's own expression | a face that anticipates its own state | gives 𝓛_A's form, not the cap set it is projected onto, nor its use as a learned selection over bounded reactions |
| Learning-progress curiosity (Oudeyer, Schmidhuber) | satiable information drives | becomes engagement-seeking in a dyad unless partner content is imputed in rollouts, as here |

## 5. The whole system, walked through

- **Perception.**
  - MediaPipe → P₀ → reflection → u.
  - Prosody, timing, bursts, with **the cry–laugh split**.
  - The derived features (loudness, glare, laughter, Duchenne smile).
  - The fast block reads w = v − s_f in the agent's own synergy coordinates. The cone, the appraisal, C_F and Π̃ read his own face, Pu.
- **Latent state.**
  - T: E, K_id, P, I, h, A_L, N_L, C_L, μ_T, slots_T, f_id, ω, and the latched b_id, d_b,id, m_s.
  - F: traces, the band-passed input, α, C_F, V_F, A_F, μ_F, slots_F.
  - 𝒦: 𝓜, 𝓛_w, categories.
  - Nothing is labelled.
- **Face and voice.** y = sat(y_f + y_C + y_A + y_o) + visemes; the laugh synthesizer reads BU_L, RHY and BRE; there is no sob synthesizer.
- **Claude.** Three forked Claude Code sessions per turn; snippets steered by need, concern, concept and curiosity; selection by J under the separation rule. Heard back through P_name.
- **Initiative.**
  - Provisional body onset at the predicted turn end, abortable.
  - Follow-up; concern bid; curiosity bid with a sigh.
  - Recognition at sight and an arrival appraisal.
- **Learning by living.**
  - States online.
  - Nightly: 𝓜, Π̃ (own data only), the readers, 𝒜, W and Γ^{(3,4)}, Δ, the scorer; ω and the baselines per session.
- **Memory and replay.** As revision 2. Remove the state tags from replay, and partner-specific slot recall, ω, b_id, K_id and familiarity decay (S6).

## 6. A buildable network (Apple-silicon Mac, on the operator's subscription)

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

As revision 4, plus:
- the cry–laugh split (4–6 Hz modulation depth from a 1-s sliding spectrum of the burst envelope; ingressive share from the spectral tilt of breath noise; both in the GeMAPS-lite pass);
- the per-identity baselines;
- Π̃₀, computed once from Π₀.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, filters, H_i, H_o, M, cone traces, band-pass, centring, cry–laugh split **[M]** | fixed | 0 | — |
| 2 | 𝓔 (own appearance; R its ridge inverse) | 12 → 64 → 23 | ≈ 2,400 | replay, own face |
| 3 | 𝓡_θ, robust REN, no context input **[M]** | n 64, q 128; input 116; output 33 | ≈ 110,000 | replay (likelihood of own fast dynamics plus θ₀ pull) |
| 4 | fast gates and attention from T c̃ **[M]** | 64 → 33; 64 → 33 × 16 queries | ≈ 37,000 | replay |
| 5 | gain logits φ_k | 33 | 33 | replay |
| 6 | T context encoder c̃ | (lexical 64 + order 8 + identity 16 + ω 4 + E, C_L, h, A_L 4 + slot read 64) → 64 | ≈ 10,000 | replay |
| 7 | held cone: innate G₀, ω scaling, baselines **[M]** | 4 × 36 × 36, innate; b_id 36 per identity | 4 + 36 per identity | per session |
| 8 | appraisal 𝒜 **[M]** | (band-passed 36 + c̃ 64 + loads 7 + ω 4) → 64 → 12 | ≈ 7,500 | replay (likelihood) |
| 9 | appraisal selection W and two learned bases **[M]** | 12 → 5 softmax; Γ^{(3,4)} constrained (≈ 33 diagonal + ≈ 160 allowed cross entries each) | ≈ 450 | replay (𝓛_A) |
| 10 | free display Π_o: Π₀ + masked synergy Δ **[M]** | (T inputs 161) → 128 → 18 open synergies | ≈ 23,000 | replay (𝓛_display) |
| 11 | Π̃ (one own-body inverse; Π̃₀ = Π₀⁺ at birth) **[M]** | 12 + 64 → 64 → (5 loads + 32 state) | ≈ 7,300 | replay (own data only) |
| 12 | word-need reader **[M]** | (64 + 16) → 64 → 3 | ≈ 5,400 | replay (cross-modal through Π̃) |
| 13 | word → V map with identity adapter **[M]** | (64 + 16) → 32 → 1 | ≈ 2,600 | replay (threat reflex) |
| 14 | words-only partner model 𝓛_w | GRU 64 over 64-d utterance embeddings | ≈ 25,000 | online error, replay |
| 15 | μ ladder writes and gates; slots | as revision 3 | ≈ 33,000 | replay |
| 16 | 𝓜: LRU 2 × 128, innate moduli | as revision 3 | ≈ 330,000 | online fast heads + replay |
| 17 | 𝓜 heads: own body, own face, partner N, F (action-blind), Q, f_recv | 256 → 64 → (3, 23, 3, 36, 72, 6) | ≈ 75,000 | replay |
| 18 | concept layer, PMI (own tokens) | states | 0 | online |
| 19 | draft scorer | 64 → 2 | 130 | replay (J) |
| | **total learned** | | **≈ 669,000** | |
| frozen | MediaPipe (× 2), Whisper-small (streaming), MiniLM, TTS + WORLD, AEC | | | |

### 6.3 Objectives

- 𝓛_𝓜, 𝓛_𝒜, 𝓛_w: likelihoods.
- 𝓛_own: 𝓔 and Π̃ on own data only (no partner anchor).
- The two readers (§2.8).
- 𝓛_display (§2.7) and 𝓛_A (§2.6), each with a projection or mask.
- 𝓛_J: the scorer and the retrieval query only.

Every constraint holds for every free vector:
- the REN by direct parameterisation;
- the fast gates by a scaled sigmoid onto [−g_min, 1];
- the cone by being innate and scaled within [−1, 1];
- the appraisal bases by projection onto a convex set;
- Δ by tanh on the open synergies;
- the type rule by construction and a load-time trace.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms):**
  - MediaPipe ≈ 13 ms each (own process);
  - traces, centring, band-pass and the burst split < 0.2 ms;
  - REN < 1 ms; cone and appraisal products < 0.1 ms;
  - render 3–5 ms.
- **At 2 Hz:** T and F state < 1 ms; 𝒜 and selection < 0.2 ms; 𝒦 < 3 ms.
- **Memory:**
  - engine online < 2.4 GB;
  - Whisper-small ≈ 0.5 GB; TTS and WORLD 0.1–0.5 GB;
  - three Claude Code processes 0.6–1.2 GB;
  - total ≈ 3.6–4.6 GB, under the 6 GB rule.
- **Replay** < 2 GB, about 45 min a night on MPS. **Store** ≈ 1.8 GB per 30 days.

### 6.5 Claude through Claude Code, on the subscription (D84; agent finding 7)

What the subscription offers, from the project's note research/claude-code-agent-sdk-controls.md:
- model choice and five effort levels;
- a replaced system prompt;
- session resume and fork;
- streamed partial messages and interruption;
- an output-token cap that only truncates.

It offers no temperature, no `max_tokens`, no cache control, no log-probabilities and no prefill. The pattern below uses only what it offers.

- **Process.** The Claude Agent SDK for Python, which spawns the local Claude Code CLI on the operator's own login (never `--bare`, which needs an API key). Ailurini is itself built on Claude Code, so this is the same route it uses (D84).
- **Options, fixed for the engine's lifetime:**
  - `system_prompt` replaced by the constant instruction (byte-stable, so Claude Code's own prompt caching sees one prefix);
  - `tools=[]` (no tools);
  - `effort="low"`; `model="haiku"` by default, with the operator choosing a larger model at the cost of latency;
  - `include_partial_messages=True`;
  - `CLAUDE_CODE_MAX_OUTPUT_TOKENS=120` as a safety truncation only. Length comes from the instruction ("reply in one or two short sentences").
- **One canonical session per conversation.**
  - At p_end ≥ 0.7 the engine starts **three forks** of the canonical session (`resume=<canonical>`, `fork_session=True`), so their process start overlaps his last words.
  - At the turn end each fork receives the same new user message: his utterance, any observable markers and the ≤ 3 snippets, followed by one of three fixed "attend to" lines (what he said; how he seems to feel, from his words; what this reminds you of). That line is the only text that differs.
  - There is no sampling parameter, so diversity comes from these lines and the model's default sampling (Q23's recommendation).
- **Selection.**
  - Each fork streams. When its first sentence ends, the scorer rates it by a 30-s rollout.
  - The winner continues; the two losers are interrupted (`client.interrupt()`).
  - The winning fork's session id becomes the canonical session, so the history contains only what the agent actually said.
  - If he resumes speaking within 0.40 s of the provisional onset, all three forks are interrupted and discarded.
- **Latency.** About 1.5–3 s from his turn end to the first word: process and session overhead, adaptive thinking at effort `low` (it cannot be turned off on the 5.5 models through Claude Code), and no prefix control. The body onset (0.25–0.9 s), the inhale and gaze cover the first second; a soft backchannel ("mm") from the free display covers the rest when the wait exceeds 1.5 s.
- **Usage.** About 150 agent turns a day × 3 drafts × 1.3 for speculative starts ≈ 600 calls a day of a few thousand tokens each, mostly cached. This must be measured in the first week. If it strains the subscription's limits, the engine falls back to two drafts, then to one draft with interruption as the only lever.
- **Deleted:**
  - temperature 0.1(1 + r) and route R33;
  - `max_tokens`;
  - explicit cache breakpoints;
  - "thinking off";
  - the six-call pattern.
- **What the state still controls:**
  - which draft (1.6 bits);
  - which snippets (≈ 6 bits);
  - when Claude is called and when it is stopped.

### 6.6 TTS: pitch, energy, rate and laughter (buildability risk, named)

- **Plan A (revised, after the agent critic).** Any good local neural TTS. Then shift phrase-level F0 level and range and duration by WORLD analysis–resynthesis (pyworld, a few tens of ms per phrase on CPU). That gives unit-gain phrase targets largely independent of the TTS chosen.
- **Plan B (fallback).** macOS AVSpeechSynthesizer: per-utterance pitch, rate and volume.
- **Laughter.** An innate parametric source–filter laugh synthesizer (glottal pulses at the agent's F0, 4–6 Hz amplitude modulation, breath noise), driven only by y_BU_L, y_RHY and y_BRE. There is no sob or cry source, and nothing routes a sob to it (R7′).
- **The risk.** A synthetic laugh is the agent's main positive vocal display, and an uncanny one would undermine its liveliest moments. A listening test with the operator comes before S2 (a voice-identity matter under Q1).

## 7. Ablation predictions (Principle 5), from the properties

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| Lemma S\* (uncentred cone; ω multiplying his level) | the month-swap surrogate shows session-pooled slopes above c_k (revision 4: +0.31 to +0.89) for partners whose mood co-varies with play or hurt | §3.2, H1 |
| Lemma S (gate the cone within a session) | pooled slopes above c_k for partners whose face co-varies with words or tempo | revision 4 H1 |
| E1 (events read face care and V_F) | at a silent sad face the inner brow jumps to 0.32–0.42 (above c_BI); at a glaring partner a lid tightener 0.24 appears | H3 (critic D4) |
| the partner anchor in Π̃ (restore it) | the agent's display code drifts toward his (cosine 0.15–0.26), and zero-ceiling synergies enter its concern display | H4 |
| the own-display mask | after 20–40 nights the learned face uses nose wrinkle, dimpler and lip press for worry, visible to raters | §2.7 |
| FASTFRAC (set the fast caps to revision 4's 0.186) | his smile and laugh are returned about half as strongly within 0.5 s (0.186 against 0.35 per unit); the operator's facial following of the agent at lags < 1 s (S5) falls | §2.4 |
| r_k accounting (keep full fast caps, revision 4's held shares) | pooled laugh-burst slope up to 0.5·1.09 + 0.2 + 0.254 + 0.867 = 1.87 c, above its ceiling | H5, H6 |
| rule J | at a sad or crying face the agent smiles (lip 0.21–0.28, revision 4) | §2.5, H15 |
| the cry–laugh split | the agent's laugh synthesizer fires at his sobs (fast echo up to 0.23 per unit sob onset) | §2.2 |
| the arrival appraisal m_s | it beams at a grieving arrival (lip 0.63, cheek 0.43, revision 4) | §2.9, H15.8 |
| K_id → one shared K | a stranger is greeted almost like the operator (revision 4: 0.54 against 0.61) | §2.8 |
| 𝓛_A (freeze W and the learned bases at birth) | the appraisal stays two reflexes: no learned hurt-withdraw to glare, no concern at laughter over a sad topic (H13); reactions no longer vary by person | §2.6 |
| the activation row of Π₀ | the reader's A output has no target; anxiety is read as distress only, and the calm voice at an anxious user loses its activation-specific part | §2.7, H10 |
| the threat reflex's laughter exemption | a loud laughing teaser and loud praise train hurt (v_w 0.66): brow 0.60 at teasing | H11, H15.9 |
| f_glare in the threat reflex | the word → V map learns only from non-laughing loudness; glare-only hostility never trains hurt | §2.8 |
| the play-surprise reflex (laughter from P only) | own laughter stops after the first ten minutes of an evening (revision 4: 0.24 → 0.04) | H12 |
| the alternation and safety conditions of the play rule | anxious rumination earns play relief (revision 4: cheek 0.10, laugh 0.10) | H12 |
| the non-substantive rule for N_L | "yeah" after bad news relieves the worry: a smile 0.65 a minute after "my father died" | H15.8 |
| **crossed-habits word-route lesion** (swap the agent's own hurt and relief displays for a week) | Π̃ inverts sad faces toward relief; within about a week the word-need reader's output for loss words falls toward zero and word concern at bad news vanishes; reverting restores it | §2.8 (agent critic §2.3) |
| Δ's mood, slot and concept inputs | raters, or a fixed population face model, can no longer tell the concept category from the agent's face above the six-scalar floor (observer-side; not Π̃ itself) | §2.7 |
| ω (fix at priors) | no relationship-specific smile return or sympathy | §3.6 |
| P, I, the greeting, the turn-end gate, the zero ceilings, S5 free of common cause, state tags in replay | as revision 4 | §7 of revision 4 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **New weakest point: reading him rests entirely on the agent's own expressive code.**
   - Π̃ is one map, trained on the agent's own (state, face, voice) pairs, with no partner anchor. That closes the co-training drift (H4), but it means the agent reads his inner state only as well as his code resembles its own.
   - Some people show distress through channels the agent's display never uses: a lip press, a brow lowerer, a chin raise, a flat face over a tight voice. Such a person is under-read (H10's synthetic partner uses a chin raise the agent ignores). Both word readers inherit the under-reading.
   - The only correction is slow: separated reports that disagree with the decoded need.
   - Falsifier F8′.
2. **The sympathy brow at a silent face is small in absolute terms.** At his 0.5 brow the Q22 ceiling allows 0.10; this operator's ω_sym 0.73 gives 0.05, and ω_sym = 1 gives 0.07. The concern bid at 26 s and the words carry the rest. An absolute 0.20 at a still 0.5 brow would need a ceiling of 0.40, which is the operator's call.
3. **Laughter's budget went to the fast gear (D81).** The held laugh-back while he keeps laughing is small (0.09 c at hold). The agent's own big laughs come from its play reflex, on content. If people in fact laugh back in a held way, the allocation should change, within the same ceiling.
4. **r_k is measured, not proved** (assumption 9). Very short, dense laugh clicks are outside the families.
5. **The sign mask's residual R38** binds on the inner brow for a partner whose brow rises with his laugh (up to 0.31 at loading 1, against 0.20).
6. **The innate reflexes added** (cry–laugh split, threat reflex, play-surprise laugh) are each a few lines of P2 strain, declared as reflexes with a theory pointer. None is a label on the user. Cold, quiet contempt is still never learned as hurt: no reflex covers it.
7. **The separation rule** is structural, not causal; the S4 basis caveat; the default act ā carries moral content (as revision 4).
8. **Subscription latency.** First words 1.5–3 s after his turn end, with the body covering the first second. Usage of about 600 calls a day has to be measured.

### 8.2 Falsifiers (state-level, once built)

- **F1.** With partner-swap, segment-shuffle, timing-resample and **month-swap** surrogates (words and turn order fixed), any channel exceeds one of:
  - its pooled bound (§3.3);
  - its steady hold;
  - its zero-lag cap FASTFRAC_k c_k.

  Or phrase timing tracks his timing.
- **F2–F7.** As revision 4 (knowing; crossed habits for C_F; separation-window credit; smile amplitude moving T state; C_F threshold timing; naming).
- **F8′.** Π̃'s readings of his face disagree with his later separated reports more than a person-independent baseline does; or the word-need reader's agreement with reports falls over nights.
- **F9.** At bad news, or at a grieving arrival, the cheek raise or the relief envelope rises within 2 s.
- **F10 (new).** Any laugh-synthesizer output within 2 s of his sob bursts.
- **F11 (new).** The learned appraisal bases or Δ place weight on BL, LT, LPR, NW or DIM synergies.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (all Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Report 5, Q16, Q18 and answer, Q19, Q20–Q23 with the operator's answers of 2026-11-26T08:41:00Z | in full |
| DECISIONS.md D78, D80, D81–D84 | in full |
| research/foundations/designs.md | in full |
| design-cayley-ledger.md revision 4 (saved as .r4.md), including "Critiques of revision 4 and the answer" | in full |
| critique-4-design-cayley-ledger-routes.md; sims/critique-cayley4-routes/checks.py and out.txt | in full; partners D1–D8 re-run in H1, H3, H4, H5, H8, H9 |
| critique-4-design-cayley-ledger-agent.md, including its seven fixes; sims/critique-cayley4-agent/scen.py and out.txt | in full; scenarios A–F re-run in H15 |
| research/claude-code-agent-sdk-controls.md | in full (§6.5) |
| sims/design-g4/checks.py (engine and constants) | the parts reused in design-g5 |
| **Not read, named only as pointers:** Simner 1971, Sagi & Hoffman 1976 (neonatal reactive crying); peek-a-boo laughter and incongruity in infancy; Provine on laughter contagion; Keltner et al. 2001 (teasing); Heerey & Crossley (anticipatory smiles); Bachorowski et al. (laughter acoustics) | nothing depends on them beyond what is argued here |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.**
- the fast wrap: a robust REN in a conic sector, with per-channel gains;
- the cone: per-channel box constraints on an LTI map over completely monotone kernels, with a signed mask, centred on a running baseline;
- the appraisal display: a constrained mixture of linear maps on a band-passed input, trained to predict the agent's own display;
- care: Yoshida & Man with path-specific credit;
- valence: Joffily & Coricelli, event-indexed;
- curiosity: Oudeyer's learning progress;
- reading others: the inverse of one's own display (Principle 3; analysis by synthesis).

**Clause 2 (a changed invariant, a derived update, deleted scalars): not met.** Two design rules are new to this project and stated nowhere I have read in this form:
- **Lemma S\*:** a slowly learned gain is safe on a partner path only if what it multiplies is centred on the partner's own baseline at a time constant much shorter than the gain's. Then the pooled slope over any time scale is ≤ sup|g|(1 + τ_b/(τ_b + τ_ω)). It is the elementary fact behind Lemma S, applied again one time scale up. Its use is to close the last seam the critics found with one construction rule instead of a freeze.
- **Anticipation of one's own innate display as the training signal for social reactions:** a predictive-coding objective, applied to selection among capped reactions.

Neither is a new mechanism.

**Deleted from revision 4:**
- the warm sadness → smile entries;
- the partner anchor in Π̃;
- six of eight appraisal bases and the three selection rules;
- V_F in ω and in the events;
- LT in the distress row;
- κ on zero-ceiling channels;
- temperature and R33;
- the six-call draft pattern;
- one shared K.

**Added (innate unless stated):**
- FASTFRAC and the r_k accounting;
- the centring baselines;
- rule J;
- the signed synergies and the reflection rule;
- the cry–laugh split, the threat reflex and the play-surprise reflex;
- the activation row;
- K_id;
- the arrival appraisal;
- the sigh;
- learned: W and two appraisal bases.

**My honest verdict.** A careful recombination, with no concrete failure I can find after closing all of revision 4's findings, and with the operator's two emphases met: fast per-expression mimicry up to the ceilings, and Claude through Claude Code. Under D82 it can go to the operator as a build candidate (a testbed), stated as a recombination, once the next critiques find no concrete failure. The search for a new core mechanism continues in parallel.

---

## Revision 2 history

Kept in `design-cayley-ledger.r2.md` ("Revision 2 history"). Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revision 2 and the answer, and the revision 3 history

Kept in `design-cayley-ledger.r3.md`.

## Critiques of revision 3 and the answer, and the revision 4 history

Kept in `design-cayley-ledger.r4.md` ("Critiques of revision 3 and the answer"; "Revision 4 history (2026-11-26): each critic finding and how it is closed").

## Critiques of revision 4 and the answer (recorded 2026-11-26T08:24:59Z, under Q19)

**Routes** (critique-4-design-cayley-ledger-routes.md; checks in sims/critique-cayley4-routes/).
1. **Medium–high (D78, weeks scale): the word seam returns through ω.** ω_smile is fixed within a session but learned over about 20 sessions from play relief and loudness/glare, which follow the partner's month-long mood. The gain on his smile therefore rises and falls with his smile level (Lemma S case ii, one level up). Session-pooled lip-pull slope is +0.31 to +0.89 against ceiling 0.35. The absolute effect is small (0.05–0.08), but one quantity moves five channels.
2. **Medium (spec text): face and voice enter the uncapped free display.** Section 2.1 builds relief and distress events from care (which reads the face) and from V (loudness, glare). Built as written: lid tightener 0.24 (ceiling 0), inner brow 0.32–0.42 (ceiling 0.20). The H11 engine already uses only words and hurt, so the scenario numbers stand; the text must be fixed.
3. **Low–medium: the face–reader loop pulls the agent's expressive style toward the partner's** (cosine 0 → 0.26). It can bring zero-ceiling channels into the word-driven concern display.
- **Low:**
  - the fast echo after clipping gives laugh-burst energy +0.07 (claimed ≤ 0.01);
  - ω_smile saturates (0.98–1.0) for any partner who plays at all;
  - two of G₀'s glare entries sit outside its budget set.
- **No concrete failure found:** Lemma S and the appraisal display; T1 within a session; the ceilings and face–voice sign mask (worst lip pull 0.27, whole face ≤ 0.35); the relationship loop (≤ 0.175); the counter-mimicking partner (stable for |μ| < 1.67); curiosity and turn gating.

**Agent and fitness** (critique-4-design-cayley-ledger-agent.md; sims/critique-cayley4-agent/). **Close, but not yet fit.** None of the failures touches the copy certificate. Of critique 3's nine changes, four are closed and five are partly closed.
- **Concrete failures:**
  - The reunion greeting at sight beams at a visibly grieving face (lip 0.63, cheek 0.43; stranger 0.54).
  - Silent sadness and crying get a slight smile (0.21–0.28) with almost no inner brow (0.03–0.05), and sobs reach the laugh synthesiser through route R7. This contradicts what Q22 told the operator.
  - The appraisal display's choice among eight reactions has no training objective, so it stays three hand-written rules.
  - The learned-face objective favours the anger, disgust and contempt channels, because the innate display leaves them unused.
  - The agent can read in others only what its own face shows (tiredness, hurt); it cannot read anxiety.
  - Claude drafts "temperature 0.1(1+r)" is not buildable on the subscription, and the call pattern assumes API-key features. An API key is a new paid service: operator's decision (Q23).
  - The hurt map learns from loudness, so loud praise or loud teasing trains hurt.
  - Smaller: the day-1 anger figures use a word reading not yet available; play laughter is used up within 10 min; the play rule fires on anxious rumination.
- **Principles:** the word-to-hurt map is not a classifier, but its teacher (an innate anger-display reflex) must be declared as a reflex. The eight appraisal reactions are the main Principle 2 strain.

**The answer (maintainer).** All findings are accepted.
- **The copy certificate held within sessions in both critiques.**
- **What remains:**
  - one slow route (ω learned across weeks from states that follow the partner's mood);
  - spec-text routes;
  - sympathy and grief handling;
  - the trainability of the appraisal display and the learned face;
  - reading states the agent's own face cannot show;
  - buildability on the subscription.
- **Next:** revision 5 (revision 4 saved as design-cayley-ledger.r4.md). Status: held.

## Revision 5 history (2026-11-26): each finding and how it is closed

Checks: `sims/design-g5/checks.py` (H0–H15; out.txt, 15/15 pass). Revision 4 is saved as `design-cayley-ledger.r4.md`. Written after the operator's answers to Q20–Q23 (D81–D84), with D81's emphasis that fast, partial, per-expression mimicry must stay, and D84's that Claude is reached through Claude Code.

**Routes critique (critique-4-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 (medium–high) | ω learned over weeks from mood-following states multiplies his level: session-pooled lip pull +0.31 to +0.89 against 0.35 | **Lemma S\*.** The ω-scaled cone diagonal multiplies his deviation from his own baseline b_id (τ_b 6 sessions), not his level, and ω learns slowly (τ_ω 60). The pooled multi-session toward slope is ≤ s_C c_k(1 + ρ), ρ = 0.091, for any ω process. ω also no longer reads V_F (F); month-swap surrogate added to F1 | §2.5, §3.2; H1: critic's D3/D3b partners +0.023 / +0.012; adversarial ω over periods 8–3000 sessions ≤ 0.001; bound 0.191 |
| 2 (medium) | spec text routes face-borne care and V_F into the free display (LT 0.24, BI 0.32–0.42) | **E1:** events are built from T parts only (𝒟_p(N_L), h, K_id, P, I, the play-surprise laugh); N̂_F, C_F and V_F are knowing, bids and cone/appraisal input only; LT removed from Π₀'s distress row | §2.1, §2.2 rule 3, §2.7; H3: LT 0.00, BI from events 0.00 |
| 3 (low–medium) | the face–reader loop pulls the agent's style toward his (cosine 0.26) and can bring zero-ceiling channels into its concern display | the partner anchor in Π̃ is deleted (one own-body map, trained on own data only, partner reading = the same map); the own-display mask removes BL, LT, LPR, NW, DIM synergies from Δ and from every learned appraisal basis | §2.7, §2.8, §2.2 rule 8; H4: cosine 0.000, weight 0 (revision 4 anchor with a lip-press partner: 0.15 and 0.22) |
| 4 (low) | the fast echo after `sat` gives laugh-burst energy +0.07, against a claimed ≤ 0.01 | the rectified DC is measured at the full gate over partner families as r_k and charged to each channel's pooled budget; held shares are sized so that every channel totals ≤ 0.996 c_k. Under D81 the fast caps rise to the ceilings themselves on smile, cheek and laughter (κ_k = c_k(1 + γ)/2γ), so r_k is large there (0.87 c on bursts), and the held laugh share is small | §2.1, §2.4, §3.1, §3.3; H5, H6; H9: all routes together at their caps, rendered, ≤ 0.76 c |
| 5 (low) | ω_smile saturates (0.98–1.0) for any partner who plays at all | s_smile = 0.3 + 0.7·min(1, ρ_play/0.6) − 1.3·min(1, h̄/0.10), normalised by the session's available play deficit, without tanh; rate 1/60 | §2.12; H2: 0, 1, 2, 4 play turns → 0.30, 0.66, 0.91, 1.00; hurt 0.05 lowers each by 0.65 |
| 6 (low) | two G₀ glare entries on the 20-s trace lie outside its (zero) charged budget | moved to the 2-min and 20-min traces and resized; every G₀ entry checked against its set with signed derived features and the reflection rule | §2.5; H7: all entries in budget |

**Agent critique (critique-4-design-cayley-ledger-agent.md), its seven fixes and smaller items:**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 | the greeting at sight beams at a grieving face (lip 0.63, cheek 0.43); identity-blind (stranger 0.54) | recognition flash at sight; an arrival appraisal m_s (his face over the first 1 s through Π̃, centred at his own arrival baseline, latched) multiplies all contact relief of the session by (1 − m_s); his first words still mask by word distress; K per identity (K_id), 0 for a stranger; a non-substantive reply cannot relieve a decoded worry | §2.8, §2.9; H14 (route bounded: 0.040 first minute; −0.012 across sessions); H15.8: m_s 1.00, lip 0.09, cheek 0 at sight; stranger lip 0.02 with a 0.20 flash |
| 2 | sympathy at silent sadness and crying is a smile (0.21–0.28) with inner brow 0.03–0.05; sobs reach the laugh synthesizer | rule J (no sadness → joy positive entry anywhere; the warm LP ← BI/LD entries deleted); inner-brow held share 0.70 c filling within a minute, fast fraction 0.15; attentive head entries; word-concern lip 0.12 → 0.05; the cry–laugh split at the boundary with BU_S at ceiling 0, κ 0, no synthesizer | §2.1, §2.2, §2.5; H15.1–2: lip 0.07–0.08 (rest), inner brow 0.05 silent, 0.08 crying, laugh 0.00, bid at 26–27 s. The absolute brow is limited by Q22's 0.20 copy fraction (§8.1.2) |
| 3 | the hurt teacher is loudness, so loud praise and loud teasing train hurt | the teacher is a declared innate threat reflex: g_at·max(glare, loud·(1 − 2 f_pos)₊), f_pos = max(laughter, Duchenne smile) | §2.8; H11: loud laughing teaser and loud praiser v_w 0.00 (revision 4: 0.66); shouted insults 0.50; H15.9 |
| 4 | the appraisal's selection W has no objective; it stays three hand-written rules | W and two learned bases trained by 𝓛_A (anticipate the agent's own innate display 2 s ahead; projected onto the cap set); hand-written reactions 8 → 2 newborn reflexes | §2.6; H13: learns hurt-withdraw to glare (selected 0.94) and concern at laughter over a sad topic (0.78), no violations; ablation in §7 |
| 5 | the learned face pays for a private code on the anger/disgust/contempt channels; the Δ prediction is circular; the Π̃ heads are underspecified | own-display mask; one Π̃ map, own data only, no anchor; observer-side prediction (raters or a fixed population face model) | §2.7, §2.8; H4; §7 |
| 6 | the agent reads in others only what its own face shows; no anxiety | an activation row in Π₀ driven by the agent's own latched lexical surprise (T); Π̃₀ = Π₀⁺ reads activation from day 1; the word-need reader outputs (V, A, tiredness) and drops K and P | §2.7, §2.8; H10: "freaking out" → A 0.57; anxious face → A 0.54; H15.3 |
| 7 | the Claude call pattern assumes API-key features and a temperature | §6.5 re-specified for Claude Code through the Agent SDK on the operator's login (D84): three forked sessions, replaced system prompt, no tools, effort `low`, length by instruction, losers interrupted; temperature, R33, `max_tokens` and cache control deleted; latency 1.5–3 s stated; usage ≈ 600 calls a day to measure | §2.11, §6.5 |
| smaller | day-1 anger row used a word reading not yet available | reported faithfully: inner brow 0.03, gaze away 0.09, quieter −0.17, slower +0.10, no frown back | §3.14.5 |
| smaller | play laughter exhausted within ten minutes | a per-event play-surprise laugh reflex, habituating to repeated content (through the words-only model's surprise), not drawn from P | §2.8; H12: 0.40 per play turn in all four clusters, 0 for a repeated joke; H15.6 |
| smaller | the play rule fires on anxious rumination | play needs an agent turn between his turns (turn order) and his word care below its dead-band; hurt no longer blocks play | §2.8; H12: 0 of 3 rumination turns qualify; H15.3 |
| smaller | the need reader is set by hand in the scenarios | every scenario need is decoded from the utterance by the trained reader of H10, and every face concern by Π̃₀ | §3.14; H10, H15 |
| principles | the innate anger-display teacher must be declared as a reflex | declared, with the cry–laugh split and the play-surprise laugh, in §2.12's assembly list | §2.8, §3.12 |
| recommended | an event display at a threshold crossing; the crossed-habits lesion; a laugh listening test | the sigh before a curiosity bid; the crossed-habits word-route lesion in §7; the listening test in §6.6 | §2.9, §7, §6.6 |

**Operator answers folded in (D81–D84).**
- **D81:** fast, partial, per-expression matching stays, so the fast caps equal the ceilings on smile, cheek and laughter (returned at 0.45 s; lip and laugh 0.227 per unit onset innate, up to the ceiling under context), with its DC counted.
- **D82:** the novelty verdict is stated plainly for the operator.
- **D83:** the per-expression ceilings are kept; words and face feed the appraisal.
- **D84:** Claude is reached through Claude Code on the subscription.

**Status:** revision 5; to be critiqued. For the routes critic:
- Lemma S\* and the month-swap surrogate;
- r_k's partner families (assumption 9);
- the new residual R38 on the inner brow;
- the arrival mask;
- the cry–laugh split as a route.

For the agent critic: sympathy at a silent face against the Q22 ceiling, Π̃ without an anchor (§8.1.1), the learned appraisal reactions, and subscription latency.
