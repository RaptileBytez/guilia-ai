from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from utils.ai import PromptLoader, HistoryManager
from utils.logger import Logger  # Neu: Import des Loggers
from datetime import datetime

# Load the variables from .env into the system environment
load_dotenv()

# Logger für dieses Modul initialisieren
log = Logger("Chatbot")

class Chatbot:
    """Orchestrates the interaction between the Gemini 3 LLM and local persistence."""

    def __init__(self, session_id="default_user"):
        self.loader = PromptLoader()
        self.history_manager = HistoryManager()
        self.session_id = session_id

        now = datetime.now().strftime("%I:%M %p")
        
        # System Instruction laden
        self.system_instruction = self.loader.get_system_prompt(
            "giulia_assistant",
            current_time=now, 
            location="your private office"
        )

        # Historie laden
        self.messages = self.history_manager.load_history(self.session_id)
        log.info(f"Chatbot initialized. Session: {self.session_id}, Messages loaded: {len(self.messages)}")

        # Client Setup
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
            self.model = "gemini-3-flash-preview"
            log.info(f"Gemini Client connected. Using model: {self.model}")
        except Exception as e:
            log.error(f"Failed to initialize Gemini Client: {e}")
            raise

        # Safety Settings
        safety_config = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            )
        ]

    def get_response(self, message: str) -> str:
        """Processes user input and returns a persona-aligned response."""
        
        # 1. Template Anwendung
        user_text = self.loader.get_template("boss_template", message=message)
        
        user_msg = types.Content(
            role="user", 
            parts=[types.Part(text=user_text)]
        )
        self.messages.append(user_msg)
        
        log.debug(f"Prompt prepared for API (Length: {len(user_text)})")

        try:
            # 3. API Call
            log.info(f"Calling Gemini API for session '{self.session_id}'...")
            start_time = datetime.now()
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.messages,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                )
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            log.info(f"API Response received in {duration:.2f}s")

            # Model Antwort verarbeiten
            model_msg = types.Content(
                role="model",
                parts=[types.Part(text=response.text)]
            )
            self.messages.append(model_msg)
            
            # 5. Historie speichern
            self.history_manager.save_history(self.session_id, self.messages)

            return str(response.text)
        
        except errors.ServerError:
            log.warning("Gemini API Overload (ServerError).")
            return "I'm a bit overwhelmed with work right now, boss. Give me a moment to catch my breath?"
        
        except Exception as e:
            log.error(f"Unexpected Error in Chatbot.get_response: {e}")
            return "Something went wrong in the office. Check the logs, boss?"