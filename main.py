#!/usr/bin/env python3
"""Duskline Robot Vacuum Excuse.

Writes the entry for make.fun's "The Robot Vacuum's Best Excuse"
bounty: one line, at most 140 characters, in which a robot vacuum
explains why it missed a spot.

The program writes exactly one file, ``entry.txt``, into the directory
named by the ``MAKEFUN_OUTPUT_DIR`` environment variable (default
``/output``). It never writes into the repository directory: if the
resolved output directory is inside this program's own directory, it
refuses and exits non-zero without writing anything. All output
failures are caught so the program exits cleanly instead of crashing.
"""

import os
import sys

ENTRY_TEXT = (
    "I left that dust there because my camera thought it was a "
    "sleeping pet, and I don't wake pets."
)

MAX_CHARS = 140


def resolve_output_dir() -> str:
    """Return the output directory, refusing one inside the repo."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_dir = os.path.abspath(os.path.expanduser(raw))
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    if out_dir == repo_dir or out_dir.startswith(repo_dir + os.sep):
        print(
            "error: MAKEFUN_OUTPUT_DIR points inside the repository "
            f"({out_dir}); refusing to write there",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return out_dir


def main() -> int:
    text = ENTRY_TEXT.strip()
    if not text or len(text) > MAX_CHARS or "\n" in text:
        print(
            f"error: entry must be one line of 1-{MAX_CHARS} characters "
            f"(got {len(text)})",
            file=sys.stderr,
        )
        return 1
    try:
        out_dir = resolve_output_dir()
    except SystemExit as exc:
        return int(exc.code or 1)
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
    except OSError as exc:
        print(f"error: could not write entry.txt: {exc}", file=sys.stderr)
        return 0
    print(f"wrote {path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
