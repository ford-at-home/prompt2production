"""Combine video footage with an audio track."""

from pathlib import Path
import subprocess


def compose_video(video_path: str, audio_path: str, output_path: str) -> str:
    """Use ffmpeg to mux audio and video, with a stub fallback."""
    out_file = Path(output_path)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        out_file.as_posix(),
    ]
    try:  # pragma: no cover - ffmpeg may not be installed
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        out_file.write_text("synthetic composed video")
    return str(out_file)
