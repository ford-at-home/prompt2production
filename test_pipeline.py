#!/usr/bin/env python3
"""Simple test script to verify the pipeline works."""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from core.chains.scene_builder import generate_script
        print("✓ scene_builder imported")
    except Exception as e:
        print(f"✗ scene_builder import failed: {e}")
        return False
    
    try:
        from core.chains.storyboard_gen import generate_storyboard
        print("✓ storyboard_gen imported")
    except Exception as e:
        print(f"✗ storyboard_gen import failed: {e}")
        return False
    
    try:
        from core.chains.timing_chain import estimate_timing
        print("✓ timing_chain imported")
    except Exception as e:
        print(f"✗ timing_chain import failed: {e}")
        return False
    
    try:
        from core.chains.narrator_voice_gen import build_voiceover
        print("✓ narrator_voice_gen imported")
    except Exception as e:
        print(f"✗ narrator_voice_gen import failed: {e}")
        return False
    
    try:
        from core.chains.video_prompt_gen import generate_video_prompts
        print("✓ video_prompt_gen imported")
    except Exception as e:
        print(f"✗ video_prompt_gen import failed: {e}")
        return False
    
    try:
        from core.services.video_composer import compose_video
        print("✓ video_composer imported")
    except Exception as e:
        print(f"✗ video_composer import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without external APIs."""
    print("\nTesting basic functionality...")
    
    try:
        from core.chains.scene_builder import generate_script
        
        config = {
            "num_scenes": 3,
            "topic": "test topic",
            "tone": "neutral"
        }
        
        script = generate_script(config)
        print(f"Generated script: {script}")
    except Exception as e:
        print(f"✗ basic functionality test failed: {e}")
        return False
    
    return True 