# Solomon & Corbit 1974: An opponent-process theory of motivation. I. Temporal dynamics of affect

Citation: R. L. Solomon, J. D. Corbit. *Psychological Review* 81(2): 119-145, 1974. doi:10.1037/h0036128.

Source read: the full text, from a PDF hosted on a university course page (ninova.itu.edu.tr). The copy's provenance is unofficial and the APA publisher version was not checked. The companion imprinting paper was not obtained and is unread: Hoffman & Solomon 1974, *Learning and Motivation* 5: 149-164, "III. Some affective dynamics in imprinting". Solomon's 1980 *American Psychologist* review was blocked by the host and is also unread.

## Claims
- Every strong hedonic state (the a process) recruits an opponent b process of opposite sign. Manifest affect is a − b.
- Timing: the a process "has a short time constant". The b process "is sluggish, so it has a relatively long latency, recruits slowly, and dies out slowly". It is "a slave process: It is activated indirectly via the activation of the a process."
- Plasticity: "the b process is strengthened by use and weakened by disuse". A well-used b process "will show a shorter latency of response to a, a quicker rise, a higher asymptote, and a longer decay time". "In contrast, an a process is a relatively stable, unconditioned reaction."
- Attachment uses the same mechanism. The authors present addiction, love and imprinting together: "with examples taken from love and affection, social attachment, and imprinting in birds, … addiction does not differ in principle from any acquired motivational system."
  - Imprinting, after Hoffman's duckling work: when the imprinting object is removed "there is a burst of distress crying which may last for several minutes and then disappear. With successive presentations and removals of the imprinting stimulus, the frequency and intensity of distress crying will increase."
  - Lovers: separated, "they will feel lonely, sad, and depressed (State B) … Actual reunion will simultaneously erase B and reinstate A".
- Time scales of B states differ by system. Distress calling in precocial birds lasts "a few hours", while "loneliness and grief" last "for months".
- The b process "can, under proper conditions, be activated by events in memory, as a consequence of Pavlovian conditioning procedures."

## Evidence
A theory paper. It organises published examples (parachutists, dogs given shocks, opiate users, ducklings) into one qualitative scheme. There are no new data and no fitted equations; the dynamics are given as block diagrams (Figs. 3-4).

## License
APA copyright. Read from an unofficial course copy. No code.

## Runs on this Mac without a GPU?
n.a. A two-time-constant linear system with a use-dependent gain takes a few lines to simulate.

## Verdict: adopt (the two-time-scale form for separation), with a hard safety constraint
- This is the foundational fast/slow account of separation distress:
  - a fast positive process tied to the partner's presence;
  - a slow, use-strengthened opponent that appears as distress when the partner leaves;
  - each opponent attached to a particular object, here the imprinting object.
- Taken unchanged, it predicts escalating, addiction-like separation distress with every contact-and-loss cycle. That is the dependence pattern Knox et al. warn about (knox-2025-harmful-traits-ai-companions.md) and the unbounded drive Principle 6 forbids.
- Use the time-scale split. Bound the b process's gain and make it satiable, so "strengthened by use" saturates. Test explicitly that distress does not grow without bound across repeated partings.

## What it implies for the open question
- Separation distress needs at least two state variables per attachment figure: a fast one and a slow, plastic one. Each is tied to that figure.
- One scalar "contact" gauge cannot reproduce three things:
  - the after-reaction on parting, which comes from the slow opponent outliving the fast process;
  - the growth of that after-reaction with history, which comes from b's use-dependence;
  - its specificity to the object, since the duckling's distress follows removal of its imprinting object.
- Structure pays here through time scale and identity, not through the number of needs.
- An ablation prediction for the Bot: collapse the per-person (a, b) pair into one decaying contact trace, and the overshoot of distress after a parting, and its dependence on that person's history, should disappear.
