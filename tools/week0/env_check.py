"""Check 0: the Mac before M1 (macOS, chip, Python, uv, Xcode command line tools, free disk above the 10 % floor).

Needs no approval: it reads only the machine's own description and its free space. Run:
    uv run python -m tools.week0.env_check [--need models]
"""
from __future__ import annotations

import platform
import shutil
import subprocess
import sys

from tools.week0 import common, thresholds


def _out(cmd) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--need", choices=("core", "models"), default="core",
                   help="core: 1 GB; models: 4 GB more for the approved models")
    args = p.parse_args(argv)
    usage = shutil.disk_usage(common.ROOT)
    xcode = bool(_out(["xcode-select", "-p"])) if sys.platform == "darwin" else False
    v = thresholds.env(sys.platform, tuple(sys.version_info[:3]), shutil.which("uv") is not None, xcode,
                       usage.free, usage.total, args.need)
    note = ""
    if sys.platform == "darwin":
        note = f"macOS {_out(['sw_vers', '-productVersion'])}; {_out(['sysctl', '-n', 'machdep.cpu.brand_string'])}; " \
               f"{platform.machine()}"
    return common.finish(v, args, load="-", note=note)


if __name__ == "__main__":
    sys.exit(main())
