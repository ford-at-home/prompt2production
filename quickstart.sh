#!/bin/bash
# Quick start script for prompt2production

echo "🎬 Welcome to prompt2production!"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Note: Add your API keys to .env for real video generation"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Try these examples:"
echo ""
echo "  python -m cli.build_project \"How does Bitcoin work? Explain it like a Wild West gold rush\""
echo ""
echo "  python -m cli.build_project \"What is machine learning? Use a cooking recipe metaphor\""
echo ""
echo "  python -m cli.build_project \"Explain cloud computing like it's a hotel service\""
echo ""
echo "💡 Your videos will appear in the output/ directory"
echo ""