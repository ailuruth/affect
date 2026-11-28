# VoxCPM2 (OpenBMB, 2026)

Code: github.com/OpenBMB/VoxCPM (README read in full).

**How fully read:** README only; the documentation site and technical report not read.

## What it says
- A 2B-parameter TTS trained on over 2 million hours in 30 languages, 48 kHz. Modes: "Voice Design" (a new voice "from a natural-language description alone (gender, age, tone, emotion, pace ...)"), "Controllable Cloning" (clone from a short clip "with optional style guidance to steer emotion, pace, and expression", e.g. the instruction "(slightly faster, cheerful tone)"), and "Ultimate Cloning" from clip plus transcript.
- Weights and code under Apache-2.0. Runs on `mps`; through llama.cpp-omni "RTF ~1.76 (Q8_0) on Apple M4 Pro / Metal", i.e. slower than real time on a newer Mac than this one.

## What matters for this engine
- Every control is a natural-language instruction that names emotions or bins (label-like); identity is a description or a cloned clip. Slower than real time on Apple silicon. The licence is clean, the control model is not.

## Verdict: reject
