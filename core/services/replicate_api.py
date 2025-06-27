"""Video generation wrapper for segment-based rendering."""

import os
from pathlib import Path
from typing import List, Dict
from core.utils.config import config as global_config
from core.utils.logger import setup_logger, log_api_call

try:  # pragma: no cover - optional dependency
    import replicate
    has_replicate = True
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    replicate = None
    has_replicate = False
    
try:
    import requests
except ImportError:
    requests = None


def estimate_generation_time(model_name: str, duration: int) -> str:
    """Estimate generation time based on model and duration.
    
    Returns a human-readable time estimate.
    """
    # Time estimates based on model performance
    if "google/veo" in model_name:
        time_min = 3 * duration / 5  # ~3-5 minutes per 5s
        time_max = 5 * duration / 5
    elif "tencent/hunyuan-video" in model_name:
        time_min = 4 * duration / 5  # ~4-6 minutes per 5s
        time_max = 6 * duration / 5
    elif "minimax/video-01" in model_name:
        time_min = 2.5  # ~2.5-3.5 minutes for 6s
        time_max = 3.5
    elif "kling" in model_name:
        if "pro" in model_name:
            time_min = 4  # ~4-6 minutes for pro
            time_max = 6
        else:
            time_min = 3  # ~3-4 minutes for standard
            time_max = 4
    elif "ltx-video" in model_name:
        time_min = 0.5  # ~30-60 seconds (real-time)
        time_max = 1
    elif "zeroscope" in model_name:
        time_min = 1  # ~1-2 minutes
        time_max = 2
    else:
        time_min = 2  # Default estimate
        time_max = 4
    
    if time_max < 1:
        return f"{int(time_min * 60)}-{int(time_max * 60)} seconds"
    else:
        return f"{time_min:.1f}-{time_max:.1f} minutes"


def render_video_segments(visual_segments: List[Dict], config: dict) -> List[str]:
    """Render individual video files for each segment.
    
    Returns list of paths to video files.
    """
    logger = setup_logger(__name__)
    
    out_dir = Path(config.get("output_dir", global_config.get("pipeline.output.directory", "output")))
    segments_dir = out_dir / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)
    
    video_paths = []
    
    # Check if we're in development mode with stubs
    if global_config.get('development.use_stubs', True) or not has_replicate or requests is None:
        # Create placeholder videos
        for segment in visual_segments:
            segment_path = segments_dir / f"segment_{segment['index']:02d}.mp4"
            placeholder_text = f"Segment {segment['index']}: {segment['visual_prompt'][:50]}..."
            segment_path.write_text(placeholder_text)
            video_paths.append(str(segment_path))
            log_api_call(logger, "Replicate", "video generation (stub)", 
                        {"segment": segment['index']}, stub_mode=True)
        return video_paths
    
    # Get API token from environment
    api_token_env = global_config.get('api.replicate.api_token_env', 'REPLICATE_API_TOKEN')
    api_token = os.environ.get(api_token_env)
    
    if not api_token:
        logger.error(f"Replicate API token not found in environment variable {api_token_env}")
        return []
    
    # Real video generation
    model_name = config.get("video_model", global_config.get("api.replicate.video_model", "anotherjesse/zeroscope-v2-xl"))
    
    for segment in visual_segments:
        segment_path = segments_dir / f"segment_{segment['index']:02d}.mp4"
        
        # Prepare inputs based on model
        if "google/veo" in model_name:
            # Google Veo 3 - State of the art
            inputs = {
                "prompt": segment['visual_prompt'],
                "aspect_ratio": "16:9",
                "duration": segment['duration'],
                "quality": "high",  # Options: "standard", "high"
                "enable_audio": True,  # Native audio generation!
                "seed": config.get("seed", 42)
            }
        elif "tencent/hunyuan-video" in model_name:
            # HunyuanVideo - 13B parameter open-source
            inputs = {
                "prompt": segment['visual_prompt'],
                "resolution": "1280x720",  # Options: "1280x720", "960x960", "720x1280"
                "video_length": segment['duration'],
                "guidance_scale": 7.0,
                "num_inference_steps": 50,  # More steps = better quality
                "flow_shift": 0,  # Controls motion amount
                "embedded_guidance_scale": 6.0,
                "seed": config.get("seed", 42)
            }
        elif model_name == "minimax/video-01":
            # MiniMax Hailuo - Exceptional realism
            inputs = {
                "prompt": segment['visual_prompt'],
                "prompt_optimizer": True,  # Auto-enhance prompts
                "model": "video-01",
                "duration": min(segment['duration'], 6)  # Max 6 seconds
            }
        elif model_name == "minimax/video-01-director":
            # MiniMax Director - Cinematic camera control
            inputs = {
                "prompt": segment['visual_prompt'],
                "camera_mode": "auto",  # Options: "auto", "zoom_in", "zoom_out", "pan_left", "pan_right", "tilt_up", "tilt_down"
                "duration": min(segment['duration'], 6),
                "prompt_optimizer": True
            }
        elif "kling" in model_name:
            # Kling models - Highest resolution
            inputs = {
                "prompt": segment['visual_prompt'],
                "aspect_ratio": "16:9",
                "duration": min(segment['duration'], 10),  # 5 or 10 seconds
                "mode": "standard" if "standard" in model_name else "pro",
                "camera_motion": "auto"  # Professional camera movements
            }
        elif "mochi" in model_name:
            # Genmo Mochi - 10B params, fine-tunable
            inputs = {
                "prompt": segment['visual_prompt'],
                "num_frames": int(segment['duration'] * 30),  # 30 fps
                "num_inference_steps": 64,
                "guidance_scale": 4.5,
                "seed": config.get("seed", 42)
            }
        elif "ltx-video" in model_name:
            # LTX-Video - Real-time generation
            inputs = {
                "prompt": segment['visual_prompt'],
                "num_frames": int(segment['duration'] * 24),  # 24 fps
                "width": 768,
                "height": 512,
                "guidance_scale": 7.5,
                "num_inference_steps": 25,  # Fewer steps for speed
                "seed": config.get("seed", 42)
            }
        elif "stable-video-diffusion" in model_name:
            # Stability AI SVD
            inputs = {
                "prompt": segment['visual_prompt'],
                "num_frames": 25,  # Fixed at 25 frames
                "sizing_strategy": "maintain_aspect_ratio",
                "motion_bucket_id": 127,  # Controls motion amount
                "cond_aug": 0.02,
                "decoding_t": 14,
                "seed": config.get("seed", 42)
            }
        elif "zeroscope" in model_name:
            # Zeroscope - Fast but lower quality
            inputs = {
                "prompt": segment['visual_prompt'],
                "num_frames": int(segment['duration'] * 8),  # 8 fps
                "height": 320,
                "width": 576,
                "num_inference_steps": 50,
                "guidance_scale": 17.5,
                "negative_prompt": "very blue, dust, noisy, washed out, ugly, distorted, broken",
                "fps": 8,
                "seed": config.get("seed", 42)
            }
        else:
            # Generic inputs for unknown models
            inputs = {
                "prompt": segment['visual_prompt']
            }
            if hasattr(segment, 'duration'):
                inputs["duration"] = segment['duration']
        
        # Get retry configuration
        max_retries = global_config.get('retry.max_attempts', 3) if "google/veo" in model_name or "hunyuan" in model_name else 1
        retry_delay = global_config.get('retry.delay_seconds', 30)
        
        for attempt in range(max_retries):
            try:
                # Configure Replicate client
                if has_replicate:
                    replicate.Client(api_token=api_token)
                
                # Log expected generation time
                expected_time = estimate_generation_time(model_name, segment['duration'])
                logger.info(f"Expected generation time: {expected_time}")
                
                # Log API call
                log_api_call(logger, "Replicate", "video generation", 
                            {"model": model_name, "segment": segment['index'], "duration": segment['duration'], "attempt": attempt + 1}, 
                            stub_mode=False)
                
                # Run the model
                if attempt > 0:
                    logger.info(f"Retry {attempt + 1}/{max_retries}: Generating video segment {segment['index']} with {model_name}")
                else:
                    logger.info(f"Generating video segment {segment['index']} with {model_name}")
                
                # Set timeout based on model
                import replicate.client
                if "google/veo" in model_name or "hunyuan" in model_name:
                    # Longer timeout for premium models
                    timeout_seconds = global_config.get('retry.timeout_minutes', 10) * 60
                    client = replicate.Client(api_token=api_token)
                    client.timeout = timeout_seconds
                    output = client.run(model_name, input=inputs)
                else:
                    output = replicate.run(model_name, input=inputs)
                
                # Handle different output formats
                handled = False
                
                if hasattr(output, 'read'):
                    # It's a file-like object from Replicate
                    logger.info(f"Downloading segment {segment['index']} directly from file object")
                    segment_path.write_bytes(output.read())
                    logger.info(f"Successfully generated and saved segment {segment['index']} to {segment_path}")
                    handled = True
                else:
                    # Try to get URL from various formats
                    output_url = None
                    if isinstance(output, str):
                        output_url = output
                    elif isinstance(output, dict) and 'video' in output:
                        output_url = output['video']
                    elif isinstance(output, list) and len(output) > 0:
                        output_url = output[0]
                    else:
                        output_url = str(output)
                    
                    # Download the video file if we have a URL
                    if output_url and isinstance(output_url, str) and output_url.startswith('http'):
                        logger.info(f"Downloading segment {segment['index']} from {output_url}")
                        response = requests.get(output_url, timeout=300)  # 5 minute timeout
                        response.raise_for_status()
                        segment_path.write_bytes(response.content)
                        logger.info(f"Successfully generated and saved segment {segment['index']} to {segment_path}")
                        handled = True
                
                if not handled:
                    logger.error(f"Could not handle output from Replicate for segment {segment['index']}: {type(output)}")
                    # Create empty file as placeholder
                    segment_path.write_bytes(b'')
                else:
                    # Success! Break out of retry loop
                    break
                    
            except Exception as e:
                logger.error(f"Failed to generate segment {segment['index']} (attempt {attempt + 1}/{max_retries}): {type(e).__name__}: {str(e)}")
                
                # If not the last attempt, wait before retrying
                if attempt < max_retries - 1:
                    logger.info(f"Waiting {retry_delay} seconds before retry...")
                    import time
                    time.sleep(retry_delay)
                else:
                    # Final attempt failed, create empty file as placeholder
                    logger.error(f"All attempts failed for segment {segment['index']}")
                    segment_path.write_bytes(b'')
        
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