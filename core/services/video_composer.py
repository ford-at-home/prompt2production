"""Video composition for assembling segments with synchronized audio."""

from pathlib import Path
import subprocess
from typing import List, Dict
from core.utils.config import config as global_config
from core.utils.logger import setup_logger


def create_placeholder_video(output_path: str, duration: float, text: str = "") -> bool:
    """Create a simple placeholder video with text overlay.
    
    Args:
        output_path: Path for the output video
        duration: Duration in seconds
        text: Optional text to display
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create a black video with optional text
        filter_complex = f"color=c=black:s=576x320:d={duration}:r=8"
        
        if text:
            # Add text overlay
            filter_complex += f",drawtext=text='{text}':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", filter_complex,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", str(duration),
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception:
        return False


def validate_video_file(video_path: str) -> bool:
    """Check if a file is a valid video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        True if valid video, False otherwise
    """
    path = Path(video_path)
    
    # Check if file exists and has content
    if not path.exists() or path.stat().st_size == 0:
        return False
    
    # Try to probe the file with ffmpeg
    try:
        cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", 
               "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip() == "video"
    except Exception:
        return False


def compose_video_segments(
    video_paths: List[str], 
    audio_path: str, 
    segment_info: List[Dict],
    output_path: str
) -> str:
    """Assemble video segments with synchronized audio.
    
    This function:
    1. Validates all video segments
    2. Creates placeholders for invalid segments
    3. Concatenates all video segments
    4. Overlays the full narration audio
    5. Ensures perfect synchronization
    """
    logger = setup_logger(__name__)
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if we're in stub mode
    if global_config.get('development.use_stubs', True):
        # Create placeholder
        out_file.write_text(
            f"Composed video: {len(video_paths)} segments with audio from {audio_path}"
        )
        return str(out_file)
    
    # Validate and fix video segments
    valid_paths = []
    for i, (path, info) in enumerate(zip(video_paths, segment_info)):
        if validate_video_file(path):
            valid_paths.append(path)
            logger.info(f"Segment {i+1} is valid: {path}")
        else:
            # Create placeholder video
            logger.warning(f"Segment {i+1} is invalid, creating placeholder: {path}")
            duration = info.get('duration', 5)
            text = f"Segment {i+1}"
            
            # Try to create placeholder
            if create_placeholder_video(path, duration, text):
                valid_paths.append(path)
                logger.info(f"Created placeholder for segment {i+1}")
            else:
                # Create a very simple placeholder as last resort
                logger.error(f"Failed to create placeholder for segment {i+1}")
                # Skip this segment
                continue
    
    if not valid_paths:
        logger.error("No valid video segments found")
        # Create a simple error video
        create_placeholder_video(str(out_file), 5, "No valid segments")
        return str(out_file)
    
    # Create a temporary file list for ffmpeg concat
    list_file = out_file.parent / "segments.txt"
    with open(list_file, 'w') as f:
        for path in valid_paths:
            # Ensure paths are absolute and properly escaped
            abs_path = Path(path).absolute()
            # Use forward slashes even on Windows for FFmpeg compatibility
            f.write(f"file '{str(abs_path).replace(chr(92), '/')}'\n")
    
    try:
        # Step 1: Concatenate video segments
        concat_output = out_file.parent / "concatenated.mp4"
        concat_cmd = [
            "ffmpeg",
            "-y",  # Overwrite
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-c", "copy",
            str(concat_output)
        ]
        
        logger.info(f"Concatenating {len(valid_paths)} video segments")
        result = subprocess.run(concat_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Concatenation failed: {result.stderr}")
            # Try alternative concatenation method
            concat_cmd = [
                "ffmpeg",
                "-y"
            ]
            # Add all input files
            for path in valid_paths:
                concat_cmd.extend(["-i", str(path)])
            
            # Use filter_complex for concatenation
            filter_str = "".join(f"[{i}:v][{i}:a]" for i in range(len(valid_paths)))
            filter_str += f"concat=n={len(valid_paths)}:v=1:a=0[v]"
            
            concat_cmd.extend([
                "-filter_complex", filter_str,
                "-map", "[v]",
                str(concat_output)
            ])
            
            subprocess.run(concat_cmd, check=True, capture_output=True)
        
        # Step 2: Add audio track if concatenation succeeded
        if concat_output.exists():
            final_cmd = [
                "ffmpeg",
                "-y",  # Overwrite
                "-i", str(concat_output),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",  # End when shortest stream ends
                str(out_file)
            ]
            
            logger.info("Adding audio track to video")
            subprocess.run(final_cmd, check=True, capture_output=True)
            
            # Cleanup temporary files
            list_file.unlink(missing_ok=True)
            concat_output.unlink(missing_ok=True)
            
            logger.info(f"Successfully composed video: {out_file}")
        else:
            raise Exception("Concatenation output not found")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        # Create fallback video
        create_placeholder_video(str(out_file), 10, "Video composition error")
    except Exception as e:
        logger.error(f"Composition error: {str(e)}")
        # Create fallback video
        create_placeholder_video(str(out_file), 10, "Video composition error")
    
    return str(out_file)


def compose_video(video_path: str, audio_path: str, output_path: str) -> str:
    """Legacy single-video composition for backward compatibility."""
    out_file = Path(output_path)
    
    # Get FFmpeg settings from config
    overwrite = "-y" if global_config.get("pipeline.video_composition.overwrite", True) else "-n"
    video_codec = global_config.get("pipeline.video_composition.video_codec", "copy")
    audio_codec = global_config.get("pipeline.video_composition.audio_codec", "aac")
    additional_flags = global_config.get("pipeline.video_composition.additional_flags", [])
    
    cmd = [
        "ffmpeg",
        overwrite,
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
    ] + additional_flags + [
        out_file.as_posix(),
    ]
    try:  # pragma: no cover - ffmpeg may not be installed
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        placeholder_text = global_config.get('placeholders.composed_video', 'synthetic composed video')
        out_file.write_text(placeholder_text)
    return str(out_file)


def create_video_timeline(segment_info: List[Dict]) -> str:
    """Create an edit decision list (EDL) for reference."""
    timeline = "# Video Timeline\n\n"
    
    for seg in segment_info:
        timeline += f"Segment {seg['index']:02d}: "
        timeline += f"[{seg['start_time']:05.2f} - {seg['end_time']:05.2f}]\n"
        timeline += f"  Duration: {seg['duration']}s\n"
        timeline += f"  Words: {seg['words']}\n"
        timeline += f"  Text: {seg['text'][:50]}...\n\n"
    
    return timeline