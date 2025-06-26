"""Generate prompts for video rendering."""

from pathlib import Path
from typing import List, Dict

from core.utils.template_renderer import render_template
from jinja2 import Template
from core.utils.prompt_cleaner import clean_prompt
from core.utils.config import config as global_config


def generate_video_prompts(storyboard: List[str], config: Dict) -> List[str]:
    """Render a prompt for each storyboard line."""
    template_file = global_config.get("templates.files.video_prompt", "video_prompt.jinja")
    template_path = (
        Path(__file__).resolve().parent.parent / "templates" / template_file
    )

    template = Template(template_path.read_text())

    ctx = {
        "metaphor_world": config.get("metaphor_world", global_config.get("pipeline.defaults.metaphor_world", "demo")),
        "tone": config.get("tone", global_config.get("pipeline.defaults.tone", "neutral")),
    }

    prompts = []
    for index, line in enumerate(storyboard, start=1):
        ctx.update({"index": index, "storyboard_line": line})
        prompt = render_template(template_path, ctx)
        prompts.append(clean_prompt(prompt))

    return prompts
