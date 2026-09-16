import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from dotenv import load_dotenv, find_dotenv
from drone_supervisor import DroneMissionSupervisor

load_dotenv(find_dotenv())

if __name__ == "__main__":
    supervisor = DroneMissionSupervisor()
    corridor = "CENTERPOINTE_TO_OTTAWA_RIVER"

    print("=== Domain-Transforming Integration Agent (Breadth Architecture) ===")
    print(f"Evaluating Mission Corridor: {corridor} (Ottawa Winter Operation)\n")

    # 1. Propagación de influencia en el Grafo de Conocimiento Interdominio
    print("1. CROSS-DOMAIN DEPENDENCY INFLUENCE PROPAGATION (Source: 'Subzero_Weather'):")
    cascade = supervisor.analyze_cascade_impact("Subzero_Weather")
    for node, (strength, path) in cascade.items():
        print(f"   * Node: {node:<26} | Impact: {strength*100:5.1f}% | Path: {' -> '.join(path)}")

    # 2. Caso Nominal de Invierno: -6.2°C, 18.5 km/h, 82% Batería, Sin NOTAMs, Autorizado
    print("\n2. UNIFIED CONSTRAINT ENVELOPE (Nominal Winter Flight Case):")
    nominal_envelope = supervisor.assess_mission(corridor, temp_c=-6.2, wind_kmh=18.5, soc=0.82, notams=0, parks_auth=True)
    print(f"   Unified Envelope Green: {nominal_envelope.unified_envelope_green}")
    print(f"   Go / No-Go Decision:    [{nominal_envelope.go_no_go_decision}]")
    for d in nominal_envelope.domains:
        status_str = "[OK]" if d.is_satisfied else "[FAIL]"
        print(f"     {status_str} {d.domain_name:<36}: {d.details}")

    # 3. Caso Severo con Fusión Conservadora: Temperatura -11.5°C (< -10°C umbral)
    print("\n3. CONSERVATIVE CONSTRAINT FUSION REJECTION DEMO (Extreme Cold: -11.5°C):")
    abort_envelope = supervisor.assess_mission(corridor, temp_c=-11.5, wind_kmh=18.5, soc=0.82, notams=0, parks_auth=True)
    print(f"   Unified Envelope Green: {abort_envelope.unified_envelope_green}")
    print(f"   Go / No-Go Decision:    [{abort_envelope.go_no_go_decision}]")
    for d in abort_envelope.domains:
        if not d.is_satisfied:
            print(f"     [VETO TRIGGERED] {d.domain_name}: {d.details}")