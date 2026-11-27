"""Projections after every replay step, and the budget check of every learned part (spec §1.9 step 4, §4.3 A2, A6,
A7, A8; design Claim L). Every learned coupling stays inside its per-expression set whatever its weights:

  appraisal Gamma(3,4)   `appraisal.project_basis` under the smallest |omega_g| of every known person and the prior
                         of a new one, so the set holds for whoever the next session is with (A7)
  Delta                  zero synergy columns on the own-display mask rows (BL, LT, LPR, NW, DIM) (A7)
  cone learned entries   no replay step of spec §1.9 writes them; they are re-projected at every latch, and A6 is
                         checked here for every person's omega anyway
  readers, H_id, adapter knowing only (no path to the face); outputs clipped to their ranges; adapter |.| <= 0.15
  omega                  in [-1, 1]
  L_d, gates             frozen dyad parts (M3), never written by replay; A8 and A2 checked here all the same
"""
from __future__ import annotations

import numpy as np

from engine.invariants import asserts as A
from engine.routes import appraisal as AP
from engine.routes import cone as C
from engine.routes.free_display import MASK_ZERO
from engine.routes.learned_t import OMEGA_PRIOR


def omega_floor(omegas) -> np.ndarray:
    """Elementwise smallest |omega_g| over the known persons and the new-person prior."""
    om = [np.abs(OMEGA_PRIOR)] + [np.abs(np.asarray(o, dtype=np.float64)) for o in omegas]
    return np.min(np.stack(om), axis=0)


def project_appraisal(net, omegas, S) -> None:
    lo = omega_floor(omegas)
    net.learned_bases = np.stack([AP.project_basis(net.learned_bases[i], lo, S) for i in range(2)])


def project_delta(delta) -> None:
    delta.syn[:, list(MASK_ZERO)] = 0.0


def check_all(L, omegas, dyad_prior=None) -> list:
    """Every learned part against its set, for every person's omega (and the new-person prior). [] when green."""
    out = []
    S = C.pair_sign(np.zeros((C.N, C.N)) if dyad_prior is None else dyad_prior)
    for om in [OMEGA_PRIOR] + [np.asarray(o, dtype=np.float64) for o in omegas]:
        if np.any(np.abs(om) > 1.0) or not np.all(np.isfinite(om)):
            out.append(("A6", "omega outside [-1, 1]"))
            continue
        bases = np.concatenate([AP.innate_bases(om), L.appraisal.learned_bases])
        out += [("A7",) + tuple(v) for v in A.check_a7(bases, om, S, L.delta)]
        cone = C.Cone(30.0, dyad_prior)
        G = cone.latch(om, np.zeros(C.N_IN))
        out += [("A6",) + tuple(v) for v in A.check_a6(G, om, cone.S, cone.G0)]
    out += [("A8",) + tuple(v) for v in A.check_a8(np.zeros(C.N), L.ld.W)]
    for name, part in (("reader_own", L.reader_own), ("reader_his", L.reader_his), ("word_v", L.word_v),
                       ("delta.W1", L.delta), ("appraisal", L.appraisal)):
        arrays = [getattr(part, a) for a in ("W", "b", "W1", "W2", "syn", "Wsel", "learned_bases") if hasattr(part, a)]
        if not all(np.all(np.isfinite(x)) for x in arrays):
            out.append(("finite", name))
    for ident, ad in L.adapter.items():
        if not (np.all(np.isfinite(ad.W)) and np.all(np.isfinite(ad.b))):
            out.append(("finite", "adapter." + ident))
    return out
