# Multi-Agent MDP Homomorphic Networks (van der Pol, van Hoof, Oliehoek & Welling)

Citation: E. van der Pol, H. van Hoof, F. A. Oliehoek, M. Welling, "Multi-Agent MDP Homomorphic Networks", ICLR 2022. arXiv:2110.04495v2.

Source read: arXiv PDF, text-extracted. Read in full: abstract, §§1–5 (related work, MMDPs and groups, distributing symmetries, the equivariant message-passing network, wildlife-monitoring and traffic-light experiments). Appendices were not read beyond the references in the main text.

## What the paper does
- **Problem.** In a cooperative multi-agent system, a global symmetry (rotating the world by 90°) maps one agent's situation onto another agent's, possibly far away and out of communication. Single-agent equivariance therefore only works centrally.
- **Factorisation (Definition 4, eq. 6).** A distributable global symmetry L_g[s] = (P_g^s[{L̃_g[s_i]}], P_g^e[{U_g[e_ij]}]) is a permutation of agents and of edges, plus a local transformation of each agent's observation and a transformation U_g of each edge feature (e.g. the difference vector between agents' coordinates). Uncoordinated local transformations are *not* a symmetry (Fig. 4).
- **Network.** A message-passing network whose message function and node update are equivariant (eqs. 9–14), with a direct-sum representation T_g = U_g ⊕ L_g for edges (rotation matrices) and agent encodings (permutations of group channels); weights constrained by the Symmetrizer (projection onto the equivariant subspace).
- **Evidence.** C4 symmetry: on drone wildlife monitoring (3 and 4 agents, 15 seeds) and 4-intersection traffic lights, the equivariant MPN learns faster than a standard MPN and than stochastic or full data augmentation (Fig. 5 and the traffic figure). Effect sizes are shown as learning curves only.

## What it means for the design
1. **The equivariance that matters between agents lives on the edge.** The relation between two agents (e_ij) must transform with the global symmetry; agent identity is a permutation. For a dyad this gives the familiar block form (cohen-welling-2016-group-equivariant-cnn.md): swap-equivariance alone cannot say "whose".
2. **Local (per-agent) transformations are not symmetries of the joint problem.** This is the multi-agent counterpart of Noether's Theorem II: making the computation invariant to each agent's own frame independently is a gauge freedom that must be compensated by edge (link) variables. That is the route of Direction 2 in new-core-search-3-synthesis.md, which reduces to relative frames.
3. **Cooperative, shared reward.** The setting assumes a common objective, which this project's agent must not have with the user (Principle 6), so the factorisation is a typing rule only.

## License
Paper: ICLR (author copyright). Code not checked.

## Runs on this Mac without a GPU?
Small PPO policies on 21×21 images; probably yes, slowly. Not run.

## Verdict: watch (typing rule for relational edges)
Confirms that between-agent symmetry is carried by permutations plus edge features; it supplies no mechanism for self/other separation or for copy avoidance.
