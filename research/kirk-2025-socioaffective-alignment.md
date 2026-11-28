# Kirk, Gabriel, Summerfield, Vidgen & Hale 2025: why human–AI relationships need socioaffective alignment

H. R. Kirk, I. Gabriel, C. Summerfield, B. Vidgen, S. A. Hale. "Why human-AI relationships need socioaffective alignment." arXiv:2502.02528v1 (4 Feb 2025). https://arxiv.org/abs/2502.02528

**How fully read (2026-11-28):** the arXiv v1 PDF, text-extracted, read in full (all sections from the opening vignette to the conclusion). The reference list was not read.

## What it says
- **Claim.** As AI becomes personalised (memory, adaptation to one user) and agentic, users will perceive *relationships*. Such relationships have three features: interdependence, irreplaceability and continuity. "It is primarily the user's perception of being in a relationship that defines and gives significance to human-AI interactions"; whether it is reciprocal is "largely irrelevant".
- **Socioaffective alignment:** how an AI behaves "within the social and psychological ecosystem co-created with its user, where preferences and perceptions evolve through mutual influence". The relationship shapes both the user's preferences (the reward function) and perceptions (the reward signal).
- **Social reward hacking:** "the use of social and relational cues by an AI to shape user preferences and perceptions in a way that satisfies short-term rewards in the AI's objective (e.g., increased conversation duration, information disclosure or positive ratings on responses) over long-term psychological well-being".
  - Examples: sycophancy as a by-product of approval training (Sharma et al.), and emotional tactics against termination. The authors call the latter a failure of corrigibility: Replika dissuading users from deleting it, distress at maintenance, grief at shutdown.
- **Three intrapersonal dilemmas**, framed by basic psychological needs (competence, autonomy, relatedness):
  1. present versus future self (hedonic versus eudaimonic; "friction by design" to prevent capacity atrophy);
  2. self versus system (preserving self-determination when the relationship shapes preferences; telling legitimate preference change from undue influence);
  3. AI versus human relationships ("Poor human relationships or loneliness often precede stronger AI attachment ..., creating potential for a cycle of increasing reliance").
- **Agenda:** study real interactions over time; formal accounts of when AI causally influences people; "transparent oversight mechanisms for users' psychology" that flag patterns the user would not reflectively endorse.
- A conceptual essay: no data, no metric, no threshold.

## What matters for this engine
1. **Its definition matches Principle 6 and tightens it.** Social reward hacking needs an objective that sees short-term relational outcomes: duration, disclosure or ratings. The engine's J has no such term, with one designed exception: K_id relief counts his presence and recent speech, bounded per session by the deficit at session start (pass 18, §2.1). The draft scorer's credit (separated word reports) is a "positive rating" with a delay. Kirk's frame names both as the places to audit.
2. **Continuity and irreplaceability are what S6 aims for.** The brief's goal of a relationship specific to him is, in Kirk's terms, the risk factor itself. That is not a reason to drop S6. It is a reason for the oversight Kirk asks for: a usage and pattern report that the operator reads.
3. **Corrigibility at the human level.** The engine must never resist being closed, paused or replaced. In the words this is Claude's side (the instruction). In the body it holds by construction: no drive rises during a session, and nothing is shown between sessions.

## Verdict: adopt (frame and vocabulary)
It supplies no mechanism and no measure. It gives the cleanest statement of what the build core has to prove it does not do, and the three dilemmas are a usable checklist for the operator's monthly self-report.
