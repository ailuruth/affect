# Review of the build specification (research/build/spec.md)

Independent reviewer, 2026-11-26T21:54:00Z. I did not write the spec. Read: spec.md (all 567 lines); design-cayley-ledger.md at revision 9.2 (the audit table and its "No allowed source" list, §2.9, §2.13, §8, Revision 9 and 9.1 histories, Check of 9.1 and the answer, Build core summary), plus r3/r6/r7/r8.3 where the spec inherits text; the reference ledger (`sims/design-g7/checks.py` `ledger7`, `sims/design-g9/ledger_lag120.py`, `sims/check-cayley91/ledger_close.py` and its `k070_w10_*` outputs); questions.md Q19–Q34 and Report 10; DECISIONS.md D70, D78, D80–D91; brief.md; research/machine.md. Nothing was run, downloaded or committed.

## Verdict: NOT READY (narrow fixes; M0 can start in parallel)

The spec follows revision 9.2 closely. The modules, ceilings and ledger match the design: 97 keys, κ 0.70, attenuate-only, the 0.45-s echo, and the isolation of Claude Code. The milestone layout is good. The concrete problems are elsewhere:
- some safety invariants are wrong (one is vacuous, two will fire on behaviour the design allows), and the fail-safe does nothing for T-route failures;
- one falsifier (F19) fails by construction;
- several restated or inherited falsifiers demand situational outcomes that 9.2 gave up on purpose, which brings D88 rules back as pass criteria;
- the label lint can be bypassed with ordinary snake_case or a plural;
- a few off-Mac and usage questions are missing or put to the operator inconsistently.

None of these needs a new mechanism. Issues 1–6 must be fixed before M4. M0 can begin now if it takes the fixes to A3, A14, A15 and the lint (issues 2, 3, 5, 7).

## Issues, ranked

### 1. F19 fails by construction (high; criterion 4)
F19: "any T quantity other than Λ_V(own) in g and g_o changes when only Claude's reply text is changed". Under the spec's own interfaces, at least three other T quantities read the agent's reply text:
- **q̂** reads "the agent's last turn (through Λ's encoder)" (§1.5.5; audit S17, "the last two turns"). It drives the own laugh, the relief of P, and q_trace in g and g_o.
- **p̂_end and h(t)** read "last turn ended in a question and whose" (§1.5.6; M1). The phrase template also follows the text's question form (§1.7).
- **P_name** attenuates T loads from the agent's own words (S49; r3 §2.10.4).

The reply's length also moves the `agent_utterance_end` events. The swap test of §5.3 will therefore fail on correct code. **Fix:** restate F19 as "no T quantity changes except through the declared Ω→T ports: Λ_V(own) in g and g_o; q̂'s and the turn model's agent-turn inputs; P_name (≤ 0.05); agent turn-event times". Test each port by lesion, and require every other T field to be bit-identical.

### 2. The runtime invariants: one vacuous, two that misfire, and a fail-safe that misses T routes (high; criterion 4)
- **A5 / F1′ is vacuous as written.** §1.6 says the shadow is "held at factual values: T values, …", which means they are copied. A5 then compares a copy with its source, so an F→T leak can never be seen. Rule 10 (r6 §2.1, "every T value must equal its factual value", a dynamic type check) needs the shadow to **compute** its T state from its own inputs. Only g, D_τ, Ω values and the agent's noise are held. Fix the §1.6 sentence. A5 then means something, and "whole output falls back to ȳ" is safe, because the shadow's independently computed T state is the clean one.
- **A3 will fire on allowed behaviour.** "Rendered − shadow = 0 on the 13 zero-ceiling channels" ignores what the spec itself allows: zero-ceiling cone rows may have diagonal ≤ 0; the appraisal's cross entries are away-orthant; S31 says the away magnitudes on BL and LT are learnable. Away partner-caused parts are nonzero, and the ledger (which bounds toward slope only) lets them through. **Fix:** A3 = the in-phase toward slope (the ledger's S⁺) on zero-ceiling channels is 0, plus no toward cone or appraisal entries.
- **A14 will fire on correct dynamics.** "Σ drops within a session ≤ 𝒟(session start)" is false whenever 𝒟 rises during the session: hurt latches, E decays, P rises. An insult that then decays already breaks it. **Fix:** Σ drops ≤ 𝒟(start) + Σ rises (rises counted from the drive dynamics), plus every drive in [0, 1] and 𝒟 ≥ 0.
- **The single fail-safe (render ȳ_k) does nothing for T-route failures.** A2 on g_o, A7, A8, A9 and A14 concern T routes (L_d, the own laugh, free display, prosody, body), which are identical in ȳ. Falling back to ȳ_k still renders the faulty L_d or laugh. **Fix:** one fail-safe per assertion:
  - for a T-route failure, set that route to its context-free constant, or 0 (the §3.2 "disabled part" state), for the session;
  - for A9, mute speech or use neutral prosody, and gate the laugh synth to 0;
  - for A14, freeze the body at its last valid state and stop learning.
- **Smaller points:**
  - §1.6 writes the bound as "S⁻ ≤ κ c_k E". The reference bounds the positive (toward) part, `Sm = max(0, S)`. Write S⁺, or give the exact formula from `ledger7`.
  - Say whether ledger budgets persist across sessions or reset.
  - Add a page-side watchdog: neutral rest face and mute if no RenderFrame arrives for more than about 200 ms. "The fast loop never stops" says nothing about an engine crash.
  - Principle 7 is enforced only by the store schema (A12). Nothing at runtime stops a library in `engine`, `asr` or `tts` from opening a socket. Add a check at start (e.g. a macOS `sandbox-exec` profile that denies network to those processes, with only the Claude Code subprocesses allowed out), and set `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1` (see issue 6).

### 3. Falsifiers that reinstate situational rules as pass criteria (high; criterion 2, D88)
Revision 9.2 gives up guaranteed situational silences on purpose. Their strength is now the corpus listeners' (S14, S19, S22: "the strength is the corpus's, not 0"; "No allowed source" items 2 and 4). Zero-tolerance falsifiers over hand-picked situations either fail the correct mechanism or invite re-adding rules. In detail:
- **F6 (restated)** contains "or speaks more than once per lapse without his reply". That is the removed S34 rule ("one per lapse") brought back. It contradicts M1: the agent now asks again after an unanswered question when recorded speakers do. The other clause (lesion β = 0 leaves initiative timing unchanged) is scheduled at M7, but on day 1 𝓜 is untrained, so ΔĴ ≈ 0 and the lesion is vacuous. **Fix:** drop the once-per-lapse clause. Make the 𝒟_p clause a dose–response steering test on 𝒟_p at M8 or later, with 𝓜 trained. Compare repeat-bid timing with held-out recorded speakers (h(t) calibration, already in F24).
- **F9 (restated)**: "at his words of loss, the cheek raise or the drop envelope rises within 2 s". This is a situational target, and the mechanism is not built to meet it:
  - g_o attenuates to the corpus level, not to 0;
  - K_id falls continuously while he is present (S26), so drop events and env_drop run through any early-session utterance, whatever the words.

  **Fix:** a relative test. The drop and own-smile output × g_o after such words is lower than after other utterances by at least the held-out listeners' contrast, and g_o's attenuation is not removed. Or retire F9 as F12 was.
- **F10** ("any laugh-synth output within 2 s of his BU_S bursts") was protected in r6/r7 by the play laugh × g, which reads sobs. In 9.2 the own laugh is 0.40 q̂ g_o, and g_o reads **no** channel of his (rule 13′), so nothing in the mechanism ties the own laugh to his sobs. Either state that F10 now tests only the fast echo (BU_L after the burst split) and restate the own-laugh part relative to recorded listeners, or accept that it can fail by design.
- **F15 (live clause)**: "within 2 s of his laugh following words of loss…". **F20**: "> 0.6 s after…". Both contradict "No allowed source" item 4, the accepted 0.2–0.5-s partial echo before the word is delivered. Kyutai's word-end-to-delivery is 0.6–0.75 s, the echo plays at +0.45 s, and g stays above 0 after delivery. **Fix:** make them relative to the corpus: the agent's return ratio at such laughs is not above held-out listeners' return ratio at the same events, and the delay to closing is within the measured recogniser latency plus one gate evaluation.
- **F13 (restated)**: "own laugh fires on > 5 % of held-out utterances whose listeners did not laugh, relative to q̂'s calibration". "Fires" is undefined. The own laugh is a continuous 0.40 q̂ g_o and sounds whenever its BU_L share clears θ_L = 0.04. That is roughly q̂ g_o > 0.25, which will hold on well over 5 % of non-laugh utterances for any calibrated q̂ with a realistic base rate. **Fix:** a calibration statement (reliability curve of q̂; expected own-laugh amplitude on non-laugh utterances ≤ the calibrated expectation). That is F24 for q̂, so fold F13 into F24.
- **The event categories behind these tests** ("words of loss, insult or harm", "troubles, mockery and misfortune laughs", "words of need") have no defined instrument: a word list, human annotation, or the listener's masked face as in F15/F16. Define each one in `eval/`. Add an import test that `engine/` never imports `eval/`. Move the §3.1 event counters out of `engine/dyads/events.py` into `eval/`, so no situational detector lives in the engine package.
- **F21** (r8.3: onset-aligned versus whole-segment gate fit) has dropped out without a note. It belonged to the removed S10–S12 timing. List it as deleted, as F12 is.

### 4. Thresholds and timings: generic or situational (medium; criterion 2)
Every value the spec sets was checked. None names a situation. A few are hand-set decision or engineering constants that fit none of A15's categories {body, reflex, newborn, ceiling, bias, operator}, so A15 as written fails at M0 or forces a wrong label.

| Value | Where | Verdict |
|---|---|---|
| p̂_end ≥ 0.5 (draft hand-off) | §1.5.6, new in the spec | **generic** (every turn alike); but hand-set, and 0.5 is optimal only under symmetric costs. The design says only "at the predicted turn end". Choose it on val (e.g. matching held-out listeners' response-latency distribution, or minimising false starts × fork-churn cost), or tag it. Also cost the churn: each false start kills and respawns 3 forks, which uses usage |
| β = 4, "now vs in 5 s" | §1.5.6 (design: "a general decision constant") | generic; needs a tag |
| deadline 0.5 s after first sentence / 3.0 s; 2 sentences or 60 words; +0.35 s onset; pauses 0.20/0.40 s | §1.8, §1.7 | generic (S50 body; Ω engineering) |
| pool shrink at p90 > 3.0 s over 20 turns, 30 min | §1.8 | resource engineering, not behaviour |
| marker "[no reply … 25 s]", rounded to 5 s | §1.8 | observable text; generic |
| g knots 0.05–0.80; m_ref 90th pct; q̂ target ≥ 0.25 with 3–7 Hz JawDrop; sign-prior \|ρ\| ≥ 0.2 | §1.5.4, §3.2 | fit definitions, generic |
| S38 thresholds (word care < 0.05, V̂ > 0.20) | §1.3 (by reference) | kept by the audit as a bias; generic |
| F-test tolerances (5 %, 0.6 s, 10 %, 1 %, 2 s) | §5.1 | test tolerances; fine where the criterion is generic (F1, F22). Situational where they encode a situational outcome (issue 3) |
| lesion predictions "κ → 1: 1.03–1.20 c" and "lags 0–3 s: 1.3–2.9 c" | §5.2 | measured with the 61-key κ = 1 ledger and the 8.3 ledger, not with the lesioned 97-key κ 0.70 ledger. Re-derive before the run (Principle 5) |

**Fix:** add categories `decision` and `engineering` to A15 (or give each such constant a justification), and record p̂_end's 0.5 as chosen on val. §3.3's promise that a unit test fails if an innate constant "names a situation" has no stated method. Specify it: a reviewed allowlist of constant names, plus a forbidden situation-word list (arrival, mourning, grief, joke, bad-news, greeting, …) applied to INNATE.lock keys and comments.

### 5. The label lint can be bypassed (medium; criterion 3)
§7.4 matches whole words with word boundaries. In regex, `_` is a word character, so `is_sad`, `fear_level` or `joy_gain` contain no word boundary and **pass**. camelCase (`isHappy`) passes. Plurals pass (`emotions`, `fears`, `moods`, `concerns`). So would a model id such as `…/roberta-base-go_emotions`.

The list also lacks design-adjacent words: distress, relief, hurt, glad, surprise, love, hate, lonely, bored, upset, frustrat-, nervous, scared, calm, excite-, sentiment, valence, arousal. The design names that read as affect words in code positions are distress, relief, hurt, glad-with and care. `tools/` is not scanned.

**Fix:**
- split identifiers and literals into tokens on `_`, case changes and digits, and match stems (emotion*, happi*, sad, sadness, griev*/grief, ang(e)r*, fear*, worr*, mood*, …), with an explicit exemption list;
- scan `tools/` as well;
- add a **model allowlist by SHA-256** at load (FaceLandmarker, Kyutai, Whisper-small, MiniLM, TTS voice). The import denylist misses `transformers.pipeline("sentiment-analysis")`, because transformers is a dependency of sentence-transformers.

Give glad-with its neutral code name (e.g. `basis_return_LP_CR`). The rest of §7.4 is adequate: the identifier mapping, the A12/A13 schemas and the denylist exemption.

### 6. Off-Mac flows and usage: missing or inconsistent (medium; criterion 6, D70, Q34)
The spec flags conversation text to Anthropic, Claude Code telemetry and the call volume, and decides none of them. Missing:
- **Account data-use setting.** Depending on the operator's Claude account privacy setting, his transcribed words and past snippets sent through Claude Code may be used by Anthropic for model training. That is his decision. Add it to M6 and to Q34 item 1.
- **Paid overage.** "Not a new paid service" holds only if extra or overage usage billing on the subscription is off or capped. Ask him to confirm. Q34 item 2 promises "a daily cap you can set", but no such switch exists in §7.3. Add `claude_daily_cap`.
- **Usage counted in calls, not tokens.** Each of the 3 forks resumes the **whole** canonical transcript, so usage grows with transcript length. The spec never says how long the canonical transcript gets (per session? across days?) or what happens near the context limit. Claude Code auto-compaction would rewrite history and break A11's byte identity. **Fix:** a transcript window policy (e.g. per-session canonical transcript, earlier days only through ≤ 3 snippets), auto-compaction disabled or detected and treated as an A11 event, and the usage estimate in tokens per day.
- **Runtime hub calls.** sentence-transformers, mlx-whisper and the Kyutai MLX runtime contact huggingface.co at load when given repo ids. No user data goes out, but these are outbound calls. Require local paths plus `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1`. Claude Code's auto-updater also calls out; set `DISABLE_AUTOUPDATER` alongside the M6 telemetry question. Mention browser telemetry (use a dedicated profile) when the browser is asked about at M2.
- **Inconsistencies between Q34 and the spec:**
  - Q34 item 5 tells the operator that with a slower recogniser "the quick laugh back waits longer". Under 9.2 the echo never waits (S10 removed); the consequence is a **longer partial echo** at a bad-news laugh (spec §1.2.6 says this correctly). Correct Q34.
  - Q34 item 6 recommends "30 days, then only what replay consolidated". Spec §1.9 and §8 item 12 keep a 2-Hz decimation indefinitely and keep transcripts forever, and the snippets sent to Anthropic come from those transcripts. Make them agree, and ask about transcript retention explicitly.
  - Q34 item 1's option "allow without past snippets" and item 4's option "models only, no dyad fit" have no switch. Add `send_snippets` and `dyad_fit_enabled`, and say what runs without the fit: §3.2 already gives context-free constants for disabled parts.
- CI: if it runs on GitHub Actions, code and synthetic arrays leave the Mac. That is fine, but say so, and keep CI free of any recorded or operator data.

### 7. F22 and F1 on recorded partners cover only 6 of the 20 capped channels (medium; criterion 4)
Seamless FAUValue maps only onto LP, CR, BI, BO, LD and JO; the 18 face channels include 12 zero-ceiling ones. The 3 laugh-sound, 5 head–gaze and 6 voice channels are "held at baseline" (§5). On those channels F22's injected copy is 0, so the M4 gate for M7 does not test them. **Fix:** at M4 also run F22 and F1 on the operator's own M2 feature recordings (all 33 channels; features only, already approved for storage), and keep F22 live at M7 for all non-zero channels.

Also:
- **Bit-exact regression first.** The regression numbers (0.83–0.88 c, 0 frames) were measured at **fs = 10 Hz** (`ledger_lag120.py`: `fs = 10.0`). M4's "reproduces … at 30 Hz" is untested. First reproduce at 10 Hz against `ledger7`/`ledger9` bit for bit, then at 30 Hz with a stated tolerance.
- **The F22 delays are now set.** At 9.2's 97 keys the checker measured delays 150–300 s and 10 and 90 s. 20, 40, 60 and 120 s were not run at 97 keys. F22 covers them; good.
- **Check the data exists.** "≥ 50 test people with ≥ 2 h each": count this on the downloaded subset at M3 before relying on it.

### 8. Compute and run-time budgets for evaluation and the fast loop (medium; criterion 5)
- **F22 run time.** 12 delays × 50 people × 2 h × 216,000 frames × about 1 ms (ledger only, injected after assembly) ≈ **36 CPU-hours**. machine.md requires asking before runs over about 6 h. Budget it, parallelise across performance cores (about 4–5 h on 8 cores), or put it to the operator. The same applies to the E1 lesions (≥ 20 seeds each) and to F1's surrogates if any re-run the engine.
- **The GIL.** Python 3.12 keeps the GIL. The fast thread (30 Hz, p99 ≤ 5 ms) shares it with the slow thread (torch 𝓜 steps), the asyncio I/O thread (websocket decoding of 30-Hz face frames and 50-Hz PCM) and the Ω manager parsing 3–4 SDK streams; voice features (pyworld) are also in-process. The 0.36 s of slack in the echo ring buffer protects the echo lag, but missed ticks repeat frames. **Recommend:** put voice features in their own process (like ASR), measure fast-tick p99 under full load at M1, and run the online 𝓜 on CPU rather than MPS (tiny kernels, sync overhead, contention with MLX on the GPU). The shadow "in the same thread" also conflicts with the fast/slow split for slow-loop quantities; say that the slow-loop shadow runs in the slow thread.
- **Memory.** The total ≤ 5.8 GB against the 6-GB plan is plausible: Kyutai 1B at 8-bit is about 1 GB, Whisper-small about 0.5 GB, Claude Code CLI 0.2–0.4 GB each, Chrome with two trackers 0.5–1 GB. The margin is 0.2 GB. The fallback order (4-bit, then fewer forks) is right.
- **The model choices are realistic.** Kyutai stt-1b-en_fr has an MLX runtime; mlx-whisper; MediaPipe 0.10.35 at 13 ms; Piper, with GPL-3.0 flagged at Q1. pyworld needs a C toolchain on macOS (Xcode command line tools); add that to M0/M1.
- **Browser clock.** `requestVideoFrameCallback`'s `captureTime` is not reliably available for local getUserMedia streams in Safari. Add a fallback timestamp (e.g. `expectedDisplayTime` minus the measured offset), and re-map the clock periodically, not only at connect.
- **Echo measurement.** The capture-to-photon done-check (0.45 ± 0.035 s) needs a stated rig, such as a 240-fps phone video of an LED or screen flash in front of the camera and the avatar on screen, or a photodiode. "Scripted input" does not say how light gets into the camera.

### 9. M0 and M1: concrete, with gaps (medium; criterion 7)
- **M0 is nearly codable now.** The channel table checks out: Σ c_k = 2.44, A0 holds on every row (max 0.974 on LP), r_k = 0.95 G_k/c_k. To start:
  - **INNATE.lock contents.** Many body and reflex constants are cited by reference only (r5 §2.8 for I_lp; r3 §2.11, r5 §2.1 and r6 §2.1 for others). Before INNATE.lock can be "complete", list every innate constant in one table in `config/innate.py` with its value, source section and A15 category, including the new categories from issue 4. Define the canonical serialisation behind the SHA-256 (sorted JSON with float `repr`).
  - **Type wrapper API.** Give a minimal API for the provenance wrapper (§4.4): a numpy subclass carrying a tag set, propagated through ufuncs and `__array_function__`. Define A15's static check ("no counter, accumulator or event rate is a T field") as a concrete AST rule.
  - **Dependencies.** `mlx`, `mlx-whisper` and the Kyutai MLX runtime are macOS-only, and `uv lock` needs index access, which this cloud session should not use (D90). Put them in a `mac` extra with platform markers; M0 core is numpy, scipy and pytest only. Generate `uv.lock` on the Mac at M1. Allow Python ≥ 3.12, < 3.14 (this environment has 3.13).
- **M1 is a good list.** Its scripts can be written now but run only on the Mac after the Ask. Missing: the branch thresholds for several checks.
  - What recogniser latency, coverage or RTF selects the fallback (only "RTF < 0.5" is given)?
  - What breathing-separation result turns breathing off (cite design §3.17 item 15's criterion)?
  - What camera-to-photon or tracking p99 fails M1?
  - What memory total triggers each step of the §2.4 fallback?

  Add a pass or branch value to every row so week0.md is mechanical.

### 10. Minor
- §1.6 "Lag buffers" store the 2-s window for 300 s (only 3 s needed). That is harmless.
- The F-table mapping is otherwise complete. F1–F24 are mapped; F12 is deleted; F21 needs a deletion note (issue 3).
- §5.2's "learned turn-taking → fixed 6-s rule" lesion uses a removed situational timer (S34) as the comparison arm. That is acceptable as a lesion control, but say so.
- The spec's §0 diagram puts "SHADOW · LEDGER" in the fast loop, while §1.6's shadow also needs slow-loop quantities. See issue 8.

## Criterion-by-criterion

1. **Faithful to 9.2: yes.** Correct: every module of the Build core summary is present; the ceilings c_k, G_k and shares; the ledger with 2-s lags 0–3 s, 10-s and 60-s windows both to 300 s, 5 + 61 + 31 = 97 keys, κ 0.70, the 0.10 RMS floor, b < 0 recovery, attenuate-only (matches `ledger7` and the 97-key `ledger_close.py w10`); the 0.45-s echo on every channel (S10 removed); L_d with BI, BO, LD, LP, CR and RT only, with TILT, HP, VG, FR and EN held at 0; no rule J; M1 removed; S45's +0.45 brow (Q33 switch); S46 (Q31 switch); Claude through the subscription with `setting_sources=[]`, no tools, a typed prompt builder, and no state, labels or numbers. Exceptions: the A5/rule-10 wording (issue 2) and the S⁻/S⁺ notation.
2. **No situation-specific rule in the mechanism: yes. In the falsifiers: no** (issue 3). The hand-set generic constants need tags (issue 4).
3. **No labels below Claude: yes in design.** The lint is inadequate (issue 5).
4. **Invariants and tests: no.** A3, A5 and A14 are wrong, the fail-safe misses T routes, and F19 fails by construction (issues 1–2). Tests are judged on internal state (E1 lesions with shams, E2 steering on the engine's own state, E3 with both surrogates). F22 covers 10–300 s but only 6 channels on recorded data (issue 7).
5. **Buildable on an M1 Pro with 16 GB: yes, with risks** (GIL, F22 compute, the echo measurement rig; issue 8).
6. **Off-Mac flows: mostly.** Missing: the training-use setting, paid overage, the token volume, hub calls. Q34 is inconsistent with the spec (issue 6).
7. **M0/M1 concrete: M0 yes with fixes; M1 needs branch thresholds** (issue 9).
