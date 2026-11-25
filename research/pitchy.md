# pitchy (Ian Johnson; McLeod Pitch Method)

Sources read: github.com/ianprime0509/pitchy README and LICENSE; npm metadata for pitchy 4.1.0; github.com/peterkhayes/pitchfinder README and npm metadata (alternative).

## Claims
- A pure-JavaScript pitch detector, "fast and accurate enough to be used in real-time applications such as tuners", implementing McLeod and Wyvill's "A Smarter Way to Find Pitch" (MPM).
- `PitchDetector.forFloat32Array(n).findPitch(input, sampleRate)` returns `[pitchHz, clarity]`, where clarity in [0, 1] separates a true pitch from noise.

## Evidence
- ESM-only, one dependency (`fft.js`); works in browser and Node.
- Measured here (Node 24, Apple M1 Pro, 2048-sample frames at 48 kHz, a 180 Hz harmonic tone plus noise, 3000 calls): 0.11-0.12 ms per call, returned 180.0 Hz, clarity 0.999. A 30 Hz prosody loop costs well under 1% of a core.
- Also used here on `say` output to measure f0 (see macos-speech-synthesis.md), giving monotonic f0 changes.
- Alternative pitchfinder (YIN, AMDF, McLeod, dynamic wavelet): its npm license field says "GNU v3" and the repo has no LICENSE file, which is a worse fit.

## License (paper, code, model weights)
- Code: 0BSD (LICENSE: "Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted"). The README's license paragraph says "zig-xml" by copy-paste mistake; the LICENSE file is authoritative. No weights.

## Runs on this Mac without a GPU?
- Yes. About 0.12 ms per 2048-sample frame in Node (measured).

## Verdict: adopt
- Gives continuous f0 and a voicing proxy (clarity) with no model and no labels (Principle 1). Runs in an AudioWorklet, so raw audio never leaves the page; only feature frames are stored (Principle 7).
- Energy (RMS) and speech rate (syllable-nucleus or energy-peak rate over voiced segments) are a few lines of our own code. No reviewed library provides speech rate.

## Role in S2
- perception
