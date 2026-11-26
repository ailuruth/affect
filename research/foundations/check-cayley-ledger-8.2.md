# Check of the Cayley–ledger revision 8.2 face-only limit

Independent checker, 2026-11-26T17:22:47Z

Standard: questions.md Q19 (concrete failures only), D78 (especially condition 4: copying must never become a state the agent settles into), D81–D85, and Q24 (open; the design follows its recommendation). Scope: the 8.2 face-only limit (T_max 180 s, T_ref 120 s, non-face evidence N = max(C_L, sobs, V_v, breathing) ≥ 0.02), the changed concern-posture text, and the Build-candidate summary.

Checks: `sims/check-cayley82/check.py` (A, B0–B2; `out.txt`) and `check_b.py` (B3, B3b; `out_b.txt`). Both load `sims/design-g82/checks.py`'s definitions (engine, `Agent81`, `Agent82`, `lag_face`) unchanged and skip its L0–L4 loops. The engine takes about 4 min to load, and each set of runs takes about 1.5–5 min. No processes are left running.

## Verdict: FAIL (one medium failure: the limit is bypassed by the answering partner's own voice, and at high levels by his breathing)

The face-only limit does what it says for **face** dynamics. I found no face strategy that beats it. **But the same answering partner holds the look indefinitely once he speaks.** He needs to speak only a few words every few minutes, in a voice about 0.03 softer than his rest. That is ordinary conversational variation, and it is also what his own code produces when he answers the look in voice as well as face. With that, the face-only clock never fills. The look is on 100 % of the time and the agent's inner brow is held at +0.19 to +0.24 in every code: the same mutual concern state that routes critique 8 and the check of 8.1 called D78-condition-4 failures. The author's L1 answerers are mute by construction: `lag_face` strips his voice channels (`NOV`), so his answer "in his own code" leaves out the voice that the 8.2 rule treats as non-face evidence.

## Evidence

### 1. The face-only limit against face dynamics: holds

A (30 min, operator and different-channel codes). The adversarial faces were:
- release-gaming cyclers, keyed to the look, that are sad for D_on s of the look, then rest for D_off s (D_on 30–179 s, D_off 10–125 s);
- a "window answerer" who knows T_ref and is sad only while the look is on or the refractory period has ended;
- random telegraph faces (4 seeds).

| Partner | Posture on, 5–30 min | Longest visible face-only stretch |
|---|---|---|
| cyclers 60/21, 100/21, 170/21, 170/119, 30/10, 179/125 | 60.0 % (visible 62.7–63.8 %) | 188–191.5 s |
| cycler 150/25 (a 20-s release, then a 0.5-s sensitized re-onset) | 60.0 % (visible **64.8–64.9 %**) | **195.5–196.0 s** |
| cycler 100/60 | 48.0 % | 130 s |
| window answerer | 60.0 % (visible 63.8 %) | 191.5 s |
| random telegraph | 39–51 % | 110–191.5 s |

- The posture state never exceeds T_max of face-only hold or 60 % duty, as the construction argues: the clock refills only through non-face evidence or T_ref without the look.
- Text precision only: the visible look can bridge a release and its sensitized re-onset. So the measured visible stretch reaches 196.0 s, against F12's "T_max + 15 s" = 195 s, and the visible duty reaches 64.9 %, against the stated ≤ 0.64. State these on the posture's on-state, or widen the visible margins (T_max + 20 s; ≤ 0.65).

**Is the bounded face-only cycle itself a D78-4 failure?** No. Condition 4 forbids a copy state the agent *settles into*. Here every episode ends by construction at 180 s, and nothing his face does can lengthen it or shorten the 120-s gap. The cycle is a fixed, agent-clocked oscillation with a hard duty ceiling, not an attractor whose basin the partner's dynamics can deepen. Its time-mean (agent BI +0.09 to +0.17) is a bounded level, like the R40′ level row, not a growing or self-sustaining coupling. I accept it as bounded, as long as the face is the only thing answering.

### 2. Non-face channels: genuine distress is kept, but voice and breathing reopen the answering loop

**Genuine distress keeps the look** (the author's L2, re-read). With words, a sad voice, silent-panic breathing or sobs, the look has one onset and is never withdrawn in 30 min in every code. Confirmed.

**B3: a speaking answerer** (out_b.txt). His face is the check of 8.1's C1b partner (μ 1.0, τ 300 s, carried on), which 8.2 cycles at 60 %. He also speaks for 4 s every P s with no distress words, his voice at rest except that its energy EN is lowered by d.

| Code | V_v at EN −0.02 / −0.03 / −0.05 | d = 0 (control) | d = 0.03, every 80 s | d = 0.05, every 80 s | d = 0.03, every 120 s |
|---|---|---|---|---|---|
| operator | 0.016 / 0.023 / 0.039 | 60 %, 6 withdrawals | **100 %, 0 withdrawals**, BI +0.236 | 100 %, BI +0.236 | **100 %**, BI +0.236 |
| quiet 0.3 | **0.052** / 0.078 / 0.130 | 60 % | **100 %**, BI +0.200 | 100 % | 100 % |
| different channels | 0.020 / 0.030 / 0.051 | 36 % | **100 %**, BI +0.190 | 100 % | 100 % |

- **Control B3b:** the same soft voice with a neutral face releases normally at the 20-s rule. So it is the combination, an answering face plus any slightly soft speech, that holds the look indefinitely.
- **Why it holds.** V_v is averaged over the last 90 s, is not gated by anything, and counts as present at 0.02. One soft utterance keeps N present for 90 s. A gap then needs another 180 s to fill the clock, so speaking once every 4 minutes or so is enough.
- **The threshold is ordinary speech variation.** EN −0.03 sits inside ordinary variation and is below his own V 0.3 sadness voice (EN −0.045 operator). For a quiet code, EN −0.02 already reads 0.052, because V_v is scaled by his small calibration spread.
- **This is the D78-4 mutual state again, not genuine-distress evidence.** A partner who answers the look in his own code answers in his voice too whenever he speaks (`pp.code(V)` lowers FR and EN). The 8.2 design itself concedes that the limit "does not tell answering from genuine sadness; it bounds both the same way". For any partner who speaks, it now bounds neither.
- **A literal copy path is also plausible.** The agent's concerned voice is quieter: design-g8 scenario 1 has EN −0.05/−0.08 after his words. Vocal accommodation at about half gain gives his EN about −0.03, which is enough. In a fully silent episode the agent's own voice is unchanged (B0: 0.000 on FR, EN, RT and LAT), so this copy path needs a spoken exchange; I did not close that loop in simulation.

**B1: an answering breather.** His breathing BR = β × low-pass(look, 30 s), on the same answering face:
- β 0.5: 60 % (no change);
- **β 0.7 and 0.9: 100 %, never withdrawn, BI +0.19 to +0.24**, in both codes.

The breathing term reaches presence once his breathing passes about 0.52 of the constructed silent-panic level, with his non-brow face distressed. This is narrower than the voice route: strong, sustained breathing in answer to a look is real physiological arousal, and no agent channel is copied. But it bypasses the "whatever his face does" bound in the same way and should be stated.

**B2: voice accommodation to the agent's own voice in a silent episode.** No effect, because the agent's voice does not move there (B0). The voice route above does not depend on this.

**Possible fixes (not checked here):**
- Let only decoded words (C_L) and sobs reset the face-only clock.
- Let voice and breathing only *extend* T_max (for example to 10 min), not reset it.
- Or require V_v to exceed a distress-level threshold (≥ 0.05) on fresh speech, not a 90-s mean, and accept the stated cost to sad-voiced or panicking users.
- Then re-run L1 with his answer in his full code, voice included, and speech every 1–4 min.

### 3. Nothing else broken

- **Totals.** R1g (≤ 0.31 c LP, ≤ 0.35 c CR, ≤ 0.53 c BU_L) agrees across §0 move 6, the bound table, §3.3 and §3.11. 8.2 touches no fast or gated route.
- **The squint fix** is copied into `Agent82.step` unchanged (SQ_CH = BL, LPR). Its anger side effect is now stated in §2.10 and in the summary.
- **Laugh timing.** δ_g = min(1.0, ℓ_p90 + 0.25), the finalised-through requirement, the 0.75-s fallback threshold and the summary's 0.8–1.0 s are mutually consistent.
- **Stale text (minor):**
  - §2.15's closing sentence still lists "a contingency test" among the innate parts.
  - §3.14 scenario 1 says "three probes held" (annotated, but reads as current).

### 4. Build-candidate summary: accurate for a silent partner; corrections needed

**Present and accurate:**
- the one-line description;
- what the operator gets (laughter, echo timing 0.8–1.0 s against a person's 0.4–0.5 s, the look within 2–7 s);
- the brow-only trade-off (bid at about 50 s, about 110 s for a quiet face);
- the silent-sadness cost (3 min on, 2 min off, 60 %, about 22 min off per hour);
- the half look and the anger side effect;
- novelty: recombination;
- the Q24 options and the other remaining choices, one line each;
- a risks list.

**Corrections:**
1. "So whatever his face does, including answering the agent's own look, it is on at most 3 of every 5 minutes (60 %)", and "a person whose face keeps answering it gets it in 3-min pieces", hold only for a **silent** partner. Add: "A person who answers the look and speaks, even a few words every few minutes in a voice slightly softer than usual, or whose breathing answers it strongly, keeps it indefinitely." The alternative is to fix the mechanism.
2. Add to the risks:
   - the V_v presence threshold against ordinary voice variation (EN −0.02 to −0.03; a quiet face's voice reads 0.05 at EN −0.02);
   - how often the limit is bypassed by voice or breathing in real sessions;
   - vocal accommodation to the agent's quieter concerned voice.
3. Add the stated 8.2 cost that one reply's words keep the look for about 21 min (C_L above presence).
4. Optional precision: the visible look is on up to 64–65 % of the time (the posture state 60 %), and can bridge a release for up to about 196 s.
