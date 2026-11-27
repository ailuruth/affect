"""Operator switches (spec §7.3): an unanswered switch is not used."""
import pytest

from engine.config import operator as op


def test_unanswered_refuses():
    with pytest.raises(op.Unanswered, match="claude_text_approved"):
        op.require("claude_text_approved", "dyad_streams")
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
