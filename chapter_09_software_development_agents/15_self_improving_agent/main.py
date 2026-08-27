import sys
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from engine import SelfImprovingEngine

load_dotenv(find_dotenv())

if __name__ == "__main__":
    # Telemetría operativa simulada
    telemetry_logs = [
        {"session_id": "s101", "task": "async_fetch", "error": "SyntaxError: 'await' outside async function", "attempts": 3, "resolved": False},
        {"session_id": "s102", "task": "async_stream", "error": "SyntaxError: 'await' outside async function", "attempts": 3, "resolved": False},
        {"session_id": "s103", "task": "sql_query", "error": "TableNotFound", "attempts": 1, "resolved": True},
        {"session_id": "s104", "task": "async_download", "error": "SyntaxError: 'await' outside async function", "attempts": 3, "resolved": False},
        {"session_id": "s105", "task": "test_compliance", "error": "FalsePositive on MockData", "attempts": 2, "resolved": False}
    ]

    engine = SelfImprovingEngine()
    print("Initiating Self-Improvement Analysis & Feedback Loop...")
    planner_result = engine.analyze_feedback_and_plan(telemetry_logs)

    print(f"\nRequires HITL Review: {planner_result.requires_human_review}")
    print("Generated Improvement Hypotheses:\n" + "="*80)

    for h in planner_result.hypotheses:
        print(f"Signal:     {h.source_signal}")
        print(f"Type:       {h.adaptation_type.value}")
        print(f"Proposal:   {h.proposed_change}")
        print(f"Confidence: {h.confidence} | Evidence Count: {h.evidence_count}")
        
        # Simulación de compuerta HITL
        engine.apply_adaptation(h, hitl_approved=True)
        print("-" * 80)