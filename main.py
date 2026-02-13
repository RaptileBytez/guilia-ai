from chatbot import Chatbot
from utils.logger import Logger
import os

log = Logger("Guilia-Core")
log.info("Starting Giulia...")

def main():
    # Clear the terminal for a clean start (optional)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("--- 🍷 Giulia is online ---")
    print("(Type 'exit' or 'quit' to end the session)\n")

    # Initialize the bot (HistoryManager handles the JSON loading inside __init__)
    bot = Chatbot(session_id="boss_session_01")

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
        reply = bot.get_response(user_input)
        
        print(f"🍷 Giulia: {reply}\n")

if __name__ == "__main__":
    main()
