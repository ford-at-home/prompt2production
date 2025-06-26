# Configuration Guide

This guide explains how to configure prompt2production for your needs.

## 🎯 Quick Start

Most users won't need to change anything! The defaults create great 45-second explainer videos:

```bash
python create_video.py "how bitcoin works"
```

### What's New

- **Cutting-edge video model**: Now using Tencent's Hunyuan Video (state-of-the-art open source)
- **Background music**: Add AI-generated music with `--music` flag
- **Smart music matching**: Music style automatically matches your topic

## 📝 Command Line Options

Customize your video without editing any files:

```bash
# Change video length (default: 45 seconds)
python create_video.py "how wifi works" --duration 30

# Change segment length (default: 5 seconds)
python create_video.py "how wifi works" --segment 3

# Change voice (default: american-male)
python create_video.py "how wifi works" --voice british-female

# Add metaphor for better visuals
python create_video.py "how docker works" --metaphor "shipping containers"

# Change narration style
python create_video.py "how ai works" --style "friendly and casual"

# Add background music
python create_video.py "how space travel works" --music

# Disable music (if enabled by default)
python create_video.py "legal procedures explained" --no-music
```

## ⚙️ Main Configuration File

The `config.yaml` file contains all system settings:

### Video Structure
```yaml
pipeline:
  video:
    total_duration: 45      # Total video length in seconds
    segment_duration: 5     # Each scene length in seconds
    segments: 9            # Calculated from total/segment
```

### Timing Settings
```yaml
pipeline:
  timing:
    words_per_minute: 150   # Natural speaking pace
    buffer_percentage: 0.9  # Use 90% of time for safety
```

### API Configuration

#### For Voice (ElevenLabs)
```yaml
api:
  elevenlabs:
    api_key_env: "ELEVENLABS_API_KEY"  # From .env file
    voice_id: "21m00Tcm4TlvDq8ikWAM"   # Default voice
    model_id: "eleven_monolingual_v1"   # TTS model
```

#### For Video (Replicate)
```yaml
api:
  replicate:
    api_token_env: "REPLICATE_API_TOKEN"  # From .env file
    video_model: "tencent/hunyuan-video"  # State-of-the-art model
    # Alternatives: minimax/video-01, genmo/mochi-1-preview
```

#### For Music (MusicGen)
```yaml
api:
  music:
    enabled: true  # Generate background music by default
    model: "meta/musicgen"  # MusicGen by Meta
    model_version: "melody"  # Options: "melody", "large"
    duration: 45  # Match video duration
```

#### For Script (AWS Bedrock)
```yaml
api:
  bedrock:
    profile: "personal"  # AWS profile name
    model: "anthropic.claude-3-haiku-20240307-v1:0"
    region: "us-east-1"
```

## 🔑 API Setup

### 1. Create `.env` file
```bash
cp env.example .env
```

### 2. Add your API keys
```bash
# .env
ELEVENLABS_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_token_here
```

### 3. Set up AWS credentials
```bash
aws configure --profile personal
```

### 4. Enable production mode
```yaml
# config.yaml
development:
  use_stubs: false  # Switch from demo to real APIs
```

## 🎨 Voice Options

Popular voice styles for `--voice`:
- `american-male` (default)
- `american-female`
- `british-male` 
- `british-female`
- `morgan-freeman`
- `david-attenborough`

## 📊 Video Length Formulas

The system automatically calculates:
- **Number of segments** = total_duration ÷ segment_duration
- **Words per segment** = (segment_duration × words_per_minute ÷ 60) × buffer
- **Total words** = total_duration × words_per_minute ÷ 60

Examples:
- 45-second video = ~113 words total, ~12-13 words per 5-second segment
- 30-second video = ~75 words total, ~12-13 words per 5-second segment
- 60-second video = ~150 words total, ~12-13 words per 5-second segment

## 🎬 Quality Settings

### Development Mode (Fast)
```yaml
development:
  use_stubs: true   # Use placeholders
  stub_delay: 0     # No artificial delays
```

### Production Mode (Quality)
```yaml
development:
  use_stubs: false  # Use real AI APIs

quality:
  video_resolution: "1080p"
  video_fps: 30
  voice_quality: "premium"
```

## 📁 Output Structure

Configure where files are saved:
```yaml
pipeline:
  output:
    directory: "output"  # Base directory
    filenames:
      script: "full_script.txt"
      storyboard: "storyboard.md"
      voiceover: "narration.mp3"
      composed_video: "final_video.mp4"
```

## 🚀 Performance Tuning

### Faster Generation
```yaml
pipeline:
  video:
    segment_duration: 10  # Fewer, longer segments
    total_duration: 30    # Shorter videos
```

### Higher Quality
```yaml
pipeline:
  timing:
    words_per_minute: 140      # Slower narration
    buffer_percentage: 0.85    # Tighter timing
```

## 💡 Common Configurations

### Educational Content (Default)
```bash
python create_video.py "how photosynthesis works"
```

### Technical Explainer
```bash
python create_video.py "how kubernetes works" \
  --metaphor "orchestra conductor" \
  --style "technical but accessible"
```

### Fun Educational
```bash
python create_video.py "how the internet works" \
  --voice "playful" \
  --style "fun and energetic"
```

### Corporate Training
```bash
python create_video.py "our deployment process" \
  --voice "professional" \
  --style "clear and authoritative" \
  --duration 60
```

## 🔧 Advanced: Custom Prompts

Edit prompt templates in `core/templates/`:
- `script_prompt.jinja` - How scripts are written
- `visual_prompt.jinja` - How visuals are described
- `video_prompt.jinja` - Video generation instructions

## 📈 Monitoring

View generation statistics in output metadata:
```json
{
  "topic": "how docker technology works",
  "duration": 45,
  "segments": 9,
  "words_per_minute": 150,
  "total_words": 112,
  "generation_time": 47.3
}
```