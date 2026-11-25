# macOS speech synthesis: `say`, embedded speech commands, AVSpeechSynthesizer

Sources read: `man say` on this Mac; Apple Speech Synthesis Programming Guide, "Fine-Tuning" chapter (documentation archive, 2006); developer.apple.com JSON docs for AVSpeechUtterance (overview, pitchMultiplier, rate, init(ssmlRepresentation:), prefersAssistiveTechnologySettings) and AVSpeechSynthesizer.write(_:toBufferCallback:).

## Claims
- `say` speaks text or writes AIFF/WAVE/CAF with a chosen voice (`-v`) and rate in words per minute (`-r`).
- Embedded commands change prosody inside the text and apply from the next word on: `[[rate N]]` (50-500 wpm), `[[pbas N]]` baseline pitch (1-127), `[[pmod N]]` pitch modulation depth, `[[volm N]]`, `[[slnc ms]]`, `[[emph +|-]]`, each settable absolutely or relatively (`+`/`-`). Effects are "dependent on synthesizer capabilities".
- AVSpeechUtterance: `pitchMultiplier` 0.5-2.0, `rate`, `volume`, pre and post delays, set per utterance before enqueueing. SSML input since macOS 13 (`init(ssmlRepresentation:)`); `write(_:toBufferCallback:)` (macOS 10.15+) returns audio buffers.

## Evidence (measured on this Mac, M1 Pro, f0 by pitchy)
- Voice "Samantha (English (US))": `[[pbas 45]]` gives median f0 190.5 Hz, `[[pbas 50]]` 235.2 Hz, `[[pbas 60]]` 367.7 Hz, so baseline pitch is honored and monotonic.
- "Fred": `[[pbas 35]]` 60.1 Hz, `[[pbas 60]]` 204.2 Hz.
- `[[rate 120]]` vs `[[rate 240]]` on the same sentence: 4.28 s vs 3.01 s.
- One sentence rendered to file in 1.42 s wall time, including process start.
- 188 voices are installed. Apple's docs do not list which SSML elements each voice honors; not tested here.

## License (paper, code, model weights)
- Part of macOS, governed by the macOS license; there are no separate weights to manage. Apple documentation is copyrighted.

## Runs on this Mac without a GPU?
- Yes: system service, on-device, offline for installed voices.

## Verdict: adopt (as the S2 voice baseline)
- The only option reviewed with continuous per-word controls for pitch base, pitch range, rate and volume. The motor pathway can emit continuous values, never emotion labels (Principles 1 and 2 applied to output). It is fully local, with no model to ship.
- When `prefersAssistiveTechnologySettings` is true, assistive-technology settings take precedence over utterance values. Keep it false.
- Voice identity: which installed voice to use is the operator's decision, like the face's look (Principle 8). Use a plain default until approved.

## Role in S2
- voice
