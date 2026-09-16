from typing import Dict, Any, Optional
from gap_detector import KnowledgeGapDetector, KnowledgeGap
from hypothesis_generator import ScientificHypothesisGenerator
from experiment_tracker import ExperimentTracker

class ScientificDiscoveryAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.gap_detector = KnowledgeGapDetector()
        self.hypothesis_gen = ScientificHypothesisGenerator(api_key=api_key)
        self.tracker = ExperimentTracker()

    def run_discovery_cycle(self, domain_theme: str) -> Dict[str, Any]:
        gaps = self.gap_detector.detect_candidate_gaps(domain_theme)
        top_gap = gaps[0]

        hypotheses = self.hypothesis_gen.formulate_hypotheses(top_gap)
        primary_hypothesis = hypotheses[0]

        # Convertir lista de predicciones a diccionario para comparación
        predicted_dict = {
            item.property_name: item.predicted_value
            for item in primary_hypothesis.experimental_protocol.expected_target_properties
        }

        simulated_lab_measurements = {
            "glass_transition_temp_c": 358.0,
            "elongation_at_break_pct": 16.2
        }

        evaluation = self.tracker.record_and_evaluate(
            hypothesis_id=primary_hypothesis.hypothesis_id,
            predicted=predicted_dict,
            measured=simulated_lab_measurements
        )

        return {
            "gap": top_gap,
            "hypothesis": primary_hypothesis,
            "evaluation": evaluation
        }