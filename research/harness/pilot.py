"""Fix the pilot subset (operator: a few hundred interactions first). 300 train + 150 val interactions from splits_v3.json,
chosen by sha256('affect-pilot-v2:'+interaction) order (not stratified; the resulting mix is reported).
Test split untouched. The URL split (dev/train/test of the dataset) comes from filelist.csv, not from our split."""
import csv, hashlib, json, re
from collections import defaultdict
H = "research/harness/"
S = json.load(open(H + "splits_v3.json"))
FL = {r["file_id"]: r for r in csv.DictReader(open("research/data/seamless/filelist.csv"))}
pat = re.compile(r"^(V\d+_S\d+_I\d+)_P")
out = []; summary = {}
for split, n in (("train", 300), ("val", 150)):
    inter = defaultdict(list)
    for f in S["files"][split]: inter[pat.match(f).group(1)].append(f)
    keys = sorted(inter, key=lambda k: hashlib.sha256(("affect-pilot-v2:" + k).encode()).hexdigest())[:n]
    for k in keys:
        for f in inter[k]: out.append([FL[f]["label"], FL[f]["split"], f])
    summary[split] = dict(interactions=len(keys), files=sum(len(inter[k]) for k in keys),
                          improvised=sum(FL[inter[k][0]]["label"] == "improvised" for k in keys))
json.dump(out, open(H + "pilot_v2.json", "w")); print(json.dumps(summary))

val = set(S["files"]["val"])
e3 = sorted({pat.match(f).group(1) for _, _, f in out if f in val}, key=lambda k: hashlib.sha256(("affect-e3-v2:" + k).encode()).hexdigest())[:20]
json.dump(e3, open(H + "e3_subset_v2.json", "w")); print("e3 subset", len(e3))
