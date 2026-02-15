from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.ai import PromptLoader, HistoryManager, GeminiProvider
from utils.logger import Logger  # Neu: Import des Loggers
from datetime import datetime

# Load the variables from .env into the system environment
load_dotenv()

# Logger für dieses Modul initialisieren
log = Logger("Chatbot")

class GuiliaChatbot:
    def __init__(self, session_id="default_user", ai_model=None):               
        # Der Provider kapselt jetzt ALLES (Client, Modell-Name, Retries)
        self.ai_model = ai_model or GeminiProvider()
        model_tag = getattr(self.ai_model, "model_name", None)

        self.loader = PromptLoader(default_model_tag=model_tag)
        self.history_manager = HistoryManager()
        self.session_id = session_id
        now = datetime.now().strftime("%I:%M %p")
        self.system_instruction = self.loader.get_prompt(
            "core/giulia_assistant",
            current_time=now, 
            location="your private office"
        )

        self.messages = self.history_manager.load_history(self.session_id)
        log.info(f"Chatbot initialized. Session: {self.session_id}, Messages loaded: {len(self.messages)}")

    def get_response(self, message: str) -> str:
        # 1. Template Anwendung
        user_text = self.loader.get_prompt("core/boss_wrapper", message=message)
        
        # Wir nutzen hier noch types.Content, da GeminiProvider das aktuell erwartet
        user_msg = types.Content(role="user", parts=[types.Part(text=user_text)])
        self.messages.append(user_msg)
        
        log.debug(f"Prompt prepared for API (Length: {len(user_text)})")

        try:
            log.info(f"Calling AI Interface for session '{self.session_id}'...")
            start_time = datetime.now()
            
            # --- DER MAGISCHE TEIL ---
            # Kein self.client mehr, keine types.GenerateContentConfig hier
            response_text = self.ai_model.generate(
                system_instruction=self.system_instruction,
                messages=self.messages
            )
            # -------------------------
            
            duration = (datetime.now() - start_time).total_seconds()
            log.info(f"API Response received in {duration:.2f}s")

            model_msg = types.Content(role="model", parts=[types.Part(text=response_text)])
            self.messages.append(model_msg)
            
            self.history_manager.save_history(self.session_id, self.messages)

            return response_text
        
        except Exception as e:
            log.error(f"Error in Chatbot.get_response: {e}")
            return "Something went wrong in the office. Check the logs, boss?"