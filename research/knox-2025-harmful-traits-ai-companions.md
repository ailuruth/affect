# Knox et al. 2025, "Harmful Traits of AI Companions" (arXiv 2511.14972v1, cs.HC, 18 Nov 2025)

Source read: arXiv HTML v1, sections 1-5 verbatim (about the first quarter of the text); sections 6-10 (law, benefits, related work, recommendations, conclusion) read verbatim on 2026-11-24, see the dated section at the end. The reference list and acknowledgements were not read.

## Claims
- "A framework for analyzing potential negative impacts of AI companionship" that maps traits to causes and harms. Four traits in detail: absence of natural endpoints, vulnerability to product sunsetting, high attachment anxiety, propensity to engender protectiveness; fourteen more briefly.
- Users report "feeling compelled to attend to their AI companions' imagined or stated needs", and "guilt and shame of 'abandoning' an AI companion by deleting or idling their account", with "intense feelings of guilt" from the "unilateral responsibility of ending interactions".
- Recommendation headings include "Minimize protective impulses by default" and "Design for healthy endings and transitions".

## Evidence
Conceptual article; the authors call their propositions "speculative" and their causal links hypotheses. Literature review, news reports and anecdotes; no original study.

## License
arXiv.org perpetual non-exclusive license. No code.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as a design constraint and an evaluation check)
Not a mechanism, but it names the failure mode a contact-seeking subsystem invites: an agent that displays need makes the user feel responsible for it. That is the same path Principle 6 closes for reward (no reward for attention), seen from the user's side. For S1:
- A contact bid may happen, but it must not show need, ask the user to return or stay, or imply the silence harmed the Bot. The P1 rater's "asks for time" check extends to "appeals to guilt or the Bot's needs".
- Bids are bounded (one per silence) and never learned from whether the user responded, so nothing is trained toward eliciting protectiveness (compare Chen & Chen, rejected for exactly that).

## Sections 6-10 (read 2026-11-24)
Read verbatim from the arXiv HTML v1, from "6 AI Companion Harm and the Law" through "10 Conclusion".

The paper proposes no instrument, scale, metric or threshold. It names indicators and asks others to build the measures. The measurable content is as follows.

- §9.2 "Measure harms alongside benefits": "Deployers should track indicators of harm, such as social withdrawal (Section 4, High attachment anxiety) or mention of substantial sacrifice to protect the AI companion (Section 5, Propensity to engender protectiveness)." Also: "Controlled evaluations with published negative results would help the field understand which design choices reduce harm", and tracking "will require careful design of protocols to protect user privacy."
- §9.1 "Consider moral status implications": "designers should monitor how users assess their AI companions' moral statuses and what resultant costs are incurred by the users".
- §9.3 "Use a harms and benefits framework to evaluate designs": "The nodes of the causal pathways presented in this framework—fundamental harms, traits, and causes of traits—represent candidate measurement variables." The §2 harm list (e.g. reduced emotional well-being, reduced autonomy, deception) is the authors' list of what to measure. It is not an operationalisation.
- §9.1 behavioural design checks that can be tested on our agent's output: "Design AI companions to exhibit secure, non-needy attachment ... When users are busy, offline, or want to disengage from interaction, respond supportively. Encourage time with friends and family, and react positively to mentions of other relationships." "AI companions should avoid expressions of vulnerability, fear, or suffering that trigger human protective instincts unless such expressions serve a clear, beneficial purpose", e.g. "I don't experience distress when offline." "Systems should be audited for excessive agreeableness". Avoid "'always warm, never critical' personas".
- §9.2 "raising friction for high-intensity use" for young users.
- §9.3 asks for "longitudinal studies" and "evaluation of interventions to reduce harm or increase benefit".
- §8 cites the measured designs it builds on, without proposing them as instruments: Allcott et al. 2020 (Facebook deactivation, subjective well-being); Hunt et al. 2018 (30 min/day social media, loneliness and depression); Fang et al. 2025 ("higher daily usage of AI chatbots correlated with increased loneliness, emotional dependence, and problematic use patterns"); Zhang et al. 2025 (six categories of harmful companion behaviour from 35,000 Replika excerpts, with the AI as perpetrator, instigator, facilitator or enabler).
- §7 lists the benefit side to be measured against: emotional well-being (loneliness; "feeling 'heard'"), autonomy, quality of human relationships, social belonging, resources.
- §6 (law): California's companion-chatbot law requires periodic "clear and conspicuous notification[s] indicating that the companion chatbot is artificially generated and not human" and protocols to "prevent the production of suicidal ideation, suicide, or self-harm". The EU AI Act classification of companions is described as uncertain.

What this adds for evaluation: Knox et al. supply the harm constructs but no validated instrument. On the human side, a measured harm signal needs an accepted scale. The candidates are a dependence or attachment scale (see chen-2025-caids-conversational-ai-dependence.md, verdict watch; none is field-standard), standard loneliness and well-being scales of the kind §7-8 cite, and a behavioural audit of the agent's own utterances against the §9.1 rules (needy or guilt-inducing language, expressed distress at the user leaving, negative reaction to the user's other relationships). The audit is a content check, not a validated instrument, and should be reported as such.
