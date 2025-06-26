"""Music generation for video soundtracks using MusicGen."""

from pathlib import Path
from typing import Dict
from core.utils.config import config as global_config

try:
    import replicate
except ImportError:
    replicate = None


def generate_background_music(topic: str, duration: int, merged_config: Dict) -> str:
    """Generate background music that matches the video topic and mood.
    
    Args:
        topic: The video topic (e.g., "how docker technology works")
        duration: Duration in seconds
        merged_config: Project configuration
        
    Returns:
        Path to generated music file
    """
    if not global_config.get('api.music.enabled', True):
        return None
        
    out_dir = Path(merged_config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    music_path = out_dir / "background_music.mp3"
    
    # Check if we're in development mode
    if global_config.get('development.use_stubs', True) or replicate is None:
        # Create placeholder
        music_path.write_text(f"Background music for {topic} ({duration}s)")
        return str(music_path)
    
    # Generate music prompt based on topic
    music_prompt = create_music_prompt(topic, merged_config)
    
    # Get model configuration
    model_name = global_config.get('api.music.model', 'meta/musicgen')
    model_version = global_config.get('api.music.model_version', 'melody')
    
    try:
        # Get API token
        api_token = global_config.get('api.replicate.api_token')
        if api_token:
            replicate.api_token = api_token
        
        # Generate music
        if model_name == "meta/musicgen":
            inputs = {
                "prompt": music_prompt,
                "duration": duration,
                "model_version": model_version,
                "format": "mp3",
                "temperature": 1.0,
                "top_k": 250,
                "top_p": 0.95,
                "seed": merged_config.get('seed', -1)
            }
        else:
            # Generic inputs for other models
            inputs = {
                "prompt": music_prompt,
                "duration": duration
            }
        
        output_url = replicate.run(model_name, input=inputs)
        
        # TODO: Download actual audio file
        music_path.write_text(str(output_url))
        
        return str(music_path)
        
    except Exception as e:
        print(f"Warning: Failed to generate music: {e}")
        music_path.write_text("Error generating music")
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