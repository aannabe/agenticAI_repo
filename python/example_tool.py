"""Example script showing the project's Python conventions.

Run:  uv run python/example_tool.py 3 1 4 1 5
Delete or replace this file when you add real code.
"""

from __future__ import annotations

import argparse
import statistics
from collections.abc import Sequence


def summarize(values: Sequence[float]) -> dict[str, float]:
    """Return the count, minimum, maximum and mean of ``values``.

    Raises ValueError if ``values`` is empty (there is nothing to summarize).
    """
    if not values:
        raise ValueError("values must not be empty")
    return {
        "count": float(len(values)),
        "min": min(values),
        "max": max(values),
        "mean": statistics.fmean(values),  # fmean: fast float mean from the standard library
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point; returns a process exit code."""
    parser = argparse.ArgumentParser(description="Summarize a list of numbers.")
    parser.add_argument("numbers", nargs="+", type=float, help="numbers to summarize")
    args = parser.parse_args(argv)

    for name, value in summarize(args.numbers).items():
        print(f"{name}: {value:g}")  # :g prints 3.0 as "3" and keeps other values compact
    return 0


if __name__ == "__main__":  # only run main() when executed as a script, not when imported
    raise SystemExit(main())
