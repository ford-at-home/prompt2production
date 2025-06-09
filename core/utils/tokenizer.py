"""Utility helpers for tokenization."""


def count_tokens(text: str) -> int:
    """Return a naive token count."""

    return len(text.split())

