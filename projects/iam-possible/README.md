# MISSION: IAM-POSSIBLE  
A Cinematic Explainer of AWS IAM, Tarantino-Style

This project is the first in a series of stylized technical explainers using the `prompt-to-production` framework.  
It dramatizes AWS Identity and Access Management (IAM) through a nightclub metaphor, narrated in the voice of a cocky hacker with Samuel L. Jackson energy.

## Output Artifacts

This project will generate:

- `SCRIPT.md`: Final narration script
- `STORYBOARD.md`: Visual prompts per scene
- `TIMED_SCRIPT.md`: Estimated timing matrix
- `output/final/`: Final media artifacts (requires ElevenLabs & Sora)
  - `final_video.mp4` (Sora)
  - `final_voiceover.mp3` (ElevenLabs)
  - `transcript.txt`
  - `render_notes.md`

## Requirements

- **ElevenLabs** for voiceover synthesis
- **Sora or Replicate** for cinematic video rendering
- Optional: Midjourney, Runway for fallback visuals

## Deployment

- Assets are deployed to an S3 bucket with 1000-request limit to prevent abuse.
