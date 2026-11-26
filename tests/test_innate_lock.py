"""INNATE.lock: canonical, reproducible, checked at start (spec §3.3, A10)."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from engine.config import innate
from engine.config.channels import TABLE
from engine.invariants.asserts import InvariantError, check_a10, register_innate_array

ROOT = Path(__file__).resolve().parents[1]


def test_lock_reproducible_in_fresh_interpreters():
    digests = set()
    for seed in ("0", "1", "12345"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        out = subprocess.run([sys.executable, "-m", "engine.config.innate"], cwd=ROOT, env=env,
                             capture_output=True, check=True).stdout.rstrip(b"\n")
        digests.add(hashlib.sha256(out).hexdigest())
    assert len(digests) == 1
    assert digests == {hashlib.sha256(innate.LOCK_PATH.read_bytes()).hexdigest()}


def test_canonical_format():
    data = innate.LOCK_PATH.read_bytes()
    doc = json.loads(data)
    assert data == json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert not data.endswith(b"\n") and b'", "' not in data and b'": ' not in data
    assert doc["sha256"] == hashlib.sha256(innate.canonical(doc["entries"])).hexdigest()
    assert innate.canonical({"b": 0.1, "a": [1, 2.5]}) == b'{"a":[1,2.5],"b":0.1}'
    with pytest.raises(ValueError):
        innate.canonical({"x": float("nan")})


def test_lock_holds_every_constant_and_channel_table():
    e = json.loads(innate.LOCK_PATH.read_bytes())["entries"]
    assert set(e) == set(innate.ENTRIES)
    assert e["channel_c"]["value"] == list(TABLE.c)
    assert e["ledger_kappa"]["value"] == 0.7
    assert len(e["ledger_keys"]["value"]) == 97


def test_a10_passes():
    assert check_a10() == hashlib.sha256(innate.LOCK_PATH.read_bytes()).hexdigest()


def test_a10_refuses_tampered_lock(tmp_path):
    doc = json.loads(innate.LOCK_PATH.read_bytes())
    doc["entries"]["ledger_kappa"]["value"] = 0.8
    p = tmp_path / "INNATE.lock"
    p.write_bytes(innate.canonical(doc))
    with pytest.raises(InvariantError, match="A10"):
        check_a10(p)
    with pytest.raises(InvariantError, match="A10"):
        check_a10(tmp_path / "missing.lock")


def test_a10_aliasing():
    innate_arr = register_innate_array(np.array(TABLE.c))
    check_a10(learned={"w": np.zeros(33)})
    with pytest.raises(InvariantError, match="aliases"):
        check_a10(learned={"w": innate_arr[:10]})
