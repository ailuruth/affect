"""Check 4: Kyutai STT 1B at full load: language, word-end-to-delivery p90, WER on the 5-minute reading, RTF.

Refuses until Q34 items 4 (models), 5 (his conversation language) and 10 (offline) are answered and the load
session runs. The reading (tools/week0/reading.txt, read aloud by him) is recorded once to ~/.affect-week0/
reading.wav (or given with --wav) and reused by check 5. Delivery latency: the frames arrive in real time and are
processed in order (`measure.realtime_finish`); each streamed word is delivered when its last piece is emitted;
word ends come from Whisper-small's word timestamps on the same recording (the reference alignment). Run:
    uv run python -m tools.week0.asr_stream [--wav path]
"""
from __future__ import annotations

import sys

from tools.week0 import asr_common, common, measure, thresholds


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--wav", help="a recording of the reading he made himself (WAV, or anything afconvert reads)")
    p.add_argument("--seconds", type=float, default=300.0, help="recording length when recording now")
    args = p.parse_args(argv)
    sw = common.require_approval("downloads_approved", "conversation_language", "hub_offline_after_download")
    common.require_mac()
    load = common.require_full_load(args)
    language = sw["conversation_language"]
    ref_text = asr_common.READING.read_text()
    audio24 = asr_common.reading_audio(args, 24000)
    duration = len(audio24) / 24000.0
    rec = asr_common.stream_recogniser()
    pieces = rec(audio24)
    compute = rec.last_compute
    words = asr_common.stream_words(pieces)
    finish = measure.realtime_finish(compute, asr_common.FRAME_S)
    _, ref_words = asr_common.utterance_recogniser(language)(asr_common.reading_audio(args, 16000))
    lat = measure.delivery_latencies(words, finish, ref_words)
    if len(lat) < 50:
        raise common.Refused(f"only {len(lat)} words matched the reference alignment; check the recording")
    v = thresholds.stream_asr(language, round(thresholds.percentile(lat, 90), 3),
                              round(thresholds.wer(ref_text, " ".join(w for w, _ in words)), 4),
                              round(sum(compute) / duration, 4))
    return common.finish(v, args, load=load, note=f"{len(lat)} matched words, {duration:.0f} s")


if __name__ == "__main__":
    sys.exit(main())
