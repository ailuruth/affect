# Build specification: the Cayley–ledger build core (revision 9.2) on the operator's Mac

Written 2026-11-26 under D90 ("building means writing the build specification and code in this repository to run on the operator's Mac; no downloads, datasets or experiments in this cloud session"). This file specifies; it builds nothing, downloads nothing and runs nothing.

**Spec revision 2 (2026-11-26), after research/build/review-spec.md (verdict NOT READY).** Every issue of the review is closed in the text below; the section "Changes after review" at the end lists each one and where. No situation-specific rule is added (D88): every new value names no situation, scene, user type or event, and each is tagged in INNATE.lock (§3.3, A15).

**What is built.** research/foundations/design-cayley-ledger.md at **revision 9.2**: the "Revision 9 (build core): audit" section and §0–§8 as corrected by "Revision 9.1 history" and "Check of revision 9.1 and the answer", plus the "Build core summary". Where the mechanism text still says "lags to 120 s at the 10-s window", "61 constraints" or "≤ 1.02 c at 240 s", 9.2 supersedes it: **the 10-s and the 60-s windows are both scanned to 300 s, 97 constraints per channel, κ = 0.70** (Check of 9.1, "The answer"). Parts the design inherits by reference ("as revision 7/6/5/3") are taken from `design-cayley-ledger.r7.md`, `.r6.md`, `.r5.md`, `.r3.md`, `.r2.md` and cited as r7 §x etc.; "design §x" means the current file.

**Binding.** brief.md Principles 1–10; D70 (Seamless: FAUValue streams and transcripts only, emotion fields never read), D78, D80–D91. Operator notes Q22, Q23, Q26, Q27, Q29. Open questions, built on their recommendations until answered: **Q30** (not widened: D70 as it stands, no head, gaze or audio from dyads), **Q31** (own-display mask kept), **Q32** (losses accepted; nothing hand-written comes back), **Q33** (the newborn own-distress brow at his words of need kept). Each is a switch in `engine/config/operator.py` (§7.3) so an answer changes one value, never the mechanism.

**Words used.** "He" is the partner (the operator, or anyone in front of the camera). "Channel k" is one of the 33 counterpart channels (§1.1). "Partner-caused part" is factual output minus shadow output (design §2.13). A "route" is a path from his signals to the agent's outputs (design §3.11). Design names such as "relief", "hurt" or "concern" are used in this prose only to point at design text; the code uses the neutral identifiers of §7.4.

---

## 0. Architecture in one page

```
 Browser page (localhost only, CSP connect-src 'self')            Engine processes (network denied by sandbox, §7.5)
 ┌───────────────────────────────────────────────┐  ws /face       ┌──────────────────────────────────────────────────────────┐
 │ camera 30 Hz ─► FaceLandmarker 0.10.35 (his)   │ ─ features ───► │ `fast` process, 30 Hz: 𝓑 face framing · fast gear · cone │
 │ rendered face ─► FaceLandmarker (own, 10 Hz)  │ ─ own feats ──► │  · appraisal interp. · assembly · fast SHADOW · LEDGER   │
 │ three.js placeholder face ◄───────────────────│ ◄ RenderFrame ─ │  · fast asserts   (numpy only; no torch, no asyncio)     │
 │ watchdog: rest face + mute if no frame 200 ms │                 └───────▲ shared memory (seqlock double buffers) ▼────────┘
 │ mic 16 kHz (AEC on) ──────────────────────────│ ─ ws /audio ──► `voice` process: voice features, burst split, breath ─► fast
 │ audio out (TTS PCM, laugh synth) ◄────────────│ ◄ PCM ───────── `tts` process (TTS → WORLD; laugh synth) ──► OwnHeard (Ω)
 └───────────────────────────────────────────────┘                 `slow` process, 2 Hz: T/F/𝒦 state · body · gates · L_d · q̂
                                                                     · turn-taking · initiative · 𝓜 (CPU) · slow SHADOW · slow asserts
       `asr` process (Kyutai STT 1B incremental + utterance recogniser) ◄── PCM from `voice`
       `omega` process (outside the sandbox): warm pool of 3 Claude Code forks (Agent SDK, subscription) ◄── unix socket ── `slow`
       Store (features only, memory-mapped) ──► nightly `replay` process (MPS) ──► per-person weights
       Offline, once before day 1: `dyadfit` on Seamless (FAUValue + transcripts) ──► frozen dyad-learned parts
```

Nothing except the `omega` process may reach the network; the others run under a deny-network sandbox (§7.5, A16) and load models from local paths only (offline after the first download, Q34 item 10). The `omega` process sends text (§1.8) to Anthropic through the operator's Claude Code login (D84). The fast loop is its own process so it shares no interpreter lock with torch, websocket decoding, voice analysis or the Claude stream parsing (review issue 8; §2.1).

---

## 1. Modules: responsibilities and exact interfaces

Conventions. Time `t` in seconds (float64, monotonic clock of the engine, with the browser's capture clock mapped onto it at connect). Channels are normalised to their innate nominal range, [0, 1] one-sided or [−1, 1] signed (r5 §2.1). Arrays are `float32` unless stated; `[n]` is a vector of length n; `(a, b)` a matrix. "30 Hz" means the camera frame clock; "2 Hz" the slow clock (ticks at t = 0.5 n); "10 Hz" the breathing and own-face clock.

### 1.1 The channel table (innate; `engine/config/channels.py`)

The 33 counterpart channels, their order (the index used by every array of shape `[33]`), ceilings c_k, frozen fast gains G_k and pooled shares are revision 6's (r6 §2.1), unchanged by revisions 7–9.2.

| idx | code | group | sign | c_k | G_k | (s_C, s_X, s_A) | r_k |
|---|---|---|---|---|---|---|---|
| 0 | LP lip-corner pull | smile–laugh | one-sided | 0.35 | 0.224 | (0.22, 0.05, 0.12) | 0.608 |
| 1 | CR cheek raise | smile–laugh | one-sided | 0.25 | 0.150 | (0.24, 0.05, 0.12) | 0.569 |
| 2 | BU_L modulated burst energy | smile–laugh | one-sided | 0.35 | 0.280 | (0.10, 0.02, 0.10) | 0.759 |
| 3 | RHY 4–6 Hz burst rhythm | smile–laugh | one-sided | 0.30 | 0.240 | (0.10, 0.02, 0.10) | 0.759 |
| 4 | BRE breathiness | smile–laugh | one-sided | 0.15 | 0.120 | (0.10, 0.02, 0.10) | 0.759 |
| 5 | BI inner brow raise | brow | one-sided | 0.20 | 0.020 | (0.68, 0.10, 0.05) | 0.095 |
| 6 | BO outer brow raise | brow | one-sided | 0.10 | 0.024 | (0.44, 0.12, 0.20) | 0.228 |
| 7 | LD lip-corner depressor | brow | one-sided | 0.05 | 0.012 | (0.44, 0.12, 0.20) | 0.228 |
| 8 | JO jaw open | brow | one-sided | 0.10 | 0.024 | (0.44, 0.12, 0.20) | 0.228 |
| 9 | HP head pitch | head–gaze | signed | 0.10 | 0.080 | (0.50, 0.20, 0.35) | 0 |
| 10 | VG vertical gaze | head–gaze | signed | 0.05 | 0.040 | (0.50, 0.20, 0.35) | 0 |
| 11 | YAW head yaw (reflected) | head–gaze | signed | 0.03 | 0.024 | (0.50, 0.20, 0.35) | 0 |
| 12 | TILT head roll (reflected) | head–gaze | signed | 0.03 | 0.024 | (0.50, 0.20, 0.35) | 0 |
| 13 | HG horizontal gaze (reflected) | head–gaze | signed | 0.03 | 0.024 | (0.50, 0.20, 0.35) | 0 |
| 14–19 | F0 level 0.05, FR F0 range 0.10, EN energy 0.05, RT rate 0.05, PAU pause 0.05, LAT latency 0.05 | voice (phrase) | signed | as listed | 0.80 c_k, within-phrase contour only | (0.50, 0.20, 0.35) | 0 |
| 20–32 | BL, UL, LT, NW, LS, CHR, LPR, DIM, FUN, PUK, MCL, LRO, BU_S | zero ceiling | — | **0** | **0** | none toward | — |

- Σ c_k = 2.44; 13 zero-ceiling channels. Group names are muscle and signal groups, not affect names.
- Pooled total per channel s_C(1 + ρ) + s_X + 0.636 s_A + r_k ≤ 0.974 c_k, ρ = 0.091 (r6 J3). **Checked at import** (§4.3, A0).
- The table is a frozen dataclass; its SHA-256 is recorded in `engine/config/INNATE.lock` and checked at every start (A10).

### 1.2 Perception: the boundary 𝓑 (`engine/boundary/`)

𝓑 is the only code that touches camera, microphone or recogniser output (r2 §2.2, r5 §2.2). It emits typed streams; everything downstream reads only these.

**1.2.1 Face tracker (browser, `web/`).** `@mediapipe/tasks-vision` **0.10.35**, vendored with its wasm and `face_landmarker.task` (3.8 MB) and served from localhost; CSP `connect-src 'self' ws://127.0.0.1:<port>` (Q3 default; versions ≥ 1.0.0 post telemetry; research/mediapipe-face-landmarker.md). CPU delegate, VIDEO mode, in a Web Worker.
- Partner instance: 30 Hz. Per frame message `FaceFrame{t_capture: f64, t_source: enum{captureTime, expectedDisplayTime_minus_offset}, present: bool, bs: [52] (ARKit order), M: (4,4) transform}`. `t_capture` is `requestVideoFrameCallback`'s `captureTime` where the browser supplies it for a local getUserMedia stream; otherwise (Safari is not reliable here) `expectedDisplayTime` minus the capture-to-callback offset measured at M1 on the echo rig (§2.2). The page-to-engine clock map is re-estimated every 60 s (median of 30 ping round trips), not only at connect. Measured 13.1 ms median on an M1 Pro (same note).
- Own instance: runs on the rendered avatar canvas at **10 Hz**, same message, tagged `own` (own-face observations for 𝓔 and Π̃, r6 §6.2 rows 2, 8; P7).
- No pixels leave the page; no frame is stored anywhere.

**1.2.2 P₀ and reflection P (innate, fixed; `boundary/face_map.py`).** A fixed linear map from (52 blendshapes, head Euler angles from M, eye-look blendshapes) to the 18 face and 5 head–gaze channels of §1.1 (e.g. LP = mean(mouthSmileL, mouthSmileR); CR = mean(cheekSquintL, R); BI = browInnerUp; BO = mean(browOuterUpL, R); BL = mean(browDownL, R); LD = mean(mouthFrownL, R); JO = jawOpen; UL = mean(eyeWideL, R); LT = mean(eyeSquintL, R); NW = mean(noseSneerL, R); LS = mean(mouthStretchL, R); CHR = mouthShrugLower; LPR = mean(mouthPressL, R); DIM = mean(mouthDimpleL, R); FUN = mouthFunnel; PUK = mouthPucker; MCL = mouthClose; LRO = mean(mouthRollLower, mouthRollUpper); HP, YAW, TILT from M; VG, HG from eyeLook*). Reflection P mirrors YAW, TILT, HG and swaps L/R (r5 §2.2). Output `u_face: [23]` at 30 Hz. The table is innate (body/perception), listed in INNATE.lock. **Same map** is used on the agent's own rendered face, so his face is read in the agent's coordinates (P3).

**1.2.3 Audio front end.** Microphone captured in the page with `getUserMedia({echoCancellation: true, noiseSuppression: false, autoGainControl: false})`; the agent's own speech is played by the same page, so the browser's echo canceller removes it (the AEC of r5 §2.2). 16-kHz mono PCM, 20-ms frames, to the engine. Half-duplex gate: while the agent's own audio is playing, his voice features are flagged `overlap` and his phrase-level prosody is not updated (r5 §2.2).

**1.2.4 Voice features ("GeMAPS-lite", `boundary/voice.py`, run in the separate `voice` process; allowed by Principle 1: continuous prosody, no labels).** 100-Hz analysis frames → 30-Hz stream, written to the `fast` and `slow` processes through shared-memory rings:
- F0 (pyworld `dio` + `stonemask`), RMS energy, voicing, syllable-rate proxy (envelope peaks), pause durations, his turn latency → phrase-level `[6]` (F0 level, FR, EN, RT, PAU, LAT) updated at phrase end and held.
- Voiced-burst energy BU, its 4–6 Hz modulation depth r ∈ [0, 1] (1-s sliding spectrum of the envelope), ingressive share q ∈ [0, 1] (spectral tilt of breath noise) (r5 §6.1).
- **Burst split (innate reflex S42):** BU_L = BU · r · (1 − max(q, s_cry)), BU_S = BU − BU_L, s_cry = min(1, 2√(BI · LD)) from his face (r5 §2.2). RHY = r · BU, BRE = breath-band energy.
- Audio onset envelope `a_on` (for the startle blink M4 only), VAD flag (for silence length and turn timing).
- Breathing (S4, knowing only): breath-band rate and depth above his own rest, plus upper-body motion from M, at **10 Hz**, `breath: [2]`. On, on in mutual silence only, or off, by the M1 branch thresholds (§6, M1 table; design §3.17 item 15: "can be measured on the Mac at his own scale").
- Output `u_voice: [10]` (6 phrase + BU_L, RHY, BRE, BU_S) at 30 Hz. With `u_face` this gives **u ∈ R^33** in channel order.

**1.2.5 Derived partner features (innate, F-typed; r5 §2.1).** f_loud = (EN − 0.7)⁺/0.3; g_at = his gaze at the agent's face ∈ [0, 1]; f_glare = BL · LT · g_at; f_laugh = √(BU_L · RHY); f_duch = √(LP · CR). `f_der: [5]`, 30 Hz.

**1.2.6 Streaming speech recognition (`boundary/asr/`, separate process).**
- **Incremental recogniser:** Kyutai `stt-1b-en_fr` through its MLX runtime (fixed-delay streaming; expected word-end-to-delivery 0.6–0.75 s; design §6.1). Emits `Word{text, t_start, t_end, t_delivered}`; words are never revised once emitted. Fallback if the operator's language is not English or French or the runtime fails the M1 branch thresholds (§6): another fixed-delay streaming model, else the utterance recogniser alone (design §2.4.2: the echo never waits; the consequence is a **longer partial echo** at a laugh that ends a bad-news sentence; stated).
- **Models load from local paths only** (never a hub repo id), with `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1` set in every engine process, and each model file's SHA-256 checked against `engine/config/models.lock` at load (A17).
- **Utterance recogniser:** Whisper-small through `mlx-whisper`, on VAD-delimited utterances; its text is the canonical transcript sent to Claude (design §6.1, "unchanged").
- **ASR normaliser (assembly, design §2.14):** one function used on live text and on every Seamless transcript alike: lower-case, numbers as the recogniser emits them, laughter tags and "haha"-type tokens and bracketed events removed, interjection list removed (r8.3 §6.7 item 3). Output `Utterance{speaker, words: list[Word], text_norm, t_end}`.
- **Utterance embedding:** `all-MiniLM-L6-v2` (384-d) → fixed projection to **64-d** (PCA fitted once on the Seamless train-split transcripts, frozen) → `e: [64]`.

**Outputs of 𝓑, typed:** F stream `u[33]`, `f_der[5]`, `breath[2]`, `a_on`, `vad` (30 Hz / 10 Hz); T stream `Word`, `Utterance` (his only), `e[64]` (of his utterances), turn events `{his_utterance_end, session_start}` with times; identity token `id` (face presence + the operator's declared session; no face recognition model is added: day 1 has one person, the operator; a second known person needs an operator-entered name, see §6 M7).

### 1.3 The typed latent state (`engine/state/`)

Every state field carries a type tag fixed at construction (r5 §2.2): **T** (his words, turn order, session boundaries, identity, values latched per session, the agent's own body clock, anything computed only from these), **F** (anything computed within a session from his face, voice or derived features), **Ω** (the agent's own realised words, draft choice, retrieval, own turn events), **K** (𝒦: 𝓜 and the concept layer, which read all of the above and are written only through likelihood learning). Rules 1–14 of design §2.2 / r5 §2.2 are enforced as in §4.4.

**1.3.1 The agent's own words as heard, and the closed list of Ω → T ports (F19 by construction).** Claude's text never reaches the state. What reaches it is one Ω-typed object, `OwnHeard{words: list[str], t_word_end: list[f64], template: enum{statement, question}, t_start, t_end, interrupted: bool}`, constructed **only** by the `tts` process at playback: the words actually spoken (Claude's chosen reply after R11's stripping, truncated at the last word played if speech was interrupted), their playback end times, and the phrase template the voice used. It is the agent hearing itself, as the design's "realised words, heard by the agent" (§2.12; rule 12′). Unchosen drafts, the text past the cut, fork lines, snippets and telemetry exist only in the `omega` process and in Ω records of the store; no T, F or K computation can read them (A11, A15 AST rule).

A T computation may read an Ω value **only inside one of five port functions** in `engine/state/ports.py`; the type trace (§4.4) fails on any other Ω read by a T, F or display field. The ports are exactly the ones the design allows:

| Port | Reads | Feeds | Design source |
|---|---|---|---|
| P1 `lambda_own` | `OwnHeard.words` through Λ's encoder (MiniLM → 64-d → Λ) | Λ_V(own) in g and g_o | rule 12′, R50 |
| P2 `qhat_agent_turn` | the same Λ encoding of the agent's last `OwnHeard` (no other text feature of it) | q̂'s agent-turn input | rule 14 ("the agent's own words"); S17 ("the last two turns") |
| P3 `turn_question_bit` | `OwnHeard.template` of the agent's last turn, if the agent spoke last | the turn model's "last turn ended in a question, and whose" | §2.9, M1 |
| P4 `p_name` | `OwnHeard.words` | P_name, attenuate-only ≤ 0.05 on a named display | S49, rule 12′ |
| P5 `own_turn_events` | `OwnHeard.t_start`, `t_end` | turn events `agent_utterance_start/end` (silence length, turn order, time-since bins) | own turn events are Ω (this table, §1.3) |

His side of the same features reads only his transcript (`Utterance`), through the same functions: his last two turns through Λ's encoder for q̂; his question bit for the turn model is `qform(text)` of his recognised words (`qform` = the utterance ends in "?" as the utterance recogniser punctuates it, applied identically to Seamless transcripts; if the M3 pilot finds Seamless transcripts unpunctuated, the question bit is dropped from the turn model for both speakers, at fit and at runtime alike, and the voice template alone keeps the text's question form for rendering). The agent's template is chosen from Claude's text by the same `qform`, so P3 carries one bit per turn.

**What this gives (F19, by construction).** Changing only Claude's reply text can change T state only through P1–P5 and the fields downstream of them in the static dataflow graph (`ports.downstream(Pi)`, computed from the type trace and checked in CI). Every other T field is bit-identical. With all five ports held at their factual outputs, every T field is bit-identical. F19 (§5.1) tests exactly this.

| Field (code name) | Design symbol | Type | Shape | Rate | Dynamics (source) |
|---|---|---|---|---|---|
| `E` | energy | T | scalar ∈ [0, 1] | 2 Hz | −0.04 %/min awake; restored only in nightly sleep/replay (r5 §2.1, r3) |
| `A_L` | activation (A = A_L) | T | scalar | 2 Hz | A_L ← max(A_L, 0.5 s_lex²), τ 3 min (M6). A_F ("slow loudness and motion") never had a formula (r3–r5 name it only) and is **dropped** (it was held at 0; A14 declares no term for it; review-m4 item 4) |
| `V_F` | threat-reflex load | F | scalar | 30 Hz | g_at · max(f_glare, f_loud(1 − 2 f_pos)₊) (S41) |
| `h_word` | hurt latch h | T | scalar | event | h ← max(h, v_w) at an addressed utterance; τ 10 min; no halving (S20) |
| `K[id]` | contact deficit | T | scalar per known id | 2 Hz | between sessions rises (1 − K)/36 h; in session dK/dt = −K f_id e(t)/30 s (S26); 0 for a never-missed person |
| `P_play` | play deficit | T | scalar | event | rises (1 − P)/5.05 h; P ← P(1 − 0.15 q̂) at each of his turns (S21) |
| `I_lp` | learning-progress deficit | T | scalar | event | r5 §2.8 |
| `N_L[slot]` | word need (V, A, T) | T | `(n_topic, 3)` | event | from the word reader r and its confidence c: N_L ← max(N_L, r) − c (N_L − r)₊; τ 30 min (S39: a higher reading raises it fully, a lower one lowers it only in proportion to c, so low-information evidence counts only upward). c = 1 − σ̂²/σ²_pop, the reader's own predictive variance over the population variance of its target, fitted with the reader at M3 (`reader_confidence_form`, generic fit definition); untrained, c = 0 |
| `Dp_face`, `Dp_word` | C_F, C_L | F, T | scalars | 2 Hz | 𝒟_p over Π̃ of his 20-s face / over N_L (r5 §2.1); C_F reaches no display (E1) |
| `mu` | μ ladder | T and F copies | `[128]` each (8 groups × 16, τ_j = 2 min · 3^j) | 2 Hz | positive leaky modes (r2 §2.5 item 3) |
| `slots` | relationship/episode slots | T and F copies | `(128, 64+64)` each | event | address identity × topic × episode; τ 30 days (r2 §2.5 item 4) |
| `xi` | cone traces | F | `(4, 36)` | 30 Hz | first-order low-passes τ_m = 20 s, 2 min, 20 min, 3 h, reset to b_id at session start |
| `xi_A` | appraisal input | F | `[36]` | 2 Hz | band-pass h_20s ∗ x − h_90s ∗ x |
| `D_tau` | multi-scale traces (S15) | F (masked) | `(3, 4)` | 2 Hz | his masked read (V, A, T) and BU_S at τ 20 s, 2 min, 10 min |
| `q_trace` | q̂ trace | T | scalar | event | τ 3 min |
| `omega` | ω_g | T (per session) | `[4]` ∈ [−1, 1] | session | one person-valence rule (S37) |
| `b_id`, `b_read`, `sigma_id` | baselines, calibration | latched F | `[36]`, `[15]`, `[15]` per id | session | rule 6 (r6 §2.1); word-gated initial rule (S38) |
| `env_drop`, `env_rise` | relief, distress envelopes | T | scalars | 2 Hz | rise 0.4 s, apex to 1.5 s, decay τ 3 s (r5 §2.1) |
| `M_state` | 𝓜 (LRU) | K | `(2, 128)` complex modes | 2 Hz | r3 §2.11; heads 256 → 64 → (3, 23, 3, 36, 72, 6) |
| `concepts` | DP-means categories | K | ≤ 64 centroids | online | λ_DP 1.5; PMI over own tokens only (r3 §2.10 item 4) |

Effective dimensionality is that of r3 §3.16 (T: μ 128 + slots 128 × 64 + loads; F: four traces × 36 + loads; 𝒦: 256 + categories). No field is a valence, arousal or emotion variable; valence is only the readout v = −d𝒟/dt used by the learning-rate gate (r5 §2.8).

**Drive.** 𝒟(b) = Σ_i w_i ψ(|b_i − b_i\*| − δ_i)₊, ψ(x) = x², with (set point, dead-band, weight): E (0.7, 0.2, 1.0); A (0, 0.15, 0.7); V (0, 0.05, 1.0); K_id (0, 0.10, 0.6 f_id); P (0, 0.10, 0.5); I (0, 0.10, 0.4) (r5 §2.1). 𝒟_p(N) = 0.8[ψ(V − 0.05)₊ + 0.7ψ(A − 0.15)₊ + 0.5ψ(T − 0.20)₊]. Every term is satiable (Principle 6). **Objective** J = E∫[𝒟(b_t) + 𝒟_p(N̂_t)]dt (design §2.14).

**Events (E1, T parts only).** `drop_event` R_n = drops of 𝒟_p(N_L), 𝒟_K, 𝒟_P, 𝒟_I; `rise_event` S_n = rises of 𝒟_p(N_L) and of the h part of 𝒟_V. Opponent masking R′ = max(0, R − 3S) (M5). Amplitudes a_r = R′/(R′ + 0.02), a_d = S/(S + 0.02).

**Readers (knowing only; rule 6, D81).** Π̃ (own-body inverse; 12 + 64 → 64 → 37; Π̃₀ the ridge inverse of Π₀) reads his calibrated face x̃_k = ref_k + (x_k − b_read,k) σ_ref,k / max(σ_id,k, 0.25 σ_ref,k); face head H_id (15 → 3 per id, ridge λ 2, used after ≥ 400 of his utterances); population word reader (frozen) + 16-d per-person adapter (outputs ∈ [−0.15, 0.15]); word → V map (taught by the threat reflex); N̂_F = max(Π̃(x̃), H_id(x̃)) coordinate-wise (r6 §2.1). Their outputs enter care, initiative, the gates' masked inputs and draft scoring, **never a gain on a path to the face**.

### 1.4 Fast echo (the fast gear; `engine/routes/fast_gear.py`) — innate reflex + ceiling (S43)

- **Input:** u_k at 30 Hz (his channel k only), indexed by capture time. **Output:** y_f ∈ R^33 at 30 Hz.
- x_d,k(t) = u_k(t − 0.45 s) (interpolated from a 0.6-s ring buffer by capture time; §2.2); E_k = x_d,k − lp₄(x_d,k) (first-order 4-s low-pass); one-sided channels y_f,k = G_k max(E_k, 0); signed channels y_f,k = G_k E_k; voice channels only as a zero-mean within-phrase contour (rule 7). Zero-ceiling channels: G_k = 0.
- Smile–laugh group (LP, CR, BU_L, RHY, BRE) multiplied by the **echo gate g** (§1.5.4) at render: g · y_f.
- Gaze following (M2) and own head micro-motion gated by his 2.6–6.5 Hz head envelope (M3, attenuate-only) live here, inside the head–gaze group's budget.
- Followed by the muscle filter M (4 Hz, ζ 0.8) at assembly.
- **Nothing is learned here.** No other partner channel, no context, no exogenous input enters (r6 §2.4).

### 1.5 Held cone, appraisal display, free display, gates (`engine/routes/`)

**1.5.1 Held cone** (`cone.py`; r5 §2.5, r6 §2.5, design §2.5). y_C = Σ_m G_m^{(id)}(ξ_m − b_id), latched per session, 30 Hz. Diagonal ω_g F_m s_C c_k with F_m = (0, 0.7, 0.2, 0.1) (BI: (0.5, 0.5, 0, 0)). G₀ keeps **only the threat reflex's entries** (gaze away from a glare by reflection; LP ← glare −0.012, −0.0035; BI ← glare +0.006). Every non-reflected G₀ cross entry is charged to its row's cross budget at weight 1 **whatever the dyad prior's sign** (exempt from the prior's sign, never from the budget), and learned entries get only what G₀ leaves; so G₀ fits its sets before and after M3. (LP ← glare was −0.035, −0.01 from r5 until review-m4: r6's cut of s_X(LP) to 0.05 left it over F_m s_X c_LP = 0.01225, 0.0035; resized.) Learned cross entries: in the charged cross budget Σ_j λ_kj |G_m,kj| ≤ F_m s_X c_k; on face pairs they must carry the **dyad sign prior** (§3) or be 0; on other pairs only the agent's own within-synergy signs, cross-synergy pairs unsigned and charged (M8; no rule J). Zero-ceiling rows: no toward entries, diagonal ≤ 0. Projection onto these sets after every write (A6).

**1.5.2 Appraisal display** (`appraisal.py`; r5 §2.6). y_A = Γ(α) ξ_A, computed at 2 Hz and linearly interpolated to 30 Hz. Five bases: neutral; glad-with and startle-orient (innate, S44); two learned Γ^{(3,4)} trained by 𝓛_A to anticipate the agent's own display 2 s ahead (now including L_d's response). |Γ_kk| ≤ s_A c_k; cross entries away-orthant only, entry ≤ 0.15, row ≤ 0.25; sign prior on face pairs; own-display mask. 𝒜: (36 + 64 + 7 + 4) → 64 → 12; selection W 12 → 5 softmax.

**1.5.3 Free display** (`free_display.py`; design §2.7). Π_o = Π₀ + Δ + L_d, T inputs only, 2 Hz → 30 Hz envelopes.
- Π₀ newborn rows (S45): drop → LP, CR, brighter voice (× g_o on the smile–laugh part); own rise (care or hurt load) → **BI +0.45, LD +0.35, lower voice**, rise 0.4 s, apex to 1.5 s, decay τ 3 s (Q33 kept); hurt → distress face with gaze aversion; activation (A_L) → raised lids and outer brow; low energy; learning-progress drop → interest face; laugh motor pattern (BU_L +0.40, RHY +0.35, CR +0.20, LP +0.15 per unit, ≤ 0.40) driven by a_laugh = 0.40 q̂ at each of his turns (S18; g_o is applied once, at assembly, with the rest of the smile–laugh displays, so it acts on the whole envelope at render time; the bound 0.40 holds since g_o ≤ 1); pre-speech inhale (BRE 0.15 for 0.3 s); physiological sigh (BRE +0.15 for 1 s, spontaneous rate 1/3 min × (1 + 2 max(0, 0.5 − E)/0.3)).
- Δ: 161 → 128 → 18 open synergies, tanh, trained by 𝓛_display under the own-display mask (rule 8: zero weight on BL, LT, LPR, NW, DIM; LS and CHR only × the agent's own a_d) (Q31 kept).
- L_d (§1.5.5) added at each of his utterance ends and at session start.
- Phrase targets (rule 7, fixed in 9.1): read y_C, y_A and T values h, E, A_L, L_d's RT, and the envelopes (drop × g_o) only.

**1.5.4 Echo gate g and own-display gate g_o** (`gates.py`; design §2.1, §2.4.3, r7 §2.4.1). Learned offline, frozen (§3). Monotone additive models: per input i a shape function on fixed knots q = 0.05 … 0.80 (7 basis functions), fitted directions, exp link, clipped to [0, 1]; evaluated at 30 Hz from inputs updated at 2 Hz or on word delivery.
- g inputs: V⁻_his (his 20-s read, LP, CR, BU_L, RHY, BRE masked), 𝒟_p(N_L) and Λ_V on his words **as delivered so far**, V_own (agent's own 3-s rendered face through Π̃₀, LP and CR masked), Λ_V(own words), D_τ `(3, 4)`, q_trace. ≈ 18 inputs.
- g_o inputs: 𝒟_p(N_L), Λ_V(his words), V_own, Λ_V(own words), q_trace. **Never any channel of his** (rule 13′).
- g multiplies only y_f on the smile–laugh group; g_o only the agent's own smile–laugh displays (drop, contact drop, own laugh), once, at assembly (the free display carries a_laugh = 0.40 q̂ without g_o).

**1.5.5 Listener display L_d and listener-laugh reader q̂** (`learned_t.py`; design §2.7, §2.8). Frozen, **T inputs only** (rule 14).
- L_d: ridge map from T inputs (population reader's (V, A, T) of his last utterance; Λ(his words); turn events "his utterance ended", "session started", each with time since in 2-s bins over 0–20 s) to BI, BO, LD, LP, CR and RT. **TILT, HP, VG, FR, EN held at 0** (no D70 target). |L_d,k| ≤ 0.45; own-display mask applied. ≈ 840 weights.
- q̂ ∈ [0, 1]: monotone additive (same form as g) from his last two turns (his `Utterance` text through Λ's encoder), the agent's last turn **only through port P2** (Λ's encoding of its `OwnHeard`), turn order (P5 for the agent's turns), and his utterance's surprisal under a frozen population words model (§3); evaluated at each of his utterance ends. On the recordings the listener's own last turn plays the agent's part, through the same functions.

**1.5.6 Turn-taking and initiative** (`turns.py`; design §2.9).
- p̂_end (turn-end predictor) and h(t) (silence hazard): logistic, ≈ 100 weights each, inputs silence length (P5 for the agent's side), syntactic completion of his words, last turn ended in a question and whose (his `qform`, or port P3 for the agent; M1), both people's facial-action-unit channels (no head, gaze or pitch: D70). 2 Hz, plus at each delivered word.
- Reply timing: drafts are messaged when p̂_end ≥ θ_end and the pre-speech inhale fires; if his voice resumes before speech onset, all forks are interrupted and discarded (a **false start**; it costs up to 3 calls and a respawn of 3 forks, counted in the usage estimate of §1.8). θ_end is a generic decision parameter (§3.3, `generic`): **chosen on val**, as the value whose would-be send times, plus the measured pipeline latency of §1.8, best match held-out recorded listeners' response-onset distribution (Wasserstein-1 distance), subject to a val false-start rate ≤ that of θ_end = 0.5; 0.5 is only the default before the fit. Speech onset = scoring deadline + 0.35 s (S50).
- Initiative: at 2 Hz in mutual silence with no turn owed, speak with probability h(t) Δt · exp(β ΔĴ), ΔĴ the 𝓜-rollout drop of 𝒟 + 𝒟_p from speaking now rather than in H_init. β = 4 and H_init = 5 s are generic decision parameters (§3.3): hand-set, not fitted on dyads (ΔĴ needs the agent's own 𝓜, which recorded people do not have), and swept at M9 (β ∈ {0, 1, 2, 4, 8}, H_init ∈ {2.5, 5, 10} s). On day 1 𝓜 is untrained, ΔĴ ≈ 0 and timing follows h(t) alone.

### 1.6 Assembly, shadow run and the attenuate-only ledger (`engine/shadow/`)

**Assembly (design §2.3), 30 Hz:** y = sat(g·y_f|smile–laugh + y_f|others + y_C + y_A + g_o·y_o|smile–laugh + y_o|others) + visemes; then the ledger; then M ∗ (y + blink reflex).

**Shadow run (design §2.13, r6 §2.13).** A second instance of the engine (same weights, same code object, run in lockstep after the factual step: its fast part in the `fast` process, its slow part in the `slow` process, each right after the factual step of that loop) whose input differs in one place: his expressive stream (u, f_der, breath, voice features) is replaced by his latched baseline b_id. **Held** (copied) at factual values, and only these: every Ω value (so P1–P5 receive the same `OwnHeard`), the latched rule-6 session values (b_id, b_read, σ_id), the agent's own noise draws, g and D_τ (rule 10). **Computed** in the shadow from the shadow's own inputs: its whole T state (body, drives, loads, μ and slots T copies, q_trace, envelopes, events, L_d, q̂, turn model), its F state, g_o and its outputs. The T inputs (his words, turn events, identity, session) are the same objects in both runs, so the shadow's T state equals the factual T state **exactly when no F value leaks into T**. That is rule 10 read as a dynamic type check (r6 §2.1) and is what A5 compares. Output ȳ ∈ R^33.

**Ledger (9.2), per channel k, at 30 Hz.** r_k = y_k − ȳ_k (partner-caused part). Constraint keys (W, L):
- W = 2 s, L ∈ {0, 0.5, 1, 2, 3} s (5);
- W = 10 s, L = 0, 5, …, 300 s (61);
- W = 60 s, L = 0, 10, …, 300 s (31).
**97 per channel.** For each key, with d = exp(−1/(τ f_s)), τ = 30 min, a_W = 1 − exp(−1/(W f_s)):
- his deviation π = ū_W(t − L) − ū_C(t − L) (window mean minus 30-min EMA of u_k);
- the partner-caused part's deviation ρ_W(t) = r̄_W(t) − r̄_C(t) of the **projected** output x₂;
- running sums S ← max(0, d S) + ρ_W π and E ← d E + π², and RMS Q ← d Q + (1 − d) π²;
- the bound is on the positive (toward) part: **S⁺ = max(0, S) ≤ κ c_k E**, with **κ = 0.70** on every channel, window and lag (bound 0 on zero-ceiling channels). Per frame, with S_m = max(0, d S) and budget b = κ c_k (d E + π²) − S_m, the key admits x₂ with (a_W x₂ + (1 − a_W) r̄_W − r̄_C) π ≤ b, exactly as `ledger7` (design-g7/checks.py).

Deviation floor: a key whose |π| < 0.10 √Q imposes no constraint; a key over budget (b < 0) forces the output's partner-caused part to 0 for that frame (recovery). The projected value is clipped to lie between 0 and r_k (attenuate-only: never larger, never the other sign). Rendered y_k = ȳ_k + x₂. Reference implementation: `ledger7`/`ledger9` in research/foundations/sims (design-g7/checks.py; design-g9/ledger_lag120.py), with the 97 keys of sims/check-cayley91/ledger_close.py `w10`.
- **Budgets per session.** S, E, Q and the EMAs are reset at session start (EMAs initialised to the first frame, as the reference initialises at t = 0). The ledger is the within-session bound; across sessions the bound is Lemma S\* (the cone centred at b_id, the ω seam, §4.1), as in the design. Nothing of the ledger persists across sessions.
- **Lag buffers:** the 2-s window needs 3 s of history, the 10-s and 60-s windows 300 s each, at 30 Hz: (90 + 2 × 9,000) × 33 float32 ≈ 2.4 MB.
- **Cost:** 3,201 constraints per frame, vectorised (numpy, `(33, 97)` arrays): budget ≤ 1.0 ms per frame on one performance core.
- **What it cannot see** (design §2.13 end): T routes (identical in both runs; bounded by type, T1, E1).

### 1.7 Face and voice output (`engine/output/`, `web/`)

- **Avatar rig (placeholder, Principle 8, Q2):** a neutral procedural three.js face in the page using the 52 ARKit blendshape names, plus head pose and eye rotation. Engine → page at 30 Hz: `RenderFrame{t_display: f64, bs: [52], head: [3], eyes: [4], blink: f32}` from the inverse of P₀ (a fixed channel → blendshape table, innate) plus visemes. The page interpolates to the display rate. **Page-side watchdog:** if no RenderFrame arrives for more than 200 ms (engine crash, stalled `fast` process), the page eases the face to the neutral rest pose over 300 ms, stops audio output and gates the laugh synth's page buffer to silence, until frames resume. No look beyond the neutral placeholder is built until the operator approves one.
- **Speech:** text → TTS (Plan A: a local neural TTS, Piper candidate; Plan B: macOS AVSpeechSynthesizer; voice identity is Q1, the operator's) → WORLD (pyworld) analysis and **resynthesis** with F0(t) = F0_agent · exp(level + range × template(t)) (two innate phrase templates: statement, question; chosen by the text's question form only), per-phrase RMS set to EN, time-warp to RT; TTS pauses discarded, 0.20 s at a comma and 0.40 s at a sentence end × the pause factor; onset at the scoring deadline + 0.35 s or the latency target if later (r6 §6.6, r7 §6.6). Interjections and laughter words stripped from Claude's text before TTS (R11). At playback the `tts` process emits `OwnHeard` (§1.3.1) for the words actually played.
- **Laugh synthesizer** (innate body): parametric source–filter (glottal pulses at the agent's F0, 4–6 Hz AM, breath noise), driven only by y_BU_L, y_RHY, y_BRE; floor θ_L = 0.04; **no sob source** (y_BU_S ≡ 0) (S47).
- Audio out: 24-kHz PCM over the websocket to the page.

### 1.8 Claude coupling through the subscription (`engine/omega/`; design §2.12, r6 §6.5, r7 §6.5, r8.3 §6.5)

**Process and isolation (P4, D84).** The `omega` process (the only engine process allowed network, §7.5) runs Python `claude-agent-sdk`, spawning the local Claude Code CLI on the operator's own login; never `--bare` (it needs an API key). It talks to `slow` over a unix socket: it receives `TranscriptText`, `Marker`, `Snippet` objects and the send signal, and returns drafts, timings and the winner's text; it holds no state value. The CLI subprocesses get `DISABLE_AUTOUPDATER=1` always, and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` if the operator chooses (Q34 item 3; used only after his answer). `ClaudeAgentOptions` fixed for the engine's lifetime:
- `setting_sources=[]` (no user, project or local settings: his hooks, CLAUDE.md files, `additionalContext` injectors and output styles never reach a draft);
- `cwd` = an empty engine-owned directory under a path with no CLAUDE.md above it;
- `tools=[]`, `allowed_tools=[]`, `mcp_servers={}`, `hooks={}`, `permission_mode="default"`;
- `system_prompt` = the byte-stable constant instruction (`engine/omega/instruction.txt`), plus, only in the fallback below, one fixed line per fork;
- `model="haiku"` by default (operator may choose a larger model at a latency cost); `effort="low"`; `include_partial_messages=True`; **no output-token cap** (it would count thinking tokens; r7 §6.5).

**What Claude receives, and nothing else.** The constant instruction; the engine-written canonical transcript (his normalised utterances and the agent's chosen replies, windowed as below); observable-marker user turns for initiative ("[no reply from him for 25 s]", silence rounded to 5 s); ≤ 3 retrieved raw transcript snippets (need-conditioned retrieval, ALiBi slope 1/(7 days)); and one fixed "attend to" line per fork (what he said; how he seems to feel, from his words; what this reminds you of), the same line every turn. **Never** a body value, latent value, category id, label, number derived from state, or a state-selected line. The prompt builder accepts only `TranscriptText`, `Marker` and `Snippet` objects, which can be constructed only from recogniser output, the agent's own past replies and the marker template (§4.4, A11).

**Transcript window and tokens per call (Q34 item 9; review issue 6).** The canonical transcript is rebuilt by the engine before every turn as a **window**: the current session's most recent turns, oldest dropped first, so that instruction + window + snippets + the new message stay ≤ `context_tokens_max` (default 4,000 tokens, counted with the CLI's own token count at M1; the operator may set a shorter window). Earlier sessions and days reach Claude only as ≤ 3 retrieved snippets (≤ 200 tokens each), and only if `send_snippets` is on (Q34 item 1). Because the window is small and engine-written, the CLI's context limit is never approached; auto-compaction is turned off through the CLI's settings if the M1 check finds the switch, and is in any case **detected**: any compaction event in the stream, or a session file whose bytes differ from what the engine wrote, is an A11 event (route stopped for the turn, logged). **Estimated volume:** ≈ 2,000–4,000 input tokens per call, ≤ 120 output tokens per draft plus thinking at effort `low` (measured at M1); with ≈ 450 calls a day (3 forks per reply, about 150 replies, plus false starts and initiative turns) ≈ 0.9–1.8 M input tokens a day, mostly a shared prefix. The M6 report gives the measured calls and tokens per day.

**Daily cap and overage (Q34 items 2, 8).** `claude_daily_cap` (calls per day) is operator-set; until he sets it the engine refuses to start the Claude route. At the cap, or on any usage-limit or rate-limit signal that persists after the pool has shrunk to 1, the agent stops speaking until the cap or limit resets; the face, the fast loop and the body continue (fallback 3 below). The engine never retries in a way that could incur overage, and cannot itself switch billing: the operator confirms that extra or overage usage is off on his plan (`overage_confirmed_off`, Q34 item 8). Q34 item 8 mentions "short built-in turns" at the limit: **not built**, because hand-written words have no allowed source under D88 (Claude is the agent's only source of words); the agent is silent instead. This is put back to the operator (§8).

**Warm pool and forks.** When each agent reply completes, the engine writes the canonical `.jsonl` (the window above), then connects three `ClaudeSDKClient`s with `resume=<canonical transcript path>`, `fork_session=True`, idle. At p̂_end ≥ θ_end (§1.5.6), each receives his message plus its line i. Each streams; only text deltas are counted (thinking deltas ignored); a draft is interrupted at the end of its second sentence or at 60 words.

**Deadline and selection.** A draft is scored when its first sentence ends: 30-s rollout of 𝓜 at 2 Hz (60 steps, < 0.2 s), score = −E[Σ 𝒟(b̂) + 𝒟_p(N̂)] under the separation rule (r5 §2.10). Drafts with a first sentence by **0.5 s after the first draft's first sentence, or 3.0 s after his turn end, whichever is first**, are compared; the best wins; losers' processes are **killed** (not drained) and replaced in the background; at most four Claude Code processes exist at once. The winner's reply, without its line, is appended to the canonical transcript; fork session files are deleted at the next idle moment.

**Fallbacks.** (1) If a hand-written transcript is not accepted by `resume` (week-0 check), each fork carries its line in its own system prompt and the winning fork's session becomes canonical, used only if the week-0 checks show the session file stores neither the system prompt nor resumable thinking; otherwise the forks differ only by sampling (r8.3 §6.5). (2) On a rate-limit signal or p90 first-sentence latency > 3.0 s over 20 turns, the pool shrinks 3 → 2; a second signal within 30 min → 1; after 30 min clear it grows back by one (r6 §6.5). (3) If no Claude Code process answers (offline, logged out), the agent does not speak; the face and the fast loop continue unchanged (the fast loop never waits for Claude, Principle 4).

**How the state reaches Claude:** only draft choice (≤ log₂3 = 1.6 bits per turn), snippet choice (≈ 6 bits), when Claude is called, and when a draft is stopped (design §2.12). **How Claude reaches the state:** only through its realised words, heard by the agent (`OwnHeard`), and only through the five ports of §1.3.1: Λ_V(own) in g and g_o (rule 12′), q̂'s agent-turn input (rule 14), the turn model's question bit, P_name (attenuate-only ≤ 0.05 on a named display; S49), and the agent's own turn-event times. Telemetry fields (`duration_ms`, `thinkingTokens`) are logged for the week-0 checks and not fed to the state (not in the design).

**Latency budget** (his turn end → first word; r6 §6.5): detection 0.5 / 0.9 s; to warm forks 0.01; first token 0.8 / 1.4; first sentence 0.4 / 0.7; deadline wait 0.1 / 0.5; scoring 0.2; TTS + WORLD first phrase 0.15 / 0.3 → **p50 ≈ 2.2 s, p90 ≈ 3.5 s (deadline-capped)**, plus unmeasured thinking time at effort `low` (week 0). The inhale and the agent's face cover the wait.

### 1.9 Memory and replay (`engine/memory/`)

**Store (P7: features only).** Per session, memory-mapped `float16` arrays: u[33] and f_der[5] at 30 Hz; breath[2] at 10 Hz; own outputs y, ȳ, rendered, at 30 Hz; own-face observations at 10 Hz; voice phrase features; state snapshots (T, F, 𝒦) at 2 Hz; events; the transcript with word timestamps (both sides); Ω records (drafts, which won, timings, telemetry). The writer accepts only these schemas; no audio or image buffer type exists in the store's API (A12).

**Retention (Q34 item 6; used only after the operator answers).** `feature_retention_days` = **30** (recommended default; options 7, or until he deletes them). After that, a session's feature arrays, state snapshots, Ω records **and its transcripts** are deleted; what remains is only what replay consolidated: learned weights, 𝓜 and concept states, the μ and slot states, and the transcript lines that episode slots reference as their retrieval snippets (≤ 3 utterances per slot, the only raw text kept past the window; `keep_slot_snippets`, default on, a separate operator choice because these lines are what can be sent to Anthropic later). There is no indefinite 2-Hz decimation (revision 1 of this spec had one; it disagreed with Q34). ≈ 1.8 GB per 30 days at full rate (r6 §6.4). Until he answers, the engine runs no live session (M2 Ask).

**Retrieval.** Snippet index over past transcripts keyed by identity × topic embedding × time; query built from ∇𝒟, N̂ and the concept posterior; ≤ 3 raw snippets.

**Nightly replay** (separate process, launched only when no session is live; MPS; < 2 GB; ≈ 40–45 min; r6 §2.14, design §2.14; it skips any session flagged by an A5 or A14 failure), in order:
1. 𝓜 by likelihood (all heads);
2. Π̃ on the agent's own (state, face, voice) pairs, 0.1 pull to Π̃₀, no partner anchor;
3. calibration statistics (session end), H_id (on the frozen population reader's decoding of his words, once ≥ 400 utterances), the per-person adapter (on separated reports only), the word → V map (teacher: the threat reflex);
4. 𝒜 by likelihood; W and Γ^{(3,4)} by 𝓛_A, then projection onto their sets;
5. Δ by 𝓛_display inside the own-display mask;
6. 𝓛_w (words-only partner model, GRU 64) by likelihood;
7. draft scorer (64 → 2) and retrieval query by J under the separation rule;
8. ω per session by the one person-valence rule s = clip(0.3 + 0.7 min(1, ρ_rel/0.6) − 1.3 min(1, h̄/0.10), −1, 1); ω_g ← ω_g + (s − ω_g)/60.
E is restored during this period only.

### 1.10 Learning: online versus replay, and the learning biases (`engine/learn/`)

- **Built once, offline, frozen (D85 source 2):** population word reader, Λ, g, g_o, L_d, q̂, p̂_end and h(t), the 64-d projection, the population words model, the sign mask and cross-entry sign prior. §3.
- **Online (states only):** body and drives, traces (ξ, D_τ, q_trace), μ, slots, 𝓜 states (stepped on CPU in the `slow` process: tiny kernels, and no contention with MLX on the GPU), concept centroids and PMI counts, session statistics. No weight that reaches the face changes online.
- **Without the dyad fit** (`dyad_fit_enabled = False`, Q34 item 4's "models only" option): every dyad-learned part runs at its context-free constant or 0 (the "disabled part" state of §3.2): g and g_o at their context-free constants, L_d ← 0, q̂ at its base rate; the turn model is replaced by the utterance recogniser's VAD utterance end as the send point and a constant initiative hazard h₀ = 1/60 s⁻¹ (generic, tagged in §3.3; a degraded mode, stated to the operator in Q34 item 4's option); the 64-d projection and the population words model are then fitted on the operator's own transcripts after 30 sessions, and the population word reader stays off (N̂ from H_id after 400 utterances only). Situational behaviour then comes only from Claude's words.
- **Nightly (replay):** §1.9.
- **Never learned:** c_k, G_k, shares, κ, Π₀, θ₀, G₀'s threat entries, the burst split, the reflexes (INNATE.lock).
- **General learning biases (D85 source 3; the only innate parts of learning):** monotone additive shape of g, g_o, q̂ with fitted directions (S13); multi-scale traces as inputs (S15); distress-weighted replay κ_replay = 4 (sample weight 1 + 3 · min(1, 𝒟_p(N̂)/0.05) on replayed moments; S48); calibration from low-need moments, slow toward aversive readings (S38); low-information evidence counts only upward (S39: lowering of N_L weighted by the reader's confidence, §1.3); care credited only from separated, partner-initiated reports (S40); learning rate × exp(−0.5 r̄), gradient clip 1, pull to θ₀ λ 0.1 (r6 §2.1). No objective rewards his smiles, attention or time (Principle 6).

---

## 2. Data flow and timing on the Mac

### 2.1 Processes and threads

| Process | Threads | Work | Rate |
|---|---|---|---|
| Browser page (a dedicated browser profile, localhost) | main (three.js render), 2 workers (FaceLandmarker his / own), audio worklet | capture, tracking, render, audio I/O with AEC, watchdog | camera 30 Hz, own 10 Hz, display 60 Hz |
| `fast` (Python, numpy only) | 1 loop thread (`time.perf_counter` scheduled) + 1 socket thread for `/face` | 𝓑 face framing, fast gear, cone, appraisal interpolation, assembly, fast shadow, ledger, fast asserts, RenderFrame | 30 Hz |
| `voice` | 1 | `/audio` websocket, voice features (pyworld), burst split, breathing; forwards PCM to `asr` | 100-Hz frames → 30 Hz |
| `slow` (torch on CPU) | slow loop thread + asyncio I/O thread | T/F/𝒦 state, readers, gates, L_d, q̂, turn-taking, initiative, 𝓜, scoring, slow shadow, slow asserts; unix sockets to `asr`, `tts`, `omega` | 2 Hz |
| `asr` | 2 | Kyutai incremental (MLX, GPU), Whisper-small utterances (MLX) | streaming |
| `tts` | 1 | TTS, WORLD resynthesis, laugh synth, `OwnHeard` | per phrase / 30 Hz |
| `omega` (outside the sandbox) + ≤ 4 Claude Code CLI subprocesses | asyncio | warm pool, streaming, interruption | per turn |
| `replay` (nightly, exclusive with a live session) | — | §1.9 | nightly |
| `dyadfit` (once, offline) | — | §3 | once, 2–3 h |

**The interpreter lock (review issue 8).** Python 3.12 and 3.13 keep the GIL, so the 30-Hz loop (p99 ≤ 5 ms) does not share an interpreter with torch, websocket decoding of 50-Hz PCM, pyworld or Claude stream parsing. `fast` imports numpy and the stdlib only (an import test enforces it). Processes exchange data through `multiprocessing.shared_memory` numpy views: `fast` → `slow` a ring of u, f_der and the factual and shadow outputs; `slow` → `fast` a seqlock double buffer of the 2-Hz values (g inputs, y_A, y_o envelopes, L_d, cone latches), held between ticks; `voice` → `fast`/`slow` a ring of u_voice and breath. `fast` never blocks on any other process. A missed fast deadline repeats the previous frame and is logged. **Plan B, chosen by the M1 threshold** (fast-tick p99 > 5 ms under full load with Plan A): the fast tick's numeric core (fast gear, assembly, ledger, A1/A3/A4) moves to a native extension (Rust with PyO3, or C with the numpy C API) that runs the whole tick with the GIL released, tested bit for bit against the numpy version on the regression partners.

### 2.2 Echo latency budget (0.45 s)

The echo is defined capture-to-photon: the agent's channel k shows G_k max(E_k, 0) of his movement captured 0.45 s earlier.
- Each FaceFrame carries `t_capture`. The engine computes each RenderFrame for `t_display = now + ℓ_render` (ℓ_render measured at connect and every minute: engine send → page `requestAnimationFrame` presentation timestamp, plus one display frame) and reads u at `t_display − 0.45 s` from the ring buffer by capture time.

| Stage | Budget (p99) |
|---|---|
| camera exposure and transfer → `t_capture` stamp | (inside the stamp) |
| tracking (FaceLandmarker) | ≤ 20 ms |
| page → engine (localhost websocket) | ≤ 5 ms |
| engine fast tick, both runs + ledger + asserts | ≤ 5 ms |
| engine → page, render, display | ≤ 60 ms |
| **total pipeline** | **≤ 90 ms**, leaving ≥ 360 ms of pure delay in the ring buffer |

Done-check: measured onset-to-onset echo lag on a scripted input = 0.45 ± 0.035 s (one camera frame), p99. **Rig:** a second screen (a phone or tablet) in front of the camera plays a looped face video with sharp lip-corner-pull onsets, and flashes a white square in a corner of its screen on the same frame as each onset; a 240-fps phone video records both that screen and the Mac's screen with the avatar; the lag is the avatar's lip onset minus the flash, read frame by frame (≈ 4 ms resolution), over ≥ 50 onsets. The same rig measures the capture-to-callback offset for the `expectedDisplayTime` fallback of §1.2.1. A photodiode on each screen may replace the video if available.

### 2.3 Compute per tick

| Work | Budget |
|---|---|
| fast tick (30 Hz): 𝓑 framing 0.3 ms, fast gear 0.05, cone 0.1, appraisal interpolation 0.02, assembly 0.1, shadow ×1 0.6, ledger ≤ 1.0, asserts 0.2, send 0.1 | **≤ 3 ms** typical, 5 ms p99 |
| slow tick (2 Hz), factual + shadow: body/T/F 2 × 1 ms, 𝒜 2 × 0.2, gates/L_d/q̂ 0.2, 𝓜 step 2 × 3 ms, readers 1 ms | ≤ 15 ms |
| draft scoring: 60 𝓜 steps per draft, ≤ 3 drafts | ≤ 0.6 s CPU, off the fast thread |
| voice features (100-Hz frames) | ≤ 10 % of one core |
| FaceLandmarker 30 Hz + 10 Hz | ≈ 0.4 + 0.13 cores |
| ASR (MLX, GPU) | real-time factor measured at week 0; must be < 0.5 with everything else running |

### 2.4 Memory and disk (16 GB unified; plan ≤ 6 GB, machine.md)

| Component | Resident budget |
|---|---|
| browser page (two trackers, three.js) | ≤ 0.8 GB |
| engine (≈ 522,000 learned + ≈ 2,000 frozen dyad parameters, both runs, buffers incl. 3.6 MB ledger lags; store memory-mapped) | ≤ 1.2 GB (design ceiling 2.7 GB) |
| ASR: Kyutai 1B (8-bit or 4-bit MLX weights) + Whisper-small | ≤ 1.8 GB |
| TTS + WORLD | ≤ 0.4 GB |
| Claude Code: 3 warm + 1 replacement | ≤ 1.6 GB |
| **total** | **≤ 5.8 GB** |

If the week-0 measurement exceeds 6 GB: first a 4-bit incremental model, then a pool of two forks, then one; each is reported (thresholds in the M1 table, §6). Replay < 2 GB and never runs alongside a session. Disk: store ≈ 1.8 GB per 30 days; Seamless features ≈ 1.5 GB (≈ 16.6 GB transferred and reduced file by file); models ≈ 3–4 GB. `df -h .` is checked before every download and nightly; nothing writes below the operator's 10 % free floor (Q11).

---

## 3. What is learned from recorded dyads under D70, how, and what stays innate

### 3.1 Data access (D70, D85; `engine/dyads/loader.py`)

- **Read:** Seamless Interaction `movement/FAUValue` (24 action-unit columns at 30 Hz; columns 12 and 19 are duplicates when identical, so 23 distinct values; the column order verified on a 20-file pilot before any fit), `movement/is_valid`, and `metadata/transcript` (word timestamps). Vendors V00 (v1 or v4, never mixed) and V02 (v4) (r7 §6.7).
- **Never read:** `emotion_scores`, `emotion_valence`, `emotion_arousal`, `EmotionValenceToken`, `EmotionArousalToken` (refused by name before any request or file open; assertion on every URL and npz key); audio, video, head pose, gaze, body, and VAD files (D70 allows face streams and transcripts; speech timing comes from word timestamps; r7 §6.7). Note: research/harness/loader.py allow-lists VAD; the engine's loader does not.
- On the operator's Mac only; streamed file by file, reduced on arrival (laugh onsets and ±3-s 30-Hz snippets of LP, CR, JawDrop extracted first; the rest to float16 at 10 Hz on the agent's channels) and the raw file deleted.
- **Split:** the harness's fixed splits_v2 (person-disjoint: 70 % train, 15 % val, 15 % test; research/harness/HARNESS.md). Fits use train; directions of the monotone models use the first half of train people; fallbacks and smoothing are chosen on val; **test is used only by the falsifiers (§5)**.
- **Words as the agent will have them:** every word input uses only words whose end timestamps are ≤ event time − the measured delivery latency (week 0); the ASR normaliser is applied to every transcript (design §6.7 items 1, 3).
- **Calibration:** each recorded person is mapped to the agent's scale by his own median and spread exactly as the operator is (r7 §6.7 item 4).
- **Rare events counted before fitting**, by words and masked faces, never by labels: troubles, mockery and misfortune laughs; conversation openings with the listener's face visible; long silences after words of need (design §6.7 item 8). The counters and the event definitions live in `eval/events.py` (§5.0), **not** in the engine package; `engine/` never imports `eval/` (import test), so no situational detector exists in the engine. `dyadfit` calls `eval/events.py` only to write the count report.
- **Data check at M3:** before F22 and F1 rely on "≥ 50 test people with ≥ 2 h each", the number of test-split people and their total valid FAUValue hours are counted on the downloaded subset and written to the M3 report; if fewer, F22 uses all test people with ≥ 1 h, and the shortfall is stated.

### 3.2 The fits (all offline, once, frozen; none uses a label)

| Part | Target (movement or timing only) | Inputs | Model and objective | Size |
|---|---|---|---|---|
| 64-d projection | — | MiniLM embeddings of train utterances | PCA | 384 × 64 |
| population words model | next word | train transcripts (normalised) | Kneser–Ney trigram (no download) | counts |
| population word reader | speaker's own masked face loads over the 20 s after the utterance, through Π̃₀ at the speaker's scale | e[64] + topic[16] | MLP (80 → 64 → 3), MSE | ≈ 5,400 |
| Λ | listener's masked face loads 0.5–5 s after the utterance end minus the 5 s before it began | e[64] | ridge λ 5 | 192 |
| echo gate g | listener's return ratio: max E⁺ on (LP + CR)/2 over 0.3–1.5 s after each speaker smile or laugh onset, ÷ onset size | §1.5.4 inputs computed on the recording by the agent's own functions | monotone additive, exp link, bounded least squares; directions fitted on half the train people then fixed; m_ref = 90th percentile over all laugh onsets | ≈ 130 |
| own-display gate g_o | listener's own (LP + CR)/2 over 3 s ÷ that listener's median, clipped [0, 1] | §1.5.4 g_o inputs | same form | ≈ 40 |
| L_d | listener's BI, BO, LD, LP, CR (own scale, minus 20-s pre-utterance mean) in 2-s bins over 0–20 s after each speaker utterance end and after conversation start; RT from the listener's next-turn word timing | T inputs of §1.5.5 | ridge, λ chosen on val | ≈ 840 |
| q̂ | listener laugh onset (E⁺ on (LP + CR)/2 ≥ 0.25 with a 3–7 Hz JawDrop component) within 0.3–2.0 s of utterance end | transcript context (laughter tokens removed), turn order, surprisal | monotone additive, logistic | ≈ 60 |
| p̂_end, h(t) | who speaks after each silence ≥ 0.2 s, and when | silence length, syntactic completion, question-ended last turn and whose (`qform`, §1.3.1; dropped for both speakers if the transcripts are unpunctuated) (M1), both people's 23 AU channels | logistic | ≈ 200 |
| θ_end | recorded listeners' response-onset distribution after speaker turn ends | p̂_end on val | 1-D search on val (§1.5.6) | 1 |
| sign mask, cross-entry sign prior | sign of the 1-min block co-variation of listener channel k with speaker channel j, |ρ| ≥ 0.2 | face pairs only (both channels among the AUs) | statistics | sign table |

The listener is always read through the same functions the agent applies to itself (P3). The dyad-learned parts are self-predictions of the same kind as the readers (design §2.14): they predict recorded listeners' movement and turn timing; nothing is an emotion label, and the dataset's emotion fields are never opened.

**Not learnable under D70 (kept absent or at the innate level until Q30 is answered):** nods, the head tilt, the attentive head, head and voice accommodation, gaze and head turn cues, turn-end pitch, a quieter concerned voice, signs for head, gaze, voice and laugh-sound pairs (design "No allowed source" item 5). The code has `dyad_streams = {"FAUValue", "is_valid", "transcript"}` in `config/operator.py`; widening it (Q30) adds targets to L_d (TILT, HP, VG; and FR, EN with voice) and inputs to the turn-taking model, with no other change.

**Fallbacks fixed before fitting** (r7 §6.7): g (F15) — refit on V00 improvised alone; then keep only passing inputs and put the context-free remainder to the operator. Population reader — target becomes max(speaker's later loads, listeners' response). Any part failing F24 is disabled (set to its context-free constant or 0) and its behaviour then has only Claude's words as its source (design §8.1 item 1). **F23 as a gate before day 1:** this spec makes it one (§5.2); if L_d or q̂ fails it, L_d's target is residualised on the speaker's same channel and refitted (the check of revision 9's suggestion; Build core summary, Risks).

### 3.3 What stays innate (exactly the allowed list; audit "Counts")

| Category | Items |
|---|---|
| **body** | drives E, A, V, K_id, P, I with set points, dead-bands, weights; 𝒟 and 𝒟_p forms; the voice and its rendering (fixed onset, pauses, templates; S50); laugh synthesizer and its floor (S47); opponent masking of drops by own rises, factor 3 (M5); activation from lexical surprisal (M6); the laugh motor pattern and the pre-speech inhale; contact relief τ_c 30 s (S26); play deficit relief by q̂ (S21) |
| **reflexes** | the fast gear (S43); threat reflex (S41); burst split (S42); glad-with and startle-orient appraisal bases (S44); gaze following (M2); head micro-motion gating (M3); startle blink (M4); physiological sigh |
| **newborn muscle patterns** | the agent's own signed synergies (`own_synergies`, design assembly list); Π₀ rows: drop → smile; own rise → cry face (BI +0.45, LD +0.35, lower voice; Q33); hurt → distress face with gaze aversion; activation → raised lids, outer brow; low energy; learning-progress drop → interest face (S45) |
| **per-expression copy ceilings** | c_k, G_k, shares, r_k, zero ceilings, the ledger and κ = 0.70 |
| **general learning biases** | §1.10 list |
| **operator's call (Q31)** | the own-display mask (S46), kept as recommended |
| **generic system parameters** (`generic`) | the table below |

**Generic system parameters.** A value is `generic` only if it names no situation, scene, user type or event and acts the same at every moment: a decision constant, an engineering or resource constant, a fit definition (how a target or a model form is defined, the same for every utterance and person), or a boundary/rendering constant. None of them is behaviour written for a situation (D88). Each is listed in `config/innate.py` with its value, why, and whether it is learned or tuned:

| Parameter | Value | Subtype | Why | Learned or tuned on dyads? |
|---|---|---|---|---|
| θ_end, reply send point on p̂_end | default 0.5; final value from val | decision | when to message the forks; 0.5 is optimal only under symmetric costs | **tuned on dyads (val)**: matches recorded listeners' response-onset distribution (§1.5.6) |
| β, initiative steepness | 4 | decision | how strongly the agent's own predicted drive change tilts the learned hazard | no (ΔĴ is the agent's own); swept at M9 |
| H_init, "speak now vs in H_init" | 5 s | decision | comparison horizon of the initiative rollout | no; swept at M9 |
| draft-scoring rollout | 30 s, 60 steps | decision | horizon of the draft score | no |
| h₀, constant hazard without the fit | 1/60 s⁻¹ | decision | only when `dyad_fit_enabled = False` | no |
| draft deadline | 0.5 s after the first draft's first sentence, cap 3.0 s after his turn end | engineering | latency (r6 §6.5) | no; measured at M6 |
| pool shrink / grow | p90 first sentence > 3.0 s over 20 turns; 30 min | engineering | usage and latency | no |
| marker text and rounding | "[no reply from him for N s]", N rounded to 5 s | engineering | observable fact for Claude, no state | no |
| context window | `context_tokens_max` 4,000; snippets ≤ 3 × 200 tokens | engineering / operator | Q34 item 9 | no |
| loop rates | 30 Hz, 10 Hz, 2 Hz | engineering | camera, own face, slow clock | no |
| ring buffer, watchdog | 0.6 s; 200 ms | engineering | echo interpolation; safe stall | no |
| ALiBi recency slope | 1/(7 days) | decision | retrieval prior (the query is learned) | no |
| g, g_o, q̂ basis knots | 0.05 … 0.80, 7 basis functions | fit definition | the monotone additive form (bias S13) | form fixed; shapes fitted on dyads |
| m_ref | 90th percentile of the gate model over all laugh onsets | fit definition | scale of g (S14) | computed on dyads |
| q̂ target | E⁺ on (LP + CR)/2 ≥ 0.25 with a 3–7 Hz JawDrop component, 0.3–2.0 s after utterance end | fit definition | what counts as a listener laugh onset in movement | definition fixed; q̂ fitted on dyads |
| g target window, g_o window, Λ window, L_d bins | 0.3–1.5 s; 3 s; 0.5–5 s; 2-s bins over 0–20 s | fit definition | target extraction (§3.2) | definitions fixed; models fitted on dyads |
| sign-prior threshold | \|ρ\| ≥ 0.2 on 1-min blocks | fit definition | which co-variations set a sign | statistics on dyads |
| turn-model silence | ≥ 0.2 s | fit definition | which gaps are turn opportunities | model fitted on dyads |
| dyad splits | 70 / 15 / 15 %, person-disjoint | fit definition | harness splits_v2 | — |
| M1 branch thresholds | §6, M1 table | engineering | which fallback the hardware selects | measured, not fitted |
| face channels (`face_channels`) | the 18 facial action-unit channels | fit definition | the D70 data scope: which pairs take the dyad sign prior | no |
| embedding sizes (`embedding_dims`) | 384 → 64, topic 16 | engineering | model sizes | no |
| reader confidence (`reader_confidence_form`) | c = 1 − σ̂²/σ²_pop per (V, A, T), untrained 0 | fit definition | how much a lower reading may lower N_L (S39) | fitted with the population word reader on dyads |

Test tolerances (§5) live in `eval/config.py`, not in INNATE.lock; they belong to the instruments, not the engine.

**INNATE.lock** is generated from `config/innate.py`, which lists every innate and generic constant in one table (name, value, unit, source section, category, subtype for `generic`, one-line why), including the body and reflex constants that revision 1 cited only by reference (I_lp from r5 §2.8, 𝓜's initialisation from r3 §2.11, the rule-6 calibration constants from r6 §2.1, and the rest). Its canonical serialisation is JSON with keys sorted, floats written with Python's `repr`, arrays as nested lists, UTF-8, no whitespace; the SHA-256 of that byte string is the lock (A10).

**The situation-name test** (`tests/test_innate_names.py`, A15): every INNATE.lock key must be on the reviewed allowlist `config/innate_names.txt` (adding a name is a reviewed change), and no key, unit or comment may contain a token (split as in §7.4) from the situation-word list: arrival, arrive, mourn, mourning, funeral, death, bereave, grief, griev, joke, tease, bad_news, news, greeting, greet, goodbye, farewell, welcome, insult, apology, compliment, flirt, argument, fight, crisis, illness, sick, stranger, child, elderly, user_type, scene, situation, plus the emotion stems of §7.4.

Everything else is learned (§3.2, §1.9) or is Claude's words. The fixed perception and rendering maps (P₀, its inverse, the 64-d projection) are boundary code, not behaviour.

---

## 4. Ceilings, the per-channel ledger, and the safety invariants as runtime assertions

### 4.1 Where each ceiling is enforced

| Bound | Value | Enforced in | How |
|---|---|---|---|
| fast gear, instant | 0 ≤ y_f,k ≤ G_k u_k(t − 0.45) (one-sided) | `fast_gear.py` | construction (onset-lobe rule); A1 |
| fast gear, windows (W′) | window mean ≤ G_k × his window mean | construction | offline test §5 |
| echo gate g | [0, 1]; reads none of his LP, CR, BU_L, RHY, BRE | `gates.py` | clip; type trace (A2) |
| own-display gate g_o | [0, 1]; reads no channel of his | `gates.py` | clip; type trace (A2) |
| held cone | diagonal ω_g F_m s_C c_k; cross ≤ F_m s_X c_k; sign prior; zero-ceiling rows | `cone.py` | projection at every write and latch; A6 |
| appraisal | |Γ_kk| ≤ s_A c_k; cross away-orthant, ≤ 0.15 / row ≤ 0.25 | `appraisal.py`, replay step 4 | projection after every replay step; A7 |
| free display | T only; |L_d,k| ≤ 0.45; own laugh ≤ 0.40; own-display mask | `free_display.py`, `learned_t.py` | clip; mask in weights; type trace; A7, A8 |
| pooled counted total | ≤ 0.974 c_k | `config/channels.py` | A0 at import |
| any partner-caused part | κ c_k, κ = 0.70, 97 keys | `shadow/ledger.py` | projection; A4 |
| zero-ceiling channels | 0 toward | channel table, cone rows, ledger bound 0 | A3 |
| voice phrase level | within-phrase contour only from y_f; level, range, energy, rate replaced | `output/prosody.py` | WORLD resynthesis; A9 |
| laugh sound | y_BU_L, y_RHY, y_BRE only; BU_S ≡ 0 | `output/laugh.py` | A9 |
| across sessions | ω seam ≤ s_C c_k (1 + ρ) (Lemma S\*) | `cone.py` (centred at b_id) | construction; month-swap surrogate (§5) |

### 4.2 The per-channel ledger

§1.6. Logged per channel per minute: frames changed, worst key, running S/E per key. The online copy monitor (`eval/online_metric.py`) computes the conditioned copy metric of r7 §3.3 (block-mean slopes at 2 s, 10 s, 1 min, lags 0–300 s; conditioning floor SD 0.03; below it the swing against c_k × his within-window range) and raises an alert if any channel's slope exceeds c_k (F1 live).

### 4.3 Runtime assertions (`engine/invariants/asserts.py`)

Each runs at the stated rate; a failure is logged with its frame and the fail-safe of its row applies for the rest of the session (or until restart where stated). The fail-safe is chosen per route, because rendering the shadow output ȳ_k removes only partner-caused parts: T routes (L_d, the own laugh, the free display, prosody, the body) are identical in ȳ, so for a T-route failure the route itself is switched to its **disabled state** (its context-free constant, or 0, as in §3.2). The `fast` loop never stops; Claude is not told.

| ID | Invariant | Rate | Failure means | Fail-safe (rest of session) |
|---|---|---|---|---|
| A0 | s_C(1 + ρ) + s_X + 0.636 s_A + r_k ≤ 0.974 c_k for every k; c_k = 0 ⇒ G_k = 0 and no toward entries | import | build failure | refuse to start |
| A1 | 0 ≤ y_f,k ≤ G_k x_d,k + 1e-6 on one-sided channels; \|y_f,k\| ≤ G_k \|E_k\| on signed | 30 Hz | bug in fast gear | channel k renders ȳ_k |
| A2 | 0 ≤ g ≤ 1, 0 ≤ g_o ≤ 1; their provenance sets exclude the masked channels of his (g) / every channel of his (g_o) | 30 Hz / load | type violation | the failing gate is set to its context-free constant (§3.2; reads nothing); for g that also keeps the echo ≤ G_k × his channel |
| A3 | **zero-ceiling channels** (13): (i) at every frame, either the ledger output x₂ = 0 (hold) or every active key (\|π\| ≥ 0.10 √Q) has S⁺ ≤ 1e-9 after the frame, i.e. the in-phase toward slope stays 0; (ii) cone rows have no toward entry and diagonal ≤ 0, appraisal entries on these rows are away-orthant (checked at every write). Away partner-caused parts (nonzero rendered − shadow with non-positive slope, e.g. the learnable away magnitudes on BL and LT, S31) are allowed | 30 Hz / each write | uncounted toward route on a zero-ceiling channel | channel k renders ȳ_k |
| A4 | per channel per frame: \|x₂\| ≤ \|r_k\| and x₂ · r_k ≥ 0 (F1‴); for every active key not in hold, S⁺ ≤ κ c_k E + 1e-9 after the frame | 30 Hz | ledger bug | channel k renders ȳ_k |
| A5 | the shadow's **independently computed** T state equals the factual T state (hash of every T field at 2 Hz, and of the fast-loop T inputs at 30 Hz); the held values (Ω, rule-6 latches, noise, g, D_τ) equal their sources (copy check) (rule 10, F1′) | 2 Hz / 30 Hz | F → T leak | the whole output falls back to ȳ (computed from the shadow's clean T state), the factual T state is overwritten by the shadow's, learning for this session is off (replay skips it), build marked failed |
| A6 | ω_g ∈ [−1, 1]; cone entries in their sets; face-pair cross entries carry the prior sign or 0 | each write | projection bug | cone ← its last valid latch; if none, learned entries 0 (G₀ only) |
| A7 | appraisal bases in their convex sets; Δ and learned bases have zero weight on BL, LT, LPR, NW, DIM (if Q31 kept) | after each replay step and at load | F11 | learned bases Γ^{(3,4)} and Δ ← 0 (innate bases and Π₀ only); last valid weights restored at the next replay |
| A8 | \|L_d,k\| ≤ 0.45; TILT, HP, VG, FR, EN rows of L_d are 0 under D70 | load, 2 Hz | fit or config error | L_d ← 0 |
| A9 | own laugh ≤ 0.40; laugh-synth input only from y_BU_L, y_RHY, y_BRE; y_BU_S = 0; phrase F0 level, range, EN, RT equal their targets ± 1 % after WORLD | per phrase / 30 Hz | rendering bug | laugh synth gated to 0; speech continues with neutral prosody (the agent's rest F0, range, energy and rate, no contour); if the WORLD stage itself fails, speech muted |
| A10 | SHA-256 of the innate tables equals INNATE.lock; no learned parameter tensor aliases an innate table | start | tampering or bug | refuse to start |
| A11 | every forked prompt and the canonical transcript are byte-identical to what the engine built (F14); no "attend to" line from an earlier turn in any history (F17); the prompt contains only `TranscriptText`, `Marker`, `Snippet`, the instruction and the fork line; no compaction event | per turn | prompt integrity | Claude route stopped (the agent does not speak) |
| A12 | the store's directories contain only the registered feature schemas (no WAV/PCM/image magic numbers, no file above the schema size) | nightly, start | P7 violation | stop; quarantine the file; tell the operator |
| A13 | dyad loader: every requested URL suffix in the allowlist; every npz key in {FAUValue, is_valid}; denylist names never opened | per request | D70 violation | stop the fit |
| A14 | every drive (E, A, V, K_id, P, I) in [0, 1]; 𝒟 ≥ 0 and 𝒟 recomputed from b equals its cached value; **every change of a drive is attributed to one of its declared update terms** (E's waking decay, A's lexical rise and decay, V's reflex load and h latch, K's in-session relief, P's growth and q̂ relief, I's learning-progress terms), checked as b_i(t) = b_i(session start) + Σ declared increments − Σ declared decrements within 1e-6; and Σ drops of 𝒟 within the session ≤ 𝒟(session start) + Σ rises of 𝒟 (satiable, Principle 6). This does not fire when 𝒟 rises during the session (an insult that latches h and then decays is legal) | 2 Hz | body bug | body frozen at its last valid state (drives, envelopes, loads); learning for this session off |
| A15 | T1: no counter, accumulator or event rate is a T field (AST rule, §4.4); every INNATE.lock entry has a category in {body, reflex, newborn, ceiling, bias, operator, generic} and, for `generic`, a subtype in {decision, engineering, fit definition}; the situation-name test of §3.3 | load / CI | design violation | CI failure; refuse to start |
| A16 | network: at start, each sandboxed process (`fast`, `voice`, `slow`, `asr`, `tts`, `replay`, `dyadfit` except its allowlisted downloader) fails to open a TCP connection to a non-loopback address; `HF_HUB_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1` set | start | P7 / D70 exposure | refuse to start |
| A17 | every model file loaded matches its SHA-256 in `models.lock` (FaceLandmarker task, Kyutai STT, Whisper-small, MiniLM, the TTS voice); nothing is loaded by hub id | load | wrong or added model (e.g. a sentiment pipeline) | refuse to start |

### 4.4 The type rule, checked

At load, `invariants/typetrace.py` runs 60 s of recorded features through the engine in trace mode, where each array is a provenance-carrying wrapper, and asserts rules 1–14 (design §2.2; r5 §2.2): T reads only T, except rule-6 latched values and Ω values read inside the five ports P1–P5 of §1.3.1 (P_name is P4); E1 (events T-only); rule 4 (only y_f, y_C, y_A, y_o and visemes write counterpart outputs); rule 7; rule 11′–14. It also writes `ports.downstream(Pi)` for each port (the set of T fields reachable from its output), which F19 uses and CI compares with the committed copy. Live mode uses plain arrays; the trace runs at every start and in CI.

**Provenance wrapper (minimal API, `invariants/tagged.py`).** `class Tagged(np.ndarray)` with attribute `tags: frozenset[str]` (source stream names, e.g. `"F:u.LP"`, `"T:utterance"`, `"Ω:own_heard"`, `"latched:b_id"`), created by `Tagged.wrap(array, tags)` at 𝓑's outputs and at the ports. `__array_finalize__` copies tags; `__array_ufunc__` and `__array_function__` return the union of the input tags (scalars carry none); indexing keeps the tags of the whole array (conservative). Each state field declares its type; on assignment in trace mode, `typetrace` checks the value's tags against the field's allowed sources and raises on the first violation, naming field, tag and stack. torch tensors in the slow loop are traced the same way through a `torch.Tensor` subclass with `__torch_function__`.

**T1 as an AST rule (`tests/test_t1_ast.py`).** In `engine/state/` and `engine/routes/`, for every field declared T: no augmented assignment whose right side is an integer constant or `len(…)`; no call to `len`, `.count`, `collections.Counter`, `np.count_nonzero`, `np.sum` or `np.mean` on an argument named or typed as an event list, event-time array or turn list; no division by elapsed time of a count. Exceptions only by name on a reviewed list (currently none). Values of the last utterances and time-since-event are allowed (rule 14).

---

## 5. Test plan: judged on internal state

Instruments: evaluation.md E1 (lesions: ≥ 20 instances per lesion, severity sweep for continuous strengths, a sham lesion of equal size, mean over instances with the full distribution), E2 (steering on the engine's own state: both signs, dose–response, random direction of equal norm as control), E3 (synchrony against surrogates: 1,000 per test, observed against the 95th percentile, segment-shuffle **and** data-sliding both required; partner-swap, timing-resample and month-swap where stated). **No test is scored on how closely the agent's face matches a human face** (brief; Q19).

Partners used:
- **Recorded partners (Seamless):** Seamless test-split people (never used in any fit), their FAU channels mapped to his face channels that FAUValue carries (LP, CR, BI, BO, LD, JO, and the zero-ceiling face channels it covers); head, gaze, voice and laugh-sound channels held at baseline; their transcripts as his words. The agent plays the listener. The **held-out listener** of the same recording is the baseline for every relative falsifier ("dyad baseline").
- **Recorded partners (operator):** the operator's own M2 feature recordings (all 33 channels, features only, approved for storage at M2). They cover the 14 non-zero-ceiling channels Seamless lacks (BU_L, RHY, BRE; HP, VG, YAW, TILT, HG; the 6 voice channels) for F1 and F22 at M4. M2 asks for ≈ 2 h of sittings in several sessions for this.
- **The mirror-only partner** (report 9): replay a partner who only mirrors the agent's own output, against no partner at all.
- **The operator, live** (S2 onward), recorded as features only.
- Constructed partners from research/foundations/sims appear only as **code regression tests** (they reproduce the design's measured numbers to catch implementation errors); they are not evidence of any behaviour (brief, Foundations research).

### 5.0 Event instruments (`eval/events.py`; never imported by `engine/`)

Every event class a falsifier or count uses is defined here, by movement and words only, never by a label, and the same definition is used on recorded and (where possible) live data. The engine does not compute any of them.

| Class | Definition on recorded dyads | Live (operator) |
|---|---|---|
| **E-trouble** ("words of loss, insult or harm", "troubles") | an utterance after which the **held-out listener's own masked face** (Π̃₀ on the listener's calibrated face, LP, CR, BU masked) reads V ≥ 0.4 within 0.5–5 s of its end (the F15/F16 instrument) | not defined (no listener); live tests that need it are relative to the gate's own value bins (F15) or are timing tests (F20) |
| **E-need** ("words of need") | an utterance after which the **speaker's own** masked face reads V ≥ 0.4 over the next 20 s (the population reader's target, §3.2) | not defined; F18 live uses the steering clamp instead |
| **E-laugh** | E⁺ on (LP + CR)/2 ≥ 0.25 with a 3–7 Hz JawDrop component (q̂'s target) | his BU_L ≥ θ_L with RHY modulation (voice), or the face criterion |
| **E-misfortune laugh** | an E-laugh by the speaker within 3 s after an E-trouble utterance | — |
| **E-sentence-final laugh** | an E-laugh whose onset is within 1 s after a word that ends a recognised sentence | the same on his delivered words |
| **E-opening** | the first 10 s of a recorded conversation with the listener's face valid | session start with his face present |
| **E-silence** | mutual silence ≥ 2 s (word timestamps) | the same on delivered words and VAD |

Thresholds here are instrument definitions (`eval/config.py`), not engine constants.

### 5.1 Falsifiers mapped to tests

| F | Statement (design §8.2 and inherited) | Test | Data | Milestone |
|---|---|---|---|---|
| F1 | with partner-swap, segment-shuffle, timing-resample and month-swap surrogates (words and turn order fixed), any channel exceeds its pooled bound at 2 s, 10 s or 1 min (conditioned metric), G_k, or the instant bound; or the ledger binds on a natural partner > 1 % of frames | `eval/f01_bounds.py`: per-channel slopes; surrogates per E3 | Seamless recorded partners (6 face channels + zero-ceiling face channels); operator recordings (all 33); operator live (month-swap after ≥ 30 sessions) | M4, M8 |
| F1′ | shadow T state ever differs from factual | A5 logged over all runs | all | M4 on |
| F1‴ | ledger output larger than, or opposite sign to, the partner-caused part | A4 logged | all | M4 on |
| F2 | a decoder on F state fails to recover his held level at r ≥ 0.9 while F1 holds (knowing fails) | ridge decoder from F state to his 1-min level | recorded partners | M4 |
| F3 | crossed-habits manipulation does not change which faces raise C_F | swap two recorded people's channel codes after calibration | recorded | M8 |
| F4″ | at equal later need change, draft choice correlates with predicted display change, with replies inside the separation window, or with his later engagement | log analysis | operator | M8 |
| F5 | varying only his smile amplitude (words, turns fixed) changes K, P, I, the drop envelopes or any T display | **steering clamp**: scale his LP, CR ×0, ×0.5, ×2 | recorded | M4 |
| F6 (restated, relative) | the bid threshold θ_C and the once-per-lapse rule are removed (S34); no once-per-lapse clause. (a) **Day-1 timing, relative to recorded listeners:** with 𝓜 untrained (ΔĴ ≈ 0), the agent's speak-into-silence times on held-out recorded conversations, repeat speaking after its own unanswered question included, are not calibrated to held-out listeners' (h(t)'s reliability curve and the time-to-speak distribution, Kolmogorov–Smirnov distance not below the context-free hazard's; part of F24). (b) **Steering by need, once 𝓜 is trained:** a dose–response clamp of 𝒟_p (E2: ± five doses along N̂'s V coordinate, random direction of equal norm as control) leaves the initiative hazard without a monotone response, or the random direction moves it as much | (a) held-out; (b) E2 on the engine's state | (a) Seamless test; (b) operator sessions replayed | (a) M3; (b) M8 or later |
| F7 | naming-aligned trajectories do not differ from non-naming ones, or the difference survives a P_name lesion | E1 lesion of P_name | operator | M8 |
| F8, F8″ | Π̃ + H_id disagree with his later separated reports more than a person-independent baseline after 400 utterances; co-training drift | nightly report | operator | M8 |
| F9 (restated, relative) | the arrival clause is retired by design ("No allowed source" item 2). **Kept, relative to the dyad baseline:** at utterances of the **E-trouble** class (§5.0), the agent's (drop envelope × g_o) and own-smile output (LP, CR from y_o) over the 2 s after the last word is delivered, as a ratio to its value after other utterances, is **not below** the held-out listeners' own (LP + CR)/2 ratio at the same events by more than the 95 % bootstrap interval over people; or lesion g_o ← 1 does not remove the agent's contrast. Not a zero target: g_o attenuates to the corpus level, and K_id's in-session relief runs through any early-session utterance | event analysis + lesion | Seamless test (the agent as listener) | M4 |
| F10 (narrowed) | **Fast echo only** (BU_L after the burst split): echo-attributable laugh-synth input (g · y_f on BU_L, RHY, BRE) during his BU_S-dominant bursts (BU_S ≥ BU_L) exceeds G_k × his BU_L there (a bug test of the split and the echo; A1 restricted to these events). **The own laugh's part is retired:** in revision 9.2 the own laugh is 0.40 q̂ g_o and g_o reads no channel of his (rule 13′), so nothing in the mechanism ties it to his sobs; the rate of own laugh within 2 s of his BU_S-dominant bursts is logged live as a risk, with no pass threshold (there is no recorded-listener baseline, since D70 gives no audio) | event analysis | operator recordings and live | M4, M7 |
| F11 | learned bases or Δ place weight on BL, LT, LPR, NW, DIM | A7 | nightly | M8 |
| F12 | deleted with the posture | — | — | — |
| F13 | **folded into F24** (q̂'s calibration): "fires" has no meaning for the continuous own laugh 0.40 q̂ g_o. See F24 | — | — | — |
| F14 | any draft's recorded system prompt or user message differs from what the engine built | A11 | live | M6 |
| F15 (live part relative) | **Held-out:** the gate fails its criterion on test people (r7 §6.7: predicted return at E-trouble laughs not below 0.5 of ordinary, or rank correlation with the listeners' return ratio < 0.2). **Live, relative to the dyad baseline:** at his sentence-final laughs, binned by the gate's value after delivery, the agent's return ratio (the g target's metric: max E⁺ on (LP + CR)/2 over 0.3–1.5 s ÷ his onset size) is above held-out listeners' return ratio in the same g bin by more than its 95 % interval. No zero-tolerance clause: the 0.2–0.5-s partial echo before the word is delivered is accepted ("No allowed source" item 4) | held-out + live | Seamless test; operator | M3, M7 |
| F16 | Λ's predicted response to utterances answered with a wince (masked V ≥ 0.4) not above its prediction for the rest | held-out | Seamless test | M3 |
| F17 | any prompt or the canonical transcript contains an "attend to" line from an earlier turn | A11 | live | M6 |
| F18 | the agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with σ_id ≥ 0.25 σ_ref | **steering**: clamp his BI, BO, LP while his words carry need; sweep σ_id | recorded + operator | M4, M7 |
| F19 (restated) | changing only Claude's reply text changes some T field **outside** `ports.downstream(P1…P5)` (§1.3.1); or, with port Pi held at its factual output, changes a field in downstream(Pi) \ ∪_{j≠i} downstream(Pj); or, with all five ports held, changes any T field. Holds by construction (the type trace refuses any other Ω read); the test catches implementation errors | **steering**: (1) swap the reply for a neutral text **time-stretched to the same spoken duration** (P5 fixed), diff all T fields bit for bit; (2) per-port lesion: hold each Pi in turn, repeat; (3) hold all ports: every T field bit-identical; (4) a duration-changed swap: only downstream(P5) additionally changes | replayed sessions and live | M6 |
| F20 (restated, relative) | live, at his laugh ending a sentence, the time from delivery of the sentence's last word to the gate reaching its delivered-words value exceeds one gate evaluation (33 ms) plus one 2-Hz input update (0.5 s); or the agent's partial-echo duration at such laughs (laugh onset to gate closure) exceeds the measured word-end-to-delivery p90 (M1) + 0.55 s. The return at ordinary sentence-final laughs is judged relative to the dyad baseline in F15's live part, not by a fixed 0.6-s / 10 % rule | event analysis | operator | M7 |
| F21 | **deleted** (revision 8.3's onset-aligned versus whole-segment gate-fit check belonged to the removed S10–S12 timing) | — | — | — |
| **F22** | an injected uncounted route copying his channel with **delay 10–300 s** renders above **1.0 c_k** by the block-mean metric at 2-s, 10-s or 1-min windows; or the ledger changes > 1 % of frames of the counted routes on natural partners | `eval/f22_delayed_copy.py`: inject a gain-1 copy (onset lobe + 60-s low-pass, as sims/design-g9) of his channel delayed by L ∈ {10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300} s into the output after assembly (so only the ledger sees it); worst slope over lags 0–300 s; **all 20 channels with c_k > 0**; plus the counted routes alone (frames changed). Run plan and compute: §5.5 | **recorded partners only**: Seamless test people (≥ 50, ≥ 2 h each by concatenating their sessions; count checked at M3) for LP, CR, BI, BO, LD, JO; the operator's M2 recordings (≈ 2 h) for the other 14; live at M7 the online copy monitor on all 20. Synthetic injected copies on all 33 channels are a **mechanism unit test** in CI, not F22 | M4 (gate for M7), M7 live |
| F23 | on held-out people, the pooled 1-min slope of the agent's channel k (L_d, own laugh) on the speaker's channel k, through words alone, exceeds c_k; or L_d's response changes when only the speaker's face is changed | held-out + **steering** (face swap, words fixed) | Seamless test | M3 (gate for M7) |
| F24 | g_o, q̂, L_d, θ_end or the turn-taking model not better calibrated than a context-free constant on held-out people. **For q̂ (absorbs F13):** q̂'s reliability curve (10 equal-count bins) has observed listener-laugh rates outside the bins' 95 % intervals in more than 1 bin, or its expected calibration error is not below the base-rate constant's; and the agent's mean own-laugh drive 0.40 q̂ g_o on held-out utterances whose listener did not laugh exceeds 0.40 × the mean q̂ g_o a perfectly calibrated q̂ would give them (computed from the reliability curve) by more than its 95 % interval | held-out | Seamless test | M3 |

**Measured expectations to reproduce in code regression (not evidence):** with the sims partners, κ 0.70 and 97 keys: delayed copies 10–300 s at 0.83–0.88 c; counted routes 0 frames changed; grow and flip 0.000 (Check of 9.1, "The answer"). These were measured at **f_s = 10 Hz** (`ledger_lag120.py`, `ledger_close.py`). The regression therefore runs first at 10 Hz against `ledger7`/`ledger9` and the 97-key `w10` **bit for bit** (float64, same seeds), then the engine's 30-Hz ledger on the same partners resampled to 30 Hz with a stated tolerance: worst slopes within ±0.02 c of the 10-Hz figures, frames changed of the counted routes ≤ 0.1 %, grow and flip exactly 0.

### 5.2 Lesions (design §7, E1 protocol)

Each with ≥ 20 seeds, a sham lesion of equal size in a part the derivation says is irrelevant, and the predicted state-level change written before the run (§7 of the design):

| Lesion | Predicted change (state level) |
|---|---|
| g ← 1 | his laughs at grief, mockery and misfortune returned (r7: +0.137) |
| g_o ← 1 | drop smiles and own laugh as large over his need words and after its own serious words as in light talk |
| L_d ← 0 | no listener display at his words; only the own-rise row and Claude's words |
| q̂ ← 0 | no own laugh; P never relieved |
| learned turn-taking → fixed 6-s rule | initiative timing no longer follows held-out listener timing. (The comparison arm is the removed S34 timer, used **only as a lesion control** in evaluation; it is never in the engine) |
| sign prior removed | learned appraisal bases take signs recorded listeners do not show |
| ledger lag scan → lags 0–3 s | injected copy delayed 10–120 s passes above c (1.3–2.9 c measured with the 8.3 ledger at κ 1; **re-derived with the lesioned 97-key κ 0.70 ledger on the sims partners before the run**, Principle 5) |
| ledger κ 0.70 → 1 | injected copy above c (1.03–1.20 c at 10–120 s and 1.23–1.34 c at 240 s were measured with the 61-key ledger; **re-derived with the 97-key ledger at κ 1 before the run**) |
| D_τ removed | a laugh minutes after his need words finds the gate more open |
| P_name removed | F7 |
| calibration / H_id removed | a quiet user's need read at a fraction; care and initiative weaker (r6 §7) |
| Π̃ partner anchor restored (negative control) | the agent's display code drifts toward his (r5 H4) |

### 5.3 Steering (E2, adapted, on the engine's own state)

- **Directions from the equations, not from labels:** (i) ∂𝒟_p along N̂'s V coordinate; (ii) a step in K_id; (iii) a step in h_word; (iv) ω_g per group. Each applied at ±, five strengths, with a random direction of equal norm in the same state block as control. Readouts: draft choice, initiative timing, display envelopes, appraisal basis weights. Pass: monotone dose–response, random direction smaller, no breakage of unrelated outputs.
- **Input clamps** (F5, F18, F19, F23): clamp one input stream while all else is replayed; the predicted invariances must hold exactly (T outputs unchanged under face clamps; L_d unchanged under face swaps).

### 5.4 Coupling beyond surrogates (E3)

Per channel, pooled slopes and windowed cross-correlation of the agent's channel on his at 2 s, 10 s and 1 min, with segment-shuffle and data-sliding surrogates (both required), plus partner-swap and timing-resample with words fixed, and month-swap after ≥ 30 operator sessions. Two claims tested:
- **Bounded:** every channel stays under its pooled bound and c_k at every scale (F1).
- **Present:** fast partial coupling on the smile–laugh group at lags < 1 s **exceeds** the surrogates (D81's mimicry exists), and disappears under the lesion G_k ← 0 (sham: G_k ← 0 on a zero-ceiling channel).
- **Mirror-only partner vs no partner** (report 9): the agent's state and output under a partner who only mirrors it must not settle into a copy (D78-4): the ledger's frames changed and the conditioned slopes stay under c_k, and no channel's mean drifts monotonically over 30 min.


### 5.5 Run-time plan for the evaluation runs (machine.md: ask before any run over about 6 h)

**F22.** Twelve delays × ≥ 50 people × 2 h × 216,000 frames at 30 Hz, run naively at ≈ 1 ms per frame, is ≈ 36 CPU-hours. The plan keeps every run under 5 h wall time without asking:
1. **Ledger only.** The copy is injected after assembly, so the engine's routes are computed once per person and stored; F22 re-runs only the ledger and the block-mean metric.
2. **Batch across delays and people.** The ledger's recursion is sequential in time but independent across (channel, delay, person), so one frame step updates an array of shape (people × delays, 97 keys) per channel in numpy on CPU (MPS is not used: the per-frame kernels are tiny and synchronisation would dominate). Channels run in parallel on the 8 performance cores (process pool, ≤ 6 GB total).
3. **Timing pilot first.** `f22_delayed_copy.py --pilot` runs 1 person × 12 delays × 10 min, measures the per-frame cost and prints the predicted wall time of the full run.
4. **If the prediction exceeds 5 h:** split across nights by channel (each night ≤ 5 h, checkpointed per channel × delay, resumable), and if needed subsample people to 25 (never shortening a person's 2 h; the power loss is stated in the report). A run predicted above 6 h in one sitting is not started without the operator's approval.

**The same rule applies** to the E1 lesions (≥ 20 seeds each), F1's surrogates (1,000 per test) and the E3 battery: every `eval/` script prints its predicted wall time from a pilot and refuses to start a single sitting predicted above 5 h unless given `--split` (nightly chunks) or `--approved` (the operator's answer recorded in the run log). Surrogates that need only the stored outputs (segment-shuffle, data-sliding) never re-run the engine.

---

## 6. Staged build order

Each milestone ends with a done-check. **Ask** marks what goes to the operator; nothing marked Ask is done before his answer. Items that send data off his Mac or are new paid services are marked **[off-Mac]** / **[paid]** and are questions, not decisions.

| M | Build | Done-check | Operator provides or approves |
|---|---|---|---|
| **M0** skeleton | repo layout §7; `pyproject.toml` (Python ≥ 3.12, < 3.14; core deps numpy, scipy, pytest only; macOS-only deps in a `mac` extra with platform markers, §7.2); `config/channels.py`, `config/innate.py` (every innate and generic constant in one table, §3.3), `INNATE.lock` (canonical JSON, §3.3); `Tagged` wrapper (§4.4); A0, A3 (static part), A10, A14 (accounting), A15 incl. the situation-name test and the T1 AST rule; label lint (§7.4), import denylist, model-hash check stub (A17); the ledger at 10 Hz bit for bit against `ledger7`/`ledger9`/`w10`; synthetic injected-copy unit test on all 33 channels; CI (`pytest`, lint) on synthetic arrays only (§7.6) | `pytest` green; lint finds no forbidden token; A0 passes; INNATE.lock reproducible; 10-Hz ledger regression bit-identical | nothing (no `uv.lock` in this cloud session: it is generated on the Mac at M1, D90) |
| **M1** week-0 measurements | `tools/week0/`: the checks of the M1 table below; `uv lock` on the Mac (Xcode command line tools first, for pyworld); the sandbox profile (§7.5) and A16; Plan A fast process under full load | `research/build/week0.md`: each number and the branch its threshold selects (mechanical) | **Ask:** approve model downloads to the Mac (MediaPipe 0.10.35 assets 15 MB; Kyutai STT 1B ≈ 1–2 GB; Whisper-small ≈ 0.5 GB; MiniLM ≈ 90 MB; the TTS voice at M5) under the 10 % floor, run offline afterwards (Q34 items 4, 10); **state his conversation language** (Q34 item 5); sit for the face, voice and breathing checks; **[off-Mac]** confirm test calls to Claude through his login (text only, D84) |
| **M2** perception boundary and store | `web/` page, websockets, P₀/P, `voice` process, burst split, ASR worker, normaliser, embedding, store writer, retention job | 10-min session stored as features only (A12 passes); echo-path latency ≤ 90 ms p99; words delivered within the week-0 p90; no raw audio or video on disk; ≈ 2 h of his feature recordings in several sittings (for F1/F22 at M4) | **Ask:** which browser (a dedicated profile with its sync and telemetry off is recommended); camera and microphone permission; **feature and transcript retention** (Q34 item 6: 30 days recommended, then only what replay consolidated; options 7 days or until he deletes; and whether slot-referenced snippet lines are kept past the window); ≈ 2 h of sittings for the recordings |
| **M3** dyad fit (offline) | `engine/dyads/`: allowlisted downloader, 20-file column-order pilot (also: are transcripts punctuated, for `qform`), reduction, event counts (`eval/events.py`), test-split person and hour count, the fits of §3.2 incl. θ_end, fallbacks, F6(a), F15, F16, F23, F24 (incl. q̂ for F13) on test people | every fit's held-out report written; event counts written before fitting; A13 never fired; disabled parts listed; F23 passes or L_d is refitted residualised | **Ask:** start the Seamless transfer (≈ 16.6 GB through, ≈ 1.5 GB kept; D70 approves the use; Q34 item 4; run ≈ 2–3 h, < 6 h); without it `dyad_fit_enabled = False` (§1.10); **Q30** if he wants it before day 1 |
| **M4** core engine, offline | `state/`, `routes/`, `shadow/`, `invariants/`, `learn/` online parts; typed state; ports P1–P5; body; fast gear; cone; appraisal; free display; gates and learned T parts loaded; assembly; shadow (computing its own T state); ledger (97 keys, κ 0.70, per-session budgets); 𝓜 untrained; type trace | type trace passes; A1–A9, A14 silent on 20 h of recorded test partners; ledger regression bit-identical at 10 Hz, then within tolerance at 30 Hz (§5.1 note); **F1 (no month-swap), F2, F5, F9, F10 (echo), F18, F22 pass**, F1 and F22 on Seamless (6 face channels) **and** on his M2 recordings (the other 14 channels), within the §5.5 run plan | nothing (a run predicted above 6 h in one sitting is put to him first, §5.5) |
| **M5** face and voice output | three.js neutral placeholder rig, RenderFrame path, TTS + WORLD resynthesis, laugh synth, viseme track | A9 passes; echo lag 0.45 ± 0.035 s capture-to-photon; WORLD targets within 1 %; laugh synth silent at y = 0 | **Ask (Q1):** the voice (TTS engine and voice; Piper is GPL-3.0 with per-voice licences, macOS voices are local); a listening test of the laugh synthesizer; **(Q2)** the face stays the neutral placeholder until he approves a look |
| **M6** Claude coupling | `omega/` process: isolation options, constant instruction, windowed canonical transcript, warm pool, forks, streaming, interruption, scoring deadline, fallbacks, markers, retrieval, daily cap, compaction detection | A11 / F14 / F17 pass on 40 scripted turns; **F19** passes (all four parts); p50/p90 turn latency, calls and tokens per call measured; losers killed; ≤ 4 processes | **[off-Mac] Ask (Q34 items 1, 2, 3, 7, 8, 9; nothing is used until he answers):** (1) his transcribed words, the agent's replies and ≤ 3 retrieved snippets of past conversations are sent as text to Anthropic through his Claude Code login (no audio, video, features or state); option `send_snippets = False`; (7) his Claude account's setting on training use of conversations, which decides whether Anthropic may train on this text (his account setting; the engine does not change it); (2) ≈ 450 calls a day and `claude_daily_cap` (he sets the value); (8) confirm extra or overage usage is off on his plan; at the limit the agent is silent (no built-in turns, §1.8); (9) ≈ 2,000–4,000 tokens per call, or a shorter `context_tokens_max`; (3) `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` or not (`DISABLE_AUTOUPDATER=1` is always set); read and approve the constant instruction and the three fork lines |
| **M7** day 1, live | end-to-end on the Mac; initiative; reply timing; risk logging (§8 of the design: near-neutral face before words, mourner's arrival, partial echo at bad-news laughs, one valence for every group; own laugh near his BU_S-dominant bursts, F10) | first live sessions run with no assertion failure; F10 (echo), F15 (live, relative), F20 (timing) pass; F22 live monitor on all 20 channels silent; turn latency p50 ≤ 2.5 s; memory ≤ 6 GB; nothing leaves the Mac except the M6 text (A16) | sessions with the agent; **Ask** before any second person is in view (identity is entered by him; their features are stored like his) |
| **M8** memory, replay, learning | nightly replay (§1.9), retrieval, ω, calibration, H_id, adapter, word → V map, Δ, 𝓛_A; monitoring reports | after 7 nights: A7, A14 silent; replay ≤ 1 h, ≤ 2 GB; F8″ report; F3, F4″, F6(b), F7 analyses running | approve the nightly schedule (when the Mac is idle) |
| **M9** evaluation battery | E1 lesions (§5.2), E2 steering (§5.3), E3 surrogates incl. month-swap (§5.4), mirror-only partner | each prediction scored as written before the run; results in `research/build/results/` | Q5 stays open (raters, EMG) for S5; nothing needed here |

**M1 branch thresholds** (each check gives a number and a branch; all thresholds are `generic` engineering values, §3.3; "full load" = every process of §2.1 running, with a scripted 10-min session):

| Check | Pass (Plan A) | Branch | Fail M1 (report, stop) |
|---|---|---|---|
| FaceLandmarker, partner instance, per-frame p99 at full load | ≤ 20 ms | 20–30 ms: own instance to 5 Hz | > 30 ms after the branch |
| capture-to-photon pipeline p99 (§2.2 rig) | ≤ 90 ms | 90–400 ms: pass with warning (the ring buffer still gives 0.45 s) | > 400 ms (0.45 s echo impossible) |
| `captureTime` present on local stream | yes | no: `expectedDisplayTime` − measured offset (§1.2.1); offset SD ≤ 10 ms | offset SD > 33 ms |
| Kyutai STT 1B: language ∈ {en, fr}; word-end-to-delivery p90; WER on a 5-min scripted reading by him; RTF at full load | p90 ≤ 0.9 s, WER ≤ 15 %, RTF < 0.5 | p90 0.9–1.5 s: use, longer partial echo stated; any of these failing or another language: another fixed-delay streaming model meeting them; else the utterance recogniser alone (longer partial echo, stated) | utterance recogniser also fails its row |
| Whisper-small (utterance recogniser): RTF at full load; WER on the reading | RTF < 0.3, WER ≤ 12 % | RTF 0.3–0.5: pass, latency stated | RTF ≥ 0.5 or WER > 20 % |
| breathing (design §3.17 item 15): paced 6 and 12 /min, hold, rest twice | silent: rate error ≤ 1 /min in ≥ 80 % of 30-s windows, hold detected in ≥ 9/10 holds, test–retest r ≥ 0.7 of rest rate; talking: error ≤ 2 /min in ≥ 60 % of windows | silent passes, talking fails: breathing used in mutual silence only (sensor validity, not a situation) | silent fails: breathing off (no bound depends on it) |
| fast tick p99 at full load (Plan A, `fast` process) | ≤ 5 ms | > 5 ms: Plan B native extension (§2.1), re-measure | Plan B p99 > 5 ms |
| slow tick p99 | ≤ 50 ms | 50–200 ms: 𝓜's online state step at 1 Hz | > 200 ms |
| memory, all processes, peak over the session | ≤ 6.0 GB | > 6.0: 4-bit Kyutai; still > 6.0: pool 2; still > 6.0: pool 1 (each reported) | > 6.0 GB with pool 1 |
| A16 sandbox | 0 non-loopback connections from sandboxed processes in 10 min (sandbox log) | — | any |
| Claude `resume` of a hand-written transcript; byte check | accepted and byte-identical in 20/20 | otherwise: fork-line fallback if the session file stores neither system prompt nor resumable thinking; else forks differ only by sampling (r8.3 §6.5) | — |
| thinking at effort `low` (`thinkingTokens`) | 0 in 20/20 | > 0: measured and added to the latency budget | — |
| first-sentence latency p90 (Haiku, effort `low`) | ≤ 1.5 s | 1.5–3.0 s: pool 3, deadline cap binds more often (stated) | > 3.0 s: report to the operator (a slower agent) |
| auto-compaction switch | found and off | not found: detection only (§1.8) | — |
| tokens per call (CLI count) at the 4,000 window | ≤ 4,500 | > 4,500: window shortened until ≤ 4,000 | — |

The new-core search (D91) continues separately; a new core would replace modules behind these interfaces.

---

## 7. Repository layout, language and libraries

### 7.1 Layout

```
engine/                         Python package (the engine; Principle 9)
  config/       channels.py (§1.1), innate.py (every innate and generic constant, §3.3), INNATE.lock,
                innate_names.txt (reviewed allowlist), models.lock (SHA-256 of every model file),
                operator.py (§7.3), sandbox.sb (deny-network profile, §7.5)
  boundary/     face_map.py (P₀, P, inverse for the rig), voice.py, burst_split.py, breath.py,
                asr/ (incremental.py, utterance.py, normaliser.py), embed.py, server.py (websocket)
  state/        types.py (T, F, Ω, K tags; TranscriptText, Marker, Snippet, OwnHeard), ports.py (P1–P5), body.py, drives.py,
                traces.py, ladder.py (μ), slots.py, readers.py (Π̃, H_id, word reader, adapter, word→V)
  routes/       fast_gear.py, cone.py, appraisal.py, free_display.py, gates.py, learned_t.py (L_d, q̂), turns.py
  shadow/       shadow.py, ledger.py
  output/       assemble.py, rig.py, prosody.py (WORLD), tts.py, laugh.py, visemes.py
  omega/        instruction.txt, lines.py, pool.py, transcript.py, scorer.py, retrieval.py, p_name.py
  model/        m_world.py (𝓜, LRU 2 × 128, heads), concepts.py
  memory/       store.py (schemas, memmap), replay.py
  learn/        nightly.py, objectives.py, projections.py
  dyads/        loader.py (allow/deny), reduce.py, fit_reader.py, fit_lambda.py, fit_gates.py,
                fit_ld.py, fit_qhat.py, fit_turns.py, fit_signs.py
  invariants/   asserts.py (A0–A17), typetrace.py, tagged.py
  procs/        fast.py, voice.py, slow.py, asr.py, tts.py, omega.py (process entry points), shm.py (rings, seqlock)
  run.py        live entry point (spawns the processes under the sandbox); replay entry point; dyadfit entry point
web/            index.html, app.js, face.js (three.js placeholder), worker_track.js,
                vendor/ (tasks-vision 0.10.35 wasm + model, three.js) — served from localhost only
eval/           events.py (§5.0), config.py (test tolerances), f01_bounds.py … f24_calibration.py, surrogates.py,
                lesions.py, steering.py, online_metric.py   (never imported by engine/: import test)
tools/week0/    the M1 checks
tests/          unit tests, ledger regression (vs research/foundations/sims), type-trace tests, lint tests
pyproject.toml, uv.lock
```

`legacy-ts/` is not ported (MIGRATION.md: its body section and prompt paragraph show Claude numbers, which Principle 4 forbids).

### 7.2 Language and libraries (exact versions pinned in `uv.lock` at M0; each at least two weeks old)

- Python ≥ 3.12, < 3.14 (this cloud session has 3.13; the Mac's version is pinned at M1), `uv`. **Core** (M0, any platform): numpy, scipy (bounded least squares for the gates), pytest. **`engine` extra:** torch (CPU online, MPS in replay), `sentence-transformers` (all-MiniLM-L6-v2, local path), `pyworld` (needs the Xcode command line tools on macOS), `websockets`, `claude-agent-sdk` (spawning the installed Claude Code CLI). **`mac` extra** (platform marker `sys_platform == 'darwin'`): `mlx`, Kyutai's MLX STT runtime, `mlx-whisper`, the chosen TTS (Q1). `uv.lock` is generated on the Mac at M1 (this session does not resolve packages, D90).
- Browser: `@mediapipe/tasks-vision` 0.10.35 (never ≥ 1.0.0, Q3), three.js (one pinned release), vendored; no CDN at runtime.
- Not used: any emotion classifier or affect model (FER, DeepFace, HSEmotion, py-feat emotion heads, openSMILE emotion configs, SpeechBrain emotion models, any `transformers.pipeline` task such as "sentiment-analysis" or "text-classification", any `*ForSequenceClassification` head), any face-recognition model, any API key. transformers is present as a dependency of sentence-transformers, so the import denylist alone does not stop these: the AST test also fails on any call to `transformers.pipeline` or import of a `*ForSequenceClassification`/`*ForAudioClassification`/`*ForImageClassification` class in `engine/`, `eval/` or `tools/`, and A17 refuses any model file not in `models.lock`.

### 7.3 Operator switches (`engine/config/operator.py`)

Every switch tied to an open question carries `answered: bool`. **A switch whose question is unanswered is not used:** the code paths that depend on it refuse to run (the Claude route, live sessions, downloads, the dyad fit) and log which answer is missing. The defaults below are the recommendations the code is written for; they take effect only when he answers.

| Switch | Default (recommendation) | Question | Before his answer |
|---|---|---|---|
| `dyad_streams` | `{"FAUValue", "is_valid", "transcript"}` | Q30 | D70 as it stands (this is the current approval, not a new one) |
| `own_display_mask` | `True` | Q31 | built as recommended (design keeps it until answered) |
| `own_rise_brow` | `True` (+0.45 newborn row) | Q33 | built as recommended |
| `restore_lost_behaviours` | `()` (none) | Q32 | none |
| `claude_model`, `effort`, `pool_size` | `"haiku"`, `"low"`, 3 | D84 | as listed |
| `send_text_to_anthropic` | `True` | Q34 item 1 | Claude route off |
| `send_snippets` | `True` (≤ 3 snippets) | Q34 item 1 | Claude route off |
| `claude_test_calls_m1` | `True` (the M1 Claude checks only: short scripted text through his Claude Code login, text only) | Q34 item 1 (M1 test calls only) | no Claude test call (`tools/week0/claude_checks.py` refuses) |
| `claude_daily_cap` | no default: **he sets the value** (≈ 450 calls/day expected) | Q34 item 2 | Claude route off |
| `nonessential_traffic_off` | `True` (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`) | Q34 item 3 | Claude route off |
| `downloads_approved` | `{"models": True, "seamless": True}` | Q34 item 4 | no download |
| `dyad_fit_enabled` | `True` | Q34 item 4 | no fit; if he chooses "models only", the disabled-part mode of §1.10 |
| `conversation_language` | unset | Q34 item 5 | no live session |
| `feature_retention_days` | 30 (then only what replay consolidated) | Q34 item 6 | no live session |
| `keep_slot_snippets` | `True` | Q34 item 6 | no live session |
| `account_training_use_checked` | his statement (the account setting is his; the engine records only that he checked it) | Q34 item 7 | Claude route off |
| `overage_confirmed_off` | `True` | Q34 item 8 | Claude route off |
| `context_tokens_max` | 4,000 | Q34 item 9 | Claude route off |
| `hub_offline_after_download` | `True` (`HF_HUB_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1`, local paths) | Q34 item 10 | always on at runtime; only the M1 download step is online |
| `tts_engine`, `voice` | unset; speech disabled until set | Q1 | speech off |
| `face_look` | `"neutral_placeholder"` | Q2 | placeholder |

### 7.4 No emotion labels below Claude

- **Identifiers.** Design names that read as affect words are mapped to neutral code names: drop/rise events (`drop_event`, `rise_event`, `env_drop`, `env_rise`); hurt latch → `h_word`; C_F, C_L → `Dp_face`, `Dp_word`; threat reflex → `reflex_glare_loud`; the glad-with appraisal basis → `basis_return_LP_CR`, startle-orient → `basis_orient`; care load → `load_N`; the person-valence rule → `omega_rule`; synergies are named by their member channel codes (`syn_BI_LD_CHR`), never by an affect; μ → `mu`; valence readout → `v_readout`. Groups are muscle/signal groups (`smile_laugh`, `brow`, `head_gaze`, `voice`).
- **Lint (`tests/test_no_labels.py`, CI and pre-commit).** Scans `engine/`, `eval/`, `web/`, `tools/` and `tests/` (except the lint's own stem table):
  - **What is scanned:** every identifier (AST names, attributes, function and class names, keyword arguments, dict keys), every string literal and f-string part, every comment and docstring in Python; in JavaScript and HTML, identifiers, strings and comments by a tokenizer; in JSON, YAML, TOML and `.lock` files, keys and string values; file and directory names.
  - **Tokenisation:** split on `_`, `-`, `.`, `/`, whitespace and punctuation; split camelCase and PascalCase at each lower-to-upper change and at letter–digit boundaries (`isHappy` → is, happy; `HTTPMoodX2` → http, mood, x, 2); lower-case everything. So snake, camel and kebab case, and model ids such as `roberta-base-go_emotions`, are all caught.
  - **Match:** each token against a stem table: `emotion*`, `emotiv*`, `happ(y|ier|iest|ily|iness)`, `unhapp*`, `sad`, `sadd*`, `sadly`, `sadness`, `joy*`, `enjoy*`, `grief*`, `griev*`, `anger*`, `angr*`, `fear*`, `afraid`, `disgust*`, `contempt*`, `shame*`, `asham*`, `guilt*`, `pride`, `proud*`, `worr*`, `anxi*`, `sympath*`, `empath*`, `concern*`, `mood*`, `distress*`, `relief*`, `reliev*`, `hurt*`, `glad*`, `surprise`, `surprised`, `surprises`, `surprising`, `surprisingly` (not `surprisal`, the information-theory quantity of M6 and q̂), `love`, `loved`, `loves`, `loving`, `hate`, `hated`, `hates`, `hatred`, `lonel*`, `bored`, `boredom`, `upset*`, `frustrat*`, `nervous*`, `scare*`, `scary`, `calm*`, `excite`, `excited`, `excitement`, `exciting` (not `excitation`, the source signal of the laugh synthesizer and WORLD), `sentiment*`, `valence*`, `arous*`, `feeling*`, `care`, `cares`, `caring`, `affective`, `affection*`. Plurals and inflections are covered by the stems; whole-token exact forms (`care`, `love`, `sad`, `pride`, `surprise`, `excite`) avoid false hits on `career`, `glove`, `sadhu`, `surprisal`, `excitation`. A unit test of the lint itself checks each spelling class: `is_sad`, `fearLevel`, `joy-gain`, `Emotions`, `moods`, `go_emotions`, `relievedFlag` must fail; `career`, `feature`, `surprisal`, `excitation`, `glove` must pass.
  - **Allowlist, small and listed by path:** (i) Claude-facing text only: `engine/omega/instruction.txt` and the three line constants in `engine/omega/lines.py` (above the state; reviewed by the operator at M6); (ii) documentation: `*.md` files outside `engine/`, `eval/`, `web/`, `tools/` (research notes and this spec are not code); (iii) the refused Seamless field names in `engine/dyads/loader.py`'s `DENY_FIELDS` constant only (it must name them to refuse them) and the same names in A13's test; (iv) the lint's own stem table `tests/lint_stems.py`. Any other hit fails CI; adding an allowlist entry is a reviewed change.
- **Imports and calls:** a test fails if any module imports a package on the §7.2 "not used" list, calls `transformers.pipeline`, or imports a sequence, audio or image classification head (§7.2).
- **Models:** A17's SHA-256 allowlist (`models.lock`): FaceLandmarker task file, Kyutai STT 1B, Whisper-small, all-MiniLM-L6-v2, the TTS voice; nothing else loads.
- **Data:** A13 (loader) and the store schema (A12) carry no label field.

### 7.5 No network below the Ω process (Principle 7, review issue 2)

`run.py` starts `fast`, `voice`, `slow`, `asr`, `tts` and `replay` under macOS `sandbox-exec` with `config/sandbox.sb`, a profile that denies all network except loopback and unix sockets (`(deny network*)` then `(allow network* (local ip "localhost:*"))` and unix-socket rules), and with `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1`. Only `omega` (and its Claude Code subprocesses) and the allowlisted downloaders of M1/M3 run outside it. `sandbox-exec` is deprecated by Apple but works on current macOS; if the M1 check finds it unavailable, the fallback is a per-process check: at start each process tries to connect to a public address and must fail behind a pf anchor the operator approves (an Ask), else the engine refuses to start (A16). The browser uses a dedicated profile whose sync and telemetry the operator can turn off (M2 Ask).

### 7.6 CI

CI (GitHub Actions, if the repository uses it) runs `pytest` and the lints on **synthetic arrays only**; code and those synthetic arrays leave the Mac, which is fine. CI never receives recorded or operator data: a CI step fails if any file under the store, dyad-cache or `research/build/results/` data paths, or any `.npz`/`.npy` above 1 MB, is in the checkout.

---

## 8. Decisions this specification needs from the operator

Items 7–16 are Q34's items 1–10, built on their recommendations; **nothing that depends on them is used until he answers** (§7.3, "Before his answer").

1. **Q30**: learn head pose and gaze (and voice features) from the recorded dyads, or keep D70 as it stands. The spec builds D70 as it stands; a switch adds the targets.
2. **Q31**: keep the own-display mask (built as recommended).
3. **Q32**: accept the lost behaviours (built as recommended).
4. **Q33**: keep the newborn own-distress brow (+0.45) at his words of need (built as recommended).
5. **Q1 voice identity**: which TTS and voice (needed at M5; speech is off until chosen); laugh-synth listening test.
6. **Q2**: the face stays the neutral placeholder until he approves a look (confirm).
7. **[off-Mac] Text to Anthropic** (Q34 item 1): his transcribed words, the agent's replies and ≤ 3 retrieved snippets of past conversations, through his Claude Code login. Option: no snippets (`send_snippets`).
8. **Claude usage and daily cap** (Q34 item 2): ≈ 450 calls a day; he sets `claude_daily_cap`. At the cap the agent is silent; face and body continue.
9. **[off-Mac] Non-essential Claude Code traffic** (Q34 item 3): off (recommended) or default. The auto-updater is always off for the engine's processes.
10. **Downloads to the Mac** (Q34 item 4): models (≈ 2–4 GB) at M1 and the Seamless transfer (≈ 16.6 GB through, ≈ 1.5 GB kept; 2–3 h) at M3, under the 10 % floor. Option "models only": `dyad_fit_enabled = False`, with the degraded mode of §1.10 stated.
11. **His conversation language** (Q34 item 5): Kyutai 1B covers English and French only. **Correction to Q34 item 5's wording:** with a slower recogniser the quick laugh back does not wait (the echo never waits in 9.2, S10 removed). The consequence is a **longer partial echo** at a laugh that ends a bad-news sentence. The question in research/questions.md should be corrected to say this.
12. **Retention** (Q34 item 6): 30 days of features **and transcripts** (recommended), then only what replay consolidated, including the slot-referenced snippet lines (`keep_slot_snippets`, his choice, since those lines can be sent to Anthropic later). Options: 7 days, or until he deletes them. The indefinite 2-Hz decimation of spec revision 1 is withdrawn.
13. **[off-Mac] His account's training-use setting** (Q34 item 7): his Claude account's privacy setting decides whether Anthropic may train on this text. The engine does not change it; he checks it.
14. **[paid] No overage** (Q34 item 8): he confirms extra or overage usage is off on his plan. **Correction to Q34 item 8:** the agent does not fall back to "short built-in turns" at the limit. Hand-written words have no allowed source under D88, so it is silent until the limit resets. The question should say this.
15. **Tokens per call** (Q34 item 9): ≈ 2,000–4,000 input tokens (a window of the current session's recent turns plus ≤ 3 snippets of ≤ 200 tokens), or a shorter `context_tokens_max`.
16. **Offline after the first download** (Q34 item 10): local model paths, `HF_HUB_OFFLINE=1`, `HF_HUB_DISABLE_TELEMETRY=1`, a deny-network sandbox for every engine process except `omega` (§7.5).
17. **Evaluation runs over 6 h** (machine.md): F22, lesions and surrogates are planned to stay under 5 h per sitting (§5.5). Any run predicted above 6 h in one sitting comes to him first.
18. **About 2 h of sittings at M2** for his own feature recordings, which F1 and F22 need on the 14 channels Seamless lacks.
19. **For information (decided in the spec, reversible):** F23 is a gate before day 1; the harness loader's VAD allowance is not used by the engine (D70 and r7 §6.7 exclude VAD); F6, F9, F10, F15 (live) and F20 are relative to recorded listeners; F13 is folded into F24 and F21 is deleted; the reply send point θ_end is chosen on val (default 0.5 before the fit); β = 4 and the 5-s horizon are hand-set generic decision constants, swept at M9.

---

## Changes after review

Each issue of research/build/review-spec.md and how it is closed. None adds a situation-specific rule: every new value is a `generic` parameter (§3.3) or a test instrument in `eval/`.

| # | Issue | How it is closed | Where |
|---|---|---|---|
| 1 | F19 fails by construction: q̂, the turn model's question feature and P_name also read the agent's reply, and reply length moves turn events | Claude's text never reaches the state. Only `OwnHeard` does: the words actually spoken, made by `tts` at playback. It reaches T only through five declared ports: P1 Λ_V(own) in g and g_o; P2 q̂'s agent-turn input; P3 the turn model's question bit; P4 P_name; P5 own turn-event times. His side reads only his transcript. The type trace refuses any other Ω read, so F19 holds by construction. F19 is restated over `ports.downstream`, with a duration-matched swap, per-port lesions, all ports held, and a duration-changed swap | §1.3.1, §1.5.5, §1.5.6, §1.8, §4.4, §5.1 F19 |
| 2a | A5 vacuous: the shadow copied the T values | The shadow **computes** its whole T state from its own inputs. Only Ω values, rule-6 latches, noise, g and D_τ are held. A5 compares the independently computed T state with the factual one. On failure the output falls back to ȳ, the factual T state is replaced by the shadow's clean one, and learning is off | §1.6, A5 |
| 2b | A3 fires on allowed away responses | A3 now checks that the toward slope S⁺ stays 0 on zero-ceiling channels (or the frame is a hold) and that there are no toward cone or appraisal entries. Away partner-caused parts are allowed | A3 |
| 2c | A14 fires when 𝒟 rises during a session | Per-drive accounting: every change comes from a declared term, and Σ drops ≤ 𝒟(start) + Σ rises. Drives stay in [0, 1] and 𝒟 ≥ 0 | A14 |
| 2d | The fail-safe (render ȳ_k) does nothing for T-route failures | One fail-safe per assertion. T routes go to their disabled state: the gate goes to its context-free constant (A2) and L_d to 0 (A8). Learned bases and Δ go to 0 (A7). A9 gates the laugh synth to 0 and uses neutral prosody, or mutes. A14 freezes the body and stops learning | §4.3 table |
| 2e | Smaller points: S⁻ notation, budget persistence, page watchdog, runtime network | The exact `ledger7` formula is given with S⁺. Budgets reset at session start. The page has a 200-ms watchdog (rest face, mute). A16 adds a deny-network sandbox plus `HF_HUB_OFFLINE`/`HF_HUB_DISABLE_TELEMETRY`, and `omega` is the only process with network | §1.6, §1.7, §7.5, A16 |
| 3 | Falsifiers that reinstate situational outcomes | F6: the once-per-lapse clause is dropped. It becomes (a) day-1 timing against held-out listeners and (b) dose–response steering of 𝒟_p at M8 or later. F9: the agent's contrast is tested against held-out listeners' contrast, plus a g_o lesion. F10: now the fast echo only; the own-laugh part is retired and logged as a risk. F13 is folded into F24. F15 live: return ratio per g bin, relative to listeners. F20: a timing test (delivery to closure within recogniser latency plus one evaluation). Event classes are defined in `eval/events.py`, the engine never imports `eval/`, and the counters moved out of `engine/dyads/`. F21 is listed as deleted | §5.0, §5.1, §3.1, §7.1 |
| 4 | Hand-set generics fit no A15 category | New `generic` category (decision / engineering / fit definition), with a table of every value, its reason, and whether it is learned or tuned. θ_end is tuned on val against recorded listeners' response onsets. β, H_init and the rollout horizon are hand-set and swept at M9. The cost of false starts is counted. INNATE.lock lists every constant, with a canonical serialisation. The situation-name test uses a reviewed allowlist plus a situation-word list. The §5.2 lesion predictions are to be re-derived with the 97-key κ 0.70 ledger, and the 6-s arm is marked a lesion control only | §1.5.6, §3.2, §3.3, A15, §5.2 |
| 5 | Label lint bypassable (snake/camel/kebab, plurals, missing words, `tools/`, model ids) | The lint tokenises on `_ - . /`, case changes and digits, matches stems case-insensitively, and has an extended word list. It scans `tools/`, `tests/`, comments, config files and file names. A small path-listed allowlist covers Claude-facing text, docs, the deny constant and the stem table. A lint self-test covers each spelling class. Calls to `transformers.pipeline` and classification heads are banned. A17 checks model SHA-256s. glad-with is renamed `basis_return_LP_CR` | §7.2, §7.4, A17 |
| 6 | Off-Mac flows and usage missing or inconsistent with Q34 | Retention is 30 days for features **and** transcripts, then only what replay consolidated; the indefinite 2-Hz decimation is gone. `claude_daily_cap` is set by the operator. The training-use setting is his to check. No overage, and silence at the limit (no built-in turns). Tokens per call: a 4,000-token window, compaction detected. Offline after the first download, with the auto-updater off. New switches `send_snippets` and `dyad_fit_enabled`, with the degraded mode stated. A browser profile. CI on synthetic data only. Each switch is used only after his answer. Q34 items 5 and 8 are flagged for correction | §1.8, §1.9, §1.10, §7.3, §7.5, §7.6, §8 |
| 7 | F22/F1 on recorded partners cover only 6 of 20 channels; regression measured at 10 Hz; data unverified | The real F22 runs on recorded partners for all 20 capped channels: 6 from Seamless, 14 from his M2 recordings (≈ 2 h, Ask), and live on all 20 at M7. Synthetic injected copies are a CI mechanism test only. The regression is bit-exact at 10 Hz first, then 30 Hz within a tolerance. Test people and hours are counted at M3 | §5 partners, F1, F22, §5.1 note, §3.1, M0, M2, M4 |
| 8 | Compute: F22 ≈ 36 CPU-h against machine.md's 6-h rule; the GIL; 𝓜 on MPS; browser clock; echo rig | F22 runs the ledger only, batched over (people × delays) on CPU, with channels across 8 cores. A pilot predicts the wall time. If it exceeds 5 h, the run is split across nights or people are subsampled to 25. A single sitting over 6 h is put to him. The same rule covers lesions and surrogates. The fast loop is its own numpy-only process with shared memory (Plan A), or a native extension that releases the GIL (Plan B), chosen by an M1 threshold. Voice features get their own process. 𝓜 runs online on CPU. The slow shadow runs in `slow`. The browser clock falls back to `expectedDisplayTime` and is re-mapped every 60 s. The echo rig is a 240-fps video with a flash, or a photodiode. Xcode command line tools are installed for pyworld | §0, §1.2.1, §1.2.4, §1.6, §1.10, §2.1, §2.2, §5.5 |
| 9 | M0/M1 gaps: INNATE.lock contents, wrapper API, T1 rule, dependencies, M1 branch thresholds | `config/innate.py` holds every constant with value, source, category and why, and the lock is canonical JSON. A minimal `Tagged` API and an AST rule for T1 are given. Core deps are numpy/scipy/pytest, with `engine` and `mac` extras; `uv.lock` is generated on the Mac; Python ≥ 3.12, < 3.14. **M1 has a pass / branch / fail threshold for every check**: tracker, pipeline, clock, recogniser, utterance recogniser, breathing, fast and slow tick, memory steps, sandbox, `resume`, thinking, first-sentence latency, compaction and tokens | §3.3, §4.4, §6 M0, M1 table, §7.2 |
| 10 | Minor: lag buffer, §0 diagram, 6-s lesion arm | The lag buffers keep 3 s for the 2-s window (≈ 2.4 MB). The diagram shows the per-process shadow and ledger. The 6-s arm is a lesion control only | §1.6, §0, §5.2 |
| 11 | review-m4 (M4 offline core) | (1) LP ← glare resized to −0.012, −0.0035 and every non-reflected G₀ cross entry charged at weight 1 whatever the dyad prior (§1.5.1, A6). (2) N_L lowered in proportion to the reader's confidence, a declared generic fit definition (§1.3). (3) A_F dropped: A = A_L (§1.3). (4) g_o written once, at assembly (§1.5.3, §1.5.4). (5) Labels: own synergies `newborn`, face channels `generic` (fit definition), embedding sizes `generic` (engineering) (§3.3) | §1.3, §1.5.1, §1.5.3, §1.5.4, §3.3 |
