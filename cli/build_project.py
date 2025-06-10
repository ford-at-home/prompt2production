"""CLI entry point for running a project through the pipeline."""

import argparse
from pathlib import Path

try:  # pragma: no cover - optional dependency
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None


def _simple_yaml(text: str) -> dict:
    """Very small YAML subset parser used when PyYAML is unavailable."""
    data = {}
    stack = [(0, data)]
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip()
        while indent < stack[-1][0]:
            stack.pop()
        if value == "":
            new = {}
            stack[-1][1][key] = new
            stack.append((indent + 2, new))
        else:
            if value.startswith("\"") and value.endswith("\"") or value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass
            stack[-1][1][key] = value
    return data

from core.chains.scene_builder import generate_script
from core.chains.storyboard_gen import generate_storyboard
from core.chains.timing_chain import estimate_timing
from core.chains.narrator_voice_gen import build_voiceover
from core.chains.video_prompt_gen import generate_video_prompts
from core.services.replicate_api import render_video
from core.services.video_composer import compose_video
from core.services.s3_deployer import deploy


def build_project(config_path: str) -> None:
    """Run the full pipeline using the given YAML configuration."""

    with open(config_path) as f:
        text = f.read()

    if yaml is not None:
        config = yaml.safe_load(text)
    else:
        config = _simple_yaml(text)

    output_dir = Path(config.get("output_dir", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    script = generate_script(config)
    storyboard = generate_storyboard(script, config)
    video_prompts = generate_video_prompts(storyboard, config)
    timings = estimate_timing(script, config.get("words_per_minute", 120))

    (output_dir / "SCRIPT.md").write_text("\n".join(script))
    (output_dir / "STORYBOARD.md").write_text("\n".join(storyboard))
    timing_lines = [f"{t['seconds']:.2f}s: {t['line']}" for t in timings]
    (output_dir / "TIMED_SCRIPT.md").write_text("\n".join(timing_lines))

    voice_path = build_voiceover(script, config)
    video_path = render_video(video_prompts, voice_path, config)
    final_video = compose_video(video_path, voice_path, output_dir / "final_composed.mp4")

    (output_dir / "transcript.txt").write_text("\n".join(script))
    (output_dir / "render_notes.md").write_text(
        f"Video model: {config.get('video_model', 'unknown')}\n"
    )

    deploy(voice_path, config)
    deploy(final_video, config)

    print("Pipeline complete. Artifacts generated in", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run prompt2production pipeline")
    parser.add_argument("config", help="Path to project YAML configuration")
    args = parser.parse_args()

    build_project(args.config)


if __name__ == "__main__":
    main()
