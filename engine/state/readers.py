"""Readers and word encoders (spec §1.3 "Readers", §1.2.6, §3.2). Knowing only: their outputs enter the partner-load terms, initiative,
the gates' masked inputs and draft scoring, never a gain on a path to the face.

UNTRAINED STUBS. Every learned part here has its declared shape and a `trained = False` flag; weights are zero (or,
for the encoder, a fixed hashing placeholder) until the offline fit (M3) or replay (M8) writes them:
  - `Encoder`: placeholder for MiniLM (384-d) -> frozen 64-d projection (M2/M3). A deterministic hashed
    bag-of-words, so that different words give different codes in mechanism tests; it is not a model of meaning.
  - `Lambda` (64 -> 3, ridge; 192 weights), `PopReader` (64 + 16 -> 64 -> 3), `WordToV` (64 + 16 -> 1),
    `Surprisal` (the population words model), `Progress` (pi_topic of the words-only partner model),
    `PiTilde0` (the own-body inverse on his masked calibrated face -> (V, A, T)), `PNameMap` (P4's word -> display map).
All stubs propagate provenance tags (engine/invariants/tagged.py) so that the type trace sees their sources.
"""
from __future__ import annotations

import hashlib

import numpy as np

from engine.config.innate import ENTRIES
from engine.invariants.tagged import Tagged, tags_of

DIMS = ENTRIES["embedding_dims"].value
E_DIM = DIMS["e"]
TOPIC_DIM = DIMS["topic"]


class TText(str):
    """A string carrying provenance tags (trace mode only): his words ("T:utterance") or the agent's ("O:own_heard")."""
    tags: frozenset = frozenset()

    @classmethod
    def wrap(cls, s: str, tags) -> "TText":
        o = cls(s)
        o.tags = frozenset(tags)
        return o


def text_tags(words) -> frozenset:
    out = frozenset()
    for w in ([words] if isinstance(words, str) else words):
        out |= getattr(w, "tags", frozenset())
    return out


def _carry(value: np.ndarray, tags: frozenset):
    return Tagged.wrap(value, tags) if tags else value


def _word_code(w: str) -> np.ndarray:
    seed = int.from_bytes(hashlib.sha256(w.lower().encode("utf-8")).digest()[:8], "little")
    return np.random.default_rng(seed).standard_normal(E_DIM)


class Encoder:
    """Placeholder utterance encoder -> e[64] (hashed bag of words, unit norm; zeros for no words)."""
    trained = False

    def encode(self, words):
        words = [words] if isinstance(words, str) else list(words)
        tg = text_tags(words)
        toks = [t for w in words for t in str(w).lower().split() if t]
        v = np.zeros(E_DIM)
        for t in toks:
            v = v + _word_code(t)
        n = np.linalg.norm(v)
        if n > 0:
            v = v / n
        return _carry(v, tg)

    def topic(self, words) -> int:
        """Topic slot of an utterance (placeholder: the hashed code's largest coordinate among the first 16)."""
        v = np.asarray(self.encode(words))
        return int(np.argmax(np.abs(v[:TOPIC_DIM]))) if np.any(v) else 0


class _Linear:
    trained = False

    def __init__(self, n_in: int, n_out: int):
        self.W = np.zeros((n_in, n_out))
        self.b = np.zeros(n_out)

    def __call__(self, x):
        return x @ self.W + self.b


class Lambda(_Linear):
    """Lambda: e[64] -> listener response (V, A, T) of a listener's masked face; Lambda_V is coordinate 0."""

    def __init__(self):
        super().__init__(E_DIM, 3)


class PopReader:
    """Population word reader: (e[64], topic[16]) -> 64 -> (V, A, T) in [0, 1]. Untrained: 0 (N_L = 0, spec §1.3)."""
    trained = False

    def __init__(self):
        self.W1 = np.zeros((E_DIM + TOPIC_DIM, 64))
        self.b1 = np.zeros(64)
        self.W2 = np.zeros((64, 3))
        self.b2 = np.zeros(3)

    def __call__(self, e, topic_code):
        x = np.concatenate([e, topic_code])
        h = np.tanh(x @ self.W1 + self.b1)
        return np.clip(h @ self.W2 + self.b2, 0.0, 1.0)


class WordToV(_Linear):
    """Word -> V map (taught by the threat reflex in replay, M8): v_w in [0, 1]."""

    def __init__(self):
        super().__init__(E_DIM + TOPIC_DIM, 1)

    def __call__(self, e, topic_code):
        return np.clip((np.concatenate([e, topic_code]) @ self.W + self.b)[0], 0.0, 1.0)


class Surprisal:
    """Lexical surprisal s_lex in [0, 1] under the frozen population words model (M3). Untrained: 0."""
    trained = False

    def __call__(self, e):
        return e[0] * 0.0


class Progress:
    """pi_topic: words-only partner model's error over the previous 8 minus the latest 4 utterances (M8). Untrained: 0."""
    trained = False

    def __call__(self, e):
        return e[0] * 0.0


class PiTilde0(_Linear):
    """The own-body reader on his masked calibrated face (channels of `read_idx`) -> (V, A, T). Untrained stub."""

    def __init__(self, n_in: int):
        super().__init__(n_in, 3)

    def __call__(self, x):
        return np.clip(x @ self.W + self.b, 0.0, 1.0)


class PNameMap(_Linear):
    """P4: the agent's own heard words -> attenuation of each named display channel, in [0, p_name_max]."""

    def __init__(self):
        super().__init__(E_DIM, 33)
        self.bound = ENTRIES["p_name_max"].value

    def __call__(self, e):
        return np.clip(e @ self.W + self.b, 0.0, self.bound)


def topic_code(slot: int, like=None):
    v = np.zeros(TOPIC_DIM)
    v[slot % TOPIC_DIM] = 1.0
    return _carry(v, tags_of(like)) if like is not None else v
