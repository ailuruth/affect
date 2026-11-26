# Deep variational information bottleneck (Alemi, Fischer, Dillon & Murphy)

Alexander A. Alemi, Ian Fischer, Joshua V. Dillon & Kevin Murphy, *ICLR 2017*; arXiv:1612.00410v7 (23 Oct 2019).

## What was read
The arXiv v7 PDF from export.arxiv.org, in full: §1–3 (objective and variational bound), §4.1 (MNIST; K = 256 and K = 2 embeddings), §4.2 (adversarial robustness on MNIST and ImageNet), future directions, Appendix A (hyperparameters) and Appendix B (the unsupervised version and its relation to VAEs). Appendix C (approximate quadratic form) was skimmed. Figures were seen as captions and extracted text.

## The computation, precisely

**Objective (Eqs. 2–3).** Learn a stochastic encoder $p(z\mid x;\theta)$ that solves
$$\max_\theta I(Z;Y) \quad\text{s.t.}\quad I(X;Z) \le I_c,$$
or equivalently maximises $R_{IB} = I(Z;Y) - \beta I(Z;X)$. Here Y is the target, under the Markov chain $Y \leftrightarrow X \leftrightarrow Z$ (Eq. 5: Z may not read Y directly). Large β means heavy compression.

**Variational bounds.**
- A decoder $q(y\mid z)$ gives the lower bound $I(Z;Y) \ge \int p(x)p(y\mid x)p(z\mid x)\log q(y\mid z) + H(Y)$ (Eq. 12).
- A fixed "marginal" $r(z)$ gives the upper bound $I(Z;X) \le \int p(x)p(z\mid x)\log\frac{p(z\mid x)}{r(z)}$ (Eq. 14).

The loss is (Eq. 17)
$$J_{IB} = \frac1N\sum_n \mathbb E_{\epsilon}\big[-\log q(y_n\mid f(x_n,\epsilon))\big] + \beta\,\mathrm{KL}\big[p(Z\mid x_n)\,\|\, r(Z)\big].$$
It uses a Gaussian encoder $z = \mu(x) + \sigma(x)\epsilon$ (the reparameterisation trick) and $r(z) = \mathcal N(0, I)$. The KL term is an **upper bound** on the rate. Constraining it therefore constrains the true rate conservatively.

**Behaviour as β grows (MNIST, Figs. 1–2).**
- **Collapse.** "the error rate shoots up once β rises above the critical value of β ∼ 10⁻²", which "corresponds to a setting where the mutual information between X and Z is less than log₂(10) bits, so the model can no longer represent the fact that there are 10 different classes".
- **Overlap in a 2-D embedding.** "as β increases … the embedding covariances increase in relation to the distance between samples, and the classes start to overlap … once β passes a critical value, the encoding 'collapses'". At β = 10⁻¹ performance is still good "even though there is a lot of uncertainty about where any individual image will map to … it would be difficult for an outside agent to infer which particular instance the model is representing."
- **Determinism.** As β → 0, the network drives σ → 0 and becomes nearly deterministic, and it overfits.

**Numbers.**
- Permutation-invariant MNIST error: 1.13% (VIB, β = 10⁻³) against 1.38% for the baseline. Best results come at I(X;Z) of about 10–100 bits.
- ImageNet: 80.12% accuracy at β = 0.01 with I(X;Z) ≈ 45 bits, against >10,000 bits at β = 0 (78.87%).
- Adversarial robustness: under a targeted L2 attack the deterministic models always fail, while VIB resists about 43.3% of attacks. As β rises, a successful attack needs larger L2/L∞ perturbations concentrated on fewer pixels. The authors' reading: "it is more difficult to pass small, idiosyncratic perturbations through the latent bottleneck."

## What it means for the designs

VIB is the practical way to put an information cap *inside a trained network*. It is the obvious way to build the partner→agent channel, so its properties matter.

- **A learning-proof cap needs a fixed noise floor, not a β.** VIB's β is a price, and learning can always trade it, so it is a dial. To make a cap innate, fix the encoder's noise and bound its mean. For example $z = \tanh(\cdot)\cdot m + \sigma_0\epsilon$ with innate $m, \sigma_0$ gives a per-dimension, per-sample capacity ≤ ½log₂(1 + m²/σ₀²), whatever the weights. This is the "innate noisy perceptual channel" of the Tatikonda note, built with VIB's machinery. (This is my construction; the paper only uses a learned σ.)
- **Categorisation of the partner emerges as the cap tightens.** Below log₂(k) bits, k partner categories cannot all be kept, and the encoding collapses to coarser groups (Fig. 2). For a partner stream, a tight cap per window predicts that the agent reads the partner as a few overlapping states, with abrupt loss of a distinction at a critical rate.
- **Idiosyncratic detail does not get through.** The adversarial result is the network analogue of "small partner fluctuations cannot steer the agent". That works against *fine-grained* copying, such as micro-movements and exact timing. It does nothing against copying a large, slow, prototypical display, which is cheap in bits.
- **Stochasticity.** At useful β, responses to the same input are a distribution. An outside observer cannot recover the exact input from the response. That stops exact matching but leaves category-level matching.
- **Gain and sign.** As with every information quantity, the cap is invariant to rescaling and sign flips of z, and of the downstream readout. It cannot by itself bound per-channel copy *gain*, or prefer non-copying to anti-copying.
- **Copy non-attracting.** The relevance variable Y decides what is kept. If Y is "predict the partner's next face", the bottleneck keeps exactly the copy-relevant bits, so copy is attracting within the cap. If Y is the agent's own concerns (its body, its drives), partner bits are kept only insofar as they bear on those. That is the useful use: the IB places the partner's influence *behind the agent's own relevance variable*.
- **Framework.** This is the information bottleneck, an existing framework, used as a regulariser. It is not a core. It is the right *implementation primitive* for an innate rate cap, because it gives an upper-bound estimator of the rate that can be trained through.

## Verdict
**adopt as implementation.** It gives a trainable, conservative rate bound (KL to a fixed prior). A truly innate cap needs a fixed noise floor rather than a β. Behaviour under a tight cap is categorical collapse and robustness to small idiosyncratic input. Gain and sign remain uncapped.
