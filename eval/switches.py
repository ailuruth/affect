"""The documented lesion switches (spec §5.2, E1; design §7). Each switch names the part it disables, how, the spec
row it serves, its sham, and its size (for the sham of equal size). A switch is applied by the harness to one
engine pair (eval/drive.run) before frame 0, on that run's own copy of the learned parts; the engine code itself is
never edited and has no lesion flag of its own beyond each part's `disabled` state (its fail-safe / disabled-part
state, spec §1.10, §4.3).

Built (the part exists in the engine at this build):
  gate_g_const        g <- 1             the echo gate's `disabled` state: its context-free constant 1.0, reads nothing
  gate_go_const       g_o <- 1           likewise for the own-display gate
  listener_zero       L_d <- 0           the listener display's `disabled` state (A8's fail-safe)
  qhat_zero           qhat <- 0          q-hat's `disabled` state: its context-free constant 0
  dtau_removed        D_tau removed      the gate's D_tau traces held at 0 in both runs (the held-copy path)
  ledger_lags_0_3     lag scan -> 0-3 s  the ledger rebuilt with only the keys of lag <= 3 s (7 of 97)
  ledger_kappa_1      kappa 0.70 -> 1    the ledger rebuilt with kappa 1
  p_name_removed      P_name removed     the P_name map's weights set to 0 (P4 output 0)
  echo_gain_zero_SL   G_k <- 0 on the smile_laugh group (E3 "present" claim, spec §5.4)
Not built here (refuse to run, with the reason): turns_fixed_6s, sign_prior_removed, calibration_removed,
partner_anchor_restored.

Shams. `sham_unread` changes, by the lesion's size, a part no route reads at this build (the turn model's weights:
the turn model is not wired into the state at M4), so the derivation predicts exactly zero effect on every readout;
a nonzero sham effect is an isolation bug. For the echo gain the sham is the same operation on the zero-ceiling
channels (G_k is already 0 there by A0).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from engine.config.channels import SMILE_LAUGH, TABLE, ZERO_CEILING
from engine.shadow.ledger import KEYS, Ledger


class NotBuilt(Exception):
    pass


@dataclass(frozen=True)
class Lesion:
    name: str
    part: str
    how: str
    spec_row: str
    sham: str
    kind: str = "engine"                  # engine | ledger
    built: bool = True
    reason: str = ""

    def apply(self, pair) -> None:
        if not self.built:
            raise NotBuilt(f"{self.name}: {self.reason}")
        _APPLY[self.name](pair)

    def size(self, learned) -> float:
        return float(_SIZE.get(self.name, lambda L: 1.0)(learned))


def _gate(name):
    def f(pair):
        getattr(pair.L.gates, name).disabled = True
    return f


def _listener(pair):
    pair.L.ld.disabled = True


def _qhat(pair):
    pair.L.qhat.disabled = True


def _dtau(pair):
    pair.factual.held_D_tau = np.zeros((3, 4))
    pair.shadow.held_D_tau = np.zeros((3, 4))
    for run in (pair.factual, pair.shadow):
        run.gi.D_tau = np.zeros((3, 4))


def ledger_for(name, fs: float, ceilings=None) -> Ledger:
    """The ledger of a ledger lesion (or the intact one for name None), over `ceilings` (default: the 33 channels)."""
    c = TABLE.c if ceilings is None else ceilings
    if name is None:
        return Ledger(c, fs)
    if name == "ledger_lags_0_3":
        return Ledger(c, fs, keys=tuple(k for k in KEYS if k[1] <= 3.0))
    if name == "ledger_kappa_1":
        return Ledger(c, fs, kappa=1.0)
    raise KeyError(name)


def _ledger(name):
    def f(pair):
        pair.ledger = ledger_for(name, pair.fs)
    return f


def _pname(pair):
    pair.L.pname.W = np.zeros_like(pair.L.pname.W)
    pair.L.pname.b = np.zeros_like(pair.L.pname.b)


def _gain_zero(idx):
    def f(pair):
        for run in (pair.factual, pair.shadow):
            run.fast.G = run.fast.G.copy()
            run.fast.G[list(idx)] = 0.0
    return f


def _sham_unread(pair, size: float = 1.0, seed: int = 0):
    r = np.random.default_rng(seed)
    tm = pair.L.turns
    v = r.standard_normal(tm.w_haz.shape[0] + tm.w_end.shape[0])
    v *= size / max(np.linalg.norm(v), 1e-300)
    tm.w_haz = tm.w_haz + v[:tm.w_haz.shape[0]]
    tm.w_end = tm.w_end + v[tm.w_haz.shape[0]:]


def _gate_size(name):
    return lambda L: np.linalg.norm(getattr(L.gates, name).beta) + abs(getattr(L.gates, name).b0)


_APPLY = {
    "gate_g_const": _gate("g"), "gate_go_const": _gate("g_o"), "listener_zero": _listener, "qhat_zero": _qhat,
    "dtau_removed": _dtau, "ledger_lags_0_3": _ledger("ledger_lags_0_3"), "ledger_kappa_1": _ledger("ledger_kappa_1"),
    "p_name_removed": _pname, "echo_gain_zero_SL": _gain_zero(SMILE_LAUGH),
    "echo_gain_zero_zero_ceiling": _gain_zero(ZERO_CEILING),
}
_SIZE = {
    "gate_g_const": _gate_size("g"), "gate_go_const": _gate_size("g_o"),
    "listener_zero": lambda L: np.linalg.norm(L.ld.W),
    "qhat_zero": lambda L: np.linalg.norm(L.qhat.beta) + abs(L.qhat.b0),
    "p_name_removed": lambda L: np.linalg.norm(L.pname.W) + np.linalg.norm(L.pname.b),
    "ledger_lags_0_3": lambda L: float(len(KEYS) - sum(1 for k in KEYS if k[1] <= 3.0)),
    "ledger_kappa_1": lambda L: 0.30,
    "echo_gain_zero_SL": lambda L: float(np.linalg.norm(TABLE.G[list(SMILE_LAUGH)])),
}

LESIONS = {x.name: x for x in (
    Lesion("gate_g_const", "echo gate g", "g.disabled: context-free constant 1.0", "§5.2 g <- 1", "sham_unread"),
    Lesion("gate_go_const", "own-display gate g_o", "g_o.disabled: constant 1.0", "§5.2 g_o <- 1", "sham_unread"),
    Lesion("listener_zero", "listener display L_d", "ld.disabled: L_d = 0", "§5.2 L_d <- 0", "sham_unread"),
    Lesion("qhat_zero", "q-hat", "qhat.disabled: constant 0", "§5.2 q-hat <- 0", "sham_unread"),
    Lesion("dtau_removed", "D_tau traces of g", "held at 0 in both runs", "§5.2 D_tau removed", "sham_unread"),
    Lesion("ledger_lags_0_3", "ledger lag scan", "keys with lag <= 3 s only", "§5.2 lag scan -> 0-3 s",
           "sham_unread", kind="ledger"),
    Lesion("ledger_kappa_1", "ledger margin", "kappa 1.0", "§5.2 kappa 0.70 -> 1", "sham_unread", kind="ledger"),
    Lesion("p_name_removed", "P_name map", "weights 0 (port P4 output 0)", "§5.2 P_name removed (F7)", "sham_unread"),
    Lesion("echo_gain_zero_SL", "fast gear G_k, smile_laugh", "G_k = 0 on LP, CR, BU_L, RHY, BRE",
           "§5.4 present: G_k <- 0", "echo_gain_zero_zero_ceiling"),
    Lesion("echo_gain_zero_zero_ceiling", "fast gear G_k, zero-ceiling channels", "G_k = 0 (already 0)",
           "§5.4 sham", "sham_unread"),
    Lesion("turns_fixed_6s", "learned turn-taking", "fixed 6-s rule (lesion control only)", "§5.2", "sham_unread",
           built=False, reason="the turn model is not wired into the state at this build (M6/M7)"),
    Lesion("sign_prior_removed", "cross-entry sign prior", "prior removed", "§5.2", "sham_unread", built=False,
           reason="learned appraisal cross bases are untrained stubs (0) until the M3 fit"),
    Lesion("calibration_removed", "calibration / H_id", "readers without b_read, sigma_id, H_id", "§5.2",
           "sham_unread", built=False, reason="the body does not yet read the calibration or H_id (M8 offline part)"),
    Lesion("partner_anchor_restored", "Pi-tilde partner anchor (negative control)", "anchor restored", "§5.2",
           "sham_unread", built=False, reason="needs the fitted Pi-tilde (M3/M8)"),
)}


class Sham:
    """The sham of a lesion: `sham_unread` of equal size, or the named sham switch."""

    def __init__(self, lesion: Lesion, learned, seed: int = 0):
        self.lesion, self.seed = lesion, seed
        self.size = lesion.size(learned)
        self.name = lesion.sham

    def apply(self, pair) -> None:
        if self.name == "sham_unread":
            _sham_unread(pair, self.size, self.seed)
        else:
            LESIONS[self.name].apply(pair)
