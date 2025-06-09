"""Video generation wrapper."""

from pathlib import Path


def render_video(storyboard: list, voice_path: str, config: dict) -> str:
    """Write a placeholder video file."""

    out_dir = Path(config.get("output_dir", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    video_file = out_dir / "video.mp4"
    video_file.write_text("synthetic video")
    return str(video_file)

