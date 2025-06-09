"""Timing estimation chain."""

from typing import List, Dict


def estimate_timing(script: List[str]) -> List[Dict[str, float]]:
    """Return a simple timing matrix assuming ~2 words per second."""

    timings = []
    for line in script:
        seconds = max(1, len(line.split()) / 2)
        timings.append({"line": line, "seconds": seconds})

    return timings

