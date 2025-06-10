"""Generate prompts for video rendering."""

from pathlib import Path
from typing import List, Dict

from core.utils.template_renderer import render_template

from core.utils.prompt_cleaner import clean_prompt


def generate_video_prompts(storyboard: List[str], config: Dict) -> List[str]:
    """Render a prompt for each storyboard line."""
    template_path = (
        Path(__file__).resolve().parent.parent / "templates" / "video_prompt.jinja"
    )

    ctx = {
        "metaphor_world": config.get("metaphor_world", "demo"),
        "tone": config.get("tone", "neutral"),
    }

    prompts = []
    for index, line in enumerate(storyboard, start=1):
        ctx.update({"index": index, "storyboard_line": line})
        prompt = render_template(template_path, ctx)
        prompts.append(clean_prompt(prompt))

    return prompts
