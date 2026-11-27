# engine (milestones M0, and the offline parts of M4, M6, M8 and M9)

The engine of research/build/spec.md (build core: research/foundations/design-cayley-ledger.md, revision 9.2).
Nothing here touches a camera, a microphone, a model, Claude or the network (the M6 tests run a fake Claude CLI). All tests use small synthetic arrays;
their results say nothing about behaviour.

## M0: configuration, invariants, ledger

- `config/channels.py`: the 33 counterpart channels (spec §1.1) as a frozen table; A0 runs at import.
- `config/innate.py`: every innate and generic constant in one table (name, value, unit, source, category,
  generic subtype, why). `config/INNATE.lock` is its canonical JSON with the SHA-256 of the entries; regenerate with
  `make lock` (a reviewed change). `config/innate_names.txt` is the reviewed name allowlist. `config/operator.py`
  holds the operator switches of §7.3; an unanswered one refuses to be used.
- `invariants/t1_rule.py` (T1 as an AST rule), `invariants/tagged.py` (the `Tagged` provenance wrapper; M4 adds
  `__setitem__`, so writes into a traced buffer carry the written tags).
- `state/drives.py`: the drive forms and the declared update terms A14 accounts for.
- `shadow/ledger.py`: the attenuate-only ledger, 97 keys per channel, kappa 0.70; bit-identical at 10 Hz to
  `ledger7` / `ledger9` / `w10` in research/foundations/sims.

## M4 (offline core)

**State** (`state/`)
- `types.py`: field types T / F / O (Ω) / K / latched / own, with the provenance prefixes each may carry
  (`ALLOWED_SOURCES`); the T objects `Word`, `Utterance`, `TurnEvent`, `qform`; the Ω object `OwnHeard`, which only
  `heard_at_playback` can make (the `tts` process at M5), truncated at the last word played.
- `ports.py`: the five Ω → T ports P1 `lambda_own`, P2 `qhat_agent_turn`, P3 `turn_question_bit`, P4 `p_name`
  (≤ 0.05), P5 `own_turn_events`. Their outputs are tagged `T:port.Pi`; `ports_downstream.json` is the committed
  `downstream(Pi)` (CI compares it with a fresh trace).
- `body.py`: the innate body at 2 Hz: E, A_L, h_word, K (in-session drop, between-session rise, none for a person
  never missed), P (lowered by qhat), I, N_L, D_p, the E1 events with opponent masking and their envelopes, the own laugh
  amplitude 0.40 qhat, q_trace, the sigh (own noise draw), L_d and qhat evaluation (A = A_L; N_L lowered only by the
  reader's confidence); every drive change recorded for
  A14, whose fail-safe freezes the body.
- `readers.py`: untrained stubs with fixed shapes: a hashed bag-of-words placeholder for the MiniLM → 64-d encoder,
  Lambda, the population word reader (with its confidence head, 0 untrained), word → V, surprisal, pi_topic, the own-body reader on his masked face and on
  the own face, the P_name map.

**Routes** (`routes/`)
- `fast_gear.py`: frozen per-channel echo at 0.45 s from a capture-time ring buffer, onset lobe, G_k.
- `cone.py`: the held cone, 4 traces centred at b_id, latched per session; diagonal omega_g F_m s_C c_k; G0 = the
  threat-reflex entries only; learned cross entries (stub 0) projected onto the charged budget, away caps, the dyad
  sign prior on face pairs, own within-synergy signs elsewhere, the reflection rule on YAW and HG.
- `appraisal.py`: zero-DC 20-90 s band-pass, the two innate bases (`basis_return_LP_CR`, `basis_orient`), two
  learned bases (stub 0), the network and selection (stub 0, so 1/5 each), 2-Hz display interpolated to 30 Hz, the
  set and its projection.
- `free_display.py`: Pi_0 newborn rows, inhale, sigh, Delta (stub, own-display mask), L_d, P_name; T inputs only.
- `gates.py`: the monotone additive form (7 basis functions, exp link, clip), g (18 inputs) and g_o (5 inputs) with
  their input traces (D_tau, V_his, V_own); untrained gates are their context-free constant 1.0.
- `learned_t.py`: L_d (6 × 140 ridge), qhat (logistic, base rate 0), the turn model (theta_end 0.5), omega's rule,
  and `Learned`, the container of every learned part (all untrained; `Learned().untrained()` lists them).
- `boundary/derived.py`: f_loud, g_at, f_glare, f_laugh, f_duch and the threat reflex V_F.

**Shadow** (`shadow/`)
- `assemble.py`: y = sat(g y_f|SL + y_f|others + y_C + y_A + g_o y_o|SL + y_o|others); the muscle filter (4 Hz,
  zeta 0.8, numpy only); the laugh-synth input (BU_L, RHY, BRE only).
- `shadow.py`: `Run` (one engine instance), `ShadowPair` (factual and shadow in lockstep: the shadow computes its own
  T state from his baseline b_id; held: Ω objects, b_id, noise draws, g, D_tau), the ledger, A1-A9 with their
  fail-safes (`Safety`), and `traced_session`, the type-trace driver.
- `invariants/asserts.py`: A1, A2, A5 (`t_state_digest`, `check_a5`), A6, A7, A8, A9 added to the M0 checks.
- `invariants/typetrace.py`: trace mode (`TypedState` checks every declared field assignment; display terms checked
  against rule 4, 11', 13'), `run_trace`, `downstream`.

**Regressions against the reference sims** (tests/refsims.py reads the reference functions verbatim):
fast gear = `fast` of design-g9 bit for bit at 10 Hz (integer 0.4-s delay, as the reference) and at 20 Hz (0.45 s);
30-Hz interpolated echo against the formula (1e-12); cone diagonal = design-g5 H9 (1e-15); band-pass = design-g5
`bp` (1e-15), step peak 0.505 at 39 s, sup 0.636; gate basis = design-g7 `phi` exactly and its fitted-gate formula
(1e-12); the 30-Hz ledger through the engine's own fast gear: counted routes 0 frames changed, grow and flip 0, and
(slow) delayed copies 10-300 s at 0.83-0.88 c, within 0.02 c of the 10-Hz figures.

**What is not exact, and why** (also in the module docstrings)
- Own laugh: the free display carries a_laugh = 0.40 qhat (T) and g_o multiplies it once at assembly, at render
  time (spec §1.5.3 now says so; it used to write g_o in both places).
- A_F ("slow loudness and motion") never had a formula and is dropped from the code path: A = A_L (spec §1.3).
- N_L (S39): N_L <- max(N_L, r) - c (N_L - r)+, so a higher reading raises it fully and a lower one lowers it in
  proportion to the population reader's confidence c = 1 - var_pred / var_pop (its own predictive variance over the
  population variance of the target; `reader_confidence_form`, generic fit definition). Chosen because it is the
  reader's own posterior relative to its prior, needs no extra model or threshold, is fitted with the reader at M3,
  and is exactly 0 for an untrained reader (today's behaviour: evidence only raises N_L).
- "Addressed" utterances (h_word) are all of his; "partner-initiated" (I) means not directly after an agent turn.
- E1 events are stamped at the 2-Hz tick (≤ 0.5 s after the utterance end).
- The fast gear's 4-s low-pass starts at 0, as the reference; the shadow's g_at is 0 (b_id has no gaze baseline).
- Without the own-face tracker (M2), each run's own previous rendered output stands in for its own-face observation.
- G0's LP ← f_glare is −0.012 (2-min trace) and −0.0035 (20-min trace), i.e. F_m s_X c_LP (review-m4: r5's
  −0.035, −0.01 were over budget since r6). Every non-reflected G0 cross entry is charged at weight 1 whatever the
  dyad prior's sign (`cone.g0_usage`): LP ← f_glare uses 98 % of LP's 2-min budget and all of its 20-min budget
  under priors −1, 0 and +1 alike, A6 never fires on G0, and learned entries get only what G0 leaves.
- The type trace follows data flow only; a branch on a T value from a port first hid I_lp from downstream(P5) (the
  F19 test caught it; the update is now branch-free). It runs on synthetic data with small random stub weights.
- Not built here: 𝓜, mu and slots (z_T = 0), the turn model's inputs, prosody/WORLD (A9's per-phrase part), visemes,
  blink, own head micro-motion gating, the calibration readers (b_read, sigma_id
  are carried, unused), online learning, the process split and its entry points.

**INNATE.lock** gained (a reviewed change): `cone_away_caps`, `cone_lateral_rows`, `own_synergies`,
`derived_feature_sign_as`, `face_channels`, `echo_gate_unread`, `p_name_max`, `g0_glare_to_HG`, `g0_glare_traces`,
`appraisal_return_channels`, `appraisal_orient_basis`, `pi0_rise_voice`, `pi0_drop_row`, `pi0_word_latch_row`,
`pi0_activation_row`, `pi0_low_energy_row`, `pi0_progress_drop_row`, `pi0_driver_shape`, `appraisal_net_shape`,
`display_delta_shape`, `embedding_dims`, `listener_display_form`, `qhat_form` (values from r5 §2.5-2.7, spec §1.5).
After review-m4: `g0_glare_to_LP` resized to [−0.012, −0.0035]; `reader_confidence_form` added; `own_synergies` is
`newborn`, `face_channels` `generic` (fit definition), `embedding_dims` `generic` (engineering).

## M6 (offline part): the Claude coupling (`omega/`)

Spec §1.8. Nothing calls the real `claude`: the tests drive `tests/fake_claude.py`, which mimics the CLI's
stream-json output and session files under a temporary HOME.
- `state/types.py` gained the prompt objects: `TranscriptText` (only from his `Utterance` or a `ChosenReply`),
  `Marker` (only from the INNATE marker template, silence rounded to 5 s), `Snippet` (only from stored
  `TranscriptText`), and `ChosenReply` (the winning draft, made only in `omega/pool.py`). All are Ω. The state reads
  none of them; it hears the agent only as `OwnHeard`, made at playback, through the five ports (F19).
- `omega/instruction.txt`, `omega/lines.py`: the constant instruction, the three fork lines and the snippet
  template. `text_digest()` must equal the operator switch `claude_text_approved` (he reads and approves the text).
  Neither holds a state value, a label or a number.
- `omega/isolation.py`: `OmegaConfig.from_operator` refuses (Unanswered / ValueError) until Q34 items 1, 2, 3, 7,
  8, 9 and the text approval are answered and `claude_daily_cap` is a positive number. The CLI flags are the CLI
  equivalents of the spec's `ClaudeAgentOptions`: `--setting-sources ""`, `--tools ""`, `--strict-mcp-config` with
  no servers, `--permission-mode default`, `--model`/`--effort` from the switches, `--system-prompt` the
  instruction, stream-json in and out with partial messages, `--resume <canonical> --fork-session`; never `--bare`.
  Environment: `DISABLE_AUTOUPDATER=1` always, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` per switch; effort,
  thinking-budget, output-cap and model overrides removed. The working directory must be empty, with no CLAUDE.md in
  it or above it.
- `omega/transcript.py`: the window (oldest turns dropped first; instruction + window + snippets + message + fork
  line <= `context_tokens_max`, tokens estimated conservatively at 3 UTF-8 bytes per token until M1 measures the
  CLI's count), the canonical `.jsonl` writer, the A11 byte check, and the F14 / F17 / compaction check of a fork's
  own session file.
- `omega/pool.py`: the warm pool (forks spawned idle on the canonical transcript), the daily cap (persisted calls
  per day; silent at the cap), streaming (text deltas only), the scoring deadline (0.5 s after the first draft's
  first sentence or 3.0 s after his turn end; none by then: silent), losers killed by SIGKILL to the process group
  and replaced in the background (never more than `claude_max_processes` = 4), the cut at two sentences or 60 words,
  interruption (`interrupt()`), fallback 1 (line in the system prompt), fallback 2 (pool 3 -> 2 -> 1 on limit
  signals or slow first sentences, then silence until the limit resets; grows back after 30 min), fallback 3
  (silence when no process answers). There are no hand-written words anywhere (D88): every fallback is silence. A11
  failures stop the route for the session; compaction makes the turn silent. Fork session files are deleted at the
  next idle moment. Telemetry goes to `Pool.log` only.
- `omega/retrieval.py`: <= 3 snippets, relevance (from `slow`) minus 1/7 per day of age; nothing if `send_snippets`
  is off. `omega/scorer.py`: the scoring interface; the world model is not built, so every draft scores 0 and the
  earliest first sentence wins.

INNATE.lock gained (a reviewed change): `claude_max_processes` (4) and `token_estimate` (3 bytes per token, 200
tokens kept for his next message in the pre-written window). `config/operator.py` gained `claude_text_approved`, and
`require` takes an optional switch table (tests pass an answered copy; the engine always reads `SWITCHES`).

**Not built yet:** the `omega` process entry point and its unix socket to `slow`; the 𝓜 draft score; `p_name.py`;
the measured done-checks (p50/p90 latency, calls and tokens per call, F19 on replayed sessions), which need the real
CLI on the Mac after the operator's answers. Not exact: the spec names the Python Agent SDK; it is not installed in
this session, so the process speaks the CLI's stream-json protocol with the equivalent flags (the SDK spawns the same
CLI). The real CLI's event names for a usage limit (`rate_limit_event` with status `rejected`, or an error result
naming a limit) and for compaction (`system` / `compact_boundary`) are taken from the documentation and checked at M1.

## M8 (offline part): store, retention, replay and nightly learning (`memory/`, `learn/`)

Spec §1.9, §1.10. Nothing here has seen a recorded session: the tests write small synthetic sessions into a
temporary store (`tests/synth_store.py`); the store path is never inside the checkout (the CI data guard).
- `memory/store.py`: the feature and transcript store. `Store.open_session` refuses until the operator answered Q34
  item 6 (`feature_retention_days`, `keep_slot_snippets`: no live session before). `SessionWriter.append` takes only
  floating-point arrays of a registered stream (INNATE `store_schemas`: u, f_der, breath, y, y_bar, rendered,
  own_face, voice phrase features, the 2-Hz body snapshot, own loads, display drivers, xi_A, his 20-s lateral trace,
  z_T, state_T/F/K), written float16 and read back as memory maps; int16 PCM, uint8 pixels, bytes, 3-D blocks, wrong
  widths and files above a schema's session size (4 h) are refused before anything is written. There is no audio or
  image method or schema. Text enters only as `TranscriptText` (with word timestamps), events and Ω records with
  fixed keys and value types. `check_a12` / `enforce_a12` (A12, `invariants/asserts.check_a12`): only registered
  file names, no media magic number in a file's first 16 bytes, no file above its schema size; a hit is quarantined
  and stops the night with a message for the operator. `live.lock` and `replay.lock` exclude each other.
- `memory/retention.py`: the window comes from `feature_retention_days` (7, 30, or None = until he deletes them).
  **Before his answer it deletes nothing** and reports every session older than the default 30 days (a deletion
  cannot be undone, a keep can; and no new session can open meanwhile). After it: a session past the window loses its
  arrays, snapshots, Ω records and transcript; the lines episode slots reference (`reference_snippets`, <= 3 per
  slot) are kept in `consolidated/snippets.jsonl` if `keep_slot_snippets`, else dropped.
- `memory/retrieval_index.py`: the snippet index (identity x the encoder's e[64] x time; <= 3 consecutive lines per
  snippet, from retained transcripts and kept slot lines) and `RetrievalQuery` ([grad D 6; N-hat 3; concept
  posterior 64] -> 64, untrained 0, so relevance is 0 and `omega/retrieval.retrieve`'s recency decides).
- `memory/replay.py`: `Replay.may_start` needs the new operator switch `nightly_schedule` (M8 Ask: hours and idle
  time; unanswered, no replay), no live session, the Mac idle for the approved time, the hour inside the window
  (midnight wrap allowed) and the disk above the 10 % floor; `run` then checks A12, takes the replay lock, runs
  retention, loads the closed, unflagged, unreplayed sessions at their 2-Hz ticks (his 30-Hz face is read from the
  memory map at the ticks only) and runs the steps. `Budget` (INNATE `replay_budget`: 3600 s, 2 GB) is checked before
  every step with a 4x working estimate of the night's data and inside every gradient loop; a step that reaches a
  budget is undone and every later step deferred (the sessions stay unreplayed). Sessions flagged by A5 or A14 are
  skipped.
- `learn/weights.py`: the general learning biases: sample weight 1 + 3 min(1, D_p/0.05) (S48), learning rate x
  exp(-0.5 r_bar) with r_bar the night's mean own drop-event amplitude, gradient clip 1, pull 0.1 to theta_0.
  `ALLOWED_WEIGHT_SIGNALS` = the body snapshot's D_p and the own drop amplitudes; `TARGET_SOURCES` lists what each
  objective's target is computed from, none of it his face, gaze, presence or a duration.
- `learn/objectives.py`, `learn/nightly.py`, `learn/projections.py`: the steps of §1.9 on the stubs' fixed shapes:
  (2) Pi-tilde on the agent's own face -> own loads (reader_own; reader_his is the same own inverse on his read
  channels), (3) calibration (b_read from low-need moments, tau 1 for three sessions, then 6, or 60 above V-hat 0.20;
  sigma_id from the MAD of the last 6 sessions, floored at 0.25 sigma_ref; sigma_ref from the agent's own rendered
  output), H_id (ridge 2 on the population reader's decoding, after 400 utterances; `readers.HeadId`), the adapter
  (separated reports only, |.| <= 0.15; `readers.Adapter`), word -> V (threat-reflex teacher over 3 s), (4) W and
  Gamma(3,4) by L_A, projected after every step under the smallest |omega_g| of every known person and the new-person
  prior, (5) Delta by L_display (own legibility through Pi-tilde, 0.1 |delta|^2, own-display mask after every step),
  (8) omega by omega_rule, then E raised to its set point. After every step `check_all` runs A6 (cone latch for
  every omega), A7 (every basis and Delta), A8 and the carried-level ranges; a violating step is undone and logged.
  The weights, theta_0 and the last valid copy go to `consolidated/learned*.npz`, the latches to `persons.json`.
- INNATE.lock gained (a reviewed change): `store_schemas`, `store_limits` (generic engineering), `replay_budget`,
  `replay_sgd` (engineering: step size 0.05, 200 steps, first-night initial scale 0.01), `replay_windows_s` (fit
  definition: 3-s teacher, 20-s H_id, 2-s anticipation), `appraisal_objective_l2`, `display_objective`,
  `calib_initial` (bias; r5 §2.6-2.7, r6 §2.1). `config/operator.py` gained `nightly_schedule`.

**What is not exact, and why**
- Not built, so skipped and reported: step 1 (the world model), step 6 (L_w), step 7 (the scorer and the retrieval
  query by J, which needs the world model's rollout), 𝒜's own likelihood in step 4 (unspecified beyond "by
  likelihood" and reading z_T, which is 0 until the world model exists), and L_display's 0.3-weighted anticipation
  term (it needs the anticipation head). These stubs keep their shapes.
- Delta's open synergies (18 x 33) start at 0 in the M4 stub, a stationary point where no gradient flows; the first night
  initialises W1, W2 and the synergy matrix at scale 0.01 (seeded, masked) and that becomes its theta_0.
- Pi-tilde's pull target is the stub's start (0), not a ridge inverse of Pi_0 (which maps drivers, not loads).
- H_id reads the 28 read channels (his LP, CR, BU_L, RHY, BRE masked), not r6's 15; b_read and sigma_id have the
  same 28 entries. The adapter and H_id are trained and saved but not yet read by the body (it reads the
  population reader alone).
- E is restored to its set point (0.7) if it fell below it, never lowered; the spec says only "restored".
- No replay step writes the cone's learned cross entries (§1.9 lists none); A6 is checked after replay anyway.
- A deferred night leaves its sessions unreplayed, so the next night learns the completed steps on them again.

## M9 (scaffolding): the evaluation battery (`eval/`, outside the engine)

Spec §5, §6 M9. `eval/` is never imported by `engine/` (tests/test_imports.py, tests/test_eval_flist.py) and carries
no affect label (the lint scans it). Every test is judged on internal state (body fields, drive, gates, the
partner-caused part y - ybar, the ledger's x2 and frames changed, T-state digests, assertion failures), never on how
closely the agent's face matches a human face. In this session it runs only on synthetic stand-ins, as a harness
test; those runs are marked `synthetic` and are not evidence.
- `eval/registry.py`: each prediction is written to `predictions/<test_id>.json` with a UTC timestamp and SHA-256
  before its run; `start_run` refuses a missing prediction or one not strictly older than the start; `score`
  refuses one missing, changed after the start (hash against the start record), re-registered with new content, or
  a hash-chained `log.jsonl` that was edited; a run is scored once. The criterion (eq / lt / ge / abs_le / monotone
  / gt_quantile / all / ...) is part of the prediction and is applied mechanically.
- `eval/results.py`: results are JSON / CSV summaries (no arrays, <= 1 MB) with the `affect-eval-*` schema marker; a
  synthetic result is refused anywhere under research/build/results/. The CI data guard (`tools/ci.py`) now admits
  there only Markdown and such unmarked-synthetic eval/ summaries (it refused every non-Markdown file before).
- `eval/drive.py`: one `ShadowPair` session with hooks (lesion, steering step, mirror partner, face transform) and the
  readouts. `eval/switches.py`: the documented lesion switches of §5.2 (g <- 1, g_o <- 1, L_d <- 0, q-hat <- 0, D_tau
  removed, ledger lags 0-3 s, kappa 1, P_name removed, G_k <- 0 on smile_laugh) through each part's own `disabled`
  state or a rebuilt ledger, each with a sham of equal size (an equal-norm change of the turn model's weights, which
  no route reads at this build; G_k <- 0 on the zero-ceiling channels for the echo gain). Four §5.2 rows are listed
  as not built (turn model, sign prior, calibration / H_id, partner anchor) and refuse to run.
- `eval/lesions.py` (E1: intact, lesioned, sham per instance; means and full distributions; >= 20 instances outside
  a synthetic run), `eval/steering.py` (E2: K, h_word, N-hat's V coordinate, omega_g at +-5 doses with a random
  direction of equal norm in the same block, applied to both runs, A14 restarted at the step; input clamps with an
  exact T-state-digest invariance), `eval/surrogates.py` (E3: pooled block-mean slopes of the conditioned output x2
  at 2 s / 10 s / 1 min against segment-shuffle and data-sliding, both required, plus partner-swap,
  timing-resample, and month-swap only with >= 30 sessions >= 28 days apart; an engine re-run path keeps words fixed),
  `eval/mirror.py` (the mirror-only partner against no partner), `eval/f22_delayed_copy.py` (F22 ledger-only, every
  delay batched in one ledger; `--pilot` prints the §5.5 plan).
- `eval/flist.py`: every F of the spec's §5.1 table (checked against the table) with its test, data source (Seamless,
  his M2 recordings, live, replayed, nightly, runtime) and machine / stage. `eval/planner.py`: guard (refuses a
  sitting predicted above 5 h without split / approved, above 6 h without the operator's recorded answer, above 6 GB),
  plan (packs resumable chunks into sittings of <= 5 h), and §5.5's F22 recipe (channels over 8 cores, split by
  channel, subsample to 25 people, else ask).
- `make eval-dry` (`eval/dry_run.py`, about 4 min): registers 24 predictions, then runs every harness on stand-ins
  into a temporary directory. On the stand-ins 19 of 24 are met. The five not met are reported, not hidden: N-hat's V
  direction moves D_p less than a random (V, A, T) direction of equal norm (the negative doses clip at 0); under G_k <-
  0 on smile_laugh a small 2-s coupling of LP remains above the segment-shuffle 95th percentile (the held cone's
  diagonal); under the mirror-only partner the ledger changes 33 % of frames and FR, EN drift monotonically over the
  6-min run (T state bit-identical to no partner, slopes <= 0.48 c); F22 on BI leaves the copy at about 3 c on a 12-min
  stand-in (the known M0 finding, tests/test_ledger_injected.py xfail). None of this is evidence.

**Not built here:** `eval/events.py` and every driver that needs recorded dyads (F1's `f01_bounds.py`, F2, F9's event
classes, F15, F16, F24) or live sessions; they plug into these harnesses at M3 / M4 / M7 on the Mac.

## How to run

```
make ci              # data guard, label lint, pytest (about 2 min)
make regress-full    # also the full 2-h reference regressions, 10 Hz and 30 Hz (several minutes)
make eval-dry        # every eval/ harness end to end on synthetic stand-ins (about 4 min; not evidence)
python -m pytest -q  # tests only
```

## What comes at M1, on the Mac

`uv lock` and the pinned environment; research/build/week0.md, written by `tools/week0/` (`make week0`; one script
per check of the spec §6 M1 table, thresholds applied by `tools/week0/thresholds.py` from INNATE `m1_thresholds`,
each refusing until its operator answer in `config/operator.py`; research/build/handoff.md step 7); the
deny-network profile `config/sandbox.sb` and A16; `models.lock`; the Plan A `fast` process timed under full load. The M4 done-checks that need recorded partners
(F1, F2, F5, F9, F10, F18, F22 on Seamless and his M2 recordings; A1-A9 silent on 20 h) run on the Mac.
