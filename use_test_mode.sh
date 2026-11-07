#!/bin/bash
# Switch to test mode - fast models for development

echo "🚀 Switching to TEST MODE (fast/cheap models)..."

# Backup current config
if [ -f "config.yaml" ]; then
    cp config.yaml config.yaml.backup
fi

# Use test config
cp config.test.yaml config.yaml

echo "✅ TEST MODE activated!"
echo ""
echo "Current settings:"
echo "  - Video Model: LTX-Video (30-60 seconds per segment)"
echo "  - Duration: 10 seconds (2 segments)"
echo "  - Music: Disabled"
echo "  - Output: output_test/"
echo ""
echo "Usage: python create_video.py \"your topic\""
echo ""
echo "To switch back to production: ./use_production_mode.sh"