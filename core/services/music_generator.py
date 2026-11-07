"""Music generation for video soundtracks using MusicGen."""

import os
from pathlib import Path
from typing import Dict
from core.utils.config import config as global_config
from core.utils.logger import setup_logger, log_api_call

try:
    import replicate
except ImportError:
    replicate = None
    
try:
    import requests
except ImportError:
    requests = None


def generate_background_music(topic: str, duration: int, merged_config: Dict) -> str:
    """Generate background music that matches the video topic and mood.
    
    Args:
        topic: The video topic (e.g., "how docker technology works")
        duration: Duration in seconds
        merged_config: Project configuration
        
    Returns:
        Path to generated music file
    """
    logger = setup_logger(__name__)
    
    if not global_config.get('api.music.enabled', True):
        return None
        
    out_dir = Path(merged_config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    music_path = out_dir / "background_music.mp3"
    
    # Check if we're in development mode
    if global_config.get('development.use_stubs', True) or replicate is None or requests is None:
        # Create placeholder
        music_path.write_text(f"Background music for {topic} ({duration}s)")
        log_api_call(logger, "Replicate", "music generation (stub)", 
                    {"duration": duration}, stub_mode=True)
        return str(music_path)
    
    # Get API token from environment
    api_token_env = global_config.get('api.replicate.api_token_env', 'REPLICATE_API_TOKEN')
    api_token = os.environ.get(api_token_env)
    
    if not api_token:
        logger.error(f"Replicate API token not found in environment variable {api_token_env}")
        return None
    
    # Generate music prompt based on topic
    music_prompt = create_music_prompt(topic, merged_config)
    
    # Get model configuration
    model_name = global_config.get('api.music.model', 'riffusion/riffusion')
    
    try:
        # Configure Replicate client
        replicate.Client(api_token=api_token)
        
        # Log API call
        log_api_call(logger, "Replicate", "music generation", 
                    {"model": model_name, "duration": duration, "prompt_length": len(music_prompt)}, 
                    stub_mode=False)
        
        # Generate music based on model
        if "riffusion" in model_name:
            inputs = {
                "prompt_a": music_prompt,
                "denoising": 0.75,
                "prompt_strength": 0.5,
                "alpha": 0.5,
                "num_inference_steps": 50,
                "seed_image_id": "vibes"
            }
        elif "musicgen" in model_name:
            inputs = {
                "prompt": music_prompt,
                "duration": duration,
                "model_version": "melody",
                "output_format": "mp3",
                "temperature": 1.0,
                "top_k": 250,
                "top_p": 0.0,
                "classifier_free_guidance": 3.0,
                "seed": -1
            }
        else:
            # Generic inputs
            inputs = {
                "prompt": music_prompt,
                "duration": duration
            }
        
        # Run the model
        output = replicate.run(model_name, input=inputs)
        
        # Handle different output formats
        output_url = None
        
        if hasattr(output, 'read'):
            # It's a file-like object from Replicate
            music_path.write_bytes(output.read())
            logger.info(f"Successfully generated music and saved to {music_path}")
            return str(music_path)
        elif isinstance(output, str):
            output_url = output
        elif isinstance(output, dict) and 'audio' in output:
            output_url = output['audio']
        elif isinstance(output, list) and len(output) > 0:
            output_url = output[0]
        else:
            output_url = str(output)
        
        # Download the audio file if we have a URL
        if output_url and isinstance(output_url, str) and output_url.startswith('http'):
            response = requests.get(output_url, timeout=60)
            response.raise_for_status()
            music_path.write_bytes(response.content)
            logger.info(f"Successfully generated music and saved to {music_path}")
        else:
            logger.error(f"Could not handle output from Replicate: {type(output)}")
            return None
        
        return str(music_path)
        
    except Exception as e:
        logger.error(f"Failed to generate music: {type(e).__name__}: {str(e)}")
        return None


def create_music_prompt(topic: str, config: Dict) -> str:
    """Create a music generation prompt based on the video topic.
    
    Maps technical topics to appropriate musical styles.
    """
    # Extract key themes
    topic_lower = topic.lower()
    
    # Determine music style based on topic
    if any(word in topic_lower for word in ['technology', 'tech', 'software', 'computer', 'digital', 'ai']):
        base_style = "ambient electronic, tech house, futuristic"
        mood = "innovative, forward-thinking"
    elif any(word in topic_lower for word in ['science', 'biology', 'chemistry', 'physics', 'nature']):
        base_style = "atmospheric, orchestral, documentary"
        mood = "wonder, discovery"
    elif any(word in topic_lower for word in ['business', 'finance', 'corporate', 'management']):
        base_style = "corporate, uplifting, professional"
        mood = "confident, productive"
    elif any(word in topic_lower for word in ['health', 'medical', 'medicine', 'wellness']):
        base_style = "calming, healing, ambient"
        mood = "peaceful, reassuring"
    elif any(word in topic_lower for word in ['history', 'ancient', 'classical', 'traditional']):
        base_style = "orchestral, period-appropriate, cinematic"
        mood = "epic, timeless"
    else:
        base_style = "ambient, educational, modern"
        mood = "engaging, clear"
    
    # Get tone from config
    tone = config.get('tone', 'educational')
    
    # Build the prompt
    if tone == 'epic':
        return f"{base_style}, epic cinematic, {mood}, dramatic builds"
    elif tone == 'playful':
        return f"{base_style}, upbeat, playful, {mood}, light and fun"
    elif tone == 'professional':
        return f"{base_style}, {mood}, sophisticated, subtle"
    else:  # educational
        return f"{base_style}, {mood}, clear, supportive, not distracting"


def mix_audio_tracks(voice_path: str, music_path: str, output_path: str, music_volume: float = 0.2) -> str:
    """Mix voice narration with background music.
    
    Args:
        voice_path: Path to voice narration
        music_path: Path to background music
        output_path: Output path for mixed audio
        music_volume: Volume level for music (0.0-1.0)
    """
    import subprocess
    from pathlib import Path
    
    out_file = Path(output_path)
    
    if global_config.get('development.use_stubs', True):
        out_file.write_text(f"Mixed audio: voice + music at {music_volume} volume")
        return str(out_file)
    
    try:
        # FFmpeg command to mix audio
        # -filter_complex creates a mixing graph
        cmd = [
            "ffmpeg",
            "-y",
            "-i", voice_path,
            "-i", music_path,
            "-filter_complex",
            f"[1:a]volume={music_volume}[music];[0:a][music]amix=inputs=2:duration=shortest",
            "-ac", "2",  # Stereo output
            str(out_file)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return str(out_file)
        
    except subprocess.CalledProcessError as e:
        print(f"Audio mixing error: {e.stderr.decode() if e.stderr else 'Unknown'}")
        # Fall back to voice only
        subprocess.run(["cp", voice_path, str(out_file)])
        return str(out_file)
    except Exception as e:
        print(f"Mixing error: {e}")
        return voice_path