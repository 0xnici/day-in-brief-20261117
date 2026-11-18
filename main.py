#!/usr/bin/env python3
"""Entry program: "Sum up 17 November's world news in one image".

The entry is a newspaper front page for Tuesday 17 November 2026, typeset
ahead of time by tools/render.py from that day's wire reporting. Its six
panels carry the US strikes on Qeshm Island and the Tara Gas evacuation,
the strike that closed part of the Crimean Bridge, the outage cascade
across the United States, the loss of US measles elimination status, the
Quad summit in Manila with leaders gathering in Shenzhen, and the appeal
to open Gaza's crossings before winter.

The runner is offline and standard-library only, so the page cannot be
typeset at run time — a legible front page needs the real typesetting
pass, not a runtime guess. What the runner asks for is one file, written
exactly: this program copies the committed page to /output/entry.png
(or to $MAKEFUN_OUTPUT_DIR/entry.png when that is set), reads the copy
back, and fails unless the bytes on disk are the committed page, byte
for byte. The source never changes, so every run writes identical bytes.
"""

import hashlib
import os
import sys

PAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def deliver_page() -> int:
    with open(PAGE_FILE, "rb") as handle:
        page = handle.read()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(page)

    # Read the copy back before reporting success: the entry counts only
    # if the file on disk is the committed page, unchanged, so a short
    # write or a swapped source must fail here rather than pass silently.
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != page:
        print(f"error: {target} does not match the committed page", file=sys.stderr)
        return 1

    digest = hashlib.sha256(page).hexdigest()
    print(f"wrote {target} ({len(page)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(deliver_page())
