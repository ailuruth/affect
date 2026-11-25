# Cross-species affective neuroscience decoding of the primal affective experiences of humans and related animals

Jaak Panksepp, *PLoS ONE* 6(9):e21236, 2011 (PMC3168430). I read the main text and Appendix S1 (`pone.0021236.s001.doc`), which describes each system.

## Claims
- Localized electrical stimulation of the brain (ESB) in homologous subcortical regions elicits seven "primary-process" emotional systems in all mammals tested: **SEEKING, RAGE, FEAR, LUST, CARE, PANIC/GRIEF, PLAY**. The capitalized names mark networks. "No claim is made of identity with the corresponding vernacular words."
- These systems survive early neo-decortication (PLAY included). Animals will work to switch ESB of these sites on or off, so the states act as rewards and punishments. Panksepp argues they are therefore felt.
- The systems sit in nested hierarchies: primary processes, then secondary learning, then tertiary cortical awareness and appraisal, with bottom-up and top-down causation.
- Appendix S1:
  - **PANIC/GRIEF** is the response of young animals "when they get lost". It is "a separation-distress process — a psychic pain" that "helps cement infant-mother attachments". Young animals "are adept at crying out for care".
  - **CARE** is maternal motivation, driven by estrogen, progesterone, prolactin and oxytocin.
  - **PLAY** is social rough-and-tumble with laughter-like vocalizations.
  - **SEEKING** is appetitive "wanting", not "liking". It also carries homeostatic affects such as hunger and thirst.

## Evidence
A review of decades of ESB, lesion, decortication and place-preference work across species. Human ESB reports are cited as comparable. There is no new data. Neurochemical details are in Figure 5 and the cited books.

## License
- Paper: CC BY (PLoS).
- Code: none.

## Runs on this Mac without a GPU?
n.a.

## Verdict: adopt (as a list of innate functions, not as emotions)
Adopted as the theory basis for the brief's innate subsystems: separation distress, contact seeking and care, play, novelty seeking. Each has a fixed trigger and a reflex output. To satisfy Principle 2 we take the **trigger→reflex function** and drop the emotion naming and the claim about feelings. LeDoux (ledoux-survival-circuits.md) explicitly rejects that claim, and Barrett calls it the mental-inference fallacy. Subsystems are named by function in code (`separation_distress`), never by feeling.

## What it gives S1
- **Separation-distress subsystem.**
  - Trigger: loss of contact with the attachment figure. In S1 that is elapsed silence beyond the learned expected gap for this user (contact body variable below its predicted value).
  - Reflex: "crying out", which in text means a bid for contact. This is the only S1 subsystem allowed to initiate a message, and it is rate-limited and satiable.
  - Offset: contact restores the body variable and stops the distress drive.
- **Attachment through relief.** In Panksepp's account, distress followed by reunion "cements" attachment. In S1, the relief of a reunion should strengthen the user-specific contact prediction in $h$. Prediction: a Bot whose distress was relieved by this user shows a stronger reunion response next time than a Bot that never went through that cycle.
- **PLAY as a separate, low-priority subsystem.** It is triggered by safety plus contact and suppressed while separation distress is active. Prediction: humor or teasing returns only after contact is restored, not on the first reunion turn.
- **SEEKING carries homeostatic needs.** Body deficits (activity budget, predictability) should raise exploratory and initiative behavior, not a "wanting" label.
