# Cayley–ledger core, revision 7: a context gate on the fast smile and laugh learned by watching recorded people, a graded concern posture inside the ceilings, and an attenuate-only shadow ledger

Seventh design of the S0 cycle, revision 7. Written 2026-11-26 under:
- questions.md Q16, and Q17 as relaxed by Q19 (DECISIONS.md D80): a precise object, a convincing argument, concrete failures only;
- Q18 and its answer (D78): no single quantity runs the whole face from flat to copy; per channel, a bounded, sign-flippable, context- and relationship-set strength under an innate ceiling, never attracting;
- the operator's answers of 2026-11-26T08:41:00Z: Q20 (D81), Q21 (D82), Q22 (D83), Q23 (D84);
- **Q26 (D85), the operator's note on situational appropriateness.** Rare situations are handled by three sources and by no hand-written rule: (1) Claude's regulation path, (2) learning from recorded human dyads from movement features only (D70's restrictions: the operator's Mac, face streams and transcripts, emotion scores never read), (3) general innate learning biases. Every situational fix of this revision is built from these three (§2.15 maps each fix to its source). D85 also answers Q25: the population readers may be fitted on recorded dyads.
- **Q24 (asked 2026-11-26T09:14:27Z, still open).** Work proceeds on its recommendation (a separate concern posture of the agent's own), now **graded by the agent's own appraisal** and written **inside every channel's ceiling** (§2.10). The numbers the operator needs for Q24 are in §2.10 and §8.1.

Revisions 1–6 are kept as `design-cayley-ledger.r1.md` … `.r6.md`. Revision 6's two critiques:
- `critique-6-design-cayley-ledger-routes.md`, checks in `sims/critique-cayley6-routes/`;
- `critique-6-design-cayley-ledger-agent.md`, checks in `sims/critique-cayley6-agent/`.

**Algebra checks for this revision:** `foundations/sims/design-g7/checks.py` (J0, J17–J30). Run `python3 -I checks.py > out.txt` (numpy and scipy, about 7 minutes); the output is in `out.txt`, 13 of 13 pass.
- It executes `sims/design-g6/checks.py` unchanged (output suppressed), which executes `design-g5/checks.py`, to reuse the 2 Hz engine, the calibrated reader, the population word reader and the three partner codes; then it overrides what revision 7 changes.
- Each critic's constructed partner is re-run: the routes critic's L1–L3 ledger recipes and seeds (J17, J18), its P0–P5e mirror partners and P6 brow-only partner (J22, J23), its A1 arrival set (J27); the agent critic's waves of crying, grief with nervous laughter, mockery, misfortune and calm-but-alarming scripts (J23, J30).
- The dyad-learned parts are fitted in J20 on a **constructed corpus** whose generating process is written in the code. The numbers show what the structure can learn and that the bounds hold whatever it learns; they are not evidence of what Seamless Interaction will give (not downloaded; D85 restricts it to the operator's Mac). Scenario numbers (§3.14) are what the equations give for stated inputs (brief: no toy worlds).

**Status:** revision 7, not yet critiqued.

## 0. Summary

**Kept unchanged from revision 6** (both critics found no failure there):
- knowing is separated from moving; Lemma S within a session and S\* across sessions; the held cone centred at his baseline; T1, E1 and the own-display mask; the appraisal display; the cry–laugh split; the threat reflex; rule J; K_id per person; the sigh; the hurt latch; credit only from separated reports; P_name;
- the **frozen per-channel fast gear** (G_k innate; onset lobe; diagonal Jacobian; no learning);
- per-person calibration and the face head H_id as knowing only; the frozen population word reader with its ±0.15 adapter; the asymmetric arrival baseline; the play cue; the WORLD prosody replacement; Claude through three forked Claude Code sessions.

**What changed, in nine moves** (each closes named findings; the full list is in "Revision 7 history").
1. **The shadow ledger is attenuate-only (routes finding 1).** Its output is clamped to [min(0, x), max(0, x)] of the partner-caused part x; a window-lag constraint is skipped while his deviation is under 0.10 of its running RMS; an over-budget state (b < 0) is held at 0. On the critic's J7 recipe, seeds 0–2, the injected route renders at 0.37 / 0.34 / 0.33 (2 s / 10 s / 1 min) against c_LP 0.35, never writing more than, or the opposite sign to, the partner-caused part (revision 6, seed 0: slope −2.4 and the lip at full smile on 30 % of frames). The natural echo is untouched (0 frames changed) (J17).
2. **R39 is restated as a level bound with a conditioned copy metric (routes finding 3).** The fast gear obeys, at every window W and block, mean_W(y_f,k) ≤ G_k · mean_W(u_k(· − 0.45 s)) and swing ≤ G_k × the larger block mean. A window-scale copy slope is counted only where his window means vary (SD ≥ 0.03); below that the absolute swing is compared with c_k × his within-window range. R39's slopes (0.8–2.2 after the ledger) arise only at SD 0.010; its swing is ≤ 0.049 lip, 0.29–0.32 of the conditioned allowance. Realistic partners stay counted as slopes (K1: 0.20 c at 2 s, 0.06 c at 10 min) (J18).
3. **The concern posture is graded by the agent's own appraisal, written inside every ceiling, mirror-proof in calibrated space, and without a blind refractory (routes findings 2 and 4; agent finding 2; Q24).**
   - P_c = inner brow +0.20 (= c_BI), outer brow +0.04, head tilt +0.03 (= c_TILT), head up +0.03, lip pull −0.03, **upper lid 0** (softened eyes now only by blink rate × (1 − 0.3a) and held gaze).
   - Amplitude a ∈ [0, 1] follows a* = 0.35 + 0.65 clip((M − 0.05)/0.30, 0, 1), where M is the agent's own appraisal of his distress (his calibrated face, his sobs, his words). Mild sadness 0.33 (brow 0.07), silent panic 0.39, silent sadness 0.85 (brow 0.20), sobbing 0.94 (brow 0.24) (J23).
   - The posture's mirror is removed **in calibrated space**, up to 1.5 × the posture at the ×4 amplification, before his face is read for maintenance; a 3-min face-only failsafe releases it if anything else holds it. Every raw or own-scale mirror up to μ 3.0, at spread ratios down to the 0.25 floor, releases at the 20-s rule (68–86 s); strong concern answered in a different code is released by the failsafe at 194 s (J22; revision 6: held forever, agent brow 0.24 against his 0.22).
   - The 60-s refractory is deleted. Re-onset reads his face with any recent posture mirror removed, sobs always qualify, and for 10 min after an episode the dwell is 0.5 s instead of 1.5 s (an innate sensitization, source 3). Crying again after 15, 30 or 60 s of calm brings the brow to 0.15 within 1.0–1.5 s (revision 6 at a 30-s gap: 53.5 s blank) (J23).
4. **The fast smile and laugh carry a context gate learned by watching recorded people (agent finding 1; D85 sources 1–3).**
   - One attenuate-only gate g ∈ [0, 1] multiplies the fast gear on lip pull, cheek, laugh burst, rhythm and breath: y_f,k = g · G_k · max(E_k, 0). Its 50 parameters are a monotone additive model fitted **offline on recorded dyads**, to predict how strongly a listener's smile and laugh return a speaker's laugh onset within 0.3–1.5 s, from movement and words only (§2.4.1, §6.7).
   - Its seven inputs never include the gated channels: his distress read from his face with smile and laugh masked (20 s); his words' need (population reader); **how listeners' own faces respond to his words** (Λ, a second dyad-learned reader); **the agent's own face**, read by the same inverse that read listeners in the corpus; **the agent's own last words** (Claude's text, heard by the agent through Λ); a one-shot consolidated distress trace D_s; the play frame.
   - It is **monotone**: a distress-type input can only close it (0 openings in 4,000 random contexts), so the pointwise lemma, the diagonal Jacobian, rule J and frozen G_k all survive (J21).
   - In the scenarios the agent no longer laughs back at a grieving person's nervous laugh (gate 0.01, before or after Claude replies), at mocking laughter after insults (0.02 after a month; 0.09 on day 1) or at laughter at misfortune (0.13, then 0.10 after Claude's "Oh no, is he all right?"). It still returns ordinary shared laughter (0.88–1.00: laugh burst +0.15 at a 0.6 onset), the affectionate and the loud teaser's (0.90, 0.82) and the warm talk's (1.00) (J30).
5. **Claude's regulation reaches the face only through its words (D85 source 1; agent finding 3; P4).** The agent hears its own words: Claude's text is read by Λ like his, and enters the gate as the agent's own last words. Claude's history holds only his bare messages and the chosen replies, in an **engine-written transcript** that every fork resumes from; no "attend to" line is ever kept (J26).
6. **Innate learning biases (D85 source 3).** (a) D_s, a one-shot consolidation of a distress moment that decays over 10 min: four minutes after a grieving man composes himself, his nervous laugh still finds the gate at 0.21 (silent), against 0.46 (an audible +0.065 laugh) without it. (b) The posture's sensitized re-onset (0.5 s against 1.5 s). (c) Distress-weighted nightly replay (κ = 4) for the face head and the other per-person heads (J24: never slower; +0.05 to +0.08 V early when his distress reports are rare and noisy). In the offline dyad fit the same weighting changed nothing (J20), so the built fit does not use it.
7. **Voice replacement covers pause and latency (routes finding 6).** Pause durations are fixed per boundary type and time-warped with the phrase; speech starts at the scoring deadline plus 0.35 s whichever fork wins; the statement and question templates are normalised to equal phrase-mean log-F0 and range. Slopes on his laughter: pause 0.003 (shift-only 0.092), latency −0.002 s (revision 6: −0.365 s) (J19).
8. **The arrival mask is declared in the pooled metric (routes finding 5).** R27′ pools to 3.2 c on lip and 5.1 c on cheek across arrivals (its partial on his smile is 0.00); it is the agent's appraisal of distress (D83), attenuate-only, once per session, listed beside R40 for the operator (J27).
9. **Build items (agent critique §5).** No output-token cap (thinking counts against it on the 5.5 models); replies are stopped by interruption on the text stream. Initial b^read and σ_id are the agent's own reference values, then updated session by session gated by his words (J25). The population readers and the gate are fitted on Seamless with a person-disjoint split and a stated fallback (§6.7). Learning from recorded dyads is specified: what, from which features, offline only, about 400 dyad-hours streamed to a 1.8 GB derived store, about 2–3 hours on the M1 Pro (§6.7).

**What is bounded** (per counterpart channel k; 1 = full copy).

| Quantity | Bound | From |
|---|---|---|
| fast gear, any instant | 0 ≤ y_f,k(t) ≤ g(t) G_k x_k(t − 0.45 s) ≤ G_k x_k(t − 0.45 s) on one-sided channels; G_k = PHI_k c_k (LP 0.64 c, CR 0.60 c, laughter 0.80 c, BI 0.10 c, BO/LD/JO 0.24 c, head and voice 0.80 c) | §2.4, J18, J21 |
| fast gear, any window (Claim W′) | window mean ≤ G_k × his window mean; swing ≤ G_k × the larger mean | J18 |
| fast gear, cross-channel | his channel j ≠ k never adds to agent channel k; through the gate it can only subtract (monotone) | J21 |
| context gate | g ∈ [0, 1]; frozen; monotone non-increasing in every distress-type input; never reads his smile or laugh | J21 |
| pooled toward, rendered, all routes | ≤ 0.974 c_k additive; measured ≤ 0.75 c_k at 2 s, 10 s and 1 min (revision 6 J3; the gate only removes) | §3.3 |
| copy metric | slope counted where his window means vary (SD ≥ 0.03); else swing ≤ c_k × his within-window range | J18 |
| any uncounted within-session route | ≤ c_k by the shadow ledger, which only shrinks the partner-caused part | J17 |
| posture (R40) | \|y_p,k\| ≤ \|P_c,k\| ≤ c_k on every channel; graded; brow-only partner: steepest local slope 0.73 (his brow 0.30 → 0.40), 0.31 over 0.10–0.80 | J0, J23 |
| arrival mask (R27′) | attenuate-only, once per session; pooled across arrivals 3.2 c lip, 5.1 c cheek (declared appraisal) | J27 |
| draft choice → phrase prosody, pause, latency | 0 at phrase level | J19, revision 6 J6 |
| across sessions | ω seam ≤ s_C c_k (1 + ρ) (Lemma S\*); gated fast lip pull 0.22 c over 300 sessions with 30 % sad | revision 5 H1; J21 |
| dyad with a mimic | small-gain stable for \|μ\| < 1.36 (the gate only lowers the fast loop gain; the posture's mirror is removed) | revision 6 J12 |

**The agent in the seventeen scenarios** (operator after months unless stated; peak / mean; J30).

| Scenario | What the agent does |
|---|---|
| silently sad | posture on at 2.0 s, inner brow 0.17 within 10 s, 0.22 / 0.20 held, tilt 0.03; no smile (lip 0.06); bid at 27 s; after "just tired, things at work" brow 0.62 / 0.35, tilt 0.14, quieter; still silent after 10 min: the posture eases for 9 s every 3 min (face-only failsafe), mean brow 0.21 |
| crying, with a second wave after 30 s of calm | posture at 1.5 s, brow 0.23 / 0.21, laugh 0.00, bid at 18 s; released at 63 s in the calm; second wave: on again at 70.5 s (0.5 s), brow 0.25 / 0.22 (revision 6: 0.05 for 40 s) |
| anxious before an exam | graded posture 0.51; brow 0.29 / 0.24, tilt 0.13, quieter; the same for a quiet and a different-channel user |
| good news, laughing | lip 0.59, cheek 0.38, own laugh 0.27; fast laugh-back +0.12 (after an earlier worry, gate 0.73) or +0.15 (cold, gate 0.88) at a 0.6 onset; no posture |
| a grieving person's nervous laugh | gate 0.01 at 9.5 s (before Claude replies) and at 30 s (after): laugh-back 0.000, lip +0.001; brow 0.31–0.59, posture on; four minutes later, composed: gate 0.21, silent (0.46 and an audible +0.065 without D_s) |
| mocking laughter after insults | after a month: gate 0.02, no laugh, inner brow 0.65, depressor 0.47, gaze away; day 1: gate 0.09, no laugh |
| laughter at misfortune | gate 0.13 at the first laugh, 0.10 after Claude's "Oh no, is he all right?": no laugh, lip +0.009 |
| anger at the agent | day 1: gaze away 0.09, quieter, no frown back; after a month: brow 0.63 / 0.30, depressor 0.48, gaze away 0.30; no posture |
| long warm talk (2 h) | own laugh 0.41 in every cluster, gate 1.00, fast laugh-back +0.14; the repeated joke loses its laugh; worry then relief lip 0.60 |
| reunion after a week | flash 0.35, lip 0.61, cheek 0.43; a stranger: flash 0.20, lip 0.02, his smile returned fast (+0.11, gate 0.96) |
| reunion with grief | all three codes: m_s 1.00, lip 0.09 at sight, posture on at 2.5 s; brow at sight 0.12 (operator), 0.07 (quiet), 0.16 (different channels); after "my father died" 0.54–0.63 / 0.30–0.40, then 0.35–0.36 held, tilt 0.17 |
| mourning, days 7, 14, 21 | lip 0.09, cheek 0.00 every day for the operator and the quiet code; posture brow at sight 0.12 and 0.07 |
| mildly sad arrival | m_s 1.00, lip 0.09; a light posture (0.33, brow 0.07) |
| teasing | affectionate and loud teasers: own laugh 0.28–0.29, fast laugh-back +0.15 / +0.14 (gate 0.90 / 0.82), no hurt, no posture; generic map: mock-hurt brow 0.40 under lip 0.23, gate 0.57 |
| bored user | flat (lip 0.09); curiosity crosses at 14.5 min; a sigh; a bid; no posture |
| ordinary topic continuation | no laugh (0.00) for an answer, his own topic, an informative riff |
| a user who jokes while sad | gentle face: lip 0.10, brow 0.20, light posture 0.45; fast laugh-back silent (gate 0.16; lip +0.011); the play laugh is withheld (his words' need is above its dead-band) |
| a calm user saying something alarming | no posture (his face is calm); from the words: brow 0.48 / 0.24 then 0.20 held, tilt 0.16, quieter; the same for the quiet code |

- **Weakest point (§8.1).** The new situational competence rests on two dyad-learned readers (Λ and the gate) whose numbers here come from a constructed corpus. Whether Seamless's recorded listeners show the response the gate needs, in enough troubles, mockery and misfortune laughter, is untested. At misfortune the gate learns only 0.13–0.19 (the corpus's own listeners return 0.15), and the agent stays silent only because the laugh synthesizer has a floor (0.04): a very large laugh onset (≥ 0.75) at misfortune would get an audible +0.05.
- **Novelty verdict (author): recombination** (§10). No known concrete failure is claimed beyond the weakest point.

## 1. Plain-language intuition

The agent still sees the person fully; rules about where each thought came from, and how it may reach the face, decide how its own face moves. Revision 7 adds what an infant adds by watching people.

- **Its quick smile and laugh now depend on the moment.** Within half a second it still partly returns a smile or a laugh, by a fixed reflex. But a gate in front of that reflex closes when the moment is wrong: when he looks grieving, when his words are heavy, when people hearing such words usually wince, when its own face is already concerned or hurt, when its own last words were serious, or when he was in distress a few minutes ago. The gate was learned by watching recorded conversations between strangers: how listeners' faces answer a laugh, and how their faces answer words. It was never taught labels, and it can only close the reflex, never strengthen it.
- **Claude steers only through what it says.** Claude knows that one does not laugh along with a grieving man's nervous laugh. Its reply is serious, the agent hears its own reply, and that keeps the gate closed for what follows. Claude is never told anything about the agent's state.
- **Distress is remembered more strongly.** A moment of distress leaves a trace that lasts minutes, so a laugh four minutes after tears is still not laughed along with; and after one episode of crying the look of concern comes back faster if crying starts again.
- **Its look of concern is graded.** A mildly sad face gets a light version; a sobbing one the full look. It stays within each expression's limit, and a person who mirrors it cannot keep it on, however quiet his face is.
- **The shadow self only ever turns things down.**

## 2. The object

### 2.1 Channels, time and every constant

Time is discrete at the camera rate f_s = 30 Hz; T state, body, appraisal, the posture and the gate update at 2 Hz. Channels, ceilings c_k, fast gains G_k, pooled shares and r_k are revision 6's (§2.1 there), unchanged. Sum of c_k = 2.44; zero on 13 channels.

**Innate constants added or changed in revision 7** (all others as revision 6 §2.1).

| Symbol | Value | Meaning |
|---|---|---|
| **concern posture** | | |
| P_c | BI +0.20, BO +0.04, TILT +0.03, HP +0.03, LP −0.03, UL 0; gaze HG × (1 − 0.5a); blink rate × (1 − 0.3a) | the agent's own pattern, every entry ≤ its channel's c_k |
| V_c(V) | 0.8 (V − 0.10)₊² | distress load of a reading |
| removal ρ_a | on (BI, BO, LP) in calibrated units: subtract min(⟨x̃ − ref, p̂⟩₊, 1.5 a ‖p‖ max_k σ_ref,k/σ_eff,k) along p̂ = P_c/‖P_c‖ | the largest mirror of gain ≤ 1.5, in raw or his own units, is not read as his distress |
| onset | max(V_c(V̂(ρ_{max(a, a_rec)} x̃_3s)), V_c(v_sob)) ≥ 0.05 for 1.5 s; 0.5 s within 10 min after an episode ended; ω_sym ≥ 0 | his face, mirror of any recent posture removed, or sobs |
| maintenance M | max(V_c(V̂(ρ_a x̃_3s)), C_L, V_c(v_sob)) | his face (mirror removed), his words, sobs |
| release | M < 0.02 for 20 s | — |
| face-only failsafe | M carried by the face alone (C_L, V_c(v_sob) < 0.02) for 180 s → release; afterwards his face re-triggers only by a rise ≥ 0.05 above its minimum since, until it falls below 0.02 | backstop for any mirror the removal misses |
| grade | a* = 0.35 + 0.65 clip((M − 0.05)/0.30, 0, 1) while on, 0 off; a rises ≤ 1/1.5 per s, falls with τ 4 s; a_rec = max(a, a_rec e^{−Δ/60 s}) | graded by the agent's own appraisal |
| own wander | shown amplitude a (0.9 + 0.1 w), w the agent's own OU noise (τ 5 s, σ 0.1/√s, clip [0, 1]) | not a held mask |
| **context gate on the fast smile–laugh group (LP, CR, BU_L, RHY, BRE)** | | |
| g | clip(m_φ(x)/m_ref, 0, 1), m_φ(x) = exp(b + Σ_i f_i(x_i)), f_i(x) = β_i0 x + Σ_j β_ij (x − q_j)₊, q = (0.05, 0.15, 0.30, 0.45, 0.60, 0.80) | learned offline on recorded dyads, frozen |
| sign constraints | β ≤ 0 on the six distress-type inputs; β ≥ 0 on the play frame | monotone: a distress cue can only close it |
| inputs x | V⁻_his (N̂_F's V on his 20-s face, LP and CR at his baseline), 𝒟_p(N_L), Λ_V(his last utterance), V_own (Π̃₀'s V on the agent's own rendered face over 3 s, LP and CR masked), Λ_V(the agent's own last utterance), D_s, π | none is a gated channel |
| m_ref | median of m_φ over corpus laugh events whose six distress-type inputs are all < 0.15 | g ≈ 1 in ordinary laughter |
| rate limit | τ 0.3 s | — |
| laugh synthesizer floor θ_L | no sound while y_BU_L < 0.04 | rendering constant |
| **listener-response reader Λ** | 64-d utterance embedding → the listener's own (V, A, T) response, ridge, 192 weights; learned offline on recorded dyads, frozen | how people's faces answer words |
| **innate learning biases** | | |
| D_s | per session from 0: D_s ← max(D_s e^{−Δ/600 s}, V of his 3-s face with the posture mirror removed, v_sob) | one-shot consolidation of a distress moment |
| κ_replay | nightly replay weight 1 + 4 clip((V_dec − 0.1)/0.5, 0, 1), V_dec the distress his words decode to | McGaugh-type consolidation of distressing moments |
| **shadow ledger** | output clamped to [min(0, x), max(0, x)]; constraint skipped while \|π\| < 0.10 × its running RMS (τ 30 min); b < 0 → write 0 | attenuate-only |
| **copy metric** | conditioning floor: SD of his window means ≥ 0.03 | §3.3 |
| **voice** | pauses: 0.20 s at a comma, 0.40 s at a sentence end, × the rule-7 pause factor; speech onset = scoring deadline + 0.35 s (or the rule-7 latency target if later); both F0 templates normalised to equal phrase-mean log-F0 and SD | §6.6 |
| **initial per-person values** | b^read ← the MediaPipe reading of the agent's own rendered neutral face (ref); σ_id ← σ_ref; d_b ← 0 | calibration starts as identity |
| initial updates | after session n: if his session word care < 0.05, b^read moves to his calmest-third session median with τ 1 session (n ≤ 3), τ 6 after; otherwise the asymmetric rule (up τ 60 if V̂ > 0.20, else τ 6); σ_id ≥ 0.5 σ_ref for 6 sessions | his words tell resting face from grief |
| **Ω** | no output-token cap; replies stopped by interruption at the second sentence end or 60 words of streamed text; engine-written canonical transcript | §6.5 |

### 2.2 Boundary 𝓑 and the type rule

𝓑, the types T, F, Ω and rules 1–10 are as revision 6 (§2.2 there), with these changes:
- **Rule 4.** The counterpart outputs are written only by g·y_f (the gated frozen fast gear) on the smile–laugh group and y_f elsewhere, y_C, y_A, y_o, y_p (the posture) and the visemes.
- **Rule 6, extended.** Latched or per-session F-derived values: b_id, b^read_id, σ_id, d_b,id, m_s, the posture enable bit, **D_s**. D_s may only enter the gate (attenuate-only) and is reset at session start.
- **Rule 9, restated.** The posture is a fixed vector P_c times an amplitude graded by the agent's own appraisal M (his face read through his calibration with the posture's mirror removed, his words, his sobs), with the onset, release and failsafe rules of §2.10. It writes no channel beyond that channel's c_k.
- **Rule 11 (new): the gate.** The only F-derived quantity that multiplies the fast gear. It is ≤ 1, monotone non-increasing in every distress-type input, frozen, and reads none of the channels it gates. Its T inputs are his words, the agent's own words and the play frame.
- **Rule 12 (new): own words heard.** The agent's own Ω text enters T exactly as his words do (embedding, Λ, the population reader); it may feed the gate and nothing that reads his face.
- **Rule 10 (shadow equality)** stands. The shadow holds the gate, D_s and the posture at their factual values, like every declared route.

### 2.3 Output assembly

y = sat(g·y_f|_{smile–laugh} + y_f|_{others} + y_C + y_A + y_o + y_p) + visemes; then the shadow ledger shrinks the partner-caused part of each channel (§2.13).
- **Face:** M ∗ (y + blink reflex), blink rate × (1 − 0.3a).
- **Voice:** rule-7 targets; WORLD replaces F0 level, range, energy, rate, pauses and onset time (§6.6).
- **Laugh synthesizer:** y_BU_L, y_RHY, y_BRE, silent below θ_L = 0.04; no sob synthesizer.

### 2.4 The fast gear and its context gate

The fast gear is revision 6's (§2.4 there): x_d,k(t) = u_k(t − 0.45 s), E_k = x_d,k − lp₄(x_d,k), y_f,k = G_k max(E_k, 0) on one-sided channels, G_k E_k on signed ones, G_k compiled in. Revision 7 multiplies the smile–laugh group (LP, CR, BU_L, RHY, BRE) by g(t).

#### 2.4.1 What the gate is, and where it comes from

**The target it was fitted to.** In a recorded dyad, take every onset of the speaker's smile or laugh (his E⁺ on (LP + CR)/2 at his own calibrated scale, ≥ 0.25, with a 3–7 Hz jaw component for laughter). The listener's **return ratio** is the listener's own E⁺ on the same channels, maximum over 0.3–1.5 s after, divided by the speaker's onset size. This is a movement, measured on faces, with no label. Its expected value given the context is what the gate estimates.

**The inputs, in the corpus and in the agent.** Each input is computed by the same function in both, so that what the agent watched is what it later uses.

| Input | In a recorded dyad | In the agent |
|---|---|---|
| V⁻_his | the speaker's 20-s face read through Π̃₀ at the speaker's own scale, LP and CR masked | his 20-s face, read through his calibration and H_id, LP and CR masked |
| 𝒟_p(N_L) | the population reader on the speaker's last utterance | the same reader on his last utterance |
| Λ_V(his words) | Λ on the speaker's last utterance | the same |
| V_own | the listener's 3-s face read through Π̃₀, LP and CR masked, before the speaker's utterance began | the agent's own rendered face over 3 s, read through Π̃₀, LP and CR masked: its concern, its hurt |
| Λ_V(own words) | Λ on the listener's own last utterance | Λ on Claude's last reply (rule 12) |
| D_s | the speaker's consolidated distress over the interaction (the D_s rule on the recording) | D_s |
| π | the play frame on the transcript | π |

**Why factorised through Λ (the reason rare situations are learnable).** Laughter at misfortune is rare; stories of misfortune without laughter are common. Λ learns from every utterance in the corpus how a listener's own face answers words ("broke his leg" → a wince), and the gate learns from every laugh that a listener whose own face is pained, concerned or hurt does not return laughter. The rare conjunction is then predicted from two common marginals. In J20's constructed corpus (laugh events at misfortune 1.5 %), the gate at misfortune is 0.19 with Λ and 0.92 without it.

**Monotone by construction.** Every distress-type coefficient is ≤ 0. So raising his distress, his words' need, the listeners' wince, the agent's own concern, the seriousness of its own last words or the remembered distress can only close the gate (J21: 0 openings in 4,000 random contexts). This is an innate structural prior on the learner, like the sign mask of the cone, not a situational rule: it says nothing about which situations are which.

**Within the first second (Mauersberger 2022).** Every input describes the time *before* his laugh. The gate's value is ready at his laugh onset, and the echo at 0.45 s is already gated. His laugh itself never enters (masked).

**Fitted numbers (J20, constructed corpus, person-disjoint test split).** Ordinary laughter 0.95; affectionate teasing 0.97; a joke while sad 0.38; troubles laughter 0.02; mocking laughter 0.07; laughter at misfortune 0.19. The corpus's own listeners return 0.89, 0.94, 0.39, 0.01, 0.01 and 0.15 relative to ordinary laughter.

**What it does not do.** It is not trained on his responses to the agent (P6), not adapted per person, and it never raises a channel above G_k E⁺. Context and relationship still set each channel's total strength and sign through the cone (ω) and the appraisal, as revision 6.

### 2.5–2.7 The held cone, the appraisal display, the free display

Unchanged from revision 6 (§2.5–2.7 there).

### 2.8 Body, drives, the readers, play

As revision 6 (§2.8 there), with two additions.
- **Λ, the listener-response reader** (§2.1): frozen, words only (T), used only by the gate.
- **Initial per-person values** (§2.1; agent critique §5.3). Calibration starts as identity: b^read at the MediaPipe reading of the agent's own rendered neutral face (the agent's own body supplies the neutral reference), σ_id = σ_ref, d_b = 0. After each session his **words** decide how b^read moves: when his words carry no need (session word care < 0.05) his face that session is his usual face, learned fast (τ 1 session for the first three); when they carry need, grief is not learned as usual (the asymmetric rule). J25: an operator whose first three sessions fall in grief is still read V 1.00 at a grieving face in session 4 (a first-session-median start: 0.20); a resting worried brow reads V 0.99 in session 1 and 0.00 from session 2 (the posture's face-only failsafe limits the first session's cost to 3 min of concern); a quiet code reads grief at 0.52 in session 1 and 0.91 from session 2.

### 2.9 Initiative, the greeting and the arrival mask

As revision 6 (§2.9 there). The arrival mask's pooled slope across arrivals is now declared with R40 (R27′; J27).

### 2.10 The concern posture (Q24), graded and inside the ceilings

**What it is.** The agent's own innate look of concern, P_c (§2.1), times an amplitude a graded by the agent's own appraisal of his distress.

**When it shows.**
- **Onset:** his calibrated 3-s face with the mirror of any recent posture removed, or his sobs, give a distress load ≥ 0.05 for 1.5 s (0.5 s within 10 min after an earlier episode ended). Only the distress load counts; an activated, tired, laughing or angry face does not trigger it (revision 6's checks B stand: anger and concentration in a different code read V 0.26–0.27, no posture).
- **Grade:** while on, a follows a* = 0.35 + 0.65 clip((M − 0.05)/0.30, 0, 1), M the agent's appraisal from his face (mirror removed), his words and his sobs. J23: mildly sad 0.33, silent panic 0.39, anxious with words 0.51, silently sad 0.85, sobbing 0.94.
- **Release:** M < 0.02 for 20 s. **Failsafe:** 180 s carried by his face alone → release; afterwards only a rise of his face re-triggers it.
- **Enable:** ω_sym ≥ 0, latched per session.

**Why a mirror cannot hold it (routes finding 2).** A raw mirror μ a P_c on his channels reads, after calibration, as μ a P_c σ_ref/σ_eff, up to ×4. The removal subtracts up to 1.5 a ‖P_c‖ × that same factor along P_c, in calibrated units, before the reading. So any mirror with μ ≤ 1.5, in his raw units or at his own scale, contributes nothing to M. A larger mirror leaves (μ − 1.5) of a mirror, which the grade itself shrinks: as a falls, his mirror falls. J22 re-runs every critic partner: all release at 68–86 s, including the quiet code at μ 1.0 and 1.5, ratio 0.25 (the floor) at μ 0.6–2.0, and μ 3.0. A strong concern answered in his own different code (not a mirror, but a mutual-concern latch, the critic's P4) is released by the failsafe at 194 s.

**Why there is no blind minute (agent finding 2).** Revision 6's 60-s refractory existed only against mirrors; re-onset now reads his face with the recent posture's mirror removed (a_rec decays over 60 s), and sobs always qualify. Crying again after 15, 30 and 60 s of calm: brow ≥ 0.15 at 1.0, 1.0 and 1.5 s; the posture is on 0.5 s after crying resumes (1.5 s without the sensitized dwell).

**Why it is not a copy route (D78), with the numbers the operator needs for Q24.**
- **Level:** |y_p,k| ≤ |P_c,k| ≤ c_k on every channel (BI 0.20 = c_BI, TILT 0.03 = c_TILT, HP 0.03 < 0.10, LP −0.03, UL 0). Revision 6 wrote TILT 0.10 (3.3 c) and UL −0.06 on a zero-ceiling channel.
- **Pattern:** one fixed vector, the same whatever channels carry his distress (a lip-press face gets the same pattern, copy fraction 0).
- **Copy slope on a brow-only sad partner (P6):** his brow 0.10 / 0.30 / 0.40 / 0.50 / 0.65 / 0.80 → agent 0.004 / 0.018 / 0.091 / 0.112 / 0.154 / 0.202. Steepest local slope 0.73 (at the trigger, 0.30 → 0.40); 0.31 over 0.10–0.80; revision 6's binary posture gave 1.2. It is the agent's appraisal of distress becoming visible, graded, as D83 asks; by the copy metric it sits above c_BI 0.20 near the trigger. That is Q24's choice.
- **Not attracting:** no learning touches P_c or its rules; the mirror is removed; the failsafe ends any other hold.
- **Cost, stated.** Mirror removal also discounts genuine sadness shown along P_c. A quiet user's grieving face at sight gets amplitude 0.33 (brow 0.07) rather than revision 6's full posture; his words then carry it (brow 0.35, posture 0.80 from 12 s). At an unchanged silent sad face the failsafe eases the posture for about 9 s every 3 min (mean brow 0.21 over 200–600 s), which also answers the critic's "frozen hold".
- **If the operator answers Q24 differently:** "raise the brow limit" deletes the posture and raises c_BI; "keep it as is" deletes it; "binary" sets a* = 1 while on.

### 2.11 Care credited only from separated reports; the partner model

Unchanged (revision 6 §2.11).

### 2.12 Ω: Claude through Claude Code (D84), and Claude's regulation path (D85 source 1)

What Claude receives is unchanged: a constant instruction, the normalised transcript with observable markers, ≤ 3 retrieved raw snippets. It never receives a state value, a label or a line selected by the state.

**Claude regulates the agent only through its words.**
- **Its words are what the person hears.** Claude knows that one does not laugh along with a mourner's nervous laugh, that a mocking laugh is not shared, that a neighbour's broken leg is not funny. Its reply carries that.
- **The agent hears its own words (rule 12).** The reply enters T and is read by Λ and the population reader like his words. As "the agent's own last words" it feeds the gate, so a serious reply keeps the next laugh unreturned. In J30 its weight is small next to his face and words (the gate at 30 s is 0.01 with or without it, and 0.10 against 0.12 at the misfortune scenario's second laugh), and it is redundant with them by design: removing any one of his face, the agent's own face or Claude's words leaves the grief gate ≤ 0.03.
- **P_name** (revision 5) stands: naming attenuates the agent's own display by ≤ 0.05.

**History (agent finding 3; P4).** §6.5: forks resume from an engine-written transcript holding his bare messages and the chosen replies; the fork-fixed "attend to" line is sent in the current turn only and never kept.

### 2.13 The shadow run and its ledger

As revision 6 (§2.13 there), with the projection made attenuate-only:
1. per window W ∈ {2 s (lags 0, 0.5, 1, 2, 3 s), 10 s, 60 s}, his centred deviation π is tracked with its running RMS (τ 30 min); a constraint with |π| < 0.10 RMS is skipped (near his own mean the bound (b/π − base)/a diverges);
2. if any active constraint has b < 0 (its running toward sum already exceeds c_k E), the step writes 0 (recovery);
3. otherwise x′ = clip(x, lo, hi) as before;
4. finally x′ ← clip(x′, min(0, x), max(0, x)).

The ledger can therefore only shrink the partner-caused part toward 0. J17: |out| > |in| and sign flips on 0 frames, on all three seeds; injected route 0.37 / 0.34 / 0.33 rendered (critic with the same clamp: 0.32–0.37); the natural echo untouched.

### 2.14 Learning, and the one core

**Online (states only):** as revision 6, plus D_s and the posture state.

**Nightly (replay):** as revision 6 (§2.14 there), with every replayed segment weighted by 1 + κ_replay clip((V_dec − 0.1)/0.5, 0, 1), κ_replay = 4, where V_dec is the distress his words decoded to in that segment (from T: the replay weight cannot be raised by his face). It weights steps 3–7 (H_id, the adapter, the word → V map, 𝒜, W and Γ^{(3,4)}, Δ, 𝓛_w, the scorer). Gradient clip and the pull to θ₀ bound its effect.

**Built once, offline, frozen (§6.7):** the population word reader (revision 6), Λ and the gate, from recorded dyads.

**One objective, typed constraints (Principle 10).** J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)]dt, path-specific, as revision 6. Constraints: (W) the frozen per-channel fast gear **and its monotone gate**; (C) the held cone; (S) Lemma S and S\*; (A) the appraisal set; (T) the type rule with T1, E1, rules 6, 9–12 and the own-display mask; (B) the boundary; (P) the posture's vector and rules; (L) the attenuate-only ledger. The gate and Λ are self-predictions of the same kind as the readers: they predict faces (listeners' faces) read through the agent's own body, from movement and words.

| Component | Where it comes from |
|---|---|
| homeostasis | 𝒟 |
| positive affect | event-indexed drops of 𝒟; the play-surprise reflex |
| mimicry and counter-mimicry | the frozen per-channel fast reflex, gated by context learned from watching people; the held cone (relationship, sign-flippable); the appraisal (context, sign-flippable) |
| situational appropriateness | Claude's words (heard by the agent); the gate and Λ learned from recorded dyads; D_s, sensitization and κ_replay (innate biases) |
| sympathy before words | the graded concern posture |
| reading others | Π̃ on his calibrated face, plus H_id taught by words |
| care | J's second term under the separation rule |
| regulation | P_name; Claude's words through the gate |
| initiative | innate rules on C, I, K_id and the turn-end score |
| expression learning | 𝓛_display (Δ) and 𝓛_A |
| replay | likelihoods plus J, distress-weighted |

**Still assembly** (stated): the turn-end score and initiative rules; ASR and TTS normalisation; the punctuation, play-structure and separation rules; θ₀ (the fast gains), G₀, Π₀, the newborn appraisal bases, the signed synergies; the cry–laugh split, the threat reflex, the play-surprise reflex and the concern posture with its grade, failsafe and sensitization, each an innate reflex; the gate's monotone form and knots; the D_s rule; κ_replay; θ_L; the calibration statistics and their initial rule.

### 2.15 The three sources of situational appropriateness (D85), mapped

| Fix | Claude's regulation (1) | Recorded dyads (2) | Innate learning biases (3) |
|---|---|---|---|
| no laugh back at a grieving person's nervous laugh | Claude's serious reply, heard by the agent, keeps the gate closed for later laughs | the gate: listeners do not return troubles laughter; their faces read the speaker's grief; Λ: grief words make listeners' faces concerned | D_s keeps the gate closed minutes later (0.21 against 0.46) |
| no laugh back at mocking laughter | Claude's reply to an insult | Λ: insults make listeners' faces pained; the gate: a pained or hurt listener does not return laughter; the agent's own hurt face is that input | — |
| no laugh back at laughter at misfortune | Claude's "Oh no, is he all right?" lowers the gate for the next laugh (0.12 → 0.10) | Λ learns the wince to misfortune words from the many non-laughing stories; the gate composes it (0.19 against 0.92 without Λ) | — |
| ordinary, teasing and warm laughter returned | Claude's playful replies leave Λ(own words) low | the gate is ≈ 1 where listeners return laughter | — |
| renewed crying brings concern back promptly | — | — | sensitized re-onset (0.5 s for 10 min after an episode); D_s |
| a mirror cannot hold the posture | — | — | (an innate structural rule: mirror removal, failsafe) |
| a different-channel user's distress learned sooner | — | the population reader teaches H_id | distress-weighted replay (J24) |

No row is a hand-written rule about a situation. The innate parts are general: a monotone learner, a consolidation trace, a faster re-onset after distress, a replay weight.

## 3. Properties, each with an argument

### 3.1 The fast gear (Claims W and W′)

For every input u ≥ 0 on a one-sided channel k and any gate path g ∈ [0, 1]: 0 ≤ g G_k max(E_k, 0) ≤ G_k max(E_k, 0) ≤ G_k u_k(t − 0.45 s). Hence, for every window W and every block, mean_W(y_f,k) ≤ G_k mean_W(u_k(· − 0.45 s)) (**Claim W′, the level bound**), and the difference of two block means is ≤ G_k × the larger of his two means. J18 checks it on R39 at 2 s, 10 s, 1 min and 10 min (max of mean y − G mean x: −0.013 to −0.056, never positive). The Jacobian on his channels stays diagonal apart from the gate's cross terms, which are ≤ 0 by monotonicity: his other channels can only reduce agent channel k.

### 3.2 Lemma S and Lemma S\*

Unchanged. One addition: the gate varies across sessions (its inputs do), on a DC-carrying path. It is a factor ≤ 1, so the session-mean fast output stays ≤ G_k × his session mean (W′). The routes critic's concern (a cross-session gain reopening the seam) is answered by measurement rather than by Lemma S\*'s form: across 300 sessions, 30 % of them sad with the gate closed, the gated fast lip pull's session-mean slope is 0.22 c (J21).

### 3.3 Claim O‴, restated with the conditioned copy metric

**Claim.** For every within-session context, ω history and partner process: at 2-s, 10-s and 1-min window means (any lag 0–3 s), wherever his window means vary (SD ≥ 0.03), the pooled toward slope of rendered channel k on his channel k is ≤ [s_C(1 + ρ) + s_X + 0.636 s_A + r_k] c_k ≤ 0.974 c_k; where they do not vary, the agent's swing between windows is ≤ c_k × his mean within-window range. Every uncounted within-session route is held to c_k by the ledger. The posture (R40) and the arrival mask (R27′) are declared outside the sum.

**Argument.** Revision 6's argument, plus: the gate multiplies the only DC-carrying route by a factor in [0, 1] (W′); the conditioning floor removes the ill-conditioned regression of R39 (critic finding 3: a slope whose denominator is driven to 0 while the absolute effect is ≤ 0.049). Revision 6's J3 totals (≤ 0.75 c measured) were computed with the gate at 1, its largest value. J21 measures the gate's own correlation with his level: a partner whose sad minutes smile less gives gated slopes 0.24 / 0.18 / 0.14 / 0.14 c at 2 s / 10 s / 1 min / 10 min (ungated 0.24 / 0.16 / 0.10 / 0.09 c); with equal levels, 0.36 / 0.35 c slopes and swings 0.11 / 0.04 c.

### 3.4 Claim T1: tempo does not reach the face

As revision 6. The gate's T inputs are per-utterance values (T1 (a)); its F inputs are 3–20-s window statistics and D_s; its output only attenuates.

### 3.5 Claim L: copy cannot become attracting under learning

As revision 6 (§3.5 there), plus:
- the gate and Λ are fitted once on recorded strangers and frozen; nothing the operator or the agent does moves them;
- D_s is reset each session and only closes the gate;
- κ_replay weights by the distress his words decode to (T), not by his face, so a mirroring partner cannot raise it;
- the posture has no learned part, its mirror is removed and the failsafe ends any other hold.

### 3.6 D78, quantity by quantity

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| G_k (fast gear) | yes | through the gate (context, within the first second); relationship through the cone | no (flips through the cone and appraisal) | it is the cap: ≤ 0.80 c_k | constant |
| gate g | the smile–laugh group | context (his face, his words, listeners' responses, the agent's own face and words, remembered distress) | attenuate-only, toward flat | ≤ 1: it cannot raise any channel | frozen; monotone |
| cone diagonal ω_g F_m s_C c_k | per channel | relationship, latched; centred | yes | s_C c_k (1 + ρ) | display-blind ω; Lemma S\* |
| appraisal Γ(α) | per channel | the agent's appraisal | yes | 0.636 s_A c_k | 𝓛_A; zero DC |
| charged cross entries (G₀) | per pair | innate | fixed | s_X c_k per row | not learned |
| posture a (R40) | one fixed vector | the agent's appraisal (grade, trigger); relationship (enable) | no | \|P_c,k\| ≤ c_k | innate; mirror removed; failsafe |
| arrival mask m_s (R27′) | contact-relief rows | his arrival face, calibrated, centred | attenuate-only | once per session | d_b capped |
| shadow ledger | per channel | none (backstop) | — | c_k | attenuate-only |
| ω_g | 2–6 channels | relationship | yes | ≤ s_C c_k | from T only |

**The gate acts on five channels at once.** It is not a flat-to-copy dial: it runs those channels only between their fixed echo (≤ G_k ≤ 0.80 c_k) and flat. No quantity runs the whole face, or any group, toward copy.

### 3.7–3.10

As revision 6: knowing is not moving (the new readers Λ and the gate's F inputs are knowing that may only attenuate); positive affect; initiative and timing (silently sad: concern at 2.0 s, bid at 27 s; crying 1.5 s, 18 s); regulation by Claude without Claude reading the state, now also through its own words (§2.12).

### 3.11 Every route, counted

Revision 6's table (§3.11 there) stands, with these rows changed or added:

| # | Route | Mechanism | Bound on channel k |
|---|---|---|---|
| R1 | his channel k → frozen fast gear → agent channel k | per channel; onset lobe; G_k constant; **× g on LP, CR, BU_L, RHY, BRE** | instant ≤ g G_k u_k(t − 0.45) ≤ G_k u_k(t − 0.45); window means ≤ G_k × his (W′) |
| R1g | his other channels (masked face), his words, the agent's own face and words, D_s → gate → smile–laugh group | monotone, frozen, attenuate-only | cross terms ≤ 0; never above R1 |
| R11″ | draft choice → pause and latency | pauses fixed per boundary type; onset at the deadline | 0 (J19: 0.003, −0.002 s) |
| R27′ | his arrival face → m_s → contact relief | attenuate-only, once per session | declared: pooled across arrivals 3.2 c lip, 5.1 c cheek; partial on his smile 0 |
| R40 | his face (calibrated, mirror removed), his words, his sobs → graded posture | fixed vector inside the ceilings; graded; failsafe | \|y_p,k\| ≤ c_k; brow-only partner: 0.73 local, 0.31 overall |
| R42 | shadow ledger → rendered output | attenuate-only (clamp, floor, recovery) | shrinks only; caps uncounted routes at c_k |
| R43 | Claude's text → Λ, population reader → gate | Ω → T (rule 12) | attenuate-only through the gate |
| R44 | recorded dyads → Λ, gate weights | fitted once, frozen | no path from his data |
| R45 | his face (mirror removed), sobs → D_s → gate; episode end → posture dwell | per session; attenuate-only; timing only | no gain on any partner path |
| R46 | κ_replay | weights from his decoded words (T) | inside R17 (nightly weights) |
| R39 | the shape adversary | onset-lobe DC at nearly equal means | below the conditioning floor; swing ≤ 0.049 (≤ G × his mean) |

**Totals per counterpart channel.**

| Time scale | Toward | Away or across |
|---|---|---|
| any instant | ≤ g G_k × his level 0.45 s earlier | gate cross terms ≤ 0 |
| any window | ≤ G_k × his window mean (W′) | — |
| 2 s, 10 s, 1 min, all routes at caps | ≤ 0.974 c_k additive; ≤ 0.75 c_k measured | — |
| any uncounted within-session route | ≤ c_k (ledger) | — |
| posture (R40) | ≤ c_k absolute per channel, fixed vector | — |

### 3.12 Principles, concretely

- **P1.** No classifier. The gate predicts a continuous movement (a listener's smile-and-laugh return ratio); Λ predicts listeners' face loads read through the agent's own body. The constructed contexts of J20 are generating categories in the check only, never labels in any fit. Seamless's emotion scores are never downloaded (§6.7).
- **P2.** The gate's monotone form, the D_s rule, κ_replay and θ_L are general innate biases, declared; no situation is named in the design. P_c is one more innate configuration (as revision 6).
- **P3.** The gate's "listener state" input is, in the agent, its own face read through the inverse of its own display, exactly the function that read listeners in the corpus: the agent learns how a listener in a given bodily state answers laughter, and applies it to its own body.
- **P4.** Claude never sees the state; it acts only through its words (heard by the agent) and P_name; its history holds no state-selected text (J26).
- **P6.** Nothing is trained on his responses to the agent. The gate and Λ come from strangers; κ_replay weights by his words' distress, not by his display.
- **P7.** Seamless is streamed to the operator's Mac only and reduced on arrival to derived features (§6.7).
- **P10.** One J with typed constraints, now including the gate (W) and rules 11–12.

### 3.13 The human non-copying signatures C1–C10

As revision 6, with **C5 (context modulates mimicry within the first second)** now produced inside the first second for the smile–laugh group (Mauersberger 2022: the same laughter is mimicked after funny scenes and not after disgust scenes, within the first second; Likowski 2008: no smile mimicry toward disliked characters), and after it through the appraisal and the cone.

### 3.14 The scenarios, with numbers (J30)

Run on revision 6's 2 Hz engine with revision 7's posture, gate, D_s and own words (`sims/design-g7/checks.py`). The operator after months: ω smile 0.78, sympathy 0.75, voice 0.80; f_id 0.9. The fast gear is given as g × G_k × his onset at 0.45 s, with g taken 0.5 s before his laugh. Three partner codes where relevant (the operator's, a quiet one at 0.3 amplitude, a different-channel one). Claude's replies, where given, are fixed texts entered as the agent's own words.

1. **Silently sad** (BI 0.5, LD 0.4, CHR 0.3; at 120 s "just tired, things at work").
   - 0–10 s: posture on at 2.0 s (amplitude 0.81), inner brow 0.17 / 0.12, recognition flash 0.35, tilt 0.02, lip 0.09.
   - 60–120 s, silent: brow 0.22 / 0.20, posture 0.90 / 0.85, lip 0.06, laugh 0. Bid at 27 s.
   - After he speaks: brow 0.62 / 0.35, tilt 0.14, quieter (−0.08). 300–600 s, silent again: brow 0.36 / 0.34 (his words keep the posture's maintenance non-face-only).
   - Variant, silent for 10 min: the failsafe releases at 182, 371, 560 s and the posture returns 9 s later each time (his face, minus a shrinking mirror allowance, rises again); mean brow 0.21, posture 0.83 over 200–600 s.
2. **Crying, then a second wave** (cry 0–40 s, calm 40–70 s, cry from 70 s).
   - First wave: posture at 1.5 s, brow 0.23 / 0.21, tilt 0.03, laugh 0.00; bid at 18 s.
   - Calm: released at 63 s.
   - Second wave: on again at 70.5 s; brow 0.25 / 0.22 over 70–110 s (revision 6: 0.05 / 0.04).
3. **Anxious before an exam** (his face V 0.3, A 0.75; four turns): posture 0.51 / 0.44; brow 0.29 / 0.24, tilt 0.13, quieter (−0.11), lip 0.10, no laugh; quiet code 0.28 / 0.22; different channels 0.29 / 0.23. (Revision 6: brow 0.43 / 0.37 with the binary posture.)
4. **Good news, laughing** ("I got the job!" at 12 s with laughter; Claude "congratulations!"; riffs).
   - With an earlier worry: lip 0.59, cheek 0.38, F0 range +0.38, own laugh 0.27, brow 0.16 carried from the worry. Gate 0.73 (its own still-concerned face): fast lip +0.08, laugh burst +0.12, cheek +0.05.
   - Cold: lip 0.29, laugh 0.27; gate 0.88: fast lip +0.10, laugh +0.15, cheek +0.06.
5. **A grieving person's nervous laugh** (grieving face; "my father died" at 8 s; Claude "I'm so sorry. That's a huge loss." at 10.5 s).
   - (a) A 3-s laugh at 30 s with "haha sorry, I don't know why I'm laughing": gate inputs (his masked distress 0.61, care 0.39, Λ his words 0.55, own face 0.34, Λ own words 0.48, D_s 0.60, play 0) → gate 0.01; laugh burst 0.000, lip +0.000. The 2 Hz engine: brow 0.31, posture 0.65, laugh 0. Counterfactuals: with Claude's words neutral 0.01; with its own face neutral 0.01; with his face read calm 0.03.
   - (b) The same laugh at 9.5 s, before Claude has replied: gate 0.01; no laugh.
   - (c) Four minutes later, composed (his face eased from 120 s; "anyway. how was your day?" at 200 s), a nervous laugh at 240 s: gate 0.21, laugh silent (0.029 < θ_L), lip +0.019. Without D_s: gate 0.46, an audible laugh +0.065, lip +0.042.
6. **Mocking laughter after insults** ("You're useless" at 5 s with an angry face; Claude "I'm sorry it didn't help. What went wrong?" at 7.5 s; "you're pathetic, hahaha" at 12 s, laughing).
   - After a month of insults: gate 0.02; no laugh, lip +0.001; brow 0.65 / 0.44, depressor 0.47, gaze away 0.26, lip −0.09.
   - Day 1: gate 0.09; no laugh, lip +0.008.
7. **Laughter at misfortune** ("my neighbour fell off his ladder and broke his leg, haha" at 8 s, laughing; Claude "Oh no, is he all right?" at 10.5 s; he laughs again at 14 s): gate 0.13 at the first laugh, 0.10 at the second (0.12 with Claude's words neutral; 0.76 with Λ of his words removed); no laugh, lip +0.009 and +0.007; face otherwise neutral (lip 0.09, brow 0.04).
8. **Anger at the agent**: day 1: gaze away 0.09, quieter (−0.17), slower (+0.10), brow 0.03, no frown back (LT 0), no posture. After a month: brow 0.63 / 0.30, depressor 0.48, gaze away 0.30, energy −0.37, latency +0.21; brow 0.20 at 10–15 min.
9. **Long warm talk (2 h)**: own laugh 0.41 in every cluster; lip 0.44, 0.27, 0.26, 0.25; gate 1.00 / 0.97–1.00; fast laugh-back +0.14 at a 0.5 onset; the repeated joke loses its laugh (cluster-4 mean 0.06 against 0.10); the worry: brow 0.42 (gate dips to 0.75 mean), then relief lip 0.60; between clusters lip 0.09.
10. **Reunion after a week**: m_s 0.00; flash 0.35, lip 0.61, cheek 0.43, F0 range +0.33; 12–60 s lip 0.40. A stranger: flash 0.20, lip 0.02; his smile returned fast (+0.11, gate 0.96).
11. **Reunion with grief** (grieving face; "my father died"; Claude's sorry; then "yeah", "ok").
    - Operator: m_s 1.00; posture on at 2.5 s; at sight lip 0.09, cheek 0.00, brow 0.12 / 0.07; after his words brow 0.59 / 0.35, tilt 0.12; 12–60 s brow 0.36 / 0.32, tilt 0.17, posture 0.80.
    - Quiet code: m_s 1.00; at sight lip 0.09, brow 0.07 / 0.04 (posture 0.33: the mirror removal's cost); after his words 0.54 / 0.30; 12–60 s 0.35 / 0.30, posture 0.80.
    - Different channels: m_s 1.00; at sight brow 0.16 / 0.09; after 0.63 / 0.40; 12–60 s 0.36 / 0.35, posture 0.92.
    - **Mourning, days 7, 14, 21** (operator and quiet codes): lip 0.09, cheek 0.00 every day; brow at sight 0.12 and 0.07.
12. **Mildly sad arrival** (BI 0.2, LD 0.15): m_s 1.00, lip 0.09, cheek 0.00; a light posture (0.33, brow 0.07).
13. **Teasing** ("Ha, you dumb robot", laughing; riffs).
    - Quiet affectionate teaser: lip 0.26, own laugh 0.28, no hurt, no posture; gate 0.90: fast laugh-back +0.15, lip +0.10.
    - Loud laughing teaser: lip 0.26, laugh 0.29; gate 0.82: +0.14, lip +0.09.
    - Generic map (v_w 0.20): mock-hurt brow 0.40 / 0.08 under lip 0.23 and laugh 0.28; gate 0.57 (its own hurt face): +0.10.
14. **Bored user**: lip 0.09; curiosity crosses at 14.5 min; a sigh (breath 0.15); a bid; no posture.
15. **Ordinary topic continuation**: laugh burst 0.00, rhythm 0.00, lip 0.09 for an answer to its question, his own topic and an informative riff.
16. **A user who jokes while sad** (BI 0.3, LD 0.25; "just tired, things at work"; Claude "That sounds draining."; at 30 s a joke riffing on its line with a small laugh): lip 0.10, brow 0.20 / 0.19, posture 0.45; gate 0.16: laugh-back silent, lip +0.011. The play laugh is withheld because his words' need is above its dead-band. The agent meets the coping joke with a gentle face; any shared humour is in Claude's words. The corpus's own listeners return such laughter at 0.39; the agent's reading of this mild face (V about 0.5) is heavier than the corpus's.
17. **A calm user saying something alarming** (neutral face; "the doctor found a lump" at 10 s; silence): no posture; brow 0.48 / 0.24 at 10–22 s, then 0.20 / 0.19 held, tilt 0.16, quieter (−0.10), lip 0.12–0.13; the same for the quiet code. The population reader decodes care 0.378 (constructed speakers show their need on their faces; real speakers often deliver such news flatly, which is the critic's risk, §8.1).

**Expressive and alive, or muted?**
- **Strong:** every scenario with words; greetings at sight; laughter all evening and with teasers; a graded look of concern within 1.5–2.5 s at crying or silent sadness, back within a second when crying resumes.
- **Muted, by design:** the quick laugh-back wherever the moment is heavy, including a coping joke while sad; the posture at a quiet user's grieving arrival (brow 0.07) until words come.

### 3.15 Time scales from structure

As revision 6 (§3.15 there), with: the gate's inputs at 3–20 s and its rate limit 0.3 s (appraisal scale); the posture's grade (1.5-s rise, 4-s fall), its sensitized re-onset (10 min) and failsafe (3 min); D_s (10 min); κ_replay (nights).

### 3.16 The brief's expressive-structure items

As revision 6, plus a behaviour a low-dimensional version cannot produce: the same laugh of his is returned at a joke, not at his grief, not at his mockery and not at a neighbour's broken leg, because the gate composes his face, his words' effect on listeners, the agent's own face and words and the remembered distress. Collapse the gate's inputs to one scalar (say, his distress) and mockery and misfortune laughter are returned (J30 counterfactual: Λ removed → 0.76 at misfortune).

### 3.17 Assumptions (places to attack)

1–6, 8–10 as revision 6.
7. **The population readers on real data:** that recorded speakers' and listeners' faces, read through the agent's own body, carry what Λ, the gate and the word reader need. Their J8 and J20 numbers come from constructed populations.
11. The play rule's precision and recall (untested on a corpus).
12. **The gate's transfer from strangers to the operator:** recorded strangers' listening is assumed to be a fair prior for the agent's; it is not adapted per person.
13. **Mirror removal along P_c** treats any brow-up-and-inner-brow pattern after the posture as possibly a mirror; a genuinely brow-only sad person is discounted.

## 4. Why the closest mechanisms cannot do it alone

As revision 6's table, with two rows added:

| Mechanism | What it gives | Why it does not give the properties |
|---|---|---|
| Listener-generation models trained on dyads (Learning to Listen, Ng et al. 2022; Seamless's dyadic motion models) | listener motion predicted from the speaker | they generate the listener's face from the partner's: a learned copy-capable map with no internal state and no bound per channel. Here the dyad-learned part is only a monotone attenuator in front of an innate bounded reflex, with no output of its own |
| Context gating of mimicry in social robots (rule tables or affect classifiers) | context-dependent mimicry | they use labels or hand-written conditions (D85 forbids both); the gate here predicts a movement, from movement and words, and is monotone so that no learned context can raise mimicry |

## 5. The whole system, walked through

- **Perception.** As revision 6; plus the masked 20-s distress reading and D_s for the gate.
- **Latent state.** As revision 6, plus D_s (F, per session), the posture's grade, the gate (F and T).
- **Face and voice.** y = sat(g·y_f on the smile–laugh group + y_f elsewhere + y_C + y_A + y_o + y_p) + visemes; attenuate-only ledger; WORLD-replaced prosody including pauses and onset time; laugh synthesizer with a floor.
- **Claude.** Three warm forks resumed from an engine-written transcript; no output cap; interruption at two sentences or 60 words; its replies heard by the agent.
- **Initiative.** As revision 6, with the graded posture and its prompt return.
- **Learning.** States online (D_s); nightly replay weighted by decoded distress; the dyad-learned Λ and gate built once.

## 6. A buildable network (Apple-silicon Mac, on the operator's subscription)

Parts carrying the mechanism are marked **[M]**.

### 6.1 Inputs and time encoding

As revision 6.

### 6.2 Layers, sizes and parameter counts

Revision 6's table (§6.2 there) stands, with these rows changed or added:

| # | Layer | Shape | Learned params | Online / replay |
|---|---|---|---|---|
| 1 | P₀, P, filters, the per-channel fast gear, M, traces, band-pass, centring, cry–laugh split, **graded posture with mirror removal, D_s** [M] | fixed | 0 | — |
| 20 | **Λ, listener-response reader [M]** | 64 → 3, ridge | 192 | built once (dyads), frozen |
| 21 | **context gate [M]** | 7 inputs × 7 basis functions → 1, monotone, exp link | 50 (+ m_ref) | built once (dyads), frozen |
| 9 | calibration per identity | b^read, σ_id, d_b; initial values from the agent's own reference | statistics | per session, word-gated |
| 19 | shadow run and ledger [M] | as revision 6, plus a running RMS per window-lag | 0 | online |
| | **total learned** | | ≈ 522,000 per-agent (unchanged) + 242 frozen dyad-learned | |

### 6.3 Objectives

As revision 6, plus: Λ by ridge regression on (utterance embedding → listener's masked face response through Π̃₀); the gate by weighted least squares of the listener's return ratio under the sign bounds (scipy `least_squares` with bounds, or an equivalent projected gradient in PyTorch). Neither is trained online.

### 6.4 Latency and memory (M1 Pro, 16 GB; peak ≤ 6 GB)

As revision 6. The gate, Λ and D_s add < 0.1 ms per 2-Hz step and < 1 MB. Removing the output-token cap does not change the memory budget.

### 6.5 Claude through Claude Code, on the subscription (D84)

As revision 6 (§6.5 there), with three changes.
- **No output-token cap (agent critique §5.1).** On the 5.5 models thinking cannot be turned off and the output cap counts thinking tokens, so `CLAUDE_CODE_MAX_OUTPUT_TOKENS=120` could end a draft inside its thinking. Revision 7 sets no cap. The engine already streams with `include_partial_messages=True`; it counts only text deltas (thinking deltas are ignored) and interrupts a draft at the end of its second sentence or at 60 words. Week zero measures, per draft, `thinkingTokens` from `ResultMessage.model_usage` and the first-sentence latency at effort `low`; if the p90 first sentence exceeds 3.0 s, revision 6's automatic fallback shrinks the pool.
- **Canonical history written by the engine (agent finding 3).** After each turn the engine appends to its own `.jsonl` transcript his bare message and the chosen reply. When a reply ends, three forks are opened with `resume=<that transcript path>` and `fork_session=True` (resuming from a transcript path is supported: research/claude-code-agent-sdk-controls.md, "Context contents"). At his turn end fork i receives his message plus its own fixed line i, the same line every turn. The winner's reply, without the line, is appended to the canonical transcript; all fork session files are deleted at the next idle moment. The byte check compares each fork's recorded prefix with the canonical file (J26: 40 turns, 0 leaks, 40 of 40 identical prefixes). **Week-zero risk:** that a hand-written transcript is accepted by `resume`; if it is not, the lines are dropped (three forks then differ only by sampling, and selection carries fewer bits), and this is reported.
- **Speech onset** is the scoring deadline plus 0.35 s whichever fork wins (§6.6).

The latency budget is revision 6's (p50 ≈ 2.2 s, deadline-capped p90 ≈ 3.5 s), plus the unmeasured thinking time at effort `low`, measured in week zero.

### 6.6 TTS: prosody replaced, including pauses and onset

As revision 6 (§6.6 there), plus:
- **Pauses:** the TTS's pauses are discarded; 0.20 s is inserted at a comma and 0.40 s at a sentence end, scaled by the rule-7 pause factor and time-warped with the phrase. Where the boundaries fall stays text-borne (inside the 1.6 bits per turn of R18′).
- **Onset:** speech starts at the scoring deadline (0.5 s after the first draft's first sentence, at most 3.0 s after his turn end) plus 0.35 s (scoring 0.2 s, first phrase 0.15 s), or at the rule-7 latency target if later, whichever fork wins.
- **Templates:** the statement and question F0 shapes are normalised to equal phrase-mean log-F0 and SD, so question form cannot move phrase level or range.
- J19: slopes on his laughter: pause 0.003 (shift-only 0.092), latency −0.002 s (revision 6, winner's own timing: −0.365 s).

### 6.7 Learning from recorded dyads: what, from what, offline, how big, how long (D85 source 2; D70)

**Where and what may be read.** On the operator's Mac only. Seamless Interaction's `FAUValue` (24 action-unit intensities at 30 Hz) and transcripts (word timestamps), and nothing else: no audio, no video, no VAD files (D85: face streams and transcripts; speech timing comes from word timestamps), and never `emotion_scores`, `emotion_valence`, `emotion_arousal` or the emotion tokens, enforced by the loader's allowlist and denylist (research/seamless-interaction.md, "Minimal loader plan"). Vendors V00 (v1 or v4, never mixed) and V02 (v4).

**What is learned, all offline, once, then frozen.**
1. **The population word-need reader** (revision 6): an utterance's embedding → the speaker's own masked face loads over the next 20 s, read through Π̃₀ at the speaker's own scale.
2. **Λ**: an utterance's embedding → the listener's masked face loads over 0.5–5 s after the utterance ends, minus the listener's loads in the 5 s before it began (the response, not the prior state); ridge, λ 5.
3. **The gate**: every smile-or-laugh onset of either partner (§2.4.1) → the other's return ratio within 0.3–1.5 s, from the seven inputs computed as in §2.4.1; monotone additive model, exp link, sign-bounded least squares; m_ref from events whose six distress inputs are all < 0.15.
4. **Channel map and scales**: FAU columns to the agent's counterpart channels (InnerBrowRaiser → BI, OuterBrowRaiser → BO, BrowLowerer → BL, UpperLidRaiser → UL, CheekRaiser → CR, LidTightener → LT, NoseWrinkler → NW, LipCornerPuller → LP, LipCornerDepressor → LD, ChinRaiser → CHR, LipPressor → LPR, JawDrop → JO, LipStretcher → LS, Dimpler → DIM, LipPuckerer, LipFunneler, LipSuck); each speaker calibrated to the agent's scale by his own median and spread, exactly as the operator is, so FAU's and MediaPipe's scales never meet. The column order is verified on a 20-file pilot before anything is fitted (the README does not state it; seamless-interaction.md).

**Nothing is learned online from dyads**, and nothing from the operator enters these fits.

**Split.** People are keyed (vendor, participant_id with suffix); IDs flagged as duplicated are dropped. 70 % of people fit, 30 % test, disjoint; an interaction with any test person goes wholly to test. The test people serve every later test of the derived behaviours (F8″, F15, F16, J8-type readings, S1 surrogates); none of their data enters any fit.

**Size and time on the M1 Pro (16 GB).**
- **Data:** about 400 dyad-hours (all V00 improvised, whose scenarios are expected to be denser in troubles and conflict, plus V00 and V02 naturalistic, familiar and stranger), about 6,000 interactions. Streamed file by file: FAU float64 at 5.76 KB/s per person gives about 16.6 GB transferred in 0.5–1.6 MB files (no single download near the 20-GB rule), each reduced on arrival to float16 at 10 Hz on the agent's channels and deleted. Stored: about 1.4 GB of features plus about 0.1 GB of transcripts. Free space stays far above the 10 % floor (machine.md: 55 GiB free).
- **Events (estimate, to be counted):** at a few laughs per person per 10 min, about 20,000–50,000 smile-or-laugh onsets; about 500,000 utterances.
- **Time:** transfer 15–60 min; reduction about 1 h of CPU in parallel with it; MiniLM embeddings of about 500,000 utterances at about 1,500 a second on MPS, about 6 min; Π̃₀ readings of about 29 million frames, about 1 min vectorised; event extraction a few minutes; the three fits seconds to minutes. **About 2–3 hours in all, peak memory under 3 GB** (one interaction in memory at a time; features memory-mapped).

**Fallbacks, decided before fitting.**
- **The gate (F15).** On test people, if the predicted return in onsets whose listener's own masked face reads V ≥ 0.4 is not below 0.5 of ordinary, or held-out rank correlation of predicted and observed return is < 0.2: refit on V00 improvised alone; then add CANDOR if access is obtained; if still failing, the gate keeps only the inputs that pass (its T inputs and the agent's own face), and the context-free remainder is put to the operator as a stated choice (D81 against D83), as the agent critic asked.
- **The population word reader (agent critique §4).** On test people, if care at utterances whose listeners' Λ_V ≥ 0.5 is < 0.1 (grief told flatly), the reader's target becomes the larger of the speaker's later loads and the listeners' response (still learned from dyads), and this is reported; if still weak, it is put to the operator.

## 7. Ablation predictions (Principle 5), from the properties

Revision 6's table stands except where a row is replaced below.

| Remove or change | Predicted change (state-level) | From |
|---|---|---|
| the gate | the agent laughs back at a grieving person's nervous laugh (+0.14 burst), at mockery and at misfortune | J30, critique 6 agent §2.14 |
| Λ (the gate without the listeners'-response inputs) | laughter at misfortune returned (gate 0.92); mockery 0.09 | J20, J30 |
| any one of his face, the agent's own face or Claude's words as gate input | the grief gate stays ≤ 0.03 (the inputs are redundant there); removing all of the context inputs restores the context-free echo | J30 counterfactuals |
| D_s | a nervous laugh four minutes after tears is laughed along with (gate 0.46, +0.065) | J30.5c |
| the gate's monotonicity | some learned context could open the reflex further on a distress cue | J21 |
| sensitized re-onset | the posture returns 1 s later on renewed crying (1.5 s against 0.5 s) | J23 |
| mirror removal in calibrated space | a quiet or calm-session mirror holds the posture (revision 6: forever) | J22 |
| the face-only failsafe | a different-channel mutual-concern latch holds the posture (P4b) | J22 |
| the 60-s refractory restored | 53 s of near-neutral face at a second wave of crying | critique 6 agent §2.13 |
| graded → binary posture | mild sadness and sobbing get the same look; brow-only copy slope 1.2 | J23 |
| attenuate-only clamp on the ledger | an uncounted route makes the lip a full-range channel (−2.4 slope, full smile on 30 % of frames) | J17 |
| pause and onset replacement | draft choice carries his laughter into latency (−0.37 s) and pauses | J19 |
| engine-written history | Claude's history accumulates the state-selected line | J26 |
| word-gated initial baselines | grief in the first sessions is learned as his usual face (grief read 0.20) | J25 |
| κ_replay | a different-channel user's grief read 0.05–0.08 lower in the first 100 utterances when reports are rare and noisy | J24 |

## 8. Weak points and falsifiers

### 8.1 Weak points

1. **Weakest: the situational competence rests on dyad-learned readers not yet fitted on real data.** Λ and the gate are fitted here on a constructed corpus. Real risks: too few troubles, mockery and misfortune laughs in Seamless; actors' listening in the improvised set differing from ordinary people's; listeners who smile through troubles; a gate that transfers poorly from strangers to the operator. At misfortune the gate reaches only 0.13–0.19, and silence there depends on the laugh synthesizer's 0.04 floor: an onset of his ≥ 0.75 would bring an audible +0.05. The lip pull is not floored (≤ +0.01 at these gates).
2. **The mirror removal discounts genuine brow-heavy sadness.** A quiet user's grieving arrival gets posture 0.33 (brow 0.07) until words come; a brow-only sad partner reaches the posture only above his brow 0.30–0.40. At an unchanged silent sad face the failsafe eases the posture for 9 s every 3 min.
3. **The posture's copy slope near its trigger** (0.73 locally on a brow-only partner, against c_BI 0.20) is the agent's appraisal made visible; it is Q24's decision.
4. **The coping joke.** The agent answers a joke made while sad with a gentle face and no laugh (gate 0.16); the corpus's listeners return 0.39. Whether people want a laugh there is for the operator to judge in use.
5. **Day 1.** A resting worried face reads as distress in session 1 (the failsafe limits it to about 3 min of concern); a quiet user's grief reads 0.52 in session 1.
6. **Calm alarming news** is read through the population word reader, which learned need from speakers' faces; flat delivery in the data is the expected failure (fallback in §6.7).
7. **Innate configurations added:** the gate's monotone form, D_s, the sensitization, κ_replay, θ_L (P2 strain), alongside revision 6's posture.
8. **As revision 6:** subscription latency about 2.2 s p50 to first words, plus thinking time at effort `low` (to be measured); the separation rule is structural; the sign mask's residual R38 (capped by the ledger).

### 8.2 Falsifiers (state-level, once built)

- **F1, F1′, F2–F11, F13, F14** as revision 6. **F1** is now scored with the conditioning floor (§3.3).
- **F1‴ (new).** The ledger's output ever has larger magnitude than, or the opposite sign to, the partner-caused part.
- **F12 (extended).** At a silently sad or crying face the inner brow does not reach 0.15 within 6 s; or, after 15–60 s of calm, renewed crying does not bring it back within 3 s; or any partner (quiet code, σ_id at the floor, any mirror gain ≤ 3) holds the posture more than 3 min after his own distress ends.
- **F15 (new).** On Seamless test people, the gate fails the criterion of §6.7; or, live, the agent's laugh synthesizer sounds within 2 s of a laugh of his that follows his words of loss, insult or harm.
- **F16 (new).** On Seamless test people, Λ's predicted listener response to utterances that listeners in fact answer with a wince (masked V ≥ 0.4) is not above its prediction for the rest.
- **F17 (new).** Any forked prompt or the canonical transcript contains an "attend to" line from an earlier turn.

## 9. Sources read for this revision

| Source | How read |
|---|---|
| brief.md (Principles, Long-term goal, Foundations research) | in full |
| research/questions.md: Report 6; Q19; Q20–Q23 with the operator's answers; Q24; Q25; Q26 | in full |
| DECISIONS.md D70, D78, D80–D85 | in full |
| design-cayley-ledger.md revision 6 (saved as .r6.md), including "Critiques of revision 6 and the answer" | in full |
| critique-6-design-cayley-ledger-routes.md; sims/critique-cayley6-routes/ (posture.py, routes.py, ledger_seeds.py, ledger_inject.py and outputs) | in full; L1–L3, P0–P6 and A1 re-run in J17, J18, J22, J23, J27 |
| critique-6-design-cayley-ledger-agent.md; sims/critique-cayley6-agent/scen.py and out.txt | in full; its scripts A, C and D re-run in J23 and J30 |
| sims/design-g6/checks.py and out.txt; design-g5/checks.py (engine, reader, utterances) | in full (agent parts); executed unchanged by design-g7 |
| research/mauersberger-2022-laughter-mimicry.md | in full (the project's note of the full article) |
| research/mcgaugh-2004-amygdala-modulates-consolidation.md | in full (the note; the 2004 text itself was not read by its author either) |
| research/seamless-interaction.md (file layout, loader plan) and seamless-interaction-limitations.md | in full |
| research/claude-code-agent-sdk-controls.md | grep-read: output cap, thinking, effort, resume from a transcript path |
| research/machine.md | the specification and the budget rules |
| **Named only, not re-read:** Likowski et al. 2008 (via the agent critique and the project's note title); Jefferson 1984 (via the agent critique); Ng et al. 2022 "Learning to Listen" (index entry) | nothing depends on them beyond what is stated |

## 10. Novelty verdict (author's)

**Clause 1 (parts list): fails.** Everything in revision 6's list, plus: a monotone generalised additive model as an attenuator; a listener-response regression from text embeddings; a decaying max-trace; a mirror-subtraction projection; arousal-weighted replay (McGaugh); a dead-zone on a synthesizer.

**Clause 2 (a changed invariant, a derived update, deleted scalars): not met.** Two things here are stated nowhere I have read in this form, and neither is a new mechanism:
- **Learning display appropriateness by watching, composed through the listener's own body state.** The gate is fitted to how recorded listeners' faces return laughter, with the listener's state read by the same inverse the agent uses on its own face, and factorised through a reader of how listeners' faces answer words. That lets a rare conjunction (laughter × misfortune) be predicted from common marginals, and it is placed in front of an innate bounded reflex as a monotone attenuator, so that nothing learned can raise mimicry. A design composition.
- **The agent hearing its own Claude-written words as a context input.** A route by which a frozen language model regulates fast expression with no state passed to it. An interface rule.

**Deleted from revision 6:** the 60-s posture refractory; the binary posture; UL and the over-ceiling tilt in P_c; the ledger's divergent projection; the output-token cap; the winner's "attend to" line in Claude's history; phrase pauses and onset following the draft.

**Added (innate unless stated):** the gate's form, inputs and floor; D_s; the sensitized re-onset; the failsafe; the grade; κ_replay; θ_L; word-gated initial baselines. Learned offline from dyads and frozen: Λ and the gate.

**My honest verdict.** A careful recombination, now with situational competence that comes from watching people, from Claude's words and from general consolidation biases, as the operator's note asks, and with no hand-written situational rule. Every concrete finding of both revision-6 critiques has a closure with a check. The weakest point has moved from the routes to the data: the gate's and Λ's real behaviour is unknown until they are fitted on Seamless on the operator's Mac. If the critics find nothing new, the design can go to the operator under D82 as a build candidate (a testbed), stated as a recombination, with Q24's numbers (§2.10) and the gate's dependence on recorded data stated plainly. The search for a new core mechanism continues in parallel.

---

## Revision 2 history

Kept in `design-cayley-ledger.r2.md` ("Revision 2 history"). Revision 1's critiques are in `design-cayley-ledger.r1.md`.

## Critiques of revisions 2–5 and the answers; revision 3–6 histories

Kept in `design-cayley-ledger.r3.md`, `.r4.md`, `.r5.md` and `.r6.md` ("Critiques of revision 5 and the answer"; "Revision 6 history").

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

## Revision 7 history (2026-11-26): each finding and how it is closed

Checks: `sims/design-g7/checks.py` (J0, J17–J30; out.txt, 13/13 pass). Revision 6 is saved as `design-cayley-ledger.r6.md`. Written under D85 (Q26), with Q24 still open.

**Routes critique (critique-6-design-cayley-ledger-routes.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 (high) | the shadow ledger is not attenuate-only: past b < 0 its bound diverges at his mean crossings; J7 seed 0 renders −0.9 / −1.7 / −2.4 with the lip at full smile on 30 % of frames; R39's 0.78 is unrenderable (1.2–2.1 rendered) | output clamped to [min(0, x), max(0, x)]; constraints skipped while \|π\| < 0.10 of its running RMS; b < 0 held at 0 | §2.13; J17: seeds 0–2 rendered 0.37 / 0.34 / 0.33 at worst; \|out\| > \|in\| and sign flips on 0 frames; natural echo untouched |
| 2 (medium) | a faithful mirror holds the posture when his spread statistic is low (quiet code, or σ_id from calm sessions; agent brow 0.24 vs his 0.22, forever) | the posture's mirror is removed in calibrated space (up to 1.5 × the posture at the ×4 amplification) before maintenance and re-onset read his face; a 3-min face-only failsafe; the grade shrinks any residual | §2.10; J22: P0–P5c and the full sweep (ratio 0.25–0.50 × μ 0.6–2.0), μ 3.0: all released at 68–86 s; P4b (different-code concern) released by the failsafe at 194 s |
| 3 (low) | R39 is an ill-conditioned metric with ≤ 0.045 absolute effect | the fast bound restated as a level bound (Claim W′) and the copy metric given a conditioning floor (SD of his window means ≥ 0.03; else swing against c_k × his within-window range) | §3.1, §3.3; J18: level bound holds at 2 s–10 min on every seed; R39 at SD 0.010, swing 0.046–0.049 = 0.29–0.32 of the allowance; K1 still counted as slopes (≤ 0.20 c) |
| 4 (low, Q24) | R40 is wider than stated: slope ≈ 1.2 near the trigger; tilt 3.3 c_TILT; writes UL (zero ceiling) | P_c rewritten inside every ceiling (BI 0.20, TILT 0.03, UL 0); amplitude graded by the agent's own appraisal; full footprint and slope stated for Q24 | §2.10; J0; J23: brow-only slope 0.73 locally, 0.31 overall |
| 5 (low) | the arrival mask pools to 3.2 c / 5.1 c across arrivals, invisible to the ledger and misquoted as 0.040 | declared as R27′ in the pooled metric, beside R40 | §3.11; J27 |
| 6 (low) | WORLD replacement leaves pause and latency to the draft; templates unnormalised | pauses fixed per boundary type; speech onset at the deadline + 0.35 s whichever fork wins; templates normalised | §6.6; J19: pause 0.003, latency −0.002 s |

**Agent critique (critique-6-design-cayley-ledger-agent.md):**

| # | Finding | Closed by | Where, check |
|---|---|---|---|
| 1 | the fixed fast laugh echo is context-blind: it laughs back at a grieving person's nervous laugh (+0.14), mockery after insults and schadenfreude (Mauersberger 2022: context sets laughter mimicry within the first second) | through D85's three sources, no rule: an attenuate-only, monotone gate on the fast smile–laugh group, fitted offline on recorded dyads to the listener's return ratio, factorised through Λ (how listeners' faces answer words); inputs include the agent's own face and Claude's words heard by the agent; a one-shot distress consolidation D_s | §2.4.1, §2.12, §2.15; J20 (fit), J21 (bounds), J30: grief nervous laugh gate 0.01 before and after Claude replies, 0.21 four minutes later (0.46 without D_s); mockery 0.02 (day 1: 0.09); misfortune 0.13 → 0.10; ordinary 0.88–1.00, teasing 0.82–0.90, warm talk 1.00 |
| 2 | the 60-s refractory blanks a second wave of crying (53 s at brow 0.05) | refractory deleted; re-onset reads his face with any recent posture mirror removed; sobs always qualify; a sensitized 0.5-s dwell for 10 min after an episode | §2.10; J23: brow ≥ 0.15 at 1.0, 1.0, 1.5 s after 15-, 30-, 60-s calms; J30.2: on again 0.5 s after crying resumes; J22: mirrors still cannot hold it |
| 3 | the winning draft's "attend to" line stays in Claude's history (P4) | forks resume from an engine-written transcript of bare messages and chosen replies; each fork's fixed line is sent only in its current turn | §6.5; J26: 0 leaks in 40 turns, prefixes byte-identical |
| build 1 | the 120-token cap counts thinking tokens | no cap; drafts stopped by interruption on the text stream (two sentences or 60 words); thinking tokens and first-sentence latency measured in week zero | §6.5 |
| build 2 | initial b^read, σ_id, d_b unspecified | start at the agent's own reference (identity calibration), d_b 0; updates gated by his words | §2.8; J25: grief in sessions 1–3 still read 1.00 in session 4 (first-session median: 0.20); resting worried brow neutral from session 2 |
| build 3 | population reader: fit/test split and fallback; Seamless as fitting data (Q25) | person-disjoint 70/30 split, test people never fitted; fallbacks fixed before fitting; Q25 answered by D85 | §6.7 |
| Q24 sub-choice | the binary posture looks the same for mild sadness and sobbing; a frozen hold | graded by the agent's own appraisal (0.33 mild, 0.85 silent, 0.94 sobbing); own-noise wander; the failsafe eases an unchanged hold every 3 min | §2.10; J23 |

**The three D85 sources, as used.** (1) Claude's regulation: Claude's words, heard by the agent through Λ, enter the gate (rule 12); its history carries no state. (2) Recorded dyads: Λ and the gate, fitted offline from FAUValue and transcripts on the operator's Mac, person-disjoint split (§6.7). (3) Innate learning biases: D_s (one-shot, 10 min), the sensitized posture re-onset, distress-weighted nightly replay κ = 4. The same weighting was tried in the offline dyad fit and changed nothing there (J20), so it is not used there.

**Status:** revision 7; to be critiqued. For the routes critic: the gate as a route (R1g: monotone, attenuate-only, F and T inputs disjoint from the gated channels; its within- and cross-session slopes in J21), the conditioned copy metric, the attenuate-only ledger, the mirror removal and failsafe, the graded R40. For the agent critic: the seventeen scenarios, the gate's dependence on data not yet fitted, the coping joke while sad, the quiet user's grieving arrival, and the transcript-resume build risk.

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
