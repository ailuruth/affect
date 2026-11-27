"""The feature store (A12: features only, never raw audio or video) and the retention job (Q34 item 6). Synthetic
arrays in a temporary directory only."""
import dataclasses
import inspect

import numpy as np
import pytest

from engine.config import operator as op
from engine.invariants.asserts import InvariantError, check_a12
from engine.memory import store as ST
from engine.memory.retention import reference_snippets, run_retention
from engine.memory.store import SessionWriter, Store, StoreRefused, enforce_a12
from engine.state import types as T
from synth_store import DAY, answered, write_session


def unanswered_switches() -> dict:
    """The switches with every operator answer withdrawn (the state before the answers of 2026-11-28)."""
    return {n: dataclasses.replace(s, answered=False, usable_before_answer=False) for n, s in op.SWITCHES.items()}


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "st", answered())


# ---------------------------------------------------------------------------------------------------- the writer
def test_no_live_session_before_the_retention_answer(tmp_path):
    s = Store(tmp_path / "st", unanswered_switches())
    with pytest.raises(op.Unanswered, match="feature_retention_days"):
        s.open_session("s1", "op", 0.0)
    assert not s.live()


def test_writer_api_has_no_media_type():
    public = {n for n, _ in inspect.getmembers(SessionWriter, inspect.isfunction) if not n.startswith("_")}
    assert public == {"append", "append_transcript", "append_event", "append_omega", "flag", "close"}
    banned = ("audio", "video", "image", "frame", "pcm", "wav", "jpeg", "png", "pixel", "mp4")
    assert not [k for k in ST.SCHEMAS if any(b in k.lower() for b in banned)]


@pytest.mark.parametrize("stream,payload", [
    ("audio", np.zeros((10, 1))),                                         # no such stream
    ("video", np.zeros((2, 33))),
    ("u", (np.arange(330) % 200).astype(np.int16).reshape(10, 33)),       # PCM-like int16
    ("own_face", np.zeros((2, 33), dtype=np.uint8)),                      # pixels
    ("own_face", np.zeros((4, 48, 33))),                                  # an image-shaped block
    ("u", b"RIFF\x00\x00\x00\x00WAVEfmt "),                                # raw bytes
    ("u", bytearray(66)),
    ("u", memoryview(b"\x00" * 66)),
    ("u", np.zeros((3, 32))),                                             # wrong width
    ("u", np.full((1, 33), np.nan)),
])
def test_writer_refuses_media_and_unregistered(store, stream, payload):
    w = store.open_session("s1", "op", 0.0)
    with pytest.raises(StoreRefused):
        w.append(stream, payload)
    w.close(1.0)
    assert not list((store.root / "sessions" / "s1").glob("*.f16"))
    assert check_a12(store.root) == []


def test_writer_refuses_above_the_schema_size(store):
    w = store.open_session("s1", "op", 0.0)
    with pytest.raises(StoreRefused, match="schema size"):
        w.append("voice_phrase", np.zeros((ST.max_rows("voice_phrase") + 1, 8)))
    w.close(1.0)


def test_text_records_only_through_their_schemas(store):
    w = store.open_session("s1", "op", 0.0)
    with pytest.raises(StoreRefused):
        w.append_transcript("raw text")
    with pytest.raises(StoreRefused):
        w.append_event(kind="drop_event", t=1.0, audio=[1, 2])
    with pytest.raises(StoreRefused):
        w.append_event(kind="label", t=1.0)
    with pytest.raises(StoreRefused):
        w.append_omega(t=1.0, telemetry={"x": "text"})
    i = w.append_transcript(T.his_text(T.Utterance("him", (), "we planted beans", 2.0, "we planted beans")),
                            [("we", 1.5), ("planted", 1.8), ("beans", 2.0)])
    w.close(3.0)
    (r,) = store.sessions()
    (entry, words), = r.transcript()
    assert i == 0 and isinstance(entry, T.TranscriptText) and entry.text == "we planted beans"
    assert words[-1] == ("beans", 2.0)


def test_a_session_is_features_only(store):
    write_session(store, "s1", seconds=30.0)
    assert check_a12(store.root) == []
    files = sorted(p.name for p in (store.root / "sessions" / "s1").iterdir())
    allowed = {f"{k}.f16" for k in ST.SCHEMAS} | set(ST.TEXT_FILES) | {"manifest.json"}
    assert set(files) <= allowed
    for p in (store.root / "sessions" / "s1").glob("*.f16"):
        head = p.read_bytes()[:16]
        assert not any(m in head for m in ST.MAGIC)
    (r,) = store.sessions()
    u = r.array("u")
    assert isinstance(u, np.memmap) and u.dtype == np.float16 and u.shape == (900, 33)
    assert not store.live()


@pytest.mark.parametrize("name,data,why", [
    ("sessions/s1/talk.wav", b"RIFF\x24\x00\x00\x00WAVEfmt ", "unregistered"),
    ("sessions/s1/u.f16", b"\x89PNG\r\n\x1a\n" + b"\x00" * 64, "magic"),
    ("sessions/s1/breath.f16", b"\x00\x00\x00\x00ftypisom", "magic"),
    ("consolidated/frame.jpg", b"\xff\xd8\xff\xe0", "unregistered"),
    ("notes.txt", b"x", "unregistered"),
])
def test_a12_fires_and_quarantines(store, name, data, why):
    write_session(store, "s1", seconds=10.0)
    p = store.root / name
    p.write_bytes(data)
    bad = check_a12(store.root)
    assert [r for r, w in bad] == [name] and why in bad[0][1].replace("media magic number", "magic")
    with pytest.raises(InvariantError, match="A12"):
        enforce_a12(store.root)
    assert not p.exists() and (store.root / "quarantine").is_dir()
    assert check_a12(store.root) == []


def test_a12_size_check(store):
    write_session(store, "s1", seconds=10.0)
    p = store.root / "sessions" / "s1" / "voice_phrase.f16"
    p.write_bytes(b"\x00" * (ST.max_bytes("voice_phrase") + 2))
    assert check_a12(store.root) == [("sessions/s1/voice_phrase.f16", "above the schema size")]


def test_live_session_and_replay_exclude_each_other(store):
    w = store.open_session("s1", "op", 0.0)
    with pytest.raises(StoreRefused):
        store._take("replay.lock")
    with pytest.raises(StoreRefused):
        store.open_session("s2", "op", 0.0)
    w.close(1.0)
    store._take("replay.lock")
    with pytest.raises(StoreRefused):
        store.open_session("s3", "op", 0.0)
    store._release("replay.lock")


# ---------------------------------------------------------------------------------------------------- retention
def _three_sessions(store):
    write_session(store, "old1", t0=0.0, seconds=20.0, seed=1)
    write_session(store, "old2", t0=2 * DAY, seconds=20.0, seed=2)
    write_session(store, "new", t0=39 * DAY, seconds=20.0, seed=3)
    reference_snippets(store, "slot7", [("old1", 0), ("old1", 1)])


def test_retention_unanswered_keeps_everything_and_reports(tmp_path):
    st = Store(tmp_path / "st", answered())
    _three_sessions(st)
    sw = unanswered_switches()
    rep = run_retention(st, 40 * DAY, sw)
    assert not rep.answered and rep.deleted == []
    assert rep.beyond_window == ["old1", "old2"] and "waiting for the operator" in rep.message
    assert {s.sid for s in st.sessions()} == {"old1", "old2", "new"}
    sw2 = dict(sw, feature_retention_days=dataclasses.replace(sw["feature_retention_days"], answered=True))
    rep = run_retention(st, 40 * DAY, sw2)                   # one of the two answers is still missing
    assert rep.deleted == [] and len(st.sessions()) == 3


def test_retention_answered_30_days(tmp_path):
    st = Store(tmp_path / "st", answered())
    _three_sessions(st)
    rep = run_retention(st, 40 * DAY, answered(feature_retention_days=30, keep_slot_snippets=True))
    assert rep.answered and rep.deleted == ["old1", "old2"]
    assert [s.sid for s in st.sessions()] == ["new"]
    kept = st.read_lines("snippets.jsonl")
    assert len(kept) == 2 and {k["slot"] for k in kept} == {"slot7"}
    assert rep.kept_snippet_lines == 2 and set(rep.deleted_before_replay) == {"old1", "old2"}
    assert st.read_json("slot_refs.json", {}) == {}
    assert check_a12(st.root) == []


def test_retention_answered_without_slot_snippets_and_7_days(tmp_path):
    st = Store(tmp_path / "st", answered())
    _three_sessions(st)
    rep = run_retention(st, 47 * DAY, answered(feature_retention_days=7, keep_slot_snippets=False))
    assert rep.deleted == ["old1", "old2", "new"]
    assert st.read_lines("snippets.jsonl") == [] and st.sessions() == []


def test_retention_until_he_deletes(tmp_path):
    st = Store(tmp_path / "st", answered())
    _three_sessions(st)
    rep = run_retention(st, 400 * DAY, answered(feature_retention_days=None))
    assert rep.deleted == [] and len(st.sessions()) == 3


def test_slot_keeps_at_most_three_lines(store):
    with pytest.raises(ValueError):
        reference_snippets(store, "s", [("a", i) for i in range(4)])
