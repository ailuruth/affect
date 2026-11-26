"""Check 0b: download the four M1 models (after Q34 item 4), check free space first, write their SHA-256 into
engine/config/models.lock (A17).

Refuses until `downloads_approved` (Q34 item 4) is answered with models approved. Each download is preceded by a
free-space check: nothing is written if it would leave less than the operator's 10 % floor. After the download
every engine process runs offline (`hub_offline_after_download`, Q34 item 10). Run:
    uv run python -m tools.week0.download_models
The model files go to $AFFECT_MODELS_DIR (default ~/affect-models), outside the repository.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

from tools.week0 import common, thresholds

MODELS_DIR = Path(os.environ.get("AFFECT_MODELS_DIR", Path.home() / "affect-models"))
MODELS_LOCK = common.ROOT / "engine" / "config" / "models.lock"
# (name, kind, source, approximate size in GB). Hub ids are the operator's to confirm before running (handoff §6).
MODELS = (
    ("mediapipe_tasks_vision_0.10.35", "npm", "https://registry.npmjs.org/@mediapipe/tasks-vision/-/tasks-vision-0.10.35.tgz", 0.02),
    ("face_landmarker", "url", "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task", 0.01),
    ("kyutai_stt_1b_en_fr", "hub", "kyutai/stt-1b-en_fr-mlx", 2.0),
    ("whisper_small", "hub", "mlx-community/whisper-small-mlx", 0.5),
    ("all_minilm_l6_v2", "hub", "sentence-transformers/all-MiniLM-L6-v2", 0.1),
)


def spare_gb(path: Path) -> float:
    u = shutil.disk_usage(path if path.exists() else path.parent)
    return (u.free - thresholds.TH["disk_floor_fraction"] * u.total) / 1e9


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=60) as r, tmp.open("wb") as f:
        shutil.copyfileobj(r, f)
    tmp.replace(dest)


def download(name: str, kind: str, source: str, dest_root: Path) -> Path:
    dest = dest_root / name
    if kind == "hub":
        hub = common.lazy("huggingface_hub", "uv sync --extra engine")
        hub.snapshot_download(repo_id=source, local_dir=str(dest))
    elif kind == "npm":
        tgz = dest / "package.tgz"
        _fetch(source, tgz)
        with tarfile.open(tgz) as t:
            t.extractall(dest, filter="data")
        tgz.unlink()
    else:
        _fetch(source, dest / Path(source).name)
    return dest


def main(argv=None) -> int:
    p = common.parser(__doc__)
    args = p.parse_args(argv)
    ok = common.require_approval("downloads_approved", "hub_offline_after_download")
    if not ok["downloads_approved"].get("models"):
        raise common.Refused("the operator's answer to Q34 item 4 does not approve the models")
    common.require_mac()
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ.pop("HF_HUB_OFFLINE", None)               # the one online step (spec §7.5); every other process is offline
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for name, kind, source, size in MODELS:
        left = spare_gb(MODELS_DIR)
        if left < size:
            raise common.Refused(f"{name} needs about {size} GB; only {left:.2f} GB above the 10 % floor")
        if args.dry_run:
            print(f"would download {name} ({kind}: {source}), about {size} GB; {left:.2f} GB spare")
            continue
        print(f"downloading {name} ...")
        download(name, kind, source, MODELS_DIR)
    if args.dry_run:
        return 0
    files = {}
    for f in sorted(MODELS_DIR.rglob("*")):
        if f.is_file() and ".cache" not in f.parts:
            files[f.relative_to(MODELS_DIR).as_posix()] = sha256(f)
    MODELS_LOCK.write_text(json.dumps({"files": files, "root": "$AFFECT_MODELS_DIR",
                                       "note": "SHA-256 of every model file, written by tools/week0/download_models.py (A17)"},
                                      sort_keys=True, indent=1) + "\n")
    got = {name for name, *_ in MODELS if (MODELS_DIR / name).is_dir() and any((MODELS_DIR / name).rglob("*"))}
    v = thresholds.downloads(len(got), len(MODELS), spare_gb(MODELS_DIR))
    return common.finish(v, args, load="-", note=f"{len(files)} files hashed")


if __name__ == "__main__":
    sys.exit(main())
