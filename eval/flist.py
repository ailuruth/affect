"""The F-list registry: every falsifier of spec §5.1 (design §8.2 and inherited) mapped to its test, its data
source and where it runs (machine and stage). tests/test_eval_flist.py checks that every F-id of the spec's §5.1
table is here and nothing else.

Data sources: SEAMLESS (Seamless test-split people, never used in a fit; the agent as listener; the held-out
listener is the dyad baseline), OPERATOR_M2 (his M2 feature recordings, all 33 channels, about 2 h), LIVE (the
operator, live, features only), REPLAYED (his stored sessions replayed), NIGHTLY (the nightly replay's reports),
RUNTIME (an assertion logged over every run). Machine: every evidence run is on the operator's Mac; this cloud
session runs only the synthetic mechanism tests in CI and the harness dry run (`make eval-dry`), which are never
evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

SEAMLESS = "Seamless test split (recorded partners)"
OPERATOR_M2 = "operator M2 feature recordings"
LIVE = "operator live"
REPLAYED = "operator sessions replayed"
NIGHTLY = "nightly replay reports"
RUNTIME = "runtime assertion log (all runs)"
SOURCES = (SEAMLESS, OPERATOR_M2, LIVE, REPLAYED, NIGHTLY, RUNTIME)

MAC = "operator's Mac"
CLOUD = "cloud CI (synthetic mechanism test only, not evidence)"


@dataclass(frozen=True)
class Stage:
    milestone: str
    machine: str
    data: tuple


@dataclass(frozen=True)
class Falsifier:
    fid: str
    statement: str
    test: str
    stages: tuple
    status: str

    @property
    def data(self) -> tuple:
        return tuple(dict.fromkeys(d for s in self.stages for d in s.data))


def _m(ms, *data):
    return Stage(ms, MAC, tuple(data))


def _ci(*data):
    return Stage("CI", CLOUD, tuple(data) or ("synthetic stand-ins",))


FALSIFIERS = (
    Falsifier("F1", "with partner-swap, segment-shuffle, timing-resample and month-swap surrogates (words and turn order "
              "fixed) a channel exceeds its pooled bound at 2 s, 10 s or 1 min, G_k or the instant bound; or the "
              "ledger binds on a natural partner on > 1 % of frames",
              "eval/surrogates.py (Battery, run_surrogates); eval/f01_bounds.py at M4",
              (_m("M4", SEAMLESS, OPERATOR_M2), _m("M8", LIVE), _ci()), "harness built; F1 driver at M4"),
    Falsifier("F1′", "the shadow's T state ever differs from the factual one", "A5 (engine/invariants/asserts.py), logged",
              (_m("M4", RUNTIME), _ci()), "runtime assertion"),
    Falsifier("F1‴", "ledger output larger than, or opposite in sign to, the partner-caused part",
              "A4 (engine/invariants/asserts.py), logged", (_m("M4", RUNTIME), _ci()), "runtime assertion"),
    Falsifier("F2", "a ridge decoder on F state fails to recover his held 1-min level at r >= 0.9 while F1 holds",
              "ridge decoder from F state (eval/f02_decoder.py at M4)", (_m("M4", SEAMLESS, OPERATOR_M2),),
              "not built: needs recorded partners"),
    Falsifier("F3", "crossed-habits manipulation (two people's channel codes swapped after calibration) does not change "
              "which faces raise Dp_face", "eval/steering.py replace_channels on recorded people",
              (_m("M8", SEAMLESS),), "harness built (input clamp); analysis at M8"),
    Falsifier("F4″", "at equal later need change, draft choice correlates with predicted display change, with replies "
              "inside the separation window, or with his later engagement", "log analysis (eval/f04_drafts.py at M8)",
              (_m("M8", LIVE),), "not built: needs the scorer and live logs"),
    Falsifier("F5", "varying only his smile amplitude (LP, CR x0, x0.5, x2; words, turns fixed) changes K, P, I, the "
              "drop envelopes or any T display", "eval/steering.py run_clamp (T-state digest per tick)",
              (_m("M4", SEAMLESS), _ci()), "harness built"),
    Falsifier("F6", "(a) day-1 speak-into-silence timing not calibrated to held-out listeners (KS not below the "
              "context-free hazard's); (b) a dose-response clamp of D_p along N-hat's V leaves the initiative hazard "
              "without a monotone response, or the random direction moves it as much",
              "(a) held-out timing; (b) eval/steering.py target N_L.V, readout the hazard",
              (_m("M3", SEAMLESS), _m("M8", REPLAYED)), "(b) harness built; readout needs the turn model"),
    Falsifier("F7", "naming-aligned trajectories do not differ from others, or the difference survives a P_name lesion",
              "eval/lesions.py p_name_removed", (_m("M8", LIVE),), "harness built (lesion)"),
    Falsifier("F8", "Pi-tilde + H_id disagree with his later separated reports more than a person-independent baseline "
              "after 400 utterances", "nightly report", (_m("M8", NIGHTLY),), "not built: nightly report at M8"),
    Falsifier("F8″", "co-training drift of Pi-tilde and H_id", "nightly report", (_m("M8", NIGHTLY),),
              "not built: nightly report at M8"),
    Falsifier("F9", "at E-trouble utterances the agent's (drop envelope x g_o) and own LP, CR over the 2 s after the "
              "last word, as a ratio to other utterances, is not below the held-out listeners' own (LP + CR)/2 ratio "
              "by more than the 95 % bootstrap interval; or g_o <- 1 does not remove the agent's contrast",
              "event analysis (eval/events.py at M3) + eval/lesions.py gate_go_const", (_m("M4", SEAMLESS),),
              "lesion harness built; event classes need recorded dyads"),
    Falsifier("F10", "echo-attributable laugh-synth input during his BU_S-dominant bursts exceeds G_k x his BU_L there "
              "(fast echo only); the own laugh near those bursts is a logged risk", "event analysis",
              (_m("M4", OPERATOR_M2), _m("M7", LIVE)), "not built: needs his recordings"),
    Falsifier("F11", "learned bases or Delta place weight on BL, LT, LPR, NW, DIM", "A7 (nightly)",
              (_m("M8", NIGHTLY, RUNTIME), _ci()), "runtime assertion"),
    Falsifier("F12", "deleted with the posture", "-", (), "deleted"),
    Falsifier("F13", "folded into F24 (q-hat's calibration)", "see F24", (), "folded into F24"),
    Falsifier("F14", "a draft's recorded system prompt or user message differs from what the engine built",
              "A11 (engine/omega/transcript.py)", (_m("M6", LIVE), _ci()), "runtime assertion"),
    Falsifier("F15", "held-out: the gate fails its criterion on test people; live: at his sentence-final laughs, per g "
              "bin, the agent's return ratio is above held-out listeners' by more than its 95 % interval",
              "held-out + live event analysis", (_m("M3", SEAMLESS), _m("M7", LIVE)), "not built: needs the gate fit"),
    Falsifier("F16", "Lambda's predicted response to utterances answered with a wince not above its prediction for the "
              "rest", "held-out", (_m("M3", SEAMLESS),), "not built: needs the Lambda fit"),
    Falsifier("F17", "a prompt or the canonical transcript contains an attend-to line from an earlier turn",
              "A11 (engine/omega/transcript.py)", (_m("M6", LIVE), _ci()), "runtime assertion"),
    Falsifier("F18", "the agent's BI block-mean slope on his BI exceeds c_BI at 1 or 10 min for any code with "
              "sigma_id >= 0.25 sigma_ref (his BI, BO, LP clamped while his words carry need; sigma_id swept)",
              "eval/steering.py run_clamp + eval/metrics.worst_block_slope", (_m("M4", SEAMLESS), _m("M7", LIVE)),
              "harness built"),
    Falsifier("F19", "changing only Claude's reply text changes a T field outside downstream(P1..P5); per-port holds; "
              "all ports held; a duration-changed swap", "type trace + tests/test_ports_typetrace.py; replayed sessions",
              (_m("M6", REPLAYED, LIVE), _ci()), "offline part built (M6)"),
    Falsifier("F20", "live, delivery of a sentence's last word to the gate's delivered-words value exceeds 33 ms + 0.5 s, "
              "or the partial echo exceeds the word-end-to-delivery p90 + 0.55 s", "event analysis (timing)",
              (_m("M7", LIVE),), "not built: needs live sessions"),
    Falsifier("F21", "deleted (revision 8.3's onset-aligned gate-fit check)", "-", (), "deleted"),
    Falsifier("F22", "an injected uncounted copy of his channel delayed 10-300 s renders above 1.0 c_k by the block-mean "
              "metric at 2 s, 10 s or 1 min; or the ledger changes > 1 % of the counted routes' frames on natural "
              "partners", "eval/f22_delayed_copy.py (ledger only, batched; --pilot plans per §5.5)",
              (_m("M4", SEAMLESS, OPERATOR_M2), _m("M7", LIVE), _ci()),
              "harness built; synthetic injected copies are the CI mechanism test (tests/test_ledger_injected.py)"),
    Falsifier("F23", "on held-out people the pooled 1-min slope of L_d / own laugh on the speaker's channel through words "
              "alone exceeds c_k; or L_d changes when only the speaker's face is changed",
              "held-out + eval/steering.py run_clamp (face swap, words fixed)", (_m("M3", SEAMLESS),),
              "clamp harness built; held-out part needs the L_d fit"),
    Falsifier("F24", "g_o, q-hat, L_d, theta_end or the turn model not better calibrated than a context-free constant on "
              "held-out people (q-hat: reliability curve and ECE; mean own-laugh drive)", "held-out calibration",
              (_m("M3", SEAMLESS),), "not built: needs the M3 fits"),
)

BY_ID = {f.fid: f for f in FALSIFIERS}


def rows() -> list:
    """Flat table for results/flist.csv: fid, status, test, milestone, machine, data."""
    out = []
    for f in FALSIFIERS:
        for s in f.stages or (Stage("-", "-", ()),):
            out.append([f.fid, f.status, f.test, s.milestone, s.machine, "; ".join(s.data)])
    return out
