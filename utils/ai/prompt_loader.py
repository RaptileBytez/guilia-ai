import os
from typing import Optional
from utils.logger import Logger

log = Logger("PromptLoader")

class PromptLoader:
    """Handles the retrieval and templating of AI prompt files from disk.
    
    Now supports a unified, path-based retrieval system that accounts for 
    model-specific optimizations and hierarchical task structures.
    """

    def __init__(self, base_path="prompts", default_model_tag=None):
        self.base_path = base_path
        self.default_model_tag = default_model_tag
        if not os.path.exists(base_path):
            log.warning(f"Base path '{base_path}' does not exist.")

    def get_prompt(self, relative_path: str, model_tag: Optional[str] = None, **kwargs) -> str:
        """Loads and renders a prompt from the hierarchical structure.
        
        Args:
            relative_path (str): Path relative to base_path (e.g., 'core/giulia_assistant').
            model_tag (str): Optional suffix for model-specific files (e.g., 'gpt4').
            **kwargs: Variables to inject into the template.
        """
        tag = model_tag or self.default_model_tag
        full_path = os.path.join(self.base_path, relative_path)
        
        # 1. Check for model-specific version (e.g., path/to/file_gpt4.txt)
        if tag:
            specific_file = f"{full_path}_{tag}.txt"
            if os.path.exists(specific_file):
                log.debug(f"Loading model-specific prompt: {specific_file}")
                return self._read_and_format(specific_file, **kwargs)

        # 2. Fallback to default version (e.g., path/to/file.txt)
        default_file = f"{full_path}.txt"
        if os.path.exists(default_file):
            return self._read_and_format(default_file, **kwargs)
        
        log.error(f"Prompt file not found: {default_file}")
        raise FileNotFoundError(f"Could not find prompt at {full_path}")

    def _read_and_format(self, path: str, **kwargs) -> str:
        """Helper to read file and safely inject variables."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                template = f.read()
            
            rendered = template.format(**kwargs)
            log.info(f"Successfully rendered prompt: {path}")
            return rendered
        except KeyError as e:
            log.error(f"Missing variable {e} in prompt: {path}")
            return template  # Return raw template as safety fallback
        except Exception as e:
            log.error(f"Error reading prompt {path}: {e}")
            return ""