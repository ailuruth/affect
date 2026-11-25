# Anthropic 2026: Claude Code CLI (`claude -p`) and Claude Agent SDK for Python, what a caller can control

## Citation

Anthropic. Claude Code documentation, code.claude.com/docs/en/: "Agent SDK reference - Python" (agent-sdk/python), "CLI reference" (cli-reference), "Run Claude Code programmatically" (headless), "Agent SDK overview" (agent-sdk/overview), "Streaming input" (agent-sdk/streaming-vs-single-mode), "Model configuration" (model-config), "Environment variables" (env-vars), "Hooks reference" (hooks). Fetched as Markdown on 2026-11-25. Local CLI checked: Claude Code 2.1.332 (`claude --help`). The Python SDK is not installed on this Mac; its reference page was read instead.

## What was read

- Read in full: the `ClaudeSDKClient` class and methods, `ClaudeAgentOptions` (every field), `ThinkingConfig`, `EffortLevel`, `ResultMessage`, `StreamEvent`, the interrupt example (agent-sdk/python, lines 498-1790 of the Markdown); model-config "Available models", "Adjust effort level" through "Where you can't turn thinking off"; headless "Stream responses", "Customize the system prompt", "Continue conversations", bare-mode auth; hooks "Add context for Claude" and "Decision control"; env-vars rows for `CLAUDE_CODE_EFFORT_LEVEL`, `MAX_THINKING_TOKENS`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`; the full `claude --help` output.
- Searched all fetched pages for `temperature`, `top_p`, `logprob`, `stop_sequence`, `max_tokens`, `sampling`, `deterministic`. None of them names a sampling parameter or log-probabilities.
- Not read: the TypeScript reference, permissions, sessions, plugins and MCP pages beyond what is cited here.

## What is controllable, exactly

| Lever | CLI (`claude -p`) | Python SDK | Granularity | Is it text that Claude reads? |
|---|---|---|---|---|
| Model | `--model`, `--fallback-model` | `model`, `fallback_model`, `client.set_model()` mid-session | discrete: aliases `haiku`, `sonnet`, `opus`, `fable`, or full IDs (e.g. `claude-opus-5-5`) | no |
| Effort (thinking depth) | `--effort low\|medium\|high\|xhigh\|max`; env `CLAUDE_CODE_EFFORT_LEVEL` (highest precedence) | `effort` | 5 discrete levels; default `medium` on Opus/Sonnet/Haiku 5.5 | no (but "ultrathink" in the prompt is text) |
| Fixed thinking budget | env `MAX_THINKING_TOKENS` | `thinking={"type":"enabled","budget_tokens":N}` | integer, **but ignored on adaptive-reasoning models** (see below) | no |
| Thinking display | — | `thinking.display = "summarized"\|"omitted"` | — | no |
| Max output tokens | env `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | via `env` | integer; truncates, does not shape | no |
| System prompt | `--system-prompt[-file]`, `--append-system-prompt[-file]` | `system_prompt` (string, preset+append, custom, file) | free text | **yes** |
| Context contents | the prompt; `--resume`, `--continue`, `--fork-session`; resume from a `.jsonl` transcript path | `query()` prompt; streaming input with images; `resume`, `fork_session`, `resume_session_at` (branch from an earlier message) | any text, images | **yes** (images: not words or numbers) |
| Hook-injected context | settings hooks | `hooks` | `additionalContext` string, wrapped as a system reminder | **yes** |
| Tools available | `--tools`, `--allowedTools`, `--disallowedTools`, `--mcp-config` | `tools`, `allowed_tools`, `disallowed_tools`, `mcp_servers`, `client.toggle_mcp_server()` mid-session, `can_use_tool` callback | set membership, per call or mid-session | tool names and descriptions are text; a denial is returned as text |
| Turn limit, spend limit | `--max-turns` (print mode; in cli-reference, not in `--help`), `--max-budget-usd` | `max_turns`, `max_budget_usd`, `task_budget` | integer / dollars / tokens | no |
| Structured output | `--json-schema` | `output_format` | schema | the schema is text |
| Streaming | `--output-format stream-json --verbose --include-partial-messages` | `include_partial_messages=True` yields `StreamEvent` (raw API deltas) | token-chunk deltas | — |
| Interruption | SIGTERM | `client.interrupt()` (streaming mode); `ResultMessage.terminal_reason = "aborted_streaming"` | any time | an interrupted turn stays in the session history |
| Timing | when the caller sends | when the caller sends | continuous | no, unless timestamps are shown |
| Parallel samples | N separate processes | N separate `query()` calls or forks | integer N | no |
| Telemetry back | `result`, `usage`, `duration_ms` | `ResultMessage`: `duration_ms`, `duration_api_ms`, `usage`, `model_usage[...]["thinkingTokens"]`, `stop_reason`, `total_cost_usd` | — | — |

### What is not controllable

- **No sampling parameters.** No temperature, top-p, top-k or stop sequences in either interface. Diversity across N drafts comes only from the model's default sampling and from varying the context.
- **No log-probabilities, logits, embeddings or activations.** `StreamEvent.event` carries the raw API stream deltas (text and thinking deltas), not probabilities. So no token-level reweighting (FUDGE, GeDi, PPLM) and no KL estimate from log-probabilities.
- **No assistant prefill is documented.** A caller can resume a session or a transcript file, or branch at an earlier message (`resume_session_at`), but no documented option makes Claude continue a partial assistant message. Continuing an accepted prefix means passing it back as context, which Claude reads as text. (Resuming from a hand-written `.jsonl` transcript might allow it; undocumented, not tested.)
- **Thinking budget in tokens is not a lever on current models.** Model-config: "Fable models, Sonnet 5 and later, Haiku 5.5, and Opus 4.7 and later always use adaptive reasoning." Env-vars: for a positive `MAX_THINKING_TOKENS`, "Claude Code ignores the number itself on adaptive reasoning models". And: "You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5, or the Fable models... the model decides per step how much to think based on the effort level." A fixed token budget works only on Opus 4.6 and Sonnet 4.6 with `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. On current models, depth of thought has five settings. The docs add: "The effort scale is calibrated per model, so the same level name does not represent the same underlying value across models."
- **Effort changes apply at turn boundaries**, not mid-generation ("the next message you send runs at that level").

### Authentication under the subscription constraint

- Bare mode (`--bare`) "never reads OAuth credentials"; it needs `ANTHROPIC_API_KEY`. So the engine must not use `--bare`.
- The SDK spawns the local CLI, which uses the operator's login. The overview warns: "Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." This is about products for others. The operator running the engine for themselves on their own login is the case here (my reading; the page does not address it directly).
- `total_cost_usd` and `max_budget_usd` are client-side estimates. On a subscription they track usage, not billing.

## Evidence

This note is documentation, not an experiment. The one relevant result in this project: P1 (research/predictions.md) put body values into the context as unnamed numbers and found 0 of 5 vs 0 of 5 replies acknowledged a 3-day absence. The context channel, used with numbers, did nothing measurable.

## Available through `claude -p` / Agent SDK?

This note is the answer. The admissible levers under Principle 4 (no numbers, labels or state words in the prompt) are:

1. **Which model** answers (discrete, per call or mid-session).
2. **Effort** (five levels, per call; per-model calibration).
3. **When** Claude is called, and **whether** it is called at all.
4. **How long** it may speak (output-token cap; truncation only).
5. **Interrupting** a streamed reply, at any chunk.
6. **Selecting** among N independently sampled drafts, outside Claude.
7. **Which verbatim context** is present: which past episodes, which earlier turns (branching), which images.
8. **Which tools exist** for Claude in this turn (affordances), and which calls are denied.

Levers 7 and 8 and the system prompt put text in front of Claude. They are admissible only if the text is not a description of the state (see synthesis).

## What it implies for the interface theory

- **The interface is coarse in every dimension except time and selection.** Model and effort are discrete with 3-5 settings each. The output cap truncates. Only call timing, interruption timing and draft selection take a continuous or many-valued state input.
- **Effort is the only documented lever that changes Claude's processing without text.** It changes how much it thinks, not what it attends to. Five levels, calibrated per model, applied at turn start. It is a gain on deliberation. This matches the brief's "thinking budget" coupling, but on current models that budget is a 5-level effort, not a token count. Test it before relying on it: does `low` vs `max` change the content of a reunion reply at all, or only its length and latency?
- **Model switching mid-session** (`set_model`) is a second processing lever. It changes the whole policy at once, in a jump. As a state-dependent switch (e.g. Haiku under high load, Opus when settled) it is a discrete gate, not a graded coupling.
- **Interruption is the finest-grained black-box lever.** With `include_partial_messages`, the engine sees text deltas as they arrive and can stop at any chunk. What it cannot do is resume the same generation from the stopped point except by passing the accepted text back as context. Interruption gives a stopping-time channel: the state can decide when a reply ends. The interrupted turn stays in the session history; for the next call, start from a fork taken before the interrupted turn.
- **Images are a non-verbal context channel.** Streaming input accepts image blocks. A rendered image of the agent's own face carries state without words or numbers, as in efference-memory.md §2.5. It still asks Claude to read the state, through perception rather than a label. Whether that is allowed under Principle 4 is a decision for the operator: Claude would be naming what it sees, which is its job in the brief.
- **Everything else is text.** Hooks, the system prompt, tool descriptions and denial messages are words. A state-dependent system prompt with no state words in it ("be brief") is still an instruction chosen by state. It is a coded label.
- **Telemetry closes a loop without text.** `duration_ms`, output tokens and `thinkingTokens` per call tell the engine how Claude processed a turn. These can feed the engine's state (for example, a long hesitation by Claude is an interoceptive event for the agent), which gives a two-way coupling with no words in either direction.

## Verdict

Adopt as the fixed constraint set. No sampling knobs, no log-probabilities, no prefill, and only five effort levels on current models. Any interface theory must be stated in terms of model choice, effort, timing, stopping, selection among N drafts, verbatim context selection, and tool affordances.
