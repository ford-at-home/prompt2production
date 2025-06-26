"""Video generation wrapper for segment-based rendering."""

from pathlib import Path
from typing import List, Dict
from core.utils.config import config as global_config

try:  # pragma: no cover - optional dependency
    import replicate
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    replicate = None


def render_video_segments(visual_segments: List[Dict], config: dict) -> List[str]:
    """Render individual video files for each segment.
    
    Returns list of paths to video files.
    """
    out_dir = Path(config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    segments_dir = out_dir / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)
    
    video_paths = []
    
    for segment in visual_segments:
        segment_path = segments_dir / f"segment_{segment['index']:02d}.mp4"
        
        # Check if we're in development mode with stubs
        if global_config.get('development.use_stubs', True) or replicate is None:
            # Create placeholder
            placeholder_text = f"Segment {segment['index']}: {segment['visual_prompt'][:50]}..."
            segment_path.write_text(placeholder_text)
        else:
            # Real video generation
            model_name = config.get("video_model", global_config.get("api.replicate.video_model", "google/veo-3"))
            
            inputs = {
                "prompt": segment['visual_prompt'],
                "duration": segment['duration'],
                "fps": 30,
                "aspect_ratio": "16:9"
            }
            
            # Add seed if specified
            seed = config.get("seed")
            if seed is not None:
                inputs["seed"] = seed + segment['index']  # Vary seed per segment
            
            try:
                # Get API token from config
                api_token = global_config.get('api.replicate.api_token')
                if api_token:
                    replicate.api_token = api_token
                
                output_url = replicate.run(model_name, input=inputs)
                
                # TODO: Download actual video file
                segment_path.write_text(str(output_url))
                
            except Exception as e:
                print(f"Warning: Failed to generate segment {segment['index']}: {e}")
                segment_path.write_text(f"Error generating segment {segment['index']}")
        
        video_paths.append(str(segment_path))
    
    return video_paths


def render_video(prompts: List[str], voice_path: str, config: dict) -> str:
    """Legacy function for backward compatibility."""
    # Convert to segment format
    segments = []
    for i, prompt in enumerate(prompts):
        segments.append({
            'index': i + 1,
            'visual_prompt': prompt,
            'duration': 5,  # Default segment duration
        })
    
    paths = render_video_segments(segments, config)
    
    # Return path to first segment as placeholder
    return paths[0] if paths else "output/video.mp4"