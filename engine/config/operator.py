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
    "dyad_streams": Switch(frozenset({"FAUValue", "is_valid", "transcript"}), "Q30", False,
                           "D70 as it stands (the current approval)", True),
    "own_display_mask": Switch(True, "Q31", False, "built as recommended", True),
    "own_rise_brow": Switch(True, "Q33", False, "built as recommended", True),
    "restore_lost_behaviours": Switch((), "Q32", False, "none", True),
    "claude_model": Switch("haiku", "D84", True, "as listed"),
    "effort": Switch("low", "D84", True, "as listed"),
    "pool_size": Switch(3, "D84", True, "as listed"),
    "send_text_to_anthropic": Switch(True, "Q34 item 1", False, "Claude route off"),
    "send_snippets": Switch(True, "Q34 item 1", False, "Claude route off"),
    "claude_daily_cap": Switch(None, "Q34 item 2", False, "Claude route off (he sets the value)"),
    "nonessential_traffic_off": Switch(True, "Q34 item 3", False, "Claude route off"),
    "downloads_approved": Switch({"models": True, "seamless": True}, "Q34 item 4", False, "no download"),
    "dyad_fit_enabled": Switch(True, "Q34 item 4", False, "no fit"),
    "conversation_language": Switch(None, "Q34 item 5", False, "no live session"),
    "feature_retention_days": Switch(30, "Q34 item 6", False, "no live session"),
    "keep_slot_snippets": Switch(True, "Q34 item 6", False, "no live session"),
    "account_training_use_checked": Switch(None, "Q34 item 7", False, "Claude route off"),
    "overage_confirmed_off": Switch(True, "Q34 item 8", False, "Claude route off"),
    "context_tokens_max": Switch(4000, "Q34 item 9", False, "Claude route off"),
    "hub_offline_after_download": Switch(True, "Q34 item 10", False, "always on at runtime", True),
    "tts_engine": Switch(None, "Q1", False, "speech off"),
    "voice": Switch(None, "Q1", False, "speech off"),
    "face_look": Switch("neutral_placeholder", "Q2", False, "placeholder", True),
}


class Unanswered(RuntimeError):
    pass


def require(*names: str) -> dict:
    """Values of the named switches, or Unanswered naming every missing answer."""
    missing = [f"{n} ({SWITCHES[n].question}: {SWITCHES[n].before_answer})" for n in names
               if not (SWITCHES[n].answered or SWITCHES[n].usable_before_answer)]
    if missing:
        raise Unanswered("waiting for the operator: " + "; ".join(missing))
    return {n: SWITCHES[n].value for n in names}
