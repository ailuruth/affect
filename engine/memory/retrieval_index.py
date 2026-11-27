"""Retrieval support (spec §1.9 "Retrieval"): the snippet index over past transcripts, keyed by identity x topic
embedding x time, and the learned query built from the drive's gradient, N-hat and the concept posterior.

  query q = [grad D (6); N-hat (3); concept posterior (64)] @ W_q      W_q (73 x 64), trained nightly by J under the
                                                                      separation rule (step 7) once the world model
                                                                      exists (UNTRAINED STUB: 0, so every relevance is
                                                                      0 and recency alone orders the snippets)
  relevance(snippet) = cos(q, key)                                    key = the encoder's e[64] of the snippet's text
The relevance numbers stay in the `slow` process; `engine.omega.retrieval.retrieve` applies the ALiBi recency slope
and keeps <= 3, and only the raw stored text reaches Claude (as `Snippet`), only if `send_snippets` is on.
Candidates are only stored lines: the retained sessions' transcripts (inside the retention window) and the slot
snippet lines retention kept past it. A snippet is at most 3 consecutive lines of one session.
"""
from __future__ import annotations

import numpy as np

from engine.config.innate import ENTRIES

DIMS = ENTRIES["embedding_dims"].value
N_GRAD, N_NHAT, N_CONCEPT = 6, 3, int(ENTRIES["concepts_max"].value)
Q_IN = N_GRAD + N_NHAT + N_CONCEPT
SNIPPET_LINES = int(ENTRIES["context_window"].value["snippets"])


class RetrievalQuery:
    def __init__(self):
        self.W = np.zeros((Q_IN, DIMS["e"]))
        self.trained = False

    def __call__(self, grad_D, N_hat, concept_post):
        cp = np.zeros(N_CONCEPT)
        c = np.reshape(np.asarray(concept_post, dtype=np.float64), -1)[:N_CONCEPT]
        cp[:c.size] = c
        x = np.concatenate([np.reshape(grad_D, -1)[:N_GRAD], np.reshape(N_hat, -1)[:N_NHAT], cp])
        return x @ self.W


class SnippetIndex:
    """Index of candidate snippets for one identity: (Snippet, key e[64], t)."""

    def __init__(self, entries):
        self.entries = list(entries)

    @classmethod
    def build(cls, store, encoder, identity: str):
        from engine.state.types import restored_text, snippet
        out = []
        for s in store.sessions():
            if s.manifest["identity"] != identity:
                continue
            lines = [e for e, _ in s.transcript()]
            for i in range(0, len(lines), SNIPPET_LINES):
                chunk = lines[i:i + SNIPPET_LINES]
                out.append((snippet(chunk), np.asarray(encoder.encode([e.text for e in chunk]), dtype=np.float64)))
        for r in store.read_lines("snippets.jsonl"):
            if r.get("identity") == identity:
                e = restored_text(r["speaker"], r["text"], r["t"])
                out.append((snippet([e]), np.asarray(encoder.encode([e.text]), dtype=np.float64)))
        return cls(out)

    def candidates(self, q) -> list:
        """[(Snippet, relevance)], relevance = cosine(q, key) (0 for a zero query or key)."""
        q = np.asarray(q, dtype=np.float64)
        nq = np.linalg.norm(q)
        out = []
        for s, key in self.entries:
            nk = np.linalg.norm(key)
            out.append((s, float(q @ key / (nq * nk)) if nq > 0 and nk > 0 else 0.0))
        return out
