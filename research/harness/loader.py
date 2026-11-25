"""Shared Seamless Interaction feature loader (harness v1). Every architecture uses this unchanged.
Allow-list only: FAUValue (T,24) float, is_valid (T,1), transcript words, VAD segments.
Block-listed fields are refused by name before any file is opened (Principle 1; operator answer Q6).
Every .npy is loaded with allow_pickle=False."""
import json, os
import numpy as np
ROOT = "research/data/seamless/s3"
ALLOWED = {"movement/FAUValue", "movement/is_valid", "metadata/transcript", "metadata/vad"}
BLOCKED = {"emotion_scores", "emotion_valence", "emotion_arousal", "EmotionValenceToken", "EmotionArousalToken"}
DUP_COLUMN = 19  # columns 12 and 19 are byte-identical in released FAUValue (research/seamless-interaction.md); 19 is dropped
def _path(label, split, field, file_id, ext):
    if any(b in field for b in BLOCKED): raise PermissionError(f"blocked field: {field}")
    if field not in ALLOWED: raise PermissionError(f"field not on allow-list: {field}")
    return os.path.join(ROOT, label, split, field, f"{file_id}.{ext}")
def load_aus(label, split, file_id):
    """Return (T,23) float32 AU intensities (duplicate column removed) and (T,) bool validity mask."""
    a = np.load(_path(label, split, "movement/FAUValue", file_id, "npy"), allow_pickle=False)
    v = np.load(_path(label, split, "movement/is_valid", file_id, "npy"), allow_pickle=False).reshape(-1).astype(bool)
    a = np.delete(a, DUP_COLUMN, axis=1).astype(np.float32)
    return a, v
def load_jsonl(label, split, field, file_id):
    with open(_path(label, split, field, file_id, "jsonl")) as f: return [json.loads(l) for l in f]
if __name__ == "__main__":  # equation check only, not a result
    try: _path("naturalistic", "dev", "emotion_scores", "x", "npy"); print("FAIL: block list")
    except PermissionError: print("block list ok")
    a, v = load_aus("naturalistic", "dev", "V00_S0080_I00000377_P0115"); print("shape", a.shape, "valid frac", round(float(v.mean()), 3))
