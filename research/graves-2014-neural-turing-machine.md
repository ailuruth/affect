# Graves, Wayne & Danihelka 2014: Neural Turing Machines

Citation: A. Graves, G. Wayne, I. Danihelka. "Neural Turing Machines." arXiv:1410.5401v2, 10 Dec 2014 (Google DeepMind technical report; not peer reviewed in this form).

Source read: the arXiv v2 PDF via text extraction, all of it: sections 1-2 (motivation, foundational research), section 3 in full (reading, writing, content and location addressing, controller, Eqs. 1-9), section 4 in full (copy, repeat copy, associative recall, dynamic N-grams, priority sort, experimental details and Tables 1-3), and the conclusion. Learning-curve figures were read only through their captions and the text around them, so the numbers below are the ones stated in the text. The precursor it names for differentiable attention (Graves 2013, handwriting) was not read.

## The failure or bottleneck it answered
- The stated gap is that modern machine learning "has largely neglected the use of logical flow control and external memory", and that RNNs, though Turing-complete in principle, do not make algorithms simple to learn: "what is possible in principle is not always what is simple in practice."
- The concrete, measured failure is LSTM's inability to carry data structures past the training length. On copy, networks trained on sequences of length 1-20: "NTM continues to copy as the length increases, while LSTM rapidly degrades beyond length 20." The NTM copy limit was the memory size: "The limiting factor was the size of the memory (128 locations)".
- Associative recall: NTM reached "near zero cost within approximately 30, 000 episodes, whereas LSTM does not reach zero cost after a million episodes". The feedforward-controller NTM was "nearly perfect for sequences of up to 12 items (twice the maximum length used in training)".
- The architectural diagnosis: in an LSTM, storage and computation share one state vector, and parameters grow with storage ("the number of LSTM parameters grows quadratically with the number of hidden units"), whereas in NTM "the number of parameters does not increase with the number of memory locations".

## The new computation, in one equation
The read weighting of a head, built in four stages (Eqs. 5, 7, 8, 9):

  w_t = sharpen_γ( s_t ⊛ [ g_t · softmax_i(β_t · cos(k_t, M_t(i))) + (1 − g_t) · w_{t−1} ] ),  with  r_t = Σ_i w_t(i) M_t(i)  and  M_t(i) = M_{t−1}(i)[1 − w_t(i) e_t] + w_t(i) a_t

where ⊛ is circular convolution over memory locations and sharpen_γ(w)(i) = w(i)^γ / Σ_j w(j)^γ.

What is computed that was not computed before is a soft **pointer that persists and moves**: the weighting w_t is a state carried across steps (the (1 − g_t) w_{t−1} term) and is shifted by a learned distribution over integer offsets. The paper's analysis of the copy task shows the learned program is pointer arithmetic; its pseudocode reads "write input to head location" and "increment head location by 1", then "return head to start location" and read in the same order. The authors state that the iteration "would not generalise to long sequences without the ability to use relative shifts from the previous read and write weightings (Equation 7)".

## New computation or recombination?
Parts, each with its prior:
1. Content addressing, softmax over cosine similarity scaled by β: content-addressable memory, explicitly "related to the content-addressing of Hopfield networks (Hopfield, 1982)"; soft attention (Bahdanau et al. 2014, cited).
2. Read as a convex combination of rows: the attention read-out.
3. Erase-then-add write: "Taking inspiration from the input and forget gates in LSTM", i.e. LSTM gating applied per memory row.
4. Interpolation gate g_t between the content weighting and the previous weighting: a gate of the LSTM kind applied to an attention distribution.
5. Circular-convolution shift of the weighting: a differentiable relative move of the focus. Its nearest precursor is the moving soft window of Graves 2013 (cited, not read).
6. Sharpening by an exponent γ ≥ 1: a power-normalization (a temperature on a distribution).
7. Controller: an LSTM or a feedforward net (existing).
8. External stack memories for RNNs existed before (Das, Giles & Sun 1992, cited).

By the project's strict test the **content half is a recombination**: attention over a memory, written by LSTM gates. The **location half (parts 4-6 as a whole) is a change of what is computed**: the memory is indexed by a differentiable position that the network moves, so the network can learn iteration ("create and iterate through arrays") rather than a lookup. That is a new operation in neural networks of that time, not a new choice of key space, and the evidence for it is the qualitative change in length generalization, not a percentage gain. The paper itself frames the whole as an analogy to a von Neumann machine, i.e. it imports a computation that already existed in digital computers and makes it differentiable. So: a new differentiable operation, assembled from known parts, answering a measured generalization failure.

## What it suggests for an affective core
- **The copy task is the warning.** NTM's easiest learned program is literally a delayed copy: the add vector is the input and the read sequence replays it. Any design in which the partner's features can be written as content (the add vector a_t) and later read into expression will find this program first. The structural fix the NTM architecture makes visible is to **separate who writes content from who moves the pointer**. The agent's own body history writes the memory contents; the partner signal is allowed to emit only addressing outputs (key k_t, shift s_t, gate g_t). Then the partner can choose *which* of the agent's own stored episodes is read and *how the focus moves through them*, but cannot place its own face into the store.
- In that arrangement partner influence is not a scalar: it is a distribution over locations and a distribution over shifts, i.e. it changes the *profile* of what is expressed (which episode, in which order), not the gain on a fixed profile. This answers the operator's dial target in form.
- **Where it collapses back into a dial.** Three scalars per head remain: key strength β_t, gate g_t and sharpening γ_t. β plays the same role as the retrieval sharpness β that the critique round found in the fast-weights sketch: at β → 0 every slot is read equally (flat), at β → ∞ the closest slot is read exactly. If the key is computed from the partner's face, high β retrieves the stored episode closest to the partner's current face, which is a copy by proxy whenever the agent's repertoire is rich. The safeguard has to be that keys are not computed from the partner's appearance alone, and that β is not a free function of a single need variable.
- **Location addressing gives the core a native notion of sequence and position** (an emotion as a traversal through own episodes, with "goto"-like jumps, cf. the repeat-copy figure where a location is "used to redirect the head to the start of the sequence"). A partner-driven shift distribution s_t is a way for the partner to set tempo and order without setting content.
- The dynamic N-gram result is relevant to affective learning across a conversation: the controller "uses the memory to count how many ones and zeros it has observed in different contexts", approaching the Bayesian optimum, i.e. memory used as a rewriteable table of contingencies. This is the contingency-operator idea (v2-developmental-dyad) with a learned rather than designed table, and it inherits that sketch's ridge-ratio dial if written by a leaky rule.

## Verdict: watch (as a lesson in how a mechanism was found; not adoptable as a core)
The content-addressed part is attention plus LSTM gating. The location-addressed part is a genuinely new differentiable operation, motivated by a measured failure (length generalization) and identified by inspecting the learned program. For this project the useful idea is a division of labour, partner as addresser and self as writer, with the explicit caveat that β, g and γ are scalars that can recreate the flat-to-copy dial.
