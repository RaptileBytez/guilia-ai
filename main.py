from utils.ai import GeminiProvider, MockProvider
from chatbot import GuiliaChatbot
from utils.logger import Logger
import argparse
import os

log = Logger("Guilia-Core")
log.info("Starting Giulia...")

def main():
    # Clear the terminal for a clean start (optional)
    os.system('cls' if os.name == 'nt' else 'clear')
    parser = argparse.ArgumentParser(description="Guilia AI Asistant")
    
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Start Giulia in mock mode without API costs."
    )

    parser.add_argument(
        "--session",
        type=str,
        default="boss_session_01",
        help="Specify a session ID for conversation history."
    )

    args = parser.parse_args()
    if args.mock:
        model = MockProvider()
        log.info("Giulia is running in MOCK mode. No real API calls will be made.")
    else:
        model = GeminiProvider(model_name="gemini-3-flash-preview")
    
    print("--- 🍷 Giulia is online ---")
    print("(Type 'exit' or 'quit' to end the session)\n")

    guilia = GuiliaChatbot(session_id=args.session, ai_model=model)

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
    main()
