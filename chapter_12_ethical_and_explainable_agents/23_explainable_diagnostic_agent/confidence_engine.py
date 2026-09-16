from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CalibratedConfidence:
    primary_probability: float
    confidence_tier: str  # 'HIGH', 'MODERATE', 'LOW - ESCALATE'
    epistemic_uncertainty: float  # Model knowledge gap
    aleatoric_uncertainty: float  # Inherent data noise

class ConfidenceAwareEngine:
    """
    Calibrates confidence scores and separates epistemic from aleatoric uncertainty.
    """
    def calibrate(self, raw_score: float, evidence_completeness: float) -> CalibratedConfidence:
        # Scale score
        calibrated = round(raw_score * 0.95, 2)
        epistemic = round((1.0 - evidence_completeness) * 0.4, 2)
        aleatoric = 0.05

        if calibrated >= 0.85:
            tier = "HIGH"
        elif calibrated >= 0.70:
            tier = "MODERATE"
        else:
            tier = "LOW - ESCALATE"

        return CalibratedConfidence(
            primary_probability=calibrated,
            confidence_tier=tier,
            epistemic_uncertainty=epistemic,
            aleatoric_uncertainty=aleatoric
        )