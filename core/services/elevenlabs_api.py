"""Simple ElevenLabs wrapper."""

from pathlib import Path


def synthesize_voice(text: str, config: dict) -> str:
    """Pretend to create an MP3 file with ElevenLabs."""

    out_dir = Path(config.get("output_dir", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "final_voiceover.mp3"
    out_file.write_text("synthetic audio")
    return str(out_file)
