from google import genai
from google.genai import types
from .model_interface import AIModelInterface
from utils.logger import Logger

log = Logger("ModelProvider")

class GeminiProvider(AIModelInterface):
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model_name = model_name
        
        # Hier ziehen die HttpOptions und der Client ein
        try:
            self.client = genai.Client(
                http_options=types.HttpOptions(
                    retry_options=types.HttpRetryOptions(
                        attempts=3,
                        initial_delay=2.0,
                        max_delay=60.0
                    )
                )
            )
            log.info(f"GeminiProvider initialized with {self.model_name}")
        except Exception as e:
            log.error(f"Failed to initialize Gemini Client in Provider: {e}")
            raise

    def generate(self, system_instruction: str, messages: list) -> str:
        # Hier wandert der eigentliche API-Call hin
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return str(response.text)

class MockProvider(AIModelInterface):
    """Fake implementation for testing and saving costs."""
    def __init__(self, model_name="mock-model"):
        self.model_name = model_name
        log.info("MockProvider initialized. No real API calls will be made.")

    def generate(self, system_instruction: str, messages: list) -> str:
        log.debug("MockProvider: Intercepted request.")
        return "Boss, this is a simulated response. The interface works perfectly!"