"""CI-style runner (spec §7.6): the data guard, the label lint, then pytest. Synthetic arrays only.

Usage: python tools/ci.py            (fast suite)
       python tools/ci.py --slow     (also the full-length reference regressions, minutes)
Exit status is non-zero on the first failing step.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIRS = ("store", "dyad_cache", "dyad-cache", "research/data")
RESULTS = "research/build/results"
MAX_ARRAY_BYTES = 1024 * 1024
SKIP = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}


def data_violations(root: Path = ROOT) -> list:
    """Recorded or operator data must never be in the checkout: anything under the store, dyad-cache or data
    paths, any non-Markdown file under research/build/results/, any .npy/.npz above 1 MB."""
    root = Path(root)
    out = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts) or not p.is_file():
            continue
        r = rel.as_posix()
        if any(r == d or r.startswith(d + "/") for d in DATA_DIRS):
            out.append((r, "data path"))
        elif r.startswith(RESULTS + "/") and p.suffix != ".md":
            out.append((r, "results data"))
        elif p.suffix in (".npy", ".npz") and p.stat().st_size > MAX_ARRAY_BYTES:
            out.append((r, "array above 1 MB"))
    return sorted(out)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    bad = data_violations(ROOT)
    for r, why in bad:
        print(f"data guard: {r}: {why}")
    if bad:
        return 1
    print("data guard: clean")
    rc = subprocess.call([sys.executable, str(ROOT / "tools" / "lint_labels.py")], cwd=ROOT)
    if rc:
        return rc
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    if "--slow" in argv:
        cmd += ["-m", "slow or not slow"]
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
