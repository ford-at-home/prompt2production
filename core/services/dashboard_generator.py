"""Generate HTML dashboard for video results."""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json

from core.utils.config import config as global_config
from core.utils.logger import setup_logger

try:
    from jinja2 import Template
    has_jinja2 = True
except ImportError:
    has_jinja2 = False


def generate_dashboard(
    project_data: Dict,
    output_dir: Path,
    generation_time: float,
    prompts_log: Optional[List[Dict]] = None
) -> Path:
    """Generate an HTML dashboard for the video project.
    
    Args:
        project_data: Dictionary containing all project information
        output_dir: Directory where the video files are stored
        generation_time: Total time taken to generate the video
        prompts_log: Optional list of prompts used in generation
        
    Returns:
        Path to the generated dashboard HTML file
    """
    logger = setup_logger(__name__)
    logger.info("Generating project dashboard...")
    
    # Load template
    template_path = Path(__file__).parent.parent / "templates" / "dashboard.html"
    
    if not template_path.exists():
        logger.error(f"Dashboard template not found at {template_path}")
        return None
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Prepare data for template
    segments_data = []
    for i, segment in enumerate(project_data.get('segments', [])):
        visual_segment = None
        if 'visual_segments' in project_data:
            visual_segment = next(
                (vs for vs in project_data['visual_segments'] if vs.get('index', i) == i),
                None
            )
        
        segments_data.append({
            'text': segment.get('text', ''),
            'start_time': int(segment.get('start_time', i * 5)),
            'end_time': int(segment.get('end_time', (i + 1) * 5)),
            'visual_description': visual_segment.get('visual_prompt', '') if visual_segment else ''
        })
    
    # Get model information
    script_model = global_config.get('api.bedrock.model', 'anthropic.claude-3-haiku')
    voice_model = global_config.get('api.elevenlabs.model_id', 'eleven_monolingual_v1')
    video_model = project_data.get('video_model', global_config.get('api.replicate.video_model', 'google/veo'))
    music_model = global_config.get('api.music.model', 'meta/musicgen') if global_config.get('api.music.enabled', False) else None
    
    # Calculate statistics
    total_words = sum(s.get('words', 0) for s in project_data.get('segments', []))
    
    # Prepare template context
    context = {
        'project_name': project_data.get('project_name', 'Video Project'),
        'topic': project_data.get('technical_topic', 'Unknown Topic'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_duration': project_data.get('total_duration', 45),
        'segment_count': len(segments_data),
        'segment_duration': project_data.get('segment_duration', 5),
        'total_words': total_words,
        'generation_time': f"{generation_time:.1f}",
        'script_model': script_model.split('/')[-1] if '/' in script_model else script_model,
        'voice_model': voice_model,
        'video_model': video_model.split('/')[-1] if '/' in video_model else video_model,
        'music_model': music_model.split('/')[-1] if music_model and '/' in music_model else music_model,
        'voice_style': project_data.get('voice_style', 'american-male'),
        'narrator_style': project_data.get('narrator_style', 'Friendly and clear'),
        'tone': project_data.get('tone', 'educational'),
        'metaphor_world': project_data.get('metaphor_world'),
        'segments': segments_data,
        'prompts': prompts_log or []
    }
    
    # Render template
    if has_jinja2:
        template = Template(template_content)
        html_content = template.render(**context)
    else:
        # Simple template replacement if Jinja2 not available
        html_content = template_content
        for key, value in context.items():
            if isinstance(value, list):
                # Skip complex replacements for lists
                continue
            html_content = html_content.replace(f'{{{{ {key} }}}}', str(value))
    
    # Save dashboard
    dashboard_path = output_dir / "dashboard.html"
    with open(dashboard_path, 'w') as f:
        f.write(html_content)
    
    logger.info(f"Dashboard generated at: {dashboard_path}")
    
    # Also save the context data as JSON for debugging
    context_path = output_dir / "dashboard_data.json"
    with open(context_path, 'w') as f:
        # Convert Path objects to strings for JSON serialization
        serializable_context = {
            k: str(v) if isinstance(v, Path) else v 
            for k, v in context.items()
        }
        json.dump(serializable_context, f, indent=2)
    
    return dashboard_path


def collect_prompts_from_logs(log_dir: Path, project_name: str) -> List[Dict]:
    """Collect all prompts used during generation from logs.
    
    Args:
        log_dir: Base logs directory
        project_name: Name of the project
        
    Returns:
        List of prompt dictionaries
    """
    prompts = []
    
    # Look for saved prompts in debug directory
    prompt_dir = Path(global_config.get('development.prompt_directory', 'debug/prompts'))
    if prompt_dir.exists():
        # Get prompts created during this session
        # Note: In production, you'd want to filter by timestamp or session ID
        for prompt_file in sorted(prompt_dir.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)[:10]:
            try:
                content = prompt_file.read_text()
                prompt_type = "Script Generation" if "script" in content.lower() else "Visual Generation"
                prompts.append({
                    'type': prompt_type,
                    'model': 'bedrock/claude',
                    'content': content[:500] + "..." if len(content) > 500 else content
                })
            except:
                pass
    
    return prompts