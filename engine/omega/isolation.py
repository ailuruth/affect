"""Isolation of the Claude Code processes and the refusal to start before the operator's answers (spec §1.8, §7.3).

The omega process drives the local Claude Code CLI on the operator's own login (never `--bare`, which needs an API
key) in streaming JSON mode. The flags are the CLI equivalents of the spec's fixed `ClaudeAgentOptions` (the Python
Agent SDK spawns the same CLI with these flags; it is not installed in this cloud session, so the omega process
speaks the CLI's stream-json protocol itself):

| ClaudeAgentOptions | CLI flag |
| setting_sources=[] | --setting-sources "" (no user, project or local settings, hooks, CLAUDE.md, output styles) |
| tools=[], allowed_tools=[] | --tools "" |
| mcp_servers={} | --strict-mcp-config --mcp-config '{"mcpServers": {}}' |
| hooks={} | (no settings are read, so no hook is loaded) |
| permission_mode="default" | --permission-mode default |
| system_prompt | --system-prompt <the constant instruction> (+ the fork line only in fallback 1) |
| model, effort | --model, --effort (operator switches; default haiku, low) |
| include_partial_messages=True | --output-format stream-json --verbose --include-partial-messages |
| resume=<canonical>, fork_session=True | --resume <canonical session id> --fork-session |
| (streaming input) | --input-format stream-json: the process starts idle (warm) and gets his message on stdin |
| no output-token cap | CLAUDE_CODE_MAX_OUTPUT_TOKENS removed from the environment (it would count thinking) |

Environment: `DISABLE_AUTOUPDATER=1` always; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` only if the operator chose
it (Q34 item 3); variables that would override the fixed options (effort, thinking budget, output cap, model) are
removed. The working directory is an empty engine-owned directory with no CLAUDE.md in it or above it.

`OmegaConfig.from_operator` refuses (engine.config.operator.Unanswered, or ValueError for an unusable value) unless
every switch of Q34 items 1, 2, 3, 7, 8, 9 is answered, the daily cap is set, and the approved text digest equals
the instruction and fork lines on disk. No Claude Code process can be spawned without an OmegaConfig.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from engine.config import operator as op
from engine.config.innate import ENTRIES
from engine.omega import lines as L

MAX_PROCESSES = int(ENTRIES["claude_max_processes"].value)
EFFORTS = ("low", "medium", "high", "xhigh", "max")
SWITCHES_NEEDED = ("send_text_to_anthropic", "send_snippets", "claude_daily_cap", "nonessential_traffic_off",
                   "account_training_use_checked", "overage_confirmed_off", "context_tokens_max",
                   "claude_text_approved", "claude_model", "effort", "pool_size")
ENV_REMOVED = ("CLAUDE_CODE_EFFORT_LEVEL", "MAX_THINKING_TOKENS", "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
               "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "ANTHROPIC_MODEL", "ANTHROPIC_SMALL_FAST_MODEL",
               "CLAUDE_CODE_SUBAGENT_MODEL")
MEMORY_FILES = ("CLAUDE.md", "CLAUDE.local.md")


def check_workdir(path: Path) -> Path:
    """An empty engine-owned directory with no CLAUDE.md in it or in any directory above it."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    path = path.resolve()
    if any(path.iterdir()):
        raise ValueError(f"the Claude working directory must be empty: {path}")
    for d in (path, *path.parents):
        for name in MEMORY_FILES:
            if (d / name).exists():
                raise ValueError(f"a {name} above the Claude working directory would reach every draft: {d / name}")
    return path


@dataclass(frozen=True)
class OmegaConfig:
    cli: tuple                     # argv prefix of the Claude Code CLI (production: the installed `claude`)
    workdir: Path
    home: Path                     # where the CLI keeps its session files (~/.claude/projects/...)
    state_dir: Path                # the call counter of the daily cap
    model: str
    effort: str
    pool_size: int
    daily_cap: int
    tokens_max: int
    send_snippets: bool
    nonessential_traffic_off: bool
    line_in_system: bool = False   # fallback 1 (week-0 `resume` check)
    extra_env: dict = field(default_factory=dict)

    @classmethod
    def from_operator(cls, cli, workdir: Path, state_dir: Path, home: Path | None = None, switches=None,
                      line_in_system: bool = False, extra_env=None) -> "OmegaConfig":
        sw = op.require(*SWITCHES_NEEDED, switches=switches)
        if sw["send_text_to_anthropic"] is not True:
            raise ValueError("send_text_to_anthropic is not True: the Claude route stays off (Q34 item 1)")
        if sw["overage_confirmed_off"] is not True:
            raise ValueError("overage_confirmed_off is not True: the Claude route stays off (Q34 item 8)")
        if not sw["account_training_use_checked"]:
            raise ValueError("account_training_use_checked is not recorded (Q34 item 7)")
        cap = sw["claude_daily_cap"]
        if isinstance(cap, bool) or not isinstance(cap, int) or cap <= 0:
            raise ValueError("claude_daily_cap must be a positive number of calls per day, set by the operator (Q34 item 2)")
        tmax = sw["context_tokens_max"]
        tmax_lim = int(ENTRIES["context_window"].value["tokens_max"])
        if isinstance(tmax, bool) or not isinstance(tmax, int) or not 0 < tmax <= tmax_lim:
            raise ValueError(f"context_tokens_max must be an integer in 1..{tmax_lim} (Q34 item 9)")
        if sw["claude_text_approved"] != L.text_digest():
            raise ValueError("the constant instruction or the fork lines differ from the text the operator approved")
        if sw["effort"] not in EFFORTS:
            raise ValueError(f"effort must be one of {EFFORTS}")
        size = sw["pool_size"]
        if isinstance(size, bool) or not isinstance(size, int) or not 1 <= size <= MAX_PROCESSES - 1:
            raise ValueError(f"pool_size must be 1..{MAX_PROCESSES - 1}")
        cli = tuple(str(x) for x in (cli if isinstance(cli, (list, tuple)) else (cli,)))
        if not cli or not cli[0]:
            raise ValueError("no Claude Code CLI given")
        state_dir = Path(state_dir)
        state_dir.mkdir(parents=True, exist_ok=True)
        return cls(cli, check_workdir(workdir), Path(home) if home is not None else Path.home(), state_dir,
                   str(sw["claude_model"]), sw["effort"], size, cap, tmax, bool(sw["send_snippets"]),
                   bool(sw["nonessential_traffic_off"]), bool(line_in_system), dict(extra_env or {}))


def command(cfg: OmegaConfig, system_prompt: str, resume_sid: str | None) -> list:
    cmd = [*cfg.cli, "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
           "--include-partial-messages", "--setting-sources", "", "--tools", "", "--strict-mcp-config",
           "--mcp-config", json.dumps({"mcpServers": {}}), "--permission-mode", "default", "--model", cfg.model,
           "--effort", cfg.effort, "--system-prompt", system_prompt]
    if resume_sid is not None:
        cmd += ["--resume", resume_sid, "--fork-session"]
    return cmd


def environment(cfg: OmegaConfig, base=None) -> dict:
    env = {k: v for k, v in (os.environ if base is None else base).items() if k not in ENV_REMOVED}
    env.update({k: v for k, v in cfg.extra_env.items() if k not in ENV_REMOVED})
    env["DISABLE_AUTOUPDATER"] = "1"
    if cfg.nonessential_traffic_off:
        env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    return env
