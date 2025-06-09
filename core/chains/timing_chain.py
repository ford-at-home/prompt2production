"""Timing estimation chain."""

from typing import List, Dict

from core.utils.tokenizer import count_tokens


def estimate_timing(script: List[str], wpm: int = 120) -> List[Dict[str, float]]:
    """Return a timing matrix using words-per-minute heuristic."""

    timings = []
    for line in script:
        word_count = count_tokens(line)
        seconds = max(1, (word_count / wpm) * 60)
        timings.append({"line": line, "seconds": seconds})

    return timings
