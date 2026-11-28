"""Operator switches (spec §7.3): an unanswered switch is not used."""
import pytest

from engine.config import operator as op


def test_unanswered_refuses():
    with pytest.raises(op.Unanswered, match="nightly_schedule"):
        op.require("nightly_schedule", "dyad_streams")
    with pytest.raises(op.Unanswered, match="tts_engine"):
        op.require("tts_engine")


def test_answers_of_2026_11_28():
    """D94-D97: Q30 widens the dyad streams; Q34 items 1-10 answered as recommended, language English."""
    sw = op.require("dyad_streams", "claude_daily_cap", "conversation_language", "claude_test_calls_m1",
                    "account_training_use_checked", "feature_retention_days")
    assert sw["dyad_streams"] == {"FAUValue", "is_valid", "transcript", "head_pose", "gaze", "voice_features"}
    assert sw["claude_daily_cap"] == 450 and sw["conversation_language"] == "en"
    assert sw["claude_test_calls_m1"] is True and sw["feature_retention_days"] == 30
    assert sw["account_training_use_checked"]


def test_answers_of_2026_11_28_second_set():
    """D104: Q36 A (text kept, approved by digest), Q35 revision 2 with the floor, Q4 I0, Q37 U0; Q1 still open."""
    from engine.omega import lines as L
    sw = op.require("claude_text_approved", "safety_net", "speak_first_limits", "usage_report")
    assert sw["claude_text_approved"] == L.text_digest()
    assert sw["safety_net"] == "scaled_rev2_with_floor"
    assert sw["speak_first_limits"] is None and sw["usage_report"] == "weekly_operator_only"
    with pytest.raises(op.Unanswered):
        op.require("voice")
