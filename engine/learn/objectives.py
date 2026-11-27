"""Replay objectives with their gradients (spec §1.9; r5 §2.6, §2.7; r6 §6.3). numpy only; every loss is a
weighted mean over replayed moments with the S48 sample weights (engine/learn/weights.py).

  weighted least squares   L = sum_n w_n |X_n W + b - Y_n|^2 / sum w            (Pi-tilde, word -> V, adapter)
  ridge (closed form)      W = argmin sum_n w_n |X_n W + b - Y_n|^2 + lambda |W|^2   (H_id, lambda 2)
  L_A                      E |y_A(t) - (Pi_0 d(t + 2 s) - Pi_0 d(t))|^2 + 0.001 |Gamma(3,4)|^2, with
                           y_A = sum_r s_r Gamma(r) xi_A (the lateral rows on the side opposite his 20-s lateral
                           trace, as `Appraisal.display`); gradients for Gamma(3,4) and the selection W
  L_display                E |Pi-tilde(face) - s|^2 + 0.1 |delta|^2, face = the agent's own observed face with Delta's
                           old contribution replaced by the new one, s the agent's own loads (V, A, T); no partner
                           term. The 0.3-weighted anticipation term needs the anticipation head P_ant, which is not
                           built (it reads the world model); it is 0 here
None of these has his face, his gaze or his presence as a target.
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES

L2_A = float(ENTRIES["appraisal_objective_l2"].value)
_LD = ENTRIES["display_objective"].value


def wls_grad(X, Y, w, W, b):
    """(loss, dW, db) of the weighted mean squared error."""
    w = np.asarray(w, dtype=np.float64)
    R = X @ W + b - Y
    sw = max(float(w.sum()), 1e-12)
    loss = float(np.sum(w[:, None] * R ** 2) / sw)
    G = 2.0 * w[:, None] * R / sw
    return loss, X.T @ G, G.sum(0)


def ridge(X, Y, w, lam):
    """Weighted ridge with an unpenalised intercept: (W, b)."""
    w = np.asarray(w, dtype=np.float64)
    sw = max(float(w.sum()), 1e-12)
    mx = (w @ X) / sw
    my = (w @ Y) / sw
    Xc, Yc = X - mx, Y - my
    A = Xc.T @ (w[:, None] * Xc) + lam * np.eye(X.shape[1])
    W = np.linalg.solve(A, Xc.T @ (w[:, None] * Yc))
    return W, my - mx @ W


def softmax(z):
    z = z - np.max(z, axis=-1, keepdims=True)
    e = np.exp(z)
    return e / np.sum(e, axis=-1, keepdims=True)


def appraisal_loss(bases, Wsel, alpha, xi, side, refl, target, w):
    """L_A and its gradients. bases (5, 33, 36) (0-2 innate, 3-4 learned); Wsel (5, 12); alpha (n, 12); xi (n, 36);
    side (n, 33) = -sign(his 20-s trace); refl (33, 36) the reflected mask; target (n, 33); w (n,).
    Returns (loss, dGamma (2, 33, 36), dWsel (5, 12))."""
    n = xi.shape[0]
    sw = max(float(np.sum(w)), 1e-12)
    s = softmax(alpha @ Wsel.T)                                         # (n, 5)
    direct = np.einsum("rkj,nj->nrk", bases * (1.0 - refl), xi)          # (n, 5, 33)
    lat = np.einsum("rkj,nj->nrk", bases * refl, xi) * side[:, None, :]
    per = direct + lat                                                   # each basis's display
    y = np.einsum("nr,nrk->nk", s, per)
    R = y - target
    loss = float(np.sum(w[:, None] * R ** 2) / sw) + L2_A * float(np.sum(bases[3:] ** 2))
    G = 2.0 * w[:, None] * R / sw                                        # dL/dy (n, 33)
    eff = (1.0 - refl)[None, :, :] + side[:, :, None] * refl[None, :, :]  # (n, 33, 36)
    dGam = np.empty((2,) + bases.shape[1:])
    for i, r in enumerate((3, 4)):
        dGam[i] = np.einsum("n,nk,nj,nkj->kj", s[:, r], G, xi, eff) + 2.0 * L2_A * bases[r]
    g_s = np.einsum("nk,nrk->nr", G, per)                                # dL/ds
    g_z = s * (g_s - np.sum(g_s * s, axis=1, keepdims=True))             # softmax backward
    return loss, dGam, g_z.T @ alpha


def display_loss(delta, z, env_rise, base, read_W, read_b, own_idx, target, w, mask_zero, rise_only):
    """L_display and its gradients for Delta (W1, W2, syn). z (n, 161); env_rise (n,); base (n, 33) the agent's own
    face without Delta; read_W, read_b the own-body reader on columns own_idx; target (n, 3) its own loads."""
    B = float(delta_bound(delta))
    h1 = np.tanh(z @ delta.W1)
    a = h1 @ delta.W2
    ta = np.tanh(a)
    dl = B * ta                                                          # (n, 18)
    m = np.ones((z.shape[0], delta.syn.shape[1]))
    m[:, list(mask_zero)] = 0.0
    m[:, list(rise_only)] *= env_rise[:, None]
    y = (dl @ delta.syn) * m
    face = base + y
    R = face[:, own_idx] @ read_W + read_b - target
    sw = max(float(np.sum(w)), 1e-12)
    loss = _LD["legibility"] * float(np.sum(w[:, None] * R ** 2) / sw) + _LD["l2"] * float(np.mean(np.sum(dl ** 2, 1)))
    gR = _LD["legibility"] * 2.0 * w[:, None] * R / sw
    gface = np.zeros_like(face)
    gface[:, own_idx] = gR @ read_W.T
    gpre = gface * m
    dsyn = dl.T @ gpre
    ddl = gpre @ delta.syn.T + _LD["l2"] * 2.0 * dl / z.shape[0]
    da = ddl * B * (1.0 - ta ** 2)
    dW2 = h1.T @ da
    dh1 = da @ delta.W2.T
    dW1 = z.T @ (dh1 * (1.0 - h1 ** 2))
    return loss, dW1, dW2, dsyn


def delta_bound(delta) -> float:
    return ENTRIES["display_delta_shape"].value["bound"]


def delta_output(delta, z, env_rise, mask_zero, rise_only):
    """Delta's contribution for a batch (the same formula as DisplayDelta.__call__)."""
    dl = delta_bound(delta) * np.tanh(np.tanh(z @ delta.W1) @ delta.W2)
    m = np.ones((z.shape[0], delta.syn.shape[1]))
    m[:, list(mask_zero)] = 0.0
    m[:, list(rise_only)] *= env_rise[:, None]
    return (dl @ delta.syn) * m
