# Handoff for milestone M1: what to run on your Mac

Written 2026-11-26 for the operator. Sources: research/build/spec.md §6 (row M1 and the "M1 branch thresholds" table),
§7.2, §7.3, §7.5; engine/README.md; Makefile; pyproject.toml; research/machine.md; research/questions.md Q34.

M1 measures what your Mac can do (tracking time, speech-recogniser speed and accuracy, breathing detection, tick
times, memory, the network sandbox, and a few checks of the Claude command-line tool). Each check gives a number, and
the number picks a branch from a fixed table. Nothing is tuned by hand.

## Status, plainly

- **Ready now:** the engine skeleton and the offline core (M0 and the offline part of M4). Steps 1–5 below work today.
- **Not written yet:** `tools/week0/` does not exist. Nor do the sandbox profile (`engine/config/sandbox.sb`), the
  model downloader, the browser page with the face tracker, or the processes that make up "full load". So the M1
  checks themselves (step 7) **cannot run yet**. The scripts still to be written are listed in step 7, with the
  command each will have. Until they exist, do steps 1–6 and answer the questions in step 6.
- **Nothing is downloaded or sent off your Mac without your approval.** Steps 3–4 install software (Python and
  packages from the public Python package index). No model, dataset or recording is downloaded, and nothing about
  you is sent anywhere. Models come only after you answer Q34 item 4. Claude test calls come only after you confirm
  them (step 6).

## 1. Check the Mac

Open Terminal. Check that you have free space above your 10 % floor:

```
df -h .
```

You need about 1 GB now, and about 2–4 GB more for the models later (only if you approve them).

## 2. Install the Xcode command line tools (needed later to build `pyworld`)

```
xcode-select --install
```

If it says they are already installed, carry on.

## 3. Install uv and Python 3.13

If you use Homebrew:

```
brew install uv
```

Otherwise use the installer on uv's own website (astral.sh); that is a download you choose to make. Then:

```
uv python install 3.13
uv --version
```

The project accepts Python 3.12 or 3.13 (not 3.14).

## 4. Get the code and install the core

Use the repository address you already have (on GitHub):

```
git clone <repository-url> affect
cd affect
uv lock
uv sync
```

`uv lock` writes `uv.lock`, which pins exact package versions for your Mac (this is part of M1; keep the file).
`uv sync` creates `.venv/` with only numpy, scipy and pytest.

Do **not** install the larger extras (`engine`, `mac`: torch, the speech runtimes, pyworld) yet. They are needed for
the M1 checks, once those scripts exist and you have approved model downloads. The command will then be:

```
uv sync --extra engine --extra mac
```

## 5. Run the tests first: `make ci`

```
make ci PY="uv run python"
```

It runs a check that no recorded data is in the folder, the label lint, and the test suite on small synthetic arrays.
It takes about 2 minutes. **Expected:** it ends with all tests passed, except one test reported as `xfailed`
(the known small-ceiling gap, Q35; D92), which is expected. If anything else fails, stop and send the last 40 lines of
the output.

Optional, several minutes:

```
make regress-full PY="uv run python"
```

## 6. Answer these before M1 starts (research/questions.md, Q34)

M1 cannot start until you have answered:

1. **Item 4, downloads to the Mac.** M1 needs the models: MediaPipe face-tracker assets (≈ 15 MB), Kyutai STT 1B
   (≈ 1–2 GB), Whisper-small (≈ 0.5 GB), all-MiniLM-L6-v2 (≈ 90 MB). The TTS voice comes later (M5), and the Seamless
   recordings at M3 (≈ 16.6 GB passes through, ≈ 1.5 GB kept). Free space is checked before each download, and nothing
   writes below your 10 % floor. You can answer "models only".
2. **Item 5, your conversation language.** The streaming recogniser covers English and French only. For any other
   language the check moves to the fallback row (another streaming model, or the slower utterance recogniser).
3. **Item 10, offline after the first download.** The recommended answer is yes: after the download step, every engine
   process runs with the model hub switched off and the network denied (only the Claude process can reach the network).
4. **Claude test calls (text only, through your own Claude Code login).** Five of the M1 checks call Claude with
   short scripted text. No audio, video, face data or anything about you is sent. Please confirm you allow these
   test calls. Q34 items 1 and 8 (text to Anthropic, no paid overage) are the full question, for M6; a yes to the test
   calls alone is enough for M1.

Until each answer is recorded, the code that depends on it refuses to run (`engine/config/operator.py`).

## 7. The M1 checks (scripts still to be written)

Every check runs under **full load**: every engine process running, with a scripted 10-minute session. You run
each one; it prints its number and writes it into `research/build/week0.md`. The commands below are the ones the
scripts will have. **None of these files exists yet.**

| # | Script (to be written) | What you do | What it measures | Pass (Plan A) | Branch | Fail (stop, report) |
|---|---|---|---|---|---|---|
| 0 | `tools/week0/env_check.py` | run it | macOS, chip, Python, uv, Xcode tools, free disk | — | — | — |
| 0 | `tools/week0/download_models.py` | run it after item 4 | downloads the four models, checks free space first, writes their SHA-256 into `engine/config/models.lock` | — | — | — |
| 1 | `tools/week0/tracker.py` | sit in front of the camera | face-tracker time per frame, p99, at full load | ≤ 20 ms | 20–30 ms: own-face tracker drops to 5 Hz | > 30 ms after the branch |
| 2 | `tools/week0/echo_rig.py` | set up the rig (below), then run it on the video | capture-to-screen pipeline time, p99 | ≤ 90 ms | 90–400 ms: pass with warning | > 400 ms |
| 3 | `tools/week0/clock.py` | run it with the browser page open | whether the browser gives a capture time; otherwise the spread of the measured offset | capture time present | absent: use the fallback; offset SD ≤ 10 ms | offset SD > 33 ms |
| 4 | `tools/week0/asr_stream.py` | read the 5-minute script aloud | Kyutai STT: language, word-end-to-delivery p90, word error rate, speed (RTF) at full load | p90 ≤ 0.9 s, WER ≤ 15 %, RTF < 0.5 | p90 0.9–1.5 s: used, longer partial echo; worse, or another language: another streaming model, else the utterance recogniser alone | the utterance recogniser also fails its row |
| 5 | `tools/week0/asr_utterance.py` | (same reading) | Whisper-small: RTF at full load, WER | RTF < 0.3, WER ≤ 12 % | RTF 0.3–0.5: pass, latency stated | RTF ≥ 0.5 or WER > 20 % |
| 6 | `tools/week0/breath.py` | follow the prompts: paced breathing at 6 and 12 per minute, 10 breath holds, rest twice, then the same while talking | breathing rate error and hold detection | silent: rate error ≤ 1 /min in ≥ 80 % of 30-s windows, ≥ 9 of 10 holds, test–retest r ≥ 0.7; talking: error ≤ 2 /min in ≥ 60 % of windows | silent passes, talking fails: breathing used only when both are silent | silent fails: breathing off |
| 7 | `tools/week0/fast_tick.py` | run it | the 30-Hz engine tick, p99, at full load | ≤ 5 ms | > 5 ms: Plan B (native extension), re-measure | Plan B > 5 ms |
| 8 | `tools/week0/slow_tick.py` | run it | the 2-Hz tick, p99 | ≤ 50 ms | 50–200 ms: one part steps at 1 Hz | > 200 ms |
| 9 | `tools/week0/memory.py` | run it | peak memory of all processes over the session | ≤ 6.0 GB | > 6.0: 4-bit Kyutai; then pool of 2; then pool of 1 | > 6.0 GB with pool 1 |
| 10 | `tools/week0/sandbox_check.py` (+ `engine/config/sandbox.sb`) | run it | network connections from sandboxed processes in 10 min | 0 non-local connections | — | any |
| 11 | `tools/week0/claude_checks.py resume` | after step 6 item 4 | Claude `resume` of a hand-written transcript, byte check | accepted and identical 20/20 | otherwise a fallback for the forks | — |
| 12 | `tools/week0/claude_checks.py thinking` | (same) | thinking tokens at effort `low` | 0 in 20/20 | > 0: measured, added to latency | — |
| 13 | `tools/week0/claude_checks.py latency` | (same) | first-sentence latency p90 (Haiku, effort `low`) | ≤ 1.5 s | 1.5–3.0 s: pool of 3, deadline binds more often | > 3.0 s: reported to you (a slower agent) |
| 14 | `tools/week0/claude_checks.py compaction` | (same) | whether the auto-compaction switch exists and is off | found and off | not found: detection only | — |
| 15 | `tools/week0/claude_checks.py tokens` | (same) | tokens per call at the 4,000-token window | ≤ 4,500 | > 4,500: window shortened | — |
| — | `tools/week0/report.py` | run it last | writes `research/build/week0.md`: every number and the branch it selects | — | — | — |

Also still to be written for these checks: the browser page with the face tracker (M2's `web/`, at least its tracking
part), the scripted 10-minute load session (`tools/week0/load_session.py`), and the 5-minute reading text
(`tools/week0/reading.txt`).

When they exist, each check runs as, for example:

```
uv run python -m tools.week0.env_check
uv run python -m tools.week0.tracker
uv run python -m tools.week0.report
```

**The echo rig (check 2).** A phone or tablet in front of the camera plays a looped face video with sharp
lip-corner-pull onsets and flashes a white square in one corner on the same frame as each onset. A second phone
films both that screen and the Mac's screen at 240 frames per second, for at least 50 onsets. The video stays on your
Mac; the script reads the lag frame by frame. A photodiode on each screen can replace the video.

**What stays on your Mac.** Your reading, your breathing recordings and the rig video are used only to compute the
numbers. The scripts delete them or keep them locally, as you choose. Only numbers go into `week0.md`.

## 8. What to send back

Send `research/build/week0.md`: commit it to the repository, or paste it. Check first that it holds only numbers and
branch names (no transcripts or recordings). If a check stops at its "Fail" column, send the file as it is, with the
terminal output of that check.

Also keep `uv.lock` from step 4 and send it with `week0.md` (it pins the environment for later milestones).
