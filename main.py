import sys
from utils.ai import GeminiProvider, MockProvider, GPTProvider
from chatbot import GuiliaChatbot
from utils.db.factory import DBFactory
from utils.logger import Logger
import argparse
import os

log = Logger("Guilia-Core")
log.info("Starting Giulia...")

def test_db_connection() -> bool:
    try:
        db = DBFactory.get_provider(env="BLD", system_type="AGILE_E6")
        db.execute_query("SELECT 1 FROM DUAL")  # Ein einfacher Test-Query, um die Verbindung zu prüfen
        log.info("Database connection test successful.")
        return True

    except Exception as e:
        log.error(f"Database connection test failed: {e}")
        return False

def main():
    # Clear the terminal for a clean start (optional)
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description="Giulia AI - Executive Assistant")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="gemini", 
        choices=["gemini", "openai", "mock"],
        help="Wähle das KI-Modell (Standard: gemini)"
    )

    parser.add_argument(
        "--session",
        type=str,
        default="boss_session_01",
        help="Specify a session ID for conversation history."
    )

    args = parser.parse_args()
    if args.model == "mock":
        provider = MockProvider()
        log.info("Giulia is running in MOCK mode. No real API calls will be made.")
    elif args.model == "openai":
        provider = GPTProvider(model_name="gpt-4o-mini")
        log.info("Giulia is using OpenAI's GPT-4o-mini model.")
    else:
        provider = GeminiProvider(model_name="gemini-3-flash-preview")
        log.info("Giulia is using Google's Gemini 3 Flash Preview model.")
    
    guilia = GuiliaChatbot(session_id=args.session, ai_model=provider)

    
    print("--- 🍷 Giulia is online ---")
    print("(Type 'exit' or 'quit' to end the session)\n")

    while True:
        # 1. Get user input from terminal
        user_input = input("👤 You: ").strip()

        # 2. Check for exit command
        if user_input.lower() in ["exit", "quit"]:
            print("\nGiulia: Leaving so soon? I'll be waiting for your return, boss.")
            break

        if not user_input:
            continue

        # 3. Get and print response
        # The history saving is handled internally in bot.get_response()
        print("ℹ️  Giulia is thinking...")
        reply = guilia.get_response(user_input)
        
        print(f"🍷 Giulia: {reply}\n")

if __name__ == "__main__":

    if test_db_connection():
        main()
    else:
        log.error("Giulia cannot start without a database connection. Please check your configuration and try again.")
        sys.exit(1)
