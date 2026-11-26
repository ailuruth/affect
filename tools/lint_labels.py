"""The label lint (spec §7.4): no affect label below Claude.

Scans engine/, eval/, web/, tools/ and tests/: every file's name and directory names, and every file's whole text
(Python: also the decoded value of every string literal, so escapes cannot hide a word). Scanning the whole text
covers identifiers, attributes, keyword arguments, dict keys, strings, f-string parts, comments and docstrings in
Python; identifiers, strings and comments in JavaScript and HTML; keys and values in JSON, YAML, TOML and .lock.

Tokenisation: split on any non-alphanumeric character (so _ - . / whitespace and punctuation), then camelCase and
PascalCase at each lower-to-upper change, acronym ends and letter-digit boundaries; lower-case. Each token is
fullmatched against the stem table in tests/lint_stems.py.

Allowlist (by path, reviewed): engine/omega/instruction.txt; the fork-line constants in engine/omega/lines.py;
DENY_FIELDS in engine/dyads/loader.py; tests/lint_stems.py. Documentation .md files outside the scanned trees are
not scanned at all. Usage: python tools/lint_labels.py [root]  (exit 1 on any hit).
"""
from __future__ import annotations

import ast
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNED = ("engine", "eval", "web", "tools", "tests")
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".git", ".venv", "node_modules"}
BINARY_SUFFIXES = {".npy", ".npz", ".pyc", ".png", ".jpg", ".wasm", ".task", ".bin", ".onnx"}
ALLOW_FILES = {"engine/omega/instruction.txt", "tests/lint_stems.py"}
ALLOW_CONSTANTS = {"engine/omega/lines.py": {"LINE_WHAT_HE_SAID", "LINE_HOW_HE_SEEMS", "LINE_REMINDS"},
                   "engine/dyads/loader.py": {"DENY_FIELDS"}}

_CAMEL = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+")


def tokens(text: str) -> list:
    out = []
    for part in re.split(r"[^0-9A-Za-z]+", text):
        if part:
            out += [t.lower() for t in _CAMEL.findall(part)]
    return out


def _load_stems(root: Path):
    spec = importlib.util.spec_from_file_location("lint_stems", root / "tests" / "lint_stems.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_STEMS_MOD = _load_stems(ROOT)
_STEM_RE = re.compile("|".join(f"(?:{s})" for s in _STEMS_MOD.STEMS))


def hits_in(text: str) -> list:
    return sorted({t for t in tokens(text) if _STEM_RE.fullmatch(t)})


def _blank_constants(src: str, names: set) -> str:
    """Blank out the source of module-level assignments to the allowlisted constant names."""
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    spans = []
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            tg = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id in names for t in tg):
                spans.append((node.lineno, node.end_lineno))
    for a, b in spans:
        for i in range(a - 1, b):
            lines[i] = "\n"
    return "".join(lines)


def _python_strings(src: str) -> str:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return ""
    return "\n".join(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str))


def scan_file(path: Path, rel: str) -> list:
    out = [(rel, "name", h) for h in hits_in(rel)]
    if rel in ALLOW_FILES or path.suffix in BINARY_SUFFIXES:
        return out
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return out + [(rel, "unreadable", "binary file in a scanned tree")]
    if rel in ALLOW_CONSTANTS:
        text = _blank_constants(text, ALLOW_CONSTANTS[rel])
    out += [(rel, "text", h) for h in hits_in(text)]
    if path.suffix == ".py":
        out += [(rel, "string", h) for h in hits_in(_python_strings(text))]
    return sorted(set(out))


def scan(root: Path = ROOT) -> list:
    root = Path(root)
    out = []
    for top in SCANNED:
        base = root / top
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
                continue
            rel = p.relative_to(root).as_posix()
            if p.is_dir():
                out += [(rel, "dir", h) for h in hits_in(p.name)]
            elif p.is_file():
                out += scan_file(p, rel)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = Path(argv[0]) if argv else ROOT
    hits = scan(root)
    for rel, where, tok in hits:
        print(f"{rel}: {where}: forbidden token {tok!r}")
    print(f"label lint: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
