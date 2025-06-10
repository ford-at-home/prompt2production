# Setup Guide

## Prerequisites

- Python 3.8+
- FFmpeg (for video composition)
- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/prompt2production.git
   cd prompt2production
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

5. **Install FFmpeg:**
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu:** `sudo apt install ffmpeg`
   - **Windows:** Download from https://ffmpeg.org/download.html

## API Keys Required

1. **AWS Bedrock** - For LLM text generation
2. **ElevenLabs** - For voice synthesis
3. **Replicate** - For video generation
4. **AWS S3** (optional) - For deployment

## Quick Test

```bash
make build PROJECT=quick-demo
```

## Troubleshooting

- **FFmpeg not found:** Ensure FFmpeg is installed and in your PATH
- **API errors:** Check your API keys in the `.env` file
- **Memory issues:** Reduce video quality settings in project config 