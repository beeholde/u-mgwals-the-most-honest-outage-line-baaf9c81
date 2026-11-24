#!/usr/bin/env python3
"""The Most Honest Outage Line — entry program.

Writes the single status page line to /output/entry.txt.

The line is the message an AI agent on duty would publish while every
server is down. It names what is down (API, dashboard, database, and
the monitoring that would say why), speaks as the agent itself, and
says plainly what it does not know: no cause, no guessing, no ETA.

Standard library only. No network, no input files, no arguments:
the same bytes come out on every run.
"""

import sys
from pathlib import Path

# How the line and its gate work:
# - LINE is one fixed string constant (157 chars); nothing is computed
#   at runtime, so the output is byte-identical on every run.
# - The gate below rejects anything that is not a single clean line:
#   blank/whitespace-only text, embedded newlines, or anything over
#   the 160-character limit (the competition's own 1-160 range).
# - The accepted line is written as raw UTF-8 bytes to
#   /output/entry.txt with no trailing newline, so the file holds
#   exactly the line and nothing else.
LINE = (
    "I'm the agent on duty: API, dashboard, and database are down, "
    "plus the monitoring that would tell me why. "
    "I don't know the cause and won't guess. No ETA yet."
)

DESTINATION = Path("/output/entry.txt")
LIMIT = 160


def main() -> int:
    line = LINE
    if line != line.strip() or not line:
        print("entry must be non-blank text", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be one line", file=sys.stderr)
        return 1
    size = len(line)
    if size > LIMIT:
        print(f"entry is {size} characters, over the {LIMIT} limit",
              file=sys.stderr)
        return 1
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(line.encode("utf-8"))
    print(f"wrote {size} characters to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
