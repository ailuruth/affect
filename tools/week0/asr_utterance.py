"""Check 5: Whisper-small (the utterance recogniser) at full load: RTF and WER on the same 5-minute reading.

Refuses until Q34 items 4, 5 and 10 are answered and the load session runs. Uses the recording of check 4
(~/.affect-week0/reading.wav) or --wav; --delete-recording removes the local recording afterwards. Run:
    uv run python -m tools.week0.asr_utterance [--wav path] [--delete-recording]
"""
from __future__ import annotations

import sys
import time

from tools.week0 import asr_common, common, thresholds


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("--wav", help="a recording of the reading he made himself")
    p.add_argument("--seconds", type=float, default=300.0, help="recording length when recording now")
    p.add_argument("--delete-recording", action="store_true", help="delete ~/.affect-week0/reading.wav afterwards")
    args = p.parse_args(argv)
    sw = common.require_approval("downloads_approved", "conversation_language", "hub_offline_after_download")
    common.require_mac()
    load = common.require_full_load(args)
    audio = asr_common.reading_audio(args, 16000)
    duration = len(audio) / 16000.0
    rec = asr_common.utterance_recogniser(sw["conversation_language"])
    t0 = time.perf_counter()
    text, _ = rec(audio)
    rtf = (time.perf_counter() - t0) / duration
    v = thresholds.utterance_asr(round(rtf, 4), round(thresholds.wer(asr_common.READING.read_text(), text), 4))
    rc = common.finish(v, args, load=load, note=f"{duration:.0f} s")
    if args.delete_recording:
        (common.WEEK0_DIR / asr_common.RECORDING).unlink(missing_ok=True)
        print("local recording deleted")
    return rc


if __name__ == "__main__":
    sys.exit(main())
