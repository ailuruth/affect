"""Every innate and generic constant of the engine, in one table (spec §3.3; A10, A15).

Each entry: name, value, unit, source section, category, subtype (only for `generic`), one-line why.
Categories: body, reflex, newborn, ceiling, bias, operator, generic. Generic subtypes: decision,
engineering, fit definition. A generic value names no scene, user type or event and acts the same at
every moment (D88); test tolerances are not here (they belong to eval/config.py).

INNATE.lock is the canonical serialisation of this table: JSON, keys sorted, floats by Python repr,
arrays as nested lists, UTF-8, no whitespace. Regenerate with `python -m engine.config.innate --write`;
A10 compares the file with this module at every start.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

from engine.config.channels import (APPRAISAL_SUP, ONSET_LOBE_FACTOR, POOLED_MAX, RHO, TABLE)

CATEGORIES = frozenset({"body", "reflex", "newborn", "ceiling", "bias", "operator", "generic"})
GENERIC_SUBTYPES = frozenset({"decision", "engineering", "fit definition"})
LOCK_PATH = Path(__file__).with_name("INNATE.lock")


@dataclass(frozen=True)
class Constant:
    name: str
    value: object
    unit: str
    source: str
    category: str
    why: str
    subtype: str = ""


def _ledger_keys() -> list:
    """(window s, lag s): 2-s window lags 0-3 s (5); 10-s window 0-300 s by 5 s (61); 60-s window 0-300 s by 10 s (31)."""
    keys = [[2.0, l] for l in (0.0, 0.5, 1.0, 2.0, 3.0)]
    keys += [[10.0, float(l)] for l in range(0, 301, 5)]
    keys += [[60.0, float(l)] for l in range(0, 301, 10)]
    return keys


_C = Constant
_TABLE = (
    # ------------------------------------------------------------------ per-expression copy ceilings
    _C("channel_codes", list(TABLE.codes), "-", "spec §1.1; r6 §2.1", "ceiling", "order of every [33] array"),
    _C("channel_groups", list(TABLE.groups), "-", "spec §1.1", "ceiling", "muscle and signal groups of the channels"),
    _C("channel_signs", list(TABLE.signs), "-", "spec §1.1", "ceiling", "one-sided [0, 1], signed [-1, 1], or zero ceiling"),
    _C("channel_c", list(TABLE.c), "nominal range", "spec §1.1; Q22", "ceiling", "innate ceiling toward the partner per channel"),
    _C("channel_G", list(TABLE.G), "per unit onset", "spec §1.1; S43", "ceiling", "frozen fast gain per channel"),
    _C("channel_s_C", list(TABLE.s_C), "fraction of c_k", "spec §1.1; r6 §2.1", "ceiling", "cone diagonal share"),
    _C("channel_s_X", list(TABLE.s_X), "fraction of c_k", "spec §1.1; r6 §2.1", "ceiling", "charged cross-entry share"),
    _C("channel_s_A", list(TABLE.s_A), "fraction of c_k", "spec §1.1; r6 §2.1", "ceiling", "appraisal diagonal share"),
    _C("channel_r", list(TABLE.r), "fraction of c_k", "r6 §2.1 J2", "ceiling", "onset-lobe allowance 0.949 G_k/c_k, 0 on signed channels"),
    _C("onset_lobe_factor", ONSET_LOBE_FACTOR, "-", "r6 §2.1 J2", "ceiling", "factor of the onset-lobe allowance"),
    _C("pooled_max", POOLED_MAX, "fraction of c_k", "r6 J3; spec A0", "ceiling", "bound on the additive pooled total of counted routes"),
    _C("cone_seam_rho", RHO, "-", "r6 J3; Lemma S*", "ceiling", "across-session seam factor of the cone"),
    _C("appraisal_band_sup", APPRAISAL_SUP, "-", "r5 §2.1", "ceiling", "sup gain of the 20-90 s band-pass"),
    _C("appraisal_band_s", [20.0, 90.0], "s", "r5 §2.1", "ceiling", "band-pass h_20s - h_90s of the appraisal input"),
    _C("appraisal_cross_max", {"entry": 0.15, "row": 0.25}, "fraction", "r5 §2.6", "ceiling", "away-orthant cross entries of the appraisal bases"),
    _C("cone_trace_tau_s", [20.0, 120.0, 1200.0, 10800.0], "s", "r5 §2.5", "ceiling", "first-order trace time constants of the held cone"),
    _C("cone_trace_shares", [0.0, 0.7, 0.2, 0.1], "-", "r5 §2.5", "ceiling", "F_m, share of s_C per trace"),
    _C("cone_trace_shares_BI", [0.5, 0.5, 0.0, 0.0], "-", "r5 §2.5", "ceiling", "F_m on the inner brow"),
    _C("cone_baseline_tau_sessions", 6.0, "sessions", "r5 §2.5", "ceiling", "b_id moves toward his session mean; centres the cone"),
    _C("cone_cross_budget_weights", {"signed_pair": 1.0, "unmasked_pair": 0.3}, "-", "r5 §2.5", "ceiling", "lambda_kj of the charged cross budget"),
    _C("ledger_kappa", 0.70, "fraction of c_k", "design §2.13 (9.1, 9.2)", "ceiling", "every ledger key holds the toward slope at kappa c_k"),
    _C("ledger_keys", _ledger_keys(), "s", "design §2.13 (9.2); spec §1.6", "ceiling", "97 (window, lag) constraints per channel"),
    _C("ledger_floor", 0.10, "fraction of RMS", "design-g7 ledger7", "ceiling", "a key with |pi| below 0.10 RMS imposes nothing"),
    _C("ledger_tau_budget_s", 1800.0, "s", "design-g7 ledger7", "ceiling", "decay of the running sums S, E, Q"),
    _C("ledger_tau_centre_s", 1800.0, "s", "design-g7 ledger7", "ceiling", "EMA that centres his and the output's window means"),
    _C("ledger_pi_eps", 1e-9, "-", "design-g7 ledger7", "ceiling", "|pi| below this imposes no side of the interval"),
    _C("ledger_evidence_floor", 0.54, "his pi^2 frames at 10 Hz (scaled by f_s / 10)", "design-scaled-safety-net §7.5; D104",
       "ceiling", "initial evidence on every ledger key's E: one minute (600 frames) of his movement at 0.03"),
    # ------------------------------------------------------------------ scaled safety net, revision 2 (Q35, D104)
    _C("governor_kappa", 0.60, "fraction of c_k", "design-scaled-safety-net §7.2", "ceiling",
       "the governor's target slope kappa_g c_k on every channel, key and memory"),
    _C("governor_z", 3.0, "-", "design-scaled-safety-net §7.2", "ceiling",
       "confidence level of the engagement test as a normal multiplier (one-sided p 0.00135)"),
    _C("governor_t_test", True, "-", "design-scaled-safety-net §7.2", "ceiling",
       "the multiplier is Student's t at z's level with n - 1 degrees of freedom"),
    _C("governor_n_req", 2.0, "independent batches", "design-scaled-safety-net §7.2", "ceiling",
       "evidence a key needs before it may engage"),
    _C("governor_batch_W", 2.0, "windows", "design-scaled-safety-net §7.2", "ceiling",
       "batch length of the sandwich and the evidence count, in windows"),
    _C("governor_start_W", 2.0, "windows", "design-scaled-safety-net §7.2", "ceiling",
       "a key counts only from t >= L + start_W W (no pre-session history in its sums)"),
    _C("governor_sigma0", 0.01, "his units", "design-scaled-safety-net §7.2", "ceiling",
       "floor on his window-mean SD (the regressor), the same for every channel"),
    _C("governor_taus_s", [1800.0, 300.0, 60.0], "s", "design-scaled-safety-net §7.2", "ceiling",
       "the three memories of the estimate; latches combine by the largest slope"),
    _C("governor_keys", {"sets": [{"window_s": 10.0, "kind": "step", "lag_step_s": 5.0},
                                  {"window_s": 10.0, "kind": "level", "lag_step_s": 5.0},
                                  {"window_s": 60.0, "kind": "level", "lag_step_s": 10.0}],
                         "max_lag_s": 300.0}, "s", "design-scaled-safety-net §7.2", "ceiling",
       "153 (window, kind, lag) keys per channel and memory, lags 0-300 s"),
    _C("governor_ratchet", True, "-", "design-scaled-safety-net §7.2", "ceiling",
       "a_k never rises within a session once lowered"),
    _C("listener_display_max", 0.45, "nominal range", "spec §1.5.5; A8", "ceiling", "|L_d,k| bound"),
    _C("listener_display_stream_rows", {"head_pose": ["HP", "TILT"], "gaze": ["VG"], "voice_features": ["FR", "EN"]},
       "-", "design §2.1 (9.1); D70; D95", "ceiling",
       "rows of L_d each dyad stream unlocks; a row whose stream is not in dyad_streams is held at 0 (A8)"),
    _C("cone_away_caps", {"entry": [0.25, 0.12, 0.08, 0.04], "row": [0.30, 0.15, 0.10, 0.05]}, "nominal range",
       "r5 §2.5; sims design-g5 A_M, R_M", "ceiling", "away-orthant entry and row caps of the held cone per trace"),
    _C("cone_lateral_rows", ["YAW", "HG"], "-", "r5 §2.5 reflection rule", "ceiling",
       "lateral rows driven by a non-lateral input render opposite his 20-s lateral trace (TILT excluded, charged)"),
    _C("own_synergies", {
        "syn_LP_CR": {"LP": 1, "CR": 1, "LT": 1, "JO": 1, "BU_L": 1, "RHY": 1, "BRE": 1, "FR": 1, "EN": 1},
        "syn_BI_LD": {"BI": 1, "BL": 1, "LD": 1, "CHR": 1, "BU_S": 1, "VG": -1, "HP": -1, "FR": -1, "EN": -1, "RT": -1},
        "syn_BL_LT_LPR": {"BL": 1, "LT": 1, "LPR": 1, "EN": 1, "UL": 1, "F0": 1},
        "syn_BI_BO_UL": {"BI": 1, "BO": 1, "UL": 1, "JO": 1},
        "syn_NW_UL_BL": {"NW": 1, "UL": 1, "BL": 1},
        "syn_JO_EN_RT": {"JO": 1, "EN": 1, "RT": 1}},
       "sign", "r5 §2.5; design §2.5 (9.1, M8); design assembly list", "newborn",
       "the agent's own signed synergies: within-synergy signs only; cross-synergy pairs unsigned and charged"),
    _C("derived_feature_sign_as", {"f_loud": "EN", "f_glare": "BL", "f_laugh": "BU_L"}, "-", "r5 §2.5", "ceiling",
       "a derived input carries its constituent channel's sign"),
    _C("face_channels", ["LP", "CR", "BI", "BO", "LD", "JO", "BL", "UL", "LT", "NW", "LS", "CHR", "LPR", "DIM", "FUN",
                         "PUK", "MCL", "LRO"], "-", "spec §3.1, §3.2; D70", "generic",
       "facial action-unit channels (the D70 data scope): a face pair takes the dyad sign prior or 0", "fit definition"),
    _C("echo_gate_unread", ["LP", "CR", "BU_L", "RHY", "BRE"], "-", "spec §1.5.4; rule 11'", "ceiling",
       "his channels the echo gate never reads, traces included"),
    _C("p_name_max", 0.05, "fraction", "spec §1.3.1 P4; S49", "ceiling", "attenuate-only bound of P_name on a named display"),
    _C("own_laugh_max", 0.40, "nominal range", "spec §1.5.3; A9", "ceiling", "own laugh pattern amplitude bound"),
    # ------------------------------------------------------------------ body
    _C("drive_terms", {"E": [0.7, 0.2, 1.0], "A": [0.0, 0.15, 0.7], "V": [0.0, 0.05, 1.0], "K": [0.0, 0.10, 0.6],
                       "P": [0.0, 0.10, 0.5], "I": [0.0, 0.10, 0.4]},
       "(set point, dead-band, weight)", "spec §1.3 Drive; r5 §2.1", "body", "D(b) = sum w psi(|b - b*| - delta)+; K weight times f_id"),
    _C("drive_psi_power", 2.0, "-", "r5 §2.1", "body", "psi(x) = x^2"),
    _C("Dp_terms", {"scale": 0.8, "V": [0.05, 1.0], "A": [0.15, 0.7], "T": [0.20, 0.5]},
       "(threshold, weight)", "spec §1.3; r5 §2.1", "body", "D_p(N) = 0.8 [psi(V-0.05)+ + 0.7 psi(A-0.15)+ + 0.5 psi(T-0.20)+]"),
    _C("energy_decay_per_min", 0.0004, "1/min", "r5 §2.1", "body", "E falls 0.04 %/min awake; restored only in nightly replay"),
    _C("activation_lexical_gain", 0.5, "-", "r5 §2.1; M6", "body", "A_L <- max(A_L, 0.5 s_lex^2)"),
    _C("activation_lexical_tau_s", 180.0, "s", "r5 §2.1; M6", "body", "decay of A_L"),
    _C("h_word_tau_s", 600.0, "s", "spec §1.3; S20", "body", "decay of the word latch h; no halving"),
    _C("contact_rise_tau_h", 36.0, "h", "r5 §2.1", "body", "K rises (1 - K)/36 h between sessions"),
    _C("contact_in_session_tau_s", 30.0, "s", "design §2.1; S26", "body", "dK/dt = -K f_id e(t)/30 s within a session"),
    _C("contact_presence_factor", {"face_and_spoke_60s": 1.0, "face_only": 0.5}, "-", "design §2.1; S26", "body", "e(t) of the in-session contact term"),
    _C("contact_spoke_window_s", 60.0, "s", "design §2.1; S26", "body", "window for 'has spoken' in e(t)"),
    _C("contact_known_min", 0.3, "f_id", "r5 §2.1", "body", "familiarity above which K_id exists"),
    _C("play_rise_tau_h", 5.05, "h", "r5 §2.1", "body", "P rises (1 - P)/5.05 h"),
    _C("play_qhat_gain", 0.15, "-", "design §2.1; S21", "body", "P <- P (1 - 0.15 qhat) at each of his turns"),
    _C("learn_progress_rise_tau_h", 1.0, "h awake", "r4 §2.1; r5 §2.8", "body", "I rises (1 - I)/1 h awake"),
    _C("learn_progress_gain", 0.5, "-", "r4 §2.1; r5 §2.8", "body", "I <- max(0, I - 0.5 pi_topic) at a partner-initiated utterance"),
    _C("learn_progress_windows", [8, 4], "utterances", "r4 §2.9", "body", "pi_topic = error over previous 8 minus latest 4, floored at 0"),
    _C("word_need_tau_s", 1800.0, "s", "spec §1.3; S39", "body", "decay of N_L per topic slot"),
    _C("event_amplitude_half", 0.02, "drive units", "r5 §2.1", "body", "a = R/(R + 0.02) and S/(S + 0.02)"),
    _C("opponent_mask_factor", 3.0, "-", "spec §1.3; M5", "body", "R' = max(0, R - 3 S)"),
    _C("envelope_shape_s", {"rise": 0.4, "apex_end": 1.5, "decay_tau": 3.0}, "s", "r5 §2.1", "body", "env_drop, env_rise: linear rise, apex, exponential decay"),
    _C("laugh_pattern", {"BU_L": 0.40, "RHY": 0.35, "CR": 0.20, "LP": 0.15}, "per unit", "spec §1.5.3; S18", "body", "own laugh motor pattern"),
    _C("laugh_drive_gain", 0.40, "-", "design §2.1; S18", "body", "a_laugh = 0.40 qhat g_o at each of his turns"),
    _C("inhale_pattern", {"BRE": 0.15, "duration_s": 0.3}, "-", "spec §1.5.3", "body", "pre-speech inhale"),
    _C("laugh_synth_floor", 0.04, "nominal range", "spec §1.7; S47", "body", "theta_L, below it the synthesizer is silent"),
    _C("laugh_synth_am_hz", [4.0, 6.0], "Hz", "spec §1.7", "body", "amplitude modulation band of the source"),
    _C("voice_pause_s", {"comma": 0.20, "sentence_end": 0.40}, "s", "spec §1.7; r6 §6.6", "body", "pauses times the pause factor"),
    _C("voice_onset_after_deadline_s", 0.35, "s", "spec §1.5.6; S50", "body", "speech onset after the scoring deadline"),
    _C("voice_templates", ["statement", "question"], "-", "spec §1.7", "body", "the two innate phrase templates"),
    # ------------------------------------------------------------------ reflexes
    _C("fast_gear_delay_s", 0.45, "s", "spec §1.4; S10, S43", "reflex", "echo lag capture to photon on every channel"),
    _C("fast_gear_onset_tau_s", 4.0, "s", "spec §1.4", "reflex", "E_k = x_d - lp4(x_d)"),
    _C("muscle_filter", {"freq_hz": 4.0, "zeta": 0.8}, "-", "spec §1.4", "reflex", "second-order muscle filter M at assembly"),
    _C("loud_threshold", {"EN": 0.7, "span": 0.3}, "nominal range", "spec §1.2.5", "reflex", "f_loud = (EN - 0.7)+/0.3"),
    _C("reflex_glare_loud_pos_gain", 2.0, "-", "spec §1.3; S41", "reflex", "V_F = g_at max(f_glare, f_loud (1 - 2 f_pos)+)"),
    _C("burst_split_brow_gain", 2.0, "-", "spec §1.2.4; S42", "reflex", "s_cry = min(1, 2 sqrt(BI LD))"),
    _C("burst_mod_band_hz", [4.0, 6.0], "Hz", "spec §1.2.4", "reflex", "modulation depth r of the voiced burst"),
    _C("burst_mod_window_s", 1.0, "s", "spec §1.2.4", "reflex", "sliding spectrum of the envelope"),
    _C("head_envelope_band_hz", [2.6, 6.5], "Hz", "spec §1.4; M3", "reflex", "his head envelope gating own head micro-motion"),
    _C("g0_glare_to_LP", [-0.012, -0.0035], "per unit", "spec §1.5.1; review-m4 Part 2", "reflex",
       "threat-reflex entries of G0 on lip pull, sized to F_m s_X c_LP (charged at weight 1 whatever the dyad prior)"),
    _C("g0_glare_to_HG", [0.25, 0.05], "per unit", "r5 §2.5; design §2.5", "reflex",
       "threat-reflex gaze away from a glare on traces 0 and 1, by the reflection rule"),
    _C("g0_glare_traces", {"LP": [1, 2], "BI": [0, 1], "HG": [0, 1]}, "trace index", "r5 §2.5", "reflex",
       "which cone traces carry the threat-reflex entries"),
    _C("appraisal_return_channels", ["LP", "CR", "BU_L", "RHY", "BRE"], "-", "spec §1.5.2; S44", "reflex",
       "innate return basis basis_return_LP_CR: diagonal s_A c_k omega of the smile_laugh group"),
    _C("appraisal_orient_basis", {"HG_from_f_loud": 0.10, "EN_from_f_loud": -0.10}, "per unit", "r5 §2.6; S44", "reflex",
       "innate orient basis basis_orient: gaze away by reflection and a quieter voice at a sudden loud voice"),
    _C("g0_glare_to_BI", 0.006, "per unit", "spec §1.5.1", "reflex", "threat-reflex entry of G0 on inner brow"),
    _C("sigh_pattern", {"BRE": 0.15, "duration_s": 1.0}, "-", "design §2.1; S35", "reflex", "physiological sigh"),
    _C("sigh_rate", {"per_s": 1.0 / 180.0, "gain": 2.0, "E_ref": 0.5, "E_span": 0.3}, "-", "design §2.1", "reflex",
       "rate 1/3 min x (1 + 2 max(0, 0.5 - E)/0.3)"),
    # ------------------------------------------------------------------ newborn muscle patterns
    _C("pi0_rise_row", {"BI": 0.45, "LD": 0.35}, "nominal range", "spec §1.5.3; S45; Q33", "newborn", "own rise row with lower voice"),
    _C("pi0_rise_voice", {"FR": -0.20, "EN": -0.15}, "nominal range", "r5 §2.7; S45", "newborn", "lower voice of the own rise row"),
    _C("pi0_drop_row", {"LP": 0.55, "CR": 0.45, "FR": 0.35, "EN": 0.25}, "nominal range", "r5 §2.7; S45", "newborn",
       "drop event -> lip pull, cheek, brighter voice (x g_o on the smile_laugh part)"),
    _C("pi0_word_latch_row", {"BI": 0.25, "LD": 0.20, "LP": -0.25, "HG": 0.30, "EN": -0.20, "LAT": 0.15}, "nominal range",
       "r5 §2.7; S45", "newborn", "h_word driver -> brow, depressor, gaze aversion, lower energy"),
    _C("pi0_activation_row", {"UL": 0.20, "BO": 0.15, "FR": 0.15, "RT": 0.15, "BRE": 0.10}, "nominal range",
       "r5 §2.7; S45; M6", "newborn", "A_L driver -> raised lids and outer brow"),
    _C("pi0_low_energy_row", {"UL": -0.30, "FR": -0.25, "EN": -0.25, "RT": -0.15}, "nominal range", "r5 §2.7; S45",
       "newborn", "low energy driver"),
    _C("pi0_progress_drop_row", {"BO": 0.15, "UL": 0.10, "FR": 0.10}, "nominal range", "r5 §2.7; S45", "newborn",
       "learning-progress drop -> interest face"),
    _C("pi0_driver_shape", {"activation_half": 0.2, "h_word_half": 0.15, "low_energy_ref": 0.5, "low_energy_span": 0.3},
       "-", "r5 §2.7", "newborn", "a_A = A_L/(A_L + 0.2); h_d = h/(h + 0.15); e = (0.5 - E)+/0.3"),
    _C("pi0_rise_envelope_s", {"rise": 0.4, "apex_end": 1.5, "decay_tau": 3.0}, "s", "spec §1.5.3", "newborn", "envelope of the own rise row"),
    # ------------------------------------------------------------------ general learning biases
    _C("gate_shape", "monotone additive, exp link, clipped [0, 1]", "-", "spec §1.5.4; S13", "bias", "form of g, g_o and qhat"),
    _C("trace_taus_s", [20.0, 120.0, 600.0], "s", "spec §1.3; S15", "bias", "multi-scale traces D_tau"),
    _C("q_trace_tau_s", 180.0, "s", "spec §1.3", "bias", "trace of qhat"),
    _C("replay_need_weight", {"gain": 3.0, "scale": 0.05}, "-", "spec §1.10; S48", "bias", "sample weight 1 + 3 min(1, D_p/0.05)"),
    _C("lr_gate_coeff", 0.5, "-", "r6 §2.1", "bias", "learning rate x exp(-0.5 r_bar)"),
    _C("grad_clip", 1.0, "-", "r6 §2.1", "bias", "gradient clip in replay"),
    _C("theta0_pull", 0.1, "-", "r6 §2.1", "bias", "pull to the initial weights"),
    _C("pi_tilde_pull", 0.1, "-", "spec §1.9", "bias", "pull of the own inverse to its ridge start"),
    _C("calib_sigma_floor", 0.25, "fraction of sigma_ref", "r6 §2.1", "bias", "sigma_id >= 0.25 sigma_ref, at most x4"),
    _C("calib_mad_factor", 1.4826, "-", "r6 §2.1", "bias", "sigma_id from the median absolute deviation"),
    _C("calib_sigma_sessions", 6, "sessions", "r6 §2.1", "bias", "window of sigma_id"),
    _C("calib_read_tau_sessions", {"low_need": 6.0, "high_need": 60.0, "V_threshold": 0.20}, "sessions", "r6 §2.1; S38", "bias",
       "b_read moves slowly toward a session whose read V exceeds 0.20"),
    _C("head_id_min_utterances", 400, "utterances", "spec §1.3", "bias", "H_id used only after 400 of his utterances"),
    _C("head_id_ridge", 2.0, "-", "spec §1.3", "bias", "ridge lambda of H_id"),
    _C("adapter_bound", 0.15, "-", "spec §1.3", "bias", "per-person adapter outputs in [-0.15, 0.15]"),
    _C("adapter_dim", 16, "-", "spec §1.3", "bias", "identity code size of the adapter"),
    _C("omega_tau_sessions", 60.0, "sessions", "spec §1.9", "bias", "omega_g <- omega_g + (s - omega_g)/60"),
    _C("omega_prior", [0.5, 0.3, 0.2, 0.5], "-", "r5 §2.1", "bias", "per-group omega of a new person"),
    _C("omega_rule", {"offset": 0.3, "rel_gain": 0.7, "rel_scale": 0.6, "h_gain": 1.3, "h_scale": 0.10}, "-", "spec §1.9; S37", "bias",
       "s = clip(0.3 + 0.7 min(1, rho_rel/0.6) - 1.3 min(1, h_bar/0.10), -1, 1)"),
    _C("concepts_dp_lambda", 1.5, "-", "r3 §2.10", "bias", "DP-means penalty"),
    _C("concepts_max", 64, "-", "r3 §2.10", "bias", "at most 64 centroids"),
    _C("mu_ladder", {"groups": 8, "modes": 16, "tau_base_s": 120.0, "tau_ratio": 3.0}, "-", "spec §1.3; r2 §2.5", "bias", "positive leaky modes"),
    _C("slots_shape", {"slots": 128, "width": 128, "tau_days": 30.0}, "-", "spec §1.3; r2 §2.5", "bias", "relationship and episode slots"),
    _C("world_model_init", {"layers": 2, "modes": 128, "modulus_range_s": [1.0, 120.0]}, "-", "r2 §2.5; r3 §2.11", "bias",
       "LRU with innate moduli; phases and couplings learned"),
    _C("appraisal_net_shape", {"inputs": [36, 64, 7, 4], "hidden": 64, "out": 12, "bases": 5}, "-", "spec §1.5.2", "bias",
       "form of the appraisal network and its basis selection softmax"),
    _C("display_delta_shape", {"inputs": 161, "hidden": 128, "out": 18, "bound": 0.3}, "-", "spec §1.5.3; r5 §2.7", "bias",
       "form of the learned open synergies of the free display"),
    _C("embedding_dims", {"encoder": 384, "e": 64, "topic": 16}, "-", "spec §1.2.6, §1.3", "generic",
       "utterance embedding, its fixed projection and the topic code (model sizes)", "engineering"),
    # ------------------------------------------------------------------ operator's call
    _C("own_display_mask", {"zero": ["BL", "LT", "LPR", "NW", "DIM"], "own_rise_only": ["LS", "CHR"]}, "-", "spec §1.5.3; S46; Q31",
       "operator", "learned own-display weights on these channels"),
    # ------------------------------------------------------------------ generic system parameters (§3.3 table)
    _C("theta_end_default", 0.5, "probability", "spec §1.5.6", "generic", "send point on p_end before the val fit", "decision"),
    _C("initiative_beta", 4.0, "-", "spec §1.5.6", "generic", "steepness of the drive-change tilt of the hazard; swept at M9", "decision"),
    _C("initiative_horizon_s", 5.0, "s", "spec §1.5.6", "generic", "comparison horizon of the rollout; swept at M9", "decision"),
    _C("draft_rollout", {"horizon_s": 30.0, "steps": 60}, "-", "spec §1.8", "generic", "horizon of the draft score", "decision"),
    _C("hazard_without_fit_per_s", 1.0 / 60.0, "1/s", "spec §1.10", "generic", "constant hazard only when the dyad fit is off", "decision"),
    _C("alibi_slope_per_day", 1.0 / 7.0, "1/day", "spec §1.9", "generic", "retrieval recency prior", "decision"),
    _C("draft_deadline_s", {"after_first": 0.5, "cap_after_turn_end": 3.0}, "s", "spec §1.8; r6 §6.5", "generic", "latency", "engineering"),
    _C("draft_cut", {"sentences": 2, "words": 60}, "-", "spec §1.8", "generic", "a draft is interrupted here", "engineering"),
    _C("pool_resize", {"p90_s": 3.0, "turns": 20, "window_min": 30.0, "size": 3}, "-", "spec §1.8", "generic", "usage and latency", "engineering"),
    _C("marker_template", {"text": "[no reply from him for N s]", "round_s": 5}, "-", "spec §1.8", "generic",
       "observable silence length for Claude, no state", "engineering"),
    _C("context_window", {"tokens_max": 4000, "snippets": 3, "snippet_tokens": 200}, "tokens", "spec §1.8; Q34 item 9", "generic",
       "transcript window per call", "engineering"),
    _C("claude_max_processes", 4, "processes", "spec §1.8, §2.1", "generic",
       "warm pool plus one replacement; the omega process never runs more Claude Code processes", "engineering"),
    _C("token_estimate", {"bytes_per_token": 3.0, "message_reserve_tokens": 200}, "tokens", "spec §1.8; Q34 item 9",
       "generic", "conservative token count until the CLI's own count is measured at M1; room kept in the "
       "pre-written window for his next message", "engineering"),
    _C("loop_rates_hz", {"fast": 30.0, "own_face": 10.0, "slow": 2.0}, "Hz", "spec §1", "generic", "camera, own face, slow clock", "engineering"),
    _C("ring_buffer_s", 0.6, "s", "spec §1.4", "generic", "echo interpolation by capture time", "engineering"),
    _C("watchdog_ms", {"stall": 200, "ease": 300}, "ms", "spec §1.7", "generic", "page eases to rest and mutes on a stall", "engineering"),
    _C("clock_remap", {"period_s": 60.0, "pings": 30}, "-", "spec §1.2.1", "generic", "page-to-engine clock map", "engineering"),
    _C("assert_tol", {"A1": 1e-6, "A3": 1e-9, "A4": 1e-9, "A4_rel": 1e-6, "A14": 1e-6}, "-", "spec §4.3", "generic", "rounding allowance of runtime asserts", "engineering"),
    _C("ledger_frame_budget_ms", 1.0, "ms", "spec §1.6", "generic", "ledger cost per frame on one performance core", "engineering"),
    _C("governor_rate_hz", 10.0, "Hz", "design-scaled-safety-net §7.2, §7.7", "generic",
       "rate of the governor's sums, batches and gain (window means at the input rate, a held between)", "engineering"),
    _C("governor_frame_budget_ms", 0.5, "ms", "design-scaled-safety-net §7.2", "generic",
       "governor cost per frame on one performance core", "engineering"),
    _C("m1_thresholds", {
        "tracker_p99_ms": [20.0, 30.0], "pipeline_p99_ms": [90.0, 400.0], "clock_offset_sd_ms": [10.0, 33.0],
        "stream_asr": {"p90_s": [0.9, 1.5], "wer": 0.15, "rtf": 0.5, "languages": ["en", "fr"]},
        "utterance_asr": {"rtf": [0.3, 0.5], "wer": [0.12, 0.20]},
        "breath": {"rate_err_silent": 1.0, "share_silent": 0.8, "holds": 0.9, "retest_r": 0.7, "rate_err_talk": 2.0,
                   "share_talk": 0.6, "window_s": 30.0},
        "fast_tick_p99_ms": 5.0, "slow_tick_p99_ms": [50.0, 200.0], "memory_gb": 6.0, "claude_runs": 20,
        "thinking_tokens_max": 0, "sandbox_connections_max": 0, "sandbox_minutes": 10.0,
        "first_sentence_p90_s": [1.5, 3.0], "tokens_per_call": 4500,
        "python": [[3, 12], [3, 14]], "disk_floor_fraction": 0.10, "disk_needed_gb": {"core": 1.0, "models": 4.0}},
       "-", "spec §6 M1 table", "generic", "which fallback the hardware selects; measured, not fitted", "engineering"),
    _C("store_schemas", {
        "u": {"dims": 33, "hz": 30.0}, "f_der": {"dims": 5, "hz": 30.0}, "breath": {"dims": 2, "hz": 10.0},
        "y": {"dims": 33, "hz": 30.0}, "y_bar": {"dims": 33, "hz": 30.0}, "rendered": {"dims": 33, "hz": 30.0},
        "own_face": {"dims": 33, "hz": 10.0}, "voice_phrase": {"dims": 8, "hz": 2.0},
        "body": {"dims": 12, "hz": 2.0}, "own_loads": {"dims": 3, "hz": 2.0}, "drivers": {"dims": 7, "hz": 2.0},
        "xi_A": {"dims": 36, "hz": 2.0}, "cone_lateral": {"dims": 33, "hz": 2.0}, "z_T": {"dims": 161, "hz": 2.0},
        "state_T": {"dims": 512, "hz": 2.0}, "state_F": {"dims": 512, "hz": 2.0}, "state_K": {"dims": 512, "hz": 2.0}},
       "dims, Hz", "spec §1.9 (P7: features only)", "generic",
       "the only array streams the feature store accepts, all float16 (no audio or image type exists)", "engineering"),
    _C("store_limits", {"session_max_s": 14400.0, "text_line_max_bytes": 65536, "slot_lines_max": 3,
                        "magic": ["RIFF", "WAVE", "fLaC", "OggS", "ID3", "ftyp", "\x89PNG", "\xff\xd8\xff", "GIF8",
                                  "\x1aE\xdf\xa3", "caff", "FORM"]},
       "s, bytes", "spec §1.9, A12", "generic",
       "largest session a schema file may hold; text line cap; snippet lines kept per slot; media magic numbers A12 refuses",
       "engineering"),
    _C("replay_budget", {"wall_s": 3600.0, "memory_gb": 2.0, "idle_check": "no live session and the approved idle window"},
       "s, GB", "spec §1.9, §2.4, §6 M8", "generic", "nightly replay stops before either budget is passed", "engineering"),
    _C("replay_sgd", {"lr": 0.05, "steps": 200, "init_scale": 0.01, "seed": 0}, "-", "spec §1.10", "generic",
       "step size, step count and first-night initial scale of every replayed gradient learner", "engineering"),
    _C("replay_windows_s", {"teacher": 3.0, "head_id": 20.0, "anticipation": 2.0}, "s", "spec §1.9; r5 §2.6", "generic",
       "word -> V teacher window after an utterance; H_id face window; the 2-s anticipation of the appraisal objective",
       "fit definition"),
    _C("appraisal_objective_l2", 0.001, "-", "r5 §2.6", "bias", "L_A = E |y_A - (Pi_0 d(t + 2 s) - Pi_0 d(t))|^2 + 0.001 |Gamma(3,4)|^2"),
    _C("display_objective", {"legibility": 1.0, "anticipation": 0.3, "l2": 0.1}, "-", "r5 §2.7", "bias",
       "L_display = E|Pi~(face) - s|^2 + 0.3 E|anticipation|^2 + 0.1 |delta|^2, no partner term"),
    _C("calib_initial", {"sessions": 3, "tau_sessions": 1.0, "need_max": 0.05}, "sessions", "r6 §2.1; S38", "bias",
       "b_read moves fast (tau 1 session) in the first three sessions while the session word need stays below 0.05"),
    _C("gate_basis", {"knot_range": [0.05, 0.80], "count": 7}, "quantile", "spec §1.5.4; S13", "generic", "basis of the monotone additive form", "fit definition"),
    _C("gate_m_ref_percentile", 90.0, "percentile", "spec §3.2; S14", "generic", "scale of g over all laugh onsets", "fit definition"),
    _C("qhat_target", {"level": 0.25, "jaw_band_hz": [3.0, 7.0], "window_s": [0.3, 2.0]}, "-", "spec §3.2", "generic",
       "a listener laugh onset in movement", "fit definition"),
    _C("fit_windows_s", {"g": [0.3, 1.5], "g_o": 3.0, "lambda": [0.5, 5.0], "listener_bins": {"width": 2.0, "span": [0.0, 20.0]}},
       "s", "spec §3.2", "generic", "target extraction windows", "fit definition"),
    _C("sign_prior", {"abs_rho_min": 0.2, "block_s": 60.0}, "-", "spec §3.2", "generic", "which co-variations set a sign", "fit definition"),
    _C("listener_display_form", {"outputs": ["BI", "BO", "LD", "LP", "CR", "RT"], "features": 7, "bin_s": 2.0, "bins": 10,
                                  "turn_events": ["his_utterance_end", "session_start"]},
       "-", "spec §1.5.5; §3.2", "generic", "ridge on (1, V, A, T, Lambda) x time-since bin per turn event (feature anchors; weights fitted from recorded listeners)", "fit definition"),
    _C("turn_model_form", {"base": ["silence_s", "syntactic_completion", "qform_last", "qform_whose"],
                            "au_columns": 23, "people": 2,
                            "stream_inputs": {"head_pose": ["HP", "YAW", "TILT"], "gaze": ["VG", "HG"],
                                              "voice_features": ["F0", "FR"]}},
       "-", "spec §1.5.6, §3.2; D70; D95", "generic",
       "inputs of p_end and the hazard: the base inputs, both people's AU columns, and both people's head, gaze and "
       "pitch channels for each approved dyad stream", "fit definition"),
    _C("qhat_form", {"inputs": ["lam_his_last", "lam_his_prev", "lam_agent_last", "turn_order", "surprisal"]}, "-",
       "spec §1.5.5", "generic", "monotone additive logistic model of the listener-laugh reader", "fit definition"),
    _C("reader_confidence_form", {"measure": "one_minus_predictive_var_ratio", "untrained": 0.0, "range": [0.0, 1.0]},
       "-", "design S39; spec §1.3; review-m4 Part 3", "generic",
       "confidence c = 1 - (reader predictive variance / population variance of the target), per coordinate, fitted "
       "with the population word reader; lowers N_L by c (N_L - r)+", "fit definition"),
    _C("turn_silence_min_s", 0.2, "s", "spec §3.2", "generic", "which gaps are turn opportunities", "fit definition"),
    _C("dyad_split", [0.70, 0.15, 0.15], "fraction", "spec §3.1; harness splits_v2", "generic", "person-disjoint train, val, test", "fit definition"),
)

ENTRIES = {c.name: c for c in _TABLE}
assert len(ENTRIES) == len(_TABLE), "duplicate innate name"


def _plain(v):
    """Validate and normalise a value for canonical JSON (finite floats, ints, str, bool, lists, dicts)."""
    if isinstance(v, bool) or v is None or isinstance(v, str):
        return v
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        if not math.isfinite(v):
            raise ValueError("non-finite innate value")
        return v
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in v.items()}
    raise TypeError(f"innate value of type {type(v).__name__}")


def canonical(obj) -> bytes:
    """Sorted keys, float repr (json's own), nested lists, UTF-8, no whitespace."""
    return json.dumps(_plain(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def table_dict() -> dict:
    out = {}
    for c in _TABLE:
        e = {"value": c.value, "unit": c.unit, "source": c.source, "category": c.category, "why": c.why}
        if c.subtype:
            e["subtype"] = c.subtype
        out[c.name] = e
    return out


def lock_bytes() -> bytes:
    entries = table_dict()
    digest = hashlib.sha256(canonical(entries)).hexdigest()
    return canonical({"entries": entries, "sha256": digest})


def write_lock(path: Path = LOCK_PATH) -> str:
    data = lock_bytes()
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    import sys
    if "--write" in sys.argv:
        print(write_lock())
    else:
        sys.stdout.buffer.write(lock_bytes() + b"\n")
