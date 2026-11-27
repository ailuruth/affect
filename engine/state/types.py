"""Type tags of the latent state and the typed T / Ω objects (spec §1.3, §1.3.1; r5 §2.2).

T: his words, turn order, session boundaries, identity, per-session latched values, the agent's own body clock,
   and anything computed only from these.
F: anything computed within a session from his face, voice or derived features.
O: the agent's own realised words, draft choice, retrieval, own turn events (the design's Omega).
K: the world model and the concept layer.
latched: rule-6 session values (b_id, b_read, sigma_id), readable by T only as rule 6 allows.
own: the agent's own rendered face as its own camera sees it (rule 13': g_o and g may read it; no T field does).

FIELD_TYPES is the declaration the T1 AST rule (engine/invariants/t1_rule.py) and the type trace
(engine/invariants/typetrace.py) read. ALLOWED_SOURCES says which provenance prefixes (engine/invariants/tagged.py)
a field of each type may carry; the trace checks every assignment of a declared field against it.

The objects: `Word`, `Utterance` and `TurnEvent` are T (made by the boundary from his recognised words and the
session; M2 builds the recogniser, here they are plain records). `OwnHeard` is the one Ω object that reaches the
state, made only by `heard_at_playback` (called by the `tts` process at playback, M5); a T computation may read it
only inside a port of engine/state/ports.py.

The prompt objects (M6, spec §1.8, A11): `TranscriptText`, `Marker` and `Snippet` are the only things the Claude
prompt builder (engine/omega/transcript.py) accepts. Each is made only by its factory: `his_text` from his recognised
`Utterance`, `agent_text` from a `ChosenReply` (the winning draft, made only by engine/omega/pool.py), `marker` from
the observable silence length and the INNATE marker template, `snippet` from earlier `TranscriptText` entries.
None carries a body value, latent value, label or any number derived from state. `ChosenReply` and the prompt
objects are Ω: no T, F or K computation reads them (only `OwnHeard`, made at playback, reaches the state).
"""
from __future__ import annotations

from dataclasses import dataclass, field

TYPES = frozenset({"T", "F", "O", "K", "latched", "own"})

FIELD_TYPES = {
    # ---------------------------------------------------------------- body and loads (spec §1.3 table)
    "E": "T",
    "A_L": "T",
    "V_F": "F",
    "h_word": "T",
    "K": "T",
    "P_play": "T",
    "I_lp": "T",
    "N_L": "T",
    "Dp_face": "F",
    "Dp_word": "T",
    "mu_T": "T",
    "mu_F": "F",
    "slots_T": "T",
    "slots_F": "F",
    "xi": "F",
    "xi_A": "F",
    "D_tau": "F",
    "q_trace": "T",
    "omega": "T",
    "b_id": "latched",
    "b_read": "latched",
    "sigma_id": "latched",
    "env_drop": "T",
    "env_rise": "T",
    "M_state": "K",
    "concepts": "K",
    # ---------------------------------------------------------------- M4: T values of the body and learned T parts
    "env_progress": "T",          # envelope of the learning-progress drop events (interest row)
    "env_laugh": "T",             # envelope of the own laugh pattern, amplitude 0.40 qhat at his turns
    "drop_events": "T",           # recent (time, amplitude) of E1 drop events (values of the last events, rule 14)
    "rise_events": "T",
    "progress_events": "T",
    "laugh_events": "T",
    "D_T_prev": "T",              # the T drive terms at the previous tick (for E1 events)
    "q_hat": "T",
    "L_d": "T",
    "reader_his": "T",            # population reader (V, A, T) of his last utterance
    "e_his_last": "T",
    "e_his_prev": "T",
    "lam_his_last": "T",
    "lam_his_prev": "T",
    "lam_delivered": "T",         # Lambda_V on his words as delivered so far
    "surprisal_last": "T",
    "t_his_end": "T",
    "t_session_start": "T",
    "t_his_spoke": "T",
    "present": "T",
    "last_speaker": "T",
    "sigh_t": "T",
    "inhale_t": "T",
    # ---------------------------------------------------------------- the port outputs (P1-P5): T after the port
    "lam_own": "T",               # P1
    "e_agent_turn": "T",          # P2
    "q_bit_agent": "T",           # P3
    "p_name": "T",                # P4
    "t_agent_start": "T",         # P5
    "t_agent_end": "T",           # P5
    # ---------------------------------------------------------------- M4: F state of the routes and readers
    "ring_u": "F",
    "lp4": "F",
    "xi_A_lo": "F",
    "xi_A_hi": "F",
    "trace_read20": "F",
    "V_his": "F",
    "y_A_tick": "F",
    "y_A_prev_tick": "F",
    # ---------------------------------------------------------------- the agent's own face (rule 13')
    "own_face_trace": "own",
    "V_own": "own",
}

assert set(FIELD_TYPES.values()) <= TYPES

# Provenance prefixes each type may carry (spec §4.4: T reads only T, except rule-6 latched values and Ω values read
# inside the five ports, whose outputs are tagged "T:port.Pi"; F never reads Ω).
ALLOWED_SOURCES = {
    "T": frozenset({"T:", "latched:", "noise:"}),
    "F": frozenset({"F:", "T:", "latched:", "noise:", "own:"}),
    "latched": frozenset({"F:", "T:", "latched:"}),
    "O": frozenset({"O:"}),
    "K": frozenset({"F:", "T:", "latched:", "noise:", "own:", "O:"}),
    "own": frozenset({"own:", "T:"}),
}


def fields_of(tag: str) -> frozenset:
    return frozenset(k for k, v in FIELD_TYPES.items() if v == tag)


# ---------------------------------------------------------------------------------------------------- T objects
@dataclass(frozen=True)
class Word:
    text: str
    t_start: float
    t_end: float
    t_delivered: float


@dataclass(frozen=True)
class Utterance:
    """His recognised utterance (T). `text_norm` is the ASR normaliser's output (no laughter tokens); `text` keeps the
    recogniser's punctuation for qform."""
    speaker: str
    words: tuple
    text_norm: str
    t_end: float
    text: str = ""


@dataclass(frozen=True)
class TurnEvent:
    """A turn event (T): his_utterance_end, session_start; agent_utterance_start/end come only out of port P5."""
    kind: str
    t: float


TURN_KINDS = frozenset({"his_utterance_end", "session_start", "agent_utterance_start", "agent_utterance_end"})


def qform(text: str) -> bool:
    """The question bit: the utterance ends in '?' as the recogniser punctuates it (spec §1.3.1)."""
    return text.rstrip().endswith("?")


# ---------------------------------------------------------------------------------------------------- Ω object
_PLAYBACK = object()


@dataclass(frozen=True)
class OwnHeard:
    """The agent's own words as heard (Ω; spec §1.3.1). Made only by `heard_at_playback`."""
    words: tuple
    t_word_end: tuple
    template: str
    t_start: float
    t_end: float
    interrupted: bool
    _origin: object = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self._origin is not _PLAYBACK:
            raise TypeError("OwnHeard is made only at playback (heard_at_playback, the tts process)")
        if self.template not in ("statement", "question"):
            raise ValueError("template must be 'statement' or 'question'")
        if len(self.words) != len(self.t_word_end):
            raise ValueError("one playback end time per word")


def heard_at_playback(words, t_word_end, template: str, t_start: float, t_played_until: float | None = None) -> OwnHeard:
    """The words actually played: the chosen reply after R11's stripping, truncated at the last word whose playback
    ended by `t_played_until` if speech was interrupted. Called by the `tts` process (M5) and by tests."""
    words, t_word_end = tuple(words), tuple(float(x) for x in t_word_end)
    interrupted = False
    if t_played_until is not None and t_word_end and t_played_until < t_word_end[-1]:
        keep = [i for i, te in enumerate(t_word_end) if te <= t_played_until]
        words = tuple(words[i] for i in keep)
        t_word_end = tuple(t_word_end[i] for i in keep)
        interrupted = True
    t_end = t_word_end[-1] if t_word_end else float(t_start)
    return OwnHeard(words, t_word_end, template, float(t_start), float(t_end), interrupted, _PLAYBACK)


# ---------------------------------------------------------------------------------------------------- prompt objects
_RECOGNISER, _CHOSEN, _TEMPLATE, _STORE = object(), object(), object(), object()


@dataclass(frozen=True)
class ChosenReply:
    """The winning draft's text, cut at its interruption point, without its fork line (Ω; spec §1.8). Made only by
    `engine.omega.pool` (`_chosen_reply`); it goes to the `tts` process and to the canonical transcript, never to
    the state (the state hears only `OwnHeard`, made at playback)."""
    text: str
    t: float
    _origin: object = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self._origin is not _CHOSEN:
            raise TypeError("ChosenReply is made only by the omega pool")


def _chosen_reply(text: str, t: float) -> ChosenReply:
    return ChosenReply(str(text), float(t), _CHOSEN)


@dataclass(frozen=True)
class TranscriptText:
    """One turn of the canonical transcript: his normalised words (`his`) or the agent's chosen reply (`agent`)."""
    speaker: str
    text: str
    t: float
    _origin: object = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self._origin not in (_RECOGNISER, _CHOSEN) or self.speaker not in ("his", "agent"):
            raise TypeError("TranscriptText is made only by his_text (recogniser) or agent_text (chosen reply)")
        if (self.speaker == "his") != (self._origin is _RECOGNISER):
            raise TypeError("speaker does not match the source")


def his_text(utt: Utterance) -> TranscriptText:
    if not isinstance(utt, Utterance):
        raise TypeError("his_text reads only a recognised Utterance")
    return TranscriptText("his", utt.text_norm, float(utt.t_end), _RECOGNISER)


def agent_text(reply: ChosenReply) -> TranscriptText:
    if not isinstance(reply, ChosenReply):
        raise TypeError("agent_text reads only a ChosenReply")
    return TranscriptText("agent", reply.text, reply.t, _CHOSEN)


@dataclass(frozen=True)
class Marker:
    """An observable-marker user turn for initiative: the INNATE marker template with the silence rounded to 5 s."""
    text: str
    t: float
    _origin: object = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self._origin is not _TEMPLATE:
            raise TypeError("Marker is made only by marker()")


def marker(silence_s: float, t: float) -> Marker:
    from engine.config.innate import ENTRIES
    tpl = ENTRIES["marker_template"].value
    step = float(tpl["round_s"])
    n = int(max(step, step * round(float(silence_s) / step)))
    return Marker(tpl["text"].replace("N", str(n)), float(t), _TEMPLATE)


@dataclass(frozen=True)
class Snippet:
    """A retrieved raw transcript snippet of an earlier session: consecutive stored `TranscriptText` entries."""
    entries: tuple
    t: float
    _origin: object = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self._origin is not _STORE:
            raise TypeError("Snippet is made only by snippet()")


def snippet(entries) -> Snippet:
    entries = tuple(entries)
    if not entries or not all(isinstance(e, TranscriptText) for e in entries):
        raise TypeError("a Snippet is made only of stored TranscriptText entries")
    return Snippet(entries, entries[0].t, _STORE)
