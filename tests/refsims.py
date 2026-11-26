"""Reference definitions read verbatim from research/foundations/sims (for regression tests only).

Each loader takes the exact source text of the reference function(s) out of the sims file and executes only that
text, with the sample rate given, so the tests compare the engine with the reference's own formula. Constructed
signals; never evidence about behaviour.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.signal import lfilter

ROOT = Path(__file__).resolve().parents[1]
SIMS = ROOT / "research" / "foundations" / "sims"


def _lines(path: Path, start: str, count: int = 1) -> str:
    src = path.read_text().splitlines()
    i = next(n for n, ln in enumerate(src) if ln.startswith(start))
    return "\n".join(src[i:i + count]) + "\n"


def g9(fs: float = 10.0) -> dict:
    """lp, delay and fast of design-g9/ledger_lag120.py, executed at sample rate fs."""
    p = SIMS / "design-g9" / "ledger_lag120.py"
    src = (_lines(p, "def lp(x, tau)") + _lines(p, "def delay(x, n)", 2) + _lines(p, "def fast(u, G, dl=0.45)"))
    ns = {"np": np, "lfilter": lfilter, "fs": fs}
    exec(src, ns)
    return ns


def g9_partners() -> dict:
    """The seed-910 partners u, u2 of design-g9 (2 h at 10 Hz), built by the reference's own code."""
    p = SIMS / "design-g9" / "ledger_lag120.py"
    src = p.read_text()
    body = src[src.index("def lp(x, tau)"):src.index('print(f"partners')]
    ns = {"np": np, "lfilter": lfilter, "fs": 10.0, "os": __import__("os")}
    exec(body, ns)
    return ns


def g5(fs: float) -> dict:
    """lp, the cone trace constants TAU_M, F_M, F_BI and bp of design-g5/checks.py, at sample rate fs."""
    p = SIMS / "design-g5" / "checks.py"
    src = (_lines(p, "def lp(x, tau, fs):", 2) + _lines(p, "TAU_M = ") + _lines(p, "F_M = ") + _lines(p, "F_BI = ")
           + _lines(p, "def bp(x): return lp(x, 20.0, fs) - lp(x, 90.0, fs)"))
    ns = {"np": np, "lfilter": lfilter, "fs": fs}
    exec(src, ns)
    return ns


def g7_gate() -> dict:
    """KN and phi of design-g7/checks.py, and the evaluation formula of its fitted gate (fit_gate's return line)."""
    p = SIMS / "design-g7" / "checks.py"
    src = _lines(p, "KN = ") + _lines(p, "def phi(X):", 5)
    ns = {"np": np}
    exec(src, ns)
    ret = _lines(p, "    return lambda x, b=b, m_ref=m_ref, drop=drop:").strip()
    ns["gate_expr"] = ret[len("return "):]
    return ns
