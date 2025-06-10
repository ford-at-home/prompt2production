"""Prompt cleaning and optimization utilities."""

import re
from typing import List, Dict, Any


def clean_prompt(prompt: str) -> str:
    """Clean and optimize a video prompt."""
    if not prompt:
        return prompt
    
    # Remove extra whitespace
    prompt = re.sub(r'\s+', ' ', prompt.strip())
    
    # Remove common problematic phrases
    problematic_phrases = [
        "high quality",
        "professional",
        "cinematic",
        "award winning",
        "stunning",
        "beautiful",
        "amazing",
        "incredible",
        "perfect",
        "best",
        "top quality",
        "premium",
        "4k",
        "8k",
        "ultra hd",
        "high resolution"
    ]
    
    for phrase in problematic_phrases:
        prompt = re.sub(re.escape(phrase), '', prompt, flags=re.IGNORECASE)
    
    # Remove redundant punctuation
    prompt = re.sub(r'[.!?]+', '.', prompt)
    prompt = re.sub(r'[,;]+', ',', prompt)
    
    # Clean up multiple spaces
    prompt = re.sub(r'\s+', ' ', prompt)
    
    # Ensure it ends with a period
    if not prompt.endswith('.'):
        prompt += '.'
    
    return prompt.strip()


def optimize_for_video(prompt: str) -> str:
    """Optimize prompt specifically for video generation."""
    # Keep it simple and concrete
    prompt = clean_prompt(prompt)
    
    # Add basic video-specific terms if not present
    if "camera" not in prompt.lower() and "shot" not in prompt.lower():
        prompt = prompt.replace('.', ', medium shot.')
    
    return prompt


def validate_prompt(prompt: str) -> Dict[str, Any]:
    """Validate a prompt and return analysis."""
    analysis = {
        "length": len(prompt),
        "word_count": len(prompt.split()),
        "has_technical_terms": bool(re.search(r'\b(computer|digital|system| 