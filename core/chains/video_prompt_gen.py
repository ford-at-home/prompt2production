"""Video prompt generation chain."""

import json
from pathlib import Path
from typing import List, Dict, Any
import random

from core.utils.prompt_cleaner import clean_prompt


class VideoPromptGenerator:
    """Generates video prompts for each scene."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get("output_dir", "output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple, concrete video prompts that work well
        self.concrete_prompts = [
            "A person typing on a computer keyboard, close-up shot",
            "A hand drawing diagrams on a whiteboard with markers",
            "A smartphone screen showing an app interface",
            "A person pointing at charts and graphs on a screen",
            "A hand writing notes in a notebook with a pen",
            "A computer monitor displaying code or text",
            "A person using a tablet to navigate through menus",
            "A hand clicking buttons on a touchscreen device",
            "A person reading from a document or book",
            "A hand gesturing to explain a concept",
            "A person sitting at a desk working on a laptop",
            "A hand scrolling through content on a mobile device",
            "A person presenting slides on a projector screen",
            "A hand highlighting text in a document",
            "A person taking notes with a digital stylus"
        ]
        
    def generate_prompts(self, script_lines: List[str], storyboard: List[str]) -> List[Dict[str, Any]]:
        """Generate video prompts for each scene."""
        print("🎬 Generating video prompts...")
        
        video_prompts = []
        
        for i, (script_line, storyboard_line) in enumerate(zip(script_lines, storyboard)):
            # Get context from previous scenes for narrative flow
            context = self._get_context(script_lines, i)
            
            # Create a simple, concrete prompt based on the script line
            prompt = self._create_concrete_prompt(script_line, storyboard_line, context, i)
            
            # Clean and optimize the prompt
            cleaned_prompt = clean_prompt(prompt)
            
            video_prompt_data = {
                "scene": i + 1,
                "script_line": script_line,
                "storyboard_line": storyboard_line,
                "prompt": cleaned_prompt,
                "context": context
            }
            
            video_prompts.append(video_prompt_data)
            print(f"  Scene {i+1}: {cleaned_prompt[:60]}...")
        
        # Save video prompts
        self._save_prompts(video_prompts)
        
        return video_prompts
    
    def _get_context(self, script_lines: List[str], current_index: int) -> str:
        """Get context from previous scenes for narrative flow."""
        if current_index == 0:
            return "Introduction scene"
        
        # Get the previous 2-3 lines for context
        start_idx = max(0, current_index - 2)
        context_lines = script_lines[start_idx:current_index]
        return " ".join(context_lines)
    
    def _create_concrete_prompt(self, script_line: str, storyboard_line: str, context: str, scene_index: int) -> str:
        """Create a simple, concrete video prompt."""
        # Cycle through concrete prompts for variety
        base_prompt = self.concrete_prompts[scene_index % len(self.concrete_prompts)]
        
        # Add context from the script line to make it relevant
        if "computer" in script_line.lower() or "digital" in script_line.lower():
            return f"A person working on a computer, {script_line.lower()}"
        elif "security" in script_line.lower() or "access" in script_line.lower():
            return f"A hand typing on a keyboard, {script_line.lower()}"
        elif "identity" in script_line.lower() or "authentication" in script_line.lower():
            return f"A smartphone showing a login screen, {script_line.lower()}"
        elif "management" in script_line.lower() or "control" in script_line.lower():
            return f"A person pointing at a control panel, {script_line.lower()}"
        else:
            return f"{base_prompt}, {script_line.lower()}"
    
    def _save_prompts(self, video_prompts: List[Dict[str, Any]]) -> None:
        """Save video prompts to JSON file."""
        prompts_file = self.output_dir / "video_prompts.json"
        
        with open(prompts_file, 'w') as f:
            json.dump(video_prompts, f, indent=2)
        
        # Also save as markdown for easy reading
        md_file = self.output_dir / "VIDEO_PROMPTS.md"
        md_content = ["# Video Prompts\n"]
        
        for prompt_data in video_prompts:
            md_content.append(f"## Scene {prompt_data['scene']}")
            md_content.append(f"**Script:** {prompt_data['script_line']}")
            md_content.append(f"**Prompt:** {prompt_data['prompt']}")
            md_content.append(f"**Context:** {prompt_data['context']}")
            md_content.append("")
        
        md_file.write_text("\n".join(md_content))


def generate_video_prompts(script_lines: List[str], storyboard: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Main function to generate video prompts."""
    generator = VideoPromptGenerator(config)
    return generator.generate_prompts(script_lines, storyboard) 