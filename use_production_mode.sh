#!/bin/bash
# Switch to production mode - best quality models

echo "🏆 Switching to PRODUCTION MODE (highest quality)..."

# Backup current config
if [ -f "config.yaml" ]; then
    cp config.yaml config.yaml.backup
fi

# Use production config
cp config.production.yaml config.yaml

echo "✅ PRODUCTION MODE activated!"
echo ""
echo "Current settings:"
echo "  - Video Model: Google Veo 3 (3-5 minutes per segment)"
echo "  - Duration: 45 seconds (9 segments)"
echo "  - Music: Enabled"
echo "  - Output: output/"
echo ""
echo "⚠️  WARNING: Production mode uses premium models that:"
echo "  - Cost more (~$0.50-1.00 per segment)"
echo "  - Take longer (30-45 minutes for full video)"
echo ""
echo "Usage: python create_video.py \"your topic\" --duration 45"
echo ""
echo "To switch to test mode: ./use_test_mode.sh"