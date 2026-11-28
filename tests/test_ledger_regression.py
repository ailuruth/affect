"""Ledger regression at 10 Hz against the reference, bit for bit (spec §5.1 note, §6 M0).

Reference: `ledger7` (research/foundations/sims/design-g7/checks.py), `ledger9` (sims/design-g9/ledger_lag120.py,
loaded exactly as sims/check-cayley91/ledger_close.py loads it) with the 97 keys of `w10`; the same constructed
partners (seed 910, 10 Hz), float64. These are code regression tests: they catch implementation errors and say
nothing about behaviour.

Default runs use the first 30 min of each 2-h partner; `pytest -m slow` runs the full 2 h at the delays of the
check of revision 9.1 and compares the printed figures of sims/check-cayley91/k070_w10_*.out.txt as well.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import pytest

from engine.config.innate import ENTRIES
from engine.shadow import ledger as L

ROOT = Path(__file__).resolve().parents[1]
SIMS = ROOT / "research" / "foundations" / "sims"
G9 = SIMS / "design-g9"
FS = 10.0
C_LP = 0.35
KAPPA = ENTRIES["ledger_kappa"].value


@pytest.fixture(scope="module")
def ref():
    src = (G9 / "ledger_lag120.py").read_text()
    src = src[: src.index('print(f"partners')].replace("HERE = os.path.dirname(os.path.abspath(__file__))",
                                                       f"HERE = {str(G9)!r}")
    g = {"__name__": "defs"}
    exec(src, g)
    keys_w10 = ([(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, float(l)) for l in range(0, 121, 5)]
                + [(60.0, float(l)) for l in range(0, 301, 10)]) + [(10.0, float(l)) for l in range(125, 301, 5)]
    g["KEYS_W10"] = keys_w10
    return g


def test_reference_key_set_equals_engine(ref):
    assert ref["fs"] == FS
    assert len(ref["KEYS_W10"]) == 97 == len(L.KEYS)
    assert sorted(ref["KEYS_W10"]) == sorted(L.KEYS)
    assert len(set(L.KEYS)) == 97
    assert sum(1 for w, _ in L.KEYS if w == 2.0) == 5
    assert sum(1 for w, _ in L.KEYS if w == 10.0) == 61
    assert sum(1 for w, _ in L.KEYS if w == 60.0) == 31


def _same(ref_res, eng_res):
    o, h, gr, fl = ref_res
    o2, h2, gr2, fl2 = eng_res
    assert o.dtype == o2.dtype == np.float64
    assert np.array_equal(o, o2), f"max |diff| {np.max(np.abs(o - o2))!r}"
    assert (h, gr, fl) == (h2, gr2, fl2)


N30 = int(30 * 60 * FS)


@pytest.mark.parametrize("partner,lag_s", [("u", 240), ("u2", 150), ("u", 10)])
def test_bit_identical_delayed_copy_30min(ref, partner, lag_s):
    uu = ref[partner][:N30]
    x = ref["delay"](uu, lag_s * FS) - uu.mean()
    r_ref = ref["ledger9"](ref["KEYS_W10"], uu, x, KAPPA * C_LP)
    r_eng = L.run(uu, x, [C_LP], FS)
    _same(r_ref, r_eng)
    assert r_eng[2] == 0.0 and r_eng[3] == 0.0       # never larger, never the other sign
    assert r_eng[1] > 0.3                             # the copy is trimmed on a large share of frames


def test_bit_identical_counted_routes_30min(ref):
    uu = ref["u2"][:N30]
    y = ref["fast"](uu, 0.224, 0.45) + 0.22 * C_LP * ref["lp"](uu - uu.mean(), 120.0)
    r_ref = ref["ledger9"](ref["KEYS_W10"], uu, y, KAPPA * C_LP)
    r_eng = L.run(uu, y, [C_LP], FS)
    _same(r_ref, r_eng)
    assert r_eng[1] == 0.0                            # counted routes: 0 frames changed (as the reference)


def test_bit_identical_ledger7_keys(ref):
    """ledger7 itself (revision 7 keys: 2-s lags 0-3 s, 10-s and 60-s at lag 0), at kappa 1 on c."""
    uu = ref["u"][: int(20 * 60 * FS)]
    x = ref["delay"](uu, 20 * FS) - uu.mean()
    keys7 = [(2.0, l) for l in (0.0, 0.5, 1.0, 2.0, 3.0)] + [(10.0, 0.0), (60.0, 0.0)]
    r_ref = ref["ledger7"](uu, x, C_LP)
    r_eng = L.run(uu, x, [C_LP], FS, kappa=1.0, keys=keys7)
    _same(r_ref, r_eng)


def test_bit_identical_inside_33_channels(ref):
    """The vectorised 33-channel ledger gives each channel exactly the single-channel reference result."""
    from engine.config.channels import TABLE
    n = int(10 * 60 * FS)
    rng = np.random.default_rng(5)
    U = rng.uniform(0, 1, (n, 33))
    X = rng.normal(0, 0.05, (n, 33))
    ks = (0, 5, 9, 20)                                  # LP, BI, HP (signed), BL (zero ceiling)
    for k, (part, lag) in zip(ks, (("u", 240), ("u2", 60), ("u", 90), ("u2", 30))):
        uu = ref[part][:n].copy()
        U[:, k] = uu
        X[:, k] = ref["delay"](uu, lag * FS) - uu.mean()
    out, h, gr, fl = L.run(U, X, TABLE.c, FS)
    for k in ks:
        o, hk, grk, flk = ref["ledger9"](ref["KEYS_W10"], U[:, k], X[:, k], KAPPA * TABLE.c[k])
        assert np.array_equal(o, out[:, k]), TABLE.codes[k]
        assert (hk, grk, flk) == (h[k], gr[k], fl[k])


def test_evidence_floor_matches_rev2_lib_and_zero_floor_is_today(ref):
    """The ledger's evidence floor (design-scaled-safety-net.md §7.5; D104): with E0 = 0.54 the engine's ledger equals
    rev2_lib.LedgerE0 (E starts at 1e-9 + E0) bit for bit; E0 = 0 is the ledger of revision 9.2 (the tests above),
    and the floor changes the output (it admits more early in the session, never more than its input)."""
    import refsims
    from engine.shadow.governor import evidence_floor
    R = refsims.rev2_lib()
    assert evidence_floor(FS) == ENTRIES["ledger_evidence_floor"].value == 0.54
    uu = ref["u"][:N30]
    x = ref["delay"](uu, 240 * FS) - uu.mean()
    led_ref = R.LedgerE0([C_LP], 0.54)
    o_ref = np.array([led_ref.step(uu[t:t + 1], x[t:t + 1])[0] for t in range(N30)])
    o, h, gr, fl = L.run(uu, x, [C_LP], FS, evidence_floor=0.54)
    assert np.array_equal(o, o_ref), np.max(np.abs(o - o_ref))
    assert float(led_ref.hits[0]) / N30 == h
    assert gr == 0.0 and fl == 0.0
    o0, h0, *_ = L.run(uu, x, [C_LP], FS)
    assert not np.array_equal(o, o0) and h < h0
    o00, *_ = L.run(uu, x, [C_LP], FS, evidence_floor=0.0)
    assert np.array_equal(o00, o0)


# ------------------------------------------------------------------------------------------- full 2 h (slow)
def _printed(name):
    rows = {}
    for line in (SIMS / "check-cayley91" / name).read_text().splitlines():
        m = re.search(r"K1 \S+ blocks (5 min|30 s)\s+L\s+(\d+) s .*max/c ([\d.]+) \| changed ([\d.]+) grow ([\d.]+) flip ([\d.]+)", line)
        if m:
            rows[(m.group(1).strip(), int(m.group(2)))] = tuple(float(v) for v in m.group(3, 4, 5, 6))
        m = re.search(r"K2 \S+ blocks (5 min|30 s)\s+counted routes frames changed ([\d.]+)", line)
        if m:
            rows[(m.group(1).strip(), "K2")] = float(m.group(2))
    return rows


FULL = [("5", 10), ("5", 90), ("5", 150), ("5", 180), ("5", 210), ("5", 240), ("5", 270), ("5", 300),
        ("30", 150), ("30", 180), ("30", 240), ("30", 300)]


@pytest.mark.slow
@pytest.mark.parametrize("part,lag_s", FULL)
def test_full_2h_delayed_copy_matches_reference_and_printed(ref, part, lag_s):
    printed = {}
    for f in ("k070_w10_240.out.txt", "k070_w10_a.out.txt", "k070_w10_b.out.txt", "k070_w10_c.out.txt"):
        printed.update(_printed(f))
    label = {"5": "5 min", "30": "30 s"}[part]       # block length of the reference's partner
    uu = ref["u"] if part == "5" else ref["u2"]
    x = ref["delay"](uu, lag_s * FS) - uu.mean()
    r_ref = ref["ledger9"](ref["KEYS_W10"], uu, x, KAPPA * C_LP)
    r_eng = L.run(uu, x, [C_LP], FS)
    _same(r_ref, r_eng)
    ws = ref["worst"](uu, r_eng[0], 300)
    mx = max(s for s, _ in ws) / C_LP
    exp = printed[(label, lag_s)]
    got = (float(f"{mx:.3f}"), float(f"{r_eng[1]:.2f}"), float(f"{r_eng[2]:.3f}"), float(f"{r_eng[3]:.3f}"))
    assert got == exp, (got, exp)
    assert 0.83 <= mx <= 0.885


@pytest.mark.slow
@pytest.mark.parametrize("part", ["5", "30"])
def test_full_2h_counted_routes(ref, part):
    printed = _printed("k070_w10_240.out.txt")
    label = {"5": "5 min", "30": "30 s"}[part]
    uu = ref["u"] if part == "5" else ref["u2"]
    y = ref["fast"](uu, 0.224, 0.45) + 0.22 * C_LP * ref["lp"](uu - uu.mean(), 120.0)
    r_ref = ref["ledger9"](ref["KEYS_W10"], uu, y, KAPPA * C_LP)
    r_eng = L.run(uu, y, [C_LP], FS)
    _same(r_ref, r_eng)
    assert float(f"{r_eng[1]:.3f}") == printed[(label, "K2")] == 0.0
