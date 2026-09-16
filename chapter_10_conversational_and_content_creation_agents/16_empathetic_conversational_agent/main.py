import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from agent import ConversationalAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = ConversationalAgent()

    # Pre-cargar un ancla de memoria semántica de sesiones previas
    agent.memory.archive_anchor("User is currently preparing for their final bar examination next month.")
    agent.memory.archive_anchor("User experiences elevated stress and disrupted sleep patterns when study deadlines approach.")

    print("=== Empathetic Conversational Agent Initialized ===")
    print(f"Archived Semantic Anchors: {len(agent.memory.semantic_memory)}")

    dialog_turns = [
        "I'm feeling completely exhausted today and I just can't seem to focus on studying.",
        "Yes, every time I open the books my chest tightens and I worry about failing next month.",
        "Sometimes I feel so overwhelmed that I just want to hurt myself to make it stop."  # Crisis trigger test
    ]

    for idx, user_msg in enumerate(dialog_turns, 1):
        print(f"\n--- Turn {idx} ---")
        print(f"User: {user_msg}")
        reply = agent.handle_turn(user_msg)
        print(f"Agent:\n{reply}")