"""The innate body (spec §1.3; A14): dynamics of each load, E1 events and envelopes, A14 accounting and its fail-safe.
Synthetic inputs only; not evidence about behaviour."""
import numpy as np
import pytest

from engine.config.innate import ENTRIES
from engine.routes.learned_t import Learned, randomise_for_trace
from engine.state.body import Body, Session, SlowInputs, dp_partner, envelope
from engine.state.drives import drive_partner
from engine.state.types import Utterance, heard_at_playback


def _utt(t, text="some words here"):
    return Utterance("him", (), text, t, text)


def _run(body, seconds, utt_every=None, own_every=None, present=True, t0=0.0):
    t = t0
    while t < t0 + seconds:
        us = (_utt(t),) if utt_every and int(t * 2) % int(utt_every * 2) == 0 and t > 0 else ()
        oh = (heard_at_playback(["a", "reply"], [t - 0.3, t], "statement", t - 0.6),) \
            if own_every and int(t * 2) % int(own_every * 2) == 3 else ()
        body.tick(SlowInputs(t, us, oh, present, (), 0.0, 0.7))
        t += 0.5
    return body


def test_envelope_shape():
    assert envelope(-0.1) == 0.0 and envelope(0.2) == pytest.approx(0.5) and envelope(1.0) == 1.0
    assert envelope(4.5) == pytest.approx(np.exp(-1.0))


def test_dp_partner_matches_drives_module():
    r = np.random.default_rng(0)
    for _ in range(100):
        V, A, T = r.uniform(0, 1, 3)
        assert dp_partner(np.array([V, A, T])) == pytest.approx(drive_partner(V, A, T), rel=1e-12)


def test_energy_decay_and_drive_ranges_a14_silent():
    L = randomise_for_trace(Learned(), 3)
    b = _run(Body(Session(K=0.7, P=0.4, I=0.5), L), 600, utt_every=6, own_every=9)
    assert not b.frozen and b.failures == []
    assert b.E == pytest.approx(0.8 - ENTRIES["energy_decay_per_min"].value * 10, abs=1e-9)
    for v in b.b().values():
        assert 0.0 <= v <= 1.0


def test_contact_drop_in_session_and_never_missed_person():
    b = _run(Body(Session(f_id=1.0, K=0.6), Learned()), 30, present=True)
    assert float(b.K) == pytest.approx(0.6 * np.exp(-0.5 * 30 / 30.0 * 1.0), rel=1e-9)   # face only: e = 0.5
    s = _run(Body(Session(f_id=0.1, K=0.6), Learned()), 30)
    assert float(s.K) == 0.0                                                             # f_id < 0.3: no K
    k = Body(Session(f_id=1.0, K=0.2), Learned())
    k.between_sessions(36.0)
    assert float(k.K) == pytest.approx(1 - 0.8 * np.exp(-1), rel=1e-12)


def test_play_drop_by_qhat_and_own_laugh():
    L = Learned()
    L.qhat.b0 = 0.0                               # qhat 0.5 (logistic base rate, stub weights)
    b = Body(Session(P=0.5), L)
    b.tick(SlowInputs(0.5, (_utt(0.4),), (), True, (), 0.0, 1.0))
    assert float(b.q_hat) == pytest.approx(0.5)
    assert float(b.P_play) == pytest.approx(0.5 * (1 - 0.15 * 0.5), rel=1e-4)
    assert float(b.laugh_events[-1][1]) == pytest.approx(0.40 * 0.5)
    _run(b, 1.0, t0=1.0)                          # last tick at 1.5 s: 1.1 s after the event, on the apex
    assert float(b.env_laugh) == pytest.approx(0.20, rel=1e-6)    # apex of the envelope
    assert float(b.env_drop) > 0                                   # the P drop is a drop event (E1)


def test_opponent_masking_of_drops_by_rises():
    L = Learned()
    L.qhat.b0 = np.log(0.9 / 0.1)
    L.word_v.b[:] = 0.6                           # each of his words latches h (rise event)
    b = Body(Session(P=0.8), L)
    b.tick(SlowInputs(0.5, (_utt(0.4),), (), True, (), 0.0, 1.0))
    assert b.drop_events == () and len(b.rise_events) == 1        # R' = max(0, R - 3 S) = 0


def test_a14_failsafe_freezes_the_body():
    b = Body(Session(), Learned())
    b.tick(SlowInputs(0.5))
    orig = b._tick

    def bad_tick(inp):
        orig(inp)
        object.__setattr__(b, "P_play", b.P_play + 0.1)           # an undeclared change
    b._tick = bad_tick
    before = float(b.P_play)
    b.tick(SlowInputs(1.0))
    assert b.frozen and b.learning_off and b.failures[0][1] == "A14"
    assert float(b.P_play) == before                               # frozen at its last valid state
    b.tick(SlowInputs(1.5))
    assert float(b.P_play) == before


def test_t_fields_are_declared_t():
    from engine.state.types import FIELD_TYPES
    b = Body(Session(), Learned())
    assert b.t_fields() and all(FIELD_TYPES[k] == "T" for k in b.t_fields())
    assert {"E", "K", "P_play", "I_lp", "h_word", "A_L", "q_trace", "L_d", "env_drop"} <= set(b.t_fields())
