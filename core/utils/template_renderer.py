"""Template rendering utility with optional Jinja2 support."""

from pathlib import Path
import re

try:  # pragma: no cover - optional dependency
    from jinja2 import Template
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    Template = None


def render_template(path: Path, context: dict) -> str:
    """Render the template with the given context.

    If Jinja2 is available, it is used. Otherwise a minimal ``{{ var }}``
    replacement is performed so the pipeline can run without extra
    dependencies.
    """
    text = path.read_text()
    if Template is not None:
        return Template(text).render(**context)

    pattern = re.compile(r"{{\s*(\w+)\s*}}")
    sanitized = pattern.sub(lambda m: f"{{{m.group(1)}}}", text)
    return sanitized.format(**context)
