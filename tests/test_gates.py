"""The gates g and g_o (spec §1.5.4, A2): the monotone additive form against sims/design-g7's phi and fitted-gate
formula, the untrained context-free state, the input lists (rules 11', 13'). Synthetic arrays only."""
import numpy as np
import pytest

import refsims
from engine.config.innate import ENTRIES
from engine.invariants.asserts import check_a2
from engine.routes import gates as GT


def test_basis_and_formula_match_reference_gate():
    ref = refsims.g7_gate()
    r = np.random.default_rng(0)
    n_in = 7
    m = GT.MonotoneAdditive([f"x{i}" for i in range(n_in)], "exp")
    m.knots = np.tile(np.array(ref["KN"]), (n_in, 1))
    b = 0.3 * r.normal(size=1 + n_in * (len(ref["KN"]) + 1))
    m.b0, m.beta, m.m_ref = b[0], b[1:].reshape(n_in, -1), 0.8
    gate = eval(ref["gate_expr"], {"np": np, "phi": ref["phi"], "b": b, "m_ref": 0.8, "drop": ()})
    for _ in range(200):
        x = r.uniform(0, 1, n_in)
        assert np.array_equal(GT.basis(x, m.knots).reshape(-1), ref["phi"](x)[0])
        assert m(x) == pytest.approx(gate(x), rel=1e-12, abs=1e-15)


def test_form_constants():
    assert GT.N_BASIS == ENTRIES["gate_basis"].value["count"] == 7
    assert GT.DEFAULT_KNOTS[0] == 0.05 and GT.DEFAULT_KNOTS[-1] == 0.80 and GT.DEFAULT_KNOTS.size == 6
    assert len(GT.G_INPUTS) == 18 and len(GT.GO_INPUTS) == 5


def test_untrained_gates_are_their_context_free_constant_and_in_range():
    gs = GT.Gates()
    r = np.random.default_rng(1)
    for _ in range(50):
        g, go = gs.g(r.uniform(0, 1, 18)), gs.g_o(r.uniform(0, 1, 5))
        assert g == 1.0 and go == 1.0 and check_a2(g, go) == []
    gs.g.disabled = True
    assert gs.g(np.full(18, np.nan)) == gs.g.context_free           # disabled: reads nothing


def test_clip_and_a2():
    m = GT.MonotoneAdditive(["a"], "exp")
    m.beta[0, 0] = 50.0
    assert m(np.array([1.0])) == 1.0                                  # exp link clipped to [0, 1]
    assert check_a2(1.5, 0.5) == ["g"] and check_a2(0.5, -0.1) == ["g_o"] and check_a2(np.nan, 0.2) == ["g"]


def test_directions():
    m = GT.MonotoneAdditive(["a", "b"], "exp")
    m.directions[:] = [-1, 1]
    m.beta[0] = -0.1
    m.beta[1] = 0.2
    assert m.directions_hold()
    m.beta[1, 3] = -0.01
    assert not m.directions_hold()


def test_inputs_never_name_his_unread_channels():
    unread = set(ENTRIES["echo_gate_unread"].value)
    for name in GT.G_INPUTS + GT.GO_INPUTS:
        assert not any(c in name.split("_") for c in unread)
    assert not any(n.startswith(("V_his", "D_tau")) for n in GT.GO_INPUTS)    # g_o: no channel of his (rule 13')
