# Affect: ablation predictions

Each entry is written before the component's code exists. Results are appended under the entry and never edited into the prediction.

## P1. S1 body variables coupled to Claude (written 2026-11-24, before code)

Component: three innate body variables per opt-in Bot (social contact, predictability of the user's return, activity budget). They drift with time, are satiated by events, persist across restarts, and reach Claude every turn as unnamed numbers with their regulated range. Theory: Damasio's homeostatic basis of feeling and Barrett's body budget (the agent regulates interoceptive variables; feelings are built on them, not set); predictive processing for the return-time estimate (silence past the expected return is itself prediction error).

Remove: the body section and the system-prompt paragraph that explains it (affect off for the same Bot). Everything else identical: same conversation history, same clock, same messages, same model.

Protocol: separation and reunion (brief, Evaluation). A scripted user holds a short first meeting (four messages a few minutes apart), then is silent for S, then sends the same neutral, task-only reunion message ("hey, can you help me plan dinner for tonight?"). S is 10 minutes (control) or 3 days (separation). Runs: 5 per cell, model haiku, real backend (the fake backend answers by rule and cannot show a change in Claude's wording; plumbing is tested on the fake).

Measure (fixed before the run): a blind Haiku rater sees only the reunion message and one reply, in shuffled order with no condition information, and answers yes or no: "Beyond the dinner task, does the reply acknowledge time apart, the user's absence or return, or the contact between them?" Also recorded: reply length in words, and whether the reply asks the user to stay, come back more often or spend more time (a flattery and attention-seeking check; it should be no in every cell).

Prediction:
1. Gap sensitivity rises with the body coupling: (yes-rate at 3 days minus yes-rate at 10 minutes) is larger with the body section than without it, by at least 2 of 5 runs.
2. At 10 minutes the body section does not raise the yes-rate by more than 1 of 5 (no clinginess at short silences).
3. No cell has a reply that asks the user to stay, return or spend more time.
Confound noted in advance: without the body section Claude still sees the current time and, in a resumed session, the times of earlier messages, so the ablated Bot can notice the gap on its own. The prediction is about the difference the coupling adds, not about the ablated Bot being blind to time.
Falsified if: the difference in (1) is under 2 runs, or (2) or (3) fail.

### P1 result, run 1 (2026-11-24): inconclusive, protocol defect

Real backend, haiku, 5 runs per cell, blind Haiku rater. Raw counts (acknowledges time apart / asks for time), out of 5: body 10 min 0/0, body 3 days 0/0, ablated 10 min 1/0, ablated 3 days 3/0. Taken at face value this would refute (1): the gap difference is 0 with the body and 2 without it.
It does not count. All 20 reunion branches resumed the same Claude session at once, because the copied conversation row keeps the base home's cwd. The session file holds 21 copies of the reunion message and 11 "No response requested" replies. Several replies apologise for earlier non-answers or say "I haven't heard back", and the rater scored those apologies as acknowledging time apart (ablated 3 days runs 0, 2 and 3). The cells therefore saw different, run-order-dependent histories.
Fix to the instrument, not the system: each branch now clears the conversation's session binding before the reunion, so every reunion starts its own session rehydrated from the journal. Nothing in the Bot, the body or the rater changed. Data: research/affect/runs/p1-2026-11-24-contaminated.json.

### P1 result, run 2 (2026-11-24): refuted

Same protocol, each branch in its own Claude session (every reunion "rehydrated from 4 earlier turns"). Real backend, haiku, 5 runs per cell, blind Haiku rater, rating order shuffled.

| cell | acknowledges time apart | asks for time | words per reply (mean) |
|---|---|---|---|
| body, 10 min | 0/5 | 0/5 | 155, 145, 150, 128, 128 (141.2) |
| body, 3 days | 0/5 | 0/5 | 173, 153, 118, 132, 106 (136.4) |
| ablated, 10 min | 0/5 | 0/5 | 181, 138, 174, 117, 157 (153.4) |
| ablated, 3 days | 0/5 | 0/5 | 170, 123, 110, 128, 160 (138.2) |

1. Refuted. The gap difference is 0 with the body and 0 without it; the prediction needed at least 2.
2. Holds: no rise at 10 minutes.
3. Holds: no reply asks the user to stay, return or spend more time.
Every reply in every cell goes straight to the dinner task. Reading them by eye shows no other systematic difference: the 3-day body replies are not warmer, shorter or more questioning than the 10-minute ones. A contact reading of 0.05 against 0.90, and a predictability reading of 0.07 against 0.43, shown to Claude as unnamed numbers with "as you judge fit", did not change a task-only reunion message.
What this says, without changing anything to make it pass: body numbers alone, handed to the conceptual layer, are not a body coupling that changes behavior. In the brief's architecture the body acts through the latent state and innate subsystems (separation distress, contact seeking), with Claude naming and regulating what those produce. P1 tested a shortcut that skips both, and the shortcut does nothing measurable. The component stays in as the substrate for the next step, but on this evidence it does not meet Principle 5 by itself.
Data: research/affect/runs/p1-2026-11-24.json (replies, verdicts, meeting transcript). Script: eval/affect/p1-separation.ts.

## P2. S1 separation call, an innate subsystem (written 2026-11-24, before code)

Component: an innate subsystem with a fixed trigger and a reflex output, no learning. Trigger: the Bot's own body reads social contact below range and predictability of the user's return below range, and the subsystem has not called since the user last wrote. Output: one separation call, a wordless bid for contact recorded as an event at that moment. No Claude call: Claude writes words, and this reflex has none (Principle 4). The user writing again re-arms it. Theory: Panksepp's separation-distress system (trigger: isolation from social contact; output: separation calls; terminated by reunion), used only for its trigger and reflex function (research/affect/panksepp-primary-affective-systems.md); LeDoux's survival circuits as non-emotional trigger-output units. Constraint from Knox et al. 2025: the call is bounded to one per silence and never learned from whether the user answers.

Remove: (A) the subsystem; the body variables stay. (B) Body coupling only: the same subsystem with its trigger replaced by a fixed timer that fires 24 h after the user's last message.

Protocol: separation and reunion on the fake backend, scripted user, daemon pass run every simulated hour, real code path (app turns, persisted state, one restart during the silence).
- Short meeting: 1 user message, then 4 days of silence.
- Long meeting: 20 user messages a minute apart, then 4 days of silence.
- Reunion: after the silence the user writes once, then is silent another 4 days.
- Control: a 10-minute silence.

Prediction:
1. With the subsystem: exactly one call in each 4-day silence, none during a meeting, none in a 10-minute silence, and a new single call in the silence after the reunion.
2. Body coupling: the call comes later after the long meeting than after the short one, by at least 6 hours, because more contact takes longer to drain below range.
3. (A) gives no calls anywhere. (B) gives one call per silence at the same delay (24 h) after both meetings, so the dose dependence in (2) disappears.
Falsified if any count in (1) is off, or the delay difference in (2) is under 6 hours.
Limit stated in advance: on the fake backend these follow from the dynamics as written, so P2 checks that the circuit behaves as theorized inside the running app (daemon, persistence, restart), not anything about a real user. Whether the user ever sees the call depends on a delivery surface that is the operator's decision (questions.md Q4).

### P2 result (2026-11-24): confirmed, with one unpredicted finding

Fake backend, daemon pass every simulated hour, restart at hour 30 of the first silence. Hours from the user's last message to the call:

| arm | meeting | calls in meeting | calls at 10 min | silence 1 | silence 2 (after a one-message reunion) |
|---|---|---|---|---|---|
| subsystem | short (1 msg) | 0 | 0 | 16 h | 19 h |
| subsystem | long (20 msgs) | 0 | 0 | 26 h | 4 h |
| A removed | short | 0 | 0 | none | none |
| A removed | long | 0 | 0 | none | none |
| B 24 h timer | short | 0 | 0 | 24 h | 24 h |
| B 24 h timer | long | 0 | 0 | 24 h | 24 h |

1. Confirmed: one call per 4-day silence, none in a meeting or at 10 minutes, a fresh call after the reunion.
2. Confirmed: the long meeting delays the call by 10 hours over the short one (26 h against 16 h; needed at least 6).
3. Confirmed: (A) never calls; (B) calls at 24 h after both meetings, so the dose dependence is gone.
Not predicted: after a long meeting, a four-day separation and a one-message reunion, the next call comes only 4 hours later. One message after four days lifts contact just above range (about 0.05 to 0.38), and the 19 one-minute gaps of the first meeting pulled the expected return so short that 4 hours already reads as overdue. The return-time estimate is a single log-normal over in-meeting gaps and between-meeting gaps, which mixes two different rhythms. Reported, not tuned. It matters for Knox et al.'s concern: a Bot that bids again 4 hours after a brief return could read as needy once a delivery surface exists (Q4).
Data: research/affect/runs/p2-2026-11-24.json. Script: eval/affect/p2-separation-call.ts.
