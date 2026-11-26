# Critique 5 of the Cayley–ledger core (revision 5): routes, fast mimicry at the ceilings, and the learning loops

Independent critic, 2026-11-26T09:22:23Z. I did not write the design.

**Standard.** This critique follows questions.md Q19 and the operator's answers to Q20–Q23 (DECISIONS.md D78, D80–D84):
- the inner state may know the partner closely; only expression is bounded;
- fast, partial, per-expression mimicry within the Q22 ceilings must stay;
- only whole-face copying and getting stuck in copying are ruled out;
- each expression has its own innate ceiling;
- strong expressions come from words and face through the agent's own appraisal;
- the engine runs through the subscription.

Proof gaps are not reported. Each finding is a concrete scenario with numbers. "Copy" is the slope of the rendered agent channel (after `sat`) on the partner's same channel, over window means of 2 s, 10 s and 1 min, at the best lag from 0 to 3 s.

**Read:**
- brief.md;
- questions.md: the Q18 answer and Q19–Q23;
- DECISIONS.md: D78 and D80–D84;
- critique-4-design-cayley-ledger-routes.md and critique-design-own-body-generative-routes.md;
- design-cayley-ledger.md, revision 5, in full, with r1 §3.1–3.2 for Claim W and N2;
- sims/design-g5/checks.py and out.txt.

**Checks.** They are in `research/foundations/sims/critique-cayley5-routes/checks.py`, sections K1–K7. Run `python3 -I checks.py` (numpy and scipy, about 2 minutes). The output is in `out.txt`.
- The checks use the design's constants: γ_f, κ_k = FASTFRAC_k c_k (1 + γ_f)/(2γ_f), the 4-s H_i and H_o, the 0.45-s echo, the shares, the trace constants, Π₀ and Π̃₀, τ_b and τ_ω.
- The partners are constructed. They are not evidence about people.
- The operators used in K1 and K2 satisfy the design's own class: strictly causal, with ‖S_f(w)‖_T ≤ γ_f‖w‖_T on every truncation. The checks verify this numerically for each run.

## Summary

Revision 5 closes critique 4's findings as specified: the ω seam, the event types and the style drift. I found no failure in the centring, the masks, the events or the Claude route. The new fast gear at the full ceilings, though, opens two concrete failures, and a third sits in the learned word reader. Ranked:

1. **High (D78 and Q22: per-channel ceilings broken). The fast wrap bounds directions, not channels, so cross-channel paths inside S_f exceed the ceilings on co-moving channels.**
   - **The gap.** Claim W's matrix sector (r1 W1) caps ⟨y, u⟩ ≤ b⟨u, Ku⟩ along every partner direction. It does not cap the slope of one agent channel on the same partner channel when his channels move together. Revision 1 said so itself (N2: a per-channel bound needs Σ_j|H_kj|σ_j/σ_k ≤ κ).
   - **Why revision 5 makes it worse.** It raised κ on LP, CR, BU_L, RHY and BRE to the full ceilings (κ_LP = 0.564). It then charged only the diagonal echo to each channel (H5, H6, H9).
   - **Numbers (K1).** A laughing partner, with S_f = γ_f e_k vᵀ inside the sector (W1 ratio 0.02–0.09). Pooled 1-min rendered slopes:
     - breath **0.39 (2.6 c)**;
     - jaw **0.13 (1.3 c)**;
     - cheek 0.20, or **0.24 (0.95 c) with every route at its cap**.

     At 2-s windows:
     - cheek **0.44 (1.8 c)**;
     - head pitch **0.66 (6.6 c)**;
     - F0-range contour **0.37 (3.6 c)**;
     - lip pull with every route **0.36 (> 0.35)**.
   - **Rule J inside the fast block.** The REN has no sign structure, so a sad brow onset of 0.5 can return a smile of +0.074 within 0.5 s.
   - **Not violated.** The whole face stays bounded (0.28 on the laughing direction, K7).
2. **Medium (D78 and D81: copy attracting under learning, getting stuck in copying). The fast gates are trained by "likelihood of own fast dynamics", and a partner who mirrors the agent makes his face a predictor of the agent's own face.**
   - **A mirroring partner (K3).** The nightly fit drives the lip-pull gain from the innate 0.227 to the cap **0.350** within 60 nights, for a mirror gain μ ≥ 0.3. Under one reading of the target it needs μ ≥ 0.5.
   - **A partner who does not mirror.** It erodes the gain to 0.07–0.14, so the innate mimicry D81 asks for fades.
   - **The common cause (K4).** The revision-5 play-surprise laugh, which fires all evening, co-occurs with his punchline laughter. The fit then wants a laugh-at-his-laugh gain of **0.45**, above the 0.35 cap. With finding 1 the target of that pull is the cross-channel maximum.
   - **Why it matters here.** S5 makes the operator the mirroring partner by design.
3. **Low–medium (shared-prior learning, the own-body critique's pattern). The word-need reader learns his per-topic face, and the agent displays it, uncapped.**
   - **Across topics (K5).** The agent's 20-s mean inner brow at his words has a slope of **0.74** on his per-topic brow, against c_BI = 0.20. It shows whenever the topic comes up, even with his face neutral.
   - **A partner who mirrors the agent's concern face.** The decoded need inflates by 1.2–1.6× (V 0.26 → 0.42 at μ = 0.7). The fixed point is finite: the loop amplifies but does not lock.
   - **Under D83.** This is arguably "own appraisal". But it is a night-delayed per-topic copy on a ceilinged channel, with no ceiling.
4. **Low–medium (a bound claimed for every parameter value). The rectification allowance r_k is measured on the linear echo only.**
   - **The construction (K2).** An admissible S_f trades energy for area: an RMS envelope with a 12-s memory, times the sign of his head micro-motion.
   - **The numbers.** In the same loop it raises rendered BU_L from 0.52 c to **0.91 c**, above the 0.867 c charged. The BU_L total is then **1.04 c**, against the claimed 0.996.
5. **Low (a specification condition). Claude's drafts reach the voice only if WORLD *shifts* TTS prosody rather than replacing it.** The draft choice is a function of F, through the 𝓜 rollout. If the TTS's text-driven F0 range and energy survive at phrase level, his laughter selects the livelier draft, on channels with c = 0.05–0.10.

**No concrete failure found:**
- **(1) The moving baseline (K6).**
  - It gives a held copy of a *change* of his mood that fades over about 6 sessions, at ≤ s_C c (0.175 on lip pull).
  - The lagged session slopes are ≤ 0.03. With ω < 0, the baseline reaches the face only as +|ω| s_C c b, which is the same size.
  - Lemma S\* holds on everything I tried.
- **(2) The whole face** stays ≤ 0.28–0.35 even with finding 1.
- **Dyad loop stability.** Loop gain < 1 in every case, so there is no dynamic lock-in.
- **(4) The events.**
  - They are T-only as specified.
  - Contact relief at sight has a fixed amplitude.
  - The play, curiosity and laugh reflexes read words and turn order only. The tempo stays out (T1).
- **(5) Masks and style drift.**
  - Every zero-ceiling row is closed in the fast wrap (κ = 0), the cone, the appraisal and Δ.
  - With no anchor, no drift.
- **(3) Claude.**
  - The transcript strips laughter tokens.
  - The draft selection is 1.6 bits, declared. Its only routes into expression are the visemes (≤ 0.05), P_name (attenuate-only) and the TTS (finding 5).
- **D84.** It is met.

---

## 1. The fast wrap's cross-channel paths (high)

**Mechanism.**
- **The operator.** S_f = diag(γσ(φ)) · g ⊙ A · M ∘ 𝓡_θ([Φ_R(Fŵ), …]). 𝓡_θ maps all 116 inputs to all 33 outputs.
- **The constraint.** It is the vector bound ‖S_f(w)‖_T ≤ γ_f‖w‖_T.
- **What that leaves free.** With w = K^{1/2}Pu − s_f and y = 2K^{1/2}s_f, the gain from his channel j to the agent's channel k reaches 2γ_f√(κ_kκ_j). The agent's channel k can then collect from every co-moving channel of his.
- **For a laughing partner** (LP, CR, BU_L, RHY and BRE together), y_k/a ≈ 2√κ_k γ_f ‖K^{1/2}1_G‖. For breath that is about 0.63 per unit of his laugh configuration, against c_BRE = 0.15.
- **What the design charges.** §2.4 states the cap as "the zero-lag in-phase gain on channel k ≤ FASTFRAC_k c_k". H5, H6 and H9 charge only the diagonal echo.

**Scenario (K1).**
- **The partner.** H9's laughing partner, 6 h at 20 Hz, with jaw, head pitch and F0 range also moving with his laughs.
- **The operator.** S_f = γ_f e_k vᵀ, where v is the normalised K^{1/2} over his other laugh channels. It has a 0.45-s delay and the design's H_i and H_o.
- **The sector check on each run.** ⟨y, u⟩/(b⟨u, Ku⟩) = 0.02–0.09, so the design's own W1 holds.

| Agent channel (c_k) | Design's diagonal echo at the cap: 2 s / 1 min | Cross route, same sector: 2 s / 10 s / 1 min |
|---|---|---|
| breath BRE (0.15) | 0.096 / 0.086 | **0.405 / 0.347 / 0.386 (2.6 c)** |
| jaw JO (0.10) | 0.018 / 0.015 | **0.139 / 0.119 / 0.133 (1.3 c)** |
| cheek CR (0.25) | 0.137 / 0.059 | **0.444** / 0.316 / 0.204 |
| head pitch HP (0.10, signed) | 0.064 / 0.004 | **0.661** / 0.054 / −0.025 |
| F0 range FR (0.10, contour) | 0.059 / 0.002 | **0.365** / 0.025 / −0.006 |
| lip pull LP (0.35) | 0.130 / 0.003 | 0.301 / 0.097 / 0.046 |

- **Every route at its cap together** (cone, charged cross, appraisal, plus the cross fast route):
  - cheek 0.457 at 2 s and **0.239 (0.95 c) at 1 min**;
  - breath **0.390 (2.6 c)**;
  - lip pull **0.359 at 2 s**.
- **Rule J.** The agent's LP ← his BI at the sector limit returns a smile of +0.074 to a 0.5 brow onset within 0.5 s. Rule J says "anywhere", but nothing in the REN enforces it.

**Why it counts.**
- **D78 and Q22.** The per-channel ceilings are exceeded, on the rendered output, at the 2-s scale that D81's fast mimicry lives on, and on one-sided channels also at 1 min, after rectification.
- **The operator's own words.** The design measures the fast part per diagonal only, and its claim is "for every parameter value". The REN is learned, and finding 2 shows a training signal that pulls toward exactly such routes.
- **What still holds.** The whole-face direction stays inside W1 (0.28, K7). This is a per-channel failure, not a whole-face one.

**Fix.**
- **Make the partner-input part of 𝓡_θ per channel.** Output k reads only Φ_R of his channel k (mirrored for the lateral channels), plus the exogenous a through √κ_a.
- **Cross-channel fast responses,** if wanted, go through a separate fixed innate path in the away orthant (signed as G₀ is), charged to s_X.
- **What that gives.** H5 and H9 then bound the fast part, and rule J holds by construction.
- **A weaker alternative.** Impose the r1 N2 row condition Σ_j √(κ_kκ_j)|M_kj| ≤ FASTFRAC_k c_k (1 + γ_f)/(2γ_f) on the linearisation. That is hard to enforce on a REN.

## 2. The fast gates learn to copy a partner who mirrors (medium)

**Mechanism.**
- **The training.** §3.5 item 5 trains the fast gates and 𝓡_θ by "the likelihood of own fast dynamics plus the θ₀ pull", with nothing else specified.
- **What a mirroring partner does to it.** His face at t − 0.45 s contains the agent's own face from t − 0.9 s. The agent's own expressions are smooth (rise 0.4 s, apex 1.5 s, decay 3 s), so his face predicts the agent's next face, and the fitted gain rises.
- **The same through a common cause.** Any expression of the agent's that co-occurs with his produces the same pull.

**Scenario (K3).**
- **The agent.** Lip pull = own word-driven smiles + g · HP(his lip pull, 0.45 s).
- **The partner.** u = μ · (agent's face 0.45 s earlier) + his own smiles.
- **The fit.** Nightly least squares on 4 h, with the θ₀ pull at λ = 0.5. Two readings of the target: the rendered own fast face, or the own non-fast residual.

| μ (his own expressivity) | Gain after 60 nights, rendered target | Gain after 60 nights, residual target |
|---|---|---|
| 0 (1.0) | 0.138 | 0.071 |
| 0.3 (1.0) | **0.350 = cap** | 0.208 |
| 0.5 (0.5) | **0.350** | **0.350** |
| 0.8 (0.3) | **0.350** | **0.350** |

The innate gain is 0.227.

- **The common cause (K4).**
  - The agent's play-surprise laugh fires 0.6 s after his utterance end, at every play turn all evening (revision 5).
  - He laughs at his own punchlines.
  - The least-squares gain of own fast laugh on his laugh is **0.451**, above the BU_L cap of 0.35, so the gate is pinned at 1.

**Why it counts.**
- **D78's fourth condition.** Copying must not be attracting under the design's own learning, and here the in-phase gain settles at its maximum because he mirrors.
- **Claim L.** Item 5 only says the gates stay in range.
- **S5.** The brief's S5 makes the operator's mirroring the success criterion, so this is the expected case, not an adversarial one.
- **With finding 1 unfixed,** the attractor is the cross-channel route.
- **The opposite failure.** With a partner who does not mirror, the same objective erodes D81's innate echo to 0.07–0.14.

**Fix.**
- Do not fit any partner → own-face gain by predicting the own face.
- Fix the per-channel gain at θ₀. Let only T context modulate it, through a display-blind objective. Or fit on partner-shuffled or partner-swapped input, so that his mirroring and common causes contribute zero.
- Add a falsifier: the fast gain must not rise with his mirror gain.

## 3. The word-need reader acts out his per-topic face (low–medium)

**Mechanism.**
- **Training.** The reader is fitted nightly to Π̃(his face) over the 20 s after each of his utterances (§2.8).
- **Runtime.** It is words only. Its output drives word concern (BI 0.25) and distress events (BI 0.45, LD 0.35) in the free display, which has no ceiling.

**Numbers (K5, with the design's Π₀, Π̃₀ and display rules).**
- **The topic route.** Across words whose true face reads V 0.16, 0.26 and 0.37 (his brow 0.08–0.19), the agent's 20-s mean inner brow is 0.035, 0.080 and 0.113. That is a slope of **0.74** per unit of his brow, against c_BI = 0.20.
- **With a partner who mirrors the agent's concern face.**
  - Decoded V rises to 0.19, 0.32 and 0.44 at μ = 0.3, and to 0.26, 0.42 and 0.56 at μ = 0.7.
  - The agent's brow rises 1.4–2.3×.
  - Π̃₀ is sensitive: his brow 0.10 alone reads as V 0.13.

**Why it counts, and the limit.** This is the shared-prior pattern of the own-body critique (finding 3): a night-delayed per-topic copy on a ceilinged channel, shown at the words even while his face is neutral. It uses the agent's own display form (no zero-ceiling channels), and the mirror loop converges, so it is not lock-in. D83 may accept it as appraisal. If so, that should be stated as a decision, not hidden under "common cause, words fixed": the month-swap surrogate would expose it.

**Fix.** Any one of these:
- train the reader on separated reports (words) instead of his face;
- read his face only at his utterance onset, before the agent's display can be mirrored;
- cap word concern's BI share at c_BI × (the agent's ω_sym).

## 4. r_k is not a bound over admissible S_f (low–medium)

**Mechanism.**
- **What r_k was measured on.** The worst rendered 1-min slope of the *linear* full-gate echo.
- **What the class allows.** A truncation-gain bound allows energy to be traded for area. An output of amplitude a over a duration D has area ∝ √D for fixed energy.
- **Why the rectification follows.** A sign carrier at 1–3 Hz survives H_o, and `sat` removes the negative half on channels that rest at 0.

**Scenario (K2).**
- **The operator.** z = γ_f √(LP_12s(ŵ²)) · sign(his head micro-motion). The truncation bound is verified at every T.
- **The loop.** Run in the design's loop on laughing bursts.
- **The numbers.** Rendered BU_L pooled 1-min slope: **0.91 c**, against 0.52 c for the linear echo in the same loop. The design charges 0.867 c. BU_L total: 0.0764 + 0.02 + 0.032 + 0.91 = **1.04 c**.

**Fix.** Any one of these:
- give S_f a finite memory (an FIR-like REN with impulse response ≤ 1.5 s) and measure r_k over that class;
- render one-sided fast output on a pedestal, so that `sat` never clips it;
- charge r_k = FASTFRAC_k at the design stage.

## 5. Claude and the TTS: a condition (low)

**What is fine.**
- **What Claude sees.** The transcript (laughter tokens removed), the markers and the snippets. Claude does not see his face or voice.
- **The selection.** The 𝓜 rollout reads F, which is allowed knowing, declared at 1.6 bits.

**The condition.** The chosen text enters expression through the TTS. Plan A "shifts" phrase-level F0 level and range by WORLD. If the TTS's own text-driven prosody survives, the F-dependent choice moves FR and EN with his laughter. Exclamatory against flat drafts differ by more than these ceilings (0.05–0.10).

**Fix.** Specify that WORLD *replaces* phrase-level F0 level, range, energy and rate with the targets of rule 7. Keep stripping interjections from Claude's text before the TTS (R11).

## 6. Areas checked with no concrete failure

- **The baseline b_id and ω (K6).**
  - **What centring does.** The cone answers a mood change at ≤ s_C c and adapts over about 6 sessions. That is a held copy of a change, within the share.
  - **Lagged session slopes.** ≤ 0.03 at lags of 1–12 sessions, for session-white and monthly moods.
  - **The baseline itself.** With ω < 0, it reaches the face only as +|ω| s_C c b, of the same size and lagged.
  - **Lemma S\*.** It holds.
  - **The arrival mask.** It is attenuate-only and bounded (H14).
- **Stuck in copying, dynamically.** Even with findings 1–2, the loop gain with any mirror of μ ≤ 1 is < 1 (H8, and K1's gains ≤ 0.66 on one channel), so the dyad does not hold a mutual copy. "Stuck" happens only through learning (findings 2–3).
- **The events from words, hurt, contact, play and curiosity.**
  - **The hurt map's teacher** is the threat reflex (F), so his glare and shouting enter the weights. But the display it drives is away (hurt, no frown back).
  - **Everything else** reads words and turn order.
  - **Tempo.** Event times follow his turn ends but carry no rate code.
  - **The weak spot** is the reader (finding 3).
- **The masks on anger, disgust and contempt.**
  - κ = 0, no toward cone entries, and no appraisal or Δ weight.
  - LS and CHR are gated by the agent's own a_d.
  - Finding 1's routes cannot write a zero-ceiling channel, because κ_k = 0 multiplies the output.
- **Style drift.** H4 is reproduced in substance: no anchor, so no drift.
- **The whole face (K7).** The W1 bound on the laughing direction is 0.28, equal to H0's quadratic form.
- **D84.** Forks, no tools, effort `low`, no temperature and no API key.

## 7. Verdict

Revision 5 fixes what critique 4 found, and its slow side (Lemma S\*, E1, the mask) holds against everything I built.

The new fast gear at the full ceilings fails in two concrete ways:
- its per-channel cap is a direction cap, so co-moving partner channels push breath, jaw, cheek, head pitch and the F0 contour past their ceilings (§1);
- its unspecified likelihood objective makes the in-phase gain climb to its cap for exactly the partner S5 hopes for, a mirroring operator (§2).

Both fixes are local:
- a per-channel fast block;
- a fast-gain objective that cannot learn from his mirroring.

With them, and with the reader decision in §3 made explicitly, I found no route above the ceilings.
