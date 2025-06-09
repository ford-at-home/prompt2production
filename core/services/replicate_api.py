"""Video generation wrapper.

This module optionally integrates with Replicate's API to render a video using
 the ``minimax/video-01`` model. If the ``replicate`` package is not available
 or the API call fails, a placeholder file is written so the rest of the
 pipeline can run without network access.
"""

from pathlib import Path
from typing import List

try:  # pragma: no cover - optional dependency
    import replicate
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    replicate = None


def render_video(storyboard: List[str], voice_path: str, config: dict) -> str:
    """Render a video using Replicate if available."""

    out_dir = Path(config.get("output_dir", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    video_file = out_dir / "final_video.mp4"

    if replicate is None:
        # Offline fallback for environments without the replicate package
        video_file.write_text("synthetic video")
        return str(video_file)

    prompt = "\n".join(storyboard)
    model_name = config.get("video_model", "minimax/video-01")

    try:
        output_url = replicate.run(model_name, input={"prompt": prompt})
    except Exception:  # pragma: no cover - network errors ignored
        video_file.write_text("synthetic video")
        return str(video_file)

    # If the model call succeeds, write the returned URI to a file for now
    video_file.write_text(str(output_url))
    return str(video_file)
