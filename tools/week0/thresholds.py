"""The M1 branch thresholds (spec §6, "M1 branch thresholds"), applied mechanically.

Every function takes measured numbers and returns a `Verdict`: the outcome and the branch it selects. The numbers
come from INNATE `m1_thresholds` (generic, engineering; spec §3.3), never from the scripts. No function reads a
clock, a device or a file, so they are unit-tested with synthetic numbers (tests/test_week0.py).

Outcomes:
  pass     Plan A (the "Pass" column)
  branch   the "Branch" column; `selects` names the fallback
  fail     the "Fail M1 (report, stop)" column: M1 stops and the number is reported
  remeasure the table asks for a second measurement after a branch (the tracker's own instance at 5 Hz, Plan B of
           the fast tick, the memory steps); `selects` says what to apply before measuring again
  gap      the number lies in a range the spec table does not assign (e.g. a clock offset SD between 10 and 33 ms);
           recorded as it is, for the spec owner, and M1 is not complete until it is assigned
"""
from __future__ import annotations

from dataclasses import dataclass, field

from engine.config.innate import ENTRIES

TH = ENTRIES["m1_thresholds"].value
OUTCOMES = ("pass", "branch", "fail", "remeasure", "gap")


@dataclass(frozen=True)
class Verdict:
    check: str
    outcome: str
    selects: str
    measured: dict = field(default_factory=dict)

    def __post_init__(self):
        assert self.outcome in OUTCOMES, self.outcome


def _v(check, outcome, selects, **measured):
    return Verdict(check, outcome, selects, {k: v for k, v in measured.items() if v is not None})


# ------------------------------------------------------------------------------------------------ 0 environment
def env(platform: str, python: tuple, uv: bool, xcode_tools: bool, free_bytes: int, total_bytes: int,
        need: str = "core") -> Verdict:
    """The Mac before M1 (no branch row in spec §6): macOS, Python >= 3.12 and < 3.14, uv, the Xcode command line
    tools (pyworld), and free disk: what M1 needs (`need`: core 1 GB, models 4 GB more) above the operator's 10 %
    floor (Q11). Any missing item is a fail naming it."""
    lo, hi = (tuple(x) for x in TH["python"])
    floor = TH["disk_floor_fraction"] * total_bytes
    needed = TH["disk_needed_gb"]["core"] + (TH["disk_needed_gb"]["models"] if need == "models" else 0.0)
    spare_gb = (free_bytes - floor) / 1e9
    m = dict(platform=platform, python=".".join(map(str, python[:3])), uv=uv, xcode_tools=xcode_tools,
             free_gb=round(free_bytes / 1e9, 2), spare_above_floor_gb=round(spare_gb, 2), need=need)
    missing = [name for name, ok in (("macOS", platform == "darwin"), ("Python 3.12 or 3.13", lo <= tuple(python[:2]) < hi),
                                     ("uv", uv), ("Xcode command line tools", xcode_tools),
                                     (f"{needed:.0f} GB above the 10 % floor", spare_gb >= needed)) if not ok]
    if missing:
        return _v("env_check", "fail", "missing: " + ", ".join(missing), **m)
    return _v("env_check", "pass", "ready for M1", **m)


def downloads(files_hashed: int, files_expected: int, spare_gb_after: float) -> Verdict:
    """Model download (no branch row): every expected file downloaded and its SHA-256 in models.lock, with the
    disk still above the floor."""
    m = dict(files_hashed=files_hashed, files_expected=files_expected, spare_above_floor_gb=round(spare_gb_after, 2))
    if files_hashed == files_expected and files_expected > 0 and spare_gb_after >= 0:
        return _v("download_models", "pass", "models in models.lock", **m)
    return _v("download_models", "fail", "models incomplete or below the floor", **m)


# ------------------------------------------------------------------------------------------------ 1 tracker
def tracker(p99_ms: float, p99_after_branch_ms: float | None = None) -> Verdict:
    """FaceLandmarker, partner instance, per-frame p99 at full load. <= 20 ms pass; 20-30 ms: own instance to 5 Hz;
    > 30 ms after the branch: fail. Above 30 ms before the branch, the branch is applied and measured again."""
    lo, hi = TH["tracker_p99_ms"]
    if p99_ms <= lo:
        return _v("tracker", "pass", "Plan A: own-face instance at 10 Hz", p99_ms=p99_ms)
    if p99_after_branch_ms is None:
        if p99_ms <= hi:
            return _v("tracker", "branch", "own-face instance to 5 Hz", p99_ms=p99_ms)
        return _v("tracker", "remeasure", "set the own-face instance to 5 Hz and measure again", p99_ms=p99_ms)
    if p99_after_branch_ms <= hi:
        return _v("tracker", "branch", "own-face instance to 5 Hz", p99_ms=p99_ms, p99_after_branch_ms=p99_after_branch_ms)
    return _v("tracker", "fail", "partner tracker too slow with the own instance at 5 Hz",
              p99_ms=p99_ms, p99_after_branch_ms=p99_after_branch_ms)


# ------------------------------------------------------------------------------------------------ 2 echo rig
def pipeline(p99_ms: float) -> Verdict:
    """Capture-to-photon pipeline p99 (rig). <= 90 ms pass; 90-400 ms pass with warning; > 400 ms fail."""
    lo, hi = TH["pipeline_p99_ms"]
    if p99_ms <= lo:
        return _v("echo_rig", "pass", "Plan A", p99_ms=p99_ms)
    if p99_ms <= hi:
        return _v("echo_rig", "branch", "pass with warning: the ring buffer still gives 0.45 s", p99_ms=p99_ms)
    return _v("echo_rig", "fail", "0.45 s echo impossible", p99_ms=p99_ms)


# ------------------------------------------------------------------------------------------------ 3 clock
def clock(capture_time_present: bool, offset_sd_ms: float | None = None) -> Verdict:
    """`captureTime` on the local stream: present -> pass. Absent: expectedDisplayTime minus the measured offset,
    branch if the offset SD <= 10 ms; fail if > 33 ms; between: branch, pass with the SD stated."""
    lo, hi = TH["clock_offset_sd_ms"]
    if capture_time_present:
        return _v("clock", "pass", "captureTime", capture_time_present=True, offset_sd_ms=offset_sd_ms)
    if offset_sd_ms is None:
        return _v("clock", "remeasure", "captureTime absent: measure the expectedDisplayTime offset",
                  capture_time_present=False)
    if offset_sd_ms <= lo:
        return _v("clock", "branch", "expectedDisplayTime minus the measured offset", capture_time_present=False,
                  offset_sd_ms=offset_sd_ms)
    if offset_sd_ms > hi:
        return _v("clock", "fail", "no usable capture clock", capture_time_present=False, offset_sd_ms=offset_sd_ms)
    return _v("clock", "branch", "expectedDisplayTime minus offset; pass with the offset SD stated (10-33 ms, one frame or less)",
              capture_time_present=False, offset_sd_ms=offset_sd_ms)


# ------------------------------------------------------------------------------------------------ 4, 5 recognisers
STREAM_LANGUAGES = tuple(TH["stream_asr"]["languages"])


def stream_asr(language: str | None, p90_s: float, wer: float, rtf: float) -> Verdict:
    """Kyutai STT 1B. Pass: language in {en, fr}, p90 <= 0.9 s, WER <= 15 %, RTF < 0.5. Branch: p90 0.9-1.5 s with the
    rest passing -> use it, longer partial echo stated. Anything else (or another language): another fixed-delay
    streaming model meeting the row, else the utterance recogniser alone. (Fail is decided with check 5: `asr_plan`.)"""
    t = TH["stream_asr"]
    p_lo, p_hi = t["p90_s"]
    m = dict(language=language, p90_s=p90_s, wer=wer, rtf=rtf)
    if language not in STREAM_LANGUAGES:
        return _v("asr_stream", "branch", "fallback: another streaming model meeting the row, else the utterance "
                  "recogniser alone (language)", **m)
    rest_ok = wer <= t["wer"] and rtf < t["rtf"]
    if rest_ok and p90_s <= p_lo:
        return _v("asr_stream", "pass", "Plan A: Kyutai STT 1B", **m)
    if rest_ok and p90_s <= p_hi:
        return _v("asr_stream", "branch", "Kyutai STT 1B, longer partial echo (stated)", **m)
    return _v("asr_stream", "branch", "fallback: another streaming model meeting the row, else the utterance "
              "recogniser alone", **m)


def utterance_asr(rtf: float, wer: float) -> Verdict:
    """Whisper-small. Pass RTF < 0.3 and WER <= 12 %; RTF 0.3-0.5 (WER <= 12 %): pass, latency stated; fail RTF >= 0.5
    or WER > 20 %; WER in (12 %, 20 %] with RTF < 0.5: branch, pass with the WER stated."""
    t = TH["utterance_asr"]
    r_lo, r_hi = t["rtf"]
    w_lo, w_hi = t["wer"]
    if rtf >= r_hi or wer > w_hi:
        return _v("asr_utterance", "fail", "utterance recogniser fails its row", rtf=rtf, wer=wer)
    if wer > w_lo:
        return _v("asr_utterance", "branch", "pass with the WER stated (12-20 %)", rtf=rtf, wer=wer)
    if rtf < r_lo:
        return _v("asr_utterance", "pass", "Plan A: Whisper-small", rtf=rtf, wer=wer)
    return _v("asr_utterance", "branch", "pass, latency stated", rtf=rtf, wer=wer)


def asr_plan(stream: Verdict, utterance: Verdict) -> Verdict:
    """Checks 4 and 5 together: M1 fails only if the stream recogniser falls to the fallback and the utterance
    recogniser also fails its row."""
    fallback = stream.selects.startswith("fallback")
    if fallback and utterance.outcome == "fail":
        return _v("asr_plan", "fail", "no recogniser meets its row", stream=stream.outcome, utterance=utterance.outcome)
    if fallback:
        return _v("asr_plan", "branch", "utterance recogniser alone unless another streaming model meets row 4 "
                  "(longer partial echo, stated)", stream=stream.outcome, utterance=utterance.outcome)
    return _v("asr_plan", stream.outcome, stream.selects, stream=stream.outcome, utterance=utterance.outcome)


# ------------------------------------------------------------------------------------------------ 6 breathing
def _share_within(errors, limit: float) -> float:
    errors = list(errors)
    return sum(1 for e in errors if abs(e) <= limit) / len(errors) if errors else 0.0


def breath(silent_errors, holds_detected: int, holds_total: int, retest_r: float, talking_errors) -> Verdict:
    """Silent: |rate error| <= 1 /min in >= 80 % of 30-s windows, >= 9/10 holds detected, test-retest r >= 0.7.
    Talking: |error| <= 2 /min in >= 60 % of windows. Both: on. Silent only: mutual silence only. Silent fails:
    breathing off (the table's fail column; no bound depends on it)."""
    t = TH["breath"]
    s_share = _share_within(silent_errors, t["rate_err_silent"])
    t_share = _share_within(talking_errors, t["rate_err_talk"])
    hold_frac = holds_detected / holds_total if holds_total else 0.0
    m = dict(silent_share=round(s_share, 4), holds=f"{holds_detected}/{holds_total}", retest_r=retest_r,
             talking_share=round(t_share, 4))
    silent_ok = s_share >= t["share_silent"] and hold_frac >= t["holds"] and retest_r >= t["retest_r"]
    if not silent_ok:
        return _v("breath", "fail", "breathing off", **m)
    if t_share >= t["share_talk"]:
        return _v("breath", "pass", "breathing on", **m)
    return _v("breath", "branch", "breathing used in mutual silence only (sensor validity)", **m)


# ------------------------------------------------------------------------------------------------ 7, 8 ticks
def fast_tick(p99_ms: float, plan: str = "A") -> Verdict:
    """30-Hz tick p99 at full load: Plan A <= 5 ms pass; > 5 ms: Plan B (native extension), measure again;
    Plan B > 5 ms: fail."""
    lim = TH["fast_tick_p99_ms"]
    if plan == "A":
        if p99_ms <= lim:
            return _v("fast_tick", "pass", "Plan A (numpy fast process)", p99_ms=p99_ms, plan="A")
        return _v("fast_tick", "remeasure", "Plan B: native extension (spec §2.1), then measure again",
                  p99_ms=p99_ms, plan="A")
    if p99_ms <= lim:
        return _v("fast_tick", "branch", "Plan B (native extension)", p99_ms=p99_ms, plan="B")
    return _v("fast_tick", "fail", "Plan B too slow", p99_ms=p99_ms, plan="B")


def slow_tick(p99_ms: float) -> Verdict:
    """2-Hz tick p99: <= 50 ms pass; 50-200 ms: the online state step of M at 1 Hz; > 200 ms fail."""
    lo, hi = TH["slow_tick_p99_ms"]
    if p99_ms <= lo:
        return _v("slow_tick", "pass", "Plan A (2 Hz)", p99_ms=p99_ms)
    if p99_ms <= hi:
        return _v("slow_tick", "branch", "online state step of M at 1 Hz", p99_ms=p99_ms)
    return _v("slow_tick", "fail", "slow tick too slow", p99_ms=p99_ms)


# ------------------------------------------------------------------------------------------------ 9 memory
MEMORY_STEPS = ("plan_a", "kyutai_4bit", "pool_2", "pool_1")


def memory(peak_gb: float, step: str = "plan_a") -> Verdict:
    """Peak memory of all processes over the session: <= 6.0 GB pass (or the branch of the step reached); above it,
    the next step (4-bit Kyutai, then pool 2, then pool 1) and measure again; > 6.0 GB with pool 1: fail."""
    assert step in MEMORY_STEPS, step
    lim = TH["memory_gb"]
    i = MEMORY_STEPS.index(step)
    if peak_gb <= lim:
        return _v("memory", "pass" if i == 0 else "branch", "Plan A" if i == 0 else step, peak_gb=peak_gb, step=step)
    if i + 1 < len(MEMORY_STEPS):
        return _v("memory", "remeasure", f"apply {MEMORY_STEPS[i + 1]} and measure again", peak_gb=peak_gb, step=step)
    return _v("memory", "fail", "above 6.0 GB with pool 1", peak_gb=peak_gb, step=step)


# ------------------------------------------------------------------------------------------------ 10 sandbox
def sandbox(non_local_connections: int, sandbox_available: bool = True) -> Verdict:
    """A16: 0 non-loopback connections from sandboxed processes in 10 min; any is a fail. Without sandbox-exec the
    spec's fallback (a per-process check behind a pf anchor the operator approves) is an Ask: recorded as a fail."""
    if not sandbox_available:
        return _v("sandbox", "fail", "sandbox-exec unavailable: pf-anchor fallback needs the operator (Ask)",
                  sandbox_available=False)
    if non_local_connections <= TH["sandbox_connections_max"]:
        return _v("sandbox", "pass", "sandbox-exec with config/sandbox.sb", connections=non_local_connections)
    return _v("sandbox", "fail", "a sandboxed process reached the network", connections=non_local_connections)


# ------------------------------------------------------------------------------------------------ 11-15 Claude
def claude_resume(accepted_identical: int, runs: int) -> Verdict:
    """`resume` of a hand-written transcript: accepted and byte-identical in 20/20 -> pass; otherwise the fork-line
    fallback (or forks that differ only by sampling)."""
    need = TH["claude_runs"]
    if runs >= need and accepted_identical == runs:
        return _v("claude_resume", "pass", "resume of the canonical transcript", ok=accepted_identical, runs=runs)
    if runs < need:
        return _v("claude_resume", "remeasure", f"only {runs} of {need} runs", ok=accepted_identical, runs=runs)
    return _v("claude_resume", "branch", "fork-line fallback if the session file stores neither system prompt nor "
              "resumable thinking; else forks differ only by sampling", ok=accepted_identical, runs=runs)


def claude_thinking(runs_with_thinking: int, runs: int, mean_thinking_tokens: float = 0.0) -> Verdict:
    """Thinking at effort `low`: 0 in 20/20 -> pass; > 0: measured and added to the latency budget."""
    need = TH["claude_runs"]
    m = dict(runs_with_thinking=runs_with_thinking, runs=runs, mean_thinking_tokens=mean_thinking_tokens)
    if runs < need:
        return _v("claude_thinking", "remeasure", f"only {runs} of {need} runs", **m)
    if runs_with_thinking <= TH["thinking_tokens_max"]:
        return _v("claude_thinking", "pass", "no thinking at effort low", **m)
    return _v("claude_thinking", "branch", "thinking measured and added to the latency budget", **m)


def claude_latency(p90_s: float) -> Verdict:
    """First-sentence latency p90 (Haiku, effort low): <= 1.5 s pass; 1.5-3.0 s: pool 3, the deadline cap binds more
    often (stated); > 3.0 s: reported to the operator (a slower agent)."""
    lo, hi = TH["first_sentence_p90_s"]
    if p90_s <= lo:
        return _v("claude_latency", "pass", "Plan A", p90_s=p90_s)
    if p90_s <= hi:
        return _v("claude_latency", "branch", "pool 3; the deadline cap binds more often (stated)", p90_s=p90_s)
    return _v("claude_latency", "fail", "reported to the operator: a slower agent", p90_s=p90_s)


def claude_compaction(switch_found: bool, switch_off: bool) -> Verdict:
    """Auto-compaction switch: found and off -> pass; not found: detection only. Found but on: turn it off and check
    again."""
    if switch_found and switch_off:
        return _v("claude_compaction", "pass", "auto-compaction off", found=True, off=True)
    if switch_found:
        return _v("claude_compaction", "remeasure", "turn the auto-compaction switch off and check again",
                  found=True, off=False)
    return _v("claude_compaction", "branch", "detection only (spec §1.8)", found=False)


def claude_tokens(p90_tokens: float) -> Verdict:
    """Tokens per call (CLI count) at the 4,000-token window: <= 4,500 pass; > 4,500: the window is shortened until
    <= 4,000."""
    if p90_tokens <= TH["tokens_per_call"]:
        return _v("claude_tokens", "pass", "context window 4,000 tokens", tokens=p90_tokens)
    return _v("claude_tokens", "branch", "window shortened until tokens per call <= 4,000", tokens=p90_tokens)


# ------------------------------------------------------------------------------------------------ helpers
def percentile(xs, q: float) -> float:
    """Linear-interpolated percentile (numpy's default), without numpy for the light scripts."""
    v = sorted(float(x) for x in xs)
    if not v:
        raise ValueError("no samples")
    pos = (len(v) - 1) * q / 100.0
    i = int(pos)
    return v[i] if i + 1 >= len(v) else v[i] + (v[i + 1] - v[i]) * (pos - i)


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate: word-level Levenshtein distance / reference length, after lower-casing and stripping
    punctuation."""
    import re
    norm = lambda s: re.sub(r"[^\w' ]+", " ", s.lower()).split()
    r, h = norm(reference), norm(hypothesis)
    if not r:
        raise ValueError("empty reference")
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hw in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw))
        prev = cur
    return prev[-1] / len(r)
