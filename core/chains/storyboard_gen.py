"""Storyboard generation chain."""

from typing import List


def generate_storyboard(script: List[str]) -> List[str]:
    """Create a simple visual description for each line of script."""

    return [f"Visual: {line}" for line in script]

