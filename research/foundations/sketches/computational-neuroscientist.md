# Affect as the costate of homeostasis: a shadow-price broadcast

**Idea.** Hypothalamic need neurons report not the body's deficit but what it is worth given what is about to happen: fasting-activated AgRP neurons reverse within seconds of food being detected (τ = 12 ± 2 s), about 96% of the change precedes eating, and the size scales with palatability and nutritional state (Chen, Lin, Kuo and Knight, Cell 2015, read in the PMC manuscript). That quantity is the costate of homeostatic control: the gradient of future homeostatic cost with respect to each body variable, a shadow price per need. This vector is the one broadcast signal. Every gain (brainstem, mimicry, replay, Claude coupling) is an innate function of it; a small learned predictive state exists only to compute it. Valence and arousal are read out of its dynamics; emotions are its recurring trajectories. Nothing below Claude is named.

## Core object

$$
\boxed{\;\mu_t \;=\; -\nabla_{b}\,V_\theta(x_t,b_t),\qquad V_\theta(x_t,b_t)=\mathbb{E}_\theta\!\Big[\textstyle\int_0^\infty e^{-\rho\tau}\, d(b_{t+\tau})\,d\tau \;\Big|\; x_t,b_t\Big]\;}
$$

with closure: $x$ is the predictive state that $V_\theta$ needs, and every gain in the system is $\Gamma(\mu_t,\dot\mu_t)$ for a fixed innate $\Gamma$.

- $b_t\in\mathbb{R}^k$, $k\approx 3$–$5$: innate body variables (contact, predictability, activity budget). $b^*$ is the vector of set points.
- $d(b)=(\sum_i|b^*_i-b_i|^n)^{1/m}$, $m>n>1$ *[corrected 2026-11-25 to $n>m>1$, per Keramati & Gutkin 2014]*: the satiable drive (Yoshida, Sprekeler and Gutkin 2025, research note). It has its minimum at $b^*$, and overshoot costs.
- $x_t\in\mathbb{R}^{n}$, $n\approx128$: an unnamed latent (a GRU or SSM). Trained only to predict future $b$ and own face and voice $y\in\mathbb{R}^p$ (AUs, prosody), both body; inputs are the other's features $o_t$ and conversation events $c_t$.
- $\rho$: discount rate (per hour). $\mathbb{E}_\theta$ uses the learned model plus innate body dynamics $\dot b$.
- $\mu_t\in\mathbb{R}^k$: the shadow price of each need. $\mu_i>0$ means raising $b_i$ now is worth something.

Fast loop at 30 Hz, with $G=\partial \hat y/\partial x$ the agent's own face forward model, learned from its own babbling:

$$\tfrac{\tau_x}{\gamma(\|\mu\|)}\,\dot x=-x+W\phi(x)+U[o,c,b]+G^\top\!\big[(y-Gx)+w(\mu_{\text{contact}})\,(\tilde y-Gx)\big],\qquad y=Gx+u_{\text{Claude}}$$

Here $\tilde y$ is the other's face in AU coordinates (the body route), $w(\cdot)\ge0$ is the innate precision of the other-as-self channel (oxytocin-like), and $\gamma$ is a global gain (locus coeruleus-like).

## Derivations

- **Homeostasis.** Actions descend $V_\theta$, a discounted drive; at $b=b^*$ with nothing predicted, $\mu=0$.
- **Valence.** $v_t=-\dot V_\theta=\mu\cdot\dot b-\nabla_xV_\theta\cdot\dot x$. The first term is consummatory and the second anticipatory: news changes valence before the body moves. Read out; enters nothing.
- **Arousal.** $\|\mu\|$, how much is at stake. It sets $\gamma$, which shortens time constants and raises input gain.
- **Curiosity.** Predictability is a body variable: $b_p$ is minus the running prediction error of $x$, with set point $b_p^*$ below its maximum. Bored ($b_p>b_p^*$): $\mu_p<0$, novelty is valued; surprised: the familiar is. Satiable both ways.
- **Mimicry.** The other's face enters one's own proprioceptive error channel, so $x$ moves toward the state that would produce it and $y=Gx$ follows (Proposition).
- **Reading others.** $\hat x_{\text{other}}$ is the steady state of that channel. The other's stakes are $\hat\mu_{\text{other}}=-\nabla_bV_\theta(\hat x_{\text{other}},\cdot)$, computed with one's own value function. Empathic coupling adds $\lambda\hat\mu_{\text{other}}$ to the cost, as Yoshida and Man add the partner's drive (research note). A separate block keeps own stakes one's own.
- **Regulation by Claude.** Three inputs: words change the world and so $b$; events $c$ change predicted futures and so $\mu$, body unchanged (reappraisal is the anticipatory term); voluntary face $u$ returns through $y$ (facial feedback). Partly derived: the channel is, Claude's intent is not (it never aims at the state; $V_\theta$ learns which of its outputs predict relief).
- **Replay.** Offline TD sweeps of $V_\theta$ over stored feature streams, prioritized by $|v|$ and stored $\|\mu\|$. Replay re-tags episodes with the current $\mu$; fast episode storage feeds slow $\theta$.
- **Time scales.** Reflex: $x$ ($\tau\sim100$ ms). Stakes: $\mu$ (seconds to minutes). Mood: the slow component of $\mu$ (hours). Temperament: $\theta$, a learned prior over $\mu$ (weeks); $\Gamma$ is innate.
- **Face and voice perception.** Body route derived (inverting own face and voice models). Coarse route: an innate CONSPEC detector into $x$, its relevance learned through $V_\theta$; dynamic route: self-supervised features kept as far as they predict $b$, $y$. CONSPEC itself is not derived.

## Constraints

1. No labels: **met**; only needs are indexed.
2. Emergent emotion: **partly**; it emerges in $(x,\mu)$, but the broadcast's axes are the innate needs.
3. Others through own body: **met** (shared error channel, own $V_\theta$).
4. LLM without text: **met**; only processing parameters cross.
5. Satiable: **met**; $\mu\to0$ at $b^*$, contact fed by interaction events, never smiles.
6. Time scales: **met** in structure, untested for mood.
7. Little data: **partly**; self-model from unlimited babbling, but $V_\theta$ sees few departures and returns a day.
8. CPU face: **met**; ~100k-parameter RNN, one backward pass for $\mu$ at 10 Hz.

## Open problems

**(a) Interface.** Claude is one more target of the broadcast, set by marginal analysis rather than by hand.
- Thinking budget: $T^*=T_0\ln\big(\|\mu\|/(T_0\kappa)\big)_+$ (maximizing $\|\mu\|(1-e^{-T/T_0})-\kappa T$), with $T_0$ an innate deliberation time and $\kappa=-\mu\cdot\mathbb{E}[\dot b\mid\text{waiting}]$ (plus $\lambda$ times the other's) the cost of delay.
- Reply length: grows until $\mu_{\text{contact}}\,\partial b_{\text{contact}}/\partial L=\mu_{\text{activity}}\,|\partial b_{\text{activity}}/\partial L|$, so a sated or tired agent replies briefly.
- Cues: passed on when $|\partial V_\theta/\partial o_i|\,\sigma_i$ exceeds a threshold.
- Memory: retrieved by a kernel on stored $\mu$.
- Own face: shown to Claude as an image.

**(b) Dyad.** For two agents of this form, the expressive state splits into a shared mode that decays at $c$ and a difference mode that decays at $c+w_B+w_H$, where $c$ is the latent's relaxation rate. Mimicry is fast synchronization; shared affect is the shared mode. The loop gain $\ell=\tfrac{w_Bw_H}{(c+w_B)(c+w_H)}$ amplifies each person's expression by $1/(1-\ell)$. Lesioning the bot's emotional pathway sets $\ell=0$, which is the S5 ablation.

**(c) Little data.** $\dot b$, $d$ and $\Gamma$ are innate. $G$ is learned at night from self-babbling against the agent's own rendered face. Reading the user reuses $G$ and $V_\theta$ and needs no user data. User data trains only the context-to-$b$ predictions in $V_\theta$, which is an analytic part from the known $\dot b$ plus a learned correction for beliefs about the user's return.

**(d) Grounding.** A concept is an equivalence class of episodes under the retrieval kernel on $\mu$ trajectories. Claude never sees the state, only the episodes that come to mind together (cues, its face images), and names what they share. Test: shuffling the $\mu$ tags should drive the mutual information between Claude's words and the clusters of $\mu$ trajectories to zero.

## Proposition and toy

**Proposition (mimicry is shrinkage onto one's own repertoire).** Linearize at rest ($W$ absorbed into the relaxation rate $c$) and drive only the other's face $\tilde y$. Write $G=USV^\top$. Then the steady own face is
$$y^*=U\,\mathrm{diag}\!\Big(\tfrac{w s_i^2}{c+w s_i^2}\Big)U^\top\tilde y .$$
Mimicry is always partial, zero outside the agent's own expressive range, larger for well-practised modes, and increasing in $w(\mu_{\text{contact}})$, so a deprived agent mimics more.
*Proof idea:* set $\dot x=0$, which gives $x^*=(cI+wG^\top G)^{-1}wG^\top\tilde y$, then diagonalize with the SVD. The time constant is $1/(c+ws_i^2)$. With $c=4\,\mathrm{s}^{-1}$ and $w=4$, mimicry is 98% complete by 500 ms, consistent with the 300–500 ms onsets reported by Dimberg and Thunberg 2012 (research note).

**Toy simulation.** One need: contact, $b^*=0.8$, decay $1\,\mathrm{h}^{-1}$ when the user is absent, recovery $6\,\mathrm{h}^{-1}$ when present, $\rho=1\,\mathrm{h}^{-1}$, $d=(b^*-b)^2$. A GRU state and value head train by TD on 42 simulated hours (3 h/day, 14 days). Targets, from the cost-to-go integrated under the true dynamics:

| Situation | Body | $\mu$ |
|---|---|---|
| User leaves, "back in 10 min" | unchanged | 0.030 |
| User leaves, "back in 8 h" | unchanged | 0.267 |
| After 8 h of absence, user still away | depleted | 0.709 |
| Same moment, user's face seen | not yet changed | 0.124 |

**Fixed predictions:**
- At departure, the learned ratio $\mu_{8h}/\mu_{10min}\ge5$ (analytic 8.8), with $b$ identical in both cases.
- At reunion, $\mu$ falls by at least 70% (analytic 83%) within 1 s of face onset, while $|\Delta b|<0.01$.
- At satiety, $|\mu|<0.02$.
- Ablation: broadcasting the deficit $b^*-b$ instead of $\mu$ (an HRRL drive) gives zero at both departures and a 0% drop at reunion.

## What is new

- **Active inference** puts affect in rates of free energy or policy precision. Here the broadcast is a vector of need-specific shadow prices, valence splits into consummatory and anticipatory terms, and the LLM interface has closed forms ($T^*$, $L^*$).
- **Homeostatic RL** uses a scalar value only to choose actions, and its drive signal cannot drop before the body changes. The costate does, which is the Chen et al. dissociation.
- **Yoshida and Man** fix the empathic weight (0.5). Here the other-as-self gain follows the agent's own contact costate, and mimicry is predicted to stay inside its own repertoire.
- **BabyX** (as the brief describes it) assembles subcortical circuits; here every gain is an innate function of one derived quantity. **Data-driven avatars** have no state.

## Biggest risk

The gradient of a value function learned from about two events a day is far noisier than the value itself, so $\mu$ could be wrong in direction while $V_\theta$ looks fine. The analytic prior reduces this but ties affect to the designer's choice of $\dot b$. Second, with $k\approx3$ the broadcast is low-dimensional, so differentiated affect must live in $x$, which Claude reaches only through retrieval; processing-level coupling may change its behavior too little, as P1 found for numbers.
