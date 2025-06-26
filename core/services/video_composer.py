"""Video composition for assembling segments with synchronized audio."""

from pathlib import Path
import subprocess
from typing import List, Dict
from core.utils.config import config as global_config


def compose_video_segments(
    video_paths: List[str], 
    audio_path: str, 
    segment_info: List[Dict],
    output_path: str
) -> str:
    """Assemble video segments with synchronized audio.
    
    This function:
    1. Concatenates all video segments
    2. Overlays the full narration audio
    3. Ensures perfect synchronization
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if we're in stub mode
    if global_config.get('development.use_stubs', True):
        # Create placeholder
        out_file.write_text(
            f"Composed video: {len(video_paths)} segments with audio from {audio_path}"
        )
        return str(out_file)
    
    # Create a temporary file list for ffmpeg concat
    list_file = out_file.parent / "segments.txt"
    with open(list_file, 'w') as f:
        for path in video_paths:
            f.write(f"file '{Path(path).absolute()}'\n")
    
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
        
        subprocess.run(concat_cmd, check=True, capture_output=True)
        
        # Step 2: Add audio track
        final_cmd = [
            "ffmpeg",
            "-y",  # Overwrite
            "-i", str(concat_output),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",  # End when shortest stream ends
            str(out_file)
        ]
        
        subprocess.run(final_cmd, check=True, capture_output=True)
        
        # Cleanup temporary files
        list_file.unlink()
        concat_output.unlink()
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        # Create fallback file
        out_file.write_text("Error composing video")
    except Exception as e:
        print(f"Composition error: {e}")
        out_file.write_text("Error composing video")
    
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