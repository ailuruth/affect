# Affect: questions for the operator

Decisions that are yours (visual identity, data leaving this Mac, new paid services, changes to existing Ailurini behavior). Work that these block is not built; work they do not block continues.

## Report 5: one design revised twice, and a question about novelty (Q21 below; 2026-11-26T06:31:55Z)

**The design.** The seventh design puts one built-in limit, the same whichever way the agent learns, on every path from the agent's inner state to its own face and voice. Two revisions followed.
- **First version.** It hid your face from the agent's mind behind heavy noise. The critics showed this stops caring as well as copying: it would never notice you were sad. Speech rate, laughter in the transcript and head and gaze mirroring also leaked.
- **Second version.** The agent knows you fully: its slow inner state follows your held expression almost perfectly. Every path to its expression is bounded, and in its own checks held copying fell from 0.91 to 0.09. This separation of knowing you from moving toward you works, and it carries forward.
- **The critics still found:**
  - the slow state's knowledge reaches the fast face through an unbounded side input, so the agent's pitch follows yours at 0.9;
  - the limit added against slow copying works in both directions, so the agent is muted, held within ±0.15 whichever way it would move;
  - the agent has no positive feelings: good news and warm moments leave it unmoved;
  - it never speaks first;
  - its care learns to prefer drafts that make you look happier, which is a form of flattery.

**What comes next.**
- Read on three gaps:
  - satiable positive drives: wanting good things, not only avoiding bad ones;
  - care that learns to actually help without being rewarded for how you look;
  - how and when a listener takes the initiative.
- Then a third revision:
  - a one-sided limit on the slow paths too;
  - every side input inside the limit.

**Still no design to choose from.**

## Q21. Should a design with no known concrete failure be put to you even if it combines existing mechanisms? (asked 2026-11-26T06:31:55Z; work continues meanwhile)

**Why this comes up.** Eight designs so far, and the critics have judged every one a combination of existing mechanisms. Your rule, as last written, is that a design with no known concrete failure goes to you as a candidate to build. The brief also asks for a genuinely new core mechanism. The two can conflict: the current design may soon have no concrete failure and still be a combination.

**Options:**
- **Put it to you, with the novelty verdict stated plainly** (my recommendation). You decide whether a sound combination is worth building as a first testbed, while the search for a new mechanism continues in parallel.
- **Hold it until a design is also new.** Only a design judged new reaches you.
- **Something else:** tell me the rule.

**What it blocks:** nothing now. It matters only once a design clears the concrete-failure check.

**Answer (operator), 2026-11-26T08:41:00Z: yes.** A design with no known concrete failure is put to the operator, with its novelty verdict stated plainly.

## Report 4: two more reading rounds and a sixth design (no answer needed, 2026-11-26T04:48:22Z)

**What was read.** Seven readers, about 45 sources. This session's network first allowed no paper sites. A personal environment for this project now allows the main open-access ones. Some sources were still unreachable: where a reader used a later paper that restates the results, its note says so, and nothing unread is cited.
- **How people avoid copying over long conversations.** They don't couple less: on the same channel they are less alike than chance at some timings and more alike at others. Disagreement flips the direction. Pairs actively avoid repeating the pattern they just made together. Shared smiling comes mostly from reacting to the same thing.
- **How the brain keeps imitation from turning into copying.** It reads the other's face in its own muscle coordinates but keeps it in a separate "theirs" slot. It tags each movement as "mine" or "theirs", and the situation decides how much "theirs" may reach its own face.
- **Mathematics for limits that hold over all routes at once.** Networks whose stability and per-channel limits are built in, so learning can't break them. Privacy-style budgets that every output draws on together. Limits on how many bits per second the partner can pass to the agent.
- **What tells copying from its opposite.** No information measure can: copying and doing the opposite carry exactly the same information. Copying is one extreme corner of all the ways two faces can be related, and doing the opposite is the other.

**A sixth design: a fast part you reach and a slow part you can't drive.** Your face reaches only a fast, always-settling part with built-in limits. Moods sit in a slow part that you can change only through a small budget of events.
- **The critics found:**
  - its moods last about half a minute under its own noise, not hours;
  - the slow part can still track your held face, matching it at about 0.9 on one-minute averages;
  - Claude's draft choice and the voice had no limit;
  - it is a combination of known parts.

**The pattern, now seen six times.** Every design limits routes one at a time, and copying comes back through a route it didn't count. This round points to a two-part answer that no design has tried yet:
- **one budget over everything your face can influence**, which closes the counting problem;
- **a separate one-sided limit against moving in step with you** on each channel, measured over the whole path from your face to the agent's, which closes the direction problem. Responding in the opposite direction stays free.

The open problem is building a network that satisfies the second limit by construction. That is the next design.

**Still no design is ready for you to choose from.**

## Report 3: the third round of critiques (no answer needed, 2026-11-26T02:08:03Z)

**What was done.** Independent reviewers, none of whom wrote the designs, checked the three newest designs step by step. They checked 144 proof steps in all: 81 hold, 40 have gaps and 23 are wrong. The work moved to a cloud session; a usage limit paused it for about nine hours, and it resumed on its own.

**The three designs reviewed, and what each found.**
- **The partner as a learned regulator** (third version).
  - **What improved:** your face no longer reaches the agent's same expression directly, and every route has a built-in limit.
  - **What fails:**
    - the term that comforts you has a limit on its size but not on how fast it changes, so the agent can again fall into one of two stuck states;
    - the smile limit, once a missing "relief smile" is counted, is above the design's own copy line;
    - its comfort can't tell your unusual happiness from distress, and it gives up on distress that lasts.
- **Reading you through the agent's own body** (second version).
  - **What improved:** much milder than before.
  - **What fails:**
    - one learned number still moves a group of channels (social smile, brows, head, pitch) all the way to copying;
    - if your face follows the agent's after more than about three seconds, the agent learns to follow you.

    It also turns out to be active inference underneath, a framework you excluded as a core.
- **Persistent states whose existence the agent's own needs decide** (new).
  - **What improved:** it is the only design so far where your face reaches the agent only as brief built-in events, each with a fixed limit and no single strength setting.
  - **What fails:**
    - events your face sets off indirectly, through what the agent makes of the conversation, add enough routes to copy the whole face;
    - how often you trigger events works as a strength dial;
    - your held expression levels still leak in.

**All five designs are now critiqued and on hold. All are combinations of existing mechanisms.** None is ready for you to choose from, so there is no choice to put to you yet.

**The pattern.** Each new design closes the direct route from your face to the agent's face, and copying comes back through an indirect one:
- a comforting loop;
- a shared learned estimate;
- the agent's own interpretation of events.

The next reading round goes after this directly. It looks for mathematics that bounds what *all* routes together can carry, not each route one at a time. The candidates are bounds on how much information a whole system can pass, and structures where copying is impossible by symmetry rather than by tuning. It will also read on how people avoid falling into copying over long conversations.

## Report 2: the second cycle, and a question about the "no single setting" rule (2026-11-25T14:40:05Z)

**What was read.** Five more readers, about 65 sources:
- **Reading a partner's face as information** about the situation, judged against one's own concerns, rather than as a signal to pass on. This is how people seem to work, and it explains why responses are handled per expression and can flip sign.
- **Telling "they respond to me" from "I follow them".** A standard statistical fix exists: the agent uses its own small random variations as a handle on cause and effect.
- **How a frozen Claude can be shaped without words or numbers.** Choosing among drafts, and choosing which past conversation snippets it sees.
- **The emotional voice and conversational timing.** Replies come within about 0.2 seconds, so the agent must predict when your turn ends.
- **Agency, coping, and wanting versus liking.** All of these can come from one learned model of what causes what.

**Designs.** One new design and one revision:
- **New: reading you through the agent's own body.** Your face is only evidence. The agent explains it with its own model of how its own face shows its own feelings, then responds with its own judgment of the situation.
- **Revised: the partner as a learned regulator.** It blocks direct copying and adds a declared, brief, built-in smile and brow match.

**What the critiques found.**
- **Both still contain the flat-to-copy setting on the smile and frown channels,** in slower or subtler forms.
- **Both had a piece that conflicted with your rule against rewarding your expressions:**
  - one steered your face toward the agent's own resting face;
  - the other scored Claude's drafts by how you would feel.

  Both pieces are withdrawn. Your face may only ever be evidence, never something the agent drives.
- **The tally:** 17 designs and sketches so far, and every one has, somewhere, a quantity that takes the agent from flat to copying.

**Why this keeps happening, and a question for you (Q18 below).**

## Report 1: the first read–design–critique cycle (2026-11-25T13:25:38Z, no answer needed)

**What was read.** Ten readers covered about 125 published sources, each with a note and a one-line index entry. The biggest findings:
- **Your dial question is answered by the literature.** When people respond to a familiar or liked partner, the shape of the response changes, not just its size. Each expression is handled separately:
  - smiles are returned almost always, except to rivals;
  - sadness is mirrored only for people on one's side;
  - disgust is never mirrored;
  - some responses reverse: smiling at a partner's anger when cooperating.

  A fast automatic match comes first, and the effect of context arrives 2–4 seconds later. Partner history is learned within minutes.
- **Coordination between people is not one strength setting either.** Whether two people move together or opposite is separate from how strongly they are linked, and it differs by channel (in couples, heart rate and skin conductance can be linked in opposite directions). Roles emerge and swap. A close partner acts as a learned regulator. The same holds for voices: loudness converges, pitch adjusts only locally, and voice quality converges slowly.
- **Published listener-face and avatar systems fail at both ends of that dial:**
  - they copy the speaker, which people notice and trust less;
  - or they go flat, which the challenge scores reward;
  - the partner barely matters: raters cannot tell when it is swapped;
  - none has a lasting internal state.

  The full table is in research/foundations/known-failures.md.
- **The face.** The face has separate emotional and deliberate driving routes. What is innate is muscle patterns (newborns smile in their sleep), not emotions. Copying is learned from being imitated, and it can be reversed by an hour of practice.
- **Memory.** A temperament and a relationship with you can plausibly form from a few hours a day with nightly replay. The piece that carries "specific to you" is feeding the context of each memory back in during replay.
- **Claude.** Through your subscription, no continuous signal can be fed to Claude. What the state may do is choose among Claude's drafts and choose which real past conversation snippets it sees. That reweights text without writing it, with a proved ceiling on how much it can shift each reply. When needs are met, the influence switches off.
- **How breakthrough mechanisms were found.** Attention and the Transformer would themselves fail your "list every part" test. What made them new was a measured failure followed by a principle that removed a setting someone would otherwise have to tune.

**Which designs exist.** Three, written independently to your mathematical-depth standard:
- **The two people as one mathematical structure.** How each body connects to the shared space of expressions is learned per expression.
- **"Whose" kept apart from "what".** Like the position encoding in language models, responses depend only on the relation between the agent's frame and the partner's.
- **The partner as a learned regulator.** The partner never pushes on the agent directly; it only selects among the agent's own ways of calming or redistributing its internal state.

**What the critiques found.** Independent reviewers checked every proof step by step.
- **All three still contain the flat-to-copy setting,** each in a new disguise:
  - in the first, a "ceiling";
  - in the second, a learned strength that works out to between 0 and 1;
  - in the third, a property that holds only when the agent has no needs.
- **Many proof steps failed:** 23 of 83 items were errors.
- **All three are combinations of existing mechanisms,** as their own authors had said.
- **Two lessons carry forward:**
  - (1) any map that carries the partner's face into the agent's face, learned or tuned, ends up with this setting;
  - (2) learning "who responds to whom" from experience is easily fooled: the agent can mistake its own following for the partner responding.

**What happens next.** Two readers are now working on the most promising way out the reading suggests:
- treating the partner's expression as information about the shared situation, judged against the agent's own concerns, rather than as a signal to pass on, which is how people appear to work;
- how infants and causal statistics tell "they respond to me" apart from "I follow them".

The three designs are held for revision, and new designs will follow from this reading.


## Q1. The S2 voice (voice identity) — open, 2026-11-24
S2 will speak through macOS speech synthesis (`say` / AVSpeechSynthesizer), which is local and takes per-word pitch, pitch range, rate and volume (research/affect/macos-speech-synthesis.md). Which installed voice the Bot uses is its voice identity. Not built until you pick one. Blocks: spoken output in S2. Does not block: S1, perception, the placeholder face.

## Q2. Upgrading the placeholder face (visual identity) — answered in brief.md on 2026-11-25; recorded, not built
S2 starts with a deliberately neutral procedural face drawn in three.js, using the 52 ARKit blendshape channel names. The only freely licensed (CC0) realistic rig found is TalkingHead's mpfb.glb (research/affect/talkinghead.md), a realistic human head. Using it, even untextured, sets the Bot's look. Not used unless you approve it or another look.

## Q3. Face-feature library version (data leaving this Mac) — decided by default, reversible, 2026-11-24
@mediapipe/tasks-vision 1.0.0 and later send usage telemetry (not video) to odml.pa.googleapis.com every 60 s; 0.10.35 has no such endpoint (research/affect/mediapipe-face-landmarker.md). Plan: pin 0.10.35, serve its wasm and model from the local server, and set CSP `connect-src 'self'`, so nothing leaves the Mac. If you would rather use a 1.x build and accept the telemetry, say so.

## Q4. How a separation call reaches you (outward-facing behavior) — open, 2026-11-24
An Affect Bot's separation-call subsystem can now decide, below Claude and without words, that it is bidding for contact after a long silence (one bid per silence, at most). Today the bid is only recorded and shown by `ailurini bots calls <bot>`. Showing it to you anywhere else — a macOS notification, a mark on the Bot's sidebar row, or a short message Claude writes into the thread — is outward-facing behavior and, for the sidebar, a visual element. Knox et al. 2025 (research/affect/knox-2025-harmful-traits-ai-companions.md) warn that agents that display need make users feel responsible for them. Which surface, if any? Until you pick, nothing reaches you unprompted.

## Q5. Other raters, and facial EMG hardware (people outside this Mac; possibly a purchase) — open, 2026-11-24, needed no earlier than S5
evaluation.md finds two measures that cannot be done by the operator alone on this Mac:
- **Human-perception questionnaires** (Godspeed, Networked Minds) need several respondents; none supports a single rater. Using them means showing recordings of the Bot to other people, which sends the Bot's face and voice off this Mac and involves people beyond you.
- **Rapid facial mimicry** is defined in facial EMG (Dimberg & Thunberg 2012). Automatic AU coding of your face is the fallback S5 uses, but a null from it does not rule out mimicry. EMG needs hardware this Mac does not have.
Neither blocks S0, S1 or S2. Without them, S5 rests on AU-coded synchrony under a single-case design, and perception questionnaires are not used.

## Q6. May the project use Meta's Seamless Interaction recordings? (needed now: every new candidate is tested on them)

**What it is:** a public set of recorded two-person conversations, with each person's facial-muscle movements measured frame by frame. Its license allows research use but not commercial use (CC BY-NC 4.0).

**How it would be used:**
- It is downloaded onto this Mac only; nothing is sent anywhere.
- Only the facial-movement numbers and the transcripts are used. The emotion labels it also ships with are thrown away unread.

**Why it matters now:** all eight new core sketches test their first prediction on it. Without it, the candidates can't be compared on published data.

- **Yes, use it:** the new candidates are tested and compared on it. The project then can't be sold or used commercially while it depends on this data.
- **No:** I look for another published conversation dataset with suitable terms. Testing waits until one is found, and the closest alternative (CANDOR) has its own terms to check.

*[The Q2 note that was here, about the approved parody face, is unchanged: it affects S2 only.]*

**Answer (operator), 2026-11-25: yes.** Use the Seamless Interaction recordings under their non-commercial research terms, downloaded to this Mac only, using only the facial-movement streams and transcripts. I have no plan to use this project commercially.

## Q7. Where S0 stands, and whether you want to redirect it: status, 2026-11-25. Work continues without an answer.

**The gate.** The brief requires each candidate to meet the four expressive-structure items before it can be marked complete, and the comparison needs at least three candidates written to the standard. After three independent reviews of the shared test bed (research/foundations/sims/structure/VERIFICATION*.md), **neither viable candidate meets all four items**:

| | Content-dependent selection | Structure over a learned space | Dimensionality plus ablation | Richness from structure |
|---|---|---|---|---|
| **Costate** | Mostly met (myopic) | Partly. The need field is instantiated but its benefit is not shown; two attempts stood down. | Partly | Partly |
| **Robust regulator** | Partly (myopic by construction) | Partly | Partly | Shown in a toy (ES16) |

**What is solid:**
- Need-conditioned selection and attention beat fair low-dimensional ablations: ES1, ES8b, ES9.
- Per-person two-time-scale tracking helps: ES10b.
- Look-ahead beats myopic selection: ES12, 0.73×. This is the only result that separates the candidates.
- The Principle 6 constraints (D66 and its two amendments) remove engagement gradients in toys, with a measured price.

**What has not worked:**
- No world tested shows that a field of needs over a *learned* space pays.
- A no-learning threshold rule with innate self-fill beats every learned policy tested.
- The slow-costate time signature did not appear (ES17).

**Possible redirections, yours to choose if you want one:**
- **(a) Continue as now.** More toys toward the four items, then a fourth review.
- **(b) Interpret the requirement as "stated and shown where it pays".** Proceed to the comparison with the gaps documented. This would be your reading of the brief; I will not adopt it myself.
- **(c) Accept the gaps as findings.** The richness may need real data or a learned world model, not toy worlds. In that case S0 could end with a comparison that says so plainly.

Until you answer, I continue with (a).

**Q7 update, 2026-11-25, after the fourth review (sims/structure/VERIFICATION-4.md).**
- **A tie-breaking bug reversed one finding.**
  - Reply-conditioning alone does **not** stop the agent learning to raise its own expression to draw engagement; both learning arms do (0.69–0.78).
  - Only D66's outright exclusion of the agent's expression from every learned map blocks it. **That exclusion is essential.**
- **Costate's rollout over a library of base policies slightly beats the no-learning threshold rule when exploration costs are removed** (0.976, from a probe). With ε-exploration learning, it does not.
- **The slow-costate signature exists but is weak:** ρ ≈ 0.4, against the predicted 0.5.
- **Neither candidate meets all four items.** The options above stand. I continue with (a).

**Q7 update, 2026-11-25: new evidence since the last update.**
- **Richness from structure (item 4).** Against a fair full-state learned value, the candidates' per-need rule loses with 2 needs (1.36×) and wins with 8 needs (ES20b). *[corrected after VERIFICATION-5]* The "about 20×" came from an unstable baseline; with a stable one the advantage at 8 needs is about 1.4×. So the structure pays modestly, and more as needs multiply.
- **Tampering (D67).**
  - A drive that reads a resettable sensor is gamed on 99.99% of steps (ES21).
  - Both candidates now read the body only through innate event detectors, with no learned parameters inside the drive.
- **Still unmet for both candidates:**
  - the benefit of a learned *spill* space for needs;
  - Costate's slow-costate signature at its predicted strength;
  - a fully derived (non-myopic) selection rule in field worlds.
- **The options above stand.** I continue with (a).
**Answer (operator), 2026-11-25: none of (a), (b) or (c). Restart the core search.**
- Both remaining candidates (Costate, Robust regulator) are homeostatic regulators over a few body gauges, with affect read out of their values or prices. That is the "a few variables" design I rejected, now in mathematical form. The need fields added on top of them do not change that. Stop refining them in need-regulation toys (multi-need homeostasis, attachment over separations, sensor tampering).
- What I want from the core: emotion emerging as structure in a rich learned latent state, with that same state driving the face, the voice and what Claude says, and reading the other person through the agent's own body. Homeostasis is at most one input to that state, not the core.
- Explore genuinely new architectures, on the level of what attention and the Transformer were when they appeared: a new computational mechanism, not an existing framework (active inference, homeostatic RL, optimal control) with extra structure bolted on. Sketch several, from different lenses, before developing any.
- Judge candidates on published tasks, data and analyses used as published (brief.md, Evaluation). A self-made toy can illustrate a mechanism but is not evidence for completing a candidate or comparing candidates.
- Write future questions to me in plain language, with one line per option saying what happens if I pick it.

## Q8. Operator note on the pace of S0, 2026-11-25 (an instruction, not a question)
The divergence phase ended too fast: eight sketches and a pick of three in one tick. The core is the most important decision in this project, so slow down before converging. D69's pick of three stays provisional until all of the following are done:
- **Ground every sketch in the literature.** For each, find and read in the primary source the closest prior work in ML, neuroscience and dynamical systems, and state concretely what the sketch does that the prior work does not. A sketch that turns out to be an existing mechanism renamed is recorded as such.
- **Widen before narrowing.** Write more sketches from lenses not yet used, so that the pool is not only the eight from a single tick.
- **Critique round.** Independent subagents that did not write a sketch try to reduce it to an existing framework, and to break it on the risks the eight share (collapse into a delayed copy of the partner; a single hidden dial from flat affect to rigid imitation). Record each critique and the sketch's answer to it.
- **Then re-pick**, with the reasons written in research/foundations/sketches/README.md, and tell me in plain language whether the pick changed.


## Q9. Operator note: a new mechanism is still missing, 2026-11-25 (an instruction, not a question)
The three D69 candidates are not the new mechanism I asked for. Efference-keyed memory is attention or modern Hopfield retrieval plus fast-weight delta-rule writes, applied in a new key space. Contingency operators and coupled oscillators are existing mathematics. Surprise-gated re-noising is the closest to a new mechanism, but it still borrows diffusion. Keep all three as recombination baselines, not as the core, and change how the search is done:
- **Novelty test for every candidate.** List each computational part. If every part is an existing mechanism (attention, Hopfield retrieval, fast weights, recurrent or state-space models, diffusion, energy models, oscillators, linear operators, value or price readouts), the candidate is a recombination: record it as one, whatever the key space, the time scales or the naming. Only a computation that does not exist in prior work counts as a new mechanism, and its closest prior work must be read in full, not from abstracts.
- **Find the mechanism from failures on real data, as attention came from the fixed-vector bottleneck of sequence-to-sequence models.** First run the strongest published models for predicting a listener's face and voice reactions in face-to-face conversation (released code and weights only, run as published and runnable on this Mac; for example Learning to Listen, Ng et al. 2022, checked in its primary source. Meta's Seamless Interaction dyadic models are not released, per research/seamless-interaction.md, so they are not a baseline) on Seamless Interaction, scored with their published metrics and with the analyses in evaluation.md. Then write down, with numbers, exactly where they fail: for example carry-over with a returning partner, collapse into a delayed copy, no lasting state, flat affect, or misreading under context. Then design a mechanism whose reason to exist is one of those measured failures, and test it on the same data against the same baselines.
- **Keep Q8.** Ground, widen and critique before converging. A candidate is developed in full only after it passes the novelty test and names the measured failure it is meant to fix.
- Report to me in plain language: the baselines run, where they failed, and which failure each new candidate targets.

## Q10. Operator note: know this Mac's limits before planning work, 2026-11-25 (an instruction, not a question)
- Measure this Mac once, from macOS itself, and write research/machine.md: chip and CPU/GPU core counts (`system_profiler SPHardwareDataType`, `sysctl -n machdep.cpu.brand_string`), unified memory (`sysctl -n hw.memsize`), free disk on the volume holding this repository (`df -h .`), macOS version, and whether PyTorch MPS is available in this project's uv environment. Re-check free disk before any large download.
- Plan every dataset download, baseline and experiment against research/machine.md and state the budget in the plan: disk needed, peak memory, and expected run time on this Mac. Leave headroom: keep at least 20% of the disk free, and keep peak memory well below unified memory, because the operator uses this Mac for other work.
- Prefer a small pilot (a few hundred Seamless interactions, under 1 GB) before any full download, and download features only, as research/seamless-interaction.md describes.
- A baseline or model that cannot run on this Mac as published (unreleased weights, CUDA-only, more memory than this Mac has) is recorded as not runnable here, with the reason, and is not adapted or simplified to make it fit.
- No approval is needed for large downloads or long runs (the operator confirmed: 20 GB and 6 hours are fine, and he does not want to be asked about size or run time). Stay within the disk and memory headroom above, and record the budget in the plan.

## Q11. This Mac's disk is already below your free-space rule. ANSWERED 2026-11-25: floor lowered to 10% free (see the operator answer at the end of this section). Downloads may start.

**The situation:** your rule is to keep at least 20% of the disk free. The disk holding this project is 460 GiB, with **55 GiB free (12%)**. To reach 20% free, about 37 GiB more would need to be freed. Everything else in the plan (running published listener-reaction models and testing new designs on the conversation recordings) needs some downloads: model weights, plus a pilot of a few hundred conversations, under 1 GB of features.

- **Free up space yourself** (about 37 GiB or more): I then work within the rule as written, with pilots first.
- **Allow small downloads anyway** (for example up to 5 GB in total, features and model weights only): I run the pilot and the first published baselines now, and stop well before the disk gets tighter.
- **No downloads at all for now:** I continue only with reading and design work (prior work, more sketches, critiques). Running baselines waits.

Until you answer, I do only work that needs no downloads.

**Update after your note "no approval needed for download size; keep 20% of the disk free":** the disk is still at 12% free, so the 20% rule still blocks *every* download, even the 1.3 GB pilot of the conversation data. Everything that needs no new data is being done meanwhile (the shared test harness, the person-level splits, reading and critiques).
- **Free about 40 GiB:** I start the pilot immediately and screen many designs on it.
- **Lower the floor (for example to 10% free):** I download the pilot (about 1.3 GB) and later the full training features (about 28 GB; my earlier figure of 11 GB was too low) within that floor. At a 10% floor about 9 GiB is usable now, so the full training set would still need space freed.

**Answer (operator), 2026-11-25: lower the floor to 10% free.** Download the pilot and then the full training features within that floor. Re-check free disk before each download. This replaces the 20% figure in Q10 and research/machine.md.

## Q11. Operator note: build and evaluate as many architectures as possible, 2026-11-25 (an instruction, not a question)
Breadth is wanted. Generate and evaluate as many distinct architectures as this Mac allows, not three.
- **One shared harness first.** Before screening, build one evaluation harness on Seamless Interaction that every architecture runs through unchanged: fixed train/validation/test splits by person (no person in two splits), the same feature loader and block list, the published baseline metrics, and the analyses in evaluation.md. Fix and record the splits, metrics and pass thresholds before any architecture is scored, with timestamps from the system clock.
- **Screen widely, develop narrowly.** Many architectures (dozens, not a handful) get a short, equal-budget screening run on a pilot subset, with the same compute and data budget each, recorded in one table: research/foundations/screening.md (architecture, its parts, novelty-test verdict, which measured baseline failure it targets, scores, run time, peak memory). Only the strongest go on to full development and the critique round in Q8.
- **Sources of architectures.** New mechanisms from the measured baseline failures (Q9), the sketches already written, variations of each, and recombinations. Recombinations are screened too, as baselines; the novelty test decides only which can become the core.
- **Fairness.** Equal budgets, the same splits, no tuning on the test split, and the same number of hyperparameter trials per architecture, recorded. A screening result is a filter, not a claim; claims need the full protocol and independent recomputation.
- Within the disk and memory headroom in Q10. No approval is needed for download size or run time.

## Q12. None of the published "listener reaction" models can run here as published. How should the comparison be done? (needed before baselines run)

**The situation.** I checked ten published models that predict how a listener's face reacts in a conversation. None can run on this Mac, or on the conversation recordings you approved, without being changed:
- they all need an NVIDIA graphics card (CUDA);
- they need either raw audio and video, or a 3D face format the recordings don't include.

Your rule is not to adapt or simplify a published model to make it fit, so I have recorded them as not runnable.

**What can still be done here exactly as published:** the simple comparison methods and scores those papers use. These are:
- **"always the typical face"** (the median face);
- **"a random clip of someone else"**;
- **"the most similar past moment"** (nearest neighbour);
- **"copy the speaker"** and **"copy the speaker half a second late"**;
- **their standard accuracy, variety and timing scores.**

They work directly on the recordings' facial-movement numbers. The published papers also already report one telling failure: simply copying the speaker beat every learned model on their main timing score.

**Options:**
- **Use the published simple methods and scores, plus the failures the papers report:** I measure, on the recordings, where these simple methods fail, and design new mechanisms against those failures. This needs only the small pilot download (see the disk question).
- **Also run one learned model on a rented cloud GPU, as published:** a fairer test against real learned models. It means a new paid service, and the recordings' features would leave this Mac. I would ask again with the exact cost before doing it.
- **Allow me to adapt one learned model to the recordings' face format:** this would break your "don't adapt" rule. I would retrain it from its published code on the approved features, and clearly label it as adapted.

**Answer (operator), 2026-11-25: the first option.** Use the published simple baselines and the published metrics (REACT and Learning to Listen, as transcribed in research/harness/HARNESS.md), plus the failures the papers report. No cloud GPU, and no adapted learned models. Measure on the recordings where the simple baselines fail, including the flat-versus-copy dial, and design new mechanisms against those failures.

## Q13. Status: the independent critiques of the eight design sketches (no answer needed), 2026-11-25

**The pick changed.** Four reviewers who had not written the sketches checked each of the eight designs against your novelty test and read the closest published work in full. **All eight turned out to be combinations of existing mechanisms.** So none is a candidate for the core any more. That includes the three I had picked earlier. All eight will instead be run as comparison baselines.

**The useful finding.** All eight fail in the same way. In each design, a single setting decides how much of the other person's face goes into the agent's own face. Turned down, the agent goes flat; turned up, it copies. That is the "single hidden dial" you warned about. The published record shows a related failure: in a well-known listener-face challenge, simply copying the speaker beat every learned model on its main timing score.

**Next.** First measure this failure on the conversation recordings: how much copying, how flat, and whether a single setting explains it. Then design new mechanisms aimed specifically at it. The measuring needs the recordings, so it waits on the disk question (Q11).

## Q14. Status: four more design sketches, from new angles (no answer needed), 2026-11-25

**The pick did not change.** I asked for four more sketches from fields not tried before:
- how the immune system tells self from non-self;
- musical and theatre improvisation;
- animal signalling;
- robots that learn by acting.

Independent reviewers checked them. All four are again combinations of existing mechanisms. In three of them, one setting still runs the agent from flat to copying. In the fourth (improvisation), no setting is exposed, but how it is fitted to data plays the same role.

**What this suggests.** Across all twelve sketches, the flat-to-copy dial appears whenever the partner's face is carried into the agent's face by a learned or tuned connection. Before inventing more, I will check whether real people work this way:
- **Turning up or down?** When people meet a familiar person rather than a stranger, does their reaction to the other's face just get stronger or weaker? Then a single dial is true of people too, and the goal is setting it well.
- **Changing shape?** Or does it change which expressions they answer, and how? Then a new mechanism must reproduce that.

This check needs the conversation recordings, so it waits on the disk question (Q11).

## Q15. Operator note: stop the baseline-scoring track, 2026-11-25 (an instruction, not a question)
- **Do not re-measure what is already documented.** The failures of existing listener-reaction and dyadic face models are reported in their papers, in the REACT challenge reports and in published surveys and reviews of the field. Collect them from those sources, read in full, into research/foundations/known-failures.md, each with its citation and the evidence the source gives. Stop scoring the simple baselines (median face, random clip, nearest neighbour, mirror, delayed mirror) on Seamless as a step toward inventing; it is not a gate for anything.
- **Why:** face-matching scores (accuracy, diversity, synchrony of the listener's face) measure the surface of the output. They are the "looks right" criterion I rejected, and they say nothing about whether a learned internal state causes the face, the voice and the words. They must not steer the invention.
- **What the core is judged on instead:** the claims in brief.md and evaluation.md that test internal state, not surface: steering the state changes face, voice and words together and dose-dependently, lesions remove specific functions, and coupling to the partner beats surrogate baselines (E1 to E3). Surface metrics may be reported later as a side check, never as the criterion for choosing the core.
- **The human dial question (does a person's reaction to a familiar partner only scale, or change shape?)** is answered from the published literature on facial mimicry and familiarity first. Run it on Seamless only if the literature leaves it open, and say so.
- **Next:** with known-failures.md in hand, return to inventing mechanisms (Q9, Q11 breadth), aimed at the documented failures and at the flat-to-copy dial found in all twelve sketches.

## Q16. Operator note: the S0 process from now on, 2026-11-25 (an instruction, not a question)
This replaces the process steps in Q8, Q9, Q11 and Q15 (baselines first, shared harness, screening, measuring failures). The principles in brief.md, the novelty test, "no toy worlds as evidence" and the Mac budget still hold. S0 is now one simple cycle, repeated:

1. **Read as much research as possible.** Go wide and deep across every field that bears on the goal: affective and cognitive neuroscience, developmental psychology, face perception and mimicry, ML architectures and how new mechanisms were found, dynamical systems, embodied and social AI, and the known failures of existing systems (papers, challenge reports, surveys). Read primary sources in full. Write a note per source in research/ and keep research/index.md current. Each cycle should add substantially, not a handful of notes.

2. **Design a new architecture and the whole system from it.** Using what was read, design a new core mechanism and the full system around it: perception of the other's face and voice through the agent's own body, the latent state where emotion emerges, face and voice output, the coupling to Claude, learning by living, and memory and replay. Write it in research/foundations/<design>.md with equations, what is new against the closest prior work read in full, and its weak points. Have an independent subagent critique it (can it be reduced to existing mechanisms; does it collapse into flat-or-copy behaviour; what does it fail to explain) and record the critique and the answer.

3. **Repeat.** Each new cycle reads more, with the gaps the last critique exposed in mind, then revises the existing designs or writes new ones. Keep all designs in research/foundations/designs.md with a one-line summary, novelty verdict and main weakness each.

- No downloads or experiments are needed for this cycle. Testing comes later, once the operator picks designs to build, and judges internal state (brief.md, evaluation.md E1 to E3), not surface face-matching.
- After every few cycles, report to the operator in plain language: what was read, which designs exist, what is new in each, and what the critiques found.

## Q17. Operator note: mathematical depth is the standard for every design, 2026-11-25 (an instruction, not a question)
Mathematical depth was the operator's requirement from the start. A design described in words with a few equations attached is a sketch, not a design. The standard is the depth of mechanisms like attention or RoPE: RoPE is a precise object (rotating queries and keys by position) with a property proved from it (the inner product depends only on relative position). Every design in research/foundations/ must meet this:
- **A precise mathematical object.** Define the mechanism exactly: its spaces, operators, group actions, dynamics or algebraic structure, with every variable and its domain. Plain-language intuition comes first, but the object itself must be exact.
- **Properties proved, not asserted.** State the properties the design needs as theorems and prove them, or derive them carefully, with every step checkable. At minimum: that the design has no single setting that runs it from flat affect to copying the partner (or exactly what it has instead); that its drives are satiable where it has drives; how time scales from reflex to temperament arise from the structure; and what reading the other through its own body means as a mathematical statement.
- **Why existing mechanisms cannot do it.** Show mathematically, not by naming, why the property does not follow from the closest existing mechanisms (attention, Hopfield retrieval, fast weights, state-space models, diffusion, oscillators, linear operators). If it does follow, the design is a recombination.
- **Down to a buildable network.** From the object, derive a concrete network: how 30 Hz face streams, voice, transcript events and the agent's own body enter; how time and position are encoded (RoPE, ALiBi, continuous-time or state-space encodings, or a new encoding the object implies) and why; which layers in what order with sizes and parameter counts; training objectives and what is learned online versus in replay; and the latency and memory budget on this Mac (research/machine.md). Mark which parts carry the new mechanism and which are ordinary choices.
- **Critique checks the mathematics.** The independent critique must check each proof step by step and try to construct a counterexample, not only judge the idea.

## Q18. What exactly should "no single setting from flat to copying" mean? (needed for the next designs; work continues meanwhile)

**The situation.** Seventeen designs and sketches all failed this test. The reviewers' proofs show why.

Whenever your face can influence the agent's face at all, some quantity exists whose size decides how much. On any one channel, say smiling, turning that quantity from zero upward takes the agent from not responding to responding like you. That is true of people too: how strongly one person returns another's smile varies.

What the research says is different about people:
- that strength is set separately for each expression, by context and by the relationship;
- it can flip sign;
- matching is not a state people get stuck in.

What designs can reach is to make the setting learned, per expression, bounded and context-set, and to make copying a state the agent is pushed away from. No design can remove such a quantity entirely without also removing your influence.

**Options:**
- **Keep the rule as written:** no quantity anywhere may run a channel from flat to copy. Designs keep being judged as failing. I would read toward mechanisms where your face never reaches the agent's expressive channels at all, which may conflict with your mimicry principle (perceived faces drive the agent's own motor pathways).
- **Refine the rule** (my recommendation). No single quantity may run the *whole* face from flat to copy. Each channel's strength must:
  - be set separately per expression by context and learned relationship;
  - be able to flip sign;
  - stay under a built-in ceiling;
  - never let copying become a state the agent settles into.

  Designs would be judged against that, with each such quantity named and bounded.
- **Something else:** tell me the criterion you have in mind, and designs will be held to it.

**Answer (operator), 2026-11-26: refine the rule, as recommended.** No single quantity may run the whole face from flat to copy. Each channel's strength must be set separately per expression by context and learned relationship, be able to flip sign, stay under a built-in ceiling, and never let copying become a state the agent settles into. Name and bound every such quantity in each design. The original concern was one-dimensional designs, not the existence of per-channel strengths.

## Q19. Operator note: proofs need not be rigorous; critiques look for concrete failures; candidates go to the operator (2026-11-26T04:57:50Z; an instruction, not a question; updates Q17)
- **Proofs.** They do not need to be complete or rigorous; this is not a mathematics project. Each design keeps a precise mathematical object and a convincing argument for each key property. A design is no longer held for proof gaps or loose steps.
- **Critiques.** They focus on concrete ways the mechanism actually fails (for example, an uncounted route that carries copying), not on rigor.
- **Testing.** Correctness will be settled by building and testing, judged on internal state (steering, lesions, coupling beyond surrogates).
- **Candidates.** Once a design has no known concrete failure, it is put to the operator as a candidate to build.

## Q20. May the agent's inner state follow your face closely, as long as its own expression never moves toward copying yours? (asked 2026-11-26T05:41:07Z; work continues on the recommended reading)

**Why this comes up.** The latest design stopped copying by hiding your face from the agent's slow mind behind heavy noise. It worked against copying, but the agent then couldn't notice you were sad, couldn't learn how to respond to you, and couldn't care. The critics' lead is to separate two things:
- **knowing:** the agent's inner state models your face and voice richly (it knows you look sad, and for how long);
- **moving toward:** every path from that inner state to the agent's own face and voice passes through the built-in limit against moving in step with you.

**Options:**
- **Allow knowing, limit only the expression** (my recommendation). The inner state may follow your face and voice as closely as perception allows. The flat-to-copy rule (Q18) applies to every path from that state to the agent's expression, and is enforced by construction. This fits your aims of perceiving your emotion and reading you through the agent's own body, and it is how people work: we know exactly how the other looks without copying it.
- **Limit knowing too.** The inner state may carry only a noisy, bounded summary of your face, as in the latest design. The critics showed this makes the agent unable to care or learn you from your face.
- **Something else:** tell me the line you want drawn.

**What it blocks:** nothing is blocked. The next revision is written on the recommended reading and will be changed if you choose otherwise.

**Answer (operator), 2026-11-26T08:41:00Z: allow knowing, limit only the expression (as recommended).** Humans do mimic unconsciously, so partial, fast, per-expression matching within the Q22 ceilings must stay. Only whole-face copying and getting stuck in copying are ruled out.

## Q22. Two choices about how the agent's face responds to yours (asked 2026-11-26T07:36:40Z; work continues on the recommendations)

The latest design passes the strongest checks so far. Its critics raised two things that are your call rather than defects:

**1. One limit for every expression, or a limit set per expression?** Right now the agent's face may move toward yours by at most 0.10 of a full copy on every channel alike. Human data: smiles are returned almost always, sadness is mirrored for people on one's side, disgust is never mirrored. Your rule (Q18) asks for strengths set per expression.
- **Per-expression built-in ceilings** (my recommendation). For example, smile and laughter up to about 0.3–0.4 toward yours; sympathetic brow-raise at a sad face up to about 0.2; disgust, contempt and anger toward yours 0. Each ceiling is innate, and the actual strength within it is still learned per relationship and context and can flip sign. The agent would smile back at your laugh and show sympathy at a sad face. Copying the whole face remains impossible.
- **Keep one uniform 0.10 cap.** Safest against copying, but it never laughs because you laugh, and it shows no sympathy at a silently sad face.

**2. Should strong expressions follow your words or your face?** At present the agent's strong, lasting expressions follow what you say and its own body; your face moves it only within the cap.
- **Both, through the agent's own appraisal** (my recommendation). Your face and voice feed the agent's own judgement of the situation: you look shaken, so something happened to you. That judgement drives its own expression, which is not a copy of yours, within the per-expression ceilings above.
- **Words only.** Simpler and safest, but the agent reacts to what is said more than to you.

**What it blocks:** nothing. Revision 4 is written on the recommendations and will change if you choose otherwise.

**Answer (operator), 2026-11-26T08:41:00Z: both recommendations.** Each expression gets its own built-in ceiling. Strong expressions come from both words and face, through the agent's own appraisal.

## Q23. How the agent reaches Claude: your subscription or a paid API key? (asked 2026-11-26T08:24:59Z; work continues on the recommendation)

**Why this comes up.** The current design has the agent's state choose among several of Claude's drafts per turn. As written, it asks for six drafts in parallel with a set randomness, and that assumes features of Anthropic's paid programming access (an API key) that your subscription does not offer. A paid API key would be a new paid service, so the choice is yours.

**Options:**
- **Stay on your subscription** (my recommendation for now). The next revision drops the randomness setting and asks for fewer, differently phrased drafts within what the subscription allows. The state's influence on Claude is narrower, but nothing new is paid for.
- **Use a paid API key.** This gives full control over the number of drafts and their randomness, and lower latency, but it is a new paid service, and conversation text would go through it.
- **Something else:** tell me.

**What it blocks:** nothing now. It only matters at build time.

**Answer (operator), 2026-11-26T08:41:00Z: stay on the subscription.** Ailurini is built on Claude Code, so the engine must work through the subscription.
