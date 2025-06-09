"""Scene builder chain.

This module would normally call an LLM like Amazon Bedrock to expand the
project configuration into a full script. To keep the repository lightweight,
`generate_script` simply creates placeholder lines so the rest of the pipeline
can be demonstrated without external services.
"""

from typing import List, Dict

from core.services.bedrock_nova import run_prompt


def generate_script(config: Dict) -> List[str]:
    """Return a dummy script for the requested scene count."""

    scene_count = int(config.get("scene_count", 3))
    base_prompt = config.get(
        "script_prompt",
        "Write narration for scene {i} of the project {project_name}.",
    )
    project_name = config.get("project_name", "demo")

    script = []
    for i in range(scene_count):
        prompt = base_prompt.format(i=i + 1, project_name=project_name)
        script.append(run_prompt(prompt))

    return script

