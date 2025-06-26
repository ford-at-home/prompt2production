"""Configuration management for Prompt2Production pipeline."""

import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


class Config:
    """Centralized configuration management."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self, config_path: Optional[str] = None) -> None:
        """Load configuration from YAML file."""
        if config_path is None:
            # Look for config.yaml in project root
            root_dir = Path(__file__).parent.parent.parent
            config_path = root_dir / "config.yaml"
        
        if not Path(config_path).exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if yaml:
                self._config = yaml.safe_load(f)
            else:
                # Fallback to simple parser if PyYAML not available
                self._config = self._simple_yaml_parser(f.read())
        
        # Process environment variables
        self._process_env_vars()
    
    def _simple_yaml_parser(self, text: str) -> dict:
        """Simple YAML parser for when PyYAML is not available."""
        # This is a very basic implementation
        result = {}
        current_section = result
        indent_stack = [(0, result)]
        
        for line in text.splitlines():
            if not line.strip() or line.strip().startswith('#'):
                continue
                
            indent = len(line) - len(line.lstrip())
            key_value = line.strip()
            
            if ':' in key_value:
                key, value = key_value.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle section changes based on indentation
                while indent <= indent_stack[-1][0] and len(indent_stack) > 1:
                    indent_stack.pop()
                
                current_section = indent_stack[-1][1]
                
                if value:
                    # Simple value
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value in ('true', 'True'):
                        value = True
                    elif value in ('false', 'False'):
                        value = False
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass
                    
                    current_section[key] = value
                else:
                    # New section
                    new_section = {}
                    current_section[key] = new_section
                    indent_stack.append((indent + 2, new_section))
        
        return result
    
    def _process_env_vars(self) -> None:
        """Process environment variable references in config."""
        # Load API keys from environment
        if 'api' in self._config:
            if 'elevenlabs' in self._config['api']:
                env_var = self._config['api']['elevenlabs'].get('api_key_env')
                if env_var:
                    self._config['api']['elevenlabs']['api_key'] = os.getenv(env_var, '')
            
            if 'replicate' in self._config['api']:
                env_var = self._config['api']['replicate'].get('api_token_env')
                if env_var:
                    self._config['api']['replicate']['api_token'] = os.getenv(env_var, '')
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Examples:
            config.get('api.bedrock.model')
            config.get('pipeline.timing.words_per_minute', 120)
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_output_path(self, filename_key: str) -> Path:
        """Get full output path for a given filename key."""
        output_dir = Path(self.get('pipeline.output.directory', 'output'))
        filename = self.get(f'pipeline.output.filenames.{filename_key}', f'{filename_key}.txt')
        return output_dir / filename
    
    def merge_project_config(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge project-specific config with global config.
        
        Project config takes precedence over global config.
        """
        merged = {}
        
        # Start with defaults from global config
        defaults = self.get('pipeline.defaults', {})
        merged.update(defaults)
        
        # Override with project-specific values
        merged.update(project_config)
        
        # Add output directory if not specified
        if 'output_dir' not in merged:
            merged['output_dir'] = self.get('pipeline.output.directory', 'output')
        
        # Add API configuration
        merged['_api_config'] = self._config.get('api', {})
        
        return merged


# Global config instance
config = Config()