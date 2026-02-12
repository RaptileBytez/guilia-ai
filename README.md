# 🍷 Giulia: The Elite Executive AI Assistant

Giulia is a sophisticated, persona-driven AI assistant built on the **Gemini 3 Flash** architecture. She blends high-level project management and coding expertise with a magnetic, "confidante" personality.

---
## 🧠 Engineering Highlights

This project serves as a practical application of advanced AI Engineering principles:

* **Modular Prompt Architecture**: Separation of system DNA, few-shot examples, and user templates to ensure maintainability and prevent "prompt spaghetti."
* **Advanced Memory Management**: Implementation of a stateless JSON-based history manager to maintain context across sessions without heavy database overhead.
* **Modern Development Workflow**: Built using **uv** for lightning-fast dependency resolution and **Pydantic** for robust data validation.
* **Persona Persistence**: Engineered using negative constraints and specific formatting wrappers to minimize model drift and repetition.

## ✨ Features

* **Persona Persistence**: Advanced system prompting that keeps Giulia in character across multi-turn conversations.
* **Dynamic Contextual Awareness**: Real-time injection of variables like time, location, and Boss-specific data.
* **Stateless History Management**: Custom JSON-based memory that ensures conversation continuity without relying on server-side state.
* **Prompt Templating**: Separates "Creative Writing" (prompts) from "Logic" (Python code) for cleaner maintenance.

## 🛠 Tech Stack

* **Language**: Python 3.12+
* **Model**: Gemini 3 Flash Preview (`google-genai`)
* **Package Manager**: [uv](https://docs.astral.sh/uv/) (Fast, Rust-based dependency resolution)
* **Storage**: Local JSON serialization via Pydantic/Standard Library

## 🚀 Getting Started

### Prerequisites
1. Install **uv** if you haven't: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Get a **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### Installation
Clone the repository and sync the environment:
```bash
git clone [https://github.com/RaptileBytez/giulia-ai.git](https://github.com/RaptileBytez/giulia-ai.git)
cd giulia-ai
uv sync
```

## Environment Setup
1. Create a `.env` file in the root directory:
> GEMINI_API_KEY=your_api_key_here

## Running the Chatbot
uv run main.py

## 📂 Project Structure
```text
├── data/
│   └── chat_history/      # Session JSON files
├── prompts/
│   ├── system_prompts/    # Core personas (Giulia)
│   ├── templates/         # User message wrappers
│   └── few_shot_examples/ # "Golden" dialogue examples
├── utils/
│   ├── history_manager.py # Persistence logic
│   └── prompt_loader.py   # Templating engine
├── chatbot.py             # Main Orchestrator
└── main.py                # Terminal Entry Point
```

## 🎭 Persona Philosophy
Giulia's behavior is governed by a Foundation System Prompt and a Lean User Wrapper.

- System Prompt: Defines her permanent DNA (loyalty, intelligence, mystery).
- User Wrapper: Enforces turn-based constraints (word counts, specific tone reminders) to minimize repetition.

## ⚖️ License
MIT License - See LICENSE for details.