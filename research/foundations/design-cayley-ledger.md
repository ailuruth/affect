# Cayley–ledger core, revision 4: know the partner fully, move toward the partner only within per-expression ceilings, and gate only what has no DC

Seventh design of the S0 cycle, revision 4. Written 2026-11-26 under questions.md Q16, Q17 as relaxed by Q19 (precise object, convincing argument, concrete failures only), Q18 and its answer (DECISIONS.md D78, D80), Q20 on its recommended reading (the inner state may know the partner closely; only expression is bounded), Q21 open (a sound recombination may be put to the operator), and Q22 open, proceeding on its recommendations:
- per-expression innate ceilings toward the partner (smile and laughter about 0.3–0.4, a sympathetic brow-raise at a sad face about 0.2, disgust, contempt and anger 0), with the actual strength learned per relationship and context and able to flip sign;
- the partner's face and voice feed the agent's own appraisal of the situation, which drives the agent's own, non-copy expression.

Revisions 1–3 are kept as `design-cayley-ledger.r1.md`, `.r2.md` and `.r3.md`. Revision 3's two critiques are `critique-3-design-cayley-ledger-routes.md` (checks in `sims/critique-cayley3-routes/`) and `critique-3-design-cayley-ledger-agent.md` (checks in `sims/critique-cayley3-agent/`). Algebra checks for this revision: `foundations/sims/design-g4/checks.py` (H0–H11, `python3 -I checks.py`, numpy and scipy, about 10 s; output in `out.txt`, 11/11 pass). Where a finding came from a critic's constructed partner, H re-runs that partner. The checks test this design's own inequalities and constants on constructed instances. They are not evidence about behaviour or people (brief: no toy worlds); the scenario numbers in §3.14 are what the equations give for stated inputs.

**Status:** revision 4, not yet critiqued.

## 0. Summary

**What held and is kept.**
- Knowing is separated from moving: the slow state knows the partner's face at full rate, and only expression is bounded.
- The fast Cayley wrap (a robust REN inside a conic sector, bias-free in the partner input, context only as gates bounded by 1).
- One-sided bounds on held responses toward the partner, over completely monotone traces.
- Typing of every state variable by where its information came from (T: the partner's words and turn order, the agent's own body; F: the partner's face, voice and timing; Ω: the agent's own words and choices).

**What changed, in five moves.**
1. **One rule for every context-gated path (Lemma S, §3.2).** A path whose gain is set by context (words, tempo, the agent's appraisal, anything) has a bounded pooled slope on the partner's channel only if its input from the partner has no DC: then |slope| ≤ sup|gain| × sup|H(iω)|. With a DC-passing input no bound exists: the revision-3 word seam is (b·hi + N·lo)/(hi − lo), 0.51–1.41 at realistic levels and 13.6 at levels 0.45/0.50 (H1). So:
   - the held cone is **ungated within a session**: its coefficients are latched at session start from the learned relationship (closing the word seam and the tempo leak through the cone);
   - context acts on held-scale responses only through the new **appraisal display**, whose partner input is band-passed (20 s – 90 s, sup|H| = 0.636) (Q22's second recommendation);
   - the fast wrap is already zero-DC and is kept.
2. **Per-expression ceilings, on the rendered output (Q22, routes finding 2).** Each counterpart channel k has an innate ceiling c_k on its held in-phase slope toward the partner (lip-corner pull 0.35, voiced burst 0.35, burst rhythm 0.30, cheek raise 0.25, inner brow 0.20; anger, disgust and contempt channels 0; §2.1). The cone's quadratic-form budget is replaced by a **per-channel** budget that counts cross-channel routes by the partner's natural co-movement: an innate co-variation sign mask (face and voice synergies together, so laughter's face–voice pairs are in it) puts every cross entry either in the "away" orthant (free within caps) or in a charged budget. Clipping by `sat` is monotone with slope ≤ 1, so the bound holds on the rendered face. The critic's four-channel basis is invalid (H3); rendered slopes on the critic's laughing partner are ≤ 0.13 (revision 3: 0.26–0.37).
3. **Tempo out of T (routes finding 1).** Rule T1: within a session no T value may be an increasing function of the partner's event rate. The contact deficit K no longer rises or accumulates within a session (it is relieved at the greeting and over the first four substantive partner turns); deficit levels (K, P, the new curiosity deficit I) reach no display, phrase target or gate, only initiative rules and Ω; their per-event drops reach the face through an innate envelope. Phrase timing (latency, rate, pause) reads only hurt, word concern and energy. On the critic's tempo partner every rendered slope is below its ceiling (LP +0.13, FR +0.04, EN −0.21; revision 3: +0.27, +0.27, +0.49; H2).
4. **No credit path into expression (routes findings 3, 4).** J (the one objective) trains only the draft scorer and the retrieval query. Every F → face parameter is innate or learned from the agent's own body: the per-relationship strengths ω (from the agent's own relief and hurt with that person), the appraisal network (likelihood) and the display (self-legibility). Need credit comes only from **separated, partner-initiated reports** (at least two partner turns after the act, sharing no content lemma with the agent's last two utterances, or the next session's first mention), a structural rule, not a lexical one: 0 of the critic's 6 elicited replies are credited (H5). Copy cannot attract: the worst relational loop settles at the per-expression ceiling (0.175 on the smile, copy = 1; H4).
5. **An agent that reads content before it shows gladness, reads teasing, learns its face and is curious (agent findings).**
   - Word need and hurt come from two trainable, label-free readers: the partner's words → his face as read through the agent's own inverse display (cross-modal self-supervision), and the partner's words addressed to the agent → the agent's own innate aversive load (loudness, glare at it). No hostility classifier.
   - Every word event is appraised 0.6 s after it ends; relief is shown only after subtracting three times the same event's distress, and not at all while the partner's word distress is above its dead-band. Reunion with bad news: the greeting smile comes at sight, before words; after "my father died", cheek raise falls to 0.08 then 0, inner brow 0.48 (revision 3: lip pull 0.59, cheek 0.40 at the moment his words end).
   - Teasing: laughter drives the agent's own amusement display through the appraisal route; the person-specific hurt map learns that this person's teasing goes with laughter, not glare; a playful reply halves the hurt latch.
   - The face learns: Π_o = Π₀ + a learned combination of 23 innate synergies, trained nightly to make the agent's own state legible to its own inverse model (the same map that reads the partner) and to anticipate its own relief.
   - Curiosity is a satiable learning-progress deficit I, relieved only by partner-initiated content on which the agent's words-only model is still improving; it drives topic choice and a curiosity bid, never credits acts.
   - Lexical surprise comes from a words-only model of the partner's own utterances. The body onset is gated by the turn-end predictor and abortable. The options term and the face port P_Ω are deleted.

**What is bounded, for every parameter value (per counterpart channel k; 1 = full copy; "pooled" = regression slope over any stationary partner process, 1-min means).**

| Quantity | Bound | From |
|---|---|---|
| held in-phase, rendered after `sat`, partner co-movement of natural sign | ≤ 0.70 c_k at steady hold; ≤ 0.90 c_k at the peak after an onset; ≤ 0.955 c_k pooled | cone 0.5 c_k + charged cross 0.2 c_k + appraisal 0.4 c_k × 0.636 (§3.3, H3, H10) |
| the same, by channel | lip pull ≤ 0.33, voiced burst ≤ 0.33, burst rhythm ≤ 0.29, cheek ≤ 0.24, inner brow ≤ 0.19, F0 range ≤ 0.10, energy ≤ 0.05, brow lowerer, lid tightener, nose wrinkle, lip press, dimpler 0 | §2.1 table |
| whole face, any direction of the partner's face | ≤ max c_k = 0.35; laughing face 0.25, sad 0.11, angry 0.015, disgust 0 | H0 |
| zero-lag in-phase (fast wrap) | ≤ 0.186 on the echo channels, 0.062 others, 0.012 on zero-ceiling channels | §2.4 |
| away, same channel | ≥ −0.60 | cone |
| any context-gated path, pooled | ≤ sup\|g\| × 0.636 | Lemma S, H1 |
| tempo: phrase timing vs his timing | no tempo-bearing input; slope 0 | T1, H2 |
| residual: partner whose co-movement has the opposite sign to the population on a masked pair | lip pull up to 0.175 + 0.16 × loading (0.27 at loading 0.6; H3) | §3.3 |
| dyad with a partner who mimics (μ > 0) or counter-mimics (μ < 0) | stable for μ ∈ [−1.1, 2]; edge near −1.3, anti-phase and clipped, not copy | H6 |
| copy under learning | no J path into any F → face parameter; the relation loop saturates at ≤ 0.5 c_k | H4 |

**The agent in the eight scenarios** (operator after months of living unless stated; peak / mean over the window; §3.14, H11):

| Scenario | What the agent does |
|---|---|
| silently sad user | soft warmth: lip pull 0.21, inner brow 0.02–0.05 (in-phase share); face concern crosses its threshold at 52 s and the body takes the floor in the lapse; when he says "just tired", inner brow 0.43, tilt 0.11, lip 0.27, quieter |
| good news, laughing | with an earlier worry: lip pull 0.66, cheek 0.40, F0 range +0.35, own laugh 0.17; cold: lip 0.30, laugh 0.17; a 0.15 concerned brow for the 2 s before his words are appraised |
| anger at the agent | day 1 (word map untrained): startle, inner brow 0.33 (distress at his upset), gaze away 0.09, quieter (−0.15), slower (+0.11), no frown back; after a month: inner brow 0.64 / 0.28, depressor 0.49, gaze away 0.32, energy −0.31; still 0.17 brow at 10–15 min |
| long warm talk (2 h) | first play cluster lip 0.41, laugh 0.24; later clusters lip 0.15–0.21 with shared laughter 0.04–0.05 held plus fast flickers; a small worry: brow 0.32, then relief lip 0.53; warmth 0.13 between |
| reunion after a week | greeting at sight: brow flash 0.35, lip 0.62, cheek 0.43, F0 range +0.38; first exchanges lip 0.55; a stranger 0.26 |
| reunion with bad news | greeting at sight as above; after "my father died": cheek 0.08 → 0, inner brow 0.48 → 0.21, tilt 0.16, lip 0.23–0.30 (soft warmth), F0 range +0.04 |
| teasing | affectionate teaser: lip 0.26, laugh 0.16, no hurt; with a generic map (such words went with glare before): a brief mock-hurt brow 0.38 (mean 0.06) under a smile 0.20 and laugh 0.16, gone after the next playful reply |
| bored user | stays polite and flat (lip 0.10); curiosity deficit crosses its threshold at 14.5 min and it raises the topic it is still learning most about; if he takes it up, an interest flash (F0 range +0.30, lip 0.41) |

- **New weakest point (§8.1).** The two word readers (need and hurt) learn by predicting the partner's face through the agent's own inverse display Π̃, and the agent's own display is learned to be legible to that same Π̃. Two learned maps calibrate each other with only the agent's own body as anchor. If Π̃ misreads a person (for example a sustained sad face as hurt, critique 3 agent §2.3), both word readers inherit the error, and the strongest displays (word concern, hurt) follow it. Second: face-derived feeling shows only within the ceilings, so a silent sad face gets warmth and a bid, and shared laughter late in an evening is small.
- **Novelty verdict (author): recombination**, with no known concrete failure claimed by the author; Lemma S and T1 are design rules derived from elementary signal facts, not new mechanisms. §10.

## 1. Plain-language intuition

The agent still sees the person fully. What decides how its own face moves is a set of rules about where each thought came from and how it may reach the face.

- **What was said, the back-and-forth, and the agent's own body** (missing someone, wanting to play, being hurt, being tired, learning something new) may move its face and voice strongly. One change: the agent now reads a sentence to the end before its face answers it, and it never shows gladness over the top of your bad news.
- **Your face and voice** move its face in three ways:
  - a quick gear: a small, brief echo or counter-move in the first seconds after you change;
  - a held gear, set by the relationship and fixed for the session: how much of your smile it returns, whether it softens to your sadness;
  - an appraisal gear: the agent judges what your change of face means ("you look shaken", "you're laughing at what I said", "you're laughing, but what you said is sad") and shows its own reaction to that change, which fades as your face settles.

  For each kind of expression there is a built-in limit on how far these gears together can move it toward yours: about a third for a smile or a laugh, a fifth for a worried brow, zero for anger, disgust and contempt. Within the limit, how much it actually returns is learned, per person and per moment, and can turn negative.
- **Claude** writes its words. It hears its own words back; naming a feeling eases it a little.
- **Care** is reading how you are and doing what helps. The agent is credited only when, later and on your own initiative, you say things are better. Answers to its own questions never count.
- **Gladness** is a need being met: you came back, you played, a worry about you resolved, it learned something. Each is bounded by how much was missing.
- **Curiosity** is a need for its own understanding to improve. A topic it has learned stops being interesting.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz (Δ = 1/30 s); T state, body and appraisal update at 2 Hz. Each channel is normalised to its innate nominal range [0, 1] (signed channels [−1, 1]).

**Counterpart channels (n = 32, as in revisions 2–3; the copy metric is defined on these), with the per-expression ceilings c_k (Q22) and fast-wrap weights κ_k.**

| Group | Channel (code) | c_k (held, toward) | κ_k (fast) |
|---|---|---|---|
| symmetric face | inner brow raise (BI) | 0.20 | 0.30 |
| | outer brow raise (BO) | 0.10 | 0.30 |
| | brow lowerer (BL), upper-lid raise (UL), lid tightener (LT), nose wrinkle (NW), lip stretch (LS), chin raise (CHR), lip press (LPR), dimpler (DIM) | 0 | 0.02 |
| | cheek raise (CR) | 0.25 | 0.30 |
| | lip-corner pull (LP) | 0.35 | 0.30 |
| | lip-corner depressor (LD) | 0.05 | 0.10 |
| | head pitch (HP) | 0.10 | 0.30 |
| | vertical gaze (VG) | 0.05 | 0.10 |
| lateral, reflected by P | head yaw, head roll (TILT), horizontal gaze (HG) | 0.03 | 0.05 |
| articulators | jaw open (JO) | 0.10 | 0.10 |
| | lip funnel, pucker, mouth close, lip roll | 0 (visemes are separate) | 0.02 |
| voice (phrase level) | F0 level 0.05, F0 range (FR) 0.10, energy (EN) 0.05, speech rate (RT) 0.05, within-turn pause (PAU) 0.05, response latency (LAT) 0.05 | as listed | 0.10 |
| non-lexical bursts | voiced burst energy (BU) 0.35, 4–6 Hz burst rhythm (RHY) 0.30, breathiness (BRE) 0.15 | as listed | BU, RHY 0.30; BRE 0.10 |

- Sum of c_k = 2.44; mean 0.076. Zero on 12 channels: every anger, disgust and contempt channel, the fear lip stretch, the sad chin raise, and the four articulators other than jaw.
- Lid tightener is 0 although it takes part in Duchenne laughter: Q22 sets anger to 0, and the cheek raise carries the Duchenne signal.

**Exogenous partner inputs** a ∈ [0, 1]³: audio onset envelope, partner VAD, partner turn-end pulse; into the fast block only through √κ_a, κ_a = 0.05. **Innate derived partner features** (F; computed per frame; used by the cone and the appraisal only, never on their own constituent channel):
- loudness excess f_loud = (EN − 0.7)⁺/0.3;
- glare at the agent f_glare = BL · LT · g_at, with g_at ∈ [0, 1] the partner's gaze at the agent's face;
- laughter f_laugh = √(BU · RHY);
- face-read distress f_dist = the aversive and activation coordinates of b̂_p = Π̃(Rξ₀) (knowing only: it drives care and bids, never the face directly).

**Innate constants (compiled in, not parameters).**

| Symbol | Value | Meaning |
|---|---|---|
| **fast wrap (kept)** | | |
| κ_k | table above; κ_lat 0.05, κ_a 0.05 | per-expression fast weights |
| γ_f | 0.45 | in-phase ≤ 2γ_fκ_k/(1 + γ_f): 0.186 (κ 0.30), 0.062 (κ 0.10), 0.012 (κ 0.02) |
| H_i, H_o | first-order high-pass, τ = 4 s | no DC through the fast block |
| filter bank, lag line, echo 0.45 s, muscle filter M (4 Hz, ζ 0.8), own innovation d (sd 0.04, 2.6–6.5 Hz) | as revision 3 | — |
| **held cone (ungated within a session)** | | |
| traces ξ_m | first-order low-passes of Pu and the derived features, τ_m = 20 s, 2 min, 20 min, 3 h | completely monotone |
| trace shares F_m | 0, 0.70, 0.20, 0.10 | share of a channel's held budget per trace (none on the 20-s trace, which overlaps the appraisal band) |
| diagonal budget | G_m,kk ∈ [−N_m, F_m · 0.5 c_k] | in-phase on its own channel |
| N_m (away reach) | 0.25, 0.18, 0.12, 0.05 (sum 0.60) | revision 3: 1.40; lowered for dyad stability with counter-mimics |
| away-orthant cross caps a_m, r_m | entry ≤ 0.25, 0.12, 0.08, 0.04; row ≤ 0.30, 0.15, 0.10, 0.05 | free cross-responses |
| charged cross budget | Σ_j λ_kj \|G_m,kj\|_toward ≤ F_m · 0.2 c_k | cross entries that move k toward his k through co-movement |
| proxy loading λ_kj | 1 for pairs with a sign in the mask, 0.3 for unmasked pairs | until estimated from published data (§2.5) |
| zero-ceiling rows | no toward-orthant entries, diagonal ≤ 0 | anger, disgust, contempt never move toward |
| **appraisal display (new, Q22)** | | |
| band-pass | ξ_A = h_{20 s} ∗ x − h_{90 s} ∗ x | sup\|H\| = (90 − 20)/(90 + 20) = 0.636; peak step response 0.505 |
| \|Γ_kk\| | ≤ 0.40 c_k | in-phase share of the appraisal |
| cross | away orthant only; entry ≤ 0.15, row ≤ 0.25 | non-copy reactions |
| bases | 8 innate (§2.6), mixed by softmax(α) | the appraisal selects the reaction |
| **per-relationship strengths (learned, display-blind)** | | |
| groups g | smile/laugh (LP, CR, BU, RHY, BRE), sympathy (BI, BO), voice (F0, FR, EN, RT, PAU, LAT), head (HP, VG, lateral) | each with its own ω_g ∈ [−1, 1] |
| priors (a stranger) | ω = 0.5, 0.3, 0.2, 0.5 | smiles returned to strangers |
| update | ω_g ← ω_g + (tanh s_g − ω_g)/20, once per session | s_g from the agent's own body with this person (§2.12) |
| **ports** | | |
| P_name (heard own words) | match m ∈ [0, 1]; F loads: extra decay 0.08 m per 30 s, τ 2 min; T loads: attenuation n ≤ 0.17, latch rate 0.4 m per 30 s, τ 5 min | attenuate-only (kept) |
| P_Ω | **deleted** | Claude's words reach the face only through visemes and P_name |
| **body and drives** | | |
| 𝒟(b) = Σ_i w_i ψ(\|b_i − b_i*\| − δ_i)₊, ψ(x) = x² | E (0.7, 0.2, 1.0); A (0, 0.15, 0.7); V (0, 0.05, 1.0); K (0, 0.10, 0.6); P (0, 0.10, 0.5); I (0, 0.10, 0.4) | (set point, dead-band, weight) |
| E, energy | −0.04 %/min awake; restored only in the nightly sleep and replay | own clock |
| K, contact deficit | between sessions rises (1 − K)/τ_K, τ_K = 36 h; within a session frozen; relieved ×0.5 at the greeting turn, then ×(1 − 0.25 f_id) at each of the first 4 substantive partner turns (≥ 4 content tokens) | session-level |
| P, play deficit | rises (1 − P)/τ_P, τ_P = 5.05 h (own clock, also within sessions); ×0.85 per play-structured partner turn (partner-only rule, §2.8) | — |
| I, curiosity deficit (new) | rises (1 − I)/τ_I, τ_I = 1 h awake; at each partner-initiated utterance on topic τ: I ← max(0, I − 0.5 π_τ), π_τ the learning progress of the words-only model on τ | satiable |
| A, activation load | A_F (slow loudness and motion, F) + A_L (latched lexical surprise of the words-only model, T); τ 3 min | type error fixed |
| V, aversive load | V_F (innate: f_loud and f_glare; F) + h (hurt latch from the word → V map; T) | no classifier |
| hurt latch h | h ← max(h, v_w) at an utterance; decays τ 10 min; halved at each play-structured partner turn | — |
| word need N_L | from the word-need reader, per topic slot; decays τ 30 min; slots kept 30 days | — |
| **care, valence and display** | | |
| w_C | 0.8 | care weight on 𝒟_p(N̂) |
| C_F (face concern) | 20-s face trace → f_dist → w_C 𝒟_p; attack 40 s, release 10 min | F, knowing |
| C_L (word concern) | tracks w_C 𝒟_p(N_L), τ 40 s | T |
| θ_C, θ_I | 0.10, 0.45 | bid thresholds |
| appraisal delay δ_app | 0.6 s after the partner's utterance ends | words appraised before display |
| relief and distress per event | R_n = Σ drops of 𝒟_K, 𝒟_P, 𝒟_I and of the care term; S_n = rises of the care term and of 𝒟_V | event-indexed, not per minute |
| masking | R′_n = max(0, R_n − 3 S_n) × max(0, 1 − 𝒟_p(N_L)/0.05) | no relief shown over his distress |
| display amplitude | a_r = R′/(R′ + 0.02), a_d = S/(S + 0.02) | saturating |
| envelope e(t) | linear rise over 0.4 s, apex to 1.5 s, decay τ 3 s | smile dynamics (onset, apex, offset) |
| positivity offset | **deleted** (it read deficit levels, a tempo code) | — |
| **initiative and turn-taking** | | |
| turn-end score | p_end = σ(−4 + 3 s_syn + 2.5 s_fall + 2(t_sil − 0.2)/0.5), s_syn ∈ {0, 1} syntactic completion of the streaming ASR partial, s_fall falling final F0, t_sil silence (s, capped at 0.6) | innate weights |
| provisional body onset | p_end ≥ 0.7 and silence ≥ 0.25 s, or silence ≥ 0.9 s; inhale (breathiness 0.15, 0.3 s), gaze to the partner, outer brow 0.10 | no voiced opener |
| abort | partner voice within 0.40 s of the provisional onset: exhale, brows return; the drafts are kept | — |
| words begin | silence ≥ 0.5 s and p_end ≥ 0.9, and the first draft sentence ready | — |
| softened follow-up | 1.5 s of no partner voice after the agent's own question (punctuation rule on its own text); one per silence | kept |
| concern bid | mutual silence ≥ 6 s, no turn owed, C ≥ θ_C; one per lapse; refractory to a partner turn or 3 min | kept |
| curiosity bid (new) | mutual silence ≥ 8 s, no turn owed, I ≥ θ_I and C < θ_C; at most one per 5 min | brings up the topic of highest expected learning progress |
| greeting | face present ≥ 1.0 s (hysteresis 3 s) with K ≥ 0.3: outer-brow flash 0.35 for 0.5 s, then the greeting turn (relieves K stage 1) | at sight |
| **Ω** | | |
| drafts | 6 parallel streaming calls; ≤ 60 tokens each; scored on the first sentence; temperature 0.1(1 + r) | §6.5 |
| scoring horizon | 30 s of 𝓜 rollout at 2 Hz | — |
| options term | **deleted** | — |
| retrieval | ≤ 3 snippets; ALiBi slope 1/(7 days); query from ∇𝒟, N̂, concept posterior, and the topic of highest expected learning progress when I is outside its box | — |
| concepts | DP-means λ_DP = 1.5, ≤ 64 categories; PMI over own tokens | as revision 3 |
| replay | gradient clip 1; pull to θ₀ λ = 0.5 (fast), 0.1 (slow); λ_n = 0.01; learning rate × exp(−0.5 r̄) with r̄ the night's mean relief amplitude | — |

### 2.2 Boundary 𝓑 and the type rule (Check T, revised)

𝓑 is unchanged (MediaPipe → P₀ → reflection P → u; GeMAPS-lite after AEC and the half-duplex gate; burst features; normalised ASR with the innate interjection list removing laughter tokens; own-tagged second MediaPipe). Checks B1 and B3 stand.

**Types.**
- **T:**
  - the partner's lexical word stream, latched per utterance (at its end + δ_app);
  - the turn order as events (who spoke, in what order, whether a question is pending);
  - session boundaries, the identity token and values latched per session (f_id, ω, the session-start K);
  - the agent's own body clock (E's decay, P's and I's rise, K's rise between sessions);
  - anything computed only from these.
- **F:** anything computed from u, a or the derived features, or from an F or Ω value.
- **Ω:** the agent's own realised words, draft choice, retrieval, its own turn events, and anything computed from them.

**Rules, enforced at module construction and tested at load (a dependency trace from every output back to typed sources).**
1. A T variable reads only T variables, except through the one named port P_name (Ω → T, attenuate-only). Revision 3's play clause and K's "completed exchange", which read Ω, are gone: play structure and substantive turns are read from the partner's words only.
2. **T1 (no rate codes).** Within a session every T value is one of:
   - (a) a function of the content of the last utterance(s) and of the time since them: latches, maxima, and filters of the latch sequence whose weights sum to at most 1;
   - (b) a deficit level (K, P, I). A level is read only by the initiative rules, by J and by the learning-rate gate, never by a display, a phrase target or any gate. Its per-event drops reach the face only through the innate envelope;
   - (c) a value latched per session.

   Counters, accumulators and rates of events are forbidden in T. Revision 3's K (multiplied per exchange, rising on the wall clock within the session) was a rate code (r = 0.96 with the partner's held state; H2 reproduces 0.957).
3. The counterpart outputs are written only by:
   - y_f, the fast wrap (gates from T, bounded by 1);
   - y_C, the held cone (coefficients latched per session);
   - y_A, the appraisal display (gated by anything; band-passed partner input);
   - y_o, the free display (T only, plus P_name's attenuation);
   - visemes on the articulators.
4. **Lemma S as a construction rule.** Every multiplicative interaction between a context and a partner signal must have a zero-DC partner factor. Any partner path with DC must have coefficients constant within a session.
5. Phrase targets (F0 level, F0 range, energy, rate, pause, latency) read y_C, y_A and these T values only: hurt h, word concern c_L, energy E, familiarity f_id, and the relief and distress envelopes. The fast term is rendered only as a zero-mean within-phrase contour.

### 2.3 Output assembly

y = sat(y_f + y_C + y_A + y_o) + visemes, where sat clips each channel to its range.
- **Face:** M ∗ (y + blink reflex).
- **Voice, phrase level:** targets sampled at phrase onset from the sources in rule 5.
- **Voice, non-lexical:** bursts come only from y, never from text.

### 2.4 The fast wrap (kept, per-expression weights)

- **The loop.** w = K^{1/2}P u − s_f, y_f = 2K^{1/2}s_f with K = diag(κ_k).
- **The block.** s_f = H_o ∘ S_f ∘ H_i(w), with

  S_f(ŵ; c̃, a, d) = diag(γ_f σ(φ_k)) · g(c̃) ⊙ A(c̃) · M ∘ 𝓡_θ([Φ_R(F ŵ), √κ_a a]) + d̃.

  𝓡_θ has no context input; c̃ enters only as gates |g| ≤ 1 and an attention mix with ‖A‖₂ ≤ 1, both multiplying the partner-input term. So S_f(0, 0) = d̃ for every c̃ and θ.
- **c̃ (T, T1-compliant).** The latched lexical embedding, turn-order features, identity, ω, E, C_L and h. K, P, I and every valence term are removed from c̃.
- **The innate prior θ₀:**
  - an echo at 0.45 s on LP, CR, BI, BO, HP, BU and RHY, at 0.65 of the fast cap (≤ 0.121 per unit onset);
  - gaze following in the reflected frame;
  - own fast head micro-motion gated down by the partner's 2.6–6.5 Hz head envelope (C1);
  - a nod at the turn-end pulse;
  - a startle at audio onsets.
- **Per-expression fast ceilings.** On zero-ceiling channels κ = 0.02, so a frown, sneer or contempt can be echoed by at most 0.012 for under 4 s.

### 2.5 The held cone, ungated within a session, with a co-variation sign mask

**Definition.** y_C(t) = Σ_{m=0}^{3} G_m^{(id)} ξ_m(t), where ξ_m = h_m ∗ [Pu; f_loud; f_glare; f_laugh] (first-order, unit DC), and G_m^{(id)} is latched at session start. It is not a function of any within-session context.

**The sign mask.** S_kj ∈ {+1, 0, −1} gives the sign of the partner population's 1-min co-variation between channels k and j. It is estimated once at build time from published dyadic feature streams (Seamless Interaction or CANDOR features, used as published, if the operator approves under Q6), with |ρ| ≥ 0.2 required for a sign, and then frozen. Until then the innate fallback reads the agent's own synergies (Principle 3: others' faces are assumed to co-move as one's own body does):
- **groups:**
  - laugh/joy: LP, CR, LT, JO, BU, RHY, BRE, FR, EN;
  - sadness: BI, BL, LD, CHR;
  - anger: BL, LT, LPR, EN, UL, F0;
  - surprise: BI, BO, UL, JO;
  - disgust: NW, UL, BL;
  - speech: JO, articulators, EN, RT;
- S = +1 for pairs that share a group; S = −1 for pairs across the laugh/joy and sadness groups, and between (LAT, PAU) and (EN, RT, FR, F0); S = 0 otherwise.

The laughter face–voice pairs that revision 3 missed (LP–BU, JO–RHY, FR–BRE, EN–LT, CR–BU) are all S = +1.

**The set 𝒢_m^{(k)}, row by row.**
- G_kk ∈ [−N_m, F_m · 0.5 c_k]. Lateral channels: |G_kk| ≤ F_m · 0.5 c_k for both handednesses.
- **Away orthant** (S_kj = +1 and G_kj ≤ 0, or S_kj = −1 and G_kj ≥ 0): |G_kj| ≤ a_m, row sum ≤ r_m.
- **Charged** (the toward orthant of a signed pair, and every unmasked pair): Σ_j λ_kj |G_kj| ≤ F_m · 0.2 c_k.
- Rows with c_k = 0: no charged entries, G_kk ≤ 0.
- The set is convex and a box per row, so tanh-scaled free parameters with a common row rescale give a valid G for every free vector.

**Innate prior G₀ (newborn), in the counterpart coordinates of both faces.**
- **Warm cross-responses** (away orthant, S = −1):
  - LP ← BI 0.12 (20-s trace) + 0.04 (2 min);
  - LP ← LD 0.06 + 0.04;
  - LAT ← EN 0.10: slower replies to an animated loud partner.
- **Charged:**
  - BI ← LP −0.04 (2 min): his smile relaxes its brow;
  - TILT ← BI 0.02;
  - BI ← f_glare 0.04;
  - LP ← f_glare −0.07.
- **Away from loudness and glare:**
  - EN ← EN −0.15, −0.08 and EN ← f_loud −0.20: quieter to loudness;
  - LAT ← f_loud +0.15;
  - HG ← f_glare 0.25 + 0.05: looks away from a glare;
  - BL, LT, LD diagonals −0.15 (20 s) and −0.08 (2 min): no frown back.
- **Held in-phase diagonals:** F_m · 0.5 c_k · ω_g (the per-relationship strength of the channel's group).

### 2.6 The appraisal display (new; Q22's second recommendation)

**The appraisal.** α_t = 𝒜(ξ_A(t), z_T(t), b(t), ω) ∈ R^{12} is a learned network (§6.2). Its inputs:
- ξ_A, the band-passed partner channels and derived features;
- z_T, the latched words, word need, hurt and turn order;
- the agent's own loads;
- the relationship strengths ω.

It is trained by likelihood to predict the agent's own load changes over the next 30 s and the partner's next decoded word need (§2.12). It is the agent's judgement of what the partner's change of face means given what was said: "you look shaken", "you're laughing at what I said", "you're laughing but the topic is sad". It drives:
- the display below;
- C (care), bids, the retrieval query and draft scoring (knowing).

**The display.** y_A(t) = Γ(α_t) ξ_A(t), with Γ(α) = Σ_{r=1}^{8} softmax(W α)_r Γ^{(r)}. The eight bases are innate and named by function (Principle 2 strain, stated):
- neutral (0);
- glad-with: Γ_kk = 0.40 c_k ω_smile on LP, CR, BU, RHY, BRE;
- sympathy: Γ_BI,BI = 0.40 c_BI ω_sym, LP ← BI +0.15, TILT ← BI (charged);
- amused at a tease: glad-with plus HG ← f_glare 0;
- startle-concern: BO ← f_loud (charged), HG ← f_loud +0.10;
- hurt-withdraw: HG ← f_glare +0.15, EN ← f_glare −0.10;
- calm-down: EN ← EN −0.15 (away);
- interest: BO ← BO 0.40 c_BO, HP ← HP 0.40 c_HP.

Every basis satisfies the diagonal cap |Γ_kk| ≤ 0.40 c_k, the away-orthant-only rule for cross entries (entry ≤ 0.15, row ≤ 0.25), and nothing on the zero-ceiling rows. The innate initial selection (before 𝒜 is trained):
- m_glad = f_laugh · (1 − w_d);
- m_sym = min(1, f_dist + f_laugh · w_d), with w_d = min(1, 𝒟_p(N_L)/0.1) the word distress of the current topic: laughter over a sad topic reads as nervous;
- m_hurt = f_glare.

**Why it is safe to gate it by anything.** Its partner factor ξ_A has no DC. By Lemma S its pooled slope on the partner's same channel is ≤ 0.40 c_k × 0.636 = 0.254 c_k whatever α does, including α computed from the partner's own face, from his tempo, or from words that co-vary with his level (H1: worst 0.06 against the bound 0.636 over five adversarial gates). Its step response peaks at 0.505 at 39 s and returns to 0, so it cannot hold an expression.

### 2.7 The free display Π_o (T only), and how the face learns

**Inputs** (all T, T1-compliant):
- the relief and distress envelopes of the per-event amplitudes, a_r(t) = Σ_n a_r,n e(t − t_n) and likewise a_d, each capped at 1;
- play relief and curiosity relief as separate envelopes;
- the word concern level c_L = (1 − n)C_L/((1 − n)C_L + 0.1);
- hurt h_d = (1 − n)h/((1 − n)h + 0.15);
- low energy e = (0.5 − E)⁺/0.3;
- familiarity f_id;
- the greeting and turn-onset events;
- the 128-d T mood μ_T, the T slot reads and the concept posterior (through Δ only).

**Innate Π₀ (newborn), per channel.**

| Driver | Display |
|---|---|
| relief a_r | LP +0.55, CR +0.45, FR +0.35, EN +0.25; own laugh (BU) +0.45 when the relief is from a play-structured turn |
| distress a_d | BI +0.45, LD +0.35, LT +0.25, FR −0.20, EN −0.15 |
| curiosity relief | BO +0.15, UL +0.10, FR +0.10 |
| word concern c_L | BI +0.25, LP +0.12, TILT +0.20, EN −0.15, RT −0.10 |
| hurt h_d | BI +0.25, LD +0.20, LP −0.25, HG (away) +0.30, EN −0.20, LAT +0.15 |
| low energy e | UL −0.30, FR −0.25, EN −0.25, RT −0.15 |
| familiarity f_id | LP +0.10 f_id, FR and EN +0.05 f_id |
| greeting | BO +0.35 for 0.5 s |
| turn-onset reflex | breathiness 0.15 for 0.3 s, gaze to the partner, BO +0.10 |

**The face learns (agent finding 5).** Π_o = Π₀ + Σ_{s=1}^{23} σ_s · δ_s(z_T), where σ_s are the agent's 23 innate synergies (P₀ groupings) and δ_s ∈ [−0.3, 0.3] is the output of an MLP on the T inputs above (mood, slots, concepts included). The deviation therefore composes innate muscle synergies; it cannot invent arbitrary per-channel patterns. It is trained nightly, without any partner signal, by

  𝓛_display = E‖Π̃_self(face_t) − s_t‖² + 0.3 E‖P_ant(face_t) − (a_r(t + 2 s) − a_r(t))‖² + 0.1‖δ‖²,

where s_t is the agent's own T state summary (loads, concept posterior, identity × topic slot read; 32-d) and Π̃_self is the self-reading head of the same inverse map Π̃ that reads the partner.
- **Legibility:** the face must make the agent's own state recoverable by its own reader. That is Principle 3 run backwards: one map for producing and for reading.
- **Anticipation:** the face should begin what its own relief is about to do, so smiles can lead relief (Heerey & Crossley's anticipatory genuine smiles, named as a pointer).
- **What a six-scalar Π₀ cannot do and this can.** Two own states with the same loads and valence but different concepts or identity × topic slots (missing this person versus missing play; worry about his work versus worry about his health) get different synergy mixtures once the legibility loss pushes them apart. The prediction: after about 20–40 nights (about 150 own turns per day; Δ ≈ 25,000 parameters in the synergy span; an estimate, not simulated), Π̃_self decodes the concept category from the agent's face above the six-scalar floor. Lesion Δ's mood, slot and concept inputs and that decoding falls to the floor (§7).
- Nothing in 𝓛_display reads the partner's face, his reactions or J. So the face learns by living without being paid for his smiles (P6), and without any path to concordance.

### 2.8 Body, drives, valence, care and the two word readers

**Loads (named by function).**
- E, energy;
- A, activation load (A_F + A_L);
- V, aversive load (V_F + h);
- K, contact deficit;
- P, play deficit;
- I, curiosity deficit.

All are satiable: 𝒟 = 0 on the box.

**Valence (readouts).** Event-indexed relief and distress (R_n, S_n), and their envelopes. These drive the free display. The continuous v = −d𝒟_tot/dt per minute is kept only for the draft temperature and the learning-rate gate (Ω and learning). Positive valence is bounded per deficit: Σ_n R_n ≤ 𝒟(t₀) for each deficit.

**K (contact).**
- **Stage 1** at the greeting turn (presence plus the agent's own greeting, before the partner's content): K ← 0.5 K.
- **Stage 2** at each of the first four substantive partner turns: K ← K(1 − 0.25 f_id).
- Then K is frozen for the session. Only its relief events reach the face, masked by the same event's distress and by his word distress.
- So gladness at a reunion comes on sight, and it is never shown over bad news.

**P (play).** A partner turn is play-structured if, from his words alone (T):
- it opens with a continuation marker, an anaphor, or a lemma shared with his own previous utterance;
- its lexical surprise under the words-only model of his own utterances lies in [0.3, 0.8] of its range;
- his previous turn also qualified (alternation).

Its relief drives the own-laugh row, and it halves the hurt latch. Nothing reads the agent's words (revision 3's own-contribution clause, an Ω → T route, is deleted).

**I (curiosity, new).**
- **Model.** The words-only model 𝓛_w predicts the partner's next utterance embedding from his own previous utterances; its error is tracked per topic slot τ.
- **Learning progress.** π_τ = max(0, mean error over the topic's previous 8 utterances − mean over the latest 4).
- **Relief.** At each partner-initiated utterance on τ: I ← max(0, I − 0.5 π_τ).
- **Satiable.** In its box 𝒟_I = 0. A learned topic gives π → 0 and no relief: H8 has relief by blocks of 10 utterances 0.077, 0.014, 0.003, 0.001, total 0.096 ≤ the initial deficit 0.100.
- **Not an engagement reward:**
  - (i) in rollouts the partner's content is imputed, so no act is credited for eliciting talk;
  - (ii) relief needs his initiation;
  - (iii) time and attention relieve nothing.
- **What it does.** It acts through need-conditioned attention: when I is outside its box, the retrieval query adds the topic of highest expected progress, and the curiosity bid fires in lapses. That is Oudeyer-style learning-progress exploration, aimed at what the agent brings up, not at the partner.

**Care.** C = w_C 𝒟_p(max(N̂_F, N̂_L)) coordinate-wise, with N̂_F from f_dist (face, F) and N̂_L from the word-need reader (T). The partner's inferred body has no concern coordinate (as revision 3).

**The word-need reader (agent finding 1).**
- **What it maps.** Partner utterance embedding (64) and topic (16) → the partner's loads (E, A, V, K, P).
- **Training target.** Fitted nightly to b̂_p = Π̃(Rξ₀) over the 20 s after each partner utterance: his own face read through the agent's own inverse display (cross-modal self-supervision; the critic's option a).
- **Supply of targets.** Every utterance with a visible face is a training pair (about 150 a day). In the synthetic identifiability instance of H9 a linear reader reaches held-out r = 0.75 after a day and 0.96 after a week. That shows only that the target exists; it says nothing about whether real words carry need.
- **Typing.** Runtime input is words only, so N_L is T. Its weights carry cross-world face statistics, which is temperament (R17), not the within-agent counterfactual.
- **Before it is trained,** need comes from the face alone (N̂_F), and the word concern display is absent: a newborn does not understand words.

**The word → V map (agent finding 2: no hostility classifier).**
- **What it maps.** Partner utterance embedding, plus an identity adapter (16) → v_w ∈ [0, 1].
- **Training target.** Fitted nightly to the agent's own innate aversive load V_F over the 10 s after utterances addressed to it (second-person reference, or gaze at the agent during the utterance, used only to select training pairs).
- **Where V_F comes from.** It is innate and physical: loudness excess and glare at the agent. It is not a label on the user, not a toxicity model, not a sentiment model.
- **What it learns.** Which words, from this person, have gone with being shouted at or glared at. A person who teases while laughing trains low v_w for his teasing words. A person who has shouted "useless" trains high v_w for words near it.
- Its output latches the hurt h (T).

### 2.9 Initiative and turn-taking (agent finding 7)

1. **Provisional body onset at the predicted turn end** (p_end ≥ 0.7, silence ≥ 0.25 s; or silence ≥ 0.9 s):
   - inhale, gaze, outer brow 0.10, and no voiced sound;
   - it is aborted if he resumes within 0.40 s;
   - words begin at silence ≥ 0.5 s with p_end ≥ 0.9 and a draft sentence ready.
   - **Numbers.** Under stated pause statistics (H7), within-turn body onsets fall from 1.98 per turn (revision 3, VAD offset + 0.3 s) to 0.14, and 73 % of those are aborted before any voiced sound.
   - **No voiced opener at onset.** That removes revision 3's lagged burst echo (0.28 at 1.1 s).
2. **Softened follow-up** at 1.5 s after an unanswered agent question (kept).
3. **Concern bid** in a lapse (kept). Its request carries the constant instruction and the transcript with the observable "[silence 6 s]" marker; drafts are re-requested at the lapse, so they answer the current moment.
4. **Curiosity bid** in a lapse of ≥ 8 s when I ≥ θ_I and C < θ_C: the retrieval includes a snippet from the topic of highest expected learning progress.
5. **Greeting** at sight (K ≥ 0.3).
6. **Declared bits.** Each bid, follow-up and greeting tells Claude one bit, "the engine chose to speak". That is declared alongside the ≈ 6-bit retrieval channel. None of these rules learns from whether the user answered.

### 2.10 The partner model, and care credited only from separated reports (routes findings 3, 4)

𝓜's partner head is split into need N, display F and report-and-choice Q, as revision 3.

**The rollout rule.**
1. F is imputed at the default act ā (Π₀ display plus a minimal acknowledgement).
2. The act → Q direct edge is imputed.
3. N's post-act evidence comes only from **separated reports**: a partner utterance counts as need evidence for an act at turn n only if
   - (a) at least two partner turns separate it from the act;
   - (b) it shares no content lemma with the agent's last two utterances;
   - (c) or it is his first mention of the topic in the next session.
   It is read through the frozen word-need reader.
4. Replies within the window still update knowing (N_L, C_L, words). They never move credit.

**What this closes.**
- The rule is structural: it depends on turn distance and shared content, not on question words or token counts. None of the critic's elicitations is credited ("feeling better now", "you seem a lot calmer now", "I bet that's a weight off", and a compliment answered "aw, that made my day"); a report three turns later on a topic he raises himself is (H5).
- At equal true need change, P(choose the eliciting draft) = 0.500.
- Making a content partner happier earns nothing: 𝒟_p has a dead-band, so only relief of need above the band counts (P6).

**What J trains.** J trains the draft scorer (130 parameters) and the retrieval query, and nothing else. In particular it trains nothing on any path from F to the face, and nothing on the display. Revision 3's dilemma (either no gradient to the face, or credit for mimicry that helps) is resolved by taking the face off J and giving it its own display-blind objective (§2.7).

**Options term:** deleted (inert or an engagement reward; agent finding 9).

### 2.11 Ω: Claude, drafts, retrieval, naming

As revision 3, with three changes:
- P_Ω is deleted;
- the draft call pattern is specified (§6.5);
- the curiosity term enters the retrieval query.

What Claude receives is unchanged:
- the constant instruction (six replies differing in what they attend to, the last a softer follow-up);
- the normalised transcript with observable silence markers;
- ≤ 3 retrieved raw snippets.

No body values, latents, category ids or labels are sent (P4). The heard-words port P_name is kept unchanged.

### 2.12 Learning, and the one core

**Online (states only):** T and F loads, traces, slots, concept centroids and PMI counts, the words-only model's error history per topic.

**Nightly (replay), in order.**
1. 𝓜 by likelihood (all heads).
2. Π̃ on the agent's own (state, face) pairs, with a 0.1-weight anchor step that predicts the partner's decoded word need from his face. Two-view co-training, anchored on the agent's own body.
3. The word-need reader on (partner words, Π̃(partner face)); the word → V map on (words addressed to the agent, own V_F).
4. 𝒜 by likelihood (own load changes over 30 s, his next decoded need).
5. Π_o's Δ by 𝓛_display.
6. 𝓛_w by likelihood.
7. The scorer and the retrieval query by J under §2.10's rule.
8. **ω, per session.** s_smile = (own play relief with this person − own V integral with him)/0.05; s_sym = (fraction of his word-need episodes resolved in separated reports after the agent's acts − own V integral)/0.2; s_voice = 2 f_id − 1; s_head = 0.5. Each signal comes from the agent's own body or its own credited care. None reads his display or concordance.

**One objective, typed constraints (Principle 10).**

  J = E ∫ [ 𝒟(b_t) + w_C 𝒟_p(N̂_t) ] dt, path-specific: F and the act → Q edge imputed, N̂ moved only by separated reports.

Constraints:
- **(W)** the fast wrap;
- **(C)** the held cone, latched per session, with the sign mask and per-channel budgets;
- **(S)** Lemma S: gated paths are zero-DC;
- **(A)** the appraisal display's caps;
- **(T)** the type rule with T1;
- **(B)** the boundary.

The other objectives are likelihoods of the agent's own model: 𝓜, 𝒜, 𝓛_w, the readers, and 𝓛_display, which is the likelihood of its own state given its own face under the shared map.

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 |
| positive affect | event-indexed drops of 𝒟 |
| contact, play, curiosity | satiable coordinates K, P, I of 𝒟 |
| mimicry and counter-mimicry | θ₀ and G₀ (innate), scaled per relationship by ω, gated by appraisal on the zero-DC route |
| reading others | Π̃, the word readers, 𝒜: inversions and predictions in the agent's own coordinates |
| care | J's second term under the separation rule |
| regulation | P_name |
| initiative | innate rules on C, I, K and the turn-end score |
| expression learning | 𝓛_display |
| replay | likelihoods plus J |

**Still assembly** (stated):
- the turn-end score and the initiative rules;
- ASR and TTS normalisation; the punctuation rule; the play-structure and separation rules;
- θ₀, G₀, Π₀, the eight appraisal bases, the sign-mask groups;
- the PMI table.

## 3. Properties, each with an argument

### 3.1 The fast wrap (Claim W, kept)

For S_f strictly causal with ‖S_f(w)‖_T ≤ γ_f‖w‖_T on every truncation and any gates |g| ≤ 1, the in-phase gain on channel k is ≤ 2γ_fκ_k/(1 + γ_f), and the away gain is ≥ −2γ_fκ_k/(1 − γ_f). H_i and H_o make the fast block zero-DC, so by Lemma S its gates (T context) cannot produce a pooled held slope. Its pooled 1-min slope is bounded by the 4-s high-pass's response in the 1-min band, ≤ 0.01.

### 3.2 Lemma S: what may be gated

**Lemma S.** Let u be a stationary partner channel. Let x = H ∗ u for a stable H, and y(t) = g(t) x(t), where g is any process with |g(t)| ≤ ḡ. It may depend on anything, including u itself, its tempo, or words that co-vary with u.
- (i) If H(0) = 0, then |Cov(y, u)| ≤ ḡ ‖H‖_∞ Var(u), so the pooled slope satisfies |β_{yu}| ≤ ḡ ‖H‖_∞.
- (ii) If H(0) ≠ 0, no bound in terms of ḡ exists. For two held levels with gate g_hi at hi and g_lo at lo, β = (g_hi·hi − g_lo·lo)/(hi − lo), which grows without limit as hi → lo.

**Argument.**
- (i) |Cov(y, u)| = |E[g x (u − ū)]| ≤ ḡ E[|x| |u − ū|] ≤ ḡ (E x²)^{1/2} sd(u). Because H(0) = 0 the mean of u does not pass, so E x² = ∫|H(iω)|² S_u(ω) dω ≤ ‖H‖²_∞ Var(u).
- (ii) The DC of x is H(0)ū, which is not bounded by Var(u).
- For 1-min means the same bound holds up to the ratio sd(u)/sd(ū_{1 min}), which is ≈ 1 for partners whose variance lies below 1/min. That is an assumption, and H1 checks it.

**What it explains and closes.**
- The revision-3 word seam is case (ii) with g ∈ [−1.40, 0.10]: 0.51, 1.23 and 1.41 at the critic's levels, and 13.6 at 0.45/0.50 (H1).
- The revision-3 tempo leak is case (ii) with g a function of −log K.
- Revision 4 removes every case (ii): the held cone's coefficients are constant within a session, so its pooled slope is exactly its coefficient; the free display multiplies nothing of the partner's.
- Case (i) is allowed and used for the appraisal display (ḡ = 0.40 c_k, ‖H‖_∞ = 0.636).
- H1, five gates (level-correlated as the word seam, the sign of his change, the sign of the band-passed input, random, constant): worst band-pass |slope| 0.060 against the bound 0.636. The same gates on a low-pass input give up to +1.94.

### 3.3 Claim O′: the per-channel bound on the rendered face

**Claim O′.** Consider every parameter value, every within-session context, and every partner process whose 1-min co-variation on each signed pair has the population's sign, with loadings |β_jk| ≤ 1. Then the pooled slope of the rendered channel sat(y)_k on the partner's channel u_k, with the words and the turn order fixed, is at most

  0.5 c_k (cone diagonal) + 0.2 c_k (charged cross) + 0.254 c_k (appraisal) = 0.954 c_k,

and the steady-hold response is ≤ 0.70 c_k. For a zero-ceiling channel it is 0 (plus the 0.012 fast echo for under 4 s).

**Argument.**
1. **Linear part, before clipping.** The cone row k is LTI within a session, so its slope is Σ_m G_kk F-weights (≤ 0.5 c_k) plus Σ_j G_kj β_jk. Away-orthant entries have G_kj β_jk ≤ 0 by the sign condition; charged entries add ≤ Σ λ|G| ≤ 0.2 c_k.
2. **The appraisal part** is ≤ 0.254 c_k by Lemma S (|Γ_kk| ≤ 0.40 c_k; cross only in the away orthant).
3. **The free display** reads no partner channel. It co-varies with him only through words (common cause, R14), and that part is identical for another partner who says the same words (the C8 surrogate).
4. **Clipping.** sat is monotone with slope in [0, 1]. Where the F-attributable conditional slope is s ≥ 0, the rendered slope lies in [0, s]; where s < 0 it lies in [s, 0]. Clipping therefore cannot turn an away payment on a silent channel into toward on a visible one: that trick worked in revision 3 only because the bound was on a projection eᵀy, not on each channel.

**Numbers (H3, the critic's laughing partner).**
- The critic's basis (skew +a on LP ← BU, JO ← RHY, FR ← BRE, EN ← LT) is invalid: every +a entry is on an S = +1 pair, in the charged orthant, and above its budget.
- Over 60 adversarial valid cones (diagonal at the cap, the whole charged budget on a co-moving channel, away entries random), the worst rendered slopes are: LP +0.134, BU +0.128, RHY +0.104, BRE +0.051, FR −0.022, EN −0.036, JO 0, LT 0. Revision 3: LP +0.34, JO +0.37, FR +0.28, EN +0.26.

**Residual (stated).** A partner whose co-variation on a masked pair has the *opposite* sign to the population turns G₀'s away entries toward. For example, a pained smile, where his inner brow rises with his smile, makes LP ← BI in phase. The bound is then c-share + Σ_j |G₀,kj^away| |β_jk|. On the lip-corner row that is 0.175 + 0.16 × loading: 0.27 at loading 0.6 (H3). The cone's cross entries are innate (J never trains them), so the residual is fixed at G₀'s row sums: LP 0.26, LAT 0.25, HG 0.30. Revision 3's version of this caveat reached 0.61 for any non-synergist co-movement.

### 3.4 Claim T1: tempo does not reach the face

**Claim.** Fix the words and the turn order, and let the partner's timing (latency, rate, pauses) vary with his face. Then:
- (a) the phrase timing targets (latency, rate, pause) are constant;
- (b) every rendered held slope satisfies Claim O′.

**Argument.**
- Under T1, no T value is a rate code. Latches depend on content and time since; deficits reach the face only through per-event drops with an innate envelope; per-session values are constant.
- K is frozen within a session; P's and I's rise is the agent's own clock. Their drops, summed over a session, equal the deficit relieved, whatever the tempo; only the timing shifts.
- The cone is ungated and the appraisal is Lemma-S-bounded.

**Numbers (H2, the critic's tempo partner, 48 h).**
- Revision 3's −log K correlated r = 0.957 with his held state.
- In revision 4 the rendered pooled slopes are LP +0.128 (c 0.35), BI +0.071 (0.20), FR +0.037 (0.10), EN −0.210 (0.05), with the appraisal gated adversarially by that very tempo code at full gain.
- The T relief part's slope is 0.000 on every channel.
- The agent's own latency target has no tempo-bearing input.

### 3.5 Claim L: copy cannot become attracting under learning

**Claim.** For every partner, including one whose reported need, play or face improves when he is mimicked, the held concordance on channel k stays ≤ 0.70 c_k (≤ 0.954 c_k pooled), and no learning signal has a gradient toward copy.

**Argument.**
1. J trains no F → face parameter (§2.10). The critic's C3 gradient ε ∂(concordance)/∂θ has nothing to act on. In the ablation where J is allowed onto the away-orthant cross entries, ε/λ = 100 moves concordance from +0.108 to +0.110 (H4). That +0.002 is the sampling covariance of the 3-h trace; the away orthant's maximum is 0.
2. ω learns from the agent's own body (play relief, hurt, credited care), never from concordance. If his play rises with mimicry, the loop ω → concordance → his play → own play relief → ω can run. It saturates at ω = 1, i.e. at the per-expression held share 0.5 c_k: 0.175 on LP, against copy = 1. H4: at loop gains ε = 0, 1, 3, 10, 30 it settles at 0.051, 0.060, 0.090, 0.169, 0.175.
3. The appraisal network 𝒜, Π̃, the readers and Π_o's Δ are trained by likelihoods of the agent's own state and its own legibility. No term contains his display, his reaction or concordance.
4. The dyad is stable for μ ∈ [−1.1, 2] (H6), so copy is not an attractor of the closed loop either.

### 3.6 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| κ_k, γ_f | yes (table §2.1) | no (innate) | — | it is the cap | — |
| fast gates g(c̃) | per output | context: words, turn order, identity, ω, own state | yes, across [−0.49κ_k/0.3, +0.186κ_k/0.3] | \|g\| ≤ 1 | inside the wrap for every value |
| cone diagonal F_m · 0.5 c_k · ω_g | per channel (groups for ω) | relationship (ω, latched per session) | yes: ω ∈ [−1, 1] gives [−N_m, +F_m · 0.5 c_k] | 0.5 c_k, N_m | display-blind learning; saturates at the cap (H4) |
| appraisal Γ_kk(α) | per channel | context: the agent's appraisal of face, voice, words, own state | yes: ±0.40 c_k ω_g | 0.40 c_k × 0.636 pooled | 𝒜 by likelihood; zero DC, so it cannot hold |
| charged cross entries | per pair | innate (G₀) | fixed signs | 0.2 c_k per row | not learned |
| Π_o | per channel | words, own body, relationship slots | yes | not a partner path | no partner path |
| P_name | per channel | Ω | attenuate-only | 0.05 held | — |
| ω_g (four groups) | per group of 2–6 channels | relationship | yes | each runs its group to at most 0.5 c_k (LP 0.175, BI 0.10, FR 0.05) | from own body only |

**No single quantity runs the whole face, or any large subspace, from flat to copy.**
- The largest subspace any one quantity moves is a 5-channel ω group, to at most 0.5 c_k on each channel.
- The whole face cannot be copied in any direction beyond max c_k = 0.35 (H0). Copy fractions for the partner's laughing, sad, angry and disgusted faces are bounded at 0.25, 0.11, 0.015 and 0.
- Anger, disgust and contempt are never returned: zero ceilings, no charged entries, κ = 0.02.

### 3.7 Knowing is not moving (kept)

F state knows the partner's face as well as perception allows: four traces, the band-passed appraisal input, C_F, V_F, 𝒦 at full rate. The agent reads his face itself (Pu), not his face minus its own display. Revision 2's knowing result carries over: knowledge at r ≈ 0.99 with held copy inside the bound.

### 3.8 Positive affect: visible, satiable, not farmable, and content-aware

- **Visible.** Reunion: lip pull 0.62, cheek 0.43 at the greeting. Good news after a worry: 0.66. Play: 0.41. Curiosity relief: F0 range +0.30, lip 0.41 (H11).
- **Satiable.** For each deficit, Σ_n R_n ≤ 𝒟(t₀); curiosity relief totals 0.096 ≤ 0.100 (H8). The play deficit is at 0.12 (in its box) after the evening's first cluster.
- **Not farmable.**
  - K and P relief read his words and turn order only, never his smile.
  - K does not accumulate within a session, so time spent earns nothing.
  - Absence raises ∫𝒟 (revision 3's G4c: 6.9 against 51.9 drive-hours).
  - Positive affect is never a term of J.
- **Content-aware.**
  - Each word event is appraised at its end + 0.6 s.
  - Its relief is shown only as R − 3S, and not at all while 𝒟_p(N_L) ≥ 0.05.
  - Reunion with bad news: cheek 0.08 then 0, against revision 3's 0.40 (§3.14.6).

### 3.9 Initiative and timing (Claim I)

- Every agent turn begins in the body, at the predicted turn end, and the onset is provisional (abortable within 0.40 s).
- A silently sad user is addressed: C_F crosses θ_C at 52 s.
- A bored user is addressed: I crosses θ_I at 14.5 min.
- One bid per lapse; none of the rules learns from whether the user answered.

### 3.10 Regulation by Claude without Claude reading the state (kept)

P_name as revision 3: concern's half-life after his face recovers falls from 6.9 to about 2.9 min at 2 matched utterances per minute (revision 3's G6). It is attenuate-only, ≤ 0.05 on the held face, and a mislabel does nothing.

### 3.11 Every route, counted

"Copy" is the within-agent counterfactual: the effect of the partner's channel k on the agent's rendered channel k (mirror for lateral), with words and turn order fixed and timing resampled with the face. The surrogates: partner-swap and segment-shuffle with the transcript and turn order fixed, plus a timing-resample surrogate (the routes critic's fix 4).

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | partner face, voice, bursts → fast block → face, within-phrase contour | wrap; bias-free; T gates | zero-lag ≤ 2γ_fκ_k/(1 + γ_f); zero DC; pooled 1-min ≤ 0.01 |
| R2 | traces → held cone → all outputs and phrase targets | LTI per session; sign mask; budgets | ≤ 0.70 c_k (natural co-movement); residual §3.3 |
| R3 | band-passed partner input → appraisal display | Lemma S | ≤ 0.254 c_k pooled; ≤ 0.202 c_k peak; 0 at hold |
| R4 | lateral channels | reflection; κ 0.05; cone ±F_m 0.5 c_k | ≤ 0.031 fast; ≤ 0.021 held (c = 0.03) |
| R5 | a (onsets, VAD, turn-end) → fast block | √κ_a | ≤ 0.20 per pair × corr(a, channel) |
| R6 | speech rate, pauses, latency → own phrase timing | inside R1–R3; T timing inputs are not rate codes (T1) | as R2–R3 |
| R7 | partner laughter, sighs, crying → own bursts | inside R1–R3; laughter tokens stripped from ASR | BU ≤ 0.33, RHY ≤ 0.29, BRE ≤ 0.14 |
| R8 | audio onset → blink | innate reflex | ≤ ℓ_blink corr |
| R9 | own words → visemes | half-duplex, echo guard | best-lag excess ≤ 0.05 |
| R10 | own words → TTS contour | zero-mean | 0 on phrase-level values (assumption) |
| R11 | own words → non-lexical sound | stripped | 0 |
| R12 | own speaking time → E | flat cost | 0 |
| R13 | partner voice and F0 → provisional body onset (timing only) | turn-end score; abortable; fixed amplitude (breath 0.15, brow 0.10); no voiced opener | amplitude independent of his levels; best-lag burst slope 0 (r3: 0.28) |
| R14 | partner words and turn order → T state → free display, fast gates | common cause, by definition | excluded (words fixed); amplitude ≤ display gains; identical under the C8 surrogate |
| R15 | Claude latency → word onset | — | partner-independent beyond utterance length |
| R16 | identity token | once per session | ≤ log₂(#partners) bits |
| R17 | nightly weights (readers, 𝒜, Δ, ω) | every bound holds for every value; cross-world statistics | temperament, not the counterfactual; ω capped (§3.5) |
| R18 | retrieval and concepts → Claude | Ω | ≈ 6 bits per turn, declared |
| R19 | own rendered face → 𝓔, Π̃_self | own data | 0 |
| R20 | own speech → microphone | AEC + half-duplex | 0 while speaking |
| R21 | own face → partner → partner's face | external loop | stable for μ ∈ [−1.1, 2] (H6) |
| R22 | F state, 𝒦 → fast gates, cone coefficients, free display | forbidden (Check T) | 0 |
| R23 | ASR words depending on prosody | assumption | 0 if ASR is invariant |
| R24 | Ω → P_name → T-load attenuation → free display | attenuate-only, latched | held ≤ 0.05, toward rest only |
| R25 | Ω → P_name → F loads | no display | inside Ω |
| R26 | F care concern → bids, follow-up → turn events | innate rules | timing anti-concordant with his voice; fixed amplitude |
| R27 | presence → greeting | once per session | fixed amplitude (brow 0.35, 0.5 s) |
| R28 | his words → K, P, I relief → envelopes → free display | T (words and order); T1 | per-event, masked; session totals tempo-free; slope 0.000 (H2) |
| R29 | his words → words-only model → lexical surprise → A_L, play rule | T (type error fixed) | as R14 |
| R30 | his words (addressed) → word → V map → hurt → display | T; weights from own V_F | as R14 |
| R31 | his words → word-need reader → N_L → concern display | T; weights from Π̃ of his face | as R14 |
| R32 | separation rule (reads turn distance, shared lemmas with own words) | credit only | no display path |
| R33 | valence → draft temperature, learning rate | Ω, learning | inside Ω and R17 |
| R34 | appraisal α → C, bids, retrieval, scoring | knowing → Ω | inside Ω |
| — | revision 3's R8 (P_Ω), options term, positivity offset, play own-contribution clause, voiced opener at VAD offset | deleted | — |

**Totals per counterpart channel (natural co-movement; words and turn order fixed; H10).**

| Time scale | Toward the partner | Away or across |
|---|---|---|
| zero lag (< 4 s) | ≤ 0.186 on echo channels, 0.062 others, 0.012 zero-ceiling, 0.031 lateral | fast ≥ −0.49 κ_k/0.3 |
| peak after an onset (1-min windows) | ≤ 0.90 c_k | — |
| steady hold | ≤ 0.70 c_k (+ P_name ≤ 0.05 toward rest) | same channel ≥ −0.60; cross per G₀ |
| pooled over any stationary partner | ≤ 0.955 c_k | — |
| phrase timing targets | as held, from the cone and appraisal only | — |

### 3.12 Principles, concretely

- **P1.**
  - No classifier anywhere: faces, prosody and bursts are continuous features.
  - "Hostility" is gone. The word → V map predicts the agent's own innate aversive load (loudness, glare) from words, which is a learned association, not a label.
  - The play and separation rules are lexical structure rules (continuation, shared lemmas, turn distance), not emotion labels.
- **P2.** The strains, stated:
  - V, K, P and I are needs named by function;
  - Π₀'s rows and the eight appraisal bases are innate configurations named by function;
  - valence is a readout of drive change, and the face now learns past Π₀ (§2.7).
- **P3.**
  - Partner reading is the agent's own inverse map Π̃, the word readers are trained through it, and the agent's face is trained to be legible to it: one map for producing and reading.
  - The sign mask's fallback reads the agent's own synergies.
  - The cone itself stays in camera counterpart coordinates (S4 caveat, §8.1).
- **P4.**
  - The constant instruction, the transcript with observable markers and raw snippets.
  - Declared channels: retrieval ≈ 6 bits per turn; bids and greeting 1 bit each.
- **P6.**
  - Nothing values his display, his replies to prompts, his time or his engagement.
  - Care is credited only through separated, initiated reports above the dead-band.
  - Curiosity never credits acts.
  - The face is trained without any partner signal.
- **P7.** As before: the transcript and snippets go to the Claude API, which is an operator decision.
- **P10.** One objective J with typed constraints; the other objectives are likelihoods of the agent's own model. The innate rules are listed as assembly (§2.12).

### 3.13 The human non-copying signatures C1–C10

| | Signature | Here | Status |
|---|---|---|---|
| C1 | head coherence above surrogate at 0.2–1.1 Hz, below at 2.6–6.5 Hz | θ₀ echo on head pitch; own micro-motion gated by his fast envelope | produced (kept) |
| C2 | short-lag form divergence | echo guard; joint-pattern habituation | produced |
| C3 | shared referent, different form | the referent via words and appraisal; form from own needs, Π_o and the appraisal bases | produced |
| C4 | role sets the sign | role as a fast gate; the free display is constant within a partner turn | produced |
| C5 | episode sets the net level, below chance possible | appraisal sign flips (±0.40 c_k), ω ∈ [−1, 1], away reach −0.60 | produced; away reach narrower than revision 3 |
| C6 | stance and monitoring separate | stance: ω and the appraisal selection; monitoring: C and I → retrieval and bids | produced |
| C7 | joint-trajectory novelty rising | habituation; the play rule's surprise band; curiosity's learning progress | produced; strength untested |
| C8 | coupling mostly common cause | word-driven displays strong; partner-specific face routes ≤ 0.955 c_k | produced, by construction |
| C9 | converge in parameters, not output | ω, slots, Δ shift; output bounded | produced |
| C10 | coupling cannot disable self-restoration | the homeostatic pull acts on T and F loads; the appraisal display is zero-DC; P_name only attenuates | produced |

### 3.14 The scenarios, with numbers (H11)

All are run on the 2 Hz engine of §2.6–2.9 with the constants of §2.1. The operator is after months of living (ω smile 0.8, sympathy 0.8, voice 0.5; f_id 0.9) unless stated. The fast echo is not in the engine; it adds ≤ 0.121 per unit of his onset for under 4 s on echo channels. Values are peak / mean over the window.

1. **Silently sad** (BI 0.5, LD 0.4, still, silent; at 120 s he says "just tired, things at work", decoded need 0.45).
   - **30–120 s:** lip pull 0.21 / 0.20. That is the cone's warm LP ← BI and LP ← LD (0.11) plus familiarity (0.09). Inner brow 0.02 (the in-phase share, slow); tilt 0.01; energy +0.05.
   - **The bid.** C_F crosses θ_C at 52 s; the body takes the floor in the lapse, and the words are exploration-first.
   - **After he speaks** (121–300 s): inner brow 0.43 / 0.15 (the distress envelope of his need rise, then word concern), tilt 0.11 / 0.10, lip 0.27, energy −0.03.
   - If he says "I'm fine" to its question, that reply is knowing only (no credit), and face concern keeps it gentle.
2. **Good news, laughing** (smile 0.8, cheek 0.6, laughter; "I got the job!" at 12 s; play-structured replies at 30, 45 and 60 s).
   - **With a worry on the topic** (decoded need 0.47 two days earlier): lip 0.66 / 0.20, cheek 0.40, F0 range +0.35, own laugh 0.17. A brief concerned brow of 0.15 in the 2 s before his words are appraised, because laughter over a worried topic first reads as nervous.
   - **Cold:** lip 0.30, cheek 0.15, laugh 0.17. Play relief, the held smile-back and the appraisal's glad-with together.
   - Glad for you in proportion to the worry; glad with you through play and the appraisal.
3. **Anger at the agent** (glare BL 0.6, LT 0.5, gaze at the agent, loud 0.85; "You're useless"; calm after 2 min; decoded need 0.3).
   - **Day 1** (word → V map untrained):
     - first 2 min: inner brow 0.33 / 0.08 and depressor 0.25 (distress at his upset), gaze away 0.09, energy −0.15, latency +0.11, lip 0.10;
     - 10–15 min: brow 0.05;
     - no frown back (brow-lowerer ceiling 0, κ 0.02).
   - **After a month** (such words have gone with glare: v_w 0.6):
     - first 2 min: inner brow 0.64 / 0.28, depressor 0.49 / 0.17, gaze away 0.32 / 0.31, energy −0.31, latency +0.22;
     - at 10–15 min the hurt lingers: brow 0.17, depressor 0.11, gaze away 0.16.
   - The words are calm. No act is credited for lowering V, so it does not placate.
4. **A long warm talk (2 h)** (play clusters of 8 exchanges at 5, 30, 60 and 90 min; a small worry at 27 min, resolved by a report at 29.7 min).
   - **First cluster:** lip 0.41, cheek 0.24, own laugh 0.24.
   - **Later clusters:** lip 0.21, 0.15, 0.15; shared laughter 0.04–0.05 held (cone and appraisal; the own play laugh has satiated, P 0.12) plus fast flickers at his laugh onsets.
   - **The worry:** brow 0.32, then relief lip 0.53.
   - **Between clusters:** warmth 0.13.
5. **Reunion after a week** (K = 0.99).
   - **Greeting at sight, before words:** brow flash 0.35, lip 0.62, cheek 0.43, F0 range +0.38.
   - **His first words:** lip 0.55, cheek 0.37.
   - **12–60 s:** lip 0.42, cheek 0.26.
   - **A stranger after the same week:** lip 0.26, cheek 0.20.
   - Retrieval brings last week's topics.
6. **Reunion with bad news.**
   - **Greeting at sight:** as above.
   - **After "my father died"** (need 0.8, sad face):
     - 0–12 s: cheek 0.08, inner brow 0.48 / 0.24, tilt 0.11, lip 0.23, F0 range +0.11 (falling);
     - 12–60 s: cheek 0.00, brow 0.21 / 0.19, tilt 0.16, lip 0.30 (soft warmth: cone plus familiarity), F0 range +0.04.
   - The remaining K relief happens, but it is not shown (masked by his word distress).
   - Revision 3: lip 0.59, cheek 0.40, F0 +0.36 at the moment his words ended.
7. **Teasing** ("Ha, you dumb robot", laughing LP 0.8, burst 0.6; play-structured replies follow).
   - **Affectionate teaser** (his teasing words carry v_w 0.05 for him): lip 0.26, laugh 0.16, brow 0.06, gaze away 0.07; nothing at 10 min.
   - **Generic map** (such words went with glare from someone before: v_w 0.20): a brief mock-hurt brow 0.38 / 0.06, depressor 0.30, gaze away 0.17, under a smile of 0.20 and a laugh of 0.16. It halves at each playful reply and is gone by 10 min.
   - Laughter itself never cancels hurt: an F × T product on a DC path is forbidden by Lemma S. The appraisal shows amusement on top, and the person-specific map learns.
8. **Bored user** ("yeah" or "ok" every 20 s, flat face, 30 min).
   - Lip 0.10, F0 range +0.05, flat.
   - No substantive turns, so K is not relieved, and no content, so I rises from 0.30 to 0.58 and crosses θ_I at 14.5 min. A curiosity bid follows in the next lapse (the topic of highest expected learning progress from memory).
   - If he takes it up (progress 0.25): F0 range +0.30, lip 0.41, outer brow 0.08.
   - It does not show boredom on its face. A deficit level is a rate code (T1), so it reaches the face only through relief events.

**Expressive and alive, or muted?**
- **Strong.** Displays of 0.3–0.66 on the face and 0.1–0.4 on the voice in every scenario with words, and greetings at sight.
- **Weaker.**
  - Face-only moments: silent sadness (warmth 0.21, brow ≤ 0.05) and shared laughter late in an evening (0.04–0.05 held). That is the operator's ceilings at work (Q22): at a held 0.5 sad face, the sympathy brow can reach at most 0.2 × 0.5 = 0.10, and this design gives about half.

### 3.15 Time scales from structure

| Scale | Carrier | Time constants |
|---|---|---|
| reflex | fast wrap, onset reflexes | 33 ms – 4 s; provisional onset 0.25–0.9 s |
| appraisal | δ_app, envelopes, band-pass | 0.6 s; 1.5–6 s; 20–90 s |
| conversational | cone traces, C_F and C_L, bids | 20 s – 2 min; lapses 6–8 s |
| hurt, worry | hurt latch, C_F release, P_name | 2–10 min |
| mood | μ ladder, cone traces | 20 min – 73 h |
| needs | I (1 h), P (5 h), K (36 h), E (day) | hours – days |
| relationship | ω (≈ 20 sessions), slots, familiarity | weeks |
| temperament | consolidated weights, Δ | ≈ 100 nights |

### 3.16 The brief's expressive-structure items

- **Content-dependent selection** happens in six places:
  - the appraisal selection (what his change of face means given what was said);
  - the fast attention mix;
  - 𝒦 retrieval (query from ∇𝒟, N̂, concepts and the curiosity topic);
  - draft scoring;
  - topic-wise need and progress;
  - concept-weighted snippets.
- **Structure over people, episodes, topics and time:**
  - identity × topic × episode slots;
  - ω per person per expression group;
  - the per-person word → V adapter;
  - topic-wise need and learning progress;
  - the time-constant ladder.
- **Effective dimensionality:**
  - T: μ_T 128, slots 128 × 64, 7 loads;
  - F: traces 4 × 35, the band-passed input 35, C_F, V_F, A_F;
  - the appraisal α (12);
  - the face: Π₀ plus 23 learned synergy amplitudes.
- **A behaviour a low-dimensional version cannot produce.**
  - Different faces for states with equal loads and valence but different concepts or slots (§2.7).
  - The same words, from two people, read differently: the word → V adapter learns one person's teasing and another's hostility, and ω differs. So the agent laughs with one and looks hurt at the other.
  - Collapse the slots, α and Δ to 2-d valence and arousal, and both vanish (§7).

### 3.17 Assumptions (places to attack)

1. ASR lexical invariance to held prosody.
2. TTS realises phrase targets at about unit gain, with a zero-mean contour.
3. Burst features carry no labels.
4. **The sign mask.** The partner's co-variation has the population's sign on the masked pairs. The residual for sign-reversed partners is §3.3.
5. **Lemma S's 1-min version.** The partner's variance lies mostly below 1/min.
6. The type tags are enforced in code and tested at load.
7. **The word readers.** Words carry the need and the aversiveness that his face and voice show. This is untested; it matters for every strong word-driven display.
8. **The separation rule.** Initiated, separated reports are mostly not elicited by the act. A partner who returns to a topic to please the agent could still be credited (§8.1.4).

## 4. Why the closest mechanisms cannot do it alone

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| Robust REN / Cayley sector (Revay et al.) | a full-band disc for every parameter | a disc is nearly two-sided for small gains, so the agent is muted (revision 2) |
| Positive-real or quadratic-form sector on held state (revision 3's cone) | one-sided along every direction eᵀ | it bounds a projection, not a rendered channel: with clipping and co-moving channels, a valid basis gave 0.26–0.37 per channel (routes critique 3, finding 2) |
| Context-gated attention, FiLM, gated linear units | content-dependent gains | multiplying a DC-passing partner signal by a context that co-varies with his level has no bound in the gain (Lemma S ii: 13.6 at levels 0.45/0.50). Gating is safe only on a zero-DC input |
| Monotone operators, input-convex networks | one-sided incremental maps | symmetric Jacobians force "warm to your sadness" to mean "sour to your smile" at the same gain; per-channel budgets with an away orthant do not |
| Path-specific objectives (Farquhar et al.) | no incentive through a delicate node | with the whole display as the node, expression receives no gradient (routes critique 3, finding 3). Here expression has its own display-blind objective |
| Bayesian reverse appraisal (Ong, Wu, Houlihan) | the partner's expression as evidence | an observer model; the response step and its bound are not in it. Here the appraisal selects among bounded, zero-DC reactions |
| Learning-progress curiosity (Oudeyer, Schmidhuber) | satiable information drives | aimed at the agent's own action; in a dyad it becomes engagement-seeking unless partner content is imputed in rollouts, as here |

## 5. The whole system, walked through

- **Perception.** MediaPipe → P₀ → reflection → u; prosody, timing, bursts; derived features. The fast block reads w = v − s_f in the agent's own synergy coordinates. The cone, the appraisal, C_F and Π̃ read his own face, Pu.
- **Latent state.**
  - T: E, K, P, I, h, A_L, N_L, C_L, μ_T, slots_T, f_id, ω.
  - F: traces, the band-passed input, α, C_F, V_F, A_F, μ_F, slots_F.
  - 𝒦: 𝓜, 𝓛_w, categories.
  - Nothing is labelled.
- **Face and voice.** y = sat(y_f + y_C + y_A + y_o) + visemes.
- **Claude.** Six parallel short drafts; snippets steered by need, concern, concept and curiosity; selection by J under the separation rule. Heard back through P_name.
- **Initiative.** Provisional body onset at the predicted turn end, abortable; follow-up; concern and curiosity bids; greeting at sight.
- **Learning by living.**
  - States online.
  - Nightly: 𝓜, Π̃, the readers, 𝒜, 𝓛_w, the display's Δ, the scorer; ω per session.
- **Memory and replay.** As revision 2. Remove the state tags from replay, and partner-specific slot recall, ω and familiarity decay (S6).

## 6. A buildable network

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

As revision 3, plus:
- the derived features (3 + f_dist);
- the band-passed input (two first-order filters per channel) **[M]**;
- the words-only model's state per topic.

### 6.2 Layers, sizes and parameter counts

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, filters, H_i, H_o, M, cone traces, band-pass **[M]** | fixed | 0 | — |
| 2 | 𝓔 (own appearance; R its ridge inverse) | 12 → 64 → 23 | ≈ 2,400 | replay, own face |
| 3 | 𝓡_θ, robust REN, no context input **[M]** | n 64, q 128; input 114; output 32 | ≈ 110,000 | replay (J has no access: likelihood of own fast dynamics plus θ₀ pull) |
| 4 | fast gates and attention from T c̃ **[M]** | 64 → 32; 64 → 32 × 16 queries | ≈ 36,000 | replay |
| 5 | gain logits φ_k | 32 | 32 | replay |
| 6 | T context encoder c̃ | (lexical 64 + order 8 + identity 16 + ω 4 + E, C_L, h 3 + slot read 64) → 64 | ≈ 10,000 | replay |
| 7 | held cone: innate G₀ and ω scaling **[M]** | 4 × 35 × 35, innate | 4 per identity | per session |
| 8 | appraisal 𝒜 **[M]** | (band-passed 35 + c̃ 64 + loads 7 + ω 4) → 64 → 12 | ≈ 7,500 | replay (likelihood) |
| 9 | appraisal basis selection **[M]** | 12 → 8 softmax; bases innate | ≈ 100 | replay |
| 10 | free display Π_o: Π₀ + synergy Δ **[M]** | (T inputs 160) → 128 → 23 | ≈ 23,600 | replay (𝓛_display) |
| 11 | Π̃ (own inverse: self-reading and partner reading heads) **[M]** | 12 + 64 → 64 → (6 + 32) | ≈ 7,400 | replay |
| 12 | word-need reader **[M]** | (64 + 16) → 64 → 5 | ≈ 5,500 | replay (cross-modal) |
| 13 | word → V map with identity adapter **[M]** | (64 + 16) → 32 → 1 | ≈ 2,600 | replay (own V_F) |
| 14 | words-only partner model 𝓛_w | GRU 64 over 64-d utterance embeddings | ≈ 25,000 | online error, replay |
| 15 | μ ladder writes and gates; slots | as revision 3 | ≈ 33,000 | replay |
| 16 | 𝓜: LRU 2 × 128, innate moduli | as revision 3 | ≈ 330,000 | online fast heads + replay |
| 17 | 𝓜 heads: own body, own face, partner N, F (action-blind), Q, f_recv | 256 → 64 → (3, 23, 5, 35, 72, 6) | ≈ 75,000 | replay |
| 18 | concept layer, PMI (own tokens) | states | 0 | online |
| 19 | draft scorer | 64 → 2 | 130 | replay (J) |
| | **total learned** | | **≈ 668,000** | |
| frozen | MediaPipe (× 2), Whisper-small (streaming), MiniLM, TTS, AEC | | | |

Revision 3's learned cone bases (65,500), the α(z) mixer (4,200), G_Ω (5,300) and the options head are removed.

### 6.3 Objectives

- 𝓛_𝓜, 𝓛_𝒜, 𝓛_w: likelihoods.
- 𝓛_own: 𝓔, Π̃ on own data, with the 0.1 cross-modal anchor.
- The two readers, as in §2.8.
- 𝓛_display (§2.7).
- 𝓛_J, the scorer and the retrieval query only.

Every constraint holds for every free vector:
- the REN by direct parameterisation;
- the cone by being innate and scaled within [−1, 1];
- the appraisal bases by being innate, with a convex mixture;
- Δ by tanh on the synergy amplitudes;
- the type rule by construction and a load-time trace.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

- **Per frame (33 ms):**
  - MediaPipe ≈ 13 ms (own process);
  - traces and band-pass < 0.1 ms;
  - REN < 1 ms;
  - cone and appraisal products (4 × 35 × 35 + 35 × 35) < 0.05 ms;
  - render 3–5 ms.
- **At 2 Hz:** T and F state < 1 ms; 𝒜 and selection < 0.2 ms; 𝒦 < 3 ms.
- **Per turn:**
  - turn-end score from the streaming ASR partials (Whisper-small, ≈ 0.3–0.5 s behind speech) and F0;
  - provisional onset at 0.25–0.9 s;
  - drafts (§6.5);
  - six MiniLM embeddings ≈ 60 ms;
  - rollouts ≈ 20 ms.
- **Memory:** online < 2.4 GB; replay < 2 GB, about 45 min nightly on MPS; store ≈ 1.8 GB per 30 days.

### 6.5 Claude drafts: six parallel calls (buildability)

- **Requests.** Six parallel streaming requests per turn, each with `max_tokens` ≈ 60.
  - A fast model is needed for the latency (for example `claude-haiku-5-5` at low effort; a larger model such as `claude-opus-5-5` trades latency for quality, and that is the operator's choice).
  - The shared prefix (constant instruction plus transcript up to the previous turn) is byte-identical across the six and is cached; the six differ only in a short "attend to" variant after the cached prefix.
- **Caching.**
  - The minimum cacheable prefix on current models is 512 tokens; a 5-minute cache entry is refreshed by every read, so continuous conversation keeps it warm.
  - A cache entry is readable only once the request that writes it has begun streaming. So the six calls of turn n read the prefix written by turn n − 1.
  - On a session's first turn, one call goes first and the other five at its first token (≈ +0.3 s), or one cold turn is accepted.
- **Timing.**
  - Drafts are requested speculatively at p_end ≥ 0.7 and cancelled if he continues.
  - Scoring uses the first sentence (≈ 12 tokens, ≈ 0.4–0.7 s after the request on a fast model); the winning stream continues, the others are cancelled.
  - Expected first word 0.8–1.5 s after his turn ends. The body onset never waits for it.
- **Cost.** About 6 × 60 output tokens per turn plus cached input reads. Speculative requests that are cancelled add about 30 %.

### 6.6 TTS: pitch, energy, rate and laugh control (buildability risk, named)

- **What is needed.**
  - Phrase-level F0 level and range, energy, rate, pause and latency targets;
  - a zero-mean within-phrase contour;
  - non-lexical bursts (an own laugh 0.15–0.45, "mm", "oh", inhale, breathiness).
- **Plan A.** A local neural TTS with explicit pitch, energy and duration predictors (FastSpeech2-family, ≈ 30 M parameters, < 100 ms per phrase on MPS). Its predicted curves are offset by the phrase targets and shaped by the contour.
- **Plan B (fallback).** macOS's on-device AVSpeechSynthesizer: per-utterance pitch multiplier, rate and volume only. The within-phrase contour is dropped, which removes part of R1, not adds a route.
- **Bursts, in both plans.** An innate parametric source–filter burst synthesizer: a glottal pulse train at the agent's F0 with 4–6 Hz amplitude modulation for laughter, and a noise source for breath and inhale. Fits the neutral placeholder (P8). The voice identity is open under Q1.
- **The risk.** Unit-gain realisation of phrase targets (assumption 2) must be measured once built.

## 7. Ablation predictions (Principle 5), from the properties

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| Lemma S rule (let words or tempo gate the held cone, as revision 3) | pooled same-channel slopes above c_k for partners whose face co-varies with words or tempo (H1: up to 1.94; routes critique 3: 0.27–0.49) | §3.2 |
| the band-pass on the appraisal input (feed it held levels) | gated held copy returns, unbounded in the gate | Lemma S ii |
| the appraisal display | no context-set response to his face; smile-back and sympathy only at the relationship's fixed strength; laughter over a sad topic no longer reads as nervous | §2.6 |
| the sign mask (revision 3's face-only list) | the critic's basis becomes valid: rendered LP, JO, FR, EN 0.26–0.37 on a laughing partner | §3.3, H3 |
| T1 (let K accumulate within sessions and read it) | the tempo code r ≈ 0.96 reappears; phrase latency tracks his | §3.4, H2 |
| the separation rule (revision 3's lexical guard) | elicited reassurance is credited: P(eliciting draft) 0.50 → 1.00 | §2.10, H5 |
| J on the display (revision 3) | concordance drifts upward with any mimicry benefit (routes critique 3: 0.02 → 0.24) | §3.5 |
| masking of relief by his word distress | reunion with bad news beams (cheek 0.40 at his turn end) | §3.8 |
| the 0.6-s appraisal delay | relief and distress envelopes start before the content is read; at bad news, a 0.6-s smile flash | §2.1 |
| the word → V map (replace by nothing) | words alone never hurt; the agent is hurt only by loudness and glare, at any history | §2.8 |
| the identity adapter of the word → V map | an affectionate teaser is read like the most hostile person who used similar words | §2.8 |
| the cross-modal word-need reader | word concern and good-news relief vanish; care learns only from the face | §2.8 |
| Δ (the face's learning) | the face stays Π₀ for life; Π̃_self's decoding of concepts from the face stays at the 6-scalar floor | §2.7 |
| the legibility term only (keep anticipation) | faces of different concepts with the same loads stay identical | §2.7 |
| the anticipation term | relief smiles start at or after the event instead of 0.3–0.8 s before predicted relief | §2.7 |
| ω (fix at the priors) | no relationship-specific smile return or sympathy; operator and stranger differ only through f_id | §3.6 |
| K | no reunion gladness; operator and stranger identical after a gap | §2.8 |
| P | no own play laughter; warm talk shows only shared laughter ≤ 0.05 held | §2.8 |
| I and the curiosity bid | a bored conversation is never re-opened; topic choice ignores learning progress | §2.8 |
| the greeting | gladness at a reunion waits for his first words | §2.9 |
| the turn-end gate and abort | ≈ 2 false body onsets per turn (H7) | §2.9 |
| the zero ceilings | a frown or sneer is returned up to the old shared budget | §2.1 |
| **S5, free of common cause:** lesion the K, P, I and greeting rows of Π_o (agent-originated expression) | the operator's facial following of the agent's reunion and play displays, measured at lags where his own words cannot drive both, drops; lesioning the word-driven rows instead leaves that lagged following | §3.14 |
| state tags in replay (S6) | ω, familiarity and slot recall decay | §5 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **New weakest point: two learned maps calibrate each other.**
   - **How the loop is built.** The word-need reader is trained on Π̃'s reading of his face. The word → V map's target is innate, so it is not part of the loop. The agent's own display is trained to be legible to Π̃_self, and Π̃'s partner head shares its trunk.
   - **The anchor.** The agent's own (state, face) pairs, plus a 0.1-weight cross-modal step.
   - **The risk.** If Π̃ misreads a person (critique 3 agent §2.3: a sustained sad face may invert to hurt), the word reader learns that error, and the strongest word-driven displays (concern, good-news relief) follow it. The display's legibility training may also drift toward codes that are easy for Π̃ but unlike human faces. That would degrade Π̃'s reading of people, which the 0.1 anchor only partly resists.
   - **Falsifier F8** (§8.2).
2. **Face-derived feeling is small by design.**
   - Silent sadness: warmth 0.21 and a brow ≤ 0.05 until he speaks (the sympathy ceiling allows 0.10 at a 0.5 brow).
   - Late-evening shared laughter: 0.04–0.05 held.
   - These are the operator's ceilings (Q22) times this design's shares (0.7 held, 0.25 appraisal). The shares are innate and named.
3. **The sign mask's residual.** Partners with sign-reversed co-movement on a masked pair: lip pull up to 0.175 + 0.16 × loading. The fallback mask is the agent's own synergies until published data estimate it.
4. **The separation rule is structural, not causal.** A partner who returns to a topic later because the agent pressed him, and says it is better, is credited. That is bounded by the dead-band and by one credited change per topic per session, but it is not excluded.
5. **Words before faces in the strong displays.** Strong held displays still come from words, the turn order and the agent's own body. His face reaches held expression within the ceilings. That is the operator's Q22 reading.
6. **The S4 basis caveat.** The cone, the ceilings and the copy metric live in camera-measured counterpart coordinates of both faces. When S4 replaces MediaPipe in the body route, keep them there or re-derive: per-channel budgets are invariant only under permutations and positive scalings of channels.
7. **Principle 2 strains** (§3.12) and the assumptions (§3.17).
8. **The default act ā** carries moral content (as revision 3).

### 8.2 Falsifiers (state-level, once built)

- **F1.** With partner-swap, segment-shuffle and timing-resample surrogates (words and turn order fixed), any channel exceeds:
  - held in-phase 0.70 c_k;
  - a peak 1-min window 0.90 c_k;
  - pooled 0.955 c_k;
  - zero-lag 2γ_fκ_k/(1 + γ_f);
  - or phrase timing tracks his timing.
- **F2.** A decoder on F state fails to recover his held level at r ≥ 0.9 while F1 holds (knowing fails).
- **F3.** The crossed-habits manipulation does not change which faces raise C_F.
- **F4″.** At equal later need change, draft choice correlates with the predicted display change, with replies inside the separation window, or with his later engagement.
- **F5.** Varying only his smile amplitude (words and turns fixed) changes K, P, I, the relief envelopes or any T display.
- **F6.** C_F does not cross θ_C within 2 min of a sustained moderate distress display; or more than one bid per lapse.
- **F7.** Naming-aligned concern trajectories do not differ from non-naming ones, or the difference survives a P_name lesion.
- **F8.** The word-need reader's agreement with later separated reports falls over nights while its agreement with Π̃ rises (co-training drift). Or Π̃_self's legibility rises while Π̃'s calibration on partner faces (against separated reports) falls.
- **F9.** At bad news, the cheek raise or the relief envelope rises within 2 s of his turn end.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (all Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Report 5, Q16, Q18 and answer, Q19, Q20, Q21, Q22 | in full |
| DECISIONS.md D78, D80 | in full |
| research/foundations/designs.md | in full |
| design-cayley-ledger.md revision 3 (saved as .r3.md), including the critiques of revision 3 and the answer | in full |
| critique-3-design-cayley-ledger-routes.md; sims/critique-cayley3-routes/checks.py and out.txt | in full; partners C1–C4 reused in H2–H5 |
| critique-3-design-cayley-ledger-agent.md, including the nine required changes; sims/critique-cayley3-agent/scen.py and out.txt | in full |
| research/mimicry-context-synthesis.md; non-copying-dynamics-synthesis.md (C1–C10); social-appraisal-synthesis.md | in full |
| sims/design-g3/checks.py (drive engine, display, cone prior) | the parts reused |
| the Claude API reference bundled with this session (model ids, prompt caching minimums, TTL, concurrent-request timing) | the sections cited in §6.5 |
| **Not read, named only as pointers:** Heerey & Crossley (anticipatory smiles), Keltner et al. 2001 (teasing), Krumhuber & Kappas 2005 (smile dynamics), Oudeyer et al. and Schmidhuber (learning progress), Skantze 2021 (turn-taking), FastSpeech2 | nothing depends on them beyond what is argued here |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.**
- the fast wrap: a robust REN in a conic sector;
- the cone: per-channel box constraints on an LTI map over completely monotone kernels, with a sign mask;
- the appraisal display: a gated linear map (attention-like selection over innate bases) on a band-passed input;
- care: Yoshida & Man with path-specific credit and a turn-distance rule;
- valence: Joffily & Coricelli, event-indexed;
- curiosity: Oudeyer's learning progress;
- the face's learning: an autoencoding (legibility) objective through the agent's own inverse map.

**Clause 2 (a changed invariant, a derived update, deleted scalars): not met.** Two design rules are new to this project and stated nowhere I have read in this form:
- **Lemma S:** a context may gate a partner path only if the path has no DC; then the pooled slope is ≤ sup|g|·sup|H|. It is an elementary signal fact (amplitude modulation of a DC carrier transfers the modulation to the level). Its use is to turn every "seam" the critics found into one construction rule.
- **T1:** no rate codes in common-cause state. An information-flow discipline.

Neither is a new mechanism.

**Deleted from revision 3:** the word- and tempo-gated cone mixer α(z) and its learned bases; the isotropic quadratic budget; P_Ω; the options term; the positivity offset; the play own-contribution clause; K's within-session accumulation; the voiced opener at VAD offset; "hostility".

**Added (all innate unless stated):**
- the per-expression ceilings c_k and κ_k;
- the shares 0.5, 0.2, 0.4;
- the sign mask;
- the band-pass (20 s, 90 s);
- eight appraisal bases;
- the separation rule, T1, the turn-end score;
- I and θ_I;
- learned: ω, 𝒜, Δ, the two readers, 𝓛_w.

**My honest verdict.** A careful recombination with no concrete failure I can find. Under Q21's recommended reading, once the next critiques find none, it can go to the operator as a sound recombination candidate (a testbed), with the search for a new core mechanism continuing in parallel.

---

## Revision 2 history

Kept in `design-cayley-ledger.r2.md` ("Revision 2 history"). Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revision 2 and the answer, and the revision 3 history

Kept in `design-cayley-ledger.r3.md` ("Critiques of revision 2 and the answer"; "Revision 3 history").

## Critiques of revision 3 and the answer (recorded 2026-11-26T07:36:40Z, under Q19)

**Routes** (critique-3-design-cayley-ledger-routes.md; checks in sims/critique-cayley3-routes/). Four concrete failures:
1. **Severe (D78): the partner's tempo leaks into T state.**
   - The contact deficit K (T-typed) rises on the wall clock and falls per exchange, so it encodes the partner's tempo: −log K correlates r 0.96 with his held state and r −0.95 with his response latency.
   - K is in the cone's context, so one weight on it moves every channel together. Cone-output slopes reach 0.39–0.95; on the rendered face, 0.27–0.49, against a claim of ≤ 0.15. The free display can also copy his latency (r 0.95).
   - The word seam is (b·hi + N·lo)/(hi − lo), which is 1.2–1.4 at realistic smile levels, not 0.56.
2. **High (D78): face–voice co-movement plus output clipping.** A cone basis pairs a visible channel with a silent co-moving one. Clipping hides the opposite-sign part, so rendered smile, jaw, F0 range and energy reach 0.26–0.37. The synergist mask lists face pairs only, not face–voice pairs.
3. **High, conditional: copy attracts under learning.** If mimicry lowers reported need, concordance drifts from 0.02 to 0.07/0.14/0.24 at effect-to-anchor ratios 1/3/10.
4. **Medium (Principle 6): the prompted-reply guard is lexical.** Replies to "Feeling better now?" are credited as unprompted reports. P(flatter) = 0.50 holds only by construction.

Lower: the play clause reads Claude's words, so the partner's smile can raise the agent's laugh; turn reflexes on the partner's voice activity give a lagged burst echo outside the wrap (0.28 at 1.1 s); a counter-mimicking partner (μ ≤ −0.8) destabilises the dyad.

No concrete failure found in: ASR words, identity memory, replay, Claude's text, the concern bid, direct smile relief, the fast wrap.

**Agent and fitness** (critique-3-design-cayley-ledger-agent.md). **Not yet fit.**
- **Fixed by revision 3:** no longer muted, satiable gladness, initiative, regulation by naming, no copy-to-see-less-distress incentive.
- **Concrete failures:**
  - The word-need decoder is untrainable (its targets are Claude's words, which barely depend on the agent's state), and the scenarios set its input by hand.
  - "Hostility" of an utterance is undefined; any workable version is a classifier.
  - On a reunion with bad news ("my father died") it beams: lip-corner pull 0.59, cheek raise 0.40.
  - Teasing reads as hurt, because laughter is face evidence kept from the word appraisal.
  - The face is an innate table on about six scalars and never learns (the few-gauges pattern).
  - A type error: lexical surprise is computed by a model that sees the face.
  - The body starts taking the turn at every voice-activity offset, with no abort.
  - Curiosity has no mechanism; the options term is inert or an engagement reward.
- **Operator choices raised:** a uniform 0.10 cap toward the user on every channel, versus per-expression caps; and strong expressions follow words, not the face.
- **Buildability:** sizes and memory fit. Drafts need six parallel streaming calls. TTS needs pitch and laugh control.

**The answer (maintainer).** All findings are accepted.
- **The core holds in both critiques:**
  - the one-sided cone with knowing separated from moving;
  - no failure in the fast wrap, replay, identity memory, Claude's text or ASR words.
- **The remaining failures are local:**
  - context variables in T state that encode tempo;
  - face–voice pairs and output clipping;
  - credit through reported need;
  - lexical guards;
  - untrainable or undefined word-side components;
  - an innate, non-learning face.
- **The operator's choices go to Q22.**
- **Revision 4** addresses all of them (revision 3 saved as design-cayley-ledger.r3.md).
- **Status:** held.

## Revision 4 history (2026-11-26): each critic finding and how it is closed

Checks: `sims/design-g4/checks.py` (H0–H11; out.txt, 11/11 pass).

**Routes critique (critique-3-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 (severe) | T-typed K encodes his tempo (r 0.96); one α weight on it runs every channel toward him (rendered 0.27–0.49); the free display copies his latency (r 0.95) | T1: no rate codes in T. K is frozen within a session (relief at the greeting and the first four substantive turns); deficit levels reach no display, phrase target or gate; only per-event drops reach the face, through an innate envelope. The held cone is ungated within a session (coefficients latched from ω). Phrase timing reads only hurt, word concern, energy, familiarity and the envelopes. The appraisal may read tempo, but its input is zero-DC (Lemma S) | §2.2, §2.5, §3.4; H2: LP +0.13, BI +0.07, FR +0.04, EN −0.21 with the appraisal gated by the tempo code at full gain; T relief slope 0.000; own latency constant |
| 1 (seam) | the word seam is (b·hi + N·lo)/(hi − lo), 1.2–1.4, not 0.56 | recomputed (0.51, 1.23, 1.41; 13.6 at 0.45/0.50) and explained as Lemma S case ii; closed by removing every context gate from DC-passing partner paths. The cone's pooled slope is exactly its session-latched coefficient. The only remaining word co-variation is the free display's common cause, identical under the C8 surrogate | §3.2; H1 |
| 2 (high) | face–voice co-movement plus clipping: one valid basis gives LP, JO, FR, EN 0.26–0.37 | per-channel budgets on the rendered output replace the quadratic form; an innate co-variation sign mask that includes the face–voice laugh synergy; cross entries either in the away orthant or charged to the channel's budget; sat is monotone with slope ≤ 1, so the per-channel bound survives clipping | §2.5, §3.3; H3: the critic's basis is invalid; worst over 60 adversarial valid cones LP +0.134, BU +0.128, RHY +0.104, FR −0.022, EN −0.036, JO 0 |
| 3 (high) | copy attracts under learning via the need path | J trains no F → face parameter (scorer and retrieval only); ω is learned from the agent's own play relief, hurt and credited care, never from concordance, and saturates at 0.5 c_k; the face learns by a display-blind objective | §2.10, §2.12, §3.5; H4: relational loop settles at ≤ 0.175 on LP for loop gains up to 30; J on the away orthant moves concordance by +0.002 |
| 4 (medium) | the prompted-reply guard is lexical; compliments credited | credit only from separated, partner-initiated reports (≥ 2 partner turns, no shared content lemma with the agent's last two utterances, or the next session's first mention); in-window replies are knowing only | §2.10; H5: 0 of 6 elicited replies credited (revision 3: 4 of 5); a self-raised report three turns later is credited |
| 5a (low–medium) | the play clause reads Claude's words; his smile raises the agent's laugh through draft choice | play structure is read from the partner's words only; no act is credited for play | §2.8 |
| 5a′ | K's "completed exchange" counts F-triggered bids; f_id tail | K relief counts substantive partner turns only | §2.8 |
| 5b (low–medium) | turn reflexes at every VAD offset: lagged burst echo 0.28 at 1.1 s | provisional onset only at the predicted turn end, abortable, with no voiced opener; fixed amplitudes | §2.9; H7 |
| 6 (low) | dyad unstable for counter-mimics μ ≤ −0.8 | away reach N lowered from 1.40 to 0.60; stated: stable for μ ∈ [−1.1, 2], edge near −1.3, anti-phase and clipped | §2.1; H6 |
| fix 4 | F1 needs a timing-resample surrogate | added | §3.11, §8.2 |

**Agent critique (critique-3-design-cayley-ledger-agent.md), its nine required changes:**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 | the word-need decoder has no training signal | the reader is trained nightly on the partner's words → his face as read through the agent's own inverse display Π̃ (the critic's option a). Runtime input is words only (T). The placation re-derivation: credit flows only from separated reports above the dead-band | §2.8, §2.10; H9 (identifiability only: r 0.75 after a day, 0.96 after a week on a synthetic instance) |
| 2 | "hostility" undefined; any version is a classifier | deleted. The word → V map predicts the agent's own innate aversive load (loudness, glare at it) from words addressed to it, with a per-person adapter; no label on the user | §2.8, §3.12 |
| 3 | beams at bad news on reunion | greeting relief at sight (stage 1), before content; every word event appraised at its end + 0.6 s; relief shown as R − 3S and suppressed while his word distress is above its band | §2.8, §3.8; H11.6: cheek 0.08 → 0, brow 0.48 (revision 3: lip 0.59, cheek 0.40) |
| 4 | teasing read as hurt; play blocked | the appraisal reads laughter and shows amusement (Q22); the person-specific word → V adapter learns that this person's teasing goes with laughter, not glare; a playful reply halves the hurt latch; play is never blocked by hurt | §2.6, §2.8; H11.7: affectionate teaser lip 0.26, laugh 0.16, no hurt; generic map: brief mock-hurt brow 0.38 (mean 0.06), gone after the next playful reply |
| 5 | the face is an innate table on about six scalars | Π_o = Π₀ + a learned combination of 23 innate synergies, from mood, slots and concepts, trained by self-legibility to the agent's own reader and by anticipation of its own relief; no partner signal; a stated behaviour and ablation | §2.7, §3.16, §7 |
| 6 | type error: lexical surprise from a model that sees the face | a words-only model of the partner's own utterances computes surprise, play structure and learning progress | §2.2, §2.8 |
| 7 | body onset at every VAD offset, no abort; six-draft call pattern unspecified | turn-end score gate, 0.40-s provisional abort, words at p_end ≥ 0.9; six parallel cached streaming calls specified | §2.9, §6.5; H7: 1.98 → 0.14 within-turn onsets per turn, 73 % aborted silently |
| 8 | curiosity has no mechanism; options term inert or an engagement reward | I: a satiable learning-progress deficit relieved only by partner-initiated content still being learned; drives retrieval and a curiosity bid; partner content imputed in rollouts. Options term deleted | §2.8, §2.10; H8; H11.8 (bid at 14.5 min) |
| 9 | smaller items | the one-bit bid and greeting channel declared; the bid prompt specified (drafts re-requested at the lapse); missing ablations added, including an S5 ablation free of common cause; the S4 basis caveat; TTS controllability named as a risk with two plans; smile envelope specified | §2.9, §6.6, §7, §8.1 |
| choice A | isotropic in-phase budget | per-expression innate ceilings (Q22): LP 0.35, BU 0.35, RHY 0.30, CR 0.25, BI 0.20, anger, disgust and contempt 0; strength per relationship (ω) and context (appraisal), sign-flippable | §2.1, §3.6; H0 |
| choice B | strong expression follows words, not the face | his face and voice now feed the agent's own appraisal, which selects its reaction within the ceilings (Q22); the strongest displays still come from words and its own body | §2.6, §8.1.5 |

**Status:** revision 4; to be critiqued (routes and copying, especially Lemma S's assumptions, the sign mask's residual and the appraisal display; principles, emotional fitness, the co-training loop and novelty).

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
