import sys
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from agent import TDGCodegenAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    requirement = """
    Create a shipping calculator function named `calculate_shipping(cart_total, weight)`.
    Rules:
    - Base shipping rate is $5.00.
    - Weight cost is $0.50 per kg.
    - If cart_total > 100, apply a 20% discount on total shipping.
    - If cart_total > 50 (and <= 100), apply a 10% discount on total shipping.
    - If weight < 0, raise a ValueError("Weight cannot be negative").
    """

    agent = TDGCodegenAgent()
    result = agent.run_tdg_loop(requirement)

    print("\n================ FINAL VERIFIED CODE ================")
    print(result["code"])
    print("\n================ TEST RUNNER OUTPUT ================")
    print(result["output"])