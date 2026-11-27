# E(n) Equivariant Graph Neural Networks (Satorras, Hoogeboom & Welling)

Citation: V. G. Satorras, E. Hoogeboom, M. Welling, "E(n) Equivariant Graph Neural Networks", ICML 2021 (PMLR 139). arXiv:2102.09844v3.

Source read: arXiv PDF, text-extracted. Read in full: §§1–3 (equivariance, GNNs, the EGCL layer, its equivariance analysis, the velocity variant, edge inference) and the comparison table of message forms. Experiments (N-body, graph autoencoders, QM9) and appendices were skimmed.

## What the paper does
- **Layer (eqs. 3–6).** m_ij = φ_e(h_i, h_j, ‖x_i − x_j‖², a_ij); x_i ← x_i + C Σ_{j≠i} (x_i − x_j) φ_x(m_ij); m_i = Σ_j m_ij; h_i ← φ_h(h_i, m_i). Node features see only invariant squared distances; coordinates move only along relative vectors, weighted by learned invariant scalars. Proof of E(n) equivariance in their App. A (not read; the argument in §3.1 is that distances are invariant and sums of differences transform as type-1 vectors).
- **Velocity variant (eq. 7).** v_i ← φ_v(h_i) v_i^init + C Σ (x_i − x_j) φ_x(m_ij); x_i ← x_i + v_i.
- **Edge inference (eq. 8).** e_ij ≈ φ_inf(m_ij) ∈ [0, 1] gates messages without breaking equivariance.
- Claimed advantage: no spherical harmonics or higher-order representations; scales to any n.

## What it means for the design (derived here, not claimed by the paper)
1. **With two agents, the only equivariant vector is their difference.** Put the agent's expression x_s and its reading of the partner x_p in one space with translation and rotation equivariance. Then the agent's update is (x_s − x_p) φ(‖x_s − x_p‖², h). The copy point x_s = x_p is a fixed point of the coupling for every parameter value, attracting whenever φ < 0 near it, repelling whenever φ > 0. Geometric equivariance in a dyad does not avoid copy; it singles copy out as *the* distinguished point and leaves its stability to a learned scalar. The same holds for any relative-coordinate interaction (Newton's third law style).
2. **Invariant scalars in, equivariant vectors out** is still a useful typing rule for gaze and head pose (as noted for Clifford networks in ruhe-2023-clifford-group-equivariant.md), not for expression.

## License
Paper: PMLR (author copyright). Code public (licence not checked).

## Runs on this Mac without a GPU?
Small graphs, yes. Not run.

## Verdict: reject as core; keep the two-agent remark
The dyadic special case shows why "make the interaction depend only on the relation" invites copying: the relation's zero is the copy state.
