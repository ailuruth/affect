# Critique 2 of the Cayley–ledger core (revision 2): routes, dials, care incentive and human behaviour

Independent critic, 2026-11-26T06:29:11Z. I did not write the design. Written under questions.md Q19 and DECISIONS.md D80: proof gaps are not reported, only concrete failures, each with a scenario and a numeric check where one was possible. Read on Q20's recommended reading: the inner state may know the partner closely, and only expression is bounded. Judged against D78, brief.md Principles 1–10 and C1–C10 (non-copying-dynamics-synthesis.md). Nothing was downloaded.

Read in full: brief.md; questions.md Q18 (with answer), Q19, Q20; DECISIONS.md D78, D80; both revision-1 critiques (routes and novelty, the novelty one in its summary and §1); design-cayley-ledger.md revision 2; sims/design-g2/checks.py (H1–H2 in full, the rest skimmed) and out.txt.

Checks are in `research/foundations/sims/critique-cayley2-routes/`. All run with `python3 -I <script>` (numpy, scipy) in under a minute, and their output is in `out.txt`. They use the design's own constants, filters and loop (v = √κu, w = v − s, y = 2√κs, s strictly causal, H_o and L as in checks.py, knowledge = L(w + s) as in H2). They test the design's claims on constructed inputs and are not evidence about people. Where a check depends on a property of the partner, it is stated as an assumption.

| Script | Finding |
|---|---|
| `ctx_route.py` | K1: knowledge → c̃ → fast block → TTS sample |
| `role_route.py` | K1b: role (partner VAD) in c̃, unscaled |
| `placation.py` | K3: own-body head pays for changing the partner |
| `lexical_rate.py` | K4: turn rate through the lexical latch into A |
| `sampled_fast_lp.py` | K2: phrase-onset sampling of the bounded fast path |
| `band_gap.py` | K5: the actual band gap |

## Summary verdict

Revision 2 closes all five of revision 1's route failures. I reproduce none of them. But the move that lets the slow block know the partner opens a new route that the design's own copy metrics cannot see. Ranked by severity:

1. **K1. Severe (D78 disqualifier). The slow block's knowledge reaches the face and voice through the fast block's context input, with no bound.**
   - **The hole.** S_f is a contraction "in its partner input… for every fixed (a, c, d)", and c̃ is a "free input" (§2.4). But c̃ contains S_s's states: body, mood summary and attended slot. Those states know the partner's held level (r 0.994, H2a), so c̃ is a function of w. The design's sum ‖ΔS‖ ≤ γ_f‖H_iΔw‖ + γ_s‖LΔw‖ omits the term ∂S_f/∂c̃ · ∂c̃/∂w. Bias-freeness holds only at c = ∅ (§2.10), so a c̃-only REN term exists.
   - **What it does.** Multiplied by the role switch, which is also in c̃, that term passes H_o as a transient at every turn exchange. The TTS samples it at turn onset and holds it for the phrase.
   - **Numbers (ctx_route.py).** The agent's rendered first-phrase F0 target tracks the partner's held F0 level with slope **+0.92** and r **0.91**, on every turn, for the whole evening. The bound is 0.10 held and 0.15 at any instant. Peak |y| is 1.9 against a claimed instantaneous cap of 0.15.
   - **What the design's own metrics show.** They read nothing: zero-lag slope +0.007, 1-min +0.002, 10-min +0.000. So falsifier F1 would pass.
   - **Why it disqualifies.** One learned REN weight on a shared c̃ coordinate runs all 32 channels from flat (A = 0) to copy (A = 3.5). Its ceiling is learned, not innate. §3.9's row "shared context coordinates… ≤ 0.198" is false.
   - **K1b: role.** Role, taken from the partner's VAD, enters c̃ without the κ_a scaling. A role-only display on jaw open therefore has a zero-lag slope of **0.83** on the partner's jaw at gain 0.3 (r 0.83), against the design's cap of 0.365.
2. **K3. High (Principle 6). Placation through the agent's own body.**
   - **The hole.** Only the partner head of 𝓜 is action-blind. The own-body head (i) is not, and C and V sit inside 𝒟(b).
   - **What it learns.** Head (i) learns that acts which make the partner look better lower the agent's own C.
   - **Numbers (placation.py).** Between two drafts of equal self-simulated relief, the scorer picks the flattering one with P = 0.72–0.99 at the 30-s horizon, and P = 1.00 on J's 10-min return, which also trains Π and S_f. On that horizon it gives up as much as 0.12 of self-simulated relief to make the partner smile.
   - **Interaction with K1.** If partners warm to being mimicked, this gives learning a gradient toward copying, and K1 gives the capacity. Copy then becomes attracting.
3. **K4. Medium, conditional on one reading of §2.5.2. Turn rate as a dial.**
   - **The hole.** The lexical latch is clocked by the partner's turn-end pulse. If lexical surprise enters A as one impulse per utterance, mean A swings by **35%** across the partner's speech-rate range, with the words fixed (lexical_rate.py).
   - **Where it goes.** Through c → Π's own word-appraisal gain (up to 0.8, outside the partner budget), this gives own-rate slopes of 0.07–0.28 on the partner's held rate. The claim is ≤ 0.10. It is revision 1's K1 by another door.
4. **K2. Low. Phrase sampling of the bounded fast path.**
   - If the agent times its own onset through y's latency channel, the sampled phrase level reaches **0.41** of the partner's last phrase step, against 0.339.
   - With uncertain onset timing it reaches **0.13–0.15**, which is within the claims. It is within D78 either way.
5. **K5. Low (accuracy). The design misplaces the "blind band".**
   - The design puts it at 4 s – 1 min. The minimum of |H_i|² + |L|² is actually **0.124 at a 97-s period**, and the sum is 0.415 at 30 s, not 0.08.
   - No copy follows from this: the fast ceiling is 0.18 at 30 s and 0.07 at 60 s. But the gap is at 1–3 min.

**Areas with no concrete failure found:**
- every other output path in the single wrap (item 1);
- the ℓ∞ slow block and the no-demodulation rule as such (item 3);
- Claude, draft choice, retrieval, replay and nightly learning, apart from K1/K3 and the stated TTS assumption (item 2);
- C1–C10 once K1 is fixed (item 6).

Details are in §6.

---

## 1. K1: slow knowledge into the fast block's context, uncapped (severe)

### Mechanism, from the design's own text

- **The fast block.** §2.4 gives S_f(ŵ) = diag(γ_f σ(φ_k)) · A(c̃) · M ∘ 𝓡_θ([Φ_R(Fŵ), √κ_a a], c̃, d), where 𝓡_θ is "Lipschitz 1 in its partner input. Context c̃ and own innovation d are free inputs."
- **What c̃ contains.** c̃ = (S_s's slow states: body, mood summary, attended slot; the lexical embedding; role from partner VAD; identity).
- **Why c̃ is not exogenous.** S_s's states are functions of L(w), and they know the partner's held level (H2a, 0.994). So c̃ depends on the partner, and S_f's contraction "for every fixed c̃" is not a contraction in w.
- **Bias-freeness does not close it.** The "bias-free S" rule (§2.10) makes S(0; c = ∅, …) = 0. With c ≠ ∅, which is always the case once the partner has been seen, 𝓡_θ has a term driven by c̃ alone: the REN's feedthrough and input matrices on c̃, with no norm bound.
- **What H_o does and does not stop.** H_o removes only the DC of that term. A product of the knowledge and anything in c̃ that switches at turn rate passes through. Role does (partner VAD), and the lexical latch does (a step at every partner turn end).

### Scenario

- **The partner.** All evening he speaks in a low, flat voice (held F0 level ℓ). In another episode he holds a smile.
- **What the agent knows.** S_s knows ℓ.
- **The learned term.** The REN has a c̃-only output of A·(knowledge)·(1 − role_listening) on the F0-level channel, or on the face channels.
- **At each partner turn end**, H_o passes a transient of size A·ℓ that decays over 4 s.
- **On the voice.** The TTS takes the phrase targets from y at the agent's onset, 1–3 s later (§2.8.5), and holds them for the phrase. So every first phrase of every agent turn is pitched at the partner's held level.
- **On the face.** The face shows y directly. At every turn exchange, it snaps toward the partner's held expression and relaxes over 4 s.

### Evidence (ctx_route.py)

8 h at 30 Hz. The partner's held level changes about every 20 min. Turns are 3–8 s, the agent's onset comes 1–3 s after the partner's VAD offset, and the design's exact loop and filters are used.

| c̃-path gain A | turn-onset rendered F0 vs partner level: slope, r | design's metrics: zero-lag, 1-min, 10-min slope | max \|y\| |
|---|---|---|---|
| 0 | 0, – | 0, 0, 0 | 0 |
| 1.0 | +0.26, 0.91 | +0.002, +0.001, 0.000 | 0.54 |
| 2.0 | +0.52, 0.91 | +0.004, +0.001, 0.000 | 1.09 |
| 3.5 | **+0.92, 0.91** | +0.007, +0.002, 0.000 | 1.90 |

The design's claims are:
- zero-lag in-phase ≤ 0.198;
- any instant of a held response ≤ 0.150;
- 10-min means ≤ 0.105.

The route breaks the second claim by a factor of 12. It carries held copying on the rendered voice at near-full gain. The first and third claims are measured by whole-run regressions, and those average the turn-locked copy to zero. So F1 as written cannot detect this route.

### Why it is a D78 disqualifier

- **One quantity, all channels.** A single learned quantity, the REN's c̃-input weight on a shared c̃ coordinate such as the mood summary, scales the copy on all 32 channels at once. That is a whole-face dial from flat to copy.
- **No innate ceiling.** The only innate factor is γ_fσ ≤ 0.45, which multiplies an unbounded REN output.
- **Copy can become attracting.** Combined with K3 (an incentive), copy can become attracting under the design's own learning.

### K1b: role is a partner signal that enters c̃ unscaled

Role comes from the partner's VAD, which is a partner input that R4 scales by √κ_a = 0.05. In c̃ it reaches:
- the REN, with no bound;
- Π, with the word-appraisal gain that sits "outside the partner budget", up to 0.8.

**role_route.py** puts a role-only display (no face input) on jaw open while the partner speaks. The agent's visemes are off then (half-duplex), so this is all of the agent's jaw while listening.

| Role gain | Zero-lag slope on the partner's jaw | r |
|---|---|---|
| 0.1 | 0.28 | 0.83 |
| 0.3 | 0.83 | 0.83 |
| 0.8 | 2.2 | 0.83 |

The design's own cap for this pair is 0.198 + 0.20·corr = 0.365. The same applies to burst energy and to speaking brow raises.

### Fix

1. **Make S_f bias-free in its partner input:** S_f(ŵ = 0; c̃, a, d) = 0 for every c̃.
   - c̃ may only gate partner-input terms multiplicatively: gain(c̃)·(Lipschitz-1 function of ŵ), with |gain| ≤ 1.
   - Own innovation d stays additive, with an amplitude that may depend on H but not on the knowledge.
   - Then Δs_f = gain·Δŵ + ŵ·Δgain. The second term is zero-mean and in phase with the partner's *transients*, not with his held level. It cannot carry a held level, because ŵ has no DC. I argue this but did not run a check on it.
   - Alternatively, give 𝓡 an innate Lipschitz bound in the partner-dependent part of c̃ and include the composite w → S_s → c̃ → S_f in γ (small gain): γ_f + L_c̃·γ_{w→c̃} ≤ γ.
2. **Treat role and the latch clock as partner inputs.** They enter scaled by √κ_a, or only as gates. That applies to Π too.
3. **Apply the same rule to G_Ω.** G_Ω reads c̃, and §2.6 caps it only "in e". With a 15-s output high-pass, a c̃-only term there is K1 with longer transients. Make G_Ω(0, c̃) = 0, and state that the 0.10 cap is joint.
4. **Re-test with a turn-locked metric.** Extend F1: regress the rendered phrase targets, and the face in the 0–4 s after each partner VAD offset, on the partner's held level.

## 2. K3: placation through the agent's own body (high; Principle 6)

### Mechanism

- **What is action-blind and what is not.** §2.7 makes 𝓜's partner head action-blind. Head (i), "own body next b", is trained by predictive likelihood with the agent's own outputs among its inputs (only the partner head is masked).
- **Why that matters.** C (concern), V (aversive load: being the target of the partner's aversive state) and A are body variables inside 𝒟(b) (§2.1: C has weight 0.8 and dead-band 0.05). They are driven by the partner's inferred body.
- **What head (i) learns.** In lived data, the partner looks better after some of the agent's acts, so C and V fall. Head (i) learns that act → own-C fall.
- **Who uses it.** The draft score (§2.8.3: −E Σ[𝒟(b̂) + …]) and J (which trains Π, S_f and the scorer) both evaluate 𝒟(b̂) through head (i).
- **The result.** A path from the agent's acts, through the partner's state, to its own objective. That is exactly what the "path-specific reading of Principle 6" (§2.11) says never happens. The phrase "the partner looking happier afterwards lowers C in the body (evidence), but the planner never predicts or values it" (§3.11) is false for head (i).

### Evidence (placation.py)

The partner is sad (𝒟(b̂_p) = 0.6). Of two drafts, one is followed by the partner's distress falling by e (time constant 5 s). That is an assumption about the partner. τ_C = 10 min, and the scoring is as in §2.8.3 at temperature 0.1.

- **Head (i) learns the effect.** Fitted on lived data, it gives C(+30 s) = 0.029 + 0.951·C0 **− 0.018·[flatter]**. It has learned the partner-mediated effect.
- **Equal self-simulated relief (R = 0.3 for both drafts):**

  | Horizon | e = 0.1 | e = 0.3 | e = 0.45 |
  |---|---|---|---|
  | draft score, 30 s: P(flatter) | 0.72 | 0.94 | 0.99 |
  | J return, 10 min: P(flatter) | 1.00 | 1.00 | 1.00 |

  With C, V and A rolled out from the action-blind partner head instead, P = 0.50 in every case.
- **What the agent pays for the partner's smile.** On J's 10-min return, it trades up to **0.03–0.12** of self-simulated relief for it, against R ranges of about 0.3–0.4. The same holds for Π: smiling at a sad partner who smiles back (ordinary human mimicry) lowers the agent's own C, so Π learns to smile *in order to change his face*.

### Fix

- In every rollout (draft score, J returns), compute the partner-driven body variables C, V and the partner part of A from their innate dynamics driven by the **action-blind** partner-head predictions, never from head (i).
- Train head (i) only on the partner-independent variables (E, H, I, and own-driven A). Alternatively, give it inputs with the partner streams clamped to the action-blind prediction.
- Add falsifier F4's test to the build: P(choice) against the predicted partner change, at equal R.

## 3. K4: turn rate through the lexical latch (medium, conditional)

### Mechanism

- **The latch.** S_s latches each partner utterance at the turn-end pulse (§2.5.6), and A "rises through the lexical surprise" with τ = 3 min (§2.5.2, §3.11).
- **The conditional.** If that is an impulse per utterance, A integrates the partner's turn rate. With the words fixed, the turn rate is set by the partner's speech rate and pauses: slower speech gives longer turns and fewer latches per minute.
- **Why it is uncounted.** The latch clock is a partner timing signal entering S_s outside L(w). S_s's bound holds "for every fixed c", so the route is not counted. The design's statement "no state of S integrates inter-utterance time" is true of the latch but not of A.

### Evidence (lexical_rate.py)

Same words and same surprises in every condition. The partner's held rate is 3–6 syllables/s; utterances are lognormal with median 20 syllables; the agent's turns are 3–8 s.

| Reading of "rises through the lexical surprise" | Swing of mean A across the partner's rate range |
|---|---|
| impulse | **35%** |
| held latched value | 0.3% (safe) |

If Π's word-appraisal path maps A's range onto g of the own speech-rate range (g up to 0.8, outside the partner budget), the agent's held speech rate follows the partner's with slope:
- **0.07** at g = 0.2;
- **0.18** at g = 0.5;
- **0.28** at g = 0.8.

The claim is ≤ 0.10. Arousal drives F0, energy and rate together, so this is a shared three-channel subspace.

### Fix

- Specify the held reading: A's lexical input is the latched value, divided by elapsed time and not summed per event.
- Or count the latch clock as a partner input inside S_s's γ_s budget.

## 4. K2: phrase-onset sampling of the bounded fast path (low)

### Mechanism

- **The sample-and-hold.** The TTS samples F0 level, F0 range, energy, rate and pause from y at each phrase onset and holds them (§2.8.5). That is an output sample-and-hold outside the wrap.
- **What the wrap bounds.** The fast block is bounded in ℓ₂ (energy), not pointwise.
- **The partner's input.** His voice channels are zero-order held per phrase, so they arrive as steps.

### Evidence (sampled_fast_lp.py)

An LP over every LTI closed loop the design allows on one κ = 0.3 channel (|S| ≤ γ_f|H_i||H_o|, with the slow block off) maximises the sampled value after the partner's last phrase step.

| Sample time after the step | Sampled value / step |
|---|---|
| exactly 2 s | **0.414** |
| uncertain, 1–3 s | 0.148 |
| uncertain, 2–5 s | 0.134 |

- The 0.414 case applies when the agent's onset is set by y's own latency channel (Claude's drafts ready early), so the fast block knows its own sampling time.
- It exceeds the claimed lagged broadband bound of 0.339 and the zero-lag bound of 0.198, but it is a per-channel strength within D78.
- **Fix:** take phrase targets from a 1-s causal mean of y, or from the slow component plus a separately capped fast term. Alternatively, put the per-phrase target sequence through its own discrete-time wrap.

## 5. K5: where the band gap actually is (low; accuracy and human behaviour)

**band_gap.py**, using the design's own discrete filters:

| Period | \|H_i\|² + \|L\|² | Fast-path ceiling γ_f\|H_i\|\|H_o\| |
|---|---|---|
| 30 s | 0.415 | 0.18 |
| 60 s | 0.173 | 0.07 |
| 97 s (minimum) | **0.124** | — |

- **What the design gets wrong.** §8.1's figure "≈ 0.08 at 30 s" is wrong, and so is "4 s – 1 min nearly blind".
- **Copy.** Lag copy of a 30-s oscillating partner is bounded by the fast disc at that frequency (|T| ≤ about 0.14), so there is no copy failure.
- **Human behaviour.** A partner whose face changes gradually over 1–3 min (becoming tearful slowly) reaches expression with at most about 0.03 from the fast path and about 0.15 from the slow path. The design should state the gap where it is.

## 6. Areas checked with no concrete failure

### Item 1: the single wrap

| Output | Finding |
|---|---|
| Face, gaze, head, bursts | only through y |
| Visemes | articulators only, half-duplex, echo guard |
| Voice levels, rate, pause | through y, but see K1 and K2 for the sample-and-hold |
| Non-lexical vocalisations | from y only; Claude's text is stripped |
| Blink and startle | outside the wrap, non-counterpart, counted as R7; blink entrainment at speech onsets is human |

Two outputs are computed partly outside y, with no copy shown:
- **Response latency.** The rendered latency is max(y-target, Claude readiness). With the API at 1–3 s and the y-target at 0.4–1.4 s, the rendered latency is mostly set outside the wrap. Its partner dependence is the length of his utterance, not his latency.
- **Turn length.** It is set by Claude's draft length (verbosity mirroring). That is the R14 definitional seam, which the design names.

### Item 2: Claude, drafts, retrieval, replay and learning

- **Draft choice and retrieval.** They reach expression only through:
  - the port (zero-DC; H6 holds as specified, apart from G_Ω's c̃ term, see K1 fix 3);
  - visemes;
  - the TTS contour, which is zero-mean under assumption 2.
- **What I found inside Ω.** No copy incentive in J other than K3.
- **Replay and nightly learning.** They change θ inside the cone for every θ. The fast block's parameters cannot make it copy, except through the unbounded c̃ path of K1, which is a parameter-capacity problem rather than a learning one.

### Item 3: the two structural rules

- No state flows from S_f to S_s. The only fast-to-slow path is L∘H_o through w (ℓ₁ ≈ 0.11), which the design counts.
- I found no violation of the ℓ∞ structure inside S_s.
- The dials found are:
  - the reverse direction, slow to fast through c̃ (K1);
  - the latch clock (K4);
  - role (K1b).

### Item 4: band edges

- K5 corrects the description.
- K2 is the only edge effect. It comes from sampling, not filtering.
- On narrowband partners (the jaw at syllable rate), the fast disc allows a lagged gain of up to 0.49 at half a period. The table in §3.8 states 0.339 "broadband". This is per channel and within D78.

### Item 6: human behaviour

With K1 fixed by gating, the following still hold:
- the fast match arrives at about 0.53 s;
- the sign can flip within a turn through the latch and role, now as gates;
- partner history within minutes comes from online slots;
- C1 and C7 are unchanged.

I found no C1–C10 violation. The ≤ 0.15 held facial reach is the design's own named weak point. Nothing in C1–C10 contradicts it, and no source I read measures a stronger held face response in conversation.

### Revision 1's failures

I re-checked all five:
- speech rate through Q;
- duration-proportional cost;
- the lateral mirror;
- ASR tokens;
- blindness.

All are closed as the design states, except that K4 reopens speech rate under one reading.

## 7. Sources read

| Source | How read |
|---|---|
| design-cayley-ledger.md, revision 2 | in full |
| sims/design-g2/checks.py, out.txt | out.txt in full; H1, H2 and the wrap simulator in full, the rest skimmed |
| critique-design-cayley-ledger-routes.md | in full |
| critique-design-cayley-ledger-novelty.md | summary and §1 |
| brief.md; questions.md Q18–Q20; DECISIONS.md D78, D80; non-copying-dynamics-synthesis.md | in full |
| TTS, ASR and Claude API behaviour; partners' response to being mimicked | **not measured.** Stated as assumptions in K1 (TTS samples at onset, as specified), K2 (onset timing) and K3 (partner effect e) |
