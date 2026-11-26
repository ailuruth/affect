# Routes critique of the commutator-coupling design

Independent critic, 2026-11-26T19:07:44Z

**Design checked:** research/foundations/design-commutator-coupling.md. I also read its checks (sims/design-cc/checks.py, out.txt).

**Standard:**
- questions.md Q18 and Q19: only concrete failures count, not gaps in rigour.
- Operator answers Q20–Q23 and Q26.
- DECISIONS.md D78, especially condition 4: copying must never become a state the agent settles into.
- D81: fast, partial, per-expression mimicry must stay.
- D83: each expression has its own innate ceiling, and strong expressions come through the agent's own appraisal.

**My checks:** research/foundations/sims/critique-cc-routes/cc_routes.py (output in cc_routes.out.txt, 6 min) and cayley_ledger_lag.py (output in cayley_ledger_lag.out.txt, 30 s).
- Both load the designs' own operators verbatim at run time: the design's limiter, echo, metric and tree, and the Cayley ledger7 function.
- All signals are constructed. They only exhibit mechanisms and are not evidence about people.

---

## Verdict: not fit

The core algebra holds (P1–P4, C1–C4), and the efference own side does remove the C7 lock for the commutator route itself. But the claim that carries the design is false as written. That claim is "everything his face and voice caused is capped at c_k^tot at every lag and scale; exact copy is outside the reachable set on every channel" (§2.7, §3.6, §4).

**Concrete failures, most serious first:**

1. **High. Calibration sits on the expressive path, so the ceiling is learned and exact copy passes.**
   - The echo and both limiter stages use the calibrated x̃ = ref + (x − b)·σ_ref/max(σ_id, 0.25σ_ref), which amplifies his movements up to ×4 per identity.
   - The Cayley design this one reuses forbade exactly that: rule 6 says σ_id and b^read "may only enter readings … never a gain on a partner path".
   - For a reserved partner, **an exact copy of his raw lip pull passes both caps untouched**: 1.000 → 0.991 against his raw channel (A1). The echo becomes 0.61 of his raw smile, against a ceiling of 0.35.
   - One per-identity property, his expressiveness, raises the effective ceiling of every non-zero channel at once, up to ×4.
2. **High. Routes that are partner-caused but held at their factual values in S⁰ bypass the limiter and leak into the own side.**
   - **His word-event counts.** These are his utterance onsets and turn ends, entering z as a level-1 path. They are a rate code on his tempo, and Cayley's T1 was dropped. Any route through them has δ ≡ 0, so the limiter never acts on it (A2: a rate readout tracks his rate at slope 0.55 against c^tot 0.10).
   - **Claude's draft choice.** Drafts are scored on z, so the route runs z → reply → a → ρ. This is a closed loop through the own side, which P7 says does not exist, and the route is missing from the §4 table.
   - **The concern posture.** Cayley declared its brow slope over his sadness at 0.43–2.05, above c^tot_BI = 0.45.
3. **High/medium. Slow lagged following is invisible to both the limiter and the design's own copy metric.**
   - A 90-s delayed copy renders at 0.86 and a 5-min one at 0.70 (1-min block means, ceiling 0.35).
   - A 5-min low-pass follow passes the limiter with no attenuation at all (rms ×1.04).
   - The design's own metric scores all three as about 0 before the limiter, so its checks could never show this.
   - Risk 8 ("replay beyond 60 s") understates the problem. Any slow follow (his face level → body route and slow blocks → display) is uncapped, and the core's slow blocks are slow filters of his face.
4. **Medium. On zero and small ceilings, the limiter deletes legitimate appraisal-driven expression.**
   - With c = 0 the factor is 0 for every partner-caused movement, including "away" movement (A4: rms 0.00).
   - So on the 13 zero channels, nothing caused by his face or voice can ever show: no lid raise at his shout, no frown of concern or puzzlement.
   - At c^tot 0.10 (voice) a non-copy route keeps 29 % of its size; at c 0.03 (lateral channels) it keeps 9 %.
   - This conflicts with D83: strong expressions through the agent's own appraisal.
5. **Medium. The limiter is not attenuate-only, and the D81 echo has no reserved share.**
   - With a learned following route present, 15 % of active frames flip sign and 38 % of near-zero input frames get output (A5).
   - The echo is cut to 0.065 peak (×0.45).
   - The dyad pretraining objective does push the core toward following, which §3.6 and §8.3 say nothing does. So in practice the D81 echo is the part that gets eaten.
6. **Low. A knowing failure, not copying: the divisive floor ε_kj ∝ 2^j erases slow-scale ρ.**
   - Mean ρ for a maximal-area pair is 0.08 at j = 12, 0.02 at j = 14, and 0.000 at j = 20 (A6).
   - So the "relationship and temperament" scales 14–24 carry nothing, and §3.2's table and ablation 6 do not hold.

**What I checked and found sound:**
- **P1–P4 and the tree identity.** The algebra is right.
- **Lags 0–60 s in x̃ units.** C6's lagged copies are capped at 0.26–0.28.
- **No lock through the rendered face on the commutator route,** thanks to the efference own side.
- **The echo's timing** (0.83–1.03 s) and its partiality in x̃ units.
- **m_k is bounded by G_k** in x̃ units.
- **Mutual loops.** I found no copy attractor with an answering partner. Even with failure 1, the loop gain (raw echo 0.61 × a human return of about 0.3) is well below 1. The structural loop in failure 2(b) runs once per turn, and I did not exhibit a lock through it.
- **The counterfactual runs are computable.** 34 cores is cheap. Each S^k also needs its own Π̃/appraisal pass (module 1), which §8.5 does not cost, but that is affordable at 2 Hz.
- **Cross-channel mask.** The core's mask holds. Cross-channel effects all reach the outer cap at c^tot, so nothing leaks around it; the proxy problem is the declared risk 3.

---

## Evidence

### 1. Calibration on the expressive path (A1)

**Construction.** A partner whose raw smile is 0.25 of the C6 partner's, so σ_id = 0.25 σ_ref (the ×4 floor). x̃ is formed exactly as in §2.1. The full two-stage limiter runs at c_LP = 0.35 and then at c^tot = 0.55, as in §2.7's rendered-channel formula.

| Route | Gain vs x̃, before → after | Gain vs his raw channel, before → after | rms out/in |
|---|---|---|---|
| exact raw copy, lag 0.9 s | 0.250 → 0.248 | **1.000 → 0.991** | 1.00 |
| exact raw copy, lag 0 | 0.250 → 0.248 | **1.000 → 0.994** | 0.99 |
| frozen echo on x̃ (G 0.224) | 0.154 → 0.154 | **0.614 → 0.614** | 1.00 |

**Why it passes.** The limiter's κ scales as 1/(scale of x̃), so the cap toward his raw face is c·σ_ref/max(σ_id, 0.25σ_ref).

**Where exact raw copy passes the inner cap.** A raw copy at gain 1 has gain σ_id/σ_ref against x̃. It passes the inner cap whenever σ_id/σ_ref ≤ 0.85 c_k. For a partner at the floor (0.25), that holds on LP and BU_L (0.85 × 0.35 = 0.30) and on RHY (0.255). On CR and BI the allowed raw gain is 0.85 and 0.68. Through c^tot the raw allowance reaches 4 × 0.85 × 0.55 = 1.9 on LP.

**The echo is not "reused verbatim".** §6 says it is, but Cayley's E_k used his raw reflected channel, and §2.1 changes that to x̃. For a reserved partner the frozen G_k therefore becomes 4G_k in raw units: LP 0.90, BU_L 1.12, RHY 0.96.

**How this meets D78's disqualifiers.**
- A learned ceiling: σ_id is learned per identity, as the MAD over his last 6 sessions.
- A shared quantity that moves many channels together: a person's low expressiveness, or a camera that compresses his blendshapes, lowers σ_id on every channel at once.

**Caveat.** If the operator means ceilings to be relative to his own expressive range, this is not a copy failure. But then the design must state it, and the copy metric must change. The project's metric so far, and Cayley's rule 6, use his raw channel.

### 2. Partner-caused routes held factual in S⁰

The design defines S⁰ as "his face and voice held, words, turn events, the agent's own words, the posture and the gate kept factual". Then δ = s − s^{S⁰} is blind to everything his face or voice causes through those, and y = s^{S⁰} + Lim(δ) renders it uncapped.

**(a) His speech timing.**
- §2.5 puts "its own and his word-event counts (utterance onsets, turn ends …)" in u_j, the own path at level 1. That is a partner increment entering the core, although "what never enters: the partner's increments" (§2.5) says it cannot.
- A CDE integrates it into a rate code on his tempo. His onsets also co-vary with his voice-energy and jaw channels.
- A2: a leaky integrator of his onset counts read onto the agent's rate target. δ is exactly 0 (max |δ| = 0.0, limiter output 0.0), and the rendered rate follows his at slope 0.55 against c^tot_rate = 0.10. The gain 0.5 is an illustrative readout; δ ≡ 0 for any gain.
- The objective pushes this way too. §8.4 pretrains "own next face/voice" on recorded dyads, where people do accommodate speech rate.
- Cayley closed this route with T1 ("no rate codes in T"). This design reuses Cayley's S⁰ rule 10 but not T1.

**(b) Draft choice.**
- §8.6 scores Claude's drafts by a rollout "with z as the rollout state", so z, which his face drives through ρ and the body route, selects the reply.
- The reply is held factual in S⁰. It reaches s^{S⁰} through word events and the word-driven display, and so reaches a = s^{S⁰}, which feeds ρ.
- That closes the loop ρ → z → draft → a → ρ through the own side. §3.4's "nothing the agent does because of him re-enters ρ" is false at turn scale.
- Cayley counted this route as R18′ (≤ 1.6 bits per turn). Here it is missing from the §4 table and outside the limiter.
- Its rate is about one choice per turn, and I did not exhibit a lock. It is an uncounted route, not a demonstrated attractor.

**(c) The concern posture.**
- It is held equal in S⁰ (§2.7 last bullet), so it sits in both s^{S⁰} and a, uncapped by the limiter.
- Cayley's own numbers for it are BI pooled slope 0.43–2.05 over his sadness, which is above c^tot_BI = 0.45.
- §3.6's "every channel's partner-caused coherent gain ≤ c_k^tot" is therefore false as stated.
- It also puts a partner-caused, lagged brow movement into the own side of ρ_BI, so the core reads "I followed him" when only the posture rose.

### 3. Slow following (A3; 2 h; smile bursts plus a session-scale drift)

| Route (ceiling 0.35) | Design's metric (lags ≤ 60 s, window-centred), before → after | 1-min block means, best lag 0–10 min, before → after | 5-min means, after | rms out/in |
|---|---|---|---|---|
| copy, lag 90 s | −0.080 → −0.055 | 0.976 → **0.859** (lag 90 s) | 0.857 | 0.67 |
| copy, lag 5 min | +0.041 → +0.037 | 0.898 → **0.702** (lag 300 s) | 0.303 | 0.66 |
| low-pass follow, τ 5 min, DC gain 1 | +0.007 → +0.007 | 0.111 → 0.112 | **0.425** | **1.04** |

**Why the limiter cannot see slow content.**
- Stage 2 high-passes everything at ≤ 60 s.
- Stage 1's residual band pairs samples only 34 s apart, with lags ≤ 60 s.
- The independent metric removes window means, so it shares the same blindness.

**Which routes produce slow following.** The body route (his face → Π̃ → appraisal → b → z) and the slow blocks (memory from 2 min up to 620 h) are slow filters of his face. A display that follows his slow face level with any DC gain passes unmodified; the third row shows the limiter did nothing (×1.04).

**Contrast with Cayley.** Cayley capped the same thing with sup-gain bounds on its 20-min and 3-h cone traces.

### 4. Zero and small ceilings (A4; independent, non-copy route as in C6's last row)

| Ceiling c | rms out/in of an independent route | Same route, away (−0.3 × his, lag 1 s) |
|---|---|---|
| 0 (13 channels) | **0.00** | **0.00** |
| 0.03 (lateral, same-channel) | 0.09 | — |
| 0.10 (voice c^tot) | 0.29 | — |
| 0.35 (smile) | 0.73 | — |

**Why.** κ is a maximum over about 3,600 lags of a sign-blind statistic, so it is never 0 on finite data, and α = min(1, 0.85c/κ) = 0 whenever c = 0. The limiter cannot tell "toward his channel" from "partner-caused at all".

**What this costs.** D83 allows anger, disgust and contempt *toward his* to be 0. It does not ask for every appraisal-driven lid, brow-lowerer or lip-press movement caused by his face or voice to be deleted. That includes surprise at his shout and a frown at his confusing face. (Cayley's ledger with c = 0 constrained only the toward slope.)

### 5. Attenuate-only and the echo's share (A5; smile, c 0.35)

| Partner-caused content | Frames with \|out\| > \|in\| | Sign flips | Output where input < 0.01 | Echo peak (0.151) after | Echo rms |
|---|---|---|---|---|---|
| echo alone | 0 | 0 | 0 | 0.151 | ×0.99 |
| echo + follow 0.5 at 1.0 s | 0.016 | **0.150** | **0.379** | **0.065** | ×0.45 |
| echo + follow 0.3 at 1.5 s | 0.019 | 0.001 | 0.085 | 0.096 | ×0.71 |

**Why it is not attenuate-only.** Each causal Haar band gets its own factor α_o. A sum of differently scaled bands is not a shrink of the input: it creates movement after a burst and flips its sign. These are the same defects that Cayley critique 7 ranked high for the ledger.

**Why the echo gets eaten.** The echo has no reserved share of c_k. Meanwhile §8.4's dyad pretraining predicts recorded people's "own next face", which includes their own following of the other (the confound named in §8.4). P6 says the core can reconstruct him from ρ. So the objective does ask for a following route, which contradicts §3.6's "nothing in the objectives asks for that". When that route grows, the limiter shrinks the echo along with it. D81's fast partial mimicry is then the first casualty.

### 6. The divisive floor (A6)

The pair is a quarter-period lead at amplitude 0.1 each, with white tracker noise of SD 0.005, at the matched scale.

| j | Node length | Mean ρ, ε = ν²2^j (design) | Mean ρ, ε = 2ν² (white-noise floor) |
|---|---|---|---|
| 9 | 17 s | 0.31 | 0.50 |
| 12 | 2.3 min | 0.08 | 0.50 |
| 14 | 9 min | 0.02 | 0.50 |
| 20 | 9.7 h | 0.000 | 0.50 |

**Why.** Tracker jitter is white, so its increment over any span has a fixed SD (ν√2); it does not diffuse. Expressions are bounded, so their increments stop growing past a few seconds. ε ∝ 2^j therefore swamps every slow node.

---

## Side item: can a frozen Cayley-ledger route make a lagged copy that its ledger misses?

Checked against design-cayley-ledger.md (8.3; ledger as in .r7.md §2.13 and .r6.md §2.13), which I did not edit. The script is cayley_ledger_lag.py.

**Answer: no counted Cayley route does this, but the ledger's backstop claim is narrower than stated.**

**Why the counted routes are safe at every lag.** Their bounds are sup-gain bounds, and a sup-gain bound holds at every lag. For such a route, a regression at any lag is at most max|H(ω)|.
- The fast gear: 0 ≤ y ≤ g G_k u(t − δ), with a high-pass onset lobe.
- The held cone: first-order low-passes, so |H| ≤ H(0).
- The appraisal display: band-pass with sup 0.636.

**Measured check of the nonlinear fast gear (K2).** Its best block-mean slope over lags 0–120 s equals its lag-0–3-s value: 0.07, 0.04 and 0.02 at 2 s, 10 s and 60 s.

**Routes the ledger never sees, at any lag.** These are held factual in its shadow, so they are invisible to the ledger whatever their lag. All are declared, with numbers, in Cayley 8.3; none is a lag-specific miss.
- the posture (R40′);
- the draft choice and Ω (R18′);
- the arrival mask (R27′).

**The backstop gap.** The ledger also claims "every uncounted within-session route ≤ c_k". It scans lags 0–3 s at 2 s and only lag 0 at 10 s and 60 s. Here is what it leaves of an uncounted gain-1 delayed copy, by the critics' block-mean metric with lags extended to 0–120 s (ceiling 0.35):

| Delay | Partner with 5-min mood blocks | Livelier partner (30-s blocks) |
|---|---|---|
| 0–2 s | 0.36–0.37 (capped) | 0.34–0.36 |
| 10 s | 0.46 | 0.51 |
| 20 s | 0.50 | 0.48 |
| 40 s | 0.52 | 0.56–0.62 |
| 90 s | 0.58 | **0.96** (the ledger changed 5 % of frames) |

So the backstop holds only for delays up to about 5 s. A lagged route that the type analysis missed, such as a bug or a future addition, would pass at 1.3–2.7 c.

**Plainly:** no concrete failure in 8.3's counted routes. The ledger's "any uncounted route ≤ c_k" should read "any uncounted route with a delay ≲ 5 s". Scanning lags up to ≥ 120 s at the 10-s and 60-s windows would close the gap; the commutator design's lag-complete idea applies there directly.

---

## What a revision would need

1. **Keep calibration off the expressive path.** The echo and the limiter's reference should use his raw, reflected channel, as Cayley rule 6 does; x̃ stays for knowing.
   - If the operator wants ceilings relative to his own range, state that and clip the amplification on expressive paths at ×1 (σ_ref/max(σ_id, σ_ref)), so that no learned per-identity factor can raise a ceiling.
2. **Make S⁰ hold everything his face and voice cause, or count each exception with a bound.**
   - Replace his word-event timing in S⁰ with a tempo-free surrogate, or reinstate T1 (no rate codes from his speech timing in u_j).
   - Either re-score the same drafts with z^{S⁰} and use S⁰'s pick there, or declare R18′ with its bit bound.
   - Keep the posture out of the own side a, and declare its brow numbers against c^tot.
   - Then restate §3.6 and §4 honestly.
3. **Cap slow following.**
   - Add uncentred (block-mean) coherence at windows of 1–30 min with lags up to ≥ 30 min.
   - Alternatively, give the body-route and slow-block display a sup-gain bound on its partner-caused part, as Cayley did for its cone traces.
   - Extend the independent metric the same way, or the checks cannot see the failure.
4. **Cap only what is toward him.**
   - Bias-correct κ for the maximum over N lags, for example by subtracting the noise level expected for N lags and N_eff samples.
   - On the 13 zero channels, limit only content coherent with his same channel, so appraisal-driven movement uncorrelated with it survives.
   - Check the voice and lateral channels at their small c.
5. **Make the limiter attenuate-only in time and protect the echo.**
   - Use one broadband factor per channel, informed by the per-band κ, or Cayley r7's clamp.
   - Cap the non-echo routes first, so the frozen echo keeps its share of c_k (D81).
6. **Use a scale-independent noise floor** (ε = 2ν^aν^x, or one that saturates after a few seconds), so the slow blocks receive the relationship-scale ρ that §3.2 promises.

The core idea, a same-channel commutator from an efference own side for knowing, survives all of this. The failures are in the counterfactual bookkeeping and in the limiter, which is the element the design itself says carries the guarantee (§3.3).
