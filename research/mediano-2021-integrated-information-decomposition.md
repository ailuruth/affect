# Towards an extended taxonomy of information dynamics via Integrated Information Decomposition (Mediano, Rosas et al.)

Pedro A. M. Mediano, Fernando E. Rosas, Andrea I. Luppi, Robin L. Carhart-Harris, Daniel Bor, Anil K. Seth & Adam B. Barrett, arXiv:2109.13186v1 [q-bio.NC], 27 Sep 2021 (ΦID).

## What was read
The full arXiv v1, about 13,400 words: main text, Methods (double-redundancy lattice, axioms, Proposition 1) and Supporting Information §§I–VII. Covered: the product-lattice proof, PID atoms decomposed into ΦID atoms, the CCS and MMI double-redundancy functions, single-atom proofs for the COPY, XOR and PPR systems, the construction of single-atom systems, the AR system, and the whole-brain model set-up. I skimmed the DMF parameter tables. Figures were read from their captions. Rosas et al. 2020 ("Reconciling emergences") was not read; nothing here relies on it.

## The computation, precisely

**From PID to ΦID.** For two elements with Markov dynamics, the time-delayed mutual information I(X_t; X_{t+1}) can be decomposed with a forward PID (past parts as sources, joint future as target). That "can tell where the information is coming from, but not where it is going to." ΦID takes the product of the forward and backward PID lattices: atoms α → β with α, β ∈ {Red, Un1, Un2, Syn}, giving 16 atoms with the order α→β ≼ α′→β′ iff α ≼ α′ and β ≼ β′.

**Axioms.**
1. Compatibility: the double-redundancy reduces to a PID redundancy when either side is a single set, and to mutual information when both are.
2. Partial ordering: it is monotone on the product lattice.

Proposition 1 ("15-for-free"): Shannon quantities and two single-target PIDs fix 15 atoms, and one extra function, I_∂^{{1}{2}→{1}{2}}, fixes the 16th. Two choices are given: a multi-target CCS (Ince) and MMI, I_∂^{MMI} = min_{i,j} I(X_i; Y_j).

**Taxonomy (six modes).**
- Storage: Red→Red, Un_i→Un_i, Syn→Syn.
- **Copy: "Information that becomes duplicated." Un1→Red, Un2→Red.**
- Transfer: Un1→Un2, Un2→Un1.
- Erasure: Red→Un_i.
- Downward causation: Syn→Un_i, Syn→Red.
- Upward causation: Un_i→Syn, Red→Syn.

**What standard measures are.** TE(1→2) = Syn→Red + Syn→Un2 + Un1→Red + Un1→Un2. "Un1→Un2 is the only 'genuine' transfer term". Causal density (the sum of both TEs) double-counts Syn→Red. Φ_WMS = all synergies + transfer − Red→Red, so it goes negative in redundant systems. The revised Φ_R adds the double-redundancy back.

**Three logic-gate systems with Φ_WMS = 1** and a single nonzero atom each:
- COPY (Y2 = X1): Un1→Un2 = 1;
- downward XOR (Y1 = X1 ⊕ X2): Syn→Un1 = 1;
- parity-preserving random: Syn→Syn = 1. This system "has zero CD and zero AIS, yet it clearly has dynamical structure".

**Data.** In 40 Fantasia subjects, breath-to-heart TE exceeds heart-to-breath TE. The excess "is driven by" Syn→Un, not by Un→Un, and Un→Red goes in the opposite direction. The DMF whole-brain model: Φ_R peaks near G ≈ 2 where Φ_WMS dips below zero.

**Stated limits.** The results depend on the chosen double-redundancy function ("there is not yet a consensus"). The framework is observational: it is Granger-sense unless p(X_{t+1}|X_t) is an interventional distribution. Non-Markovian systems are deferred to later work.

## What it means for the designs

Treat the dyad as a two-element system: X¹ = partner, X² = agent.

1. **ΦID names our failure mode, and it is still sign-blind.** "Agent copies partner" with the partner's face persisting is partner-unique information becoming redundant: Un_p→Red, ΦID's own "Copy" mode. If the partner's state does not persist, it is Un_p→Un_a (their COPY gate). An anti-copying agent (a = −p) produces exactly the same atoms, because every atom is built from mutual informations. The copy *mode* of ΦID is "duplication up to relabelling", not resemblance. It cannot serve as the per-expression constraint for the same reason as PID (williams-beer-2010).
2. **It does give two candidate signatures of the human non-copying data, as properties of the joint process:**
   - **C7 (the anti-repetition of the pair's pattern grows over minutes)** is a statement that the pair's future is not predictable from either part's past alone but is shaped jointly. That is upward causation and synergistic storage (Un→Syn, Syn→Syn) and downward causation onto the agent (Syn→Un_a). A copying dyad loads Un_p→Red and Red→Red instead. **Prediction:** across a 2-minute exchange, a human-like agent shifts weight from Red→Red toward Syn→Syn and Syn→Un_a. A copier does the opposite. This is testable with MMI-ΦID on Gaussianised features, which is cheap on a CPU.
   - **C2 ("less alike than chance at lag 1")** is *not* a synergy statement. It is a sign statement about concordance at one lag. ΦID sees it only as Un_p→Un_a or Un_p→Red, the same as copying. The human anti-copy signature therefore has two separate parts: a sign part (needs an order-sensitive measure) and a synergy part (needs PID/ΦID). Neither measure captures both.
3. **TE in a design document must be read as an aggregate.** The partner→agent TE that a contingency drive would maximise includes Un_p→Red, the copy mode. A drive on raw TE is therefore a drive that *can be satisfied by copying*. This is a concrete mechanism for the recurring indirect copy routes. A drive (or evaluation) should target the synergy atoms, or Un_p→Un_a with a separate sign guard, never TE whole.
4. **Cost and fragility.** The atoms depend on the redundancy function, and values below the MMI/CCS level are not settled. They are for analysis, not for loss functions the agent descends at runtime.

## Verdict
**Adopt as the evaluation taxonomy** for the dyad as a joint process (C7 measured as a shift from redundancy toward synergy atoms, and TE always decomposed). **Reject as the constraint**: its "Copy" mode is duplication up to relabelling and cannot tell copying from its opposite.
