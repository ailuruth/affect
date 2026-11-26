"""Operator switches (spec §7.3): an unanswered switch is not used."""
import pytest

from engine.config import operator as op


def test_unanswered_refuses():
    with pytest.raises(op.Unanswered, match="claude_daily_cap"):
        op.require("claude_daily_cap", "dyad_streams")
    assert op.require("dyad_streams")["dyad_streams"] == {"FAUValue", "is_valid", "transcript"}
