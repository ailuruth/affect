# Sun, Li, Dalal et al. 2024: Learning to (Learn at Test Time): RNNs with Expressive Hidden States

Citation: Y. Sun, X. Li, K. Dalal, J. Xu, A. Vikram, G. Zhang, Y. Dubois, X. Chen, X. Wang, S. Koyejo, T. Hashimoto, C. Guestrin. arXiv:2407.04620v4 (31 Aug 2025; first version 5 Jul 2024). Code in JAX and PyTorch.

Source read: the arXiv v4 PDF via text extraction. Main text read in full: section 1, section 2 (2.1-2.7, including Theorems 1-2 and Table 1), section 3 (3.1-3.3), section 4 (related work, including fast weights and modern RNN layers) and section 5. Appendices A (dual form for nonlinear f), B (Nadaraya-Watson) and C (experiment details) were not read. Plots were read only through captions and text. DeltaNet, Titans and Irie et al. were not read here; the project's critique-fast-weights.md read Titans §2-3.1.

## The failure or bottleneck it answered
- The measured bottleneck is long-context use by fixed-size recurrent states: "Tokens later in a sequence should be easier to predict on average ... This is indeed the case for Transformer ... In contrast, the same metric plateaus for Mamba after 16k." The same failure had been reported for LSTMs by Kaplan et al. 2020.
- The diagnosis: "RNN layers have to compress context into a hidden state of fixed size", so "the performance of RNN layers in long context is limited by the expressive power of its hidden state". Self-attention avoids it by keeping the whole KV cache, at a per-token cost that grows with t.
- The proposed fix is a better compression heuristic, borrowed from training itself: "self-supervised learning can compress a massive training set into the weights of a model".
- Measured: at 8k context on the Pile and at 32k on Books, TTT-Linear and TTT-MLP (Mamba backbone) beat Mamba at matched FLOPs, and "as context length grows longer, the advantage of TTT layers over Mamba widens." At 2k they are comparable. Table 1 (125M parameters) walks from linear attention (perplexity 15.91) to TTT-Linear (11.09); the largest single gains are mini-batch TTT (−1.70) and LayerNorm plus residual inside f (−1.22).
- Stated limitation: TTT-MLP "still faces challenges in memory I/O", and wall-clock cost "can still require substantial wall-clock time".

## The new computation, in one equation
The hidden state is the weight W of an inner model f, and the update rule is one gradient step on a self-supervised loss whose views are learned in the outer loop (Eqs. 2, 4, 5):

  W_t = W_{t−1} − η(x_t) ∇_W ‖ f(θ_K x_t; W) − θ_V x_t ‖² |_{W = W_{t′}},  z_t = f(θ_Q x_t; W_t),

with η(x) = η_base σ(θ_lr · x), t′ the last step of the previous mini-batch of b = 16 tokens, and θ_K, θ_V, θ_Q, θ_lr, W_0 trained by next-token prediction through the inner updates.

What is computed is a per-sequence *learning trajectory*: the state at time t is the result of t steps of training on the sequence so far, so "W remembers inputs that produce large gradients". The update rule is specified by a loss (what the state should be able to reconstruct), not by a hand-written recurrence, and the outer loop chooses which loss.

## New computation or recombination?
Parts, each with its prior, several stated by the paper itself:
1. Fast weights updated on the most relevant data, and fast-weight programmers with slow weights writing fast ones (1980s-1992; Schmidhuber; Ba et al.): "TTT can be viewed as a special case of fast weights" and networks with TTT layers "a special case of FWPs".
2. The delta rule: "DeltaNet [62], which is equivalent to TTT-Linear with inner-loop mini-batch size 1, without the Layer Norm and residual connection."
3. Linear attention: Theorem 1, "the TTT layer with f(x) = W x ..., batch gradient descent with η = 1/2 ..., and W_0 = 0" produces "the same output sequence ... as linear attention."
4. Softmax self-attention: Theorem 2, the TTT layer with a Nadaraya-Watson learner "produces the same output sequence ... as self-attention."
5. An MLP as fast weights: "one instantiation in Irie et al. [38] makes the fast weights an MLP, preceding our TTT-MLP."
6. Test-time training on one instance (Sun et al. 2020), dynamic evaluation, local learning (Bottou & Vapnik).
7. A data-dependent learning rate as a gate: "η(x) can also be interpreted as a gate for ∇ℓ" (the same as Titans' θ_t).
8. Bi-level optimization and learning to learn (MAML-type "gradients of gradients").
9. Mini-batch gradient descent and the dual form: systems choices for parallel hardware.

By the project's test this is a **recombination**, and the paper says so: "The idea of using linear models as hidden states has already been well studied in DeltaNet", and its contribution is "a practical framework that can instantiate arbitrary neural networks as hidden states." The Titans-style gated gradient write, which the project's critique-fast-weights.md already judged a recombination, is the same family. What the framing adds is a *language*: any learner (model plus optimizer, parametric or not) induces a sequence layer, and one picks the layer by picking the self-supervised task. Table 1 shows the one place where this language changed the computation in practice: going from batch GD (linear attention, a cumsum of outer products) to mini-batch GD with a nonlinear f makes the state's update depend on its own current predictions, which a cumsum cannot do.

## What it suggests for an affective core
- **The dial is present.** η(x) is a gate: at η → 0 the state never adapts to the partner (flat), at large η it is dominated by the latest tokens. If x is the partner stream and the loss reconstructs partner features, the inner model becomes a predictor of the partner, and if expression is read from that model, the agent is a delayed, smoothed copy, set by one gain. This is the fast-weights critique's result again.
- **What TTT offers instead of a gain is a choice of loss.** The three views are matrices, not scalars: θ_K decides what of the input enters as the training input, θ_V what is used as the label, θ_Q what is read out. A partner stream used only in the training view, with the label view drawn from the agent's own body and need variables, makes the inner learner learn "what my own body does next given this partner pattern", not "what the partner does next". Partner influence is then the content of a learned mapping, so it can change shape with the situation instead of scaling. The project's test classes a choice of what is stored or keyed as not new, so this is a design choice inside a known mechanism, not a new mechanism.
- **The state as a learner has a native notion of surprise and of learning progress.** ℓ(W_{t−1}; x_t) against ℓ(W_t; x_t) (their Fig. 4) is a per-step learning-progress signal (Oudeyer's IAC, already adopted as a definition in this project), computed for free. It could feed curiosity, but it inherits the noisy-TV problem.
- **Two-level learning matches the project's time scales.** The inner loop (within a conversation) and the outer loop (across conversations, choosing what the inner loop learns) give a principled split between "what changes with this partner today" and "what kind of things I learn from partners". The outer loop is where the agent's temperament would live.
- **The non-parametric limit is attention.** By Theorem 2, a TTT layer whose learner keeps all data and reads with a softmax kernel is self-attention. So moving the core to TTT does not escape the retrieval-sharpness dial unless the learner is parametric and compressive.

## Verdict: watch (recombination by the paper's own theorems; the "pick the loss, not the recurrence" framing is useful vocabulary)
The authors prove the equivalences to linear attention and self-attention and name DeltaNet as TTT-Linear with b = 1. It is the fast-weights family the project has already set aside as recombination. The usable idea is that partner influence can be carried by which subspaces form the training input, the label and the readout of an inner learner, matrices fixed by an outer loop, rather than by one write gain; η remains a gain and must not be the only route by which the partner enters.
