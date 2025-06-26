"""Simple ElevenLabs wrapper."""

from pathlib import Path
from core.utils.config import config as global_config


def synthesize_voice(text: str, config: dict) -> str:
    """Pretend to create an MP3 file with ElevenLabs."""
    out_dir = Path(config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    out_dir.mkdir(parents=True, exist_ok=True)
    
    filename = global_config.get("pipeline.output.filenames.voiceover", "final_voiceover.mp3")
    out_file = out_dir / filename
    
    # Check if we're in development mode with stubs
    if global_config.get('development.use_stubs', True):
        placeholder_text = global_config.get('placeholders.synthetic_audio', 'synthetic audio')
        out_file.write_text(placeholder_text)
    else:
        # TODO: Implement real ElevenLabs API call
        # api_key = global_config.get('api.elevenlabs.api_key')
        # voice_id = config.get('voice_id', global_config.get('api.elevenlabs.voice_id'))
        # model_id = global_config.get('api.elevenlabs.model_id')
        out_file.write_text("synthetic audio")
    
    return str(out_file)
