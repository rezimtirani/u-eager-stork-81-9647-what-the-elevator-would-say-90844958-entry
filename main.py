"""What the Elevator Would Say — a one-line make.fun entry.

An elevator finally gets to talk back: it rides up and down all day,
and the only thanks it ever hears come from people who pressed the
wrong button first. Only the Python standard library is used.
"""

import os
import sys

ELEVATOR_LINE = "I go up and down all day, and the only people who thank me are the ones who pressed the wrong button first."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 120 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 120


def check_line(text):
    """Return the line once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line, not only whitespace, with no trailing newline in the file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be 1 to {MAX_CHARS} characters, got {len(text)}"
        )
    return text


def describe_line(text):
    """Summarise a line the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII line
    reads the same either way while a line with wide characters
    would not. Returns a one-line human-readable summary.
    """
    return (
        f"entry is {len(text)} characters, "
        f"{len(text.encode('utf-8'))} UTF-8 bytes"
    )


def main():
    line = check_line(ELEVATOR_LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise RuntimeError("MAKEFUN_OUTPUT_DIR is not set")
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"wrote {out_path} ({describe_line(line)})")


if __name__ == "__main__":
    main()
