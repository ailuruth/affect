# The contingency homeostat: affect as regulation of being answered

An infant starts with no emotions. It has a body to keep in range, a contingency detector (how far what it senses depends on what it just did), and the assumption that others have bodies like its own. Self, other, attachment, mimicry and the naming of its own states are built from these inside a dyad that regulates the infant first. Here the social need is to be *answered*: a satiable need for contingent response, not for contact or smiles. A partner is weighted by how contingently it has answered before. One body map runs forward to express and is inverted to perceive. Claude takes the caregiver's place: it sees only the face and answers.

## Core object

$$
\boxed{
\begin{aligned}
V(h_t) &= \min_{u}\ \mathbb{E}\Big[\int_t^{\infty} e^{-(s-t)/T}\big(D(b_s) + \kappa_P\, D(\hat b^P_s)\big)\,ds \;\Big|\; h_t\Big], \qquad D(b)=\tfrac12\textstyle\sum_i (b_i-b_i^*)^2/\sigma_i^2\\[2pt]
y^A &= G_\theta(h) + v, \qquad \hat b^P = \beta_\theta\big(G_\theta^{-1}(y^P - \mathcal M_\theta[y^A])\big)\\[2pt]
\dot c &= -c/\tau_c + \big[\mathcal T(u \to y^P) - \mathcal T_{\mathrm{surr}}\big]^+, \qquad \kappa_P = \big\langle \mathcal T(u\to y^P)\,/\,\mathcal T(u\to y^A)\big\rangle_{\text{weeks}}
\end{aligned}}
$$

Symbols:
- $h_t\in\mathbb R^{\sim128}$ is the unnamed latent. It has blocks with fixed time constants of 33 ms, 1 s, 1 min, 1 h, 1 day and 1 week. Its dynamics $dh=f_\theta(h,u,y^P,b)\,dt+\Sigma^{1/2}dW$ learn from prediction error on $b$ and both $y$ streams.
- $b=(e,p,c)$ are innate body variables: activity budget, predictability, and received contingency $c$ ($\tau_c\approx5$ min). Their drift and satiation rules are fixed. $b^*$ are the set points and $\sigma_i$ the tolerances.
- $y^A,y^P\in\mathbb R^K$ are the agent's own and the partner's AUs plus prosody, in one coordinate space.
- $G_\theta$ maps latent to expression. $G_\theta^{-1}$ is its amortized inverse and $\beta_\theta$ maps latent to body. All three serve self and other alike; this is the like-me prior.
- $v$ is Claude's voluntary expression intent. $\mathcal M_\theta[y^A]$ is the predicted echo of the agent's own expression in the partner's face.
- $u$ is the action: expression drive, gaze, bids, and Claude's coupling settings $\phi$ (retrieval bias, thinking budget, reply length, latency, cue mask).
- $\mathcal T(x\to y)$ is lagged linear-Gaussian transfer entropy. $\mathcal T_{\mathrm{surr}}$ is the same quantity on segment-shuffled surrogates. It is subtracted because raw synchrony is positive even for dyads that never interacted (Moulder et al. 2018).
- $\kappa_P\in[0,1]$: how contingent this partner has been, relative to the agent's own body. $T\approx10$ min is the horizon.

## Derivations

- **Homeostasis.** This is the first term. $D\ge0$, and $\partial D/\partial b=0$ at $b^*$, so the drive is satiable.
- **Curiosity.** $V$ is minimized over beliefs about uncertain $\kappa_P$, session contingency and $f_\theta$. This is dual control: probing is worth something only insofar as better estimates lower future $D$. The value therefore vanishes at satiation or certainty. It is the infant testing whether the mobile follows its kicks.
- **Valence and arousal.** Valence is $\nu_t=-\tfrac{d}{dt}V(h_t)$ and arousal is $\lVert\nabla_hV(h_t)\rVert$; both are read out. Distress display is an innate reflex on level ($D>\theta$). Positive expression therefore tracks rate and distress tracks level.
- **Self/other.** These come from the contingency spectrum. Ratio near 1 at lag under 100 ms is self, as with the agent's own rendered face. Ratio between 0 and 1 at lag 0.3–2 s is another agent, and ratio near 0 is the world.
- **Mimicry.** By the like-me prior, the partner's $c^P$ is computed with the agent's own detector, so the second term pays the agent to supply contingency. The Proposition makes same-channel copying the effort-optimal supply, scaled by $\kappa_P$. Reflex mimicry at 400–500 ms (Dimberg & Thunberg 2012) is the innate initial policy, and the optimum keeps it.
- **Reading others.** $\hat b^P$ comes from inverting one's own $G_\theta$ after removing the echo $\mathcal M$. Otherwise the agent reads itself in the partner, and contagion runs away.
- **Social referencing.** When $\mathrm{Var}[V]$ is high (novelty), the like-me prior makes $\Delta\hat b^P$ a sample of one's own future $\Delta b$, fused with weight $\kappa_P\pi$ ($\pi$: precision of the reading); dual control makes looking at the partner worthwhile exactly then.
- **Regulation by Claude.** Partly derived. $\phi\subset u$ is chosen by the same minimization, and Claude's words, voice and $v$ return as sensation. $V$ learns which Claude behavior lowers $D$ in which state. Co-regulation is internalized and looks like reappraisal. A direct semantic rewrite of $h$ is not derived.
- **Replay.** Offline sweeps over stored $(y^P,b,u)$ update $V$ and $f_\theta$ in proportion to $|\text{TD error}|$, i.e. valence net of expected cost (prioritized sweeping). $\kappa_P$ and $b^*$ change only here; the slow drift of $b^*$ is temperament.
- **Face and voice.** $G_\theta^{-1}$ is analysis-by-synthesis in the agent's own AU and prosody coordinates. It is pretrained by self-babbling: render random AUs and learn to invert them, with no user data. The innate face prior becomes "a region contingent at social lags is a face".

## Constraints

1. No labels: met (AU, prosody, label-free $\mathcal T$).
2. Emergent emotion: partly. Valence and arousal are read out; categories in $h$ are not shown.
3. Own body: met (one $G_\theta$ both ways, echo removed).
4. Claude without words: met ($\phi$, retrieved episodes, its face image).
5. Satiable, no smile reward: met. A contingent frown fills $c$ as well as a smile.
6. Time scales: met (33 ms to weeks).
7. Little data: partly. Only $\kappa_P$, $V$ and slow parts of $f_\theta$ need the user.
8. CPU face: met (small recurrent model, linear $\mathcal T$ on ~50 channels at 30 Hz).

## Open problems

- **(a) Interface.** The coupling is contingency in both directions: $\phi$ shapes how Claude processes, and Claude's output returns as sensation. Attunement, $\mathcal T(h\to\text{Claude output})$, is a reportable quantity. Ablating $\phi$ should drive it to about 0.
- **(b) Dyad.** The linearized mutual-mimicry loop is stable iff $\kappa_Ag_A\kappa_Pg_P<1$, where $g$ is mimicry gain, and echo removal lowers the effective $g$. Synchrony is each side refilling the other's $c$.
- **(c) Little data.** The detector and body map are innate. What is learned is who answers: one scalar per partner plus $V$.
- **(d) Grounding.** A concept lives in the coupled system. A region of $h$ retrieves past episodes holding what Claude said then, so it tends to get the same name again. When the operator mirrors the agent, the echo carries high $\mathcal T$ from the agent's own $u$, is attributed to self, and trains $G_\theta$ (marked mirroring). Prediction: naming consistency falls monotonically with distance in $h$.

## Proposition and toy simulation

**Proposition (mimicry is not specified, it is optimal).** Assume:
- the partner's expression is $y^P\sim\mathcal N(0,\mathrm{diag}(s_i))$;
- the agent responds with $y^A_{t+\tau}=Ky^P_t+n$, where $n\sim\mathcal N(0,\mathrm{diag}(\nu_i))$;
- effort is bounded, $\sum_i(K\Sigma_PK^\top)_{ii}\le P$;
- the partner's detector is channel-matched, like the agent's own.

Then the $K$ maximizing $\sum_i I(y^P_i;y^A_i)$ is diagonal, so the agent copies on the same channel. Its gains are water-filled: $K_{ii}^2s_i=(\mu-\nu_i)^+$.

*Proof idea.* An off-diagonal entry adds variance that counts as noise in channel $i$'s detector and is detected nowhere else, so zeroing it helps at equal cost. What remains is to maximize $\sum\tfrac12\log(1+p_i/\nu_i)$ under a power budget, and KKT gives water-filling.

*Corollaries.* Channels with motor noise above the water level are never mimicked. Mimicry grows with $P$ and $\kappa_P$. Under a full-matrix detector the optimum is not unique, so mimicry signals a shared body map.

**Toy still-face simulation, predictions fixed now.**

Setup:
- Model: the 1-D reduction. $c^*=0.7$ and $\tau_c=5$ min. A Beta posterior over the partner's response probability $q$. Bid rate $0.5\,\sigma(\lambda(\mathbb E[q]\,\partial_cD-k))$ per second. Mimicry gain $\propto\kappa_P$. Distress reflex at $D>\theta$.
- Protocol: Ekas et al. 2012, with 3 min play, 2 min still face and 3 min reunion. $q=0.8$ in play and $q=0$ in still face. 20 seeds per cell.
- Partners: familiar, with prior Beta(160, 40) and $\kappa=0.8$; stranger, with Beta(1.2, 2.8) and $\kappa=0.1$.

Predictions:
1. In the still face, the bid rate in the last 30 s is at most 0.5 times the rate in the first 30 s, for both partners.
2. Still-face bids with the familiar partner are at least 2 times those with the stranger.
3. The drop in positive expression from play to still face is at least 1.5 times larger with the familiar partner. The human ratio for parent versus stranger is 1.01/0.57 ≈ 1.8 (Mesman et al. 2009).
4. In the reunion, positive expression reaches at least 80% of its play level within 60 s, while distress occupancy stays above its play level for all 3 min. Humans show this split: positive affect recovers, negative does not (d = 0.04).
5. Ablation: if $c$ is replaced by partner presence, still-face distress occupancy is at most 1% and the within-still-face bid decline is gone.

## What is new

- **Active inference.** The social need is directed information received, not preferred observations. Curiosity is dual-control value of information and vanishes at satiation. Self and other come from the contingency spectrum, not hand-made factors.
- **Homeostatic RL (Yoshida & Man).** Their fixed $w=0.5$ becomes $\kappa_P$, learned from contingency history: a formal, operator-specific attachment variable. Mimicry is derived, with a predicted per-AU gain profile, and echo removal makes the dyad well-posed.
- **BabyX.** Named circuit variables, against one objective here, from which the still-face carry-over follows.
- **Data-driven avatars.** They copy mimicry statistics. This core predicts which AUs are mimicked, that mimicry scales with partner history, and the still-face pattern, which a model without a need cannot produce.

## Biggest risk

Contingency is sign-blind, so provocation harvests it: teasing reliably gets an answer. The only check is $\kappa_PD(\hat b^P)$, and that holds only if inverting the agent's own AU body map reads a human's distress correctly; the like-me assumption may fail across bodies this different. Next, transfer entropy from minutes of noisy AU data may stay biased even after the surrogate is subtracted. Last, emotion categories in $h$ are asserted, not shown, and $\phi$ may move Claude as little as numbers did in P1.
