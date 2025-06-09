"""Tiny wrapper around a hypothetical Bedrock/Nova LLM API."""


def run_prompt(prompt: str) -> str:
    """Return a fake LLM result."""

    return f"[LLM output for: {prompt[:30]}...]"

