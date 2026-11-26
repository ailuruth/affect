"""A3 (static), A14 (accounting), A17 (model-hash stub) on small synthetic values."""
import json

import numpy as np
import pytest

from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants.asserts import DriveAccount, InvariantError, check_a3_static, check_a17_model
from engine.state import drives

# ---------------------------------------------------------------------------------------------- A3 static
def _sign_prior(n_in=36):
    S = np.zeros((33, n_in))
    S[np.arange(33), np.arange(33)] = 1.0
    S[20, 21] = 1.0          # a signed pair: + is toward
    S[22, 0] = -1.0          # a signed pair: - is toward
    return S


def test_a3_static_accepts_away_entries():
    M = np.zeros((33, 36))
    M[20, 20] = -0.05        # diagonal <= 0
    M[20, 21] = -0.02        # away on a + pair
    M[22, 0] = +0.01         # away on a - pair
    M[0, 0] = 0.2            # capped row: not A3's business
    check_a3_static(ZERO_CEILING, M, _sign_prior())


@pytest.mark.parametrize("k,j,v", [(20, 20, 0.01), (20, 21, 0.02), (22, 0, -0.01), (25, 3, 0.01)])
def test_a3_static_refuses_toward_entries(k, j, v):
    M = np.zeros((33, 36))
    M[k, j] = v
    with pytest.raises(InvariantError, match="A3"):
        check_a3_static(ZERO_CEILING, M, _sign_prior())


# ---------------------------------------------------------------------------------------------- A14
B0 = {"E": 0.7, "A": 0.1, "V": 0.0, "K": 0.6, "P": 0.3, "I": 0.2}


def _apply(acc, b, drive, term, d):
    acc.record(drive, term, d)
    b[drive] += d
    acc.check(b, drives.drive(b))


def test_a14_accepts_declared_dynamics_with_a_rise():
    b = dict(B0)
    acc = DriveAccount(b)
    _apply(acc, b, "V", "h_word_latch", 0.4)      # D rises within the session: legal
    for _ in range(15):
        _apply(acc, b, "V", "h_word_decay", -0.02)
        _apply(acc, b, "K", "in_session_contact", -0.02)
        _apply(acc, b, "E", "waking_decay", -0.0002)
        _apply(acc, b, "P", "growth", 0.001)


def test_a14_refuses_unattributed_change():
    b = dict(B0)
    acc = DriveAccount(b)
    b["P"] -= 0.1
    with pytest.raises(InvariantError, match="unattributed"):
        acc.check(b, drives.drive(b))


@pytest.mark.parametrize("drive,term,d", [("P", "bonus", -0.1), ("K", "in_session_contact", 0.1),
                                          ("E", "waking_decay", 0.01)])
def test_a14_refuses_undeclared_or_wrong_sign(drive, term, d):
    acc = DriveAccount(dict(B0))
    with pytest.raises(InvariantError, match="A14"):
        acc.record(drive, term, d)


def test_a14_range_and_cache():
    b = dict(B0)
    acc = DriveAccount(b)
    with pytest.raises(InvariantError, match="cached"):
        acc.check(b, drives.drive(b) + 0.01)
    b["V"] = 1.2
    acc.record("V", "h_word_latch", 1.2)
    with pytest.raises(InvariantError, match="outside"):
        acc.check(b, drives.drive(b))


def test_a14_satiable_bound():
    acc = DriveAccount(dict(B0))
    acc.drops = acc.D_start + 1.0          # inject an accounting state that breaks the bound
    with pytest.raises(InvariantError, match="drops"):
        acc.check(dict(B0), drives.drive(B0))


def test_drive_forms():
    assert drives.drive({"E": 0.7, "A": 0.0, "V": 0.0, "K": 0.0, "P": 0.0, "I": 0.0}) == 0.0
    assert abs(drives.drive({"E": 0.7, "A": 0.0, "V": 0.15, "K": 0.0, "P": 0.0, "I": 0.0}) - 0.01) < 1e-12
    assert abs(drives.drive_partner(0.15, 0.0, 0.0) - 0.008) < 1e-12


# ---------------------------------------------------------------------------------------------- A17 stub
def test_a17_model_hash(tmp_path):
    f = tmp_path / "model.bin"
    f.write_bytes(b"weights")
    lock = tmp_path / "models.lock"
    lock.write_text(json.dumps({"files": {}}))
    with pytest.raises(InvariantError, match="not in models.lock"):
        check_a17_model(f, lock)
    import hashlib
    lock.write_text(json.dumps({"files": {"model.bin": hashlib.sha256(b"weights").hexdigest()}}))
    assert check_a17_model(f, lock)
    with pytest.raises(InvariantError, match="hub id"):
        check_a17_model("someorg/some-model", lock)


def test_models_lock_present_and_empty_until_m1():
    from engine.config import innate
    assert json.loads(innate.LOCK_PATH.with_name("models.lock").read_bytes())["files"] == {}
