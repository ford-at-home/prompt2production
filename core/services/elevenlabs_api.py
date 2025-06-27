"""Simple ElevenLabs wrapper."""

import os
from pathlib import Path
from core.utils.config import config as global_config
from core.utils.logger import setup_logger, log_api_call

try:
    import requests
    has_requests = True
except ImportError:
    has_requests = False


def synthesize_voice(text: str, config: dict) -> str:
    """Create an MP3 file with ElevenLabs text-to-speech."""
    logger = setup_logger(__name__)
    
    out_dir = Path(config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    out_dir.mkdir(parents=True, exist_ok=True)
    
    filename = global_config.get("pipeline.output.filenames.voiceover", "final_voiceover.mp3")
    out_file = out_dir / filename
    
    # Check if we're in development mode with stubs
    if global_config.get('development.use_stubs', True) or not has_requests:
        placeholder_text = global_config.get('placeholders.synthetic_audio', 'synthetic audio')
        out_file.write_text(placeholder_text)
        log_api_call(logger, "ElevenLabs", "text-to-speech (stub)", 
                    {"text_length": len(text)}, stub_mode=True)
        return str(out_file)
    
    # Real ElevenLabs API call
    api_key_env = global_config.get('api.elevenlabs.api_key_env', 'ELEVENLABS_API_KEY')
    api_key = os.environ.get(api_key_env)
    
    if not api_key:
        logger.error(f"ElevenLabs API key not found in environment variable {api_key_env}")
        # Create a silent audio file as fallback
        out_file.write_bytes(b'')
        return str(out_file)
    
    voice_id = config.get('voice_id', global_config.get('api.elevenlabs.voice_id', '21m00Tcm4TlvDq8ikWAM'))
    model_id = global_config.get('api.elevenlabs.model_id', 'eleven_monolingual_v1')
    
    # Log API call
    log_api_call(logger, "ElevenLabs", "text-to-speech", 
                {"voice_id": voice_id, "model_id": model_id, "text_length": len(text)}, 
                stub_mode=False)
    
    try:
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Save the audio file
        out_file.write_bytes(response.content)
        logger.info(f"Successfully synthesized voice to {out_file}")
        
    except Exception as e:
        logger.error(f"Error calling ElevenLabs API: {type(e).__name__}: {str(e)}")
        # Create empty file as fallback
        out_file.write_bytes(b'')
    
    return str(out_file)
