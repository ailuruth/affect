# Park, O'Brien, Cai, Morris, Liang & Bernstein 2023: Generative Agents: Interactive Simulacra of Human Behavior

## Citation

J. S. Park, J. C. O'Brien, C. J. Cai, M. R. Morris, P. Liang, M. S. Bernstein. "Generative Agents: Interactive Simulacra of Human Behavior." UIST '23, San Francisco, 29 Oct - 1 Nov 2023. arXiv 2304.03442. Code: github.com/joonspk-research/generative_agents.

## What was read

PDF from arXiv, text extracted with pdftotext.
- Read in full: abstract; section 1 (introduction); 4 (architecture overview); 4.1 (memory and retrieval); 4.2 (reflection, first half); 6.1-6.5 (controlled evaluation: interview design, conditions, evaluators, analysis, results); 8.2 (future work and limitations).
- Skimmed: section 3 (Smallville sandbox), 4.3 (planning), 7 (end-to-end evaluation, headings and first paragraphs).
- Not read: related work, appendices (full question list, sample responses), ethics section beyond the introduction's summary.

Why this source: it is the standard primary reference for the black-box pattern "a scoring function outside the LLM decides which verbatim past records enter the prompt". It is the closest published form of the project's "retrieval of verbatim episodic snippets chosen by state".

## Mechanism

- **Memory stream.** A list of records. Each has "a natural language description, a creation timestamp, and a most recent access timestamp" (4.1). Records are observations, reflections and plans.
- **Retrieval score** (4.1), with each term min-max scaled to [0, 1]:

      score = α_recency · recency + α_importance · importance + α_relevance · relevance,   all α = 1

  - recency: exponential decay over sandbox game hours since last access, factor 0.995 per hour;
  - importance: an integer 1-10 that the LLM itself assigns when the record is written ("cleaning up the room" → 2, "asking your crush out on a date" → 8);
  - relevance: cosine similarity between the record's embedding and the embedding of a query describing the current situation.
  - "The top-ranked memories that fit within the language model's context window are included in the prompt."
- **Reflection** (4.2): when the summed importance of recent events passes 150 (about 2-3 times a game day), the LLM is asked for salient questions over the last 100 records, retrieves for each, and writes "insights" with citations back into the stream.
- The LLM was gpt-3.5-turbo, used only through prompts. No weights, logits or activations: the whole architecture is black-box.

## Evidence

- Controlled evaluation (6.1-6.5): 25 agents after two game days; 5 interview categories (self-knowledge, memory, plans, reactions, reflections), 5 questions each; 100 Prolific raters each rank 5 conditions by believability for one agent; ranks converted to TrueSkill.
- TrueSkill μ (σ): full architecture 29.89 (0.72); no reflection 26.88 (0.69); no reflection, no planning 25.64 (0.68); human crowdworkers 22.95 (0.69); no memory, no reflection, no planning 21.21 (0.70). Full vs no-memory: "Cohen's d = 8.16". Kruskal-Wallis H(4) = 150.29, p < 0.001; all pairwise Dunn tests significant except crowdworker vs fully ablated.
- Ablations remove whole memory types. They do **not** ablate the retrieval score's terms (recency, importance, relevance) separately, so the paper gives no evidence on which term matters.
- Ablated conditions "were given equivalent access to all memories accrued" up to the interview; the authors call the differences "a conservative estimate".
- Failure modes (6.5.2): retrieval misses ("I haven't been following the election too closely" though the agent had heard of it), incomplete fragments, and embellishment ("he's going to make an announcement tomorrow").
- Limitation (8.2): the retrieval functions are hand-set; "memory hacking" is flagged as a risk.

## Available through `claude -p` / Agent SDK?

Yes, entirely. Retrieval runs outside Claude; the selected records are placed in the prompt, a hook's `additionalContext`, or an earlier turn of a resumed session. Nothing in the method needs anything beyond text in, text out.

## What it implies for the interface theory

- **The coupling lives in the scoring function, not in Claude.** Replace "relevance to the current situation" with a state-dependent query (the agent's current needs and body, as in efference-memory.md §2.5) and the state decides which past episodes Claude sees. Claude reads only verbatim episodes. It is never told the state. This is the brief's "need-conditioned attention" applied to memory, and it is admissible under Principle 4 if the records are verbatim and carry no affect labels.
- **What this source does not show.** Its effect (d = 8.16) is for memory vs no memory, a content effect. It does not show that *state-dependent* choice of memories changes behavior beyond relevance-based choice. That is the comparison the project needs: same memory store, retrieval query from the state vs from the text alone, vs a shuffled state (a sham).
- **Text-channel risk, three ways.**
  1. Records written by the LLM in natural language, as here, contain descriptions ("Klaus is passionate about research"). If the engine stores Claude's own summaries, labels re-enter through memory. Store verbatim transcript spans and feature-stream pointers, not summaries.
  2. The LLM-assigned importance score is an affect judgment by the language layer. If importance then feeds retrieval, Claude's labels steer what Claude later sees. For this project, importance must come from the engine (for example, the arousal-like signal at encoding, research/mcgaugh-2004-amygdala-modulates-consolidation.md), not from Claude.
  3. Selection is a channel even without labels. If the engine always shows "sad" episodes when its state is low, Claude can infer the state from the pattern. That is mood-congruent recall, which is what the brief wants: the state shapes what comes to mind. But it means the coupling is an implicit text channel of bounded capacity (choosing k of M records carries at most log2 C(M, k) bits per turn), not a non-textual one. The honest description is "the state reaches Claude only as which of its own past words and the user's words it is reminded of".
- **Reflections are the grounding problem in miniature.** The reflection step is Claude naming a cluster of records. In this project the cluster should come from the engine's latent state (episodes that share a state), and Claude names it. That inverts the paper's flow, where the LLM both clusters and names.

## Verdict

Adopt the retrieval pattern as the context-selection channel, with three changes: the query comes from the engine's state, importance comes from the engine (not from Claude), and records are verbatim. Watch the evidence: the paper never isolates the retrieval score's terms, so it cannot say whether state-weighted retrieval does anything beyond relevance.
