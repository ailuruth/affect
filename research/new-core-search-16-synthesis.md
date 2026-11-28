# Searching for a new core mechanism, sixteenth pass: what the nightly replay should prioritise, and what it must not learn from (synthesis, 2026-11-28)

## In plain terms

- **The question.** Each night the engine replays the stored day and learns from it. The spec weights each replayed moment by how much partner need it carried: a hard moment counts up to 4 times (κ_replay = 4, bias S48). Is that right? What else should decide what is replayed? Which nightly teachers read his face or voice, and can any of them turn into a slowly varying gain on his input, the pass-13/14 route to a held copy? Does training on the agent's own outputs risk drift or collapse? And what does this mean for the open M8 choice of when replay runs?
- **What the evidence says about weighting hard moments.**
  - Pooled over 36 datasets, people remember emotional, mostly negative, material better than neutral material, and they do so about equally after sleep and after waking. The sleep-specific advantage appears only in some designs, and only for negative material.
  - Pooled over 24 studies, sleep does not take the charge out of hard memories: physiological reactivity is unchanged and rated arousal to negative pictures goes slightly *up*.
  - What selective offline consolidation does track, in the studies read, is *expected future use*: an announced test or reward. And human rest replays the *weakly learned* items more. [[SCHAPIRO-PLAIN]]
  - The normative account (Mattar & Daw) says a memory is worth replaying in proportion to how much replaying it would still change what the agent does (gain), times how likely the situation is to come up again (need). Neither term is valence. A bad outcome is replayed strongly, but only while replaying it still changes behaviour. Replaying what no longer teaches anything is their model of rumination.
- **So κ_replay = 4 is a declared constraint with thin support.** It is not wrong to have it, but it is not what the biology shows, and it costs something:
  - With 10 % of moments at full weight, they make up 31 % of what is learned each night.
  - The weight never falls. A hard moment counts 4× every night for the 30 days it is stored, because the weight reads the stored need level, which replay does not change. Sleep does not depotentiate either, so nothing offsets this.
  - Nights full of relief also learn more slowly (learning rate × exp(−0.5 r̄)). Both learning biases lean the same way: toward learning from hard days.
- **One real defect, and a fix.** The spec writes the weight as 𝒟_p(N̂). N̂ includes the reading of *his face* (N̂_F), so as written the weight reads his face. Revision 7 designed it to read only the need his *words* decode to, "so a mirroring partner cannot raise it". The code stores an undefined "Dp" column. **Fix R1: the weight reads 𝒟_p(N_L), the words-only need (the existing Dp_word column).** That restores revision 7's rule. The weight then weights the fit of H_id and Π̃, which feed the echo gate, from words only.
- **A second small fix.** The weight should not bias the fits that *read levels* (the face readers H_id and Π̃, the adapter). Weighting hard moments shifts what those readers report toward distress. **Fix R2: those fits are unweighted** (or importance-corrected); the weight applies only to the expression and selection learners (𝒜's bases, Δ, the draft scorer).
- **An optional alternative (my derivation, unchecked): Change R.** Weight a moment by how much was at stake *in either direction* (relief or distress events from his words, the agent's play and curiosity), times how likely its context is to come back (same person, same topic in recent sessions), times how much is still left to learn from it (falling with each night it has been replayed). It reads nothing from his face or voice, names no situation, and every quantity is bounded. Over 30 nights a hard moment counts about 1.8× in total instead of 4×, and a good moment counts as much as a hard one.
- **Teachers.** Three nightly learners are taught by something read from his face or voice: the world model 𝓜, the word → V map (taught by the threat reflex) and the draft scorer (taught by J, which includes the face-borne need). The replay weight itself also reads his face. Each of those that reaches a gain on his input does so through a route that is already declared and bounded (ω into the cone, Lemma S\*; own words into the echo gate, one choice per turn), except the replay weight, which Fix R1 closes. One more mismatch: the echo gate was fitted offline on the *innate* reader Π̃₀ but runs on the *learned* readers. **Fix G: feed the frozen gate from the frozen reader it was fitted with**, or re-measure R1g under the learned readers.
- **Own outputs.** The engine does not dream up training data, so the collapse seen when models train on their own samples does not apply directly. But two learners are trained on the agent's own outputs: Π̃ reads the agent's own face, and Δ shapes that face so that Π̃ reads it. They can drift together into a private code, and since Π̃ is also how the agent reads *him*, his reading drifts with it. The pull toward the innate starting weights bounds this. **Add a data anchor** (fixed innate face–state pairs mixed into Π̃'s fit each night) **and a drift monitor** on a fixed probe set.
- **M8, the nightly schedule.** The evidence does not make the hour matter for software. One block per day, after the day's sessions and before the next, is what keeps the declared rates meaning what they say. Options are listed in §5.
- **Not a new core.** Component-level: two fixes, one construction rule, one optional weighting rule, one anchor and one monitor.

## Scope of this pass

The build core is design-cayley-ledger.md revision 9.1, specified in research/build/spec.md revision 9.2. Parts read:
- spec §1.3 (types T/F/Ω/K, ports, readers, drives), §1.5 (cone, appraisal, gates), §1.9 (store, retention, nightly replay steps 1–8), §1.10 (learning biases), §7.3 (`nightly_schedule`), §8 (open M8 choice);
- design §2.2 (rules 6, 10, 11′–14), §2.8, §2.14–2.15, §3.2 (Lemma S, S\*), §3.5 (Claim L), and r7 §2.4.1, §2.14, §3.5 (κ_replay as first designed), r5 §2.6–2.7 (𝒜, 𝓛_A, 𝓛_display, Π̃, the word-need reader), r4–r6 (the replay row: clip, pull, exp(−0.5 r̄));
- the M8 code: engine/learn/weights.py, engine/learn/nightly.py, engine/memory/store.py (read, not changed);
- new-core-search-13-synthesis.md §9 (the pass-14 critique; fixes A-i to A-iv, B-ii).

Not redone: memory-replay-synthesis.md and its twelve notes (McClelland 1995, Kumaran 2016, Hayes 2021, Schaul 2016, van de Ven 2020, Rolnick 2019, EWC/SI, Tse 2007, McGaugh 2004, Nader/Hardt, Walker/Payne/Kensinger). They are used as their notes state.

Constraints:
- brief Principles 1–3, 6 and 10;
- no emotion labels or named emotion variables below Claude;
- D88 (no situation-specific rules);
- Q18 (every quantity named and bounded, per channel, copying never attracting);
- fix A-iii (no gate input may be a learned map whose nightly teacher reads a gated channel, unless declared).

Words: "hard moment" means a 2-Hz moment with high partner-need load 𝒟_p; "his face" covers his face, voice and derived features (F-typed); "gated channels" are LP, CR, BU_L, RHY and BRE, the smile–laugh group the echo gate multiplies.

## Sources (notes in research/)

| Note | What | How fully read |
|---|---|---|
| lipinska-2019-sleep-emotional-memory-meta-analysis.md | 36 datasets: is emotional memory preferentially consolidated in sleep? | full text (Frontiers PDF); forest plots by caption |
| lipinska-2022-sleep-emotional-reactivity-meta-analysis.md | 24 studies: does sleep depotentiate reactivity? (read in place of Davidson & Pace-Schott 2021) | full text (Frontiers PDF); supplement not read |
| cunningham-chambers-payne-2014-expectation-emotional-memory.md | expected test × emotional trade-off across sleep and wake | full text (Frontiers PDF) |
| barner-2023-sleep-tmr-relevance.md | relevance and odour TMR during SWS; the TMR source of this pass | full text (Frontiers PDF); Exp. 2 results paragraph in part |
| shumailov-2023-curse-of-recursion-model-collapse.md | model collapse when trained on own samples | arXiv v3 main text in full; the *Nature* 2024 version not read |
| gerstgrasser-2024-accumulating-data-avoids-collapse.md | accumulate vs replace; bounded error with accumulation | arXiv v2 main text in full |
| mattar-daw-2018-prioritized-memory-access.md | priority = gain × need, derived; replay asymmetries; familiarity | bioRxiv v4 in full (Methods and derivation included); the *Nature Neuroscience* typeset text not read |
[[SOURCES-ROWS]]

**Used as their notes state:** memory-replay-synthesis.md, sleep-emotional-memory-walker-payne-kensinger.md, schaul-2016-prioritized-experience-replay.md, hayes-2021-replay-missing-biology.md, mcgaugh-2004-amygdala-modulates-consolidation.md, rolnick-2019-experience-replay-continual.md, van-de-ven-2020-brain-inspired-replay.md.

**Not reachable, so not read and not cited for any claim:**
[[UNREACHABLE]]

**Checks.** No simulation. The weight shares, the 30-night totals and the pull's stationary variance were computed by hand and checked in a few lines of Python (`python3 -I -c`). They are algebra, not evidence.

## What this pass adds (in short)

1. **An evidence verdict on κ_replay** (§1): thin support, and a stated cost.
2. **Fix R1** (§1.3): the replay weight reads words only, as revision 7 intended. This is a defect in the spec text, and the M8 code leaves it undefined.
3. **Fix R2** (§1.3): no replay weight on the level-reading fits.
4. **Change R** (§1.4, optional, my derivation): stakes × need × remaining gain, valence-free, T-only, every quantity bounded.
5. **A teacher table** (§2), with one new construction rule, **Fix G**.
6. **The own-output loops** (§3): what the spec already guards and what it lacks (a data anchor and a drift monitor).
7. **M8 options** (§5), each one line.

---

## 1. What should set replay priority

### 1.1 What the evidence shows

| Claim | Evidence read this pass | Verdict |
|---|---|---|
| Sleep keeps emotional (negative) material better than wake does | No overall effect: negative vs neutral d = 0.52 after sleep, 0.58 after wake (k = 20 each). Sleep-specific only with baseline-controlled retention (0.64 vs 0.18, k = 9) and free recall. Positive: none (Lipinska 2019) | **weak, design-dependent, negative only** |
| Sleep removes the emotional charge (sleep to forget) | Physiology unchanged (SMD 0.02); valence ratings unchanged; rated arousal to negative material *higher* after sleep (2 × 2 SMD 0.65) (Lipinska 2022) | **not supported** |
| What sleep selects is expected future use | Announced test plus reward: relevant > irrelevant overall; sleep × relevance short of significance (p = .096 at 1 week) (Barner 2023). An announced test produces in wake the selectivity sleep produces without it (Cunningham 2014) | **supported, modest** |
| Selection is capacity-limited; unprioritised items can be rescued by cueing | Oudiette 2013 as reported by Barner; Barner's own TMR null with a descriptive trend for the irrelevant set | **watch** |
| Priority should be gain × need, not salience or surprise | Derived exactly (EVB = Need × Gain); reproduces forward/reverse balance, reward asymmetries, aversive-zone replay when it changes behaviour, decline with familiarity; only gain is reduced by replay (Mattar & Daw 2018) | **adopt as the normative frame** |
[[EVIDENCE-ROWS]]

Taken with what the repo already holds:
- McGaugh's modulator is *valence-free* arousal, and it acts after the event, awake as well as asleep (mcgaugh note). Lipinska 2019 fits that: arousal at encoding helps both sleep and wake memory.
- Hayes 2021 reports Isele & Cosgun: priority by TD error or reward alone did not prevent forgetting, while coverage matching did as well as an unlimited buffer.
- Schaul's |δ| priority warns of unlearnable transitions hogging replay.

### 1.2 What κ_replay = 4 does, and what it costs (my derivations)

The spec's weight is w = 1 + 3 min(1, 𝒟_p(N̂)/0.05). 𝒟_p = 0.05 is reached at a read V of 0.30 (0.8 (V − 0.05)² = 0.05), so any clearly troubled moment gets the full 4.

- **Share.** If a fraction p of a night's moments are at full weight, their share of the weighted loss is 4p/(1 + 3p): p = 0.02 → 7.5 %, 0.05 → 17 %, 0.10 → 31 %, 0.20 → 50 %.
- **No decay.** The weight is a function of the stored moment's need level, which replay does not change. A hard moment is weighted 4× on every one of the ≤ 30 nights it is stored, a total of 120 against 30 for an ordinary moment. Nothing in the engine plays the role of a tag that falls once the moment has been learned. Lipinska 2022 removes the biological hope that sleep would do it.
- **Same-direction learning-rate bias.** The night's learning rate is × exp(−0.5 r̄), with r̄ the night's mean relief amplitude. A night of many reliefs (r̄ = 0.5) learns at 0.78 of the rate of a night of none. Distress weighting and relief-slowed learning both tilt the slow learners toward hard days.
- **Where the tilt lands.**
  - In a correctly specified, well-identified regression, weights that depend only on the inputs do not bias the conditional mean.
  - But the readers are ridge-regularised and low-capacity (H_id is 15 → 3 with ridge 2), and the weight correlates with their *target*. Their fitted level then moves toward the heavily weighted region: a weighted-mean shift of Cov(w, y)/E[w].
  - The readers' output is the agent's sense of how he is, read from his face. So a person with some hard days is read as somewhat more troubled on ordinary days. That is a negativity bias in *knowing* him, the part the design keeps open on purpose. It does not reach the face beyond the ceilings, but it does reach care, initiative and draft choice.
- **Slower forgetting of his hard moments.** Within the 30-day window, hard moments dominate what the slow learners carry. After the window, the pull to θ₀ forgets everything at the same rate; but what the weights hold when the data are deleted is already tilted.

**In Mattar & Daw's terms** κ_replay is a stakes-salience heuristic with neither a gain factor (it never falls as the moment is learned) nor a need factor (it ignores whether the context recurs). Their model predicts what such a weight does: it keeps replaying hard moments after they have taught what they can, which is their candidate model of rumination.

**Verdict on κ_replay = 4 (plain):** keep a priority, but not this one as written. The biology supports selecting what matters for the future and what is not yet learned, of either sign. It does not support a fixed 4× on hard moments for as long as they are stored. The spec's version also reads his face (§1.3). If the operator keeps κ_replay, apply Fix R1 and Fix R2. If he wants the engine not to lean toward hard days, use Change R.

### 1.3 Fix R1 and Fix R2 (needed)

- **Fix R1 (a defect in the spec text).**
  - Revision 7 (r7 §2.14, §3.5) defined the weight from "the distress his words decoded to in that segment (from T: the replay weight cannot be raised by his face)". The spec (§1.10) writes 𝒟_p(N̂). N̂ is the care read, which takes the coordinate-wise max of N̂_F (Π̃ and H_id on his face) and N_L (his words). engine/learn/weights.py reads a store column `Dp` whose writer is not built, and calls it "the agent's own D_p(N-hat)".
  - **Fix:** w = 1 + 3 min(1, 𝒟_p(N_L)/0.05), reading the existing `Dp_word` column (T). This changes one input of one innate bias; it names no situation (D88).
  - **Why it matters beyond Principle 6.** The weight multiplies the fits of H_id and Π̃, whose outputs feed the echo gate g through V⁻_his and D_τ (spec §1.5.4). With N̂_F in the weight, an input of g would be a learned map whose nightly *sample weight* reads his face, including the gated channels unless N̂_F is masked. That is fix A-iii's case with "weight" in place of "teacher".
  - There is also a self-reference: N̂_F contains H_id's own output, so H_id's fit is weighted by its own readings.
- **Fix R2.**
  - Apply the replay weight only to steps whose output is an expression or a selection: 𝒜's W and Γ^{(3,4)}, Δ, the draft scorer and the retrieval query. Fit the readers (Π̃, H_id, the adapter, the word → V map) and 𝓜 unweighted, or with importance weights 1/w normalised per night.
  - This is the existing synthesis's own rule (memory-replay-synthesis.md §2: "importance weights at β = 1 apply wherever a gradient is read as affect"), applied to the readers.

### 1.4 Change R: stakes × need × remaining gain (optional; my derivation, unchecked)

Only if the operator wants a general replacement for κ_replay. Every quantity is T-typed or replay bookkeeping. None reads his face or voice, his presence, his gaze or session length, and none names a situation.

  w_k = 1 + 3 · s_k · u_k · γ_k,  so 1 ≤ w_k ≤ 4.

| Quantity | Definition | Type | Bound | Generic constant |
|---|---|---|---|---|
| s_k, stakes | max of the opponent-masked relief amplitude a_r and the distress amplitude a_d (spec §1.3 events: drops and rises of 𝒟_p(N_L), P and I; **K and the h part of 𝒟_V excluded**) over events within ±20 s of moment k | T (E1 events) | [0, 1] | window 20 s (the read window) |
| u_k, need | 0.25 + 0.75 × (fraction of this person's last 7 sessions in which moment k's topic slot was addressed) | T (identity × topic slot address) | [0.25, 1] | 7 sessions; floor 0.25 |
| γ_k, remaining gain | 1/(1 + c_k/3), c_k the number of earlier nights on which moment k was replayed | replay bookkeeping in the store, not a state field (A15 untouched) | (0, 1] | 3 nights |

What each term is for:
- **Stakes is valence-free.** Three reasons:
  - McGaugh's modulator is valence-free arousal.
  - Mattar & Daw's gain has a sign only through behaviour change.
  - The human data show negative material kept better after sleep and after wake alike (Lipinska 2019), which gives no reason to treat hard moments as a separate class.

  Weighting good moments equally is a choice, not a finding (§8). Two exclusions:
  - K (contact relief, which is his presence) is excluded so that no weight follows his attention or time (Principle 6).
  - The h part of 𝒟_V is excluded because the word → V map that writes h is taught by the threat reflex, which reads his gated channels (A-iii).

  P (play relief) comes from q̂, which reads his *words*, not his laughter (rule 14).
- **Need is expected future use:** Mattar & Daw's need (expected future occupancy, learned only from real experience), and the quantity that Barner and Cunningham manipulate. In the engine's own terms it is how often this person and topic come back. It is computed from the slot address (T), not from anything he shows.
- **Remaining gain falls with replay.** Mattar & Daw: "only gain is affected by replay"; replaying what no longer changes behaviour has zero utility. γ plays the part of a tag that drops once the moment is learned, the part §1.2 found missing. It is a count, not a prediction error, so it cannot be held high by an unpredictable channel (Schaul's unlearnable transitions) and cannot read F.
- **The floor of 1** is the coverage term. Every stored moment is replayed at least at base weight, as Isele & Cosgun's result in the Hayes note requires.

Totals over 30 nights, for a moment at full stakes and need (computed):
- the spec's κ_replay: 120 (4 every night);
- Change R: 53.0. Nightly weights 4.0, 3.25, 2.5 (night 4), 1.9 (night 8), 1.53 (night 15), 1.28 (night 30);
- uniform weighting: 30.

So a hard or a good moment counts about 1.8 times an ordinary one over its life, against 4 times now.

**What Change R does not do.** It does not make the engine forget hard moments: they are still weighted up, as much as good moments of the same stakes. It does not touch calibration's slowness toward aversive readings (S38) or the separation rule (S40). Its ablation, written before building: with Change R in place of κ_replay, the readers' mean read V on low-need moments of a person with some hard days should be lower, by an amount set by the share formula of §1.2; and the agent's reading of his later separated reports (F8″) should be no worse.

## 2. The nightly teachers, and whether any feeds a gate or gain on his input

The pass-13/14 lesson: a gain on a partner input that varies slowly with something he does becomes a held copy, unless the input is zero-DC (Lemma S(i)) or the gain is latched per session and bounded across sessions (Lemma S\*). Fix A-iii extends rule 11′ to teachers. Below, "reads F" means that the target, the training input or the sample weight is computed from his face or voice.

| Step (spec §1.9) | Fitted | Teacher / target | Reads F? | Output reaches | Gain or gate on his input? | Verdict |
|---|---|---|---|---|---|---|
| 1 | 𝓜, all heads | his and the agent's channels, by likelihood | **target F** (his face channels, AUs, voice) | draft-scoring rollouts (Ω), initiative ΔĴ, retrieval query; if z_T is 𝓜's state (as engine/learn/nightly.py describes 𝒜's input), also 𝒜's selection α | only through α, which selects the appraisal gain Γ on ξ_A, a zero-DC band-pass | **declare.** Lemma S(i) admits any α for the raw slope; the windowed bound is open (pass-14 B-ii). Prefer that 𝒜 read only T-trained heads of 𝓜. Not built yet |
| 2 | Π̃ | the agent's own loads (T) | **training input** contains the partner-caused part of its own face (echo of his gated channels, cone, appraisal) | N̂_F → care, J, drafts; **V⁻_his and D_τ → g** | yes: g multiplies the echo on the gated group | **passes A-iii as written** (target T; g's input is masked). Second-order leak through the training inputs. Optional: fit on the shadow face ȳ (the partner-caused part removed) |
| 3a | calibration b_read, σ_id, b_id | none (statistics of his face) | F, latched (rule 6) | scale of x̃ → readers → g; centre of the cone | σ_id is a per-session gain on his face entering the readers; b_id centres the cone | **declared (rule 6, Lemma S\*);** no change |
| 3b | H_id | frozen population reader on his words (T) | input F; **sample weight F** through 𝒟_p(N̂) | N̂_F → **g** (V⁻_his, D_τ), care, J | yes, as an input of g | **teacher passes; weight fails → Fix R1.** Also Fix G |
| 3c | adapter | separated, partner-initiated reports (T) | no | N_L → 𝒟_p(N_L) → g, g_o, events | input of g and g_o (words) | **pass** |
| 3d | word → V | threat reflex V_F = g_at max(f_glare, f_loud(1 − 2 f_pos)₊), f_pos from his laugh and Duchenne smile | **teacher F, including gated channels** | h → 𝒟_V, rise events, phrase targets, J, **ω** | through ω into the cone gain | **declared across-night route** (pass 14 §9.3). Bounded by Lemma S\* in the cone. Must stay out of g and g_o (A-iii): today neither reads h. Keep it so |
| 4 | 𝒜 likelihood; W, Γ^{(3,4)} by 𝓛_A | own loads and his next decoded word need (T); own display drivers 2 s ahead (T) | input F (ξ_A, band-passed) | y_A = Γ(α) ξ_A | yes: Γ is a gain on his zero-DC band | **pass** (Lemma S(i), raw slope ≤ 0.636 s_A c). Windowed slope open (B-ii). Data are performative (yesterday's Γ), set-bounded |
| 5 | Δ | Π̃(own face) → own state (𝓛_display) | no partner channel | the free display (T inputs) | no | **pass** on type rules; drift loop with Π̃ (§3) |
| 6 | 𝓛_w | his words by likelihood | no | curiosity I, surprisal for q̂ | no | **pass** |
| 7 | draft scorer, retrieval query | J under the separation rule; J contains 𝒟_p(N̂) | **objective reads F** through N̂_F (as a level; his face is imputed in rollouts, so it is never what is credited) | draft choice (Ω) → own words → **Λ_V(own) in g and g_o** (port P1), q̂ (P2) | yes, through Ω, one choice per turn | **declared Ω route** (R50; pass-14 A-iv). Not a reward for his face (S40). Keep counted |
| 8 | ω | person-valence rule on T events and h̄ | **through h̄**, i.e. through step 3d's teacher | cone gain ω_g on his deviation from b_id (DC within a session) | yes, latched per session | **declared and bounded** (Lemma S\*: ≤ s_C c_k (1 + ρ) for any ω process). Keep out of g (A-i, A-iii) |
| — | the S48 sample weight | 𝒟_p(N̂) | **F** through N̂_F | weights steps 3–7 | weights the fits of g's inputs | **Fix R1** |
| — | learning rate × exp(−0.5 r̄) | own relief amplitudes (T) | no | all steps | no | **pass** (but see §1.2 on its direction) |

**Fix G, a construction rule (my derivation).** The echo gate g is fitted once, offline, on recorded strangers, with V⁻_his read through the *innate* reader Π̃₀ (r7 §2.4.1 table). At runtime the spec reads V⁻_his and D_τ through his calibration and the *learned* readers (r7 §2.4.1: "read through his calibration and H_id"; spec §1.3: N̂_F = max(Π̃, H_id)). So the gate's input map changes every night, and R1g's declared bound (≤ 0.31 c on LP, measured with the gate as fitted) is not measured under it.
- The rule: **a frozen gate reads its inputs through the same frozen maps it was fitted with.** For g: V⁻_his and D_τ through Π̃₀ and the per-session calibration only.
- What is lost: the gate stops benefiting from knowing him closely. That benefit was never measured, and the readers' learned knowledge still reaches care, initiative and drafts.
- If the operator prefers the learned readers in g, R1g must be re-measured across the range the learned readers can take. That range is set by the pull to Π̃₀ and H_id's ridge.
- The rule names no situation. It applies equally to g_o, which today reads V_own through Π̃₀ already.

**Answer to "does any teacher reading F feed a gate or gain on a partner input?"** Yes, four paths:
1. word → V → ω → cone;
2. J → scorer → own words → g;
3. (if z_T is 𝓜's) 𝓜 → α → Γ;
4. the S48 weight → H_id and Π̃ → g.

The first three are already declared, each with a bound: Lemma S\*; one choice per turn; Lemma S(i) for the raw slope. The fourth is undeclared and is closed by Fix R1. Fix G closes a related, undeclared change in g's input map.

## 3. Replaying the agent's own outputs: drift or collapse?

**What the ML sources say.**
- Collapse comes from training each generation on the previous generation's *samples*, which loses the tails first and makes the parameters a random walk with variance growing like n/M (Shumailov arXiv v3).
- Keeping the original real data in the mix bounds the error for every number of generations: σ²d/(T − d − 1) · π²/6 against σ²d/(T − d − 1) · n when replacing (Gerstgrasser).

**What the engine does.**
- It replays recorded moments, not samples from a learned generator. His channels and words in the store are real. The agent's own outputs in the store are real renders of what it did, and its own-face observations are real measurements of the rendered face. So the Shumailov mechanism, finite resampling of one's own model, is absent.
- Three loops are self-referential all the same:
  1. **Π̃ ↔ Δ (co-adaptation).** Step 2 fits Π̃ to (own face → own state). Step 5 fits Δ so that Π̃(own face) matches own state. Each is fitted to the other's output, and neither sees anything from outside the agent. They can drift together into a code that is legible to Π̃ but no longer close to Π₀'s human-like newborn rows. Since Π̃ is the same map applied to *his* face (Principle 3), reading him drifts with it. F8″ ("co-training drift") already names this as a falsifier, but nothing guards against it except the parameter pulls.
  2. **Performative data.** 𝒜's bases, the scorer and 𝓜 are trained on days shaped by yesterday's weights and by his responses to them. This is not collapse, but the training distribution moves with the model. The convex sets (𝒜), the separation rule (scorer) and display-blind objectives keep his responses from becoming a reward.
  3. **Replace beyond 30 days.** Feature arrays are deleted after 30 days (Q34 item 6). For anything older, only weights remain. That is Gerstgrasser's "replace" regime, with the pull to θ₀ in place of real data.

**What guards exist (spec §1.10) and what they do (my derivation).**
- With the pull λ = 0.1 and a step η, one SGD step is θ ← θ − η(clip(g) + λ(θ − θ₀)), which is a contraction toward θ₀ at rate (1 − ηλ) per step. Night-to-night noise in g therefore gives the parameters a *stationary* spread: variance ≈ η σ_g² / (2λ) for small ηλ. That is bounded, unlike a random walk whose variance grows with the number of nights. **So the pull prevents collapse-type drift of the slow weights.**
- The price is that anything learned decays toward θ₀ unless the 30-day window keeps re-supporting it. This is graceful forgetting toward the innate prior, not toward a degenerate point.
- Gradient clip 1 bounds each step. The projections (A6–A8) bound 𝒜, Δ and the cone to their sets.

**What is missing.**
- **A data-level anchor for Π̃.** Mix a fixed set of innate pairs into Π̃'s nightly fit, for example the face Π₀ (innate, never learned) produces for each of a fixed grid of states. That is Gerstgrasser's "keep the real data" in this engine's terms. The innate body is the only data source in that loop that cannot drift. Generic constants: grid size, and the mix fraction, say a quarter of Π̃'s weighted loss. No situation is named.
- **A drift monitor.** Each night, log Π̃'s reading of a fixed probe set of faces (Π₀'s rows, and a stored sample of his calibrated faces from the first week) and the size of Δ. Report when either moves beyond a declared tolerance. This makes F8″ a nightly number.
- **Optional:** fit Π̃ on the shadow face ȳ instead of the factual face, so that the partner-caused part of the agent's own face (the echo of his smile) does not enter the agent's self-reading.

## 4. Principle 6 check

- Under Fix R1 and Change R, no weight, learning-rate factor or target reads his face, his voice, his gaze, his presence or how long he stays. K is excluded from Change R's stakes for that reason.
- The remaining contact with his face in learning is as an *input* (H_id, 𝒜, calibration), as the *target of likelihood* (𝓜), and as the *teacher of one reflex-taught map* (word → V, attenuate-only; pass 14). Each is declared.
- Change R's need term rises when he keeps returning to a topic. That is his words choosing what the agent learns about, not a reward for his attention: it is bounded at 1, it is not an objective, and it does not move with his face.

## 5. M8: the nightly schedule

**What the evidence supports.**
- Selective benefits appear after one early SWS period (about 40 min, Barner) and after a full night (Lipinska 2019 found night ≥ nap in one sensitivity analysis).
- Nap and night differ in the *direction* of rated reactivity, but that subgroup effect is confounded with the waking control (Lipinska 2022).
- The 0–5 h window after learning is from mice (Graves 2003, via the existing sleep note).

None of this transfers to software as a constraint: the engine has no sleep stages, and nothing decays during the hours before replay. What does matter mechanically (my derivation):
- replay must run between one day's sessions and the next, so the next day uses consolidated weights;
- it must see the whole retention window;
- it must keep to the declared rates. The ω step (1/60 per session), the pull per step and exp(−0.5 r̄) per night assume one replay per day. Several full blocks a day would multiply the pulls and the passes over the data, so learning per day would no longer mean what the spec says.

Options, one line each (plain language):
- **A (spec default):** one block a night in the idle hours (2–6 h, after 30 min without a session). It needs the Mac left on overnight.
- **B:** one block soon after the day's last session (after 30 min idle, any hour). It learns the same thing, earlier, and also suits a Mac that is shut at night.
- **C (not recommended):** a short block after every session. The evidence does not support it, and it changes the meaning of the learning rates.

The evidence does not favour A over B. Choose by when the Mac is idle.

## 6. Evaluation markers this pass adds

1. **Weight source test (Fix R1).** Hold his words and turn order fixed and swap his face streams with another recorded person's (partner-swap surrogate). Every replay sample weight must be bit-identical. Under the spec as written it is not.
2. **Reader tilt (Fix R2, Change R).** Compare the mean read V on his low-need moments, after 30 nights, under κ_replay, under Fix R2 and under Change R. Predicted order: κ_replay > Change R ≥ Fix R2. Also check that F8″ agreement with separated reports does not worsen.
3. **Gate input map (Fix G).** Run R1g's measurement with V⁻_his read through the learned readers across their reachable range. If it exceeds the declared 0.31 c on LP, Fix G is required.
4. **Π̃ drift.** Track the nightly probe-set reading drift and the size of Δ. With the anchor, both should plateau within the window; without it, F8″ should show growing disagreement.

## 7. Novelty verdict

**Component level, not a core.** Nothing here derives a new mechanism.
- Fix R1 restores revision 7's own rule. Fix R2 is Schaul's importance correction applied to the readers.
- Change R is prioritised replay with a valence-free salience term, a recurrence (need) term and a replay-count decay. Each piece is standard (Schaul; McGaugh; the existing synthesis's T1). The combination keeps every term T-typed.
- Fix G is a construction rule: a frozen gate reads the frozen maps it was fitted with.
- The Π̃ anchor is Gerstgrasser's accumulate regime in parameter-and-data form.

What the pass contributes:
- the finding that the spec's replay weight reads his face, contrary to revision 7;
- the teacher table with each path's bound;
- the reader-tilt consequence of distress weighting;
- a stated answer on own-output replay: no collapse, a co-adaptation drift that has no data anchor, and graceful forgetting beyond 30 days.

No designs.md line.

## 8. What remains open

- **A computable gain for the engine.** Mattar & Daw's gain needs each backup's effect on the policy before it is made. The engine has no world model yet (step 1 not built). Change R uses a replay count as a stand-in; a policy-effect gain for the scorer, computed from T-only targets, is open.
- **Human replay of weak items in the engine's terms.** Change R's remaining-gain term is a count, not a prediction error. A prediction-error gain would be closer to the biology [[OPEN-SCHAPIRO]], but it would have to be computed from T-only targets to stay clear of A-iii. Whether such a version can be built before 𝓜 exists is open.
- **The windowed slope of the appraisal display under a learned selection** (pass-14 B-ii) is still unproved. Steps 1 and 4 feed it.
- **Whether z_T in 𝒜's input is 𝓜's state** (engine/learn/nightly.py) or the latched T values (r5 §2.6). The answer decides whether step 1's teacher reaches a gain on his input.
- **The Nature version of Shumailov et al.**, Davidson & Pace-Schott 2021, Baran et al. 2012, Oudiette & Paller 2013 and Feld & Born were not read.
- **Positive moments.** Every human study here used negative material, or found effects only for it. Whether good moments should be consolidated preferentially has no direct evidence in what was read. Change R weights them equally by construction, which is a choice, not a finding.
- **The relationship beyond 30 days.** With feature deletion and the θ₀ pull, what the engine knows of him after a month is the weights' slow memory plus slots and snippets. Whether that is enough for S6 is untested.
