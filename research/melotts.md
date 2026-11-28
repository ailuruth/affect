# MeloTTS (MyShell.ai and MIT; Zhao, Yu & Qin 2023/2024)

Code: github.com/myshell-ai/MeloTTS (README and docs/install.md read).

**How fully read:** README and install guide. Model cards not reachable.

## What it says
- Multilingual VITS / Bert-VITS2-based TTS with fixed accent speakers (EN-US, EN-BR, EN-INDIA, EN-AU, EN-Default, and other languages), "fast enough for CPU real-time inference". The documented control is `--speed`. Library under the MIT licence; macOS install supported, Docker suggested for some Macs.

## What matters for this engine
- A fixed synthetic speaker and a permissive licence, but no pitch or energy input, so it is an identity carrier only, like Kokoro without Kokoro's internal F0 and energy curves. No reason found to prefer it over Kokoro for English.

## Verdict: watch (identity-only alternative)
