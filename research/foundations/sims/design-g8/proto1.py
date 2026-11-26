import time, os; t0=time.time()
import numpy as np
__file__ = os.path.abspath("load7.py"); exec(open("load7.py").read())
print("loaded", time.time()-t0)
G5=G7["G5"]; g6=G7["g"]
print(G5["RD_CH"], G5["RD_L"]); print({k:v for k,v in G5["PI0"].items()})
print("REF", G7["REF"]); print("REF_SD", G7["REF_SD"])
