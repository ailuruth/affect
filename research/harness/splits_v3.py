"""Person-disjoint splits v3: as v2, but a person is keyed by the numeric id (P0844 and P0844A are one person;
dataset README warns one individual may map to several ids; REVIEW-1 S4).
Each person (numeric id, A suffix stripped) -> split by sha256('affect-split-v3:'+person) into 70/15/15 buckets. An interaction is kept
only if all its participants fall in the same split; interactions that straddle splits are dropped (reported).
Only files with released movement features (has_imitator_movement=1)."""
import csv, hashlib, json, re
from collections import defaultdict
H = "research/harness/"
FL = "research/data/seamless/filelist.csv"; REL = "research/data/seamless/relationships.csv"
pat = re.compile(r"^(V\d+)_S(\d+)_I(\d+)_P(\d+A?)$")
def bucket(person):
    h = int(hashlib.sha256(("affect-split-v3:" + person).encode()).hexdigest(), 16) % 100
    return "train" if h < 70 else ("val" if h < 85 else "test")
rel = {(r["vendor_id"], r["session_id"].zfill(4)): r["relationship"] for r in csv.DictReader(open(REL))}
inter = defaultdict(list)
for r in csv.DictReader(open(FL)):
    if r["has_imitator_movement"] != "1": continue
    v, s, i, p = pat.match(r["file_id"]).groups(); inter[(v, s, i)].append((f"{v}_P{p.rstrip('A')}", r["file_id"], r["label"]))
files = defaultdict(list); kept = dropped = solo = 0; meta = defaultdict(lambda: defaultdict(int))
for (v, s, i), mem in inter.items():
    if len(mem) < 2: solo += 1; continue
    sp = {bucket(p) for p, _, _ in mem}
    if len(sp) > 1: dropped += 1; continue
    sp = sp.pop(); kept += 1; files[sp] += [f for _, f, _ in mem]
    meta[sp][mem[0][2]] += 1; meta[sp]["rel_" + rel.get((v, s), "unknown")] += 1
persons = {s: sorted({f.split("_")[0] + "_P" + f.rsplit("_P", 1)[1].rstrip("A") for f in files[s]}) for s in files}
out = dict(rule="person (numeric id, A suffix stripped) -> split by sha256('affect-split-v3:'+person) mod 100 (<70 train, <85 val, else test); keep interaction only if all participants share a split; straddling interactions dropped",
           interactions_total=len(inter), interactions_kept=kept, interactions_dropped_straddling=dropped, interactions_single_participant=solo,
           counts={s: dict(files=len(files[s]), persons=len(persons[s]), interactions=dict(meta[s])) for s in ("train", "val", "test")},
           files={s: sorted(files[s]) for s in ("train", "val", "test")})
json.dump(out, open(H + "splits_v3.json", "w"))
print(json.dumps({k: v for k, v in out.items() if k != "files"}, indent=1))
