# Build specification: the Cayley–ledger build core (revision 9.2) on the operator's Mac

Written 2026-11-26 under D90 ("building means writing the build specification and code in this repository to run on the operator's Mac; no downloads, datasets or experiments in this cloud session"). This file specifies; it builds nothing, downloads nothing and runs nothing.

**What is built.** research/foundations/design-cayley-ledger.md at **revision 9.2**: the "Revision 9 (build core): audit" section and §0–§8 as corrected by "Revision 9.1 history" and "Check of revision 9.1 and the answer", plus the "Build core summary". Where the mechanism text still says "lags to 120 s at the 10-s window", "61 constraints" or "≤ 1.02 c at 240 s", 9.2 supersedes it: **the 10-s and the 60-s windows are both scanned to 300 s, 97 constraints per channel, κ = 0.70** (Check of 9.1, "The answer"). Parts the design inherits by reference ("as revision 7/6/5/3") are taken from `design-cayley-ledger.r7.md`, `.r6.md`, `.r5.md`, `.r3.md`, `.r2.md` and cited as r7 §x etc.; "design §x" means the current file.

**Binding.** brief.md Principles 1–10; D70 (Seamless: FAUValue streams and transcripts only, emotion fields never read), D78, D80–D91. Operator notes Q22, Q23, Q26, Q27, Q29. Open questions, built on their recommendations until answered: **Q30** (not widened: D70 as it stands, no head, gaze or audio from dyads), **Q31** (own-display mask kept), **Q32** (losses accepted; nothing hand-written comes back), **Q33** (the newborn own-distress brow at his words of need kept). Each is a switch in `engine/config/operator.py` (§7.3) so an answer changes one value, never the mechanism.

**Words used.** "He" is the partner (the operator, or anyone in front of the camera). "Channel k" is one of the 33 counterpart channels (§1.1). "Partner-caused part" is factual output minus shadow output (design §2.13). A "route" is a path from his signals to the agent's outputs (design §3.11). Design names such as "relief", "hurt" or "concern" are used in this prose only to point at design text; the code uses the neutral identifiers of §7.4.

---

## 0. Architecture in one page

```
 Browser page (localhost only, CSP connect-src 'self')             Python engine (one process, two real-time loops)
 ┌───────────────────────────────────────────────┐   ws://127.0.0.1   ┌──────────────────────────────────────────────────────────┐
 │ camera 30 Hz ─► FaceLandmarker 0.10.35 (his)   │ ─ features ──────► │ 𝓑 boundary: P₀, reflection P, calibration, voice feats   │
 │ mic 16 kHz (AEC on) ──────────────────────────│ ─ PCM ───────────► │   │                                                       │
 │ rendered face ─► FaceLandmarker (own, 10 Hz)  │ ─ own features ──► │ fast loop 30 Hz: fast gear · cone · appraisal (2 Hz in) │
 │ three.js placeholder face ◄───────────────────│ ◄ render vector ── │   · free display · assembly · SHADOW · LEDGER · asserts │
 │ audio out (TTS PCM, laugh synth) ◄────────────│ ◄ PCM ──────────── │ slow loop 2 Hz: T/F/𝒦 state · body · gates · L_d · q̂ ·  │
 └───────────────────────────────────────────────┘                    │   turn-taking · initiative · 𝓜 · retrieval               │
                                                                      └──────┬──────────────┬───────────────┬────────────────────┘
       ASR worker (Kyutai STT 1B incremental + utterance recogniser) ◄──PCM─┘              │               │
       TTS worker (neural TTS → WORLD prosody replacement; laugh synth)  ◄── text+targets ─┘               │
       Ω manager: warm pool of 3 Claude Code forks (Agent SDK, subscription) ◄── transcript, markers ───────┘
       Store (features only, memory-mapped) ──► nightly replay process (MPS) ──► per-person weights
       Offline, once before day 1: dyad fit on Seamless (FAUValue + transcripts) ──► frozen dyad-learned parts
```

Nothing below the Ω manager sends anything off the Mac. The Ω manager sends text (§1.10) to Anthropic through the operator's Claude Code login (D84).

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
- Partner instance: 30 Hz. Per frame message `FaceFrame{t_capture: f64 (from requestVideoFrameCallback captureTime), present: bool, bs: [52] (ARKit order), M: (4,4) transform}`. Measured 13.1 ms median on an M1 Pro (same note).
- Own instance: runs on the rendered avatar canvas at **10 Hz**, same message, tagged `own` (own-face observations for 𝓔 and Π̃, r6 §6.2 rows 2, 8; P7).
- No pixels leave the page; no frame is stored anywhere.

**1.2.2 P₀ and reflection P (innate, fixed; `boundary/face_map.py`).** A fixed linear map from (52 blendshapes, head Euler angles from M, eye-look blendshapes) to the 18 face and 5 head–gaze channels of §1.1 (e.g. LP = mean(mouthSmileL, mouthSmileR); CR = mean(cheekSquintL, R); BI = browInnerUp; BO = mean(browOuterUpL, R); BL = mean(browDownL, R); LD = mean(mouthFrownL, R); JO = jawOpen; UL = mean(eyeWideL, R); LT = mean(eyeSquintL, R); NW = mean(noseSneerL, R); LS = mean(mouthStretchL, R); CHR = mouthShrugLower; LPR = mean(mouthPressL, R); DIM = mean(mouthDimpleL, R); FUN = mouthFunnel; PUK = mouthPucker; MCL = mouthClose; LRO = mean(mouthRollLower, mouthRollUpper); HP, YAW, TILT from M; VG, HG from eyeLook*). Reflection P mirrors YAW, TILT, HG and swaps L/R (r5 §2.2). Output `u_face: [23]` at 30 Hz. The table is innate (body/perception), listed in INNATE.lock. **Same map** is used on the agent's own rendered face, so his face is read in the agent's coordinates (P3).

**1.2.3 Audio front end.** Microphone captured in the page with `getUserMedia({echoCancellation: true, noiseSuppression: false, autoGainControl: false})`; the agent's own speech is played by the same page, so the browser's echo canceller removes it (the AEC of r5 §2.2). 16-kHz mono PCM, 20-ms frames, to the engine. Half-duplex gate: while the agent's own audio is playing, his voice features are flagged `overlap` and his phrase-level prosody is not updated (r5 §2.2).

**1.2.4 Voice features ("GeMAPS-lite", `boundary/voice.py`; allowed by Principle 1: continuous prosody, no labels).** 100-Hz analysis frames → 30-Hz stream:
- F0 (pyworld `dio` + `stonemask`), RMS energy, voicing, syllable-rate proxy (envelope peaks), pause durations, his turn latency → phrase-level `[6]` (F0 level, FR, EN, RT, PAU, LAT) updated at phrase end and held.
- Voiced-burst energy BU, its 4–6 Hz modulation depth r ∈ [0, 1] (1-s sliding spectrum of the envelope), ingressive share q ∈ [0, 1] (spectral tilt of breath noise) (r5 §6.1).
- **Burst split (innate reflex S42):** BU_L = BU · r · (1 − max(q, s_cry)), BU_S = BU − BU_L, s_cry = min(1, 2√(BI · LD)) from his face (r5 §2.2). RHY = r · BU, BRE = breath-band energy.
- Audio onset envelope `a_on` (for the startle blink M4 only), VAD flag (for silence length and turn timing).
- Breathing (S4, knowing only): breath-band rate and depth above his own rest, plus upper-body motion from M, at **10 Hz**, `breath: [2]`. Dropped if the week-0 check fails (design §3.17 item 15).
- Output `u_voice: [10]` (6 phrase + BU_L, RHY, BRE, BU_S) at 30 Hz. With `u_face` this gives **u ∈ R^33** in channel order.

**1.2.5 Derived partner features (innate, F-typed; r5 §2.1).** f_loud = (EN − 0.7)⁺/0.3; g_at = his gaze at the agent's face ∈ [0, 1]; f_glare = BL · LT · g_at; f_laugh = √(BU_L · RHY); f_duch = √(LP · CR). `f_der: [5]`, 30 Hz.

**1.2.6 Streaming speech recognition (`boundary/asr/`, separate process).**
- **Incremental recogniser:** Kyutai `stt-1b-en_fr` through its MLX runtime (fixed-delay streaming; expected word-end-to-delivery 0.6–0.75 s; design §6.1). Emits `Word{text, t_start, t_end, t_delivered}`; words are never revised once emitted. Fallback if the operator's language is not English or French or the runtime fails the week-0 check: another fixed-delay streaming model, else the utterance recogniser alone (design §2.4.2: a longer partial echo; stated).
- **Utterance recogniser:** Whisper-small through `mlx-whisper`, on VAD-delimited utterances; its text is the canonical transcript sent to Claude (design §6.1, "unchanged").
- **ASR normaliser (assembly, design §2.14):** one function used on live text and on every Seamless transcript alike: lower-case, numbers as the recogniser emits them, laughter tags and "haha"-type tokens and bracketed events removed, interjection list removed (r8.3 §6.7 item 3). Output `Utterance{speaker, words: list[Word], text_norm, t_end}`.
- **Utterance embedding:** `all-MiniLM-L6-v2` (384-d) → fixed projection to **64-d** (PCA fitted once on the Seamless train-split transcripts, frozen) → `e: [64]`.

**Outputs of 𝓑, typed:** F stream `u[33]`, `f_der[5]`, `breath[2]`, `a_on`, `vad` (30 Hz / 10 Hz); T stream `Word`, `Utterance`, `e[64]`, turn events `{his_utterance_end, session_start, agent_utterance_end}` with times; identity token `id` (face presence + the operator's declared session; no face recognition model is added: day 1 has one person, the operator; a second known person needs an operator-entered name, see §6 M7).

### 1.3 The typed latent state (`engine/state/`)

Every state field carries a type tag fixed at construction (r5 §2.2): **T** (his words, turn order, session boundaries, identity, values latched per session, the agent's own body clock, anything computed only from these), **F** (anything computed within a session from his face, voice or derived features), **Ω** (the agent's own realised words, draft choice, retrieval, own turn events), **K** (𝒦: 𝓜 and the concept layer, which read all of the above and are written only through likelihood learning). Rules 1–14 of design §2.2 / r5 §2.2 are enforced as in §4.4.

| Field (code name) | Design symbol | Type | Shape | Rate | Dynamics (source) |
|---|---|---|---|---|---|
| `E` | energy | T | scalar ∈ [0, 1] | 2 Hz | −0.04 %/min awake; restored only in nightly sleep/replay (r5 §2.1, r3) |
| `A_F`, `A_L` | activation | F, T | scalars | 2 Hz | A_L ← max(A_L, 0.5 s_lex²), τ 3 min (M6) |
| `V_F` | threat-reflex load | F | scalar | 30 Hz | g_at · max(f_glare, f_loud(1 − 2 f_pos)₊) (S41) |
| `h_word` | hurt latch h | T | scalar | event | h ← max(h, v_w) at an addressed utterance; τ 10 min; no halving (S20) |
| `K[id]` | contact deficit | T | scalar per known id | 2 Hz | between sessions rises (1 − K)/36 h; in session dK/dt = −K f_id e(t)/30 s (S26); 0 for a never-missed person |
| `P_play` | play deficit | T | scalar | event | rises (1 − P)/5.05 h; P ← P(1 − 0.15 q̂) at each of his turns (S21) |
| `I_lp` | learning-progress deficit | T | scalar | event | r5 §2.8 |
| `N_L[slot]` | word need (V, A, T) | T | `(n_topic, 3)` | event | from the word reader; τ 30 min; low-information utterances only raise it (S39) |
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

**1.5.1 Held cone** (`cone.py`; r5 §2.5, r6 §2.5, design §2.5). y_C = Σ_m G_m^{(id)}(ξ_m − b_id), latched per session, 30 Hz. Diagonal ω_g F_m s_C c_k with F_m = (0, 0.7, 0.2, 0.1) (BI: (0.5, 0.5, 0, 0)). G₀ keeps **only the threat reflex's entries** (gaze away from a glare by reflection; LP ← glare −0.035, −0.01; BI ← glare +0.006). Learned cross entries: in the charged cross budget Σ_j λ_kj |G_m,kj| ≤ F_m s_X c_k; on face pairs they must carry the **dyad sign prior** (§3) or be 0; on other pairs only the agent's own within-synergy signs, cross-synergy pairs unsigned and charged (M8; no rule J). Zero-ceiling rows: no toward entries, diagonal ≤ 0. Projection onto these sets after every write (A6).

**1.5.2 Appraisal display** (`appraisal.py`; r5 §2.6). y_A = Γ(α) ξ_A, computed at 2 Hz and linearly interpolated to 30 Hz. Five bases: neutral; glad-with and startle-orient (innate, S44); two learned Γ^{(3,4)} trained by 𝓛_A to anticipate the agent's own display 2 s ahead (now including L_d's response). |Γ_kk| ≤ s_A c_k; cross entries away-orthant only, entry ≤ 0.15, row ≤ 0.25; sign prior on face pairs; own-display mask. 𝒜: (36 + 64 + 7 + 4) → 64 → 12; selection W 12 → 5 softmax.

**1.5.3 Free display** (`free_display.py`; design §2.7). Π_o = Π₀ + Δ + L_d, T inputs only, 2 Hz → 30 Hz envelopes.
- Π₀ newborn rows (S45): drop → LP, CR, brighter voice (× g_o on the smile–laugh part); own rise (care or hurt load) → **BI +0.45, LD +0.35, lower voice**, rise 0.4 s, apex to 1.5 s, decay τ 3 s (Q33 kept); hurt → distress face with gaze aversion; activation (A_L) → raised lids and outer brow; low energy; learning-progress drop → interest face; laugh motor pattern (BU_L +0.40, RHY +0.35, CR +0.20, LP +0.15 per unit, ≤ 0.40) driven by a_laugh = 0.40 q̂ g_o at each of his turns (S18); pre-speech inhale (BRE 0.15 for 0.3 s); physiological sigh (BRE +0.15 for 1 s, spontaneous rate 1/3 min × (1 + 2 max(0, 0.5 − E)/0.3)).
- Δ: 161 → 128 → 18 open synergies, tanh, trained by 𝓛_display under the own-display mask (rule 8: zero weight on BL, LT, LPR, NW, DIM; LS and CHR only × the agent's own a_d) (Q31 kept).
- L_d (§1.5.5) added at each of his utterance ends and at session start.
- Phrase targets (rule 7, fixed in 9.1): read y_C, y_A and T values h, E, A_L, L_d's RT, and the envelopes (drop × g_o) only.

**1.5.4 Echo gate g and own-display gate g_o** (`gates.py`; design §2.1, §2.4.3, r7 §2.4.1). Learned offline, frozen (§3). Monotone additive models: per input i a shape function on fixed knots q = 0.05 … 0.80 (7 basis functions), fitted directions, exp link, clipped to [0, 1]; evaluated at 30 Hz from inputs updated at 2 Hz or on word delivery.
- g inputs: V⁻_his (his 20-s read, LP, CR, BU_L, RHY, BRE masked), 𝒟_p(N_L) and Λ_V on his words **as delivered so far**, V_own (agent's own 3-s rendered face through Π̃₀, LP and CR masked), Λ_V(own words), D_τ `(3, 4)`, q_trace. ≈ 18 inputs.
- g_o inputs: 𝒟_p(N_L), Λ_V(his words), V_own, Λ_V(own words), q_trace. **Never any channel of his** (rule 13′).
- g multiplies only y_f on the smile–laugh group; g_o only the agent's own smile–laugh displays (drop, contact drop, own laugh).

**1.5.5 Listener display L_d and listener-laugh reader q̂** (`learned_t.py`; design §2.7, §2.8). Frozen, **T inputs only** (rule 14).
- L_d: ridge map from T inputs (population reader's (V, A, T) of his last utterance; Λ(his words); turn events "his utterance ended", "session started", each with time since in 2-s bins over 0–20 s) to BI, BO, LD, LP, CR and RT. **TILT, HP, VG, FR, EN held at 0** (no D70 target). |L_d,k| ≤ 0.45; own-display mask applied. ≈ 840 weights.
- q̂ ∈ [0, 1]: monotone additive (same form as g) from the transcript context of his last two turns and the agent's last turn (through Λ's encoder), turn order, and the utterance's surprisal under a frozen population words model (§3); evaluated at each of his utterance ends.

**1.5.6 Turn-taking and initiative** (`turns.py`; design §2.9).
- p̂_end (turn-end predictor) and h(t) (silence hazard): logistic, ≈ 100 weights each, inputs silence length, syntactic completion, last turn ended in a question and whose (M1), both people's facial-action-unit channels (no head, gaze or pitch: D70). 2 Hz, plus at each delivered word.
- Reply timing: drafts are messaged when p̂_end ≥ 0.5 (the calibrated predictor's even-odds point; a general decision constant, not a scene threshold) and the pre-speech inhale fires; if his voice resumes before speech onset, all forks are interrupted and discarded. Speech onset = scoring deadline + 0.35 s (S50).
- Initiative: at 2 Hz in mutual silence with no turn owed, speak with probability h(t) Δt · exp(β ΔĴ), β = 4, ΔĴ the 𝓜-rollout drop of 𝒟 + 𝒟_p from speaking now rather than in 5 s.

### 1.6 Assembly, shadow run and the attenuate-only ledger (`engine/shadow/`)

**Assembly (design §2.3), 30 Hz:** y = sat(g·y_f|smile–laugh + y_f|others + y_C + y_A + g_o·y_o|smile–laugh + y_o|others) + visemes; then the ledger; then M ∗ (y + blink reflex).

**Shadow run (design §2.13, r6 §2.13).** A second instance of the engine (same weights, same code object, run in lockstep in the same thread after the factual step) whose input differs in one place: his expressive stream (u, f_der, breath, voice features) is replaced by his latched baseline b_id. Held at factual values: T values, every Ω value, latched session values, the agent's own noise, g and D_τ (rule 10). g_o, L_d and q̂ are computed in the shadow from the shadow's own inputs. Output ȳ ∈ R^33.

**Ledger (9.2), per channel k, at 30 Hz.** r_k = y_k − ȳ_k (partner-caused part). Constraint keys (W, L):
- W = 2 s, L ∈ {0, 0.5, 1, 2, 3} s (5);
- W = 10 s, L = 0, 5, …, 300 s (61);
- W = 60 s, L = 0, 10, …, 300 s (31).
**97 per channel.** For each key, his window mean of u_k at t − L and the window mean of the output's partner-caused part at t, both centred at 30-min EMAs, feed running sums S, E with τ 30 min; the bound is S⁻ ≤ κ c_k E with **κ = 0.70** on every channel, window and lag (bound 0 on zero-ceiling channels). Deviation floor: a key whose |π| < 0.10 × its running RMS imposes no constraint; a key over budget (b < 0) forces the output's partner-caused part to 0 for that frame (recovery). The projected value is clipped to lie between 0 and r_k (attenuate-only: never larger, never the other sign). Rendered y_k = ȳ_k + projected r_k. Reference implementation: `ledger7`/`ledger9` in research/foundations/sims (design-g7/checks.py; design-g9/ledger_lag120.py), with the 97 keys of sims/check-cayley91/ledger_close.py `w10`.
- **Lag buffers:** for W ∈ {2, 10, 60} s, the centred window mean of his channel is stored for 300 s at 30 Hz: 3 × 9,000 × 33 float32 ≈ 3.6 MB.
- **Cost:** 3,201 constraints per frame, vectorised (numpy, `(33, 97)` arrays): budget ≤ 1.0 ms per frame on one performance core.
- **What it cannot see** (design §2.13 end): T routes (identical in both runs; bounded by type, T1, E1).

### 1.7 Face and voice output (`engine/output/`, `web/`)

- **Avatar rig (placeholder, Principle 8, Q2):** a neutral procedural three.js face in the page using the 52 ARKit blendshape names, plus head pose and eye rotation. Engine → page at 30 Hz: `RenderFrame{t_display: f64, bs: [52], head: [3], eyes: [4], blink: f32}` from the inverse of P₀ (a fixed channel → blendshape table, innate) plus visemes. The page interpolates to the display rate. No look beyond the neutral placeholder is built until the operator approves one.
- **Speech:** text → TTS (Plan A: a local neural TTS, Piper candidate; Plan B: macOS AVSpeechSynthesizer; voice identity is Q1, the operator's) → WORLD (pyworld) analysis and **resynthesis** with F0(t) = F0_agent · exp(level + range × template(t)) (two innate phrase templates: statement, question; chosen by the text's question form only), per-phrase RMS set to EN, time-warp to RT; TTS pauses discarded, 0.20 s at a comma and 0.40 s at a sentence end × the pause factor; onset at the scoring deadline + 0.35 s or the latency target if later (r6 §6.6, r7 §6.6). Interjections and laughter words stripped from Claude's text before TTS (R11).
- **Laugh synthesizer** (innate body): parametric source–filter (glottal pulses at the agent's F0, 4–6 Hz AM, breath noise), driven only by y_BU_L, y_RHY, y_BRE; floor θ_L = 0.04; **no sob source** (y_BU_S ≡ 0) (S47).
- Audio out: 24-kHz PCM over the websocket to the page.

### 1.8 Claude coupling through the subscription (`engine/omega/`; design §2.12, r6 §6.5, r7 §6.5, r8.3 §6.5)

**Process and isolation (P4, D84).** Python `claude-agent-sdk`, spawning the local Claude Code CLI on the operator's own login; never `--bare` (it needs an API key). `ClaudeAgentOptions` fixed for the engine's lifetime:
- `setting_sources=[]` (no user, project or local settings: his hooks, CLAUDE.md files, `additionalContext` injectors and output styles never reach a draft);
- `cwd` = an empty engine-owned directory under a path with no CLAUDE.md above it;
- `tools=[]`, `allowed_tools=[]`, `mcp_servers={}`, `hooks={}`, `permission_mode="default"`;
- `system_prompt` = the byte-stable constant instruction (`engine/omega/instruction.txt`), plus, only in the fallback below, one fixed line per fork;
- `model="haiku"` by default (operator may choose a larger model at a latency cost); `effort="low"`; `include_partial_messages=True`; **no output-token cap** (it would count thinking tokens; r7 §6.5).

**What Claude receives, and nothing else.** The constant instruction; the engine-written canonical transcript (his normalised utterances and the agent's chosen replies); observable-marker user turns for initiative ("[no reply from him for 25 s]", silence rounded to 5 s); ≤ 3 retrieved raw transcript snippets (need-conditioned retrieval, ALiBi slope 1/(7 days)); and one fixed "attend to" line per fork (what he said; how he seems to feel, from his words; what this reminds you of), the same line every turn. **Never** a body value, latent value, category id, label, number derived from state, or a state-selected line. The prompt builder accepts only `TranscriptText`, `Marker` and `Snippet` objects, which can be constructed only from recogniser output, the agent's own past replies and the marker template (§4.4, A11).

**Warm pool and forks.** When each agent reply completes, the engine writes the canonical `.jsonl`, then connects three `ClaudeSDKClient`s with `resume=<canonical transcript path>`, `fork_session=True`, idle. At p̂_end ≥ 0.5 (§1.5.6), each receives his message plus its line i. Each streams; only text deltas are counted (thinking deltas ignored); a draft is interrupted at the end of its second sentence or at 60 words.

**Deadline and selection.** A draft is scored when its first sentence ends: 30-s rollout of 𝓜 at 2 Hz (60 steps, < 0.2 s), score = −E[Σ 𝒟(b̂) + 𝒟_p(N̂)] under the separation rule (r5 §2.10). Drafts with a first sentence by **0.5 s after the first draft's first sentence, or 3.0 s after his turn end, whichever is first**, are compared; the best wins; losers' processes are **killed** (not drained) and replaced in the background; at most four Claude Code processes exist at once. The winner's reply, without its line, is appended to the canonical transcript; fork session files are deleted at the next idle moment.

**Fallbacks.** (1) If a hand-written transcript is not accepted by `resume` (week-0 check), each fork carries its line in its own system prompt and the winning fork's session becomes canonical, used only if the week-0 checks show the session file stores neither the system prompt nor resumable thinking; otherwise the forks differ only by sampling (r8.3 §6.5). (2) On a rate-limit signal or p90 first-sentence latency > 3.0 s over 20 turns, the pool shrinks 3 → 2; a second signal within 30 min → 1; after 30 min clear it grows back by one (r6 §6.5). (3) If no Claude Code process answers (offline, logged out), the agent does not speak; the face and the fast loop continue unchanged (the fast loop never waits for Claude, Principle 4).

**How the state reaches Claude:** only draft choice (≤ log₂3 = 1.6 bits per turn), snippet choice (≈ 6 bits), when Claude is called, and when a draft is stopped (design §2.12). **How Claude reaches the state:** only through its realised words, heard by the agent: Λ_V(own) in g and g_o (rule 12′) and P_name (attenuate-only ≤ 0.05 on a named display; S49). Telemetry fields (`duration_ms`, `thinkingTokens`) are logged for the week-0 checks and not fed to the state (not in the design).

**Latency budget** (his turn end → first word; r6 §6.5): detection 0.5 / 0.9 s; to warm forks 0.01; first token 0.8 / 1.4; first sentence 0.4 / 0.7; deadline wait 0.1 / 0.5; scoring 0.2; TTS + WORLD first phrase 0.15 / 0.3 → **p50 ≈ 2.2 s, p90 ≈ 3.5 s (deadline-capped)**, plus unmeasured thinking time at effort `low` (week 0). The inhale and the agent's face cover the wait.

### 1.9 Memory and replay (`engine/memory/`)

**Store (P7: features only).** Per session, memory-mapped `float16` arrays: u[33] and f_der[5] at 30 Hz; breath[2] at 10 Hz; own outputs y, ȳ, rendered, at 30 Hz; own-face observations at 10 Hz; voice phrase features; state snapshots (T, F, 𝒦) at 2 Hz; events; the transcript with word timestamps (both sides); Ω records (drafts, which won, timings, telemetry). Full rate for 30 days, then decimated to 2 Hz (r3 §2.11); transcripts kept. ≈ 1.8 GB per 30 days (r6 §6.4). The writer accepts only these schemas; no audio or image buffer type exists in the store's API (A12).

**Retrieval.** Snippet index over past transcripts keyed by identity × topic embedding × time; query built from ∇𝒟, N̂ and the concept posterior; ≤ 3 raw snippets.

**Nightly replay** (separate process, launched only when no session is live; MPS; < 2 GB; ≈ 40–45 min; r6 §2.14, design §2.14), in order:
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
- **Online (states only):** body and drives, traces (ξ, D_τ, q_trace), μ, slots, 𝓜 states, concept centroids and PMI counts, session statistics. No weight that reaches the face changes online.
- **Nightly (replay):** §1.9.
- **Never learned:** c_k, G_k, shares, κ, Π₀, θ₀, G₀'s threat entries, the burst split, the reflexes (INNATE.lock).
- **General learning biases (D85 source 3; the only innate parts of learning):** monotone additive shape of g, g_o, q̂ with fitted directions (S13); multi-scale traces as inputs (S15); distress-weighted replay κ_replay = 4 (sample weight 1 + 3 · min(1, 𝒟_p(N̂)/0.05) on replayed moments; S48); calibration from low-need moments, slow toward aversive readings (S38); low-information evidence counts only upward (S39); care credited only from separated, partner-initiated reports (S40); learning rate × exp(−0.5 r̄), gradient clip 1, pull to θ₀ λ 0.1 (r6 §2.1). No objective rewards his smiles, attention or time (Principle 6).

---

## 2. Data flow and timing on the Mac

### 2.1 Processes and threads

| Process | Threads | Work | Rate |
|---|---|---|---|
| Browser page (Chrome or Safari, localhost) | main (three.js render), 2 workers (FaceLandmarker his / own), audio worklet | capture, tracking, render, audio I/O with AEC | camera 30 Hz, own 10 Hz, display 60 Hz |
| `engine` (Python 3.12) | **fast thread** (pinned loop, `time.perf_counter` scheduled), **slow thread**, asyncio I/O thread | fast: 𝓑 face/voice framing, fast gear, cone, assembly, shadow, ledger, asserts, RenderFrame; slow: T/F/𝒦 state, readers, gates, L_d, q̂, turn-taking, initiative, 𝓜, scoring; I/O: websocket, ASR/TTS/Ω queues | 30 Hz / 2 Hz |
| `asr` | 2 | Kyutai incremental (MLX, GPU), Whisper-small utterances (MLX) | streaming |
| `tts` | 1 | TTS, WORLD resynthesis, laugh synth | per phrase / 30 Hz |
| Ω manager (inside `engine`'s asyncio loop) + ≤ 4 Claude Code CLI subprocesses | — | warm pool, streaming, interruption | per turn |
| `replay` (nightly, exclusive with a live session) | — | §1.9 | nightly |
| `dyadfit` (once, offline) | — | §3 | once, 2–3 h |

The fast thread never blocks on the slow thread, ASR, TTS or Ω: it reads the latest slow outputs from a lock-free double buffer (2-Hz values held between ticks). A missed fast deadline repeats the previous frame and is logged.

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

Done-check: measured onset-to-onset echo lag on a scripted input = 0.45 ± 0.035 s (one camera frame), p99.

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

If the week-0 measurement exceeds 6 GB: first a 4-bit incremental model, then a pool of two forks, then one; each is reported. Replay < 2 GB and never runs alongside a session. Disk: store ≈ 1.8 GB per 30 days; Seamless features ≈ 1.5 GB (≈ 16.6 GB transferred and reduced file by file); models ≈ 3–4 GB. `df -h .` is checked before every download and nightly; nothing writes below the operator's 10 % free floor (Q11).

---

## 3. What is learned from recorded dyads under D70, how, and what stays innate

### 3.1 Data access (D70, D85; `engine/dyads/loader.py`)

- **Read:** Seamless Interaction `movement/FAUValue` (24 action-unit columns at 30 Hz; columns 12 and 19 are duplicates when identical, so 23 distinct values; the column order verified on a 20-file pilot before any fit), `movement/is_valid`, and `metadata/transcript` (word timestamps). Vendors V00 (v1 or v4, never mixed) and V02 (v4) (r7 §6.7).
- **Never read:** `emotion_scores`, `emotion_valence`, `emotion_arousal`, `EmotionValenceToken`, `EmotionArousalToken` (refused by name before any request or file open; assertion on every URL and npz key); audio, video, head pose, gaze, body, and VAD files (D70 allows face streams and transcripts; speech timing comes from word timestamps; r7 §6.7). Note: research/harness/loader.py allow-lists VAD; the engine's loader does not.
- On the operator's Mac only; streamed file by file, reduced on arrival (laugh onsets and ±3-s 30-Hz snippets of LP, CR, JawDrop extracted first; the rest to float16 at 10 Hz on the agent's channels) and the raw file deleted.
- **Split:** the harness's fixed splits_v2 (person-disjoint: 70 % train, 15 % val, 15 % test; research/harness/HARNESS.md). Fits use train; directions of the monotone models use the first half of train people; fallbacks and smoothing are chosen on val; **test is used only by the falsifiers (§5)**.
- **Words as the agent will have them:** every word input uses only words whose end timestamps are ≤ event time − the measured delivery latency (week 0); the ASR normaliser is applied to every transcript (design §6.7 items 1, 3).
- **Calibration:** each recorded person is mapped to the agent's scale by his own median and spread exactly as the operator is (r7 §6.7 item 4).
- **Rare events counted before fitting**, by words and masked faces, never by labels: troubles, mockery and misfortune laughs; conversation openings with the listener's face visible; long silences after words of need (design §6.7 item 8).

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
| p̂_end, h(t) | who speaks after each silence ≥ 0.2 s, and when | silence length, syntactic completion, question-ended last turn and whose (M1), both people's 23 AU channels | logistic | ≈ 200 |
| sign mask, cross-entry sign prior | sign of the 1-min block co-variation of listener channel k with speaker channel j, |ρ| ≥ 0.2 | face pairs only (both channels among the AUs) | statistics | sign table |

The listener is always read through the same functions the agent applies to itself (P3). The dyad-learned parts are self-predictions of the same kind as the readers (design §2.14): they predict recorded listeners' movement and turn timing; nothing is an emotion label, and the dataset's emotion fields are never opened.

**Not learnable under D70 (kept absent or at the innate level until Q30 is answered):** nods, the head tilt, the attentive head, head and voice accommodation, gaze and head turn cues, turn-end pitch, a quieter concerned voice, signs for head, gaze, voice and laugh-sound pairs (design "No allowed source" item 5). The code has `dyad_streams = {"FAUValue", "is_valid", "transcript"}` in `config/operator.py`; widening it (Q30) adds targets to L_d (TILT, HP, VG; and FR, EN with voice) and inputs to the turn-taking model, with no other change.

**Fallbacks fixed before fitting** (r7 §6.7): g (F15) — refit on V00 improvised alone; then keep only passing inputs and put the context-free remainder to the operator. Population reader — target becomes max(speaker's later loads, listeners' response). Any part failing F24 is disabled (set to its context-free constant or 0) and its behaviour then has only Claude's words as its source (design §8.1 item 1). **F23 as a gate before day 1:** this spec makes it one (§5.2); if L_d or q̂ fails it, L_d's target is residualised on the speaker's same channel and refitted (the check of revision 9's suggestion; Build core summary, Risks).

### 3.3 What stays innate (exactly the allowed list; audit "Counts")

| Category | Items |
|---|---|
| **body** | drives E, A, V, K_id, P, I with set points, dead-bands, weights; 𝒟 and 𝒟_p forms; the voice and its rendering (fixed onset, pauses, templates; S50); laugh synthesizer and its floor (S47); opponent masking of drops by own rises, factor 3 (M5); activation from lexical surprisal (M6); the laugh motor pattern and the pre-speech inhale; contact relief τ_c 30 s (S26); play deficit relief by q̂ (S21) |
| **reflexes** | the fast gear (S43); threat reflex (S41); burst split (S42); glad-with and startle-orient appraisal bases (S44); gaze following (M2); head micro-motion gating (M3); startle blink (M4); physiological sigh |
| **newborn muscle patterns** | Π₀ rows: drop → smile; own rise → cry face (BI +0.45, LD +0.35, lower voice; Q33); hurt → distress face with gaze aversion; activation → raised lids, outer brow; low energy; learning-progress drop → interest face (S45) |
| **per-expression copy ceilings** | c_k, G_k, shares, r_k, zero ceilings, the ledger and κ = 0.70 |
| **general learning biases** | §1.10 list |
| **operator's call (Q31)** | the own-display mask (S46), kept as recommended |

Everything else is learned (§3.2, §1.9) or is Claude's words. The fixed perception and rendering maps (P₀, its inverse, the 64-d projection) are boundary code, not behaviour. A unit test reads `INNATE.lock` and fails if any innate constant lacks one of these category tags or names a situation (§4.4, A15).

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

Each runs every tick at the stated rate; a failure is logged with its frame, and the **fail-safe** for that channel for the rest of the session is to render the shadow output ȳ_k (partner-caused part 0). The fast loop never stops; Claude is not told.

| ID | Invariant | Rate | Failure means |
|---|---|---|---|
| A0 | s_C(1 + ρ) + s_X + 0.636 s_A + r_k ≤ 0.974 c_k for every k; c_k = 0 ⇒ G_k = 0 and no toward entries | import | build failure |
| A1 | 0 ≤ y_f,k ≤ G_k x_d,k + 1e-6 on one-sided channels; |y_f,k| ≤ G_k |E_k| on signed | 30 Hz | bug in fast gear |
| A2 | 0 ≤ g ≤ 1, 0 ≤ g_o ≤ 1; their provenance sets exclude the masked channels of his (g) / every channel of his (g_o) | 30 Hz / load | type violation |
| A3 | rendered − shadow = 0 on the 13 zero-ceiling channels | 30 Hz | uncounted route on a zero-ceiling channel |
| A4 | per channel per frame: |out| ≤ |r_k| and out · r_k ≥ 0 (F1‴) | 30 Hz | ledger bug |
| A5 | shadow T state, Ω values, g, D_τ equal factual values (hash at 2 Hz; rule 10, F1′) | 2 Hz | F → T leak: build failure; whole output falls back to ȳ |
| A6 | ω_g ∈ [−1, 1]; cone entries in their sets; face-pair cross entries carry the prior sign or 0 | each write | projection bug |
| A7 | appraisal bases in their convex sets; Δ and learned bases have zero weight on BL, LT, LPR, NW, DIM (if Q31 kept) | after each replay step and at load | F11 |
| A8 | |L_d,k| ≤ 0.45; TILT, HP, VG, FR, EN rows of L_d are 0 under D70 | load, 2 Hz | fit or config error |
| A9 | own laugh ≤ 0.40; laugh synth input only from y_BU_L, y_RHY, y_BRE; y_BU_S = 0; phrase F0 level, range, EN, RT equal their targets ± 1 % after WORLD | per phrase / 30 Hz | rendering bug |
| A10 | SHA-256 of the innate tables equals INNATE.lock; no learned parameter tensor aliases an innate table | start | tampering or bug |
| A11 | every forked prompt and the canonical transcript are byte-identical to what the engine built (F14); no "attend to" line from an earlier turn in any history (F17); the prompt contains only `TranscriptText`, `Marker`, `Snippet`, the instruction and the fork line | per turn | Claude route stopped and logged |
| A12 | the store's directories contain only the registered feature schemas (no WAV/PCM/image magic numbers, no file above the schema size) | nightly, start | P7 violation: stop |
| A13 | dyad loader: every requested URL suffix in the allowlist; every npz key in {FAUValue, is_valid}; denylist names never opened | per request | D70 violation: stop |
| A14 | every drive in [0, 1]; 𝒟 ≥ 0; Σ drops within a session ≤ 𝒟(session start) (satiable, Principle 6) | 2 Hz | body bug |
| A15 | T1: no counter, accumulator or event rate is a T field (static AST check of `state/`); every INNATE.lock entry has a category in {body, reflex, newborn, ceiling, bias, operator} | load / CI | design violation |

### 4.4 The type rule, checked

At load, `invariants/typetrace.py` runs 60 s of recorded features through the engine in trace mode, where each array is a provenance-carrying wrapper, and asserts rules 1–14 (design §2.2; r5 §2.2): T reads only T (except P_name and rule-6 latched values); E1 (events T-only); rule 4 (only y_f, y_C, y_A, y_o and visemes write counterpart outputs); rule 7; rule 11′–14. Live mode uses plain arrays; the trace runs at every start and in CI.

---

## 5. Test plan: judged on internal state

Instruments: evaluation.md E1 (lesions: ≥ 20 instances per lesion, severity sweep for continuous strengths, a sham lesion of equal size, mean over instances with the full distribution), E2 (steering on the engine's own state: both signs, dose–response, random direction of equal norm as control), E3 (synchrony against surrogates: 1,000 per test, observed against the 95th percentile, segment-shuffle **and** data-sliding both required; partner-swap, timing-resample and month-swap where stated). **No test is scored on how closely the agent's face matches a human face** (brief; Q19).

Partners used:
- **Recorded partners:** Seamless test-split people (never used in any fit), their FAU channels mapped to his 18 face channels (head, gaze and voice held at baseline), their transcripts as his words. The agent plays the listener.
- **The mirror-only partner** (report 9): replay a partner who only mirrors the agent's own output, against no partner at all.
- **The operator, live** (S2 onward), recorded as features only.
- Constructed partners from research/foundations/sims appear only as **code regression tests** (they reproduce the design's measured numbers to catch implementation errors); they are not evidence of any behaviour (brief, Foundations research).

### 5.1 Falsifiers mapped to tests

| F | Statement (design §8.2 and inherited) | Test | Data | Milestone |
|---|---|---|---|---|
| F1 | with partner-swap, segment-shuffle, timing-resample and month-swap surrogates (words and turn order fixed), any channel exceeds its pooled bound at 2 s, 10 s or 1 min (conditioned metric), G_k, or the instant bound; or the ledger binds on a natural partner > 1 % of frames | `eval/f01_bounds.py`: per-channel slopes; surrogates per E3 | recorded partners; operator (month-swap after ≥ 30 sessions) | M4, M8 |
| F1′ | shadow T state ever differs from factual | A5 logged over all runs | all | M4 on |
| F1‴ | ledger output larger than, or opposite sign to, the partner-caused part | A4 logged | all | M4 on |
| F2 | a decoder on F state fails to recover his held level at r ≥ 0.9 while F1 holds (knowing fails) | ridge decoder from F state to his 1-min level | recorded partners | M4 |
| F3 | crossed-habits manipulation does not change which faces raise C_F | swap two recorded people's channel codes after calibration | recorded | M8 |
| F4″ | at equal later need change, draft choice correlates with predicted display change, with replies inside the separation window, or with his later engagement | log analysis | operator | M8 |
| F5 | varying only his smile amplitude (words, turns fixed) changes K, P, I, the drop envelopes or any T display | **steering clamp**: scale his LP, CR ×0, ×0.5, ×2 | recorded | M4 |
| F6 (restated) | the bid threshold θ_C is removed (S34): **restated** as "the speak-or-wait choice in mutual silence does not respond to 𝒟_p (lesion ΔĴ → 0 leaves initiative timing unchanged), or speaks more than once per lapse without his reply" | lesion β = 0 vs intact | recorded + operator | M7 |
| F7 | naming-aligned trajectories do not differ from non-naming ones, or the difference survives a P_name lesion | E1 lesion of P_name | operator | M8 |
| F8, F8″ | Π̃ + H_id disagree with his later separated reports more than a person-independent baseline after 400 utterances; co-training drift | nightly report | operator | M8 |
| F9 (restated) | the arrival clause is retired by design ("No allowed source" item 2: gladness at a mourner's arrival for 2–3 s is accepted). **Kept:** at bad news (his words of loss), the cheek raise or the drop envelope rises within 2 s after the word is delivered | event analysis | recorded + operator | M5, M7 |
| F10 | any laugh-synth output within 2 s of his BU_S bursts | event analysis | operator | M7 |
| F11 | learned bases or Δ place weight on BL, LT, LPR, NW, DIM | A7 | nightly | M8 |
| F12 | deleted with the posture | — | — | — |
| F13 (restated) | the play rule is removed (S17); **restated** as F24 for q̂: the own laugh fires on > 5 % of held-out utterances whose listeners did not laugh, relative to q̂'s calibration | held-out | Seamless test | M3 |
| F14 | any draft's recorded system prompt or user message differs from what the engine built | A11 | live | M6 |
| F15 | the gate fails its criterion on test people (r7 §6.7: predicted return where the listener's own masked face reads V ≥ 0.4 not below 0.5 of ordinary, or rank correlation < 0.2); live, the laugh synth sounds within 2 s of his laugh following his words of loss, insult or harm | held-out + live | Seamless test; operator | M3, M7 |
| F16 | Λ's predicted response to utterances answered with a wince (masked V ≥ 0.4) not above its prediction for the rest | held-out | Seamless test | M3 |
| F17 | any prompt or the canonical transcript contains an "attend to" line from an earlier turn | A11 | live | M6 |
| F18 | the agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with σ_id ≥ 0.25 σ_ref | **steering**: clamp his BI, BO, LP while his words carry need; sweep σ_id | recorded + operator | M4, M7 |
| F19 | any T quantity other than Λ_V(own) in g and g_o changes when only Claude's reply text is changed | **steering**: swap the reply for a neutral text, diff T state | live and replayed sessions | M6 |
| F20 | live, the laugh synth sounds > 0.6 s after his laugh ending a sentence with words of loss, insult or harm; or ordinary sentence-final laughter not returned within 0.6 s in > 10 % of cases | event analysis | operator | M7 |
| **F22** | an injected uncounted route copying his channel with **delay 10–300 s** renders above **1.0 c_k** by the block-mean metric at 2-s, 10-s or 1-min windows; or the ledger changes > 1 % of frames of the counted routes on natural partners | `eval/f22_delayed_copy.py`: inject a gain-1 copy (onset lobe + 60-s low-pass, as sims/design-g9) of his channel delayed by L ∈ {10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300} s into the output after assembly (so only the ledger sees it); worst slope over lags 0–300 s; every channel with c_k > 0; plus the counted routes alone (frames changed) | **recorded test partners** (≥ 50 people, ≥ 2 h each by concatenating their sessions) | M4 (gate for M7) |
| F23 | on held-out people, the pooled 1-min slope of the agent's channel k (L_d, own laugh) on the speaker's channel k, through words alone, exceeds c_k; or L_d's response changes when only the speaker's face is changed | held-out + **steering** (face swap, words fixed) | Seamless test | M3 (gate for M7) |
| F24 | g_o, q̂, L_d or the turn-taking model not better calibrated than a context-free constant on held-out people | held-out | Seamless test | M3 |

**Measured expectations to reproduce in code regression (not evidence):** with the sims partners, κ 0.70 and 97 keys: delayed copies 10–300 s at 0.83–0.88 c; counted routes 0 frames changed; grow and flip 0.000 (Check of 9.1, "The answer").

### 5.2 Lesions (design §7, E1 protocol)

Each with ≥ 20 seeds, a sham lesion of equal size in a part the derivation says is irrelevant, and the predicted state-level change written before the run (§7 of the design):

| Lesion | Predicted change (state level) |
|---|---|
| g ← 1 | his laughs at grief, mockery and misfortune returned (r7: +0.137) |
| g_o ← 1 | drop smiles and own laugh as large over his need words and after its own serious words as in light talk |
| L_d ← 0 | no listener display at his words; only the own-rise row and Claude's words |
| q̂ ← 0 | no own laugh; P never relieved |
| learned turn-taking → fixed 6-s rule | initiative timing no longer follows held-out listener timing |
| sign prior removed | learned appraisal bases take signs recorded listeners do not show |
| ledger lag scan → lags 0–3 s | injected copy delayed 10–120 s passes at 1.3–2.9 c |
| ledger κ 0.70 → 1 | injected copy at 1.03–1.20 c (10–120 s), 1.23–1.34 c (240 s) |
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

---

## 6. Staged build order

Each milestone ends with a done-check. **Ask** marks what goes to the operator; nothing marked Ask is done before his answer. Items that send data off his Mac or are new paid services are marked **[off-Mac]** / **[paid]** and are questions, not decisions.

| M | Build | Done-check | Operator provides or approves |
|---|---|---|---|
| **M0** skeleton | repo layout §7; `pyproject.toml` with exact pins; `config/channels.py`, `INNATE.lock`; type wrappers; A0, A10, A15; label lint and import denylist (§7.4); CI (`pytest`, lint) on synthetic arrays only | `pytest` green; lint finds no forbidden token; A0 passes; INNATE.lock reproducible | nothing |
| **M1** week-0 measurements | `tools/week0/`: MediaPipe latency (both instances); camera-to-photon latency; Kyutai STT word-end-to-delivery p50/p90, language coverage, MLX runtime, RTF with everything running; Whisper-small; breathing separation (rest, paced, hold; silent and talking); memory of all processes together; Claude checks: hand-written transcript accepted by `resume`; session file stores no system prompt and no resumable thinking; Haiku 5.5 thinking (disabled / `MAX_THINKING_TOKENS=0`) via `thinkingTokens`; first-sentence latency at effort `low`; byte check | a report `research/build/week0.md` with each number and the branch it selects (recogniser fallback, breathing on/off, fork-line fallback, pool size) | **Ask:** approve model downloads to the Mac (MediaPipe 0.10.35 assets 15 MB; Kyutai STT 1B ≈ 1–2 GB; Whisper-small ≈ 0.5 GB; MiniLM ≈ 90 MB) under the 10 % floor; **state his conversation language** (Kyutai 1B: English, French); sit for the face, voice and breathing checks; **[off-Mac]** confirm test calls to Claude through his login (text only, D84) |
| **M2** perception boundary and store | `web/` page, websocket, P₀/P, voice features, burst split, ASR worker, normaliser, embedding, store writer | 10-min session stored as features only (A12 passes); echo-path latency ≤ 90 ms p99; words delivered within the week-0 p90; no raw audio or video on disk | **Ask:** which browser; camera and microphone permission; feature retention (30 days full rate, then 2 Hz, kept on the Mac) |
| **M3** dyad fit (offline) | `engine/dyads/`: allowlisted downloader, 20-file column-order pilot, reduction, event counts, the fits of §3.2, fallbacks, F15, F16, F23, F24, F13′ on test people | every fit's held-out report written; event counts written before fitting; A13 never fired; disabled parts listed; F23 passes or L_d is refitted residualised | **Ask:** start the Seamless transfer (≈ 16.6 GB through, ≈ 1.5 GB kept; D70 approves the use; machine.md asks before large transfers; run ≈ 2–3 h, < 6 h); **Q30** (head, gaze, voice features from the dyads) if he wants it before day 1 |
| **M4** core engine, offline | `state/`, `routes/`, `shadow/`, `invariants/`, `learn/` online parts; typed state; body; fast gear; cone; appraisal; free display; gates and learned T parts loaded; assembly; shadow; ledger (97 keys, κ 0.70); 𝓜 untrained; type trace | type trace passes; A1–A9, A14 silent on 20 h of recorded test partners; ledger regression reproduces 0.83–0.88 c and 0 frames on the sims partners at 30 Hz; **F1 (no month-swap), F2, F5, F18, F22 pass on recorded test partners** | nothing |
| **M5** face and voice output | three.js neutral placeholder rig, RenderFrame path, TTS + WORLD resynthesis, laugh synth, viseme track | A9 passes; echo lag 0.45 ± 0.035 s capture-to-photon; WORLD targets within 1 %; laugh synth silent at y = 0 | **Ask (Q1):** the voice (TTS engine and voice; Piper is GPL-3.0 with per-voice licences, macOS voices are local); a listening test of the laugh synthesizer; **(Q2)** the face stays the neutral placeholder until he approves a look |
| **M6** Claude coupling | `omega/`: isolation options, constant instruction, canonical transcript, warm pool, forks, streaming, interruption, scoring deadline, fallbacks, markers, retrieval | A11 / F14 / F17 pass on 40 scripted turns; **F19** passes; p50/p90 turn latency measured; losers killed; ≤ 4 processes | **[off-Mac] Ask:** confirm that his transcribed words, the agent's replies and ≤ 3 retrieved snippets of past conversations are sent as text to Anthropic through his Claude Code login (no audio, video, features or state); confirm ≈ 450 calls a day on his subscription (not a new paid service; may meet usage limits; the pool shrinks automatically); **Ask:** set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` for the engine's Claude Code processes (less telemetry leaves the Mac) or not; read and approve the constant instruction and the three fork lines |
| **M7** day 1, live | end-to-end on the Mac; initiative; reply timing; risk logging (§8 of the design: near-neutral face before words, mourner's arrival, partial echo at bad-news laughs, one valence for every group) | first live sessions run with no assertion failure; F10, F15 (live), F20 pass; turn latency p50 ≤ 2.5 s; memory ≤ 6 GB; nothing leaves the Mac except the M6 text | sessions with the agent; **Ask** before any second person is in view (identity is entered by him; their features are stored like his) |
| **M8** memory, replay, learning | nightly replay (§1.9), retrieval, ω, calibration, H_id, adapter, word → V map, Δ, 𝓛_A; monitoring reports | after 7 nights: A7, A14 silent; replay ≤ 1 h, ≤ 2 GB; F8″ report; F3, F4″, F7 analyses running | approve the nightly schedule (when the Mac is idle) |
| **M9** evaluation battery | E1 lesions (§5.2), E2 steering (§5.3), E3 surrogates incl. month-swap (§5.4), mirror-only partner | each prediction scored as written before the run; results in `research/build/results/` | Q5 stays open (raters, EMG) for S5; nothing needed here |

The new-core search (D91) continues separately; a new core would replace modules behind these interfaces.

---

## 7. Repository layout, language and libraries

### 7.1 Layout

```
engine/                         Python package (the engine; Principle 9)
  config/       channels.py (§1.1), innate.py (body, reflexes, newborn rows, biases), INNATE.lock,
                operator.py (Q30 dyad_streams, Q31 own_display_mask, Q33 own_rise_brow, model, pool size)
  boundary/     face_map.py (P₀, P, inverse for the rig), voice.py, burst_split.py, breath.py,
                asr/ (incremental.py, utterance.py, normaliser.py), embed.py, server.py (websocket)
  state/        types.py (T, F, Ω, K tags; TranscriptText, Marker, Snippet), body.py, drives.py,
                traces.py, ladder.py (μ), slots.py, readers.py (Π̃, H_id, word reader, adapter, word→V)
  routes/       fast_gear.py, cone.py, appraisal.py, free_display.py, gates.py, learned_t.py (L_d, q̂), turns.py
  shadow/       shadow.py, ledger.py
  output/       assemble.py, rig.py, prosody.py (WORLD), tts.py, laugh.py, visemes.py
  omega/        instruction.txt, lines.py, pool.py, transcript.py, scorer.py, retrieval.py, p_name.py
  model/        m_world.py (𝓜, LRU 2 × 128, heads), concepts.py
  memory/       store.py (schemas, memmap), replay.py
  learn/        nightly.py, objectives.py, projections.py
  dyads/        loader.py (allow/deny), reduce.py, events.py, fit_reader.py, fit_lambda.py, fit_gates.py,
                fit_ld.py, fit_qhat.py, fit_turns.py, fit_signs.py
  invariants/   asserts.py (A0–A15), typetrace.py
  run.py        live entry point; replay entry point; dyadfit entry point
web/            index.html, app.js, face.js (three.js placeholder), worker_track.js,
                vendor/ (tasks-vision 0.10.35 wasm + model, three.js) — served from localhost only
eval/           f01_bounds.py … f24_calibration.py, surrogates.py, lesions.py, steering.py, online_metric.py
tools/week0/    the M1 checks
tests/          unit tests, ledger regression (vs research/foundations/sims), type-trace tests, lint tests
pyproject.toml, uv.lock
```

`legacy-ts/` is not ported (MIGRATION.md: its body section and prompt paragraph show Claude numbers, which Principle 4 forbids).

### 7.2 Language and libraries (exact versions pinned in `uv.lock` at M0; each at least two weeks old)

- Python 3.12, `uv`. numpy, scipy (bounded least squares for the gates), torch with MPS (𝓜, Π̃, Δ, 𝒜; replay), `mlx` and Kyutai's MLX STT runtime, `mlx-whisper`, `sentence-transformers` (all-MiniLM-L6-v2, local), `pyworld`, the chosen TTS (Q1), `websockets`, `claude-agent-sdk` (spawning the installed Claude Code CLI), `pytest`.
- Browser: `@mediapipe/tasks-vision` 0.10.35 (never ≥ 1.0.0, Q3), three.js (one pinned release), vendored; no CDN at runtime.
- Not used: any emotion classifier or affect model (FER, DeepFace, HSEmotion, py-feat emotion heads, openSMILE emotion configs, SpeechBrain emotion models), any face-recognition model, any API key.

### 7.3 Operator switches (`engine/config/operator.py`)

| Switch | Default (recommendation) | Question |
|---|---|---|
| `dyad_streams` | `{"FAUValue", "is_valid", "transcript"}` | Q30 |
| `own_display_mask` | `True` | Q31 |
| `own_rise_brow` | `True` (+0.45 newborn row) | Q33 |
| `restore_lost_behaviours` | `()` (none; Q32) | Q32 |
| `claude_model`, `effort`, `pool_size` | `"haiku"`, `"low"`, 3 | D84 |
| `tts_engine`, `voice` | unset; speech disabled until set | Q1 |
| `face_look` | `"neutral_placeholder"` | Q2 |

### 7.4 No emotion labels below Claude

- **Identifiers.** Design names that read as affect words are mapped to neutral code names: drop/rise events (`drop_event`, `rise_event`, `env_drop`, `env_rise`); hurt latch → `h_word`; C_F, C_L → `Dp_face`, `Dp_word`; threat reflex → `reflex_glare_loud`; synergies are named by their member channel codes (`syn_BI_LD_CHR`), never by an affect; μ → `mu`; valence readout → `v_readout`. Groups are muscle/signal groups (`smile_laugh`, `brow`, `head_gaze`, `voice`).
- **Lint (`tests/test_no_labels.py`, CI and pre-commit):** an AST and text scan of `engine/`, `eval/`, `web/` fails on any identifier or string literal containing a forbidden word (emotion, emotional, happy, happiness, sad, sadness, joy, grief, anger, angry, fear, afraid, disgust, contempt, shame, guilt, pride, worry, anxious, sympathy, empathy, concern, mood), word-boundary, case-insensitive. Exempt files, each listed: `engine/dyads/loader.py`'s denylist constant (it must name the refused Seamless fields) and `engine/omega/instruction.txt`/`lines.py` (Claude's own text, above the state; reviewed by the operator at M6).
- **Imports:** a test fails if any module imports a package on the §7.2 "not used" list.
- **Data:** A13 (loader) and the store schema (A12) carry no label field.

---

## 8. Decisions this specification needs from the operator

1. **Q30** — learn head pose and gaze (and voice features) from the recorded dyads, or keep D70 as it stands. The spec builds D70 as it stands; a switch adds the targets.
2. **Q31** — keep the own-display mask (built as recommended).
3. **Q32** — accept the lost behaviours (built as recommended).
4. **Q33** — keep the newborn own-distress brow (+0.45) at his words of need (built as recommended).
5. **Q1 voice identity** — which TTS and voice (needed at M5; speech is off until chosen); laugh-synth listening test.
6. **Q2** — the face stays the neutral placeholder until he approves a look (confirm).
7. **[off-Mac] Text to Anthropic** — his transcribed words, the agent's replies and ≤ 3 retrieved snippets of past conversations, through his Claude Code login (implied by D84; confirm explicitly, including the snippets of earlier days).
8. **Claude usage** — ≈ 450 calls a day on his subscription with automatic shrinking of the pool (not a new paid service).
9. **[off-Mac] Claude Code telemetry** — run the engine's Claude Code processes with `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` or not.
10. **Downloads to the Mac** — the models (≈ 2–4 GB) at M1 and the Seamless transfer (≈ 16.6 GB through, ≈ 1.5 GB kept; 2–3 h) at M3, under the 10 % floor.
11. **His conversation language** — the incremental recogniser (Kyutai 1B) covers English and French only.
12. **Live feature retention** — 30 days at full rate, then 2 Hz, on the Mac (≈ 1.8 GB per 30 days).
13. **For information (decided in the spec, reversible):** F23 is a gate before day 1; the harness loader's VAD allowance is not used by the engine (D70 and r7 §6.7 exclude VAD); F6, F9 and F13 are restated because the bid threshold, the arrival mask and the play rule no longer exist; the turn-end send point is p̂_end ≥ 0.5.
