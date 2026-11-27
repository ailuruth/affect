# engine (milestones M0, and the offline parts of M4 and M6)

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

## How to run

```
make ci              # data guard, label lint, pytest (about 2 min)
make regress-full    # also the full 2-h reference regressions, 10 Hz and 30 Hz (several minutes)
python -m pytest -q  # tests only
```

## What comes at M1, on the Mac

`uv lock` and the pinned environment; research/build/week0.md, written by `tools/week0/` (`make week0`; one script
per check of the spec §6 M1 table, thresholds applied by `tools/week0/thresholds.py` from INNATE `m1_thresholds`,
each refusing until its operator answer in `config/operator.py`; research/build/handoff.md step 7); the
deny-network profile `config/sandbox.sb` and A16; `models.lock`; the Plan A `fast` process timed under full load. The M4 done-checks that need recorded partners
(F1, F2, F5, F9, F10, F18, F22 on Seamless and his M2 recordings; A1-A9 silent on 20 h) run on the Mac.
