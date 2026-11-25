"""Fix person-level train/val/test splits for Seamless Interaction (operator note Q11).
Rule: no person in two splits. People who share any recorded interaction are linked; each connected
component goes wholly to one split. Only files with released movement features (has_imitator_movement=1)
are considered. Assignment: components sorted by a fixed hash, greedily filled to 70/15/15 by file count."""
import csv, hashlib, json, re, sys
from collections import defaultdict
FL = "research/data/seamless/filelist.csv"
pat = re.compile(r"^(V\d+)_S(\d+)_I(\d+)_P(\d+A?)$")
rows = [r for r in csv.DictReader(open(FL)) if r["has_imitator_movement"] == "1"]
parent = {}
def find(x):
    while parent.setdefault(x, x) != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b): parent[find(a)] = find(b)
inter = defaultdict(list); bad = 0
for r in rows:
    m = pat.match(r["file_id"])
    if not m: bad += 1; continue
    v, s, i, p = m.groups(); person = f"{v}_P{p}"; key = (v, s, i)
    inter[key].append((person, r)); find(person)
for key, mem in inter.items():
    for (p, _) in mem[1:]: union(mem[0][0], p)
comp_files = defaultdict(list)
for key, mem in inter.items():
    for (p, r) in mem: comp_files[find(p)].append(r["file_id"])
comps = sorted(comp_files, key=lambda c: hashlib.sha256(("affect-split-v1:" + c).encode()).hexdigest())
total = sum(len(v) for v in comp_files.values()); target = {"train": 0.70, "val": 0.15, "test": 0.15}; got = defaultdict(int); assign = {}
for c in comps:
    n = len(comp_files[c]); s = min(target, key=lambda k: got[k] / total - target[k]); assign[c] = s; got[s] += n
persons = defaultdict(set)
for p in list(parent): persons[assign[find(p)]].add(p)
files = {s: sorted(f for c in comp_files if assign[c] == s for f in comp_files[c]) for s in target}
out = dict(rule="no person in two splits; connected components of co-occurrence; sha256('affect-split-v1:'+component_root) order; greedy 70/15/15 by file count",
           n_files_considered=len(rows), n_unparsed=bad, n_components=len(comps), largest_component_files=max(len(v) for v in comp_files.values()),
           counts={s: dict(files=len(files[s]), persons=len(persons[s])) for s in target}, files=files)
json.dump(out, open("splits_v1.json", "w"))
print(json.dumps({k: v for k, v in out.items() if k != "files"}, indent=1))
