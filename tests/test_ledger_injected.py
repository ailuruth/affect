"""Mechanism unit test (spec §5.1 F22 row: "synthetic injected copies on all 33 channels are a mechanism unit test in
CI, not F22"). A gain-1 copy of his channel, delayed 10-300 s, is injected after assembly on every channel at once;
the safety net of D104 must hold it: the scaled governor (engine/shadow/governor.py, design-scaled-safety-net.md §7.2)
in front of the 97-key ledger at kappa 0.70 with its one-minute evidence floor (§7.5). Synthetic signals: not
evidence about behaviour.

One batched run carries, side by side as columns (every channel of the governor and the ledger is independent):
  the copies as this test has always built them (padded, minus the session mean; neutral input = session mean),
  the same copies built causally with an engine-like neutral input b_id (rev2_lib.engine_baseline), and
  the mechanism shapes of §7.7 (rev2_check.py R2's partners and routes, the columns of the cells named).
"""
from __future__ import annotations

import numpy as np
import pytest

import refsims
from engine.config.channels import TABLE, ZERO_CEILING
from engine.invariants.asserts import check_a3_frame, check_a4_frame, check_a4g_frame
from engine.shadow.governor import Governor, evidence_floor
from engine.shadow.ledger import Ledger
from synth import delay, lp, partner, worst_block_slope

FS = 10.0
T = int(3600 * FS)
DELAYS = (10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300)
CAPPED = [k for k in range(33) if TABLE.c[k] > 0]
R = refsims.rev2_lib()
TT = np.arange(T) / FS


def _hp(v, tau):
    return v - R.lp(v[:, None], tau)[:, 0]


def _lobe(u, u0, D):
    v = u - u0
    e = v - R.lp(v[:, None], 4.0)[:, 0]
    return R.causal_copy(np.maximum(e, 0) + R.lp(v[:, None], 60.0)[:, 0] + u0, D, u0)


# (name, rev2_check SCEN index (partner seed 300 + index), route(u, u0) with gain 1, cells (c, g/c), expected to pass)
SHAPES = (
    ("onset lobe + 60-s lp, 120 s", 4, lambda u, u0: _lobe(u, u0, 120.0), ((0.05, 3.0), (0.05, 33.0)), True),
    ("low-passed 120 s, delay 90 s", 5, lambda u, u0: R.lp(R.causal_copy(u, 90.0, u0)[:, None], 120.0)[:, 0],
     ((0.05, 3.0), (0.05, 33.0)), True),
    ("fast echo (2-s high-pass), 30 s", 7, lambda u, u0: R.causal_copy(_hp(u - u0, 2.0) + u0, 30.0, u0),
     ((0.05, 3.0), (0.05, 33.0)), True),
    ("on 10 s / off 50 s", 8, lambda u, u0: R.causal_copy(u, 90.0, u0) * ((TT % 60.0) < 10.0),
     ((0.05, 3.0), (0.05, 33.0)), True),
    ("on 6 min / off 24 min", 9, lambda u, u0: R.causal_copy(u, 90.0, u0) * (((TT + 600.0) % 1800.0) < 360.0),
     ((0.35, 10.0),), False),
)
CS = (0.03, 0.05, 0.10, 0.35)
GR = (1.5, 3.0, 10.0, 33.0)


def _shape_columns():
    """rev2_check.py job_R2's partners (16 columns over CS x GR per scenario, seed 300 + index, u0 = b_id); only the
    columns of the named cells are kept (each column is independent, so the subset gives the same numbers)."""
    cols = []
    for name, si, f, cells, ok in SHAPES:
        U = R.partners_fast(16, 300 + si, T=T)
        u0 = R.engine_baseline(16, 300 + si)
        for cc, gg in cells:
            j = CS.index(cc) * 4 + GR.index(gg)
            cols.append((name, cc, gg, ok, U[:, j], u0[j], gg * cc * f(U[:, j], u0[j])))
    return cols


@pytest.fixture(scope="module")
def batched():
    r = np.random.default_rng(33)
    U = np.zeros((T, 33))
    X = np.zeros((T, 33))
    for k in range(33):
        u = partner(T, FS, r, 300.0 if k % 2 == 0 else 30.0)
        if TABLE.signs[k] == "signed":
            u = u - 0.4
        U[:, k] = u
        X[:, k] = delay(u, DELAYS[k % 12] * FS) - u.mean()
    b_id = R.engine_baseline(33, 33, signed=R.SIGNED)
    Xc = np.stack([R.causal_copy(U[:, k], DELAYS[k % 12], b_id[k]) for k in range(33)], 1)
    sh = _shape_columns()
    UA = np.concatenate([U, U, np.stack([s[4] for s in sh], 1)], 1)
    XA = np.concatenate([X, Xc, np.stack([s[6] for s in sh], 1)], 1)
    cA = np.concatenate([TABLE.c, TABLE.c, [s[1] for s in sh]])
    u0A = np.concatenate([U.mean(0), b_id, [s[5] for s in sh]])
    zero = list(ZERO_CEILING) + [33 + k for k in ZERO_CEILING]
    n = UA.shape[1]
    gov = Governor(cA, FS, u0A)
    led = Ledger(cA, FS, evidence_floor=evidence_floor(FS))
    O = np.zeros_like(XA)
    G = np.zeros_like(XA)
    a3 = np.zeros(n, dtype=np.int64)
    a4 = np.zeros(n, dtype=np.int64)
    a4g = np.zeros(n, dtype=np.int64)
    for t in range(T):
        G[t] = gov.step(UA[t], XA[t])
        O[t] = led.step(UA[t], G[t])
        a4g += check_a4g_frame(XA[t], G[t], gov.a, gov.prev_a, gov.ever_latched, zero)
        a3 += check_a3_frame(zero, O[t], led.S, led.last_active)
        a4 += check_a4_frame(G[t], O[t], led.S, led.E, led.bound, led.last_active, led.last_hold)
    return dict(U=UA, X=XA, O=O, G=G, led=led, gov=gov, a3=a3, a4=a4, a4g=a4g, shapes=sh)


def _part(b, i):
    s = slice(33 * i, 33 * i + 33)
    return b["U"][:, s], b["X"][:, s], b["O"][:, s]


@pytest.fixture(scope="module")
def slopes(batched):
    U, X, O = _part(batched, 0)
    return worst_block_slope(U, X, FS).max(0), worst_block_slope(U, O, FS).max(0)


def test_attenuate_only_every_frame(batched):
    X, O, G, led = batched["X"], batched["O"], batched["G"], batched["led"]
    assert np.all(np.abs(O) <= np.abs(X)) and np.all(O * X >= 0)
    assert np.all(np.abs(G) <= np.abs(X)) and np.all(G * X >= 0)
    assert led.grow.sum() == 0 and led.flip.sum() == 0


def test_a3_a4_and_a4g_hold_every_frame(batched):
    assert batched["a3"].sum() == 0
    assert batched["a4"].sum() == 0
    assert batched["a4g"].sum() == 0


def test_copy_strongly_attenuated_on_capped_channels(slopes):
    """The gain-1 copy, far above every ceiling, is cut to at most half its slope on every capped channel, and to
    <= 2.5 c_k (what the ledger alone already guaranteed; kept as a floor under the governor)."""
    before, after = slopes
    c = TABLE.array("c")
    for k in CAPPED:
        assert before[k] > 2 * c[k], TABLE.codes[k]
        assert after[k] <= 0.5 * before[k], (TABLE.codes[k], after[k], before[k])
        assert after[k] <= 2.5 * c[k], (TABLE.codes[k], after[k] / c[k])


def test_copy_held_below_ceiling_on_capped_channels(slopes):
    """F22's 1.0 c_k criterion on this test's own seed and construction (design §7.4: 0.72 c with the governor,
    2.01 c with the ledger alone)."""
    before, after = slopes
    c = TABLE.array("c")
    worst = max(after[k] / c[k] for k in CAPPED)
    assert worst <= 1.0, worst


def _causal_worst(batched, start_s):
    U, X, O = _part(batched, 1)
    a = int(start_s * FS)
    w = worst_block_slope(U[a:], O[a:], FS).max(0)
    return {TABLE.codes[k]: w[k] / TABLE.c[k] for k in CAPPED}


def test_copy_causal_engine_baseline(batched):
    """The same copies built causally (0 until the route acts) with the engine's neutral input b_id, read from 10 min
    on (design §7.4: 0.67 c): after the detection span the net holds every capped channel below 1.0 c_k."""
    w = _causal_worst(batched, 600.0)
    assert max(w.values()) <= 1.0, w


@pytest.mark.xfail(strict=True, reason=(
    "the detection span (design-scaled-safety-net.md §7.6): built causally with b_id, the whole 1-h session reads "
    "1.26 c on BO (c 0.10, g/c 10; route on at 150 s, detected about 89 s later) and <= 0.91 c elsewhere; no causal "
    "net that keeps the false-engagement margin removes it (Q35/D99 stays open on this point)"))
def test_copy_causal_engine_baseline_whole_session(batched):
    w = _causal_worst(batched, 0.0)
    assert max(w.values()) <= 1.0, w


def test_zero_ceiling_channels_carry_no_toward_copy(batched, slopes):
    """A3 holds exactly (test above); the governor sets a = 0 once a toward key latches, and the block-mean metric
    reads at most a few hundredths of the copy's gain-1 slope."""
    U, X, O = _part(batched, 0)
    after = slopes[1][list(ZERO_CEILING)]
    assert len(ZERO_CEILING) == 13
    assert np.all(after <= 0.03), after
    assert np.mean(np.abs(O[:, ZERO_CEILING])) < 0.01 * np.mean(np.abs(X[:, ZERO_CEILING]))
    a = batched["gov"].a
    assert set(np.unique(a[list(ZERO_CEILING) + [33 + k for k in ZERO_CEILING]])) <= {0.0, 1.0}


def _shape_results(batched):
    out = []
    for i, (name, cc, gg, ok, *_ ) in enumerate(batched["shapes"]):
        j = 66 + i
        w = worst_block_slope(batched["U"][:, j], batched["O"][:, j], FS).max() / cc
        out.append((name, cc, gg, ok, float(w)))
    return out


@pytest.fixture(scope="module")
def shapes(batched):
    return _shape_results(batched)


def test_mechanism_shapes(shapes):
    """§7.7: at c = 0.05 and g/c 3 and 33, the spec's onset-lobe shape, a 120-s low-passed copy, the fast echo and a
    10-s on / 50-s off copy, each <= 1.0 c (design §7.4: <= 0.95 c), causal with b_id."""
    res = [(n, cc, gg, w) for n, cc, gg, ok, w in shapes if ok]
    assert len(res) == 8
    assert all(w <= 1.0 for *_, w in res), res


@pytest.mark.xfail(strict=True, reason=(
    "the detection span (design §7.4, §7.6): a copy on 6 min / off 24 min at c 0.35, g/c 10 reads 1.26 c over the "
    "session; its first on-period runs at the ledger's level until the governor has two batches of evidence"))
def test_mechanism_switched_6_24(shapes):
    res = [(n, cc, gg, w) for n, cc, gg, ok, w in shapes if not ok]
    assert len(res) == 1
    assert res[0][3] <= 1.0, res


def _counted_partners(seeds, n, u_mean: bool):
    """The counted routes alone on test_counted_routes_untouched's partners (seeds side by side, capped channels
    only). u_mean: this test's original recipe (onset filter from 0, the held route about his session mean, neutral
    input = session mean); else the engine-like recipe of rev2_check.py R5 (relative to b_id)."""
    Us, Ys, u0s, cs = [], [], [], []
    for seed in seeds:
        if u_mean:
            r = np.random.default_rng(seed)
            U = np.zeros((n, 33))
            Y = np.zeros((n, 33))
            for k in range(33):
                u = partner(n, FS, r, 300.0 if k % 2 == 0 else 30.0)
                if TABLE.signs[k] == "signed":
                    u = u - 0.4
                U[:, k] = u
                xd = delay(u, 0.45 * FS)
                e = xd - lp(xd, 4.0, FS)
                fast = TABLE.G[k] * (np.maximum(e, 0.0) if TABLE.signs[k] == "one_sided" else e)
                Y[:, k] = fast + 0.22 * TABLE.c[k] * lp(u - u.mean(), 120.0, FS)
            u0 = U.mean(0)
        else:
            U = R.partners_fast(33, seed, T=n, signed=R.SIGNED)
            u0 = R.engine_baseline(33, seed, signed=R.SIGNED)
            Y = R.counted_routes(U, u0, np.asarray(TABLE.c), np.asarray(TABLE.G), R.SIGNED)
        Us.append(U[:, CAPPED])
        Ys.append(Y[:, CAPPED])
        u0s.append(u0[CAPPED])
        cs.append(np.asarray(TABLE.c)[CAPPED])
    return np.concatenate(Us, 1), np.concatenate(Ys, 1), np.concatenate(u0s), np.concatenate(cs)


SEEDS = tuple(range(7, 15))


def test_counted_routes_untouched():
    """F22's second clause, as a mechanism test, on the 8 synthetic partners of seeds 7-14 (30 min): the fast gear
    (0.45 s) plus a held 2-min route at 0.22 c_k on every capped channel.
    - The governor never engages (a = 1 on every frame), with the engine's neutral input b_id (design §7.4 R5) and with
      this test's original recipe (session mean).
    - Governor -> ledger with the evidence floor changes <= 1 % of frames on the original recipe (§7.5: 0/8 partners
      above 1 %; the ledger alone: 5/8). With b_id the ledger stage reaches 0.97 % (seed 10) and 4.61 % (seed 13) in
      30-min sessions (§7.5); that case is not asserted here."""
    n = int(1800 * FS)
    nc = len(CAPPED)
    for u_mean in (False, True):
        U, Y, u0, c = _counted_partners(SEEDS, n, u_mean)
        gov = Governor(c, FS, u0)
        led = Ledger(c, FS, evidence_floor=evidence_floor(FS)) if u_mean else None
        for t in range(n):
            x = gov.step(U[t], Y[t])
            if led is not None:
                led.step(U[t], x)
        assert gov.engaged.sum() == 0 and np.all(gov.a == 1.0), (u_mean, gov.engaged.reshape(-1, nc).max(1))
        if led is not None:
            changed = (led.hits / n).reshape(len(SEEDS), nc).max(1)
            assert np.all(changed <= 0.01), dict(zip(SEEDS, changed))
