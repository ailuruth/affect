"""The feature and transcript store (spec §1.9; P7, D70, A12). Features only: no raw audio or video is ever written.

Layout under the store root (never inside the checkout; tools/ci.py's data guard refuses a `store/` path there):
  sessions/<sid>/manifest.json         session id, identity, t0, t_end, rows and widths per stream, A5/A14 flags,
                                        whether replay consolidated it
  sessions/<sid>/<stream>.f16           one registered stream (INNATE `store_schemas`), float16, row-major,
                                        memory-mapped by readers; a file never exceeds its schema's size
  sessions/<sid>/transcript.jsonl       his recognised lines and the agent's chosen replies, with word timestamps
  sessions/<sid>/events.jsonl           the engine's own events (drop/rise events, turn events, reports)
  sessions/<sid>/omega.jsonl            Ω records (drafts, which won, timings, telemetry)
  consolidated/                         what replay keeps: learned weights, per-person latches, slot snippet lines
  live.lock / replay.lock               a live session and replay never run together (spec §2.4)
  quarantine/                           files A12 moved out of the store (the operator is told)

The writer's API has no audio or image buffer type: `append` takes only floating-point arrays of a registered
stream's width (an int16 PCM buffer, a uint8 frame, bytes or a 3-D image are refused before anything is written);
text goes in only as `TranscriptText` or as records whose keys and value types are fixed. `check_a12` scans the
directories nightly and at start: only registered file names, no media magic number, no file above its schema size.
A live session opens only after the operator answered Q34 item 6 (`feature_retention_days`, `keep_slot_snippets`).
"""
from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from engine.config.innate import ENTRIES
from engine.config.operator import require
from engine.state.types import TranscriptText, restored_text

SCHEMAS = ENTRIES["store_schemas"].value
LIMITS = ENTRIES["store_limits"].value
MAGIC = tuple(m.encode("latin-1") for m in LIMITS["magic"])
SESSION_MAX_S = float(LIMITS["session_max_s"])
LINE_MAX = int(LIMITS["text_line_max_bytes"])
SNAPSHOT_STREAMS = frozenset({"state_T", "state_F", "state_K"})      # width declared at the first append (<= dims)
TEXT_FILES = ("transcript.jsonl", "events.jsonl", "omega.jsonl")
CONSOLIDATED_FILES = ("learned.npz", "learned_last_valid.npz", "persons.json", "snippets.jsonl", "slot_refs.json",
                      "replay_log.jsonl", "retention_log.jsonl")
BODY_COLUMNS = ("E", "A", "V", "K", "P", "I", "D", "Dp", "Dp_word", "h_word", "V_F", "drop_amp")
assert len(BODY_COLUMNS) == SCHEMAS["body"]["dims"]

EVENT_KINDS = frozenset({"drop_event", "rise_event", "turn_event", "report"})
EVENT_KEYS = {"kind": str, "t": float, "amp": float, "term": str, "credited": bool, "separated": bool, "utt": int,
              "of": int, "turn": str}
EVENT_TERMS = frozenset({"Dp_word", "K", "P", "I", "h_word"})
TURN_KINDS = frozenset({"his_utterance_end", "session_start", "agent_utterance_start", "agent_utterance_end"})
OMEGA_KEYS = {"t": float, "drafts": list, "winner": int, "timings": dict, "telemetry": dict}


class StoreRefused(ValueError):
    """The store refused a write (unregistered stream, media-like buffer, wrong width, oversize, bad record)."""


def max_rows(stream: str) -> int:
    return int(SCHEMAS[stream]["hz"] * SESSION_MAX_S) + 1


def max_bytes(stream: str) -> int:
    return max_rows(stream) * int(SCHEMAS[stream]["dims"]) * 2


def _features(stream: str, a, width: int | None):
    if stream not in SCHEMAS:
        raise StoreRefused(f"no registered stream {stream!r} (the store holds features only)")
    if isinstance(a, (bytes, bytearray, memoryview, str)) or not isinstance(a, (np.ndarray, list, tuple, float, int)):
        raise StoreRefused(f"{stream}: only numeric feature arrays are stored, not {type(a).__name__}")
    arr = np.asarray(a)
    if arr.dtype.kind != "f":
        raise StoreRefused(f"{stream}: dtype {arr.dtype} refused (features are floating point; no PCM or pixels)")
    if arr.ndim == 1:
        arr = arr[None, :]
    dims = int(SCHEMAS[stream]["dims"])
    w = dims if width is None else width
    if arr.ndim != 2 or arr.shape[1] != w:
        raise StoreRefused(f"{stream}: shape {arr.shape} refused (rows x {w})")
    if not np.all(np.isfinite(arr)):
        raise StoreRefused(f"{stream}: non-finite values")
    return arr.astype(np.float16)


def _line(obj) -> bytes:
    b = (json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    if len(b) > LINE_MAX:
        raise StoreRefused("text record above the line cap")
    return b


def _check_record(rec: dict, keys: dict, what: str) -> None:
    for k, v in rec.items():
        if k not in keys:
            raise StoreRefused(f"{what}: key {k!r} is not in its schema")
        want = keys[k]
        ok = isinstance(v, bool) if want is bool else (
            isinstance(v, (int, float)) and not isinstance(v, bool) if want is float else isinstance(v, want)
            and not (want is int and isinstance(v, bool)))
        if not ok:
            raise StoreRefused(f"{what}: {k} must be {want.__name__}")


class SessionWriter:
    """Writes one live session. Made by `Store.open_session` (which takes the live lock)."""

    def __init__(self, store: "Store", sid: str, identity: str, t0: float):
        self.store, self.sid = store, sid
        self.dir = store.root / "sessions" / sid
        self.dir.mkdir(parents=True, exist_ok=False)
        self.manifest = {"session": sid, "identity": str(identity), "t0": float(t0), "t_end": None, "rows": {},
                         "widths": {}, "flags": {"A5": False, "A14": False}, "replayed": False, "lines": 0}
        self._write_manifest()
        self.closed = False

    def _write_manifest(self) -> None:
        tmp = self.dir / "manifest.json.tmp"
        tmp.write_text(json.dumps(self.manifest, sort_keys=True))
        os.replace(tmp, self.dir / "manifest.json")

    def append(self, stream: str, a) -> None:
        """Append rows of one registered feature stream (float16 on disk)."""
        if self.closed:
            raise StoreRefused("session closed")
        width = self.manifest["widths"].get(stream)
        if stream in SNAPSHOT_STREAMS and width is None:
            arr0 = np.asarray(a) if not isinstance(a, (bytes, bytearray, memoryview, str)) else None
            if arr0 is None:
                raise StoreRefused(f"{stream}: only numeric feature arrays are stored")
            width = int(arr0.shape[-1]) if arr0.ndim in (1, 2) else -1
            if not 0 < width <= int(SCHEMAS.get(stream, {"dims": 0})["dims"]):
                raise StoreRefused(f"{stream}: snapshot width {width} refused")
        arr = _features(stream, a, width if stream in SNAPSHOT_STREAMS else None)
        rows = self.manifest["rows"].get(stream, 0) + arr.shape[0]
        if rows > max_rows(stream):
            raise StoreRefused(f"{stream}: above the schema size of one session")
        with open(self.dir / f"{stream}.f16", "ab") as f:
            f.write(arr.tobytes(order="C"))
        self.manifest["rows"][stream] = rows
        self.manifest["widths"][stream] = int(arr.shape[1])
        self._write_manifest()

    def append_transcript(self, entry: TranscriptText, words=()) -> int:
        """One transcript line (his recognised words or the agent's chosen reply) with (word, t_end) pairs."""
        if not isinstance(entry, TranscriptText):
            raise StoreRefused("the transcript takes only TranscriptText")
        ws = [[str(w), float(t)] for w, t in words]
        with open(self.dir / "transcript.jsonl", "ab") as f:
            f.write(_line({"speaker": entry.speaker, "text": entry.text, "t": entry.t, "words": ws}))
        self.manifest["lines"] += 1
        self._write_manifest()
        return self.manifest["lines"] - 1

    def append_event(self, **rec) -> None:
        _check_record(rec, EVENT_KEYS, "event")
        if rec.get("kind") not in EVENT_KINDS or "t" not in rec:
            raise StoreRefused("event: kind and t required")
        if "term" in rec and rec["term"] not in EVENT_TERMS:
            raise StoreRefused("event: unknown term")
        if "turn" in rec and rec["turn"] not in TURN_KINDS:
            raise StoreRefused("event: unknown turn kind")
        with open(self.dir / "events.jsonl", "ab") as f:
            f.write(_line(rec))

    def append_omega(self, **rec) -> None:
        _check_record(rec, OMEGA_KEYS, "omega record")
        if not all(isinstance(d, str) for d in rec.get("drafts", [])):
            raise StoreRefused("omega record: drafts are text")
        for k in ("timings", "telemetry"):
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in rec.get(k, {}).values()):
                raise StoreRefused(f"omega record: {k} are numbers")
        with open(self.dir / "omega.jsonl", "ab") as f:
            f.write(_line(rec))

    def flag(self, aid: str) -> None:
        """An A5 or A14 failure: replay skips this session (spec §1.9, §4.3)."""
        if aid not in self.manifest["flags"]:
            raise StoreRefused(f"no flag {aid!r}")
        self.manifest["flags"][aid] = True
        self._write_manifest()

    def close(self, t_end: float) -> None:
        self.manifest["t_end"] = float(t_end)
        self._write_manifest()
        self.closed = True
        self.store._release("live.lock")


@dataclass
class SessionReader:
    dir: Path
    manifest: dict

    @property
    def sid(self) -> str:
        return self.manifest["session"]

    def array(self, stream: str):
        """The stream as a read-only float16 memmap (rows, width); an empty (0, width) array if never written."""
        w = int(self.manifest["widths"].get(stream, SCHEMAS[stream]["dims"]))
        n = int(self.manifest["rows"].get(stream, 0))
        p = self.dir / f"{stream}.f16"
        if n == 0 or not p.exists():
            return np.zeros((0, w), dtype=np.float16)
        return np.memmap(p, dtype=np.float16, mode="r", shape=(n, w))

    def _jsonl(self, name: str) -> list:
        p = self.dir / name
        if not p.exists():
            return []
        return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln]

    def transcript(self) -> list:
        """[(TranscriptText, words)] in order; line index = position."""
        return [(restored_text(r["speaker"], r["text"], r["t"]), [tuple(w) for w in r["words"]])
                for r in self._jsonl("transcript.jsonl")]

    def events(self) -> list:
        return self._jsonl("events.jsonl")

    def omega_records(self) -> list:
        return self._jsonl("omega.jsonl")

    def set_replayed(self) -> None:
        self.manifest["replayed"] = True
        tmp = self.dir / "manifest.json.tmp"
        tmp.write_text(json.dumps(self.manifest, sort_keys=True))
        os.replace(tmp, self.dir / "manifest.json")


class Store:
    def __init__(self, root, switches: dict | None = None):
        self.root = Path(root)
        self.switches = switches
        (self.root / "sessions").mkdir(parents=True, exist_ok=True)
        (self.root / "consolidated").mkdir(exist_ok=True)

    # ------------------------------------------------------------------------------------------ locks
    def _take(self, name: str) -> None:
        other = "replay.lock" if name == "live.lock" else "live.lock"
        if (self.root / other).exists():
            raise StoreRefused(f"{other} is held: a live session and replay never run together")
        try:
            fd = os.open(self.root / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise StoreRefused(f"{name} is already held") from None
        os.close(fd)

    def _release(self, name: str) -> None:
        try:
            os.remove(self.root / name)
        except FileNotFoundError:
            pass

    def live(self) -> bool:
        return (self.root / "live.lock").exists()

    # ------------------------------------------------------------------------------------------ sessions
    def open_session(self, sid: str, identity: str, t0: float) -> SessionWriter:
        """A live session's writer. Refused until the operator answered the retention question (Q34 item 6)."""
        require("feature_retention_days", "keep_slot_snippets", switches=self.switches)
        if not sid.replace("-", "").replace("_", "").isalnum():
            raise StoreRefused("session id: letters, digits, '-' and '_' only")
        self._take("live.lock")
        try:
            return SessionWriter(self, sid, identity, t0)
        except Exception:
            self._release("live.lock")
            raise

    def sessions(self) -> list:
        out = []
        for d in sorted((self.root / "sessions").iterdir()):
            m = d / "manifest.json"
            if d.is_dir() and m.exists():
                out.append(SessionReader(d, json.loads(m.read_text())))
        return sorted(out, key=lambda s: s.manifest["t0"])

    def delete_session(self, sid: str) -> None:
        shutil.rmtree(self.root / "sessions" / sid)

    # ------------------------------------------------------------------------------------------ consolidated
    def consolidated(self, name: str) -> Path:
        if name not in CONSOLIDATED_FILES:
            raise StoreRefused(f"no consolidated file {name!r}")
        return self.root / "consolidated" / name

    def read_json(self, name: str, default):
        p = self.consolidated(name)
        return json.loads(p.read_text()) if p.exists() else default

    def write_json(self, name: str, obj) -> None:
        p = self.consolidated(name)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_text(json.dumps(obj, sort_keys=True, allow_nan=False))
        os.replace(tmp, p)

    def append_log(self, name: str, rec: dict) -> None:
        with open(self.consolidated(name), "ab") as f:
            f.write(_line(rec))

    def read_lines(self, name: str) -> list:
        p = self.consolidated(name)
        return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln] if p.exists() else []

    def write_lines(self, name: str, recs: list) -> None:
        p = self.consolidated(name)
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(b"".join(_line(r) for r in recs))
        os.replace(tmp, p)

    def save_arrays(self, name: str, arrays: dict) -> None:
        p = self.consolidated(name)
        for k, v in arrays.items():
            if np.asarray(v).dtype.kind != "f":
                raise StoreRefused(f"learned array {k!r}: floating point only")
        tmp = p.with_name(p.name + ".tmp.npz")
        np.savez(tmp, **{k: np.asarray(v, dtype=np.float64) for k, v in arrays.items()})
        os.replace(tmp, p)

    def load_arrays(self, name: str) -> dict:
        p = self.consolidated(name)
        if not p.exists():
            return {}
        with np.load(p, allow_pickle=False) as z:
            return {k: z[k] for k in z.files}


# ---------------------------------------------------------------------------------------------------- A12
def _magic_hit(head: bytes) -> bool:
    return any(m in head for m in MAGIC)


def check_a12(root) -> list:
    """A12 (nightly, start): the store's directories contain only the registered feature schemas: no unregistered
    file, no WAV/PCM/image/video magic number in a file's first 16 bytes, no feature file above its schema size and
    every feature file a whole number of float16 rows. Returns [(relative path, why)]."""
    root = Path(root)
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if not p.is_file() or rel.parts[0] == "quarantine":
            continue
        r = rel.as_posix()
        with open(p, "rb") as f:
            head = f.read(16)
        size = p.stat().st_size
        parts = rel.parts
        if len(parts) == 1:
            ok = parts[0] in ("live.lock", "replay.lock") and size == 0
            if not ok:
                out.append((r, "unregistered file"))
            continue
        if parts[0] == "consolidated" and len(parts) == 2:
            if parts[1] not in CONSOLIDATED_FILES:
                out.append((r, "unregistered file"))
            elif not parts[1].endswith(".npz") and _magic_hit(head):
                out.append((r, "media magic number"))
            elif parts[1].endswith(".npz"):
                try:
                    with np.load(p, allow_pickle=False) as z:
                        if any(z[k].dtype.kind != "f" for k in z.files):
                            out.append((r, "non-float learned array"))
                except Exception:
                    out.append((r, "unreadable learned arrays"))
            continue
        if parts[0] == "sessions" and len(parts) == 3:
            name = parts[2]
            if name in TEXT_FILES or name == "manifest.json":
                if _magic_hit(head):
                    out.append((r, "media magic number"))
                continue
            stem, dot, ext = name.partition(".")
            if ext != "f16" or stem not in SCHEMAS:
                out.append((r, "unregistered file"))
                continue
            if _magic_hit(head):
                out.append((r, "media magic number"))
            elif size > max_bytes(stem):
                out.append((r, "above the schema size"))
            elif size % 2:
                out.append((r, "not whole float16 values"))
            continue
        out.append((r, "unregistered file"))
    return out


def enforce_a12(root) -> None:
    """A12 fail-safe: quarantine every offending file (moved under quarantine/, out of every reader's way), then
    stop with InvariantError naming them for the operator."""
    from engine.invariants.asserts import InvariantError
    root = Path(root)
    bad = check_a12(root)
    if not bad:
        return
    q = root / "quarantine"
    q.mkdir(exist_ok=True)
    for r, _ in bad:
        src = root / r
        if src.exists():
            os.replace(src, q / r.replace("/", "__"))
    raise InvariantError("A12", "quarantined, tell the operator: " + "; ".join(f"{r} ({why})" for r, why in bad))
