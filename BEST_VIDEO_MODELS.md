# 🏆 Best Video Generation Models Guide

## Currently Configured: Google Veo 3
You're using **Google Veo 3** - the absolute state-of-the-art video generation model with native audio generation capabilities.

## Top Video Models Ranking

### 🥇 Google Veo 3 (CONFIGURED)
- **Quality**: ⭐⭐⭐⭐⭐ State of the art
- **Speed**: 3-5 minutes per 5s segment
- **Resolution**: Up to 1080p
- **Special Features**: Native audio generation, hyperrealism
- **Best For**: Maximum quality with sound effects

### 🥈 Tencent HunyuanVideo
- **Quality**: ⭐⭐⭐⭐⭐ Sora-level (13B parameters)
- **Speed**: 4-6 minutes per 5s segment
- **Resolution**: 1280x720
- **Special Features**: Open-source, customizable
- **Best For**: High quality with flexibility

### 🥉 MiniMax Video-01 (Hailuo)
- **Quality**: ⭐⭐⭐⭐⭐ Exceptional realism
- **Speed**: 2.5-3.5 minutes for 6s
- **Resolution**: 720p
- **Special Features**: Prompt optimizer
- **Best For**: Realistic human motion

### 4️⃣ Kling v2.1 Pro
- **Quality**: ⭐⭐⭐⭐½ 
- **Speed**: 4-6 minutes
- **Resolution**: 1080p (highest available)
- **Special Features**: 10s videos, camera motion
- **Best For**: Longer, high-res videos

### 5️⃣ MiniMax Director
- **Quality**: ⭐⭐⭐⭐½
- **Speed**: 2.5-3.5 minutes
- **Resolution**: 720p
- **Special Features**: Cinematic camera control
- **Best For**: Professional camera movements

## Quick Model Switching

To switch models, edit `config.yaml`:

```yaml
# For open-source flexibility:
video_model: "tencent/hunyuan-video"

# For realistic motion:
video_model: "minimax/video-01"

# For highest resolution:
video_model: "kwaivgi/kling-v2.1"

# For cinematic control:
video_model: "minimax/video-01-director"
```

## Generation Time Estimates

| Model | 5-second video | 10-second video |
|-------|----------------|-----------------|
| Google Veo 3 | 3-5 minutes | 6-10 minutes |
| HunyuanVideo | 4-6 minutes | 8-12 minutes |
| MiniMax | 2.5-3.5 min | N/A (6s max) |
| Kling Pro | 4-6 minutes | 8-12 minutes |
| LTX-Video | 30-60 seconds | 1-2 minutes |

## Cost Estimates (Replicate Pricing)

- **Google Veo 3**: ~$0.50-1.00 per segment
- **HunyuanVideo**: ~$1.21 per segment (4x H100)
- **MiniMax**: ~$0.30-0.50 per segment
- **Kling Pro**: ~$0.40-0.80 per segment

## Pro Tips for Best Results

### 1. Prompt Engineering
```
# Good prompt structure:
"[Shot type] of [subject] [action] in [setting], [style/mood], [technical details]"

# Example:
"Cinematic wide shot of a dancer performing salsa moves in a vibrant dance studio, warm lighting, smooth camera movement, professional cinematography"
```

### 2. Model-Specific Tips

**Google Veo 3**:
- Include audio descriptions: "with sound of footsteps"
- Be specific about camera angles
- Use cinematic terminology

**HunyuanVideo**:
- Adjust `num_inference_steps` (25-100) for quality/speed
- Use `flow_shift` (-10 to 10) to control motion

**MiniMax**:
- Enable `prompt_optimizer` for better results
- Keep prompts under 200 characters

**Kling**:
- Specify camera motion: "zoom_in", "pan_left", etc.
- Use "pro" mode for maximum quality

### 3. Optimal Settings by Use Case

**For Presentations**: Google Veo 3 (with audio)
**For Social Media**: MiniMax (fast, good quality)
**For Film/TV**: Kling Pro or HunyuanVideo
**For Prototyping**: LTX-Video (real-time)

## Troubleshooting

### If generation fails:
1. Check your Replicate API token
2. Ensure prompt is under model's character limit
3. Try reducing video duration
4. Check model-specific requirements

### For faster generation:
- Use LTX-Video for drafts
- Reduce resolution/quality settings
- Generate shorter segments

### For better quality:
- Increase inference steps
- Use more descriptive prompts
- Generate at native resolution
- Avoid rapid motion in prompts

## Command Examples

```bash
# Standard quality video
python create_video.py "quantum computing explained" --duration 10

# Quick test with fast model (edit config first)
python create_video.py "test video" --duration 5 --segment 5

# High quality with music
python create_video.py "the beauty of mathematics" --duration 30 --music
```

Remember: The best model depends on your specific needs - quality, speed, resolution, or special features!