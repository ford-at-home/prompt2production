# 🚀 Test vs Production Mode Guide

## Overview

This project now supports two distinct modes for video generation:

- **Test Mode**: Fast, cheap models for development and testing
- **Production Mode**: Premium models for final, high-quality output

## Quick Start

### Using Test Mode (Recommended for Development)

```bash
# Option 1: Use the --test flag
python create_video.py "your topic" --test

# Option 2: Switch to test mode globally
./use_test_mode.sh
python create_video.py "your topic"
```

### Using Production Mode (For Final Videos)

```bash
# Option 1: Use the --production flag
python create_video.py "your topic" --production

# Option 2: Switch to production mode globally
./use_production_mode.sh
python create_video.py "your topic"
```

## Mode Comparison

| Feature | Test Mode | Production Mode |
|---------|-----------|-----------------|
| **Video Model** | LTX-Video | Google Veo 3 |
| **Generation Time** | 30-60s per segment | 3-5 min per segment |
| **Total Time (30s video)** | ~2-3 minutes | ~30-45 minutes |
| **Video Quality** | 768x512, good | 1280x720+, exceptional |
| **Cost per Segment** | ~$0.05-0.10 | ~$0.50-1.00 |
| **Default Duration** | 10 seconds | 45 seconds |
| **Music Generation** | Disabled | Enabled |
| **Retry Logic** | No retries | 3 retries with delays |
| **Output Directory** | `output_test/` | `output/` |

## Workflow Recommendations

### 1. Development Workflow

Always use test mode during development:

```bash
# Start in test mode
./use_test_mode.sh

# Iterate quickly
python create_video.py "test topic 1"
python create_video.py "test topic 2" 
python create_video.py "test topic 3"

# Each video takes only 2-3 minutes!
```

### 2. Testing Script Quality

Test your script generation without video:

```bash
# Just generate script and voice (no video)
python create_video.py "your topic" --test --segment 0
```

### 3. Production Workflow

Once you're happy with the content:

```bash
# Switch to production
python create_video.py "your final topic" --production --duration 30

# Or for maximum quality
./use_production_mode.sh
python create_video.py "your final topic" --duration 45
```

### 4. Hybrid Workflow

Test segments first, then produce final:

```bash
# Test with 10 seconds
python create_video.py "complex topic" --test

# Review output_test/video_*/
# If good, create full version
python create_video.py "complex topic" --production --duration 60
```

## Configuration Files

### Test Configuration (`config.test.yaml`)
- Model: `lightricks/ltx-video`
- Fast generation (real-time capable)
- Lower resolution for speed
- No background music
- Shorter default duration

### Production Configuration (`config.production.yaml`)
- Model: `google/veo-3` 
- Highest quality output
- Native audio generation
- Background music enabled
- Full duration videos
- Retry logic for reliability

### Default Configuration (`config.yaml`)
- This file is overwritten when switching modes
- Always backed up to `config.yaml.backup`

## Cost Optimization

### Test Mode Costs
- ~$0.05-0.10 per segment
- 10-second video (2 segments): ~$0.20
- Perfect for iteration

### Production Mode Costs
- ~$0.50-1.00 per segment
- 30-second video (6 segments): ~$3-6
- 60-second video (12 segments): ~$6-12

### Tips to Save Money
1. Always develop in test mode
2. Keep production videos concise
3. Use retry logic to avoid re-running entire pipeline
4. Test scripts separately before generating video

## Advanced Features

### Custom Timeouts

Production mode includes automatic timeouts:
- 10 minutes per segment (configurable)
- 3 retry attempts with 30-second delays
- Automatic placeholder generation on failure

### Mode Detection

The system shows current mode on startup:
```
🚀 Using TEST MODE (fast models)
   Duration set to 10s for testing
```

or

```
🏆 Using PRODUCTION MODE (best quality)
⚠️  This will take 30-45 minutes and cost more
```

### Parallel Development

You can work on multiple videos simultaneously:
```bash
# Terminal 1: Test new ideas
python create_video.py "idea 1" --test

# Terminal 2: Produce final video
python create_video.py "final topic" --production
```

## Troubleshooting

### "Model not found" Error
- Ensure your Replicate API token is set
- Check model availability on Replicate

### Timeouts in Production
- Normal for Google Veo 3 (3-5 min/segment)
- Retry logic will handle temporary failures
- Check logs in `output/video_*/pipeline.log`

### Quality Issues
- Ensure you're using production mode for final output
- Check visual prompts in storyboard.md
- Adjust prompts for better results

## Best Practices

1. **Always start with test mode**
   - Validate your concept
   - Check script quality
   - Test visual descriptions

2. **Review before production**
   - Check `output_test/*/full_script.txt`
   - Listen to `output_test/*/final_voiceover.mp3`
   - Review `output_test/*/storyboard.md`

3. **Optimize for production**
   - Keep videos under 60 seconds
   - Use clear, descriptive prompts
   - Enable music for better engagement

4. **Monitor costs**
   - Track usage in Replicate dashboard
   - Use test mode for all development
   - Batch production runs

## Examples

### Quick Test
```bash
python create_video.py "quantum computing basics" --test
# 2-3 minutes, ~$0.20
```

### Full Production
```bash
python create_video.py "quantum computing explained" --production --duration 45
# 30-45 minutes, ~$4-5
```

### Script Only
```bash
python create_video.py "test narration" --test --no-music --segment 0
# <1 minute, ~$0.05
```

Remember: **Test mode for development, Production mode for delivery!**