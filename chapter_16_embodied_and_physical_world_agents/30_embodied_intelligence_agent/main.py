import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from embodied_agent import EmbodiedIntelligenceAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = EmbodiedIntelligenceAgent()
    goal = "Move package A to shelf B without colliding with obstacles or violating workspace bounds."

    print("=== Embodied Intelligence Agent Initialized (Depth Architecture) ===")
    print(f"High-Level Operator Goal: '{goal}'\n")

    # 1. Planificación estratégica (0.1 - 1 Hz)
    print("1. DECOMPOSING TASK INTO PARAMETERIZED PHYSICAL ACTIONS:")
    plan = agent.plan_task(goal)
    for act in plan.actions:
        print(f"   Step {act.step_number}: {act.action_type:<6} -> ({act.target_x}, {act.target_y}, {act.target_z}) | {act.rationale}")

    # 2. Ejecución con chequeo de invariantes de seguridad en A_safe(s)
    print("\n2. EXECUTING IN REAL-TIME CONTROL LOOP WITH SAFETY ENFORCEMENT:")
    trace = agent.execute_plan(plan)
    for t in trace:
        print(f"   Step {t['step']}: {t['status']} {t['action']} {t.get('target', '')} (Lat: {t.get('latency_ms', 0)}ms)")

    # 3. Demostración de interrupción por seguridad (Worker entra en el perímetro)
    print("\n3. SAFETY INVARIANT INTERRUPT DEMO (Human worker steps within 0.8m):")
    agent.world_model.set_human_distance(0.8)
    trace_interrupt = agent.execute_plan(plan)
    for t in trace_interrupt:
        if "REJECTED" in t['status']:
            print(f"   [HALT] {t['action']} -> {t['reason']}")