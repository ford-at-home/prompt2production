"""Scene builder chain.

This module would normally call an LLM like Amazon Bedrock to expand the
project configuration into a full script. To keep the repository lightweight,
`generate_script` simply creates placeholder lines so the rest of the pipeline
can be demonstrated without external services.
"""

from typing import List, Dict


def generate_script(config: Dict) -> List[str]:
    """Return a dummy script for the requested scene count."""

    scene_count = int(config.get("scene_count", 3))
    project_name = config.get("project_name", "demo")

    script = [
        f"Scene {i + 1}: Placeholder narration for {project_name}."
        for i in range(scene_count)
    ]

    return script

