# Searching for a new core mechanism, sixteenth pass: what the nightly replay should prioritise, and what it must not learn from (synthesis, 2026-11-28)

## In plain terms

- **The question.** Each night the engine replays the stored day and learns from it. The spec weights each replayed moment by how much partner need it carried: a hard moment counts up to 4 times (κ_replay = 4, bias S48). Is that right? What else should decide what is replayed? Which nightly teachers read his face or voice, and can any of them turn into a slowly varying gain on his input, the pass-13/14 route to a held copy? Does training on the agent's own outputs risk drift or collapse? And what does this mean for the open M8 choice of when replay runs?
- **What the evidence says about weighting hard moments.**
  - Pooled over 36 datasets, people remember emotional, mostly negative, material better than neutral material, and they do so about equally after sleep and after waking. The sleep-specific advantage appears only in some designs, and only for negative material.
  - Pooled over 24 studies, sleep does not take the charge out of hard memories: physiological reactivity is unchanged and rated arousal to negative pictures goes slightly *up*.
  - What selective offline consolidation does track, in the studies read, is *expected future use*: an announced test or reward. The repo's Hayes note also reports that human rest replays *weakly learned* items more (Schapiro 2018, which this pass could not reach, so it is not relied on here).
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

**Used as their notes state:** memory-replay-synthesis.md, sleep-emotional-memory-walker-payne-kensinger.md, schaul-2016-prioritized-experience-replay.md, hayes-2021-replay-missing-biology.md, mcgaugh-2004-amygdala-modulates-consolidation.md, rolnick-2019-experience-replay-continual.md, van-de-ven-2020-brain-inspired-replay.md.

**Not reachable, so not read and not cited for any claim:**
- **Schapiro, McDevitt, Rogers, Mednick & Norman 2018** (*Nat Commun* 9:3920, human rest replay prioritises weakly learned items). nature.com is outside this session's network, PMC served a bot check, and the bioRxiv preprint (10.1101/173021) returned HTTP 429 on every one of about ten retries over roughly 12 minutes. Its finding is mentioned only as the Hayes 2021 note reports it.
- **Liu, Dolan, Kurth-Nelson & Behrens 2019** (*Cell*, human replay sequences). cell.com and PMC were not reachable.
- **Baran et al. 2012** (*J Neurosci*). jneurosci.org and PMC were not reachable. **Cunningham, Crowell, Alger et al. 2014** (*Neurobiol Learn Mem*) was not reachable either; the Frontiers Cunningham 2014 paper was read instead.
- **Davidson & Pace-Schott 2021** (*Curr Sleep Med Rep*) and **Davidson, Jönsson, Carlsson & Pace-Schott 2021** (*Nat Sci Sleep*). Springer, dovepress and PMC were not reachable; Lipinska et al. 2022 was read in their place.
- **Oudiette & Paller 2013** (*TiCS*), **Oudiette et al. 2013** (*J Neurosci*), **Feld & Born 2017** and **Joensen et al. 2022** (*Learn Mem*). These were paywalled or on blocked hosts; Barner et al. 2023 was read in their place.
- **The published versions of Shumailov et al. 2024** (*Nature*) **and Mattar & Daw 2018** (*Nat Neurosci*). nature.com was not reachable, so the arXiv and bioRxiv preprints were read instead.

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
- **Human replay of weak items in the engine's terms.** Change R's remaining-gain term is a count, not a prediction error. A prediction-error gain would be closer to the biology (Schapiro et al. 2018, as reported by Hayes 2021: weakly learned items replayed more; primary not read), but it would have to be computed from T-only targets to stay clear of A-iii. Whether such a version can be built before 𝓜 exists is open.
- **The windowed slope of the appraisal display under a learned selection** (pass-14 B-ii) is still unproved. Steps 1 and 4 feed it.
- **Whether z_T in 𝒜's input is 𝓜's state** (engine/learn/nightly.py) or the latched T values (r5 §2.6). The answer decides whether step 1's teacher reaches a gain on his input.
- **Not read** (see Sources): Schapiro 2018, Liu 2019, Baran 2012, Davidson & Pace-Schott 2021, Oudiette & Paller 2013, Feld & Born, and the published versions of Shumailov and of Mattar & Daw.
- **Positive moments.** Every human study here used negative material, or found effects only for it. Whether good moments should be consolidated preferentially has no direct evidence in what was read. Change R weights them equally by construction, which is a choice, not a finding.
- **The relationship beyond 30 days.** With feature deletion and the θ₀ pull, what the engine knows of him after a month is the weights' slow memory plus slots and snippets. Whether that is enough for S6 is untested.

## 9. Critique (pass 17, independent; 2026-11-28T11:41:43Z)

**Scope.** §1.2–§1.4 (the κ_replay costs, Fix R1, Fix R2, Change R), §2 (the teacher table, Fix G), §3 (own-output loops, the anchor and monitor), §4 and §7. They are checked against brief Principles 1–3 and 6, Q18, Q28 and Q35, design-cayley-ledger.md 9.1/9.2 (type rules, Lemma S and S\*, g, g_o, ω, R1g, F8″), spec §1.3, §1.5.4, §1.9–§1.10, §3.2 and the A-asserts table, new-core-search-13-synthesis.md §9 (A-i to A-iv, B-i to B-iii), and D88, D99 and D100. Every claim about the code was checked by reading engine/learn/nightly.py, engine/learn/weights.py, engine/memory/replay.py, engine/routes/gates.py, engine/shadow/shadow.py, engine/state/body.py, engine/state/readers.py, engine/state/types.py, engine/routes/learned_t.py and engine/boundary/derived.py. The earlier sections are not edited.

**Checks.** `research/foundations/sims/new-core-search-17/check.py`, with its output in `out.txt` (numpy only; `python3 -I -B check.py > out.txt`, about 0.6 s). They are algebra on synthetic signals. **They are not evidence about people, about behaviour, or about the engine as built.** C1–C5 below refer to its sections.

### 9.1 In plain terms

- **The biggest error is a premise the code does not share.** Pass 16 assumes that every stored moment is replayed every night for the 30 days it is kept, so a hard moment counts 4× on 30 nights (120 against 30). The built replay does not do this. engine/memory/replay.py loads only the sessions *not yet replayed* and marks them replayed afterwards. Each moment is learned from on one night only.
  - So, as built, κ_replay costs 4 against 1, once.
  - Change R's "remaining gain" term γ is always 1, because no moment is ever replayed a second time.
  - §3's "replace regime beyond 30 days" in fact applies from the first night.
  - Whether replay *should* cover the whole window is an open design choice that the spec does not state either way. It has to be decided before Change R means anything.
- **Fix G is not optional. It names a defect that exists in the code today, and the defect is wider than §2 says.**
  - The echo gate g reads his read level (V⁻_his and D_τ) through `L.reader_his`, and both g and g_o read the agent's own face level V_own through `L.reader_own`. Both readers are rewritten every night by step 2.
  - The spec says V_own is read "through Π̃₀", the frozen innate reader, and the gates were fitted through Π̃₀. So the gates' input maps change nightly, and R1g's measured bound no longer applies to the gate that actually runs.
  - §2 says g_o "today reads V_own through Π̃₀ already". The code contradicts this.
  - §2 says H_id feeds g. The code contradicts this too: no runtime code reads H_id.
- **A second latent defect, of the same pattern as R1, sits under Π̃ and Δ.**
  - The target of both steps is a stored stream, `own_loads`, which has no writer and no type tag.
  - By r5 §2.7 its V coordinate is "distress + hurt". The agent's body V is V_F + h_word, and V_F is the threat reflex on *his* face, which reads his Duchenne smile and laugh (LP, CR, BU_L, RHY) and his gaze.
  - The code's `TARGET_SOURCES` calls this stream "the agent's own loads, from its own face", and that description is wrong.
  - If the writer stores body V, then Π̃ (an input of g and g_o) is a learned map whose nightly target reads the gated channels. That is fix A-iii's case. It also means Δ, which the design calls "T only", is trained toward a target that reads his face.
- **Fix R2 is sound, with one simplification.** In this engine's full-batch replay, "importance-corrected" is exactly the same as "unweighted" (C3), so it is one fix, not two. The reader bias it removes is real: a weight that is a function of the reader's own target moves the reader's level up (C3: +0.022 in read V on ordinary moments in a toy).
- **Change R is not ready.**
  - Its γ term does nothing in the built replay.
  - Its need term u reads how long his sessions are: with the same topic mix, 10-utterance sessions give u ≈ 0.61 and 50-utterance sessions give u ≈ 0.97 (C4). That is his time, entering as a learning weight.
  - Its stakes term needs event amplitudes the store does not keep (per term, re-masked without K and h).
  - It makes relief-heavy nights carry more weight, because play and curiosity drops happen at many of his turns, while care rises are rarer.
- **The anchor helps less than §3 suggests.**
  - Fixed Π₀ face–state pairs pin Π̃ only on the directions Π₀'s rows span. Off that span they are exactly equivalent to a stronger pull, λ/(1 − α) (C5), and off the span is where a private Π̃/Δ code would live.
  - The proposed probe set includes "his calibrated faces from the first week". Keeping those breaks the 30-day retention rule (Q34 item 6).
  - Any automatic action taken on probes of his face would make his face a learning-rate factor (Principle 6).
- **No proposal adds a whole-face knob (Q18), breaks A5, names a situation (D88) or is a new core.**

### 9.2 Derivations (Q17 standard)

| Item | Verdict | Why |
|---|---|---|
| 31 % weighted-loss share (10 % at full weight) | **correct** as arithmetic for two-level weights (C1: 0.3077) | With continuous weights, the moments between 1 and 4 lower the full-weight share: C3 has 9.4 % of moments at full weight carrying 21 %. The formula is the two-level case, not a general bound. |
| 120 vs 30 vs 53 over 30 nights | **arithmetic correct** (C1: 53.026 = 30 + 9(H₃₂ − H₂)); **premise contradicted by the code** | (a) As built, each moment is replayed once (replay.py: `not s.manifest.get("replayed")`, then `set_replayed()`). The totals are 4, 1 and 1 + 3su. (b) Even under whole-window replay, a sum of weights is not a sum of influence. Each night's 200 steps at lr 0.05 with the 0.1 pull shrink earlier nights' effect by ρ = 0.367 per night. The pull-discounted ratios are 4.00 (κ) and 1.29 (Change R), not 4 and 1.77 (C1). |
| θ₀-pull stationary spread ≈ ησ²/2λ | **correct for i.i.d. per-step noise** (C2: 0.2513 against 0.2500); **wrong model for the code** | `_descend` takes 200 full-batch steps on the *same* night's data, so the noise is fixed within a night. The stationary variance is then (σ/λ)²(1 − r)/(1 + r) with r = (1 − ηλ)²⁰⁰ = 0.367: 46.3 against a simulated 45.8, about 185× the stated value. The conclusion "bounded, not a random walk" stands. The constant does not. The only hard bound is deterministic: ‖θ − θ₀‖ ≤ clip/λ = 10 per parameter group, which is vacuous at the weights' scale. |
| γ removes the ratchet | **wrong as stated** (no-op as built); **unproved** under whole-window replay | Counterexamples: (1) as built, c_k = 0 always, so γ = 1. (2) Under window replay, c_k equals the moment's age in nights, because every stored moment is replayed every night. γ is then a fixed age discount, not remaining gain. A moment fully learned on night 1 still gets 3.25 on night 2, and a moment that cannot be learned decays at exactly the same rate. It removes the *per-moment* "never falls", but not Mattar & Daw's rumination case, which needs a gain that tracks learning. |

### 9.3 The teacher table (§2) against the code

| Row | §2 claim | Code | Verdict |
|---|---|---|---|
| 1 𝓜 | not built; 𝒜 may read 𝓜's z_T | not built; the z_T part of 𝒜's input is `np.zeros(64)` nightly (`appraisal_batches`) and at runtime (`Run.slow_tick`) | **confirmed** |
| 2 Π̃ | target own loads (T); output → g via V⁻_his, D_τ | the target `own_loads` has **no writer and no type**. By r5 §2.7 its V is distress + hurt, so it contains V_F (F: LP, CR, BU_L, RHY, gaze_at). Output → g via `reader_his` (confirmed), **and → g and g_o via `reader_own` (V_own), which the table misses** | **target "T" unproved, likely wrong; one path missed** |
| 3a calibration | σ_id, b_read scale x̃ → readers → g | computed nightly (τ chosen by the *learned* `reader_his` on his raw face, S38, declared), but **never applied at runtime**: `ShadowPair` stores b_read and σ_id and nothing reads them. The gate reads raw `u_read` | **not built as claimed**; the gate is fitted "at the speaker's scale", so this belongs with Fix G |
| 3b H_id | sample weight F → Fix R1; output → g | weight is `Dp_word` (R1 built, correct). **No runtime code reads H_id**: not g, not care. Also, H_id is a closed-form ridge refitted from scratch each night on that night's sessions only (no θ₀ pull; replay-once), so it is memoryless across nights | **"→ g" contradicted by the code**; memorylessness is a gap |
| 3c adapter | pass; → N_L → g | pass on the teacher. The body's N_L uses `L.pop` only, so the adapter reaches nothing at runtime yet | **confirmed (teacher); downstream not built** |
| 3d word → V | teacher V_F incl. gated channels; out of g and g_o | confirmed (`derived.py`: f_pos = max(f_laugh, f_duch); V_F = g_at · …). **Missed:** the teacher also reads his gaze-at (attention), and h_word feeds body V, so **word → V → h → own_loads V → Π̃ → g, g_o** is a second-order path into the gates | **one path missed** |
| 4 𝒜 | input F only through band-passed ξ_A | **missed:** the selection input b7 carries body "V" = V_F + h_word, nightly and at runtime (`b7 = … self.V_F + b.h_word …`). That is an unfiltered 2-Hz F signal in α, which is pass-14 B-ii's case | **one F input missed** |
| 5 Δ | no partner channel | Δ's target is `own_loads` (as in row 2). If V includes V_F, Δ is trained toward his face, against design 9.1 line "Δ (T only, own legibility)" | **unproved; depends on the own_loads writer** |
| 6, 7 | not built | not built | confirmed |
| 8 ω | through h̄ | `step_omega` reads h_word and drop events (T); h is taught by V_F | confirmed |
| S48 weight | Fix R1 | `sample_weight(Dp_word)`; every step uses `s.weights()`; the tests swap the face-including column | **R1 confirmed.** Residual: the untyped `Dp` body column is still in `BODY_COLUMNS` with no writer. Remove it, or tag it F |

**Face-reading paths into g, g_o or a gain on his input that §2 missed:**
1. Π̃'s learned `reader_own` → V_own → g and g_o. This exists in the code today.
2. word → V (teacher V_F) → h_word → own-load V → Π̃'s target → g and g_o. It is live once `own_loads` is written with body V.
3. V_F directly in 𝒜's selection input → Γ on ξ_A. Lemma S(i) covers the raw slope; the windowed slope is open (B-ii).

Fix G closes 1 and 2 for the gates. Path 3 needs B-ii, or V_F removed from α's input.

### 9.4 Fix R2

- **Is the distinction sound?** Yes.
  - The readers (Π̃, H_id, adapter, word → V) estimate a *level*, a conditional mean. The display and selection parts (𝒜's bases, Δ, scorer, query) choose an expression or an action, and there a declared emphasis is a learning bias, not a measurement error.
  - The bias is endogenous. In H_id the weight 𝒟_p(N_L) is a monotone function of N_L, which is the maximum over the same population-reader outputs that form H_id's target. The weight is therefore close to a function of y, which is outcome-dependent sampling. C3 shows the result: +0.022 in mean read V on ordinary moments, and a 9 % slope inflation.
- **Does importance correction keep the readers unbiased?** It does nothing that unweighting does not do. Replay is full-batch weighting, not priority sampling, so w · (1/w) = 1 (C3: identical coefficients). Schaul's correction applies only if sampling is prioritised. Write R2 as "unweighted", and keep the importance-weight wording only for a future sampled replay.
- **New path?** None. R2 only removes the weight from fits that feed g. Two notes:
  - the list must name both Π̃ parts (`reader_own` and `reader_his`);
  - 𝓜 unweighted is consistent with its likelihood role.
- **Verdict on R2:** sound, as one rule ("unweighted"), with the reader list completed.

### 9.5 Change R

- **Does s, u or γ read F?**
  - s: no F. Its inputs are 𝒟_p(N_L) (the population reader on his words, T), P (q̂ on his words, with the agent's last turn through port P2, Ω → T, declared) and I (progress on partner-initiated words, T).
    - Through P2 the agent's own words move s, and s weights the scorer that chooses those words. That is a performative loop (one choice per turn); count it beside R50 and A-iv.
    - s cannot be computed from the stored events. body.py combines the four drop terms into one opponent-masked a_r, and the mask uses S including the h rises. Excluding K and h requires per-term amplitudes, re-masked.
  - u is T only if three things hold:
    - the topic of moment k is the slot of *his* last utterance under the frozen encoder (`Encoder.topic`);
    - it is never the K-typed concept layer or 𝓜;
    - it is never a slot addressed by the agent's own words (Ω).
  
    As written, "moment k's topic slot" fixes none of these.
  - γ is bookkeeping, as stated.
  - Λ, the turn model and a learned population reader are not read. The population reader is frozen.
- **Does u reward his time?**
  - Not as an objective. But it *reads* his time as a weight: "fraction of his last 7 sessions in which the topic was addressed" rises with session length at a fixed topic mix (C4: 0.46 at 5 utterances, 0.61 at 10, 0.97 at 50).
  - That is the Principle 6 rule as `weights.py` states it ("nothing reads … his time … as a weight").
  - Fix: make u depend on the topic *share* of his last N utterances (for example the last 200), so it reads the mix and not the duration or the frequency of his visits.
- **D88.** Not situation-specific. The constants (7, 0.25, 3, 20 s) are generic, and the exclusions (K, h) are by type, not by scene.
- **Equal weight for equal stakes.**
  - True per moment, by construction. Not true per night:
    - P drops at every one of his turns (∝ q̂) and I drops at partner-initiated content, so relief events are far more frequent than 𝒟_p(N_L) rises;
    - h rises (hurt) are excluded from s, but play is not.
  
    So nightly mass shifts toward play and curiosity moments, and a hurtful exchange gains no stakes from h.
  - The exclusion of h is justified by the "no weight reads his face" rule, not by A-iii. Under R2 the weight no longer reaches any gate input.
  - The symmetry itself has no evidence for positive material (§8). It is a choice and should be labelled as one.
- **Verdict on Change R:** adopt with named fixes, and only after the replay regime is decided:
  - (R-a) decide whole-window or once. If once, drop γ. If whole-window, rename γ as an age discount and justify it as that.
  - (R-b) make u length-invariant (topic share of his last N utterances), defined from his words through the frozen encoder only.
  - (R-c) store per-term event amplitudes so that s can be computed, re-masked without K and h.
  - (R-d) count the P2 → q̂ → P → s → scorer loop as an Ω route.
  - (R-e) state the nightly relief/distress mass, not only per-moment equality.

### 9.6 Fix G

- **Is the premise true?** Yes, and more broadly than stated.
  - The fit: spec §3.2 fits g with "§1.5.4 inputs computed on the recording by the agent's own functions", which at M3 means Π̃₀ on strangers at the speaker's scale.
  - The runtime: `Run.slow_tick` calls `gi.slow(self.L.reader_his, self.L.reader_own, u_read, …)`, and both objects are in `nightly.param_items` and trained by `step_pi_tilde`. `u_read` is raw (no b_read or σ_id).
  - §2's statement that g_o "reads V_own through Π̃₀ already" is false in the code, although it is what the spec says.
  - H_id is not in g.
- **Freeze, or re-measure R1g each night?** Freeze.
  - R1g is a measured bound on strangers with the gate as fitted. Re-measuring it nightly would need the M3 dyad set and that measurement in every replay.
  - The learned readers' reachable range has no useful bound to measure across: the pull gives only ‖θ − θ₀‖ ≤ 10 (C2).
  - Q35 says the ledger cannot be relied on to police the smallest limits for routes whose bound is not shown, and R1g is the one route the design declares outside the sum.
  - The general rule is: **a frozen fitted map reads its inputs through maps frozen with it, at the same calibration.** Re-measurement is the fallback only if the operator wants g to know him.
- **Conflict with A-iii?** None. Fix G implies A-iii for g and g_o, because no gate input is then a learned map at all.
  - It does conflict with spec §1.3's sentence "Their outputs enter care, initiative, the gates' masked inputs …" and with r7 §2.4.1's "read through his calibration and H_id". Those sentences must be changed when Fix G is adopted.
- **Verdict on Fix G:** adopt, extended. It covers V_own (g and g_o), V⁻_his and D_τ, and it applies the latched calibration that the fit assumed.

### 9.7 The co-drift anchor

- **Is the loop real?** Yes.
  - Step 2 fits `reader_own` and `reader_his` on (observed own face → `own_loads`). That face was rendered with yesterday's Δ.
  - Step 5 then fits Δ so that `reader_own`(base + Δ(z)) ≈ `own_loads`.
  - This is block coordinate descent on one joint objective plus pulls. It converges to a bounded fixed point. It is not a random walk, and C2's corrected spread applies.
  - The fixed point can still sit far from Π̃₀. In the C5 toy, noise on the own face alone moves Π̃ on Π₀'s span by ‖WΠ₀ − I‖ ≈ 1.08 under the 0.1 pull.
  - The loop is not closed on the agent if `own_loads` carries V_F (§9.3 row 2).
- **Does mixing in Π₀ pairs bound it, and with what constant?**
  - On span(Π₀) it pulls Π̃ toward the innate inverse with weight α (C5: 1.08 → 0.97 at α = 0.25, → 0.76 at 0.5).
  - Off the span it is *exactly* a pull of λ/(1 − α) toward θ₀, and nothing more (C5: identical coefficients at α 0.25 and 0.5).
  - So it does not specifically bound a private off-span code, which is the drift F8″ worries about.
- **Is a probe-set monitor enough? What should it trigger?** A monitor detects drift; it does not bound it.
  - Probe on Π₀'s rows and on synthetic faces only. His first-week faces cannot be kept past 30 days (Q34 item 6) without a separate operator answer.
  - On a breach the trigger should be: report F8″; restore Π̃ and Δ to `learned_last_valid.npz`; hold them until the operator answers.
  - It must not adapt pulls or learning rates from probes of his face, because that would be his face as a learning-rate factor.
  - With Fix G, Π̃ drift no longer reaches any gain, so the anchor becomes a guard on knowing, not a safety guard.
- **Verdict on the anchor:** adopt with named fixes:
  - (N-a) state the constant (α on the span, λ/(1 − α) off it);
  - (N-b) probe set innate or synthetic only;
  - (N-c) trigger is report, roll back and hold, with no adaptive learning-rate change;
  - (N-d) build it only after `own_loads` is typed.

### 9.8 Q18, type rules, shadow

- **Q18.** None of the four adds a gain on an expression.
  - Change R and R2 are per-moment sample weights on learners.
  - The anchor's α is one scalar on one reader's loss.
  - Fix G removes nightly change from an existing group gate (g, already declared as R1g).
- **A5.** Not broken by any of the four.
  - They are nightly and change no in-session T field.
  - Under Fix G, g and D_τ stay held in the shadow, and g_o is not T.
  - The replay count c_k lives in store bookkeeping, not in state.
- **Type rules.** Fix G repairs a deviation from spec §1.5.4. Change R's u needs (R-b) to keep "T only" true.

### 9.9 Novelty and gaps

All four proposals are components, not a core, as §7 says.

What they fail to address:
1. the replay regime itself (once or whole-window), which §1.2 and Change R silently assume;
2. the type of `own_loads` (§9.3 row 2), which decides whether Π̃ and Δ are taught by his face;
3. V_F in 𝒜's selection (B-ii);
4. H_id's memoryless nightly refit;
5. the calibration that is never applied at runtime;
6. the gaze-at term in word → V's teacher, which is his attention inside a learned map's target (declared as a teacher, but not named as attention in §2 or §4).

### 9.10 Defects in the built code (as R1 was)

1. **G-defect (exists today).** The gates read learned readers.
   - *Minimal general change:* `Learned` keeps frozen `reader_his0` and `reader_own0` (the M3 Π̃₀, outside `nightly.param_items`, never written by replay). `Run.slow_tick` passes those to `GateInputs.slow`, on the calibrated face (b_read and σ_id latched per session).
   - *Test:* write synthetic sessions, record g and g_o on a fixed frame sequence, run one replay night, then rerun. g and g_o must be bit-identical. A static test checks that no object passed to `GateInputs.slow` is reachable from `param_items(L)`.
2. **own_loads defect (latent; same pattern as R1).** The target stream of steps 2 and 5 has no writer and no type tag, and its declared description is wrong.
   - *Minimal change:* give `own_loads` a typed writer. Either make V the T part only (min(1, h_word), with A_L and the energy load), or declare the V_F part as an F target and keep Fix G mandatory. Correct `TARGET_SOURCES["pi_tilde"]`.
   - *Test:* partner-swap surrogate. Keep his words and turn order, swap his u and f_der streams with another recording, and require the `own_loads` stream and the step-2 and step-5 fits to be bit-identical (if the T-only option is chosen).
3. **Minor.** Delete or F-tag the unwritten `Dp` body column. Decide whether V_F belongs in 𝒜's selection input b7 (B-ii).

### 9.11 Final verdicts

| Proposal | Verdict | Named fixes |
|---|---|---|
| Fix R1 (built) | **correct as built** | remove the residual `Dp` column |
| Fix R2 | **adopt with named fixes** | one rule ("unweighted"); name both Π̃ parts |
| Change R | **adopt with named fixes, after the replay-regime decision** | R-a to R-e |
| Fix G | **adopt, extended; it repairs a defect in the code today** | V_own as well as V⁻_his and D_τ; frozen Π̃₀ at the latched calibration; edit spec §1.3 and r7 §2.4.1 |
| Anchor and monitor | **adopt with named fixes** | N-a to N-d |

**Most serious error.** §1.2's "4× on every one of the ≤ 30 nights", and everything built on it (the 120 total, γ's purpose, "replace beyond 30 days"), assumes whole-window replay. The built replay learns from each moment once.
