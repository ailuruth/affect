"""Instrument and test constants of the evaluation battery (spec §5.0, §5.2-§5.5). These are test instruments, not
engine constants: the engine never reads them (spec §5.0 "Thresholds here are instrument definitions")."""
from __future__ import annotations

# Event instruments (spec §5.0), for eval/events.py at M3 (recorded dyads; not built here: no data in this session).
EVENT_V_MIN = 0.4                 # masked-face V reading that marks an E-trouble / E-need utterance
TROUBLE_WINDOW_S = (0.5, 5.0)     # listener reading window after the utterance end
NEED_WINDOW_S = 20.0              # speaker reading window
LAUGH_E_MIN = 0.25                # E+ on (LP + CR)/2
LAUGH_JAW_HZ = (3.0, 7.0)
SILENCE_MIN_S = 2.0
OPENING_S = 10.0

# E1 lesions (spec §5.2): instances per lesion, a sham of equal size.
LESION_MIN_INSTANCES = 20
# E2 steering (spec §5.3): five strengths per sign, random direction of equal norm as control.
STEER_DOSES = (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)
# E3 surrogates (spec §5.4): 1,000 per test, observed against the 95th percentile; both kinds below required.
SURROGATE_N = 1000
SURROGATE_QUANTILE = 0.95
SURROGATES_REQUIRED = ("segment_shuffle", "data_slide")
SURROGATE_KINDS = ("segment_shuffle", "data_slide", "partner_swap", "timing_resample", "month_swap")
SEGMENT_S = 60.0                  # segment length of the segment-shuffle surrogate
SLIDE_MIN_S = 120.0               # minimum circular shift of the data-sliding surrogate
RESAMPLE_SEG_S = 30.0             # timing-resample: segment length whose duration is redrawn
RESAMPLE_JITTER = 0.25            # timing-resample: each segment's duration scaled by U(1 - j, 1 + j)
MONTH_SWAP_MIN_SESSIONS = 30      # month-swap only after >= 30 operator sessions (spec §5.4)
MONTH_SWAP_MIN_DAYS = 28.0
WINDOWS_S = (2.0, 10.0, 60.0)     # the block-mean metric's windows (spec §5.1 F1, F22)
PRESENT_LAGS_S = (0.0, 0.25, 0.5, 0.75)   # "fast partial coupling at lags < 1 s" (spec §5.4)

# Mirror-only partner (spec §5.4, report 9).
MIRROR_MINUTES = 30.0
MIRROR_LAG_S = 0.3                # the mirror's own latency
MIRROR_GAIN = 1.0
DRIFT_BLOCKS = 6                  # "no channel's mean drifts monotonically over 30 min": 6 blocks of 5 min
DRIFT_TOL_C = 0.1                 # a monotone run of block means counts as drift above 0.1 c_k end to end
LEDGER_FRAMES_MAX = 0.01          # "the ledger changes > 1 % of frames" (F1, F22)

# F22 (spec §5.1, §5.5).
F22_DELAYS_S = (10, 20, 40, 60, 90, 120, 150, 180, 210, 240, 270, 300)
F22_MAX_LAG_S = 300.0
F22_MIN_PEOPLE = 50
F22_SUBSAMPLE_PEOPLE = 25
F22_HOURS_PER_PERSON = 2.0
F22_COPY_LP_S = 60.0              # the copy's low-pass part (onset lobe + 60-s low-pass, as sims/design-g9)

# Run plan (machine.md budget rules; spec §5.5).
SITTING_START_LIMIT_H = 5.0       # no single sitting predicted above 5 h is started without --split or --approved
ASK_LIMIT_H = 6.0                 # machine.md: ask the operator before any run expected over about 6 h
MEMORY_LIMIT_GB = 6.0             # machine.md: plan peak use <= 6 GB per experiment
PERFORMANCE_CORES = 8
