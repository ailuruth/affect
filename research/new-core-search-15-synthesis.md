# Searching for a new core mechanism, fifteenth pass: do held voice levels drift toward a partner's, and should the agent's? (synthesis, 2026-11-28)

## In plain terms

- **The question.** Over minutes of conversation, do people's held voice levels (mean pitch, pitch range, loudness, speaking rate, pauses, voice quality) drift toward their partner's? Which features do, on what time scale, and what drives it? Should the agent's voice do the same? (Reading gap in research/foundations/designs.md, "State at handoff"; voice-synthesis.md open problems; pass 11 §6.)
- **What people do.** It depends on the feature, and the effects are small.
  - **Loudness:** the clearest case. A partner pulls a speaker off her own level, early in the conversation and more over time. Turn to turn, loudness co-varies at r ≈ .2–.5, depending on the corpus.
  - **Speaking rate and pause length:** people keep a different rate and pause length for each of two partners, and switch between them. They close the gap to the current partner by about a tenth.
  - **Mean pitch:** mostly personal. People stay closer to their own pitch in another conversation than to their partner's. They adjust it a little at each turn exchange (r ≈ .14–.28).
  - **Voice quality:** converges late, if at all. On one feature (jitter), matching goes with awkward conversations.
  - **Pitch range:** no open source measured it in conversation.
- **How variable it is.** Very. On average it is often zero, and people differ more than conditions do. Matching on one feature does not predict matching on another (R² ≤ .03). Liking pulls a speaker toward a partner and disliking pushes away. Matching goes with conversations that work. Trying to dominate shows no link.
- **What the build core does now.** This corrects the brief for this pass. The agent's held voice level is *not* forbidden from following him altogether.
  - **It follows his changes.** The held cone already moves the agent's six phrase-level voice settings with *his own changes* away from *his own usual level*. It does so over minutes (traces of 2 min, 20 min, 3 h), with a sign set by the relationship (ω) and inside each setting's limit. After months with a well-liked partner, a change of his held for 10 minutes moves the agent about 0.3 of its limit per unit of his change.
  - **It does not follow his habits.** What the agent cannot do is take on *his habitual level*: talk louder with a habitually loud person, or slower with a habitually slow one. Humans do that (proximity).
- **Keep that difference.** In this engine, taking on his habitual level is by definition a held copy of who he is:
  - the shadow ledger cannot see it, because the shadow keeps his usual level;
  - rule 6 forbids it;
  - the month-swap test would flag it.

  So it is a deliberate difference from humans. It gives a testable marker: the agent's held voice tracks his changes, not his habits.
- **What is missing turn to turn.** The agent's reply does not start a little higher when his last phrase was higher. Humans do this, weakly. The fast echo writes only a zero-mean contour inside the phrase, and the cone is too slow to carry it. Other gaps:
  - his reply latency can only lengthen the agent's delay, never shorten it, because the pipeline floor is about 2 s;
  - there is no response to his low-pitch back-channel cue;
  - L_d's pitch-range and loudness rows are held at 0, because the dyad corpus has no audio (D70).
- **One optional small component (my derivation, unchecked).** A turn-locked echo of how his last phrase differed from his own recent *turn-final* phrases, scaled by ω and carved from the appraisal share. Centring on his turn-final phrases, not on his overall level, is what keeps it from copying his habitual end-of-turn drop. Its effect would be tiny: a few hundredths of a semitone per unit of his change. I would not build it until his M2 recordings can size it.
- **Reward route.** A robot that matched children's pitch and rate drew more smiles and laughter from them. So vocal convergence *would* be a flattery route if it were learned from his reactions. The build core does not learn it from his reactions:
  - the cone's form is innate;
  - ω follows relief from his words and presence, never his face or voice.

  There remains a slow, bounded loop: his warmer words lead to larger ω, which leads to more convergence. It runs through his words only, and Lemma S\* bounds it. The engine need not avoid convergence. It must never tune the coupling by his response.
- **Not a new core.** An evidence map, a correction to how the voice routes were described, one marker and one optional component.

## Scope of this pass

The build core is design-cayley-ledger.md revision 9.1, as specified in research/build/spec.md revision 9.2. The parts read:
- spec §1.1, rows 14–19: F0 level 0.05, FR 0.10, EN 0.05, RT 0.05, PAU 0.05, LAT 0.05; fast gain 0.80 c_k, "within-phrase contour only"; shares (s_C, s_X, s_A) = (0.50, 0.20, 0.35);
- §1.2.4: his phrase-level `[6]` is updated at his phrase end and held;
- §1.4: the fast gear;
- §1.5.1: the held cone;
- §1.6: the shadow and the ledger;
- §1.7: WORLD re-rendering with F0(t) = F0_agent · exp(level + range × template(t));
- design rule 7: phrase targets read y_C, y_A, h, E, A_L, L_d's RT and the envelopes; rule 6; Lemma S and S\*; §2.13 (the ledger at 0.70 c);
- pass 11 (per-channel renderer condition);
- pass 13 §9, the pass-14 critique: a slowly varying gain on a one-sided or DC-carrying partner input becomes a held copy.

Constraints:
- brief Principles 1–3 and 6;
- no emotion labels or named emotion variables below Claude;
- D88 (no situation rules);
- Q18 (per-channel, bounded, sign-flippable, copying never attracting).

**Vocabulary.** Following Levitan & Hirschberg 2011:
- *proximity:* partners' levels are closer than chance, globally (session means) or locally (adjacent turns);
- *convergence:* the distance shrinks over time;
- *synchrony:* the levels co-vary, possibly without being close.

"Held level" means a phrase- or session-level mean that persists for minutes. b_id is his slow per-person baseline (τ_b 6 sessions, latched per session). No proposed quantity uses an emotion label. Where a paper uses affect-classifier labels (Kory-Westlund & Breazeal, Affdex), that is reported as the paper's.

## Sources (notes in research/)

| Note | What | How fully read |
|---|---|---|
| ostrand-chodroff-2021-partner-specific-alignment.md | partner-specific global proximity; 96 speakers alternating between two contrasting partners; 323 features | full text (PMC); Tables 2–3 lost in extraction, taken from prose |
| borrie-lubold-ponbarry-2015-disordered-speech-entrainment.md | local synchrony and proximity of pitch, intensity, jitter and shimmer in 60 dyads; task success | full text (PMC), all tables |
| borrie-2019-syncing-up-crqa-entrainment.md | cross-recurrence against 500 sham dyads; rhythmic, articulatory, phonatory | full text (PMC); Tables 2–4 lost in extraction |
| yu-2013-phonetic-imitation-attitude.md | attitude to the talker sets the sign of VOT imitation (read in place of Babel 2012) | full text (PMC); some coefficients lost |
| kory-westlund-breazeal-2019-robot-speech-entrainment.md | a robot matching children's absolute pitch and rate; children's faces, recall, closeness | full text (PMC); Table 2 lost |

**Used as their notes state:** levitan-2011-2012-acoustic-prosodic-entrainment.md, pardo-2006-phonetic-convergence.md, voice-synthesis.md, eyben-2016-gemaps.md, levinson-torreira-2015-turn-taking-timing.md, ward-tsukahara-2000-backchannel-low-pitch.md.

**Not reachable, so not read and not cited for any claim:**
- *Hosts outside this session's network:*
  - the ISCA archive, which holds Levitan et al. 2015 (cross-linguistic), Levitan et al. 2016 (entraining avatar) and Michalsky & Schoormann 2017;
  - the ACL Anthology and cs.columbia.edu, which hold Levitan et al. 2015 and 2018 and Weise & Levitan 2018;
  - escholarship.org, pubs.asha.org, journals.sagepub.com, doi.org and api.crossref.org.
- *Closed or not found as open copies:* Natale 1975 (JPSP), Gregory & Webster 1996 (JPSP), Pardo et al. 2017 (*AP&P*) and 2018 (*J. Phonetics*), Pardo 2012 (review), Babel 2012, Babel & Bulatov 2012, Borrie & Delfino 2017 and Lubold et al. 2016 (HRI). Cohen Priva, Edelist & Gleason 2017 (*JASA*, convergence of speech rate to the interlocutor's baseline) was also not reached.
- *PMC bot check:* two PMC articles kept serving a bot check after repeated waits: Wynn & Borrie 2022 (the entrainment framework, PMC10437141) and Pardo et al. 2013 (PMC3753450).
- *Secondary only:* Pardo et al. 2017/2018, Weise & Levitan 2018, Cohen Priva & Sanker 2018, Borrie & Liss 2014 and Lubold et al. appear below only as the read papers report them, marked "(as reported by …)".

**Checks.** No simulation. The step responses of the cone and the gain of the proposed centring filter were computed by hand and checked in a one-line Python calculation. They are algebra, not evidence.

## What this pass adds (in short)

1. **A per-feature table** (§1): converge, diverge or neither; global or local; time scale; size and spread; driver.
2. **A correction** (§2): the build core already has a held, relationship-signed co-movement of all six phrase-level voice settings, through the cone. What it excludes is proximity to his habitual level. A statement that "the agent's held voice level may not follow his" is true only of the fast gear.
3. **Proposition V1** (§3, mine): in this engine, any held-level proximity to the partner is a held copy of b_id, and it is invisible to the shadow ledger. So it is a deliberate difference from humans, kept as a marker (§6).
4. **Proposition V2** (§3, mine): late-onset convergence (Levitan's voice quality) comes from the cone's slow traces with a fixed gain. Producing it by a growing or salience-scaled gain is the pass-14 failure.
5. **A local-adjustment inventory** (§4) and **one optional component, Change V** (§4.2, mine, unchecked).
6. **A reward-route verdict** (§5).

---

## 1. Per feature: what people do

| Feature | Global (held over minutes) | Local (turn to turn) | Time course | Size and spread | What drives it | Sources |
|---|---|---|---|---|---|---|
| **Loudness (intensity)** | **Converges.** Proximity to the partner; closer to the partner than to one's own other-session value: the partner pulls a speaker off her baseline | Synchrony r ≈ .47–.50 (Columbia Games); r ≈ .18 in Diapix controls (my conversion of Borrie's 0.59); proximity \|t\| ≈ 1.9 | Early (first half) and increasing | Moderate; varies with corpus and method | Encouragement (mixed and same-sex pairs), trying to be liked; more toward an outlier partner; less with a dysarthric partner | levitan-2011-2012; borrie 2015 |
| **Speaking rate** | **Converges, per partner.** Partner-specific proximity: distance to the current listener 0.94 vs 1.07 syll/s to the other | Synchrony r ≈ .15 | Profile learned within a few minutes of exposure; held and switched across alternating ~70-s rounds | Small (gap closed by about 0.13 syll/s); no cross-level consistency (R² ≤ .027) | Communicative utility (authors' reading); more toward outliers | ostrand-chodroff 2021; levitan |
| **Pauses and gaps** | **Converges, per partner.** Longest pause 3.60 vs 4.06 s; gap length accommodated over a conversation | Floor transfer is anti-phase by definition | Minutes | Small | Utility; partner identity | ostrand-chodroff; levinson-torreira |
| **Mean pitch (F0)** | **Mostly neither.** Personal: closer to self in another session than to the partner; converges across session halves without reaching proximity; only mixed-sex pairs showed global pitch entrainment | Proximity and synchrony r ≈ .14–.28; the only verified turn-level convergence | "Continuous local adjustments, rather than global similarity" | Small; pitch synchrony predicts task success (r = .57 across dyads, .53–.85 within groups) | Trying to be liked (mixed pairs); conversation going well; lower with dysarthric partners | levitan; borrie 2015 |
| **Pitch range** | **Unknown** in conversation. Healthy listeners shifted pitch variation toward recorded dysarthric speech in a quasi-conversation (Borrie & Liss 2014, as reported by Borrie et al. 2015) | — | — | — | — | (gap) |
| **Voice quality** (shimmer, NHR, jitter) | Shimmer and NHR **converge late** (proximity only in the second half). Jitter: no proximity | Weak synchrony (r ≈ .16–.23). Jitter synchrony predicts success in one study (r = .36) | Late onset | Phonatory recurrence beats sham but predicts success least | **Jitter entrainment goes with "awkward" and against "encouragement"**: a candidate for divergence | levitan; borrie 2015, 2019 |
| **Segmental (VOT, formants)** | **Neither on average.** VOT shift 0.47 ms (n.s.); F1 not partner-specific; holistic AXB about 56 % and classifier 55 % | — | Cumulative over ~44 min; persists after the conversation | Individuals −6.8 to +7.8 ms | **Attitude sets the sign** (liking toward, disliking away: 4.5 ms per 2 SD); role and sex in Pardo | yu 2013; ostrand; pardo 2006 |

**Across features:**
- **No unitary gain.** Alignment on one feature or level does not predict alignment on another, across 96 speakers (Ostrand; Weise & Levitan 2018 and Cohen Priva & Sanker 2018, as reported by Ostrand). A single accommodation scalar would misdescribe humans. Per-channel coupling (Q18) is right.
- **Sign is free.** Convergence can reverse with how one regards the partner (Yu). It can be absent on average with large individual spread (Yu, Pardo). One feature's matching marks awkwardness (jitter).
- **Drivers seen:**
  - liking or encouragement (Levitan 2012; Yu);
  - role (Pardo);
  - the partner's speech pathology, which reduces it (Borrie 2015);
  - communicative utility (Ostrand's reading).

  Not trying to dominate (Levitan 2012). Gregory & Webster's status finding was not read.
- **Surrogates.** Against sham dyads, *sustained* co-organisation survives; single-instant matching does not (Borrie 2019). Every other source used only non-partner or non-adjacent baselines.

## 2. What the build core already does with his held voice levels

Four routes write the six phrase-level channels (rule 7): the fast gear, the cone (y_C), the appraisal display (y_A) and T values.

- **Fast gear:** G_k = 0.80 c_k on his phrase features delayed 0.45 s and high-passed at 4 s. It is rendered *only as a zero-mean within-phrase contour*, so it never sets a phrase level. Revision 3 closed the routes that sampled it at onset (K1, K2) for that reason.
- **Held cone (spec §1.5.1):**
  - y_C,k = ω_voice F_m s_C c_k Σ_m (ξ_m,k − b_id,k), with traces τ_m = 20 s, 2 min, 20 min, 3 h and weights F_m = (0, 0.7, 0.2, 0.1). s_C = 0.50 on the voice rows.
  - The latched ω_voice ∈ [−1, 1] is set by the general person-valence rule (S37). Revision 5 illustrated it at about 0.8 after months with a liked partner.
  - **The cone is a held route on every voice channel, F0 level included.**
- **Ledger:** the partner-caused part on each channel is held at ≤ 0.70 c_k at 2-, 10- and 60-s windows, with lags to 300 s. It changed 0 frames of the counted routes on natural partners (design §2.13).
- **L_d:** fitted on Seamless. Only RT has a target (the listener's next-turn word rate after a speaker's words); FR and EN are 0 under D70. It reads T only, so it is a content response, not entrainment to his rate.

**Step response of the cone (my arithmetic).** For a sustained change d of his held level (normalised units), starting at t = 0, the agent's held level moves by ω s_C c_k d Σ_m F_m (1 − e^{−t/τ_m}):

| t | 5 s | 30 s | 2 min | 10 min | 30 min | 60 min |
|---|---|---|---|---|---|---|
| Σ F_m(1 − e^{−t/τ_m}) | 0.029 | 0.160 | 0.463 | 0.779 | 0.871 | 0.918 |
| response at ω = 0.8, per unit d, in c_k | 0.012 | 0.064 | 0.185 | 0.312 | 0.348 | 0.367 |

On F0 level, c = 0.05 in log-F0 units (the renderer's exp(level)) is 0.87 semitone. The ledger's 0.70 c is 0.61 semitone. So a 10-minute change of d = 1 in his normalised F0 level moves the agent about 0.27 semitone.

How much of his natural drift d = 1 represents depends on the normaliser of his F0 channel, which the spec leaves to the voice front end. It is not computed here.

What this shows: the agent's held voice already follows his held *changes* in the human direction (with ω > 0) or away (ω < 0). The shape is early-then-increasing, as Levitan's loudness. The magnitude is set by the relationship, as in Yu and Levitan 2012.

What it does not do: the cone multiplies only ξ − b_id. A habitually loud man at his usual loudness gives the agent exactly the agent's own rest energy. So:
- Ostrand's partner-specific rate and pause levels are not produced;
- Levitan's "closer to the partner than to oneself" on intensity is not produced;
- Kory-Westlund's absolute pitch matching is not produced.

## 3. Whether the build core may produce held-level proximity

**Proposition V1 (my derivation).** Write his phrase-level feature as u_k = b_id,k + d_k. Take any route that makes the agent's held level depend on his habitual level, that is, on b_id,k, as proximity requires (y_k = λ_k (u_k − r_k) with r_k the agent's rest, or any y_k with ∂y_k/∂b_id,k ≠ 0). Then:
1. **The ledger is blind to it.** The shadow replaces u by b_id and holds b_id at its factual value (spec §1.6). The b_id-dependent part is identical in both runs and the partner-caused part is zero. Only its construction gain bounds it.
2. **It is a held copy across sessions.** Across sessions and persons, the term λ_k b_id,k differs by person and persists as long as b_id does (τ_b 6 sessions). It is a copy of who he is, at gain λ_k, and the month-swap surrogate (F1) is built to detect exactly that.
3. **Rule 6 forbids it.** "b_id may only centre a partner input … never a gain on a partner path." Lemma S\* bounds only the ω seam on the cone's *centred* input. It says nothing about a route on b_id itself.

So proximity convergence is not a behaviour that a smaller or slower gain could make safe: in this engine it *is* a held copy. **Verdict: a deliberate difference from humans. Keep it, and test it as a marker (§6).** There is no smallest general change that produces proximity without a held copy, and I propose none.

**Proposition V2 (my derivation; the lesson of pass 14).** Three human patterns tempt a gain change. Each is either already produced with a fixed gain or would be a held copy:
- **Late onset** (Levitan: voice quality reaches proximity only in the second half). The cone's slow traces (20 min, 3 h) already give a response that keeps rising after the 2-min trace has settled (table above: 0.78 at 10 min, 0.92 at 60 min). Producing late onset instead by a gain that grows within the session multiplies a partner input that has DC within a session (his session mean minus b_id). That is Lemma S case (ii): no bound in the pooled slope, so a held copy (pass 14, P1a/C6). The agent has no jitter, shimmer or NHR channels anyway. Voice quality is the TTS identity's (Q1, Principle 8), apart from BRE in the laugh sound.
- **Salience** (Levitan 2012: a pair accommodates more when one speaker is an outlier). A gain g(|d̄|) that rises with his slow deviation makes the output g(|d̄|)·d̄. That is a nonlinear function of his slow level with DC, again unbounded in the pooled slope. The fixed linear cone already gives a larger absolute response to a larger deviation. Levitan's "more relative to baseline" cannot distinguish the two. **Do not add it.**
- **A within-session relationship trace on the voice cone** (ω^s, pass 13's Change A). Pass 14 rejected it for the echo gate on the same grounds. The cone's input has DC within the session, so the case is stronger here. **Excluded.**

## 4. Local, turn-by-turn adjustments

### 4.1 Inventory

| Human local adjustment | Evidence | Build core | Why |
|---|---|---|---|
| Turn-initial phrase level follows his last phrase (pitch, loudness, rate synchrony) | r ≈ .14–.50 (Levitan; Borrie 2015) | **Missing** (≈ 0) | The fast gear is contour-only. The cone's 2-min trace moves about 0.7(1 − e^{−2.2/120}) ≈ 0.013 of a step in the ≈ 2.2-s wait, so its turn-level slope is ≈ 0.005 c_k at ω = 0.8 (my arithmetic) |
| Within-phrase prosodic co-movement | — (no source measured within-phrase) | **Present**: the fast gear's zero-mean contour at 0.45 s, G = 0.80 c_k | — |
| Pitch "reset" after his turn | turn-level pitch proximity (Levitan; Borrie 2015) | **Missing.** The two innate templates start every phrase at the agent's level; nothing references his turn-final pitch | as row 1 |
| Reply latency matched to his | gap accommodation (levinson-torreira); latency shorter in entrained pairs (Levitan 2012) | **One-sided.** LAT is in the cone, but onset = scoring deadline + 0.35 s *or the latency target if later* (spec §1.7): p50 ≈ 2.2 s. The agent can slow toward a slow partner, never speed toward a fast one | pipeline floor, not a rule |
| Back-channel at his low-pitch cue | 350–700 ms after a 110-ms low-pitch region (Ward & Tsukahara) | **Missing**: no nod (S33, D70), no vocal back-channel | D70; Q30 |
| Rate after his words | listeners' rate after speaker's words | **Present as content response**: L_d's RT (T only, fitted on transcripts) | — |
| Pitch-range and loudness response after his words | — | **Held at 0**: L_d's FR and EN have no audio target under D70 | D70 |

### 4.2 Change V: a turn-locked phrase echo centred on his own turn-final phrases (optional; my derivation, unchecked)

This is the smallest general change I can find that gives turn-level synchrony of phrase levels without a held copy.

**Quantities, per voice channel k ∈ {F0, FR, EN, RT, PAU}.** LAT is excluded because it is his latency, already one-sided.
- v_k,n: his phrase-level value at his n-th utterance end (the turn event of §1.2.6). F-typed.
- m_k: an exponential mean of *his turn-final* values only.
  - Update after each utterance end: m_k ← m_k + α_n (v_k,n − m_k), with α_n = 1 − exp(−Δt_n/τ_L).
  - τ_L = 120 s. Δt_n is the time since his previous utterance end, so the rate is counted in time, not events (pass 14, A3).
  - Reset to b_id,k at session start.
- e_k,n = v_k,n − m_k (computed before the update).
- **Output:** the agent's next reply phrase-level target gains y_V,k = ω_voice s_V,k c_k e_k,n, clipped to ±s_V,k c_k. It is applied to the first phrase of the reply only, then returns to 0.
- **Sign and size.** The sign is ω_voice, latched per session; no hand sign is set. The share s_V,k is innate, carved from the appraisal share by
  - 0.636 s_A,k^slow + κ_V s_V,k ≤ 0.636 s_A,k,
  - with κ_V = sup |(1 − z⁻¹)/(1 − (1 − α) z⁻¹)| = 2/(2 − α) ≤ 2 (at α → 1, when his turns are minutes apart).
  - With half the voice appraisal share moved (s_A^slow = 0.175): s_V ≤ 0.056.
  - The pooled voice total stays 0.968 ≤ 0.974.

**Why it is not a held copy.**
1. **Zero mean for a stationary partner, even with a habitual end-of-turn drop.** For stationary turn-final statistics, E[m] = E[v], so E[e] = 0. Centring instead on b_id or on the cone's trace would leave E[e] = δ_tf,k, his habitual difference between turn-final and overall level (people end turns lower and quieter). That would give a held offset ω s_V c_k δ_tf,k: a copy of his personal turn-ending habit, sampled at the agent's onsets. This is the K1/K2 failure in a new form. Centring on his own turn-final phrases removes it.
2. **Drift leaves only a small, transient DC.** If his turn-final level drifts at rate r, the residual DC is ≈ ω s_V c_k r τ_L, which vanishes when he stops drifting. A drift of 0.1 normalised units per 10 min gives ≤ 0.0011 c_k.
3. **No slowly varying gain.** The only gain is ω, latched per session, so the pass-14 lesson is respected. No selection reads anything.
4. **Policed by the ledger.** In the shadow, v = m = b_id, so e = 0. The whole route is partner-caused and the ledger holds it at ≤ 0.70 c_k.

**Expected size.** ≤ ω s_V c_k per unit of his change: at ω = 0.8 on F0 level, 0.0022 log units, about 0.04 semitone. Against human turn-level r ≈ .14–.28 on pitch, this is a token. On EN it is 0.0022 of the normalised range.

**Status.**
- D88 passes: no situation is named.
- D70 gives no dyad audio to fit or check s_V. That is the reason S30's accommodation entries were removed. Here there is no hand sign, but the size is still an unfitted innate share. **Recommendation: watch, not adopt.** Size it on the operator's M2 recordings at most, and adopt only with the operator, or once Q30 widens D70.
- If adopted: re-run J3 and the counted-routes test with Change V, and add it to the ledger regression (as pass 14's B-iii).

## 5. Listeners, convergence and Principle 6

- **What was read.**
  - A robot that matched children's absolute pitch (age table plus last utterance) and rate drew more smiles and laughter and fewer "disappointment" outputs: laughter F = 8.94, valence F = 14.6, with Affdex labels.
  - It did not raise closeness, and it lowered word identification (Kory-Westlund & Breazeal 2019).
  - Pitch-adaptive robot voices raised learning but not self-reported rapport (Lubold et al., as reported there).
  - Humans read convergence as wanting to be liked (Levitan 2012; Communication Accommodation Theory as summarised by Ostrand).
  - No source on distrust of a converging voice was reachable.
- **Consequence.** Convergence *is* a route to the operator's smiles. Any learner that adjusted the agent's voice coupling by his expressions, engagement or time spent would find it and amplify it: Principle 6's flattery path.
- **What the build core does.** The coupling's form is innate. Its only learned scalar ω follows relief events (contact, his words through q̂, curiosity, credited care) and the hurt latch. Those are T values that by rule 10 never read his face or voice. So there is no reward from his expressions.

  One loop remains, the one pass 14 named for ω. The agent converges, then he says warmer or more playful things, then q̂ and play relief rise, then ω_voice rises at 1/60 per session, then the agent converges more. It is open to his words and his presence, closed to his face. It is bounded by |ω| ≤ 1 and Lemma S\* (≤ s_C c_k (1 + ρ)). It is satiable, because relief needs a drive deficit.
- **Verdict.** The engine need not avoid convergence. The cone's relationship-signed co-movement is its own expression, not an instrument. It must avoid three things:
  1. learning any voice-coupling gain or sign from his reactions;
  2. held-level proximity (§3, which also escapes the ledger);
  3. treating his convergence toward the agent as anything but evidence. It is the vocal analogue of S5, measured and never targeted (brief Principle 6; the operator's expressions are evidence only).

## 6. Evaluation markers this pass adds

1. **Changes, not habits (the deliberate difference; from V1).** Run month-swap or person-swap surrogates on his M2 recordings. At equal deviations from each person's b_id, the agent's held phrase levels must not differ between a habitually loud and a habitually quiet speaker, or between a fast and a slow one: proximity ≈ 0, measured with Ostrand's Listener vs Non-listener squared distances. A human listener would show partner-specific rate and pause proximity (Ostrand: 0.94 vs 1.07 syll/s; 3.60 vs 4.06 s). A non-zero agent proximity is a held copy and a bug.
2. **Held co-movement (cone).** Within a session, the agent's EN and RT should follow his sustained deviations with the step shape of §2: about 0.19 c at 2 min and 0.31 c at 10 min at ω = 0.8, with sign(ω). Lesion: set ω_voice to 0 and the co-movement vanishes while the within-phrase contour remains. This replaces voice-synthesis.md's "slow coupling term" prediction with the build core's own route.
3. **No turn-level synchrony unless Change V is adopted.** The turn-level correlation between his last phrase and the agent's next phrase level should be ≈ 0 (≤ 0.005 c slope). A non-zero value would expose an uncounted sampled route.
4. **Test against surrogates.** Any vocal-coupling claim, the agent's or the operator's, is judged against sham pairings (Borrie 2019; moulder-2018), not only non-adjacent turns.

## 7. Novelty verdict

**Component level, not a core.** Nothing here derives a new mechanism.
- V1 and V2 apply the existing type rules (rule 6, rule 10, Lemma S and S\*) and pass 14's lesson to the voice.
- Change V is a first-order high-pass of a turn-sampled signal, centred so that a per-person offset cancels, under a latched gain. It is a standard filter.

What the pass does contribute:
- the correction that the cone already carries held-level co-movement on the voice;
- the identification of human proximity convergence as precisely the b_id copy the engine excludes;
- the turn-final centring that separates a turn-locked echo from a copy of a speaking habit.

No designs.md line.

## 8. What remains open

- **Pitch range** in conversation: no open source found.
- **Held mean pitch in natural conversation over minutes** beyond Levitan's 12 sessions. Pardo et al. 2017/2018, Cohen Priva et al. 2017 (convergence to the partner's *baseline* rate, which bears directly on V1), Natale 1975 and Gregory & Webster 1996 were not reachable.
- **The normaliser of his phrase-level channels.** Without it, "per unit d" cannot be turned into semitones or decibels of his drift, so the cone's absolute effect on his natural variation is unquantified.
- **Whether listeners prefer, ignore or distrust a converging synthetic voice,** in adults and over many sessions. One child study and a second-hand report only. Levitan et al. 2016 (an avatar that entrains) not reached.
- **Whether the operator converges on the agent's voice** (the vocal S5). The agent's six settings are known exactly (pass 11), so it is measurable with Ostrand's design and sham pairings.
- **Gap accommodation is one-sided** while the reply pipeline's floor is about 2 s. This is a latency question (spec §1.8), not a coupling rule.
- **Change V** is unchecked and probably too small to matter. It is recorded so that a later pass need not re-derive why turn-final centring is required.
