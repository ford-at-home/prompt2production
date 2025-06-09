"""Scene builder chain.

This module would normally call an LLM like Amazon Bedrock to expand the
project configuration into a full script. To keep the repository lightweight,
`generate_script` simply creates placeholder lines so the rest of the pipeline
can be demonstrated without external services.
"""

from typing import List, Dict
from pathlib import Path

from jinja2 import Template

from core.services.bedrock_nova import run_prompt


def generate_script(config: Dict) -> List[str]:
    """Return a dummy script for the requested scene count."""

    scene_count = int(config.get("scene_count", 3))

    template_path = Path(__file__).resolve().parent.parent / "templates" / "vo_prompt.jinja"
    template = Template(template_path.read_text())

    context = {
        "technical_topic": config.get("technical_topic", "demo"),
        "metaphor_world": config.get("metaphor_world", "demo"),
        "narrator_style": config.get("narrator_style", "plain"),
        "tone": config.get("tone", "neutral"),
        "scene_count": scene_count,
    }

    script = []
    for i in range(scene_count):
        context["index"] = i + 1
        prompt = template.render(**context)
        script.append(run_prompt(prompt))

    return script
