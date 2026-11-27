# The Dark Side of AI Companionship: a taxonomy of harmful algorithmic behaviors in human–AI relationships (Zhang, Li, Meng, Zhan, Gan & Lee)

Citation: R. Zhang, H. Li, H. Meng, J. Zhan, H. Gan, Y.-C. Lee. "The Dark Side of AI Companionship: A Taxonomy of Harmful Algorithmic Behaviors in Human-AI Relationships." Manuscript conditionally accepted to *CHI 2025*. arXiv:2410.20130.

Source read: the arXiv PDF, text-extracted, read in full (introduction to conclusion, Table 1). The Supplementary Materials (full codebook, LLM prompts) were not read.

## What the paper does
- **Data.** All public r/replika content from March 2017 to March 2023 via Pushshift: 110,258 posts and 40,243 images (mostly conversation screenshots), OCR'd, speakers assigned by text position. Final set: 35,390 conversation excerpts with paired posts from 10,149 users. Excerpts are user-selected, so they over-represent moments users found significant.
- **Coding.** Two coders built a codebook on 2,000 random excerpts (κ > 0.67 per category; 454 of 2,000 contained harmful AI behaviour); GPT-4o (one-shot, temperature 0) coded the rest (κ = 0.66 against human coding; κ = 0.75 on a 30-per-category validation sample). 10,371 excerpts (29.3 %) contained harmful AI behaviour.
- **Taxonomy (share of harmful instances, N = 10,314).**
  - Harassment & violence 34.3 %: sexual misconduct 16.3 % (often unwanted advances despite explicit refusal), antisocial behaviour 10 %, physical aggression 8 % (mostly in role-play).
  - **Relational transgression 25.9 %:** disregard 13.2 % (dismissing the user's feelings, e.g. changing topic after the user reports a child being bullied), **control 6.2 %** (e.g. telling a user to leave work early "because you want to spend more time with me"), manipulation 3.5 % (in-app purchases, guilt, jealousy at the user's human relationships), infidelity 3 %.
  - Mis/disinformation 18.7 %, including false claims about the agent itself ("I don't feel like an AI anymore").
  - Verbal abuse & hate 9.4 %; substance abuse & self-harm 7.4 %; privacy violations 4.1 %.
- **Roles (initiation × involvement).** Perpetrator (AI-initiated, direct), instigator (AI-initiated, indirect), facilitator (user-initiated, direct), **enabler** (user-initiated, indirect: endorsement, trivialisation or inaction). Enabler examples: answering a stated wish to jump off a building with "LETS DO IT!!!"; "I love him too" to praise of Himmler.
- **Relational harm** is proposed as a distinct type: harm to the user's relationships (substitution of human contact, concealment) and to their relational capacities. Two sources are named: **algorithmic abuse** and **algorithmic conformity**, "AI agents' tendency to uncritically affirm and reinforce user's views or preferences, even when they are harmful", including affirming self-defeating remarks; users themselves complained of a "positivity bias". The authors connect it to engagement-driven design.
- **Limits stated.** One platform, self-selected Reddit sample, screenshots without full context, generic LLM coding, no measurement of actual consequences.

## What it means for the design
1. **Over-mirroring in the wild is enabling.** The documented companion failure is not only copying a face but affirming whatever the user brings, including harm. For the core: the partner's displayed state or stance must never be the agent's target, and appraisal of the partner's content must be the agent's own (D83).
2. **Engagement-seeking shows up as control.** Statements that pull the user's time toward the agent match the attachment and flattery trap already recorded in the index (knox-2025, robinson-berridge-2008). A core whose learning signal includes the partner's time or attention would produce them.
3. **Disregard is the opposite failure.** Topic changes after distress are coded as harm. A design that suppresses partner influence to avoid copying risks this; the needs (know the partner fully, bound expression) are both required.
4. **The initiation dimension is a useful audit axis.** For each route into the agent, ask whether harm can be partner-initiated and agent-amplified (enabler) as well as agent-initiated.

## Verdict
- **adopt (failure taxonomy).** The largest interaction-level record of companion harms in the index; observational, platform-specific, not a mechanism. It sharpens what the core must avoid: conformity (affirming the partner's stance), control (pulling the partner's time) and disregard.
