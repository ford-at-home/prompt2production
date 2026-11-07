"""Centralized logging configuration for prompt2production."""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from core.utils.config import config as global_config


def setup_logger(name: str, project_name: Optional[str] = None) -> logging.Logger:
    """Set up a logger with consistent formatting and output locations.
    
    Args:
        name: Logger name (usually __name__)
        project_name: Optional project name for project-specific logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # Set level from config
    level = global_config.get('logging.level', 'INFO')
    logger.setLevel(getattr(logging, level))
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    # Console handler (simple format)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handlers (detailed format)
    # Central log directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Main application log
    app_log_path = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    app_file_handler = logging.FileHandler(app_log_path)
    app_file_handler.setLevel(logging.DEBUG)
    app_file_handler.setFormatter(detailed_formatter)
    logger.addHandler(app_file_handler)
    
    # Project-specific log if project name provided
    if project_name:
        project_log_dir = log_dir / "projects" / project_name
        project_log_dir.mkdir(parents=True, exist_ok=True)
        
        project_log_path = project_log_dir / "pipeline.log"
        project_file_handler = logging.FileHandler(project_log_path)
        project_file_handler.setLevel(logging.DEBUG)
        project_file_handler.setFormatter(detailed_formatter)
        logger.addHandler(project_file_handler)
    
    return logger


def log_step(logger: logging.Logger, step_num: int, step_name: str, details: Optional[str] = None):
    """Log a pipeline step with consistent formatting.
    
    Args:
        logger: Logger instance
        step_num: Step number
        step_name: Name of the step
        details: Optional additional details
    """
    emoji_map = {
        1: "📝", 2: "⏱️", 3: "🎨", 4: "📋", 5: "🎙️",
        6: "🎵", 7: "🎬", 8: "🎞️", 9: "☁️", 10: "✅"
    }
    emoji = emoji_map.get(step_num, "▶️")
    
    message = f"{emoji} Step {step_num}: {step_name}"
    if details:
        message += f" - {details}"
    
    logger.info(message)


def log_api_call(logger: logging.Logger, service: str, operation: str, 
                 params: Optional[dict] = None, stub_mode: bool = False):
    """Log API calls with consistent formatting.
    
    Args:
        logger: Logger instance
        service: Service name (e.g., "ElevenLabs", "Replicate")
        operation: Operation being performed
        params: Optional parameters
        stub_mode: Whether running in stub mode
    """
    mode = "STUB" if stub_mode else "LIVE"
    message = f"[{mode}] {service} API - {operation}"
    
    if params:
        # Filter sensitive data
        safe_params = {k: v for k, v in params.items() 
                      if k not in ['api_key', 'token', 'secret']}
        if safe_params:
            message += f" - Params: {safe_params}"
    
    logger.debug(message)


def log_timing(logger: logging.Logger, operation: str, duration: float):
    """Log operation timing.
    
    Args:
        logger: Logger instance
        operation: Operation name
        duration: Duration in seconds
    """
    logger.info(f"⏱️ {operation} completed in {duration:.2f}s")


def log_error(logger: logging.Logger, error: Exception, context: str):
    """Log errors with context.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Context where error occurred
    """
    logger.error(f"❌ Error in {context}: {type(error).__name__}: {str(error)}")
    logger.debug(f"Full traceback:", exc_info=True)