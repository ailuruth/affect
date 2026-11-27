"""Operator switches (spec §7.3). Each switch tied to an open question carries `answered`. A switch whose question
is unanswered is not used: code paths that depend on it refuse to run (`require`) and say which answer is missing.
Defaults are the recommendations the code is written for; they take effect only when the operator answers.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Switch:
    value: object
    question: str
    answered: bool
    before_answer: str
    usable_before_answer: bool = False   # the spec builds on the recommendation until answered (Q30-Q33, Q2, Q34.10)


SWITCHES = {
    # Q30 answered (D95): head pose, gaze and voice features (pitch, loudness, timing as numbers) added, on his Mac
    # only, no labels. Exact Seamless file names for head and gaze are verified on the M3 pilot; voice features are
    # computed from the audio on the Mac file by file and the audio is discarded (only the numbers are kept).
    "dyad_streams": Switch(frozenset({"FAUValue", "is_valid", "transcript", "head_pose", "gaze", "voice_features"}),
                           "Q30", True, "D70 as it stands (the current approval)", True),
    "own_display_mask": Switch(True, "Q31", True, "built as recommended", True),
    "own_rise_brow": Switch(True, "Q33", True, "built as recommended", True),
    "restore_lost_behaviours": Switch((), "Q32", True, "none", True),
    "claude_model": Switch("haiku", "D84", True, "as listed"),
    "effort": Switch("low", "D84", True, "as listed"),
    "pool_size": Switch(3, "D84", True, "as listed"),
    "send_text_to_anthropic": Switch(True, "Q34 item 1", True, "Claude route off"),
    "send_snippets": Switch(True, "Q34 item 1", True, "Claude route off"),
    "claude_test_calls_m1": Switch(True, "Q34 item 1 (M1 test calls only)", True, "no Claude test call"),
    # Q34 item 2: "accept, with a daily cap"; set at the expected regular use, the operator can change the number.
    "claude_daily_cap": Switch(450, "Q34 item 2", True, "Claude route off (he sets the value)"),
    "nonessential_traffic_off": Switch(True, "Q34 item 3", True, "Claude route off"),
    "downloads_approved": Switch({"models": True, "seamless": True}, "Q34 item 4", True, "no download"),
    "dyad_fit_enabled": Switch(True, "Q34 item 4", True, "no fit"),
    "conversation_language": Switch("en", "Q34 item 5", True, "no live session"),
    "feature_retention_days": Switch(30, "Q34 item 6", True, "no live session"),
    "keep_slot_snippets": Switch(True, "Q34 item 6", True, "no live session"),
    "account_training_use_checked": Switch("the operator checks his account setting himself (answer of 2026-11-28)",
                                           "Q34 item 7", True, "Claude route off"),
    "overage_confirmed_off": Switch(True, "Q34 item 8", True, "Claude route off"),
    "context_tokens_max": Switch(4000, "Q34 item 9", True, "Claude route off"),
    # SHA-256 of engine/omega/instruction.txt and the three fork lines, as he read and approved them (spec §6 M6 Ask;
    # engine/omega/lines.py `text_digest`). Any change to that text needs his approval again.
    "claude_text_approved": Switch(None, "Q34 (constant instruction and fork lines)", False, "Claude route off"),
    # M8 Ask: when nightly replay may run (local hours of the window, and how long the Mac must have been idle).
    "nightly_schedule": Switch({"start_hour": 2, "end_hour": 6, "idle_min_s": 1800.0}, "M8 Ask (nightly schedule)",
                               False, "no nightly replay"),
    "hub_offline_after_download": Switch(True, "Q34 item 10", True, "always on at runtime", True),
    "tts_engine": Switch(None, "Q1", False, "speech off"),
    "voice": Switch(None, "Q1", False, "speech off"),
    "face_look": Switch("neutral_placeholder", "Q2", False, "placeholder", True),
}


class Unanswered(RuntimeError):
    pass


def require(*names: str, switches: dict | None = None) -> dict:
    """Values of the named switches, or Unanswered naming every missing answer. `switches` defaults to SWITCHES
    (tests pass an answered copy; the live engine always reads SWITCHES)."""
    sw = SWITCHES if switches is None else switches
    missing = [f"{n} ({sw[n].question}: {sw[n].before_answer})" for n in names
               if not (sw[n].answered or sw[n].usable_before_answer)]
    if missing:
        raise Unanswered("waiting for the operator: " + "; ".join(missing))
    return {n: sw[n].value for n in names}
