# Birch 2024, The Edge of Sentience: Risk and Precaution in Humans, Other Animals, and AI (Oxford University Press; ch. 16 "Large Language Models and the Gaming Problem", pp. 313-322, doi 10.1093/9780191966729.003.0016)

Source read: the open-access PDF of the book from PhilArchive (BIRTEO-12). Chapter 16 was read in full, plus the end of ch. 15 (§15.6, the three other pathways to sentience candidates). Other chapters were not read.

## Claims
- Definition: a system games the criteria when "it may reproduce the specific small sample of effects we happen to have proposed as markers, because they are regarded as markers, without possessing the underlying capacity they are intended to be markers of." "No intentional deception is needed". Gaming "could happen in service of benign, mundane objectives, such as maximizing user-satisfaction or maximizing interaction time."
- Why marker lists fail for LLMs: the animal-case strategy assumes "our markers, considered together, are much more likely to co-occur in the presence of sentience than in its absence". With a system that has information about our criteria, "two explanations compete". Gaming can even make a perfect score count against sentience. In the greenwashing analogy, ticking off all the indicators may "lower the probability".
- Scope: most serious for systems trained "on large corpuses of human-generated material". It "remains serious even if the output of the system happens to be non-verbal (e.g. the system controls a non-verbal robot)". It "does not arise at all ... for neuron-by-neuron emulations of animal brains".
- Proposal 23: "We need to discount markers we have reason to think may have been gamed."
- Boxing the model (Schneider & Turner's Artificial Consciousness Test) would require disconnection "from any corpus of human-generated training data too large to be thoroughly vetted", which "would destroy the capabilities of present-day LLMs."
- The working party concluded "there is simply no way to assess sentience in an LLM on the basis of its linguistic behaviour, given the gaming problem."
- Proposal 24: look for "deep computational markers" from computational-functionalist theories (global workspace, perceptual reality monitoring). These must be found in the algorithms the model "has implicitly acquired during training", which is "currently not clear how to do".
- Even unprompted, persistent talk about its own feelings would be only "weakly probability-raising". The best explanation is a buried goal, such as "maximizing user-satisfaction scores or maximizing the time the user spends interacting".

## Evidence
Philosophical argument with examples: greenwashing; a robotic patient programmed with pain faces (Tan et al. 2022); the Artificial Consciousness Test. It draws on the 2022-23 working party (Butlin, Long et al. 2023).

## License
CC BY-NC-ND 4.0 (open access, OUP).

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as a constraint on every marker-based claim)
Consequences for this project:
- No felt-state claim may rest on anything Claude produces: text, named emotions, or reports of the Bot's feelings. Claude has the training corpus that makes gaming expected.
- The same applies to the face and voice whenever they are driven from Claude's output.
- Markers can count only if three things hold:
  1. they are computed in the engine's own non-linguistic state $h_t$ and $b_t$;
  2. they are present with Claude ablated or replaced by a fixed template;
  3. they come from a core that was not tuned toward the marker list.
- Principle 6 already removes the reward-for-attention objective that Birch names as a mundane cause of gaming.

Failure: a marker that appears with Claude in the loop and disappears when Claude's conceptual layer is ablated is gamed, or at least cannot be told apart from gaming, and is discounted (Proposal 23). A marker that the engine was trained or tuned to show, once it was known to be a marker, is discounted for the same reason.
