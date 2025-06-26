"""Generate visual prompts for each script segment."""

from typing import List, Dict
from pathlib import Path

from core.utils.template_renderer import render_template
from core.services.bedrock_nova import run_prompt
from core.utils.config import config as global_config


def generate_segment_visuals(topic: str, segments: List[Dict], project_config: Dict) -> List[Dict]:
    """Generate visual descriptions for each script segment.
    
    Creates prompts that:
    1. Illustrate the concept being explained in that segment
    2. Maintain visual continuity across segments
    3. Are appropriate for the topic and tone
    """
    # Determine visual style
    metaphor = project_config.get('metaphor_world')
    tone = project_config.get('tone', global_config.get('pipeline.defaults.tone', 'educational'))
    
    # Generate overall visual theme first
    theme_prompt = f"""Define a consistent visual style for a video explaining "{topic}".

The video will have {len(segments)} scenes, each {segments[0]['duration']} seconds long.
{"Use the metaphor of " + metaphor + " throughout." if metaphor else "Use clear, literal visuals."}
Tone: {tone}

Describe:
1. Overall visual style (realistic, animated, abstract, etc.)
2. Color palette
3. Key visual elements to repeat across scenes
4. How to show progression/continuity

Keep it brief and actionable."""

    visual_theme = run_prompt(theme_prompt)
    
    # Generate visual for each segment
    visual_segments = []
    
    for i, segment in enumerate(segments):
        # Create context from previous and next segments
        context = {
            'segment_text': segment['text'],
            'segment_number': segment['index'],
            'total_segments': len(segments),
            'visual_theme': visual_theme,
            'previous_text': segments[i-1]['text'] if i > 0 else None,
            'next_text': segments[i+1]['text'] if i < len(segments)-1 else None,
            'duration': segment['duration'],
            'topic': topic,
            'metaphor': metaphor,
            'tone': tone
        }
        
        # Generate visual prompt
        visual_prompt = generate_single_visual(context)
        
        visual_segments.append({
            **segment,  # Include all timing info
            'visual_prompt': visual_prompt,
            'visual_theme': visual_theme
        })
    
    return visual_segments


def generate_single_visual(context: Dict) -> str:
    """Generate a visual prompt for a single segment."""
    
    prompt = f"""Create a {context['duration']}-second video scene prompt.

Narration for this segment: "{context['segment_text']}"

This is scene {context['segment_number']} of {context['total_segments']}.
Overall topic: {context['topic']}
Visual theme: {context['visual_theme']}
{"Metaphor: " + context['metaphor'] if context['metaphor'] else "Style: Literal/educational"}

Requirements:
- Directly illustrate what's being said in the narration
- Maintain visual continuity with the theme
- Include motion/animation appropriate for {context['duration']} seconds
- Be specific about camera angles, movements, and key visual elements

Write a concise, specific prompt for video generation:"""

    return run_prompt(prompt)


def create_storyboard_summary(visual_segments: List[Dict]) -> str:
    """Create a summary storyboard of all segments."""
    
    storyboard = f"# Storyboard: {visual_segments[0].get('topic', 'Video')}\n\n"
    storyboard += f"Total Duration: {sum(s['duration'] for s in visual_segments)} seconds\n"
    storyboard += f"Segments: {len(visual_segments)}\n\n"
    
    for seg in visual_segments:
        time_range = f"[{seg['start_time']:02.0f}:{seg['end_time']:02.0f}]"
        storyboard += f"## Scene {seg['index']} {time_range}\n"
        storyboard += f"**Narration:** {seg['text'][:100]}...\n" if len(seg['text']) > 100 else f"**Narration:** {seg['text']}\n"
        storyboard += f"**Visuals:** {seg['visual_prompt']}\n"
        storyboard += f"**Words:** {seg['words']} | **Duration:** {seg['duration']}s\n\n"
    
    return storyboard


def optimize_visual_transitions(visual_segments: List[Dict]) -> List[Dict]:
    """Add transition hints to ensure smooth visual flow."""
    
    for i, seg in enumerate(visual_segments):
        if i > 0:
            # Add transition from previous
            seg['transition_in'] = 'smooth cut'
        
        if i < len(visual_segments) - 1:
            # Add transition to next
            seg['transition_out'] = 'smooth cut'
        
        # First and last segments get special treatment
        if i == 0:
            seg['visual_prompt'] += " Start with an establishing shot."
        elif i == len(visual_segments) - 1:
            seg['visual_prompt'] += " End with a concluding visual that summarizes the concept."
    
    return visual_segments