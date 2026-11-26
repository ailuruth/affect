"""Check 2: capture-to-screen pipeline time, p99, read from the 240-fps rig video (spec §2.2 rig).

The rig: a phone or tablet in front of the camera plays a looped face video with sharp lip-corner-pull onsets and
flashes a white square in a corner on the same frame as each onset; a second phone films that screen and the Mac's
screen at 240 fps for at least 50 onsets, while the load session runs. The page marks each onset it renders with a
white square in a corner of the Mac's screen. Give the two squares' regions in the video (x,y,w,h in pixels); the lag
is the Mac square's rise minus the phone square's rise, frame by frame (about 4 ms resolution). The video stays on
the Mac (it is only read). A photodiode trace pair (CSV: t_s,flash,screen) can replace the video (--photodiode).
    uv run python -m tools.week0.echo_rig VIDEO --flash-roi x,y,w,h --screen-roi x,y,w,h [--fps 240]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from tools.week0 import common, measure, page_checks, thresholds

MIN_ONSETS = 50


def _roi(s: str):
    x, y, w, h = (int(v) for v in s.split(","))
    return x, y, w, h


def traces_from_video(path: Path, rois, fps_override=None):
    cv2 = common.lazy("cv2", "uv pip install opencv-python (not in the extras; an addition to approve)")
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise common.Refused(f"cannot open {path}")
    fps = fps_override or cap.get(cv2.CAP_PROP_FPS)
    out = [[] for _ in rois]
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for i, (x, y, w, h) in enumerate(rois):
            out[i].append(float(gray[y:y + h, x:x + w].mean()))
    cap.release()
    return fps, out


def main(argv=None) -> int:
    p = common.parser(__doc__)
    p.add_argument("video", nargs="?", help="the rig video (stays local)")
    p.add_argument("--flash-roi", type=_roi)
    p.add_argument("--screen-roi", type=_roi)
    p.add_argument("--fps", type=float, help="override the container's frame rate (240 by default on most phones)")
    p.add_argument("--photodiode", help="CSV t_s,flash,screen instead of a video")
    args = p.parse_args(argv)
    common.require_approval(*page_checks.CAMERA_SWITCHES)
    common.require_mac()
    if args.photodiode:
        rows = list(csv.reader(Path(args.photodiode).open()))
        t = [float(r[0]) for r in rows if r and r[0][0].isdigit()]
        fps = (len(t) - 1) / (t[-1] - t[0])
        flash = [float(r[1]) for r in rows if r and r[0][0].isdigit()]
        screen = [float(r[2]) for r in rows if r and r[0][0].isdigit()]
    else:
        if not (args.video and args.flash_roi and args.screen_roi):
            p.error("VIDEO, --flash-roi and --screen-roi are needed (or --photodiode)")
        fps, (flash, screen) = traces_from_video(Path(args.video), (args.flash_roi, args.screen_roi), args.fps)
    lags = measure.pair_onsets(measure.rising_crossings(flash, fps), measure.rising_crossings(screen, fps))
    if len(lags) < MIN_ONSETS:
        raise common.Refused(f"only {len(lags)} onsets paired (at least {MIN_ONSETS} needed)")
    v = thresholds.pipeline(round(1000.0 * thresholds.percentile(lags, 99), 2))
    return common.finish(v, args, load="as recorded (load session during the video)",
                         note=f"{len(lags)} onsets at {fps:.0f} fps")


if __name__ == "__main__":
    sys.exit(main())
