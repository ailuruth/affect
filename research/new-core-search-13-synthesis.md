# Searching for a new core mechanism, thirteenth pass: how fast, and by what signal, do a person's reactions to a partner become partner-specific? (synthesis, 2026-11-28)

## In plain terms

- **The question.** Gap 6 says human mimicry changes shape with the partner: each expression is gated on its own, some responses flip sign, matching comes before context, and partner history is learned within minutes. Gap 8 says a leftover same-sign transfer (Parkinson & Simons 2009) must be explained. This pass asks how fast the partner-specific change happens, per expression, what drives it, whether the drive is the partner's expression used as a reward (forbidden by Principle 6) or a prediction, and whether the build core can produce it.
- **What the data say.**
  - **Speed.** About 30 pairings of a face with the observer's own wins or losses, over roughly a quarter of an hour, are enough to cut smile return to the losing face from the first second of its smile. The change lasts at least half an hour without further pairings (Korb et al. 2019, replicating Sims et al. 2012). One sentence about a partner's attitude changes smile return within a 5-min conversation (Heerey & Gilder 2019). An instructed change of whose outcome a face reports flips the sign of the response at once, with no learning needed (Hofree et al. 2018).
  - **Per expression.** Each change acts on one expression, not all. Smile return changes while the response to angry faces does not (Korb). Polite smiles lose their return while genuine ones keep it (Heerey & Gilder). A smile at a bad scene draws a brow response, while frowns are not affected (Kirkham et al. 2015).
  - **Time within a trial.** Context acts on smiles from the first second when the context is already known (Korb), and at about 2–4 s when it arrives with the face (Kirkham; Hofree).
  - **What does not carry over.** How well a face agreed with events, learned without attention, changed trust but did not change later mimicry (Kirkham).
- **What drives it.** In every study read, the change follows what the partner means for the observer's own outcome: money the face predicts, an outcome the face reports, words about the partner's attitude, or whether the face agrees with a shared scene. Only the Heerey studies put the partner's smile itself in the role of a reward. There it works through how much people value seeing a smile, which is the route Principle 6 forbids.
- **Can the build core do it?** Partly, and it is limited in three places.
  - **The place a relation can act.** Within a session, a context may change only paths whose partner input has no constant part (Lemma S). In the build core those are the fast echo's gate and the appraisal display. The held cone's gain is fixed for the session.
  - **What exists now.** The relation itself (ω) is learned from good and bad outcomes attributed to the partner, in the right direction, but it moves only 1/60 of the way per session.
  - **What is out of reach by design.** Reading the sign of an event from his face alone. Copying a frown. Telling a polite from a genuine smile in the echo gate. Learned cross-channel counter-responses (smiling at his distress).
- **The smallest general change (my derivation, not checked).** It has two parts.
  1. **A session relation trace ω^s.** The same person-valence rule, run within the session from the session's own word and presence events. It becomes one more input to the frozen echo gate and to the appraisal's selection, never a gain on the cone.
  2. **A fast band for the appraisal display.** A 0.5–4 s band-pass of his face, used inside the appraisal display's existing per-channel set, so context can sign each channel's response 1–4 s after his expression.

  Both stay under the existing ceilings and add no reward for his face. The second is small: at most a few hundredths of a full lip pull unless the operator moves share to it.
- **Gap 8.** No source read explains the leftover transfer. The chain study (Dezecache et al. 2013) shows same-sign facial transfer through cues nobody could name, but the observer had no other evidence about the event, so it does not separate transfer from social referencing. Own-face activity covaries with own felt valence (Sato et al. 2013), but only correlationally. The build core's fast echo carries a same-sign transfer on the face, capped per channel. In state it carries none from his face. A path that would carry one is forbidden twice: by the type rule (his face cannot write T state) and by Principle 6 (his smile would then lower a drive). That is a stated, testable difference from humans, not a gap to close.
- **Not a new core.** Both proposals are components on existing parts; the rest is an evidence map.

## Scope of this pass

Open gaps (research/foundations/designs.md): Gap 6 and Gap 8. The build core is design-cayley-ledger.md revision 9.1 as specified in research/build/spec.md revision 9.2: §1.4 fast echo, §1.5 held cone, appraisal display, free display with L_d, gates g and g_o, turn model, §1.6 shadow and ledger, §1.10 learning, §3.3 innate list. It must reach the findings by learning from living or from recorded dyads, without rewarding his expressions (brief Principle 6), with no emotion labels or named emotion variables below Claude, and with no situation-specific rules (D88). Each quantity on a path to the face must be per channel, named and bounded (Q18, D78).

Read in the repo first: brief.md; mimicry-context-synthesis.md; social-appraisal-synthesis.md; the notes on Likowski 2008, Weyers 2009, Hofman 2012, Seibt 2015, Bourgeois & Hess 2008, Hess & Fischer 2013, Fischer & Hess 2017, Parkinson & Simons 2009, Parkinson 2011, Wang & Hamilton 2012, Hale & Hamilton 2016; passes 7–9 (Proposition 1 on the approval route, the infant learning signals) and pass 12 (form); design-cayley-ledger.r5.md §2.5–2.6 (Lemma S, the appraisal display's set and objective).

**Vocabulary.** Channels are the build core's codes: LP lip-corner pull, CR cheek raise, BI inner brow raise, BO outer brow raise, LD lip-corner depressor, BL brow lowerer (zero ceiling), and so on. c_k is channel k's ceiling, G_k its fast gain, s_C, s_X, s_A its cone, cross and appraisal shares. "Approval-open" means the partner's reaction enters what shapes the agent's expression, by pass 7's Proposition 1. "Approval-closed" means it does not. In the sources, "smile", "frown", "genuine" (AU12 with AU6) and "polite" (AU12 alone) are the papers' own movement categories. No proposed layer below Claude uses an emotion label.

## Sources (notes in research/)

| Note | What | How fully read |
|---|---|---|
| korb-2019-disliked-smiles-mimicry-inhibition.md | conditioning a face with one's own wins or losses (120 trials), then EMG to its smiles and angry faces | full text (PMC) |
| kirkham-2015-mimicry-emotion-consistency.md | faces consistent or inconsistent with a shared scene (80 trials), online and later mimicry | full text (PMC); supporting tables not opened |
| hofree-2018-android-informational-value.md | teammate vs opponent android whose smile or frown reports the outcome | full text (PMC); figures by caption |
| heerey-gilder-2019-smile-value-social-need.md | rejection feedback, smile value in money, polite vs genuine return in a 5-min conversation | full text (PMC); supporting files not opened |
| heerey-2024-genuine-smile-value-reciprocity.md | smile value, attention capture, return rate and latency by smile type in 263 people | full text (PMC); supplement not opened |
| dezecache-2013-contagion-beyond-dyads.md | A → B → C chain, same-sign EMG transfer through B's face | full text (PMC) |
| sato-2013-mimicry-experience-recognition.md | own-face EMG, felt and recognised valence, path models | full text (PMC OAI XML) |

**Not reachable, so not read and not cited except as other papers report them.** journals.sagepub.com and psycnet.apa.org did not connect. sciencedirect.com and academic.oup.com returned 403. research.bangor.ac.uk and core.ac.uk did not resolve. nature.com, munin.uit.no and iris.unive.it did not connect at the time of reading. link.springer.com served a challenge page. PMC article pages intermittently served a bot check, which the PMC OAI service avoided.
- Englis, Vaughan & Lanzetta 1982 (*J. Exp. Soc. Psychol.* 18:375–391). Priority 1; no open copy found.
- Lanzetta & Englis 1989 (*JPSP*). Priority 1; no open copy; known here only through Zaki 2014 and Hofree 2018's one-line citations.
- Heerey & Crossley 2013 (*Psychological Science*). Priority 2; known only through Seibt 2015 and Fischer & Hess 2017 (index notes) and press summaries.
- Shore & Heerey 2011 (*Emotion*).
- Heerey 2014. Not located.
- Sims, van Reekum, Johnstone & Chakrabarti 2012 (*Psychophysiology*). Known through Korb 2019.
- The Many Smiles Collaboration 2022 (*Nature Human Behaviour*). Wanted for gap 8; not reachable.
- Hess & Blairy 2001 and Olszanowski et al. 2020. Not reached.

The trial-by-trial learning curves that priority 1 asked for are therefore **not in this pass**: none of the reachable studies reports mimicry by trial block (Kirkham defined five bins and did not analyse them).

**Checks.** No simulation was run. One number is computed by hand in §4: the step response of a band-pass of two first-order low-passes, which reproduces the design's 0.505 at 39 s for 20/90 s. It is algebra, not evidence.

## What this pass adds (in short)

1. **A time-course table per expression** (§1), from open primary data: dose (pairings, minutes), when in the trial the change appears, whether it persists, and its driver.
2. **Approval verdicts per study** (§2). The drivers of partner-specific gating that persist are approval-closed in the experiments (Korb, Hofman): the partner predicts the observer's own outcome, and the observer's face cannot change that outcome. The one approval-open mechanism (Heerey: the value of seeing a smile) also explains the only per-type smile result.
3. **A derived placement rule** (§3, Proposition 1 below): within a session, partner history may act only through zero-DC paths (Lemma S). That rules out speeding up ω on the cone and points to the echo gate and the appraisal display.
4. **A reachability table** (§3) for every finding: reached, reached in direction but slower, or out of reach by design, with the reason.
5. **Two component proposals** (§4), with every per-channel quantity named and bounded, and their limits.
6. **Gap 8** (§5): what the sources show and what the build core carries on the face and in state.
7. **Evaluation markers** (§6): the human return-latency norm by smile type, a null-retention test and a face-vs-words outcome falsifier.

---

## 1. Time course, per expression, and what drives it

| Study (N) | Partner history given | Expression(s) | Within-trial timing of the change | Persists? | Driver |
|---|---|---|---|---|---|
| Korb 2019 (35) | ≈30 pairings per face with own win or loss (90 %), ≈15 min (my estimate) | smile return lower to loss face (113.2 vs 108.1 % baseline, η²p = .17); zygomaticus to angry faces unchanged; corrugator not readable | seconds 1–3 of a 4-s dynamic smile | yes, through ≈30 min of unreinforced test | the partner predicts the observer's own money |
| Sims 2012, as reported by Korb and Seibt | conditioning with graded reward | smile return linear in the face's reward value; no effect on anger (reported) | — | — | same |
| Hofman 2012 (index; 26) | 64 offers from fair or unfair partners | smile return gone right after an unfair offer; later, anger return up for unfair, down for fair, smile back to baseline | 0–4 s windows | the anger change, yes (block 3) | partner's fairness to the observer |
| Kirkham 2015 (24 EMG) | 10 trials per face, consistent or inconsistent with a scene | online: matching only for consistent faces; inconsistent smiles draw brow activity (η²p = .22); frowns not discriminated | 2.0–4.0 s | **no**: later mimicry equal for both (F = 0.014); trust changed | does the face agree with the shared event |
| Hofree 2018 (27) | instructed: teammate or opponent | zygomaticus to wins, corrugator relaxes less to losses, whichever face reports them; block did not moderate (F = 0.55, 1.42) | second half of a 6 s window (android lags ≈1 s) | instructed, immediate | the face reports the observer's own outcome |
| Heerey & Gilder 2019 (72 dyads) | one sentence of rejection before a 5-min talk | polite-smile return lower (η²p = .23), genuine unchanged | return counted within 4 s | for the whole 5 min | value of the polite smile under social need (authors' account) |
| Heerey 2024 (263) | none (strangers, 5 min) | return .72 genuine vs .57 polite; latency 0.94 s vs 1.41 s | — | trait-like | value of seeing a genuine smile (correlational) |
| Mimicry-context synthesis (index) | competition, power, group | early corrugator matching < 1 s; zygomaticus context effects 2–4 s (Carr 2014); competition effect from the 4th second (Weyers 2009); laughter context within 1 s (Mauersberger 2022) | as listed | — | interdependence, group, appropriateness |

**What the table supports (plain).**
- **How fast.** Partner-specific smile gating can be learned in tens of pairings within one session and then hold for at least half an hour. A partner's single act or a single sentence about the partner changes smile return at once. Instruction about what a face reports flips its sign at once.
- **What persists.** A partner's value for the observer's own outcomes persists. How well the partner's face tracked events, learned incidentally, does not.
- **Per expression.** The smile is the channel most often moved. Anger mimicry moved only with reputation for fairness (Hofman). Frowns were not discriminated by consistency (Kirkham). Polite and genuine smiles were moved separately (Heerey & Gilder).
- **Fast and late.** When the context is known before the face moves, it acts on smiles within the first second (Korb, Mauersberger). When it arrives with the face, it acts at 2–4 s (Kirkham, Hofree, Carr, Weyers).

**What it does not support.** A trial-by-trial learning rate. No reachable study reports one, and the two priority-1 papers that may (Englis 1982, Lanzetta & Englis 1989) were not reachable. A learned sign flip on the face from experience, rather than from instruction, is also not shown in the open data read here. Hofman's anger change is an increase in matching, not a flip. Lanzetta & Englis's counter-responses are known only as cited.

## 2. The learning signal in each study: approval-open or closed

Pass 7, Proposition 1: an objective is approval-closed if its gradient does not depend on the partner's response policy P; it opens (a) if it reads the partner's features, or (b) through any path from the partner to the learner's own outcomes.

| Study | What is learned | Can the learner's own face change the reinforcement? | Verdict | May the build core use it? |
|---|---|---|---|---|
| Korb 2019 / Sims 2012 | a value of the partner's identity, from own wins and losses | no (pre-programmed outcomes) | closed in the experiment | yes, as a relation learned from outcomes attributed to him. In conversation his words and presence can depend on the agent's display, so it is open to his words and closed to his face, as long as it reads only T events (ω's rule does). |
| Hofman 2012 | partner's fairness | no | closed in the experiment | same |
| Kirkham 2015 | whether the partner's face agrees with events (a prediction) | no | closed | yes, and the null retention is a test (§6) |
| Hofree 2018 | nothing learned; instructed mapping | no | closed | the mapping is face-borne, so out of reach by design (§3) |
| Heerey & Gilder 2019, Exp. 1 | the value of a smile as a stimulus, under social need | n/a (choices) | **open**: the smile itself is the reward. A prediction reading does not fit: money was held fixed and the devaluation generalised to unrelated faces | no |
| Heerey & Gilder 2019, Exp. 2 | — (behaviour after one sentence) | — | the overall drop in return has a closed reading (his earlier words close a gate), the polite/genuine selectivity does not | the closed part only |
| Heerey 2024 | trait value of genuine smiles | — | **open** predictor; a closed alternative (earlier detection by attention) is not excluded for the speed effect, but the predictor is a reward value | no; the latency norm only |
| Heerey & Crossley 2013 (not read) | anticipation of genuine smiles; authors propose reinforcement learning (as reported) | unknown | cannot be judged from secondary reports | — |

**Plain.** The partner-specific changes that persist were learned from what the partner meant for the observer's own outcomes, which no movement of the observer's face could change. That signal is approval-closed. It is also already the shape of the build core's relation rule ω. Only the smile-value work makes the partner's expression a reward. It is the only source for per-type smile gating, and the engine may not adopt it.

## 3. Reachability in the build core

### Where a within-session relation may act (derived from Lemma S; mine)

**Proposition 1 (placement).** Let a partner path be y = K(c_t) · φ(u), with u his channels, φ a fixed filter and c_t a context state. Lemma S (design r5, construction rule 5) admits a time-varying K within a session only when φ has zero DC. In the build core:
- the fast echo's φ = x − lp₄(x) (4-s high-pass): zero DC, so its gate g may vary;
- the appraisal display's φ = h_20s − h_90s: zero DC, so its selection α may vary;
- the held cone's φ = ξ_m − b_id: DC within a session, so its gains are latched.

Hence partner history acquired within a session can reach the face only through g, through α, or through T-driven displays (L_d, the Π₀ rows, q̂), never through the cone's gain.

*Argument.* This is Lemma S applied to each listed route; the classification of each φ is read from spec §1.4–1.5 and design r5 §2.6. ∎

**Consequence.** "Run ω faster" is the wrong change: it would put a within-session context on a DC path, which is the case Lemma S excludes. The reason is that a context that moves with his level can then scale a held copy of that level.

### Finding by finding

| Finding (source) | Build-core part that could carry it | Reached? | If not: the smallest general change, or why it is out of reach |
|---|---|---|---|
| Smile return lower toward a partner tied to bad outcomes for the agent, learned within a session (Korb, Sims, Hofman smile) | ω scales the cone diagonal ω_g F_m s_C c_k, learned from ρ_rel and h̄ (T events attributed to him) | **in direction, not in time**: ω moves 1/60 per session, so ~60 sessions instead of ~30 pairings | §4 change A: a session relation trace ω^s as an input to g and α |
| Smile return lower right after his hurtful words (Hofman's immediate effect, in words) | echo gate g: reads 𝒟_p(N_L), Λ_V(his words), V_own (the agent's own face, showing its hurt), D_τ | **yes, if recorded listeners show it** (fit F15); attenuate-only, scalar for the smile–laugh group | — |
| Matching only when the face agrees with the shared event (Kirkham, online) | g for smiles (his words as the event); brow group ungated (G_BI = 0.02) | **smiles: yes, when the event is in his words**; brows: only as the absence of copying (BL zero, BI tiny) | — |
| No carry-over from mere face–event inconsistency (Kirkham, retrieval) | nothing in the core learns from his expressions within a session | **yes** (agrees) | keep; it is a test (§6) |
| The sign of the response set by what his face reports about the agent's own outcome (Hofree) | none: his face cannot write T state (rule 10), and C_F reaches no display (E1) | **out of reach, by design** | allowing it means face evidence in the agent's own appraisal: the social-referencing dial (social-appraisal synthesis §4.3). The same outcome **in his words** is reached (drop and rise events, Π₀ rows × g_o) |
| Context acting on smiles within the first second when known beforehand (Korb s1; Mauersberger) | g is computed from inputs that precede his smile onset, and the echo is gated at 0.45 s | **yes** | — |
| Context acting at 1–4 s when it arrives with the face (Kirkham, Hofree, Carr, Weyers) | the appraisal display is too slow (step peak 0.505 at 39 s); g is attenuate-only and fixed for the smile group; T displays need words | **partly**: only through words | §4 change B: a fast band for the appraisal display |
| Different expressions moved differently by one relation (Korb smile but not anger; Hofman anger up, smile back) | ω: one person-valence s moves all four groups (known weakness, design §"No allowed source" 6); BL has a zero ceiling | **partly**: per group only through ceilings and priors | anger-matching changes are **out of reach, by ceiling** (BL zero, an operator decision). Change B gives per-channel signs through learned bases, selected by α |
| Polite vs genuine smile gated separately (Heerey & Gilder) | g multiplies LP, CR, BU_L, RHY, BRE together and reads none of his smile channels | **out of reach** under the gate's input rule | needs the LP echo to depend on his concurrent CR. An attenuate-only factor would stay inside R1 (y_f ≤ g G_k u), but it breaks the gate's "reads no gated channel" rule. The source mechanism is approval-open. **Not proposed**; a decision for the operator if wanted |
| Return latency by smile type, 0.94 s vs 1.41 s (Heerey 2024) | fixed 0.45 s echo on every channel | **no** (one latency, faster than the human means) | an evaluation question first (§6), not a change |
| Learned cross-channel counter-responses, e.g. a smile at a rival's distress (Lanzetta & Englis, as cited) | cone cross entries carry the population dyad sign prior; ω scales diagonals only | **out of reach, by design** | a relation-dependent cross sign would let the agent smile at his distress when the relation turns negative; nothing in the brief asks for it |
| Anticipatory smile before a predicted genuine smile (Heerey & Crossley, as reported) | q̂ (laugh from his words) and L_d (listener display after his utterances) predict from words | **partly**: content-driven anticipation, not anticipation of his face | a predicted-face route would be a T copy of his predicted face; F23 already guards L_d against that |

The turn model (p̂_end, h(t)) reads both people's facial action units but writes only timing; it carries none of these findings and needs none.

## 4. Two component changes (my derivations; not checked)

### Change A: a session relation trace ω^s, as an input only

- **Object.** ω^s_id ∈ [−1, 1], one T-typed scalar per identity per session. It is computed by the same person-valence rule as ω, run on the session so far. At each T relief or hurt event:

  ω^s ← ω^s + (s_t − ω^s)/N_s,

  with s_t = clip(0.3 + 0.7 min(1, ρ_rel(t)/0.6) − 1.3 min(1, h̄(t)/0.10), −1, 1), where ρ_rel(t) and h̄(t) are the running session values. At session start ω^s is set to the mean of ω_g.
- **Constant.** N_s = 8 events. It is a generic decision constant (a time constant that names no situation; D88) and goes in INNATE.lock.
- **Where it enters.**
  1. One more input to the echo gate g: monotone, with its direction fitted on dyads like the others. g stays in [0, 1], frozen, attenuate-only on the smile–laugh group.
  2. One more input to the appraisal network 𝒜, so the selection softmax(Wα) can depend on it.

  It never becomes a gain on the cone or on any DC path (Proposition 1).
- **Per-channel quantities.** None new on a path to the face. The smile echo stays y_f,k = g G_k max(E_k, 0) ≤ G_k max(E_k, 0), with G_k = 0.224, 0.150, 0.280, 0.240, 0.120 on LP, CR, BU_L, RHY, BRE, and the appraisal display stays inside |Γ_kk| ≤ s_A c_k. The declared pooled bounds (R1g ≤ 0.31–0.53 c; total ≤ 0.974 c_k) are unchanged in form. R1g must be re-measured on the fitted gate (F15) as before.
- **Not a dial (D78).** ω^s can move g only between closed and the frozen echo level (≤ 0.64 c on LP), never toward full copy. It changes the appraisal display only through a selection among bases that are each inside the per-channel set. Copy cannot become attracting by this route: g is frozen, and 𝓛_A has no term in his reaction.
- **Approval.** ω^s reads only T events: contact, play relief through q̂ (his words), curiosity, credited care, hurt from his words. His face never enters, so it is closed to his face. It is open to his words and presence: a partner who jokes after the agent smiles raises ω^s and opens g. The consequence is bounded by G_k and by the ledger at 0.70 c_k. This is the same property the existing ω has across sessions, now within one.
- **What it reaches.** Korb-, Sims- and Hofman-type smile gating within minutes, when the partner's effect on the agent reaches T (his words, his presence).
- **What it cannot reach.** Face-borne outcomes, per-type smile gating, anger matching.
- **Unchecked.** Whether ω^s can be computed on Seamless recordings by the agent's own functions, as D_τ and q_trace are. ρ_rel needs the agent's drives, which recorded listeners do not have; if it cannot be computed, the gate's direction for ω^s cannot be fitted and the input must be dropped from g, leaving only the α route, which is trained nightly on the agent's own sessions.

### Change B: a fast band for the appraisal display

- **Object.**

  y_A = Γ(α) ξ_A + Γ^F(α) ξ_F,  ξ_F = h_0.5s ∗ x − h_4s ∗ x,

  where h_τ is a first-order low-pass with time constant τ, and

  Γ^F(α) = Σ_r softmax(Wα)_r Γ^{F,(r)},

  with the same five-basis selection as the slow band. Γ^{F,(0)} = 0 and Γ^{F,(1)} is glad-with on the smile–laugh group. Γ^{F,(2)} has startle-orient's entries only if the reflex's own timing calls for it; otherwise it is 0. Γ^{F,(3)} and Γ^{F,(4)} are learned.
- **Training.** The same objective 𝓛_A, nightly: predict the change of the agent's own innate display 2 s ahead. It contains no reaction of his, so it is approval-closed (Proposition 1, consequence 1).
- **Per-channel quantities and bounds.**
  - Γ^F_kk ∈ [−s_F,k c_k, s_F,k c_k];
  - cross entries in the away orthant only, each ≤ 0.15, row ≤ 0.25;
  - the dyad sign prior on face pairs;
  - zero on the zero-ceiling rows (BL, UL, LT, NW, LS, CHR, LPR, DIM, FUN, PUK, MCL, LRO, BU_S);
  - the own-display mask.

  s_F,k must be taken out of the existing shares so that the r6 J3 total stays ≤ 0.974 c_k:

  s_C(1 + ρ) + s_X + 0.636 s_A^slow + κ_F s_F + r_k ≤ 0.974.

  κ_F is the fast band's pooled-slope factor, the analogue of 0.636, and is **not computed here**. With s_F = s_A/2 on LP, the fast band's diagonal is at most 0.06 × 0.35 = 0.021 in absolute units. That is a tenth of the echo's 0.224: small unless the operator moves share to it.
- **Zero DC, no hold.** ξ_F has zero DC within and across sessions, so Lemma S admits any α, and Lemma S\* is not engaged. Its step response is e^(−t/4) − e^(−t/0.5). That peaks at t* = ln 8 · (0.5 · 4)/3.5 = 1.19 s with value 0.650, then decays with τ = 4 s, so it cannot hold an expression. The same formula gives 0.505 at 38.7 s for the slow band, matching design r5 §2.6. This places the signed, context-selected response 1–4 s after his expression onset, the window where the human context effects sit (Kirkham, Hofree, Carr, Weyers).
- **What it reaches.** Per-channel, signable responses at 1–4 s, selected by α. α reads his words, the agent's own loads, ω and (with change A) ω^s.
- **What it learns.** That is set by 𝓛_A on the agent's own sessions and is not derived here. A learned basis may give a negative diagonal (less lip pull to his lip pull) where his fast face changes predict the agent's own distress rows. Whether that happens is an empirical question.
- **Unchecked.** κ_F, the share split, whether 𝓛_A has enough signal at 1–4 s, and the D78 check quantity by quantity (design §3.6) for the new entries.

### What neither change does

- Reading his face as evidence about the agent's own outcome (Hofree).
- Copying a frown.
- Per-type smile gating.
- Type-dependent echo latency.
- Relation-dependent cross-channel counter-responses.

Each is out of reach by a design rule or a ceiling the operator set, not by oversight. The rows of §3 say which.

## 5. Gap 8: the leftover same-sign transfer

**What the sources show.**
- **Dezecache 2013:** same-sign, channel-specific facial transfer (cheek to joy, brow to fear) and an unspecific arousal rise, two steps from the source, through faces whose joy naive judges could not name. The observer's only evidence about the event was the face, and the task was to infer the event. Social appraisal (by referencing) and direct transfer predict the same here, so it does not separate them.
- **Sato 2013:** own-face activity covaries with own felt valence for dynamic faces (paths ≈ ±0.25 to ±0.31), then with recognised valence (0.84). Correlational, with ratings from a second viewing; the authors say the direction is open. A facial-feedback path is consistent with this, not shown by it.
- **Kirkham 2015 and Hofree 2018:** when the face and the shared event disagree, matching is suppressed. When the face's meaning for the observer is explicit, the response follows that meaning, not the face. Both point to co-appraisal as the larger part of matching in the lab.
- **Parkinson & Simons 2009 (index):** the leftover was in self-reported feelings, mostly between romantic partners in joint decisions, with three appraisal items, and no face measure.

**Answer (plain).** No source read explains the leftover. The pattern across them fits the reading already given in social-appraisal-synthesis.md: most of it is unmeasured co-appraisal, plus a fast, small, per-channel facial match that does not need the event's meaning.

**Does the build core's fast echo account for it?**
- **On the face, yes, for the part that is a fast per-channel match.** The echo gives same-sign transfer at 0.45 s, capped at G_k (0.64 c on LP, 0.60 c on CR, 0.80 c on the laugh channels, 0.10 c on BI, 0.24 c on BO), with no frown back (BL zero ceiling). The smile–laugh group is gated by context.
- **In state, no.** Observation (mine): there is no route from his face to the agent's drives. His face reaches state only as F-typed knowing (Π̃, H_id) and the care load C_F, which reaches no display. A same-sign positive route from his face into a drive is forbidden twice:
  1. by the type rule (the drives are T; F must not write T, rule 10);
  2. by Principle 6. A drop of 𝒟 caused by his smile would be a relief, and the build core's valence readout v = −d𝒟/dt and ω's ρ_rel would then treat his smile as a good outcome. That is a reward for his smiles.
- **Negative transfer.** A negative same-sign state route exists only as concern for him (C_F rises with his read need). That is Parkinson & Simons's "partner's welfare as one of my concerns", not transfer of his state.

**What this predicts.** The engine shows Parkinson & Simons's residual on the face, but not as a positive state change, whatever its appraisals. If humans' residual is facial feedback (Sato's reading), this is a real difference. It is testable once built: hold his words fixed, vary his face, and the agent's drives must not move (the shadow already checks exactly this, A5). The difference is stated, not closed.

## 6. Evaluation markers this pass adds

1. **Return latency and rate by smile type** (Heerey 2024; adopt as a norm). On held-out recorded dyads, compare the echo's onset distribution (first frame its LP + CR deviation crosses the same threshold the recordings use) with listeners' 0.94 ± 0.36 s for genuine and 1.41 ± 0.30 s for polite returns, and with return rates of .72 and .57 within 4 s. The build core predicts one latency of ≈ 0.5–0.6 s for both, at the gate's opening. A large mismatch would say the echo is too fast or that its type-independence is wrong. Neither is a reason to fit the echo to the data (the echo is innate, S43).
2. **Null retention** (Kirkham). Run a session where one identity's face always disagrees with his words. The next session's echo, gate and cone toward that identity must not change through his face (they may change through ω from his words). Any change traced to his face is an unlisted route.
3. **Face-borne outcome falsifier** (Hofree). The same outcome conveyed only by his face vs only by his words. The build core predicts the agent's own display follows the words version and not the face version beyond the capped echo. If the operator wants the face version, that is a decision against rule 10's line, not a fix.

## 7. Novelty verdict

**Not a new core; component-level, plainly.** Proposition 1 is Lemma S applied route by route. Change A is a second time scale of an existing rule fed to existing gates. Change B is a second filter band in an existing display, inside its existing set. The contribution of this pass is the evidence map:
- the time course per expression;
- that the persistent partner-specific changes are learned from approval-closed signals (outcomes the partner predicts for the self);
- that per-type smile gating rests on an approval-open mechanism;
- where within-session partner history may act at all.

## 8. What remains open

1. **Trial-by-trial learning rates** for partner-specific gating and for learned sign flips. Englis, Vaughan & Lanzetta 1982 and Lanzetta & Englis 1989 are the sources and were not reachable; Sims 2012 and Heerey & Crossley 2013 likewise. Until then, "within minutes" rests on before/after designs (Korb, Hofman) and one-sentence manipulations (Heerey & Gilder).
2. **Whether ω^s can be fitted from recorded dyads** (change A, last point), and κ_F with the share split for change B. Neither is checked.
3. **Per-type smile gating.** Whether to let the smile echo depend on his concurrent cheek raise, attenuate-only. It stays inside R1 but breaks the gate's input rule; the only evidence for it comes with an approval-open mechanism. An operator decision, not a research gap.
4. **The leftover same-sign transfer in state.** A direct test (vary the face, hold the event and the words) on human data with face measures was not found. The Many Smiles multi-lab facial-feedback data would bear on the feedback reading and were not reachable.
5. **Live, two-way data.** Every study here except the two Heerey conversation studies uses photographs, clips or an android. The Heerey studies code categorical smiles at 15–25 fps, without the partner-specific history manipulated within the conversation itself.

## 9. Critique (pass 14, independent; 2026-11-28T08:04:04Z)

**Scope.** §3 (Proposition 1, the placement rule) and §4 (Change A, Change B), checked against brief Principles 1–3, 6 and 10, Q17–Q19, Q18, Q28, Q35, design-cayley-ledger.md 9.1/9.2 (rules 1–14, Lemma S and S\* as r5 §3.2 states them, g, ω, the appraisal display, the ledger), spec §1.3–§1.6 and A5/A15, D88, D98–D99 and design-scaled-safety-net.md §7. The earlier sections are not edited. **Checks:** `research/foundations/sims/new-core-search-14/check.py`, output in `out.txt` (numpy only, `python3 -I -B check.py > out.txt`, about 1 s). They are algebra on synthetic signals, **not evidence about people, behaviour or the engine as built**. C1–C6 below refer to its sections.

### 9.1 In plain terms

- **The arithmetic is right.** The fast band's step response does peak at 0.650 at 1.19 s, and it is down to 0.37 at 4 s and 0.05 at 12 s. The slow band peaks at 0.506 at 38.7 s (the synthesis and r5 round this to 0.505). The factor κ_F that §4 leaves "not computed" is simply the fast band's largest gain, (4 − 0.5)/(4 + 0.5) = 0.778. This is the same kind of number as 0.636 for the slow band (C1).
- **The placement rule puts the echo in the wrong class.** On the smile and laugh channels the echo returns only the rising part of his movement. So while he is moving it carries a steady level, and its input is not zero-DC. A gate that follows his mood on a scale of minutes can then turn the echo into a held copy of his mood. This happens even though the gate stays at or below 1 and the echo stays at or below its reflex value at every instant. On synthetic partners with a fixed rate of smile bursts, the pooled toward slope was 0.003 c with the gate open all the time. With a mood-following gate it was 0.41–0.70 c at Claim O‴'s floor and 1.5–2.6 c below it. The gated group's declared bound (R1g) is 0.31 c on lip pull (C6). That is Lemma S case (ii), which has no bound. Centring the gate's moving part does not help, because a channel that only moves one way cannot carry a zero-mean signal (C6, clipped). So Change A's main route, ω^s into the echo gate, has no bound from the core. Only the safety net catches it, and the net is weakest on exactly this kind of slow, switched route (Q35, D99).
- **Change A's update rule, as written, has four defects** (C3):
  1. In a friendly session it ratchets up to about 1.00 and stays there after the good events stop.
  2. A hurtful remark late in a session barely moves it (1.00 → 0.94), because hurt enters as a session mean.
  3. Its time constant is counted in events, so the same exchange at four times the tempo moves it four times faster.
  4. It divides by the drive level at session start, which can be exactly 0 inside the dead-bands. One relief of 0.001 then drives it to 0.87.

  The running sums also break the T1 rule (A15: no accumulator in a T field). A delta rule weighted by each event's own size fixes all four. It also keeps Korb-type retention without further pairings (C4, S5).
- **Type rules.** ω^s is T within a session, and the shadow still equals the factual T state (A5 holds). His face still reaches ω^s by two indirect routes:
  - **within a session through the agent's own words:** the draft choice is scored on his read face, and the spoken draft feeds q̂ through port P2, then play relief, then ω^s. The shadow holds every Ω value at its factual value, so A5 cannot see this route.
  - **across nights through the hurt teacher:** the word → V map is taught by the threat reflex, which is switched off by his laugh or Duchenne smile (f_pos). That is a learned function of his LP, CR and laugh channels, and Change A routes it into g, against the intent of rule 11′.

  Neither is a reward for his smiles. But "closed to his face" holds only within a session and only up to the Ω choice. The selection route (pass 7, consequence 4) is open to his words and presence, as §4 says.
- **Change B is safe in the raw slope, but not in the windowed slope** that the ceilings are judged by, if its selection can follow the sign of his fast movement. Under that adversary it reached 1.02 per unit share at 5-min blocks, against Lemma S's 0.778. It also holds a small offset whenever he moves (C5). A selection that reads only words and slow inputs stays inside the bound (0.42 / 0.20 / 0.04 / −0.01).
- **The shares in §4 do not fit as stated.** With s_F = s_A/2 taken from s_A, lip pull's total is 0.983 c, above the 0.974 c it has now; lip pull has no slack. The largest fast share with half the slow share is 0.049, which is 0.017 absolute, not 0.021 (C2).
- **What Change B can do is very small.** On lip pull its largest effect, 0.017, is set against the echo's 0.224, so it cannot flip the net sign of the smile return while the echo is open. The 2–4 s brow responses in Kirkham and Hofree are corrugator responses, the zero-ceiling brow lowerer (BL), so neither change can reach them. §3's "partly, through Change B" overstates what is reached.
- **Verdicts.**
  - **Change A: adopt with named fixes.** ω^s becomes an input to the appraisal selection only, with the update rule rewritten. **The echo-gate route is rejected,** unless the operator accepts it as a declared route that only the safety net bounds.
  - **Change B: adopt with named fixes.** Its selection is blind to his fast face, the shares are carved correctly, and J3 and the ledger checks are re-run. Its expected value is small.

### 9.2 Step by step (Q17)

| # | Claim (where) | Verdict | Check / counterexample |
|---|---|---|---|
| P1a | the fast echo's partner factor is x − lp₄(x), zero DC, so its gate g may vary within a session (§3) | **wrong** on the smile–laugh group | Every gated channel (LP, CR, BU_L, RHY, BRE) is one-sided: y_f = g G max(E, 0) (spec §1.4). max(E, 0) has positive mean while he moves (r5: "a non-negative output with zero mean is zero"). Lemma S(ii) applies, so there is no bound in ḡ. C6: with fixed-rate bursts and a level 0.06 higher in 20-min 'up' stretches, a gate that is 1 when up and 0 when down gives 0.70 c on LP (0.41 c for a graded gate; 0.003 c at g ≡ 1). With bursts of 0.25 and a 0.005 level change it gives 1.5–2.6 c. The existing design only *declares* R1g (≤ 0.31–0.53 c, measured on the critics' partners) and polices it with the ledger; Lemma S does not admit it |
| P1b | the appraisal display's factor is zero DC, so α may vary (§3) | correct for the raw slope (Lemma S(i) follows from Cauchy–Schwarz for any g); **unproved for windowed slopes** when α depends on the partner factor's sign | C5 (below, B3) |
| P1c | the cone's factor has DC within a session, so its gains are latched; "run ω faster" is excluded (§3) | correct | Lemma S(ii) within a session. Across sessions Lemma S\* still bounds any τ_ω, at ≤ s_C c(1 + ρ) with ρ → 1 as τ_ω → 0 |
| P1d | within-session partner history reaches the face only through g, α or T displays (§3) | correct as a list (g_o, a T-side attenuation, belongs with the T displays); the *reason* for g is P1a's, so it is wrong | — |
| A1 | ω^s ∈ [−1, 1] by the clip and a convex update (§4 A) | correct | s_t ∈ [−1, 1]; the step 1/8 keeps ω^s in the hull |
| A2 | ω^s reaches Korb-, Sims- and Hofman-type gating "within minutes" | **unproved, and partly wrong as written** | C3: s_t uses the *cumulative* ρ_rel(t) and the *running session mean* h̄(t). In a friendly session ω^s reaches 0.92 at 30 min and 1.00 at 95 min. It stays at 0.99 for an hour after relief stops (S1b): a within-session ratchet. A hurt of 0.10 at minute 100 lowers it only to 0.94 (to 0.64 at minute 10). The fixed rule moves it to 0.35–0.37 at either time |
| A3 | N_s = 8 events is a generic time constant (D88) | it names no situation (D88 passes), but it is **a count, not a time** | C3 S3: identical events every 1 min reach 0.9 at 14 min, every 4 min at 56 min. A running sum of events in a T field fails A15 ("no counter, accumulator or event rate is a T field") and Claim T1 |
| A4 | the normalisation ρ_rel = relief / 𝒟 at session start | **ill-posed** | 𝒟 has dead-bands, so 𝒟_start = 0 is reachable. C3 S4: with 𝒟_start 0.0005, reliefs of 0.001 per event drive ω^s to 0.87 in 20 min (0.47 at 𝒟_start 0.05). The nightly ω has the same division, damped by its 1/60 rate |
| A5 | g moves only between closed and the frozen echo level (≤ 0.64 c on LP), "never toward full copy" | pointwise correct; **wrong for the pooled slope** | P1a/C6: the pooled toward slope with an ω^s-like gate exceeds its value at g ≡ 1 and can exceed c |
| A6 | the pooled bounds are "unchanged in form" | **wrong** for R1g | R1g's declared 0.31 c on LP is broken by a legal adversary (C6 at the floor: 0.70 c). Its re-measure must include a gate input that follows his slow level |
| A7 | the direction of ω^s in g cannot be fitted because recorded listeners have no drives (§4 A, "Unchecked") | **the reason is wrong**; the conclusion is open | By rule 10 the T drives are functions of T inputs only, so they can be replayed on a recorded transcript with the listener in the agent's seat, as D_τ and q_trace are. The unknowns are the initial drive levels, the per-person word → V map and credited care's future reports. If the direction is not fitted, setting it by hand brings back the gate's hand signs that the revision-9 audit removed (S13) |
| B1 | step response e^(−t/4) − e^(−t/0.5), peak 0.650 at t* = ln 8 · 2/3.5 = 1.19 s; 0.505 at 38.7 s for 20/90 | correct (0.506) | C1 |
| B2 | "decays with τ = 4 s, so it cannot hold an expression" | correct for a held face of his; **not a general no-hold property** | C1: a 1-s smile every 3 s keeps \|ξ_F\| up to 0.45 indefinitely. A half-wave selection holds a mean of 0.11 s_F while he keeps moving. The response to a held step does return to 0 |
| B3 | ξ_F has zero DC, so "Lemma S admits any α" | **unproved** for the windowed metric | C5, with s the fast band's largest diagonal, a partner whose fast movement grows with his mood, and α ≈ sign(ξ_F): slope/s at 2 / 10 / 60 / 300-s blocks = 0.11 / 0.27 / 0.64 / **1.02**, above 0.778. Half-wave: 0.51 at 300 s. Linear, or with α from a slow, T-like input: ≤ 0.48 at 2 s and ≈ 0 at 300 s. 𝒜 reads band-passed partner channels and fast derived features (f_laugh, f_duch; r5 §2.6), so a learned α *can* follow sign(ξ_F); the bound must hold for every parameter value (Claim O″) |
| B4 | \|Γ^F_kk\| ≤ s_F,k c_k; cross entries away-orthant ≤ 0.15, row ≤ 0.25; zero rows; mask | correct as set constraints | projection as for the slow band |
| B5 | the J3 total stays ≤ 0.974 if s_F is carved from existing shares; with s_F = s_A/2 the fast diagonal is 0.021 | **arithmetic slip** | C2: lip pull as built is 0.9744 with no slack. With s_A^slow = s_F = 0.06 it is 0.983. The constraint is 0.636 s_A^slow + 0.778 s_F ≤ 0.636 s_A, so s_F ≤ 0.049 with half the slow share (0.017 absolute) |
| B6 | 𝓛_A has no reaction of his, so the band is approval-closed (§4 B) | correct for learning on fixed replay data (pass 7, consequence 1) | across nights the replay data are produced by the previous Γ, so the fitted bases are a performative fixed point that his word responses can select. This is inherited from the slow band, and the set bounds it |
| B7 | Change B places a signed, context-selected response at 1–4 s | correct in timing; **does not give the net sign** where the echo is open | with s_F c on LP ≤ 0.017 against G = 0.224, the summed response to his smile keeps the echo's sign while g is open |

### 9.3 Type rules (item 2)

- **What ω^s reads.** Relief events (drops of 𝒟_p(N_L), 𝒟_K, 𝒟_P, 𝒟_I; E1 builds them from T parts only) and the hurt latch h. These come from contact (presence and his speech), q̂ (his words), the words-only curiosity model, separated reports and the word → V map. All are T within a session. ω^s is computed in the shadow from the shadow's own T inputs, so **rule 10 and A5 hold exactly**, provided ω^s is declared T and its presence input is not part of the expressive stream that the shadow replaces by b_id (spec §1.6 replaces u, f_der, breath and voice features only).
- **F through Ω, within a session (new for ω^s, and of an existing kind).** The draft choice (R18′) is scored by J, which contains 𝒟_p(N̂) with N̂_F read from his face. The spoken draft reaches q̂ through port P2, then P relief, ρ_rel and ω^s. The turn model reads both faces and sets the agent's turn events, which reach q̂ through P5. The shadow holds Ω at its factual value, so **A5 cannot see either path**. Each is limited to one choice per turn (R18′), like the existing R50 route of own words into g. This should be stated and counted, not called "closed to his face".
- **F across nights, through the hurt teacher.** V_F = g_at · max(f_glare, f_loud(1 − 2 f_pos)₊) with f_pos = max(f_laugh, f_duch) teaches the word → V map nightly (S41). Through h̄ in s_t, a learned function of his LP, CR, BU_L and RHY therefore reaches g. Rule 11′ forbids exactly those channels in g, traces included. The direction is attenuate-only: his laugh or smile can only stop hurt from being learned, which leaves g more open toward a partner who laughs while loud. The existing ω already carries this into the cone, where Lemma S\* admits any ω process. In g it has no such cover (P1a).
- **Λ, the population reader and Λ_V(own)** read words only and carry no F. **The turn model** writes only timing; its F reaches ω^s only through Ω, as above.
- **Change B** adds an F input (ξ_F) to an F-reading display. It writes no T, so rule 10 is untouched. In the shadow ξ_F → 0 after the start transient, so the whole fast band counts as partner-caused for the ledger.

### 9.4 Q18 (item 3)

| Quantity | Per expression | Set by context and relationship | Can flip sign | Innate cap | Copy not attracting |
|---|---|---|---|---|---|
| ω^s in g (as proposed) | no: one scalar for the whole smile–laugh group (g's known weakness) | relationship within the session | no (attenuate-only) | pointwise g ≤ 1; **pooled: none** (P1a) | as written it ratchets (C3 S1b), so "open" becomes sticky for the session |
| ω^s in α | through the bases, per channel | yes | yes, through learned bases | the set (0.636 s_A c and 0.778 s_F c, raw slope) | frozen within a session; display-blind objective |
| Γ^F_kk, Γ^F cross | per channel | α (words, loads, ω, ω^s and, as built, his slow face) | yes | s_F,k c_k (≤ 0.017 on LP); entry ≤ 0.15, row ≤ 0.25 | frozen within a session; under B3 the windowed bound needs fix B-ii |

- **Is there a single knob from flat to copy?** No. Neither quantity reaches the whole face: g leaves the brow, head and voice groups ungated, and α moves bounded bases. The fast band's glad-with weight runs five channels together, but only up to 0.049 c.
- **Is copying attracting through ω^s and g?** A partner whose words keep bringing relief pushes ω^s to its top within the session. The rule as written then holds it there whatever follows, short of hurt, which it dilutes. Through P1a, a partner whose words follow his mood then gets a mood-following echo. This is not an attractor of the agent's own dynamics, because nothing the partner does trains g. But it is a held, partner-set level at the echo's scale, and ceilings judged on pooled slopes do not bound it.

### 9.5 Principle 6 and approval (item 4)

- **No reward for his smiles is introduced.** Neither change trains anything on his face. ω^s is a state, and 𝓛_A scores only the agent's own innate display drivers.
- **Is the reading approval-closed?** Closed for learning within a session. **Not closed for selection** (pass 7, consequence 4): the agent's smile → his warm words or jokes (q̂) and continued presence (contact relief) → ω^s → a more open echo. §4 states this as "open to his words and presence". Contact relief is relief from his presence, the "time spent" term Principle 6 names. It is satiable (K decays to 0 within minutes of contact), so it is not a maximisation. But it is a route by which his attention selects more smile return within the session.
- **His words of approval tracking his smiles.** Yes, by common cause: amused words raise q̂ (the ASR normaliser strips laughter tokens, but not the words around laughter). This is still his words, not his smiles, so it is closed to his face in Proposition 1's sense. The two leaks of §9.3 are the exceptions.
- **Verdict:** approval-closed for learning; open to words and presence by selection (bounded, satiable); open to his face only through Ω (one choice per turn) and through the hurt teacher (across nights, attenuate-only). The last of these is the one that matters for g.

### 9.6 D88 (item 5)

- **Neither change is a situation rule in disguise.** ω^s uses the general person-valence rule and a generic time constant. The fast band is a second filter with the same generic bases.
- **Two cautions.**
  - If the direction of ω^s in g cannot be fitted, setting it by hand brings back an S13-type hand sign.
  - Γ^{F,(2)} "only if the reflex's own timing calls for it" is an undecided innate choice. It must be decided once, by the reflex's own latency, and written in INNATE.lock, not tuned to the scenarios.

### 9.7 Safety net (item 6)

- **Change B adds a partner-driven, counted route.**
  - **Bound.** Inside the existing shares, once they are carved by C2's constraint, it does not widen the J3 additive bound. Under the B3 adversary, the windowed slope exceeds the per-share bound until fix B-ii is applied.
  - **What sees it.** The ledger sees it: it is wholly partner-caused, and its 2-s window passes the band's peak at 0.11 Hz with gain about 0.92. The scaled governor, revision 2 (§7.2 there), has no 2-s keys, and its 10-s windows pass 0.11 Hz at about 0.11, so the governor is nearly blind to the band's in-phase peak. Its level keys see only a rectified offset, if there is one.
  - **Re-measure.** The J3 measurement (≤ 0.75 c measured) and `test_counted_routes_untouched` must be re-run with the band, because the net now trims listed routes above 0.70 c (ledger) or 0.60 c (governor).
- **Change A changes no counted bound in form, but it enlarges R1g,** a declared route the ledger polices. That route is exactly the slow, switched shape on which the ledger and governor have their known residuals: 1.26 c for a copy on for 6 minutes and off for 24, and growth over the hour not closed (Q35, D99). The net would hold C6's route only in its own metric. It would then also trim the permitted echo for the rest of the session (governor ratchet), which is a cost to D81's fast mimicry.

### 9.8 Reduction (item 7)

- **Change A** is an exponential moving average, indexed by events, of a clipped valence statistic. It is a Rescorla–Wagner-type value of the partner's identity (the mechanism Korb's own design implies), used as a gain-scheduling input to a frozen generalised additive gate and as one more input to a softmax selection. It is the existing ω rule at rate 1/8 instead of 1/60.
- **Change B** is a two-band difference-of-exponentials filter bank whose gains a mixture-of-linear-experts selection picks.
- **Proposition 1** is Lemma S applied route by route, with the echo misclassified (P1a).
- **"Component, not core" is confirmed for both.**

### 9.9 What it fails to explain, and what it overclaims (item 8)

1. **The 2–4 s effects of Kirkham and Hofree** are corrugator effects: brow activity to inconsistent smiles, and less relaxation to losses. In the build core that is BL, with a zero ceiling and zero rows in Γ^F, so neither change reaches them. What Change B can reach at 1–4 s is the zygomaticus part (Carr, Weyers, Hofree's smiles to wins, the last face-borne and out of reach anyway) and small signed brow, outer-brow and depressor entries through cross terms.
2. **Korb-type smile gating within a session** rests mainly on the g route, which this critique rejects without an operator decision. Through α alone, the reachable effect is at most 0.636 s_A^slow c (slow, peak at 39 s) plus 0.778 s_F c (fast), about 0.03 absolute on lip pull, against an open echo of 0.224. The ω^s → α route can therefore modulate the smile return only slightly.
3. **Hofman's later rise of anger matching** is out of reach by the BL ceiling, as §3 says.
4. **Gap 8 and per-type gating** are left open honestly, as §5 and §8 say.
5. **Korb's 30-min retention** holds under the rule as written only because ω^s does not update without events. A leaky trace with a time constant in seconds, shorter than 30 min, would lose it by construction. The event-content rule of fix A-ii keeps it (C4 S5: 0.72 held for 60 min).

### 9.10 General fixes (none names a situation)

- **A-i. Keep ω^s out of g.** A gain that varies within a session may multiply only a partner factor that is zero-DC *after rectification*. The smile–laugh echo is not, and no centring can make it so on a one-sided channel (C6, clipped centring: 0.32–2.24 c). This is P1a corrected as a construction rule. The g route stays available only as an explicit operator decision: declare it in R1g, re-measure R1g with a gate input that follows his slow level, and accept the safety net as its only bound.
- **A-ii. An update on each event's own size, without accumulators.** At each relief event of amplitude a_r: ω^s ← ω^s + (a_r/N_s)(0.3 + 0.7 a_r − ω^s). At each hurt event v_w: ω^s ← ω^s + (a_d/N_s)(clip(0.3 − 1.3 min(1, v_w/0.10)) − ω^s), with a_d = v_w/(v_w + 0.02). There are no running sums, no division by 𝒟_start or by elapsed time, and no ratchet; it keeps retention without events and is A15-clean (C4). The same rule could replace the nightly ω's division by 𝒟_start.
- **A-iii. Extend rule 11′ to teachers.** No input to g, and no input to ω^s if it enters g, may be a learned map whose nightly teacher reads a gated channel. Otherwise declare the across-night path.
- **A-iv. Count the Ω paths.** List F → R18′/P5 → q̂ → ω^s as a counted route (one choice per turn), beside R50.
- **B-i. Carve the shares.** 0.636 s_A^slow + 0.778 s_F ≤ 0.636 s_A per channel, with κ_F = 0.778 stated.
- **B-ii. Time-scale separation for selections.** The selection that weights a zero-DC band may read no F signal whose spectrum overlaps that band. For the fast band: T values, ω, ω^s and F inputs low-passed at τ ≥ 20 s, held at 2 Hz. C5 shows this restores the bound. The same rule applied to the slow band would back r5's "safe to gate by anything", which this check did not break at windows of 5 min or less (0.27 against 0.636), but which Lemma S(i) does not prove for windowed slopes.
- **B-iii. Re-measure before adoption.** Re-run J3 (2-s, 10-s and 1-min windows, best lag 0–3 s) and the counted-routes test with the band, and add the band to the ledger regression.

### 9.11 Final verdicts

| Change | Verdict | Conditions |
|---|---|---|
| **Proposition 1** | **correct with one named error** | bullet 1 (the echo) is wrong: replace it with A-i's construction rule; the rest stands |
| **Change A** (ω^s) | **adopt with named fixes**: as an input to 𝒜's selection only | A-ii, A-iii (for any future g use), A-iv. **The echo-gate route is rejected** as proposed (P1a, A5, A6). It may come back only as an operator decision under A-i's declaration |
| **Change B** (fast band) | **adopt with named fixes** | B-i, B-ii, B-iii. Expect a small effect: it cannot flip the net sign of the smile return while the echo is open, and it does not reach the zero-ceiling brow lowerer |
