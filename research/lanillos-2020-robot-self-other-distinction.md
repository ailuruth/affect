# Robot self/other distinction: active inference meets neural networks learning in a mirror (Lanillos, Pages & Cheng)

Pablo Lanillos, Jordi Pages & Gordon Cheng, *ECAI 2020*, Frontiers in Artificial Intelligence and Applications 325:2410–2416, doi:10.3233/FAIA200372 (arXiv:2004.05473).

## What was read
**Not the paper.** arXiv and the Radboud repository were blocked by this session's network policy. What I had: abstract fragments in search excerpts. **No accuracy figures, architecture details or equations were seen.**

## The computation, precisely
- **Claim (abstract-level):** self/other distinction and mirror self-recognition cast as **free-energy minimisation with a learned forward model**. The robot learns the expected visual input given its own inferred body state, from non-appearance cues (the motion contingency, not what it looks like). An observed body is classed as *self* when the forward model, driven by the robot's own actions, explains it: the prediction error stays low while the robot acts. Otherwise it is *other*. Tested on a humanoid (TIAGo, per the authors' other work [unverified]) in a mirror, robot vs robot, and robot vs human.
- **What the signal depends on:** the agent's *own action*, which causes the predicted visual change. This is the comparator of blakemore-wolpert-frith-2002 and the cue integration of synofzik-2008-2013, implemented as accumulated prediction error under an active-inference controller.

## What it means for the designs
- **A working recipe for the source tag.** The attribution $a_t = p(\text{self} \mid o_{1:t}, u_{1:t})$ is computed from how well the agent's forward model, given its own commands, explains the observed body. For a face dyad, run it per action unit or per expression component: a partner movement that the agent's own recent commands do not predict is other-tagged.
- **Known failure with a mimicking partner** (already noted in blakemore-wolpert-frith-2002 and contingency-causal-synthesis.md): a partner who copies the agent looks like a mirror, so it gets tagged *self*. The cure there is the agent's own exogenous variation. Here it means the partition is only identifiable when the agent's own output has variance the partner cannot predict.
- **Time scale:** accumulation over a short window (seconds), for which the source gives no figure.

## Verdict
**watch (abstract-level).** It confirms that the attribution step can be a learned forward model plus prediction error, which the repo already has from the agency notes. Nothing new beyond that until it is read.
