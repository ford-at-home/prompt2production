"""Storyboard generation chain."""

from typing import List, Dict
from pathlib import Path

from core.utils.template_renderer import render_template

from core.services.bedrock_nova import run_prompt


def generate_storyboard(script: List[str], config: Dict) -> List[str]:
    """Generate visual prompts for each line using Bedrock/Nova."""

    template_path = Path(__file__).resolve().parent.parent / "templates" / "visual_prompt.jinja"

    prompts = []
    ctx = {
        "metaphor_world": config.get("metaphor_world", "demo"),
        "tone": config.get("tone", "neutral"),
    }
    for idx, line in enumerate(script, start=1):
        ctx.update({"index": idx, "script_line": line})
        prompt = render_template(template_path, ctx)
        prompts.append(run_prompt(prompt))

    return prompts
