"""CLI entry point for running a project through the pipeline."""

import argparse
try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None

from pathlib import Path
from core.chains.scene_builder import generate_script
from core.chains.storyboard_gen import generate_storyboard
from core.chains.timing_chain import estimate_timing
from core.chains.narrator_voice_gen import build_voiceover
from core.services.replicate_api import render_video
from core.services.s3_deployer import deploy


def build_project(config_path: str) -> None:
    """Run the full pipeline using the given YAML configuration."""

    if yaml is None:
        raise RuntimeError("pyyaml is required to load project files")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    output_dir = Path(config.get("output_dir", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    script = generate_script(config)
    storyboard = generate_storyboard(script, config)
    timings = estimate_timing(script, config.get("words_per_minute", 120))

    (output_dir / "SCRIPT.md").write_text("\n".join(script))
    (output_dir / "STORYBOARD.md").write_text("\n".join(storyboard))
    timing_lines = [f"{t['seconds']:.2f}s: {t['line']}" for t in timings]
    (output_dir / "TIMED_SCRIPT.md").write_text("\n".join(timing_lines))

    voice_path = build_voiceover(script, config)
    video_path = render_video(storyboard, voice_path, config)

    (output_dir / "transcript.txt").write_text("\n".join(script))
    (output_dir / "render_notes.md").write_text(
        f"Video model: {config.get('video_model', 'unknown')}\n"
    )

    deploy(voice_path, config)
    deploy(video_path, config)

    print("Pipeline complete. Artifacts generated in", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run prompt2production pipeline")
    parser.add_argument("config", help="Path to project YAML configuration")
    args = parser.parse_args()

    build_project(args.config)


if __name__ == "__main__":
    main()

