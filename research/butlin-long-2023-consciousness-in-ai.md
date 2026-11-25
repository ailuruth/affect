# Butlin, Long, Elmoznino, Bengio, Birch, Constant, Deane, Fleming, Frith, Ji, Kanai, Klein, Lindsay, Michel, Mudrik, Peters, Schwitzgebel, Simon & VanRullen 2023, "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness" (arXiv 2308.08708v3, 22 Aug 2023)

Source read: the full PDF. Read verbatim: the executive summary, Table 1, §1.2 (methods, including the passage on behavioural tests), and the §4 passage on valence. Section 2 (per-theory arguments) and §3.2 (case studies) were skimmed.

## Claims
- Method: "computational functionalism ... as a working hypothesis" and a "theory-heavy approach". "AI systems which possess more of the indicator properties are more likely to be conscious." Credences combine "(a) the similarity of the functions, (b) the strength of the evidence for the theories in question, and (c) one's credence in computational functionalism." IIT is excluded as incompatible with computational functionalism.
- Indicator properties (Table 1, verbatim):
  - RPT-1: "Input modules using algorithmic recurrence"
  - RPT-2: "Input modules generating organised, integrated perceptual representations"
  - GWT-1: "Multiple specialised systems capable of operating in parallel (modules)"
  - GWT-2: "Limited capacity workspace, entailing a bottleneck in information flow and a selective attention mechanism"
  - GWT-3: "Global broadcast: availability of information in the workspace to all modules"
  - GWT-4: "State-dependent attention, giving rise to the capacity to use the workspace to query modules in succession to perform complex tasks"
  - HOT-1: "Generative, top-down or noisy perception modules"
  - HOT-2: "Metacognitive monitoring distinguishing reliable perceptual representations from noise"
  - HOT-3: "Agency guided by a general belief-formation and action selection system, and a strong disposition to update beliefs in accordance with the outputs of metacognitive monitoring"
  - HOT-4: "Sparse and smooth coding generating a 'quality space'"
  - AST-1: "A predictive model representing and enabling control over the current state of attention"
  - PP-1: "Input modules using predictive coding"
  - AE-1: "Agency: Learning from feedback and selecting outputs so as to pursue goals, especially where this involves flexible responsiveness to competing goals"
  - AE-2: "Embodiment: Modeling output-input contingencies, including some systematic effects, and using this model in perception or control"
- No scoring threshold is given. The assessment is qualitative, property by property. "no current system appears to be a strong candidate for consciousness."
- Behavioural tests are distrusted because systems "may be trained to mimic human behaviour while working in very different ways, thus 'gaming' behavioural tests (Andrews & Birch 2023)."
- Valence is out of scope: "We have not discussed neuroscientific or philosophical theories of valence or otherwise investigated the prospects of specifically valenced conscious experience in AI systems."

## Evidence
A conceptual survey of theories, with architecture case studies: Transformers, Perceiver, Adaptive Agent, a virtual rodent, PaLM-E. There are no experiments.

## License
arXiv, CC BY-NC-SA 4.0.

## Runs on this Mac without a GPU?
n.a. It is a checklist applied to an architecture.

## Verdict: watch
It is an architecture audit, not a test with scoring rules. It also says nothing about felt valence, which is the project's question. It is useful in two ways:
1. It is a published list for stating which indicators the engine's design has, and does not have, by construction. This is answered from the formal core, not from behavior.
2. Its rejection of behavioural tests agrees with Birch on gaming.

Failure, if used: an indicator claimed from the agent's text output rather than from the architecture. Another failure is a "more indicators, so more likely conscious" claim that ignores credence in computational functionalism, which the authors require. It cannot support any stage claim alone; at most it is provisional.
