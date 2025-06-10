# Setup Guide

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `env.example` to `.env` and fill in your API keys.
3. Run a project build:
   ```bash
   make build PROJECT=quick-demo
   ```
