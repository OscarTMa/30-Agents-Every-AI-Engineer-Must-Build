import sys
from pathlib import Path
from datetime import datetime

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from models import ZoneConfig, ZoneType, SensorReading
from building_agent import SmartBuildingAgent

if __name__ == "__main__":
    agent = SmartBuildingAgent()

    # Configurar Zonas
    server_zone = ZoneConfig(zone_id="ZONE-SERVER-01", zone_type=ZoneType.SERVER_ROOM, target_temp_range=(64.0, 70.0), max_co2_ppm=800.0)
    office_zone = ZoneConfig(zone_id="ZONE-OFFICE-4B", zone_type=ZoneType.OFFICE, target_temp_range=(68.0, 74.0), max_co2_ppm=1000.0)

    agent.register_zone(server_zone)
    agent.register_zone(office_zone)

    now = datetime.now()

    # Ingestar lecturas con ruido para el cuarto de servidores (sobrecalentamiento)
    agent.ingest_reading("ZONE-SERVER-01", SensorReading("temperature", 81.5, now))
    agent.ingest_reading("ZONE-SERVER-01", SensorReading("temperature", 82.1, now))
    agent.ingest_reading("ZONE-SERVER-01", SensorReading("temperature", 80.9, now))
    agent.ingest_reading("ZONE-SERVER-01", SensorReading("co2", 450.0, now))

    # Ingestar lecturas para la oficina (CO2 alto y ocupación)
    agent.ingest_reading("ZONE-OFFICE-4B", SensorReading("temperature", 72.0, now))
    agent.ingest_reading("ZONE-OFFICE-4B", SensorReading("co2", 1250.0, now))
    agent.ingest_reading("ZONE-OFFICE-4B", SensorReading("motion", 1.0, now))

    print("=== Physical World Sensing & Smart Building Agent ===")
    print("Executing Sense-Model-Plan-Act Cognitive Cycles across Building Digital Twin...\n")

    for zid in ["ZONE-SERVER-01", "ZONE-OFFICE-4B"]:
        state, alerts, commands = agent.run_cognitive_cycle(zid)
        print("="*75)
        print(f"ZONE: {zid} ({agent.zones[zid].zone_type.value})")
        print(f"Fused Digital Twin State: Temp={state.temperature_f:.1f}°F, CO2={state.co2_ppm:.0f} ppm, Occupancy={state.occupancy_detected}")
        
        print("\nActive Alerts:")
        if alerts:
            for a in alerts:
                print(f"  * {a}")
        else:
            print("  * [NORMAL] All parameters within nominal range.")

        print("\nActuator Dispatches (Closed-Loop Proportional Control):")
        if commands:
            for c in commands:
                print(f"  -> Dispatch {c.actuator_type} @ {c.intensity_pct}% power")
        else:
            print("  -> System idle (within deadband hysteresis range).")
        print("="*75 + "\n")