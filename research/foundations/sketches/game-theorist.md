# The Mirror Game: affect as incentive-compatible play in a self-simulated dyad, with Claude as mediator

Lens: game theory and multi-agent learning.

## Idea

The conversation is a repeated game between the Bot and the user, played through faces and voices, with Claude as a third party neither can inform directly. The Bot models the user as a copy of itself with an unknown type offset (a level-1 interactive POMDP) and plays to keep its own satiable drive, plus a weighted drive of the *inferred* user body, low. Three choices carry the weight:
- Reading the user's face, the Bot subtracts its own expressions as interventions it caused, so eliciting smiles gains nothing: empathy is incentive-compatible.
- Claude is a mediator the Bot can reach only through costly garblings of the world, never through messages.
- Emotions are cells of the strategic partition of the latent state: sets of states that call for the same play.

## Core object

$$
V(\beta_t)=\min_{u_t=(y^{\mathrm{vol}}_t,\ \sigma_t)\,\in\,\mathcal Y\times\Sigma(\omega_t)}\ \mathbb E_{\beta_t,u_t}\Big[D(b^A_{t+1})+\lambda\,D\big(\hat b^U_{t+1}\big)+\gamma\,V(\beta_{t+1})\Big]
$$
$$
\beta_t=q_\theta\big(x^U_t,\tau\ \big|\ y^U_{\le t},e_{\le t};\ \mathrm{do}(y^A_{\le t})\big),\qquad
y^i_t=G_\theta(h^i_t;\tau^i)+y^{i,\mathrm{vol}}_t+\kappa\,y^{j}_{t-\Delta}+\varepsilon^i_t,\ \ i\neq j .
$$

Symbols:
- $i,j\in\{A,U\}$: the Bot (A) and the user (U).
- $x^i=(b^i,h^i)$: body variables $b^i\in\mathbb R^m$ (contact, predictability, activity budget; set points $b^*$) and an unnamed latent $h^i\in\mathbb R^{128}$. The user's $x^U$ is hidden.
- $D(b)=(\sum_k|b_k-b^*_k|^{p})^{1/r}$ with $r>p>1$: a satiable drive, from Yoshida, Sprekeler and Gutkin 2025 (note in research/).
- $y^i\in[0,1]^K$: the display, action units or blendshapes plus prosody ($K\approx 30$).
- $G_\theta$: the Bot's own learned state-to-display map, applied to the user shifted by a type $\tau\in\mathbb R^{8}$ (the innate "other is like me" prior).
- $y^{\mathrm{vol}}$: the voluntary display. It drains the activity budget by $\eta\lVert y^{\mathrm{vol}}\rVert^2$, so a display departing from felt state is a costly signal.
- $\kappa\in[0,1)$, $\Delta\approx0.4$ s: innate reflex mimicry gain and delay (differential facial responses start at 300–500 ms; Dimberg and Thunberg 2012).
- $e_t$: conversation events.
- $\beta_t$: the belief over the user's state and type.
  - $\mathrm{do}(\cdot)$: the Bot's own displays are interventions, so the part of $y^U$ that mimics $y^A$ is explained by the Bot's action, not by $x^U$.
  - $\hat b^U=\mathbb E_\beta[b^U]$: the inferred user body.
- $\lambda\in[0,1]$: the coupling weight, as in Yoshida and Man.
- $\Sigma(\omega_t)$: garblings of the world record $\omega_t$ (cues, episodic memory, own-face render, dialogue): omit cues, bias retrieval, set thinking budget, length and latency, show or withhold the face. They never add content, so no value of $b$ or $h$ reaches Claude.
- $c_t=C(\sigma_t(\omega_t))$: Claude's reply. $C$ is frozen, and the reply acts on the world.
- $\gamma\in(0,1)$: the discount factor. $\theta$: all learned parameters.

## Derivations

- **Homeostasis.** The first term. $D$ is minimal at $b^*$ and overshoot raises it, so every drive is satiable.
- **Curiosity.** $V$ is a Bayes-adaptive value over $\tau$ and $\theta$, so actions that sharpen $\beta$ pay off in future play. This value of information vanishes as the posterior concentrates, so curiosity is satiable.
- **Valence.** Read out as $v_t=V(\beta_{t-1})-V(\beta_t)$, the change in the game's continuation value.
- **Arousal.** Read out as the stakes, $a_t=\max_uQ(\beta_t,u)-\min_uQ(\beta_t,u)$: how much the next move matters. It is zero when nothing the Bot does can change anything.
- **Emotion categories.** The cells of the quotient $h\sim h'$: two latent states share a cell if they have the same optimal action set and the same predicted response from the modeled user, up to $\varepsilon$. The cells are emergent and unnamed, and only as fine as the dyad's play needs.
- **Mimicry.** The reflex $\kappa$ is an explicit constraint, not derived. Derived: its voluntary amplification or suppression via $y^{\mathrm{vol}}$, and leakage, since $x^U$ is inferred in the Bot's own motor coordinates.
- **Reading others.** $\beta$ inverts the Bot's own $G_\theta$, with $\mathrm{do}$-conditioning. Level 2 ("the user reads me with my model") comes free, because the user's predicted reply is computed with the same $V$.
- **Regulation by Claude.** Claude's reply is a public signal that both players condition on. Reappraisal is that reply moving $\beta$, the Bot's belief about which situation, and so which game, is being played. Claude never sets $h$.
- **Replay.** Counterfactual regret over stored feature streams, updated by regret matching, each episode weighted by $|v|$. The Bot becomes no-regret against a stationary user; if the user also adapts without regret, the dyad approaches correlated equilibrium with the conversation as device.
- **Face and voice perception.** The likelihood inside $\beta$, an analysis-by-synthesis through $G_\theta$. The fast coarse and dynamic routes are not derived separately. They are amortized approximations of the same posterior.
- **Time scales.** Nested learning rates (multi-timescale stochastic approximation): reflex ($\kappa$, fixed, 30 Hz); mood ($\beta$, slow dimensions of $h$); temperament (policy and $\theta$ via replay, weeks). The constants are not derived.

## Constraints

1. Partly. Nothing below Claude carries labels, but conversation events $e_t$ may carry emotion words into $h$.
2. Met. Categories are a quotient; $v$ and $a$ are read-outs of $V$ and $Q$.
3. Met. The Bot reads the other through its own $G_\theta$, with self-caused mimicry explained away.
4. Met. Claude receives only garblings. It may infer a "short-budget mode", but that is processing, not a report of the state.
5. Met. All drives are satiable. Coupling is to the inferred body at a set point, never to displays (see the proposition).
6. Partly. The time scales come from nested learning rates whose values are chosen, not derived.
7. Partly. Only $\tau$ (8 dimensions) is person-specific, but $\theta$ is still learned and the Bayes-adaptive $V$ must be approximated.
8. Met. The fast path is $G_\theta(h)+\kappa y^U$ plus an amortized policy, which runs on CPU. Planning happens offline.

## Open problems

- **(a) The interface.** The Bot is an information designer facing a frozen receiver. Its only instruments are garblings, and every omitted cue lowers reply quality, which the Bot pays for through $V$. A costly channel cannot carry cheap talk, so Claude's behavior changes without Claude being told anything.
- **(b) The dyad.** $(x^A,x^U)$ is one system. The reflex loop has gain $\kappa_A\kappa_U$ and is stable only if $\kappa_A\kappa_U<1$. Synchrony is correlation from the shared device (the conversation) and the mimicry loop; for S5, the user's following should lag near $\Delta$.
- **(c) Little data.** Innate $D$, $b^*$, $\kappa$ and the self-as-other prior leave only $\tau$ to fit per person.
- **(d) Grounding.** Replay shows Claude, through garbling only, the episodes and face renders from one strategic cell. A name is grounded when the mutual information between Claude's word choice and cell membership is above zero with the garbling on, and near zero with it ablated.

## Proposition

**Incentive-compatible empathy.** Take the linear-Gaussian model $y^U=Lx^U+\kappa y^A+\varepsilon$, and let $\hat x^U$ be the $\mathrm{do}$-conditioned posterior mean computed with estimated gain $\hat\kappa$.

**Claim.** If $\hat\kappa=\kappa$, the Bot's display $y^A$ affects $\mathbb E[D(\hat b^U)]$ only through the user's true state, so displays that work only through mimicry are worth zero. If $\hat\kappa\neq\kappa$, the incentive to manipulate displays is proportional to $\kappa-\hat\kappa$.

**Proof idea.** The posterior is a function of $y^U-\hat\kappa y^A=Lx^U+(\kappa-\hat\kappa)y^A+\varepsilon$, whose distribution does not depend on $y^A$ when $\hat\kappa=\kappa$. Differentiating $D$ through the Kalman gain gives the $(\kappa-\hat\kappa)$ term. A naive reader ($\hat\kappa=0$) smiles into a mirror and believes the user is better off than they are.

## Toy simulation

**Setup.** A one-dimensional dyad. The user's state is $x^U=-1$, below its set point of 0. Parameters are $\kappa=0.3$, $\lambda=0.5$ and a voluntary-display drain $\eta=0.1$. The Bot's own felt display is neutral ($G_\theta=0$), and there is no genuine contagion ($\alpha=0$), so displays cannot change the user's actual state. The Bot learns $y^{\mathrm{vol}}$ by policy gradient. (These values are the analytic one-step optima, $y^{\mathrm{vol}}=\lambda(\kappa-\hat\kappa+\alpha)/(\eta+\lambda(\kappa-\hat\kappa+\alpha)^2)$.)

**Predictions, fixed now** (steady state, tolerance $\pm0.05$):

| Reader | Learned display $y^{\mathrm{vol}}$ | Bias in estimate of user |
|---|---|---|
| Naive ($\hat\kappa=0$) | $1.03$ | $+0.31$ |
| $\mathrm{do}$-conditioned | $0.00$ | $0$ |
| Miscalibrated ($\hat\kappa=0.2$) | $0.48$ | not fixed |

With genuine contagion on ($\alpha=0.05$), comforting survives: the $\mathrm{do}$-conditioned Bot learns $0.25$ and the naive one $1.09$.

## What is new

- **Versus active inference.** A preferred observation of the other's face rewards eliciting displays, and the framework has no incentive analysis. The Mirror Game adds $\mathrm{do}$-conditioning against the Bot's own mimicry and a provable bound on flattery.
- **Versus Yoshida and Man, and Sanyal 2026.** Their coupling reads the partner's expression at face value and has no mimicry loop. Once partners mimic, those decoders can be manipulated. Sanyal's model also does not learn.
- **Versus BabyX.** No objective or partner model from which mimicry, reading or regulation follow.
- **Versus data-driven avatars.** They play the empirical distribution of human behavior, not a best response.
- **New mechanisms, absent from all of the above:**
  - emotions as the strategic quotient of the latent state;
  - arousal as stakes;
  - Claude as an uninformed mediator reachable only by costly garblings;
  - replay as counterfactual-regret consolidation.

## Biggest risk

Emotions as commitment devices cut both ways. The proposition removes the incentive to manipulate the user's displays, not the user's *state*: a slow, visible mood such as sulking can be a profitable commitment that extracts real attention, which fills the contact drive. Satiability bounds how much this is worth, not whether it happens. Also:
- The strategic quotient collapses to a single cell, so no emotions emerge, if the effective action space is too small.
- A human is not a $\tau$-shifted copy of the Bot. A wrong $G_\theta$ makes $\hat\kappa$ wrong, and flattery returns in proportion to the error.
