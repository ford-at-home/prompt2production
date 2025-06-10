"""CLI entry point for running a project through the pipeline."""

import argparse
import json
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None

from core.chains.scene_builder import generate_script
from core.chains.storyboard_gen import generate_storyboard
from core.chains.timing_chain import estimate_timing
from core.chains.narrator_voice_gen import build_voiceover
from core.chains.video_prompt_gen import generate_video_prompts
from core.services.video_composer import compose_video
from core.services.s3_deployer import deploy


def build_project(config_path: str) -> None:
    """Run the full pipeline using the given YAML configuration."""

    if yaml is None:
        raise RuntimeError("pyyaml is required to load project files")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    output_dir = Path(config.get("output_dir", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🚀 Starting prompt2production pipeline...")
    
    # Generate script
    print("📝 Generating script...")
    script_lines = generate_script(config)
    
    # Generate storyboard
    print("🎨 Generating storyboard...")
    storyboard = generate_storyboard(script_lines, config)
    
    # Generate video prompts
    print("🎬 Generating video prompts...")
    video_prompts = generate_video_prompts(script_lines, storyboard, config)
    
    # Estimate timing
    print("⏱️ Estimating timing...")
    timings = estimate_timing(script_lines, config.get("words_per_minute", 120))
    
    # Generate voiceover
    print("🎤 Generating voiceover...")
    voice_path = build_voiceover(script_lines, config)
    
    # Generate and compose video
    print("🎥 Generating and composing video...")
    video_path = compose_video(video_prompts, voice_path, timings, config)
    
    # Save intermediate files
    print("💾 Saving intermediate files...")
    (output_dir / "script.json").write_text(json.dumps({"lines": script_lines}, indent=2))
    (output_dir / "storyboard.json").write_text(json.dumps({"scenes": storyboard}, indent=2))
    (output_dir / "timing.json").write_text(json.dumps({"timings": timings}, indent=2))
    (output_dir / "voiceover.json").write_text(json.dumps({"voice_path": voice_path}, indent=2))
    
    # Deploy if configured
    if config.get("deploy_to_s3", False):
        print("☁️ Deploying to S3...")
        deploy(voice_path, config)
        deploy(video_path, config)

    print("✅ Pipeline complete! Artifacts generated in", output_dir)
    print(f"📁 Final video: {video_path}")
    print(f"🎵 Final audio: {voice_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run prompt2production pipeline")
    parser.add_argument("config", help="Path to project YAML configuration")
    args = parser.parse_args()

    build_project(args.config)


if __name__ == "__main__":
    main()
