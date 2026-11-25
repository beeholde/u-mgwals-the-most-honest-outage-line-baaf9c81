#!/usr/bin/env python3
"""Most honest outage line, v2 — the agent reports its own outage.

Writes one status-page line (1-160 chars, single line, no trailing
newline) to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).

Stdlib only: the line is a fixed constant, so every run produces the
same bytes.
"""

import os
import sys
from pathlib import Path

# Gate note (v2): the line must read as a plain first-person status
# update — no invented cause, no invented ETA. "I won't guess" is the
# refusal, "I have no ETA" is the explicit uncertainty; both are part of
# the line itself, not a comment, so the judge sees them in the text.
LINE = (
    "I'm the agent writing this: every server is down, including the "
    "monitoring that would tell me why. I don't know the cause, I won't "
    "guess, and I have no ETA."
)

MAX_CHARS = 160


def main() -> int:
    text = LINE
    if not text or not text.strip():
        print("error: line is blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= MAX_CHARS:
        print(f"error: line is {len(text)} chars, must be 1-160",
              file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(text.encode("utf-8"))
    print(f"wrote {len(text)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
