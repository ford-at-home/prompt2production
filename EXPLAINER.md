# EXPLAINER.md – How `prompt2production` Works

This document provides a comprehensive walkthrough of how the `prompt2production` framework operates. It describes the purpose, architecture, components, and the step-by-step workflow used to generate fully-formed cinematic explainers from simple YAML inputs.

---

## 🧐 Purpose

`prompt2production` is a modular AI-powered pipeline that transforms a **technical topic** and a **creative metaphor** into a complete set of production-ready media artifacts. Think: explainer videos styled like Tarantino films or Pixar shorts—educational, entertaining, and visually arresting.

It’s designed for developers, DevRel professionals, security educators, and AI creatives who want to tell powerful technical stories through stylized multimedia.

---

## 🧑‍🏫 Architecture

PROMPT_INPUTS.yaml
↓
SceneBuilder (LLM)
↓
Voiceover Script (SCRIPT.md)
↓
Storyboard Prompt Generator (LLM)
↓
Visual Prompts (STORYBOARD.md)
↓
Timing Estimator
↓
Timed Script (TIMED_SCRIPT.md)
↓
Optional Rendering (via APIs)
↓
Packaged Output
↓
S3 Deployment (with request limiter)

---

## 🗂 Directory Breakdown

- `core/`: Shared logic across all projects
  - `chains/`: Prompt chains for script, storyboard, voice, timing
  - `templates/`: Jinja2 templates for prompts
  - `services/`: API wrappers for LLMs, voice, and video
  - `utils/`: Helpers like token counters
- `projects/`: Project-specific content (e.g. IAM-POSSIBLE)
- `output/`: Generated assets
- `cli/`: Entry point for automated chains
- `Makefile`: Build automation

---

## 🤐 Workflow Explained

### 1. Author `PROMPT_INPUTS.yaml`
This file contains the blueprint for your video:

```yaml
technical_topic: "AWS IAM"
metaphor_world: "Nightclub security"
narrator_style: "Samuel L. Jackson"
scene_count: 18
tone: "Cocky, cinematic, accurate"
voice_model: "ElevenLabs"
video_model: "Sora"
```

### 2. Run the Project Build
```bash
make build PROJECT=iam-possible
```
This launches the following chain of events:

### 3. SceneBuilder Chain (`scene_builder.py`)
Splits the story into `scene_count` sections
Prompts the LLM (via Bedrock Nova or Claude) to write a line of VO per scene
Output → `SCRIPT.md`
Template: `vo_prompt.jinja`

### 4. Storyboard Generator (`storyboard_gen.py`)
Converts each scene’s VO line into a vivid visual description
Uses metaphor context + narrator tone + scene number
Output → `STORYBOARD.md`
Template: `visual_prompt.jinja`

### 5. Timing Estimator (`timing_chain.py`)
Tokenizes each VO line
Estimates playback time using either:
- ElevenLabs preview API
- Static WPM model (default)
Output → `TIMED_SCRIPT.md`

### 6. Narrator Voice Rendering (optional)
Uses ElevenLabs to synthesize each VO line
Respects narrator profile (e.g., energy, accent, pacing)
Output → `final_voiceover.mp3`

### 7. Cinematic Video Generation (optional)
Uses Sora or Replicate’s video API
Inputs from `STORYBOARD.md`
Output → `final_video.mp4`

### 8. Assemble Output
Stored in `/output/final/`:
- `final_video.mp4`
- `final_voiceover.mp3`
- `SCRIPT.md`
- `STORYBOARD.md`
- `TIMED_SCRIPT.md`
- `transcript.txt`
- `render_notes.md`

### 9. Deploy to S3
`s3_deployer.py` uploads all assets to the defined bucket
A CloudFront layer or TTL rule can limit access after 1,000 requests
Enables public viewing without abuse risk

---

### 🔐 External Dependencies
- Amazon Bedrock (Nova or Claude) – for scene/VO generation
- ElevenLabs – for narrator voice synthesis
- Sora (OpenAI) or Replicate – for cinematic visuals

### 🗜‍🏰 Use Cases
- Developer onboarding videos
- DevSecOps training (e.g., IAM-POSSIBLE)
- DevRel content
- Story-driven walkthroughs of APIs
- Satirical tech education (e.g., TCP/IP noir detective)

### 🛠 Planned Features
- Web UI for creating new projects visually
- Prebuilt narrator voice profiles
- LangChain or Strands backend for more complex flows
- Version-controlled runs per project

### ✅ Summary
With prompt2production, a YAML input becomes an entire cinematic training artifact—voiced, visualized, and packaged for delivery. Each module is swappable, making it ideal for future expansion.

Build once. Reuse forever. Tell better tech stories.

