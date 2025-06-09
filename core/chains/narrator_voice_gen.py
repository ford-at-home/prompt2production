"""Narrator voice generation chain."""

from typing import List

from core.services.elevenlabs_api import synthesize_voice


def build_voiceover(script: List[str], config: dict) -> str:
    """Generate a voiceover file using the ElevenLabs service."""

    text = "\n".join(script)
    return synthesize_voice(text, config)

