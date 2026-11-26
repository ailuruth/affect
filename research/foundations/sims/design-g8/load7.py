"""Loads the revision-7 engine exactly as built (../design-g7/checks.py), skipping only its own result loops
(J17-J19, J21, J22-J30), the same way the revision-7 routes critic's posture7.py does. Definitions are unchanged."""
import io, os, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
P7SRC = os.path.join(HERE, "..", "design-g7", "checks.py")
L = open(P7SRC).read().split("\n")
_k = ("# =========================================================== J17", "# =========================================================== agent part",
      "# =========================================================== J21", "# =========================================================== the revision-7 agent",
      "# =========================================================== J22", "cases = [")
idx = {k: next(i for i, s in enumerate(L) if s.startswith(k)) for k in _k}
src = "\n".join(L[:idx[_k[0]]] + L[idx[_k[1]]:idx[_k[2]]] + L[idx[_k[3]]:idx[_k[5]]])
G7 = {"__name__": "g7", "__file__": P7SRC}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "checks_g7_parts", "exec"), G7)
