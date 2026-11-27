"""The Claude-facing text besides the constant instruction (spec §1.8; reviewed by the operator at M6).

- The three fork lines ("attend to" lines): one per fork, the same line every turn, appended to his message (or, in
  fallback 1, to that fork's system prompt). They name what to attend to, never a value of the state.
- The snippet template: the header of a retrieved passage and the speaker names in it.
- `text_digest`: SHA-256 of the instruction and of all these constants. The operator switch `claude_text_approved`
  must hold this digest (he read and approved the text); `engine.omega.pool.OmegaConfig` refuses otherwise.

The label lint allowlists only engine/omega/instruction.txt and the three LINE_* constants below (spec §7.4).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

INSTRUCTION_PATH = Path(__file__).with_name("instruction.txt")

LINE_WHAT_HE_SAID = "(Attend to what he said.)"
LINE_HOW_HE_SEEMS = "(Attend to how he seems to feel, from his words.)"
LINE_REMINDS = "(Attend to what this reminds you of.)"
LINES = (LINE_WHAT_HE_SAID, LINE_HOW_HE_SEEMS, LINE_REMINDS)

SNIPPET_HEADER = "[an earlier conversation]"
SNIPPET_END = "[end of the earlier conversation]"
SPEAKER_HIS = "He"
SPEAKER_AGENT = "You"


def instruction_bytes() -> bytes:
    """The constant instruction, byte-stable for the engine's lifetime (read once per process)."""
    return INSTRUCTION_PATH.read_bytes()


def instruction() -> str:
    return instruction_bytes().decode("utf-8").rstrip("\n")


def text_digest() -> str:
    h = hashlib.sha256()
    for part in (instruction_bytes(), *[x.encode("utf-8") for x in
                                        (*LINES, SNIPPET_HEADER, SNIPPET_END, SPEAKER_HIS, SPEAKER_AGENT)]):
        h.update(len(part).to_bytes(8, "big"))
        h.update(part)
    return h.hexdigest()
