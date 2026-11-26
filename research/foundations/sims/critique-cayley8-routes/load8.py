"""Loader: executes ../design-g8/checks.py up to and including the revision-8 definitions (Agent8 and helpers), skipping its
J31-J39 result loops, exactly as the author's file loads revision 7. Import-free: use `exec(open('load8.py').read())`."""
import io, os, contextlib, time
import numpy as np
_T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
P8SRC = os.path.join(HERE, "..", "design-g8", "checks.py")
_L8 = open(P8SRC).read().split("\n")
_cut = next(i for i, s in enumerate(_L8) if s.startswith("# =========================================================== J31"))
_end = next(i for i, s in enumerate(_L8) if s.startswith("'''") and i > _cut)
_src8 = "\n".join(_L8[:_cut] + ["'''", "exec(compile(BODY, 'checks_g8', 'exec'), G7)"])
G8 = {"__name__": "g8", "__file__": P8SRC}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src8, "checks_g8_defs", "exec"), G8)
G = G8["G7"]
print(f"[loaded revision 8 definitions in {time.time() - _T0:.0f} s]", flush=True)
