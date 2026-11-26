# AvE: Assistance via Empowerment (Du, Tiomkin, Kıcıman, Polani, Abbeel & Dragan)

Yuqing Du, Stas Tiomkin, Emre Kıcıman, Daniel Polani, Pieter Abbeel & Anca Dragan, *NeurIPS 2020*, arXiv:2006.14796v5 (7 Jan 2021). https://arxiv.org/abs/2006.14796

## What was read
The arXiv PDF in full: introduction, empowerment preliminaries, problem setting, the proxy (Algorithm 1), gridworld and Lunar Lander experiments, the user study (Tables 3–4), discussion, limitations and broader impact. There is no appendix in this version. Figures were read from their captions. The video was not watched.

## The computation, precisely
- **Empowerment.** E(s) = max over p(A⃗_T | s) of I[A⃗_T ; S_T | s], the channel capacity from the human's T-step action sequences to their final state, with open-loop actions. The probing distribution "is only used for the computation of the empowerment/channel capacity E(s), and never generates the behavior directly."
- **Assistance objective.** R(s_a, s_h) = R_original(s_a, s_h) + c_emp · E_human(s_h), with c_emp ≥ 0. The agent "does not carry the human to the goal, but instead clears a path so they can get there on their own."
- **Proxy (Algorithm 1).** Roll out N random-action trajectories of horizon T from the current state and return Var(flatten(final states)). This "relies on an assumption of homogeneous noise and high SNR". It needs a simulator of the human's dynamics.

## Evidence with numbers
- **Gridworld (100 trials)**, human trapped by heavy blocks, goal unknown to the agent. Success % (mean steps):
  - Corner: goal inference GI 90–100% (4.35–4.51); empowerment 100% (5.24); proxy 99% (8.79); oracle 100% (4.1).
  - Center: GI with a large goal set 50% (2.27); GI with a small set and the true goal missing 55% (3.3); empowerment 100% (4.8); oracle 100% (1.91).
  - The GI failure mode is that the agent "chooses to move a block on top of the true goal. As the human can no longer access the goal, they wait ... and cannot act further to inform the agent ... leading to an infinite loop."
- **Lunar Lander, simulated pilots (success %, 10 seeds):**

  | Pilot | Baseline copilot | Empowerment copilot |
  |---|---|---|
  | Noop | 5.9 | 9.7 |
  | Laggy | 38.4 | 37.3 |
  | Noisy | 8.5 | 30.7 |
  | Sensor | 2.8 | 10.8 |

  Best c_emp = 0.001 from a sweep of 1e-5 to 10.
- **User study (n = 20, within-subject, counterbalanced, 50 episodes each).**
  - Success: 33 ± 7% with empowerment vs 17 ± 9% without (paired t, p < 0.0001).
  - "Made parts of the task easier": 6.4 vs 5.55 (Bonferroni p = 0.007). "Sufficient control": 4.7 vs 3.6 (p = 0.025, 0.175 corrected). Not significant after correction.
- **Failure.** "If c_emp is too high, the copilot tends to override the pilot and focus only on hovering"; "the assistant prevents landing altogether due to prioritizing stability excessively."

## License
arXiv non-exclusive licence. Code: github.com/yuqingd/ave; licence not checked.

## Verdict
**watch (supporting evidence for option-based help with real people; not a mechanism to build).** It is the only source here that measured a human partner. Raising the human's control over what happens next doubled task success, and participants rated it as making the task easier. The measure needs a simulator of the human's dynamics, and it overrides the human when weighted too high.

## What it means for the designs
1. **Help as "clear the path, don't carry them" matches Principle 6.** The credited quantity is the partner's own control over what follows, not their expression. The goal-inference failure is the conversational one: the agent decides what the partner needs, acts on it, and leaves no move by which the partner can correct it. A comforting agent that keeps comforting someone who wanted advice is in the "block on top of the goal" loop.
2. **The overriding failure maps onto conversation as taking over.** That means talking for the partner, closing the topic, or "stabilising" their mood when they need to say something hard. It is the same failure as Franzmeyer's blocking. Weight the options term low (the paper's best was c_emp = 0.001 against a task reward) and keep it under the satiable need drive.
3. **What a dyadic "empowerment" needs is a simulator of the partner, which the design has: 𝓜's partner head.** An options estimate can be computed by rolling out the partner head over the partner's *own* next moves under each candidate agent act. The PSO rule (Farquhar) must then hold the partner's display at its baseline value inside those rollouts, so that "options" never include "options to smile".
4. **No conflict with Principle 6, if bounded.** Empowerment is not smiles, attention or time. But an agent that expands a person's options *within the conversation* has an incentive to keep the conversation going. Count options over the partner's life outside the session (stated plans, decisions reported later), or cap the term per session.
