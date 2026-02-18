from google import genai
from google.genai import types
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from .model_interface import AIModelInterface
from utils.logger import Logger

log = Logger("ModelProvider")

class GeminiProvider(AIModelInterface):
    """
    Gemini 3 Flash Preview implementation. 
    This provider interacts with Google's Gemini API to generate responses based on system instructions and message history.
    It includes robust error handling and logging to ensure smooth operation and easier debugging.
    """
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
    
    def get_type(self) -> str:
        return "gemini"

class GPTProvider(AIModelInterface):
    """GPT-4o-mini implementation.
    This provider uses OpenAI's GPT-4o-mini model to generate responses. It constructs the message list according to OpenAI's API requirements and includes error handling to manage potential issues during API calls.
    """
    def __init__(self, model_name="gpt-4o-mini"):
        self.model_name = model_name

        try:
            self.client = OpenAI()
            log.info(f"GPT4oMiniProvider initialized with {self.model_name}")
        except Exception as e:
            log.error(f"Failed to initialize OpenAI client in GPT4oMiniProvider: {e}")
            raise

    def generate(self, system_instruction: str, messages: list) -> str:
        """Generates a response using the OpenAI API (GPT-4o-mini)."""
        try:
            # 1. Konstruiere die finale Nachrichtenliste
            # OpenAI erwartet den System-Prompt als erste Nachricht
            full_messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": system_instruction}]
            
            for msg in messages:
                full_messages.append({
                    "role": msg["role"], 
                    "content": msg["content"]
                })

            # 3. API-Call
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=full_messages,
                temperature=0.7, # Etwas kreativer für Giulia
                max_tokens=150   # Genug Platz für ihre Antworten
            )

            content = response.choices[0].message.content
            log.info(f"Successfully generated response from {self.model_name}")
            return str(content) if content is not None else ""

        except Exception as e:
            log.error(f"Error during GPT-4o-mini generation: {e}")
            return "I am currently suffering from a Network Issue, Boss."
    
    def get_type(self) -> str:
        return "gpt4o-mini"

class MockProvider(AIModelInterface):
    """Fake implementation for testing and saving costs."""
    def __init__(self, model_name="mock-model"):
        self.model_name = model_name
        log.info("MockProvider initialized. No real API calls will be made.")

    def generate(self, system_instruction: str, messages: list) -> str:
        log.debug("MockProvider: Intercepted request.")
        return "Boss, this is a simulated response. The interface works perfectly!"
    
    def get_type(self) -> str:
        return "mock"