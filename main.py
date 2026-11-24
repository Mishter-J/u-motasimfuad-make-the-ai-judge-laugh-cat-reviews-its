"""Make the AI Judge Laugh: Cat Reviews Its Human.

Writes one funny single-line one-star review from a house cat about its
human to /output/entry.txt.

The review is a fixed string literal. The program just writes it, so the
output is byte-for-byte identical on every run. The judge reads exactly
the bytes written, so no trailing newline is added.

Standard library only. No network access, no randomness, no arguments.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

REVIEW = (
    "One star. My human bought a $400 cat bed and I sleep in the box. "
    "Dear judge, the box cost $0, fits one (1) perfect cat, "
    "and has 5 stars from me."
)


def main() -> None:
    # The gate: 1 to 200 characters, a single line, not only whitespace.
    # Fail loudly here rather than writing an entry the scorer would refuse.
    if not 1 <= len(REVIEW) <= 200 or "\n" in REVIEW or not REVIEW.strip():
        raise SystemExit("review violates the entry gate (1-200 chars, one line)")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / "entry.txt"
    dest.write_text(REVIEW, encoding="utf-8")
    # Guard against a truncated or partial write: the file must be the
    # exact bytes of the review.
    if dest.read_text(encoding="utf-8") != REVIEW:
        dest.unlink(missing_ok=True)
        raise SystemExit("entry.txt does not match the review")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
