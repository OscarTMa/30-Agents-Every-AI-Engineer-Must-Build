import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from discovery_agent import ScientificDiscoveryAgent

load_dotenv(find_dotenv())

if __name__ == "__main__":
    agent = ScientificDiscoveryAgent()
    domain = "High-temperature aerospace flexible polymers"

    print("=== Scientific Discovery Agent Initialized ===")
    print(f"Initiating autonomous literature gap mining for: '{domain}'...\n")

    discovery_result = agent.run_discovery_cycle(domain)
    gap = discovery_result["gap"]
    hyp = discovery_result["hypothesis"]
    eval_res = discovery_result["evaluation"]

    print("="*80)
    print(f"1. TARGET KNOWLEDGE GAP IDENTIFIED [{gap.gap_id}]")
    print(f"   Domain:       {gap.domain} ({gap.gap_type})")
    print(f"   Description:  {gap.description}")
    print(f"   Novelty:      {gap.novelty_score*100:.0f}% | Feasibility: {gap.feasibility_score*100:.0f}%")
    print("="*80)

    print(f"\n2. ABDUCTIVE HYPOTHESIS FORMULATION [{hyp.hypothesis_id}]")
    print(f"   Title:        {hyp.formulation_name}")
    print(f"   Rationale:    {hyp.abductive_rationale}")
    print(f"   Novelty:      {hyp.novelty_assessment}")

    print("\n3. EXPERIMENTAL PROTOCOL & IN-SILICO PREDICTIONS:")
    print(f"   Procedure:    {hyp.experimental_protocol.synthesis_procedure}")
    print(f"   Techniques:   {hyp.experimental_protocol.characterization_techniques}")
    print(f"   Predictions:  {hyp.experimental_protocol.expected_target_properties}")

    print("\n" + "="*80)
    print("4. CLOSED-LOOP PHYSICAL LAB MEASUREMENT & EVALUATION")
    print("="*80)
    print(f"   Measured Lab Results: {eval_res.measured_properties}")
    print(f"   Prediction Errors:    {eval_res.error_percentages}")