# engine (milestones M0 and the offline part of M4)

The engine of research/build/spec.md (build core: research/foundations/design-cayley-ledger.md, revision 9.2).
Nothing here touches a camera, a microphone, a model, Claude or the network. All tests use small synthetic arrays;
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
  amplitude 0.40 qhat, q_trace, the sigh (own noise draw), L_d and qhat evaluation; every drive change recorded for
  A14, whose fail-safe freezes the body.
- `readers.py`: untrained stubs with fixed shapes: a hashed bag-of-words placeholder for the MiniLM → 64-d encoder,
  Lambda, the population word reader, word → V, surprisal, pi_topic, the own-body reader on his masked face and on
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
- Own laugh: the spec writes a_laugh = 0.40 qhat g_o and also g_o y_o|smile_laugh at assembly; applying both would
  give g_o². Here the free display carries 0.40 qhat (T) and g_o multiplies it once at assembly, at render time.
- A_F has no formula in the spec ("slow loudness and motion"): held at 0.
- N_L: the spec does not define "low-information"; every utterance can only raise N_L (it decays with tau 30 min).
- "Addressed" utterances (h_word) are all of his; "partner-initiated" (I) means not directly after an agent turn.
- E1 events are stamped at the 2-Hz tick (≤ 0.5 s after the utterance end).
- The fast gear's 4-s low-pass starts at 0, as the reference; the shadow's g_at is 0 (b_id has no gaze baseline).
- Without the own-face tracker (M2), each run's own previous rendered output stands in for its own-face observation.
- G0's LP ← f_glare (−0.035) uses 86 % of LP's 2-min charged budget as an unsigned pair (weight 0.3); if the M3
  dyad prior signs LP–BL as a toward pair (weight 1) it is 0.035 > F_1 s_X c_LP = 0.012 and A6 fires (for the spec
  owner).
- The type trace follows data flow only; a branch on a T value from a port first hid I_lp from downstream(P5) (the
  F19 test caught it; the update is now branch-free). It runs on synthetic data with small random stub weights.
- Not built here: 𝓜, mu and slots (z_T = 0), the turn model's inputs, prosody/WORLD (A9's per-phrase part), visemes,
  blink, own head micro-motion gating, TranscriptText/Marker/Snippet (M6), the calibration readers (b_read, sigma_id
  are carried, unused), online learning, the process split and its entry points.

**INNATE.lock** gained (a reviewed change): `cone_away_caps`, `cone_lateral_rows`, `own_synergies`,
`derived_feature_sign_as`, `face_channels`, `echo_gate_unread`, `p_name_max`, `g0_glare_to_HG`, `g0_glare_traces`,
`appraisal_return_channels`, `appraisal_orient_basis`, `pi0_rise_voice`, `pi0_drop_row`, `pi0_word_latch_row`,
`pi0_activation_row`, `pi0_low_energy_row`, `pi0_progress_drop_row`, `pi0_driver_shape`, `appraisal_net_shape`,
`display_delta_shape`, `embedding_dims`, `listener_display_form`, `qhat_form` (values from r5 §2.5-2.7, spec §1.5).

## How to run

```
make ci              # data guard, label lint, pytest (about 2 min)
make regress-full    # also the full 2-h reference regressions, 10 Hz and 30 Hz (several minutes)
python -m pytest -q  # tests only
```

## What comes at M1, on the Mac

`uv lock` and the pinned environment; `tools/week0/` and research/build/week0.md; the deny-network sandbox and A16;
`models.lock`; the Plan A `fast` process timed under full load. The M4 done-checks that need recorded partners
(F1, F2, F5, F9, F10, F18, F22 on Seamless and his M2 recordings; A1-A9 silent on 20 h) run on the Mac.
