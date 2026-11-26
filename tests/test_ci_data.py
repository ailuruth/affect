"""CI receives synthetic arrays only (spec §7.6)."""
from pathlib import Path

from tools.ci import data_violations

ROOT = Path(__file__).resolve().parents[1]


def test_checkout_has_no_recorded_data():
    assert data_violations(ROOT) == []


def test_guard_fires(tmp_path):
    (tmp_path / "store").mkdir()
    (tmp_path / "store" / "s.f16").write_bytes(b"x")
    (tmp_path / "big.npy").write_bytes(b"0" * (1024 * 1024 + 1))
    (tmp_path / "small.npy").write_bytes(b"0")
    assert {p for p, _ in data_violations(tmp_path)} == {"store/s.f16", "big.npy"}
