"""Download allow-listed Seamless feature files for a list of file_ids. Not run until the disk rule allows it
(operator: keep >= 10% of the disk free (lowered from 20% by the operator, Q11); checked before every file). Never fetches video, audio or classifier fields."""
import csv, json, os, shutil, sys, urllib.request
BASE = "https://dl.fbaipublicfiles.com/seamless_interaction"
ROOT = "research/data/seamless/s3"
ALLOW = ("movement/FAUValue", "movement/is_valid", "metadata/transcript", "metadata/vad")
EXT = {"movement/FAUValue": "npy", "movement/is_valid": "npy", "metadata/transcript": "jsonl", "metadata/vad": "jsonl"}
DENY = ("emotion", "Emotion", "mp4", "wav", "is_occluded")
FLOOR = 0.10  # operator, 2026-11-25 (Q11): floor lowered from 20% to 10%
def free_frac(path=ROOT):
    u = shutil.disk_usage(path); return u.free / u.total
def fetch(label, split, file_id):
    for field in ALLOW:
        url = f"{BASE}/{label}/{split}/{field}/{file_id}.{EXT[field]}"
        assert field in ALLOW and not any(d in url for d in DENY), url
        dst = os.path.join(ROOT, label, split, field, f"{file_id}.{EXT[field]}")
        if os.path.exists(dst): continue
        if free_frac() < FLOOR: sys.exit(f"STOP: free disk {free_frac():.1%} below the {FLOOR:.0%} floor")
        os.makedirs(os.path.dirname(dst), exist_ok=True); tmp = dst + ".part"
        urllib.request.urlretrieve(url, tmp); os.replace(tmp, dst)
if __name__ == "__main__":
    ids = json.load(open(sys.argv[1]))  # list of [label, split, file_id]
    for label, split, fid in ids: fetch(label, split, fid)
