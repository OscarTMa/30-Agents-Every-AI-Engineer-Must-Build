import sys
from pathlib import Path

# Asegurar resolución de importaciones locales
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from collective_agent import CollectiveIntelligenceSystem

load_dotenv(find_dotenv())

def run_main():
    system = CollectiveIntelligenceSystem()

    assignment_task = (
        "Design a grading rubric for an introductory Python assignment: "
        "'Implement a function `merge_sorted_lists(list1, list2)` that returns a new sorted list containing "
        "all elements from both input lists in non-decreasing order without using Python's built-in `sort()` or `sorted()`.'"
    )

    print("=== Collective Intelligence Agent Initialized ===")
    print(f"Problem: {assignment_task}\n")
    print("Executing Multi-Agent Proposal, Cross-Critique, and Consensus Deliberation...")

    result = system.design_rubric(assignment_task)

    print("\n" + "="*80)
    print("COLLECTIVE CONSENSUS RESULT")
    print("="*80)
    print(f"Rounds Executed:     {result.rounds_executed}")
    print(f"Consensus Score:     {result.consensus_score} / 10.0")
    print(f"Convergence State:   {'CONVERGED' if result.is_converged else 'INCOMPLETE'}")

    print("\n--- SYNTHESIZED HYBRID RUBRIC ---")
    print(result.final_rubric)

if __name__ == "__main__":
    run_main()