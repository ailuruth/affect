# A survey on proactive dialogue systems: problems, methods, and prospects (Deng et al.)

Yang Deng, Wenqiang Lei, Wai Lam & Tat-Seng Chua, IJCAI 2023 survey track, arXiv:2305.02750v2.

## What was read
The full arXiv text (8 pp.): introduction, the three dialogue types with problem definitions, methods, datasets and evaluation, challenges and prospects, conclusion. References skimmed.

## Claims
- **Definition:** proactivity is "the capability to create or control the conversation by taking the initiative and anticipating the impacts on themselves or human users, rather than only passively responding". Derived from organisational-behaviour proactivity (Grant & Ashford 2008).
- **Three families**, all of which lead the *content* of a turn the system already owes:
  - open-domain: *target-guided* dialogue (steer topics toward a target keyword or entity hidden from the user; subtasks topic-shift detection, topic planning, topic-aware generation; metrics success rate at turn t and turns-to-target) and *prosocial* dialogue (detect a problematic utterance, generate a rule of thumb, answer prosocially);
  - task-oriented: *non-collaborative* (negotiation, persuasion; strategy learning, user personality modelling, persuasive generation) and *enriched* (add unrequested useful information or chit-chat);
  - information-seeking: *clarification questions* (predict need, then ask) and *preference elicitation* ("System Ask, User Respond", often multi-turn RL).
- **The trigger is always a system goal** (a target, a price, a donation, an ambiguity, a missing preference), never the system's own state or the user's silence.
- **Open problems named:** hybrid dialogues with changing goals; evaluation, which "involves the evaluation not only from the perspective of natural language, but also from ... human-computer interaction, sociology, psychology"; ethics, with three items: factuality, **aggressiveness** in non-collaborative settings, and **privacy**, since "the agent's proactivity raises more concerns on misusing personal information obtained from the users".

## Evidence with numbers
A survey; the only numbers are dataset sizes (e.g. ProsocialDialog 58K dialogues, P4G 1,017, ESConv is not covered). No result on timing, turn-taking or silence.

## What it means for the designs
1. **The literature's "proactive" is not the gap the critique names.** Every surveyed system speaks only when a turn is owed and chooses what to say. None decides *whether to speak at all* during a silence, none starts a turn, and none takes initiative from an internal affective state. Initiative from the agent's concern has no ready-made method here; it has to be designed from the conversation-timing and support literature.
2. **Goal-driven proactivity is the wrong model for this agent.** Target-guided and persuasive systems are scored on steering the user toward the system's target in few turns. An agent whose initiative is scored that way would learn exactly the "elicit a response" pressure Knox et al. warn against. The agent's initiative should be scored on its own drive (does the bid follow from its concern, is it bounded, one per silence), never on whether the user responded.
3. **Clarification-need prediction is the closest usable piece.** It separates *whether* to initiate (a binary need predictor) from *what* to say (generation). The same split fits here: the body computes the binary "take the floor" decision from silence type and its own concern; Claude writes the bid only after that decision.
4. **Privacy is an initiative-specific risk.** A bid such as "you've looked sad since ten" uses inferred state about the user; proactivity makes such inferences audible. Initiative content should name what the agent noticed in the moment (the silence, a sigh) rather than its longer-term inferences, unless the user has already talked about them.

## Verdict
**watch (map of a neighbouring field):** useful as evidence of absence; no surveyed method starts a turn in silence or from the agent's own state, and the goal-steering objectives are what the agent should avoid. The need/act split from clarification work is worth copying.
