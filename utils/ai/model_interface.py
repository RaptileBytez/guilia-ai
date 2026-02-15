from abc import ABC, abstractmethod
from utils.logger import Logger

log = Logger("AIInterface")

class AIModelInterface(ABC):
    """Abstract base class defining the interface for AI model interactions.

    This interface ensures that any AI model implementation (e.g., Gemini, 
    OpenAI) adheres to a consistent method signature for generating responses 
    based on user input and conversation history.

    Methods:
        get_response: Generates a response from the AI model given user input and history.
    """
    
    @abstractmethod
    def generate(self, system_instruction: str, messages: list) -> str:
        """Generates a response from the AI model.

        Args:
            system_instruction (str): The core instruction guiding the model's behavior.
            messages (list): A list of conversation turns, typically including 
                both user and model messages, formatted as required by the API.
        Returns:
            str: The generated response from the AI model.
        """
        pass