"""CLI entry point for running a project through the pipeline."""

import argparse
from pathlib import Path
import time

try:  # pragma: no cover - optional dependency
    import yaml
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None

from core.utils.config import config
from core.utils.logger import setup_logger, log_step, log_timing
import re
from datetime import datetime


def create_project_from_prompt(prompt: str) -> dict:
    """Create a project configuration from a text prompt.
    
    Attempts to extract technical topic and metaphor from the prompt.
    """
    # Generate a project name from timestamp
    project_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Try to extract metaphor patterns
    metaphor_patterns = [
        r"like (?:a |an )?(.+?)(?:\.|$)",
        r"using (?:a |an )?(.+?) metaphor",
        r"as (?:a |an )?(.+?)(?:\.|$)",
        r"explain(?:ed)? (?:like|as) (.+?)(?:\.|$)"
    ]
    
    metaphor_world = None
    for pattern in metaphor_patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            metaphor_world = match.group(1).strip()
            break
    
    # If no metaphor found, use a default
    if not metaphor_world:
        metaphor_world = "everyday life"
    
    # Extract the technical topic (everything before the metaphor part)
    technical_topic = prompt
    if metaphor_world and metaphor_world != "everyday life":
        # Remove the metaphor part from the prompt
        for pattern in metaphor_patterns:
            technical_topic = re.sub(pattern, "", technical_topic, flags=re.IGNORECASE)
        technical_topic = technical_topic.strip().rstrip("?").strip()
    
    # Determine tone based on keywords
    tone = "educational and engaging"
    if any(word in prompt.lower() for word in ["epic", "dramatic", "intense"]):
        tone = "epic and cinematic"
    elif any(word in prompt.lower() for word in ["fun", "playful", "silly"]):
        tone = "playful and fun"
    elif any(word in prompt.lower() for word in ["professional", "serious", "corporate"]):
        tone = "professional"
    
    return {
        "project_name": project_name,
        "technical_topic": technical_topic or prompt,
        "metaphor_world": metaphor_world,
        "narrator_style": "Friendly and clear",
        "scene_count": 5,
        "tone": tone,
        "output_dir": f"output/{project_name}"
    }


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

from core.chains.cohesive_script_builder import generate_cohesive_script, validate_script_timing
from core.chains.segment_visualizer import generate_segment_visuals, create_storyboard_summary
from core.chains.narrator_voice_gen import build_voiceover
from core.services.replicate_api import render_video_segments
from core.services.video_composer import compose_video_segments
from core.services.music_generator import generate_background_music, mix_audio_tracks
from core.services.s3_deployer import deploy
from core.services.dashboard_generator import generate_dashboard, collect_prompts_from_logs


def build_project_from_dict(project_config: dict) -> None:
    """Run the full pipeline using the given project configuration dictionary."""
    # Merge project config with global config
    merged_config = config.merge_project_config(project_config)
    _run_pipeline(merged_config)


def build_project(config_input: str) -> None:
    """Run the full pipeline using the given YAML configuration or text prompt."""
    
    # Check if input is a file path or a text prompt
    if config_input.endswith('.yaml') or config_input.endswith('.yml'):
        # It's a YAML file
        with open(config_input) as f:
            text = f.read()

        if yaml is not None:
            project_config = yaml.safe_load(text)
        else:
            project_config = _simple_yaml(text)
    else:
        # It's a text prompt - create a simple project config
        project_config = create_project_from_prompt(config_input)
    
    build_project_from_dict(project_config)


def _run_pipeline(merged_config: dict) -> None:
    """Execute the actual pipeline with the merged configuration."""
    # Start overall timing
    pipeline_start = time.time()
    
    # Extract project name for logging
    project_name = merged_config.get('project_name', f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Set up logger
    logger = setup_logger(__name__, project_name)
    
    output_dir = Path(merged_config.get("output_dir", config.get("pipeline.output.directory", "output")))
    output_dir.mkdir(parents=True, exist_ok=True)

    topic = merged_config.get('technical_topic', 'your topic')
    duration = merged_config.get('total_duration', config.get('pipeline.video.total_duration', 45))
    
    # Log pipeline start
    logger.info("=" * 60)
    logger.info(f"Starting pipeline for project: {project_name}")
    logger.info(f"Topic: {topic}")
    logger.info(f"Duration: {duration} seconds")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Mode: {'STUB' if config.get('development.use_stubs', True) else 'PRODUCTION'}")
    logger.info("=" * 60)
    
    print(f"\n🎬 Creating {duration}-second video about: {topic}")
    print(f"📁 Output directory: {output_dir}\n")

    # Step 1: Generate cohesive script
    step_start = time.time()
    log_step(logger, 1, "Writing cohesive narration script")
    print("1️⃣  Writing cohesive narration script...")
    full_script, segments = generate_cohesive_script(topic, merged_config)
    log_timing(logger, "Script generation", time.time() - step_start)
    logger.debug(f"Generated {len(segments)} segments with total {sum(s['words'] for s in segments)} words")
    
    # Step 2: Validate timing
    step_start = time.time()
    log_step(logger, 2, "Validating segment timing")
    print("2️⃣  Validating segment timing...")
    segments = validate_script_timing(segments, config.get('pipeline.timing.words_per_minute', 150))
    log_timing(logger, "Timing validation", time.time() - step_start)
    
    # Step 3: Generate visuals for each segment
    step_start = time.time()
    log_step(logger, 3, "Creating visual descriptions for each segment")
    print("3️⃣  Creating visual descriptions for each segment...")
    visual_segments = generate_segment_visuals(topic, segments, merged_config)
    log_timing(logger, "Visual description generation", time.time() - step_start)
    
    # Step 4: Create storyboard
    step_start = time.time()
    log_step(logger, 4, "Generating storyboard")
    print("4️⃣  Generating storyboard...")
    storyboard = create_storyboard_summary(visual_segments)
    log_timing(logger, "Storyboard creation", time.time() - step_start)
    
    # Save intermediate files
    (output_dir / "full_script.txt").write_text(full_script)
    (output_dir / "storyboard.md").write_text(storyboard)
    
    # Save segment breakdown
    segment_breakdown = "\n".join([
        f"[{s['start_time']:02.0f}-{s['end_time']:02.0f}s] {s['text']}"
        for s in segments
    ])
    (output_dir / "segment_breakdown.txt").write_text(segment_breakdown)
    
    # Step 5: Generate voiceover
    step_start = time.time()
    log_step(logger, 5, "Synthesizing voiceover")
    print("5️⃣  Synthesizing voiceover...")
    voice_path = build_voiceover(full_script, merged_config)
    log_timing(logger, "Voice synthesis", time.time() - step_start)
    logger.debug(f"Voice file saved to: {voice_path}")
    
    # Step 6: Generate background music (optional)
    music_path = None
    if config.get('api.music.enabled', False):
        print("6️⃣  Creating background music...")
        music_path = generate_background_music(topic, duration, merged_config)
        
        if music_path:
            # Mix voice with music
            print("   Mixing audio tracks...")
            mixed_audio_path = mix_audio_tracks(
                voice_path, 
                music_path, 
                output_dir / "final_audio.mp3",
                music_volume=0.15  # Keep music subtle
            )
            # Use mixed audio for video
            audio_for_video = mixed_audio_path
        else:
            audio_for_video = voice_path
    else:
        audio_for_video = voice_path
    
    # Step 7: Generate video segments
    step_start = time.time()
    log_step(logger, 7, "Generating video segments", f"{len(visual_segments)} segments")
    print("7️⃣  Generating video segments...")
    video_segments = render_video_segments(visual_segments, merged_config)
    log_timing(logger, "Video segment generation", time.time() - step_start)
    
    # Step 8: Compose final video
    step_start = time.time()
    log_step(logger, 8, "Assembling final video")
    print("8️⃣  Assembling final video...")
    final_video = compose_video_segments(
        video_segments, 
        audio_for_video, 
        visual_segments,
        output_dir / "final_video.mp4"
    )
    log_timing(logger, "Video composition", time.time() - step_start)
    
    # Save metadata
    metadata = {
        'topic': topic,
        'duration': duration,
        'segments': len(segments),
        'words_per_minute': config.get('pipeline.timing.words_per_minute', 150),
        'total_words': sum(s['words'] for s in segments),
        'video_model': merged_config.get('video_model', config.get('api.replicate.video_model', 'unknown'))
    }
    
    import json
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    
    if not config.get('development.use_stubs', True):
        step_start = time.time()
        log_step(logger, 9, "Deploying to S3")
        print("9️⃣  Deploying to S3...")
        deploy(voice_path, merged_config)
        deploy(final_video, merged_config)
        if music_path:
            deploy(music_path, merged_config)
        log_timing(logger, "S3 deployment", time.time() - step_start)

    # Generate dashboard before final summary
    # Prepare project data for dashboard
    project_data = {
        **merged_config,
        'segments': segments,
        'visual_segments': visual_segments,
        'video_model': merged_config.get('video_model', config.get('api.replicate.video_model', 'unknown')),
    }
    
    # Collect prompts from logs
    prompts_log = collect_prompts_from_logs(Path("logs"), project_name)
    
    # Calculate total time before dashboard generation
    total_time = time.time() - pipeline_start
    
    # Generate dashboard
    step_start = time.time()
    log_step(logger, 10, "Generating project dashboard")
    dashboard_path = generate_dashboard(
        project_data,
        output_dir,
        total_time,
        prompts_log
    )
    log_timing(logger, "Dashboard generation", time.time() - step_start)

    # Update total time to include dashboard generation
    total_time = time.time() - pipeline_start
    logger.info("=" * 60)
    logger.info(f"Pipeline completed successfully in {total_time:.2f} seconds")
    logger.info(f"Final video: {final_video}")
    logger.info(f"Total segments: {len(segments)}")
    logger.info(f"Total words: {sum(s['words'] for s in segments)}")
    logger.info("=" * 60)
    
    print(f"\n✅ Video creation complete!")
    print(f"🎥 Final video: {final_video}")
    print(f"📊 Duration: {duration}s | Segments: {len(segments)}")
    print(f"📝 Full script: {output_dir}/full_script.txt")
    print(f"⏱️  Total time: {total_time:.2f}s")
    
    if dashboard_path:
        print(f"📋 Dashboard: {dashboard_path}")
        print(f"\n🌐 Open the dashboard in your browser:")
        print(f"   file://{dashboard_path.absolute()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create beautiful explainer videos with AI",
        epilog="Example: python create_video.py \"how docker technology works\""
    )
    parser.add_argument(
        "topic", 
        help="What to explain (e.g., 'how docker technology works')"
    )
    parser.add_argument(
        "--duration", 
        type=int, 
        default=45,
        help="Total video length in seconds (default: 45)"
    )
    parser.add_argument(
        "--segment", 
        type=int, 
        default=5,
        help="Length of each segment in seconds (default: 5)"
    )
    parser.add_argument(
        "--voice", 
        default="american-male",
        help="Voice style (e.g., 'british-female', 'morgan-freeman')"
    )
    parser.add_argument(
        "--metaphor", 
        default=None,
        help="Visual metaphor to use (e.g., 'shipping containers' for Docker)"
    )
    parser.add_argument(
        "--style", 
        default="clear and engaging",
        help="Narration style (default: 'clear and engaging')"
    )
    parser.add_argument(
        "--music",
        action="store_true",
        default=False,
        help="Add background music to the video"
    )
    parser.add_argument(
        "--no-music",
        action="store_true",
        default=False,
        help="Disable background music"
    )
    args = parser.parse_args()
    
    # Create configuration from arguments
    project_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    config_dict = {
        "project_name": project_name,
        "technical_topic": args.topic,
        "total_duration": args.duration,
        "segment_duration": args.segment,
        "segments": args.duration // args.segment,
        "voice_style": args.voice,
        "metaphor_world": args.metaphor,
        "narrator_style": args.style,
        "tone": "educational",
        "output_dir": f"output/{project_name}"
    }
    
    # Handle music configuration
    if args.music:
        config_dict['enable_music'] = True
    elif args.no_music:
        config_dict['enable_music'] = False
    # Otherwise use config.yaml default
    
    # Save the generated config for reference
    import json
    config_path = Path(config_dict['output_dir']) / 'project_config.json'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    # Run the pipeline
    build_project_from_dict(config_dict)


if __name__ == "__main__":
    main()
