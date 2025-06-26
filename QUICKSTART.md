# Quick Start Guide

Get your first explainer video in under 2 minutes!

## 🚀 Installation (30 seconds)

### Option 1: Easiest - Just Make a Video!
```bash
# Clone the repository
git clone https://github.com/yourusername/prompt2production.git
cd prompt2production

# This command handles everything - setup + video creation
make video
```

### Option 2: Quickstart Script
```bash
# Clone the repository
git clone https://github.com/yourusername/prompt2production.git
cd prompt2production

# Run the quickstart script
./quickstart.sh
```

### Option 3: Manual Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/prompt2production.git
cd prompt2production

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🎬 Create Your First Video (1 minute)

```bash
python create_video.py "how wifi works"
```

That's it! Your video will be ready in `output/video_*/final_video.mp4`

## 📺 What You Get

A professional 45-second explainer video with:
- ✅ Clear narration explaining the topic
- ✅ 9 synchronized video scenes
- ✅ Smooth transitions
- ✅ Professional voice-over

## 🎯 Try These Examples

```bash
# Technology explanations
python create_video.py "how bitcoin works"
python create_video.py "what is machine learning"
python create_video.py "how cloud computing works"

# Science topics
python create_video.py "how photosynthesis works"
python create_video.py "what causes earthquakes"
python create_video.py "how vaccines work"

# Everyday things
python create_video.py "how wifi works"
python create_video.py "how search engines work"
python create_video.py "how gps navigation works"
```

## ⚡ Quick Customizations

### Shorter Video (30 seconds)
```bash
python create_video.py "how batteries work" --duration 30
```

### Different Voice
```bash
python create_video.py "how solar panels work" --voice british-female
```

### Add Visual Metaphor
```bash
python create_video.py "how docker works" --metaphor "shipping containers"
```

### Combine Options
```bash
python create_video.py "how the internet works" \
  --duration 60 \
  --voice morgan-freeman \
  --metaphor "highway system"
```

## 📁 Output Files

After generation, check `output/video_[timestamp]/`:
- `final_video.mp4` - Your complete video
- `full_script.txt` - The narration text
- `storyboard.md` - Visual descriptions
- `segment_breakdown.txt` - Timing information

## 🔑 Using Real AI (Optional)

By default, the app runs in demo mode. To generate real videos:

1. **Get API Keys:**
   - ElevenLabs (voice): https://elevenlabs.io/
   - Replicate (video): https://replicate.com/

2. **Add to `.env`:**
   ```bash
   cp env.example .env
   # Edit .env and add your keys
   ```

3. **Add AWS Credentials:**
   Create/edit `~/.aws/credentials`:
   ```ini
   [personal]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

4. **Enable Production Mode:**
   Edit `config.yaml`:
   ```yaml
   development:
     use_stubs: false
   ```

## 💡 Tips

1. **Keep topics focused** - "how wifi works" is better than "the history of wireless communication"

2. **Use metaphors for complex topics** - They create better visuals

3. **Default settings work great** - 45 seconds with 5-second segments is optimal

4. **Check the script first** - Read `full_script.txt` to ensure the explanation is what you want

## 🚨 Troubleshooting

**"Command not found"**
- Make sure you're in the project directory
- Try `python3` instead of `python`

**"Module not found"**
- Run `pip install -r requirements.txt` again
- Consider using a virtual environment

**Video looks wrong**
- Check `storyboard.md` to see what visuals were planned
- Try adding a `--metaphor` to guide the visuals

## 🎉 Next Steps

1. Generate a few videos to see how it works
2. Experiment with different topics and options
3. Set up API keys for production-quality output
4. Read [CONFIGURATION.md](CONFIGURATION.md) for advanced options

---

**Need help?** The default settings create great videos. Just describe what you want to explain!