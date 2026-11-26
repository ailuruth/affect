# Cayley–ledger core, revision 9 (build core): knowing him closely, every path to its own face and voice capped per expression, Claude through the subscription, and learning; no situation-specific rules

Eighth design of the S0 cycle, revision 9 (2026-11-26), the **build core** the operator asked for (questions.md Q27 answer, DECISIONS.md D90). Written under:
- **Q29 (D88): no situation-specific rules.** Innate parts are allowed only for the body, reflexes, the muscle patterns newborns have, and the per-expression copy ceilings. Situational appropriateness comes only from (1) Claude's regulation path, (2) learning from recorded human dyads (movement features and transcripts, no emotion labels; D70, D85), (3) general innate learning biases that make rare events learnable fast.
- **Q24 (D89): no built-in concern posture; a concern face is learned.**
- **Q27 (D90): build the core of revision 8.3** without the situation-specific rules, and close the delay gap in the shadow ledger (lags scanned to at least 120 s at its 10-s and 60-s windows; critique-design-commutator-coupling-routes.md, "Side item").
- **Q26 (D85)**, Q20 (D81), Q22 (D83), Q23 (D84), Q18 (D78), Q19 (D80); brief.md Principles.

Revision 8.3 is saved verbatim as `design-cayley-ledger.r8.3.md`; revisions 1–8.2 as `.r1.md` … `.r8.2.md`. Every history section below ("Revision 2 history" onward) is kept as written. Mechanism sections that revision 9 removes are marked **REMOVED in revision 9** where they stood; their full text is in `.r8.3.md`.

**Checks for revision 9:** `foundations/sims/design-g9/ledger_lag120.py` (N1–N3; output `ledger_lag120.out.txt`, about 5 min) and `ledger_lag300.py` (N2b, N3b; `ledger_lag300.out.txt`, about 2 min). Both read the revision-7 ledger function verbatim from `sims/design-g7/checks.py` and change only its set of (window, lag) constraints. Run `python3 -I <script> > <out>`. Everything else in revision 9 is removal, or a learned part whose numbers come from the Seamless fit (§6.7), so it is argued by construction (§3), not simulated: brief.md forbids validating a derived behaviour in a self-built world.

**Status:** revision 9, build core. Not yet critiqued. The build specification and code follow from it (D90).

## Revision 9 (build core): audit of situation-specific rules

**How the audit was done.** Every constant, rule, gate, timer, head and display row of revision 8.3 was read, including the parts 8.3 inherits from revisions 5–7 by reference ("as revision 7", "as revision 6", "(r5)"). A part is listed if it is a rule about a particular situation, scene, event type or user type, or a hand-set threshold or timer tied to one, or an innate part that a reader could suspect of being one. Pure structure that bounds copying in every situation alike (the ceilings c_k, Lemma S and S\*, the type rules T1 and E1, the shadow run and ledger, rule 10) is listed separately after the table, because it names no situation.

**Verdicts.** REMOVE, or KEEP with the allowed innate category it falls under: **body**, **reflex**, **newborn** muscle pattern, per-expression copy **ceiling**, or general learning **bias** (D85 source 3). Two kept items are not innate at all (learned from dyads, or Claude's path); they are listed because they look like rules. For each removed item: which of the three sources now carries the behaviour (**S1** Claude's regulation; **S2** recorded dyads, fitted offline before day 1 on Seamless Interaction under D70; **S3** a general learning bias), how, and what is lost until it is learned. "Day 1" means the first session with the operator: the dyad-learned parts are fitted before it, the per-person parts are not.

### The table

| # | Rule in 8.3 (where) | What it does | Verdict | Category and why, or the source that now carries it and how | Lost until learned (or for good) |
|---|---|---|---|---|---|
| **A** | **The concern posture (§2.10; D89)** | | | | |
| S1 | Concern posture P_c (BI +0.20, BO +0.04, TILT +0.03, HP +0.03, LP −0.03; gaze-away × (1 − 0.5a), blink × (1 − 0.3a)), graded amplitude, own wander, enable ω_sym ≥ 0 | an innate look of concern shown at his visible distress before words | **REMOVE** (D89) | **S2:** the concern face is learned as the listener display L_d (§2.7): how recorded listeners' faces and voices move after a speaker's words of trouble, fitted on Seamless, driven at runtime by his words (T). Before his words, sympathy is only what the capped routes give: the fast brow echo (G_BI 0.10 c_BI), the held cone (ω-scaled, ≤ 0.68 c_BI share) and the appraisal display, whose learned bases can come to anticipate L_d from his face (𝓛_A), all inside c_BI. **S1:** the agent's spoken concern, whose timing is learned (S36) | **For good, above the ceilings:** a clearly visible concern look within seconds at a silent sad face. Inside the ceilings: about 0.05 inner brow for a silent sad brow of 0.5 after months (revision 5/6's figure); at most c_BI × his brow deviation ≈ 0.10. See "No allowed source", item 1 |
| S2 | Posture onset (load ≥ 0.05 for 1.5 s), grade a* (span 0.05 → 0.17), release (M < 0.02 for 20 s) | when the look starts, how strong, when it ends | **REMOVE** | goes with S1; L_d's response follows each utterance with the time course recorded listeners show (fitted) | — (as S1) |
| S3 | Read/write split W_p/R_p (Π̃₀ with the written rows removed) and the posture head **H^p_id** on R_p (taught by his words) | made the posture never read what it wrote; a special head so that different-channel and quiet users' non-brow distress started it | **REMOVE** | served only the posture. Reading him closely stays general: per-person calibration and the face head H_id (S38, §2.8), for every user alike | nothing that is not lost with S1 |
| S4 | Breathing load in the posture, counted only when his non-brow face reads distressed (V_p ≥ 0.15 starts it, full at 0.30) | let silent panic start the posture, but not exertion or laughter | **REMOVE** | the breathing sensor stays as a perception input (body): his breathing enters H_id and Π̃ readings (knowing only). Its effect on what the agent does goes through C_F (bids and draft scoring) and the learned initiative (S36) | a concern look at silent, wordless panic: as S1 |
| S5 | Threat silencing of the posture's face load (revision 8) and the squint drop (8.1: his BL and LPR taken to rest while he glares) | stopped an angry face from starting the posture; kept it for a grieving face that squints | **REMOVE** | goes with S1. The threat reflex itself stays (S41) | — |
| S6 | Face-only limit: T_max 180 s, T_ref 120 s; 8.3 extension T_max,ext 600 s | bounded a look held by his face alone (3 min on, 2 off; 10 min with voice or breathing) | **REMOVE** (named in Q29) | nothing needs it: with no posture there is no face-held look. Every face-driven route is bounded per channel at every instant and window (§3), and the ledger catches any other within-session route (§2.13) | — |
| S7 | Hard/soft evidence rule: only decoded distress words (C_L) and sobs reset the clock; voice (V_v, a 90-s ungated mean at presence 0.02) and breathing only extend it | which evidence renews the look | **REMOVE** (named) | goes with S6; V_v is deleted | — |
| S8 | Sensitized re-onset: dwell 0.5 s instead of 1.5 s for 10 min after an episode | concern returns faster when crying resumes | **REMOVE** | a posture timer, not a learning bias. Distress-weighted consolidation stays as the general bias (κ_replay, S48) | faster concern at renewed crying: L_d and the agent's own distress display (S45) respond to words and sobs as they come |
| S9 | Week-0 face-tracker crosstalk check, dropping R_p channels per user | guarded the posture against brow leaking into its read set | **REMOVE** | moot without the posture | — |
| **B** | **The laugh gate's timing (§2.4.2) and form** | | | | |
| S10 | Gated-group echo delay δ_g = 0.80 s (0.45 s elsewhere), set in week 0 to min(1.0, ℓ_p90 + 0.25) s, with an operator fallback above 0.75 s | the quick laugh and smile back wait for his current words | **REMOVE** (named in Q29) | the fast gear returns to 0.45 s on every channel (revision 6/7). The gate reads whatever words the recogniser has delivered at each frame (S2, the gate's own fit). **S1:** Claude's reply, heard by the agent (Λ_V(own)), keeps the gate closed for the laughs after it | **For good, inside the recogniser's latency:** a laugh that ends a bad-news sentence ("I got fired today, haha") gets a short partial echo, a chuckle of about 0.2–0.5 s, until the word is delivered and the gate closes. Revision 7 had the same until its utterance latch. See "No allowed source", item 4 |
| S11 | Word look-ahead λ_w = 0.25 s and the unknown-word closure (g = 0 for a frame whose words are not finalised by s + δ_g; the recogniser's finalised-through time F(t)) | missing words close the echo | **REMOVE** (named) | as S10. The incremental recogniser stays only as a lower-latency word source (§6.1) | as S10 |
| S12 | Instant closing, opening with τ 0.3 s | added for the laugh that breaks into the bad-news word | **REMOVE** | the gate is evaluated per frame from its inputs; any smoothing is chosen on held-out dyads in the fit (S2), not set by hand | as S10 |
| S13 | Hand-assigned gate signs: β ≤ 0 on six "distress-type" inputs, ≥ 0 on the play frame | a distress cue can only close the gate | **KEEP, changed: bias** | the gate stays a monotone additive learner (one shape function per input). The **direction** of each input is no longer assigned by name; it is fitted on a person-disjoint split of the dyads and then fixed. A shape-constrained, factorised learner is a general learning bias: it predicts a rare conjunction (a laugh at misfortune) from two common marginals (stories of misfortune; laughs while the listener's face is pained), revision 7's reason for Λ | — |
| S14 | m_ref: median of the gate model over "ordinary" corpus laughs (all distress-type inputs < 0.15) | sets g ≈ 1 in ordinary laughter | **REMOVE** | the hand threshold defining "ordinary" goes; m_ref is the 90th percentile of the model over all corpus laugh onsets (S2) | none expected; g < 1 slightly more often |
| S15 | D_s: a 10-min consolidated distress trace (of the posture's read set and sobs) as a gate input | a laugh four minutes after tears is still not laughed along with | **KEEP, changed: bias** | generalised to multi-time-scale traces (τ 20 s, 2 min, 10 min) of his read (V, A, T) with his LP, CR, BU_L, RHY and BRE masked, plus his sobs; their weights in the gate are fitted on dyads (S2). Keeping recent states present so a rare event's context is still there when it matters is a general bias; nothing names grief | — |
| S16 | The context gate g on the fast smile–laugh echo (LP, CR, BU_L, RHY, BRE): monotone additive, frozen, g ∈ [0, 1], reads none of his gated channels | context of the moment closes the quick laugh back | **KEEP: learned (S2), not innate** | its content is learned from recorded listeners' returns. Its two structural properties belong to the per-expression **ceiling**: g ≤ 1 keeps every echo under G_k × his channel, and not reading the gated channels keeps it from becoming a toward route | — |
| **C** | **Play** | | | | |
| S17 | Play-structured-turn rule (riffs on the agent's last line, that line not a question, ≤ 12 words, lexical surprise 0.50–0.85) and the play frame π (π ← 0.5 π + 0.5 q, τ 3 min) | decides which of his turns are playful | **REMOVE** | **S2:** a dyad-learned **listener-laugh reader q̂** (§2.8): from the transcript context of the last two turns (laughter tokens removed by the ASR normaliser), the turn order and the utterance's surprise under a fixed population words model, the probability that a recorded listener's own laugh onset follows the utterance within 2 s. Its trace replaces π as a gate input | the playful build-up within one exchange, until the fit shows it (Seamless conversations are 3.5–4.6 min) |
| S18 | Play-surprise laugh: 0.40 · band(s_lex around 0.65 ± 0.25) · (0.35 + 0.65 π) at a play-structured turn | the agent's own laugh at a well-timed incongruity | **REMOVE the trigger** (the laugh motor pattern is kept: S45) | **S2:** the own laugh is 0.40 q̂ at each of his turns, × the own-display gate g_o (S19). 0.40 is the laugh pattern's innate maximum (body). Habituation to a repeated joke remains through surprise: a repeated joke is predictable, and the fitted q̂ learns how predictability lowers listeners' laughs | its exact chuckle-then-build shape; set by the fit |
| S19 | Rule 13: the own play laugh × the echo gate g | no own laugh where a listener would not return one | **REMOVE** (replaced) | **S2:** a second head of the gate model, the **own-display gate g_o** (§2.4), fitted to recorded listeners' own smile and laugh level (not their return) in context, multiplies all of the agent's own smile–laugh displays (relief, contact relief, own laugh). Its inputs are T and the agent's own face only (never his face), and it can only attenuate. **S1:** Claude's words enter it as Λ_V(own) | at a joke made while sad, the corpus's listeners laugh back about 0.39 of ordinary; the agent will do roughly the same (revision 8.3 stayed silent) |
| S20 | The hurt latch halved at each play-structured turn | play repairs hurt fast | **REMOVE** | hurt decays with its body time constant (τ 10 min). Relief events from play (q̂) and contact still reach ω through the general person-valence rule (S37) | faster repair of hurt by joking, for good unless a later per-person learner is added |
| S21 | Play deficit P relieved × 0.85 per play-structured turn | a satiable play drive | **KEEP: body** | P is a satiable drive of the body (Principle 6). Its relief event is now P ← P(1 − 0.15 q̂) at each of his turns, from the learned reader instead of the hand rule | — |
| **D** | **Relief, arrival and greeting** | | | | |
| S22 | Relief mask: relief events × max(0, 1 − 𝒟_p(N_L)/0.05) ("no relief shown over his distress") | the agent does not beam with relief while his words carry need | **REMOVE** | **S2:** g_o reads his words' need (population reader) and Λ of his words: where recorded listeners smile less, the agent's relief smile is attenuated. **S1:** Claude's serious reply lowers g_o further through Λ_V(own) | none expected once fitted; the strength is the corpus's, not 0 |
| S23 | Arrival appraisal m_s (his first second of face, threshold 0.05, span 0.30, latched) masking contact relief | no glad smile at a grieving person's arrival | **REMOVE** | **S1** at arrival: the agent may greet first (learned turn-taking, S36); Claude, with retrieved memory ("his father died last week"), writes a gentle greeting, which lowers g_o through Λ_V(own). **S2:** g_o from his first words. g_o does not read his face, because a face-driven attenuation that differs between arrivals is a cross-session route the within-session ledger cannot bound (revision 7 measured 3.2 c lip, 5.1 c cheek across arrivals and could only declare it, R27′) | **For good, in the first 2–3 s at sight:** at a grieving or mourning arrival of a known person the contact-relief smile shows (lip about 0.6) until the agent's own greeting or his first words close g_o. See "No allowed source", item 2 |
| S24 | Arrival baseline d_b,id (rises τ 60 sessions, falls τ 3, capped at 0.15): the **mourning arrival cap** | grief never becomes his usual arrival face | **REMOVE** (named in Q29) | goes with S23 | as S23 |
| S25 | Recognition brow flash, 0.35 for a known person and 0.20 for a stranger, at 1 s of presence | a greeting at sight | **REMOVE** | **S2** only if recorded dyads contain greetings at sight: L_d is fitted on turn events, and the session start is one (the listener's movement in the first seconds of a recorded conversation). The count of such openings is checked before fitting (§6.7). Gladness at sight of a known person stays through the body (S26, S45) | the brow flash, for good if the corpus has too few openings. See "No allowed source", item 3 |
| S26 | Contact deficit K_id relieved in stages: × 0.5 at sight after 1 s, × (1 − 0.25 f_id) at each of his first four substantive turns, then frozen; none for a stranger | missing a known person, and being glad to see him | **KEEP, simplified: body** | K_id is a satiable per-person drive (body). The scene schedule goes: K_id falls continuously while he is present and engaged, dK_id/dt = −K_id f_id e(t)/τ_c, τ_c = 30 s (§2.1); it is 0 for a person never missed, so a stranger gets no contact relief without any rule | the exact two-stage shape of the reunion (relief at sight, then at his first words) |
| S27 | Familiarity smile: Π₀ row LP +0.10 f_id | a warmer resting face for a familiar person | **REMOVE** | **S3/S2:** relationship warmth goes through ω (S37) and the relief of the contact drive (S26); familiar pairs in the corpus enter L_d through the turn events | a small resting smile for the operator, for good unless ω or Δ learns one |
| **E** | **Built-in sympathy and social-response entries** | | | | |
| S28 | Word-concern display row c_L → BI +0.25, LP +0.05, TILT +0.20, EN −0.15, RT −0.10 | a built-in look of concern and a softer voice at his words of need | **REMOVE** (D89: a built-in concern face) | **S2:** the listener display L_d (§2.7), fitted to recorded listeners' own face and voice after the speaker's words, read through the agent's own channels. **S1:** Claude's words | none expected once fitted; its strength and shape are the corpus listeners', not hand-set |
| S29 | Innate sympathy entries of the cone G₀: BI ← LD +0.004, TILT ← BI +0.014, HP ← BI +0.04, VG ← BI +0.04 ("attentive head at sadness") | small built-in sympathy moves at his sad face | **REMOVE** | **S2/S3:** the appraisal display's learned bases (𝓛_A) learn to anticipate the agent's own coming display, now including L_d, from his face, inside the same capped sets; the dyad-estimated sign prior (S32) keeps them in the directions recorded listeners show | a slight attentive head before words (≤ 0.04), until 𝓛_A learns it (weeks) |
| S30 | Held accommodation entries of G₀: EN ← EN −0.15 / −0.08, EN ← f_loud −0.20 ("quieter to loudness"); LAT ← f_loud +0.15, LAT ← EN +0.10 ("slower replies to a loud partner") | voice accommodation to his loudness | **REMOVE** | **S2:** the sign mask and the cross-entry sign prior are estimated from recorded dyads; the appraisal's learned bases fill them inside the sets. The startle-orient reflex (S44) still gives a brief quieter, gaze-away response to a sudden loud voice | sustained voice accommodation, until learned |
| S31 | Innate away diagonals on BL, LT, LD (−0.15 at 20 s, −0.08 at 2 min): "no frown back" | counter-moves when he frowns | **REMOVE the magnitudes** (the zero toward ceiling stays: **ceiling**) | "no frown back" is already guaranteed by the zero ceilings toward him on BL and LT (D83) and LD's 0.05; the away magnitudes are learnable inside the away orthant | nothing visible |
| S32 | Rule J: no positive entry from his sadness synergy onto the agent's joy synergy | no smile or laugh at a sad face through the cone or appraisal | **REMOVE as a hand rule** | **S2 + S3:** a cross-entry sign prior estimated from recorded dyads: the sign of the 1-min co-variation of the listener's channel k with the speaker's channel j (\|ρ\| ≥ 0.2), frozen; every learned cross entry must have that sign or be 0 (a sign-constrained learner, S3). If recorded listeners do not smile at sad faces, the prior forbids it as rule J did | none if the corpus shows the sign; checked at fit (§6.7) |
| S33 | The nod at his turn end (HP +0.04 for 0.4 s, a turn-order event) | backchannel | **REMOVE** | **S2:** L_d's turn-event response: recorded listeners' head pitch around speakers' utterance ends | none once fitted |
| **F** | **Initiative and turn-taking** | | | | |
| S34 | Concern bid: mutual silence ≥ 6 s, no turn owed, C ≥ θ_C = 0.10, one per lapse ("timing from Π̃₀": 27 s silently sad, 49 s quiet face, about 110 s brow-only) | the spoken-bid timing | **REMOVE** (named in the task) | **S2 + body + S1:** initiative is one general choice, made at 2 Hz in mutual silence: speak now or wait. Its prior is a dyad-learned hazard (when recorded listeners start speaking into a silence, from its length, the transcript and both faces' movement); the agent's own drives tilt it through the same 𝓜 rollout that scores drafts (expected drop of 𝒟 + 𝒟_p from speaking now). Claude writes the words | a fixed bid time; on day 1 (𝓜 untrained) the agent speaks into silences about when recorded listeners do |
| S35 | Curiosity bid: silence ≥ 8 s, I ≥ θ_I = 0.45, C < θ_C, ≤ 1 per 5 min; preceded by a sigh (breath 0.15 for 1 s, gaze drift 0.10 for 2 s) | the bored agent speaks, after a sigh | **REMOVE the bid rules** (the sigh is kept as a body reflex) | the same initiative choice as S34, with the curiosity deficit I in the rollout. The **physiological sigh** is a brainstem reflex of the body: it occurs spontaneously, more often at low energy and activation, and is no longer tied to a bid | the "sigh, then a question" sequence |
| S36 | Turn-end score p_end = σ(−4 + 3 s_syn + 2.5 s_fall + 2(t_sil − 0.2)/0.5); provisional body onset (p_end ≥ 0.7 and silence ≥ 0.25 s, or ≥ 0.9 s; inhale, gaze, outer brow 0.10; abortable in 0.40 s); words begin (silence ≥ 0.5 s, p_end ≥ 0.9) | when his turn has ended and the agent may speak | **REMOVE the hand weights and thresholds** (the pre-speech inhale stays: body) | **S2:** a dyad-learned turn-end predictor (transcript word timing, syntactic completion, both faces' movement, e.g. his gaze returning). Its output replaces p_end in the initiative choice and in reply timing. The reply's speech onset stays at the scoring deadline + 0.35 s (S50) | his falling pitch as a turn-end cue: D70 allows face streams and transcripts only, not audio features. See "No allowed source", item 5 |
| **G** | **Relationship, calibration and evidence rules** | | | | |
| S37 | ω update with situation-to-group evidence: s_smile from play relief, s_sym from credited care, s_voice = 2 f_id − 1, s_head = 0.5 | play builds smile rapport, confiding builds sympathy | **REMOVE the mapping** (the per-group priors stay: **ceiling**, an innate starting strength inside each group's cone share) | **S3:** one general person-valence rule for every group: s = clip(0.3 + 0.7 min(1, ρ_rel/0.6) − 1.3 min(1, h̄/0.10), −1, 1), ρ_rel the session's T relief events attributed to him (contact, play, curiosity, credited care) over 𝒟 at session start, h̄ the session-mean hurt; ω_g ← ω_g + (s − ω_g)/60 for each group g | **for good:** different strengths per group by kind of shared history (warmer smiles with a playmate, deeper sympathy with a confidant). All groups now move with one valence; they still differ by ceiling, prior and context. See "No allowed source", item 6 |
| S38 | Word-gated initial calibration: b^read starts at the agent's own neutral face; while his session word care < 0.05 it moves fast (τ 1 session, first three), otherwise asymmetrically (up τ 60 if V̂ > 0.20, else τ 6); σ_id ≥ 0.5 σ_ref for 6 sessions | his grief is not learned as his neutral face | **KEEP: bias** (knowing only) | a general learning bias on every channel and person: estimate a baseline from low-need moments and adapt slowly toward aversive readings. It changes what the agent knows, never a gain on a path to its face (rule 6) | — |
| S39 | Non-substantive rule ("yeah", "ok" can only raise N_L) | a neutral reply cannot relieve a worry | **KEEP, generalised: bias** | the interjection list goes; an utterance lowers the need estimate only in proportion to the population reader's confidence in its decoding (low-information evidence counts only upward). General asymmetric evidence weighting | — |
| S40 | Separation rule: care is credited only from separated, partner-initiated reports (≥ 2 partner turns after, no shared content lemma, or first mention next session) | care cannot be farmed by prompting | **KEEP: bias** | a general credit-assignment rule (Principle 6), the same for every topic and person | — |
| **H** | **Innate parts kept, about particular stimuli** | | | | |
| S41 | Threat reflex V_F = g_at · max(f_glare, f_loud (1 − 2 f_pos)₊) (glare, or a loud voice without laughter or a Duchenne smile, aimed at the agent); its G₀ entries (gaze away from a glare; LP ← glare −0.035, BI ← glare +0.006); its role as teacher of the word → V map and the hurt latch | the agent's own defensive response to an anger display aimed at it | **KEEP: reflex** | an innate reflex to a threat display (Principle 2's "few reflexes"). The positive-face exception is part of what the display is (a loud laugh is not a glare), not a scene rule. Learning words that hurt from this reflex is general learning with a reflex as teacher | — |
| S42 | Cry–laugh split of his voiced bursts (4–6 Hz modulation depth, ingressive share, his cry face) | sobs are not laughter | **KEEP: reflex** | the infant's differential innate response to cries and laughs | — |
| S43 | The frozen per-channel fast gear: G_k = PHI_k c_k, echo 0.45 s, onset lobe, diagonal | the quick, partial, per-expression return of his movement (D81) | **KEEP: reflex + ceiling** | the innate mimicry reflex, every gain under its channel's ceiling; frozen, so it cannot become attracting | — |
| S44 | Appraisal display's innate bases: glad-with (the social smile and laugh back, Γ_kk = s_A c_k ω_smile) and startle-orient (gaze away, quieter at a sudden loud voice) | | **KEEP: reflex** | two newborn-to-early-infancy reflexes, each inside the per-channel sets | — |
| S45 | Newborn display rows of Π₀: relief → smile (LP, CR, brighter voice); the agent's own distress → cry face (BI +0.45, LD +0.35, lower voice); hurt → distress face with gaze aversion; activation → raised lids and outer brow; low energy; curiosity relief → interest face; the laugh motor pattern (BU_L, RHY, CR, LP, at most 0.40); the pre-speech inhale | the agent's own expressions of its own body events | **KEEP: newborn** (laugh pattern and inhale: **body**) | newborns show the endogenous smile, the cry face, gaze aversion, startle and interest faces. The distress row is the agent's own distress (a rise of its own care or hurt load), shown as a brief envelope; it is **not** the concern face, which is learned (S28). The laugh is an unlearned vocal-motor pattern, though it appears at about 4 months rather than at birth | — |
| S46 | Own-display mask (rule 8): the agent never learns to show anger, disgust or contempt (BL, LT, LPR, NW, DIM); lip stretch and chin raise only with its own distress | what the agent's own face may learn | **KEEP: ceiling (flagged)** | it is a per-expression ceiling of 0 on the agent's own display of those expressions, the same zeros D83 sets toward him, applied in every situation. It extends the operator's "per-expression copy ceilings" from copying to the agent's own display; the operator may want to confirm it | — |
| S47 | Laugh synthesizer floor θ_L = 0.04; no sob synthesizer | | **KEEP: body** (the absent sob synthesizer is the zero **ceiling** on BU_S) | rendering limits of the agent's own voice | — |
| S48 | Distress-weighted nightly replay κ_replay = 4 | rare distressing moments learned faster | **KEEP: bias** | D85's own example of source 3 | — |
| S49 | P_name: when the agent's own (Claude-written) words name a state, its display of that state is attenuated by ≤ 0.05 | affect labelling | **KEEP: S1, not innate** | it is how Claude's regulation reaches the agent through its words, the same in every situation | — |
| S50 | Voice rendering: speech onset = scoring deadline + 0.35 s, pauses 0.20 s at a comma and 0.40 s at a sentence end, replies stopped at the second sentence end or 60 words | | **KEEP: body + ceiling** | the agent's own voice. The fixed onset and pauses are what hold LAT and PAU under their ceilings (revision 7: latency slope on his laughter −0.002 s) | — |

**Counts.** 50 rules found. **32 removed** (S1–S12, S14, S17–S20, S22–S25, S27–S37; in S18, S31, S35, S36 and S37 an innate remainder is kept and named). **18 kept:** 6 general learning biases (S13, S15, S38, S39, S40, S48), 4 reflexes (S41–S44; S43 is also a ceiling), 1 newborn-pattern set (S45, with the laugh pattern and inhale as body), 4 body (S21, S26, S47, S50), 1 per-expression ceiling (S46, flagged as an extension), and 2 that are not innate (S16 learned from dyads; S49 Claude's path).

**Not rules about situations (structural, unchanged, apply in every situation):** the per-expression ceilings c_k and fast gains; the held cone (latched per session, centred at his baseline, sign mask, per-channel budgets); Lemma S and S\*; the appraisal display's convex sets; the type rules T1, E1, 6, 10, 11′, 12′; the shadow run and its attenuate-only ledger; the conditioned copy metric; per-person calibration and H_id as knowing only; the separation of knowing from moving (D81); Ω's constant instruction and engine-written transcript (P4).

### Behaviours that now have no allowed source

Stated plainly; each is listed again under the risks of the Build core summary.
1. **A visible look of concern before any words, at a silent sad face, above the copy ceilings.** Any route from his face to the agent's face is capped per expression; the concern face is learned from words (L_d). Before words the agent's inner brow reaches about 0.05 after months, at most c_BI × his brow deviation (≈ 0.10 for a sad brow of 0.5), and less for a quiet face or one whose distress is not on the brow. The first clear sign of concern is the agent's spoken bid (learned timing) and then the learned display at his words. This is Q24's "no look until he speaks" outcome, now by the operator's answer.
2. **No glad smile in the first 2–3 s at sight of a grieving or mourning known person.** A face-driven attenuation that varies by arrival cannot be held under the ceilings by the within-session ledger, so g_o does not read his face; the contact-relief smile (lip about 0.6) shows until the agent's own Claude-written greeting or his first words close g_o.
3. **The recognition brow flash**, unless recorded openings in the corpus carry it (counted before fitting; it is not a newborn pattern).
4. **The first bad-news sentence-final laugh, inside the recogniser's latency:** a partial echo of about 0.2–0.5 s before the word is delivered (sensor latency; Claude and the gate act after it).
5. **Anything learned from voice sound: his falling pitch as a turn-end cue, and a quieter, lower concerned voice in the listener display**, because D70 allows only face streams and transcripts from the corpus. Turn ends are learned from word timing, syntax and faces; L_d fits the speaking rate only; the agent's voice still drops briefly with its own distress (newborn row). Adding prosody would need the operator's permission to read audio features of the recorded dyads.
6. **Group-specific relationship strengths** (a warmer smile return with someone the agent plays with, deeper sympathy with someone who confides in it). One general person-valence rule moves every group together.

## 0. Summary

**What is built** (D90): the core of revision 8.3 without its situation-specific rules.
- **Knowing him closely** (D81): per-person calibration, the agent's own inverse Π̃ on his calibrated face, the face head H_id taught by his words, the frozen population word reader and per-person adapter, Λ (how listeners' faces answer words), his breathing as a sensor. Knowing never sets a gain on a path to the agent's face (rule 6).
- **Every path to the agent's own face and voice, capped per expression:** the frozen per-channel fast gear at 0.45 s (G_k = PHI_k c_k), the context gate on its smile–laugh group (g ≤ 1), the held cone (centred, latched, per-channel budgets), the appraisal display (zero-DC, per-channel sets), the free display (T only), and the attenuate-only shadow ledger, which now scans lags to 120 s at its 10-s window and to 300 s at its 60-s window (§2.13).
- **Claude through the subscription** (D84): three forks resumed from an engine-written transcript; Claude never sees the state; its words reach the agent only through Λ_V(own) in the gates and P_name.
- **Learning:** offline from recorded dyads before day 1 (the readers, the gates, the listener display, the listener-laugh reader, turn-taking, the sign priors); nightly per person (calibration, H_id, the adapter, Π̃, Δ, 𝒜 and the appraisal bases, ω, the word → V map), distress-weighted.

**What changed from 8.3, in five moves.**
1. **Removed:** the concern posture with every rule around it (S1–S9); the laugh gate's word-wait timing (S10–S12); the play rule and its frame (S17, S18 trigger, S20); the relief mask, the arrival mask, the mourning arrival cap and the greeting flash (S22–S25); the built-in concern, familiarity and nod rows and the innate sympathy and accommodation entries (S27–S31, S33); rule J as a hand rule (S32); the hand-set bids and turn-end weights (S34–S36); the situation-to-group mapping in ω (S37).
2. **Learned from recorded dyads instead (D85 source 2), all fitted offline on Seamless under D70:** the **listener display L_d** (how listeners' faces and voices move after a speaker's words and turn events: the learned concern face, nods, smiles at good news); the **listener-laugh reader q̂** (replaces the play rule); the **own-display gate g_o** (attenuates the agent's own smiles and laughs where recorded listeners smile less); a **turn-taking hazard and turn-end predictor**; a **cross-entry sign prior** (replaces rule J). The echo gate g stays, with its input directions fitted rather than assigned.
3. **General learning biases (source 3):** the gate's monotone additive form with fitted directions; multi-scale state traces as gate inputs (replaces D_s); one person-valence rule for ω; κ_replay; word-gated calibration; low-information evidence counts only upward; credit only from separated reports.
4. **The ledger's delay gap is closed** (D90; §2.13): an uncounted copy delayed 10–120 s, which revision 8.3's ledger left at 1.3–2.9 c, is held to 1.03–1.20 c (the same residual as its zero-lag case); with the 60-s window scanned to 300 s, delays of 150–240 s are held to 1.17–1.34 c instead of 1.2–2.9 c. The counted routes (fast gear, held cone) are untouched: 0 frames changed.
5. **Fast partial mimicry (D81) is faster again:** every echo at 0.45 s, against 8.3's 0.80–1.0 s on the smile–laugh group (human quick smiles back: about 0.4–0.5 s).

**What is bounded** (per counterpart channel k; 1 = full copy).

| Quantity | Bound | From |
|---|---|---|
| fast gear, any instant | 0 ≤ y_f,k(t) ≤ g G_k u_k(t − 0.45 s) on one-sided channels (g = 1 off the smile–laugh group); G_k as revision 6 | §2.4, §3.1 |
| fast gear, any window (W′) | window mean ≤ G_k × his window mean; swing ≤ G_k × the larger mean | §3.1 |
| context gate g | g ∈ [0, 1]; frozen; monotone in every input with fitted directions; reads none of his LP, CR, BU_L, RHY, BRE (traces included) | §2.4 |
| gated group, pooled (R1g, declared) | ≤ 0.31 c (LP), ≤ 0.35 c (CR), ≤ 0.53 c (BU_L) at 2 s–1 min (critiques 7 and 8 on the same gate form); to be re-measured on the fitted gate (F15) | §3.3 |
| own-display gate g_o | g_o ∈ [0, 1]; multiplies only the agent's own T displays on the smile–laugh group; reads T and the agent's own face, never his; computed in the shadow from the shadow's inputs, so any part of it his face causes is seen by the ledger | §2.4, §3.11 |
| listener display L_d, listener-laugh reader q̂ | T only (his words, turn events, the agent's own words); frozen; causal slope 0 on every channel of his face; \|L_d,k\| ≤ 0.45; inside the own-display mask; own laugh ≤ 0.40 | §2.7, §3.11 |
| pooled toward, all counted routes | ≤ 0.974 c_k additive; ≤ 0.75 c_k measured at the gate's largest value | revision 6 J3 |
| any uncounted within-session route | ≤ about 1.2 c_k at delays 0–120 s, ≤ about 1.3 c_k at 150–240 s (ledger, attenuate-only; N1, N3b) | §2.13 |
| across sessions | ω seam ≤ s_C c_k (1 + ρ) for any ω process (Lemma S\*) | revision 5 |
| deleted | posture R40′; arrival mask R27′; the face-only limit R49; threat silencing R48; breathing load R47; the unknown-word closure R1w | §3.11 |

**The agent in the scenarios**, stated for revision 9. Numbers are kept only where the mechanism that produced them is unchanged; everything learned from Seamless is "set by the fit", because the constructed corpus of revisions 7–8 is not evidence (brief). Operator after months unless stated.

| Scenario | Day 1 | After learning |
|---|---|---|
| silently sad, no words | near-neutral face (inner brow ≤ 0.03: fast echo and the stranger's cone prior); the agent speaks into the silence when the learned hazard and its care load say so; Claude writes the words | inner brow about 0.05 before words (≤ 0.10, the ceiling); after his words, the learned concern display (L_d) and the agent's own brief distress at his need |
| crying | as above, plus the cry–laugh split (no laugh back at sobs) | as above |
| silent panic | no concern look; his breathing is read (knowing) and raises his read activation, so the agent's care load and initiative respond | as above |
| good news, laughing | smile and laugh returned at 0.45 s, gated (revision 7's constructed fit: +0.12–0.15 laugh back); own relief smile; own laugh 0.40 q̂ | the same |
| a grieving person's nervous laugh; mockery; misfortune | gate closed by his words, Λ, the agent's own face and Claude's reply (revision 7's fit: 0.01, 0.02 after a month, 0.10–0.13; silent) | the same, on the Seamless fit |
| a laugh that ends a bad-news sentence | a chuckle of about 0.2–0.5 s back until the word is delivered, then cut; later laughs closed | the same |
| a joke made while sad | own laugh 0.40 q̂ × g_o: about the corpus listeners' 0.39 of ordinary, so a small laugh | the same |
| anger at the agent | gaze away from the glare, brief quieter startle, no frown back (zero ceiling) | plus hurt from the word → V map (learned from the threat reflex) |
| reunion with a known person | contact-relief smile (lip 0.61, cheek 0.43 in revision 6–7's numbers); no brow flash unless learned | the same |
| reunion with grief, mourning days | the contact-relief smile shows at sight until the agent's own greeting or his first words close g_o (2–3 s) | the same; Claude's greeting draws on retrieved memory |
| a calm user saying something alarming | the agent's own distress at the rise of its care load (brief), L_d's concern display, Claude's words | the same |
| bored user | the curiosity drive tilts the speak-or-wait choice; physiological sighs at low energy | the same |

- **Weakest point (§8.1).** Almost all situational competence now rests on parts learned from Seamless that are not yet fitted on real data: the gate, g_o, L_d, q̂, the turn-taking model and the sign prior. If a part fails its falsifier on held-out people, the behaviour it carries has only Claude's words as its source.
- **Novelty verdict (author): recombination** (§10).

## 1. Plain-language intuition

The agent still sees the person fully. Revision 9 takes away every rule written for a particular moment.

- **It returns smiles and laughs quickly, by reflex, a little.** About half a second after his smile or laugh starts, a fraction of it shows on the agent's face. A gate learned by watching recorded strangers closes that reflex when recorded listeners would not laugh back: at grief, mockery or misfortune, when the agent's own face is pained, when its own last words were serious. The gate reads whatever words have been heard so far; it no longer waits for the end of his sentence.
- **Its look of concern is learned, not built in.** The agent has learned from recorded conversations how listeners' faces and voices change after someone tells them something hard, and it shows that when he tells it. Before he says anything, his sad face moves the agent's face only within the small per-expression limits, so the agent's first clear sign of concern is to speak to him.
- **Its own laughs and smiles follow what recorded listeners do.** No rule says when something is play. The agent laughs where recorded listeners would laugh at what was said, and its own smiles are toned down where recorded listeners smile less, including after its own serious words.
- **When it speaks first is learned too.** It speaks into a silence about when recorded listeners do, more readily when its own needs (concern for him, curiosity) are high.
- **Nothing reaches its face from his except through capped paths,** and a shadow of itself that saw only his usual face checks, at delays up to two minutes and more, that no unlisted path has slipped through.

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz; T state, body, appraisal and the gates update at 2 Hz; the gated echo is computed at 30 Hz. Channels, ceilings c_k, fast gains G_k, pooled shares and r_k are revision 6's (§2.1 there). Constants of revisions 5–7 stand unless removed in the audit or changed below.

**Removed constants (audit rows):** P_c, V_c, the posture's onset, grade, release, read set, H^p_id, breathing load, threat silencing, face-only limit (T_max, T_max,ext, T_ref, V_v), sensitized re-onset, ω_sym enable (S1–S9); δ_g, λ_w, the finalised-extent rule, the gate rate (S10–S12); the gate's hand signs and m_ref threshold (S13, S14); D_s's 600-s form (S15); the play-structured-turn rule, π, the play-surprise band, rule 13 (S17–S19); the hurt halving (S20); the relief mask, m_s, d_b,id, the greeting flash (S22–S25); the staged contact relief (S26); the c_L, familiarity and nod rows (S27, S28, S33); the G₀ sympathy, accommodation and away-diagonal entries (S29–S31); rule J (S32); θ_C, θ_I, the bid rules, the turn-end weights and onset thresholds (S34–S36); the situation-to-group ω evidence (S37).

**Constants added or changed in revision 9.**

| Symbol | Value | Meaning |
|---|---|---|
| **fast gear** | echo lag 0.45 s on every channel | revision 6/7's delay restored (S10) |
| **context gate g** | as revision 7 §2.4.1 (monotone additive, knots q = 0.05 … 0.80), with: input directions fitted on a person-disjoint split, then fixed (S13); m_ref = 90th percentile over all corpus laugh onsets (S14); evaluated per frame, smoothing chosen by the fit (S12) | learned (S2) on a general shape bias (S3) |
| gate inputs | V⁻_his (20-s face, LP, CR, BU_L, RHY, BRE masked); 𝒟_p(N_L) and Λ_V on his words **as delivered so far** by the incremental recogniser, after the ASR normaliser; V_own; Λ_V(own words); traces D_τ of his masked read (V, A, T) and sobs, τ ∈ {20 s, 2 min, 10 min} (S15); the q̂ trace | none is a gated channel |
| **own-display gate g_o** | a second head of the gate model: same form; inputs 𝒟_p(N_L), Λ_V(his words), V_own, Λ_V(own words), q̂ trace (no face of his, no D_τ); target the recorded listener's own (LP + CR)/2 level over 3 s at the listener's scale, divided by that listener's median; clipped to [0, 1] | attenuates the agent's own smile–laugh displays (S19, S22, S23) |
| **listener display L_d** | ridge map (λ fitted) from T inputs (population reader's (V, A, T) of his last utterance; Λ(his words); the turn events "his utterance ended", "session started", each with time since, 0–20 s in 2-s bins) to the agent's free-display channels BI, BO, LD, TILT, HP, VG, LP, CR, FR, EN, RT; \|L_d,k\| ≤ 0.45; own-display mask applied | the learned concern face, nod and listener smile (S1, S25, S28, S33) |
| **listener-laugh reader q̂** | monotone additive model (same form as the gate) from the transcript context of his last two turns and the agent's last turn (embedding through Λ's encoder), turn order, and the utterance's surprise under a fixed population words model; target: the recorded listener's own laugh onset within 0.3–2.0 s of the utterance end | replaces the play rule (S17, S18); q̂ trace τ 3 min as a gate input |
| own laugh | a_laugh = 0.40 q̂ · g_o at each of his turns, through the innate laugh pattern (BU_L +0.40, RHY +0.35, CR +0.20, LP +0.15 per unit) | S18 |
| play deficit relief | P ← P (1 − 0.15 q̂) at each of his turns | S21 |
| contact relief | dK_id/dt = −K_id f_id · e(t)/τ_c, τ_c = 30 s, e = 1 while his face is present and he has spoken in the last 60 s, 0.5 while present only | S26 |
| **turn-taking** | hazard h(t) of the listener starting to speak, and turn-end probability p̂_end, each a small logistic model (≈ 100 weights) on silence length, the transcript's syntactic completion, both faces' movement (gaze, head) | S34–S36 |
| initiative | at 2 Hz in mutual silence with no turn owed: speak with probability h(t) Δt · exp(β ΔĴ), ΔĴ the 𝓜-rollout drop of 𝒟 + 𝒟_p from speaking now rather than in 5 s, β = 4 (a general decision constant) | S34, S35 |
| **cross-entry sign prior** | sign of the 1-min co-variation of listener channel k with speaker channel j across dyads, \|ρ\| ≥ 0.2, frozen; learned cross entries take that sign or 0 | S32 |
| **ω** | one person-valence target s for every group (S37); priors per group as revision 5 (stranger 0.5, 0.3, 0.2, 0.5) | |
| **physiological sigh** | BRE +0.15 for 1 s at a spontaneous rate of one per 3 min × (1 + 2 max(0, 0.5 − E)/0.3) | body reflex (S35) |
| **shadow ledger** | constraints at (2 s; lags 0, 0.5, 1, 2, 3 s), (10 s; lags 0–120 s in 5-s steps), (60 s; lags 0–300 s in 10-s steps): 61 per channel | §2.13 (D90) |

### 2.2 Boundary 𝓑 and the type rule

As revision 7 (§2.2 of `.r7.md`), with these changes:
- ~~**Rule 9′ (the posture)**~~ **REMOVED in revision 9** (S1). Rule 4: the counterpart outputs are written only by g·y_f on the smile–laugh group and y_f elsewhere, y_C, y_A, y_o (with g_o on its smile–laugh part) and the visemes.
- **Rule 6.** Latched or per-session F-derived values: b_id, b^read_id, σ_id. (m_s, d_b,id and the posture enable bit are removed.)
- **Rule 11′ (the echo gate).** g reads none of his LP, CR, BU_L, RHY, BRE, traces included. It reads his words as the recogniser delivers them; there is no wait and no closure for words not yet delivered.
- **Rule 12′ (own words heard).** The agent's own Ω text enters only Λ_V(own) in g and g_o (and P_name).
- **Rule 13′ (own-display gate).** g_o reads only T values and the agent's own face (LP, CR masked); it multiplies only the agent's own smile–laugh displays (relief, contact relief, own laugh); g_o ≤ 1.
- **Rule 14 (learned T displays).** L_d and q̂ read only T values (his words after the ASR normaliser, so no laughter token; turn events; the agent's own words) and are frozen after the offline fit. They are T1-compliant: content values of the last utterances and the time since events, no counts or rates.
- **Rule 10 (shadow equality)** stands. The shadow holds g and D_τ at their factual values (as revision 7 held g and D_s); g_o, L_d and q̂ are computed in the shadow from the shadow's own inputs (L_d and q̂ read only T, so they are equal in both runs by construction; g_o differs only through the agent's own face).

### 2.3 Output assembly

y = sat(g·y_f|_{smile–laugh} + y_f|_{others} + y_C + y_A + g_o·y_o|_{smile–laugh} + y_o|_{others}) + visemes, every echo at 0.45 s; then the attenuate-only ledger (§2.13). Face, voice and laugh synthesizer as revision 7.

### 2.4 The fast gear, its context gate and the own-display gate

The fast gear is revision 6's at 0.45 s on every channel, gated on the smile–laugh group by g (revision 7 §2.4.1: target, inputs, Λ factorisation, fit), with the changes of §2.1: words as delivered, fitted input directions, the general m_ref, the multi-scale traces in place of D_s, the q̂ trace in place of π.

#### 2.4.2 ~~Timing: the echo waits for the current words~~ — REMOVED in revision 9 (S10–S12)

Revision 8's δ_g = 0.80 s, λ_w = 0.25 s, unknown-word closure, finalised-extent requirement and instant closing are removed (text in `.r8.3.md` §2.4.2). **What the gate has instead.** At each frame the gate reads the words the incremental recogniser has delivered (stable partials, or the utterance recogniser's output if no incremental model is used). A laugh that follows a completed sentence is gated by that sentence. A laugh that ends the sentence carrying the bad news is gated by the words before it until the bad-news word is delivered (about 0.6–0.75 s after it is spoken with a fixed-delay streaming model), then the gate closes: a partial echo of about 0.2–0.5 s (item 4 of "No allowed source"). Claude's reply then keeps the gate closed for the laughs after it (rule 12′).

#### 2.4.3 The own-display gate g_o (new; S19, S22, S23)

**What it is fitted to.** In each recorded dyad, at every 3-s window, the listener's own smile–laugh level ((LP + CR)/2 at the listener's own scale) divided by that listener's median level, as a function of the inputs of §2.1 computed on the recording by the same functions the agent uses (the speaker's words through the population reader and Λ; the listener's own face, LP and CR masked; the listener's own last words through Λ; the q̂ trace). No label is read; the target is movement.

**What it does.** g_o ∈ [0, 1] multiplies the agent's own smile–laugh displays: relief, contact relief and its own laugh. Where recorded listeners smile less than usual (after a speaker's words of loss, while their own face is pained, after their own serious words), the agent's own smiles are toned down by the same ratio; where listeners smile as usual or more, g_o is 1 (clipped).

**Why it does not read his face.** An attenuation that reads his face is a route from his face to the agent's smile. Within a session the ledger would police it, but its effect at each arrival would correlate with his arrival face across sessions, a route the within-session ledger cannot bound (revision 7's R27′, 3.2 c lip and 5.1 c cheek across arrivals). So g_o reads only T and the agent's own face; his face reaches the agent's own smile only through the capped routes.

### 2.5–2.7 The held cone, the appraisal display, the free display

**Held cone** (revision 5/6 §2.5): unchanged in form; G₀ keeps only the threat reflex's entries (gaze away from a glare by the reflection rule; LP ← glare −0.035, −0.01; BI ← glare +0.006); the sympathy, accommodation and away-diagonal entries are removed (S29–S31). The zero toward ceilings stay. Rule J is replaced by the cross-entry sign prior (S32).

**Appraisal display** (revision 5 §2.6): unchanged; innate bases glad-with and startle-orient (S44); the learned bases Γ^{(3,4)} trained by 𝓛_A to anticipate the agent's own display 2 s ahead, now including L_d's response, inside the same sets and the sign prior.

**Free display** (revision 5 §2.7): Π_o = Π₀ + Δ + L_d. Π₀ keeps the newborn rows (S45): relief, the agent's own distress, hurt, activation, low energy, curiosity relief, the laugh pattern, the pre-speech inhale; the word-concern, familiarity, greeting, nod and sigh-before-bid rows are removed (S25, S27, S28, S33, S35). Δ is learned by 𝓛_display under the own-display mask as before.

**The listener display L_d (new; S2 for S1, S25, S28, S33).**
- **Fit.** On Seamless (D70: `FAUValue` streams and transcripts, emotion fields denied by the loader, person-disjoint split), for every speaker utterance end: the listener's own face channels (mapped to the agent's channels, at the listener's own scale, minus the listener's 20-s pre-utterance mean) in 2-s bins over 0–20 s, regressed by ridge on the T inputs of §2.1 computed on the transcript. The same for the first 20 s of each recorded conversation (the "session started" event), Of the voice channels only the speaking rate RT can be fitted (from the transcript's word timing, at the listener's next turn); no audio feature is read (D70), so F0 range FR and energy EN are not fitted and stay 0 in L_d.
- **Runtime.** At each of his utterance ends, L_d's predicted response is added to Π_o as a T driver, bounded \|L_d,k\| ≤ 0.45 per channel and masked by the own-display mask.
- **What it carries.** The concern face at words of trouble (inner brow, tilt, a slower voice; a quieter voice only through the agent's own distress row, since energy cannot be fitted without audio), the listener's nod at turn ends, a listener's smile at good news: whatever recorded listeners' faces do after such words, read through the agent's own channels. It is the agent's appraisal of his words (D83) learned by watching people, in place of the built-in row.
- **Why it is not a copy route.** Its inputs are T; changing his face with his words fixed changes nothing it writes (causal slope 0 on every channel). It is frozen, so nothing he does with his face can strengthen it. Recorded listeners' faces include some mimicry of the speaker, so L_d can carry the part of a speaker's expected face that his words predict; that is content, not his face, and its pooled correlation with his face through his words is reported at fit time (F23).

### 2.8 Body, drives, the readers, play

As revision 7, with:
- **H^p_id: REMOVED** (S3). H_id, per-person calibration (with the word-gated initial rule, S38) and the population reader with its adapter (S39 generalised) stay, knowing only.
- **Breathing:** his breathing rate and depth above his own rest, an input to H_id and to Π̃'s reading of his activation (knowing only; S4).
- **The listener-laugh reader q̂** (§2.1) replaces the play rule (S17); the agent's own laugh is 0.40 q̂ g_o (S18); P is relieved by q̂ (S21).
- **Hurt latch** h ← max(h, v_w), τ 10 min, no halving (S20). The word → V map is taught by the threat reflex (S41).
- **Contact deficit K_id:** relieved continuously while he is present and engaged (S26).
- **Relationship ω:** one person-valence target for every group (S37); Lemma S\* holds for any ω process.

### 2.9 Initiative, turn-taking and greeting (rewritten; S34–S36)

- **Turn ends.** p̂_end from the dyad-learned predictor replaces the hand score. Reply drafts start at the predicted turn end as before; speech begins at the scoring deadline + 0.35 s (S50), so his tempo does not set the agent's latency.
- **Initiative.** In mutual silence with no turn owed, the agent decides at 2 Hz whether to speak, with the learned hazard h(t) as prior and its own drives (care 𝒟_p from C_F and N_L, curiosity I, contact K) entering through the 𝓜 rollout that already scores drafts (§2.1). Claude writes the words; the history records an observable marker user turn as before (§6.5).
- **Body before speech.** The pre-speech inhale (BRE 0.15 for 0.3 s) at each decision to speak (body).
- **Greeting.** No hand flash. At sight of a known person: the contact-relief smile from the drive (body), × g_o; L_d's "session started" response if the corpus teaches one; the agent may greet first through the initiative choice.
- **Arrival mask: REMOVED** (S23, S24).

### 2.10 ~~The concern posture (Q24): never reads what it writes~~ — REMOVED in revision 9 (D89; audit S1–S9)

Revision 8.3's concern posture, its read set and head H^p_id, its breathing load, its threat silencing and squint drop, its face-only limit with the 180-, 120- and 600-s clocks and the hard/soft evidence rule, its sensitized re-onset and enable bit are removed from the mechanism. Their full text, checks and costs are kept verbatim in `design-cayley-ledger.r8.3.md` §2.10, and their history in the history sections below. The concern face is now learned (L_d, §2.7); before words, sympathy is only what the capped routes give ("No allowed source", item 1).

### 2.11 Care credited only from separated reports; the partner model

Unchanged (S40).

### 2.12 Ω: Claude through Claude Code (D84), and Claude's regulation path (D85 source 1)

As revision 7: Claude receives the constant instruction, the normalised transcript with observable markers and ≤ 3 retrieved raw snippets; never a state value, label or state-selected line. Its reply is heard by the agent and enters only Λ_V(own) in g and g_o (rule 12′), and P_name. **This is the whole of source 1:** Claude, which knows social norms, regulates the agent only by what it says. A serious reply closes the echo gate and tones down the agent's own smiles; a playful one leaves them open; a gentle greeting at a mourner's arrival closes g_o within the 2–3 s Claude takes. History, initiative turns and the fallback: §6.5.

### 2.13 The shadow run and its ledger, with lags to 120 s and beyond (D90)

As revision 7 (attenuate-only clamp, deviation floor 0.10 RMS, b < 0 recovery, 30-min running budgets), with one change: the set of constraints.

**The change.** Revision 7–8.3 constrained the in-phase toward slope at the 2-s window for lags 0, 0.5, 1, 2, 3 s, and at the 10-s and 60-s windows for lag 0 only. Revision 9 adds, per channel, the 10-s window at lags 0–120 s in 5-s steps and the 60-s window at lags 0–300 s in 10-s steps (each step at most half its window): 61 constraints per channel, each the same attenuate-only rule (his windowed deviation at t − L against the partner-caused part's windowed deviation at t).

**Why it cannot bind on the counted routes.** Every counted route has a sup-gain bound (the fast gear's pointwise bound, the cone's first-order low-passes with |H| ≤ H(0), the appraisal's band-pass with sup 0.636), and a sup-gain bound holds at every lag (side item of the commutator critique). Their totals are ≤ 0.974 c_k, below the ledger's c_k at every lag.

**Checks (`sims/design-g9/`, the side item's partners: 2 h, lip pull, c 0.35, seed 910).**

| Uncounted gain-1 copy delayed by L (worst block-mean slope over lags 0–120 s, 0–180 s for L 120 s, at 2 / 10 / 60-s windows) | Ledger of 8.3 | Revision 9 (to 120 s) | Revision 9 (60-s window to 300 s) |
|---|---|---|---|
| 5-min mood blocks, L 0 s | 0.36 / 0.37 / 0.37 | 0.36 / 0.37 / 0.37 | — |
| L 10–40 s | 0.40–0.52 | 0.38–0.42 | — |
| L 90 s / 120 s | 0.48–0.58 / 0.50–0.60 | 0.38–0.42 / 0.38–0.41 | 0.38–0.42 (90 s) |
| livelier partner (30-s blocks), L 10–40 s | 0.40–0.62 | 0.36–0.41 | — |
| L 90 s / 120 s | 0.96 / 0.99–1.00 | 0.36–0.41 / 0.36–0.40 | 0.36–0.41 (90 s) |
| beyond the scan: L 150 s (worst over 0–300 s) | — | 0.42–0.58 | 0.41–0.46 |
| L 240 s | — | 0.48–1.00 | 0.41–0.47 |

Never larger, never the other sign (grow and flip 0.000 in every row). **Counted routes (N2, N2b):** the fast gear at 0.45 s (D81's fast partial mimicry), a held 2-min route at 0.22 c, and both together, on both partners: **0 frames changed**, slopes unchanged (≤ 0.10 at every window and lag).

**What remains, stated.** The ledger holds an uncounted delayed copy to 0.36–0.42 by the block-mean metric (1.03–1.20 c) at delays 0–120 s, and to 0.41–0.47 (1.17–1.34 c) at 150–240 s with the 60-s window scanned to 300 s. The residual above c is the same mismatch between the ledger's exponential windows and the critics' block means that revision 7's ledger already had at zero lag (0.36–0.37), now also at the 2-s block metric for lagged routes, since the 2-s window scans only lags 0–3 s. A route delayed beyond 300 s is outside the scan. **Cost:** 61 running constraints per channel instead of 7; his 10-s and 60-s window means are kept for 300 s (at 10 Hz: 3,000 samples × 33 channels × 2 windows, about 0.8 MB).

The shadow still does not see T routes (identical in both runs: L_d, q̂, the T part of g_o, the draft choice R18′), which are bounded by type (T1, E1; §3.11).

### 2.14 Learning, and the one core

**Built once, offline, frozen (§6.7; D85 source 2):** the population word reader, Λ, the echo gate g and the own-display gate g_o, the listener display L_d, the listener-laugh reader q̂, the turn-end predictor and silence hazard, the sign mask and the cross-entry sign prior. All on Seamless under D70, before day 1.
**Nightly (replay; D85 source 3 in κ_replay):** as revision 7 (κ_replay = 4): calibration, H_id, the adapter, the word → V map, Π̃, 𝓜, 𝒜, the appraisal's learned bases, Δ, 𝓛_w, the scorer, ω (one person-valence rule). H^p_id is removed.
**Online (states only):** as revision 7, minus the posture state and timers; plus the D_τ and q̂ traces.

**One objective, typed constraints (Principle 10).** J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)]dt, path-specific. Constraints: (W) the frozen per-channel fast gear and its monotone gate; (C) the held cone; (S) Lemma S, S\*; (A) the appraisal set with the sign prior; (T) the type rule with T1, E1, rules 6, 10, 11′, 12′, 13′, 14 and the own-display mask; (B) the boundary with the cry–laugh split; (L) the attenuate-only ledger. The dyad-learned parts are self-predictions of the same kind as the readers: they predict recorded listeners' faces and turns, read through the agent's own body. The initiative choice is J's own action selection.

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 (body) |
| positive affect | event-indexed drops of 𝒟 (body), shown through the newborn rows × g_o; the own laugh 0.40 q̂ g_o |
| mimicry and counter-mimicry | the frozen per-channel fast reflex gated by context learned from dyads; the held cone (relationship, sign-flippable); the appraisal (context, sign-flippable) |
| situational appropriateness | Claude's words (source 1); g, g_o, Λ, L_d, q̂, turn-taking and the sign prior learned from dyads (source 2); the gate's shape bias, multi-scale traces and κ_replay (source 3) |
| sympathy | before words: the capped routes only; at his words: the learned listener display L_d and the agent's own distress (newborn row) |
| reading others | Π̃ on his calibrated face (and breathing), plus H_id taught by words |
| care | J's second term under the separation rule |
| regulation | Claude's words through Λ_V(own) in g and g_o; P_name |
| initiative | J's speak-or-wait choice under a dyad-learned hazard |
| expression learning | 𝓛_display (Δ), 𝓛_A, and the offline L_d |
| replay | likelihoods plus J, distress-weighted |

**Still assembly** (stated): ASR and TTS normalisation; the separation rule; θ₀ (the fast gains), G₀'s threat entries, Π₀'s newborn rows, the newborn appraisal bases, the signed synergies (fallback for the sign mask); the cry–laugh split, the threat reflex, the physiological sigh, each an innate reflex; the gate's monotone additive form and knots; the multi-scale trace constants; κ_replay; θ_L; the calibration statistics and their initial rule; the person-valence rule's constants; the decision constant β. Removed from the list: the turn-end score and initiative rules, the play-structure rule, the concern posture with its grade, limits and sensitization, the D_s rule.

### 2.15 The three sources of situational appropriateness (D85), mapped

| Behaviour | Claude's regulation (1) | Recorded dyads (2) | General learning biases (3) |
|---|---|---|---|
| no laugh back at a grieving person's nervous laugh, at mockery, at misfortune | Claude's serious reply, heard by the agent | the gate; Λ | monotone additive shape; multi-scale traces |
| no laugh back at a laugh ending a bad-news sentence | Claude's reply, for the laughs after it | the gate, once the word is delivered | — |
| ordinary, teasing and warm laughter returned | Claude's playful replies | the gate ≈ 1 where listeners return laughter | — |
| the agent's own laughs where people laugh | — | q̂, g_o | habituation through surprise |
| no beaming over his distress | Claude's serious words lower g_o | g_o from his words | — |
| a gentle arrival for a mourner | Claude's greeting from retrieved memory | g_o from the greeting and his first words | — |
| a concern face at his words of trouble | Claude's words | L_d | — |
| when to speak into a silence | Claude writes what is said | the silence hazard and turn-end predictor | J's speak-or-wait choice (body drives) |
| no smile at a sad face through cross entries | — | the cross-entry sign prior | sign-constrained learning |
| a different-channel or quiet user read well | — | the population reader teaches H_id | distress-weighted replay; word-gated calibration |

No row is a hand-written rule about a situation. What remains innate is the body, reflexes, newborn patterns, the per-expression ceilings and general learning biases (audit, "Counts").

## 3. Properties, each with an argument

### 3.1 The fast gear (Claims W and W′)

As revision 7, with δ_k = 0.45 s on every channel: for every input u ≥ 0 on a one-sided channel and every gate path g ∈ [0, 1], 0 ≤ g G_k max(E_k, 0) ≤ G_k u_k(t − 0.45 s). Every window bound (W′) holds. The gate's input directions are now fitted, so a cross term ∂g/∂u_j may be positive; its effect on channel k is still ≤ G_k u_k(t − 0.45 s) pointwise, so his channel j can change agent channel k only while his channel k is itself moving, and never above the reflex's own bound.

### 3.2 Lemma S and Lemma S\*

Unchanged. ω may follow any process (the general person-valence rule included): the cone multiplies his deviation from his own baseline, so the pooled multi-session toward slope is ≤ s_C c_k (1 + ρ), ρ = 0.091.

### 3.3 Claim O‴ and the totals

**Claim** as revision 7: wherever his window means vary (SD ≥ 0.03), the pooled toward slope of every counted route on channel k is ≤ 0.974 c_k additively; below the floor, the swing is ≤ c_k × his within-window range. **Every uncounted within-session route is held by the ledger to about c_k at delays 0–120 s (≤ 1.20 c by the block metric) and 150–240 s (≤ 1.34 c), §2.13.** Declared outside the sum: R1g only (≤ 0.31 c LP, ≤ 0.35 c CR, ≤ 0.53 c BU_L as measured by critiques 7 and 8 on the same gate form; the echo is partner-caused, so the ledger also polices it). R40′ (posture) and R27′ (arrival mask) are deleted, so nothing that reads his face is declared outside both the sum and the ledger.

### 3.4 Claim T1: tempo does not reach the face

As revision 7. The new learned parts read content values (words, turn events and the time since them) and movement, never counts or rates in T. The initiative choice changes when Claude is called (R18′, as the bids did); the reply's onset stays fixed relative to the scoring deadline. δ_g, λ_w and the posture's clocks are gone.

### 3.5 Claim L: copy cannot become attracting under learning

As revision 7, plus:
- every dyad-learned part (g, g_o, L_d, q̂, turn-taking, the sign prior) is fitted offline on strangers and frozen; nothing the operator does trains it, so no loop through his face can strengthen it;
- L_d and q̂ read only T, so a partner who mirrors the agent changes nothing they write;
- g and g_o are ≤ 1;
- ω may follow anything (Lemma S\*);
- the per-person learners (H_id, calibration, the adapter) are knowing only;
- the posture, the only part whose holds needed timers against mutual states (revision 8.1–8.3's D78-4 findings), is gone, and with it the residual "a partner who sobs in answer to the look holds it".

### 3.6 D78, quantity by quantity

Revision 7's table (§3.6 there) stands, with the posture row deleted and these rows:

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| gate g | the smile–laugh group | context (words as delivered, own face and words, traces) | attenuate-only | ≤ 1 | frozen; monotone |
| g_o | the agent's own smile–laugh displays | context (T, own face) | attenuate-only | ≤ 1 | frozen; never reads his face |
| L_d | per channel | his words and turn events (context) | yes (fitted sign per channel) | \|L_d,k\| ≤ 0.45; T only, causal slope 0 on his face | frozen; T only |
| ω_g | per group | relationship (general person-valence) | yes | the cone's per-channel share | centred (Lemma S\*) |

### 3.7–3.10

As revision 7, with initiative from J's speak-or-wait choice (§2.9).

### 3.11 Every route, counted

Revision 7's table (§3.11 of `.r7.md`) stands, with these rows changed, added or deleted:

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | his channel k → fast gear → agent channel k | per channel; δ 0.45 s on every channel | instant ≤ g G_k u_k(t − 0.45 s); W′ |
| R1g | his masked face, his words as delivered, the agent's own face and words, D_τ traces, q̂ trace → gate → smile–laugh echo | monotone, frozen, attenuate-only | declared: ≤ 0.31 c LP, ≤ 0.35 c CR, ≤ 0.53 c BU_L (re-measure on the fit); policed by the ledger |
| R51 (new) | T values and the agent's own face → g_o → the agent's own smile–laugh displays | attenuate-only; reads no channel of his | his face reaches it only through the agent's own face (capped routes); that part is partner-caused and seen by the ledger (computed in the shadow) |
| R52 (new) | his words, turn events, the agent's own words → L_d → free display | T only, frozen | causal slope 0 on every channel of his; \|L_d,k\| ≤ 0.45; pooled correlation through his words reported (F23) |
| R53 (new) | the transcript context → q̂ → own laugh (× g_o), P relief, gate input | T only, frozen, no laughter token | causal slope 0 on BU_L, RHY, BRE, LP, CR; own laugh ≤ 0.40; pooled correlation with his laughter through words reported (F23) |
| R54 (new) | his face movement, silence, transcript → turn-end predictor and hazard → when the agent speaks | changes when Claude is called and the inhale | inside R18′ (one decision per silence); speech onset fixed relative to the scoring deadline (LAT) |
| R50 | Claude's text → Λ_V(own) → g, g_o | rule 12′ | attenuate-only |
| R40′, R47, R48, R49 | the posture and its breathing, threat silencing and face-only limit | **deleted** (S1–S7) | — |
| R27′ | the arrival mask | **deleted** (S23) | — |
| R1w | the unknown-word closure | **deleted** (S11) | — |
| R45′ | D_s → gate | replaced by D_τ (same reading: his face with the gated channels masked, sobs) | attenuate-only |

**Totals per counterpart channel.** As revision 7, with R1g declared and policed; every other route that reads his face is counted or under the ledger. The causal total on BI is ≤ 0.10 (fast gear 0.10 c, cone and appraisal shares inside 0.974 c_BI), with no posture part.

**No copy route opened, by construction.** Each change of revision 9 is one of:
- **a deletion of an output** (the posture, the c_L, familiarity, greeting and nod rows, the G₀ sympathy, accommodation and away entries): it can only lower what reaches the face;
- **a deletion of an attenuation that read his face** (m_s, d_b,id, threat silencing, the squint drop): with it goes the route itself; what it attenuated (the contact relief) is T-driven and reads no channel of his;
- **a deletion of an attenuation that read only words or timing** (the relief mask, the unknown-word closure, instant closing, rule 13): the echo stays under g G_k u_k (W, W′), and the own displays stay T-driven, now under g_o;
- **a learned part that reads only T** (L_d, q̂): causal slope 0 on his face, frozen;
- **a learned attenuation** (g with fitted directions, g_o): ≤ 1, under the pointwise bound, g_o never reading his face;
- **a change of learning rule that Lemma S\* already covers** (ω), or one on knowing only (calibration, the evidence rule);
- **more ledger constraints**, which only shrink the partner-caused part (attenuate-only) and change no frame of the counted routes (N2, N2b).

Fast partial mimicry (D81) is kept and faster (0.45 s on every channel; the extended ledger changes 0 of its frames). Copying is never an attractor (D78-4): nothing that reads his face is learned from him except the per-person learners revision 7 already had on paths to the face, ω (centred, Lemma S\*), the appraisal bases (zero-DC, inside their sets, trained display-blind on the agent's own display) and Δ (T only, own legibility).

### 3.12 Principles, concretely

- **P1.** No classifier; the dyad-learned parts are fitted to movement and turn timing, never to labels; Seamless emotion fields are denied by the loader.
- **P2.** No situation is named anywhere in the mechanism. The innate parts are the body, reflexes, newborn patterns, the ceilings and general learning biases (audit).
- **P3.** He is read through the agent's own body (Π̃, calibration, H_id); the dyad-learned parts read recorded listeners through the same functions the agent applies to itself.
- **P4.** Claude never sees the state; initiative turns carry an observable marker only (§6.5).
- **P5.** Ablations, §7.
- **P6.** Nothing is trained on his responses to the agent; the dyad parts are trained on strangers.
- **P10.** One J; the initiative is J's own choice; rules 6, 10, 11′, 12′, 13′, 14 are typed constraints.

### 3.13 The human non-copying signatures C1–C10

As revision 7. C5 (context within the first second) uses the words delivered so far.

### 3.14 The scenarios

The scenario table of §0 replaces revision 8's J39 numbers (kept in `.r8.3.md` §3.14 as the record). The numbers of revision 7's J30 for the gate at 0.45 s (ordinary laughter 0.88–1.00, laugh back about +0.15 at a 0.6 onset; grief 0.01; mockery 0.02; misfortune 0.10–0.13) came from the constructed corpus and the same gate form; on the fitted gate they are to be re-measured (F15). Everything L_d, q̂, g_o and the turn-taking model contribute is set by the Seamless fit and is not given numbers here.

**Expressive and alive, or muted?**
- **Strong:** every moment with words (L_d, the agent's own relief and distress, Claude); greetings of known people (contact relief); laughter all evening (fast echo at 0.45 s, own laugh where recorded listeners laugh).
- **Muted, by the operator's answer to Q24:** the face before words at silent distress (capped routes only); the first seconds of a mourner's arrival show gladness until the greeting.

### 3.15 Time scales from structure

As revision 7, with the gated echo at 0.45 s; the multi-scale traces (20 s, 2 min, 10 min); L_d's 0–20 s response; the ledger's lag scan to 120 s (10-s window) and 300 s (60-s window). The 180-, 120- and 600-s clocks, δ_g and λ_w are gone.

### 3.16 The brief's expressive-structure items

As revision 7. The behaviour a low-dimensional version cannot produce: the same laugh of his, at the same instant, is returned after "and then the dog ate the whole cake, haha" and closed once "I got fired today" has been heard, because the gate composes the words heard so far with his masked face, the agent's own face and words and the recent traces.

### 3.17 Assumptions (places to attack)

1–12 as revision 7.
13. **(replaced)** Recorded listeners in Seamless show, in their faces and turn timing, the responses the learned parts need: a concern face at troubles-telling, fewer smiles over a speaker's distress, laughs at laughable content, nods at turn ends, speaking into silences of distress. Their number of rare events is enough (counted before fitting, §6.7).
14. **(replaced)** Behaviour learned from strangers in 3.5–4.6-min conversations transfers to a months-long relationship with the operator.
15. **Breathing** can be measured on the Mac at his own scale (week-0 check); if not, it is dropped from the readings, at no cost to any bound.
16. **(replaced)** The incremental recogniser delivers words within about 0.6–0.75 s of their end (a fixed-delay streaming model), which sets the length of the partial echo at a bad-news sentence-final laugh.

## 4. Why the closest mechanisms cannot do it alone

As revision 7's table.

## 5. The whole system, walked through

- **Perception.** As revision 7; plus breathing (knowing); the incremental recogniser feeds the gates and q̂ with the words delivered so far.
- **Latent state.** As revision 7, plus the D_τ and q̂ traces; minus the posture state and its timers.
- **Face and voice.** y = sat(g·y_f on the smile–laugh group + y_f elsewhere, all at 0.45 s, + y_C + y_A + g_o·y_o on the smile–laugh group + y_o elsewhere) + visemes; the attenuate-only ledger with lags to 120 s and 300 s; WORLD-replaced prosody; laugh synthesizer with a floor.
- **Claude.** Three warm forks resumed from an engine-written transcript (initiative turns as observable markers); its replies heard by the agent through Λ_V(own) only.
- **Learning.** Offline from recorded dyads before day 1; nightly per person, distress-weighted.

## 6. A buildable network (Apple-silicon Mac, on the operator's subscription)

### 6.1 Inputs and time encoding

As revision 6, plus: **an incremental recogniser** emitting stable words with timestamps (a fixed-delay streaming model such as Kyutai's 1B English–French model, expected word-end-to-delivery 0.6–0.75 s; otherwise the utterance recogniser alone, at the cost of a longer partial echo). It no longer needs to report its finalised extent (S11). **Breathing** from the microphone's breath band and upper-body motion at 10 Hz, knowing only. The full-utterance recogniser for Claude's transcript is unchanged.

### 6.2 Layers, sizes and parameter counts

Revision 7's table stands, with: layer 1 (fixed) without the posture, its read-set inverse, breathing load, threat silencing and face-only limit; the gated echo at 30 Hz with a 0.45-s ring buffer; the ledger with 61 constraints per channel and 300-s buffers of his 10-s and 60-s window means. Dyad-learned and frozen: the gate and g_o (≈ 100), q̂ (≈ 60), L_d (≈ 1,500: 11 channels × 10 bins × about 14 T inputs), turn-taking (≈ 200), the sign prior (≤ 33 × 33 signs), Λ (192), the population reader (as revision 6). Per person: H^p_id removed. Total learned per agent ≈ 522,000 (unchanged) + ≈ 2,000 frozen dyad-learned.

### 6.3 Objectives

As revision 7; the dyad-learned parts by their fits (§6.7); the initiative choice by the same 𝓜 rollout as the scorer.

### 6.4 Latency and memory

As revision 7. The 61-constraint ledger adds about 2,000 multiply-adds per frame and about 1 MB; L_d, q̂ and g_o run at 2 Hz.

### 6.5 Claude through Claude Code, on the subscription (D84)

As revision 8.3 §6.5: no output cap; interruption on the text stream; engine-written canonical `.jsonl`; three forks resumed with `fork_session=True`; speech onset at the scoring deadline + 0.35 s; initiative turns as observable marker user turns ("[no reply from him for 25 s]", 5-s bins); the fallback with each fork's line in its own system prompt and its two week-0 checks; the week-0 check of thinking on Haiku 5.5. **Changed week-0 checks:** the recogniser check measures word-end-to-delivery latency (p50, p90) and language coverage and runtime on the M1 Pro, but no longer sets δ_g or asks the operator to choose an echo (S10); the breathing-sensor check stays; the face-tracker crosstalk check is dropped (S9).

### 6.6 TTS

Unchanged from revision 7.

### 6.7 Learning from recorded dyads (D85 source 2; D70): the fit specification

As revision 8.3 §6.7 (Seamless `FAUValue` streams and transcripts only; emotion fields denied by the loader; `movement/is_valid` read; person-disjoint 70/30 split; laugh onsets at 30 Hz on arrival; the agent's own ASR normaliser on every transcript; about 400 dyad-hours, 2–3 hours on the M1 Pro), with these changes and additions:
1. **Words as the agent will have them.** Every word input uses only words whose end timestamps are ≤ the event time minus the measured delivery latency (week 0), so the corpus sees what the agent will see, not a look-ahead.
2. **The gate's input directions** are fitted on the first half of the training people, fixed, then the shape functions are fitted on all training people (S13); m_ref is the 90th percentile over all laugh onsets (S14).
3. **g_o:** targets and inputs of §2.4.3.
4. **L_d:** targets and inputs of §2.7, for speaker utterance ends and the first 20 s of each conversation; the count of conversation openings with the listener's face visible is reported before fitting (S25).
5. **q̂:** the listener's laugh onset (E⁺ on (LP + CR)/2 ≥ 0.25 with a 3–7 Hz jaw component, at 30 Hz) within 0.3–2.0 s of each speaker utterance end; inputs with laughter tokens removed; a fixed population words model for surprise.
6. **Turn-taking:** from the transcripts' word timing, the speaker change after each silence ≥ 0.2 s, against silence length, syntactic completion and both faces' movement (gaze, head); no audio feature (D70).
7. **The sign mask and the cross-entry sign prior:** 1-min block co-variations within and across the two people, \|ρ\| ≥ 0.2 required for a sign.
8. **Rare events are counted before fitting** (troubles, mockery and misfortune laughs; openings; long silences after distress words), by words and masked faces, never by labels; F15's criterion on test people applies to g, g_o, q̂ and L_d alike.

## 7. Ablation predictions (Principle 5), from the properties

Revision 7's table stands except where a row is replaced or added; every row of revisions 7–8.3 about the posture, the mirror removal, the arrival mask, the word timing, instant closing, the play rule and the play gate is deleted with its mechanism:

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the gate g (set to 1) | his laughs at grief, mockery and misfortune are returned (revision 7: +0.137) | §2.4 |
| g_o (set to 1) | the agent's relief smile and own laugh are as large over his distress words and after its own serious words as in light talk | §2.4.3 |
| L_d | no concern face, nod or listener smile at his words; only the agent's own brief distress and Claude's words | §2.7 |
| q̂ (set to 0) | the agent never laughs of its own accord; P is never relieved | §2.8 |
| the learned turn-taking (replace by a fixed 6-s rule) | initiative timing no longer follows recorded listeners' timing (testable against held-out Seamless) | §2.9 |
| the cross-entry sign prior | learned appraisal bases may take signs recorded listeners do not show (e.g. a smile at a sad face) | §2.5 |
| the ledger's lag scan (back to lags 0–3 s) | an injected uncounted copy delayed 10–120 s passes at 1.3–2.9 c | §2.13, N1 |
| the D_τ traces | a composed laugh minutes after distress finds the gate more open | §2.4 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **Weakest: almost all situational competence now rests on parts learned from Seamless that are not yet fitted on real data** (g, g_o, L_d, q̂, turn-taking, the sign prior). The risks of revision 7 stand for all of them: too few rare events, actors' listening, transfer from strangers in short conversations to a months-long relationship.
2. **No visible concern before words** above the ceilings (operator's Q24 answer); a silent sad, crying or panicking person sees at most a slight brow (≈ 0.05) until the agent speaks.
3. **The mourner's arrival:** gladness at sight for 2–3 s until the greeting closes g_o.
4. **The first bad-news sentence-final laugh** gets a partial echo of about 0.2–0.5 s.
5. **One person-valence rule for every group:** no group-specific relationship.
6. **Turn-taking without prosody** (D70), until the operator allows audio features.
7. **The ledger's residual:** about 1.2 c (block metric) for an uncounted delayed copy at 0–120 s, 1.3 c at 150–240 s; delays beyond 300 s are outside the scan.
8. **As revision 7:** subscription latency (≈ 2.2 s p50 to first words plus thinking time at effort `low`); the separation rule is structural; the sign mask's residual R38; σ_id far below his real spread misreads him (knowing only).

### 8.2 Falsifiers (state-level, once built)

- **F1, F1′, F1‴, F2–F11, F13–F17** as revision 7; F15 now applies to g, g_o, q̂ and L_d.
- **F12 (deleted with the posture).**
- **F18 (restated).** The agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with σ_id ≥ 0.25 σ_ref.
- **F19.** Any T quantity other than Λ_V(own) in g and g_o changes when only Claude's reply text is changed.
- **F20 (restated).** Live, the laugh synthesizer sounds for more than 0.6 s after a laugh of his that ends a sentence containing words of loss, insult or harm; or ordinary laughter at a sentence's end is not returned within 0.6 s in more than 10 % of cases.
- **F22 (new; D90).** An injected uncounted route copying his channel with a delay of 10–120 s renders above 1.25 c_k by the block-mean metric at 2-s, 10-s or 1-min windows; or the extended ledger changes more than 1 % of frames on natural partners' counted routes.
- **F23 (new).** On held-out Seamless people, the pooled 1-min slope of the agent's channel k (L_d, own laugh) on the speaker's channel k, through words alone, exceeds c_k; or L_d's response to a sentence changes when only the speaker's face is changed.
- **F24 (new).** On held-out Seamless people, g_o, q̂, L_d or the turn-taking model is not better calibrated than a context-free constant.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| research/questions.md: reports 7–9; Q22–Q29 with the operator's answers (Q24, Q26, Q27, Q28, Q29) | in full |
| DECISIONS.md D78, D80–D91 | in full |
| brief.md (Goal, Principles, Foundations research) | in full |
| design-cayley-ledger.md revision 8.3 (saved as .r8.3.md), including every history section | in full |
| design-cayley-ledger.r7.md §0–§2.15; .r6.md §2; .r5.md §2.1–§2.12 (the parts 8.3 inherits by reference) | in full where inherited |
| critique-design-commutator-coupling-routes.md, "Side item"; sims/critique-cc-routes/cayley_ledger_lag.py and its output | in full; its partners re-run with the extended ledger (N1–N3) |
| sims/design-g7/checks.py, `ledger7` | the function, read verbatim by the revision-9 checks |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.** Everything in revision 7's list minus the concern posture and its limits, plus: learned display rules (a context gate on the agent's own displays), a listener-response display and a laugh-likelihood reader fitted on recorded dyads, a learned turn-taking hazard, a lag-complete attenuate-only monitor.

**Clause 2: not met.** The design compositions of revision 7 stand (learning display appropriateness by watching, composed through the listener's own body state; the agent hearing its own Claude-written words). Revision 9 adds no mechanism; it subtracts every hand-written situational rule and routes each behaviour to one of the three allowed sources, which makes the composition cleaner and its innate part smaller.

**My honest verdict.** A recombination, built as the operator asked: the core is unchanged where it carried the copy bounds, and every situational behaviour now depends on what is learned from recorded people or said by Claude. What that costs is stated in "No allowed source". The new-core search continues in the background (D91).

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


## Build-candidate summary (revisions 8.1–8.3) — REPLACED in revision 9

Replaced by the "Build core summary" at the end of this file (D90). The last text of the Build-candidate summary (revision 8.3) is kept verbatim in `design-cayley-ledger.r8.3.md`.

## Critiques of revision 8 and the answer (recorded 2026-11-26T14:51:36Z, under Q19, D81–D85)

**Routes** (critique-8-design-cayley-ledger-routes.md; sims/critique-cayley8-routes/). **One medium failure.**
- **The contingency probe only catches concern answered instantly.** With the author's own answering partner (J33 P4b–d), his sadness ends at 40 s and he then answers the agent's concern look with a 5–90 s lag. The look is then held for the full 15 minutes in every code (posture 0.94; agent inner brow +0.19 to +0.23). All four probes read "held": his evidence drops only 1–12% during the 8-s softening, against a required 20%.
- This is an attracting mutual state (D78's fourth condition) and contradicts the claimed release at 190 s, which holds only at zero lag. The probe's specificity is fine (0 of 24 false releases).
- **Proposed fixes:** a longer probe, a cumulative test across probes, or a time cap on face-only hold; then re-run J33 with lagged answers.
- **No other concrete failure:**
  - the look never depends on the channels it writes;
  - the 0.80-s laugh echo adds no copy route;
  - the gated play laugh can only lower;
  - totals on lip pull, cheek and laugh stay ≤ 0.53 c.
- **Text to correct:**
  - the gated laugh echo reaches 0.53 c, not the declared 0.42 c;
  - declare the look's correlation as a level, with gaze and blink included;
  - distress memory must not read breath sound;
  - the glare silencing reads gaze, so state it as an exception to rule 9′;
  - add a week-0 check for face-tracker crosstalk.
- **Note, not a failure:** the smile echo starts at 0.80 s, inside the first second but late against human 0.4–0.5 s.

**Agent and fitness** (critique-8-design-cayley-ledger-agent.md; sims/critique-cayley8-agent/). **One narrow failure away from a build candidate.** All of critique 7's changes are closed (the posture fix is better than asked); D81 holds (laugh back about 0.83 s); D83 holds.
- **Failure B2:** threat silencing blanks the concern look for a grieving face that squints while looking at the agent (0.00; looking away, 0.99). Sobs rescue it; silence does not. **Fix:** while the glare is up, drop only the brow lowerer and lip press from what the look reads, instead of silencing everything; recheck the anger and squint cases.
- **Trade-off B1, for Q24:** brow-only sadness gets no look before words. The first sign of concern is the spoken bid, at about 50 s (about 110 s for a quiet face). The summary must state this.
- **Build:**
  - ASR is unlikely to finalise words within 0.55 s (Apple's recogniser takes 1.5–2.2 s, anecdotally; Kyutai 1B is about 0.65–0.75 s at p90), so the echo will land at about 0.9–1.0 s, which the design's fallback covers;
  - the spec must require the recogniser to report its finalised extent, so that missing words close the gate;
  - week-0 checks: language coverage (Kyutai 1B is English and French only), runtime on the M1 Pro, the breathing sensor.
- **Novelty:** recombination. A corrected Build-candidate summary is in the critique's §6.2.

**The answer (maintainer).** Both critiques find only narrow, local fixes; the core holds. A short revision 8.1 will apply exactly these:
- the probe fix with a lagged-answer recheck;
- the squint fix;
- the text corrections;
- the ASR finalised-extent requirement and week-0 checks;
- the corrected Build-candidate summary, including the brow-only trade-off.

After one quick check of those fixes, the design goes to the operator as a build candidate (D82). Revision 8 saved as design-cayley-ledger.r8.md.

## Revision 8.1 history (2026-11-26): the narrow fixes

Checks: `sims/design-g81/checks.py` (K1–K5; out.txt), on revision 8's engine loaded unchanged. Revision 8 is saved as `design-cayley-ledger.r8.md`. Nothing either revision-8 critic found sound is changed. Q24 stays open on its recommendation.

| # | Finding (critique 8) | Closed by | Where, check |
|---|---|---|---|
| routes 1 (medium) | the 8-s probe releases answering concern only at zero lag; at 5–90 s the look is held 15 min in every code (posture 0.94, agent brow +0.19 to +0.23); F12 met | the 8-s probe is replaced by a **face-only cap**: after 240 s of face-only hold the look is withdrawn for a 60-s test (later 120 s, the cap doubling); release if his evidence falls below 0.7 of before | §2.1, §2.10; K1: released by 302.5 s at every lag 0–90 s, all codes (genuine-then-answering, lags to 240 s: by 902.5 s); K2: genuine fluctuating sadness released 0 of 24 (P2), 2 of 12 brief (B3, SD 0.20; revision 8: 4 of 12); K3: every J33 case ends, J34 faces one onset and no release; F12 restated (6 min) |
| agent B2 | threat silencing blanks the posture for a grieving face squinting at the agent (0.00) | the glare drops only his BL and LPR from what the posture reads | §2.1, §2.10; K4: grief + squint at the agent 0.00 → 0.99 (on at 2.5 s), quiet code 0.99, different channels 0.50; anger, anger with heavy breathing or lip press, concentration: 0.00 in every code |
| routes text | gated laugh echo bound | R1g declared ≤ 0.53 c BU_L, ≤ 0.31 c LP, ≤ 0.35 c CR | bound table, §3.3, §3.11 |
| routes text | R40′'s pooled slope is unbounded; gaze and blink outside the level row | R40′ declared as a level, gaze-away × (1 − 0.5a) and blink × (1 − 0.3a) included; slopes reported only | bound table, §3.11 |
| routes text | D_s could read his breath sound (BRE in R_p) | D_s reads R_p without BRE | §2.1, R45′; K5 (D_s unchanged by BRE 0.3) |
| routes text | the glare reads his gaze, in W_p | stated as the one exception to rule 9′ (attenuate-only) | §2.2, R48 |
| routes text | face-tracker crosstalk untested; F18 cannot see it | week-0 crosstalk check; F18 note | §6.5, §8.2 |
| agent build | "unknown words close" needs the recogniser's finalised extent | the recogniser must report its finalised-through time; the gate uses words only if it has passed s + λ_w | §2.4.2, §6.1, §6.5 |
| agent build | stable latency ≤ 0.55 s unlikely | expected δ_g ≈ 0.9–1.0 s with a fixed-delay streaming model (e.g. Kyutai 1B), inside the fallback; candidates and fallback named | §2.4.2, §6.1 |
| agent build | week-0 checks | language coverage, runtime on the M1 Pro, breathing sensor (plus the crosstalk check) | §6.5 |
| agent summary | Build-candidate summary | replaced by critique 8's corrected §6.2, with the brow-only trade-off (no look before words; first sign the spoken bid at about 50 s, about 110 s for a quiet face) and the echo timing (0.8–1.0 s, later than a person's 0.4–0.5 s) | Build-candidate summary |

**Costs added by 8.1, stated.** Steady genuine distress held by the face alone now loses the look for a 60-s test after 4 min (and 120 s after each further 8, 16 … min) instead of an 8-s half softening every 3 min; 15-min brow means 0.14–0.19 instead of 0.18–0.22. The test's margin at a 90-s lag is thin (ratio 0.67 against 0.70), and a noisy 90-s answerer can hold the look up to about 17 min or re-trigger it. A different-channel user whose grief is mostly brow lowerer gets a half look when he squints at the agent.

**Status:** revision 8.1; goes to the operator as a build candidate under D82, stated as a recombination, with Q24 open.

## Check of revision 8.1 and the answer (recorded 2026-11-26T16:02:37Z)

**Independent check** (check-cayley-ledger-8.1.md; sims/check-cayley81/). **FAIL, one medium failure.**
- The face-only cap releases the critic's partner at every lag from 0 to 90 s. But when his distress is carried on continuously, a slow answerer (time constant ≥ 300 s at gain 1.0; 240 s at 1.2; 90–180 s at gain 2–3) holds the look for 60 minutes in both the operator's and the different-channel code (agent inner brow +0.19 to +0.24). Because the cap doubles, its tests get rarer, so the hold is effectively permanent: D78 condition 4.
- Pure delays ≥ 90 s cycle the look on and off indefinitely (on 85–91% of the time).
- The squint fix works and opens no copy route; as a side effect, anger with a lip depressor or chin raise now gets the full look (not a failure).
- Totals and laugh-gate timing are consistent.
- **Summary corrections needed:** drop the claim that answering always releases the look; add the cap's cost (about 266 s per hour for steady silent sadness); fix stale "probe" mentions.

**The answer (maintainer).** This is the second failure of the same step: releasing a face-only concern hold by testing whether his face answers. Under the loop rule (same step fails twice: stand it down), test-based release is stood down.
- **Replacement, by construction:** a face-only hold has a fixed, non-doubling maximum. After that, the look continues only while non-face evidence of his distress is present (his words, voice, sobs or breathing). Face-only evidence alone can then restart it only after a fixed refractory period.
- **Why it is robust:** no partner face dynamics, at any lag or gain, can then hold it indefinitely.
- **Cost:** steady silent sadness without voice or words loses the look after the maximum. This trade-off goes to the operator in the build-candidate summary, under Q24.
- **Next:** a small revision 8.2 applies this and the summary corrections, followed by one quick independent check.

## Revision 8.2 history (2026-11-26): test-based release stood down

Checks: `sims/design-g82/checks.py` (L0–L4; out.txt), on revision 8.1's engine and `Agent81` loaded unchanged, as the 8.1 checker did. Revision 8.1 is saved as `design-cayley-ledger.r8.1.md`. Nothing else is changed; Q24 stays open on its recommendation.

| # | Finding (check of 8.1) | Closed by | Where, check |
|---|---|---|---|
| 1 (medium) | a slow answerer (τ ≥ 300 s at gain 1.0; 240 s at 1.2; 90–180 s at gain 2–3) holds the face-only cap's look for 60 min (agent brow +0.19 to +0.24); the doubling cap tests ever more rarely; pure delays ≥ 90 s cycle it on 85–91 % of the time. Second failure of the same step, so under the loop rule test-based release is stood down | the **face-only limit**, a construction: a hold carried by his face alone (no words, voice, sobs or breathing present, N < 0.02) lasts at most **T_max = 180 s**, summed over episodes until non-face evidence appears or the look has been off for T_ref; then his face alone cannot restart, grade or hold it for **T_ref = 120 s**. No doubling, and nothing reads his response to the look. His voice gets its own reading V_v for this purpose | §2.1, §2.10; L1: 65 partners (the checker's slow answerers τ 90–600 s at gain 1.0–3.0, carried on and from 0, pure delays 30–400 s, the routes critic's P1): every face-only stretch ≤ 191.5 s (T_max + the look's rise and fall), posture duty ≤ 60.0 % = T_max/(T_max + T_ref), visible ≤ 63.8 % |
| 1, specificity | genuine distress must keep the look | it does whenever his words, voice, sobs or breathing also show distress | L2: 15 of 15 (words, sad voice, silent panic, sobs, every code; 30 min): one onset, never withdrawn while that evidence is present |
| 1, cost | (new) | steady silent, wordless sadness gets the look 60 % of the time, about 21.7 min off per hour (8.1: 4.4 min) | L3: 60.0 % in every code at V 0.6 and 0.8 |
| 1, J33 | mirrors and answering concern still end | unchanged for mirrors (62.5–66 s); full-strength answering concern now ends at 182.5 s | L4 |
| summary | "released … including when he has only been answering the agent's own look" is false | dropped; the summary states the face-only limit (3 min on, 2 min off at most) | Build-candidate summary |
| summary | the cap's cost is missing | replaced by the new cost under Q24: silent, wordless sadness gets the look only part of the time (60 %); brow-only sadness gets none before words | Build-candidate summary |
| summary, text | stale "probe" mentions | fixed: §0, rule 9′, §2.14, §2.15, §3.4, §3.6, §3.11 (R49), §3.12 P2/P6, §3.14, §3.15, §3.17, §5, §6.2, §7, §8, §10, and the summary's novelty, lesion and Live lists; historical records left as written | — |
| side effect | anger with a lip depressor or chin raise gets the full look (squint fix) | stated in §2.10's costs and in the summary's exceptions and risks | — |

**Costs added by 8.2, stated.**
- Silent, wordless, sob-free distress held by the face alone gets the look 3 min on, 2 min off (60 %).
- A partner whose face keeps answering the look gets it in the same 3-min pieces, at most 60 % of the time; this is bounded, not ended. The agent's brow averages +0.09 to +0.17 over such a cycle.
- A differently expressive user's mildly sad voice reads below presence on the constructed codes (V_v 0.010 at V 0.3; 0.021 at V 0.6).
- One reply's words keep the look for about 21 min (C_L above presence); after that, if he stays silent, the face-only limit applies again.

**Status:** revision 8.2; for one quick independent check, then to the operator as a build candidate under D82, stated as a recombination, with Q24 open.

## Check of revision 8.2 and the answer (recorded 2026-11-26T17:42:47Z)

**Independent check** (check-cayley-ledger-8.2.md; sims/check-cayley82/). **FAIL, one medium failure.**
- The face-only limit holds against every face strategy tried: release-gaming cyclers keyed to the look, a window answerer who knows T_ref, random telegraph faces. The posture is on ≤ 60.0 % with no face-only stretch over T_max; the visible look reaches 196.0 s and 64.9 % because it can bridge a release and its sensitized re-onset (text precision: state the bounds on the on-state, or widen the visible margins). The bounded 3-min cycle itself is not a D78-4 failure.
- **But voice and breathing bypass it.** The 8.1 checker's slow answerer (C1b) who also speaks for 4 s every 80 or 120 s, with no distress words and a voice only 0.03–0.05 softer than his rest, keeps V_v (a 90-s ungated mean) present, so the face-only clock never fills: the look is on 100 % of the time, agent inner brow +0.19 to +0.24, in every code (B3; with a neutral face the same voice releases normally, B3b). A breathing answer at β 0.7–0.9 (his breathing at about 0.52 or more of the constructed silent-panic level) does the same (B1). This is the D78-4 mutual state again. The author's L1 answerers were mute by construction.
- Genuine distress keeps the look (L2 confirmed). Totals, the squint fix and laugh timing are consistent.
- **Minor text:** §2.15 still lists "a contingency test"; §3.14 says "three probes held".
- **Summary corrections:** (1) the "whatever his face does … 60 %" claims hold only for a silent partner; (2) add risks: the V_v threshold against ordinary voice variation, how often the limit is bypassed in real sessions, vocal accommodation to the agent's quieter concerned voice; (3) add the cost that one reply's words keep the look about 21 min; (4) optional: the visible look up to 64–65 % and about 196 s.
- **Suggested fixes (not checked):** only words (C_L) and sobs reset the clock; or voice and breathing only extend T_max (e.g. to 10 min); or a distress-level threshold on fresh voice. Then re-run L1 with his answer in his full code, voice included, and speech every 1–4 min.

**The answer (maintainer).** A narrow revision 8.3 applies the checker's first two suggestions combined: only decoded distress words and sobs reset the face-only clock; his voice and breathing may only extend the face-only maximum to 600 s, never reset it; the refractory period stays 120 s. It re-runs the checker's B1 and B3 partners, checks that genuine distress with words or sobs is still kept, states the new cost to voice-only and breathing-only distress, fixes the minor text and applies summary corrections 1–4.

## Revision 8.3 history (2026-11-26): voice and breathing extend, never reset

Checks: `sims/design-g83/checks.py` (M1–M5; out.txt), on revision 8.2's definitions loaded unchanged, as the 8.2 checker did; the rule is in `Agent83`. Revision 8.2 is saved as `design-cayley-ledger.r8.2.md`. Nothing else is changed; Q24 stays open on its recommendation.

| # | Finding (check of 8.2) | Closed by | Where, check |
|---|---|---|---|
| 1 (medium) | an answering face plus a few slightly soft words every 1–4 min (EN −0.03 / −0.05; V_v from an ungated 90-s mean) or a breathing answer (β 0.7, 0.9) resets the face-only clock: look on 100 %, agent brow +0.19 to +0.24, every code (B1, B3) | **reset narrowed:** only hard evidence H = max(C_L, V_c(v_sob)), his decoded distress words and sobs, resets the clock; soft evidence (V_v, breathing) only extends the maximum from T_max = 180 s to **T_max,ext = 600 s** (summed clock as before); refractory T_ref = 120 s, in which only words or sobs let his face count. By construction, without words or sobs: ≤ 600 s at a stretch, ≤ 600/720 = 0.83 of the time | §2.1, §2.10; M1 (60 min, 26 partners: B3 every 60/80/120/240 s at EN −0.03/−0.05 in three codes, B1 β 0.5/0.7/0.9, both together): longest stretch on **600.0 s** (visible 611.5 s), duty ≤ **81.9 %** (visible 83.6 %); speech every 120–240 s is now withdrawn at 180 s once his voice reading lapses (≤ 271 s, 24.6–65.5 %); β 0.5: 180 s, 16–38 % |
| 1, routes | can words or sobs themselves be an answering route? | argued: C_L is word content appraised through Claude as typed text, and the look carries no words; sobs need v_sob ≥ 0.103 and the agent never sobs. Residual stated: a partner who sobs (v_sob 0.20 × his low-pass of the look) or keeps naming distress in answer holds the look (100 %, brow +0.235); at 0.05–0.10 × the look his sobs stay below presence (60 %) | §2.10; M4 |
| 1, mute faces | the 8.2 bound for face-only partners must not change | unchanged: mute slow answerers, delays and the checker's cyclers ≤ 180.0 s, ≤ 60.0 % (visible ≤ 196.0 s, 64.9 %) | M2 |
| 1, specificity | genuine distress must keep the look | with words or sobs: one onset, never withdrawn (30 min, every code); one reply's words keep it to 1348 s, then the 180-s limit (withdrawn 1527.5 s). **Sad voice only or silent panic only: now 10 min on, 2 min off** (withdrawn at onset + 600 s, back 120 s later; 83.3 % per cycle; agent brow 0.15–0.20) | M3 |
| text | visible stretch 196.0 s vs "T_max + 15 s"; visible duty 64.9 % vs ≤ 0.64 | bounds stated on the posture's on-state; the visible look up to about T + 16 s and 65 % (84 % extended), measured 196.0 s / 64.9 % and 611.5 s / 83.6 % | §0 bound table, §2.10, F12; M5 |
| text | §2.15 "a contingency test"; §3.14 "three probes held" | §2.15: "a fixed hold limit with a refractory period"; §3.14: marked as revision 8's | §2.15, §3.14 |
| summary 1 | "whatever his face does … 60 %" holds only for a silent partner | restated for 8.3: without words or sobs at most 10 of every 12 min (83 %), 3 of every 5 (60 %) if also silent and breathing normally; voice and breathing lengthen, never renew | Build-candidate summary |
| summary 2 | missing risks | added: the V_v threshold against ordinary voice variation (now deciding 3- vs 10-min pieces); how often each limit binds in real sessions; vocal accommodation to the agent's quieter concerned voice; the sob/word residual | Build-candidate summary |
| summary 3 | one reply's words keep the look about 21 min | added as a stated cost and a risk | Build-candidate summary |
| summary 4 | visible margins | added (about 196 s / 612 s, 65 % / 84 %) | Build-candidate summary |

**Costs added by 8.3, stated.**
- Distress shown only in his voice or breathing (speaking sadly without distress words, silent panic) gets the look 10 min on, 2 min off (83.3 %), where 8.2 kept it throughout.
- A sad voice that pauses for more than about 90 s, once the clock has passed 180 s, lets the look be withdrawn at that moment (soft evidence extends only while present).
- A partner who answers the look in face and voice or breathing gets it in 10-min pieces, about 82 % of the time; the agent's brow averages about +0.16 to +0.20 over such a cycle (8.2's face-only cycle: +0.09 to +0.17). Bounded, not ended.
- A partner who sobs or keeps naming his distress in answer to the look holds it indefinitely (residual; not a copy of the agent's face, but a mutual state that can last).
- One reply's words still keep the look for about 21 min.

**Status:** revision 8.3; for one quick independent check of the reset rule (an answerer who also uses words or sobs is the remaining route), then to the operator as a build candidate under D82, stated as a recombination, with Q24 open.

## Check of revision 8.3 and the answer (recorded 2026-11-26T17:57:02Z)

**Independent check** (check-cayley-ledger-8.3.md; sims/check-cayley83/). **PASS: no concrete failure.**
- The 600-s bound holds against voice and breathing timed to the refractory window, voice timed to the clock passing 180 s, release gaming near 600 s and random schedules: never more than 600.0 s or 81.9 % without distress words or sobs (visible 612.0 s, 83.7 %). Neutral words, hedges and "I'm fine" do not reach word presence; "hmm" and "yeah" are removed before decoding.
- The residual (a partner who sobs, or names his distress when the look returns or every 20 min, keeps it 93–100 %, agent brow +0.29 to +0.33) is acceptable, not D78-4: the words alone start nothing, and no agent channel is copied.
- Nothing else broken. One spec precision: the refractory period blanks the whole face load, voice included (text and code differed).
- Summary corrections: the Q24 line still said voice and breathing keep the look steady; voice-only "10 min on" needs speech about every 90 s; 21 min is an upper end; state the word-answer residual concretely.

**The answer (maintainer).** All four summary corrections and the refractory precision are applied above (§2.1 table, §2.10, Build-candidate summary). No mechanism change. **Status:** revision 8.3, checked, no known concrete failure; with the operator as a build candidate (Q27, D87). The concern look is not revised again without the operator's answer to Q27.


## Revision 9 history (2026-11-26): the build core, without situation-specific rules

Written under the operator's answers recorded 2026-11-26T20:40:42Z: Q29 (D88), Q24 (D89), Q27 (D90), Q28 (D91), with Q26 (D85). Revision 8.3 is saved as `design-cayley-ledger.r8.3.md`. Checks: `sims/design-g9/ledger_lag120.py` (N1–N3) and `ledger_lag300.py` (N2b, N3b).

| # | Instruction | Done | Where, check |
|---|---|---|---|
| Q29 / D88 | list every situation-specific rule in 8.3; remove it or justify it as an allowed innate item | 50 rules listed, including those 8.3 inherits from revisions 5–7; 32 removed, 18 kept (6 general learning biases, 4 reflexes, 1 newborn-pattern set, 4 body, 1 per-expression ceiling flagged as an extension, 2 not innate) | "Revision 9 (build core): audit of situation-specific rules" |
| Q24 / D89 | no built-in concern posture; the concern face is learned | the posture and everything around it removed (S1–S9); the built-in word-concern row removed (S28); the concern face is the dyad-learned listener display L_d; before words, only the capped routes | §2.7, §2.10 (marked removed) |
| Q26 / D85 | situational appropriateness from Claude, recorded dyads and general learning biases only | each removed behaviour mapped to its source in the audit and §2.15; new dyad-learned parts g_o, L_d, q̂, turn-taking, sign prior; Claude's words reach the agent through Λ_V(own) in g and g_o | §2.4.3, §2.7–§2.9, §2.12, §2.15, §6.7 |
| Q27 / D90 | build the core: knowing closely, every path capped per expression, Claude through the subscription, learning | the core kept as 8.3 had it, minus the removed rules; every route that reads his face is counted or under the ledger; R40′ and R27′, the two face-reading routes 8.3 declared outside both, are deleted | §0, §3.3, §3.11 |
| Q27 / D90 | close the delay gap: the ledger scans lags to at least 120 s at its 10-s and 60-s windows | 10-s window to 120 s, 60-s window to 300 s; an uncounted copy delayed 10–120 s held to 1.03–1.20 c (8.3's ledger: 1.3–2.9 c), 150–240 s to 1.17–1.34 c; counted routes 0 frames changed | §2.13; N1–N3, N2b, N3b |
| task | check that no copy route opens; fast partial mimicry kept; copying never an attractor | argued by construction, change by change; fast echo back to 0.45 s and untouched by the extended ledger | §3.11, §3.5 |
| task | flag behaviours with no allowed source | six, stated plainly | "Behaviours that now have no allowed source" |

**What revision 9 does not do.** It does not fit anything on Seamless, download anything or run an experiment (D90: the build specification and code are written for the operator's Mac). It does not re-run revision 8's scenario checks: those measured the removed posture and timing on a constructed corpus; the remaining numbers are revision 7's for the unchanged gate form, to be re-measured on the fit.

**Status:** revision 9, the build core; not yet critiqued.

## Build core summary

(Replaces the Build-candidate summary of revisions 8.1–8.3, whose last text is kept verbatim in `design-cayley-ledger.r8.3.md`.)

**One line.** A conversational agent whose face and voice come from an inner state that knows the operator closely but can move toward him only through innately capped, per-expression paths; everything it does that depends on the situation is learned from recorded conversations between people or said by Claude, which it reaches through his Claude Code subscription and which is never told the state.

**What is built.**
- **Knowing him:** per-person calibration; the agent's own inverse Π̃ reading his face (and breathing) as its own state would produce it; the face head H_id taught by his words; the frozen population word reader with a per-person adapter; Λ, how listeners' faces answer words. Knowing never sets a gain on a path to the face.
- **Every path to its own face and voice, capped per expression:** the innate ceilings c_k (smile and laughter highest, sympathy brow 0.20, anger, disgust and contempt 0); the frozen per-channel fast echo at 0.45 s; the held cone, centred at his own baseline; the appraisal display; the free display, driven by words and the agent's own body only; the attenuate-only shadow ledger, which now scans delays to 120 s (10-s window) and 300 s (60-s window).
- **Claude:** three forks per turn through the subscription, resumed from an engine-written transcript; its words are the agent's words; the agent hears them, and that is how Claude regulates it.
- **Innate, and nothing else:** the body (drives for energy, contact, play, curiosity, care; its voice and laugh); reflexes (the fast echo, the threat reflex, the cry–laugh split, startle, the physiological sigh, the social smile back); newborn expressions (smile, cry face, gaze aversion, interest, startle); the per-expression ceilings; general learning biases (a shape-constrained learner, multi-scale memory traces, distress-weighted replay, calibration from calm moments, credit only from separated reports).

**What is learned, and from what.**

| Part | Learned from | When | What it gives |
|---|---|---|---|
| echo gate g | recorded listeners' return of speakers' laughs and smiles | offline, before day 1 | no quick laugh back at grief, mockery, misfortune or after its own serious words |
| own-display gate g_o | recorded listeners' own smile level in context | offline | its own smiles and laughs toned down where people smile less |
| listener display L_d | recorded listeners' faces after speakers' words and turn ends | offline | the concern face at words of trouble, nods, a listener's smile |
| listener-laugh reader q̂ | recorded listeners' laughs after utterances | offline | its own laughs where people laugh; play drive relief |
| turn-taking hazard and turn-end predictor | recorded word timing and faces | offline | when it speaks into a silence and when his turn has ended |
| sign mask and cross-entry sign prior | recorded co-variation of the two people's channels | offline | the directions its learned reactions may take |
| population word reader, Λ | recorded speakers' and listeners' faces after words | offline | what his words mean for him and for a listener |
| calibration, H_id, adapter, Π̃ | him: his face, taught by his words | nightly, weeks | reading him closely, including a quiet or differently expressive face |
| ω | relief and hurt with him (one valence rule) | over about 60 sessions | how strongly its held expressions follow his |
| appraisal bases, Δ | its own display (anticipation, legibility) | nightly | early reactions inside the ceilings; a face that shows its own state |
| word → V map, hurt | its own threat reflex | nightly | hurt at insults |

All dyad learning is on Seamless Interaction, on the operator's Mac only, from face-movement streams and transcripts, the dataset's emotion scores never read (D70, D85).

**What the operator gets on day 1.**
- Replies in about 2.2 s through his subscription, Claude's words with Claude's judgement.
- His smiles and laughs partly returned at about 0.45 s, except where recorded listeners would not return them (as soon as the words are in), and its own laughs where people laugh.
- A learned concern face, slower voice and nods when he tells it something hard; its own brief distress at his need; gladness when a known person arrives (from the second session: the contact drive needs someone to have missed).
- At a glare or a shout aimed at it, it looks away and startles (reflexes); hurt at words comes only once the word → V map has learned which words come with glares.
- Before he says anything, a near-neutral face at his silent distress (brow ≤ 0.03); the agent speaks into the silence when recorded listeners would.

**What it gets after learning (weeks to months).**
- It reads his own face, including a quiet or differently expressive one, as well as his words allow (calibration, H_id).
- Its held expressions follow his within the ceilings as the relationship grows (ω), and its early reactions anticipate its own coming expression (appraisal bases), so a slight concern (about 0.05 brow) can show before words.
- Hurt from words that hurt (the word → V map).
- When to speak first is tuned to its own needs through its world model (𝓜).

**What it no longer does, by the operator's answers** (each stated in "No allowed source"): a clear concern look before words; a sure absence of gladness in the first seconds of a mourner's arrival; the recognition brow flash unless the corpus teaches it; a clean silence at the first bad-news laugh (a 0.2–0.5-s chuckle first); prosody learned from the corpus (turn-end pitch, a quieter concerned voice); relationship strengths that differ by group.

**Risks to watch** (judged on internal state).
- **The dyad fit.** Whether Seamless's recorded listeners show what each learned part needs; the counts of rare events (troubles, mockery and misfortune laughs, openings, distress silences); F15 and F24 on held-out people for g, g_o, q̂, L_d and the turn-taking model; transfer from strangers in 4-min conversations to the operator over months. If a part fails, its behaviour has only Claude's words left.
- **Copying through words.** L_d and q̂ cannot copy his face (causal slope 0), but their pooled correlation with his face through his words is measured on held-out people (F23).
- **The ledger.** How often the extended scan binds on natural partners (expected: never on counted routes; N2); its residual of about 1.2 c for an unlisted delayed copy (F22); delays beyond 300 s are unscanned.
- **Steering.** Clamp his brow, outer brow and lip while he is sad: the agent's brow moves at most within c_BI (F18). Swap Claude's reply for a neutral text: only Λ_V(own) in g and g_o may change (F19). Hold his words fixed and change only his face: L_d and q̂ must not change.
- **Lesions.** The gate, g_o, L_d, q̂, the learned turn-taking, the sign prior, the ledger's lag scan, the traces (§7).
- **Coupling beyond surrogates.** Per-channel pooled slopes at 2 s, 10 s and 1 min under partner-swap, segment-shuffle and timing-resample surrogates, with the gates live.
- **Live.** How the near-neutral face before words reads at his silent distress, and how soon the agent speaks; the mourner's-arrival smile; the partial echo at bad-news laughs (F20); whether one valence for every group feels flat; the recogniser's delivery latency; the breathing sensor.

**Choices left to the operator.**
- **The own-display mask** (S46): keep the agent from ever learning to show anger, disgust or contempt (recommended; it is a per-expression ceiling on its own face rather than on copying), or allow it.
- **Audio features of the recorded dyads:** allowing prosody (pitch, energy) from Seamless would give a learned source for turn-end pitch and a quieter concerned voice; that widens D70.
- **The ledger's 60-s window to 300 s** (adopted; D90 asked for at least 120 s): it costs about 1 MB and holds 150–240-s delays too.

**Novelty verdict: recombination**, stated plainly (§10). The new-core search continues in the background (D91).
