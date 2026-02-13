import os
import json
from pathlib import Path
from google.genai import types
from utils.logger import Logger

log = Logger("HistoryManager")

class HistoryManager:
    """Handles disk-based persistence of chat history using Pydantic serialization.

    This manager ensures that conversation state survives application restarts 
    by mapping Gemini's internal 'Content' objects to standard JSON.

    Attributes:
        storage_dir (Path): Validated path to the history storage directory.
    """
    def __init__(self, storage_dir="data/chat_history"):
        """Sets up the history storage directory.

        Args:
            storage_dir (str): Relative path for JSON storage. 
                Defaults to "data/chat_history".
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_path(self, session_id: str) -> Path:
        """Generates the file path for a given session."""
        return self.storage_dir / f"{session_id}.json"
    
    def load_history(self, session_id: str):
        """Loads and deserializes history from a JSON file.

        Args:
            session_id (str): The ID of the session to retrieve.

        Returns:
            list: A list of types.Content objects ready for the Gemini API.
        """
        path = self._get_path(session_id)
        if not path.exists():
            log.info(f"No existing history found for session: {session_id}") # Info, kein Fehler
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert raw dicts back into formal Gemini objects
                history = [types.Content(**msg) for msg in data]
                log.info(f"Successfully loaded {len(history)} messages for session: {session_id}")
                return history
        except Exception as e:
            log.error(f"Error loading history for session {session_id}: {e}")
            return []

    def save_history(self, session_id: str, history):
        """Serializes the current conversation history to disk.

        Args:
            history (list): A list of types.Content objects to save.
        """
        path = self._get_path(session_id)

        try:
            # Use model_dump() to turn objects into dictionaries
            # exclude_none=True keeps the JSON clean by removing empty fields
            serializable_history = [
                msg.model_dump(exclude_none=True) if hasattr(msg, 'model_dump') else msg 
                for msg in history
            ]

            with open(path, "w", encoding="utf-8") as f:
                json.dump(serializable_history, f, indent=4)
            
            log.debug(f"History for session {session_id} saved to {path}")
        except Exception as e:
            log.error(f"Error saving history for session {session_id}: {str(e)}")