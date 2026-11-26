"""Shared part of checks 1 and 3, which read numbers the browser page measures (web/, M2's tracking part): the
page POSTs them to 127.0.0.1 (loopback only) or saves them to a JSON file given with --from-file.

The camera opens in the page only, and only after Q34 items 5 (no live session before his language) and 10
(offline) are answered; the face tracker's model is one of the Q34 item 4 downloads."""
from __future__ import annotations

from tools.week0 import common

CAMERA_SWITCHES = ("downloads_approved", "conversation_language", "hub_offline_after_download")


def args_with_file(doc: str):
    p = common.parser(doc)
    p.add_argument("--from-file", help="a JSON list of samples the page saved (instead of receiving them live)")
    return p


def prepare(args) -> str:
    common.require_approval(*CAMERA_SWITCHES)
    common.require_mac()
    return common.require_full_load(args)
