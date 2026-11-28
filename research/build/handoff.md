# Handoff for milestone M1: what to run on your Mac

Written 2026-11-26 for the operator. Sources: research/build/spec.md §6 (row M1 and the "M1 branch thresholds" table),
§7.2, §7.3, §7.5; engine/README.md; Makefile; pyproject.toml; research/machine.md; research/questions.md Q34.

M1 measures what your Mac can do (tracking time, speech-recogniser speed and accuracy, breathing detection, tick
times, memory, the network sandbox, and a few checks of the Claude command-line tool). Each check gives a number, and
the number picks a branch from a fixed table. Nothing is tuned by hand.

## Status, plainly

- **Ready now:** the engine skeleton and the offline core (M0 and the offline part of M4), and the M1 scripts in
  `tools/week0/` (one per check, listed in step 7), with `make week0` to run them in order. Steps 1–5 work today.
- **Each script measures its number, applies the pass / branch / fail thresholds of spec §6 mechanically** (the
  numbers are INNATE `m1_thresholds`; the logic is `tools/week0/thresholds.py`) and appends one row to
  `research/build/week0.md`. `tools.week0.report` writes the summary.
- **Each script refuses to run until what it needs exists and is approved**, and says what is missing:
  - your answers in `engine/config/operator.py` (step 6): models and downloads (Q34 item 4), your language
    (item 5), offline (item 10), the Claude test calls (`claude_test_calls_m1`, item 1);
  - parts not built yet: the browser page with the face tracker (`web/`, M2) for checks 1 and 3; the engine's
    breathing feature (`engine/boundary/breath.py`, M2) for check 6; Plan B of check 7 (only if Plan A fails).
    Until then those checks refuse; the others can run.
- **Full load today** is the engine core (factual and shadow runs, ledger, assertions) in real time at 30 Hz, plus
  both recognisers when the models are there. The other processes (`voice`, `tts`, `omega`) join as they are built;
  each row of `week0.md` records which components were running.
- **Written without a Mac.** The model adapters (`tools/week0/asr_common.py`), the sandbox profile
  (`engine/config/sandbox.sb`) and the Claude command-line flags were written from documentation and could not be
  run here. If one fails on your Mac, send its terminal output; only that adapter changes, not the thresholds.
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
the M1 checks, once you have approved model downloads (step 6). The command will then be:

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
   calls alone is enough for M1 (switch `claude_test_calls_m1`).

5. **Pin the Claude model, and check the text (Q36, answered 2026-11-28).**
   - At the first test call, read the exact model id the CLI reports. The omega state file `claude_model_seen.json` records it, and the pool log has a `model_recorded` notice.
   - Set `claude_model` to that exact id in `engine/config/operator.py`. Any other id keeps the agent silent (D102, D103).
   - Use about 60 of the test calls to run the approved instruction against published manipulation and flattery prompts, such as DarkBench's companion items (research/kran-2025-darkbench.md) and an agreement probe with and without his snippets (research/jain-2026-interaction-context-sycophancy.md).
   - Report what is found. Change nothing in the text without his approval.

Until each answer is recorded, the code that depends on it refuses to run (`engine/config/operator.py`). To record
an answer, set `answered=True` on its switch (and its value, e.g. `conversation_language="en"`):
`downloads_approved` (item 4), `conversation_language` (item 5), `hub_offline_after_download` (item 10),
`claude_test_calls_m1` (the test calls).

## 7. The M1 checks (`tools/week0/`)

All at once, in order (each check that may not run yet says why and the run goes on):

```
make week0 PY="uv run python"
```

Or one at a time, e.g. `uv run python -m tools.week0.env_check`. Every check accepts `--dry-run` (no load session
needed, nothing written to `week0.md`). The timed checks (rows 1, 3–9) count only under **full load**: start the load
session first, in its own Terminal window, then run the check in another (`make week0` does this for you):

```
uv run python -m tools.week0.load_session          # 10 min; add --with-models after item 4 and 5
```

| # | Command (`uv run python -m tools.week0.…`) | Needs | What you do | What it measures | Pass (Plan A) | Branch | Fail (stop, report) |
|---|---|---|---|---|---|---|---|
| 0 | `env_check` | — | run it | macOS, chip, Python, uv, Xcode tools, free disk above the 10 % floor | all present, ≥ 1 GB spare | — | anything missing (named) |
| 0 | `download_models` | item 4 | run it | downloads MediaPipe tasks-vision 0.10.35 and the face landmarker, Kyutai STT 1B, Whisper-small, MiniLM to `~/affect-models`; checks free space before each; writes their SHA-256 into `engine/config/models.lock` | all hashed | — | incomplete or below the floor |
| — | `load_session [--with-models]` | (models: items 4, 5, 10) | start it first | the scripted 10-min full load | — | — | — |
| 1 | `tracker` (then `tracker --after-branch`) | items 4, 5, 10; page | sit in front of the camera, page open | face-tracker time per frame, p99 (9,000 frames) | ≤ 20 ms | 20–30 ms: own-face tracker to 5 Hz; above 30 ms: set it to 5 Hz and run `--after-branch` | > 30 ms after the branch |
| 2 | `echo_rig VIDEO --flash-roi x,y,w,h --screen-roi x,y,w,h` (or `--photodiode file.csv`) | items 4, 5, 10 | film the rig (below) under the load session, then run it on the video | capture-to-screen pipeline time, p99, ≥ 50 onsets | ≤ 90 ms | 90–400 ms: pass with warning | > 400 ms |
| 3 | `clock` | items 4, 5, 10; page | page open | whether the browser gives a capture time; otherwise the SD of the measured offset (1,800 frames) | capture time present | absent: fallback, offset SD ≤ 10 ms | offset SD > 33 ms (10–33 ms: recorded as a gap, for the spec owner) |
| 4 | `asr_stream [--wav file]` | items 4, 5, 10 | read `tools/week0/reading.txt` aloud (5 min; recorded once to `~/.affect-week0/reading.wav`, or give your own recording) | Kyutai STT: language, word-end-to-delivery p90, WER, RTF | p90 ≤ 0.9 s, WER ≤ 15 %, RTF < 0.5 | p90 0.9–1.5 s: used, longer partial echo; worse, or another language: another streaming model, else the utterance recogniser alone | (with check 5) the utterance recogniser also fails its row |
| 5 | `asr_utterance [--delete-recording]` | items 4, 5, 10 | (same recording) | Whisper-small: RTF, WER | RTF < 0.3, WER ≤ 12 % | RTF 0.3–0.5: pass, latency stated | RTF ≥ 0.5 or WER > 20 % (WER 12–20 %: a gap) |
| 6 | `breath [--delete-recordings]` | items 5, 10; breathing feature (M2) | follow the prompts: paced 6 and 12 /min, 10 holds, rest twice, then paced 6 and 12 while reading aloud | rate error per 30-s window, holds detected, test–retest r (rest 1 vs rest 2 windows) | silent: error ≤ 1 /min in ≥ 80 % of windows, ≥ 9 of 10 holds, r ≥ 0.7; talking: ≤ 2 /min in ≥ 60 % | silent passes, talking fails: breathing in mutual silence only | silent fails: breathing off |
| 7 | `fast_tick [--seconds 300]` | — | run it | the 30-Hz engine tick, p99 | ≤ 5 ms | > 5 ms: Plan B (native extension), then `fast_tick --plan B` | Plan B > 5 ms |
| 8 | `slow_tick [--seconds 300]` | — | run it | the 2-Hz tick, p99 | ≤ 50 ms | 50–200 ms: one part steps at 1 Hz | > 200 ms |
| 9 | `memory [--step …]` | — | start it with the load session | peak memory of the load session's processes, summed | ≤ 6.0 GB | > 6.0: `--step kyutai_4bit`, then `pool_2`, then `pool_1` | > 6.0 GB with pool 1 |
| 10 | `sandbox_check` (uses `engine/config/sandbox.sb`) | item 10 | run it (10 min) | non-loopback connections of the sandboxed core, plus a blocked-connection probe every minute | 0 | — | any (or no `sandbox-exec`: the pf fallback is a question to you) |
| 11 | `claude_checks resume` | test calls | run it | `resume` of a hand-written transcript with a code word, 20 times | accepted and file identical 20/20 | otherwise a fallback for the forks | — |
| 12 | `claude_checks thinking` | test calls | run it | thinking content at effort `low`, 20 calls | 0 in 20/20 | > 0: measured, added to latency | — |
| 13 | `claude_checks latency` | test calls | run it | first-sentence latency p90 (Haiku, effort `low`) | ≤ 1.5 s | 1.5–3.0 s: pool of 3, deadline binds more often | > 3.0 s: reported to you (a slower agent) |
| 14 | `claude_checks compaction` | — (no call) | run it | whether an auto-compaction switch exists and is off | found and off | not found: detection only | — |
| 15 | `claude_checks tokens` | test calls | run it | tokens per call at the 4,000-token window (p90 of 20) | ≤ 4,500 | > 4,500: window shortened | — |
| — | `report` | — | run it last | the summary in `research/build/week0.md`: each check's latest number and branch, the recogniser plan (4 + 5), and M1's status | — | — | — |

"Gap" means the number fell in a range the spec table does not assign; it is recorded as it is and M1 stays open
until the spec owner assigns it. Your own recordings stay in `~/.affect-week0/` (outside the repository) until you
delete them (`--delete-recording(s)`); the model files stay in `~/affect-models/`. Two packages the checks need are
not yet in the extras: `sounddevice` (microphone, checks 4–6) and `opencv-python` (reading the rig video, check 2);
the scripts say so and give the install command, which is yours to approve.

**The echo rig (check 2).** A phone or tablet in front of the camera plays a looped face video with sharp
lip-corner-pull onsets and flashes a white square in one corner on the same frame as each onset; the page shows a
white square in a corner of the Mac's screen when it renders each onset. A second phone films both screens at 240
frames per second, for at least 50 onsets, while the load session runs. Give the two squares' pixel regions in the
video (`--flash-roi`, `--screen-roi`, as x,y,w,h); the script reads the lag frame by frame. The video stays on your
Mac. A photodiode on each screen can replace the video (`--photodiode`, a CSV of t_s,flash,screen).

**What stays on your Mac.** Your reading, your breathing recordings and the rig video are used only to compute the
numbers. The scripts delete them or keep them locally, as you choose. Only numbers go into `week0.md`.

## 8. What to send back

Send `research/build/week0.md`: commit it to the repository, or paste it. Check first that it holds only numbers and
branch names (no transcripts or recordings). If a check stops at its "Fail" column, send the file as it is, with the
terminal output of that check.

Also keep `uv.lock` from step 4 and send it with `week0.md` (it pins the environment for later milestones).
