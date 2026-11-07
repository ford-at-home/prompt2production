"""Utilities for cleaning up prompt text."""

import re


def clean_prompt(text: str) -> str:
    """Simplify whitespace and strip markup."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
