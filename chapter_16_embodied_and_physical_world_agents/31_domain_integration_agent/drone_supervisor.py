import os
import sys
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from knowledge_graph import HeterogeneousDomainGraph
from constraint_envelope import evaluate_envelope, UnifiedConstraintEnvelope

class DroneMissionSupervisor:
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.graph = HeterogeneousDomainGraph()
        self._setup_graph()

    def _setup_graph(self):
        # Relaciones entre dominios en el corredor Nepean - Ottawa River
        self.graph.add_edge("Subzero_Weather", "Battery_Discharge_Rate", "accelerates", 0.85)
        self.graph.add_edge("Battery_Discharge_Rate", "Flight_Duration_Budget", "constrains", 0.90)
        self.graph.add_edge("NOTAM_Alert_Zone", "Corridor_Segment_3", "blocks", 1.00)
        self.graph.add_edge("Corridor_Segment_3", "Mission_Timeline", "delays", 0.75)

    def analyze_cascade_impact(self, disruption_source: str) -> dict:
        return self.graph.propagate_influence(disruption_source, initial_strength=1.0, threshold=0.2)

    def assess_mission(self, corridor_id: str, temp_c: float, wind_kmh: float, soc: float, notams: int, parks_auth: bool) -> UnifiedConstraintEnvelope:
        return evaluate_envelope(corridor_id, temp_c, wind_kmh, soc, notams, parks_auth)