"""Timing estimation chain."""

from typing import List, Dict
from core.utils.tokenizer import count_tokens
from core.utils.config import config as global_config


def estimate_timing(script: List[str], wpm: int = None) -> List[Dict[str, float]]:
    """Return a timing matrix using words-per-minute heuristic."""
    if wpm is None:
        wpm = global_config.get('pipeline.timing.words_per_minute', 120)
    
    min_seconds = global_config.get('pipeline.timing.minimum_seconds_per_line', 1.0)
    
    timings = []
    for line in script:
        word_count = count_tokens(line)
        seconds = max(min_seconds, (word_count / wpm) * 60)
        timings.append({"line": line, "seconds": seconds})

    return timings
