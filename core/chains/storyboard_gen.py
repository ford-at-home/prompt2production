"""Storyboard generation chain."""

from typing import List

from core.services.bedrock_nova import run_prompt


def generate_storyboard(script: List[str]) -> List[str]:
    """Generate visual prompts for each line using Bedrock/Nova."""

    prompts = []
    for line in script:
        prompt = f"Create a vivid shot description for: {line}"
        prompts.append(run_prompt(prompt))

    return prompts

