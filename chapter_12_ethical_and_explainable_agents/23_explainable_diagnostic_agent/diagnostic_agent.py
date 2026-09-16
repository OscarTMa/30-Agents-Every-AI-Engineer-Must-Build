from typing import Dict, Any, Optional
from logger import DecisionLogger
from confidence_engine import ConfidenceAwareEngine
from explainer import ClinicalExplainer, AudienceExplanations

class DiagnosticAssistantAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.logger = DecisionLogger()
        self.confidence_engine = ConfidenceAwareEngine()
        self.explainer = ClinicalExplainer(api_key=api_key)

    def diagnose_and_explain(self, vitals: Dict[str, Any], symptoms: list[str]) -> Dict[str, Any]:
        # Step 1: Record Input Stage
        self.logger.record_step("Evidence_Ingestion", {"vitals": vitals, "symptoms": symptoms})

        # Step 2: Diagnostic Synthesis (Simulated Clinical Assessment)
        diagnosis = "Community-Acquired Pneumonia"
        feature_attributions = {
            "chest_imaging_consolidation": 0.35,
            "elevated_wbc_count": 0.28,
            "productive_cough_fever_4d": 0.22,
            "spo2_oxygen_drop_to_92pct": 0.15
        }
        self.logger.record_step("Feature_Attribution", feature_attributions)

        # Step 3: Confidence Calibration
        confidence = self.confidence_engine.calibrate(raw_score=0.92, evidence_completeness=0.90)
        self.logger.record_step("Confidence_Calibration", {
            "prob": confidence.primary_probability,
            "tier": confidence.confidence_tier,
            "epistemic": confidence.epistemic_uncertainty
        })

        # Step 4: Audience-Adapted Explanation Generation
        explanations = self.explainer.generate_explanations(
            diagnosis=diagnosis,
            feature_attributions=feature_attributions,
            confidence=confidence.primary_probability
        )
        self.logger.record_step("Explanation_Synthesis", {
            "clinician": explanations.clinician_explanation,
            "patient": explanations.patient_explanation
        })

        return {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "feature_attributions": feature_attributions,
            "explanations": explanations,
            "audit_trail": self.logger.export_audit_trail()
        }