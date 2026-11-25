# Deuflhard & Weber 2005, "Robust Perron cluster analysis in conformation dynamics" (Linear Algebra Appl. 398:161-184; ZIB-Report 03-19)

Source read: ZIB-Report 03-19 (dated October 13, 2003), the preprint of the journal paper, read as rendered page images because the PDF's Type-3 fonts defeat text extraction. Read: abstract, contents, introduction, section 1 (Perron cluster eigenproblem, uncoupled and nearly uncoupled chains, Lemma 1.1, critique of PCCA), section 2 (almost characteristic functions, Theorem 2.1, coupling matrix, Theorem 2.2 and its remark), section 3 (feasible set, objective functions I₁ and I₂, reduced feasible set, solution for k = 2), the starting-simplex subalgorithm at the end of section 4, section 5 (numerical illustrations) and the conclusion. Not read: the unconstrained reformulation in section 4 (report pp. 17-18) and the references. The published LAA version was not compared. Schütte et al. on transfer operators were not read.

## Claims
- Setting: "The stochastic matrices treated in this paper are proper discretizations of the self-adjoint transfer operator constructed by Schütte"; the matrices are "stochastic and generalized symmetric" (symmetric in the π-weighted inner product). The abstract says "Once some reversible Markov operator has been discretized". So the method assumes reversibility (detailed balance).
- Uncoupled case: with k invariant subsets the Perron eigenvalue "is k-fold, i.e. λ₁ = ··· = λ_k = 1", and the eigenvectors are combinations of characteristic functions. The authors "call k the Perron index".
- Nearly uncoupled case: "a Perron cluster of eigenvalues λ̃₁ = 1, λ̃₂ = 1 − O(ε), ... λ̃_k = 1 − O(ε), will arise", with "ε = 1 − λ̃₂" (1.7).
- Number of sets from the spectrum, in practice by inspection. HIV protease inhibitor example: "λ̃₁ = 1.0, λ̃₂ = 0.997, λ̃₃ = 0.985, λ̃₄ = 0.815, ... with a small gap after the second eigenvalue and a significant gap after the third one; hence, we chose k = 3 for the Perron index, but compared it with k = 2 and k = 4". The paper gives no numerical threshold for "significant".
- Validity checks on the chosen k: Remark after Theorem 2.2: "the Perron index k must be chosen small enough such that 1 − λ̃_k = O(√ε) does not occur." The metastability "Σ wᵢᵢ = tr(W̃)" "makes only sense as long as the (stochastic) coupling matrix is diagonally dominant, which means that wᵢᵢ > 0.5". Theorem 2.2 requires "Θ = ‖Ã⁻¹Λ̃Ã − I_k‖₁ < 1" and then bounds "Σλ̃ᵢ − O(ε²) ≤ Σwᵢᵢ < Σλ̃ᵢ" (2.12).
- What failure of k looks like: at k = 3, "Θ = 0.0165 < 1"; at k = 4, "the second row is no longer diagonally dominant (w₂₂ = 0.25 < 0.5) so that the definition of metastability no longer makes any sense. Moreover, we here get Θ = 10.776 > 1, which means that assumption (2.11) in Theorem 2.2 is violated." At k = 2 the almost-characteristic values "clearly reveal[s] the fact that the data contain three clusters rather than just two ones."
- Output: almost characteristic functions (soft memberships) satisfying positivity and "partition of unity", and the coupling matrix of stay and move probabilities "W̃ = D̃⁻²⟨χ̃, T̃χ̃⟩_π". Example k = 3: "π̃₁ = 0.51, π̃₂ = 0.37, π̃₃ = 0.12" and diagonal 0.93, 0.95, 0.74.
- Why PCCA+ replaced PCCA: the sign pattern of eigenvectors is perturbed at O(ε) while the level pattern is perturbed at O(ε²) only, so sign-based PCCA "exhibits certain structural discontinuities, which, in turn, induce some lack of robustness."

## Evidence
Perturbation theorems plus three examples (butane, an artificial k = 3 case, the HIV protease inhibitor VX-478 simulated at 900 K). No benchmark statistics.

## License
ZIB-Report freely downloadable from the ZIB OPUS server; journal version © Elsevier. No code in the paper.

## Runs on this Mac without a GPU?
Yes. It needs the top k eigenvectors of a transition matrix plus a small optimisation over k² coefficients. Third-party implementations were not checked.

## Verdict: adopt (as the method for reading emotions as metastable sets); watch the reversibility assumption
- For (d): emotions as metastable sets maps onto the Perron cluster. Count the eigenvalues near 1 before a large gap, then get soft memberships χ̃ᵢ (graded, overlapping emotion membership, no hand-named variables, consistent with Principle 2) and a coupling matrix W̃ giving persistence wᵢᵢ and transition probabilities.
- The paper chooses k by eye from the gap and then checks it with Θ < 1 and wᵢᵢ > 0.5. Those two checks give a falsifiable test for "the agent has k emotions".
- Conflict: the theory is for self-adjoint (reversible) operators. An agent driven by non-conservative forces (housekeeping heat > 0, as in Seifert and Hatano-Sasa) is not reversible. Using PCCA+ on such dynamics needs a non-reversible variant, which is not in this paper.
