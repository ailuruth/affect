# In-context learning and induction heads (Olsson, Elhage, Nanda, Joseph, … Kaplan, McCandlish & Olah)

Citation: C. Olsson, N. Elhage, N. Nanda, N. Joseph, N. DasSarma, T. Henighan, B. Mann, A. Askell, Y. Bai, A. Chen, T. Conerly, D. Drain, D. Ganguli, Z. Hatfield-Dodds, D. Hernandez, S. Johnston, A. Jones, J. Kernion, L. Lovitt, K. Ndousse, D. Amodei, T. Brown, J. Clark, J. Kaplan, S. McCandlish, C. Olah. "In-context Learning and Induction Heads." *Transformer Circuits Thread*, 8 March 2022. arXiv:2209.11895.

Source read: the arXiv PDF (a print of the HTML article), text-extracted. Read in full: abstract, introduction, Key Concepts, Arguments 1–6, Unexplained Curiosities, Discussion. **Skimmed only:** the Model Analysis Table, Related Work, Comments & Replications and the appendices. The interactive figures were not available. The reverse engineering is summarised from the earlier "Mathematical Framework" paper, which was not read.

## How the mechanism was found and argued
- **Definition by behaviour.** An induction head is a head that, on repeated random tokens, (i) attends to the token after an earlier occurrence of the current token ("prefix matching") and (ii) raises that token's logit ("copying"): [A][B] … [A] → [B].
- **Circuit (small attention-only models).** Two heads in different layers. A "previous-token head" writes each token's predecessor into its residual stream; the induction head's key reads that subspace (K-composition), giving a QK term Id ⊗ h_prev ⊗ W with W of positive eigenvalues, so the query (current token) matches keys that encode "the token before me". Copying is an OV circuit with positive eigenvalues. GPT-2 also uses a second, "pointer-arithmetic" mechanism through positional embeddings and Q-composition.
- **Six arguments**, with the strength of each stated per model class:
  1. **Co-occurrence.** In-context learning (loss at token 500 minus token 50) jumps abruptly between 2.5e9 and 5e9 training tokens, from < 0.15 to ≈ 0.4 nats, then stays constant across model sizes. Induction heads form in the same window. The window is the only non-convex part of the loss curve, and training trajectories turn in per-token-loss PCA space there. One-layer models show none of this.
  2. **Co-perturbation.** A "smeared key" k_j = σ(α)k_j + (1 − σ(α))k_{j−1}, one learned scalar per head, lets one-layer models form induction heads. In-context learning then appears in one-layer models, and earlier in deeper ones.
  3. **Ablation.** Removing induction heads at test time removes almost all in-context learning in small attention-only models; evidence is weaker with MLPs (interactions, layer-norm masking).
  4. **Generality.** In a 40-layer, 13B model, heads that meet the strict definition also do translation (attention "meanders" off the diagonal with word order) and abstract pattern completion (≈ 65 % of attention to the correct category in a synthetic template task). The authors call this [A*][B*] … [A] → [B]: "in-context nearest neighbors".
  5. **Mechanistic plausibility.** Searching the context for similar prefixes and copying what followed is nearest-neighbour prediction, which improves with more data points, hence with context.
  6. **Continuity** from small to large models.
- **Caveats stated.** For large models the evidence is correlational. Other composition heads may form in the same window. A constant in-context score does not mean constant mechanisms.

## The mathematical object
**A lookup keyed on what preceded each stored item, returning what followed it.** Formally, with a one-step shifted key k̃_s = φ(x_{s−1}) and value v_s = ψ(x_s):

ŷ_t = Σ_{s<t} softmax_s(⟨q(x_t), k̃_s⟩) v_s,

an associative memory over transitions in the current context. Two structural facts:
- the shift is what makes the operation possible; with it built in (smeared key) one layer suffices;
- the computation emerges abruptly in training, as a phase change, once composition is possible.

## What it means for the design
1. **Contingency as retrieval, not as correlation.** Keyed on the agent's own preceding act and returning the partner's following move, the same operation is "what you did the last times I did this": an in-context, per-partner store of the partner's responses to the agent. It keeps "you responded to me" as content (which earlier moment matched, how sharply) rather than erasing it.
2. **The output type matters.** Induction heads are copiers. Pointed at the agent's own motor output, the operation copies. It must be typed to write into the agent's model of the partner only.
3. **A built-in shift is an innate structure with an ablation.** The smeared-key result says the shift can be given rather than learned. A body-given "my previous act" key would make contingency learning available from the first exchanges; removing it should delay or remove it. That is a derived ablation prediction of the kind Principle 5 asks for.
4. **Nearest-neighbour in-context prediction is a kernel smoother.** Its residual is the partialling-out residual of derivation-self-invariant-maps.md Theorem 5, with the match temperature as the regulariser. That reduction applies directly.

## Verdict
- **adopt (method and object).** The method — a measured abrupt change, an architectural intervention that moves it, ablation, then mechanism — is the discovery pattern the project's novelty test asks for. The object, a transition-keyed associative lookup, is known; applied to the dyad it is a recombination.
