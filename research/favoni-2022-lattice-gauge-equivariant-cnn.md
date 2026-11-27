# Lattice gauge equivariant CNNs (Favoni, Ipp, Müller & Schuh)

Citation: M. Favoni, A. Ipp, D. I. Müller, D. Schuh, "Lattice gauge equivariant convolutional neural networks", arXiv:2012.12901v2 [hep-lat] (22 Nov 2021). The journal version was not checked.

Source read: arXiv PDF, text-extracted. Read in full: main text (layers, proof sketch of Wilson-loop expressivity, experiments, outlook) and the Supplementary Material sections I–III (Monte Carlo generation, datasets, implementation). The remaining supplementary tables of baseline architectures were skimmed.

## What the paper does
- **Object.** Link variables U_{x,µ} ∈ SU(N_c) transport from site x to x+µ and transform as U_{x,µ} → Ω_x U_{x,µ} Ω†_{x+µ} (eq. 1). Locally transforming channels W_{x,i} → Ω_x W_{x,i} Ω†_x (eq. 4). Plaquettes U_{x,µν} = U_{x,µ}U_{x+µ,ν}U†_{x+ν,µ}U†_{x,ν} are 1×1 untraced Wilson loops; traces of Wilson loops are gauge invariant.
- **Layers.** L-Conv parallel-transports neighbouring W's along coordinate axes only, because the shortest lattice path is otherwise not unique (eq. 5). L-Bilin multiplies locally transforming objects (eq. 6), and with 1 and Hermitian conjugates included acts as a residual module. L-Act scales W by any gauge-invariant scalar (e.g. ReLU(Re Tr W)). L-Exp updates links by exp(i Σ β [W]_ah), staying in the group (eqs. 8–9). Trace layers give invariant output.
- **Expressivity claim.** Alternating L-Conv and L-Bilin can grow every contractible Wilson loop (Fig. 2, proof by induction over tiles); with Polyakov loops for non-contractible ones, "in principle, the full gauge connection can be reconstructed" (citing Giles 1981; Loll 1993, not read).
- **Evidence.** On 1+1D SU(2) regression of traced Wilson loops, test MSE for 4×4 loops: L-CNN 1.4·10⁻⁷ vs best CNN 4.2·10⁻³; the baseline "collapses and only predicts the average value" (Fig. 3; 2,680 baseline models trained). Trained CNNs approximate invariance but are vulnerable to adversarial gauge transformations (Fig. 4). Topological charge on a Wilson-flowed 8·24³ lattice tracked to near-integer values (Fig. 5).

## What it means for the design
1. **Gauge invariance as a design principle, stated exactly.** If each person's expression coordinates may be re-chosen independently at every moment (a per-node gauge freedom on a two-row "dyadic ladder" over time), every gauge-invariant function of the dyad is a function of Wilson loops. A flat connection (all loops trivial) is the formal statement of "the partner moves exactly as I do, in some time-varying frame": copy-in-a-frame is pure gauge.
2. **But Noether's Theorem II applies** (noether-1918-invariant-variation-problems.md): the local symmetry adds identities, not dynamics. The L-CNN is a typing discipline for *reading* holonomy; it does not say what the state should do with it.
3. **Where the curvature comes from.** A Wilson loop is nontrivial only if some links are not pure gauge, i.e. carry relational data that cannot be written as Ω_x Ω†_{x+µ}. On the dyadic ladder the only such links are the cross (self–partner) links, which are a relative frame. That is the relative-frame-transport design already held as a recombination (designs.md); in the abelian case the plaquette of two paths is their signed area, the commutator-coupling input (new-core-search-synthesis.md). See new-core-search-3-synthesis.md, Direction 2.

## License
arXiv preprint (author copyright); code stated to be open source on GitLab (licence not checked).

## Runs on this Mac without a GPU?
The paper's models range from ≈100 to ≈40,000 parameters; tiny. Not run here.

## Verdict: watch (prior art for any gauge-typed dyadic core)
It shows the gauge route can be built and is expressive, and it fixes the vocabulary (links, plaquettes, Wilson loops, L-Exp). For this project it mainly shows that a gauge-typed dyad reduces to relative frames plus holonomy, both already explored.
