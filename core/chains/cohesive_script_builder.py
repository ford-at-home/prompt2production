"""Generate a cohesive script that flows naturally for the entire duration."""

from typing import List, Dict, Tuple
from pathlib import Path

from core.utils.template_renderer import render_template
from core.services.bedrock_nova import run_prompt
from core.utils.config import config as global_config
from core.utils.tokenizer import count_tokens


def generate_cohesive_script(topic: str, project_config: Dict) -> Tuple[str, List[Dict]]:
    """Generate a complete, flowing script for the topic, then segment it.
    
    Returns:
        - Full script text
        - List of segments with text and timing
    """
    # Get video configuration
    total_duration = project_config.get('total_duration', 
                                       global_config.get('pipeline.video.total_duration', 45))
    segment_duration = project_config.get('segment_duration',
                                        global_config.get('pipeline.video.segment_duration', 5))
    num_segments = int(total_duration / segment_duration)
    
    # Calculate target words for the script
    wpm = global_config.get('pipeline.timing.words_per_minute', 150)
    target_words = int((total_duration / 60) * wpm)
    
    # Generate the full script first
    script_prompt = f"""Write a {total_duration}-second narration script explaining "{topic}".

Requirements:
- Exactly {target_words} words (for {wpm} words per minute pace)
- Clear, flowing explanation that builds understanding
- Natural progression from basic to deeper concepts
- Engaging and easy to understand (ELI5 level)
- No jargon unless immediately explained
- Must work as continuous narration (no scene breaks)

Write ONLY the narration text, no formatting or metadata."""

    full_script = run_prompt(script_prompt)
    
    # Now intelligently segment the script
    segments = segment_script(full_script, num_segments, segment_duration, wpm)
    
    return full_script, segments


def segment_script(script: str, num_segments: int, segment_duration: float, wpm: int) -> List[Dict]:
    """Break a script into timed segments at natural breaking points.
    
    This function tries to:
    1. Keep sentences together
    2. Break at punctuation when possible
    3. Maintain roughly equal timing per segment
    """
    # Target words per segment
    words_per_segment = int((segment_duration / 60) * wpm * 
                           global_config.get('pipeline.timing.buffer_percentage', 0.9))
    
    # Split into sentences first
    import re
    sentences = re.split(r'(?<=[.!?])\s+', script.strip())
    
    segments = []
    current_segment = []
    current_words = 0
    
    for sentence in sentences:
        sentence_words = len(sentence.split())
        
        # If adding this sentence would exceed our target, start a new segment
        if current_words + sentence_words > words_per_segment and current_segment:
            segments.append({
                'text': ' '.join(current_segment),
                'words': current_words,
                'duration': segment_duration,
                'index': len(segments) + 1
            })
            current_segment = [sentence]
            current_words = sentence_words
        else:
            current_segment.append(sentence)
            current_words += sentence_words
    
    # Add the last segment
    if current_segment:
        segments.append({
            'text': ' '.join(current_segment),
            'words': current_words,
            'duration': segment_duration,
            'index': len(segments) + 1
        })
    
    # If we have too many segments, merge the shortest ones
    while len(segments) > num_segments:
        # Find shortest adjacent pair
        min_combined_words = float('inf')
        merge_index = 0
        
        for i in range(len(segments) - 1):
            combined_words = segments[i]['words'] + segments[i + 1]['words']
            if combined_words < min_combined_words:
                min_combined_words = combined_words
                merge_index = i
        
        # Merge the segments
        segments[merge_index]['text'] += ' ' + segments[merge_index + 1]['text']
        segments[merge_index]['words'] += segments[merge_index + 1]['words']
        segments.pop(merge_index + 1)
        
        # Re-index
        for i, seg in enumerate(segments):
            seg['index'] = i + 1
    
    # If we have too few segments, split the longest ones
    while len(segments) < num_segments:
        # Find longest segment
        max_words = 0
        split_index = 0
        
        for i, seg in enumerate(segments):
            if seg['words'] > max_words:
                max_words = seg['words']
                split_index = i
        
        # Split at middle sentence
        text = segments[split_index]['text']
        sentences = re.split(r'(?<=[.!?])\s+', text)
        mid_point = len(sentences) // 2
        
        first_half = ' '.join(sentences[:mid_point])
        second_half = ' '.join(sentences[mid_point:])
        
        # Replace with two segments
        segments[split_index] = {
            'text': first_half,
            'words': len(first_half.split()),
            'duration': segment_duration,
            'index': split_index + 1
        }
        
        segments.insert(split_index + 1, {
            'text': second_half,
            'words': len(second_half.split()),
            'duration': segment_duration,
            'index': split_index + 2
        })
        
        # Re-index
        for i, seg in enumerate(segments):
            seg['index'] = i + 1
    
    # Add timing information
    start_time = 0
    for seg in segments:
        seg['start_time'] = start_time
        seg['end_time'] = start_time + segment_duration
        start_time += segment_duration
    
    return segments


def validate_script_timing(segments: List[Dict], wpm: int) -> List[Dict]:
    """Validate and adjust segment timing to ensure speakability."""
    buffer = global_config.get('pipeline.timing.buffer_percentage', 0.9)
    
    for seg in segments:
        # Calculate actual speaking time needed
        words = seg['words']
        time_needed = (words / wpm) * 60
        
        # Check if it fits in the segment duration
        if time_needed > seg['duration'] * buffer:
            seg['warning'] = f"Too many words ({words}) for {seg['duration']}s segment"
            seg['suggested_edit'] = 'shorten'
        elif time_needed < seg['duration'] * 0.7:  # Too short
            seg['warning'] = f"Too few words ({words}) for {seg['duration']}s segment"
            seg['suggested_edit'] = 'expand'
        else:
            seg['timing_status'] = 'good'
    
    return segments