# Quick Demo Project

A simple demonstration project that creates a 45-second explainer video about IAM (Identity and Access Management).

## Usage

```bash
# Run the demo
make build PROJECT=quick-demo

# Or directly
python -m cli.build_project projects/quick-demo/PROMPT_INPUTS.yaml
```

## Expected Output

- `output/script.json` - Generated script
- `output/storyboard.json` - Storyboard with scenes
- `output/timing.json` - Timing information
- `output/video_prompts.json` - Video generation prompts
- `output/voiceover.json` - Voiceover generation data
- `output/final_voiceover.mp3` - Generated audio
- `output/clips/` - Individual video clips
- `output/final_video.mp4` - Final composed video

## Configuration

Edit `PROMPT_INPUTS.yaml` to customize:
- Topic and content
- Duration and pacing
- Video and voice models
- Output settings 