# prompt2production

**prompt2production** is a generative media pipeline for turning technical topics into cinematic, metaphor-driven explainers.

Install dependencies with:

```bash
pip install -r requirements.txt
```

It uses:
- LLMs for scripting (via Bedrock/Nova)
- Voice cloning APIs (like ElevenLabs)
- Video/image generation (like Sora, Replicate, Runway)
- A structured prompt chaining system to stitch everything together

🎬 Input: YAML file describing a project
📦 Output: Fully formed narrative, storyboard, timing, and downloadable media artifacts

Use it for:
- Security training
- DevRel content
- Internal onboarding
- Just plain fun

## Example: IAM-POSSIBLE

The `projects/iam-possible` folder shows a complete run of the pipeline. It presents AWS Identity and Access Management as a Tarantino-style nightclub heist narrated by a cocky hacker with Samuel L. Jackson flair. Running this project generates a script, storyboard, and timing matrix, then renders a final voiceover and video using services like ElevenLabs and Sora. All produced assets are uploaded to a rate-limited S3 bucket.

## Pipeline Overview

See [EXPLAINER.md](EXPLAINER.md) for a full walkthrough of how the pipeline works.

The `projects/iam-possible` folder shows a complete run of the pipeline. It
presents AWS Identity and Access Management as a Tarantino-style nightclub
heist narrated by a cocky hacker with Samuel L. Jackson flair. Running this
project generates a script, storyboard, and timing matrix, then renders a final
voiceover and video using services like ElevenLabs and Sora. All produced
assets are uploaded to a rate-limited S3 bucket.

## Pipeline Overview

1. **Define your project** in a YAML file (see `projects/iam-possible/PROMPT_INPUTS.yaml`).
2. **Run the pipeline**:

   ```bash
   make build PROJECT=iam-possible
   python -m cli.build_project path/to/PROMPT_INPUTS.yaml
   ```
3. `scene_builder` uses an LLM to draft each scene's narration.
4. `storyboard_gen` converts narration into visual prompts.
5. `timing_chain` estimates how long each line will take.
6. `narrator_voice_gen` calls ElevenLabs to create an audio track.
7. `replicate_api` (or Sora) renders the final video using the storyboard and audio.
8. `s3_deployer` uploads the assets so they can be downloaded or shared.

This repository contains lightweight stubs for each step so you can see how the pieces fit together before plugging in real API keys and logic.

## Configuration

The pipeline expects a few environment variables so it can connect to external services:

- `ELEVENLABS_API_KEY` – used for voice synthesis.
- `REPLICATE_API_TOKEN` – required for video generation with Replicate.

By default the video step calls the `minimax/video-01` model on Replicate. If the `replicate` package is not installed or the API call fails, a placeholder file is created so you can test the rest of the pipeline offline. Text-to-text prompts use AWS Bedrock's Nova model, which reads credentials from your `~/.aws/credentials` file.
This repository contains lightweight stubs for each step so you can see how the
pieces fit together before plugging in real API keys and logic.
