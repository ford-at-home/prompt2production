# prompt2production

Create beautiful 45-second explainer videos with AI. Just tell it what to explain.

## 🚀 Quick Start

```bash
# Setup (one time)
git clone https://github.com/yourusername/prompt2production.git
cd prompt2production

# Create a video (handles setup automatically)
make video
# Then type your topic when prompted!
```

**That's it!** In ~2 minutes you'll have a professional explainer video with:
- 🎙️ Smooth 45-second narration explaining the topic clearly
- 🎬 9 perfectly-timed 5-second video scenes
- 🔊 Professional AI voice narration
- 🎵 Optional background music that matches your topic
- ✨ Everything synchronized and ready to share

## 🎯 How It Works

1. **You provide**: "how docker technology works"
2. **AI writes**: A clear, flowing 45-second explanation
3. **Smart chunking**: Breaks narration into 9 natural segments (~5 seconds each)
4. **Visual generation**: Creates a video scene for each segment
5. **Perfect sync**: Combines everything into one smooth video

## 📺 Example Videos You Can Make

```bash
python create_video.py "how machine learning works"
python create_video.py "what is cryptocurrency"
python create_video.py "how the internet works"
python create_video.py "what is cloud computing"
python create_video.py "how vaccines work"
```

## 🎨 Customization Options

```bash
# Change video length (default: 45 seconds)
python create_video.py "how wifi works" --duration 30

# Change segment length (default: 5 seconds)  
python create_video.py "how wifi works" --segment 3

# Change voice style
python create_video.py "how wifi works" --voice "british-female"

# Add a metaphor for better visuals
python create_video.py "how wifi works" --metaphor "radio station"

# Add background music
python create_video.py "how the brain works" --music
```

## 📋 Output Structure

Your video will be broken down like this:

```
[0:00-0:05] "Docker is a technology that packages applications..."
[0:05-0:10] "Think of it like shipping containers for software..."
[0:10-0:15] "Each container includes everything the app needs..."
[0:15-0:20] "This makes applications portable across systems..."
[0:20-0:25] "Developers can build once and run anywhere..."
[0:25-0:30] "Docker uses layers to make containers efficient..."
[0:30-0:35] "Multiple containers can share the same base..."
[0:35-0:40] "This revolutionized how we deploy software..."
[0:40-0:45] "Making cloud computing more accessible to everyone."
```

## 🔧 Installation

### Requirements
- Python 3.8+
- FFmpeg (for video assembly)
- API keys for AI services (optional - works in demo mode without them)

### API Setup (Optional)

For production-quality videos, you'll need:

1. **API Keys** - Add to `.env` file:
```bash
cp env.example .env
# Edit .env with your keys:
# - ELEVENLABS_API_KEY (for voices)
# - REPLICATE_API_TOKEN (for video)
```

2. **AWS Credentials** - Add to `~/.aws/credentials`:
```ini
[personal]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

## 🏗️ Pipeline Architecture

```
Input: "how docker works"
    ↓
1. Script Generation (45 seconds)
    ↓
2. Smart Segmentation (9 chunks)
    ↓
3. Visual Prompt Generation
    ↓
4. Parallel Video Generation (9 scenes)
    ↓
5. Voice Synthesis (with timing)
    ↓
6. Video Assembly & Sync
    ↓
Output: final_video.mp4
```

## 🎬 Advanced Features

### Custom Timing
```python
# config.yaml
video:
  total_duration: 45  # Total video length in seconds
  segment_duration: 5  # Each scene length in seconds
  segments: 9         # Number of scenes
```

### Quality Settings
```python
# config.yaml
quality:
  video_resolution: "1080p"
  voice_quality: "premium"
  video_style: "cinematic"
```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 2 minutes
- **[Examples](EXAMPLES.md)** - See what you can create
- **[Configuration](CONFIGURATION.md)** - Customize everything
- **[Data Flow](DATA_FLOW.md)** - How it works under the hood

## 🤝 Contributing

We'd love your help making this better:
- Improve script generation prompts
- Add new voice styles
- Enhance video scene transitions
- Create topic templates

## 📝 License

MIT - Use it for anything!

---

**Just describe what you want explained.** The AI handles the rest. 🎥✨