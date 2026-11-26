# A unified Bellman equation for causal information and value in Markov decision processes (Tiomkin & Tishby)

Stas Tiomkin & Naftali Tishby, arXiv:1703.01585v2 [cs.SY], 5 Jun 2018.

**Substitution note.** The brief asked for Tishby & Polani 2011, "Information theory of decisions and actions" (in *Perception-Action Cycle*, Springer, pp. 601–636). The only free copy found (cse.huji.ac.il) is outside this session's network allowlist, and the Springer page is paywalled. That chapter was **not read**. This paper, co-authored by Tishby, gives the directed-information version of the same perception–action-cycle programme for MDPs and was read in its place. Nothing below cites Tishby & Polani beyond what this paper says about it ("KL-control … penalizes complex policies … does not directly address the question of the information transfer rate").

## What was read
The arXiv PDF from export.arxiv.org, in full (about 6,700 words): §1–8, including the derivations of both Bellman recursions and both simulations. The extracted equations are partly garbled. Eq. 21 in particular came out as $p^*(A'\mid S,A) = 1/|A|$, which cannot be right as printed, so it is not relied on.

## The computation, precisely

**Inbound channel (environment → agent; §3–4).** For an MDP $p(S_{t+1}\mid S_t,A_t)$ with policy $\pi(A\mid S)$, the causally conditioned directed information from states to actions obeys the recursion (Eq. 16)
$$\vec I_T(S_t,A_t) = I[S_{t+1};A_{t+1}\mid S_t,A_t] + \big\langle \vec I_T(S_{t+1},A_{t+1})\big\rangle.$$
Combined with value, this gives the unified recursion (Eq. 18)
$$G^\pi_T(S_t,A_t,\beta) = \Big\langle \ln\frac{\pi(A_{t+1}\mid S_{t+1})}{p(A_{t+1}\mid S_t,A_t)} - \beta r\Big\rangle + \big\langle G^\pi_T(S_{t+1},A_{t+1},\beta)\big\rangle,$$
minimised over π. The optimum is a Boltzmann policy $\pi^*(A\mid S)\propto\exp(-G^{\pi^*,q^*}(S,A,\beta))$ (Eq. 20/22), solved by iteration. Note the policy is compared with $p(A_{t+1}\mid S_t,A_t)$: the action *predicted from the previous state and action*. So the cost is the bits in the action that were not already predictable from the past. The cheap action is therefore the one that continues what the agent was doing.

**Maze results (Fig. 2).**
- The 625-cell maze shows a phase transition in β: at β = 0.05 the agent passes the narrow door; at β = 0.005 it "prefers not to take the risk" and takes the longer path.
- Directed information along the path is concentrated where precision matters: "near the corners and/or through the narrow door". The doorway entrance is "the maximal information rate that the agent should process".

**Outbound channel (agent → environment; §6–7).** The directed information from action trajectories to state trajectories also obeys a Bellman-type recursion (Eq. 31). Its maximisation is an empowerment-like, Blahut–Arimoto-style capacity computation (Eqs. 32–34). In the firehouse grid world, the high-value locations agree qualitatively with the minimum average shortest path.

The paper states the asymmetry: minimise the inbound rate for a given reward, and maximise the outbound rate as a target-free drive.

## What it means for the designs

- **Bits are spent in bursts at critical moments, not uniformly.** Under a rate cap, partner information is drawn when the agent's own situation is at a narrow door, a point where a small difference in the partner changes what the agent should do. For a dyad this predicts that partner-dependence concentrates at decision points: turn transitions, the onset of an event, and an appraisal-relevant change. In between, output continues on its own predicted course. That fits C4 (role and turn gate the coupling) and C8 (coupling locked to shared events) in non-copying-dynamics-synthesis.md. It also gives a reason for the *fast onset, then context* shape (gap 6): onset is when the bits are worth paying for.
- **The cost is "surprise relative to my own past action".** The comparison distribution is $p(A_{t+1}\mid S_t,A_t)$. An agent whose output tracks the partner continuously pays at every step. An agent that holds its own course and corrects occasionally pays rarely. So **inertia and smoothness (sluggishness) are the cheap default.** Sims' rational-inattention result is the macroeconomic version, but it was not read here.
- **Inbound and outbound are different quantities with opposite natural signs.** A copier has a high inbound rate, and its outbound influence is only what the partner re-copies. A *leader*, or an agent that acts on the shared world, has a low inbound and a high outbound rate. A core that held inbound DI (partner → agent) under an innate cap, while letting the agent's own satiable drives pursue outbound influence on the joint state, would make copy a poor regime on both counts. This is a candidate pairing for C7 (novelty of the joint trajectory): maximising outbound directed information over the joint state rewards *variety the agent causes*, and copy causes none. (My inference. The paper treats the two channels separately and does not combine them.)
- **Gain, sign, held levels.** Same as the Tanaka note: the rates are scale- and sign-invariant, and the paper's examples are discrete. A held partner level is nearly free once predicted.
- **Framework.** This is KL/information-regularised RL plus empowerment. Both are existing and optimisation-based, so excluded as a core. Usable as constraints:
  1. the inbound directed-information rate as the certified quantity (it has a Bellman recursion, so it can be *accounted* step by step in a running system, not only bounded offline);
  2. the inbound/outbound asymmetry as a design target.

## Verdict
**adopt (two ideas).**
1. Rate-limited agents spend partner bits in bursts at critical moments and otherwise continue their own predicted course. The cost is relative to the agent's own predicted next action, which makes inertia the cheap default.
2. Inbound and outbound directed information are distinct, and a copying regime is high-inbound and low-outbound, which gives a two-quantity handle on copy that no single gain has.

The source chapter, Tishby & Polani 2011, remains unread.
