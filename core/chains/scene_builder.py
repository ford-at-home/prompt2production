"""Scene builder chain.

This module would normally call an LLM like Amazon Bedrock to expand the
project configuration into a full script. To keep the repository lightweight,
`generate_script` simply creates placeholder lines so the rest of the pipeline
can be demonstrated without external services.
"""

from typing import List, Dict
from pathlib import Path

from core.utils.template_renderer import render_template
from core.services.bedrock_nova import run_prompt
from core.utils.config import config as global_config


def generate_script(config: Dict) -> List[str]:
    """Return a generated script for the requested scene count using a template and LLM."""

    scene_count = int(config.get("scene_count", global_config.get("pipeline.defaults.scene_count", 3)))

    template_dir = Path(global_config.get("templates.directory", "core/templates"))
    template_file = global_config.get("templates.files.voiceover_prompt", "vo_prompt.jinja")
    template_path = Path(__file__).resolve().parent.parent / "templates" / template_file

    context = {
        "technical_topic": config.get("technical_topic", global_config.get("pipeline.defaults.technical_topic", "demo")),
        "metaphor_world": config.get("metaphor_world", global_config.get("pipeline.defaults.metaphor_world", "demo")),
        "narrator_style": config.get("narrator_style", global_config.get("pipeline.defaults.narrator_style", "plain")),
        "tone": config.get("tone", global_config.get("pipeline.defaults.tone", "neutral")),
        "scene_count": scene_count,
    }

    script = []
    for i in range(scene_count):
        context["index"] = i + 1
        prompt = render_template(template_path, context)
        script.append(run_prompt(prompt))

    return script
