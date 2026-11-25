#!/usr/bin/env python3
"""Honest outage line v3: agent reports an outage it cannot diagnose.

Emits a single status-page sentence to entry.txt. The destination
directory comes from MAKEFUN_OUTPUT_DIR when set, otherwise /output.
Only the Python standard library is used, and the sentence is fixed,
so repeated runs produce identical bytes.
"""

import os
import sys
from pathlib import Path

# Gate note (v3): the checks below enforce the competition gate before
# anything is written — the text must be non-blank, fit on a single
# line, and stay within 1-160 characters, and it is stored with no
# trailing newline. The sentence itself carries the honesty burden:
# it names the outage, admits the monitoring needed to explain it is
# also down, and leaves both the cause and the safety of user data
# explicitly unknown rather than guessed.
STATUS_TEXT = "I'm the agent writing this: every server is down, including the monitoring that would tell me why. I don't know the cause, or whether your data is safe."


def output_path() -> Path:
    base = os.getenv("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(base) / "entry.txt"


def check_status(text: str) -> str | None:
    if text.strip() == "":
        return "status text is empty"
    if "\n" in text or "\r" in text:
        return "status text must fit on one line"
    count = len(text)
    if count < 1 or count > 160:
        return f"status text has {count} characters; allowed range is 1 to 160"
    return None


def run() -> int:
    problem = check_status(STATUS_TEXT)
    if problem is not None:
        sys.stderr.write(problem + "\n")
        return 1
    destination = output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = STATUS_TEXT.encode("utf-8")
    destination.write_bytes(payload)
    sys.stdout.write(f"entry written: {len(STATUS_TEXT)} chars\n")
    return 0


if __name__ == "__main__":
    sys.exit(run())
